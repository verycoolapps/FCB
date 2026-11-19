# FileCraftBooster — PowerPoint Engine Reference

**Document class:** Engine technical reference
**Audience:** Engineers and reviewers implementing or auditing PPTX generation
**Version:** 1.0
**Primary libraries:** `python-pptx`, `PptxGenJS`

---

## 1. Purpose

The PowerPoint engine produces and enhances `.pptx` artifacts: board decks, training decks, sales pitches, status updates, and branded presentations. It is the reference implementation for all presentation-format output in FileCraftBooster.

---

## 2. Scope

Covers: library selection (`python-pptx` vs `PptxGenJS`), slide storytelling structure, layouts and masters, text frames and placeholders, SmartArt-equivalent diagrams, native charts, speaker notes, transitions and animations, design principles, corporate template compliance, input/output specs, error handling, and worked examples.

Out of scope: `.pps` (slide show binary), `.potx` template generation (FileCraftBooster produces `.pptx` that can be saved as template), real-time collaboration features.

---

## 3. Capabilities

| Capability | Implementation path | Notes |
|---|---|---|
| Presentation creation from scratch | `python-pptx` / `PptxGenJS` | Full control over slides, shapes, text |
| Template-based generation | `python-pptx` (open template) / `PptxGenJS` (layout definitions) | Use corporate `.pptx` or `.potx` as base |
| Slide layouts | `python-pptx` `slide_layouts` / `PptxGenJS` `layout` | Title, content, section, blank |
| Text frames and placeholders | Both libraries | Bullets, multi-level, rich text |
| Shapes and diagrams | `python-pptx` `shapes` / `PptxGenJS` `shape` | Rectangles, arrows, chevrons, connectors |
| SmartArt-equivalent | Manual shape composition | Process flows, cycles, hierarchies via shapes |
| Native charts | `python-pptx` `add_chart` / `PptxGenJS` `addChart` | Column, line, pie, bar, area, scatter |
| Speaker notes | `python-pptx` `notes_slide` / `PptxGenJS` `addNotes` | Per-slide presenter notes |
| Transitions | `python-pptx` `slide.transition` / `PptxGenJS` `transition` | Fade, push, wipe, morph (limited) |
| Animations | Raw OOXML (`p:timing`) | Minimal; professional decks rarely need complex animations |
| Image embedding | Both libraries | PNG, JPEG, SVG (limited SVG support) |
| Table insertion | Both libraries | Native PowerPoint tables |
| Video/audio embedding | `python-pptx` (limited) | File path or URL reference |

---

## 4. Detailed Procedures

### 4.1 Library selection decision rule

| Scenario | Library | Rationale |
|---|---|---|
| Python-based pipeline | `python-pptx` | Native Python integration, easier scripting |
| Node.js/web-based pipeline | `PptxGenJS` | JavaScript/TypeScript, browser-compatible |
| Need complex charts | `python-pptx` | Better chart API, more chart types |
| Need HTML-to-slide conversion | `PptxGenJS` | Supports rich text HTML in text frames |
| Need template preservation | `python-pptx` | Opens existing `.pptx`/`.potx`, preserves masters |
| Need rapid prototyping | `PptxGenJS` | Concise API, fewer lines for simple decks |

### 4.2 Slide storytelling structure

**Standard deck arc:**

1. **Title slide** — Deck title, subtitle, date, presenter/company.
2. **Agenda / Contents** — Bullet list of sections (optional for short decks).
3. **Section dividers** — One slide per major section with section title.
4. **Content slides** — One idea per slide; mix of text, data, visuals.
5. **Data slides** — Charts, tables, key metrics.
6. **Closing slide** — Summary, next steps, Q&A, contact info.

**Storytelling rules:**

- **One idea per slide.** If a slide has two ideas, split it.
- **6×6 rule.** Max 6 bullets per slide, max 6 words per bullet (guideline, not absolute).
- **Assertion titles.** Slide titles should state the takeaway, not just the topic. Bad: "Market Analysis". Good: "Market grew 23% driven by enterprise segment".
- **Visual hierarchy.** Most important element largest/most prominent.
- **Whitespace.** Don't fill every pixel; breathing room aids comprehension.

