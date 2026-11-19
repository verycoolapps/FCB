# Microsoft API Integration

## Purpose

This document describes how FileCraftBooster integrates with Microsoft 365:
the Microsoft Graph API for tenant data and services, and the Office.js
add-in model for document-level automation. It defines exactly what the
skill can do autonomously, what requires the user's authenticated session,
and what must degrade gracefully into artifact generation plus step-by-step
instructions.

The honesty rule is absolute: the skill never pretends to send an email,
move a file, or publish to SharePoint unless a real authenticated session
exists. When credentials are absent, the deliverable is a ready-to-use
file (CSV, EML/MIME skeleton, JSON payload, instruction sheet) plus
precise manual steps.

## Scope

- Microsoft Graph REST API v1.0 (and where `beta` differs)
- OAuth 2.0 flows: delegated auth-code + PKCE, device code, client credentials
- Entra ID (Azure AD) app registration and consent
- Token acquisition, refresh, caching, and expiry handling
- Office.js add-in model: task panes, `Office.context`, bindings
- App-specific JavaScript APIs for Excel, Word, PowerPoint
- Capability detection and graceful fallback
- Throttling, error taxonomy, pagination, delta queries

Out of scope: publishing an Office add-in to AppSource or registering a
production multi-tenant app — those are documented as manual procedures.

## Capabilities

| Capability | Offline? | Requires live tenant? | Notes |
|---|---|---|---|
| Generate document artifacts | Yes | No | Primary deliverable path |
| Build Graph request scripts/payloads | Yes | No | Python `requests` or PowerShell snippets |
| Send mail via Graph | No | Yes — delegated token | Fallback: `.eml` draft + instructions |
| Read mailbox/calendar/drive | No | Yes | Fallback: export scripts user runs |
| Office.js in-document automation | No | N/A | Only inside Office hosts; emits `.js` + manifest |
| Bulk transforms from exports | Partial | No | Works on exported CSV/JSON files |

## Microsoft Graph Overview

### API versions

- `https://graph.microsoft.com/v1.0` — production, supported, recommended.
- `https://graph.microsoft.com/beta` — preview, can change without notice.
  Use only when a needed property exists only in beta; warn the user and
  pin the exact beta surface used.

### Common resource families

- `GET /me` — signed-in user profile (`displayName`, `mail`, `id`)
- `GET /me/messages`, `POST /me/sendMail` — mailbox read and send
- `GET /me/mailFolders`, `GET /me/calendarView`, `POST /me/events`
- `GET /me/drive`, `GET /me/drive/root/children`,
  `PUT /me/drive/items/{id}/content`
- `GET /sites`, `GET /sites/{site-id}/drive` — SharePoint sites and drives
- `GET /teams`, `GET /teams/{id}/channels` — Microsoft Teams
- `GET /me/planner/tasks`, `GET /planner/plans` — Planner
- `GET /me/onenote/notebooks`, `GET /me/todo/lists` — OneNote, To Do
- `GET /users/{id}`, `POST /users` — directory operations (admin scopes)

### Pagination

Collections are paged. Request with `$top` (max ~999 for messages, smaller
for some resources) and follow `@odata.nextLink` verbatim — the URL is
opaque; never construct page URLs manually.

```
GET /me/messages?$top=50&$select=subject,receivedDateTime&$orderby=receivedDateTime desc
→ response contains @odata.nextLink with $skiptoken=...
```

Loop until `@odata.nextLink` is absent. Record page count for transparency.

### Delta queries

For change tracking use `/delta`:

```
GET /me/mailFolders/{folderId}/messages/delta
GET /me/drive/root/children/delta
GET /users/{id}/events/delta
```

Store the returned `@odata.deltaLink` for the next incremental sync. Deleted
items carry a `@removed` annotation. This is the correct pattern for
scheduled export jobs; avoid full re-reads on large mailboxes.

## Authentication Flows

### Delegated permissions — auth code + PKCE (interactive)

Best for user-context operations (`/me/*`, `Mail.Read`, `Files.ReadWrite`,
`Calendars.ReadWrite`). PKCE is mandatory for public clients.

