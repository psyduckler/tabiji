#!/usr/bin/env python3
"""Generate credit card travel benefits pages for tabiji.ai"""
import json, os, glob

CARDS_DIR = os.path.expanduser("~/tabiji/app/data/cards")
OUTPUT_DIR = os.path.expanduser("~/tabiji/credit-cards")

NAV = '''<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/trends/">📊 Travel Trends</a>
                <a href="/scams/">🚨 Tourist Scams</a>
                <a href="/credit-cards/">💳 Credit Card Benefits</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>'''

BASE_CSS = '''
:root {
    --indigo: #2D3A5C; --indigo-light: #3D4E7A; --warm-cream: #F5F0E8; --sand: #E8DFD0;
    --earth: #8B7355; --earth-light: #A6906F; --terracotta: #C4704B; --deep-brown: #3E2F23;
    --sage: #7A8B6F; --white: #FEFCF9; --text: #2C2419; --text-muted: #6B5D4F;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 100%; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--white); color: var(--text); }
img, video { max-width: 100%; height: auto; }
nav { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 2rem; position: fixed; top: 0; left: 0; right: 0; background: rgba(254,252,249,0.95); backdrop-filter: blur(10px); z-index: 100; border-bottom: 1px solid var(--sand); }
.logo { text-decoration: none; font-size: 1.3rem; font-weight: 700; color: var(--indigo); }
.logo span { color: var(--terracotta); }
.logo{position:relative;padding-left:38px}.logo .owl-default,.logo .owl-fly{position:absolute;left:0;top:50%;transform:translateY(-50%);transition:opacity .15s ease}.logo .owl-fly{opacity:0}.logo:hover .owl-default{opacity:0}.logo:hover .owl-fly{opacity:1}
.cta-nav { background: var(--terracotta); color: white; padding: 0.55rem 1.25rem; border-radius: 8px; text-decoration: none; font-size: 0.9rem; font-weight: 600; }
.nav-links { display: flex; gap: 1.5rem; align-items: center; }
.hamburger { display: none; background: none; border: none; font-size: 1.5rem; color: var(--indigo); cursor: pointer; }
.nav-dropdown { position: relative; }
.nav-dropdown-toggle { background: none; border: none; color: var(--indigo); font-size: 0.9rem; font-weight: 500; cursor: pointer; padding: 0; font-family: inherit; }
.nav-dropdown-toggle::after { content: ' ▾'; font-size: 1.1rem; }
.nav-dropdown-menu { display: none; position: absolute; top: calc(100% + 0.5rem); left: 50%; transform: translateX(-50%); background: rgba(254, 252, 249, 0.98); backdrop-filter: blur(20px); border: 1px solid var(--sand); border-radius: 10px; padding: 0.5rem 0; min-width: 200px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); z-index: 200; }
.nav-dropdown.open .nav-dropdown-menu { display: block; }
.nav-dropdown-menu a { display: block; padding: 0.5rem 1.2rem; color: var(--indigo); text-decoration: none; font-size: 0.9rem; font-weight: 500; white-space: nowrap; transition: background 0.15s; }
.nav-dropdown-menu a:hover { background: rgba(0,0,0,0.04); }
@media (max-width: 768px) {
    .hamburger { display: block; }
    .nav-links { display: none; position: absolute; top: 100%; left: 0; right: 0; background: rgba(254, 252, 249, 0.98); backdrop-filter: blur(20px); border-bottom: 1px solid var(--sand); padding: 1rem 1.5rem; flex-direction: column; gap: 1rem; }
    .nav-links.open { display: flex; }
    .nav-dropdown-menu { position: static; transform: none; background: none; backdrop-filter: none; border: none; border-radius: 0; box-shadow: none; padding: 0; min-width: 0; padding-left: 1rem; }
    .nav-dropdown-menu a { padding: 0.35rem 0; font-size: 0.85rem; opacity: 0.8; }
    nav a.cta-nav { text-align: center; }
}
footer { text-align: center; padding: 3rem 2rem; border-top: 1px solid var(--sand); background: var(--white); }
.logo-footer { font-size: 1.2rem; font-weight: 700; color: var(--indigo); margin-bottom: 0.5rem; }
footer p { color: var(--text-muted); font-size: 0.85rem; }
'''

FOOTER = '''<footer>
    <div class="logo-footer">tabiji<span style="color:var(--terracotta)">.ai</span></div>
    <p>© 2026 Tabiji. AI-powered travel planning.</p>
    <p style="margin-top:0.5rem"><a href="/resources/" style="color:var(--earth);text-decoration:none">Resources</a> · <a href="/credit-cards/" style="color:var(--earth);text-decoration:none">Credit Cards</a> · <a href="/plan" style="color:var(--earth);text-decoration:none">Plan a Trip</a></p>
</footer>'''

