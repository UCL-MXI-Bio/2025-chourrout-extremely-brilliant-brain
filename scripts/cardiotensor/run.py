import os
import subprocess
import pathlib

try:
  import cardiotensor
except ImportError:
  raise Exception("Please install cardiotensor")

if not pathlib.Path("./cardiotensor.conf").exists():
  raise Exception("Please download cardiotensor.conf")

subprocess.run(['cardio-tensor','cardiotensor.conf'])
