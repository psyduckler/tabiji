#!/usr/bin/env python3
"""
Generate sydney-nz-data.json for a 46-day Australia + New Zealand trip.
May 3 – Jun 17, 2026 | 2 travelers | Vegetarian | $2-5k budget
"""
import json
from datetime import date, timedelta

START = date(2026, 5, 3)

def fmt_date(d):
    return d.strftime("%A, %B %-d")

def pin(lat, lng, label, num, cat="attraction", desc=""):
    return {"lat": lat, "lng": lng, "label": label, "num": num, "cat": cat, "desc": desc or label}

def act(title, desc, details=None):
    return {"title": title, "description": desc, "details": details or []}

def meal(t, name, desc, meta=""):
    return {"type": t, "name": name, "description": desc, "meta": meta}

def tip(text):
    return {"type": "tip", "text": text}

def tb(label, activities=None, meals=None, tips=None):
    return {"label": label, "activities": activities or [], "meals": meals or [], "tips": tips or []}

def day(num, title, neighborhoods, desc, timeblocks, mappins):
    return {
        "num": num, "title": title, "neighborhoods": neighborhoods,
        "description": desc, "timeBlocks": timeblocks, "mapPins": mappins
    }

days = []

# ═══════════════════════════════════════
# DAYS 1-3: SYDNEY (May 3-5)
# ═══════════════════════════════════════

days.append(day(1, "Sydney Arrival & Harbour Icons", "Circular Quay · The Rocks · Sydney CBD",
    "Touch down in Sydney and experience the world-famous harbour. Walk from the Opera House to the Harbour Bridge as the city lights up.",
    [
        tb("Morning — Arrival & Settle In",
            [act("✈️ Arrive in Sydney", "Check into accommodation near Circular Quay or the CBD. Grab a flat white and get your bearings.",
                ["📍 Sydney CBD / Circular Quay", "💡 Opal card for all public transport — daily cap ~$17.80", "💰 Airport to city: Train $19"])],
            [meal("Breakfast", "Local Café Flat White & Avo Toast", "Sydney practically invented avocado toast. Any café near your hotel will do it justice.", "💰 $12-18/person")],
            [tip("💡 Opal card has daily ($17.80) and weekly ($50) caps. Sundays capped at $2.90!")]),
        tb("Afternoon — Circular Quay & The Rocks",
            [act("🎵 Sydney Opera House", "Walk around the exterior and Bennelong Point. The sails change colour with the light. Consider a guided tour ($43) or just soak it in from the harbour walkway.",
                ["📍 Bennelong Point · Exterior FREE, tours from $43", "💡 Best photo angle: Mrs Macquarie's Chair (20-min walk east)"]),
             act("🪨 The Rocks", "Sydney's oldest neighbourhood. Cobblestone lanes, heritage pubs, weekend markets. Wander Nurses Walk and find street art in laneways.",
                ["📍 The Rocks · FREE to explore", "🛍️ The Rocks Markets (weekends): handmade goods, street food, live music"])],
            [meal("Lunch", "Vegetarian at The Rocks", "Pancakes on the Rocks does great veggie options. Or grab falafel from the market stalls on weekends.", "💰 $15-22/person")]),
        tb("Evening — Harbour Bridge & Sunset",
            [act("🌉 Sydney Harbour Bridge Walk", "Walk across the bridge for jaw-dropping views of the Opera House and harbour. Free pedestrian walkway from The Rocks side — 20 min each way.",
                ["📍 Cumberland St, The Rocks · FREE to walk", "🌅 Golden hour = best Opera House photos"])],
            [meal("Dinner", "Bodhi Restaurant (Vegetarian Yum Cha)", "All-vegetarian/vegan yum cha under fig trees in Cook + Phillip Park. A Sydney institution — the 'duck' pancakes and dumplings are legendary.", "📍 2-4 College St · 💰 $25-35/person")],
            [tip("💡 Walk back via Circular Quay for the Opera House lit up at night. Completely different, magical vibe.")])
    ],
    [pin(-33.8568, 151.2153, "Sydney Opera House", 1), pin(-33.8599, 151.2090, "The Rocks", 2),
     pin(-33.8523, 151.2108, "Sydney Harbour Bridge", 3), pin(-33.8730, 151.2130, "Bodhi Restaurant", 4, "food", "Vegetarian yum cha")]
))

