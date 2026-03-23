#!/usr/bin/env python3
"""Part 3: Days 31-46"""
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

# DAY 31 - Darwin to Uluru (fly/drive)
days.append(D(31,"Darwin to Uluru","Darwin → Alice Springs → Uluru-Kata Tjuta NP",
"Fly to Alice Springs or Uluru direct. The Red Centre — Australia's spiritual heart. Uluru rises from the flat desert like a living entity.",
[TB("Morning — Travel to Uluru",
    [A("✈️ Darwin → Ayers Rock Airport (direct)","2-hour flight direct to Uluru (Ayers Rock Airport). Or fly Darwin → Alice → bus 5hrs. Direct flight recommended.",
       ["📍 DRW → AYQ · Direct from ~$180","💡 Or: Darwin → Alice Springs ($120) + 5-hr bus to Uluru",
        "⏰ NT = UTC+9:30 throughout","💰 Park pass $25/pp (valid 3 days)"])],
    [M("Breakfast","Darwin","Early start.","💰 $10-15/pp")]),
 TB("Afternoon — Arrive Uluru",
    [A("🪨 First Sunset at Uluru","Nothing can prepare you for your first sight of Uluru. Drive to the sunset viewing area (Talinguru Nyakunytjaku) with a glass of sparkling wine. Watch it turn from ochre to deep red to purple.",
       ["📍 Talinguru Nyakunytjaku · FREE","🌅 Arrive 1 hour before sunset","💡 The colour is breathtaking — every phone photo is inadequate","⚠️ DO NOT climb Uluru. It's permanently closed (Oct 2019). The Anangu people ask this."])],
    [M("Lunch","Outback Pioneer Hotel","Limited options in Yulara. Packed lunch from resort bakery.",
       "📍 Yulara · 💰 $15-25/pp"),
     M("Dinner","Desert Gardens Hotel","Resort restaurant. Decent vegetarian pasta and salads.",
       "📍 Yulara · 💰 $28-42/pp")],
    [T("⚠️ DO NOT CLIMB ULURU. It was permanently closed in Oct 2019 out of respect for the Anangu people. Climbing is deeply offensive to traditional owners.")])],
[P(-25.3444,131.0369,"Uluru Sunset Viewing",1),P(-25.3640,131.0216,"Uluru",2)]))

# DAY 32 - Uluru Full Day
days.append(D(32,"Uluru — Base Walk & Cultural Tours","Uluru-Kata Tjuta NP · Mutitjulu Waterhole",
"Walk around the full base of Uluru (10.6 km) and discover its extraordinary layers of stories, art, and meaning. The rock is different at every angle.",
[TB("Dawn — Sunrise at Uluru",
    [A("🌅 Uluru Sunrise","Watch the sun rise from Talinguru Nyakunytjaku. Uluru goes from black silhouette to glowing orange in minutes. Arguably the most spectacular sunrise in Australia.",
       ["📍 Sunrise viewing area · FREE · Arrive 30 min before sunrise",
        "🌅 Leave resort ~5:15 AM in May"])],
    [M("Breakfast","Packed","Bring coffee and pastries from resort for sunrise.","")]),
 TB("Morning — Base Walk",
    [A("🚶 Uluru Base Walk","The full 10.6 km circuit takes 3-4 hours and reveals: Kantju Gorge, Mutitjulu Waterhole (sacred, ancient rock art), Kuniya Piti, and constant changing views of the monolith.",
       ["📍 Full circuit 10.6 km · FREE with park pass","💡 Start at Mala Walk car park going clockwise","⚠️ Photography is restricted in some areas (signs indicate)"]),
     A("🎨 Mutitjulu Waterhole & Rock Art","A sacred site with permanent water and ancient rock art. The art depicts the Tjukurpa (Dreaming) — creation stories that explain Uluru's features.",
       ["📍 West side of base walk","💡 Some art panels 10,000+ years old"])],
    [M("Lunch","Picnic","Pack lunch and eat in shaded areas near the base.","")]),
 TB("Afternoon — Cultural Tour",
    [A("🌿 Anangu Cultural Experience","Book a guided tour with Anangu traditional owners. Learn the Tjukurpa (Dreaming), how to hunt, traditional medicine plants, and the deep spiritual significance of every feature of Uluru.",
       ["📍 Various · From $65/pp","💡 Hearing the Tjukurpa directly from Anangu people transforms how you see Uluru"])],
    [M("Dinner","Sounds of Silence","Bush tucker dinner under the stars with didgeridoo. Vegetarian options available. One of the world's great dining experiences.",
       "📍 Under the stars · 💰 $220/pp · Book well ahead")],
    [T("💡 Aboriginal astronomical knowledge is extraordinary — the 'Emu in the Sky' is a constellation made of dark patches, not stars. Anangu guides will show you.")])],
[P(-25.3640,131.0216,"Uluru Base Walk",1),P(-25.3782,131.0160,"Mutitjulu Waterhole",2)]))

