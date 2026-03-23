#!/usr/bin/env python3
"""
Generate sydney-nz-data.json — 46 day Australia + NZ trip
May 3 – Jun 17, 2026
Writes directly to sydney-nz-data.json
"""
import json, os, sys

# Helper constructors
def P(lat, lng, label, n, cat="attraction", desc=""):
    return {"lat":lat,"lng":lng,"label":label,"num":n,"cat":cat,"desc":desc or label}
def A(title, desc, det=None):
    return {"title":title,"description":desc,"details":det or []}
def M(t, name, desc, meta=""):
    return {"type":t,"name":name,"description":desc,"meta":meta}
def T(text):
    return {"type":"tip","text":text}
def TB(label, acts=None, meals=None, tips=None):
    return {"label":label,"activities":acts or [],"meals":meals or [],"tips":tips or []}
def D(num, title, hoods, desc, tbs, pins):
    return {"num":num,"title":title,"neighborhoods":hoods,"description":desc,"timeBlocks":tbs,"mapPins":pins}

days = []

#===== DAY 1: May 3 — Sydney Arrival =====
days.append(D(1,"Sydney Arrival & Harbour Icons","Circular Quay · The Rocks · Sydney CBD",
"Touch down in Sydney and experience the world-famous harbour. Walk from the Opera House to the Harbour Bridge as the city lights up.",
[TB("Morning — Arrival & Settle In",
    [A("✈️ Arrive in Sydney","Check into accommodation near Circular Quay or the CBD. Grab a flat white and get your bearings.",
       ["📍 Sydney CBD / Circular Quay","💡 Opal card: daily cap ~$17.80, weekly $50, Sunday $2.90","💰 Airport train $19"])],
    [M("Breakfast","Flat White & Avo Toast","Sydney's café culture is legendary. Any local café does avocado toast justice.","💰 $12-18/person")],
    [T("💡 Opal card Sunday cap ($2.90) = perfect for exploring on a budget!")]),
 TB("Afternoon — Opera House & The Rocks",
    [A("🎵 Sydney Opera House","Walk around the exterior at Bennelong Point. The sails change colour with the light. Consider a guided tour ($43) or soak it in free from the harbour walkway.",
       ["📍 Bennelong Point · Exterior FREE, tours $43","💡 Best photo: Mrs Macquarie's Chair (20-min walk east)"]),
     A("🪨 The Rocks","Sydney's oldest neighbourhood. Cobblestone lanes, heritage pubs, weekend markets. Wander Nurses Walk and find street art tucked in laneways.",
       ["📍 The Rocks · FREE","🛍️ Rocks Markets (Sat-Sun): handmade goods, street food, live music"])],
    [M("Lunch","The Rocks Vegetarian","Pancakes on the Rocks for veggie options, or falafel from weekend market stalls.","💰 $15-22/person")]),
 TB("Evening — Harbour Bridge Sunset",
    [A("🌉 Sydney Harbour Bridge Walk","Walk across for jaw-dropping Opera House views. Free pedestrian walkway from The Rocks side — 20 min each way.",
       ["📍 Cumberland St, The Rocks · FREE","🌅 Golden hour = best Opera House photos"])],
    [M("Dinner","Bodhi Restaurant","All-vegetarian yum cha under fig trees in Cook + Phillip Park. A Sydney institution — 'duck' pancakes and dumplings are legendary.","📍 2-4 College St · 💰 $25-35/person")],
    [T("💡 Walk back via Circular Quay for the Opera House lit up at night. Magical.")])],
[P(-33.8568,151.2153,"Sydney Opera House",1),P(-33.8599,151.2090,"The Rocks",2),P(-33.8523,151.2108,"Harbour Bridge",3),P(-33.8730,151.2130,"Bodhi Restaurant",4,"food")]))

