# Extremely Brilliant Brain 🩻🧠✨
Supplementary material for the release of the “Extremely Brilliant Brain”

## Dataset
The data can be downloaded from the BioImage Archive (BIA) following the Brain Imaging Data Structure (BIDS) specification: https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1939

The data is also replicated on a Google Cloud Storage bucket for streaming to Neuroglancer (see below). Some files had to be converted to a format that is compatible with Neuroglancer, using the scripts that are provided.

## Interactive figures
Interactive figures are available in the [subfolder](./interactive_figures/).

## Scripts
The Python scripts are available in the [subfolder](./scripts/).

Besides, this work has required the development of a few Python tools:

| Repository                                                                                                 | Usecase                                                                                                                              |
|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| [`stack-to-chunk`](https://github.com/HiPCTProject/stack-to-chunk)                                         | Conversion of a series of 2D images to a 3D volume stored as an OME-Zarr                                                             |
| [`ngregister`](https://github.com/HiPCTProject/ngregister)                                                 | Register with an affine transform using a set of hotkeys within Neuroglancer (optimal for large multiscale dataset)                  |
| [`ngretrieve`](https://github.com/chourroutm/ngretrieve)                                                   | Download a crop of the dataset that can be picked with a Neuroglancer annotation layer                                               |
| [`ngpointstobox`](https://github.com/chourroutm/ngpointstobox)                                             | Change a set of annotations into one annotation that is their bounding box in a Neuroglancer state                                   |
| [`ngvolbox`](https://github.com/chourroutm/ngvolbox)                                                       | Replace a volume layer with an annotation layer that is its bounding box                                                             |
| [`segment_properties_for_neuroglancer`](https://github.com/chourroutm/segment_properties_for_neuroglancer) | Generate the segmentation properties for the Neuroglancer precomputed format to add metrics and a colormap to the segmentation layer |

## License

<p xmlns:cc="http://creativecommons.org/ns#" >This work is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a>.</p> 

A copy of the license is available in the repository.

--------

<details>
<summary>Notes</summary>

> - BioImage Archive: https://www.ebi.ac.uk/bioimage-archive/
> - Brain Imaging Data Structure (BIDS): https://bids.neuroimaging.io/
> - Google Cloud Storage: https://cloud.google.com/storage
> - Neuroglancer: https://neuroglancer-docs.web.app/ | [https://github.com/google/neuroglancer](https://github.com/google/neuroglancer?tab=readme-ov-file#neuroglancer-web-based-volumetric-data-visualization)

</details>
