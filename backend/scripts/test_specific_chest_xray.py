"""
TEST A SPECIFIC CHEST X-RAY IMAGE

This script tests a specific chest X-ray image through the validator
to diagnose why it might be rejected.

Usage:
    python backend/scripts/test_specific_chest_xray.py <path_to_image>
    
Example:
    python backend/scripts/test_specific_chest_xray.py my_chest_xray.jpg
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image
import argparse


def test_specific_image(image_path: Path):
    """Test a specific image through the validator."""
    print("\n" + "=" * 90)
    print(f"TESTING SPECIFIC CHEST X-RAY: {image_path.name}")
    print("=" * 90)
    
    if not image_path.exists():
        print(f"\n✗ ERROR: Image not found at: {image_path}")
        print("\nUsage: python backend/scripts/test_specific_chest_xray.py <path_to_image>")
        return False
    
    # Load validator
    print("\n[1/3] Loading validator...")
    validator = ChestXRayValidator()
    validator.load()
    
    print(f"      Validation Threshold: {validator.VALIDATION_THRESHOLD:.2%}")
    print(f"      Margin Threshold: {validator.MARGIN_THRESHOLD:.2%}")
    
    # Load image
    print(f"\n[2/3] Loading test image...")
    try:
        image = Image.open(image_path)
        print(f"      Image size: {image.size}")
        print(f"      Image mode: {image.mode}")
        print(f"      Format: {image.format}")
    except Exception as e:
        print(f"\n✗ ERROR loading image: {e}")
        return False
    
    # Validate
    print(f"\n[3/3] Running validation...")
    result = validator.validate(image)
    
    # Display comprehensive results
    print("\n" + "=" * 90)
    print("VALIDATION RESULT")
    print("=" * 90)
    
    print(f"\n┌─ DECISION")
    print(f"│  Valid Chest X-ray: {result['is_valid_chest_xray']}")
    print(f"│  Detected Type: {result['detected_type']}")
    print(f"│  Confidence: {result['confidence']:.4f} ({result['confidence']:.2%})")
    print(f"└─")
    
    print(f"\n┌─ SCORES")
    print(f"│  Chest X-ray:  {result['scores']['chest_xray']:.4f} ({result['scores']['chest_xray']:.2%})")
    print(f"│                {'█' * int(result['scores']['chest_xray'] * 50)}")
    print(f"│")
    print(f"│  Unsupported:  {result['scores']['unsupported']:.4f} ({result['scores']['unsupported']:.2%})")
    print(f"│                {'█' * int(result['scores']['unsupported'] * 50)}")
    print(f"│")
    print(f"│  Margin:       {result['scores']['margin']:.4f} ({result['scores']['margin']:+.2%})")
    if result['scores']['margin'] > 0:
        print(f"│                {'█' * int(result['scores']['margin'] * 50)}")
    else:
        print(f"│                {'▓' * int(abs(result['scores']['margin']) * 50)}")
    print(f"└─")
    
    print(f"\n┌─ THRESHOLDS")
    print(f"│  Validation:   {result['threshold']:.4f} ({result['threshold']:.2%})")
    print(f"│                {'─' * int(result['threshold'] * 50)}")
    print(f"│")
    print(f"│  Margin:       {result['margin_threshold']:.4f} ({result['margin_threshold']:.2%})")
    print(f"│                {'─' * int(result['margin_threshold'] * 50)}")
    print(f"└─")
    
    print(f"\n┌─ CONDITIONS")
    chest_meets = result['scores']['chest_xray'] >= result['threshold']
    margin_meets = result['scores']['margin'] >= result['margin_threshold']
    print(f"│  Chest score >= threshold:   {chest_meets}  {'✓' if chest_meets else '✗'}")
    print(f"│  Margin >= margin threshold:  {margin_meets}  {'✓' if margin_meets else '✗'}")
    print(f"│  BOTH conditions met:         {chest_meets and margin_meets}  {'✓' if chest_meets and margin_meets else '✗'}")
    print(f"└─")
    
    if not result['is_valid_chest_xray']:
        print(f"\n┌─ REJECTION REASON")
        print(f"│  {result['reason']}")
        print(f"└─")
    
    # Final verdict
    print("\n" + "=" * 90)
    if result['is_valid_chest_xray']:
        print("✓✓✓ IMAGE ACCEPTED ✓✓✓")
        print("=" * 90)
        print("\nThis image WILL proceed to inference pipeline.")
        print("Expected API response: HTTP 200 (if pipeline loaded) or HTTP 503 (if pipeline not loaded)")
        return True
    else:
        print("✗✗✗ IMAGE REJECTED ✗✗✗")
        print("=" * 90)
        print("\nThis image will NOT proceed to inference pipeline.")
        print("Expected API response: HTTP 400 with error='unsupported_image'")
        
        # Provide diagnostic information
        print("\n" + "-" * 90)
        print("DIAGNOSTIC INFORMATION")
        print("-" * 90)
        
        if not chest_meets:
            print(f"\n⚠ Chest X-ray score too low:")
            print(f"   Current: {result['scores']['chest_xray']:.4f} ({result['scores']['chest_xray']:.2%})")
            print(f"   Required: {result['threshold']:.4f} ({result['threshold']:.2%})")
            print(f"   Gap: {result['threshold'] - result['scores']['chest_xray']:.4f}")
            
            if result['scores']['chest_xray'] > 0.35:
                print(f"\n   POSSIBLE CAUSE: Image is borderline")
                print(f"   - Image may be low quality")
                print(f"   - Image may be unusual view (lateral, oblique)")
                print(f"   - Image may have artifacts or borders")
                print(f"\n   RECOMMENDATION:")
                print(f"   - Try a different chest X-ray image")
                print(f"   - Ensure image is frontal (PA or AP) view")
                print(f"   - Remove any borders or text overlays if present")
            else:
                print(f"\n   POSSIBLE CAUSE: Image is clearly not a chest X-ray")
                print(f"   - Very low confidence indicates wrong image type")
        
        if not margin_meets:
            print(f"\n⚠ Margin too small:")
            print(f"   Current: {result['scores']['margin']:.4f} ({result['scores']['margin']:+.2%})")
            print(f"   Required: {result['margin_threshold']:.4f} ({result['margin_threshold']:.2%})")
            print(f"   Gap: {result['margin_threshold'] - result['scores']['margin']:.4f}")
            
            if result['scores']['margin'] < 0:
                print(f"\n   POSSIBLE CAUSE: Image looks more like something else")
                print(f"   - Unsupported score is HIGHER than chest X-ray score")
                print(f"   - Image may be skull, hand, or other anatomy")
            else:
                print(f"\n   POSSIBLE CAUSE: Ambiguous image")
                print(f"   - Scores are too close together")
                print(f"   - Validator is uncertain about image type")
        
        print("\n" + "-" * 90)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test a specific chest X-ray image through the validator"
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="Path to chest X-ray image file"
    )
    
    args = parser.parse_args()
    
    if not args.image:
        # If no argument provided, try to find a chest X-ray in the dataset
        default_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
        
        print("\nNo image path provided. Testing with dataset sample...")
        print(f"Using: {default_path}\n")
        
        if default_path.exists():
            success = test_specific_image(default_path)
        else:
            print("ERROR: No image provided and default dataset image not found.")
            print("\nUsage:")
            print("  python backend/scripts/test_specific_chest_xray.py <path_to_image>")
            print("\nExample:")
            print("  python backend/scripts/test_specific_chest_xray.py my_chest_xray.jpg")
            sys.exit(1)
    else:
        image_path = Path(args.image)
        success = test_specific_image(image_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
