"""
Test FastAPI /predict endpoint using Python standard library (no external dependencies)
"""
import urllib.request
import json
import mimetypes
from pathlib import Path


def create_multipart_form_data(file_path: str, field_name: str = "file"):
    """Create multipart/form-data payload for file upload"""
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # Read file
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"
    
    filename = Path(file_path).name
    
    # Build multipart body
    body = []
    body.append(f"--{boundary}".encode())
    body.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"'.encode()
    )
    body.append(f"Content-Type: {content_type}".encode())
    body.append(b"")
    body.append(file_data)
    body.append(f"--{boundary}--".encode())
    
    body_bytes = b"\r\n".join(body)
    
    return body_bytes, f"multipart/form-data; boundary={boundary}"


def test_predict(api_url: str, image_path: str):
    """Test /predict endpoint"""
    print(f"\n{'='*70}")
    print(f"Testing: {image_path}")
    print(f"{'='*70}")
    
    try:
        # Create multipart form data
        body, content_type = create_multipart_form_data(image_path)
        
        # Create request
        request = urllib.request.Request(
            f"{api_url}/predict",
            data=body,
            headers={"Content-Type": content_type},
            method="POST"
        )
        
        # Send request
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            response_data = response.read().decode("utf-8")
            result = json.loads(response_data)
        
        # Display results
        print(f"✓ HTTP Status: {status}")
        print(f"✓ Success: {result.get('success', False)}")
        print(f"✓ Model: {result.get('model', 'N/A')}")
        print(f"✓ Prediction: {result.get('prediction_label', 'N/A')}")
        print(f"✓ Confidence: {result.get('confidence', 0):.2%}")
        print(f"✓ Inference Time: {result.get('inference_time_ms', 0)}ms")
        print(f"✓ Probabilities:")
        for label, prob in result.get('probabilities', {}).items():
            print(f"    {label}: {prob:.2%}")
        print(f"✓ Disclaimer: {result.get('disclaimer', 'N/A')[:80]}...")
        
        return True, result
        
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error: {e.code} {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            error_data = json.loads(error_body)
            print(f"✗ Detail: {error_data.get('detail', 'No detail')}")
        except:
            print(f"✗ Raw error: {e.read()}")
        return False, None
        
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return False, None


def test_health(api_url: str):
    """Test /health endpoint"""
    print(f"\n{'='*70}")
    print("Testing /health endpoint")
    print(f"{'='*70}")
    
    try:
        request = urllib.request.Request(f"{api_url}/health")
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        print(f"✓ API: {data.get('api', 'unknown')}")
        print(f"✓ Vision Model: {data.get('vision_model', 'unknown')}")
        print(f"✓ Classical SVM: {data.get('classical_svm', 'unknown')}")
        print(f"✓ Quantum Model: {data.get('quantum_model', 'unknown')}")
        print(f"✓ Pipeline Loaded: {data.get('pipeline_loaded', False)}")
        
        return data.get('pipeline_loaded', False)
        
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    API_URL = "http://127.0.0.1:8000"
    
    print("\n" + "="*70)
    print("Q-MedTriage API Test (Standard Library)")
    print("="*70)
    
    # Test health endpoint
    healthy = test_health(API_URL)
    
    if not healthy:
        print("\n✗ API is not healthy. Make sure the server is running:")
        print("  python -m uvicorn src.api.main:app --reload")
        exit(1)
    
    # Test with real X-rays
    test_images = [
        ("NORMAL", "data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg"),
        ("PNEUMONIA", "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg"),
    ]
    
    results = []
    for label, image_path in test_images:
        if Path(image_path).exists():
            success, result = test_predict(API_URL, image_path)
            results.append((label, success, result))
        else:
            print(f"\n✗ Image not found: {image_path}")
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    for true_label, success, result in results:
        if success and result:
            predicted = result.get('prediction_label', 'N/A')
            confidence = result.get('confidence', 0)
            match = "✓" if true_label == predicted else "✗"
            print(f"{match} {true_label} → {predicted} ({confidence:.2%})")
        else:
            print(f"✗ {true_label} → FAILED")
    
    print("="*70)
