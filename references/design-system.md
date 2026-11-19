# Design System — Eight Categories, Typography Intelligence, Color Intelligence, Accessibility, Design Tokens

## Purpose

The design engine gives every FileCraftBooster deliverable a coherent visual identity. It defines eight design categories (each a complete design language), typography intelligence for the Microsoft font stack, color intelligence (palette derivation, 60-30-10, accessible palettes), WCAG contrast rules, and emits a machine-readable design-token spec per deliverable.

## Scope

In scope: category selection, typography pairing, color palette derivation, layout density, imagery style, chart style, accessibility contrast, font-substitution handling, design-token output.

Out of scope: actual layout/rendering (handled by word/excel/powerpoint engines consuming these tokens); brand-logo extraction beyond seed-color input.

## The Eight Design Categories

Each category is a complete design language: typography pairing, color philosophy, layout density, imagery style, chart style. Select one per deliverable — do not mix categories within a single deliverable.

### 1. Corporate Executive
- **Typography:** Aptos (body) + Aptos Display or Arial (headings). Fallback: Calibri → Arial.
- **Color philosophy:** restrained — 1 brand color + neutrals (charcoal, slate, off-white). Color used for emphasis, not decoration.
- **Layout density:** medium-low; generous whitespace; one idea per slide/section.
- **Imagery:** professional photography, minimal illustration; corporate settings, diverse people.
- **Chart style:** clean lines/bars, minimal gridlines, direct labels over legends where possible.

### 2. Luxury Editorial
- **Typography:** Cambria or Georgia (serif body) + Didot/Bodoni-style display if licensed, else Cambria Display; high contrast sizes.
- **Color philosophy:** deep neutrals (ivory, charcoal, gold accent); monochrome-heavy with one metallic accent.
- **Layout density:** low; large imagery, generous margins, editorial whitespace.
- **Imagery:** high-end photography, texture, still-life; muted tones.
- **Chart style:** minimal or none — prefer tables and narrative; when charts needed, thin elegant lines.

### 3. Modern Technology
- **Typography:** Aptos/Segoe UI (UI feel) + Consolas for code/data; clean geometric sans.
- **Color philosophy:** dark or light with one vibrant accent (electric blue, cyan, violet); gradients subtle.
- **Layout density:** medium-high; cards, grids, dashboards; data-dense allowed.
- **Imagery:** product shots, abstract tech, UI screenshots; avoid stock-photo clichés.
- **Chart style:** modern — rounded bars, area fills, dark-mode aware, data labels.

### 4. Architectural & Engineering
- **Typography:** Arial/Helvetica-style sans for annotations + Times/Georgia for body text; monospace for specs.
- **Color philosophy:** blueprint-inspired — deep blue/white or graphite/amber; high contrast for readability.
- **Layout density:** high; drawings, dimensions, tables, specifications dominate.
- **Imagery:** technical drawings, renders, site photos, diagrams; precise, scaled.
- **Chart style:** technical — dimensioned, annotated, grid-referenced.

### 5. Financial & Analytical
- **Typography:** Arial/Calibri body + tabular-nums-friendly fonts; dense but legible.
- **Color philosophy:** conservative — navy, grey, white + semantic colors (green up / red down); avoid decorative color.
- **Layout density:** high; tables, KPIs, variance columns; every number formatted consistently (thousands separators, decimals, %).
- **Imagery:** minimal — charts and data viz are the visuals; photos only for context.
- **Chart style:** waterfall, variance, trend — precise axes, gridlines, number formatting.

### 6. Creative & Marketing
- **Typography:** expressive pairing — display sans + humanist sans or serif; bold headlines.
- **Color philosophy:** bold, energetic; 2–3 saturated colors + neutrals; color blocking.
- **Layout density:** varied — hero slides sparse, content slides denser; visual rhythm.
- **Imagery:** vibrant, diverse, aspirational; illustration + photography mix.
- **Chart style:** infographics, icon arrays, minimal traditional charts.

### 7. Academic & Research
- **Typography:** Times New Roman or Cambria (serif) throughout; strict hierarchy; numbered sections.
- **Color philosophy:** minimal — black text, minimal accent (one dark color); no decoration.
- **Layout density:** high; justified text, footnotes, references, tables.
- **Imagery:** figures, diagrams, data plots; formal captions ("Figure 1.").
- **Chart style:** publication-quality — error bars, significance marks, consistent axis formatting.

### 8. Government & Institutional
- **Typography:** Arial/Calibri or Times; formal, plain.
- **Color philosophy:** official palette — navy, institutional colors, restrained; accessibility-first.
- **Layout density:** medium-high; formal structure, numbered sections, official letterhead.
- **Imagery:** institutional photos, official seals, flags; formal.
- **Chart style:** clear, formal, WCAG-compliant; tables for precision.