# DAY 33 - Kata Tjuta
days.append(D(33,"Kata Tjuta — Valley of the Winds","Kata Tjuta · Walpa Gorge · Kings Canyon area",
"Kata Tjuta (The Olgas) are, many argue, even more impressive than Uluru. Thirty-six domed rock formations, and the Valley of the Winds walk is one of Australia's great hikes.",
[TB("Morning — Kata Tjuta",
    [A("🌄 Valley of the Winds Walk","The full loop (7.4 km) winds through dramatic gorges between the domes. Karu and Karingana lookouts are jaw-dropping. The sacred men's site means you can't do the full loop, but what's open is extraordinary.",
       ["📍 Kata Tjuta · FREE with park pass · 7.4 km · ~3-4 hrs",
        "⚠️ Check closures: the walk closes at 11 AM if temperature exceeds 36°C",
        "💡 Start at dawn — golden light and cooler temperatures"]),
     A("🪨 Walpa Gorge Walk","Short (2.6 km) alternative that goes into a beautiful gorge between the domes.",
       ["📍 Kata Tjuta · FREE · ~1 hr"])],
    [M("Breakfast","Early/Packed","Sunrise start — pack breakfast.","")]),
 TB("Afternoon — Kings Canyon (optional)",
    [A("🏜️ Kings Canyon (Optional Drive)","330 km west of Uluru. If you have the energy, the Rim Walk (6 km) around the canyon is stunning — the Garden of Eden (natural waterhole at the base) is otherworldly. Requires a car.",
       ["📍 Watarrka NP · ~3.5 hrs drive from Uluru",
        "💡 Kings Canyon Resort if staying overnight"])],
    [M("Lunch","Packed","Desert picnic.",""),
     M("Dinner","Outback BBQ at Resort","Or Kings Canyon Resort if you've driven out.",
       "💰 $25-38/pp")])],
[P(-25.2989,130.7340,"Kata Tjuta",1),P(-25.3203,130.7803,"Walpa Gorge",2)]))

# DAY 34 - Fly to Adelaide
days.append(D(34,"Uluru to Adelaide","Uluru → Adelaide · North Terrace · Central Market",
"Fly to South Australia's beautiful, liveable capital. Adelaide is underrated — exceptional food and wine, a vibrant arts scene, and the best central market in Australia.",
[TB("Morning — Flight",
    [A("✈️ Uluru → Adelaide","~2-hour flight to Adelaide.",
       ["📍 AYQ → ADL · ~2 hrs · From ~$150",
        "💡 Adelaide is on ACST (UTC+9:30) same as NT"])],
    [M("Breakfast","Airport or packed","Light breakfast before flight.","")]),
 TB("Afternoon — Adelaide",
    [A("🏛️ North Terrace — Cultural Boulevard","Adelaide's cultural strip. The Art Gallery of SA, SA Museum (free!), State Library, and University of Adelaide all line this leafy boulevard.",
       ["📍 North Terrace · FREE entry to most","💡 SA Museum has a brilliant natural history and Indigenous collection"]),
     A("🌿 Adelaide Central Market","One of Australia's greatest food markets. Deli counters, fresh produce, cheese, coffee, and a wonderful communal atmosphere.",
       ["📍 44 Gouger St · FREE entry · Tue-Sat","💡 Incredible vegetarian food — multiple dedicated stalls"])],
    [M("Lunch","Adelaide Central Market","Graze through the market. Vegetarian options everywhere.",
       "📍 44 Gouger St · 💰 $12-20/pp"),
     M("Dinner","Africola","Adelaide institution. Ethiopian-inspired, heavily vegetarian-friendly menu. The injera and vegetable stews are outstanding.",
       "📍 4 East Terrace · 💰 $28-45/pp")])],
[P(-34.9209,138.5998,"North Terrace",1),P(-34.9285,138.5983,"Central Market",2,"food")]))

