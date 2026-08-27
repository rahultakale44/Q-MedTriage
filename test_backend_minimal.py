"""
Minimal backend for testing /ask endpoint without ML pipeline
This bypasses the Qiskit import issue
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Loaded environment from {env_path}")
except ImportError:
    print("⚠ python-dotenv not installed")

app = FastAPI(
    title="Q-MedTriage Test API",
    version="0.3.0",
    description="Minimal test server for intelligence layer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("=" * 70)
print("Initializing Q-MedTriage Test API (Intelligence Layer Only)")
print("=" * 70)

# Initialize Intelligence Layer only
rag_retriever = None
gemini_synthesizer = None
INTELLIGENCE_ENABLED = False

try:
    from src.rag.retriever import RAGRetriever
    from src.rag.gemini_synthesizer import GeminiSynthesizer
    
    print("\n" + "-" * 70)
    print("Intelligence Layer Initialization")
    print("-" * 70)
    
    # Initialize RAG retriever
    rag_retriever = RAGRetriever()
    rag_retriever.load()
    print("✓ RAG retriever ready")
    
    # Initialize Gemini synthesizer
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        gemini_synthesizer = GeminiSynthesizer()
        gemini_synthesizer.initialize()
        print("✓ Gemini synthesizer ready")
        INTELLIGENCE_ENABLED = True
    else:
        print("✗ GEMINI_API_KEY not configured")
        
except Exception as e:
    print(f"✗ Intelligence layer initialization failed: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
print(f"Intelligence Layer Enabled: {INTELLIGENCE_ENABLED}")
print("=" * 70)


@app.get("/")
def root():
    return {
        "name": "Q-MedTriage Test API",
        "status": "online",
        "intelligence_enabled": INTELLIGENCE_ENABLED
    }


@app.get("/health")
def health():
    return {
        "api": "online",
        "rag_retriever": "ready" if (rag_retriever and rag_retriever.is_ready) else "unavailable",
        "gemini_synthesizer": "ready" if (gemini_synthesizer and gemini_synthesizer.is_ready) else "unavailable",
        "intelligence_enabled": INTELLIGENCE_ENABLED
    }


@app.post("/ask")
async def ask(question: str):
    """
    Q&A endpoint for medical questions
    """
    # Check if intelligence layer is available
    if not INTELLIGENCE_ENABLED:
        return {
            "question": question,
            "answer": (
                "The Q&A service is currently unavailable. "
                "Please ensure GEMINI_API_KEY is configured."
            ),
            "sources": [],
            "success": False,
            "error": "Intelligence layer not available"
        }
    
    # Validate question
    if not question or not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        print(f"\n[RAG] Query received: '{question}'")
        
        # Step 1: Retrieve relevant medical evidence
        print(f"[RAG] Retrieving evidence...")
        retrieved_results = rag_retriever.retrieve(
            query=question,
            top_k=5
        )
        print(f"[RAG] Retrieved {len(retrieved_results)} documents")
        
        # Step 2: Synthesize response using Gemini
        print(f"[LLM] Generating explanation...")
        synthesis_result = gemini_synthesizer.synthesize(
            query=question,
            retrieved_results=retrieved_results
        )
        print(f"[LLM] Response generated: {synthesis_result['success']}")
        
        # Return response
        return {
            "question": question,
            "answer": synthesis_result.get("answer"),
            "sources": synthesis_result.get("sources", []),
            "disclaimer": synthesis_result.get("disclaimer"),
            "success": synthesis_result.get("success", False),
            "retrieved_count": len(retrieved_results)
        }
        
    except Exception as e:
        print(f"[ERROR] Q&A failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "question": question,
            "answer": (
                "I encountered an error while retrieving information. "
                "Please try again or rephrase your question."
            ),
            "sources": [],
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
