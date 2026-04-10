#!/usr/bin/env python3
"""
Generate 50 new scam pages, update the scam index, and update country hubs.

Steps:
1. Add CITY_SLUGS entries for the 50 new cities
2. Run generate_pages.py to build the HTML
3. Update scams/index.html with new entries
4. Update country hub pages with scam links
"""
import json
import os
import re
import sys

BASE = "/Users/bjh/Documents/tabiji"
SCAMS_DIR = os.path.join(BASE, "scams")
GEN_SCRIPT = os.path.join(SCAMS_DIR, "generate_pages.py")

# New city slug mappings
NEW_SLUGS = {
    "Cusco": "cusco",
    "Agra": "agra",
    "Varanasi": "varanasi",
    "Hoi An": "hoi-an",
    "Da Nang": "da-nang",
    "Koh Samui": "koh-samui",
    "Krabi": "krabi",
    "Boracay": "boracay",
    "El Nido": "el-nido",
    "Luang Prabang": "luang-prabang",
    "Lombok": "lombok",
    "Yogyakarta": "yogyakarta",
    "Amalfi Coast": "amalfi-coast",
    "Cinque Terre": "cinque-terre",
    "Sorrento": "sorrento",
    "La Paz": "la-paz",
    "Santiago": "santiago",
    "Mendoza": "mendoza",
    "Penang": "penang",
    "Langkawi": "langkawi",
    "Nha Trang": "nha-trang",
    "Sapa": "sapa",
    "Ubud": "ubud",
    "Positano": "positano",
    "Budva": "budva",
    "Hvar": "hvar",
    "San Jose": "san-jose-costa-rica",
    "Arusha": "arusha",
    "Queenstown": "queenstown",
    "Cairns": "cairns",
    "Lake Bled": "lake-bled",
    "Udaipur": "udaipur",
    "Maui": "maui",
    "Koh Phangan": "koh-phangan",
    "Chefchaouen": "chefchaouen",
    "Lyon": "lyon",
    "Bordeaux": "bordeaux",
    "Valparaíso": "valparaiso",
    "Rishikesh": "rishikesh",
    "Stone Town": "stone-town",
    "Gold Coast": "gold-coast",
    "Dalat": "dalat",
    "Chiang Rai": "chiang-rai",
    "Lake Como": "lake-como",
    "Bologna": "bologna",
    "Essaouira": "essaouira",
    "Nusa Penida": "nusa-penida",
    "Pai": "pai",
    "Bariloche": "bariloche",
    "Siargao": "siargao",
}

# Country mapping for each city (for country hub updates)
CITY_COUNTRY_SLUG = {
    "cusco": "peru",
    "agra": "india",
    "varanasi": "india",
    "hoi-an": "vietnam",
    "da-nang": "vietnam",
    "koh-samui": "thailand",
    "krabi": "thailand",
    "boracay": "philippines",
    "el-nido": "philippines",
    "luang-prabang": "laos",
    "lombok": "indonesia",
    "yogyakarta": "indonesia",
    "amalfi-coast": "italy",
    "cinque-terre": "italy",
    "sorrento": "italy",
    "la-paz": "bolivia",
    "santiago": "chile",
    "mendoza": "argentina",
    "penang": "malaysia",
    "langkawi": "malaysia",
    "nha-trang": "vietnam",
    "sapa": "vietnam",
    "ubud": "indonesia",
    "positano": "italy",
    "budva": "montenegro",
    "hvar": "croatia",
    "san-jose-costa-rica": "costa-rica",
    "arusha": "tanzania",
    "queenstown": "new-zealand",
    "cairns": "australia",
    "lake-bled": "slovenia",
    "udaipur": "india",
    "maui": "united-states",
    "koh-phangan": "thailand",
    "chefchaouen": "morocco",
    "lyon": "france",
    "bordeaux": "france",
    "valparaiso": "chile",
    "rishikesh": "india",
    "stone-town": "tanzania",
    "gold-coast": "australia",
    "dalat": "vietnam",
    "chiang-rai": "thailand",
    "lake-como": "italy",
    "bologna": "italy",
    "essaouira": "morocco",
    "nusa-penida": "indonesia",
    "pai": "thailand",
    "bariloche": "argentina",
    "siargao": "philippines",
}


