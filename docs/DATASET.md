# Dataset

## Primary Dataset

CheXpert: Chest X-rays.

The original image dataset is not included in this repository because of
its very large size and dataset access/licensing requirements.

## Local Metadata Files

The following metadata/label files are used during development:

- `train_cheXbert.csv`
- `train_visualCheXbert.csv`

These files are stored locally and excluded from Git tracking.

## Planned Target

The project will initially focus on chest X-ray triage with pneumonia-related
classification.

Before model training, we will inspect the available labels, class balance,
patient distribution, and image-path mapping.

## Data Leakage Prevention

Patient-level separation will be considered when constructing training,
validation, and test splits.

## Reproducibility

Dataset preparation scripts will be stored in the repository so that the
processing pipeline can be reproduced without committing the original
dataset.