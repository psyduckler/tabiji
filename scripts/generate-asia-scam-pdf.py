#!/usr/bin/env python3
"""
Generate a professional PDF of tourist scams for Asian cities.
Data sourced from tabiji.ai/scams/ HTML pages.
"""

import os
import re
import json
from html import unescape
from collections import defaultdict

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable

# ── Config ──────────────────────────────────────────────────────────
SCAMS_DIR = "/Users/psy/.openclaw/workspace/tabiji/scams"
OUTPUT_PATH = "/Users/psy/.openclaw/workspace/tabiji/pdfs/scams-asia.pdf"

# Asian country codes
ASIAN_CC = {
    'th', 'vn', 'kh', 'la', 'mm',
    'jp', 'kr',
    'cn', 'hk', 'mo', 'tw',
    'in', 'np', 'lk', 'bd', 'pk', 'mv',
    'my', 'sg', 'id', 'ph', 'bn', 'tl',
    'ae', 'sa', 'qa', 'kw', 'bh', 'om',
    'il', 'jo', 'lb', 'sy', 'iq', 'ps',
    'tr', 'ge', 'am', 'az', 'uz', 'kz', 'kg', 'tj', 'tm',
    'mn',
}

COUNTRY_NAMES = {
    'th': 'Thailand', 'vn': 'Vietnam', 'kh': 'Cambodia', 'la': 'Laos', 'mm': 'Myanmar',
    'jp': 'Japan', 'kr': 'South Korea',
    'cn': 'China', 'hk': 'Hong Kong', 'mo': 'Macau', 'tw': 'Taiwan',
    'in': 'India', 'np': 'Nepal', 'lk': 'Sri Lanka', 'bd': 'Bangladesh', 'pk': 'Pakistan', 'mv': 'Maldives',
    'my': 'Malaysia', 'sg': 'Singapore', 'id': 'Indonesia', 'ph': 'Philippines', 'bn': 'Brunei', 'tl': 'East Timor',
    'ae': 'United Arab Emirates', 'sa': 'Saudi Arabia', 'qa': 'Qatar', 'kw': 'Kuwait', 'bh': 'Bahrain', 'om': 'Oman',
    'il': 'Israel', 'jo': 'Jordan', 'lb': 'Lebanon', 'sy': 'Syria', 'iq': 'Iraq', 'ps': 'Palestine',
    'tr': 'Turkey', 'ge': 'Georgia', 'am': 'Armenia', 'az': 'Azerbaijan', 'uz': 'Uzbekistan',
    'kz': 'Kazakhstan', 'kg': 'Kyrgyzstan', 'tj': 'Tajikistan', 'tm': 'Turkmenistan',
    'mn': 'Mongolia',
}

# Region groupings for ordering
REGIONS = {
    'Southeast Asia': ['th', 'vn', 'kh', 'la', 'mm', 'my', 'sg', 'id', 'ph', 'bn', 'tl'],
    'East Asia': ['jp', 'kr', 'cn', 'hk', 'mo', 'tw', 'mn'],
    'South Asia': ['in', 'np', 'lk', 'bd', 'pk', 'mv'],
    'Middle East': ['ae', 'sa', 'qa', 'kw', 'bh', 'om', 'il', 'jo', 'lb', 'sy', 'iq', 'ps', 'tr', 'ge', 'am', 'az'],
    'Central Asia': ['uz', 'kz', 'kg', 'tj', 'tm'],
}

# ── Colors ──────────────────────────────────────────────────────────
BRAND_DARK = HexColor('#1a1a2e')
BRAND_BLUE = HexColor('#16213e')
BRAND_ACCENT = HexColor('#e94560')
BRAND_ORANGE = HexColor('#f5a623')
BRAND_LIGHT = HexColor('#f8f9fa')
SEVERITY_HIGH = HexColor('#dc3545')
SEVERITY_MED = HexColor('#fd7e14')
SEVERITY_LOW = HexColor('#28a745')
TEXT_DARK = HexColor('#2c2c2c')
TEXT_MUTED = HexColor('#6c757d')
BG_LIGHT = HexColor('#f0f4f8')
BG_CARD = HexColor('#ffffff')
BORDER_LIGHT = HexColor('#dee2e6')


# ── HTML Parsing ────────────────────────────────────────────────────

