import zarr
import dask
import dask.array
import tifffile as tiff
import numpy as np
from pathlib import Path
import subprocess
from dask import delayed

dataset_full = dask.array.from_zarr("gs://ucl-hip-ct-ebb-hseid5pvpp8vgtzt/sub-01/ses-01/micr/sub-01_ses-01_sample-brain_XPCT.ome.zarr/0/")

data_path = Path("/your_path/input_as_tiff_stack")
command = f"mkdir -p {data_path.absolute()}"
subprocess.run(command.split(" "))

margin = 32
lower_corner = (2325-margin, 1113-margin, 10774-margin)
upper_corner = (17268+margin, 17931+margin, 10774+margin)
# lower_corner = (5000, 5000, 10774-64)
# upper_corner = (5512, 5512, 10774+64)

optimal_intensity_window = (14246, 14456)

data_slab = dataset_full[
    lower_corner[0]:upper_corner[0],
    lower_corner[1]:upper_corner[1],
    lower_corner[2]:upper_corner[2]
].rechunk((upper_corner[0]-lower_corner[0],upper_corner[1]-lower_corner[1],1))

# Prepare all computations in a list (lazy execution)
lazy_results = []
for i in range(data_slab.shape[2]):
    file_path = data_path / f"slice{(lower_corner[2]+i):05}_offset{lower_corner[0]:05}x{lower_corner[1]:05}x{lower_corner[2]:05}_idx{i:05}.tif"
    
    print(f"Preparing slice {(lower_corner[2]+i):05} ({i:05}/{(data_slab.shape[2]-1):05}) as \"{file_path}\"...")
    
    lazy_results.append(delayed(tiff.imwrite)(file_path, data_slab[:,:,i], mode="w", photometric='minisblack', imagej=True))

# Execute in parallel
dask.compute(*lazy_results)  # Parallel execution
