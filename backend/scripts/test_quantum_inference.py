"""
Test Quantum SVM inference with real X-ray images.

This script tests the complete pipeline:
Image → ResNet50 → 2048D → PCA → 4D → Quantum SVM → Prediction

Compares Classical SVM vs Quantum SVM performance.
"""

import sys
from pathlib import Path
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.inference.predict import ChestXRayInference
from src.models.quantum_svm import QuantumSVM


def test_quantum_vs_classical():
    """Test both Classical and Quantum SVM on the same images."""
    
    print("=" * 70)
    print("Q-MedTriage: Quantum vs Classical SVM Comparison")
    print("=" * 70)
    
    # Test images
    test_images = [
        ("NORMAL", "data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg"),
        ("PNEUMONIA", "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg"),
    ]
    
    # Initialize classical inference pipeline
    print("\n" + "-" * 70)
    print("Initializing Classical SVM Pipeline")
    print("-" * 70)
    classical_pipeline = ChestXRayInference()
    
    # Load quantum model
    print("\n" + "-" * 70)
    print("Loading Quantum SVM")
    print("-" * 70)
    quantum_svm = QuantumSVM.load("models/quantum_svm.pkl")
    print(f"✓ Quantum SVM loaded")
    print(f"  Feature dimension: {quantum_svm.feature_dimension}")
    print(f"  Qubits: {quantum_svm.feature_dimension}")
    print(f"  Probability enabled: {quantum_svm.probability}")
    
    # Test each image
    results = []
    
    for true_label, image_path in test_images:
        print("\n" + "=" * 70)
        print(f"Testing: {true_label} X-ray")
        print(f"Image: {image_path}")
        print("=" * 70)
        
        if not Path(image_path).exists():
            print(f"✗ Image not found: {image_path}")
            continue
        
        # -----------------------------------------------------------------
        # Classical SVM
        # -----------------------------------------------------------------
        print("\n" + "-" * 70)
        print("Classical SVM Inference")
        print("-" * 70)
        
        classical_start = time.time()
        classical_result = classical_pipeline.predict(image_path, include_features=True)
        classical_time = (time.time() - classical_start) * 1000
        
        if not classical_result["success"]:
            print(f"✗ Classical inference failed: {classical_result.get('error')}")
            continue
        
        print(f"✓ Prediction: {classical_result['prediction_label']}")
        print(f"✓ Confidence: {classical_result['confidence']:.2%}")
        print(f"✓ Probabilities:")
        for label, prob in classical_result['probabilities'].items():
            print(f"    {label}: {prob:.2%}")
        print(f"✓ Inference time: {classical_time:.2f}ms")
        
        # Extract PCA features for quantum model
        pca_features = classical_result["features"]["pca_values"]
        print(f"✓ PCA features extracted: {len(pca_features)}D")
        
        # -----------------------------------------------------------------
        # Quantum SVM
        # -----------------------------------------------------------------
        print("\n" + "-" * 70)
        print("Quantum SVM Inference")
        print("-" * 70)
        
        # Prepare features for quantum model (reshape to 2D)
        import numpy as np
        pca_features_2d = np.array(pca_features).reshape(1, -1)
        
        quantum_start = time.time()
        
        # Predict
        quantum_prediction = quantum_svm.predict(pca_features_2d)[0]
        quantum_label = "PNEUMONIA" if quantum_prediction == 1 else "NORMAL"
        
        # Get probabilities
        if quantum_svm.probability:
            quantum_proba = quantum_svm.predict_proba(pca_features_2d)[0]
            quantum_confidence = quantum_proba[quantum_prediction]
            quantum_time = (time.time() - quantum_start) * 1000
            
            print(f"✓ Prediction: {quantum_label}")
            print(f"✓ Confidence: {quantum_confidence:.2%}")
            print(f"✓ Probabilities:")
            print(f"    NORMAL: {quantum_proba[0]:.2%}")
            print(f"    PNEUMONIA: {quantum_proba[1]:.2%}")
            print(f"✓ Inference time: {quantum_time:.2f}ms")
        else:
            quantum_time = (time.time() - quantum_start) * 1000
            print(f"✓ Prediction: {quantum_label}")
            print(f"✓ Inference time: {quantum_time:.2f}ms")
            print("⚠ Probability not available")
            quantum_confidence = None
            quantum_proba = None
        
        # -----------------------------------------------------------------
        # Comparison
        # -----------------------------------------------------------------
        print("\n" + "-" * 70)
        print("Comparison")
        print("-" * 70)
        print(f"True Label:           {true_label}")
        print(f"Classical Prediction: {classical_result['prediction_label']}")
        print(f"Quantum Prediction:   {quantum_label}")
        print(f"Classical Confidence: {classical_result['confidence']:.2%}")
        if quantum_confidence:
            print(f"Quantum Confidence:   {quantum_confidence:.2%}")
        print(f"Classical Time:       {classical_time:.2f}ms")
        print(f"Quantum Time:         {quantum_time:.2f}ms")
        
        # Store results
        results.append({
            "true_label": true_label,
            "image_path": image_path,
            "classical": {
                "prediction": classical_result['prediction_label'],
                "confidence": classical_result['confidence'],
                "probabilities": classical_result['probabilities'],
                "time_ms": classical_time,
                "correct": classical_result['prediction_label'] == true_label,
            },
            "quantum": {
                "prediction": quantum_label,
                "confidence": quantum_confidence,
                "probabilities": {
                    "NORMAL": quantum_proba[0] if quantum_proba is not None else None,
                    "PNEUMONIA": quantum_proba[1] if quantum_proba is not None else None,
                },
                "time_ms": quantum_time,
                "correct": quantum_label == true_label,
            },
        })
    
    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for result in results:
        print(f"\n{result['true_label']} Image:")
        print(f"  Classical: {result['classical']['prediction']} "
              f"({result['classical']['confidence']:.2%}) "
              f"{'✓' if result['classical']['correct'] else '✗'}")
        print(f"  Quantum:   {result['quantum']['prediction']} "
              f"({result['quantum']['confidence']:.2%} if result['quantum']['confidence'] else 'N/A') "
              f"{'✓' if result['quantum']['correct'] else '✗'}")
    
    print("\n" + "=" * 70)
    print("Quantum SVM inference test complete!")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    test_quantum_vs_classical()
