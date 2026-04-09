#!/usr/bin/env python3
"""
health-tier1-fixes.py — Idempotent Tier 1 fixes for health-data/*.json

Applies the following fixes detected in the 2026-04-08 audit:

1. Peru's lastUpdated is malformed ("2022026-03-30") → "2026-04-08".
2. All canonical files with lastUpdated == "2026-03-30" → "2026-04-08".
3. mentalHealth.internationalLine == "Contact your embassy for referrals"
   (26 countries) → delete the field so the build script's existing
   findahelpline.com fallback (gen_mental_health line 481) takes over.
4. CU's mentalHealth.englishTherapists has the embassy boilerplate →
   replaced with a country-accurate sentence.
5. Generic metaDescription for 27 countries → composed from existing
   structured data (emergency number, banned meds, vaccinations, water,
   quality rating, EU 112) so each country gets distinctive SERP copy.

Idempotent: re-running produces the same JSON files. Skips files whose
lastUpdated is already current and whose metaDescription is already
non-generic. Operates only on canonical health-data/*.json files
(skips " 2.json" working-tree pollution by name pattern).

Usage:
    python3 scripts/health-tier1-fixes.py            # apply fixes
    python3 scripts/health-tier1-fixes.py --dry-run  # show what would change
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
TABIJI_ROOT = SCRIPT_DIR.parent
DATA_DIR = TABIJI_ROOT / "health-data"

TODAY = "2026-04-08"
MALFORMED_DATE = "2022026-03-30"
STALE_DATE = "2026-03-30"
EMBASSY_BOILERPLATE = "Contact your embassy for referrals"
META_TEMPLATE_PREFIX = "Complete health & medication guide for traveling to"
META_HOOKS = (
    "banned",
    "restricted",
    "yellow fever",
    "malaria",
    "altitude",
    "dengue",
    "japanese encephalitis",
    "soroche",
    "world-class",
    "schengen",
    "medical evacuation",
    "evacuation insurance",
    "khat",
    "tuberculosis",
    "cholera",
    "ehic",
    # Below: signals that mean a description is genuinely country-specific even
    # if it doesn't name a disease/medication. Added 2026-04-08 after the first
    # pass falsely flagged Cuba/Iran/Lebanon/Maldives/Uruguay as generic.
    "shortage",
    "mandatory",
    "resort",
    "desert",
    "excellent",
    "drug laws",
    "sanctions",
    "crisis",
    "cannabis laws",
    "decompression",
)

CU_ENGLISH_THERAPISTS_REPLACEMENT = (
    "Limited English-speaking mental health services. Most counseling in Cuba "
    "is in Spanish; international hotels in Havana and Varadero can sometimes "
    "arrange referrals."
)


def is_canonical(path: Path) -> bool:
    """Skip duplicate working-tree files like 'AL 2.json'."""
    return " " not in path.name


def first_emergency_number(emergency: str) -> str:
    """'117 (police), 106 (fire/ambulance), 105 (civil defense)' → '117'."""
    if not emergency:
        return ""
    first = emergency.split(",")[0].strip()
    # Strip parenthetical: '117 (police)' → '117'
    if "(" in first:
        first = first.split("(")[0].strip()
    return first


def short_med_name(name: str) -> str:
    """Reduce a verbose medication entry to its most-searchable short form.

    Examples:
        'Pseudoephedrine (Sudafed and similar)' → 'Sudafed'
        'ADHD stimulant medications (Adderall, Ritalin, Vyvanse)' → 'Adderall'
        'Codeine-containing medications' → 'Codeine'
        'All narcotic/opioid medications' → 'Opioids'
        'Cannabis/hashish' → 'Cannabis'
        'Cannabis/CBD products' → 'Cannabis'
        'Amphetamines (Adderall, etc.)' → 'Adderall'
    """
    if not name:
        return ""
    s = name.strip()

    # If parenthetical contains a brand list, prefer the first brand
    # because brand names rank far better in SERPs than generic class names.
    if "(" in s and ")" in s:
        before = s.split("(")[0].strip()
        inside = s.split("(")[1].split(")")[0]
        first_brand = inside.split(",")[0].split(" and ")[0].strip().rstrip(".")
        if first_brand and first_brand[0].isupper() and 2 <= len(first_brand) <= 18:
            return first_brand
        s = before

    # Strip leading "All " / "Most " quantifiers
    for prefix in ("All ", "Most "):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break

    # Strip suffix noise like "-containing medications", " medications", " products"
    for suffix in (
        "-containing medications",
        "-containing drugs",
        " medications",
        " drugs",
        " products",
    ):
        if s.endswith(suffix):
            s = s[: -len(suffix)]

    # "Cannabis/hashish" / "narcotic/opioid" → first half
    if "/" in s:
        s = s.split("/")[0]

    s = s.strip().rstrip(",.")

    # Friendly normalization for plural class names
    rewrites = {
        "narcotic": "Opioids",
        "opioid": "Opioids",
        "amphetamines": "Adderall",
        "amphetamine": "Adderall",
    }
    if s.lower() in rewrites:
        return rewrites[s.lower()]

    # Capitalize first letter if it's lowercase (e.g. "narcotic" wasn't matched)
    if s and s[0].islower():
        s = s[0].upper() + s[1:]

    return s


def is_universally_required_vaccine(entry: str, vacc_name: str) -> bool:
    """Return True only if `entry` mentions `vacc_name` AND does NOT carry a
    conditional qualifier like 'if arriving from endemic area'."""
    e = entry.lower()
    if vacc_name.lower() not in e:
        return False
    conditional_markers = (
        "if arriving",
        "endemic area",
        "endemic country",
        "endemic region",
        "from an endemic",
        "from endemic",
        "for travel to certain",
        "for travelers from",
    )
    return not any(m in e for m in conditional_markers)


def compose_meta_description(d: dict) -> str:
    """Build a country-specific meta description from structured fields.
    Targets 130-160 chars. Returns the existing metaDescription if it
    already contains a country-specific hook."""
    name = d.get("countryName", "")
    em_short = first_emergency_number(d.get("emergencyNumber", ""))

    hooks: list[str] = []

    # 1. Banned medications — highest SEO value (people search for these).
    #    Fall back to "restricted" status when no fully-banned items exist.
    meds = d.get("restrictedMeds", [])
    banned = [
        short_med_name(m.get("name", ""))
        for m in meds
        if isinstance(m, dict) and m.get("status") == "banned"
    ]
    banned = [b for b in banned if b]
    if banned:
        if len(banned) >= 2:
            hooks.append(f"{banned[0]} & {banned[1]} banned")
        else:
            hooks.append(f"{banned[0]} banned")
    else:
        restricted = [
            short_med_name(m.get("name", ""))
            for m in meds
            if isinstance(m, dict) and m.get("status") == "restricted"
        ]
        restricted = [r for r in restricted if r]
        if restricted:
            hooks.append(f"{restricted[0]} restricted")

    # 2. Required vaccinations — only if UNCONDITIONALLY required, not
    #    "if arriving from endemic area"
    vacc = d.get("vaccinations", {})
    req = vacc.get("required", []) if isinstance(vacc, dict) else []
    if any(is_universally_required_vaccine(str(v), "yellow fever") for v in req):
        hooks.append("yellow fever required")

    # 3. Healthcare quality
    rating = d.get("qualityRating", 3)
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        rating = 3
    if rating == 5:
        hooks.append("world-class hospitals")
    elif rating == 4:
        hooks.append("good private healthcare")
    elif rating <= 2:
        hooks.append("limited public healthcare")

    # 4. Water safety
    water = d.get("waterSafety", "")
    if water in ("bottled-only", "unsafe"):
        hooks.append("bottled water only")

    # 5. Insurance required
    ins = d.get("travelInsurance", {})
    if isinstance(ins, dict) and ins.get("required"):
        hooks.append("insurance required for visa")

    # 6. EU 112 (only as a tertiary hook)
    if d.get("eu112") and len(hooks) < 2:
        hooks.append("EU 112 emergency")

    # Compose. Aim for 130-160 chars.
    # Try with up to 2 hooks; if too long, drop hooks one at a time so we
    # never emit a "..."-truncated meta description (bad for SERP CTR).
    tail = " Hospital info, pharmacy tips, vaccinations, and travel insurance."
    selected = list(hooks[:2])
    while True:
        parts = [f"Travel health guide for {name}"]
        if em_short:
            parts.append(f"emergency {em_short}")
        parts.extend(selected)
        candidate = ", ".join(parts) + "." + tail
        if len(candidate) <= 160 or not selected:
            break
        selected.pop()  # drop the last hook and retry

    # Final safety net: if even the no-hooks version is too long (very long
    # country name or emergency number), trim the trailing tail.
    if len(candidate) > 160:
        candidate = candidate[:160].rstrip(", .")
    return candidate


def metadescription_is_generic(md: str) -> bool:
    if not md.startswith(META_TEMPLATE_PREFIX):
        return False
    md_lower = md.lower()
    return not any(h in md_lower for h in META_HOOKS)


def fix_file(path: Path, dry_run: bool) -> dict:
    """Apply all Tier 1 fixes to a single JSON file. Returns a dict of
    {field_name: 'before -> after'} for each change made."""
    text = path.read_text(encoding="utf-8")
    d = json.loads(text)
    changes: dict[str, str] = {}

    # 1 & 2. lastUpdated date fixes
    last = d.get("lastUpdated", "")
    if last == MALFORMED_DATE:
        d["lastUpdated"] = TODAY
        changes["lastUpdated"] = f"{MALFORMED_DATE!r} → {TODAY!r} (malformed)"
    elif last and last <= STALE_DATE:
        d["lastUpdated"] = TODAY
        changes["lastUpdated"] = f"{last!r} → {TODAY!r} (stale)"

    # 3. Embassy boilerplate in mentalHealth.internationalLine → delete it,
    # let build script's findahelpline.com fallback take over.
    mh = d.get("mentalHealth")
    if isinstance(mh, dict):
        intl = mh.get("internationalLine", "")
        if EMBASSY_BOILERPLATE in intl:
            del mh["internationalLine"]
            changes["mentalHealth.internationalLine"] = (
                f"removed (was {EMBASSY_BOILERPLATE!r}); "
                f"build script will emit findahelpline.com fallback"
            )

        # 4. Cuba's englishTherapists has the boilerplate
        eth = mh.get("englishTherapists", "")
        if EMBASSY_BOILERPLATE in eth:
            mh["englishTherapists"] = CU_ENGLISH_THERAPISTS_REPLACEMENT
            changes["mentalHealth.englishTherapists"] = (
                f"replaced embassy boilerplate with country-specific note"
            )

    # 5. Generic metaDescription → compose from structured data
    md = d.get("metaDescription", "")
    if metadescription_is_generic(md):
        new_md = compose_meta_description(d)
        d["metaDescription"] = new_md
        changes["metaDescription"] = (
            f"({len(md)}c generic) → ({len(new_md)}c) {new_md!r}"
        )

    if changes and not dry_run:
        # Preserve formatting style: 2-space indent, no trailing newline manipulation
        new_text = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
        path.write_text(new_text, encoding="utf-8")

    return changes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = ap.parse_args()

    files = sorted(p for p in DATA_DIR.glob("*.json") if is_canonical(p))
    print(f"Scanning {len(files)} canonical health-data files…\n")

    summary = {
        "lastUpdated_fixed": 0,
        "internationalLine_removed": 0,
        "englishTherapists_replaced": 0,
        "metaDescription_personalized": 0,
        "files_changed": 0,
    }

    for f in files:
        changes = fix_file(f, args.dry_run)
        if not changes:
            continue
        summary["files_changed"] += 1
        if "lastUpdated" in changes:
            summary["lastUpdated_fixed"] += 1
        if "mentalHealth.internationalLine" in changes:
            summary["internationalLine_removed"] += 1
        if "mentalHealth.englishTherapists" in changes:
            summary["englishTherapists_replaced"] += 1
        if "metaDescription" in changes:
            summary["metaDescription_personalized"] += 1
        print(f"{f.stem}:")
        for k, v in changes.items():
            print(f"  {k}: {v}")
        print()

    print("=" * 60)
    print(f"Files changed: {summary['files_changed']}")
    print(f"  lastUpdated fixed:           {summary['lastUpdated_fixed']}")
    print(f"  internationalLine removed:   {summary['internationalLine_removed']}")
    print(f"  englishTherapists replaced:  {summary['englishTherapists_replaced']}")
    print(f"  metaDescription personalized:{summary['metaDescription_personalized']}")
    if args.dry_run:
        print("\n(dry run — no files written)")


if __name__ == "__main__":
    main()
