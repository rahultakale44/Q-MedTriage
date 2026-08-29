"""
COMPREHENSIVE VALIDATOR DEBUG TEST

This script measures actual CLIP scores for different image types to diagnose
why genuine chest X-rays are being rejected.

Run from project root:
    python backend/scripts/debug_validator_scores.py
"""

import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from src.inference.chest_xray_validator import ChestXRayValidator
from PIL import Image


def print_detailed_scores(name: str, result: dict):
    """Print detailed validation scores with visual bars."""
    print("\n" + "=" * 80)
    print(f"{name}")
    print("=" * 80)
    
    print(f"\nImage Mode: {result.get('image_mode', 'N/A')}")
    print(f"Image Size: {result.get('image_size', 'N/A')}")
    
    print(f"\nVALIDATION DECISION:")
    print(f"  Valid: {result['is_valid_chest_xray']}")
    print(f"  Detected Type: {result['detected_type']}")
    print(f"  Decision Confidence: {result['confidence']:.4f} ({result['confidence']:.2%})")
    
    scores = result['scores']
    chest_score = scores['chest_xray']
    unsupported_score = scores['unsupported']
    margin = scores['margin']
    
    print(f"\nSCORES:")
    print(f"  Chest X-ray:  {chest_score:.4f} ({chest_score:.2%})  {'█' * int(chest_score * 50)}")
    print(f"  Unsupported:  {unsupported_score:.4f} ({unsupported_score:.2%})  {'█' * int(unsupported_score * 50)}")
    print(f"  Margin:       {margin:.4f} ({margin:+.2%})  {'█' * int(abs(margin) * 50) if margin > 0 else '▓' * int(abs(margin) * 50)}")
    
    print(f"\nTHRESHOLDS:")
    print(f"  Validation:   {result['threshold']:.4f} ({result['threshold']:.2%})  {'─' * int(result['threshold'] * 50)}")
    print(f"  Margin:       {result['margin_threshold']:.4f} ({result['margin_threshold']:.2%})  {'─' * int(result['margin_threshold'] * 50)}")
    
    print(f"\nCONDITIONS:")
    chest_meets = chest_score >= result['threshold']
    margin_meets = margin >= result['margin_threshold']
    print(f"  Chest score >= threshold:  {chest_meets}  {'✓' if chest_meets else '✗'}")
    print(f"  Margin >= margin threshold: {margin_meets}  {'✓' if margin_meets else '✗'}")
    print(f"  BOTH conditions met:        {chest_meets and margin_meets}  {'✓' if chest_meets and margin_meets else '✗'}")
    
    if not result['is_valid_chest_xray']:
        print(f"\nREJECTION REASON:")
        print(f"  {result['reason']}")
    
    print("\n" + "=" * 80)


