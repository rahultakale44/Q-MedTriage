"""
Trace the exact issue by testing both valid and invalid images
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_image(image_path, description):
    print("\n" + "=" * 70)
    print(f"Testing: {description}")
    print("=" * 70)
    print(f"File: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path.split('\\')[-1], f, 'image/jpeg')}
            response = requests.post(f'{API_URL}/predict', files=files)
        
        print(f"\nHTTP Status: {response.status_code}")
        print(f"OK: {response.ok}")
        
        data = response.json()
        print(f"\nResponse Body Keys: {list(data.keys())}")
        print(f"  success: {data.get('success')}")
        print(f"  error: {data.get('error')}")
        
        if 'validation' in data:
            print(f"  validation.is_valid_chest_xray: {data['validation'].get('is_valid_chest_xray')}")
            print(f"  validation.confidence: {data['validation'].get('confidence')}")
            print(f"  validation.detected_type: {data['validation'].get('detected_type')}")
        
        # Determine what frontend should do
        print(f"\n>>> FRONTEND BEHAVIOR:")
        if response.status_code == 400 and data.get('error') == 'unsupported_image':
            print("  validationError = TRUE")
            print("  Show: Invalid Image screen")
            print("  NO pipeline stages")
        elif response.ok and data.get('success'):
            print("  validationError = FALSE")
            print("  Show: Full pipeline → Result")
            print(f"  Prediction: {data.get('prediction_label')} ({data.get('confidence'):.1%})")
        else:
            print("  validationError = FALSE")
            print("  Show: System error (NOT invalid image)")
            
    except Exception as e:
        print(f"\nFETCH ERROR: {e}")
        print(">>> FRONTEND BEHAVIOR:")
        print("  validationError = FALSE")
        print("  Show: Network error (NOT invalid image)")

# Test with genuine chest X-ray
test_image(
    r"data\archive (1)\chest_xray\chest_xray\test\NORMAL\IM-0001-0001.jpeg",
    "GENUINE CHEST X-RAY"
)

print("\n" + "=" * 70)
print("Note: Skull X-ray test would require an actual skull X-ray file")
print("=" * 70)
