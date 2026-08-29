# Chest X-ray Validation Gate

## Critical Safety Feature

**Problem Identified**: The system previously accepted ANY uploaded image and labeled it as a "Chest Radiograph", including skull X-rays, photographs, and other non-chest images. This is unsafe.

**Solution Implemented**: Strict input validation gate that analyzes image content BEFORE allowing access to the classification pipeline.

---

## Architecture

### Pipeline Flow

```
Image Upload
    ↓
[VALIDATION GATE] ← NEW SAFETY GATE
    ↓
Is this a valid CHEST RADIOGRAPH?
    ↓
    ├─YES → Image Preprocessing
    │         ↓
    │       ResNet50 Feature Extraction (2048D)
    │         ↓
    │       PCA Dimensionality Reduction (2048D → 4D)
    │         ↓
    │       Classical SVM or Quantum SVM
    │         ↓
    │       RAG Evidence Retrieval
    │         ↓
    │       LLM Reasoning Synthesis
    │         ↓
    │       Final Result
    │
    └─NO  → IMMEDIATE REJECTION
            ↓
          Return Error Response
          ↓
          "Unsupported Image"
          ↓
          NO PREDICTION, NO CLASSIFICATION
```

---

## Implementation Details

### Validation Method: CLIP Zero-Shot Classification

**Model**: `openai/clip-vit-base-patch32`

**Approach**: Vision-language model trained on 400M image-text pairs. Can distinguish image types without task-specific training.

**Why CLIP?**
- No retraining needed
- Can distinguish medical image types
- Understands semantic image content
- Lightweight (~350MB model)
- Fast inference (~100-300ms)

### Validation Categories

**Chest X-ray Prompts** (Accept if high confidence):
```python
[
    "a frontal chest x-ray radiograph",
    "a chest radiograph showing lungs",
    "a chest x-ray medical image",
    "a posteroanterior chest radiograph"
]
```

**Unsupported Prompts** (Reject if these score higher):
```python
[
    "a skull x-ray",
    "a brain scan",
    "a hand x-ray",
    "a dental x-ray",
    "a spine x-ray",
    "a leg or arm x-ray",
    "a CT scan",
    "an MRI scan",
    "an ultrasound image",
    "a photograph",
    "a regular picture",
    "a non-medical image"
]
```

### Decision Logic (Conservative)

The validator computes similarity scores for all text prompts against the uploaded image, then:

1. **Aggregate by category**: Take maximum score per category
2. **Chest X-ray score** must be ≥ **65%** (VALIDATION_THRESHOLD)
3. **Margin** (chest_xray - unsupported) must be ≥ **20%** (MARGIN_THRESHOLD)
4. **Accept** only if BOTH conditions met
5. **Reject** otherwise

**Safety Principle**: "When uncertain, do not classify"

- ✅ False rejection of uncertain image → **SAFE**
- ❌ False acceptance of unsupported image → **DANGEROUS**

---

## Configuration

### Thresholds

Located in: `backend/src/inference/chest_xray_validator.py`

```python
class ChestXRayValidator:
    # Minimum confidence for chest X-ray category
    VALIDATION_THRESHOLD = 0.65  # 65%
    
    # Minimum margin between chest_xray and unsupported
    MARGIN_THRESHOLD = 0.20  # 20%
```

**Tuning Guidelines:**

- **Increase VALIDATION_THRESHOLD** (e.g., 0.70) → More strict, fewer false acceptances
- **Decrease VALIDATION_THRESHOLD** (e.g., 0.60) → More lenient, may accept borderline images
- **Increase MARGIN_THRESHOLD** (e.g., 0.25) → Require clearer distinction
- **Decrease MARGIN_THRESHOLD** (e.g., 0.15) → Allow closer ambiguous cases

**Recommendation**: Start conservative, monitor production acceptance/rejection rates, adjust carefully.

---

## API Integration

### Backend Changes

**File**: `backend/src/api/main.py`

**Phase 0: Validator Initialization** (runs at startup):
```python
chest_xray_validator = ChestXRayValidator()
chest_xray_validator.load()
VALIDATOR_LOADED = True
```

**Validation Gate** (runs before every prediction):
```python
if VALIDATOR_LOADED:
    validation_result = chest_xray_validator.validate(image)
    
    if not validation_result["is_valid_chest_xray"]:
        # REJECT
        return JSONResponse(
            status_code=400,
            content={
                "valid": False,
                "error": "unsupported_image",
                "message": "This system is designed exclusively for chest radiograph analysis.",
                "validation": {...}
            }
        )
    
    # ACCEPT - proceed to classification
```