# DAY 35 - Adelaide & Friends/Family
days.append(D(35,"Adelaide — Friends, Family & Food","Adelaide Hills · Hahndorf · CBD",
"Reconnect with friends and family in Adelaide. Explore the Adelaide Hills and the German village of Hahndorf.",
[TB("Morning — Adelaide Hills",
    [A("🌿 Adelaide Hills Drive","Beautiful rolling hills 30 minutes from the CBD. Apple orchards, vineyards, and charming villages. Mount Lofty summit (727m) for the view over Adelaide.",
       ["📍 Mt Lofty Summit · $10/car parking · 45-min drive",
        "💡 Cleland Wildlife Park is nearby — koalas, wombats, kangaroos"]),
     A("🏘️ Hahndorf Village","Australia's oldest surviving German settlement. Heritage buildings, artisan shops, and bakeries. The Hahndorf Inn has been here since 1839.",
       ["📍 Hahndorf · 30 min from Adelaide · FREE to explore"])],
    [M("Breakfast","Adelaide","With friends/family.","💰 $12-18/pp")]),
 TB("Afternoon — Family Time",
    [A("👨‍👩‍👧‍👦 Friends & Family","Enjoy quality time with your Adelaide connections. Let them show you their favourite spots.",
       ["📍 Adelaide (wherever they take you)"])],
    [M("Lunch","Hahndorf","German bakeries and cafés — ask for vegetarian schnitzel (mushroom) or apple strudel.",
       "💰 $15-25/pp"),
     M("Dinner","Friends & Family Home","Home-cooked meal — the best kind.",
       "💰 Priceless")])],
[P(-34.9791,138.7225,"Mt Lofty Summit",1),P(-35.0325,138.8025,"Hahndorf",2)]))

# DAY 36 - Barossa/McLaren Vale
days.append(D(36,"Barossa Valley & McLaren Vale","Barossa Valley · McLaren Vale",
"Two of Australia's great wine regions. Even if wine isn't your focus, the landscapes are beautiful and the food is extraordinary.",
[TB("Morning — Barossa Valley",
    [A("🍷 Barossa Valley","World-famous shiraz country. The vines here are among the oldest in the world. Seppeltsfield, Jacobs Creek, and Penfolds are the big names — but small producers are more interesting.",
       ["📍 ~70 km from Adelaide · 1 hr drive",
        "💡 Seppeltsfield Centennial Wines — oldest continuous family winery in Australia",
        "🌿 The Barossa Farmers Market (Sat morning) is excellent for vegetarian produce"])],
    [M("Breakfast","Barossa Farmers Market","Saturday: extraordinary market produce.",
       "💰 $10-18/pp")]),
 TB("Afternoon — McLaren Vale",
    [A("🌊 McLaren Vale","Stunning wine region near the sea. d'Arenberg Cube is a surreal 5-storey cube winery with incredible views.",
       ["📍 ~40 km south of Adelaide",
        "💡 d'Arenberg Cube: free to visit exterior, tours available"])],
    [M("Lunch","McLaren Vale","Blessed Cheese for extraordinary vegetarian cheese platters.",
       "📍 150 Main Rd · 💰 $20-35/pp"),
     M("Dinner","Peel Street (Adelaide)","Adelaide's best restaurant strip. Peel Street restaurant for Modern Australian vegetarian options.",
       "💰 $30-45/pp")])],
[P(-34.5321,138.9531,"Barossa Valley",1),P(-35.2274,138.5447,"McLaren Vale",2)]))

