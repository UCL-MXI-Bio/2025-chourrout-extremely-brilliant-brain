import numpy as np
import tifffile as tiff
from pathlib import Path
import configparser
import inquirer
import subprocess
import pathlib

# ------------------------
# Tests

try:
  import cardiotensor
except ImportError:
  raise Exception("Please install cardiotensor")

run_demo = inquirer.confirm(
  "Run on the demo data instead of the full-resolution dataset?",
  default=True,
)
CONFIG_FILE = "cardiotensor_(demo_data).conf" if run_demo else "cardiotensor_(full_resolution).conf"

if not pathlib.Path(CONFIG_FILE).exists():
  raise Exception("Please download {}")

subprocess.run(['cardio-tensor',CONFIG_FILE])

# ------------------------
# Post-processing

with open('cardiotensor.conf', 'r') as config_file:
    config = configparser.ConfigParser()
    config.read(config_file)

data_path = Path(config.get("OUTPUT", "OUTPUT_PATH").strip())

eigvec_slice = np.load(data_path)

print(eigvec_slice.shape)

eigvec_slice[eigvec_slice<0] *= -1.0

rgb_slice = eigvec_slice * 255
rgb_slice[:, np.any(np.isnan(rgb_slice),axis=0)] = 0

rgb_slice = rgb_slice[[0,2,1],...].astype(np.uint8)

rgb_slice_transposed = np.fliplr(np.flipud(rgb_slice.transpose((1,2,0))))

# ------------------------
# Output writing

tiff.imwrite(data_path.with_suffix(".tif"),rgb_slice_transposed,photometric="rgb",imagej=True)
