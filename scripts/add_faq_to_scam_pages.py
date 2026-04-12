#!/usr/bin/env python3
"""
Add FAQ sections and FAQPage JSON-LD schema to scam pages that are missing them.

- Finds all scam pages under /scams/*/index.html that lack "faq-section"
- Extracts city name, scam titles, and country from each page
- Generates 5 city-specific FAQs using templates and actual scam data
- Injects FAQ HTML between the emergency action-section and the related-section
- Adds FAQPage JSON-LD schema to the existing ld+json block
- Also adds ".faq-a" to the speakable cssSelector array
"""

import os
import re
import json
import glob
import html

SCAMS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scams")

# Transport questions by region/context
TRANSPORT_QUESTIONS = {
    # Asia
    "bangkok": ("Are tuk-tuks safe in {city}?", "Tuk-tuks in {city} are a common way to get around but are frequently used in tourist scams. Drivers may quote inflated fares, take you to commission-based shops, or claim attractions are closed. Always agree on a fare before getting in, use Grab or Bolt apps for fixed pricing, and avoid drivers who approach you near major tourist sites."),
    "bali": ("Are taxis safe in {city}?", "Licensed taxis with meters (look for Bluebird Group) are generally safe in Bali. Avoid unmarked taxis and drivers who refuse to use the meter. Ride-hailing apps like Grab and Gojek offer transparent pricing and are widely available. Be cautious of drivers near tourist areas who quote inflated fixed prices."),
    "tokyo": ("Is public transport safe in {city}?", "Public transport in {city} is extremely safe and reliable. The main risk for tourists is not scams but confusion with the complex rail network. Buy a Suica or Pasmo IC card for easy travel. Be cautious of unlicensed taxi services near nightlife districts and always use official taxi stands or ride-hailing apps."),
    "delhi": ("Are auto-rickshaws safe in {city}?", "Auto-rickshaws in {city} are a common way to get around but drivers frequently refuse to use meters and quote inflated prices. Use Uber or Ola apps for transparent pricing. If taking an auto-rickshaw, insist on the meter or negotiate the fare firmly before getting in. Avoid drivers who approach you at train stations or airports."),
    "cairo": ("Are taxis safe in {city}?", "Licensed taxis in {city} can be safe but many drivers refuse to use meters or quote inflated prices to tourists. Use ride-hailing apps like Uber or Careem for transparent, fixed pricing. If taking a street taxi, agree on the fare before getting in and have small bills ready to avoid change scams."),
    "rome": ("Is public transport safe in {city}?", "Public transport in {city} is generally safe but pickpocketing is common on crowded buses and metro lines, especially Line A between Termini and the Vatican. Keep valuables in front pockets or a money belt. Buy tickets from official machines or tabacchi shops and validate them to avoid fines from inspectors."),
    "paris": ("Is the Paris Metro safe for tourists?", "The Paris Metro is generally safe during daytime hours. The main risks are pickpockets, especially on Lines 1, 4, and the RER B to the airport. Keep bags zipped and in front of you. Avoid empty carriages late at night. Use official ticket machines and watch for fake petition signers near station entrances."),
    "barcelona": ("Is the Barcelona Metro safe?", "The Barcelona Metro is efficient and mostly safe, but it is one of Europe's top pickpocket hotspots. Lines L1 and L3 near tourist stops like Las Ramblas and Sagrada Familia are highest risk. Keep your phone in a front pocket, use a crossbody bag, and stay alert during boarding when crowds press together."),
    "london": ("Is the London Underground safe?", "The London Underground is one of the safest metro systems in the world. The main risk is opportunistic pickpocketing on crowded platforms during rush hour. Use contactless payment or Oyster cards for travel. Be cautious of unofficial minicab drivers outside stations late at night and always use licensed black cabs or ride-hailing apps."),
}

# Regional safe areas info
SAFE_AREAS_DATA = {
    # These are fallback templates; the script generates contextual answers
}

