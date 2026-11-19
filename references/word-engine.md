# FileCraftBooster — Word Engine Reference

**Document class:** Engine technical reference
**Audience:** Engineers and reviewers implementing or auditing DOCX generation
**Version:** 1.0
**Primary libraries:** `python-docx`, `docxtpl` (python-docx-template), raw OOXML

---

## 1. Purpose

The Word engine produces and enhances `.docx` artifacts: reports, memos, proposals, contracts, mail-merge letters, accessible documents, and tracked-changes-aware edits. It is the reference implementation for all document-format output in FileCraftBooster.

---

## 2. Scope

Covers: generation approaches (`python-docx` vs `docxtpl` vs raw OOXML), style systems, tables of contents, tables, headers/footers, footnotes, mail merge, tracked changes, accessibility, input/output specs, decision rules, error handling, and worked examples.

Out of scope: `.doc` (legacy binary), `.rtf` generation, PDF rendering (handled by `visual-assets` or external tools).

---

## 3. Capabilities

| Capability | Implementation path | Notes |
|---|---|---|
| Structured document generation | `python-docx` | Full control over styles, tables, headers |
| Template-based generation (mail merge) | `docxtpl` | Jinja2 placeholders inside a styled `.docx` template |
| Field injection (TOC, page numbers) | Raw OOXML / `python-docx` XML manipulation | Required for `TOC`, `PAGE`, `NUMPAGES` fields |
| Tracked-changes-aware editing | `python-docx` + OOXML `w:ins`/`w:del` | Preserves existing revision marks; adds new ones |
| Accessibility remediation | `python-docx` + OOXML | Heading order, alt text, table headers |
| Style system injection | `python-docx` `styles` API + OOXML `styles.xml` | Adds custom styles without breaking template |
| Header/footer fields | `python-docx` `section.header`/`footer` + OOXML | Page numbers, dates, document title |
| Footnotes/endnotes | Raw OOXML (`w:footnote`/`w:endnote` parts) | `python-docx` has limited native support |

---

## 4. Detailed Procedures

### 4.1 Choosing the generation approach

**Decision rule:**

- **Use `docxtpl` when** the document is a *template* with variable content (mail merge, contract from template, report with repeating sections). The user or a prior step provides a styled `.docx` with Jinja2 tags (`{{ client_name }}`, `{% for item in items %}`).
- **Use `python-docx` when** the document is *built from scratch* or requires programmatic control over every element (dynamic tables, conditional sections, complex headers).
- **Use raw OOXML when** `python-docx` cannot express the required structure (custom XML parts, complex field codes, `w:ins`/`w:del` revision marks, footnote part manipulation).

### 4.2 Style system

**Built-in styles (always available):**

| Style name | Purpose | OOXML style ID |
|---|---|---|
| `Title` / `Subtitle` | Document title / subtitle | `Title` / `Subtitle` |
| `Heading 1`–`Heading 9` | Section hierarchy | `Heading1`–`Heading9` |
| `Normal` | Body text | `Normal` |
| `List Bullet` / `List Number` | Lists | `ListBullet` / `ListNumber` |
| `Table Grid` | Bordered tables | `TableGrid` |
| `Footnote Text` / `Hyperlink` | Footnotes / links | `FootnoteText` / `Hyperlink` |
| `TOC Heading`, `TOC 1`–`TOC 9` | TOC title and levels | `TOCHeading`, `TOC1`–`TOC9` |

**Custom style injection procedure:**

1. Open template or create `Document()`.
2. Access `doc.styles` and add/modify `w:style` entries in `styles.xml`.
3. For each custom style, define: `w:name`, `w:basedOn` (parent style), `w:next` (next-paragraph style), `w:pPr` (paragraph properties), `w:rPr` (run properties).
4. Apply via `paragraph.style = doc.styles['CustomStyleName']`.

**Heading order rule (accessibility):** Never skip levels (H1 → H3 is invalid). Every document MUST start with `Title` or `Heading 1`, and subsequent headings MUST follow sequential order or return to a higher level.

