# PHASE 2 — Intelligence Layer Audit Summary

## Date: August 26, 2026
## Status: ✅ AUDIT COMPLETE — AWAITING APPROVAL FOR IMPLEMENTATION

---

## 📊 AUDIT RESULTS

### ✅ Current System Status
- **Pipeline:** Fully functional (X-ray → ResNet50 → PCA → Classical/Quantum SVM)
- **API:** FastAPI server running on Python 3.14.4 via `.venv`
- **Models:** All trained and verified (UNTOUCHED)
- **Frontend:** React dashboard builds successfully
- **Test Results:** Classical and Quantum SVM both working correctly

### 🏗️ Existing Infrastructure
- **RAG directories:** `src/rag/`, `src/llm/`, `src/vector_db/` already exist but are EMPTY
- **API stub:** `/ask` endpoint exists but returns placeholder
- **Dependencies:** Core ML stack installed (torch, qiskit, scikit-learn, fastapi)

### ❌ What's Missing for Intelligence Layer
- FAISS (vector database)
- sentence-transformers (embeddings)
- openai (LLM service)
- Medical knowledge corpus
- RAG retrieval service
- LLM synthesis service
- Intelligence API endpoint

---

## 🎯 PROPOSED SOLUTION

### Architecture Overview
```
Image → Vision Classifier → Prediction
                              ↓
                         RAG Query Generation
                              ↓
                         Embedding (sentence-transformers)
                              ↓
                         Vector Search (FAISS)
                              ↓
                         Retrieved Evidence (5 docs)
                              ↓
                         LLM Synthesis (OpenAI GPT)
                              ↓
                         Intelligence Response
```

### Key Design Decisions

1. **Vector Database: FAISS**
   - Lightweight, local, deterministic
   - No external services required
   - Proven performance

2. **Embeddings: sentence-transformers**
   - Model: `all-MiniLM-L6-v2` (384D, ~90MB)
   - Local inference (no API calls)
   - Fast embedding generation

3. **LLM: OpenAI GPT-3.5/4 API**
   - Reliable, high-quality
   - Swappable architecture (abstract interface)
   - Environment variable for API key

4. **Knowledge Base: Custom Medical Corpus**
   - Sources: WHO, CDC, NIH, Mayo Clinic
   - 20-30 documents initially (expandable)
   - JSON format with metadata preservation

5. **API Design: Separate Endpoint**
   - New: `POST /intelligence` (vision + RAG + LLM)
   - Unchanged: `POST /predict` (vision only)
   - Graceful fallback if intelligence fails

---

## 🛡️ SAFETY GUARANTEES

### Non-Negotiable Rules
1. ✅ LLM cannot override classifier prediction
2. ✅ Prediction remains in separate structured field
3. ✅ All medical claims cite retrieved evidence
4. ✅ No fabricated sources allowed
5. ✅ Intelligence failure → fallback to basic prediction
6. ✅ Vision classifier never depends on LLM
7. ✅ Clear medical disclaimer in every response
8. ✅ Attribution: AI classification vs retrieved info vs generated text

### LLM Safety Prompt
```
CRITICAL INSTRUCTIONS:
- You CANNOT change the AI prediction
- Use ONLY retrieved evidence for medical facts
- Do NOT diagnose the patient
- Do NOT prescribe treatment
- Do NOT invent citations
- Communicate uncertainty clearly
- Emphasize professional evaluation needed
```

---

## 📋 IMPLEMENTATION PLAN

### Stage 1: Dependencies & Compatibility Testing ⏱️ 30 min
- Install faiss-cpu, sentence-transformers, openai
- Test Python 3.14 compatibility
- Update requirements.txt
- Create .env.example

### Stage 2: Knowledge Base Construction ⏱️ 60 min
- Curate 20-30 authoritative medical documents
- Create `data/knowledge/medical_corpus.json`
- Implement ingestion script
- Test chunking and metadata

### Stage 3: Vector Database ⏱️ 45 min
- Implement embedding generation
- Implement FAISS index creation
- Build initial vector index
- Test similarity search

### Stage 4: RAG Retrieval Service ⏱️ 45 min
- Implement query embedding
- Implement document retrieval
- Test with sample queries
- Verify source metadata preservation

### Stage 5: LLM Service ⏱️ 45 min
- Implement abstract LLM interface
- Implement OpenAI integration
- Create safety-focused prompts
- Test with mock data

### Stage 6: API Integration ⏱️ 45 min
- Create `/intelligence` endpoint
- Wire vision → RAG → LLM pipeline
- Implement fallback behavior
- Test with real X-rays

### Stage 7: Testing ⏱️ 60 min
- Unit tests for each component
- Integration tests
- End-to-end tests (classical + quantum)
- Failure scenario tests
- Regression tests

### Stage 8: Frontend Integration ⏱️ 60 min
- Update API service client
- Add Intelligence display section
- Show retrieved evidence with sources
- Clear attribution UI

### Stage 9: Validation ⏱️ 30 min
- Verify model files unchanged
- Run all existing tests
- Performance benchmarking
- Final smoke tests

**Total Estimated Time:** 5-6 hours

