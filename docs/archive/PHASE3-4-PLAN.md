# Tabiji API Phase 3–4: Offline Packs, Intelligence Graph & Local Model Layer

_Author: Kapi | Date: 2026-03-30_
_Status: Proposal — awaiting review_

---

## Current State (API v1.4.0)

```
/api/v1/
├── index.json              # API root (version, stats, endpoint list)
├── catalog.json            # 6,054 entity catalog (picks places)
├── search-index.json       # 7,923 search docs
├── countries.json          # 250 countries
├── countries/{iso2}.json   # country detail (incl. healthInfo on some)
├── destinations.json       # 6,905 destinations
├── destinations/{slug}.json
├── picks.json              # 527 curated guides → 1,202 detail files
├── picks/{slug}.json
├── itineraries.json        # 374 itineraries
├── itineraries/{slug}.json
├── compare.json            # 117 comparisons
└── compare/{slug}.json
```

Site content (not yet in API):
- `alerts/` — 224 country travel advisory HTML pages
- `scams/` — 55 city scam guide HTML pages
- `health/` — 51 country healthcare HTML pages
- `app/data/emergency-numbers.json` — 192 countries
- `app/data/advisories-us.json` — 208 US State Dept entries
- `app/data/advisories-uk.json` — 226 UK FCDO entries
- `app/data/safety/{iso2}.json` — 2 complete profiles (JP, TH)

---

## Proposed Endpoint Map

### Sprint 1 — Safety & Alerts API

```
NEW endpoints:

/api/v1/safety.json                   # safety collection index
/api/v1/safety/{iso2}.json            # unified safety profile per country
/api/v1/alerts.json                   # travel advisory collection index
/api/v1/alerts/{iso2}.json            # advisory detail per country (US + UK combined)
```

### Sprint 2 — Scams & Relationship Endpoints

```
NEW endpoints:

/api/v1/scams.json                    # scam collection index (all cities)
/api/v1/scams/{slug}.json             # scam detail per city
/api/v1/countries/{iso2}/scams.json   # scams aggregated by country
/api/v1/countries/{iso2}/safety.json  # safety profile (alias → safety/{iso2}.json)
/api/v1/countries/{iso2}/alerts.json  # advisory (alias → alerts/{iso2}.json)

EXTENDED:
/api/v1/destinations/{slug}.json      # add: safetyRef, alertsRef, scamsRef
/api/v1/countries/{iso2}.json         # add: safetyRef, alertsRef, scamSlugs
```

### Sprint 3 — Filtering & Recommendations

```
NEW endpoints:

/api/v1/filter.json                   # filterable index with facets
/api/v1/facets.json                   # available filter dimensions + value counts
/api/v1/recommend.json                # heuristic recommendation engine
```

### Sprint 4 — Offline Packs, Manifest & Knowledge Chunks

```
NEW endpoints:

/api/v1/manifest.json                 # collection inventory with checksums
/api/v1/packs.json                    # pack catalog
/api/v1/packs/{pack}.json             # downloadable region/theme packs
/api/v1/knowledge/chunks.json         # AI-ready text chunks (full)
/api/v1/knowledge/chunks/{pack}.json  # chunks scoped to a pack
```

---

## Example JSON Schemas

### 1. `safety/{iso2}.json` — Unified Country Safety Profile

_Already defined in `app/SCOPE.md`. Two complete examples exist at `app/data/safety/jp.json` and `th.json`._

