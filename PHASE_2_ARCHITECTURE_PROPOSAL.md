# PHASE 2: INTELLIGENCE LAYER — Architecture Proposal

## Date: August 26, 2026
## Status: AUDIT COMPLETE — AWAITING APPROVAL

---

## 📋 EXECUTIVE SUMMARY

This document presents the architecture for adding RAG + VectorDB + LLM intelligence to the verified Q-MedTriage image classification pipeline.

**Critical Design Principle:**
The Intelligence Layer is an **augmentation layer**, NOT a replacement for the vision classifier. The existing prediction pipeline remains primary and must never be broken by Intelligence Layer failures.

---

## ✅ CURRENT STATE AUDIT

### Verified Working Pipeline
```
X-ray upload (JPEG)
  ↓
ResNet50 feature extraction (2048D)
  ↓
PCA dimensionality reduction (4D)
  ↓
Classical SVM / Quantum SVM
  ↓
Prediction + Confidence + Probabilities
  ↓
FastAPI JSON response
  ↓
React Dashboard
```

### Existing Components

**Backend (FastAPI):**
- ✅ `src/api/main.py` — Main API server
- ✅ `/predict` endpoint — Image classification (classical/quantum)
- ✅ `/health` endpoint — System status
- ✅ `/ask` endpoint — **STUB** (currently returns placeholder)
- ✅ `src/inference/predict.py` — Complete inference pipeline

**Current API Response Schema:**
```json
{
  "success": true,
  "model": "Classical SVM",
  "model_type": "classical",
  "prediction": 1,
  "prediction_label": "PNEUMONIA",
  "confidence": 0.9267,
  "probabilities": {
    "NORMAL": 0.0733,
    "PNEUMONIA": 0.9267
  },
  "inference_time_ms": 46.7,
  "disclaimer": "AI-assisted triage prediction for research purposes...",
  "filename": "example.jpeg",
  "classifier": "classical"
}
```

**Infrastructure Directories:**
- ✅ `src/llm/` — **EMPTY** (ready for LLM service)
- ✅ `src/rag/` — **EMPTY** (ready for RAG service)
- ✅ `src/vector_db/` — **EMPTY** (ready for vector database)

**Environment:**
- Python: **3.14.4** (critical compatibility constraint)
- Virtual environment: `.venv/Scripts/python.exe`
- Installed packages: torch, torchvision, scikit-learn, qiskit, fastapi, uvicorn
- **NOT INSTALLED:** faiss, sentence-transformers, openai, transformers, chromadb

**Frontend (React + Vite):**
- ✅ `dashboard/src/App.jsx` — Main dashboard
- ✅ Components: Navbar, StageNavigation, ScrollProgress, AutoRunButton, FakeXray
- ✅ Hooks: `usePipeline.js`, `usePrediction.js`
- ✅ API service: `services/api.js`
- ✅ Currently uses DEMO_ANALYSIS data (static)

**Knowledge Base:**
- ⚠️ `docs/` directory exists but only contains `DATASET.md`
- ❌ No medical knowledge documents currently exist
- ❌ No vector database created

---

## 🎯 INTELLIGENCE LAYER OBJECTIVES

### What the Intelligence Layer Will Provide

For a given classifier prediction (e.g., "PNEUMONIA" @ 92.67% confidence):

1. **Medical Context Retrieval (RAG)**
   - What is pneumonia?
   - Common symptoms and signs
   - When immediate medical attention is needed
   - General risk factors

2. **Evidence Grounding**
   - Source: WHO, CDC, NIH, peer-reviewed literature
   - Preserve metadata (title, URL, organization)
   - No fabricated citations

3. **LLM Synthesis**
   - Translate classifier output into human-readable context
   - Explain what the AI model detected
   - Provide general medical information (NOT diagnosis)
   - Clear uncertainty communication

4. **Structured Response**
   ```json
   {
     "prediction": "PNEUMONIA",
     "confidence": 0.9267,
     "classifier": "classical",
     "intelligence": {
       "medical_context": "...",
       "retrieved_evidence": [...],
       "sources": [...],
       "explanation": "...",
       "triage_guidance": "...",
       "disclaimer": "..."
     }
   }
   ```

