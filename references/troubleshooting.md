# Troubleshooting Catalog

## Purpose

Failure-diagnosis catalog for FileCraftBooster workflows. Each entry
follows **symptom → diagnosis → fix → prevention**. Use the index to jump
to the relevant failure class.

## Index

1. Missing dependencies · 2. Corrupt files · 3. Encoding issues ·
4. Font problems · 5. Formula errors · 6. TOC / field issues ·
7. Image problems · 8. Graph API errors · 9. License ambiguity ·
10. Formatting drift · 11. Template merge conflicts

---

## 1. Missing Dependencies

**Symptom:** `ModuleNotFoundError: No module named 'docx'` / `openpyxl` /
`pptx` / `pypdf` / `pdfplumber`, or `pptxgenjs` not found.

**Diagnosis:**

```bash
python3 -c "import docx, openpyxl, pptx, pypdf, pdfplumber" 2>&1
node -e "require('pptxgenjs')" 2>&1
which python3 node pip3 npm
```

Check which interpreter actually runs the script — `python3` vs `python`
vs Homebrew/pyenv differ. `pip` fixes do not help `require()` failures
and vice versa.

**Fix:**

```bash
python3 -m pip install --upgrade pip
python3 -m pip install python-docx openpyxl python-pptx pypdf pdfplumber
python3 -c "import docx"          # verify same interpreter
npm install pptxgenjs             # local, or -g for global
```

On PEP 668 externally-managed environments:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install python-docx openpyxl python-pptx pypdf pdfplumber
```

**Prevention:** pin deps in `requirements.txt`/`package.json`; preflight
`python3 -c "import docx, openpyxl, pptx"` before work; use a venv.

---

## 2. Corrupt Files

**Symptom:** `BadZipFile`, `Package not found`, or Office "unreadable
content".

**Diagnosis:** DOCX/XLSX/PPTX are ZIP+XML. Test:

```python
import zipfile
z = zipfile.ZipFile(path)
bad = z.testzip()                 # first bad member or None
print("OK" if bad is None else f"Corrupt member: {bad}")
```

**Fix — Path A, extract-and-rebuild:**

```python
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w",
        zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        try:
            data = zin.read(item.filename)
        except Exception as e:
            print(f"Skipping {item.filename}: {e}"); continue
        zout.writestr(item, data)
```

Dropping non-essential members (thumbnails) is safe; if
`word/document.xml`, `xl/workbook.xml`, or `ppt/presentation.xml` is
corrupt, the file is unrecoverable this way.

**Path B — LibreOffice headless** (tolerates malformed XML; also
converts legacy `.doc`/`.xls`/`.ppt`):

```bash
soffice --headless --convert-to docx --outdir recovered/ broken.docx
soffice --headless --convert-to pdf broken.docx   # render check
```

**Path C — PDF:** `qpdf --check f.pdf`, `mutool clean f.pdf out.pdf`, or
`gs -o out.pdf -sDEVICE=pdfwrite f.pdf`.

**Prevention:** write temp + `os.replace()` atomic rename; `testzip()`
untrusted inputs; timestamped backups.

---

## 3. Encoding Issues

**Symptom:** mojibake (`Ã©`, `â€™`, `â€”`), `?` replacements,
`UnicodeDecodeError`.

**Diagnosis:**

```python
raw = open(path, "rb").read(200)
print(raw[:4])   # b'\xef\xbb\xbf' = UTF-8 BOM; b'\xff\xfe' = UTF-16LE
for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
    try:
        raw.decode(enc); print("decodes as", enc)
    except Exception: pass
```

Smart quotes/em-dashes are multi-byte UTF-8; cp1252 read as UTF-8 yields
`â€`-prefixed mojibake. Repair double-encoded text and strip BOM:

```python
fixed = raw.decode("utf-8").encode("cp1252", errors="ignore") \
        .decode("utf-8", errors="replace")
text = raw.decode("utf-8-sig")   # strip BOM
import unicodedata
text = unicodedata.normalize("NFKC", text)
```

DOCX/PPTX XML is always UTF-8; set `encoding="utf-8"` on text exports.

**Prevention:** declare encoding on all text I/O; `newline=""` for CSV;
UTF-8 without BOM unless legacy Excel needs it; normalize smart quotes
only when target requires ASCII — flag in manifest.

---

## 4. Font Problems

**Symptom:** wrong font after generation, PDF substitution, `font not
found`, tofu boxes (`□`).

**Diagnosis:**

```bash
fc-list | grep -i "fontname"; fc-match "Calibri"
# font names inside a DOCX:
python3 -c "from docx import Document; d=Document('f.docx'); \
print({r.font.name for p in d.paragraphs for r in p.runs if r.font.name})"
```

**Fix — substitution table:**

| Requested | Fallback |
|---|---|
| Calibri | Carlito |
| Arial | Liberation Sans / Arimo |
| Times New Roman | Liberation Serif / Tinos |
| Cambria | Caladea |
| Segoe UI | Selawik / Noto Sans |
| Brand font | Second choice or embedded subset |

**Font embedding for PDFs:**

```bash
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dEmbedAllFonts=true \
   -dSubsetFonts=true -sOutputFile=out.pdf in.pdf