```json
{
  "id": "safety:jp",
  "iso2": "JP",
  "name": "Japan",
  "lastUpdated": "2026-03-30T00:00:00Z",
  "version": 1,

  "emergency": {
    "police": "110",
    "ambulance": "119",
    "fire": "119",
    "universal": null,
    "notes": "..."
  },

  "embassies": [
    {
      "name": "U.S. Embassy Tokyo",
      "city": "Tokyo",
      "address": "...",
      "phone": "+81-3-3224-5000",
      "emergencyPhone": "+81-3-3224-5000",
      "email": "TokyoACS@state.gov",
      "website": "https://jp.usembassy.gov/",
      "lat": 35.6664,
      "lng": 139.7375,
      "type": "embassy"
    }
  ],

  "travelAdvisory": {
    "source": "US State Department",
    "level": 1,
    "levelText": "Exercise Normal Precautions",
    "summary": "...",
    "lastUpdated": "2026-01-15",
    "url": "..."
  },

  "travelAdvisoryUK": {
    "source": "UK FCDO",
    "summary": "...",
    "lastUpdated": "2026-03-01",
    "url": "..."
  },

  "healthcare": {
    "systemType": "Universal (National Health Insurance)",
    "qualityRating": "excellent",
    "walkInAccess": true,
    "costForTourists": "...",
    "pharmacyAccess": "...",
    "hospitalNotes": "...",
    "vaccinationsRecommended": ["Routine", "Hepatitis A", "Hepatitis B"],
    "malariaRisk": false,
    "insuranceAdvice": "..."
  },

  "medications": {
    "controlledSubstances": [
      {
        "drug": "Adderall / amphetamines",
        "status": "banned",
        "note": "..."
      }
    ],
    "generalAdvice": "..."
  },

  "scams": [
    {
      "name": "Kabukicho bar scam",
      "city": "Tokyo",
      "description": "...",
      "avoidance": "..."
    }
  ],

  "connectivity": {
    "simOptions": "...",
    "wifiAvailability": "...",
    "bestOption": "..."
  },

  "cultural": {
    "tipping": "...",
    "dressCode": "...",
    "greetings": "...",
    "taboos": ["..."],
    "haggling": "..."
  },

  "phrases": [
    { "english": "Hello", "local": "Konnichiwa", "phonetic": "kohn-nee-chee-wah" }
  ],

  "safety": {
    "overallRisk": "very-low",
    "violentCrime": "very-low",
    "pettyCrime": "low",
    "naturalDisasters": ["earthquakes", "typhoons"],
    "lgbtSafety": "...",
    "soloFemaleSafety": "...",
    "notes": "..."
  },

  "practical": {
    "tapWater": true,
    "drivingSide": "left",
    "plugType": ["A", "B"],
    "voltage": "100V / 50-60Hz",
    "dialCode": "+81",
    "visaFreeCountries": "...",
    "timeZone": "UTC+09:00",
    "bestTimeToVisit": "..."
  }
}
```

### 2. `alerts/{iso2}.json` — Travel Advisory Detail

```json
{
  "id": "alerts:jp",
  "iso2": "JP",
  "name": "Japan",
  "lastUpdated": "2026-03-30T00:00:00Z",

  "us": {
    "level": 1,
    "levelText": "Exercise Normal Precautions",
    "summary": "Japan is generally a safe destination...",
    "dateIssued": "2026-01-15",
    "url": "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/japan-travel-advisory.html",
    "regions": []
  },

  "uk": {
    "summary": "Most visits to Japan are trouble-free...",
    "dateIssued": "2026-03-01",
    "url": "https://www.gov.uk/foreign-travel-advice/japan",
    "entryRequirements": "...",
    "healthNotes": "...",
    "safetyWarnings": []
  },

  "combinedLevel": "low",
  "combinedSummary": "Both US and UK governments rate Japan as low-risk. Exercise normal precautions."
}
```

### 3. `alerts.json` — Advisory Collection Index

```json
{
  "count": 208,
  "lastUpdated": "2026-03-30T00:00:00Z",
  "sources": ["US State Department", "UK FCDO"],
  "items": [
    {
      "iso2": "JP",
      "name": "Japan",
      "usLevel": 1,
      "usLevelText": "Exercise Normal Precautions",
      "ukSummary": "Most visits are trouble-free",
      "combinedLevel": "low",
      "url": "/api/v1/alerts/jp.json",
      "lastUpdated": "2026-03-30T00:00:00Z"
    }
  ]
}
```

### 4. `safety.json` — Safety Collection Index

```json
{
  "count": 20,
  "lastUpdated": "2026-03-30T00:00:00Z",
  "priorityCountries": ["JP", "TH", "MX", "IT", "FR", "ES", "PT", "GR", "GB", "DE",
                         "CR", "CO", "PE", "VN", "ID", "MA", "TR", "KR", "AU", "NZ"],
  "items": [
    {
      "iso2": "JP",
      "name": "Japan",
      "overallRisk": "very-low",
      "advisoryLevel": 1,
      "emergencyPolice": "110",
      "emergencyAmbulance": "119",
      "embassyCount": 2,
      "scamCount": 2,
      "url": "/api/v1/safety/jp.json",
      "lastUpdated": "2026-03-30T00:00:00Z"
    }
  ]
}
```

### 5. `scams/{slug}.json` — City Scam Detail

