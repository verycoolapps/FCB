# FileCraftBooster — Microsoft 365 Ecosystem Coverage Map

**Document class:** Capability and coverage reference
**Audience:** Skill users planning multi-app deliverables; skill maintainers scoping integrations
**Version:** 1.0

---

## 1. Purpose

This document maps FileCraftBooster's coverage across the Microsoft 365 estate. For every product it states: what FileCraftBooster can produce, plan, or manage; the capability tier; and the availability caveats (tenant requirements, Graph auth, license tier, premium features).

**Honesty rule:** "Awareness only" means FileCraftBooster can discuss, template, or produce offline artifacts related to the product — it does NOT mean live integration exists. Every "Full artifact generation" claim below refers to a local file artifact (`.docx`, `.xlsx`, `.pptx`, `.eml`, `.ics`, `.svg`), not a live tenant write, unless explicitly noted.

---

## 2. Capability Tiers

| Tier | Meaning |
|---|---|
| **T1 — Full artifact generation** | Produces a real, editable file of the native format or a directly usable export. |
| **T2 — Plan & structure** | Produces outlines, templates, configuration guides, or structured data that a human or admin applies. |
| **T3 — Metadata & templates** | Produces metadata files, naming conventions, taxonomy docs, or starter templates. |
| **T4 — Awareness only** | Can explain, advise, or produce tangential artifacts; no direct artifact for the product. |

---

## 3. Coverage Map

### 3.1 Core productivity

| Product | What FileCraftBooster produces / manages | Tier | Caveats |
|---|---|---|---|
| **Word** | `.docx` reports, memos, proposals, contracts, mail-merge letters, accessible documents, tracked-changes-aware edits | **T1** | None for local files. Live co-authoring/comments require Graph auth + SharePoint/OneDrive host. |
| **Excel** | `.xlsx` models, financials, RAB/BOQ, KPI dashboards, data-validation-driven templates, PivotTable-ready datasets | **T1** | Power Query refresh against live sources requires the workbook to be opened in Excel with credentials; FileCraftBooster writes the query definitions, not the live connection. |
| **PowerPoint** | `.pptx` decks, board/training/sales decks, speaker notes, branded templates, embedded charts | **T1** | Morph/Zoom transitions and real-time collaboration require desktop PowerPoint; FileCraftBooster emits standard OOXML transitions. |
| **Outlook** | Email drafts (`.eml`/HTML), calendar invites (`.ics`), signature blocks, mail-merge batches, scheduling plans | **T1** (drafts/invites) / **T2** (send) | Sending requires Graph `Mail.Send` permission or manual send. `.ics` files work in any calendar client. |
| **OneNote** | Section/page outlines exported as `.docx` or `.html`, notebook structure templates, meeting-note templates | **T2** | No native `.one` format generation; output is importable content, not a live notebook. |
| **To Do** | Task-list templates exported as `.xlsx` or `.csv` for import, daily-plan documents | **T3** | No direct Microsoft To Do API; import via CSV or manual copy. |
| **Bookings** | Booking-page requirement docs, staff-schedule templates, service-menu spreadsheets | **T2** | Requires Microsoft 365 Business Premium/Business Standard for live Bookings; FileCraftBooster produces setup artifacts only. |

### 3.2 Collaboration & content

| Product | What FileCraftBooster produces / manages | Tier | Caveats |
|---|---|---|---|
| **Teams** | Meeting agendas, channel-naming conventions, team-charter docs, recap templates, announcement posts (Markdown/HTML) | **T2** | Live channel/post creation requires Graph `ChannelMessage.Send` + Teams admin consent; FileCraftBooster produces content to paste or Graph-post when authenticated. |
| **SharePoint** | Site-structure plans, column-taxonomy docs, document-library templates, `.aspx`-free content packages | **T2** | Site provisioning requires Graph `Sites.ReadWrite.All` + SharePoint admin; FileCraftBooster produces the plan and files, not the live site. |
| **OneDrive** | Folder-taxonomy templates, sync-ready file packages, sharing-policy docs | **T3** | File sync is client-side; FileCraftBooster writes files to a chosen local/OneDrive path. |
| **Loop** | Loop-component content (tables, task lists, decision logs) as `.docx`/`.xlsx` exports compatible with Loop import | **T3** | Loop has no public write API; artifacts are copied into Loop manually. |
| **Lists** | List schemas as `.xlsx`/`.csv` for import, view-configuration docs, Power Automate trigger specs | **T2** | List creation requires Graph `Lists.ReadWrite` or manual UI; FileCraftBooster produces the schema and import file. |
| **Planner** | Plan outlines, task templates, bucket structures as `.csv`/`.xlsx` | **T3** | Planner has limited API (Graph beta); import is manual or via Graph with premium license. |
| **Forms** | Question sets as structured JSON/YAML, quiz logic specs, response-analysis templates | **T2** | Form creation requires Graph `Forms.ReadWrite` (premium); FileCraftBooster produces the question bank and logic, applied via UI or Graph. |
| **Sway** | Narrative outlines, section plans, image-brief docs | **T4** | No Sway API; FileCraftBooster produces the content plan only. |
| **Whiteboard** | Brainstorm templates as `.png`/`.svg` layouts, sticky-note frameworks | **T3** | No programmatic Whiteboard generation; output is a visual reference. |
| **Stream** | Video-storyboard docs, chapter-marker sheets, thumbnail briefs | **T3** | Stream (now Microsoft 365 Video / Clipchamp integration) has no public write API for upload metadata. |
| **Clipchamp** | Storyboard templates, caption scripts, brand-kit specs | **T3** | No Clipchamp API; FileCraftBooster produces pre-production artifacts. |

