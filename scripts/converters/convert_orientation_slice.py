import tifffile as tiff
import os
from tqdm import tqdm
from cloudvolume import CloudVolume
from cloudvolume.lib import mkdir
from pathlib import Path
import numpy as np

# The file below is the output from the cardiotensor/run.py script
image_filename = Path("input/vectors_rgba_sigma3_rho6_slice-10774.tif")

data_to_write = tiff.imread(image_filename).astype(np.uint8)

data_to_write = data_to_write[...,np.newaxis].transpose((1,2,3,0))

data_to_write = np.fliplr(data_to_write)

print(f"Writing data of shape: {data_to_write.shape}")

output_dir = "output/orientations_slice.precomputed/"
output_dir = Path(output_dir)
mkdir(output_dir)

output_dir = output_dir.absolute().as_uri() + "/"

print(output_dir)

ebb_resolution_nm = 7720

# Create a CloudVolume object for the Neuroglancer precomputed format
info = CloudVolume.create_new_info(
	num_channels = 4,
	layer_type = 'image', # 'image' or 'segmentation'
	data_type = 'uint8', # can pick any popular uint
	encoding = 'raw', # see: https://github.com/seung-lab/cloud-volume/wiki/Compression-Choices
	resolution = [ ebb_resolution_nm ] * 3, # X,Y,Z values in nanometers
	voxel_offset = [ 1441, 1113, 10774 ], # values X,Y,Z values in voxels
	chunk_size = [ 2048, 2048, 1 ], # rechunk of image X,Y,Z in voxels
	volume_size =  data_to_write.shape[:-1], # X,Y,Z size in voxels
	max_mip = 0,
	factor = (2,2,2),
)

vol = CloudVolume(
	output_dir,
	info=info,
	progress=False,
	parallel=False,
	cache_locking=True,
	compress=False,
	delete_black_uploads = True
)

vol.commit_info()

print("CloudVolume info:")
print(vol.info)

vol[:,:,:,:] = data_to_write