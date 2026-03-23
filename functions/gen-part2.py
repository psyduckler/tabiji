#!/usr/bin/env python3
"""Part 2: Days 16-30"""
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
    return {"label":l,"activities":a or [],"meals":m or[],"tips":t or []}
def D(n,t,h,d,tbs,pins):
    return {"num":n,"title":t,"neighborhoods":h,"description":d,"timeBlocks":tbs,"mapPins":pins}

days = []

# DAY 16 - Yamba Family
days.append(D(16,"Yamba — Family & Friends","Yamba · Clarence River · Iluka",
"Relaxed day with friends and family. River, beaches, small-town warmth.",
[TB("Morning — River",
    [A("🛶 Clarence River","Kayak, paddleboard, or walk the riverbank. Massive beautiful river.",["📍 Clarence River · Hire from $30/hr"])],
    [M("Breakfast","Yamba Café","Riverside café.","💰 $12-18/pp")]),
 TB("Afternoon — Iluka & Bundjalung",
    [A("🌲 Iluka Rainforest Walk","World Heritage-listed littoral rainforest right to the beach. Short walk, huge reward.",["📍 Iluka · FREE · 2.5 km loop"]),
     A("🏖️ Iluka Bluff","Quiet beach at the river mouth. Dolphins often visible.",["📍 Iluka · FREE"])],
    [M("Lunch","Pacific Hotel Yamba","Legendary halloumi burger and ocean views.","💰 $16-24/pp"),
     M("Dinner","Family Dinner","Another evening with your Yamba people.","💰 Priceless")])],
[P(-29.4333,153.3617,"Yamba",1),P(-29.405,153.363,"Iluka",2)]))

# DAY 17 - Drive to Gold Coast/Sunshine Coast
days.append(D(17,"Yamba to Gold Coast","Yamba → Gold Coast · Surfers Paradise · Burleigh Heads",
"Drive north into Queensland. The Gold Coast is glitzy on the surface but has genuinely great beaches and a thriving food scene.",
[TB("Morning — Drive North",
    [A("🚗 Yamba → Gold Coast","~4 hours north. Welcome to Queensland — Sunshine State.",["📍 ~370 km · 4 hrs"])],
    [M("Breakfast","Yamba","Farewell breakfast with friends.","💰 $12-18/pp")]),
 TB("Afternoon — Gold Coast",
    [A("🏖️ Burleigh Heads","Best beach on the Gold Coast. National park headland walk with ocean views, then surf or swim.",["📍 Burleigh Heads · FREE","💡 Better than Surfers Paradise for actual beach vibes"]),
     A("🌿 Burleigh Head National Park","Short coastal walk through rainforest to volcanic rock platforms.",["📍 FREE · 30-min loop"])],
    [M("Lunch","Borough Barista (Burleigh)","Excellent veggie options with ocean views.","💰 $16-24/pp"),
     M("Dinner","Paddock Bakery (Miami)","Famous for vegetarian baked goods and brunch vibes.","💰 $18-28/pp")])],
[P(-28.0904,153.4483,"Burleigh Heads",1),P(-28.0194,153.4300,"Surfers Paradise",2)]))

# DAY 18 - Sunshine Coast
days.append(D(18,"Gold Coast to Noosa","Gold Coast → Noosa · Eumundi · Noosa NP",
"Drive to the Sunshine Coast. Noosa is Australia's most elegant beach town — think Byron Bay with better restaurants.",
[TB("Morning — Drive",
    [A("🚗 Gold Coast → Noosa","~2.5 hours north along the coast.",["📍 ~200 km · 2.5 hrs"])],
    [M("Breakfast","Gold Coast Café","Quick breakfast before heading north.","💰 $12-18/pp")]),
 TB("Afternoon — Noosa",
    [A("🏖️ Noosa Main Beach","Protected north-facing beach — calm turquoise water. One of Australia's best.",["📍 Hastings St · FREE"]),
     A("🌿 Noosa National Park","Coastal walk through bushland with koala sightings. Hell's Gates lookout is dramatic.",["📍 FREE · Multiple tracks","🐨 Koalas frequently spotted in trees along the walk"])],
    [M("Lunch","Hastings Street","Noosa's dining strip. Excellent vegetarian at multiple cafés.","💰 $18-28/pp"),
     M("Dinner","Locale Noosa","Italian-Australian with outstanding veggie pasta and pizza.","💰 $22-35/pp")])],
[P(-26.3881,153.0817,"Noosa Beach",1),P(-26.3942,153.0956,"Noosa NP",2)]))