def step1_add_slugs():
    """Add new CITY_SLUGS entries to generate_pages.py"""
    print("Step 1: Adding CITY_SLUGS to generate_pages.py...")

    with open(GEN_SCRIPT) as f:
        content = f.read()

    # Find the end of CITY_SLUGS dict (the closing brace + newline before next section)
    # The dict ends with:  "Montego Bay": "montego-bay",\n}
    insert_point = content.find('"Montego Bay": "montego-bay",')
    if insert_point == -1:
        print("  ERROR: Could not find CITY_SLUGS end marker")
        return False

    # Find the line end after this entry
    line_end = content.index("\n", insert_point)

    # Build new entries
    new_entries = []
    for city, slug in sorted(NEW_SLUGS.items()):
        entry = f'    "{city}": "{slug}",'
        # Check if it already exists
        if f'"{city}":' in content:
            continue
        new_entries.append(entry)

    if not new_entries:
        print("  All slugs already exist")
        return True

    insert_text = "\n" + "\n".join(new_entries)
    content = content[:line_end] + insert_text + content[line_end:]

    with open(GEN_SCRIPT, "w") as f:
        f.write(content)

    print(f"  Added {len(new_entries)} new CITY_SLUGS entries")
    return True


def step1b_add_safety_tips():
    """Add safety tips for new cities"""
    print("Step 1b: Adding SAFETY_TIPS for new cities...")

    with open(GEN_SCRIPT) as f:
        content = f.read()

    # Find the end of SAFETY_TIPS dict
    # We'll add entries before the closing brace
    tips = {
        "Cusco": [
            "Never accept items placed in your hands by women with alpacas — agree on a price first or decline",
            "Book Machu Picchu tours only through verified agencies with DIRCETUR licenses — never from street vendors",
            "Use small bills and exact change for taxis — watch for the counterfeit note switch",
            "Carry a photocopy of your passport — never hand the original to anyone on the street",
        ],
        "Agra": [
            "Hire official guides only from inside the Taj Mahal ticket counter — they carry ASI ID badges",
            "Never believe a taxi driver who says your hotel is closed — call the hotel directly",
            "Use Ola or Uber instead of e-rickshaws for transparent pricing and avoid overcharging",
            "Decline all gemstone purchase offers — the export-and-resell-for-profit scheme is always a scam",
        ],
        "Varanasi": [
            "Keep your hands at your sides on the ghats — don't accept offerings, flowers, or tilaks without agreeing on a price",
            "Agree on boat ride price, duration, stops, and return point before boarding — get it in writing",
            "Navigate using Google Maps rather than accepting shortcut guides through the lanes",
            "Buy silk from government emporiums like UP Handloom — not from shops your 'guide' takes you to",
        ],
        "Hoi An": [
            "When using Hoi An tailors, photograph the fabric bolt and take a cutting as reference",
            "State the denomination out loud when handing over Vietnamese dong — prevent the note switch",
            "Use Grab for transparent transport pricing — avoid unmetered taxis and cyclos",
            "Ask 'Bao nhieu?' (How much?) before any interaction with vendors or photo ops",
        ],
        "Da Nang": [
            "Download Grab before landing at Da Nang airport — never accept fares shown on a driver's phone",
            "Ask about minimum spend before sitting in 'free' beach loungers",
            "Video-record rental motorbikes from all angles before riding — never leave your passport as deposit",
            "The fair Grab fare from the airport to the city center is 50,000-100,000 VND",
        ],
        "Koh Samui": [
            "Video-record jet skis from every angle before and after renting — in front of the operator",
            "If confronted with a damage claim, call Tourist Police at 1155 immediately — do not pay under pressure",
            "Never accept free activities in exchange for attending a timeshare presentation",
            "Buy drinks from established bars, not random beach bucket vendors — methanol poisoning is a real risk",
        ],
        "Boracay": [
            "Only book tours with DOT-accredited operators — ask for their accreditation number",
            "Standard tricycle fare between stations is ₱20-50 — refuse anything above ₱100 for short rides",
            "Video jet skis and water sports equipment before use — check under any tape or stickers for hidden damage",
            "Book everything through your hotel's tour desk to avoid unregistered operators",
        ],
        "Luang Prabang": [
            "Watch the morning alms ceremony from a respectful distance — don't participate through paid 'helpers'",
            "Pre-book Pakbeng accommodation before the slow boat — ignore anyone on the boat claiming everything is full",
            "Count your change carefully at the night market — carry small bills to avoid short-changing",
            "A fair room in Pakbeng costs 80,000-150,000 kip ($4-8) — don't pay more to boat touts",
        ],
        "La Paz": [
            "Never hand over your wallet to anyone claiming to be a police officer — offer to walk to the station",
            "Use ATMs only inside banks during business hours — never get into a taxi waiting near an ATM",
            "Book Death Road tours with Gravity Bolivia or Barracuda Biking — budget $80-120 for proper safety equipment",
            "Carry a color photocopy of your passport — keep the original locked at your hotel",
        ],
        "Ubud": [
            "Use bank-affiliated money changers only (BMC, Central Kuta) — count every note slowly before leaving",
            "Remove sunglasses, hats, and earrings before entering the Monkey Forest — monkeys are trained to snatch",
            "Decline gallery invitations from 'art students' near the Monkey Forest — it's a commission-driven sales pitch",
            "Use Wise or Revolut cards at ATMs for near-market exchange rates",
        ],
        "Amalfi Coast": [
            "Use official parking garages in Positano or take the SITA bus — avoid unofficial parking attendants",
            "Ask about coperto, servizio, and view supplements before ordering at waterfront restaurants",
            "Book boat tours through Viator or GetYourGuide for verified operators — avoid harbor freelancers",
            "Say 'acqua del rubinetto' for free tap water — decline bread if you don't want the charge",
        ],
        "San Jose": [
            "Use only official orange airport taxis from the designated stand — or pre-book through your hotel",
            "Verify rental car insurance is included in the online price before booking — mandatory coverage adds $15-30/day",
            "Choose accommodation with 24/7 security, gated entrances, and cameras",
            "Use Uber or DiDi instead of street taxis — especially at night",
        ],
        "Arusha": [
            "Verify safari companies are registered with TATO (Tanzania Association of Tour Operators) before paying",
            "Pay a maximum 20-30% deposit via credit card — never via Western Union or wire transfer",
            "Book directly with safari operators at their physical offices — avoid bus station middlemen",
            "Budget $1,200-1,500 minimum for a legitimate 3-day safari",
        ],
    }

    # Find a good insertion point in SAFETY_TIPS
    for city, tip_list in tips.items():
        if f'"{city}":' in content:
            continue  # Already exists
        # Find the end of SAFETY_TIPS by looking for the pattern
        # We'll insert before a known city that's near the end
        marker = '"Rio de Janeiro": ['
        idx = content.find(marker)
        if idx == -1:
            continue

        tip_str = json.dumps(tip_list, indent=8)
        # Format as Python list
        tip_lines = [f'        "{t}",' for t in tip_list]
        entry = f'    "{city}": [\n' + "\n".join(tip_lines) + "\n    ],\n    "
        content = content[:idx] + entry + content[idx:]

    with open(GEN_SCRIPT, "w") as f:
        f.write(content)

    print(f"  Added safety tips for {len(tips)} cities")
    return True


