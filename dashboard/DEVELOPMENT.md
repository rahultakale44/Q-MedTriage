# Q-MedTriage Frontend Development

## Current Status

### ✅ Completed (Commit 01)

1. **Project Metadata Updated**
2. **Centralized Demo Data**
3. **Data Architecture**
4. **CNN Backbone Updated**
5. **Pipeline State Hook**
6. **API Service Layer**
7. **Updated Visualizations**

### ✅ Completed (Commit 02)

1. **Image Propagation Through Pipeline**
   - Uploaded image now appears in PREPROCESS stage
   - Uploaded image now appears in CNN (VISION) stage
   - User's actual X-ray flows through early pipeline stages
   - FakeXray only shows when no image uploaded

2. **Visual Flow Indicators**
   - Added "DATA FLOWS TO [NEXT STAGE]" indicators between stages
   - Arrow icons show progression direction
   - Helps user understand stage connections

3. **Stage Transition Animations**
   - Smooth fade and scale transitions between stages
   - Each stage animates in with opacity and scale
   - Creates cohesive flow feeling

4. **Pipeline Status Indicators**
   - Mini image preview in pipeline header when image uploaded
   - "IMAGE IN PIPELINE" indicator shows active analysis
   - Stage progress dots at bottom show completed stages
   - Dots illuminate as user scrolls through stages

5. **Enhanced Stage Descriptions**
   - Each stage now explains INPUT → PROCESS → OUTPUT
   - More detailed descriptions of what happens at each step
   - Better technical communication of the architecture

6. **Performance**
   - Dynamic latency display from demo data
   - All builds successful (349KB bundle)
   - No console errors

## Architecture

```
dashboard/src/
├── data/
│   └── demoData.js          # Centralized demo data
├── hooks/
│   └── usePipeline.js       # Pipeline state management
├── services/
│   └── api.js               # Backend communication layer
├── components/              # [To be organized]
├── App.jsx                  # Main application
└── App.css                  # Styles
```

## Next Steps

### ~~Phase 2: Image Propagation (Commits 02-05)~~ ✅ DONE
- [x] Make uploaded image appear in preprocessing stage
- [x] Show uploaded image in CNN stage
- [x] Add visual flow indicators between stages
- [x] Implement stage-to-stage transitions
- [x] Add pipeline progress indicators

### Phase 3: Enhanced Storytelling (Commits 03-07)
- [ ] Add "data flowing" animations
- [ ] Improve INPUT → PROCESS → OUTPUT narrative
- [ ] Add stage connection lines
- [ ] Better scroll-driven reveals

### Phase 4: Component Organization (Commits 11-15)
- [ ] Review `/components/` directory files
- [ ] Extract reusable components from App.jsx
- [ ] Create proper component hierarchy
- [ ] Remove unused component files

### Phase 5: Backend Integration (Commits 16-20)
- [ ] Connect `usePipeline` hook to API service
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test with real backend

## Demo Data vs Real Data

### Current Approach
All visualizations use `DEMO_ANALYSIS` from `/src/data/demoData.js`.

### Future Integration
When backend is ready:
1. Update `USE_DEMO_DATA = false` in `/src/services/api.js`
2. Update `BASE_URL` to point to deployed backend
3. API responses should match the structure in `demoData.js`

### Expected Backend Response Shape
```javascript
{
  image: { status, format, dimensions },
  preprocessing: { steps, output },
  cnn: { backbone, featureDimension, extractionTime },
  pca: { inputDimension, outputDimension, components },
  classical: { model, prediction, confidence },
  quantum: { model, qubits, prediction, confidence },
  evidence: { results: [{ title, relevance, source }] },
  reasoning: { explanation },
  triage: { classification, confidence, priority }
}
```

## Development Commands

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint
```

## Dataset Status

**Current Dataset**: JSRT (Nodule / Non-Nodule)
**Status**: Downloading in background
**Frontend Strategy**: Continue development with demo data

Once dataset download completes:
1. Inspect actual file structure
2. Update preprocessing pipeline
3. Train models
4. Replace demo data with real results

## Key Design Principles

1. **Storytelling First**: Pipeline stages should feel connected
2. **One Analysis Journey**: Uploaded image flows through entire system
3. **Clear Demo Mode**: Always distinguish demo from real data
4. **Backend Ready**: Architecture prepared for API integration
5. **Medical Safety**: Always emphasize "AI-assisted, not diagnostic"

## Notes

- All hardcoded medical values are now in `demoData.js`
- CNN backbone is configurable (currently ResNet50)
- Feature dimensions reflect ResNet50 output (2048D)
- PCA compression: 2048D → 4D
- Quantum circuit: 4 qubits for 4-dimensional input
- Confidence values are realistic but demo data
