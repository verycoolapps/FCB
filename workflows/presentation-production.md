# Workflow: Presentation Production

**Purpose:** Produce or enhance PowerPoint `.pptx` decks (and Sway-style narrative decks where appropriate) — pitch decks, report decks, training, board updates, classroom materials, proposal decks.

---

## Trigger

Activate when the deliverable is a slide deck or presentation: "make a pitch deck", "create slides for", "build a presentation", "improve this PowerPoint", "turn this report into slides".

## Input

- Topic, audience, occasion, duration (drives slide count: ~1–2 min/slide for talks, more for leave-behinds).
- Source material: report, data, outline, existing deck.
- Brand: template, colors, logo, fonts.
- Visual assets needed (photos, icons, diagrams).
- Delivery mode: live talk, async review, kiosk, print/PDF.

## Preconditions

- Load references: `powerpoint-engine.md`, `advanced-document-patterns.md` (narrative arcs), `design-system.md`; add `accessibility.md` always; `feng-shui-design.md` if requested.
- Decide: build from outline vs. transform existing content vs. enhance existing deck.
- Story structure must be chosen BEFORE slide layout — narrative first, slides second.

## Step-by-Step Process

1. **UNDERSTAND** — 12 questions; lock: audience, goal (inform/persuade/train), duration, delivery mode.
2. **STORY** — Build narrative arc per `advanced-document-patterns.md`:
   - Pitch: Hook → Problem → Stakes → Solution → How it works → Proof → Offer → Ask.
   - Report: Headline finding → Context → Evidence → Implications → Recommendations → Next steps.
   - Training: Objective → Why it matters → Concept → Demo → Practice → Recap → Resources.
   - Write the **one-sentence takeaway per slide** before designing anything.
3. **ARCHITECT** — Slide list with type per slide: Title / Agenda / Section / Content / Data / Quote / Image / Closing. Target 8–15 slides for a 15-min talk; max ~20 unless leave-behind.
4. **DESIGN** — Set masters/layouts, palette, typography (title ≥32pt, body ≥20pt for projection), grid, logo placement, slide numbers, footer.
5. **RESEARCH** — Facts and assets. Every image via `visual-research-workflow.md`; every stat sourced.
6. **CREATE** — Build via `scripts/presentation_generator.py`. Rules: one idea per slide; ≤6 bullets; charts over tables; speaker notes for every content slide.
7. **VISUAL ASSETS** — Icons consistent set (one family); diagrams rebuilt as native shapes where possible for editability.
8. **ENHANCE** — Add: transitions only if purposeful (default none), animations minimal, hyperlinks to appendix, embedded fonts note if custom.
9. **VALIDATE** — `scripts/document_validator.py` + 7-level QA ladder.
10. **DELIVER** — `final-delivery-workflow.md`. Include PDF export if for distribution.

## Decision Points

- **Deck vs. document** → if the "presentation" is really a 30-page report to be read, produce a Word doc + optional 5-slide summary deck; say so.
- **Data slides** → chart type chosen by message (comparison → bar; trend → line; composition → stacked bar/pie sparingly; distribution → histogram). Never 3D charts.
- **Existing deck** → preserve user's template/masters; improve content and consistency, don't redesign unless asked.
- **Image-heavy** → full-bleed images with text overlay allowed only if contrast ≥4.5:1; otherwise side-by-side layout.
- **Long deck requested** → push back gently: offer main deck + appendix deck.

## Application Routing

- **PowerPoint** — primary.
- **Sway** — alternative for async, scroll-style narratives (mention as option).
- **Word** — speaker script, handouts, appendix document.
- **Excel** — source data and chart data; live-linked charts only if environment supports it.
- **Clipchamp** — if user wants a video version of the deck.
- **Forms** — audience feedback/polling link suggestion.
- **Outlook/Teams** — delivery and rehearsal scheduling (no sends without consent).

## Execution Rules

