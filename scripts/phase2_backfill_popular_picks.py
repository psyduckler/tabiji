#!/usr/bin/env python3
import argparse
import html
import json
import os
import re
import ssl
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
POPULAR_PICKS_DIR = REPO_ROOT / 'popular-picks'
SERPAPI_URL = 'https://serpapi.com/search.json'
REQUEST_DELAY = 0.2
MAPS_JS_SRC = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc&callback=initPopularPicksMaps'
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

SERPAPI_KEY = os.environ.get('SERPAPI_KEY') or os.environ.get('SERPAPI_API_KEY')
if not SERPAPI_KEY:
    try:
        SERPAPI_KEY = subprocess.check_output(
            ['security', 'find-generic-password', '-s', 'serpapi-key', '-w'],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        SERPAPI_KEY = None

if not SERPAPI_KEY:
    print('ERROR: No SerpAPI key found. Set SERPAPI_KEY / SERPAPI_API_KEY or add keychain item serpapi-key.', file=sys.stderr)
    sys.exit(1)


def search_place(query: str):
    params = {
        'engine': 'google_maps',
        'q': query,
        'api_key': SERPAPI_KEY,
        'hl': 'en',
    }
    url = SERPAPI_URL + '?' + '&'.join(f'{k}={quote_plus(str(v))}' for k, v in params.items())
    req = Request(url, method='GET', headers={'Accept': 'application/json'})
    try:
        with urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
            data = json.loads(resp.read())
        results = data.get('local_results', [])
        if results:
            return normalize_result(results[0])
        place = data.get('place_results')
        if place:
            return normalize_result(place)
        return None
    except HTTPError as e:
        body = e.read().decode() if e.fp else ''
        print(f'  SerpAPI error ({e.code}): {body[:200]}', file=sys.stderr)
        return None
    except Exception as e:
        print(f'  Request error: {e}', file=sys.stderr)
        return None


def normalize_result(result):
    if not result:
        return None
    place_id = result.get('place_id')
    maps_uri = f'https://www.google.com/maps/place/?q=place_id:{place_id}' if place_id else None
    gps = result.get('gps_coordinates') or {}
    operating = result.get('operating_hours') or {}
    weekday = []
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        val = operating.get(day)
        if val:
            weekday.append(f'{day.capitalize()}: {val}')
    open_state = (result.get('open_state') or '').lower()
    open_now = True if 'open' in open_state and 'closed' not in open_state else False if 'closed' in open_state else None
    return {
        'name': result.get('title'),
        'rating': result.get('rating'),
        'review_count': result.get('reviews'),
        'phone': result.get('phone'),
        'website': result.get('website'),
        'maps_uri': maps_uri,
        'address': result.get('address'),
        'lat': gps.get('latitude'),
        'lng': gps.get('longitude'),
        'weekday': weekday,
        'open_now': open_now,
    }


def extract_page_context(content: str):
    hero = ''
    if m := re.search(r'<div class="hero-badge">.*?—\s*(.*?)</div>', content, re.S):
        hero = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
    return {'page_context': hero}


def token_set(text: str):
    parts = re.findall(r"[a-z0-9']+", (text or '').lower())
    stop = {'the', 'and', 'bar', 'cafe', 'café', 'restaurant', 'tokyo', 'city', 'branch'}
    return [p for p in parts if p not in stop and len(p) > 1]


def is_reasonable_match(expected: str, actual: str):
    expected_tokens = token_set(expected)
    actual_tokens = set(token_set(actual))
    if not expected_tokens or not actual_tokens:
        return True
    overlap = sum(1 for t in expected_tokens if t in actual_tokens)
    needed = 1 if len(expected_tokens) <= 2 else 2
    return overlap >= needed


def extract_sections(content: str):
    sections = []
    pattern = re.compile(r'(<section class="restaurant-section" id="([^"]+)"[^>]*>)(.*?)(</section>)', re.S)
    for m in pattern.finditer(content):
        open_tag, section_id, inner, close_tag = m.groups()
        h2 = re.search(r'<h2>(.*?)</h2>', inner, re.S)
        name = html.unescape(re.sub(r'<[^>]+>', '', h2.group(1)).strip()) if h2 else None
        loc = ''
        loc_patterns = [
            r'<span class="detail-label">📍[^<]*</span><span>(.*?)</span>',
            r'<strong>Area:</strong>\s*(.*?)</p>',
            r'<strong>Neighborhood:</strong>\s*(.*?)</p>',
        ]
        for pat in loc_patterns:
            mm = re.search(pat, inner, re.S)
            if mm:
                loc = html.unescape(re.sub(r'<[^>]+>', '', mm.group(1)).strip())
                break
        existing_query = ''
        mm = re.search(r'data-map-query="([^"]+)"', open_tag)
        if mm:
            existing_query = html.unescape(mm.group(1))
        elif m2 := re.search(r'href="https://www\.google\.com/maps/search/([^"]+)"', inner):
            existing_query = html.unescape(m2.group(1).replace('+', ' '))
        rank = None
        if rm := re.search(r'<div class="restaurant-rank">#?(\d+)</div>', inner):
            rank = int(rm.group(1))
        elif rm := re.search(r'<span class="restaurant-number">(\d+)</span>', inner):
            rank = int(rm.group(1))
        sections.append({
            'match': m,
            'open_tag': open_tag,
            'inner': inner,
            'close_tag': close_tag,
            'section_id': section_id,
            'name': name,
            'location': loc,
            'existing_query': existing_query,
            'rank': rank,
        })
    return sections


def build_query(section, page_context=''):
    if section['existing_query']:
        return section['existing_query']
    parts = [section['name'] or '', section['location'] or '', page_context or '']
    return ' '.join(p for p in parts if p).strip()


def rating_html(place):
    if not place or not place.get('rating'):
        return ''
    count = place.get('review_count')
    count_str = f"{count:,}" if isinstance(count, int) else (str(count) if count else '?')
    return f'<span class="google-rating"><span class="star">★</span> {place["rating"]} · {count_str} reviews</span>'


def hours_html(place):
    rows = place.get('weekday') or []
    if not rows:
        return ''
    status = 'Open now' if place.get('open_now') is True else 'Closed now' if place.get('open_now') is False else 'Hours'
    cells = []
    for row in rows:
        if ': ' in row:
            d, t = row.split(': ', 1)
            cells.append(f'            <span>{html.escape(d[:3])}</span><span>{html.escape(t)}</span>')
    if not cells:
        return ''
    return '    <div class="shop-hours">\n        <details>\n            <summary>🕐 ' + status + '</summary>\n            <div class="hours-grid">\n' + '\n'.join(cells) + '\n            </div>\n        </details>\n    </div>\n'


def contact_html(place):
    parts = []
    if place.get('phone'):
        phone = place['phone']
        phone_href = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')
        parts.append(f'<span>📞 <a href="tel:{html.escape(phone_href)}">{html.escape(phone)}</a></span>')
    if place.get('website'):
        parts.append(f'<span>🌐 <a href="{html.escape(place["website"])}" target="_blank" rel="noopener">Website</a></span>')
    if not parts:
        return ''
    return '    <div class="shop-contact">\n        ' + '\n        '.join(parts) + '\n    </div>\n'


def map_query_value(section, place):
    return place.get('address') or section.get('existing_query') or f"{section['name']} {section.get('location','')}".strip()


def add_or_replace_attr(tag: str, attr: str, value: str):
    escaped = html.escape(value, quote=True)
    pattern = re.compile(rf'\s{re.escape(attr)}="[^"]*"')
    if pattern.search(tag):
        return pattern.sub(f' {attr}="{escaped}"', tag)
    return tag[:-1] + f' {attr}="{escaped}">'


def enrich_section(section, place):
    open_tag = section['open_tag']
    inner = section['inner']
    label = f"{section['rank']}. {section['name']}" if section.get('rank') else section['name']
    if place.get('maps_uri'):
        open_tag = add_or_replace_attr(open_tag, 'data-map-name', label)
        open_tag = add_or_replace_attr(open_tag, 'data-map-cta-url', place['maps_uri'])
    if place.get('lat') is not None:
        open_tag = add_or_replace_attr(open_tag, 'data-map-lat', str(place['lat']))
    if place.get('lng') is not None:
        open_tag = add_or_replace_attr(open_tag, 'data-map-lng', str(place['lng']))
    query_val = map_query_value(section, place)
    if query_val:
        open_tag = add_or_replace_attr(open_tag, 'data-map-query', query_val)

    if 'google-rating' not in inner:
        rh = rating_html(place)
        if rh:
            if 'class="cuisine-tags"' in inner:
                inner = re.sub(r'(<div class="cuisine-tags">.*?</div>)', rf'\1\n          {rh}', inner, count=1, flags=re.S)
            elif 'class="restaurant-header"' in inner:
                inner = re.sub(r'(<div class="restaurant-header">.*?</div>\s*</div>)', rf'\1\n        {rh}', inner, count=1, flags=re.S)

    if place.get('maps_uri'):
        if '📌 Google Maps' in inner:
            inner = re.sub(r'href="https://www\.google\.com/maps/search/[^"]+"', f'href="{html.escape(place["maps_uri"], quote=True)}"', inner, count=1)
        elif 'class="restaurant-details"' in inner:
            map_link = f'          <div class="detail-item"><a href="{html.escape(place["maps_uri"], quote=True)}" target="_blank" rel="noopener">📌 Google Maps →</a></div>'
            inner = re.sub(r'(<div class="restaurant-details">\s*<div class="detail-grid">)', rf'\1\n{map_link}', inner, count=1, flags=re.S)

    extras = ''
    if 'shop-hours' not in inner:
        extras += hours_html(place)
    if 'shop-contact' not in inner:
        extras += contact_html(place)
    if extras and 'class="restaurant-details"' in inner:
        inner = re.sub(r'(</div>\s*</div>\s*)(<div class="restaurant-body">)', rf'\1{extras}\2', inner, count=1, flags=re.S)

    return open_tag + inner + section['close_tag']


def build_map_panel(title, picks):
    first = picks[0]
    lis = '\n'.join([f'      <li><a href="#{html.escape(p["anchorId"])}">{html.escape(p["label"])}</a></li>' for p in picks[:12]])
    return f'''<div class="map-sidebar" data-map-panel="desktop">\n        <h2>{html.escape(title)}</h2>\n        <div class="map-active-pick" data-map-active-pick>{html.escape(first['label'])}</div>\n        <div class="popular-picks-map" data-map-canvas aria-label="{html.escape(title)}"></div>\n        <div class="map-legend">\n          <strong>Start with:</strong>\n          <ul>\n{lis}\n          </ul>\n          <p><a href="{html.escape(first['ctaUrl'], quote=True)}" target="_blank" rel="noopener" data-map-cta>Open in Google Maps →</a></p>\n        </div>\n      </div>'''


def build_map_script(title, default_cta, picks):
    config = {
        'enabled': True,
        'title': title,
        'ctaLabel': 'Open in Google Maps',
        'defaultCtaUrl': default_cta,
        'picks': picks,
    }
    return f'''  <script>\n    window.__POPULAR_PICKS_MAP__ = {json.dumps(config, ensure_ascii=False, separators=(',', ':'))};\n    (function () {{\n      var sections = Array.prototype.slice.call(document.querySelectorAll('.restaurant-section'));\n      var panels = Array.prototype.slice.call(document.querySelectorAll('[data-map-panel]'));\n      var mapConfig = window.__POPULAR_PICKS_MAP__ || {{}};\n      var mapState = {{ maps: [] }};\n      if (!sections.length || !panels.length) return;\n\n      function findPickBySection(section) {{\n        var id = section && section.id;\n        if (!id || !Array.isArray(mapConfig.picks)) return null;\n        return mapConfig.picks.find(function (pick) {{ return pick.anchorId === id; }}) || null;\n      }}\n\n      function syncPanels(section, pick) {{\n        panels.forEach(function (panel) {{\n          var title = panel.querySelector('[data-map-active-pick]');\n          var cta = panel.querySelector('[data-map-cta]');\n          if (title) title.textContent = (section && section.dataset.mapName) || (pick && pick.label) || '';\n          if (cta) cta.href = (pick && pick.ctaUrl) || (section && section.dataset.mapCtaUrl) || mapConfig.defaultCtaUrl || '#';\n        }});\n      }}\n\n      function highlightMarker(activePick) {{\n        mapState.maps.forEach(function (entry) {{\n          entry.markers.forEach(function (markerEntry) {{\n            var isActive = activePick && markerEntry.pick.anchorId === activePick.anchorId;\n            markerEntry.marker.setIcon({{ path: google.maps.SymbolPath.CIRCLE, scale: isActive ? 12 : 9, fillColor: isActive ? '#2D3A5C' : '#C4704B', fillOpacity: 1, strokeColor: '#FFFFFF', strokeWeight: 2 }});\n            markerEntry.marker.setZIndex(isActive ? 1000 : markerEntry.pick.rank);\n          }});\n          if (activePick) entry.map.panTo({{ lat: activePick.lat, lng: activePick.lng }});\n        }});\n      }}\n\n      function setActive(section) {{\n        if (!section) return;\n        var activePick = findPickBySection(section);\n        sections.forEach(function (item) {{ item.classList.toggle('active', item === section); }});\n        syncPanels(section, activePick);\n        if (window.google && google.maps && activePick) highlightMarker(activePick);\n      }}\n\n      function initMaps() {{\n        if (!window.google || !google.maps || !Array.isArray(mapConfig.picks) || !mapConfig.picks.length) return;\n        panels.forEach(function (panel) {{\n          var canvas = panel.querySelector('[data-map-canvas]');\n          if (!canvas) return;\n          var map = new google.maps.Map(canvas, {{ zoom: 13, center: {{ lat: mapConfig.picks[0].lat, lng: mapConfig.picks[0].lng }}, mapTypeControl: false, streetViewControl: false, fullscreenControl: false }});\n          var bounds = new google.maps.LatLngBounds();\n          var infoWindow = new google.maps.InfoWindow();\n          var markers = mapConfig.picks.map(function (pick) {{\n            var marker = new google.maps.Marker({{ position: {{ lat: pick.lat, lng: pick.lng }}, map: map, title: pick.label, icon: {{ path: google.maps.SymbolPath.CIRCLE, scale: 9, fillColor: '#C4704B', fillOpacity: 1, strokeColor: '#FFFFFF', strokeWeight: 2 }}, zIndex: pick.rank }});\n            bounds.extend(marker.getPosition());\n            marker.addListener('click', function () {{\n              infoWindow.setContent('<strong>' + pick.label.replace(/</g,'&lt;') + '</strong><br><a href="' + pick.ctaUrl + '" target="_blank" rel="noopener">Open in Google Maps</a>');\n              infoWindow.open(map, marker);\n              var target = document.getElementById(pick.anchorId);\n              if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});\n              setActive(target);\n            }});\n            return {{ pick: pick, marker: marker, infoWindow: infoWindow }};\n          }});\n          if (mapConfig.picks.length > 1) map.fitBounds(bounds, 48);\n          mapState.maps.push({{ panel: panel, map: map, markers: markers }});\n        }});\n        setTimeout(function () {{ setActive(sections[0]); }}, 0);\n      }}\n\n      window.initPopularPicksMaps = initMaps;\n      setActive(sections[0]);\n\n      if ('IntersectionObserver' in window) {{\n        var observer = new IntersectionObserver(function (entries) {{\n          var visible = entries.filter(function (entry) {{ return entry.isIntersecting; }}).sort(function (a, b) {{ return b.intersectionRatio - a.intersectionRatio; }});\n          if (visible[0]) setActive(visible[0].target);\n        }}, {{ rootMargin: '-25% 0px -45% 0px', threshold: [0.2, 0.45, 0.7] }});\n        sections.forEach(function (section) {{ observer.observe(section); }});\n      }}\n    }})();\n  </script>\n  <script async src="{MAPS_JS_SRC}"></script>'''


def maybe_replace_map_block(content, title, picks):
    if not picks:
        return content
    panel_html = build_map_panel(title, picks)
    content, n = re.subn(r'<div class="map-sidebar">.*?</div>\s*</div>\s*<div class="content">', panel_html + '\n\n      <div class="content">', content, count=1, flags=re.S)
    if n == 0:
        content = re.sub(r'<div class="map-sidebar">.*?</div>', panel_html, content, count=1, flags=re.S)
    return content


def inject_map_script(content, title, picks):
    if 'window.__POPULAR_PICKS_MAP__' in content:
        content = re.sub(r'<script>\s*window\.__POPULAR_PICKS_MAP__[\s\S]*?<script async src="https://maps\.googleapis\.com/maps/api/js\?key=[^"]+"></script>', build_map_script(title, picks[0]['ctaUrl'], picks), content, count=1, flags=re.S)
        return content
    script = build_map_script(title, picks[0]['ctaUrl'], picks)
    if '</body>' in content:
        return content.replace('</body>', script + '\n</body>', 1)
    return content + '\n' + script + '\n'


def update_h1_from_title(content):
    h1m = re.search(r'<h1>(.*?)</h1>', content, re.S)
    titlem = re.search(r'<title>(.*?)</title>', content, re.S)
    if not h1m or not titlem:
        return content, False
    h1 = re.sub(r'\s+', ' ', html.unescape(h1m.group(1))).strip()
    title = re.sub(r'\s+', ' ', html.unescape(titlem.group(1))).strip()
    clean_title = re.sub(r'\s*\|\s*tabiji\.ai\s*$', '', title)
    clean_title = re.sub(r'\s*\((20\d\d|2026)\)\s*$', '', clean_title).strip()
    broken = (
        h1.startswith('12 Best ') or h1.startswith('10 Best ') or h1.startswith('N Best ')
    ) and (len(clean_title) > 0)
    if not broken:
        return content, False
    return content[:h1m.start()] + f'<h1>{html.escape(clean_title)}</h1>' + content[h1m.end():], True


def rebuild_bad_pages(slugs):
    rebuilt = []
    failed = []
    for slug in slugs:
        api = REPO_ROOT / 'api' / 'v1' / 'picks' / f'{slug}.json'
        out = POPULAR_PICKS_DIR / slug / 'index.html'
        if not api.exists():
            failed.append((slug, 'missing api json'))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(['node', 'generators/popular-picks/build-page.js', str(api), str(out)], cwd=REPO_ROOT, check=True)
            rebuilt.append(slug)
        except subprocess.CalledProcessError as exc:
            failed.append((slug, f'build failed: {exc.returncode}'))
    return rebuilt, failed


def process_page(path: Path, dry_run=False):
    content = path.read_text(errors='ignore')
    page_ctx = extract_page_context(content)
    sections = extract_sections(content)
    if not sections:
        return {'slug': path.parent.name, 'processed': False, 'reason': 'no restaurant sections'}

    changed = False
    picks = []
    lookup = {}
    for idx, section in enumerate(sections, start=1):
        query = build_query(section, page_ctx.get('page_context', ''))
        if not query:
            continue
        print(f'  [{idx}/{len(sections)}] {section["name"]} :: {query}')
        place = search_place(query)
        time.sleep(REQUEST_DELAY)
        if place and not is_reasonable_match(section['name'], place.get('name') or ''):
            print(f"    rejected weak match: {place.get('name')}")
            place = None
        if not place or not place.get('maps_uri') or place.get('lat') is None or place.get('lng') is None:
            print('    not found / incomplete')
            continue
        lookup[section['section_id']] = place
        picks.append({
            'anchorId': section['section_id'],
            'rank': section.get('rank') or idx,
            'name': section['name'],
            'label': f"{section.get('rank') or idx}. {section['name']}",
            'lat': place['lat'],
            'lng': place['lng'],
            'ctaUrl': place['maps_uri'],
            'mapQuery': map_query_value(section, place),
        })
        print(f"    found {place.get('name')} ★ {place.get('rating')} ({place.get('review_count')})")

    if not picks:
        return {'slug': path.parent.name, 'processed': False, 'reason': 'no place matches'}

    for section in reversed(sections):
        place = lookup.get(section['section_id'])
        if not place:
            continue
        m = section['match']
        replacement = enrich_section(section, place)
        content = content[:m.start()] + replacement + content[m.end():]
        changed = True

    map_title = 'Map'
    if tm := re.search(r'<div class="map-sidebar">\s*<h2>(.*?)</h2>', content, re.S):
        map_title = html.unescape(re.sub(r'<[^>]+>', '', tm.group(1)).strip())
    content = maybe_replace_map_block(content, map_title, picks)
    content = inject_map_script(content, map_title, picks)
    content, h1_changed = update_h1_from_title(content)
    changed = changed or h1_changed

    if changed and not dry_run:
        path.write_text(content)
    return {'slug': path.parent.name, 'processed': changed, 'matches': len(picks), 'h1_changed': h1_changed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    bad_pages = []
    for idx in POPULAR_PICKS_DIR.glob('*/index.html'):
        text = idx.read_text(errors='ignore')
        if len(text.strip()) < 100 or '</body>' not in text or '</html>' not in text:
            bad_pages.append(idx.parent.name)
    if bad_pages:
        print('Rebuilding malformed pages:', ', '.join(bad_pages))
        if not args.dry_run:
            rebuilt, failed = rebuild_bad_pages(bad_pages)
            if rebuilt:
                print('Rebuilt:', ', '.join(rebuilt))
            if failed:
                print('Rebuild failed:', '; '.join(f'{slug} ({err})' for slug, err in failed))

    pages = sorted(POPULAR_PICKS_DIR.glob('*/index.html'))
    selected = []
    for path in pages:
        if args.slug and path.parent.name != args.slug:
            continue
        text = path.read_text(errors='ignore')
        if 'restaurant-section' not in text:
            continue
        if 'data-map-cta-url=' in text and 'window.__POPULAR_PICKS_MAP__' in text and 'google-rating' in text:
            continue
        selected.append(path)
    if args.limit:
        selected = selected[:args.limit]

    print(f'Processing {len(selected)} pages')
    results = []
    for path in selected:
        print(f'\n== {path.parent.name} ==')
        results.append(process_page(path, dry_run=args.dry_run))

    print('\nSummary:')
    for r in results[:50]:
        print(r)

if __name__ == '__main__':
    main()