def extract_page_data(filepath):
    """Extract city name, country, scam titles, slug, and country code from a scam page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract city name from h1
    h1_match = re.search(r'<h1>\d+ Tourist Scams in (.+?)</h1>', content)
    city = h1_match.group(1).strip() if h1_match else None

    # Extract country from hero-meta
    country_match = re.search(r'<span>...\s*(.+?),\s*(.+?)</span>', content)
    country = country_match.group(2).strip() if country_match else None

    # Extract scam titles
    scam_titles = re.findall(r'<div class="scam-title">(.+?)</div>', content)

    # Extract slug from filepath
    slug = os.path.basename(os.path.dirname(filepath))

    # Extract country code from JSON-LD
    cc_match = re.search(r'"addressCountry":\s*"(\w+)"', content)
    country_code = cc_match.group(1) if cc_match else ""

    # Extract number of scams from h1
    num_match = re.search(r'<h1>(\d+) Tourist Scams', content)
    num_scams = int(num_match.group(1)) if num_match else len(scam_titles)

    return {
        'city': city,
        'country': country,
        'scam_titles': scam_titles,
        'slug': slug,
        'country_code': country_code,
        'num_scams': num_scams,
        'content': content,
        'filepath': filepath,
    }


def get_transport_question(city, country, scam_titles):
    """Generate a transport safety question appropriate for the city/region."""
    city_lower = city.lower()
    slug_key = city_lower.replace(' ', '-')

    # Check direct city match first
    if slug_key in TRANSPORT_QUESTIONS:
        q, a = TRANSPORT_QUESTIONS[slug_key]
        return q.format(city=city), a.format(city=city)

    # Scan scam titles for transport-related keywords
    scam_str = ' '.join(scam_titles).lower()
    has_taxi = any(w in scam_str for w in ['taxi', 'cab', 'uber', 'ride', 'driver'])
    has_tuk = any(w in scam_str for w in ['tuk-tuk', 'tuktuk', 'rickshaw', 'auto-rickshaw'])
    has_metro = any(w in scam_str for w in ['metro', 'subway', 'underground', 'train', 'bus', 'transport'])

    if country and country.lower() in ['thailand', 'cambodia', 'laos', 'vietnam', 'indonesia', 'philippines', 'myanmar', 'sri lanka', 'india', 'nepal', 'bangladesh']:
        if has_tuk or has_taxi:
            return (
                f"Are taxis and ride services safe in {city}?",
                f"Licensed, metered taxis in {city} are generally safe, though some drivers target tourists with inflated fares or rigged meters. Use ride-hailing apps like Grab or local equivalents for transparent, fixed pricing. Avoid drivers who approach you at tourist sites or transportation hubs, and always confirm the fare or ensure the meter is running before departure."
            )
        return (
            f"Is local transport safe in {city}?",
            f"Public transport in {city} is generally functional but tourists should stay alert for common issues like taxi meter scams, inflated fares, and unlicensed drivers. Use ride-hailing apps when available for transparent pricing. If taking local transport, confirm the fare beforehand and keep valuables secure, especially on crowded routes."
        )

    if country and country.lower() in ['france', 'italy', 'spain', 'germany', 'netherlands', 'belgium', 'portugal', 'greece', 'czech republic', 'czechia', 'hungary', 'poland', 'austria', 'croatia', 'romania', 'turkey', 'united kingdom', 'ireland', 'scotland', 'england', 'denmark', 'sweden', 'norway', 'finland', 'switzerland']:
        if has_metro:
            return (
                f"Is public transport safe in {city}?",
                f"Public transport in {city} is well-connected and generally safe. The main risk for tourists is pickpocketing on crowded buses and metro lines near popular stops. Keep bags zipped and close to your body, especially during rush hours. Use official ticket machines and be cautious of people creating distractions near turnstiles."
            )
        return (
            f"Are taxis safe in {city}?",
            f"Licensed taxis in {city} are generally safe and regulated. Always ensure the meter is running or agree on a fare before departure. Use official taxi ranks rather than accepting rides from drivers who approach you. Ride-hailing apps provide transparent pricing and are a good alternative to street hails."
        )

    if country and country.lower() in ['mexico', 'colombia', 'brazil', 'peru', 'argentina', 'chile', 'costa rica', 'ecuador', 'guatemala', 'panama', 'dominican republic', 'cuba', 'puerto rico', 'uruguay', 'bolivia', 'honduras', 'el salvador', 'nicaragua', 'belize', 'jamaica', 'trinidad and tobago']:
        return (
            f"Are taxis safe in {city}?",
            f"Use authorized taxi services or ride-hailing apps (Uber, DiDi, Cabify, InDrive) in {city} rather than hailing cabs on the street. Ask your hotel to call a registered radio taxi if apps are not available. Avoid unmarked vehicles, especially at night, and always share your trip details with someone you trust."
        )

    if country and country.lower() in ['morocco', 'egypt', 'kenya', 'tanzania', 'south africa', 'ethiopia', 'ghana', 'senegal', 'tunisia', 'nigeria', 'rwanda', 'uganda', 'zimbabwe', 'namibia', 'botswana', 'mozambique', 'madagascar']:
        return (
            f"Are taxis safe in {city}?",
            f"Taxis in {city} vary in safety and reliability. Use reputable taxi companies recommended by your hotel or ride-hailing apps where available. Always agree on the fare before departure, as many taxis do not use meters. Avoid accepting rides from unlicensed vehicles, especially late at night or near tourist sites."
        )

    # Default
    return (
        f"Are taxis safe in {city}?",
        f"Licensed taxis in {city} are generally safe when you take basic precautions. Use ride-hailing apps for transparent pricing when available. If taking a street taxi, ensure the meter is running or negotiate the fare before getting in. Avoid unlicensed vehicles and drivers who approach you aggressively at tourist sites or transport hubs."
    )


def generate_safe_areas_answer(city, country):
    """Generate an answer about safe areas to stay in."""
    return (
        f"What are the safest areas for tourists in {city}?",
        f"Stick to well-reviewed tourist neighborhoods and book accommodation with strong recent reviews on major platforms. "
        f"In {city}, areas with established tourist infrastructure, good lighting, and proximity to main attractions tend to be safest. "
        f"Ask your hotel or guesthouse staff for current local advice on areas to avoid, especially at night. "
        f"Check recent traveler forums for up-to-date safety information specific to the neighborhoods you plan to visit."
    )


def generate_scammed_answer(city, country):
    """Generate an answer about what to do if scammed."""
    return (
        f"What should I do if I get scammed in {city}?",
        f"File a police report immediately at the nearest station — you will need this for any insurance claims. "
        f"Cancel compromised credit or debit cards by calling your bank's 24/7 emergency line. "
        f"Contact your country's embassy or consulate in {city} if your passport was stolen. "
        f"Document everything with photos, receipts, and written notes while details are fresh. "
        f"Report the scam on travel forums like Reddit to warn other travelers."
    )


def generate_faqs(data):
    """Generate 5 FAQ Q&A pairs for a scam page."""
    city = data['city']
    country = data['country'] or 'the country'
    scam_titles = data['scam_titles']
    num_scams = data['num_scams']

    # Summarize scam types for the safety answer
    if len(scam_titles) >= 3:
        scam_summary = f"{scam_titles[0]}, {scam_titles[1]}, and {scam_titles[2]}"
    elif len(scam_titles) == 2:
        scam_summary = f"{scam_titles[0]} and {scam_titles[1]}"
    elif len(scam_titles) == 1:
        scam_summary = scam_titles[0]
    else:
        scam_summary = "various tourist-targeting scams"

    top_scam = scam_titles[0] if scam_titles else "overcharging tourists"
    second_scam = scam_titles[1] if len(scam_titles) > 1 else "overcharging at tourist-area businesses"

    # FAQ 1: Is [City] safe for tourists?
    faq1_q = f"Is {city} safe for tourists?"
    faq1_a = (
        f"{city} is visited by millions of tourists each year and most visits are trouble-free. "
        f"The main risks are not violent crime but tourist-targeted scams like {scam_summary}. "
        f"We have documented {num_scams} common scams in {city}. "
        f"Stay alert in busy tourist areas, keep valuables secure, and research common scams before you arrive."
    )

    # FAQ 2: Most common scam
    faq2_q = f"What is the most common scam in {city}?"
    faq2_a = (
        f"The most frequently reported tourist scam in {city} is the {top_scam}. "
        f"This scam is well-documented by travelers on Reddit and travel forums. "
        f"The {second_scam} is also commonly reported. "
        f"Read the detailed breakdowns above for red flags and specific avoidance strategies for each scam."
    )

    # FAQ 3: Transport safety
    faq3_q, faq3_a = get_transport_question(city, country, scam_titles)

    # FAQ 4: Safe areas
    faq4_q, faq4_a = generate_safe_areas_answer(city, country)

    # FAQ 5: What to do if scammed
    faq5_q, faq5_a = generate_scammed_answer(city, country)

    return [
        (faq1_q, faq1_a),
        (faq2_q, faq2_a),
        (faq3_q, faq3_a),
        (faq4_q, faq4_a),
        (faq5_q, faq5_a),
    ]


def build_faq_html(faqs):
    """Build the FAQ section HTML matching existing page format."""
    items = []
    for q, a in faqs:
        items.append(f'''
        <div class="faq-item">
            <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
                {html.escape(q)}
                <span class="faq-arrow">&#9660;</span>
            </button>
            <div class="faq-a">{html.escape(a)}</div>
        </div>''')

    faq_html = '''
    <!-- FAQ -->
    <div class="faq-section">
        <h2 class="section-heading">Frequently Asked Questions</h2>
''' + ''.join(items) + '''

    </div>
'''
    return faq_html


def build_faq_jsonld(faqs):
    """Build the FAQPage JSON-LD object to add to the @graph."""
    main_entity = []
    for q, a in faqs:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return {
        "@type": "FAQPage",
        "mainEntity": main_entity
    }


def inject_faq_section(content, faq_html):
    """Inject the FAQ HTML between the emergency action-section and the related-section."""
    # Find the insertion point: after the closing </div> of the action-section, before the related-section
    # The pattern in pages without FAQ is:
    #   </div>  (closing action-section)
    #   [possibly whitespace/blank lines]
    #   <div class="related-section">

    pattern = re.compile(
        r'(</div>\s*<!-- end emergency -->\s*)'  # try with comment first
        r'(\s*<div class="related-section">)',
        re.DOTALL
    )
    match = pattern.search(content)

    if not match:
        # Most pages don't have a comment, so try simpler pattern
        # Look for the closing of action-section followed by related-section
        # The action-section ends with </div>\n    </div>\n\n    (then optional whitespace)
        # We need to find the </div> that closes the action-section div, then insert before related-section
        pattern2 = re.compile(
            r'(    </div>\n    </div>\n)\s*\n?\s*(\n?\s*<div class="related-section">)',
            re.DOTALL
        )
        match = pattern2.search(content)

    if not match:
        # Even simpler: just find <div class="related-section"> and insert before it
        # But we need to make sure we're inserting after the emergency section
        idx = content.find('<div class="related-section">')
        if idx == -1:
            return None

        # Insert FAQ HTML before the related-section
        return content[:idx] + faq_html.rstrip('\n') + '\n\n    ' + content[idx:]

    return content[:match.start(2)] + '\n' + faq_html.rstrip('\n') + '\n\n' + content[match.start(2):]


def inject_faq_jsonld(content, faq_jsonld):
    """Add FAQPage schema to the existing ld+json @graph array and update speakable."""
    # Find the ld+json script block
    ld_pattern = re.compile(
        r'(<script type="application/ld\+json">\s*)(.*?)(</script>)',
        re.DOTALL
    )
    match = ld_pattern.search(content)
    if not match:
        return content

    ld_text = match.group(2).strip()

    try:
        ld_data = json.loads(ld_text)
    except json.JSONDecodeError:
        print(f"  WARNING: Could not parse JSON-LD")
        return content

    if "@graph" not in ld_data:
        return content

    graph = ld_data["@graph"]

    # Check if FAQPage already exists
    for item in graph:
        if item.get("@type") == "FAQPage":
            return content  # already has it

    # Find the Place item index to insert FAQPage before it
    place_idx = None
    article_idx = None
    for i, item in enumerate(graph):
        if item.get("@type") == "Place":
            place_idx = i
        if item.get("@type") == "Article":
            article_idx = i

    # Insert FAQPage before Place (if found), otherwise at end
    if place_idx is not None:
        graph.insert(place_idx, faq_jsonld)
    else:
        graph.append(faq_jsonld)

    # Update speakable to include .faq-a
    for item in graph:
        if item.get("@type") == "Article" and "speakable" in item:
            selectors = item["speakable"].get("cssSelector", [])
            if ".faq-a" not in selectors:
                selectors.append(".faq-a")
                item["speakable"]["cssSelector"] = selectors

    # Serialize back with proper formatting
    new_ld = json.dumps(ld_data, indent=4, ensure_ascii=False)

    # Reconstruct the script block with the same indentation style
    new_script = match.group(1) + new_ld + '\n    ' + match.group(3)
    content = content[:match.start()] + new_script + content[match.end():]

    return content


def process_page(filepath):
    """Process a single scam page: extract data, generate FAQs, inject HTML and JSON-LD."""
    data = extract_page_data(filepath)

    if not data['city']:
        print(f"  SKIP: Could not extract city name from {filepath}")
        return False

    if not data['scam_titles']:
        print(f"  SKIP: No scam titles found in {filepath}")
        return False

    faqs = generate_faqs(data)
    faq_html = build_faq_html(faqs)
    faq_jsonld = build_faq_jsonld(faqs)

    content = data['content']

    # Inject FAQ HTML
    new_content = inject_faq_section(content, faq_html)
    if new_content is None:
        print(f"  SKIP: Could not find injection point in {filepath}")
        return False

    # Inject FAQ JSON-LD
    new_content = inject_faq_jsonld(new_content, faq_jsonld)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    # Find all scam city pages (exclude country hubs and the index)
    pattern = os.path.join(SCAMS_DIR, "*/index.html")
    all_pages = sorted(glob.glob(pattern))

    # Filter out country pages and the main index
    city_pages = [
        p for p in all_pages
        if '/country/' not in p and not p.endswith('scams/index.html')
    ]

    print(f"Total scam city pages found: {len(city_pages)}")

    # Find pages missing FAQ sections
    missing_faq = []
    for p in city_pages:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'faq-section' not in content:
            missing_faq.append(p)

    print(f"Pages missing FAQ: {len(missing_faq)}")
    print()

    updated = 0
    skipped = 0
    errors = []

    for filepath in missing_faq:
        slug = os.path.basename(os.path.dirname(filepath))
        print(f"Processing: {slug} ...", end=' ')

        try:
            success = process_page(filepath)
            if success:
                updated += 1
                print("OK")
            else:
                skipped += 1
        except Exception as e:
            errors.append((slug, str(e)))
            print(f"ERROR: {e}")

    print()
    print(f"=== RESULTS ===")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {len(errors)}")

    if errors:
        print("\nError details:")
        for slug, err in errors:
            print(f"  {slug}: {err}")

    # Verification pass
    print("\n=== VERIFICATION ===")
    still_missing = 0
    for p in city_pages:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'faq-section' not in content:
            still_missing += 1
            print(f"  Still missing: {os.path.basename(os.path.dirname(p))}")

    print(f"Pages still missing FAQ after run: {still_missing}")
    print(f"Pages with FAQ total: {len(city_pages) - still_missing} / {len(city_pages)}")


if __name__ == "__main__":
    main()
