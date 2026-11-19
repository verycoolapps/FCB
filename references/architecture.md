# FileCraftBooster — Architecture

**Document class:** System architecture reference
**Audience:** Skill maintainers, reviewers, and engineers extending FileCraftBooster
**Version:** 1.0

---

## 1. Purpose

This document defines the internal architecture of FileCraftBooster: how a user request is classified, routed to the correct app engine, enriched with shared context, executed, verified, and delivered. It is the authoritative map for every subsystem listed in the module registry.

---

## 2. Scope

Covers: layer model, module map, shared context object, orchestration and fallback rules, hand-off contracts, and state management across multi-app workflows. Does not cover engine internals (see `word-engine.md`, `excel-engine.md`, `powerpoint-engine.md`) or tenant coverage (see `microsoft-ecosystem.md`).

---

## 3. Layer Model

FileCraftBooster is organized as four cooperating layers. No layer may bypass the layer above it except through declared fallback contracts.

```
┌─────────────────────────────────────────────────────┐
│ L0  INTENT ROUTER                                   │
│     Request parsing → classification → routing      │
├─────────────────────────────────────────────────────┤
│ L1  APP ENGINES (primary producers)                 │
│     Word · Excel · PowerPoint · Outlook · Visual     │
├─────────────────────────────────────────────────────┤
│ L2  SHARED SERVICES (cross-cutting)                 │
│     Design system · Licensing · Collab · QA ·       │
│     Accessibility · Security · API integration      │
├─────────────────────────────────────────────────────┤
│ L3  OUTPUT & DELIVERY                               │
│     File write → manifest → verification → handoff  │
└─────────────────────────────────────────────────────┘
```

### Layer responsibilities

| Layer | Owns | Never does |
|---|---|---|
| L0 Intent Router | Classification, ambiguity resolution, clarification prompts | File generation |
| L1 App Engines | Format-specific artifact production and enhancement | Brand decisions without tokens |
| L2 Shared Services | Cross-cutting quality, compliance, and context | Owning a request end-to-end |
| L3 Output & Delivery | Persistence, manifests, verification reports | Content authoring |

---

## 4. Module Map

Every subsystem below is a distinct module with a defined owner layer, input contract, and output contract.

| Module | Layer | Primary inputs | Primary outputs |
|---|---|---|---|
| `intent-router` | L0 | Raw user prompt, attached files, prior context | Classified intent + routed engine + plan |
| `word-engine` | L1 | Brief, audience, tone, length, brand tokens | `.docx` + style manifest |
| `excel-engine` | L1 | Data source, model spec, KPI requirements | `.xlsx` + formula audit report |
| `powerpoint-engine` | L1 | Story arc, slide count, template | `.pptx` + speaker notes + layout report |
| `outlook-engine` | L1 | Recipients, message purpose, calendar intent | Draft `.eml`/HTML, `.ics`, scheduling plan |
| `collaboration` | L2 | Co-author list, file handoffs, comment threads | Shared plan, review checklist, version notes |
| `visual-assets` | L2 | Asset spec (chart, icon, diagram, screenshot description) | SVG/PNG/DrawingML snippet + placement spec |
| `licensing` | L2 | Asset provenance, font names, license register | License audit + attribution block |
| `design-system` | L2 | Brand tokens (palette, type, spacing) | Resolved token sheet per artifact |
| `feng-shui-palettes` | L2 | Element/direction request (optional creative brief) | Color palette recommendation with rationale |
| `cross-app-workflows` | L2 | Multi-artifact request (e.g., deck + workbook + doc) | Orchestrated plan + dependency order |
| `qa` | L2 | Any produced artifact | Validation report (structure, formulas, accessibility) |
| `security` | L2 | Files, links, macros, external references | Risk report; sanitized artifacts where needed |
| `accessibility` | L2 | Document/slide structure, alt text, reading order | A11y checklist + fixes applied |
| `api-integration` | L2 | Microsoft Graph auth state, site/mailbox IDs | Read/write operations against M365 |
| `enhancement` | L1/L2 | Existing artifact + improvement request | Revised artifact + diff notes |
| `advanced-patterns` | L2 | Complex request patterns (mail merge at scale, model linking) | Pattern recipe + execution plan |
| `troubleshooting` | L2 | Error signature, failed artifact | Diagnosis + remediation steps |

