#! /bin/bash

FILE_FINAL="../data/mri_as_bids/sub-01/ses-02/anat/sub-01_ses-02_T2w.nii.gz"
if [ -f "$FILE_FINAL" ]; then
  echo "Files are ready for scripts/hippunfold-docker/run.sh"
  exit 0
fi

FILE_TMP="../data/sub-01_ses-02_T2w.nii.gz"
if [ ! -f "$FILE_TMP" ]; then
  echo "Error: $FILE_TMP does not exist."
  exit 1
fi

mkdir -p ../data/mri_as_bids/sub-01/ses-02/anat

touch ../data/mri_as_bids/dataset_description.json
touch ../data/mri_as_bids/participants.json
touch ../data/mri_as_bids/participants.tsv
touch ../data/mri_as_bids/sub-01/ses-02/anat/sub-01_ses-02_T2w.json
mv $FILE_TMP $FILE_FINAL
touch ../data/mri_as_bids/sub-01/sub-01_sessions.json
touch ../data/mri_as_bids/sub-01/sub-01_sessions.tsv

echo "Folder structure:"
tree ../data/mri_as_bids

echo "Files are ready for scripts/hippunfold-docker/run.sh"
exit 0