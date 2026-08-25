"""
Classical SVM Training Pipeline for Q-MedTriage

Trains a classical SVM classifier on 4D PCA-reduced features.
This establishes the classical baseline for comparison with quantum classifiers.

CRITICAL DATA FLOW:
1. Load 4D PCA-reduced features (training, validation, test)
2. Fit SVM on training features ONLY
3. Evaluate on validation set (for hyperparameter tuning/model selection)
4. Evaluate on official test set (final evaluation only)
5. Save trained model for inference

IMPORTANT:
- PCA is already fitted on training data (from COMMIT 08)
- This script loads pre-computed 4D features
- Official test set used ONLY for final evaluation (no tuning)
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

from src.config import (
    FEATURE_CACHE_DIR,
    CLASSICAL_SVM_PATH,
    CLASS_NAMES,
    CLASS_LABELS,
    RANDOM_SEED,
    RESULTS_DIR,
)
from src.models.classical_svm import ClassicalSVM


def load_pca_features(split: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load PCA-reduced 4D features
    
    Args:
        split: 'train', 'val', or 'test'
        
    Returns:
        Tuple of (features, labels)
    """
    features_path = FEATURE_CACHE_DIR / f"{split}_features_pca4d.npy"
    labels_path = FEATURE_CACHE_DIR / f"{split}_labels_pca4d.npy"
    
    if not features_path.exists():
        raise FileNotFoundError(
            f"PCA-reduced features not found: {features_path}\n"
            f"Run 'python src/models/apply_pca.py' first to generate 4D features."
        )
    
    features = np.load(features_path)
    labels = np.load(labels_path)
    
    print(f"✓ Loaded {split} 4D features: {features.shape}")
    print(f"  Labels: {labels.shape}")
    print(f"  Class distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")
    
    return features, labels


def verify_class_mapping():
    """Verify class labels are correctly mapped"""
    print("=" * 70)
    print("VERIFYING CLASS MAPPING")
    print("=" * 70)
    print()
    print("Expected class mapping:")
    for class_name, label in CLASS_LABELS.items():
        print(f"  {label} → {class_name}")
    print()
    print("Class names for predictions:")
    for i, name in enumerate(CLASS_NAMES):
        print(f"  {i} → {name}")
    print()


def train_classical_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    kernel: str = "rbf",
    C: float = 1.0,
    gamma: str = "scale",
) -> ClassicalSVM:
    """
    Train Classical SVM on 4D features
    
    Args:
        X_train: Training features (N, 4)
        y_train: Training labels (N,)
        kernel: SVM kernel ('linear', 'rbf', 'poly')
        C: Regularization parameter
        gamma: Kernel coefficient for 'rbf' and 'poly'
        
    Returns:
        Trained ClassicalSVM instance
    """
    print("=" * 70)
    print("TRAINING CLASSICAL SVM")
    print("=" * 70)
    print()
    print(f"Configuration:")
    print(f"  Kernel: {kernel}")
    print(f"  C: {C}")
    print(f"  Gamma: {gamma}")
    print(f"  Random seed: {RANDOM_SEED}")
    print()
    
    # Initialize classifier
    svm = ClassicalSVM(kernel=kernel, C=C, gamma=gamma)
    
    # Train
    print()
    svm.train(X_train, y_train)
    
    return svm


def evaluate_and_report(
    svm: ClassicalSVM,
    X_val: np.ndarray,
    y_val: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    evaluate_test: bool = False,
) -> Dict:
    """
    Evaluate SVM on validation and optionally test set
    
    Args:
        svm: Trained ClassicalSVM instance
        X_val: Validation features
        y_val: Validation labels
        X_test: Test features
        y_test: Test labels
        evaluate_test: Whether to evaluate on official test set
        
    Returns:
        Dictionary with evaluation results
    """
    results = {}
    
    # Always evaluate on validation set
    print("=" * 70)
    print("VALIDATION SET EVALUATION")
    print("=" * 70)
    print()
    
    val_metrics = svm.evaluate(X_val, y_val, verbose=True)
    results["validation"] = val_metrics
    
    # Optionally evaluate on official test set
    if evaluate_test:
        print()
        print("=" * 70)
        print("OFFICIAL TEST SET EVALUATION")
        print("=" * 70)
        print()
        print("⚠️  This is the official held-out test set")
        print("⚠️  Used ONLY for final evaluation")
        print()
        
        test_metrics = svm.evaluate(X_test, y_test, verbose=True)
        results["test"] = test_metrics
    else:
        print()
        print("=" * 70)
        print("OFFICIAL TEST SET")
        print("=" * 70)
        print()
        print("⚠️  Test set evaluation SKIPPED (as intended)")
        print("⚠️  Use evaluate_test=True only for final evaluation")
        print()
        results["test"] = None
    
    return results