---

## 5. Shared Context Object

Every engine invocation receives a `SharedContext` envelope. Engines MUST NOT invent brand, audience, or compliance facts that are absent from this object.

```yaml
SharedContext:
  user_profile:
    name: string
    role: string            # e.g., "FP&A analyst", "HR manager"
    locale: string          # e.g., "en-US", "id-ID"
    preferred_language: string
  brand_tokens:
    palette: {primary, secondary, accent, neutral}[]
    typography: {heading_font, body_font, sizes}
    spacing_scale: number[]
    logo_ref: string | null
  license_register:
    fonts: [{name, license, source}]
    images: [{asset, license, attribution}]
    templates: [{name, license, owner}]
  accessibility_profile:
    standard: WCAG_2_2_AA | Section_508 | internal
    require_alt_text: bool
    require_reading_order: bool
    colorblind_safe: bool
  tenant_context:
    graph_auth: bool
    tenant_id: string | null
    premium_features_available: [string]
  session_state:
    artifacts_produced: [artifact_manifest]
    open_questions: [string]
    fallback_chain_position: int
```

**Rules**

1. `brand_tokens` and `license_register` are read-only once resolved; engines may propose additions but must flag them for L2 review.
2. `accessibility_profile` is mandatory before any visual artifact is written. If absent, `accessibility` module injects the default (WCAG 2.2 AA, alt text required, reading order required).
3. `tenant_context` gates any `api-integration` call. No Graph call may be attempted with `graph_auth: false`.
4. `session_state.artifacts_produced` accumulates manifests; `cross-app-workflows` uses it to detect missing deliverables.

---

## 6. Orchestration Rules

### 6.1 Routing table (L0 → L1)

| Signal in request | Primary engine | Secondary engine |
|---|---|---|
| "document", "report", "letter", "memo", "contract", "proposal" | `word-engine` | `visual-assets` (charts/diagrams) |
| "spreadsheet", "model", "budget", "forecast", "KPI", "RAB", "dashboard" | `excel-engine` | `visual-assets` |
| "deck", "presentation", "slides", "pitch", "board meeting" | `powerpoint-engine` | `visual-assets`, `excel-engine` (embedded data) |
| "email", "reply", "schedule meeting", "calendar invite" | `outlook-engine` | `word-engine` (signature block) |
| "compare files", "merge docs", "combine sheets" | `enhancement` | target app engine |
| "share with team", "collect feedback" | `collaboration` | target app engine |

### 6.2 Fallback chains

Fallbacks are ordered; each hop must be logged in `session_state`.

- **Primary tool unavailable** (e.g., `docxtpl` not installed) → use `python-docx` with post-processing to inject fields → if `python-docx` also fails, emit raw OOXML patch plan for manual application.
- **Brand tokens missing** → `design-system` requests clarification once; if unanswered, use neutral default palette and flag in manifest.
- **Graph auth absent** → `api-integration` switches to file-export mode and produces an offline artifact plus a `.graph-request.json` sidecar describing the intended write.
- **Premium feature required** (e.g., Power BI embedded) → degrade to static artifact (PNG chart + XLSX data) and note the premium gate in the manifest.
- **Corrupt input file** → `troubleshooting` attempts repair (DOCX/ZIP rebuild, XLSX shared-strings recovery); unrecoverable → request a clean copy with a precise error signature.

### 6.3 Hand-off contracts

Every engine-to-engine hand-off passes a typed contract:

```yaml
HandOff:
  from_engine: string
  to_engine: string
  payload:
    artifact_path: string
    manifest_ref: string
    required_inputs: [string]   # e.g., ["chart_png", "speaker_notes"]
    constraints: [string]      # e.g., ["16:9", "brand_palette_v2"]
  acceptance_criteria: [string]
```

Example: `excel-engine` → `powerpoint-engine` for a board deck chart slide. `powerpoint-engine` MUST verify the PNG dimensions match the target placeholder before placement; on mismatch it requests a re-render at the declared aspect ratio.

---

## 7. State Management Across Multi-App Workflows

`cross-app-workflows` owns state for requests that span engines (e.g., "create a budget workbook, a summary memo, and a board deck").

