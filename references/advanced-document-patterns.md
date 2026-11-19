# Advanced Document Patterns Catalog

## Purpose

This document catalogs sophisticated, reusable document patterns for
Microsoft 365 workflows: structured spreadsheets (RAB/BOQ, KPI
dashboards), formal documents (SOPs, policies, contracts), and narrative
documents (investor decks, research papers, registers and logs). Each
pattern includes a structure template, formula patterns, quality
checklist, decision rules for when to use it, and a concrete example.

## Pattern Index

1. RAB / BOQ — Rincian Anggaran Biaya / Bill of Quantities
2. SOP Systems — Standard Operating Procedures
3. KPI Dashboards
4. Investor Decks
5. Research Papers (IMRaD)
6. Policy Documents
7. Registers & Logs
8. Contracts & Agreements

Each pattern includes a structure template, formula patterns, quality
checklist, decision rules for when to use it, and a concrete example.

---
## 1. RAB / BOQ — Rincian Anggaran Biaya / Bill of Quantities

### When to use

Construction, procurement, event budgeting, project costing — anywhere
items must be priced by quantity × unit price with auditable totals.

### Structure template (Excel)

```
Sheet "BOQ": No | Item Code | Description | Unit | Qty | Unit Price |
  Total (=E*F) | Category | Notes
Sheet "Summary": material/labor/equipment subtotals, Overhead %,
  Contingency %, Grand Total, per-category breakdown
```

Category codes: `MAT-` materials, `LAB-` labor, `EQP-` equipment,
`SUB-` subcontractors, `OVH-` overhead.

### Formula patterns

- Line total: `=E2*F2` (Qty × Unit Price)
- Category subtotal: `=SUMIF(BOQ!H:H,"MAT-*",BOQ!G:G)`
- Grand total: `=SUM(BOQ!G:G)`
- With markup: `=Total*(1+Overhead%+Contingency%)`
- Unit-rate build-up:
  `=MaterialCost + LaborHours*LaborRate + EquipmentHours*EquipmentRate`

### Quality checklist

- [ ] Every line has unit and quantity > 0
- [ ] Item codes unique and sequential within category
- [ ] Totals tie: Summary grand total = sum of BOQ totals
- [ ] Currency format consistent; VAT/tax treatment stated
- [ ] Revision column or version noted
- [ ] No hardcoded totals — all formulas

### Example

```
No | Code    | Description           | Unit | Qty | Unit Price | Total
1  | MAT-001 | Portland Cement 50kg  | bag  | 120 | 62,500     | =E2*F2
2  | LAB-001 | Mason skill level 3   | m²   | 450 | 85,000     | =E3*F3
3  | EQP-001 | Mixer rental         | day  | 30  | 350,000    | =E4*F4
```

---

## 2. SOP Systems — Standard Operating Procedures

### When to use

Repeatable processes needing consistent execution: onboarding, incident
response, quality checks, safety procedures.

### Structure template (DOCX)

```
1. Document Control — Doc No: SOP-<dept>-<seq>-<rev>;
   revision table (Rev | Date | Description | Author | Approver);
   distribution list
2. Purpose — one paragraph, why this SOP exists
3. Scope — what is covered / explicitly excluded
4. Definitions & References — acronyms, related docs
5. Roles & Responsibilities — RACI matrix:
   Role | Responsible | Accountable | Consulted | Informed
6. Procedure — numbered steps, each with:
   action verb first, responsible role, expected output, forms referenced
7. Records & Forms — list of appendices
8. Revision History — table
9. Approval Block — prepared / reviewed / approved by, signatures, dates
```

### Numbering & checklist

- Steps use decimal numbering (`6.1`, `6.1.1`); revision codes `R01`,
  `R02`… with effective dates; review cycle "annually or on change".
- [ ] Every step starts with an imperative verb
- [ ] No step requires undocumented knowledge ("as usual", "etc.")
- [ ] Each form referenced exists as an appendix
- [ ] Roles named are defined in the R&R matrix
- [ ] Approval block has signature and date lines
- [ ] Revision history complete; current rev matches header

### Example — SOP step

```
6.3 Record the inspection result.
    6.3.1 The Quality Inspector (QI) records pass/fail per checklist
         item in Form QC-104.
    6.3.2 Any "fail" triggers Section 7 (Nonconformance).
    Output: Completed Form QC-104, retained for 3 years.
```

---

## 3. KPI Dashboards

### When to use

Performance tracking for teams, departments, or products — monthly/weekly
operational reviews.

### Structure template (Excel)

```
Sheet "Definitions": metric, formula, data source, owner, review freq
Sheet "Data": raw period values (month columns)
Sheet "Dashboard": summary table + charts
  Columns: Metric | Target | Actual | Variance | Variance % | Status
Sheet "Drilldown": per-metric detail linking back to Data
```

### Formula patterns

