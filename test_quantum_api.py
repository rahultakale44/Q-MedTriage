"""
Test Quantum SVM API integration.

Tests both Classical and Quantum SVM through the FastAPI /predict endpoint.
"""
import urllib.request
import json
import mimetypes
from pathlib import Path


def create_multipart_form_data(file_path: str, field_name: str = "file", classifier: str = "classical"):
    """Create multipart/form-data payload for file upload with classifier parameter"""
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
        print(f"✓ Quantum SVM: {data.get('quantum_svm', 'unknown')}")
        print(f"✓ Pipeline Loaded: {data.get('pipeline_loaded', False)}")
        
        return data
        
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return None


def test_predict(api_url: str, image_path: str, classifier: str = "classical"):
    """Test /predict endpoint with specified classifier"""
    print(f"\n{'='*70}")
    print(f"Testing: {image_path}")
    print(f"Classifier: {classifier.upper()}")
    print(f"{'='*70}")
    
    try:
        # Create multipart form data
        body, content_type = create_multipart_form_data(image_path, classifier=classifier)
        
        # Create request with classifier parameter
        url = f"{api_url}/predict?classifier={classifier}"
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": content_type},
            method="POST"
        )
        
        # Send request
        with urllib.request.urlopen(request, timeout=60) as response:
            status = response.status
            response_data = response.read().decode("utf-8")
            result = json.loads(response_data)
        
        # Display results
        print(f"✓ HTTP Status: {status}")
        print(f"✓ Success: {result.get('success', False)}")
        print(f"✓ Model: {result.get('model', 'N/A')}")
        print(f"✓ Model Type: {result.get('model_type', 'N/A')}")
        print(f"✓ Prediction: {result.get('prediction_label', 'N/A')}")
        
        confidence = result.get('confidence')
        if confidence is not None:
            print(f"✓ Confidence: {confidence:.2%}")
        else:
            print(f"✓ Confidence: Not available")
        
        print(f"✓ Inference Time: {result.get('inference_time_ms', 0)}ms")
        
        probabilities = result.get('probabilities')
        if probabilities:
            print(f"✓ Probabilities:")
            for label, prob in probabilities.items():
                print(f"    {label}: {prob:.2%}")
        else:
            print(f"✓ Probabilities: Not available")
        
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


if __name__ == "__main__":
    API_URL = "http://127.0.0.1:8000"
    
    print("\n" + "="*70)
    print("Q-MedTriage: Classical vs Quantum SVM API Test")
    print("="*70)
    
    # Test health endpoint
    health_data = test_health(API_URL)
    
    if not health_data or not health_data.get('pipeline_loaded'):
        print("\n✗ API is not healthy. Make sure the server is running:")
        print("  python -m uvicorn src.api.main:app --reload")
        exit(1)
    
    # Check if quantum model is available
    quantum_available = health_data.get('quantum_svm') == 'ready'
    print(f"\nQuantum SVM Available: {quantum_available}")
    
    # Test images
    test_images = [
        ("NORMAL", "data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg"),
        ("PNEUMONIA", "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg"),
    ]
    
    results = []
    
    for true_label, image_path in test_images:
        if not Path(image_path).exists():
            print(f"\n✗ Image not found: {image_path}")
            continue
        
        # Test Classical SVM
        print(f"\n{'='*70}")
        print(f"Testing {true_label} Image with CLASSICAL SVM")
        print(f"{'='*70}")
        classical_success, classical_result = test_predict(API_URL, image_path, "classical")
        
        # Test Quantum SVM if available
        if quantum_available:
            print(f"\n{'='*70}")
            print(f"Testing {true_label} Image with QUANTUM SVM")
            print(f"{'='*70}")
            quantum_success, quantum_result = test_predict(API_URL, image_path, "quantum")
        else:
            print(f"\n⚠ Skipping Quantum SVM test (model not available)")
            quantum_success = False
            quantum_result = None
        
        # Store results
        results.append({
            "true_label": true_label,
            "image_path": image_path,
            "classical": classical_result,
            "quantum": quantum_result,
        })
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    for result in results:
        print(f"\n{result['true_label']} Image:")
        
        if result['classical']:
            classical_pred = result['classical'].get('prediction_label', 'N/A')
            classical_conf = result['classical'].get('confidence')
            conf_str = f"{classical_conf:.2%}" if classical_conf is not None else "N/A"
            match = "✓" if classical_pred == result['true_label'] else "✗"
            print(f"  Classical: {classical_pred} ({conf_str}) {match}")
        else:
            print(f"  Classical: FAILED")
        
        if result['quantum']:
            quantum_pred = result['quantum'].get('prediction_label', 'N/A')
            quantum_conf = result['quantum'].get('confidence')
            conf_str = f"{quantum_conf:.2%}" if quantum_conf is not None else "N/A"
            match = "✓" if quantum_pred == result['true_label'] else "✗"
            print(f"  Quantum:   {quantum_pred} ({conf_str}) {match}")
        elif quantum_available:
            print(f"  Quantum:   FAILED")
        else:
            print(f"  Quantum:   NOT AVAILABLE")
    
    print("="*70)
