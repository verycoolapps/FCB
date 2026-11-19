# Collaboration Engine — OneNote, Teams, OneDrive, SharePoint, Loop, Lists, Planner

## Purpose

The collaboration engine produces Microsoft 365 collaboration artifacts: structured notes, meeting plans, file-organization schemes, document-library schemas, living documents, list schemas, and project plans. It distinguishes two output classes: **generatable artifacts** (templates, schemas, content, naming conventions — produced as files the user imports or pastes) and **live-tenant operations** (actual OneNote page creation, Teams channel provisioning, SharePoint library creation via Microsoft Graph — executed only with authorization and tenant access).

## Scope

In scope: OneNote page/note structures, Teams channel and meeting planning, OneDrive folder conventions, SharePoint library/metadata design, Microsoft Loop component documents, Microsoft Lists schema design, Planner plan/task/bucket design, and the decision rules for choosing which surface fits which artifact.

Out of scope: live tenant mutations without authorization; anything covered by `outlook-engine.md` (email/calendar).

## Artifact Classes — Generatable vs Live-Tenant

| Surface | Generatable artifact | Requires live tenant (Graph) |
|---|---|---|
| OneNote | Page templates (HTML/Markdown → ENEX or paste-ready), section/page naming schemes, tag vocabulary | `POST /me/onenote/notebooks`, page creation, tag application |
| Teams | Channel plans, meeting agenda docs, chat-summary templates, tab layouts | `POST /teams/{id}/channels`, tab installation, meeting creation |
| OneDrive | Folder trees, naming conventions, README/index files | Folder creation via Graph/SharePoint API |
| SharePoint | Content-type schemas, metadata column specs, view definitions | Library/list creation, column provisioning |
| Loop | Component specs (checklist/table/paragraph JSON or paste-ready markup), workspace layouts | Loop workspace/component creation via Graph (`/me/loop`) |
| Lists | Full schema: columns, types, choices, views — as importable CSV/`.list` spec or paste-ready | List creation, item entry |
| Planner | Plan structure: buckets, tasks, labels, due-date rules — as CSV import spec | Plan/bucket/task creation via Graph (`/planner/plans`, `tasks`) |

Default posture: **produce the generatable artifact first**; offer live-tenant execution as an explicit second step requiring authorization.

## Input Specification

```yaml
surface:        # onenote | teams | onedrive | sharepoint | loop | lists | planner | auto
purpose:        # e.g. "onboard the Q4 campaign team"
audience:       # members, roles, org units
constraints:
  tenant_limits:   # e.g. "SharePoint only, no Teams premium"
  naming_rules:    # org conventions to respect
  retention:       # compliance/retention notes
content_seed:   # source material: notes, docs, prior plans
existing_assets:  # URLs/IDs of existing notebooks/sites/plans to extend
scale:          # pages/items/tasks estimate — drives schema choices
```

## OneNote — Page & Note Structure

**Hierarchy:** Notebook → Section Groups → Sections → Pages → Sub-pages. Tags live on pages/sub-pages.

- **Section design:** one section per domain (e.g., `Projects/`, `Meetings/`, `Reference/`, `Archive/`). Avoid >7 top-level sections.
- **Page templates (generatable):** Meeting notes (agenda / discussion / decisions / action items with owner+due), Project brief (objective / scope / milestones / risks / contacts), Research log (question / sources / findings / open items), Daily journal.
- **Tag vocabulary:** standard set — `to_do`, `important`, `question`, `definition`, `contact`, plus project tags. Tags are created per-notebook; define the vocabulary in a `_Tags.md` index page.
- **Naming:** `YYYY-MM-DD — Topic` for dated pages; stable nouns for evergreen pages. Never rename sections casually — links break.
- **Live ops:** page creation uses `POST /me/onenote/pages` with `Content-Type: text/html`; enforce max 1MB/page practical guidance; attachments go to file-storage references, not embedded blobs.

## Teams — Channel Planning & Meeting Workflows

**Structure:** Team → Channels (standard, private, shared) → Tabs (Planner, OneNote, SharePoint, apps) → Posts/Meetings/Files.