```json
{
  "id": "scam:tokyo",
  "slug": "tokyo",
  "city": "Tokyo",
  "country": "Japan",
  "countryCode": "JP",
  "lastUpdated": "2026-03-30T00:00:00Z",

  "scamCount": 8,
  "scams": [
    {
      "id": "scam:tokyo:kabukicho-bar",
      "name": "Kabukicho Bar Scam",
      "category": "overcharging",
      "severity": "high",
      "frequency": "common",
      "description": "Friendly strangers invite you to a 'local bar' — drinks arrive with a bill of ¥100,000+.",
      "avoidance": "Never follow strangers to bars. Only enter establishments you chose yourself.",
      "location": "Kabukicho, Shinjuku",
      "tags": ["nightlife", "bars", "overcharging"],
      "sources": ["reddit:r/JapanTravel", "tabiji:scams/tokyo"]
    }
  ],

  "sourceUrl": "https://tabiji.ai/scams/tokyo/",
  "relatedAlerts": "/api/v1/alerts/jp.json",
  "relatedSafety": "/api/v1/safety/jp.json"
}
```

### 6. `scams.json` — Scam Collection Index

```json
{
  "count": 55,
  "totalScams": 342,
  "lastUpdated": "2026-03-30T00:00:00Z",
  "items": [
    {
      "slug": "tokyo",
      "city": "Tokyo",
      "country": "Japan",
      "countryCode": "JP",
      "scamCount": 8,
      "topCategories": ["overcharging", "tourist-traps"],
      "url": "/api/v1/scams/tokyo.json"
    }
  ]
}
```

### 7. `filter.json` — Filterable Destination Index

```json
{
  "count": 6905,
  "lastUpdated": "2026-03-30T00:00:00Z",
  "facetsUrl": "/api/v1/facets.json",
  "items": [
    {
      "slug": "tokyo",
      "name": "Tokyo",
      "country": "Japan",
      "countryCode": "JP",
      "continent": "Asia",
      "region": "Eastern Asia",

      "budget": { "min": 80, "max": 200, "currency": "USD", "tier": "moderate" },
      "season": { "best": ["Mar", "Apr", "May", "Oct", "Nov"], "avoid": ["Jul", "Aug"] },
      "vibes": ["urban", "cultural", "foodie", "nightlife"],
      "travelStyles": ["solo", "couples", "family"],

      "safety": {
        "overallRisk": "very-low",
        "advisoryLevel": 1,
        "soloFemaleSafety": "very-safe",
        "lgbtSafety": "safe"
      },

      "practical": {
        "visaFreeUS": true,
        "englishFriendly": "moderate",
        "tapWaterSafe": true,
        "vegetarianFriendly": "moderate"
      },

      "climate": {
        "type": "humid-subtropical",
        "avgTempC": { "jan": 6, "apr": 15, "jul": 27, "oct": 18 }
      },

      "scores": {
        "editorial": 0.92,
        "popularity": 0.95,
        "value": 0.70
      }
    }
  ]
}
```

### 8. `facets.json` — Filter Dimensions

```json
{
  "lastUpdated": "2026-03-30T00:00:00Z",
  "facets": {
    "continent": {
      "values": [
        { "value": "Asia", "count": 1842 },
        { "value": "Europe", "count": 2156 },
        { "value": "Africa", "count": 634 }
      ]
    },
    "budget.tier": {
      "values": [
        { "value": "budget", "count": 1923 },
        { "value": "moderate", "count": 3012 },
        { "value": "luxury", "count": 1970 }
      ]
    },
    "safety.overallRisk": {
      "values": [
        { "value": "very-low", "count": 1200 },
        { "value": "low", "count": 2800 },
        { "value": "moderate", "count": 2100 },
        { "value": "high", "count": 700 },
        { "value": "extreme", "count": 105 }
      ]
    },
    "vibes": {
      "values": [
        { "value": "beach", "count": 1456 },
        { "value": "cultural", "count": 3201 },
        { "value": "foodie", "count": 2810 },
        { "value": "nightlife", "count": 1678 },
        { "value": "nature", "count": 2543 },
        { "value": "adventure", "count": 1890 }
      ]
    },
    "safety.soloFemaleSafety": {
      "values": [
        { "value": "very-safe", "count": 980 },
        { "value": "safe", "count": 2300 },
        { "value": "moderate", "count": 2800 },
        { "value": "caution", "count": 700 },
        { "value": "avoid-alone", "count": 125 }
      ]
    },
    "practical.vegetarianFriendly": {
      "values": [
        { "value": "excellent", "count": 1200 },
        { "value": "good", "count": 2100 },
        { "value": "moderate", "count": 2400 },
        { "value": "limited", "count": 1205 }
      ]
    },
    "season.best": {
      "values": [
        { "value": "Jan", "count": 2340 },
        { "value": "Feb", "count": 2420 },
        { "value": "Mar", "count": 3100 },
        { "value": "Apr", "count": 3450 },
        { "value": "May", "count": 3200 }
      ]
    }
  }
}
```

