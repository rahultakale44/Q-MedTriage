"""
Test Chest X-ray Validation via API

Tests the /predict endpoint with various images to verify validation works end-to-end.

Prerequisites:
1. Backend server running: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
2. Test images (optional): real chest X-rays and other medical images

Run from project root:
    python backend/scripts/test_validation_api.py
"""

import requests
from PIL import Image
import io
import numpy as np


def create_synthetic_chest_xray() -> bytes:
    """Create a synthetic chest X-ray for testing."""
    img = Image.new('L', (512, 512), color=128)
    pixels = np.array(img)
    
    # Simulate chest X-ray appearance
    center_x, center_y = 256, 256
    for i in range(512):
        for j in range(512):
            dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if dist_from_center < 200:
                intensity = min(255, int(80 + dist_from_center * 0.5))
            else:
                intensity = 40
            pixels[i, j] = intensity
    
    img = Image.fromarray(pixels.astype('uint8'), 'L')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def create_synthetic_photograph() -> bytes:
    """Create a random photograph for testing."""
    pixels = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    img = Image.fromarray(pixels, 'RGB')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def test_api_validation():
    """Test the API validation endpoint."""
    API_URL = "http://localhost:8000"
    
    print("=" * 80)
    print("API VALIDATION TEST")
    print("=" * 80)
    
    # Check health
    print("\nChecking API health...")
    try:
        response = requests.get(f"{API_URL}/health")
        health = response.json()
        print(f"✓ API Status: {health['api']}")
        print(f"✓ Validator: {health.get('chest_xray_validator', 'unknown')}")
        print(f"✓ Vision Model: {health['vision_model']}")
        
        if health.get('chest_xray_validator') != 'ready':
            print("\n✗ WARNING: Chest X-ray validator not ready!")
            print("  The system will accept ANY image (UNSAFE)")
            return
    except Exception as e:
        print(f"\n✗ Error connecting to API: {e}")
        print("  Make sure the backend is running:")
        print("  python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
        return
    
    # Test cases
    print("\n" + "=" * 80)
    print("TEST 1: Synthetic Chest X-ray (should accept)")
    print("=" * 80)
    
    chest_xray_bytes = create_synthetic_chest_xray()
    files = {"file": ("chest_xray.jpg", chest_xray_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ ACCEPTED - Image validated as chest X-ray")
            print(f"\nValidation Info:")
            if "validation" in result:
                print(f"  Valid: {result['validation']['is_valid_chest_xray']}")
                print(f"  Confidence: {result['validation']['confidence']:.2%}")
                print(f"  Type: {result['validation']['detected_type']}")
            print(f"\nPrediction:")
            print(f"  Condition: {result.get('prediction_label', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 0):.2%}")
            print(f"  Model: {result.get('model', 'N/A')}")
        elif response.status_code == 400:
            result = response.json()
            print("✗ REJECTED")
            print(f"\nRejection Details:")
            print(f"  Error: {result.get('error', 'N/A')}")
            print(f"  Message: {result.get('message', 'N/A')}")
            if "validation" in result:
                print(f"  Reason: {result['validation'].get('reason', 'N/A')}")
                print(f"  Confidence: {result['validation'].get('confidence', 0):.2%}")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Random photograph
    print("\n" + "=" * 80)
    print("TEST 2: Random Photograph (should reject)")
    print("=" * 80)
    
    photo_bytes = create_synthetic_photograph()
    files = {"file": ("photograph.jpg", photo_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✗ WARNING: Image was ACCEPTED (should have been rejected!)")
            print(f"\nValidation Info:")
            if "validation" in result:
                print(f"  Valid: {result['validation']['is_valid_chest_xray']}")
                print(f"  Confidence: {result['validation']['confidence']:.2%}")
            print("\nThis indicates the validator may need threshold tuning.")
        elif response.status_code == 400:
            result = response.json()
            print("✓ CORRECTLY REJECTED")
            print(f"\nRejection Details:")
            print(f"  Error: {result.get('error', 'N/A')}")
            print(f"  Message: {result.get('message', 'N/A')}")
            if "validation" in result:
                print(f"\nValidation Scores:")
                if "scores" in result['validation']:
                    scores = result['validation']['scores']
                    print(f"  Chest X-ray: {scores.get('chest_xray', 0):.2%}")
                    print(f"  Unsupported: {scores.get('unsupported', 0):.2%}")
                    print(f"  Margin: {scores.get('margin', 0):.2%}")
                print(f"\nReason: {result['validation'].get('reason', 'N/A')}")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("NEXT STEPS FOR PRODUCTION TESTING")
    print("=" * 80)
    print("""
1. Test with REAL chest X-rays:
   - Upload actual frontal chest X-rays
   - Verify they are ACCEPTED
   - Check confidence scores are reasonable (>70%)

2. Test with REAL unsupported images:
   - Upload skull X-rays → should be REJECTED
   - Upload hand X-rays → should be REJECTED
   - Upload CT scans → should be REJECTED
   - Upload MRI scans → should be REJECTED
   - Upload photographs → should be REJECTED

3. Test edge cases:
   - Lateral chest X-rays (side view)
   - Poor quality/noisy X-rays
   - Rotated X-rays
   - Very dark/bright X-rays

4. Monitor validation metrics in production:
   - Acceptance rate
   - Average confidence for accepted images
   - Rejection reasons distribution
   - User feedback on false rejections

5. Adjust thresholds if needed:
   - VALIDATION_THRESHOLD (currently 0.65)
   - MARGIN_THRESHOLD (currently 0.20)
   - Location: backend/src/inference/chest_xray_validator.py

Remember: False rejection is SAFER than false acceptance!
    """)


if __name__ == "__main__":
    test_api_validation()
