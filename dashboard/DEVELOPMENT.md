# Q-MedTriage Frontend Development

## Current Status

### ✅ Completed (Commit 01)

1. **Project Metadata Updated**
   - Updated README.md to reflect JSRT dataset (not CheXpert)
   - Updated browser title to "Q-MedTriage | Quantum Medical Intelligence"

2. **Centralized Demo Data**
   - Created `/src/data/demoData.js` with structured mock data
   - All hardcoded values now reference centralized source
   - Clear separation between demo and future real data

3. **Data Architecture**
   - `DEMO_ANALYSIS` - Complete pipeline analysis data
   - `DEMO_QUANTUM_CIRCUIT` - Quantum visualization data
   - `DEMO_MODEL_COMPARISON` - Classical vs Quantum metrics
   - `DEMO_SYSTEM_STATUS` - System health indicators

4. **CNN Backbone Updated**
   - Changed from "MOBILENET" to "ResNet50"
   - Feature dimensions: 1280D → 2048D
   - All references now use `DEMO_ANALYSIS.cnn.*`

5. **Pipeline State Hook**
   - Created `/src/hooks/usePipeline.js`
   - Ready for future backend integration
   - Manages uploaded image and analysis state

6. **API Service Layer**
   - Created `/src/services/api.js`
   - Demo mode with simulated delays
   - Clean interface for backend integration
   - Functions ready: `analyzeImage`, `askQuestion`, `checkHealth`

7. **Updated Visualizations**
   - CNN: Now shows 2048 features
   - PCA: Shows 2048D → 4D compression
   - Quantum: Uses real PCA component values
   - Evidence: Maps over actual demo evidence array
   - Reasoning: Dynamic source count
   - Triage: Dynamic confidence percentage

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

### Phase 2: Image Propagation (Commits 02-05)
- [ ] Make uploaded image appear in preprocessing stage
- [ ] Show uploaded image in CNN stage
- [ ] Add visual flow indicators between stages
- [ ] Implement stage-to-stage transitions

### Phase 3: Enhanced Storytelling (Commits 06-10)
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
