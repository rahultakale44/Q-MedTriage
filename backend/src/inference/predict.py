"""
End-to-End Inference Pipeline for Q-MedTriage

This module provides the complete inference workflow:
Image → Preprocessing → Feature Extraction → PCA → Classification → Result

Supports both Classical SVM and Quantum SVM classifiers.
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import joblib
from pathlib import Path
from typing import Union, Dict, Optional
import time

# Import QuantumSVM at module level to avoid import order issues
try:
    from src.models.quantum_svm import QuantumSVM
    QUANTUM_SVM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import QuantumSVM: {e}")
    QUANTUM_SVM_AVAILABLE = False
    QuantumSVM = None


class ChestXRayInference:
    """
    Complete inference pipeline for chest X-ray pneumonia detection
    
    Pipeline:
    1. Load and preprocess image (224x224, ImageNet normalization)
    2. Extract ResNet50 features (2048D)
    3. Apply frozen PCA transformation (2048D → 4D)
    4. Classify with trained Classical SVM
    5. Return structured prediction with confidence
    """
    
    def __init__(
        self,
        pca_model_path: str = None,
        svm_model_path: str = None,
        quantum_svm_path: str = None,
        device: str = "auto"
    ):
        """
        Initialize inference pipeline
        
        Args:
            pca_model_path: Path to trained PCA model
            svm_model_path: Path to trained Classical SVM model
            quantum_svm_path: Path to trained Quantum SVM model
            device: Device for ResNet50 ('cpu', 'cuda', or 'auto')
        """
        # Resolve paths relative to project root
        project_root = Path(__file__).resolve().parents[3]  # backend/src/inference/predict.py -> project root
        
        if pca_model_path is None:
            pca_model_path = project_root / "models" / "pca_reducer.pkl"
        if svm_model_path is None:
            svm_model_path = project_root / "models" / "classical_svm.pkl"
        if quantum_svm_path is None:
            quantum_svm_path = project_root / "models" / "quantum_svm.pkl"
        
        self.device = self._get_device(device)
        
        print("=" * 70)
        print("Q-MedTriage Inference Pipeline Initialization")
        print("=" * 70)
        
        # Load models
        self.pca_model = self._load_pca(pca_model_path)
        self.svm_model = self._load_svm(svm_model_path)
        self.resnet_model = self._load_resnet()
        
        # Try to load quantum model (optional)
        self.quantum_model = self._load_quantum_svm(quantum_svm_path)
        
        # Define preprocessing (MUST match training preprocessing exactly)
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.Grayscale(num_output_channels=3),  # Convert to 3-channel
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # Class labels
        self.class_names = ["NORMAL", "PNEUMONIA"]
        
        print("\n[OK] Inference pipeline ready")
        print(f"[OK] Device: {self.device}")
        print("=" * 70)
    
    def _get_device(self, device: str) -> torch.device:
        """Determine compute device"""
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)
    
    def _load_pca(self, path: str):
        """Load trained PCA model"""
        pca_path = Path(path)
        if not pca_path.exists():
            raise FileNotFoundError(f"PCA model not found: {pca_path}")
        
        pca_model = joblib.load(pca_path)
        print(f"[OK] PCA model loaded: {pca_path}")
        print(f"  Components: {pca_model.n_components_}")
        return pca_model
    
    def _load_svm(self, path: str):
        """Load trained SVM model"""
        svm_path = Path(path)
        if not svm_path.exists():
            raise FileNotFoundError(f"SVM model not found: {svm_path}")
        
        svm_model = joblib.load(svm_path)
        print(f"[OK] SVM model loaded: {svm_path}")
        return svm_model
    
    def _load_quantum_svm(self, path: str):
        """Load trained Quantum SVM model (optional)"""
        if not QUANTUM_SVM_AVAILABLE:
            print("WARNING: QuantumSVM class not available (import failed)")
            print("  Quantum classifier will not be available")
            return None
        
        quantum_path = Path(path)
        if not quantum_path.exists():
            print(f"WARNING: Quantum SVM not found: {quantum_path}")
            print("  Quantum classifier will not be available")
            return None
        
        try:
            # Load the model using the pre-imported QuantumSVM class
            quantum_model = QuantumSVM.load(str(quantum_path))
            print(f"SUCCESS: Quantum SVM loaded: {quantum_path}")
            return quantum_model
            
        except Exception as e:
            print(f"ERROR: Failed to load Quantum SVM: {e}")
            print(f"  Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            print("  Quantum classifier will not be available")
            return None
    
    def _load_resnet(self):
        """Load ResNet50 feature extractor"""
        # Load pre-trained ResNet50
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        
        # Remove final classification layer (keep up to avgpool)
        model = nn.Sequential(*list(model.children())[:-1])
        
        model = model.to(self.device)
        model.eval()
        
        print(f"[OK] ResNet50 feature extractor loaded")
        print(f"  Output dimension: 2048")
        
        return model
    
    def preprocess_image(
        self, 
        image_input: Union[str, Path, Image.Image]
    ) -> torch.Tensor:
        """
        Preprocess image for inference
        
        Args:
            image_input: Image file path or PIL Image
        
        Returns:
            Preprocessed tensor (1, 3, 224, 224)
        """
        # Load image if path provided
        if isinstance(image_input, (str, Path)):
            image = Image.open(image_input).convert("L")  # Convert to grayscale
        else:
            image = image_input.convert("L")
        
        # Apply transforms
        tensor = self.transform(image)
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor
    
    def extract_features(self, image_tensor: torch.Tensor) -> np.ndarray:
        """
        Extract ResNet50 features
        
        Args:
            image_tensor: Preprocessed image tensor (1, 3, 224, 224)
        
        Returns:
            Feature vector (2048,)
        """
        image_tensor = image_tensor.to(self.device)
        
        with torch.no_grad():
            features = self.resnet_model(image_tensor)
        
        # Flatten from (1, 2048, 1, 1) to (2048,)
        features = features.squeeze().cpu().numpy()
        
        return features
    
    def apply_pca(self, features: np.ndarray) -> np.ndarray:
        """
        Apply PCA transformation
        
        Args:
            features: ResNet50 features (2048,)
        
        Returns:
            PCA-reduced features (4,)
        """
        # Reshape to (1, 2048) for sklearn
        features_2d = features.reshape(1, -1)
        
        # Apply PCA
        pca_features = self.pca_model.transform(features_2d)
        
        # Return as 1D array (4,)
        return pca_features.flatten()
    
    def classify(self, pca_features: np.ndarray) -> Dict:
        """
        Classify using trained Classical SVM
        
        Args:
            pca_features: PCA-reduced features (4,)
        
        Returns:
            Classification result with probabilities
        """
        # Reshape to (1, 4) for sklearn
        features_2d = pca_features.reshape(1, -1)
        
        # Get probabilities
        probabilities = self.svm_model.predict_proba(features_2d)[0]
        
        # IMPORTANT: When using class_weight='balanced', svm.predict() uses
        # a weighted decision boundary that can differ from argmax(probabilities).
        # For medical triage, we want to predict based on highest probability,
        # not the weighted boundary. This ensures the displayed prediction
        # matches the probability bars shown to users.
        prediction = int(np.argmax(probabilities))
        
        return {
            "prediction": prediction,
            "prediction_label": self.class_names[prediction],
            "probabilities": {
                "NORMAL": float(probabilities[0]),
                "PNEUMONIA": float(probabilities[1]),
            },
            "confidence": float(probabilities[prediction]),
        }
    
    def classify_quantum(self, pca_features: np.ndarray) -> Dict:
        """
        Classify using trained Quantum SVM
        
        Args:
            pca_features: PCA-reduced features (4,)
        
        Returns:
            Classification result with probabilities (if available)
        """
        if self.quantum_model is None:
            raise ValueError("Quantum SVM model not loaded")
        
        # Reshape to (1, 4) for sklearn-compatible interface
        features_2d = pca_features.reshape(1, -1)
        
        # Predict
        prediction = self.quantum_model.predict(features_2d)[0]
        prediction_label = self.class_names[prediction]
        
        result = {
            "prediction": int(prediction),
            "prediction_label": prediction_label,
        }
        
        # Add probabilities if available
        if self.quantum_model.probability:
            probabilities = self.quantum_model.predict_proba(features_2d)[0]
            result["probabilities"] = {
                "NORMAL": float(probabilities[0]),
                "PNEUMONIA": float(probabilities[1]),
            }
            result["confidence"] = float(probabilities[prediction])
        else:
            # Quantum model doesn't provide calibrated probabilities
            result["probabilities"] = None
            result["confidence"] = None
        
        return result
    
    def predict(
        self, 
        image_input: Union[str, Path, Image.Image],
        classifier: str = "classical",
        include_features: bool = False
    ) -> Dict:
        """
        Complete end-to-end prediction
        
        Args:
            image_input: Image file path or PIL Image
            classifier: "classical" or "quantum"
            include_features: Whether to include intermediate features in response
        
        Returns:
            Prediction result dictionary
        """
        start_time = time.time()
        
        # Validate classifier choice
        if classifier not in ["classical", "quantum"]:
            return {
                "success": False,
                "error": f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'",
                "error_type": "ValueError",
            }
        
        # Check if quantum model is available
        if classifier == "quantum" and self.quantum_model is None:
            return {
                "success": False,
                "error": "Quantum SVM model not loaded",
                "error_type": "ModelNotAvailableError",
            }
        
        try:
            # 1. Preprocess
            image_tensor = self.preprocess_image(image_input)
            
            # 2. Extract features
            resnet_features = self.extract_features(image_tensor)
            
            # 3. Apply PCA
            pca_features = self.apply_pca(resnet_features)
            
            # 4. Classify
            if classifier == "classical":
                classification = self.classify(pca_features)
                model_name = "Classical SVM"
                model_type = "classical"
            else:  # quantum
                classification = self.classify_quantum(pca_features)
                model_name = "Quantum SVM"
                model_type = "quantum"
            
            # Calculate inference time
            inference_time = time.time() - start_time
            
            # Build response
            result = {
                "success": True,
                "model": model_name,
                "model_type": model_type,
                "prediction": classification["prediction"],
                "prediction_label": classification["prediction_label"],
                "confidence": classification.get("confidence"),
                "probabilities": classification.get("probabilities"),
                "inference_time_ms": round(inference_time * 1000, 2),
                "disclaimer": (
                    "AI-assisted triage prediction for research purposes. "
                    "Not a medical diagnosis. Requires professional clinical evaluation."
                ),
            }
            
            # Optionally include intermediate features
            if include_features:
                result["features"] = {
                    "resnet_shape": resnet_features.shape,
                    "pca_shape": pca_features.shape,
                    "pca_values": pca_features.tolist(),
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }
    
    def predict_batch(
        self, 
        image_inputs: list,
        batch_size: int = 32
    ) -> list:
        """
        Predict on multiple images
        
        Args:
            image_inputs: List of image paths or PIL Images
            batch_size: Batch size for processing
        
        Returns:
            List of prediction results
        """
        results = []
        
        for image_input in image_inputs:
            result = self.predict(image_input)
            results.append(result)
        
        return results


# ============================================================================
# STANDALONE USAGE
# ============================================================================

def quick_predict(image_path: str) -> Dict:
    """
    Quick prediction function for single image
    
    Args:
        image_path: Path to chest X-ray image
    
    Returns:
        Prediction result
    """
    pipeline = ChestXRayInference()
    return pipeline.predict(image_path)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Q-MedTriage Inference Pipeline - Standalone Test")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = ChestXRayInference()
    
    # Test with sample images if available
    test_normal = Path("data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg")
    test_pneumonia = Path("data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg")
    
    if test_normal.exists():
        print("\n" + "-" * 70)
        print("Testing with NORMAL X-ray:")
        print("-" * 70)
        result = pipeline.predict(test_normal, include_features=True)
        
        if result["success"]:
            print(f"[OK] Prediction: {result['prediction_label']}")
            print(f"[OK] Confidence: {result['confidence']:.2%}")
            print(f"[OK] Inference time: {result['inference_time_ms']}ms")
            print(f"[OK] Probabilities:")
            for label, prob in result['probabilities'].items():
                print(f"    {label}: {prob:.2%}")
        else:
            print(f"[X] Error: {result['error']}")
    
    if test_pneumonia.exists():
        print("\n" + "-" * 70)
        print("Testing with PNEUMONIA X-ray:")
        print("-" * 70)
        result = pipeline.predict(test_pneumonia, include_features=True)
        
        if result["success"]:
            print(f"[OK] Prediction: {result['prediction_label']}")
            print(f"[OK] Confidence: {result['confidence']:.2%}")
            print(f"[OK] Inference time: {result['inference_time_ms']}ms")
            print(f"[OK] Probabilities:")
            for label, prob in result['probabilities'].items():
                print(f"    {label}: {prob:.2%}")
        else:
            print(f"[X] Error: {result['error']}")
    
    print("\n" + "=" * 70)
    print("Inference pipeline test complete")
    print("=" * 70)