days.append(day(2, "Bondi to Coogee & Inner West Vibes", "Bondi · Coogee · Newtown · Surry Hills",
    "Walk Australia's most famous coastal trail from Bondi to Coogee, then explore Sydney's coolest inner-city neighbourhoods for vintage shops, street art, and incredible vegetarian food.",
    [
        tb("Morning — Bondi to Coogee Coastal Walk",
            [act("🏖️ Bondi to Coogee Coastal Walk", "The most spectacular urban walk in Australia. 6 km along dramatic cliffs through Tamarama, Bronte, and Clovelly beaches. Each beach has its own personality.",
                ["📍 Start Bondi Beach (bus 333) · FREE · ~2 hours", "💡 Start early (8-9 AM) to beat crowds", "📸 Bondi Icebergs pool from above = iconic shot"])],
            [meal("Breakfast", "Bondi Café Scene", "Porch and Parlour or Speedos Café on the beach. Acai bowls, smoothies, best people-watching in Sydney.", "💰 $15-22/person")],
            [tip("💡 May is autumn — pleasant 18-22°C but UV is still strong. Sunscreen essential.")]),
        tb("Afternoon — Newtown & Inner West",
            [act("🎨 Newtown — King Street", "Sydney's bohemian heart. Packed with vintage shops, record stores, bookshops, and the best vegetarian restaurants in the city. Street art everywhere.",
                ["📍 King St, Newtown · Train to Newtown station · FREE", "🛍️ Cream on King, Route 66, Better Read Than Dead bookshop"]),
             act("🌿 Surry Hills", "Sydney's foodie capital. Crown and Bourke Streets lined with cafés, bars, and boutiques.", ["📍 Crown St / Bourke St · Walk or bus from Newtown"])],
            [meal("Lunch", "Lentil as Anything (Newtown)", "Pay-what-you-feel vegetarian restaurant. Amazing curries, salads, baked goods. A community institution.", "📍 391 King St · 💰 Pay what you feel"),
             meal("Dinner", "Yellow (Potts Point)", "All-vegetarian fine dining by Chef Brent Savage. Multi-course tasting menu with native Australian ingredients. Unforgettable.", "📍 57 Macleay St · 💰 $85-120/person tasting menu")],
            [tip("💡 Newtown has the densest concentration of vegetarian/vegan restaurants in Sydney.")])
    ],
    [pin(-33.8915, 151.2767, "Bondi Beach", 1), pin(-33.9193, 151.2578, "Coogee Beach", 2),
     pin(-33.8976, 151.1790, "Newtown", 3), pin(-33.8785, 151.2268, "Yellow Restaurant", 4, "food")]
))

