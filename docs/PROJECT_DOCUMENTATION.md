# Q-MedTriage: Technical Documentation

## Project Overview

Q-MedTriage is an AI-powered medical image triage system that combines classical machine learning, quantum computing, and retrieval-augmented generation (RAG) to provide rapid pneumonia detection from chest X-rays with evidence-grounded explanations.

**Key Innovation:** Integration of quantum computing in the classification pipeline and RAG-based medical intelligence layer for transparent, source-backed explanations.

---

## Problem Statement

### Medical Context

Pneumonia is a leading cause of mortality worldwide, requiring rapid triage for effective treatment. Chest X-rays are a primary diagnostic tool, but radiologist availability can be limited in resource-constrained settings or during emergencies.

### Technical Challenge

Build an AI system that:
1. **Classifies** chest X-rays as NORMAL or PNEUMONIA
2. **Provides confidence scores** for triage prioritization
3. **Explores quantum advantage** in medical image classification
4. **Generates evidence-grounded explanations** using RAG + LLM
5. **Maintains safety** through clear AI vs. medical professional boundaries

### Critical Terminology

- **Prediction Label**: The classified category (NORMAL or PNEUMONIA)
- **Confidence**: How strongly the model matched the image to the predicted class (0-100%)
  - NOT a literal probability of disease
  - Reflects pattern recognition strength, not clinical diagnosis
- **Quantum SVM**: Quantum kernel-based classifier using reduced feature space
- **RAG**: Retrieval-Augmented Generation - grounding LLM responses in retrieved medical evidence

---

## System Architecture

### Complete Pipeline

```
User Uploads Chest X-ray (JPEG/PNG)
        ↓
┌─────────────────────────────────────┐
│ 1. IMAGE PREPROCESSING              │
│    - Resize to 224×224               │
│    - Grayscale/RGB normalization     │
│    - ImageNet normalization          │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ 2. FEATURE EXTRACTION               │
│    ResNet50 (Transfer Learning)      │
│    → 2048-dimensional CNN features   │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ 3. PCA DIMENSIONALITY REDUCTION     │
│    2048D → 4D                        │
│    (Quantum compatibility)           │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ 4. CLASSIFICATION                   │
│    Classical SVM  OR  Quantum SVM    │
│    → Prediction + Confidence         │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ 5. RAG EVIDENCE RETRIEVAL           │
│    Query: prediction context         │
│    → FAISS vector search             │
│    → Top-5 relevant medical docs     │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ 6. LLM SYNTHESIS                    │
│    Input: prediction + evidence      │
│    → Groq/OpenAI-compatible API      │
│    → Evidence-grounded explanation   │
└─────────────────────────────────────┘
        ↓
   JSON Response + UI Display
```

---

## Classical AI Layer

### 1. Transfer Learning with ResNet50

**Architecture:**
- Pretrained ResNet50 (ImageNet weights)
- Remove classification head
- Use as feature extractor (2048D output)

**Rationale:**
- Proven CNN architecture
- Pretrained on 1M+ images
- Generalizes well to medical imaging
- Fast inference (~50-100ms)

**Implementation:**
```python
from torchvision import models

resnet = models.resnet50(pretrained=True)
resnet.fc = nn.Identity()  # Remove classification layer
resnet.eval()

# Extract features
with torch.no_grad():
    features = resnet(preprocessed_image)  # → torch.Size([1, 2048])
```

### 2. PCA Dimensionality Reduction

**Purpose:**
- Reduce 2048D features to 4D
- Remove redundancy and noise
- Enable quantum processing (limited qubit availability)
- Improve computational efficiency

**Training:**
- Trained on 5,216 chest X-ray images
- Captures ~85-90% of variance in 4 principal components
- Frozen after training (no retraining during inference)

**Critical Design Choice:**
4 dimensions chosen as optimal balance:
- Sufficient information preservation
- Quantum hardware feasibility
- Classical SVM performance maintained

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=4)
pca.fit(train_features_2048d)

