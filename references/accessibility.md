# Document Accessibility — WCAG-Oriented Standards

## Purpose

Ensure every document, spreadsheet, presentation, and PDF produced by
FileCraftBooster meets WCAG 2.1 accessibility standards so content is usable
by people with disabilities and compatible with assistive technologies
(screen readers, refreshable Braille, magnifiers, switch devices).

This applies to all output formats: Word, Excel, PowerPoint, PDF, and email.

## Core Principles (WCAG POUR)

- **Perceivable:** information presentable in ways users can perceive (alt
  text, contrast, captions).
- **Operable:** components operable via keyboard, no traps.
- **Understandable:** clear language, predictable behavior.
- **Robust:** works with current and future assistive tech (semantic markup,
  tagged PDFs).

## Structure and Headings

### Heading Hierarchy

- Use real heading styles (Heading 1–6), never bold text styled as headings.
- Never skip levels: H1 → H2 → H3 valid; H1 → H3 invalid.
- One H1 per document section or slide deck (title slide counts as H1).
- Heading text must describe content, not be generic ("Section 1" is poor;
  "Financial Performance Q3" is good).

### Lists

- Use real list formatting, not manual characters ("•", "1.") typed at line
  start.
- Nested lists use proper indent levels; don't fake nesting with spaces.
- Multi-level numbered lists use auto-numbering so screen readers announce
  correct structure.

### Tables vs Layout

- **Data tables:** real table objects with header rows marked.
- **Layout tables:** avoid entirely; use text boxes or columns instead.
  Screen readers read table cells linearly, destroying layout-only tables.
- Simple structure preferred: no merged cells, split cells, or nested tables
  in data tables.

## Alt Text Rules

### When Alt Text Is Required

- **Informative images:** photos, diagrams, charts, screenshots — describe
  what the image conveys.
- **Functional images:** icons acting as buttons/links — describe the action
  ("Search button").
- **Complex images:** charts and graphs — describe the data trend and key
  values, not just "chart."

### When Alt Text Should Be Empty/Decorative

- **Decorative images:** borders, background patterns, stock photos used
  purely for visual interest — mark as decorative (empty alt text or
  "decorative" role). Screen readers skip these, reducing noise.

### Writing Alt Text

- Be concise: under 125 characters for simple images; complex images may
  need 1–2 sentences.
- Describe content and function, not appearance: "Bar chart showing revenue
  growth from $1.2M to $2.4M over four quarters" not "Blue and green bar
  chart."
- For charts: include chart type, what is measured, key values, and trend.
- Never start with "Image of" or "Picture of" — screen readers already
  announce the element type.
- Don't include "alt text" or "description" as literal words in the alt text.

### Per-App Implementation

- **Word:** right-click image → Edit Alt Text.
- **PowerPoint:** right-click image → Edit Alt Text; check "Mark as
  decorative" for decorative images.
- **Excel:** right-click chart/image → Format → Alt Text; or use the
  Accessibility Checker.
- **PDF:** tagged PDF structure carries alt text; ensure source document
  has it before export.

## Color Independence

### Never Use Color Alone

- **Do not** convey meaning solely through color: "red items are overdue,
  green items are on track" fails for color-blind users.
- Always pair color with a secondary cue: shape, icon, pattern, text label,
  or position.
- Acceptable pairs: Red + "OVERDUE" text or ⚠ icon; Green + ✓ or "Complete";
  Blue + underline or bold for links.

### Charts and Graphs

- Use patterns, shapes, or direct labels in addition to color for data
  series.
- Line charts: vary line style (solid, dashed, dotted) in addition to color.
- Bar charts: use patterns or labels, not just color fills.
- Pie charts: label slices directly; avoid relying on legend color matching.

### Status Indicators

- Status badges must include text: "Approved," "Pending," "Rejected" — not
  just colored dots.
- Traffic-light indicators (red/yellow/green) need text equivalents.

## Contrast Minimums (WCAG AA)

| Element | Minimum Ratio | Notes |
|---|---|---|
| Normal text (<18pt or <14pt bold) | 4.5:1 | Body text, captions, labels |
| Large text (≥18pt or ≥14pt bold) | 3:1 | Headings, titles, slide text |
| UI components and graphical objects | 3:1 | Buttons, form borders, chart elements |
| Focus indicators | 3:1 | Visible focus rings for keyboard nav |

### Measuring Contrast

- Use the contrast ratio formula: `(L1 + 0.05) / (L2 + 0.05)` where L1 is the
  lighter relative luminance.
- FileCraftBooster QA automatically checks generated palettes against these
  thresholds; failing combinations are auto-adjusted or flagged.

### Practical Rules

