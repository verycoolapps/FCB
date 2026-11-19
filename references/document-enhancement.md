# Document Enhancement Pipeline

## Purpose

This document defines the enhancement pipeline for existing Office files:
take a document the user already has, analyze it, choose a strategy, apply
changes safely, validate the result, and report exactly what changed. The
pipeline exists because most real-world files are messy — inconsistent
styles, stale content, missing accessibility structure, off-brand colors —
and users want improvement without losing data.

The hard rule: **never delete important data, formulas, or content without
explicit user approval.** Any destructive operation produces a change plan
first and waits for confirmation.

## Scope

- DOCX (Word) — via `python-docx` / `docxtpl`
- XLSX (Excel) — via `openpyxl` (`keep_vba=True` when macros present)
- PPTX (PowerPoint) — via `python-pptx` / `pptxgenjs` for new decks
- PDF — text extraction via `pypdf` / `pdfplumber`; editing is limited

Out of scope: binary formats without library support (.doc, .xls, .ppt
legacy), encrypted/password-protected files (report and stop), and files
the user has not confirmed ownership of.

## Pipeline Overview

```
inspect → analyze → strategy → apply → validate → compare
   │          │         │        │         │         │
   │          │         │        │         │         └─ change manifest + diff report
   │          │         │        │         └─ re-open file, integrity check, rollback advice
   │          │         │        └─ modifications per approved plan
   │          │         └─ minimal-touch | restyle | rewrite | regenerate
   │          └─ structure map, style audit, content quality, a11y, brand
   └─ file identity, size, format version, corruption check
```

## Phase 1 — Inspect

Before touching anything, establish ground truth:

1. **File identity**: format, size, modified date, author metadata, whether
   the file is a zip container (docx/xlsx/pptx are ZIP+XML — a quick
   `zipfile.testzip()` equivalent catches corruption early).
2. **Content inventory**: page/slide/sheet count, word/row/shape counts,
   embedded objects (images, charts, OLE objects, macros).
3. **Protection state**: read-only flag, document protection, sheet
   protection, encrypted flag. If protected, report which parts are locked
   and which remain editable.
4. **Baseline copy**: create `<name>.backup-<timestamp>.<ext>` in the same
   directory (or a `backups/` subfolder). This is the rollback anchor —
   never skip it.

## Phase 2 — Analyze

Produce a structured analysis report. Six dimensions:

### 2.1 Structure map

- DOCX: heading hierarchy (H1–H6), section breaks, tables, lists, TOC
  presence, headers/footers, footnotes/endnotes.
- XLSX: sheet inventory, used ranges, merged cells, tables, named ranges,
  defined names, external links, data-validation rules, pivot tables.
- PPTX: slide count, layouts used, masters, placeholders vs. manual
  shapes, notes pages, embedded media.
- PDF: page count, extractable text vs. scanned (no text layer), form
  fields, bookmarks/outline.

### 2.2 Style audit

Compare observed formatting against the target design-system tokens (or a
sensible corporate default if none supplied):

- Fonts: family, size, weight per role (heading/body/caption).
- Colors: direct RGB vs. theme colors; flag off-palette values.
- Paragraph spacing: before/after, line spacing, indentation.
- Number formats: currency/date/percent consistency in spreadsheets.
- Theme drift: document theme colors vs. direct formatting overrides
  (direct formatting always wins visually — flag it).

### 2.3 Content quality

- Placeholders: `[TODO]`, `XXX`, `Lorem ipsum`, `{{merge_field}}` remnants.
- Typos: run a spelling pass; flag repeated errors.
- Inconsistencies: date formats (`01/02/2024` vs `2 Jan 2024`), capitalization
  of headings, unit usage (kg vs KG).
- Stale references: "updated last quarter" with no date, dead hyperlinks.

### 2.4 Accessibility gaps

- DOCX: missing heading styles (body text styled as bold instead of
  Heading 2), images without alt text, tables without header rows,
  insufficient color contrast.
- PPTX: reading-order issues, text in images only, low-contrast pairs.
- XLSX: sheets with no header row, color-only data encoding (needs a
  legend or conditional formatting instead).
- PDF: no tagged structure, no alt text, no bookmarks on long docs.

### 2.5 Brand compliance

- Logo presence/placement, brand color usage, font compliance, disclaimer
  and confidentiality footer presence.

### 2.6 Risk flags

- Macros (`.docm`, `.xlsm`, `.pptm`), external links, embedded OLE objects,
  content that looks confidential (SSN-like patterns, credential strings) —
  flag for user review before any cloud processing.

## Phase 3 — Strategy Selection

Choose one strategy; state it explicitly in the plan:

