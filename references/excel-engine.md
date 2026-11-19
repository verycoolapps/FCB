# FileCraftBooster — Excel Engine Reference

**Document class:** Engine technical reference
**Audience:** Engineers and reviewers implementing or auditing XLSX generation
**Version:** 1.0
**Primary libraries:** `openpyxl`, `XlsxWriter`, `pandas` + `xlsxwriter`

---

## 1. Purpose

The Excel engine produces and enhances `.xlsx` artifacts: financial models, RAB/BOQ cost models, KPI dashboards, data-validation-driven templates, PivotTable-ready datasets, and formula-correct workbooks. It is the reference implementation for all spreadsheet output in FileCraftBooster.

---

## 2. Scope

Covers: library selection (`openpyxl` vs `XlsxWriter` vs `pandas`), financial model patterns (3-statement, DCF, LBO-lite), RAB/BOQ structures, KPI dashboards, formula intelligence (modern functions, dynamic arrays, financial/statistical/date functions), PivotTables, Power Query patterns, data validation, conditional formatting, named ranges, defined tables, charts, formula-correctness rules, recalculation flags, and worked examples.

Out of scope: `.xls` (legacy binary), `.xlsm` with VBA macros (FileCraftBooster does not generate VBA), Power BI `.pbix` files.

---

## 3. Capabilities
| Capability | Implementation path | Notes |
|---|---|---|
| Workbook creation from scratch | `XlsxWriter` | Fastest, best charts/formatting, no Excel dependency |
| Modify existing workbook | `openpyxl` | Preserves formulas/styles; `XlsxWriter` cannot modify |
| Bulk data pipelines | `pandas` + `xlsxwriter` | `df.to_excel(engine='xlsxwriter')` |
| Financial models (3-stmt/DCF/LBO) | Both + formula templates | See §4.3 |
| RAB/BOQ cost models | Both + structured tables | See §4.4 |
| KPI dashboards | `XlsxWriter` + CF + charts | See §4.5 |
| PivotTables | `openpyxl` (basic) / raw OOXML | Complex pivots need OOXML |
| Power Query definitions | Raw OOXML `customXml` | Refresh requires Excel |
| Data validation | `openpyxl`/`XlsxWriter` `data_validation` | Lists, dates, custom formulas |
| Conditional formatting | Both libraries | Scales, bars, icons, formulas |
| Named ranges / tables | Both libraries | `defined_names`, `add_table` |
| Charts | `XlsxWriter` (native) / `openpyxl` (limited) | Column, line, pie, bar, area, scatter |

## 4. Detailed Procedures

### 4.1 Library selection decision rule

| Scenario | Library | Rationale |
|---|---|---|
| New workbook, heavy formatting, charts | `XlsxWriter` | Fastest, best chart support, no Excel dependency |
| Modify existing workbook (preserve formulas/styles) | `openpyxl` | Reads/writes existing files; `XlsxWriter` cannot modify |
| Bulk data from pandas DataFrame | `pandas` + `xlsxwriter` | `df.to_excel(engine='xlsxwriter')` for formatted output |
| Need PivotTables | `openpyxl` (basic) or raw OOXML | `XlsxWriter` does not support PivotTables |
| Need Power Query definitions | Raw OOXML `customXml` | Neither library natively supports Power Query |
| Need VBA macros | Not supported | FileCraftBooster does not generate `.xlsm` |

### 4.2 Workbook structure standards

**Sheet ordering convention:**

1. `README` or `Cover` — purpose, instructions, version.
2. `Assumptions` / `Inputs` — all hardcoded inputs centralized.
3. `Data` / `Raw_Data` — source data (if applicable).
4. `Calculations` / `Model` — formulas and logic.
5. `Outputs` / `Dashboard` — summaries, charts, KPIs.
6. `Checks` — reconciliation, error checks, validation.

**Cell reference rules:**

- NEVER hardcode magic numbers in formulas; reference `Assumptions` sheet.
- Use named ranges for key inputs (`TaxRate`, `WACC`, `GrowthRate`).
- Use structured table references (`Table1[Column]`) for data tables.
- Absolute references (`$A$1`) for fixed anchors; relative for ranges.

