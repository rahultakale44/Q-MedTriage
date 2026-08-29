# Validation Error Data Flow - Complete Chain

## Overview
This document traces the complete data flow for validation errors from backend to frontend UI.

## CASE A: Unsupported Image (Skull/Hand/Photo)

### Backend Response
```http
POST /predict
Status: 400 Bad Request
Content-Type: application/json

{
  "valid": false,
  "error": "unsupported_image",
  "message": "This system is designed exclusively for chest radiograph analysis. Please upload a valid chest X-ray image.",
  "validation": {
    "is_valid_chest_xray": false,
    "confidence": 0.012,
    "detected_type": "unsupported",
    "reason": "Image appears to be a skull X-ray, not a chest radiograph.",
    "scores": {
      "chest_xray": 0.012,
      "unsupported": 0.363,
      "margin": -0.351
    }
  }
}
```

### Data Flow Chain

**1. usePrediction.js** (`frontend/src/hooks/usePrediction.js`)

```javascript
// Line 56-68
if (response.status === 400 && data.error === "unsupported_image") {
  const validationError = data.message || "...";
  
  setPredictionState({
    isLoading: false,
    isComplete: false,
    result: null,
    error: validationError,          // "This system is designed exclusively..."
    validationError: true,            // ✅ FLAG SET
    validation: data.validation,      // Full validation details
  });
  
  throw new Error(validationError);
}
```

**Returns:**
```javascript
{
  isLoading: false,
  isComplete: false,
  result: null,
  error: "This system is designed exclusively for chest radiograph analysis...",
  validationError: true,
  validation: { is_valid_chest_xray: false, confidence: 0.012, ... }
}
```

**2. useAnalysisPipeline.js** (`frontend/src/hooks/useAnalysisPipeline.js`)

```javascript
// Line 75
const { isLoading, isComplete, result, error, validationError, validation, predict } = usePrediction();

// Line 267-273
return {
  // ...
  predictionResult: result,
  predictionError: error,
  validationError: validationError,    // ✅ PROPAGATED
  validation: validation,
  // ...
};
```

**3. App.jsx** (`frontend/src/App.jsx`)

```javascript
// Line 33-43
const {
  // ...
  predictionError,
  validationError,    // ✅ RECEIVED
  validation,
  // ...
} = useAnalysisPipeline();

// Line 125-134
{currentStage === STAGES.RESULT && (
  <ResultStage
    key="result"
    image={uploadedImage}
    predictionData={predictionResult}
    error={predictionError}
    validationError={validationError}  // ✅ PASSED TO COMPONENT
    validation={validation}
    onOpenChat={openChat}
    onReset={resetPipeline}
  />
)}
```

**4. ResultStage.jsx** (`frontend/src/components/stages/ResultStage.jsx`)

```javascript
// Line 9
export function ResultStage({ image, predictionData, error, validationError, validation, onOpenChat, onReset }) {

// Line 11
if (validationError) {  // ✅ CONDITION CHECKED
  return (
    <motion.div className="result-stage error validation-error">
      <div className="result-container">
        <h2 className="result-title">Unsupported Image</h2>
        <p className="result-message validation-message">
          This system is designed exclusively for chest radiograph analysis.
        </p>
        <p className="result-submessage">
          Please upload a valid chest X-ray image (frontal/PA view).
        </p>
        <div className="validation-details">
          <AlertCircle size={16} />
          <span>Images such as skull X-rays, CT scans, MRI scans, photographs, or other non-chest radiographs are not supported.</span>
        </div>
        <button className="primary-action-button" onClick={onReset}>
          <RotateCcw size={20} />
          Upload Chest X-ray
        </button>
      </div>
    </motion.div>
  );
}
```

### User Sees:
```
┌─────────────────────────────────────┐
│         🖼️  Unsupported Image       │
│                                     │
│  This system is designed exclusively│
│  for chest radiograph analysis.    │
│                                     │
│  Please upload a valid chest X-ray  │
│  image (frontal/PA view).           │
│                                     │
│  ⚠️ Images such as skull X-rays,   │
│  CT scans, MRI scans, photographs,  │
│  or other non-chest radiographs     │
│  are not supported.                 │
│                                     │
│  [🔄 Upload Chest X-ray]           │
└─────────────────────────────────────┘
```

---

## CASE B: Valid Chest X-ray (Pipeline Unavailable)

### Backend Response
```http
POST /predict
Status: 503 Service Unavailable
Content-Type: application/json

{
  "detail": "Inference pipeline not available. The image passed validation, but the classification models are not loaded."
}
```

### Data Flow Chain

**1. usePrediction.js**

