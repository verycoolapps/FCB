#!/usr/bin/env python3
"""spreadsheet_generator.py — Generate styled XLSX workbooks with openpyxl.

CLI examples:
    python3 spreadsheet_generator.py --output sales.xlsx \
        --sheet "Sales|A,B\n1,10\n2,20" --sheet "Notes|Item,Qty\nWidget,5" --force

    python3 spreadsheet_generator.py --output dash.xlsx \
        --sheet "Data|Month,Revenue\nJan,100\nFeb,150" \
        --dashboard "Summary!A1" --force

Requires: pip install openpyxl
"""

from __future__ import annotations

import argparse
import csv
import io
import logging
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

try:
    import openpyxl
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.worksheet import Worksheet
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'openpyxl'. Install it with:\n"
        "    pip install openpyxl\n"
    )
    raise SystemExit(2)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("spreadsheet_generator")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

HEADER_FILL = PatternFill("solid", fgColor="1F3A5F")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
THIN = Side(style="thin", color="B0B0B0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
NUMBER_FORMATS = {
    "int": "#,##0",
    "float": "#,##0.00",
    "percent": "0.0%",
    "currency": '"$"#,##0.00',
}

# Cells whose cached value looks like an Excel error literal
XLSX_ERROR_LITERALS = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NULL!", "#NUM!")


@dataclass
class SheetSpec:
    name: str
    rows: list[list[str]] = field(default_factory=list)
    data_file: Optional[Path] = None
    header_row: bool = True
    freeze: bool = True
    formulas: list[tuple[str, str]] = field(default_factory=list)  # (cell, formula)


def _coerce_rows(rows: list[list[str]]) -> list[list[object]]:
    """Convert CSV-ish string cells to int/float where possible."""
    out: list[list[object]] = []
    for row in rows:
        coerced: list[object] = []
        for cell in row:
            s = cell.strip()
            try:
                coerced.append(int(s))
                continue
            except ValueError:
                pass
            try:
                coerced.append(float(s))
                continue
            except ValueError:
                pass
            coerced.append(s)
        out.append(coerced)
    return out


def create_sheet_from_rows(wb: openpyxl.Workbook, spec: SheetSpec) -> Worksheet:
    """Create (or reuse) a worksheet and populate it from spec rows."""
    safe_name = spec.name[:31] or "Sheet"
    if safe_name in wb.sheetnames:
        ws = wb[safe_name]
        ws.delete_rows(1, ws.max_row)
    else:
        ws = wb.create_sheet(title=safe_name)

    if spec.data_file:
        if not spec.data_file.is_file():
            raise FileNotFoundError(f"Data file not found: {spec.data_file}")
        text = spec.data_file.read_text(encoding="utf-8-sig")
        dialect = csv.Sniffer().sniff(text[:2048], delimiters=",;\t|")
        parsed = list(csv.reader(io.StringIO(text), dialect))
        spec.rows = [[c for c in r] for r in parsed if any(c.strip() for c in r)]

    rows = _coerce_rows(spec.rows)
    for r_idx, row in enumerate(rows, start=1):
        for c_idx, value in enumerate(row, start=1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    apply_table_style(ws, header_row=spec.header_row)
    if spec.freeze and rows:
        ws.freeze_panes = "A2"
    _auto_width(ws)

    for cell_ref, formula in spec.formulas:
        if not formula.startswith("="):
            formula = "=" + formula
        ws[cell_ref] = formula
    return ws


def apply_table_style(ws: Worksheet, header_row: bool = True) -> None:
    """Style header row, borders, alignment and basic number formats."""
    max_row = ws.max_row
    max_col = ws.max_column
    if max_row == 0 or max_col == 0:
        return
    for row in ws.iter_rows(min_row=1, max_row=max_row, min_col=1, max_col=max_col):
        for cell in row:
            cell.border = BORDER
            cell.alignment = Alignment(vertical="center")
            if isinstance(cell.value, float):
                cell.number_format = NUMBER_FORMATS["float"]
            elif isinstance(cell.value, int) and not isinstance(cell.value, bool):
                cell.number_format = NUMBER_FORMATS["int"]
    if header_row:
        for cell in ws[1]:
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = Alignment(horizontal="center", vertical="center")


def _auto_width(ws: Worksheet, max_width: int = 50) -> None:
    for col_idx in range(1, ws.max_column + 1):
        letter = get_column_letter(col_idx)
        longest = 0
        for cell in ws.iter_cols(min_col=col_idx, max_col=col_idx):
            for c in cell:
                if c.value is not None:
                    longest = max(longest, len(str(c.value)))
        ws.column_dimensions[letter].width = min(max(longest + 2, 8), max_width)


def add_chart(wb: openpyxl.Workbook, data_ws: Worksheet, chart_type: str,
              title: str, anchor: str, categories_col: int = 1,
              values_cols: Optional[Sequence[int]] = None,
              data_range: Optional[tuple[int, int]] = None) -> None:
    """Add a bar/line chart on a new 'Charts' sheet (created if needed)."""
    chart_type = chart_type.lower()
    if chart_type in ("bar", "column"):
        chart = BarChart()
        chart.type = "col"
    elif chart_type in ("line",):
        chart = LineChart()
    else:
        raise ValueError(f"Unsupported chart type: {chart_type!r} (use bar|line)")

    if "Charts" not in wb.sheetnames:
        wb.create_sheet("Charts")
    chart_sheet = wb["Charts"]

    min_row, max_row = data_range or (1, data_ws.max_row)
    max_col = data_ws.max_column
    if values_cols is None:
        values_cols = list(range(categories_col + 1, max_col + 1))
    if not values_cols:
        raise ValueError("No value columns available for chart")

    data = Reference(data_ws, min_col=min(values_cols), max_col=max(values_cols),
                     min_row=min_row, max_row=max_row)
    cats = Reference(data_ws, min_col=categories_col,
                     min_row=min_row + (1 if data_ws.cell(min_row, categories_col).value else 0),
                     max_row=max_row)
    # Skip header for categories when first row looks like a header
    if data_ws.cell(min_row, categories_col).value is not None and isinstance(
            data_ws.cell(min_row, categories_col).value, str):
        cats = Reference(data_ws, min_col=categories_col, min_row=min_row + 1, max_row=max_row)
        data = Reference(data_ws, min_col=min(values_cols), max_col=max(values_cols),
                         min_row=min_row, max_row=max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = title
    chart.width = 18
    chart.height = 10
    chart_sheet.add_chart(chart, anchor)


def build_dashboard(wb: openpyxl.Workbook, data_sheet_name: str,
                    anchor: str = "A1", chart_type: str = "bar",
                    title: str = "Dashboard") -> None:
    """Build a summary sheet with a chart from a data sheet."""
    if data_sheet_name not in wb.sheetnames:
        raise ValueError(f"Data sheet not found: {data_sheet_name}")
    dash_name = "Dashboard"
    if dash_name in wb.sheetnames:
        wb.remove(wb[dash_name])
    dash = wb.create_sheet(dash_name)
    dash["A1"] = title
    dash["A1"].font = Font(bold=True, size=14, color="1F3A5F")
    dash["A3"] = f"Source: {data_sheet_name}"
    dash["A3"].font = Font(italic=True, size=9, color="666666")
    data_ws = wb[data_sheet_name]
    add_chart(wb, data_ws, chart_type, title, anchor)
    wb.move_sheet("Charts", offset=-(len(wb.sheetnames) - 1)) if "Charts" in wb.sheetnames else None


def validate_workbook(path: Path) -> list[str]:
    """Open the workbook and return a list of problems (empty = valid)."""
    problems: list[str] = []
    if not path.is_file():
        return [f"File not found: {path}"]
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            if "xl/workbook.xml" not in names:
                problems.append("Not an XLSX package (missing xl/workbook.xml)")
                return problems
    except zipfile.BadZipFile:
        return [f"Not a valid ZIP/XLSX file: {path}"]
    try:
        wb = openpyxl.load_workbook(str(path), data_only=False)
        if not wb.sheetnames:
            problems.append("Workbook has no sheets")
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str):
                        for err in XLSX_ERROR_LITERALS:
                            if err in cell.value and not cell.value.startswith("="):
                                problems.append(
                                    f"Sheet '{ws.title}'!{cell.coordinate}: "
                                    f"possible error literal {err}"
                                )
        wb.close()
    except Exception as exc:  # noqa: BLE001
        problems.append(f"openpyxl failed to open workbook: {exc}")
    return problems


def parse_sheet_arg(value: str) -> tuple[str, str]:
    if "|" not in value:
        raise argparse.ArgumentTypeError("--sheet must be 'Name|CSV data'")
    name, data = value.split("|", 1)
    name = name.strip()
    if not name:
        raise argparse.ArgumentTypeError("--sheet name must not be empty")
    return name, data


def parse_csv_rows(data: str) -> list[list[str]]:
    rows = [
        [c.strip() for c in r]
        for r in csv.reader(io.StringIO(data))
        if any(c.strip() for c in r)
    ]
    if not rows:
        raise ValueError("Sheet data is empty")
    return rows


def parse_formula_arg(value: str) -> tuple[str, str]:
    """Parse 'Sheet!A1=SUM(B2:B10)' or 'A1=SUM(B2:B10)' (uses first sheet)."""
    if "=" not in value:
        raise argparse.ArgumentTypeError("--formula must be 'Cell=FORMULA' or 'Sheet!Cell=FORMULA'")
    cell_part, formula = value.split("=", 1)
    cell_part = cell_part.strip()
    if "!" in cell_part:
        sheet, cell = cell_part.rsplit("!", 1)
    else:
        sheet, cell = "", cell_part
    if not cell.strip():
        raise argparse.ArgumentTypeError("--formula cell reference missing")
    return (sheet.strip(), cell.strip(), formula.strip())


def _resolve_output(output: Path, force: bool) -> Path:
    if output.exists() and not force:
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
        description="Generate styled XLSX workbooks (openpyxl).",
        epilog=f"{FOOTER}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--output", "-o", required=True, type=Path, help="Output .xlsx path")
    ap.add_argument("--sheet", action="append", default=[],
                    metavar="'Name|CSV data' or 'Name|@datafile.csv'",
                    help="Add a sheet (repeatable). Prefix CSV with @ to read a file.")
    ap.add_argument("--formula", action="append", default=[],
                    metavar="'Sheet!A1=SUM(B2:B10)'",
                    help="Inject a formula into a cell (repeatable)")
    ap.add_argument("--dashboard", nargs="?", const="__auto__", default=None,
                    metavar="DATA_SHEET",
                    help="Build a 'Dashboard' sheet with a chart from DATA_SHEET "
                         "(default: first sheet)")
    ap.add_argument("--chart-type", choices=["bar", "line"], default="bar",
                    help="Dashboard chart type (default: bar)")
    ap.add_argument("--no-freeze", action="store_true", help="Do not freeze header row")
    ap.add_argument("--force", action="store_true", help="Overwrite existing output")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argparser().parse_args(argv)
    try:
        specs: list[SheetSpec] = []
        for raw in args.sheet:
            name, data = parse_sheet_arg(raw)
            spec = SheetSpec(name=name, freeze=not args.no_freeze)
            if data.startswith("@"):
                spec.data_file = Path(data[1:]).expanduser()
            else:
                spec.rows = parse_csv_rows(data)
            specs.append(spec)

        if not specs:
            log.error("Nothing to generate: provide at least one --sheet")
            return 2

        wb = openpyxl.Workbook()
        # Remove default sheet; we create our own
        wb.remove(wb.active)

        # Attach formulas to matching sheet specs
        for f_raw in args.formula:
            sheet_name, cell, formula = parse_formula_arg(f_raw)
            target = None
            for spec in specs:
                if spec.name[:31] == sheet_name or (not sheet_name and spec is specs[0]):
                    target = spec
                    break
            if target is None:
                log.error("Formula targets unknown sheet %r", sheet_name)
                return 2
            target.formulas.append((cell, formula))

        sheets: dict[str, Worksheet] = {}
        for spec in specs:
            sheets[spec.name[:31]] = create_sheet_from_rows(wb, spec)
            log.info("Created sheet '%s' (%d rows)", spec.name, len(spec.rows) or "?")

        if args.dashboard is not None:
            data_name = specs[0].name[:31] if args.dashboard == "__auto__" else args.dashboard
            build_dashboard(wb, data_name, chart_type=args.chart_type)
            log.info("Added dashboard chart from '%s'", data_name)

        out = _resolve_output(args.output, args.force)
        wb.save(str(out))
        wb.close()

        problems = validate_workbook(out)
        if problems:
            for p in problems:
                log.error("Validation: %s", p)
            return 1
        log.info("Wrote %s", out)
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        log.error("Failed: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        log.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
