"""
Minimal test to isolate quantum model loading issue.
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

print("Testing quantum model loading...")

try:
    from src.models.quantum_svm import QuantumSVM
    print("✓ QuantumSVM class imported")
    
    model_path = "models/quantum_svm.pkl"
    print(f"\nLoading model from: {model_path}")
    
    quantum_model = QuantumSVM.load(model_path)
    print(f"✓ Model loaded successfully")
    print(f"  Feature dimension: {quantum_model.feature_dimension}")
    print(f"  Probability: {quantum_model.probability}")
    print(f"  Is trained: {quantum_model.is_trained}")
    
    # Try a prediction
    import numpy as np
    test_features = np.array([[0.5, -0.3, 0.2, 0.1]])
    pred = quantum_model.predict(test_features)
    print(f"✓ Prediction test: {pred}")
    
    if quantum_model.probability:
        proba = quantum_model.predict_proba(test_features)
        print(f"✓ Probability test: {proba}")
    
    print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
    
except Exception as e:
    print(f"\n✗✗✗ ERROR ✗✗✗")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
