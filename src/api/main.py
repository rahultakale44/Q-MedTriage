from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def root():
    return {
        "name": "Q-MedTriage",
        "status": "online",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "api": "online",
        "vision_model": "pending",
        "quantum_model": "pending",
        "rag": "pending"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    return {
        "status": "received",
        "filename": file.filename,
        "message": "Inference pipeline will be connected here."
    }


@app.post("/ask")
async def ask(question: str):
    return {
        "question": question,
        "answer": "RAG pipeline will be connected here.",
        "sources": []
    }