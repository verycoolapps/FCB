# Outlook Engine — Email Drafting, Rewriting, Scheduling

## Purpose

The Outlook engine turns plain-language intent into publication-ready email artifacts: subjects, bodies, recipient suggestions, follow-up dates, and calendar scheduling proposals. It covers the full Microsoft 365 messaging surface reachable through Microsoft Graph (`/me/messages`, `/me/sendMail`, `/me/mailFolders`, `/me/events`, `/me/calendarView`), the draft-then-review workflow that makes autonomous email production safe, and the template library that keeps tone and structure consistent across cold outreach, follow-ups, requests, apologies, and internal memos.

## Scope

In scope: drafting new emails, rewriting existing drafts for tone/length/clarity, suggesting recipients and CC/BCC sets, proposing follow-up dates, generating meeting requests with timezone-correct proposals, building reusable email templates, and maintaining signature blocks.

Out of scope: sending anything. The engine never calls `POST /me/sendMail` and never creates `/me/events` records without explicit per-send user authorization. See **Hard Rule** below.

## Capabilities

- **Draft generation** — subject line, body, greeting, sign-off from a structured intent spec.
- **Rewrite engine** — tone matrix: formal ↔ casual, persuasive, empathetic, concise, executive summary. Preserves facts and commitments; never invents.
- **Template library** — seven canonical templates plus user-defined variants stored as reusable skeletons with `{{placeholders}}`.
- **Scheduling proposals** — meeting request drafts with timezone handling, duration defaults, buffer rules, and calendar-conflict guidance.
- **Signature blocks** — versioned signature text per context (internal, external, executive, support).
- **Thread awareness** — reads an existing thread (if supplied) and writes a reply-shaped draft (quoting conventions, subject `Re:`).
- **Follow-up scheduling** — proposes a concrete follow-up date relative to send date and priority.

## Hard Rule — Never Send Without Authorization

> **NEVER send email and NEVER create calendar events without explicit user authorization.**

This is non-negotiable and applies at every level:

- The engine's default output is a **draft artifact** (subject + body + recipients + suggested action), not a Graph `sendMail` call.
- `POST /me/sendMail` and `POST /me/events` are permitted only after the user reviews the draft and explicitly says to send/schedule — and even then, prefer writing to `/me/messages` drafts and letting the user hit send, so a human always has the final click.
- Bulk sends, mail-merge campaigns, and auto-follow-up sequences require per-batch authorization.
- If the user's request implies sending ("email John that…"), the correct output is the drafted email plus a one-line "ready to send — confirm recipients and authorize" note.
- The same rule covers calendar: produce an `.ics` file or a described event spec, not a live `/me/events` POST.

## Input Specification

Every generation request is normalized to a structured spec before any writing happens:

```yaml
purpose:        # one line: what the email must accomplish
channel:        # new | reply | forward | meeting_request | follow_up
audience:      # role + relationship: e.g. "procurement manager, new prospect"
relationship:   # cold | warm | existing_vendor | internal | executive_up
audience_count: # 1 | small_group | broad_broadcast
constraints:
  must_include:     # facts, numbers, dates the body MUST contain
  must_avoid:       # topics, phrases, commitments that are forbidden
  deadline:         # when a reply or action is needed
tone:           # formal | casual | persuasive | empathetic | concise
action_required:   # what the recipient should do, and by when
attachments:    # filenames or descriptions to reference
sender_context:    # who is writing, their title, org, signature variant
thread_context:    # optional: prior messages/quoted text for replies
timezone:           # sender's IANA tz, e.g. Asia/Jakarta; recipient tz if known
```

Missing fields are inferred conservatively and flagged in the output's "assumptions" section. Never silently invent facts — if a required fact (price, date, name) is absent, mark it `{{TODO: confirm X}}` rather than fabricating.

## Output Specification

```yaml
subject:            # ≤ 70 chars; no clickbait; includes purpose keyword
body:               # markdown/plain text, greeting → paragraphs → CTA → sign-off
recipients:
  to:               # suggested addresses or roles with rationale
  cc:               # optional, with rationale
  bcc:              # only when confidentiality requires it
follow_up:
  suggested_date:   # concrete date, e.g. "2026-11-26 (7 days)"
  follow_up_body:   # optional short bump draft
assumptions:        # every inferred field, one line each
action_required_from_user: # "review draft" | "confirm recipients" | "authorize send"
metadata:
  template_used:    # template id or "freeform"
  tone_transform:   # original → final tone if rewritten
```

