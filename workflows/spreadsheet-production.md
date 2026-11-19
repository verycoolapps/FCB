# Workflow: Spreadsheet Production

**Purpose:** Produce or enhance Excel `.xlsx` workbooks — financial models, budgets, trackers, dashboards, KPI sheets, inventory, schedules, calculators, data analysis files.

---

## Trigger

Activate when numbers, calculations, tracking, or analysis are the core: "make a budget", "build a tracker", "create a dashboard", "model this", "fix this Excel file", "analyze this data".

## Input

- Purpose of the workbook and who will use it.
- Raw data (CSV, pasted tables, existing XLSX) or parameters to model.
- Structure preference: flat table vs. relational sheets vs. dashboard.
- Formatting/branding constraints.
- Refresh cadence (one-off vs. recurring — affects automation notes).

## Preconditions

- Identify workbook type: **data entry** (lists/tables), **calculation** (formulas/models), **report** (formatted output), or **dashboard** (summary + charts).
- Confirm data source: user-provided, researched (cite source), or `[NEEDS INPUT]`.
- Load references: `excel-engine.md` (covers conventions, formulas, financial modeling); add `design-system.md` for styled dashboards.
- Decide sheet architecture before writing a single cell.

## Step-by-Step Process

1. **UNDERSTAND** — 12 questions; lock: workbook type, audience, data availability, size.
2. **ARCHITECT** — Design sheet plan:
   - Data workbooks: `README` / `Instructions` sheet → `Data` (raw, append-only) → `Lookups` → `Output`.
   - Models: `Inputs` (all assumptions, blue-font convention) → `Calculations` → `Outputs` → `Checks`.
   - Dashboards: `Data` → `Calc` → `Dashboard` (charts + KPIs only, no raw edits on dashboard sheet).
