"""
Quantum SVM (QSVM) Classifier for Q-MedTriage

This module implements quantum kernel-based classification using Qiskit.
The quantum classifier operates on the same 4D PCA-reduced features as
the classical SVM for fair comparison.

Requirements:
    pip install qiskit qiskit-machine-learning qiskit-aer
"""

import numpy as np
from typing import Dict, Optional

try:
    from qiskit import QuantumCircuit
    from qiskit_machine_learning.kernels import QuantumKernel
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit.primitives import Sampler
    from qiskit.circuit.library import ZZFeatureMap
    
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("Warning: Qiskit not installed. Quantum classifier unavailable.")
    print("Install with: pip install qiskit qiskit-machine-learning qiskit-aer")


class QuantumSVM:
    """
    Quantum SVM classifier using quantum kernel

    Encodes 4D feature vectors into a 4-qubit quantum circuit
    and uses quantum kernel for classification.
    """

    def __init__(self, n_qubits: int = 4, feature_map: str = "ZZFeatureMap", reps: int = 2):
        """
        Initialize Quantum SVM

        Args:
            n_qubits: Number of qubits (should match feature dimension)
            feature_map: Type of feature map ('ZZFeatureMap', 'PauliFeatureMap')
            reps: Number of repetitions in feature map
        """
        if not QISKIT_AVAILABLE:
            raise ImportError(
                "Qiskit not available. Install with: "
                "pip install qiskit qiskit-machine-learning qiskit-aer"
            )

        self.n_qubits = n_qubits
        self.feature_map_type = feature_map
        self.reps = reps
        self.is_trained = False

        # Create feature map
        if feature_map == "ZZFeatureMap":
            self.feature_map = ZZFeatureMap(
                feature_dimension=n_qubits,
                reps=reps,
                entanglement="linear",
            )
        else:
            raise ValueError(f"Unsupported feature map: {feature_map}")

        # Create quantum kernel
        self.sampler = Sampler()
        self.quantum_kernel = QuantumKernel(
            feature_map=self.feature_map,
            sampler=self.sampler,
        )

        # Initialize QSVC
        self.model = QSVC(quantum_kernel=self.quantum_kernel)

        print(f"Quantum SVM initialized")
        print(f"  Qubits: {n_qubits}")
        print(f"  Feature Map: {feature_map}")
        print(f"  Repetitions: {reps}")

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> "QuantumSVM":
        """
        Train the quantum classifier

        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)

        Returns:
            Self for method chaining
        """
        if X_train.shape[1] != self.n_qubits:
            raise ValueError(
                f"Feature dimension ({X_train.shape[1]}) "
                f"must match number of qubits ({self.n_qubits})"
            )

        print(f"\nTraining Quantum SVM...")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Feature dimension: {X_train.shape[1]}")
        print(f"  This may take several minutes due to quantum simulation...")

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
        Predict class probabilities (if available)

        Args:
            X: Features (n_samples, n_features)

        Returns:
            Probability estimates (n_samples, n_classes)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        # QSVC may not support predict_proba directly
        # Use decision function as proxy
        try:
            scores = self.model.decision_function(X)
            # Convert to probabilities using sigmoid
            proba_pos = 1 / (1 + np.exp(-scores))
            proba_neg = 1 - proba_pos
            return np.column_stack([proba_neg, proba_pos])
        except:
            # Fallback: return hard predictions
            predictions = self.predict(X)
            n = len(predictions)
            proba = np.zeros((n, 2))
            proba[predictions == 0, 0] = 1.0
            proba[predictions == 1, 1] = 1.0
            return proba

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
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
            confusion_matrix,
            classification_report,
        )

        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        # Predictions
        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)[:, 1]

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
            print("\nQuantum SVM Performance:")
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

    def get_quantum_circuit(self, x: np.ndarray) -> QuantumCircuit:
        """
        Get the quantum circuit for a given feature vector

        Args:
            x: Single feature vector

        Returns:
            Quantum circuit
        """
        if x.shape[0] != self.n_qubits:
            raise ValueError(
                f"Feature dimension ({x.shape[0]}) "
                f"must match number of qubits ({self.n_qubits})"
            )

        # Bind feature vector to feature map
        circuit = self.feature_map.bind_parameters(x)
        return circuit


if __name__ == "__main__":
    if not QISKIT_AVAILABLE:
        print("Qiskit not available. Please install:")
        print("  pip install qiskit qiskit-machine-learning qiskit-aer")
    else:
        print("Quantum SVM Classifier for Q-MedTriage")
        print("=" * 50)
        print("\nThis quantum classifier will be compared against Classical SVM")
        print("\nUsage:")
        print("  # Train")
        print("  qsvm = QuantumSVM(n_qubits=4)")
        print("  qsvm.train(X_train_4d, y_train)")
        print()
        print("  # Evaluate")
        print("  metrics = qsvm.evaluate(X_test_4d, y_test)")
        print()
        print("  # Get quantum circuit")
        print("  circuit = qsvm.get_quantum_circuit(x_sample)")