### 4.3 Financial model patterns

#### 3-Statement Model (Income Statement, Balance Sheet, Cash Flow)

- `Assumptions` sheet: revenue growth, margins, tax rate, capex, working capital days.
- `Income_Statement`: Revenue → COGS → Gross Profit → OpEx → EBITDA → D&A → EBIT → Interest → EBT → Tax → Net Income.
- `Balance_Sheet`: Assets (Cash, AR, Inventory, PP&E) = Liabilities (AP, Debt) + Equity.
- `Cash_Flow`: Net Income + D&A − Capex − ΔWorking Capital = Operating CF; + Financing CF = Ending Cash.
- `Checks`: Cash on BS = Cash on CF; Assets = Liabilities + Equity.

**Formula rules:** Revenue `=Prior_Revenue * (1 + Revenue_Growth_Rate)`; COGS `=Revenue * COGS_Percent`; Net Income `=EBT * (1 - Tax_Rate)`; Cash `=Prior_Cash + Operating_CF + Financing_CF`; balance check `=Assets - (Liabilities + Equity)` must equal 0.

#### DCF Model

- `Assumptions`: WACC, terminal growth, forecast period (5–10 years).
- `FCF_Forecast`: Revenue → EBITDA → EBIT → NOPAT → + D&A − Capex − ΔNWC = FCF.
- `Valuation`: PV of FCF (explicit period) + PV of terminal value (Gordon Growth) = Enterprise Value; − Net Debt = Equity Value.
- `Checks`: WACC components sum to 100%; terminal value should not dominate (>70% of EV is a red flag).

**Key formulas:** `PV = FCF / (1 + WACC)^Year`; `Terminal Value = FCF_Final * (1 + g) / (WACC - g)`; `Enterprise Value = Σ PV(FCF) + PV(Terminal Value)`; `Equity Value = Enterprise Value − Net Debt`.

#### LBO-lite Model

- `Sources_Uses`: Purchase price, debt tranche, equity contribution.
- `Operating_Forecast`: Revenue, EBITDA, leverage ratios.
- `Debt_Schedule`: Beginning balance, amortization, cash sweep, ending balance.
- `Returns`: IRR, MOIC, equity proceeds at exit.

**Key formulas:** `Debt_Paydown = Min(Available_Cash, Scheduled_Amortization + Cash_Sweep)`; `Equity_Proceeds = Exit_EV − Net_Debt_at_Exit`; `IRR` via `=IRR(cash_flows)` or `=XIRR(cash_flows, dates)`; `MOIC = Total_Proceeds / Equity_Invested`.

### 4.4 RAB/BOQ (Bill of Quantities) cost models

**Indonesian construction context:** RAB (Rencana Anggaran Biaya) is the standard cost estimate for construction projects.

- `BOQ` sheet: Item No, Description, Unit, Quantity, Unit Price, Total Price.
- `Price_Breakdown`: Material, labor, equipment, overhead, profit per item.
- `Summary`: Total direct cost, overhead %, profit %, tax (PPN 11%), grand total.
- `Checks`: Sum of item totals = BOQ total; markup percentages applied correctly.

**Formula rules:** `Total_Price = Quantity * Unit_Price`; `Unit_Price = Material + Labor + Equipment + Overhead + Profit`; `Grand_Total = Subtotal * (1 + PPN_Rate)` where `PPN_Rate = 0.11` (2026 rate); use `ROUND` to 0 or 2 decimals for currency.

### 4.5 KPI dashboards

- Top row: 4–6 headline KPIs (Revenue, Profit, Growth %, Margin %).
- Middle: Trend charts (line for revenue, bar for expenses).
- Bottom: Detailed table with drill-down capability.
- Implementation: `XlsxWriter` native charts, conditional formatting for thresholds, data validation for period selector, named ranges for chart references.

### 4.6 Formula intelligence

#### Modern functions (Excel 365 / 2021+)