**Endpoints with Validation**:
- ✅ `/predict` - Primary classification endpoint
- ✅ `/intelligence` - Full pipeline with RAG/LLM

---

## Response Examples

### Valid Chest X-ray (Accepted)

**Request**:
```bash
POST /predict
Content-Type: multipart/form-data

file: chest_xray.jpg
```

**Response** (200 OK):
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
  "validation": {
    "is_valid_chest_xray": true,
    "confidence": 0.78,
    "detected_type": "chest_xray"
  },
  "disclaimer": "AI-assisted triage prediction...",
  "filename": "chest_xray.jpg"
}
```

### Skull X-ray (Rejected)

**Request**:
```bash
POST /predict
Content-Type: multipart/form-data

file: skull_xray.jpg
```

**Response** (400 Bad Request):
```json
{
  "valid": false,
  "error": "unsupported_image",
  "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
  "validation": {
    "is_valid_chest_xray": false,
    "confidence": 0.23,
    "detected_type": "unsupported",
    "reason": "Image appears to be a skull X-ray, not a chest radiograph.",
    "scores": {
      "chest_xray": 0.23,
      "unsupported": 0.71,
      "margin": -0.48
    }
  }
}
```

### Photograph (Rejected)

**Request**:
```bash
POST /predict
Content-Type: multipart/form-data

file: photo.jpg
```

**Response** (400 Bad Request):
```json
{
  "valid": false,
  "error": "unsupported_image",
  "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
  "validation": {
    "is_valid_chest_xray": false,
    "confidence": 0.12,
    "detected_type": "unsupported",
    "reason": "Low chest X-ray confidence (12%). Unable to confirm this is a chest radiograph.",
    "scores": {
      "chest_xray": 0.12,
      "unsupported": 0.82,
      "margin": -0.70
    }
  }
}
```

---

## Frontend Integration

### UI Changes

**Before Upload** (`PreviewStage.jsx`):
```jsx
// OLD (REMOVED):
<h2>Chest Radiograph Detected</h2>

// NEW:
<h2>Image Uploaded Successfully</h2>
<p>Chest X-ray validation will occur during analysis</p>
```

**After Validation Rejection** (`ResultStage.jsx`):
```jsx
<div className="result-stage error validation-error">
  <div className="result-icon error-icon">
    <ImageIcon size={64} />
  </div>
  <h2>Unsupported Image</h2>
  <p>This system is designed exclusively for chest radiograph analysis.</p>
  <p>Please upload a valid chest X-ray image (frontal/PA view).</p>
  <div className="validation-details">
    <AlertCircle size={16} />
    <span>Images such as skull X-rays, CT scans, MRI scans, 
          photographs, or other non-chest radiographs are not supported.</span>
  </div>
  <button onClick={onReset}>Upload Chest X-ray</button>
