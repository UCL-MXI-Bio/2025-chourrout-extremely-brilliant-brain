# Scripts

## System Requirements

### Software Dependencies
Each individual Python script has its own dependencies. E.g. for `cardiotensor/run.py`, install the dependencies listed in the `cardiotensor/requirements.txt` file.

### Operating Systems
- Supported operating systems (with versions):
  - Ubuntu 20.04 LTS
  - Ubuntu 22.04 LTS
  - Ubuntu 22.04 LTS as Windows Subsystem for Linux 2 on Windows 11

### Tested Versions
- Versions and environments the software has been tested on:
  - OS: Ubuntu 20.04 LTS, Ubuntu 22.04 LTS
  - Dependency versions: use the relevant `requirements.txt` file
  - Compiler/runtime versions: gcc 9.4.0, gcc 11.4.0

### Hardware Requirements
Some portions of the code &mdash; such as `cardiotensor` &mdash; have been developed for multi-threading on the GPU, which requires a CUDA-enabled Nvidia GPU. Nevertheless, these will fallback to CPU multi-threads if CUDA is not detected, and they will be significantly slower.

The demo code is meant to run on any computer by using a smaller demo crop from the actual data. However, some portions of the code &mdash; such as `cardiotensor` &mdash; have been tailored to run on 1 TB RAM workstations.

## Installation Guide