def strip_html(text):
    """Remove HTML tags and decode entities."""
    if not text:
        return ''
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_country_code(content):
    """Extract country code from JSON-LD in HTML."""
    ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not ld_match:
        return None
    try:
        ld = json.loads(ld_match.group(1))
        for item in ld.get('@graph', []):
            if item.get('@type') == 'Place':
                addr = item.get('address', {})
                return addr.get('addressCountry', '').lower()
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def extract_city_name(content):
    """Extract city name from JSON-LD."""
    ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not ld_match:
        return None
    try:
        ld = json.loads(ld_match.group(1))
        for item in ld.get('@graph', []):
            if item.get('@type') == 'Place':
                return item.get('name', '')
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def extract_scams(content):
    """Parse scam cards from HTML content."""
    scams = []

    # Find all scam cards
    scam_starts = list(re.finditer(r'<div class="scam-card"', content))
    if not scam_starts:
        return scams

    for i, m in enumerate(scam_starts):
        start = m.start()
        end = scam_starts[i + 1].start() if i + 1 < len(scam_starts) else len(content)
        block = content[start:end]

        scam = {}

        # Title
        title_m = re.search(r'class="scam-title"[^>]*>(.*?)</div>', block, re.DOTALL)
        scam['title'] = strip_html(title_m.group(1)) if title_m else ''

        # Number
        num_m = re.search(r'class="scam-number"[^>]*>(.*?)</span>', block, re.DOTALL)
        scam['number'] = strip_html(num_m.group(1)) if num_m else ''

        # Location
        loc_m = re.search(r'class="scam-location"[^>]*>(.*?)</span>', block, re.DOTALL)
        scam['location'] = strip_html(loc_m.group(1)) if loc_m else ''

        # TLDR
        tldr_m = re.search(r'<p class="scam-tldr"[^>]*>(.*?)</p>', block, re.DOTALL)
        if not tldr_m:
            tldr_m = re.search(r'class="scam-tldr"[^>]*>(.*?)</div>', block, re.DOTALL)
        scam['tldr'] = strip_html(tldr_m.group(1)) if tldr_m else ''

        # Story body
        story_m = re.search(r'<p class="scam-story-body"[^>]*>(.*?)</p>', block, re.DOTALL)
        if not story_m:
            story_m = re.search(r'class="scam-story-body"[^>]*>(.*?)</div>', block, re.DOTALL)
        scam['story'] = strip_html(story_m.group(1)) if story_m else ''

        # Severity
        sev_m = re.search(r'(\d+)\s+(High Risk|Medium|Low)', block)
        scam['severity_count'] = sev_m.group(1) if sev_m else ''
        scam['severity'] = sev_m.group(2) if sev_m else ''

        # Avoidance tips
        avoid_block = re.search(r'<h4>How to Avoid</h4>(.*?)</div>\s*</div>', block, re.DOTALL)
        if avoid_block:
            tips = re.findall(r'<li[^>]*>(.*?)</li>', avoid_block.group(1), re.DOTALL)
            scam['avoidance'] = [strip_html(t) for t in tips]
        else:
            # Try alternate: just grab all <li> after "How to Avoid"
            avoid_section = re.search(r'How to Avoid(.*?)(?:</div>\s*</div>\s*</div>|Red Flags)', block, re.DOTALL)
            if avoid_section:
                tips = re.findall(r'<li[^>]*>(.*?)</li>', avoid_section.group(1), re.DOTALL)
                scam['avoidance'] = [strip_html(t) for t in tips]
            else:
                scam['avoidance'] = []

        # Red flags
        rf_block = re.search(r'<h4>Red Flags</h4>(.*?)</div>\s*</div>', block, re.DOTALL)
        if rf_block:
            flags = re.findall(r'<li[^>]*>(.*?)</li>', rf_block.group(1), re.DOTALL)
            scam['red_flags'] = [strip_html(f) for f in flags]
        else:
            scam['red_flags'] = []

        if scam['title']:
            scams.append(scam)

    return scams


def load_all_asian_scams():
    """Load all scam data for Asian cities."""
    cities = []

    for slug in sorted(os.listdir(SCAMS_DIR)):
        html_path = os.path.join(SCAMS_DIR, slug, 'index.html')
        if not os.path.isfile(html_path):
            continue

        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cc = extract_country_code(content)
        if cc not in ASIAN_CC:
            continue

        city_name = extract_city_name(content) or slug.replace('-', ' ').title()
        scams = extract_scams(content)

        cities.append({
            'slug': slug,
            'city': city_name,
            'country_code': cc,
            'country': COUNTRY_NAMES.get(cc, cc.upper()),
            'scams': scams,
            'scam_count': len(scams),
        })

    return cities


