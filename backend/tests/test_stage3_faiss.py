"""
Stage 3: FAISS Index + Embeddings - Comprehensive Tests

Tests the complete FAISS-based semantic retrieval system.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag.document_loader import MedicalKnowledgeLoader
from src.vector_db.embeddings import EmbeddingGenerator
from src.vector_db.faiss_store import FAISSVectorStore


def test_corpus_loading():
    """Test 1: Corpus loading and validation"""
    print("\n" + "=" * 70)
    print("TEST 1: Corpus Loading and Validation")
    print("=" * 70)
    
    loader = MedicalKnowledgeLoader()
    documents = loader.load()
    
    # Validate count
    assert len(documents) == 22, f"Expected 22 documents, got {len(documents)}"
    print(f"✓ Loaded 22 documents")
    
    # Validate structure
    assert loader.validate(), "Corpus validation failed"
    print(f"✓ Corpus validation passed")
    
    # Validate sources
    stats = loader.get_statistics()
    assert stats["total_documents"] == 22
    print(f"✓ Statistics confirmed: {stats['total_documents']} documents")
    
    return documents


def test_embedding_generation(documents):
    """Test 2: Embedding generation"""
    print("\n" + "=" * 70)
    print("TEST 2: Embedding Generation")
    print("=" * 70)
    
    generator = EmbeddingGenerator()
    generator.load_model()
    
    # Test model
    assert generator.model is not None, "Model not loaded"
    print(f"✓ Embedding model loaded: {generator.model_name}")
    
    # Test dimension
    dim = generator.get_dimension()
    assert dim == 384, f"Expected 384D, got {dim}D"
    print(f"✓ Embedding dimension: {dim}D")
    
    # Test single embedding
    test_text = "What are the symptoms of pneumonia?"
    embedding = generator.generate_embedding(test_text)
    assert embedding.shape[0] == 384, f"Wrong embedding shape: {embedding.shape}"
    print(f"✓ Single embedding generated: {embedding.shape}")
    
    # Test batch embeddings
    texts = [doc.text for doc in documents[:5]]
    embeddings = generator.generate_embeddings(texts, show_progress=False)
    assert embeddings.shape == (5, 384), f"Wrong batch shape: {embeddings.shape}"
    print(f"✓ Batch embeddings generated: {embeddings.shape}")
    
    # Validate all embeddings
    for emb in embeddings:
        assert generator.validate_embedding(emb), "Invalid embedding"
    print(f"✓ All embeddings validated")
    
    return generator


def test_faiss_index_building(documents, generator):
    """Test 3: FAISS index building"""
    print("\n" + "=" * 70)
    print("TEST 3: FAISS Index Building")
    print("=" * 70)
    
    store = FAISSVectorStore(embedding_generator=generator)
    store.build_index(documents, show_progress=False)
    
    # Validate index
    assert store.index is not None, "Index not created"
    assert store.index.ntotal == 22, f"Expected 22 vectors, got {store.index.ntotal}"
    print(f"✓ FAISS index created: {store.index.ntotal} vectors")
    
    # Validate metadata
    assert len(store.metadata) == 22, f"Expected 22 metadata entries, got {len(store.metadata)}"
    print(f"✓ Metadata stored: {len(store.metadata)} entries")
    
    # Validate dimension
    assert store.embedding_dim == 384, f"Expected 384D, got {store.embedding_dim}D"
    print(f"✓ Embedding dimension: {store.embedding_dim}D")
    
    # Validate index
    assert store.validate(), "Index validation failed"
    print(f"✓ Index validation passed")
    
    return store


def test_metadata_mapping(store):
    """Test 4: Metadata mapping"""
    print("\n" + "=" * 70)
    print("TEST 4: Metadata Mapping")
    print("=" * 70)
    
    # Check that all metadata has required fields
    required_fields = ["id", "title", "source", "source_url", "condition", "category", "text"]
    
    for i, meta in enumerate(store.metadata):
        for field in required_fields:
            assert field in meta, f"Metadata {i} missing field: {field}"
    
    print(f"✓ All {len(store.metadata)} metadata entries have required fields")
    
    # Check that metadata maps correctly to documents
    for i, meta in enumerate(store.metadata):
        assert len(meta["text"]) > 0, f"Empty text in metadata {i}"
        assert len(meta["source_url"]) > 0, f"Empty source URL in metadata {i}"
    
    print(f"✓ All metadata entries have non-empty text and URLs")
    
    # Check for unique IDs
    ids = [meta["id"] for meta in store.metadata]
    assert len(ids) == len(set(ids)), "Duplicate IDs in metadata"
    print(f"✓ All document IDs are unique")


def test_semantic_search(store):
    """Test 5: Semantic search"""
    print("\n" + "=" * 70)
    print("TEST 5: Semantic Search")
    print("=" * 70)
    
    test_cases = [
        {
            "query": "What are common symptoms of pneumonia?",
            "expected_condition": "pneumonia",
            "expected_category": "symptoms",
            "min_results": 3
        },
        {
            "query": "How is pneumonia diagnosed?",
            "expected_condition": "pneumonia",
            "expected_category": "diagnosis",
            "min_results": 2
        },
        {
            "query": "What does a normal chest X-ray show?",
            "expected_condition": "normal_chest_xray",
            "expected_category": "overview",
            "min_results": 2
        },
        {
            "query": "When should I seek medical attention?",
            "expected_condition": "pneumonia",
            "expected_category": "triage",
            "min_results": 1
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        results = store.search(query, top_k=5)
        
        # Check we got results
        assert len(results) >= test["min_results"], \
            f"Query {i}: Expected at least {test['min_results']} results, got {len(results)}"
        
        # Check top result relevance
        top_result = results[0]
        top_condition_matches = top_result["condition"] == test["expected_condition"]
        top_category_matches = top_result["category"] == test["expected_category"]
        
        # At least one should match for relevance
        relevant = top_condition_matches or any(
            r["condition"] == test["expected_condition"] and 
            r["category"] == test["expected_category"]
            for r in results[:3]
        )
        
        if relevant:
            print(f"✓ Query {i}: '{query}'")
            print(f"  Top result: {top_result['title']} ({top_result['condition']}/{top_result['category']})")
            print(f"  Similarity: {top_result['similarity_score']:.4f}")
        else:
            print(f"✗ Query {i}: '{query}' - relevance check failed")
            all_passed = False
    
    assert all_passed, "Some semantic search tests failed"
    print(f"\n✓ All semantic search tests passed")


def test_condition_filtering(store):
    """Test 6: Condition filtering"""
    print("\n" + "=" * 70)
    print("TEST 6: Condition Filtering")
    print("=" * 70)
    
    # Test pneumonia filter
    results = store.search("symptoms", top_k=5, condition="pneumonia")
    assert all(r["condition"] == "pneumonia" for r in results), \
        "Pneumonia filter returned non-pneumonia documents"
    print(f"✓ Pneumonia filter: {len(results)} results (all pneumonia)")
    
    # Test normal_chest_xray filter
    results = store.search("chest x-ray", top_k=3, condition="normal_chest_xray")
    assert all(r["condition"] == "normal_chest_xray" for r in results), \
        "Normal X-ray filter returned non-normal documents"
    print(f"✓ Normal X-ray filter: {len(results)} results (all normal_chest_xray)")


def test_save_load_index(store):
    """Test 7: Save and load index"""
    print("\n" + "=" * 70)
    print("TEST 7: Save and Load Index")
    print("=" * 70)
    
    # Save
    store.save_index("test_index")
    print(f"✓ Index saved")
    
    # Load into new store
    new_store = FAISSVectorStore()
    new_store.load_index("test_index")
    print(f"✓ Index loaded")
    
    # Validate loaded store
    assert new_store.index.ntotal == 22, "Loaded index has wrong count"
    assert len(new_store.metadata) == 22, "Loaded metadata has wrong count"
    assert new_store.embedding_dim == 384, "Loaded index has wrong dimension"
    print(f"✓ Loaded index validated: {new_store.index.ntotal} vectors, {new_store.embedding_dim}D")
    
    # Test search with loaded index
    results = new_store.search("pneumonia symptoms", top_k=3)
    assert len(results) == 3, "Search with loaded index failed"
    print(f"✓ Search with loaded index works: {len(results)} results")
    
    return new_store


def test_source_preservation(store):
    """Test 8: Source preservation"""
    print("\n" + "=" * 70)
    print("TEST 8: Source Preservation")
    print("=" * 70)
    
    results = store.search("What is pneumonia?", top_k=5)
    
    # Check that all results have source information
    for result in results:
        assert result["source"], "Missing source"
        assert result["source_url"], "Missing source URL"
        assert result["source"] in ["WHO", "CDC", "NIH", "Mayo Clinic", "NHS", "General Medical Ethics"], \
            f"Unexpected source: {result['source']}"
    
    print(f"✓ All {len(results)} results have valid sources")
    
    # Check URL format
    for result in results:
        url = result["source_url"]
        assert url.startswith("http"), f"Invalid URL format: {url}"
    
    print(f"✓ All source URLs are valid")


def run_all_tests():
    """Run all Stage 3 tests"""
    print("\n" + "=" * 70)
    print("STAGE 3: FAISS INDEX + EMBEDDINGS - COMPREHENSIVE TESTS")
    print("=" * 70)
    
    try:
        # Test 1: Corpus loading
        documents = test_corpus_loading()
        
        # Test 2: Embedding generation
        generator = test_embedding_generation(documents)
        
        # Test 3: FAISS index building
        store = test_faiss_index_building(documents, generator)
        
        # Test 4: Metadata mapping
        test_metadata_mapping(store)
        
        # Test 5: Semantic search
        test_semantic_search(store)
        
        # Test 6: Condition filtering
        test_condition_filtering(store)
        
        # Test 7: Save and load
        loaded_store = test_save_load_index(store)
        
        # Test 8: Source preservation
        test_source_preservation(loaded_store)
        
        # Final summary
        print("\n" + "=" * 70)
        print("STAGE 3 TEST SUMMARY")
        print("=" * 70)
        print("✓ All tests passed successfully")
        print(f"\nIndex Statistics:")
        print(f"  Documents indexed: 22")
        print(f"  Embedding dimension: 384D")
        print(f"  Embedding model: sentence-transformers/all-MiniLM-L6-v2")
        print(f"  Vector database: FAISS (IndexFlatL2)")
        print(f"  Metadata entries: 22")
        print(f"  Sources preserved: Yes")
        print(f"  Condition filtering: Working")
        print(f"  Save/Load: Working")
        print("\n✅ Stage 3 is COMPLETE and ready for Stage 4")
        print("=" * 70)
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
