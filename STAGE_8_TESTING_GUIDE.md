# STAGE 8 — TESTING GUIDE

## BACKEND + FRONTEND INTEGRATION TESTING

This guide walks through testing the complete Q-MedTriage system with real backend/frontend integration.

---

## PREREQUISITES

### 1. Python Environment
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### 2. Backend Dependencies
```bash
# Install if not already installed
pip install -r requirements.txt
pip install -r requirements_intelligence.txt  # Optional: for /intelligence endpoint
```

### 3. Environment Configuration

**Backend** (root `.env`):
```env
# Optional: Enable intelligence layer
INTELLIGENCE_ENABLED=true
GEMINI_API_KEY=your_api_key_here  # Required for /intelligence
```

**Frontend** (`dashboard/.env`):
```env
VITE_API_URL=http://localhost:8000
```

---

## STARTING THE SYSTEM

### Terminal 1: Backend API

```bash
# From project root
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
==================================================================
Initializing Q-MedTriage API
==================================================================
✓ Phase 1: Inference pipeline ready
------------------------------------------------------------------
Phase 2: Intelligence Layer Initialization
------------------------------------------------------------------
✓ Phase 2: RAG retriever ready
✓ Phase 2: Gemini synthesizer ready
==================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**If intelligence layer fails:**
```
⚠ Phase 2: GEMINI_API_KEY not configured
  Intelligence layer will be unavailable
  Set GEMINI_API_KEY in .env to enable
```
This is OK. The `/predict` endpoint will still work.

### Terminal 2: Frontend Dashboard

```bash
# From dashboard directory
cd dashboard
npm run dev
```

**Expected output:**
```
VITE v8.2.2  ready in 300 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## MANUAL TESTING CHECKLIST

### Test 1: Health Check ✅

**Backend API:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "api": "online",
  "vision_model": "ready",
  "classical_svm": "ready",
  "quantum_svm": "ready",
  "rag_retriever": "ready",
  "gemini_synthesizer": "ready",
  "intelligence_enabled": true,
  "pipeline_loaded": true
}
```

**Status:** If `pipeline_loaded: true`, backend is ready ✅

---

### Test 2: Frontend Connection ✅

1. Open browser: http://localhost:5173
2. Check browser console (F12)
3. Look for errors
4. Expected: No connection errors

**Status:** ✅ if no errors

---

### Test 3: Image Upload (PNEUMONIA) ✅

1. Navigate to http://localhost:5173
2. Click "START TRIAGE" or "UPLOAD X-RAY"
3. Select a pneumonia chest X-ray from `data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/`
4. Wait for analysis

**Expected behavior:**
- [x] Loading state appears
- [x] "ANALYZING X-RAY" or similar message
- [x] Left visual workspace updates
- [x] No demo data mixed with real results

**Expected result after ~2 seconds:**
- [x] Prediction: "PNEUMONIA"
- [x] Confidence: 85-95%
- [x] Probabilities shown
- [x] Medical disclaimer displayed

**Browser Console:**
Should see:
```
POST http://localhost:8000/predict 200 OK
```

**Status:** ✅ if real prediction displays

---

### Test 4: Image Upload (NORMAL) ✅

1. Upload a normal chest X-ray from `data/archive (1)/chest_xray/chest_xray/test/NORMAL/`
2. Wait for analysis

**Expected result:**
- [x] Prediction: "NORMAL"
- [x] Confidence: 80-95%
- [x] Appropriate priority level (ROUTINE)

**Status:** ✅ if real prediction displays

---

### Test 5: Invalid File Type ✅

1. Try to upload a .txt or .pdf file
2. Expected:
   - [x] Validation error
   - [x] Message: "Invalid file type"
   - [x] No API call made (check Network tab)

**Status:** ✅ if error handled gracefully

---

### Test 6: Backend Offline Error Handling ✅

1. Stop the backend (CTRL+C in Terminal 1)
2. Try to upload an image
3. Expected:
   - [x] Connection error message
   - [x] Clear error state
   - [x] No crash
   - [x] User can retry

**Browser Console:**
Should see:
```
POST http://localhost:8000/predict net::ERR_CONNECTION_REFUSED
```

**Status:** ✅ if error handled gracefully

---

### Test 7: Duplicate Submit Prevention ✅

1. Restart backend
2. Upload image
3. While processing, try to upload another image
4. Expected:
   - [x] Second upload is blocked OR
   - [x] First request is cancelled and second starts OR
   - [x] User is clearly warned

**Status:** ✅ if handled safely

---

### Test 8: Stage 7.5 Layout Preserved ✅

While using the application:
- [x] Left visual workspace is sticky (remains visible during scroll)
- [x] Right narrative scrolls naturally
- [x] 50/50 composition maintained
- [x] No horizontal overflow
- [x] Responsive behavior intact (test at 1440px, 1000px, 650px widths)

**Status:** ✅ if visual architecture unchanged

---

### Test 9: Stage Synchronization ✅

1. Upload image
2. Scroll through the right-side narrative
3. Expected:
   - [x] Left visual changes with scroll position
   - [x] Stage number updates (01/08, 02/08, etc.)
   - [x] Framer Motion transitions work
   - [x] No visual glitches

**Status:** ✅ if scrollytelling works

---

### Test 10: Intelligence Endpoint (Optional) ⚠️

**Only test if GEMINI_API_KEY is configured**

1. Check backend startup shows: "✓ Phase 2: Gemini synthesizer ready"
2. Make request to `/intelligence`:

```bash
curl -X POST http://localhost:8000/intelligence \
  -F "file=@path/to/chest_xray.jpg"
