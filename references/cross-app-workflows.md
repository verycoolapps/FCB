# Cross-App Workflows — Canonical Multi-App Orchestrations

## Purpose

Define the four canonical workflows that span multiple Microsoft 365 apps,
specifying per-app deliverables, orchestration order, context passing, naming
and consistency rules, and failure handling. Each workflow produces a coherent
artifact set rather than isolated files.

## Shared Conventions (Apply to All Workflows)

### Context Passing Between Engines

When one workflow engine hands off to the next, it passes a **shared context
bundle**:

```json
{
  "project_id": "PRJ-2026-014",
  "project_name": "Northbridge Office Fit-Out",
  "client": "Acme Corp",
  "brand_tokens": {
    "primary": "#1F4E79",
    "secondary": "#2E75B6",
    "accent": "#C55A11",
    "font_heading": "Calibri",
    "font_body": "Calibri"
  },
  "license_register": "licenses/northbridge-fitout-2026.lic",
  "terminology_glossary": "glossary/northbridge-fitout-2026.gloss",
  "currency": "USD",
  "locale": "en-US",
  "date_format": "YYYY-MM-DD",
  "owner": "aps@company.com"
}
```

Rules:
- Context bundle is created once at workflow start and passed unchanged to
  every engine. No engine mutates it; derived values go into per-app outputs.
- Every generated artifact embeds the `project_id` in its filename and, where
  the format supports it, in document properties (Title, Subject, Company).
- Terminology glossary is generated first if absent, so all engines use
  identical product names, unit conventions, and defined terms.

### Consistency Rules (All Workflows)

- **Naming:** `{project_id}_{deliverable}_{version}.{ext}` e.g.
  `PRJ-2026-014_proposal_v1.docx`. No spaces in filenames.
- **Numbering:** sections numbered `1.`, `1.1`, `1.1.1`; tables `Table 3-1`
  (chapter-table); figures `Figure 2-4`. Numbering is per-document and
  continuous.
- **Cross-references:** internal refs use Word/PowerPoint native fields
  (REF, SEQ), never hardcoded "see page 12."
- **Dates:** all dates ISO `YYYY-MM-DD` in data; rendered format per
  `locale` field.
- **Currency/units:** single currency and unit system per project; no mixed
  units across artifacts.
- **Version labels:** v0.1 draft → v1.0 issued; watermark drafts, remove on
  final.

### Deliverable Manifest Format

Every workflow ends by writing a manifest:

```json
{
  "workflow": "business_proposal",
  "project_id": "PRJ-2026-014",
  "generated_at": "2026-11-19T14:32:00Z",
  "artifacts": [
    {"app": "word", "path": "PRJ-2026-014_proposal_v1.docx", "status": "complete", "pages": 18},
    {"app": "excel", "path": "PRJ-2026-014_pricing_v1.xlsx", "status": "complete", "sheets": 4},
    {"app": "powerpoint", "path": "PRJ-2026-014_pitch_v1.pptx", "status": "complete", "slides": 14},
    {"app": "outlook", "path": "PRJ-2026-014_cover_email.eml", "status": "complete"},
    {"app": "onenote", "path": "PRJ-2026-014_brief.pdf", "status": "complete"}
  ],
  "qa_summary": {"blockers": 0, "majors": 1, "minors": 3},
  "handoff_notes": "Pricing sheet totals verified against proposal Section 5."
}
```

## Workflow A — Business Proposal

**Trigger phrases:** "create a business proposal," "proposal for client,"
"sales proposal with pricing and deck," "end-to-end proposal package."

### Orchestration Order

1. **Intake & context build** — collect client, scope, budget ceiling, brand
   tokens, license register. Generate terminology glossary.
2. **Excel engine first** — build pricing model (items, quantities, unit
   prices, discounts, tax, totals). Rationale: the proposal and deck quote
   numbers; the model is the single source of truth.
3. **Word engine** — proposal document referencing the pricing model's
   computed totals (embed as linked values or static values with a
   reconciliation note).
4. **PowerPoint engine** — pitch deck: problem, solution, pricing summary
   (top-line only), timeline, team, ask. Pulls headline numbers from the same
   model.
5. **OneNote engine (optional)** — project brief notebook: scope, assumptions,
   glossary, open questions.
6. **Outlook engine** — cover email summarizing the package with attachment
   manifest and next steps.
