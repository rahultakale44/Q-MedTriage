"""
Embedding Generation

Generates semantic embeddings using sentence-transformers
for the medical knowledge corpus.
"""

import os
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates embeddings for text using sentence-transformers
    
    Uses all-MiniLM-L6-v2 model (384 dimensions) for semantic similarity.
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the embedding generator
        
        Args:
            model_name: Name of the sentence-transformers model
                       (defaults to sentence-transformers/all-MiniLM-L6-v2)
        """
        # Use environment variable or default
        if model_name is None:
            model_name = os.getenv(
                "EMBEDDING_MODEL", 
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        
        self.model_name = model_name
        self.model = None
        self.embedding_dim = None
    
    def load_model(self):
        """
        Load the sentence-transformers model
        
        Note: First-time usage will download the model (~90MB)
        """
        if self.model is not None:
            print(f"✓ Embedding model already loaded: {self.model_name}")
            return
        
        print(f"Loading embedding model: {self.model_name}")
        print("  (First-time usage will download ~90MB model)")
        
        try:
            self.model = SentenceTransformer(self.model_name)
            
            # Determine embedding dimension
            test_embedding = self.model.encode("test", convert_to_numpy=True)
            self.embedding_dim = test_embedding.shape[0]
            
            print(f"✓ Embedding model loaded successfully")
            print(f"  Model: {self.model_name}")
            print(f"  Dimension: {self.embedding_dim}D")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load embedding model: {e}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector (384D for all-MiniLM-L6-v2)
        """
        if self.model is None:
            self.load_model()
        
        embedding = self.model.encode(
            text, 
            convert_to_numpy=True,
            show_progress_bar=False
        )
        
        return embedding
    
    def generate_embeddings(
        self, 
        texts: List[str], 
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            batch_size: Batch size for encoding
            show_progress: Show progress bar
        
        Returns:
            Array of embeddings (N x 384)
        """
        if self.model is None:
            self.load_model()
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=show_progress
        )
        
        return embeddings
    
    def get_dimension(self) -> int:
        """
        Get embedding dimension
        
        Returns:
            Embedding dimension (384 for all-MiniLM-L6-v2)
        """
        if self.embedding_dim is None:
            if self.model is None:
                self.load_model()
        
        return self.embedding_dim
    
    def validate_embedding(self, embedding: np.ndarray) -> bool:
        """
        Validate that an embedding has the correct dimension
        
        Args:
            embedding: Embedding vector to validate
        
        Returns:
            True if valid, False otherwise
        """
        expected_dim = self.get_dimension()
        
        if embedding.ndim == 1:
            actual_dim = embedding.shape[0]
        elif embedding.ndim == 2:
            actual_dim = embedding.shape[1]
        else:
            print(f"✗ Invalid embedding shape: {embedding.shape}")
            return False
        
        if actual_dim != expected_dim:
            print(f"✗ Embedding dimension mismatch: {actual_dim} != {expected_dim}")
            return False
        
        return True


# ============================================================================
# STANDALONE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Embedding Generator - Test")
    print("=" * 70)
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Test single embedding
    print("\nTest 1: Single embedding")
    test_text = "What are the symptoms of pneumonia?"
    embedding = generator.generate_embedding(test_text)
    
    print(f"✓ Generated embedding for: '{test_text}'")
    print(f"  Dimension: {embedding.shape[0]}")
    print(f"  Sample values: {embedding[:5]}")
    
    # Validate
    if generator.validate_embedding(embedding):
        print(f"✓ Embedding validation passed")
    
    # Test batch embeddings
    print("\nTest 2: Batch embeddings")
    test_texts = [
        "What is pneumonia?",
        "How is pneumonia diagnosed?",
        "What are the risk factors for pneumonia?",
        "How is pneumonia treated?",
        "What does a normal chest X-ray show?"
    ]
    
    embeddings = generator.generate_embeddings(test_texts, show_progress=False)
    
    print(f"✓ Generated {len(embeddings)} embeddings")
    print(f"  Shape: {embeddings.shape}")
    print(f"  Expected: ({len(test_texts)}, {generator.get_dimension()})")
    
    # Validate all
    all_valid = all(generator.validate_embedding(emb) for emb in embeddings)
    if all_valid:
        print(f"✓ All embeddings valid ({generator.get_dimension()}D)")
    
    # Test semantic similarity
    print("\nTest 3: Semantic similarity")
    from numpy.linalg import norm
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (norm(a) * norm(b))
    
    query = "pneumonia symptoms"
    query_emb = generator.generate_embedding(query)
    
    print(f"Query: '{query}'")
    print("Similarity scores:")
    for i, text in enumerate(test_texts):
        sim = cosine_similarity(query_emb, embeddings[i])
        print(f"  {sim:.4f} - {text}")
    
    print("\n" + "=" * 70)
    print("Embedding Generator test complete")
    print("=" * 70)
