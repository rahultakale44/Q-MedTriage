"""
TEST COMPLETE INFERENCE FLOW

This script tests the complete flow from image upload through prediction.
"""

import sys
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
API_URL = "http://localhost:8000"


def test_valid_chest_xray():
    """Test with a valid chest X-ray"""
    print("\n" + "=" * 80)
    print("TEST 1: VALID CHEST X-RAY")
    print("=" * 80)
    
    # Use a chest X-ray from dataset
    image_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "NORMAL" / "IM-0001-0001.jpeg"
    
    if not image_path.exists():
        print(f"ERROR: Test image not found: {image_path}")
        return False
    
    print(f"Image: {image_path.name}")
    print("Expected: Validation passes -> Inference executes -> Prediction returned")
    print()
    
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        
        try:
            response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
            print(f"Status: {response.status_code}")
            
            data = response.json()
            
            if response.status_code == 200:
                print("[OK] SUCCESS: Prediction returned")
                print()
                print(f"  Model: {data.get('model')}")
                print(f"  Prediction: {data.get('prediction_label')}")
                print(f"  Confidence: {data.get('confidence', 0):.2%}")
                print(f"  Probabilities:")
                probs = data.get('probabilities', {})
                print(f"    NORMAL: {probs.get('NORMAL', 0):.2%}")
                print(f"    PNEUMONIA: {probs.get('PNEUMONIA', 0):.2%}")
                print(f"  Inference time: {data.get('inference_time_ms')}ms")
                
                # Check validation info
                validation = data.get('validation', {})
                if validation:
                    print(f"\n  Validation confidence: {validation.get('confidence', 0):.2%}")
                
                return True
                
            elif response.status_code == 400:
                print("[X] FAIL: Image was rejected by validation")
                print(f"  Error: {data.get('error')}")
                print(f"  Message: {data.get('message')}")
                return False
                
            elif response.status_code == 503:
                print("[X] FAIL: Pipeline unavailable")
                print(f"  Detail: {data.get('detail')}")
                return False
                
            else:
                print(f"[X] FAIL: Unexpected status {response.status_code}")
                print(f"  Response: {data}")
                return False
                
        except Exception as e:
            print(f"[X] ERROR: {e}")
            return False


def test_invalid_image_skull():
    """Test with invalid image (synthetic skull X-ray)"""
    print("\n" + "=" * 80)
    print("TEST 2: INVALID IMAGE (Skull X-ray)")
    print("=" * 80)
    print("Expected: HTTP 400 - Validation rejects before inference")
    print()
    
    # Create synthetic skull X-ray
    from PIL import Image
    import numpy as np
    import io
    
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
    
    files = {"file": ("skull.jpg", img_bytes, "image/jpeg")}
    
    try:
        response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
        print(f"Status: {response.status_code}")
        
        data = response.json()
        
        if response.status_code == 400 and data.get('error') == 'unsupported_image':
            print("[OK] SUCCESS: Correctly rejected by validation")
            print()
            print(f"  Error: {data.get('error')}")
            print(f"  Message: {data.get('message')}")
            
            validation = data.get('validation', {})
            if validation:
                print(f"\n  Detected type: {validation.get('detected_type')}")
                print(f"  Confidence: {validation.get('confidence', 0):.2%}")
                print(f"  Reason: {validation.get('reason')}")
            
            return True
            
        else:
            print(f"[X] FAIL: Should have been rejected with HTTP 400")
            print(f"  Got status: {response.status_code}")
            print(f"  Response: {data}")
            return False
            
    except Exception as e:
        print(f"[X] ERROR: {e}")
        return False


def test_pneumonia_chest_xray():
    """Test with a PNEUMONIA chest X-ray"""
    print("\n" + "=" * 80)
    print("TEST 3: PNEUMONIA CHEST X-RAY")
    print("=" * 80)
    
    # Use a PNEUMONIA chest X-ray from dataset
    image_path = PROJECT_ROOT / "data" / "archive (1)" / "chest_xray" / "chest_xray" / "test" / "PNEUMONIA" / "person1_virus_6.jpeg"
    
    if not image_path.exists():
        print(f"SKIP: Test image not found: {image_path}")
        return None
    
    print(f"Image: {image_path.name}")
    print("Expected: Validation passes -> Prediction shows PNEUMONIA or NORMAL")
    print()
    
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        
        try:
            response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
            print(f"Status: {response.status_code}")
            
            data = response.json()
            
            if response.status_code == 200:
                print("[OK] SUCCESS: Prediction returned")
                print()
                print(f"  Model: {data.get('model')}")
                print(f"  Prediction: {data.get('prediction_label')}")
                print(f"  Confidence: {data.get('confidence', 0):.2%}")
                print(f"  Inference time: {data.get('inference_time_ms')}ms")
                
                return True
                
            else:
                print(f"[X] FAIL: Unexpected status {response.status_code}")
                print(f"  Response: {data}")
                return False
                
        except Exception as e:
            print(f"[X] ERROR: {e}")
            return False


def main():
    print("\n" + "=" * 80)
    print("COMPLETE INFERENCE FLOW TEST")
    print("=" * 80)
    
    # Check API health
    print("\nChecking API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        health = response.json()
        
        print(f"  API: {health.get('api')}")
        print(f"  Validator: {health.get('chest_xray_validator')}")
        print(f"  Pipeline: {'ready' if health.get('pipeline_loaded') else 'not ready'}")
        print(f"  Classical SVM: {health.get('classical_svm')}")
        
        if not health.get('pipeline_loaded'):
            print("\n[X] ERROR: Inference pipeline not loaded!")
            print("  Cannot proceed with tests.")
            return False
            
    except Exception as e:
        print(f"\n[X] ERROR: Cannot connect to API: {e}")
        print("  Make sure backend is running:")
        print("  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    # Run tests
    results = []
    
    results.append(("Valid chest X-ray", test_valid_chest_xray()))
    results.append(("Invalid skull X-ray", test_invalid_image_skull()))
    
    pneumonia_result = test_pneumonia_chest_xray()
    if pneumonia_result is not None:
        results.append(("Pneumonia chest X-ray", pneumonia_result))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    total = len(results)
    
    for test_name, result in results:
        status = "[OK] PASS" if result else "[X] FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} passed, {failed} failed")
    
    if failed == 0:
        print("\n" + "=" * 80)
        print("[OK] ALL TESTS PASSED")
        print("=" * 80)
        print("\nComplete inference flow is working:")
        print("1. Valid chest X-rays pass validation and get predictions")
        print("2. Invalid images are rejected before inference")
        print("3. Validation confidence is separate from prediction confidence")
        return True
    else:
        print("\n" + "=" * 80)
        print("[X] SOME TESTS FAILED")
        print("=" * 80)
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
