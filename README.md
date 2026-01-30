# Extremely Brilliant Brain 🩻🧠✨

Supplementary material for the release of the “Extremely Brilliant Brain” (EBB), a 7.72 μm/voxel 3D volume of a whole adult human brain acquired using Hierarchical Phase-Contrast Tomography (HiP-CT)<sup>[see note]</sup>.

## Preprint
The associated manuscript is available as a preprint on bioRxiv: https://www.biorxiv.org/content/10.64898/2026.01.27.702076

## Dataset
The data (EBB & MRI) can be downloaded from the BioImage Archive (BIA)<sup>[see note]</sup> following the Brain Imaging Data Structure (BIDS) specification<sup>[see note]</sup>: https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1939

The EBB data itself can be downloaded from the Human Organ Atlas (HOA) data portal<sup>[see note]</sup> as series of JPEG2000 files at different voxel sizes: https://human-organ-atlas.esrf.fr/datasets/2270234369



The data is also replicated on a Google Cloud Storage<sup>[see note]</sup> bucket for streaming to Neuroglancer<sup>[see note]</sup>. Some files had to be converted to a format that is compatible with Neuroglancer, using the scripts that are provided.

## Interactive figures
Interactive figures are available in the [subfolder](./interactive_figures/).

## Scripts
The Python scripts are available in the [subfolder](./scripts/).

Besides, this work has required the use of a few Python tools:

| Repository                                                                                                 | Usecase                                                                                                                              |
|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| [`stack-to-chunk`](https://github.com/HiPCTProject/stack-to-chunk)                                         | Conversion of a series of 2D images to a 3D volume stored as an OME-Zarr                                                             |
| [`ngregister`](https://github.com/HiPCTProject/ngregister)                                                 | Register with an affine transform using a set of hotkeys within Neuroglancer (optimal for large multiscale dataset)                  |
| [`cardiotensor`](https://github.com/JosephBrunet/cardiotensor)                                             | Compute the structure tensor field in a 3D volume                                                                                    |
| [`ngretrieve`](https://github.com/chourroutm/ngretrieve)                                                   | Download a crop of the dataset that can be picked with a Neuroglancer annotation layer                                               |
| [`ngpointstobox`](https://github.com/chourroutm/ngpointstobox)                                             | Change a set of annotations into one annotation that is their bounding box in a Neuroglancer state                                   |
| [`ngvolbox`](https://github.com/chourroutm/ngvolbox)                                                       | Replace a volume layer with an annotation layer that is its bounding box                                                             |
| [`segment_properties_for_neuroglancer`](https://github.com/chourroutm/segment_properties_for_neuroglancer) | Generate the segmentation properties for the Neuroglancer precomputed format to add metrics and a colormap to the segmentation layer |
| [`freesurfer`](https://github.com/freesurfer/freesurfer)                                                   | Suite of processing tools for 3D imaging data, initially focused on MRI and the NIfTI file format                                    |
| [`FastSurfer`](https://github.com/Deep-MI/FastSurfer)                                                      | Deep learning-enabled segmentation toolbox                                                                                           |
| [`hippunfold`](https://github.com/khanlab/hippunfold)                                                      | Hippocampus parcellation toolbox                                                                                                     |

## License

<p xmlns:cc="http://creativecommons.org/ns#" >This work is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a>.</p> 

A copy of the license is available in the repository.

--------

<details>
<summary>Notes</summary>

> - Hierarchical Phase-Contrast Tomography (HiP-CT): https://mecheng.ucl.ac.uk/hip-ct/ | https://www.nature.com/articles/s41592-021-01317-x
> - BioImage Archive: https://www.ebi.ac.uk/bioimage-archive/
> - Brain Imaging Data Structure (BIDS): https://bids.neuroimaging.io/
> - Human Organ Atlas (HOA): https://human-organ-atlas.esrf.fr/
> - Google Cloud Storage: https://cloud.google.com/storage
> - Neuroglancer: https://neuroglancer-docs.web.app/ | [https://github.com/google/neuroglancer](https://github.com/google/neuroglancer?tab=readme-ov-file#neuroglancer-web-based-volumetric-data-visualization)

</details>
