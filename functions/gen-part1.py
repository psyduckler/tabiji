#!/usr/bin/env python3
"""Part 1: Helper functions and Days 1-15"""
import json

def P(lat,lng,label,n,cat="attraction",desc=""):
    return {"lat":lat,"lng":lng,"label":label,"num":n,"cat":cat,"desc":desc or label}
def A(t,d,det=None):
    return {"title":t,"description":d,"details":det or []}
def M(t,n,d,m=""):
    return {"type":t,"name":n,"description":d,"meta":m}
def T(t):
    return {"type":"tip","text":t}
def TB(l,a=None,m=None,t=None):
    return {"label":l,"activities":a or [],"meals":m or [],"tips":t or []}
def D(n,t,h,d,tbs,pins):
    return {"num":n,"title":t,"neighborhoods":h,"description":d,"timeBlocks":tbs,"mapPins":pins}

days = []

# DAY 1 - Sydney Arrival
days.append(D(1,"Sydney Arrival & Harbour Icons","Circular Quay · The Rocks · Sydney CBD",
"Touch down in Sydney and experience the world-famous harbour. Walk from the Opera House to the Harbour Bridge as the city lights up.",
[TB("Morning — Arrival",
    [A("✈️ Arrive in Sydney","Check into accommodation near Circular Quay. Grab a flat white and get your bearings.",["📍 Sydney CBD","💡 Opal card: daily cap ~$17.80, Sunday $2.90","💰 Airport train $19"])],
    [M("Breakfast","Flat White & Avo Toast","Sydney's café culture is legendary.","💰 $12-18/pp")]),
 TB("Afternoon — Opera House & The Rocks",
    [A("🎵 Sydney Opera House","Walk around Bennelong Point. The sails change colour with the light. Tours from $43 or free exterior.",["📍 Bennelong Point · Exterior FREE","💡 Best photo: Mrs Macquarie's Chair"]),
     A("🪨 The Rocks","Sydney's oldest neighbourhood. Cobblestone lanes, heritage pubs, weekend markets.",["📍 The Rocks · FREE","🛍️ Rocks Markets (Sat-Sun)"])],
    [M("Lunch","The Rocks","Pancakes on the Rocks for veggie options, or falafel from market stalls.","💰 $15-22/pp")]),
 TB("Evening — Harbour Bridge",
    [A("🌉 Harbour Bridge Walk","Walk across for jaw-dropping Opera House views. Free from The Rocks side — 20 min each way.",["📍 Cumberland St · FREE","🌅 Golden hour = best photos"])],
    [M("Dinner","Bodhi Restaurant","All-vegetarian yum cha under fig trees. 'Duck' pancakes and dumplings are legendary.","📍 2-4 College St · 💰 $25-35/pp")],
    [T("💡 Walk back via Circular Quay for Opera House lit up at night.")])],
[P(-33.8568,151.2153,"Opera House",1),P(-33.8599,151.2090,"The Rocks",2),P(-33.8523,151.2108,"Harbour Bridge",3),P(-33.873,151.213,"Bodhi",4,"food")]))

# DAY 2 - Bondi & Inner West
days.append(D(2,"Bondi to Coogee & Inner West","Bondi · Coogee · Newtown",
"Walk Australia's most famous coastal trail, then explore Sydney's coolest neighbourhoods for vintage shops, street art, and incredible vegetarian food.",
[TB("Morning — Coastal Walk",
    [A("🏖️ Bondi to Coogee Walk","6 km along dramatic cliffs through Tamarama, Bronte, and Clovelly. Most spectacular urban walk in Australia.",["📍 Bus 333 to Bondi · FREE · ~2 hrs","📸 Icebergs pool from above = iconic"])],
    [M("Breakfast","Bondi Café","Speedos Café on the beach. Acai bowls and people-watching.","💰 $15-22/pp")]),
 TB("Afternoon — Newtown",
    [A("🎨 Newtown — King Street","Bohemian heart. Vintage shops, records, bookshops, densest vegetarian restaurant concentration in Sydney.",["📍 Train to Newtown · FREE"])],
    [M("Lunch","Lentil as Anything","Pay-what-you-feel vegetarian. Amazing curries and salads.","📍 391 King St · Pay what you feel"),
     M("Dinner","Yellow (Potts Point)","All-vegetarian fine dining. Tasting menu with native ingredients.","📍 57 Macleay St · 💰 $85-120/pp")])],
[P(-33.8915,151.2767,"Bondi",1),P(-33.9193,151.2578,"Coogee",2),P(-33.8976,151.179,"Newtown",3)]))