# DAY 37 - Adelaide to Melbourne (Great Ocean Road start)
days.append(D(37,"Adelaide to Warrnambool","Adelaide → Robe → Warrnambool",
"Begin the Great Ocean Road journey. Drive east through SA's Limestone Coast — dramatic sea stacks and beautiful beaches.",
[TB("Morning — Drive East",
    [A("🚗 Adelaide → Robe","~330 km, 3.5 hours. Robe is a beautiful limestone fishing town with excellent seafood (great halloumi burgers too).",
       ["📍 ~3.5 hrs","💡 Beachport also worth a stop — quiet beach town"])],
    [M("Breakfast","Adelaide","Early start.","💰 $10-15/pp")]),
 TB("Afternoon — Robe to Warrnambool",
    [A("🚗 Robe → Warrnambool","Cross into Victoria. ~2.5 more hours.",
       ["📍 ~2.5 hrs","💡 You're now in Victoria — slightly different time zone if QLD was confusing"]),
     A("🐳 Logans Beach Whale Nursery","Southern right whales calve here May-Oct. Viewing platform right on the beach. Free.",
       ["📍 Logans Beach Rd, Warrnambool · FREE","🐳 May-Oct: southern right whales nursing calves in the shallows"])],
    [M("Lunch","Robe","Fish & chips or vegetarian burger.","💰 $14-22/pp"),
     M("Dinner","Warrnambool — Fishtales","Great vegetarian options at this popular restaurant.",
       "💰 $22-35/pp")])],
[P(-37.7694,142.4879,"Warrnambool",1),P(-37.7750,142.5180,"Logans Beach Whales",2)]))

# DAY 38 - Great Ocean Road Day 1
days.append(D(38,"Great Ocean Road — West","Port Campbell · Twelve Apostles · Loch Ard Gorge",
"The most spectacular coastal drive in Australia. The Twelve Apostles rise from the Southern Ocean like ancient sentinels. Start from the western end — fewer crowds.",
[TB("Morning — Twelve Apostles",
    [A("🪨 Twelve Apostles","Limestone stacks rising up to 45m from the ocean. Only 8 remain (they collapse over time). Sunrise is the best time — golden light, fewer tourists.",
       ["📍 Port Campbell NP · FREE · Sunrise!",
        "💡 Go to the eastern viewing platform, not just the main area",
        "🌅 Sunrise here is genuinely spectacular"]),
     A("🏴‍☠️ Loch Ard Gorge","Named after the ship that wrecked here in 1878. Two survivors clung to the rock walls. Now a beautiful gorge with a sheltered beach.",
       ["📍 2 km from Twelve Apostles · FREE"])],
    [M("Breakfast","Packed","Early start for sunrise. Coffee from Port Campbell afterwards.",
       "")]),
 TB("Afternoon — Drive East",
    [A("🌊 The Grotto, London Arch & Bay of Islands","A series of extraordinary rock formations along a short stretch of coast. The Grotto is a collapsed sea cave with a sinkhole view to the ocean.",
       ["📍 Various, Port Campbell NP · FREE"]),
     A("🌿 Otways Rainforest","Stop at the Otways (Maits Rest Rainforest Walk — 30 min, free) for ancient myrtle beech rainforest. Koalas frequently spotted.",
       ["📍 Great Ocean Road · FREE · 30-min walk"])],
    [M("Lunch","Port Campbell","Café in the small township.","💰 $14-22/pp"),
     M("Dinner","Apollo Bay","Beautiful bay town. Bay Leaf Café for vegetarian-friendly dinner.",
       "💰 $22-35/pp")])],
[P(-38.6623,143.1050,"Twelve Apostles",1),P(-38.6744,143.0944,"Loch Ard Gorge",2),P(-38.7781,143.4306,"Apollo Bay",3)]))

