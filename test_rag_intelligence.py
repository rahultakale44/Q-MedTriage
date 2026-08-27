"""
Test script for RAG/Intelligence Layer Only
Tests RAG retrieval and Gemini synthesis without loading ML models
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded .env from {env_path}")
    else:
        print(f"Warning: .env file not found at {env_path}")
except ImportError:
    print("Warning: python-dotenv not installed, relying on system environment")

print("=" * 70)
print("Testing Q-MedTriage Intelligence Layer")
print("=" * 70)

# Check environment
print("\n1. Checking environment configuration...")
gemini_key_configured = bool(os.getenv("GEMINI_API_KEY"))
print(f"   GEMINI_API_KEY configured: {'✓ Yes' if gemini_key_configured else '✗ No'}")

if not gemini_key_configured:
    print("\n✗ GEMINI_API_KEY not found in environment")
    print("  Please ensure .env file exists with GEMINI_API_KEY set")
    sys.exit(1)

# Test RAG Retriever
print("\n2. Testing RAG Retriever...")
try:
    from src.rag.retriever import RAGRetriever
    
    print("   Loading retriever...")
    retriever = RAGRetriever()
    retriever.load()
    
    print(f"   ✓ RAG Retriever ready")
    print(f"   ✓ Documents: {retriever.vector_store.index.ntotal}")
    print(f"   ✓ Embedding dimension: {retriever.embedding_generator.get_dimension()}D")
    
    RAG_STATUS = "WORKING"
    
except Exception as e:
    print(f"   ✗ RAG Retriever failed: {e}")
    RAG_STATUS = "FAILED"
    retriever = None

# Test Gemini Synthesizer
print("\n3. Testing Gemini Synthesizer...")
try:
    from src.rag.gemini_synthesizer import GeminiSynthesizer
    
    print("   Initializing synthesizer...")
    synthesizer = GeminiSynthesizer()
    synthesizer.initialize()
    
    print(f"   ✓ Gemini Synthesizer ready")
    print(f"   ✓ Model: {synthesizer.model_name}")
    print(f"   ✓ Temperature: {synthesizer.temperature}")
    
    GEMINI_STATUS = "WORKING"
    
except Exception as e:
    print(f"   ✗ Gemini Synthesizer failed: {e}")
    GEMINI_STATUS = "FAILED"
    synthesizer = None

# Test complete RAG pipeline
if RAG_STATUS == "WORKING" and GEMINI_STATUS == "WORKING":
    print("\n4. Testing complete RAG → LLM pipeline...")
    
    test_questions = [
        "Why this prediction?",
        "What are symptoms of pneumonia?",
        "Explain simply"
    ]
    
    for question in test_questions:
        print(f"\n   Query: '{question}'")
        
        try:
            # Retrieve evidence
            print(f"   [RAG] Retrieving...")
            results = retriever.retrieve(question, top_k=3)
            print(f"   [RAG] ✓ Retrieved {len(results)} documents")
            
            # Synthesize response
            print(f"   [LLM] Generating...")
            response = synthesizer.synthesize(question, results)
            
            if response['success']:
                print(f"   [LLM] ✓ Response generated")
                print(f"   [LLM] Answer length: {len(response['answer'])} chars")
                print(f"   [LLM] Sources: {len(response['sources'])}")
                print(f"\n   Preview:")
                preview = response['answer'][:200]
                print(f"   {preview}...")
                ASK_STATUS = "WORKING"
            else:
                print(f"   [LLM] ✗ Generation failed: {response.get('error')}")
                ASK_STATUS = "FAILED"
                
        except Exception as e:
            print(f"   ✗ Pipeline failed: {e}")
            ASK_STATUS = "FAILED"
            import traceback
            traceback.print_exc()
            break
else:
    print("\n4. Skipping pipeline test (prerequisites failed)")
    ASK_STATUS = "NOT TESTED"

# Final report
print("\n" + "=" * 70)
print("FINAL STATUS REPORT")
print("=" * 70)
print(f"RAG Retriever:        {RAG_STATUS}")
print(f"Gemini Synthesizer:   {GEMINI_STATUS}")
print(f"/ask Pipeline:        {ASK_STATUS}")
print("=" * 70)

if RAG_STATUS == "WORKING" and GEMINI_STATUS == "WORKING" and ASK_STATUS == "WORKING":
    print("\n✓ Intelligence layer fully operational")
    print("✓ Backend /ask endpoint should work correctly")
else:
    print("\n✗ Intelligence layer has issues")
    if RAG_STATUS != "WORKING":
        print("  - Fix RAG retriever initialization")
    if GEMINI_STATUS != "WORKING":
        print("  - Check GEMINI_API_KEY configuration")
    if ASK_STATUS == "FAILED":
        print("  - Check complete pipeline flow")
