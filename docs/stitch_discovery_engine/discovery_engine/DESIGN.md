---
name: Discovery Engine
colors:
  surface: '#fcf8ff'
  surface-dim: '#dcd8e5'
  surface-bright: '#fcf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f2ff'
  surface-container: '#f0ecf9'
  surface-container-high: '#eae6f4'
  surface-container-highest: '#e4e1ee'
  on-surface: '#1b1b24'
  on-surface-variant: '#464555'
  inverse-surface: '#302f39'
  inverse-on-surface: '#f3effc'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#7e3000'
  on-tertiary: '#ffffff'
  tertiary-container: '#a44100'
  on-tertiary-container: '#ffd2be'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb695'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7b2f00'
  background: '#fcf8ff'
  on-background: '#1b1b24'
  surface-variant: '#e4e1ee'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  h1:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  h2:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  micro:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 1.5rem
  margin-page: 2rem
  stack-xs: 0.25rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 1.5rem
---

## Brand & Style
The design system for this platform is built on the principles of **Precision, Clarity, and Efficiency**. Targeting enterprise product teams and analysts, the UI evokes a sense of high-performance utility similar to world-class engineering tools.

The aesthetic follows a **Modern Corporate Minimalism** movement. It prioritizes data density without clutter, using generous whitespace to separate functional areas and a high-contrast typographic hierarchy to guide the eye. Visual flourishes are strictly functional, employing subtle borders and soft tonal shifts rather than heavy shadows or decorative elements. The goal is to provide a "quiet" interface where user data is the protagonist.

## Colors
The palette is rooted in a neutral "Slate" scale to maintain professional gravitas. 

- **Primary (Indigo):** Reserved strictly for primary call-to-actions, active navigation states, and critical interaction points.
- **Neutrals:** Uses a deep charcoal (#0F172A) for primary headings to ensure AAA accessibility. Borders use a light gray (#E2E8F0) to define structure without creating visual noise.
- **Semantic Colors:** Success, Warning, and Error states use highly legible, standard tones. These should be used sparingly in charts and status badges to maintain the system's restrained aesthetic.
- **Surfaces:** The primary application background is a very faint gray (#F8FAFC), while interactive cards and containers use pure white (#FFFFFF) to create a subtle layered effect.

## Typography
This design system utilizes **Inter** for its exceptional legibility in data-heavy environments. 

- **Weight Usage:** Use `600` for all headings to provide a strong structural anchor. Use `500` for UI labels, buttons, and table headers. Use `400` for all long-form body text and descriptions.
- **Scale:** High-level analytics (KPIs) should use `display-lg`. Section headers within dashboards use `h2`.
- **Micro-copy:** Use the `micro` style for overline text or very small metadata, ensuring the uppercase transformation and letter spacing are applied for readability at small sizes.

## Layout & Spacing
The layout follows a **Fixed-Fluid hybrid grid**. The main content area is capped at 1440px to prevent excessive line lengths on ultra-wide monitors, centering itself with dynamic margins.

- **Sidebar:** Fixed width at 240px. It should be pinned to the left with a subtle background color shift to distinguish it from the workspace.
- **Grid:** A 12-column grid system is used for dashboard layouts. KPI cards typically span 3 columns (4 per row), while primary charts span 8 or 12 columns.
- **Density:** Maintain a 16px (1rem) base unit for internal component padding, increasing to 24px (1.5rem) for outer card padding to emphasize the "Premium" feel.

## Elevation & Depth
Depth is communicated through **Tonal Layering** and **Low-Contrast Outlines**.

- **Level 0 (Background):** The canvas uses a soft neutral tint (#F8FAFC).
- **Level 1 (Cards/Surface):** White surfaces with a 1px border (#E2E8F0). Do not use shadows for standard containers.
- **Level 2 (Interactive/Floating):** For dropdowns, popovers, and modals, use a very soft, diffused shadow: `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`.
- **Active State:** When a card or element is selected, replace the gray border with a 1px Primary Indigo border or a 2px offset "ring".

## Shapes
The design system uses a **Rounded** (0.5rem / 8px) corner radius as the standard for all primary UI components, including buttons, input fields, and cards.

- **Standard (8px):** Components like cards and large buttons.
- **Large (12px):** Used for "rounded-lg" on larger modal containers or featured dashboard widgets.
- **Full (Pill):** Used exclusively for status tags and badges to differentiate them from interactive buttons.

## Components
- **Buttons:** Primary buttons use a solid Indigo background with white text. Secondary buttons use a white background with a gray border. High-density views can use "Ghost" buttons (text only) to reduce visual noise.
- **Data Tables:** Headers must be `label-sm` with a subtle gray background or bottom-only border. Rows should have a fixed height (48px for standard, 40px for compact) with a 1px border-bottom.
- **KPI Cards:** Feature a `display-lg` number in the primary text color, paired with a `label-sm` title in secondary gray above the value.
- **Sidebar Navigation:** Use a deep Slate background (#0F172A). Active items should have a subtle left-aligned indigo accent bar and a low-opacity white background highlight.
- **Tags/Badges:** Use "Pill" shapes with 10% opacity backgrounds of the semantic color (e.g., Sage green background at 10% for success text).
- **Input Fields:** 1px border with 8px radius. On focus, the border transitions to Primary Indigo with a soft 3px indigo glow (halo).
- **Charts:** Use a flat palette. Avoid gradients and shadows. Line charts should use a 2px stroke width. Tooltips should follow the "Level 2" elevation rules.