"""
Tests for COMMIT 10 Quantum SVM.
"""

import numpy as np
import pytest

from src.models.quantum_svm import QuantumSVM


@pytest.fixture
def sample_data():
    rng = np.random.default_rng(42)

    X_train = rng.normal(
        0,
        1,
        size=(8, 4),
    )

    y_train = np.array([
        0, 0, 0, 0,
        1, 1, 1, 1,
    ])

    X_test = rng.normal(
        0,
        1,
        size=(4, 4),
    )

    y_test = np.array([
        0, 1, 0, 1,
    ])

    return X_train, y_train, X_test, y_test


def test_qsvm_initialization():
    model = QuantumSVM()

    assert model.feature_dimension == 4
    assert model.reps == 2
    assert model.C == 1.0
    assert model.is_trained is False


def test_qsvm_feature_map_has_four_qubits():
    model = QuantumSVM()

    assert model.feature_map.num_qubits == 4


def test_qsvm_accepts_4d_features(sample_data):
    X_train, y_train, _, _ = sample_data

    model = QuantumSVM()

    model.train(X_train, y_train)

    assert model.is_trained is True


def test_qsvm_predict(sample_data):
    X_train, y_train, X_test, _ = sample_data

    model = QuantumSVM()
    model.train(X_train, y_train)

    predictions = model.predict(X_test)

    assert predictions.shape == (4,)
    assert np.all(
        np.isin(predictions, [0, 1])
    )


def test_qsvm_predict_proba(sample_data):
    X_train, y_train, X_test, _ = sample_data

    model = QuantumSVM()
    model.train(X_train, y_train)

    probabilities = model.predict_proba(X_test)

    assert probabilities.shape == (4, 2)

    np.testing.assert_allclose(
        probabilities.sum(axis=1),
        np.ones(4),
        atol=1e-6,
    )

    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)


def test_qsvm_evaluation(sample_data):
    X_train, y_train, X_test, y_test = sample_data

    model = QuantumSVM()
    model.train(X_train, y_train)

    metrics = model.evaluate(
        X_test,
        y_test,
        verbose=False,
    )

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics
    assert "confusion_matrix" in metrics


def test_qsvm_predict_before_training_raises():
    model = QuantumSVM()

    X = np.random.randn(2, 4)

    with pytest.raises(ValueError):
        model.predict(X)


def test_qsvm_rejects_wrong_dimension():
    model = QuantumSVM()

    X = np.random.randn(10, 2048)
    y = np.zeros(10)

    with pytest.raises(ValueError):
        model.train(X, y)


def test_qsvm_rejects_invalid_labels():
    model = QuantumSVM()

    X = np.random.randn(10, 4)
    y = np.array([0, 1, 2, 0, 1, 0, 1, 0, 1, 0])

    with pytest.raises(ValueError):
        model.train(X, y)


def test_qsvm_rejects_nan():
    model = QuantumSVM()

    X = np.random.randn(10, 4)
    X[0, 0] = np.nan

    y = np.array([
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
    ])

    with pytest.raises(ValueError):
        model.train(X, y)