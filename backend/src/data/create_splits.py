"""
Create Reproducible Train/Validation/Test Splits for Kermany Dataset

SPLIT STRATEGY:
1. OFFICIAL TEST SET: Preserved exactly as provided (624 images)
   - NEVER used during training or hyperparameter tuning
   - Used ONLY for final model evaluation

2. OFFICIAL VAL SET: Too small (16 images) - NOT USED
   - Kermany's validation set is insufficient for reliable model selection
   
3. NEW VALIDATION SET: Created from original training data
   - Stratified split: 80% train, 20% validation
   - Fixed random seed (42) for reproducibility
   - Class-balanced to maintain representative distribution

IMPORTANT:
- This is an IMAGE-LEVEL split (patient IDs not available in directory structure)
- No patient-level deduplication possible with current dataset metadata
- Assumes Kermany et al. performed patient-level separation in their original splits
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple
from sklearn.model_selection import train_test_split

from src.data.kermany_dataset import KermanyDataset
from src.config import (
    DATA_ROOT,
    PROCESSED_DATA_DIR,
    RANDOM_SEED,
    VAL_RATIO,
    CLASS_LABELS,
)


def create_reproducible_splits(
    random_seed: int = RANDOM_SEED,
    val_ratio: float = VAL_RATIO,
    output_dir: Path = PROCESSED_DATA_DIR,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Create reproducible train/validation/test splits
    
    Args:
        random_seed: Random seed for reproducibility
        val_ratio: Validation ratio (from original train data)
        output_dir: Directory to save split CSVs
        
    Returns:
        Tuple of (train_df, val_df, test_df)
    """
    print("=" * 70)
    print("Creating Reproducible Splits for Kermany Dataset")
    print("=" * 70)
    
    # Initialize dataset handler
    handler = KermanyDataset(data_root=str(DATA_ROOT))
    
    # Verify dataset exists
    stats = handler.inspect_dataset()
    if stats["status"] != "found":
        raise FileNotFoundError(f"Dataset not found at {DATA_ROOT}")
    
    print(f"\n✓ Dataset found: {stats['total_images']} images")
    
    # ========================================================================
    # STEP 1: PRESERVE OFFICIAL TEST SET
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 1: Preserving Official Test Set")
    print("=" * 70)
    
    test_df = handler.create_dataframe("test")
    print(f"\nOfficial test set: {len(test_df)} images")
    print(f"  NORMAL: {len(test_df[test_df['label'] == 0])}")
    print(f"  PNEUMONIA: {len(test_df[test_df['label'] == 1])}")
    print(f"  Class balance: NORMAL={len(test_df[test_df['label'] == 0])/len(test_df):.2%}")
    
    # ========================================================================
    # STEP 2: LOAD ORIGINAL TRAINING DATA
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 2: Loading Original Training Data")
    print("=" * 70)
    
    original_train_df = handler.create_dataframe("train")
    print(f"\nOriginal train set: {len(original_train_df)} images")
    print(f"  NORMAL: {len(original_train_df[original_train_df['label'] == 0])}")
    print(f"  PNEUMONIA: {len(original_train_df[original_train_df['label'] == 1])}")
    
    # ========================================================================
    # STEP 3: CREATE NEW TRAIN/VALIDATION SPLIT
    # ========================================================================
    print("\n" + "=" * 70)
    print(f"STEP 3: Creating Train/Validation Split (ratio={val_ratio:.0%})")
    print("=" * 70)
    
    # Set random seed for reproducibility
    np.random.seed(random_seed)
    
    # Stratified split by class
    train_indices = []
    val_indices = []
    
    for class_label in [0, 1]:
        # Get indices for this class
        class_mask = original_train_df['label'] == class_label
        class_indices = original_train_df[class_mask].index.tolist()
        
        # Split with stratification
        class_train, class_val = train_test_split(
            class_indices,
            test_size=val_ratio,
            random_state=random_seed,
            shuffle=True,
        )
        
        train_indices.extend(class_train)
        val_indices.extend(class_val)
        
        class_name = "NORMAL" if class_label == 0 else "PNEUMONIA"
        print(f"\n{class_name}:")
        print(f"  Total: {len(class_indices)}")
        print(f"  Train: {len(class_train)} ({len(class_train)/len(class_indices):.1%})")
        print(f"  Val: {len(class_val)} ({len(class_val)/len(class_indices):.1%})")
    
    # Create final split DataFrames
    train_df = original_train_df.loc[train_indices].copy()
    val_df = original_train_df.loc[val_indices].copy()
    
    # Update split column
    train_df['split'] = 'train'
    val_df['split'] = 'val'
    test_df['split'] = 'test'
    
    # Reset indices
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    
    # ========================================================================
    # STEP 4: VERIFY SPLITS
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 4: Verifying Splits")
    print("=" * 70)
    
    # Check for leakage
    train_paths = set(train_df['image_path'].values)
    val_paths = set(val_df['image_path'].values)
    test_paths = set(test_df['image_path'].values)
    
    train_val_overlap = train_paths & val_paths
    train_test_overlap = train_paths & test_paths
    val_test_overlap = val_paths & test_paths
    
    print(f"\nLeakage check:")
    print(f"  Train ∩ Val: {len(train_val_overlap)} images")
    print(f"  Train ∩ Test: {len(train_test_overlap)} images")
    print(f"  Val ∩ Test: {len(val_test_overlap)} images")
    
    if len(train_val_overlap) > 0 or len(train_test_overlap) > 0 or len(val_test_overlap) > 0:
        raise ValueError("❌ DATA LEAKAGE DETECTED!")
    
    print("  ✓ No data leakage detected")
    
    # Verify totals
    total = len(train_df) + len(val_df) + len(test_df)
    expected = len(original_train_df) + len(test_df)
    
    print(f"\nTotal images:")
    print(f"  Expected: {expected}")
    print(f"  Actual: {total}")
    
    if total != expected:
        raise ValueError(f"❌ Image count mismatch: {total} != {expected}")
    
    print("  ✓ Image counts verified")
    
    # ========================================================================
    # STEP 5: PRINT FINAL STATISTICS
    # ========================================================================
    print("\n" + "=" * 70)
    print("FINAL SPLIT STATISTICS")
    print("=" * 70)
    
    def print_split_stats(df, name):
        total = len(df)
        normal = len(df[df['label'] == 0])
        pneumonia = len(df[df['label'] == 1])
        
        print(f"\n{name}:")
        print(f"  Total: {total}")
        print(f"  NORMAL: {normal} ({normal/total:.1%})")
        print(f"  PNEUMONIA: {pneumonia} ({pneumonia/total:.1%})")
    
    print_split_stats(train_df, "TRAINING")
    print_split_stats(val_df, "VALIDATION")
    print_split_stats(test_df, "TEST (OFFICIAL)")
    
    print(f"\nSplit ratios:")
    total_images = len(train_df) + len(val_df) + len(test_df)
    print(f"  Train: {len(train_df)/total_images:.1%}")
    print(f"  Val: {len(val_df)/total_images:.1%}")
    print(f"  Test: {len(test_df)/total_images:.1%}")
    
    # ========================================================================
    # STEP 6: SAVE SPLITS
    # ========================================================================
    print("\n" + "=" * 70)
    print("STEP 6: Saving Splits")
    print("=" * 70)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    train_path = output_dir / "train.csv"
    val_path = output_dir / "val.csv"
    test_path = output_dir / "test.csv"
    
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"\n✓ Saved splits:")
    print(f"  {train_path}")
    print(f"  {val_path}")
    print(f"  {test_path}")
    
    # Save split configuration
    config_path = output_dir / "split_config.txt"
    with open(config_path, 'w') as f:
        f.write("KERMANY DATASET SPLIT CONFIGURATION\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Random seed: {random_seed}\n")
        f.write(f"Validation ratio: {val_ratio:.1%}\n")
        f.write(f"Split strategy: Stratified image-level split\n\n")
        f.write(f"Training: {len(train_df)} images\n")
        f.write(f"Validation: {len(val_df)} images\n")
        f.write(f"Test: {len(test_df)} images (official Kermany split)\n\n")
        f.write("IMPORTANT NOTES:\n")
        f.write("- Official test set preserved and NEVER used during training\n")
        f.write("- Validation created from original train data (stratified)\n")
        f.write("- Image-level split (patient metadata not available)\n")
        f.write("- Reproducible with fixed random seed\n")
    
    print(f"  {config_path}")
    
    print("\n" + "=" * 70)
    print("✓ SPLITS CREATED SUCCESSFULLY")
    print("=" * 70)
    
    return train_df, val_df, test_df


if __name__ == "__main__":
    # Create splits
    train_df, val_df, test_df = create_reproducible_splits()
    
    print("\n" + "=" * 70)
    print("USAGE")
    print("=" * 70)
    print("\nTo load splits in your training script:")
    print("```python")
    print("import pandas as pd")
    print("from src.config import PROCESSED_DATA_DIR")
    print()
    print("train_df = pd.read_csv(PROCESSED_DATA_DIR / 'train.csv')")
    print("val_df = pd.read_csv(PROCESSED_DATA_DIR / 'val.csv')")
    print("test_df = pd.read_csv(PROCESSED_DATA_DIR / 'test.csv')")
    print("```")
    print("=" * 70)
