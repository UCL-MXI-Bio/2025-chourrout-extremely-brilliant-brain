import dask
import dask.array
import inquirer
import nibabel
import nitransforms.linear
import numpy as np
import tifffile as tiff
from dask import delayed
from pathlib import Path
from tqdm.dask import TqdmCallback

GCS_BUCKET_NAME = "ucl-hip-ct-ebb-hseid5pvpp8vgtzt"
PATH_TO_DATA_IN_GCS_BUCKET = "sub-01/ses-01/micr/sub-01_ses-01_sample-brain_XPCT.ome.zarr"

# The bucket is public; requesting anonymous access explicitly skips gcsfs's
# slow default-credentials probe (which can take a long time to fail before
# falling back to anonymous access on its own).
GCS_STORAGE_OPTIONS = {"token": "anon"}

# Per-level isotropic voxel size in micrometers, read directly from the dataset's
# own OME-NGFF .zattrs (multiscales[0].datasets[*].coordinateTransformations),
# not assumed. Axes there are (x, y, z), matching NIfTI's own (i, j, k) order.
LEVEL_VOXEL_SIZE_UM = {
    0: 7.72,
    1: 15.44,
    2: 30.88,
    3: 61.76,
    4: 123.52,
    5: 247.04,
    6: 494.08,
    7: 988.16,
    8: 1976.32,
}

# Levels offered for download here. Levels 0-3 are excluded: they're multiple
# GB to TB at this resolution, impractical for this convenience downloader --
# use the Human Organ Atlas data portal for full-resolution data instead (see
# the main menu).
DOWNLOADABLE_LEVELS = [4, 5, 6, 7, 8]

# Alignment chains: each is a level-agnostic 4x4 matrix mapping native HiP-CT brain
# PHYSICAL space (mm, corner-origin: voxel (0,0,0) -> RAS (0,0,0), any pyramid
# level) to the target space's RAS(mm) -- no per-level rescaling needed, since
# both sides are already physical. Stored as RAS_TO_RAS LTA files, written and
# read via nitransforms (see transforms/*.lta for provenance and derivation
# notes for each).
TRANSFORMS_DIR = Path(__file__).resolve().parent.parent / "transforms"
ALIGNMENT_TARGETS = {
    "MNI space": "hipct_native_to_mni.lta",
    "Native MRI space": "hipct_native_to_mri_native.lta",
    "BigBrain space": "hipct_native_to_bigbrain.lta",
    "FastSurfer input space": "hipct_native_to_fastsurfer_input.lta",
}

PHYSICAL_ALIGNMENT_CHAINS = {
    name: nitransforms.linear.load(TRANSFORMS_DIR / filename, fmt="fs").matrix
    for name, filename in ALIGNMENT_TARGETS.items()
}

# BIDS `space-<label>` entity values for each alignment target (labels must be
# alphanumeric, no dashes/underscores). "Native HiP-CT brain space (no
# alignment)" has no entry -- the space- entity is simply omitted for that
# case, per BIDS convention for data in its own acquisition space.
SPACE_LABELS = {
    "MNI space": "MNI",
    "Native MRI space": "T2w",
    "BigBrain space": "BigBrain",
    "FastSurfer input space": "FSInput",
}


def bids_filename(level, alignment=None, desc=None, suffix="XPCT", ext=".nii.gz"):
    """BIDS-style filename for a downloaded/derived HiP-CT volume, consistent
    with this dataset's own source naming (sub-01_ses-01_sample-brain_XPCT.ome.zarr,
    see PATH_TO_DATA_IN_GCS_BUCKET) and with download_mri.py's output names
    (sub-01_ses-02_T2w.nii.gz, sub-01_ses-02_desc-masked_T2w.nii.gz)."""
    entities = ["sub-01", "ses-01", "sample-brain"]
    if level is not None:
        entities.append(f"res-{round(LEVEL_VOXEL_SIZE_UM[level])}um")
    if alignment is not None and alignment in SPACE_LABELS:
        entities.append(f"space-{SPACE_LABELS[alignment]}")
    if desc is not None:
        entities.append(f"desc-{desc}")
    return "_".join(entities) + f"_{suffix}{ext}"


# FastSurfer's bounding-box limit (see scripts/README.md's note on
# fastsurfer-docker/run.sh's input requirements).
FASTSURFER_MAX_DIM = 320


def crop_to_fastsurfer_limit(data, affine):
    """Symmetrically crop any axis exceeding FASTSURFER_MAX_DIM voxels down to
    exactly that size, adjusting the affine's translation to match (a pure
    index crop, no resampling -- physical space and voxel size are
    unaffected). Matches the constraint FastSurfer's docker run.sh imposes on
    its --t1 input."""
    affine = affine.copy()
    slices = []
    for axis, size in enumerate(data.shape):
        if size > FASTSURFER_MAX_DIM:
            excess = size - FASTSURFER_MAX_DIM
            lo = excess // 2
            hi = lo + FASTSURFER_MAX_DIM
            slices.append(slice(lo, hi))
            affine[:3, 3] += affine[:3, axis] * lo
        else:
            slices.append(slice(None))
    return data[tuple(slices)], affine


def native_affine(level):
    """Corner-origin voxel-index -> native HiP-CT brain physical RAS(mm) affine at the
    given pyramid level (voxel (0,0,0) -> RAS (0,0,0))."""
    voxel_size_mm = LEVEL_VOXEL_SIZE_UM[level] * 1e-3
    return np.diag([voxel_size_mm, voxel_size_mm, voxel_size_mm, 1.0])


