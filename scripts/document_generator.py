#!/usr/bin/env python3
"""document_generator.py — Generate professional DOCX reports with python-docx.

CLI examples:
    python3 document_generator.py --title "Q4 Report" --subtitle "Confidential" \
        --output report.docx --section "Summary|All KPIs exceeded target." \
        --section "Risks|Supply chain delays." --table "Risks|Item|Owner|Impact" \
        "Supply delay|Logistics|A.S.|High|" --force

    python3 document_generator.py --input-json spec.json --output report.docx --force

Requires: pip install python-docx
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import logging
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional, Sequence

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'python-docx'. Install it with:\n"
        "    pip install python-docx\n"
    )
    raise SystemExit(2)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("document_generator")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

THEME = {
    "primary": RGBColor(0x1F, 0x3A, 0x5F),
    "accent": RGBColor(0xC8, 0x90, 0x1A),
    "body": RGBColor(0x22, 0x22, 0x22),
    "heading_font": "Calibri",
    "body_font": "Calibri",
}

SECTION_RE = "Heading|Body text"
TABLE_RE = "Optional header cols...|row1...|row2..."  # document only


@dataclass
class Section:
    heading: str
    body: str = ""


@dataclass
class ReportSpec:
    title: str = ""
    subtitle: str = ""
    author: str = ""
    sections: list[Section] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)  # each: header + rows
    toc: bool = True
    page_numbers: bool = True


def _style_document(doc: "Document") -> None:
    """Apply the shared theme fonts/colors to the Normal style and headings."""
    normal = doc.styles["Normal"]
    normal.font.name = THEME["body_font"]
    normal.font.size = Pt(11)
    normal.font.color.rgb = THEME["body"]
    for level in range(1, 4):
        try:
            st = doc.styles[f"Heading {level}"]
        except KeyError:
            continue
        st.font.name = THEME["heading_font"]
        st.font.color.rgb = THEME["primary"]
        st.font.bold = True
    for lvl, size in ((1, 26), (2, 20), (3, 14)):
        try:
            st = doc.styles[f"Heading {lvl}"]
            st.font.size = Pt(size)
        except KeyError:
            pass


def _set_cell_shading(cell, hex_color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def _add_page_number_footer(section) -> None:
    """Insert a centered 'Page X of Y' field into the footer of *section*."""
    footer = section.footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.text = "Page "
    # PAGE field
    fld1 = OxmlElement("w:fldSimple")
    fld1.set(qn("w:instr"), "PAGE")
    run_el = OxmlElement("w:r")
    t_el = OxmlElement("w:t")
    t_el.text = "1"
    run_el.append(t_el)
    fld1.append(run_el)
    para._p.append(fld1)
    # " of "
    r = para.add_run(" of ")
    r.font.size = Pt(9)
    # NUMPAGES field
    fld2 = OxmlElement("w:fldSimple")
    fld2.set(qn("w:instr"), "NUMPAGES")
    run_el2 = OxmlElement("w:r")
    t_el2 = OxmlElement("w:t")
    t_el2.text = "1"
    run_el2.append(t_el2)
    fld2.append(run_el2)
    para._p.append(fld2)
    for run in para.runs:
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def add_header_footer(doc: "Document", title: str = "", page_numbers: bool = True) -> None:
    """Set document header (title right-aligned) and footer (page numbers)."""
    for section in doc.sections:
        if title:
            header = section.header
            hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hp.text = title
            for run in hp.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = THEME["accent"]
        if page_numbers:
            _add_page_number_footer(section)


def add_cover(doc: "Document", title: str, subtitle: str = "", author: str = "") -> None:
    """Add a centered cover block with title, optional subtitle and author."""
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(34)
    run.font.bold = True
    run.font.color.rgb = THEME["primary"]
    if subtitle:
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        srun = sp.add_run(subtitle)
        srun.font.size = Pt(16)
        srun.font.color.rgb = THEME["accent"]
    if author:
        ap = doc.add_paragraph()
        ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        arun = ap.add_run(f"Prepared by {author}")
        arun.font.size = Pt(12)
        arun.italic = True
    doc.add_page_break()


def add_toc_field(doc: "Document") -> None:
    """Insert a Table of Contents field (updates on open in Word)."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    p.add_run("Table of Contents")
    para = doc.add_paragraph()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    run = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "(Right-click and select 'Update Field' to populate.)"
    run.append(t)
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr, fld_sep, run, fld_end):
        para._p.append(el)


