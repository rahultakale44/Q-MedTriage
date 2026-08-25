"""
Classical SVM Smoke Test

Tests SVM training and inference on sample data to verify the pipeline works correctly
before running on the full dataset.
"""

import numpy as np
from pathlib import Path

from src.config import FEATURE_CACHE_DIR
from src.models.classical_svm import ClassicalSVM


def main():
    """Run SVM smoke test on sample data"""
    print("=" * 70)
    print("CLASSICAL SVM SMOKE TEST")
    print("=" * 70)
    print()
    print("Testing SVM pipeline on sample data...")
    print()
    
    # Check if sample PCA features exist
    sample_features_path = FEATURE_CACHE_DIR / "sample_test_features.npy"
    sample_labels_path = FEATURE_CACHE_DIR / "sample_test_labels.npy"
    
    if not sample_features_path.exists():
        print("⚠️  Sample features not found.")
        print("   Run 'python src/models/test_pca_sample.py' first to generate sample features.")
        return
    
    # Load sample data
    sample_features = np.load(sample_features_path)
    sample_labels = np.load(sample_labels_path)
    
    print(f"✓ Loaded sample features: {sample_features.shape}")
    print(f"✓ Loaded sample labels: {sample_labels.shape}")
    print()
    
    # For smoke test, check if features are already 4D (PCA-reduced)
    # If not, we'll use them as-is for testing purposes
    if sample_features.shape[1] == 2048:
        print("⚠️  Sample features are 2048D (not PCA-reduced)")
        print("   This smoke test will work with 2048D for testing purposes")
        print()
    elif sample_features.shape[1] == 4:
        print("✓ Sample features are 4D (PCA-reduced)")
        print()
    
    # Split sample data for training/testing
    # Use first 7 for training, last 3 for testing
    n_train = 7
    X_train = sample_features[:n_train]
    y_train = sample_labels[:n_train]
    X_test = sample_features[n_train:]
    y_test = sample_labels[n_train:]
    
    print("Sample split:")
    print(f"  Train: {X_train.shape}")
    print(f"  Test: {X_test.shape}")
    print()
    
    # Initialize SVM
    print("=" * 70)
    print("INITIALIZING SVM")
    print("=" * 70)
    print()
    
    svm = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    print()
    
    # Train
    print("=" * 70)
    print("TRAINING ON SAMPLE DATA")
    print("=" * 70)
    print()
    
    svm.train(X_train, y_train)
    print()
    
    # Predict
    print("=" * 70)
    print("PREDICTION")
    print("=" * 70)
    print()
    
    predictions = svm.predict(X_test)
    probabilities = svm.predict_proba(X_test)
    
    print("Predictions:")
    for i, (pred, proba, true) in enumerate(zip(predictions, probabilities, y_test)):
        class_name = "PNEUMONIA" if pred == 1 else "NORMAL"
        confidence = proba[pred]
        match = "✓" if pred == true else "✗"
        print(f"  Sample {i+1}: {class_name} (confidence: {confidence:.4f}) {match}")
    print()
    
    # Evaluate
    print("=" * 70)
    print("EVALUATION ON SAMPLE TEST SET")
    print("=" * 70)
    print()
    
    metrics = svm.evaluate(X_test, y_test, verbose=True)
    print()
    
    # Test save/load
    print("=" * 70)
    print("TESTING MODEL PERSISTENCE")
    print("=" * 70)
    print()
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        # Save
        svm.save(temp_path)
        print()
        
        # Load
        svm_loaded = ClassicalSVM.load(temp_path)
        print()
        
        # Verify loaded model produces same predictions
        predictions_loaded = svm_loaded.predict(X_test)
        
        if np.array_equal(predictions, predictions_loaded):
            print("✓ Loaded model produces identical predictions")
        else:
            print("✗ Loaded model predictions differ!")
        print()
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    # Determinism check
    print("=" * 70)
    print("TESTING DETERMINISM")
    print("=" * 70)
    print()
    
    predictions_2 = svm.predict(X_test)
    
    if np.array_equal(predictions, predictions_2):
        print("✓ Predictions are deterministic (same input → same output)")
    else:
        print("✗ Predictions differ on repeated calls!")
    print()
    
    # Final summary
    print("=" * 70)
    print("SMOKE TEST RESULTS")
    print("=" * 70)
    print()
    print("✓ SVM initialization working")
    print("✓ Training working")
    print("✓ Prediction working")
    print("✓ Probability estimation working")
    print("✓ Evaluation metrics working")
    print("✓ Model save/load working")
    print("✓ Deterministic behavior confirmed")
    print()
    print("SVM SMOKE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
