# 🚀 ⚡ 🛡️ FileCraftBooster

## The Microsoft Productivity Intelligence Engine

**VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-Proprietary-red)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-green)]()
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)]()

FileCraftBooster is an AI skill package that turns plain-language requests into production-grade Microsoft 365 artifacts — documents, workbooks, decks, diagrams, plans, and email — while verifying visual assets against real license terms before anything ships. It covers the full Microsoft productivity surface: Word, Excel, PowerPoint, Outlook, OneNote, Teams, OneDrive, SharePoint, Loop, Lists, Planner, Visio, Access, Project, Clipchamp, Whiteboard, Forms, Power Automate, Power Apps, Power BI, Sway, Publisher, Dynamics 365, Fabric, Azure, Entra ID, M365 Copilot, Microsoft Graph, To Do, Bookings, and Stream.

It is not a wrapper around a single API. It is a routing engine: it understands intent, selects the correct application and file format, loads only the reference material it needs, executes deterministic scripts for file generation, and runs a seven-level quality gate before delivery.

---

## Table of Contents

- [Key Features](#key-features)
- [How It Works — The Pipeline](#how-it-works--the-pipeline)
- [Installation](#installation)
- [Requirements](#requirements)
- [Folder Architecture](#folder-architecture)
- [Supported Microsoft Applications](#supported-microsoft-applications)
- [Supported File Formats](#supported-file-formats)
- [Visual Asset & Licensing Policy](#visual-asset--licensing-policy)
- [Security Considerations](#security-considerations)
- [Usage Examples](#usage-examples)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Version Info](#version-info)

---

## Key Features

| Feature | What it does |
|---|---|
| **Intent recognition** | 12-question recognition layer classifies the request before touching any file |
| **Application routing** | Maps each request to the correct Microsoft app, format, and workflow |
| **Workflow orchestration** | Nine-stage pipeline: UNDERSTAND → PLAN → DESIGN → RESEARCH → CREATE → AUTOMATE → ENHANCE → VALIDATE → DELIVER |
| **Deterministic generators** | Six Python scripts produce real DOCX/XLSX/PPTX files via `python-docx`, `openpyxl`, `python-pptx` |
| **Asset intelligence** | Discovers 2D/3D assets, verifies license class, generates attribution registers |
| **Design systems** | Eight built-in design categories plus Feng Shui-inspired optional palettes |
| **Cross-app workflows** | Four canonical multi-app patterns: business proposal, construction project, corporate management, education |
| **Seven-level QA** | Structural, content, visual, functional, accessibility, security, and delivery checks |
| **Graceful degradation** | Works fully offline for file generation; cloud features activate only when real auth exists |

---

## How It Works — The Pipeline

```mermaid
flowchart LR
    A[UNDERSTAND] --> B[PLAN]
    B --> C[DESIGN]
    C --> D[RESEARCH]
    D --> E[CREATE]
    E --> F[AUTOMATE]
    F --> G[ENHANCE]
    G --> H[VALIDATE]
    H --> I[DELIVER]

    style A fill:#1a5276,color:#fff
    style B fill:#1a6b3c,color:#fff
    style C fill:#6c3483,color:#fff
    style D fill:#7d6608,color:#fff
    style E fill:#922b21,color:#fff
    style F fill:#1a5276,color:#fff
    style G fill:#1a6b3c,color:#fff
    style H fill:#6c3483,color:#fff
    style I fill:#117a65,color:#fff
```

| Stage | Responsibility |
|---|---|
| **UNDERSTAND** | Classify intent, audience, deliverable type, constraints |
| **PLAN** | Select apps, formats, workflow, required references |
| **DESIGN** | Pick design system, palette, typography, layout rules |
| **RESEARCH** | Gather facts, assets, license verification where needed |
| **CREATE** | Generate files via scripts or structured templates |
| **AUTOMATE** | Apply cross-app steps (mail merge, exports, follow-ups) |
| **ENHANCE** | Improve existing documents without destroying content |
| **VALIDATE** | Run 7-level QA: structure, content, visuals, function, a11y, security, delivery |
| **DELIVER** | Package, name, version, attribute, and summarize output |

---

## Installation

```bash
# 1. Clone or copy the package
git clone <your-repo-url> FileCraftBooster
cd FileCraftBooster

# 2. Install Python dependencies
pip install python-docx openpyxl python-pptx Pillow reportlab

# 3. Verify scripts compile
python3 -m py_compile scripts/*.py

# 4. Point your AI assistant at the package
#    SKILL.md is the entry point — load it as a skill/module.
```

No build step, no daemon, no network requirement for core file generation.

---

## Requirements

| Requirement | Minimum | Notes |
|---|---|---|
| Python | 3.10+ | Scripts use `from __future__ import annotations` and type hints |
| `python-docx` | latest | Word DOCX generation + validation |
| `openpyxl` | latest | Excel XLSX generation + formula scanning |
| `python-pptx` | latest | PowerPoint PPTX generation + validation |
| `Pillow` | latest | Image inspection, optimization, format checks |
| `reportlab` | latest | Optional: PDF generation/inspection |
| OS | macOS / Linux / Windows | No OS-specific calls |

> **Graceful degradation:** If a dependency is missing, each script checks at startup, prints the exact `pip install` command, and exits cleanly. Document analysis and enhancement workflows degrade to text-level operations rather than failing.

---

## Folder Architecture

```
FileCraftBooster/                    (33 files total)
├── README.md                        ← you are here
├── SKILL.md                         operational entry point + routing brain
├── references/                      (19 files — deep knowledge modules)
│   ├── architecture.md              modular skill architecture & orchestration
│   ├── microsoft-ecosystem.md       full M365 app coverage + capability tiers
│   ├── word-engine.md               DOCX via python-docx / OOXML
│   ├── excel-engine.md              XLSX, formulas, dashboards, Power Query
│   ├── powerpoint-engine.md         PPTX storytelling, layouts, charts
│   ├── outlook-engine.md            email drafting via Graph (consent-gated)
│   ├── collaboration-engine.md      OneNote/Teams/SharePoint/Planner/Loop
│   ├── visual-asset-intelligence.md 2D/3D discovery, format pipelines
│   ├── licensing-and-attribution.md license classes, verification, register
│   ├── design-system.md             8 design categories + typography rules
│   ├── feng-shui-design.md          element palettes (optional, non-superstitious)
│   ├── cross-app-workflows.md       4 canonical multi-app patterns
│   ├── document-quality-assurance.md 7-level QA framework
│   ├── security-and-privacy.md      connectivity levels A/B/C, least privilege
│   ├── accessibility.md             WCAG-oriented document accessibility
│   ├── microsoft-api-integration.md Graph API, Office.js, auth honesty
│   ├── document-enhancement.md      inspect→analyze→enhance→validate flow
│   ├── advanced-document-patterns.md RAB/BOQ, SOP, KPI dashboards, decks
│   └── troubleshooting.md           failure modes + diagnostics
├── workflows/                       (6 files — executable process flows)
│   ├── document-production.md
│   ├── spreadsheet-production.md
│   ├── presentation-production.md
│   ├── visual-research-workflow.md
│   ├── enterprise-workflow.md
│   └── final-delivery-workflow.md
└── scripts/                         (6 files — real executable Python)
    ├── document_generator.py        DOCX reports (cover, TOC, tables, headers)
    ├── spreadsheet_generator.py     XLSX models + dashboards + charts
    ├── presentation_generator.py    PPTX decks, 16:9, speaker notes
    ├── visual_asset_manager.py      license-filtered asset pipeline
    ├── document_validator.py        PASS/FAIL QA for docx/xlsx/pptx/pdf
    └── asset_license_auditor.py     license audit → report.md + CSV
```

---

## Supported Microsoft Applications

| Tier | Applications | What FileCraftBooster does |
|---|---|---|
| **Core productivity** | Word, Excel, PowerPoint, Outlook | Generate/enhance DOCX, XLSX, PPTX; draft emails (send = consent-gated) |
| **Notes & comms** | OneNote, Teams, To Do, Bookings | Structured notes, meeting prep, task plans, booking summaries |
| **Files & collaboration** | OneDrive, SharePoint, Loop, Lists, Planner | Folder plans, site structures, shared trackers, sprint boards |
| **Data & BI** | Power BI, Fabric, Lists, Dynamics 365 | Dashboard specs, dataset documentation, CRM report scaffolds |
| **Automation & low-code** | Power Automate, Power Apps, Forms, Stream | Flow specifications, app mockups, form design, video plans |
| **Design & PM** | Visio, Whiteboard, Project, Access, Clipchamp, Sway, Publisher | Diagram specs, storyboards, project plans, DB schemas, publish layouts |
| **Identity & platform** | Azure, Entra ID, M365 Copilot, Microsoft Graph | Auth guidance, Graph endpoint plans, Copilot prompt packs |

> **Honesty note:** File generation is fully local. Anything requiring a live Microsoft 365 tenant (sending mail, writing to SharePoint, calling Graph) requires real OAuth credentials and explicit user authorization — see [Security Considerations](#security-considerations).

---

## Supported File Formats

| Category | Formats | Notes |
|---|---|---|
| **Documents** | DOCX, PDF, RTF, HTML, TXT | DOCX via python-docx; PDF via reportlab/inspection |
| **Spreadsheets** | XLSX, XLSM, CSV | XLSX via openpyxl; formula-error scanning built in |
| **Presentations** | PPTX, PDF | PPTX via python-pptx; 16:9 theme system |
| **Images** | SVG, PNG, JPG, WebP | Pillow-verified; optimized before insertion |
| **3D assets** | GLB, glTF, OBJ, STL, FBX, USDZ, BLEND, STEP, IFC | **Requires conversion** to PNG/SVG preview before use in Office docs — see pipeline note below |

> **3D conversion caveat:** Office documents cannot embed native STEP/IFC/BLEND. The pipeline renders/converts to raster or SVG previews first. Conversion quality depends on available local tools (e.g., Blender, trimesh); the skill never pretends a 3D file was "inserted" when only a preview was.

---

## Visual Asset & Licensing Policy

Every asset that enters a deliverable passes through classification before use. "Found on the internet" is not a license.

### License classes

| Class | Commercial use | Modification | Attribution | Default verdict |
|---|---|---|---|---|
| CC0 / Public Domain | ✅ | ✅ | Optional | **ALLOW** |
| CC BY | ✅ | ✅ | **Required** | **ALLOW + register** |
| CC BY-SA | ✅ | ✅ (share-alike) | Required | **ALLOW + register + note SA** |
| CC BY-NC | ❌ | ✅ | Required | **NON-COMMERCIAL ONLY** |
| CC BY-ND | ✅ | ❌ | Required | **NO DERIVATIVES** |
| Proprietary / stock | Per license | Per license | Per license | **REVIEW required** |
| Unknown / unverifiable | ? | ? | ? | **BLOCK** |

### Attribution register

`visual_asset_manager.py` emits `attribution_register.csv` with columns: `file, source, creator, license, license_url, attribution_text, commercial_ok, modification_ok`. `asset_license_auditor.py` produces `license_audit_report.md` + CSV with per-asset verdicts and risk flags.

---

## Security Considerations

FileCraftBooster defines three connectivity levels:

| Level | Scope | Examples | Guardrails |
|---|---|---|---|
| **A — Local** | File generation only, zero network | DOCX/XLSX/PPTX scripts, validators, asset scanning | Default mode; no credentials needed |
| **B — Cloud read/integration** | Microsoft Graph, Entra ID, OAuth | Fetching templates, resolving users, reading SharePoint metadata | OAuth only; least-privilege scopes; tokens never stored in files |
| **C — Workflow automation** | Power Automate / external actions | Sending email, posting to Teams, writing to SharePoint | **Explicit per-action consent**; dry-run preview; audit log |

**Rules that apply at every level:**

- **Least privilege** — request the minimum Graph scopes the task needs
- **No hardcoded secrets** — credentials come from env vars or the OS keychain, never from generated files
- **Consent for destructive/external actions** — sending, deleting, publishing, or overwriting requires explicit confirmation
- **No silent fallback** — if auth fails, the skill reports it; it does not pretend the cloud step succeeded
- **Audit trail** — Level B/C actions are logged in the delivery summary

---

## Usage Examples

Prompt → output. These are the shapes of request the skill is built for.

### Documents

```
"Create a 12-page project proposal DOCX for a hospital IT modernization,
with executive summary, timeline table, and budget section."
→ document-production workflow → document_generator.py → proposal.docx → document_validator.py PASS
```

```
"Turn this messy meeting transcript into a clean OneNote-ready action
items doc with owners and deadlines."
→ document-enhancement → structured DOCX with tables
```

### Spreadsheets

```
"Build an Excel financial model for a 3-year SaaS projection:
revenue, COGS, opex, EBITDA, cash flow, with a dashboard sheet."
→ spreadsheet-production → spreadsheet_generator.py → model.xlsx
  (formulas: XLOOKUP, LET, LAMBDA, dynamic arrays where appropriate)
```

### Presentations

```
"Make a 10-slide investor deck for our pre-seed round, Series-A style
visual hierarchy, speaker notes on every slide."
→ presentation-production → presentation_generator.py → deck.pptx
```

### Assets

```
"Find hero images for the proposal — commercial use only, generate the
attribution register."
→ visual-research-workflow → license filter → attribution_register.csv
```

### Cross-app

```
"Package a construction project kickoff: proposal DOCX + BOQ XLSX +
Gantt-style PPTX + Teams channel plan + SharePoint folder structure."
→ enterprise-workflow → per-app deliverables → final-delivery QA
```

---

## Limitations

Read this before relying on the package for anything client-facing.

- **Cloud features need real auth.** Anything touching a live M365 tenant (send mail, write to SharePoint, call Graph) requires valid OAuth credentials. Without them, the skill produces the *plan and files*, not the live action — and says so.
- **No fake API claims.** FileCraftBooster does not simulate Microsoft Graph responses. If a step needs the network and none exists, it reports the gap.
- **3D formats need conversion.** GLB/STEP/IFC/BLEND cannot be embedded natively in Office files; a preview (PNG/SVG) is produced instead. Conversion fidelity depends on local tooling.
- **PDF is inspect-and-generate, not full Acrobat.** Complex PDF editing (form filling, redaction) is out of scope.
- **Design systems are rules, not themes.** The 8 design categories guide typography/color/layout; they do not ship `.thmx` files.
- **Feng Shui palettes are optional aesthetics.** The skill never fabricates birth-data analysis or makes superstitious claims.

---

## Troubleshooting

<details>
<summary><b>Script exits with "Missing dependency"</b></summary>

Each script checks its imports at startup and prints the exact install command. Run it:

```bash
pip install python-docx openpyxl python-pptx Pillow reportlab
```

If `pip` targets the wrong Python, use `python3 -m pip install ...`.

</details>

<details>
<summary><b>document_validator.py reports FAIL on a file I just generated</b></summary>

Run with `--json` for machine-readable detail. Common causes:

- **Empty document** — a section spec had no body text; re-run with content
- **Formula errors in XLSX** — scan flags `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`; fix the formula spec
- **PDF FAIL** — missing `%PDF` header or EOF marker; the file is corrupt or not a PDF

</details>

<details>
<summary><b>License audit blocks an asset I want to use</b></summary>

`Unknown` license → **BLOCK** by design. Either find a licensed alternative, provide a license file/URL as evidence, or accept the risk explicitly (the audit report records your override). `CC BY-NC` assets cannot be used in commercial deliverables; `CC BY-ND` assets cannot be modified — including cropping or recoloring.

</details>

<details>
<summary><b>Graph / Outlook step fails with auth error</b></summary>

Expected behavior at Level B/C without credentials. The skill will:

1. Report the missing scope or token
2. Offer the Level A fallback (draft the email/file locally)
3. Wait for explicit authorization before any send/write action

Do not paste tokens into prompts or generated files — use env vars.

</details>

<details>
<summary><b>Generated PPTX looks generic</b></summary>

The deck follows the selected design system (8 categories). If the output looks flat, specify the category explicitly in the prompt (e.g., "luxury editorial style" or "financial & analytical"). Typography defaults to Aptos/Calibri for corporate, Georgia/Cambria for editorial, Segoe UI for technology.

</details>

<details>
<summary><b>3D asset preview is low quality</b></summary>

Preview rendering uses whatever local converter is available. For better results, pre-convert with Blender (`blender --background --python export.py`) to a high-res PNG or SVG, then reference the converted file. The skill will not upscale or fake detail.

</details>

---

## Version Info

| | |
|---|---|
| **Version** | 1.0.0 |
| **Release date** | November 2026 |
| **Author** | VeryCoolApps — PT. Agra Karya Digital |
| **Website** | www.vcadeveloper.com |
| **License** | Proprietary — All rights reserved |
| **Python** | 3.10+ |

---

# Bahasa Indonesia

## 🚀 ⚡ 🛡️ FileCraftBooster

## Mesin Kecerdasan Produktivitas Microsoft

**VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com**

FileCraftBooster adalah paket skill AI yang mengubah permintaan berbahasa sehari-hari menjadi artefak Microsoft 365 siap produksi — dokumen, workbook, presentasi, diagram, rencana, dan email — sekaligus memverifikasi aset visual terhadap ketentuan lisensi sebelum apa pun dikirim. Cakupannya meliputi seluruh permukaan produktivitas Microsoft: Word, Excel, PowerPoint, Outlook, OneNote, Teams, OneDrive, SharePoint, Loop, Lists, Planner, Visio, Access, Project, Clipchamp, Whiteboard, Forms, Power Automate, Power Apps, Power BI, Sway, Publisher, Dynamics 365, Fabric, Azure, Entra ID, M365 Copilot, Microsoft Graph, To Do, Bookings, dan Stream.

Ini bukan sekadar pembungkus satu API. Ini adalah mesin routing: memahami maksud, memilih aplikasi dan format yang benar, memuat hanya referensi yang dibutuhkan, menjalankan skrip deterministik untuk pembuatan file, dan menerapkan gerbang kualitas tujuh tingkat sebelum pengiriman.

---

## Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Cara Kerja — Pipeline](#cara-kerja--pipeline)
- [Instalasi](#instalasi)
- [Kebutuhan Sistem](#kebutuhan-sistem)
- [Arsitektur Folder](#arsitektur-folder)
- [Aplikasi Microsoft yang Didukung](#aplikasi-microsoft-yang-didukung)
- [Format File yang Didukung](#format-file-yang-didukung)
- [Kebijakan Aset Visual & Lisensi](#kebijakan-aset-visual--lisensi)
- [Pertimbangan Keamanan](#pertimbangan-keamanan)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Keterbatasan](#keterbatasan)
- [Pemecahan Masalah](#pemecahan-masalah)
- [Info Versi](#info-versi)

---

## Fitur Utama

| Fitur | Fungsi |
|---|---|
| **Pengenalan maksud** | Lapisan pengenalan 12 pertanyaan mengklasifikasikan permintaan sebelum menyentuh file |
| **Routing aplikasi** | Memetakan setiap permintaan ke aplikasi, format, dan workflow Microsoft yang tepat |
| **Orkestrasi workflow** | Pipeline sembilan tahap: UNDERSTAND → PLAN → DESIGN → RESEARCH → CREATE → AUTOMATE → ENHANCE → VALIDATE → DELIVER |
| **Generator deterministik** | Enam skrip Python menghasilkan file DOCX/XLSX/PPTX nyata via `python-docx`, `openpyxl`, `python-pptx` |
| **Kecerdasan aset** | Menemukan aset 2D/3D, memverifikasi kelas lisensi, menghasilkan register atribusi |
| **Sistem desain** | Delapan kategori desain bawaan plus palet opsional bernuansa Feng Shui |
| **Workflow lintas aplikasi** | Empat pola multi-app kanonik: proposal bisnis, proyek konstruksi, manajemen korporat, pendidikan |
| **QA tujuh tingkat** | Pemeriksaan struktural, konten, visual, fungsional, aksesibilitas, keamanan, dan pengiriman |
| **Degradasi anggun** | Berfungsi penuh offline untuk pembuatan file; fitur cloud aktif hanya jika autentikasi nyata tersedia |

---

## Cara Kerja — Pipeline

```mermaid
flowchart LR
    A[UNDERSTAND] --> B[PLAN]
    B --> C[DESIGN]
    C --> D[RESEARCH]
    D --> E[CREATE]
    E --> F[AUTOMATE]
    F --> G[ENHANCE]
    G --> H[VALIDATE]
    H --> I[DELIVER]

    style A fill:#1a5276,color:#fff
    style B fill:#1a6b3c,color:#fff
    style C fill:#6c3483,color:#fff
    style D fill:#7d6608,color:#fff
    style E fill:#922b21,color:#fff
    style F fill:#1a5276,color:#fff
    style G fill:#1a6b3c,color:#fff
    style H fill:#6c3483,color:#fff
    style I fill:#117a65,color:#fff
```

| Tahap | Tanggung jawab |
|---|---|
| **UNDERSTAND** | Mengklasifikasikan maksud, audiens, jenis deliverable, dan batasan |
| **PLAN** | Memilih aplikasi, format, workflow, dan referensi yang diperlukan |
| **DESIGN** | Menentukan sistem desain, palet, tipografi, dan aturan tata letak |
| **RESEARCH** | Mengumpulkan fakta, aset, dan verifikasi lisensi bila diperlukan |
| **CREATE** | Menghasilkan file melalui skrip atau template terstruktur |
| **AUTOMATE** | Menerapkan langkah lintas aplikasi (mail merge, ekspor, tindak lanjut) |
| **ENHANCE** | Meningkatkan dokumen yang ada tanpa merusak konten |
| **VALIDATE** | Menjalankan QA 7 tingkat: struktur, konten, visual, fungsi, aksesibilitas, keamanan, pengiriman |
| **DELIVER** | Mengemas, menamai, memberi versi, atribusi, dan merangkum output |

---

## Instalasi

```bash
# 1. Kloning atau salin paket
git clone <url-repo-anda> FileCraftBooster
cd FileCraftBooster

# 2. Instal dependensi Python
pip install python-docx openpyxl python-pptx Pillow reportlab

# 3. Verifikasi skrip terkompilasi
python3 -m py_compile scripts/*.py

# 4. Arahkan asisten AI Anda ke paket ini
#    SKILL.md adalah titik masuk — muat sebagai skill/modul.
```

Tanpa langkah build, tanpa daemon, tanpa kebutuhan jaringan untuk pembuatan file inti.

---

## Kebutuhan Sistem

| Kebutuhan | Minimum | Catatan |
|---|---|---|
| Python | 3.10+ | Skrip menggunakan `from __future__ import annotations` dan type hints |
| `python-docx` | terbaru | Pembuatan + validasi DOCX Word |
| `openpyxl` | terbaru | Pembuatan XLSX Excel + pemindaian formula |
| `python-pptx` | terbaru | Pembuatan + validasi PPTX PowerPoint |
| `Pillow` | terbaru | Inspeksi gambar, optimasi, cek format |
| `reportlab` | terbaru | Opsional: pembuatan/inspeksi PDF |
| OS | macOS / Linux / Windows | Tidak ada panggilan khusus OS |

> **Degradasi anggun:** Jika dependensi tidak ada, setiap skrip memeriksanya saat startup, mencetak perintah `pip install` yang tepat, dan keluar dengan bersih. Alur analisis dan peningkatan dokumen turun ke operasi level teks alih-alih gagal total.

---

## Arsitektur Folder

```
FileCraftBooster/                    (total 33 file)
├── README.md                        ← Anda berada di sini
├── SKILL.md                         titik masuk operasional + otak routing
├── references/                      (19 file — modul pengetahuan mendalam)
│   ├── architecture.md              arsitektur skill modular & orkestrasi
│   ├── microsoft-ecosystem.md       cakupan penuh aplikasi M365 + tier kemampuan
│   ├── word-engine.md               DOCX via python-docx / OOXML
│   ├── excel-engine.md              XLSX, formula, dashboard, Power Query
│   ├── powerpoint-engine.md         storytelling PPTX, layout, grafik
│   ├── outlook-engine.md            penyusunan email via Graph (berlisensi persetujuan)
│   ├── collaboration-engine.md      OneNote/Teams/SharePoint/Planner/Loop
│   ├── visual-asset-intelligence.md penemuan aset 2D/3D, pipeline format
│   ├── licensing-and-attribution.md kelas lisensi, verifikasi, register
│   ├── design-system.md             8 kategori desain + aturan tipografi
│   ├── feng-shui-design.md          palet elemen (opsional, non-superstitif)
│   ├── cross-app-workflows.md       4 pola multi-app kanonik
│   ├── document-quality-assurance.md kerangka QA 7 tingkat
│   ├── security-and-privacy.md      level konektivitas A/B/C, least privilege
│   ├── accessibility.md             aksesibilitas dokumen berorientasi WCAG
│   ├── microsoft-api-integration.md Graph API, Office.js, kejujuran auth
│   ├── document-enhancement.md      alur inspect→analyze→enhance→validate
│   ├── advanced-document-patterns.md pola RAB/BOQ, SOP, dashboard KPI, deck
│   └── troubleshooting.md           mode kegagalan + diagnostik
├── workflows/                       (6 file — alur proses yang dapat dieksekusi)
│   ├── document-production.md
│   ├── spreadsheet-production.md
│   ├── presentation-production.md
│   ├── visual-research-workflow.md
│   ├── enterprise-workflow.md
│   └── final-delivery-workflow.md
└── scripts/                         (6 file — Python nyata yang dapat dieksekusi)
    ├── document_generator.py        laporan DOCX (cover, TOC, tabel, header)
    ├── spreadsheet_generator.py     model XLSX + dashboard + grafik
    ├── presentation_generator.py    deck PPTX, 16:9, speaker notes
    ├── visual_asset_manager.py      pipeline aset terfilter lisensi
    ├── document_validator.py        QA PASS/FAIL untuk docx/xlsx/pptx/pdf
    └── asset_license_auditor.py     audit lisensi → report.md + CSV
```

---

## Aplikasi Microsoft yang Didukung

| Tingkat | Aplikasi | Yang dilakukan FileCraftBooster |
|---|---|---|
| **Produktivitas inti** | Word, Excel, PowerPoint, Outlook | Menghasilkan/meningkatkan DOCX, XLSX, PPTX; menyusun email (kirim = memerlukan persetujuan) |
| **Catatan & komunikasi** | OneNote, Teams, To Do, Bookings | Catatan terstruktur, persiapan rapat, rencana tugas, ringkasan booking |
| **File & kolaborasi** | OneDrive, SharePoint, Loop, Lists, Planner | Rencana folder, struktur situs, tracker bersama, papan sprint |
| **Data & BI** | Power BI, Fabric, Lists, Dynamics 365 | Spesifikasi dashboard, dokumentasi dataset, scaffold laporan CRM |
| **Otomasi & low-code** | Power Automate, Power Apps, Forms, Stream | Spesifikasi flow, mockup aplikasi, desain formulir, rencana video |
| **Desain & PM** | Visio, Whiteboard, Project, Access, Clipchamp, Sway, Publisher | Spesifikasi diagram, storyboard, rencana proyek, skema DB, tata letak publikasi |
| **Identitas & platform** | Azure, Entra ID, M365 Copilot, Microsoft Graph | Panduan auth, rencana endpoint Graph, paket prompt Copilot |

> **Catatan kejujuran:** Pembuatan file sepenuhnya lokal. Apa pun yang memerlukan tenant Microsoft 365 langsung (mengirim email, menulis ke SharePoint, memanggil Graph) membutuhkan kredensial OAuth nyata dan otorisasi eksplisit pengguna — lihat [Pertimbangan Keamanan](#pertimbangan-keamanan).

---

## Format File yang Didukung

| Kategori | Format | Catatan |
|---|---|---|
| **Dokumen** | DOCX, PDF, RTF, HTML, TXT | DOCX via python-docx; PDF via reportlab/inspeksi |
| **Spreadsheet** | XLSX, XLSM, CSV | XLSX via openpyxl; pemindaian error formula bawaan |
| **Presentasi** | PPTX, PDF | PPTX via python-pptx; sistem tema 16:9 |
| **Gambar** | SVG, PNG, JPG, WebP | Diverifikasi Pillow; dioptimalkan sebelum disisipkan |
| **Aset 3D** | GLB, glTF, OBJ, STL, FBX, USDZ, BLEND, STEP, IFC | **Memerlukan konversi** ke pratinjau PNG/SVG sebelum digunakan di dokumen Office — lihat catatan pipeline di bawah |

> **Peringatan konversi 3D:** Dokumen Office tidak dapat menyematkan STEP/IFC/BLEND secara native. Pipeline merender/mengonversi ke pratinjau raster atau SVG terlebih dahulu. Kualitas konversi bergantung pada alat lokal yang tersedia (misalnya Blender, trimesh); skill tidak akan berpura-pura file 3D "disisipkan" ketika hanya pratinjau yang dihasilkan.

---

## Kebijakan Aset Visual & Lisensi

Setiap aset yang masuk ke deliverable melewati klasifikasi sebelum digunakan. "Ditemukan di internet" bukanlah lisensi.

### Kelas lisensi

| Kelas | Penggunaan komersial | Modifikasi | Atribusi | Verdict default |
|---|---|---|---|---|
| CC0 / Domain Publik | ✅ | ✅ | Opsional | **IZINKAN** |
| CC BY | ✅ | ✅ | **Wajib** | **IZINKAN + register** |
| CC BY-SA | ✅ | ✅ (share-alike) | Wajib | **IZINKAN + register + catat SA** |
| CC BY-NC | ❌ | ✅ | Wajib | **KHUSUS NON-KOMERSIAL** |
| CC BY-ND | ✅ | ❌ | Wajib | **TANPA DERIVATIF** |
| Proprietary / stok | Sesuai lisensi | Sesuai lisensi | Sesuai lisensi | **PERLU REVIEW** |
| Tidak diketahui / tak terverifikasi | ? | ? | ? | **BLOKIR** |

### Register atribusi

`visual_asset_manager.py` menghasilkan `attribution_register.csv` dengan kolom: `file, source, creator, license, license_url, attribution_text, commercial_ok, modification_ok`. `asset_license_auditor.py` menghasilkan `license_audit_report.md` + CSV dengan verdict per aset dan flag risiko.

---

## Pertimbangan Keamanan

FileCraftBooster mendefinisikan tiga level konektivitas:

| Level | Cakupan | Contoh | Pengaman |
|---|---|---|---|
| **A — Lokal** | Hanya pembuatan file, tanpa jaringan | Skrip DOCX/XLSX/PPTX, validator, pemindaian aset | Mode default; tanpa kredensial |
| **B — Integrasi cloud baca** | Microsoft Graph, Entra ID, OAuth | Mengambil template, resolve pengguna, membaca metadata SharePoint | Hanya OAuth; scope least-privilege; token tidak pernah disimpan di file |
| **C — Otomasi workflow** | Power Automate / aksi eksternal | Mengirim email, posting ke Teams, menulis ke SharePoint | **Persetujuan eksplisit per aksi**; pratinjau dry-run; log audit |

**Aturan yang berlaku di setiap level:**

- **Least privilege** — meminta scope Graph minimum yang dibutuhkan tugas
- **Tanpa rahasia hardcoded** — kredensial berasal dari env var atau keychain OS, tidak pernah dari file yang dihasilkan
- **Persetujuan untuk aksi destruktif/eksternal** — mengirim, menghapus, menerbitkan, atau menimpa memerlukan konfirmasi eksplisit
- **Tanpa fallback diam-diam** — jika auth gagal, skill melaporkannya; tidak berpura-pura langkah cloud berhasil
- **Jejak audit** — aksi Level B/C dicatat dalam ringkasan pengiriman

---

## Contoh Penggunaan

Prompt → output. Berikut bentuk permintaan yang menjadi target skill ini.

### Dokumen

```
"Buat proposal proyek DOCX 12 halaman untuk modernisasi TI rumah sakit,
dengan ringkasan eksekutif, tabel timeline, dan bagian anggaran."
→ workflow document-production → document_generator.py → proposal.docx → document_validator.py PASS
```

```
"Ubah transkrip rapat yang berantakan ini menjadi dokumen item aksi
yang rapi untuk OneNote, dengan penanggung jawab dan tenggat."
→ document-enhancement → DOCX terstruktur dengan tabel
```

### Spreadsheet

```
"Bangun model keuangan Excel untuk proyeksi SaaS 3 tahun:
pemasukan, HPP, opex, EBITDA, arus kas, dengan sheet dashboard."
→ workflow spreadsheet-production → spreadsheet_generator.py → model.xlsx
  (formula: XLOOKUP, LET, LAMBDA, dynamic array bila sesuai)
```

### Presentasi

```
"Buat deck investor 10 slide untuk putaran pre-seed kami,
hierarki visual gaya Series-A, speaker notes di setiap slide."
→ workflow presentation-production → presentation_generator.py → deck.pptx
```

### Aset

```
"Cari gambar hero untuk proposal — hanya penggunaan komersial,
buatkan register atribusinya."
→ visual-research-workflow → filter lisensi → attribution_register.csv
```

### Lintas aplikasi

```
"Kemas kickoff proyek konstruksi: proposal DOCX + BOQ XLSX +
Gantt-style PPTX + rencana channel Teams + struktur folder SharePoint."
→ enterprise-workflow → deliverable per aplikasi → QA final-delivery
```

---

## Keterbatasan

Baca ini sebelum mengandalkan paket untuk hal yang menyangkut klien.

- **Fitur cloud memerlukan auth nyata.** Apa pun yang menyentuh tenant M365 langsung (kirim email, tulis ke SharePoint, panggil Graph) membutuhkan kredensial OAuth valid. Tanpa itu, skill menghasilkan *rencana dan file*, bukan aksi langsung — dan mengatakannya.
- **Tanpa klaim API palsu.** FileCraftBooster tidak mensimulasikan respons Microsoft Graph. Jika suatu langkah memerlukan jaringan dan tidak ada, ia melaporkan celahnya.
- **Format 3D perlu konversi.** GLB/STEP/IFC/BLEND tidak dapat disematkan native di file Office; pratinjau (PNG/SVG) dihasilkan sebagai gantinya. Fidelitas konversi bergantung pada tooling lokal.
- **PDF adalah inspeksi-dan-buat, bukan Acrobat penuh.** Pengeditan PDF kompleks (pengisian formulir, redaksi) di luar cakupan.
- **Sistem desain adalah aturan, bukan tema.** 8 kategori desain memandu tipografi/warna/tata letak; tidak mengirim file `.thmx`.
- **Palet Feng Shui bersifat opsional secara estetika.** Skill tidak pernah membuat analisis data kelahiran palsu atau klaim superstitif.

---

## Pemecahan Masalah

<details>
<summary><b>Skrip keluar dengan "Missing dependency"</b></summary>

Setiap skrip memeriksa impornya saat startup dan mencetak perintah instalasi yang tepat. Jalankan:

```bash
pip install python-docx openpyxl python-pptx Pillow reportlab
```

Jika `pip` menargetkan Python yang salah, gunakan `python3 -m pip install ...`.

</details>

<details>
<summary><b>document_validator.py melaporkan FAIL pada file yang baru saya buat</b></summary>

Jalankan dengan `--json` untuk detail yang dapat dibaca mesin. Penyebab umum:

- **Dokumen kosong** — spesifikasi bagian tidak memiliki teks isi; jalankan ulang dengan konten
- **Error formula di XLSX** — pemindaian menandai `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`; perbaiki spesifikasi formula
- **PDF FAIL** — header `%PDF` atau penanda EOF hilang; file korup atau bukan PDF

</details>

<details>
<summary><b>Audit lisensi memblokir aset yang ingin saya pakai</b></summary>

Lisensi `Unknown` → **BLOKIR** sesuai desain. Temukan alternatif berlisensi, berikan file/URL lisensi sebagai bukti, atau terima risiko secara eksplisit (laporan audit mencatat override Anda). Aset `CC BY-NC` tidak boleh digunakan dalam deliverable komersial; aset `CC BY-ND` tidak boleh dimodifikasi — termasuk cropping atau recoloring.

</details>

<details>
<summary><b>Langkah Graph / Outlook gagal dengan error auth</b></summary>

Perilaku yang diharapkan pada Level B/C tanpa kredensial. Skill akan:

1. Melaporkan scope atau token yang hilang
2. Menawarkan fallback Level A (buat draft email/file secara lokal)
3. Menunggu otorisasi eksplisit sebelum aksi kirim/tulis apa pun

Jangan menempelkan token ke prompt atau file yang dihasilkan — gunakan env var.

</details>

<details>
<summary><b>PPTX yang dihasilkan terlihat generik</b></summary>

Deck mengikuti sistem desain yang dipilih (8 kategori). Jika hasilnya terlihat datar, sebutkan kategorinya secara eksplisit dalam prompt (misalnya "gaya luxury editorial" atau "financial & analytical"). Tipografi default: Aptos/Calibri untuk korporat, Georgia/Cambria untuk editorial, Segoe UI untuk teknologi.

</details>

<details>
<summary><b>Pratinjau aset 3D berkualitas rendah</b></summary>

Rendering pratinjau menggunakan konverter lokal yang tersedia. Untuk hasil lebih baik, konversi terlebih dahulu dengan Blender (`blender --background --python export.py`) ke PNG atau SVG resolusi tinggi, lalu referensikan file hasil konversi. Skill tidak akan upscale atau memalsukan detail.

</details>

---

## Info Versi

| | |
|---|---|
| **Versi** | 1.0.0 |
| **Tanggal rilis** | November 2026 |
| **Penulis** | VeryCoolApps — PT. Agra Karya Digital |
| **Situs web** | www.vcadeveloper.com |
| **Lisensi** | Proprietary — Hak cipta dilindungi |
| **Python** | 3.10+ |

---

© 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