GA4 = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-D7QHNRXLHJ');
</script>'''

def fee_display(card):
    fee = card.get('annualFee', 0)
    if fee == 0:
        return '$0 (no annual fee)'
    return f'${fee}/year'

def fee_tier(fee):
    if fee == 0: return '$0'
    if fee < 100: return 'Under $100'
    if fee <= 500: return '$100–500'
    return '$500+'

def get_card_highlights(card):
    tb = card.get('travelBenefits', {})
    highlights = []
    lounge = tb.get('loungeAccess')
    if lounge:
        highlights.append(f"✈️ Lounge access ({lounge.get('network','Priority Pass')})")
    else:
        highlights.append("❌ No lounge access")
    rental = tb.get('rentalCarInsurance')
    if rental:
        rtype = rental.get('type','secondary').title()
        highlights.append(f"🚗 {rtype} rental car insurance")
    else:
        highlights.append("❌ No rental car insurance")
    ge = tb.get('globalEntryTSA')
    if ge:
        highlights.append(f"🛂 Global Entry/TSA PreCheck credit (${ge.get('creditAmount',100)})")
    if tb.get('noForeignTransactionFee'):
        highlights.append("🌍 No foreign transaction fees")
    return highlights[:4]

def render_benefit_row(label, value, note=None):
    color = '#2a7a2a' if value else '#888'
    icon = '✅' if value else '—'
    html = f'<tr><td class="benefit-label">{label}</td><td class="benefit-val" style="color:{color}">{icon} {value if value else "Not included"}</td></tr>'
    return html

def render_card_page(card):
    tb = card.get('travelBenefits', {})
    rewards = card.get('rewards', {})
    slug = card['slug']
    name = card['name']
    issuer = card['issuer']
    network = card.get('network','')
    fee = card.get('annualFee', 0)
    best_for = card.get('bestFor', '')
    card_status = card.get('cardStatus', '')

    # Build lounge section
    lounge = tb.get('loungeAccess')
    if lounge:
        lounge_html = f'''
        <div class="benefit-card lounge-card">
            <h3>✈️ Lounge Access</h3>
            <p><strong>Network:</strong> {lounge.get('network','')}</p>
            {'<p><strong>Guest policy:</strong> Up to ' + str(lounge.get('guests','')) + ' complimentary guests per visit' + (f" (${lounge.get('guestFee')} fee per additional guest)" if lounge.get('guestFee') else '') + '</p>' if lounge.get('guests') else ''}
            {'<ul>' + ''.join(f'<li>{l}</li>' for l in lounge.get('otherLounges',[])) + '</ul>' if lounge.get('otherLounges') else ''}
            {'<p class="benefit-note">' + lounge.get('notes','') + '</p>' if lounge.get('notes') else ''}
        </div>'''
    else:
        lounge_html = '<div class="benefit-card benefit-missing"><h3>✈️ Lounge Access</h3><p>This card does not include airport lounge access. Consider upgrading to a premium card or purchasing a <a href="https://www.prioritypass.com" target="_blank">Priority Pass membership</a> separately.</p></div>'

    # Trip delay
    trip_delay = tb.get('tripDelay')
    if trip_delay:
        covers = ', '.join(trip_delay.get('covers', []))
        delay_html = f'''<div class="benefit-card">
            <h3>⏱️ Trip Delay Insurance</h3>
            <p>If your trip is delayed by <strong>{trip_delay.get('triggerHours', 6)}+ hours</strong>, you're covered for up to <strong>${trip_delay.get('coveragePerPerson', 0)}/person</strong> in expenses.</p>
            <p><strong>Covers:</strong> {covers}</p>
            {'<p class="benefit-note">' + trip_delay.get('notes','') + '</p>' if trip_delay.get('notes') else ''}
            <p class="benefit-note">Must book travel with this card. Keep all receipts for reimbursement.</p>
        </div>'''
    else:
        delay_html = '<div class="benefit-card benefit-missing"><h3>⏱️ Trip Delay Insurance</h3><p>Not included on this card. If your flight is delayed, you\'ll pay out of pocket for meals and hotels.</p></div>'

    # Trip cancellation
    trip_cancel = tb.get('tripCancellation')
    if trip_cancel:
        covers = ', '.join(trip_cancel.get('covers', []))
        cancel_html = f'''<div class="benefit-card">
            <h3>🚫 Trip Cancellation & Interruption</h3>
            <p>Reimburses up to <strong>${(trip_cancel.get('coveragePerPerson') or 0):,}/person</strong> (max ${(trip_cancel.get('coveragePerTrip') or 0):,}/trip) if you must cancel or cut short your trip.</p>
            <p><strong>Covered reasons:</strong> {covers}</p>
            {'<p class="benefit-note">' + trip_cancel.get('notes','') + '</p>' if trip_cancel.get('notes') else ''}
        </div>'''
    else:
        cancel_html = '<div class="benefit-card benefit-missing"><h3>🚫 Trip Cancellation & Interruption</h3><p>Not included on this card. If you need to cancel a non-refundable trip, you won\'t be reimbursed through this card.</p></div>'

    # Baggage
    lost_bag = tb.get('lostBaggage')
    bag_delay = tb.get('baggageDelay')
    bag_html = ''
    if lost_bag:
        bag_html += f'''<div class="benefit-card">
            <h3>🧳 Baggage Insurance</h3>
            <p><strong>Lost/stolen/damaged baggage:</strong> Up to <strong>${(lost_bag.get('coveragePerPerson') or 0):,}/person</strong></p>'''
        if lost_bag.get('checkedBagCoverage'):
            bag_html += f'<p>Checked bags: up to ${(lost_bag.get("checkedBagCoverage") or 0):,} | Carry-on: up to ${(lost_bag.get("carryOnCoverage") or lost_bag.get("coveragePerPerson") or 0):,}</p>'
        if lost_bag.get('notes'):
            bag_html += f'<p class="benefit-note">{lost_bag.get("notes")}</p>'
        if bag_delay:
            bag_html += f'<p style="margin-top:0.75rem"><strong>Delayed baggage:</strong> Up to ${bag_delay.get("coveragePerPerson",0)}/person after {bag_delay.get("triggerHours",6)}+ hours. Covers {", ".join(bag_delay.get("covers",[]))}.</p>'
        else:
            bag_html += '<p style="margin-top:0.75rem"><em>Baggage delay coverage: not included.</em></p>'
        bag_html += '</div>'
    elif bag_delay:
        bag_html = f'''<div class="benefit-card">
            <h3>🧳 Baggage Delay Insurance</h3>
            <p>If your bags are delayed by {bag_delay.get('triggerHours',6)}+ hours, you're covered up to ${bag_delay.get('coveragePerPerson',0)}/person for essentials.</p>
        </div>'''
    else:
        bag_html = '<div class="benefit-card benefit-missing"><h3>🧳 Baggage Insurance</h3><p>No lost or delayed baggage coverage on this card. Airline compensation is your main recourse.</p></div>'

    # Rental car
    rental = tb.get('rentalCarInsurance')
    if rental:
        rtype = rental.get('type','secondary')
        primary_note = ''
        if rtype == 'primary':
            primary_note = '<p class="highlight-note">✅ <strong>Primary coverage</strong> — this means you do NOT need to file with your personal auto insurance first. You can decline the collision damage waiver (CDW) at the counter and save $10–30/day.</p>'
        else:
            primary_note = '<p class="benefit-note">Secondary coverage — you must file with your personal auto insurance first, then this card covers the remainder.</p>'
        coverage = rental.get('coverageAmount')
        rental_html = f'''<div class="benefit-card">
            <h3>🚗 Rental Car Insurance</h3>
            {primary_note}
            {'<p><strong>Coverage amount:</strong> Up to ${:,}</p>'.format(coverage) if coverage else ''}
            <p><strong>Covers:</strong> {", ".join(rental.get("covers",[]))}</p>
            <p><strong>Excludes:</strong> {", ".join(rental.get("excludes",[]))}</p>
            {'<p><strong>Eligible countries:</strong> ' + rental.get('countries','') + '</p>' if rental.get('countries') else ''}
            {'<p class="benefit-note">' + rental.get('notes','') + '</p>' if rental.get('notes') else ''}
        </div>'''
    else:
        rental_html = '<div class="benefit-card benefit-missing"><h3>🚗 Rental Car Insurance</h3><p>No rental car coverage on this card. You\'ll need to purchase the CDW at the counter or rely on your personal auto insurance.</p></div>'

    # Emergency medical
    medical = tb.get('emergencyMedical', {})
    med_html = ''
    if medical and (medical.get('evacuation') or medical.get('evacuationCoverage') or medical.get('medicalCoverage')):
        med_html = f'''<div class="benefit-card">
            <h3>🏥 Emergency Medical & Evacuation</h3>
            {'<p><strong>Evacuation coverage:</strong> Up to ${:,} for emergency medical transportation.</p>'.format(medical.get('evacuationCoverage')) if medical.get('evacuationCoverage') else ('<p>✅ Emergency evacuation coordination covered (transportation costs covered).</p>' if medical.get('evacuation') else '')}
            {'<p><strong>Medical treatment:</strong> Up to ${:,} for medical expenses while traveling.</p>'.format(medical.get('medicalCoverage')) if medical.get('medicalCoverage') else ''}
            {'<p class="benefit-note">' + medical.get('notes','') + '</p>' if medical.get('notes') else ''}
        </div>'''
    elif medical and medical.get('notes'):
        med_html = f'''<div class="benefit-card benefit-missing">
            <h3>🏥 Emergency Medical & Evacuation</h3>
            <p class="benefit-note">{medical.get('notes')}</p>
        </div>'''
    else:
        med_html = '<div class="benefit-card benefit-missing"><h3>🏥 Emergency Medical & Evacuation</h3><p>No emergency medical or evacuation benefit. Consider supplemental travel insurance for international trips.</p></div>'

    # Global Entry / TSA
    ge = tb.get('globalEntryTSA')
    if ge:
        covers = ', '.join(ge.get('covers', ['Global Entry', 'TSA PreCheck']))
        ge_html = f'''<div class="benefit-card">
            <h3>🛂 Global Entry / TSA PreCheck Credit</h3>
            <p>Get a <strong>${ge.get('creditAmount',100)} statement credit</strong> every {ge.get('frequency','4 years')} when you pay for {covers} with this card.</p>
            <p>Global Entry ($100) includes TSA PreCheck and lets you skip customs lines when returning to the US — worth every cent for international travelers.</p>
        </div>'''
    else:
        ge_html = '<div class="benefit-card benefit-missing"><h3>🛂 Global Entry / TSA PreCheck Credit</h3><p>No Global Entry or TSA PreCheck credit on this card.</p></div>'

    # Foreign transaction fees
    no_ftf = tb.get('noForeignTransactionFee', False)
    ftf_html = f'''<div class="benefit-card {"" if no_ftf else "benefit-missing"}">
        <h3>🌍 Foreign Transaction Fees</h3>
        {"<p>✅ <strong>No foreign transaction fees</strong> — use this card internationally without paying an extra 2–3% on every purchase.</p>" if no_ftf else "<p>❌ <strong>Foreign transaction fee applies</strong> — using this card abroad will cost you an extra 2–3% on each transaction. Consider using a different card for international travel.</p>"}
    </div>'''

    # Credits section
    credits = []
    airline_credit = tb.get('airlineCredit')
    if airline_credit:
        credits.append(f'<li><strong>Airline fee credit:</strong> ${airline_credit.get("amount",0)}/year — {airline_credit.get("notes","")}</li>')
    hotel_credit = tb.get('hotelCredit')
    if hotel_credit:
        credits.append(f'<li><strong>Hotel credit:</strong> ${hotel_credit.get("amount",0)}/year — {hotel_credit.get("notes","")}</li>')
    uber_credit = tb.get('uberCredit')
    if uber_credit:
        credits.append(f'<li><strong>Uber credit:</strong> ${uber_credit.get("amount",0)}/year — {uber_credit.get("notes","")}</li>')
    for oc in tb.get('otherCredits', []):
        amt = oc.get('amount')
        amt_str = f'${amt}/year' if amt else ''
        credits.append(f'<li><strong>{oc.get("name","")}:</strong> {amt_str} — {oc.get("notes","")}</li>')

    credits_html = ''
    if credits:
        credits_html = f'''<div class="benefit-card credits-card">
            <h3>💰 Annual Credits & Perks</h3>
            <ul>{''.join(credits)}</ul>
        </div>'''

    # Rewards section
    rewards_html = f'''<div class="rewards-section">
        <h2 id="rewards">Rewards Structure</h2>
        <div class="rewards-grid">
            <div class="reward-item">
                <div class="reward-rate">{rewards.get('baseRate','1x')}</div>
                <div class="reward-label">Base rate on all purchases</div>
            </div>
            {'<div class="reward-item highlight"><div class="reward-rate">' + rewards.get('travelRate','') + '</div><div class="reward-label">Travel purchases</div></div>' if rewards.get('travelRate') else ''}
            {'<div class="reward-item"><div class="reward-rate">' + rewards.get('diningRate','') + '</div><div class="reward-label">Dining</div></div>' if rewards.get('diningRate') and rewards.get('diningRate') != rewards.get('baseRate') else ''}
            {''.join('<div class="reward-item"><div class="reward-rate">' + (cat.get('rate','') if isinstance(cat, dict) else '') + '</div><div class="reward-label">' + (cat.get('category','') if isinstance(cat, dict) else str(cat)) + '</div></div>' for cat in rewards.get('otherBonusCategories',[]))}
        </div>
        <div class="point-values">
            <h3>Point / Mile Values</h3>
            <ul>
                <li><strong>Cash back / statement credit:</strong> ~{int((rewards.get('pointValue',{}).get('cashBack') or 0.01)*100)}¢ per point</li>
                <li><strong>Travel portal redemption:</strong> ~{int((rewards.get('pointValue',{}).get('travelPortal') or 0.01)*100)}¢ per point</li>
                <li><strong>Transfer partners:</strong> {rewards.get('pointValue',{}).get('transferPartners','Varies')}</li>
            </ul>
        </div>
    </div>'''

    # Pros and cons
    pros, cons = build_pros_cons(card)
    pros_html = ''.join(f'<li>✅ {p}</li>' for p in pros)
    cons_html = ''.join(f'<li>❌ {c}</li>' for c in cons)

    # Related cards
    related = get_related_cards(card)
    related_html = ''
    if related:
        links = ' · '.join(f'<a href="/credit-cards/{r["slug"]}/">{r["name"]}</a>' for r in related)
        related_html = f'''<div class="related-cards">
            <h3>Compare with Similar Cards</h3>
            <p>{links}</p>
        </div>'''

    # Status banner
    status_banner = ''
    if card_status:
        status_banner = f'<div class="status-banner">⚠️ {card_status}</div>'

    # JSON-LD
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} Travel Benefits Guide",
        "description": f"Complete guide to travel benefits on the {name} — lounge access, insurance, rewards, and more.",
        "author": {"@type": "Organization", "name": "Tabiji"},
        "datePublished": "2026-03-30",
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"}
    })

    meta_desc = f"Full breakdown of {name} travel benefits: {'lounge access, ' if lounge else ''}{'primary rental car insurance, ' if rental and rental.get('type')=='primary' else ''}trip insurance, rewards, and who this card is best for."
    meta_desc = meta_desc[:155]

    # Build travelPerks summary list
    perks_list = card.get('travelPerks', [])
    perks_html = ''.join(f'<li>{p}</li>' for p in perks_list[:8])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Travel Benefits Guide 2026 — tabiji.ai</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://tabiji.ai/credit-cards/{slug}/">
    <meta property="og:title" content="{name} Travel Benefits Guide 2026">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/credit-cards/{slug}/">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <script type="application/ld+json">{jsonld}</script>
    {GA4}
    <style>
        {BASE_CSS}
        .card-hero {{
            background: linear-gradient(135deg, var(--indigo) 0%, var(--indigo-light) 100%);
            color: white;
            padding: 7rem 2rem 3rem;
            text-align: center;
        }}
        .card-hero h1 {{
            font-size: clamp(1.6rem, 4vw, 2.4rem);
            line-height: 1.2;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}
        .card-hero .issuer {{ font-size: 1rem; opacity: 0.8; margin-bottom: 1.5rem; }}
        .card-stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}
        .stat-item {{
            background: rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 0.75rem 1.25rem;
            text-align: center;
            min-width: 120px;
        }}
        .stat-value {{
            font-size: 1.3rem;
            font-weight: 700;
        }}
        .stat-label {{
            font-size: 0.75rem;
            opacity: 0.75;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .status-banner {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 0.75rem 2rem;
            text-align: center;
            font-size: 0.95rem;
            font-weight: 500;
        }}
        .page-container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem 4rem;
        }}
        .breadcrumb {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }}
        .breadcrumb a {{ color: var(--earth); text-decoration: none; }}
        .breadcrumb a:hover {{ color: var(--terracotta); }}
        .section-intro {{
            background: var(--warm-cream);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        .section-intro h2 {{
            font-size: 1.05rem;
            color: var(--indigo);
            margin-bottom: 0.75rem;
        }}
        .section-intro ul {{
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }}
        .section-intro li {{
            font-size: 0.9rem;
            color: var(--text);
        }}
        @media (max-width: 600px) {{
            .section-intro ul {{ grid-template-columns: 1fr; }}
        }}
        h2 {{
            font-size: 1.5rem;
            color: var(--indigo);
            font-weight: 700;
            margin: 2.5rem 0 1rem;
            letter-spacing: -0.01em;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--sand);
        }}
        h3 {{
            font-size: 1.1rem;
            color: var(--indigo);
            font-weight: 600;
        }}
        p {{
            font-size: 1rem;
            line-height: 1.75;
            color: var(--text);
            margin-bottom: 0.75rem;
        }}
        ul, ol {{ padding-left: 1.5rem; }}
        li {{ font-size: 1rem; line-height: 1.7; color: var(--text); margin-bottom: 0.3rem; }}
        a {{ color: var(--terracotta); }}
        .benefits-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        @media (max-width: 680px) {{
            .benefits-grid {{ grid-template-columns: 1fr; }}
        }}
        .benefit-card {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 12px;
            padding: 1.25rem;
            border-left: 3px solid var(--sage);
        }}
        .benefit-card h3 {{
            font-size: 0.95rem;
            margin-bottom: 0.6rem;
            color: var(--indigo);
        }}
        .benefit-card p {{
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 0.4rem;
        }}
        .benefit-card ul {{
            padding-left: 1.25rem;
            margin-top: 0.5rem;
        }}
        .benefit-card li {{
            font-size: 0.88rem;
            margin-bottom: 0.3rem;
        }}
        .benefit-missing {{
            border-left-color: var(--sand);
            opacity: 0.7;
        }}
        .benefit-missing h3 {{ opacity: 0.6; }}
        .lounge-card {{ border-left-color: var(--indigo); }}
        .credits-card {{ border-left-color: var(--terracotta); grid-column: 1 / -1; }}
        .benefit-note {{
            font-size: 0.82rem !important;
            color: var(--text-muted) !important;
            font-style: italic;
        }}
        .highlight-note {{
            background: rgba(122, 139, 111, 0.12);
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            font-size: 0.88rem !important;
            font-style: normal !important;
            color: var(--text) !important;
        }}
        .rewards-section {{
            background: var(--warm-cream);
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        .rewards-section h2 {{
            border: none;
            margin-top: 0;
            padding-bottom: 0;
            margin-bottom: 1rem;
        }}
        .rewards-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }}
        .reward-item {{
            background: white;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            min-width: 140px;
            flex: 1;
            border: 1px solid var(--sand);
        }}
        .reward-item.highlight {{
            border-color: var(--terracotta);
            background: rgba(196, 112, 75, 0.05);
        }}
        .reward-rate {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--indigo);
            margin-bottom: 0.25rem;
        }}
        .reward-label {{
            font-size: 0.78rem;
            color: var(--text-muted);
        }}
        .point-values h3 {{
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}
        .point-values li {{
            font-size: 0.9rem;
        }}
        .pros-cons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        @media (max-width: 600px) {{
            .pros-cons {{ grid-template-columns: 1fr; }}
        }}
        .pros-box, .cons-box {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 12px;
            padding: 1.25rem;
        }}
        .pros-box h3 {{ color: #2a7a2a; margin-bottom: 0.75rem; }}
        .cons-box h3 {{ color: #a44; margin-bottom: 0.75rem; }}
        .pros-box li, .cons-box li {{ font-size: 0.9rem; margin-bottom: 0.4rem; list-style: none; padding-left: 0; }}
        .best-for-box {{
            background: linear-gradient(135deg, var(--indigo) 0%, var(--indigo-light) 100%);
            color: white;
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        .best-for-box h2 {{
            color: white;
            border-color: rgba(255,255,255,0.2);
            margin-top: 0;
        }}
        .best-for-box p {{
            color: rgba(255,255,255,0.9);
            font-size: 1.05rem;
        }}
        .related-cards {{
            background: var(--warm-cream);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2rem;
        }}
        .related-cards h3 {{
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}
        .related-cards a {{
            color: var(--terracotta);
            text-decoration: none;
            font-weight: 500;
        }}
        .cta-box {{
            background: var(--warm-cream);
            border: 2px solid var(--terracotta);
            border-radius: 14px;
            padding: 1.75rem;
            text-align: center;
            margin-top: 2rem;
        }}
        .cta-box h3 {{
            color: var(--indigo);
            font-size: 1.2rem;
            margin-bottom: 0.75rem;
        }}
        .cta-box a.cta-btn {{
            display: inline-block;
            background: var(--terracotta);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            margin-top: 0.75rem;
        }}
    </style>
</head>
<body>
{NAV}
<div class="card-hero">
    <p class="issuer">💳 {issuer} · {network}</p>
    <h1>{name}</h1>
    <p style="font-size:1rem;opacity:0.8">Travel Benefits Guide 2026</p>
    <div class="card-stats">
        <div class="stat-item">
            <div class="stat-value">{'Free' if fee == 0 else f'${fee}'}</div>
            <div class="stat-label">Annual Fee</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{'✅' if lounge else '❌'}</div>
            <div class="stat-label">Lounge Access</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{'Primary' if rental and rental.get('type')=='primary' else ('Secondary' if rental else 'None')}</div>
            <div class="stat-label">Rental Coverage</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{'None' if no_ftf else '~3%'}</div>
            <div class="stat-label">Foreign Tx Fee</div>
        </div>
    </div>
</div>
{status_banner}
<div class="page-container">
    <div class="breadcrumb">
        <a href="/">Home</a> › <a href="/credit-cards/">Credit Card Benefits</a> › {name}
    </div>
    <div class="section-intro">
        <h2>📌 At a Glance: Top Travel Perks</h2>
        <ul>
            {perks_html}
        </ul>
    </div>

    <h2 id="benefits">Travel Benefits Breakdown</h2>
    <p>Here's exactly what you get — and what you don't — when you use the {name} for travel.</p>

    <div class="benefits-grid">
        {lounge_html}
        {ge_html}
        {delay_html}
        {cancel_html}
        {bag_html}
        {med_html}
        {rental_html}
        {ftf_html}
    </div>

    {credits_html}

    {rewards_html}

    <h2 id="pros-cons">Pros & Cons for Travelers</h2>
    <div class="pros-cons">
        <div class="pros-box">
            <h3>👍 Pros</h3>
            <ul>{pros_html}</ul>
        </div>
        <div class="cons-box">
            <h3>👎 Cons</h3>
            <ul>{cons_html}</ul>
        </div>
    </div>

    <div class="best-for-box">
        <h2>🎯 Who Is This Card Best For?</h2>
        <p>{best_for}</p>
    </div>

    {related_html}

    <div class="cta-box">
        <h3>Planning a Trip? Let AI Build Your Itinerary</h3>
        <p>Tabiji creates personalized day-by-day travel itineraries — free, in seconds.</p>
        <a href="/plan" class="cta-btn">Get a Free Itinerary →</a>
    </div>
</div>
{FOOTER}
<script>
document.querySelectorAll('.nav-dropdown-toggle').forEach(btn => {{
    document.addEventListener('click', e => {{
        if (!btn.parentElement.contains(e.target)) {{
            btn.parentElement.classList.remove('open');
        }}
    }});
}});
</script>
</body>
</html>'''

    return html


