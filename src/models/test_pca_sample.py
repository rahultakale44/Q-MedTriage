"""
PCA Smoke Test

Tests PCA reduction on the 10-image sample features to verify
the pipeline works before running on full dataset.
"""

import numpy as np
from pathlib import Path

from src.config import FEATURE_CACHE_DIR, PCA_COMPONENTS, RESNET_FEATURE_DIM, RANDOM_SEED
from src.models.pca_reduction import PCAReducer, analyze_pca_quality


def main():
    """Run PCA smoke test on sample features"""
    print("=" * 70)
    print("PCA REDUCTION SMOKE TEST")
    print("=" * 70)
    print()
    print("Testing PCA reduction on 10-image sample...")
    print()
    
    # Load sample features
    sample_features_path = FEATURE_CACHE_DIR / "sample_test_features.npy"
    sample_labels_path = FEATURE_CACHE_DIR / "sample_test_labels.npy"
    
    if not sample_features_path.exists():
        print(f"❌ Sample features not found: {sample_features_path}")
        print()
        print("Run smoke test first:")
        print("  python src/models/test_extraction_sample.py")
        return
    
    features = np.load(sample_features_path)
    labels = np.load(sample_labels_path)
    
    print(f"✓ Loaded sample features: {features.shape}")
    print(f"✓ Loaded sample labels: {labels.shape}")
    print()
    
    # Verify shape
    assert features.shape == (10, RESNET_FEATURE_DIM), \
        f"Unexpected shape: {features.shape}"
    
    # Initialize PCA reducer
    print(f"Initializing PCA reducer ({RESNET_FEATURE_DIM}D → {PCA_COMPONENTS}D)...")
    reducer = PCAReducer(n_components=PCA_COMPONENTS, random_state=RANDOM_SEED)
    print()
    
    # Fit and transform
    print("Fitting PCA and transforming features...")
    reduced = reducer.fit_transform(features)
    print()
    
    # Verify output shape
    assert reduced.shape == (10, PCA_COMPONENTS), \
        f"Unexpected reduced shape: {reduced.shape}"
    
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print()
    print(f"✓ Input shape: {features.shape}")
    print(f"✓ Output shape: {reduced.shape}")
    print(f"✓ Dimension reduction: {RESNET_FEATURE_DIM}D → {PCA_COMPONENTS}D")
    print()
    
    # Get explained variance
    explained_var = reducer.get_explained_variance_ratio()
    cumulative_var = np.cumsum(explained_var)
    
    print("Explained Variance:")
    for i, (var, cum) in enumerate(zip(explained_var, cumulative_var)):
        print(f"  PC{i+1}: {var:.4f} ({var*100:.2f}%) — Cumulative: {cum:.4f} ({cum*100:.2f}%)")
    print()
    print(f"Total variance retained: {cumulative_var[-1]:.4f} ({cumulative_var[-1]*100:.2f}%)")
    print()
    
    # Analyze quality
    print("Quality Analysis:")
    quality = analyze_pca_quality(features, reduced, reducer)
    print(f"  Reconstruction MSE: {quality['reconstruction_mse']:.4f}")
    print(f"  Relative Error: {quality['relative_error']:.4f}")
    print()
    
    # Check for NaN/Inf
    assert not np.isnan(reduced).any(), "Reduced features contain NaN!"
    assert not np.isinf(reduced).any(), "Reduced features contain Inf!"
    
    print("✓ No NaN/Inf values in reduced features")
    print()
    
    # Verify deterministic behavior
    print("Testing deterministic behavior...")
    reduced2 = reducer.transform(features)
    assert np.array_equal(reduced, reduced2), "Transform is not deterministic!"
    print("✓ Transform is deterministic (same input → same output)")
    print()
    
    # Test save/load
    print("Testing PCA model save/load...")
    temp_path = FEATURE_CACHE_DIR / "pca_smoke_test.pkl"
    reducer.save(str(temp_path))
    
    # Load and verify
    loaded_reducer = PCAReducer.load(str(temp_path))
    reduced_loaded = loaded_reducer.transform(features)
    
    assert np.allclose(reduced, reduced_loaded), "Loaded model produces different results!"
    print("✓ Saved/loaded model produces identical results")
    print()
    
    # Cleanup
    temp_path.unlink()
    
    print("=" * 70)
    print("PCA SMOKE TEST PASSED")
    print("=" * 70)
    print()
    print("✓ All smoke test checks passed!")
    print()
    print("Ready for full dataset PCA reduction.")
    print()
    print("To apply PCA to full dataset, first extract features:")
    print("  python src/models/extract_features.py")
    print()
    print("Then apply PCA reduction:")
    print("  python src/models/apply_pca.py")
    print()


if __name__ == "__main__":
    main()