---

## 🏗️ PROPOSED ARCHITECTURE

### Component Selection

#### 1. Vector Database: **FAISS**
**Why FAISS:**
- ✅ Lightweight, local-first (no external services)
- ✅ High performance for small-to-medium datasets
- ✅ Facebook Research — production-tested
- ✅ Simple Python interface
- ✅ Deterministic behavior
- ✅ Works offline
- ⚠️ Need to verify Python 3.14 compatibility

**Alternative:** ChromaDB (if FAISS has Python 3.14 issues)

#### 2. Embedding Model: **sentence-transformers**
**Why sentence-transformers:**
- ✅ Local inference (no API calls)
- ✅ Medical domain models available
- ✅ Mature library (Hugging Face)
- ✅ Good balance of speed vs quality
- ⚠️ Need to verify Python 3.14 compatibility

**Recommended Model:** `all-MiniLM-L6-v2` (384 dimensions, fast)
**Alternative:** `all-mpnet-base-v2` (768 dimensions, more accurate)

#### 3. LLM Service: **OpenAI GPT-4 API**
**Why OpenAI API:**
- ✅ Reliable, high-quality responses
- ✅ Easy to swap providers later
- ✅ No local GPU requirements
- ✅ Well-documented Python SDK
- ✅ Good safety alignment

**Design for Provider Flexibility:**
```python
# Abstract interface allows swapping providers
class LLMService:
    def generate(prompt, context) -> str
    
# Implementations:
# - OpenAILLM
# - AnthropicLLM
# - LocalLLM (future)
```

**Environment Variable (never committed):**
```
OPENAI_API_KEY=sk-...
```

#### 4. Knowledge Base: **Custom Medical Corpus**
**Sources (authoritative only):**
- WHO (World Health Organization)
- CDC (Centers for Disease Control)
- NIH/MedlinePlus (public health information)
- Mayo Clinic (patient education materials)
- Public domain medical literature

**Structure:**
```json
{
  "id": "pneumonia_001",
  "condition": "pneumonia",
  "category": "overview",
  "title": "What is Pneumonia?",
  "text": "...",
  "source": "WHO",
  "url": "https://www.who.int/...",
  "retrieved_date": "2026-08-26"
}
```

**Storage:** `data/knowledge/medical_corpus.json`

---

## 📁 PROPOSED FILE STRUCTURE

```
src/
├── rag/
│   ├── __init__.py
│   ├── ingestion.py        # Document loading & chunking
│   ├── retrieval.py        # RAG retrieval service
│   └── knowledge_base.py   # Knowledge corpus management
├── vector_db/
│   ├── __init__.py
│   ├── faiss_store.py      # FAISS vector database
│   └── embeddings.py       # Embedding generation
├── llm/
│   ├── __init__.py
│   ├── service.py          # Abstract LLM interface
│   ├── openai_llm.py       # OpenAI implementation
│   └── prompts.py          # System prompts & templates
├── api/
│   └── main.py             # Update with /intelligence endpoint
└── inference/
    └── predict.py          # (unchanged)

data/
└── knowledge/
    ├── medical_corpus.json     # Source documents
    └── vector_index/           # FAISS index (generated)
        ├── index.faiss
        └── metadata.json

tests/
├── test_rag_ingestion.py
├── test_rag_retrieval.py
├── test_llm_service.py
├── test_intelligence_api.py
└── test_intelligence_e2e.py

.env                        # API keys (gitignored)
```

---

## 🔌 API DESIGN

### Option A: Separate Endpoint (RECOMMENDED)

**Existing endpoint (unchanged):**
```
POST /predict
```

**New intelligence endpoint:**
```
POST /intelligence
Body: {
  "file": <image>,
  "classifier": "classical" | "quantum"
}

Response: {
  "success": true,
  "prediction": {...},      // Same as /predict
  "intelligence": {
    "medical_context": "...",
    "retrieved_evidence": [...],
    "sources": [...],
    "explanation": "...",
    "triage_guidance": "...",
    "disclaimer": "..."
  }
}
```

**Fallback behavior:**
If RAG/LLM fails, return:
```json
{
  "success": true,
  "prediction": {...},
  "intelligence": {
    "error": "Intelligence service unavailable",
    "fallback": true
  }
}
```

