"""
ResNet50 Feature Extraction for Kermany Dataset

Extracts 2048-dimensional CNN features from chest X-ray images using
pretrained ResNet50 for downstream classification tasks.

IMPORTANT:
- Uses deterministic (validation/test) transforms for ALL splits
- No augmentation during feature extraction (ensures reproducibility)
- Processes train, validation, and test separately (prevents leakage)
- Saves features with metadata for reproducibility
"""

import torch
import torch.nn as nn
from torchvision import models
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple
from tqdm import tqdm
import json
from datetime import datetime

from src.config import (
    PROCESSED_DATA_DIR,
    FEATURE_CACHE_DIR,
    RESNET_FEATURE_DIM,
    BATCH_SIZE,
    NUM_WORKERS,
    RANDOM_SEED,
)
from src.data.pytorch_dataset import KermanyPneumoniaDataset
from src.data.transforms import get_val_transforms  # Deterministic only!


class ResNet50FeatureExtractor:
    """
    ResNet50 feature extractor for medical images
    
    Extracts 2048-D features from the penultimate layer of pretrained ResNet50.
    """
    
    def __init__(self, device: str = "auto"):
        """
        Initialize feature extractor
        
        Args:
            device: 'auto', 'cuda', or 'cpu'
        """
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        print(f"Initializing ResNet50 Feature Extractor...")
        print(f"Device: {self.device}")
        
        # Load pretrained ResNet50
        print("Loading pretrained ResNet50 (ImageNet weights)...")
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        
        # Remove final FC layer to get 2048-D features
        # ResNet50 architecture: ... -> AvgPool -> FC(2048 -> 1000)
        # We want the 2048-D output before FC
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        
        self.model = self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
        
        print(f"✓ ResNet50 loaded successfully")
        print(f"✓ Feature dimension: {RESNET_FEATURE_DIM}D")
        print()
    
    def extract_features_from_dataloader(
        self,
        dataloader: DataLoader,
        desc: str = "Extracting features"
    ) -> Tuple[np.ndarray, np.ndarray, list]:
        """
        Extract features from a DataLoader
        
        Args:
            dataloader: DataLoader with images
            desc: Progress bar description
            
        Returns:
            features: Array of shape (N, 2048)
            labels: Array of shape (N,)
            paths: List of image paths (if available)
        """
        all_features = []
        all_labels = []
        all_paths = []
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc=desc):
                # Unpack batch (handle both with/without paths)
                if len(batch) == 3:
                    images, labels, paths = batch
                    all_paths.extend(paths)
                else:
                    images, labels = batch
                
                # Move to device
                images = images.to(self.device)
                
                # Extract features
                features = self.model(images)
                
                # Flatten from (batch, 2048, 1, 1) to (batch, 2048)
                features = features.squeeze(-1).squeeze(-1)
                
                # Store
                all_features.append(features.cpu().numpy())
                all_labels.append(labels.numpy())
        
        # Concatenate all batches
        features = np.vstack(all_features)
        labels = np.concatenate(all_labels)
        
        return features, labels, all_paths


def extract_and_save_features(
    split_name: str,
    df: pd.DataFrame,
    extractor: ResNet50FeatureExtractor,
    batch_size: int = BATCH_SIZE,
    num_workers: int = NUM_WORKERS,
) -> Dict:
    """
    Extract features for a specific split and save to disk
    
    Args:
        split_name: 'train', 'val', or 'test'
        df: DataFrame with image_path and label columns
        extractor: ResNet50FeatureExtractor instance
        batch_size: Batch size for extraction
        num_workers: Number of data loading workers
        
    Returns:
        Dictionary with extraction statistics
    """
    print("=" * 70)
    print(f"EXTRACTING FEATURES: {split_name.upper()} SET")
    print("=" * 70)
    print(f"Number of images: {len(df)}")
    print(f"Batch size: {batch_size}")
    print()
    
    # Create dataset with deterministic transforms
    # IMPORTANT: No augmentation, even for training set
    dataset = KermanyPneumoniaDataset.from_dataframe(
        df,
        transform=get_val_transforms(),  # Deterministic!
        return_path=True  # Keep paths for metadata
    )
    
    # Create dataloader
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,  # Never shuffle during feature extraction
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
    )
    
    # Extract features
    features, labels, paths = extractor.extract_features_from_dataloader(
        dataloader,
        desc=f"Extracting {split_name} features"
    )
    
    # Verify shapes
    assert features.shape == (len(df), RESNET_FEATURE_DIM), \
        f"Feature shape mismatch: {features.shape} vs ({len(df)}, {RESNET_FEATURE_DIM})"
    assert labels.shape == (len(df),), \
        f"Label shape mismatch: {labels.shape} vs ({len(df)},)"
    
    # Save features
    output_path = FEATURE_CACHE_DIR / f"{split_name}_features.npy"
    labels_path = FEATURE_CACHE_DIR / f"{split_name}_labels.npy"
    paths_path = FEATURE_CACHE_DIR / f"{split_name}_paths.txt"
    
    np.save(output_path, features)
    np.save(labels_path, labels)
    
    with open(paths_path, 'w') as f:
        f.write('\n'.join(paths))
    
    print()
    print(f"✓ Saved features: {output_path}")
    print(f"  Shape: {features.shape}")
    print(f"  Dtype: {features.dtype}")
    print(f"✓ Saved labels: {labels_path}")
    print(f"  Shape: {labels.shape}")
    print(f"✓ Saved paths: {paths_path}")
    print()
    
    # Class distribution
    unique, counts = np.unique(labels, return_counts=True)
    print(f"Class distribution:")
    for label, count in zip(unique, counts):
        class_name = "NORMAL" if label == 0 else "PNEUMONIA"
        print(f"  {class_name} (label={label}): {count} ({count/len(labels):.1%})")
    print()
    
    # Feature statistics
    print(f"Feature statistics:")
    print(f"  Mean: {features.mean():.4f}")
    print(f"  Std: {features.std():.4f}")
    print(f"  Min: {features.min():.4f}")
    print(f"  Max: {features.max():.4f}")
    print()
    
    # Return statistics
    stats = {
        "split": split_name,
        "num_images": len(df),
        "feature_shape": features.shape,
        "feature_dim": RESNET_FEATURE_DIM,
        "class_distribution": {
            int(label): int(count) for label, count in zip(unique, counts)
        },
        "feature_stats": {
            "mean": float(features.mean()),
            "std": float(features.std()),
            "min": float(features.min()),
            "max": float(features.max()),
        },
        "output_files": {
            "features": str(output_path),
            "labels": str(labels_path),
            "paths": str(paths_path),
        }
    }
    
    return stats