# Inference
features_4d = pca.transform(features_2048d)
```

### 3. Classical SVM Classifier

**Algorithm:** Support Vector Machine with RBF kernel

**Training Data:**
- Training set: 5,216 images (80% split)
- Test set: 624 images (20% split)
- Classes: NORMAL (1,341 images), PNEUMONIA (3,875 images)

**Performance:**
- Accuracy: ~89-91%
- Precision: ~88-90%
- Recall: ~89-92%
- ROC-AUC: ~0.92-0.94

**Output:**
```python
{
    "prediction": 1,                    # 0=NORMAL, 1=PNEUMONIA
    "prediction_label": "PNEUMONIA",
    "confidence": 0.9267,               # SVM decision function confidence
    "probabilities": {
        "NORMAL": 0.0733,
        "PNEUMONIA": 0.9267
    }
}
```

---

## Quantum AI Layer

### Why Quantum Computing for Medical Imaging?

**Quantum Advantage Hypothesis:**
Medical image classification in reduced-dimensional space may benefit from:
1. **Quantum kernel methods** - exploring non-classical feature spaces
2. **Entanglement** - capturing complex correlations
3. **Quantum feature maps** - non-linear transformations

**Current Status:** Research prototype demonstrating quantum ML feasibility

**Important Disclaimer:**
- This is NOT production quantum computing
- Results are experimental and educational
- No claims of quantum supremacy
- Comparison with classical methods is for research purposes

### PCA: Quantum-Classical Bridge

**Why 4 Dimensions?**

1. **Qubit Limitations:**
   - Each feature dimension requires qubits for encoding
   - Current quantum simulators limited to ~10-20 qubits
   - 4D allows efficient encoding with 2-4 qubits

2. **Information Preservation:**
   - PCA captures ~85-90% of original 2048D information
   - Critical features retained
   - Noise reduced

3. **Classical Performance:**
   - Classical SVM performs well on 4D PCA features
   - Fair comparison baseline established

### Quantum SVM Implementation

**Framework:** Qiskit (IBM Quantum)

**Architecture:**
```
4D PCA Features
    ↓
Quantum Feature Map (ZZFeatureMap)
    ↓
Quantum Kernel Estimation
    ↓
Classical SVM with Quantum Kernel
    ↓
Prediction + Confidence
```

**Quantum Feature Map:**
- ZZFeatureMap with 2 qubits per feature
- Entanglement pattern: full entanglement
- Depth: 2 repetitions

**Training:**
- Subset sampling (200 images) due to computational constraints
- Stratified sampling (maintains class balance)
- Quantum kernel computed for all training pairs

**Limitations:**
- Training time: ~6-10 minutes (vs. <1 second classical)
- Inference time: ~6-8 seconds per image (vs. 50ms classical)
- Accuracy: Comparable to classical (~88-92%)
- Scalability: Limited by quantum simulation overhead

**Performance Comparison:**

| Metric | Classical SVM | Quantum SVM |
|--------|--------------|-------------|
| Training Time | <1 second | 6-10 minutes |
| Inference Time | 50ms | 6-8 seconds |
| Accuracy | 89-91% | 88-92% |
| Model Size | ~500KB | ~2MB |

---

## Intelligence Layer (RAG + LLM)

### Architecture

**Purpose:** Provide evidence-grounded medical context for AI predictions

**Critical Safety Principle:**
- Intelligence layer is AUGMENTATION, not replacement
- Classifier prediction is authoritative
- LLM never overrides or modifies the prediction
- All medical claims must cite retrieved evidence

### 1. Medical Knowledge Base

**Sources (Authoritative Only):**
- World Health Organization (WHO)
- Centers for Disease Control and Prevention (CDC)
- National Institutes of Health (NIH)
- Mayo Clinic patient education materials

**Structure:**
```json
{
    "id": "pneumonia_symptoms_001",
    "condition": "pneumonia",
    "category": "symptoms",
    "title": "Symptoms of Pneumonia",
    "text": "Pneumonia symptoms can vary from mild to severe...",
    "source": "Mayo Clinic",
    "source_url": "https://www.mayoclinic.org/...",
    "keywords": ["fever", "cough", "breathing"],
    "retrieved_date": "2026-08-26"
}
```

**Corpus Size:** 22 documents covering:
- Pneumonia overview, symptoms, treatment
- Normal chest X-ray findings
- Triage guidance
- Risk factors

### 2. Vector Database (FAISS)

**Embedding Model:** `all-MiniLM-L6-v2` (SentenceTransformers)
- Dimension: 384D
- Model size: ~90MB (cached locally)
- Fast inference: ~10-20ms per query

**Index Type:** FAISS IndexFlatL2 (L2 distance, exact search)

**Retrieval Process:**
```
User Question
    ↓