def build_pros_cons(card):
    tb = card.get('travelBenefits', {})
    pros = []
    cons = []
    fee = card.get('annualFee', 0)
    slug = card['slug']

    if tb.get('noForeignTransactionFee'):
        pros.append("No foreign transaction fees — safe to use internationally")
    else:
        cons.append("Charges foreign transaction fees (~2–3%) on international purchases")

    lounge = tb.get('loungeAccess')
    if lounge:
        pros.append(f"Airport lounge access ({lounge.get('network','')})")
    else:
        cons.append("No airport lounge access")

    rental = tb.get('rentalCarInsurance')
    if rental:
        if rental.get('type') == 'primary':
            pros.append("Primary rental car insurance — skip the CDW at the counter")
        else:
            pros.append("Rental car collision coverage (secondary)")
    else:
        cons.append("No rental car insurance")

    if tb.get('tripCancellation'):
        tc = tb['tripCancellation']
        pros.append(f"Trip cancellation coverage (up to ${(tc.get('coveragePerPerson') or 0):,}/person)")
    else:
        cons.append("No trip cancellation/interruption insurance")

    if tb.get('tripDelay'):
        td = tb['tripDelay']
        pros.append(f"Trip delay coverage after {td.get('triggerHours',6)}+ hours")
    else:
        cons.append("No trip delay insurance")

    if tb.get('globalEntryTSA'):
        ge = tb['globalEntryTSA']
        pros.append(f"${ge.get('creditAmount',100)} Global Entry/TSA PreCheck credit")
    else:
        cons.append("No Global Entry or TSA PreCheck credit")

    em = tb.get('emergencyMedical', {})
    if em and (em.get('evacuation') or em.get('evacuationCoverage')):
        pros.append("Emergency medical evacuation benefit")
    else:
        cons.append("No emergency medical evacuation coverage")

    if fee == 0:
        pros.append("No annual fee — keeps costs zero")
    elif fee < 100:
        pros.append(f"Low annual fee (${fee}) relative to benefits")
    elif fee >= 500:
        cons.append(f"High annual fee (${fee}) requires heavy use to justify")

    # Card-specific
    if slug == 'amex-platinum':
        pros.append("Access to Amex Centurion Lounges — among the best in the US")
        pros.append("Complimentary hotel elite status (Marriott Gold + Hilton Gold)")
    if slug == 'chase-sapphire-reserve':
        pros.append("$300 automatic travel credit offsets much of the annual fee")
        pros.append("Points transfer 1:1 to United, Hyatt, British Airways, and more")
    if slug == 'capital-one-venture-x':
        pros.append("$300 annual travel credit + 10K anniversary miles nearly offset the fee")
    if slug == 'citi-prestige':
        pros.append("Fourth night free on 4+ night hotel stays (up to 2x/year)")
        cons.append("Card discontinued — no longer available to new applicants")
    if slug == 'us-bank-altitude-reserve':
        cons.append("Card closed to new applications as of November 2024")
        cons.append("$325 travel credit now restricted to US Bank Travel Center only")
    if slug == 'discover-it-miles':
        cons.append("Limited international acceptance — Discover not widely accepted abroad")
        pros.append("First-year mile match effectively doubles year-one earnings")
    if slug in ['amex-platinum', 'amex-gold', 'amex-green']:
        pros.append("Access to Amex Membership Rewards — 20+ airline/hotel transfer partners")

    return pros[:6], cons[:6]