### 3.3 Data, automation & intelligence

| Product | What FileCraftBooster produces / manages | Tier | Caveats |
|---|---|---|---|
| **Power Automate** | Flow specifications (YAML/JSON definitions), trigger/action catalogs, error-handling patterns, approval-workflow docs | **T2** | Flow *deployment* requires Power Automate premium (per-user or per-flow) and tenant consent; FileCraftBooster produces the definition and implementation guide. |
| **Power Apps** | Canvas-app screen specs, data-source mappings, formula patterns (Power Fx), component libraries | **T2** | App *build* requires Power Apps premium for custom connectors/Dataverse; FileCraftBooster produces specs and Power Fx snippets. |
| **Power BI** | Report-page wireframes, DAX measure libraries, data-model docs, `.pbix`-adjacent Excel datasets | **T2** | `.pbix` generation is not supported (proprietary format); FileCraftBooster produces the semantic model spec, DAX, and source Excel files. Requires Power BI Pro/Premium for publish. |
| **Fabric** | Lakehouse schema docs, notebook outlines (PySpark/SQL), pipeline specs, data-dictionary templates | **T2** | Fabric requires Microsoft Fabric capacity (F SKUs); FileCraftBooster produces code and schemas, not live capacity provisioning. |
| **Dynamics 365** | Entity/field mapping docs, data-import templates (`.xlsx`/`.csv`), workflow specs, report definitions | **T2** | Requires Dynamics 365 license + environment access; FileCraftBooster produces import files and configuration docs. |
| **Azure** | Resource-naming conventions, ARM/Bicep templates for common patterns, cost-estimation spreadsheets, architecture docs | **T2** | Requires Azure subscription + `az` CLI or portal; FileCraftBooster produces IaC templates and docs. |
| **Entra ID** | Group/role-naming conventions, access-review templates, conditional-access policy docs (JSON), guest-lifecycle workflows | **T2** | Requires Entra ID P1/P2 for advanced policies; FileCraftBooster produces policy JSON and docs, applied via Graph/portal. |
| **Microsoft Graph** | Query recipes (`/me/messages`, `/sites/{id}/drive`, `/users/{id}/events`), batch-request patterns, delta-sync strategies, webhook subscriptions | **T2** | Requires app registration + delegated/application permissions; FileCraftBooster produces code and docs, not live tokens. |
| **Microsoft 365 Copilot** | Prompt libraries, Copilot-ready document structures (headings, metadata, alt text), agent-instruction docs, scenario playbooks | **T3** | Copilot requires Microsoft 365 Copilot license; FileCraftBooster produces the content and prompts that Copilot consumes. |

### 3.4 Specialized / legacy

| Product | What FileCraftBooster produces / manages | Tier | Caveats |
|---|---|---|---|
| **Visio** | Diagram specs (shapes, connectors, layers), `.vsdx`-adjacent SVG exports, process-flow docs | **T3** | No native `.vsdx` generation; output is SVG/PNG + spec for manual Visio rebuild. |
| **Access** | Table schemas, query specs (SQL), form/report wireframes, migration docs | **T2** | `.accdb` generation is not supported; FileCraftBooster produces schema docs and SQL. |
| **Project** | WBS outlines, task lists, resource plans as `.xlsx`/`.csv` for import, Gantt-data specs | **T3** | Project has limited API; import is via CSV/XML or manual. |
| **Publisher** | Newsletter/layout specs, brand-template docs, print-ready `.docx`-to-PDF workflows | **T4** | Publisher is desktop-only with no API; FileCraftBooster produces the design spec and content. |

---

## 4. Tier Summary Table

| Tier | Products | Count |
|---|---|---|
| **T1 — Full artifact generation** | Word, Excel, PowerPoint, Outlook (drafts/invites) | 4 |
| **T2 — Plan & structure** | OneNote, Bookings, Teams, SharePoint, Lists, Forms, Power Automate, Power Apps, Power BI, Fabric, Dynamics 365, Azure, Entra ID, Microsoft Graph | 14 |
| **T3 — Metadata & templates** | To Do, OneDrive, Loop, Planner, Whiteboard, Stream, Clipchamp, Copilot, Visio, Project | 10 |
| **T4 — Awareness only** | Sway, Publisher | 2 |

---

## 5. Availability Caveats — Consolidated

### 5.1 Requires live tenant + Graph auth

