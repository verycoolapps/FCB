# Workflow: Document Production

**Purpose:** Produce or enhance Word `.docx` documents and companion `.pdf` files — reports, proposals, letters, memos, contracts, resumes, manuals, meeting minutes, invoices.

---

## Trigger

Activate when the primary deliverable is a narrative document: "write a report", "create a proposal", "draft a letter", "make a PDF", "improve this Word file", "format this document".

## Input

- Topic, purpose, audience, and any source content from the user.
- Existing `.docx`/`.pdf`/text to enhance (optional).
- Brand constraints: colors, fonts, logo, template (optional).
- Data or tables to embed (optional — if heavy data, consider producing an `.xlsx` companion).
- Length target (pages or words) and deadline.

## Preconditions

- Determine output language (default: match user).
- Confirm audience tier (executive / client / student / internal / public) — drives tone per `references/outlook-engine.md`.
- Decide companion artifacts: spreadsheet for data, deck for executive summary (only if it adds value — do not pad scope).
- Load references: `word-engine.md`, `design-system.md`, `accessibility.md`; add `outlook-engine.md`, `feng-shui-design.md`, `security-and-privacy.md` when applicable.

## Step-by-Step Process

1. **UNDERSTAND** — Run the 12 recognition questions. Lock: document type, audience, purpose, length.
2. **PLAN** — Choose structure template:
   - Report: Title → Executive summary → Context → Findings → Analysis → Recommendations → Appendix.
   - Proposal: Cover → Executive summary → Problem → Solution → Approach → Timeline → Pricing → Terms → Acceptance.
   - Letter/Memo: single-page or short-form conventions per `outlook-engine.md` / `word-engine.md`.
   - Contract: parties → recitals → definitions → terms → signatures (flag that this is a template, not legal advice).
3. **DESIGN** — Select design system; set styles (Heading 1–3, Body, Caption, Quote) before writing content. Define palette, fonts, margins (2.54 cm default, 2 cm for dense reports), page numbers, header/footer.
4. **RESEARCH** — Gather facts via web search or user-provided data. Every image: run `visual-research-workflow.md`. Every statistic: needs a source or `[NEEDS INPUT]`.
5. **CREATE** — Generate via `scripts/document_generator.py` (preferred). Structure the script call: styles → sections → content blocks → tables → images → headers/footers → metadata.
6. **ENHANCE** — Add: table of contents (if >4 sections), cross-references, captions, footnotes/citations, tracked-changes-ready clean text, document properties (title, author, subject).
7. **PDF companion** — If requested or distribution implies print, run Word print-to-PDF export or produce print-ready layout; verify page breaks.
8. **VALIDATE** — Run `scripts/document_validator.py` + 7-level QA ladder.
9. **DELIVER** — Hand off to `final-delivery-workflow.md`.

## Decision Points

- **Length vs. depth conflict** → flag it; propose cutting sections or splitting into two documents; proceed with stated interpretation.
- **Data-heavy request** → embed summary table in doc + produce `.xlsx` companion rather than a 40-page table dump.
- **Contract/legal** → include disclaimer: "template only; not legal advice; have counsel review."
- **Confidential content** → apply `security-and-privacy.md`; add handling note in delivery summary.
- **Existing file provided** → diff-improve mode: preserve structure unless user asked for restructure; never silently reformat a legal document.

## Application Routing

- **Word** — primary artifact.
- **Excel** — companion data, mail-merge lists, embedded financial tables.
- **PowerPoint** — executive summary deck when audience is leadership.
- **Outlook** — delivery email draft (do not send).
- **PDF** — export for print/distribution.
- **OneNote** — source research clipping if user uses it.

## Execution Rules

- Always write to a new versioned filename; never overwrite the user's original.
- Use real styles, not direct formatting — every heading must be a Heading style for accessibility and TOC generation.
- Tables must have header rows marked; avoid merged-cell chaos; keep to ≤6 columns unless landscape.
- Images: only licensed assets with attribution; meaningful alt text.
- No lorem ipsum, no `[insert here]` in delivered files — use `[NEEDS INPUT: ...]` markers only when blocking, and disclose them.

## Validation

- `document_validator.py`: opens cleanly, all styles resolve, TOC fields present, images have alt text, no broken hyperlinks, metadata set.
- Manual check: read first and last page render; verify page numbers; confirm no text overflow in tables.
- QA ladder levels 1–7; security tier if sensitive.

## Error Recovery

- **Script fails** → retry once with diagnostics; fall back to manual construction; report.
- **Missing facts** → skeleton + `[NEEDS INPUT]` list; offer regeneration.
- **License unverifiable** → substitute shape/icon/diagram; disclose.
- **Cannot produce PDF** (no LibreOffice/Word) → deliver `.docx` + note the export step.

## Expected Outputs

- `ProjectName_DocumentType_vN.docx` (primary).
- `ProjectName_DocumentType_vN.pdf` (if requested/needed).
- Optional companion `.xlsx` / `.pptx`.
- Attribution register entry for every asset.
- Delivery summary with QA sign-off.

---

## Document-Type Playbooks

### Report / Analysis
- Lead with the answer, not the method. Executive summary ≤ 1 page.
- Charts/figures numbered sequentially (`Figure 1`, `Table 2`) and referenced in text.
- Appendix holds raw data, methodology, and full source list.

### Proposal
- Mirror the client's language and evaluation criteria when provided.
- Pricing/terms section must be unambiguous: what's included, what's excluded, payment schedule, validity period.
- Include acceptance/signature block when the proposal expects signature.

### Letter / Memo / Notice
- One page unless complexity demands more.
- Reference line ("Re:") for memos; full address block for formal letters.
- Clear ask or decision requested within the first third.

### Resume / CV
- Reverse-chronological; quantified bullets ("reduced X by Y%").
- Single column unless design system calls for two; ATS-safe fonts if digital submission likely.
- No photo, age, marital status, or national ID unless country convention requires.

### Contract / Legal Template
- Numbered clauses; defined terms capitalized consistently.
- Signature/notary blocks; effective-date clause; entire-agreement clause.
- Mandatory disclaimer in delivery summary: "template only — not legal advice."

### Invoice
- Seller/buyer blocks, invoice number (sequential suggestion), date, due date, line items, tax lines, totals, payment instructions, late-fee clause if applicable.

### Meeting Minutes
- Attendees, agenda items, decisions (owner + date), action items table (task/owner/due), next meeting.
- Circulate-as-draft note; never present minutes as final without chair approval.

## Formatting Standards Quick Reference

| Element | Standard |
|---|---|
| Body font | 11pt Calibri/Arial or design-system equivalent |
| Heading scale | H1 16–18pt, H2 13–14pt, H3 12pt bold |
| Line spacing | 1.15–1.5 for reports; single for dense docs |
| Margins | 2.54 cm default; 2 cm dense; 3 cm formal |
| Page numbers | Bottom-right, "Page X of Y" for formal docs |
| Colors | 1 accent + neutrals; links styled consistently |
| Tables | Header row shaded, borders light, ≤6 columns portrait |
| Images | ≤15 cm wide; caption below in 9pt italic |

## Common Failure Modes to Avoid

- Wall-of-text without headings → restructure before delivery.
- Inconsistent heading levels (H1 → H3 skip) → breaks TOC and accessibility.
- Images stretched or pixelated → re-run optimizer at correct aspect ratio.
- Table split awkwardly across pages → set "repeat header row" + keep-with-next.
- Hidden metadata (author names, comments, prior version text) → scrub via properties check.
- Font substitution on open → use standard fonts or embed/note requirement.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
