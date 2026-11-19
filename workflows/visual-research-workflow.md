# Workflow: Visual Research

**Purpose:** Find, verify, download, optimize, insert, and attribute visual assets — photos, illustrations, icons, logos, textures, templates — for any Microsoft 365 artifact.

---

## Trigger

Activate whenever an artifact needs imagery: "find an image for", "get me a hero photo", "need an icon for", "source a background", "this document looks bare — add visuals". Also standalone: "find me images of X with free license".

## Input

- Asset description: subject, mood, style, orientation (landscape/portrait/square), color direction.
- Usage context: document, slide, Excel dashboard, email header, social-style graphic.
- License constraint: commercial OK required? Attribution acceptable? Exclusive/paid allowed?
- Quantity needed and target dimensions.

## Preconditions

- Load references: `visual-asset-intelligence.md`, `licensing-and-attribution.md`; add `design-system.md` for style matching, `feng-shui-design.md` if harmony palette requested.
- Define the asset spec before searching: orientation, minimum resolution (≥1600px wide for full-slide, ≥1200px for document headers, ≥512px for icons), style (photo/illustration/flat/icon), color temperature.
- Decide acceptable license tiers: CC0 / public domain > CC-BY > CC-BY-SA > free-with-attribution. **Never** use "found on Google Images" without verifying the source page license.

## Step-by-Step Process

