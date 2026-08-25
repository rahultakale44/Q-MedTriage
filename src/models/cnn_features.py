"""
CNN Feature Extraction for Q-MedTriage

This module implements transfer learning using ResNet50 for feature extraction
from chest X-ray images.

The extracted features are used as input to both classical and quantum classifiers.
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Union, List
from tqdm import tqdm


class ResNet50FeatureExtractor:
    """
    ResNet50-based feature extractor for medical images

    Uses pre-trained ResNet50 with the final classification layer removed
    to extract 2048-dimensional feature vectors.
    """

    def __init__(self, device: str = "auto"):
        """
        Initialize feature extractor

        Args:
            device: Device to run model on ('cpu', 'cuda', or 'auto')
        """
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # Load pre-trained ResNet50
        self.model = models.resnet50(pretrained=True)

        # Remove final classification layer
        # ResNet50 outputs 2048-dim features before the FC layer
        self.model = nn.Sequential(*list(self.model.children())[:-1])

        self.model = self.model.to(self.device)
        self.model.eval()

        # Define preprocessing transforms
        self.transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.Grayscale(num_output_channels=3),  # Convert to 3-channel
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

        print(f"ResNet50 Feature Extractor initialized on {self.device}")
        print(f"Output dimension: 2048")

    def preprocess_image(self, image_path: Union[str, Path]) -> torch.Tensor:
        """
        Preprocess a single image

        Args:
            image_path: Path to image file

        Returns:
            Preprocessed tensor ready for model input
        """
        image = Image.open(image_path).convert("L")  # Convert to grayscale
        tensor = self.transform(image)
        return tensor.unsqueeze(0)  # Add batch dimension

    def extract_features(self, image_path: Union[str, Path]) -> np.ndarray:
        """
        Extract features from a single image

        Args:
            image_path: Path to image file

        Returns:
            2048-dimensional feature vector
        """
        tensor = self.preprocess_image(image_path).to(self.device)

        with torch.no_grad():
            features = self.model(tensor)

        # Flatten from (1, 2048, 1, 1) to (2048,)
        features = features.squeeze().cpu().numpy()

        return features

    def extract_batch_features(
        self, image_paths: List[Union[str, Path]], batch_size: int = 32
    ) -> np.ndarray:
        """
        Extract features from multiple images efficiently

        Args:
            image_paths: List of image file paths
            batch_size: Batch size for processing

        Returns:
            Array of shape (num_images, 2048)
        """
        all_features = []

        # Process in batches
        for i in tqdm(range(0, len(image_paths), batch_size), desc="Extracting features"):
            batch_paths = image_paths[i : i + batch_size]

            # Load and preprocess batch
            batch_tensors = []
            for path in batch_paths:
                try:
                    tensor = self.preprocess_image(path)
                    batch_tensors.append(tensor)
                except Exception as e:
                    print(f"Error processing {path}: {e}")
                    continue

            if len(batch_tensors) == 0:
                continue

            # Stack into batch
            batch = torch.cat(batch_tensors, dim=0).to(self.device)

            # Extract features
            with torch.no_grad():
                features = self.model(batch)

            # Flatten and store
            features = features.squeeze().cpu().numpy()
            if len(features.shape) == 1:  # Single image case
                features = features.reshape(1, -1)

            all_features.append(features)

        # Concatenate all batches
        all_features = np.vstack(all_features)

        return all_features

    def get_feature_dim(self) -> int:
        """Get output feature dimensionality"""
        return 2048


if __name__ == "__main__":
    # Example usage
    extractor = ResNet50FeatureExtractor()

    print(f"\nFeature dimension: {extractor.get_feature_dim()}")
    print("\nReady to extract features from Kermany Chest X-Ray dataset")
    print("Usage:")
    print("  features = extractor.extract_features('path/to/image.png')")
    print("  batch_features = extractor.extract_batch_features(image_paths)")
