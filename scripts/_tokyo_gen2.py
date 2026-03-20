#!/usr/bin/env python3
"""Part 2: Complete Day 4, budget table, practical info, and write final JS."""
import json, os, importlib.util, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load part 1 to get the partial data dict
spec = importlib.util.spec_from_file_location("gen1", os.path.join(SCRIPT_DIR, "_tokyo_gen.py"))
gen1 = importlib.util.module_from_spec(spec)

# We can't exec it as-is since it's incomplete (day 4 open). Instead, rebuild final dict here.
# Re-use all the data from part 1 but complete day 4.

# Shorthand emoji
E = lambda c: c  # passthrough; we define strings directly

day4 = {
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
        {"title": "Chidorigafuchi Cherry Blossoms and Boat Ride",
         "description": ("The most iconic sakura scene in all of Tokyo \u2014 260 cherry trees arch over the "
                         "Imperial Palace moat, forming a pink tunnel reflected in the green water below. "
                         "Rent a rowboat and drift under the canopy. Arrive early \u2014 boat queues build "
                         "fast during peak bloom."),
         "details": ["\U0001f6a3 Boat rental: \u00a5800/30min, opens 9:30am during sakura season",
                     "\U0001f338 Walkway along the moat equally beautiful without a boat",
                     "\U0001f4f8 Best light: morning sun illuminating blossoms against the moat",
                     "\U0001f3ef Kitanomaru Park adjacent \u2014 free, peaceful, cherry trees throughout"]},
        {"title": "Tsukiji Outer Market",
         "description": ("The inner wholesale market moved to Toyosu but the outer market remains a wonderland "
                         "of fresh sushi, tamagoyaki, and street food. Grab sushi at any counter \u2014 all "
                         "source from the same market. Fresh tuna at 7am hits different."),
         "details": ["\U0001f41f Tuna, uni, scallop \u2014 incredibly fresh from the overnight auction",
                     "\U0001f95a Tamagoyaki (sweet egg roll) on a stick \u2014 the Tsukiji street snack",
                     "\U0001f4cd 10 min from Chidorigafuchi by taxi or Hanzomon Line"]}
      ],
      "meals": [{"type": "\u2615 Breakfast", "name": "Tsukiji Outer Market Sushi Counter",
        "description": ("Pick any sushi counter in the outer market. Fresh nigiri for breakfast is a "
                        "quintessential Tokyo experience you will remember forever."),
        "meta": "\U0001f4b0 $$\u2013$$$ \u00b7 \U0001f4cd Tsukiji Outer Market \u00b7 From 5am \u00b7 Counter seats"}],
      "tips": [{"type": "tip", "text": ("March 23 is a Monday \u2014 Imperial Palace East Gardens close on "
                                        "Mondays and Fridays. Spend time at the Chidorigafuchi walkway and "
                                        "Kitanomaru Park (both open) instead.")}]
    },
    {
      "label": "Afternoon",
      "activities": [
        {"title": "Ginza Shopping District",
         "description": ("Tokyo\u2019s most elegant neighborhood \u2014 wide boulevards, department stores, art "
                         "galleries, and Japanese craft shops. Visit Ginza Six (rooftop garden with skyline views), "
                         "Itoya stationery (12 floors of Japanese paper and pens), and the architectural showcase "
                         "along Chuo-dori."),
         "details": ["\U0001f6cd\ufe0f Ginza Six \u2014 luxury dept store with a stunning rooftop garden",
                     "\u270f\ufe0f Itoya \u2014 12 floors of stationery heaven, perfect for gifts",
                     "\U0001f375 Higashiya Ginza \u2014 traditional Japanese sweets with matcha",
                     "\U0001f4cd Walkable from Tsukiji (15 min) or one subway stop"]},
        {"title": "Rikugien Garden Evening Illumination",
         "description": ("One of Tokyo\u2019s most beautiful Edo-period landscape gardens. During late March, the "
                         "famous weeping cherry tree is illuminated at night \u2014 a massive shidarezakura lit "
                         "dramatically against the dark garden. One of Tokyo\u2019s most poetic sakura views."),
         "details": ["\U0001f338 Illumination: Mar 20\u2013Apr 6, 2026 \u2014 17:00 to 21:00",
                     "\U0001f4a1 Arrive before sunset to see both daylight and illuminated views",
                     "\u00a5300 entry \u00b7 \U0001f4cd Komagome Station, 2 min walk",
                     "\U0001f375 Tea house inside serves matcha with seasonal wagashi"]}
      ],
      "meals": [{"type": "\U0001f35c Lunch", "name": "Ginza Kagari",
        "description": ("Michelin Bib Gourmand chicken paitan (white broth) ramen in Ginza. Creamy, golden chicken "
                        "broth unlike any ramen you\u2019ve had. 9 counter seats, quick-moving queue. A perfect "
                        "farewell bowl before your last afternoon in Tokyo."),
        "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Ginza \u00b7 9 counter seats \u00b7 Ticket machine"}]
    },
    {
      "label": "Evening",
      "activities": [{"title": "Farewell Walk \u2014 Yurakucho Under the Tracks",
        "description": ("Beneath the railway tracks near Yurakucho Station, dozens of tiny yakitori joints and "
                        "izakayas have served salarymen since the 1940s. Smoky, atmospheric, deeply local. "
                        "The perfect farewell dinner \u2014 counter seat, beer, skewers, and soak in Tokyo "
                        "one last time before you leave."),
        "details": ["\U0001f3ae Dozens of tiny joints under the elevated Yamanote Line tracks",
                    "\U0001f37a Salaryman atmosphere \u2014 real Tokyo, not tourist Tokyo",
                    "\U0001f4cd Yurakucho Station, 2 min walk from Ginza",
                    "\U0001f6cd\ufe0f Tokyo Station underground open until 9pm for last-minute omiyage"]}],
      "meals": [{"type": "\U0001f377 Dinner", "name": "Yakitori under the Tracks at Yurakucho",
        "description": ("Pick any stall under the Yamanote Line tracks. Smoky charcoal grill, counter seating, "
                        "cold beer, and the rumble of trains overhead \u2014 a quintessentially Tokyo farewell."),
        "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Yurakucho Station, under elevated tracks \u00b7 Cash mostly"}],
      "tips": [{"type": "tip", "text": ("Stock up on omiyage at Tokyo Station\u2019s underground shopping before "
                                        "heading to the airport \u2014 Tokyo Banana, shiroi koibito, regional "
                                        "wagashi. Open until 9pm.")}]
    }
  ],
  "mapPins": [
    {"lat": 35.6942, "lng": 139.7499, "label": "Chidorigafuchi", "num": 1, "cat": "attraction", "desc": "Imperial Palace moat \u2014 Tokyo\u2019s most iconic sakura tunnel"},
    {"lat": 35.6977, "lng": 139.7500, "label": "Kitanomaru Park", "num": 2, "cat": "attraction", "desc": "Peaceful park adjacent to Chidorigafuchi with cherry trees"},
    {"lat": 35.6654, "lng": 139.7707, "label": "Tsukiji Outer Market", "num": 3, "cat": "food", "desc": "Fresh sushi, tamagoyaki and street food from 5am"},
    {"lat": 35.6716, "lng": 139.7648, "label": "Ginza Six", "num": 4, "cat": "attraction", "desc": "Luxury department store with rooftop garden"},
    {"lat": 35.6709, "lng": 139.7636, "label": "Ginza Kagari", "num": 5, "cat": "food", "desc": "Michelin chicken paitan ramen \u2014 9 counter seats"},
    {"lat": 35.7329, "lng": 139.7465, "label": "Rikugien Garden", "num": 6, "cat": "attraction", "desc": "Illuminated weeping cherry tree at night \u2014 magical"},
    {"lat": 35.6753, "lng": 139.7614, "label": "Yurakucho Yakitori", "num": 7, "cat": "food", "desc": "Izakayas under the Yamanote Line tracks since the 1940s"},
    {"lat": 35.6812, "lng": 139.7671, "label": "Tokyo Station", "num": 8, "cat": "attraction", "desc": "Beautiful 1914 red-brick station \u2014 lit up magnificently at night"}
  ]
}

