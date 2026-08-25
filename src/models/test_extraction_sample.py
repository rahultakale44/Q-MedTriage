"""
Smoke Test for Feature Extraction

Tests feature extraction on a small sample (10 images from training set)
to verify the pipeline works before running on full dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path

from src.config import PROCESSED_DATA_DIR, RESNET_FEATURE_DIM
from src.models.extract_features import ResNet50FeatureExtractor, extract_and_save_features


def main():
    """Run smoke test on small sample"""
    print("=" * 70)
    print("FEATURE EXTRACTION SMOKE TEST")
    print("=" * 70)
    print()
    print("Testing feature extraction on 10 training images...")
    print()
    
    # Load training data
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    
    # Take small sample (5 NORMAL + 5 PNEUMONIA)
    normal_sample = train_df[train_df['label'] == 0].head(5)
    pneumonia_sample = train_df[train_df['label'] == 1].head(5)
    sample_df = pd.concat([normal_sample, pneumonia_sample]).reset_index(drop=True)
    
    print(f"Sample size: {len(sample_df)} images")
    print(f"  NORMAL: {len(normal_sample)}")
    print(f"  PNEUMONIA: {len(pneumonia_sample)}")
    print()
    
    # Initialize extractor
    extractor = ResNet50FeatureExtractor(device="auto")
    
    # Extract features (use small batch size)
    stats = extract_and_save_features(
        split_name="sample_test",
        df=sample_df,
        extractor=extractor,
        batch_size=2,  # Small batch for smoke test
        num_workers=0,  # Sequential processing for testing
    )
    
    # Verify output
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    
    # Load saved features
    features = np.load(Path("data/features/sample_test_features.npy"))
    labels = np.load(Path("data/features/sample_test_labels.npy"))
    
    print(f"✓ Features shape: {features.shape}")
    print(f"✓ Labels shape: {labels.shape}")
    print(f"✓ Feature dimension: {features.shape[1]} (expected: {RESNET_FEATURE_DIM})")
    
    # Verify shapes
    assert features.shape == (len(sample_df), RESNET_FEATURE_DIM), \
        f"Unexpected feature shape: {features.shape}"
    assert labels.shape == (len(sample_df),), \
        f"Unexpected label shape: {labels.shape}"
    
    # Verify labels match
    expected_labels = sample_df['label'].values
    assert np.array_equal(labels, expected_labels), \
        "Labels don't match!"
    
    # Verify no NaN/Inf values
    assert not np.isnan(features).any(), "Features contain NaN!"
    assert not np.isinf(features).any(), "Features contain Inf!"
    
    print()
    print("✓ All smoke test checks passed!")
    print()
    print("=" * 70)
    print("SMOKE TEST COMPLETE — Ready for full extraction")
    print("=" * 70)
    print()
    print("To extract features for full dataset, run:")
    print("  python src/models/extract_features.py")
    print()


if __name__ == "__main__":
    main()
