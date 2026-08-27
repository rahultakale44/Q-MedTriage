"""
Kermany Chest X-Ray Dataset Handler for Q-MedTriage

This module handles the Kermany et al. Chest X-Ray dataset for
NORMAL vs PNEUMONIA classification.

Reference:
    Kermany, Daniel; Zhang, Kang; Goldbaum, Michael (2018),
    "Labeled Optical Coherence Tomography (OCT) and Chest X-Ray Images
    for Classification", Mendeley Data, v2

Dataset Structure (Standard Kermany format):
    data/archive (1)/chest_xray/
        ├── train/
        │   ├── NORMAL/
        │   │   ├── image_001.jpeg
        │   │   └── ...
        │   └── PNEUMONIA/
        │       ├── image_001.jpeg
        │       └── ...
        ├── test/
        │   ├── NORMAL/
        │   └── PNEUMONIA/
        └── val/
            ├── NORMAL/
            └── PNEUMONIA/

Classes:
    - NORMAL (label 0)
    - PNEUMONIA (label 1)
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
from collections import Counter


# Centralized label mapping
CLASS_LABELS = {
    "NORMAL": 0,
    "PNEUMONIA": 1,
}


class KermanyDataset:
    """Handler for Kermany Chest X-Ray dataset"""

    def __init__(self, data_root: str = "data/archive (1)/chest_xray"):
        """
        Initialize Kermany dataset handler

        Args:
            data_root: Root directory containing train/test/val folders
                      Default: "data/archive (1)/chest_xray" (actual download location)
        """
        self.data_root = Path(data_root)
        self.train_dir = self.data_root / "train"
        self.test_dir = self.data_root / "test"
        self.val_dir = self.data_root / "val"

        self.classes = ["NORMAL", "PNEUMONIA"]
        self.label_map = CLASS_LABELS

        self.stats = None

    def inspect_dataset(self) -> Dict:
        """
        Inspect the Kermany dataset structure and validate

        Returns:
            Dictionary containing dataset statistics
        """
        if not self.data_root.exists():
            return {
                "status": "not_found",
                "message": f"Dataset directory not found: {self.data_root}",
                "instructions": (
                    "Please download the Kermany Chest X-Ray dataset from Kaggle:\n"
                    "https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia\n"
                    f"Extract to: {self.data_root}"
                ),
            }

        stats = {
            "status": "found",
            "data_root": str(self.data_root),
            "classes": self.classes,
            "label_mapping": self.label_map,
            "splits": {},
        }

        # Inspect each split
        for split_name, split_dir in [
            ("train", self.train_dir),
            ("test", self.test_dir),
            ("val", self.val_dir),
        ]:
            if not split_dir.exists():
                stats["splits"][split_name] = {
                    "status": "not_found",
                    "count": 0,
                }
                continue

            split_stats = {"status": "found", "classes": {}, "total": 0}

            for class_name in self.classes:
                class_dir = split_dir / class_name
                if not class_dir.exists():
                    split_stats["classes"][class_name] = {
                        "count": 0,
                        "status": "directory_not_found",
                    }
                    continue

                # Count images
                image_files = [
                    f
                    for f in class_dir.iterdir()
                    if f.is_file()
                    and f.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp"]
                ]

                # Check for corrupted files
                sample_files = [f.name for f in image_files[:5]]

                split_stats["classes"][class_name] = {
                    "count": len(image_files),
                    "formats": list(set(f.suffix.lower() for f in image_files)),
                    "sample_files": sample_files,
                }

                split_stats["total"] += len(image_files)

            # Calculate class balance
            if split_stats["total"] > 0:
                split_stats["class_balance"] = {
                    class_name: split_stats["classes"][class_name]["count"]
                    / split_stats["total"]
                    for class_name in self.classes
                    if class_name in split_stats["classes"]
                }

            stats["splits"][split_name] = split_stats

        # Calculate total across all splits
        total_images = sum(
            split_data.get("total", 0) for split_data in stats["splits"].values()
        )
        stats["total_images"] = total_images

        self.stats = stats
        return stats

    def get_image_paths(
        self, split: str = "train", class_name: Optional[str] = None
    ) -> List[Path]:
        """
        Get all image paths for a specific split and optionally a specific class

        Args:
            split: 'train', 'test', or 'val'
            class_name: Optional class filter ('NORMAL' or 'PNEUMONIA')

        Returns:
            List of image file paths
        """
        split_dir = {"train": self.train_dir, "test": self.test_dir, "val": self.val_dir}.get(
            split
        )

        if not split_dir or not split_dir.exists():
            return []

        image_paths = []

        classes_to_scan = [class_name] if class_name else self.classes

        for cls in classes_to_scan:
            class_dir = split_dir / cls
            if not class_dir.exists():
                continue

            for img_path in class_dir.iterdir():
                if img_path.is_file() and img_path.suffix.lower() in [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".bmp",
                ]:
                    image_paths.append(img_path)

        return image_paths

    def create_dataframe(self, split: str = "train") -> pd.DataFrame:
        """
        Create a pandas DataFrame with image paths and labels

        Args:
            split: 'train', 'test', or 'val'

        Returns:
            DataFrame with columns: image_path, label, class_name
        """
        data = []

        for class_name in self.classes:
            image_paths = self.get_image_paths(split=split, class_name=class_name)

            for img_path in image_paths:
                data.append(
                    {
                        "image_path": str(img_path),
                        "label": self.label_map[class_name],
                        "class_name": class_name,
                        "split": split,
                    }
                )

        df = pd.DataFrame(data)
        return df

    def create_splits_csv(
        self,
        output_dir: str = "data/processed",
        use_official_splits: bool = True,
        val_ratio: float = 0.1,
        random_seed: int = 42,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create and save train/val/test split CSVs

        Args:
            output_dir: Directory to save split CSV files
            use_official_splits: If True, use Kermany's official train/test splits
            val_ratio: Validation ratio if creating val split from train
            random_seed: Random seed for reproducibility

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        import numpy as np

        np.random.seed(random_seed)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if use_official_splits:
            # Use Kermany's official splits
            train_df = self.create_dataframe("train")
            test_df = self.create_dataframe("test")

            # Check if val split exists
            if self.val_dir.exists() and len(self.get_image_paths("val")) > 0:
                val_df = self.create_dataframe("val")
            else:
                # Create val split from train
                print(f"No validation split found. Creating from train ({val_ratio*100}%)")

                # Stratified split by class
                val_samples = []
                train_samples = []

                for class_name in self.classes:
                    class_samples = train_df[train_df["class_name"] == class_name]
                    n_val = int(len(class_samples) * val_ratio)

                    # Shuffle and split
                    class_samples = class_samples.sample(frac=1, random_state=random_seed)
                    val_samples.append(class_samples[:n_val])
                    train_samples.append(class_samples[n_val:])

                train_df = pd.concat(train_samples, ignore_index=True)
                val_df = pd.concat(val_samples, ignore_index=True)
                val_df["split"] = "val"

        else:
            # Custom split from all data
            all_data = []
            for split in ["train", "test", "val"]:
                df = self.create_dataframe(split)
                if len(df) > 0:
                    all_data.append(df)

            combined_df = pd.concat(all_data, ignore_index=True)

            # Stratified split
            train_samples, val_samples, test_samples = [], [], []

            for class_name in self.classes:
                class_samples = combined_df[combined_df["class_name"] == class_name]
                class_samples = class_samples.sample(frac=1, random_state=random_seed)

                n = len(class_samples)
                n_train = int(n * 0.7)
                n_val = int(n * 0.15)

                train_samples.append(class_samples[:n_train])
                val_samples.append(class_samples[n_train : n_train + n_val])
                test_samples.append(class_samples[n_train + n_val :])

            train_df = pd.concat(train_samples, ignore_index=True)
            val_df = pd.concat(val_samples, ignore_index=True)
            test_df = pd.concat(test_samples, ignore_index=True)

        # Save splits
        train_df.to_csv(output_path / "train.csv", index=False)
        val_df.to_csv(output_path / "val.csv", index=False)
        test_df.to_csv(output_path / "test.csv", index=False)

        print(f"\nCreated splits:")
        print(f"  Train: {len(train_df)} samples")
        print(f"    NORMAL: {len(train_df[train_df['label'] == 0])}")
        print(f"    PNEUMONIA: {len(train_df[train_df['label'] == 1])}")
        print(f"  Validation: {len(val_df)} samples")
        print(f"    NORMAL: {len(val_df[val_df['label'] == 0])}")
        print(f"    PNEUMONIA: {len(val_df[val_df['label'] == 1])}")
        print(f"  Test: {len(test_df)} samples")
        print(f"    NORMAL: {len(test_df[test_df['label'] == 0])}")
        print(f"    PNEUMONIA: {len(test_df[test_df['label'] == 1])}")

        return train_df, val_df, test_df

    def validate_images(self, split: str = "train", max_check: int = 100) -> Dict:
        """
        Validate images for corruption

        Args:
            split: Split to validate
            max_check: Maximum number of images to check per class

        Returns:
            Validation report
        """
        from PIL import Image

        report = {"corrupted": [], "valid": 0, "checked": 0}

        image_paths = self.get_image_paths(split)[:max_check]

        for img_path in image_paths:
            report["checked"] += 1
            try:
                img = Image.open(img_path)
                img.verify()  # Verify it's a valid image
                report["valid"] += 1
            except Exception as e:
                report["corrupted"].append({"path": str(img_path), "error": str(e)})

        return report

    def generate_report(self, output_path: str = "data/dataset_report.json"):
        """
        Generate detailed dataset report

        Args:
            output_path: Path to save report JSON
        """
        if self.stats is None:
            self.inspect_dataset()

        # Save report
        with open(output_path, "w") as f:
            json.dump(self.stats, f, indent=2)

        print(f"\nDataset report saved to: {output_path}")
        print(json.dumps(self.stats, indent=2))


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("Kermany Chest X-Ray Dataset Handler for Q-MedTriage")
    print("=" * 70)

    dataset = KermanyDataset()

    print("\nInspecting Kermany dataset...")
    stats = dataset.inspect_dataset()

    if stats["status"] == "not_found":
        print(f"\n❌ Dataset not found!")
        print(f"\n{stats['message']}")
        if "instructions" in stats:
            print(f"\n{stats['instructions']}")
    elif stats["total_images"] > 0:
        print(f"\n✓ Found {stats['total_images']} total images")
        print(f"\nClass mapping: {stats['label_mapping']}")

        for split_name, split_data in stats["splits"].items():
            if split_data["status"] == "found":
                print(f"\n{split_name.upper()} split:")
                for class_name in dataset.classes:
                    if class_name in split_data["classes"]:
                        count = split_data["classes"][class_name]["count"]
                        print(f"  {class_name}: {count}")

        # Generate report
        dataset.generate_report()

        # Optionally create splits
        print("\nTo create CSV splits, run:")
        print("  train_df, val_df, test_df = dataset.create_splits_csv()")
    else:
        print("\n⚠️ Dataset found but no images detected")
        print("Please verify the dataset structure matches the expected format")