### 9. `recommend.json` — Heuristic Recommendations

_Static recommendations pre-computed for common query patterns. Client sends query params; matches against pre-built recommendation sets._

```json
{
  "lastUpdated": "2026-03-30T00:00:00Z",
  "presets": [
    {
      "id": "solo-female-safe-budget",
      "query": "safe, budget-friendly solo female travel",
      "filters": {
        "safety.soloFemaleSafety": ["very-safe", "safe"],
        "budget.tier": ["budget"],
        "travelStyles": ["solo"]
      },
      "results": [
        {
          "slug": "lisbon",
          "name": "Lisbon",
          "score": 0.94,
          "reasons": [
            "Rated 'very-safe' for solo female travelers",
            "Budget tier: $45-80/day",
            "Excellent public transit, walkable center"
          ]
        }
      ],
      "resultCount": 25
    },
    {
      "id": "warm-cheap-vegetarian",
      "query": "warm, cheap, safe, vegetarian-friendly",
      "filters": {
        "climate.type": ["tropical", "subtropical"],
        "budget.tier": ["budget"],
        "safety.overallRisk": ["very-low", "low"],
        "practical.vegetarianFriendly": ["excellent", "good"]
      },
      "results": [],
      "resultCount": 18
    }
  ]
}
```

### 10. `manifest.json` — Collection Inventory

```json
{
  "version": "1.5.0",
  "generatedAt": "2026-03-30T00:00:00Z",
  "collections": {
    "destinations": {
      "count": 6905,
      "indexUrl": "/api/v1/destinations.json",
      "detailPattern": "/api/v1/destinations/{slug}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:abc123...",
      "sizeBytes": 2450000
    },
    "countries": {
      "count": 250,
      "indexUrl": "/api/v1/countries.json",
      "detailPattern": "/api/v1/countries/{iso2}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:def456...",
      "sizeBytes": 890000
    },
    "safety": {
      "count": 20,
      "indexUrl": "/api/v1/safety.json",
      "detailPattern": "/api/v1/safety/{iso2}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:ghi789...",
      "sizeBytes": 340000
    },
    "alerts": {
      "count": 208,
      "indexUrl": "/api/v1/alerts.json",
      "detailPattern": "/api/v1/alerts/{iso2}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:jkl012..."
    },
    "scams": {
      "count": 55,
      "indexUrl": "/api/v1/scams.json",
      "detailPattern": "/api/v1/scams/{slug}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:mno345..."
    },
    "picks": {
      "count": 527,
      "indexUrl": "/api/v1/picks.json",
      "detailPattern": "/api/v1/picks/{slug}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:pqr678..."
    },
    "itineraries": {
      "count": 374,
      "indexUrl": "/api/v1/itineraries.json",
      "detailPattern": "/api/v1/itineraries/{slug}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:stu901..."
    },
    "compare": {
      "count": 117,
      "indexUrl": "/api/v1/compare.json",
      "detailPattern": "/api/v1/compare/{slug}.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "checksum": "sha256:vwx234..."
    }
  },
  "totalSizeBytes": 48500000,
  "packsUrl": "/api/v1/packs.json"
}
```

### 11. `packs/{pack}.json` — Downloadable Region/Theme Pack

```json
{
  "id": "pack:japan",
  "name": "Japan Travel Pack",
  "description": "Complete offline guide: 12 destinations, safety data, scam alerts, healthcare, and 45 curated picks for Japan.",
  "version": 3,
  "generatedAt": "2026-03-30T00:00:00Z",
  "sizeBytes": 95000,
  "checksum": "sha256:abc...",

  "coverage": {
    "countries": ["JP"],
    "destinationCount": 12,
    "picksCount": 45,
    "itineraryCount": 8,
    "scamCities": ["tokyo", "osaka", "kyoto"]
  },

  "data": {
    "countries": [
      { /* full countries/jp.json content */ }
    ],
    "safety": [
      { /* full safety/jp.json content */ }
    ],
    "alerts": [
      { /* full alerts/jp.json content */ }
    ],
    "destinations": [
      { /* tokyo destination */ },
      { /* kyoto destination */ }
    ],
    "scams": [
      { /* scams/tokyo.json content */ },
      { /* scams/osaka.json content */ }
    ],
    "picks": [
      { /* relevant picks */ }
    ],
    "itineraries": [
      { /* relevant itineraries */ }
    ]
  },

  "metadata": {
    "packType": "country",
    "tags": ["asia", "safe", "cultural", "foodie"],
    "primaryLanguage": "Japanese",
    "emergencyNumber": "110"
  }
}
```

