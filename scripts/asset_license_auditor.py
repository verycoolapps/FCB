#!/usr/bin/env python3
"""asset_license_auditor.py — Audit license metadata for visual assets.

Reads a manifest (JSON or CSV) or a directory of assets with sidecar
*.license.json files, classifies each license, computes commercial-use and
attribution verdicts, flags risks, and writes license_audit_report.md plus
license_audit_report.csv.

Examples:
    python3 asset_license_auditor.py --manifest assets.json --output-dir ./audit
    python3 asset_license_auditor.py --dir ./assets --output-dir ./audit

Requires: no third-party dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger("asset_license_auditor")

FOOTER = "# © 2026 VeryCoolApps — PT. Agra Karya Digital — www.vcadeveloper.com — Proprietary. All rights reserved."

# ---------------------------------------------------------------------------
# License classification table (canonical data)
# ---------------------------------------------------------------------------
# class -> dict(commercial, modification, attribution, share_alike, risk, summary)
LICENSE_TABLE: dict[str, dict] = {
    "cc0": {
        "commercial": True, "modification": True, "attribution": False,
        "share_alike": False, "risk": "low",
        "summary": "CC0 Public Domain Dedication — no restrictions.",
    },
    "pd": {
        "commercial": True, "modification": True, "attribution": False,
        "share_alike": False, "risk": "low",
        "summary": "Public domain — no known copyright restrictions.",
    },
    "cc-by": {
        "commercial": True, "modification": True, "attribution": True,
        "share_alike": False, "risk": "low",
        "summary": "CC BY — free use incl. commercial; attribution required.",
    },
    "cc-by-sa": {
        "commercial": True, "modification": True, "attribution": True,
        "share_alike": True, "risk": "medium",
        "summary": "CC BY-SA — derivatives must use same license (copyleft).",
    },
    "cc-by-nc": {
        "commercial": False, "modification": True, "attribution": True,
        "share_alike": False, "risk": "high",
        "summary": "CC BY-NC — NON-COMMERCIAL use only.",
    },
    "cc-by-nc-sa": {
        "commercial": False, "modification": True, "attribution": True,
        "share_alike": True, "risk": "high",
        "summary": "CC BY-NC-SA — non-commercial + share-alike.",
    },
    "cc-by-nd": {
        "commercial": True, "modification": False, "attribution": True,
        "share_alike": False, "risk": "high",
        "summary": "CC BY-ND — NO derivatives/adaptations allowed.",
    },
    "cc-by-nc-nd": {
        "commercial": False, "modification": False, "attribution": True,
        "share_alike": False, "risk": "critical",
        "summary": "CC BY-NC-ND — non-commercial, no derivatives.",
    },
    "proprietary": {
        "commercial": False, "modification": False, "attribution": True,
        "share_alike": False, "risk": "critical",
        "summary": "Proprietary/copyrighted — use requires explicit license.",
    },
    "unknown": {
        "commercial": False, "modification": False, "attribution": True,
        "share_alike": False, "risk": "critical",
        "summary": "License unknown — treat as all-rights-reserved (BLOCK).",
    },
}

_LICENSE_ALIASES = {
    "cc0-1.0": "cc0", "cc0": "cc0", "public domain": "pd", "pd": "pd",
    "cc-by-4.0": "cc-by", "cc-by-3.0": "cc-by", "cc-by-2.0": "cc-by",
    "cc by": "cc-by", "cc-by": "cc-by", "attribution": "cc-by",
    "cc-by-sa-4.0": "cc-by-sa", "cc-by-sa-3.0": "cc-by-sa", "cc-by-sa": "cc-by-sa",
    "cc-by-nc-4.0": "cc-by-nc", "cc-by-nc-3.0": "cc-by-nc",
    "cc-by-nc": "cc-by-nc", "cc-by-nc-sa-4.0": "cc-by-nc-sa",
    "cc-by-nc-sa": "cc-by-nc-sa",
    "cc-by-nd-4.0": "cc-by-nd", "cc-by-nd-3.0": "cc-by-nd", "cc-by-nd": "cc-by-nd",
    "cc-by-nc-nd": "cc-by-nc-nd",
    "proprietary": "proprietary", "all rights reserved": "proprietary",
    "copyright": "proprietary", "standard license": "proprietary",
}


@dataclass
class LicenseEntry:
    asset: str
    license_raw: str = ""
    license_class: str = "unknown"
    creator: str = ""
    source: str = ""
    license_url: str = ""
    commercial_ok: bool = False
    modification_ok: bool = False
    attribution_required: bool = False
    share_alike: bool = False
    risk: str = "critical"
    flags: list[str] = field(default_factory=list)


def classify(license_raw: Optional[str]) -> str:
    """Classify a free-form license string into a canonical class."""
    if not license_raw or not str(license_raw).strip():
        return "unknown"
    v = str(license_raw).strip().lower()
    for alias, cls in _LICENSE_ALIASES.items():
        if alias in v:
            return cls
    if "creative commons" in v or "cc-" in v or v.startswith("cc "):
        return "unknown"
    return "unknown"


def verdict(entry: LicenseEntry) -> tuple[str, str]:
    """Return (commercial_verdict, attribution_requirement) human strings."""
    info = LICENSE_TABLE[entry.license_class]
    commercial = "ALLOWED" if info["commercial"] else "BLOCKED"
    if entry.license_class == "unknown":
        commercial = "BLOCKED"
    elif entry.license_class in ("cc-by-nc", "cc-by-nc-sa", "cc-by-nc-nd"):
        commercial = "NON-COMMERCIAL ONLY"
    attribution = "REQUIRED" if info["attribution"] else "NOT REQUIRED"
    return commercial, attribution


def risk_flags(entry: LicenseEntry) -> list[str]:
    flags = list(entry.flags)
    cls = entry.license_class
    if cls == "unknown" or not entry.license_raw.strip():
        flags.append("BLOCK: unknown license — treat as all-rights-reserved")
    if cls in ("cc-by-nc", "cc-by-nc-sa", "cc-by-nc-nd"):
        flags.append("NON-COMMERCIAL ONLY — do not use in paid/commercial products")
    if cls in ("cc-by-nd", "cc-by-nc-nd"):
        flags.append("NO DERIVATIVES — cannot crop/modify/remix")
    if cls == "cc-by-sa":
        flags.append("SHARE-ALIKE — derivatives must use CC BY-SA")
    if cls == "proprietary":
        flags.append("BLOCK: proprietary — requires explicit license agreement")
    if cls == "cc-by" and not entry.license_url:
        flags.append("ATTRIBUTION: provide creator + license link in credits")
    return flags


def parse_manifest(path: Path) -> list[dict]:
    """Parse a JSON or CSV manifest into a list of entry dicts."""
    if not path.is_file():
        raise FileNotFoundError(f"Manifest not found: {path}")
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            if isinstance(data.get("assets"), list):
                return [e for e in data["assets"] if isinstance(e, dict)]
            return [{"file": k, **(v if isinstance(v, dict) else {"license": v})}
                    for k, v in data.items()]
        if isinstance(data, list):
            return [e for e in data if isinstance(e, dict)]
        raise ValueError("Unsupported JSON manifest structure")
    # CSV
    rows = list(csv.DictReader(text.splitlines()))
    return [dict(r) for r in rows]


def _entry_from_dict(d: dict) -> LicenseEntry:
    lic_raw = str(d.get("license", d.get("licence", d.get("license_raw", ""))))
    cls = classify(lic_raw)
    e = LicenseEntry(
        asset=str(d.get("file", d.get("asset", d.get("path", d.get("name", "?"))))),
        license_raw=lic_raw,
        license_class=cls,
        creator=str(d.get("creator", d.get("author", ""))),
        source=str(d.get("source", d.get("source_url", ""))),
        license_url=str(d.get("license_url", d.get("license_link", ""))),
    )
    e.flags = risk_flags(e)
    e.commercial_ok = LICENSE_TABLE[cls]["commercial"]
    e.modification_ok = LICENSE_TABLE[cls]["modification"]
    e.attribution_required = LICENSE_TABLE[cls]["attribution"]
    e.share_alike = LICENSE_TABLE[cls]["share_alike"]
    e.risk = LICENSE_TABLE[cls]["risk"]
    return e


def scan_sidecars(directory: Path) -> list[LicenseEntry]:
    """Scan a directory for assets + <name>.license.json sidecars."""
    if not directory.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory}")
    entries: list[LicenseEntry] = []
    for p in sorted(directory.rglob("*")):
        if p.is_dir():
            continue
        sidecar = p.with_name(p.name + ".license.json")
        if not sidecar.is_file():
            sidecar = p.with_suffix(p.suffix + ".license.json")
        if sidecar.is_file():
            try:
                meta = json.loads(sidecar.read_text(encoding="utf-8"))
                if not isinstance(meta, dict):
                    meta = {}
            except json.JSONDecodeError:
                meta = {}
            meta.setdefault("file", str(p.relative_to(directory)))
            entries.append(_entry_from_dict(meta))
        elif p.suffix.lower() == ".json":
            continue  # JSON metadata files are not assets
        else:
            # asset without sidecar -> unknown license
            entries.append(_entry_from_dict({"file": str(p.relative_to(directory)), "license": ""}))
    return entries


def render_report(entries: Sequence[LicenseEntry], source_desc: str) -> str:
    lines = [
        "# Asset License Audit Report",
        "",
        f"**Source:** {source_desc}  ",
        f"**Assets audited:** {len(entries)}  ",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---|",
        f"| Total assets | {len(entries)} |",
        f"| Commercial use allowed | {sum(1 for e in entries if e.commercial_ok)} |",
        f"| Non-commercial only | {sum(1 for e in entries if e.license_class.startswith('cc-by-nc'))} |",
        f"| No derivatives | {sum(1 for e in entries if e.license_class.endswith('-nd'))} |",
        f"| Unknown license (BLOCK) | {sum(1 for e in entries if e.license_class == 'unknown')} |",
        f"| Attribution required | {sum(1 for e in entries if e.attribution_required)} |",
        "",
        "## Per-Asset Detail",
        "",
        "| Asset | License | Class | Commercial | Attribution | Risk | Flags |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in entries:
        commercial, attribution = verdict(e)
        flags = "; ".join(e.flags) if e.flags else "—"
        lic_display = e.license_raw or "(unspecified)"
        lines.append(
            f"| `{e.asset}` | {lic_display} | {e.license_class} | "
            f"{commercial} | {attribution} | {e.risk} | {flags} |"
        )
    lines += [
        "",
        "## License Classification Reference",
        "",
        "| Class | Commercial | Modification | Attribution | Share-Alike | Risk |",
        "|---|---|---|---|---|---|",
    ]
    for cls, info in LICENSE_TABLE.items():
        lines.append(
            f"| {cls} | {'yes' if info['commercial'] else 'no'} | "
            f"{'yes' if info['modification'] else 'no'} | "
            f"{'yes' if info['attribution'] else 'no'} | "
            f"{'yes' if info['share_alike'] else 'no'} | {info['risk']} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_csv(entries: Sequence[LicenseEntry], path: Path) -> None:
    fields = ["asset", "license_raw", "license_class", "creator", "source",
              "license_url", "commercial_ok", "modification_ok",
              "attribution_required", "share_alike", "risk", "flags"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for e in entries:
            commercial, _ = verdict(e)
            w.writerow({
                "asset": e.asset,
                "license_raw": e.license_raw,
                "license_class": e.license_class,
                "creator": e.creator,
                "source": e.source,
                "license_url": e.license_url,
                "commercial_ok": "yes" if e.commercial_ok else "no",
                "modification_ok": "yes" if e.modification_ok else "no",
                "attribution_required": "yes" if e.attribution_required else "no",
                "share_alike": "yes" if e.share_alike else "no",
                "risk": e.risk,
                "flags": " | ".join(e.flags),
            })


def _resolve_output_dir(output_dir: Path, force: bool) -> Path:
    report_md = output_dir / "license_audit_report.md"
    if output_dir.exists() and report_md.exists() and not force:
        i = 1
        while True:
            candidate = output_dir.with_name(f"{output_dir.name}_{i}")
            if not (candidate / "license_audit_report.md").exists():
                return candidate
            i += 1
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Audit license metadata for a manifest or directory of "
                    "assets with sidecar .license.json files.",
        epilog=FOOTER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--manifest", type=Path,
                     help="JSON or CSV manifest of assets + license fields")
    src.add_argument("--dir", type=Path,
                     help="Directory of assets; reads <name>.license.json sidecars")
    ap.add_argument("--output-dir", type=Path, default=Path("."),
                    help="Where to write license_audit_report.md/.csv (default: cwd)")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing report files")
    return ap


def main(argv: Optional[str] = None) -> int:  # type: ignore[override]
    args = build_argparser().parse_args(argv)
    try:
        if args.manifest:
            raw_entries = parse_manifest(args.manifest)
            entries = [_entry_from_dict(e) for e in raw_entries]
            source_desc = str(args.manifest)
        else:
            entries = scan_sidecars(args.dir)
            source_desc = str(args.dir)

        out_dir = _resolve_output_dir(args.output_dir, args.force)
        md_path = out_dir / "license_audit_report.md"
        csv_path = out_dir / "license_audit_report.csv"
        md_path.write_text(render_report(entries, source_desc), encoding="utf-8")
        write_csv(entries, csv_path)

        blocked = sum(1 for e in entries if e.license_class in ("unknown", "proprietary"))
        log.info("Audited %d assets -> %s, %s (blocked/unknown: %d)",
                 len(entries), md_path, csv_path, blocked)
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
