#!/usr/bin/env python3
"""Part 2: Finish data and write final JS file."""
import json, os, importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load part 1
spec = importlib.util.spec_from_file_location("p1", os.path.join(SCRIPT_DIR, "_write_tokyo.py"))
p1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p1)
data = p1.data

# Finish Day 4
day4 = data["days"][3]
day4["timeBlocks"][0]["activities"].append(
    {"title": "Tsukiji Outer Market Sushi",
     "description": ("The inner wholesale market moved to Toyosu but the outer market remains a wonderland "
                     "of fresh sushi, tamagoyaki, and street food. Grab sushi at any counter \u2014 "
                     "all source from the same market. Fresh tuna at 7am hits different."),
     "details": ["\U0001f41f Tuna, uni, scallop \u2014 incredibly fresh from the overnight auction",
                 "\U0001f95a Tamagoyaki (sweet egg) on a stick \u2014 the Tsukiji street snack",
                 "\U0001f4cd 10 min from Chidorigafuchi by taxi or Hanzomon Line"]}
)
day4["timeBlocks"][0]["meals"] = [
    {"type": "\u2615 Breakfast", "name": "Tsukiji Outer Market Sushi Counter",
     "description": ("Pick any sushi counter in the outer market. Fresh nigiri for breakfast is a "
                     "quintessential Tokyo experience you will remember forever."),
     "meta": "\U0001f4b0 $$\u2013$$$ \u00b7 \U0001f4cd Tsukiji Outer Market \u00b7 From 5am \u00b7 Counter seats"}
]
day4["timeBlocks"][0]["tips"] = [
    {"type": "tip", "text": ("March 23 is a Monday \u2014 Imperial Palace East Gardens close on Mon & Fri. "
                             "Spend extra time at the Chidorigafuchi walkway and Kitanomaru Park instead.")}
]

# Day 4 Afternoon
day4["timeBlocks"].append({
    "label": "Afternoon",
    "activities": [
        {"title": "Ginza Shopping District",
         "description": ("Tokyo's most elegant neighborhood \u2014 wide boulevards, department stores, art galleries. "
                         "Visit Ginza Six (rooftop garden with views), Itoya stationery (12 floors of Japanese paper "
                         "and pens), and the architectural showcase along Chuo-dori."),
         "details": ["\U0001f6cd\ufe0f Ginza Six \u2014 luxury department store with a stunning rooftop garden",
                     "\u270f\ufe0f Itoya \u2014 12 floors of stationery heaven, perfect for gifts",
                     "\U0001f375 Higashiya Ginza \u2014 traditional Japanese sweets with matcha",
                     "\U0001f4cd Walkable from Tsukiji (15 min) or one subway stop"]},
        {"title": "Rikugien Garden Evening Illumination",
         "description": ("One of Tokyo's most beautiful Edo-period landscape gardens. During late March, the famous "
                         "weeping cherry tree is illuminated at night \u2014 a massive shidarezakura lit dramatically "
                         "against the dark garden. One of Tokyo's most poetic sakura views."),
         "details": ["\U0001f338 Illumination: Mar 20\u2013Apr 6, 2026 \u2014 17:00 to 21:00",
                     "\U0001f4a1 Arrive before sunset to see both daylight and illuminated views",
                     "\u00a5300 entry \u00b7 \U0001f4cd Komagome Station, 2 min walk",
                     "\U0001f375 Tea house inside serves matcha with seasonal wagashi"]}
    ],
    "meals": [{"type": "\U0001f35c Lunch", "name": "Ginza Kagari",
               "description": ("Michelin Bib Gourmand chicken paitan (white broth) ramen in Ginza. Creamy, golden "
                               "chicken broth unlike any ramen you've had. 9 counter seats, quick-moving queue. "
                               "A perfect farewell bowl before heading out."),
               "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Ginza \u00b7 9 counter seats \u00b7 Ticket machine"}]
})

# Day 4 Evening
day4["timeBlocks"].append({
    "label": "Evening",
    "activities": [{"title": "Farewell Walk \u2014 Yurakucho Under the Tracks",
                    "description": ("Beneath the railway tracks near Yurakucho Station, dozens of tiny yakitori joints "
                                    "and izakayas have served salarymen since the 1940s. Smoky, atmospheric, deeply local. "
                                    "The perfect farewell dinner \u2014 counter seat, beer, skewers, soak in Tokyo one last time."),
                    "details": ["\U0001f3ae Dozens of tiny joints under the elevated Yamanote Line tracks",
                                "\U0001f37a Salaryman atmosphere \u2014 real Tokyo, not tourist Tokyo",
                                "\U0001f4cd Yurakucho Station, 2 min walk from Ginza",
                                "\U0001f6cd\ufe0f Tokyo Station underground shops open until 9pm for last-minute omiyage"]}],
    "meals": [{"type": "\U0001f377 Dinner", "name": "Yakitori under the Tracks, Yurakucho",
               "description": ("Pick any stall under the Yamanote Line tracks at Yurakucho. Smoky charcoal grill, "
                               "counter seating, cold beer, and the rumble of trains overhead \u2014 a quintessentially "
                               "Tokyo farewell."),
               "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Yurakucho Station, under the elevated tracks \u00b7 Cash mostly"}],
    "tips": [{"type": "tip", "text": ("Stock up on omiyage (souvenirs/gifts) at Tokyo Station's underground shopping "
                                      "before heading to the airport \u2014 Tokyo Banana, shiroi koibito, regional wagashi. "
                                      "Open until 9pm.")}]
})

