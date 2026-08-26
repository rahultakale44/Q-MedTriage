"""
Train Quantum Support Vector Machine for Q-MedTriage.

COMMIT 10/30

Uses the frozen 4D PCA features produced by the PCA pipeline.

Input:
    data/features/train_features_pca4d.npy
    data/features/train_labels_pca4d.npy
    data/features/test_features_pca4d.npy
    data/features/test_labels_pca4d.npy

Output:
    models/quantum_svm.pkl
    results/quantum_svm_training_results.json
"""

from pathlib import Path
import json
import sys

import numpy as np
from sklearn.model_selection import train_test_split

# Allow imports from the project root when this file is run directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.quantum_svm import QuantumSVM


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

FEATURES_DIR = PROJECT_ROOT / "data" / "features"
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

TRAIN_FEATURES = FEATURES_DIR / "train_features_pca4d.npy"
TRAIN_LABELS = FEATURES_DIR / "train_labels_pca4d.npy"

TEST_FEATURES = FEATURES_DIR / "test_features_pca4d.npy"
TEST_LABELS = FEATURES_DIR / "test_labels_pca4d.npy"

MODEL_PATH = MODELS_DIR / "quantum_svm.pkl"
RESULTS_PATH = RESULTS_DIR / "quantum_svm_training_results.json"


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

FEATURE_DIMENSION = 4
REPS = 2
ENTANGLEMENT = "linear"
C = 1.0
PROBABILITY = True
RANDOM_STATE = 42

# QSVM training subset size (to make quantum kernel computation practical)
# Full training set: 4,172 samples → 17.4M kernel entries
# Subset of 500 samples → 250K kernel entries (much more practical)
QSVM_TRAIN_SAMPLES = 500  # Configurable: adjust if needed


def create_stratified_subset(
    X_train: np.ndarray,
    y_train: np.ndarray,
    subset_size: int,
    random_state: int = 42,
):
    """
    Create a stratified subset of training data for QSVM training.
    
    This reduces the quantum kernel computation from approximately:
    - Full: 4,172 × 4,172 ≈ 17.4M kernel entries
    - Subset: 1,000 × 1,000 ≈ 1M kernel entries
    
    Args:
        X_train: Full training features (N, 4)
        y_train: Full training labels (N,)
        subset_size: Target subset size
        random_state: Random state for reproducibility
        
    Returns:
        X_subset, y_subset: Stratified subset maintaining class distribution
    """
    
    if subset_size >= len(X_train):
        print(f"Requested subset size ({subset_size}) >= full training size ({len(X_train)})")
        print("Using all training samples.")
        return X_train, y_train
    
    # Calculate stratified subset
    # train_test_split with test_size gives us the subset we want
    X_subset, _, y_subset, _ = train_test_split(
        X_train,
        y_train,
        train_size=subset_size,
        stratify=y_train,
        random_state=random_state,
    )
    
    return X_subset, y_subset


def load_data():
    """Load frozen PCA-reduced training and test features."""

    required_files = [
        TRAIN_FEATURES,
        TRAIN_LABELS,
        TEST_FEATURES,
        TEST_LABELS,
    ]

    for path in required_files:
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found:\n{path}"
            )

    X_train = np.load(TRAIN_FEATURES)
    y_train = np.load(TRAIN_LABELS)

    X_test = np.load(TEST_FEATURES)
    y_test = np.load(TEST_LABELS)

    return X_train, y_train, X_test, y_test