- **Channel plan (generatable):** table of channel name, type, purpose, membership, default tab set. Convention: `general` stays clean; topic channels per workstream; `social`/`random` optional.
- **Tabs layout:** standard trio — Planner (tasks), OneNote (notes), SharePoint/Stream (files/recordings). Add channel-specific tabs only when >50% of channel traffic needs them.
- **Meeting agenda template:** purpose → attendees → agenda items (timeboxed) → decisions needed → action items table.
- **Chat/meeting summaries:** post-meeting summary format — decisions / action items (owner, due) / open questions; store in the channel's OneNote tab, link from the meeting recap post.
- **Live ops:** `POST /teams/{team-id}/channels` requires `Channel.Create` + Team install; tabs via `POST /teams/{id}/channels/{id}/tabs`. Requires authorization and `Teamwork.Migrate.All` or delegated consent depending on app type.

## OneDrive — File Organization Conventions

- **Folder tree:** `00-Inbox` (unprocessed), `10-Active/<project>/`, `20-Archive/<year>/`, `30-Templates/`, `90-Private/` (restricted). Numbered prefixes sort correctly.
- **Naming:** `YYYY-MM-DD — Description — vN.ext` for versioned deliverables; kebab-case for folders; no spaces in folder names used in links; avoid `\ / : * ? " < > |`.
- **README/index:** each project folder gets a `README.md` — purpose, owner, status, key links, last-updated.
- **Sharing hygiene:** share links default to "specific people"; never "anyone with link" for internal docs; set expiration on external shares.
- **Live ops:** `POST /me/drive/root/children` for folders; `createLink` for share links. All mutations require authorization.

## SharePoint — Libraries & Metadata

- **Document library design:** one library per content domain; content types for distinct document classes (e.g., `Contract`, `Report`, `Policy`).
- **Metadata columns (generatable spec):** per content type — required columns first, then optional; use managed metadata for controlled vocabularies (departments, document types); date columns with required format; choice columns ≤20 options.
- **Views (generatable):** default view = metadata-ordered; add filtered views per role ("My documents", "Pending review", "This quarter").
- **Content approval & retention:** flag libraries needing approval workflow; retention labels are tenant-policy-driven — document required labels, don't create them.
- **Live ops:** `POST /sites/{site-id}/lists` to create library; column provisioning via `columns` endpoint. Requires `Sites.ReadWrite.All`.

## Microsoft Loop — Living Documents

Loop components: **paragraph, table, checklist, heading, divider, image, divider**. Workspaces are containers; components live in pages.

- **Generatable artifact:** component JSON/markup the user pastes into Loop, or a component spec (`type`, `properties`, `children`) for Graph `POST /me/loop/components`.
- **Use cases:** living meeting notes (checklist for action items, table for decisions), project trackers (table with status/owner/due columns), onboarding hubs (checklists + links).
- **Conventions:** one workspace per project/initiative; name `YYYY-QN — Project`; components < 500 rows per table for performance; every action item gets owner + due column.
- **Live ops:** Loop API is in beta (`/me/loop/workspaces`, `/components`); treat as preview — always deliver paste-ready markup as the primary artifact.

## Microsoft Lists — Schema Design

A List = SharePoint list with typed columns and saved views. Design schema before items.

- **Column types:** single line text, multiple lines, choice (dropdown), person/group, date, number, currency, yes/no, lookup, calculated, hyperlink, image.
- **Schema rules:** ≤ 30 columns per list; choices ≤ 20 options; use lookup instead of duplicating person lists; index columns used in view filters; required only where data must exist.
- **Views:** create per-role views (e.g., `My tasks`, `Overdue`, `By status`) with filters + sort + column subsets — views are generatable specs (`viewType`, `filters`, `sorts`).
- **Import path:** schema spec → user creates list in UI or via Graph `POST /sites/{id}/lists`; items import via CSV or `items` endpoint.
- **Live ops:** `POST /sites/{site-id}/lists` + `columns` + `items`. Authorization required; CSV import is the zero-permission fallback.

## Planner — Plan, Buckets, Tasks, Labels

- **Plan:** one per project/initiative, not per person. Naming: `Project — Phase` or `Team — QN`.
- **Buckets:** stages or workstreams (e.g., `Discovery`, `Build`, `Review`, `Done`); 3–7 buckets; order = sequence.
- **Tasks:** title = verb-first deliverable (`Draft Q3 forecast`, not `Forecast`); assignee required; start/due dates; priority (urgent/high/medium/low); labels 1–3 per task from a plan-level vocabulary.
- **Labels:** plan-level, color-coded, ≤15 total; document vocabulary in plan description.
- **Generatable artifact:** full CSV import spec — columns `Task, Bucket, Assigned to, Start, Due, Priority, Labels, Description` — Planner imports this natively via UI.
- **Live ops:** `POST /planner/plans` → `POST /planner/plans/{id}/buckets` → `POST /planner/tasks`. Requires delegated auth.

