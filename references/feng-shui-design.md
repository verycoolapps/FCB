# Feng Shui-Inspired Design Intelligence for Documents and Decks

## Purpose

Apply balanced, element-inspired palettes and composition cues to Microsoft 365
documents, spreadsheets, and slide decks. The system treats the five classical
elements — Wood, Fire, Earth, Metal, Water — as a design vocabulary for color,
texture, and spatial rhythm, producing palettes that feel harmonious without
imposing superstition.

## Critical Framing Rules (Read First)

1. **This is optional aesthetic styling.** It is never superstition, never a
   claim about fortune, luck, or fate. Present every output as an
   "element-inspired palette," not a "Feng Shui correction."
2. **Always offer a non-Feng-Shui alternative.** Every recommended palette must
   ship alongside a neutral brand-default alternative so the user can opt out.
3. **Never fabricate or request birth data.** Do not ask for date of birth,
   hour of birth, zodiac sign, or any bazi/horoscope input. This skill does not
   perform birth-data analysis, and such requests are out of scope.
4. **Never claim fortune-telling outcomes.** No language about "attracting
   wealth," "fixing career energy," or "changing fortune." Deliverable copy must
   describe visual properties only (contrast, hierarchy, warmth, focus).
5. **Disclose the metaphor.** When a palette is suggested, state plainly that
   the element names are metaphorical design labels, not predictions.

## Scope

- Word (.docx) report and proposal styling
- Excel (.xlsx) dashboard and workbook theming
- PowerPoint (.pptx) decks and template masters
- PDF export styling
- OneDrive/SharePoint branded collateral produced via FileCraftBooster

Out of scope: interior design, architecture, bazi/horoscope consultation,
physically rearranging furniture or offices.

## Capabilities

- Element palette generation per deliverable type (hex palettes + named colors)
- Texture/material cue selection (subtle fills, borders, background tints)
- Bagua-inspired spatial mapping translated to document layout zones
- Mode selection (Corporate Balanced, Creative Bold, Calm Minimal,
  Executive Authority, Wellness Soft)
- JSON output spec consumed by downstream styling scripts
- Non-Feng-Shui fallback palette recommendation

## The Five Elements — Design Vocabulary

### Wood (木) — Growth, Renewal, Creativity

- **Palette direction:** greens and teals.
  - Deep anchor: `#2E5941` (Pine), `#1F4D3A` (Forest)
  - Mid: `#4A7C59` (Sage), `#7FB069` (Leaf)
  - Accent: `#A3D9A5` (Spring), `#D4ECDD` (Mist)
- **Secondary accent options:** `#C9A227` (ochre), `#8B5E34` (bark brown)
- **Material/texture cues:** organic gradients, leaf-pattern header rules,
  soft rounded corners (6–10pt), matte finishes in print
- **Document associations:** creativity, new ventures, learning, family growth

### Fire (火) — Passion, Visibility, Energy

- **Palette direction:** reds, oranges, warm golds — use sparingly for
  emphasis only; large areas overwhelm.
  - Deep anchor: `#8B1E1E` (Ember), `#B33A2B` (Crimson)
  - Mid: `#D96C3D` (Flame), `#E8975A` (Amber)
  - Accent: `#F4D35E` (Gold), `#FFF3D6` (Parchment)
- **Material/texture cues:** high-contrast title bands, bold rule lines,
  diagonal energy lines used at most once per page
- **Document associations:** visibility, recognition, launches, performance
- **Caution:** never use Fire-dominant palettes for dense financial tables;
  restrict to headers, callouts, and cover slides.

### Earth (土) — Stability, Support, Foundations

- **Palette direction:** ochres, tans, warm neutrals — the default corporate
  base.
  - Deep anchor: `#7A5C3E` (Sienna), `#5C4A32` (Umber)
  - Mid: `#B08968` (Clay), `#D4A373` (Sand)
  - Accent: `#E8DCC4` (Linen), `#F2E9DC` (Bone)
- **Material/texture cues:** solid fills, subtle grid textures, generous
  whitespace, serif headings
- **Document associations:** stability, trust, administration, contracts,
  operations, health support

### Metal (金) — Precision, Clarity, Efficiency

- **Palette direction:** silvers, cool grays, whites — high-contrast
  analytical feel.
  - Deep anchor: `#3D4852` (Slate), `#2B2F36` (Charcoal)
  - Mid: `#6B7280` (Steel), `#9CA3AF` (Silver)
  - Accent: `#E5E7EB` (Mist), `#F9FAFB` (Paper)
  - Optional warm metal: `#B08D57` (Brass), `#C9A227` (Gold leaf)