```

Fonts must exist on the *converting* machine. **Tofu boxes:** font lacks
the glyph — switch to Noto Sans / Arial Unicode MS or replace the char.

**Prevention:** check availability before generation; embed fonts or
PDF-embed for distribution; avoid emoji/rare glyphs unverified.

---

## 5. Formula Errors

**Symptom:** `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`, `#N/A`, circular
reference warning, stale/0 after openpyxl round-trip.

**Diagnosis:**

```python
from openpyxl import load_workbook
wb  = load_workbook("f.xlsx", data_only=False)  # formulas
wbv = load_workbook("f.xlsx", data_only=True)   # cached values
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                print(ws.title, c.coordinate, c.value)
```

- `#REF!` — referenced cell/row/col deleted; trace with Ctrl+[ or search
  `#REF!` in formula strings.
- `#DIV/0!` — zero/empty denominator → `=IF(denom=0,"",numer/denom)` or
  `IFERROR`.
- `#NAME?` — newer functions (`XLOOKUP`, `FILTER`, `IFS`, `TEXTJOIN`,
  `CONCAT`) stored as `_xlfn.*` fail in older Excel → use legacy
  equivalents (`INDEX/MATCH`, nested `IF`, `&`).
- `#VALUE!` — wrong type in arithmetic. `#N/A` — lookup miss (data
  issue; wrap in `IFERROR` if acceptable).
- Circular reference — self-referencing formula; enable iterative calc
  only if intended.

**Fix patterns:**

```python
cell.value = '=IF(B2=0,"",A2/B2)'
cell.value = '=IFERROR(VLOOKUP(A2,Data!$A:$C,2,FALSE),"Not found")'
cell.value = '=INDEX(Data!$C:$C,MATCH(A2,Data!$A:$A,0))'
```

**Prevention:** `data_only=False` for edits (`data_only=True` destroys
formulas on save); recount formula cells after edits; flag volatile
functions (`NOW()`, `TODAY()`, `RAND()`, `OFFSET()`, `INDIRECT()`).

---

## 6. TOC / Field Issues

**Symptom:** stale TOC, "Error! Bookmark not defined", wrong page
numbers, TOC doesn't update.

**Diagnosis:** TOC is field code `TOC \o "1-3" \h \z \u`; refreshes on
F9 or when `word/settings.xml` has `<w:updateFields w:val="true"/>`:

```python
import zipfile
with zipfile.ZipFile("file.docx") as z:
    s = z.read("word/settings.xml").decode()
    print("updateFields set:", "updateFields" in s)
```

"Bookmark not defined" = headings lost their `Heading` style.

**Fix:** inject the flag via python-docx XML:

```python
from docx.oxml.ns import qn
settings = d.settings.element
fld = settings.makeelement(qn('w:updateFields'), {qn('w:val'): 'true'})
settings.insert(0, fld)
```

Manual: select TOC → Update Field → entire table, or Ctrl+A then F9.
Restore real Heading styles; regenerate TOC if structure changed.

**Prevention:** set `updateFields=true` on generated docs with TOCs; use
real heading styles; note "press F9 if needed" in report.

---

## 7. Image Problems

**Symptom:** broken image icons, blurry images, unsupported-format
errors, missing in PDF export, huge file sizes.

**Diagnosis:**

```python
from docx import Document
d = Document("file.docx")
for i, s in enumerate(d.inline_shapes):
    print(i, s.type, s.width, s.height)
for rel in d.part.rels.values():
    if "image" in rel.reltype:
        print(rel.target_ref)
```

Broken `r:embed`/`r:link` target = missing file/dead URL. <150 DPI at
print size = blurry (<300 for print). DOCX supports
PNG/JPEG/GIF/BMP/TIFF/WMF/EMF; WebP/SVG may fail in older Word.

**Fix:** re-download+embed broken links; replace missing files with a
note; swap in higher-res source; convert unsupported via Pillow
(`Image.open("x.webp").save("x.png")`); shrink with
`img.thumbnail((1600,1600), Image.LANCZOS)` + `quality=85`.

**Prevention:** validate format/DPI before insertion; prefer PNG or
JPEG≥85; embed copies under `assets/`; set explicit EMU dimensions in
PPTX.

---

## 8. Graph API Errors

**Symptom:** `401`, `403`, `404`, `429`, `503` from Graph calls.

| Status | Symptom | Fix |
|---|---|---|
| 401 | `InvalidAuthenticationToken` | Refresh: `POST /{tenant}/oauth2/v2.0/token` with `grant_type=refresh_token` → new `access_token`, retry once. Refresh fails → re-auth. |
| 403 | `Authorization_RequestDenied` / "Insufficient privileges" | Check token `scp` claim vs required scope; send user to consent: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={id}&response_type=code&scope={scopes} offline_access`. App-only: `.../adminconsent?client_id={id}&scope=.../.default`. |
| 404 | `Request_ResourceNotFound` | IDs are type-specific — user (GUID/UPN), drive item (id or `/me/drive/root:/path`), site (`hostname:/sites/name` or GUID). Confirm auth via `GET /me` first. |
| 429 | Throttling + `Retry-After` | Honor `Retry-After` exactly; else `delay = min(2^attempt,60)+jitter`, max 5 retries; reduce concurrency, use `$batch`, lower `$top`, prefer delta queries. |
| 503 | Service unavailable | Retry 3× exponential backoff; check M365 Service Health; report `request-id` to tenant admin. |

**Prevention:** decode JWT `exp`, refresh at ~80% lifetime; store granted
scopes; log `request-id`/`client-request-id`; never retry 401/403/404
blindly — each needs different remediation.

---

## 9. License Ambiguity

**Symptom:** no license metadata, or ambiguous license.

**Diagnosis:** Office core properties hold author/lastModifiedBy, not
license — license lives in footers, LICENSE files, or package metadata:

```python
d = Document("file.docx"); cp = d.core_properties
print(cp.author, "|", cp.last_modified_by)
wb = load_workbook("file.xlsx")
print(wb.properties.creator, "|", wb.properties.lastModifiedBy)
```

**Fix:** default policy — **exclude and report**:

```
LICENSE STATUS: UNVERIFIED
File: template.xlsx
Finding: No license file; author "Unknown"
Action: Excluded from distribution.
Recommendation: Confirm ownership before sharing.
```

If ownership confirmed: add `LICENSE` file + footer — `/proprietary`
(© holder, all rights reserved), `/mit`, `/cc-by-4.0`.

**Prevention:** every distributed asset carries LICENSE or copyright
footer; license check before ingesting third-party templates.

---

## 10. Formatting Drift

**Symptom:** output differs from source — colors shifted, fonts wrong,
direct formatting overriding theme.

**Diagnosis:** run-level formatting always beats style/theme:

```python
from docx import Document
d = Document("file.docx")
for p in d.paragraphs:
    for r in p.runs:
        if r.font.color and r.font.color.rgb:
            print("Direct color override:", r.font.color.rgb)
# Theme colors live in word/theme/theme1.xml
```

Drift causes: cross-document copy-paste, python-docx default template vs
corporate template, missing theme fonts, `w:rPr` overrides.

**Fix — clear direct formatting:**

```python
for p in d.paragraphs:
    for r in p.runs:
        r.font.color.rgb = None; r.font.name = None
        r.font.size = None; r.bold = None; r.italic = None
```

**Use corporate template as base:** `Document("corporate-template.dotx")`.
**PPTX:** edit `ppt/theme/theme1.xml` or apply `slide.slide_layout` for
master inheritance.

**Prevention:** start from user's `.dotx`; post-gen style audit vs spec;
prefer named styles; test render before delivery.

---

## 11. Template Merge Conflicts

**Symptom:** duplicated sections, misplaced placeholders, broken
formatting, leftover `{{tags}}`.

**Diagnosis:** scan for unreplaced tokens:

```python
import re
leftover = re.findall(r'\{\{[^}]+\}\}|\$\{[^}]+\}|<\?[^?]+\?>', text)
print("Unreplaced:", leftover)
```

Jinja2/docxtpl blocks (`{% if %}`, `{% for %}`) fail silently on data
shape mismatch; placeholders spanning merged cells break on expansion.

docxtpl usage:

```python
from docxtpl import DocxTemplate
tpl = DocxTemplate("template.docx")
tpl.render({"client_name": "Acme Corp",
            "items": [{"desc": "A", "qty": 1}]})
tpl.save("output.docx")
```

**Fix:** context keys must match `{{tags}}` exactly (case-sensitive);
optional fields get defaults; repeating sections need lists not scalars;
post-merge style repair:

```python
d = Document("output.docx")
for p in d.paragraphs:
    if p.style.name == 'Normal' and len(p.text) > 100:
        p.style = d.styles['Body Text']
```

**Prevention:** test template with sample data; validate every `{{tag}}`
has a context key; generate a template spec (placeholder, type, source);
keep templates flat — split complex conditionals.

---

## Quick Reference Card

| Error | First check | Likely fix |
|---|---|---|
| `ModuleNotFoundError` | Which Python? | `python3 -m pip install` in venv |
| `BadZipFile` | `zipfile.testzip()` | Extract-rebuild or LibreOffice |
| `Ã©` mojibake | File encoding | cp1252→utf-8 or utf-8-sig |
| Wrong font | `fc-list`, styles.xml | Substitute or install font |
| `#REF!` | Trace precedent | Restore deleted reference |
| `#NAME?` | Excel version | Replace `_xlfn.` funcs w/ legacy |
| TOC stale | `updateFields` flag | Set flag or F9 |
| Broken image | Relationship target | Re-embed or replace |
| Graph 401 | Token exp | Refresh flow |
| Graph 403 | Granted scopes | Admin consent URL |
| Graph 429 | Retry-After | Backoff + fewer requests |
| No license | Metadata check | Exclude + report |
| Format drift | Direct vs style | Clear direct formatting |
| Merge leftover | `{{tags}}` scan | Fix context keys |

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