# DAY 19 - Fraser Island/K'gari
days.append(D(19,"K'gari (Fraser Island) Day Trip","K'gari · Lake McKenzie · Eli Creek",
"World's largest sand island. Crystal lakes, ancient rainforest growing on sand, and dingoes. A UNESCO World Heritage wonder.",
[TB("Full Day — K'gari",
    [A("🏝️ K'gari (Fraser Island)","World's largest sand island. Book a day tour from Noosa/Hervey Bay. Lake McKenzie (stunning blue freshwater), Eli Creek, Maheno Shipwreck, and rainforest.",
       ["📍 Day tour from Noosa ~$200/pp","💡 Lake McKenzie's white silica sand and blue water is surreal","🐕 Dingoes: keep 5m distance, never feed them","⏱️ Full day 7 AM - 6 PM"])],
    [M("Breakfast","Tour Provided","Most tours include breakfast/lunch.",""),
     M("Lunch","Tour Provided","Included in most day tours.",""),
     M("Dinner","Noosa — Spirit House (nearby)","Thai in a stunning rainforest garden. Excellent vegetarian menu.","💰 $30-45/pp")])],
[P(-25.2628,153.1363,"Lake McKenzie",1),P(-25.1933,153.1517,"Eli Creek",2)]))

# DAY 20 - Drive to Airlie Beach
days.append(D(20,"Noosa to Airlie Beach","Noosa → Rockhampton → Airlie Beach",
"Big drive day heading north towards the Whitsundays. Break it up with stops. Australia's scale becomes very real.",
[TB("Full Day — Drive",
    [A("🚗 Noosa → Airlie Beach","~850 km, split into 2 days. Today: Noosa to Rockhampton/Gladstone (~550 km, 6 hrs). Stay overnight.",
       ["📍 Noosa → Rockhampton · ~6 hrs","💡 Stop at 1770/Agnes Water (southernmost reef town)","🦘 Watch for kangaroos near dusk"])],
    [M("Breakfast","Noosa","Farewell breakfast.","💰 $12-18/pp"),
     M("Lunch","Bundaberg or 1770","Stop for lunch along the way. Mon Repos turtle centre near Bundaberg is worth a quick stop.","💰 $14-22/pp"),
     M("Dinner","Rockhampton","Overnight stop. Surprisingly good dining scene.","💰 $18-28/pp")])],
[P(-23.3791,150.5100,"Rockhampton",1)]))

# DAY 21 - Continue to Airlie
days.append(D(21,"Rockhampton to Airlie Beach","Rockhampton → Mackay → Airlie Beach",
"Continue north to the Whitsunday gateway. The landscape shifts from farmland to tropical coast.",
[TB("Morning — Drive",
    [A("🚗 Rockhampton → Airlie Beach","~500 km, 5.5 hours. The tropics begin.",["📍 ~5.5 hrs","💡 Stop in Mackay for coffee — nice river town"])],
    [M("Breakfast","Rockhampton","Quick start.","💰 $10-15/pp")]),
 TB("Afternoon — Airlie Beach",
    [A("🌴 Airlie Beach Lagoon","Free public lagoon pool right on the waterfront. Tropical vibes, palm trees, and a bar next door.",["📍 Airlie Beach · FREE","💡 Stinger season (Oct-May) makes ocean swimming risky — the lagoon is safe"]),
     A("🛍️ Airlie Main Street","Small but vibrant town. Backpacker energy meets sailing luxury.",["📍 FREE to explore"])],
    [M("Lunch","Mackay","Coffee and lunch en route.","💰 $14-22/pp"),
     M("Dinner","Fish D'vine (Airlie)","Great veggie options including halloumi burgers and vegetarian curries.","💰 $18-30/pp")])],
[P(-20.2686,148.7186,"Airlie Beach",1)]))

