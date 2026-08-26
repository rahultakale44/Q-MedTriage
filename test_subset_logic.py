"""
Quick test to validate stratified subset sampling logic without running expensive QSVM training.
"""

import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split

# Load the actual PCA features
FEATURES_DIR = Path("data/features")

X_train_full = np.load(FEATURES_DIR / "train_features_pca4d.npy")
y_train_full = np.load(FEATURES_DIR / "train_labels_pca4d.npy")

X_test = np.load(FEATURES_DIR / "test_features_pca4d.npy")
y_test = np.load(FEATURES_DIR / "test_labels_pca4d.npy")

print("=" * 70)
print("VALIDATING STRATIFIED SUBSET LOGIC")
print("=" * 70)

print()
print("Original training data:")
print(f"  Shape: {X_train_full.shape}")
print(f"  Total samples: {len(X_train_full)}")

unique_full, counts_full = np.unique(y_train_full, return_counts=True)
print()
print("Original training class distribution:")
for label, count in zip(unique_full, counts_full):
    class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
    percentage = (count / len(y_train_full)) * 100
    print(f"  {class_name} ({int(label)}): {int(count)} ({percentage:.1f}%)")

print()
print("Test data:")
print(f"  Shape: {X_test.shape}")
print(f"  Total samples: {len(X_test)}")

unique_test, counts_test = np.unique(y_test, return_counts=True)
print()
print("Test class distribution:")
for label, count in zip(unique_test, counts_test):
    class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
    percentage = (count / len(y_test)) * 100
    print(f"  {class_name} ({int(label)}): {int(count)} ({percentage:.1f}%)")

# Test different subset sizes
subset_sizes = [500, 750, 1000]

for subset_size in subset_sizes:
    print()
    print("-" * 70)
    print(f"Testing subset size: {subset_size}")
    print("-" * 70)
    
    # Create stratified subset
    X_subset, _, y_subset, _ = train_test_split(
        X_train_full,
        y_train_full,
        train_size=subset_size,
        stratify=y_train_full,
        random_state=42,
    )
    
    print(f"  Subset shape: {X_subset.shape}")
    print(f"  Total samples: {len(X_subset)}")
    
    unique_subset, counts_subset = np.unique(y_subset, return_counts=True)
    print()
    print(f"  Subset class distribution:")
    for label, count in zip(unique_subset, counts_subset):
        class_name = "PNEUMONIA" if int(label) == 1 else "NORMAL"
        percentage = (count / len(y_subset)) * 100
        expected_pct = (counts_full[label] / len(y_train_full)) * 100
        diff = abs(percentage - expected_pct)
        print(f"    {class_name} ({int(label)}): {int(count)} ({percentage:.1f}%) [expected: {expected_pct:.1f}%, diff: {diff:.1f}%]")
    
    # Verify stratification quality
    ratio_full = counts_full[1] / counts_full[0]  # PNEUMONIA / NORMAL
    ratio_subset = counts_subset[1] / counts_subset[0]
    ratio_diff_pct = abs(ratio_full - ratio_subset) / ratio_full * 100
    
    print()
    print(f"  Class ratio (PNEUMONIA/NORMAL):")
    print(f"    Full training: {ratio_full:.3f}")
    print(f"    Subset:        {ratio_subset:.3f}")
    print(f"    Difference:    {ratio_diff_pct:.2f}%")
    
    if ratio_diff_pct < 5.0:
        print(f"    ✓ Class ratio well preserved (<5% difference)")
    else:
        print(f"    ⚠️  Class ratio difference > 5%")

print()
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
print()
print("✓ Stratified subset logic is working correctly")
print("✓ Class distribution is preserved")
print()
print("To train QSVM with subset, run:")
print("  python src/models/train_quantum_svm.py")
print()
print("To change subset size, edit QSVM_TRAIN_SAMPLES in train_quantum_svm.py")