3. **DESIGN** — Apply design system: header fills, banded rows, freeze panes, number formats (currency/date/percent with consistent decimals), column widths.
4. **CREATE** — Build via `scripts/spreadsheet_generator.py`. Rules: formulas over hardcoded values; named ranges for key inputs; no volatile functions unless required; protect assumption cells via sheet protection notes (do not password-protect without user key).
5. **DATA** — Import/clean data: trim whitespace, standardize dates, flag duplicates, preserve raw data sheet untouched.
6. **CHARTS/DASHBOARD** — Add charts only where they answer a question; label axes; use consistent color per series; KPI cards for top metrics.
7. **VALIDATE** — Run `scripts/document_validator.py`: formula errors (#REF!, #DIV/0!, #VALUE!), circular refs, broken links, inconsistent formats.
8. **ENHANCE** — Add: instructions sheet, data dictionary, change log, version cell, print setup (landscape, fit-to-width for reports).
9. **DELIVER** — `final-delivery-workflow.md`.

## Decision Points

- **Flat file vs. relational** → relational (lookup sheets) when data repeats (e.g., products, employees); flat when it's a one-off list.
- **Hardcode vs. formula** → always formula for derived values; hardcode only true inputs/constants, visually marked.
- **Dashboard scope** → if user wants "dashboard" but has <20 rows of data, deliver a formatted report sheet + one summary chart; explain why a full BI dashboard isn't warranted (or produce Power BI note).
- **Recurring use** → add an `Automation` note or Power Automate recipe reference; do not build macros unless asked.
- **External data** → if data must refresh from web/SharePoint, document the source and manual refresh steps; never fabricate live connections.

## Application Routing

- **Excel** — primary.
- **Power BI / Fabric** — when visualization scale exceeds Excel (mention as option, don't build without ask).
- **Word** — narrative companion (executive summary) when reporting upward.
- **PowerPoint** — slide-ready chart extraction.
- **Planner / Lists** — when the "spreadsheet" is really task tracking.
- **Power Automate** — scheduled refresh/approval flows.

## Execution Rules

- Every workbook gets an `Instructions` or `README` first sheet when it has >1 sheet or non-obvious logic.
- Inputs are visually distinct (blue font on light fill convention or documented alternative).
- Error handling: wrap lookups in IFERROR with meaningful messages; validate dropdowns via data validation.
- No merged cells inside data ranges; no entire-column formatting; keep under ~100k formula cells for performance.
- Charts: title, labeled axes, legend only when needed, colorblind-safe palette.
- Never include real personal/financial data in examples unless user supplied it.

## Validation

- `document_validator.py`: zero formula errors, no circular references, all sheets protected-as-intended, number formats consistent, charts reference correct ranges.
- Recalculate check: spot-verify 3+ formulas by hand; confirm totals reconcile.
- Open-test: file loads without repair prompt (verify via openpyxl round-trip).
- QA ladder 1–7.

## Error Recovery

- **Corrupt/oversized source file** → extract data to CSV, rebuild clean, report what was dropped.
- **Formula engine unavailable** → deliver formulas as-is + a `README` listing expected values to verify; never paste static values silently.
- **Too much data** → sample + summarize; offer full-data variant.
- **Conflicting requirements** → state interpretation; e.g., "dashboard" requested but data is 12 rows → report + chart + explanation.

## Expected Outputs

- `ProjectName_Workbook_vN.xlsx` with Instructions sheet, clean architecture, validated formulas.
- Optional `.csv` export of key tables; optional `.pptx` chart extract; optional Word narrative.
- Data dictionary + change log inside the workbook.
- Delivery summary with QA sign-off.

---

## Workbook-Type Playbooks

### Budget / Expense Tracker
- Monthly columns or rows consistent; category column locked via data validation.
- Running totals via SUMIFS; variance column = actual − budget with conditional formatting (red/green).
- Receipt attachment note column; totals reconcile to a summary sheet.

### Financial Model
- Three-statement linkage (IS → BS → CF) only when user provides or requests full modeling; otherwise single-purpose model.
- All assumptions on `Inputs` sheet, referenced by name; scenario toggle (Base/Up/Down) via CHOOSE or scenario manager notes.
- Checks sheet: balance sheet balances, cash flow ending = BS cash, no negative heads without flag.

### Inventory / Asset Tracker
- SKU/ID as unique key; stock-in/stock-out transaction log; on-hand = SUMIFS of transactions.
- Reorder-point column with conditional highlight; supplier and location lookup sheets.

### Project / Task Tracker
- Task, owner, start, end, % complete, status dropdown, dependencies (FS/SS notes).
- Gantt via conditional-formatting bar chart (stacked bar trick) when visual timeline needed.

### Dashboard
- KPIs top row (cards or large numbers with trend arrow); charts middle; detail table bottom.
- Every chart answers a named question; no chart without a takeaway.
- Slicers/timeline controls documented in Instructions sheet.

### Calculator / Estimator
- Inputs clearly grouped; outputs protected; formulas visible-on-demand via a `Formulas` mirror sheet or documented in Instructions.
- Sanity bounds: warn via IF() when inputs exceed realistic ranges.

## Formula & Convention Rules

- Named ranges for all key inputs and outputs.
- No nested IF deeper than 3 — refactor with helper columns or IFS/SWITCH.
- Dates: ISO `YYYY-MM-DD` in data, formatted per locale in display; never mixed formats in one column.
- Currency: one currency per workbook unless multi-currency explicitly modeled (then document FX source/date).
- Percentages stored as decimals (0.15) formatted as %; never typed as "15%" text.
- Circular references: forbidden unless intentional iteration — flag and document.
- External links: avoid; if unavoidable, document source and refresh steps.

## Common Failure Modes to Avoid

- Mixed data types in a column (numbers stored as text) → TEXT-to-columns cleanup.
- Hidden sheets containing critical logic → document or unhide.
- #REF! after row inserts → use structured tables or INDEX/MATCH, not fragile cell refs.
- Charts pointing at wrong ranges after edits → re-verify every chart post-build.
- Overflowing text in cells → wrap or widen; never truncate silently.
- Dashboard that requires manual refresh → note refresh steps in Instructions.

## Handoff Notes

- If the workbook feeds a deck or report, list the exact cells/values other artifacts cite.
- If recurring updates expected, include a `Changelog` sheet structure (date, change, author).
- Suggest protection: structure-protect with a documented password the user sets, not one we invent.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
