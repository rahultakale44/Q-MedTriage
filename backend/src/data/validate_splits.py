"""
Validate Train/Validation/Test Splits

Comprehensive validation to ensure data integrity and prevent leakage.
"""

import pandas as pd
from pathlib import Path
from PIL import Image
from typing import Dict, List
from collections import Counter

from src.config import PROCESSED_DATA_DIR, CLASS_LABELS


def validate_splits() -> Dict:
    """
    Comprehensive validation of data splits
    
    Returns:
        Dictionary with validation results
    """
    print("=" * 70)
    print("DATA SPLIT VALIDATION")
    print("=" * 70)
    
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "statistics": {},
    }
    
    # Load splits
    try:
        train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
        val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
        test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")
    except FileNotFoundError as e:
        results["valid"] = False
        results["errors"].append(f"Split files not found: {e}")
        return results
    
    print(f"\n✓ Loaded splits:")
    print(f"  Train: {len(train_df)}")
    print(f"  Val: {len(val_df)}")
    print(f"  Test: {len(test_df)}")
    
    # ========================================================================
    # TEST 1: Schema Validation
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 1: Schema Validation")
    print("-" * 70)
    
    required_columns = ['image_path', 'label', 'class_name', 'split']
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        missing = set(required_columns) - set(df.columns)
        if missing:
            results["valid"] = False
            results["errors"].append(f"{name}: Missing columns {missing}")
        else:
            print(f"✓ {name}: All required columns present")
    
    # ========================================================================
    # TEST 2: Data Leakage Check
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 2: Data Leakage Check")
    print("-" * 70)
    
    train_paths = set(train_df['image_path'].values)
    val_paths = set(val_df['image_path'].values)
    test_paths = set(test_df['image_path'].values)
    
    train_val_overlap = train_paths & val_paths
    train_test_overlap = train_paths & test_paths
    val_test_overlap = val_paths & test_paths
    
    print(f"  Train ∩ Val: {len(train_val_overlap)} images")
    print(f"  Train ∩ Test: {len(train_test_overlap)} images")
    print(f"  Val ∩ Test: {len(val_test_overlap)} images")
    
    if len(train_val_overlap) > 0:
        results["valid"] = False
        results["errors"].append(f"Train/Val leakage: {len(train_val_overlap)} images")
    
    if len(train_test_overlap) > 0:
        results["valid"] = False
        results["errors"].append(f"Train/Test leakage: {len(train_test_overlap)} images")
    
    if len(val_test_overlap) > 0:
        results["valid"] = False
        results["errors"].append(f"Val/Test leakage: {len(val_test_overlap)} images")
    
    if results["valid"]:
        print("✓ No data leakage detected")
    
    # ========================================================================
    # TEST 3: Label Validation
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 3: Label Validation")
    print("-" * 70)
    
    valid_labels = set(CLASS_LABELS.values())
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        invalid_labels = set(df['label'].unique()) - valid_labels
        if invalid_labels:
            results["valid"] = False
            results["errors"].append(f"{name}: Invalid labels {invalid_labels}")
        else:
            print(f"✓ {name}: All labels valid {sorted(df['label'].unique())}")
    
    # ========================================================================
    # TEST 4: File Existence Check
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 4: File Existence Check (sampling)")
    print("-" * 70)
    
    # Sample check (full check would be expensive)
    sample_size = 50
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        sample_paths = df['image_path'].sample(min(sample_size, len(df)), random_state=42)
        missing = [p for p in sample_paths if not Path(p).exists()]
        
        if missing:
            results["warnings"].append(f"{name}: {len(missing)}/{len(sample_paths)} sampled files not found")
            print(f"⚠ {name}: {len(missing)}/{len(sample_paths)} sampled files not found")
        else:
            print(f"✓ {name}: All sampled files exist ({len(sample_paths)} checked)")
    
    # ========================================================================
    # TEST 5: Class Distribution
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 5: Class Distribution")
    print("-" * 70)
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        label_counts = Counter(df['label'])
        total = len(df)
        
        print(f"\n{name}:")
        for label in sorted(label_counts.keys()):
            count = label_counts[label]
            pct = count / total * 100
            class_name = "NORMAL" if label == 0 else "PNEUMONIA"
            print(f"  {class_name} (label={label}): {count} ({pct:.1f}%)")
        
        # Check for extreme imbalance
        if len(label_counts) < 2:
            results["warnings"].append(f"{name}: Only one class present!")
        else:
            min_count = min(label_counts.values())
            max_count = max(label_counts.values())
            imbalance_ratio = max_count / min_count
            
            if imbalance_ratio > 10:
                results["warnings"].append(
                    f"{name}: Severe class imbalance (ratio={imbalance_ratio:.1f})"
                )
            elif imbalance_ratio > 5:
                print(f"  ⚠ Moderate class imbalance (ratio={imbalance_ratio:.1f})")
    
    results["statistics"]["class_distribution"] = {
        "train": dict(Counter(train_df['label'])),
        "val": dict(Counter(val_df['label'])),
        "test": dict(Counter(test_df['label'])),
    }
    
    # ========================================================================
    # TEST 6: Image Format Consistency
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 6: Image Format Consistency (sampling)")
    print("-" * 70)
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        sample_paths = df['image_path'].sample(min(10, len(df)), random_state=42)
        formats = []
        
        for path in sample_paths:
            path_obj = Path(path)
            if path_obj.exists():
                formats.append(path_obj.suffix.lower())
        
        unique_formats = set(formats)
        print(f"  {name}: Detected formats {unique_formats}")
        
        if len(unique_formats) > 1:
            results["warnings"].append(f"{name}: Multiple image formats {unique_formats}")
    
    # ========================================================================
    # TEST 7: Duplicate Path Check
    # ========================================================================
    print("\n" + "-" * 70)
    print("TEST 7: Duplicate Path Check")
    print("-" * 70)
    
    for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
        duplicates = df['image_path'].duplicated().sum()
        if duplicates > 0:
            results["valid"] = False
            results["errors"].append(f"{name}: {duplicates} duplicate paths found")
        else:
            print(f"✓ {name}: No duplicate paths")
    
    # ========================================================================
    # FINAL REPORT
    # ========================================================================
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if results["valid"]:
        print("\n✓ ALL CRITICAL TESTS PASSED")
    else:
        print("\n❌ VALIDATION FAILED")
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  - {error}")
    
    if results["warnings"]:
        print("\nWarnings:")
        for warning in results["warnings"]:
            print(f"  - {warning}")
    
    print("\n" + "=" * 70)
    
    return results