## Decision Rules — Which Surface for Which Artifact

| Need | Choose | Why |
|---|---|---|
| Persistent structured notes with tags | OneNote | hierarchical, taggable, offline-capable |
| Team coordination + files + meetings | Teams | channels centralize comms; tabs embed tools |
| Personal/small-team file storage | OneDrive | simpler permissions than SharePoint |
| Org-wide document control, metadata, retention | SharePoint | libraries, content types, DLP, compliance |
| Living, collaboratively-edited document | Loop | real-time co-authoring, portable components |
| Structured item tracking with views/filters | Lists | typed columns, saved views, Power Automate |
| Visual task boards with assignments | Planner | buckets, labels, native Teams/To Do sync |
| Quick task list, no structure | Planner tasks or To Do | lowest overhead |
| Formal document requiring version control | SharePoint library + content approval | audit trail, retention |

Escalation rule: if the artifact needs both structured data AND rich narrative, use SharePoint/Lists for data + Loop/OneNote for narrative, linked together.

## Input Requirements

All fields from the Input Specification, plus surface-specific seeds: existing notebook/site/plan IDs when extending, tenant constraints (e.g., GCC, no external sharing), and compliance notes (retention labels, sensitivity labels required).

## Output Specification

```yaml
artifact_type:    # template | schema | content | plan | convention_doc
deliverables:
  - name:         # e.g. "meeting-notes-template.enex-ready.html"
    format:       # html | md | csv | json | yaml | spec-table
    content:      # or reference to generated file
live_ops_plan:    # optional: ordered list of Graph calls needed, each flagged requires_authorization: true
assumptions:      # inferred constraints
migration_notes:  # how to import into tenant (UI steps or Graph calls)
```

## Error Handling

- **No tenant access:** always deliver generatable artifacts; list required Graph scopes/permissions for the live path.
- **Ambiguous surface:** if purpose fits two surfaces, produce the decision-rule table entry and ask user to pick; default to the simpler surface.
- **Naming conflicts:** if user provides existing assets, fetch/inspect before generating to avoid collisions.
- **Schema errors:** validate Lists columns (type compatibility, choice count, lookup targets exist) before output; Planner CSV is validated against Planner's import format.
- **Permission gaps:** document exactly which Graph permission each live op needs (`Channel.Create`, `Sites.ReadWrite.All`, `Tasks.ReadWrite`); downgrade gracefully to artifact-only output.
- **Beta APIs (Loop):** mark Loop live-ops as preview; primary deliverable is paste-ready markup.

## Practical Examples

**Example 1 — New project onboarding.** Input: surface `auto`, purpose "stand up collaboration for Project Atlas", 8 members. Output: decision-rule picks Teams (channels: `general`, `atlas-build`, `atlas-design`, `social`) + Planner plan (buckets `Discovery/Build/Review/Done`, 23 tasks in CSV import spec) + OneNote meeting-notes template + OneDrive folder tree. Live ops listed as optional Phase 2.

**Example 2 — Compliance document library.** Input: surface `sharepoint`, 4 content types, retention required. Output: library spec with metadata columns (DocType choice, Department managed-metadata, ReviewDate date, Sensitivity choice), 3 saved views, approval workflow note; live library creation deferred pending authorization.

**Example 3 — Meeting notes.** Input: surface `onenote`, weekly ops sync. Output: page template with agenda/checklist/action-items-with-owner sections, tag vocabulary, naming `YYYY-MM-DD — Ops Sync`; paste-ready HTML for quick creation.

**Example 4 — List schema.** Input: surface `lists`, "track vendor contracts". Output: schema — columns ContractName(text,req), Vendor(lookup→Vendors), Value(currency), Start/End(date), Status(choice: Draft/Active/Renewal/Expired), Owner(person); views `My contracts`, `Expiring ≤90d`, `By status`; CSV with 12 sample items.

## Quality Standards

- Every schema validates against the target surface's constraints (column limits, choice counts, type rules).
- Naming conventions are stated once, consistently, and enforced across all artifacts in a bundle.
- Live-tenant operations are never executed without explicit authorization; the artifact-only path must be fully usable standalone.
- Each bundle includes a short "import steps" section so a non-technical user can realize the artifacts.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
