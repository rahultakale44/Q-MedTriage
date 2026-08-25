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

**Dataset Statistics:**
- Total Images: 5,856
- Training: 5,216 images (NORMAL: 1,341 | PNEUMONIA: 3,875)
- Validation: 16 images (NORMAL: 8 | PNEUMONIA: 8)
- Test: 624 images (NORMAL: 234 | PNEUMONIA: 390)

**Official Splits:** The Kermany dataset provides pre-split train/validation/test sets, which are preserved for reproducibility.

**To inspect the dataset:**
```bash
python src/data/kermany_dataset.py
```

Frontend development continues with deterministic demo data until the full ML pipeline is trained.

## Disclaimer

This project is developed for educational and hackathon purposes.
It is not intended for clinical diagnosis or medical decision-making.