#!/usr/bin/env python3
"""
Enrich 18 existing safety profiles with accurate travel data.

Fills in empty sections for: AU, CO, CR, DE, ES, FR, GB, GR, ID, IT, KR, MA, MX, NZ, PE, PT, TR, VN

Sections populated:
  - cultural (tipping, dressCode, greetings, taboos, haggling)
  - phrases (10 key travel phrases in local language + phonetics)
  - connectivity (simOptions, wifiAvailability, bestOption)
  - practical (drivingSide, plugType, voltage, dialCode, visaFreeCountries, timeZone, bestTimeToVisit)
  - safety (overallRisk, violentCrime, pettyCrime, naturalDisasters, lgbtSafety, soloFemaleSafety, notes)

JP and TH are complete reference profiles — NOT touched.

Usage: python3 app/scripts/enrich-safety-profiles.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SAFETY_DIR = BASE_DIR / "app" / "data" / "safety"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Country enrichment data ───────────────────────────────────────────────────

ENRICHMENT = {

    "AU": {
        "cultural": {
            "tipping": "Not expected. Australian wages are higher by law and service charges are not added to bills. A tip of 10% is appreciated for exceptional service at restaurants, but never obligatory. No tipping expected for taxis or hotels.",
            "dressCode": "Very casual — thongs (flip-flops) and shorts are acceptable almost everywhere. Smart casual for city restaurants and bars. Keep beachwear at the beach or pool. Sun protection (hat, sunscreen) is a practical necessity.",
            "greetings": "Handshake on first meeting. Close friends hug. Very informal — 'G'day' or 'How ya going?' are standard. First-name basis happens almost immediately, even in business contexts.",
            "taboos": [
                "Queue jumping — Australians take orderly queuing very seriously",
                "Boasting or bragging — 'tall poppy syndrome' means showing off is frowned upon",
                "Bringing food, plants, or undeclared items through customs — heavy fines apply",
                "Littering — particularly in national parks and beaches",
                "Calling Australia 'the outback' or assuming everyone lives near crocodiles",
                "Assuming Australians and New Zealanders are interchangeable"
            ],
            "haggling": "Not practiced. Prices are fixed in shops, restaurants, and markets."
        },
        "phrases": [
            {"english": "Hello", "local": "G'day / Hello", "phonetic": "g-day"},
            {"english": "Thank you", "local": "Thank you / Cheers", "phonetic": "thank-yoo / cheerz"},
            {"english": "Excuse me / Sorry", "local": "Excuse me / Sorry", "phonetic": "ek-skyooz-mee"},
            {"english": "Yes", "local": "Yeah / Yes", "phonetic": "yeh"},
            {"english": "No", "local": "Nah / No", "phonetic": "nah"},
            {"english": "Please", "local": "Please", "phonetic": "pleez"},
            {"english": "How much?", "local": "How much is it?", "phonetic": "how much iz it"},
            {"english": "Where is...?", "local": "Where is...?", "phonetic": "wair iz"},
            {"english": "Help!", "local": "Help!", "phonetic": "help"},
            {"english": "Goodbye", "local": "See ya / Goodbye", "phonetic": "see-yah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs at the airport from Telstra (~$30 AUD, 15GB), Optus, or Vodafone AU. Telstra has the best rural/outback coverage. eSIM via Airalo or Holafly from $8 USD for 1GB, $25 for 10GB.",
            "wifiAvailability": "Good WiFi at cafes, hotels, and libraries. McDonald's and most major coffee chains (Gloria Jean's, The Coffee Club) offer free WiFi. Coverage is spotty in remote/outback areas.",
            "bestOption": "Telstra prepaid SIM at the airport (~$30 AUD, 15-40GB) for best rural coverage. eSIM via Airalo if you want to activate before arrival."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "left",
            "plugType": ["I"],
            "voltage": "230V / 50Hz",
            "dialCode": "+61",
            "visaFreeCountries": "US citizens require an ETA (Electronic Travel Authority) — ~$20 USD, applied online before travel. UK citizens also need an ETA. EU citizens require an ETA or visa.",
            "timeZone": "UTC+8 to UTC+11 (varies by state/territory; AEDT, AEST, ACST, AWST)",
            "bestTimeToVisit": "September-November (spring) and March-May (autumn) offer mild weather nationwide. Avoid December-February for the southeast (extreme heat) and north (tropical wet season)."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "low",
            "pettyCrime": "low",
            "naturalDisasters": ["bushfires", "floods", "cyclones (north)", "sharks", "venomous wildlife"],
            "lgbtSafety": "Very welcoming. Same-sex marriage legal since 2017. Sydney's Mardi Gras is one of the world's largest LGBTQ+ events. Generally safe everywhere.",
            "soloFemaleSafety": "Very safe. Standard city precautions apply at night. Remote areas require planning for safety (distances, limited services).",
            "notes": "One of the safest countries in the world. Main risks are environmental — sun, ocean rips, wildlife. Follow beach safety flags and always swim between the flags. Driving long distances in remote areas requires preparation."
        }
    },

    "CO": {
        "cultural": {
            "tipping": "10% propina (tip) is customary at sit-down restaurants and often added to the bill as 'propina voluntaria' — check before adding more. Tip taxi drivers by rounding up the fare. Hotel porters $1-2 USD per bag.",
            "dressCode": "Colombians dress smartly — looking presentable is a sign of respect. Avoid overly casual dress in cities. Medellin has a reputation for fashion-consciousness. Warmer coastal regions are more casual.",
            "greetings": "One cheek kiss between women and between men and women. Men shake hands. 'Buenos días/tardes/noches' always. First-name basis after introduction. Personal space is closer than Northern Europe/North America.",
            "taboos": [
                "Discussing drug trafficking or Pablo Escobar with locals — deeply sensitive and offensive",
                "Assuming Colombia is dangerous everywhere — locals are proud of the country's transformation",
                "Wearing expensive jewelry or displaying phones in crowded areas",
                "Declining food or drink offered by a host — very rude",
                "Calling people 'negro' or commenting on race — contextually complex, avoid",
                "Drinking tap water outside Bogotá, Medellín, and main cities"
            ],
            "haggling": "Acceptable in markets and with street vendors. Not appropriate in established shops or restaurants."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Gracias", "phonetic": "grah-syahs"},
            {"english": "Excuse me / Sorry", "local": "Perdón / Disculpe", "phonetic": "pehr-don / dees-kool-peh"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "no"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto cuesta?", "phonetic": "kwahn-toh kwes-tah"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Auxilio! / ¡Ayuda!", "phonetic": "owk-see-lyoh / ah-yoo-dah"},
            {"english": "Goodbye", "local": "Adiós / Chao", "phonetic": "ah-dyos / chow"}
        ],
        "connectivity": {
            "simOptions": "Local SIMs from Claro, Movistar, or Tigo available at airports and convenience stores (Éxito, Jumbo). ~$5-15 USD for 5-20GB. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Good WiFi in Bogotá, Medellín, and Cartagena. Most cafes, hostels, and hotels provide WiFi. Free public WiFi in many parks and town squares.",
            "bestOption": "Local Claro or Tigo prepaid SIM — best coverage and cheapest data. Buy at El Dorado airport on arrival or at any Éxito supermarket."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["A", "B"],
            "voltage": "110V / 60Hz",
            "dialCode": "+57",
            "visaFreeCountries": "US citizens: 90 days visa-free on tourist entry. UK and EU citizens also visa-free for 90 days.",
            "timeZone": "UTC-05:00 (Colombia Standard Time, no daylight saving)",
            "bestTimeToVisit": "December-March and July-August (dry seasons). Cartagena is good year-round. Avoid April-May and October-November (heavy rains)."
        },
        "safety": {
            "overallRisk": "medium",
            "violentCrime": "medium",
            "pettyCrime": "high",
            "naturalDisasters": ["earthquakes", "volcanic activity", "flooding"],
            "lgbtSafety": "Legal and increasingly accepted in major cities (Bogotá, Medellín). Same-sex marriage legal. More conservative in rural areas.",
            "soloFemaleSafety": "Exercise increased caution. Solo female travel is common in tourist areas but requires awareness. Avoid traveling alone at night, especially in less-touristed areas.",
            "notes": "Colombia has transformed enormously but petty crime (phone snatching, bag theft) remains high in cities. Use Uber or InDriver over street taxis. Avoid displaying valuables. Bogotá's La Candelaria and Medellín's city center require vigilance at night."
        }
    },

    "CR": {
        "cultural": {
            "tipping": "10% is standard at restaurants and typically added to the bill as 'servicio incluido' — check if already included. Tip tour guides $5-10/day per person. Round up taxi fares.",
            "dressCode": "Casual and practical. Lightweight clothing for coastal/jungle areas. Modest dress for church visits. Bring a rain jacket — it rains frequently even in dry season.",
            "greetings": "One cheek kiss between women and between men and women (in social settings). Handshake in business. Very friendly and informal. 'Pura vida' (pure life) is the national saying — use it for hello, goodbye, thanks, you're welcome.",
            "taboos": [
                "Littering — Costa Ricans are very environmentally proud",
                "Wasting food",
                "Being overly rushed — 'Tico time' is real; things move slowly",
                "Disrespecting nature reserves or wildlife",
                "Leaving tips on the table uncollected (hand it directly)"
            ],
            "haggling": "Not common in established shops or restaurants. Acceptable with independent artisan vendors at craft markets."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola / ¡Pura vida!", "phonetic": "oh-lah / poo-rah vee-dah"},
            {"english": "Thank you", "local": "Gracias / ¡Pura vida!", "phonetic": "grah-syahs"},
            {"english": "Excuse me / Sorry", "local": "Con permiso / Disculpe", "phonetic": "kon pehr-mee-so"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "no"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto cuesta?", "phonetic": "kwahn-toh kwes-tah"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Auxilio! / ¡Ayuda!", "phonetic": "owk-see-lyoh"},
            {"english": "Goodbye", "local": "Adiós / ¡Pura vida!", "phonetic": "ah-dyos"}
        ],
        "connectivity": {
            "simOptions": "SIMs from Kolbi (state-owned, best coverage), Claro, or Movistar at airports and convenience stores. ~$10-20 USD for 10-30GB. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Good WiFi in San José, tourist towns (La Fortuna, Tamarindo, Manuel Antonio). More limited in remote jungle/beach areas. Most hotels and sodas (local restaurants) offer WiFi.",
            "bestOption": "Kolbi prepaid SIM for best national coverage, especially in remote national parks. Buy at Juan Santamaría International Airport."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["A", "B"],
            "voltage": "120V / 60Hz",
            "dialCode": "+506",
            "visaFreeCountries": "US citizens: 90 days visa-free. UK and EU citizens also visa-free for 90 days.",
            "timeZone": "UTC-06:00 (Central Standard Time, no daylight saving)",
            "bestTimeToVisit": "December-April (dry season). May-November is green season (cheaper, fewer crowds, brief afternoon rains). Caribbean coast has a different dry season (September-October)."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes", "volcanic eruptions", "flooding", "tropical storms"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2020. San José has a small but vibrant LGBTQ+ scene. Generally welcoming across the country.",
            "soloFemaleSafety": "Generally safe. Standard precautions apply. Avoid beaches at night alone. Catcalling is common but generally not threatening.",
            "notes": "One of the safer Central American countries. Petty theft (bag snatching, car break-ins) is the main concern. Never leave bags visible in parked cars. Riptides are a serious beach hazard — heed warning flags."
        }
    },

    "DE": {
        "cultural": {
            "tipping": "Round up restaurant bills or leave 5-10% for good service — tell the server the total you want to pay when settling. Don't leave cash on the table. Tip taxi drivers 5-10% by rounding up. Not obligatory but appreciated.",
            "dressCode": "Practical and understated. Germans dress for function. Smart casual for restaurants. No shorts or flip-flops in upscale venues. Business attire is formal.",
            "greetings": "Firm handshake, direct eye contact. 'Guten Morgen/Tag/Abend' (Good morning/day/evening). Last-name basis with Herr/Frau until invited to use first names. Punctuality is extremely important.",
            "taboos": [
                "Being late — punctuality is considered basic respect in Germany",
                "Jaywalking — Germans wait for the light even on empty roads",
                "Making Nazi references or jokes — illegal and deeply offensive",
                "Talking loudly in public spaces, especially public transport",
                "Shopping on Sundays — most stores are closed (Ladenschlussgesetz)",
                "Wishing someone happy birthday before their actual birthday — considered bad luck"
            ],
            "haggling": "Not practiced. Prices are fixed."
        },
        "phrases": [
            {"english": "Hello", "local": "Hallo / Guten Tag", "phonetic": "hah-loh / goo-ten tahk"},
            {"english": "Thank you", "local": "Danke / Danke schön", "phonetic": "dahn-keh / dahn-keh shern"},
            {"english": "Excuse me / Sorry", "local": "Entschuldigung", "phonetic": "ent-shool-dee-goong"},
            {"english": "Yes", "local": "Ja", "phonetic": "yah"},
            {"english": "No", "local": "Nein", "phonetic": "nine"},
            {"english": "Please", "local": "Bitte", "phonetic": "bit-teh"},
            {"english": "How much?", "local": "Wie viel kostet das?", "phonetic": "vee-feel kos-tet dahs"},
            {"english": "Where is...?", "local": "Wo ist...?", "phonetic": "voh ist"},
            {"english": "Help!", "local": "Hilfe!", "phonetic": "hil-feh"},
            {"english": "Goodbye", "local": "Auf Wiedersehen / Tschüss", "phonetic": "owf-vee-dehr-zayn / chuss"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Telekom (best coverage), Vodafone, or O2 at airports, Saturn/MediaMarkt stores, and supermarkets. ~€15-30 for 10-25GB. eSIM via Airalo or Holafly from $5 USD. Note: registration required for SIM (passport needed).",
            "wifiAvailability": "WiFi ubiquitous at hotels, cafes, and restaurants. Train stations have free WiFi. Deutsche Bahn trains have WiFi (variable quality). Public free WiFi exists in many city centers.",
            "bestOption": "Telekom or Vodafone prepaid SIM for best LTE/5G coverage. Buy at Frankfurt or Munich airport on arrival, or at a MediaMarkt electronics store."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+49",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period. ETA (ETIAS) system planned for 2025.",
            "timeZone": "UTC+01:00 (CET) / UTC+02:00 (CEST in summer)",
            "bestTimeToVisit": "May-September for outdoor activities and festivals (Oktoberfest late Sep-Oct). Christmas markets in December are magical. Avoid school holiday weeks for crowds."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "low",
            "naturalDisasters": ["flooding (Rhine, Elbe rivers)"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2017. Berlin is one of Europe's most LGBTQ+ inclusive cities. Cologne Pride (Christopher Street Day) is a major event.",
            "soloFemaleSafety": "Very safe. Standard city precautions apply at night.",
            "notes": "Germany is one of Europe's safest countries. Pickpockets operate in tourist areas (Cologne Cathedral, Berlin Hauptbahnhof, Munich Marienplatz). Keep bags zipped and close."
        }
    },

    "ES": {
        "cultural": {
            "tipping": "Not obligatory but appreciated. Leave €1-2 per person for restaurant meals or round up the bill. Cafes: 10-20 cents for coffee. Taxis: round up. Service charge is rarely included.",
            "dressCode": "Stylish and put-together in cities. Avoid shorts and flip-flops in city centers and restaurants. Cover shoulders and knees for churches. Evening meal (after 9pm) calls for smarter dress.",
            "greetings": "Two cheek kisses (left first) between women and between men and women. Men shake hands or hug. Very warm and expressive. 'Hola' is universal. First-name basis quickly.",
            "taboos": [
                "Eating dinner before 9pm (locals eat very late — lunch is the main meal)",
                "Ordering a cappuccino after lunch or dinner (only for breakfast)",
                "Visiting a restaurant expecting to eat immediately — things move slowly by design",
                "Loud or aggressive behavior in public",
                "Sunbathing topless outside of designated beaches (fines in many cities)",
                "Rushing service staff — meals are social experiences, not transactions"
            ],
            "haggling": "Not practiced in shops or restaurants. Some flexibility at large markets (El Rastro in Madrid) but rare."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Gracias", "phonetic": "grah-thyahs"},
            {"english": "Excuse me / Sorry", "local": "Perdón / Disculpa", "phonetic": "pehr-don / dees-kool-pah"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "no"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto cuesta?", "phonetic": "kwahn-toh kwes-tah"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Ayuda! / ¡Socorro!", "phonetic": "ah-yoo-dah / so-kor-oh"},
            {"english": "Goodbye", "local": "Adiós / Hasta luego", "phonetic": "ah-dyos / as-tah lweh-go"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Orange, Vodafone ES, or Movistar at airports, El Corte Inglés, and phone shops. ~€10-20 for 10-25GB. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Excellent WiFi in hotels, cafes (especially in Madrid and Barcelona), and restaurants. Free public WiFi in many city centers and parks. AVE high-speed trains have WiFi.",
            "bestOption": "Orange or Vodafone prepaid SIM for widest 4G/5G coverage. Buy at BARAJAS (Madrid) or El Prat (Barcelona) airport on arrival."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+34",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period.",
            "timeZone": "UTC+01:00 (CET) / UTC+02:00 (CEST in summer)",
            "bestTimeToVisit": "April-June and September-October for best weather and fewer crowds. July-August is peak season (crowded, hot, expensive). Canary Islands are warm year-round."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "very-low",
            "pettyCrime": "medium",
            "naturalDisasters": ["wildfires (summer)", "flooding (Valencia/Mediterranean coast)"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2005. Madrid's Chueca neighborhood and Sitges are iconic LGBTQ+ destinations. Gran Canaria's Maspalomas is a major LGBTQ+ resort.",
            "soloFemaleSafety": "Very safe. Standard precautions at night. Barcelona's Las Ramblas is a pickpocket hotspot — be vigilant.",
            "notes": "Pickpocketing is Spain's main tourist crime risk — particularly in Barcelona (Las Ramblas, Sagrada Família, Metro), Madrid (Puerta del Sol), and Seville. Use a cross-body bag. Drink spiking at nightclubs reported — watch your drinks."
        }
    },

    "FR": {
        "cultural": {
            "tipping": "Service is included by law in all restaurant bills (service compris). Additional tipping is not expected but leaving €1-3 for good service is appreciated. Tip hotel porters €1-2 per bag. Cafes: leave change from your coins.",
            "dressCode": "French people dress with understated elegance — avoid overly casual dress in Paris, especially at night. Cover up modestly in churches. Beachwear stays at the beach. Looking effortless is the ideal.",
            "greetings": "Two cheek kisses (la bise) between friends — varies by region (2 in Paris, up to 4 in Provence). Handshake in business. Always say 'Bonjour Madame/Monsieur' when entering a shop. Saying 'Bonjour' is non-negotiable — skipping it is considered rude.",
            "taboos": [
                "Skipping 'Bonjour' when entering a shop, restaurant, or interacting with anyone",
                "Asking someone's salary, age, or political views (considered private)",
                "Pouring wine with your left hand (bad luck tradition)",
                "Putting bread upside down on the table (old superstition)",
                "Rushing through a meal — eating is a ritual, not a refueling stop",
                "Expecting shops and restaurants to be open at lunchtime (1pm-2pm many close)"
            ],
            "haggling": "Not practiced. Prices are fixed, except perhaps at flea markets (marchés aux puces) where gentle negotiation is acceptable."
        },
        "phrases": [
            {"english": "Hello", "local": "Bonjour", "phonetic": "bon-zhoor"},
            {"english": "Thank you", "local": "Merci / Merci beaucoup", "phonetic": "mehr-see / mehr-see boh-koo"},
            {"english": "Excuse me / Sorry", "local": "Excusez-moi / Pardon", "phonetic": "ek-skew-zay-mwah / par-don"},
            {"english": "Yes", "local": "Oui", "phonetic": "wee"},
            {"english": "No", "local": "Non", "phonetic": "non"},
            {"english": "Please", "local": "S'il vous plaît", "phonetic": "seel-voo-pleh"},
            {"english": "How much?", "local": "Combien ça coûte?", "phonetic": "kom-byan sah koot"},
            {"english": "Where is...?", "local": "Où est...?", "phonetic": "oo-eh"},
            {"english": "Help!", "local": "Au secours!", "phonetic": "oh-skoor"},
            {"english": "Goodbye", "local": "Au revoir", "phonetic": "oh-reh-vwahr"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Orange, SFR, or Free Mobile at airports, convenience stores (Relay), and phone shops. ~€10-20 for 10-30GB. eSIM via Airalo or Holafly from $5 USD. Free Mobile offers excellent value for data.",
            "wifiAvailability": "Excellent WiFi in hotels, cafes, and restaurants. Free public WiFi in Paris parks and many train stations. TGV high-speed trains have WiFi. Some Paris Métro stations have WiFi.",
            "bestOption": "Orange prepaid SIM for widest 4G/5G coverage across France. Buy at CDG or Orly airport arrivals hall. eSIM from Airalo if you want to set up before arrival."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "E"],
            "voltage": "230V / 50Hz",
            "dialCode": "+33",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period.",
            "timeZone": "UTC+01:00 (CET) / UTC+02:00 (CEST in summer)",
            "bestTimeToVisit": "April-June and September-October for mild weather, fewer crowds, and lower prices. July-August is peak season (crowded, expensive, Parisians leave for holiday). Paris in Christmas-New Year is magical."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["flooding (Seine river)", "heatwaves (summer)"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2013. Le Marais in Paris is a major LGBTQ+ hub. Paris Pride (Marche des Fiertés) is a major annual event.",
            "soloFemaleSafety": "Generally safe. Catcalling exists in some areas. Avoid poorly lit areas at night, particularly around Gare du Nord and Châtelet-Les Halles.",
            "notes": "Pickpocketing is the main tourist risk — particularly around the Eiffel Tower, Louvre, Sacré-Cœur, and the Paris Métro. Distraction scams (petition signing, friendship bracelet) are common near monuments. Keep bags close and zipped."
        }
    },

    "GB": {
        "cultural": {
            "tipping": "10-15% at sit-down restaurants if service is not already included (check the bill). Pubs: no tipping expected for drinks at the bar, but tip table service. Taxis: round up or 10-15%. Never tip in fast-food restaurants.",
            "dressCode": "Smart casual in city restaurants and theaters. Pubs are casual. Black tie for special events. London is fashion-forward — anything goes in the right context. Layers are essential given unpredictable weather.",
            "greetings": "Handshake on first meeting. Cheek kiss not standard in England (more common in social London). Very reserved — personal space matters. Apologizing frequently is a national pastime. Queue etiquette is sacred.",
            "taboos": [
                "Jumping the queue — the most serious social offense",
                "Asking someone's age, salary, or directly about their personal life",
                "Being too forward or loud in public (seen as brash)",
                "Confusing English/British/Scottish/Welsh — know the distinction",
                "Talking about religion or politics with strangers",
                "Not saying please and thank you at every opportunity"
            ],
            "haggling": "Not practiced in shops or restaurants. Antique markets and car boot sales allow some negotiation."
        },
        "phrases": [
            {"english": "Hello", "local": "Hello / Hiya / Alright?", "phonetic": "heh-loh / hi-yah"},
            {"english": "Thank you", "local": "Thank you / Cheers / Ta", "phonetic": "thank-yoo / cheerz"},
            {"english": "Excuse me / Sorry", "local": "Excuse me / Sorry / Pardon", "phonetic": "ek-skyooz-mee"},
            {"english": "Yes", "local": "Yes / Yeah", "phonetic": "yes / yeh"},
            {"english": "No", "local": "No", "phonetic": "noh"},
            {"english": "Please", "local": "Please", "phonetic": "pleez"},
            {"english": "How much?", "local": "How much is it?", "phonetic": "how much iz it"},
            {"english": "Where is...?", "local": "Where is...? / Whereabouts is...?", "phonetic": "wair iz"},
            {"english": "Help!", "local": "Help!", "phonetic": "help"},
            {"english": "Goodbye", "local": "Goodbye / Cheers / Ta-ra", "phonetic": "good-bye / tah-rah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from EE, Three, O2, or Vodafone UK at airports (WHSmith, Boots), supermarkets, or phone shops. ~£10-20 for 10-30GB. Three has unlimited data roaming deals. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Excellent WiFi nationwide. Most cafes (Costa, Starbucks, Pret), pubs, and hotels provide free WiFi. Free WiFi on London Underground (most stations). National Rail trains have WiFi (varies by operator).",
            "bestOption": "Three prepaid SIM for value and coverage. Buy at any Three store or airport WHSmith. eSIM from Airalo if you want to activate before landing at Heathrow."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "left",
            "plugType": ["G"],
            "voltage": "230V / 50Hz",
            "dialCode": "+44",
            "visaFreeCountries": "US citizens: 6 months visa-free (no pre-registration currently needed). EU citizens: 6 months visa-free. ETA (Electronic Travel Authorisation) required from 2025 for visa-free travelers.",
            "timeZone": "UTC+00:00 (GMT) / UTC+01:00 (BST in summer)",
            "bestTimeToVisit": "May-September for best weather. June-August is peak season. Shoulder seasons (April, October) offer fewer crowds. Scotland's Highlands are stunning in autumn."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["flooding", "severe storms"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal. London's Soho is a historic LGBTQ+ hub. Manchester's Canal Street and Brighton are major LGBTQ+ cities. Pride events nationwide.",
            "soloFemaleSafety": "Very safe. Standard urban precautions apply at night, especially in nightlife districts.",
            "notes": "Generally very safe. Knife crime exists in certain urban areas but doesn't typically affect tourists. Pickpockets active in London (Oxford Street, Notting Hill Carnival, tourist sites). Terrorism threat rated 'substantial' — standard vigilance."
        }
    },

    "GR": {
        "cultural": {
            "tipping": "Not obligatory but appreciated. Leave 10% at sit-down restaurants. Cafes: round up. Taxis: round up the fare. Tour guides: €5-10 per person per day. Service is not usually included in the bill.",
            "dressCode": "Casual on the islands. Shoulders and knees must be covered when entering churches and monasteries (sometimes scarves provided). Topless sunbathing accepted on many beaches. Smart casual in upscale Athens restaurants.",
            "greetings": "Handshake on first meeting. Good friends exchange cheek kisses. Very warm and hospitable (filoxenia — love of strangers). 'Yia sou' (hello/goodbye casual) or 'Kalimera' (good morning). Eye contact is warm and sustained.",
            "taboos": [
                "The 'moutza' — showing open palm face-first is a serious insult (don't wave with palm out)",
                "Declining food or drink from a host — always accept something",
                "Smoking restrictions are widely ignored; don't expect smoke-free dining",
                "Discussing the Greek debt crisis or economic problems can be sensitive",
                "Flushing toilet paper — many plumbing systems require paper in the bin (check signs)",
                "Photographing military installations"
            ],
            "haggling": "Acceptable in markets and souvenir shops. Not in restaurants or established stores."
        },
        "phrases": [
            {"english": "Hello", "local": "Γεια σου / Γεια σας (Yia sou/Yia sas)", "phonetic": "yah-soo (informal) / yah-sahs (formal)"},
            {"english": "Thank you", "local": "Ευχαριστώ (Efcharistó)", "phonetic": "ef-hah-rees-TOH"},
            {"english": "Excuse me / Sorry", "local": "Συγγνώμη (Signómi)", "phonetic": "seeg-NOH-mee"},
            {"english": "Yes", "local": "Ναι (Nai)", "phonetic": "neh"},
            {"english": "No", "local": "Όχι (Óchi)", "phonetic": "OH-hee"},
            {"english": "Please", "local": "Παρακαλώ (Parakaló)", "phonetic": "pah-rah-kah-LOH"},
            {"english": "How much?", "local": "Πόσο κάνει; (Póso káni?)", "phonetic": "POH-so KAH-nee"},
            {"english": "Where is...?", "local": "Πού είναι...; (Pou ínai?)", "phonetic": "poo EE-neh"},
            {"english": "Help!", "local": "Βοήθεια! (Voítheia!)", "phonetic": "voh-EE-thee-ah"},
            {"english": "Goodbye", "local": "Αντίο / Γεια (Andío / Yia)", "phonetic": "ahn-DEE-oh / yah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Cosmote (best coverage), Vodafone GR, or Wind at airports and phone shops. ~€15-25 for 10-30GB. eSIM via Airalo or Holafly from $5 USD. Coverage on smaller islands can be limited.",
            "wifiAvailability": "Good WiFi in hotels and cafes on main islands and Athens. More limited on smaller islands. Most tavernas offer WiFi. Free WiFi in many central plateia (squares).",
            "bestOption": "Cosmote prepaid SIM for best island and rural coverage. Buy at Athens or Heraklion airport. eSIM from Airalo is a convenient option if your phone supports it."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+30",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period.",
            "timeZone": "UTC+02:00 (EET) / UTC+03:00 (EEST in summer)",
            "bestTimeToVisit": "April-June and September-October for ideal weather, fewer crowds, and lower prices. July-August is peak season (very crowded, extremely hot on islands). Shoulder months offer the best value."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "low",
            "naturalDisasters": ["earthquakes", "wildfires (summer)", "tsunamis (rare)"],
            "lgbtSafety": "Athens and Mykonos are LGBTQ+ friendly with active scenes. Same-sex civil partnerships recognized. More conservative in rural areas and older island communities.",
            "soloFemaleSafety": "Generally safe. Catcalling is common but not typically threatening. Normal precautions at night.",
            "notes": "Very safe overall. Petty crime minimal. Tap water safety varies by island — bottled water recommended on many islands. Check local advice. Protests in Athens (Syntagma Square) can turn disruptive; avoid large gatherings."
        }
    },

    "ID": {
        "cultural": {
            "tipping": "Not obligatory but increasingly expected in tourist areas. 10% at restaurants if not included. Tip tour guides Rp 50,000-100,000/day. Round up taxis or tip Rp 5,000-10,000. Gig drivers (Gojek/Grab): tip in-app.",
            "dressCode": "Conservative dress is important, especially outside Bali's tourist areas. Shoulders and knees covered when visiting temples, mosques, and villages. Sarong and sash required at Bali temples (often provided or rented). Beachwear stays at the beach. In Sumatra and Java, dress modestly.",
            "greetings": "Handshake (right hand only — left is considered unclean). Younger people greeting elders: bow slightly or touch elder's hand to forehead. 'Selamat pagi/siang/sore/malam' (Good morning/afternoon/evening/night). Smile is universal and very important.",
            "taboos": [
                "Using the left hand for giving/receiving anything, eating, or pointing",
                "Pointing with your index finger (use thumb instead)",
                "Touching someone's head (considered sacred)",
                "Entering a temple or home with shoes on",
                "Public displays of affection beyond hand-holding",
                "Disrespecting Islam, local customs, or the Indonesian flag/national anthem"
            ],
            "haggling": "Expected in markets, street stalls, and souvenir shops. Start at 40-50% of the asking price and negotiate to around 60-70%. Not in fixed-price stores or restaurants."
        },
        "phrases": [
            {"english": "Hello", "local": "Halo / Selamat pagi", "phonetic": "hah-loh / seh-lah-maht pah-gee"},
            {"english": "Thank you", "local": "Terima kasih", "phonetic": "teh-ree-mah kah-see"},
            {"english": "Excuse me / Sorry", "local": "Permisi / Maaf", "phonetic": "pehr-mee-see / mah-ahf"},
            {"english": "Yes", "local": "Ya / Iya", "phonetic": "yah / ee-yah"},
            {"english": "No", "local": "Tidak / Enggak", "phonetic": "tee-dahk / eng-gahk"},
            {"english": "Please", "local": "Tolong / Silakan", "phonetic": "toh-long / see-lah-kahn"},
            {"english": "How much?", "local": "Berapa harganya?", "phonetic": "beh-rah-pah har-gah-nyah"},
            {"english": "Where is...?", "local": "Di mana...?", "phonetic": "dee mah-nah"},
            {"english": "Help!", "local": "Tolong!", "phonetic": "toh-long"},
            {"english": "Goodbye", "local": "Selamat tinggal / Sampai jumpa", "phonetic": "seh-lah-maht ting-gahl / sahm-pie joom-pah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Telkomsel (best coverage), XL Axiata, or Indosat Ooredoo at airports and minimarkets (Indomaret, Alfamart). ~Rp 50,000-150,000 for 10-30GB (~$3-10 USD). Registration requires passport. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Good WiFi in Bali's tourist areas and major cities. Quality drops significantly outside tourist zones. Most hotels, cafes, and warung (local restaurants) offer WiFi in Bali, Yogyakarta, and Jakarta.",
            "bestOption": "Telkomsel prepaid SIM for best island-wide coverage, especially outside Bali. Buy at Ngurah Rai (Bali) or Soekarno-Hatta (Jakarta) airport. eSIM from Airalo works well for Bali-focused trips."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+62",
            "visaFreeCountries": "US citizens: 30-day Visa on Arrival ($35 USD) or Bali e-VOA online (recommended). Extendable once for another 30 days. UK and EU citizens: same Visa on Arrival process.",
            "timeZone": "UTC+07:00 (WIB, Sumatra/Java) / UTC+08:00 (WITA, Bali/Lombok) / UTC+09:00 (WIT, Papua)",
            "bestTimeToVisit": "April-October (dry season) for Bali and most of Indonesia. November-March is wet season with heavy rain. Bali's Ubud can be visited year-round."
        },
        "safety": {
            "overallRisk": "medium",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes", "tsunamis", "volcanic eruptions", "flooding", "tropical storms"],
            "lgbtSafety": "Homosexuality is not illegal at the federal level but is banned in Aceh (under Sharia law). Climate is increasingly hostile — avoid public affection. Bali is relatively tolerant but not openly LGBTQ+ friendly.",
            "soloFemaleSafety": "Exercise increased caution. Dress modestly outside tourist areas. Harassment can occur. Avoid traveling alone at night in less-touristed areas.",
            "notes": "Bali is generally safe for tourists. Main concerns are traffic accidents (scooter/motorbike), scams, and petty theft. Indonesia sits on the 'Ring of Fire' — earthquake and tsunami risk is real. Register with your embassy and follow official advice."
        }
    },

    "IT": {
        "cultural": {
            "tipping": "Not obligatory. Restaurants typically add a 'coperto' (cover charge, €1-3/person) — this is not a tip. Leave €1-3 per person for good restaurant service. Cafes: leave small coins. Taxis: round up. Not tipping is not rude.",
            "dressCode": "Italians dress stylishly — looking good is a social obligation. Shorts are fine in coastal/summer areas but avoid them in cities for evening meals. Cover shoulders and knees in churches (strictly enforced — shorts/sleeveless turns people away). Smart casual for restaurants.",
            "greetings": "Two cheek kisses between friends (left first). Handshake in formal/business settings. 'Buongiorno' (morning) and 'Buonasera' (afternoon/evening) — always greet shopkeepers when entering. First-name basis after introduction.",
            "taboos": [
                "Ordering a cappuccino after 11am (locals only have milky coffee in the morning)",
                "Sitting down at a cafe and expecting counter prices (sitting costs more)",
                "Speaking loudly in churches and historic sites",
                "Wearing swimwear away from the beach (fines in many coastal towns)",
                "Putting the bill on the table before it's asked for (waiters wait to be asked)",
                "Expecting ice in drinks (not automatic — ask for 'ghiaccio')"
            ],
            "haggling": "Not common. Acceptable at flea markets (like Porta Portese in Rome). Fixed prices everywhere else."
        },
        "phrases": [
            {"english": "Hello", "local": "Ciao / Buongiorno", "phonetic": "chow / bwon-jor-noh"},
            {"english": "Thank you", "local": "Grazie / Grazie mille", "phonetic": "grat-syeh / grat-syeh meel-leh"},
            {"english": "Excuse me / Sorry", "local": "Scusi / Mi dispiace", "phonetic": "skoo-zee / mee dee-spyah-cheh"},
            {"english": "Yes", "local": "Sì", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "no"},
            {"english": "Please", "local": "Per favore", "phonetic": "pehr fah-voh-reh"},
            {"english": "How much?", "local": "Quanto costa?", "phonetic": "kwahn-toh kos-tah"},
            {"english": "Where is...?", "local": "Dov'è...?", "phonetic": "doh-veh"},
            {"english": "Help!", "local": "Aiuto!", "phonetic": "ah-yoo-toh"},
            {"english": "Goodbye", "local": "Arrivederci / Ciao", "phonetic": "ah-ree-veh-dehr-chee / chow"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from TIM, Vodafone IT, WindTre, or Iliad at airports, tabaccherie (tobacconists), and electronics stores. ~€10-25 for 10-50GB. eSIM via Airalo or Holafly from $5 USD. Note: passport registration required.",
            "wifiAvailability": "Good WiFi in hotels, B&Bs, and cafes. Quality varies — some older hotels have weak signals. Free WiFi in many piazzas and city centers. Trenitalia high-speed trains have WiFi.",
            "bestOption": "Iliad or WindTre prepaid SIM offer excellent value (~€10 for 50-100GB monthly). TIM has best rural coverage. eSIM from Airalo if you prefer digital setup."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F", "L"],
            "voltage": "230V / 50Hz",
            "dialCode": "+39",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period.",
            "timeZone": "UTC+01:00 (CET) / UTC+02:00 (CEST in summer)",
            "bestTimeToVisit": "April-June and September-October for ideal weather and manageable crowds. July-August is peak season (crowded, hot, expensive). Christmas markets in December are lovely. Winter is low season with fewer crowds."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes", "volcanic eruptions (Etna, Stromboli)", "flooding"],
            "lgbtSafety": "Generally tolerant, especially in northern cities. Rome and Milan have active LGBTQ+ scenes. No same-sex marriage (civil unions recognized). More conservative in southern Italy and Sicily.",
            "soloFemaleSafety": "Generally safe. Catcalling common but not typically threatening. Use standard precautions at night. Naples requires more vigilance than northern cities.",
            "notes": "Pickpocketing and bag snatching are the main tourist risks — Rome (Vatican, Colosseum, Termini station), Florence (Duomo, Uffizi), Naples, and Venice. Be vigilant on buses and in crowded tourist areas. Scooter bag snatching is a known tactic in Naples."
        }
    },

    "KR": {
        "cultural": {
            "tipping": "Do not tip. Tipping is not customary and can cause confusion or embarrassment. Service staff take great pride in their work and do not expect additional payment. Quality service is standard, not exceptional.",
            "dressCode": "Koreans dress very smartly — appearance matters significantly. Trendy and fashionable in Seoul's Gangnam and Hongdae areas. Remove shoes when entering homes and some traditional restaurants. Cover up in older neighborhoods and temples.",
            "greetings": "Bow (slight nod for strangers, deeper bow for elders/formal). Handshake in business — use both hands or support the right arm with the left hand. Hierarchy is important — address elders and superiors with respect. Business cards are given/received with both hands and examined carefully.",
            "taboos": [
                "Writing someone's name in red ink (associated with death)",
                "Sticking chopsticks upright in rice (funeral symbolism, same as Japan)",
                "Pointing with index finger (use whole hand instead)",
                "Blowing your nose in public (very impolite)",
                "Eating or drinking while walking in public",
                "Receiving or giving with one hand (use both or support right arm with left)"
            ],
            "haggling": "Not practiced in established shops. Some flexibility at Namdaemun and Dongdaemun markets, but generally prices are fixed."
        },
        "phrases": [
            {"english": "Hello", "local": "안녕하세요 (Annyeonghaseyo)", "phonetic": "ahn-nyung-hah-seh-yoh"},
            {"english": "Thank you", "local": "감사합니다 (Gamsahamnida)", "phonetic": "gahm-sah-hamm-nee-dah"},
            {"english": "Excuse me / Sorry", "local": "죄송합니다 (Joesonghamnida)", "phonetic": "jweh-song-hamm-nee-dah"},
            {"english": "Yes", "local": "네 (Ne)", "phonetic": "neh"},
            {"english": "No", "local": "아니요 (Aniyo)", "phonetic": "ah-nee-yoh"},
            {"english": "Please", "local": "주세요 (Juseyo)", "phonetic": "joo-seh-yoh"},
            {"english": "How much?", "local": "얼마예요? (Eolmayeyo?)", "phonetic": "eol-mah-yeh-yoh"},
            {"english": "Where is...?", "local": "...이/가 어디예요? (...i/ga eodiyeyo?)", "phonetic": "eo-dee-yeh-yoh"},
            {"english": "Help!", "local": "도와주세요! (Dowajuseyo!)", "phonetic": "doh-wah-joo-seh-yoh"},
            {"english": "Goodbye", "local": "안녕히 가세요 (Annyeonghi gaseyo)", "phonetic": "ahn-nyung-hee gah-seh-yoh"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs or rental at Incheon Airport from KT (KollUS), SK Telecom, or LG Uplus. ~$15-40 USD for 7-30 days unlimited. eSIM via Airalo or KT from $8 USD. Korea has some of the world's fastest 5G — coverage is excellent nationwide.",
            "wifiAvailability": "Excellent WiFi everywhere — cafes, restaurants, subway, buses, even most public spaces. Korea is one of the world's most connected countries. Free public WiFi is ubiquitous.",
            "bestOption": "eSIM from KT (Korea Telecom) or Airalo — activate before arrival. Or rent a pocket WiFi at Incheon Airport for groups. Korea's free public WiFi means mobile data is less critical than in most countries."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "220V / 60Hz",
            "dialCode": "+82",
            "visaFreeCountries": "US citizens: 90 days visa-free (K-ETA electronic travel authorization may be required — check current requirements). UK and EU citizens: visa-free entry.",
            "timeZone": "UTC+09:00 (Korea Standard Time, no daylight saving)",
            "bestTimeToVisit": "March-May for cherry blossoms and spring. September-November for autumn foliage and festivals. Avoid July-August (hot, humid, monsoon season) and January-February (very cold)."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "very-low",
            "naturalDisasters": ["typhoons (summer)", "earthquakes (minor)"],
            "lgbtSafety": "Legal but socially conservative. No same-sex partnership recognition. Seoul has a small LGBTQ+ scene in Itaewon. Public displays of affection between same-sex couples may attract attention.",
            "soloFemaleSafety": "Very safe. Seoul and other cities are exceptionally safe for solo female travelers. Women-only options (pink parking spots, safety zones) indicate strong awareness.",
            "notes": "South Korea is one of Asia's safest countries for tourists. The North Korea situation is stable and does not affect tourists in the south. Very low crime, excellent infrastructure, and helpful people. Biggest hazard is traffic and road accidents."
        }
    },

    "MA": {
        "cultural": {
            "tipping": "Expected. Tip restaurant servers 10-15% (rarely added automatically). Tip guides 50-100 MAD/day. Hotel porters 10-20 MAD/bag. Tip anyone who helps you (unofficial parking attendants, people who give directions). Having coins ready is important.",
            "dressCode": "Modest dress essential everywhere — shoulders and knees covered. In cities (Marrakech, Fez, Rabat) dress conservatively but you don't need full cover. Women should especially avoid tight or revealing clothing to minimize harassment. At Sahara camps, looser clothes are also practical. Swimwear at beach resorts only.",
            "greetings": "Right hand to heart after shaking hands is a respectful gesture. Men greet men with handshake (sometimes kiss on cheeks for friends). Men do not initiate physical greeting with women — wait for the woman to extend her hand. 'As-salamu alaykum' (peace be upon you) / response 'Wa alaykum as-salam'.",
            "taboos": [
                "Public displays of affection (illegal technically, and frowned upon even for opposite-sex couples)",
                "Drinking alcohol in public or in front of fasting Muslims during Ramadan",
                "Pointing feet at someone (considered disrespectful)",
                "Photographing people without permission — especially in souks",
                "Wearing revealing clothing outside beach/resort areas",
                "Refusing tea offered by a shopkeeper (very impolite — you don't need to buy)"
            ],
            "haggling": "Essential in souks and markets. Expected. Start at 30-40% of asking price and negotiate. Not in fixed-price shops (look for 'prix fixe' signs). Shopping without haggling means paying tourist prices."
        },
        "phrases": [
            {"english": "Hello", "local": "السلام عليكم / مرحبا (As-salamu alaykum / Marhaba)", "phonetic": "as-sah-lah-moo ah-lay-koom / mar-ha-bah"},
            {"english": "Thank you", "local": "شكراً (Shukran)", "phonetic": "shook-rahn"},
            {"english": "Excuse me / Sorry", "local": "عفواً / آسف (Afwan / Aasif)", "phonetic": "ahf-wahn / ah-seef"},
            {"english": "Yes", "local": "نعم (Na'am) / Ah (Darija)", "phonetic": "nah-am / ah"},
            {"english": "No", "local": "لا (La)", "phonetic": "lah"},
            {"english": "Please", "local": "من فضلك (Min fadlak)", "phonetic": "min fahd-lahk"},
            {"english": "How much?", "local": "بشحال هاد؟ (Bshhal had?) / كم الثمن؟", "phonetic": "besh-hahl had"},
            {"english": "Where is...?", "local": "فين...؟ (Fin...?) / أين...؟", "phonetic": "feen"},
            {"english": "Help!", "local": "ساعدني! (Sa'idni!)", "phonetic": "sah-id-nee"},
            {"english": "Goodbye", "local": "مع السلامة (Ma'a as-salama)", "phonetic": "mah-ah as-sah-lah-mah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Maroc Telecom (best coverage), Orange MA, or Inwi at Mohammed V Airport (Casablanca), Menara Airport (Marrakech), and phone shops. ~$5-15 USD for 5-20GB. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Good WiFi in riads, hotels, and cafes in tourist areas (Marrakech, Fez, Casablanca). More limited in rural Sahara regions. Most restaurants catering to tourists offer WiFi.",
            "bestOption": "Maroc Telecom prepaid SIM for best coverage including the Atlas Mountains and Sahara. Buy at Marrakech or Casablanca airport. eSIM from Airalo is a clean alternative."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["C", "E"],
            "voltage": "220V / 50Hz",
            "dialCode": "+212",
            "visaFreeCountries": "US citizens: 90 days visa-free. UK citizens: 90 days visa-free. EU citizens: visa-free for varying durations.",
            "timeZone": "UTC+01:00 (WET, no summer time change — remains UTC+1 all year since 2019, except during Ramadan when it reverts to UTC+0)",
            "bestTimeToVisit": "March-May and September-November for pleasant temperatures in Marrakech and Fez. December-February in the Sahara. July-August is very hot in inland cities (45°C+). Coastal cities (Essaouira, Agadir) are good year-round."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes", "flooding"],
            "lgbtSafety": "Homosexuality is illegal (up to 3 years in prison under Article 489). LGBTQ+ travelers should exercise extreme discretion. No public displays of affection between same-sex couples.",
            "soloFemaleSafety": "Exercise increased caution. Persistent harassment (verbal, following) is common in medinas. Having a confident demeanor, dressing modestly, and using guided tours reduces issues significantly. Never walk alone in medinas at night.",
            "notes": "Generally safe for tourists but persistent hassle from unofficial guides and touts is exhausting. Hiring a licensed guide in medinas dramatically reduces this. The 2023 earthquake affected the Marrakech/High Atlas region — check current conditions."
        }
    },

    "MX": {
        "cultural": {
            "tipping": "Expected and important — many workers earn minimum wage and depend on tips. 15-20% at sit-down restaurants. Hotel porters $1-2 USD per bag. Tour guides $5-10 USD/day. Taxis: not obligatory but appreciated. Always tip in cash — not on card.",
            "dressCode": "Casual to smart casual in most contexts. Dress modestly when visiting churches (shoulders covered). Resort areas (Cancún, Los Cabos) are very casual. Mexico City restaurants can be quite fashionable.",
            "greetings": "One cheek kiss between women and between men and women. Men shake hands with a warm grip (sometimes patting on the back). Very warm and hospitable. 'Buenos días/tardes/noches' expected. Use titles (Señor/Señora) until told otherwise.",
            "taboos": [
                "Refusing food or drink from a host — very impolite",
                "Discussing politics, religion, or the drug war with strangers",
                "Assuming everyone speaks English (always try 'habla inglés?' first)",
                "Wasting food at someone's home",
                "Drinking tap water (most Mexicans also drink bottled water)",
                "Being overly blunt or critical — indirect communication is preferred"
            ],
            "haggling": "Common at artisan markets, souvenir stalls, and street vendors. Not in established restaurants, shops, or malls. Start at 50-60% of the asking price."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Gracias", "phonetic": "grah-syahs"},
            {"english": "Excuse me / Sorry", "local": "Perdón / Disculpe", "phonetic": "pehr-don / dees-kool-peh"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "no"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto cuesta?", "phonetic": "kwahn-toh kwes-tah"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Ayuda! / ¡Auxilio!", "phonetic": "ah-yoo-dah / owk-see-lyoh"},
            {"english": "Goodbye", "local": "Adiós / Hasta luego", "phonetic": "ah-dyos / as-tah lweh-go"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Telcel (best coverage) or AT&T Mexico at airports and OXXO convenience stores. ~$15-25 USD for 5-20GB. eSIM via Airalo or Holafly from $5 USD. Telcel has the widest rural coverage.",
            "wifiAvailability": "Good WiFi in hotels, hostels, and cafes in tourist areas. Less reliable in rural areas and small towns. OXXO convenience stores often have WiFi. Most airports have free WiFi.",
            "bestOption": "Telcel prepaid SIM from OXXO or airport for best coverage. eSIM from Airalo is convenient for Cancún, Mexico City, or resort-based trips."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["A", "B"],
            "voltage": "127V / 60Hz",
            "dialCode": "+52",
            "visaFreeCountries": "US citizens: 180 days visa-free (tourist card/FMM included with entry). UK and EU citizens: 180 days visa-free.",
            "timeZone": "UTC-6 to UTC-8 (varies by state; most of Mexico is CST/UTC-6, Baja California is UTC-8)",
            "bestTimeToVisit": "December-April (dry season) for most regions. Avoid June-October hurricane season on Caribbean/Pacific coasts. Mexico City is good year-round. Día de los Muertos (Oct 31-Nov 2) is a spectacular cultural event."
        },
        "safety": {
            "overallRisk": "medium",
            "violentCrime": "medium",
            "pettyCrime": "high",
            "naturalDisasters": ["earthquakes", "hurricanes", "tropical storms", "volcanic activity (Popocatépetl)"],
            "lgbtSafety": "Mexico City and Guadalajara are LGBTQ+ friendly with active scenes. Puerto Vallarta is one of Latin America's most LGBTQ+ welcoming resorts. Same-sex marriage legal nationwide. More conservative in rural areas.",
            "soloFemaleSafety": "Exercise increased caution. Tourist areas are generally safe during the day. Avoid traveling alone at night in unknown areas. Use Uber or official taxis. Femicide rates are high nationally — research specific areas carefully.",
            "notes": "Tourist areas (Cancún, Cabo, Puerto Vallarta, Oaxaca, Mexico City tourist zones) are generally safe. The US State Department issues level-3/4 advisories for several states (Colima, Guerrero, Michoacán, Tamaulipas). Research your specific destination carefully. Never rent a car and drive at night in unfamiliar areas."
        }
    },

    "NZ": {
        "cultural": {
            "tipping": "Not expected or standard. New Zealanders (Kiwis) don't tip as a general rule — wages are regulated and service is not tip-dependent. In upscale restaurants, rounding up or leaving a small tip is appreciated but never obligatory.",
            "dressCode": "Very casual. Outdoorsy attire is totally normal. Smart casual for city restaurants. Māori cultural sites (marae) require removing shoes — follow the lead of your host. Sun protection is essential (NZ has high UV due to ozone thinning).",
            "greetings": "Handshake on first meeting. Māori greeting: hongi (pressing noses together) for formal cultural occasions — wait for the host to initiate. Very informal and friendly — 'Hey' or first name immediately. Warm smiles are standard.",
            "taboos": [
                "Mocking or appropriating Māori culture (haka, tā moko tattoos, etc.)",
                "Leaving any rubbish in nature — NZ takes environment seriously",
                "Disturbing wildlife (especially kiwi and endangered birds)",
                "Assuming NZ and Australia are the same (both countries bristle at this)",
                "Walking on sacred sites or climbing rocks without permission (some areas are tapu/sacred)",
                "Bringing undeclared food, plant material, or soil through biosecurity"
            ],
            "haggling": "Not practiced. Prices are fixed."
        },
        "phrases": [
            {"english": "Hello", "local": "Kia ora (Māori) / Hello", "phonetic": "kee-ah oh-rah"},
            {"english": "Thank you", "local": "Ngā mihi (Māori) / Thank you", "phonetic": "ngah mee-hee"},
            {"english": "Excuse me / Sorry", "local": "Sorry / Excuse me", "phonetic": "sor-ee"},
            {"english": "Yes", "local": "Āe (Māori) / Yeah / Yes", "phonetic": "ah-eh / yeh"},
            {"english": "No", "local": "Kāo (Māori) / No", "phonetic": "kah-oh / no"},
            {"english": "Please", "local": "Please", "phonetic": "pleez"},
            {"english": "How much?", "local": "How much is it?", "phonetic": "how much iz it"},
            {"english": "Where is...?", "local": "Where is...? / Kei hea...? (Māori)", "phonetic": "keh heh-ah"},
            {"english": "Help!", "local": "Help! / Āwhina! (Māori)", "phonetic": "help / ah-fee-nah"},
            {"english": "Goodbye", "local": "Ka kite anō (Māori) / See ya", "phonetic": "kah-kee-teh ah-noh"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Spark (best rural coverage), One NZ (formerly Vodafone), or 2degrees at Auckland/Christchurch airports and supermarkets. ~NZ$25-50 for 10-30GB. eSIM via Airalo or Holafly from $8 USD.",
            "wifiAvailability": "Good WiFi in cities, towns, and tourist areas. Remote areas (Fiordland, Milford Sound, Coromandel) have very limited connectivity. Most accommodation and cafes offer WiFi.",
            "bestOption": "Spark prepaid SIM for widest coverage including rural and national park areas. Buy at Auckland or Queenstown airport. eSIM from Airalo is an easy pre-arrival option."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "left",
            "plugType": ["I"],
            "voltage": "230V / 50Hz",
            "dialCode": "+64",
            "visaFreeCountries": "US citizens: NZeTA (New Zealand Electronic Travel Authority) required — ~NZ$23, applied online. UK and EU citizens: also require NZeTA.",
            "timeZone": "UTC+12:00 (NZST) / UTC+13:00 (NZDT in summer)",
            "bestTimeToVisit": "December-February (Austral summer) for warmest weather, outdoor activities. March-May is mild with fewer crowds. June-August is winter — ski season in South Island (Queenstown). Avoid school holidays for lower prices."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "low",
            "naturalDisasters": ["earthquakes", "volcanic eruptions (White Island/Whakaari — ongoing risk)", "tsunamis", "flooding"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2013. Wellington and Auckland have active LGBTQ+ scenes. Hero Festival in Auckland is a major event.",
            "soloFemaleSafety": "Very safe. Standard precautions apply. Very relaxed and friendly culture.",
            "notes": "One of the world's safest and friendliest countries. Main risks are environmental — UV radiation, road conditions (driving on left side can be challenging), and natural hazards. Whakaari/White Island erupted in 2019 — check current access status before visiting."
        }
    },

    "PE": {
        "cultural": {
            "tipping": "10% at restaurants is standard (sometimes added as 'propina' but check the bill). Tip tour guides $10-20 USD/day for multi-day treks (Inca Trail porters also deserve tips — $20-30 USD/day is recommended). Taxi drivers: round up.",
            "dressCode": "Casual in Lima and tourist towns. Layers essential for Andean altitudes (cold mornings and nights even in summer). Respectful dress at Andean communities and ruins. Comfortable, breathable clothing for jungle (Iquitos, Manu).",
            "greetings": "One cheek kiss between women and between men and women (in social settings). Handshake in business. 'Buenos días/tardes/noches' always. Warm and hospitable. Personal space is closer than Northern Europe/North America.",
            "taboos": [
                "Disrespecting Inca/Quechua heritage sites — touching, climbing, or defacing ruins",
                "Taking photographs at Andean communities without permission",
                "Altitude sickness (soroche) — don't ignore symptoms; rest and acclimatize before exertion",
                "Drinking tap water",
                "Displaying expensive electronics in public, especially in Lima's Miraflores/Barranco",
                "Littering — Peruvians take pride in natural sites"
            ],
            "haggling": "Expected at artisan markets (Pisac, Otavalo, San Pedro). Not in restaurants, established shops, or for trekking services. Start at 50-60% of asking price."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola / Napaykullayki (Quechua)", "phonetic": "oh-lah / nah-pie-koo-yay-kee"},
            {"english": "Thank you", "local": "Gracias / Sulpayki (Quechua)", "phonetic": "grah-syahs / sool-pie-kee"},
            {"english": "Excuse me / Sorry", "local": "Disculpa / Perdón", "phonetic": "dees-kool-pah / pehr-don"},
            {"english": "Yes", "local": "Sí / Arí (Quechua)", "phonetic": "see / ah-ree"},
            {"english": "No", "local": "No / Mana (Quechua)", "phonetic": "no / mah-nah"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto cuesta?", "phonetic": "kwahn-toh kwes-tah"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Ayuda! / ¡Auxilio!", "phonetic": "ah-yoo-dah"},
            {"english": "Goodbye", "local": "Adiós / Tinkunanchiskama (Quechua)", "phonetic": "ah-dyos / teen-koo-nahn-chees-kah-mah"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Claro PE (best coverage including Andes), Entel, or Movistar at Lima airport and phone shops. ~$10-20 USD for 5-15GB. eSIM via Airalo or Holafly from $5 USD. Coverage is very limited in the Amazon jungle and remote Andean areas.",
            "wifiAvailability": "Good WiFi in Lima (Miraflores, Barranco), Cusco, and most tourist town hotels and cafes. Very limited in remote areas (Machu Picchu town has WiFi, trail does not).",
            "bestOption": "Claro Peru prepaid SIM for widest Andean and national coverage. Buy at Jorge Chávez International Airport (Lima). eSIM from Airalo if you want to set up before arriving."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["A", "B", "C"],
            "voltage": "220V / 60Hz",
            "dialCode": "+51",
            "visaFreeCountries": "US citizens: 90 days visa-free (tourist entry). UK and EU citizens: visa-free for 90 days.",
            "timeZone": "UTC-05:00 (Peru Standard Time, no daylight saving)",
            "bestTimeToVisit": "May-September (dry season) for Cusco, Machu Picchu, and the Inca Trail. June-August is peak season. October-April is the wet season in the Andes (Machu Picchu can still be visited). Lima is gray/overcast May-November (garúa season)."
        },
        "safety": {
            "overallRisk": "medium",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes", "flooding", "landslides", "altitude sickness"],
            "lgbtSafety": "Legal and increasingly tolerated in Lima. No same-sex marriage recognition. More conservative in Andean and rural communities. Lima has a growing LGBTQ+ scene.",
            "soloFemaleSafety": "Exercise increased caution. Solo female travel is common on the tourist circuit but requires vigilance. Avoid walking alone at night. Take taxis to and from bus stations.",
            "notes": "Altitude sickness is a real risk in Cusco (3,400m) and Machu Picchu — spend 1-2 days acclimatizing in Cusco before trekking. Petty theft is the main crime concern in Lima and Cusco. The Inca Trail requires advance booking (permits sell out months ahead)."
        }
    },

    "PT": {
        "cultural": {
            "tipping": "Not obligatory but appreciated. Leave 5-10% at restaurants for good service (service is not automatically included). Cafes: leave small coins. Taxi drivers: round up. Portugal has lower tipping expectations than Spain or France.",
            "dressCode": "Casual to smart casual. Cover up for churches (shoulders and knees). Lisbon and Porto are fashionable cities but not snobbish about dress. Practical clothing for hills (Lisbon is famously hilly — comfortable shoes essential).",
            "greetings": "Handshake on first meeting. Friends exchange two cheek kisses (right first). Very warm and welcoming — Portuguese are known for saudade (a melancholic warmth). 'Bom dia/Boa tarde/Boa noite' always appreciated.",
            "taboos": [
                "Confusing Portugal with Spain (or assuming it's similar) — culturally distinct",
                "Assuming everyone speaks Spanish (Portuguese is different — they speak Portuguese)",
                "Not acknowledging saudade — the Portuguese are proud of this cultural concept",
                "Speaking too loudly (Portuguese culture values modesty and discretion)",
                "Rushing through a pastel de nata — these must be savored",
                "Leaving food on your plate at someone's home (seen as insulting the cook)"
            ],
            "haggling": "Not practiced in shops or restaurants. Some flexibility at antique markets and flea markets (Feira da Ladra in Lisbon)."
        },
        "phrases": [
            {"english": "Hello", "local": "Olá / Bom dia", "phonetic": "oh-LAH / bom-JEE-ah"},
            {"english": "Thank you", "local": "Obrigado (m) / Obrigada (f)", "phonetic": "oh-bree-GAH-doo / oh-bree-GAH-dah"},
            {"english": "Excuse me / Sorry", "local": "Com licença / Desculpe", "phonetic": "kom lee-SEN-sah / desh-KOOL-peh"},
            {"english": "Yes", "local": "Sim", "phonetic": "seem"},
            {"english": "No", "local": "Não", "phonetic": "nowng"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-VOR"},
            {"english": "How much?", "local": "Quanto custa?", "phonetic": "KWAHN-too KOOS-tah"},
            {"english": "Where is...?", "local": "Onde fica...?", "phonetic": "ON-deh FEE-kah"},
            {"english": "Help!", "local": "Socorro!", "phonetic": "so-KOH-roo"},
            {"english": "Goodbye", "local": "Adeus / Até logo", "phonetic": "ah-DAY-oosh / ah-TEH LOH-goh"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from NOS (best coverage), MEO, or Vodafone PT at airports, post offices (CTT), and phone shops. ~€10-20 for 10-25GB. eSIM via Airalo or Holafly from $5 USD.",
            "wifiAvailability": "Excellent WiFi in Lisbon, Porto, and Algarve hotels and cafes. Good coverage in most tourist areas. Free public WiFi in many city centers and plazas.",
            "bestOption": "NOS or MEO prepaid SIM for widest national coverage. Buy at Lisbon Humberto Delgado Airport or at any CTT post office. eSIM from Airalo is a convenient pre-arrival option."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+351",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen zone). UK citizens: 90 days in any 180-day period.",
            "timeZone": "UTC+00:00 (WET) / UTC+01:00 (WEST in summer) — same as UK/Ireland",
            "bestTimeToVisit": "April-October for warm, sunny weather. June-August is peak season and crowded. May and September offer ideal weather with fewer tourists. Madeira and Azores are worth visiting year-round."
        },
        "safety": {
            "overallRisk": "very-low",
            "violentCrime": "very-low",
            "pettyCrime": "low",
            "naturalDisasters": ["wildfires (summer)", "earthquakes (rare)", "flooding"],
            "lgbtSafety": "Very LGBTQ+ friendly. Same-sex marriage legal since 2010. Lisbon and Porto have active LGBTQ+ scenes. Lisbon Pride is one of Europe's largest. Very welcoming overall.",
            "soloFemaleSafety": "Very safe. One of Europe's safest countries for solo female travelers.",
            "notes": "Portugal consistently ranks among Europe's safest countries. Petty crime (pickpocketing) is the main concern in Lisbon's tourist areas (Alfama, Baixa, Bairro Alto nightlife). Standard vigilance in crowded areas. Wildfires are a risk in rural areas in summer."
        }
    },

    "TR": {
        "cultural": {
            "tipping": "Expected but not as high as in the US. Leave 10-15% at restaurants (rarely included). Tip tour guides 50-100 TRY/hour or $5-10 USD/day. Hotel porters 20-30 TRY/bag. Tip hammam attendants. Always tip in cash.",
            "dressCode": "Cover shoulders and knees for mosques — head scarves provided for women at major mosques. Dress modestly in conservative towns and rural areas. Istanbul and coastal resorts are more relaxed. Remove shoes when entering mosques and homes.",
            "greetings": "Handshake, sometimes with left hand placed on heart for warmth. Men may kiss cheeks with close friends. 'Merhaba' (hello) or 'Günaydın/İyi günler/İyi akşamlar' (good morning/day/evening). Very hospitable — expect offers of tea (çay). Accepting tea is polite.",
            "taboos": [
                "Insulting the Turkish flag, Atatürk, or Turkish national identity (illegal under Penal Code Article 301)",
                "Discussing the Kurdish issue or Armenian history with strangers",
                "Public displays of affection beyond hand-holding (frowned upon outside Istanbul)",
                "Showing the soles of your feet to someone",
                "Refusing hospitality (tea, food) without a good excuse",
                "Wearing shoes inside mosques or homes"
            ],
            "haggling": "Expected and enjoyable at bazaars (Grand Bazaar, Spice Bazaar, local markets). Start at 40-50% of asking price. Not in regular shops, restaurants, or modern stores. Drinking tea during negotiations is part of the culture."
        },
        "phrases": [
            {"english": "Hello", "local": "Merhaba", "phonetic": "mehr-hah-bah"},
            {"english": "Thank you", "local": "Teşekkür ederim", "phonetic": "teh-shek-kur eh-deh-reem"},
            {"english": "Excuse me / Sorry", "local": "Affedersiniz / Özür dilerim", "phonetic": "ahf-feh-dehr-see-neez / ur-zur dee-leh-reem"},
            {"english": "Yes", "local": "Evet", "phonetic": "eh-vet"},
            {"english": "No", "local": "Hayır", "phonetic": "hah-yuhr"},
            {"english": "Please", "local": "Lütfen", "phonetic": "lut-fen"},
            {"english": "How much?", "local": "Ne kadar?", "phonetic": "neh kah-dahr"},
            {"english": "Where is...?", "local": "...nerede?", "phonetic": "neh-reh-deh"},
            {"english": "Help!", "local": "İmdat! / Yardım!", "phonetic": "eem-daht / yahr-duhm"},
            {"english": "Goodbye", "local": "Güle güle / Hoşça kal", "phonetic": "goo-leh goo-leh / hosh-chah kahl"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Turkcell (best coverage), Vodafone TR, or Türk Telekom at Istanbul Atatürk/Sabiha Gökçen airports and phone shops. Tourist SIMs ~$15-30 USD for 10-20GB. Note: SIM registration requires passport and your phone's IMEI may need to be registered — check requirements. eSIM via Airalo from $5 USD.",
            "wifiAvailability": "Good WiFi in Istanbul hotels, cafes, and restaurants. Widespread free WiFi in tourist areas. Major transport hubs have WiFi. Quality can vary — hotel WiFi is generally better than cafe WiFi.",
            "bestOption": "eSIM via Airalo avoids the SIM registration complications. Alternatively, Turkcell tourist SIM from the airport (~$20 USD for 20GB) offers the best coverage including Cappadocia and coastal areas."
        },
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+90",
            "visaFreeCountries": "US citizens: e-Visa required before travel (~$50 USD, applied online at evisa.gov.tr). UK citizens: also require e-Visa. EU citizens: most can enter visa-free for 90 days.",
            "timeZone": "UTC+03:00 (Turkey Time — no daylight saving since 2016)",
            "bestTimeToVisit": "April-June and September-November for Istanbul and Cappadocia. Coastal areas (Aegean/Mediterranean) are best May-October. July-August is very hot and crowded. Avoid major holidays (Eid/Kurban Bayramı) for domestic travel."
        },
        "safety": {
            "overallRisk": "medium",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["earthquakes (significant seismic zone)", "flooding"],
            "lgbtSafety": "Homosexuality is legal but not recognized. Istanbul Pride has been banned since 2015. Public attitudes have become more conservative in recent years. Discretion advised outside of specific tolerant areas in Istanbul.",
            "soloFemaleSafety": "Exercise increased caution. Harassment is common in tourist areas and bazaars. Dressing modestly and projecting confidence helps. Avoid solo travel at night in less-touristed areas.",
            "notes": "Turkey experienced major earthquakes in February 2023 (southeastern Turkey). Istanbul is generally safe for tourists. Petty theft in Grand Bazaar and tourist areas is common. Follow US/UK State Department advice for southeastern regions near the Syrian border."
        }
    },

    "VN": {
        "cultural": {
            "tipping": "Not traditional but increasingly appreciated in tourist areas. Leave 10-15% at tourist restaurants and bars in Hanoi/Ho Chi Minh City (rarely automatic). Tip tour guides 50,000-100,000 VND/day. Round up taxi fares. Hotel porters: 20,000-50,000 VND.",
            "dressCode": "Modest and conservative, especially in central Vietnam (Hue, Hoi An). Cover shoulders and knees at temples and pagodas. Lightweight, breathable clothing essential for heat/humidity. Long trousers preferred in rural areas.",
            "greetings": "Slight bow with hands together (Buddhist greeting). Handshake acceptable for men in business. Women may not initiate handshake. 'Xin chào' (hello) is universal. Vietnamese is tonal — locals appreciate any attempt. Offer business cards with both hands.",
            "taboos": [
                "Touching someone's head (sacred)",
                "Pointing with index finger (point with whole hand)",
                "Losing your temper or showing anger publicly (extreme loss of face)",
                "Patting a child on the head",
                "Taking photographs of military installations",
                "Wearing shoes inside temples, pagodas, and traditional homes"
            ],
            "haggling": "Expected and part of the culture at markets, street vendors, and souvenir shops. Start at 50-60% of asking price. Agree on taxi fares before getting in (or insist on the meter). Not in restaurants or fixed-price stores."
        },
        "phrases": [
            {"english": "Hello", "local": "Xin chào", "phonetic": "seen chow"},
            {"english": "Thank you", "local": "Cảm ơn", "phonetic": "gahm uhn"},
            {"english": "Excuse me / Sorry", "local": "Xin lỗi", "phonetic": "seen loy"},
            {"english": "Yes", "local": "Vâng / Có", "phonetic": "vuhng / gaw"},
            {"english": "No", "local": "Không", "phonetic": "khong"},
            {"english": "Please", "local": "Làm ơn", "phonetic": "lahm uhn"},
            {"english": "How much?", "local": "Bao nhiêu tiền?", "phonetic": "bow nyew tyen"},
            {"english": "Where is...?", "local": "...ở đâu?", "phonetic": "uh dow"},
            {"english": "Help!", "local": "Cứu tôi với!", "phonetic": "kuu toy voy"},
            {"english": "Goodbye", "local": "Tạm biệt / Chào", "phonetic": "tahm byet / chow"}
        ],
        "connectivity": {
            "simOptions": "Prepaid SIMs from Viettel (best coverage), Vinaphone, or Mobifone at airports and convenience stores. ~100,000-200,000 VND for 5-20GB (~$4-8 USD). eSIM via Airalo or Holafly from $4 USD. Registration requires passport.",
            "wifiAvailability": "Excellent WiFi in hotels, cafes, and restaurants throughout Vietnam. Vietnam has very fast internet speeds. Free WiFi at most coffee shops (Vietnam has a famous cafe culture).",
            "bestOption": "Viettel prepaid SIM for best national coverage including rural areas. Buy at Noi Bai (Hanoi) or Tan Son Nhat (Ho Chi Minh City) airport. eSIM from Airalo is excellent for Vietnam."
        },
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["A", "C"],
            "voltage": "220V / 50Hz",
            "dialCode": "+84",
            "visaFreeCountries": "US citizens: e-Visa required ($25 USD, 90 days, multiple entry). UK citizens: 45-day visa exemption. EU citizens: visa exemption varies by country (France, Germany, Italy: 45 days free).",
            "timeZone": "UTC+07:00 (Indochina Time, no daylight saving)",
            "bestTimeToVisit": "October-April for Ho Chi Minh City and Mekong Delta (south). February-April for Central Vietnam (Hoi An, Hue). October-December for Hanoi and northern highlands. Vietnam's diverse climate means there's always somewhere good to visit."
        },
        "safety": {
            "overallRisk": "low",
            "violentCrime": "low",
            "pettyCrime": "medium",
            "naturalDisasters": ["typhoons (central Vietnam, Oct-Dec)", "flooding", "earthquakes (minor)"],
            "lgbtSafety": "Relatively tolerant by regional standards. Homosexuality is not illegal. No same-sex marriage recognition. Ho Chi Minh City has a growing LGBTQ+ scene. More conservative in rural/northern areas.",
            "soloFemaleSafety": "Generally safe. Bag snatching by motorbike is a known risk in Ho Chi Minh City — hold bags away from the road. Use grab (rideshare app) rather than flagging taxis.",
            "notes": "Traffic is the biggest safety hazard — road accidents are common. Cross the street slowly and steadily — motorbikes will flow around you. Bag snatching by motorbike is common in HCMC. Scams in tourist areas (overcharging, fake tours) require vigilance. Use official taxis (Vinasun, Mai Linh) or Grab app."
        }
    },
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def enrich_profile(iso2):
    path = SAFETY_DIR / f"{iso2.lower()}.json"
    if not path.exists():
        print(f"  ⚠️  {iso2}: file not found at {path}")
        return False

    profile = load_json(path)
    data = ENRICHMENT[iso2]

    # Cultural
    if "cultural" in data:
        c = data["cultural"]
        profile["cultural"]["tipping"] = c.get("tipping")
        profile["cultural"]["dressCode"] = c.get("dressCode")
        profile["cultural"]["greetings"] = c.get("greetings")
        profile["cultural"]["taboos"] = c.get("taboos", [])
        profile["cultural"]["haggling"] = c.get("haggling")

    # Phrases
    if "phrases" in data:
        profile["phrases"] = data["phrases"]

    # Connectivity
    if "connectivity" in data:
        profile["connectivity"]["simOptions"] = data["connectivity"].get("simOptions")
        profile["connectivity"]["wifiAvailability"] = data["connectivity"].get("wifiAvailability")
        profile["connectivity"]["bestOption"] = data["connectivity"].get("bestOption")

    # Practical
    if "practical" in data:
        p = data["practical"]
        profile["practical"]["tapWater"] = p.get("tapWater", profile["practical"].get("tapWater"))
        profile["practical"]["drivingSide"] = p.get("drivingSide")
        profile["practical"]["plugType"] = p.get("plugType", [])
        profile["practical"]["voltage"] = p.get("voltage")
        profile["practical"]["dialCode"] = p.get("dialCode")
        profile["practical"]["visaFreeCountries"] = p.get("visaFreeCountries")
        profile["practical"]["timeZone"] = p.get("timeZone")
        profile["practical"]["bestTimeToVisit"] = p.get("bestTimeToVisit")

    # Safety
    if "safety" in data:
        s = data["safety"]
        profile["safety"]["overallRisk"] = s.get("overallRisk")
        profile["safety"]["violentCrime"] = s.get("violentCrime")
        profile["safety"]["pettyCrime"] = s.get("pettyCrime")
        profile["safety"]["naturalDisasters"] = s.get("naturalDisasters", [])
        profile["safety"]["lgbtSafety"] = s.get("lgbtSafety")
        profile["safety"]["soloFemaleSafety"] = s.get("soloFemaleSafety")
        profile["safety"]["notes"] = s.get("notes")

    profile["lastUpdated"] = TODAY
    save_json(path, profile)
    return True


def main():
    print("Enriching 18 safety profiles...")
    enriched = []
    skipped = []
    for iso2 in ENRICHMENT:
        print(f"  ✍️  {iso2}...")
        if enrich_profile(iso2):
            enriched.append(iso2)
        else:
            skipped.append(iso2)

    print(f"\n✅ Enriched {len(enriched)} profiles: {', '.join(enriched)}")
    if skipped:
        print(f"⚠️  Skipped {len(skipped)}: {', '.join(skipped)}")
    print(f"\nOutput: {SAFETY_DIR}")


if __name__ == "__main__":
    main()
