# URGENT: Classical SVM Model is Broken

## Critical Issue Discovered

**Problem:** The Classical SVM model is performing at **50% accuracy** (random guessing) despite training reports claiming 92% validation accuracy.

### Test Results (backend/scripts/test_model_accuracy.py)
```
NORMAL images:   1/5 correct (20%) - Heavily misclassified as PNEUMONIA
PNEUMONIA images: 4/5 correct (80%)
Overall: 5/10 (50% accuracy)
```

### User Impact
- System classified a chest X-ray with pneumonia indicators as "NORMAL 71%"
- Gemini analysis correctly identified consolidation/opacity patterns
- Our model missed it due to bias toward NORMAL classification

## Root Cause Analysis

1. **Model is severely biased** - classifying most images as one category
2. **Training metrics (92%) don't match actual performance (50%)**
3. Possible causes:
   - Model file corruption
   - Training/validation split issues
   - Feature extraction pipeline broken
   - PCA transformation mismatch

## Current System State

### What's Working ✓
- Image validation (CLIP-based chest X-ray detection)
- Frontend UI (compact, animated grid)
- Backend API (FastAPI server running)
- Preprocessing pipeline (transforms match training)

### What's Broken ✗
- **Classical SVM classifier** - 50% accuracy
- **Quantum SVM** - 61% accuracy with severe PNEUMONIA bias (worse than random)
- Feature extraction pipeline (no cached features in `backend/data/features/`)

## Immediate Fix Required

### Option 1: Retrain from Scratch (Recommended)
**Full pipeline retraining required:**

```bash
cd backend

# Step 1: Extract ResNet50 features
python -m src.models.extract_features

# Step 2: Fit PCA on training features
python -m src.models.pca_reduction

# Step 3: Apply PCA to all splits
python -m src.models.apply_pca

# Step 4: Train Classical SVM
python -m src.models.train_classical_svm

# Step 5: Test the new model
python scripts/test_model_accuracy.py
```

**Expected Time:** 30-60 minutes depending on hardware

### Option 2: Use Pre-trained CNN (Alternative)
Replace SVM with a fine-tuned ResNet classifier:
- Train end-to-end ResNet50 on chest X-ray dataset
- Higher accuracy potential (typically 95%+)
- Longer training time but more robust

### Option 3: Download Known-Good Models (Quick Fix)
If you have backup models from a previous successful training session, restore them.

## Files to Investigate

1. **Model file:** `models/classical_svm.pkl` - May be corrupted
2. **Training results:** `results/classical_svm_training_results.json` - Shows 92% but actual is 50%
3. **PCA model:** `models/pca_reducer.pkl` - Verify this matches training
4. **Feature cache:** `backend/data/features/` - Currently empty

## Medical Safety Implications

⚠️ **CRITICAL:** Do NOT use this system for any real medical decisions until the model is fixed and validated!

- False negatives (missing pneumonia) = dangerous
- False positives (normal flagged as pneumonia) = unnecessary concern
- Current 50% accuracy = unacceptable for any medical application

## Next Steps

1. **Stop using the current model** for any real analysis
2. **Retrain the entire pipeline** following Option 1 above
3. **Validate on held-out test set** to confirm 90%+ accuracy
4. **Document the training process** to prevent future issues
5. **Consider ensemble methods** or deeper CNN architectures for better performance

## Timeline

- **Retraining:** 30-60 minutes
- **Validation:** 5-10 minutes  
- **Testing with real images:** 5 minutes
- **Total:** ~1-2 hours to fully resolve

---

**Status:** ❌ SYSTEM NOT PRODUCTION-READY
**Priority:** 🔴 CRITICAL
**Impact:** High - affects core classification functionality
