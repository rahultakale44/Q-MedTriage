"""
Image Preprocessing and Augmentation for Q-MedTriage

Provides transform pipelines for training, validation, and test data.
"""

from torchvision import transforms
from src.config import (
    IMAGE_SIZE,
    IMAGENET_MEAN,
    IMAGENET_STD,
    TRAIN_AUGMENTATION,
    VAL_TEST_PREPROCESSING,
)


def get_train_transforms():
    """
    Get training transforms with augmentation
    
    Augmentation strategy for chest X-rays:
    - Horizontal flip: Safe for chest X-rays (left/right symmetry)
    - Mild rotation: Small angles to avoid distorting anatomy
    - Brightness/contrast: Slight adjustments for imaging variations
    - NO vertical flip: Not appropriate for chest X-rays
    - NO aggressive transforms: Preserve clinical features
    
    Returns:
        transforms.Compose: Training transform pipeline
    """
    return transforms.Compose([
        transforms.Resize(TRAIN_AUGMENTATION["resize"]),
        transforms.RandomCrop(TRAIN_AUGMENTATION["crop_size"]),
        transforms.RandomHorizontalFlip(p=TRAIN_AUGMENTATION["horizontal_flip_prob"]),
        transforms.RandomRotation(
            degrees=TRAIN_AUGMENTATION["rotation_degrees"],
            fill=0  # Fill with black (appropriate for X-rays)
        ),
        transforms.ColorJitter(
            brightness=TRAIN_AUGMENTATION["brightness"],
            contrast=TRAIN_AUGMENTATION["contrast"]
        ),
        transforms.Grayscale(num_output_channels=3),  # Convert grayscale to 3-channel
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_val_transforms():
    """
    Get validation transforms (deterministic preprocessing only)
    
    NO augmentation - validation must be reproducible for model selection.
    
    Returns:
        transforms.Compose: Validation transform pipeline
    """
    return transforms.Compose([
        transforms.Resize(VAL_TEST_PREPROCESSING["resize"]),
        transforms.CenterCrop(VAL_TEST_PREPROCESSING["center_crop"]),
        transforms.Grayscale(num_output_channels=3),  # Convert grayscale to 3-channel
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_test_transforms():
    """
    Get test transforms (identical to validation)
    
    NO augmentation - test set must be reproducible for final evaluation.
    
    Returns:
        transforms.Compose: Test transform pipeline
    """
    return get_val_transforms()  # Same as validation


def get_inference_transforms():
    """
    Get transforms for inference/deployment
    
    Returns:
        transforms.Compose: Inference transform pipeline
    """
    return get_val_transforms()  # Same as validation/test


# ============================================================================
# TRANSFORM VERIFICATION
# ============================================================================

def verify_transform_output(transform, image_path: str = None):
    """
    Verify that transforms produce correct tensor shape
    
    Args:
        transform: Transform to verify
        image_path: Optional path to test image
    """
    from PIL import Image
    import torch
    
    # Create dummy image if no path provided
    if image_path is None:
        img = Image.new('L', (512, 512), color=128)  # Grayscale
    else:
        img = Image.open(image_path).convert('L')
    
    # Apply transform
    tensor = transform(img)
    
    print(f"Input image size: {img.size}")
    print(f"Output tensor shape: {tensor.shape}")
    print(f"Expected shape: [3, {IMAGE_SIZE}, {IMAGE_SIZE}]")
    
    # Verify shape
    assert tensor.shape == (3, IMAGE_SIZE, IMAGE_SIZE), \
        f"Incorrect tensor shape: {tensor.shape}"
    
    # Verify value range (after normalization)
    print(f"Tensor value range: [{tensor.min():.3f}, {tensor.max():.3f}]")
    
    print("✓ Transform verification passed")


if __name__ == "__main__":
    print("=" * 70)
    print("Q-MedTriage Transform Pipelines")
    print("=" * 70)
    
    print("\n1. TRAINING TRANSFORMS (with augmentation):")
    print("-" * 70)
    train_transforms = get_train_transforms()
    print(train_transforms)
    
    print("\n2. VALIDATION TRANSFORMS (deterministic):")
    print("-" * 70)
    val_transforms = get_val_transforms()
    print(val_transforms)
    
    print("\n3. TEST TRANSFORMS (deterministic):")
    print("-" * 70)
    test_transforms = get_test_transforms()
    print(test_transforms)
    
    print("\n4. VERIFYING TRANSFORM OUTPUT:")
    print("-" * 70)
    verify_transform_output(train_transforms)
    
    print("\n" + "=" * 70)
    print("All transforms configured successfully")
    print("=" * 70)
