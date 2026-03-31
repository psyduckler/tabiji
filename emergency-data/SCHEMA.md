# Emergency Data Schema v1

Offline-first emergency data for tabiji.ai destinations.
One JSON file per country: `{ISO2}.json` (matches `health-data/` convention).

Target: ~2-5KB per country, all 55+ countries, total bundle <300KB gzipped.

## Schema: `{ISO2}.json`

```jsonc
{
  // ── Identity (matches health-data) ──
  "iso2": "JP",
  "countryName": "Japan",
  "countrySlug": "japan",
  "flag": "🇯🇵",
  "lastUpdated": "2026-03-31",
  "schemaVersion": "1.0",

  // ── 1. Offline Emergency Phrases ──
  "emergencyPhrases": {
    "language": "Japanese",            // primary local language
    "languageCode": "ja",              // ISO 639-1
    "script": "mixed",                 // "latin" | "cyrillic" | "arabic" | "cjk" | "mixed"
    "phrases": [
      {
        "id": "help",
        "english": "Help!",
        "local": "助けて！",
        "romanized": "Tasukete!",       // phonetic for non-native readers
        "phonetic": "tah-sue-keh-teh",  // simplified pronunciation guide
        "category": "critical",         // "critical" | "medical" | "police" | "communication"
        "notes": null                   // optional context
      },
      {
        "id": "call_ambulance",
        "english": "Call an ambulance!",
        "local": "救急車を呼んでください！",
        "romanized": "Kyūkyūsha wo yonde kudasai!",
        "phonetic": "kyoo-kyoo-sha oh yon-deh koo-dah-sai",
        "category": "medical",
        "notes": "Dial 119 for ambulance"
      },
      {
        "id": "call_police",
        "english": "Call the police!",
        "local": "警察を呼んでください！",
        "romanized": "Keisatsu wo yonde kudasai!",
        "phonetic": "kay-sah-tsoo oh yon-deh koo-dah-sai",
        "category": "police",
        "notes": "Dial 110 for police"
      },
      {
        "id": "hospital",
        "english": "Where is the hospital?",
        "local": "病院はどこですか？",
        "romanized": "Byōin wa doko desu ka?",
        "phonetic": "byoh-een wah doh-koh des-kah",
        "category": "medical",
        "notes": null
      },
      {
        "id": "robbed",
        "english": "I've been robbed",
        "local": "盗まれました",
        "romanized": "Nusumaremashita",
        "phonetic": "noo-sue-mah-reh-mah-shh-tah",
        "category": "police",
        "notes": null
      },
      {
        "id": "allergic",
        "english": "I'm allergic to ___",
        "local": "___アレルギーがあります",
        "romanized": "___ arerugī ga arimasu",
        "phonetic": "___ ah-reh-roo-gee gah ah-ree-mas",
        "category": "medical",
        "notes": "Fill in: peanuts=ピーナッツ, shellfish=甲殻類, eggs=卵"
      },
      {
        "id": "dont_speak",
        "english": "I don't speak [language]",
        "local": "日本語が話せません",
        "romanized": "Nihongo ga hanasemasen",
        "phonetic": "nee-hon-goh gah hah-nah-seh-mah-sen",
        "category": "communication",
        "notes": null
      },
      {
        "id": "embassy",
        "english": "I need to contact my embassy",
        "local": "大使館に連絡したいです",
        "romanized": "Taishikan ni renraku shitai desu",
        "phonetic": "tai-shee-kahn nee ren-rah-koo shh-tai des",
        "category": "critical",
        "notes": null
      },
      {
        "id": "fire",
        "english": "Fire!",
        "local": "火事だ！",
        "romanized": "Kaji da!",
        "phonetic": "kah-jee dah",
        "category": "critical",
        "notes": "Dial 119 for fire"
      },
      {
        "id": "lost_passport",
        "english": "I lost my passport",
        "local": "パスポートを紛失しました",
        "romanized": "Pasupōto wo funshitsu shimashita",
        "phonetic": "pah-sue-poh-toh oh foon-shee-tsoo shee-mah-shh-tah",
        "category": "critical",
        "notes": "Go to nearest police box (交番 kōban) first, then embassy"
      },
      {
        "id": "need_doctor",
        "english": "I need a doctor",
        "local": "医者が必要です",
        "romanized": "Isha ga hitsuyō desu",
        "phonetic": "ee-shah gah hee-tsoo-yoh des",
        "category": "medical",
        "notes": null
      },
      {
        "id": "feel_unsafe",
        "english": "I feel unsafe / I'm in danger",
        "local": "危険です・助けてください",
        "romanized": "Kiken desu / Tasukete kudasai",
        "phonetic": "kee-ken des / tah-sue-keh-teh koo-dah-sai",
        "category": "critical",
        "notes": null
      }
    ]
  },

  // ── 2. Legal Rights When Detained ──
  "legalRights": {
    "summary": "Japan allows police to detain suspects for up to 23 days before charges. You have the right to contact your embassy and request a lawyer, but there is no right to have a lawyer present during interrogation.",
    "maxDetentionWithoutCharge": "23 days",
    "maxDetentionNotes": "48h initial + 10-day extension + 10-day re-extension + 3 days for prosecutors",
    "rightToLawyer": true,
    "lawyerDuringInterrogation": false,
    "lawyerDuringInterrogationNotes": "Lawyer can visit you in detention but cannot be present in the interrogation room",
    "rightToEmbassyContact": true,
    "embassyContactNotes": "Police are required to notify your embassy if you request it under the Vienna Convention",
    "rightToSilence": true,
    "rightToSilenceNotes": "You have the right to remain silent. Exercise it — confession rate in Japan is 99%+",
    "rightToInterpreter": true,
    "interpreterNotes": "Free interpreter provided, but quality varies. Request your embassy's recommended interpreter if possible",
    "keyDosAndDonts": [
      {
        "type": "do",
        "text": "Immediately request to contact your embassy"
      },
      {
        "type": "do",
        "text": "State clearly: 'I want a lawyer' (弁護士が必要です / Bengoshi ga hitsuyō desu)"
      },
      {
        "type": "do",
        "text": "Exercise your right to remain silent until a lawyer arrives"
      },
      {
        "type": "do",
        "text": "Stay calm and polite — demeanor matters significantly in Japanese legal proceedings"
      },
      {
        "type": "dont",
        "text": "Do NOT sign any document you cannot read in your language"
      },
      {
        "type": "dont",
        "text": "Do NOT admit to anything, even informally — statements can be used against you"
      },
      {
        "type": "dont",
        "text": "Do NOT resist physically — assault on an officer is a separate serious charge"
      }
    ],
    "localLawyerHotline": "Japan Legal Support Center (Houterasu): 0570-078377 (multilingual)",
    "commonOffensesForTourists": [
      "Drug possession (zero tolerance — even trace amounts)",
      "Overstaying visa",
      "Public intoxication / disorderly conduct",
      "Photography in restricted areas"
    ],
    "bailAvailable": false,
    "bailNotes": "Bail is rarely granted to foreigners during the initial 23-day detention period",
    "policeReportProcess": "Go to the nearest police box (交番 kōban) or police station. Ask for English support. You'll receive a 受理番号 (juribanō — receipt number) needed for insurance claims.",
    "sources": [
      "US Embassy Tokyo — Arrest of a US Citizen",
      "Japan Federation of Bar Associations",
      "Japan Legal Support Center (Houterasu)"
    ]
  },

  // ── 3. Natural Disaster Protocols ──
  "naturalDisasters": {
    "primaryRisks": ["earthquake", "tsunami", "typhoon", "volcanic_eruption", "flooding"],
    "riskLevel": "high",  // "low" | "moderate" | "high" — overall natural disaster risk
    "protocols": [
      {
        "type": "earthquake",
        "riskLevel": "high",
        "alertSystem": "J-Alert (nationwide) + Earthquake Early Warning (緊急地震速報) on all phones",
        "alertAppOffline": "Safety Tips (NTA) — works offline, push alerts in English",
        "immediateActions": [
          "DROP to hands and knees",
          "Take COVER under sturdy furniture or against interior wall",
          "HOLD ON until shaking stops",
          "Stay away from windows, heavy furniture, and exterior walls",
          "If outdoors: move to open area away from buildings, power lines, trees"
        ],
        "afterActions": [
          "Check for injuries, apply first aid",
          "Expect aftershocks — they can be strong",
          "If near coast, move to high ground immediately (tsunami risk)",
          "Check gas lines — turn off if you smell gas",
          "Tune to NHK World (English) for updates"
        ],
        "shelterInfo": "Designated evacuation sites (避難所 hinanjo) are marked with green signs at schools and parks. Google Maps shows them offline if pre-cached.",
        "localPhrase": "地震だ！ (Jishin da!) — Earthquake!",
        "seasonality": null
      },
      {
        "type": "tsunami",
        "riskLevel": "high",
        "alertSystem": "J-Alert + tsunami warning sirens along coastline",
        "alertAppOffline": "Safety Tips (NTA)",
        "immediateActions": [
          "Move INLAND and UPHILL immediately — don't wait for official warning",
          "Get above 30m/100ft elevation if possible",
          "Never go to the beach to watch — waves move faster than you can run",
          "If in a building, go to 3rd floor or higher",
          "If in a boat, head to deep water (offshore)"
        ],
        "afterActions": [
          "Stay at high ground — multiple waves can arrive over hours",
          "Do not return to coast until official all-clear",
          "Avoid flooded areas — debris, contamination, and structural damage"
        ],
        "shelterInfo": "Tsunami evacuation towers (津波避難タワー) exist in coastal towns. Look for blue tsunami evacuation signs pointing uphill.",
        "localPhrase": "津波！高台へ！ (Tsunami! Takadai e!) — Tsunami! Go to high ground!",
        "seasonality": null
      },
      {
        "type": "typhoon",
        "riskLevel": "moderate",
        "alertSystem": "Japan Meteorological Agency warnings via TV, radio, and smartphone push",
        "alertAppOffline": "Safety Tips (NTA) + NHK World app",
        "immediateActions": [
          "Stay indoors — away from windows",
          "Stock water and food for 2-3 days",
          "Charge all devices",
          "Know your building's designated shelter area",
          "If flooding risk: move to upper floors"
        ],
        "afterActions": [
          "Avoid downed power lines and flooded roads",
          "Check for landslide risk if in mountainous areas",
          "Trains may be suspended — check Hyperdia or Jorudan for status"
        ],
        "shelterInfo": "Same evacuation centers as earthquakes. Hotels will typically shelter guests in place.",
        "localPhrase": "台風が来ます (Taifū ga kimasu) — A typhoon is coming",
        "seasonality": "June–October, peak August–September"
      }
    ],
    "offlineApps": [
      {
        "name": "Safety Tips",
        "publisher": "Japan National Tourism Agency",
        "platforms": ["iOS", "Android"],
        "offlineCapable": true,
        "features": "Earthquake/tsunami/typhoon alerts in English, evacuation maps, medical phrases"
      }
    ],
    "emergencyBroadcast": {
      "station": "NHK World",
      "frequency": "Available on most hotel TVs, 693 kHz AM radio",
      "language": "English",
      "notes": "Primary English-language emergency broadcast during disasters"
    }
  }
}
```

