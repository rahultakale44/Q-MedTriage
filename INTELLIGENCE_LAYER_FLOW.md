# Intelligence Layer — Data Flow Diagram

## Complete Pipeline Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                         [ Upload X-ray Image ]
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI: /intelligence                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 1: VISION CLASSIFICATION                    │
│                   (EXISTING — UNCHANGED)                            │
├─────────────────────────────────────────────────────────────────────┤
│  Image (JPEG)                                                       │
│    ↓                                                                │
│  Preprocessing (224x224, grayscale→RGB, normalize)                 │
│    ↓                                                                │
│  ResNet50 Feature Extraction                                        │
│    → 2048D feature vector                                           │
│    ↓                                                                │
│  PCA Dimensionality Reduction                                       │
│    → 4D feature vector                                              │
│    ↓                                                                │
│  Classical SVM / Quantum SVM                                        │
│    → prediction: 1 (PNEUMONIA)                                      │
│    → confidence: 0.9267                                             │
│    → probabilities: {NORMAL: 0.0733, PNEUMONIA: 0.9267}            │
│    ↓                                                                │
│  ✅ RESULT: Structured prediction                                  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 2: RAG QUERY GENERATION                     │
│                   (NEW)                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Input:                                                             │
│    - prediction: "PNEUMONIA"                                        │
│    - confidence: 0.9267                                             │
│    ↓                                                                │
│  Construct Query:                                                   │
│    "Provide general medical information about pneumonia             │
│     for AI-assisted triage context. Include symptoms,              │
│     when to seek care, and general risk factors."                  │
│    ↓                                                                │
│  ✅ RESULT: Structured RAG query                                   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 3: EMBEDDING GENERATION                     │
│                   (NEW)                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Query String                                                       │
│    ↓                                                                │
│  sentence-transformers (all-MiniLM-L6-v2)                          │
│    → 384D embedding vector                                          │
│    ↓                                                                │
│  Normalize vector (L2 norm)                                         │
│    ↓                                                                │
│  ✅ RESULT: Query embedding (384D)                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 4: VECTOR SIMILARITY SEARCH                 │
│                   (NEW)                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Query Embedding (384D)                                             │
│    ↓                                                                │
│  FAISS Index Search (IndexFlatL2)                                   │
│    - Compare with all document embeddings                           │
│    - Retrieve top k=5 most similar                                  │
│    ↓                                                                │
│  Retrieved Documents:                                               │
│    1. [WHO] "Pneumonia: Overview" (similarity: 0.89)               │
│    2. [CDC] "Pneumonia Symptoms" (similarity: 0.85)                │
│    3. [NIH] "When to Seek Care" (similarity: 0.82)                 │
│    4. [Mayo] "Pneumonia Risk Factors" (similarity: 0.79)           │
│    5. [WHO] "Pneumonia Treatment" (similarity: 0.76)               │
│    ↓                                                                │
│  Extract Metadata:                                                  │
│    - Document text                                                  │
│    - Source (WHO, CDC, NIH, Mayo)                                  │
│    - Title                                                          │
│    - URL                                                            │
│    - Retrieved date                                                 │
│    ↓                                                                │
│  ✅ RESULT: Top 5 evidence documents with metadata                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 5: LLM SYNTHESIS                            │
│                   (NEW)                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Build LLM Prompt:                                                  │
│                                                                     │
│    SYSTEM:                                                          │
│    You are a medical information assistant for an AI triage        │
│    system. You provide evidence-grounded explanations.             │
│                                                                     │
│    CRITICAL RULES:                                                  │
│    - Do NOT change the AI prediction                               │
│    - Use ONLY the retrieved evidence                               │
│    - Do NOT diagnose the patient                                   │
│    - Do NOT prescribe treatment                                    │
│    - Do NOT invent facts or citations                              │
│    - Clearly communicate uncertainty                               │
│    - Emphasize professional evaluation needed                      │
│                                                                     │
│    CONTEXT:                                                         │
│    - AI Prediction: PNEUMONIA                                      │
│    - Confidence: 92.67%                                            │
│    - Classifier: Classical SVM                                     │
│                                                                     │
│    RETRIEVED EVIDENCE:                                              │
│    [Document 1: WHO - Pneumonia Overview]                          │
│    "Pneumonia is an infection that inflames the air sacs..."       │
│                                                                     │
│    [Document 2: CDC - Pneumonia Symptoms]                          │
│    "Common symptoms include cough, fever, chills..."               │
│                                                                     │
│    [... 3 more documents ...]                                       │
│                                                                     │
│    USER:                                                            │
│    Generate a concise, patient-friendly explanation of the AI      │
│    classification result and relevant medical context.             │
│    ↓                                                                │
│  OpenAI API Call (GPT-3.5-turbo / GPT-4)                           │
│    ↓                                                                │
│  LLM Generated Response:                                            │
│    "The AI vision model analyzed the uploaded chest X-ray and      │
│     classified it as showing signs consistent with pneumonia,      │
│     with 92.67% confidence.                                         │
│                                                                     │
│     According to the World Health Organization, pneumonia is       │
│     an infection that inflames the air sacs in one or both lungs.  │
│     The CDC notes that common symptoms include cough with phlegm,  │
│     fever, chills, and difficulty breathing.                       │
│                                                                     │
│     This AI classification is for research and triage assistance   │
│     purposes only. It is not a medical diagnosis. If you are       │
│     experiencing respiratory symptoms, please seek evaluation      │
│     from a qualified healthcare provider for proper diagnosis      │
│     and treatment."                                                 │
│    ↓                                                                │
│  ✅ RESULT: Grounded, patient-friendly explanation                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 6: RESPONSE ASSEMBLY                        │
│                   (NEW)                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Combine all components:                                            │
│                                                                     │
│  {                                                                  │
│    "success": true,                                                 │
│    "prediction": {                                                  │
│      "model": "Classical SVM",                                     │
│      "prediction": 1,                                              │
│      "prediction_label": "PNEUMONIA",                              │
│      "confidence": 0.9267,                                         │
│      "probabilities": {                                            │
│        "NORMAL": 0.0733,                                           │
│        "PNEUMONIA": 0.9267                                         │
│      },                                                            │
│      "inference_time_ms": 46.7,                                    │
│      "classifier": "classical"                                     │
│    },                                                              │
│    "intelligence": {                                               │
│      "medical_context": "The AI vision model analyzed...",        │
│      "retrieved_evidence": [                                       │
│        {                                                           │
│          "id": "pneumonia_overview_001",                           │
│          "title": "Pneumonia: Overview",                           │
│          "text": "Pneumonia is an infection...",                  │
│          "source": "WHO",                                          │
│          "url": "https://www.who.int/...",                         │
│          "similarity_score": 0.89                                  │
│        },                                                          │
│        ... 4 more documents ...                                    │
│      ],                                                            │
│      "explanation": "The AI vision model analyzed...",            │
│      "triage_guidance": "Seek medical evaluation...",             │
│      "disclaimer": "This AI classification is for research..."     │
│    },                                                              │
│    "filename": "xray.jpeg"                                         │
│  }                                                                  │
│    ↓                                                                │
│  ✅ RESULT: Complete intelligence response                         │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   REACT DASHBOARD DISPLAY                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌─────────────────────────────────────────┐
        │      AI CLASSIFICATION RESULT           │
        ├─────────────────────────────────────────┤
        │  Prediction: PNEUMONIA                  │
        │  Confidence: 92.67%                     │
        │  Classifier: Classical SVM              │
        │  Time: 46.7ms                           │
        └─────────────────────────────────────────┘
                                  │
                                  ▼
        ┌─────────────────────────────────────────┐
        │      MEDICAL CONTEXT                    │
        ├─────────────────────────────────────────┤
        │  The AI vision model analyzed the       │
        │  uploaded chest X-ray and classified    │
        │  it as showing signs consistent with    │
        │  pneumonia, with 92.67% confidence.     │
        │                                         │
        │  According to the World Health          │
        │  Organization, pneumonia is an          │
        │  infection that inflames the air        │
        │  sacs in one or both lungs...           │
        └─────────────────────────────────────────┘
                                  │
                                  ▼
        ┌─────────────────────────────────────────┐
        │      EVIDENCE SOURCES                   │
        ├─────────────────────────────────────────┤
        │  📄 WHO: Pneumonia Overview             │
        │     🔗 www.who.int/...                  │
        │                                         │
        │  📄 CDC: Pneumonia Symptoms             │
        │     🔗 www.cdc.gov/...                  │
        │                                         │
        │  📄 NIH: When to Seek Care              │
        │     🔗 www.nih.gov/...                  │
        │                                         │
        │  [Show 2 more sources...]               │
        └─────────────────────────────────────────┘
                                  │
                                  ▼
        ┌─────────────────────────────────────────┐
        │      DISCLAIMER                         │
        ├─────────────────────────────────────────┤
        │  ⚠️ This AI classification is for       │
        │  research and triage assistance         │
        │  purposes only. It is not a medical     │
        │  diagnosis. Please seek evaluation      │
        │  from a qualified healthcare provider.  │
        └─────────────────────────────────────────┘