```

**Expected response:**
```json
{
  "success": true,
  "prediction": {
    "condition": "PNEUMONIA",
    "confidence": 0.923,
    ...
  },
  "intelligence": {
    "answer": "Detailed medical explanation...",
    "sources": [...]
  }
}
```

**Status:** ⚠️ Optional — not required for Stage 8 completion

---

## AUTOMATED TEST SCRIPT

Create `test_stage8_integration.sh`:

```bash
#!/bin/bash

echo "==================================="
echo "STAGE 8 INTEGRATION TEST"
echo "==================================="

# Test 1: Health Check
echo -e "\nTest 1: Health Check"
curl -s http://localhost:8000/health | jq

# Test 2: Predict with test image
echo -e "\nTest 2: Prediction (requires test image)"
# Uncomment and add path to test image:
# curl -X POST http://localhost:8000/predict \
#   -F "file=@data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg" \
#   | jq

echo -e "\nTests complete!"
```

Make executable:
```bash
chmod +x test_stage8_integration.sh
./test_stage8_integration.sh
```

---

## TROUBLESHOOTING

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'src'`

**Fix:**
```bash
# Ensure running from project root
cd /path/to/Q-MedTriage
uvicorn src.api.main:app --reload
```

---

### Backend starts but /predict fails

**Error:** `503 Service Unavailable`

**Check backend console:**
```
✗ Failed to load inference pipeline: ...
```

**Fix:**
1. Verify model files exist in `models/`
2. Check ResNet50 weights are present
3. Verify PCA model exists
4. Ensure Classical SVM model exists

---

### Frontend can't connect

**Error in browser console:**
```
Access to fetch at 'http://localhost:8000/predict' from origin 'http://localhost:5173'
has been blocked by CORS policy
```

**Fix:**
Backend should have CORS enabled (already configured in `src/api/main.py`). Restart backend if issue persists.

---

### Demo data still showing

**Issue:** Frontend displays fake/demo data instead of real predictions

**Check:**
1. Open `dashboard/src/services/api.js`
2. Verify: `const USE_DEMO_DATA = false;`
3. If true, change to false
4. Rebuild: `npm run build`
5. Restart dev server

---

### Environment variables not loading

**Issue:** `VITE_API_URL` not recognized

**Fix:**
1. Verify `dashboard/.env` exists
2. Restart dev server (CTRL+C, then `npm run dev`)
3. Check console: `import.meta.env.VITE_API_URL` should show URL

---

## SUCCESS CRITERIA

Stage 8 is complete when **ALL** of these are true:

- [x] Backend starts without errors
- [x] Frontend starts without errors
- [x] Health check returns `pipeline_loaded: true`
- [x] Image upload triggers real `/predict` call
- [x] Real prediction displays (PNEUMONIA or NORMAL)
- [x] Real confidence displays (0.XX decimal)
- [x] Loading state works
- [x] Error state works
- [x] Stage 7.5 layout preserved
- [x] No horizontal overflow
- [x] Responsive behavior intact
- [x] Production build succeeds
- [x] Lint passes
- [ ] All manual tests pass (Tests 1-9)

---

## NEXT STEPS AFTER TESTING

1. Document test results in `STAGE_8_COMPLETION_REPORT.md`
2. Create `STAGE_8_CHECKLIST.md`
3. Commit changes
4. Push to repository
5. Proceed to deployment/production preparation if needed

---

**END OF TESTING GUIDE**
