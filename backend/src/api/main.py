from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import sys
from pathlib import Path
from typing import Optional, Any

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try backend/.env first, then fallback to project root .env
    backend_env_path = PROJECT_ROOT / '.env'
    root_env_path = PROJECT_ROOT.parent / '.env'
    
    if backend_env_path.exists():
        load_dotenv(backend_env_path)
        print(f"Loaded environment from {backend_env_path}")
    elif root_env_path.exists():
        load_dotenv(root_env_path)
        print(f"Loaded environment from {root_env_path}")
    else:
        print(f"Warning: .env file not found at {backend_env_path} or {root_env_path}")
except ImportError:
    print("Warning: python-dotenv not installed, relying on system environment")

from src.inference.predict import ChestXRayInference
from src.inference.chest_xray_validator import ChestXRayValidator

# Intelligence Layer (Phase 2) imports
try:
    from src.rag.retriever import RAGRetriever
    from src.rag.grok_synthesizer import GrokSynthesizer
    INTELLIGENCE_IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Intelligence layer imports failed: {e}")
    INTELLIGENCE_IMPORTS_AVAILABLE = False
    RAGRetriever = None
    GrokSynthesizer = None

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

# Phase 0: Chest X-ray Validator (CRITICAL SAFETY GATE)
chest_xray_validator = None
VALIDATOR_LOADED = False

try:
    chest_xray_validator = ChestXRayValidator()
    chest_xray_validator.load()
    VALIDATOR_LOADED = True
    print("OK: Phase 0: Chest X-ray validator ready (SAFETY GATE ACTIVE)")
except Exception as e:
    print(f"ERROR: Failed to load chest X-ray validator: {e}")
    print("WARNING: System will accept ANY image - UNSAFE!")
    VALIDATOR_LOADED = False
    chest_xray_validator = None

# Phase 1: Image Classification
try:
    inference_pipeline = ChestXRayInference()
    PIPELINE_LOADED = True
    print("OK: Phase 1: Inference pipeline ready")
except Exception as e:
    print(f"ERROR: Failed to load inference pipeline: {e}")
    PIPELINE_LOADED = False
    inference_pipeline = None

# Phase 2: Intelligence Layer (RAG + Grok)
rag_retriever = None
grok_synthesizer = None
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
            print("OK: Phase 2: RAG retriever ready")
             
            # Initialize Grok synthesizer (requires API key)
            xai_api_key = os.getenv("XAI_API_KEY")
            if xai_api_key and xai_api_key != "your_xai_api_key_here":
                grok_synthesizer = GrokSynthesizer()
                grok_synthesizer.initialize()
                print("OK: Phase 2: Grok synthesizer ready")
                INTELLIGENCE_ENABLED = True
            else:
                print("WARNING: Phase 2: XAI_API_KEY not configured")
                print("  Intelligence layer will be unavailable")
                print("  Set XAI_API_KEY in .env to enable")
                 
        except Exception as e:
            print(f"WARNING: Phase 2: Intelligence layer initialization failed: {e}")
            print("  /intelligence endpoint will return errors")
            rag_retriever = None
            grok_synthesizer = None
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
        "chest_xray_validator": "ready" if VALIDATOR_LOADED else "failed",
        "vision_model": "ready" if PIPELINE_LOADED else "failed",
        "classical_svm": "ready" if PIPELINE_LOADED else "failed",
        "quantum_svm": "ready" if quantum_available else "unavailable",
        "rag_retriever": "ready" if (rag_retriever and rag_retriever.is_ready) else "unavailable",
        "grok_synthesizer": "ready" if (grok_synthesizer and grok_synthesizer.is_ready) else "unavailable",
        "intelligence_enabled": INTELLIGENCE_ENABLED,
        "pipeline_loaded": PIPELINE_LOADED,
        "validator_loaded": VALIDATOR_LOADED
    }


