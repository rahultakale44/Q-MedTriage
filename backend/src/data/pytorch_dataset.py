"""
PyTorch Dataset for Kermany Chest X-Ray Images

Provides torch.utils.data.Dataset interface for training/validation/testing.
"""

import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple, Callable, List
import pandas as pd
import numpy as np

from src.config import (
    DATA_ROOT,
    CLASS_LABELS,
    NUM_CLASSES,
    BATCH_SIZE,
    NUM_WORKERS,
    PIN_MEMORY,
    CLASS_WEIGHTS,
)
from src.data.transforms import get_train_transforms, get_val_transforms, get_test_transforms


class KermanyPneumoniaDataset(Dataset):
    """
    PyTorch Dataset for Kermany Chest X-Ray pneumonia detection
    
    Returns:
        image: Preprocessed image tensor [3, 224, 224]
        label: Class label (0=NORMAL, 1=PNEUMONIA)
        image_path: Path to original image file (for debugging/explainability)
    """
    
    def __init__(
        self,
        image_paths: List[Path],
        labels: List[int],
        transform: Optional[Callable] = None,
        return_path: bool = True,
    ):
        """
        Initialize dataset
        
        Args:
            image_paths: List of image file paths
            labels: List of corresponding labels
            transform: Transform to apply to images
            return_path: Whether to return image path with sample
        """
        assert len(image_paths) == len(labels), \
            f"Mismatch: {len(image_paths)} images, {len(labels)} labels"
        
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.return_path = return_path
        
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple:
        """Get a single sample"""
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        # Load image
        try:
            image = Image.open(image_path).convert('L')  # Grayscale
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            # Return a black image as fallback
            image = Image.new('L', (224, 224), color=0)
        
        # Apply transform
        if self.transform is not None:
            image = self.transform(image)
        else:
            # Minimal transform if none provided
            from torchvision import transforms
            default_transform = transforms.Compose([
                transforms.Resize(224),
                transforms.Grayscale(num_output_channels=3),
                transforms.ToTensor(),
            ])
            image = default_transform(image)
        
        # Return with or without path
        if self.return_path:
            return image, label, str(image_path)
        else:
            return image, label
    
    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        transform: Optional[Callable] = None,
        return_path: bool = True,
    ) -> "KermanyPneumoniaDataset":
        """
        Create dataset from DataFrame
        
        Args:
            df: DataFrame with 'image_path' and 'label' columns
            transform: Transform to apply
            return_path: Whether to return paths
            
        Returns:
            KermanyPneumoniaDataset instance
        """
        image_paths = [Path(p) for p in df['image_path'].values]
        labels = df['label'].values.tolist()
        
        return cls(image_paths, labels, transform, return_path)


def create_weighted_sampler(labels: List[int]) -> WeightedRandomSampler:
    """
    Create weighted sampler for handling class imbalance
    
    Args:
        labels: List of training labels
        
    Returns:
        WeightedRandomSampler for balanced batch sampling
    """
    # Count class frequencies
    class_counts = np.bincount(labels, minlength=NUM_CLASSES)
    
    # Calculate weights for each sample
    weights = np.array([CLASS_WEIGHTS[label] for label in labels])
    
    # Create sampler
    sampler = WeightedRandomSampler(
        weights=weights,
        num_samples=len(weights),
        replacement=True  # Allow oversampling minority class
    )
    
    return sampler