#===== DAY 2: May 4 — Bondi & Inner West =====
days.append(D(2,"Bondi to Coogee & Inner West","Bondi · Coogee · Newtown · Surry Hills",
"Walk Australia's most famous coastal trail, then explore Sydney's coolest neighbourhoods for vintage shops, street art, and incredible vegetarian food.",
[TB("Morning — Bondi to Coogee Coastal Walk",
    [A("🏖️ Bondi to Coogee Walk","6 km along dramatic cliffs through Tamarama, Bronte, and Clovelly beaches. The most spectacular urban walk in Australia.",
       ["📍 Start Bondi Beach (bus 333) · FREE · ~2 hours","📸 Bondi Icebergs pool from above = iconic shot","💡 Start 8-9 AM to beat crowds"])],
    [M("Breakfast","Bondi Café Scene","Porch and Parlour or Speedos Café on the beach. Acai bowls and best people-watching.","💰 $15-22/person")],
    [T("💡 May is autumn — pleasant 18-22°C but UV still strong. Sunscreen essential.")]),
 TB("Afternoon — Newtown & Dinner",
    [A("🎨 Newtown — King Street","Sydney's bohemian heart. Vintage shops, record stores, bookshops, and the densest concentration of vegetarian restaurants in the city.",
       ["📍 King St · Train to Newtown · FREE","🛍️ Cream on King, Route 66, Better Read Than Dead bookshop"])],
    [M("Lunch","Lentil as Anything","Pay-what-you-feel vegetarian restaurant. Amazing curries, salads, baked goods.","📍 391 King St · 💰 Pay what you feel"),
     M("Dinner","Yellow (Potts Point)","All-vegetarian fine dining. Multi-course tasting menu with native Australian ingredients. Unforgettable.","📍 57 Macleay St · 💰 $85-120/person tasting menu")],
    [T("💡 Newtown has the densest concentration of vegetarian/vegan restaurants in Sydney.")])],
[P(-33.8915,151.2767,"Bondi Beach",1),P(-33.9193,151.2578,"Coogee Beach",2),P(-33.8976,151.1790,"Newtown",3),P(-33.8785,151.2268,"Yellow",4,"food")]))

#===== DAY 3: May 5 — Blue Mountains =====
days.append(D(3,"Blue Mountains — Three Sisters & Rainforest","Katoomba · Leura · Blue Mountains NP",
"One of Australia's most dramatic landscapes. Plunging valleys, eucalyptus-hazed peaks, the iconic Three Sisters, and ancient rainforest — 2 hours from Sydney.",
[TB("Morning — Three Sisters",
    [A("🏔️ Three Sisters at Echo Point","Three sandstone pillars rising from Jamison Valley. In Gundungurra Dreaming, three women turned to stone. Breathtaking.",
       ["📍 Echo Point, Katoomba · FREE · Train ~2hrs from Central","🌿 Blue haze = eucalyptus oil refracting light"])],
    [M("Breakfast","Katoomba Cafés","Grab something near the station or bring snacks from Sydney.","💰 $8-15/person")],
    [T("💡 May = 8-15°C in the mountains. Bring layers!")]),
 TB("Midday — Scenic World & Rainforest",
    [A("🚡 Scenic World","Scenic Railway (world's steepest, 52°), Skyway, and Cableway. The boardwalk at the bottom goes through Jurassic-era rainforest.",
       ["📍 Violet St, Katoomba · $53/adult unlimited pass","💡 Rainforest boardwalk alone worth the ticket"])],
    [M("Lunch","Leura Village","Cute mountain village with lovely cafés and veggie options.","📍 Leura Mall · 💰 $18-30/person")]),
 TB("Afternoon — Return to Sydney",
    [A("🌺 Leura Cascades","Short walk to gentle waterfalls in ferny bushland, then browse the village.",["📍 Leura · FREE"])],
    [M("Dinner","Chat Thai (Sydney CBD)","Back in Sydney. Excellent vegetarian Thai curries and pad thai.","📍 20 Campbell St · 💰 $15-22/person")])],
[P(-33.7320,150.3121,"Three Sisters",1),P(-33.7292,150.3014,"Scenic World",2),P(-33.7152,150.3364,"Leura",3)]))

