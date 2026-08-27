"""
Tests for PCA Dimensionality Reduction
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import os
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.pca_reduction import PCAReducer, analyze_pca_quality
from src.config import PCA_COMPONENTS, RESNET_FEATURE_DIM, RANDOM_SEED


def test_pca_reducer_initialization():
    """Test PCA reducer can be initialized"""
    reducer = PCAReducer(n_components=4, random_state=RANDOM_SEED)
    
    assert reducer.n_components == 4
    assert reducer.random_state == RANDOM_SEED
    assert not reducer.is_fitted


def test_pca_input_output_dimensions():
    """Test that PCA reduces 2048D to 4D"""
    # Create dummy 2048D features
    n_samples = 100
    train_features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    # Fit and transform
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reduced = reducer.fit_transform(train_features)
    
    # Check output shape
    assert reduced.shape == (n_samples, PCA_COMPONENTS), \
        f"Expected shape ({n_samples}, {PCA_COMPONENTS}), got {reduced.shape}"


def test_pca_fitted_only_on_training():
    """Test that PCA is fitted only on training data"""
    n_train = 100
    n_test = 50
    
    train_features = np.random.randn(n_train, RESNET_FEATURE_DIM)
    test_features = np.random.randn(n_test, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    
    # Fit on training only
    reducer.fit(train_features)
    
    # Transform test (no refitting)
    test_reduced = reducer.transform(test_features)
    
    # Verify shapes
    assert test_reduced.shape == (n_test, PCA_COMPONENTS)
    assert reducer.is_fitted


def test_pca_transform_before_fit_raises_error():
    """Test that transforming before fitting raises an error"""
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    
    dummy_features = np.random.randn(10, RESNET_FEATURE_DIM)
    
    with pytest.raises(ValueError, match="PCA must be fitted before transform"):
        reducer.transform(dummy_features)


def test_pca_deterministic_with_same_seed():
    """Test that PCA with same seed produces identical results"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    # First reduction
    reducer1 = PCAReducer(n_components=PCA_COMPONENTS, random_state=42)
    reduced1 = reducer1.fit_transform(features)
    
    # Second reduction with same seed
    reducer2 = PCAReducer(n_components=PCA_COMPONENTS, random_state=42)
    reduced2 = reducer2.fit_transform(features)
    
    # Should be identical
    np.testing.assert_array_almost_equal(reduced1, reduced2)


def test_pca_different_seeds_may_differ_in_sign():
    """Test that PCA with different seeds may differ in component signs (expected sklearn behavior)"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    # PCA with different seeds
    reducer1 = PCAReducer(n_components=PCA_COMPONENTS, random_state=42)
    reduced1 = reducer1.fit_transform(features)
    
    reducer2 = PCAReducer(n_components=PCA_COMPONENTS, random_state=123)
    reduced2 = reducer2.fit_transform(features)
    
    # sklearn PCA may flip component signs with different random_state
    # This is expected and doesn't affect the quality of the transformation
    # We just verify both produce valid results
    assert reduced1.shape == reduced2.shape
    assert not np.isnan(reduced1).any()
    assert not np.isnan(reduced2).any()


def test_pca_explained_variance():
    """Test that explained variance is recorded correctly"""
    n_samples = 200
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reducer.fit(features)
    
    # Get explained variance
    explained_var = reducer.get_explained_variance_ratio()
    
    # Check shape
    assert explained_var.shape == (PCA_COMPONENTS,)
    
    # Check values are valid (between 0 and 1)
    assert np.all(explained_var >= 0)
    assert np.all(explained_var <= 1)
    
    # Check they sum to <= 1
    assert np.sum(explained_var) <= 1.0


def test_pca_save_and_load():
    """Test that PCA model can be saved and loaded"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        # Fit and save
        reducer1 = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
        reducer1.fit(features)
        reducer1.save(temp_path)
        
        # Load
        reducer2 = PCAReducer.load(temp_path)
        
        # Verify loaded model works
        assert reducer2.is_fitted
        assert reducer2.n_components == PCA_COMPONENTS
        
        # Transform test data with both
        test_features = np.random.randn(50, RESNET_FEATURE_DIM)
        reduced1 = reducer1.transform(test_features)
        reduced2 = reducer2.transform(test_features)
        
        # Should produce identical results
        np.testing.assert_array_almost_equal(reduced1, reduced2)
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_pca_no_data_leakage():
    """Test that validation/test transformation doesn't leak information"""
    n_train = 200
    n_val = 50
    n_test = 50
    
    # Create distinct datasets
    train_features = np.random.randn(n_train, RESNET_FEATURE_DIM)
    val_features = np.random.randn(n_val, RESNET_FEATURE_DIM)
    test_features = np.random.randn(n_test, RESNET_FEATURE_DIM)
    
    # Fit on training only
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    train_reduced = reducer.fit_transform(train_features)
    
    # Get components fitted on training data
    components_from_train = reducer.get_components().copy()
    
    # Transform validation and test
    val_reduced = reducer.transform(val_features)
    test_reduced = reducer.transform(test_features)
    
    # Verify components didn't change (no refitting occurred)
    components_after_transform = reducer.get_components()
    np.testing.assert_array_equal(components_from_train, components_after_transform)
    
    # Verify output shapes
    assert train_reduced.shape == (n_train, PCA_COMPONENTS)
    assert val_reduced.shape == (n_val, PCA_COMPONENTS)
    assert test_reduced.shape == (n_test, PCA_COMPONENTS)


def test_pca_inverse_transform():
    """Test that inverse transform reconstructs features"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reduced = reducer.fit_transform(features)
    
    # Reconstruct
    reconstructed = reducer.inverse_transform(reduced)
    
    # Should have original dimensionality
    assert reconstructed.shape == features.shape
    
    # Should be similar but not identical (lossy compression)
    # Just check it doesn't crash and has reasonable values


def test_pca_quality_analysis():
    """Test PCA quality analysis function"""
    n_samples = 100
    original = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reduced = reducer.fit_transform(original)
    
    # Analyze quality
    metrics = analyze_pca_quality(original, reduced, reducer)
    
    # Check metrics are present
    assert "reconstruction_mse" in metrics
    assert "relative_error" in metrics
    assert "variance_explained" in metrics
    assert "n_components" in metrics
    assert "per_component_variance" in metrics
    
    # Check values are reasonable
    assert metrics["n_components"] == PCA_COMPONENTS
    assert 0 <= metrics["variance_explained"] <= 1
    assert len(metrics["per_component_variance"]) == PCA_COMPONENTS


def test_pca_components_shape():
    """Test that PCA components have correct shape"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reducer.fit(features)
    
    components = reducer.get_components()
    
    # Components should be (n_components, n_features)
    assert components.shape == (PCA_COMPONENTS, RESNET_FEATURE_DIM)


def test_pca_transform_consistency():
    """Test that repeated transforms give same results"""
    n_samples = 100
    features = np.random.randn(n_samples, RESNET_FEATURE_DIM)
    
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    reducer.fit(features)
    
    # Transform twice
    reduced1 = reducer.transform(features)
    reduced2 = reducer.transform(features)
    
    # Should be identical
    np.testing.assert_array_equal(reduced1, reduced2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
