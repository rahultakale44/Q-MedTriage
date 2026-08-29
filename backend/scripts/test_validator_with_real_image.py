"""
Quick test of validator with a real chest X-ray from the dataset
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image

def main():
    print("=" * 80)
    print("VALIDATOR TEST WITH REAL CHEST X-RAY")
    print("=" * 80)
    
    # Find a real chest X-ray image from dataset
    test_image_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
    
    if not test_image_path.exists():
        print(f"\n✗ Test image not found at: {test_image_path}")
        print("\nThis test requires the Kermany chest X-ray dataset.")
        return
    
    print(f"\nTest Image: {test_image_path.name}")
    print(f"Path: {test_image_path}")
    
    # Load validator
    print("\nLoading validator...")
    validator = ChestXRayValidator()
    validator.load()
    
    # Load image
    print(f"\nLoading test image...")
    image = Image.open(test_image_path)
    print(f"Image size: {image.size}")
    print(f"Image mode: {image.mode}")
    
    # Validate
    print("\nRunning validation...")
    result = validator.validate(image)
    
    # Display results
    print("\n" + "=" * 80)
    print("VALIDATION RESULT")
    print("=" * 80)
    print(f"\nValid Chest X-ray: {result['is_valid_chest_xray']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Detected Type: {result['detected_type']}")
    
    print(f"\nScores:")
    print(f"  Chest X-ray: {result['scores']['chest_xray']:.2%}")
    print(f"  Unsupported: {result['scores']['unsupported']:.2%}")
    print(f"  Margin: {result['scores']['margin']:.2%}")
    
    print(f"\nThresholds:")
    print(f"  Validation: {result['threshold']:.2%}")
    print(f"  Margin: {result['margin_threshold']:.2%}")
    
    if result['is_valid_chest_xray']:
        print("\n✓ DECISION: ACCEPTED - Will proceed to classification")
        print("\nThis is the expected result for a real chest X-ray!")
    else:
        print(f"\n✗ DECISION: REJECTED")
        print(f"\nReason: {result['reason']}")
        print("\nWARNING: Real chest X-ray was rejected!")
        print("This may indicate threshold needs adjustment.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