ALL_CARDS = [
    {"slug": "amex-gold", "name": "Amex Gold", "issuer": "Amex"},
    {"slug": "amex-green", "name": "Amex Green", "issuer": "Amex"},
    {"slug": "amex-platinum", "name": "Amex Platinum", "issuer": "Amex"},
    {"slug": "capital-one-venture-x", "name": "Capital One Venture X", "issuer": "Capital One"},
    {"slug": "capital-one-venture", "name": "Capital One Venture", "issuer": "Capital One"},
    {"slug": "chase-sapphire-preferred", "name": "Chase Sapphire Preferred", "issuer": "Chase"},
    {"slug": "chase-sapphire-reserve", "name": "Chase Sapphire Reserve", "issuer": "Chase"},
    {"slug": "citi-prestige", "name": "Citi Prestige", "issuer": "Citi"},
    {"slug": "discover-it-miles", "name": "Discover it Miles", "issuer": "Discover"},
    {"slug": "us-bank-altitude-reserve", "name": "US Bank Altitude Reserve", "issuer": "US Bank"},
]


def get_related_cards(card):
    slug = card['slug']
    issuer = card.get('issuer', '')
    fee = card.get('annualFee', 0)

    related = []
    # Same issuer
    for c in ALL_CARDS:
        if c['slug'] != slug and c['issuer'] == issuer:
            related.append(c)
    # Similar fee tier
    if not related:
        tier = fee_tier(fee)
        for c in ALL_CARDS:
            if c['slug'] != slug and fee_tier(fee) == tier:
                related.append(c)
    return related[:3]