### 4.3 Layouts and masters

**Built-in layouts (python-pptx slide_layouts indices):** 0 Title Slide; 1 Title and Content; 2 Section Header; 3 Two Content; 4 Comparison; 5 Title Only; 6 Blank; 7 Content with Caption; 8 Picture with Caption; 9 Title and Vertical Text; 10 Vertical Title and Text.

**Corporate template compliance:**

- Open template `.pptx` or `.potx` as base via `Presentation('corporate_template.pptx')`.
- Use template's slide masters and layouts; apply its color scheme, fonts, and logo.
- DO NOT override template styles unless explicitly requested.
- Placeholders auto-populate from layout definitions.

```python
prs = Presentation('corporate_template.pptx')
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)
prs.save('output.pptx')
```

### 4.4 Text frames and placeholders

**Text frame properties:** `word_wrap=True`; `auto_size` (`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`/`SHAPE_TO_FIT_TEXT`); `margin_left/right/top/bottom` for internal padding; `vertical_anchor` (`MSO_ANCHOR.TOP`/`MIDDLE`/`BOTTOM`).

```python
text_frame = shape.text_frame
text_frame.text = "First level bullet"
p = text_frame.add_paragraph()
p.text = "Second level bullet"
p.level = 1  # Indent level (0-8)
p.font.size = Pt(18)

run = p.add_run()
run.text = "Bold text"
run.font.bold = True
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

**Font floors:** minimum 18pt body, 24pt titles, 14pt footnotes/captions. NEVER below 12pt.

### 4.5 SmartArt-equivalent diagrams

PowerPoint's SmartArt is a proprietary format; FileCraftBooster builds equivalent diagrams from native shapes.

**Process flow (chevron chain):**

```python
from pptx.enum.shapes import MSO_SHAPE
steps = ["Discover", "Design", "Build", "Deploy", "Measure"]
for i, step in enumerate(steps):
    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(0.5) + Inches(1.6) * i, Inches(3), Inches(2), Inches(1))
    shape.text_frame.text = step
    shape.text_frame.paragraphs[0].font.size = Pt(16)
    shape.text_frame.paragraphs[0].font.bold = True
