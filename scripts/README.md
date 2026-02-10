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
