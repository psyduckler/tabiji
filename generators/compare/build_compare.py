#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"
API_COMPARE_DIR = REPO_ROOT / "api" / "v1" / "compare"
INVENTORY_PATH = COMPARE_DIR / "inventory.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path):
    return json.loads(read_text(path))


def find_tag_block(html: str, marker: str, tag: str, start_at: int = 0) -> Tuple[str, int, int]:
    start = html.find(marker, start_at)
    if start == -1:
        raise ValueError(f"Marker not found: {marker}")
    return extract_balanced_tag(html, start, tag)


def extract_balanced_tag(html: str, start: int, tag: str) -> Tuple[str, int, int]:
    open_re = re.compile(rf"<(?:{tag})\b", re.I)
    close_re = re.compile(rf"</(?:{tag})>", re.I)
    pos = start
    depth = 0
    first_open = open_re.search(html, pos)
    if not first_open or first_open.start() != start:
        raise ValueError(f"Expected <{tag}> at index {start}")
    pos = start
    while True:
        o = open_re.search(html, pos)
        c = close_re.search(html, pos)
        if not c:
            raise ValueError(f"Unclosed <{tag}> block starting at {start}")
        if o and o.start() < c.start():
            depth += 1
            pos = o.end()
        else:
            depth -= 1
            pos = c.end()
            if depth == 0:
                return html[start:pos], start, pos


def extract_jsonld_blocks(head_html: str) -> List[Dict]:
    blocks = []
    for match in re.finditer(r'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>', head_html):
        raw = match.group(1)
        try:
            blocks.append(json.loads(raw))
        except Exception:
            blocks.append({"parseError": True, "raw": raw})
    return blocks


def inner_html(block: str, tag: str) -> str:
    block = block.strip()
    open_end = block.find(">") + 1
    close_start = block.lower().rfind(f"</{tag.lower()}>")
    return block[open_end:close_start]


def extract_head_field(head_html: str, pattern: str, label: str) -> str:
    match = re.search(pattern, head_html, re.I | re.S)
    if not match:
        raise ValueError(f"Missing {label}")
    return match.group(1).strip()


def extract_meta_content(head_html: str, attr: str, value: str, label: str) -> str:
    tag_re = re.compile(r"<meta\b[^>]*>", re.I)
    for match in tag_re.finditer(head_html):
        tag = match.group(0)
        if re.search(rf'{attr}="{re.escape(value)}"', tag, re.I):
            content = re.search(r'content="([^"]*)"', tag, re.I)
            if content:
                return content.group(1).strip()
    raise ValueError(f"Missing {label}")


def extract_link_href(head_html: str, rel_value: str, label: str) -> str:
    tag_re = re.compile(r"<link\b[^>]*>", re.I)
    for match in tag_re.finditer(head_html):
        tag = match.group(0)
        if re.search(rf'rel="{re.escape(rel_value)}"', tag, re.I):
            href = re.search(r'href="([^"]*)"', tag, re.I)
            if href:
                return href.group(1).strip()
    raise ValueError(f"Missing {label}")


