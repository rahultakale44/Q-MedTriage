"""
VALIDATOR DEBUG TEST

This script runs the validator on multiple images and prints detailed scores
to diagnose why genuine chest X-rays might be rejected.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image
import numpy as np


def print_validation_details(image_path: str, image: Image.Image, validator: ChestXRayValidator):
    """Print detailed validation scores for an image."""
    result = validator.validate(image)
    
    print("=" * 80)
    print(f"IMAGE: {image_path}")
    print("=" * 80)
    print(f"Image dimensions: {image.size}")
    print(f"Image mode: {image.mode}")
    print(f"\nVALIDATION SCORES:")
    print(f"  Chest X-ray score:    {result['scores']['chest_xray']:.4f} ({result['scores']['chest_xray']:.2%})")
    print(f"  Unsupported score:    {result['scores']['unsupported']:.4f} ({result['scores']['unsupported']:.2%})")
    print(f"  Margin:               {result['scores']['margin']:.4f} ({result['scores']['margin']:.2%})")
    print(f"\nTHRESHOLDS:")
    print(f"  Validation threshold: {result['threshold']:.4f} ({result['threshold']:.2%})")
    print(f"  Margin threshold:     {result['margin_threshold']:.4f} ({result['margin_threshold']:.2%})")
    print(f"\nDECISION:")
    print(f"  Valid chest X-ray:    {result['is_valid_chest_xray']}")
    print(f"  Detected type:        {result['detected_type']}")
    print(f"  Confidence:           {result['confidence']:.4f} ({result['confidence']:.2%})")
    if result['reason']:
        print(f"  Reason:               {result['reason']}")
    
    # Check individual criteria
    print(f"\nCRITERIA ANALYSIS:")
    chest_score = result['scores']['chest_xray']
    margin = result['scores']['margin']
    threshold = result['threshold']
    margin_threshold = result['margin_threshold']
    
    print(f"  ✓/✗ Chest score >= threshold:  {chest_score:.4f} >= {threshold:.4f} = {chest_score >= threshold}")
    print(f"  ✓/✗ Margin >= margin_threshold: {margin:.4f} >= {margin_threshold:.4f} = {margin >= margin_threshold}")
    print(f"  ✓/✗ BOTH conditions met:       {chest_score >= threshold and margin >= margin_threshold}")
    
    print("=" * 80)
    print()


def create_synthetic_skull() -> Image.Image:
    """Create a synthetic skull X-ray."""
    img = Image.new('L', (512, 512), color=128)
    pixels = np.array(img)
    
    center_x, center_y = 256, 256
    for i in range(512):
        for j in range(512):
            dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if dist_from_center < 220:
                intensity = 180
            else:
                intensity = 30
            pixels[i, j] = intensity
    
    return Image.fromarray(pixels.astype('uint8'), 'L')


def create_synthetic_hand() -> Image.Image:
    """Create a synthetic hand X-ray."""
    img = Image.new('L', (512, 512), color=50)
    pixels = np.array(img)
    
    for i in range(512):
        for j in range(512):
            if (j % 100 < 20) and (i > 100):
                pixels[i, j] = 200
    
    return Image.fromarray(pixels.astype('uint8'), 'L')


def main():
    print("=" * 80)
    print("CHEST X-RAY VALIDATOR DEBUG TEST")
    print("=" * 80)
    print("\nThis test measures actual validator scores to diagnose rejection issues.\n")
    
    # Initialize validator
    validator = ChestXRayValidator()
    validator.load()
    
    print("\n")
    
    # Test 1: Real chest X-ray from dataset
    chest_xray_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
    
    if chest_xray_path.exists():
        print("TEST 1: GENUINE CHEST X-RAY FROM DATASET")
        image = Image.open(chest_xray_path)
        print_validation_details(str(chest_xray_path), image, validator)
    else:
        print(f"⊘ Real chest X-ray not found at: {chest_xray_path}\n")
    
    # Test a few more chest X-rays if available
    test_dir = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL"
    if test_dir.exists():
        chest_files = sorted(list(test_dir.glob("*.jpeg")))[:5]
        for i, chest_file in enumerate(chest_files[1:], start=2):
            print(f"TEST {i}: GENUINE CHEST X-RAY #{i}")
            image = Image.open(chest_file)
            print_validation_details(str(chest_file), image, validator)
    
    # Test 2: Synthetic skull X-ray
    print("TEST: SYNTHETIC SKULL X-RAY")
    skull_image = create_synthetic_skull()
    print_validation_details("synthetic_skull.jpg", skull_image, validator)
    
    # Test 3: Synthetic hand X-ray
    print("TEST: SYNTHETIC HAND X-RAY")
    hand_image = create_synthetic_hand()
    print_validation_details("synthetic_hand.jpg", hand_image, validator)
    
    # Summary
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nReview the scores above to understand:")
    print("1. What scores do genuine chest X-rays receive?")
    print("2. What scores do non-chest images receive?")
    print("3. Is there sufficient separation between them?")
    print("4. Are the thresholds appropriate?")
    print("5. Is the margin calculation correct?")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