---

## ⚠️ KNOWN RISKS

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Python 3.14 incompatibility | Medium | High | Test each library individually; fallback options |
| LLM API costs | Low | Medium | Use GPT-3.5-turbo; cache responses |
| LLM hallucination | Medium | High | Strict prompts; evidence grounding; validation |
| Response latency | High | Low | Async processing; loading states |
| Model file corruption | Low | Critical | Git status checks; no training scripts run |

---

## 📈 EXPECTED PERFORMANCE

### Response Times
- Classical inference: ~1.5-4s total (vision 0.1s + RAG 0.2s + LLM 1-3s)
- Quantum inference: ~7-10s total (vision 6s + RAG 0.2s + LLM 1-3s)

### Resource Usage
- Vector DB: ~10-20MB
- Embedding model: ~90MB (cached)
- Memory: +500MB peak

### Quality Metrics
- Retrieval relevance: >0.7 similarity score
- LLM grounding: 100% claims cited
- Fallback rate: <5% (if LLM fails)

---

## 📁 FILES TO CREATE

### Backend Core (11 files)
```
src/rag/__init__.py
src/rag/ingestion.py
src/rag/retrieval.py
src/rag/knowledge_base.py
src/vector_db/__init__.py
src/vector_db/embeddings.py
src/vector_db/faiss_store.py
src/llm/__init__.py
src/llm/service.py
src/llm/openai_llm.py
src/llm/prompts.py
```

### Data & Knowledge (1 file)
```
data/knowledge/medical_corpus.json
```

### Tests (5 files)
```
tests/test_rag_ingestion.py
tests/test_rag_retrieval.py
tests/test_llm_service.py
tests/test_intelligence_api.py
tests/test_intelligence_e2e.py
```

### Configuration (2 files)
```
.env.example
requirements.txt (updated)
```

### Scripts (3 files)
```
scripts/build_knowledge_base.py
scripts/test_intelligence.py
scripts/validate_rag.py
```

### Frontend (2 files)
```
dashboard/src/components/IntelligenceDisplay.jsx (new)
dashboard/src/services/api.js (updated)
```

### Documentation (2 files)
```
docs/INTELLIGENCE_LAYER.md
docs/KNOWLEDGE_SOURCES.md
```

### Modified (2 files)
```
src/api/main.py (add /intelligence endpoint)
dashboard/src/App.jsx (add intelligence display)
```

**Total: 28 files** (16 new, 4 updated, 8 supporting)

---

## 🚫 FILES NEVER TO MODIFY

```
models/classical_svm.pkl       ❌ NO TOUCH
models/quantum_svm.pkl         ❌ NO TOUCH
models/pca_reducer.pkl         ❌ NO TOUCH
src/inference/predict.py       ❌ NO TOUCH (core logic)
src/models/*.py               ❌ NO TOUCH (model definitions)
Any training scripts          ❌ NO TOUCH
```

---

## ✅ APPROVAL REQUIRED

Before proceeding with implementation, please confirm:

- [ ] **Architecture approved** — FAISS + sentence-transformers + OpenAI
- [ ] **API design approved** — Separate `/intelligence` endpoint
- [ ] **Knowledge sources approved** — WHO, CDC, NIH, Mayo Clinic
- [ ] **Safety rules approved** — LLM grounding, no override, fallback
- [ ] **Implementation sequence approved** — 9-stage plan
- [ ] **OpenAI API key available** — For LLM service (or alternative provider)
- [ ] **Timeline acceptable** — 5-6 hours estimated

---

## 🎯 SUCCESS CRITERIA

### Must Have ✅
1. Vision classifier predictions unchanged
2. Intelligence layer adds medical context
3. RAG retrieves relevant evidence with sources
4. LLM generates grounded explanations
5. Works with classical AND quantum classifiers
6. Graceful fallback on failure
7. Frontend displays intelligence clearly

### Must NOT Have ❌
1. Modified model files
2. Changed training results
3. Broken /predict endpoint
4. Fabricated citations
5. LLM overriding classifier
6. Committed API keys
7. Failed regression tests

---

## 🚀 NEXT STEPS

**Current Status:** Awaiting approval to proceed

**Once approved:**
1. Install dependencies with compatibility testing
2. Build knowledge base (medical corpus curation)
3. Implement RAG pipeline incrementally
4. Test at each stage
5. Integrate with API
6. Update frontend
7. Full validation

**Estimated start time:** Immediately upon approval  
**Estimated completion:** 5-6 hours (same day)

---

## 📞 QUESTIONS FOR USER

1. **LLM Provider:** Confirm OpenAI GPT-3.5/4, or prefer alternative (Claude, local LLM)?
2. **API Key:** Is OpenAI API key available in environment?
3. **Knowledge Base:** Should we include any specific medical sources beyond WHO/CDC/NIH?
4. **Performance:** Is 1-4s total response time acceptable for hackathon demo?
5. **Scope:** Should intelligence layer be mandatory or optional (toggle)?

---

**Audit Completed By:** Kiro AI Assistant  
**Review Date:** August 26, 2026  
**Approval Status:** ⏳ PENDING