def extract_page(html_path: Path) -> Dict:
    html = read_text(html_path)
    slug = html_path.parent.name
    head = extract_head_field(html, r"<head>([\s\S]*?)</head>", "head block")
    body = extract_head_field(html, r"<body>([\s\S]*?)</body>", "body block")

    style_css = extract_head_field(head, r"<style>([\s\S]*?)</style>", "style block")
    title = extract_head_field(head, r"<title>(.*?)</title>", "title")
    meta_description = extract_meta_content(head, "name", "description", "meta description")
    og_title = extract_meta_content(head, "property", "og:title", "og:title")
    og_description = extract_meta_content(head, "property", "og:description", "og:description")
    og_image = extract_meta_content(head, "property", "og:image", "og:image")
    twitter_title = extract_meta_content(head, "name", "twitter:title", "twitter:title")
    twitter_description = extract_meta_content(head, "name", "twitter:description", "twitter:description")
    twitter_image = extract_meta_content(head, "name", "twitter:image", "twitter:image")
    published_time = extract_meta_content(head, "property", "article:published_time", "published time")
    modified_time = extract_meta_content(head, "property", "article:modified_time", "modified time")
    canonical = extract_link_href(head, "canonical", "canonical")

    jsonld = extract_jsonld_blocks(head)
    article_schema = next((b for b in jsonld if b.get("@type") == "Article"), None)
    breadcrumb_schema = next((b for b in jsonld if b.get("@type") == "BreadcrumbList"), None)
    faq_schema = next((b for b in jsonld if b.get("@type") == "FAQPage"), None)
    if not article_schema or not breadcrumb_schema or not faq_schema:
        raise ValueError(f"{slug}: missing required JSON-LD blocks")

    nav_block, _, _ = find_tag_block(body, "<nav>", "nav")
    hero_block, _, _ = find_tag_block(body, '<section class="hero">', "section")
    toc_mobile_block, _, toc_mobile_end = find_tag_block(body, '<div class="toc-mobile-sticky"', "div")
    methodology_block, _, _ = find_tag_block(body, '<div class="methodology-box">', "div")
    toc_sidebar_block, _, _ = find_tag_block(body, '<aside class="toc-sidebar">', "aside")
    photo_grid_block, _, photo_end = find_tag_block(body, '<div class="photo-grid">', "div")
    verdict_block, _, verdict_end = find_tag_block(body, '<div class="verdict-box">', "div", start_at=photo_end)
    comparison_block, _, comparison_end = find_tag_block(body, '<div class="comparison-section">', "div", start_at=verdict_end)

    deep_dives = []
    cursor = comparison_end
    while True:
        idx = body.find('<section class="deep-dive">', cursor)
        if idx == -1:
            break
        block, _, cursor = extract_balanced_tag(body, idx, "section")
        deep_dives.append(block)

    faq_block, _, faq_end = find_tag_block(body, '<section class="faq-section">', "section")
    cta_block, _, _ = find_tag_block(body, '<div class="cta-section">', "div", start_at=faq_end)
    footer_block, _, footer_end = find_tag_block(body, '<footer>', "footer")

    script_blocks = [m.group(0) for m in re.finditer(r"<script[\s\S]*?</script>", body[footer_end:])]

    toc_items = [
        {"href": m.group(1), "label": m.group(2)}
        for m in re.finditer(r'<li><a href="([^"]+)">([\s\S]*?)</a></li>', toc_sidebar_block)
    ]

    faq_items = [
        {"question": re.sub(r"<[^>]+>", "", m.group(1)).strip(), "answer": re.sub(r"<[^>]+>", "", m.group(2)).strip()}
        for m in re.finditer(r'<div class="faq-item">\s*<h3>([\s\S]*?)</h3>\s*<p>([\s\S]*?)</p>\s*</div>', faq_block)
    ]

    api_json = load_json(API_COMPARE_DIR / f"{slug}.json")

    return {
        "slug": slug,
        "pageType": "compare-leaf",
        "status": "published",
        "destinations": {
            "destination1": api_json["destination1"],
            "destination2": api_json["destination2"],
        },
        "seo": {
            "title": title,
            "metaDescription": meta_description,
            "ogTitle": og_title,
            "ogDescription": og_description,
            "ogImage": og_image,
            "twitterTitle": twitter_title,
            "twitterDescription": twitter_description,
            "twitterImage": twitter_image,
            "publishedTime": published_time,
            "modifiedTime": modified_time,
            "canonical": canonical,
        },
        "schema": {
            "article": article_schema,
            "breadcrumb": breadcrumb_schema,
            "faq": faq_schema,
        },
        "shell": {
            "styleCss": style_css,
            "navHtml": nav_block,
            "footerHtml": footer_block,
            "scripts": script_blocks,
        },
        "content": {
            "heroHtml": hero_block,
            "tocMobileHtml": toc_mobile_block,
            "methodologyHtml": methodology_block,
            "tocSidebarHtml": toc_sidebar_block,
            "tocItems": toc_items,
            "photoGridHtml": photo_grid_block,
            "verdictHtml": verdict_block,
            "comparisonHtml": comparison_block,
            "deepDiveHtml": deep_dives,
            "faqHtml": faq_block,
            "faqItems": faq_items,
            "ctaHtml": cta_block,
        },
    }