Embed with all-MiniLM-L6-v2 (384D)
    ↓
FAISS Similarity Search (top-k=5)
    ↓
Retrieved Medical Documents + Metadata
```

### 3. LLM Synthesis (Groq)

**Provider:** Groq (OpenAI-compatible API)
**Model:** `openai/gpt-oss-120b` (120B parameter model)
**Max Tokens:** 1000 (detailed responses)
**Temperature:** 0.3 (factual, consistent)

**System Prompt Design:**
```
You are a medical AI assistant for Q-MedTriage.

You receive:
1. CURRENT ANALYSIS RESULT (AI model output)
   - Prediction: {label}
   - Confidence: {confidence}
   
2. RETRIEVED MEDICAL EVIDENCE (from knowledge base)
   - {document_1}
   - {document_2}
   - ...

Rules:
- You are NOT a doctor
- Do NOT diagnose patients
- Do NOT prescribe treatment
- Use ONLY retrieved evidence for medical claims
- Clearly distinguish AI output from medical facts
- Explain confidence as AI classification metric, not disease probability
- Include medical disclaimer
```

**Response Format:**
```json
{
    "question": "Why was this prediction made?",
    "answer": "The AI model classified this X-ray as PNEUMONIA with 92% confidence, meaning the model strongly matched the image patterns to its learned features for pneumonia. According to the Mayo Clinic...",
    "sources": [
        {
            "title": "Symptoms of Pneumonia",
            "source": "Mayo Clinic",
            "url": "https://...",
            "condition": "pneumonia",
            "category": "symptoms"
        }
    ],
    "follow_up_questions": [
        "What are common symptoms of pneumonia?",
        "What does the confidence percentage mean?",
        "When should I seek medical attention?"
    ],
    "disclaimer": "This information is for educational purposes only...",
    "success": true
}
```

### Safety Mechanisms

1. **Prediction Isolation:**
   - Classifier runs first, result stored
   - LLM receives prediction as INPUT, not output
   - No mechanism for LLM to change prediction

2. **Evidence Grounding:**
   - Retrieved documents passed to LLM
   - System prompt enforces "use ONLY retrieved evidence"
   - Post-generation validation (sources must match retrieved docs)

3. **Graceful Degradation:**
   - If RAG fails → return prediction without explanation
   - If LLM fails → return prediction + retrieved evidence without synthesis
   - System always provides at least the classifier result

4. **Clear Attribution:**
   - "AI Classification" section (from vision model)
   - "Medical Information" section (from knowledge base)
   - "Generated Explanation" section (from LLM)
   - Medical disclaimer on all responses

---

## Backend Architecture

### FastAPI Application

**File:** `src/api/main.py`

**Initialization:**
```python
# Phase 1: Vision Pipeline
inference_pipeline = ChestXRayInference()