```

**Hierarchy (org chart):** top box = CEO/Manager; middle row = department heads; bottom row = team members; connect with lines/arrows from parent to children.

**Cycle:** arrange shapes in a circle via trigonometry; add arrows between shapes to show flow.

**Matrix (2×2):** four rectangles in a grid; label axes (e.g., "High/Low Impact" × "High/Low Effort").

### 4.6 Native charts

**Chart types (`XL_CHART_TYPE` / PptxGenJS `ChartType`):** `COLUMN_CLUSTERED`/`bar` (comparisons/rankings), `LINE`/`line` (trends), `PIE`/`pie` (part-to-whole, max 5 slices), `AREA`/`area` (cumulative), `XY_SCATTER`/`scatter` (correlations), `RADAR`/`radar` (multi-axis), `DOUGHNUT`/`doughnut` (center text).

```python
from pptx.chart.data import CategoryChartData
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (100, 120, 150, 180))
chart_data.add_series('Expenses', (80, 90, 110, 130))
chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(2), Inches(8), Inches(4), chart_data)
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
```

```javascript
slide.addChart(pptx.ChartType.bar, [
    { name: 'Revenue', labels: ['Q1','Q2','Q3','Q4'], values: [100,120,150,180] },
    { name: 'Expenses', labels: ['Q1','Q2','Q3','Q4'], values: [80,90,110,130] },
], { x: 1, y: 2, w: 8, h: 4, showLegend: true });
```

### 4.7 Speaker notes

```python
notes_slide = slide.notes_slide
notes_slide.notes_text_frame.text = "Emphasize enterprise growth; mention churn reduction initiative."
```

```javascript
slide.addNotes('Emphasize enterprise growth; mention churn reduction initiative.');
```

Best practices: talking points, not full script; include data sources, caveats, anticipated questions; under 200 words per slide.

### 4.8 Transitions and animations

| Type | `python-pptx` | `PptxGenJS` | Use case |
|---|---|---|---|
| Fade | `PP_TRANSITION_TYPE.FADE` | `transition: { type: 'fade' }` | Default, professional |
| Push | `PP_TRANSITION_TYPE.PUSH` | `transition: { type: 'push' }` | Directional emphasis |
| Wipe | `PP_TRANSITION_TYPE.WIPE` | `transition: { type: 'wipe' }` | Section changes |
| Morph | Not supported | `transition: { type: 'morph' }` | Requires PowerPoint 2019+ |
| None | `PP_TRANSITION_TYPE.NONE` | `transition: { type: 'none' }` | Minimalist |

`python-pptx` has no native animation API (raw OOXML `p:timing` required); `PptxGenJS` does not support animations. Keep animations minimal or none — professional decks rely on content, not effects. NEVER use more than one transition type per deck.


### 4.9 Design principles

- **One idea per slide:** title states the takeaway; body supports with evidence; visual reinforces the message.
- **6×6 rule (guideline):** max 6 bullets, max 6 words per bullet; data-dense slides may exceed.
- **Contrast:** dark text on light background (or vice versa); minimum 4.5:1 contrast (WCAG AA); avoid red/green (colorblind unsafe); test on projectors.
- **Safe margins:** minimum 0.5" (1.27 cm) from all edges; account for projector overscan; keep critical content within central 90%.
- **Font floors:** titles 28–40pt; body 18–24pt; footnotes/captions 14pt minimum; NEVER below 12pt.
- **Aspect ratio:** default 16:9 (13.33" × 7.5"); fallback 4:3 (10" × 7.5") if template requires; NEVER mix ratios within a deck.

### 4.10 Corporate template compliance

Checklist: open correct template (`.pptx`/`.potx`); use its slide masters/layouts; apply its color scheme and fonts; place logo in correct position; follow naming conventions; respect footer/page-number placement; do not modify hidden slides/layouts. If template constraints conflict with content requirements, flag to user and propose options (e.g., use blank layout for extra sections or modify template).

---

## 5. Input Requirements

```yaml
powerpoint_engine_input:
  brief: string              # What the deck is about
  audience: string           # Who will see it
  purpose: board | training | sales | status | pitch | other
  slide_count: int           # Target number of slides (5-50 typical)
  tone: formal | casual | persuasive | technical
  template_path: string | null  # Optional .pptx/.potx template
  brand_tokens: {palette: {...}, typography: {...}, logo_ref: string | null}
  data: object | null        # Charts, tables, key metrics
  speaker_notes_required: bool
  aspect_ratio: 16:9 | 4:3
  accessibility_profile: {require_alt_text: bool, require_reading_order: bool}
```

**Validation rules:**

- `brief` MUST be non-empty and ≥ 20 characters.
- `audience` MUST be specified.
- `slide_count` MUST be reasonable (5–50 for typical decks; >50 requires chunking).
- `purpose` MUST map to structure template (board deck ≠ training deck).
- If `template_path` provided, MUST validate it opens and has expected masters/layouts.
- `aspect_ratio` MUST match template if provided; conflict → flag to user.

---

## 6. Output Specifications

```yaml
powerpoint_engine_output:
  artifact_path: string      # .pptx file path
  manifest:
    engine: "powerpoint-engine"
    engine_version: "1.0"
    library_used: string      # "python-pptx" | "pptxgenjs"
    slide_count: int
    slides: [{index, layout, title, has_notes, has_chart, has_table, has_image}]
    aspect_ratio: "16:9" | "4:3"
    transitions_used: [string]
    animations_used: [string]
    brand_tokens_applied: [string]
    template_used: string | null
    accessibility_checks: {alt_text: pass|fail|n/a, reading_order: pass|fail|n/a, font_size_min: int, contrast_ratio: pass|fail|n/a}
    license_register_entries: [string]
    limitations: [string]
