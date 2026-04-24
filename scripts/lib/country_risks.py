"""
Curated per-country "biggest risks for tourists" data for the country-page
rebuild. Popular destinations get hand-written risk rankings that capture the
non-obvious (motorbike deaths in Thailand, rabies in Bali, altitude in Peru,
etc.). Less-traveled countries fall back to a programmatic derivation from the
structured health-data JSON fields (water safety, strict meds, yellow fever,
healthcare quality).

Each CURATED entry is a list of 3-5 dicts:
    {
        "title": "Short headline",
        "body": "1-2 sentence explanation with a concrete action",
        "tone": "danger" | "caution" | "info",
    }

Used by scripts/build-country-pages.py → country_risks.get(slug) falls back to
derive_default_risks() when no curated entry exists.
"""

from __future__ import annotations


# -------------------------------------------------------------------
# Curated top-risks for ~40 high-traffic destinations.
# Ordered by risk severity (most likely to kill or ruin a trip first).
# -------------------------------------------------------------------

CURATED = {
    # ---------- Southeast Asia ----------
    "thailand": [
        {"tone": "danger", "title": "Motorbike crashes are the #1 tourist killer",
         "body": "Moped and motorcycle accidents cause more tourist deaths in Thailand than all other causes combined. Wear a helmet, never drive drunk, and verify your travel insurance covers motorbike riding (most policies exclude it by default)."},
        {"tone": "caution", "title": "Dengue peaks April through October",
         "body": "Monsoon season brings elevated dengue transmission, especially in Bangkok, Chiang Mai, Phuket, and Koh Samui. Use DEET at dawn and dusk, sleep in screened rooms, and see a doctor for any fever + joint pain within 14 days of a trip."},
        {"tone": "caution", "title": "Box jellyfish in the Gulf June–October",
         "body": "Chironex-genus box jellyfish appear in Gulf waters (Koh Samui, Koh Phangan) during warm months. Sting kits (vinegar) at most beach resorts; don't swim at dusk or after rain."},
        {"tone": "caution", "title": "Adderall, Ritalin, Tramadol require permits",
         "body": "ADHD stimulants and tramadol require a Thai FDA import permit before arrival. Medical cannabis is legal for Thai residents only — tourists are arrested."},
        {"tone": "info", "title": "Street food is safer than you think at busy stalls",
         "body": "Cooked-to-order food at high-turnover vendors is generally safe. Avoid sliced fruit, tap-water ice at cheaper venues, and raw/undercooked seafood."},
    ],
    "indonesia": [
        {"tone": "danger", "title": "Rabies is endemic — don't touch animals",
         "body": "Bali has an active rabies epidemic in stray dogs and monkeys. Any bite or scratch requires immediate wound washing and post-exposure vaccination within hours. Medical-grade rabies immunoglobulin is limited outside Denpasar."},
        {"tone": "danger", "title": "Motorbike crashes + traffic chaos",
         "body": "Moped accidents are the leading cause of foreign-tourist death in Bali. Rent through a licensed operator, wear a helmet, and check your insurance covers it — most policies don't unless you've added a motorbike rider."},
        {"tone": "caution", "title": "Dengue year-round, peaks rainy season",
         "body": "Transmitted by day-biting mosquitoes; use DEET throughout the day, not just at dusk. Watch for sudden fever + severe joint pain + rash within 2 weeks of return."},
        {"tone": "caution", "title": "Bali belly: tap water + ice at budget venues",
         "body": "Don't drink tap water or eat ice at roadside warungs. Higher-end restaurants and resorts filter water and ice safely. Bring oral rehydration salts and loperamide."},
        {"tone": "info", "title": "Medical evacuation to Singapore for serious cases",
         "body": "Local hospitals are adequate for routine care. Serious trauma, cardiac, or complex surgery typically gets evacuated to Singapore Mount Elizabeth or Bangkok Bumrungrad. Insurance with $250K+ evacuation cover is essential."},
    ],
    "vietnam": [
        {"tone": "danger", "title": "Motorbike chaos in Hanoi + Ho Chi Minh City",
         "body": "Traffic accidents are the leading cause of traveler death in Vietnam. Most major cities have dense motorbike traffic with minimal enforcement. If you ride, verify insurance covers it."},
        {"tone": "caution", "title": "Dengue + Japanese encephalitis risk",
         "body": "Dengue year-round in urban areas, peaks rainy season. Japanese encephalitis vaccination recommended for rural visits of 4+ weeks or repeated trips."},
        {"tone": "caution", "title": "Foreign prescriptions not recognized",
         "body": "A US prescription doesn't let you buy controlled medications in Vietnam. Bring your own supply with doctor's letter. Pharmacy counterfeit risk is real — stick to reputable chains like Pharmacity or Long Chau."},
        {"tone": "info", "title": "Medical evacuation to Bangkok or Singapore",
         "body": "Hanoi and Ho Chi Minh have decent private hospitals for routine care; complex cases evacuate to Bangkok (Bumrungrad) or Singapore."},
    ],
    "philippines": [
        {"tone": "danger", "title": "Rabies endemic in stray dogs",
         "body": "Dog bites are a leading traveler medical emergency. Post-exposure vaccination required within hours. Treat all scratches/bites as rabies exposure until cleared by a doctor."},
        {"tone": "caution", "title": "Dengue + chikungunya year-round",
         "body": "Elevated during rainy season (June–November). Daytime mosquitoes; use DEET throughout the day. Watch for fever + joint pain + rash."},
        {"tone": "caution", "title": "Typhoon season June–December",
         "body": "Infrastructure including hospitals can be disrupted during typhoons. Have trip-cancellation insurance and monitor PAGASA forecasts before booking."},
    ],
    "cambodia": [
        {"tone": "danger", "title": "Traffic accidents + motorbike crashes",
         "body": "Road safety is poor. Leading cause of foreign traveler death. Avoid night travel on rural roads."},
        {"tone": "caution", "title": "Dengue + malaria in rural border areas",
         "body": "Dengue urban/rural; malaria only in forested border regions (Ratanakiri, Mondulkiri) — see a travel doc about prophylaxis if visiting these."},
        {"tone": "info", "title": "Rural healthcare extremely limited",
         "body": "Outside Phnom Penh + Siem Reap, medical facilities are basic. Plan on evacuation to Bangkok for anything complex."},
    ],

    # ---------- East Asia ----------
    "japan": [
        {"tone": "danger", "title": "Adderall, Sudafed, and pseudoephedrine are prohibited",
         "body": "Japan's controlled-substance list is stricter than most travelers expect. Adderall, Vyvanse, Ritalin are banned — no import permit available. Pseudoephedrine (Sudafed, Claritin-D) is also prohibited. Check every medication before you fly."},
        {"tone": "caution", "title": "Upfront payment at hospitals is universal",
         "body": "Japanese hospitals expect full payment at point of service, including at ERs. Carry a credit card with a high limit. Some hospitals refuse treatment without upfront cash or card."},
        {"tone": "caution", "title": "Limited English outside Tokyo + Osaka",
         "body": "Medical communication is hard outside major cities. Use the Japan National Tourism Organization's multilingual hospital list or call 03-5774-0992 (TELL English crisis line in Tokyo)."},
        {"tone": "info", "title": "Earthquakes and tsunamis — know the drill",
         "body": "Japan has frequent seismic activity. Your hotel's evacuation route + the local tsunami warning signs are worth knowing. NHK World has English emergency broadcasts."},
    ],
    "south-korea": [
        {"tone": "caution", "title": "ADHD stimulants + benzos require permits",
         "body": "Amphetamines (Adderall), methylphenidate (Ritalin), and benzodiazepines need advance Korean MFDS approval. Don't bring without it."},
        {"tone": "caution", "title": "Air quality in Seoul (fine particulates)",
         "body": "Spring and winter see elevated PM2.5 from continental dust. Sensitive travelers (asthma, COPD) should bring N95 masks and check daily AQI."},
        {"tone": "info", "title": "Healthcare is excellent and fast",
         "body": "Korean hospitals rival Japan's with often faster service and more English availability. Severance (Yonsei) and Samsung Medical Center have international departments."},
    ],
    "china": [
        {"tone": "danger", "title": "Foreign prescriptions not accepted",
         "body": "A US prescription doesn't let you buy any controlled medication in China. Bring your own supply in original packaging with a doctor's letter. Counterfeit pharmaceutical risk outside major chains."},
        {"tone": "caution", "title": "Air quality in northern cities",
         "body": "Beijing, Tianjin, and northern China can have severe air-quality days, especially November–March. Respiratory-condition travelers should bring N95 masks and check daily AQI."},
        {"tone": "caution", "title": "CBD and cannabis — zero tolerance",
         "body": "Any cannabinoid product is prohibited. Customs uses THC testing. No exception for CBD isolate."},
        {"tone": "info", "title": "Tier-1 city hospitals are world-class",
         "body": "Beijing United Family, Shanghai United Family, and similar international-focused hospitals offer English service and direct billing. Rural healthcare is basic — evacuate to major cities for anything serious."},
    ],
    "hong-kong": [
        {"tone": "info", "title": "Excellent healthcare, high out-of-pocket",
         "body": "HK's private hospitals are among Asia's best, but tourists pay full rates — ER visits start at $500-800 USD. Carry insurance with a $50K+ cap."},
        {"tone": "caution", "title": "Medication rules align with mainland China in some cases",
         "body": "HK is more permissive than mainland but still restricts common ADHD meds + benzos. Bring prescription + doctor's letter."},
    ],

    # ---------- South Asia ----------
    "india": [
        {"tone": "danger", "title": "Road traffic accidents — leading cause of tourist death",
         "body": "India has among the world's highest road-traffic fatality rates. Hire drivers (even for short trips); avoid night driving outside cities; always wear a seatbelt."},
        {"tone": "caution", "title": "Gastro illness is near-universal for new visitors",
         "body": "Bottled water only, no ice outside high-end hotels, no raw/undercooked anything. Bring ciprofloxacin + loperamide + oral rehydration salts. See a doctor if symptoms persist beyond 3 days."},
        {"tone": "caution", "title": "Dengue + chikungunya in monsoon (June–October)",
         "body": "Both spread by day-biting mosquitoes. Use DEET throughout the day. Watch for sudden fever + severe joint pain."},
        {"tone": "caution", "title": "Air quality in Delhi, Kolkata, northern India",
         "body": "Winter pollution (November–February) can reach hazardous levels. Sensitive travelers should bring N95 masks and check daily AQI."},
        {"tone": "info", "title": "Private hospitals in major cities are excellent",
         "body": "Apollo, Fortis, Max — world-class for complex care at a fraction of Western prices. Avoid public hospitals; they're overwhelmed and under-resourced."},
    ],
    "nepal": [
        {"tone": "danger", "title": "Altitude sickness above 3,000m",
         "body": "Acute Mountain Sickness is the #1 cause of trekker evacuation in Nepal. High-altitude pulmonary edema (HAPE) and cerebral edema (HACE) can kill within hours. Ascend slowly, know the symptoms, and descend immediately if symptomatic."},
        {"tone": "danger", "title": "Helicopter evacuation is expensive + common",
         "body": "Trekking-related helicopter evacuation runs $5,000–20,000. Insurance with mountain-rescue coverage is mandatory for any trek above 2,500m."},
        {"tone": "caution", "title": "Gastro from water and food",
         "body": "Giardia and other waterborne illnesses are common. Bottled or filtered water only. Even teahouse water should be purified."},
    ],
    "sri-lanka": [
        {"tone": "caution", "title": "Dengue year-round, serious outbreaks periodically",
         "body": "Colombo and coastal cities see elevated dengue. Use DEET throughout the day."},
        {"tone": "caution", "title": "Leptospirosis from freshwater",
         "body": "Avoid swimming in freshwater during and after monsoon. Cover cuts if wading."},
    ],

    # ---------- Middle East ----------
    "uae": [
        {"tone": "danger", "title": "Strict medication rules — arrest for common drugs",
         "body": "Codeine, tramadol, Xanax, Adderall, and many cold medications require pre-approved import permits from the UAE Ministry of Health. Tourists have been arrested at Dubai airport for undeclared controlled substances. Get the permit 2-4 weeks before travel."},
        {"tone": "caution", "title": "CBD and cannabis — zero tolerance",
         "body": "Any cannabinoid product is illegal. Hair, blood, and urine testing at customs. Multi-year prison sentences have been handed down for trace amounts."},
        {"tone": "info", "title": "World-class hospitals, high upfront costs",
         "body": "Dubai and Abu Dhabi hospitals are excellent but expensive. An ER visit starts around $1,500 USD. Insurance is essentially mandatory."},
    ],
    "saudi-arabia": [
        {"tone": "danger", "title": "Medication rules mirror UAE + stricter",
         "body": "Strictest controlled-substance enforcement in the Gulf. Don't bring anything without pre-approved Ministry of Health authorization."},
        {"tone": "caution", "title": "Heat + dehydration in summer",
         "body": "Summer temperatures routinely exceed 45°C. Heat stroke is the leading medical emergency for outdoor visitors. Hydrate constantly, limit midday activity."},
    ],
    "israel": [
        {"tone": "caution", "title": "Active security environment",
         "body": "Check US State Department advisories before travel. Hospitals in Tel Aviv and Jerusalem are world-class; rural + West Bank medical access is limited."},
        {"tone": "info", "title": "Travel insurance must cover conflict zones if applicable",
         "body": "Standard travel insurance often excludes active conflict zones. Read the fine print; specialty insurers cover this."},
    ],
    "turkey": [
        {"tone": "caution", "title": "Earthquakes — know your hotel's evacuation route",
         "body": "Active seismic zones, especially southeastern Turkey. Major 2023 earthquake killed 50,000+. Check your hotel's construction era and evacuation signage."},
        {"tone": "info", "title": "Medical tourism for dental + cosmetic — verify credentials",
         "body": "Turkey is a medical-tourism hub. JCI-accredited facilities (Acibadem, Memorial) are world-class. Avoid the cheapest operators — quality varies wildly."},
    ],
    "egypt": [
        {"tone": "caution", "title": "Gastro — bottled water only",
         "body": "Tap water unsafe outside 5-star hotels. Skip ice at street vendors. Salads washed in tap water are a common source."},
        {"tone": "caution", "title": "Schistosomiasis in the Nile",
         "body": "Don't swim in the Nile or irrigation canals. Parasitic worms enter through skin contact with freshwater."},
        {"tone": "info", "title": "Cairo hospitals adequate for basics; evacuate for complex cases",
         "body": "Private hospitals in Cairo handle routine care. Serious trauma or complex surgery typically evacuates to Europe (Athens, Frankfurt) or Dubai."},
    ],

    # ---------- Africa ----------
    "south-africa": [
        {"tone": "danger", "title": "Malaria in Kruger + northeast regions",
         "body": "Kruger National Park, Limpopo, and Mpumalanga are malaria zones. Prophylaxis required. Use DEET + long sleeves at dusk. Most of Cape Town and Garden Route is malaria-free."},
        {"tone": "caution", "title": "Crime-related medical emergencies",
         "body": "Higher violent-crime risk than most destinations. Stay in vetted areas, avoid unlit streets at night, don't display valuables."},
        {"tone": "info", "title": "Private healthcare is world-class",
         "body": "Mediclinic, Netcare, Life Healthcare — South African private hospitals rival anything in the US. Avoid public hospitals; they're overwhelmed."},
    ],
    "kenya": [
        {"tone": "danger", "title": "Malaria below 2,500m elevation",
         "body": "Most of Kenya below 2,500m is malaria-transmission zone. Prophylaxis required. Nairobi city center (1,800m) is lower-risk but not zero. Coastal areas (Mombasa, Diani) are highest-risk."},
        {"tone": "danger", "title": "Yellow fever vaccination required",
         "body": "Required for entry if arriving from an endemic country. Recommended for all travelers regardless. Must be administered 10+ days before travel."},
        {"tone": "caution", "title": "Safari medical considerations",
         "body": "Tetanus, rabies, and trauma risk on safari. Bring DEET + long sleeves + sunscreen. Medical evacuation to Nairobi for anything serious."},
    ],
    "tanzania": [
        {"tone": "danger", "title": "Malaria below 1,800m",
         "body": "All of Tanzania except Kilimanjaro heights. Prophylaxis required."},
        {"tone": "danger", "title": "Yellow fever required for entry",
         "body": "Required if arriving from any endemic country. Get it 10+ days before travel."},
        {"tone": "caution", "title": "Altitude sickness on Kilimanjaro",
         "body": "Summit is 5,895m. Acute Mountain Sickness kills hikers every year. Proper acclimatization (7+ day climbs) matters more than fitness."},
    ],
    "morocco": [
        {"tone": "caution", "title": "Altitude sickness in the Atlas Mountains",
         "body": "Toubkal climbs reach 4,167m. AMS risk above 3,000m. Ascend gradually."},
        {"tone": "caution", "title": "Rabies risk from stray dogs",
         "body": "Common in Marrakech, Fez medinas. Post-exposure vaccination essential within hours of any bite."},
        {"tone": "info", "title": "Private hospitals in Casablanca, Rabat are reliable",
         "body": "Rural healthcare is limited. Medical evacuation to Europe (Madrid, Paris) for serious cases."},
    ],

    # ---------- Europe ----------
    "france": [
        {"tone": "info", "title": "Tap water is universally safe",
         "body": "Any French tap water (l'eau du robinet) is potable. Restaurants that charge for bottled water are a tourist trick."},
        {"tone": "info", "title": "Pharmacies: green cross sign, Sunday rotation",
         "body": "French pharmacies (pharmacies) have a rotating on-call schedule on Sundays — check the posted list in any closed pharmacy window."},
        {"tone": "info", "title": "EHIC/GHIC is for EU/UK residents only",
         "body": "US travelers pay out-of-pocket or bill travel insurance. Public hospitals are cheaper than private but have long ER waits."},
    ],
    "germany": [
        {"tone": "info", "title": "Tap water safe, pharmacies (Apotheke) closed Sundays",
         "body": "Sunday emergency pharmacies rotate — look for Notdienst signage. Tap water is universally safe."},
        {"tone": "info", "title": "Private health insurers accept many international cards",
         "body": "Private clinics generally accept major international cards. Public hospitals (Krankenhaus) may require cash upfront for non-emergencies."},
    ],
    "italy": [
        {"tone": "info", "title": "Tap water safe except where marked non potabile",
         "body": "Italian tap water is universally safe. Public fountains are too. Only avoid if explicitly marked non potabile (not potable)."},
        {"tone": "caution", "title": "Pharmacy Sundays and August closures",
         "body": "Many pharmacies close for much of August. Rotating farmacia di turno is posted in closed pharmacy windows."},
    ],
    "spain": [
        {"tone": "info", "title": "Excellent public healthcare; pharmacies extensive",
         "body": "Spanish farmacias (green cross) can advise on most minor issues without a doctor visit. EHIC/GHIC accepted; US travelers pay out-of-pocket."},
    ],
    "united-kingdom": [
        {"tone": "info", "title": "NHS covers emergencies at free point-of-use",
         "body": "Emergency NHS care is free regardless of nationality or insurance. Non-emergency care is not — US travel insurance should cover routine medical needs."},
        {"tone": "caution", "title": "Pseudoephedrine restricted",
         "body": "Pseudoephedrine (Sudafed) is behind the pharmacist counter in the UK; small quantities only per transaction."},
    ],
    "greece": [
        {"tone": "caution", "title": "Sunburn + heatstroke in summer",
         "body": "Temperatures routinely exceed 40°C on southern islands. Hydrate, limit midday sun, and use SPF 50+."},
        {"tone": "info", "title": "Tap water: safe in mainland, bottled on most islands",
         "body": "Athens and mainland tap water is safe. Santorini, Mykonos, and smaller islands rely on desalination or cisterns — bottled water recommended."},
    ],

    # ---------- Americas ----------
    "mexico": [
        {"tone": "danger", "title": "Never drink tap water — ice is the trap",
         "body": "Tap water unsafe nationwide. Ice at tourist restaurants is usually safe (purified-water ice is standard); street vendors are not. Bottled water for drinking and brushing teeth."},
        {"tone": "caution", "title": "Private hospitals in tourist zones expect upfront payment",
         "body": "Mexico City and resort-area private hospitals (Hospital ABC, Centro Médico ABC) are excellent but require upfront payment. Carry a credit card or have insurance with direct-billing."},
        {"tone": "caution", "title": "Altitude sickness in Mexico City (2,240m)",
         "body": "CDMX sits above 2,000m. Mild altitude symptoms are common on arrival. Avoid alcohol the first day; hydrate."},
        {"tone": "info", "title": "Dengue + Zika in coastal + jungle areas",
         "body": "Caribbean and Pacific coasts, Yucatán. Use DEET. Pregnant travelers should consult a doctor about Zika risk."},
    ],
    "brazil": [
        {"tone": "danger", "title": "Dengue epidemic since 2024",
         "body": "Brazil reporting record dengue cases nationwide. Use DEET constantly during the day. Seek care for any fever within 2 weeks of return."},
        {"tone": "danger", "title": "Yellow fever vaccination required for many areas",
         "body": "Required for Amazon region, Pantanal, and most of the interior. Recommended for all travelers. Must be administered 10+ days before travel."},
        {"tone": "caution", "title": "Crime-related medical risk in major cities",
         "body": "Rio and São Paulo have elevated violent-crime rates. Stick to vetted areas, don't flash valuables, use ride-hailing rather than walking at night."},
    ],
    "argentina": [
        {"tone": "caution", "title": "Altitude in Salta, Jujuy, northern Andes",
         "body": "Salta Province can reach 4,000m+ on tourist routes. AMS risk; acclimatize gradually."},
        {"tone": "info", "title": "Healthcare quality: excellent in Buenos Aires, variable elsewhere",
         "body": "Private hospitals in BA (Hospital Italiano, Hospital Alemán) rival US standards. Rural care is basic."},
    ],
    "peru": [
        {"tone": "danger", "title": "Altitude sickness in Cusco + Machu Picchu",
         "body": "Cusco sits at 3,400m — AMS affects most visitors in some form. Fly into Lima (sea level) first, acclimatize 2+ days in Cusco before trekking. Coca tea helps; altitude-sickness medication (Diamox) is more reliable."},
        {"tone": "caution", "title": "Yellow fever for Amazon regions",
         "body": "Required for Madre de Dios, Loreto, and Amazonas. 10+ days before travel."},
        {"tone": "caution", "title": "Traveler's diarrhea is near-universal",
         "body": "Bottled water, no ice at budget venues, no raw fruit you didn't peel yourself. Bring ciprofloxacin + loperamide + oral rehydration salts."},
    ],
    "costa-rica": [
        {"tone": "caution", "title": "Dengue year-round, peaks rainy season",
         "body": "Coastal and lowland regions. Use DEET."},
        {"tone": "caution", "title": "Adventure-sport injuries",
         "body": "Ziplining, surfing, whitewater, ATV. Verify your travel insurance covers adventure activities — most default policies exclude them."},
    ],
    "colombia": [
        {"tone": "caution", "title": "Yellow fever for jungle regions",
         "body": "Required for Amazon and Los Llanos departments. Recommended for all travelers."},
        {"tone": "caution", "title": "Altitude in Bogotá (2,640m) + Andes",
         "body": "Mild AMS common on arrival. Avoid alcohol first 24 hours."},
        {"tone": "info", "title": "Healthcare in Bogotá + Medellín is excellent + affordable",
         "body": "Private hospitals (Fundación Valle del Lili, Hospital Pablo Tobón) offer world-class care at a fraction of US prices. Popular for medical tourism."},
    ],
    "canada": [
        {"tone": "info", "title": "Healthcare for visitors: pay out-of-pocket",
         "body": "Canadian single-payer healthcare covers residents only. Visitors face full billing — ER visits start around $1,000 CAD. Travel insurance is essential."},
        {"tone": "caution", "title": "Remote-area medical evacuation is expensive",
         "body": "Yukon, Northwest Territories, Nunavut, and remote BC/Alberta: air ambulance runs $20,000-100,000 CAD. Insurance with $250K+ evacuation coverage is mandatory for wilderness travel."},
    ],
    "united-states": [
        {"tone": "danger", "title": "Healthcare is the most expensive in the world",
         "body": "An uninsured ER visit can run $5,000-50,000+. Travel insurance with adequate medical coverage ($250K minimum) is essential for all visitors."},
        {"tone": "caution", "title": "EMS is expensive — ambulances $1,000-5,000",
         "body": "Call 911 for life-threatening emergencies only. For non-emergencies, an Uber to an urgent care is 1/10th the cost."},
    ],

    # ---------- Oceania ----------
    "australia": [
        {"tone": "danger", "title": "Dangerous wildlife — mostly avoidable",
         "body": "Jellyfish (box, Irukandji) on northern beaches November–April. Snake bites in bush. Saltwater crocodiles in northern rivers. Most deaths are from water + sun, not wildlife."},
        {"tone": "danger", "title": "Sun + heat are the actual killers",
         "body": "UV index routinely extreme. SPF 50+, reapply every 2 hours. Dehydration + heat stroke are the #1 medical emergency category."},
        {"tone": "info", "title": "Medicare is for residents; visitors pay",
         "body": "Excellent public healthcare, but visitors pay full rates unless from a reciprocal-agreement country (UK, NZ, Ireland, Sweden, etc.). Travel insurance essential."},
    ],
    "new-zealand": [
        {"tone": "caution", "title": "Adventure-sport injuries",
         "body": "Bungee, skiing, canyoning, white-water rafting. ACC (Accident Compensation Corporation) covers treatment for accidents regardless of fault, but evacuation and repatriation aren't included — travel insurance still essential."},
        {"tone": "info", "title": "Sun exposure + ozone hole",
         "body": "UV in NZ summer is among the world's highest. SPF 50+, reapply frequently."},
    ],

    # ---------- High-risk / dangerous destinations ----------
    "afghanistan": [
        {"tone": "danger", "title": "US State Department: Do Not Travel (Level 4)",
         "body": "Active armed conflict, kidnapping, terrorism. US citizens should not travel to Afghanistan. If you must, professional security support and advance evacuation planning are mandatory."},
        {"tone": "danger", "title": "Healthcare is severely degraded",
         "body": "Decades of conflict have destroyed the healthcare system. Reliable medical care is limited to Kabul's NGO-supported facilities. Serious illness requires evacuation, which is logistically complex."},
        {"tone": "danger", "title": "Polio vaccination required for long stays",
         "body": "Afghanistan is one of the world's last polio reservoirs. Booster required within 12 months if staying 4+ weeks."},
    ],
    "somalia": [
        {"tone": "danger", "title": "US State Department: Do Not Travel",
         "body": "Active terrorism, piracy, civil unrest. Traveler kidnappings are frequent."},
        {"tone": "danger", "title": "Healthcare effectively unavailable",
         "body": "Rely on private medical support through security contractors. Evacuation is logistically difficult."},
    ],
    "syria": [
        {"tone": "danger", "title": "US State Department: Do Not Travel",
         "body": "Active conflict, arbitrary detention. US citizens should not travel to Syria."},
    ],
    "north-korea": [
        {"tone": "danger", "title": "US State Department: Do Not Travel",
         "body": "US passports are not valid for travel to DPRK without special validation. Arrest and long-term detention of US citizens is a real risk."},
    ],
    "yemen": [
        {"tone": "danger", "title": "Active armed conflict",
         "body": "Civil war, missile strikes, cholera outbreaks. No reliable medical care outside Aden."},
    ],
    "venezuela": [
        {"tone": "danger", "title": "Healthcare collapse + medication shortages",
         "body": "Most pharmacies lack basic medications. Hospitals intermittently without power, water, supplies. Bring everything you need; medical evacuation essential for anything serious."},
        {"tone": "caution", "title": "Yellow fever + malaria in interior",
         "body": "Required for Amazon/Bolivar states; malaria in same regions."},
    ],

    # ---------- Small-volume but common traveler destinations ----------
    "iceland": [
        {"tone": "caution", "title": "Weather-related medical emergencies",
         "body": "Hypothermia, falls on ice, motor-vehicle accidents in changing conditions. Excellent public healthcare but medical evacuation from remote areas is expensive."},
        {"tone": "info", "title": "Healthcare: emergencies covered, rest is expensive",
         "body": "European public healthcare but non-emergency care is pricey for visitors. Travel insurance essential."},
    ],
    "switzerland": [
        {"tone": "danger", "title": "Most expensive healthcare in Europe",
         "body": "A single ER visit can exceed $5,000 USD. Travel insurance is not optional. Mountain-rescue coverage is essential if you're skiing or hiking."},
        {"tone": "caution", "title": "Altitude sickness above 3,000m",
         "body": "Jungfraujoch (3,454m), Matterhorn Glacier Paradise (3,883m). Mild AMS common for visitors ascending quickly from valleys."},
    ],
    "singapore": [
        {"tone": "danger", "title": "Zero tolerance for controlled substances",
         "body": "Capital punishment for drug trafficking; strict penalties for possession. All medications including melatonin, Adderall, codeine require advance Health Sciences Authority approval."},
        {"tone": "info", "title": "Healthcare is world-class, expensive for tourists",
         "body": "Mount Elizabeth, Raffles, Gleneagles — among Asia's best hospitals. Tourists pay full rates; an ER visit starts around SGD $300-500. Insurance essential."},
    ],
}