# Phase 2: Intelligence Layer
rag_retriever = RAGRetriever()
grok_synthesizer = GrokSynthesizer()
```

### API Endpoints

#### 1. `/predict` - Image Classification

**Method:** POST  
**Input:** Multipart form-data with image file  
**Query Parameters:**
- `classifier`: "classical" (default) or "quantum"

**Response:**
```json
{
    "success": true,
    "model": "Classical SVM",
    "model_type": "classical",
    "prediction_label": "PNEUMONIA",
    "confidence": 0.9267,
    "probabilities": {
        "NORMAL": 0.0733,
        "PNEUMONIA": 0.9267
    },
    "inference_time_ms": 46.7,
    "disclaimer": "AI-assisted triage prediction...",
    "filename": "example.jpeg"
}
```

#### 2. `/intelligence` - Full Pipeline with Explanation

**Method:** POST  
**Input:** Image + classifier choice  
**Response:** Prediction + RAG evidence + LLM explanation

#### 3. `/ask` - Context-Aware Q&A

**Method:** POST  
**Query Parameters:** `question` (required)  
**Body:** `{"analysis_context": {...}}` (optional)

**Example:**
```bash
POST /ask?question=Why%20was%20this%20prediction%20made?
Body: {
    "analysis_context": {
        "prediction": "PNEUMONIA",
        "confidence": 0.9267,
        "probabilities": {...}
    }
}
```

**Response:** Evidence-grounded answer with sources

#### 4. `/health` - System Status

**Method:** GET  
**Response:**
```json
{
    "api": "online",
    "vision_model": "ready",
    "classical_svm": "ready",
    "quantum_svm": "ready",
    "rag_retriever": "ready",
    "grok_synthesizer": "ready",
    "intelligence_enabled": true,
    "pipeline_loaded": true
}
```

### Model Loading Strategy

**Lazy Loading:** Models loaded once at startup
```python
# PCA model (~500KB)
pca_model = joblib.load("models/pca_reducer.pkl")

# Classical SVM (~500KB)
svm_model = joblib.load("models/classical_svm.pkl")

# Quantum SVM (~2MB)
quantum_model = QuantumSVM.load("models/quantum_svm.pkl")

# ResNet50 (cached by PyTorch, ~100MB)
resnet = models.resnet50(pretrained=True)
```

---

## Frontend Architecture

### Technology Stack

- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Custom CSS with modern animations
- **State Management:** React Hooks (useState, useEffect)
- **API Client:** Fetch API

### Pipeline Visualization

**Components:**
1. **UploadStage** - Image upload with drag-and-drop
2. **ScanningStage** - Preprocessing animation
3. **FeatureExtractionStage** - ResNet50 visualization
4. **DimensionalityReductionStage** - PCA visualization (2048D → 4D)
5. **QuantumProcessingStage** - Quantum circuit animation (if quantum selected)
6. **EvidenceRetrievalStage** - RAG search visualization
7. **ReasoningStage** - LLM synthesis animation
8. **ResultStage** - Final prediction + explanation

### Custom Hooks

**`usePipeline.js`:**
- Manages multi-stage pipeline state
- Handles stage progression
- Coordinates animations

**`usePrediction.js`:**
- Manages API calls to backend
- Handles loading/error states
- Processes prediction results

### API Service Layer

**File:** `dashboard/src/services/api.js`

```javascript
export async function analyzeImage(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);
    
    const response = await fetch(`${BASE_URL}/predict`, {
        method: "POST",
        body: formData,
    });
    
    return await response.json();
}

export async function askQuestion(question, context) {
    const response = await fetch(
        `${BASE_URL}/ask?question=${encodeURIComponent(question)}`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ analysis_context: context }),
        }
    );
    
    return await response.json();
}
```

---

## Setup Instructions

### Prerequisites

- Python 3.14.4+
- Node.js 18+
- npm 9+
- 8GB+ RAM (for ML models)
- Internet connection (first run downloads models)

### Backend Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Q-MedTriage
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   .\.venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

6. **Download Models** (if not included)
   - Models should be in `models/` directory
   - ResNet50 downloads automatically on first use

### Frontend Setup

1. **Navigate to Dashboard**
   ```bash
   cd dashboard
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure API URL**
   - Edit `dashboard/.env` if needed
   - Default: `VITE_API_URL=http://localhost:8000`

### Running the Application

#### Start Backend

```bash
# From project root, with venv activated
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Start Frontend

```bash
# From dashboard directory
npm run dev
```

Frontend will be available at: `http://localhost:5174`

### Testing

```bash
# Run automated tests
pytest tests/

# Run specific test
pytest tests/test_classical_svm.py -v

# Run all tests with coverage
pytest tests/ --cov=src
```

---

## Environment Variables

**File:** `.env` (never commit, use `.env.example` as template)

```bash
# Groq/OpenAI-compatible LLM API
XAI_API_KEY=gsk_...
XAI_MODEL=openai/gpt-oss-120b
XAI_MAX_TOKENS=1000
XAI_TEMPERATURE=0.3

# RAG Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
RAG_TOP_K=5
VECTOR_DB_PATH=data/knowledge/index
KNOWLEDGE_CORPUS_PATH=data/knowledge/medical_corpus.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Safety Configuration
INTELLIGENCE_ENABLED=true
FALLBACK_TO_PREDICTION_ONLY=true
```

