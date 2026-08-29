"""
END-TO-END VALIDATION TEST

This test verifies that invalid images are rejected by the API BEFORE
reaching the inference pipeline, even when the pipeline is not available.

This replicates the actual frontend user flow.
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
    """Create a synthetic skull X-ray (uniform, rounder)."""
    img = Image.new('L', (512, 512), color=128)
    pixels = np.array(img)
    
    center_x, center_y = 256, 256
    for i in range(512):
        for j in range(512):
            dist_from_center = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            if dist_from_center < 220:
                intensity = 180  # Bright skull bone
            else:
                intensity = 30  # Dark background
            pixels[i, j] = intensity
    
    img = Image.fromarray(pixels.astype('uint8'), 'L')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def create_hand_xray() -> bytes:
    """Create a synthetic hand X-ray (finger bones)."""
    img = Image.new('L', (512, 512), color=50)
    pixels = np.array(img)
    
    # Vertical finger bones
    for i in range(512):
        for j in range(512):
            if (j % 100 < 20) and (i > 100):
                pixels[i, j] = 200  # Bright bones
    
    img = Image.fromarray(pixels.astype('uint8'), 'L')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def create_photograph() -> bytes:
    """Create a random colorful photograph."""
    pixels = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    img = Image.fromarray(pixels, 'RGB')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


def test_endpoint_order():
    """
    CRITICAL TEST: Verify validation runs BEFORE pipeline availability check
    
    This is the bug that allowed skull X-rays to bypass validation.
    """
    print("=" * 80)
    print("END-TO-END VALIDATION TEST")
    print("=" * 80)
    print()
    print("This test verifies that:")
    print("1. Invalid images are rejected BEFORE checking pipeline availability")
    print("2. Rejection returns proper 'unsupported_image' error")
    print("3. Valid images get 'pipeline not available' error (expected)")
    print()
    
    # Check health
    print("Checking API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        health = response.json()
        print(f"✓ API Status: {health['api']}")
        print(f"✓ Validator: {health.get('chest_xray_validator', 'unknown')}")
        print(f"✓ Pipeline: {health.get('vision_model', 'unknown')}")
        
        if health.get('chest_xray_validator') != 'ready':
            print("\n✗ CRITICAL: Chest X-ray validator not ready!")
            print("  Cannot test validation properly.")
            return False
            
    except Exception as e:
        print(f"\n✗ Error connecting to API: {e}")
        print("  Make sure the backend is running:")
        print("  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    test_results = []
    
    # ==================================================
    # TEST 1: SKULL X-RAY (must be rejected by validation)
    # ==================================================
    print("\n" + "=" * 80)
    print("TEST 1: SKULL X-RAY (Synthetic)")
    print("=" * 80)
    print("Expected: HTTP 400 with 'unsupported_image' error")
    print("NOT: HTTP 503 'Inference pipeline not available'")
    print()
    
    skull_bytes = create_skull_xray()
    files = {"file": ("skull.jpg", skull_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Check response
        if response.status_code == 400:
            if data.get("error") == "unsupported_image":
                print("✓ PASS: Skull X-ray correctly rejected by validation")
                print(f"  Error type: {data.get('error')}")
                print(f"  Message: {data.get('message')}")
                if "validation" in data:
                    print(f"  Detected as: {data['validation'].get('detected_type')}")
                    print(f"  Confidence: {data['validation'].get('confidence', 0):.2%}")
                    print(f"  Reason: {data['validation'].get('reason')}")
                test_results.append(("Skull rejection", True))
            else:
                print(f"✗ FAIL: Got 400 but wrong error type: {data.get('error')}")
                print(f"  Expected: 'unsupported_image'")
                print(f"  Got: {data}")
                test_results.append(("Skull rejection", False))
        elif response.status_code == 503:
            print("✗ FAIL: Got 503 'Inference pipeline not available'")
            print("  This means validation was NOT run!")
            print("  BUG: Pipeline check happened before validation")
            print(f"  Response: {data}")
            test_results.append(("Skull rejection", False))
        else:
            print(f"✗ FAIL: Unexpected status code: {response.status_code}")
            print(f"  Response: {data}")
            test_results.append(("Skull rejection", False))
            
    except Exception as e:
        print(f"✗ Error: {e}")
        test_results.append(("Skull rejection", False))
    
    # ==================================================
    # TEST 2: HAND X-RAY (must be rejected by validation)
    # ==================================================
    print("\n" + "=" * 80)
    print("TEST 2: HAND X-RAY (Synthetic)")
    print("=" * 80)
    print("Expected: HTTP 400 with 'unsupported_image' error")
    print()
    
    hand_bytes = create_hand_xray()
    files = {"file": ("hand.jpg", hand_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 400 and data.get("error") == "unsupported_image":
            print("✓ PASS: Hand X-ray correctly rejected by validation")
            test_results.append(("Hand rejection", True))
        elif response.status_code == 503:
            print("✗ FAIL: Got 503 instead of validation rejection")
            test_results.append(("Hand rejection", False))
        else:
            print(f"✗ FAIL: Unexpected response: {data}")
            test_results.append(("Hand rejection", False))
            
    except Exception as e:
        print(f"✗ Error: {e}")
        test_results.append(("Hand rejection", False))
    
    # ==================================================
    # TEST 3: PHOTOGRAPH (must be rejected by validation)
    # ==================================================
    print("\n" + "=" * 80)
    print("TEST 3: PHOTOGRAPH (Random)")
    print("=" * 80)
    print("Expected: HTTP 400 with 'unsupported_image' error")
    print()
    
    photo_bytes = create_photograph()
    files = {"file": ("photo.jpg", photo_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 400 and data.get("error") == "unsupported_image":
            print("✓ PASS: Photograph correctly rejected by validation")
            test_results.append(("Photo rejection", True))
        elif response.status_code == 503:
            print("✗ FAIL: Got 503 instead of validation rejection")
            test_results.append(("Photo rejection", False))
        else:
            print(f"✗ FAIL: Unexpected response: {data}")
            test_results.append(("Photo rejection", False))
            
    except Exception as e:
        print(f"✗ Error: {e}")
        test_results.append(("Photo rejection", False))
    
    # ==================================================
    # TEST 4: REAL CHEST X-RAY (if available)
    # ==================================================
    print("\n" + "=" * 80)
    print("TEST 4: REAL CHEST X-RAY (from dataset)")
    print("=" * 80)
    print("Expected: Passes validation, but gets 503 (pipeline not loaded)")
    print()
    
    chest_xray_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
    
    if chest_xray_path.exists():
        with open(chest_xray_path, "rb") as f:
            chest_bytes = f.read()
        
        files = {"file": ("chest_xray.jpg", chest_bytes, "image/jpeg")}
        
        try:
            response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            if response.status_code == 400 and data.get("error") == "unsupported_image":
                print("✗ FAIL: Real chest X-ray was rejected by validation!")
                print("  This indicates threshold is too strict.")
                print(f"  Validation confidence: {data.get('validation', {}).get('confidence', 'N/A')}")
                test_results.append(("Chest acceptance", False))
            elif response.status_code == 503:
                print("✓ PASS: Real chest X-ray passed validation")
                print("  (Got expected 503 because inference pipeline not loaded)")
                print(f"  Message: {data.get('detail')}")
                test_results.append(("Chest acceptance", True))
            elif response.status_code == 200:
                print("✓ PASS: Real chest X-ray passed validation AND inference succeeded!")
                print(f"  Prediction: {data.get('prediction_label')}")
                print(f"  Confidence: {data.get('confidence', 0):.2%}")
                test_results.append(("Chest acceptance", True))
            else:
                print(f"? Unexpected response: {response.status_code}")
                print(f"  {data}")
                test_results.append(("Chest acceptance", False))
                
        except Exception as e:
            print(f"✗ Error: {e}")
            test_results.append(("Chest acceptance", False))
    else:
        print("⊘ SKIPPED: Real chest X-ray not found in dataset")
        test_results.append(("Chest acceptance", None))
    
    # ==================================================
    # SUMMARY
    # ==================================================
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
        print()
        print("The validation safety gate is working correctly:")
        print("1. Invalid images are rejected BEFORE pipeline check")
        print("2. Proper error messages are returned")
        print("3. Valid chest X-rays pass validation")
        return True
    else:
        print()
        print("=" * 80)
        print("✗ SOME TESTS FAILED")
        print("=" * 80)
        print()
        print("The validation safety gate has issues.")
        return False


if __name__ == "__main__":
    try:
        success = test_endpoint_order()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