# DAY 22 - Whitsundays
days.append(D(22,"Whitsunday Islands","Whitsunday Island · Hill Inlet · Whitehaven Beach",
"One of the most beautiful places on Earth. Whitehaven Beach's pure white silica sand and the swirling sands of Hill Inlet are bucket-list moments.",
[TB("Full Day — Whitsundays Sailing",
    [A("⛵ Whitsunday Islands Day Sail","Book a day sailing trip to Whitehaven Beach and Hill Inlet lookout. The sand is 98.9% pure silica — it squeaks underfoot and won't burn your feet.",
       ["📍 Depart Airlie Beach · Day trips from $180/pp","💡 Hill Inlet lookout at high tide = swirling sand photo","🐢 Snorkelling at Mantaray Bay or Chalkies Beach","🧴 Reef-safe sunscreen only!"]),
     A("🏖️ Whitehaven Beach","7 km of the whitest sand on Earth. Consistently voted world's best beach. The water is impossibly turquoise.",
       ["📍 Whitsunday Island · Accessible by boat only","💡 Walk to Hill Inlet Lookout from north end"])],
    [M("Breakfast","Tour Included","Most sailing trips include meals.",""),
     M("Lunch","Tour Included","Fresh lunch on the boat.",""),
     M("Dinner","Airlie Beach","Celebrate at Mr Bones (pizza, great veggie options).","💰 $18-28/pp")])],
[P(-20.2830,149.0335,"Whitehaven Beach",1),P(-20.2570,149.0440,"Hill Inlet",2)]))

# DAY 23 - Great Barrier Reef
days.append(D(23,"Great Barrier Reef","Outer Reef · Airlie Beach",
"Snorkel the Great Barrier Reef — the largest living structure on Earth. Visible from space. Absolutely unmissable.",
[TB("Full Day — Reef Trip",
    [A("🐠 Great Barrier Reef Snorkel/Dive","Book an outer reef trip for the best coral. The reef is alive with colour — turtles, clownfish, giant clams, parrotfish. A life-defining experience.",
       ["📍 Day trip from Airlie · From $220/pp","💡 Outer reef > inner reef for coral quality","🐢 Green sea turtles are common","🧴 REEF-SAFE SUNSCREEN ONLY","⏱️ Full day 8 AM - 5 PM"]),
     A("🪸 Reef Snorkelling","Even beginner snorkellers see incredible things. Guides point out marine life. Semi-sub and glass-bottom boats for non-swimmers.",
       ["💡 Bring an underwater camera","🐠 Look for: clownfish, parrotfish, Maori wrasse, reef sharks"])],
    [M("Breakfast","Tour","Early start, light breakfast on boat.",""),
     M("Lunch","Tour","Included — usually BBQ lunch on the pontoon.",""),
     M("Dinner","Airlie","Relaxed dinner after a big day. Deja Vu for veggie Thai.","💰 $18-28/pp")],
    [T("💡 The reef is bleaching due to climate change. Seeing it now, while it's still spectacular, is genuinely urgent.")])],
[P(-19.7500,149.5000,"Outer Reef",1)]))

