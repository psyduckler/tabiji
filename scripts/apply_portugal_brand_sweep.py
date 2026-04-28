#!/usr/bin/env python3
"""Paragraph-scoped lowercase-brand sweep for Portugal scam pages.

For each <p class="scam-story-body"> that ends with a <strong>...</strong>
bolded summary, the bolded summary is the canonical capitalization for that
paragraph (the author already wrote brand/proper-noun tokens correctly there).
This script substitutes the lowercase forms of those tokens in the body
prose with their canonical forms — but only for tokens whose canonical form
appears in the bolded summary of the *same paragraph*.

Per the Lyon/Annecy "Pickpocketing" lesson in the project memory:
- Paragraph-scoped, never file-wide blanket replace
- Word-boundary regex
- Case-sensitive (won't touch already-correct text)
- Only substitutes tokens validated by the same paragraph's bolded summary

Usage:
    python3 scripts/apply_portugal_brand_sweep.py --dry-run    # preview only
    python3 scripts/apply_portugal_brand_sweep.py              # apply
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return Path(out)


REPO = repo_root()
CITIES = ["funchal", "albufeira", "sintra", "faro", "cascais"]

# Substitution map: lowercase-form -> canonical-form
# The canonical form must appear in the paragraph's bolded summary for the
# substitution to fire (per-paragraph validation).
SUBSTITUTIONS = {
    # Brand names
    "bolt": "Bolt",
    "uber": "Uber",
    "idealista": "Idealista",
    "facebook marketplace": "Facebook Marketplace",
    "revolut": "Revolut",
    "bizum": "Bizum",
    "welcome pickups": "Welcome Pickups",
    "eva transportes": "Eva Transportes",
    "getyourguide": "GetYourGuide",
    "tiqets": "Tiqets",
    "headout": "Headout",
    "google ads": "Google Ads",
    "google reviews": "Google Reviews",
    "booking.com": "Booking.com",
    "airbnb": "Airbnb",
    "vrbo": "VRBO",
    "whatsapp": "WhatsApp",
    "sahibinden": "Sahibinden",
    "tui": "TUI",
    "jet2": "Jet2",
    "ryanair": "Ryanair",
    "rodavante": "Rodavante",
    "sixt": "Sixt",
    "auto-jardim": "Auto-Jardim",
    "goldcar": "Goldcar",
    "centauro": "Centauro",
    "klass wagen": "Klass Wagen",
    "blandy's wine lodge": "Blandy's Wine Lodge",
    "taberna da poncha": "Taberna da Poncha",
    "pingo doce": "Pingo Doce",
    "lidl": "Lidl",
    "continente": "Continente",
    "caixa geral de depósitos": "Caixa Geral de Depósitos",
    "millennium bcp": "Millennium BCP",
    "santander": "Santander",
    "multibanco": "Multibanco",

    # Acronyms / institutional names
    "gnr": "GNR",
    "psp": "PSP",
    "fao": "FAO",
    "fnc": "FNC",
    "lis": "LIS",
    "atms": "ATMs",
    "atm": "ATM",
    "pdf": "PDF",
    "cctv": "CCTV",
    "mb way": "MB WAY",
    "cmvm": "CMVM",
    "asae": "ASAE",
    "ctt": "CTT",
    "decreto-lei": "Decreto-Lei",

    # Brand-style domain names (the bullet lists capitalize these explicitly)
    "madeira.fun": "Madeira.fun",
    "polícia judiciária": "Polícia Judiciária",
    "polícia de segurança pública": "Polícia de Segurança Pública",
    "turismo de portugal": "Turismo de Portugal",
    "dgv portugal": "DGV Portugal",
    "uk action fraud": "UK Action Fraud",
    "irish consumer protection commission": "Irish Consumer Protection Commission",

    # Place names (multi-word)
    "pena palace": "Pena Palace",
    "castelo dos mouros": "Castelo dos Mouros",
    "quinta da regaleira": "Quinta da Regaleira",
    "parques de sintra": "Parques de Sintra",
    "volta do duche": "Volta do Duche",
    "são pedro de sintra": "São Pedro de Sintra",
    "cerro da alagoa": "Cerro da Alagoa",
    "rua dos pescadores": "Rua dos Pescadores",
    "praia dos pescadores": "Praia dos Pescadores",
    "praia da oura": "Praia da Oura",
    "oura strip": "Oura Strip",
    "rua do município": "Rua do Município",
    "rua de santo antónio": "Rua de Santo António",
    "rua do prior": "Rua do Prior",
    "rua quebra costas": "Rua Quebra Costas",
    "ria formosa": "Ria Formosa",
    "ilha de faro": "Ilha de Faro",
    "jardim manuel bivar": "Jardim Manuel Bivar",
    "câmara de lobos": "Câmara de Lobos",
    "monte palace tropical garden": "Monte Palace Tropical Garden",
    "monte cable-car": "Monte cable-car",
    "vilamoura marina": "Vilamoura Marina",
    "via verde": "Via Verde",

    # Single-word place names (validated by bold to avoid false positives)
    "monte": "Monte",
    "livramento": "Livramento",
    "aerobus": "Aerobus",
    "vilamoura": "Vilamoura",
    "alfama": "Alfama",
    "baixa": "Baixa",
    "rossio": "Rossio",
    "ribeira": "Ribeira",
    "cascais": "Cascais",
    "funchal": "Funchal",
    "albufeira": "Albufeira",
    "lagos": "Lagos",
    "sintra": "Sintra",
    "lisbon": "Lisbon",
    "porto": "Porto",
    "madeira": "Madeira",
    "algarve": "Algarve",

    # Months
    "april": "April",
    "may": "May",
    "june": "June",
    "july": "July",
    "august": "August",
    "september": "September",
    "october": "October",
    "november": "November",
    "december": "December",
    "january": "January",
    "february": "February",
    "march": "March",

    # Days
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",

    # Currency / nationality
    "gbp": "GBP",
    "eur": "EUR",
    "usd": "USD",
    "uk": "UK",
    "uk/irish": "UK/Irish",
    "uk/irish/german": "UK/Irish/German",
    "irish": "Irish",
    "german": "German",
    "british": "British",
    "northern european": "Northern European",
    "european": "European",
    "english": "English",
    "portuguese": "Portuguese",
    "portugal's": "Portugal's",

    # Other
    "pr": "PR",  # public relations (short form)
}

# Sort by length descending so multi-word substitutions match before single-word
SUB_ITEMS = sorted(SUBSTITUTIONS.items(), key=lambda kv: -len(kv[0]))

# Second-pass allowlist: tokens that are unambiguously proper nouns / brand
# names / acronyms — safe to substitute file-wide (still with URL-skip
# lookahead). Use this only for tokens with no other plausible meaning in any
# context. Per the Lyon/Annecy lesson, anything ambiguous should stay in the
# paragraph-scoped pass above.
GLOBAL_TOKENS = {
    # Acronyms / institutions (always uppercase in any context)
    "fao": "FAO",
    "fnc": "FNC",
    "lis": "LIS",
    "psp": "PSP",
    "gnr": "GNR",
    "cmvm": "CMVM",
    "asae": "ASAE",
    "ctt": "CTT",
    "cctv": "CCTV",
    "atm": "ATM",
    "atms": "ATMs",
    "pdf": "PDF",
    # Portuguese institutions
    "polícia judiciária": "Polícia Judiciária",
    "polícia de segurança pública": "Polícia de Segurança Pública",
    "turismo de portugal": "Turismo de Portugal",
    "dgv portugal": "DGV Portugal",
    "decreto-lei": "Decreto-Lei",
    "caixa geral de depósitos": "Caixa Geral de Depósitos",
    "millennium bcp": "Millennium BCP",
    # Brands
    "bolt": "Bolt",
    "uber": "Uber",
    "revolut": "Revolut",
    "bizum": "Bizum",
    "idealista": "Idealista",
    "headout": "Headout",
    "tiqets": "Tiqets",
    "getyourguide": "GetYourGuide",
    "google ads": "Google Ads",
    "google reviews": "Google Reviews",
    "facebook marketplace": "Facebook Marketplace",
    "booking.com": "Booking.com",
    "welcome pickups": "Welcome Pickups",
    "eva transportes": "Eva Transportes",
    "klass wagen": "Klass Wagen",
    "rodavante": "Rodavante",
    "auto-jardim": "Auto-Jardim",
    "blandy's wine lodge": "Blandy's Wine Lodge",
    "taberna da poncha": "Taberna da Poncha",
    "pingo doce": "Pingo Doce",
    # Place names with no other meaning in any plausible context
    "pena palace": "Pena Palace",
    "castelo dos mouros": "Castelo dos Mouros",
    "quinta da regaleira": "Quinta da Regaleira",
    "parques de sintra": "Parques de Sintra",
    "volta do duche": "Volta do Duche",
    "são pedro de sintra": "São Pedro de Sintra",
    "cerro da alagoa": "Cerro da Alagoa",
    "câmara de lobos": "Câmara de Lobos",
    "ria formosa": "Ria Formosa",
    "ilha de faro": "Ilha de Faro",
    "jardim manuel bivar": "Jardim Manuel Bivar",
    "praia da oura": "Praia da Oura",
    "praia dos pescadores": "Praia dos Pescadores",
    "rua dos pescadores": "Rua dos Pescadores",
    "rua de santo antónio": "Rua de Santo António",
    "rua quebra costas": "Rua Quebra Costas",
    "rua do prior": "Rua do Prior",
    "rua do município": "Rua do Município",
    "monte palace tropical garden": "Monte Palace Tropical Garden",
    # Days
    "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
    "thursday": "Thursday", "friday": "Friday", "saturday": "Saturday",
    "sunday": "Sunday",
}
GLOBAL_ITEMS = sorted(GLOBAL_TOKENS.items(), key=lambda kv: -len(kv[0]))


def fix_paragraph(body: str, bold_text: str) -> tuple[str, list[tuple[str, str, int]]]:
    """Apply substitutions in body where the canonical form appears in bold_text.

    Returns (new_body, fixes_applied) where fixes_applied is a list of
    (lowercase, canonical, count) tuples.
    """
    fixes: list[tuple[str, str, int]] = []
    new_body = body
    seen_positions: set[tuple[int, int]] = set()

    for lower, canonical in SUB_ITEMS:
        # Skip if the canonical form doesn't appear in the bold (per-paragraph validation)
        # Use word-boundary check to avoid e.g. "Bolt" matching inside "Boltz"
        if not re.search(rf'\b{re.escape(canonical)}\b', bold_text):
            continue

        # Case-sensitive search for lowercase form in body.
        # Negative lookahead skips URL/domain patterns (foo.bar) — those are
        # only safe to substitute via an explicit multi-char map entry like
        # "madeira.fun" → "Madeira.fun" that has already matched (and reserved
        # its positions in seen_positions) earlier in this loop iteration.
        pattern = rf'\b{re.escape(lower)}\b(?!\.[a-z])'
        matches = list(re.finditer(pattern, new_body))
        if not matches:
            continue

        # Filter out already-claimed positions (longer-match-first dedup)
        applicable = [m for m in matches if not any(
            sp[0] <= m.start() < sp[1] for sp in seen_positions
        )]
        if not applicable:
            continue

        # Apply substitutions (right-to-left to preserve indexes)
        for m in reversed(applicable):
            new_body = new_body[:m.start()] + canonical + new_body[m.end():]
            seen_positions.add((m.start(), m.start() + len(canonical)))

        fixes.append((lower, canonical, len(applicable)))

    return new_body, fixes


def process_file(path: Path, apply: bool) -> tuple[int, int]:
    """Returns (paragraphs_changed, total_substitutions).

    Handles two page structures observed across Portugal cities:
    1. Inline-bold (albufeira/sintra/cascais): each scam-story-body ends with
       a <strong> bolded summary that serves as the ground-truth canonical
       capitalization for that paragraph.
    2. Separate-avoid-list (funchal/faro): scam-story-body paragraphs have NO
       inline <strong>; the canonical capitalization lives in the same
       scam-card's <div class="detail-block avoid"> <ul> bullets.
    """
    content = path.read_text()
    new_content = content
    paragraphs_changed = 0
    total_subs = 0

    # Pre-build per-scam-card "avoid bullets text" for the separate-list cities
    # Map: (card_start_offset, card_end_offset) -> bullets_text
    card_pattern = re.compile(
        r'<div class="scam-card"[^>]*id="scam-\d+"[^>]*>(.*?)(?=<div class="scam-card"|<a class="book-mid-cta"|<section)',
        re.DOTALL,
    )
    card_avoid_text: list[tuple[int, int, str]] = []
    for cm in card_pattern.finditer(content):
        card_inner = cm.group(1)
        # Find the avoid-block bullets within this card
        am = re.search(
            r'<div class="detail-block avoid">(.*?)</div>',
            card_inner, re.DOTALL,
        )
        bullets_text = ""
        if am:
            bullets_text = re.sub(r'<[^>]+>', ' ', am.group(1))
        card_avoid_text.append((cm.start(), cm.end(), bullets_text))

    def avoid_text_for_offset(offset: int) -> str:
        for s, e, t in card_avoid_text:
            if s <= offset < e:
                return t
        return ""

    # Find each scam-story-body paragraph
    para_pattern = re.compile(r'<p class="scam-story-body">(.*?)</p>', re.DOTALL)
    matches = list(para_pattern.finditer(content))

    # Build replacements; apply right-to-left to preserve offsets
    para_replacements: list[tuple[int, int, str, list[tuple[str, str, int]]]] = []
    for m in matches:
        para_inner = m.group(1)
        has_inline_bold = '<strong>' in para_inner

        if has_inline_bold:
            body, _, bold_with_tag = para_inner.partition('<strong>')
            bold = re.sub(r'</strong>.*$', '', bold_with_tag, flags=re.DOTALL)
            bold_text = re.sub(r'<[^>]+>', '', bold)
        else:
            # Use the scam-card's avoid-bullets as ground truth
            body = para_inner
            bold_with_tag = ""
            bold_text = avoid_text_for_offset(m.start())
            if not bold_text:
                continue

        new_body, fixes = fix_paragraph(body, bold_text)
        if not fixes:
            continue

        if has_inline_bold:
            new_para_inner = new_body + '<strong>' + bold_with_tag
        else:
            new_para_inner = new_body
        new_para_full = f'<p class="scam-story-body">{new_para_inner}</p>'
        para_replacements.append((m.start(), m.end(), new_para_full, fixes))

    if not para_replacements:
        return 0, 0

    # Print proposed changes
    print(f"\n┌─ {path.relative_to(REPO)}")
    for start, end, _, fixes in para_replacements:
        ln = content[:start].count('\n') + 1
        sub_count = sum(c for _, _, c in fixes)
        paragraphs_changed += 1
        total_subs += sub_count
        print(f"│  L{ln}: {sub_count} substitutions")
        for lower, canonical, count in fixes:
            print(f"│    {lower!r} → {canonical!r} ({count}x)")

    if apply:
        # Apply right-to-left
        for start, end, new_para, _ in reversed(para_replacements):
            new_content = new_content[:start] + new_para + new_content[end:]
        path.write_text(new_content)
        print(f"└─ APPLIED: {paragraphs_changed} paragraphs, {total_subs} substitutions")
    else:
        print(f"└─ DRY-RUN: would apply {paragraphs_changed} paragraphs, {total_subs} substitutions")

    return paragraphs_changed, total_subs


def apply_global_pass(path: Path, apply: bool) -> int:
    """Second pass: substitute always-cap tokens file-wide within scam-story-body
    paragraphs only (still scoped — won't touch ToC, comments, code, etc.).
    Skips URL/domain patterns via lookahead.
    """
    content = path.read_text()
    new_content = content
    total_subs = 0

    para_pattern = re.compile(r'(<p class="scam-story-body">)(.*?)(</p>)', re.DOTALL)

    def fix_para(match):
        nonlocal total_subs
        body = match.group(2)
        new_body = body
        seen_positions: set[tuple[int, int]] = set()
        for lower, canonical in GLOBAL_ITEMS:
            pattern = rf'\b{re.escape(lower)}\b(?!\.[a-z])'
            matches = list(re.finditer(pattern, new_body))
            applicable = [m for m in matches if not any(
                sp[0] <= m.start() < sp[1] for sp in seen_positions
            )]
            if not applicable:
                continue
            for m in reversed(applicable):
                new_body = new_body[:m.start()] + canonical + new_body[m.end():]
                seen_positions.add((m.start(), m.start() + len(canonical)))
            total_subs += len(applicable)
        return match.group(1) + new_body + match.group(3)

    new_content = para_pattern.sub(fix_para, content)
    if total_subs > 0 and apply:
        path.write_text(new_content)
    return total_subs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Preview only, do not modify files")
    args = ap.parse_args()

    print("=== PASS 1: paragraph-scoped (uses inline <strong> or scam-card avoid bullets as ground truth) ===")
    grand_paras = 0
    grand_subs = 0
    for city in CITIES:
        path = REPO / "scams" / city / "index.html"
        p, s = process_file(path, apply=not args.dry_run)
        grand_paras += p
        grand_subs += s

    print()
    print(f"PASS 1 TOTAL: {grand_paras} paragraphs, {grand_subs} substitutions")

    print()
    print("=== PASS 2: file-wide always-cap allowlist (within scam-story-body paragraphs only) ===")
    pass2_subs = 0
    for city in CITIES:
        path = REPO / "scams" / city / "index.html"
        n = apply_global_pass(path, apply=not args.dry_run)
        if n > 0:
            print(f"  {city}: {n} substitutions")
        pass2_subs += n
    print(f"PASS 2 TOTAL: {pass2_subs} substitutions")

    print()
    print(f"GRAND TOTAL: {grand_subs + pass2_subs} substitutions across {len(CITIES)} cities")
    if args.dry_run:
        print("(dry-run only — re-run without --dry-run to apply)")


if __name__ == "__main__":
    main()