def render_index_page(cards_data):
    card_items = []
    for c in cards_data:
        tb = c.get('travelBenefits', {})
        fee = c.get('annualFee', 0)
        lounge = tb.get('loungeAccess')
        rental = tb.get('rentalCarInsurance')
        ge = tb.get('globalEntryTSA')
        highlights = get_card_highlights(c)
        hi_html = ''.join(f'<li>{h}</li>' for h in highlights)
        slug = c['slug']
        name = c['name']
        issuer = c['issuer']
        network = c.get('network', '')
        tier = fee_tier(fee)
        fee_disp = 'Free' if fee == 0 else f'${fee}/yr'
        card_status = c.get('cardStatus', '')
        status_note = ''
        if card_status and 'CLOSED' in card_status or (card_status and 'DISCONTINUED' in card_status):
            status_note = '<span class="card-status-badge">Closed to new apps</span>'

        card_items.append(f'''<div class="card-item" data-fee-tier="{tier}">
            <div class="card-header">
                <div>
                    <div class="card-name"><a href="/credit-cards/{slug}/">{name}</a> {status_note}</div>
                    <div class="card-meta">{issuer} · {network}</div>
                </div>
                <div class="card-fee">{fee_disp}</div>
            </div>
            <ul class="card-highlights">{hi_html}</ul>
            <a href="/credit-cards/{slug}/" class="card-link">View full benefits →</a>
        </div>''')

    all_items_html = '\n'.join(card_items)

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Credit Card Travel Benefits Compared 2026",
        "description": "Compare travel benefits across 10 popular credit cards — lounge access, insurance, rewards, and annual fees.",
        "author": {"@type": "Organization", "name": "Tabiji"},
        "datePublished": "2026-03-30",
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"}
    })

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Credit Card Travel Benefits Compared 2026 — tabiji.ai</title>
    <meta name="description" content="Compare travel benefits across 10 popular credit cards — lounge access, trip insurance, rental car coverage, rewards, and annual fees. Find the best card for your travel style.">
    <link rel="canonical" href="https://tabiji.ai/credit-cards/">
    <meta property="og:title" content="Credit Card Travel Benefits Compared 2026">
    <meta property="og:description" content="Compare lounge access, trip insurance, rental car coverage, and rewards across Amex, Chase, Capital One, and more.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/credit-cards/">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <script type="application/ld+json">{jsonld}</script>
    {GA4}
    <style>
        {BASE_CSS}
        .page-hero {{
            background: linear-gradient(135deg, var(--indigo) 0%, var(--indigo-light) 100%);
            color: white;
            padding: 7rem 2rem 3rem;
            text-align: center;
        }}
        .page-hero h1 {{
            font-size: clamp(1.8rem, 4vw, 2.8rem);
            line-height: 1.2;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}
        .page-hero p {{
            font-size: 1.1rem;
            opacity: 0.85;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        .page-container {{
            max-width: 940px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem 4rem;
        }}
        .intro-box {{
            background: var(--warm-cream);
            border-radius: 14px;
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text);
        }}
        .filter-bar {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1.75rem;
            align-items: center;
        }}
        .filter-bar span {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-right: 0.25rem;
        }}
        .filter-btn {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 20px;
            padding: 0.35rem 0.9rem;
            font-size: 0.85rem;
            color: var(--indigo);
            cursor: pointer;
            font-family: inherit;
            transition: all 0.15s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--indigo);
            color: white;
            border-color: var(--indigo);
        }}
        .cards-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
        }}
        @media (max-width: 680px) {{
            .cards-grid {{ grid-template-columns: 1fr; }}
        }}
        .card-item {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            transition: box-shadow 0.2s, transform 0.2s;
        }}
        .card-item:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }}
        .card-item.hidden {{ display: none; }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }}
        .card-name {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--indigo);
        }}
        .card-name a {{
            color: var(--indigo);
            text-decoration: none;
        }}
        .card-name a:hover {{ color: var(--terracotta); }}
        .card-meta {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }}
        .card-fee {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--terracotta);
            white-space: nowrap;
            margin-left: 1rem;
        }}
        .card-highlights {{
            list-style: none;
            padding: 0;
            margin-bottom: 0.75rem;
        }}
        .card-highlights li {{
            font-size: 0.85rem;
            color: var(--text);
            padding: 0.2rem 0;
            line-height: 1.4;
        }}
        .card-link {{
            font-size: 0.88rem;
            color: var(--terracotta);
            text-decoration: none;
            font-weight: 600;
        }}
        .card-link:hover {{ text-decoration: underline; }}
        .card-status-badge {{
            font-size: 0.72rem;
            background: #fff3cd;
            color: #856404;
            border-radius: 4px;
            padding: 0.1rem 0.4rem;
            font-weight: 500;
            margin-left: 0.3rem;
            vertical-align: middle;
        }}
        .section-title {{
            font-size: 1.3rem;
            color: var(--indigo);
            font-weight: 700;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--sand);
        }}
        .compare-table-wrap {{
            overflow-x: auto;
            margin: 2rem 0;
            -webkit-overflow-scrolling: touch;
        }}
        .compare-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            min-width: 640px;
        }}
        .compare-table th {{
            background: var(--indigo);
            color: white;
            padding: 0.6rem 0.75rem;
            text-align: left;
            font-weight: 600;
            white-space: nowrap;
        }}
        .compare-table td {{
            padding: 0.55rem 0.75rem;
            border-bottom: 1px solid var(--sand);
            vertical-align: middle;
        }}
        .compare-table tr:nth-child(even) td {{
            background: var(--warm-cream);
        }}
        .compare-table a {{
            color: var(--terracotta);
            text-decoration: none;
            font-weight: 500;
        }}
        .yes {{ color: #2a7a2a; font-weight: 600; }}
        .no {{ color: #888; }}
        .primary-badge {{ color: #1a5c1a; font-weight: 700; }}
        .secondary-badge {{ color: #666; }}
        .cta-box {{
            background: var(--warm-cream);
            border: 2px solid var(--terracotta);
            border-radius: 14px;
            padding: 1.75rem;
            text-align: center;
            margin-top: 2.5rem;
        }}
        .cta-box h3 {{ color: var(--indigo); font-size: 1.2rem; margin-bottom: 0.75rem; }}
        .cta-box a.cta-btn {{
            display: inline-block;
            background: var(--terracotta);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            margin-top: 0.75rem;
        }}
    </style>
</head>
<body>
{NAV}
<div class="page-hero">
    <h1>💳 Credit Card Travel Benefits Compared</h1>
    <p>Find the right card for your trips — lounge access, trip insurance, rental car coverage, and rewards, all in one place.</p>
</div>
<div class="page-container">
    <div class="intro-box">
        <strong>Why credit card travel benefits matter:</strong> The right card can save you hundreds of dollars per trip. Primary rental car insurance alone saves $10–30/day at the counter. Trip cancellation coverage can reimburse thousands if you need to cancel. And lounge access turns a 2-hour layover into something almost enjoyable. This guide covers all major travel benefits for 10 popular cards so you can make an informed choice.
    </div>

    <div class="section-title">All Cards</div>
    <div class="filter-bar">
        <span>Filter by annual fee:</span>
        <button class="filter-btn active" onclick="filterCards('all', this)">All</button>
        <button class="filter-btn" onclick="filterCards('$0', this)">Free ($0)</button>
        <button class="filter-btn" onclick="filterCards('Under $100', this)">Under $100</button>
        <button class="filter-btn" onclick="filterCards('$100–500', this)">$100–500</button>
        <button class="filter-btn" onclick="filterCards('$500+', this)">$500+</button>
    </div>
    <div class="cards-grid" id="cardsGrid">
        {all_items_html}
    </div>

    <div style="margin-top:2.5rem">
        <div class="section-title">Quick Comparison Table</div>
        <div class="compare-table-wrap">
            <table class="compare-table">
                <thead>
                    <tr>
                        <th>Card</th>
                        <th>Annual Fee</th>
                        <th>Lounge</th>
                        <th>Rental Car</th>
                        <th>Trip Cancel</th>
                        <th>No FX Fee</th>
                        <th>Global Entry</th>
                    </tr>
                </thead>
                <tbody>
                    {render_comparison_rows(cards_data)}
                </tbody>
            </table>
        </div>
    </div>

    <div class="cta-box">
        <h3>Ready to Book Your Next Trip?</h3>
        <p>Tabiji builds personalized AI travel itineraries — free, in seconds. Tell us where you want to go.</p>
        <a href="/plan" class="cta-btn">Get a Free Itinerary →</a>
    </div>
</div>
{FOOTER}
<script>
function filterCards(tier, btn) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.card-item').forEach(item => {{
        if (tier === 'all' || item.dataset.feeTier === tier) {{
            item.classList.remove('hidden');
        }} else {{
            item.classList.add('hidden');
        }}
    }});
}}
document.querySelectorAll('.nav-dropdown-toggle').forEach(btn => {{
    document.addEventListener('click', e => {{
        if (!btn.parentElement.contains(e.target)) {{
            btn.parentElement.classList.remove('open');
        }}
    }});
}});
</script>
</body>
</html>'''


def render_comparison_rows(cards_data):
    rows = []
    for c in cards_data:
        tb = c.get('travelBenefits', {})
        slug = c['slug']
        name = c['name']
        fee = c.get('annualFee', 0)
        fee_str = 'Free' if fee == 0 else f'${fee}'
        lounge = '✅' if tb.get('loungeAccess') else '<span class="no">—</span>'
        rental = tb.get('rentalCarInsurance')
        if rental:
            if rental.get('type') == 'primary':
                rental_str = '<span class="primary-badge">Primary</span>'
            else:
                rental_str = '<span class="secondary-badge">Secondary</span>'
        else:
            rental_str = '<span class="no">—</span>'
        trip_cancel = '<span class="yes">✅</span>' if tb.get('tripCancellation') else '<span class="no">—</span>'
        no_fx = '<span class="yes">✅</span>' if tb.get('noForeignTransactionFee') else '<span class="no">❌</span>'
        ge = tb.get('globalEntryTSA')
        ge_str = f'<span class="yes">${ge.get("creditAmount",100)}</span>' if ge else '<span class="no">—</span>'
        rows.append(f'<tr><td><a href="/credit-cards/{slug}/">{name}</a></td><td>{fee_str}</td><td>{lounge}</td><td>{rental_str}</td><td>{trip_cancel}</td><td>{no_fx}</td><td>{ge_str}</td></tr>')
    return '\n'.join(rows)


def main():
    json_files = sorted(glob.glob(os.path.join(CARDS_DIR, '*.json')))
    cards_data = []
    for jf in json_files:
        with open(jf) as f:
            card = json.load(f)
        cards_data.append(card)
        slug = card['slug']
        out_dir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        html = render_card_page(card)
        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w') as f:
            f.write(html)
        print(f"✅ Generated: credit-cards/{slug}/index.html")

    # Index page
    index_html = render_index_page(cards_data)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)
    print("✅ Generated: credit-cards/index.html")


if __name__ == '__main__':
    main()
