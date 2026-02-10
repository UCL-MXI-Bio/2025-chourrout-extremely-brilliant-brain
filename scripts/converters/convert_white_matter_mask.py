import tifffile as tiff
import os
from tqdm import tqdm
from cloudvolume import CloudVolume
from cloudvolume.lib import mkdir
from pathlib import Path
import numpy as np

image_filename = Path("input/123.52um_white-matter.tif")

is_zyx_instead_of_xyz = True

image_array = tiff.imread(image_filename)
image_shape = image_array.shape
dtype = image_array.dtype

print(f"Dataset shape: {image_shape}")
print(f"Dataset dtype: {dtype}")

output_dir = "output/whitematter.precomputed/"
output_dir = Path(output_dir)
mkdir(output_dir)

output_dir = output_dir.absolute().as_uri() + "/"

print(output_dir)

ebb_resolution_nm = 7720
binned_resolution_nm = ebb_resolution_nm * 16

# Create a CloudVolume object for the Neuroglancer precomputed format
info = CloudVolume.create_new_info(
	num_channels = 1,
	layer_type = 'segmentation', # 'image' or 'segmentation'
	data_type = 'uint8', # can pick any popular uint
	encoding = 'compresso', # see: https://github.com/seung-lab/cloud-volume/wiki/Compression-Choices
	resolution = [ binned_resolution_nm ] * 3, # X,Y,Z values in nanometers
	voxel_offset = [ 0, 0, 0 ], # values X,Y,Z values in voxels
	chunk_size = [ 256 ] * 3, # rechunk of image X,Y,Z in voxels
	volume_size = image_shape[::-1] if is_zyx_instead_of_xyz else image_shape, # X,Y,Z size in voxels
	max_mip = 4,
	factor = (2,2,2),
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

data_to_write = tiff.imread(image_filename).astype(np.uint8)

if is_zyx_instead_of_xyz:
	data_to_write = np.transpose(data_to_write, (2, 1, 0))[..., np.newaxis]
else:
	data_to_write = data_to_write[..., np.newaxis]
 


vol[:,:,:, 1] = data_to_write

# --------------------------

from taskqueue import LocalTaskQueue
import igneous.task_creation as tc

tq = LocalTaskQueue(parallel=True)
tasks = tc.create_downsampling_tasks(output_dir, mip=0, num_mips = 3, factor= (2,2,2), fill_missing=True, delete_black_uploads=True,sparse=True,memory_target=int(500e9))
tq.insert(tasks)
tq.execute()
# tasks = tc.create_mesh_manifest_tasks(output_dir)
# tq.insert(tasks)
# tq.execute()
print("Done!")