# -------------------------------------------------------------------
# Programmatic derivation for countries without curated entries
# -------------------------------------------------------------------

def derive_default_risks(country_data: dict, yf_required: bool, strict_meds: bool) -> list:
    """Build a sensible ranked top-risks list from the country's JSON data
    when no curated entry exists."""
    risks = []

    water = (country_data.get("waterSafety") or "").lower()
    quality = country_data.get("qualityRating") or 3

    if water == "unsafe":
        risks.append({
            "tone": "caution",
            "title": "Tap water is not safe — bottled water only",
            "body": "Drink bottled or properly treated water. Skip ice at budget venues and street vendors. Brush your teeth with bottled water where tap is questionable.",
        })
    elif water == "caution":
        risks.append({
            "tone": "caution",
            "title": "Tap water safety varies by region",
            "body": "Major cities typically treat water, but rural areas and older infrastructure can be unreliable. Bottled water is a cheap insurance policy.",
        })

    if yf_required:
        risks.append({
            "tone": "danger",
            "title": "Yellow fever vaccination required or strongly recommended",
            "body": "Verify requirements at your destination's embassy. Vaccination must be administered 10+ days before travel and is documented on a yellow International Certificate of Vaccination.",
        })

    if strict_meds:
        risks.append({
            "tone": "caution",
            "title": "Strict medication-import enforcement",
            "body": "Controlled substances (opioids, ADHD stimulants, benzodiazepines) require advance permits. Check each of your prescriptions against the destination's pharmaceutical authority before flying.",
        })

    if quality <= 2:
        risks.append({
            "tone": "caution",
            "title": "Healthcare is limited — plan for medical evacuation",
            "body": "Routine care is available in major cities; complex trauma, cardiac, or surgery typically requires air evacuation to a regional hub. Travel insurance with $250K+ evacuation coverage is essential.",
        })

    # Fallback: generic advice if nothing else matched
    if not risks:
        risks.append({
            "tone": "info",
            "title": "Check your vaccinations and carry prescription documentation",
            "body": "Ensure routine vaccinations are up to date, bring your prescription medications in original packaging with a doctor's letter, and verify your travel insurance covers international medical care + evacuation.",
        })

    return risks


def top_risks_for(slug: str, country_data: dict, yf_required: bool, strict_meds: bool) -> list:
    """Return top risks for a country — curated if available, derived otherwise."""
    if slug in CURATED:
        return CURATED[slug]
    return derive_default_risks(country_data, yf_required, strict_meds)
