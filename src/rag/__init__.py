"""
RAG (Retrieval-Augmented Generation) Module

Provides document loading, embedding, retrieval, and LLM synthesis
for the Q-MedTriage Intelligence Layer.
"""

from .document_loader import MedicalKnowledgeLoader

# RAGRetriever and GeminiSynthesizer can be imported but not at module level
# to avoid circular imports
# Use: from src.rag.retriever import RAGRetriever
# Use: from src.rag.gemini_synthesizer import GeminiSynthesizer

__all__ = ["MedicalKnowledgeLoader"]
