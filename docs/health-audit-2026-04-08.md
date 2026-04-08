# Health Country Pages — Audit & Enhancement Plan
**Date:** 2026-04-08
**Scope:** All 100 country health insurance / medication guides at `/health/`
**Source of truth:** `health-data/*.json` (34-field schema) → `scripts/build-health-page.py` → `docs/health-template.html`

---

## TL;DR

Structurally the dataset is in **excellent shape** — every page has every section, every page has valid `MedicalWebPage` + `FAQPage` + `BreadcrumbList` JSON-LD, every hospital callout has a phone number, every page has 3+ sources. The template system is idempotent and clean.

The real opportunities are:
1. **Tiny technical fixes** (1 malformed date, 49 stale dates, 27 boilerplate phrases)
2. **Depth gaps** — every page covers the same 14 sections at the same length, but content for high-traffic countries (Japan, Thailand, Mexico, Italy) could go 2–3× deeper, while edge-case content (yellow fever zones, altitude regions, Schengen-specific rules) is thin.
3. **Brand-new data fields & sections** that travelers actually search for but we don't yet cover (cost calculator, air quality, altitude, women's/LGBTQ+/family/diabetic care, telemedicine, etc.)
4. **Monetization** — these are the highest-intent pages on the site for travel insurance affiliates, and currently have no CTA.

---

## Tier 1 — Quick fixes (do this week)