```

**File constraints:**

- `.pptx` MUST be valid ZIP with `ppt/presentation.xml`, `ppt/slides/slide*.xml`, `ppt/slideMasters/slideMaster*.xml`.
- All XML MUST be well-formed; namespaces MUST be declared.
- File size SHOULD be < 100 MB; larger requires media compression.
- Aspect ratio MUST be consistent throughout.

---

## 7. Decision Rules

| Scenario | Decision |
|---|---|
| Python-based pipeline | `python-pptx` |
| Node.js/web-based pipeline | `PptxGenJS` |
| Need complex charts | `python-pptx` |
| Need HTML formatting in text | `PptxGenJS` |
| Need template preservation | `python-pptx` (open existing) |
| Need rapid prototyping | `PptxGenJS` |
| Need SmartArt | Build from shapes (both libraries) |
| Need animations | Raw OOXML (python-pptx) or skip (PptxGenJS) |
| Need morph transition | `PptxGenJS` only (PowerPoint 2019+) |
| Template conflict | Flag to user; propose options |
| Aspect ratio mismatch | Use template's ratio; warn if user requested different |

---

## 8. Quality Standards

- **Structure:** Follow storytelling arc; one idea per slide.
- **Titles:** Assertion titles (takeaway, not topic).
- **Text:** Max 6 bullets, max 6 words per bullet (guideline).
- **Fonts:** Minimum 18pt body, 24pt titles, 14pt footnotes.
- **Colors:** Brand palette; sufficient contrast; avoid red/green.
- **Margins:** ≥ 0.5" from edges; critical content in central 90%.
- **Charts:** Labeled axes, clear titles, max 4 series.
- **Transitions:** One type per deck; professional (fade default).
- **Animations:** Minimal or none.
- **Speaker notes:** Present on content slides; concise talking points.
- **Template:** Respected unless explicitly overridden.
- **Manifest:** Every output MUST include slide inventory and accessibility status.

---

## 9. Error Handling

| Error | Detection | Recovery |
|---|---|---|
| Corrupt `.pptx` | `zipfile.BadZipFile` or `pptx` exception | Attempt repair: extract `ppt/presentation.xml`, rebuild minimal package; if fails, request clean copy |
| Template not found | `FileNotFoundError` | Use default blank template; warn user |
| Layout index out of range | `IndexError` | Fall back to blank layout; log warning |
| Font not available | Runtime warning | Fallback to `Calibri` or `Arial`; note in manifest |
| Image file not found | `FileNotFoundError` | Skip image, log warning, continue |
| Chart data mismatch | Series/category length mismatch | Validate data before chart creation; truncate or pad |
| Aspect ratio conflict | Template vs user request | Use template's ratio; warn user |
| File too large | Memory error | Compress images; reduce slide count; split into multiple decks |
| Placeholder not found | `KeyError` on placeholder index | Use shape name or position fallback |
| Animation XML invalid | OOXML parse error | Skip animations; use transitions only |

---

## 10. Practical Examples

### Example A — Board deck (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Q3 2026 Board Review"
slide.placeholders[1].text = "Adhithya Soemitro | VeryCoolApps\nNovember 19, 2026"

slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Agenda"
slide.placeholders[1].text_frame.text = "1. Financial Performance\n2. Product Updates\n3. Strategic Initiatives\n4. Risks & Mitigations\n5. Q4 Outlook"

slide = prs.slides.add_slide(prs.slide_layouts[2])
slide.shapes.title.text = "1. Financial Performance"

slide = prs.slides.add_slide(prs.slide_layouts[5])
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
tf = title_box.text_frame
tf.text = "Revenue grew 23% YoY driven by enterprise segment"
tf.paragraphs[0].font.size = Pt(32); tf.paragraphs[0].font.bold = True

chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (4.2, 4.5, 5.1, 5.8))
chart_data.add_series('Target', (4.0, 4.5, 5.0, 5.5))
chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(1.5), Inches(11), Inches(5), chart_data)

notes = slide.notes_slide
notes.notes_text_frame.text = "Highlight Q3 beat; mention enterprise win with PT Maju Jaya."

slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Thank You"
slide.placeholders[1].text = "Questions?\nadhithya@vcadeveloper.com"

prs.save('board_deck_q3_2026.pptx')

### Example B — Training deck (PptxGenJS)

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

pptx.defineLayout({ name: 'WIDE', width: 13.33, height: 7.5 });
pptx.layout = 'WIDE';

// Title
let slide = pptx.addSlide();
slide.addText('FileCraftBooster Training', { x: 1, y: 2, w: 11, h: 1.5, fontSize: 44, bold: true, align: 'center' });
slide.addText('Module 1: Document Generation', { x: 1, y: 3.5, w: 11, h: 0.8, fontSize: 24, align: 'center', color: '666666' });

// Content
slide = pptx.addSlide();
slide.addText('Key Concepts', { x: 0.5, y: 0.3, w: 12, h: 0.8, fontSize: 32, bold: true });
slide.addText([
    { text: '• Intent routing: classify request → select engine', options: { bullet: true, breakLine: true } },
    { text: '• Shared context: brand tokens, accessibility, license', options: { bullet: true, breakLine: true } },
    { text: '• Quality gates: QA, accessibility, security scans', options: { bullet: true, breakLine: true } },
    { text: '• Output: artifact + manifest + verification report', options: { bullet: true } },
], { x: 0.7, y: 1.5, w: 12, h: 5, fontSize: 20 });

// Chart slide
slide = pptx.addSlide();
slide.addText('Performance Metrics', { x: 0.5, y: 0.3, w: 12, h: 0.8, fontSize: 32, bold: true });
slide.addChart(pptx.ChartType.line, [
    { name: 'Speed', labels: ['Week 1','Week 2','Week 3','Week 4'], values: [10,15,22,30] },
    { name: 'Quality', labels: ['Week 1','Week 2','Week 3','Week 4'], values: [85,88,92,95] },
], { x: 1, y: 1.5, w: 11, h: 5, showLegend: true, chartColors: ['4472C4','ED7D31'] });
slide.addNotes('Show improvement trend; emphasize quality over speed.');

pptx.writeFile({ fileName: 'training_module1.pptx' });
```