1. **App registration** (Entra portal → App registrations → New):
   name it (e.g. `FileCraftBooster Connector`), choose single- vs
   multi-tenant, set redirect URI (`http://localhost` for CLI, or the
   add-in's task-pane URL for Office.js).
2. **API permissions**: add Microsoft Graph *delegated* permissions
   (`Mail.Send`, `Files.Read.All`, `Sites.Read.All`, `Calendars.ReadWrite`).
   Adding a permission does not grant consent — consent must still be
   completed per tenant.
3. **Authorize**:
   ```
   GET https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
     ?client_id={app-id}&response_type=code
     &redirect_uri={redirect}
     &scope=https://graph.microsoft.com/Mail.Send offline_access
     &code_challenge={s256(verifier)}&code_challenge_method=S256
     &state={csrf-token}
   ```
4. **Exchange code** at `/oauth2/v2.0/token` with `code_verifier`.
5. Response includes `access_token` (~60–90 min) and `refresh_token`
   (~90 days rolling when `offline_access` is granted and used).

### Client credentials (daemon / app-only)

For unattended scenarios: mail ingestion, SharePoint bulk export, Teams
channel sync. Uses *application* permissions and requires admin consent.

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
  grant_type=client_credentials
  client_id={app-id}
  client_secret={secret}
  scope=https://graph.microsoft.com/.default
```

Never ship a client secret inside a skill package. Require it via
environment variable or prompt; never persist it in generated artifacts.

### Device code flow

For headless machines: request a device code, show the user
`verification_uri` + `user_code`, poll the token endpoint until approved.

```
POST /{tenant}/oauth2/v2.0/devicecode
  client_id=...&scope=...offline_access
→ { device_code, user_code, verification_uri, expires_in, interval }
```

### Token lifecycle

- Decode `exp` from the JWT; refresh when within 5 minutes of expiry.
- On 401: attempt one refresh, then one retry; on second 401, stop and
  require re-authentication.
- Cache tokens per (tenant, client_id, scope-set) for the process lifetime.
- Never log tokens or include them in output artifacts.

### Entra ID app registration checklist

1. Portal → Microsoft Entra ID → App registrations → New registration.
2. Record Application (client) ID and Directory (tenant) ID.
3. Authentication blade: configure platform (SPA for Office task panes,
   Web for confidential clients, Public client for PKCE).
4. API permissions → Microsoft Graph → Delegated or Application → add scopes.
5. Grant admin consent when application permissions are used.
6. Certificates & secrets → New client secret; note expiry (max ~24 months).

## Office.js Add-in Model

Office.js runs inside Word, Excel, and PowerPoint hosts. Two layers:

- **Task pane**: an HTML page in a side pane. `Office.onReady()` waits for
  host readiness before calling host-specific APIs.
- **Document bindings**: `Office.context.document.bindings` link regions of
  the document to named data; `getDataAsync()`/`setDataAsync()` sync values.
  Bindings survive edits better than raw range addressing.

Minimal skeleton:

```js
Office.onReady((info) => {
  if (info.host === Office.HostType.Excel) { /* Excel.run(...) */ }
  if (info.host === Office.HostType.Word)  { /* Word.run(...) */ }
  if (info.host === Office.HostType.PowerPoint) { /* PowerPoint.run(...) */ }
});
```

FileCraftBooster delivers generated add-ins as:
1. `manifest.xml` (valid Office Add-in manifest)
2. `taskpane.html` + `taskpane.js`
3. Ribbon command definitions if needed
4. `README-INSTALL.md` with sideloading steps (Insert → Add-ins → My Add-ins
   → Upload My Add-in)

Generated add-ins must declare appropriate `ReadWriteDocument`/`ReadDocument`
grants and include a graceful "run outside Office" message.

## App-Specific JavaScript APIs

### Excel JavaScript API

```js
await Excel.run(async (context) => {
  const sheet = context.workbook.worksheets.getActiveWorksheet();
  const range = sheet.getRange("A1:D10");
  range.load("values,formulas,numberFormat");
  await context.sync();
  // modify values / formulas / numberFormat ...
  await context.sync();
});
```

Patterns to generate: bulk read/write (always batch via `context.sync()`,
never per-cell syncs), named ranges, table objects (`workbook.tables`),
chart insertion, conditional formatting, freeze panes.

### Word JavaScript API

```js
await Word.run(async (context) => {
  const body = context.document.body;
  body.insertText("...", "Start");
  const range = body.getRange("...");
  range.font.bold = true;
  await context.sync();
});
```

Patterns: search-and-replace via `body.search()`, style application,
content controls, headers/footers. Check `document.changeTrackingMode`
before editing — warn when track changes is on.

### PowerPoint JavaScript API

```js
await PowerPoint.run(async (context) => {
  const slide = context.presentation.slides.getItemAt(0);
  slide.shapes.load("items");
  await context.sync();
  // add text boxes, images, tables; set layouts
});
```

Patterns: deck-wide restyle (theme colors, fonts), slide duplication,
batch text replacement across shapes, notes-page text.

## Capability Detection

Run detection in this order before any live action:

1. **Host check** — `typeof Office !== "undefined" && Office.onReady`.
   If absent, Office.js features are impossible; produce artifacts +
   instructions instead.
2. **Graph reachability** — only when the user supplied/consented
   credentials: `GET /me` with a 10-second timeout. Success → record
   `displayName`, `mail`, `id` for the session. Failure → classify by
   status and degrade.
3. **Permission probe** — `GET /me/mailFolders/inbox?$top=1` distinguishes
   "authenticated" from "missing Mail.Read consent" (403).
4. **Feature negotiation** — `GET /me?$select=id` proves v1.0; if a
   beta-only field is needed, query `https://graph.microsoft.com/beta/me`
   once and warn.

Decision rule: if any required scope is missing, do NOT partially execute.
Produce the offline artifact and a "grant these permissions" checklist.

## Throttling and Rate Limits

Graph returns `429 Too Many Requests` with `Retry-After` (seconds) and
`request-id`/`client-request-id` headers for support tickets.

Handling rules:

- Honor `Retry-After` exactly; if absent, exponential backoff:
  `delay = min(2^attempt * 1s, 60s)` with ±20% jitter, max 5 retries.
- Batch independent requests via `POST /$batch` (up to 20 per call).
- Reduce `$top` for broad queries; prefer `$filter`/`$select` to shrink
  payloads.
- For mail/calendar scans, use delta queries or `receivedDateTime ge`
  filters instead of full mailbox reads.
- Keep ≤4 concurrent requests per app registration per mailbox; Graph
  throttles per-app/per-user/per-tenant.

## Error Taxonomy

| Status | Meaning | Response |
|---|---|---|
| 400 | Malformed request / invalid filter | Fix query; surface `error.message` verbatim |
| 401 | Token missing/expired/invalid | Refresh once, retry once; then require re-auth |
| 403 | No consent/permission, or policy denied | Show required scope + admin-consent URL: `https://login.microsoftonline.com/{tenant}/adminconsent?client_id={id}&scope={scopes}` |
| 404 | Resource not found / wrong ID format | Validate ID (GUID vs UPN vs path); check `/me` vs `/users/{id}` |
| 405 | Method not allowed | Check endpoint verb (`sendMail` is POST-only) |
| 409 | Conflict (e.g., event exists) | Surface `error.code`; usually user-actionable |
| 429 | Throttled | See Throttling section |
| 500/502/503/504 | Service-side | Retry with backoff (3 attempts); report `request-id` |
| 507 | Quota exceeded | Report; no retry helps |

Graph error body shape:

```json
{ "error": { "code": "ErrorAccessDenied",
             "message": "Access is denied...",
             "innerError": { "date": "...", "request-id": "...",
                             "client-request-id": "..." } } }
```

Always extract `error.code` and `error.message`; include `request-id` in
user-facing reports so tenant admins can trace.

## Input Requirements

- **Offline mode**: source file(s) to enhance, user intent, optional brand
  spec (colors, fonts, logo path). No credentials needed.
- **Live Graph mode**: tenant ID, app credentials (client secret via env
  var/prompt, never pasted into files), granted scopes, target resource
  identifiers (folder IDs, site URLs, event subjects).
- **Office.js mode**: a host document plus generated add-in files;
  installation is a manual step by the user.

## Output Specifications

- `auth/graph_client.py` or `scripts/msgraph.ps1` — reusable client with
  token refresh, retry, and pagination helpers.
- `payloads/` — ready JSON bodies for sendMail, event creation, file upload.
- `exports/` — CSV/JSON results when running against a live tenant.
- `addins/` — manifest.xml + taskpane files + install instructions.
- `INTEGRATION-REPORT.md` — what ran live vs. generated offline, scopes
  required, and manual follow-up steps.

## Decision Rules

- No credentials → always offline artifact path. Never fake a send.
- `Mail.Send` scope present + user confirms recipient/content → live send
  permitted; otherwise produce `.eml` draft.
- Application permissions requested → require explicit admin-consent step;
  warn that app-only mail send needs `Mail.Send` application permission and
  an Exchange application access policy.
- Beta API needed → use it, flag `BETA` in the report, prefer v1.0
  equivalents where they exist.
- Pagination >50 pages → preview first pages, then full export only on
  confirmation (size guard).

## Practical Examples

**Example 1 — draft a status email from a DOCX (offline):**
Extract body text → summarize → write `status-email.eml` with headers
(`To:`, `Subject:`, `MIME-Version`) → instruct user to open in Outlook or
paste into Outlook Web. No Graph call attempted.

**Example 2 — scheduled mailbox export (live):**
Delta query `GET /me/mailFolders/inbox/messages/delta?$top=100` → write new
items to `mail-export.csv` → save `@odata.deltaLink` to `sync-state.json` →
next run resumes incrementally.

**Example 3 — Excel add-in applying corporate formatting:**
Generate `manifest.xml` + `taskpane.js` calling `Excel.run` to set theme
colors, number formats, and freeze panes on the active sheet. Deliver with
sideload instructions; verify `Office.context.requirements.isSetSupported`
before running.

**Example 4 — SharePoint document library listing (live, read-only):**
`GET /sites/{hostname}:/sites/{name}:/drive/root/children` → paginate →
CSV of name, size, lastModified, webUrl. Falls back to a Graph PowerShell
script if no token is available.

## Quality Standards

- Every generated script must include: timeout, retry with backoff, token
  refresh, and `--dry-run` mode printing requests without executing.
- Secrets appear only as env-var references (`$env:FCB_CLIENT_SECRET`),
  never literal values.
- Reports distinguish three states per action: `EXECUTED`, `GENERATED`
  (artifact ready), `MANUAL` (instructions provided).

## Error Handling

- Authentication failure → produce `auth-setup.md` with portal steps and
  the exact scope list.
- 403 on a specific resource → narrow the scope request or pick a
  different endpoint (`/me/drive` vs `/sites` for the same file).
- Partial failure mid-export → write checkpoint (deltaLink / skiptoken) so
  the job is resumable; report completed vs. remaining counts.
- Office.js outside host → emit a warning banner in generated HTML plus
  fallback: a `.js` file the user can run via Script Lab.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
