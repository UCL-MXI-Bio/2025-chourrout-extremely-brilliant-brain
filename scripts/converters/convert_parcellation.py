import tifffile as tiff
import os
from tqdm.notebook import tqdm
from cloudvolume import CloudVolume
from cloudvolume.lib import mkdir
from pathlib import Path
import numpy as np

image_filename = Path("input/494um_EBB_fastsurfer.tif")

image_array = tiff.imread(image_filename)
image_shape = image_array.shape
dtype = image_array.dtype

print(f"Dataset shape: {image_shape}")
print(f"Dataset dtype: {dtype}")

output_dir = "output/segmentation.precomputed/"
output_dir = Path(output_dir)
mkdir(output_dir)

output_dir = output_dir.absolute().as_uri() + "/"

print(output_dir)

ebb_resolution_nm = 7720
binned_resolution_nm = 494080

# Create a CloudVolume object for the Neuroglancer precomputed format
info = CloudVolume.create_new_info(
	num_channels = 1,
	layer_type = 'segmentation', # 'image' or 'segmentation'
	data_type = 'uint16', # can pick any popular uint
	encoding = 'compresso', # see: https://github.com/seung-lab/cloud-volume/wiki/Compression-Choices
	resolution = [ binned_resolution_nm ] * 3, # X,Y,Z values in nanometers
	voxel_offset = [ 0, 0, 0 ], # values X,Y,Z values in voxels
	chunk_size = [ 64 ] * 3, # rechunk of image X,Y,Z in voxels
	volume_size = image_shape, # X,Y,Z size in voxels
)
vol = CloudVolume(
    output_dir,
    info=info,
    progress=False,
    parallel=False,
    cache_locking=True,
    compress=False,
    delete_black_uploads = True,
)

vol.commit_info()

print("CloudVolume info:")
print(vol.info)

chunk_data = tiff.imread(image_filename).astype(image_array.dtype)

chunk_data = chunk_data[..., np.newaxis]

vol[:,:,:] = chunk_data