# DAY 39 - Great Ocean Road Day 2 / Melbourne
days.append(D(39,"Great Ocean Road to Melbourne","Anglesea · Torquay · Melbourne",
"Drive the rest of the Great Ocean Road through surf country. Arrive in Melbourne — Australia's cultural capital.",
[TB("Morning — Drive to Melbourne",
    [A("🌊 Torquay & Bells Beach","Torquay is the surf capital of Australia — home to Rip Curl and Quiksilver. Bells Beach is the world's most famous surf break.",
       ["📍 Torquay · FREE","🏄 Bells Beach: surfing only — no swimming, powerful waves"]),
     A("🚗 Drive to Melbourne","~1.5 hours into the city from Torquay.",
       ["📍 ~100 km · 1.5 hrs"])],
    [M("Breakfast","Apollo Bay or Lorne","Beautiful cafés on the coast.","💰 $14-20/pp")]),
 TB("Afternoon — Melbourne Arrival",
    [A("🎨 Hosier Lane & Street Art","Melbourne's famous graffiti laneway. Layers of world-class street art by local and international artists. It changes constantly.",
       ["📍 Hosier Lane, CBD · FREE"]),
     A("☕ Melbourne Coffee Culture","Melbourne's café culture is a serious religion. Hardware Société, Brother Baba Budan, Patricia Coffee. Single-origin, pour-over, the works.",
       ["📍 Various CBD · $5-8/cup","💡 Asking for a 'large coffee' will get you a look. Order by type."])],
    [M("Lunch","Lorne","Stop for lunch on the coast.","💰 $16-24/pp"),
     M("Dinner","Moroccan Soup Bar (Melbourne)","Legendary vegetarian restaurant. BYOB, full of food, $30 flat. Book ahead — always packed.",
       "📍 183 St Georges Rd, Fitzroy · 💰 $30 flat vegetarian feast")])],
[P(-37.8136,144.9631,"Melbourne CBD",1),P(-37.8168,144.9704,"Hosier Lane",2,"attraction","Famous graffiti laneway")]))

# DAY 40 - Melbourne
days.append(D(40,"Melbourne — Culture & Neighbourhoods","Fitzroy · Collingwood · Carlton · Southbank",
"Melbourne's inner suburbs are where Australian culture is being made. Street art, Vietnamese food, live music, bookshops, and coffee at every turn.",
[TB("Morning — Fitzroy & Carlton",
    [A("📚 Fitzroy & Smith Street","Melbourne's hippest corridor. Vintage stores, record shops, bookshops, and the densest concentration of good coffee in the Southern Hemisphere.",
       ["📍 Smith St / Johnston St, Fitzroy · FREE"]),
     A("🌿 Carlton Gardens & Museum","Stroll through Carlton Gardens (UNESCO), then visit Melbourne Museum — excellent Indigenous galleries and natural history.",
       ["📍 Carlton Gardens · FREE · Museum $15"])],
    [M("Breakfast","Fitzroy Café","Proud Mary or St Ali for exceptional coffee and vegetarian brunch.",
       "📍 Fitzroy · 💰 $16-24/pp")]),
 TB("Afternoon — Southbank & Galleries",
    [A("🏛️ National Gallery of Victoria (NGV)","Australia's most visited art museum. International collection in the main building (free), Australian art across the river. Incredible architecture.",
       ["📍 180 St Kilda Rd · FREE international collection"]),
     A("🎭 Southbank Promenade","Walk along the Yarra River. Buskers, restaurants, and the Arts Precinct.",
       ["📍 FREE"])],
    [M("Lunch","Queen Victoria Market (if Tuesday or weekend)","Melbourne's famous market. Excellent vegetarian options — roast veggie wraps, falafel, souvlaki.",
       "📍 Corner Elizabeth & Victoria Sts · 💰 $10-18/pp"),
     M("Dinner","Lune Croissanterie + Vegie Bar","Lune for the world's best croissant (seriously). Then Vegie Bar in Fitzroy for a full vegetarian dinner — a Melbourne institution.",
       "📍 Fitzroy · 💰 $20-30/pp")])],
[P(-37.8043,144.9687,"Fitzroy",1),P(-37.8225,144.9690,"NGV",2),P(-37.8091,144.9550,"Carlton Gardens",3)]))