1. **SPECIFY** — Write the asset brief: what, why, where it goes, style, colors, orientation, license tier.
2. **SEARCH** — Query vetted sources from `visual-asset-intelligence.md` (Openverse, Wikimedia Commons, Unsplash/Pexels-class sources, official icon sets, Microsoft-provided assets). Prefer: exact-subject match, correct orientation, sufficient resolution, clean license.
3. **VERIFY LICENSE** — For each candidate, open the source page and confirm: license name, commercial-use permission, attribution requirement, any restrictions (ND = no derivatives — avoid for edited assets). Record: source URL, author, license, date accessed. If unverifiable → reject the asset.
4. **DOWNLOAD** — Fetch the highest usable resolution. Store in a working `assets/` folder with a clean filename: `asset_subject_source_author.ext`.
5. **OPTIMIZE** — Run `scripts/visual_asset_manager.py`: resize to target dimensions (don't ship 6000px images in a Word doc), convert to appropriate format (JPEG for photos, PNG for graphics/icons with transparency, SVG preferred for icons/logos), compress (target <500KB per image for documents, <1MB for decks).
6. **INSERT** — Place via `scripts/document_generator.py` / `scripts/presentation_generator.py` / `scripts/spreadsheet_generator.py`: correct alignment, captions if needed, consistent sizing (e.g., all document images same width or credit-line style).
7. **ATTRIBUTE** — Add attribution: visible credit line, footnote, or slide footer per license requirement; plus entry in the attribution register (mandatory for CC-BY and free-with-attribution).
8. **DELIVER** — Assets folder + attribution register go with the delivery package.

## Decision Points

- **No suitable licensed asset** → generate a native shape/diagram/icon-font composition; or use a clearly-labeled placeholder `[IMAGE NEEDED: description]` and tell the user exactly what to supply.
- **Logo request** → only use the actual brand logo if user provides it or it's from the official brand kit; never recreate a trademarked logo approximately — flag trademark concerns.
- **People/faces** → prefer diverse, professional, context-appropriate imagery; avoid stereotypes; check license covers the specific use.
- **Cultural/religious/medical imagery** → apply extra care; verify respectful representation; when in doubt, use abstract/diagrammatic visuals.
- **Feng Shui palette request** → apply `feng-shui-design.md` element-color mapping to choose/grade assets toward the palette.

## Application Routing

- **Word/Excel/PowerPoint** — insertion targets.
- **Sway/Whiteboard** — visual-heavy alternative formats.
- **SharePoint/OneDrive** — asset library storage for team reuse (link, don't send without consent).
- **Clipchamp** — if assets feed a video.

## Execution Rules

- Every asset MUST have a recorded license before insertion. No exceptions.
- Never hotlink images — always download and embed/attach the file.
- Keep a per-project `assets/` folder and `ATTRIBUTION.md` register.
- Don't modify CC-ND (NoDerivatives) assets beyond cropping/resizing for layout — prefer CC0/CC-BY/Pexels/Unsplash licenses that permit editing.
- Icons: use one consistent family/weight per artifact.
- Alt text required on every inserted image — describe content and function, not "image of".

## Validation

- License audit: every file in `assets/` has a matching register entry with source URL + license.
- Technical check: dimensions adequate for placement, format correct, file size reasonable.
- Visual check: image renders, isn't stretched, contrast with text/background is sufficient.
- Attribution check: required credits are visible or documented.

## Error Recovery

- **Source site blocks download** → try alternate source or the API; if all fail, use substitute asset or placeholder + instructions.
- **License ambiguous** → treat as unverified; find alternative. Ambiguity = rejection.
- **Image quality too low** → request higher-res from source; if none, choose different asset.
- **Broken/404 asset URL** → discard; do not ship dead references.

## Expected Outputs

- Optimized asset files in `assets/` (correct format/size).
- `ATTRIBUTION.md` register: asset | description | author | source URL | license | date.
- Inserted images with alt text and credits in the target artifact.
- Note in delivery summary: assets used, licenses, any placeholders remaining.

---

## Source Strategy

Priority order when searching (per `visual-asset-intelligence.md`):

1. **User-provided / brand kit** — always first if exists.
2. **Official/vendor sources** — Microsoft-created assets, brand press kits, government/open-data imagery (PD).
3. **CC0 / public domain** — Openverse, Wikimedia Commons, government archives, NASA, Smithsonian Open Access.
4. **Free-license stock** — Unsplash, Pexels, Pixabay-class (verify per-asset license page; rules change).
5. **CC-BY / CC-BY-SA** — acceptable with attribution; SA requires share-alike note.
6. **Paid stock** — only if user approves spend; document cost in summary.

**Never:** Google Images hotlink, Pinterest pins, random blog images, AI-generated images presented as real photos without disclosure, or "royalty-free" claims without reading the actual license text.

## Asset-Type Playbooks

### Icons
- One family per artifact (e.g., all Material Symbols or all Fluent UI).
- Consistent stroke/weight; monochrome or 2-tone; sized to grid (16/24/32/48px multiples).
- SVG preferred; PNG fallback at 2x for sharpness.

### Photos
- Match aspect ratio to placement BEFORE downloading (don't crop heads off).
- Check for embedded text/watermarks/logos in image; reject if present.
- Color temperature should harmonize with palette; note grading needs.

### Illustrations / Graphics
- Style consistency matters more than subject perfection.
- Transparent PNG/SVG for overlays; check edges aren't white-fringed.
- Avoid mixed illustration styles in one artifact.

### Logos / Brand Marks
- Only official files from brand kit or official press page.
- Never redraw, recolor beyond brand guidelines, or approximate.
- Clear-space and minimum-size rules respected.

### Backgrounds / Textures
- Subtlety: text must remain readable (contrast check at actual placement).
- Seamless tiles only if actually tileable — verify before use.
- File size matters: compress aggressively; these sit behind everything.

## License Quick-Reference

| License | Commercial | Modify | Attribute | Verdict |
|---|---|---|---|---|
| CC0 / PD | Yes | Yes | No (nice) | Preferred |
| Pexels/Unsplash-type | Yes | Yes | No (appreciated) | Preferred |
| CC-BY | Yes | Yes | Yes — required | OK with credit |
| CC-BY-SA | Yes | Yes | Yes + share-alike | OK w/ note |
| CC-BY-ND | Yes | No | Yes | Layout-only use |
| "Free for personal" | No | — | — | Reject for business |
| Unknown/"found online" | — | — | — | Reject |

## Optimization Targets

| Placement | Max dimension | Target size | Format |
|---|---|---|---|
| Document inline | 1200px wide | <300KB | JPEG/PNG |
| Slide full-bleed | 1920px wide | <800KB | JPEG |
| Icon | 48–256px | <50KB | SVG/PNG |
| Email header | 1200×400 | <150KB | JPEG |
| Print (300dpi) | per trim size | <2MB | TIFF/PNG |

## Attribution Placement Rules

- **Documents:** footnote on page of use, "Image: description — Author via Source (License)"; or consolidated credits page for many assets.
- **Slides:** tiny credit bottom-corner or appendix credits slide.
- **Excel:** cell comment or Instructions sheet entry.
- **Email:** signature-line credit only if license demands visibility; otherwise file footer.
- **Always also:** entry in `ATTRIBUTION.md` register regardless of visible credit.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
