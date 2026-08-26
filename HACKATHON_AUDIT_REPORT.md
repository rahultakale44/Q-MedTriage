# Q-MedTriage Hackathon Readiness Audit
## Comprehensive Project Analysis & Improvement Strategy

**Date**: 2026-08-26  
**Status**: Pre-Hackathon Optimization Phase  
**Objective**: Transform from experiment to demo-ready medical AI system

---

## A. CURRENT ARCHITECTURE

### Pipeline Components

```
Medical X-ray Image
    ↓
[1] PREPROCESSING (data/preprocess.py)
    ├─ Resize 224×224
    ├─ Normalize (ImageNet standards)
    └─ Augmentation (training only)
    ↓
[2] FEATURE EXTRACTION (models/cnn_features.py)
    ├─ ResNet50 pretrained backbone
    └─ Output: 2048D feature vector
    ↓
[3] PCA REDUCTION (models/apply_pca.py)
    ├─ 2048D → 4D compression
    └─ Frozen PCA model (pca_reducer.pkl)
    ↓
[4] CLASSICAL SVM (models/classical_svm.py)
    ├─ RBF kernel, C=1.0
    ├─ Accuracy: 92.05%
    ├─ ROC-AUC: 97.20%
    └─ Model: classical_svm.pkl
    ↓
[5] QUANTUM SVM (models/quantum_svm.py)
    ├─ 4-qubit ZZFeatureMap
    ├─ FidelityQuantumKernel
    ├─ Accuracy: 61.22%
    ├─ ROC-AUC: 47.03%
    └─ Model: quantum_svm.pkl
    ↓
[6] TRIAGE OUTPUT
    └─ NORMAL vs PNEUMONIA classification
```

### Frontend Architecture

**Location**: `dashboard/`  
**Tech Stack**: React + Vite + Framer Motion + Lucide Icons  
**Current State**: ✅ **FULLY IMPLEMENTED** stunning scrolling storytelling UI

**Components**:
- Hero section with animated quantum core
- 8-stage pipeline visualization
- Auto-run demo mode
- Image upload capability
- Stage-by-stage animated transitions
- Sticky visualization panel
- Progress indicators

**UI Stages**:
1. INPUT - Image upload
2. PREPROCESS - Normalization steps
3. VISION (CNN) - Feature extraction
4. REDUCTION (PCA) - Dimensionality reduction
5. QUANTUM - 4-qubit circuit
6. EVIDENCE - Vector DB retrieval (placeholder)
7. REASONING - LLM synthesis (placeholder)
8. TRIAGE - Final classification

**Demo Data**: Uses deterministic mock data (shows "NODULE" detection - needs update to "PNEUMONIA")

### Backend Architecture

**Location**: `src/api/main.py`  
**Tech Stack**: FastAPI  
**Current State**: ⚠️ **STUB IMPLEMENTATION**

**Endpoints**:
- `GET /` - Status check
- `GET /health` - Component health  
- `POST /predict` - Image prediction (not connected)
- `POST /ask` - RAG Q&A (not connected)

### Saved Models

| Model | Location | Status | Performance |
|-------|----------|--------|-------------|
| **PCA Reducer** | `models/pca_reducer.pkl` | ✅ Ready | 2048D→4D |
| **Classical SVM** | `models/classical_svm.pkl` | ✅ Ready | 92% Acc, 97% AUC |
| **Quantum SVM** | `models/quantum_svm.pkl` | ✅ Ready | 61% Acc, 47% AUC |

### Missing Components

❌ **NOT IMPLEMENTED**:
- End-to-end inference pipeline (image → prediction)
- Backend-frontend integration
- Real-time prediction API
- GradCAM or visual explainability
- Vector database (FAISS) with medical knowledge
- RAG system with retrieval
- LLM explanation synthesis
- Performance dashboard with real metrics
- Confusion matrix visualization
- ROC curve plots
- Model comparison charts

---

## B. CURRENT PROJECT CAPABILITIES

### ✅ WHAT WORKS

**Machine Learning**:
- ✅ Complete preprocessing pipeline
- ✅ ResNet50 feature extraction (tested)
- ✅ PCA reduction pipeline (frozen, validated)
- ✅ Classical SVM trained (excellent: 92% accuracy)
- ✅ Quantum SVM trained (poor: 61% accuracy, retained for comparison)
- ✅ Both models saved and loadable
- ✅ Reproducible train/val/test splits (fixed seed 42)
- ✅ 1,332 lines of tests across 7 test files