budget_table = [
  {"category": "Accommodation", "budget": "\u00a56,000\u201312,000/night", "midrange": "\u00a512,000\u201325,000/night", "luxury": "\u00a525,000+/night"},
  {"category": "Meals (per day)", "budget": "\u00a52,000\u20134,000/day", "midrange": "\u00a54,000\u20138,000/day", "luxury": "\u00a510,000+/day"},
  {"category": "Transport", "budget": "\u00a5500\u20131,000/day (Metro pass)", "midrange": "\u00a51,000\u20132,000/day", "luxury": "\u00a53,000+/day (taxis)"},
  {"category": "Activities", "budget": "\u00a51,000\u20133,000/day", "midrange": "\u00a53,000\u20135,000/day", "luxury": "\u00a55,000+/day"},
  {"category": "4-Day Total (solo)", "budget": "\u00a545,000\u201370,000 (~$300\u2013470)", "midrange": "\u00a570,000\u2013140,000 (~$470\u2013940)", "luxury": "\u00a5200,000+ (~$1,300+)"}
]

practical_info = [
  {"title": "\u2708\ufe0f Getting There", "items": [
    "Narita Airport (NRT) \u2014 1h by Narita Express to Shinjuku/Tokyo Station (~\u00a53,000)",
    "Haneda Airport (HND) \u2014 30 min by Keikyu Line to central Tokyo (cheaper and faster)",
    "Both airports have excellent English signage and IC card top-up machines at arrivals"]},
  {"title": "\U0001f3e8 Where to Stay", "items": [
    "Shinjuku \u2014 best nightlife access, massive transport hub, huge range of prices",
    "Asakusa \u2014 historic atmosphere, steps from Senso-ji, great capsule and budget hotels",
    "Shibuya \u2014 central, great for Day 3 Harajuku and Meguro access",
    "Shimokitazawa \u2014 for the vibe-seekers; charming, quieter, great local coffee"]},
  {"title": "\U0001f321\ufe0f Weather in Late March", "items": [
    "Temperatures: 10\u201317\u00b0C (50\u201363\u00b0F) \u2014 layers are essential",
    "Pack a light jacket \u2014 evenings along Meguro River can be chilly",
    "Occasional spring rain \u2014 cherry blossoms look magical with raindrops too",
    "March 20\u201323 is typically early bloom (first flowers opening)"]},
  {"title": "\U0001f4f1 Connectivity", "items": [
    "Buy a pocket Wi-Fi or data SIM at the airport (IIJmio, Mobal, or Sakura Mobile)",
    "eSIM options: Airalo Japan plan works well \u2014 set it up before you land",
    "Most cafes and convenience stores have free Wi-Fi",
    "Download Google Maps offline for Tokyo before you arrive"]}
]

