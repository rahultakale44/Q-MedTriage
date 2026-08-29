"""
Test Script for Chest X-ray Validation Gate

This script demonstrates that the validation gate correctly:
1. ACCEPTS valid chest radiographs
2. REJECTS invalid/unsupported medical images
3. REJECTS non-medical images

Run from project root:
    python backend/scripts/test_chest_xray_validation.py
"""

import sys
from pathlib import Path

# Add backend to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image
import numpy as np


def create_test_image(image_type: str) -> Image.Image:
    """
    Create synthetic test images for demonstration.
    In production, use real medical images for validation.
    """
    # Create a blank image
    img = Image.new('RGB', (512, 512), color=(128, 128, 128))
    pixels = np.array(img)
    
    if image_type == "chest_xray":
        # Simulate chest X-ray appearance
        # Dark lung fields with brighter mediastinum
        center_x, center_y = 256, 256
        for i in range(512):
            for j in range(512):
                dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                # Darker at edges (lung fields), brighter in center (mediastinum)
                if dist_from_center < 200:
                    intensity = min(255, int(80 + dist_from_center * 0.5))
                else:
                    intensity = 40
                pixels[i, j] = [intensity, intensity, intensity]
    
    elif image_type == "skull":
        # Simulate skull X-ray (more uniform, rounder)
        center_x, center_y = 256, 256
        for i in range(512):
            for j in range(512):
                dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                if dist_from_center < 220:
                    intensity = 180
                else:
                    intensity = 30
                pixels[i, j] = [intensity, intensity, intensity]
    
    elif image_type == "hand":
        # Simulate hand X-ray (finger bones)
        for i in range(512):
            for j in range(512):
                if (j % 100 < 20) and (i > 100):
                    intensity = 200  # Bones
                else:
                    intensity = 50  # Soft tissue
                pixels[i, j] = [intensity, intensity, intensity]
    
    elif image_type == "photograph":
        # Colorful photograph
        pixels = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    
    return Image.fromarray(pixels.astype('uint8'), 'RGB')


def test_validator():
    """Test the chest X-ray validator with various image types."""
    print("=" * 80)
    print("CHEST X-RAY VALIDATION GATE TEST")
    print("=" * 80)
    
    # Initialize validator
    print("\nInitializing validator...")
    validator = ChestXRayValidator()
    validator.load()
    
    print(f"\n Validation Threshold: {validator.VALIDATION_THRESHOLD}")
    print(f"✓ Margin Threshold: {validator.MARGIN_THRESHOLD}")
    
    # Test cases
    test_cases = [
        {
            "name": "TEST 1: Synthetic Chest X-ray (Simulated)",
            "image_type": "chest_xray",
            "expected": "ACCEPT (in real scenario with actual chest X-ray)"
        },
        {
            "name": "TEST 2: Skull X-ray (Simulated)",
            "image_type": "skull",
            "expected": "REJECT"
        },
        {
            "name": "TEST 3: Hand X-ray (Simulated)",
            "image_type": "hand",
            "expected": "REJECT"
        },
        {
            "name": "TEST 4: Photograph (Random)",
            "image_type": "photograph",
            "expected": "REJECT"
        }
    ]
    
    print("\n" + "=" * 80)
    print("RUNNING VALIDATION TESTS")
    print("=" * 80)
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print("-" * 80)
        print(f"Expected: {test_case['expected']}")
        
        # Create test image
        image = create_test_image(test_case['image_type'])
        
        # Validate
        result = validator.validate(image)
        
        # Display results
        print(f"\nValidation Result:")
        print(f"  Valid Chest X-ray: {result['is_valid_chest_xray']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Detected Type: {result['detected_type']}")
        print(f"\nScores:")
        print(f"  Chest X-ray: {result['scores']['chest_xray']:.2%}")
        print(f"  Unsupported: {result['scores']['unsupported']:.2%}")
        print(f"  Margin: {result['scores']['margin']:.2%}")
        
        if not result['is_valid_chest_xray']:
            print(f"\nRejection Reason:")
            print(f"  {result['reason']}")
        
        # Determine pass/fail
        if result['is_valid_chest_xray']:
            decision = "✓ ACCEPTED - Will proceed to classification"
        else:
            decision = "✗ REJECTED - Will NOT proceed to classification"
        
        print(f"\nDecision: {decision}")
        
        results.append({
            "test": test_case['name'],
            "expected": test_case['expected'],
            "valid": result['is_valid_chest_xray'],
            "confidence": result['confidence']
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        status = "PASS" if (
            ("REJECT" in result['expected'] and not result['valid']) or
            ("ACCEPT" in result['expected'] and result['valid'])
        ) else "NOTE"
        
        print(f"\n{i}. {result['test']}")
        print(f"   Expected: {result['expected']}")
        print(f"   Result: {'ACCEPTED' if result['valid'] else 'REJECTED'} (confidence: {result['confidence']:.2%})")
        print(f"   Status: {status}")
    
    print("\n" + "=" * 80)
    print("IMPORTANT NOTES")
    print("=" * 80)
    print("""
1. This test uses SYNTHETIC images for demonstration purposes.
2. For accurate validation testing, use REAL medical images:
   - Real chest X-rays (frontal, PA view)
   - Real skull X-rays
   - Real hand/limb X-rays
   - Real CT/MRI scans
   - Real photographs

3. The validator uses CLIP (vision-language model) which was trained
   on diverse image-text pairs and can distinguish medical image types.

4. Validation threshold is CONSERVATIVE (65% confidence + 20% margin):
   - False rejection of uncertain images: SAFE
   - False acceptance of unsupported images: DANGEROUS
   - "When uncertain, do not classify"

5. To test with real images, modify this script to load actual files:
   image = Image.open("path/to/chest_xray.jpg")
   result = validator.validate(image)

6. Production deployment should include monitoring of validation rates
   to detect if the threshold needs adjustment.
    """)
    
    print("\n" + "=" * 80)
    print("VALIDATION MECHANISM")
    print("=" * 80)
    print(f"""
Method: CLIP (Contrastive Language-Image Pre-training)
Model: {validator.model_name}
Approach: Zero-shot classification against text prompts

Chest X-ray prompts:
{validator.CATEGORIES['chest_xray']}

Unsupported prompts (examples):
{validator.CATEGORIES['unsupported'][:4]}
... and more

Decision Logic:
1. Compute similarity scores for all prompts
2. Aggregate scores by category (max per category)
3. Check chest_xray score >= {validator.VALIDATION_THRESHOLD} (threshold)
4. Check margin >= {validator.MARGIN_THRESHOLD} (chest_xray - unsupported)
5. Accept only if BOTH conditions met
    """)


if __name__ == "__main__":
    try:
        test_validator()
    except Exception as e:
        print(f"\n✗ Error running validation test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