### 4.3 Table of contents (TOC)

**Two approaches:**

**A. Field-based TOC (recommended for Word-native documents):**

Insert a `TOC` field code that Word populates on open or manual update. Canonical field structure: `w:fldChar begin` → `w:instrText " TOC \o \"1-3\" \h \z \u "` → `w:fldChar separate` → placeholder text → `w:fldChar end`. Switches: `\o "1-3"` sets heading levels, `\h` enables hyperlinks, `\z` hides tab leader in web view, `\u` uses paragraph outline levels.

**B. Static TOC (for non-Word consumers):**

Generate a manual list of headings with page numbers estimated from content length. Mark entries as `TOC 1`–`TOC 9` styles. Less accurate but works in all viewers.

**Update-on-open flag:** Set `w:updateFields w:val="true"` in `settings.xml` so Word refreshes all fields (including TOC) when the document opens.

### 4.4 Tables

**Structure requirements:**

- Every table MUST have a header row (`w:tblHeader` on first `w:tr`).
- Use `Table Grid` style or explicit borders for readability.
- Banding (alternating row colors) via `w:tblPr` → `w:tblStyleRowBandSize`.
- Merged cells: use `w:gridSpan` (horizontal) and `w:vMerge` (vertical) in `w:tcPr`.

```python
from docx import Document
doc = Document()
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text = 'Milestone', 'Owner', 'Due Date'
for cell in hdr:
    for p in cell.paragraphs:
        for r in p.runs:
            r.bold = True
# Add data rows via table.add_row().cells[i].text = ...
```

### 4.5 Headers and footers

**Page numbers (field-based):** Build `PAGE` (and optionally `NUMPAGES`) field codes in `section.footer.paragraphs[0]` by appending `w:fldChar begin`, `w:instrText`, `w:fldChar end` elements to a run via `OxmlElement`/`qn` from `docx.oxml`.

**Header content:** Document title (left), date (right), or company logo (image). Use `section.header.paragraphs[0]` and add runs/images.

**Different first page:** Set `section.different_first_page_header_footer = True` for cover pages without page numbers.

### 4.6 Footnotes and endnotes

`python-docx` has limited native support. Use raw OOXML:

1. Add footnote part to `word/footnotes.xml`.
2. Reference from body via `<w:footnoteReference w:id="N"/>`.
3. Define footnote content in `footnotes.xml` with matching `w:id`.

For endnotes, use `word/endnotes.xml` similarly.

### 4.7 Mail merge (docxtpl)

```python
from docxtpl import DocxTemplate
tpl = DocxTemplate('template.docx')
tpl.render({
    'client_name': 'Acme Corp',
    'date': '2026-11-19',
    'items': [
        {'description': 'Consulting', 'amount': '10,000'},
        {'description': 'Support', 'amount': '2,500'},
    ],
})
tpl.save('output.docx')
```

**Template tags:** `{{ variable }}` — simple substitution; `{% for item in items %} ... {% endfor %}` — loop; `{% if condition %} ... {% endif %}` — conditional; `{{ item.description | upper }}` — Jinja2 filters. For formatted merge fields (bold, color, hyperlinks) use `RichText` objects.

### 4.8 Tracked changes

- `w:ins` = inserted text; `w:del` = deleted text (uses `w:delText`); `w:moveFrom`/`w:moveTo` = moved text; `w:rPrChange`, `w:pPrChange` = property changes.
- **Adding revisions:** wrap new content in `<w:ins w:id="N" w:author="FileCraftBooster" w:date="...">` and deletions in `<w:del>`.
- **Accept/reject all:** not natively supported; requires XML manipulation to remove `w:ins`/`w:del` wrappers and keep final content.

### 4.9 Accessibility

