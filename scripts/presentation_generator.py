#!/usr/bin/env python3
"""presentation_generator.py — Generate styled 16:9 PPTX decks with python-pptx.

CLI examples:
    python3 presentation_generator.py --output deck.pptx --title "Roadmap" \
        --slide "Agenda|Why now;Goals;Timeline" \
        --slide "Market|TAM $12B;Growth 18% CAGR" --force

    python3 presentation_generator.py --output deck.pptx --slides-json slides.json --force

Requires: pip install python-pptx
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Inches, Pt
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'python-pptx'. Install it with:\n"
        "    pip install python-pptx\n"
    )
    raise SystemExit(2)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("presentation_generator")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

THEME = {
    "primary": RGBColor(0x1F, 0x3A, 0x5F),
    "accent": RGBColor(0xC8, 0x90, 0x1A),
    "bg_light": RGBColor(0xF4, 0xF6, 0xF9),
    "text": RGBColor(0x22, 0x22, 0x22),
    "muted": RGBColor(0x66, 0x66, 0x66),
    "font": "Calibri",
}

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


@dataclass
class SlideSpec:
    title: str
    bullets: list[str] = field(default_factory=list)
    notes: str = ""
    image_note: str = ""  # e.g. "[IMAGE: chart.png]" rendered as placeholder note
    kind: str = "content"  # content | divider


def _blank_layout(prs: Presentation):
    for layout in prs.slide_layouts:
        if layout.name in ("Blank", "Title Only", "Title and Content", "Title Slide"):
            return layout
    return prs.slide_layouts[6]


def apply_theme(prs: Presentation) -> None:
    """Set 16:9 size and theme-consistent default text styles."""
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT


def add_title_slide(prs: Presentation, title: str, subtitle: str = "",
                    author: str = "") -> None:
    layout = prs.slide_layouts[0]  # Title Slide
    slide = prs.slides.add_slide(layout)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = THEME["bg_light"]
    if slide.shapes.title is not None:
        slide.shapes.title.text = title
        for para in slide.shapes.title.text_frame.paragraphs:
            for run in para.runs:
                run.font.size = Pt(40)
                run.font.bold = True
                run.font.color.rgb = THEME["primary"]
                run.font.name = THEME["font"]
    subs = slide.placeholders[1] if len(slide.placeholders) > 1 else None
    subtitle_text = subtitle or (f"{author}" if author else "")
    if subs is not None and subtitle_text:
        subs.text = subtitle_text
        for para in subs.text_frame.paragraphs:
            for run in para.runs:
                run.font.size = Pt(20)
                run.font.color.rgb = THEME["accent"]
                run.font.name = THEME["font"]


def _add_slide_number(slide, prs: Presentation) -> None:
    """Add a small slide-number text box in the bottom-right corner."""
    # slide.slide_id is an rId; find its position in the slide-id list
    sldIdLst = prs.slides._sldIdLst  # noqa: SLF001
    idx = 0
    for i, sldId in enumerate(sldIdLst, start=1):
        if sldId.rId == slide.slide_id:
            idx = i
            break
    box = slide.shapes.add_textbox(Inches(12.4), Inches(7.05), Inches(0.8), Inches(0.4))
    tf = box.text_frame
    tf.text = str(idx or len(sldIdLst))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    for run in p.runs:
        run.font.size = Pt(10)
        run.font.color.rgb = THEME["muted"]


def add_content_slide(prs: Presentation, title: str, bullets: Sequence[str],
                      notes: str = "", image_note: str = "") -> None:
    layout = _blank_layout(prs)
    slide = prs.slides.add_slide(layout)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = THEME["bg_light"]

    # Title bar
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35),
                                         Inches(12.1), Inches(0.9))
    tf = title_box.text_frame
    tf.word_wrap = True
    run = tf.paragraphs[0].add_run()
    run.text = title
    run.font.size = Pt(30)
    run.font.bold = True
    run.font.color.rgb = THEME["primary"]
    run.font.name = THEME["font"]
    # Accent underline
    line = slide.shapes.add_shape(1, Inches(0.6), Inches(1.25), Inches(2.2), Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = THEME["accent"]
    line.line.fill.background()

    # Bullets
    body = slide.shapes.add_textbox(Inches(0.8), Inches(1.6),
                                    Inches(11.7), Inches(5.0))
    btf = body.text_frame
    btf.word_wrap = True
    first = True
    for i, bullet in enumerate(bullets, start=1):
        para = btf.paragraphs[0] if first else btf.add_paragraph()
        first = False
        para.space_after = Pt(10)
        r = para.add_run()
        r.text = f"•  {bullet}"
        r.font.size = Pt(18)
        r.font.color.rgb = THEME["text"]
        r.font.name = THEME["font"]

    if image_note:
        note_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.55),
                                            Inches(11.7), Inches(0.45))
        nrun = note_box.text_frame.paragraphs[0].add_run()
        nrun.text = f"[IMAGE PLACEHOLDER] {image_note}"
        nrun.font.size = Pt(10)
        nrun.font.italic = True
        nrun.font.color.rgb = THEME["muted"]

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    _add_slide_number(slide, prs)
    return slide


def add_section_divider(prs: Presentation, title: str, subtitle: str = "") -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[2])  # Section Header
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = THEME["primary"]
    if slide.shapes.title is not None:
        slide.shapes.title.text = title
        for para in slide.shapes.title.text_frame.paragraphs:
            for run in para.runs:
                run.font.size = Pt(36)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.name = THEME["font"]
    subs = slide.placeholders[1] if len(slide.placeholders) > 1 else None
    if subs is not None and subtitle:
        subs.text = subtitle
        for para in subs.text_frame.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
                run.font.name = THEME["font"]
    _add_slide_number(slide, prs)


def parse_slide_arg(value: str) -> tuple[str, list[str], str]:
    """Parse 'Title|bullet1;bullet2' (optionally ':: notes' suffix)."""
    notes = ""
    if "::" in value:
        value, notes = value.rsplit("::", 1)
    if "|" not in value:
        raise argparse.ArgumentTypeError("--slide must be 'Title|bullet;bullet'")
    title, bullets_raw = value.split("|", 1)
    title = title.strip()
    if not title:
        raise argparse.ArgumentTypeError("--slide title must not be empty")
    bullets = [b.strip() for b in bullets_raw.split(";") if b.strip()]
    return title, bullets, notes.strip()


def load_slides_json(path: Path) -> list[SlideSpec]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("slides", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("slides JSON must be a list or {'slides': [...]}")
    specs: list[SlideSpec] = []
    for item in items:
        if isinstance(item, str):
            t, b, n = parse_slide_arg(item)
            specs.append(SlideSpec(title=t, bullets=b, notes=n))
        elif isinstance(item, dict):
            specs.append(SlideSpec(
                title=str(item.get("title", "")),
                bullets=[str(b) for b in item.get("bullets", [])],
                notes=str(item.get("notes", "")),
                image_note=str(item.get("image_note", "")),
                kind=str(item.get("kind", "content")),
            ))
        else:
            raise ValueError(f"Unsupported slide entry: {item!r}")
    return specs


def validate_deck(path: Path) -> list[str]:
    """Re-open the PPTX and return problems (empty = valid)."""
    problems: list[str] = []
    if not path.is_file():
        return [f"File not found: {path}"]
    try:
        with zipfile.ZipFile(path) as zf:
            if "ppt/presentation.xml" not in zf.namelist():
                problems.append("Not a PPTX package (missing ppt/presentation.xml)")
                return problems
        prs = Presentation(str(path))
        n_slides = len(prs.slides._sldIdLst)  # noqa: SLF001
        if n_slides == 0:
            problems.append("Deck has no slides")
        empty_titles = 0
        for i, slide in enumerate(prs.slides, start=1):
            has_text = any(
                shape.has_text_frame and shape.text_frame.text.strip()
                for shape in slide.shapes
            )
            if not has_text:
                empty_titles += 1
        if empty_titles:
            problems.append(f"{empty_titles} slide(s) contain no text")
        prs.part.package.close() if hasattr(prs.part.package, "close") else None
    except Exception as exc:  # noqa: BLE001
        problems.append(f"python-pptx failed to open deck: {exc}")
    return problems


def _resolve_output(output: Path, force: bool) -> Path:
    if output.exists() and not force:
        stem, suffix = output.stem, output.suffix
        i = 1
        while True:
            candidate = output.with_name(f"{stem}_{i}{suffix}")
            if not candidate.exists():
                return candidate
            i += 1
    return output


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Generate styled 16:9 PPTX decks (python-pptx).",
        epilog=f"{FOOTER}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--output", "-o", required=True, type=Path, help="Output .pptx path")
    ap.add_argument("--title", default="", help="Deck title (title slide)")
    ap.add_argument("--subtitle", default="", help="Subtitle on title slide")
    ap.add_argument("--author", default="", help="Author on title slide")
    ap.add_argument("--no-title-slide", action="store_true",
                    help="Skip the title slide")
    ap.add_argument("--slide", action="append", default=[],
                    metavar="'Title|bullet;bullet' or 'Title|b1;b2::speaker notes'",
                    help="Add a content slide (repeatable)")
    ap.add_argument("--divider", action="append", default=[],
                    metavar="'Section Title|optional subtitle'",
                    help="Add a section divider slide (repeatable)")
    ap.add_argument("--slides-json", type=Path, default=None,
                    help="JSON file with structured slides")
    ap.add_argument("--force", action="store_true", help="Overwrite existing output")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argparser().parse_args(argv)
    try:
        prs = Presentation()
        apply_theme(prs)

        if not args.no_title_slide and args.title:
            add_title_slide(prs, args.title, args.subtitle, args.author)
        elif args.title and args.no_title_slide:
            log.warning("--no-title-slide set; --title ignored")

        if args.slides_json:
            if not args.slides_json.is_file():
                log.error("Slides JSON not found: %s", args.slides_json)
                return 2
            for spec in load_slides_json(args.slides_json):
                if spec.kind == "divider":
                    add_section_divider(prs, spec.title, spec.bullets[0] if spec.bullets else "")
                else:
                    add_content_slide(prs, spec.title, spec.bullets,
                                      notes=spec.notes, image_note=spec.image_note)

        for raw in args.slide:
            title, bullets, notes = parse_slide_arg(raw)
            add_content_slide(prs, title, bullets, notes=notes)

        for raw in args.divider:
            if "|" in raw:
                t, sub = raw.split("|", 1)
            else:
                t, sub = raw, ""
            add_section_divider(prs, t.strip(), sub.strip())

        if len(prs.slides._sldIdLst) == 0:  # noqa: SLF001
            log.error("Nothing to generate: provide --title or at least one --slide")
            return 2

        out = _resolve_output(args.output, args.force)
        prs.save(str(out))
        problems = validate_deck(out)
        if problems:
            for p in problems:
                log.error("Validation: %s", p)
            return 1
        log.info("Wrote %s (%d slides)", out, len(prs.slides._sldIdLst))  # noqa: SLF001
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        log.error("Failed: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        log.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
