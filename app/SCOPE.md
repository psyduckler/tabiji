# Tabiji Travel Safety App — Data Layer Scope

_Scoped: Mar 30, 2026_

## Vision
Offline-first travel safety companion for older travelers (55-65+). Emergency contacts, healthcare guides, scam alerts, cultural basics — all cached on-device. Optional local AI chat against downloaded country packs.

## Data Layer Architecture

### Schema: `country-safety/{iso2}.json`

Each country gets a unified safety/travel JSON doc. This extends our existing API (`/api/v1/countries/{iso2}.json`) with new safety-specific fields.

```json
{
  "id": "country-safety:jp",
  "iso2": "JP",
  "name": "Japan",
  "lastUpdated": "2026-03-30T00:00:00Z",

  "emergency": {
    "police": "110",
    "ambulance": "119",
    "fire": "119",
    "universal": null,
    "notes": "Police and fire/ambulance use different numbers. English support is limited — ask hotel staff for help if possible."
  },

  "embassies": [
    {
      "name": "U.S. Embassy Tokyo",
      "city": "Tokyo",
      "address": "1-10-5 Akasaka, Minato-ku, Tokyo 107-8420",
      "phone": "+81-3-3224-5000",
      "emergencyPhone": "+81-3-3224-5000",
      "email": "TokyoACS@state.gov",
      "website": "https://jp.usembassy.gov/",
      "lat": 35.6664,
      "lng": 139.7375,
      "type": "embassy"
    },
    {
      "name": "U.S. Consulate General Osaka-Kobe",
      "city": "Osaka",
      "address": "2-11-5 Nishitenma, Kita-ku, Osaka 530-8543",
      "phone": "+81-6-6315-5900",
      "emergencyPhone": "+81-6-6315-5900",
      "email": null,
      "website": "https://jp.usembassy.gov/embassy-consulates/osaka-kobe/",
      "lat": 34.6966,
      "lng": 135.5023,
      "type": "consulate"
    }
  ],

  "travelAdvisory": {
    "source": "US State Department",
    "level": 1,
    "levelText": "Exercise Normal Precautions",
    "summary": "Japan is generally a safe destination...",
    "lastUpdated": "2026-01-15",
    "url": "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/japan-travel-advisory.html"
  },

  "travelAdvisoryUK": {
    "source": "UK FCDO",
    "summary": "...",
    "lastUpdated": "2026-03-01",
    "url": "https://www.gov.uk/foreign-travel-advice/japan"
  },

  "healthcare": {
    "systemType": "Universal (National Health Insurance)",
    "qualityRating": "excellent",
    "walkInAccess": true,
    "costForTourists": "Tourists pay full price without insurance. Hospital visits can be ¥5,000-30,000+ for minor issues.",
    "pharmacyAccess": "Pharmacies (yakkyoku) are common. Many OTC meds available. Prescription drugs require a local prescription.",
    "hospitalNotes": "High quality. Most staff speak limited English — bring Google Translate. Major hospitals in Tokyo/Osaka have international departments.",
    "vaccinationsRecommended": ["Routine", "Hepatitis A", "Hepatitis B"],
    "malariaRisk": false,
    "insuranceAdvice": "Travel insurance strongly recommended. Japanese hospitals may require upfront payment."
  },

  "medications": {
    "controlledSubstances": [
      {
        "drug": "Adderall / amphetamines",
        "status": "banned",
        "note": "Strictly prohibited. Carrying even with a prescription can result in arrest and imprisonment."
      },
      {
        "drug": "Pseudoephedrine (Sudafed)",
        "status": "banned",
        "note": "Prohibited. Use alternative cold medicines."
      },
      {
        "drug": "Codeine",
        "status": "restricted",
        "note": "Allowed in small quantities with documentation. Bring prescription and doctor's letter."
      }
    ],
    "generalAdvice": "Carry a copy of prescriptions translated into English. Some common Western medications are not available. Japan's stimulant control laws are extremely strict.",
    "yakkan-shoumei": "Required import certificate (Yakkan Shoumei) for many medications. Apply to MHLW before travel."
  },

  "scams": [
    {
      "name": "Kabukicho bar scam",
      "city": "Tokyo",
      "description": "Friendly strangers invite you to a 'local bar' — drinks arrive with a bill of ¥100,000+. Staff block the exit.",
      "avoidance": "Never follow strangers to bars. Only enter establishments you chose yourself."
    },
    {
      "name": "Fake monks",
      "city": "Nationwide",
      "description": "People in monk robes hand you a 'blessed' bracelet then demand payment.",
      "avoidance": "Politely decline any unsolicited gifts. Real monks don't solicit on streets."
    }
  ],

  "connectivity": {
    "simOptions": "Pocket WiFi rental at airports (¥500-1000/day). eSIM via Ubigi, Airalo, or Holafly. Physical SIM from BIC Camera or airport.",
    "wifiAvailability": "Free WiFi at convenience stores, train stations, and many restaurants. Quality varies.",
    "bestOption": "Pocket WiFi or eSIM. Japan's eSIM coverage is excellent on major carriers."
  },

  "cultural": {
    "tipping": "Do not tip. It can be considered rude.",
    "dressCode": "Remove shoes when entering homes, temples, and some restaurants. Cover shoulders at shrines.",
    "greetings": "Bow instead of handshake. Deeper bow = more respect.",
    "taboos": ["Talking on phone on trains", "Eating while walking", "Pointing with fingers (use open hand)", "Blowing nose in public"],
    "haggling": "Not practiced. Prices are fixed everywhere."
  },

  "phrases": [
    { "english": "Hello", "local": "Konnichiwa", "phonetic": "kohn-nee-chee-wah" },
    { "english": "Thank you", "local": "Arigatou gozaimasu", "phonetic": "ah-ree-gah-toh go-zah-ee-mahs" },
    { "english": "Excuse me", "local": "Sumimasen", "phonetic": "soo-mee-mah-sen" },
    { "english": "Help!", "local": "Tasukete!", "phonetic": "tah-soo-keh-teh" },
    { "english": "Hospital", "local": "Byouin", "phonetic": "byoh-een" },
    { "english": "Police", "local": "Keisatsu", "phonetic": "keh-saht-soo" },
    { "english": "I don't understand", "local": "Wakarimasen", "phonetic": "wah-kah-ree-mah-sen" },
    { "english": "Where is...?", "local": "...wa doko desu ka?", "phonetic": "wah doh-koh des-kah" },
    { "english": "How much?", "local": "Ikura desu ka?", "phonetic": "ee-koo-rah des-kah" },
    { "english": "Yes / No", "local": "Hai / Iie", "phonetic": "hai / ee-eh" }
  ],

  "safety": {
    "overallRisk": "very-low",
    "violentCrime": "very-low",
    "pettyCrime": "low",
    "naturalDisasters": ["earthquakes", "typhoons", "tsunamis"],
    "lgbtSafety": "Generally safe but limited legal protections. PDA is uncommon for all couples.",
    "soloFemaleSafety": "Very safe. Some train cars have women-only sections during rush hour.",
    "notes": "Japan is one of the safest countries in the world for tourists. Main risks are natural disasters and language barriers in emergencies."
  },

  "practical": {
    "tapWater": true,
    "drivingSide": "left",
    "plugType": ["A", "B"],
    "voltage": "100V / 50-60Hz",
    "dialCode": "+81",
    "visaFreeCountries": "US, UK, EU, Australia, Canada — 90 days visa-free",
    "timeZone": "UTC+09:00",
    "bestTimeToVisit": "March-May (spring), October-November (autumn)"
  }
}
```

