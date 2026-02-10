This data `downsampled_data_float32.nii.gz` can be downloaded using the script in `../converters/extract_downsampled_data.py`.

To apply the rotation stored as an LTA, one can use FreeSurfer's command:

```bash
mri_vol2vol --lta downsampled_data_float32_rotated.lta --no-resample --mov downsampled_data_float32.nii.gz --targ downsampled_data_float32.nii.gz --o downsampled_data_float32_rotated.nii.gz
```

As FastSurfer is limited by a $ 320 \times 320 \times 320 $ bounding box, the volume `downsampled_data_float32_rotated.nii.gz` has been cropped (from 336 voxels to 320 voxels) along the anterior-posterior axis and saved as `downsampled_data_float32_rotated_crop.nii.gz`.