# DAY 24 - Drive to Cairns area
days.append(D(24,"Airlie Beach to Townsville","Airlie → Bowen → Townsville",
"Continue north. Stop at Bowen for mango country and beautiful bays.",
[TB("Morning — Drive",
    [A("🚗 Airlie → Townsville","~275 km, 3.5 hours. Stop at Bowen — fruit bowl of Queensland.",["📍 ~3.5 hrs","💡 Bowen: mango capital + gorgeous bays"])],
    [M("Breakfast","Airlie Beach","Quick start.","💰 $10-15/pp")]),
 TB("Afternoon — Townsville",
    [A("🏝️ Magnetic Island (Optional)","20-min ferry to 'Maggie Island'. Koalas, beaches, WWII forts. Can do a quick half-day visit.",["📍 Ferry from Townsville · $16 return","🐨 Wild koalas — Fort walk trail"]),
     A("🌊 The Strand","Townsville's beautiful 2.2 km beachfront promenade.",["📍 FREE"])],
    [M("Lunch","Bowen","Mango smoothies and fish & chips (veggie alternatives available).","💰 $12-20/pp"),
     M("Dinner","Townsville — A Touch of Salt","Upscale dining with good vegetarian options.","💰 $25-38/pp")])],
[P(-19.2590,147.4600,"Townsville",1),P(-19.1500,146.8500,"Magnetic Island",2)]))

# DAY 25 - Cairns & Daintree
days.append(D(25,"Townsville to Cairns","Townsville → Mission Beach → Cairns",
"Arrive in tropical Cairns — gateway to the Daintree and reef. Stop at Mission Beach for cassowary country.",
[TB("Morning — Drive to Cairns",
    [A("🚗 Townsville → Cairns","~350 km, 4 hours. Stop at Mission Beach — cassowary territory.",["📍 ~4 hrs","💡 Mission Beach: endangered cassowary sightings","🦅 Don't approach cassowaries — they can be aggressive"])],
    [M("Breakfast","Townsville","Quick breakfast.","💰 $10-15/pp")]),
 TB("Afternoon — Cairns",
    [A("🌴 Cairns Esplanade & Lagoon","Free public lagoon pool on the waterfront. Cairns doesn't have a beach (it's all mud flats), but the lagoon is excellent.",["📍 Cairns Esplanade · FREE","💡 No ocean swimming in Cairns — crocs and stingers"]),
     A("🌿 Cairns Botanic Gardens","Tropical gardens with a rainforest boardwalk. Free and beautiful.",["📍 FREE · Collins Ave"])],
    [M("Lunch","Mission Beach","Café between rainforest and beach.","💰 $14-22/pp"),
     M("Dinner","Cairns Night Markets","Huge night market with Asian street food, vegetarian stalls galore.","📍 Esplanade · 💰 $10-18/pp")])],
[P(-16.9186,145.7781,"Cairns",1),P(-17.8681,146.1067,"Mission Beach",2)]))

# DAY 26 - Daintree
days.append(D(26,"Daintree Rainforest","Daintree · Cape Tribulation · Mossman Gorge",
"The oldest rainforest on Earth (180 million years). Where the rainforest meets the reef — the only place on Earth where two World Heritage sites sit side by side.",
[TB("Morning — Mossman Gorge",
    [A("🌿 Mossman Gorge","Crystal-clear swimming holes in ancient rainforest. The Kuku Yalanji Dreamtime Walks offer Indigenous-led tours through country.",
       ["📍 Mossman · Dreamtime Walk $79/pp","💡 The swimming hole is stunning — emerald water in granite gorge","🏊 Safe to swim (no crocs in fresh water here)"])],
    [M("Breakfast","Cairns","Early start for the drive north (~1.5 hrs).","💰 $10-15/pp")]),
 TB("Afternoon — Daintree & Cape Tribulation",
    [A("🌴 Daintree River Cruise","Spot saltwater crocodiles on a river cruise. They're prehistoric and enormous.",["📍 Daintree River · Cruises from $30/pp","🐊 Saltwater crocs can be 5m+ long"]),
     A("🏖️ Cape Tribulation","Where rainforest dramatically meets the ocean. Walk the boardwalk through ancient forest to the beach. Named by Captain Cook after his ship struck the reef here.",
       ["📍 Cape Tribulation · FREE","⚠️ No swimming — crocs and stingers","💡 One of the most photographed spots in Australia"])],
    [M("Lunch","Daintree Ice Cream Company","Tropical fruit ice cream made from fruit grown on-site. All vegetarian!","📍 Daintree · 💰 $8-12/pp"),
     M("Dinner","Cairns","Back in Cairns. Ochre Restaurant for native Australian cuisine with great veggie options.","💰 $25-40/pp")],
    [T("💡 The Daintree is 180 million years old — older than the Amazon by 100 million years.")])],
[P(-16.4697,145.4240,"Mossman Gorge",1),P(-16.1687,145.4688,"Cape Tribulation",2),P(-16.3040,145.3977,"Daintree River",3)]))

