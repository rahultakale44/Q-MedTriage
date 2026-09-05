"""
Test NORMAL images that are showing as NORMAL but with higher PNEUMONIA probability
"""
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.inference.predict import ChestXRayInference

print("=" * 70)
print("Testing NORMAL Images with Bug")
print("=" * 70)

pipeline = ChestXRayInference()

# Test NORMAL images
normal_dir = PROJECT_ROOT / "data/archive (1)/chest_xray/chest_xray/test/NORMAL"
test_images = list(normal_dir.glob("*.jpeg"))[:5]

for img_path in test_images:
    print(f"\n{'=' * 70}")
    print(f"Image: {img_path.name}")
    print(f"Expected: NORMAL")
    print("-" * 70)
    
    result = pipeline.predict(str(img_path), classifier="classical")
    
    if result["success"]:
        pred = result['prediction_label']
        conf = result['confidence']
        probs = result['probabilities']
        
        normal_prob = probs['NORMAL']
        pneumonia_prob = probs['PNEUMONIA']
        
        print(f"Prediction: {pred}")
        print(f"Confidence: {conf:.1%}")
        print(f"NORMAL probability: {normal_prob:.1%}")
        print(f"PNEUMONIA probability: {pneumonia_prob:.1%}")
        
        # Check for bug
        if pred == "NORMAL" and pneumonia_prob > normal_prob:
            print(f"\n❌ BUG FOUND: Showing NORMAL but PNEUMONIA has higher probability!")
            print(f"   This should predict PNEUMONIA ({pneumonia_prob:.1%}) not NORMAL ({normal_prob:.1%})")
        elif pred == "PNEUMONIA" and normal_prob > pneumonia_prob:
            print(f"\n❌ BUG FOUND: Showing PNEUMONIA but NORMAL has higher probability!")
        else:
            print(f"\n✓ Correct: {pred} has highest probability")
    else:
        print(f"Error: {result.get('error')}")

print("\n" + "=" * 70)