### Example C — Sales pitch (python-pptx with template)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation('sales_template.pptx')

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "VeryCoolApps × PT Maju Jaya"
slide.placeholders[1].text = "Enterprise Productivity Suite Proposal\nAdhithya Soemitro | November 2026"

# Slide 2: Problem
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Your Team Spends 12 Hours/Week on Manual Documents"
content = slide.placeholders[1].text_frame
content.text = "• Manual report generation\n• Version control issues\n• Inconsistent branding\n• Accessibility compliance gaps"

# Slide 3: Solution
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "FileCraftBooster Automates 80% of Document Work"
content = slide.placeholders[1].text_frame
content.text = "• AI-powered document generation\n• Brand-consistent templates\n• Accessibility built-in\n• Multi-app workflows (Word, Excel, PowerPoint)"

# Slide 4: Pricing
slide = prs.slides.add_slide(prs.slide_layouts[5])
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1))
tf = title_box.text_frame
tf.text = "Investment: IDR 150M/year"
tf.paragraphs[0].font.size = Pt(32)
tf.paragraphs[0].font.bold = True

body_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
tf = body_box.text_frame
tf.text = "Includes:\n• Unlimited document generation\n• Priority support\n• Custom template development\n• Quarterly business reviews"
tf.paragraphs[0].font.size = Pt(20)

# Slide 5: Close
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Let's Build Together"
slide.placeholders[1].text = "Next Step: Technical deep-dive session\nContact: adhithya@vcadeveloper.com"

prs.save('sales_pitch_pt_maju_jaya.pptx')
```

---

## 11. Cross-References

- `architecture.md` — Shared context, orchestration rules
- `microsoft-ecosystem.md` — PowerPoint tier-1 capabilities and caveats
- `word-engine.md` — Embedding Word content in slides
- `excel-engine.md` — Linking workbook charts to slides

---

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