### Installation Instructions
As portions of the code interact together, it is recommended to download the whole repository:
```bash
git clone https://github.com/UCL-MXI-Bio/2025-chourrout-extremely-brilliant-brain
cd 2025-chourrout-extremely-brilliant-brain/scripts/
````

The preferred method to run the Python scripts is to use the new environment manager, `uv` (https://docs.astral.sh/uv/). To install `uv` in a local account (this does not require admin access), run the _standalone installer_ from their website: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

### Typical Install Time

* Approximate installation time on a “normal” desktop computer:

  * 5–10 minutes

## Demo

### Instructions to Run the Demo

- Each script can be run with the included `demo_data`.
- Modify the path to make sure to point to the `demo_data` folder.

### Expected Output

* Description of the expected output:

  * Output formats: either TIFF, NIfTI, .npy (NumPy array) or the [precomputed Neuroglancer format](https://github.com/google/neuroglancer/tree/master/src/datasource/precomputed)
  * Visualizations: 
    * TIFF and NIfTI files can be opened with [Fiji](https://fiji.sc)
    * NIfTI files can be opened with [FreeSurfer](https://freesurfer.net)
    * .npy (NumPy array) files can be opened with [napari](https://napari.org/stable/)
    * the [precomputed Neuroglancer format](https://github.com/google/neuroglancer/tree/master/src/datasource/precomputed) is specifically meant for Neuroglancer

### Expected Runtime

* Approximate runtime on a “normal” desktop computer:

  * 60 seconds

## Instructions for Use

### Running the Software on Your Own Data

1. Prepare your input data according to the required format
2. Start the virtual environment specific to the folder (e.g. using `uv`)
2. Specify input/output paths and configuration options
3. Execute the main command

```bash
# Example
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python run.py
```

## Detailed input/output and description per script

<details>
<summary><code>cardiotensor/run.py</code></summary>

- Inputs:
  - configuration file `cardiotensor_*.conf`
  - series of 2D images (sometimes referred to as a stack of slices) from the same 3D volume `slice_0*.tif`
- Description: compute the struture tensor of the image intensity gradient to determine 3D orientations of the structures in the image
- Outputs:
  - series of 2D vector maps `slice_0*.npy` (matching each input 2D image)

</details>

<details>
<summary><code>cardiotensor/run.py</code></summary>

- Inputs:
  - configuration file `cardiotensor_*.conf`
  - series of 2D images (sometimes referred to as a stack of slices) from the same 3D volume `slice_0*.tif`
- Description: compute the struture tensor of the image intensity gradient to determine 3D orientations of the structures in the image
- Outputs:
  - series of 2D vector maps `slice_0*.npy` (matching each input 2D image)

</details>

<details>
<summary><code>converters/convert_16bit_to_32bit_nifti.py</code></summary>

- Inputs:
  - NIfTI file as 16-bit unsigned integer data type
- Description: cast a 16-bit unsigned integer data type NIfTI file into a 32-bit floating point data type NIfTI file while preserving the header and affine transform
- Outputs:
  - NIfTI file as 32-bit floating point data type

</details>

<details>
<summary><code>converters/convert_brain_mask.py</code></summary>

- Inputs:
  - binary TIFF file with the background set as 0 and the brain (including a safety margin to keep the meningeal blood vessels) as 1
- Description: convert a binary TIFF file of the appropriate dimensions into a Neuroglancer precomputed volume format data source for rendering into Neuroglancer, including meshes
- Outputs:
  - Neuroglancer precomputed volume format data source including meshes for rendering into Neuroglancer

</details>

<details>
<summary><code>converters/convert_orientation_slice.py</code></summary>

- Inputs:
  - 2D vector map `slice_0*.npy` from running the structure tensor
  - resampled binary TIFF file with the background set as 0 and the brain (including a safety margin to keep the meningeal blood vessels) as 1
- Description: convert a 2D vector field into a red-green-blue-opacity (RGBA) Neuroglancer precomputed volume format data source for rendering into Neuroglancer
- Outputs:
  - Neuroglancer precomputed volume format data source as RGBA for rendering into Neuroglancer

</details>

<details>
<summary><code>converters/convert_parcellation.py</code></summary>

- Inputs:
  - NIfTI 3D volume of the segmentation of EBB as a whole brain
- Description: convert a 3D segmentation into a Neuroglancer precomputed volume format data source for rendering into Neuroglancer
- Outputs:
  - Neuroglancer precomputed volume format data source as labels for rendering into Neuroglancer

</details>

<details>
<summary><code>downloaders/extract_downsampled_data.py</code></summary>

- Inputs:
  - none
- Description: download a pre-determined downsampled version of the EBB dataset
- Outputs:
  - NIfTI file of the downsampled version of the EBB dataset

</details>

<details>
<summary><code>downloaders/extract_slab_as_tiff_stack.py</code></summary>

- Inputs:
  - none
- Description: download a pre-determined region of interest of the EBB dataset at full resolution
- Outputs:
  - series of 2D images (sometimes referred to as a stack of slices) from the same 3D volume `slice_0*.tif`

</details>

<details>
<summary><code>downloaders/download_mri.sh</code> & <code>downloaders/download_masked_mri.sh</code></summary>

- Inputs:
  - none
- Description: download the original (resp. masked) version of the 3T T2-weighted MRI
- Outputs:
  - NIfTI file of the original (resp. masked) 3T T2-weighted MRI into the `data` folder

</details>  

<details>
<summary><code>fastsurfer-docker/run.sh</code></summary>

- Inputs:
  - RAS-reoriented NIfTI file with max. 320 voxels per dimension
  - `docker-compose.yml` file for the Docker container
  - FreeSurfer license as `license.txt`
- Description: compute the parcellation of the brain using the deep-learning-enabled FastSurfer
- Outputs:
  - NIfTI 3D volume of the segmentation of EBB as a whole brain

</details>

<details>
<summary><code>hippunfold-docker/prepare_folder_structure_with_mri.sh</code></summary>

- Inputs:
  - NIfTI file of the original 3T T2-weighted MRI into the `data/` folder
- Description: create the folder structure as BIDS for HippUnfold
- Outputs:
  - folder structure as BIDS for the original 3T T2-weighted MRI into the `data/ebb-mri_as_bids/` folder

</details>

<details>
<summary><code>hippunfold-docker/prepare_folder_structure_with_mri.sh</code></summary>

- Inputs:
  - folder structure as BIDS for the original 3T T2-weighted MRI into the `data/ebb-mri_as_bids/` folder
- Description: compute the parcellation of the hippocampi using the deep-learning-enabled HippUnfold
- Outputs:
  - series of NIfTI 3D volumes of the parcellation of the hippocampi in EBB

</details>