## Template Library

Seven canonical templates. Each is a skeleton with mandatory blocks and optional blocks; placeholders use `{{snake_case}}`.

### 1. Cold Outreach
- **Blocks:** opener (1 line, relevance hook) → credibility (1–2 lines) → value proposition (1 short paragraph) → soft CTA (question, not demand) → sign-off.
- **Rules:** ≤ 120 words body. No attachments on first touch. Subject ≤ 6 words, lowercase-ok, no "Quick question" spam patterns unless audience is warm.
- **Follow-up:** +5 business days, bump adds one new piece of value, never "just checking in" alone.

### 2. Follow-Up (after proposal/meeting)
- **Blocks:** context reference → status recap (3 bullets max) → open questions → next step with date → sign-off.
- **Rules:** restate commitments made; do not re-pitch unless asked.

### 3. Meeting Request
- **Blocks:** purpose (one line) → agenda (3–5 bullets) → proposed windows (2–3 options with tz) → duration → RSVP ask → sign-off.
- **Rules:** always include duration; prefer 2–3 time options over "let me know when works"; for external recipients state both timezones.

### 4. Apology / Service Recovery
- **Blocks:** direct acknowledgment (no hedging) → what happened (facts only) → impact acknowledgment → remedy/compensation → prevention commitment → direct contact offer → sign-off.
- **Rules:** no passive voice ("mistakes were made"); no excessive apology stacking — one sincere apology, then fix.

### 5. Negotiation
- **Blocks:** shared goal framing → position statement (clear, non-adversarial) → rationale (2–3 bullets) → flexibility signal → ask → sign-off.
- **Rules:** never reveal walk-away position; anchor with justification; leave room for counter.

### 6. Internal Memo
- **Blocks:** TL;DR (1–2 lines) → context → details (bullets/tables) → decisions needed → owners + dates → sign-off.
- **Rules:** assume reader is busy — TL;DR must stand alone; decisions and owners in a table.

### 7. Customer Support Response
- **Blocks:** empathy opener → acknowledgment of issue → resolution steps or ETA → prevention/self-help link → escalation path → sign-off.
- **Rules:** mirror the customer's language level; never blame the customer; include ticket/reference number when present.

## Tone Rewriting Matrix

Apply transforms in order: **strip → structure → voice**. Never add facts during tone shifts.

| Target tone | Transform rules |
|---|---|
| Formal | Expand contractions; replace slang; "I" stays but soften imperatives ("Please find attached" → "I am attaching"); full sign-off block; subject line descriptive. |
| Casual | Contractions; short sentences; drop throat-clearing ("I hope this email finds you well"); first-name greeting; emoji only if audience norm allows (never for first contact). |
| Persuasive | Lead with outcome/benefit; social proof one line max; single clear ask; scarcity only if real. |
| Empathetic | Acknowledge feeling/impact before problem-solving; "I understand" once, not repeatedly; offer help before asking for information. |
| Concise | Cut to subject + ≤3 sentences; bullets over prose; remove all pleasantries except greeting/sign-off. |
| Executive | BLUF — bottom line first; numbers and dates prominent; no narrative; decision requested explicitly. |

## Scheduling Etiquette & Timezone Handling

- **Propose, don't dictate:** offer 2–3 windows across different days/times; include duration and timezone for each.
- **Defaults:** 30 min for 1:1s, 60 for workshops, 15 for quick syncs. Add 15-min buffer around external meetings.
- **Timezone rules:** store sender tz (IANA, e.g. `Asia/Jakarta`) and recipient tz if known. Always render times as `Tue 25 Nov, 14:00–14:30 WIB (GMT+7)` — never bare "2pm". When recipient tz unknown, offer windows in sender tz plus one UTC reference.
- **Avoid:** Friday afternoons, Monday 8–9am, lunch hours (12–13 local), and back-to-back stacks >3 hours. Respect declared focus blocks if calendar access exists.
- **Recurring requests:** state the recurrence rule explicitly ("every Tuesday, 4 occurrences") and end date.
- **Output for scheduling:** produce the meeting-request draft AND a structured event spec (`title, start, end, tz, attendees, agenda, location/link`) the user can confirm — not a live event.