def validate_image_integrity(df: pd.DataFrame, max_check: int = 100) -> Dict:
    """
    Validate image file integrity
    
    Args:
        df: DataFrame with image_path column
        max_check: Maximum number of images to check
        
    Returns:
        Validation results
    """
    print(f"\nValidating image integrity ({max_check} samples)...")
    
    results = {
        "checked": 0,
        "valid": 0,
        "corrupted": [],
        "missing": [],
    }
    
    sample_paths = df['image_path'].sample(min(max_check, len(df)), random_state=42)
    
    for path_str in sample_paths:
        path = Path(path_str)
        results["checked"] += 1
        
        if not path.exists():
            results["missing"].append(str(path))
            continue
        
        try:
            img = Image.open(path)
            img.verify()
            results["valid"] += 1
        except Exception as e:
            results["corrupted"].append({
                "path": str(path),
                "error": str(e)
            })
    
    print(f"  Checked: {results['checked']}")
    print(f"  Valid: {results['valid']}")
    print(f"  Missing: {len(results['missing'])}")
    print(f"  Corrupted: {len(results['corrupted'])}")
    
    return results


if __name__ == "__main__":
    # Run validation
    results = validate_splits()
    
    # Additional integrity check
    print("\n" + "=" * 70)
    print("IMAGE INTEGRITY CHECK")
    print("=" * 70)
    
    try:
        train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
        integrity_results = validate_image_integrity(train_df, max_check=50)
        
        if len(integrity_results["corrupted"]) > 0:
            print("\nCorrupted images found:")
            for item in integrity_results["corrupted"][:5]:
                print(f"  {item['path']}: {item['error']}")
    except Exception as e:
        print(f"Error during integrity check: {e}")
    
    # Exit with appropriate code
    if not results["valid"]:
        print("\n❌ Validation failed - please fix errors before training")
        exit(1)
    else:
        print("\n✓ Validation passed - splits are ready for training")
        exit(0)
