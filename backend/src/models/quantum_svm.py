"""
Quantum Support Vector Machine for Q-MedTriage.

COMMIT 10/30
Uses a 4-qubit fidelity quantum kernel on the frozen 4D PCA features
produced by COMMIT 08.
"""

from pathlib import Path
from typing import Dict, Optional

import joblib
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

try:
    from qiskit.circuit.library import zz_feature_map
    from qiskit.primitives import StatevectorSampler
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    from qiskit_machine_learning.state_fidelities import ComputeUncompute
    QISKIT_AVAILABLE = True
except (ImportError, TypeError) as e:
    print(f"Warning: Qiskit imports failed: {e}")
    QISKIT_AVAILABLE = False
    zz_feature_map = None
    StatevectorSampler = None
    QSVC = None
    FidelityQuantumKernel = None
    ComputeUncompute = None


CLASS_LABELS = {
    "NORMAL": 0,
    "PNEUMONIA": 1,
}

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]


class QuantumSVM:
    """
    Quantum Support Vector Classifier using a fidelity quantum kernel.

    Input:
        4D PCA-reduced ResNet50 features.

    Output:
        NORMAL (0) or PNEUMONIA (1).
    """

    def __init__(
        self,
        feature_dimension: int = 4,
        reps: int = 2,
        entanglement: str = "linear",
        C: float = 1.0,
        probability: bool = True,
        random_state: int = 42,
    ):
        if feature_dimension != 4:
            raise ValueError(
                "QuantumSVM expects exactly 4 PCA features / 4 qubits."
            )

        self.feature_dimension = feature_dimension
        self.reps = reps
        self.entanglement = entanglement
        self.C = C
        self.probability = probability
        self.random_state = random_state

        # 4D PCA → 4 qubits
        self.feature_map = zz_feature_map(
            feature_dimension=feature_dimension,
            reps=reps,
            entanglement=entanglement,
        )

        # Deterministic statevector-based sampler.
        sampler = StatevectorSampler()

        # Fidelity calculation using Compute-Uncompute.
        fidelity = ComputeUncompute(
            sampler=sampler
        )

        # Modern Qiskit ML quantum kernel.
        self.quantum_kernel = FidelityQuantumKernel(
            feature_map=self.feature_map,
            fidelity=fidelity,
            enforce_psd=True,
        )

        self.model = QSVC(
            quantum_kernel=self.quantum_kernel,
            C=C,
            probability=probability,
            random_state=random_state,
        )

        self.is_trained = False

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
    ) -> "QuantumSVM":
        """Train QSVC using training data only."""

        X_train = np.asarray(X_train)
        y_train = np.asarray(y_train)

        self._validate_features(X_train)
        self._validate_labels(y_train)

        print("Training Quantum SVM...")
        print(f"Training samples: {len(X_train)}")
        print(f"Feature dimension: {X_train.shape[1]}")
        print(f"Qubits: {self.feature_dimension}")
        print(f"Feature-map repetitions: {self.reps}")
        print(f"Entanglement: {self.entanglement}")
        print(f"C: {self.C}")

        self.model.fit(X_train, y_train)

        self.is_trained = True

        print("Quantum SVM training complete!")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""

        self._check_trained()

        X = np.asarray(X)
        self._validate_features(X)

        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Return probability estimates."""

        self._check_trained()

        X = np.asarray(X)
        self._validate_features(X)

        if not self.probability:
            raise ValueError(
                "Probability estimation is disabled."
            )

        return self.model.predict_proba(X)

    def evaluate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        verbose: bool = True,
    ) -> Dict:
        """Evaluate QSVM using medical-triage metrics."""

        self._check_trained()

        X = np.asarray(X)
        y = np.asarray(y)

        self._validate_features(X)
        self._validate_labels(y)

        predictions = self.predict(X)

        metrics = {
            "accuracy": accuracy_score(y, predictions),
            "precision": precision_score(
                y,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y,
                predictions,
                zero_division=0,
            ),
            "f1_score": f1_score(
                y,
                predictions,
                zero_division=0,
            ),
            "confusion_matrix": confusion_matrix(
                y,
                predictions,
            ),
        }

        if self.probability:
            probabilities = self.predict_proba(X)

            # PNEUMONIA probability.
            pneumonia_probability = probabilities[:, 1]

            try:
                metrics["roc_auc"] = roc_auc_score(
                    y,
                    pneumonia_probability,
                )
            except ValueError:
                metrics["roc_auc"] = float("nan")

        if verbose:
            self._print_metrics(metrics)

        return metrics

    def save(
        self,
        path: str = "models/quantum_svm.pkl",
    ) -> None:
        """Persist the QSVM model."""

        self._check_trained()

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self, path)

        print(f"Quantum SVM saved to: {path}")

    @classmethod
    def load(
        cls,
        path: str = "models/quantum_svm.pkl",
    ) -> "QuantumSVM":
        """Load a persisted QSVM."""

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Quantum SVM model not found: {path}"
            )

        classifier = joblib.load(path)

        if not isinstance(classifier, cls):
            raise TypeError(
                "Saved object is not a QuantumSVM instance."
            )

        classifier.is_trained = True

        print(f"Quantum SVM loaded from: {path}")

        return classifier

    def _validate_features(self, X: np.ndarray) -> None:
        """Validate 4D feature matrix."""

        if X.ndim != 2:
            raise ValueError(
                f"Expected 2D feature matrix, got shape {X.shape}"
            )

        if X.shape[1] != self.feature_dimension:
            raise ValueError(
                f"Expected {self.feature_dimension}D features, "
                f"got {X.shape[1]}D."
            )

        if not np.all(np.isfinite(X)):
            raise ValueError(
                "Features contain NaN or infinite values."
            )

    @staticmethod
    def _validate_labels(y: np.ndarray) -> None:
        """Validate binary NORMAL/PNEUMONIA labels."""

        unique_labels = np.unique(y)

        if not np.all(
            np.isin(unique_labels, [0, 1])
        ):
            raise ValueError(
                f"Invalid class labels: {unique_labels}. "
                "Expected only 0=NORMAL and 1=PNEUMONIA."
            )

    def _check_trained(self) -> None:
        """Ensure the model has been trained."""

        if not self.is_trained:
            raise ValueError(
                "Quantum SVM has not been trained yet."
            )

    @staticmethod
    def _print_metrics(metrics: Dict) -> None:
        """Print evaluation metrics."""

        print()
        print("=" * 60)
        print("QUANTUM SVM EVALUATION")
        print("=" * 60)

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
        print("Confusion Matrix:")
        print(metrics["confusion_matrix"])

        cm = metrics["confusion_matrix"]

        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()

            print()
            print(
                f"False Negatives: {fn} "
                "(PNEUMONIA → NORMAL)"
            )
            print(
                "False negatives are particularly important "
                "for medical triage."
            )

        print("=" * 60)

    def get_feature_map(self):
        """Return the quantum feature map."""

        return self.feature_map