def save_extraction_metadata(
    train_stats: Dict,
    val_stats: Dict,
    test_stats: Dict,
    extraction_time: float,
):
    """
    Save metadata about the feature extraction process
    
    Args:
        train_stats: Training set statistics
        val_stats: Validation set statistics
        test_stats: Test set statistics
        extraction_time: Total extraction time in seconds
    """
    metadata = {
        "extraction_date": datetime.now().isoformat(),
        "model": "ResNet50",
        "pretrained_weights": "ImageNet",
        "feature_dimension": RESNET_FEATURE_DIM,
        "preprocessing": "deterministic (validation transforms)",
        "augmentation": "none (deterministic extraction)",
        "random_seed": RANDOM_SEED,
        "device": str(torch.device("cuda" if torch.cuda.is_available() else "cpu")),
        "extraction_time_seconds": extraction_time,
        "splits": {
            "train": train_stats,
            "val": val_stats,
            "test": test_stats,
        },
        "total_images": sum([
            train_stats["num_images"],
            val_stats["num_images"],
            test_stats["num_images"],
        ]),
    }
    
    metadata_path = FEATURE_CACHE_DIR / "extraction_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved extraction metadata: {metadata_path}")


def main():
    """Main feature extraction pipeline"""
    import time
    
    print("=" * 70)
    print("RESNET50 FEATURE EXTRACTION FOR KERMANY DATASET")
    print("=" * 70)
    print()
    
    # Set seeds for reproducibility
    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    # Load splits
    print("Loading data splits...")
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")
    
    print(f"✓ Train: {len(train_df)} images")
    print(f"✓ Val: {len(val_df)} images")
    print(f"✓ Test: {len(test_df)} images")
    print(f"✓ Total: {len(train_df) + len(val_df) + len(test_df)} images")
    print()
    
    # Initialize extractor
    extractor = ResNet50FeatureExtractor(device="auto")
    
    # Start timer
    start_time = time.time()
    
    # Extract features for each split
    train_stats = extract_and_save_features("train", train_df, extractor)
    val_stats = extract_and_save_features("val", val_df, extractor)
    test_stats = extract_and_save_features("test", test_df, extractor)
    
    # End timer
    extraction_time = time.time() - start_time
    
    # Save metadata
    print("=" * 70)
    print("SAVING EXTRACTION METADATA")
    print("=" * 70)
    save_extraction_metadata(train_stats, val_stats, test_stats, extraction_time)
    print()
    
    # Final summary
    print("=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Total time: {extraction_time:.1f} seconds ({extraction_time/60:.1f} minutes)")
    print()
    print("Extracted features:")
    print(f"  Train: {train_stats['num_images']} images → {RESNET_FEATURE_DIM}D features")
    print(f"  Val: {val_stats['num_images']} images → {RESNET_FEATURE_DIM}D features")
    print(f"  Test: {test_stats['num_images']} images → {RESNET_FEATURE_DIM}D features")
    print()
    print("Next steps:")
    print("  1. PCA reduction: 2048D → 4D")
    print("  2. Train Classical SVM on 4D features")
    print("  3. Train Quantum QSVM on 4D features")
    print("  4. Compare performance")
    print("=" * 70)


if __name__ == "__main__":
    main()
