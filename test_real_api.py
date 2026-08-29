import requests

# Test with genuine chest X-ray
genuine_path = r"data\archive (1)\chest_xray\chest_xray\test\NORMAL\IM-0001-0001.jpeg"

print("=" * 70)
print("Testing GENUINE CHEST X-RAY")
print("=" * 70)
print(f"File: {genuine_path}\n")

with open(genuine_path, 'rb') as f:
    files = {'file': ('chest_xray.jpeg', f, 'image/jpeg')}
    response = requests.post('http://localhost:8000/predict', files=files)
    
print(f"HTTP Status: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"\nResponse Body:")
print(response.text[:2000])  # First 2000 chars

if response.status_code != 200:
    print(f"\nERROR RESPONSE")
    
print("\n" + "=" * 70)
