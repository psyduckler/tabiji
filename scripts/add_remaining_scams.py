#!/usr/bin/env python3
"""Add remaining 12 destinations to the scams research batch."""
import json

with open("/Users/bjh/Documents/tabiji/scams/research/batch_new_50.json") as f:
    data = json.load(f)

additional = [
  {
    "city": "Rishikesh",
    "country": "India",
    "country_code": "in",
    "flag": "\U0001f1ee\U0001f1f3",
    "scams": [
      {
        "scam_name": "The Fake Ashram Yoga Teacher Training",
        "location": "Tapovan, Laxman Jhula area",
        "danger_level": "medium",
        "story": "You sign up for a 200-hour Yoga Teacher Training at an ashram advertising $500 for 28 days. The 'certification' comes from a made-up yoga alliance, classes have 60+ students, and the guru has no formal training. Some ashrams operate like factories, churning out uncertified yoga teachers. Others have darker issues \u2014 there have been documented cases of ashram operators targeting solo female travelers.",
        "red_flags": ["Price well below $800-1,200 for legitimate 200-hour YTT", "No Yoga Alliance (YA) certification mentioned or verifiable", "Ashram has few reviews or reviews mentioning overcrowding", "Guru has no verifiable credentials or lineage"],
        "how_to_avoid": ["Verify the school is registered with Yoga Alliance (yogaalliance.org)", "Read recent Google and TripAdvisor reviews focusing on class size and quality", "Budget $800-1,500 for a legitimate 200-hour YTT in Rishikesh", "Speak to recent graduates before enrolling \u2014 legitimate schools will connect you"],
        "reddit_sources": ["r/yoga: 'Many Rishikesh YTT schools are diploma mills \u2014 verify Yoga Alliance registration'", "r/india: 'Rishikesh yoga teacher training quality varies wildly \u2014 research thoroughly before paying'"]
      },
      {
        "scam_name": "The Fake GST Billing Scam",
        "location": "Shops and restaurants citywide",
        "danger_level": "low",
        "story": "Restaurants and shops in Rishikesh charge GST (Goods and Services Tax) of 5-18% on your bill. Many charge this tax without valid GST registration \u2014 meaning the tax goes straight into the owner's pocket, not to the government. In 2024, Indian authorities flagged widespread fake GST billing in tourist areas including Rishikesh.",
        "red_flags": ["GST charged but no GSTIN number printed on the receipt", "Restaurant adds GST to prices already listed as inclusive", "Bill has a handwritten GST line rather than a printed tax calculation"],
        "how_to_avoid": ["Ask for a proper GST invoice with the GSTIN number", "Verify the GSTIN on the government portal (gst.gov.in)", "If a business charges GST without displaying their registration, the charge may not be legitimate", "Small eateries and street food vendors are exempt from GST"],
        "reddit_sources": ["r/india: 'Fake GST billing in Rishikesh is rampant \u2014 check for the GSTIN on your receipt'", "r/travel: 'Some Rishikesh restaurants charge tax that goes into their pocket, not the government'"]
      }
    ]
  },
  {
    "city": "Stone Town",
    "country": "Tanzania",
    "country_code": "tz",
    "flag": "\U0001f1f9\U0001f1ff",
    "scams": [
      {
        "scam_name": "The Beach Boy Commission Hustle",
        "location": "Nungwi Beach, Kendwa Beach, Stone Town waterfront",
        "danger_level": "medium",
        "story": "Beach boys are young men who offer tours, boat trips, and restaurant recommendations on Zanzibar beaches. Some are legitimate, but many earn commission by steering you to overpriced activities and restaurants. A snorkeling trip that costs $15 through your hotel becomes $40 through a beach boy. What starts as a friendly conversation becomes persistent harassment if you decline.",
        "red_flags": ["Persistent approach on the beach with tour offers", "Claims of special access or exclusive deals", "Becomes aggressive or guilt-trips when you decline", "Follows you down the beach after you say no"],
        "how_to_avoid": ["Book activities through your hotel or verified operators", "A firm but polite no is sufficient \u2014 do not engage in extended negotiations", "Standard prices: snorkeling $15-25, sunset dhow cruise $20-30, spice tour $20-30", "Report persistent harassment to your hotel"],
        "reddit_sources": ["r/travel: 'Zanzibar beach boys are relentless \u2014 book through your hotel and ignore the beach sellers'", "r/solotravel: 'The beach boy commission in Zanzibar doubles the price of everything \u2014 go direct'"]
      },
      {
        "scam_name": "The Stone Town Ferry Ticket Office Scam",
        "location": "Stone Town port area",
        "danger_level": "medium",
        "story": "You arrive at Stone Town port to buy a ferry ticket to Dar es Salaam. Before reaching the official Azam Marine counter, you pass through a gauntlet of unofficial booking offices that look official. They charge a markup of $10-20 per ticket, sometimes selling you a different class than promised.",
        "red_flags": ["Ticket office is outside the port terminal building", "Price above the official Azam Marine listed fare", "Agent offers a discount for cash payment"],
        "how_to_avoid": ["Buy ferry tickets online at azammarine.com before arriving", "The official booking office is inside the terminal", "Official fares: economy $35, business $40, VIP $50 (Zanzibar to Dar)", "Cross-check the ticket class with what the agent quoted"],
        "reddit_sources": ["r/travel: 'Walk past all the fake ticket offices at Stone Town port \u2014 the official Azam counter is inside'", "r/solotravel: 'Buy Zanzibar ferry tickets on the Azam website to avoid the port markup scam'"]
      }
    ]
  },
  {
    "city": "Gold Coast",
    "country": "Australia",
    "country_code": "au",
    "flag": "\U0001f1e6\U0001f1fa",
    "scams": [
      {
        "scam_name": "The Timeshare Presentation Trap",
        "location": "Surfers Paradise, Cavill Avenue area",
        "danger_level": "medium",
        "story": "A friendly person on Cavill Avenue offers you free theme park tickets or a spa package \u2014 all you need to do is attend a 90-minute presentation. The presentation lasts 3-4 hours and involves aggressive hard-sell tactics for timeshare or holiday club memberships costing A$10,000-50,000.",
        "red_flags": ["Free gifts in exchange for attending a presentation", "Presentation always lasts much longer than advertised", "High-pressure sales with time-limited discounts"],
        "how_to_avoid": ["Never accept free gifts conditional on attending a sales presentation", "If you agree, you can leave at any time \u2014 just stand up and walk out", "No legitimate investment requires a same-day decision"],
        "reddit_sources": ["r/australia: 'Surfers Paradise timeshare presentations are a 4-hour nightmare'", "r/travel: 'Gold Coast timeshare scam \u2014 the free theme park tickets cost you 4 hours of your vacation'"]
      },
      {
        "scam_name": "The Nightclub Tab Inflation",
        "location": "Surfers Paradise nightlife strip",
        "danger_level": "high",
        "story": "A promoter on the street offers free entry and a free drink at a nearby club. Inside, you run a tab. The bill is inflated with drinks you didn't order, or your card is charged multiple times. Some clubs target intoxicated tourists with inflated tabs, using bouncers to pressure payment.",
        "red_flags": ["Free entry and drink offers from street promoters", "Bar doesn't show you the charge before tapping your card", "Bouncer involvement when questioning the bill"],
        "how_to_avoid": ["Pay for each drink individually in cash rather than running a tab", "Check every charge on your card before leaving", "Set a spending limit via your banking app", "Stick to well-known, reviewed venues"],
        "reddit_sources": ["r/australia: 'Surfers Paradise clubs are known for overcharging drunk tourists \u2014 pay cash per drink'", "r/goldcoast: 'Never run a tab at Cavill Avenue clubs'"]
      }
    ]
  },
  {
    "city": "Dalat",
    "country": "Vietnam",
    "country_code": "vn",
    "flag": "\U0001f1fb\U0001f1f3",
    "scams": [
      {
        "scam_name": "The Canyoning Tour Safety Gamble",
        "location": "Tour agencies on Nguyen Chi Thanh Street",
        "danger_level": "high",
        "story": "Dalat is famous for canyoning \u2014 rappelling down waterfalls. Budget agencies offer it for $25 when the standard price is $60-80. The cheap tours use frayed ropes, guides without first aid training, and skip safety briefings. People have died canyoning in Dalat.",
        "red_flags": ["Price under $40 for a canyoning tour", "No mention of safety equipment or guide certifications", "No waiver or safety briefing before the activity"],
        "how_to_avoid": ["Book with Phat Tire Ventures or Highland Sport Travel", "Budget $60-80 per person for a safe canyoning experience", "Ask about guide certifications and equipment age"],
        "reddit_sources": ["r/vietnam: 'Dalat canyoning on the cheap is genuinely dangerous \u2014 use Phat Tire or Highland Sport'", "r/travel: 'The $25 canyoning tour in Dalat uses equipment you wouldn't trust your life with'"]
      },
      {
        "scam_name": "The Easy Rider Motorbike Tour Knock-Off",
        "location": "Dalat city center, hotel lobbies",
        "danger_level": "medium",
        "story": "Dalat Easy Riders are legendary motorbike tour guides. But the brand has been copied by dozens of unlicensed operators. Some are fine; others use unsafe bikes, don't know the routes, and pocket deposits for tours they never deliver.",
        "red_flags": ["Rider approaches you on the street claiming to be an Easy Rider", "No verifiable connection to the original group", "Demands full payment upfront in cash"],
        "how_to_avoid": ["Book through the original Dalat Easy Riders website or their office", "Pay a deposit, not full payment, and settle the rest at the end", "Ask to see the bike and check its condition"],
        "reddit_sources": ["r/vietnam: 'So many fake Easy Riders in Dalat now \u2014 verify through the original office'", "r/travel: 'The real Dalat Easy Riders have years of reviews \u2014 don't book random guys on the street'"]
      }
    ]
  },
  {
    "city": "Chiang Rai",
    "country": "Thailand",
    "country_code": "th",
    "flag": "\U0001f1f9\U0001f1ed",
    "scams": [
      {
        "scam_name": "The White Temple Photo Fee Scam",
        "location": "Outside Wat Rong Khun (White Temple)",
        "danger_level": "low",
        "story": "After visiting the White Temple, a vendor offers to take your photo with a professional camera for 'free.' They print it on the spot and demand 200-500 baht. When you decline, they loudly shame you for 'wasting film.'",
        "red_flags": ["Photographer offers free photos at a tourist landmark", "Photo is printed before you agree to pay", "Aggressive reaction when you decline to purchase"],
        "how_to_avoid": ["Politely decline unsolicited photo offers", "Take your own photos \u2014 the temple is photogenic from every angle", "If you want a professional photo, agree on the price before posing"],
        "reddit_sources": ["r/ThailandTourism: 'Vendors at the White Temple print unsolicited photos then demand payment'", "r/travel: 'Take your own photos at Chiang Rai temples'"]
      },
      {
        "scam_name": "The Golden Triangle Border Crossing Scam",
        "location": "Chiang Saen/Golden Triangle area",
        "danger_level": "high",
        "story": "Tour operators at the Golden Triangle offer a quick boat trip to the Laos side for passport stamps and duty-free shopping. Some operators charge inflated border crossing fees and take you to commission shops. The Golden Triangle area has also been linked to scam compounds.",
        "red_flags": ["Tour offers border crossing at prices above the official visa fee", "Includes mandatory shopping stops", "Trip to the Myanmar side specifically"],
        "how_to_avoid": ["Skip the border crossing unless you genuinely need to visit Laos", "The Golden Triangle viewpoint itself is free and worth visiting", "If crossing to Laos, the official visa-on-arrival is $30-50 depending on nationality"],
        "reddit_sources": ["r/thailand: 'The Golden Triangle boat trip to Laos is a commission-driven shopping tour'", "r/travel: 'Golden Triangle area is linked to scam compounds \u2014 stick to the Thai side'"]
      }
    ]
  },
  {
    "city": "Lake Como",
    "country": "Italy",
    "country_code": "it",
    "flag": "\U0001f1ee\U0001f1f9",
    "scams": [
      {
        "scam_name": "The Bellagio Water Taxi Gouge",
        "location": "Bellagio, Varenna, Menaggio docks",
        "danger_level": "medium",
        "story": "A water taxi captain at Bellagio offers to take you across the lake to Villa del Balbianello for \u20ac80. The regular public ferry costs \u20ac5. Some charge per person rather than per boat \u2014 a couple ends up paying \u20ac160 for what should be a \u20ac10 ferry ride.",
        "red_flags": ["Price quoted without clarifying per person or per boat", "Captain approaches you at the dock", "Claims the public ferry isn't running today"],
        "how_to_avoid": ["Use the public ferries operated by Navigazione Laghi", "A single ferry ticket between towns is \u20ac3-7", "Buy a one-day ferry pass for \u20ac15 and hop between all lake towns", "If using a water taxi, agree on total price before boarding"],
        "reddit_sources": ["r/italy: 'Lake Como water taxis charge 10-20x the public ferry \u2014 use Navigazione Laghi'", "r/travel: 'The public ferry system on Lake Como is cheap and beautiful \u2014 skip water taxis'"]
      },
      {
        "scam_name": "The Villa Garden Entry Confusion",
        "location": "Villas around the lake",
        "danger_level": "low",
        "story": "You visit Villa Carlotta and pay the \u20ac12 entrance. Then you learn the separate garden section is another \u20ac8. Then the art gallery inside is a third ticket. Individual fees are legitimate but rarely presented clearly upfront.",
        "red_flags": ["Multiple separate tickets for what seems like one attraction", "Prices not clearly listed at the main entrance"],
        "how_to_avoid": ["Check villa websites before visiting for full pricing", "Villa del Balbianello: \u20ac10 gardens only, \u20ac20 gardens + villa, plus \u20ac7 boat from Lenno", "Villa Carlotta: \u20ac12 includes everything", "Budget \u20ac15-25 per villa visit"],
        "reddit_sources": ["r/italy: 'Lake Como villa prices add up fast \u2014 check websites before visiting'", "r/travel: 'Budget \u20ac20-30 per villa on Lake Como including boats and entry'"]
      }
    ]
  },
  {
    "city": "Bologna",
    "country": "Italy",
    "country_code": "it",
    "flag": "\U0001f1ee\U0001f1f9",
    "scams": [
      {
        "scam_name": "The Friendship Bracelet Pickpocket",
        "location": "Piazza Maggiore, Via dell'Indipendenza, near Due Torri",
        "danger_level": "medium",
        "story": "A man approaches you near the Two Towers and ties a friendship bracelet on your wrist while chatting enthusiastically. While you're distracted, an accomplice lifts your wallet or phone. The bracelet is a distraction technique used by professional pickpocket teams operating across northern Italian cities.",
        "red_flags": ["Someone approaches to tie something on your wrist", "Overly friendly physical contact from a stranger", "A second person hovers nearby", "Happens near major landmarks and bottleneck walkways"],
        "how_to_avoid": ["Keep your hands at your sides \u2014 don't let anyone tie anything on you", "Step back and say 'No grazie' firmly", "Keep valuables in front pockets or a money belt", "This scam operates in Rome, Florence, Bologna, Milan, and Venice"],
        "reddit_sources": ["r/italy: 'Bracelet scam teams in Bologna work the same as Rome \u2014 it's a pickpocket distraction'", "r/travel: 'Never let a stranger touch your wrists in Italian tourist areas \u2014 it's a setup'"]
      }
    ]
  },
  {
    "city": "Essaouira",
    "country": "Morocco",
    "country_code": "ma",
    "flag": "\U0001f1f2\U0001f1e6",
    "scams": [
      {
        "scam_name": "The Fake Argan Oil Cooperative",
        "location": "Road between Marrakech and Essaouira, medina shops",
        "danger_level": "medium",
        "story": "Tour buses stop at roadside 'argan oil cooperatives' where women demonstrate traditional oil pressing. The demonstration is real, but the oil for sale is often diluted with cheaper vegetable oils. A 100ml bottle sells for $30-50 when genuine argan oil costs $15-20 retail.",
        "red_flags": ["Tour bus stops specifically at this cooperative", "Oil is heavily discounted from an already inflated price", "No Ecocert or USDA Organic certification visible", "Driver receives a visible commission"],
        "how_to_avoid": ["Buy argan oil from verified pharmacies or certified cooperatives", "Look for Ecocert, USDA Organic, or IGP Argane certification on the label", "Fair price for 100ml genuine argan oil: $15-25", "The best cooperatives don't need tour bus traffic"],
        "reddit_sources": ["r/morocco: 'Roadside argan cooperatives sell diluted oil \u2014 buy from pharmacies'", "r/travel: 'Check for Ecocert certification on argan oil in Morocco \u2014 most tourist shop oil is fake'"]
      }
    ]
  },
  {
    "city": "Nusa Penida",
    "country": "Indonesia",
    "country_code": "id",
    "flag": "\U0001f1ee\U0001f1e9",
    "scams": [
      {
        "scam_name": "The Day Trip Tour Overcrowding",
        "location": "Tour operators in Bali, fast boats from Sanur",
        "danger_level": "medium",
        "story": "A Bali-based agency sells a Nusa Penida day trip for 350,000 IDR ($22) including boat, transport, lunch, and 4 photo spots. You arrive and there's 15 people crammed into a van built for 8, driving on Nusa Penida's famously dangerous cliff roads. Each stop allows exactly 10 minutes for photos.",
        "red_flags": ["Price under 500,000 IDR for a full day trip from Bali", "No mention of group size or vehicle type", "Itinerary promises 4+ spots in one day"],
        "how_to_avoid": ["Book a private driver on Nusa Penida for 600,000-800,000 IDR for 2-3 spots max", "Stay overnight on the island rather than doing a rushed day trip", "3 photo spots per day is realistic \u2014 4+ means a rushed, dangerous drive"],
        "reddit_sources": ["r/bali: 'Nusa Penida day trips are dangerously overcrowded \u2014 stay overnight or hire a private driver'", "r/travel: 'The roads on Nusa Penida are cliff edges \u2014 don't let a rushed tour driver speed on them'"]
      },
      {
        "scam_name": "The Fast Boat No-Insurance Gamble",
        "location": "Sanur Harbor fast boat departures",
        "danger_level": "high",
        "story": "Fast boats from Sanur to Nusa Penida cost 150,000-200,000 IDR and take 30-45 minutes. Budget boats charging 100,000 IDR cut costs on maintenance and insurance. In rough seas, these boats have capsized.",
        "red_flags": ["Ticket price under 150,000 IDR", "Boat looks old or poorly maintained", "No visible life jackets or safety equipment"],
        "how_to_avoid": ["Use established operators: Maruti Express, Angel Billabong, or Crown Fast Cruise", "Budget 200,000-300,000 IDR per crossing for a safe boat", "Sit near exits and locate life jackets before departure"],
        "reddit_sources": ["r/bali: 'Cheap fast boats to Nusa Penida are a safety risk \u2014 use established operators'", "r/travel: 'Pay more for the Nusa Penida boat \u2014 the budget ones have capsized'"]
      }
    ]
  },
  {
    "city": "Pai",
    "country": "Thailand",
    "country_code": "th",
    "flag": "\U0001f1f9\U0001f1ed",
    "scams": [
      {
        "scam_name": "The Scooter Rental Passport Hostage",
        "location": "Rental shops on Walking Street",
        "danger_level": "high",
        "story": "You rent a scooter for 200 baht/day. The road from Chiang Mai to Pai has 762 curves \u2014 you're going to get scratches. When you return the bike, the shop claims damage and wants 5,000-15,000 baht. Having left your passport as deposit, you have no leverage.",
        "red_flags": ["Shop requires your passport, not cash deposit", "No pre-ride condition documentation", "The infamous 762-curve road virtually guarantees drops for beginners"],
        "how_to_avoid": ["Leave cash deposit (3,000-5,000 baht), never your passport", "Video the entire bike before and after with the shop owner visible", "Get travel insurance that covers motorbike accidents", "Honestly assess your riding ability \u2014 the Pai road is serious"],
        "reddit_sources": ["r/ThailandTourism: 'Pai scooter rental shops prey on inexperienced riders after the 762 curves'", "r/travel: 'Never leave your passport at a scooter rental in Pai'"]
      }
    ]
  },
  {
    "city": "Bariloche",
    "country": "Argentina",
    "country_code": "ar",
    "flag": "\U0001f1e6\U0001f1f7",
    "scams": [
      {
        "scam_name": "The Rental Car Break-In",
        "location": "Trailheads, scenic viewpoints, parking areas",
        "danger_level": "high",
        "story": "Bariloche is Patagonia's gateway \u2014 tourists rent cars to drive the Route of the Seven Lakes. At scenic overlooks and trailheads, thieves break into rental cars targeting tourists who leave bags visible. The UK government specifically warns about vehicle break-ins in Bariloche.",
        "red_flags": ["Any belongings visible through car windows", "Isolated parking at trailheads", "Nearby individuals loitering without obvious purpose"],
        "how_to_avoid": ["Lock everything in the trunk BEFORE arriving at the destination", "Take all valuables with you on hikes", "Use parking lots with attendants when available"],
        "reddit_sources": ["r/argentina: 'Bariloche rental car break-ins are so common the UK government issues a warning'", "r/travel: 'Lock everything in the trunk BEFORE arriving at trailheads in Patagonia'"]
      },
      {
        "scam_name": "The Chocolate Shop Tourist Tax",
        "location": "Avenida Mitre (Chocolate Street)",
        "danger_level": "low",
        "story": "Bariloche calls itself the chocolate capital of Argentina. Dozens of shops on Chocolate Street offer free samples. The chocolate is genuinely good, but prices are 2-3x what you'd pay at a supermarket or in Buenos Aires.",
        "red_flags": ["Free sampling creating purchase obligation", "Prices not listed or hard to compare", "Located directly where tour buses stop"],
        "how_to_avoid": ["Enjoy the free samples guilt-free", "Buy at less touristy shops on side streets for 30-50% less", "The supermarket La Anonima sells the same brands significantly cheaper"],
        "reddit_sources": ["r/argentina: 'Bariloche chocolate street is fun but buy at side-street shops for real prices'", "r/travel: 'Sample everything on Chocolate Street but buy at La Anonima for half the price'"]
      }
    ]
  },
  {
    "city": "Siargao",
    "country": "Philippines",
    "country_code": "ph",
    "flag": "\U0001f1f5\U0001f1ed",
    "scams": [
      {
        "scam_name": "The Island Hopping Boat Safety Risk",
        "location": "General Luna port, tourist beach areas",
        "danger_level": "high",
        "story": "Budget island hopping tours offer boats for \u20b1500-800 per person. Some operators use overloaded bangka boats without life jackets. The seas around Siargao can turn rough quickly, and multiple incidents of boats capsizing have been reported.",
        "red_flags": ["Boat has no visible life jackets", "More than 10-12 people on a standard bangka", "Operator insists on going out despite rough seas"],
        "how_to_avoid": ["Count life jackets before boarding", "Book through your resort or established operators", "Maximum 10-12 people per standard bangka", "If seas look rough, postpone"],
        "reddit_sources": ["r/Philippines: 'Siargao island hopping boats are sometimes dangerously overloaded'", "r/travel: 'Book Siargao boat trips through your resort \u2014 random beach operators cut safety corners'"]
      },
      {
        "scam_name": "The Surf Lesson Price Gouge",
        "location": "Cloud 9 Beach, General Luna",
        "danger_level": "low",
        "story": "Surf instructors at Cloud 9 quote \u20b1500-800 per hour for a lesson. After the lesson, they add charges: board rental (\u20b1300 extra), rash guard (\u20b1200), and photos (\u20b1500). Your \u20b1500 lesson becomes \u20b11,500.",
        "red_flags": ["Very low initial price", "Extras mentioned only after the lesson starts"],
        "how_to_avoid": ["Ask for an all-inclusive price before starting", "Fair all-in price: \u20b1800-1,200 per hour including equipment", "Book through established surf schools (Kermit, Harana, Cloud 9 Surf School)"],
        "reddit_sources": ["r/Philippines: 'Siargao surf lessons quote low then add extras \u2014 get the full price upfront'", "r/travel: 'Book surf lessons at established Siargao schools'"]
      }
    ]
  }
]

data.extend(additional)

with open("/Users/bjh/Documents/tabiji/scams/research/batch_new_50.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

cities = [d["city"] for d in data]
total_scams = sum(len(d["scams"]) for d in data)
print(f"Total destinations: {len(cities)}")
print(f"Total scams: {total_scams}")
print(f"Average scams per city: {total_scams/len(cities):.1f}")
for i, d in enumerate(data, 1):
    print(f"  {i:2d}. {d['city']:20s} ({d['country']:15s}) \u2014 {len(d['scams'])} scams")