#===== DAY 4: May 6 — Fly to Auckland =====
days.append(D(4,"Fly to Auckland — City of Sails","Auckland CBD · Viaduct Harbour · Ponsonby",
"Fly across the Tasman to Aotearoa. Auckland — built on 53 volcanoes between two harbours. Settle in and explore the city of sails.",
[TB("Morning — Flight",
    [A("✈️ Sydney → Auckland","~3-hour flight. NZ is 2 hours ahead. Arrive early afternoon.",
       ["📍 SYD → AKL · ~3 hrs · From ~$150","💡 NZ biosecurity strict — declare all food","⏰ NZ = UTC+12"])],
    tips=[T("💡 AT HOP card for Auckland transport, or just tap contactless.")]),
 TB("Afternoon — Viaduct & Ponsonby",
    [A("⛵ Viaduct Harbour","Waterfront precinct. America's Cup territory. Walk the Wynyard Quarter boardwalk to Silo Park.",
       ["📍 Viaduct Harbour · FREE","🛥️ More boats per capita than anywhere on earth"]),
     A("🌿 Ponsonby Road","Auckland's most fashionable street. Boutiques, vintage, cafés, restaurants.",
       ["📍 Ponsonby Rd · 20-min walk from CBD"])],
    [M("Late Lunch","Viaduct Cafés","Fresh vegetarian options at waterfront restaurants.","💰 $18-28/person"),
     M("Dinner","Blue Breeze Inn","Incredible Asian-fusion — the tofu bao is famous.","📍 Ponsonby Rd · 💰 $22-35/person")])],
[P(-36.8435,174.7555,"Viaduct Harbour",1),P(-36.8584,174.7394,"Ponsonby",2)]))

#===== DAY 5: May 7 — Auckland Volcanoes =====
days.append(D(5,"Auckland Volcanoes & Harbour","Rangitoto · Devonport · Mount Eden",
"Climb a volcanic island, explore charming Devonport, and summit Mount Eden for 360° views.",
[TB("Morning — Rangitoto Island",
    [A("🌋 Rangitoto Island","Auckland's youngest volcano. Ferry, then walk through lava fields to the summit (260m). 360° views of the Gulf.",
       ["📍 Ferry from downtown · $40 return · ~25 min","⏱️ Summit: ~1 hr each way","🌿 World's largest pōhutukawa forest","💡 Bring water — no shops"])],
    [M("Breakfast","Waterfront Café","Flat white before the 9:15 AM ferry.","💰 $10-15/person")]),
 TB("Afternoon — Devonport & Mt Eden",
    [A("⚓ Devonport","Charming harbourside village. Victorian buildings, bookshops, cafés. Walk up North Head for WWII tunnels.",
       ["📍 Ferry ~12 min · $7.50 return","💡 North Head tunnels free to explore"]),
     A("🏔️ Maungawhau / Mount Eden","Auckland's highest natural point (196m). Walk the crater rim at sunset.",
       ["📍 Mt Eden Rd · FREE","⚠️ Crater is tapu (sacred) — stay on paths"])],
    [M("Lunch","Devonport Cafés","Victoria Road cafés.","💰 $15-22/person"),
     M("Dinner","Mount Eden Village","Farro for vegetarian bowls or local sushi.","💰 $18-28/person")])],
[P(-36.7862,174.8600,"Rangitoto",1),P(-36.8317,174.7943,"Devonport",2),P(-36.8764,174.7645,"Mount Eden",3)]))