```

---

## Fallback Behavior (Intelligence Layer Failure)

```
┌─────────────────────────────────────────────────────────────────────┐
│                   IF RAG/LLM FAILS                                  │
├─────────────────────────────────────────────────────────────────────┤
│  Vision Classification: ✅ SUCCESS                                  │
│    ↓                                                                │
│  RAG Retrieval: ❌ FAILED (no documents / embedding error)          │
│    OR                                                               │
│  LLM Synthesis: ❌ FAILED (API error / timeout)                     │
│    ↓                                                                │
│  Response:                                                          │
│  {                                                                  │
│    "success": true,                                                 │
│    "prediction": {                                                  │
│      ... full prediction data ...                                  │
│    },                                                              │
│    "intelligence": {                                               │
│      "error": "Intelligence service temporarily unavailable",      │
│      "fallback": true                                              │
│    }                                                                │
│  }                                                                  │
│    ↓                                                                │
│  ✅ USER STILL GETS: Prediction, confidence, probabilities         │
│  ⚠️ USER DOES NOT GET: Medical context, evidence, explanation      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Performance Timing Breakdown

### Classical SVM Path
```
Total: ~1.5-4s
├─ Image preprocessing:        10ms
├─ ResNet50 extraction:        30ms
├─ PCA reduction:              5ms
├─ Classical SVM:              5ms
├─ RAG query generation:       5ms
├─ Query embedding:            50ms
├─ Vector search (FAISS):      50ms
├─ LLM API call:               1000-3000ms
└─ Response assembly:          10ms
```

