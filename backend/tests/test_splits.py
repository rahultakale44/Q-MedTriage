"""
Tests for Data Splits
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROCESSED_DATA_DIR, CLASS_LABELS


@pytest.fixture
def split_dfs():
    """Load split DataFrames"""
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")
    return train_df, val_df, test_df


def test_splits_exist():
    """Test that split files exist"""
    assert (PROCESSED_DATA_DIR / "train.csv").exists()
    assert (PROCESSED_DATA_DIR / "val.csv").exists()
    assert (PROCESSED_DATA_DIR / "test.csv").exists()


def test_required_columns(split_dfs):
    """Test that all required columns are present"""
    train_df, val_df, test_df = split_dfs
    
    required_columns = ['image_path', 'label', 'class_name', 'split']
    
    for df in [train_df, val_df, test_df]:
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"


def test_no_train_val_leakage(split_dfs):
    """Test no overlap between train and validation"""
    train_df, val_df, test_df = split_dfs
    
    train_paths = set(train_df['image_path'].values)
    val_paths = set(val_df['image_path'].values)
    
    overlap = train_paths & val_paths
    assert len(overlap) == 0, f"Train/Val leakage: {len(overlap)} images"


def test_no_train_test_leakage(split_dfs):
    """Test no overlap between train and test"""
    train_df, val_df, test_df = split_dfs
    
    train_paths = set(train_df['image_path'].values)
    test_paths = set(test_df['image_path'].values)
    
    overlap = train_paths & test_paths
    assert len(overlap) == 0, f"Train/Test leakage: {len(overlap)} images"


def test_no_val_test_leakage(split_dfs):
    """Test no overlap between validation and test"""
    train_df, val_df, test_df = split_dfs
    
    val_paths = set(val_df['image_path'].values)
    test_paths = set(test_df['image_path'].values)
    
    overlap = val_paths & test_paths
    assert len(overlap) == 0, f"Val/Test leakage: {len(overlap)} images"


def test_labels_valid(split_dfs):
    """Test that all labels are valid"""
    train_df, val_df, test_df = split_dfs
    
    valid_labels = set(CLASS_LABELS.values())
    
    for df in [train_df, val_df, test_df]:
        labels = set(df['label'].unique())
        assert labels.issubset(valid_labels), f"Invalid labels: {labels - valid_labels}"


def test_no_duplicate_paths(split_dfs):
    """Test that there are no duplicate paths within each split"""
    train_df, val_df, test_df = split_dfs
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        duplicates = df['image_path'].duplicated().sum()
        assert duplicates == 0, f"{name}: {duplicates} duplicate paths"


def test_both_classes_present(split_dfs):
    """Test that both classes are present in each split"""
    train_df, val_df, test_df = split_dfs
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        labels = set(df['label'].unique())
        assert len(labels) == 2, f"{name}: Only {len(labels)} classes present"
        assert labels == {0, 1}, f"{name}: Unexpected labels {labels}"


def test_split_sizes_reasonable(split_dfs):
    """Test that split sizes are reasonable"""
    train_df, val_df, test_df = split_dfs
    
    total = len(train_df) + len(val_df) + len(test_df)
    
    # Train should be largest
    assert len(train_df) > len(val_df)
    assert len(train_df) > len(test_df)
    
    # Each split should have reasonable proportion
    train_ratio = len(train_df) / total
    val_ratio = len(val_df) / total
    test_ratio = len(test_df) / total
    
    assert 0.6 < train_ratio < 0.9, f"Train ratio {train_ratio:.2%} seems off"
    assert 0.05 < val_ratio < 0.3, f"Val ratio {val_ratio:.2%} seems off"
    assert 0.05 < test_ratio < 0.3, f"Test ratio {test_ratio:.2%} seems off"


def test_official_test_preserved(split_dfs):
    """Test that official test set size matches Kermany dataset"""
    train_df, val_df, test_df = split_dfs
    
    # Kermany official test set has 624 images
    assert len(test_df) == 624, f"Test set should be 624 images, got {len(test_df)}"


def test_class_name_label_consistency(split_dfs):
    """Test that class_name and label are consistent"""
    train_df, val_df, test_df = split_dfs
    
    for df in [train_df, val_df, test_df]:
        for idx, row in df.iterrows():
            expected_label = CLASS_LABELS[row['class_name']]
            assert row['label'] == expected_label, \
                f"Inconsistent: {row['class_name']} should be label {expected_label}, got {row['label']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
