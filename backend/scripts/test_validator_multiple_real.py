"""
Test validator with multiple real chest X-rays to assess threshold appropriateness
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image

def main():
    print("=" * 80)
    print("VALIDATOR TEST WITH MULTIPLE REAL CHEST X-RAYS")
    print("=" * 80)
    
    # Find test images
    test_dir = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL"
    
    if not test_dir.exists():
        print(f"\n✗ Test directory not found: {test_dir}")
        return
    
    # Get first 5 images
    image_files = sorted(list(test_dir.glob("*.jpeg")))[:5]
    
    if not image_files:
        print("\n✗ No images found in test directory")
        return
    
    print(f"\nFound {len(image_files)} test images")
    print(f"Testing with first 5 images...")
    
    # Load validator once
    print("\nLoading validator...")
    validator = ChestXRayValidator()
    validator.load()
    
    # Test each image
    results = []
    for img_path in image_files:
        print(f"\n" + "-" * 80)
        print(f"Testing: {img_path.name}")
        
        try:
            image = Image.open(img_path)
            result = validator.validate(image)
            
            print(f"  Valid: {result['is_valid_chest_xray']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Margin: {result['scores']['margin']:.2%}")
            
            results.append({
                "file": img_path.name,
                "valid": result['is_valid_chest_xray'],
                "confidence": result['confidence'],
                "margin": result['scores']['margin']
            })
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    accepted = sum(1 for r in results if r['valid'])
    rejected = len(results) - accepted
    
    print(f"\nTotal tested: {len(results)}")
    print(f"Accepted: {accepted}")
    print(f"Rejected: {rejected}")
    
    if results:
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        avg_margin = sum(r['margin'] for r in results) / len(results)
        print(f"\nAverage confidence: {avg_confidence:.2%}")
        print(f"Average margin: {avg_margin:.2%}")
    
    print("\n" + "-" * 80)
    print("ANALYSIS")
    print("-" * 80)
    
    if rejected > accepted:
        print("""
⚠ Most real chest X-rays are being REJECTED.

This indicates the validation threshold (65%) may be too conservative for
grayscale medical images. CLIP was trained primarily on color images and
may assign lower confidence to grayscale X-rays.

OPTIONS:

1. LOWER THE THRESHOLD (e.g., to 40-50%)
   - Location: backend/src/inference/chest_xray_validator.py
   - VALIDATION_THRESHOLD = 0.45  # 45% instead of 65%
   - Pro: Real chest X-rays will be accepted
   - Con: May accept some ambiguous images
   
2. USE MARGIN-ONLY DECISION
   - If chest_xray score > unsupported score by large margin (e.g., 30%)
   - Pro: Leverages relative confidence
   - Con: Less absolute certainty
   
3. ADD RGB CONVERSION PREPROCESSING
   - Convert grayscale to RGB before validation
   - May improve CLIP's performance
   
4. USE DIFFERENT VALIDATION MODEL
   - Fine-tune CLIP on medical images
   - Use specialized medical image classifier
   - Pro: Better performance on X-rays
   - Con: Additional training required

RECOMMENDATION:
Lower threshold to 0.40 (40%) and keep margin requirement at 0.20 (20%).
This provides reasonable safety while accepting real chest X-rays.
        """)
    elif accepted == len(results):
        print("""
✓ All real chest X-rays were ACCEPTED.

The validation threshold is working well for these images.
Continue testing with:
- More diverse chest X-rays
- Poor quality images
- Non-chest medical images (skull, hand, etc.)
- Non-medical images (photos, documents)
        """)
    else:
        print("""
⚠ Mixed results - some accepted, some rejected.

This suggests the threshold is at the boundary. Consider:
1. Testing with more images to assess consistency
2. Reviewing rejected images to understand characteristics
3. Adjusting threshold based on acceptable false rejection rate
        """)

if __name__ == "__main__":
    main()
