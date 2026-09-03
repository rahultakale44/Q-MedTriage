"""
Chest X-ray Validation Gate

This module implements STRICT input validation to ensure only valid chest radiographs
are accepted for classification. This is a critical safety feature.

Validation Approach:
- Uses CLIP (vision-language model) for zero-shot image classification
- Compares uploaded image against multiple medical image categories
- Conservative threshold: rejects uncertain images
- Principle: "When uncertain, do not classify"

Safety Philosophy:
- False acceptance of unsupported image = DANGEROUS
- False rejection of uncertain image = SAFE
- Only confident chest X-ray detections proceed to classification pipeline
"""

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import Dict, Any
import numpy as np
from pathlib import Path


class ChestXRayValidator:
    """
    Validates that uploaded images are actual chest radiographs before
    allowing them to proceed to the NORMAL vs PNEUMONIA classification pipeline.
    """
    
    # Categories for zero-shot classification
    CATEGORIES = {
        "chest_xray": [
            "a frontal chest x-ray radiograph",
            "a chest radiograph showing lungs",
            "a chest x-ray medical image",
            "a posteroanterior chest radiograph",
            "a thorax x-ray showing ribcage and lungs",
            "a grayscale chest radiograph",
            "an anteroposterior chest x-ray",
            "a medical chest radiograph with visible lung fields"
        ],
        "unsupported": [
            "a skull x-ray",
            "a brain scan",
            "a hand x-ray",
            "a dental x-ray",
            "a spine x-ray",
            "a leg or arm x-ray",
            "a CT scan",
            "an MRI scan",
            "an ultrasound image",
            "a photograph",
            "a regular picture",
            "a non-medical image"
        ]
    }
    
    # Conservative threshold: require high confidence for chest X-ray
    # If confidence < threshold, reject the image
    # ADJUSTED: Lowered from 40% → 25% → 20% to accept more valid grayscale chest X-rays
    # CLIP assigns lower absolute confidence to grayscale medical images
    VALIDATION_THRESHOLD = 0.20  # 20% confidence minimum
    
    # Minimum margin between chest_xray and unsupported categories
    # The chest_xray score must be at least this much higher
    # This is the PRIMARY safety mechanism - requires chest_xray score to be
    # significantly higher than any unsupported category
    # ADJUSTED: Lowered from 20% → 10% → 8% for better acceptance of valid X-rays
    MARGIN_THRESHOLD = 0.08  # 8% margin (chest_xray must be 8% higher)
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """
        Initialize the chest X-ray validator.
        
        Args:
            model_name: CLIP model to use for validation
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        self.is_ready = False
        
    def load(self):
        """Load CLIP model and processor."""
        try:
            print("\n" + "=" * 70)
            print("Initializing Chest X-ray Validator")
            print("=" * 70)
            print(f"Model: {self.model_name}")
            print(f"Device: {self.device}")
            print(f"Validation Threshold: {self.VALIDATION_THRESHOLD}")
            print(f"Margin Threshold: {self.MARGIN_THRESHOLD}")
            
            # Load CLIP model
            self.model = CLIPModel.from_pretrained(self.model_name)
            self.processor = CLIPProcessor.from_pretrained(self.model_name)
            
            self.model.to(self.device)
            self.model.eval()
            
            self.is_ready = True
            print("✓ Chest X-ray Validator ready")
            print("=" * 70)
            
        except Exception as e:
            print(f"ERROR: Failed to load chest X-ray validator: {e}")
            self.is_ready = False
            raise
    
    def validate(self, image: Image.Image) -> Dict[str, Any]:
        """
        Validate that the image is a chest radiograph.
        
        Args:
            image: PIL Image to validate
            
        Returns:
            Dict containing:
                - is_valid_chest_xray: bool
                - confidence: float (confidence in chest_xray category)
                - detected_type: str ("chest_xray" or "unsupported")
                - scores: dict with detailed scores
                - reason: str (explanation if rejected)
        """
        if not self.is_ready:
            raise RuntimeError("Validator not initialized. Call load() first.")
        
        try:
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Prepare all text prompts
            all_prompts = []
            prompt_labels = []
            
            for category, prompts in self.CATEGORIES.items():
                for prompt in prompts:
                    all_prompts.append(prompt)
                    prompt_labels.append(category)
            
            # Process image and text
            inputs = self.processor(
                text=all_prompts,
                images=image,
                return_tensors="pt",
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
            
            # Convert to numpy
            probs = probs.cpu().numpy()[0]
            
            # Aggregate scores by category
            category_scores = {}
            for i, (prob, label) in enumerate(zip(probs, prompt_labels)):
                if label not in category_scores:
                    category_scores[label] = []
                category_scores[label].append(float(prob))
            
            # Use maximum score per category (most confident detection)
            aggregated_scores = {
                category: max(scores)
                for category, scores in category_scores.items()
            }
            
            # Get chest_xray and unsupported scores
            chest_xray_score = aggregated_scores.get("chest_xray", 0.0)
            unsupported_score = aggregated_scores.get("unsupported", 0.0)
            
            # Calculate margin
            margin = chest_xray_score - unsupported_score
            
            # Decision logic (CONSERVATIVE)
            is_valid = False
            detected_type = "unsupported"
            reason = None
            
            if chest_xray_score >= self.VALIDATION_THRESHOLD:
                # Chest X-ray score is high enough
                if margin >= self.MARGIN_THRESHOLD:
                    # And significantly higher than unsupported categories
                    is_valid = True
                    detected_type = "chest_xray"
                else:
                    # But margin is too small (ambiguous)
                    reason = f"Insufficient confidence margin ({margin:.2%}). Image may not be a clear chest radiograph."
            else:
                # Chest X-ray score too low
                if unsupported_score > chest_xray_score:
                    reason = f"Image appears to be {self._get_likely_type(probs, all_prompts)}, not a chest radiograph."
                else:
                    reason = f"Low chest X-ray confidence ({chest_xray_score:.2%}). Unable to confirm this is a chest radiograph."
            
            return {
                "is_valid_chest_xray": is_valid,
                "confidence": chest_xray_score,
                "detected_type": detected_type,
                "scores": {
                    "chest_xray": chest_xray_score,
                    "unsupported": unsupported_score,
                    "margin": margin
                },
                "reason": reason,
                "threshold": self.VALIDATION_THRESHOLD,
                "margin_threshold": self.MARGIN_THRESHOLD
            }
            
        except Exception as e:
            # On any error, reject the image (fail-safe)
            return {
                "is_valid_chest_xray": False,
                "confidence": 0.0,
                "detected_type": "error",
                "scores": {},
                "reason": f"Validation error: {str(e)}",
                "threshold": self.VALIDATION_THRESHOLD,
                "margin_threshold": self.MARGIN_THRESHOLD
            }
    
    def _get_likely_type(self, probs: np.ndarray, prompts: list) -> str:
        """Get the most likely image type from unsupported categories."""
        # Find highest probability unsupported prompt
        max_idx = np.argmax(probs)
        likely_prompt = prompts[max_idx]
        
        # Extract type from prompt
        if "skull" in likely_prompt:
            return "a skull X-ray"
        elif "brain" in likely_prompt:
            return "a brain scan"
        elif "hand" in likely_prompt:
            return "a hand X-ray"
        elif "dental" in likely_prompt:
            return "a dental X-ray"
        elif "spine" in likely_prompt:
            return "a spine X-ray"
        elif "leg" in likely_prompt or "arm" in likely_prompt:
            return "a limb X-ray"
        elif "CT" in likely_prompt:
            return "a CT scan"
        elif "MRI" in likely_prompt:
            return "an MRI scan"
        elif "ultrasound" in likely_prompt:
            return "an ultrasound image"
        elif "photograph" in likely_prompt or "picture" in likely_prompt:
            return "a regular photograph"
        else:
            return "a non-chest-radiograph image"


# Global validator instance (loaded once at startup)
_validator_instance = None


def get_validator() -> ChestXRayValidator:
    """Get or create the global validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = ChestXRayValidator()
        _validator_instance.load()
    return _validator_instance