- **Material/texture cues:** hairline rules, tabular numerals, clean sans-serif,
  sharp corners, minimal decoration
- **Document associations:** analysis, finance, engineering, precision,
  logistics, "useful people" (mentor/support networks)

### Water (水) — Flow, Communication, Wisdom

- **Palette direction:** blues and deep teals — communication and calm.
  - Deep anchor: `#1B4F72` (Deep), `#16425B` (Abyss)
  - Mid: `#2E86AB` (Wave), `#5DADE2` (Sky)
  - Accent: `#A9D6E5` (Foam), `#EAF4F8` (Ice)
- **Material/texture cues:** flowing horizontal rules, soft gradients,
  generous line spacing (1.15–1.3)
- **Document associations:** communication, learning, travel, adaptability,
  career flow

## Bagua-to-Layout Mapping (Document Spatial Zones)

The classical eight-direction Bagua is adapted to page regions. This is a
layout-composition metaphor only — it does not assert any fortune effect.

| Bagua Area | Life Area (metaphor) | Document Zone | Recommended Element | Use For |
|---|---|---|---|---|
| Career (North) | Ambition, path | Top-center / running header | Water | Page headers, section banners |
| Knowledge (NE) | Learning, study | Upper-left margins | Earth | Sidebar notes, study guides |
| Family (E) | Health, roots | Left column | Wood | Recurring section dividers |
| Wealth (SE) | Resources, value | Lower-left / financial tables | Metal | KPI tables, pricing blocks |
| Relationships (S) | People, partnerships | Bottom-center / footer | Fire | Signature blocks, contact areas |
| Creativity (SW) | Ideas, innovation | Lower-right | Wood | Idea boxes, brainstorm panels |
| Helpful People (W) | Support, mentors | Right column | Metal | Reviewer boxes, endorsement areas |
| Fame (NW) | Recognition, reputation | Top-right / cover corner | Fire | Cover accents, achievement callouts |

**Center (Tai Chi):** the document's core message — the summary box, executive
summary, or cover headline. Keep it visually dominant and uncluttered.

### Applying the Mapping

- Do NOT color every zone differently — that produces noise. Select **one
  primary element** (60–70% of color weight) and **one accent element**
  (15–25%); remaining zones use neutrals.
- For dense documents (contracts, SOPs), collapse the mapping to a single
  accent element and keep everything else in Earth/neutral tones.
- For decks, apply mapping per-slide rather than per-page; one element per
  slide section is sufficient.

## Application Modes

### Corporate Balanced (default)

- Base: Earth neutrals + Metal structure
- Accent: one Water or Wood highlight
- Best for: reports, proposals, internal comms, SOPs
- Hex set example: `#5C4A32` / `#B08968` / `#2E86AB` / `#F2E9DC`

### Creative Bold

- Base: Wood greens + generous Fire accents
- High contrast, expressive
- Best for: marketing decks, campaign materials, pitch visuals
- Constraint: Fire area ≤ 15% of slide/page area
- Hex set example: `#2E5941` / `#D96C3D` / `#F4D35E` / `#EAF4F8`

### Calm Minimal

- Base: Water blues desaturated + white space
- Minimal accents; soft gradients allowed
- Best for: wellness content, HR docs, onboarding, reading-heavy reports
- Hex set example: `#16425B` / `#A9D6E5` / `#F9FAFB` / `#EAF4F8`

### Executive Authority

- Base: Metal charcoal/silver + Earth warmth
- Serif headings, hairline rules, restrained palette
- Best for: board decks, annual reports, policy documents
- Hex set example: `#2B2F36` / `#B08D57` / `#6B7280` / `#F9FAFB`

### Wellness Soft

- Base: Earth + Water blend (warm neutrals + soft blues/greens)
- Rounded shapes, low contrast, gentle imagery cues
- Best for: healthcare, education, employee wellbeing, HR
- Hex set example: `#B08968` / `#7FB069` / `#A9D6E5` / `#F2E9DC`

## Decision Rules

1. **When to apply:** Only when the user requests a styled/premium/branded
   deliverable or explicitly mentions feng shui, elements, or palette themes.
   Default deliverables use Corporate Balanced or the existing brand palette.
2. **Mode selection by deliverable:**
   - Contract, SOP, policy → Corporate Balanced or Executive Authority
   - Sales pitch, marketing → Creative Bold
   - Wellness/HR/education → Calm Minimal or Wellness Soft
   - Board/annual report → Executive Authority
   - Financial model/dashboard → Corporate Balanced (Metal accent for tables)
3. **Element weighting:** never let Fire exceed 15% of visual area; Water and
   Earth may each reach 40–50%; Wood 20–35%; Metal 20–40%.
