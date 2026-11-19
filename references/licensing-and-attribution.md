# Licensing & Attribution Intelligence — License Classification, Verification, Attribution Registers

## Purpose

The licensing engine classifies every external asset (images, icons, fonts, 3D models, text, data) by license, verifies the license before use, decides whether the asset may appear in a given deliverable, and generates correct attribution text in the required style. It is the enforcement layer behind `visual-asset-intelligence.md`: no asset reaches a deliverable without passing through this engine.

## Scope

In scope: license taxonomy classification, per-license permission matrix, verification checklists, attribution register generation (inline credit, caption credit, end-matter credits page), decision rules for client/commercial deliverables, ambiguity escalation.

Out of scope: legal advice (the engine surfaces facts and conservative defaults; a lawyer decides edge cases); obtaining licenses (it flags when a paid license is needed).

## License Classification Table

| License | Commercial use | Modify | Redistribute | Attribution required | Share-alike | Typical sources |
|---|---|---|---|---|---|---|
| **CC0 / Public Domain** | ✅ | ✅ | ✅ | ❌ (appreciated) | ❌ | Smithsonian OA, NASA, Poly Haven, ambientCG, Kenney, some Openverse/Wikimedia |
| **CC BY** | ✅ | ✅ | ✅ | ✅ | ❌ | Openverse, some Sketchfab/Wikimedia |
| **CC BY-SA** | ✅ | ✅ | ✅ | ✅ | ✅ (derivatives same license) | Wikimedia, Openverse |
| **CC BY-NC** | ❌ | ✅ | ✅ | ✅ | ❌ | Flickr, some Openverse |
| **CC BY-ND** | ✅ | ❌ (no derivatives) | ✅ | ✅ | ❌ | Some stock/flickr |
| **CC BY-NC-SA** | ❌ | ✅ | ✅ | ✅ | ✅ | Wikimedia, Openverse |
| **CC BY-NC-ND** | ❌ | ❌ | ❌ (share only) | ✅ | ❌ | Many Flickr, ResearchGate |
| **ODbL** | ✅ | ✅ | ✅ | ✅ | ✅ (database share-alike) | OpenStreetMap data |
| **MIT / Apache-2.0** | ✅ | ✅ | ✅ | ✅ (license notice) | ❌ | Code assets, icons-as-code |
| **SIL OFL 1.1** | ✅ | ✅ (fonts) | ✅ (with conditions) | ❌ (reserved name rules) | ❌ | Google Fonts, most font CDNs |
| **Proprietary / Stock** | Per license terms | Per terms | Per terms | Per terms | Per terms | Envato, Adobe Stock, iStock, ShutterStock |
| **Unknown / Unmarked** | ❌ (treat as all-rights-reserved) | ❌ | ❌ | — | — | Random web images, scraped content |

**Key distinctions:**
- **ND (NoDerivatives):** cropping, recoloring, overlaying text, or embedding in a composite may count as derivative — treat ND images as unusable in designed documents unless the license explicitly permits the use.
- **NC (NonCommercial):** any deliverable for a paying client, commercial product, or revenue-linked purpose is commercial — NC assets are excluded from client work.
- **SA (ShareAlike):** if the deliverable itself is a derivative of the asset (e.g., a collage), SA may propagate — flag for review rather than assume.
- **OFL fonts:** embedding in documents/PDFs is allowed; renaming/reselling the font itself is not; the "Reserved Font Name" cannot be used for modified versions.

## Verification Checklist

For every candidate asset, before placement:

1. **Locate license declaration** — on the asset page, in metadata, in a LICENSE file (repos), or in API response (`license` field from Openverse/Sketchfab APIs).
2. **Record provenance:**
   - `source_name` (e.g., "Wikimedia Commons")
   - `source_url` (canonical page URL, not CDN link)
   - `asset_title`
   - `author` / `creator`
   - `license_name` (exact, e.g., "CC BY-SA 4.0")
   - `license_url` (canonical license text URL)
   - `date_accessed` (YYYY-MM-DD)
   - `modifications` (what was done: cropped, recolored, resized — "none" if untouched)
3. **Cross-check license version** — CC licenses are versioned (3.0 vs 4.0 have different terms); record the version.
4. **Check for additional terms** — some sources add terms beyond the license (e.g., Unsplash: no unaltered resale; Storyset free tier: attribution required).
5. **Verify the author/agency claim** — if the page claims "public domain" for a museum object, confirm the institution's open-access policy page (Smithsonian OA and NASA are verified PD programs).

If any step fails or the license is absent → classify as `unknown` → exclude per decision rules.

## Decision Rules

Apply in order; first match wins:

1. **Client/commercial deliverable?** → Exclude all `NC` licenses, all `unknown`, all `ND` unless the use is verbatim display with no modification.
2. **Deliverable requires modification** (crop, recolor, composite, overlay)? → Exclude `ND`; flag `SA` for share-alike review.
3. **Attribution capacity?** → If the deliverable format cannot carry attribution (e.g., a favicon, a tiny icon at 16px), prefer CC0/PD; otherwise generate attribution text.
4. **Font embedding?** → Only OFL or licensed fonts; never embed proprietary fonts without license.
5. **Stock/proprietary asset?** → Verify the specific license tier purchased; record license key/receipt reference in manifest.
6. **Ambiguity or conflict** (two sources claim different licenses; license page unreachable) → **escalate to user** with the asset, the conflicting claims, and the conservative recommendation (exclude). Never guess.