days.append(day(3, "Blue Mountains — Three Sisters & Ancient Rainforest", "Katoomba · Leura · Blue Mountains NP",
    "One of Australia's most dramatic landscapes. Plunging valleys, eucalyptus-hazed peaks, the iconic Three Sisters, and walks through ancient rainforest — all just 2 hours from Sydney.",
    [
        tb("Morning — Three Sisters & Echo Point",
            [act("🏔️ Three Sisters at Echo Point", "Three towering sandstone pillars rising from the Jamison Valley. In Gundungurra Dreaming, three women turned to stone. The viewing platform is breathtaking.",
                ["📍 Echo Point, Katoomba · FREE · Train ~2hrs from Central", "💡 First train ~6 AM for no crowds", "🌿 The blue haze = eucalyptus oil refracting light"])],
            [meal("Breakfast", "Katoomba Cafés", "Grab something at Katoomba station cafés. Bring snacks from Sydney for the walks.", "💰 $8-15/person")],
            [tip("💡 May in the Blue Mountains = 8-15°C. Bring layers — the valley is 5°C cooler than Sydney.")]),
        tb("Midday — Scenic World & Rainforest",
            [act("🚡 Scenic World", "Three rides: Scenic Railway (world's steepest at 52°), Skyway (cable car across canyon), Cableway. The Scenic Walkway at the bottom goes through Jurassic-era rainforest.",
                ["📍 Violet St, Katoomba · Unlimited pass $53/adult", "💡 The rainforest boardwalk alone is worth the ticket"]),
             act("🌲 Prince Henry Cliff Walk", "Free cliff-top trail from Echo Point to Scenic World along the escarpment with valley views at every turn. ~2 km, easy grade.",
                ["📍 Echo Point to Scenic World · FREE · ~45 min"])],
            [meal("Lunch", "Leura Village", "Cute sister-town to Katoomba. Lovely cafés, plenty of veggie options. Silks Brasserie or Solitary for views.", "📍 Leura Mall · 💰 $18-30/person")]),
        tb("Afternoon — Return",
            [act("🌺 Leura Cascades", "Short walk to gentle waterfalls in ferny bushland, then browse the charming village.", ["📍 Leura · FREE · Last express train ~5:30 PM"])],
            [meal("Dinner", "Chat Thai (Sydney CBD)", "Back in Sydney. Excellent Thai — vegetarian curries, pad thai, papaya salad.", "📍 20 Campbell St · 💰 $15-22/person")])
    ],
    [pin(-33.7320, 150.3121, "Three Sisters", 1), pin(-33.7292, 150.3014, "Scenic World", 2), pin(-33.7152, 150.3364, "Leura", 3)]
))

# ═══════════════════════════════════════
# DAYS 4-6: AUCKLAND, NZ (May 6-8)
# ═══════════════════════════════════════

days.append(day(4, "Fly to Auckland — City of Sails", "Auckland CBD · Viaduct Harbour · Ponsonby",
    "Fly across the Tasman to Aotearoa. Auckland is built on 53 volcanoes between two harbours. Settle in and explore the city of sails.",
    [
        tb("Morning — Flight to Auckland",
            [act("✈️ Sydney → Auckland", "~3-hour flight across the Tasman. NZ is 2 hours ahead of Sydney. Arrive early afternoon.",
                ["📍 SYD → AKL · ~3 hrs · Budget from ~$150 one-way", "💡 NZ biosecurity is strict — declare all food", "⏰ NZ is UTC+12"])],
            tips=[tip("💡 NZ uses contactless everywhere. AT HOP card for Auckland transport or just tap your card.")]),
        tb("Afternoon — Viaduct & Ponsonby",
            [act("⛵ Viaduct Harbour", "Auckland's waterfront. America's Cup territory. Restaurants, superyachts, and the Wynyard Quarter boardwalk to Silo Park.",
                ["📍 Viaduct Harbour · FREE", "🛥️ 'City of Sails' — more boats per capita than anywhere"]),
             act("🌿 Ponsonby Road", "Auckland's most fashionable street. Boutiques, vintage stores, cafés, and excellent restaurants.",
                ["📍 Ponsonby Rd · 20-min walk from CBD"])],
            [meal("Late Lunch", "Viaduct Cafés", "Fresh vegetarian options at the Viaduct restaurants.", "💰 $18-28/person"),
             meal("Dinner", "The Blue Breeze Inn (Ponsonby)", "Incredible Asian-fusion with amazing veggie options — the tofu bao is famous.", "📍 Ponsonby Rd · 💰 $22-35/person")])
    ],
    [pin(-36.8435, 174.7555, "Viaduct Harbour", 1), pin(-36.8584, 174.7394, "Ponsonby Road", 2)]
))

