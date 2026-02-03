# Scripts

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
