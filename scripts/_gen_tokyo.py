#!/usr/bin/env python3
"""Generate the Tokyo fulfillment script."""
import json

order_str = """const order = {
  id: 'order_1773933372257_6e4kmc',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-20',
  endDate: '2026-03-23',
  groupSize: 1,
};"""

data = {
    "destination": "Tokyo, Japan",
    "countryEmoji": "\U0001f1ef\U0001f1f5",
    "title": "Solo Tokyo in Sakura Season",
    "subtitle": "4 days of cherry blossoms, ramen counters & neon-lit nights for one",
    "description": "You're arriving in Tokyo at the exact moment the city transforms. Late March is when the first sakura burst open \u2014 Shinjuku Gyoen's 1,000 trees, the lantern-lit canal at Meguro River, the moat at Chidorigafuchi turning pink. This itinerary is built for solo travelers: counter-seat ramen shops, standing sushi bars, sprawling temple grounds you can wander alone, and neighborhoods like Shimokitazawa and Yanaka where the pace slows down. Tokyo is one of the world's great solo cities \u2014 everything is designed for a party of one.",
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
        "Shimokitazawa vintage shops & craft coffee",
        "Meguro River cherry blossoms lit by paper lanterns at night"
    ],
    "essentials": [
        {"title": "\U0001f338 Cherry Blossom Timing", "text": "Late March is early bloom season in Tokyo \u2014 expect buds opening to partial bloom (March 20-23 falls right at first bloom, typically March 22-26). You'll catch the magical transition from buds to first petals. Shinjuku Gyoen has early-blooming varieties that peak before Somei Yoshino. Check real-time sakura forecasts on japan-guide.com."},
        {"title": "\U0001f687 Getting Around", "text": "Get a 72-hour Tokyo Metro pass (\u00a51,500/~$10) or use a Suica/Pasmo IC card (tap-on, works on all trains/buses/convenience stores). Google Maps transit directions are flawless in Tokyo. Trains run 5am\u2013midnight. For late nights, taxis or walk \u2014 Tokyo is extremely safe at any hour."},
        {"title": "\U0001f35c Solo Dining Culture", "text": "Tokyo is the world capital of solo dining. Counter seats at ramen shops, conveyor belt sushi (kaitenzushi), standing bars (tachinomi), and ticket-machine restaurants (shokkenki) are all designed for one. No awkwardness, no judgment \u2014 eating alone is the norm. Ichiran even has private booths with curtains."},
        {"title": "\U0001f4b4 Money & Tipping", "text": "Japan is increasingly cashless (IC cards, PayPay QR), but carry \u00a510,000-20,000 cash for small shops, shrines, and market stalls. Tipping is NOT customary and can cause confusion \u2014 the price is the price. Convenience stores (7-Eleven, Lawson, FamilyMart) have international ATMs."}
    ],
    "days": [
        {
            "num": 1, "date": "2026-03-20",
            "neighborhoods": "Shinjuku \u00b7 Shinjuku Gyoen \u00b7 Kabukicho",
            "title": "Shinjuku \u2014 Gardens, Neon & Late-Night Ramen",
            "description": "Start in the heart of Tokyo's biggest district. Morning in the serene gardens of Shinjuku Gyoen chasing early cherry blossoms, afternoon exploring the labyrinthine streets around the station, and evening diving into Kabukicho's electric nightlife \u2014 all within walking distance.",
            "timeBlocks": [
                {
                    "label": "Morning",
                    "activities": [{"title": "Shinjuku Gyoen National Garden", "description": "Tokyo's finest cherry blossom garden \u2014 58 hectares with over 1,000 trees across 70+ varieties, including early-blooming kanzan and shidarezakura (weeping cherry). Arrive at opening to have the grounds nearly to yourself. The Japanese Traditional Garden section, with sakura reflecting in the pond, is the most photogenic spot in the city.", "details": ["\U0001f338 \u00a5500 entry \u00b7 Opens 9:00am \u00b7 No alcohol allowed (keeps it peaceful)", "\U0001f4f8 Best spots: Japanese Garden pond, English Landscape lawn, Taiwan Pavilion", "\U0001f6b6 Give yourself 2+ hours \u2014 vast and every corner has something", "\U0001f392 Bag check at entrance \u2014 no tripods or large bags inside"]}],
                    "meals": [{"type": "\u2615 Breakfast", "name": "Konbini Coffee & Onigiri", "description": "Start the day the Tokyo way \u2014 grab a hot can coffee and a salmon onigiri from any 7-Eleven near Shinjuku Station. Japanese convenience store food is legitimately excellent. Try the egg sandwich (tamago sando) too.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Any 7-Eleven, Lawson, or FamilyMart \u00b7 24h"}],
                    "tips": [{"type": "tip", "text": "Shinjuku Gyoen opens at 9am sharp. Be in line by 8:50 \u2014 the first 30 minutes are magical before tour groups arrive. Use the Shinjuku Gate entrance, closest to the station."}]
                },
                {
                    "label": "Afternoon",
                    "activities": [
                        {"title": "Omoide Yokocho (Memory Lane)", "description": "A narrow strip of tiny yakitori stalls behind Shinjuku Station's west exit, here since the post-war era. Each stall seats 6-8 people at smoky counters. Order chicken skewers and a draft beer, watch the grill master work \u2014 old Tokyo at its finest.", "details": ["\U0001f3ee Each stall seats 6-8, perfect for solo counter dining", "\U0001f362 Must-try: negima (chicken & leek), tsukune (meatball), kawa (crispy skin)", "\U0001f4b0 Cash only at most stalls"]},
                        {"title": "Tokyo Metropolitan Government Building Observatory", "description": "Free observation deck on the 45th floor with panoramic views of Tokyo \u2014 on clear days you can see Mt. Fuji. No ticket needed, just security and elevator up.", "details": ["\U0001f193 Free entry \u00b7 Open until 11pm (South Tower)", "\U0001f5fb Best Mt. Fuji views: clear mornings or just before sunset", "\U0001f4cd 5 min walk from Shinjuku Station west exit"]}
                    ],
                    "meals": [{"type": "\U0001f35c Lunch", "name": "Fuunji (\u98a8\u96f2\u5150)", "description": "One of Tokyo's most legendary tsukemen (dipping ramen) shops. Thick, rich fish-and-pork broth with perfectly chewy noodles. Solo counter seats, ticket machine ordering. Queue moves fast.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Yoyogi, 5 min south of Shinjuku Station \u00b7 Counter seats only"}]
                },
                {
                    "label": "Evening",
                    "activities": [{"title": "Kabukicho & Golden Gai", "description": "Tokyo's most famous nightlife district. Kabukicho is neon-drenched \u2014 Godzilla on the Toho building, pachinko, arcades. Then Golden Gai: six narrow alleys, 200+ tiny bars seating 5-10 each. Many welcome solo travelers; this is where you make friends over whisky.", "details": ["\U0001f37a Golden Gai \u2014 \u00a5500-1000 cover + drinks from \u00a5700", "\U0001f4f8 Kabukicho neon looks best just after dark (6:30-7:30pm)", "\U0001f6ab Some bars regulars-only \u2014 look for 'Tourists Welcome' signs", "\U0001f3ae Solo karaoke (hitokara) \u2014 private rooms from \u00a5500/30min"]}],
                    "meals": [{"type": "\U0001f377 Dinner", "name": "Omoide Yokocho Yakitori (Round 2)", "description": "Return to Memory Lane for dinner \u2014 it transforms at night when lanterns glow and smoke billows. Pick any stall, counter seat, charcoal-grilled chicken with cold Asahi.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omoide Yokocho, Shinjuku west exit \u00b7 Cash only"}],
                    "tips": [{"type": "tip", "text": "Golden Gai is best around 8-9pm. Bars are tiny \u2014 if one's full, try next door. 200+ options. Many bartenders speak some English."}]
                }
            ],
            "mapPins": [
                {"lat": 35.6852, "lng": 139.7100, "label": "Shinjuku Gyoen", "num": 1, "cat": "attraction", "desc": "Tokyo's premier cherry blossom garden \u2014 1,000 trees"},
                {"lat": 35.6938, "lng": 139.7005, "label": "Tokyo Metro Govt Building", "num": 2, "cat": "attraction", "desc": "Free 45th-floor observatory with Mt. Fuji views"},
                {"lat": 35.6896, "lng": 139.6983, "label": "Omoide Yokocho", "num": 3, "cat": "food", "desc": "Post-war yakitori alley \u2014 counter seats"},
                {"lat": 35.6862, "lng": 139.6988, "label": "Fuunji", "num": 4, "cat": "food", "desc": "Legendary tsukemen ramen"},
                {"lat": 35.6942, "lng": 139.7035, "label": "Golden Gai", "num": 5, "cat": "nightlife", "desc": "200+ tiny bars in six alleys"},
                {"lat": 35.6948, "lng": 139.7015, "label": "Kabukicho", "num": 6, "cat": "nightlife", "desc": "Tokyo's neon-lit entertainment district"}
            ]
        },
        {
            "num": 2, "date": "2026-03-21",
            "neighborhoods": "Asakusa \u00b7 Ueno \u00b7 Yanaka \u00b7 Akihabara",
            "title": "Old Tokyo \u2014 Temples, Markets & Otaku Culture",
            "description": "A journey through time. Dawn at the 7th-century Senso-ji, morning in nostalgic Yanaka, afternoon cherry blossoms at Ueno Park, and evening in Akihabara's electric wonderland.",
            "timeBlocks": [
                {
                    "label": "Morning",
                    "activities": [
                        {"title": "Senso-ji Temple at Dawn", "description": "Tokyo's oldest temple (founded 645 AD) is packed by 10am \u2014 but at 6:30am, you'll have the Thunder Gate, massive red lantern, and incense-filled main hall to yourself. Nakamise street is shuttered and atmospheric.", "details": ["\u26e9\ufe0f Grounds open 24h \u00b7 Main hall opens 6:00-6:30am", "\U0001f4f8 Thunder Gate (Kaminarimon) \u2014 iconic, zero crowds at dawn", "\U0001f38b Omikuji fortune (\u00a5100) \u2014 bad luck? Tie it to the rack", "\U0001f3ee Five-story pagoda \u2014 best morning light"]},
                        {"title": "Yanaka Ginza & Yanaka Cemetery", "description": "Yanaka survived WWII firebombing and feels like 1950s Tokyo. Retro shopping street with street food, cat statues, zero chains. The cemetery has a stunning cherry blossom tunnel.", "details": ["\U0001f431 Tokyo's 'cat town' \u2014 real cats and cat-themed everything", "\U0001f338 Yanaka Cemetery sakura tunnel \u2014 most peaceful blossom spot", "\U0001f361 Try menchi-katsu and taiyaki from street stalls", "\U0001f4cd Nippori Station \u2192 3 min walk"]}
                    ],
                    "meals": [{"type": "\u2615 Breakfast", "name": "Pelican Caf\u00e9", "description": "Legendary bakery making Japan's most famous shokupan (milk bread) since 1942. Thick-cut toast, eggs, coffee. Solo-friendly counter.", "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Taito, near Asakusa \u00b7 Opens 8:00am \u00b7 Counter"}],
                    "tips": [{"type": "tip", "text": "From Senso-ji, take Yamanote Line from Uguisudani to Nippori for Yanaka. 15 min, feels like teleporting to a different era."}]
                },
                {
                    "label": "Afternoon",
                    "activities": [
                        {"title": "Ueno Park Cherry Blossoms", "description": "Japan's most famous hanami park \u2014 1,000+ cherry trees line the main avenue. During bloom the path becomes a pink tunnel. Grab a konbini bento and sit under the trees like a local.", "details": ["\U0001f338 Main cherry avenue is the classic hanami scene", "\U0001f3db\ufe0f Tokyo National Museum \u2014 Japan's oldest & largest (\u00a51,000)", "\U0001f9a2 Shinobazu Pond \u2014 swan boat for a solo cruise", "\U0001f371 Konbini bento + Strong Zero under sakura = peak Tokyo"]},
                        {"title": "Ameyoko Market", "description": "Bustling open-air market under the Yamanote Line tracks. Fresh seafood, dried fruits, chocolate strawberries \u2014 Southeast Asian energy in central Tokyo.", "details": ["\U0001f990 Fresh uni, crab legs, grilled scallops on sticks", "\U0001f36b Chocolate strawberries near Okachimachi end", "\U0001f4b0 Cash preferred"]}
                    ],
                    "meals": [{"type": "\U0001f35c Lunch", "name": "Sansada Tempura", "description": "Operating since 1837 \u2014 Asakusa institution serving crispy tempura at the counter. Watch each piece fried to order. Tendon ~\u00a51,500.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Asakusa, near Senso-ji \u00b7 Counter seats"}]
                },
                {
                    "label": "Evening",
                    "activities": [{"title": "Akihabara Electric Town", "description": "Ancient temples to anime paradise in one subway ride. Multi-story arcades, manga shops, retro game stores. Even non-otaku love the sensory overload.", "details": ["\U0001f3ae Super Potato \u2014 5 floors retro games, playable consoles", "\U0001f4e6 Mandarake \u2014 secondhand manga and collectibles", "\U0001f579\ufe0f Arcades \u2014 crane games, rhythm games, purikura", "\U0001f4cd Best after dark when neon comes alive"]}],
                    "meals": [{"type": "\U0001f377 Dinner", "name": "Kanda Yabu Soba", "description": "One of Tokyo's three great soba restaurants, established 1880. Hand-cut buckwheat noodles cold on bamboo with dipping sauce. Minimalist, meditative. Beautiful wooden building.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Kanda, between Akihabara & Ueno"}],
                    "tips": [{"type": "tip", "text": "For solo conveyor belt sushi, try Sushiro or Kura Sushi \u2014 order from tablet, sushi arrives on mini train. No interaction needed."}]
                }
            ],
            "mapPins": [
                {"lat": 35.7148, "lng": 139.7967, "label": "Senso-ji Temple", "num": 1, "cat": "attraction", "desc": "Tokyo's oldest temple \u2014 stunning at dawn"},
                {"lat": 35.7270, "lng": 139.7673, "label": "Yanaka Ginza", "num": 2, "cat": "attraction", "desc": "Retro street in old-Tokyo neighborhood"},
                {"lat": 35.7286, "lng": 139.7713, "label": "Yanaka Cemetery", "num": 3, "cat": "attraction", "desc": "Sakura-lined cemetery walk"},
                {"lat": 35.7146, "lng": 139.7732, "label": "Ueno Park", "num": 4, "cat": "attraction", "desc": "Tokyo's most famous hanami spot"},
                {"lat": 35.7103, "lng": 139.7748, "label": "Ameyoko Market", "num": 5, "cat": "food", "desc": "Open-air market \u2014 seafood & street food"},
                {"lat": 35.7022, "lng": 139.7705, "label": "Akihabara", "num": 6, "cat": "attraction", "desc": "Electric Town \u2014 anime, games, otaku"},
                {"lat": 35.7104, "lng": 139.7913, "label": "Pelican Caf\u00e9", "num": 7, "cat": "food", "desc": "Legendary shokupan bakery since 1942"},
                {"lat": 35.6997, "lng": 139.7667, "label": "Kanda Yabu Soba", "num": 8, "cat": "food", "desc": "Historic soba since 1880"}
            ]
        },
        {
            "num": 3, "date": "2026-03-22",
            "neighborhoods": "Harajuku \u00b7 Shibuya \u00b7 Shimokitazawa \u00b7 Nakameguro",
            "title": "West Side \u2014 Vintage, Vinyl & River Blossoms",
            "description": "The creative, youthful side of Tokyo. Morning at Meiji Shrine and Harajuku, afternoon in Shimokitazawa's vintage shops, evening along the Meguro River watching cherry blossoms glow under paper lanterns.",
            "timeBlocks": [
                {
                    "label": "Morning",
                    "activities": [
                        {"title": "Meiji Shrine (Meiji Jingu)", "description": "Walk through the towering torii gate into 170 acres of old-growth forest \u2014 right in central Tokyo. The approach feels like leaving the city. Write a wish on an ema wooden plaque.", "details": ["\u26e9\ufe0f Free entry \u00b7 Opens at sunrise (~5:40am in March)", "\U0001f332 Forest planted in 1920 with 100,000 donated trees", "\U0001f4f8 The massive cypress torii gate is the photo", "\U0001f38b Ema plaque (\u00a5500) \u2014 write a wish, read others'"]},
                        {"title": "Harajuku & Takeshita Street", "description": "Ancient forest to youth fashion capital. Takeshita Street: crepe shops, kawaii fashion, sensory overload. Cat Street: cooler independent boutiques and cafes.", "details": ["\U0001f366 Giant cotton candy and crepes \u2014 Harajuku signatures", "\U0001f457 Cat Street for independent Japanese fashion", "\u2615 % Arabica Coffee \u2014 minimalist espresso perfection"]}
                    ],
                    "meals": [{"type": "\u2615 Breakfast", "name": "Bills Omotesando", "description": "Australian cafe famous for ricotta hotcakes \u2014 fluffy, pillowy pancakes practically mandatory in Tokyo. Solo counter seats overlooking the kitchen.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omotesando \u00b7 Opens 8:30am \u00b7 Solo counter"}]
                },
                {
                    "label": "Afternoon",
                    "activities": [{"title": "Shimokitazawa", "description": "Tokyo's most beloved bohemian neighborhood \u2014 narrow streets packed with vintage clothing, record stores, curry restaurants, live music venues. Feels like a village inside a megacity. Perfect for solo wandering.", "details": ["\U0001f455 Vintage: Flamingo, Stick Out, New York Joe Exchange", "\U0001f35b Curry town \u2014 try Curry Spice Gelateria", "\U0001f3b5 Afternoon live shows at Shelter or Club Que", "\u2615 Bear Pond Espresso \u2014 legendary barista"]}],
                    "meals": [{"type": "\U0001f35c Lunch", "name": "Curry Spice Gelateria", "description": "Shimokitazawa original \u2014 artisanal curry + rotating spice-infused gelatos. Counter seats, solo-perfect.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Shimokitazawa \u00b7 Counter seating"}],
                    "tips": [{"type": "tip", "text": "Shimokitazawa is 3 stops from Shibuya on Keio-Inokashira line. South = vintage, north = food. Just wander."}]
                },
                {
                    "label": "Evening",
                    "activities": [
                        {"title": "Meguro River Cherry Blossoms (Night)", "description": "The 4km stretch from Nakameguro to Meguro is lined with 800+ cherry trees. During bloom, thousands of pink paper lanterns illuminate the petals \u2014 reflections ripple in the water. Walk the whole length, stop at pop-up bars.", "details": ["\U0001f3ee Lantern illumination daily, dusk to 9pm", "\U0001f377 Pop-up wine stands along the riverbank", "\U0001f4cd Start at Nakameguro Station, walk south", "\U0001f4f8 Bridge near Nakameguro Station is the money shot"]},
                        {"title": "Shibuya Crossing", "description": "The world's busiest intersection. Watch from Starbucks 2F, then cross with the crowd. Find the Hachiko statue.", "details": ["\U0001f4f8 Best views: Starbucks 2F or Mag's Park rooftop (free)", "\U0001f415 Hachiko statue \u2014 north exit", "\U0001f303 Most impressive after dark"]}
                    ],
                    "meals": [{"type": "\U0001f377 Dinner", "name": "Afuri Ramen Nakameguro", "description": "Light, refreshing yuzu shio (citrus salt) ramen \u2014 clear golden broth with a yuzu punch. Counter-seat-only. Perfect after a sakura walk.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Nakameguro \u00b7 Counter seats \u00b7 Ticket machine"}]
                }
            ],
            "mapPins": [
                {"lat": 35.6764, "lng": 139.6993, "label": "Meiji Shrine", "num": 1, "cat": "attraction", "desc": "170 acres of forest, most visited shrine"},
                {"lat": 35.6702, "lng": 139.7026, "label": "Harajuku / Takeshita St", "num": 2, "cat": "attraction", "desc": "Youth fashion \u2014 crepes, kawaii, Cat Street"},
                {"lat": 35.6610, "lng": 139.6682, "label": "Shimokitazawa", "num": 3, "cat": "attraction", "desc": "Bohemian \u2014 vintage, vinyl, curry"},
                {"lat": 35.6441, "lng": 139.6985, "label": "Meguro River", "num": 4, "cat": "attraction", "desc": "800+ cherry trees lit by lanterns"},
                {"lat": 35.6595, "lng": 139.7005, "label": "Shibuya Crossing", "num": 5, "cat": "attraction", "desc": "World's busiest intersection"},
                {"lat": 35.6469, "lng": 139.6991, "label": "Afuri Ramen", "num": 6, "cat": "food", "desc": "Yuzu shio ramen \u2014 light, citrusy"},
                {"lat": 35.6651, "lng": 139.6675, "label": "Bear Pond Espresso", "num": 7, "cat": "food", "desc": "Legendary Shimokitazawa espresso"},
                {"lat": 35.6712, "lng": 139.7125, "label": "Bills Omotesando", "num": 8, "cat": "food", "desc": "Famous ricotta hotcakes"}
            ]
        },
        {
            "num": 4, "date": "2026-03-23",
            "neighborhoods": "Chiyoda \u00b7 Imperial Palace \u00b7 Tsukiji \u00b7 Ginza",
            "title": "Imperial Sakura, Tsukiji & Ginza Farewell",
            "description": "Your final day is Tokyo at its most refined. Morning at Chidorigafuchi \u2014 the Imperial Palace moat becomes a tunnel of cherry blossoms. Fresh sushi at Tsukiji Outer Market. Afternoon in elegant Ginza, evening illuminated cherry blossoms at Rikugien Garden.",
            "timeBlocks": [
                {
                    "label": "Morning",
                    "activities": [
                        {"title": "Chidorigafuchi Cherry Blossoms & Boat Ride", "description": "The most iconic sakura scene in Tokyo \u2014 260 cherry trees arch over the Imperial Palace moat, forming a pink tunnel reflected in the water. Rent a rowboat and drift under the canopy.", "details": ["\U0001f6a3 Boat rental: \u00a5800/30min \u00b7 Opens 9:30am during sakura season", "\U0001f338 Walkway along the moat is equally beautiful without a boat", "\U0001f4f8 Best light: morning sun against the moat", "\U0001f3ef Nearby: Imperial Palace East Gardens (free, closed Mon/Fri)"]},
                        {"title": "Kitanomaru Park", "description": "Adjacent to Chidorigafuchi \u2014 former Imperial Guard grounds, now a peaceful park with cherry trees and walking paths. Much less crowded. The Nippon Budokan concert hall is here.", "details": ["\U0001f193 Free entry \u00b7 Open 24h", "\U0001f338 Cherry trees throughout, beautiful morning light", "\U0001f4cd 5 min walk from Kudanshita Station"]}
                    ],
                    "meals": [{"type": "\u2615 Breakfast", "name": "Tsukiji Outer Market Sushi", "description": "The inner wholesale market moved to Toyosu, but the outer market is still a wonderland of fresh sushi, tamagoyaki, and street food. Grab sushi at any counter \u2014 all source from the same market. Fresh tuna at 7am hits different.", "meta": "\U0001f4b0 $$-$$$ \u00b7 \U0001f4cd Tsukiji Outer Market \u00b7 From 5am \u00b7 Counter seats"}],
                    "tips": [{"type": "tip", "text": "March 23 is a Monday \u2014 Imperial Palace East Gardens close Mon & Fri. Spend time at Chidorigafuchi walkway and Kitanomaru Park instead."}]
                },
                {
                    "label": "Afternoon",
                    "activities": [
                        {"title": "Ginza Shopping District", "description": "Tokyo's most elegant neighborhood \u2014 wide boulevards, department stores, art galleries. Visit Ginza Six (rooftop garden), Itoya stationery (12 floors of Japanese paper and pens), and the architectural parade along Chuo-dori.", "details": ["\U0001f6cd\ufe0f Ginza Six \u2014 luxury dept store with rooftop garden", "\u270f\ufe0f Itoya \u2014 12 floors of stationery heaven, perfect gifts", "\U0001f375 Higashiya Ginza \u2014 traditional sweets with matcha", "\U0001f4cd Walkable from Tsukiji (15 min)"]},
                        {"title": "Rikugien Garden (Evening Illumination)", "description": "One of Tokyo's most beautiful Edo-period landscape gardens. During late March, the famous weeping cherry tree is illuminated at night \u2014 a single massive shidarezakura lit dramatically against the dark garden. One of Tokyo's most poetic sakura views.", "details": ["\U0001f338 Illumination: Mar 20 to Apr 6, 2026 \u2014 17:00 to 21:00", "\U0001f4a1 Weeping cherry at entrance is the star \u2014 arrive before sunset", "\u00a5300 entry \u00b7 \U0001f4cd Komagome Station, 2 min walk", "\U0001f375 Tea house inside serves matcha with seasonal wagashi"]}
                    ],
                    "meals": [{"type": "\U0001f35c Lunch", "name": "Ginza Kagari", "description": "Michelin-recommended chicken paitan (white broth) ramen in Ginza. Creamy