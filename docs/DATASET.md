# Dataset

## Primary Dataset

**Kermany Chest X-Ray Images (Pneumonia)**

**Reference:** Kermany, Daniel; Zhang, Kang; Goldbaum, Michael (2018), "Labeled Optical Coherence Tomography (OCT) and Chest X-Ray Images for Classification", Mendeley Data, v2

**Source:** Available on Kaggle: [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

**Classification Task:** Binary classification — NORMAL vs PNEUMONIA

The original image dataset is not included in this repository because of
its large size (~1.2 GB) and dataset licensing requirements.

**Local Dataset Location:** `data/archive (1)/chest_xray/`

## Dataset Statistics

**Total Images:** 5,856 chest X-ray images

**Classes:**
- NORMAL (label: 0)
- PNEUMONIA (label: 1)

**Official Splits:**
- **Training:** 5,216 images
  - NORMAL: 1,341 (25.7%)
  - PNEUMONIA: 3,875 (74.3%)
- **Validation:** 16 images
  - NORMAL: 8 (50%)
  - PNEUMONIA: 8 (50%)
- **Test:** 624 images
  - NORMAL: 234 (37.5%)
  - PNEUMONIA: 390 (62.5%)

**Image Format:** JPEG (grayscale chest X-rays)

## Dataset Structure

```
data/archive (1)/chest_xray/
├── train/
│   ├── NORMAL/
│   │   └── *.jpeg
│   └── PNEUMONIA/
│       └── *.jpeg
├── val/
│   ├── NORMAL/
│   │   └── *.jpeg
│   └── PNEUMONIA/
│       └── *.jpeg
└── test/
    ├── NORMAL/
    │   └── *.jpeg
    └── PNEUMONIA/
        └── *.jpeg
```

## Class Imbalance Considerations

The dataset exhibits class imbalance, particularly in the training set (~74% PNEUMONIA).

**Mitigation strategies:**
- Class-weighted loss functions during training
- Balanced evaluation metrics (precision, recall, F1-score, AUC-ROC)
- Stratified sampling for validation split creation
- Careful interpretation of accuracy metrics

## Data Leakage Prevention

The Kermany dataset provides official train/validation/test splits which are preserved to maintain reproducibility and prevent data leakage.

**Safeguards:**
- Official splits are maintained without reshuffling
- Patient-level separation is handled by the dataset creators
- No cross-contamination between splits
- Fixed random seeds for any additional split modifications

## Reproducibility

**Dataset inspection:**
```bash
python src/data/kermany_dataset.py
```

**Dataset handler:** `src/data/kermany_dataset.py`
- Automatic dataset discovery
- Split validation
- Class distribution reporting
- CSV export for ML pipelines
- Image integrity validation

**Generated artifacts:**
- `data/dataset_report.json` — Complete dataset statistics
- `data/processed/train.csv` — Training split manifest (generated on demand)
- `data/processed/val.csv` — Validation split manifest (generated on demand)
- `data/processed/test.csv` — Test split manifest (generated on demand)

All dataset processing scripts are version-controlled to ensure reproducibility without committing the actual images.

## Medical Disclaimer

This dataset is used for educational and research purposes only. The Q-MedTriage system is **NOT** intended for clinical diagnosis or medical decision-making.