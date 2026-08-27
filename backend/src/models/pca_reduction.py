"""
PCA Dimensionality Reduction for Q-MedTriage

Reduces high-dimensional CNN features to a compact representation
suitable for quantum processing.

Target: 2048D → 4D
"""

import numpy as np
from sklearn.decomposition import PCA
import joblib
from pathlib import Path
from typing import Tuple, Optional


class PCAReducer:
    """PCA-based dimensionality reduction for CNN features"""

    def __init__(self, n_components: int = 4, random_state: int = 42):
        """
        Initialize PCA reducer

        Args:
            n_components: Target number of dimensions (default: 4 for quantum)
            random_state: Random state for reproducibility (sklearn PCA is deterministic)
        """
        self.n_components = n_components
        self.random_state = random_state
        self.pca = PCA(n_components=n_components, random_state=random_state)
        self.is_fitted = False

    def fit(self, features: np.ndarray) -> "PCAReducer":
        """
        Fit PCA on training features

        Args:
            features: Training features of shape (n_samples, n_features)

        Returns:
            Self for method chaining
        """
        print(f"Fitting PCA: {features.shape[1]}D → {self.n_components}D")

        self.pca.fit(features)
        self.is_fitted = True

        # Print explained variance
        explained_var = self.pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)

        print(f"\nExplained Variance per Component:")
        for i, (var, cum) in enumerate(zip(explained_var, cumulative_var)):
            print(f"  PC{i+1}: {var:.4f} (Cumulative: {cum:.4f})")

        print(f"\nTotal variance retained: {cumulative_var[-1]:.4f}")

        return self

    def transform(self, features: np.ndarray) -> np.ndarray:
        """
        Transform features using fitted PCA

        Args:
            features: Features of shape (n_samples, n_features)

        Returns:
            Reduced features of shape (n_samples, n_components)
        """
        if not self.is_fitted:
            raise ValueError("PCA must be fitted before transform")

        return self.pca.transform(features)

    def fit_transform(self, features: np.ndarray) -> np.ndarray:
        """
        Fit PCA and transform features in one step

        Args:
            features: Features of shape (n_samples, n_features)

        Returns:
            Reduced features of shape (n_samples, n_components)
        """
        return self.fit(features).transform(features)

    def inverse_transform(self, reduced_features: np.ndarray) -> np.ndarray:
        """
        Reconstruct original feature space from reduced features

        Args:
            reduced_features: Reduced features of shape (n_samples, n_components)

        Returns:
            Reconstructed features of shape (n_samples, original_n_features)
        """
        if not self.is_fitted:
            raise ValueError("PCA must be fitted before inverse_transform")

        return self.pca.inverse_transform(reduced_features)

    def get_components(self) -> np.ndarray:
        """
        Get principal components

        Returns:
            Principal components of shape (n_components, n_features)
        """
        if not self.is_fitted:
            raise ValueError("PCA must be fitted first")

        return self.pca.components_

    def get_explained_variance_ratio(self) -> np.ndarray:
        """Get explained variance ratio for each component"""
        if not self.is_fitted:
            raise ValueError("PCA must be fitted first")

        return self.pca.explained_variance_ratio_

    def save(self, path: str = "models/pca_reducer.pkl"):
        """
        Save fitted PCA model

        Args:
            path: Path to save model
        """
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted PCA")

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pca, path)
        print(f"PCA model saved to: {path}")

    @classmethod
    def load(cls, path: str = "models/pca_reducer.pkl") -> "PCAReducer":
        """
        Load fitted PCA model

        Args:
            path: Path to saved model

        Returns:
            Loaded PCAReducer instance
        """
        reducer = cls(n_components=4)  # Will be overwritten
        reducer.pca = joblib.load(path)
        reducer.n_components = reducer.pca.n_components
        reducer.is_fitted = True

        print(f"PCA model loaded from: {path}")
        print(f"Components: {reducer.n_components}")

        return reducer


def analyze_pca_quality(
    original_features: np.ndarray, reduced_features: np.ndarray, pca_reducer: PCAReducer
) -> dict:
    """
    Analyze quality of PCA compression

    Args:
        original_features: Original high-dimensional features
        reduced_features: PCA-reduced features
        pca_reducer: Fitted PCA reducer

    Returns:
        Dictionary with quality metrics
    """
    # Reconstruct features
    reconstructed = pca_reducer.inverse_transform(reduced_features)

    # Calculate reconstruction error
    mse = np.mean((original_features - reconstructed) ** 2)
    relative_error = mse / np.mean(original_features**2)

    # Get variance explained
    var_explained = pca_reducer.get_explained_variance_ratio()
    total_var = np.sum(var_explained)

    metrics = {
        "reconstruction_mse": float(mse),
        "relative_error": float(relative_error),
        "variance_explained": float(total_var),
        "n_components": pca_reducer.n_components,
        "per_component_variance": var_explained.tolist(),
    }

    return metrics


if __name__ == "__main__":
    # Example usage
    print("PCA Reducer for Q-MedTriage")
    print("=" * 50)
    print("\nUsage:")
    print("  # Fit on training features")
    print("  reducer = PCAReducer(n_components=4)")
    print("  reduced_train = reducer.fit_transform(train_features)")
    print()
    print("  # Transform test features")
    print("  reduced_test = reducer.transform(test_features)")
    print()
    print("  # Save for later use")
    print("  reducer.save('models/pca_reducer.pkl')")
    print()
    print("  # Load saved model")
    print("  reducer = PCAReducer.load('models/pca_reducer.pkl')")