### Option B: Query Parameter
```
POST /predict?enhance=true
```

**Recommendation:** Option A for clean separation of concerns

---

## 🔄 INTELLIGENCE PIPELINE

```
User uploads X-ray
  ↓
/intelligence endpoint
  ↓
┌─────────────────────────────────────┐
│ 1. RUN VISION CLASSIFIER            │
│    (existing predict.py)             │
│    → prediction, confidence, probs   │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ 2. CONSTRUCT RAG QUERY              │
│    "Medical information about        │
│     {prediction} for AI triage       │
│     system context"                  │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ 3. EMBED QUERY                      │
│    sentence-transformers             │
│    → 384D vector                     │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ 4. VECTOR SIMILARITY SEARCH         │
│    FAISS.search(query_vector, k=5)  │
│    → top 5 relevant documents        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ 5. LLM SYNTHESIS                    │
│    Prompt:                           │
│    - Classifier: {prediction}        │
│    - Confidence: {confidence}        │
│    - Evidence: {retrieved_docs}      │
│    - Instructions: ground, clarify   │
│    → Natural language explanation    │
└─────────────────────────────────────┘
  ↓
Structured JSON response
```

---

## 🛡️ SAFETY ARCHITECTURE

### Non-Negotiable Rules

1. **LLM MUST NOT override classifier prediction**
   - Prediction remains in separate structured field
   - LLM receives prediction as input, not output

2. **RAG grounding required**
   - Every medical claim must cite retrieved evidence
   - No fabricated sources allowed

3. **Failure isolation**
   - Intelligence Layer failure → fallback to basic prediction
   - Vision classifier NEVER depends on LLM

4. **Clear attribution**
   ```
   Classifier Output: PNEUMONIA (92.67%)
   ────────────────────────────────────
   Retrieved Medical Information:
   [WHO] Pneumonia is an infection...
   ────────────────────────────────────
   AI-Generated Explanation:
   The vision model classified this X-ray...
   ```

5. **Medical disclaimer**
   - Explicit in every response
   - Distinguishes AI classification from diagnosis

### LLM System Prompt Template
```
You are a medical information assistant for an AI triage system.

CONTEXT:
- An AI vision model analyzed a chest X-ray
- Prediction: {prediction}
- Confidence: {confidence}
- Classifier: {classifier_type}

RETRIEVED EVIDENCE:
{evidence_documents}

YOUR TASK:
1. Explain what the AI model detected
2. Provide general medical context using ONLY the retrieved evidence
3. Do NOT diagnose the patient
4. Do NOT prescribe treatment
5. Do NOT invent facts or citations
6. Clearly communicate uncertainty
7. Emphasize need for professional evaluation

Generate a concise, patient-friendly explanation.
```

---

## 📚 KNOWLEDGE BASE CONSTRUCTION

### Phase 1: Initial Corpus (Hackathon MVP)

**Conditions to cover:**
- Pneumonia (bacterial, viral)
- Normal chest X-ray findings
- General triage guidance

**Document categories:**
1. **Overview** — What is the condition?
2. **Symptoms** — Common signs to watch for
3. **Triage** — When to seek care urgently
4. **Risk Factors** — Who is at higher risk?

**Example document:**
```json
{
  "id": "pneumonia_overview_001",
  "condition": "pneumonia",
  "category": "overview",
  "title": "Pneumonia: An Overview",
  "text": "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing. A variety of organisms, including bacteria, viruses and fungi, can cause pneumonia.",
  "source": "Mayo Clinic",
  "url": "https://www.mayoclinic.org/diseases-conditions/pneumonia/symptoms-causes/syc-20354204",
  "retrieved_date": "2026-08-26",
  "chunk_id": 1,
  "total_chunks": 3
}
```

**Initial corpus size:** ~20-30 documents (sufficient for demo)

**Ingestion process:**
```bash
python src/rag/build_knowledge_base.py
```
- Load documents from `data/knowledge/medical_corpus.json`
- Generate embeddings with sentence-transformers
- Build FAISS index
- Save to `data/knowledge/vector_index/`

---