### 12. `packs.json` — Pack Catalog

```json
{
  "count": 30,
  "lastUpdated": "2026-03-30T00:00:00Z",
  "packs": [
    {
      "id": "pack:japan",
      "name": "Japan",
      "packType": "country",
      "countries": ["JP"],
      "destinationCount": 12,
      "sizeBytes": 95000,
      "url": "/api/v1/packs/japan.json"
    },
    {
      "id": "pack:se-asia",
      "name": "Southeast Asia",
      "packType": "region",
      "countries": ["TH", "VN", "ID", "MY", "PH", "KH", "LA", "MM", "SG"],
      "destinationCount": 85,
      "sizeBytes": 420000,
      "url": "/api/v1/packs/se-asia.json"
    },
    {
      "id": "pack:europe-budget",
      "name": "Europe on a Budget",
      "packType": "theme",
      "countries": ["PT", "ES", "GR", "HR", "HU", "CZ", "PL", "RO", "BG"],
      "destinationCount": 62,
      "sizeBytes": 310000,
      "url": "/api/v1/packs/europe-budget.json"
    },
    {
      "id": "pack:solo-female-safe",
      "name": "Safest Solo Female Destinations",
      "packType": "theme",
      "countries": ["JP", "IS", "NZ", "PT", "SI", "NO", "DK", "IE", "AT", "CH"],
      "destinationCount": 40,
      "sizeBytes": 280000,
      "url": "/api/v1/packs/solo-female-safe.json"
    }
  ]
}
```

### 13. `knowledge/chunks.json` — AI-Ready Text Chunks

```json
{
  "version": "1.0.0",
  "generatedAt": "2026-03-30T00:00:00Z",
  "chunkCount": 15420,
  "chunks": [
    {
      "id": "chunk:safety:jp:medication:adderall",
      "type": "medicationRestriction",
      "entityId": "safety:jp",
      "text": "Adderall and all amphetamines are strictly banned in Japan. Carrying even with a valid prescription can result in arrest and imprisonment. Japan's stimulant control laws are among the strictest in the world.",
      "tags": ["japan", "medication", "controlled-substance", "banned", "adderall", "amphetamine"],
      "sourceUrl": "https://tabiji.ai/api/v1/safety/jp.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "confidence": 0.95,
      "provenance": "official-sources + editorial"
    },
    {
      "id": "chunk:scam:tokyo:kabukicho-bar",
      "type": "scamPattern",
      "entityId": "scam:tokyo:kabukicho-bar",
      "text": "The Kabukicho bar scam in Tokyo involves friendly strangers inviting tourists to a 'local bar' where drinks arrive with a bill of ¥100,000+. Staff may block the exit. Avoid following strangers to bars — only enter establishments you chose yourself.",
      "tags": ["tokyo", "japan", "scam", "nightlife", "overcharging"],
      "sourceUrl": "https://tabiji.ai/scams/tokyo/",
      "updatedAt": "2026-03-30T00:00:00Z",
      "confidence": 0.90,
      "provenance": "reddit-research + editorial"
    },
    {
      "id": "chunk:destination:tokyo:summary",
      "type": "destinationPracticalSummary",
      "entityId": "destination:tokyo",
      "text": "Tokyo, Japan. Budget: $80-200/day (moderate). Best months: March-May, October-November. Tap water is safe. Tipping is not practiced and can be considered rude. Visa-free for US, UK, EU, Australia, Canada (90 days). Drives on the left. Plugs: Type A/B, 100V.",
      "tags": ["tokyo", "japan", "asia", "urban", "cultural", "foodie"],
      "sourceUrl": "https://tabiji.ai/destinations/tokyo/",
      "updatedAt": "2026-03-30T00:00:00Z",
      "confidence": 0.92,
      "provenance": "editorial + api-data"
    },
    {
      "id": "chunk:advisory:jp:snapshot",
      "type": "advisorySnapshot",
      "entityId": "alerts:jp",
      "text": "Japan travel advisory: US State Department Level 1 (Exercise Normal Precautions). UK FCDO rates Japan as generally trouble-free. No regional warnings. Last verified March 2026.",
      "tags": ["japan", "advisory", "safe", "level-1"],
      "sourceUrl": "https://tabiji.ai/alerts/japan/",
      "updatedAt": "2026-03-30T00:00:00Z",
      "confidence": 0.98,
      "provenance": "official-sources"
    },
    {
      "id": "chunk:country:jp:safety-summary",
      "type": "countrySafetySummary",
      "entityId": "safety:jp",
      "text": "Japan is one of the safest countries for tourists. Overall risk: very low. Violent crime: very low. Petty crime: low. Natural disaster risks: earthquakes, typhoons, tsunamis. Very safe for solo female travelers — some train cars have women-only sections during rush hour. LGBTQ+ travelers are generally safe but legal protections are limited.",
      "tags": ["japan", "safety", "very-safe", "solo-female", "natural-disasters"],
      "sourceUrl": "https://tabiji.ai/api/v1/safety/jp.json",
      "updatedAt": "2026-03-30T00:00:00Z",
      "confidence": 0.95,
      "provenance": "official-sources + editorial"
    }
  ]
}
```

