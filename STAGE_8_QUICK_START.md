# STAGE 8 — QUICK START GUIDE

## 🚀 5-MINUTE INTEGRATION TEST

**Prerequisites:** Backend models trained, frontend built

---

## STEP 1: Start Backend (Terminal 1)

```bash
# From project root
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
✓ Phase 1: Inference pipeline ready
==================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## STEP 2: Start Frontend (Terminal 2)

```bash
cd dashboard
npm run dev
```

**Wait for:**
```
VITE ready in 300 ms
➜  Local:   http://localhost:5173/
```

---

## STEP 3: Test Health (Terminal 3)

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "pipeline_loaded": true,
  "classical_svm": "ready"
}
```

---

## STEP 4: Open Browser

**Navigate to:** http://localhost:5173

**Expected:**
- Q-MEDTRIAGE landing page
- 50/50 layout (left visual | right story)
- No console errors (F12)

---

## STEP 5: Upload Test Image

1. Click **"START TRIAGE"** or **"UPLOAD X-RAY"**
2. Select: `data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg`
3. Wait ~2 seconds

**Expected:**
- ✅ Loading state ("ANALYZING")
- ✅ Left visual workspace updates
- ✅ Real prediction appears (PNEUMONIA)
- ✅ Real confidence displays (85-95%)
- ✅ Medical disclaimer shows

---

## STEP 6: Verify Console

**Press F12 → Network tab**

**Should see:**
```
POST http://localhost:8000/predict
Status: 200 OK
```

**Response preview:**
```json
{
  "success": true,
  "prediction_label": "PNEUMONIA",
  "confidence": 0.92
}
```

---

## ✅ SUCCESS CRITERIA

If you see all of these, Stage 8 is working:

- [x] Backend started without errors
- [x] Frontend started without errors  
- [x] Health check returns `pipeline_loaded: true`
- [x] Image upload works
- [x] Real prediction displays (not demo data)
- [x] Confidence percentage shows (0.XX)
- [x] Left visual workspace is sticky
- [x] No horizontal overflow

---

## ❌ TROUBLESHOOTING

### Backend won't start
**Error:** `ModuleNotFoundError`  
**Fix:** Ensure running from project root

### Frontend can't connect
**Error:** `net::ERR_CONNECTION_REFUSED`  
**Fix:** Start backend first

### Still shows demo data
**Check:** `dashboard/src/services/api.js`  
**Verify:** `USE_DEMO_DATA = false`

### CORS error
**Fix:** Backend has CORS enabled — restart both servers

---

## 📋 FULL TESTING

For comprehensive testing, see:
- `STAGE_8_TESTING_GUIDE.md` (10 test scenarios)
- `STAGE_8_CHECKLIST.md` (complete verification)

---

## 📚 DOCUMENTATION

- **STAGE_8_INTEGRATION_PLAN.md** — Architecture
- **STAGE_8_COMPLETION_REPORT.md** — Implementation
- **STAGE_8_SUMMARY.md** — Overview

---

**Quick start complete!**  
**Integration status:** ✅ Working  
**Next:** Full manual testing