@app.post("/validate-image")
async def validate_image(file: UploadFile = File(...)):
    """
    Validate that an uploaded image is a chest radiograph.
    
    This endpoint ONLY performs validation, no inference.
    Use this before calling /predict to implement two-phase user flow:
    1. Upload → Validate → Show "Chest Radiograph Detected" OR "Unsupported Image"
    2. User clicks "Begin Analysis" → Call /predict
    
    Args:
        file: Uploaded image file
    
    Returns:
        HTTP 200 with validation result:
        {
            "valid": true/false,
            "detected_type": "chest_xray" | "unsupported",
            "confidence": float,
            "message": str,
            "scores": {...}
        }
    """
    print("\n" + "=" * 70)
    print("[VALIDATE-IMAGE] Request received")
    print("=" * 70)
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Must be an image."
        )
    
    try:
        # Read and load image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        print(f"[VALIDATE-IMAGE] Image loaded: {image.size} {image.mode}")
        
        # Check if validator is loaded
        if not VALIDATOR_LOADED:
            print("[VALIDATE-IMAGE] ✗ ERROR: Validator not loaded")
            print("=" * 70)
            raise HTTPException(
                status_code=503,
                detail="Chest X-ray validator not available. Cannot perform validation."
            )
        
        # Run validation
        print("[VALIDATE-IMAGE] Running chest X-ray validation...")
        validation_result = chest_xray_validator.validate(image)
        
        # Build response
        if validation_result["is_valid_chest_xray"]:
            # VALID CHEST RADIOGRAPH
            print(f"[VALIDATE-IMAGE] ✓ ACCEPTED - Chest X-ray confidence = {validation_result['confidence']:.2%}")
            print(f"[VALIDATE-IMAGE] Margin: {validation_result['scores']['margin']:.2%}")
            print("=" * 70)
            
            return JSONResponse(
                status_code=200,
                content={
                    "valid": True,
                    "detected_type": "chest_xray",
                    "confidence": validation_result["confidence"],
                    "message": "Chest radiograph detected successfully.",
                    "scores": validation_result["scores"],
                    "threshold": validation_result["threshold"],
                    "margin_threshold": validation_result["margin_threshold"]
                }
            )
        else:
            # INVALID / NON-CHEST IMAGE
            print(f"[VALIDATE-IMAGE] ✗ REJECTED - {validation_result['detected_type']}")
            print(f"[VALIDATE-IMAGE] Confidence: {validation_result['confidence']:.2%}")
            print(f"[VALIDATE-IMAGE] Reason: {validation_result['reason']}")
            print("=" * 70)
            
            return JSONResponse(
                status_code=200,  # Still 200, but valid=false in body
                content={
                    "valid": False,
                    "detected_type": validation_result["detected_type"],
                    "confidence": validation_result["confidence"],
                    "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
                    "reason": validation_result["reason"],
                    "scores": validation_result["scores"],
                    "threshold": validation_result["threshold"],
                    "margin_threshold": validation_result["margin_threshold"]
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"[VALIDATE-IMAGE] ✗ ERROR: {str(e)}")
        print("=" * 70)
        raise HTTPException(
            status_code=500,
            detail=f"Error validating image: {str(e)}"
        )


@app.post("/predict/batch")
async def predict_batch(files: list[UploadFile] = File(...), classifier: str = "classical"):
    """
    Batch predict pneumonia from multiple chest X-ray images
    
    Process up to 50 chest X-rays simultaneously with independent validation
    and prediction for each image. Invalid images are rejected individually
    without failing the entire batch.
    
    Args:
        files: List of uploaded chest X-ray images (max 50)
        classifier: "classical" (default) or "quantum"
    
    Returns:
        JSON with batch summary and individual results for each image
    """
    print("\n" + "=" * 70)
    print("[BATCH PREDICT] Request received")
    print("=" * 70)
    print(f"[BATCH PREDICT] Total images: {len(files)}")
    print("=" * 70)
    
    # Validate batch size
    if len(files) > 50:
        raise HTTPException(
            status_code=400,
            detail=f"Too many images. Maximum 50 images allowed, received {len(files)}"
        )
    
    if len(files) == 0:
        raise HTTPException(
            status_code=400,
            detail="No images provided"
        )
    
    # Validate classifier parameter
    if classifier not in ["classical", "quantum"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'"
        )
    
    # Check if pipeline is available
    if not PIPELINE_LOADED:
        raise HTTPException(
            status_code=503,
            detail="Inference pipeline not available"
        )
    
    results = []
    successful_count = 0
    rejected_count = 0
    failed_count = 0
    
    # Process each image independently
    for idx, file in enumerate(files):
        image_id = f"image_{idx + 1:03d}"
        print(f"\n[BATCH] Processing {idx + 1}/{len(files)}: {file.filename}")
        
        try:
            # Validate file type
            if not file.content_type.startswith("image/"):
                results.append({
                    "image_id": image_id,
                    "filename": file.filename,
                    "success": False,
                    "status": "failed",
                    "error": f"Invalid file type: {file.content_type}"
                })
                failed_count += 1
                continue
            
            # Read image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Validation gate
            if VALIDATOR_LOADED:
                validation_result = chest_xray_validator.validate(image)
                
                if not validation_result["is_valid_chest_xray"]:
                    # Reject this image, continue with others
                    print(f"[BATCH] ✗ REJECTED - {validation_result['detected_type']}")
                    results.append({
                        "image_id": image_id,
                        "filename": file.filename,
                        "success": False,
                        "status": "rejected",
                        "reason": validation_result["reason"],
                        "detected_type": validation_result["detected_type"],
                        "validation_confidence": validation_result["confidence"]
                    })
                    rejected_count += 1
                    continue
                
                print(f"[BATCH] ✓ ACCEPTED - Chest X-ray confidence = {validation_result['confidence']:.2%}")
            
            # Run inference
            prediction_result = inference_pipeline.predict(image, classifier=classifier, include_features=False)
            
            if not prediction_result["success"]:
                results.append({
                    "image_id": image_id,
                    "filename": file.filename,
                    "success": False,
                    "status": "failed",
                    "error": prediction_result.get("error", "Prediction failed")
                })
                failed_count += 1
                continue
            
            # Success
            results.append({
                "image_id": image_id,
                "filename": file.filename,
                "success": True,
                "status": "completed",
                "prediction": prediction_result["prediction_label"],
                "confidence": prediction_result["confidence"],
                "probabilities": prediction_result["probabilities"],
                "model": prediction_result["model"],
                "model_type": prediction_result["model_type"],
                "inference_time_ms": prediction_result["inference_time_ms"]
            })
            successful_count += 1
            print(f"[BATCH] ✓ COMPLETED - {prediction_result['prediction_label']} ({prediction_result['confidence']:.1%})")
            
        except Exception as e:
            print(f"[BATCH] ✗ ERROR processing {file.filename}: {str(e)}")
            results.append({
                "image_id": image_id,
                "filename": file.filename,
                "success": False,
                "status": "failed",
                "error": f"Processing error: {str(e)}"
            })
            failed_count += 1
    
    print("\n" + "=" * 70)
    print(f"[BATCH] Complete: {successful_count} successful, {rejected_count} rejected, {failed_count} failed")
    print("=" * 70)
    
    return JSONResponse(content={
        "success": True,
        "batch_summary": {
            "total_images": len(files),
            "processed": len(files),
            "successful": successful_count,
            "rejected": rejected_count,
            "failed": failed_count
        },
        "classifier": classifier,
        "results": results
    })


@app.post("/predict")
async def predict(file: UploadFile = File(...), classifier: str = "classical"):
    """
    Predict pneumonia from chest X-ray image
    
    CRITICAL: This endpoint includes STRICT input validation.
    Only valid chest radiographs are accepted.
    Validation runs BEFORE checking if inference pipeline is available.
    
    RECOMMENDED FLOW:
    1. Call /validate-image first to check if image is a chest radiograph
    2. Show validation result to user
    3. Only if valid, allow user to click "Begin Analysis"
    4. Then call this /predict endpoint
    
    Args:
        file: Uploaded chest X-ray image
        classifier: "classical" (default) or "quantum"
    
    Returns:
        JSON with prediction, confidence, probabilities, and disclaimer
        OR validation error if image is not a chest radiograph
    """
    print("\n" + "=" * 70)
    print("[PREDICT] Request received")
    print("=" * 70)
    print(f"[PREDICT] File: {file.filename}")
    print(f"[PREDICT] Content-Type: {file.content_type}")
    print(f"[PREDICT] Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    print("=" * 70)
    
    # Validate classifier parameter
    if classifier not in ["classical", "quantum"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'"
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
        print(f"[PREDICT] Image loaded: {image.size} {image.mode}")
        
        # ============================================================================
        # CRITICAL SAFETY GATE: Validate that this is a chest radiograph
        # THIS MUST RUN FIRST - BEFORE ANY PIPELINE CHECKS
        # ============================================================================
        print("[VALIDATION] Running chest X-ray validation...")
        
        if VALIDATOR_LOADED:
            validation_result = chest_xray_validator.validate(image)
            
            if not validation_result["is_valid_chest_xray"]:
                # REJECT: Not a chest radiograph
                print(f"[VALIDATION] ✗ REJECTED - {validation_result['detected_type']}")
                print(f"[VALIDATION] Confidence: {validation_result['confidence']:.2%}")
                print(f"[VALIDATION] Reason: {validation_result['reason']}")
                print("[VALIDATION] Image will NOT proceed to inference pipeline")
                print("=" * 70)
                
                return JSONResponse(
                    status_code=400,
                    content={
                        "valid": False,
                        "error": "unsupported_image",
                        "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
                        "validation": {
                            "is_valid_chest_xray": False,
                            "confidence": validation_result["confidence"],
                            "detected_type": validation_result["detected_type"],
                            "reason": validation_result["reason"],
                            "scores": validation_result["scores"]
                        }
                    }
                )
            
            # ACCEPT: Valid chest radiograph
            print(f"[VALIDATION] ✓ ACCEPTED - Chest X-ray confidence = {validation_result['confidence']:.2%}")
            print(f"[VALIDATION] Margin: {validation_result['scores']['margin']:.2%}")
            print("[VALIDATION] Image will proceed to inference pipeline")
        else:
            # WARNING: Validator not loaded - proceeding WITHOUT validation
            print("[VALIDATION] ✗ WARNING: Validator not loaded - proceeding without validation (UNSAFE)")
            validation_result = None
        
        # ============================================================================
        # ONLY AFTER VALIDATION PASSES: Check if pipeline is available
        # ============================================================================
        if not PIPELINE_LOADED:
            print("[INFERENCE] ✗ Inference pipeline not available")
            print("=" * 70)
            raise HTTPException(
                status_code=503,
                detail="Inference pipeline not available. The image passed validation, but the classification models are not loaded."
            )
        
        # ============================================================================
        # Run inference with selected classifier
        # ============================================================================
        print(f"[INFERENCE] Running {classifier} classifier...")
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
        
        # Add filename, classifier, and validation info to response
        result["filename"] = file.filename
        result["classifier"] = classifier
        
        if validation_result:
            result["validation"] = {
                "is_valid_chest_xray": True,
                "confidence": validation_result["confidence"],
                "detected_type": "chest_xray"
            }
        
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
    - Phase 0: Chest X-ray validation (RUNS FIRST)
    - Phase 1: Image classification (ResNet50 → PCA → Classical/Quantum SVM)
    - Phase 2: RAG evidence retrieval (FAISS similarity search)
    - Phase 2: LLM evidence-grounded synthesis
    
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
    - Validation runs FIRST before any processing
    - Classifier prediction is authoritative (never overridden)
    - LLM synthesis is evidence-only (no diagnosis/treatment)
    - All sources are from authoritative medical organizations
    - Medical disclaimer is mandatory
    """
    print("\n" + "=" * 70)
    print("[INTELLIGENCE] Request received")
    print("=" * 70)
    
    # Validate classifier parameter
    if classifier not in ["classical", "quantum"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid classifier: {classifier}. Must be 'classical' or 'quantum'"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Must be an image."
        )
    
    try:
        # ====================================================================
        # STEP 0: CRITICAL SAFETY GATE - Validate chest radiograph FIRST
        # ====================================================================
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        print(f"[INTELLIGENCE] Image loaded: {image.size} {image.mode}")
        
        # Validate that this is a chest radiograph
        print("[VALIDATION] Running chest X-ray validation...")
        
        if VALIDATOR_LOADED:
            validation_result = chest_xray_validator.validate(image)
            
            if not validation_result["is_valid_chest_xray"]:
                # REJECT: Not a chest radiograph
                print(f"[VALIDATION] ✗ REJECTED - {validation_result['detected_type']}")
                print(f"[VALIDATION] Confidence: {validation_result['confidence']:.2%}")
                print(f"[VALIDATION] Reason: {validation_result['reason']}")
                print("[VALIDATION] Image will NOT proceed to intelligence pipeline")
                print("=" * 70)
                
                return JSONResponse(
                    status_code=400,
                    content={
                        "valid": False,
                        "error": "unsupported_image",
                        "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
                        "validation": {
                            "is_valid_chest_xray": False,
                            "confidence": validation_result["confidence"],
                            "detected_type": validation_result["detected_type"],
                            "reason": validation_result["reason"],
                            "scores": validation_result["scores"]
                        }
                    }
                )
            
            # ACCEPT: Valid chest radiograph
            print(f"[VALIDATION] ✓ ACCEPTED - Chest X-ray confidence = {validation_result['confidence']:.2%}")
            print(f"[VALIDATION] Margin: {validation_result['scores']['margin']:.2%}")
            print("[VALIDATION] Image will proceed to intelligence pipeline")
        else:
            # WARNING: Validator not loaded
            print("[VALIDATION] ✗ WARNING: Validator not loaded - proceeding without validation (UNSAFE)")
            validation_result = None
        
        # ====================================================================
        # ONLY AFTER VALIDATION PASSES: Check system availability
        # ====================================================================
        
        # Check if intelligence layer is available
        if not INTELLIGENCE_ENABLED:
            raise HTTPException(
                status_code=503,
                detail="Intelligence layer not available. Check XAI_API_KEY configuration."
            )
        
        # Check if pipeline is loaded
        if not PIPELINE_LOADED:
            print("[INFERENCE] ✗ Inference pipeline not available")
            print("=" * 70)
            raise HTTPException(
                status_code=503,
                detail="Inference pipeline not available. The image passed validation, but the classification models are not loaded."
            )
        
        # ====================================================================
        # STEP 1: RUN PHASE 1 CLASSIFIER
        # ====================================================================
        
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
        # STEP 5: RUN STAGE 5 GROK SYNTHESIS
        # ====================================================================
        
        synthesis_result = None
        synthesis_success = False
        
        if retrieved_evidence:
            try:
                synthesis_result = grok_synthesizer.synthesize(
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
                    "disclaimer": GrokSynthesizer.MEDICAL_DISCLAIMER,
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
                "disclaimer": GrokSynthesizer.MEDICAL_DISCLAIMER,
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
async def ask(
    question: str,
    payload: Optional[dict[str, Any]] = Body(default=None),
):
    """
    Q&A endpoint for medical questions about analysis results
    
    Uses current analysis context + RAG retrieval + Grok synthesis to provide
    evidence-grounded medical explanations with source citations.
    
    Args:
        question: User's medical question (query parameter)
        payload: Optional JSON body with analysis_context for the current session
    
    Returns:
        JSON with:
        - question: The user's question
        - answer: Generated explanation
        - sources: List of source documents with URLs
        - follow_up_questions: Suggested follow-up questions
        - success: Operation status
    """
    analysis_context = None
    if payload:
        analysis_context = payload.get("analysis_context")

    # Check if intelligence layer is available
    if not INTELLIGENCE_ENABLED:
        return {
            "question": question,
            "answer": (
                "The Q&A service is currently unavailable. "
                "Please ensure XAI_API_KEY is configured."
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
        
        # Step 2: Synthesize response using Grok
        print(f"[LLM] Generating explanation with Grok...")
        synthesis_result = grok_synthesizer.synthesize(
            query=question,
            retrieved_results=retrieved_results,
            analysis_context=analysis_context,
        )
        print(f"[LLM] Response generated: {synthesis_result['success']}")
        
        # Return response
        return {
            "question": question,
            "answer": synthesis_result.get("answer"),
            "sources": synthesis_result.get("sources", []),
            "follow_up_questions": synthesis_result.get("follow_up_questions", []),
            "disclaimer": synthesis_result.get("disclaimer"),
            "success": synthesis_result.get("success", False),
            "retrieved_count": len(retrieved_results)
        }
        
    except Exception as e:
        print(f"[ERROR] Q&A failed: {e}")
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