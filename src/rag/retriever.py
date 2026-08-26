"""
RAG Retrieval Service

Provides semantic retrieval of medical knowledge documents using FAISS.
This is the retrieval layer only - no LLM generation or clinical conclusions.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vector_db.embeddings import EmbeddingGenerator
from src.vector_db.faiss_store import FAISSVectorStore


class RAGRetriever:
    """
    Retrieval-Augmented Generation (RAG) Retriever
    
    Loads persisted FAISS index and provides semantic retrieval
    of medical knowledge documents.
    
    IMPORTANT: This is ONLY the retrieval layer. It does NOT:
    - Generate answers
    - Call LLMs
    - Diagnose patients
    - Provide medical advice
    - Override classifier predictions
    - Make treatment recommendations
    
    It ONLY retrieves relevant evidence from the medical knowledge corpus.
    """
    
    def __init__(
        self,
        index_dir: str = None,
        index_name: str = "faiss_index"
    ):
        """
        Initialize RAG retriever
        
        Args:
            index_dir: Directory containing FAISS index
                      (defaults to data/knowledge/index/)
            index_name: Base name of index files
                       (defaults to "faiss_index")
        """
        if index_dir is None:
            index_dir = os.getenv(
                "VECTOR_DB_PATH",
                "data/knowledge/index"
            )
        
        self.index_dir = Path(index_dir)
        self.index_name = index_name
        
        # Initialize components
        self.embedding_generator = None
        self.vector_store = None
        self.is_ready = False
    
    def load(self):
        """
        Load FAISS index and initialize retriever
        
        This loads the persisted index from disk. It does NOT rebuild
        the index from scratch.
        
        Raises:
            FileNotFoundError: If index files don't exist
            ValueError: If index is invalid
        """
        print("\n" + "=" * 70)
        print("Initializing RAG Retriever")
        print("=" * 70)
        
        # Initialize embedding generator
        print("\n1. Loading embedding model...")
        self.embedding_generator = EmbeddingGenerator()
        self.embedding_generator.load_model()
        
        # Verify dimension
        embedding_dim = self.embedding_generator.get_dimension()
        if embedding_dim != 384:
            raise ValueError(
                f"Unexpected embedding dimension: {embedding_dim} "
                f"(expected 384D for all-MiniLM-L6-v2)"
            )
        print(f"✓ Embedding model ready: {embedding_dim}D")
        
        # Initialize vector store with existing embedding generator
        print("\n2. Loading FAISS index...")
        self.vector_store = FAISSVectorStore(
            index_dir=str(self.index_dir),
            embedding_generator=self.embedding_generator
        )
        
        # Load persisted index
        self.vector_store.load_index(self.index_name)
        
        # Validate
        print("\n3. Validating index...")
        if not self.vector_store.validate():
            raise ValueError("Index validation failed")
        
        self.is_ready = True
        
        print("\n" + "=" * 70)
        print("RAG Retriever Ready")
        print("=" * 70)
        print(f"  Index: {self.index_dir}/{self.index_name}")
        print(f"  Documents: {self.vector_store.index.ntotal}")
        print(f"  Dimension: {embedding_dim}D")
        print(f"  Model: {self.embedding_generator.model_name}")
        print("=" * 70)
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        condition: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve relevant medical documents for a query
        
        This method ONLY retrieves evidence. It does NOT:
        - Generate answers
        - Make diagnoses
        - Provide medical conclusions
        - Override classifier predictions
        
        Args:
            query: User query (e.g., "What are symptoms of pneumonia?")
            top_k: Number of results to return (default: 5)
            condition: Optional condition filter (e.g., "pneumonia")
        
        Returns:
            List of retrieved documents with metadata:
            - document_id: Document ID
            - title: Document title
            - text: Full document text
            - source: Source (WHO, CDC, NIH, Mayo Clinic, etc.)
            - source_url: Original source URL
            - condition: Medical condition
            - category: Document category
            - distance: L2 distance from query
            - similarity_score: Similarity score (0-1)
            - rank: Result ranking (1-based)
        
        Raises:
            ValueError: If retriever not initialized, query invalid, or top_k invalid
        """
        # Validate retriever is ready
        if not self.is_ready:
            raise ValueError(
                "Retriever not initialized. Call load() first."
            )
        
        # Validate query
        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty. Please provide a valid query string."
            )
        
        query = query.strip()
        
        # Validate top_k
        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError(
                f"top_k must be a positive integer, got: {top_k}"
            )
        
        # Cap top_k at available documents
        max_docs = self.vector_store.index.ntotal
        if top_k > max_docs:
            top_k = max_docs
        
        # Use vector store's search method
        # (which handles embedding, FAISS search, and metadata mapping)
        results = self.vector_store.search(
            query=query,
            top_k=top_k,
            condition=condition
        )
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Get retriever statistics
        
        Returns:
            Dictionary with statistics
        """
        if not self.is_ready:
            return {"error": "Retriever not initialized"}
        
        return {
            "ready": self.is_ready,
            "index_dir": str(self.index_dir),
            "num_documents": self.vector_store.index.ntotal,
            "embedding_dim": self.embedding_generator.get_dimension(),
            "embedding_model": self.embedding_generator.model_name,
            "index_type": "FAISS IndexFlatL2"
        }


# ============================================================================
# STANDALONE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RAG Retriever - Demonstration")
    print("=" * 70)
    
    try:
        # Initialize retriever
        retriever = RAGRetriever()
        retriever.load()
        
        # Test queries
        test_queries = [
            "What are common symptoms of pneumonia?",
            "How is pneumonia diagnosed?",
            "What are warning signs that require urgent medical attention?",
            "What does a normal chest X-ray indicate?",
            "What are the limitations of chest X-rays?"
        ]
        
        for query in test_queries:
            print("\n" + "=" * 70)
            print(f"Query: '{query}'")
            print("=" * 70)
            
            results = retriever.retrieve(query, top_k=3)
            
            for result in results:
                print(f"\n[{result['rank']}] {result['title']}")
                print(f"    Source: {result['source']}")
                print(f"    Condition: {result['condition']}")
                print(f"    Category: {result['category']}")
                print(f"    Similarity: {result['similarity_score']:.4f}")
                print(f"    Distance: {result['distance']:.4f}")
                print(f"    Text: {result['text'][:150]}...")
                print(f"    URL: {result['source_url']}")
        
        # Test condition filtering
        print("\n" + "=" * 70)
        print("Test: Condition filtering (pneumonia only)")
        print("=" * 70)
        results = retriever.retrieve("symptoms", top_k=3, condition="pneumonia")
        print(f"Found {len(results)} results for condition='pneumonia'")
        for result in results:
            print(f"  - {result['title']} ({result['condition']})")
        
        # Display statistics
        print("\n" + "=" * 70)
        print("Retriever Statistics")
        print("=" * 70)
        stats = retriever.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n" + "=" * 70)
        print("RAG Retriever demonstration complete")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