#===== DAY 6: May 8 — Auckland Heritage =====
days.append(D(6,"Family Heritage & Auckland Museum","Auckland Domain · Parnell · K' Road",
"A deeply personal day. Visit your great grandfather's grave — a moment of connection across generations. Then Auckland Museum's extraordinary Māori collections.",
[TB("Morning — Great Grandfather's Grave",
    [A("🪦 Great Grandfather's Grave","A personal pilgrimage. Take your time. Bring flowers — connecting across generations. This makes travel meaningful beyond the sights.",
       ["💡 Auckland cemeteries: Waikumete, Purewa, Symonds St","🕊️ aucklandcouncil.govt.nz/cemeteries","💐 Florists or any supermarket"])],
    [M("Breakfast","Local Café","Keep the morning gentle.","💰 $10-15/person")],
    [T("🕊️ Auckland Libraries have excellent genealogy resources for locating graves.")]),
 TB("Afternoon — Auckland Museum",
    [A("🏛️ Auckland War Memorial Museum","Three floors: natural history, Māori & Pacific cultures (stunning carved meeting house), war memorials. Māori cultural performance included.",
       ["📍 Auckland Domain · $28 incl. Māori performance","💡 The carved wharenui is extraordinary"]),
     A("🌸 Auckland Domain & Winter Gardens","Oldest park with ancient trees. Two free glasshouses.",
       ["📍 Auckland Domain · FREE"])],
    [M("Lunch","Parnell Village","Auckland's oldest suburb. Great veggie lunch bowls.","📍 Parnell Rd · 💰 $16-24/person"),
     M("Dinner","K' Road","Auckland's eclectic street. Coco's Cantina for Italian-NZ veggie pasta.","📍 K' Road · 💰 $20-32/person")])],
[P(-36.8605,174.7763,"Auckland Museum",1),P(-36.8580,174.7780,"Auckland Domain",2),P(-36.8546,174.7833,"Parnell",3,"food")]))

#===== DAY 7: May 9 — Wellington Arrival =====
days.append(D(7,"Auckland to Wellington","Wellington CBD · Cuba Street · Lambton Quay",
"The coolest little capital in the world. Compact, creative, packed with character. Melbourne vibes in a harbour-and-hills setting.",
[TB("Morning — Flight",
    [A("✈️ Auckland → Wellington","1-hour flight from ~$60. Airport is tiny and central.",
       ["📍 AKL → WLG · ~1 hr","🚌 Airport Express $12 or Uber ~$25"])],
    tips=[T("💡 Wellington is WINDY. Pack a windproof layer.")]),
 TB("Afternoon — Cuba Street & Cable Car",
    [A("🎭 Cuba Street","Bohemian artery. Buskers, vintage, records, craft beer. The bucket fountain is the most Wellington thing ever.",
       ["📍 Cuba St · FREE","☕ Best NZ coffee: Flight Coffee, Customs, Lamason"]),
     A("🚋 Cable Car","Ride to Botanic Garden for panoramic views.",
       ["📍 280 Lambton Quay · $10 return","🌿 Walk down through Botanic Garden (free)"])],
    [M("Lunch","Cuba St — Fidel's","Cuban-NZ fusion in a Che Guevara-themed café.","📍 Cuba St · 💰 $16-25/person"),
     M("Dinner","Loretta","Outstanding vegetarian dishes in beautiful space.","💰 $25-40/person")])],
[P(-41.2924,174.7787,"Cuba Street",1),P(-41.2852,174.7707,"Cable Car",2)]))

#===== DAY 8: May 10 — Wellington Te Papa =====
days.append(D(8,"Te Papa & Wellington Waterfront","Wellington Waterfront · Mt Victoria · Oriental Bay",
"Te Papa — one of the world's great museums. Then climb Mt Victoria for Lord of the Rings views.",
[TB("Morning — Te Papa",
    [A("🏛️ Te Papa Tongarewa","NZ's national museum. Six floors: Māori treasures, colossal squid, earthquake simulator. FREE and world-class.",
       ["📍 55 Cable St · FREE","💡 Only colossal squid specimen on display in the world","⏱️ Allow 3-4 hours"])],
    [M("Breakfast","Prefab Eatery","Wellington's beloved café. Great veggie brunch.","📍 14 Jessie St · 💰 $14-20/person")]),
 TB("Afternoon — Mt Victoria & Oriental Bay",
    [A("🏔️ Mt Victoria Lookout","Panoramic view of city, harbour, and on clear days the South Island. Peter Jackson filmed hobbit-hiding LOTR scenes here.",
       ["📍 Lookout Rd · FREE · 30-min walk from CBD","🎬 Hobbits hid from the Nazgûl right here"]),
     A("🏖️ Oriental Bay","Wellington's city beach with imported golden sand. Walk the promenade.",
       ["📍 Oriental Parade · FREE"])],
    [M("Lunch","Waterfront","Te Papa café or nearby restaurants.","💰 $16-25/person"),
     M("Dinner","Sweet Mother's Kitchen","Cajun-Southern comfort food with great veggie options.","💰 $20-32/person")])],
[P(-41.2905,174.7820,"Te Papa",1),P(-41.2964,174.7933,"Mt Victoria",2),P(-41.2881,174.7888,"Oriental Bay",3)]))