</div>
```

**Validation Error Handling** (`usePrediction.js`):
```javascript
// Check for validation error (400 status with unsupported_image error)
if (response.status === 400 && data.error === "unsupported_image") {
  const validationError = data.message || 
    "This system is designed exclusively for chest radiograph analysis.";
  
  setPredictionState({
    isLoading: false,
    isComplete: false,
    result: null,
    error: validationError,
    validationError: true,
    validation: data.validation,
  });
  
  throw new Error(validationError);
}
```

---

## Testing

### Test Scripts

**1. Validator Unit Test**:
```bash
python backend/scripts/test_chest_xray_validation.py
```

**2. API Integration Test**:
```bash
# Start backend first
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Then run test
python backend/scripts/test_validation_api.py
```

### Expected Test Results

| Image Type | Expected Result | Reasoning |
|------------|-----------------|-----------|
| Frontal chest X-ray | ✅ ACCEPT | Valid medical image |
| Lateral chest X-ray | ⚠️ REVIEW | May accept or reject |
| Skull X-ray | ❌ REJECT | Wrong anatomy |
| Hand X-ray | ❌ REJECT | Wrong anatomy |
| CT scan | ❌ REJECT | Wrong modality |
| MRI scan | ❌ REJECT | Wrong modality |
| Ultrasound | ❌ REJECT | Wrong modality |
| Photograph | ❌ REJECT | Non-medical |
| Screenshot | ❌ REJECT | Non-medical |

---

## Production Monitoring

### Metrics to Track

1. **Acceptance Rate**: % of uploaded images that pass validation
2. **Rejection Rate**: % of uploaded images rejected
3. **Average Confidence**: Mean confidence for accepted images
4. **Rejection Reasons**: Distribution of detected_type for rejections

### Alert Thresholds

- ⚠️ Acceptance rate < 50% → Threshold may be too strict
- ⚠️ Acceptance rate > 95% → Threshold may be too lenient
- ⚠️ Average confidence < 0.70 → Borderline images being accepted

### User Feedback

Collect feedback on rejections:
- False rejections (valid chest X-rays incorrectly rejected)
- User confusion about rejection reasons
- Requests for supported image types

Use feedback to tune thresholds and improve prompt engineering.

---

## Limitations

### Known Edge Cases

1. **Lateral chest X-rays** (side view):
   - May be rejected if CLIP doesn't recognize them
   - Solution: Add lateral-specific prompts if needed

2. **Poor quality X-rays**:
   - Very dark, very bright, or noisy images
   - Low confidence may trigger rejection
   - Solution: Adjust VALIDATION_THRESHOLD if needed

3. **Rotated images**:
   - CLIP should be rotation-invariant
   - Extreme rotations may reduce confidence

4. **Pediatric X-rays**:
   - Different anatomy proportions
   - Should still pass validation (lungs visible)

5. **Portable/AP X-rays**:
   - Different positioning than PA
   - Should still pass validation

### Not Supported (By Design)

- **Chest CT scans**: Different modality, requires different analysis
- **Chest MRI**: Different modality, requires different analysis
- **Fluoroscopy**: Video/dynamic imaging, not static X-ray

---

## Security Considerations

### Adversarial Attacks

**Threat**: User attempts to bypass validation with modified images.

**Mitigations**:
1. Server-side validation (cannot be bypassed by client modification)
2. Conservative thresholds (hard to fool with subtle modifications)
3. Multiple prompt categories (must fool all simultaneously)

### False Acceptance Risk

**Impact**: Unsupported image reaches classification pipeline.

**Consequences**:
- Model may produce nonsensical prediction
- User receives misleading results
- Potential safety issue

**Mitigation**:
- Conservative thresholds prioritize rejection
- Model confidence should also be low for nonsense inputs
- Medical disclaimer on all outputs

---

## Future Enhancements

### Short-term

1. **View Detection**: Distinguish PA, AP, lateral chest X-rays
2. **Quality Assessment**: Reject very low-quality images
3. **Anatomy Detection**: Verify lungs are actually visible
4. **Multi-stage Validation**: Combine CLIP with simple heuristics

### Long-term

1. **Fine-tuned Validator**: Train specifically on medical images
2. **Explainable Rejection**: Show which regions caused rejection
3. **Confidence Calibration**: Improve reliability of confidence scores
4. **Active Learning**: Learn from user feedback on rejections

---

## Troubleshooting

### Validator Not Loading

**Symptom**: Backend logs show "Chest X-ray validator not loaded"

**Causes**:
- transformers library not installed
- CLIP model download failed
- Insufficient memory

**Solutions**:
```bash
# Install/upgrade transformers
pip install --upgrade transformers

# Check available memory
# CLIP requires ~2GB RAM
```

### All Images Rejected

**Symptom**: Even valid chest X-rays are rejected

**Causes**:
- Threshold too high
- Model not loaded properly
- Wrong image format

**Solutions**:
1. Check validator initialization logs
2. Lower VALIDATION_THRESHOLD temporarily
3. Test with known-good chest X-ray
4. Check image is RGB (not RGBA or grayscale)

### All Images Accepted

**Symptom**: Even photographs/skulls are accepted

**Causes**:
- Validator not actually running
- Threshold too low
- Logic error

**Solutions**:
1. Verify VALIDATOR_LOADED = True in logs
2. Check validation result is actually being checked
3. Increase VALIDATION_THRESHOLD
4. Add logging to validation decision

---

## Dependencies

### Backend

```
transformers>=4.30.0  # CLIP model
torch>=2.0.0          # PyTorch for model inference
Pillow>=10.0.0        # Image processing
ftfy>=6.1.0           # Text processing for CLIP
regex>=2023.0.0       # Pattern matching for CLIP
```

### Model Downloads

First run will download:
- CLIP model (~350MB)
- CLIP processor config
- Tokenizer files

Subsequent runs use cached models.

---

## References

- **CLIP Paper**: [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
- **Hugging Face CLIP**: https://huggingface.co/docs/transformers/model_doc/clip
- **Medical Image Classification**: Various studies on using CLIP for medical imaging

---

**Document Version**: 1.0  
**Last Updated**: 2026-08-27  
**Status**: Production Ready
