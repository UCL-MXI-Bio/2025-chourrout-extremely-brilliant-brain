#! /bin/bash

docker run -it --rm -v ../data/ebb-mri_as_bids:/bids -v ../data/ebb-mri_hippunfold_unet:/output khanlab/hippunfold:latest /bids /output participant --modality T2w -p --core all --force-nnunet-model synthseg_v0.2