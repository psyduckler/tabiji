#!/usr/bin/env python3
"""Part 2: Day 4 afternoon/evening + budget table + practical info, then assemble final JS."""
import json, os

# Read part 1 data
import importlib.util
spec = importlib.util.spec_from_file_location("p1", os.path.join(os.path.dirname(__file__), "_gen_tokyo.py"))
p1 = importlib.util.module_from_spec(spec)

# Instead of importing, let's just build the complete day4 and assemble

day4_afternoon_evening = {
    "label": "Afternoon",
    "activities": [
        {"title": "Ginza Shopping District", "description": "Tokyo's most elegant neighborhood \u2014 wide boulevards, department stores, art galleries. Visit Ginza Six (rooftop garden), Itoya stationery (12 floors of Japanese paper and pens), and the architectural parade along Chuo-dori.", "details": ["\U0001f6cd\ufe0f Ginza Six \u2014 luxury dept store with rooftop garden", "\u270f\ufe0f Itoya \u2014 12 floors of stationery heaven", "\U0001f375 Higashiya Ginza \u2014 traditional sweets with matcha", "\U0001f4cd Walkable from Tsukiji (15 min)"]},
        {"title": "Rikugien Garden (Evening Illumination)", "description": "One of Tokyo's most beautiful Edo-period landscape gardens. During late March, the famous weeping cherry tree is illuminated at night \u2014 a massive shidarezakura lit dramatically against the dark garden.", "details": ["\U0001f338 Illumination: Mar 20 to Apr 6 \u2014 17:00 to 21:00", "\U0001f4a1 Weeping cherry at entrance is the star", "\u00a5300 entry \u00b7 \U0001f4cd Komagome Station, 2 min walk", "\U0001f375 Tea house inside serves matcha with wagashi"]}
    ],
    "meals": [{"type": "\U0001f35c Lunch", "name": "Ginza Kagari", "description": "Michelin-recommended chicken paitan (white broth) ramen in Ginza. Creamy, golden chicken broth unlike any ramen you've had. 9 counter seats, quick queue. A perfect farewell bowl.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Ginza \u00b7 9 counter seats \u00b7 Ticket machine"}]
}

day4_evening = {
    "label": "Evening",
    "activities": [{"title": "Farewell Walk \u2014 Tokyo Station at Night", "description": "End your trip at magnificent Tokyo Station \u2014 the beautifully restored 1914 red-brick building lit up at night, reflected in the glass of surrounding skyscrapers. Walk through the illuminated Marunouchi side for a final Tokyo moment.", "details": ["\U0001f3db\ufe0f The red-brick Marunouchi facade is stunning after dark", "\U0001f4f8 Reflections in the KITTE building glass", "\U0001f4cd Tokyo Station is a perfect final stop \u2014 trains to Narita/Haneda leave from here"]}],
    "meals": [{"type": "\U0001f377 Dinner", "name": "Yakitori Alley under the Tracks (Yurakucho)", "description": "Beneath the railway tracks near Yurakucho Station, dozens of tiny yakitori joints and izakayas have been serving salarymen since the 1940s. Smoky, atmospheric, and deeply local. The perfect farewell dinner \u2014 sit at a counter, order beer and skewers, and soak in Tokyo one last time.", "meta": "\U0001f4b0 $$ \u00b7 \U0001f4cd Yurakucho, under the train tracks \u00b7 Counter seats \u00b7 Cash"}],
    "tips": [{"type": "tip", "text": "If flying out tomorrow, stock up on omiyage (souvenirs) at Tokyo Station's underground shopping \u2014 Tokyo Banana, shiroi koibito, and regional wagashi are all here. Open until 9pm."}]
}

print(json.dumps({"afternoon": day4_afternoon_evening, "evening": day4_evening}, ensure_ascii=False))
