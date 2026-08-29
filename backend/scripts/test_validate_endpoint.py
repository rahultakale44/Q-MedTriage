"""
TEST /validate-image ENDPOINT

This test verifies the dedicated validation endpoint works correctly
and returns proper structured validation results.
"""

import sys
from pathlib import Path
import requests
from PIL import Image
import io
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_URL = "http://localhost:8000"


def create_skull_xray() -> bytes:
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
    
    img = Image.fromarray(pixels.astype('uint8'), 'L')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def test_validate_endpoint():
    """Test the /validate-image endpoint."""
    print("=" * 80)
    print("TEST /validate-image ENDPOINT")
    print("=" * 80)
    print()
    
    # Check health
    print("Checking API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        health = response.json()
        print(f"✓ API Status: {health['api']}")
        print(f"✓ Validator: {health.get('chest_xray_validator', 'unknown')}")
        
        if health.get('chest_xray_validator') != 'ready':
            print("\n✗ CRITICAL: Chest X-ray validator not ready!")
            return False
            
    except Exception as e:
        print(f"\n✗ Error connecting to API: {e}")
        print("  Make sure the backend is running:")
        print("  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    test_results = []
    
    # ==========================================
    # TEST 1: Valid chest X-ray
    # ==========================================
    print("\n" + "=" * 80)
    print("TEST 1: VALID CHEST X-RAY")
    print("=" * 80)
    
    chest_xray_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
    
    if chest_xray_path.exists():
        with open(chest_xray_path, "rb") as f:
            chest_bytes = f.read()
        
        files = {"file": ("chest_xray.jpg", chest_bytes, "image/jpeg")}
        
        try:
            response = requests.post(f"{API_URL}/validate-image", files=files, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Response: {data}")
            
            if response.status_code == 200:
                if data.get("valid") is True:
                    print("✓ PASS: Chest X-ray validated successfully")
                    print(f"  Detected type: {data.get('detected_type')}")
                    print(f"  Confidence: {data.get('confidence', 0):.2%}")
                    print(f"  Message: {data.get('message')}")
                    if "scores" in data:
                        print(f"  Chest score: {data['scores'].get('chest_xray', 0):.2%}")
                        print(f"  Margin: {data['scores'].get('margin', 0):.2%}")
                    test_results.append(("Valid chest X-ray", True))
                else:
                    print("✗ FAIL: Chest X-ray was rejected")
                    print(f"  Reason: {data.get('reason')}")
                    print(f"  Confidence: {data.get('confidence', 0):.2%}")
                    test_results.append(("Valid chest X-ray", False))
            else:
                print(f"✗ FAIL: Unexpected status code: {response.status_code}")
                test_results.append(("Valid chest X-ray", False))
                
        except Exception as e:
            print(f"✗ Error: {e}")
            test_results.append(("Valid chest X-ray", False))
    else:
        print("⊘ SKIPPED: Chest X-ray not found")
        test_results.append(("Valid chest X-ray", None))
    
    # ==========================================
    # TEST 2: Invalid skull X-ray
    # ==========================================
    print("\n" + "=" * 80)
    print("TEST 2: INVALID SKULL X-RAY")
    print("=" * 80)
    
    skull_bytes = create_skull_xray()
    files = {"file": ("skull.jpg", skull_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/validate-image", files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        
        if response.status_code == 200:
            if data.get("valid") is False:
                print("✓ PASS: Skull X-ray correctly rejected")
                print(f"  Detected type: {data.get('detected_type')}")
                print(f"  Confidence: {data.get('confidence', 0):.2%}")
                print(f"  Reason: {data.get('reason')}")
                test_results.append(("Invalid skull X-ray", True))
            else:
                print("✗ FAIL: Skull X-ray was incorrectly validated")
                test_results.append(("Invalid skull X-ray", False))
        else:
            print(f"✗ FAIL: Unexpected status code: {response.status_code}")
            test_results.append(("Invalid skull X-ray", False))
            
    except Exception as e:
        print(f"✗ Error: {e}")
        test_results.append(("Invalid skull X-ray", False))
    
    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    
    passed = sum(1 for _, result in test_results if result is True)
    failed = sum(1 for _, result in test_results if result is False)
    skipped = sum(1 for _, result in test_results if result is None)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASS" if result is True else ("✗ FAIL" if result is False else "⊘ SKIP")
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print()
        print("=" * 80)
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        return True
    else:
        print()
        print("=" * 80)
        print("✗ SOME TESTS FAILED")
        print("=" * 80)
        return False


if __name__ == "__main__":
    try:
        success = test_validate_endpoint()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
