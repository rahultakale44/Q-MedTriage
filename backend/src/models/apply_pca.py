"""
PCA Dimensionality Reduction Pipeline for Q-MedTriage

Reduces ResNet50 features (2048D) to 4D representation suitable for
quantum processing.

CRITICAL RULES:
- PCA is FIT ONLY on training features
- Validation and test features are TRANSFORMED using the fitted PCA
- Never fit PCA on validation or test data (prevents data leakage)
- Saves fitted PCA model for reproducibility
- Records explained variance for analysis
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple
import json
from datetime import datetime

from src.config import (
    FEATURE_CACHE_DIR,
    PCA_MODEL_PATH,
    PCA_COMPONENTS,
    RANDOM_SEED,
    RESNET_FEATURE_DIM,
)
from src.models.pca_reduction import PCAReducer, analyze_pca_quality


def load_features(split: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load extracted features for a specific split
    
    Args:
        split: 'train', 'val', or 'test'
        
    Returns:
        Tuple of (features, labels)
    """
    features_path = FEATURE_CACHE_DIR / f"{split}_features.npy"
    labels_path = FEATURE_CACHE_DIR / f"{split}_labels.npy"
    
    if not features_path.exists():
        raise FileNotFoundError(
            f"Features not found: {features_path}\n"
            f"Run 'python src/models/extract_features.py' first to extract features."
        )
    
    features = np.load(features_path)
    labels = np.load(labels_path)
    
    print(f"✓ Loaded {split} features: {features.shape}")
    print(f"  Labels: {labels.shape}")
    
    return features, labels


def apply_pca_reduction(
    train_features: np.ndarray,
    val_features: np.ndarray,
    test_features: np.ndarray,
    n_components: int = PCA_COMPONENTS,
    save_model: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, PCAReducer]:
    """
    Apply PCA reduction to all feature sets
    
    IMPORTANT: PCA is fit ONLY on training features, then applied to val/test
    
    Args:
        train_features: Training features (N_train, 2048)
        val_features: Validation features (N_val, 2048)
        test_features: Test features (N_test, 2048)
        n_components: Number of PCA components (default: 4)
        save_model: Whether to save the fitted PCA model
        
    Returns:
        Tuple of (train_reduced, val_reduced, test_reduced, pca_reducer)
    """
    print("=" * 70)
    print("PCA DIMENSIONALITY REDUCTION")
    print("=" * 70)
    print()
    
    # Verify input shapes
    print("Input feature shapes:")
    print(f"  Train: {train_features.shape}")
    print(f"  Val: {val_features.shape}")
    print(f"  Test: {test_features.shape}")
    print()
    
    assert train_features.shape[1] == RESNET_FEATURE_DIM, \
        f"Expected {RESNET_FEATURE_DIM}D features, got {train_features.shape[1]}D"
    
    # Initialize PCA reducer with random state for reproducibility
    # Note: sklearn PCA is deterministic by default (no randomness in algorithm)
    # but we set random_state for any potential stochastic operations
    reducer = PCAReducer(n_components=n_components)
    
    # FIT PCA ON TRAINING DATA ONLY
    print("=" * 70)
    print("FITTING PCA ON TRAINING DATA ONLY")
    print("=" * 70)
    print()
    print("⚠️  CRITICAL: PCA is fitted ONLY on training features")
    print("⚠️  Validation and test features will be transformed using this fit")
    print()
    
    train_reduced = reducer.fit_transform(train_features)
    
    print()
    print("=" * 70)
    print("TRANSFORMING VALIDATION DATA")
    print("=" * 70)
    print()
    print("⚠️  Using PCA fitted on training data (NO REFITTING)")
    print()
    
    val_reduced = reducer.transform(val_features)
    
    print(f"✓ Validation features transformed: {val_reduced.shape}")
    print()
    
    print("=" * 70)
    print("TRANSFORMING TEST DATA")
    print("=" * 70)
    print()
    print("⚠️  Using PCA fitted on training data (NO REFITTING)")
    print("⚠️  Official test set remains isolated")
    print()
    
    test_reduced = reducer.transform(test_features)
    
    print(f"✓ Test features transformed: {test_reduced.shape}")
    print()
    
    # Verify output shapes
    assert train_reduced.shape == (len(train_features), n_components)
    assert val_reduced.shape == (len(val_features), n_components)
    assert test_reduced.shape == (len(test_features), n_components)
    
    # Save fitted PCA model
    if save_model:
        print("=" * 70)
        print("SAVING FITTED PCA MODEL")
        print("=" * 70)
        print()
        reducer.save(str(PCA_MODEL_PATH))
        print()
    
    return train_reduced, val_reduced, test_reduced, reducer


def save_reduced_features(
    train_reduced: np.ndarray,
    val_reduced: np.ndarray,
    test_reduced: np.ndarray,
    train_labels: np.ndarray,
    val_labels: np.ndarray,
    test_labels: np.ndarray,
) -> Dict:
    """
    Save PCA-reduced features to disk
    
    Args:
        train_reduced: Reduced training features (N_train, 4)
        val_reduced: Reduced validation features (N_val, 4)
        test_reduced: Reduced test features (N_test, 4)
        train_labels: Training labels
        val_labels: Validation labels
        test_labels: Test labels
        
    Returns:
        Dictionary with saved file paths
    """
    print("=" * 70)
    print("SAVING REDUCED FEATURES")
    print("=" * 70)
    print()
    
    # Save reduced features
    train_path = FEATURE_CACHE_DIR / "train_features_pca4d.npy"
    val_path = FEATURE_CACHE_DIR / "val_features_pca4d.npy"
    test_path = FEATURE_CACHE_DIR / "test_features_pca4d.npy"
    
    np.save(train_path, train_reduced)
    np.save(val_path, val_reduced)
    np.save(test_path, test_reduced)
    
    print(f"✓ Saved training features: {train_path}")
    print(f"  Shape: {train_reduced.shape}")
    print(f"✓ Saved validation features: {val_path}")
    print(f"  Shape: {val_reduced.shape}")
    print(f"✓ Saved test features: {test_path}")
    print(f"  Shape: {test_reduced.shape}")
    print()
    
    # Also save labels alongside for convenience
    np.save(FEATURE_CACHE_DIR / "train_labels_pca4d.npy", train_labels)
    np.save(FEATURE_CACHE_DIR / "val_labels_pca4d.npy", val_labels)
    np.save(FEATURE_CACHE_DIR / "test_labels_pca4d.npy", test_labels)
    
    return {
        "train": str(train_path),
        "val": str(val_path),
        "test": str(test_path),
    }