4. **Brand precedence:** if an existing brand palette is provided, element
   palettes must harmonize with it — use element colors only as accents.
5. **Fallback rule:** if the user declines or the deliverable is regulated
   (legal filings, audited financials), use the non-Feng-Shui neutral palette.
6. **Accessibility override:** any element palette that fails WCAG contrast
   minimums is adjusted — accessibility always wins over aesthetic intent.

## Input Requirements

```json
{
  "deliverable_type": "docx|xlsx|pptx|pdf",
  "purpose": "proposal|contract|sop|report|deck|dashboard|email",
  "audience": "executive|board|client|internal|students|patients",
  "mode": "corporate_balanced|creative_bold|calm_minimal|executive_authority|wellness_soft|auto",
  "existing_brand_palette": ["#hex", "..."],
  "page_or_slide_count": 12,
  "element_emphasis": "balanced|career|wealth|health|relationships|creativity|knowledge|support",
  "opt_out": false
}
```

All fields optional except `deliverable_type`. When `mode` is `auto`, select
per the decision rules above.

## Output Specification

The styling engine returns a JSON palette spec consumed by the document
generators:

```json
{
  "mode": "corporate_balanced",
  "framing_disclosure": "Element names are metaphorical design labels, not predictions.",
  "primary_element": "earth",
  "accent_element": "water",
  "palette": {
    "primary": "#5C4A32",
    "secondary": "#B08968",
    "accent": "#2E86AB",
    "background": "#F2E9DC",
    "surface": "#FFFFFF",
    "text": "#2B2F36",
    "text_muted": "#6B7280"
  },
  "named_colors": {
    "primary": "Umber",
    "secondary": "Clay",
    "accent": "Wave",
    "background": "Bone"
  },
  "texture_cues": [
    {"zone": "header", "cue": "solid_fill", "color": "#5C4A32"},
    {"zone": "table_header", "cue": "hairline_rule", "color": "#B08968"}
  ],
  "layout_guidance": {
    "header_zone_element": "water",
    "footer_zone_element": "fire",
    "dominant_center": "earth"
  },
  "contrast_report": {
    "text_on_background": "12.4:1",
    "wcag_pass": true
  },
  "alternative_neutral": {
    "note": "Standard brand-neutral palette, no element theming",
    "palette": {"primary": "#1F2937", "accent": "#2563EB", "background": "#FFFFFF", "text": "#111827"}
  }
}
```

## Quality Standards

- Every palette must pass WCAG AA contrast for body text (4.5:1) and large
  text (3:1); report the measured ratio.
- Hex values must be valid sRGB; named colors must match a fixed dictionary
  per element (never invented per call).
- Fire element area never exceeds 15% in applied styles.
- Every themed deliverable includes the disclosure string in metadata or a
  footer note when a "style credits" line exists.
- The `alternative_neutral` block is mandatory in every output.
- No element name may appear in document body copy as a claim about the
  recipient (e.g., never "this document attracts wealth").

## Error Handling

| Condition | Behavior |
|---|---|
| User requests bazi/horoscope analysis | Decline politely; state scope is visual styling only; offer element-inspired palette instead |
| Requested colors fail contrast | Auto-adjust toward neutral; report adjustment; do not silently ship failing palette |
| Existing brand palette conflicts | Harmonize: element colors become accents only; never override brand |
| Deliverable is regulated/legal | Default to Corporate Balanced or neutral; require explicit user opt-in for themed styling |
| Unknown deliverable type | Fall back to Corporate Balanced; log mode inference |

## Practical Examples

**Example 1 — Sales proposal deck (Creative Bold):**
Input: `{"deliverable_type":"pptx","purpose":"deck","audience":"client","mode":"auto"}`
Output: Wood-dominant greens `#2E5941`/`#4A7C59`, Fire accent `#D96C3D` on
section dividers only, `#F4D35E` for KPI highlights, `#EAF4F8` backgrounds.
Alternative neutral: standard navy/gray.

**Example 2 — Employee wellness handbook (Calm Minimal):**
Input: `{"deliverable_type":"docx","purpose":"sop","audience":"internal","mode":"wellness_soft"}`
Output: Water-soft `#16425B` headings, `#A9D6E5` callout fills, Earth `#B08968`
sub-accents, `#F9FAFB` page background. Rounded table corners in rendering.

**Example 3 — Regulated contract (opt-out path):**
Input: `{"deliverable_type":"docx","purpose":"contract","element_emphasis":"wealth"}`
System detects legal/regulatory context → outputs Corporate Balanced with
Metal accent only, disclosure appended, neutral alternative emphasized.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
