import pandas as pd
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image


class ChestXrayDataset(Dataset):
    """
    PyTorch Dataset for Q-MedTriage chest X-ray data.

    Each sample contains:
        - X-ray image
        - pneumonia label
        - patient ID
        - image path
    """

    def __init__(
        self,
        csv_file,
        image_root="data/raw",
        transform=None
    ):
        self.csv_file = Path(csv_file)
        self.image_root = Path(image_root)
        self.transform = transform

        self.data = pd.read_csv(self.csv_file)

        required_columns = [
            "Path",
            "Pneumonia_Label",
            "Patient_ID",
            "Study_ID"
        ]

        for column in required_columns:
            if column not in self.data.columns:
                raise ValueError(
                    f"Required column '{column}' not found "
                    f"in {self.csv_file}"
                )

        self.data = self.data.reset_index(drop=True)

        print(f"Loaded dataset: {self.csv_file}")
        print(f"Samples: {len(self.data)}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):

        row = self.data.iloc[index]

        # --------------------------------------------------
        # IMAGE PATH
        # --------------------------------------------------

        relative_path = Path(str(row["Path"]))

        image_path = self.image_root / relative_path

        # --------------------------------------------------
        # CHECK IMAGE
        # --------------------------------------------------

        if not image_path.exists():
            raise FileNotFoundError(
                f"\nImage not found:\n"
                f"{image_path}\n\n"
                f"CSV path:\n"
                f"{row['Path']}"
            )

        # --------------------------------------------------
        # LOAD IMAGE
        # --------------------------------------------------

        image = Image.open(image_path).convert("RGB")

        # --------------------------------------------------
        # TRANSFORM
        # --------------------------------------------------

        if self.transform is not None:
            image = self.transform(image)

        # --------------------------------------------------
        # LABEL
        # --------------------------------------------------

        label = int(row["Pneumonia_Label"])

        if label not in [0, 1]:
            raise ValueError(
                f"Unexpected pneumonia label: {label}"
            )

        label = torch.tensor(
            label,
            dtype=torch.long
        )

        # --------------------------------------------------
        # PATIENT / STUDY
        # --------------------------------------------------

        patient_id = str(row["Patient_ID"])
        study_id = str(row["Study_ID"])

        # --------------------------------------------------
        # RETURN SAMPLE
        # --------------------------------------------------

        return {
            "image": image,
            "label": label,
            "patient_id": patient_id,
            "study_id": study_id,
            "image_path": str(image_path)
        }


def create_dataloader(
    csv_file,
    image_root="data/raw",
    transform=None,
    batch_size=16,
    shuffle=False,
    num_workers=0
):
    """
    Create a PyTorch DataLoader.
    """

    dataset = ChestXrayDataset(
        csv_file=csv_file,
        image_root=image_root,
        transform=transform
    )

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers
    )

    return loader