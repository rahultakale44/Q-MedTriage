"""Test API with real X-ray image"""
import requests
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/predict"

# Test images
test_normal = Path("data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg")
test_pneumonia = Path("data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg")

print("=" * 70)
print("Testing Q-MedTriage API")
print("=" * 70)

# Test with NORMAL X-ray
if test_normal.exists():
    print("\n1. Testing with NORMAL X-ray:")
    print("-" * 70)
    with open(test_normal, "rb") as f:
        files = {"file": (test_normal.name, f, "image/jpeg")}
        response = requests.post(API_URL, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Prediction: {result['prediction_label']}")
        print(f"✓ Confidence: {result['confidence']:.2%}")
        print(f"✓ Inference time: {result['inference_time_ms']}ms")
        print(f"✓ Probabilities:")
        for label, prob in result['probabilities'].items():
            print(f"    {label}: {prob:.2%}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

# Test with PNEUMONIA X-ray
if test_pneumonia.exists():
    print("\n2. Testing with PNEUMONIA X-ray:")
    print("-" * 70)
    with open(test_pneumonia, "rb") as f:
        files = {"file": (test_pneumonia.name, f, "image/jpeg")}
        response = requests.post(API_URL, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Prediction: {result['prediction_label']}")
        print(f"✓ Confidence: {result['confidence']:.2%}")
        print(f"✓ Inference time: {result['inference_time_ms']}ms")
        print(f"✓ Probabilities:")
        for label, prob in result['probabilities'].items():
            print(f"    {label}: {prob:.2%}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

print("\n" + "=" * 70)
print("API test complete")
print("=" * 70)