- Black text on white: 21:1 (excellent).
- Dark gray `#333` on white: ~12:1 (good).
- Medium gray `#767676` on white: ~4.5:1 (minimum pass for normal text).
- Light gray `#999` on white: ~2.8:1 (fails for normal text; OK for large
  text only).
- White text on colored backgrounds: verify the background color is dark
  enough; when in doubt, use dark text on light backgrounds.

## Reading Order

- Content must be readable in a logical sequence when extracted from visual
  layout.
- Screen readers process content in document order (Word), reading order
  pane (PowerPoint), or tagged structure (PDF).
- Avoid body text in text boxes or floating shapes — they break reading
  order. If callouts are necessary, keep them in the logical flow.
- **PowerPoint:** use the Reading Order pane (Home → Arrange → Selection
  Pane → Reading Order); drag objects into correct sequence; titles first.
- In Word, use proper columns (Layout → Columns), not tables or text boxes;
  screen readers read column 1 top-to-bottom then column 2.

## Tables

- **Header row:** mark the first row as a header row (Table Design → Header
  Row in Word; Table Tools in PowerPoint).
- **Simple structure:** avoid merged cells, split cells, nested tables, and
  blank cells used for spacing.
- **Captions:** add a caption ("Table 3-1: Revenue by Quarter") above or
  below the table for context.
- **Data tables vs layout tables:** data tables are real table objects —
  accessible; layout tables are borderless positioning grids — not
  accessible, screen readers read cells as data producing gibberish.
- **Complex tables:** if merged cells are genuinely needed (grouped
  headers), provide a simplified alternative table or text description;
  screen readers may not correctly associate merged headers with data.

## Links

### Meaningful Link Text

- **Never** use "click here," "read more," "link," or "this" as link text.
- Link text must describe the destination: "Download the Q3 financial
  report" not "Click here to download."
- Screen reader users often navigate by links list; meaningful text lets
  them choose without reading surrounding context.

### Link Behavior

- External links should open in a new window/tab when appropriate (warn
  user if leaving the document).
- Internal links (TOC, cross-references) should navigate within the
  document.
- Avoid links that rely on color alone; use underline + color.

## Language

- Set the document language in file properties or markup: Word (Review →
  Language → Set Proofing Language), PowerPoint (File → Options →
  Language), PDF (Document Properties → Language). Language tag enables
  screen readers to use correct pronunciation and accent.
- For multilingual documents, tag language changes within the document.
- Use clear, concise language; avoid jargon without explanation.
- Define acronyms on first use: "Key Performance Indicator (KPI)."
- Use active voice where possible; keep sentences under ~25 words average.

## Font Size Floors

| Context | Minimum Size | Notes |
|---|---|---|
| Print documents | 10pt body, 12pt recommended | Footnotes may go to 9pt |
| Slide titles | 18pt minimum, 24–32pt preferred | Readable from back of room |
| Slide body text | 18pt minimum, 20–24pt preferred | Dense slides reduce comprehension |
| Excel data cells | 10pt minimum | Headers may be 11–12pt bold |
| Captions/footnotes | 9pt minimum | Never below 9pt |

- Sans-serif fonts (Calibri, Arial, Helvetica) are more readable on screens.
- Serif fonts (Times New Roman, Georgia) are fine for print body text.
- Avoid decorative or script fonts for body text.
- Ensure fonts are embedded or have safe fallbacks for PDF export.

## Screen Reader Testing Checklist

Before delivery, verify with a screen reader (NVDA, JAWS, VoiceOver):

- [ ] Document opens and reads in logical order
- [ ] Headings announced correctly with level numbers
- [ ] Lists announced as lists with item counts
- [ ] Tables read with headers and cell positions
- [ ] Images have appropriate alt text (or skipped if decorative)
- [ ] Links announced with meaningful text
- [ ] No content trapped in unreadable order
- [ ] Form fields have labels
- [ ] Language changes announced correctly
- [ ] No keyboard traps (can Tab through all interactive elements)

## Tagged PDF Export Notes

- **Create tagged PDFs:** File → Save As → PDF → Options → "Document
  structure tags for accessibility" (enabled by default in Word, PowerPoint,
  Excel).
- **Tags carry:** heading structure (H1–H6), alt text on images, table
  headers and cell associations, reading order, language tags, link
  annotations.
- **Verify:** open in Adobe Acrobat → Tools → Accessibility → "Check
  Accessibility" or use PAC (PDF Accessibility Checker); verify reading order
  in Acrobat's Reading Order tool; test with screen reader on exported PDF.

## Per-App Checklists

### Word (.docx)

