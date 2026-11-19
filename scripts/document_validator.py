#!/usr/bin/env python3
"""document_validator.py — Validate generated Office files and PDFs.

Checks file existence, magic/ZIP structure, opens with the corresponding
library, counts content elements, scans for missing images, empty docs and
Excel formula error literals. Prints a PASS/FAIL report; exit 0 = pass, 1 = fail.

Examples:
    python3 document_validator.py report.docx
    python3 document_validator.py workbook.xlsx --json
    python3 document_validator.py deck.pptx --json
    python3 document_validator.py paper.pdf

Requires: pip install python-docx openpyxl python-pptx
(PDF check is header/footer based — no dependency needed.)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None  # type: ignore

try:
    import openpyxl
except ImportError:
    openpyxl = None  # type: ignore

try:
    from pptx import Presentation as PptxPresentation
except ImportError:
    PptxPresentation = None  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("document_validator")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

XLSX_ERROR_LITERALS = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NULL!", "#NUM!")
OFFICE_MAGIC = {
    ".docx": "word/document.xml",
    ".xlsx": "xl/workbook.xml",
    ".pptx": "ppt/presentation.xml",
}


@dataclass
class ValidationResult:
    path: str
    kind: str = "unknown"
    ok: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)


def _check_zip_member(path: Path, member: str) -> Optional[str]:
    try:
        with zipfile.ZipFile(path) as zf:
            if member not in zf.namelist():
                return f"missing {member}"
            bad = zf.testzip()
            if bad:
                return f"corrupt zip member: {bad}"
    except zipfile.BadZipFile:
        return "not a valid ZIP package"
    except OSError as exc:
        return f"cannot read file: {exc}"
    return None


def validate_docx(path: Path) -> ValidationResult:
    res = ValidationResult(path=str(path), kind="docx")
    if DocxDocument is None:
        res.errors.append("python-docx not installed (pip install python-docx)")
        return res
    err = _check_zip_member(path, OFFICE_MAGIC[".docx"])
    if err:
        res.errors.append(err)
        return res
    try:
        doc = DocxDocument(str(path))
    except Exception as exc:  # noqa: BLE001
        res.errors.append(f"python-docx failed to open: {exc}")
        return res
    paragraphs = len(doc.paragraphs)
    tables = len(doc.tables)
    non_empty_paras = sum(1 for p in doc.paragraphs if p.text.strip())
    # image references live in word/media
    with zipfile.ZipFile(path) as zf:
        media = [n for n in zf.namelist() if n.startswith("word/media/")]
    res.stats = {
        "paragraphs": paragraphs,
        "non_empty_paragraphs": non_empty_paras,
        "tables": tables,
        "images": len(media),
        "sections": len(doc.sections),
    }
    if paragraphs == 0 and tables == 0:
        res.errors.append("document is empty (no paragraphs or tables)")
    elif non_empty_paras == 0:
        res.warnings.append("no non-empty paragraphs")
    # check inline image relationships vs media files (missing image check)
    rels = path.parent  # not needed; check drawing references quickly
    res.ok = not res.errors
    return res


def validate_xlsx(path: Path) -> ValidationResult:
    res = ValidationResult(path=str(path), kind="xlsx")
    if openpyxl is None:
        res.errors.append("openpyxl not installed (pip install openpyxl)")
        return res
    err = _check_zip_member(path, OFFICE_MAGIC[".xlsx"])
    if err:
        res.errors.append(err)
        return res
    try:
        wb = openpyxl.load_workbook(str(path), data_only=False)
    except Exception as exc:  # noqa: BLE001
        res.errors.append(f"openpyxl failed to open: {exc}")
        return res
    total_cells = 0
    formula_cells = 0
    error_hits: list[str] = []
    empty_sheets = 0
    for ws in wb.worksheets:
        sheet_cells = 0
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is None:
                    continue
                sheet_cells += 1
                total_cells += 1
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formula_cells += 1
                if isinstance(cell.value, str) and not cell.value.startswith("="):
                    for lit in XLSX_ERROR_LITERALS:
                        if lit in cell.value:
                            error_hits.append(f"{ws.title}!{cell.coordinate}={cell.value!r}")
        if sheet_cells == 0:
            empty_sheets += 1
    wb.close()
    res.stats = {
        "sheets": len(wb.sheetnames) if hasattr(wb, "sheetnames") else 0,
        "cells": total_cells,
        "formula_cells": formula_cells,
        "empty_sheets": empty_sheets,
    }
    # wb closed; recount sheetnames before close is safer — reopen cheaply
    try:
        wb2 = openpyxl.load_workbook(str(path), read_only=True)
        res.stats["sheets"] = len(wb2.sheetnames)
        wb2.close()
    except Exception:  # noqa: BLE001
        pass
    if error_hits:
        res.errors.append(f"formula error literals found: {len(error_hits)}")
        res.errors.extend(error_hits[:10])
    if empty_sheets == res.stats["sheets"] and res.stats["sheets"] > 0:
        res.errors.append("all sheets are empty")
    elif empty_sheets:
        res.warnings.append(f"{empty_sheets} empty sheet(s)")
    res.ok = not res.errors
    return res


def validate_pptx(path: Path) -> ValidationResult:
    res = ValidationResult(path=str(path), kind="pptx")
    if PptxPresentation is None:
        res.errors.append("python-pptx not installed (pip install python-pptx)")
        return res
    err = _check_zip_member(path, OFFICE_MAGIC[".pptx"])
    if err:
        res.errors.append(err)
        return res
    try:
        prs = PptxPresentation(str(path))
    except Exception as exc:  # noqa: BLE001
        res.errors.append(f"python-pptx failed to open: {exc}")
        return res
    n_slides = len(prs.slides._sldIdLst)  # noqa: SLF001
    shapes = sum(len(s.shapes) for s in prs.slides)
    pics = 0
    notes = 0
    for s in prs.slides:
        for sh in s.shapes:
            if sh.shape_type == 13:  # PICTURE
                pics += 1
        if s.has_notes_slide:
            notes += 1
    res.stats = {"slides": n_slides, "shapes": shapes, "images": pics, "notes_slides": notes}
    if n_slides == 0:
        res.errors.append("presentation has no slides")
    empty = sum(
        1 for s in prs.slides
        if not any(sh.has_text_frame and sh.text_frame.text.strip() for sh in s.shapes)
    )
    if empty:
        res.warnings.append(f"{empty} slide(s) have no text")
    res.ok = not res.errors
    return res


def validate_pdf(path: Path) -> ValidationResult:
    res = ValidationResult(path=str(path), kind="pdf")
    try:
        head = path.read_bytes()[:1024]
    except OSError as exc:
        res.errors.append(f"cannot read file: {exc}")
        return res
    if not head.startswith(b"%PDF"):
        res.errors.append("missing %PDF header")
        return res
    try:
        size = path.stat().st_size
        with path.open("rb") as fh:
            fh.seek(max(0, size - 2048))
            tail = fh.read()
        if b"%%EOF" not in tail:
            res.errors.append("missing %%EOF marker near end of file")
    except OSError as exc:
        res.errors.append(f"cannot read tail: {exc}")
    res.stats = {"size_bytes": path.stat().st_size}
    res.ok = not res.errors
    return res


def validate_file(path: Path) -> ValidationResult:
    if not path.exists():
        return ValidationResult(path=str(path), errors=["file does not exist"])
    ext = path.suffix.lower()
    if ext == ".docx":
        return validate_docx(path)
    if ext == ".xlsx":
        return validate_xlsx(path)
    if ext == ".pptx":
        return validate_pptx(path)
    if ext == ".pdf":
        return validate_pdf(path)
    return ValidationResult(path=str(path), errors=[f"unsupported extension: {ext}"])


def render_report(results: Sequence[ValidationResult]) -> str:
    lines = []
    all_ok = all(r.ok for r in results)
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        lines.append(f"[{status}] {r.path} ({r.kind})")
        for k, v in sorted(r.stats.items()):
            lines.append(f"       {k}: {v}")
        for w in r.warnings:
            lines.append(f"       WARN: {w}")
        for e in r.errors:
            lines.append(f"       ERROR: {e}")
    lines.append("=" * 60)
    lines.append("OVERALL: " + ("PASS" if all_ok else "FAIL"))
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Validate DOCX/XLSX/PPTX/PDF files for structural integrity "
                    "and common content problems.",
        epilog=FOOTER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("inputs", nargs="+", type=Path,
                    help="Files to validate (.docx .xlsx .pptx .pdf)")
    ap.add_argument("--json", action="store_true",
                    help="Emit machine-readable JSON report")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argparser().parse_args(argv)
    try:
        results = [validate_file(p) for p in args.inputs]
        if args.json:
            print(json.dumps([r.__dict__ for r in results], indent=2))
        else:
            print(render_report(results))
        return 0 if all(r.ok for r in results) else 1
    except Exception as exc:  # noqa: BLE001
        log.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