def save_pca_metadata(
    reducer: PCAReducer,
    train_features: np.ndarray,
    val_features: np.ndarray,
    test_features: np.ndarray,
    train_reduced: np.ndarray,
    val_reduced: np.ndarray,
    test_reduced: np.ndarray,
    saved_paths: Dict,
):
    """
    Save comprehensive metadata about PCA reduction
    
    Args:
        reducer: Fitted PCAReducer instance
        train_features: Original training features
        val_features: Original validation features
        test_features: Original test features
        train_reduced: Reduced training features
        val_reduced: Reduced validation features
        test_reduced: Reduced test features
        saved_paths: Dictionary of saved feature file paths
    """
    # Analyze PCA quality for training set
    quality_metrics = analyze_pca_quality(train_features, train_reduced, reducer)
    
    # Get explained variance
    explained_var = reducer.get_explained_variance_ratio()
    cumulative_var = np.cumsum(explained_var)
    
    metadata = {
        "reduction_date": datetime.now().isoformat(),
        "method": "PCA (Principal Component Analysis)",
        "input_dimension": RESNET_FEATURE_DIM,
        "output_dimension": PCA_COMPONENTS,
        "random_seed": RANDOM_SEED,
        "fitted_on": "training_features_only",
        "explained_variance_per_component": {
            f"PC{i+1}": float(var) 
            for i, var in enumerate(explained_var)
        },
        "cumulative_explained_variance": {
            f"PC{i+1}": float(cum)
            for i, cum in enumerate(cumulative_var)
        },
        "total_variance_retained": float(cumulative_var[-1]),
        "quality_metrics": quality_metrics,
        "split_shapes": {
            "train": {
                "original": train_features.shape,
                "reduced": train_reduced.shape,
            },
            "val": {
                "original": val_features.shape,
                "reduced": val_reduced.shape,
            },
            "test": {
                "original": test_features.shape,
                "reduced": test_reduced.shape,
            },
        },
        "output_files": saved_paths,
        "pca_model_path": str(PCA_MODEL_PATH),
    }
    
    metadata_path = FEATURE_CACHE_DIR / "pca_reduction_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("=" * 70)
    print("PCA METADATA SAVED")
    print("=" * 70)
    print()
    print(f"✓ Metadata saved to: {metadata_path}")
    print()
    print("Explained Variance Summary:")
    for i, (var, cum) in enumerate(zip(explained_var, cumulative_var)):
        print(f"  PC{i+1}: {var:.4f} ({var*100:.2f}%) — Cumulative: {cum:.4f} ({cum*100:.2f}%)")
    print()
    print(f"Total variance retained: {cumulative_var[-1]:.4f} ({cumulative_var[-1]*100:.2f}%)")
    print()


def main():
    """Main PCA reduction pipeline"""
    print("=" * 70)
    print("PCA DIMENSIONALITY REDUCTION PIPELINE")
    print("=" * 70)
    print()
    print(f"Target: {RESNET_FEATURE_DIM}D → {PCA_COMPONENTS}D")
    print(f"Random seed: {RANDOM_SEED}")
    print()
    
    # Load features
    print("=" * 70)
    print("LOADING EXTRACTED FEATURES")
    print("=" * 70)
    print()
    
    train_features, train_labels = load_features("train")
    val_features, val_labels = load_features("val")
    test_features, test_labels = load_features("test")
    
    print()
    
    # Apply PCA reduction
    train_reduced, val_reduced, test_reduced, reducer = apply_pca_reduction(
        train_features,
        val_features,
        test_features,
        n_components=PCA_COMPONENTS,
        save_model=True,
    )
    
    # Save reduced features
    saved_paths = save_reduced_features(
        train_reduced, val_reduced, test_reduced,
        train_labels, val_labels, test_labels,
    )
    
    # Save metadata
    save_pca_metadata(
        reducer,
        train_features, val_features, test_features,
        train_reduced, val_reduced, test_reduced,
        saved_paths,
    )
    
    # Final summary
    print("=" * 70)
    print("PCA REDUCTION COMPLETE")
    print("=" * 70)
    print()
    print("Reduced features:")
    print(f"  Train: {train_features.shape} → {train_reduced.shape}")
    print(f"  Val: {val_features.shape} → {val_reduced.shape}")
    print(f"  Test: {test_features.shape} → {test_reduced.shape}")
    print()
    print("✓ PCA fitted on training data only")
    print("✓ Validation/test transformed using fitted PCA")
    print("✓ No data leakage")
    print("✓ Official test set isolation maintained")
    print()
    print("Next steps:")
    print("  1. Train Classical SVM on 4D features")
    print("  2. Train Quantum QSVM on 4D features")
    print("  3. Compare performance on same 4D representation")
    print("=" * 70)


if __name__ == "__main__":
    main()