# DAY 27 - Fly to Darwin
days.append(D(27,"Cairns to Darwin","Cairns → Darwin · Mindil Beach",
"Fly to the Top End. Darwin is Australia's most multicultural, tropical, and remote capital city. Sunsets that will ruin all other sunsets for you.",
[TB("Morning — Flight",
    [A("✈️ Cairns → Darwin","~2.5 hour flight. You've entered the Northern Territory — a completely different Australia.",["📍 CNS → DRW · From ~$120","⏰ NT = UTC+9:30 (30 min behind QLD)"])],
    [M("Breakfast","Cairns","Quick breakfast before flight.","💰 $10-15/pp")]),
 TB("Afternoon — Darwin",
    [A("🌅 Mindil Beach Sunset Market","THE Darwin experience. Markets on the beach as the sun sets over the Timor Sea. Asian street food, Indigenous art, buskers, and the most spectacular sunset you'll see.",
       ["📍 Mindil Beach · FREE entry · Thu & Sun evenings (dry season)","💡 The sunset here is genuinely life-changing","🍜 Hundreds of food stalls — amazing vegetarian laksa, satay, pad thai"]),
     A("🌴 Darwin Waterfront Precinct","Wave pool, restaurants, and the waterfront lagoon. Safe swimming!",["📍 FREE · Stokes Hill Wharf area"])],
    [M("Lunch","Darwin CBD","Quick lunch after landing.","💰 $14-22/pp"),
     M("Dinner","Mindil Beach Markets","Eat at the markets. Laksa, dumplings, pad thai, all vegetarian options.","💰 $10-18/pp")])],
[P(-12.4434,130.8456,"Mindil Beach",1),P(-12.4634,130.8456,"Darwin Waterfront",2)]))

# DAY 28 - Litchfield
days.append(D(28,"Litchfield National Park","Litchfield · Wangi Falls · Florence Falls",
"Waterfalls, swimming holes, and magnetic termite mounds. Litchfield is the accessible alternative to Kakadu — less remote, equally stunning.",
[TB("Full Day — Litchfield",
    [A("💧 Wangi Falls","Double waterfall cascading into a huge natural swimming pool surrounded by monsoon forest. The most popular swim in the NT.",
       ["📍 Litchfield NP · FREE · ~1.5 hrs from Darwin","🏊 Check croc safety signs — pool closed if crocs detected","💡 Morning visit for fewest crowds"]),
     A("🌊 Florence Falls","Swim in a plunge pool at the base of twin waterfalls. The walk down through vine forest is beautiful.",
       ["📍 Litchfield · FREE","💡 Buley Rockhole nearby — series of natural spa pools"]),
     A("🐜 Magnetic Termite Mounds","Hundreds of 2m-tall tombstone-shaped mounds, all aligned north-south to regulate temperature. Mind-blowing natural engineering.",
       ["📍 Litchfield · FREE viewing platform"])],
    [M("Breakfast","Darwin","Early start with packed snacks.","💰 $10-15/pp"),
     M("Lunch","Packed Lunch","Bring food — limited options in the park.","💡 Pack sandwiches & fruit"),
     M("Dinner","Darwin — Hanuman","Outstanding Thai/Indian in Darwin. Exceptional vegetarian menu.","📍 93 Mitchell St · 💰 $28-42/pp")],
    [T("💡 Croc safety is REAL in the NT. Never swim in unmarked waterways. Check signs at every swimming hole.")])],
[P(-13.1635,130.6840,"Wangi Falls",1),P(-13.1098,130.7878,"Florence Falls",2),P(-13.0988,130.7620,"Termite Mounds",3)]))

