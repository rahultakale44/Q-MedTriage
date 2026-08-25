"""
Tests for Preprocessing Pipeline
"""

import pytest
import torch
import numpy as np
from PIL import Image
from pathlib import Path

from src.data.transforms import (
    get_train_transforms,
    get_val_transforms,
    get_test_transforms,
)
from src.config import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


def test_train_transforms_output_shape():
    """Test that training transforms produce correct tensor shape"""
    transform = get_train_transforms()
    
    # Create dummy grayscale image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform
    tensor = transform(img)
    
    # Check shape
    assert tensor.shape == (3, IMAGE_SIZE, IMAGE_SIZE), \
        f"Expected shape (3, {IMAGE_SIZE}, {IMAGE_SIZE}), got {tensor.shape}"
    
    # Check dtype
    assert tensor.dtype == torch.float32


def test_val_transforms_output_shape():
    """Test that validation transforms produce correct tensor shape"""
    transform = get_val_transforms()
    
    # Create dummy grayscale image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform
    tensor = transform(img)
    
    # Check shape
    assert tensor.shape == (3, IMAGE_SIZE, IMAGE_SIZE)
    assert tensor.dtype == torch.float32


def test_test_transforms_output_shape():
    """Test that test transforms produce correct tensor shape"""
    transform = get_test_transforms()
    
    # Create dummy grayscale image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform
    tensor = transform(img)
    
    # Check shape
    assert tensor.shape == (3, IMAGE_SIZE, IMAGE_SIZE)
    assert tensor.dtype == torch.float32


def test_val_test_transforms_identical():
    """Test that validation and test transforms are identical"""
    val_transform = get_val_transforms()
    test_transform = get_test_transforms()
    
    # Create dummy image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transforms
    val_tensor = val_transform(img)
    test_tensor = test_transform(img)
    
    # Should be identical (deterministic)
    assert torch.allclose(val_tensor, test_tensor)


def test_val_transforms_deterministic():
    """Test that validation transforms are deterministic"""
    transform = get_val_transforms()
    
    # Create dummy image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform multiple times
    tensor1 = transform(img)
    tensor2 = transform(img)
    
    # Should be identical
    assert torch.allclose(tensor1, tensor2)


def test_transforms_handle_different_sizes():
    """Test transforms with various input sizes"""
    transform = get_val_transforms()
    
    sizes = [(224, 224), (512, 512), (1024, 768), (300, 400)]
    
    for size in sizes:
        img = Image.new('L', size, color=128)
        tensor = transform(img)
        
        # All should output same size
        assert tensor.shape == (3, IMAGE_SIZE, IMAGE_SIZE)


def test_normalization_applied():
    """Test that ImageNet normalization is applied"""
    transform = get_val_transforms()
    
    # Create white image
    img = Image.new('L', (224, 224), color=255)
    tensor = transform(img)
    
    # After normalization, values should be different from [0, 1] range
    # (they'll be normalized using ImageNet stats)
    assert tensor.min() < 0 or tensor.max() > 1, \
        "Normalization doesn't appear to be applied"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