**Security:**
- Never commit `.env` to version control
- Add `.env` to `.gitignore`
- Use `.env.example` for documentation (no secrets)
- Rotate API keys regularly

---

## Project Limitations

### Technical Limitations

1. **Quantum Processing:**
   - Quantum simulation, not real quantum hardware
   - Limited scalability (subset training required)
   - Inference time: 6-8 seconds per image
   - Not production-ready

2. **Model Scope:**
   - Binary classification only (NORMAL vs PNEUMONIA)
   - Trained on specific dataset (Kermany et al. chest X-ray dataset)
   - May not generalize to all chest X-ray types
   - No localization (does not identify specific lung regions)

3. **Knowledge Base:**
   - Limited to 22 curated documents
   - English only
   - General medical information (not case-specific)

4. **LLM Limitations:**
   - Depends on external API (Groq)
   - Requires internet connection
   - API costs for each request
   - Response quality depends on prompt engineering

### Medical Limitations

1. **Not a Medical Device:**
   - Research and educational prototype
   - Not FDA-approved or clinically validated
   - Not intended for actual patient diagnosis

2. **No Clinical Calibration:**
   - Confidence scores are ML metrics, not clinical probabilities
   - Cannot replace radiologist interpretation
   - Should not be used for treatment decisions

3. **Training Data Bias:**
   - Model trained on specific patient population
   - May not represent all demographics
   - Performance may vary across age groups, ethnicities, imaging equipment

4. **No Liability:**
   - Predictions for demonstration purposes only
   - Developers not liable for any medical decisions
   - Users assume all risk

---

## Medical Disclaimer

**IMPORTANT - READ CAREFULLY:**

Q-MedTriage is a **research prototype** and **educational demonstration** of AI/ML techniques in medical imaging. It is **NOT**:
- ❌ A medical device
- ❌ A diagnostic tool
- ❌ A replacement for professional medical evaluation
- ❌ FDA-approved or clinically validated
- ❌ Intended for patient care decisions

**This system:**
- ✓ Demonstrates AI classification techniques
- ✓ Explores quantum computing applications
- ✓ Showcases RAG-based information retrieval
- ✓ Provides educational context about pneumonia

**If you have medical concerns:**
1. Consult a qualified healthcare provider
2. Do not rely on AI predictions for diagnosis
3. Seek emergency medical attention for serious symptoms
4. Follow guidance from licensed medical professionals

**Developers and users of this system:**
- Assume full responsibility for appropriate use
- Acknowledge this is educational/research software
- Will not use for actual patient diagnosis or treatment
- Understand predictions are not medical advice

---

## Acknowledgments

### Datasets

- **Kermany et al. Chest X-ray Dataset**
  - Source: Mendeley Data
  - License: CC BY 4.0
  - Citation: Kermany et al. "Labeled Optical Coherence Tomography (OCT) and Chest X-Ray Images for Classification." Mendeley Data, v2, 2018.

### Medical Knowledge Sources

- World Health Organization (WHO)
- Centers for Disease Control and Prevention (CDC)
- National Institutes of Health (NIH)
- Mayo Clinic

### Technologies

- PyTorch & TorchVision (Meta AI)
- Qiskit (IBM Quantum)
- FastAPI (Sebastián Ramírez)
- React (Meta)
- FAISS (Facebook Research)
- SentenceTransformers (Hugging Face)
- scikit-learn (scikit-learn developers)

---

## Future Enhancements

### Short-term
- Multi-class classification (bacterial vs. viral pneumonia)
- Confidence calibration studies
- Expanded knowledge base
- Multiple language support

### Long-term
- Real quantum hardware integration
- Grad-CAM visualization (explainable AI)
- DICOM support
- Clinical validation studies
- Integration with EHR systems

---

## License

[Specify License - e.g., MIT, Apache 2.0, etc.]

---

## Contact

[Add contact information or leave blank for hackathon submission]

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-27  
**Status:** Production Documentation