**Frontend**:
- ✅ Stunning scrolling storytelling UI
- ✅ Image upload functionality
- ✅ Auto-run demo mode
- ✅ 8-stage animated pipeline visualization
- ✅ Quantum circuit visualization
- ✅ Professional design with animations
- ✅ Medical disclaimer present

**Data**:
- ✅ Kermany Chest X-Ray dataset (5,856 images)
- ✅ NORMAL vs PNEUMONIA classification
- ✅ Proper train/val/test splits
- ✅ No data leakage (validated)

### ⚠️ PARTIALLY WORKS

**Backend API**:
- ⚠️ FastAPI stub exists
- ⚠️ Endpoints defined but not functional
- ⚠️ No actual prediction pipeline connected

**Demo Data**:
- ⚠️ Shows "NODULE" detection (wrong task)
- ⚠️ Should show "PNEUMONIA" detection
- ⚠️ Quantum metrics in demo data are optimistic (94% vs actual 61%)

### ❌ DOESN'T WORK

**Critical Missing Pieces**:
- ❌ No inference.py script (image → prediction workflow)
- ❌ Backend /predict endpoint not functional
- ❌ Frontend can't call real backend
- ❌ No visual explainability (GradCAM)
- ❌ No performance dashboard
- ❌ No confusion matrix visualization
- ❌ No ROC curve plots
- ❌ No model comparison charts
- ❌ RAG system (vector DB + LLM) not implemented
- ❌ Evidence retrieval is placeholder
- ❌ LLM reasoning is placeholder

---

## C. CURRENT UI/DEMO QUALITY

### Strengths: 9/10 🌟

**Exceptional**:
- ✅ Gorgeous scrolling storytelling experience
- ✅ Smooth animations and transitions
- ✅ Professional medical-tech aesthetic
- ✅ Clear stage-by-stage flow
- ✅ Auto-run demo mode works perfectly
- ✅ Image upload UX is intuitive
- ✅ Quantum circuit visualization is impressive
- ✅ Medical disclaimer is present and appropriate

**UI Polish Level**: **PRODUCTION-GRADE**

### Weaknesses

**Critical Issues**:
1. **Demo Data Mismatch**: Shows "NODULE" detection, should be "PNEUMONIA"
2. **Fake Metrics**: Demo shows 94.7% quantum accuracy (actual: 61.22%)
3. **No Real Predictions**: Upload doesn't trigger actual inference
4. **Placeholder Stages**: Evidence + Reasoning stages show fake data
5. **No Performance Comparison**: Can't see Classical (92%) vs Quantum (61%) comparison
6. **No Model Metrics Dashboard**: No confusion matrices, ROC curves, etc.

**Missing For Hackathon**:
- Real-time prediction results
- Actual model confidence display
- Honest quantum performance comparison
- Performance metrics visualization
- Explainability (where did model look?)

---

## D. CURRENT ML QUALITY

### Classical SVM: 9/10 ⭐

**Performance** (from validation metrics):
- Accuracy: 92.05%
- Precision: 95.17%
- Recall: 94.06%
- F1 Score: 94.61%
- ROC-AUC: 97.20%

**Status**: ✅ **EXCELLENT** - Production-grade performance

**Strengths**:
- Balanced metrics across all categories
- Excellent discrimination (97% AUC)
- Trained on full 4,172 samples
- Well-calibrated probabilities

### Quantum SVM: 3/10 ⚠️

**Performance** (from test metrics):
- Accuracy: 61.22%
- Precision: 62.17%
- Recall: 96.92%
- F1 Score: 75.75%
- ROC-AUC: 47.03% (worse than random!)
- Specificity: 1.71% (catastrophic)

**Status**: ❌ **POOR** - Research demonstration only

**Issues**:
- Predicts PNEUMONIA 97.4% of the time
- False positive rate: 98.29%
- ROC-AUC below 0.5 = no discrimination
- Only advantage: 2.86% higher recall than classical

**Value**: ✅ Demonstrates quantum ML limitations honestly

---

## E. CURRENT DOCUMENTATION QUALITY

### README.md: 7/10

