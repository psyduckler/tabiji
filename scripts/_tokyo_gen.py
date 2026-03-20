#!/usr/bin/env python3
"""Generate Tokyo itinerary fulfillment script."""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "fulfill-order_1773933372257_6e4kmc.js")

D = {
  "destination": "Tokyo, Japan",
  "countryEmoji": "\U0001f1ef\U0001f1f5",
  "title": "Solo Tokyo in Sakura Season",
  "subtitle": "4 days of cherry blossoms, ramen counters & neon-lit nights for one",
  "description": ("You\u2019re arriving in Tokyo at the exact moment the city transforms. Late March is when the "
                  "first sakura burst open \u2014 Shinjuku Gyoen\u2019s 1,000 trees, the lantern-lit canal at Meguro River, "
                  "the moat at Chidorigafuchi turning pink. This itinerary is built for solo travelers: counter-seat "
                  "ramen shops, standing sushi bars, sprawling temple grounds to wander alone, and neighborhoods like "
                  "Shimokitazawa and Yanaka where the pace slows down. Tokyo is one of the world\u2019s great solo "
                  "cities \u2014 everything is designed for a party of one."),
  "duration": "3 nights",
  "dates": "Mar 20 \u2013 Mar 23, 2026",
  "budget": "$$",
  "pace": "Moderate",
  "bestFor": "Solo Travelers",
  "highlights": [
    "Cherry blossoms at Shinjuku Gyoen \u2014 70+ varieties, 1,000 trees",
    "Chidorigafuchi moat boat ride under sakura canopy",
    "Tsukemen at Fuunji \u2014 Tokyo\u2019s best dipping ramen",
    "Senso-ji Temple at dawn \u2014 Asakusa without the crowds",
    "Shimokitazawa vintage shops and craft coffee",
    "Meguro River cherry blossoms lit by paper lanterns at night"
  ],
  "essentials": [
    {"title": "\U0001f338 Cherry Blossom Timing",
     "text": ("Late March is early bloom season \u2014 March 20\u201323 falls right at first bloom "
              "(typically March 22\u201326). You\u2019ll catch the magical transition from buds to first petals. "
              "Shinjuku Gyoen has early-blooming varieties that peak before Somei Yoshino. Check real-time "
              "sakura forecasts on japan-guide.com.")},
    {"title": "\U0001f687 Getting Around",
     "text": ("Get a 72-hour Tokyo Metro pass (\u00a51,500/~$10) or a Suica/Pasmo IC card \u2014 tap-on, works on "
              "all trains, buses, and convenience stores. Google Maps transit is flawless in Tokyo. "
              "Trains run 5am\u2013midnight. For late nights, taxi or walk \u2014 Tokyo is extremely safe at any hour.")},
    {"title": "\U0001f35c Solo Dining Culture",
     "text": ("Tokyo is the world capital of solo dining. Counter seats at ramen shops, conveyor belt sushi "
              "(kaitenzushi), standing bars (tachinomi), and ticket-machine restaurants are all designed for one. "
              "No awkwardness, no judgment \u2014 eating alone is completely normal. Ichiran even has private "
              "booths with curtains.")},
    {"title": "\U0001f4b4 Money and Tipping",
     "text": ("Japan is increasingly cashless (IC cards, PayPay), but carry \u00a510,000\u201320,000 cash for small shops, "
              "shrines, and market stalls. Tipping is NOT customary \u2014 the price is the price. 7-Eleven, Lawson, "
              "and FamilyMart have international ATMs and genuinely excellent food.")}
  ],
  "days": [
    # ─── DAY 1 ───────────────────────────────────────────────────────────────
    {
      "num": 1, "date": "2026-03-20",
      "neighborhoods": "Shinjuku \u00b7 Shinjuku Gyoen \u00b7 Kabukicho",
      "title": "Shinjuku \u2014 Gardens, Neon and Late-Night Ramen",
      "description": ("Start in the heart of Tokyo\u2019s biggest district. Morning in the serene gardens of "
                      "Shinjuku Gyoen chasing early cherry blossoms, afternoon exploring the labyrinthine streets "
                      "around the station, evening diving into Kabukicho\u2019s electric nightlife \u2014 all within "
                      "walking distance."),
      "timeBlocks": [
        {
          "label": "Morning",
          "activities": [{"title": "Shinjuku Gyoen National Garden",
            "description": ("Tokyo\u2019s finest cherry blossom garden \u2014 58 hectares with 1,000+ trees across "
                            "70+ varieties, including early-blooming kanzan and shidarezakura (weeping cherry). "
                            "Arrive at opening to have the grounds nearly to yourself. The Japanese Traditional "
                            "Garden section, with sakura reflecting in the pond, is the most photogenic spot in the city."),
            "details": ["\U0001f338 \u00a5500 entry, opens 9am, no alcohol (keeps it peaceful)",
                        "\U0001f4f8 Best: Japanese Garden pond, English Landscape lawn, Taiwan Pavilion",
                        "\U0001f6b6 Give yourself 2+ hours \u2014 vast and every corner has something",
                        "\U0001f392 Bag check at entrance, no tripods or large bags inside"]}],
          "meals": [{"type": "\u2615 Breakfast", "name": "Konbini Coffee and Onigiri",
            "description": ("Start the day the Tokyo way \u2014 hot canned coffee and a salmon onigiri from any "
                            "7-Eleven near Shinjuku Station. Japanese convenience store food is legitimately excellent. "
                            "Try the egg sandwich (tamago sando) too."),
            "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Any 7-Eleven, Lawson, or FamilyMart \u00b7 24h"}],
          "tips": [{"type": "tip", "text": ("Shinjuku Gyoen opens at 9am sharp. Be in line by 8:50 \u2014 the "
                                            "first 30 minutes are magical before tour groups arrive. Use the "
                                            "Shinjuku Gate entrance, closest to the station.")}]
        },
        {
          "label": "Afternoon",
          "activities": [
            {"title": "Omoide Yokocho (Memory Lane)",
             "description": ("Narrow strip of tiny yakitori stalls behind Shinjuku Station\u2019s west exit, "
                             "here since the post-war era. Each stall seats 6\u20138 at smoky counters. Order chicken "
                             "skewers and a draft beer, watch the grill master work."),
             "details": ["\U0001f3ee Each stall seats 6\u20138 \u2014 perfect for solo counter dining",
                         "\U0001f362 Must-try: negima (chicken and leek), tsukune (meatball), kawa (crispy skin)",
                         "\U0001f4b0 Cash only at most stalls"]},
            {"title": "Tokyo Metropolitan Government Building Observatory",
             "description": ("Free observation deck on the 45th floor with panoramic views \u2014 on clear days "
                             "you can see Mt. Fuji. No ticket needed, just security and the elevator."),
             "details": ["\U0001f193 Free entry, open until 11pm (South Tower)",
                         "\U0001f5fb Best Mt. Fuji views: clear mornings or just before sunset",
                         "\U0001f4cd 5 min walk from Shinjuku Station west exit"]}
          ],
          "meals": [{"type": "\U0001f35c Lunch", "name": "Fuunji",
            "description": ("One of Tokyo\u2019s most legendary tsukemen (dipping ramen) shops. Thick, rich "
                            "fish-and-pork broth with perfectly chewy noodles. Solo counter seats, ticket machine "
                            "ordering. Queue moves fast."),
            "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Yoyogi, 5 min south of Shinjuku Station \u00b7 Counter seats only"}]
        },
        {
          "label": "Evening",
          "activities": [{"title": "Kabukicho and Golden Gai",
            "description": ("Tokyo\u2019s most famous nightlife district. Kabukicho is neon-drenched \u2014 Godzilla "
                            "on the Toho building, pachinko parlors, arcades. Then Golden Gai: six narrow alleys, "
                            "200+ tiny bars seating 5\u201310 each. Many welcome solo travelers \u2014 this is where "
                            "you make friends over whisky."),
            "details": ["\U0001f37a Golden Gai \u2014 \u00a5500\u20131000 cover plus drinks from \u00a5700",
                        "\U0001f4f8 Kabukicho neon best just after dark (6:30\u20137:30pm)",
                        "\U0001f6ab Some bars regulars-only \u2014 look for Tourists Welcome signs",
                        "\U0001f3ae Solo karaoke (hitokara) \u2014 private rooms from \u00a5500/30min nearby"]}],
          "meals": [{"type": "\U0001f377 Dinner", "name": "Omoide Yokocho Yakitori Round 2",
            "description": ("Return to Memory Lane for dinner \u2014 it transforms at night when lanterns glow "
                            "and smoke billows. Pick any stall, sit at the counter, charcoal-grilled chicken "
                            "with cold Asahi."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omoide Yokocho, Shinjuku west exit \u00b7 Cash only"}],
          "tips": [{"type": "tip", "text": ("Golden Gai is best around 8\u20139pm. Bars are tiny \u2014 if one\u2019s "
                                            "full, try next door. There are 200+ options. Many bartenders speak "
                                            "some English.")}]
        }
      ],
      "mapPins": [
        {"lat": 35.6852, "lng": 139.7100, "label": "Shinjuku Gyoen", "num": 1, "cat": "attraction", "desc": "Tokyo\u2019s premier cherry blossom garden \u2014 1,000 trees"},
        {"lat": 35.6938, "lng": 139.7005, "label": "Tokyo Metro Govt Building", "num": 2, "cat": "attraction", "desc": "Free 45th-floor observatory with Mt. Fuji views"},
        {"lat": 35.6896, "lng": 139.6983, "label": "Omoide Yokocho", "num": 3, "cat": "food", "desc": "Post-war yakitori alley \u2014 smoky counter seating"},
        {"lat": 35.6862, "lng": 139.6988, "label": "Fuunji", "num": 4, "cat": "food", "desc": "Legendary tsukemen dipping ramen \u2014 solo counter"},
        {"lat": 35.6942, "lng": 139.7035, "label": "Golden Gai", "num": 5, "cat": "nightlife", "desc": "200+ tiny bars in six narrow alleys"},
        {"lat": 35.6948, "lng": 139.7015, "label": "Kabukicho", "num": 6, "cat": "nightlife", "desc": "Tokyo\u2019s neon-lit entertainment district"}
      ]
    },
    # ─── DAY 2 ───────────────────────────────────────────────────────────────
    {
      "num": 2, "date": "2026-03-21",
      "neighborhoods": "Asakusa \u00b7 Ueno \u00b7 Yanaka \u00b7 Akihabara",
      "title": "Old Tokyo \u2014 Temples, Markets and Otaku Culture",
      "description": ("A journey through time. Dawn at the 7th-century Senso-ji Temple, morning in nostalgic "
                      "Yanaka, afternoon cherry blossoms at Ueno Park, and evening in Akihabara\u2019s electric "
                      "wonderland. East Tokyo is where tradition and obsession collide."),
      "timeBlocks": [
        {
          "label": "Morning",
          "activities": [
            {"title": "Senso-ji Temple at Dawn",
             "description": ("Tokyo\u2019s oldest temple (founded 645 AD) is packed by 10am \u2014 but at 6:30am "
                             "you\u2019ll have the Thunder Gate, massive red lantern, and incense-filled main hall "
                             "to yourself. Nakamise street is shuttered and atmospheric. Walk slowly and watch the "
                             "monks begin morning rituals."),
             "details": ["\u26e9\ufe0f Grounds open 24h, main hall opens 6:00\u20136:30am (seasonal)",
                         "\U0001f4f8 Thunder Gate (Kaminarimon) \u2014 iconic, zero crowds at dawn",
                         "\U0001f38b Omikuji fortune (\u00a5100) \u2014 bad luck? Tie it to the rack",
                         "\U0001f3ee Five-story pagoda area has the best morning light"]},
            {"title": "Yanaka Ginza and Yanaka Cemetery",
             "description": ("Yanaka survived WWII firebombing and feels like 1950s Tokyo. Retro shopping "
                             "street with street food, cat statues, zero chain stores. The adjacent cemetery "
                             "has a stunning cherry blossom tunnel \u2014 a canopy of sakura lines the main path."),
             "details": ["\U0001f431 Tokyo\u2019s cat town \u2014 real cats and cat-themed shops everywhere",
                         "\U0001f338 Yanaka Cemetery sakura tunnel \u2014 most peaceful blossom spot in Tokyo",
                         "\U0001f361 Try menchi-katsu (fried croquette) and taiyaki from stalls",
                         "\U0001f4cd Nippori Station, 3 min walk"]}
          ],
          "meals": [{"type": "\u2615 Breakfast", "name": "Pelican Cafe",
            "description": ("Near Asakusa \u2014 legendary bakery making Japan\u2019s most famous shokupan (milk bread) "
                            "since 1942. Thick-cut toast, eggs, and coffee. Simple, perfect, solo-friendly counter."),
            "meta": "\U0001f4b0 $ \u00b7 \U0001f4cd Taito, near Asakusa \u00b7 Opens 8am \u00b7 Counter seating"}],
          "tips": [{"type": "tip", "text": ("From Senso-ji, take the Yamanote Line from Uguisudani to Nippori "
                                            "for Yanaka. 15 minutes and feels like teleporting to a different era.")}]
        },
        {
          "label": "Afternoon",
          "activities": [
            {"title": "Ueno Park Cherry Blossoms",
             "description": ("Japan\u2019s most famous hanami park \u2014 1,000+ cherry trees line the main avenue, "
                             "and during bloom season the path becomes a pink tunnel with families picnicking "
                             "underneath. Grab a konbini bento and sit under the trees like a local."),
             "details": ["\U0001f338 Main cherry avenue is the classic hanami scene in Tokyo",
                         "\U0001f3db\ufe0f Tokyo National Museum \u2014 Japan\u2019s oldest and largest (\u00a51,000)",
                         "\U0001f9a2 Shinobazu Pond \u2014 rent a swan boat solo",
                         "\U0001f371 Konbini bento plus Strong Zero under sakura = peak Tokyo"]},
            {"title": "Ameyoko Market",
             "description": ("Bustling open-air market under the Yamanote Line tracks. Fresh seafood, dried "
                             "fruits, chocolate strawberries \u2014 Southeast Asian energy right in central Tokyo."),
             "details": ["\U0001f990 Fresh uni, crab legs, grilled scallops on sticks",
                         "\U0001f36b Chocolate strawberries near the Okachimachi end",
                         "\U0001f4b0 Cash preferred at most stalls"]}
          ],
          "meals": [{"type": "\U0001f35c Lunch", "name": "Sansada Tempura",
            "description": ("Operating since 1837 \u2014 Asakusa institution serving crispy tempura at the counter. "
                            "Watch each piece fried to order. The tendon (tempura rice bowl) is about \u00a51,500 and legendary."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Asakusa, near Senso-ji \u00b7 Counter seats"}]
        },
        {
          "label": "Evening",
          "activities": [{"title": "Akihabara Electric Town",
            "description": ("Ancient temples to anime paradise in one subway ride. Multi-story arcades, manga "
                            "shops, retro game stores, and electronics. Even non-otaku love the sensory overload. "
                            "Try the vintage game floors at Super Potato."),
            "details": ["\U0001f3ae Super Potato \u2014 5 floors retro games, playable consoles on top floor",
                        "\U0001f4e6 Mandarake \u2014 massive secondhand manga and collectibles",
                        "\U0001f579\ufe0f Arcades \u2014 crane games, rhythm games, purikura photo booths",
                        "\U0001f4cd Best experienced after dark when all the neon comes alive"]}],
          "meals": [{"type": "\U0001f377 Dinner", "name": "Kanda Yabu Soba",
            "description": ("One of Tokyo\u2019s three great soba restaurants, established 1880. Hand-cut buckwheat "
                            "noodles cold on bamboo with dipping sauce. Minimalist, meditative, perfect for solo "
                            "dinner. Beautiful traditional wooden building."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Kanda, between Akihabara and Ueno"}],
          "tips": [{"type": "tip", "text": ("For solo conveyor belt sushi, try Sushiro or Kura Sushi \u2014 "
                                            "order from a tablet, sushi arrives on a mini train. No interaction "
                                            "needed, no awkwardness. Brilliant.")}]
        }
      ],
      "mapPins": [
        {"lat": 35.7148, "lng": 139.7967, "label": "Senso-ji Temple", "num": 1, "cat": "attraction", "desc": "Tokyo\u2019s oldest temple \u2014 stunning at dawn"},
        {"lat": 35.7270, "lng": 139.7673, "label": "Yanaka Ginza", "num": 2, "cat": "attraction", "desc": "Retro street in old-Tokyo neighborhood"},
        {"lat": 35.7286, "lng": 139.7713, "label": "Yanaka Cemetery", "num": 3, "cat": "attraction", "desc": "Beautiful sakura-lined cemetery walk"},
        {"lat": 35.7146, "lng": 139.7732, "label": "Ueno Park", "num": 4, "cat": "attraction", "desc": "Tokyo\u2019s most famous cherry blossom hanami spot"},
        {"lat": 35.7103, "lng": 139.7748, "label": "Ameyoko Market", "num": 5, "cat": "food", "desc": "Open-air market \u2014 fresh seafood and street food"},
        {"lat": 35.7022, "lng": 139.7705, "label": "Akihabara", "num": 6, "cat": "attraction", "desc": "Electric Town \u2014 anime, games, otaku culture"},
        {"lat": 35.7104, "lng": 139.7913, "label": "Pelican Cafe", "num": 7, "cat": "food", "desc": "Legendary shokupan bakery since 1942"},
        {"lat": 35.6997, "lng": 139.7667, "label": "Kanda Yabu Soba", "num": 8, "cat": "food", "desc": "Historic soba restaurant since 1880"}
      ]
    },
    # ─── DAY 3 ───────────────────────────────────────────────────────────────
    {
      "num": 3, "date": "2026-03-22",
      "neighborhoods": "Harajuku \u00b7 Shibuya \u00b7 Shimokitazawa \u00b7 Nakameguro",
      "title": "West Side \u2014 Vintage, Vinyl and River Blossoms",
      "description": ("The creative, youthful side of Tokyo. Morning at Meiji Shrine and Harajuku, afternoon "
                      "exploring Shimokitazawa\u2019s vintage shops and curry joints, evening along the Meguro River "
                      "watching cherry blossoms glow under thousands of pink paper lanterns."),
      "timeBlocks": [
        {
          "label": "Morning",
          "activities": [
            {"title": "Meiji Shrine (Meiji Jingu)",
             "description": ("Walk through the towering torii gate into 170 acres of old-growth forest right in "
                             "central Tokyo. The approach through the forest feels like leaving the city entirely. "
                             "Write a wish on an ema wooden plaque and hang it at the shrine."),
             "details": ["\u26e9\ufe0f Free entry, opens at sunrise (~5:40am in March)",
                         "\U0001f332 Forest planted in 1920 with 100,000 donated trees",
                         "\U0001f4f8 The massive cypress torii gate on the main approach is the shot",
                         "\U0001f38b Ema plaque (\u00a5500) \u2014 write a wish, read others\u2019 too"]},
            {"title": "Harajuku and Takeshita Street",
             "description": ("Ancient forest to youth fashion capital in five minutes. Takeshita Street: crepe "
                             "shops, kawaii fashion, sensory overload. Cat Street (one block over): cooler, less "
                             "crowded, independent boutiques."),
             "details": ["\U0001f366 Giant cotton candy and crepes \u2014 Harajuku signatures",
                         "\U0001f457 Cat Street for independent Japanese fashion brands",
                         "\u2615 Percent Arabica Coffee on Cat Street \u2014 minimalist espresso perfection"]}
          ],
          "meals": [{"type": "\u2615 Breakfast", "name": "Bills Omotesando",
            "description": ("Australian cafe famous for its ricotta hotcakes \u2014 fluffy, pillowy pancakes "
                            "practically mandatory in Tokyo. Solo counter seats overlooking the kitchen."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Omotesando \u00b7 Opens 8:30am \u00b7 Solo-friendly counter"}]
        },
        {
          "label": "Afternoon",
          "activities": [{"title": "Shimokitazawa",
            "description": ("Tokyo\u2019s most beloved bohemian neighborhood \u2014 narrow streets packed with vintage "
                            "clothing shops, record stores, tiny curry restaurants, and live music venues. Feels "
                            "like a village inside a megacity. Perfect for aimless solo wandering."),
            "details": ["\U0001f455 Vintage shops: Flamingo, Stick Out, New York Joe Exchange",
                        "\U0001f35b Shimokitazawa is curry town \u2014 try Curry Spice Gelateria",
                        "\U0001f3b5 Afternoon live shows at Shelter or Club Que",
                        "\u2615 Bear Pond Espresso \u2014 legendary barista, incredible shots"]}],
          "meals": [{"type": "\U0001f35c Lunch", "name": "Curry Spice Gelateria",
            "description": ("A Shimokitazawa original \u2014 artisanal curry with rotating spice-infused gelatos "
                            "for dessert. Counter seats, solo-perfect."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Shimokitazawa \u00b7 Counter seating"}],
          "tips": [{"type": "tip", "text": ("Shimokitazawa is 3 stops from Shibuya on the Keio-Inokashira line. "
                                            "South side = vintage shops, north side = food. Just wander \u2014 "
                                            "best discoveries are unplanned.")}]
        },
        {
          "label": "Evening",
          "activities": [
            {"title": "Meguro River Cherry Blossoms at Night",
             "description": ("The 4km stretch of Meguro River from Nakameguro to Meguro is lined with 800+ "
                             "cherry trees. During bloom season, thousands of pink paper lanterns illuminate the "
                             "petals \u2014 their reflections ripple in the water below. Walk the entire length "
                             "slowly, stopping at pop-up bars and wine stands."),
             "details": ["\U0001f3ee Lantern illumination daily through early April, dusk to 9pm",
                         "\U0001f377 Pop-up wine and champagne stands along the riverbank",
                         "\U0001f4cd Start at Nakameguro Station and walk south toward Meguro",
                         "\U0001f4f8 Bridge near Nakameguro Station is the most photographed spot"]},
            {"title": "Shibuya Crossing",
             "description": ("The world\u2019s busiest intersection. Watch from the Starbucks 2F for the aerial "
                             "view, then cross with the crowd. Find the Hachiko statue at the north exit."),
             "details": ["\U0001f4f8 Best views: Starbucks 2F or Mag\u2019s Park rooftop (free)",
                         "\U0001f415 Hachiko statue \u2014 north exit, world\u2019s most loyal dog",
                         "\U0001f303 Most impressive after dark with all the screens lit"]}
          ],
          "meals": [{"type": "\U0001f377 Dinner", "name": "Afuri Ramen Nakameguro",
            "description": ("Light, refreshing yuzu shio (citrus salt) ramen \u2014 clear golden broth with a "
                            "yuzu punch, completely different from heavy tonkotsu. Counter-seat-only. Perfect "
                            "after a sakura walk."),
            "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Nakameguro \u00b7 Counter seats \u00b7 Ticket machine ordering"}]
        }
      ],
      "mapPins": [
        {"lat": 35.6764, "lng": 139.6993, "label": "Meiji Shrine", "num": 1, "cat": "attraction", "desc": "170 acres of forest \u2014 Japan\u2019s most visited shrine"},
        {"lat": 35.6702, "lng": 139.7026, "label": "Harajuku / Takeshita Street", "num": 2, "cat": "attraction", "desc": "Youth fashion capital \u2014 crepes, kawaii, Cat Street"},
        {"lat": 35.6610, "lng": 139.6682, "label": "Shimokitazawa", "num": 3, "cat": "attraction", "desc": "Bohemian neighborhood \u2014 vintage, vinyl, curry"},
        {"lat": 35.6441, "lng": 139.6985, "label": "Meguro River", "num": 4, "cat": "attraction", "desc": "800+ cherry trees lit by paper lanterns at night"},
        {"lat": 35.6595, "lng": 139.7005, "label": "Shibuya Crossing", "num": 5, "cat": "attraction", "desc": "World\u2019s busiest intersection"},
        {"lat": 35.6469, "lng": 139.6991, "label": "Afuri Ramen", "num": 6, "cat": "food", "desc": "Yuzu shio ramen \u2014 light, citrusy, counter seats"},
        {"lat": 35.6651, "lng": 139.6675, "label": "Bear Pond Espresso", "num": 7, "cat": "food", "desc": "Legendary Shimokitazawa espresso bar"},
        {"lat": 35.6712, "lng": 139.7125, "label": "Bills Omotesando", "num": 8, "cat": "food", "desc": "Famous ricotta hotcakes \u2014 solo-friendly counter"}
      ]
    },
    # ─── DAY 4 ───────────────────────────────────────────────────────────────
    {
      "num": 4, "date": "2026-03-23",
      "neighborhoods": "Chiyoda \u00b7 Imperial Palace \u00b7 Tsukiji \u00b7 Ginza",
      "title": "Imperial Sakura, Tsukiji and Ginza Farewell",
      "description": ("Your final day is Tokyo at its most refined. Morning at Chidorigafuchi \u2014 the Imperial "
                      "Palace moat becomes a tunnel of cherry blossoms, best seen from a rowboat. Fresh sushi at "
                      "Tsukiji Outer Market. Afternoon in elegant Ginza. Evening under the illuminated weeping "
                      "cherry at Rikugien Garden."),
      "timeBlocks": [
        {
          "label": "Morning",
          "activities": [
