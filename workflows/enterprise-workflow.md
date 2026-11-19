# Workflow: Enterprise Orchestration

**Purpose:** Coordinate multi-application Microsoft 365 deliverables for complex business scenarios — proposals, construction projects, management reporting, education programs, and cross-system automation.

---

## Trigger

Activate when one request spans multiple apps or produces a bundle: "prepare a full proposal package", "set up project documentation for construction", "create monthly management reports", "build course materials", "automate our approval workflow", "migrate/sync data between systems".

## Input

- The business scenario and desired outcome.
- Existing files/data across apps (documents, spreadsheets, emails, meeting notes).
- Stakeholders and their roles.
- Timeline, budget context, compliance requirements.
- Which apps the user actually has access to (do not assume all M365 apps are licensed).

## Preconditions

- Load references: `microsoft-ecosystem.md`, `cross-app-workflows.md`, `microsoft-api-integration.md`, `security-and-privacy.md`, `outlook-engine.md`; plus domain references (document/spreadsheet/presentation standards) per artifact.
- Map the scenario to a named pattern (below) or design a custom orchestration.
- Confirm scope: a bundle of files now vs. a documented automation recipe vs. both.
- Identify the system of record (where truth lives) before creating duplicates.

## Step-by-Step Process

1. **UNDERSTAND** — 12 questions + scenario classification. Identify pattern:
   - **Pattern A — Proposal/Sales:** research → Word proposal → Excel pricing → PPTX pitch → Outlook cover email → (optional) Planner tasks on win.
   - **Pattern B — Project Delivery:** SharePoint/Teams site structure → Planner/Lists task backbone → Excel tracker → Word status reports → Power BI dashboard.
   - **Pattern C — Construction/Engineering:** project charter (Word) → schedule (Project/Excel) → budget model (Excel) → drawings/docs (Visio/Word) → progress reports (PPTX+Word) → RFIs/submittals (Lists/Forms).
   - **Pattern D — Education:** course outline (Word/Sway) → slide deck (PPTX) → worksheets (DOCX/XLSX) → assessments (Forms) → grade tracker (Excel) → communication templates (Outlook).
   - **Pattern E — Management Reporting:** data sources (Excel/Lists/Dynamics) → Power BI dashboard → Word executive narrative → PPTX board deck → Outlook distribution list.
   - **Pattern F — Automation:** trigger (Forms/Excel/email) → Power Automate flow → actions (create doc, notify, update list) → error handling → monitoring.
2. **PLAN** — Produce the orchestration map: artifact list, dependency order, which workflow file handles each, shared assets (logo, palette, data sources), and the single system of record per data type.
3. **FOUNDATION** — Create shared elements first: design system application, master data (Excel/Lists structure), naming conventions, folder structure (SharePoint/OneDrive layout described or scripted).
4. **PRODUCE** — Execute each artifact through its workflow (`document-production`, `spreadsheet-production`, `presentation-production`, `visual-research-workflow`), in dependency order. Reuse licensed assets across artifacts — one `assets/` folder, one attribution register.
5. **CONNECT** — Wire cross-references: document numbers ↔ spreadsheet cells ↔ slide figures must reconcile. If live links aren't possible, document the manual sync points.
6. **AUTOMATE** — Where pattern F or recurring cadence applies: produce Power Automate flow description/JSON skeleton and/or Graph API script outline in `references/microsoft-api-integration.md` style. Never claim a flow is "live" — deliver the recipe + setup steps.
7. **VALIDATE** — Cross-artifact consistency check: names, figures, dates, terminology identical everywhere. Each artifact passes its own QA ladder.
8. **PACKAGE** — `final-delivery-workflow.md` produces one bundle: folder structure + manifest + attribution register + setup guide.
9. **DELIVER** — Summary explaining: what was produced, what needs manual setup (permissions, licenses, connections), what to do first.

## Decision Points

- **Bundle vs. single artifact** → if user asked for "a proposal" deliver the core trio (doc+sheet+deck) only if it serves the ask; don't dump every app.
- **Live integration claims** → never claim SharePoint/Teams/Planner objects were created unless the environment actually did it. Deliver files + step-by-step setup instructions otherwise.
- **Licensing gaps** → if user lacks Power BI/Project/Visio, provide the Excel/Word/PowerPoint equivalents and note the upgrade path.
- **Data conflicts between systems** → declare the system of record; other artifacts reference it, not duplicate editable copies.
- **Scale** → enterprise patterns can produce 10+ artifacts; sequence in waves and confirm if scope balloons beyond the ask.

## Application Routing

All M365 apps per the routing table in `SKILL.md`; the pattern determines the subset. Always prefer the simplest app that satisfies the need (Lists before SharePoint lists-with-code; Excel before Power BI under ~50k rows; Word before Publisher for text docs).

## Execution Rules