### 14. Domain Objects — Type Reference

Every chunk's `type` field maps to a domain object category. These are the answerable units for local model reasoning:

| Domain Object | type value | Source | Example Query |
|---|---|---|---|
| Country Safety Summary | `countrySafetySummary` | `safety/{iso2}.json` | "Is Japan safe for solo female travelers?" |
| Destination Practical Summary | `destinationPracticalSummary` | `destinations/{slug}.json` | "What's the budget for Tokyo?" |
| Medication Restriction | `medicationRestriction` | `safety/{iso2}.json` → medications | "Can I bring ADHD meds to Japan?" |
| Travel Risk Signal | `travelRiskSignal` | `alerts/{iso2}.json` | "Any warnings for Thailand right now?" |
| Scam Pattern | `scamPattern` | `scams/{slug}.json` | "What scams should I watch for in Bangkok?" |
| Advisory Snapshot | `advisorySnapshot` | `alerts/{iso2}.json` | "What's the current US advisory for Mexico?" |
| Healthcare Guide | `healthcareGuide` | `safety/{iso2}.json` → healthcare | "How does healthcare work for tourists in Italy?" |
| Cultural Norm | `culturalNorm` | `safety/{iso2}.json` → cultural | "What's the tipping custom in France?" |
| Emergency Contact | `emergencyContact` | `safety/{iso2}.json` → emergency | "What's the emergency number in Germany?" |
| Connectivity Guide | `connectivityGuide` | `safety/{iso2}.json` → connectivity | "Best SIM option for Vietnam?" |
| Phrase / Language | `phraseGuide` | `safety/{iso2}.json` → phrases | "How do you say 'help' in Thai?" |
| Itinerary Summary | `itinerarySummary` | `itineraries/{slug}.json` | "5-day Tokyo itinerary" |
| Comparison Verdict | `comparisonVerdict` | `compare/{slug}.json` | "Thailand vs Bali for first solo trip" |
| Picks Recommendation | `picksRecommendation` | `picks/{slug}.json` | "Best ramen in Tokyo" |

---

## Implementation Plan — Tied to Repo Files

### Sprint 1: Safety & Alerts API _(scripts 4–8 + API wiring)_

**Goal:** Ship `safety/`, `alerts/` endpoints with 20 priority countries fully populated.

