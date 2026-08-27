"""
Medical Knowledge Document Loader

Loads and validates the medical knowledge corpus from JSON.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class MedicalDocument:
    """Represents a single medical knowledge document"""
    id: str
    condition: str
    category: str
    title: str
    source: str
    source_url: str
    text: str
    keywords: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "condition": self.condition,
            "category": self.category,
            "title": self.title,
            "source": self.source,
            "source_url": self.source_url,
            "text": self.text,
            "keywords": self.keywords
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "MedicalDocument":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            condition=data["condition"],
            category=data["category"],
            title=data["title"],
            source=data["source"],
            source_url=data["source_url"],
            text=data["text"],
            keywords=data.get("keywords", [])
        )


class MedicalKnowledgeLoader:
    """
    Loads and manages the medical knowledge corpus
    """
    
    def __init__(self, corpus_path: Optional[str] = None):
        """
        Initialize the document loader
        
        Args:
            corpus_path: Path to the medical corpus JSON file
                        (defaults to data/knowledge/medical_corpus.json)
        """
        if corpus_path is None:
            corpus_path = "data/knowledge/medical_corpus.json"
        
        self.corpus_path = Path(corpus_path)
        self.documents: List[MedicalDocument] = []
        self.metadata: Dict = {}
    
    def load(self) -> List[MedicalDocument]:
        """
        Load the medical knowledge corpus
        
        Returns:
            List of MedicalDocument objects
        
        Raises:
            FileNotFoundError: If corpus file doesn't exist
            ValueError: If corpus is invalid
        """
        if not self.corpus_path.exists():
            raise FileNotFoundError(
                f"Medical corpus not found: {self.corpus_path}\n"
                f"Please ensure the knowledge base has been created."
            )
        
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract metadata
            self.metadata = {
                "version": data.get("version", "unknown"),
                "created_date": data.get("created_date", "unknown"),
                "description": data.get("description", ""),
                "sources": data.get("sources", []),
                "conditions": data.get("conditions", [])
            }
            
            # Load documents
            raw_docs = data.get("documents", [])
            if not raw_docs:
                raise ValueError("No documents found in corpus")
            
            self.documents = [
                MedicalDocument.from_dict(doc) 
                for doc in raw_docs
            ]
            
            print(f"✓ Loaded {len(self.documents)} medical documents")
            print(f"  Sources: {', '.join(self.metadata['sources'])}")
            print(f"  Conditions: {', '.join(self.metadata['conditions'])}")
            
            return self.documents
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in corpus file: {e}")
        except KeyError as e:
            raise ValueError(f"Missing required field in corpus: {e}")
    
    def get_by_condition(self, condition: str) -> List[MedicalDocument]:
        """
        Get documents for a specific condition
        
        Args:
            condition: Condition name (e.g., "pneumonia")
        
        Returns:
            List of matching documents
        """
        return [
            doc for doc in self.documents 
            if doc.condition.lower() == condition.lower()
        ]
    
    def get_by_category(self, category: str) -> List[MedicalDocument]:
        """
        Get documents for a specific category
        
        Args:
            category: Category name (e.g., "symptoms", "treatment")
        
        Returns:
            List of matching documents
        """
        return [
            doc for doc in self.documents 
            if doc.category.lower() == category.lower()
        ]
    
    def get_by_source(self, source: str) -> List[MedicalDocument]:
        """
        Get documents from a specific source
        
        Args:
            source: Source name (e.g., "WHO", "CDC")
        
        Returns:
            List of matching documents
        """
        return [
            doc for doc in self.documents 
            if doc.source.upper() == source.upper()
        ]
    
    def validate(self) -> bool:
        """
        Validate the loaded corpus
        
        Returns:
            True if valid, False otherwise
        """
        if not self.documents:
            print("✗ No documents loaded")
            return False
        
        required_fields = ["id", "condition", "category", "title", "source", "text"]
        
        for i, doc in enumerate(self.documents):
            for field in required_fields:
                if not getattr(doc, field):
                    print(f"✗ Document {i} missing required field: {field}")
                    return False
        
        # Check for duplicate IDs
        ids = [doc.id for doc in self.documents]
        if len(ids) != len(set(ids)):
            print("✗ Duplicate document IDs found")
            return False
        
        print(f"✓ Corpus validation passed ({len(self.documents)} documents)")
        return True
    
    def get_document_by_id(self, doc_id: str) -> Optional[MedicalDocument]:
        """
        Get a specific document by ID
        
        Args:
            doc_id: Document ID
        
        Returns:
            MedicalDocument or None if not found
        """
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None
    
    def get_statistics(self) -> Dict:
        """
        Get corpus statistics
        
        Returns:
            Dictionary with statistics
        """
        if not self.documents:
            return {"error": "No documents loaded"}
        
        conditions = {}
        categories = {}
        sources = {}
        
        for doc in self.documents:
            conditions[doc.condition] = conditions.get(doc.condition, 0) + 1
            categories[doc.category] = categories.get(doc.category, 0) + 1
            sources[doc.source] = sources.get(doc.source, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "conditions": conditions,
            "categories": categories,
            "sources": sources,
            "avg_text_length": sum(len(doc.text) for doc in self.documents) / len(self.documents)
        }


# ============================================================================
# STANDALONE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Medical Knowledge Loader - Test")
    print("=" * 70)
    
    loader = MedicalKnowledgeLoader()
    
    try:
        # Load corpus
        documents = loader.load()
        
        # Validate
        if loader.validate():
            print("\n" + "=" * 70)
            print("Corpus Statistics")
            print("=" * 70)
            stats = loader.get_statistics()
            print(f"\nTotal documents: {stats['total_documents']}")
            print(f"Average text length: {stats['avg_text_length']:.0f} characters")
            
            print("\nDocuments by condition:")
            for condition, count in stats['conditions'].items():
                print(f"  {condition}: {count}")
            
            print("\nDocuments by source:")
            for source, count in stats['sources'].items():
                print(f"  {source}: {count}")
            
            # Show sample document
            if documents:
                print("\n" + "=" * 70)
                print("Sample Document")
                print("=" * 70)
                sample = documents[0]
                print(f"ID: {sample.id}")
                print(f"Title: {sample.title}")
                print(f"Source: {sample.source}")
                print(f"Condition: {sample.condition}")
                print(f"Category: {sample.category}")
                print(f"Text: {sample.text[:200]}...")
                print(f"URL: {sample.source_url}")
        else:
            print("\n✗ Corpus validation failed")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