**Strengths**:
- ✅ Clear project description
- ✅ Dataset details and stats
- ✅ Pipeline overview
- ✅ Reproducibility instructions
- ✅ Medical disclaimer

**Weaknesses**:
- ⚠️ Status shows "COMMIT 09/30" but project is further along
- ⚠️ Mentions "Streamlit interface" but uses React dashboard
- ⚠️ Doesn't explain quantum results honestly
- ⚠️ Missing quickstart/demo instructions
- ⚠️ No architecture diagram
- ⚠️ No performance comparison section

### Technical Documentation: 8/10

**Strengths**:
- ✅ QSVM_FINAL_VALIDATION_REPORT.md (excellent analysis)
- ✅ QSVM_ANALYSIS_REPORT.md (comprehensive)
- ✅ Multiple commit summary documents
- ✅ Honest about QSVM limitations

**Weaknesses**:
- ⚠️ Too many intermediate documents (confusing)
- ⚠️ No single "hackathon presentation" document
- ⚠️ Missing: How to run demo
- ⚠️ Missing: Architecture overview
- ⚠️ Missing: Model comparison narrative

---

## F. HACKATHON SCORECARD

| Category | Score | Rationale |
|----------|-------|-----------|
| **Problem Significance** | 9/10 | Pneumonia detection is critical, real medical need |
| **Innovation** | 8/10 | Quantum ML + RAG concept is novel (even if QSVM underperforms) |
| **Technical Depth** | 7/10 | Strong ML pipeline, but RAG/LLM not implemented |
| **Model Performance** | 8/10 | Classical SVM is excellent (92%), honest quantum comparison |
| **Clinical Usefulness** | 5/10 | Good metrics but no explainability, not production-ready |
| **Explainability** | 2/10 | ❌ **CRITICAL GAP** - No GradCAM, no attention, no visual explanation |
| **User Experience** | 9/10 | Gorgeous UI, but doesn't show real predictions |
| **Demo Quality** | 6/10 | Beautiful flow, but fake data undermines credibility |
| **Reproducibility** | 8/10 | Good tests, fixed seeds, but inference pipeline missing |
| **Documentation** | 7/10 | Comprehensive technical docs, needs demo-focused guide |
| **Presentation Potential** | 7/10 | Strong story, but needs honest quantum narrative |

**Overall Score**: **7.0/10** ⭐⭐⭐⭐⭐⭐⭐☆☆☆

### What's Holding Us Back

**Top 3 Critical Gaps**:
1. ❌ **No Explainability** (worth -2 points) - Can't show WHERE model looked
2. ❌ **Fake Demo Data** (worth -1 point) - Undermines technical credibility
3. ❌ **Missing Backend Integration** (worth -1 point) - Can't do real predictions

**If Fixed**: Potential score **9.5/10** 🎯

---

## G. TOP 5 HIGHEST-IMPACT IMPROVEMENTS

### 🥇 #1: END-TO-END INFERENCE PIPELINE

**What to Change**:
Create `src/inference/predict.py` that takes an image and returns classification with confidence

**Implementation**:
```python
def predict_xray(image_path):
    # 1. Load image
    # 2. Preprocess (224x224, normalize)
    # 3. Extract ResNet50 features (2048D)
    # 4. Apply PCA (2048D → 4D)
    # 5. Predict with Classical SVM
    # 6. Predict with Quantum SVM (optional)
    # 7. Return: {classification, confidence, classical_result, quantum_result}
```

**Why It Matters**:
- Enables real predictions in demo
- Connects frontend to actual models
- Shows technical competence
- Required for any real demo

**Difficulty**: Medium  
**Risk**: Low (all components exist, just need integration)  
**Expected Hackathon Impact**: **+1.5 points**

**Files Likely Affected**:
- NEW: `src/inference/predict.py`
- NEW: `src/inference/__init__.py`
- UPDATE: `src/api/main.py` (connect /predict endpoint)
- UPDATE: `dashboard/src/services/api.js` (call real API)

---

### 🥈 #2: HONEST PERFORMANCE COMPARISON DASHBOARD

**What to Change**:
Create a performance comparison section showing Classical vs Quantum metrics with visualizations

**Implementation**:
```python
# NEW: src/visualization/model_comparison.py
def generate_comparison_charts():
    # 1. Load both model results from JSON
    # 2. Create side-by-side confusion matrices
    # 3. Generate ROC curves
    # 4. Create metrics comparison bar chart
    # 5. Export as images for dashboard
```

