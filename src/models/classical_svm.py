"""
Classical SVM Classifier for Q-MedTriage

This module implements the classical baseline classifier using Support Vector Machine.
It operates on PCA-reduced features (4D) for fair comparison with the quantum classifier.
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
import joblib
from pathlib import Path
from typing import Dict, Tuple


class ClassicalSVM:
    """Classical SVM classifier for pneumonia detection"""

    def __init__(self, kernel: str = "rbf", C: float = 1.0, gamma: str = "scale"):
        """
        Initialize Classical SVM

        Args:
            kernel: Kernel type ('linear', 'rbf', 'poly')
            C: Regularization parameter
            gamma: Kernel coefficient
        """
        self.model = SVC(
            kernel=kernel, C=C, gamma=gamma, probability=True, random_state=42
        )
        self.is_trained = False

        print(f"Classical SVM initialized")
        print(f"  Kernel: {kernel}")
        print(f"  C: {C}")
        print(f"  Gamma: {gamma}")

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> "ClassicalSVM":
        """
        Train the SVM classifier

        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)

        Returns:
            Self for method chaining
        """
        print(f"\nTraining Classical SVM...")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Feature dimension: {X_train.shape[1]}")

        self.model.fit(X_train, y_train)
        self.is_trained = True

        print("Training complete!")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels

        Args:
            X: Features (n_samples, n_features)

        Returns:
            Predicted labels (n_samples,)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities

        Args:
            X: Features (n_samples, n_features)

        Returns:
            Probability estimates (n_samples, n_classes)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        return self.model.predict_proba(X)

    def evaluate(
        self, X_test: np.ndarray, y_test: np.ndarray, verbose: bool = True
    ) -> Dict:
        """
        Evaluate model performance

        Args:
            X_test: Test features
            y_test: Test labels
            verbose: Whether to print results

        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        # Predictions
        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)[:, 1]  # Probability of positive class

        # Calculate metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_proba),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        }

        if verbose:
            print("\nClassical SVM Performance:")
            print("=" * 50)
            print(f"Accuracy:  {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall:    {metrics['recall']:.4f}")
            print(f"F1 Score:  {metrics['f1_score']:.4f}")
            print(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
            print("\nConfusion Matrix:")
            print(f"  {metrics['confusion_matrix']}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, target_names=["NORMAL", "PNEUMONIA"]))

        return metrics

    def save(self, path: str = "models/classical_svm.pkl"):
        """
        Save trained model

        Args:
            path: Path to save model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)
        print(f"Classical SVM saved to: {path}")

    @classmethod
    def load(cls, path: str = "models/classical_svm.pkl") -> "ClassicalSVM":
        """
        Load trained model

        Args:
            path: Path to saved model

        Returns:
            Loaded ClassicalSVM instance
        """
        classifier = cls()
        classifier.model = joblib.load(path)
        classifier.is_trained = True

        print(f"Classical SVM loaded from: {path}")

        return classifier


if __name__ == "__main__":
    print("Classical SVM Classifier for Q-MedTriage")
    print("=" * 50)
    print("\nThis is the classical baseline for comparison with QSVM")
    print("\nUsage:")
    print("  # Train")
    print("  svm = ClassicalSVM(kernel='rbf')")
    print("  svm.train(X_train, y_train)")
    print()
    print("  # Evaluate")
    print("  metrics = svm.evaluate(X_test, y_test)")
    print()
    print("  # Predict")
    print("  predictions = svm.predict(X_new)")
    print("  probabilities = svm.predict_proba(X_new)")