| Strategy | When | Risk |
|---|---|---|
| **Minimal-touch** | File is mostly good; fix typos, placeholder text, missing headers/footers, broken links | Lowest — style/structure untouched |
| **Style restyle** | Content is fine but formatting is inconsistent or off-brand | Medium — must preserve all content; verify no data loss in tables/fields |
| **Content rewrite** | Structure OK but prose needs restructuring/condensing | Higher — requires user review of rewritten text |
| **Full regeneration** | File is beyond repair (corrupt, legacy binary, scanned PDF with no source) | Highest — original preserved as reference; user must approve |

Selection rules:

- If formulas exist in XLSX → never choose full restyle without formula
  audit; prefer minimal-touch + targeted style fixes on non-formula cells.
- If file has tracked changes or comments → preserve them; never accept or
  reject changes silently.
- If content contains legal/financial figures → minimal-touch only unless
  user explicitly requests rewrite; show diff of every numeric change.
- If scanned PDF → cannot edit text; recommend regenerate-from-source or
  OCR+rebuild path.

## Phase 4 — Apply

### DOCX — python-docx / docxtpl

- Read-modify-write: `Document(path)` → modify → `save(path)`.
- Preserve styles: always apply named styles (`doc.styles['Heading 1']`)
  rather than direct formatting where possible; when direct formatting is
  required, log it in the manifest.
- Track changes: python-docx does not natively produce tracked changes;
  if the original has revisions, either preserve the `w:ins`/`w:del`
  markup untouched or warn that edits will not be tracked.
- docxtpl for template-driven generation: `{{placeholders}}` rendered via
  Jinja2 — safe for mail-merge style updates.
- Lists: use `style='List Bullet'`/`'List Number'` — never fake bullets
  with literal "•" characters.

### XLSX — openpyxl

- `load_workbook(path, keep_vba=True, data_only=False)` — `data_only=False`
  keeps formulas; `data_only=True` reads cached values (loses formulas —
  only use for inspection, never for saving).
- **Formula preservation**: never write a computed value over a formula
  cell. If a cell contains `=SUM(...)`, modifying it requires user approval.
- `keep_vba=True` is mandatory for `.xlsm`; without it macros are stripped.
- Charts, images, and conditional formatting survive openpyxl round-trips
  imperfectly — log any objects openpyxl cannot fully represent and warn.
- Defined names and data validation persist; verify after save.
- Merged cells: writing to a non-top-left cell of a merged range raises —
  handle explicitly.

### PPTX — python-pptx

- `Presentation(path)` → modify → `save(path)`.
- Layouts and masters are preserved on round-trip; python-pptx cannot
  create new slide masters — restyle via theme colors (`slide.slide_layout`)
  or direct shape formatting instead.
- Placeholder text vs. manual text boxes: prefer editing placeholder shapes
  (`shape.is_placeholder`) so layout inheritance keeps working.
- Grouped shapes: `shape.shape_type == MSO_SHAPE_TYPE.GROUP` requires
  iterating `shape.shapes`.

### PDF — pypdf / pdfplumber

- **Extraction only** by default: `pdfplumber` for text+tables,
  `pypdf` for page-level ops, merging, metadata.
- **Editing limitations**: pypdf can update metadata, merge/split pages,
  add annotations, fill simple AcroForm fields. It cannot reflow text,
  change fonts, or fix layout. For content changes, recommend regenerating
  from the source document (DOCX/PPTX) and re-exporting to PDF.
- Scanned PDFs have no text layer: detect via empty extraction → route to
  OCR path or request source file.

## Phase 5 — Validate

After every save:

1. **Re-open the file** with the same library and confirm it parses without
   error.
2. **Integrity spot-checks**:
   - DOCX: paragraph count, table count, heading count within ±0% of
     expected; confirm styles still resolve.
   - XLSX: confirm formula count unchanged (or matches approved changes);
     confirm sheet count and defined names intact.
   - PPTX: slide count unchanged unless slides were intentionally added;
     confirm masters present.
3. **Visual check when possible**: LibreOffice headless conversion to PDF
   (`soffice --headless --convert-to pdf`) for a render sanity check, or
   extract first-page text to confirm content order.
4. **Formula audit**: recount `=` formulas before and after; any delta
   must be explained in the manifest.

## Phase 6 — Compare & Report

Produce a **change manifest** — a structured list where every entry has:

- Location (file, sheet/slide/page, cell range or paragraph index)
- Change type (insert/delete/modify/format)
- Before value → after value (truncated for long text)
- Reason (which analysis finding it addresses)
- Risk level (safe / review / destructive-approved)

Plus a human-readable summary: strategy used, files touched, counts by
change type, and rollback instructions.

## Input Requirements

- Source file(s) — required.
- Enhancement goal — required ("corporate style", "fix typos", "modernize",
  or free text).