# DAY 3 - Blue Mountains
days.append(D(3,"Blue Mountains — Three Sisters","Katoomba · Leura · Blue Mountains NP",
"Dramatic landscapes. Plunging valleys, eucalyptus-hazed peaks, the Three Sisters, and ancient rainforest — 2 hours from Sydney.",
[TB("Morning — Three Sisters",
    [A("🏔️ Three Sisters","Sandstone pillars over Jamison Valley. In Gundungurra Dreaming, three women turned to stone.",["📍 Echo Point · FREE · Train ~2hrs","🌿 Blue haze = eucalyptus oil refracting light"])],
    [M("Breakfast","Katoomba Cafés","Near the station.","💰 $8-15/pp")],
    [T("💡 May = 8-15°C. Bring layers!")]),
 TB("Midday — Scenic World",
    [A("🚡 Scenic World","World's steepest railway (52°), Skyway, Cableway. Boardwalk through Jurassic-era rainforest.",["📍 Violet St · $53/adult unlimited"])],
    [M("Lunch","Leura Village","Mountain village cafés with veggie options.","💰 $18-30/pp")]),
 TB("Return",
    [A("🌺 Leura Cascades","Waterfalls in ferny bushland.",["📍 Leura · FREE"])],
    [M("Dinner","Chat Thai (Sydney)","Excellent vegetarian Thai.","📍 20 Campbell St · 💰 $15-22/pp")])],
[P(-33.732,150.3121,"Three Sisters",1),P(-33.7292,150.3014,"Scenic World",2),P(-33.7152,150.3364,"Leura",3)]))

# DAY 4 - Fly to Auckland
days.append(D(4,"Fly to Auckland","Auckland CBD · Viaduct · Ponsonby",
"Cross the Tasman to Aotearoa. Auckland — 53 volcanoes between two harbours.",
[TB("Morning — Flight",
    [A("✈️ Sydney → Auckland","~3-hour flight. NZ 2 hours ahead.",["📍 SYD → AKL · From ~$150","💡 NZ biosecurity strict","⏰ NZ = UTC+12"])]),
 TB("Afternoon — Explore",
    [A("⛵ Viaduct Harbour","Waterfront. America's Cup territory. Wynyard Quarter boardwalk.",["📍 Viaduct · FREE"]),
     A("🌿 Ponsonby Road","Auckland's fashionable street. Boutiques, vintage, cafés.",["📍 20-min walk from CBD"])],
    [M("Late Lunch","Viaduct Cafés","Waterfront vegetarian options.","💰 $18-28/pp"),
     M("Dinner","Blue Breeze Inn","Asian-fusion — famous tofu bao.","📍 Ponsonby · 💰 $22-35/pp")])],
[P(-36.8435,174.7555,"Viaduct",1),P(-36.8584,174.7394,"Ponsonby",2)]))

# DAY 5 - Auckland Volcanoes
days.append(D(5,"Auckland Volcanoes & Harbour","Rangitoto · Devonport · Mount Eden",
"Climb a volcanic island, explore Devonport, summit Mount Eden for 360° views.",
[TB("Morning — Rangitoto",
    [A("🌋 Rangitoto Island","Youngest volcano. Ferry, lava fields, summit (260m). 360° Gulf views.",["📍 Ferry · $40 return · 25 min","⏱️ Summit ~1 hr each way","💡 Bring water — no shops"])],
    [M("Breakfast","Waterfront Café","Before the ferry.","💰 $10-15/pp")]),
 TB("Afternoon — Devonport & Mt Eden",
    [A("⚓ Devonport","Victorian village, bookshops, WWII tunnels at North Head.",["📍 Ferry 12 min · $7.50 return"]),
     A("🏔️ Mount Eden","Auckland's highest point (196m). Walk crater rim at sunset.",["📍 FREE","⚠️ Crater is tapu — stay on paths"])],
    [M("Lunch","Devonport Cafés","Victoria Road.","💰 $15-22/pp"),
     M("Dinner","Mount Eden Village","Vegetarian bowls or sushi.","💰 $18-28/pp")])],
[P(-36.7862,174.86,"Rangitoto",1),P(-36.8317,174.7943,"Devonport",2),P(-36.8764,174.7645,"Mt Eden",3)]))