days.append(day(5, "Auckland Volcanoes & Harbour", "Rangitoto · Devonport · Mount Eden",
    "Climb a volcanic island, explore the charming village of Devonport, and summit Mount Eden for 360° views. Auckland's natural drama on full display.",
    [
        tb("Morning — Rangitoto Island",
            [act("🌋 Rangitoto Island", "Auckland's youngest volcano. Ferry to the island, walk through lava fields and native bush to the summit (260m). Spectacular 360° views of Auckland and the Hauraki Gulf.",
                ["📍 Ferry from downtown · ~25 min · $40 return", "⏱️ Summit: ~1 hr each way", "🌿 World's largest pōhutukawa forest", "💡 Bring water — no shops on island"])],
            [meal("Breakfast", "Waterfront Café", "Flat white and pastry before the 9:15 AM ferry.", "💰 $10-15/person")],
            [tip("💡 Rangitoto erupted just 600 years ago — Māori witnessed it. The lava caves near the summit are worth exploring.")]),
        tb("Afternoon — Devonport & Mount Eden",
            [act("⚓ Devonport Village", "Charming harbourside village with Victorian buildings, bookshops, and cafés. Walk up North Head for WWII tunnels and harbour views.",
                ["📍 Ferry from CBD · ~12 min · $7.50 return", "💡 North Head tunnels are free to explore"]),
             act("🏔️ Maungawhau / Mount Eden", "Auckland's highest natural point (196m). Perfect green volcanic crater bowl. Walk the rim at sunset for the best city views.",
                ["📍 Mount Eden Rd · FREE", "⚠️ Stay on paths — the crater is tapu (sacred), do not enter"])],
            [meal("Lunch", "Devonport Cafés", "Charming cafés along Victoria Road.", "💰 $15-22/person"),
             meal("Dinner", "Mount Eden Village", "Farro for wholesome vegetarian bowls or a local sushi spot.", "💰 $18-28/person")])
    ],
    [pin(-36.7862, 174.8600, "Rangitoto Island", 1), pin(-36.8317, 174.7943, "Devonport", 2), pin(-36.8764, 174.7645, "Mount Eden", 3)]
))

days.append(day(6, "Family Heritage & Auckland Museum", "Auckland Cemetery · Auckland Domain · Parnell",
    "A deeply personal day. Visit your great grandfather's grave — a moment of connection across generations. Then explore Auckland Museum's extraordinary Māori and Pacific collections.",
    [
        tb("Morning — Great Grandfather's Grave",
            [act("🪦 Visit Great Grandfather's Grave", "A personal pilgrimage. Take your time. Bring flowers — a simple gesture connecting you across generations. This is the kind of moment that makes travel meaningful beyond the sights.",
                ["💡 Research cemetery location beforehand — Auckland has several: Waikumete, Purewa, Symonds St", "🕊️ Auckland Council cemetery search: aucklandcouncil.govt.nz/cemeteries", "💐 Florists: Wild Poppies (Ponsonby) or any supermarket"])],
            [meal("Breakfast", "Local Café", "Keep the morning gentle.", "💰 $10-15/person")],
            [tip("🕊️ Auckland Libraries have excellent genealogy resources if you need help locating the grave.")]),
        tb("Afternoon — Auckland Museum & Domain",
            [act("🏛️ Auckland War Memorial Museum", "Three floors: natural history (moa skeleton!), Māori and Pacific cultures (stunning carved meeting house), and war memorials. The Māori cultural performance is powerful.",
                ["📍 Auckland Domain · $28 for international visitors (includes Māori performance)", "💡 The carved wharenui (meeting house) is extraordinary"]),
             act("🌸 Auckland Domain & Winter Gardens", "Auckland's oldest park with ancient pōhutukawa trees. Two free glasshouses — tropical and temperate.",
                ["📍 Auckland Domain · FREE · 9 AM-5:30 PM"])],
            [meal("Lunch", "Parnell Village", "Auckland's oldest suburb. Rosie café does great vegetarian lunch bowls. European village feel.", "📍 Parnell Rd · 💰 $16-24/person"),
             meal("Dinner", "K' Road (Karangahape Road)", "Auckland's most eclectic street. Coco's Cantina for Italian-NZ veggie pasta.", "📍 K' Road · 💰 $20-32/person")],
            [tip("💡 K' Road is Auckland's creative heart — street art, record shops, vintage stores. Worth a wander after dinner.")])
    ],
    [pin(-36.8605, 174.7763, "Auckland Museum", 1), pin(-36.8580, 174.7780, "Auckland Domain", 2), pin(-36.8546, 174.7833, "Parnell", 3, "food")]
))

