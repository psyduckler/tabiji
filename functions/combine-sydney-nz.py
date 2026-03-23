#!/usr/bin/env python3
"""Combine all parts and write sydney-nz-data.json"""
import json, subprocess, sys, os

def run_part(filename):
    result = subprocess.run(
        [sys.executable, filename],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(filename))
    )
    if result.returncode != 0:
        print(f"ERROR in {filename}: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)

base = os.path.dirname(os.path.abspath(__file__))

days1 = run_part(os.path.join(base, "gen-part1.py"))
days2 = run_part(os.path.join(base, "gen-part2.py"))
days3 = run_part(os.path.join(base, "gen-part3-fixed.py"))
days4 = run_part(os.path.join(base, "gen-part4.py"))

all_days = days1 + days2 + days3 + days4
print(f"Total days: {len(all_days)} (days {all_days[0]['num']}-{all_days[-1]['num']})", file=sys.stderr)

# Verify sequential numbering
for i, d in enumerate(all_days, 1):
    if d['num'] != i:
        print(f"WARNING: Day numbering gap at index {i}, day num={d['num']}", file=sys.stderr)

data = {
    "destination": "Australia + New Zealand",
    "countryEmoji": "🇦🇺🇳🇿",
    "title": "Australia & New Zealand Grand Tour",
    "subtitle": "46 Days: Sydney, New Zealand, Queensland, Northern Territory, South Australia, Victoria & Tasmania",
    "description": "An extraordinary 46-day journey across two countries — from Sydney's harbour to Auckland's volcanoes, Wellington's cafés to the Great Barrier Reef, the ancient Uluru to the wild Tasmanian wilderness. A trip that touches Australia's soul: its landscapes, its people, its Indigenous heritage, and the personal meaning of a great grandfather's grave in Auckland. Vegetarian-friendly throughout, budget-conscious, and packed with the must-see moments of a lifetime.",
    "duration": "46 days",
    "dates": "May 3 – June 17, 2026",
    "budget": "$2,000-$5,000 per person",
    "pace": "Active with rest days",
    "bestFor": "Couples, adventure travellers, vegetarians, culture lovers, nature seekers",
    "highlights": [
        "Sydney Harbour — Opera House, Harbour Bridge walk, and Bondi to Coogee",
        "Blue Mountains — Three Sisters and ancient rainforest",
        "Auckland, New Zealand — volcanoes, Rangitoto Island, and a deeply personal grave visit",
        "Wellington — Te Papa, Weta Workshop, and the coolest café culture in the world",
        "Byron Bay and Yamba — east coast beach towns and family connections",
        "Great Barrier Reef — snorkelling the world's largest coral ecosystem",
        "Uluru and Kata Tjuta — the Red Centre at sunrise and sunset",
        "Kakadu National Park — 20,000-year-old Aboriginal rock art and crocodiles",
        "Adelaide, Barossa Valley, and McLaren Vale — food and wine paradise",
        "Great Ocean Road — Twelve Apostles and the most dramatic coastal drive in Australia",
        "Melbourne — street art, world-class coffee, and the Moroccan Soup Bar",
        "Tasmania — MONA, Port Arthur, Freycinet, and friends & family",
        "Daintree Rainforest — oldest on Earth, where the rainforest meets the reef"
    ],
    "essentials": [
        {
            "title": "🗺️ The Route",
            "text": "Sydney (3 days) → Auckland NZ (3 days) → Wellington NZ including conference (6 days) → Byron Bay & Yamba (4 days) → Queensland Coast (5 days: Sunshine Coast, Whitsundays, Great Barrier Reef) → Cairns & Daintree (2 days) → Darwin & Northern Territory (5 days: Litchfield, Kakadu, Uluru) → Adelaide & surrounds (3 days) → Great Ocean Road (2 days) → Melbourne (2 days) → Tasmania (5 days) → Return Sydney (2 days)"
        },
        {
            "title": "🌿 Vegetarian Australia",
            "text": "Australia is incredibly vegetarian-friendly — especially in cities. Sydney's Newtown, Melbourne's Fitzroy, and Byron Bay are vegetarian paradises. Outback areas (Kakadu, Uluru) have limited options — always carry snacks. The markets (Salamanca, Adelaide Central, Airlie, Mindil Beach) have excellent vegetarian stalls. Ask for 'veggie option' at any pub — halloumi burgers and mushroom dishes are now standard. Outside major cities, always confirm ahead."
        },
        {
            "title": "💰 Budget Reality — $2-5k/person",
            "text": "This budget is achievable with smart choices. Flight costs are significant — shop Jetstar/Tigerair domestically, book 3-4 weeks ahead. Accommodation: hostels $30-50/night, Airbnb $60-120, motels $80-150. Many highlights are free: coastal walks, beaches, national park lookouts, markets. Big ticket items to budget for: Great Barrier Reef trip ($200-250), Scenic World Katoomba ($53), Weta Workshop ($49), Zealandia ($24), Kakadu park pass ($40), Port Arthur ($45). National Parks: buy passes upfront."
        },
        {
            "title": "🚗 Getting Around",
            "text": "For the coastal leg (Byron to Cairns), renting a car gives maximum flexibility. Queensland to Darwin is a fly (don't drive — it's 3,000 km of nothing). Adelaide → Melbourne: Great Ocean Road requires a car. In cities: Opal card (Sydney), Myki (Melbourne), AT HOP (Auckland), Snapper card (Wellington). Between cities: Jetstar and Virgin Australia are the budget choices. Book flights 3-6 weeks ahead for best prices."
        },
        {
            "title": "🌡️ May–June Weather",
            "text": "Autumn in southern Australia (mild, 12-22°C in Sydney/Melbourne), and dry season beginning in the north. Darwin in May is coming out of the wet — hot (30°C) and humid with afternoon storms possible. Uluru in May/June is perfect: 20°C days, cold nights. Tasmania in June can be cold (5-12°C) with possible snow at altitude. Queensland and Cairns: beautiful and warm (25-28°C). Pack layers for the south and light, breathable clothes for the tropics."
        },
        {
            "title": "🐊 Wildlife & Safety",
            "text": "Crocodiles: NEVER swim in unmarked waterways in the NT and North QLD. Signs mean something. Stingers (jellyfish): stinger suits or swim in netted areas Oct-May in North QLD. Dingoes on Fraser Island: keep 5m distance, never feed, never turn your back. Snakes: most are non-aggressive, but watch where you step in bush. If bitten: compression bandage, don't wash the wound, call 000. Sharks: swim between the flags at patrolled beaches. Australia's wildlife is extraordinary but must be respected."
        }
    ],
    "days": all_days,
    "budgetTable": [
        {"category": "Flights (domestic Australia + NZ)", "budget": "$600-900", "notes": "~8-10 domestic flights. Book Jetstar 3-4 weeks ahead. Sydney↔NZ is biggest cost."},
        {"category": "Accommodation (46 nights)", "budget": "$1,200-2,500", "notes": "Mix of hostels ($35-50), Airbnbs ($70-120), and occasional motels ($90-150)"},
        {"category": "Food (vegetarian, mix of cafés + cooking)", "budget": "$800-1,500", "notes": "$25-45/day/person. Markets, cafés, occasional fine dining. Cooking some meals saves a lot."},
        {"category": "Activities & Entry Fees", "budget": "$500-900", "notes": "GBR trip $220, Uluru park + tours $200, Kakadu $40, Scenic World $53, Weta $49, MONA $35, Port Arthur $45, etc."},
        {"category": "Transport (car hire + fuel)", "budget": "$400-800", "notes": "Car hire for QLD coast, Great Ocean Road, and Tasmania legs. Fuel costs for long drives."},
        {"category": "Miscellaneous & Buffer", "budget": "$200-400", "notes": "Travel insurance (essential!), SIM cards, laundry, shopping, unexpected costs"},
        {"category": "TOTAL ESTIMATE (per person)", "budget": "$3,700-7,000", "notes": "Budget end possible with hostel beds and self-catering. $5k is comfortable for 2 sharing costs."}
    ],
    "practicalInfo": [
        {
            "title": "🛂 Visas & Entry",
            "items": [
                "New Zealand: Australian citizens enter visa-free. Other nationalities: NZ Electronic Travel Authority (NZeTA) required — apply online, NZ$23.",
                "Australia: Most visitors need an ETA (Electronic Travel Authority) or eVisitor visa. Apply at immi.homeaffairs.gov.au. US/UK/EU citizens typically get the eVisitor (subclass 651) — free and instant.",
                "NZ biosecurity is strict: declare ALL food items, including sealed packets. Fines are significant.",
                "Australian biosecurity: same strict rules. Fruit, vegetables, honey, seeds, animal products must be declared."
            ]
        },
        {
            "title": "📱 SIM Cards & Connectivity",
            "items": [
                "Australia: Telstra has the best rural coverage (essential for the NT and outback). $30-50 for a prepaid month. Buy at the airport or any 7-Eleven.",
                "New Zealand: Spark or Vodafone. $30 for a month of data. Available at airports.",
                "Uluru, Kakadu, and remote areas: Telstra only. Optus and Vodafone don't work outside major highways.",
                "Download offline maps (Google Maps or Maps.me) for all regions before leaving cities."
            ]
        },
        {
            "title": "💊 Health & Insurance",
            "items": [
                "Travel insurance is ESSENTIAL. Medical care in Australia is excellent but expensive without insurance.",
                "Reciprocal healthcare: UK and Irish citizens have a reciprocal agreement with Australia. NZ citizens covered in both countries.",
                "Sun protection: Australian UV is extreme. SPF50+, reapply every 2 hours. A hat is not optional.",
                "Reef-safe sunscreen: essential for any reef snorkelling — check the bottle (no oxybenzone/octinoxate).",
                "Vaccinations: No required vaccinations, but be up to date on routine vaccines."
            ]
        },
        {
            "title": "🌿 Respecting Country",
            "items": [
                "DO NOT CLIMB ULURU. It is permanently closed (Oct 2019) and climbing is deeply offensive to the Anangu people.",
                "In Kakadu and other Aboriginal lands: some areas and objects are sacred. Respect all signage about photography restrictions.",
                "The Daintree sits on Kuku Yalanji Country. Seek out Indigenous-led tours — the Dreamtime Walk at Mossman Gorge is excellent.",
                "Leave No Trace in all national parks. Take all rubbish out. Don't pick wildflowers or move rocks.",
                "Dingoes on Fraser Island are wild animals. They look like dogs but have fatally attacked children. Keep 5m distance, never feed them."
            ]
        }
    ]
}

outfile = os.path.join(base, "sydney-nz-data.json")
with open(outfile, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Written to {outfile}")
print(f"   {len(all_days)} days, {len(data['essentials'])} essentials, {len(data['budgetTable'])} budget rows, {len(data['practicalInfo'])} practical sections")
