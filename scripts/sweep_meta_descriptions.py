#!/usr/bin/env python3
"""Sweep boilerplate meta descriptions -> unique per-city strings.

481 of 490 scam city pages ship the identical boilerplate meta description
("{n} real {city} tourist scams documented from Reddit travelers in 2026..."),
which is an SEO liability (Google rewrites duplicates, CTR suffers). This
sweeper parses each page with BeautifulSoup to extract the city name and its
top 3 scam titles, then rewrites four on-page fields to city-specific copy:

    1. <meta name="description">
    2. <meta property="og:description">
    3. <meta name="twitter:description">  (90-char compact variant)
    4. JSON-LD Article "description"

The script is **idempotent** — it only touches pages whose current meta
description matches the boilerplate regex exactly. Pages already carrying
bespoke copy (capri, dubrovnik, hong-kong, lake-garda, pisa, etc.) are left
alone.

Usage:
    python3 scripts/sweep_meta_descriptions.py --dry-run
    python3 scripts/sweep_meta_descriptions.py --dry-run --limit 5
    python3 scripts/sweep_meta_descriptions.py --city rome
    python3 scripts/sweep_meta_descriptions.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

# Current boilerplate — if meta desc matches this, we rewrite. Otherwise skip.
BOILERPLATE_RE = re.compile(
    r"^\d+ real [^\"]+ tourist scams documented from Reddit travel(?:l)?ers in 2026\. "
    r"Know what to watch for before you arrive"
)

# SEO soft caps (Google truncates descriptions around 155-160 chars in SERPs).
LEN_TARGET_MAX = 160
LEN_TARGET_MIN = 120
LEN_HARD_CAP = 300
TWITTER_TARGET = 110  # Twitter allows more but we keep it compact-ish.
FILLER = " Locations, costs, and recovery steps included."


def _extract_city(soup: BeautifulSoup) -> str | None:
    """Pull the city name out of `<h1>N Tourist Scams in <em>City</em></h1>`.

    Editorial-v2 wraps the city in `<em>`; fall back to the last word of the
    h1 text if that's absent.
    """
    h1 = soup.find("h1")
    if not h1:
        return None
    em = h1.find("em")
    if em:
        city = em.get_text(strip=True)
        if city:
            return city
    # Fallback: strip "N Tourist Scams in " prefix.
    text = h1.get_text(strip=True)
    m = re.match(r"^\d+\s+Tourist Scams in\s+(.+)$", text)
    if m:
        return m.group(1).strip()
    return None


def _extract_scam_titles(soup: BeautifulSoup) -> list[str]:
    """Return all `.scam-title` texts in document order."""
    return [t.get_text(strip=True) for t in soup.select(".scam-title")]


def _length(s: str) -> int:
    return len(s)


def _compose_primary(city: str, n: int, titles: list[str]) -> str:
    """Build the 120-160 char meta/og description.

    Policy (in order — stop as soon as the result lands in the target window):
      1. Try 3 full scams.
      2. Fall back to 2 full scams if (1) is over LEN_TARGET_MAX.
      3. Truncate titles inside the 2-scam variant down to 30 chars each.
      4. Drop to 1 scam (truncated to 40) as a last resort for long titles.
      5. Pad short results with `FILLER` until we clear LEN_TARGET_MIN.
    """

    def build(ts: list[str]) -> str:
        if len(ts) >= 3:
            head = f"{ts[0]}, {ts[1]}, and {ts[2]}"
        elif len(ts) == 2:
            head = f"{ts[0]} and {ts[1]}"
        elif len(ts) == 1:
            head = ts[0]
        else:
            head = "common traps"
        return (
            f"Watch for {head} in {city} \u2014 {n} documented 2026 scams "
            "with red flags and how to avoid them. Real traveler reports."
        )

    candidates: list[str] = []

    # 1) three full scams
    if len(titles) >= 3:
        candidates.append(build(titles[:3]))

    # 2) two full scams
    if len(titles) >= 2:
        candidates.append(build(titles[:2]))

    # 3) two truncated-to-30 scams
    if len(titles) >= 2:
        candidates.append(build([_truncate_title(t, 30) for t in titles[:2]]))

    # 4) two truncated-to-22 scams (aggressive — for very long city names)
    if len(titles) >= 2:
        candidates.append(build([_truncate_title(t, 22) for t in titles[:2]]))

    # 5) single truncated scam (adaptive cap based on remaining budget)
    if titles:
        # Fixed-width scaffold outside the {head} slot:
        #   "Watch for  in {city} \u2014 {n} documented 2026 scams with red "
        #   "flags and how to avoid them. Real traveler reports."
        scaffold = (
            f"Watch for  in {city} \u2014 {n} documented 2026 scams "
            "with red flags and how to avoid them. Real traveler reports."
        )
        budget = max(12, LEN_TARGET_MAX - len(scaffold))
        candidates.append(build([_truncate_title(titles[0], budget)]))

    # Prefer the first candidate that fits the window.
    for cand in candidates:
        if LEN_TARGET_MIN <= _length(cand) <= LEN_TARGET_MAX:
            return cand

    # If none fit, prefer the longest under the cap (so we don't under-use the
    # SERP real estate) — then pad if still short.
    under_cap = [c for c in candidates if _length(c) <= LEN_TARGET_MAX]
    if under_cap:
        desc = max(under_cap, key=_length)
        while _length(desc) < LEN_TARGET_MIN and _length(desc) + len(FILLER) <= LEN_TARGET_MAX:
            desc += FILLER
        return desc

    # Everything is still too long — return the shortest so the caller can
    # decide whether to fall back to the AmE boilerplate.
    return min(candidates, key=_length) if candidates else build([])


_TRAILING_JUNK = {
    "and", "or", "the", "a", "an", "of", "in", "on", "at", "to", "for",
    "with", "from", "by", "&", "/",
}


def _truncate_title(title: str, cap: int) -> str:
    """Trim a single scam title to fit under `cap` chars without mid-word cut.

    Also strips trailing stopwords/conjunctions so we don't end up with copy
    like "Fake Guide and" or "Taxi Overcharging and Rigged".
    """
    if len(title) <= cap:
        return title
    # Cut at last word boundary before cap.
    clipped = title[:cap].rsplit(" ", 1)[0]
    clipped = clipped.rstrip(" ,-.&/\u2014")
    # Drop trailing stopwords iteratively (e.g. "and", "of", "the") and strip
    # dangling words that start with unmatched quotes/parens.
    while True:
        words = clipped.split(" ")
        if not words:
            break
        last = words[-1]
        last_norm = last.lower().strip("'\"()[]")
        if len(words) > 1 and (
            last_norm in _TRAILING_JUNK
            or (last.startswith(("'", '"', "(", "[")) and not _is_closed(last))
        ):
            clipped = " ".join(words[:-1]).rstrip(" ,-.&/\u2014")
        else:
            break
    return clipped or title[:cap]


def _is_closed(token: str) -> bool:
    """True if a token has balanced quotes/parens."""
    return (
        token.count("'") % 2 == 0
        and token.count('"') % 2 == 0
        and token.count("(") == token.count(")")
        and token.count("[") == token.count("]")
    )


def _compose_twitter(city: str, titles: list[str]) -> str:
    """90-char compact Twitter description.

    Template: "Hard-won {city} travel safety: {scam1}, {scam2}, and more. 2026 edition."
    Falls back to trimming scam titles individually or dropping to top 1.
    """

    def build(ts: list[str]) -> str:
        if len(ts) >= 2:
            head = f"{ts[0]}, {ts[1]}, and more"
        elif len(ts) == 1:
            head = f"{ts[0]} and more"
        else:
            head = "common traps"
        return f"Hard-won {city} travel safety: {head}. 2026 edition."

    desc = build(titles[:2])
    if _length(desc) <= TWITTER_TARGET:
        return desc

    # Trim.
    trimmed = [_truncate_title(t, 22) for t in titles[:2]]
    desc = build(trimmed)
    if _length(desc) <= TWITTER_TARGET:
        return desc

    # Drop to 1.
    desc = build([_truncate_title(titles[0], 30)]) if titles else build([])
    return desc


def _compose_fallback(city: str, n: int) -> str:
    """AmE-corrected version of the original boilerplate (last resort)."""
    return (
        f"{n} real {city} tourist scams documented from Reddit travelers in "
        "2026. Know what to watch for before you arrive \u2014 and exactly "
        "how to stay safe."
    )


def _compose_jsonld(city: str, n: int, titles: list[str], primary: str) -> str:
    """JSON-LD Article description.

    Mirror the meta description — same content works inside Article schema.
    Kept as a separate helper in case we want to diverge later.
    """
    return primary


def _html_attr_escape(value: str) -> str:
    """Escape a value for use inside an HTML attribute (minimal; double quotes
    are the only delimiter we need to guard against since our template uses
    `content=\"...\"`)."""
    return value.replace("&", "&amp;").replace("\"", "&quot;").replace("<", "&lt;")


def _json_string_escape(value: str) -> str:
    """Escape for use inside a JSON string literal."""
    return (
        value.replace("\\", "\\\\")
        .replace("\"", "\\\"")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


META_DESC_RE = re.compile(
    r'(<meta name="description" content=")([^"]*)(">)'
)
OG_DESC_RE = re.compile(
    r'(<meta property="og:description" content=")([^"]*)(">)'
)
TW_DESC_RE = re.compile(
    r'(<meta name="twitter:description" content=")([^"]*)(">)'
)
JSONLD_DESC_RE = re.compile(
    r'("description":\s*")([^"]*)(",)'
)


def rewrite_page(text: str, primary: str, twitter: str, jsonld: str) -> tuple[str, int]:
    """Apply all four description swaps to `text`. Returns (new_text, swaps)."""
    swaps = 0

    def apply_one(current: str, pattern: re.Pattern, replacement: str, escape_fn) -> tuple[str, int]:
        return pattern.subn(
            lambda m: f"{m.group(1)}{escape_fn(replacement)}{m.group(3)}",
            current,
            count=1,
        )

    text, n = apply_one(text, META_DESC_RE, primary, _html_attr_escape)
    swaps += n
    text, n = apply_one(text, OG_DESC_RE, primary, _html_attr_escape)
    swaps += n
    text, n = apply_one(text, TW_DESC_RE, twitter, _html_attr_escape)
    swaps += n
    text, n = apply_one(text, JSONLD_DESC_RE, jsonld, _json_string_escape)
    swaps += n
    return text, swaps


def process_page(
    path: Path, *, dry_run: bool
) -> tuple[str, str | None]:
    """Rewrite one city page.

    Returns ("rewrote", desc_primary) on success,
            ("skipped-nonboilerplate", None) if already individualized,
            ("skipped-noh1", None) if h1 unparseable,
            ("skipped-fewtitles", None) if < 2 scam-title elements,
            ("skipped-fallback", desc) if forced to fallback template.
    """
    original = path.read_text()
    soup = BeautifulSoup(original, "html.parser")

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    if not meta_desc_tag:
        return "skipped-nometa", None
    current = meta_desc_tag.get("content", "")
    if not BOILERPLATE_RE.match(current):
        return "skipped-nonboilerplate", None

    city = _extract_city(soup)
    if not city:
        return "skipped-noh1", None

    titles = _extract_scam_titles(soup)
    if len(titles) < 2:
        return "skipped-fewtitles", None

    n = len(titles)
    primary = _compose_primary(city, n, titles)

    used_fallback = False
    if len(primary) > LEN_HARD_CAP:
        primary = _compose_fallback(city, n)
        used_fallback = True

    twitter = _compose_twitter(city, titles)
    jsonld = _compose_jsonld(city, n, titles, primary)

    new_text, swaps = rewrite_page(original, primary, twitter, jsonld)
    if swaps < 4:
        # Didn't find all four fields — refuse to write a partially-updated file.
        return "skipped-missingfield", None

    if not dry_run:
        path.write_text(new_text)

    if used_fallback:
        return "rewrote-fallback", primary
    return "rewrote", primary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Print intended changes but don't write.")
    ap.add_argument("--limit", type=int, default=None, help="Process at most N pages.")
    ap.add_argument("--city", help="Only sweep scams/<city>/index.html")
    args = ap.parse_args()

    if args.city:
        targets = [SCAMS / args.city / "index.html"]
    else:
        targets = collect_scam_targets(city_pages=True)

    if args.limit is not None:
        targets = targets[: args.limit]

    rewrote = 0
    skipped_noscam = 0  # "no scam-title found" bucket per spec
    skipped_other = 0
    for path in targets:
        if not path.exists():
            continue
        slug = path.parent.name
        status, desc = process_page(path, dry_run=args.dry_run)
        if status in ("rewrote", "rewrote-fallback"):
            rewrote += 1
            tag = "FALLBACK" if status == "rewrote-fallback" else ""
            preview = (desc or "")[:60]
            print(
                f"  {slug}:{len(desc or '')} — desc_len={len(desc or '')} "
                f'"{preview}..." {tag}'.rstrip()
            )
        elif status in ("skipped-fewtitles", "skipped-noh1"):
            skipped_noscam += 1
            print(f"  {slug}: WARN — {status}")
        else:
            skipped_other += 1

    print(
        f"\n{'would rewrite' if args.dry_run else 'rewrote'} {rewrote} files, "
        f"{skipped_noscam} skipped (no scam-title found)"
    )
    if skipped_other:
        print(
            f"  (additionally {skipped_other} pages skipped — already "
            "individualized or missing meta fields)"
        )


if __name__ == "__main__":
    main()