## 🔧 IMPLEMENTATION SEQUENCE

### Stage 1: Dependencies & Environment
1. Test Python 3.14 compatibility with proposed libraries
2. Install dependencies (faiss-cpu, sentence-transformers, openai)
3. Update requirements.txt
4. Create `.env.example` (no secrets)

### Stage 2: Knowledge Base
1. Create `data/knowledge/` directory
2. Curate initial medical corpus (20-30 documents)
3. Write ingestion script
4. Test chunking and metadata preservation

### Stage 3: Vector Database
1. Implement `src/vector_db/embeddings.py`
2. Implement `src/vector_db/faiss_store.py`
3. Test embedding generation
4. Test similarity search
5. Build initial index

### Stage 4: RAG Service
1. Implement `src/rag/retrieval.py`
2. Test query → embedding → search → documents flow
3. Verify source metadata preservation

### Stage 5: LLM Service
1. Implement `src/llm/service.py` (abstract)
2. Implement `src/llm/openai_llm.py`
3. Define prompts in `src/llm/prompts.py`
4. Test with mock prediction data
5. Verify no hallucination/fabrication

### Stage 6: API Integration
1. Create `/intelligence` endpoint
2. Wire vision → RAG → LLM pipeline
3. Implement fallback behavior
4. Test failure scenarios

### Stage 7: Testing
1. Unit tests for each component
2. Integration tests for pipeline
3. End-to-end tests with real X-rays
4. Verify classical + quantum work with intelligence

### Stage 8: Frontend Integration
1. Update `services/api.js` with `/intelligence` call
2. Add Intelligence section to dashboard
3. Display retrieved evidence with sources
4. Show clear attribution (classifier vs LLM)

### Stage 9: Validation
1. Regression tests (existing /predict must work)
2. Model files verification (unchanged)
3. Performance testing
4. Fallback scenario testing

---

## ⚠️ RISKS & MITIGATIONS

### Risk 1: Python 3.14 Compatibility
**Issue:** Some libraries may not support Python 3.14 yet
**Mitigation:**
- Test each dependency individually before full installation
- Have fallback library options ready
- Consider Python 3.11 venv if needed (separate environment)

### Risk 2: Embedding Model Size
**Issue:** sentence-transformers models can be 100-400MB
**Mitigation:**
- Use smallest viable model (all-MiniLM-L6-v2: ~90MB)
- Cache model in `.cache/` (gitignored)
- Download once during setup

### Risk 3: LLM API Costs
**Issue:** OpenAI API calls cost money
**Mitigation:**
- Use GPT-3.5-turbo (cheaper than GPT-4)
- Cache common responses
- Rate limiting
- Budget monitoring

### Risk 4: LLM Hallucination
**Issue:** LLM might fabricate medical facts
**Mitigation:**
- Strict system prompt with grounding instructions
- Explicit "use ONLY retrieved evidence" directive
- Post-generation validation
- Human review of prompt outputs during development

### Risk 5: Response Latency
**Issue:** Intelligence pipeline adds ~2-5s latency
**Mitigation:**
- Async processing where possible
- Frontend loading states
- Optional enhancement (users can opt for faster basic prediction)

---

## 📊 EXPECTED PERFORMANCE

### Latency Breakdown
- Vision classifier: ~50-100ms (classical) / ~6000ms (quantum)
- RAG retrieval: ~100-200ms
- LLM generation: ~1000-3000ms
- **Total intelligence response:** ~1.5-4s (classical) / ~7-10s (quantum)

### Resource Usage
- Vector DB index: ~10-20MB (small corpus)
- Embedding model: ~90MB (cached)
- Peak memory: +500MB (embedding model loaded)

---

## 🎓 HACKATHON DEMONSTRATION VALUE

### What Judges Will See

1. **Upload X-ray** → instant visual feedback
2. **Vision Classification** → "PNEUMONIA detected (92.67%)"
3. **Quantum Enhancement** → "4D quantum feature space"
4. **RAG Retrieval** → "Retrieved 5 medical sources (WHO, CDC, NIH)"
5. **Evidence Display** → Source cards with links
6. **LLM Synthesis** → Natural language explanation
7. **Clear Attribution** → "AI Classification" vs "Medical Information" vs "Generated Explanation"

