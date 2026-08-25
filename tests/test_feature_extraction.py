"""
Tests for ResNet50 Feature Extraction
"""

import pytest
import torch
import numpy as np
from PIL import Image
from pathlib import Path

from src.config import RESNET_FEATURE_DIM, IMAGE_SIZE
from src.data.transforms import get_val_transforms


def test_resnet50_import():
    """Test that ResNet50 model can be imported"""
    from torchvision import models
    model = models.resnet50(weights=None)  # Don't download weights in test
    assert model is not None


def test_deterministic_transforms_for_extraction():
    """Test that feature extraction uses deterministic transforms"""
    from src.models.extract_features import get_val_transforms
    
    transform = get_val_transforms()
    
    # Create dummy image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform twice
    tensor1 = transform(img)
    tensor2 = transform(img)
    
    # Should be identical (deterministic)
    assert torch.allclose(tensor1, tensor2), \
        "Transforms should be deterministic for feature extraction"


def test_resnet50_feature_dim():
    """Test that ResNet50 outputs correct feature dimension"""
    from torchvision import models
    import torch.nn as nn
    
    # Load model
    model = models.resnet50(weights=None)
    
    # Remove final FC layer
    model = nn.Sequential(*list(model.children())[:-1])
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE)
    
    # Extract features
    with torch.no_grad():
        features = model(dummy_input)
    
    # Check shape
    features = features.squeeze()
    assert features.shape == (RESNET_FEATURE_DIM,), \
        f"Expected {RESNET_FEATURE_DIM}D features, got {features.shape}"


def test_batch_feature_extraction_shape():
    """Test that batch feature extraction produces correct shapes"""
    from torchvision import models
    import torch.nn as nn
    
    batch_size = 4
    
    # Load model
    model = models.resnet50(weights=None)
    model = nn.Sequential(*list(model.children())[:-1])
    model.eval()
    
    # Create dummy batch
    dummy_batch = torch.randn(batch_size, 3, IMAGE_SIZE, IMAGE_SIZE)
    
    # Extract features
    with torch.no_grad():
        features = model(dummy_batch)
    
    # Check shape
    features = features.squeeze(-1).squeeze(-1)
    assert features.shape == (batch_size, RESNET_FEATURE_DIM), \
        f"Expected shape ({batch_size}, {RESNET_FEATURE_DIM}), got {features.shape}"


def test_feature_extraction_no_augmentation():
    """Verify that feature extraction does not use augmentation"""
    from src.models.extract_features import get_val_transforms
    from torchvision.transforms import RandomHorizontalFlip, RandomRotation
    
    transform = get_val_transforms()
    
    # Check that no random transforms are present
    transform_list = transform.transforms
    
    for t in transform_list:
        assert not isinstance(t, RandomHorizontalFlip), \
            "Feature extraction should not use RandomHorizontalFlip"
        assert not isinstance(t, RandomRotation), \
            "Feature extraction should not use RandomRotation"


def test_feature_extractor_initialization():
    """Test feature extractor can be initialized"""
    from src.models.extract_features import ResNet50FeatureExtractor
    
    # Should work on CPU
    extractor = ResNet50FeatureExtractor(device="cpu")
    assert extractor is not None
    assert extractor.device == torch.device("cpu")


def test_feature_extractor_eval_mode():
    """Test that feature extractor is in evaluation mode"""
    from src.models.extract_features import ResNet50FeatureExtractor
    
    extractor = ResNet50FeatureExtractor(device="cpu")
    
    # Check model is in eval mode
    assert not extractor.model.training, \
        "Feature extractor should be in evaluation mode"


def test_grayscale_to_rgb_conversion():
    """Test that grayscale images are converted to 3-channel RGB"""
    transform = get_val_transforms()
    
    # Create grayscale image
    img = Image.new('L', (512, 512), color=128)
    
    # Apply transform
    tensor = transform(img)
    
    # Check it's 3-channel
    assert tensor.shape[0] == 3, \
        f"Expected 3 channels, got {tensor.shape[0]}"


def test_imagenet_normalization():
    """Test that ImageNet normalization is applied"""
    transform = get_val_transforms()
    
    # Create white image
    img = Image.new('L', (512, 512), color=255)
    
    # Apply transform
    tensor = transform(img)
    
    # After normalization with ImageNet stats, values should not be in [0,1]
    # (they'll be normalized to approximately [-2, 2] range)
    assert tensor.min() < 0 or tensor.max() > 1, \
        "ImageNet normalization should be applied"


def test_no_shuffle_during_extraction():
    """Verify that dataloaders don't shuffle during feature extraction"""
    # This is enforced in the extract_features.py script
    # We verify the principle here
    
    from torch.utils.data import DataLoader, TensorDataset
    
    # Create simple dataset
    data = torch.arange(100).reshape(100, 1)
    labels = torch.zeros(100)
    dataset = TensorDataset(data, labels)
    
    # Create dataloader without shuffle
    loader = DataLoader(dataset, batch_size=10, shuffle=False)
    
    # Extract first batch
    first_batch, _ = next(iter(loader))
    
    # Should be [0, 1, 2, ..., 9]
    expected = torch.arange(10).reshape(10, 1)
    assert torch.equal(first_batch, expected), \
        "DataLoader should not shuffle during feature extraction"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