`XLOOKUP`, `XMATCH`, `LET`, `LAMBDA`, `FILTER`, `SORT`/`SORTBY`, `UNIQUE`, `SEQUENCE`, `TEXTSPLIT`, `VSTACK`/`HSTACK`, `TEXTJOIN`, `IFS`, `SWITCH`, `MAXIFS`/`MINIFS`. Canonical patterns: `=XLOOKUP(id, ids, values)`, `=LET(x, A1*2, y, x+1, y*3)`, `=FILTER(range, condition)`, `=IFS(A1>10,"High",A1>5,"Med",TRUE,"Low")`.

#### Dynamic array spill behavior

`FILTER`, `SORT`, `UNIQUE`, `SEQUENCE` return spilled arrays; blocked spill ranges produce `#SPILL!`. Use `@` implicit intersection for single values. FileCraftBooster MUST write spill-expecting formulas and never hardcode output ranges.

#### Financial functions

`NPV`, `IRR`, `XNPV`, `XIRR` (date-aware), `PMT`, `FV`, `PV`, `RATE`, `NPER`, `SLN`, `DB`, `DDB`. Canonical: `=NPV(rate, cashflows)`, `=XIRR(values, dates)`, `=PMT(rate, nper, pv)`, `=SLN(cost, salvage, life)`.

#### Statistical functions

`COUNTIFS`, `SUMIFS`, `AVERAGEIFS`, `MEDIAN`, `STDEV`/`STDEV.P`/`STDEV.S`, `CORREL`, `PERCENTILE`/`PERCENTILE.INC`. Canonical: `=SUMIFS(sum_range, crit_range, crit)`, `=STDEV.S(range)`.

#### Date functions

`EDATE`, `EOMONTH`, `NETWORKDAYS`, `WORKDAY`, `DATEDIF`, `YEARFRAC`. Canonical: `=NETWORKDAYS(start, end, holidays)`, `=EDATE(date, months)`, `=DATEDIF(start, end, "M")`.

#### Lookup chains

`VLOOKUP`/`HLOOKUP` are legacy — prefer `XLOOKUP`. `INDEX`/`MATCH` two-way lookup: `=INDEX(range, MATCH(row_crit, row_range, 0), MATCH(col_crit, col_range, 0))`. `XMATCH` returns position only: `=XMATCH(lookup, lookup_range, [match_mode], [search_mode])`.

### 4.7 PivotTables and PivotCaches

`openpyxl` supports basic PivotTables via `openpyxl.pivot.table.TableDefinition`; complex pivots (calculated fields, grouped dates, slicers) require raw OOXML manipulation of `pivotCacheDefinition*.xml`/`pivotTable*.xml`. Recommended approach: create source data as an Excel Table (`ListObject`), define PivotCache referencing the table range, create PivotTable with row/column/data fields, apply number formats and totals. Limitation: for production use, generate the data and let the user create the pivot in Excel, or have `XlsxWriter` write source data plus pivot-creation instructions.

### 4.8 Power Query / Get & Transform patterns

**FileCraftBooster can write:** `customXml/item*.xml` query definitions, connection strings, M-language formulas, and load-order specs.
**Requires Excel:** live query refresh, credential prompts/privacy levels, query folding.
**Pattern:** write query definitions + `POWER-QUERY-SETUP.md` instructing user to open in Excel → Data → Refresh All.

### 4.9 Data validation

| Type | Implementation | Example |
|---|---|---|
| List | `DataValidation(type="list", formula1="Sheet1!$A$1:$A$10")` | Dropdown from range |
| Whole number | `type="whole", operator="between", formula1=1, formula2=100` | 1–100 integer |
| Decimal | `type="decimal", operator="between", formula1=0, formula2=1` | 0.0–1.0 |
| Date | `type="date", operator="between", formula1="2026-01-01", formula2="2026-12-31"` | Date range |
| Text length | `type="textLength", operator="lessThan", formula1=50` | Max 50 chars |
| Custom formula | `type="custom", formula1="=AND(A1>0,A1<100)"` | Complex rule |