def add_heading_styled(doc: "Document", text: str, level: int = 1) -> None:
    level = max(1, min(3, level))
    doc.add_heading(text, level=level)


def add_paragraph_styled(doc: "Document", text: str, bold: bool = False,
                         italic: bool = False, size: Optional[float] = None) -> None:
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = THEME["body"]
    if size:
        run.font.size = Pt(size)
    return p


def add_table(doc: "Document", rows: Sequence[Sequence[str]],
              header: bool = True) -> None:
    """Add a bordered table; first row shaded as header when *header* is True."""
    if not rows:
        raise ValueError("add_table: rows must not be empty")
    ncols = len(rows[0])
    if any(len(r) != ncols for r in rows):
        raise ValueError("add_table: all rows must have the same number of columns")
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    for ci, cell_text in enumerate(rows[0]):
        cell = table.rows[0].cells[ci]
        cell.text = str(cell_text)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
        _set_cell_shading(cell, "1F3A5F")
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for ri, row in enumerate(rows[1:], start=1):
        for ci, cell_text in enumerate(row):
            cell = table.rows[ri].cells[ci]
            cell.text = str(cell_text)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
    if not header:
        for cell in table.rows[0].cells:
            _set_cell_shading(cell, "FFFFFF")
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb = THEME["body"]
    doc.add_paragraph()


def build_document(spec: ReportSpec) -> "Document":
    doc = Document()
    _style_document(doc)
    core = doc.core_properties
    core.title = spec.title or "Report"
    core.author = spec.author or "FileCraftBooster"
    if spec.title or spec.subtitle:
        add_cover(doc, spec.title, spec.subtitle, spec.author)
    add_header_footer(doc, title=spec.title, page_numbers=spec.page_numbers)
    if spec.toc:
        add_toc_field(doc)
    for section in spec.sections:
        if section.heading:
            add_heading_styled(doc, section.heading, level=1)
        if section.body:
            for para_text in section.body.split("\n"):
                add_paragraph_styled(doc, para_text.strip())
    for table_rows in spec.tables:
        add_table(doc, table_rows)
    return doc


def parse_section_arg(value: str) -> Section:
    if "|" not in value:
        raise argparse.ArgumentTypeError(
            f"--section must be 'Heading|Body text' (got: {value!r})"
        )
    heading, body = value.split("|", 1)
    heading, body = heading.strip(), body.strip()
    if not heading:
        raise argparse.ArgumentTypeError("--section heading must not be empty")
    return Section(heading=heading, body=body)


def parse_table_arg(value: str) -> list[list[str]]:
    """Parse 'Header1,Header2|row1a,row1b|row2a,row2b' into rows of lists."""
    rows: list[list[str]] = []
    for row_text in value.split("|"):
        cells = [c.strip() for c in row_text.split(",")]
        rows.append(cells)
    if not rows or not rows[0] or any(not r for r in rows):
        raise argparse.ArgumentTypeError(
            f"--table rows must be non-empty CSV-ish segments (got: {value!r})"
        )
    ncols = len(rows[0])
    if any(len(r) != ncols for r in rows):
        raise argparse.ArgumentTypeError("--table: every row must have the same column count")
    return rows


