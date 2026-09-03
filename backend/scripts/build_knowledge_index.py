"""
Build FAISS Knowledge Index

This script builds the FAISS vector index from the medical knowledge corpus.
Run this before starting the backend server if the intelligence layer is needed.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.vector_db.faiss_store import FAISSVectorStore
from src.rag.document_loader import MedicalKnowledgeLoader

def main():
    print("=" * 70)
    print("FAISS Knowledge Index Builder")
    print("=" * 70)
    
    # Load medical knowledge corpus
    print("\n1. Loading medical knowledge corpus...")
    corpus_path = "../data/knowledge/medical_corpus.json"  # Root data directory
    loader = MedicalKnowledgeLoader(corpus_path=corpus_path)
    documents = loader.load()
    
    print(f"✓ Loaded {len(documents)} documents")
    
    # Build FAISS index
    print("\n2. Building FAISS index...")
    index_dir = "../data/knowledge/index"  # Root data directory
    store = FAISSVectorStore(index_dir=index_dir)
    store.build_index(documents, show_progress=True)
    
    # Save index
    print("\n3. Saving index to disk...")
    store.save_index()
    
    print("\n" + "=" * 70)
    print("✓ FAISS index built successfully!")
    print("=" * 70)
    print(f"\nIndex location: {store.index_dir}")
    print(f"Total documents indexed: {len(documents)}")
    print(f"Embedding dimension: {store.embedding_dim}D")
    print("\nThe intelligence layer is now ready to use.")
    print("Restart the backend server for changes to take effect.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error building index: {e}")
        sys.exit(1)
