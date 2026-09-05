"""
Debug script to identify the prediction bug
"""
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.inference.predict import ChestXRayInference
from PIL import Image

print("=" * 70)
print("Debugging Prediction Bug")
print("=" * 70)

# Initialize pipeline
pipeline = ChestXRayInference()

# Test with a chest X-ray
test_image = PROJECT_ROOT / "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg"

if test_image.exists():
    print(f"\nTesting with: {test_image.name}")
    print("Expected: PNEUMONIA")
    print("-" * 70)
    
    # Run full prediction
    result = pipeline.predict(str(test_image), classifier="classical", include_features=True)
    
    if result["success"]:
        print(f"\n[RESULT FROM PIPELINE]")
        print(f"Prediction: {result['prediction_label']}")
        print(f"Prediction index: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Probabilities: {result['probabilities']}")
        
        # Now test the SVM directly
        print(f"\n[TESTING SVM DIRECTLY]")
        pca_features = result['features']['pca_values']
        pca_array = np.array(pca_features).reshape(1, -1)
        
        # Direct SVM prediction
        svm_prediction = pipeline.svm_model.predict(pca_array)[0]
        svm_probabilities = pipeline.svm_model.predict_proba(pca_array)[0]
        
        print(f"Direct SVM prediction: {svm_prediction}")
        print(f"Direct SVM probabilities: {svm_probabilities}")
        print(f"  Class 0 (NORMAL): {svm_probabilities[0]:.1%}")
        print(f"  Class 1 (PNEUMONIA): {svm_probabilities[1]:.1%}")
        
        # Check which class has higher probability
        max_prob_class = np.argmax(svm_probabilities)
        print(f"\nClass with highest probability: {max_prob_class} ({['NORMAL', 'PNEUMONIA'][max_prob_class]})")
        print(f"SVM predicted class: {svm_prediction} ({['NORMAL', 'PNEUMONIA'][svm_prediction]})")
        
        if max_prob_class != svm_prediction:
            print("\n❌ BUG CONFIRMED: SVM predicts class {svm_prediction} but class {max_prob_class} has higher probability!")
            print("This is caused by class_weight='balanced' shifting the decision boundary")
        else:
            print("\n✓ SVM prediction matches highest probability")
    else:
        print(f"Error: {result.get('error')}")
else:
    print(f"Test image not found: {test_image}")

print("\n" + "=" * 70)