def render_page(data: Dict) -> str:
    seo = data["seo"]
    schema = data["schema"]
    shell = data["shell"]
    content = data["content"]
    return f"""<!DOCTYPE html>

<html lang=\"en\">
<head>
<meta charset=\"utf-8\"/>
<meta content=\"width=device-width, initial-scale=1.0\" name=\"viewport\"/>
<script async=\"\" src=\"https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ\"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
<link href=\"/favicon.ico\" rel=\"icon\" type=\"image/x-icon\"/>
<link href=\"https://img.tabiji.ai/apple-touch-icon.png\" rel=\"apple-touch-icon\" sizes=\"180x180\"/>
<link href=\"https://img.tabiji.ai/icon-192.png\" rel=\"icon\" sizes=\"192x192\" type=\"image/png\"/>
<title>{seo['title']}</title>
<meta content=\"{seo['metaDescription']}\" name=\"description\"/>
<meta content=\"{seo['ogTitle']}\" property=\"og:title\"/>
<meta content=\"{seo['ogDescription']}\" property=\"og:description\"/>
<meta content=\"article\" property=\"og:type\"/>
<meta content=\"{seo['canonical']}\" property=\"og:url\"/>
<meta content=\"{seo['ogImage']}\" property=\"og:image\"/>
<meta content=\"tabiji.ai\" property=\"og:site_name\"/>
<meta content=\"summary_large_image\" name=\"twitter:card\"/>
<meta content=\"{seo['twitterTitle']}\" name=\"twitter:title\"/>
<meta content=\"{seo['twitterDescription']}\" name=\"twitter:description\"/>
<meta content=\"{seo['twitterImage']}\" name=\"twitter:image\"/>
<meta content=\"{seo['publishedTime']}\" property=\"article:published_time\"/>
<meta content=\"{seo['modifiedTime']}\" property=\"article:modified_time\"/>
<meta content=\"index, follow, max-image-preview:large\" name=\"robots\"/>
<link href=\"{seo['canonical']}\" rel=\"canonical\"/>
<!-- Schema: Article -->
<script type=\"application/ld+json\">{json.dumps(schema['article'], ensure_ascii=False, indent=4)}</script>
<!-- Schema: BreadcrumbList -->
<script type=\"application/ld+json\">{json.dumps(schema['breadcrumb'], ensure_ascii=False, indent=4)}</script>
<!-- Schema: FAQPage -->
<script type=\"application/ld+json\">{json.dumps(schema['faq'], ensure_ascii=False, indent=4)}</script>
<style>
{shell['styleCss']}
</style>
<!-- @include:shared-head:start -->
<link rel=\"stylesheet\" href=\"/assets/shared-shell.css\">
<script defer src=\"/assets/shared-shell.js\"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
{shell['navHtml']}
<!-- @include:nav:end -->
{content['tocMobileHtml']}
{content['heroHtml']}
<div class=\"content-wrapper\">{content['methodologyHtml']}
{content['tocSidebarHtml']}
<div class=\"article-content\">
{content['photoGridHtml']}
{content['verdictHtml']}
{content['comparisonHtml']}
{''.join(content['deepDiveHtml'])}
{content['faqHtml']}
{content['ctaHtml']}
</div><!-- /article-content -->
</div><!-- /content-wrapper -->
<!-- @include:footer:start -->
{shell['footerHtml']}
<!-- @include:footer:end -->
{chr(10).join(shell['scripts'])}
</body>
</html>
"""


def validate_source(data: Dict) -> List[str]:
    errors = []
    for field in ["slug", "pageType", "status", "destinations", "seo", "schema", "shell", "content"]:
        if field not in data:
            errors.append(f"missing top-level field: {field}")
    if data.get("pageType") != "compare-leaf":
        errors.append("pageType must equal compare-leaf")
    if not re.fullmatch(r"[a-z0-9-]+", data.get("slug", "")):
        errors.append("slug must be kebab-case")
    content = data.get("content", {})
    if len(content.get("deepDiveHtml", [])) < 1:
        errors.append("deepDiveHtml must contain at least 1 section")
    if len(content.get("faqItems", [])) < 1:
        errors.append("faqItems must contain at least 1 item")
    if len(content.get("tocItems", [])) < 1:
        errors.append("tocItems must contain at least 1 item")
    seo = data.get("seo", {})
    for field in ["title", "metaDescription", "ogImage", "canonical"]:
        if not str(seo.get(field, "")).strip():
            errors.append(f"seo.{field} is required")
    shell = data.get("shell", {})
    for field in ["styleCss", "navHtml", "footerHtml"]:
        if not str(shell.get(field, "")).strip():
            errors.append(f"shell.{field} is required")
    return errors