- Sending Outlook mail, posting Teams messages, creating Lists/Forms/Planner items, provisioning SharePoint sites, writing to OneDrive/SharePoint libraries.
- **Requirement:** Azure AD app registration, admin consent for scopes (`Mail.Send`, `Sites.ReadWrite.All`, `Lists.ReadWrite`, `ChannelMessage.Send`, etc.), client secret or certificate.
- **FileCraftBooster behavior:** If auth absent, produces offline artifact + `.graph-request.json` sidecar.

### 5.2 Requires premium license

- **Power Automate** per-flow/per-user for premium connectors (HTTP, SQL, custom).
- **Power Apps** premium for Dataverse/custom connectors.
- **Power BI** Pro for publish/sharing; Premium for paginated refreshes and AI features.
- **Microsoft Fabric** requires F SKU capacity.
- **Dynamics 365** requires licensed environment.
- **Microsoft 365 Copilot** requires Copilot add-on license.
- **Entra ID P1/P2** for conditional access, PIM, access reviews.
- **Microsoft Bookings** requires Business Premium/Standard.
- **FileCraftBooster behavior:** Detects license tier from tenant context; degrades to static artifacts or documents the premium gate.

### 5.3 Requires desktop client

- PowerPoint Morph/Zoom, real-time co-authoring, tracked changes UI.
- Publisher (no web version).
- Visio (desktop for `.vsdx`; web version has limited API).
- Project (desktop for full features; Project for the web has limited API).

### 5.4 No public API / limited API

- **Loop** — no write API; manual copy.
- **Sway** — no API.
- **Whiteboard** — no programmatic generation.
- **Clipchamp** — no API.
- **Stream** — no public upload-metadata API.
- **To Do** — no public API (use Microsoft Graph `/me/todo` in beta, or CSV import).
- **Planner** — Graph beta only, premium license required.

### 5.5 Format limitations

- `.pbix` (Power BI) — proprietary, not generatable.
- `.vsdx` (Visio) — proprietary, not generatable.
- `.accdb`/`.mdb` (Access) — proprietary, not generatable.
- `.one` (OneNote) — proprietary package format, not generatable.
- `.mpp` (Project) — proprietary, not generatable.

---

## 6. Honest Limitations

1. **FileCraftBooster is not a Microsoft 365 tenant admin.** It cannot provision tenants, assign licenses, or modify tenant-wide settings. It produces artifacts and configuration docs that a licensed admin applies.
2. **No live collaboration.** Real-time co-authoring, comments, and presence require the actual M365 clients; FileCraftBooster produces the content, not the live session.
3. **No proprietary format generation.** `.pbix`, `.vsdx`, `.accdb`, `.one`, `.mpp` are closed formats; FileCraftBooster produces adjacent artifacts (specs, schemas, exports).
4. **Graph calls are opt-in.** Every live write requires explicit user authorization and valid credentials; FileCraftBooster never assumes tenant access.
5. **Premium features are gated.** Where a feature requires a premium SKU, FileCraftBooster documents the requirement and provides a fallback artifact rather than failing silently.
6. **Copilot is a consumer, not a producer.** FileCraftBooster can prepare Copilot-ready content (well-structured docs, metadata, prompts) but cannot invoke Copilot itself.
7. **Version drift.** Microsoft 365 APIs and UI change frequently; FileCraftBooster's Graph recipes and UI instructions are version-pinned and may require updates.

---

## 7. Practical Examples

### Example A — "Make a SharePoint site for our Q3 campaign"

- **Tier:** T2 (SharePoint)
- **FileCraftBooster produces:** Site-structure plan (document libraries, columns, content types), folder taxonomy, template `.docx`/`.xlsx` files, Power Automate flow spec for approval routing, Graph script skeleton for site provisioning.
- **Caveat:** Requires Graph `Sites.ReadWrite.All` + SharePoint admin to execute; FileCraftBooster delivers the plan and files, admin runs the script.

### Example B — "Automate our invoice approval"

- **Tier:** T2 (Power Automate)
- **FileCraftBooster produces:** Flow definition (JSON/YAML), trigger spec (SharePoint list item created), approval-action config, error-handling branches, notification templates.
- **Caveat:** Requires Power Automate premium for HTTP/custom connectors; FileCraftBooster documents the license gate and provides a premium-free fallback using email + SharePoint alerts.

### Example C — "Build a Power BI dashboard"

- **Tier:** T2 (Power BI)
- **FileCraftBooster produces:** Semantic model spec (tables, relationships, measures in DAX), Excel source dataset with proper data types, report-page wireframes, KPI definitions.
- **Caveat:** Cannot generate `.pbix`; user builds in Power BI Desktop using the spec, or FileCraftBooster produces a static Excel dashboard as fallback.

### Example D — "Create a Copilot-ready project brief"

- **Tier:** T3 (Copilot)
- **FileCraftBooster produces:** `.docx` with clean heading hierarchy, metadata fields (author, date, version, tags), alt text on images, a prompt library for Copilot queries against the doc.
- **Caveat:** Requires Microsoft 365 Copilot license to use Copilot features; FileCraftBooster optimizes the document for Copilot consumption.

---

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