7. **QA + manifest** — run document-quality-assurance across all artifacts;
   emit manifest.

### Per-App Deliverables

| App | Deliverable | Key Content |
|---|---|---|
| Excel | Pricing model | Line items, qty, unit price, discount %, tax, subtotal/total, sensitivity table |
| Word | Proposal doc | Executive summary, scope, approach, pricing section (mirrors model), terms, sign-off |
| PowerPoint | Pitch deck | 10–16 slides; pricing slide shows 3-tier summary only |
| OneNote | Project brief | Scope statement, assumptions log, glossary, decision log |
| Outlook | Cover email | Subject `Proposal — {client} — {project_id}`, body ≤150 words, attachment list, call to action |

### Consistency Rules

- Proposal totals must equal Excel model totals to the cent; deck shows only
  rounded top-line figures.
- All artifacts share `project_id` in filename and document properties.
- Glossary terms used identically across Word and deck.

### Error Handling

- If Excel fails: deliver Word with placeholder-free "pricing to follow"
  section clearly marked `TBD-Pricing` and report partial delivery; do NOT
  invent numbers.
- If deck fails: still deliver proposal + email noting deck pending.
- If email fails: deliver all files plus a `.txt` cover-letter draft in the
  package folder.
- Any artifact marked `status: "failed"` in manifest; `handoff_notes` lists
  what needs regeneration.

## Workflow B — Construction Project

**Trigger phrases:** "construction project documents," "RAB and schedule,"
"BOQ plus progress deck," "contractor document package."

### Orchestration Order

1. **Intake** — project name, location, scope items, labor/material rates,
   schedule horizon, contract type.
2. **Excel engine** — RAB/BOQ workbook: work items, units, quantities, material
   + labor breakdown, unit price, total; plus schedule sheet (or separate
   Project-ready CSV).
3. **Word engine** — contract/SOP docs: scope of work mirroring BOQ items,
   payment terms, HSE SOPs.
4. **PowerPoint engine** — progress deck template: agenda, progress %, issues,
   next milestones.
5. **Planner/Lists engine** — task schema: phases → tasks with assignees,
   durations, dependencies; exported as Planner plan JSON or Lists schema.
6. **QA + manifest.**

### Per-App Deliverables

| App | Deliverable | Key Content |
|---|---|---|
| Excel | RAB/BOQ | Work breakdown, qty takeoff, rate analysis, subtotal per trade, contingency |
| Excel/CSV | Schedule | Tasks, durations, predecessors, Gantt-ready columns (or MS Project import CSV) |
| Word | Contract + SOPs | Scope, deliverables, payment schedule tied to BOQ line refs, safety SOP |
| PowerPoint | Progress deck | % complete, milestone tracker, issue log, lookahead |
| Planner/Lists | Task schema | Plan buckets = BOQ trades; tasks = BOQ line items with owners/dates |

### Consistency Rules

- BOQ line numbers are the primary key: contract scope, schedule tasks, and
  Planner tasks all reference the same BOQ IDs.
- Quantities and rates identical across Excel, Word, and Planner exports.
- Schedule durations sum to contract duration; flag over-runs.

### Error Handling

- BOQ incomplete → deliver schedule and deck with `scope_pending` flags;
  contract marked draft.
- Planner export unavailable → emit Lists-compatible CSV instead; note in
  manifest.
- Rate conflicts (material vs labor source mismatch) → use labor rates from
  intake, flag discrepancies in manifest `handoff_notes`.

## Workflow C — Corporate Management System

**Trigger phrases:** "corporate management documents," "KPI dashboard and
SOPs," "board pack," "policy document suite."

### Orchestration Order

1. **Intake** — entity name, departments, KPI catalog, policy inventory,
   board meeting cadence.
2. **Excel engine** — KPI dashboard workbook: KPI definitions, data tabs,
   computed metrics, chart sheets, drill-down tabs.
3. **Word engine** — SOP/policy documents: one master doc per policy, or a
  consolidated manual with per-policy sections; cross-referenced to KPI IDs.
4. **PowerPoint engine** — board deck: KPI scorecard, risk register, decisions
   required, financial summary.
5. **Planner engine** — recurring plan structure: weekly ops review, monthly
   KPI review, quarterly board; buckets = departments.
6. **Lists engine** — registers: risk register, issue log, action tracker,
   document control register.
7. **QA + manifest.**

### Per-App Deliverables

