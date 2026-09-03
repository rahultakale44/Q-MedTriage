"""
Test script to verify Classical SVM model accuracy on test dataset
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.inference.predict import ChestXRayInference
from PIL import Image
import random

def test_model_on_dataset():
    """Test the model on a sample of test images"""
    
    print("=" * 70)
    print("Testing Classical SVM on Test Dataset")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = ChestXRayInference()
    
    # Test data paths
    normal_dir = PROJECT_ROOT / "data/archive (1)/chest_xray/chest_xray/test/NORMAL"
    pneumonia_dir = PROJECT_ROOT / "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA"
    
    if not normal_dir.exists() or not pneumonia_dir.exists():
        print("ERROR: Test dataset not found!")
        return
    
    # Get sample images
    normal_images = list(normal_dir.glob("*.jpeg"))[:5]
    pneumonia_images = list(pneumonia_dir.glob("*.jpeg"))[:5]
    
    print(f"\nTesting {len(normal_images)} NORMAL images...")
    print("-" * 70)
    
    normal_correct = 0
    for img_path in normal_images:
        result = pipeline.predict(str(img_path), classifier="classical")
        predicted = result["prediction_label"]
        confidence = result["confidence"]
        
        is_correct = predicted == "NORMAL"
        if is_correct:
            normal_correct += 1
        
        status = "✓" if is_correct else "✗"
        print(f"{status} {img_path.name}: {predicted} ({confidence:.1%})")
    
    print(f"\nNORMAL Accuracy: {normal_correct}/{len(normal_images)} ({normal_correct/len(normal_images):.1%})")
    
    print(f"\nTesting {len(pneumonia_images)} PNEUMONIA images...")
    print("-" * 70)
    
    pneumonia_correct = 0
    for img_path in pneumonia_images:
        result = pipeline.predict(str(img_path), classifier="classical")
        predicted = result["prediction_label"]
        confidence = result["confidence"]
        
        is_correct = predicted == "PNEUMONIA"
        if is_correct:
            pneumonia_correct += 1
        
        status = "✓" if is_correct else "✗"
        print(f"{status} {img_path.name}: {predicted} ({confidence:.1%})")
    
    print(f"\nPNEUMONIA Accuracy: {pneumonia_correct}/{len(pneumonia_images)} ({pneumonia_correct/len(pneumonia_images):.1%})")
    
    total_correct = normal_correct + pneumonia_correct
    total_samples = len(normal_images) + len(pneumonia_images)
    overall_accuracy = total_correct / total_samples
    
    print("\n" + "=" * 70)
    print(f"Overall Accuracy: {total_correct}/{total_samples} ({overall_accuracy:.1%})")
    print("=" * 70)
    
    print("\n\nNOTE: Training results showed 92% validation accuracy")
    print("This sample test should be close to that if model is working correctly")

if __name__ == "__main__":
    test_model_on_dataset()
