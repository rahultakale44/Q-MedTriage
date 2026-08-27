"""
FAISS Vector Store

Manages FAISS index for semantic similarity search
of medical knowledge documents.
"""

import os
import json
import pickle
import numpy as np
import faiss
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vector_db.embeddings import EmbeddingGenerator
from src.rag.document_loader import MedicalDocument, MedicalKnowledgeLoader


class FAISSVectorStore:
    """
    FAISS-based vector store for semantic document retrieval
    """
    
    def __init__(
        self,
        index_dir: str = None,
        embedding_generator: EmbeddingGenerator = None
    ):
        """
        Initialize FAISS vector store
        
        Args:
            index_dir: Directory to save/load index (defaults to data/knowledge/index/)
            embedding_generator: EmbeddingGenerator instance (creates new if None)
        """
        if index_dir is None:
            index_dir = os.getenv(
                "VECTOR_DB_PATH",
                "data/knowledge/index"
            )
        
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        
        self.index = None
        self.documents = []
        self.metadata = []
        self.embedding_dim = None
    
    def build_index(
        self,
        documents: List[MedicalDocument],
        show_progress: bool = True
    ):
        """
        Build FAISS index from medical documents
        
        Args:
            documents: List of MedicalDocument objects
            show_progress: Show progress bar
        """
        if not documents:
            raise ValueError("No documents provided for indexing")
        
        print(f"\nBuilding FAISS index from {len(documents)} documents...")
        
        # Load embedding model
        self.embedding_generator.load_model()
        self.embedding_dim = self.embedding_generator.get_dimension()
        
        # Extract document texts
        texts = [doc.text for doc in documents]
        
        print(f"Generating embeddings (dim={self.embedding_dim})...")
        embeddings = self.embedding_generator.generate_embeddings(
            texts,
            show_progress=show_progress
        )
        
        # Validate embeddings
        print(f"Validating embeddings...")
        assert embeddings.shape[0] == len(documents), "Embedding count mismatch"
        assert embeddings.shape[1] == self.embedding_dim, f"Expected {self.embedding_dim}D embeddings"
        
        print(f"✓ Generated {embeddings.shape[0]} embeddings ({self.embedding_dim}D)")
        
        # Create FAISS index (L2 distance)
        print(f"Creating FAISS index...")
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Add vectors to index
        # FAISS expects float32
        embeddings_f32 = embeddings.astype('float32')
        self.index.add(embeddings_f32)
        
        print(f"✓ FAISS index created: {self.index.ntotal} vectors indexed")
        
        # Store documents and metadata
        self.documents = documents
        self.metadata = [
            {
                "id": doc.id,
                "title": doc.title,
                "source": doc.source,
                "source_url": doc.source_url,
                "condition": doc.condition,
                "category": doc.category,
                "text": doc.text,
                "keywords": doc.keywords
            }
            for doc in documents
        ]
        
        print(f"✓ Metadata stored for {len(self.metadata)} documents")
    
    def save_index(self, index_name: str = "faiss_index"):
        """
        Save FAISS index and metadata to disk
        
        Args:
            index_name: Base name for index files
        """
        if self.index is None:
            raise ValueError("No index to save. Build index first.")
        
        index_path = self.index_dir / f"{index_name}.faiss"
        metadata_path = self.index_dir / f"{index_name}_metadata.pkl"
        config_path = self.index_dir / f"{index_name}_config.json"
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        # Save configuration
        config = {
            "embedding_dim": self.embedding_dim,
            "num_documents": len(self.documents),
            "model_name": self.embedding_generator.model_name,
            "index_type": "IndexFlatL2"
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✓ Index saved to: {self.index_dir}")
        print(f"  FAISS index: {index_path.name}")
        print(f"  Metadata: {metadata_path.name}")
        print(f"  Config: {config_path.name}")
    
    def load_index(self, index_name: str = "faiss_index"):
        """
        Load FAISS index and metadata from disk
        
        Args:
            index_name: Base name for index files
        """
        index_path = self.index_dir / f"{index_name}.faiss"
        metadata_path = self.index_dir / f"{index_name}_metadata.pkl"
        config_path = self.index_dir / f"{index_name}_config.json"
        
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found: {index_path}")
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_path))
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.embedding_dim = config["embedding_dim"]
        
        print(f"✓ Index loaded from: {self.index_dir}")
        print(f"  Vectors: {self.index.ntotal}")
        print(f"  Dimension: {self.embedding_dim}D")
        print(f"  Documents: {len(self.metadata)}")
        
        # Validate
        assert self.index.ntotal == len(self.metadata), "Index/metadata count mismatch"
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        condition: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Query text
            top_k: Number of results to return
            condition: Optional condition filter (e.g., "pneumonia")
        
        Returns:
            List of result dictionaries with document metadata and scores
        """
        if self.index is None:
            raise ValueError("No index loaded. Build or load index first.")
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        query_embedding_f32 = query_embedding.astype('float32').reshape(1, -1)
        
        # Search FAISS index
        # We retrieve more than top_k to allow for filtering
        search_k = top_k * 3 if condition else top_k
        distances, indices = self.index.search(query_embedding_f32, search_k)
        
        # Build results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS returns -1 for missing results
                continue
            
            metadata = self.metadata[idx]
            
            # Apply condition filter if specified
            if condition and metadata["condition"].lower() != condition.lower():
                continue
            
            # Convert L2 distance to similarity score (inverse relationship)
            # Lower distance = higher similarity
            similarity_score = 1.0 / (1.0 + distance)
            
            result = {
                "rank": len(results) + 1,
                "document_id": metadata["id"],
                "title": metadata["title"],
                "source": metadata["source"],
                "source_url": metadata["source_url"],
                "condition": metadata["condition"],
                "category": metadata["category"],
                "text": metadata["text"],
                "keywords": metadata["keywords"],
                "distance": float(distance),
                "similarity_score": float(similarity_score)
            }
            
            results.append(result)
            
            if len(results) >= top_k:
                break
        
        return results
    
    def validate(self) -> bool:
        """
        Validate index integrity
        
        Returns:
            True if valid, False otherwise
        """
        if self.index is None:
            print("✗ No index loaded")
            return False
        
        if not self.metadata:
            print("✗ No metadata loaded")
            return False
        
        if self.index.ntotal != len(self.metadata):
            print(f"✗ Index/metadata count mismatch: {self.index.ntotal} != {len(self.metadata)}")
            return False
        
        if self.embedding_dim is None:
            print("✗ Embedding dimension not set")
            return False
        
        # Check embedding dimension
        expected_dim = 384  # all-MiniLM-L6-v2
        if self.embedding_dim != expected_dim:
            print(f"✗ Unexpected embedding dimension: {self.embedding_dim} (expected {expected_dim})")
            return False
        
        print(f"✓ Index validation passed")
        print(f"  Vectors: {self.index.ntotal}")
        print(f"  Metadata: {len(self.metadata)}")
        print(f"  Dimension: {self.embedding_dim}D")
        
        return True
    
    def get_statistics(self) -> Dict:
        """
        Get index statistics
        
        Returns:
            Dictionary with statistics
        """
        if self.index is None:
            return {"error": "No index loaded"}
        
        return {
            "num_vectors": self.index.ntotal,
            "embedding_dim": self.embedding_dim,
            "num_metadata": len(self.metadata),
            "index_type": "IndexFlatL2",
            "model_name": self.embedding_generator.model_name
        }


# ============================================================================
# STANDALONE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FAISS Vector Store - Build & Test")
    print("=" * 70)
    
    # Load medical corpus
    print("\n1. Loading medical corpus...")
    loader = MedicalKnowledgeLoader()
    documents = loader.load()
    
    if not loader.validate():
        print("✗ Corpus validation failed")
        exit(1)
    
    # Build index
    print("\n2. Building FAISS index...")
    store = FAISSVectorStore()
    store.build_index(documents, show_progress=True)
    
    # Validate
    print("\n3. Validating index...")
    if not store.validate():
        print("✗ Index validation failed")
        exit(1)
    
    # Save index
    print("\n4. Saving index...")
    store.save_index()
    
    # Test search
    print("\n5. Testing semantic search...")
    test_queries = [
        "What are common symptoms of pneumonia?",
        "How is pneumonia diagnosed?",
        "What are warning signs that require urgent medical attention?",
        "What does a normal chest X-ray indicate?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: '{query}'")
        print(f"{'='*70}")
        
        results = store.search(query, top_k=3)
        
        for result in results:
            print(f"\n[{result['rank']}] {result['title']}")
            print(f"    Source: {result['source']}")
            print(f"    Condition: {result['condition']}")
            print(f"    Category: {result['category']}")
            print(f"    Similarity: {result['similarity_score']:.4f}")
            print(f"    Text: {result['text'][:150]}...")
    
    # Test condition filtering
    print(f"\n{'='*70}")
    print("Test: Condition filtering (pneumonia only)")
    print(f"{'='*70}")
    results = store.search("symptoms", top_k=3, condition="pneumonia")
    print(f"Found {len(results)} results for condition='pneumonia'")
    for result in results:
        print(f"  - {result['title']} ({result['condition']})")
    
    # Statistics
    print(f"\n{'='*70}")
    print("Index Statistics")
    print(f"{'='*70}")
    stats = store.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("FAISS Vector Store test complete")
    print("=" * 70)
