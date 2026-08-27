"""
Vector Database Module

Provides embedding generation and FAISS-based vector storage
for semantic retrieval in the Q-MedTriage Intelligence Layer.
"""

from .embeddings import EmbeddingGenerator
from .faiss_store import FAISSVectorStore

__all__ = ["EmbeddingGenerator", "FAISSVectorStore"]
