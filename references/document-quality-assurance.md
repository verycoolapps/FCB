# Document Quality Assurance — 7-Level Framework

## Purpose

Define a deterministic, repeatable quality-assurance framework applied to every
artifact produced by FileCraftBooster. QA runs after generation and before
delivery; findings are classified by severity and remediated in a bounded loop.

## The 7 Levels

### L1 — Structural Integrity

Verify the file is a valid OOXML package and all required parts exist.

- File opens without repair prompt in the target application.
- `.docx`/`.xlsx`/`.pptx` is a valid ZIP (PK header) containing `[Content_Types].xml`,
  `_rels/.rels`, and the main document part.
- No zero-byte required parts; no duplicate part names.
- Embedded objects (charts, images, OLE) have valid relationships.
- Excel: workbook opens, sheet names valid (≤31 chars, no `[]:*?/\`), no
  external-link errors at open.
- PowerPoint: slide masters/layouts present; every slide has a layout.
- PDF: valid header `%PDF`, xref table intact, page count matches manifest.

**Severity defaults:** any L1 failure = **blocker** (file unusable).

### L2 — Content Quality

Verify content correctness and completeness.

- No placeholder text: `TODO`, `TBD`, `Lorem ipsum`, `[insert`, `XXX`,
  `FIXME`, `placeholder`, `<name>`.
- Facts consistent across artifacts in the same workflow (names, dates,
  figures, project IDs).
- Numbers reconcile: Excel totals match Word/PowerPoint quoted values;
  gradebook sums match syllabus weights.
- Terminology consistent with the project glossary.
- Dates valid (not in the past for forward-looking docs, not malformed).
- Required sections present per deliverable spec (e.g., proposal must have
  pricing, terms, sign-off).
- Spelling: run spell-check dictionary pass; flag unknown proper nouns for
  human review rather than auto-correcting.

**Severity:** placeholder/TODO = **major**; numeric mismatch = **major**;
terminology drift = **minor**; spell flag = **minor**.

### L3 — Visual Quality

Verify rendering correctness.

- Fonts specified exist or have safe fallbacks; no missing-glyph boxes.
- Images placed within margins; aspect ratio preserved; resolution adequate
  for target output (≥150 dpi for print).
- Charts legible at intended size: axis labels readable, legend not overlapping,
  data labels not clipped.
- Margins safe: no content within 0.5" of edge for print; slide content inside
  0.3" safe margin.
- Page/slide breaks not orphaning headings (keep-with-next respected).
- Table rows not split awkwardly across pages where avoidable.
- Color contrast meets WCAG minimums (see accessibility.md).
- Consistent style: fonts, sizes, colors match template/brand tokens.

**Severity:** clipped content/overlapping = **major**; orphan heading =
**minor**; style drift = **minor**.

### L4 — Functional Integrity

Verify interactive and computed elements work.

- Excel formulas: recalculate without `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`;
  precedent cells trace correctly; defined names resolve.
- TOC fields present and populated in Word docs >3 pages.
- Cross-references (REF, PAGEREF, hyperlinks) resolve; no broken anchors.
- Hyperlinks use `https://` or `mailto:`; internal doc links resolve.
- Form fields (content controls, legacy form fields) have names and default
  values where required.
- PowerPoint: animations/transitions don't block content; speaker notes
  present where required.
- Protected regions (if any) are intentional; no accidental sheet/workbook
  protection left on.

**Severity:** formula error = **major** (blocker if totals wrong); broken
cross-ref = **minor**; missing TOC = **minor**.

### L5 — Accessibility

Verify conformance to accessibility.md.

- Heading hierarchy logical (H1→H2→H3, no skipped levels).
- Images/charts have alt text; decorative images marked decorative.
- Tables have header rows; not used for layout.
- Color is not the sole carrier of meaning.
- Contrast ratios pass WCAG AA.
- Reading order logical (no text boxes out of flow for body copy).
- Language tag set on document.
- Links have meaningful text (not "click here").

**Severity:** missing alt text on informative image = **major**; heading skip
= **minor**; contrast fail = **major**.

### L6 — Security & Privacy

Verify no sensitive or unsafe content ships.

- No secrets: API keys, passwords, tokens, connection strings.
- No macros (`vbaProject.bin`) unless explicitly requested and signed off.
- No external template/content injections; no DDE/remote template references.
- External links flagged and listed in QA report for user review.
- PII minimized: only necessary personal data included; sensitive data
  (IDs, financial account numbers) redacted or omitted.
- Document properties scrubbed: no author metadata leaks unless intended.
- Embedded files inspected for executables.

**Severity:** secret/macro = **blocker**; unflagged external link =
**major**; PII excess = **major**; metadata leak = **minor**.

### L7 — Delivery & Handoff

Verify packaging and handoff readiness.

- Filename follows `{project_id}_{deliverable}_{version}.{ext}` convention.
- Version label embedded in document (footer/header or properties).
- Manifest generated listing all artifacts, statuses, QA summary.
- Handoff notes written: known issues, assumptions, regeneration commands.
- All artifacts in one delivery folder; no stray temp files.
- Final files open cleanly in target apps (smoke test).

**Severity:** missing manifest = **major**; naming violation = **minor**;
stray temp files = **minor**.

## Per-App Checklists

### Word (.docx)

- [ ] Opens without repair; valid OOXML zip
- [ ] Styles use named styles (Heading 1/2/3, Normal), not direct formatting
- [ ] TOC field present and updated (if >3 pages)
- [ ] Page numbers in footer; header consistent
- [ ] No tracked changes or comments left unless intended
- [ ] Headers/footers don't collide with body
- [ ] Table of contents page numbers correct after final pagination
- [ ] Document properties: Title, Author, Subject set

### Excel (.xlsx)

- [ ] All sheets present; names meaningful and ≤31 chars
- [ ] Formulas recalculate cleanly (no error values)
- [ ] Input cells visually distinct from formula cells (color/format)
- [ ] Frozen panes on data sheets; filters applied where appropriate
- [ ] Charts have titles, axis labels, legends; source data on-sheet
- [ ] No hidden sheets unless intentional (and noted)
- [ ] Workbook protection off unless required
- [ ] Print area set; fits-to-page where intended

### PowerPoint (.pptx)

- [ ] Slide masters/layouts consistent; fonts embedded or safe
- [ ] Every slide has a title placeholder filled
- [ ] Images not stretched; aspect ratio preserved
- [ ] Speaker notes present on content slides
- [ ] No text overflow beyond slide bounds
- [ ] Slide numbers present (if >5 slides)
- [ ] Transitions consistent; no auto-advance surprises
- [ ] Final slide has contact/next-steps info

### PDF

- [ ] Valid PDF structure; opens in multiple readers
- [ ] Text is selectable (not rasterized) unless intentional
- [ ] Bookmarks/outline present for >5 pages
- [ ] Fonts embedded
- [ ] Page size correct (A4/Letter per spec)
- [ ] Hyperlinks functional
- [ ] Tagged PDF structure present (accessibility)

### Outlook (.eml/.msg)

- [ ] Subject line clear and specific
- [ ] Body ≤150 words for cover emails; key info above fold
- [ ] Attachments listed in body and actually attached
- [ ] No sensitive data in subject line
- [ ] Signature block present
- [ ] Reply-to and sender fields correct

## Severity Classification

| Severity | Definition | Action |
|---|---|---|
| **Blocker** | File unusable, security risk, or wrong totals | Must fix before delivery; workflow halts |
| **Major** | Significant quality issue affecting usability/professionalism | Fix before delivery; may deliver with note if user approves |
| **Minor** | Cosmetic or polish issue | Fix if cheap; may ship with note |

## QA Report Format

```json
{
  "artifact": "PRJ-2026-014_proposal_v1.docx",
  "levels_run": ["L1","L2","L3","L4","L5","L6","L7"],
  "findings": [
    {
      "level": "L2",
      "severity": "major",
      "location": "Section 5, Table 5-2",
      "issue": "Total $178,450.00 does not match pricing model $178,540.00",
      "remediation": "Update proposal total or regenerate from model"
    },
    {
      "level": "L5",
      "severity": "minor",
      "location": "Page 3, Figure 3-1",
      "issue": "Chart image lacks alt text",
      "remediation": "Add alt text describing trend"
    }
  ],
  "summary": {"blockers": 0, "majors": 1, "minors": 1, "passed": false},
  "remediation_loop": {"iterations": 1, "auto_fixed": 0, "requires_human": 1}
}
```

## Remediation Loop Rules

1. QA runs once after generation; findings classified by severity.
2. Auto-fixable issues (missing alt text template, naming, metadata) are
   fixed in-place without re-running full generation.
3. Content/numeric mismatches trigger regeneration of the affected section
   or full artifact if the error is systemic.
4. Maximum 3 remediation iterations; if unresolved, deliver with
   `qa_summary.blockers/majors` populated and a prominent handoff note.
5. Security findings (L6) are never auto-waived; require explicit user
   acknowledgment to ship with a blocker.
6. Every remediation is logged with before/after state for audit.

## Practical Examples

**Example 1 — Excel formula error caught:**
QA L4 finds `#DIV/0!` in `Pricing!F12` because discount column has a zero
denominator. Remediation: guard formula with `IFERROR` or fix denominator;
re-run L4; report clean.

**Example 2 — Cross-artifact mismatch:**
QA L2 compares proposal total ($178,450) vs Excel model ($178,540). Root cause:
discount applied twice. Remediation: regenerate proposal Section 5 from model;
verify match to the cent.

**Example 2 — Security flag:**
QA L6 finds `vbaProject.bin` in a `.docx` that should not contain macros.
Remediation: strip macros, re-verify, flag in manifest if user intended macros.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
