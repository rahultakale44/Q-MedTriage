# Q-MEDTRIAGE Unified Design System

## ✅ COMPLETED CHANGES

### 1. App.jsx
- ✅ Removed LandingInfo imports and sections
- ✅ Simplified landing to just HeroSection
- ✅ Removed landing-info.css import

### 2. stages.css - Started
- ✅ Added design token variables
- ✅ Updated common stage layout with bold typography
- ✅ Updated upload stage to match hero aesthetic

## 🚧 REMAINING WORK

### stages.css (Continue updating)
Need to update all remaining stage styles to match the unified system:

**Font Sizes to Apply:**
- Stage Titles: `clamp(2.5rem, 5vw, 4.5rem)` with `font-weight: 800`
- Section Headers: `clamp(1.5rem, 3vw, 2.5rem)` with `font-weight: 700`  
- Body Text: `1rem` with `font-weight: 400`
- Labels: `0.7rem` DM Mono with `font-weight: 700`

**Colors to Apply:**
- Primary borders: `rgba(0, 229, 255, 0.25)`
- Backgrounds: `rgba(0, 229, 255, 0.04)`
- Text primary: `#f7f8ff`
- Text secondary: `#858997`
- Cyan: `#00e5ff`
- Green: `#35ef99`

**Stages Needing Update:**
1. Preview Stage
2. Scanning Stage
3. Preprocessing Stage
4. Feature Extraction Stage
5. Dimensionality Reduction Stage
6. Quantum Processing Stage
7. Evidence Retrieval Stage
8. Reasoning Stage
9. Result Stage
10. Chat Interface
11. Pipeline Progress

### bulk-analysis.css
Need to apply same unified design:
1. Mode Selection - Bold headings, cyan theme
2. Bulk Upload - Match upload stage
3. Bulk Processing - Bold progress indicators
4. Bulk Results - Compact card layout

### Component Updates
May need to update component JSX if class names changed:
- UploadStage.jsx
- AnalysisModeSelection.jsx
- BulkUploadStage.jsx
- All other stage components

## 🎨 DESIGN PRINCIPLES

### Typography Hierarchy
```css
/* Hero/Stage Title */
font-size: clamp(2.5rem, 6vw, 4.5rem);
font-weight: 800;
letter-spacing: -0.04em;
line-height: 1;

/* Section Header */
font-size: clamp(1.5rem, 3vw, 2.5rem);
font-weight: 700;
letter-spacing: -0.02em;

/* Body */
font-size: 1rem;
font-weight: 400;
line-height: 1.7;

/* Label/Caption */
font-size: 0.7rem;
font-family: "DM Mono";
font-weight: 700;
letter-spacing: 0.15em;
text-transform: uppercase;
```

### Spacing System
```css
/* Vertical rhythm */
Section padding: clamp(3rem, 6vh, 5rem)
Component gap: clamp(1.5rem, 3vh, 2.5rem)
Element gap: 1-1.5rem

/* Horizontal */
Container: 6vw padding
Max-width: 1400px
```

### Color System
```css
--primary-cyan: #00e5ff;
--success-green: #35ef99;
--accent-purple: #7586ff;
--bg-dark: #05060b;
--text-primary: #f7f8ff;
--text-secondary: #858997;
--text-tertiary: #555a68;
--border-primary: rgba(0, 229, 255, 0.25);
--border-subtle: rgba(255, 255, 255, 0.08);
```

### Component Patterns
```css
/* Cards/Panels */
background: rgba(0, 229, 255, 0.04);
border: 1px solid rgba(0, 229, 255, 0.25);
border-radius: 4px;
padding: 1.5-2rem;

/* Primary Button */
background: #00e5ff;
color: #031014;
padding: 1rem 2rem;
font-weight: 700;
letter-spacing: 0.12em;
text-transform: uppercase;

/* Secondary Button */
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(255, 255, 255, 0.12);
color: #c3c6d1;

/* Input/Dropzone */
border: 2px dashed rgba(0, 229, 255, 0.25);
background: rgba(0, 229, 255, 0.02);
```

## 📋 IMPLEMENTATION CHECKLIST

- [x] Remove LandingInfo from App.jsx
- [x] Add design tokens to stages.css
- [x] Update common stage layout
- [x] Update upload stage
- [ ] Update preview stage
- [ ] Update all processing stages (7 remaining)
- [ ] Update result stage
- [ ] Update chat interface
- [ ] Update bulk-analysis.css (mode selection)
- [ ] Update bulk-analysis.css (upload)
- [ ] Update bulk-analysis.css (processing)
- [ ] Update bulk-analysis.css (results)
- [ ] Delete landing-info.css
- [ ] Delete components/LandingInfo.jsx
- [ ] Test all stages for visual consistency
- [ ] Test responsive behavior
- [ ] Verify functionality intact

## 🎯 EXPECTED OUTCOME

After completion:
1. Bold, consistent typography throughout
2. Unified cyan/green color scheme
3. More compact, professional layouts
4. Visual continuity from hero to all stages
5. Single source of truth for styling (App.css + stages.css + bulk-analysis.css)
6. No disconnected "thin font" sections
7. Professional medical AI aesthetic throughout