#===== DAY 9: May 11 — Weta Workshop & South Coast =====
days.append(D(9,"Weta Workshop & South Coast","Miramar · Lyall Bay · Red Rocks",
"The creative powerhouse behind LOTR, Avatar, and more. Then Wellington's wild south coast — seal colonies and rugged coastline.",
[TB("Morning — Weta Workshop",
    [A("🎬 Weta Workshop Unleashed","Behind LOTR, Hobbit, Avatar. Interactive exhibits, miniatures, props. The craftsmanship is mind-blowing.",
       ["📍 1 Weka St, Miramar · $49/adult","💡 Book ahead — Wellington's #1 attraction","⏱️ 2-3 hours"])],
    [M("Breakfast","Roxy Cinema Café","Art deco cinema café in Miramar.","💰 $12-18/person")]),
 TB("Afternoon — Red Rocks & Seals",
    [A("🦭 Red Rocks Seal Colony","Walk the wild south coast to NZ fur seals. Volcanic red rocks, dramatic coastline, seals delightfully unbothered.",
       ["📍 Red Rocks, Owhiro Bay · FREE · ~45 min walk","🦭 Best May-Oct for seals","💡 Windproof layer essential"]),
     A("🌊 Lyall Bay","Wellington's surfing beach. Windswept and wild.",["📍 Lyall Bay · FREE"])],
    [M("Lunch","Maranui Café","Above the surf club with ocean views. Outstanding veggie options.","📍 7 Lyall Parade · 💰 $16-24/person"),
     M("Dinner","Courtenay Place","Entertainment district with plenty of veggie restaurants.","💰 $20-30/person")])],
[P(-41.3114,174.8262,"Weta Workshop",1),P(-41.3480,174.7340,"Red Rocks",2),P(-41.3280,174.7920,"Lyall Bay",3)]))

#===== DAY 10: May 12 — Zealandia =====
days.append(D(10,"Zealandia Ecosanctuary","Karori · Wellington CBD",
"A predator-free sanctuary where kiwi, tuatara, and species thought extinct are thriving. NZ conservation at its most hopeful.",
[TB("Morning — Zealandia",
    [A("🥝 Zealandia","225-hectare predator-fenced valley. Home to kiwi, tuatara, takahē. Walking through ancient forest where these creatures roam is profoundly moving.",
       ["📍 53 Waiapu Rd, Karori · $24/adult","🥝 Night tours ($89) for kiwi — book ahead","💡 Tuatara unchanged for 200 million years","⏱️ 2-3 hours"])],
    [M("Breakfast","Karori Café","Community café near Zealandia.","💰 $10-16/person")],
    [T("💡 Thanks to Zealandia, kiwi now breed in suburban Wellington for the first time in 100+ years.")]),
 TB("Afternoon — Free Time",
    [A("🛍️ Wellington at Leisure","Revisit Cuba Street, browse Unity Books & Arty Bees, or catch a movie at the art deco Embassy Theatre.",
       ["📍 Various · FREE to browse"])],
    [M("Lunch","CBD","Light lunch in the city.","💰 $14-22/person"),
     M("Dinner","Husk (Cuba Street)","Vegetarian-friendly with creative cocktails.","💰 $22-35/person")])],
[P(-41.2905,174.7530,"Zealandia",1),P(-41.2924,174.7787,"Cuba Street",2)]))

