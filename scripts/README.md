# Scripts

## System Requirements

### Software Dependencies
Each individual Python script has its own dependencies. E.g. for `run_cardiotensor.py`, install the dependencies listed in the `cardiotensor_requirements.txt`.

### Operating Systems
- Supported operating systems (with versions):
  - Ubuntu 20.04 LTS
  - Ubuntu 22.04 LTS
  - Ubuntu 22.04 LTS as Windows Subsystem for Linux 2 on Windows 11

### Tested Versions
- Versions and environments the software has been tested on:
  - OS: Ubuntu 20.04 LTS, Ubuntu 22.04 LTS
  - Dependency versions: use the relevant `*_requirements.txt` file
  - Compiler/runtime versions: gcc 9.4.0, gcc 11.4.0

### Hardware Requirements
Some portions of the code &mdash; such as `cardiotensor` &mdash; have been developed for multi-threading on the GPU, which requires a CUDA-enabled Nvidia GPU. Nevertheless, these will fallback to CPU multi-threads if CUDA is not detected, and they will be significantly slower.

The demo code is meant to run on any computer by using a smaller demo crop from the actual data. However, some portions of the code &mdash; such as `cardiotensor` &mdash; have been tailored to run on 1 TB RAM workstations.

## Installation Guide

### Installation Instructions
1. Step-by-step installation instructions
2. Environment setup (e.g., virtual environments, containers)
3. Configuration steps (if any)

```bash
# Example
git clone <repository-url>
cd <repository>
pip install -r requirements.txt
````

### Typical Install Time

* Approximate installation time on a “normal” desktop computer:

  * Example: 5–10 minutes

## Demo

### Instructions to Run the Demo

1. Navigate to the demo directory
2. Run the demo command on the provided sample data

```bash
# Example
python run_demo.py --input data/sample_input.csv
```

### Expected Output

* Description of the expected output:

  * Output files generated (names and formats)
  * Console/log output
  * Visualizations or reports (if any)

### Expected Runtime

* Approximate runtime on a “normal” desktop computer:

  * Example: ~30 seconds

## Instructions for Use

### Running the Software on Your Own Data

1. Prepare your input data according to the required format
2. Specify input/output paths and configuration options
3. Execute the main command

```bash
# Example
python run.py --input <your_data> --output <output_directory>
```

### Configuration Options

* Description of key parameters and flags
* Default values and recommended settings

### Notes and Best Practices

* Performance considerations
* Common pitfalls
* Troubleshooting tips


## Setup for most scripts

The preferred method to run the scripts is to use the new environment manager, `uv` (https://docs.astral.sh/uv/). To install `uv` in a local account (this does not require admin access), run the _standalone installer_ from their website: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

- On Mac, Linux or WSL, create an environment with:

```bash
uv venv
```

- Activate it with:

```bash
source .venv/bin/activate
```

- Install dependencies with:

```bash
uv pip install package-name
```

## Setup for `run_*.py` scripts

These scripts may require more steps because they use another software to run the analysis. Make sure to install the software separately and verify that it works on its own before using the `run_*.py` script.

## Running a script

Once the environment is activated and the dependencies installed, run:

```bash
python script_name.py
```