def load_json_spec(path: Path) -> ReportSpec:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON spec must be an object")
    spec = ReportSpec(
        title=str(data.get("title", "")),
        subtitle=str(data.get("subtitle", "")),
        author=str(data.get("author", "")),
        toc=bool(data.get("toc", True)),
        page_numbers=bool(data.get("page_numbers", True)),
    )
    for s in data.get("sections", []):
        spec.sections.append(Section(heading=str(s.get("heading", "")),
                                     body=str(s.get("body", ""))))
    for t in data.get("tables", []):
        if isinstance(t, dict) and "rows" in t:
            spec.tables.append([[str(c) for c in r] for r in t["rows"]])
        elif isinstance(t, list):
            spec.tables.append([[str(c) for c in r] for r in t])
    return spec


def validate_output(path: Path) -> bool:
    """Re-open the produced file with python-docx to confirm it is valid."""
    try:
        with zipfile.ZipFile(path) as zf:
            if "word/document.xml" not in zf.namelist():
                log.error("Validation failed: not a DOCX package")
                return False
        doc = Document(str(path))
        _ = len(doc.paragraphs)
        return True
    except Exception as exc:  # noqa: BLE001
        log.error("Validation failed for %s: %s", path, exc)
        return False


def _resolve_output(output: Path, force: bool) -> Path:
    if output.exists() and not force:
        # versioned fallback: name_1.docx, name_2.docx ...
        stem, suffix = output.stem, output.suffix
        i = 1
        while True:
            candidate = output.with_name(f"{stem}_{i}{suffix}")
            if not candidate.exists():
                return candidate
            i += 1
    return output


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Generate professional DOCX reports (python-docx).",
        epilog=f"{SECTION_RE}\n{TABLE_RE}\n{FOOTER}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--output", "-o", required=True, type=Path,
                    help="Output .docx path")
    ap.add_argument("--title", default="", help="Document title (cover)")
    ap.add_argument("--subtitle", default="", help="Subtitle on cover")
    ap.add_argument("--author", default="", help="Author name on cover")
    ap.add_argument("--section", action="append", default=[],
                    type=parse_section_arg, metavar="'Heading|Body text'",
                    help="Add a section (repeatable)")
    ap.add_argument("--table", action="append", default=[],
                    type=parse_table_arg, metavar="'H1,H2|r1a,r1b|r2a,r2b'",
                    help="Add a table (repeatable)")
    ap.add_argument("--input-json", type=Path, default=None,
                    help="Structured JSON spec (merged with CLI args)")
    ap.add_argument("--no-toc", action="store_true", help="Omit Table of Contents")
    ap.add_argument("--no-page-numbers", action="store_true",
                    help="Omit footer page numbers")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing output file")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argparser().parse_args(argv)
    try:
        spec = ReportSpec(
            title=args.title,
            subtitle=args.subtitle,
            author=args.author,
            sections=list(args.section),
            tables=list(args.table),
            toc=not args.no_toc,
            page_numbers=not args.no_page_numbers,
        )
        if args.input_json:
            if not args.input_json.is_file():
                log.error("Input JSON not found: %s", args.input_json)
                return 2
            json_spec = load_json_spec(args.input_json)
            # CLI args take precedence over JSON where provided
            spec.title = args.title or json_spec.title
            spec.subtitle = args.subtitle or json_spec.subtitle
            spec.author = args.author or json_spec.author
            spec.sections = list(args.section) + json_spec.sections
            spec.tables = list(args.table) + json_spec.tables
            spec.toc = json_spec.toc and not args.no_toc
            spec.page_numbers = json_spec.page_numbers and not args.no_page_numbers
        if not spec.sections and not spec.tables and not spec.title:
            log.error("Nothing to generate: provide --title/--section/--table/--input-json")
            return 2
        out = _resolve_output(args.output, args.force)
        doc = build_document(spec)
        doc.save(str(out))
        if not validate_output(out):
            return 1
        log.info("Wrote %s", out)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        log.error("Failed: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        log.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