# DAY 41 - Fly to Tasmania
days.append(D(41,"Melbourne to Hobart","Melbourne → Hobart · Salamanca Place · Battery Point",
"Fly to Tasmania — Australia's island state. Cool, green, wild, and deeply distinctive. Hobart is a small city with a big cultural scene anchored by MONA.",
[TB("Morning — Flight",
    [A("✈️ Melbourne → Hobart","1-hour flight.",
       ["📍 MEL → HBA · ~1 hr · From ~$80"])],
    [M("Breakfast","Melbourne","Quick breakfast before flight.","💰 $10-15/pp")]),
 TB("Afternoon — Hobart",
    [A("🏛️ Salamanca Place","Sandstone warehouses converted into galleries, markets, restaurants, and bars. The Salamanca Market (Saturday only) is one of Australia's best outdoor markets.",
       ["📍 Salamanca Place · FREE","🛍️ Salamanca Market (Sat): local produce, art, buskers"]),
     A("⚓ Battery Point","Hobart's historic village quarter. Winding lanes, cottages, and a proper British colonial feel. Arthur Circus is a tiny circular street of Georgian houses.",
       ["📍 Battery Point · FREE to explore"])],
    [M("Lunch","Salamanca","Lots of vegetarian options at the Salamanca cafés.",
       "💰 $16-24/pp"),
     M("Dinner","Pigeon Hole (West Hobart)","Excellent farm-to-table. Great vegetarian options from local producers.",
       "💰 $25-38/pp")])],
[P(-42.8821,147.3272,"Salamanca Place",1),P(-42.8873,147.3319,"Battery Point",2)]))

# DAY 42 - Tasmania: MONA & Huon Valley
days.append(D(42,"MONA & Huon Valley","Berriedale · Huon Valley · Mt Wellington",
"MONA (Museum of Old and New Art) is unlike any museum on Earth — a subterranean provocateur's playground. Then drive the Huon Valley for apple orchards and ancient forests.",
[TB("Morning — MONA",
    [A("🎨 MONA (Museum of Old and New Art)","David Walsh's extraordinary private museum — built underground into a sandstone cliff on a peninsula above the Derwent. Confrontational, funny, beautiful, disturbing. Arrive by ferry (part of the experience).",
       ["📍 655 Main Rd, Berriedale · $35/adult (under 18 free)",
        "🛥️ MONA ROMA ferry from Hobart waterfront — adds to the magic",
        "⏱️ Allow 3-4 hours minimum",
        "💡 The O app (free with admission) is brilliant — use it"])],
    [M("Breakfast","MONA Café","The café is excellent. Vegetarian options.",
       "💰 $14-20/pp")]),
 TB("Afternoon — Huon Valley & Mt Wellington",
    [A("🍎 Huon Valley","Apple country. Ancient Huon pines (1000+ years old!), orchards, and the beautiful valley drive south from Hobart.",
       ["📍 ~45 min south of Hobart · FREE to drive through","💡 Huon Apple & Heritage Festival (March) — or just enjoy the orchards"]),
     A("🏔️ Mount Wellington / kunanyi","The mountain that watches over Hobart. Summit at 1270m — snow is possible in late May/June. Views are spectacular.",
       ["📍 kunanyi/Mt Wellington · FREE · 30-min drive from CBD",
        "💡 Check for snow/ice in June — summit can be 5-10°C colder than city"])],
    [M("Lunch","Huon Valley","Farm gate stall or café near Huonville.",
       "💰 $14-22/pp"),
     M("Dinner","The Glass House (Salamanca)","Wine bar and restaurant with great vegetarian options.",
       "💰 $28-42/pp")])],
[P(-42.8244,147.2725,"MONA",1),P(-42.9891,147.2047,"Huon Valley",2),P(-42.8984,147.2324,"Mt Wellington",3)]))