- One takeaway per slide, written in speaker notes as the slide's thesis.
- Bullet discipline: ≤6 bullets, ≤8 words each for projected decks; more allowed for leave-behinds (state which mode).
- Fonts: title/body pair from design system; never below minimums; embed or avoid exotic fonts.
- Every image licensed + attributed; alt text on all visuals.
- Slide masters used — no per-slide manual styling that breaks theme.
- Charts: labeled, sourced, colorblind-safe; data labels where they aid reading.
- No decorative clipart; no stock-photo clichés (handshake, thumbs-up) unless specifically requested.

## Validation

- `document_validator.py`: slide count vs. plan, font sizes within minimums, notes present, images have alt text, no overflow (text fits placeholders), consistent masters.
- Render check: export to PDF/images if possible and inspect a sample of slides.
- Story check: read slide titles alone — they must narrate the argument.
- QA ladder 1–7.

## Error Recovery

- **Source content missing** → build outline deck with `[NEEDS INPUT: data for slide N]`; deliver structure + ask.
- **Asset failure** → placeholder box labeled `[IMAGE: description]` only if blocking; prefer licensed substitute.
- **Template broken/corrupt** → rebuild on clean master; disclose.
- **Cannot render preview** → validate structurally via library; note that visual check is pending.

## Expected Outputs

- `ProjectName_Deck_vN.pptx` (primary), `ProjectName_Deck_vN.pdf` (for distribution/review).
- Optional: Word handout, Excel data file, speaker script.
- Attribution register; speaker notes complete.
- Delivery summary with QA sign-off and suggested rehearsal timing.

---


## Narrative Playbooks

### Pitch Deck (investor/client)
1. Hook (vision or provocative stat) 2. Problem + cost of inaction 3. Solution (one clear sentence) 4. Product/how it works 5. Market/trction 6. Business model 7. Competition matrix 8. Team 9. Ask + use of funds 10. Close.
- Every claim needs proof on the slide or in notes (source cited).
- Financials slide: 3-year projection max, assumptions footnoted.

### Board / Executive Report
- Start with the headline: "Revenue up 12%, churn risk in Segment B."
- Traffic-light status (R/Y/G) per initiative; decisions requested clearly marked.
- Appendix carries detail; main deck stays ≤15 slides.

### Training / Enablement
- Learning objectives as measurable outcomes ("By the end you can…").
- Concept → example → practice prompt → recap pattern per module.
- Job aid slide at end: one-page checklist/cheat sheet.

### Classroom / Lecture
- Chunk into 10–15 min segments with activity breaks noted in speaker notes.
- Reading level matched to audience; define jargon on first use.
- Assessment hook: end with 3-question recall check.

### Conference / Keynote
- One big idea; slides as backdrop not teleprompter (≤5 words per line for main stage).
- Story spine: setup → tension → turn → resolution.
- Rehearsal timing noted per slide in speaker notes.

## Slide-Type Rules

| Type | Rules |
|---|---|
| Title | Deck title, presenter, date, audience; one strong visual or brand element |
| Agenda | Only if deck >10 slides or >20 min; clickable in PPT, plain in PDF |
| Section | Minimal text (section name + one-line framing); visual reset |
| Content | One idea; ≤6 bullets ≤8 words; visual supports, never decorates |
| Data | Chart chosen by message; source line + takeaway sentence in notes/title |
| Quote | Large type; attribution; ≤30 words |
| Image | Full or half bleed; caption if informational; alt text mandatory |
| Closing | Clear next step: contact, QR/link, thank-you + key takeaway repeat |

## Storytelling Quality Checks

- Read only the slide titles aloud: they must form a coherent argument.
- Each slide answers "so what?" — if not, cut or merge.
- Opening slide earns attention in 5 seconds; closing slide leaves one memorable point.
- Emotional arc matches audience: executives want confidence + control; clients want understanding + trust; classrooms want curiosity + achievable wins.

## Common Failure Modes to Avoid

- Slide is a document page (paragraphs of text) → split or move to handout.
- Chart without a stated takeaway → add insight sentence.
- Inconsistent visual rhythm (dense, dense, image, dense) → rebalance.
- Speaker notes absent → audience can't present; add notes or flag as self-running deck.
- Fonts below minimum on "it'll fit" logic → projected decks enforce minimums.
- Deck built backward from template prettiness → story first, template second.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
