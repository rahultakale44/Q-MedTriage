"""
JSRT Dataset Handler for Q-MedTriage

This module handles the JSRT (Japanese Society of Radiological Technology)
chest X-ray dataset for nodule detection.

Dataset Structure (Expected):
    data/raw/JSRT/
        ├── nodule/
        │   ├── image_001.png
        │   ├── image_002.png
        │   └── ...
        └── non_nodule/
            ├── image_001.png
            ├── image_002.png
            └── ...

Classes:
    - Nodule (positive)
    - Non-Nodule (negative)
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd


class JSRTDataset:
    """Handler for JSRT nodule detection dataset"""

    def __init__(self, data_root: str = "data/raw/JSRT"):
        """
        Initialize JSRT dataset handler

        Args:
            data_root: Root directory containing nodule/ and non_nodule/ folders
        """
        self.data_root = Path(data_root)
        self.nodule_dir = self.data_root / "nodule"
        self.non_nodule_dir = self.data_root / "non_nodule"

        self.stats = None

    def inspect_dataset(self) -> Dict:
        """
        Inspect the downloaded JSRT dataset structure

        Returns:
            Dictionary containing dataset statistics
        """
        if not self.data_root.exists():
            return {
                "status": "not_found",
                "message": f"Dataset directory not found: {self.data_root}",
            }

        stats = {
            "status": "found",
            "data_root": str(self.data_root),
            "classes": {},
        }

        # Check nodule directory
        if self.nodule_dir.exists():
            nodule_files = list(self.nodule_dir.glob("*"))
            nodule_images = [
                f
                for f in nodule_files
                if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".dcm"]
            ]
            stats["classes"]["nodule"] = {
                "count": len(nodule_images),
                "formats": list(set(f.suffix for f in nodule_images)),
                "sample_files": [f.name for f in nodule_images[:5]],
            }
        else:
            stats["classes"]["nodule"] = {"count": 0, "status": "directory_not_found"}

        # Check non-nodule directory
        if self.non_nodule_dir.exists():
            non_nodule_files = list(self.non_nodule_dir.glob("*"))
            non_nodule_images = [
                f
                for f in non_nodule_files
                if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".dcm"]
            ]
            stats["classes"]["non_nodule"] = {
                "count": len(non_nodule_images),
                "formats": list(set(f.suffix for f in non_nodule_images)),
                "sample_files": [f.name for f in non_nodule_images[:5]],
            }
        else:
            stats["classes"]["non_nodule"] = {
                "count": 0,
                "status": "directory_not_found",
            }

        # Calculate totals
        nodule_count = stats["classes"]["nodule"].get("count", 0)
        non_nodule_count = stats["classes"]["non_nodule"].get("count", 0)
        total = nodule_count + non_nodule_count

        stats["total_images"] = total
        stats["class_balance"] = {
            "nodule": nodule_count / total if total > 0 else 0,
            "non_nodule": non_nodule_count / total if total > 0 else 0,
        }

        self.stats = stats
        return stats

    def create_splits(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_seed: int = 42,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create train/validation/test splits

        Args:
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            random_seed: Random seed for reproducibility

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        import numpy as np

        np.random.seed(random_seed)

        # Collect all image paths
        data = []

        if self.nodule_dir.exists():
            for img_path in self.nodule_dir.glob("*"):
                if img_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".dcm"]:
                    data.append(
                        {
                            "image_path": str(img_path),
                            "label": 1,  # Nodule
                            "class_name": "nodule",
                        }
                    )

        if self.non_nodule_dir.exists():
            for img_path in self.non_nodule_dir.glob("*"):
                if img_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".dcm"]:
                    data.append(
                        {
                            "image_path": str(img_path),
                            "label": 0,  # Non-Nodule
                            "class_name": "non_nodule",
                        }
                    )

        # Create DataFrame
        df = pd.DataFrame(data)

        if len(df) == 0:
            raise ValueError("No images found in dataset directories")

        # Shuffle
        df = df.sample(frac=1, random_seed=random_seed).reset_index(drop=True)

        # Calculate split sizes
        n = len(df)
        train_size = int(n * train_ratio)
        val_size = int(n * val_ratio)

        # Split
        train_df = df[:train_size]
        val_df = df[train_size : train_size + val_size]
        test_df = df[train_size + val_size :]

        # Save splits
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        train_df.to_csv(output_dir / "train.csv", index=False)
        val_df.to_csv(output_dir / "val.csv", index=False)
        test_df.to_csv(output_dir / "test.csv", index=False)

        print(f"Created splits:")
        print(f"  Train: {len(train_df)} samples")
        print(f"  Validation: {len(val_df)} samples")
        print(f"  Test: {len(test_df)} samples")

        return train_df, val_df, test_df

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

        print(f"Dataset report saved to: {output_path}")
        print(json.dumps(self.stats, indent=2))


if __name__ == "__main__":
    # Example usage
    dataset = JSRTDataset()

    print("Inspecting JSRT dataset...")
    stats = dataset.inspect_dataset()

    if stats["status"] == "found" and stats["total_images"] > 0:
        print(f"\nFound {stats['total_images']} total images")
        print(f"  Nodule: {stats['classes']['nodule']['count']}")
        print(f"  Non-Nodule: {stats['classes']['non_nodule']['count']}")

        # Create splits
        print("\nCreating train/val/test splits...")
        train_df, val_df, test_df = dataset.create_splits()

        # Generate report
        dataset.generate_report()
    else:
        print("Dataset not ready yet. Please wait for download to complete.")