# DAY 6 - Auckland Heritage
days.append(D(6,"Family Heritage & Auckland Museum","Auckland Domain · Parnell",
"Visit great grandfather's grave — connection across generations. Then Auckland Museum's Māori collections.",
[TB("Morning — Grave Visit",
    [A("🪦 Great Grandfather's Grave","A personal pilgrimage. Take your time. Bring flowers.",["💡 Cemeteries: Waikumete, Purewa, Symonds St","🕊️ aucklandcouncil.govt.nz/cemeteries"])],
    [M("Breakfast","Local Café","Keep the morning gentle.","💰 $10-15/pp")]),
 TB("Afternoon — Museum",
    [A("🏛️ Auckland Museum","Natural history, Māori culture (carved meeting house), war memorials.",["📍 Auckland Domain · $28 incl. performance"]),
     A("🌸 Winter Gardens","Free tropical & temperate glasshouses.",["📍 Auckland Domain · FREE"])],
    [M("Lunch","Parnell","Oldest suburb. Great veggie bowls.","💰 $16-24/pp"),
     M("Dinner","K' Road","Coco's Cantina for Italian-NZ veggie pasta.","💰 $20-32/pp")])],
[P(-36.8605,174.7763,"Auckland Museum",1),P(-36.8546,174.7833,"Parnell",2,"food")]))

# DAY 7 - Wellington
days.append(D(7,"Auckland to Wellington","Wellington CBD · Cuba Street",
"The coolest little capital. Compact, creative, Melbourne vibes in harbour-and-hills.",
[TB("Morning — Flight",
    [A("✈️ AKL → WLG","1-hour flight from ~$60.",["📍 AKL → WLG","🚌 Airport Express $12"])]),
 TB("Afternoon — Cuba Street",
    [A("🎭 Cuba Street","Bohemian artery. Bucket fountain, vintage, records, craft beer.",["📍 Cuba St · FREE","☕ Flight Coffee, Customs, Lamason"]),
     A("🚋 Cable Car","Ride to Botanic Garden. Panoramic views.",["📍 Lambton Quay · $10 return"])],
    [M("Lunch","Fidel's","Cuban-NZ fusion café.","📍 Cuba St · 💰 $16-25/pp"),
     M("Dinner","Loretta","Outstanding vegetarian dishes.","💰 $25-40/pp")])],
[P(-41.2924,174.7787,"Cuba St",1),P(-41.2852,174.7707,"Cable Car",2)]))

# DAY 8 - Te Papa
days.append(D(8,"Te Papa & Waterfront","Waterfront · Mt Victoria · Oriental Bay",
"Te Papa — world-class museum. Then Mt Victoria for LOTR views.",
[TB("Morning — Te Papa",
    [A("🏛️ Te Papa Tongarewa","NZ's national museum. Colossal squid, Māori treasures, earthquake simulator. FREE.",["📍 55 Cable St · FREE","💡 Only colossal squid on display worldwide","⏱️ 3-4 hours"])],
    [M("Breakfast","Prefab Eatery","Wellington's beloved café.","💰 $14-20/pp")]),
 TB("Afternoon",
    [A("🏔️ Mt Victoria","Panoramic views. LOTR hobbit-hiding filmed here.",["📍 FREE · 30-min walk","🎬 Hobbits hid from Nazgûl here"]),
     A("🏖️ Oriental Bay","City beach with imported golden sand.",["📍 FREE"])],
    [M("Lunch","Waterfront","Te Papa café or nearby.","💰 $16-25/pp"),
     M("Dinner","Sweet Mother's Kitchen","Cajun-Southern comfort, great veggie options.","💰 $20-32/pp")])],
[P(-41.2905,174.782,"Te Papa",1),P(-41.2964,174.7933,"Mt Victoria",2),P(-41.2881,174.7888,"Oriental Bay",3)]))

