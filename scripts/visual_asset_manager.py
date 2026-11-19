#!/usr/bin/env python3
"""visual_asset_manager.py — Local/manifest-based visual asset pipeline.

Scans a directory of candidate assets (images/SVG), filters by license class,
scores filename/keyword relevance, copies selected assets to an output dir,
and writes attribution_register.csv.

Examples:
    python3 visual_asset_manager.py --query "team collaboration" \
        --source-dir ./assets --license-filter "cc0,cc-by" --output-dir ./out

    python3 visual_asset_manager.py --query hero --source-dir ./assets \
        --url https://example.com/img.png --output-dir ./out --force

Requires: no third-party deps (Pillow optional for image validation;
Pillow is auto-detected — install with `pip install pillow` to enable it).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import re
import shutil
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

try:
    from PIL import Image  # type: ignore
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("visual_asset_manager")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg"}
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024  # 25 MB cap
DOWNLOAD_TIMEOUT = 20  # seconds
ALLOWED_DOWNLOAD_TYPES = {
    "image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml",
    "image/bmp", "image/tiff",
}

LICENSE_CLASSES = [
    "cc0", "pd", "cc-by", "cc-by-sa", "cc-by-nc", "cc-by-nd",
    "proprietary", "unknown",
]

# license class -> (commercial_ok, modification_ok, attribution_required)
LICENSE_RULES: dict[str, tuple[bool, bool, bool]] = {
    "cc0": (True, True, False),
    "pd": (True, True, False),
    "cc-by": (True, True, True),
    "cc-by-sa": (True, True, True),
    "cc-by-nc": (False, True, True),
    "cc-by-nc-sa": (False, True, True),
    "cc-by-nd": (True, False, True),
    "cc-by-nc-nd": (False, False, True),
    "proprietary": (False, False, True),
    "unknown": (False, False, True),
}


@dataclass
class Asset:
    path: Path
    name: str
    source: str = ""
    creator: str = ""
    license_class: str = "unknown"
    license_url: str = ""
    attribution_text: str = ""
    score: float = 0.0

    @property
    def commercial_ok(self) -> bool:
        return LICENSE_RULES.get(self.license_class, LICENSE_RULES["unknown"])[0]

    @property
    def modification_ok(self) -> bool:
        return LICENSE_RULES.get(self.license_class, LICENSE_RULES["unknown"])[1]

    @property
    def attribution_required(self) -> bool:
        return LICENSE_RULES.get(self.license_class, LICENSE_RULES["unknown"])[2]


def classify_license(value: Optional[str]) -> str:
    """Map a free-form license string to a canonical license class."""
    if not value:
        return "unknown"
    v = value.strip().lower()
    # SPDX-ish IDs first
    mapping = {
        "cc0-1.0": "cc0", "cc0": "cc0", "public domain": "pd", "pd": "pd",
        "cc-by-4.0": "cc-by", "cc-by-3.0": "cc-by", "cc by": "cc-by",
        "cc-by": "cc-by", "attribution": "cc-by",
        "cc-by-sa-4.0": "cc-by-sa", "cc-by-sa": "cc-by-sa",
        "cc-by-nc-4.0": "cc-by-nc", "cc-by-nc": "cc-by-nc",
        "cc-by-nc-sa": "cc-by-nc", "cc-by-nd-4.0": "cc-by-nd", "cc-by-nd": "cc-by-nd",
        "cc-by-nc-nd": "cc-by-nd",
        "proprietary": "proprietary", "all rights reserved": "proprietary",
        "copyright": "proprietary",
    }
    for key, cls in mapping.items():
        if key in v:
            return cls
    if "creative commons" in v or "cc " in v:
        return "unknown"
    return "unknown"


def score_relevance(asset: Asset, query_terms: Sequence[str]) -> float:
    """Score 0..1 by keyword hits in filename + metadata fields."""
    if not query_terms:
        return 0.5
    haystack = " ".join([
        asset.name.lower(),
        asset.source.lower(),
        asset.creator.lower(),
        asset.attribution_text.lower(),
    ])
    hits = sum(1 for t in query_terms if t in haystack)
    # name-only hits weighted higher
    name_hits = sum(1 for t in query_terms if t in asset.name.lower())
    score = (hits / len(query_terms)) * 0.6 + (name_hits / len(query_terms)) * 0.4
    return round(min(score, 1.0), 4)


def validate_image(path: Path) -> tuple[bool, str]:
    """Check file exists, is an image by extension, and (if Pillow present) decodes."""
    if not path.is_file():
        return False, "file does not exist"
    if path.suffix.lower() not in IMAGE_EXTS:
        return False, f"unsupported extension {path.suffix}"
    if path.suffix.lower() == ".svg":
        head = path.read_bytes()[:512]
        if b"<svg" not in head.lower():
            return False, "file does not look like SVG"
        return True, "svg-ok"
    if HAS_PIL:
        try:
            with Image.open(path) as im:
                im.verify()
            return True, "image-ok"
        except Exception as exc:  # noqa: BLE001
            return False, f"image decode failed: {exc}"
    return True, "image-ok (Pillow not installed; decode skipped)"


def _load_manifest(manifest_path: Optional[Path]) -> dict[str, dict]:
    """Load manifest.json mapping filename -> metadata dict."""
    if not manifest_path:
        return {}
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {Path(str(e.get("file", e.get("path", "")))).name: e for e in data if isinstance(e, dict)}
    if isinstance(data, dict):
        # accept {"assets": [...]} or {"filename": {...}}
        if "assets" in data and isinstance(data["assets"], list):
            return {Path(str(e.get("file", e.get("path", "")))).name: e
                    for e in data["assets"] if isinstance(e, dict)}
        return {k: v for k, v in data.items() if isinstance(v, dict)}
    raise ValueError("Unsupported manifest format")


def _load_sidecar_license(path: Path) -> dict:
    """Load <name>.license.json sidecar if present."""
    sidecar = path.with_suffix(path.suffix + ".license.json")
    if not sidecar.is_file():
        sidecar = path.with_name(path.stem + ".license.json")
    if sidecar.is_file():
        try:
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def scan_assets(source_dir: Path, manifest_path: Optional[Path]) -> list[Asset]:
    """Enumerate candidate assets with license metadata merged from all sources."""
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source dir not found: {source_dir}")
    manifest = _load_manifest(manifest_path)
    assets: list[Asset] = []
    for p in sorted(source_dir.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        meta = dict(manifest.get(p.name, {}))
        meta.update(_load_sidecar_license(p))  # sidecar wins
        ok, why = validate_image(p)
        if not ok:
            log.warning("Skipping %s: %s", p.name, why)
            continue
        lic_raw = str(meta.get("license", meta.get("licence", "")))
        assets.append(Asset(
            path=p,
            name=p.name,
            source=str(meta.get("source", meta.get("source_url", p.parent.name))),
            creator=str(meta.get("creator", meta.get("author", ""))),
            license_class=classify_license(lic_raw),
            license_url=str(meta.get("license_url", meta.get("license_link", ""))),
            attribution_text=str(meta.get("attribution", meta.get("attribution_text", ""))),
        ))
    return assets


def build_attribution_register(assets: Sequence[Asset]) -> list[dict]:
    """Build CSV rows for the attribution register."""
    rows = []
    for a in assets:
        rows.append({
            "file": a.name,
            "source": a.source,
            "creator": a.creator,
            "license": a.license_class,
            "license_url": a.license_url,
            "attribution_text": a.attribution_text or (
                f"{a.creator or 'Unknown'} — {a.license_class} — {a.source}".strip(" —")
            ),
            "commercial_ok": "yes" if a.commercial_ok else "no",
            "modification_ok": "yes" if a.modification_ok else "no",
        })
    return rows


def write_register(rows: Sequence[dict], out_path: Path) -> None:
    fields = ["file", "source", "creator", "license", "license_url",
              "attribution_text", "commercial_ok", "modification_ok"]
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def download_asset(url: str, dest: Path) -> Path:
    """Download one asset over HTTP(S). REQUIRES NETWORK ACCESS.

    Enforces a 25 MB size cap, a 20 s timeout, and an image content-type check.
    """
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("Only http(s) URLs are supported")
    req = urllib.request.Request(url, headers={"User-Agent": "FileCraftBooster/1.0"})
    with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as resp:  # noqa: S310
        ctype = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if ctype and ctype not in ALLOWED_DOWNLOAD_TYPES:
            raise ValueError(f"Refusing non-image content type: {ctype}")
        data = resp.read(MAX_DOWNLOAD_BYTES + 1)
        if len(data) > MAX_DOWNLOAD_BYTES:
            raise ValueError(f"Download exceeds {MAX_DOWNLOAD_BYTES} byte cap")
        ext = Path(url.split("?")[0]).suffix or ".png"
        if ext.lower() not in IMAGE_EXTS:
            ext = ".png"
        dest = dest.with_suffix(ext)
        dest.write_bytes(data)
        return dest


def _resolve_output_dir(output_dir: Path, force: bool) -> Path:
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        i = 1
        while True:
            candidate = output_dir.with_name(f"{output_dir.name}_{i}")
            if not candidate.exists():
                return candidate
            i += 1
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Search/filter/copy licensed visual assets and emit an "
                    "attribution register. Local-first; --url download requires network.",
        epilog=FOOTER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--query", default="", help="Keyword query (space-separated)")
    ap.add_argument("--source-dir", type=Path, required=True,
                    help="Directory to scan for candidate assets")
    ap.add_argument("--manifest", type=Path, default=None,
                    help="Optional manifest.json with license metadata")
    ap.add_argument("--license-filter", default="",
                    help=f"Comma-separated license classes to keep. Choices: {', '.join(LICENSE_CLASSES)}")
    ap.add_argument("--output-dir", type=Path, required=True,
                    help="Destination directory for selected assets + CSV")
    ap.add_argument("--url", default=None,
                    help="OPTIONAL: download a single asset from this URL (network required)")
    ap.add_argument("--min-score", type=float, default=0.0,
                    help="Minimum relevance score (default 0.0)")
    ap.add_argument("--limit", type=int, default=50, help="Max assets to copy (default 50)")
    ap.add_argument("--force", action="store_true", help="Allow writing into non-empty output dir")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_argparser().parse_args(argv)
    try:
        allowed = {c.strip().lower() for c in args.license_filter.split(",") if c.strip()}
        bad = allowed - set(LICENSE_CLASSES)
        if bad:
            log.error("Unknown license classes: %s", ", ".join(sorted(bad)))
            return 2

        out_dir = _resolve_output_dir(args.output_dir, args.force)
        terms = [t.lower() for t in args.query.split() if t]

        downloaded: list[Asset] = []
        if args.url:
            dest = download_asset(args.url, out_dir / Path(args.url.split("?")[0]).name)
            log.warning("Downloaded %s from network URL (network access was used)", dest.name)
            a = Asset(path=dest, name=dest.name, source=args.url,
                      license_class="unknown", attribution_text=f"Downloaded from {args.url}")
            a.score = score_relevance(a, terms)
            downloaded.append(a)

        assets = scan_assets(args.source_dir, args.manifest)
        for a in assets:
            a.score = score_relevance(a, terms)

        selected = [a for a in assets if a.score >= args.min_score]
        if allowed:
            selected = [a for a in selected if a.license_class in allowed]
        selected.sort(key=lambda a: a.score, reverse=True)
        selected = selected[: max(0, args.limit)]

        copied = 0
        for a in selected:
            dest = out_dir / a.name
            if dest.exists():
                stem, suf = dest.stem, dest.suffix
                i = 1
                while dest.with_name(f"{stem}_{i}{suf}").exists():
                    i += 1
                dest = dest.with_name(f"{stem}_{i}{suf}")
            shutil.copy2(a.path, dest)
            a.path = dest
            copied += 1

        all_out = downloaded + selected
        rows = build_attribution_register(all_out)
        register_path = out_dir / "attribution_register.csv"
        write_register(rows, register_path)

        log.info("Scanned %d assets, selected %d (+%d downloaded), wrote %s",
                 len(assets), copied, len(downloaded), register_path)
        if not all_out:
            log.warning("No assets matched criteria")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError) as exc:
        log.error("Failed: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        log.exception("Unexpected error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved.
