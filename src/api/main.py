from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.inference.predict import ChestXRayInference

# Intelligence Layer (Phase 2) imports
try:
    from src.rag.retriever import RAGRetriever
    from src.rag.gemini_synthesizer import GeminiSynthesizer
    INTELLIGENCE_IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Intelligence layer imports failed: {e}")
    INTELLIGENCE_IMPORTS_AVAILABLE = False
    RAGRetriever = None
    GeminiSynthesizer = None

app = FastAPI(
    title="Q-MedTriage API",
    version="0.2.0",
    description="Quantum-assisted medical image triage backend with RAG intelligence layer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize inference pipeline (loaded once at startup)
print("=" * 70)
print("Initializing Q-MedTriage API")
print("=" * 70)

# Phase 1: Image Classification
try:
    inference_pipeline = ChestXRayInference()
    PIPELINE_LOADED = True
    print("✓ Phase 1: Inference pipeline ready")
except Exception as e:
    print(f"✗ Failed to load inference pipeline: {e}")
    PIPELINE_LOADED = False
    inference_pipeline = None

# Phase 2: Intelligence Layer (RAG + Gemini)
rag_retriever = None
gemini_synthesizer = None
INTELLIGENCE_ENABLED = False

if INTELLIGENCE_IMPORTS_AVAILABLE:
    # Check if intelligence layer is enabled
    intelligence_enabled_config = os.getenv("INTELLIGENCE_ENABLED", "true").lower() == "true"
    
    if intelligence_enabled_config:
        try:
            # Initialize RAG retriever
            print("\n" + "-" * 70)
            print("Phase 2: Intelligence Layer Initialization")
            print("-" * 70)
            
            rag_retriever = RAGRetriever()
            rag_retriever.load()
            print("✓ Phase 2: RAG retriever ready")
            
            # Initialize Gemini synthesizer (requires API key)
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if gemini_api_key:
                gemini_synthesizer = GeminiSynthesizer()
                gemini_synthesizer.initialize()
                print("✓ Phase 2: Gemini synthesizer ready")
                INTELLIGENCE_ENABLED = True
            else:
                print("⚠ Phase 2: GEMINI_API_KEY not configured")
                print("  Intelligence layer will be unavailable")
                print("  Set GEMINI_API_KEY in .env to enable")
                
        except Exception as e:
            print(f"⚠ Phase 2: Intelligence layer initialization failed: {e}")
            print("  /intelligence endpoint will return errors")
            rag_retriever = None
            gemini_synthesizer = None
    else:
        print("\nPhase 2: Intelligence layer disabled (INTELLIGENCE_ENABLED=false)")
else:
    print("\nPhase 2: Intelligence layer not available (import failed)")

print("=" * 70)


@app.get("/")
def root():
    return {
        "name": "Q-MedTriage",
        "status": "online",
        "version": "0.1.0",
        "pipeline_ready": PIPELINE_LOADED
    }


@app.get("/health")
def health():
    quantum_available = (
        PIPELINE_LOADED and 
        hasattr(inference_pipeline, 'quantum_model') and 
        inference_pipeline.quantum_model is not None
    )
    
    return {
        "api": "online",
        "vision_model": "ready" if PIPELINE_LOADED else "failed",
        "classical_svm": "ready" if PIPELINE_LOADED else "failed",
        "quantum_svm": "ready" if quantum_available else "unavailable",
        "rag_retriever": "ready" if (rag_retriever and rag_retriever.is_ready) else "unavailable",
        "gemini_synthesizer": "ready" if (gemini_synthesizer and gemini_synthesizer.is_ready) else "unavailable",
        "intelligence_enabled": INTELLIGENCE_ENABLED,
        "pipeline_loaded": PIPELINE_LOADED
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...), classifier: str = "classical"):
    """
    Predict pneumonia from chest X-ray image
    
    Args:
        file: Uploaded chest X-ray image
        classifier: "classical" (default) or "quantum"
    
    Returns:
        JSON with prediction, confidence, probabilities, and disclaimer
    """
    # Validate classifier parameter
    if classifier not in ["classical", "quantum"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'"
        )
    
    # Check if pipeline is loaded
    if not PIPELINE_LOADED:
        raise HTTPException(
            status_code=503,
            detail="Inference pipeline not available"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Must be an image."
        )
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Run inference with selected classifier
        result = inference_pipeline.predict(image, classifier=classifier, include_features=False)
        
        if not result["success"]:
            # Handle specific error cases
            if result.get("error_type") == "ModelNotAvailableError":
                raise HTTPException(
                    status_code=503,
                    detail=f"Quantum SVM model not available"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Prediction failed: {result.get('error', 'Unknown error')}"
            )
        
        # Add filename and classifier to response
        result["filename"] = file.filename
        result["classifier"] = classifier
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.post("/intelligence")
async def intelligence(file: UploadFile = File(...), classifier: str = "classical"):
    """
    Comprehensive intelligence endpoint: Image classification + Evidence retrieval + Explanation synthesis
    
    This endpoint integrates:
    - Phase 1: Image classification (ResNet50 → PCA → Classical/Quantum SVM)
    - Phase 2: RAG evidence retrieval (FAISS similarity search)
    - Phase 2: Gemini evidence-grounded synthesis
    
    Args:
        file: Uploaded chest X-ray image
        classifier: "classical" (default) or "quantum"
    
    Returns:
        JSON with:
        - prediction: Classifier result (condition, confidence, probabilities)
        - intelligence: Evidence-grounded explanation (answer, sources, disclaimer)
        - retrieval: Retrieval metadata
        - success: Overall operation status
    
    SAFETY GUARANTEES:
    - Classifier prediction is authoritative (never overridden)
    - Gemini synthesis is evidence-only (no diagnosis/treatment)
    - All sources are from authoritative medical organizations
    - Medical disclaimer is mandatory
    """
    # Check if intelligence layer is available
    if not INTELLIGENCE_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="Intelligence layer not available. Check GEMINI_API_KEY configuration."
        )
    
    # Validate classifier parameter
    if classifier not in ["classical", "quantum"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'"
        )
    
    # Check if pipeline is loaded
    if not PIPELINE_LOADED:
        raise HTTPException(
            status_code=503,
            detail="Inference pipeline not available"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Must be an image."
        )
    
    try:
        # ====================================================================
        # STEP 1: RUN PHASE 1 CLASSIFIER
        # ====================================================================
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Run inference with selected classifier
        classifier_result = inference_pipeline.predict(image, classifier=classifier, include_features=False)
        
        if not classifier_result["success"]:
            # Handle specific error cases
            if classifier_result.get("error_type") == "ModelNotAvailableError":
                raise HTTPException(
                    status_code=503,
                    detail=f"Quantum SVM model not available"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Classification failed: {classifier_result.get('error', 'Unknown error')}"
            )
        
        # Extract prediction details
        predicted_label = classifier_result["prediction_label"]
        confidence = classifier_result.get("confidence")
        probabilities = classifier_result.get("probabilities")
        
        # ====================================================================
        # STEP 2: MAP CLASSIFIER RESULT TO KNOWLEDGE CONDITION
        # ====================================================================
        
        # Map classifier label to knowledge base condition
        condition_mapping = {
            "PNEUMONIA": "pneumonia",
            "NORMAL": "normal_chest_xray"
        }
        
        knowledge_condition = condition_mapping.get(predicted_label)
        
        if not knowledge_condition:
            raise HTTPException(
                status_code=500,
                detail=f"Unknown classifier label: {predicted_label}"
            )
        
        # ====================================================================
        # STEP 3: CREATE RETRIEVAL QUERY
        # ====================================================================
        
        # Construct retrieval query based on prediction
        if knowledge_condition == "pneumonia":
            retrieval_query = "medical information about pneumonia diagnosis symptoms treatment"
        else:  # normal_chest_xray
            retrieval_query = "normal chest x-ray findings healthy lungs"
        
        # ====================================================================
        # STEP 4: RUN STAGE 4 RAG RETRIEVAL
        # ====================================================================
        
        try:
            retrieved_evidence = rag_retriever.retrieve(
                query=retrieval_query,
                top_k=5,
                condition=knowledge_condition
            )
            
            retrieval_success = True
            retrieval_error = None
            
        except Exception as e:
            print(f"Retrieval error: {e}")
            retrieved_evidence = []
            retrieval_success = False
            retrieval_error = str(e)
        
        # ====================================================================
        # STEP 5: RUN STAGE 5 GEMINI SYNTHESIS
        # ====================================================================
        
        synthesis_result = None
        synthesis_success = False
        
        if retrieved_evidence:
            try:
                synthesis_result = gemini_synthesizer.synthesize(
                    query=retrieval_query,
                    retrieved_results=retrieved_evidence
                )
                synthesis_success = synthesis_result.get("success", False)
                
            except Exception as e:
                print(f"Synthesis error: {e}")
                synthesis_result = {
                    "success": False,
                    "error": str(e),
                    "answer": "The explanation service could not complete the response.",
                    "sources": [],
                    "disclaimer": GeminiSynthesizer.MEDICAL_DISCLAIMER,
                    "retrieved_count": len(retrieved_evidence)
                }
                synthesis_success = False
        else:
            # No evidence retrieved - cannot synthesize
            synthesis_result = {
                "success": False,
                "error": retrieval_error or "No evidence retrieved",
                "answer": "Insufficient medical evidence available to provide explanation.",
                "sources": [],
                "disclaimer": GeminiSynthesizer.MEDICAL_DISCLAIMER,
                "retrieved_count": 0
            }
            synthesis_success = False
        
        # ====================================================================
        # STEP 6: BUILD STRUCTURED RESPONSE
        # ====================================================================
        
        response = {
            "success": classifier_result["success"] and retrieval_success and synthesis_success,
            "filename": file.filename,
            "classifier": classifier,
            
            # Phase 1: Classifier prediction
            "prediction": {
                "condition": predicted_label,
                "confidence": confidence,
                "probabilities": probabilities,
                "model": classifier_result["model"],
                "model_type": classifier_result["model_type"],
                "inference_time_ms": classifier_result["inference_time_ms"]
            },
            
            # Phase 2: Intelligence layer
            "intelligence": {
                "answer": synthesis_result.get("answer"),
                "sources": synthesis_result.get("sources", []),
                "disclaimer": synthesis_result.get("disclaimer"),
                "model": synthesis_result.get("model") if synthesis_success else None
            },
            
            # Retrieval metadata
            "retrieval": {
                "query": retrieval_query,
                "condition_filter": knowledge_condition,
                "retrieved_count": len(retrieved_evidence),
                "success": retrieval_success
            },
            
            # Classifier disclaimer (always present)
            "classifier_disclaimer": classifier_result.get("disclaimer")
        }
        
        # Add errors if any component failed
        if not retrieval_success:
            response["retrieval"]["error"] = retrieval_error
        
        if not synthesis_success:
            response["intelligence"]["error"] = synthesis_result.get("error")
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        # Controlled error response
        raise HTTPException(
            status_code=500,
            detail=f"Intelligence endpoint error: {str(e)}"
        )


@app.post("/ask")
async def ask(question: str):
    return {
        "question": question,
        "answer": "RAG pipeline will be connected here.",
        "sources": []
    }