def convert_numpy_types(obj):
    """
    Convert NumPy values into JSON-serializable Python values.
    """

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, dict):
        return {
            key: convert_numpy_types(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            convert_numpy_types(value)
            for value in obj
        ]

    return obj


def main():
    """Train, evaluate, save, and record Quantum SVM results."""

    print()
    print("=" * 70)
    print("Q-MEDTRIAGE - QUANTUM SVM TRAINING")
    print("=" * 70)

    print()
    print("Project root:")
    print(PROJECT_ROOT)

    # -------------------------------------------------------------
    # Load data
    # -------------------------------------------------------------

    print()
    print("Loading frozen PCA features...")

    X_train_full, y_train_full, X_test, y_test = load_data()

    print()
    print("Full training data:")
    print(f"  X_train shape: {X_train_full.shape}")
    print(f"  y_train shape: {y_train_full.shape}")

    print()
    print("Test data:")
    print(f"  X_test shape:  {X_test.shape}")
    print(f"  y_test shape:  {y_test.shape}")

    # -------------------------------------------------------------
    # Create stratified subset for QSVM training
    # -------------------------------------------------------------

    print()
    print("-" * 70)
    print("Preparing Quantum SVM training subset")
    print("-" * 70)
    print()
    print(f"Full training samples: {len(X_train_full)}")
    print(f"QSVM training samples: {QSVM_TRAIN_SAMPLES}")
    print(f"Random state: {RANDOM_STATE}")
    print()
    
    # Calculate expected class distribution
    unique_full, counts_full = np.unique(y_train_full, return_counts=True)
    print("Full training class distribution:")
    for label, count in zip(unique_full, counts_full):
        class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
        percentage = (count / len(y_train_full)) * 100
        print(f"  {class_name} ({int(label)}): {int(count)} ({percentage:.1f}%)")
    
    # Create stratified subset
    X_train, y_train = create_stratified_subset(
        X_train_full,
        y_train_full,
        subset_size=QSVM_TRAIN_SAMPLES,
        random_state=RANDOM_STATE,
    )
    
    print()
    print("Selected QSVM training subset class distribution:")
    unique_subset, counts_subset = np.unique(y_train, return_counts=True)
    for label, count in zip(unique_subset, counts_subset):
        class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
        percentage = (count / len(y_train)) * 100
        print(f"  {class_name} ({int(label)}): {int(count)} ({percentage:.1f}%)")
    
    print()
    print("[OK] Stratified subset created successfully")
    print(f"[OK] Class distribution preserved")

    # -------------------------------------------------------------
    # Validate dimensions
    # -------------------------------------------------------------

    if X_train.ndim != 2:
        raise ValueError(
            f"Expected X_train to be 2D, got {X_train.shape}"
        )

    if X_test.ndim != 2:
        raise ValueError(
            f"Expected X_test to be 2D, got {X_test.shape}"
        )

    if X_train.shape[1] != FEATURE_DIMENSION:
        raise ValueError(
            f"Expected {FEATURE_DIMENSION} PCA features, "
            f"got {X_train.shape[1]}"
        )

    if X_test.shape[1] != FEATURE_DIMENSION:
        raise ValueError(
            f"Expected {FEATURE_DIMENSION} PCA features, "
            f"got {X_test.shape[1]}"
        )

    if len(X_train) != len(y_train):
        raise ValueError(
            "Training features and labels have different lengths."
        )

    if len(X_test) != len(y_test):
        raise ValueError(
            "Test features and labels have different lengths."
        )

    # -------------------------------------------------------------
    # Show test class distribution
    # -------------------------------------------------------------

    print()
    print("Test class distribution (COMPLETE test set, unchanged):")
    unique_test, counts_test = np.unique(
        y_test,
        return_counts=True,
    )

    for label, count in zip(unique_test, counts_test):
        class_name = (
            "PNEUMONIA"
            if int(label) == 1
            else "NORMAL"
        )

        print(
            f"  {class_name} ({int(label)}): "
            f"{int(count)}"
        )

    # -------------------------------------------------------------
    # Create Quantum SVM
    # -------------------------------------------------------------

    print()
    print("-" * 70)
    print("Creating Quantum SVM")
    print("-" * 70)
    print()
    print(f"Qubits: {FEATURE_DIMENSION}")
    print(f"Feature-map repetitions: {REPS}")
    print(f"Entanglement: {ENTANGLEMENT}")
    print(f"C: {C}")

    quantum_svm = QuantumSVM(
        feature_dimension=FEATURE_DIMENSION,
        reps=REPS,
        entanglement=ENTANGLEMENT,
        C=C,
        probability=PROBABILITY,
        random_state=RANDOM_STATE,
    )

    # -------------------------------------------------------------
    # Train
    # -------------------------------------------------------------

    print()
    print("-" * 70)
    print("Training Quantum SVM")
    print("-" * 70)
    print()
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimension: {X_train.shape[1]}")
    print()
    print("WARNING: This may take several minutes depending on hardware...")
    print()

    quantum_svm.train(
        X_train=X_train,
        y_train=y_train,
    )

    # -------------------------------------------------------------
    # Evaluate
    # -------------------------------------------------------------

    print()
    print("-" * 70)
    print("Evaluating Quantum SVM on COMPLETE TEST set")
    print("-" * 70)
    print()
    print(f"Test samples: {len(X_test)}")
    print()

    metrics = quantum_svm.evaluate(
        X_test,
        y_test,
        verbose=True,
    )

    # -------------------------------------------------------------
    # Save model
    # -------------------------------------------------------------

    print()
    print("-" * 70)
    print("Saving Quantum SVM")
    print("-" * 70)

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    quantum_svm.save(
        str(MODEL_PATH)
    )

    # -------------------------------------------------------------
    # Save metrics
    # -------------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Calculate training subset class distribution for metadata
    train_class_dist = {}
    unique_train, counts_train = np.unique(y_train, return_counts=True)
    for label, count in zip(unique_train, counts_train):
        class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
        train_class_dist[class_name] = int(count)
    
    # Calculate test class distribution for metadata
    test_class_dist = {}
    unique_test, counts_test = np.unique(y_test, return_counts=True)
    for label, count in zip(unique_test, counts_test):
        class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
        test_class_dist[class_name] = int(count)

    results = {
        "model": "Quantum SVM",
        "algorithm": "QSVC",
        "feature_dimension": FEATURE_DIMENSION,
        "qubits": FEATURE_DIMENSION,
        "feature_map": "ZZFeatureMap",
        "reps": REPS,
        "entanglement": ENTANGLEMENT,
        "C": C,
        "probability": PROBABILITY,
        "random_state": RANDOM_STATE,
        "training_samples_full": len(X_train_full),
        "training_samples_used": len(X_train),
        "test_samples": len(X_test),
        "training_class_distribution": train_class_dist,
        "test_class_distribution": test_class_dist,
        "metrics": metrics,
    }

    results = convert_numpy_types(results)

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=4,
        )

    print()
    print(f"Results saved to: {RESULTS_PATH}")

    # -------------------------------------------------------------
    # Final summary
    # -------------------------------------------------------------

    print()
    print("=" * 70)
    print("QUANTUM SVM TRAINING COMPLETE")
    print("=" * 70)

    print()
    print(f"Model:       {MODEL_PATH}")
    print(f"Results:     {RESULTS_PATH}")
    print()
    print(
        f"Accuracy:    {metrics['accuracy']:.4f}"
    )
    print(
        f"Precision:   {metrics['precision']:.4f}"
    )
    print(
        f"Recall:      {metrics['recall']:.4f}"
    )
    print(
        f"F1 Score:    {metrics['f1_score']:.4f}"
    )

    if "roc_auc" in metrics:
        print(
            f"ROC-AUC:     {metrics['roc_auc']:.4f}"
        )

    print()
    print("Quantum SVM model is ready for inference.")
    print("=" * 70)


if __name__ == "__main__":
    main()