# ═══════════════════════════════════════
# DAYS 7-12: WELLINGTON (May 9-14)
# ═══════════════════════════════════════

days.append(day(7, "Auckland to Wellington — Coolest Little Capital", "Wellington CBD · Te Aro · Cuba Street",
    "Travel south to New Zealand's capital — the coolest little capital in the world. Compact, creative, packed with character. Think Melbourne vibes in a harbour-and-hills setting.",
    [
        tb("Morning — Travel to Wellington",
            [act("✈️ Auckland → Wellington", "1-hour flight (from ~$60 on Jetstar). Wellington Airport is tiny and right in the city.",
                ["📍 AKL → WLG · ~1 hr", "🚌 Airport Express $12 or Uber ~$25 to CBD"])],
            tips=[tip("💡 Wellington is WINDY. Not a joke. Pack a windproof layer.")]),
        tb("Afternoon — Cuba Street & Cable Car",
            [act("🎭 Cuba Street", "Wellington's bohemian artery. Buskers, vintage stores, record shops, craft beer. The bucket fountain is the most Wellington thing ever — just buckets tipping water. Locals adore it.",
                ["📍 Cuba St, Te Aro · FREE", "☕ Best coffee in NZ: Flight Coffee, Customs, or Lamason"]),
             act("🚋 Wellington Cable Car", "Ride from Lambton Quay to the Botanic Garden. Panoramic views and gorgeous gardens at the top.",
                ["📍 280 Lambton Quay · $5 one-way, $10 return", "🌿 Walk down through Botanic Garden (free)"])],
            [meal("Lunch", "Cuba St — Ombra or Fidel's", "Ombra for Italian vegetarian, Fidel's for Cuban-NZ fusion in a Che Guevara-themed café.", "📍 Cuba St · 💰 $16-25/person"),
             meal("Dinner", "Loretta", "Outstanding vegetarian dishes in a beautiful Cuba St space.", "💰 $25-40/person")],
            [tip("💡 Wellington's craft beer: Garage Project (Aro Valley) and Parrotdog (Lyall Bay) are world-class.")])
    ],
    [pin(-41.2924, 174.7787, "Cuba Street", 1), pin(-41.2852, 174.7707, "Cable Car", 2)]
))

days.append(day(8, "Te Papa & Wellington Waterfront", "Wellington Waterfront · Mt Victoria · Oriental Bay",
    "Dive into Te Papa — one of the world's great museums — then climb Mt Victoria for the Lord of the Rings hobbit-hideout views. Wellington packs more culture per square metre than cities ten times its size.",
    [
        tb("Morning — Te Papa Tongarewa",
            [act("🏛️ Te Papa Tongarewa", "New Zealand's national museum. Six floors of Māori treasures, natural history (the colossal squid!), NZ art, and immersive earthquake simulator. FREE and absolutely world-class.",
                ["📍 55 Cable St, Waterfront · FREE (some exhibitions charged)", "💡 The colossal squid specimen is the only one on display in the world", "⏱️ Allow 3-4 hours minimum"])],
            [meal("Breakfast", "Prefab Eatery", "Wellington's beloved café. Great flat whites and vegetarian brunch options.", "📍 14 Jessie St · 💰 $14-20/person")]),
        tb("Afternoon — Mt Victoria & Oriental Bay",
            [act("🏔️ Mount Victoria Lookout", "The panoramic view from the top takes in the entire city, harbour, and on clear days, the South Island. Peter Jackson filmed hobbit-hiding scenes from LOTR right here.",
                ["📍 Lookout Rd · FREE · 30-min walk from CBD or drive/bus", "🎬 Lord of the Rings filming location — hobbits hid from the Nazgûl here"]),
             act("🏖️ Oriental Bay", "Wellington's city beach. A gentle curved bay with golden sand (imported from Golden Bay!). Walk the promenade, swim if you're brave (it's May).",
                ["📍 Oriental Parade · FREE"])],
            [meal("Lunch", "Te Papa Café or Waterfront", "Te Papa's café has great views and veggie options. Or walk along the waterfront to one of many restaurants.", "💰 $16-25/person"),
             meal("Dinner", "Aro Valley — Aro Café or Sweet Mother's Kitchen", "Aro Café for wholesome vegetarian. Sweet Mother's for Cajun-Southern comfort food with great veggie options.", "💰 $20-32/person")],
            [tip("💡 If the weather is clear, the sunset from Oriental Bay facing the harbour is magical.")])
    ],
    [pin(-41.2905, 174.7820, "Te Papa Museum", 1), pin(-41.2964, 174.7933, "Mt Victoria Lookout", 2), pin(-41.2881, 174.7888, "Oriental Bay", 3)]
))