# DAY 9 - Weta & South Coast
days.append(D(9,"Weta Workshop & South Coast","Miramar · Lyall Bay · Red Rocks",
"Creative powerhouse behind LOTR, Avatar. Then wild south coast — seal colonies.",
[TB("Morning — Weta",
    [A("🎬 Weta Workshop","LOTR, Hobbit, Avatar props and miniatures. Mind-blowing craftsmanship.",["📍 Miramar · $49/adult","💡 Book ahead","⏱️ 2-3 hrs"])],
    [M("Breakfast","Roxy Cinema Café","Art deco cinema café.","💰 $12-18/pp")]),
 TB("Afternoon — Seals",
    [A("🦭 Red Rocks","Wild coast walk to NZ fur seal colony.",["📍 Owhiro Bay · FREE · 45 min walk","🦭 Best May-Oct"]),
     A("🌊 Lyall Bay","Windswept surfing beach.",["📍 FREE"])],
    [M("Lunch","Maranui Café","Above surf club, ocean views, great veggie.","💰 $16-24/pp"),
     M("Dinner","Courtenay Place","Entertainment district, veggie restaurants.","💰 $20-30/pp")])],
[P(-41.3114,174.8262,"Weta",1),P(-41.348,174.734,"Red Rocks",2)]))

# DAY 10 - Zealandia
days.append(D(10,"Zealandia Ecosanctuary","Karori · Wellington",
"Predator-free sanctuary. Kiwi, tuatara, takahē thriving. NZ conservation at its most hopeful.",
[TB("Morning — Zealandia",
    [A("🥝 Zealandia","225-hectare predator-fenced valley. Kiwi, tuatara, ancient forest.",["📍 Karori · $24/adult","🥝 Night tours $89","⏱️ 2-3 hrs"])],
    [M("Breakfast","Karori Café","Near Zealandia.","💰 $10-16/pp")]),
 TB("Afternoon — Free",
    [A("🛍️ Wellington at Leisure","Cuba Street, Unity Books, Arty Bees, Embassy Theatre.",["📍 Various · FREE"])],
    [M("Lunch","CBD","Light lunch.","💰 $14-22/pp"),
     M("Dinner","Husk","Vegetarian-friendly, creative cocktails.","💰 $22-35/pp")])],
[P(-41.2905,174.753,"Zealandia",1)]))

# DAY 11 - Conference 1
days.append(D(11,"Conference Day 1","Wellington CBD",
"Conference sessions and networking. Wellington's compact — everything walkable.",
[TB("Daytime — Conference",
    [A("📋 Conference Day 1","Full day sessions.",["📍 Conference venue"])],
    [M("Breakfast","Near venue","Quick fuel.","💰 $10-15/pp"),M("Lunch","Conference","Catered or nearby.","💰 $12-20/pp")]),
 TB("Evening",
    [A("🍷 Wellington Bars","Havana, The Library, Golding's (craft beer + vegan pizza).",["📍 Cuba St area"])],
    [M("Dinner","Logan Brown","Heritage building, veggie tasting menu.","📍 192 Cuba St · 💰 $40-65/pp")])],
[P(-41.2889,174.7772,"Wellington CBD",1)]))

# DAY 12 - Conference 2
days.append(D(12,"Conference Day 2 & Farewell NZ","Wellington CBD",
"Final conference day. Last night in Aotearoa.",
[TB("Daytime — Conference",
    [A("📋 Conference Day 2","Final sessions and networking.",["📍 Conference venue"])],
    [M("Breakfast","Café","Quick fuel.","💰 $10-15/pp"),M("Lunch","Conference/CBD","Between sessions.","💰 $12-20/pp")]),
 TB("Evening — Farewell",
    [A("🌅 Farewell Walk","Oriental Bay to Cuba St at dusk.",["📍 Waterfront · FREE"])],
    [M("Dinner","Hillside Kitchen","Farm-to-table farewell. Great veggie.","💰 $30-45/pp")],
    [T("💡 Pack tonight — flight back tomorrow.")])],
[P(-41.2881,174.7888,"Oriental Bay",1)]))