def step2_run_generator():
    """Run the page generator"""
    print("\nStep 2: Running generate_pages.py...")
    os.chdir(SCAMS_DIR)
    ret = os.system(f"python3 {GEN_SCRIPT} 2>&1 | tail -60")
    return ret == 0


def step3_update_index():
    """Update scams/index.html with new city entries"""
    print("\nStep 3: Updating scams index page...")

    index_path = os.path.join(SCAMS_DIR, "index.html")
    with open(index_path) as f:
        content = f.read()

    # Load the research data to get city/country info
    with open(os.path.join(SCAMS_DIR, "research", "batch_new_50.json")) as f:
        cities_data = json.load(f)

    added = 0
    for city_data in cities_data:
        city = city_data["city"]
        country = city_data["country"]
        flag = city_data["flag"]
        slug = NEW_SLUGS.get(city, "")
        if not slug:
            continue

        scam_count = len(city_data["scams"])
        # Check if already in the index
        if f'href="/scams/{slug}/"' in content:
            continue

        # Build the card HTML matching existing format
        # Find where to insert — look for existing cards and add after the last one
        # We'll find the pattern of grid items
        card_html = f'''<a href="/scams/{slug}/" class="city-card">
            <span class="city-flag">{flag}</span>
            <span class="city-name">{city}</span>
            <span class="city-country">{country}</span>
            <span class="scam-count">{scam_count} scams</span>
        </a>'''

        # Insert before the closing </div> of the city-grid
        grid_end = content.rfind("</div><!-- /city-grid -->")
        if grid_end == -1:
            # Try another pattern
            grid_end = content.rfind('</div>\n\n    </div>\n\n    <!-- Footer')
            if grid_end == -1:
                # Find last city-card and insert after it
                last_card = content.rfind("</a>", 0, content.rfind("</section>"))
                if last_card != -1:
                    grid_end = last_card + 4  # After </a>

        if grid_end != -1:
            content = content[:grid_end] + "\n        " + card_html + "\n        " + content[grid_end:]
            added += 1

    if added > 0:
        # Update the count in the hero
        # Find "200 Tourist Scam" or similar count
        content = re.sub(
            r'(\d+)\s*(Tourist Scam|Scam|destinations)',
            lambda m: f"{int(m.group(1)) + added} {m.group(2)}",
            content,
            count=1
        )

        with open(index_path, "w") as f:
            f.write(content)
        print(f"  Added {added} new cities to scam index")
    else:
        print("  No new cities to add (or could not find insertion point)")

    return True