| # | Fix | Affected | Effort |
|---|---|---|---|
| 1 | **Peru `lastUpdated` is malformed** (`2022026-03-30`) | 1 page (peru) | 1 min |
| 2 | **49 pages still show `2026-03-30`** as last-updated — re-run `build-health-page.py --all` after a no-op data touch, or bump `lastUpdated` to today programmatically | 49 pages | 5 min |
| 3 | **27 mental-health sections fall back to "Contact your embassy for referrals"** as their international support line. Replace with country-region-specific options (e.g., findahelpline.com, Befrienders Worldwide, regional ITAA hotlines, country-specific WhatsApp counseling services) | 27 pages | 1–2 hrs (data only) |
| 4 | **83 hero subtitles are templated boilerplate** — "Complete health & medication guide for traveling to X. Emergency numbers, pharmacy tips, hospital info, and travel insurance advice." Generate 1–2 country-specific hooks (banned med, malaria zone, altitude, visa health insurance requirement) for each. Compare Japan's hook ("Sudafed/Adderall banned") to Albania's generic one — Japan converts better in SERPs. | 83 pages | 1 day (data + LLM-assisted) |
| 5 | **Health-data files share duplicate "index 3.html" copies in working tree** from a botched copy. Delete the 47 `health/*/index 3.html` files (they're untracked, not in git) | 47 files | 1 min |

---

## Tier 2 — Section depth upgrades

The current template renders every section at roughly the same length whether the country is Japan or Luxembourg. File size varies by only ~33 lines (818–851) across all 100 countries, which means we're under-serving high-complexity destinations.

### 2a. Make hospitals listings richer
Currently each hospital has: name, area, phone, English flag, 1-line note. Add to the schema:
- **`address`** — full street address (required for Schema.org `Hospital` rich results)
- **`coordinates`** — `{lat, lng}` so we can generate a static map embed and "directions" deep-link to Google/Apple Maps
- **`hours`** — at minimum a "24/7 ER: yes/no" boolean, ideally weekday/weekend hours
- **`acceptsCreditCards`** + **`upfrontPaymentRequired`** — critical info travelers Google
- **`directBillingNetworks`** — array of insurers that direct-bill (e.g., `["Allianz","AXA","Cigna Global"]`). This is the #1 question travelers actually ask.
- **`specialties`** — array (`["maternity","cardiac","trauma","pediatrics"]`)
- **`averageWaitMinutes`** — optional, a rough "typical ER wait" range
- **`website`** — official URL
- **`googleMapsUrl`** — direct deep link
- Add a 4th and 5th hospital for capital cities and destinations with multiple tourist hubs (Mexico has Cancún + CDMX + Tulum + PV — currently we only list ~3)

### 2b. Add a "Cost cheat sheet" callout
Travelers want to know: *if I walk into an ER tomorrow with no insurance, what does it cost?* Add a structured `commonCosts` field:
```json
"commonCosts": {
  "doctorVisit": "$30-60",
  "erVisitNoAdmission": "$100-200",
  "overnightAdmission": "$300-600 / night",
  "ambulance": "$0 (free)",
  "rabiesShot": "$80-150 series",
  "stitches": "$50-150",
  "xray": "$40-100",
  "covidTest": "$15-50"
}
```
Render as a small table. This is what people are searching when they Google "Thailand hospital cost without insurance".

### 2c. Add a "When to evacuate" section
For lower-quality healthcare countries (rating ≤3), add a `medicalEvacuation` field:
- Where do most evacuations route to? (Bangkok, Singapore, Nairobi, Dubai, Miami, Frankfurt)
- Typical cost range ($5K–$150K)
- Recommended evac providers (Global Rescue, MedJet, International SOS) — affiliate opportunity
- Conditions that absolutely require evacuation (severe trauma, complex cardiac, neurosurgery, major burns)

### 2d. Pharmacy: add the *one chain you'll actually find*
Every country has 1–2 dominant pharmacy chains (Watsons, Boots, Walgreens, Mercury, Farmacia Guadalajara). The data should include:
- **`pharmacyChains`** — array of `{name, logoUrl, identifyingFeature}` so travelers can spot them on the street
- A photo of a typical pharmacy storefront for visual recognition (especially valuable in non-Latin script countries)

### 2e. Pharmacy: drug name translation table
Tylenol = Paracetamol = Doliprane (FR) = Panadol (UK/Asia) = Tachipirina (IT). This is a constant traveler pain point. Add `drugNameMap`:
```json
"drugNameMap": [
  {"genericName":"acetaminophen","localBrand":"Tachipirina","note":"Most common Italian brand"},
  {"genericName":"ibuprofen","localBrand":"Brufen","note":"OTC at any farmacia"}
]
```

### 2f. Vaccinations: time-of-year nuance
Yellow fever, malaria, Japanese encephalitis, dengue all have seasonal/regional patterns. Add to vaccinations array:
- **`region`** — "northern lowlands only", "below 1,800m", "Amazon basin", "monsoon season May–Oct"
- **`whenToGet`** — weeks before travel (yellow fever needs 10 days)

---

## Tier 3 — Brand-new fields & sections (high traveler value)

These are gaps users actively search for but the dataset has no corresponding field.

### 3a. Air quality / pollution
Massive gap for **India, China, Mongolia, Pakistan, Bangladesh, Vietnam, Thailand (burning season), Indonesia (haze), Mexico City, Iran**. Add:
- `airQuality.typicalAQI` — annual average
- `airQuality.worstMonths` — list
- `airQuality.maskRecommendation` — N95/KN95 advice
- `airQuality.respiratoryRiskNote`
- Link to live AQI dashboard (IQAir, AirVisual)

### 3b. Altitude sickness
Critical for **Bolivia (La Paz, Uyuni), Peru (Cusco, Puno), Ecuador (Quito), Nepal (trekking), Ethiopia (Simien, Lalibela), Tibet, Bhutan, Colombia (Bogotá), Mexico City**. Add:
- `altitude.maxElevationCommon` — meters
- `altitude.acclimatizationDays`
- `altitude.diamoxAvailability` — OTC vs prescription locally
- `altitude.warningSymptoms`

### 3c. Heat / sun / dehydration
Useful for desert + tropical destinations (UAE, Saudi, Qatar, Kuwait, India in May, Vietnam, Cambodia, Death Valley equivalents). Add `heatRisk` with peak months, hydration tips, heatstroke warning signs.

### 3d. Mosquito-borne disease calendar
Dengue, Zika, chikungunya, malaria, JE — each has seasonality. A small monthly grid showing risk would be far more useful than a paragraph. Add `vectorBorneDiseases[]` with `disease`, `riskMonths`, `regions`, `repellent recommendation` (DEET % needed).

### 3e. Women's health
Often-Googled, never on travel sites. Add `womensHealth`:
- Tampon vs pad availability (some countries are pad-only)
- Contraception OTC availability (morning-after pill access varies wildly)
- Abortion legality / access
- Menstrual cup + disposal norms
- OB/GYN availability for pregnant travelers
- Specific tampons-banned countries (none, but several have very limited availability)

### 3f. LGBTQ+ healthcare
- HIV testing availability and stigma
- PrEP access
- Hormone therapy continuity for trans travelers (massive unmet need — most travel guides don't touch this)
- Countries where same-sex partners may be denied next-of-kin status in hospitals

### 3g. Family / pediatric travel
- Pediatric ER availability
- Children's hospital recommendations
- Baby formula brands available
- Childhood vaccine equivalencies
- Diaper / wipes availability

### 3h. Chronic condition / accessibility-of-care
- **Insulin availability** by country and brand (huge issue — Lantus availability varies)
- **Dialysis centers** for travelers with CKD
- **Oxygen availability** for COPD travelers
- **EpiPen / adrenaline auto-injector** — many countries don't sell them; alternatives noted
- **Allergy medical ID card translations** (peanut, gluten, shellfish in local language) — already partially covered in pharmacy phrases but should be its own callout for severe allergies

### 3i. Telemedicine fallback
- Which English-language telemedicine services work in this country (Air Doctor, Doctor Anywhere, MDLIVE, Teladoc geo-availability)
- Whether the traveler's home telemedicine plan works abroad

### 3j. Hospital scams / billing pitfalls
We have a `/scams/` section but health-specific scams are different. Add `hospitalScams[]`:
- Fake "international department" upsell
- Inflated "tourist tariff" billing
- Pharmacy markups on fake/expired drugs
- Ambulance kickback schemes
- Required deposits in some Southeast Asian hospitals

### 3k. Travel medical kit checklist (per country)
Different climates and risks → different kits. Render a printable checklist tailored to the country's risk profile (DEET 30%, ORS, anti-diarrheal, altitude med, antimalarial, etc.).

### 3l. Embassy / consulate quick-contacts
Already implied in sources ("US Embassy"), but should be its own quick-facts row with phone, address, after-hours number, and a "non-US" toggle (UK FCDO, Canadian, Australian, etc.). Most users assume tabiji is US-centric — broaden it.

### 3m. Air evacuation routing map
For each country, where does an emergency evac fly to? A simple field `evacuationDestinations: ["Bangkok","Singapore"]` powers a one-line map graphic.

---

## Tier 4 — Schema.org / SEO upgrades

### 4a. Add structured data we're not yet emitting
- **`Hospital`** entity per hospital callout — gets you rich results ("hospital near me" carousels). Needs the address + coordinates from §2a.
- **`HowTo`** schema on the "How to File an Insurance Claim" subsection.
- **`Drug`** schema on each restricted-medications list item.
- **`MedicalCondition`** + **`PreventativeProcedure`** on vaccinations list.
- **`SpeakableSpecification`** is already on quick-facts; extend to emergency numbers section so Google Assistant can read it.

### 4b. Hreflang
Currently English-only. For high-traffic countries (Japan, Thailand, Mexico, Italy, Spain, France, Germany), translated versions targeting `/health/japan/?lang=es` etc. would 5–10× the addressable search market. Even MT-translated versions would unlock long-tail.

### 4c. Internal linking
Currently each page links to:
- the matching `/countries/[slug]/` guide
- `/scams/`
- `/compare/`
- `/find/`

**Missing:**
- `/credit-cards/` — most premium travel cards include emergency medical / evacuation. Big monetization miss.
- `/popular-picks/` — link to top-3 popular things to do in that country.
- Cross-link to *neighboring countries* health guides (Schengen travelers especially need this).
- Link to compare pages: `/compare/japan-vs-thailand-health/` style URLs.

### 4d. Title tag optimization
Current: "Health & Medication Guide for Japan — tabiji.ai". Better: "Japan Travel Health Guide 2026: Banned Meds, Hospitals & Insurance". Country + year + 2 specific hooks beats generic patterns for SERP CTR.

### 4e. FAQ schema expansion
Currently 4 Qs per page. Extend to 8–10 — covers the long tail of "is X legal in Y", "do I need malaria pills for Y", "where do I find an English doctor in Y". Each extra Q is a chance to rank for a Google "People Also Ask" slot.

---

## Tier 5 — Monetization

These are some of the **highest-intent pages on the site** (someone searching "Thailand travel insurance" or "Japan banned medications" is in the buying funnel) and have **zero CTAs** today.

1. **Travel insurance affiliate widget** in the Insurance section. SafetyWing, Genki, World Nomads, IMG, Heymondo all have affiliate programs. A small "Get a quote in 2 minutes" embed below the existing insurance copy.
2. **Medical evacuation memberships** — Global Rescue and MedJet pay well per signup. Bake into the §2c "When to evacuate" section.
3. **eSIM / data plan affiliate** — Airalo, Holafly, Saily. People use phones to find hospitals; eSIM is highly contextual here.
4. **Vaccine clinics** — partnerships with Passport Health (US), CityDoc (UK), MASTA (UK) for pre-travel vaccination booking. Affiliate or referral.
5. **Telemedicine** — Air Doctor and Doctor Anywhere both have affiliate programs aligned to international travelers.
6. **Branded "Print / Save" upsell** — the existing print button is a prime spot to upsell a branded PDF download in exchange for an email (lead capture).
7. **Smart packing kit** — Amazon affiliate links to N95 masks, ORS, DEET, water purification tablets, first-aid kit.

A reasonable target: a single well-placed affiliate quote widget across all 100 pages converts at 0.5–1.5% of pageviews; with $20–$60 per signup that's a meaningful revenue line at the page volume health guides will get.

---

## Tier 6 — UX / interactivity

1. **Quality rating tooltip** — clicking the ★★★★★ should explain *what the rating means* and show the 5 sub-criteria (English availability, infrastructure, pharmacy access, insurance acceptance, evacuation need).
2. **Print-as-PDF "Wallet card"** — generate a credit-card-sized PDF with: emergency number, blood type field, top hospital, allergy phrases. Print bar already exists; this is a parallel option.
3. **Compare 2 countries' health profiles** — `/compare/japan-vs-thailand-health/`. We have `/compare/` already; extend it to a health tab.
4. **Filter the hub at `/health/` by traveler profile** — "I have diabetes / I'm pregnant / I have asthma / I'm allergic to penicillin" → the hub re-ranks countries by suitability. Currently the hub is just a static A–Z grid by region.
5. **Saved offline mode** — health pages should be aggressively cached offline (PWA already exists per `manifest.json` reference). Test that the offline experience surfaces emergency numbers & top hospital reliably.
6. **Click-to-call buttons** on hospital phone numbers (`tel:+...`). Mobile users would love this. Currently the phones are plain text.
7. **Embedded mini-map** showing hospital pins. Even a static OpenStreetMap thumbnail per hospital would add a lot of trust signal.
8. **"Last verified by" badge** — e.g., "Hospital details verified 2026-03-15 by Dr. X" or "Reviewed by Jane Y, RN". Schema.org `reviewedBy`. Adds E-E-A-T (medical YMYL pages especially benefit from real human reviewers per Google's medic update).
9. **User-submitted updates** — small "report outdated info" link per section. Crowdsourced freshness.

---

## Tier 7 — Data ops & freshness

1. **Add `sourceLastChecked` per top-level field**, not just `lastUpdated` for the whole record. So we know "the visa-free entry rule was checked 2026-03-30 even though the rest of the page is older".
2. **Automated freshness checker** — nightly cron that hits CDC + WHO + IATA Travel Centre RSS feeds and flags any country whose advisory level changed.
3. **Currency / cost auto-conversion** — costs are hardcoded in USD or local currency. A small post-processing pass that converts to user's locale (USD / EUR / GBP / AUD) at render time would feel much more localized.
4. **Verification log per country** — `health-data/changelog/JP.md` style file recording what changed when. Builds trust and helps you defend "freshness" in ad/Google quality reviews.
5. **Tier classification** — explicit `dataCompleteness: "core" | "enhanced" | "verified"` field, surfaced as a small badge. Drives a roadmap from "core" → "verified" tier across the dataset.

---

## Suggested rollout order

| Sprint | Focus | Outcome |
|---|---|---|
| **Sprint 1 (this week)** | Tier 1 quick fixes + Tier 4a Hospital schema | Clean dataset, rich-result eligible |
| **Sprint 2** | Tier 2a–2b (hospital fields + cost cheat sheet) | Most-asked traveler questions answered |
| **Sprint 3** | Tier 5.1 + 5.2 (travel insurance & evac affiliates) | Revenue line live |
| **Sprint 4** | Tier 3a–3d (air quality, altitude, heat, mosquito) | Differentiation vs CDC/WHO copycats |
| **Sprint 5** | Tier 3e–3i (women's, LGBTQ+, family, chronic, telemedicine) | Underserved-audience moat |
| **Sprint 6** | Tier 6 UX (click-to-call, maps, wallet card) | Mobile experience |
| **Sprint 7+** | Tier 4b hreflang + Tier 7 ops | International + sustainability |

---

## Implementation notes for the dev team

- All upgrades belong in the **schema** (`health-data/*.json` + the `gen_*` functions in `scripts/build-health-page.py`), not in per-page edits. The template system is fully idempotent: change schema → re-run `build-health-page.py --all` → all 100 pages regenerate cleanly.
- Adding new fields is safe — the renderer only emits sections when their data is present, so legacy pages without the new fields won't break.
- For LLM-assisted enrichment (cost cheat sheets, drug name maps, women's health notes), batch country lists through a single Claude call with a strict JSON output schema → write directly into `health-data/*.json` → regenerate.
- Keep `qualityRating` as the existing 1–5 scale but add a **separate** `dataCompleteness` field (1–5) so we can track "page covers all our enhanced fields" independently of "this country has good healthcare".
