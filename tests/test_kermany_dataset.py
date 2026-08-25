"""
Tests for Kermany Dataset Handler
"""

import pytest
from pathlib import Path
from src.data.kermany_dataset import KermanyDataset, CLASS_LABELS


def test_dataset_initialization():
    """Test dataset handler initialization"""
    dataset = KermanyDataset()
    assert dataset.data_root is not None
    assert dataset.classes == ["NORMAL", "PNEUMONIA"]
    assert dataset.label_map == CLASS_LABELS


def test_dataset_exists():
    """Test that dataset can be found"""
    dataset = KermanyDataset()
    stats = dataset.inspect_dataset()
    
    assert stats["status"] == "found"
    assert stats["total_images"] > 0
    print(f"\nFound {stats['total_images']} total images")


def test_class_labels():
    """Test class label mapping"""
    assert CLASS_LABELS["NORMAL"] == 0
    assert CLASS_LABELS["PNEUMONIA"] == 1


def test_train_split_exists():
    """Test that training split exists and has images"""
    dataset = KermanyDataset()
    stats = dataset.inspect_dataset()
    
    assert "train" in stats["splits"]
    train_stats = stats["splits"]["train"]
    assert train_stats["status"] == "found"
    assert train_stats["total"] > 0
    
    # Check both classes exist
    assert "NORMAL" in train_stats["classes"]
    assert "PNEUMONIA" in train_stats["classes"]
    assert train_stats["classes"]["NORMAL"]["count"] > 0
    assert train_stats["classes"]["PNEUMONIA"]["count"] > 0


def test_test_split_exists():
    """Test that test split exists and has images"""
    dataset = KermanyDataset()
    stats = dataset.inspect_dataset()
    
    assert "test" in stats["splits"]
    test_stats = stats["splits"]["test"]
    assert test_stats["status"] == "found"
    assert test_stats["total"] > 0


def test_val_split_exists():
    """Test that validation split exists"""
    dataset = KermanyDataset()
    stats = dataset.inspect_dataset()
    
    assert "val" in stats["splits"]
    val_stats = stats["splits"]["val"]
    assert val_stats["status"] == "found"


def test_get_image_paths():
    """Test retrieving image paths"""
    dataset = KermanyDataset()
    
    # Get training images
    train_images = dataset.get_image_paths("train")
    assert len(train_images) > 0
    
    # Get normal class only
    normal_images = dataset.get_image_paths("train", "NORMAL")
    assert len(normal_images) > 0
    assert all("NORMAL" in str(p) for p in normal_images)
    
    # Get pneumonia class only
    pneumonia_images = dataset.get_image_paths("train", "PNEUMONIA")
    assert len(pneumonia_images) > 0
    assert all("PNEUMONIA" in str(p) for p in pneumonia_images)


def test_create_dataframe():
    """Test DataFrame creation"""
    dataset = KermanyDataset()
    
    train_df = dataset.create_dataframe("train")
    assert len(train_df) > 0
    assert "image_path" in train_df.columns
    assert "label" in train_df.columns
    assert "class_name" in train_df.columns
    assert "split" in train_df.columns
    
    # Verify labels
    assert set(train_df["label"].unique()) == {0, 1}
    assert set(train_df["class_name"].unique()) == {"NORMAL", "PNEUMONIA"}


def test_image_formats():
    """Test that all images are in expected format"""
    dataset = KermanyDataset()
    stats = dataset.inspect_dataset()
    
    for split_name, split_data in stats["splits"].items():
        if split_data["status"] == "found":
            for class_name, class_data in split_data["classes"].items():
                formats = class_data.get("formats", [])
                # Kermany dataset uses .jpeg
                assert ".jpeg" in formats or ".jpg" in formats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