### Workflow state object

```yaml
WorkflowState:
  workflow_id: uuid
  steps:
    - step_id: string
      engine: string
      status: pending | running | done | failed | skipped
      depends_on: [step_id]
      artifact_manifest: string | null
      error: string | null
  shared_context_ref: string
  started_at: timestamp
  completed_at: timestamp | null
```

### Rules

1. Steps execute in dependency order; independent steps MAY run in parallel.
2. A downstream step MUST NOT start until all `depends_on` artifacts exist on disk and pass `qa`.
3. Failure in one step does not abort unrelated branches; the workflow reports partial completion with a clear manifest of what was produced and what failed.
4. `session_state.artifacts_produced` is the single source of truth for "what exists" — engines MUST read it before claiming a file is missing.
5. All state is persisted to `.filecraft/state/<workflow_id>.json` so work can resume after interruption.

---

## 8. Quality Standards

- Every artifact MUST carry a manifest listing: engine version, styles/layouts used, brand tokens applied, license register entries consumed, accessibility checks passed, and known limitations.
- No engine may emit a file without passing through `qa` at least once.
- All fallbacks MUST be recorded; silent degradation is a defect.
- Multi-app workflows MUST produce a consolidated `WORKFLOW-REPORT.md` summarizing deliverables, failures, and recommended next actions.

---

## 9. Error Handling

| Failure class | Detection | Response |
|---|---|---|
| Missing input (no brief, no data) | L0 classification | Clarification prompt; never guess audience or tone |
| Missing dependency (library absent) | Engine import check | Fallback chain (§6.2) then degrade gracefully |
| Corrupt artifact | `qa` structural check | `troubleshooting` repair attempt; else request clean copy |
| License violation risk | `licensing` scan | Block distribution; substitute licensed asset or flag for user decision |
| Accessibility failure | `accessibility` scan | Auto-fix where possible (alt text, heading order); else block and report |
| Graph/auth failure | `api-integration` preflight | Switch to offline mode; emit sidecar request |

---

## 10. Practical Examples

### Example A — Single-engine request

> "Write a one-page project status memo for my manager, formal tone, include a small table of milestones."

1. L0 → `word-engine` (primary), `visual-assets` (table is native Word, no external asset needed).
2. L2 `design-system` resolves brand tokens; `accessibility` sets heading order (Title → Heading 1 → body).
3. `word-engine` produces `.docx` + manifest.
4. `qa` validates heading order, table header row, and page count estimate.
5. L3 writes file, returns path + manifest.

### Example B — Multi-app workflow

> "Build me a Q3 business review: an Excel model with revenue forecast, a 10-slide deck summarizing it, and a 2-page Word memo with key risks."

1. L0 → `cross-app-workflows`; decomposes into 3 engine tasks + 2 hand-offs (Excel chart → deck slide; Excel summary table → Word memo).
2. `excel-engine` produces `.xlsx` first (source of truth).
3. `visual-assets` renders forecast chart PNG from workbook data.
4. `powerpoint-engine` builds deck, embedding chart + speaker notes.
5. `word-engine` writes memo referencing workbook cell ranges (not hardcoded numbers).
6. `qa` verifies: workbook formulas recalc, deck chart matches workbook, memo numbers trace to workbook.
7. L3 emits `WORKFLOW-REPORT.md` + all artifacts.

### Example C — Enhancement of existing file

> "Take this uploaded `.docx` and make it accessible, then export a PDF-ready version."

1. L0 → `enhancement` with target `word-engine`.
2. `accessibility` scans: missing alt text on 3 images, heading levels skipped (H1 → H3).
3. `word-engine` applies fixes: injects alt text, normalizes heading levels, adds table header rows.
4. `qa` re-scans; `licensing` confirms no font violations.
5. Output: revised `.docx` + accessibility report + change log.

---

## 11. Module Registry Cross-Reference

| Module | Reference doc |
|---|---|
| `word-engine` | `word-engine.md` |
| `excel-engine` | `excel-engine.md` |
| `powerpoint-engine` | `powerpoint-engine.md` |
| `microsoft-ecosystem` | `microsoft-ecosystem.md` |
| All others | This document + engine docs |

---

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
