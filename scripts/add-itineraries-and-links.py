#!/usr/bin/env python3
"""
Add sample itineraries and internal links to 10 high-opportunity compare pages.
Injects HTML before the faq-section. Does not modify existing content.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO / "compare"

# ─── Page data: itineraries + internal links ─────────────────────────

PAGES = {

"bali-vs-phuket": {
    "dest1": "Bali", "dest2": "Phuket",
    "itineraries": [
        {"tab": "3 Days in Bali", "title": "Weekend in Bali (3 Days)", "days": [
            ("Day 1", 'Arrive in Ubud. Visit the <a href="/popular-picks/bali-cooking-classes/">Balinese cooking class</a> in the morning, explore the Tegallalang Rice Terraces in the afternoon, and end with a sunset dinner overlooking the valley.'),
            ("Day 2", 'Morning yoga session, then visit the Sacred Monkey Forest. Afternoon: drive to Seminyak for beach clubs and the famous sunset at Tanah Lot temple.'),
            ("Day 3", 'Snorkeling at Nusa Penida (day trip by fast boat), see Kelingking Beach and Crystal Bay. Return for a final <a href="/popular-picks/bali-fine-dining/">fine dining</a> dinner in Seminyak.'),
        ], "tip": "Book Nusa Penida boats 2-3 days ahead in peak season."},
        {"tab": "3 Days in Phuket", "title": "Weekend in Phuket (3 Days)", "days": [
            ("Day 1", 'Arrive and settle in Kata or Karon Beach area. Afternoon at the beach, evening at the Phuket Old Town night market for street food.'),
            ("Day 2", 'Full-day Phi Phi Islands boat tour — snorkeling at Maya Bay, lunch on the boat, swimming at Bamboo Island. Evening: Bangla Road nightlife.'),
            ("Day 3", 'Morning visit to Big Buddha viewpoint, then Rawai seafood market for lunch. Afternoon: Cape Promthep sunset, one of the best in Thailand.'),
        ], "tip": "Phi Phi day trips run ~$40-60 USD including lunch. Book through your hotel for best rates."},
        {"tab": "7 Days in Bali", "title": "Week in Bali (7 Days)", "days": [
            ("Days 1-2", 'Ubud: rice terraces, Monkey Forest, <a href="/popular-picks/bali-coworking-cafes/">artisan cafes</a>, Tirta Empul water temple, and a traditional Balinese massage.'),
            ("Days 3-4", 'Nusa Islands: ferry to Nusa Penida for Kelingking Beach and snorkeling. Overnight on Nusa Lembongan for a quieter island pace.'),
            ("Days 5-6", 'Seminyak/Canggu: beach clubs, surfing lessons at Batu Bolong, sunset drinks at La Brisa, <a href="/popular-picks/bali-brunch-cafes/">brunch cafes</a> in Canggu.'),
            ("Day 7", 'Mt. Batur sunrise trek (leave at 2am, worth it) or slow morning at a <a href="/popular-picks/bali-cheap-eats/">local warung</a>, then departure.'),
        ], "tip": "Rent a scooter ($5/day) — it's the best way to get around Bali. International license required."},
        {"tab": "7 Days in Phuket", "title": "Week in Phuket (7 Days)", "days": [
            ("Days 1-2", 'Old Town Phuket: Sino-Portuguese architecture, street art, Thalang Road market. Beaches: Kata, Karon, Freedom Beach.'),
            ("Days 3-4", 'Phi Phi and Khai Islands day trip. Next day: James Bond Island and Phang Nga Bay kayaking — limestone karsts rising from emerald water.'),
            ("Days 5-6", 'Day trip to <a href="/compare/phuket-vs-krabi/">Krabi</a> (2hr drive) for Railay Beach and Tiger Cave Temple. Or stay local: Phuket Elephant Sanctuary + Cape Panwa sunset.'),
            ("Day 7", 'Rawai/Nai Harn Beach (local favorite, less crowded). Seafood lunch at Rawai market ($8-12 for a feast), afternoon spa, departure.'),
        ], "tip": "Phuket is big — hire a driver for day trips (~$40/day) rather than dealing with tuk-tuk negotiations."},
    ],
    "links": {
        "More Bali Comparisons": [
            ("/compare/bali-vs-thailand/", "Bali vs Thailand"),
            ("/compare/bali-vs-fiji/", "Bali vs Fiji"),
            ("/compare/bali-vs-vietnam/", "Bali vs Vietnam"),
        ],
        "More Phuket Comparisons": [
            ("/compare/phuket-vs-krabi/", "Phuket vs Krabi"),
            ("/compare/phuket-vs-koh-samui/", "Phuket vs Koh Samui"),
            ("/compare/philippines-vs-thailand/", "Philippines vs Thailand"),
        ],
        "Bali Food & Activities": [
            ("/popular-picks/bali-cheap-eats/", "Bali Cheap Eats"),
            ("/popular-picks/bali-cooking-classes/", "Bali Cooking Classes"),
            ("/popular-picks/bali-fine-dining/", "Bali Fine Dining"),
        ],
    }
},

"lisbon-vs-porto": {
    "dest1": "Lisbon", "dest2": "Porto",
    "itineraries": [
        {"tab": "3 Days in Lisbon", "title": "Weekend in Lisbon (3 Days)", "days": [
            ("Day 1", 'Alfama: Sao Jorge Castle, Fado music in the evening, <a href="/popular-picks/lisbon-pastel-de-nata/">pastel de nata</a> at Manteigaria. Take Tram 28 through the historic hills.'),
            ("Day 2", 'Belem: Tower of Belem, Jeronimos Monastery, Pasteis de Belem (the original). Afternoon: LX Factory for food and shopping. Sunset from <a href="/popular-picks/lisbon-rooftop-bars/">a rooftop bar</a> in Bairro Alto.'),
            ("Day 3", '<a href="/popular-picks/lisbon-day-trips/">Day trip to Sintra</a> (40 min train): Pena Palace, Quinta da Regaleira, and the Moorish Castle. Return for farewell dinner in Chiado.'),
        ], "tip": "Get the Lisboa Card (€27/72hr) — covers unlimited metro, trams, and free entry to 30+ museums including Belem."},
        {"tab": "3 Days in Porto", "title": "Weekend in Porto (3 Days)", "days": [
            ("Day 1", 'Ribeira: walk the Douro riverfront, cross Dom Luis I bridge to Vila Nova de Gaia for a Port wine tasting (€5-15). Sunset from Serra do Pilar viewpoint.'),
            ("Day 2", 'Sao Bento Station (azulejo tiles), Livraria Lello bookshop, Clerigos Tower. Lunch: francesinha sandwich (Porto specialty). Afternoon: Foz do Douro beach neighborhood.'),
            ("Day 3", 'Day trip to Douro Valley (1.5hr drive): wine tastings at quintas, boat cruise on the river, vineyard lunch. One of Europe\'s most beautiful wine regions.'),
        ], "tip": "Book Livraria Lello tickets online (€5, redeemable against book purchases) — the queue without tickets can be 1-2 hours."},
        {"tab": "7 Days in Lisbon", "title": "Week in Lisbon (7 Days)", "days": [
            ("Days 1-2", 'Central Lisbon: Alfama, Bairro Alto, Chiado. Tram 28, Sao Jorge Castle, <a href="/popular-picks/lisbon-brunch/">brunch spots</a>, and fado in the evening.'),
            ("Days 3-4", 'Belem + Sintra day trip. <a href="/popular-picks/lisbon-natural-wine-bars/">Natural wine bars</a> in Santos. Visit the Gulbenkian Museum and Parque das Nacoes.'),
            ("Days 5-6", 'Day trip to Cascais and Cabo da Roca (westernmost point of Europe). Next day: Setubal for seafood and Arrabida Natural Park beaches.'),
            ("Day 7", '<a href="/popular-picks/lisbon-photography-spots/">Photography walk</a> through Graca and Mouraria (most authentic neighborhoods). Final meal at a tasca in Alfama.'),
        ], "tip": "Lisbon's hills are no joke — wear comfortable shoes and budget for occasional Uber rides (very cheap in Portugal)."},
        {"tab": "7 Days in Porto", "title": "Week in Porto (7 Days)", "days": [
            ("Days 1-2", 'Historic center: Ribeira, cathedral, Clerigos, Bolhao market. Cross to Gaia for Port cellars. Evening: live music in Galeria de Paris bars.'),
            ("Days 3-4", 'Douro Valley overnight: wine tastings, river cruise, stay at a vineyard guesthouse (~€60-80/night). One of Europe\'s most underrated experiences.'),
            ("Days 5-6", 'Beach day at Matosinhos (20min metro) — best seafood restaurants in Porto. Next day: Guimaraes day trip (birthplace of Portugal, UNESCO).'),
            ("Day 7", 'Foz do Douro coastal walk, brunch in Cedofeita, last Port tasting at a boutique cellar. Departure.'),
        ], "tip": "Porto is very walkable but hilly. The Andante transit card covers metro, buses, and trams."},
    ],
    "links": {
        "More Portugal Comparisons": [
            ("/compare/portugal-vs-spain/", "Portugal vs Spain"),
            ("/compare/portugal-vs-croatia/", "Portugal vs Croatia"),
            ("/compare/portugal-vs-morocco/", "Portugal vs Morocco"),
            ("/compare/azores-vs-madeira/", "Azores vs Madeira"),
        ],
        "Lisbon Guides": [
            ("/popular-picks/lisbon-pastel-de-nata/", "Best Pastel de Nata"),
            ("/popular-picks/lisbon-rooftop-bars/", "Rooftop Bars"),
            ("/popular-picks/lisbon-day-trips/", "Day Trips from Lisbon"),
            ("/popular-picks/lisbon-brunch/", "Brunch Spots"),
        ],
    }
},

"tokyo-vs-osaka": {
    "dest1": "Tokyo", "dest2": "Osaka",
    "itineraries": [
        {"tab": "3 Days in Tokyo", "title": "Weekend in Tokyo (3 Days)", "days": [
            ("Day 1", 'Shibuya crossing, Meiji Shrine, Harajuku (Takeshita Street). Afternoon: Shinjuku for shopping. Evening: Golden Gai bar-hopping or <a href="/popular-picks/tokyo-sushi/">omakase sushi</a>.'),
            ("Day 2", 'Tsukiji Outer Market breakfast, Senso-ji temple in Asakusa, teamLab Borderless. Evening: Akihabara or Roppongi nightlife.'),
            ("Day 3", '<a href="/popular-picks/tokyo-day-trips/">Day trip to Kamakura</a> (1hr train): Great Buddha, bamboo groves, beach town vibes. Return for a final ramen dinner in Shinjuku.'),
        ], "tip": "Get a 72-hour Tokyo Metro pass (¥1,500/~$10) — covers all metro lines. JR lines are separate."},
        {"tab": "3 Days in Osaka", "title": "Weekend in Osaka (3 Days)", "days": [
            ("Day 1", 'Dotonbori: the neon heart of Osaka. <a href="/popular-picks/osaka-street-food/">Street food</a> crawl — takoyaki, <a href="/popular-picks/osaka-okonomiyaki/">okonomiyaki</a>, gyoza. Evening: Shinsekai for <a href="/popular-picks/osaka-kushikatsu/">kushikatsu</a>.'),
            ("Day 2", 'Osaka Castle in the morning, Kuromon Market for sashimi breakfast, Namba for shopping. Afternoon: <a href="/popular-picks/osaka-craft-beer/">craft beer</a> in Amerikamura.'),
            ("Day 3", 'Day trip to Nara (45 min): feed the deer, visit Todai-ji (world\'s largest wooden building). Return for a farewell <a href="/popular-picks/osaka-ramen/">ramen</a> in Umeda.'),
        ], "tip": "Osaka is Japan's street food capital — budget ¥2,000-3,000 ($14-20) per day just for snacking."},
        {"tab": "7 Days in Tokyo", "title": "Week in Tokyo (7 Days)", "days": [
            ("Days 1-2", 'Classic Tokyo: Shibuya, Shinjuku, Harajuku, Meiji Shrine. Tsukiji market, teamLab. <a href="/popular-picks/tokyo-sushi/">Sushi</a> at a standing bar.'),
            ("Days 3-4", 'Deep Tokyo: Shimokitazawa (vintage shops), Yanaka (old Tokyo charm), Odaiba (waterfront). Day trip to <a href="/compare/tokyo-vs-kyoto/">Kamakura or Nikko</a>.'),
            ("Days 5-6", 'Day trip to Hakone (Mt. Fuji views, hot springs, <a href="/popular-picks/hakone-ryokan/">ryokan</a> stay). Next day: Akihabara + Ueno Park + National Museum.'),
            ("Day 7", 'Tsukiji for one last breakfast, then Ginza for upscale shopping or Nakameguro canal walk. Departure.'),
        ], "tip": "Get a Suica/Pasmo IC card at any station — tap on/off for all trains, buses, and even convenience stores."},
        {"tab": "7 Days in Osaka", "title": "Week in Osaka (7 Days)", "days": [
            ("Days 1-2", 'Dotonbori + Shinsekai + Kuromon Market food tour. Osaka Castle, Umeda Sky Building sunset. Evening: Hozenji Yokocho alley for izakaya.'),
            ("Days 3-4", 'Day trip to <a href="/compare/hiroshima-vs-nagasaki/">Hiroshima</a> (1.5hr shinkansen): Peace Memorial, Itsukushima Shrine on Miyajima Island. Next day: Nara deer park + Todai-ji.'),
            ("Days 5-6", 'Day trip to <a href="/compare/osaka-vs-kyoto/">Kyoto</a> (15 min train): Fushimi Inari, Kinkaku-ji, Arashiyama bamboo grove. Next day: local Osaka — Tennoji, Spa World, <a href="/popular-picks/osaka-cheap-eats/">cheap eats</a>.'),
            ("Day 7", 'Minoo waterfall hike (30 min from Umeda), then back for a final street food crawl through Dotonbori. Departure.'),
        ], "tip": "Osaka is the perfect base for Kansai — Kyoto, Nara, Kobe, and Himeji are all under 1 hour away."},
    ],
    "links": {
        "More Japan Comparisons": [
            ("/compare/tokyo-vs-kyoto/", "Tokyo vs Kyoto"),
            ("/compare/osaka-vs-kyoto/", "Osaka vs Kyoto"),
            ("/compare/hiroshima-vs-nagasaki/", "Hiroshima vs Nagasaki"),
            ("/compare/japan-vs-south-korea/", "Japan vs South Korea"),
        ],
        "Tokyo Guides": [
            ("/popular-picks/tokyo-sushi/", "Best Sushi in Tokyo"),
            ("/popular-picks/tokyo-day-trips/", "Tokyo Day Trips"),
            ("/popular-picks/hakone-ryokan/", "Hakone Ryokan"),
        ],
        "Osaka Guides": [
            ("/popular-picks/osaka-street-food/", "Osaka Street Food"),
            ("/popular-picks/osaka-ramen/", "Best Ramen in Osaka"),
            ("/popular-picks/osaka-okonomiyaki/", "Okonomiyaki Guide"),
        ],
    }
},

"mykonos-vs-santorini": {
    "dest1": "Mykonos", "dest2": "Santorini",
    "itineraries": [
        {"tab": "3 Days Mykonos", "title": "Weekend in Mykonos (3 Days)", "days": [
            ("Day 1", 'Mykonos Town (Chora): wander the whitewashed lanes, Little Venice sunset, Paraportiani church. Dinner in a backstreet taverna.'),
            ("Day 2", 'Beach day: Paradise or Super Paradise for party vibes, Agios Sostis for quiet. Afternoon boat trip to Delos (UNESCO site, birthplace of Apollo).'),
            ("Day 3", 'Morning at Ornos Beach, then explore Ano Mera village (Panagia Tourliani monastery). Sunset cocktails at 180 Sunset Bar.'),
        ], "tip": "Mykonos buses are cheap (€2) but stop running at midnight. Book taxis in advance for late nights."},
        {"tab": "3 Days Santorini", "title": "Weekend in Santorini (3 Days)", "days": [
            ("Day 1", 'Oia: the iconic blue domes, <a href="/popular-picks/santorini-sunset-viewpoints/">sunset viewpoint</a> at the castle ruins. Book dinner with caldera views in advance.'),
            ("Day 2", 'Fira to Oia hike (10km, 3-4hr) along the caldera rim — the best free activity on the island. Afternoon: Red Beach or Kamari Black Sand Beach.'),
            ("Day 3", 'Wine tasting at Santo Wines or Venetsanos (caldera views while tasting). Boat trip to the volcanic hot springs. Final sunset from Imerovigli.'),
        ], "tip": "Stay in Fira (cheaper) and bus to Oia for sunset — Oia accommodation is 2-3x the price for the same view."},
        {"tab": "7 Days Mykonos", "title": "Week in Mykonos (7 Days)", "days": [
            ("Days 1-2", 'Mykonos Town, Little Venice, Delos day trip. Beach hopping: Platis Gialos, Psarou, Paradise.'),
            ("Days 3-4", 'Rent an ATV and explore: Fokos Beach (remote, no facilities), Armenistis Lighthouse, Ano Mera village. Cooking class with a local.'),
            ("Days 5-7", 'Ferry to <a href="/compare/naxos-vs-paros/">Naxos</a> (30 min): bigger island, better beaches, half the price. Explore Naxos Town, Plaka Beach, hike to Mt. Zas. Return to Mykonos for a final night out.'),
        ], "tip": "Consider splitting a Mykonos trip with Naxos or Paros — the ferries are fast and cheap."},
        {"tab": "7 Days Santorini", "title": "Week in Santorini (7 Days)", "days": [
            ("Days 1-2", 'Oia + Fira: caldera walks, sunset spots, blue dome churches. Wine tasting. Fira-Oia hike.'),
            ("Days 3-4", 'South coast: Red Beach, Akrotiri archaeological site (Minoan ruins, the \"Greek Pompeii\"), Vlychada moonscape beach.'),
            ("Days 5-7", 'Ferry to <a href="/compare/naxos-vs-paros/">Paros</a> (2hr): Naoussa village, Kolymbithres beach, Antiparos day trip. Return for final Santorini sunset.'),
        ], "tip": "Santorini in July-Aug is extremely crowded and expensive. May, June, or September are ideal."},
    ],
    "links": {
        "More Greek Island Comparisons": [
            ("/compare/naxos-vs-paros/", "Naxos vs Paros"),
            ("/compare/greece-vs-turkey/", "Greece vs Turkey"),
            ("/compare/greece-vs-italy/", "Greece vs Italy"),
            ("/compare/crete-vs-santorini/", "Crete vs Santorini"),
        ],
        "Santorini Guides": [
            ("/popular-picks/santorini-sunset-viewpoints/", "Best Sunset Viewpoints"),
        ],
    }
},

"cabo-vs-cancun": {
    "dest1": "Cabo", "dest2": "Cancun",
    "itineraries": [
        {"tab": "3 Days Cabo", "title": "Weekend in Cabo (3 Days)", "days": [
            ("Day 1", 'Arrive, settle into the Marina area. Water taxi to Lover\'s Beach (Playa del Amor) near El Arco. Sunset dinner on the marina with views of Land\'s End.'),
            ("Day 2", 'Morning: snorkeling at Chileno Bay or Cabo Pulmo (world-class marine reserve). Afternoon: downtown San Jose del Cabo art walk. Evening: tacos and mezcal on the strip.'),
            ("Day 3", 'Whale watching (Dec-Apr) or ATV desert tour. Afternoon: beach club day at Medano Beach. Farewell dinner at Flora Farms (farm-to-table).'),
        ], "tip": "Whale season (Dec-Apr) is magical — humpbacks migrate right through the arch. Book a small-boat tour."},
        {"tab": "3 Days Cancun", "title": "Weekend in Cancun (3 Days)", "days": [
            ("Day 1", 'Hotel Zone beach day. Snorkeling at MUSA (underwater sculpture museum). Sunset at Playa Delfines. Evening: tacos in Parque de las Palapas (downtown, locals-only).'),
            ("Day 2", 'Day trip to <a href="/compare/cancun-vs-tulum/">Tulum</a> ruins (2hr drive): cliffside Mayan temple overlooking the Caribbean. Swim in a cenote (Gran Cenote or Cenote Dos Ojos). Return for nightlife in the Hotel Zone.'),
            ("Day 3", 'Isla Mujeres day trip (20 min ferry): golf cart around the island, snorkeling at Garrafon, Playa Norte (one of Mexico\'s best beaches). Return for departure.'),
        ], "tip": "Rent a car for Tulum/cenote day trips — it's half the price of organized tours and gives you flexibility."},
        {"tab": "7 Days Cabo", "title": "Week in Cabo (7 Days)", "days": [
            ("Days 1-2", 'Marina + Medano Beach, El Arco boat tour, snorkeling at Chileno Bay. San Jose del Cabo art district dinner.'),
            ("Days 3-4", 'Cabo Pulmo National Park (UNESCO marine reserve, 2hr drive): snorkeling with sea lions and bull sharks. Next day: Todos Santos artist town + surf lesson at Cerritos Beach.'),
            ("Days 5-6", 'Desert ATV tour or camel safari. Whale watching (seasonal). Deep-sea fishing trip. Evening: Flora Farms or Acre restaurant.'),
            ("Day 7", 'Relaxed beach club day at The Cape or Chileno Bay Resort. Farewell sunset at The Ledge rooftop bar.'),
        ], "tip": "Cabo Pulmo is a 2-hour drive but worth it — it's one of the most pristine marine reserves in the Americas."},
        {"tab": "7 Days Cancun", "title": "Week in Cancun (7 Days)", "days": [
            ("Days 1-2", 'Hotel Zone beaches, MUSA snorkeling, downtown Cancun for authentic food. Nightlife: Coco Bongo.'),
            ("Days 3-4", '<a href="/compare/cancun-vs-tulum/">Tulum</a> day trip (ruins + cenotes). Next day: Chichen Itza (2.5hr, leave early to beat crowds). Both are bucket-list UNESCO sites.'),
            ("Days 5-6", 'Isla Mujeres overnight: Playa Norte, Punta Sur cliffs, whale shark swimming (Jun-Sep). Next day: Puerto Morelos for a chill reef snorkel village.'),
            ("Day 7", 'Isla Contoy bird sanctuary (limited visitors, book ahead) or relaxed beach day. Departure.'),
        ], "tip": "ADO buses run Cancun-Tulum-Playa del Carmen frequently ($5-10) — cheaper and safer than driving."},
    ],
    "links": {
        "More Mexico Comparisons": [
            ("/compare/cancun-vs-tulum/", "Cancun vs Tulum"),
            ("/compare/cancun-vs-punta-cana/", "Cancun vs Punta Cana"),
            ("/compare/cozumel-vs-cancun/", "Cozumel vs Cancun"),
            ("/compare/costa-rica-vs-mexico/", "Costa Rica vs Mexico"),
        ],
    }
},

"vietnam-vs-thailand": {
    "dest1": "Vietnam", "dest2": "Thailand",
    "itineraries": [
        {"tab": "3 Days Vietnam", "title": "Weekend in Vietnam — Hanoi Focus (3 Days)", "days": [
            ("Day 1", 'Hanoi Old Quarter: Hoan Kiem Lake, 36 Streets walking tour, egg coffee at Giang Cafe, <a href="/popular-picks/hanoi-pho/">pho</a> at a street stall. Evening: beer corner on Ta Hien street.'),
            ("Day 2", 'Ha Long Bay overnight cruise: kayaking through limestone karsts, swimming, seafood dinner on board. One of Asia\'s most iconic landscapes.'),
            ("Day 3", 'Return from Ha Long. Afternoon: Temple of Literature, train street (check schedules), bun cha lunch. Departure.'),
        ], "tip": "Ha Long Bay overnight cruises start at $80/person — mid-range ($150-200) gives a much better experience."},
        {"tab": "3 Days Thailand", "title": "Weekend in Thailand — Bangkok Focus (3 Days)", "days": [
            ("Day 1", 'Grand Palace + Wat Phra Kaew, Wat Pho (reclining Buddha). Afternoon: Chatuchak Weekend Market or Chinatown. Evening: rooftop bar at Lebua (Hangover movie bar).'),
            ("Day 2", 'Floating markets: Amphawa (weekends) or Damnoen Saduak. Afternoon: Jim Thompson House. Evening: Khao San Road or Soi Cowboy nightlife.'),
            ("Day 3", 'Morning: Lumpini Park tai chi with locals. Ayutthaya day trip (1.5hr): ancient temple ruins, the old Siamese capital. Return for departure.'),
        ], "tip": "The BTS Skytrain and MRT cover central Bangkok — avoid taxis during rush hour (5-7pm gridlock)."},
        {"tab": "7 Days Vietnam", "title": "Week in Vietnam — North to Central (7 Days)", "days": [
            ("Days 1-2", 'Hanoi: Old Quarter, <a href="/popular-picks/hanoi-pho/">pho trail</a>, egg coffee, Temple of Literature. Night train to Sapa (or fly to Ha Long Bay cruise).'),
            ("Days 3-4", 'Ha Long Bay cruise or Sapa trekking (rice terraces, homestay with Hmong families). Return to Hanoi, fly to Da Nang.'),
            ("Days 5-6", 'Hoi An (30 min from Da Nang): ancient town lanterns, custom tailoring ($30-80 for a suit), Banh Mi Phuong, cooking class, An Bang Beach.'),
            ("Day 7", 'Hue imperial citadel day trip from Hoi An (scenic Hai Van Pass drive), or beach day. Departure from Da Nang.'),
        ], "tip": "Internal flights in Vietnam are cheap ($30-60 one-way on VietJet/Bamboo). Don't waste time on 12-hour buses."},
        {"tab": "7 Days Thailand", "title": "Week in Thailand — Bangkok + Islands (7 Days)", "days": [
            ("Days 1-2", 'Bangkok: temples, markets, street food, nightlife. Grand Palace, Chinatown, Chatuchak.'),
            ("Days 3-4", 'Fly to Chiang Mai (1hr): night market, Doi Suthep temple, elephant sanctuary (ethical, no riding). <a href="/compare/bali-vs-thailand/">Thai cooking class</a>.'),
            ("Days 5-7", 'Fly to <a href="/compare/phuket-vs-krabi/">Krabi or Phuket</a>: Railay Beach, island-hopping (4 Islands tour), snorkeling, beach bars. Or <a href="/compare/phuket-vs-koh-samui/">Koh Samui</a> for a resort vibe.'),
        ], "tip": "Thailand's domestic flights are incredibly cheap — Bangkok to Chiang Mai or Phuket for $20-40 on AirAsia/Nok Air."},
    ],
    "links": {
        "More Southeast Asia Comparisons": [
            ("/compare/bali-vs-thailand/", "Bali vs Thailand"),
            ("/compare/thailand-vs-cambodia/", "Thailand vs Cambodia"),
            ("/compare/vietnam-vs-laos/", "Vietnam vs Laos"),
            ("/compare/philippines-vs-thailand/", "Philippines vs Thailand"),
        ],
        "Destination Guides": [
            ("/popular-picks/hanoi-pho/", "Best Pho in Hanoi"),
            ("/compare/phuket-vs-krabi/", "Phuket vs Krabi"),
            ("/compare/phuket-vs-koh-samui/", "Phuket vs Koh Samui"),
            ("/compare/hanoi-vs-ho-chi-minh/", "Hanoi vs Ho Chi Minh"),
        ],
    }
},

"florence-vs-venice": {
    "dest1": "Florence", "dest2": "Venice",
    "itineraries": [
        {"tab": "3 Days Florence", "title": "Weekend in Florence (3 Days)", "days": [
            ("Day 1", 'Duomo climb (463 steps, book ahead), Uffizi Gallery (Botticelli, da Vinci). <a href="/popular-picks/florence-trattorias/">Lunch at a trattoria</a> in San Lorenzo. Evening: Piazzale Michelangelo sunset.'),
            ("Day 2", 'Ponte Vecchio, Pitti Palace, Boboli Gardens. Afternoon: <a href="/popular-picks/florence-leather-workshops/">San Lorenzo leather market</a>. <a href="/popular-picks/florence-aperitivo-bars/">Aperitivo</a> on the Arno.'),
            ("Day 3", 'Accademia (Michelangelo\'s David, book ahead). Day trip option: Tuscan wine country (Chianti, 45 min drive). Return for a final bistecca alla fiorentina dinner.'),
        ], "tip": "Book Uffizi and Accademia tickets weeks in advance — walk-up queues can be 2-3 hours in peak season."},
        {"tab": "3 Days Venice", "title": "Weekend in Venice (3 Days)", "days": [
            ("Day 1", 'St. Mark\'s Square + Basilica, Doge\'s Palace, Bridge of Sighs. Get lost in Dorsoduro — the best neighborhood for <a href="/popular-picks/venice-bacaro-wine-bars/">bacaro wine bars</a> and <a href="/popular-picks/venice-cicchetti/">cicchetti</a>.'),
            ("Day 2", 'Murano (glass-blowing) and Burano (colorful houses, lace) by vaporetto. Afternoon: Rialto Market for fresh seafood. <a href="/popular-picks/venice-ghost-tours/">Evening ghost tour</a>.'),
            ("Day 3", 'Early morning walk (Venice before 8am is magical and empty). Gondola ride (€80, split with others). Train to the airport or onward.'),
        ], "tip": "Buy a vaporetto day pass (€25) — individual rides are €9.50 each. The #1 line is the scenic Grand Canal route."},
        {"tab": "7 Days Florence", "title": "Week in Florence (7 Days)", "days": [
            ("Days 1-2", 'Florence highlights: Duomo, Uffizi, Accademia, Ponte Vecchio. Sunset at Piazzale Michelangelo.'),
            ("Days 3-4", 'Tuscan day trips: Siena (medieval Piazza del Campo), San Gimignano (towers), Chianti wine tasting. Next day: Pisa (optional, 1hr train).'),
            ("Days 5-6", '<a href="/compare/bologna-vs-florence/">Day trip to Bologna</a> (35 min high-speed train): eat tortellini, climb Asinelli Tower. Next day: Oltrarno artisan workshops, cooking class.'),
            ("Day 7", 'Fiesole hilltop village (20 min bus): Roman amphitheater, panoramic Florence views. Final aperitivo and dinner.'),
        ], "tip": "Florence is walkable — you don't need transit. But a day trip to Siena or Bologna is essential for a week-long stay."},
        {"tab": "7 Days Venice", "title": "Week in Venice (7 Days)", "days": [
            ("Days 1-2", 'Central Venice: San Marco, Dorsoduro, Cannaregio. Bacari crawl, Rialto Market, gondola ride.'),
            ("Days 3-4", 'Islands: Murano, Burano, Torcello (oldest settlement in the lagoon). Next day: Lido beach (20 min vaporetto).'),
            ("Days 5-6", 'Day trip to Verona (1hr train): Romeo & Juliet balcony, Roman Arena, excellent aperitivo scene. Next day: Padua (30 min): Scrovegni Chapel (Giotto frescoes), university.'),
            ("Day 7", 'Jewish Ghetto neighborhood, Libreria Acqua Alta (famous bookshop), final cicchetti crawl. Departure.'),
        ], "tip": "Venice is best explored by getting intentionally lost — put Google Maps away for a few hours and wander."},
    ],
    "links": {
        "More Italy Comparisons": [
            ("/compare/amalfi-coast-vs-cinque-terre/", "Amalfi Coast vs Cinque Terre"),
            ("/compare/bologna-vs-florence/", "Bologna vs Florence"),
            ("/compare/milan-vs-venice/", "Milan vs Venice"),
            ("/compare/northern-italy-vs-southern-italy/", "Northern vs Southern Italy"),
        ],
        "Florence & Venice Guides": [
            ("/popular-picks/florence-trattorias/", "Florence Trattorias"),
            ("/popular-picks/florence-aperitivo-bars/", "Florence Aperitivo"),
            ("/popular-picks/venice-cicchetti/", "Venice Cicchetti"),
            ("/popular-picks/venice-bacaro-wine-bars/", "Venice Bacaro Bars"),
        ],
    }
},

"prague-vs-budapest": {
    "dest1": "Prague", "dest2": "Budapest",
    "itineraries": [
        {"tab": "3 Days Prague", "title": "Weekend in Prague (3 Days)", "days": [
            ("Day 1", 'Old Town Square, Astronomical Clock, Charles Bridge (go at sunrise for no crowds). Climb the Old Town Hall tower. Evening: <a href="/popular-picks/prague-craft-beer/">craft beer</a> bar crawl.'),
            ("Day 2", 'Prague Castle complex (largest ancient castle in the world), St. Vitus Cathedral, Golden Lane. Walk down through Mala Strana. Lunch: <a href="/popular-picks/prague-svickova/">svickova</a> at a local hospoda.'),
            ("Day 3", 'Vysehrad fortress (quieter, great views), Zizkov neighborhood (the real Prague — TV Tower with crawling babies, dive bars). <a href="/popular-picks/prague-cheap-eats/">Cheap eats</a> crawl.'),
        ], "tip": "Prague is one of Europe's best beer cities — a half-liter of excellent Czech pilsner costs $1.50-2 at local pubs."},
        {"tab": "3 Days Budapest", "title": "Weekend in Budapest (3 Days)", "days": [
            ("Day 1", 'Buda Castle + Fisherman\'s Bastion (sunrise is magical). Cross the Chain Bridge to Pest side. Afternoon: <a href="/popular-picks/budapest-thermal-baths/">Szechenyi Thermal Baths</a>. Evening: <a href="/popular-picks/budapest-ruin-bars/">ruin bars</a> in the Jewish Quarter.'),
            ("Day 2", 'Parliament Building (book tour), walk along the Danube (Shoes on the Danube memorial). Great Market Hall for <a href="/popular-picks/budapest-langos/">langos</a> and paprika. Evening: Gellert Hill sunset.'),
            ("Day 3", 'Margaret Island morning jog/walk, then Hospital in the Rock (WWII bunker museum). Afternoon: Gellert Baths (Art Nouveau). Farewell dinner on a Danube river cruise.'),
        ], "tip": "Budapest thermal baths are a must — Szechenyi for the experience, Gellert for the architecture, Rudas for the rooftop pool."},
        {"tab": "7 Days Prague", "title": "Week in Prague (7 Days)", "days": [
            ("Days 1-2", 'Old Town, Charles Bridge, Prague Castle. Beer gardens and historic pubs.'),
            ("Days 3-4", 'Day trip to Kutna Hora (1hr train): Bone Church (Sedlec Ossuary), medieval silver mines. Next day: Cesky Krumlov (2.5hr bus, fairy-tale medieval town).'),
            ("Days 5-6", 'Local Prague: Vinohrady (wine bars, parks), Letna Park beer garden (best Prague panorama), DOX contemporary art. <a href="/compare/berlin-vs-prague/">Consider a Berlin side trip</a>.'),
            ("Day 7", 'Petrin Hill (mini Eiffel Tower, rose garden), Strahov Monastery library, final pilsner at a neighborhood hospoda.'),
        ], "tip": "Cesky Krumlov is worth an overnight stay — the town empties after day-trippers leave at 5pm and it's magical."},
        {"tab": "7 Days Budapest", "title": "Week in Budapest (7 Days)", "days": [
            ("Days 1-2", 'Buda Castle, Fisherman\'s Bastion, Parliament, thermal baths, ruin bars. Chain Bridge walk.'),
            ("Days 3-4", 'Day trip to Eger (2hr train): castle, thermal baths, Valley of the Beautiful Women (wine cellars). Next day: Szentendre artist village (40 min HEV train).'),
            ("Days 5-6", 'Deep Budapest: Memento Park (communist statues), Pinball Museum, Cave Church (inside Gellert Hill). Evening: classical concert at Liszt Academy or opera (~$10 tickets).'),
            ("Day 7", 'Danube Bend: Visegrad castle, Esztergom basilica (day trip). Return for farewell dinner at a Buda restaurant with river views.'),
        ], "tip": "Budapest is absurdly cheap for a European capital — a full day (food, baths, transport, drinks) can cost under $40."},
    ],
    "links": {
        "More Central Europe Comparisons": [
            ("/compare/berlin-vs-prague/", "Berlin vs Prague"),
            ("/compare/budapest-vs-krakow/", "Budapest vs Krakow"),
            ("/compare/budapest-vs-belgrade/", "Budapest vs Belgrade"),
        ],
        "Prague & Budapest Guides": [
            ("/popular-picks/prague-craft-beer/", "Prague Craft Beer"),
            ("/popular-picks/prague-cheap-eats/", "Prague Cheap Eats"),
            ("/popular-picks/budapest-ruin-bars/", "Budapest Ruin Bars"),
            ("/popular-picks/budapest-thermal-baths/", "Budapest Thermal Baths"),
        ],
    }
},

"amalfi-coast-vs-cinque-terre": {
    "dest1": "Amalfi Coast", "dest2": "Cinque Terre",
    "itineraries": [
        {"tab": "3 Days Amalfi", "title": "Weekend on the Amalfi Coast (3 Days)", "days": [
            ("Day 1", 'Positano: cascade of colorful houses, Spiaggia Grande beach, boutique shopping on the steep lanes. Sunset dinner with sea views.'),
            ("Day 2", 'SITA bus to Amalfi town: cathedral, Paper Museum. Afternoon ferry to Ravello: Villa Rufolo gardens (Wagner\'s inspiration), Belvedere of Infinity viewpoint.'),
            ("Day 3", 'Path of the Gods hike (Sentiero degli Dei): 7.8km cliffside trail from Bomerano to Nocelle with jaw-dropping coast views. Finish in Positano.'),
        ], "tip": "The Path of the Gods is the best free activity on the coast — start early (8am) to beat the heat and crowds."},
        {"tab": "3 Days Cinque Terre", "title": "Weekend in Cinque Terre (3 Days)", "days": [
            ("Day 1", 'Arrive in Riomaggiore or Manarola. Walk the cliffside paths. Sunset in Manarola (the most photographed view). Seafood dinner with local Cinque Terre white wine.'),
            ("Day 2", 'Hike the Blue Trail (Sentiero Azzurro): Monterosso to Vernazza (2hr, the best section). Afternoon: swim at Monterosso beach (the only sandy beach in the 5 villages).'),
            ("Day 3", 'Train hop: Vernazza morning coffee, Corniglia (quiet hilltop village), Riomaggiore for focaccia and anchovies. Ferry back along the coast for the best views.'),
        ], "tip": "Buy the Cinque Terre Card (€16/day) — covers all trains between villages and trail access. The ferry is separate (€35 day pass)."},
        {"tab": "7 Days Amalfi", "title": "Week on the Amalfi Coast (7 Days)", "days": [
            ("Days 1-2", 'Positano: beach, shopping, hiking. Path of the Gods.'),
            ("Days 3-4", 'Amalfi + Ravello. Day trip to Capri (1hr ferry): Blue Grotto, Anacapri chairlift, shopping on Via Camerelle.'),
            ("Days 5-6", 'Day trip to Pompeii + Herculaneum from Sorrento (1hr train). Next day: kayaking along the coast, hidden beaches.'),
            ("Day 7", 'Sorrento: lemon groves, limoncello tasting, Marina Grande fisherman\'s beach. Departure via Naples (1hr).'),
        ], "tip": "Base in Sorrento for the best transport connections — ferries to Capri, Amalfi, and trains to Pompeii all depart from here."},
        {"tab": "7 Days Cinque Terre", "title": "Week in Cinque Terre + Liguria (7 Days)", "days": [
            ("Days 1-3", 'All 5 villages: hike the Blue Trail, swim at Monterosso, sunset at Manarola, focaccia in Vernazza, pesto in Corniglia.'),
            ("Days 4-5", 'Day trip to Portovenere (20 min boat): Byron\'s Grotto, island of Palmaria. Next day: Levanto (15 min train) for a bigger beach and surfing.'),
            ("Days 6-7", 'Genoa day trip (1.5hr train): old town, aquarium (Europe\'s largest), focaccia di Recco, pesto capital. Or Portofino (30 min from Santa Margherita).'),
        ], "tip": "Stay in Riomaggiore or Manarola for the best atmosphere. Monterosso is most resort-like. Avoid Cinque Terre entirely in August — it's overwhelmingly crowded."},
    ],
    "links": {
        "More Italy Coast Comparisons": [
            ("/compare/florence-vs-venice/", "Florence vs Venice"),
            ("/compare/northern-italy-vs-southern-italy/", "Northern vs Southern Italy"),
            ("/compare/naples-vs-rome/", "Naples vs Rome"),
            ("/compare/cinque-terre-vs-portofino/", "Cinque Terre vs Portofino"),
        ],
    }
},

"kauai-vs-maui": {
    "dest1": "Kauai", "dest2": "Maui",
    "itineraries": [
        {"tab": "3 Days Kauai", "title": "Weekend in Kauai (3 Days)", "days": [
            ("Day 1", 'North Shore: Hanalei Bay (one of America\'s best beaches), Na Pali Coast viewpoint from Ke\'e Beach. Lunch: poke bowl at Hanalei Bread Company.'),
            ("Day 2", 'Waimea Canyon (\"Grand Canyon of the Pacific\"): multiple viewpoints, short hikes. Drive to Poipu Beach for afternoon snorkeling with sea turtles.'),
            ("Day 3", 'Na Pali Coast boat tour or helicopter tour — the most dramatic coastline in Hawaii. Afternoon: Poipu farmer\'s market, shave ice, departure.'),
        ], "tip": "Na Pali Coast is inaccessible by car — you must see it by boat, helicopter, or the 11-mile Kalalau Trail (permit required)."},
        {"tab": "3 Days Maui", "title": "Weekend in Maui (3 Days)", "days": [
            ("Day 1", 'West Maui: Ka\'anapali Beach, snorkeling at Black Rock. Sunset at Lahaina. Fresh fish tacos for dinner.'),
            ("Day 2", 'Road to Hana: 620 curves, 59 bridges, waterfalls at every turn. Stops: Twin Falls, Wai\'anapanapa Black Sand Beach, Pools of Oheo. Start by 7am.'),
            ("Day 3", 'Haleakala sunrise (10,000ft above sea level, 38°F at the top — bring layers). Book 60 days in advance. Afternoon: Paia town, beach time at Ho\'okipa.'),
        ], "tip": "Haleakala sunrise requires a reservation ($1 on recreation.gov) — they sell out 60 days ahead. Set your alarm."},
        {"tab": "7 Days Kauai", "title": "Week in Kauai (7 Days)", "days": [
            ("Days 1-2", 'North Shore: Hanalei Bay, Tunnels Beach snorkeling, Queen\'s Bath tidal pools. Princeville sunset.'),
            ("Days 3-4", 'Waimea Canyon + Koke\'e State Park hikes. Poipu Beach, Spouting Horn blowhole. Rum tasting at Koloa Rum Company.'),
            ("Days 5-6", 'Na Pali Coast boat tour (morning, calmer seas). Next day: Kalalau Trail first 2 miles to Hanakapi\'ai Beach (strenuous but spectacular).'),
            ("Day 7", 'Kayak the Wailua River to Secret Falls. Afternoon: Lydgate Beach, Kauai Coffee Company plantation tour. Departure.'),
        ], "tip": "Kauai is the wettest Hawaiian island — the North Shore gets more rain. Pack a light rain jacket and embrace the mist."},
        {"tab": "7 Days Maui", "title": "Week in Maui (7 Days)", "days": [
            ("Days 1-2", 'West Maui: Ka\'anapali, Lahaina, snorkeling at Molokini Crater (boat tour). Sunset at the Sheraton cliff dive.'),
            ("Days 3-4", 'Road to Hana (full day). Next day: Haleakala sunrise, then bike downhill (10,000ft to sea level). Afternoon in Paia surf town.'),
            ("Days 5-6", '<a href="/compare/maui-vs-big-island/">Big Island day trip</a> (30 min flight) or whale watching (Dec-Apr). South Maui: Wailea beaches, La Perouse Bay lava fields.'),
            ("Day 7", 'Iao Valley State Park (Iao Needle), Maui Tropical Plantation. Final poke bowl and shave ice. Departure.'),
        ], "tip": "Maui is bigger than you think — base in West Maui for beaches or Paia/Upcountry for the Road to Hana and Haleakala."},
    ],
    "links": {
        "More Hawaii Comparisons": [
            ("/compare/maui-vs-big-island/", "Maui vs Big Island"),
            ("/compare/maui-vs-oahu/", "Maui vs Oahu"),
            ("/compare/bali-vs-hawaii/", "Bali vs Hawaii"),
        ],
    }
},

}

# ─── Injection logic ─────────────────────────────────────────────────

def build_itinerary_html(data: dict) -> str:
    tabs = []
    panels = []
    for i, itin in enumerate(data["itineraries"]):
        active = ' active' if i == 0 else ''
        tabs.append(f'<button class="ux-itin-tab{active}" data-panel="itin-{i}">{itin["tab"]}</button>')
        days_html = ''
        for day_num, day_desc in itin["days"]:
            days_html += f'<div class="ux-itin-day"><span class="day-num">{day_num}</span><span class="day-desc">{day_desc}</span></div>\n'
        tip = f'<p class="ux-itin-tip">💡 {itin["tip"]}</p>' if itin.get("tip") else ''
        panels.append(f'<div class="ux-itin-panel{active}" id="itin-{i}"><div class="ux-itin-card"><h3>{itin["title"]}</h3>{days_html}{tip}</div></div>')

    return f'''<div class="ux-itineraries" id="sample-itineraries">
<h2>📅 Sample Itineraries</h2>
<div class="ux-itin-tabs">
{''.join(tabs)}
</div>
{''.join(panels)}
</div>
<script>
document.querySelectorAll('.ux-itin-tab').forEach(function(tab){{
    tab.addEventListener('click', function(){{
        document.querySelectorAll('.ux-itin-tab').forEach(function(t){{ t.classList.remove('active'); }});
        document.querySelectorAll('.ux-itin-panel').forEach(function(p){{ p.classList.remove('active'); }});
        this.classList.add('active');
        var panel = document.getElementById(this.getAttribute('data-panel'));
        if(panel) panel.classList.add('active');
    }});
}});
</script>'''


def build_links_html(data: dict) -> str:
    groups = []
    for group_title, links in data["links"].items():
        items = ''.join(f'<li><a href="{url}">→ {label}</a></li>' for url, label in links)
        groups.append(f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">{group_title}</h3><ul>{items}</ul>')
    return f'''<div class="ux-related-links">
<h2>🔗 Related Guides & Comparisons</h2>
{''.join(groups)}
</div>'''


def inject_into_page(slug: str, data: dict) -> bool:
    path = COMPARE_DIR / slug / "index.html"
    html = path.read_text("utf-8")

    # Skip if already injected
    if 'ux-itineraries' in html:
        print(f"  SKIP {slug} (already has itineraries)")
        return False

    itin_html = build_itinerary_html(data)
    links_html = build_links_html(data)
    inject_block = f'\n{itin_html}\n{links_html}\n'

    # Inject before faq-section
    if '<section class="faq-section"' in html:
        html = html.replace('<section class="faq-section"', inject_block + '<section class="faq-section"')
    elif 'class="cta-section"' in html:
        html = html.replace('<div class="cta-section"', inject_block + '<div class="cta-section"')
    else:
        print(f"  WARN {slug}: no injection point found")
        return False

    path.write_text(html, "utf-8")
    return True


# ─── Main ────────────────────────────────────────────────────────────
def main():
    for slug, data in PAGES.items():
        ok = inject_into_page(slug, data)
        status = "OK  " if ok else "SKIP"
        print(f"  {status} {slug}")
    print(f"\nDone: {len(PAGES)} pages processed")


if __name__ == "__main__":
    main()
