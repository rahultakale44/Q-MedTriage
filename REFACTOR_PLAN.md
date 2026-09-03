# Q-MEDTRIAGE UNIFIED DESIGN REFACTOR

## Problem
- Visual discontinuity after hero section
- Thin fonts vs bold hero typography
- Different color schemes
- Too much empty space
- Multiple CSS files creating inconsistency

## Solution
Create unified design system throughout the entire application.

## Design Principles
1. **Bold Typography**: Use clamp(42px, 4vw, 65px) minimum for headings
2. **Cyan Theme**: #00e5ff primary, #35ef99 success, #7586ff accent
3. **Monospace Details**: DM Mono for technical labels
4. **Compact Spacing**: Reduce empty space, increase information density
5. **Consistent Borders**: rgba(0, 229, 255, 0.25) for primary elements

## Files to Update
1. ✅ App.jsx - Remove LandingInfo sections, simplify
2. ✅ stages.css - Apply unified styling to all stages
3. ✅ bulk-analysis.css - Match hero aesthetic
4. ❌ DELETE landing-info.css
5. ❌ DELETE components/LandingInfo.jsx

## Typography Scale
- Hero/Stage Titles: clamp(42px, 6vw, 85px)
- Section Headers: clamp(28px, 3vw, 48px)
- Body: 14-16px
- Labels: 8-10px (DM Mono)

## Color Palette
- Primary: #00e5ff (cyan)
- Success: #35ef99 (green)
- Accent: #7586ff (purple)
- Background: #05060b
- Text: #f7f8ff
- Secondary Text: #858997

## Layout Principles
- Max width: 1400px
- Padding: 6vw horizontal
- Section gaps: 80-120px
- Component gaps: 24-32px
