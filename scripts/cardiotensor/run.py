import numpy as np
import tifffile as tiff
from pathlib import Path
import configparser
import os
import subprocess
import pathlib

# ------------------------
# Tests

try:
  import cardiotensor
except ImportError:
  raise Exception("Please install cardiotensor")

if not pathlib.Path("./cardiotensor.conf").exists():
  raise Exception("Please download cardiotensor.conf")

# Note: make sure to edit the path in the cardiotensor.conf file

# ------------------------
# Run cardiotensor

subprocess.run(['cardio-tensor','cardiotensor.conf'])

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
