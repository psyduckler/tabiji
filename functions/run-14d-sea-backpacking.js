const path = require('path');
const fulfillOrder = require('./fulfill-order');
const days1to7 = require('./data-14d-sea-days1-7.json');
const days8to14 = require('./data-14d-sea-days8-14.json');

const order = {
  id: "sample-14d-sea-backpacking",
  email: "internal@tabiji.ai",
  destination: "Southeast Asia",
  start_date: "2026-04-01",
  end_date: "2026-04-14",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "The classic backpacker loop — Bangkok, Chiang Mai, Vientiane, Luang Prabang, or south through Malaysia. Budget tips and hostel recs.",
  amount: "0.00",
  timestamp: "2026-03-08T23:41:00.000Z",
  status: "pending",
  notes: "Internal sample itinerary — not a customer order"
};

const itineraryData = {
  destination: "Southeast Asia (Thailand, Laos & Cambodia)",
  countryEmoji: "🇹🇭🇱🇦🇰🇭",
  title: "14-Day Southeast Asia Backpacking Route",
  subtitle: "Bangkok → Chiang Mai → Mekong Slow Boat → Luang Prabang → Vientiane → Siem Reap → Bangkok",
  description: "The classic banana pancake trail — but smarter. This 14-day loop hits three countries, mixing Bangkok's sensory chaos with Chiang Mai's temple-studded mountain vibes, the legendary two-day Mekong slow boat into Laos, UNESCO-listed Luang Prabang's dawn monk processions, Vientiane's sleepy Mekong-side charm, and Angkor Wat's mind-bending temple complexes. Designed for $30-50/day backpackers who want the highlights without the burnout. Every border crossing, bus route, and budget hack has been vetted by thousands of r/backpacking and r/solotravel veterans.",
  duration: "14 days / 13 nights",
  dates: "Flexible — works year-round, best Nov–Mar",
  budget: "$30–50/day including accommodation, food, transport, and activities",
  pace: "Active but not exhausting — travel days balanced with chill days",
  bestFor: "First-time backpackers, solo travelers, budget couples, gap-year adventurers",
  highlights: [
    "Bangkok's Grand Palace, Wat Pho & Chinatown street food — the best introduction to Asia",
    "Chiang Mai's 300+ temples, night bazaars & legendary cooking classes",
    "The 2-day Mekong slow boat through untouched jungle from Huay Xai to Luang Prabang",
    "Luang Prabang's dawn alms giving ceremony — 600 monks in saffron at sunrise",
    "Kuang Si Falls — turquoise cascading pools in the jungle outside Luang Prabang",
    "Vientiane — Southeast Asia's most chill capital, Mekong sunsets & Patuxay monument",
    "Angkor Wat sunrise — the single most iconic sight in Southeast Asia",
    "Siem Reap's Pub Street & $0.50 draft beer, night markets, and Angkor Thom",
    "Three countries, three currencies, one backpack — the quintessential SE Asia loop",
    "Street food that costs less than a coffee back home but tastes better than most restaurants"
  ],
  essentials: [
    { title: "✈️ Flights & Route Logic", text: "Fly into Bangkok (BKK or DMK). The loop goes: Bangkok → Chiang Mai (domestic flight or overnight train) → Chiang Rai → border crossing to Huay Xai, Laos → slow boat → Luang Prabang → Vientiane → fly to Siem Reap → fly back to Bangkok. Total internal flights: 2-3 ($30-80 each on AirAsia, Thai Lion, or Cambodia Angkor Air). The overnight train Bangkok→Chiang Mai is iconic and saves a hotel night (~$15-40 for a sleeper)." },
    { title: "💵 Daily Budget Breakdown", text: "Thailand: $30-40/day easy. Hostel dorm $5-10, street food meals $1-3, BTS/local transport $1-3, temple entry $3-15. Laos: even cheaper at $20-35/day. Hostel dorm $4-8, meals $2-5, slow boat $25-35. Cambodia: $25-40/day. Hostels $4-8, meals $2-5, Angkor Pass (1-day) $37, (3-day) $62. Total trip: $500-700 excluding international flights." },
    { title: "🛂 Visas", text: "Thailand: Most nationalities get 30-day visa-free on arrival. Laos: Visa on arrival at all major border crossings — $30-42 USD cash depending on nationality, bring a passport photo. Cambodia: e-Visa ($36, apply online 3+ days before) or Visa on Arrival ($30 + $5 unofficial fee). Carry passport photos and US dollars cash for all visa fees." },
    { title: "🌡️ Weather & When to Go", text: "Nov-Feb is peak season: dry, cool (75-85°F), and busiest. Mar-May is hot season (90-100°F) with fewer tourists and lower prices. Jun-Oct is rainy season — short afternoon downpours, lush greenery, emptiest temples, cheapest everything. All seasons are viable. April includes Songkran (Thai New Year water fight, April 13-15) — chaos but unforgettable." },
    { title: "🎒 Packing Essentials", text: "One 40-55L backpack max. Quick-dry clothes (2-3 changes), temple-appropriate outfit (covers knees + shoulders), rain jacket or poncho, headlamp, padlock for hostel lockers, flip-flops, solid walking sandals, reusable water bottle (refill stations everywhere), sunscreen, mosquito repellent (DEET works), and a microfiber towel. Leave the jeans at home." },
    { title: "📱 SIM Cards & Connectivity", text: "Buy local SIMs at each country's airport or border crossing. Thailand: AIS Tourist SIM ~$5-10 (30 days, 15-30GB). Laos: Unitel SIM ~$2-5 at the border or LP shops. Cambodia: Smart SIM ~$3-5 at Siem Reap airport. WiFi is widespread in hostels and cafes. Consider an eSIM (Airalo or Holafly) for multi-country coverage if your phone supports it." },
    { title: "💊 Health & Safety", text: "No mandatory vaccinations, but recommended: Hepatitis A/B, Typhoid, Tetanus. Malaria risk is low in cities and tourist areas — not needed for this route. Dengue exists — use repellent. Carry basic first-aid: Imodium, electrolyte packets, antihistamines. Tap water is NOT safe — drink bottled or filtered only. Travel insurance is non-negotiable ($30-50/trip on SafetyWing or World Nomads)." },
    { title: "💱 Money Tips", text: "ATMs everywhere in cities. Best cards: Charles Schwab debit (no foreign ATM fees) or Wise debit card. Thai Baht, Lao Kip, and Cambodian Riel/USD — Cambodia runs on US dollars for everything over $1. Withdraw in local currency to avoid terrible exchange rates. Bangkok SuperRich exchange offices have the best rates. Keep small bills — change is always scarce." }
  ],
  days: [...days1to7, ...days8to14]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