def save_training_results(
    svm: ClassicalSVM,
    results: Dict,
    train_samples: int,
    val_samples: int,
    test_samples: int,
    config: Dict,
):
    """
    Save training results and metadata
    
    Args:
        svm: Trained ClassicalSVM instance
        results: Evaluation results
        train_samples: Number of training samples
        val_samples: Number of validation samples
        test_samples: Number of test samples
        config: SVM configuration
    """
    print("=" * 70)
    print("SAVING TRAINING RESULTS")
    print("=" * 70)
    print()
    
    # Save trained model
    svm.save(str(CLASSICAL_SVM_PATH))
    
    # Prepare metadata
    metadata = {
        "training_date": datetime.now().isoformat(),
        "model_type": "Classical SVM",
        "input_dimension": 4,
        "feature_source": "PCA-reduced ResNet50 features",
        "random_seed": RANDOM_SEED,
        "configuration": config,
        "dataset": {
            "train_samples": train_samples,
            "val_samples": val_samples,
            "test_samples": test_samples,
            "class_names": CLASS_NAMES,
            "class_mapping": CLASS_LABELS,
        },
        "validation_metrics": results["validation"],
        "test_metrics": results["test"],
    }
    
    # Save metadata
    metadata_path = RESULTS_DIR / "classical_svm_training_results.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Training results saved to: {metadata_path}")
    print()


def print_medical_interpretation(metrics: Dict):
    """
    Print medical interpretation of results
    
    Args:
        metrics: Evaluation metrics dictionary
    """
    print("=" * 70)
    print("MEDICAL TRIAGE INTERPRETATION")
    print("=" * 70)
    print()
    print("For medical triage systems, key metrics:")
    print()
    print(f"1. RECALL/SENSITIVITY (Pneumonia): {metrics['recall']:.4f}")
    print(f"   → Percentage of actual pneumonia cases correctly identified")
    print(f"   → Higher is better (minimize missed diagnoses)")
    print()
    print(f"2. PRECISION (Pneumonia): {metrics['precision']:.4f}")
    print(f"   → Percentage of pneumonia predictions that are correct")
    print(f"   → Higher is better (minimize false alarms)")
    print()
    
    # Analyze confusion matrix
    cm = metrics['confusion_matrix']
    tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
    
    print("3. CONFUSION MATRIX INTERPRETATION:")
    print(f"   True Negatives (TN):  {tn} — Correctly identified NORMAL")
    print(f"   False Positives (FP): {fp} — NORMAL misclassified as PNEUMONIA")
    print(f"   False Negatives (FN): {fn} — PNEUMONIA misclassified as NORMAL ⚠️")
    print(f"   True Positives (TP):  {tp} — Correctly identified PNEUMONIA")
    print()
    print("⚠️  False Negatives (FN) are particularly critical in medical triage:")
    print("   Missing actual pneumonia cases could delay necessary treatment.")
    print()
    print(f"4. OVERALL ACCURACY: {metrics['accuracy']:.4f}")
    print(f"   Overall percentage of correct predictions")
    print()
    print(f"5. F1 SCORE: {metrics['f1_score']:.4f}")
    print(f"   Harmonic mean of precision and recall")
    print()
    print(f"6. ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"   Model's ability to distinguish between classes")
    print(f"   (1.0 = perfect, 0.5 = random)")
    print()


def main(evaluate_test: bool = False):
    """
    Main training pipeline
    
    Args:
        evaluate_test: Whether to evaluate on official test set (default: False)
    """
    print("=" * 70)
    print("CLASSICAL SVM TRAINING PIPELINE")
    print("=" * 70)
    print()
    print("Establishing classical baseline for comparison with quantum classifier")
    print()
    
    # Verify class mapping
    verify_class_mapping()
    
    # Load PCA-reduced 4D features
    print("=" * 70)
    print("LOADING PCA-REDUCED 4D FEATURES")
    print("=" * 70)
    print()
    
    X_train, y_train = load_pca_features("train")
    X_val, y_val = load_pca_features("val")
    X_test, y_test = load_pca_features("test")
    
    print()
    print("Data loaded:")
    print(f"  Training: {X_train.shape[0]} samples")
    print(f"  Validation: {X_val.shape[0]} samples")
    print(f"  Test: {X_test.shape[0]} samples")
    print(f"  Feature dimension: {X_train.shape[1]}D")
    print()
    
    # Train SVM
    svm = train_classical_svm(
        X_train,
        y_train,
        kernel="rbf",
        C=1.0,
        gamma="scale",
    )
    
    # Evaluate
    print()
    results = evaluate_and_report(
        svm,
        X_val,
        y_val,
        X_test,
        y_test,
        evaluate_test=evaluate_test,
    )
    
    # Print medical interpretation
    print()
    print_medical_interpretation(results["validation"])
    
    # Save results
    save_training_results(
        svm,
        results,
        train_samples=len(X_train),
        val_samples=len(X_val),
        test_samples=len(X_test),
        config={
            "kernel": "rbf",
            "C": 1.0,
            "gamma": "scale",
        },
    )
    
    # Final summary
    print("=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print()
    print("✓ Classical SVM trained on 4D PCA features")
    print("✓ Model saved for inference")
    print("✓ Validation metrics recorded")
    print()
    print("This classical baseline can now be compared with:")
    print("  → Quantum QSVM (same 4D representation)")
    print("  → Fair comparison using identical data splits")
    print()
    print("=" * 70)


if __name__ == "__main__":
    # By default, evaluate only on validation set
    # Set evaluate_test=True only for final evaluation
    main(evaluate_test=False)