days.append(day(9, "Wellington: Weta Workshop & South Coast", "Miramar · Lyall Bay · Red Rocks",
    "Visit the legendary Weta Workshop where Lord of the Rings, Avatar, and more were brought to life. Then explore Wellington's wild south coast — seal colonies and rugged coastline.",
    [
        tb("Morning — Weta Workshop",
            [act("🎬 Weta Workshop Unleashed", "The creative powerhouse behind LOTR, The Hobbit, Avatar, and more. Interactive exhibits, miniatures, costumes, and props. Even if you're not a mega-fan, the craftsmanship is mind-blowing.",
                ["📍 1 Weka St, Miramar · $49/adult for Unleashed experience", "💡 Book ahead — this is Wellington's #1 attraction", "⏱️ Allow 2-3 hours"])],
            [meal("Breakfast", "Miramar — Roxy Cinema Café", "Beautiful art deco cinema with a café. Great coffee and pastries.", "📍 5 Park Rd, Miramar · 💰 $12-18/person")]),
        tb("Afternoon — South Coast & Red Rocks",
            [act("🦭 Red Rocks Seal Colony", "Walk along the wild south coast to a New Zealand fur seal colony. The red-coloured rocks are volcanic, the coastline is dramatic, and the seals are delightfully unbothered by visitors.",
                ["📍 Red Rocks, Owhiro Bay · FREE · ~45 min walk from car park", "🦭 Best May-Oct when seals haul out in larger numbers", "💡 The walk is flat but exposed — windproof layer essential"]),
             act("🌊 Lyall Bay", "Wellington's surfing beach. Rough, windswept, and very Wellington. Great for a wild coastal walk even if you don't surf.",
                ["📍 Lyall Bay · FREE"])],
            [meal("Lunch", "Lyall Bay — Maranui Café", "Perched above the surf club with ocean views. Outstanding vegetarian options and Wellington's best scones.", "📍 7 Lyall Parade · 💰 $16-24/person"),
             meal("Dinner", "Courtenay Place", "Wellington's entertainment district. Plenty of vegetarian-friendly restaurants. Try the Green Man's Arms for pub food with great veggie options.", "💰 $20-30/person")],
            [tip("💡 The Wellington south coast feels like a completely different world from the city — wild, windswept, and dramatic.")])
    ],
    [pin(-41.3114, 174.8262, "Weta Workshop", 1), pin(-41.3480, 174.7340, "Red Rocks", 2), pin(-41.3280, 174.7920, "Lyall Bay", 3)]
))

