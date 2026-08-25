"""
Configuration for Q-MedTriage

Centralized configuration to avoid magic numbers scattered throughout codebase.
"""

from pathlib import Path

# ============================================================================
# DATASET CONFIGURATION
# ============================================================================

# Dataset paths
DATA_ROOT = Path("data/archive (1)/chest_xray")
PROCESSED_DATA_DIR = Path("data/processed")

# Class mapping
CLASS_LABELS = {
    "NORMAL": 0,
    "PNEUMONIA": 1,
}
NUM_CLASSES = 2
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]

# ============================================================================
# SPLIT CONFIGURATION
# ============================================================================

# Random seed for reproducibility
RANDOM_SEED = 42

# Validation split ratio (from original train directory)
# Official val split has only 16 images, so we create a larger one
VAL_RATIO = 0.20  # 80% train, 20% validation from original train data

# Official test set is preserved and NEVER used during training/validation
USE_OFFICIAL_TEST = True

# ============================================================================
# IMAGE PREPROCESSING CONFIGURATION
# ============================================================================

# Target image size for ResNet50
IMAGE_SIZE = 224  # ResNet50 expects 224x224

# ImageNet normalization (required for pretrained ResNet50)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# ============================================================================
# DATA AUGMENTATION CONFIGURATION
# ============================================================================

# Training augmentation parameters
TRAIN_AUGMENTATION = {
    "resize": 256,
    "crop_size": 224,
    "horizontal_flip_prob": 0.5,
    "rotation_degrees": 10,  # Mild rotation for medical images
    "brightness": 0.1,  # Slight brightness adjustment
    "contrast": 0.1,  # Slight contrast adjustment
}

# Validation/Test: deterministic preprocessing only (no augmentation)
VAL_TEST_PREPROCESSING = {
    "resize": 256,
    "center_crop": 224,
}

# ============================================================================
# DATALOADER CONFIGURATION
# ============================================================================

BATCH_SIZE = 32
NUM_WORKERS = 4  # Adjust based on system capabilities
PIN_MEMORY = True  # Set to True when using CUDA

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# ResNet50 feature extraction
RESNET_FEATURE_DIM = 2048  # ResNet50 penultimate layer dimension

# PCA reduction
PCA_COMPONENTS = 4  # Target dimension for quantum processing

# Device configuration
DEVICE = "auto"  # 'auto', 'cuda', or 'cpu'

# ============================================================================
# TRAINING CONFIGURATION
# ============================================================================

# Class imbalance handling
# Training set: ~26% NORMAL, ~74% PNEUMONIA
CLASS_WEIGHTS = {
    0: 1.0 / 0.26,  # NORMAL weight (inverse of frequency)
    1: 1.0 / 0.74,  # PNEUMONIA weight (inverse of frequency)
}

# Normalization for balanced weighting
total_weight = sum(CLASS_WEIGHTS.values())
CLASS_WEIGHTS = {k: v / total_weight * 2 for k, v in CLASS_WEIGHTS.items()}

# ============================================================================
# MODEL ARTIFACT PATHS
# ============================================================================

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

# Model save paths
RESNET_CHECKPOINT_PATH = MODEL_DIR / "resnet50_pneumonia.pth"
PCA_MODEL_PATH = MODEL_DIR / "pca_reducer.pkl"
CLASSICAL_SVM_PATH = MODEL_DIR / "classical_svm.pkl"
QUANTUM_QSVM_PATH = MODEL_DIR / "quantum_qsvm.pkl"

# Feature cache paths (for faster experimentation)
FEATURE_CACHE_DIR = Path("data/features")
FEATURE_CACHE_DIR.mkdir(exist_ok=True)

TRAIN_FEATURES_PATH = FEATURE_CACHE_DIR / "train_features.npy"
VAL_FEATURES_PATH = FEATURE_CACHE_DIR / "val_features.npy"
TEST_FEATURES_PATH = FEATURE_CACHE_DIR / "test_features.npy"

# ============================================================================
# LOGGING AND REPRODUCIBILITY
# ============================================================================

# Experiment tracking
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

# Log file
LOG_FILE = RESULTS_DIR / "training_log.txt"

# ============================================================================
# MEDICAL SAFETY
# ============================================================================

# Disclaimer for outputs
MEDICAL_DISCLAIMER = (
    "This system is for educational and research purposes only. "
    "NOT intended for clinical diagnosis or medical decision-making."
)


def print_config():
    """Print current configuration"""
    print("=" * 70)
    print("Q-MedTriage Configuration")
    print("=" * 70)
    print(f"\nDataset:")
    print(f"  Root: {DATA_ROOT}")
    print(f"  Classes: {CLASS_NAMES}")
    print(f"  Random seed: {RANDOM_SEED}")
    print(f"  Validation ratio: {VAL_RATIO:.1%}")
    print(f"\nImage preprocessing:")
    print(f"  Target size: {IMAGE_SIZE}x{IMAGE_SIZE}")
    print(f"  Normalization: ImageNet stats")
    print(f"\nModel architecture:")
    print(f"  ResNet50 features: {RESNET_FEATURE_DIM}D")
    print(f"  PCA reduction: {RESNET_FEATURE_DIM}D → {PCA_COMPONENTS}D")
    print(f"\nTraining:")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Num workers: {NUM_WORKERS}")
    print(f"  Class weights: {CLASS_WEIGHTS}")
    print(f"\nModel artifacts:")
    print(f"  Directory: {MODEL_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    print_config()