# DAY 43 - Tasmania: Freycinet & East Coast
days.append(D(43,"Tasmania East Coast — Freycinet","Freycinet NP · Wineglass Bay · Bicheno",
"Drive to Tasmania's east coast. Freycinet is pure pink granite peaks, white sand, and impossibly blue water. Wineglass Bay is consistently ranked one of the world's top beaches.",
[TB("Morning — Drive to Freycinet",
    [A("🚗 Hobart → Freycinet","~2.5 hours northeast along the Tasman Highway. Beautiful coastal drive.",
       ["📍 ~200 km · 2.5 hrs"])],
    [M("Breakfast","Hobart","Early start.","💰 $10-15/pp")]),
 TB("Afternoon — Wineglass Bay",
    [A("🏖️ Wineglass Bay Walk","The Wineglass Bay Lookout walk (1 hr return) gives the famous aerial view of the perfect crescent bay. Descend to the beach (3 hrs return) to walk the white sand.",
       ["📍 Freycinet NP · $30 park pass/vehicle · ~3 hrs to beach",
        "💡 The lookout view alone is worth it — one of the world's great views",
        "🌊 The water is crystal clear and cold (12-15°C in May/June)"]),
     A("🪨 Hazards Beach","Less visited than Wineglass Bay but equally beautiful. Pink granite boulders, white sand, blue water.",
       ["📍 Freycinet NP · ~4 hrs return walk from carpark"])],
    [M("Lunch","Packed","Bring lunch for the national park.",
       ""),
     M("Dinner","Freycinet Marine Farm","Oysters and seafood (they have vegetarian platters too) with harbour views.",
       "📍 1784 Coles Bay Rd · 💰 $20-35/pp")],
    [T("💡 Freycinet is booked months ahead in summer. May/June is quieter — you may have the beach to yourself.")])],
[P(-42.1511,148.2997,"Wineglass Bay",1),P(-42.2084,148.3092,"Freycinet NP",2)]))

# DAY 44 - Tasmania: Port Arthur
days.append(D(44,"Port Arthur & Tasman Peninsula","Port Arthur · Tasman Arch · Cape Hauy",
"The most intact convict site in the world. Port Arthur is hauntingly beautiful and deeply moving — a place where Australia's brutal colonial history is visible in stone.",
[TB("Morning — Port Arthur",
    [A("⛓️ Port Arthur Historic Site","UNESCO World Heritage. The main penitentiary, church ruins, hospital, and guard tower are extraordinary. The settlement was active 1830-1877 — 12,000 convicts transported here.",
       ["📍 Port Arthur · $45/adult incl. harbour cruise + ghost tour",
        "⏱️ Allow at least half a day",
        "💡 The Isle of the Dead (convict cemetery island) boat tour is sobering and beautiful",
        "🕯️ Ghost tours at night are genuinely excellent"])],
    [M("Breakfast","Port Arthur","Café at the historic site.",
       "💰 $12-18/pp")]),
 TB("Afternoon — Tasman Peninsula",
    [A("🌊 Tasman Arch & Devil's Kitchen","Extraordinary dolerite sea cliffs — some of the highest in the Southern Hemisphere. The Tasman Arch is a natural rock bridge. Devil's Kitchen is a collapsed cave with crashing surf far below.",
       ["📍 Tasman Peninsula · FREE",
        "💡 Tessellated Pavement (geometric rock formation) is nearby — remarkable natural phenomenon"]),
     A("🦅 Cape Hauy Walk","One of Tasmania's best day walks. Follows the cliff edge to The Totem Pole and Candlestick sea stacks. 6 km return, spectacular.",
       ["📍 Fortescue Bay · ~3 hrs return"])],
    [M("Lunch","Fortescue Bay Picnic","Bring lunch for the walk.",
       ""),
     M("Dinner","Hobart — Ethos Eat Drink","Outstanding vegetarian restaurant in Hobart CBD.",
       "📍 Hobart · 💰 $28-42/pp")])],
[P(-43.1446,147.8497,"Port Arthur",1),P(-43.0846,147.9012,"Tasman Arch",2),P(-43.1229,147.9423,"Cape Hauy",3)]))

# DAY 45 - Tasmania: Friends/Family & Cradle Mountain area
days.append(D(45,"Tasmania — Friends, Family & Wilderness","