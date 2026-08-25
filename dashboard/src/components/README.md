# Q-MedTriage Components

This directory contains reusable React components extracted from the main App.jsx.

## Component Organization

### Navigation Components

#### `Navbar.jsx`
Top navigation bar with:
- Q-MedTriage branding
- Navigation links (Overview, Pipeline, Quantum, Evidence, Triage)
- System online status indicator

**Props:**
- `activeStage` (number) - Current active pipeline stage
- `onNavigate` (function) - Callback for navigation clicks

#### `StageNavigation.jsx`
Vertical stage dots navigation on the right side of the screen.

**Props:**
- `stages` (array) - Array of stage objects
- `activeStage` (number) - Current active stage index
- `onNavigate` (function) - Callback for stage navigation

#### `ScrollProgress.jsx`
Animated top progress bar showing scroll position.

**Props:**
- `progressWidth` (MotionValue) - Framer Motion value for width

### Utility Components

#### `FakeXray.jsx`
Stylized fake chest X-ray visualization used as placeholder when no real image is uploaded.

**Props:** None

#### `AutoRunButton.jsx`
Toggle button for automatic pipeline progression mode.

**Props:**
- `isRunning` (boolean) - Whether auto-run is active
- `onToggle` (function) - Callback for toggle

## Component Architecture

```
App.jsx (Main Container)
├── Navbar
├── ScrollProgress
├── StageNavigation
├── Hero (inline)
│   └── HeroCore (inline)
├── Pipeline Story (inline)
│   ├── PipelineCore (inline)
│   │   ├── InputVisual
│   │   │   └── FakeXray (component)
│   │   ├── PreprocessVisual
│   │   │   └── FakeXray (component)
│   │   ├── CNNVisual
│   │   │   └── FakeXray (component)
│   │   ├── PCAVisual
│   │   ├── QuantumVisual
│   │   ├── EvidenceVisual
│   │   ├── ReasonVisual
│   │   └── TriageVisual
│   └── SceneDetails (inline)
├── FinalSystem (inline)
├── Footer (inline)
└── AutoRunButton
```

## Future Extraction Candidates

The following sections in App.jsx could be extracted into components in future refactoring:

1. **Hero.jsx** - Hero section with animated core
2. **HeroCore.jsx** - Animated orbital visualization
3. **PipelineVisualizations/** - Directory for all stage visualizations
   - InputVisual.jsx
   - PreprocessVisual.jsx
   - CNNVisual.jsx
   - PCAVisual.jsx
   - QuantumVisual.jsx
   - EvidenceVisual.jsx
   - ReasonVisual.jsx
   - TriageVisual.jsx
4. **SceneDetails.jsx** - Stage-specific detail panels
5. **FinalSystem.jsx** - Final system chain section
6. **Footer.jsx** - Footer component

## Design Principles

1. **Single Responsibility** - Each component has one clear purpose
2. **Props Over State** - Components receive data via props when possible
3. **Composition** - Build complex UIs from simple components
4. **Reusability** - Components can be used in different contexts
5. **Clean Separation** - Navigation/UI separate from visualizations

## Styling

All component styles are currently in `App.css`. This centralized approach:
- Keeps styles consistent
- Avoids CSS module overhead
- Makes theme changes easier
- Maintains existing visual identity

If components grow significantly, consider:
- CSS modules per component
- Styled-components
- Tailwind CSS (with careful consideration)