## Data Sources (all free / already available)

| Data Field | Primary Source | Backup Source | Update Freq |
|---|---|---|---|
| Emergency numbers | Wikipedia / RestCountries | Manual curation | Yearly |
| Embassy/consulate locations | State Dept (travel.state.gov scrape) | STEP program data | Monthly |
| Travel advisories (US) | State Dept RSS feed | Already have via XML | Weekly |
| Travel advisories (UK) | UK FCDO API (gov.uk) | JSON API, tested ✅ | Weekly |
| Healthcare system overview | LLM-generated + manual review | WHO country profiles | Quarterly |
| Medication restrictions | LLM-generated + country drug authority sites | INCB data | Quarterly |
| Scam database | **Our existing Reel content** | Reddit research, web scrape | Ongoing |
| Connectivity/SIM options | LLM-generated + Airalo/Holafly data | Web scrape | Quarterly |
| Cultural norms | LLM-generated + existing country-facts | Wikitravel/Wikivoyage | Yearly |
| Phrases | LLM-generated | Google Translate API | Yearly |
| Safety ratings | State Dept + FCDO + OSAC | GPI (Global Peace Index) | Yearly |
| Practical info | **Already in our API** (country-facts.json) | RestCountries | Yearly |

## What We Already Have (in tabiji API)

- ✅ 250 country profiles (iso2, capital, population, currencies, languages, timezones, driving side, dial code, flag)
- ✅ 202 country-facts (tap water, tipping, visa notes — ~60% placeholder, needs enrichment)
- ✅ 1,440+ destination profiles
- ✅ 6,093 place records with ratings/reviews
- ✅ Travel advisory RSS feed (State Dept) — just need to parse + cache
- ✅ UK FCDO API — tested, returns structured JSON with entry requirements, safety, health
- ✅ Scam content from our Reel production pipeline

