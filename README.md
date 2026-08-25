# Q-MedTriage

## Quantum-Enhanced Medical Image Triage

Q-MedTriage is a hybrid AI + Quantum Machine Learning system for
medical chest X-ray triage.

The system combines:

- Deep learning for chest X-ray classification
- Transfer learning using a pretrained vision model
- Quantum machine learning for secondary classification
- PCA-based dimensionality reduction
- Transformer/LLM-based medical explanation
- Vector database for retrieval-augmented medical information
- Real-time Streamlit interface
- Classical vs Quantum performance comparison

## Project Status

🚧 Under active development

**Current Progress:** COMMIT 08/30
- ✅ Dataset migration (Kermany Chest X-Ray)
- ✅ Reproducible train/validation/test splits
- ✅ Preprocessing pipeline with augmentation
- ✅ ResNet50 feature extraction infrastructure
- ✅ PCA dimensionality reduction (2048D → 4D)
- 🔄 Feature extraction + PCA (ready, not yet run on full dataset)
- ⏳ Classical SVM training
- ⏳ Quantum QSVM training
- ⏳ Model comparison & evaluation

## Core Pipeline

Chest X-ray
→ AI Vision Model
→ Disease Prediction
→ Feature Extraction
→ PCA
→ Quantum Classifier
→ Classical vs Quantum Comparison
→ Medical Explanation
→ Knowledge Retrieval
→ Live Dashboard

## Dataset

**Current Dataset: Kermany Chest X-Ray Dataset**

**Reference:** Kermany, Daniel; Zhang, Kang; Goldbaum, Michael (2018), "Labeled Optical Coherence Tomography (OCT) and Chest X-Ray Images for Classification", Mendeley Data, v2

**Classification Task:** NORMAL vs PNEUMONIA
- NORMAL (negative class)
- PNEUMONIA (positive class)

**Dataset Source:** Available on Kaggle: [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

The dataset is not stored in this repository due to size and licensing restrictions.

**Dataset Location:** `data/archive (1)/chest_xray/`

**Dataset Statistics (Total: 5,856 images):**

**Reproducible Splits:**
- **Training:** 4,172 images (NORMAL: 1,072 [25.7%] | PNEUMONIA: 3,100 [74.3%])
- **Validation:** 1,044 images (NORMAL: 269 [25.8%] | PNEUMONIA: 775 [74.2%])
- **Test:** 624 images (NORMAL: 234 [37.5%] | PNEUMONIA: 390 [62.5%])

**Split Strategy:**
- Official Kermany test set (624 images) preserved exactly as provided
- Training/validation split created from original train data (80%/20% stratified)
- Fixed random seed (42) for reproducibility
- Image-level split (patient metadata not available)
- Zero data leakage verified

**Class Imbalance Handling:**
- Training data: ~74% PNEUMONIA, ~26% NORMAL
- Weighted random sampling during training
- Class-weighted loss functions
- Stratified validation split

**Preprocessing Pipeline:**
- Training: Resize → RandomCrop → HorizontalFlip → MildRotation → ColorJitter → Normalize (ImageNet)
- Validation/Test: Resize → CenterCrop → Normalize (deterministic)
- Target size: 224×224 (ResNet50 compatible)

**To create/inspect splits:**
```bash
# Create reproducible splits
python src/data/create_splits.py

# Validate splits (no leakage)
python src/data/validate_splits.py

# Inspect dataset
python src/data/kermany_dataset.py
```

**Feature Extraction (ResNet50 → 2048D) + PCA Reduction (2048D → 4D):**
```bash
# Test feature extraction on small sample (10 images)
python src/models/test_extraction_sample.py

# Extract features for full dataset
python src/models/extract_features.py

# Test PCA on small sample
python src/models/test_pca_sample.py

# Apply PCA reduction to full dataset
python src/models/apply_pca.py
```

Frontend development continues with deterministic demo data until the full ML pipeline is trained.

## Disclaimer

This project is developed for educational and hackathon purposes.
It is not intended for clinical diagnosis or medical decision-making.