## Phrase Categories (standardized IDs)

Every country MUST include these 12 phrase IDs:

| ID | English | Category |
|---|---|---|
| `help` | Help! | critical |
| `call_ambulance` | Call an ambulance! | medical |
| `call_police` | Call the police! | police |
| `hospital` | Where is the hospital? | medical |
| `robbed` | I've been robbed | police |
| `allergic` | I'm allergic to ___ | medical |
| `dont_speak` | I don't speak [language] | communication |
| `embassy` | I need to contact my embassy | critical |
| `fire` | Fire! | critical |
| `lost_passport` | I lost my passport | critical |
| `need_doctor` | I need a doctor | medical |
| `feel_unsafe` | I feel unsafe / I'm in danger | critical |

Countries may add additional phrases (e.g., "earthquake!" for Japan, "unexploded ordnance" for Laos/Cambodia).

## Disaster Types (enum)

`earthquake` | `tsunami` | `typhoon` | `hurricane` | `cyclone` | `tornado` | `flooding` | `volcanic_eruption` | `wildfire` | `avalanche` | `sandstorm` | `extreme_heat` | `extreme_cold` | `landslide`

Only include types relevant to that country. A country like Thailand might have `flooding`, `earthquake` (minor), `tsunami` (coastal). Switzerland: `avalanche`, `flooding`, `earthquake` (minor).

## Legal Rights — Required Fields

Every country MUST include:
- `maxDetentionWithoutCharge` — string, the max legal hold time
- `rightToLawyer` — boolean
- `rightToEmbassyContact` — boolean
- `rightToSilence` — boolean
- `rightToInterpreter` — boolean
- `keyDosAndDonts` — at least 3 do's and 3 don'ts
- `policeReportProcess` — how to file (needed for insurance)

## File Naming

`emergency-data/{ISO2}.json` — matches `health-data/` convention.

## Size Budget

Target: 3-5KB per country (uncompressed JSON).
55 countries × 5KB = ~275KB raw, ~50KB gzipped.
Well within PWA cache budget.

## Build Integration

Future: `build-emergency-api.py` generates `/api/v1/emergency/{country-slug}.json` for API consumers, and a merged `emergency-bundle.json` for PWA offline cache.