# DAY 13 - Byron Bay
days.append(D(13,"Fly Back & Byron Bay","Wellington → Sydney → Byron Bay",
"Back to Australia. Head to Byron Bay — spiritual, bohemian heart of the east coast.",
[TB("Morning — Flights",
    [A("✈️ WLG → SYD → Byron","Fly to Sydney, connect to Ballina (~1hr). Or drive north from Sydney.",["📍 WLG → SYD → BLI · From ~$80","💡 Ballina airport 30 min from Byron"])]),
 TB("Afternoon — Byron Bay",
    [A("🌊 Cape Byron Lighthouse","Australia's most easterly point. 3.7 km loop with 360° views. Whales in May!",["📍 Cape Byron · FREE · 3.7 km","🐋 May-Nov: humpback migration"])],
    [M("Lunch","The Top Shop","Famous veggie burger with ocean views.","💰 $12-18/pp"),
     M("Dinner","Orgasmic Food","All-vegetarian institution. Famous falafel wraps.","📍 11 Bay Lane · 💰 $12-20/pp")],
    [T("💡 Byron has more vegetarian restaurants per capita than almost anywhere in Australia.")])],
[P(-28.6473,153.602,"Byron Lighthouse",1),P(-28.6435,153.612,"Main Beach",2)]))

# DAY 14 - Byron Hinterland
days.append(D(14,"Byron Hinterland & Crystal Castle","Bangalow · Crystal Castle",
"Lush hinterland. Rolling hills, rainforest, and the mystical Crystal Castle.",
[TB("Morning — Crystal Castle",
    [A("💎 Crystal Castle","Crystal garden in rainforest. Giant amethyst cave, Buddha walk, labyrinth.",["📍 Mullumbimby · $35/adult","💡 Enchanted Cave is mesmerising"])],
    [M("Breakfast","Bayleaf Café","Farm-to-table in a garden setting.","💰 $16-24/pp")]),
 TB("Afternoon — Bangalow",
    [A("🌿 Bangalow Village","Cutest hinterland village. Heritage buildings, boutiques, markets.",["📍 15 min from Byron · FREE"])],
    [M("Lunch","Bangalow Dining Rooms","Heritage pub, excellent veggie.","💰 $18-28/pp"),
     M("Dinner","No Bones (Byron)","All-vegan. Famous 'chicken' burger.","📍 11 Fletcher St · 💰 $18-30/pp")])],
[P(-28.582,153.495,"Crystal Castle",1),P(-28.6855,153.5247,"Bangalow",2)]))

# DAY 15 - Yamba
days.append(D(15,"Byron Bay to Yamba","Yamba · Angourie",
"Drive to Yamba — voted Australia's best town. Small-town coastal charm. Visit friends and family.",
[TB("Morning — Drive",
    [A("🚗 Byron → Yamba","Coastal drive south ~2 hours. Stop at Lennox Head.",["📍 ~130 km · 2 hrs","💡 Pat Morton lookout for whales"])],
    [M("Breakfast","Byron Café","Last Byron breakfast.","💰 $14-20/pp")]),
 TB("Afternoon — Yamba",
    [A("🏖️ Yamba Beaches","Main Beach, Pippi Beach, Turners Beach, breakwall walk.",["📍 Yamba · FREE","💡 Voted Australia's #1 town"]),
     A("🌊 Angourie Blue Pool","Natural swimming hole in volcanic rock. Crystal clear.",["📍 5 min from Yamba · FREE"])],
    [M("Lunch","Beachwood Café","Beach views, excellent veggie.","💰 $16-24/pp"),
     M("Dinner","Friends & Family","Home-cooked meal with your Yamba crew.","💰 Priceless")])],
[P(-29.4333,153.3617,"Yamba",1),P(-29.4677,153.3655,"Angourie",2)]))

if __name__ == "__main__":
    print(json.dumps(days))
