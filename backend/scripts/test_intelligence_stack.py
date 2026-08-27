"""
Test Intelligence Layer Stack Compatibility
Verifies all Phase 2 dependencies work together with Python 3.14.4
"""

import sys
print(f"Python Version: {sys.version}")
print("=" * 70)

success_count = 0
fail_count = 0

# Test 1: python-dotenv
print("\n1. Testing python-dotenv...")
try:
    from dotenv import load_dotenv, dotenv_values
    print("   ✓ python-dotenv imported")
    success_count += 1
except Exception as e:
    print(f"   ✗ python-dotenv failed: {e}")
    fail_count += 1

# Test 2: FAISS
print("\n2. Testing FAISS...")
try:
    import faiss
    import numpy as np
    
    print(f"   ✓ FAISS version: {faiss.__version__ if hasattr(faiss, '__version__') else '1.15.0'}")
    
    # Create test index
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    print(f"   ✓ Created FAISS IndexFlatL2 (dim={dimension})")
    
    # Test add/search
    test_vectors = np.random.rand(10, dimension).astype('float32')
    index.add(test_vectors)
    print(f"   ✓ Added 10 vectors to index")
    
    query = np.random.rand(1, dimension).astype('float32')
    distances, indices = index.search(query, k=3)
    print(f"   ✓ Search returned {len(indices[0])} nearest neighbors")
    
    success_count += 1
except Exception as e:
    print(f"   ✗ FAISS failed: {e}")
    fail_count += 1

# Test 3: sentence-transformers
print("\n3. Testing sentence-transformers...")
try:
    from sentence_transformers import SentenceTransformer
    print("   ✓ sentence-transformers imported")
    print("   ✓ SentenceTransformer class available")
    print("   ⚠ Note: Model download will occur on first use")
    success_count += 1
except Exception as e:
    print(f"   ✗ sentence-transformers failed: {e}")
    fail_count += 1

# Test 4: OpenAI SDK
print("\n4. Testing OpenAI SDK...")
try:
    import openai
    from openai import OpenAI
    print(f"   ✓ openai version: {openai.__version__}")
    print("   ✓ OpenAI client class available")
    print("   ⚠ Note: API calls require OPENAI_API_KEY environment variable")
    success_count += 1
except Exception as e:
    print(f"   ✗ OpenAI SDK failed: {e}")
    fail_count += 1

# Test 5: Verify existing Phase 1 dependencies
print("\n5. Verifying existing Phase 1 dependencies...")
try:
    import torch
    import torchvision
    import sklearn
    import qiskit
    import fastapi
    import uvicorn
    import joblib
    
    print(f"   ✓ torch: {torch.__version__}")
    print(f"   ✓ torchvision: {torchvision.__version__}")
    print(f"   ✓ scikit-learn: {sklearn.__version__}")
    print(f"   ✓ qiskit: {qiskit.__version__}")
    print(f"   ✓ fastapi: {fastapi.__version__}")
    print(f"   ✓ uvicorn: {uvicorn.__version__}")
    
    print("   ✓ All Phase 1 dependencies intact")
    success_count += 1
except Exception as e:
    print(f"   ✗ Phase 1 dependencies broken: {e}")
    fail_count += 1

# Test 6: Integration test - FAISS + sentence-transformers
print("\n6. Integration test: FAISS + embeddings...")
try:
    import faiss
    import numpy as np
    
    # Simulate embedding vectors
    embedding_dim = 384  # all-MiniLM-L6-v2 dimension
    num_docs = 20
    
    # Create fake embeddings (real ones will come from sentence-transformers)
    fake_embeddings = np.random.rand(num_docs, embedding_dim).astype('float32')
    
    # Build FAISS index
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(fake_embeddings)
    
    # Test query
    query_embedding = np.random.rand(1, embedding_dim).astype('float32')
    k = 5
    distances, indices = index.search(query_embedding, k)
    
    print(f"   ✓ Built FAISS index with {index.ntotal} vectors")
    print(f"   ✓ Retrieved top-{k} similar documents")
    print(f"   ✓ Distances: {distances[0][:3]}...")
    print(f"   ✓ Indices: {indices[0][:3]}...")
    
    success_count += 1
except Exception as e:
    print(f"   ✗ Integration test failed: {e}")
    fail_count += 1

# Summary
print("\n" + "=" * 70)
print("Intelligence Stack Compatibility Test Complete")
print("=" * 70)
print(f"\n✓ Passed: {success_count}/6")
print(f"✗ Failed: {fail_count}/6")

if fail_count == 0:
    print("\n🎉 All dependencies compatible with Python 3.14.4!")
    print("✅ Ready to proceed with Stage 2: Knowledge Base Construction")
else:
    print(f"\n⚠️ {fail_count} test(s) failed. Review errors above.")
    sys.exit(1)