## Category Selection — Keyword Mapping

| User keywords / signals | Category |
|---|---|
| board, investor, executive, quarterly, strategy, C-suite | Corporate Executive |
| luxury, premium, brand, editorial, magazine, high-end | Luxury Editorial |
| tech, SaaS, product, startup, app, AI, software, dashboard | Modern Technology |
| architecture, engineering, construction, CAD, BIM, blueprint, facility | Architectural & Engineering |
| finance, bank, audit, forecast, budget, KPI, analytics, report | Financial & Analytical |
| marketing, campaign, brand, creative, social, launch, promo | Creative & Marketing |
| research, paper, thesis, academic, study, journal, scientific | Academic & Research |
| government, policy, compliance, institutional, public sector, tender | Government & Institutional |

**Tie-breakers:** audience seniority → Corporate Executive; visual-heavy request → Creative/Luxury; data-heavy → Financial/Academic; regulated industry → Government.

## Typography Intelligence

### Microsoft Font Stack — When to Use Each

| Font | Role | When to use | Pairing notes |
|---|---|---|---|
| **Aptos / Aptos Display** | Default Office sans (2023+) | Modern Office docs, tech, corporate | Body: Aptos; Display: Aptos Display for headings |
| **Arial** | Universal sans | Maximum compatibility, fallback, government | Safe everywhere; slightly dated feel |
| **Calibri** | Legacy Office default | Existing Office docs, conservative business | Pairs with Cambria |
| **Cambria** | Office serif | Academic-ish business docs, formal reports | Body serif; pairs with Calibri |
| **Georgia** | Web-safe serif | When Cambria unavailable; warmer serif | Good screen serif |
| **Times New Roman** | Traditional serif | Academic, legal, government | Strict, formal; small x-height at small sizes |
| **Segoe UI** | Windows UI sans | Dashboards, internal tools, tech | Pairs with Consolas |
| **Verdana** | Wide sans | Low-vision accessibility, presentations | Wide, readable at distance |
| **Consolas** | Monospace | Code, data tables, technical specs | Data alignment |
| **Trebuchet MS** | Humanist sans | Friendly business, marketing | More character than Arial |
| **Courier New** | Legacy monospace | Code in formal docs | Consolas preferred |

### Fallback Chains (cross-platform export)

Every font declaration gets a fallback chain ending in generic family:

```
Primary: Aptos, 'Segoe UI', Arial, sans-serif
Display: 'Aptos Display', Aptos, Arial, sans-serif
Serif body: Cambria, Georgia, 'Times New Roman', serif
Mono: Consolas, 'Courier New', monospace
```

When embedding fonts in PDF: subset-embed for size; never embed proprietary fonts without license (see `licensing-and-attribution.md`).

### Typography Rules

- Body size: 10–11pt print docs, 18–24pt slides, 14–16px dashboards.
- Line height: 1.15–1.5× font size; never <1.0.
- Measure: 50–75 characters per line for body text.
- Hierarchy: max 3–4 levels; consistent size ratios (e.g., 1.25 or 1.333 scale).
- Never use more than 2 font families per deliverable (display + body, or body + mono).

## Color Intelligence

### Palette Derivation from Brand

Given a seed hex (from logo/brand):

1. **Extract seed** — dominant brand color; if multiple, pick the most saturated as primary.
2. **Build neutrals** — derive a neutral ramp (dark → light) tinted toward the seed hue at low saturation (5–15%).
3. **Build accent** — complementary or analogous hue at high saturation for accents/CTAs.
4. **Apply 60-30-10:**
   - **60%** neutral/background (white, off-white, light grey)
   - **30%** secondary (neutral dark, secondary brand tint)
   - **10%** accent (brand color, CTAs, highlights)
5. **Validate contrast** — run WCAG check on all text/background pairs (below).

### Accessible Palette Generation

- Text on background: ≥4.5:1 (normal text), ≥3:1 (large text ≥18pt or 14pt bold, UI components).
- Never rely on color alone — pair with icon, label, or pattern (accessibility requirement).
- Provide a dark-mode variant when the category is Modern Technology: invert neutrals, keep accent, re-verify contrast.
- Semantic colors: success = green, warning = amber, error = red, info = blue — consistent across deliverable.

### Color Token Output

Emit per deliverable (see Output Spec):

