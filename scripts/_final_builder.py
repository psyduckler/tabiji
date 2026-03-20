#!/usr/bin/env python3
"""
A self-contained script to generate the complete Tokyo itinerary fulfillment JS file.
This avoids shell/heredoc limits by embedding the data directly in Python.
"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(SCRIPT_DIR, "fulfill-order_1773933372257_6e4kmc.js")

itinerary_data = {
    "destination": "Tokyo, Japan",
    "countryEmoji": "\U0001f1ef\U0001f1f5",
    "title": "Solo Tokyo in Sakura Season",
    "subtitle": "4 days of cherry blossoms, ramen counters & neon-lit nights for one",
    "description": "You're arriving in Tokyo at the exact moment the city transforms. Late March is when the first sakura burst open \u2014 Shinjuku Gyoen's 1,000 trees, the lantern-lit canal at Meguro River, the moat at Chidorigafuchi turning pink. This itinerary is built for solo travelers: counter-seat ramen shops, standing sushi bars, sprawling temple grounds to wander alone, and neighborhoods like Shimokitazawa and Yanaka where the pace slows down. Tokyo is one of the world's great solo cities \u2014 everything is designed for a party of one.",
    "duration": "3 nights",
    "dates": "Mar 20 \u2013 Mar 23, 2026",
    "budget": "$$",
    "pace": "Moderate",
    "bestFor": "Solo Travelers",
    "highlights": [
        "Cherry blossoms at Shinjuku Gyoen \u2014 70+ varieties, 1,000 trees",
        "Chidorigafuchi moat boat ride under sakura canopy",
        "Tsukemen at Fuunji \u2014 Tokyo's best dipping ramen",
        "Senso-ji Temple at dawn \u2014 Asakusa without the crowds",
        "Shimokitazawa vintage shops and craft coffee",
        "Meguro River cherry blossoms lit by paper lanterns at night"
    ],
    "essentials": [
        {"title": "\U0001f338 Cherry Blossom Timing", "text": "Late March is early bloom season \u2014 March 20\u201323 falls right at first bloom (typically March 22\u201326). You'll catch the magical transition from buds to first petals. Shinjuku Gyoen has early-blooming varieties that peak before Somei Yoshino. Check real-time sakura forecasts on japan-guide.com."},
        {"title": "\U0001f687 Getting Around", "text": "Get a 72-hour Tokyo Metro pass (\u00a51,500/~$10) or a Suica/Pasmo IC card \u2014 tap-on, works on all trains, buses, and convenience stores. Google Maps transit is flawless in Tokyo. Trains run 5am\u2013midnight. For late nights, taxi or walk \u2014 Tokyo is extremely safe at any hour."},
        {"title": "\U0001f35c Solo Dining Culture", "text": "Tokyo is the world capital of solo dining. Counter seats at ramen shops, conveyor belt sushi (kaitenzushi), standing bars (tachinomi), and ticket-machine restaurants are all designed for one. No awkwardness, no judgment \u2014 eating alone is completely normal. Ichiran even has private booths with curtains."},
        {"title": "\U0001f4b4 Money and Tipping", "text": "Japan is increasingly cashless (IC cards, PayPay), but carry \u00a510,000\u201320,000 cash for small shops, shrines, and market stalls. Tipping is NOT customary \u2014 the price is the price. 7-Eleven, Lawson, and FamilyMart have international ATMs and genuinely excellent food."}
    ],
    "days": [
        {
            "num": 1, "date": "2026-03-20",
            "neighborhoods": "Shinjuku \u00b7 Shinjuku Gyoen \u00b7 Kabukicho",
            "title": "Shinjuku \u2014 Gardens, Neon and Late-Night Ramen",
            "description": "Start in the heart of Tokyo's biggest district. Morning in the serene gardens of Shinjuku Gyoen chasing early cherry blossoms, afternoon exploring the labyrinthine streets around the station, evening diving into Kabukicho's electric nightlife \u2014 all within walking distance.",
            "timeBlocks": [
                {"label": "Morning",
                 "activities": [{"title": "Shinjuku Gyoen National Garden", "description": "Tokyo's finest cherry blossom garden \u2014 58 hectares with 1,000+ trees across 70+ varieties. Arrive at opening to have the grounds nearly to yourself. The Japanese Traditional Garden, with sakura reflecting in the pond, is the most photogenic spot in the city.", "details": ["\U0001f338 \u00a5500 entry, opens 9am, no alcohol", "\U0001f4f8 Best spots: Japanese Garden pond, English Landscape lawn", "\U0001f6b6 Give yourself 2+ hours \u2014 it's vast", "\U0001f392 Bag check at entrance, no large bags or tripods"]}],
                 "meals": [{"type": "\u2615 Breakfast", "name": "Konbini Coffee and Onigiri", "description": "Start the day the Tokyo way \u2014 hot canned coffee and a salmon onigiri from any 7-Eleven. Japanese convenience store food is legitimately excellent. Try the egg sandwich (tamago sando) too.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Any konbini \u00b7 24h"}],
                 "tips": [{"type": "tip", "text": "Shinjuku Gyoen opens at 9am sharp. Be in line by 8:50 \u2014 the first 30 minutes are magical before the crowds. Use the Shinjuku Gate entrance."}]},
                {"label": "Afternoon",
                 "activities": [
                     {"title": "Omoide Yokocho (Memory Lane)", "description": "A narrow strip of tiny yakitori stalls behind Shinjuku Station's west exit, here since the post-war era. Each stall seats 6-8 at smoky counters. Order chicken skewers and a draft beer.", "details": ["\U0001f3ee Perfect for solo counter dining", "\U0001f362 Must-try: negima (chicken/leek), tsukune (meatball), kawa (crispy skin)", "\U0001f4b0 Cash only at most stalls"]},
                     {"title": "Tokyo Metropolitan Government Building Observatory", "description": "Free 45th-floor observation deck with panoramic views \u2014 on clear days you can see Mt. Fuji. No ticket needed, just security and the elevator.", "details": ["\U0001f193 Free entry, open until 11pm (South Tower)", "\U0001f5fb Best Fuji views: clear mornings or just before sunset", "\U0001f4cd 5 min walk from Shinjuku Station west exit"]}
                 ],
                 "meals": [{"type": "\U0001f35c Lunch", "name": "Fuunji", "description": "One of Tokyo's most legendary tsukemen (dipping ramen) shops. Thick, rich fish-and-pork broth with perfectly chewy noodles. Solo counter seats, ticket machine ordering. The queue moves fast.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Yoyogi, 5 min south of Shinjuku Station \u00b7 Counter seats only"}]},
                {"label": "Evening",
                 "activities": [{"title": "Kabukicho and Golden Gai", "description": "Tokyo's most famous nightlife district. Kabukicho is neon-drenched \u2014 Godzilla on the Toho building, pachinko, arcades. Then Golden Gai: six narrow alleys, 200+ tiny bars seating 5-10 each. Many welcome solo travelers.", "details": ["\U0001f37a Golden Gai: \u00a5500-1000 cover plus drinks", "\U0001f4f8 Kabukicho neon best just after dark (6:30-7:30pm)", "\U0001f6ab Some bars are regulars-only \u2014 look for 'Tourists Welcome' signs", "\U0001f3ae Solo karaoke (hitokara) is a big thing here"]}],
                 "meals": [{"type": "\U0001f377 Dinner", "name": "Omoide Yokocho Yakitori", "description": "Return to Memory Lane for dinner \u2014 it transforms at night when lanterns glow and smoke billows. Pick any stall, grab a counter seat, order charcoal-grilled chicken with cold Asahi.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omoide Yokocho, Shinjuku west exit \u00b7 Cash only"}],
                 "tips": [{"type": "tip", "text": "Golden Gai is best around 8-9pm. Bars are tiny \u2014 if one's full, try next door. There are 200+ options."}]}
            ],
            "mapPins": [
                {"lat": 35.6852, "lng": 139.7100, "label": "Shinjuku Gyoen", "num": 1, "cat": "attraction", "desc": "Tokyo's premier cherry blossom garden \u2014 1,000 trees"},
                {"lat": 35.6938, "lng": 139.7005, "label": "Tokyo Metro Govt Building", "num": 2, "cat": "attraction", "desc": "Free 45th-floor observatory with Mt. Fuji views"},
                {"lat": 35.6896, "lng": 139.6983, "label": "Omoide Yokocho", "num": 3, "cat": "food", "desc": "Post-war yakitori alley \u2014 smoky counter seating"},
                {"lat": 35.6862, "lng": 139.6988, "label": "Fuunji", "num": 4, "cat": "food", "desc": "Legendary tsukemen dipping ramen \u2014 solo counter"},
                {"lat": 35.6942, "lng": 139.7035, "label": "Golden Gai", "num": 5, "cat": "nightlife", "desc": "200+ tiny bars in six narrow alleys"},
                {"lat": 35.6948, "lng": 139.7015, "label": "Kabukicho", "num": 6, "cat": "nightlife", "desc": "Tokyo's neon-lit entertainment district"}
            ]
        },
        {
            "num": 2, "date": "2026-03-21",
            "neighborhoods": "Asakusa \u00b7 Ueno \u00b7 Yanaka \u00b7 Akihabara",
            "title": "Old Tokyo \u2014 Temples, Markets and Otaku Culture",
            "description": "A journey through time. Dawn at the 7th-century Senso-ji Temple, morning in nostalgic Yanaka, afternoon cherry blossoms at Ueno Park, and evening in Akihabara's electric wonderland.",
            "timeBlocks": [
                {"label": "Morning",
                 "activities": [
                     {"title": "Senso-ji Temple at Dawn", "description": "Tokyo's oldest temple (founded 645 AD) is packed by 10am, but at 6:30am you'll have the Thunder Gate and incense-filled main hall to yourself. The Nakamise shopping street is shuttered and atmospheric.", "details": ["\u26e9\ufe0f Grounds open 24h, main hall opens 6:00-6:30am", "\U0001f4f8 Thunder Gate (Kaminarimon): iconic photo with zero crowds at dawn", "\U0001f38b Draw an omikuji fortune (\u00a5100) \u2014 if bad, tie it to the rack", "\U0001f3ee Five-story pagoda area has the best morning light"]},
                     {"title": "Yanaka Ginza and Yanaka Cemetery", "description": "Yanaka survived WWII and feels like 1950s Tokyo. A retro shopping street with street food, cat statues, and zero chains. The adjacent cemetery has a stunning cherry blossom tunnel.", "details": ["\U0001f431 Tokyo's 'cat town' \u2014 real cats and cat-themed everything", "\U0001f338 Yanaka Cemetery sakura tunnel is the most peaceful blossom spot", "\U0001f361 Try menchi-katsu (fried croquette) from street stalls", "\U0001f4cd Nippori Station \u2192 3 min walk"]}
                 ],
                 "meals": [{"type": "\u2615 Breakfast", "name": "Pelican Cafe", "description": "Near Asakusa, a legendary bakery making Japan's most famous shokupan (milk bread) since 1942. The cafe serves thick-cut toast, eggs, and coffee. Simple, perfect, solo-friendly.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Taito, near Asakusa \u00b7 Opens 8am"}],
                 "tips": [{"type": "tip", "text": "From Senso-ji, take the Yamanote Line from Uguisudani to Nippori for Yanaka. It's 15 minutes and feels like teleporting to another era."}]},
                {"label": "Afternoon",
                 "activities": [
                     {"title": "Ueno Park Cherry Blossoms", "description": "Japan's most famous hanami park. Over 1,000 cherry trees line the main avenue, becoming a pink tunnel during bloom season. Grab a konbini bento and sit under the trees like a local.", "details": ["\U0001f338 The main cherry avenue is the classic hanami scene", "\U0001f3db\ufe0f Tokyo National Museum: Japan's oldest and largest (\u00a51,000)", "\U0001f9a2 Shinobazu Pond: rent a solo swan boat", "\U0001f371 Konbini bento + Strong Zero under sakura = peak Tokyo"]},
                     {"title": "Ameyoko Market", "description": "Bustling open-air market under the Yamanote Line tracks. Fresh seafood, dried fruits, chocolate strawberries \u2014 Southeast Asian energy in central Tokyo.", "details": ["\U0001f990 Fresh uni, crab legs, grilled scallops on sticks", "\U0001f36b Chocolate strawberries near the Okachimachi end", "\U0001f4b0 Cash preferred at most stalls"]}
                 ],
                 "meals": [{"type": "\U0001f35c Lunch", "name": "Sansada Tempura", "description": "Operating since 1837, this Asakusa institution serves crispy tempura at the counter. The tendon (tempura rice bowl) is about \u00a51,500 and legendary.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Asakusa, near Senso-ji \u00b7 Counter seats"}]},
                {"label": "Evening",
                 "activities": [{"title": "Akihabara Electric Town", "description": "From ancient temples to anime paradise in one subway ride. Multi-story arcades, manga shops, retro game stores. Even non-otaku love the sensory overload. Check out the vintage game floors at Super Potato.", "details": ["\U0001f3ae Super Potato: 5 floors of retro games, playable consoles on top", "\U0001f4e6 Mandarake: massive secondhand manga/collectibles", "\U0001f579\ufe0f Arcades: crane games, rhythm games, purikura", "\U0001f4cd Best experienced after dark when the neon comes alive"]}],
                 "meals": [{"type": "\U0001f377 Dinner", "name": "Kanda Yabu Soba", "description": "One of Tokyo's three great soba restaurants, from 1880. Hand-cut buckwheat noodles served cold on bamboo with dipping sauce. Minimalist, meditative, and perfect for a solo dinner.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Kanda, between Akihabara and Ueno"}],
                 "tips": [{"type": "tip", "text": "For solo conveyor belt sushi, try any Sushiro or Kura Sushi. Order from a tablet, and the sushi arrives on a mini train. No interaction, no judgment. Brilliant."}]}
            ],
            "mapPins": [
                {"lat": 35.7148, "lng": 139.7967, "label": "Senso-ji Temple", "num": 1, "cat": "attraction", "desc": "Tokyo's oldest temple \u2014 stunning at dawn"},
                {"lat": 35.7270, "lng": 139.7673, "label": "Yanaka Ginza", "num": 2, "cat": "attraction", "desc": "Retro shopping street in old-Tokyo neighborhood"},
                {"lat": 35.7286, "lng": 139.7713, "label": "Yanaka Cemetery", "num": 3, "cat": "attraction", "desc": "Beautiful sakura-lined cemetery walk"},
                {"lat": 35.7146, "lng": 139.7732, "label": "Ueno Park", "num": 4, "cat": "attraction", "desc": "Tokyo's most famous cherry blossom hanami spot"},
                {"lat": 35.7103, "lng": 139.7748, "label": "Ameyoko Market", "num": 5, "cat": "food", "desc": "Open-air market \u2014 fresh seafood and street food"},
                {"lat": 35.7022, "lng": 139.7705, "label": "Akihabara", "num": 6, "cat": "attraction", "desc": "Electric Town \u2014 anime, games, otaku culture"},
                {"lat": 35.7104, "lng": 139.7913, "label": "Pelican Cafe", "num": 7, "cat": "food", "desc": "Legendary shokupan bakery since 1942"},
                {"lat": 35.6997, "lng": 139.7667, "label": "Kanda Yabu Soba", "num": 8, "cat": "food", "desc": "Historic soba restaurant since 1880"}
            ]
        },
        {
            "num": 3, "date": "2026-03-22",
            "neighborhoods": "Harajuku \u00b7 Shibuya \u00b7 Shimokitazawa \u00b7 Nakameguro",
            "title": "West Side \u2014 Vintage, Vinyl and River Blossoms",
            "description": "The creative, youthful side of Tokyo. Morning at Meiji Shrine and Harajuku, afternoon exploring Shimokitazawa's vintage shops, evening along the Meguro River watching cherry blossoms glow under paper lanterns.",
            "timeBlocks": [
                {"label": "Morning",
                 "activities": [
                     {"title": "Meiji Shrine (Meiji Jingu)", "description": "Walk through the towering torii gate into 170 acres of old-growth forest right in central Tokyo. The approach feels like leaving the city. Write a wish on an ema wooden plaque and hang it at the shrine.", "details": ["\u26e9\ufe0f Free entry, opens at sunrise (~5:40am in March)", "\U0001f332 Forest planted in 1920 with 100,000 donated trees", "\U0001f4f8 The massive cypress torii gate on the main approach is the shot", "\U0001f38b Ema plaque (\u00a5500) \u2014 write a wish"]},
                     {"title": "Harajuku and Takeshita Street", "description": "Ancient forest to youth fashion capital in five minutes. Takeshita Street: crepe shops, kawaii fashion, sensory overload. Cat Street (one block over) is the cooler, less crowded version with independent boutiques.", "details": ["\U0001f366 Giant cotton candy and crepes \u2014 Harajuku signatures", "\U0001f457 Cat Street for independent Japanese fashion brands", "\u2615 Percent Arabica Coffee on Cat Street \u2014 minimalist espresso perfection"]}
                 ],
                 "meals": [{"type": "\u2615 Breakfast", "name": "Bills Omotesando", "description": "Australian cafe famous for its ricotta hotcakes \u2014 fluffy, pillowy pancakes practically mandatory in Tokyo. Solo counter seats overlooking the kitchen.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omotesando \u00b7 Opens 8:30am"}]},
                {"label": "Afternoon",
                 "activities": [{"title": "Shimokitazawa", "description": "Tokyo's most beloved bohemian neighborhood \u2014 narrow streets packed with vintage clothing shops, record stores, tiny curry restaurants, and live music venues. Perfect for aimless solo wandering.", "details": ["\U0001f455 Vintage shops: Flamingo, Stick Out, New York Joe Exchange", "\U0001f35b Shimokitazawa is curry town \u2014 try Curry Spice Gelateria", "\U0001f3b5 Afternoon live shows at Shelter or Club Que", "\u2615 Bear Pond Espresso \u2014 legendary barista, incredible shots"]}],
                 "meals": [{"type": "\U0001f35c Lunch", "name": "Curry Spice Gelateria", "description": "A Shimokitazawa original \u2014 artisanal curry with rotating spice-infused gelatos for dessert. Counter seats, solo-perfect.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Shimokitazawa"}],
                 "tips": [{"type": "tip", "text": "Shimokitazawa is 3 stops from Shibuya on the Keio-Inokashira line. South side = vintage, north side = food. Just wander."}]},
                {"label": "Evening",
                 "activities": [
                     {"title": "Meguro River Cherry Blossoms at Night", "description": "The 4km stretch of Meguro River is lined with 800+ cherry trees. During bloom season, thousands of pink paper lanterns illuminate the petals, their reflections rippling in the water. Walk the entire length, stopping at pop-up bars.", "details": ["\U0001f3ee Lantern illumination daily through early April, dusk to 9pm", "\U0001f377 Pop-up wine and champagne stands along the riverbank", "\U0001f4cd Start at Nakameguro Station and walk south", "\U0001f4f8 The bridge near Nakameguro Station is the most photographed spot"]},
                     {"title": "Shibuya Crossing", "description": "The world's busiest intersection. Watch from the Starbucks 2F for the aerial view, then cross with the crowd. Find the Hachiko statue at the north exit.", "details": ["\U0001f4f8 Best views: Starbucks 2F or Mag's Park rooftop (free)", "\U0001f415 Hachiko statue \u2014 world's most loyal dog", "\U0001f303 Most impressive after dark with all the screens lit"]}
                 ],
                 "meals": [{"type": "\U0001f377 Dinner", "name": "Afuri Ramen Nakameguro", "description": "Light, refreshing yuzu shio (citrus salt) ramen \u2014 clear golden broth with a yuzu punch, completely different from heavy tonkotsu. Counter-seat-only. Perfect after a sakura walk.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Nakameguro \u00b7 Ticket machine"}]}
            ],
            "mapPins": [
                {"lat": 35.6764, "lng": 139.6993, "label": "Meiji Shrine", "num": 1, "cat": "attraction", "desc": "170 acres of forest \u2014 Japan's most visited shrine"},
                {"lat": 35.6702, "lng": 139.7026, "label": "Harajuku / Takeshita Street", "num": 2, "cat": "attraction", "desc": "Youth fashion capital \u2014 crepes, kawaii, Cat Street"},
                {"lat": 35.6610, "lng": 139.6682, "label": "Shimokitazawa", "num": 3, "cat": "attraction", "desc": "Bohemian neighborhood \u2014 vintage, vinyl, curry"},
                {"lat": 35.6441, "lng": 139.6985, "label": "Meguro River", "num": 4, "cat": "attraction", "desc": "800+ cherry trees lit by paper lanterns at night"},
                {"lat": 35.6595, "lng": 139.7005, "label": "Shibuya Crossing", "num": 5, "cat": "attraction", "desc": "World's busiest intersection"},
                {"lat": 35.6469, "lng": 139.6991, "label": "Afuri Ramen", "num": 6, "cat": "food", "desc": "Yuzu shio ramen \u2014 light, citrusy, counter seats"},
                {"lat": 35.6651, "lng": 139.6675, "label": "Bear Pond Espresso", "num": 7, "cat": "food", "desc": "Legendary Shimokitazawa espresso bar"},
                {"lat": 35.6712, "lng": 139.7125, "label": "Bills Omotesando", "num": 8, "cat": "food", "desc": "Famous ricotta hotcakes \u2014 solo-friendly counter"}
            ]
        },
        {
            "num": 4, "date": "2026-03-23",
            "neighborhoods": "Chiyoda \u00b7 Tsukiji \u00b7 Ginza",
            "title": "Imperial Sakura, Tsukiji and Ginza Farewell",
            "description": "Your final day is Tokyo at its most refined. Morning at Chidorigafuchi \u2014 the Imperial Palace moat becomes a tunnel of cherry blossoms. Fresh sushi at Tsukiji Outer Market. Afternoon in elegant Ginza, and a final farewell walk.",
            "timeBlocks": [
                {"label": "Morning",
                 "activities": [
                     {"title": "Chidorigafuchi Cherry Blossoms and Boat Ride", "description": "The most iconic sakura scene in Tokyo \u2014 260 cherry trees arch over the Imperial Palace moat, forming a pink tunnel reflected in the water. Rent a rowboat and drift under the canopy. Arrive early.", "details": ["\U0001f6a3 Boat rental: \u00a5800/30min, opens 9:30am", "\U0001f338 The walkway along the moat is equally beautiful", "\U0001f4f8 Best light is in the morning", "\U0001f3ef Kitanomaru Park is adjacent and peaceful"]},
                     {"title": "Tsukiji Outer Market", "description": "The inner wholesale market moved, but the outer market remains a wonderland of fresh sushi, tamagoyaki, and street food. Grab sushi at any counter.", "details": ["\U0001f41f Tuna, uni, scallop \u2014 all incredibly fresh", "\U0001f95a Tamagoyaki (sweet egg roll) on a stick is the signature snack", "\U0001f4cd 10 min from Chidorigafuchi by taxi or Hanzomon Line"]}
                 ],
                 "meals": [{"type": "\u2615 Breakfast", "name": "Tsukiji Outer Market Sushi", "description": "Pick any sushi counter. Fresh nigiri for breakfast is a quintessential Tokyo experience.", "meta": "\U0001f4b0 $$-$$$ \u00b7 \U0001f4cd Tsukiji Outer Market \u00b7 From 5am"}],
                 "tips": [{"type": "tip", "text": "March 23 is a Monday, so the Imperial Palace East Gardens are closed. Spend time at Chidorigafuchi walkway and Kitanomaru Park instead."}]},
                {"label": "Afternoon",
                 "activities": [
                     {"title": "Ginza Shopping District", "description": "Tokyo's most elegant neighborhood. Wide boulevards, department stores, art galleries, and craft shops. Visit Ginza Six (rooftop garden with skyline views) and Itoya stationery (12 floors of Japanese paper).", "details": ["\U0001f6cd\ufe0f Ginza Six has a stunning rooftop garden", "\u270f\ufe0f Itoya is 12 floors of stationery heaven, great for gifts", "\U0001f375 Higashiya Ginza for traditional Japanese sweets", "\U0001f4cd Walkable from Tsukiji (15 min)"]}
                 ],
                 "meals": [{"type": "\U0001f35c Lunch", "name": "Ginza Kagari", "description": "Michelin Bib Gourmand chicken paitan (white broth) ramen. Creamy, golden chicken broth unlike any ramen you've had. 9 counter seats, quick-moving queue. A perfect farewell bowl.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Ginza \u00b7 9 counter seats"}]},
                {"label": "Evening",
                 "activities": [{"title": "Farewell Walk \u2014 Yurakucho & Tokyo Station", "description": "Beneath the railway tracks near Yurakucho Station, dozens of tiny yakitori joints have served salarymen since the 1940s. Smoky, atmospheric, and deeply local. End your trip at the magnificent Tokyo Station \u2014 the restored 1914 red-brick building is beautifully lit at night.", "details": ["\U0001f3ae Dozens of tiny joints under the elevated Yamanote Line tracks", "\U0001f37a Real salaryman atmosphere", "\U0001f4cd Yurakucho Station is a 2 min walk from Ginza", "\U0001f3db\ufe0f The red-brick Marunouchi facade of Tokyo Station is stunning after dark"]}],
                 "meals": [{"type": "\U0001f377 Dinner", "name": "Yakitori under the Tracks", "description": "Pick any stall under the Yamanote Line tracks at Yurakucho. Smoky charcoal grill, counter seating, cold beer, and the rumble of trains overhead \u2014 a quintessentially Tokyo farewell.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Yurakucho Station \u00b7 Cash mostly"}],
                 "tips": [{"type": "tip", "text": "Stock up on omiyage (souvenirs) at Tokyo Station's underground shopping before heading to the airport. It's open until 9pm."}]}
            ],
            "mapPins": [
                {"lat": 35.6942, "lng": 139.7499, "label": "Chidorigafuchi", "num": 1, "cat": "attraction", "desc": "Imperial Palace moat \u2014 Tokyo's most iconic sakura tunnel"},
                {"lat": 35.6977, "lng": 139.7500, "label": "Kitanomaru Park", "num": 2, "cat": "attraction", "desc": "Peaceful park adjacent to Chidorigafuchi with cherry trees"},
                {"lat": 35.6654, "lng": 139.7707, "label": "Tsukiji Outer Market", "num": 3, "cat": "food", "desc": "Fresh sushi, tamagoyaki and street food from 5am"},
                {"lat": 35.6716, "lng": 139.7648, "label": "Ginza Six", "num": 4, "cat": "attraction", "desc": "Luxury department store with rooftop garden"},
                {"lat": 35.6709, "lng": 139.7636, "label": "Ginza Kagari", "num": 5, "cat": "food", "desc": "Michelin chicken paitan ramen \u2014 9 counter seats"},
                {"lat": 35.6753, "lng": 139.7614, "label": "Yurakucho Yakitori", "num": 7, "cat": "food", "desc": "Izakayas under the Yamanote Line tracks since the 1940s"},
                {"lat": 35.6812, "lng": 139.7671, "label": "Tokyo Station", "num": 8, "cat": "attraction", "desc": "Beautiful 1914 red-brick station, lit up magnificently at night"}
            ]
        }
    ],
    "budgetTable": [
        {"category": "Accommodation", "budget": "\u00a56,000\u201312,000/night", "midrange": "\u00a512,000\u201325,000/night", "luxury": "\u00a525,000+/night"},
        {"category": "Meals (per day)", "budget": "\u00a52,000\u20134,000/day", "midrange": "\u00a54,000\u20138,000/day", "luxury": "\u00a510,000+/day"},
        {"category": "Transport", "budget": "\u00a5500\u20131,000/day (Metro pass)", "midrange": "\u00a51,000\u20132,000/day", "luxury": "\u00a53,000+/day (taxis)"},
        {"category": "Activities", "budget": "\u00a51,000\u20133,000/day", "midrange": "\u00a53,000\u20135,000/day", "luxury": "\u00a55,000+/day"},
        {"category": "4-Day Total (solo)", "budget": "\u00a545,000\u201370,000 (~$300\u2013470)", "midrange": "\u00a570,000\u2013140,000 (~$470\u2013940)", "luxury": "\u00a5200,000+ (~$1,300+)"}
    ],
    "practicalInfo": [
        {"title": "\u2708\ufe0f Getting There", "items": ["Narita (NRT) is 1hr by Narita Express train (\u00a53,000)", "Haneda (HND) is 30 min by Keikyu Line (cheaper and faster)", "Both have excellent English signage and IC card machines at arrivals"]},
        {"title": "\U0001f3e8 Where to Stay", "items": ["Shinjuku: Best nightlife access, massive transport hub, huge price range", "Asakusa: Historic vibe, steps from Senso-ji, great capsule/budget hotels", "Shibuya: Central, great for Day 3 access to Harajuku/Meguro", "Shimokitazawa: For the vibe-seekers; charming, quieter, great local coffee"]},
        {"title": "\U0001f321\ufe0f Weather in Late March", "items": ["Temperatures: 10\u201317\u00b0C (50\u201363\u00b0F) \u2014 layers are essential", "Pack a light jacket; evenings can be chilly", "Occasional spring rain is possible", "March 20\u201323 is typically early bloom (first flowers opening)"]},
        {"title": "\U0001f4f1 Connectivity", "items": ["Buy a pocket Wi-Fi or data SIM at the airport (IIJmio, Mobal, Sakura Mobile)", "eSIM options: Airalo Japan plan works well, set it up before you land", "Most cafes and convenience stores have free Wi-Fi", "Download Google Maps offline for Tokyo before you arrive"]}
    ]
}

js_template = """const fulfillOrder = require('../functions/fulfill-order');

const order = {{
  id: 'order_1773933372257_6e4kmc',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-20',
  endDate: '2026-03-23',
  groupSize: 1,
}};

const itineraryData = {itinerary_json};

try {{
  const result = fulfillOrder(order, itineraryData);
  console.log('\\u2705 Fulfilled:', JSON.stringify(result, null, 2));
}} catch (err) {{
  console.error('\\u274c Error:', err.message);
  process.exit(1);
}}
"""

# Pretty-print JSON with 2-space indent
itinerary_json_str = json.dumps(itinerary_data, indent=2, ensure_ascii=False)

final_js = js_template.format(itinerary_json=itinerary_json_str)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_js)

print(f"Successfully wrote {len(final_js):,} bytes to {OUT_FILE}")
for day in itinerary_data["days"]:
    print(f"  Day {day['num']} ({day['date']}): {len(day.get('mapPins', []))} mapPins")
