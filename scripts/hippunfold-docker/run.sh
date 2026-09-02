#! /bin/bash

docker run -it --rm -v ../data/mri_as_bids:/bids -v ../data/mri_hippunfold_unet:/output khanlab/hippunfold:latest /bids /output participant --modality T2w -p --core all --force-nnunet-model synthseg_v0.2