def step4_update_country_hubs():
    """Add scam page links to corresponding country hub pages"""
    print("\nStep 4: Updating country hub pages...")

    countries_dir = os.path.join(BASE, "countries")

    # Load city data for display names
    with open(os.path.join(SCAMS_DIR, "research", "batch_new_50.json")) as f:
        cities_data = json.load(f)

    city_display = {}
    for cd in cities_data:
        slug = NEW_SLUGS.get(cd["city"], "")
        city_display[slug] = cd["city"]

    updated_countries = set()
    for slug, country_slug in CITY_COUNTRY_SLUG.items():
        country_index = os.path.join(countries_dir, country_slug, "index.html")
        if not os.path.exists(country_index):
            print(f"  Skipping {slug} — country page {country_slug} not found")
            continue

        with open(country_index) as f:
            html = f.read()

        # Check if this scam page is already linked
        if f'/scams/{slug}/' in html:
            continue

        city_name = city_display.get(slug, slug.replace("-", " ").title())

        # Find a good place to insert the scam link
        # Look for existing scam links section or a "Safety" / "Scams" section
        scam_link = f'<a href="/scams/{slug}/">Tourist Scams in {city_name}</a>'

        # Try to find existing scam links
        existing_scam = re.search(r'href="/scams/[^"]+/"', html)
        if existing_scam:
            # Insert after the last existing scam link's parent element
            # Find the <li> or <a> containing it and add a sibling
            pos = existing_scam.end()
            # Find the end of the current <li> or line
            line_end = html.index("\n", pos)
            # Check if it's inside an <li>
            context = html[max(0, existing_scam.start()-50):existing_scam.start()]
            if "<li" in context:
                # Find the </li> after this link
                li_end = html.index("</li>", pos)
                insert_pos = li_end + 5  # After </li>
                new_li = f'\n<li>{scam_link}</li>'
                html = html[:insert_pos] + new_li + html[insert_pos:]
            else:
                # Just add after the current link line
                html = html[:line_end] + f'\n{scam_link}' + html[line_end:]

            with open(country_index, "w") as f:
                f.write(html)
            updated_countries.add(country_slug)
            print(f"  Added scam link for {city_name} to {country_slug}")

        else:
            # No existing scam links — try to add a scams section
            # Look for a safety section or resources section
            safety_match = re.search(r'(Safety|Travel Tips|Resources|Practical)', html, re.IGNORECASE)
            if safety_match:
                # Find the end of this section's content
                section_pos = safety_match.start()
                # Find the next closing tag after some content
                next_section = html.find("</section>", section_pos)
                if next_section == -1:
                    next_section = html.find("</div>", section_pos + 200)

                if next_section != -1:
                    scam_section = f'\n<p><strong>Stay safe:</strong> {scam_link}</p>\n'
                    html = html[:next_section] + scam_section + html[next_section:]

                    with open(country_index, "w") as f:
                        f.write(html)
                    updated_countries.add(country_slug)
                    print(f"  Added scam link for {city_name} to {country_slug} (new section)")

    print(f"\n  Updated {len(updated_countries)} country hub pages")
    return True


if __name__ == "__main__":
    step1_add_slugs()
    step1b_add_safety_tips()
    step2_run_generator()
    step3_update_index()
    step4_update_country_hubs()
    print("\nDone!")