def create_dataloaders(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: Optional[pd.DataFrame] = None,
    batch_size: int = BATCH_SIZE,
    num_workers: int = NUM_WORKERS,
    pin_memory: bool = PIN_MEMORY,
    use_weighted_sampler: bool = True,
) -> Tuple[DataLoader, DataLoader, Optional[DataLoader]]:
    """
    Create DataLoaders for training, validation, and test sets
    
    Args:
        train_df: Training DataFrame
        val_df: Validation DataFrame
        test_df: Optional test DataFrame
        batch_size: Batch size for dataloaders
        num_workers: Number of workers for data loading
        pin_memory: Pin memory for faster GPU transfer
        use_weighted_sampler: Use weighted sampling for class imbalance
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    # Create datasets
    train_dataset = KermanyPneumoniaDataset.from_dataframe(
        train_df,
        transform=get_train_transforms(),
        return_path=False  # Don't need paths during training
    )
    
    val_dataset = KermanyPneumoniaDataset.from_dataframe(
        val_df,
        transform=get_val_transforms(),
        return_path=False
    )
    
    # Create samplers
    train_sampler = None
    if use_weighted_sampler:
        train_sampler = create_weighted_sampler(train_df['label'].values.tolist())
        shuffle = False  # Don't shuffle when using sampler
    else:
        shuffle = True
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        sampler=train_sampler,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=True,  # Drop incomplete batches for stable training
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,  # Never shuffle validation
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    
    # Create test loader if test data provided
    test_loader = None
    if test_df is not None:
        test_dataset = KermanyPneumoniaDataset.from_dataframe(
            test_df,
            transform=get_test_transforms(),
            return_path=True  # Keep paths for final evaluation
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,  # Never shuffle test
            num_workers=num_workers,
            pin_memory=pin_memory,
        )
    
    return train_loader, val_loader, test_loader


def print_dataloader_info(
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: Optional[DataLoader] = None,
):
    """Print information about dataloaders"""
    print("=" * 70)
    print("DataLoader Configuration")
    print("=" * 70)
    
    print(f"\nTraining:")
    print(f"  Dataset size: {len(train_loader.dataset)}")
    print(f"  Batch size: {train_loader.batch_size}")
    print(f"  Num batches: {len(train_loader)}")
    print(f"  Sampler: {type(train_loader.sampler).__name__}")
    
    print(f"\nValidation:")
    print(f"  Dataset size: {len(val_loader.dataset)}")
    print(f"  Batch size: {val_loader.batch_size}")
    print(f"  Num batches: {len(val_loader)}")
    
    if test_loader is not None:
        print(f"\nTest:")
        print(f"  Dataset size: {len(test_loader.dataset)}")
        print(f"  Batch size: {test_loader.batch_size}")
        print(f"  Num batches: {len(test_loader)}")
    
    print("=" * 70)


if __name__ == "__main__":
    from src.data.kermany_dataset import KermanyDataset
    
    print("=" * 70)
    print("Testing PyTorch Dataset and DataLoaders")
    print("=" * 70)
    
    # Load split data
    print("\nLoading dataset splits...")
    handler = KermanyDataset()
    
    # Check if processed splits exist
    from src.config import PROCESSED_DATA_DIR
    train_csv = PROCESSED_DATA_DIR / "train.csv"
    
    if not train_csv.exists():
        print("Creating splits...")
        train_df, val_df, test_df = handler.create_splits_csv()
    else:
        print("Loading existing splits...")
        train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
        val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
        test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")
    
    print(f"\nSplit sizes:")
    print(f"  Train: {len(train_df)}")
    print(f"  Val: {len(val_df)}")
    print(f"  Test: {len(test_df)}")
    
    # Create dataloaders
    print("\nCreating dataloaders...")
    train_loader, val_loader, test_loader = create_dataloaders(
        train_df, val_df, test_df,
        batch_size=8,  # Small batch for testing
        num_workers=0,  # 0 for testing
    )
    
    print_dataloader_info(train_loader, val_loader, test_loader)
    
    # Test loading a batch
    print("\nTesting batch loading...")
    images, labels = next(iter(train_loader))
    print(f"  Batch shape: {images.shape}")
    print(f"  Labels shape: {labels.shape}")
    print(f"  Image dtype: {images.dtype}")
    print(f"  Labels: {labels.tolist()}")
    
    print("\n✓ Dataset and DataLoader test passed!")