days.append(day(10, "Wellington: Zealandia & Kapiti Coast", "Zealandia · Karori · Kapiti Island (optional)",
    "Discover a world that existed before humans arrived. Zealandia is a predator-free ecosanctuary where kiwi, tuatara, and species thought extinct are thriving. New Zealand conservation at its most hopeful.",
    [
        tb("Morning — Zealandia Ecosanctuary",
            [act("🥝 Zealandia Te Māra a Tāne", "A 225-hectare predator-fenced valley in the middle of Wellington. Home to kiwi, tuatara, takahē, hihi, and more. Walking through ancient forest where these creatures roam free is profoundly moving.",
                ["📍 53 Waiapu Rd, Karori · $24/adult · Opens 9 AM", "🥝 Night tours ($89) for kiwi sightings — book well ahead", "💡 Tuatara are 'living fossils' — unchanged for 200 million years", "⏱️ Allow 2-3 hours for the valley walk"])],
            [meal("Breakfast", "Karori — Café One80", "Community café near Zealandia. Good flat whites and toasties.", "💰 $10-16/person")],
            [tip("💡 Zealandia's success story: kiwi are now breeding in suburban Wellington for the first time in 100+ years thanks to this sanctuary.")]),
        tb("Afternoon — Free Time / Kapiti Coast",
            [act("🌊 Kapiti Coast (Optional Day Trip)", "If you fancy a drive, Kapiti Coast (~45 min north) has the Kapiti Island nature reserve (DOC permit needed, limited to 100 visitors/day), Paraparaumu Beach, and the lovely town of Ōtaki.",
                ["📍 Kapiti Coast · ~45 min drive north", "💡 Kapiti Island: book DOC permits weeks ahead"]),
             act("🛍️ Or: Wellington Free Afternoon", "Revisit Cuba Street, browse the indie bookshops (Unity, Arty Bees), vintage stores, or catch a movie at the art deco Embassy Theatre.",
                ["📍 Various Wellington locations · FREE to browse"])],
            [meal("Lunch", "Karori or CBD", "Light lunch near Zealandia or back in the CBD.", "💰 $14-22/person"),
             meal("Dinner", "Husk (Cuba Street)", "Vegetarian-friendly with creative cocktails and a great atmosphere.", "💰 $22-35/person")])
    ],
    [pin(-41.2905, 174.7530, "Zealandia", 1), pin(-40.9140, 174.9815, "Kapiti Island", 2)]
))

days.append(day(11, "Wellington: Conference Day 1 & Evening Exploration", "Wellington CBD · Lambton Quay · Te Aro",
    "Conference day. Attend sessions, network, then reward yourselves with Wellington's excellent evening dining scene.",
    [
        tb("Morning & Afternoon — Conference Day 1",
            [act("📋 Wellington Conference — Day 1", "Full day of conference sessions. Wellington's compact size means your venue is likely walking distance from everything.",
                ["📍 Conference venue (TBC)", "💡 Wellington CBD is tiny — everything is within 15-min walk"])],
            [meal("Breakfast", "Hotel or Nearby Café", "Quick breakfast before conference sessions.", "💰 $10-15/person"),
             meal("Lunch", "Conference Provided or Nearby", "Most Wellington conferences cater lunch. If not, dozens of great options within 5 min walk.", "💰 $12-20/person")]),
        tb("Evening — Post-Conference Exploration",
            [act("🍷 Wellington Bar Scene", "Wellington has more bars and restaurants per capita than New York. Hit up Havana (Cuba St), The Library (cocktails), or Golding's Free Dive (craft beer + vegetarian pizza).",
                ["📍 Various, mostly Cuba St / Courtenay Place area", "🍺 Golding's does excellent vegan pizza"])],
            [meal("Dinner", "Logan Brown", "One of Wellington's finest restaurants in a stunning heritage building. Excellent vegetarian tasting menu. A conference-night treat.", "📍 192 Cuba St · 💰 $40-65/person")])
    ],
    [pin(-41.2889, 174.7772, "Wellington CBD", 1), pin(-41.2924, 174.7787, "Cuba Street", 2)]
))

days.append(day(12, "Wellington: Conference Day 2 & Farewell NZ", "Wellington CBD · Airport",
    "Final conference day and last night in Aotearoa. Soak in the last of Wellington's magic before tomorrow's flight back to Australia.",
    [
        tb("Morning & Afternoon — Conference Day 2",
            [act("📋 Wellington Conference — Day 2", "Second and final day of conference sessions. Make the most of networking and connections.",
                ["📍 Conference venue (TBC)"])],
            [meal("Breakfast", "Café near venue", "Quick fuel before sessions.", "💰 $10-15/person"),
             meal("Lunch", "Conference or CBD", "Grab lunch between sessions.", "💰 $12-20/person")]),
        tb("Evening — Farewell Wellington",
            [act("🌅 Sunset Walk — Oriental Bay to CBD", "A farewell stroll along Wellington's waterfront. The harbour at dusk, with the hills lit up, is the perfect goodbye.",
                ["📍 Oriental Parade → Te Papa → Cuba