# ── PDF Generation ──────────────────────────────────────────────────

class ColorBar(Flowable):
    """A colored bar."""
    def __init__(self, width, height, color):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


def build_styles():
    """Create paragraph styles for the PDF."""
    styles = {}

    styles['cover_title'] = ParagraphStyle(
        'cover_title',
        fontName='Helvetica-Bold',
        fontSize=36,
        leading=44,
        textColor=white,
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    styles['cover_subtitle'] = ParagraphStyle(
        'cover_subtitle',
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=HexColor('#adb5bd'),
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    styles['cover_stats'] = ParagraphStyle(
        'cover_stats',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=20,
        textColor=BRAND_ORANGE,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    styles['region_title'] = ParagraphStyle(
        'region_title',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=28,
        textColor=BRAND_ACCENT,
        spaceBefore=0,
        spaceAfter=16,
    )

    styles['country_title'] = ParagraphStyle(
        'country_title',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        textColor=BRAND_DARK,
        spaceBefore=16,
        spaceAfter=8,
    )

    styles['city_title'] = ParagraphStyle(
        'city_title',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=BRAND_BLUE,
        spaceBefore=14,
        spaceAfter=4,
    )

    styles['city_meta'] = ParagraphStyle(
        'city_meta',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_MUTED,
        spaceAfter=8,
    )

    styles['scam_title'] = ParagraphStyle(
        'scam_title',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=TEXT_DARK,
        spaceBefore=10,
        spaceAfter=4,
    )

    styles['scam_body'] = ParagraphStyle(
        'scam_body',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    styles['avoidance_title'] = ParagraphStyle(
        'avoidance_title',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=HexColor('#155724'),
        spaceBefore=4,
        spaceAfter=3,
    )

    styles['avoidance_item'] = ParagraphStyle(
        'avoidance_item',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=HexColor('#155724'),
        leftIndent=15,
        spaceAfter=2,
    )

    styles['red_flag_title'] = ParagraphStyle(
        'red_flag_title',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=HexColor('#721c24'),
        spaceBefore=4,
        spaceAfter=3,
    )

    styles['red_flag_item'] = ParagraphStyle(
        'red_flag_item',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=HexColor('#721c24'),
        leftIndent=15,
        spaceAfter=2,
    )

    styles['location'] = ParagraphStyle(
        'location',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=4,
    )

    styles['toc_region'] = ParagraphStyle(
        'toc_region',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=BRAND_ACCENT,
        spaceBefore=12,
        spaceAfter=4,
    )

    styles['toc_country'] = ParagraphStyle(
        'toc_country',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=BRAND_DARK,
        spaceBefore=6,
        spaceAfter=2,
        leftIndent=10,
    )

    styles['toc_city'] = ParagraphStyle(
        'toc_city',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=1,
        leftIndent=25,
    )

    styles['footer'] = ParagraphStyle(
        'footer',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=TEXT_MUTED,
        alignment=TA_CENTER,
    )

    styles['toc_title'] = ParagraphStyle(
        'toc_title',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=BRAND_DARK,
        spaceBefore=0,
        spaceAfter=20,
        alignment=TA_CENTER,
    )

    styles['emergency_title'] = ParagraphStyle(
        'emergency_title',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=SEVERITY_HIGH,
        spaceBefore=8,
        spaceAfter=4,
    )

    styles['emergency_body'] = ParagraphStyle(
        'emergency_body',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=4,
    )

    return styles


def severity_color(severity):
    """Return color for severity level."""
    s = (severity or '').lower()
    if 'high' in s:
        return SEVERITY_HIGH
    elif 'medium' in s or 'med' in s:
        return SEVERITY_MED
    return SEVERITY_LOW


def severity_badge(severity, count=''):
    """Create a severity badge paragraph."""
    color = severity_color(severity)
    label = severity or 'Unknown'
    if count:
        label = f"{count} {label}"
    hex_color = f"#{color.hexval()[2:]}"
    return Paragraph(
        f'<font color="{hex_color}">● <b>{label}</b></font>',
        ParagraphStyle('badge', fontName='Helvetica-Bold', fontSize=9, leading=12)
    )


def generate_pdf(cities):
    """Generate the PDF document."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = build_styles()
    story = []
    usable_width = doc.width

    # ── Cover Page ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(ColorBar(usable_width, 4, BRAND_ACCENT))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("🛡️ TOURIST SCAMS", styles['cover_title']))
    story.append(Paragraph("& SAFETY GUIDE", styles['cover_title']))
    story.append(Spacer(1, 0.15 * inch))
    story.append(ColorBar(usable_width, 2, BRAND_ORANGE))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("A S I A", ParagraphStyle(
        'asia_label', fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=BRAND_ORANGE, alignment=TA_CENTER, spaceAfter=20,
    )))

    total_scams = sum(c['scam_count'] for c in cities)
    total_countries = len(set(c['country_code'] for c in cities))

    stats_data = [
        [f"{len(cities)} Cities", f"{total_scams} Scams", f"{total_countries} Countries"],
    ]
    stats_table = Table(stats_data, colWidths=[usable_width / 3] * 3)
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('TEXTCOLOR', (0, 0), (-1, -1), BRAND_ORANGE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(stats_table)

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        "Real stories from Reddit travelers. Every scam documented, every trick explained.",
        styles['cover_subtitle']
    ))
    story.append(Paragraph(
        "Know before you go — so you're never caught off-guard.",
        styles['cover_subtitle']
    ))
    story.append(Spacer(1, 0.6 * inch))
    story.append(ColorBar(usable_width, 2, BRAND_ACCENT))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("tabiji.ai", ParagraphStyle(
        'brand', fontName='Helvetica-Bold', fontSize=12, leading=14,
        textColor=HexColor('#adb5bd'), alignment=TA_CENTER,
    )))
    story.append(Paragraph("Updated April 2026", ParagraphStyle(
        'date', fontName='Helvetica', fontSize=10, leading=12,
        textColor=HexColor('#6c757d'), alignment=TA_CENTER,
    )))
    story.append(PageBreak())

    # ── Table of Contents ──
    story.append(Paragraph("Table of Contents", styles['toc_title']))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_LIGHT))
    story.append(Spacer(1, 12))

    # Group by region, then country
    by_region = defaultdict(lambda: defaultdict(list))
    for city in cities:
        cc = city['country_code']
        placed = False
        for region, codes in REGIONS.items():
            if cc in codes:
                by_region[region][city['country']].append(city)
                placed = True
                break
        if not placed:
            by_region['Other'][city['country']].append(city)

    for region_name in ['Southeast Asia', 'East Asia', 'South Asia', 'Middle East', 'Central Asia', 'Other']:
        countries = by_region.get(region_name, {})
        if not countries:
            continue
        story.append(Paragraph(f"{region_name}", styles['toc_region']))
        for country_name in sorted(countries.keys()):
            story.append(Paragraph(f"{country_name}", styles['toc_country']))
            for city in sorted(countries[country_name], key=lambda x: x['city']):
                story.append(Paragraph(
                    f"• {city['city']} — {city['scam_count']} scams",
                    styles['toc_city']
                ))

    story.append(PageBreak())

    # ── Content Pages ──
    for region_name in ['Southeast Asia', 'East Asia', 'South Asia', 'Middle East', 'Central Asia', 'Other']:
        countries = by_region.get(region_name, {})
        if not countries:
            continue

        # Region page
        story.append(Spacer(1, 0.3 * inch))
        story.append(ColorBar(usable_width, 3, BRAND_ACCENT))
        story.append(Spacer(1, 0.15 * inch))
        story.append(Paragraph(region_name, styles['region_title']))
        region_cities = sum(len(v) for v in countries.values())
        region_scams = sum(sum(c['scam_count'] for c in cl) for cl in countries.values())
        story.append(Paragraph(
            f"{region_cities} cities • {region_scams} scams • {len(countries)} countries",
            ParagraphStyle('region_meta', fontName='Helvetica', fontSize=11, leading=14,
                           textColor=TEXT_MUTED, spaceAfter=12)
        ))
        story.append(HRFlowable(width="100%", thickness=1, color=BORDER_LIGHT))
        story.append(Spacer(1, 8))

        for country_name in sorted(countries.keys()):
            country_cities = countries[country_name]

            # Country header
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"📍 {country_name}", styles['country_title']))
            story.append(HRFlowable(width="40%", thickness=1, color=BRAND_ACCENT))
            story.append(Spacer(1, 4))

            for city in sorted(country_cities, key=lambda x: x['city']):
                if not city['scams']:
                    continue

                # City header
                city_header = f"🏙️ {city['city']}"
                story.append(Paragraph(city_header, styles['city_title']))
                story.append(Paragraph(
                    f"{city['scam_count']} scams documented • {city['country']}",
                    styles['city_meta']
                ))

                # Scam cards
                for scam in city['scams']:
                    # Build scam block
                    scam_elements = []

                    # Title + severity
                    title_text = f"<b>{scam['title']}</b>"
                    if scam['severity']:
                        sev_color_hex = f"#{severity_color(scam['severity']).hexval()[2:]}"
                        title_text += f'  <font color="{sev_color_hex}" size="9">● {scam["severity"]}</font>'
                    scam_elements.append(Paragraph(title_text, styles['scam_title']))

                    # Location
                    if scam.get('location'):
                        scam_elements.append(Paragraph(
                            f"📍 {scam['location']}",
                            styles['location']
                        ))

                    # Description
                    desc = scam.get('story') or scam.get('tldr') or ''
                    if desc:
                        # Truncate very long descriptions for PDF readability
                        if len(desc) > 600:
                            desc = desc[:597] + '...'
                        scam_elements.append(Paragraph(desc, styles['scam_body']))

                    # Red flags
                    if scam.get('red_flags'):
                        scam_elements.append(Paragraph("🚩 Red Flags", styles['red_flag_title']))
                        for flag in scam['red_flags'][:5]:
                            flag_text = flag[:200] + '...' if len(flag) > 200 else flag
                            scam_elements.append(Paragraph(f"• {flag_text}", styles['red_flag_item']))

                    # Avoidance tips
                    if scam.get('avoidance'):
                        scam_elements.append(Paragraph("✅ How to Avoid", styles['avoidance_title']))
                        for tip in scam['avoidance'][:5]:
                            tip_text = tip[:200] + '...' if len(tip) > 200 else tip
                            scam_elements.append(Paragraph(f"• {tip_text}", styles['avoidance_item']))

                    # Separator
                    scam_elements.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_LIGHT))

                    # Add as a group (keep together for short ones)
                    for elem in scam_elements:
                        story.append(elem)

                story.append(Spacer(1, 8))

    # ── Final page ──
    story.append(PageBreak())
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("🛡️ Stay Safe Out There", ParagraphStyle(
        'final_title', fontName='Helvetica-Bold', fontSize=24, leading=30,
        textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=20,
    )))
    story.append(HRFlowable(width="60%", thickness=2, color=BRAND_ACCENT))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "This guide covers the most common tourist scams across Asia, "
        "sourced from real travelers on Reddit and verified by the tabiji.ai team.",
        ParagraphStyle('final_body', fontName='Helvetica', fontSize=12, leading=16,
                       textColor=TEXT_DARK, alignment=TA_CENTER, spaceAfter=16)
    ))
    story.append(Paragraph(
        "For the latest updates, visit <b>tabiji.ai/scams/</b>",
        ParagraphStyle('final_link', fontName='Helvetica', fontSize=12, leading=16,
                       textColor=BRAND_ACCENT, alignment=TA_CENTER, spaceAfter=30)
    ))
    story.append(ColorBar(usable_width, 2, BRAND_ACCENT))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("© 2026 tabiji.ai — All rights reserved", styles['footer']))
    story.append(Paragraph(
        "This guide is for informational purposes only. Always exercise common sense and due diligence while traveling.",
        ParagraphStyle('disclaimer', fontName='Helvetica', fontSize=8, leading=10,
                       textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=4)
    ))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF generated: {OUTPUT_PATH}")
    print(f"   Cities: {len(cities)} | Scams: {total_scams} | Countries: {total_countries}")


# ── Main ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("🔍 Loading Asian scam data...")
    cities = load_all_asian_scams()
    print(f"   Found {len(cities)} Asian cities")

    # Sort by region, then country, then city
    def sort_key(c):
        cc = c['country_code']
        for i, (region, codes) in enumerate(REGIONS.items()):
            if cc in codes:
                return (i, c['country'], c['city'])
        return (99, c['country'], c['city'])

    cities.sort(key=sort_key)
    generate_pdf(cities)
