"""
Test Python 3.14 compatibility with proposed Intelligence Layer dependencies

This script tests whether the proposed libraries can be imported and used
with Python 3.14.4 before full installation.
"""

import sys
print(f"Python Version: {sys.version}")
print("=" * 70)

# Test 1: Check if faiss-cpu is compatible
print("\n1. Testing faiss-cpu...")
try:
    import faiss
    print(f"   ✓ faiss version: {faiss.__version__ if hasattr(faiss, '__version__') else 'unknown'}")
    
    # Test basic functionality
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    print(f"   ✓ Created FAISS index (dim={dimension})")
    
except ImportError as e:
    print(f"   ✗ faiss-cpu not installed: {e}")
except Exception as e:
    print(f"   ✗ faiss-cpu error: {e}")

# Test 2: Check if sentence-transformers is compatible
print("\n2. Testing sentence-transformers...")
try:
    from sentence_transformers import SentenceTransformer
    print(f"   ✓ sentence-transformers imported")
    
    # Note: Don't download model in test, just check import
    print(f"   ✓ SentenceTransformer class available")
    
except ImportError as e:
    print(f"   ✗ sentence-transformers not installed: {e}")
except Exception as e:
    print(f"   ✗ sentence-transformers error: {e}")

# Test 3: Check if openai is compatible
print("\n3. Testing openai...")
try:
    import openai
    print(f"   ✓ openai version: {openai.__version__}")
    
except ImportError as e:
    print(f"   ✗ openai not installed: {e}")
except Exception as e:
    print(f"   ✗ openai error: {e}")

# Test 4: Check if transformers is compatible (alternative)
print("\n4. Testing transformers...")
try:
    import transformers
    print(f"   ✓ transformers version: {transformers.__version__}")
    
except ImportError as e:
    print(f"   ✗ transformers not installed: {e}")
except Exception as e:
    print(f"   ✗ transformers error: {e}")

# Test 5: Verify existing dependencies still work
print("\n5. Verifying existing dependencies...")
try:
    import torch
    print(f"   ✓ torch version: {torch.__version__}")
    
    import torchvision
    print(f"   ✓ torchvision version: {torchvision.__version__}")
    
    import sklearn
    print(f"   ✓ scikit-learn version: {sklearn.__version__}")
    
    import qiskit
    print(f"   ✓ qiskit version: {qiskit.__version__}")
    
    import fastapi
    print(f"   ✓ fastapi version: {fastapi.__version__}")
    
except Exception as e:
    print(f"   ✗ Existing dependency error: {e}")

print("\n" + "=" * 70)
print("Compatibility Test Complete")
print("=" * 70)