`showErrorMessage=True` shows an alert on invalid entry; `errorStyle` controls severity (`stop` rejects, `warning` allows with warning, `information` is informational).

### 4.10 Conditional formatting

| Type | Implementation |
|---|---|
| Cell value comparison | `CellIsRule` |
| Color scale | `ColorScaleRule` |
| Data bar | `DataBarRule` |
| Icon set | `IconSetRule` |
| Formula-based | `FormulaRule` |
| Top/bottom N | `Top10Rule` |

Use sparingly; too much formatting reduces readability. Reserve for KPIs and exceptions.

### 4.11 Named ranges and defined tables

```python
from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.table import Table

wb = Workbook(); ws = wb.active
ws['A1'] = 0.21  # Tax rate
wb.defined_names.add(DefinedName('TaxRate', attr_text='Assumptions!$A$1'))  # =Revenue * TaxRate
ws.add_table(Table(displayName='SalesData', ref='A1:D100'))  # =SUM(SalesData[Revenue])
```

Benefits: auto-expansion when data added; readable formulas; PivotTable-ready.

### 4.12 Charts

`XlsxWriter` chart types: `column`/`bar` (comparisons), `line` (trends), `pie`/`doughnut` (part-to-whole, sparingly), `area`/`stacked_area` (cumulative), `scatter` (correlations), `radar` (multi-axis), `stock` (OHLC). Best practices: label axes with units; consistent brand-palette colors; avoid 3D; max 4 series; title every chart; keep source data on a separate sheet.

---

## 5. Input Requirements

```yaml
excel_engine_input:
  brief: string              # What the workbook is for
  data_source: {type: csv|json|api|manual|existing_xlsx, path_or_query: string}
  model_type: financial_3stmt | dcf | lbo | rab_boq | kpi_dashboard | generic
  requirements: {sheets: [string], formulas_required: [string], charts_required: [string], validations: [string]}
  brand_tokens: {palette: {...}, typography: {...}}
  accessibility_profile: {require_alt_text: bool}
```

**Validation rules:**

- `data_source` MUST be specified; never generate without data or explicit "empty template" request.
- `model_type` MUST map to a known pattern; unknown → generic workbook with user-defined sheets.
- `requirements.formulas_required` MUST use supported functions; unsupported → flag and provide workaround.
- If `existing_xlsx` provided, MUST validate it opens without corruption before modification.

---

## 6. Output Specifications

```yaml
excel_engine_output:
  artifact_path: string      # .xlsx file path
  manifest:
    engine: "excel-engine"
    engine_version: "1.0"
    library_used: openpyxl | xlsxwriter | pandas
    sheets: [{name, purpose, row_count, col_count}]
    formulas_count: int
    formulas_by_type: {financial: int, statistical: int, date: int, lookup: int, other: int}
    charts: [{type, sheet, title}]
    validations: [{sheet, cell_range, type}]
    conditional_formatting: [{sheet, range, type}]
    named_ranges: [string]
    tables: [{name, sheet, ref}]
    brand_tokens_applied: [string]
    formula_audit:
      hardcoded_values: [string]  # Magic numbers that should be named ranges
      circular_references: [string]
      error_literals: [string]     # #REF!, #DIV/0!, #VALUE!, etc.
      precedent_tracing: pass | fail
    recalculation: {full_calc_on_load: bool, calc_mode: auto | manual}
    limitations: [string]
```

**File constraints:**

- `.xlsx` MUST be valid ZIP with `xl/workbook.xml`, `xl/worksheets/sheet*.xml`, `xl/styles.xml`.
- Formulas MUST be stored as formula strings, never as cached values only.
- `calcChain.xml` SHOULD be present for performance; `openpyxl` may not generate it.
- File size SHOULD be < 100 MB; larger requires data splitting or Power Query references.

---

## 7. Formula-Correctness Rules

These rules are MANDATORY for all generated workbooks:

1. **No hardcoded magic numbers.** Every input (tax rate, growth rate, discount rate, unit cost) MUST be in `Assumptions` sheet and referenced by name or cell.
2. **Precedent tracing.** Every formula MUST be traceable to source data; no formula should reference another formula that references a hardcoded value.
3. **Error literal prevention.** NEVER write formulas that produce `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NULL!`, `#NUM!`, `#SPILL!` under normal data conditions.
   - Use `IFERROR` for lookups: `=IFERROR(XLOOKUP(...), "Not Found")`.
   - Guard divisions: `=IF(denominator=0, 0, numerator/denominator)`.
   - Validate inputs before use in formulas.
4. **Circular reference check.** Run dependency analysis before save; flag any circular chains.
5. **Recalculation flags.** Set `fullCalcOnLoad="1"` in `workbook.xml` `calcPr` (`<calcPr calcId="191029" fullCalcOnLoad="1"/>`) to force recalculation when opened.
6. **Number formats.** Apply currency (`$#,##0.00` or `Rp #,##0`), percentage (`0.0%`), date (`dd-mmm-yyyy`) formats consistently.
7. **Text vs number.** Ensure numeric cells are stored as numbers (`cell.value = 123`), not text (`"123"`).

---

## 8. Decision Rules

| Scenario | Decision |
|---|---|
| New workbook with charts/formatting | `XlsxWriter` |
| Modify existing `.xlsx` | `openpyxl` |
| Bulk data from CSV/JSON | `pandas` + `xlsxwriter` |
| Need PivotTable | `openpyxl` (basic) or provide source data + instructions |
| Need Power Query | Write query defs + `POWER-QUERY-SETUP.md` |
| Need VBA macro | Not supported; provide manual instructions |
| Formula uses unsupported function | Provide Excel 2019-compatible alternative (e.g., `INDEX`/`MATCH` instead of `XLOOKUP`) |
| Dynamic array spill needed | Write modern function; warn user requires Excel 365/2021+ |
| File > 50 MB | Split into multiple workbooks or use Power Query external references |

---

## 9. Quality Standards

- **Structure:** Follow sheet ordering convention; `Assumptions` sheet mandatory for models.
- **Formulas:** All formulas MUST pass audit (no hardcoded values, no error literals, no circular refs).
- **Formatting:** Consistent fonts, colors, number formats; brand palette applied.
- **Validation:** Input cells MUST have data validation where appropriate.
- **Documentation:** `README` sheet explains purpose, structure, and usage; `Checks` sheet holds reconciliation formulas.
- **Performance:** Avoid volatile functions (`NOW()`, `TODAY()`, `RAND()`) in large models; prefer `INDEX`/`MATCH` over `VLOOKUP`.
- **Manifest:** Every output MUST include formula audit results and limitations.

---

## 10. Error Handling

| Error | Detection | Recovery |
|---|---|---|
| Corrupt `.xlsx` | `zipfile.BadZipFile` or `openpyxl` `InvalidFileException` | Attempt repair: extract `xl/workbook.xml`, rebuild minimal package; if fails, request clean copy |
| Missing `sharedStrings.xml` | `KeyError` on string cells | Rebuild shared strings table from cell values |
| Formula parse error | `openpyxl` warning or Excel repair prompt | Validate formula syntax; simplify or provide alternative |
| Circular reference | Dependency analysis | Break cycle by converting one formula to value or restructuring |
| Unsupported function | Function not in Excel version | Provide compatible alternative; document version requirement |
| Spill range blocked | `#SPILL!` error | Ensure no non-empty cells in spill path; move blocking content |
| File too large | Memory error | Split workbook; use Power Query external references |
| Data type mismatch | Formula returns `#VALUE!` | Cast inputs with `VALUE()`, `TEXT()`, or `NUMBERVALUE()` |
| Date format issues | Dates stored as text | Convert with `DATEVALUE()` or proper cell formatting |

---

## 11. Practical Examples

### Example A — Simple budget workbook (XlsxWriter)