| App | Deliverable | Key Content |
|---|---|---|
| Excel | KPI dashboard | Definitions, data entry, formulas, charts, threshold flags |
| Word | SOP/policy manual | Numbered procedures, roles/RACI, revision history, KPI links |
| PowerPoint | Board deck | 12–20 slides: scorecard, exceptions, decisions, outlook |
| Planner | Plan structure | Recurring meetings, department buckets, template tasks |
| Lists | Registers | Risk, issue, action, doc-control lists with metadata columns |

### Consistency Rules

- KPI IDs (e.g., `KPI-OPS-001`) appear identically in Excel, Word, deck, and
  Lists.
- Policy numbering scheme `POL-{DEPT}-{NNN}` consistent everywhere.
- Board deck numbers must reconcile with dashboard totals exactly.
- Document control register lists every artifact with version and owner.

### Error Handling

- Missing KPI data → dashboard ships with formula skeletons and `#N/A`-free
  placeholder text `Awaiting data feed`; flagged in manifest.
- Policy conflict (two policies cover same scope) → keep both, add cross-ref
  note, log in `handoff_notes` for human resolution.
- Planner unavailable → emit `.csv` task lists per department.

## Workflow D — Educational System

**Trigger phrases:** "course materials," "syllabus and gradebook," "lecture
package," "class notebook and assessments."

### Orchestration Order

1. **Intake** — course code, title, level, term, learning outcomes, class
   size, assessment weights.
2. **Word engine** — syllabus + lesson plans: outcomes, weekly topics, readings,
   assessment map.
3. **Excel engine** — gradebook/assessment rubric: assignment registry, score
   entry, weighted totals, rubric grids.
4. **PowerPoint engine** — lecture slides per week or per module.
5. **Forms engine** — quiz schema: questions, types (MC/short/essay), point
  values, branching; exported as Forms-compatible structure.
6. **OneNote engine** — class notebook structure: sections per unit, pages per
  lecture, handouts, assignments.
7. **QA + manifest.**

### Per-App Deliverables

| App | Deliverable | Key Content |
|---|---|---|
| Word | Syllabus + lesson plans | Outcomes, schedule, policies, per-session plans |
| Excel | Gradebook + rubrics | Score grid, weighting, formulas, rubric criteria |
| PowerPoint | Lecture slides | Learning objectives, content, examples, checks |
| Forms | Quiz schema | Questions, types, points, answer keys |
| OneNote | Class notebook | Unit sections, lecture pages, resource pages |

### Consistency Rules

- Assessment IDs (`ASM-01`…) map across syllabus, gradebook, Forms, notebook.
- Gradebook weights must sum to 100%; flag if not.
- Quiz questions reference lesson-plan topics by code (`LP-W03-02`).
- All dates aligned to academic term calendar.

### Error Handling

- Gradebook formula errors → deliver static template with instructions;
  manifest flags `formulas_unverified`.
- Forms export unsupported → emit question bank as `.docx` table with
  types/points; note in manifest.
- Missing syllabus data → generate skeleton with `TBD` markers clearly styled
  and listed in `handoff_notes`; never fabricate instructor details.

## Error Handling (Cross-Workflow)

| Condition | Behavior |
|---|---|
| Any engine fails | Continue remaining engines; mark artifact `failed` in manifest; deliver partial package |
| Context bundle invalid | Halt workflow; report missing required fields |
| Naming collision | Append `_v{n}` increment; never overwrite silently |
| QA blocker found | Fix if auto-remediable; else deliver with `qa_summary.blockers > 0` and prominent handoff note |
| User cancels mid-workflow | Write manifest with completed artifacts and `status: "cancelled"` |

## Practical Examples

**Example 1 — Proposal intake:**
User: "Create a business proposal for Acme Corp, $180k budget, include pricing
sheet and pitch deck."
→ Workflow A. Excel model built first with 14 line items; Word proposal
quotes totals `178,450.00 USD`; deck shows `$178k` rounded; Outlook email
drafted with 5 attachments listed.

**Example 2 — Construction package:**
User: "Construction project: 3-storey office fit-out, need RAB, schedule,
progress deck, and contract."
→ Workflow B. BOQ has 86 line items across 6 trades; schedule CSV has 112
tasks with predecessors; contract references BOQ IDs `BOQ-STR-001`…`BOQ-MEP-042`;
Planner export generated per trade bucket.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
