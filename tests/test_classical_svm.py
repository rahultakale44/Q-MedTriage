"""
Tests for Classical SVM Classifier
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import os

from src.models.classical_svm import ClassicalSVM
from src.config import RANDOM_SEED


def test_svm_initialization():
    """Test that SVM can be initialized with correct parameters"""
    svm = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    
    assert svm.model is not None
    assert not svm.is_trained
    assert svm.model.kernel == "rbf"
    assert svm.model.C == 1.0
    assert svm.model.gamma == "scale"
    assert svm.model.random_state == RANDOM_SEED


def test_svm_training():
    """Test that SVM can be trained on sample data"""
    # Create dummy 4D features
    n_samples = 100
    n_features = 4
    X_train = np.random.randn(n_samples, n_features)
    y_train = np.random.randint(0, 2, size=n_samples)
    
    svm = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    svm.train(X_train, y_train)
    
    assert svm.is_trained


def test_svm_predict():
    """Test that SVM can make predictions"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Predict
    n_test = 20
    X_test = np.random.randn(n_test, 4)
    predictions = svm.predict(X_test)
    
    assert predictions.shape == (n_test,)
    assert all(pred in [0, 1] for pred in predictions)


def test_svm_predict_proba():
    """Test that SVM can output probability estimates"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Predict probabilities
    n_test = 20
    X_test = np.random.randn(n_test, 4)
    probabilities = svm.predict_proba(X_test)
    
    assert probabilities.shape == (n_test, 2)
    # Probabilities should sum to 1
    np.testing.assert_array_almost_equal(probabilities.sum(axis=1), np.ones(n_test))
    # Probabilities should be in [0, 1]
    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)


def test_svm_predict_before_training_raises_error():
    """Test that prediction before training raises an error"""
    svm = ClassicalSVM(kernel="rbf")
    X_test = np.random.randn(10, 4)
    
    with pytest.raises(ValueError, match="Model must be trained before prediction"):
        svm.predict(X_test)


def test_svm_predict_proba_before_training_raises_error():
    """Test that predict_proba before training raises an error"""
    svm = ClassicalSVM(kernel="rbf")
    X_test = np.random.randn(10, 4)
    
    with pytest.raises(ValueError, match="Model must be trained before prediction"):
        svm.predict_proba(X_test)


def test_svm_evaluate_before_training_raises_error():
    """Test that evaluation before training raises an error"""
    svm = ClassicalSVM(kernel="rbf")
    X_test = np.random.randn(10, 4)
    y_test = np.random.randint(0, 2, size=10)
    
    with pytest.raises(ValueError, match="Model must be trained before evaluation"):
        svm.evaluate(X_test, y_test)


def test_svm_deterministic_predictions():
    """Test that SVM produces deterministic predictions"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    svm.train(X_train, y_train)
    
    # Make predictions twice
    X_test = np.random.randn(20, 4)
    predictions_1 = svm.predict(X_test)
    predictions_2 = svm.predict(X_test)
    
    # Should be identical
    np.testing.assert_array_equal(predictions_1, predictions_2)


def test_svm_evaluation_metrics():
    """Test that SVM evaluation returns expected metrics"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Evaluate
    n_test = 50
    X_test = np.random.randn(n_test, 4)
    y_test = np.random.randint(0, 2, size=n_test)
    
    metrics = svm.evaluate(X_test, y_test, verbose=False)
    
    # Check that all expected metrics are present
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics
    assert "confusion_matrix" in metrics
    
    # Check that metric values are valid
    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["precision"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["f1_score"] <= 1
    assert 0 <= metrics["roc_auc"] <= 1
    
    # Check confusion matrix shape
    cm = metrics["confusion_matrix"]
    assert len(cm) == 2
    assert len(cm[0]) == 2
    assert len(cm[1]) == 2


def test_svm_save_and_load():
    """Test that SVM model can be saved and loaded"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm1 = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    svm1.train(X_train, y_train)
    
    # Save model
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        svm1.save(temp_path)
        
        # Load model
        svm2 = ClassicalSVM.load(temp_path)
        
        # Verify loaded model is trained
        assert svm2.is_trained
        
        # Verify loaded model produces same predictions
        X_test = np.random.randn(20, 4)
        predictions_1 = svm1.predict(X_test)
        predictions_2 = svm2.predict(X_test)
        
        np.testing.assert_array_equal(predictions_1, predictions_2)
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_svm_save_before_training_raises_error():
    """Test that saving before training raises an error"""
    svm = ClassicalSVM(kernel="rbf")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="Cannot save untrained model"):
            svm.save(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_svm_correct_input_dimensions():
    """Test that SVM accepts 4D features as expected"""
    # 4D features (from PCA)
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Test prediction with 4D features
    X_test = np.random.randn(20, 4)
    predictions = svm.predict(X_test)
    
    assert predictions.shape == (20,)


def test_svm_class_labels_valid():
    """Test that predictions contain valid class labels (0 or 1)"""
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Predict
    X_test = np.random.randn(50, 4)
    predictions = svm.predict(X_test)
    
    # All predictions should be 0 or 1
    unique_labels = np.unique(predictions)
    assert all(label in [0, 1] for label in unique_labels)


def test_svm_predicted_class_matches_probability():
    """Test that predicted class corresponds to highest probability"""
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Train SVM
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    svm = ClassicalSVM(kernel="rbf")
    svm.train(X_train, y_train)
    
    # Predict
    X_test = np.random.randn(20, 4)
    predictions = svm.predict(X_test)
    probabilities = svm.predict_proba(X_test)
    
    # Predicted class should generally correspond to argmax of probabilities
    # Allow for minor differences due to SVM decision function vs probability calibration
    predicted_from_proba = np.argmax(probabilities, axis=1)
    match_rate = np.mean(predictions == predicted_from_proba)
    
    # At least 90% should match (allowing for edge cases near decision boundary)
    assert match_rate >= 0.90, f"Only {match_rate:.2%} of predictions match argmax probability"


def test_svm_different_kernels():
    """Test that SVM can be initialized with different kernels"""
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    
    # Test linear kernel
    svm_linear = ClassicalSVM(kernel="linear")
    svm_linear.train(X_train, y_train)
    assert svm_linear.is_trained
    
    # Test RBF kernel
    svm_rbf = ClassicalSVM(kernel="rbf")
    svm_rbf.train(X_train, y_train)
    assert svm_rbf.is_trained
    
    # Test poly kernel
    svm_poly = ClassicalSVM(kernel="poly")
    svm_poly.train(X_train, y_train)
    assert svm_poly.is_trained


def test_svm_reproducibility_with_same_seed():
    """Test that SVM with same seed produces identical results"""
    # Same training data
    np.random.seed(42)
    n_train = 100
    X_train = np.random.randn(n_train, 4)
    y_train = np.random.randint(0, 2, size=n_train)
    X_test = np.random.randn(20, 4)
    
    # Train first SVM
    svm1 = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    svm1.train(X_train, y_train)
    predictions_1 = svm1.predict(X_test)
    
    # Train second SVM (same configuration)
    svm2 = ClassicalSVM(kernel="rbf", C=1.0, gamma="scale")
    svm2.train(X_train, y_train)
    predictions_2 = svm2.predict(X_test)
    
    # Should produce identical results (due to random_state=42)
    np.testing.assert_array_equal(predictions_1, predictions_2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