## Attachment & Signature Conventions

- **Attachments:** reference by exact filename; note size if >5MB (suggest OneDrive/SharePoint link instead per Microsoft 365 norms). Never claim an attachment exists unless the user supplied one — otherwise write "I will send [X] separately" or omit.
- **Links:** prefer `sharepoint.com`/`onedrive.com` sharing links over attachments for files >2MB or when audience >5 people.
- **Signature blocks:** maintain per-context variants — `internal` (name, title, team, extension), `external` (name, title, company, website, LinkedIn optional, legal footer if required), `executive` (minimal), `support` (includes ticket footer). Signatures are appended verbatim; the engine never paraphrases them. Disclaimers/confidentiality footers apply to external sends automatically when the variant includes them.

## Microsoft Graph Integration Notes

| Operation | Endpoint | Engine behavior |
|---|---|---|
| Read folders | `GET /me/mailFolders` | List/choose target folder for draft filing |
| Read messages | `GET /me/messages` or `/me/mailFolders/{id}/messages` | Fetch thread context for replies; never bulk-scrape without purpose |
| Create draft | `POST /me/messages` | **Preferred write path** — creates editable draft user reviews |
| Send | `POST /me/sendMail` or `POST /me/messages/{id}/send` | **Requires explicit authorization**; prefer user clicks send on the draft |
| Events | `GET/POST /me/events`, `/me/calendarView` | Read conflicts for scheduling proposals; create only with authorization |

Auth: delegated `Mail.ReadWrite`, `Mail.Send` (send only with auth), `Calendars.ReadWrite`. Handle `401` → re-auth prompt; `403` → scope missing, downgrade to draft-only mode.

## Error Handling

- **Auth failure (401/403):** stop, report missing scope, continue in draft-only mode (no Graph writes at all).
- **Throttling (429):** honor `Retry-After`; exponential backoff max 3 retries; batch reads; never hammer `/me/messages` for context — fetch at most the last 10 messages of a thread.
- **Recipient validation:** flag malformed addresses, internal-vs-external domain mismatch (warn when external recipient appears in an "internal" template), and missing recipients — never guess an address.
- **Missing facts:** emit `{{TODO: …}}` placeholders rather than fabricating; list every placeholder in `action_required_from_user`.
- **Ambiguous intent:** if purpose/audience is unclear after one clarifying pass, produce two variants (e.g., formal + concise) and ask which direction.
- **Attachment claimed but absent:** rewrite sentence to a future-send promise or remove claim; flag in assumptions.

## Practical Examples

**Example 1 — Cold outreach.** Input: purpose "introduce our audit tool to a mid-size manufacturer", audience "Ops Director, cold", tone "formal". Output: subject `Reducing unplanned downtime — 20-min look?`, ~110-word body, CTA is a question, follow-up +5 business days with value-add bump, `action_required_from_user: review draft + confirm recipient address`.

**Example 2 — Reply rewrite.** Input: existing thread where user wrote an angry reply; target tone "empathetic", preserve the refund commitment. Output: rewritten body acknowledging impact first, refund stated identically, apology once, escalation contact offered. Subject unchanged `Re: …`.

**Example 3 — Meeting request.** Input: purpose "Q3 roadmap review", duration 45 min, sender `Asia/Jakarta`, recipient likely US Eastern. Output: draft with agenda bullets, windows `Wed 24 Nov 10:00–10:45 WIB (Wed 24 Nov 22:00 EST prev-day? — verify)` — engine renders each option in both zones, flags the date-line crossing, proposes event spec for user confirmation.

**Example 4 — Error path.** Graph returns 429 mid-thread-read: engine retries per `Retry-After`, proceeds with whatever context loaded, notes in assumptions "thread history partial — verify facts before send".

## Quality Standards

- Every draft must pass: purpose achieved in first 2 lines, single CTA, no invented facts, tone consistent start-to-finish, sign-off matches sender_context variant.
- Subject lines: no ALL CAPS, no excessive punctuation, ≤70 chars, reflects content not hype.
- Reply drafts preserve `Re:`/`Fwd:` subject conventions and quote the minimum necessary prior text.
- All scheduling output is a proposal artifact until authorized.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
