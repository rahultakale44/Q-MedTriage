"""
RAG (Retrieval-Augmented Generation) Module

Provides document loading, embedding, and retrieval functionality
for the Q-MedTriage Intelligence Layer.
"""

from .document_loader import MedicalKnowledgeLoader
from .retriever import RAGRetriever

__all__ = ["MedicalKnowledgeLoader", "RAGRetriever"]