- One design system, one palette, one font pair across the entire bundle.
- One attribution register for the whole engagement — merge per-artifact registers at packaging.
- Consistent naming: `EngagementName_ArtifactType_vN.ext` across all apps.
- Every artifact independently passes the 7-level QA ladder; the bundle additionally passes a **consistency audit** (names, numbers, dates, tone).
- Document every manual step the user must perform (creating the Teams channel, connecting the flow, sharing permissions) in a `SETUP.md` inside the bundle.
- No emails/messages/posts sent; drafts and instructions only.

## Validation

- Per-artifact validators (`document_validator.py`) + QA ladder.
- Bundle-level: manifest completeness, naming consistency, figure reconciliation across artifacts, attribution coverage = 100% of assets.
- Setup guide reviewed: every manual step is accurate for the user's stated M365 environment.

## Error Recovery

- **Missing app access** → substitute and document (Excel↔Lists, Word↔Sway, Project↔Excel Gantt).
- **Conflicting source data** → ask one targeted question or pick declared system of record and flag discrepancies.
- **Automation can't be built here** → deliver detailed flow spec + JSON/steps the user imports; never fake a "deployed" flow.
- **Partial failure mid-bundle** → deliver completed artifacts + explicit gap list; never silently drop a component.

## Expected Outputs

- Organized bundle folder: `EngagementName/` with subfolders per app or artifact type.
- `MANIFEST.md` — every file, purpose, version, dependencies.
- `SETUP.md` — manual steps: permissions, connections, imports, first-run checklist.
- `ATTRIBUTION.md` — consolidated asset register.
- `DELIVERY_SUMMARY.md` — what was built, QA sign-off per artifact, limitations, next steps.

---

## Pattern Detail: What Each Produces

### A — Proposal / Sales Package
- `01_Discovery/` — needs-analysis notes (Word) if research was done.
- `02_Proposal/` — main proposal DOCX, pricing XLSX, terms appendix.
- `03_Pitch/` — PPTX deck, one-page leave-behind PDF.
- `04_Cover/` — cover email draft (EML), follow-up sequence notes.
- Reconciliation rule: every price in deck appears identically in workbook and proposal.

### B — Project Delivery Setup
- SharePoint/OneDrive folder tree spec (documented, not created remotely).
- `Tracker.xlsx` — tasks, owners, milestones, RAG status.
- `StatusReport_v1.docx` template + `BoardUpdate_v1.pptx` template.
- `README_Setup.md` — channel/site creation steps for admin.

### C — Construction / Engineering
- Document register (Excel): drawing numbers, revisions, status, location.
- Schedule (Excel Gantt or Project XML outline — deliver `.mpp`-compatible outline CSV + instructions if Project unavailable).
- Budget model (Excel): estimated vs. committed vs. actual, contingency.
- RFI/Submittal/Transmittal templates (Word) + log (Lists/Excel).
- Safety/docs: method statements template, inspection checklists (Forms spec).

### D — Education Program
- Syllabus/course outline (DOCX or Sway spec).
- Slide deck per module; worksheets (DOCX with answer key separated); assessments spec for Forms.
- Gradebook (XLSX): weighted categories, drop-lowest rules documented.
- Parent/student communication templates (email drafts).

### E — Management Reporting
- Data dictionary defining every metric (source, formula, owner, refresh).
- Power BI report spec OR Excel dashboard if BI unavailable — same metrics either way.
- Executive narrative (DOCX, ≤4 pages) + board deck (PPTX, ≤15 slides) — both cite identical numbers.
- Distribution: recipient tiers (exec/management/team) with appropriate detail levels.

### F — Automation Recipe
- Trigger spec: what starts the flow (Forms response, new Excel row, email arrival).
- Actions list: each step with app, operation, data mapping.
- Conditions/branches and error-handling path.
- Deliverable: flow description doc + importable JSON skeleton where feasible + test checklist.
- NEVER claim "deployed" — status is always "recipe ready for import."

## Cross-Pattern Rules

### Shared Foundation (do once, reuse everywhere)
- Brand sheet: logo files, palette hex codes, font names, slide master reference.
- Naming registry: document numbers, project codes, version conventions.
- Data dictionary: canonical field names shared across Excel/Lists/Forms/Power BI.

### System of Record Declaration
For every data type, name ONE authoritative store:
- Tasks → Planner or Lists (pick one).
- Files → SharePoint doc library (pick one library per content type).
- Metrics → Power BI dataset or master Excel (pick one).
- Contacts → Outlook/Excel list (pick one).
All other artifacts reference, never duplicate-edit.

### Reconciliation Checklist (run before delivery)
- [ ] Same figure appears identically across doc/sheet/deck.
- [ ] Dates consistent (report date = data-as-of date).
- [ ] Version numbers aligned (all v1 or all current).
- [ ] Terminology consistent (project name spelled identically).
- [ ] Contact info/branding identical across artifacts.

### Rollout Phasing (for large bundles)
- Phase 1: foundation + system of record + templates.
- Phase 2: core artifacts (proposal/report/deck).
- Phase 3: supporting artifacts (forms, automation, dashboards).
- Phase 4: QA, packaging, delivery.
Deliver in phases if user wants early wins; otherwise single package.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
