import nibabel
import numpy

n16 = nibabel.load("../demo_data/downsampled_data_uint16.nii.gz")

n32_header = n16.header
n32_header.set_data_dtype(numpy.float32)

n32 = nibabel.Nifti1Image(n16.get_fdata().astype(numpy.float32),n16.affine,n32_header)

nibabel.save(n32,"/autofs/space/lachesis_002/users/mc1504/2025-chourrout-extremely-brilliant-brain/scripts/demo_data/downsampled_data_float32.nii.gz")