#===== DAY 11: May 13 — Conference Day 1 =====
days.append(D(11,"Conference Day 1","Wellington CBD",
"Conference day. Wellington's compact size means your venue is walking distance from everything.",
[TB("Daytime — Conference",
    [A("📋 Wellington Conference — Day 1","Full day of sessions and networking.",
       ["📍 Conference venue","💡 Wellington CBD is tiny — everything 15-min walk"])],
    [M("Breakfast","Hotel or Nearby","Quick fuel before sessions.","💰 $10-15/person"),
     M("Lunch","Conference or Nearby","Most Wellington conferences cater lunch.","💰 $12-20/person")]),
 TB("Evening — Post-Conference",
    [A("🍷 Wellington Bars","More bars per capita than NYC. Havana (Cuba St), The Library (cocktails), Golding's (craft beer + vegan pizza).",
       ["📍 Cuba St / Courtenay Place"])],
    [M("Dinner","Logan Brown","Heritage building, excellent vegetarian tasting menu. A conference-night treat.","📍 192 Cuba St · 💰 $40-65/person")])],
[P(-41.2889,174.7772,"Wellington CBD",1)]))

#===== DAY 12: May 14 — Conference Day 2 =====
days.append(D(12,"Conference Day 2 & Farewell NZ","Wellington CBD",
"Final conference day and last night in Aotearoa. Soak in the last of Wellington's magic.",
[TB("Daytime — Conference",
    [A("📋 Conference — Day 2","Second day of sessions. Make the most of networking.",
       ["📍 Conference venue"])],
    [M("Breakfast","Café near venue","Quick fuel.","💰 $10-15/person"),
     M("Lunch","Conference or CBD","Between sessions.","💰 $12-20/person")]),
 TB("Evening — Farewell",
    [A("🌅 Farewell Walk","Oriental Bay to Cuba Street along the waterfront at dusk.",
       ["📍 Oriental Parade → Te Papa → Cuba St · FREE"])],
    [M("Dinner","Hillside Kitchen","Farm-to-table farewell dinner with great veggie options.","📍 Kent Tce · 💰 $30-45/person")],
    [T("💡 Pack tonight — early flight back to Australia tomorrow.")])],
[P(-41.2881,174.7888,"Oriental Bay",1),P(-41.2924,174.7787,"Cuba Street",2)]))

#===== DAY 13: May 15 — Byron Bay =====
days.append(D(13,"Fly Back & Byron Bay","Wellington → Sydney → Byron Bay",
"Fly back to Australia and head north to Byron Bay — the spiritual, bohemian heart of the Australian east coast. Surf, sunsets, and incredible vegetarian food.",
[TB("Morning — Fly Back to Australia",
    [A("✈️ Wellington → Sydney → Byron Bay","Fly back to Sydney, then connect to Ballina/Byron Gateway Airport (1hr flight) or drive/bus north (~10hrs). Flight recommended.",
       ["📍 WLG → SYD → BLI · Domestic flights from ~$80","💡 Ballina airport is 30 min from Byron Bay"])]),
 TB("Afternoon — Byron Bay Arrival",
    [A("🌊 Byron Bay — Main Beach & Lighthouse Walk","Drop bags and walk to Australia's most easterly point — the Cape Byron Lighthouse. Stunning 360° views. Watch for whales (May is migration season!) and dolphins.",
       ["📍 Cape Byron Walking Track · FREE · ~3.7 km loop","🐋 May-Nov: humpback whale migration","🌅 Best sunset spot on the east coast"])],
    [M("Lunch","The Top Shop","Byron's famous burger joint (great veggie burger) perched on a hill with ocean views.","📍 Clarkes Beach · 💰 $12-18/person"),
     M("Dinner","Orgasmic Food (Byron Bay)","All-vegetarian café famous for falafel wraps and fresh juices. A Byron institution.","📍 11 Bay Lane · 💰 $12-20/person")],
    [T("💡 Byron Bay has more vegetarian restaurants per capita than almost anywhere in Australia. You'll eat incredibly well here.")])],
[P(-28.6473,153.6020,"Byron Bay Lighthouse",1),P(-28.6435,153.6120,"Main Beach",2)]))