# DAY 29 - Kakadu
days.append(D(29,"Kakadu National Park — Day 1","Kakadu · Ubirr · Cahills Crossing",
"Australia's largest national park. Aboriginal rock art 20,000+ years old, wetlands teeming with wildlife, and landscapes that are genuinely unlike anywhere else on Earth.",
[TB("Morning — Drive to Kakadu",
    [A("🚗 Darwin → Kakadu","~3 hours east. Enter Kakadu — Aboriginal-owned, jointly managed.",["📍 ~250 km · 3 hrs","💰 Park pass $40/pp (valid 7 days)","💡 Kakadu is Aboriginal land — respect is paramount"])],
    [M("Breakfast","Darwin","Early start.","💰 $10-15/pp")]),
 TB("Afternoon — Ubirr",
    [A("🎨 Ubirr Rock Art","One of Australia's most significant Aboriginal art sites. Paintings spanning 20,000+ years — creation stories, animals, contact-era depictions of Europeans. The sunset lookout above is otherworldly.",
       ["📍 Ubirr · FREE with park pass","🌅 Sunset from the top is a spiritual experience","💡 The X-ray style art (showing internal organs) is unique to this region"]),
     A("🐊 Cahills Crossing","Famous saltwater crocodile viewing spot where crocs gather at the river crossing. You will see enormous crocs.",
       ["📍 East Alligator River · FREE","🐊 Multiple large crocs visible from viewing area","⚠️ NEVER enter the water"])],
    [M("Lunch","Kakadu — Border Store","Basic supplies and takeaway near Ubirr.","💰 $12-20/pp"),
     M("Dinner","Cooinda Lodge","Kakadu's main accommodation hub. Restaurant with veggie options.","💰 $25-38/pp")])],
[P(-12.4113,132.9459,"Ubirr",1),P(-12.4250,132.9600,"Cahills Crossing",2)]))

# DAY 30 - Kakadu Day 2
days.append(D(30,"Kakadu — Yellow Water & Nourlangie","Yellow Water · Nourlangie · Jim Jim Falls",
"Cruise among thousands of birds and crocodiles at Yellow Water, then explore Nourlangie's ancient rock art galleries.",
[TB("Morning — Yellow Water",
    [A("🛶 Yellow Water Cruise","Billabong cruise through wetlands teeming with birdlife — jabiru, brolga, magpie geese, sea eagles — and saltwater crocs lurking at the water's edge. Sunrise cruise is magical.",
       ["📍 Cooinda · Sunrise cruise $99/pp","🐊 Crocs and thousands of birds","💡 Sunrise cruise (6:45 AM) is the best — cooler, birds most active"])],
    [M("Breakfast","Before cruise","Early start for sunrise cruise. Light snack.","💰 $8-12/pp")]),
 TB("Afternoon — Nourlangie & Jim Jim",
    [A("🎨 Nourlangie Rock Art","Another extraordinary gallery of Aboriginal rock art. Lightning Man (Namarrgon) is the star — a creation ancestor who controls the monsoon storms.",
       ["📍 Nourlangie · FREE with park pass","💡 Lightning Man painting is one of Kakadu's most famous images"]),
     A("💧 Jim Jim Falls (seasonal)","In the wet season this is a thundering 200m waterfall. By May/June, it's a tranquil plunge pool — still beautiful, just different.",
       ["📍 Jim Jim · 4WD access only · Check conditions","💡 May/June = end of wet, falls may still be flowing"])],
    [M("Lunch","Cooinda","Lodge restaurant or packed lunch.","💰 $14-22/pp"),
     M("Dinner","Jabiru","Small town in Kakadu. Aurora Kakadu has a restaurant.","💰 $22-35/pp")])],
[P(-12.9055,132.5322,"Yellow Water",1),P(-12.8624,132.8136,"Nourlangie",2),P(-13.2613,132.5430,"Jim Jim Falls",3)]))

if __name__ == "__main__":
    print(json.dumps(days))
