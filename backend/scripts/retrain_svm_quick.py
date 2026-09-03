"""
Quick script to retrain Classical SVM with proper paths
This bypasses the full feature extraction pipeline by working directly with the dataset
"""
import sys
from pathlib import Path
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import pandas as pd
from tqdm import tqdm

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Paths relative to project root
TRAIN_CSV = PROJECT_ROOT / "data/processed/train.csv"
VAL_CSV = PROJECT_ROOT / "data/processed/val.csv"
TEST_CSV = PROJECT_ROOT / "data/processed/test.csv"
MODEL_DIR = PROJECT_ROOT / "models"

print("=" * 70)
print("Quick Classical SVM Retraining")
print("=" * 70)
print(f"Project root: {PROJECT_ROOT}")
print(f"Train CSV: {TRAIN_CSV.exists()}")
print(f"Val CSV: {VAL_CSV.exists()}")
print(f"Test CSV: {TEST_CSV.exists()}")
print("=" * 70)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# Load ResNet50
print("\nLoading ResNet50...")
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model = nn.Sequential(*list(model.children())[:-1])
model = model.to(device)
model.eval()
print("✓ ResNet50 loaded")

# Preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(df, desc="Extracting"):
    """Extract ResNet50 features from images"""
    features = []
    labels = []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc=desc):
        try:
            img_path = PROJECT_ROOT / row['image_path']
            img = Image.open(img_path).convert('L')
            img_tensor = transform(img).unsqueeze(0).to(device)
            
            with torch.no_grad():
                feat = model(img_tensor).squeeze().cpu().numpy()
            
            features.append(feat)
            labels.append(row['label'])
        except Exception as e:
            print(f"Error processing {row['image_path']}: {e}")
            continue
    
    return np.array(features), np.array(labels)

# Load datasets
print("\nLoading datasets...")
train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)
test_df = pd.read_csv(TEST_CSV)

print(f"Train: {len(train_df)} samples")
print(f"Val: {len(val_df)} samples")
print(f"Test: {len(test_df)} samples")

# Sample for faster training (or use full dataset)
USE_FULL_DATASET = False
if not USE_FULL_DATASET:
    print("\n⚠️  Using SAMPLED dataset for faster retraining")
    train_df = train_df.sample(n=min(1000, len(train_df)), random_state=42)
    val_df = val_df.sample(n=min(300, len(val_df)), random_state=42)
    test_df = test_df.sample(n=min(200, len(test_df)), random_state=42)
    print(f"Sampled - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

# Extract features
print("\nExtracting features...")
X_train, y_train = extract_features(train_df, "Train")
X_val, y_val = extract_features(val_df, "Val")
X_test, y_test = extract_features(test_df, "Test")

print(f"\nFeature shapes:")
print(f"Train: {X_train.shape}")
print(f"Val: {X_val.shape}")
print(f"Test: {X_test.shape}")

# Fit PCA
print("\nFitting PCA (2048D → 4D)...")
pca = PCA(n_components=4, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_val_pca = pca.transform(X_val)
X_test_pca = pca.transform(X_test)

explained_var = pca.explained_variance_ratio_.sum()
print(f"✓ PCA fitted - Explained variance: {explained_var:.2%}")

# Train SVM with class weights to handle imbalance
print("\nTraining SVM with class weights...")
print("Dataset is imbalanced - using class_weight='balanced'")
svm = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42, class_weight='balanced')
svm.fit(X_train_pca, y_train)
print("✓ SVM trained with balanced class weights")

# Evaluate
print("\n" + "=" * 70)
print("VALIDATION SET EVALUATION")
print("=" * 70)
y_val_pred = svm.predict(X_val_pca)
val_acc = accuracy_score(y_val, y_val_pred)
print(f"Accuracy: {val_acc:.2%}")
print("\nClassification Report:")
print(classification_report(y_val, y_val_pred, target_names=["NORMAL", "PNEUMONIA"]))
print("\nConfusion Matrix:")
print(confusion_matrix(y_val, y_val_pred))

print("\n" + "=" * 70)
print("TEST SET EVALUATION")
print("=" * 70)
y_test_pred = svm.predict(X_test_pca)
test_acc = accuracy_score(y_test, y_test_pred)
print(f"Accuracy: {test_acc:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred, target_names=["NORMAL", "PNEUMONIA"]))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))

# Save models
if val_acc > 0.80:  # Only save if reasonable accuracy
    print("\n" + "=" * 70)
    print("SAVING MODELS")
    print("=" * 70)
    
    pca_path = MODEL_DIR / "pca_reducer.pkl"
    svm_path = MODEL_DIR / "classical_svm.pkl"
    
    joblib.dump(pca, pca_path)
    joblib.dump(svm, svm_path)
    
    print(f"✓ PCA saved: {pca_path}")
    print(f"✓ SVM saved: {svm_path}")
    print("\nModels ready for inference!")
else:
    print(f"\n⚠️  Accuracy too low ({val_acc:.2%}) - models NOT saved")
    print("Consider using full dataset or adjusting hyperparameters")

print("\n" + "=" * 70)
print("RETRAINING COMPLETE")
print("=" * 70)