# Day 4 mapPins
day4["mapPins"] = [
    {"lat": 35.6942, "lng": 139.7499, "label": "Chidorigafuchi", "num": 1, "cat": "attraction", "desc": "Imperial Palace moat \u2014 Tokyo's most iconic sakura tunnel"},
    {"lat": 35.6977, "lng": 139.7500, "label": "Kitanomaru Park", "num": 2, "cat": "attraction", "desc": "Peaceful park adjacent to Chidorigafuchi"},
    {"lat": 35.6654, "lng": 139.7707, "label": "Tsukiji Outer Market", "num": 3, "cat": "food", "desc": "Fresh sushi, tamagoyaki and street food from 5am"},
    {"lat": 35.6716, "lng": 139.7648, "label": "Ginza Six", "num": 4, "cat": "attraction", "desc": "Luxury department store with rooftop garden"},
    {"lat": 35.6709, "lng": 139.7636, "label": "Ginza Kagari", "num": 5, "cat": "food", "desc": "Michelin chicken paitan ramen \u2014 9 counter seats"},
    {"lat": 35.7329, "lng": 139.7465, "label": "Rikugien Garden", "num": 6, "cat": "attraction", "desc": "Illuminated weeping cherry tree at night \u2014 magical"},
    {"lat": 35.6753, "lng": 139.7614, "label": "Yurakucho Yakitori", "num": 7, "cat": "food", "desc": "Izakayas under the Yamanote Line tracks since the 1940s"},
    {"lat": 35.6812, "lng": 139.7671, "label": "Tokyo Station", "num": 8, "cat": "attraction", "desc": "Beautiful 1914 red-brick station \u2014 lit up magnificently at night"}
]

# Budget table
data["budgetTable"] = [
    {"category": "Accommodation", "budget": "\u00a56,000\u201312,000/night", "midrange": "\u00a512,000\u201325,000/night", "luxury": "\u00a525,000+/night"},
    {"category": "Meals (per day)", "budget": "\u00a52,000\u20134,000/day", "midrange": "\u00a54,000\u20138,000/day", "luxury": "\u00a510,000+/day"},
    {"category": "Transport", "budget": "\u00a5500\u20131,000/day (Metro)", "midrange": "\u00a51,000\u20132,000/day", "luxury": "\u00a53,000+/day (taxis)"},
    {"category": "Activities", "budget": "\u00a51,000\u20133,000/day", "midrange": "\u00a53,000\u20135,000/day", "luxury": "\u00a55,000+/day"},
    {"category": "4-Day Total (solo)", "budget": "\u00a545,000\u201370,000 (~$300\u2013470)", "midrange": "\u00a570,000\u2013140,000 (~$470\u2013940)", "luxury": "\u00a5200,000+ (~$1,300+)"}
]

# Practical info
data["practicalInfo"] = [
    {"title": "\u2708\ufe0f Getting There",
     "items": ["Narita Airport (NRT) \u2014 1h by Narita Express train to Shinjuku/Tokyo Station (roughly \u00a53,000)",
               "Haneda Airport (HND) \u2014 30 min by Keikyu Line to central Tokyo (much cheaper and faster)",
               "Both airports have excellent English signage and IC card top-up machines at arrivals"]},
    {"title": "\U0001f3e8 Where to Stay",
     "items": ["Shinjuku \u2014 best nightlife access, massive transport hub, huge range of prices",
               "Asakusa \u2014 historic atmosphere, steps from Senso-ji, good capsule/budget hotels",
               "Shibuya \u2014 central, great for Day 3 Harajuku/Meguro access",
               "Shimokitazawa \u2014 for the vibe-seekers; charming, quieter, great local coffee"]},
    {"title": "\U0001f321\ufe0f Weather in Late March",
     "items": ["Temperatures: 10\u201317\u00b0C (50\u201363\u00b0F) \u2014 layers are essential",
               "Pack a light jacket \u2014 evenings along the Meguro River can be chilly",
               "Occasional spring rain \u2014 cherry blossoms look magical with rain drops too",
               "March 20\u201323 is typically early bloom (first flowers opening)"]},
    {"title": "\U0001f4f1 Connectivity",
     "items": ["Buy a pocket Wi-Fi or data SIM at the airport (IIJmio, Mobal, or Sakura Mobile)",
               "eSIM options: Airalo Japan plan works well, set up before you land",
               "Most cafes and convenience stores have free Wi-Fi",
               "Download Google Maps offline for Tokyo before you arrive"]}
]

# Now write the JS file
OUT = os.path.join(SCRIPT_DIR, "fulfill-order_1773933372257_6e4kmc.js")
js = f"""const fulfillOrder = require('../functions/fulfill-order');

const order = {{
  id: 'order_1773933372257_6e4kmc',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-20',
  endDate: '2026-03-23',
  groupSize: 1,
}};

const itineraryData = {json.dumps(data, indent=2, ensure_ascii=False)};

try {{
  const result = fulfillOrder(order, itineraryData);
  console.log('\\u2705 Fulfilled:', JSON.stringify(result, null, 2));
}} catch (err) {{
  console.error('\\u274c Error:', err.message);
  process.exit(1);
}}
"""

with open(OUT, 'w') as f:
    f.write(js)

print(f"Written {len(js):,} bytes ({js.count(chr(10))} lines) to {OUT}")

# Validate: check all 4 days have mapPins
for day in data["days"]:
    pins = day.get("mapPins", [])
    print(f"  Day {day['num']}: {len(pins)} mapPins, {len(day['timeBlocks'])} timeBlocks")