## What We Need to Build

### Phase 1: Core Safety Data (Week 1-2)
1. **Emergency numbers database** — 250 countries, police/ambulance/fire/universal
2. **US Embassy/Consulate scraper** — parse travel.state.gov for all embassy locations, phones, addresses, geocode them
3. **Travel advisory parser** — State Dept RSS → JSON, run weekly via cron
4. **FCDO advisory parser** — UK gov.uk API → JSON, run weekly via cron
5. **Merge into country-safety/{iso2}.json** — extend existing country profiles

### Phase 2: Enrichment (Week 2-3)
6. **Healthcare guides** — LLM-generated per country with manual review. System type, tourist costs, pharmacy access, vaccination recs
7. **Medication restrictions** — Top 20 commonly-traveled countries first, expand from there. Focus on controlled substances (stimulants, opioids, CBD)
8. **Scam database** — Extract from our existing Reel scripts/research + Reddit research corpus
9. **Cultural norms + phrases** — LLM batch generation, 10 phrases per language

### Phase 3: App-Ready (Week 3-4)
10. **Offline bundle builder** — Script that packages country-safety JSONs into downloadable country packs (compressed)
11. **API endpoints** — Add `/api/v1/safety/{iso2}.json` to existing API build
12. **Search index** — Extend existing search-index.json with safety keywords
13. **Update pipeline** — Cron to refresh advisories weekly, rebuild + deploy

## Integration with Existing API

The safety data becomes a new dimension of the existing API:

```
tabiji.ai/api/v1/
├── countries/         # existing (250 country profiles)
├── countries.json     # existing (country list)
├── destinations/      # existing (6,905 destinations)
├── safety/            # NEW
│   ├── index.json     # safety data catalog
│   ├── jp.json        # per-country safety bundle
│   ├── th.json
│   └── ...
├── advisories/        # NEW
│   ├── us.json        # State Dept advisories (all countries)
│   └── uk.json        # FCDO advisories (all countries)
└── ...
```

For the app, a "country pack" download = `countries/{iso2}.json` + `safety/{iso2}.json` + related destination data. Estimated ~50-100KB per country compressed.

## On-Device AI Chat

For the local model angle:
- **Model:** Gemma 2B or Phi-3 Mini (3.8B), quantized to 4-bit (~1.5-2GB on device)
- **Context:** Downloaded country pack loaded as context
- **Use case:** "Is it safe to walk in Shinjuku at night?" → answers from cached safety + cultural data
- **Framework:** Apple Core ML (iOS) or llama.cpp with Metal acceleration
- **This is Phase 2 of the app itself** — data layer comes first

## Build Order

```
1. build-emergency-numbers.py    → safety/emergency by country
2. build-embassy-data.py         → safety/embassies by country  
3. build-travel-advisories.py    → advisories/us.json + uk.json
4. build-healthcare-guides.py    → safety/healthcare by country
5. build-medication-rules.py     → safety/medications by country
6. build-scam-database.py        → safety/scams by country (from our content)
7. build-cultural-guides.py      → safety/cultural + phrases by country
8. merge-safety-profiles.py      → safety/{iso2}.json (unified)
9. update build-api.py           → include safety/ in API build
```

## Priority Countries (build these first, validate schema)
Japan, Thailand, Mexico, Italy, France, Spain, Portugal, Greece, UK, Germany, 
Costa Rica, Colombia, Peru, Vietnam, Indonesia (Bali), Morocco, Turkey, 
South Korea, Australia, New Zealand

These cover ~80% of our audience's travel destinations based on our GA4 data.

## Decisions Made
- [x] **PWA-first, graduate to native iOS when ready** (Bernard, Mar 30). Apple Developer account secured for future native wrap (Capacitor/TWA).
- [ ] Do we scope to US embassies only, or include other Five Eyes (UK, Canada, Australia)?
- [ ] Healthcare cost estimates — how granular? (per-procedure? or just "expensive/moderate/cheap"?)
- [ ] Scam database — structured per-city or per-country?
- [ ] Should country packs include offline map tile regions? (big storage implications)

## PWA Architecture
- Host on Cloudflare Pages (existing infra, zero cost)
- Service worker caches downloaded country packs for offline use
- URL: `tabiji.ai/app/` or `app.tabiji.ai`
- Stack: Vanilla JS or lightweight framework (Preact/Svelte — TBD)
- Offline storage: IndexedDB for country packs, Cache API for app shell
- Future: Wrap with Capacitor for App Store listing