**Frontend Component**:
- Add "PERFORMANCE" section after TRIAGE stage
- Show Classical (92%) vs Quantum (61%) honestly
- Display confusion matrices as heatmaps
- Show ROC curves
- Explain why classical won

**Why It Matters**:
- Demonstrates scientific rigor
- Shows you understand trade-offs
- Turns "quantum failed" into "valuable comparison"
- Judges love honest negative results

**Difficulty**: Medium  
**Risk**: Low  
**Expected Hackathon Impact**: **+1.0 points**

**Files Likely Affected**:
- NEW: `src/visualization/model_comparison.py`
- NEW: `dashboard/src/components/PerformanceComparison.jsx`
- UPDATE: `dashboard/src/App.jsx` (add performance section)
- NEW: `results/confusion_matrix_classical.png`
- NEW: `results/confusion_matrix_quantum.png`
- NEW: `results/roc_curves_comparison.png`

---

### 🥉 #3: GRADCAM VISUAL EXPLAINABILITY

**What to Change**:
Add GradCAM visualization showing WHERE the model looked in the X-ray

**Implementation**:
```python
# NEW: src/explainability/gradcam.py
def generate_gradcam(image_path, model):
    # 1. Load ResNet50 model
    # 2. Get GradCAM heatmap from final conv layer
    # 3. Overlay heatmap on original image
    # 4. Return highlighted image
```

**Frontend Integration**:
- Show original image + GradCAM overlay in TRIAGE stage
- Highlight regions of interest
- Add "Model Attention" visualization

**Why It Matters**:
- **CRITICAL FOR MEDICAL AI** - doctors need to see reasoning
- Dramatically increases trust
- Shows technical sophistication
- Separates you from basic classifiers

**Difficulty**: Medium  
**Risk**: Medium (GradCAM can be tricky with ResNet50 + SVM pipeline)  
**Expected Hackathon Impact**: **+2.0 points** (HUGE for medical judges)

**Files Likely Affected**:
- NEW: `src/explainability/gradcam.py`
- NEW: `src/explainability/__init__.py`
- UPDATE: `src/inference/predict.py` (include GradCAM in response)
- UPDATE: `dashboard/src/components/` (add GradCAM visualization)
- UPDATE: `src/api/main.py` (return GradCAM image)

---

### #4: FIX DEMO DATA TO MATCH REAL TASK

**What to Change**:
Update `dashboard/src/data/demoData.js` to show PNEUMONIA detection with honest metrics

**Changes**:
```javascript
triage: {
  classification: "PNEUMONIA",  // was "ABNORMAL"
  prediction: "Pneumonia",       // was "Nodule"
  confidence: 0.923,             // Classical SVM confidence
  priority: "HIGH",
  recommendation: "Clinical assessment for pneumonia recommended"
}

classical: {
  confidence: 0.923,  // Use actual Classical SVM metrics
  probability: { normal: 0.077, pneumonia: 0.923 }
}

quantum: {
  confidence: 0.612,  // Use ACTUAL Quantum metrics (be honest!)
  probability: { normal: 0.388, pneumonia: 0.612 }
}
```

**Why It Matters**:
- Eliminates confusion about task
- Shows honest metrics
- Increases credibility
- Prepares for backend integration

**Difficulty**: Low  
**Risk**: Very Low  
**Expected Hackathon Impact**: **+0.5 points**

**Files Likely Affected**:
- UPDATE: `dashboard/src/data/demoData.js`

---

### #5: ONE-PAGE HACKATHON NARRATIVE DOCUMENT

**What to Change**:
Create `HACKATHON_STORY.md` with compelling 2-minute demo flow and talking points

**Structure**:
```markdown
# Q-MedTriage: Demo Flow & Narrative

## The Hook (15 seconds)
"Pneumonia kills 2.5M people annually. Early detection saves lives.
But radiologists are overworked. Can AI help?"

## The Innovation (30 seconds)
"We built Q-MedTriage: hybrid classical + quantum ML for chest X-ray triage.
ResNet50 → PCA → Dual classification with honest comparison."

## The Demo (60 seconds)
1. Upload X-ray
2. Watch pipeline process
3. Show Classical: 92% accuracy (excellent)
4. Show Quantum: 61% accuracy (poor, but valuable)
5. Show GradCAM: "Here's where the model looked"
6. Show final triage recommendation

## The Insight (15 seconds)
"Quantum ML shows promise but isn't ready for medical imaging yet.
Classical SVM achieves 92% accuracy - ready for clinical validation.
Our comparison helps guide future quantum research."

## The Ask (10 seconds)
"Next: Clinical trials, FDA pathway, integration with hospital systems."
```