#===== DAY 14: May 16 — Byron Bay & Hinterland =====
days.append(D(14,"Byron Hinterland & Crystal Castle","Bangalow · Crystal Castle · Nimbin (optional)",
"Explore the lush hinterland behind Byron — rolling hills, rainforest, and the mystical Crystal Castle. Optional detour to Australia's alternative capital, Nimbin.",
[TB("Morning — Crystal Castle",
    [A("💎 Crystal Castle & Shambhala Gardens","A stunning crystal garden set in rainforest with a giant amethyst cave, Buddha walk, and peaceful labyrinth. The world's tallest pair of crystals are here.",
       ["📍 81 Monet Dr, Mullumbimby · $35/adult","💡 The Enchanted Cave is mesmerising — giant amethyst geodes","🧘 Meditation garden and sound healing sessions available"])],
    [M("Breakfast","Bayleaf Café (Byron)","Farm-to-table breakfast in a gorgeous garden setting.","📍 Marvell St · 💰 $16-24/person")]),
 TB("Afternoon — Bangalow & Hinterland",
    [A("🌿 Bangalow Village","The cutest hinterland village. Heritage buildings, boutiques, Sunday markets, and a wonderful community feel.",
       ["📍 Byron St, Bangalow · FREE · 15 min drive from Byron"]),
     A("🌈 Nimbin (Optional)","Australia's alternative capital. Famous for its counter-culture, painted buildings, and hemp museum. It's exactly as eccentric as you've heard.",
       ["📍 Nimbin · 45 min from Byron","💡 The Nimbin Museum is a psychedelic experience"])],
    [M("Lunch","Bangalow Dining Rooms","Heritage pub with surprisingly excellent vegetarian options.","💰 $18-28/person"),
     M("Dinner","No Bones (Byron Bay)","All-vegan restaurant with creative dishes. The 'chicken' burger is famous.","📍 11 Fletcher St · 💰 $18-30/person")])],
[P(-28.5820,153.4950,"Crystal Castle",1),P(-28.6855,153.5247,"Bangalow",2),P(-28.6012,153.2227,"Nimbin",3)]))

#===== DAY 15: May 17 — Byron Bay to Yamba =====
days.append(D(15,"Byron Bay to Yamba","Yamba · Angourie · Clarence River",
"Drive south to Yamba — consistently voted Australia's best town. Small-town coastal charm, incredible surfing, and famous fish & chips (vegetarian options too). Visit friends and family.",
[TB("Morning — Drive to Yamba",
    [A("🚗 Byron Bay → Yamba","Beautiful coastal drive south (~2 hours). Stop at Lennox Head for a coffee break — great headland walk.",
       ["📍 ~130 km · 2 hrs via Pacific Highway","💡 Lennox Head's pat Morton lookout = whale watching in May"])],
    [M("Breakfast","Byron Café","Last Byron breakfast. Folk café or Combi for açaí bowls.","💰 $14-20/person")]),
 TB("Afternoon — Yamba Exploration",
    [A("🏖️ Yamba — Australia's Best Town","Main Beach is gorgeous, but also explore Pippi Beach, Turners Beach, and the breakwall walk. This is small-town Australia at its absolute best.",
       ["📍 Yamba, NSW · FREE beaches","💡 Voted Australia's #1 town multiple times"]),
     A("🌊 Angourie Blue & Green Pools","Natural rock pools carved by the ocean just south of Yamba. The Blue Pool is a natural swimming hole — crystal clear and magical.",
       ["📍 Angourie · FREE · 5 min drive from Yamba","🏊 Blue Pool = natural swimming hole in volcanic rock"])],
    [M("Lunch","Beachwood Café","Right on the beach with ocean views and excellent veggie options.","📍 Yamba · 💰 $16-24/person"),
     M("Dinner","Friends & Family","Enjoy a home-cooked meal with your Yamba crew.","💰 Priceless")],
    [T("💡 Yamba's Pacific Hotel does fish & chips that are legendary — they also do great halloumi burgers.")])],
[P(-29.4333,153.3617,"Yamba Main Beach",1),P(-29.4677,153.3655,"Angourie Blue Pool",2)]))

#===== DAY 16: May 18 — Yamba Family Day =====
days.append(D(16,"Yamba — Family & Friends Day","Yamba · Clarence River · Iluka",
"A relaxed day with friends and family. River cruise, beach time, and the genuine warmth of small-town Australia.",
[TB("Morning — Clarence River",
    [A("🛶 Clarence River Exploration","The Clarence is a massive, beautiful river. Kayak, paddleboard, or just