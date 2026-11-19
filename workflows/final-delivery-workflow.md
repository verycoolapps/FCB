# Workflow: Final Delivery

**Purpose:** Package, name, version, attribute, QA-sign, and summarize any FileCraftBooster output into a clean, professional handoff.

---

## Trigger

Final stage of EVERY task. Activate whenever artifacts are ready to hand to the user — it is not optional and not a formality.

## Input

- All produced artifacts (files, folders, assets).
- The original request and any deviations/interpretations made.
- Attribution data collected during visual research.
- QA results from validation steps.
- Known limitations and manual steps required.

## Preconditions

- Every artifact has passed (or had explicitly waived) the 7-level QA ladder.
- All assets have verified licenses and attribution entries.
- No placeholders, stubs, or `[TODO]` remain in deliverables.
- File names follow convention; versions are consistent.

## Step-by-Step Process

1. **INVENTORY** — List every file produced: path, type, purpose, size.
2. **NAME & VERSION** — Apply convention: `EngagementOrProjectName_ArtifactType_vN.ext`
   - Examples: `Aurora_SalesProposal_v1.docx`, `Aurora_PricingModel_v1.xlsx`, `Aurora_PitchDeck_v1.pptx`, `Aurora_Assets_v1.zip`.
   - Version: `v1` initial; bump minor for revisions (`v1.1`); never overwrite — always new version.
   - No spaces in filenames; underscores or hyphens; date suffix only for dated reports (`..._2026-11-19`).
3. **ORGANIZE** — For multi-artifact deliveries, build folder structure:
   ```
   DeliverableName_vN/
   ├── Documents/
   ├── Spreadsheets/
   ├── Presentations/
   ├── Assets/
   ├── MANIFEST.md
   ├── ATTRIBUTION.md
   ├── SETUP.md            (if manual steps exist)
   └── DELIVERY_SUMMARY.md
   ```
   Single artifacts ship flat with just attribution/summary as needed.
4. **ATTRIBUTION REGISTER** — Compile `ATTRIBUTION.md`. Every third-party asset gets a row:
   `| Asset file | Description | Author/Creator | Source URL | License | Date accessed |`
   Include fonts, icons, templates, and data sources (not just images). CC0/public domain entries still get listed with license noted.
5. **MANIFEST** — `MANIFEST.md`: file inventory with purpose, version, dependencies between files (e.g., "deck charts source: PricingModel_v1.xlsx"), and open-with recommendations.
6. **SETUP GUIDE** — `SETUP.md` (when applicable): exact manual steps — folder creation in SharePoint, Teams channel setup, Power Automate import, permissions, data refresh instructions. Written for a non-technical user.
7. **QA SIGN-OFF** — Run final checks via the conventions in this file:
   - All validators pass or waivers documented.
   - Attribution coverage = 100%.
   - No `[NEEDS INPUT]`/`[IMAGE NEEDED]` markers unless disclosed to user as outstanding.
   - File naming consistent; versions sequential.
8. **DELIVERY SUMMARY** — Produce `DELIVERY_SUMMARY.md` (and mirror key points in chat):
   - What was delivered (files + one-line purpose each).
   - How it maps to the request.
   - QA sign-off block (levels 1–7, security tier).
   - Limitations & honest capability notes (what couldn't be done in this environment).
   - Manual next steps for the user.
   - Offer: "Want me to adjust X, regenerate Y, or produce Z?"
9. **HAND OFF** — Present files with absolute paths, state total count, and the one thing the user should check first.

## Decision Points

- **Single vs. bundle** → single file: flat delivery + inline attribution note. Multi-file: always bundle folder.
- **Version collision** → if `v1` exists from prior session, deliver `v2` and note what changed.
- **Outstanding `[NEEDS INPUT]` markers** → deliver anyway if structure is useful, but the summary MUST list every outstanding item prominently — never bury it.
- **User asked for "just the file"** → still include minimal attribution (license requires it); offer to strip non-required credits if they confirm license permits.
- **Confidential tier T2/T3** → add handling instructions in summary (password-protect recommendation, sharing restrictions) per `security-and-privacy.md`.

## Application Routing

- **OneDrive/SharePoint** — suggested upload target; provide folder structure ready to replicate (do not upload without consent).
- **Outlook** — draft cover email summarizing delivery (never send).
- **Teams** — suggested channel post text (never post).

## Execution Rules

- Attribution is non-negotiable: licenses legally require it; missing attribution = failed delivery.
- The delivery summary must be honest: if a PDF export wasn't verified visually, say so.
- Never claim files were "tested in Excel/Word" unless actually opened/validated — say "validated programmatically" vs. "opened and verified".
- Include file sizes so user knows what they're downloading.
- Keep the summary scannable: headers, bullets, sign-off block — no walls of text.

## Validation

Final gate before handoff:

```
DELIVERY CHECKLIST
[ ] All files present per manifest
[ ] Naming convention applied, versions correct
[ ] ATTRIBUTION.md complete (100% asset coverage)
[ ] QA sign-off recorded per artifact
[ ] Limitations disclosed
[ ] No hidden placeholders
[ ] Paths absolute and valid
```

## Error Recovery

- **Attribution gap discovered late** → fix before delivery; do not ship with "will add later".
- **File corrupted in packaging** → re-run validator on packaged copy, not just source.
- **User rejects output** → identify whether issue is content, format, or scope; regenerate the specific artifact at next version; keep prior version.
- **Cannot produce manifest programmatically** → write it manually; never skip it for multi-file deliveries.

## Expected Outputs

- Deliverable folder or single file(s), correctly named and versioned.
- `MANIFEST.md`, `ATTRIBUTION.md`, `SETUP.md` (if needed), `DELIVERY_SUMMARY.md`.
- Chat response: file list + paths + QA sign-off + top manual step.

## Delivery Summary Template

```
# Delivery Summary — <Project Name> v<N>

## What You Received
| File | Purpose | Version |
|---|---|---|

## How It Maps to Your Request
<2–4 bullets>

## QA Sign-Off
Levels 1–7: PASS | Security tier: T<n> applied

## Assets & Licenses
<count> assets used — see ATTRIBUTION.md. All licenses verified.

## Limitations & Manual Steps
<honest list, or "None">

## Suggested First Step
<the single most useful next action>
```

## Versioning Rules

- `v1` = first delivery. `v1.1`/`v2` = revisions. Never silently overwrite.
- When revising, state what changed at the top of the summary.
- If user provides feedback, regenerate at next version and keep the old file.

## Handoff Etiquette

- Present absolute paths so files are clickable.
- Lead with the file the user most likely wants to open first.
- One-line description per file — not every technical detail.
- End with an offer to iterate: adjust, regenerate, or extend scope.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
