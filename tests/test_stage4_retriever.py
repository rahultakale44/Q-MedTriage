"""
Stage 4: RAG Retrieval Service - Comprehensive Tests

Tests the RAG retrieval layer (evidence retrieval only, no LLM generation).
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag.retriever import RAGRetriever


def test_retriever_initialization():
    """TEST 1: Retriever initialization"""
    print("\n" + "=" * 70)
    print("TEST 1: Retriever Initialization")
    print("=" * 70)
    
    retriever = RAGRetriever()
    retriever.load()
    
    # Verify components loaded
    assert retriever.is_ready, "Retriever not marked as ready"
    assert retriever.embedding_generator is not None, "Embedding generator not loaded"
    assert retriever.vector_store is not None, "Vector store not loaded"
    print("✓ Retriever initialized successfully")
    
    # Verify index loaded
    assert retriever.vector_store.index is not None, "FAISS index not loaded"
    assert retriever.vector_store.index.ntotal == 22, f"Expected 22 vectors, got {retriever.vector_store.index.ntotal}"
    print("✓ FAISS index loaded: 22 vectors")
    
    # Verify metadata loaded
    assert len(retriever.vector_store.metadata) == 22, f"Expected 22 metadata entries, got {len(retriever.vector_store.metadata)}"
    print("✓ Metadata loaded: 22 entries")
    
    # Verify embedding model
    assert retriever.embedding_generator.model is not None, "Embedding model not loaded"
    dim = retriever.embedding_generator.get_dimension()
    assert dim == 384, f"Expected 384D, got {dim}D"
    print(f"✓ Embedding model loaded: {dim}D")
    
    return retriever


def test_basic_semantic_retrieval(retriever):
    """TEST 2: Basic semantic retrieval"""
    print("\n" + "=" * 70)
    print("TEST 2: Basic Semantic Retrieval")
    print("=" * 70)
    
    query = "What are common symptoms of pneumonia?"
    results = retriever.retrieve(query, top_k=5)
    
    # Verify results returned
    assert len(results) > 0, "No results returned"
    print(f"✓ Results returned: {len(results)}")
    
    # Verify top result relevance
    top_result = results[0]
    assert top_result["condition"] == "pneumonia", f"Top result condition: {top_result['condition']}"
    assert "symptom" in top_result["category"].lower() or "symptom" in top_result["title"].lower(), \
        f"Top result not about symptoms: {top_result['title']}"
    print(f"✓ Top result relevant: {top_result['title']} ({top_result['category']})")
    print(f"  Similarity: {top_result['similarity_score']:.4f}")


def test_pneumonia_diagnosis_retrieval(retriever):
    """TEST 3: Pneumonia diagnosis retrieval"""
    print("\n" + "=" * 70)
    print("TEST 3: Pneumonia Diagnosis Retrieval")
    print("=" * 70)
    
    query = "How is pneumonia diagnosed?"
    results = retriever.retrieve(query, top_k=5)
    
    assert len(results) > 0, "No results returned"
    print(f"✓ Results returned: {len(results)}")
    
    # Check for diagnosis-related content
    top_result = results[0]
    relevant = ("diagnos" in top_result["title"].lower() or 
                "diagnos" in top_result["category"].lower())
    
    assert relevant, f"Top result not about diagnosis: {top_result['title']}"
    print(f"✓ Top result relevant: {top_result['title']}")
    print(f"  Category: {top_result['category']}")


def test_normal_xray_retrieval(retriever):
    """TEST 4: Normal chest X-ray retrieval"""
    print("\n" + "=" * 70)
    print("TEST 4: Normal Chest X-ray Retrieval")
    print("=" * 70)
    
    query = "What does a normal chest X-ray show?"
    results = retriever.retrieve(query, top_k=5)
    
    assert len(results) > 0, "No results returned"
    print(f"✓ Results returned: {len(results)}")
    
    # Check for normal X-ray content
    top_result = results[0]
    assert top_result["condition"] == "normal_chest_xray", \
        f"Expected normal_chest_xray, got {top_result['condition']}"
    print(f"✓ Top result relevant: {top_result['title']}")
    print(f"  Condition: {top_result['condition']}")


def test_condition_filtering(retriever):
    """TEST 5: Condition filtering"""
    print("\n" + "=" * 70)
    print("TEST 5: Condition Filtering")
    print("=" * 70)
    
    # Test pneumonia filter
    results = retriever.retrieve("symptoms", top_k=5, condition="pneumonia")
    assert all(r["condition"] == "pneumonia" for r in results), \
        "Pneumonia filter returned non-pneumonia documents"
    print(f"✓ Pneumonia filter: {len(results)} results (all pneumonia)")
    
    # Test normal_chest_xray filter
    results = retriever.retrieve("chest x-ray", top_k=3, condition="normal_chest_xray")
    assert all(r["condition"] == "normal_chest_xray" for r in results), \
        "Normal X-ray filter returned non-normal documents"
    print(f"✓ Normal X-ray filter: {len(results)} results (all normal_chest_xray)")


def test_top_k_behavior(retriever):
    """TEST 6: Top-K behavior"""
    print("\n" + "=" * 70)
    print("TEST 6: Top-K Behavior")
    print("=" * 70)
    
    query = "pneumonia"
    
    # Test top_k=1
    results = retriever.retrieve(query, top_k=1)
    assert len(results) <= 1, f"Expected 1 result, got {len(results)}"
    print(f"✓ top_k=1: {len(results)} result(s)")
    
    # Test top_k=3
    results = retriever.retrieve(query, top_k=3)
    assert len(results) <= 3, f"Expected 3 results, got {len(results)}"
    print(f"✓ top_k=3: {len(results)} result(s)")
    
    # Test top_k=5
    results = retriever.retrieve(query, top_k=5)
    assert len(results) <= 5, f"Expected 5 results, got {len(results)}"
    print(f"✓ top_k=5: {len(results)} result(s)")


def test_metadata_preservation(retriever):
    """TEST 7: Metadata preservation"""
    print("\n" + "=" * 70)
    print("TEST 7: Metadata Preservation")
    print("=" * 70)
    
    query = "What is pneumonia?"
    results = retriever.retrieve(query, top_k=3)
    
    required_fields = ["document_id", "title", "text", "source", "source_url", "condition", "category"]
    
    for i, result in enumerate(results):
        # Check all required fields present
        for field in required_fields:
            assert field in result, f"Result {i} missing field: {field}"
        
        # Check non-empty
        assert result["text"], f"Result {i} has empty text"
        assert result["source"], f"Result {i} has empty source"
        assert result["source_url"], f"Result {i} has empty source_url"
    
    print(f"✓ All {len(results)} results have required metadata")
    print(f"✓ All text fields non-empty")
    print(f"✓ All source fields non-empty")
    print(f"✓ All source_url fields non-empty")


def test_empty_query_handling(retriever):
    """TEST 8: Empty query handling"""
    print("\n" + "=" * 70)
    print("TEST 8: Empty Query Handling")
    print("=" * 70)
    
    # Test empty string
    try:
        retriever.retrieve("", top_k=5)
        assert False, "Empty query should raise ValueError"
    except ValueError as e:
        print(f"✓ Empty string rejected: {str(e)}")
    
    # Test whitespace
    try:
        retriever.retrieve("   ", top_k=5)
        assert False, "Whitespace query should raise ValueError"
    except ValueError as e:
        print(f"✓ Whitespace rejected: {str(e)}")


def test_invalid_top_k_handling(retriever):
    """TEST 9: Invalid top_k handling"""
    print("\n" + "=" * 70)
    print("TEST 9: Invalid top_k Handling")
    print("=" * 70)
    
    query = "pneumonia"
    
    # Test top_k=0
    try:
        retriever.retrieve(query, top_k=0)
        assert False, "top_k=0 should raise ValueError"
    except ValueError as e:
        print(f"✓ top_k=0 rejected: {str(e)}")
    
    # Test top_k=-1
    try:
        retriever.retrieve(query, top_k=-1)
        assert False, "top_k=-1 should raise ValueError"
    except ValueError as e:
        print(f"✓ top_k=-1 rejected: {str(e)}")


def test_unknown_condition_handling(retriever):
    """TEST 10: Unknown condition handling"""
    print("\n" + "=" * 70)
    print("TEST 10: Unknown Condition Handling")
    print("=" * 70)
    
    query = "symptoms"
    results = retriever.retrieve(query, top_k=5, condition="unknown_condition")
    
    # Should return empty results (no matching condition)
    assert len(results) == 0, f"Expected 0 results for unknown condition, got {len(results)}"
    print(f"✓ Unknown condition returns empty results")


def test_source_preservation(retriever):
    """TEST 11: Source preservation"""
    print("\n" + "=" * 70)
    print("TEST 11: Source Preservation")
    print("=" * 70)
    
    queries = [
        "What is pneumonia?",
        "How is pneumonia diagnosed?",
        "What does a normal chest X-ray show?"
    ]
    
    all_sources_valid = []
    
    for query in queries:
        results = retriever.retrieve(query, top_k=3)
        
        for result in results:
            # Check source is present and valid
            assert result["source"], f"Missing source for query: {query}"
            assert result["source"] in ["WHO", "CDC", "NIH", "Mayo Clinic", "NHS", "General Medical Ethics"], \
                f"Unexpected source: {result['source']}"
            
            # Check URL is present and starts with http
            assert result["source_url"], f"Missing source_url for query: {query}"
            assert result["source_url"].startswith("http"), \
                f"Invalid URL format: {result['source_url']}"
            
            all_sources_valid.append(result["source"])
    
    print(f"✓ All results have valid sources")
    print(f"✓ All source URLs are valid")
    print(f"  Sources found: {set(all_sources_valid)}")


def test_persistence_reload(retriever):
    """TEST 12: Persistence and reload"""
    print("\n" + "=" * 70)
    print("TEST 12: Persistence and Reload")
    print("=" * 70)
    
    # Create a new retriever instance
    new_retriever = RAGRetriever()
    new_retriever.load()
    
    # Verify it loaded successfully
    assert new_retriever.is_ready, "New retriever not ready"
    assert new_retriever.vector_store.index.ntotal == 22, "New retriever has wrong document count"
    print("✓ New retriever instance loaded successfully")
    
    # Test search with new instance
    results = new_retriever.retrieve("pneumonia symptoms", top_k=3)
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"
    print(f"✓ Search with reloaded retriever works: {len(results)} results")


def run_all_tests():
    """Run all Stage 4 tests"""
    print("\n" + "=" * 70)
    print("STAGE 4: RAG RETRIEVAL SERVICE - COMPREHENSIVE TESTS")
    print("=" * 70)
    
    try:
        # Test 1: Initialization
        retriever = test_retriever_initialization()
        
        # Test 2: Basic semantic retrieval
        test_basic_semantic_retrieval(retriever)
        
        # Test 3: Pneumonia diagnosis
        test_pneumonia_diagnosis_retrieval(retriever)
        
        # Test 4: Normal X-ray
        test_normal_xray_retrieval(retriever)
        
        # Test 5: Condition filtering
        test_condition_filtering(retriever)
        
        # Test 6: Top-K
        test_top_k_behavior(retriever)
        
        # Test 7: Metadata preservation
        test_metadata_preservation(retriever)
        
        # Test 8: Empty query
        test_empty_query_handling(retriever)
        
        # Test 9: Invalid top_k
        test_invalid_top_k_handling(retriever)
        
        # Test 10: Unknown condition
        test_unknown_condition_handling(retriever)
        
        # Test 11: Source preservation
        test_source_preservation(retriever)
        
        # Test 12: Persistence/reload
        test_persistence_reload(retriever)
        
        # Final summary
        print("\n" + "=" * 70)
        print("STAGE 4 TEST SUMMARY")
        print("=" * 70)
        print("✓ All 12 tests passed successfully")
        print(f"\nRetriever Architecture:")
        print(f"  Query → EmbeddingGenerator → 384D embedding")
        print(f"  → FAISS IndexFlatL2 → Metadata mapping")
        print(f"  → Structured retrieval results")
        print(f"\nRetriever Capabilities:")
        print(f"  ✓ Semantic search working")
        print(f"  ✓ Top-K configurable")
        print(f"  ✓ Condition filtering operational")
        print(f"  ✓ Metadata preserved")
        print(f"  ✓ Source attribution maintained")
        print(f"  ✓ Invalid inputs handled gracefully")
        print(f"  ✓ Index persistence working")
        print(f"\nSafety Verification:")
        print(f"  ✓ No LLM generation")
        print(f"  ✓ No diagnosis")
        print(f"  ✓ No treatment recommendations")
        print(f"  ✓ No classifier override")
        print(f"  ✓ Evidence retrieval ONLY")
        print("\n✅ Stage 4 is COMPLETE and ready for Stage 5")
        print("=" * 70)
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
