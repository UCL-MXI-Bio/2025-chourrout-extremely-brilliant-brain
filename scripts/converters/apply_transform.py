import inquirer
import nibabel
import numpy as np
import nitransforms.linear
from pathlib import Path

TRANSFORMS_DIR = Path(__file__).resolve().parent.parent / "transforms"

# Each entry is (origin space, target space) -> LTA filename, applied as
# target_affine = matrix @ origin_affine. The reverse direction (target ->
# origin) is available automatically via the matrix inverse -- see
# find_transform(). Only these directly-available files (or their inverses)
# are matched; a space pair that needs composing more than one transform is
# reported as not existing yet rather than guessed at.
TRANSFORMS = {
    ("Native HiP-CT brain space", "MNI space"): "hipct_native_to_mni.lta",
    ("Native HiP-CT brain space", "Native MRI space"): "hipct_native_to_mri_native.lta",
    ("Native HiP-CT brain space", "BigBrain space"): "hipct_native_to_bigbrain.lta",
    ("Native MRI space", "MNI space"): "mri_native_to_mni.lta",
}

SPACES = sorted({space for pair in TRANSFORMS for space in pair})


def find_transform(origin, target):
    """Look up the matrix mapping origin -> target, using a direct .lta file
    if one exists, or the inverse of one if only the reverse direction is
    stored. Returns None if no direct match (in either direction) exists."""
    if (origin, target) in TRANSFORMS:
        matrix = nitransforms.linear.load(TRANSFORMS_DIR / TRANSFORMS[(origin, target)], fmt="fs").matrix
        return matrix
    if (target, origin) in TRANSFORMS:
        matrix = nitransforms.linear.load(TRANSFORMS_DIR / TRANSFORMS[(target, origin)], fmt="fs").matrix
        return np.linalg.inv(matrix)
    return None


def main():
    input_path = Path(inquirer.text(
        "Path to the input NIfTI file",
        default="../data/sub-01_ses-01_sample-brain_res-494um_XPCT.nii.gz",
    ))

    origin_space = inquirer.list_input(
        "Origin space of the input file (i.e. what its own header currently expresses)",
        choices=SPACES,
    )
    target_space = inquirer.list_input(
        "Target space to transform into",
        choices=[s for s in SPACES if s != origin_space],
    )

    matrix = find_transform(origin_space, target_space)
    if matrix is None:
        print(f"No transform from '{origin_space}' to '{target_space}' exists yet.")
        return

    image = nibabel.load(input_path)
    new_affine = matrix @ image.affine

    output_path = Path(inquirer.text(
        "Path to the output NIfTI file",
        default=str(input_path.with_name(f"{input_path.stem.split('.')[0]}_in-{target_space.split()[0].lower()}.nii.gz")),
    ))

    output_image = nibabel.Nifti1Image(image.get_fdata(), new_affine, header=image.header)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nibabel.save(output_image, output_path)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