| Check | Implementation |
|---|---|
| Heading order | Verify `Heading 1` → `Heading 2` → `Heading 3` sequence; no skips |
| Alt text on images | `docx` inline shapes → `wp:docPr` → `descr` attribute |
| Table headers | `w:tblHeader` on first row |
| Color contrast | Ensure text/background contrast ≥ 4.5:1 (WCAG AA) |
| Reading order | Logical paragraph order; avoid text boxes for body content |
| Language | Set `w:lang` in `w:rPr` for spell-check and screen readers |
| Document title | `docProps/core.xml` → `dc:title` |

```python
from docx.oxml.ns import qn
inline_shape = paragraph.runs[0]._r.xpath('.//wp:inline')[0]
docPr = inline_shape.find(qn('wp:docPr'))
docPr.set('descr', 'Bar chart showing Q3 revenue growth')
docPr.set('title', 'Q3 Revenue Chart')
```

---

## 5. Input Requirements

```yaml
word_engine_input:
  brief: string              # What the document is about
  audience: string           # Who will read it
  tone: enum                 # formal | casual | technical | persuasive
  length: enum               # one_page | short | medium | long
  brand_tokens:              # From SharedContext
    palette: {...}
    typography: {...}
  template_path: string | null  # Optional .docx template
  data: object | null        # Structured data for tables/charts
  accessibility_profile:     # From SharedContext
    standard: WCAG_2_2_AA
    require_alt_text: true
```

**Validation rules:**

- `brief` MUST be non-empty and ≥ 20 characters.
- `audience` MUST be specified; never assume.
- `tone` MUST map to style choices (font, spacing, formality).
- `length` MUST constrain output (word count targets).
- If `template_path` provided, MUST validate it opens without corruption.

---

## 6. Output Specifications

```yaml
word_engine_output:
  artifact_path: string      # .docx file path
  manifest:
    engine: "word-engine"
    engine_version: "1.0"
    styles_used: [string]    # e.g., ["Title", "Heading 1", "Normal", "Table Grid"]
    tables_count: int
    images_count: int
    footnotes_count: int
    fields_present: [string] # e.g., ["TOC", "PAGE", "NUMPAGES"]
    brand_tokens_applied: [string]
    accessibility_checks:
      heading_order: pass | fail
      alt_text: pass | fail | n/a
      table_headers: pass | fail | n/a
      color_contrast: pass | fail | n/a
    license_register_entries: [string]
    limitations: [string]    # e.g., ["TOC requires Word update on open"]
```

**File constraints:**

- `.docx` MUST be a valid ZIP package with `[Content_Types].xml`, `_rels/.rels`, `word/document.xml`.
- All XML MUST be well-formed; namespaces MUST be declared.
- File size SHOULD be < 50 MB for typical documents; larger requires chunked generation.

---

## 7. Decision Rules

