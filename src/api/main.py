from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.inference.predict import ChestXRayInference

app = FastAPI(
    title="Q-MedTriage API",
    version="0.1.0",
    description="Quantum-assisted medical image triage backend"
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

try:
    inference_pipeline = ChestXRayInference()
    PIPELINE_LOADED = True
    print("✓ Inference pipeline ready")
except Exception as e:
    print(f"✗ Failed to load inference pipeline: {e}")
    PIPELINE_LOADED = False
    inference_pipeline = None

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
    return {
        "api": "online",
        "vision_model": "ready" if PIPELINE_LOADED else "failed",
        "classical_svm": "ready" if PIPELINE_LOADED else "failed",
        "quantum_model": "available" if PIPELINE_LOADED else "unavailable",
        "rag": "pending",
        "pipeline_loaded": PIPELINE_LOADED
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict pneumonia from chest X-ray image
    
    Returns:
        JSON with prediction, confidence, probabilities, and disclaimer
    """
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
        
        # Run inference
        result = inference_pipeline.predict(image, include_features=False)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Prediction failed: {result.get('error', 'Unknown error')}"
            )
        
        # Add filename to response
        result["filename"] = file.filename
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.post("/ask")
async def ask(question: str):
    return {
        "question": question,
        "answer": "RAG pipeline will be connected here.",
        "sources": []
    }