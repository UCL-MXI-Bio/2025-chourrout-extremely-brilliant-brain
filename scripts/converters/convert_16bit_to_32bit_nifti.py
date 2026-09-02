import inquirer
import nibabel
import numpy

input_path = inquirer.text(
    "Path to the input 16-bit unsigned integer NIfTI file",
    default="../demo_data/downsampled_data_uint16.nii.gz",
)
output_path = inquirer.text(
    "Path to the output 32-bit floating point NIfTI file",
    default="../demo_data/downsampled_data_float32.nii.gz",
)

n16 = nibabel.load(input_path)

n32_header = n16.header
n32_header.set_data_dtype(numpy.float32)

n32 = nibabel.Nifti1Image(n16.get_fdata().astype(numpy.float32),n16.affine,n32_header)

nibabel.save(n32,output_path)