| Scenario | Decision |
|---|---|
| User provides template + data | `docxtpl` with Jinja2 render |
| User requests "from scratch" document | `python-docx` programmatic build |
| Need TOC field | Raw OOXML `w:fldChar` + `w:instrText` |
| Need page numbers | Raw OOXML `PAGE`/`NUMPAGES` fields in header/footer |
| Need footnotes | Raw OOXML `word/footnotes.xml` part |
| Need tracked changes | Raw OOXML `w:ins`/`w:del` wrappers |
| Need custom styles not in template | `python-docx` `styles` API + `styles.xml` injection |
| Need mail merge at scale (>100 records) | `docxtpl` loop; chunk if memory-constrained |
| Need PDF output | Generate `.docx` then external conversion (not Word engine's job) |

---

## 8. Quality Standards

- **Structure:** Every document MUST have `Title` or `Heading 1` as first paragraph style.
- **Headings:** No skipped levels; max depth 3 for readability (9 allowed but discouraged).
- **Tables:** Header row mandatory; avoid tables for layout (use paragraphs).
- **Fonts:** Use brand typography tokens; fallback to `Calibri` or `Arial` if unavailable.
- **Spacing:** Consistent paragraph spacing (e.g., 0pt before, 6pt after for body).
- **Page setup:** A4 or Letter per locale; margins ≥ 1" (2.54 cm) for print.
- **Fields:** TOC and page numbers MUST use field codes, not static text.
- **Accessibility:** All images MUST have alt text; all tables MUST have header rows.
- **Manifest:** Every output MUST include a manifest listing styles, tables, fields, and accessibility status.

---

## 9. Error Handling

| Error | Detection | Recovery |
|---|---|---|
| Corrupt `.docx` (bad ZIP) | `zipfile.BadZipFile` | Attempt repair: extract `word/document.xml`, rebuild minimal package; if fails, request clean copy |
| Missing styles in template | `KeyError` on `doc.styles['Name']` | Inject missing style definitions into `styles.xml` |
| Invalid XML in OOXML patch | `xml.etree.ElementTree.ParseError` | Validate against OOXML schema; fix namespace/attribute issues |
| `docxtpl` template tag not found | `UndefinedError` | Provide default context or flag missing variable |
| Image file not found | `FileNotFoundError` | Skip image, log warning, continue document generation |
| Font not available | Runtime warning | Fallback to `Calibri`; note in manifest |
| File too large | Memory error | Chunk generation; split into multiple documents or use streaming |
| Circular reference in mail merge | Infinite loop detection | Limit iterations; validate data source before render |

---

## 10. Practical Examples

### Example A — Board memo (python-docx)

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Q3 Board Memo')
run.font.size = Pt(18)
run.font.bold = True
run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
title.style = doc.styles['Title']

doc.add_heading('Executive Summary', level=1)
doc.add_paragraph('Revenue grew 12% QoQ driven by enterprise segment...')

table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text = 'Metric', 'Q2', 'Q3'
for cell in hdr:
    for p in cell.paragraphs:
        for r in p.runs:
            r.bold = True
row = table.add_row().cells
row[0].text, row[1].text, row[2].text = 'Revenue', '$4.2M', '$4.7M'

doc.save('board_memo.docx')
```

### Example B — Mail merge letter (docxtpl)

**Template (`letter_template.docx`):**

```
{{ client_name }}

Dear {{ client_name }},

Thank you for your interest in {{ product_name }}. Your proposal is attached.

{% for item in deliverables %}
- {{ item.description }}: {{ item.amount }}
{% endfor %}

Sincerely,
{{ sender_name }}
```

**Render:**

```python
from docxtpl import DocxTemplate
tpl = DocxTemplate('letter_template.docx')
tpl.render({
    'client_name': 'PT. Maju Jaya',
    'product_name': 'Enterprise Suite',
    'deliverables': [
        {'description': 'Licenses', 'amount': 'IDR 50,000,000'},
        {'description': 'Implementation', 'amount': 'IDR 25,000,000'},
    ],
    'sender_name': 'Adhithya Soemitro',
})
tpl.save('proposal_letter.docx')
```

### Example C — Accessible report with TOC

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()
doc.settings.element.append(OxmlElement('w:updateFields'))
doc.settings.element[-1].set(qn('w:val'), 'true')

toc_para = doc.add_paragraph()
toc_para.style = doc.styles['TOC Heading']
toc_para.add_run('Table of Contents')
# Insert TOC field code via fldChar/instrText elements (see §4.3)

doc.add_heading('Introduction', level=1)
doc.add_paragraph('This report covers...')
doc.add_heading('Methodology', level=2)
doc.add_paragraph('We used...')
doc.add_heading('Results', level=2)
doc.add_paragraph('Key findings...')
doc.add_heading('Conclusion', level=1)
doc.add_paragraph('In summary...')

doc.save('accessible_report.docx')
```

---

## 11. Cross-References

- `architecture.md` — Shared context, orchestration rules
- `microsoft-ecosystem.md` — Word tier-1 capabilities and caveats
- `excel-engine.md` — When to link workbook data into Word tables
- `powerpoint-engine.md` — When to embed Word content in slides

---

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