- [ ] Heading styles used (not manual formatting)
- [ ] No skipped heading levels
- [ ] Real lists, not manual bullets/numbers
- [ ] Tables have header rows marked
- [ ] Images have alt text (informative) or marked decorative
- [ ] Links have meaningful text
- [ ] Language set in proofing settings
- [ ] Font sizes meet minimums
- [ ] No text in text boxes for body content
- [ ] TOC uses heading styles for page numbers
- [ ] Document title set in properties

### Excel (.xlsx)

- [ ] Sheet names are meaningful and unique
- [ ] No merged cells in data ranges (headers may be merged only if not in
  data rows)
- [ ] Charts have alt text describing data
- [ ] Images have alt text
- [ ] Color is not sole data indicator (use patterns/labels)
- [ ] Column headers are text, not just formatting
- [ ] Frozen panes and filters don't hide content from screen readers
- [ ] Formulas have clear precedent chains
- [ ] Hidden sheets documented if intentional
- [ ] Workbook has a summary/instructions sheet first

### PowerPoint (.pptx)

- [ ] Every slide has a unique, descriptive title
- [ ] Slide titles use Title placeholder (not text boxes)
- [ ] Reading order pane reviewed and corrected
- [ ] Images have alt text or marked decorative
- [ ] Charts have alt text with data description
- [ ] Color not sole indicator (patterns/labels backup)
- [ ] Font sizes meet minimums (18pt+ body, 24pt+ titles)
- [ ] No text overflow beyond slide bounds
- [ ] Speaker notes present for complex slides
- [ ] Slide numbers present
- [ ] Transitions don't auto-advance unexpectedly
- [ ] Final slide has contact/next steps

### PDF

- [ ] Tagged PDF structure present (not just visual PDF)
- [ ] Heading structure preserved from source
- [ ] Alt text carried through from source document
- [ ] Table headers tagged correctly
- [ ] Reading order logical
- [ ] Language tag set in document properties
- [ ] Fonts embedded
- [ ] Links functional and annotated
- [ ] No content in image-only pages without OCR/text layer

### Outlook (.eml)

- [ ] Subject line descriptive (not just "Hi" or "Document")
- [ ] Body uses headings or bold for structure
- [ ] Links have meaningful text
- [ ] Images have alt text (if HTML email)
- [ ] Color contrast adequate
- [ ] Plain-text version available (for accessibility)
- [ ] Attachments named meaningfully

## Error Handling

| Condition | Behavior |
|---|---|
| Alt text missing on informative image | Flag in QA L5; auto-generate draft alt text from image context if possible; require human review |
| Heading level skip detected | Flag in QA L5; auto-fix by promoting/demoting if unambiguous; else flag for manual fix |
| Contrast fails | Auto-adjust color toward neutral; report adjusted values; never ship failing contrast silently |
| Color-only meaning detected | Flag in QA L5; suggest adding text labels or patterns; require human confirmation for auto-fix |
| Reading order incorrect | Flag in QA L5; provide instructions for manual correction in PowerPoint Reading Order pane |
| Tagged PDF missing | Re-export with tags enabled; verify in Acrobat accessibility checker |
| Screen reader test fails | Report specific failure; provide remediation steps; block delivery if blocker severity |

## Practical Examples

### Example 1 — Accessible Chart

**Bad:**
```
[Bar chart: blue bars for Q1-Q4, no labels, legend says "Revenue"]
```

**Good:**
```
Bar chart titled "Quarterly Revenue 2026" showing revenue growth:
Q1 $1.2M, Q2 $1.5M, Q3 $1.8M, Q4 $2.1M.
Trend: consistent 25% quarter-over-quarter growth.
Alt text: "Bar chart showing quarterly revenue increasing from $1.2M in Q1
to $2.1M in Q4 2026, with each quarter growing approximately 25%."
```

### Example 2 — Accessible Table

**Bad:**
```
[Borderless 3-column layout: Name | Role | Email, but no header row marked,
merged cells for department groups]
```

**Good:**
```
Table 4-1: Team Contacts
| Name | Role | Email |
|------|------|-------|
| Alice | Manager | alice@co.com |
| Bob | Developer | bob@co.com |

Header row marked. No merged cells. Caption above table.
Alt text (if exported as image): "Table listing team members with their
names, roles, and email addresses."
```

### Example 3 — Color + Text Status

**Bad:**
```
[Red dot] Overdue    [Green dot] On Track    [Yellow dot] At Risk
```

**Good:**
```
[Red dot + "OVERDUE" text]    [Green dot + "ON TRACK" text]    [Yellow dot + "AT RISK" text]

Color is supplementary; text carries the meaning for color-blind users.
```

### Example 4 — Meaningful Link

**Bad:**
```
For more details, click here.
```

**Good:**
```
See the Q3 Financial Report for detailed revenue breakdown.
```

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