**Default posture:** when in doubt, exclude. A missing image is a recoverable defect; a license violation in a client deliverable is not.

## Attribution Register Format

The engine maintains a register — a structured list that generates attribution text blocks per style.

### Register Entry (per asset)

```yaml
- id: asset-042
  title: "Solar panel array, aerial"
  author: "Jane Photographer"
  source: "Wikimedia Commons"
  source_url: "https://commons.wikimedia.org/wiki/File:Solar_array.jpg"
  license: "CC BY-SA 4.0"
  license_url: "https://creativecommons.org/licenses/by-sa/4.0/"
  date_accessed: "2026-11-19"
  modifications: "Cropped to 16:9, resized"
  placement: "slide-3, figure-2"
```

### Generated Attribution Styles

**Inline credit** (for captions/footnotes):
> "Solar panel array, aerial" by Jane Photographer, Wikimedia Commons, CC BY-SA 4.0.

**Figure caption credit** (Word/PowerPoint caption line):
> *Figure 2. Solar panel array, aerial. Image: Jane Photographer / Wikimedia Commons, CC BY-SA 4.0.*

**End-matter credits page** (for documents with multiple assets):

```
## Image Credits

- "Solar panel array, aerial" — Jane Photographer — Wikimedia Commons — CC BY-SA 4.0
  https://commons.wikimedia.org/wiki/File:Solar_array.jpg (accessed 2026-11-19; cropped, resized)
- "Factory floor" — John Doe — Unsplash — Unsplash License
  https://unsplash.com/photos/abc123 (accessed 2026-11-18; no modifications)
```

**Compact credits line** (slide footer, when space-constrained):
> Images: Wikimedia Commons (CC BY-SA), Unsplash. Full credits in appendix.

**No-attribution assets** (CC0/PD) may be listed for transparency or omitted — list them when the deliverable values provenance (academic, government).

## Pre-Flight Verification Checklist

Run this checklist for every candidate asset before it enters a deliverable:

1. **Source identified** — canonical URL or asset ID recorded (not just a search-result page).
2. **License located** — license text or license API record retrieved; not inferred from site reputation.
3. **License classified** — mapped to the classification table; ambiguous cases marked `unknown`.
4. **Commercial use** — confirmed the deliverable's context is permitted (client work excludes NC/ND).
5. **Modification allowed** — cropping, recoloring, and compositing permitted (ND blocks all derivatives).
6. **Attribution format** — required credit string drafted (author, title, source, license, link).
7. **Share-alike impact** — for SA licenses, note that the asset file itself must carry the same license and downstream edits inherit it.
8. **Register entry** — written to the attribution register with access date and verification notes.
9. **Fallback ready** — a CC0/PD alternative selected in case the primary asset fails delivery QA.

If any step fails, the asset is excluded and the failure is recorded — exclusions are as important as inclusions for auditability.

## Error Handling

- **License page unreachable:** try the canonical license URL and the source's license API; if both fail, mark `license_unverified` and exclude.
- **Conflicting license claims:** record both, escalate to user, default exclude.
- **License requires registration/permission** (e.g., some museum high-res images): flag as `requires_permission`, provide the permission-request link, exclude until confirmed.
- **SA asset in a proprietary deliverable:** flag that the deliverable may need to carry SA terms for the asset portion — escalate rather than assume fair use.
- **Font license unclear:** check the font's OFL.txt or foundry license; Google Fonts = OFL; if unknown, substitute a known OFL alternative (see `design-system.md` fallback table).
- **Attribution space insufficient:** if the format can't carry credits (tiny icon), switch to a CC0/PD alternative rather than dropping attribution.

## Worked Examples

### Example 1 — Word report with 3 images

Assets: 1× CC BY photo (Wikimedia), 1× CC0 (Smithsonian), 1× Unsplash.
Decision: all permitted for commercial use. Output: figure captions carry credit lines for the CC BY image; Smithsonian and Unsplash listed in an "Image Credits" section at end (transparency); register entries recorded with dates.

### Example 2 — Slide deck, client commercial

Asset candidate: CC BY-NC-SA illustration from Openverse. Decision: NC → excluded for client work. Engine selects a CC0 Humaaans illustration instead; no attribution needed but listed in appendix credits anyway. If no CC0 alternative exists → flag to user: "NC asset excluded; provide licensed alternative or accept non-commercial restriction."

### Example 3 — Font for branded report

Request: "use Futura for the deck". Futura is proprietary (not OFL). Decision: flag that Futura requires a license; if the org has it installed/licensed, use with fallback chain `Futura, Century Gothic, Trebuchet MS, sans-serif`; if not, substitute `Montserrat` (OFL, similar geometric sans) and note the substitution in assumptions.

### Example 4 — Ambiguous license → escalate

Blog image found via web search shows "© Author, some rights reserved" with no license link. Decision: classify `unknown`, exclude from deliverable, report to user: "Image X has no verifiable license — excluded. Provide a licensed alternative or confirm permission."

## Quality Standards

- 100% of placed assets have a complete register entry with all verification fields.
- No NC/ND/unknown assets in commercial deliverables — enforced, not advisory.
- Attribution text matches the license's required style (CC requires "BY" credit + license link; check specific license terms).
- Every exclusion is documented with reason so the user can override deliberately.
- Register is exportable as appendix/credits page for any deliverable.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