| # | Task | Script/File | Input | Output | Notes |
|---|---|---|---|---|---|
| 1a | Build embassy scraper | `app/scripts/build-embassy-data.py` _(new)_ | travel.state.gov | `app/data/embassies.json` | Scrape US embassy locations, geocode with Google Maps API |
| 1b | Build healthcare guides | `app/scripts/build-healthcare-guides.py` _(new)_ | LLM batch (Gemini Flash) | `app/data/healthcare/` | 20 priority countries first, schema per SCOPE.md |
| 1c | Build medication rules | `app/scripts/build-medication-rules.py` _(new)_ | LLM batch + manual review | `app/data/medications/` | Focus: stimulants, opioids, CBD, pseudoephedrine |
| 1d | Build scam database | `app/scripts/build-scam-database.py` _(new)_ | `scams/*.html` (55 cities) | `app/data/scams/` | Extract structured data from existing HTML content |
| 1e | Build cultural guides | `app/scripts/build-cultural-guides.py` _(new)_ | LLM batch | `app/data/cultural/` | Norms + 10 phrases per language |
| 1f | Merge safety profiles | `app/scripts/merge-safety-profiles.py` _(new)_ | All of the above + existing emergency/advisory data | `app/data/safety/{iso2}.json` | Unify into SCOPE.md schema |
| 1g | Build safety API endpoints | Extend `api/build-api.py` | `app/data/safety/`, `app/data/advisories-*.json` | `api/v1/safety.json`, `api/v1/safety/{iso2}.json`, `api/v1/alerts.json`, `api/v1/alerts/{iso2}.json` | Add new collections to build pipeline |
| 1h | Update OpenAPI spec | `api/openapi.json` | New endpoint definitions | Updated spec | Add safety + alerts paths and schemas |
| 1i | Update API index | `api/build-api.py` → index.json generation | New stats | Updated `api/v1/index.json` | Bump version to 1.5.0 |

**Deliverable:** `safety.json` + 20× `safety/{iso2}.json` + `alerts.json` + 208× `alerts/{iso2}.json` live in API.

### Sprint 2: Scams API & Cross-References

| # | Task | Script/File | Input | Output |
|---|---|---|---|---|
| 2a | Build scams API | Extend `api/build-api.py` | `app/data/scams/` | `api/v1/scams.json`, `api/v1/scams/{slug}.json` |
| 2b | Country→scam aggregation | Extend `api/build-api.py` | scam city→country mapping | `api/v1/countries/{iso2}/scams.json` |
| 2c | Country relationship aliases | Extend `api/build-api.py` | safety + alerts data | `api/v1/countries/{iso2}/safety.json`, `api/v1/countries/{iso2}/alerts.json` |
| 2d | Destination cross-refs | Extend `api/build-api.py` | destination→country mapping | Add `safetyRef`, `alertsRef`, `scamsRef` to destination detail files |
| 2e | Update OpenAPI + docs | `api/openapi.json` | New endpoints | Updated spec |

**Deliverable:** Scams API live, all collections cross-referenced.

### Sprint 3: Filter, Facets & Recommendations

| # | Task | Script/File | Input | Output |
|---|---|---|---|---|
| 3a | Build filter index | `scripts/build-filter-index.py` _(new)_ | destinations + safety + country data | `api/v1/filter.json` |
| 3b | Build facets | `scripts/build-facets.py` _(new)_ | filter.json | `api/v1/facets.json` |
| 3c | Build recommendations | `scripts/build-recommendations.py` _(new)_ | filter.json + editorial signals | `api/v1/recommend.json` |
| 3d | Update OpenAPI | `api/openapi.json` | New endpoints | Updated spec |

**Deliverable:** Filterable destination search with faceted navigation + pre-computed recommendation sets.

### Sprint 4: Manifest, Packs & Knowledge Chunks

| # | Task | Script/File | Input | Output |
|---|---|---|---|---|
| 4a | Build manifest | `scripts/build-manifest.py` _(new)_ | All `api/v1/` collections | `api/v1/manifest.json` |
| 4b | Build pack definitions | `scripts/build-packs.py` _(new)_ | Pack config + all API data | `api/v1/packs.json`, `api/v1/packs/{pack}.json` |
| 4c | Build knowledge chunks | `scripts/build-knowledge-chunks.py` _(new)_ | All API data | `api/v1/knowledge/chunks.json` |
| 4d | Per-pack chunk export | `scripts/build-knowledge-chunks.py` | Pack definitions | `api/v1/knowledge/chunks/{pack}.json` |
| 4e | Lightweight search manifests | `scripts/build-pack-search.py` _(new)_ | Pack data | Compact search indexes per pack |
| 4f | Update OpenAPI + docs | `api/openapi.json` | New endpoints | Updated spec |

**Deliverable:** Offline-ready packaging. PWA can fetch manifest → download changed packs → cache in IndexedDB → search locally.

---

## File Tree Summary (New Files)

