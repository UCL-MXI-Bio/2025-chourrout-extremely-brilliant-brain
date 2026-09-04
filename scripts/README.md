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

- Each script can be run with the included `data`.
- Modify the path to make sure to point to the `data` folder.

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
2. Execute the main command
3. Most scripts prompt interactively for any choices, paths, or configuration options (using [`inquirer`](https://pypi.org/project/inquirer/)); scripts that download data will show the estimated download size and ask for confirmation before proceeding

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
<summary><code>converters/convert_16bit_to_32bit_nifti.py</code></summary>

- Inputs:
  - NIfTI file as 16-bit unsigned integer data type
- Description: cast a 16-bit unsigned integer data type NIfTI file into a 32-bit floating point data type NIfTI file while preserving the header and affine transform
- Outputs:
  - NIfTI file as 32-bit floating point data type

</details>

<details>
<summary><code>converters/convert_to_neuroglancer.py</code></summary>

Interactive CLI (prompts for which conversion to run, then the input/output paths): merges what used to be three separate scripts (`convert_brain_mask.py`, `convert_orientation_slice.py`, `convert_parcellation.py`).

- Inputs (selected via an interactive prompt):
  - **Brain mask**: binary TIFF file with the background set as 0 and the brain (including a safety margin to keep the meningeal blood vessels) as 1
  - **Orientation vectors**: 2D vector map `slice_0*.npy` from running the structure tensor (output of `cardiotensor/run.py`), as an RGBA TIFF
  - **Parcellation**: NIfTI 3D volume of the segmentation of the HiP-CT brain as a whole brain, as a TIFF
- Description: convert the selected input into a Neuroglancer precomputed volume format data source for rendering into Neuroglancer (brain mask additionally generates downsampled mips and meshes)
- Outputs:
  - Neuroglancer precomputed volume format data source (segmentation + meshes, RGBA image, or labels, depending on the selected conversion)

</details>

<details>
<summary><code>downloaders/download_hipct_data.py</code></summary>

Interactive CLI: merges what used to be two separate scripts (`extract_downsampled_data.py`, `extract_slab_as_tiff_stack.py`). Prompts for which download to run, the relevant parameters (pyramid downscaling level, or region-of-interest corners), and confirms before downloading (showing the estimated download size).

- Inputs:
  - none (parameters are entered interactively; sensible defaults are offered)
  - the transform files in `../transforms/*.lta` (used only by the downsampled-volume path, see below)
- Description: download HiP-CT brain data from its Google Cloud Storage OME-Zarr, either as a downsampled whole-brain volume or as a full-resolution region-of-interest crop
- Outputs:
  - **Downsampled whole-brain volume**: NIfTI file of the downsampled HiP-CT brain dataset, with the correct physical voxel size for the selected pyramid level (read from the dataset's own OME-NGFF metadata, not assumed), named following BIDS conventions (`sub-01_ses-01_sample-brain_res-<level>um[_space-<target>]_XPCT.nii.gz`). Also prompts for which space to align it to &mdash; native HiP-CT brain space (no alignment, corner-origin), MNI space, native MRI space, BigBrain space, or FastSurfer input space &mdash; by composing the level's voxel-to-physical scale with a level-agnostic physical-space transform read from `../transforms/*.lta` (see that folder's files for how each was derived and validated; the BigBrain one is best-effort and not yet fully verified). If FastSurfer input space is selected, also prompts whether to crop any axis over FastSurfer's 320-voxel-per-axis limit (a pure index crop, translation-adjusted, no resampling)
  - **Region of interest**: series of 2D images (sometimes referred to as a stack of slices) from the same 3D volume `slice_0*.tif`

</details>

<details>
<summary><code>converters/apply_transform.py</code></summary>

- Inputs:
  - NIfTI file whose header expresses one of the known spaces (native HiP-CT brain space, MNI space, native MRI space, or BigBrain space)
  - the transform files in `../transforms/*.lta`
- Description: rewrite a NIfTI file's affine header to express it in a different one of those spaces (interactively selected), composing or inverting the stored `.lta` files as needed; does not resample the voxel data, only the header
- Outputs:
  - the same NIfTI data with a new affine header, in the target space

</details>

<details>
<summary><code>downloaders/download_mri.py</code></summary>

Interactive CLI: merges what used to be two separate scripts (`download_mri.sh`, `download_masked_mri.sh`). Prompts for which MRI to download and confirms before downloading (showing the download size).

- Inputs:
  - none (selection and output path are entered interactively)
- Description: download the original or masked version of the 3T T2-weighted MRI
- Outputs:
  - NIfTI file of the selected 3T T2-weighted MRI into the `data` folder

</details>  

<details>
<summary><code>fastsurfer-docker/run.sh</code></summary>

- Inputs:
  - RAS-reoriented NIfTI file with max. 320 voxels per dimension
  - `docker-compose.yml` file for the Docker container
  - FreeSurfer license as `license.txt`
- Description: compute the parcellation of the brain using the deep-learning-enabled FastSurfer
- Outputs:
  - NIfTI 3D volume of the segmentation of the HiP-CT brain as a whole brain

</details>

<details>
<summary><code>hippunfold-docker/prepare_folder_structure_with_mri.sh</code></summary>

- Inputs:
  - NIfTI file of the original 3T T2-weighted MRI into the `data/` folder
- Description: create the folder structure as BIDS for HippUnfold
- Outputs:
  - folder structure as BIDS for the original 3T T2-weighted MRI into the `data/mri_as_bids/` folder

</details>

<details>
<summary><code>hippunfold-docker/run.sh</code></summary>

- Inputs:
  - folder structure as BIDS for the original 3T T2-weighted MRI into the `data/mri_as_bids/` folder
- Description: compute the parcellation of the hippocampi using the deep-learning-enabled HippUnfold
- Outputs:
  - series of NIfTI 3D volumes of the parcellation of the hippocampi in the HiP-CT brain

</details>