def test_real_images():
    """Test validator with real chest X-rays and create synthetic invalid images."""
    print("\n" + "=" * 90)
    print(" " * 20 + "CHEST X-RAY VALIDATOR DEBUG TEST")
    print("=" * 90)
    print()
    print("This test measures actual CLIP scores to diagnose validation issues.")
    print()
    
    # Initialize validator
    print("Initializing validator...")
    validator = ChestXRayValidator()
    validator.load()
    
    print(f"\nValidator Configuration:")
    print(f"  Model: {validator.model_name}")
    print(f"  Device: {validator.device}")
    print(f"  Validation Threshold: {validator.VALIDATION_THRESHOLD:.2%}")
    print(f"  Margin Threshold: {validator.MARGIN_THRESHOLD:.2%}")
    
    results = []
    
    # ============================================================================
    # TEST 1: GENUINE CHEST X-RAYS FROM DATASET
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("TEST GROUP 1: GENUINE CHEST X-RAYS FROM DATASET")
    print("=" * 90)
    
    # Test multiple chest X-rays
    chest_xray_paths = [
        PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg",
        PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0003-0001.jpeg",
        PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "PNEUMONIA" / "person1_bacteria_1.jpeg",
        PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "PNEUMONIA" / "person1_virus_6.jpeg",
    ]
    
    for i, path in enumerate(chest_xray_paths, 1):
        if path.exists():
            print(f"\n{'─' * 90}")
            print(f"CHEST X-RAY #{i}: {path.name}")
            print(f"{'─' * 90}")
            
            image = Image.open(path)
            result = validator.validate(image)
            result['image_mode'] = image.mode
            result['image_size'] = image.size
            
            print_detailed_scores(f"CHEST X-RAY #{i}: {path.name}", result)
            
            results.append({
                'name': f"Chest XR #{i}",
                'type': 'genuine_chest',
                'valid': result['is_valid_chest_xray'],
                'chest_score': result['scores']['chest_xray'],
                'unsupported_score': result['scores']['unsupported'],
                'margin': result['scores']['margin']
            })
        else:
            print(f"\n✗ Chest X-ray not found: {path}")
    
    # ============================================================================
    # TEST 2: SYNTHETIC SKULL X-RAY
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("TEST GROUP 2: SYNTHETIC SKULL X-RAY (SHOULD BE REJECTED)")
    print("=" * 90)
    
    # Create synthetic skull X-ray
    print("\nCreating synthetic skull X-ray...")
    img = Image.new('L', (512, 512), color=128)
    pixels = np.array(img)
    center_x, center_y = 256, 256
    for i in range(512):
        for j in range(512):
            dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if dist_from_center < 220:
                intensity = 180  # Bright skull
            else:
                intensity = 30  # Dark background
            pixels[i, j] = intensity
    skull_image = Image.fromarray(pixels.astype('uint8'), 'L')
    
    result = validator.validate(skull_image)
    result['image_mode'] = skull_image.mode
    result['image_size'] = skull_image.size
    
    print_detailed_scores("SYNTHETIC SKULL X-RAY", result)
    
    results.append({
        'name': 'Skull XR',
        'type': 'skull',
        'valid': result['is_valid_chest_xray'],
        'chest_score': result['scores']['chest_xray'],
        'unsupported_score': result['scores']['unsupported'],
        'margin': result['scores']['margin']
    })
    
    # ============================================================================
    # TEST 3: SYNTHETIC HAND X-RAY
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("TEST GROUP 3: SYNTHETIC HAND X-RAY (SHOULD BE REJECTED)")
    print("=" * 90)
    
    # Create synthetic hand X-ray
    print("\nCreating synthetic hand X-ray...")
    img = Image.new('L', (512, 512), color=50)
    pixels = np.array(img)
    for i in range(512):
        for j in range(512):
            if (j % 100 < 20) and (i > 100):
                pixels[i, j] = 200  # Bright bones
    hand_image = Image.fromarray(pixels.astype('uint8'), 'L')
    
    result = validator.validate(hand_image)
    result['image_mode'] = hand_image.mode
    result['image_size'] = hand_image.size
    
    print_detailed_scores("SYNTHETIC HAND X-RAY", result)
    
    results.append({
        'name': 'Hand XR',
        'type': 'hand',
        'valid': result['is_valid_chest_xray'],
        'chest_score': result['scores']['chest_xray'],
        'unsupported_score': result['scores']['unsupported'],
        'margin': result['scores']['margin']
    })
    
    # ============================================================================
    # TEST 4: RANDOM PHOTOGRAPH
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("TEST GROUP 4: RANDOM PHOTOGRAPH (SHOULD BE REJECTED)")
    print("=" * 90)
    
    # Create random photograph
    print("\nCreating random photograph...")
    pixels = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    photo_image = Image.fromarray(pixels, 'RGB')
    
    result = validator.validate(photo_image)
    result['image_mode'] = photo_image.mode
    result['image_size'] = photo_image.size
    
    print_detailed_scores("RANDOM PHOTOGRAPH", result)
    
    results.append({
        'name': 'Photograph',
        'type': 'photograph',
        'valid': result['is_valid_chest_xray'],
        'chest_score': result['scores']['chest_xray'],
        'unsupported_score': result['scores']['unsupported'],
        'margin': result['scores']['margin']
    })
    
    # ============================================================================
    # COMPARATIVE ANALYSIS
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("COMPARATIVE ANALYSIS")
    print("=" * 90)
    
    # Group by type
    genuine_chest = [r for r in results if r['type'] == 'genuine_chest']
    invalid_images = [r for r in results if r['type'] != 'genuine_chest']
    
    print("\n" + "-" * 90)
    print("GENUINE CHEST X-RAYS:")
    print("-" * 90)
    print(f"{'Name':<20} {'Valid':<8} {'Chest Score':<15} {'Unsup Score':<15} {'Margin':<10}")
    print("-" * 90)
    for r in genuine_chest:
        print(f"{r['name']:<20} {str(r['valid']):<8} {r['chest_score']:.4f} ({r['chest_score']:.1%})  "
              f"{r['unsupported_score']:.4f} ({r['unsupported_score']:.1%})  {r['margin']:+.4f}")
    
    if genuine_chest:
        avg_chest = np.mean([r['chest_score'] for r in genuine_chest])
        avg_unsup = np.mean([r['unsupported_score'] for r in genuine_chest])
        avg_margin = np.mean([r['margin'] for r in genuine_chest])
        print("-" * 90)
        print(f"{'AVERAGE':<20} {'':<8} {avg_chest:.4f} ({avg_chest:.1%})  "
              f"{avg_unsup:.4f} ({avg_unsup:.1%})  {avg_margin:+.4f}")
    
    print("\n" + "-" * 90)
    print("INVALID/NON-CHEST IMAGES:")
    print("-" * 90)
    print(f"{'Name':<20} {'Valid':<8} {'Chest Score':<15} {'Unsup Score':<15} {'Margin':<10}")
    print("-" * 90)
    for r in invalid_images:
        print(f"{r['name']:<20} {str(r['valid']):<8} {r['chest_score']:.4f} ({r['chest_score']:.1%})  "
              f"{r['unsupported_score']:.4f} ({r['unsupported_score']:.1%})  {r['margin']:+.4f}")
    
    if invalid_images:
        avg_chest = np.mean([r['chest_score'] for r in invalid_images])
        avg_unsup = np.mean([r['unsupported_score'] for r in invalid_images])
        avg_margin = np.mean([r['margin'] for r in invalid_images])
        print("-" * 90)
        print(f"{'AVERAGE':<20} {'':<8} {avg_chest:.4f} ({avg_chest:.1%})  "
              f"{avg_unsup:.4f} ({avg_unsup:.1%})  {avg_margin:+.4f}")
    
    # ============================================================================
    # DIAGNOSIS
    # ============================================================================
    print("\n\n" + "=" * 90)
    print("DIAGNOSIS")
    print("=" * 90)
    
    genuine_rejected = [r for r in genuine_chest if not r['valid']]
    invalid_accepted = [r for r in invalid_images if r['valid']]
    
    print(f"\nCurrent Thresholds:")
    print(f"  Validation Threshold: {validator.VALIDATION_THRESHOLD:.4f} ({validator.VALIDATION_THRESHOLD:.2%})")
    print(f"  Margin Threshold:     {validator.MARGIN_THRESHOLD:.4f} ({validator.MARGIN_THRESHOLD:.2%})")
    
    print(f"\nResults:")
    print(f"  Genuine chest X-rays tested:   {len(genuine_chest)}")
    print(f"  Genuine chest X-rays ACCEPTED: {len([r for r in genuine_chest if r['valid']])}  {'✓' if len(genuine_rejected) == 0 else '✗'}")
    print(f"  Genuine chest X-rays REJECTED: {len(genuine_rejected)}  {'✓' if len(genuine_rejected) == 0 else '✗ PROBLEM!'}")
    
    print(f"\n  Invalid images tested:         {len(invalid_images)}")
    print(f"  Invalid images REJECTED:       {len([r for r in invalid_images if not r['valid']])}  {'✓' if len(invalid_accepted) == 0 else '✗'}")
    print(f"  Invalid images ACCEPTED:       {len(invalid_accepted)}  {'✓' if len(invalid_accepted) == 0 else '✗ PROBLEM!'}")
    
    if genuine_rejected:
        print(f"\n" + "!" * 90)
        print("CRITICAL ISSUE: Genuine chest X-rays are being REJECTED")
        print("!" * 90)
        print("\nRejected genuine chest X-rays:")
        for r in genuine_rejected:
            print(f"  - {r['name']}: chest_score={r['chest_score']:.4f}, margin={r['margin']:+.4f}")
        
        print(f"\nPOSSIBLE CAUSES:")
        min_chest_score = min([r['chest_score'] for r in genuine_chest])
        min_margin = min([r['margin'] for r in genuine_chest])
        
        if min_chest_score < validator.VALIDATION_THRESHOLD:
            print(f"  1. Validation threshold too high: {validator.VALIDATION_THRESHOLD:.4f}")
            print(f"     Lowest genuine chest score: {min_chest_score:.4f}")
            print(f"     Suggested: Lower to ~{min_chest_score * 0.9:.4f}")
        
        if min_margin < validator.MARGIN_THRESHOLD:
            print(f"  2. Margin threshold too high: {validator.MARGIN_THRESHOLD:.4f}")
            print(f"     Lowest genuine margin: {min_margin:.4f}")
            print(f"     Suggested: Lower to ~{max(0.05, min_margin * 0.8):.4f}")
        
        print(f"\n  3. CLIP prompts may not match dataset characteristics")
        print(f"     - Dataset is grayscale medical images")
        print(f"     - CLIP was trained on natural RGB images")
        print(f"     - May need different prompts or model")
    
    if invalid_accepted:
        print(f"\n" + "!" * 90)
        print("CRITICAL ISSUE: Invalid images are being ACCEPTED")
        print("!" * 90)
        print("\nAccepted invalid images:")
        for r in invalid_accepted:
            print(f"  - {r['name']}: chest_score={r['chest_score']:.4f}, margin={r['margin']:+.4f}")
        
        print(f"\nPOSSIBLE CAUSES:")
        print(f"  1. Thresholds too lenient")
        print(f"  2. Synthetic test images too simple")
        print(f"  3. CLIP cannot distinguish these image types")
    
    if not genuine_rejected and not invalid_accepted:
        print(f"\n" + "✓" * 90)
        print("SUCCESS: Validator is working correctly!")
        print("✓" * 90)
        print("\n  - All genuine chest X-rays accepted")
        print("  - All invalid images rejected")
        print("  - Thresholds are appropriate")
    
    print("\n" + "=" * 90)


if __name__ == "__main__":
    try:
        test_real_images()
    except Exception as e:
        print(f"\n✗ Error running debug test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