def align_affine(target, level):
    """Voxel-index -> target-space RAS(mm) affine at the given pyramid level:
    native physical space composed with the level-agnostic physical chain."""
    return PHYSICAL_ALIGNMENT_CHAINS[target] @ native_affine(level)


def download_downsampled_volume():
    downscaling = inquirer.list_input(
        "Pyramid downscaling level to download",
        choices=[(f"{LEVEL_VOXEL_SIZE_UM[level]} µm/voxel", level) for level in DOWNLOADABLE_LEVELS],
        default=6,
    )

    resource_link = f"gs://{GCS_BUCKET_NAME}/{PATH_TO_DATA_IN_GCS_BUCKET}/{downscaling}/"
    data = dask.array.from_zarr(resource_link, storage_options=GCS_STORAGE_OPTIONS)

    size_gb = data.nbytes / (1024 ** 3)
    if not inquirer.confirm(
        f"This will download an estimated {size_gb:.2f} GB (shape {data.shape}, dtype {data.dtype}). Continue?",
        default=True,
    ):
        print("Aborted.")
        return

    alignment = inquirer.list_input(
        "Align the downloaded volume to:",
        choices=["Native HiP-CT brain space (no alignment)"] + list(ALIGNMENT_TARGETS.keys()),
    )

    output_path = Path(inquirer.text(
        "Output NIfTI path",
        default=f"../data/{bids_filename(downscaling, alignment)}",
    ))

    # Catch a compatibility issue of FreeSurfer with the 16-bit unsigned integer
    if data.dtype == np.uint16:
        data = data.astype(np.float32)

    with TqdmCallback(desc="Downloading"):
        computed = data.compute()

    if alignment == "Native HiP-CT brain space (no alignment)":
        nifti_affine = native_affine(downscaling)
    else:
        nifti_affine = align_affine(alignment, downscaling)

    if alignment == "FastSurfer input space" and inquirer.confirm(
        f"FastSurfer has a {FASTSURFER_MAX_DIM}-voxel-per-axis input limit "
        f"(current shape {computed.shape}). Apply the crop?",
        default=True,
    ):
        computed, nifti_affine = crop_to_fastsurfer_limit(computed, nifti_affine)

    nifti_header = nibabel.Nifti1Header()
    nifti_header.set_data_dtype(computed.dtype)

    nifti_image = nibabel.Nifti1Image(computed, nifti_affine, header=nifti_header)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    nibabel.save(nifti_image, output_path)

    print(f"Saved to {output_path}")


def download_roi_slab():
    resource_link = f"gs://{GCS_BUCKET_NAME}/{PATH_TO_DATA_IN_GCS_BUCKET}/0/"
    dataset_full = dask.array.from_zarr(resource_link, storage_options=GCS_STORAGE_OPTIONS)

    margin = int(inquirer.text("Margin around the region of interest (voxels)", default="32"))
    lower_corner = tuple(int(x.strip()) for x in inquirer.text(
        "Lower corner, full-resolution voxel indices (x,y,z)", default="2325,1113,10774",
    ).split(","))
    upper_corner = tuple(int(x.strip()) for x in inquirer.text(
        "Upper corner, full-resolution voxel indices (x,y,z)", default="17268,17931,10774",
    ).split(","))
    lower_corner = tuple(c - margin for c in lower_corner)
    upper_corner = tuple(c + margin for c in upper_corner)

    data_slab = dataset_full[
        lower_corner[0]:upper_corner[0],
        lower_corner[1]:upper_corner[1],
        lower_corner[2]:upper_corner[2],
    ]

    size_gb = data_slab.nbytes / (1024 ** 3)
    output_path = Path(inquirer.text(
        "Output directory for the TIFF stack",
        default=f"../data/{bids_filename(level=0, desc='roi', ext='')}",
    ))

    if not inquirer.confirm(
        f"This will download an estimated {size_gb:.2f} GB across {data_slab.shape[2]} slices to {output_path}. Continue?",
        default=True,
    ):
        print("Aborted.")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    data_slab = data_slab.rechunk((upper_corner[0]-lower_corner[0],upper_corner[1]-lower_corner[1],1))

    # Prepare all computations in a list (lazy execution)
    lazy_results = []
    for i in range(data_slab.shape[2]):
        file_path = output_path / f"slice{(lower_corner[2]+i):05}_offset{lower_corner[0]:05}x{lower_corner[1]:05}x{lower_corner[2]:05}_idx{i:05}.tif"
        lazy_results.append(delayed(tiff.imwrite)(file_path, data_slab[:,:,i], mode="w", photometric='minisblack', imagej=True))

    # Execute in parallel
    with TqdmCallback(desc="Writing slices"):
        dask.compute(*lazy_results)

    print(f"Saved to {output_path}")


HOA_PORTAL_URL = "https://human-organ-atlas.esrf.fr/datasets/2270234369"


def main():
    answer = inquirer.list_input(
        "What would you like to download from the HiP-CT brain dataset?",
        choices=[
            "Downsampled whole-brain volume (NIfTI)",
            "Pre-set full-resolution region of interest (TIFF stack)",
            "Visit the Human Organ Atlas data portal",
        ],
    )
    if answer == "Downsampled whole-brain volume (NIfTI)":
        download_downsampled_volume()
    elif answer == "Pre-set full-resolution region of interest (TIFF stack)":
        download_roi_slab()
    else:
        print(
            "The full-resolution HiP-CT brain dataset (as JPEG2000 files at various voxel "
            f"sizes) is available from the Human Organ Atlas data portal:\n{HOA_PORTAL_URL}"
        )


if __name__ == "__main__":
    main()
