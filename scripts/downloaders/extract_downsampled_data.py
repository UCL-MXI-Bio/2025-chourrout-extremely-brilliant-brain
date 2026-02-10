import dask.array
import gcsfs
import nibabel
import pathlib
import numpy as np

gcs_bucket_name = "ucl-hip-ct-ebb-hseid5pvpp8vgtzt"
path_to_data_in_gcs_bucket = "sub-01/ses-01/micr/sub-01_ses-01_sample-brain_XPCT.ome.zarr"
downscaling = 6

VOXEL_SIZE = (7.72*1e-3,) * 3 # in mm
VOXEL_UNIT = "mm"

output_path = pathlib.Path("../demo_data/downsampled_data_float32.nii.gz")

resource_link = f"gs://{gcs_bucket_name}/{path_to_data_in_gcs_bucket}/{downscaling}/"

downsampled_data = dask.array.from_zarr(resource_link)

# Catch a compatibility issue of FreeSurfer with the 16-bit unsigned integer
if downsampled_data.dtype is np.uint16:
    downsampled_data = downsampled_data.astype(np.float32)

nifti_header = nibabel.Nifti1Header()
nifti_header.set_data_dtype(downsampled_data.dtype)

# The following function is from: https://github.com/chourroutm/tiff_to_nifti/commit/ac14089d95134030a639b93e24dd7332c034eadf
def generate_affine(dimensions, voxel_size):
    """
    Generate an affine matrix for the given dimensions with respect to voxel size.
    
    Parameters:
    dimensions (tuple): The dimensions of the image (x, y, z).
    voxel_size (list): The size of each voxel (dx, dy, dz).

    Returns:
    numpy.ndarray: The generated affine matrix.
    """
    # Create an identity matrix
    affine = np.eye(4)

    # Set the voxel sizes
    affine[0, 0] = voxel_size[0]
    affine[1, 1] = voxel_size[1]
    affine[2, 2] = voxel_size[2]

    # Set the translation part to center the image
    affine[0, 3] = -dimensions[0] * voxel_size[0] / 2.0
    affine[1, 3] = -dimensions[1] * voxel_size[1] / 2.0
    affine[2, 3] = -dimensions[2] * voxel_size[2] / 2.0

    return affine

nifti_affine = generate_affine(downsampled_data.shape, VOXEL_SIZE)

nifti_image = nibabel.Nifti1Image(downsampled_data.compute(),nifti_affine,header=nifti_header)

nibabel.save(nifti_image,output_path)