def validate_rendered_output(data: Dict, html: str) -> List[str]:
    errors = []
    if data["seo"]["title"] not in html:
        errors.append("rendered HTML missing title")
    if 'class="verdict-box"' not in html:
        errors.append("rendered HTML missing verdict-box")
    if 'class="comparison-section"' not in html:
        errors.append("rendered HTML missing comparison-section")
    if html.count('class="deep-dive"') != len(data["content"]["deepDiveHtml"]):
        errors.append("deep-dive count mismatch")
    if html.count('class="faq-item"') != len(data["content"]["faqItems"]):
        errors.append("faq-item count mismatch")
    if 'application/ld+json' not in html:
        errors.append("rendered HTML missing JSON-LD")
    return errors


def iter_compare_html_files() -> List[Path]:
    return sorted([p / "index.html" for p in COMPARE_DIR.iterdir() if p.is_dir() and (p / "index.html").exists()])


def inventory_slugs() -> List[str]:
    inventory = load_json(INVENTORY_PATH)
    return [card["slug"] for card in inventory["cards"]]


def cmd_extract() -> int:
    count = 0
    for html_path in iter_compare_html_files():
        data = extract_page(html_path)
        out = DATA_DIR / f"{data['slug']}.json"
        write_json(out, data)
        count += 1
    print(f"Backfilled {count} compare leaf JSON files into {DATA_DIR.relative_to(REPO_ROOT)}")
    return 0


def cmd_build() -> int:
    count = 0
    for slug in inventory_slugs():
        data_path = DATA_DIR / f"{slug}.json"
        if not data_path.exists():
            raise SystemExit(f"Missing data file: {data_path}")
        data = load_json(data_path)
        errors = validate_source(data)
        if errors:
            raise SystemExit(f"Source validation failed for {slug}:\n" + "\n".join(errors))
        html = render_page(data)
        output_errors = validate_rendered_output(data, html)
        if output_errors:
            raise SystemExit(f"Output validation failed for {slug}:\n" + "\n".join(output_errors))
        write_text(COMPARE_DIR / slug / "index.html", html)
        count += 1
    print(f"Built {count} compare leaves from structured JSON")
    return 0


def cmd_validate() -> int:
    errors = []
    warnings = []
    slugs = inventory_slugs()
    for slug in slugs:
        data_path = DATA_DIR / f"{slug}.json"
        html_path = COMPARE_DIR / slug / "index.html"
        if not data_path.exists():
            errors.append(f"missing data file: compare-data/{slug}.json")
            continue
        if not html_path.exists():
            errors.append(f"missing leaf html: compare/{slug}/index.html")
            continue
        data = load_json(data_path)
        source_errors = validate_source(data)
        errors.extend(f"{slug}: {err}" for err in source_errors)
        rendered = render_page(data)
        output_errors = validate_rendered_output(data, rendered)
        errors.extend(f"{slug}: {err}" for err in output_errors)
        live = read_text(html_path)
        if live != rendered:
            warnings.append(f"{slug}: live HTML differs from generated output; run build")
    extra_json = sorted(p.stem for p in DATA_DIR.glob("*.json") if p.stem not in slugs)
    if extra_json:
        warnings.append("extra compare-data JSON not in inventory: " + ", ".join(extra_json))
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED with {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: compare leaf system valid ({len(slugs)} leaves, {len(warnings)} warning(s))")
    return 0


def main(argv: List[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"extract", "build", "validate"}:
        print("Usage: build_compare.py <extract|build|validate>")
        return 1
    cmd = argv[1]
    if cmd == "extract":
        return cmd_extract()
    if cmd == "build":
        return cmd_build()
    return cmd_validate()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