### Key Differentiators
- ✅ Classical vs Quantum comparison
- ✅ Evidence-grounded (not just LLM chatbot)
- ✅ Real medical sources (not fabricated)
- ✅ Graceful degradation (works even if LLM fails)
- ✅ Production-quality safety design

---

## 📝 FILES TO CREATE (27 files)

### Backend (16 files)
1. `src/rag/__init__.py`
2. `src/rag/ingestion.py`
3. `src/rag/retrieval.py`
4. `src/rag/knowledge_base.py`
5. `src/vector_db/__init__.py`
6. `src/vector_db/embeddings.py`
7. `src/vector_db/faiss_store.py`
8. `src/llm/__init__.py`
9. `src/llm/service.py`
10. `src/llm/openai_llm.py`
11. `src/llm/prompts.py`
12. `data/knowledge/medical_corpus.json`
13. `tests/test_rag_ingestion.py`
14. `tests/test_rag_retrieval.py`
15. `tests/test_llm_service.py`
16. `tests/test_intelligence_e2e.py`

### Configuration (2 files)
17. `.env.example`
18. Updated `requirements.txt`

### Documentation (3 files)
19. `docs/INTELLIGENCE_LAYER.md`
20. `docs/KNOWLEDGE_SOURCES.md`
21. Updated `README.md`

### Scripts (3 files)
22. `scripts/build_knowledge_base.py`
23. `scripts/test_intelligence.py`
24. `scripts/validate_rag.py`

### Frontend (3 files)
25. Updated `dashboard/src/services/api.js`
26. Updated `dashboard/src/App.jsx`
27. `dashboard/src/components/IntelligenceDisplay.jsx` (new)

### Modified (2 files)
- `src/api/main.py` (add /intelligence endpoint)
- `README.md` (update with Phase 2 status)

---

## 🚫 FILES THAT MUST NOT BE MODIFIED

- ❌ `models/classical_svm.pkl`
- ❌ `models/quantum_svm.pkl`
- ❌ `models/pca_reducer.pkl`
- ❌ `src/inference/predict.py` (core logic)
- ❌ `src/models/quantum_svm.py` (model class)
- ❌ `src/models/classical_svm.py` (model class)
- ❌ Any training scripts

---

## ✅ APPROVAL CHECKLIST

Before implementation begins:

- [ ] Architecture reviewed
- [ ] Python 3.14 compatibility verified
- [ ] Dependency list approved
- [ ] API design confirmed
- [ ] Knowledge base sources approved
- [ ] LLM provider confirmed (OpenAI vs alternative)
- [ ] Safety requirements understood
- [ ] Fallback behavior approved
- [ ] Implementation sequence agreed
- [ ] Git commit strategy discussed

---

## 🎯 SUCCESS CRITERIA

### Functional Requirements
1. ✅ Vision classifier predictions remain unchanged
2. ✅ Intelligence layer adds medical context
3. ✅ RAG retrieves relevant evidence with sources
4. ✅ LLM generates grounded explanations
5. ✅ System works with both classical and quantum classifiers
6. ✅ Graceful degradation on failure
7. ✅ Frontend displays intelligence with clear attribution

### Safety Requirements
1. ✅ LLM never overrides classifier prediction
2. ✅ All medical claims cite retrieved sources
3. ✅ No fabricated citations or statistics
4. ✅ Medical disclaimer in every response
5. ✅ Clear distinction: AI classification ≠ diagnosis

### Technical Requirements
1. ✅ No model files modified
2. ✅ Existing /predict endpoint works unchanged
3. ✅ Tests pass (existing + new)
4. ✅ Frontend builds successfully
5. ✅ API keys not committed

---

## 🚀 READY FOR IMPLEMENTATION?

**Current Status:** AUDIT COMPLETE

**Next Action:** AWAITING APPROVAL

Once approved, implementation will proceed stage-by-stage with incremental testing and validation at each stage.

**Estimated Implementation Time:** 4-6 hours (excluding knowledge base curation)

---

**Document Version:** 1.0  
**Author:** Kiro AI Assistant  
**Date:** August 26, 2026