**Why It Matters**:
- Gives you rehearsed talking points
- Structures the demo flow
- Handles quantum "failure" gracefully
- Shows maturity and honesty

**Difficulty**: Low  
**Risk**: None  
**Expected Hackathon Impact**: **+0.5 points**

**Files Likely Affected**:
- NEW: `HACKATHON_STORY.md`

---

## H. RECOMMENDED IMPLEMENTATION ORDER

### Phase 1: Core Functionality (Day 1) ⚡ CRITICAL

1. **Inference Pipeline** (#1)
   - Create `src/inference/predict.py`
   - Test with sample X-ray
   - Verify Classical SVM predictions work
   - Time: 3-4 hours

2. **Backend Integration** (#1 continued)
   - Connect `/predict` endpoint to inference
   - Handle image upload
   - Return JSON with classification
   - Time: 2-3 hours

3. **Fix Demo Data** (#4)
   - Update to PNEUMONIA task
   - Use honest metrics
   - Time: 30 minutes

**End of Day 1**: Can upload real X-ray and get real prediction ✅

### Phase 2: Visual Impact (Day 2) 🎨 HIGH VALUE

4. **GradCAM Explainability** (#3)
   - Implement GradCAM heatmap
   - Integrate into inference pipeline
   - Add to frontend visualization
   - Time: 4-5 hours

5. **Performance Comparison** (#2)
   - Generate confusion matrix plots
   - Create ROC curves
   - Build comparison dashboard component
   - Time: 3-4 hours

**End of Day 2**: Impressive visual demo with explainability ✅

### Phase 3: Polish & Narrative (Day 3) 📖 PRESENTATION

6. **Hackathon Narrative** (#5)
   - Write demo script
   - Create talking points
   - Prepare for quantum "failure" handling
   - Time: 1 hour

7. **Documentation Cleanup**
   - Update README with demo instructions
   - Add architecture diagram
   - Clean up excessive technical docs
   - Time: 2 hours

8. **Final Testing & Rehearsal**
   - Test full demo flow
   - Fix any bugs
   - Practice presentation
   - Time: 2-3 hours

**End of Day 3**: Ready for hackathon presentation ✅

---

## I. THINGS WE SHOULD NOT CHANGE

### ✅ PRESERVE THESE (Working Well)

**Models**:
- ❌ DON'T retrain Classical SVM (excellent performance)
- ❌ DON'T retrain Quantum SVM (completed, expensive, honest result)
- ❌ DON'T modify saved model files
- ❌ DON'T change PCA configuration

**Frontend Core**:
- ❌ DON'T redesign the UI (it's gorgeous)
- ❌ DON'T change the scrolling storytelling flow
- ❌ DON'T remove animations
- ❌ DON'T change the 8-stage structure

**Data**:
- ❌ DON'T modify train/val/test splits
- ❌ DON'T change dataset (Kermany is appropriate)
- ❌ DON'T retrain feature extraction

**Documentation**:
- ❌ DON'T delete QSVM validation reports (valuable)
- ❌ DON'T hide poor quantum results
- ❌ DON'T exaggerate quantum performance

### Rationale

The project has **strong fundamentals**:
- Excellent Classical SVM (92% accuracy)
- Beautiful UI/UX
- Honest quantum comparison
- Solid ML pipeline
- Good test coverage

The issues are **integration and presentation**, not core quality.

---

## J. PROPOSED FINAL HACKATHON STORY

### The Narrative Arc

**Act 1: The Problem (15 sec)**
> "Pneumonia is the leading infectious cause of death in children worldwide, killing 740,000 children under 5 in 2019. Early detection through chest X-ray analysis is critical, but radiologists are scarce and overworked, especially in resource-limited settings."

**Act 2: Our Approach (30 sec)**
> "We built Q-MedTriage: a hybrid classical-quantum machine learning system for AI-assisted chest X-ray triage. Our pipeline combines deep learning feature extraction, dimensionality reduction, and dual classification to provide fast, explainable pneumonia detection."

**Act 3: The Demo (60 sec)**
> [Live Demo]
> 1. "Here's a chest X-ray entering our system..."
> 2. "ResNet50 extracts 2,048 visual features..."
> 3. "PCA compresses to 4 dimensions for quantum processing..."
> 4. "Our Classical SVM achieves 92% accuracy with 97% ROC-AUC..."
> 5. "We experimentally compared with a Quantum SVM..."
> 6. "This GradCAM visualization shows where the model focused its attention..."
> 7. "Final triage: PNEUMONIA detected with 92% confidence..."

**Act 4: The Insight (20 sec)**
> "Our quantum experiment revealed something valuable: current quantum kernel methods struggle with medical imaging, achieving only 61% accuracy compared to 92% for classical approaches. This honest comparison guides future research and shows that for medical AI, classical methods remain the practical choice today."

**Act 5: Clinical Positioning (15 sec)**
> "Q-MedTriage is designed as AI-assisted decision support, not replacement. The GradCAM explainability allows clinicians to understand and verify the model's reasoning, building trust. Our 92% accuracy Classical SVM is ready for clinical validation studies."

**Act 6: Impact & Next Steps (10 sec)**
> "Next steps: Clinical trials with radiologist validation, FDA regulatory pathway exploration, and integration with hospital PACS systems. Our goal: democratize accurate pneumonia screening for underserved communities."

### Key Talking Points

✅ **DO SAY**:
- "92% accuracy on pneumonia detection"
- "Explainable AI with GradCAM attention visualization"
- "Honest comparison: quantum didn't outperform classical in this experiment"
- "AI-assisted triage to support, not replace, clinicians"
- "Reproducible pipeline with 1,300+ lines of tests"
- "Beautiful real-time visualization of the ML pipeline"

❌ **DON'T SAY**:
- "Quantum is better" (it's not, in this case)
- "Ready for clinical deployment" (needs validation)
- "Replaces radiologists" (it's decision support)
- "Diagnoses pneumonia" (it assists triage)
- "94% quantum accuracy" (fake demo data)

### Handling The Quantum Question

**If Asked: "Why did quantum perform poorly?"**

> "Great question! Our quantum kernel SVM achieved 61% accuracy compared to 92% for classical. We identified several factors: (1) limited training data—only 500 samples for the quantum model due to computational constraints versus 4,172 for classical, (2) class imbalance in the dataset, and (3) the quantum fidelity kernel may not be optimal for PCA-compressed image features. This is a valuable negative result that demonstrates current quantum ML limitations for medical imaging and guides future research directions. We kept it in our comparison because honest evaluation is critical in medical AI."

**Spin**: Turn the "failure" into scientific rigor and maturity.

---

## SUMMARY

### Current State: 7.0/10

**Strengths**:
- Excellent Classical SVM (92% accuracy)
- Gorgeous UI with smooth animations
- Honest quantum comparison
- Solid ML fundamentals
- Good documentation

**Critical Gaps**:
- No end-to-end inference pipeline
- No explainability (GradCAM)
- Fake demo data
- No performance visualization
- Backend not connected

### Potential State: 9.5/10

**With 3 Days of Focused Work**:

**Day 1**: Inference pipeline + backend integration → **Real predictions work**
**Day 2**: GradCAM + performance dashboard → **Impressive visuals**
**Day 3**: Polish + narrative → **Compelling story**

### The Winning Formula

```
Beautiful UI (already have) ✅
    +
Real Predictions (need to add) 🔧
    +
Explainability (need to add) 🔧
    +
Honest Story (need to craft) 📖
    =
9.5/10 Hackathon Project 🏆
```

### Risk Assessment

**Low Risk** ✅:
- All components exist (just need integration)
- Models are trained and validated
- UI is polished
- Tests provide safety net

**Medium Risk** ⚠️:
- GradCAM integration might be tricky
- Backend deployment timing

**High Risk** ❌:
- Nothing! (Don't retrain models, don't rebuild UI)

---

**RECOMMENDATION**: Execute Phase 1-3 implementation plan over 3 days. Focus on inference + GradCAM + honest comparison. The project has exceptional foundations—it just needs the final 20% to reach demo perfection.

**NEXT STEP**: Get approval for implementation plan, then start with `src/inference/predict.py`.

