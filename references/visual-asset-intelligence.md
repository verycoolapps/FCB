# Visual Asset Intelligence — Discovery, Licensing-Aware Sourcing, Format Handling

## Purpose

The visual asset engine finds, evaluates, prepares, and places 2D and 3D assets for Microsoft 365 deliverables. It maintains a curated source catalog with license notes, a format-conversion pipeline for 3D models (preview PNGs, SVG silhouettes), placement rules per Office app, per-context image specifications, and caching/dedup conventions. Every asset passes through the licensing rules defined in `licensing-and-attribution.md` before placement.

## Scope

In scope: 2D image sourcing (photos, illustrations, icons), 3D model sourcing and preview generation, format conversion, per-app placement, image specs (DPI, dimensions), asset caching and dedup, dead-link and format-error handling.

Out of scope: AI image generation (no generative fill in this engine); video/audio assets; font files beyond referencing `design-system.md`.

## Source Catalog

| Source | Type | License | Best for | Notes |
|---|---|---|---|---|
| **Unsplash** | Photos | Unsplash License (free commercial, no attribution required; can't resell unaltered) | Hero images, backgrounds | High-res; `images.unsplash.com` URLs stable; hotlink allowed |
| **Pexels** | Photos + video | Pexels License (free commercial, attribution appreciated) | Photos, presenter shots | Clean API; stable CDN URLs |
| **Pixabay** | Photos, illustrations, vectors | Pixabay Content License (free, no attribution) | Mixed media, vectors | Includes illustrations + vectors beyond photos |
| **Wikimedia Commons** | Photos, diagrams, maps | Per-file (CC, PD, GFDL) | Diagrams, historical, scientific | **License varies per file — verify each** |
| **Openverse** (WordPress) | Aggregated CC/PD | Varies per result | Broad CC search | API returns license field per item |
| **Smithsonian Open Access** | Museum objects, artworks | CC0 (3M+ items) | Cultural, scientific, art | High-quality scans; truly public domain |
| **NASA Image Library** | Space/earth imagery | Public domain (US Gov) | Tech, science decks | No attribution required; some usage guidelines |
| **Poly Haven** | HDRIs, textures, models | CC0 | 3D textures, HDRIs | GLB models + PBR textures |
| **ambientCG** | PBR textures | CC0 | Material textures | Seamless textures, 1K–8K |
| **Sketchfab** | 3D models | Per-model (CC variants + editorial) | 3D assets with preview | Check license per model; embed vs download differs |
| **Kenney.nl** | Game assets (2D/3D) | CC0 | Icons, UI, low-poly models | Huge consistent packs |
| **OpenClipart** | SVG clipart | Varies (many CC0/PD) | Icons, illustrations | Verify per-clip license |
| **Google Fonts** | Fonts | SIL OFL 1.1 | Typography | See `design-system.md`; OFL allows embedding |
| **unDraw** | Illustrations | unDraw License (free, attribution appreciated) | Spot illustrations | Customizable colors; consistent style |
| **Storyset** | Illustrations | Free license w/ attribution | Marketing illustrations | Attribution required on free tier |
| **Humaaans** | Character illustrations | CC0 / paid variants | People illustrations | Mix of free and paid packs |

**License quick-rules:** CC0/PD sources (Smithsonian, NASA, Poly Haven, ambientCG, Kenney, Openverse filtered to CC0) are safest. Unsplash/Pexels/Pixabay are free for commercial use without attribution but check their specific terms. Wikimedia/Openverse/Sketchfab/OpenClipart/Storyset require **per-item verification**. Route every item through `licensing-and-attribution.md` classification.

## 3D Format Handling Pipeline

### Format Reference

| Format | Extension | What it is for | Office relevance |
|---|---|---|---|
| **glTF / GLB** | `.gltf`, `.glb` | Modern web/real-time 3D; GLB = binary self-contained | Best for preview rendering; Blender/online viewers import directly |
| **OBJ** | `.obj` | Legacy geometry-only (needs `.mtl` for materials) | Widely supported; convert to GLB for preview |
| **STL** | `.stl` | 3D printing geometry (no color/UVs) | Manufacturing; preview possible but untextured |
| **FBX** | `.fbx` | Autodesk interchange w/ rigging/animation | Game/film assets; needs Blender/autodesk to read |
| **USDZ** | `.usdz` | Apple AR Quick Look | iOS AR; preview via macOS Quick Look |
| **BLEND** | `.blend` | Native Blender | Requires Blender to open/export |
| **STEP** | `.step`, `.stp` | CAD B-rep (engineering) | CAD viewers; not for raster preview without CAD kernel |
| **IFC** | `.ifc` | BIM/AEC building models | Architecture; heavy, needs BIM tools |

### Pipeline: Source → Preview

```
source file → identify format → route converter → produce deliverables
                                                          ├── preview PNG (for docs/slides)
                                                          ├── SVG silhouette (for diagrams)
                                                          └── metadata record (license, source URL, date)
```

**Conversion paths:**

- **glTF/GLB:** load with `pygltflib` or `trimesh` (`trimesh.load('model.glb')`); render preview via `trimesh.scene.Scene.save_image()` (uses pyglet/OpenGL — headless needs `PYOPENGL_PLATFORM=egl` or xvfb) or export to Blender headless for Cycles/Eevee render.
- **OBJ/STL/FBX/BLEND:** Blender headless batch render is the reliable path:
  ```bash
  blender --background --python render_preview.py -- model.fbx out.png
  # script: import, frame camera to bounds, add 3-point lights, render PNG 1600×1200
  ```
  Set `--engine BLENDER_EEVEE_NEXT` for speed (4.x) or `CYCLES` CPU low-samples for quality.
- **USDZ:** macOS `qlmanage -t` thumbnail or Reality Converter; on Linux, convert via `usdcat`/Blender USD importer.
- **STEP/IFC:** not rasterizable without CAD/BIM kernels — treat as link-out assets ("see model file") or commission a rendered preview; do not fake a preview.
- **SVG silhouette:** derive from preview via edge-detection/trace, or request the source's wireframe render. Use for architecture/engineering diagrams where a clean outline reads better than shaded render.

**Preview render spec:** transparent or neutral background (match doc theme), 3/4 isometric-ish camera angle, consistent lighting rig across assets, 1600×1200 px master, downsample per context.

## Smart Placement Rules

| Asset | PowerPoint | Word | Excel | Outlook |
|---|---|---|---|---|
| Hero photo | Slide master / title slide background, full-bleed w/ scrim | Not typical | Dashboard header banner | Signature banner (external only, small) |
| Inline figure | Content slide, 30–40% slide width, captioned | Inline after paragraph, 4–6" wide, wrapped | N/A | Embedded in body when illustrative |
| Icon set | Consistent 1 style per deck, 32–48px on slide | Bulleted list icons, small | KPI cards, status indicators | N/A |
| Chart (native) | Native chart objects (editable) | Rare | Native charts | N/A |
| 3D preview | Rendered PNG on slide, labeled "3D preview — see appendix" | Inline figure w/ caption | N/A | N/A |
| Logo | Title + closing slide, consistent placement | Header or title page | Header | Signature block |

Rules: never stretch images (preserve aspect); every placed image gets a caption or alt-text; one visual style per deliverable (don't mix photo + flat illustration + 3D casually); heroes get scrim/dark overlay for text legibility (see `design-system.md` contrast rules).

## Image Specifications per Context

| Context | Dimensions | Resolution | Format | Notes |
|---|---|---|---|---|
| Print document (A4/Letter) | 300 DPI at final size (e.g., 6" wide → 1800px) | 300 DPI | PNG/TIFF/JPEG(high q) | JPEG artifacts bad for screenshots/diagrams |
| PPT slide (16:9) | 1920×1080 master; images ≥1600px wide | 150 DPI effective | PNG (transparency) or JPEG | SVG for logos/icons |
| Excel dashboard | 600–1200px depending on cell area | Screen-res ok | PNG | Keep file size small — many images bloat workbook |
| Word inline | width 4–6", proportional | 200+ DPI | PNG/JPEG | PNG preferred |
| Email signature | ≤600px wide, height ≤150px | 72 DPI | PNG/GIF | External sends only |
| Favicon/app icon | 16/32/48/180px set | — | PNG/ICO | Rare in Office docs |
| PDF deliverable | vector where possible | — | SVG→PDF or high-DPI PNG | Text must remain selectable — never flatten |

## Caching & Dedup Conventions

- **Cache dir:** `assets/cache/<source>/<asset-id>.<ext>` with a `manifest.json` per asset: `{id, source, source_url, license, license_url, author, date_accessed, local_path, hash_sha256, preview_path}`.
- **Dedup:** hash file contents (SHA-256) on ingest; if hash matches an existing asset, reuse the existing file and record the new source as an alias. Never store two copies of identical bytes.
- **Preview cache:** previews keyed by source-file hash + render-script version; regenerate only when either changes.
- **Expiry:** re-verify licenses of cached assets quarterly; remove assets whose license changed or link died.

## 3D-to-Document Workflow

When a request needs a 3D asset inside an Office deliverable, follow this order:

1. **Acquire** — download GLB/glTF/OBJ/STL/FBX/USDZ from a catalog (Poly Haven, Sketchfab CC-filtered, Kenney). Record license in manifest.
2. **Normalize** — convert exotic formats to glTF/GLB (Blender headless `bpy.ops.import_scene.*` then `export_scene.gltf`, or `assimp` CLI). Keep units consistent: glTF is meters; Office previews need pixel output, not real-world scale.
3. **Preview render** — render a 1024×1024 transparent-background PNG with a fixed studio rig: 3-point lighting, 45° hero angle, neutral gray background, no ground shadow unless requested. Blender headless: `blender -b -P render_preview.py -- input.glb output.png`. Cache by source hash + rig version.
4. **Embed** — place the PNG like any raster asset. For interactive 3D in docs, note that Office formats cannot embed live 3D; offer an embedded Viewer screenshot or a link to the source.
5. **CAD formats (STEP/IGES/IFC)** — these are B-rep/parametric, not mesh; they cannot be previewed without a CAD kernel. Options: request user-provided render, use FreeCAD/BlenderCAD headless tessellation to mesh then preview, or flag `requires_manual_preview` and emit a placeholder box in the deliverable.

## Smart Placement Rules per App

- **PowerPoint:** full-bleed hero on title/section slides; right-column image + left text on content slides; never place body text over busy imagery without a scrim.
- **Word:** inline figures with captions for reports; full-width band images only in marketing-style docs; keep text columns clear of images.
- **Excel:** small icons/images only in header bands or dashboard KPI cards; never inside data ranges (breaks sorting/filtering and inflates file size).
- **PDF:** vector SVG preferred for diagrams/logos; raster only for photos; always preserve selectable text — never flatten pages.
- **Outlook/email:** single hero image max, hosted or embedded under size limits; alt text mandatory since many clients block images.

## Error Handling

- **Dead link / 404:** retry once, then search source for alternate size/format; if none, mark asset `unavailable` in manifest and select a replacement from the same source category.
- **Unsupported format:** route through the pipeline table; if no converter exists (e.g., exotic CAD), mark `requires_manual_preview` and either request user-provided render or substitute a different asset.
- **License failure:** if license can't be verified, exclude asset (see `licensing-and-attribution.md` decision rules) — never place unlicensed assets silently.
- **Render failure (Blender headless):** check GPU/driver; fall back to CPU Cycles low samples; last resort `trimesh` pyglet render; if all fail, record error and flag for manual preview.
- **Hotlink rot:** download assets locally into cache rather than hotlinking — Office files must embed or link-stable images; never ship a deliverable with remote-URL images that can break.
- **Oversized files:** warn when an asset >10MB will be embedded in a doc (bloat, email size limits); suggest compressed preview instead.

## Practical Examples

**Example 1 — Deck hero.** Request: "hero image for smart-factory pitch". Engine queries Unsplash/Pexels for `smart factory`, selects CC-free photo, verifies license, downloads to cache, generates 1920×1080 crop with dark scrim zone, records manifest entry, places as title-slide background with 3-line headline in safe zone.

**Example 2 — 3D pump model in report.** User supplies `pump_assembly.step` (CAD). Engine detects STEP → no raster path → checks if user can provide STEP viewer screenshot; if Blender/FreeCAD available, attempts conversion to mesh then preview; otherwise outputs placeholder box `{{3D preview required — attach render of pump_assembly.step}}` and lists it in `action_required_from_user`.

**Example 3 — Dedup hit.** Two requests reference the same Unsplash photo ID. Second request hashes to existing cache entry → reuses file, adds alias manifest entry, no re-download, consistent preview reused.

**Example 4 — License ambiguity.** Openverse result shows `license: "by-sa"` → routes to `licensing-and-attribution.md` → classified CC BY-SA → allowed with attribution + share-alike note → engine generates attribution caption text and flags that derived assets must carry same license.

## Quality Standards

- Every placed asset has a manifest record with verified license, source URL, author, and access date.
- Previews are consistent (same camera/lighting rig) across a deliverable.
- No remote hotlinks in final files; all images embedded or local-path linked.
- Image specs match the target context table; aspect ratio preserved everywhere.
- Unverifiable assets are excluded, not silently included.

---
© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