```yaml
colors:
  primary: "#1A56DB"        # brand/accent
  primary_dark: "#1E40AF"   # hover/pressed
  secondary: "#6B7280"      # neutral secondary
  background: "#FFFFFF"     # 60%
  surface: "#F9FAFB"        # cards/panels
  text_primary: "#111827"   # 30%+text
  text_secondary: "#4B5563"
  text_inverse: "#FFFFFF"
  accent: "#F59E0B"         # 10% accent
  success: "#059669"
  warning: "#D97706"
  error: "#DC2626"
  border: "#E5E7EB"
```

## Accessibility Contrast Rules (WCAG 2.1 AA)

- **Normal text:** ≥4.5:1 contrast ratio vs background.
- **Large text** (≥18pt / 24px, or ≥14pt bold): ≥3:1.
- **UI components & graphical objects:** ≥3:1 vs adjacent colors.
- **Focus indicators:** ≥3:1 vs background.
- **Never** use color as sole differentiator — add labels, patterns, or icons.

**Enforcement:** after palette derivation, compute contrast ratios for all text/background pairs; auto-adjust lightness/darkness until compliant; if a pair can't reach 4.5:1 without breaking brand, flag it and propose nearest compliant variant.

## Output Specification — Design Tokens

Every deliverable emits a `design-tokens.yaml` (or JSON) consumed by the app engines:

```yaml
deliverable_id: "q3-board-deck"
category: "corporate_executive"
fonts:
  heading: { family: "Aptos Display", fallback: ["Aptos", "Arial", "sans-serif"], size_pt: 32, weight: 600 }
  body:    { family: "Aptos", fallback: ["Segoe UI", "Arial", "sans-serif"], size_pt: 14, weight: 400 }
  mono:    { family: "Consolas", fallback: ["Courier New", "monospace"], size_pt: 11 }
colors:    # as above
spacing:
  base_unit: 8   # px/pt
  scale: [4, 8, 12, 16, 24, 32, 48, 64]
layout:
  density: "medium-low"
  max_content_width: "900pt"   # for docs
  slide_aspect: "16:9"
charts:
  style: "clean-lines"
  palette: ["primary", "secondary", "accent", "success", "warning"]
imagery:
  style: "professional-photography"
  treatment: "scrim-for-text"
accessibility:
  wcag_level: "AA"
  min_contrast_text: 4.5
  min_contrast_large: 3.0
```

## Error Handling

- **Font not installed:** check system fonts; if missing, apply substitution table — e.g., Aptos → Calibri/Arial; Cambria → Georgia; Segoe UI → Arial; Consolas → Courier New. Record substitution in `assumptions`.
- **Brand color too light/dark for text:** auto-generate accessible variant; never ship non-compliant text.
- **Category ambiguous:** apply keyword mapping; if still unclear, default Corporate Executive for business docs, Modern Technology for tech requests, Academic for research.
- **Conflicting constraints** (brand color fails contrast, luxury category wants light text on light bg): prioritize accessibility; propose adjusted palette; flag for user review.
- **Missing brand seed:** derive a professional default palette for the category; mark `colors: derived-default` in tokens.

## Practical Examples

**Example 1 — Board deck.** Input: "Q3 board presentation, financial data". → Category: Corporate Executive. Fonts: Aptos Display headings + Aptos body. Colors: derived from brand navy `#1E3A8A` → primary navy, neutrals cool grey, accent amber. Charts: clean lines with direct labels. Tokens emitted; Word/PPT engines consume.

**Example 2 — Tech product launch.** Input: "SaaS product launch deck, dark theme". → Category: Modern Technology. Fonts: Segoe UI + Consolas for code. Colors: dark background `#0F172A`, accent electric blue `#3B82F6`, card surface `#1E293B`. Charts: rounded bars, dark-mode. Verify all text ≥4.5:1 on dark bg.

**Example 3 — Academic paper.** Input: "research report with figures". → Category: Academic & Research. Fonts: Times New Roman throughout. Colors: black text, minimal navy accent for headings. Density: high, justified. Charts: publication style with error bars. No decoration.

**Example 4 — Font missing.** Request uses "Aptos Display" but system only has Calibri. → Substitution: `Aptos Display → Calibri (headings), Aptos → Calibri (body)`; note in assumptions; if target is PDF, embed Calibri subset.

## Quality Standards

- One category per deliverable; tokens consistent across all generated files in a bundle.
- All text/background pairs pass WCAG AA (4.5:1 / 3:1) — verified programmatically before output.
- Typography: ≤2 families, consistent scale, fallback chains complete.
- Color: 60-30-10 distribution respected; semantic colors consistent.
- Design tokens are complete and machine-readable; every app engine can consume them without re-deriving.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