- Variance: `=C5-B5` (Actual − Target)
- Variance %: `=IF(B5=0,"",C5/B5-1)` — guard divide-by-zero
- Traffic-light conditional formatting on Status:
  green within ±5%, amber within ±15%, red beyond — direction-aware:
  for cost metrics lower is better
  (`=IF(metric_type="cost", variance_pct<=0, variance_pct>=0)`)
- YTD aggregate:
  `=SUMIFS(Data!values,Data!metric_col,"Revenue",Data!period,">="&DATE(2026,1,1))`
- Sparkline: `=SPARKLINE(range)` or chart object

### Quality checklist

- [ ] Every KPI has a written definition (what, formula, source)
- [ ] Target has rationale (last year + growth, benchmark, capacity)
- [ ] Actuals traceable to source — no manual overrides without log
- [ ] Status logic documented per metric
- [ ] Dashboard refreshes from Data sheet — no hardcoded summaries
- [ ] Print area set; fits one landscape page

### Example metric row

```
Metric: On-Time Delivery % | Formula: On-time orders / Total orders
Target: 95% | Actual: 91.2% | Var: -3.8pp | Status: RED
Owner: Ops Manager | Source: OMS export, column K
```

---

## 4. Investor Decks (PPTX)

### When to use

Fundraising, partnership pitches, internal business cases.

### Structure template — the arc

```
1. Title — company, one-line tagline, contact
2. Problem — quantified pain, who feels it
3. Solution — product, 3 key capabilities max
4. Product — screenshot/demo, "how it works" in 3 steps
5. Market — TAM/SAM/SOM with sourced numbers
6. Business Model — pricing, unit economics
7. Traction — metrics that prove demand (MRR, growth, logos)
8. Competition — 2×2 matrix positioning
9. Team — relevant experience only
10. Financials — 3-year projections, assumptions listed
11. Ask — amount, use-of-funds breakdown, runway extension
12. Appendix — detailed financials, tech, references
```

### Conventions

- One idea per slide; max ~40 words body text
- Financial slides: assumptions slide before projections
- Traction: lead with the single most impressive verifiable metric
- Ask slide: exact number + allocation percentages summing to 100%
- Every external claim has a source footnote

### Quality checklist

- [ ] Problem slide quantifies pain (money/time/risk), not vibes
- [ ] TAM/SAM/SOM bottom-up or cited
- [ ] Projections internally consistent (revenue − costs = EBITDA bridge)
- [ ] Ask amount matches use-of-funds allocation
- [ ] Team slide shows why THIS team wins
- [ ] No placeholder text, no "insert logo here", consistent fonts/colors

---

## 5. Research Papers — IMRaD

### When to use

Academic, technical, or scientific documents following
Introduction–Methods–Results–And-Discussion structure.

### Structure template (DOCX/PDF)

```
Title page: title, authors, affiliations, corresponding author, ORCID
Abstract: 150–300 words, structured or per venue spec
Keywords: 4–6 terms
1. Introduction — context, gap, research question, contributions
2. Literature Review — thematic, not list-only
3. Methods — reproducible: data, materials, procedures, analysis,
   statistical tests, ethics/IRB if applicable
4. Results — findings by research question; figures/tables numbered
   sequentially (Figure 1, Table 1)
5. Discussion — interpretation, comparison to prior work, limitations,
   future work
6. Conclusion — concise answers to research questions
References — consistent citation style throughout
Appendices — supplementary material
```

### Citation styles

| Style | In-text | Reference format | Best for |
|---|---|---|---|
| APA 7 | (Author, Year) | Author, A. A. (Year). Title. *Journal*. | Social sciences |
| IEEE | [1] | [1] A. Author, "Title," *Journal*, vol., pp. | Engineering/CS |
| Chicago | (Author Year) or footnotes | Full bibliographic | Humanities |

Generate references as BibTeX/CSL-JSON; format via pandoc
(`--citeproc`) or reference-manager export.

### Quality checklist

- [ ] Abstract standalone-readable (no citations, no undefined abbreviations)
- [ ] Every figure/table numbered, titled, referenced in text
- [ ] Methods sufficient for replication by a competent peer
- [ ] Results separated from interpretation
- [ ] Limitations explicitly stated
- [ ] All in-text citations have entries and vice versa
- [ ] Consistent citation style — no mixing APA and IEEE

### Example — figure caption

```
Figure 3. Quarterly revenue by segment (Q1–Q4 2026).
Error bars show ±1 SD across regions. Dashed line = target.
Source: internal finance export, Nov 2026.
```

---

## 6. Policy Documents

### When to use

Formal organizational rules: HR, security, data protection, procurement
policies.

### Structure template

```
Document Control: policy number, version, effective date, owner,
                  review date, classification
1. Purpose — business reason for the policy
2. Scope — who/what it applies to; explicit exclusions
3. Definitions — every defined term capitalized consistently
4. Policy Statements — numbered clauses (4.1, 4.2, ...)
   Each clause: rule + rationale + consequence of breach
5. Procedures — how to comply, who to contact
6. Exceptions — who can grant, how documented, time limits
7. Enforcement — monitoring, audit, disciplinary reference
8. Related Documents — cross-references
9. Revision History — version table
10. Sign-off — owner approval, legal review if applicable
```