# Now load part 1's D dict by reading and exec-ing it carefully
# We'll reconstruct from scratch since we have all days
# Load the partial data from gen1 (only days 1-3 are complete there)
exec(open(os.path.join(SCRIPT_DIR, "_tokyo_gen.py")).read().split("# ─── DAY 4 ───")[0] + "\ndays_123 = D['days']")

# Rebuild complete data
D["days"] = days_123 + [day4]
D["budgetTable"] = budget_table
D["practicalInfo"] = practical_info

# Write final JS
OUT = os.path.join(SCRIPT_DIR, "fulfill-order_1773933372257_6e4kmc.js")
js_content = f"""const fulfillOrder = require('../functions/fulfill-order');

const order = {{
  id: 'order_1773933372257_6e4kmc',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-20',
  endDate: '2026-03-23',
  groupSize: 1,
}};

const itineraryData = {json.dumps(D, indent=2, ensure_ascii=False)};

try {{
  const result = fulfillOrder(order, itineraryData);
  console.log('\\u2705 Fulfilled:', JSON.stringify(result, null, 2));
}} catch (err) {{
  console.error('\\u274c Error:', err.message);
  process.exit(1);
}}
"""

with open(OUT, "w") as f:
    f.write(js_content)

print(f"Written {len(js_content):,} bytes to {OUT}")
for day in D["days"]:
    pins = day.get("mapPins", [])
    blocks = day.get("timeBlocks", [])
    print(f"  Day {day['num']} ({day['date']}): {len(pins)} mapPins, {len(blocks)} timeBlocks")