```python
import xlsxwriter
wb = xlsxwriter.Workbook('budget.xlsx')
ws = wb.add_worksheet('Budget')
header_fmt = wb.add_format({'bold': True, 'bg_color': '#1F4E79', 'font_color': 'white'})
ws.write_row('A1', ['Category', 'Jan', 'Feb', 'Mar', 'Total'], header_fmt)
for i, cat in enumerate(['Salaries', 'Rent', 'Utilities', 'Marketing']):
    row = i + 1
    ws.write(row, 0, cat)
    ws.write_row(row, 1, [10000 + i * 500, 10500 + i * 500, 11000 + i * 500])
    ws.write_formula(row, 4, f'=SUM(B{row+1}:D{row+1})')
chart = wb.add_chart({'type': 'column'})
chart.add_series({'name': 'Monthly Spend', 'categories': ['Budget', 1, 0, 4, 0], 'values': ['Budget', 1, 1, 4, 3]})
chart.set_title({'name': 'Q1 Budget by Category'})
ws.insert_chart('G2', chart)
wb.close()
```

### Example B — RAB/BOQ with formulas (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
wb = Workbook(); ws = wb.active; ws.title = 'BOQ'
headers = ['No', 'Item', 'Unit', 'Qty', 'Unit Price', 'Total']
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
items = [('1', 'Concrete work', 'm3', 100, 1500000), ('2', 'Rebar', 'kg', 5000, 12000), ('3', 'Formwork', 'm2', 200, 85000)]
for row, item in enumerate(items, 2):
    for col, val in enumerate(item, 1):
        ws.cell(row=row, column=col, value=val)
    ws.cell(row=row, column=6, value=f'=D{row}*E{row}')
for i, (label, formula) in enumerate([('Subtotal', '=SUM(F2:F4)'), ('PPN 11%', '=F5*0.11'), ('Grand Total', '=F5+F6')]):
    ws.cell(row=5 + i, column=5, value=label).font = Font(bold=True)
    ws.cell(row=5 + i, column=6, value=formula).font = Font(bold=True)
for col in range(1, 7):
    ws.column_dimensions[get_column_letter(col)].width = 15
wb.save('rab_boq.xlsx')
```

### Example C — KPI dashboard with XLOOKUP and conditional formatting

```python
import xlsxwriter
wb = xlsxwriter.Workbook('kpi_dashboard.xlsx')
ws_data = wb.add_worksheet('Data'); ws_dash = wb.add_worksheet('Dashboard')
ws_data.write_row('A1', ['Month', 'Revenue', 'Expenses', 'Profit', 'Growth %'])
for row, d in enumerate([['Jan',100000,60000,40000,0.05],['Feb',110000,65000,45000,0.10],['Mar',125000,70000,55000,0.136]], 2):
    ws_data.write_row(row, 0, d)
ws_dash.write('A1', 'KPI Dashboard')
ws_dash.write('A3', 'Latest Revenue'); ws_dash.write('B3', '=XLOOKUP("Mar", Data!A:A, Data!B:B)')
ws_dash.write('A4', 'Latest Profit'); ws_dash.write('B4', '=XLOOKUP("Mar", Data!A:A, Data!D:D)')
ws_dash.write('A5', 'Avg Growth'); ws_dash.write('B5', '=AVERAGE(Data!E2:E4)')
profit_fmt = wb.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
ws_dash.conditional_format('B4', {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': profit_fmt})
chart = wb.add_chart({'type': 'line'})
chart.add_series({'name': 'Revenue', 'categories': ['Data', 1, 0, 3, 0], 'values': ['Data', 1, 1, 3, 1]})
chart.add_series({'name': 'Expenses', 'categories': ['Data', 1, 0, 3, 0], 'values': ['Data', 1, 2, 3, 2]})
chart.set_title({'name': 'Revenue vs Expenses'})
ws_dash.insert_chart('D2', chart)
wb.close()
```
---

## 12. Cross-References

- `architecture.md` — Shared context, orchestration rules
- `microsoft-ecosystem.md` — Excel tier-1 capabilities and caveats
- `word-engine.md` — Embedding Excel tables/charts in Word documents
- `powerpoint-engine.md` — Linking workbook data to slide charts

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
