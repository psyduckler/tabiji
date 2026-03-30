#!/usr/bin/env python3
"""
build-health-page.py — Build a tabiji.ai health guide page from template + JSON data.

Usage:
    python3 scripts/build-health-page.py JP        # builds /health/japan/
    python3 scripts/build-health-page.py TH        # builds /health/thailand/
    python3 scripts/build-health-page.py --list   # show available country data files

Output:
    ~/tabiji/health/{country-slug}/index.html
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).parent.resolve()
TABIJI_ROOT  = SCRIPT_DIR.parent
TEMPLATE_PATH   = TABIJI_ROOT / "health-template.html"
DATA_DIR        = TABIJI_ROOT / "health-data"      # where country JSON files live
OUTPUT_ROOT     = TABIJI_ROOT / "health"


# ── Variable registry ───────────────────────────────────────────────────────

# Keys that come from the top-level JSON (not sub-section HTML fields)
TOP_LEVEL_KEYS = {
    "COUNTRY_NAME", "COUNTRY_SLUG", "COUNTRY_FLAG", "ISO2",
    "EMERGENCY_NUMBER", "HEALTHCARE_SYSTEM", "QUALITY_RATING",
    "PHARMACY_ACCESS", "WATER_SAFETY",
    "META_DESCRIPTION", "OG_IMAGE", "LAST_UPDATED",
    # sub-section HTML fields (injected as-is)
    "HEALTHCARE_OVERVIEW_HTML",
    "PHARMACY_GUIDE_HTML",
    "MEDICATIONS_HTML",
    "INSURANCE_HTML",
    "VACCINATIONS_HTML",
    "FOOD_WATER_HTML",
    "EMERGENCY_CONTACTS_HTML",
    "SOURCES_HTML",
}


def load_template() -> str:
    if not TEMPLATE_PATH.exists():
        sys.exit(f"ERROR: Template not found at {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def load_country_data(iso2: str) -> dict:
    iso2 = iso2.upper()
    candidates = [
        DATA_DIR / f"{iso2.lower()}.json",
        DATA_DIR / f"{iso2.upper()}.json",
        DATA_DIR / iso2.lower() / "data.json",
    ]
    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))

    available = list(DATA_DIR.glob("*.json")) + list(DATA_DIR.glob("*/data.json"))
    names = [f"  {p.stem}" for p in available]
    sys.exit(
        f"ERROR: No data file found for '{iso2}'.\n"
        f"  Searched: {candidates}\n"
        f"  Available countries:\n" + ("\n".join(names) if names else "  (none)")
    )


def build_page(template: str, data: dict) -> str:
    """Replace all {{VARIABLE}} placeholders in the template."""

    def replacer(key: str, value: str) -> str:
        """Replace {{key}} in template, raise on unresolved placeholder."""
        placeholder = "{{" + key + "}}"
        if placeholder in template:
            return template.replace(placeholder, str(value))
        # Don't error on optional/unused placeholders
        return template

    # Pass 1: sub-section HTML blocks (already rendered HTML in the JSON)
    for key in [
        "HEALTHCARE_OVERVIEW_HTML",
        "PHARMACY_GUIDE_HTML",
        "MEDICATIONS_HTML",
        "INSURANCE_HTML",
        "VACCINATIONS_HTML",
        "FOOD_WATER_HTML",
        "EMERGENCY_CONTACTS_HTML",
        "SOURCES_HTML",
    ]:
        template = replacer(key, data.get(key, ""))

    # Pass 2: top-level scalar fields
    for key in TOP_LEVEL_KEYS:
        if key not in [
            "HEALTHCARE_OVERVIEW_HTML",
            "PHARMACY_GUIDE_HTML",
            "MEDICATIONS_HTML",
            "INSURANCE_HTML",
            "VACCINATIONS_HTML",
            "FOOD_WATER_HTML",
            "EMERGENCY_CONTACTS_HTML",
            "SOURCES_HTML",
        ]:
            template = replacer(key, data.get(key, ""))

    # Pass 3: any leftover {{...}} placeholders → empty string
    template = re.sub(r"\{\{[^{}]+\}\}", "", template)

    return template


def save_page(output_path: Path, html: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"  ✅  {output_path.relative_to(TABIJI_ROOT)}")


def list_countries() -> None:
    files = sorted(DATA_DIR.glob("*.json")) + sorted(DATA_DIR.glob("*/data.json"))
    if not files:
        print(f"No country data files found in {DATA_DIR}")
    else:
        print("Available country data files:")
        for p in files:
            print(f"  {p.stem}")
        print(f"\nRun with e.g.: python3 scripts/build-health-page.py JP")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Build a tabiji health guide page.")
    parser.add_argument(
        "iso2",
        nargs="?",
        help="ISO 3166-1 alpha-2 country code (e.g. JP, TH, MX)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available country data files and exit",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build pages for all countries in the data directory",
    )
    args = parser.parse_args()

    if args.list:
        list_countries()
        return

    template = load_template()

    if args.all:
        print("Building all health guide pages …")
        files = sorted(DATA_DIR.glob("*.json"))
        if not files:
            files = [p for p in DATA_DIR.glob("*/data.json")]
        if not files:
            sys.exit(f"No .json files found in {DATA_DIR}")
        for path in files:
            iso2 = path.stem.upper()
            if path.is_dir():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            slug = data.get("country_slug", iso2.lower())
            output = OUTPUT_ROOT / slug / "index.html"
            page = build_page(template, data)
            save_page(output, page)
        print("Done.")
        return

    if not args.iso2:
        sys.exit("Usage: build-health-page.py JP\n       build-health-page.py --list\n       build-health-page.py --all")

    iso2 = args.iso2.upper()
    print(f"Building health guide for {iso2} …")

    data  = load_country_data(iso2)
    slug  = data.get("country_slug", iso2.lower())
    page  = build_page(template, data)
    output = OUTPUT_ROOT / slug / "index.html"
    save_page(output, page)
    print(f"\n📄  https://tabiji.ai/health/{slug}/\n")


if __name__ == "__main__":
    main()