```
tabiji/
├── app/
│   ├── scripts/
│   │   ├── build-emergency-numbers.py    # ✅ exists
│   │   ├── build-travel-advisories.py    # ✅ exists
│   │   ├── build-embassy-data.py         # 🆕 Sprint 1
│   │   ├── build-healthcare-guides.py    # 🆕 Sprint 1
│   │   ├── build-medication-rules.py     # 🆕 Sprint 1
│   │   ├── build-scam-database.py        # 🆕 Sprint 1
│   │   ├── build-cultural-guides.py      # 🆕 Sprint 1
│   │   └── merge-safety-profiles.py      # 🆕 Sprint 1
│   └── data/
│       ├── emergency-numbers.json        # ✅ exists (192 countries)
│       ├── advisories-us.json            # ✅ exists (208 entries)
│       ├── advisories-uk.json            # ✅ exists (226 entries)
│       ├── embassies.json                # 🆕 Sprint 1
│       ├── healthcare/                   # 🆕 Sprint 1
│       ├── medications/                  # 🆕 Sprint 1
│       ├── scams/                        # 🆕 Sprint 1
│       ├── cultural/                     # 🆕 Sprint 1
│       └── safety/
│           ├── jp.json                   # ✅ exists
│           ├── th.json                   # ✅ exists
│           └── {iso2}.json              # 🆕 Sprint 1 (18 more)
├── scripts/
│   ├── build-filter-index.py             # 🆕 Sprint 3
│   ├── build-facets.py                   # 🆕 Sprint 3
│   ├── build-recommendations.py          # 🆕 Sprint 3
│   ├── build-manifest.py                 # 🆕 Sprint 4
│   ├── build-packs.py                    # 🆕 Sprint 4
│   ├── build-knowledge-chunks.py         # 🆕 Sprint 4
│   └── build-pack-search.py              # 🆕 Sprint 4
├── api/
│   ├── build-api.py                      # ✏️ extend in Sprint 1-2
│   ├── openapi.json                      # ✏️ extend each sprint
│   └── v1/
│       ├── safety.json                   # 🆕 Sprint 1
│       ├── safety/{iso2}.json            # 🆕 Sprint 1
│       ├── alerts.json                   # 🆕 Sprint 1
│       ├── alerts/{iso2}.json            # 🆕 Sprint 1
│       ├── scams.json                    # 🆕 Sprint 2
│       ├── scams/{slug}.json             # 🆕 Sprint 2
│       ├── countries/{iso2}/scams.json   # 🆕 Sprint 2
│       ├── countries/{iso2}/safety.json  # 🆕 Sprint 2
│       ├── countries/{iso2}/alerts.json  # 🆕 Sprint 2
│       ├── filter.json                   # 🆕 Sprint 3
│       ├── facets.json                   # 🆕 Sprint 3
│       ├── recommend.json                # 🆕 Sprint 3
│       ├── manifest.json                 # 🆕 Sprint 4
│       ├── packs.json                    # 🆕 Sprint 4
│       ├── packs/{pack}.json             # 🆕 Sprint 4
│       ├── knowledge/chunks.json         # 🆕 Sprint 4
│       └── knowledge/chunks/{pack}.json  # 🆕 Sprint 4
└── docs/
    └── PHASE3-4-PLAN.md                  # 📄 this file
```

---

## Design Principles (Phase 4 Forward-Compatibility)

Every record in the API already exposes or will expose:

1. **Freshness** — `lastUpdated` / `updatedAt` on every entity
2. **Provenance** — `provenance` field: `"official-sources"`, `"reddit-research"`, `"editorial"`, `"llm-generated"`
3. **Confidence** — `confidence` float (0-1) on catalog entities and knowledge chunks
4. **Relation IDs** — `relatedPicks`, `relatedItineraries`, `safetyRef`, `alertsRef`, `scamsRef`
5. **Normalized enums** — risk levels (`very-low`→`extreme`), budget tiers (`budget`/`moderate`/`luxury`), safety ratings

This means a local model consuming `knowledge/chunks.json` can:
- Filter by confidence threshold
- Cite sources via `sourceUrl`
- Check freshness before answering
- Follow relations to get deeper context
- Use enums for structured comparison queries

---

## What Stays Static vs Dynamic

| Static JSON (keep on CDN) | Dynamic Later (if needed) |
|---|---|
| destinations, countries, safety, scams, alerts | `recommend` (personalized ranking) |
| itineraries, compare, picks | advanced search with scoring |
| packs, manifests, chunks | conversational planning |
| filter, facets | local model orchestration |

The static-JSON-on-CDN architecture is a feature, not a limitation. Don't lose it unless there's a compelling reason.