- Optional: brand spec (colors as hex, font names, logo path), target
  audience, compliance requirements (accessibility level, locale).
- For destructive changes: explicit user approval of the change plan.

## Output Specifications

- `<name>-enhanced.<ext>` — the enhanced file (original untouched).
- `<name>.backup-<timestamp>.<ext>` — pristine backup.
- `CHANGE-MANIFEST.md` or `.json` — every modification listed.
- `ENHANCEMENT-REPORT.md` — analysis findings, strategy rationale,
  validation results, rollback steps.

## Decision Rules

- File corrupt/unopenable → attempt repair (zipfile test → extract-rebuild
  → LibreOffice convert); if unrecoverable, report and request source.
- Password-protected → stop; report that decryption is out of scope.
- Formulas present + any change touches formula cells → require approval.
- Tracked changes/comments present → preserve markup; do not flatten.
- External links present → flag; do not fetch or update them silently.
- Macros present → `keep_vba=True`; never strip; warn if the save path
  would change `.xlsm` to `.xlsx`.
- PDF with no text layer → do not pretend to "edit" it; offer OCR rebuild
  or source-file regeneration.
- Multiple reasonable strategies → present options with risk ratings and
  let the user pick; default to minimal-touch.

## Quality Standards

- Backup created before every modification — non-negotiable.
- Every change traceable to a manifest entry — no silent edits.
- Validation must re-open the file; "saved without error" is not
  validation.
- Report must state what was NOT changed and why.

## Error Handling

- Library missing → install instructions per dependency
  (`pip install python-docx openpyxl python-pptx pypdf pdfplumber`).
- File locked/open in Office → detect permission error, ask user to close.
- Corrupt zip → `zipfile.testzip()` to locate bad member; attempt
  extract-and-rebuild; fall back to LibreOffice headless conversion.
- Encoding issues in extracted text → normalize UTF-8, strip BOM, report
  smart-quote/emdash corruption (see troubleshooting.md).
- Formula recalculation differences → openpyxl does not evaluate formulas;
  warn that cached values may be stale and Excel will recalc on open;
  offer LibreOffice headless recalc for verification.
- Partial failure mid-pipeline → leave original and backup untouched;
  write `FAILED-STATE.md` describing how far the pipeline got.

## Practical Examples

**Example 1 — plain Word report → corporate style:**
Inspect: 12 pages, no headings (all bold body text), Calibri 11, no header.
Analyze: map bold paragraphs to Heading styles by font size/position;
audit colors (all black — apply brand navy `#1F3864` for headings).
Strategy: style restyle + minimal-touch content (fix 3 typos found).
Apply: assign Heading 1–3 styles, add footer with page numbers and
confidentiality line, insert TOC field at top.
Validate: re-open, confirm 47 paragraphs restyled, TOC field present.
Manifest: 61 entries (47 style changes, 3 typo fixes, 4 header/footer,
TOC insert, page-number fields).

**Example 2 — modernize an old Excel financial model:**
Inspect: `.xls` legacy or `.xlsx` with mixed formatting, no tables.
Analyze: 8 sheets, 3,400 formulas, defined names `Revenue_FY`, hardcoded
print area, off-palette fills.
Strategy: minimal-touch — convert data ranges to Excel Tables (preserves
formulas), apply number-format consistency, add freeze panes; NO formula
edits.
Validate: formula count identical (3,400 → 3,400); table objects added.
Manifest: format-only changes; explicit note "no formulas modified."

**Example 3 — rebrand a PPT deck:**
Inspect: 24 slides, 2 masters, mixed layouts, company-old colors.
Analyze: map old palette `#003366`/`#CCCCCC` → new `#0A2540`/`#F6F9FC`;
fonts Arial → brand font; 6 slides use manual text boxes instead of
placeholders.
Strategy: style restyle; where placeholders absent, apply direct
formatting and log it.
Validate: slide count 24 → 24; all masters intact; render 3 sample slides
to PDF for visual check.
Manifest: theme color swaps, font changes per shape, flagged 6 manual
text boxes needing manual layout review.

**Example 4 — PDF contract cleanup:**
Inspect: 14-page PDF, extractable text, no form fields.
Analyze: inconsistent date formats, missing signature block labels,
scanned annex pages 12–14 (no text).
Strategy: cannot edit PDF directly → extract text → generate corrected
DOCX → user reviews → export to PDF. Report states clearly: "PDF edited
via source regeneration; original preserved."

## Rollback

Every run produces a timestamped backup. Rollback = copy backup over the
enhanced file. For partial rollback, the change manifest identifies which
entries to revert manually. Never delete backups automatically; advise
user retention for at least one release cycle.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