### Quality checklist

- [ ] Scope unambiguous — names covered population precisely
- [ ] Definitions cover every capitalized term
- [ ] Each clause is testable (not aspirational "should strive to")
- [ ] Exceptions have owner and expiry mechanism
- [ ] Effective and review dates explicit
- [ ] Superseded policies listed

### Example — clause style

```
4.3 Password Requirements
All workforce accounts must use passwords of at least 14 characters
with mixed classes, or a passphrase of 5+ words. Shared accounts are
prohibited except documented service accounts in Appendix B. Breach may
result in suspension per HR Policy 2.1.
```

---

## 7. Registers & Logs

### When to use

Living tracking documents: asset registers, risk registers, issue logs,
meeting minutes, action-item trackers.

### Common templates

**Asset Register (Excel)**
```
Asset ID | Description | Category | Location | Custodian | Acquisition
Date | Cost | Status | Last Audit | Next Due | Notes
```
Status vocabulary: `Active | In Repair | Retired | Lost`; conditional
formatting: red = audit overdue.

**Risk Register (Excel)**
```
Risk ID | Description | Category | Likelihood (1-5) | Impact (1-5) |
Score (=L*I) | Owner | Mitigation | Residual Score | Status | Review Date
```
Heat-map on Score: green ≤4, amber 5–12, red ≥15.

**Issue Log (Excel)**
```
Issue ID | Date Raised | Reporter | Description | Severity
(Critical/High/Medium/Low) | Owner | Status | Resolution | Closed Date
```
SLA column: Critical=4h, High=1d, Medium=3d, Low=1w response.

**Meeting Minutes (DOCX)**
```
Header: title, date, time, location/link, chair, attendees, apologies
1. Agenda items — discussion summary, decisions (D),
   action items (A: who/what/when)
2. Action Items table: # | Action | Owner | Due Date | Status
3. Next meeting date/agenda hints
4. Distribution list
```

### Quality checklist

- [ ] IDs sequential, never reused
- [ ] Status fields use controlled vocabularies (data validation)
- [ ] Every action item has owner + due date
- [ ] Overdue items visually flagged
- [ ] Registers have defined review cadence and owner

---

## 8. Contracts & Agreements

### When to use

Legal or quasi-legal agreements: service contracts, NDAs, MSAs, SOWs,
terms of service.

### Structure template

```
Title: "Master Service Agreement" / "Non-Disclosure Agreement" etc.
Preamble: effective date, parties (legal names, entity type, jurisdiction,
          addresses, authorized signatories)
Recitals: "WHEREAS..." background clauses
Definitions: capitalized defined terms
Articles/Sections:
  1. Scope of Services / Obligations
  2. Term & Termination
  3. Fees & Payment (amounts, schedule, late fees, taxes)
  4. Confidentiality / IP Ownership
  5. Warranties & Disclaimers
  6. Limitation of Liability
  7. Indemnification
  8. Dispute Resolution (governing law, venue, arbitration)
  9. General Provisions (notices, assignment, entire agreement,
     severability, counterparts, amendments)
Schedules/Exhibits: pricing tables, SLAs, technical specs
Signature blocks: party name, signature line, printed name, title, date —
                 for EACH party
```

### Quality checklist

- [ ] Party legal names exact
- [ ] Effective date and term unambiguous
- [ ] Payment terms complete: amount, currency, invoicing, net-days,
      late interest
- [ ] Liability cap defined (often 12 months of fees)
- [ ] Governing law and dispute venue specified
- [ ] Signature blocks for all parties with date lines
- [ ] Exhibits referenced in body actually attached
- [ ] Cross-references between sections resolve correctly

### Example — signature block

```
IN WITNESS WHEREOF, the parties have executed this Agreement as of
the Effective Date.

PT. AGRA KARYA DIGITAL          ___________________________
("Company")                    Authorized Signatory
                               Name: [Name]
                               Title: [Title]
                               Date: _______________
```

---

## Cross-Pattern Decision Rules

- **Numbers that must audit** (budgets, KPIs) → Excel formulas, never
  static values in DOCX tables.
- **Processes humans follow** → SOP (numbered steps + forms + approvals).
- **Persuasion** → PPTX deck following the narrative arc.
- **Legal enforceability** → formal contract/SOP/policy structure with
  sign-off blocks.
- **Tracking over time** → registers/logs with controlled vocabularies
  and review dates.
- **Scholarly credibility** → IMRaD + consistent citations + limitations.

## Quality Standards (All Patterns)

- Consistent numbering schemes within each document family
- Controlled vocabularies for status/category fields (dropdowns)
- Every table has a header row; every figure has a caption
- Version/revision metadata on every formal document
- No orphaned references (appendix cited but missing, section absent)

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