### Quantum SVM Path
```
Total: ~7-10s
├─ Image preprocessing:        10ms
├─ ResNet50 extraction:        30ms
├─ PCA reduction:              5ms
├─ Quantum SVM:                6000ms  ← Simulator overhead
├─ RAG query generation:       5ms
├─ Query embedding:            50ms
├─ Vector search (FAISS):      50ms
├─ LLM API call:               1000-3000ms
└─ Response assembly:          10ms
```

---

## Data Size Reference

```
Component                Size        Location
────────────────────────────────────────────────────────────
ResNet50 model          ~100MB      Cached by PyTorch
PCA model               ~1KB        models/pca_reducer.pkl
Classical SVM           ~10KB       models/classical_svm.pkl
Quantum SVM             ~50KB       models/quantum_svm.pkl
Embedding model         ~90MB       .cache/sentence-transformers/
Medical corpus (JSON)   ~100KB      data/knowledge/medical_corpus.json
FAISS index             ~10MB       data/knowledge/vector_index/
Vector metadata         ~50KB       data/knowledge/vector_index/metadata.json
```

---

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRUSTED                                      │
├─────────────────────────────────────────────────────────────────────┤
│  - Trained models (classical_svm.pkl, quantum_svm.pkl, pca)        │
│  - ResNet50 (PyTorch official weights)                             │
│  - Local vector database (FAISS)                                    │
│  - Curated knowledge corpus (verified sources)                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        UNTRUSTED                                    │
├─────────────────────────────────────────────────────────────────────┤
│  - User uploaded images (validated before processing)              │
│  - LLM generated text (validated against retrieved evidence)       │
│  - External API responses (error handling required)                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        NEVER STORED                                 │
├─────────────────────────────────────────────────────────────────────┤
│  - API keys (environment variables only)                            │
│  - Patient identifying information (if uploaded)                   │
│  - Raw uploaded images (processed in memory only)                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

**Document Purpose:** Visual reference for Intelligence Layer architecture  
**Target Audience:** Developers, reviewers, hackathon judges  
**Last Updated:** August 26, 2026