```javascript
// Line 71-74 - validation check already passed
// Line 76-78 - response not OK
if (!response.ok) {
  const errorMessage = data.detail || `API error: ${response.status} ${response.statusText}`;
  throw new Error(errorMessage);
}

// Catch block Line 237-246
setPredictionState({
  isLoading: false,
  isComplete: false,
  result: null,
  error: "Inference pipeline not available. The image passed validation...",
  validationError: false,    // ✅ EXPLICITLY FALSE
  validation: null,
});
```

**Returns:**
```javascript
{
  isLoading: false,
  isComplete: false,
  result: null,
  error: "Inference pipeline not available. The image passed validation...",
  validationError: false,   // ✅ NOT A VALIDATION ERROR
  validation: null
}
```

**2-3. Propagated through useAnalysisPipeline → App.jsx**

**4. ResultStage.jsx**

```javascript
// Line 11 - validationError is false, so this block is skipped
if (validationError) {
  // NOT EXECUTED
}

// Line 42-57 - Generic error handling
if (error) {
  return (
    <motion.div className="result-stage error">
      <div className="result-container">
        <div className="result-icon error-icon">
          <AlertCircle size={64} />
        </div>
        <h2 className="result-title">Analysis Interrupted</h2>
        <p className="result-message">{error}</p>  // ✅ Shows actual error
        <button className="primary-action-button" onClick={onReset}>
          <RotateCcw size={20} />
          Try Again
        </button>
      </div>
    </motion.div>
  );
}
```

### User Sees:
```
┌─────────────────────────────────────┐
│      ⚠️  Analysis Interrupted       │
│                                     │
│  Inference pipeline not available.  │
│  The image passed validation, but   │
│  the classification models are not  │
│  loaded.                            │
│                                     │
│  [🔄 Try Again]                    │
└─────────────────────────────────────┘
```

---

## Key Differences

| Aspect | Validation Error | Pipeline Error |
|--------|------------------|----------------|
| **Backend Status** | 400 Bad Request | 503 Service Unavailable |
| **Error Code** | `unsupported_image` | N/A (from `detail`) |
| **validationError Flag** | `true` | `false` |
| **UI Title** | "Unsupported Image" | "Analysis Interrupted" |
| **UI Message** | Chest radiograph requirement | Actual error message |
| **User Action** | Upload different image | Retry or wait for system |

---

## Validation Decision Points

### Backend (`backend/src/api/main.py`)

```
Request arrives
    ↓
Load image
    ↓
[VALIDATION] Run ChestXRayValidator  ← FIRST
    ↓
Is valid chest X-ray?
    ├─ NO → Return HTTP 400 immediately (STOP)
    └─ YES → Continue
        ↓
    Check PIPELINE_LOADED?  ← SECOND (only after validation)
        ├─ NO → Return HTTP 503
        └─ YES → Run inference
```

### Frontend (`frontend/src/`)

```
API Response
    ↓
status === 400 AND error === "unsupported_image"?
    ├─ YES → validationError = true
    └─ NO → validationError = false
        ↓
    ResultStage checks validationError
        ├─ true → Show "Unsupported Image" UI
        └─ false → Show generic error UI
```

---

## Backend Validation Logging

When validation runs, backend logs show:

**Rejected Image:**
```
======================================================================
[PREDICT] Request received
======================================================================
[PREDICT] Image loaded: (512, 512) L
[VALIDATION] Running chest X-ray validation...
[VALIDATION] ✗ REJECTED - unsupported
[VALIDATION] Confidence: 1.20%
[VALIDATION] Reason: Image appears to be a skull X-ray, not a chest radiograph.
[VALIDATION] Image will NOT proceed to inference pipeline
======================================================================
```

**Accepted Image (but pipeline unavailable):**
```
======================================================================
[PREDICT] Request received
======================================================================
[PREDICT] Image loaded: (1857, 1317) L
[VALIDATION] Running chest X-ray validation...
[VALIDATION] ✓ ACCEPTED - Chest X-ray confidence = 48.39%
[VALIDATION] Margin: 48.15%
[VALIDATION] Image will proceed to inference pipeline
[INFERENCE] ✗ Inference pipeline not available
======================================================================
```

---

## State Consistency Rules

**usePrediction.js ensures:**
1. Initial state always has `validationError: false`
2. Validation error explicitly sets `validationError: true`
3. Other errors explicitly set `validationError: false`
4. Success explicitly sets `validationError: false`
5. Reset explicitly sets `validationError: false`

This prevents stale or undefined validationError states.

---

## Testing Verification

E2E API test results (`backend/scripts/test_validation_e2e.py`):

```
✓ PASS: Skull rejection (HTTP 400, unsupported_image)
✓ PASS: Hand rejection (HTTP 400, unsupported_image)
✓ PASS: Photo rejection (HTTP 400, unsupported_image)
✓ PASS: Chest acceptance (validation passed, HTTP 503 pipeline unavailable)
```

Frontend build:
```
✓ built in 347ms
```

Frontend lint:
```
✓ No blocking errors
⚠ Minor warnings (unused parameter, Math.random in render)
```
