# Complete Q-MEDTRIAGE Unified Design Refactor Guide

## ✅ COMPLETED SO FAR

1. **App.jsx** - Removed LandingInfo sections
2. **stages.css** - Updated:
   - Design tokens (CSS variables)
   - Common stage layout
   - Upload stage
   - Preview stage

## 🚀 TO COMPLETE THE REFACTOR

### Step 1: Continue updating stages.css

Apply the same pattern to ALL remaining stages. For each stage:

**Pattern to Apply:**
```css
/* Example for any stage */
.{stage-name}-stage {
  min-height: 100vh;
  padding: 3rem 6vw;
}

.{stage-name}-header h2 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

.{stage-name}-description {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

/* Cards/Panels */
.{element} {
  background: rgba(0, 229, 255, 0.04);
  border: 1px solid var(--border-primary);
  border-radius: 4px;
}

/* Labels */
.{label} {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  font-family: "DM Mono", monospace;
  text-transform: uppercase;
  color: var(--text-tertiary);
}
```

**Stages to Update:**
1. ✅ Upload - DONE
2. ✅ Preview - DONE  
3. ⬜ Scanning
4. ⬜ Preprocessing
5. ⬜ Feature Extraction
6. ⬜ Dimensionality Reduction
7. ⬜ Quantum Processing
8. ⬜ Evidence Retrieval
9. ⬜ Reasoning
10. ⬜ Result
11. ⬜ Chat Interface
12. ⬜ Pipeline Progress

### Step 2: Update bulk-analysis.css

Apply same unified design to:

1. **Mode Selection**
```css
.mode-selection-header h1 {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 800;
  letter-spacing: -0.04em;
}

.mode-card {
  background: rgba(0, 229, 255, 0.04);
  border: 1px solid var(--border-primary);
  border-radius: 4px;
}

.mode-title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
}
```

2. **Bulk Upload**
```css
.bulk-upload-header h1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
}

.upload-dropzone {
  border: 2px dashed var(--border-primary);
  background: rgba(0, 229, 255, 0.02);
}
```

3. **Bulk Processing**
```css
.processing-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
}
```

4. **Bulk Results**
```css
.summary-title {
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 700;
}

.result-card {
  background: rgba(0, 229, 255, 0.04);
  border: 1px solid var(--border-primary);
}
```

### Step 3: Delete Unnecessary Files

```bash
# Delete these files
rm frontend/src/landing-info.css
rm frontend/src/components/LandingInfo.jsx
```

### Step 4: Build and Test

```bash
cd frontend
npm run build
```

Check for:
- Visual consistency
- Typography hierarchy
- Color scheme uniformity
- Responsive behavior
- All functionality works

## 📝 QUICK REFERENCE

### Font Sizes
- Hero/Main Title: `clamp(2.5rem, 6vw, 4.5rem)` weight: 800
- Section Title: `clamp(1.5rem, 3vw, 2.5rem)` weight: 700
- Body: `1rem` weight: 400
- Caption/Label: `0.7rem` weight: 700 (DM Mono)

### Colors
```css
Primary: #00e5ff (cyan)
Success: #35ef99 (green)
Accent: #7586ff (purple)
Background: #05060b
Text: #f7f8ff
Secondary Text: #858997
Tertiary Text: #555a68
Border: rgba(0, 229, 255, 0.25)
```

### Spacing
- Section padding: `3rem 6vw` (min) to `5rem 6vw` (max)
- Component gap: `1.5-2.5rem`
- Element gap: `1-1.5rem`

### Buttons
```css
/* Primary */
background: #00e5ff;
color: #031014;
padding: 1rem 2rem;
font-weight: 700;
letter-spacing: 0.12em;
text-transform: uppercase;

/* Secondary */
background: transparent;
border: 1px solid rgba(255, 255, 255, 0.12);
color: #c3c6d1;
```

## 🎯 EXPECTED RESULT

After completing all steps, the application will have:
1. ✅ Bold, consistent typography throughout
2. ✅ Unified cyan theme from hero to all stages
3. ✅ Compact, professional layouts
4. ✅ No visual discontinuity
5. ✅ Single design language
6. ✅ Faster maintenance (fewer CSS files)

## 🔧 IMPLEMENTATION COMMANDS

```bash
# To continue the refactor:

# 1. Update remaining stages in stages.css
# Follow the pattern shown above for each stage

# 2. Update bulk-analysis.css  
# Apply same design tokens and patterns

# 3. Delete old files
rm frontend/src/landing-info.css
rm frontend/src/components/LandingInfo.jsx

# 4. Test the build
cd frontend
npm run build

# 5. Run the app
npm run dev
```

## 💡 TIP

Use Find & Replace in your editor:
- Find: `font-weight: 200` → Replace: `font-weight: 800`
- Find: `font-weight: 600` → Replace: `font-weight: 700`
- Find: `rgba(0, 230, 255` → Replace: `rgba(0, 229, 255`
- Find: `#00e6ff` → Replace: `#00e5ff`
- Find: `border-radius: 12px` → Replace: `border-radius: 4px`
- Find: `letter-spacing: 0.15em` → Replace: `letter-spacing: 0.12em`

This will speed up the process significantly!
