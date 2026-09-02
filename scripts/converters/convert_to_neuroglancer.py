import numpy as np
import tifffile as tiff
import inquirer
from cloudvolume import CloudVolume
from cloudvolume.lib import mkdir
from pathlib import Path

EBB_RESOLUTION_NM = 7720

CONVERSION_TYPES = {
    "Brain mask (segmentation, with meshing)": "brain_mask",
    "Structure-tensor orientation vectors (RGBA image)": "orientation_slice",
    "Parcellation (segmentation)": "parcellation",
}

DEFAULT_INPUT = {
    "brain_mask": "input/dilated_whole_brain_123umEBB_16102024.tif",
    # The file below is the output from the cardiotensor/run.py script
    "orientation_slice": "input/vectors_rgba_sigma3_rho6_slice-10774.tif",
    "parcellation": "input/494um_EBB_fastsurfer.tif",
}

DEFAULT_OUTPUT = {
    "brain_mask": "output/mask.precomputed/",
    "orientation_slice": "output/orientations_slice.precomputed/",
    "parcellation": "output/segmentation.precomputed/",
}


def convert_brain_mask(image_filename, output_dir):
    is_zyx_instead_of_xyz = False

    first_image = tiff.imread(image_filename)
    img_shape = first_image.shape
    dtype = first_image.dtype

    print(f"Dataset shape: {img_shape}")
    print(f"Dataset dtype: {dtype}")

    mkdir(output_dir)
    output_dir_uri = output_dir.absolute().as_uri() + "/"
    print(output_dir_uri)

    binned_resolution_nm = EBB_RESOLUTION_NM * 16

    # Create a CloudVolume object for the Neuroglancer precomputed format
    info = CloudVolume.create_new_info(
        num_channels = 1,
        layer_type = 'segmentation', # 'image' or 'segmentation'
        data_type = 'uint8', # can pick any popular uint
        encoding = 'compresso', # see: https://github.com/seung-lab/cloud-volume/wiki/Compression-Choices
        resolution = [ binned_resolution_nm ] * 3, # X,Y,Z values in nanometers
        voxel_offset = [ 0, 0, 0 ], # values X,Y,Z values in voxels
        chunk_size = [ 256 ] * 3, # rechunk of image X,Y,Z in voxels
        volume_size = img_shape[::-1] if is_zyx_instead_of_xyz else img_shape, # X,Y,Z size in voxels
        max_mip = 4,
        factor = (2,2,2),
    )
    vol = CloudVolume(
        output_dir_uri,
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

    from taskqueue import LocalTaskQueue
    import igneous.task_creation as tc

    tq = LocalTaskQueue(parallel=True)
    tasks = tc.create_downsampling_tasks(output_dir_uri, mip=0, num_mips = 3, factor= (2,2,2), fill_missing=True, delete_black_uploads=True,sparse=True,memory_target=int(500e9))
    tq.insert(tasks)
    tq.execute()
    print("Done!")

    tq = LocalTaskQueue(parallel=True)
    tasks = tc.create_meshing_tasks(output_dir_uri, mip=0, shape=(256, 256, 256), fill_missing=True, sharded=False)
    tq.insert(tasks)
    tq.execute()
    tasks = tc.create_unsharded_multires_mesh_tasks(output_dir_uri)
    tq.insert(tasks)
    tq.execute()
    tasks = tc.create_mesh_manifest_tasks(output_dir_uri)
    tq.insert(tasks)
    tq.execute()
    print("Done!")

    vol.commit_info()


def convert_orientation_slice(image_filename, output_dir):
    data_to_write = tiff.imread(image_filename).astype(np.uint8)

    data_to_write = data_to_write[...,np.newaxis].transpose((1,2,3,0))

    data_to_write = np.fliplr(data_to_write)

    print(f"Writing data of shape: {data_to_write.shape}")

    mkdir(output_dir)
    output_dir_uri = output_dir.absolute().as_uri() + "/"
    print(output_dir_uri)

    # Create a CloudVolume object for the Neuroglancer precomputed format
    info = CloudVolume.create_new_info(
        num_channels = 4,
        layer_type = 'image', # 'image' or 'segmentation'
        data_type = 'uint8', # can pick any popular uint
        encoding = 'raw', # see: https://github.com/seung-lab/cloud-volume/wiki/Compression-Choices
        resolution = [ EBB_RESOLUTION_NM ] * 3, # X,Y,Z values in nanometers
        voxel_offset = [ 1441, 1113, 10774 ], # values X,Y,Z values in voxels
        chunk_size = [ 2048, 2048, 1 ], # rechunk of image X,Y,Z in voxels
        volume_size =  data_to_write.shape[:-1], # X,Y,Z size in voxels
        max_mip = 0,
        factor = (2,2,2),
    )

    vol = CloudVolume(
        output_dir_uri,
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


def convert_parcellation(image_filename, output_dir):
    image_array = tiff.imread(image_filename)
    image_shape = image_array.shape
    dtype = image_array.dtype

    print(f"Dataset shape: {image_shape}")
    print(f"Dataset dtype: {dtype}")

    mkdir(output_dir)
    output_dir_uri = output_dir.absolute().as_uri() + "/"
    print(output_dir_uri)

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
        output_dir_uri,
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


CONVERTERS = {
    "brain_mask": convert_brain_mask,
    "orientation_slice": convert_orientation_slice,
    "parcellation": convert_parcellation,
}


def main():
    answer = inquirer.list_input(
        "What would you like to convert to the Neuroglancer precomputed format?",
        choices=list(CONVERSION_TYPES.keys()),
    )
    conversion_type = CONVERSION_TYPES[answer]

    image_filename = Path(inquirer.text(
        "Path to the input TIFF file",
        default=DEFAULT_INPUT[conversion_type],
    ))
    output_dir = Path(inquirer.text(
        "Output directory for the Neuroglancer precomputed volume",
        default=DEFAULT_OUTPUT[conversion_type],
    ))

    CONVERTERS[conversion_type](image_filename, output_dir)


if __name__ == "__main__":
    main()
