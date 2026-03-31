#!/usr/bin/env python3
"""
Build 20 new safety profiles for expanded country coverage.
Does NOT modify existing 20 profiles.

Output: app/data/safety/{iso2_lower}.json

Usage: python3 app/scripts/build-expanded-profiles.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install beautifulsoup4", file=sys.stderr)
    raise SystemExit(1)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
SAFETY_DIR = DATA_DIR / "safety"
HEALTH_DIR = BASE_DIR / "health"
SCAMS_DIR = BASE_DIR / "scams"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Country data ─────────────────────────────────────────────────────────────

COUNTRIES = {
    "CN": {
        "name": "China",
        "health_slug": "china",
        "scam_cities": ["beijing", "shanghai"],
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["A", "C", "I"],
            "voltage": "220V / 50Hz",
            "dialCode": "+86",
            "visaFreeCountries": "US citizens: visa required. Transit visa-free for 144h in select cities. Most Western nationals need a visa.",
            "timeZone": "UTC+08:00",
            "bestTimeToVisit": "March-May (spring) and September-November (autumn). Avoid Chinese New Year (late Jan/Feb) and Golden Week (Oct 1-7) — extreme crowds."
        },
        "cultural": {
            "tipping": "Not expected and not customary. Some high-end international hotels may accept tips. Taxi drivers do not expect tips.",
            "dressCode": "Modest dress at temples and religious sites. Cover shoulders and knees. Business settings are formal. Casual dress is fine in cities.",
            "greetings": "Handshake is common in business. Slight nod for casual greetings. Address people by title + surname. Business cards exchanged with both hands.",
            "taboos": [
                "Sticking chopsticks upright in rice (funeral symbolism)",
                "Writing names in red ink (associated with death)",
                "Giving clocks as gifts (sounds like 'attending a funeral')",
                "The number 4 (sounds like 'death')",
                "Discussing Taiwan, Tibet, or Tiananmen Square politics"
            ],
            "haggling": "Expected at markets, street vendors, and some small shops. Not at department stores, malls, or restaurants. Start at 30-50% of asking price."
        },
        "connectivity": {
            "simOptions": "Foreign SIM cards and eSIMs work for calls/data but cannot access Google, Facebook, Instagram, WhatsApp without VPN. China Unicom or China Mobile tourist SIMs at airports.",
            "wifiAvailability": "Free WiFi at hotels, cafes, and airports but often requires Chinese phone number for registration. Many Western services are blocked.",
            "bestOption": "Get a VPN before arriving (download in advance — VPN apps blocked in China). eSIM with roaming from Airalo or Holafly bypasses the firewall via foreign routing."
        },
        "phrases": [
            {"english": "Hello", "local": "你好 (Nǐ hǎo)", "phonetic": "nee how"},
            {"english": "Thank you", "local": "谢谢 (Xièxiè)", "phonetic": "syeh-syeh"},
            {"english": "Excuse me / Sorry", "local": "对不起 (Duìbùqǐ)", "phonetic": "dway-boo-chee"},
            {"english": "Yes", "local": "是 (Shì)", "phonetic": "shuh"},
            {"english": "No", "local": "不是 (Bù shì)", "phonetic": "boo shuh"},
            {"english": "Please", "local": "请 (Qǐng)", "phonetic": "ching"},
            {"english": "How much?", "local": "多少钱？(Duōshǎo qián?)", "phonetic": "dwoh-shaow chyen"},
            {"english": "Where is...?", "local": "...在哪里？(... zài nǎlǐ?)", "phonetic": "dzai nah-lee"},
            {"english": "Help!", "local": "救命！(Jiùmìng!)", "phonetic": "jyoh-ming"},
            {"english": "Goodbye", "local": "再见 (Zàijiàn)", "phonetic": "dzai-jyen"}
        ]
    },
    "IN": {
        "name": "India",
        "health_slug": "india",
        "scam_cities": ["delhi", "mumbai", "jaipur"],
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["C", "D", "M"],
            "voltage": "230V / 50Hz",
            "dialCode": "+91",
            "visaFreeCountries": "US citizens: e-Visa available (30-day, 1-year, or 5-year). Apply online before travel. Most Western nationals eligible for e-Visa.",
            "timeZone": "UTC+05:30",
            "bestTimeToVisit": "October-March (cool, dry season). Avoid April-June (extreme heat 40°C+) and July-September (monsoon). Hill stations are pleasant in summer."
        },
        "cultural": {
            "tipping": "10-15% at restaurants if no service charge. Round up for taxis. Rs 20-50 for hotel porters. Tip tour guides Rs 200-500/day.",
            "dressCode": "Cover shoulders and knees at temples and religious sites. Remove shoes before entering temples, mosques, and homes. Women should carry a scarf for covering head at Sikh gurudwaras.",
            "greetings": "Namaste (palms together, slight bow) is the universal greeting. Handshakes common in business but avoid with opposite gender unless initiated. Use right hand for eating and passing items.",
            "taboos": [
                "Touching someone's head (considered sacred)",
                "Pointing feet at people or religious objects",
                "Using left hand for eating or passing items (considered unclean)",
                "Public displays of affection",
                "Wearing shoes inside temples or homes",
                "Eating beef in Hindu areas or pork in Muslim areas"
            ],
            "haggling": "Expected and enjoyed at markets, auto-rickshaws, and street vendors. Not at fixed-price shops or malls. Start at 40-50% of asking price."
        },
        "connectivity": {
            "simOptions": "Jio or Airtel tourist SIM at airport counters (passport + photo required, takes 1-24h to activate). Prepaid plans very cheap — unlimited data for $3-5/month.",
            "wifiAvailability": "Free WiFi at most hotels and many cafes. Airport WiFi requires Indian phone number for OTP. Quality varies widely outside cities.",
            "bestOption": "Airtel or Jio prepaid SIM for best coverage. Activation can take hours — buy at airport immediately on arrival. eSIM via Airalo as backup while local SIM activates."
        },
        "phrases": [
            {"english": "Hello", "local": "नमस्ते (Namaste)", "phonetic": "nah-mah-stay"},
            {"english": "Thank you", "local": "धन्यवाद (Dhanyavaad)", "phonetic": "dhun-yah-vaad"},
            {"english": "Excuse me / Sorry", "local": "माफ़ कीजिए (Maaf kījie)", "phonetic": "mahf kee-jee-yeh"},
            {"english": "Yes", "local": "हाँ (Haan)", "phonetic": "hahn"},
            {"english": "No", "local": "नहीं (Nahīn)", "phonetic": "nuh-heen"},
            {"english": "Please", "local": "कृपया (Kripaya)", "phonetic": "krip-ah-yah"},
            {"english": "How much?", "local": "कितना? (Kitna?)", "phonetic": "kit-nah"},
            {"english": "Where is...?", "local": "...कहाँ है? (... kahān hai?)", "phonetic": "kuh-hahn hai"},
            {"english": "Help!", "local": "मदद! (Madad!)", "phonetic": "muh-dud"},
            {"english": "Goodbye", "local": "अलविदा (Alvida)", "phonetic": "al-vee-dah"}
        ]
    },
    "US": {
        "name": "United States",
        "health_slug": "united-states",
        "scam_cities": ["new-york", "los-angeles", "miami"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["A", "B"],
            "voltage": "120V / 60Hz",
            "dialCode": "+1",
            "visaFreeCountries": "VWP (Visa Waiver Program) for 40 countries including UK, EU, Japan, Australia, South Korea — ESTA required. Others need B1/B2 visa.",
            "timeZone": "UTC-05:00 to UTC-10:00 (multiple zones)",
            "bestTimeToVisit": "Varies by region. Northeast/Midwest: May-October. Southwest: March-May, September-November. Florida: November-April. National parks: shoulder seasons."
        },
        "cultural": {
            "tipping": "Expected everywhere. 18-20% at restaurants, $1-2 per drink at bars, 15-20% for taxis, $2-5/night for hotel housekeeping. Not tipping is considered rude.",
            "dressCode": "Generally casual. Smart casual for nice restaurants. No specific religious dress codes but some venues have dress codes (no flip-flops, etc.).",
            "greetings": "Handshake and eye contact. 'Hi' or 'How are you?' (rhetorical — just say 'Good, thanks'). First names used quickly even in business.",
            "taboos": [
                "Cutting in line (taken very seriously)",
                "Not tipping service workers",
                "Discussing salary or asking someone's age/weight",
                "Standing too close during conversation (arm's length)",
                "Smoking indoors (banned almost everywhere)"
            ],
            "haggling": "Not practiced at stores or restaurants. Acceptable at flea markets, car dealerships, and private sales."
        },
        "connectivity": {
            "simOptions": "T-Mobile, AT&T, or Mint Mobile prepaid SIMs at airport shops or Best Buy. eSIM via T-Mobile, Airalo, or Holafly. Walmart Family Mobile for budget option.",
            "wifiAvailability": "Free WiFi at most cafes (Starbucks, etc.), hotels, airports, and many public libraries. Cell coverage excellent in cities, spotty in rural/mountain areas.",
            "bestOption": "T-Mobile prepaid or eSIM for best coverage. If short visit, Airalo eSIM is easiest — activate before landing."
        },
        "phrases": [
            {"english": "Hello", "local": "Hello / Hi", "phonetic": "heh-loh / hai"},
            {"english": "Thank you", "local": "Thank you / Thanks", "phonetic": "thank yoo"},
            {"english": "Excuse me / Sorry", "local": "Excuse me / Sorry", "phonetic": "ex-kyooz mee"},
            {"english": "Yes", "local": "Yes / Yeah", "phonetic": "yes"},
            {"english": "No", "local": "No", "phonetic": "noh"},
            {"english": "Please", "local": "Please", "phonetic": "pleez"},
            {"english": "How much?", "local": "How much is this?", "phonetic": "how much iz this"},
            {"english": "Where is...?", "local": "Where is...?", "phonetic": "wair iz"},
            {"english": "Help!", "local": "Help!", "phonetic": "help"},
            {"english": "Goodbye", "local": "Goodbye / Bye", "phonetic": "good-bai"}
        ]
    },
    "BR": {
        "name": "Brazil",
        "health_slug": "brazil",
        "scam_cities": ["rio-de-janeiro", "sao-paulo"],
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["C", "N"],
            "voltage": "127V or 220V / 60Hz (varies by region)",
            "dialCode": "+55",
            "visaFreeCountries": "US citizens: visa-free for 90 days (as of 2024). UK, EU, Australia, Canada also visa-free for 90 days.",
            "timeZone": "UTC-03:00 (Brasília time)",
            "bestTimeToVisit": "April-October (dry season for most regions). Rio: December-March for beaches but very crowded during Carnival. Amazon: June-November (lower water, better wildlife)."
        },
        "cultural": {
            "tipping": "10% service charge usually included in restaurant bills. If not, 10% is customary. Round up for taxis. Tip hotel porters R$5-10 per bag.",
            "dressCode": "Very casual, especially in beach cities. Beachwear only at the beach — wearing swimwear in town is frowned upon. Smart casual for nice restaurants.",
            "greetings": "Kiss on one cheek (Rio) or two cheeks (São Paulo) between men-women and women-women. Handshake between men. Very warm and physical culture.",
            "taboos": [
                "The 'OK' hand gesture (considered vulgar in Brazil)",
                "Rushing conversations — Brazilians value personal connection before business",
                "Wearing Argentina's football jersey",
                "Discussing deforestation judgmentally",
                "Being excessively punctual (social events start 30-60 min late)"
            ],
            "haggling": "Common at markets, street vendors, and independent shops. Not at malls or chain stores. Be friendly and smile while negotiating."
        },
        "connectivity": {
            "simOptions": "Claro, Vivo, or TIM prepaid SIMs at airport counters or any 'loja' (shop). Need passport. Data plans are cheap — ~R$30-50 for 15GB.",
            "wifiAvailability": "Free WiFi at hotels, shopping malls, and many restaurants/cafes. Quality varies. Airport WiFi usually requires registration.",
            "bestOption": "Claro prepaid SIM for widest 4G coverage. Buy at airport on arrival. eSIM via Airalo works well as alternative."
        },
        "phrases": [
            {"english": "Hello", "local": "Olá", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Obrigado (m) / Obrigada (f)", "phonetic": "oh-bree-gah-doo / oh-bree-gah-dah"},
            {"english": "Excuse me / Sorry", "local": "Com licença / Desculpe", "phonetic": "kohm lee-sen-sah / desh-kool-peh"},
            {"english": "Yes", "local": "Sim", "phonetic": "seem"},
            {"english": "No", "local": "Não", "phonetic": "nowng"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "Quanto custa?", "phonetic": "kwan-too koos-tah"},
            {"english": "Where is...?", "local": "Onde fica...?", "phonetic": "on-jee fee-kah"},
            {"english": "Help!", "local": "Socorro!", "phonetic": "soh-koh-hoo"},
            {"english": "Goodbye", "local": "Tchau", "phonetic": "chow"}
        ]
    },
    "PL": {
        "name": "Poland",
        "health_slug": "poland",
        "scam_cities": ["krakow", "warsaw"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "E"],
            "voltage": "230V / 50Hz",
            "dialCode": "+48",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen). UK, EU, Australia, Canada, Japan also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "May-September (warm, long days). June-August peak season. December for Christmas markets. Avoid November (grey, cold)."
        },
        "cultural": {
            "tipping": "10% at restaurants is customary. Round up for taxis. Not expected at bars for simple drinks. Say 'reszta dla pana/pani' (keep the change).",
            "dressCode": "Smart casual in cities. Cover shoulders and knees in churches. Poland is quite fashionable — avoid looking too touristy.",
            "greetings": "Handshake with eye contact. Close friends kiss on both cheeks. Use Pan (Mr) / Pani (Mrs) until invited to use first names. Poles value politeness.",
            "taboos": [
                "Confusing Poland with Russia or calling it Eastern Europe (it's Central Europe)",
                "Making light of WWII or the Holocaust",
                "Refusing food or drink when offered as a guest",
                "Sitting at the corner of a table (superstition — won't marry for 7 years)",
                "Giving even numbers of flowers (reserved for funerals)"
            ],
            "haggling": "Not practiced. Prices are fixed at shops, restaurants, and most markets."
        },
        "connectivity": {
            "simOptions": "Play, Orange, or T-Mobile prepaid SIMs at airport shops or any 'salon' in the city. Cheap data — 20GB for ~30-40 PLN. Need passport.",
            "wifiAvailability": "Free WiFi at most cafes, restaurants, hotels, and shopping malls. Quality is generally good. Many cities have free municipal WiFi.",
            "bestOption": "Play prepaid SIM for best value and coverage. eSIM via Airalo or Holafly works well. EU roaming applies if you have an EU SIM."
        },
        "phrases": [
            {"english": "Hello", "local": "Cześć", "phonetic": "cheshch"},
            {"english": "Thank you", "local": "Dziękuję", "phonetic": "jen-koo-yeh"},
            {"english": "Excuse me / Sorry", "local": "Przepraszam", "phonetic": "psheh-prah-shahm"},
            {"english": "Yes", "local": "Tak", "phonetic": "tahk"},
            {"english": "No", "local": "Nie", "phonetic": "nyeh"},
            {"english": "Please", "local": "Proszę", "phonetic": "proh-sheh"},
            {"english": "How much?", "local": "Ile kosztuje?", "phonetic": "ee-leh kosh-too-yeh"},
            {"english": "Where is...?", "local": "Gdzie jest...?", "phonetic": "gjeh yest"},
            {"english": "Help!", "local": "Pomocy!", "phonetic": "poh-moh-tsih"},
            {"english": "Goodbye", "local": "Do widzenia", "phonetic": "doh vee-dzeh-nyah"}
        ]
    },
    "PH": {
        "name": "Philippines",
        "health_slug": "philippines",
        "scam_cities": ["manila", "cebu"],
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["A", "B", "C"],
            "voltage": "220V / 60Hz",
            "dialCode": "+63",
            "visaFreeCountries": "US citizens: 30 days visa-free (extendable). UK, EU, Australia also 30 days. Can extend up to 36 months at immigration offices.",
            "timeZone": "UTC+08:00",
            "bestTimeToVisit": "November-May (dry season). December-February best weather. Avoid June-October (typhoon season, especially August-October)."
        },
        "cultural": {
            "tipping": "10% at restaurants if no service charge. Round up for taxis. Tip tour guides and drivers PHP 200-500/day.",
            "dressCode": "Casual and relaxed. Cover up at churches. Swimwear only at beaches/pools. Filipinos dress neatly even casually.",
            "greetings": "Handshake for business. 'Mano po' (touching elder's hand to forehead) shows respect to elders. Smiling is universal. Use 'po' and 'opo' for politeness.",
            "taboos": [
                "Raising your voice or showing anger publicly (causes 'loss of face')",
                "Refusing food offered by a host",
                "Being overly direct with criticism",
                "Pointing with your finger (use lips or eyes to indicate direction)",
                "Arriving exactly on time to social events ('Filipino time' is 15-30 min late)"
            ],
            "haggling": "Expected at markets, street vendors, and some small shops. Not at malls or restaurants. Be friendly and respectful."
        },
        "connectivity": {
            "simOptions": "Globe or Smart prepaid SIMs at airports and convenience stores. Very cheap — unlimited data promos for PHP 99-299/week. No registration hassle.",
            "wifiAvailability": "Free WiFi at malls, hotels, and chain restaurants. Speeds can be slow outside Metro Manila. Many islands have limited connectivity.",
            "bestOption": "Globe prepaid SIM with GoSURF or GOMO data plan. Buy at airport. Coverage good in cities but can be spotty on remote islands."
        },
        "phrases": [
            {"english": "Hello", "local": "Kumusta", "phonetic": "koo-moos-tah"},
            {"english": "Thank you", "local": "Salamat", "phonetic": "sah-lah-maht"},
            {"english": "Excuse me / Sorry", "local": "Pasensya na / Sorry po", "phonetic": "pah-sen-syah nah"},
            {"english": "Yes", "local": "Oo", "phonetic": "oh-oh"},
            {"english": "No", "local": "Hindi", "phonetic": "hin-dee"},
            {"english": "Please", "local": "Pakiusap", "phonetic": "pah-kee-oo-sahp"},
            {"english": "How much?", "local": "Magkano?", "phonetic": "mahg-kah-noh"},
            {"english": "Where is...?", "local": "Nasaan ang...?", "phonetic": "nah-sah-ahn ahng"},
            {"english": "Help!", "local": "Tulong!", "phonetic": "too-long"},
            {"english": "Goodbye", "local": "Paalam", "phonetic": "pah-ah-lahm"}
        ]
    },
    "AR": {
        "name": "Argentina",
        "health_slug": "argentina",
        "scam_cities": ["buenos-aires"],
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["C", "I"],
            "voltage": "220V / 50Hz",
            "dialCode": "+54",
            "visaFreeCountries": "US citizens: 90 days visa-free. UK, EU, Australia, Canada also visa-free. Reciprocity fee eliminated.",
            "timeZone": "UTC-03:00",
            "bestTimeToVisit": "October-April (spring/summer). Patagonia: December-February. Buenos Aires: March-May, September-November (mild). Ski season: June-September."
        },
        "cultural": {
            "tipping": "10% at restaurants is customary. Round up for taxis. Tip hotel porters AR$500-1000. Propina (tip) jars common at cafes.",
            "dressCode": "Smart casual in Buenos Aires — Argentines are stylish. Casual elsewhere. No special religious dress codes.",
            "greetings": "One kiss on the right cheek for everyone (men-men, men-women, women-women). Even at first meeting. Handshake only in very formal business.",
            "taboos": [
                "Calling Falkland Islands 'Falklands' (use 'Malvinas')",
                "Comparing Argentina to other Latin American countries negatively",
                "Rushing meals — dinner starts at 9-10 PM and is a social event",
                "Pouring wine backhanded (considered rude)",
                "Being punctual to social events (arrive 30-60 min late)"
            ],
            "haggling": "Not common at shops or restaurants. Acceptable at artisan markets and when paying cash (ask for 'descuento en efectivo')."
        },
        "connectivity": {
            "simOptions": "Claro, Movistar, or Personal prepaid SIMs at airport or city shops. Bring passport. Data is reasonably priced. Cash payments often cheaper than card.",
            "wifiAvailability": "Free WiFi at most cafes, restaurants, and hotels in Buenos Aires. Quality good in major cities, limited in rural Patagonia.",
            "bestOption": "Claro prepaid SIM for best coverage. Buy at Buenos Aires airport. eSIM via Airalo as backup. Note: bring US dollars — better exchange rate on 'blue dollar' market."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Gracias", "phonetic": "grah-syahs"},
            {"english": "Excuse me / Sorry", "local": "Disculpá / Perdón", "phonetic": "dees-kool-pah / pair-dohn"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "noh"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto sale?", "phonetic": "kwan-toh sah-leh"},
            {"english": "Where is...?", "local": "¿Dónde queda...?", "phonetic": "don-deh keh-dah"},
            {"english": "Help!", "local": "¡Ayuda!", "phonetic": "ah-yoo-dah"},
            {"english": "Goodbye", "local": "Chau", "phonetic": "chow"}
        ]
    },
    "SE": {
        "name": "Sweden",
        "health_slug": "sweden",
        "scam_cities": ["stockholm"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+46",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen). UK, EU, Australia, Canada, Japan also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "June-August (warm, midnight sun in the north). December-February for Northern Lights and snow activities. May and September for fewer crowds."
        },
        "cultural": {
            "tipping": "Not expected — service included in prices. Rounding up the bill is appreciated but not required. 5-10% at restaurants for exceptional service.",
            "dressCode": "Smart casual. Swedes dress stylishly but understated. No specific religious dress codes. Bring layers — weather changes quickly.",
            "greetings": "Handshake with eye contact. Swedes value personal space. First names used from the start. 'Hej' (hey) is the universal casual greeting.",
            "taboos": [
                "Being late (Swedes are very punctual)",
                "Bragging or showing off (Jantelagen — 'don't think you're special')",
                "Sitting next to someone on public transport when other seats are available",
                "Small talk with strangers (less common than in other cultures)",
                "Wearing shoes indoors"
            ],
            "haggling": "Never. Prices are always fixed. Sweden is essentially cashless — card/mobile payment everywhere."
        },
        "connectivity": {
            "simOptions": "Telia, Tele2, or Tre prepaid SIMs at Pressbyrån kiosks or phone shops. eSIM via Airalo or Holafly. EU roaming with any EU SIM.",
            "wifiAvailability": "Excellent free WiFi everywhere — cafes, restaurants, public transport, and many public spaces. Sweden is one of the most connected countries.",
            "bestOption": "EU SIM with roaming if you have one. Otherwise Airalo eSIM. Sweden is almost cashless — bring cards, not cash."
        },
        "phrases": [
            {"english": "Hello", "local": "Hej", "phonetic": "hey"},
            {"english": "Thank you", "local": "Tack", "phonetic": "tahk"},
            {"english": "Excuse me / Sorry", "local": "Ursäkta / Förlåt", "phonetic": "oor-shek-tah / fur-loht"},
            {"english": "Yes", "local": "Ja", "phonetic": "yah"},
            {"english": "No", "local": "Nej", "phonetic": "nay"},
            {"english": "Please", "local": "Snälla / Tack", "phonetic": "sneh-lah / tahk"},
            {"english": "How much?", "local": "Hur mycket kostar det?", "phonetic": "hoor mew-keh kos-tar deh"},
            {"english": "Where is...?", "local": "Var ligger...?", "phonetic": "var lig-er"},
            {"english": "Help!", "local": "Hjälp!", "phonetic": "yelp"},
            {"english": "Goodbye", "local": "Hej då", "phonetic": "hey doh"}
        ]
    },
    "EG": {
        "name": "Egypt",
        "health_slug": "egypt",
        "scam_cities": ["cairo"],
        "practical": {
            "tapWater": False,
            "drivingSide": "right",
            "plugType": ["C"],
            "voltage": "220V / 50Hz",
            "dialCode": "+20",
            "visaFreeCountries": "US citizens: visa on arrival (USD $25) or e-Visa. UK, EU also eligible for visa on arrival. Single entry, 30 days.",
            "timeZone": "UTC+02:00",
            "bestTimeToVisit": "October-April (cooler). December-February most pleasant. Avoid June-August (extreme heat 40°C+). Ramadan dates vary — plan accordingly."
        },
        "cultural": {
            "tipping": "Expected everywhere. 10-15% at restaurants. Tip guides, drivers, hotel staff. Baksheesh (small tips) is part of daily life — carry small bills.",
            "dressCode": "Modest dress, especially for women. Cover shoulders and knees, particularly at mosques. Women should bring a headscarf for mosque visits. Men should wear long pants at religious sites.",
            "greetings": "Handshake common between same gender. Men should wait for a woman to extend her hand first. 'As-salamu alaykum' (peace be upon you) is the standard greeting.",
            "taboos": [
                "Using left hand to eat or pass items",
                "Showing the soles of your feet",
                "Public displays of affection",
                "Photography of military installations or government buildings",
                "Criticizing religion or government publicly",
                "Drinking alcohol in public during Ramadan"
            ],
            "haggling": "Expected and essential at bazaars, markets, and with taxi drivers. Start at 25-40% of asking price. Take your time — haggling is a social ritual."
        },
        "connectivity": {
            "simOptions": "Vodafone Egypt, Orange, or Etisalat prepaid SIMs at airport arrivals hall. Need passport. Data plans very cheap — ~50 EGP for 10GB.",
            "wifiAvailability": "Free WiFi at most hotels and many cafes in Cairo and tourist areas. Quality can be unreliable. Limited in Upper Egypt and desert areas.",
            "bestOption": "Vodafone Egypt prepaid SIM at Cairo airport — counters open 24/7. Best coverage nationwide. eSIM via Airalo as alternative."
        },
        "phrases": [
            {"english": "Hello", "local": "مرحبا (Marhaba)", "phonetic": "mar-hah-bah"},
            {"english": "Thank you", "local": "شكراً (Shukran)", "phonetic": "shook-rahn"},
            {"english": "Excuse me / Sorry", "local": "عفواً (Afwan)", "phonetic": "af-wahn"},
            {"english": "Yes", "local": "أيوه (Aywa)", "phonetic": "ai-wah"},
            {"english": "No", "local": "لأ (La')", "phonetic": "lah"},
            {"english": "Please", "local": "من فضلك (Min fadlak)", "phonetic": "min fad-lak"},
            {"english": "How much?", "local": "بكام؟ (Bikam?)", "phonetic": "bee-kahm"},
            {"english": "Where is...?", "local": "فين...؟ (Fein...?)", "phonetic": "fayn"},
            {"english": "Help!", "local": "!النجدة (Elnahgda!)", "phonetic": "el-nag-dah"},
            {"english": "Goodbye", "local": "مع السلامة (Ma'a el-salama)", "phonetic": "mah-ah es-sah-lah-mah"}
        ]
    },
    "CL": {
        "name": "Chile",
        "health_slug": "chile",
        "scam_cities": ["santiago"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "L"],
            "voltage": "220V / 50Hz",
            "dialCode": "+56",
            "visaFreeCountries": "US citizens: 90 days visa-free. UK, EU, Australia, Canada also visa-free. Tourist card issued at entry.",
            "timeZone": "UTC-04:00",
            "bestTimeToVisit": "October-March (spring/summer). Atacama Desert: year-round. Patagonia: December-February. Ski season: June-August."
        },
        "cultural": {
            "tipping": "10% at restaurants is customary. Not expected at cafes. Round up for taxis. Tip tour guides CLP 5,000-10,000/day.",
            "dressCode": "Smart casual in Santiago. Casual in beach towns and the south. No specific religious dress codes.",
            "greetings": "One kiss on the right cheek between men-women and women-women. Handshake between men. 'Hola' followed by '¿Cómo estás?' is standard.",
            "taboos": [
                "Comparing Chile unfavorably to Argentina (strong rivalry)",
                "Being overly direct or confrontational",
                "Skipping the greeting ritual — always say hello first",
                "Eating on public transport",
                "Discussing Pinochet unless the other person brings it up"
            ],
            "haggling": "Not common. Prices are fixed at stores and restaurants. Some negotiation at artisan markets in tourist areas."
        },
        "connectivity": {
            "simOptions": "Entel, Movistar, or WOM prepaid SIMs at airports or phone shops. Need passport. WOM offers best value data plans.",
            "wifiAvailability": "Free WiFi at hotels, cafes, malls, and some public plazas in Santiago. Coverage limited in Patagonia and remote areas.",
            "bestOption": "WOM prepaid SIM for best data value. Buy at Santiago airport. eSIM via Airalo works well in major cities."
        },
        "phrases": [
            {"english": "Hello", "local": "Hola", "phonetic": "oh-lah"},
            {"english": "Thank you", "local": "Gracias", "phonetic": "grah-syahs"},
            {"english": "Excuse me / Sorry", "local": "Disculpa / Perdón", "phonetic": "dees-kool-pah / pair-dohn"},
            {"english": "Yes", "local": "Sí", "phonetic": "see"},
            {"english": "No", "local": "No", "phonetic": "noh"},
            {"english": "Please", "local": "Por favor", "phonetic": "por fah-vor"},
            {"english": "How much?", "local": "¿Cuánto vale?", "phonetic": "kwan-toh vah-leh"},
            {"english": "Where is...?", "local": "¿Dónde está...?", "phonetic": "don-deh es-tah"},
            {"english": "Help!", "local": "¡Ayuda!", "phonetic": "ah-yoo-dah"},
            {"english": "Goodbye", "local": "Chao", "phonetic": "chow"}
        ]
    },
    "NO": {
        "name": "Norway",
        "health_slug": "norway",
        "scam_cities": [],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+47",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen). UK, EU, Australia, Canada, Japan also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "June-August (midnight sun, hiking, fjords). September-March for Northern Lights. May and September for shoulder season value."
        },
        "cultural": {
            "tipping": "Not expected — service included. Rounding up is appreciated but never required. Norway is one of the most expensive countries in the world.",
            "dressCode": "Casual and practical. Dress in layers. No specific religious dress codes. 'There's no bad weather, only bad clothing' is the national motto.",
            "greetings": "Handshake with eye contact. Personal space respected. First names used immediately. 'Hei' is the casual greeting.",
            "taboos": [
                "Being late (Norwegians are very punctual)",
                "Bragging or being flashy (Janteloven culture)",
                "Standing too close in conversation",
                "Loud behavior on public transport",
                "Expecting everything to be open on Sundays (many shops closed)"
            ],
            "haggling": "Never. Prices are always fixed. Everything is expensive — accept it."
        },
        "connectivity": {
            "simOptions": "Telenor, Telia, or ICE prepaid SIMs at Narvesen kiosks or phone shops. EU roaming doesn't apply (Norway is EEA, not EU — check your plan).",
            "wifiAvailability": "Free WiFi at most hotels, cafes, and public buildings. Excellent 4G/5G coverage even in rural areas and along fjords.",
            "bestOption": "Telenor prepaid SIM for best fjord/rural coverage. eSIM via Airalo works well. Note: Norway uses NOK, not EUR."
        },
        "phrases": [
            {"english": "Hello", "local": "Hei", "phonetic": "hay"},
            {"english": "Thank you", "local": "Takk", "phonetic": "tahk"},
            {"english": "Excuse me / Sorry", "local": "Unnskyld", "phonetic": "oon-shuld"},
            {"english": "Yes", "local": "Ja", "phonetic": "yah"},
            {"english": "No", "local": "Nei", "phonetic": "nay"},
            {"english": "Please", "local": "Vær så snill", "phonetic": "vair soh snill"},
            {"english": "How much?", "local": "Hvor mye koster det?", "phonetic": "voor mew-eh kos-ter deh"},
            {"english": "Where is...?", "local": "Hvor er...?", "phonetic": "voor air"},
            {"english": "Help!", "local": "Hjelp!", "phonetic": "yelp"},
            {"english": "Goodbye", "local": "Ha det", "phonetic": "hah deh"}
        ]
    },
    "ZA": {
        "name": "South Africa",
        "health_slug": "south-africa",
        "scam_cities": ["cape-town", "johannesburg"],
        "practical": {
            "tapWater": True,
            "drivingSide": "left",
            "plugType": ["M", "N"],
            "voltage": "230V / 50Hz",
            "dialCode": "+27",
            "visaFreeCountries": "US citizens: 90 days visa-free. UK, EU also visa-free. Passport must have 2+ blank pages.",
            "timeZone": "UTC+02:00",
            "bestTimeToVisit": "May-September (dry winter — best for safari). October-November (spring, wildflowers). December-February (summer, beach weather). Cape Town: December-March."
        },
        "cultural": {
            "tipping": "10-15% at restaurants. R20-50 for car guards and gas station attendants. Tip safari guides R100-200/day per person.",
            "dressCode": "Casual. Smart casual for nice restaurants in Cape Town/Johannesburg. No specific religious dress codes.",
            "greetings": "Handshake is standard. In some cultures, a three-part handshake (clasp, grip, clasp). 'Howzit' is the informal South African greeting.",
            "taboos": [
                "Discussing apartheid insensitively",
                "Walking alone at night in cities (safety concern, not cultural)",
                "Flashing expensive jewelry or electronics in public",
                "Ignoring 'load shedding' schedules (planned power cuts)",
                "Assuming everyone speaks Afrikaans (11 official languages)"
            ],
            "haggling": "Common at craft markets and curio shops. Not at stores or restaurants. Township tours should be booked through reputable operators."
        },
        "connectivity": {
            "simOptions": "Vodacom, MTN, or Cell C prepaid SIMs at OR Tambo airport or any Pick n Pay/Checkers. Need passport. RICA registration required (done at point of sale).",
            "wifiAvailability": "Free WiFi at hotels, shopping malls, and many restaurants. WiFi hotspots at some public spaces. 4G coverage good in cities, limited in rural areas.",
            "bestOption": "Vodacom prepaid SIM for best coverage including safari areas. Buy at airport. Load shedding can affect cell towers — carry a power bank."
        },
        "phrases": [
            {"english": "Hello", "local": "Howzit / Molo (Xhosa) / Sawubona (Zulu)", "phonetic": "how-zit / moh-loh / sah-woo-boh-nah"},
            {"english": "Thank you", "local": "Dankie (Afrikaans) / Enkosi (Xhosa)", "phonetic": "dahn-kee / en-koh-see"},
            {"english": "Excuse me / Sorry", "local": "Verskoon my / Uxolo", "phonetic": "fer-skoon may / oo-kshoh-loh"},
            {"english": "Yes", "local": "Ja / Yebo (Zulu)", "phonetic": "yah / yeh-boh"},
            {"english": "No", "local": "Nee / Cha (Zulu)", "phonetic": "nee-ah / chah"},
            {"english": "Please", "local": "Asseblief", "phonetic": "ah-seh-bleef"},
            {"english": "How much?", "local": "Hoeveel kos dit?", "phonetic": "hoo-feel kos dit"},
            {"english": "Where is...?", "local": "Waar is...?", "phonetic": "vahr is"},
            {"english": "Help!", "local": "Help!", "phonetic": "help"},
            {"english": "Goodbye", "local": "Totsiens / Sala kahle (Zulu)", "phonetic": "tot-seens / sah-lah kah-leh"}
        ]
    },
    "LK": {
        "name": "Sri Lanka",
        "health_slug": "sri-lanka",
        "scam_cities": ["colombo"],
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["D", "G"],
            "voltage": "230V / 50Hz",
            "dialCode": "+94",
            "visaFreeCountries": "US citizens: free visa on arrival for 30 days (as of 2024). Apply for ETA online before travel. UK, EU also eligible.",
            "timeZone": "UTC+05:30",
            "bestTimeToVisit": "West/south coast: December-March. East coast: April-September. Hill country: January-April. Avoid monsoon season for your target coast."
        },
        "cultural": {
            "tipping": "10% at restaurants if no service charge. Tip drivers LKR 500-1000/day, guides LKR 1000-2000/day.",
            "dressCode": "Modest dress at temples — cover shoulders and knees, remove shoes. White clothing at temples is respectful. Avoid clothing with Buddha images (illegal to disrespect).",
            "greetings": "Hands together with slight bow (like namaste) — 'Ayubowan' in Sinhala. Handshake also acceptable. Remove hat and sunglasses at temples.",
            "taboos": [
                "Posing for photos with your back to a Buddha statue",
                "Wearing clothing with Buddha images (can be confiscated/deported)",
                "Touching someone's head",
                "Pointing feet at people or religious objects",
                "Using left hand for eating or passing items",
                "Public displays of affection"
            ],
            "haggling": "Expected at markets, tuk-tuks, and tourist shops. Not at supermarkets or restaurants. Start at 50% of asking price."
        },
        "connectivity": {
            "simOptions": "Dialog or Mobitel prepaid SIMs at Bandaranaike Airport arrivals. Need passport. Very cheap — unlimited data for ~LKR 1500/month.",
            "wifiAvailability": "Free WiFi at most hotels and some cafes. Speeds can be slow outside Colombo. 4G coverage improving but patchy in hill country.",
            "bestOption": "Dialog prepaid SIM at airport — counter is right after immigration. Best coverage including rural and hill country areas."
        },
        "phrases": [
            {"english": "Hello", "local": "ආයුබෝවන් (Ayubowan)", "phonetic": "ah-yoo-boh-wan"},
            {"english": "Thank you", "local": "ස්තූතියි (Isthuthi)", "phonetic": "is-too-tee"},
            {"english": "Excuse me / Sorry", "local": "සමාවෙන්න (Samawenna)", "phonetic": "sah-mah-ven-nah"},
            {"english": "Yes", "local": "ඔව් (Ow)", "phonetic": "oh-wuh"},
            {"english": "No", "local": "නැහැ (Naehae)", "phonetic": "neh-heh"},
            {"english": "Please", "local": "කරුණාකර (Karunakara)", "phonetic": "kah-roo-nah-kah-rah"},
            {"english": "How much?", "local": "කීයද? (Keeyada?)", "phonetic": "kee-yah-dah"},
            {"english": "Where is...?", "local": "...කොහෙද? (...koheda?)", "phonetic": "koh-heh-dah"},
            {"english": "Help!", "local": "උදව්! (Udaw!)", "phonetic": "oo-daw"},
            {"english": "Goodbye", "local": "ගිහින් එන්නම් (Gihin ennam)", "phonetic": "gee-hin en-nahm"}
        ]
    },
    "TZ": {
        "name": "Tanzania",
        "health_slug": "tanzania",
        "scam_cities": ["zanzibar"],
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["D", "G"],
            "voltage": "230V / 50Hz",
            "dialCode": "+255",
            "visaFreeCountries": "US citizens: visa on arrival ($50) or e-Visa. UK, EU, most nationalities eligible for visa on arrival.",
            "timeZone": "UTC+03:00",
            "bestTimeToVisit": "June-October (dry season, best for safari and Kilimanjaro). January-February (short dry season, calving in Serengeti). Avoid March-May (heavy rains)."
        },
        "cultural": {
            "tipping": "10% at restaurants. Safari guides: $15-25/day per person. Kilimanjaro porters: $8-15/day. Hotel porters: TZS 2000-5000.",
            "dressCode": "Modest dress, especially on Zanzibar (Muslim culture) — cover shoulders and knees. Safari: neutral colors (khaki, olive, brown). Avoid blue/black (attracts tsetse flies).",
            "greetings": "'Jambo' (hello) or 'Habari' (how are you) — response is 'Nzuri' (fine). Handshake is common. Elders are addressed with respect.",
            "taboos": [
                "Photographing people without permission (especially Maasai — tip expected)",
                "Wearing revealing clothing on Zanzibar",
                "Eating with left hand",
                "Refusing offered food or drink",
                "Disrespecting Maasai culture or traditions"
            ],
            "haggling": "Expected at markets, souvenir shops, and with taxi/tuk-tuk drivers. Not at restaurants or supermarkets. Start at 30-50% of asking price."
        },
        "connectivity": {
            "simOptions": "Vodacom or Airtel prepaid SIMs at Julius Nyerere Airport or any phone shop. Need passport. Very cheap data plans.",
            "wifiAvailability": "Free WiFi at most hotels and lodges. Limited in safari camps and national parks. Zanzibar towns have decent connectivity.",
            "bestOption": "Vodacom prepaid SIM for best coverage including safari areas. Buy at airport. Don't rely on WiFi during safari."
        },
        "phrases": [
            {"english": "Hello", "local": "Jambo / Habari", "phonetic": "jahm-boh / hah-bah-ree"},
            {"english": "Thank you", "local": "Asante (sana)", "phonetic": "ah-sahn-teh (sah-nah)"},
            {"english": "Excuse me / Sorry", "local": "Samahani", "phonetic": "sah-mah-hah-nee"},
            {"english": "Yes", "local": "Ndiyo", "phonetic": "n-dee-yoh"},
            {"english": "No", "local": "Hapana", "phonetic": "hah-pah-nah"},
            {"english": "Please", "local": "Tafadhali", "phonetic": "tah-fah-dah-lee"},
            {"english": "How much?", "local": "Bei gani?", "phonetic": "bay gah-nee"},
            {"english": "Where is...?", "local": "...iko wapi?", "phonetic": "ee-koh wah-pee"},
            {"english": "Help!", "local": "Msaada!", "phonetic": "m-sah-ah-dah"},
            {"english": "Goodbye", "local": "Kwaheri", "phonetic": "kwah-heh-ree"}
        ]
    },
    "KE": {
        "name": "Kenya",
        "health_slug": "kenya",
        "scam_cities": ["nairobi"],
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["G"],
            "voltage": "240V / 50Hz",
            "dialCode": "+254",
            "visaFreeCountries": "US citizens: e-Visa required ($50). Apply online before travel. Some nationalities eligible for visa on arrival. ETA system being implemented.",
            "timeZone": "UTC+03:00",
            "bestTimeToVisit": "January-March (hot, dry — good for safari). July-October (Great Migration in Masai Mara). June-October dry season overall best."
        },
        "cultural": {
            "tipping": "10% at restaurants. Safari guides/drivers: $15-25/day per person. Hotel porters: KES 200-500.",
            "dressCode": "Modest dress in rural and coastal areas (Muslim regions). Safari: neutral colors. Nairobi is more cosmopolitan and casual.",
            "greetings": "'Jambo' or 'Habari yako' (how are you). Handshake is standard. Elders and authority figures addressed with respect.",
            "taboos": [
                "Photographing people without asking (especially Maasai — negotiate a fee)",
                "Pointing at wildlife during safari (use open hand)",
                "Disrespecting the flag or national symbols",
                "Public intoxication",
                "Same-sex public displays of affection (illegal)"
            ],
            "haggling": "Expected at markets, souvenir shops, matatus (minibuses), and with taxi drivers. Not at supermarkets. Start at 40-50% of asking price."
        },
        "connectivity": {
            "simOptions": "Safaricom (M-Pesa network) prepaid SIM at JKIA airport or any Safaricom shop. Need passport. Data is cheap. M-Pesa mobile money is essential.",
            "wifiAvailability": "Good WiFi at hotels and cafes in Nairobi and Mombasa. Limited in safari parks and rural areas. Some lodges have WiFi.",
            "bestOption": "Safaricom prepaid SIM — essential for M-Pesa mobile payments (widely used for everything). Buy at airport on arrival."
        },
        "phrases": [
            {"english": "Hello", "local": "Jambo / Sasa", "phonetic": "jahm-boh / sah-sah"},
            {"english": "Thank you", "local": "Asante", "phonetic": "ah-sahn-teh"},
            {"english": "Excuse me / Sorry", "local": "Samahani", "phonetic": "sah-mah-hah-nee"},
            {"english": "Yes", "local": "Ndiyo", "phonetic": "n-dee-yoh"},
            {"english": "No", "local": "Hapana", "phonetic": "hah-pah-nah"},
            {"english": "Please", "local": "Tafadhali", "phonetic": "tah-fah-dah-lee"},
            {"english": "How much?", "local": "Bei gani?", "phonetic": "bay gah-nee"},
            {"english": "Where is...?", "local": "...iko wapi?", "phonetic": "ee-koh wah-pee"},
            {"english": "Help!", "local": "Msaada!", "phonetic": "m-sah-ah-dah"},
            {"english": "Goodbye", "local": "Kwaheri", "phonetic": "kwah-heh-ree"}
        ]
    },
    "CZ": {
        "name": "Czech Republic",
        "health_slug": "czech-republic",
        "scam_cities": ["prague"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "E"],
            "voltage": "230V / 50Hz",
            "dialCode": "+420",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen). UK, EU, Australia, Canada, Japan also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "May-September (warm, outdoor festivals). December for Christmas markets. April and October for fewer crowds."
        },
        "cultural": {
            "tipping": "10% at restaurants is customary. Round up for taxis. Tell the server the total you want to pay (don't leave money on table).",
            "dressCode": "Smart casual in Prague. Business settings are formal. No specific religious dress codes at churches (though modest dress appreciated).",
            "greetings": "Handshake with eye contact. Use 'Dobrý den' (good day) formally. Close friends may do a light cheek kiss. Titles are valued in formal settings.",
            "taboos": [
                "Calling it 'Czechoslovakia' (it's been Czech Republic/Czechia since 1993)",
                "Confusing Czech with Russian or Polish",
                "Toasting with water (considered bad luck)",
                "Being loud in residential areas at night",
                "Not validating public transport tickets (plain-clothes inspectors are common)"
            ],
            "haggling": "Not practiced. Prices are fixed. Watch out for tourist-trap restaurants near Old Town Square — check prices before ordering."
        },
        "connectivity": {
            "simOptions": "T-Mobile, O2, or Vodafone prepaid SIMs at airport or any newsstand. EU roaming with any EU SIM. Data is affordable.",
            "wifiAvailability": "Free WiFi at most cafes, restaurants, and hotels. Prague has good coverage. Many public spaces also have WiFi.",
            "bestOption": "EU SIM with roaming if you have one. Otherwise T-Mobile prepaid at Prague airport. eSIM via Airalo works well."
        },
        "phrases": [
            {"english": "Hello", "local": "Dobrý den / Ahoj", "phonetic": "dob-ree den / ah-hoy"},
            {"english": "Thank you", "local": "Děkuji", "phonetic": "dyeh-koo-yee"},
            {"english": "Excuse me / Sorry", "local": "Promiňte", "phonetic": "pro-min-teh"},
            {"english": "Yes", "local": "Ano", "phonetic": "ah-noh"},
            {"english": "No", "local": "Ne", "phonetic": "neh"},
            {"english": "Please", "local": "Prosím", "phonetic": "pro-seem"},
            {"english": "How much?", "local": "Kolik to stojí?", "phonetic": "koh-lik toh stoh-yee"},
            {"english": "Where is...?", "local": "Kde je...?", "phonetic": "gdeh yeh"},
            {"english": "Help!", "local": "Pomoc!", "phonetic": "poh-motz"},
            {"english": "Goodbye", "local": "Na shledanou", "phonetic": "nah skhleh-dah-noh"}
        ]
    },
    "HU": {
        "name": "Hungary",
        "health_slug": "hungary",
        "scam_cities": ["budapest"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+36",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen). UK, EU, Australia, Canada, Japan also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "April-June and September-October (mild, fewer crowds). July-August (hot, festivals). December for Christmas markets and thermal baths."
        },
        "cultural": {
            "tipping": "10-15% at restaurants (specify when paying — don't leave on table). Round up for taxis. Tip thermal bath attendants HUF 500-1000.",
            "dressCode": "Smart casual in Budapest. Business dress is formal. Bring swimwear for thermal baths (some require swim caps).",
            "greetings": "Handshake with eye contact. 'Szia' (see-ah) for casual hello. Hungarians put surname first (like Japanese). Close friends may cheek-kiss.",
            "taboos": [
                "Clinking beer glasses (relates to 1848 Austrian celebration — some Hungarians still observe this)",
                "Confusing Hungary with other Eastern European countries",
                "Whistling indoors (considered bad luck)",
                "Not taking off shoes when entering someone's home",
                "Being late without notice"
            ],
            "haggling": "Not practiced at shops or restaurants. The Great Market Hall has fixed prices despite being touristy. Watch for tourist-trap restaurants in Váci utca."
        },
        "connectivity": {
            "simOptions": "Telekom, Telenor (Yettel), or Vodafone prepaid SIMs at Budapest airport or city shops. EU roaming with any EU SIM.",
            "wifiAvailability": "Free WiFi at most cafes (Budapest's café culture is strong), hotels, and thermal baths. Good 4G coverage citywide.",
            "bestOption": "EU SIM with roaming. Otherwise Vodafone prepaid at airport. eSIM via Airalo as quick alternative."
        },
        "phrases": [
            {"english": "Hello", "local": "Szia", "phonetic": "see-ah"},
            {"english": "Thank you", "local": "Köszönöm", "phonetic": "kuh-suh-nuhm"},
            {"english": "Excuse me / Sorry", "local": "Elnézést", "phonetic": "el-nay-zaysht"},
            {"english": "Yes", "local": "Igen", "phonetic": "ee-gen"},
            {"english": "No", "local": "Nem", "phonetic": "nem"},
            {"english": "Please", "local": "Kérem", "phonetic": "kay-rem"},
            {"english": "How much?", "local": "Mennyibe kerül?", "phonetic": "men-nyee-beh keh-rewl"},
            {"english": "Where is...?", "local": "Hol van...?", "phonetic": "hol vahn"},
            {"english": "Help!", "local": "Segítség!", "phonetic": "sheh-geet-shayg"},
            {"english": "Goodbye", "local": "Viszontlátásra", "phonetic": "vee-sont-lah-tahsh-rah"}
        ]
    },
    "HR": {
        "name": "Croatia",
        "health_slug": "croatia",
        "scam_cities": ["dubrovnik", "split"],
        "practical": {
            "tapWater": True,
            "drivingSide": "right",
            "plugType": ["C", "F"],
            "voltage": "230V / 50Hz",
            "dialCode": "+385",
            "visaFreeCountries": "US citizens: 90 days visa-free (Schengen, joined 2023). UK, EU, Australia, Canada also visa-free.",
            "timeZone": "UTC+01:00",
            "bestTimeToVisit": "May-June and September (warm, fewer crowds). July-August peak in Dubrovnik."
        },
        "cultural": {
            "tipping": "10% at restaurants appreciated. Round up for taxis.",
            "dressCode": "Casual on coast. Cover shoulders/knees in churches. Comfortable shoes in Old Towns.",
            "greetings": "Handshake formal. Kiss on both cheeks between friends. 'Bok' is casual hello.",
            "taboos": ["Comparing to Serbia", "Calling it Yugoslavia", "Being loud in Old Towns at night", "Not trying local wine when offered"],
            "haggling": "Not practiced. Fixed prices everywhere."
        },
        "connectivity": {
            "simOptions": "A1, T-Mobile, or Telemach at airports. EU roaming works since 2023.",
            "wifiAvailability": "Good WiFi at cafes, hotels, restaurants along coast.",
            "bestOption": "EU SIM with roaming. Otherwise A1 prepaid at airport."
        },
        "phrases": [
            {"english": "Hello", "local": "Bok / Zdravo", "phonetic": "bohk / zdrah-voh"},
            {"english": "Thank you", "local": "Hvala", "phonetic": "hvah-lah"},
            {"english": "Excuse me / Sorry", "local": "Oprostite", "phonetic": "oh-pros-tee-teh"},
            {"english": "Yes", "local": "Da", "phonetic": "dah"},
            {"english": "No", "local": "Ne", "phonetic": "neh"},
            {"english": "Please", "local": "Molim", "phonetic": "moh-leem"},
            {"english": "How much?", "local": "Koliko košta?", "phonetic": "koh-lee-koh kosh-tah"},
            {"english": "Where is...?", "local": "Gdje je...?", "phonetic": "gd-yeh yeh"},
            {"english": "Help!", "local": "Upomoć!", "phonetic": "oo-poh-mohtch"},
            {"english": "Goodbye", "local": "Doviđenja", "phonetic": "doh-vee-jen-yah"}
        ]
    },
    "MY": {
        "name": "Malaysia",
        "health_slug": "malaysia",
        "scam_cities": ["kuala-lumpur"],
        "practical": {
            "tapWater": False,
            "drivingSide": "left",
            "plugType": ["G"],
            "voltage": "240V / 50Hz",
            "dialCode": "+60",
            "visaFreeCountries": "US citizens: 90 days visa-free. Very easy entry.",
            "timeZone": "UTC+08:00",
            "bestTimeToVisit": "March-October for west coast. November-February for east coast. KL hot year-round."
        },
        "cultural": {
            "tipping": "Not expected. Some upscale restaurants add 10% service charge.",
            "dressCode": "Modest at mosques (robes provided). Remove shoes at mosques and homes.",
            "greetings": "Light handshake then touch heart. Don't offer handshake to opposite gender unless initiated.",
            "taboos": ["Touching heads", "Using left hand", "Pointing with index finger", "Public displays of affection", "Eating pork in Malay restaurants"],
            "haggling": "Expected at night markets. Not at malls or supermarkets."
        },
        "connectivity": {
            "simOptions": "Hotlink (Maxis), Celcom, or Digi at KLIA or 7-Eleven. RM30-50 for tourist plans.",
            "wifiAvailability": "Good WiFi at malls, hotels, cafes. Spotty in Borneo jungle.",
            "bestOption": "Hotlink (Maxis) prepaid at KLIA airport."
        },
        "phrases": [
            {"english": "Hello", "local": "Selamat datang", "phonetic": "seh-lah-maht dah-tahng"},
            {"english": "Thank you", "local": "Terima kasih", "phonetic": "teh-ree-mah kah-see"},
            {"english": "Excuse me / Sorry", "local": "Maafkan saya", "phonetic": "mah-ahf-kahn sah-yah"},
            {"english": "Yes", "local": "Ya", "phonetic": "yah"},
            {"english": "No", "local": "Tidak", "phonetic": "tee-dahk"},
            {"english": "Please", "local": "Tolong", "phonetic": "toh-long"},
            {"english": "How much?", "local": "Berapa harga?", "phonetic": "beh-rah-pah har-gah"},
            {"english": "Where is...?", "local": "Di mana...?", "phonetic": "dee mah-nah"},
            {"english": "Help!", "local": "Tolong!", "phonetic": "toh-long"},
            {"english": "Goodbye", "local": "Selamat tinggal", "phonetic": "seh-lah-maht ting-gahl"}
        ]
    },
    "SG": {
        "name": "Singapore",
        "health_slug": "singapore",
        "scam_cities": [],
        "practical": {
            "tapWater": True,
            "drivingSide": "left",
            "plugType": ["G"],
            "voltage": "230V / 50Hz",
            "dialCode": "+65",
            "visaFreeCountries": "US citizens: 90 days visa-free. Among easiest countries to visit.",
            "timeZone": "UTC+08:00",
            "bestTimeToVisit": "Year-round (tropical 28-32C). February-April slightly drier."
        },
        "cultural": {
            "tipping": "Not expected. 10% service charge + 7% GST usually added. Don't tip at hawker centres.",
            "dressCode": "Casual. Smart casual for nice restaurants. Bring jacket for AC.",
            "greetings": "Handshake. English is common language. 'Hello' works universally.",
            "taboos": ["Littering (SGD $300 fine)", "Chewing gum (banned)", "Jaywalking", "Eating on MRT (SGD $500 fine)", "Drug possession (death penalty for trafficking)"],
            "haggling": "Only at some tourist markets. Singapore is a fixed-price society."
        },
        "connectivity": {
            "simOptions": "Singtel, StarHub, or M1 tourist SIMs at Changi vending machines. SGD 15-38.",
            "wifiAvailability": "Excellent free WiFi everywhere. Wireless@SG is government network.",
            "bestOption": "Singtel tourist SIM at Changi. World-class 5G coverage."
        },
        "phrases": [
            {"english": "Hello", "local": "Hello / Ni hao", "phonetic": "heh-loh / nee how"},
            {"english": "Thank you", "local": "Thank you / Xièxiè", "phonetic": "thank yoo / syeh-syeh"},
            {"english": "Excuse me / Sorry", "local": "Excuse me / Paiseh", "phonetic": "ex-kyooz mee / pai-seh"},
            {"english": "Yes", "local": "Yes / Can", "phonetic": "yes / kan"},
            {"english": "No", "local": "No / Cannot", "phonetic": "noh / kah-not"},
            {"english": "Please", "local": "Please", "phonetic": "pleez"},
            {"english": "How much?", "local": "How much?", "phonetic": "how much"},
            {"english": "Where is...?", "local": "Where is...?", "phonetic": "wair iz"},
            {"english": "Help!", "local": "Help!", "phonetic": "help"},
            {"english": "Goodbye", "local": "Bye", "phonetic": "bai"}
        ]
    }
}

# ── Data loaders ─────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_us_advisories():
    data = load_json(DATA_DIR / "advisories-us.json")
    return data.get("advisories", {})

def load_uk_advisories():
    data = load_json(DATA_DIR / "advisories-uk.json")
    return data.get("advisories", {})

def load_emergency_numbers():
    data = load_json(DATA_DIR / "emergency-numbers.json")
    return data.get("countries", {})

def extract_health_data(slug):
    path = HEALTH_DIR / slug / "index.html"
    if not path.exists():
        return {"summary": "", "vaccinations": [], "risks": []}
    try:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        meta = soup.find("meta", attrs={"name": "description"})
        summary = meta["content"] if meta else ""
        return {"summary": summary, "vaccinations": [], "risks": []}
    except Exception:
        return {"summary": "", "vaccinations": [], "risks": []}

def extract_scam_data(city_slugs):
    scams = []
    for slug in city_slugs:
        path = SCAMS_DIR / slug / "index.html"
        if not path.exists():
            continue
        try:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            cards = soup.find_all("div", class_=re.compile(r"scam"))
            for card in cards[:5]:
                title = card.find(["h2", "h3"])
                desc = card.find("p")
                if title:
                    scams.append({
                        "name": title.get_text(strip=True),
                        "city": slug,
                        "severity": "medium",
                        "description": desc.get_text(strip=True) if desc else "",
                        "avoidanceTip": ""
                    })
        except Exception:
            pass
    return scams

# ── Profile builder ──────────────────────────────────────────────────────────

def build_profile(iso2, config):
    us_advisories = load_us_advisories()
    uk_advisories = load_uk_advisories()
    emergency = load_emergency_numbers()

    us_adv = us_advisories.get(iso2, {})
    uk_adv = uk_advisories.get(iso2, {})
    emerg = emergency.get(iso2, {})

    health_data = extract_health_data(config["health_slug"])
    scam_data = extract_scam_data(config.get("scam_cities", []))

    return {
        "id": f"safety:{iso2.lower()}",
        "iso2": iso2,
        "name": config["name"],
        "lastUpdated": TODAY,
        "emergency": {
            "police": emerg.get("police", ""),
            "ambulance": emerg.get("ambulance", ""),
            "fire": emerg.get("fire", ""),
            "universal": emerg.get("universal", "")
        },
        "embassies": {},
        "travelAdvisory": {
            "source": "US Department of State",
            "level": us_adv.get("level", 0),
            "levelText": us_adv.get("levelText", ""),
            "summary": us_adv.get("summary", ""),
            "lastUpdated": us_adv.get("lastUpdated", "")
        },
        "travelAdvisoryUK": {
            "source": "UK FCDO",
            "level": uk_adv.get("level", ""),
            "summary": uk_adv.get("summary", ""),
            "lastUpdated": uk_adv.get("lastUpdated", "")
        },
        "healthcare": {
            "summary": health_data["summary"],
            "quality": "",
            "vaccinations": health_data["vaccinations"],
            "risks": health_data["risks"]
        },
        "medications": [],
        "scams": scam_data,
        "connectivity": config["connectivity"],
        "cultural": config["cultural"],
        "phrases": config["phrases"],
        "safety": {
            "overallRisk": "",
            "soloFemaleSafety": "",
            "lgbtSafety": "",
            "nightSafety": ""
        },
        "practical": config["practical"]
    }

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    SAFETY_DIR.mkdir(parents=True, exist_ok=True)

    existing = set(f.stem.upper() for f in SAFETY_DIR.glob("*.json"))
    new_countries = {k: v for k, v in COUNTRIES.items() if k not in existing}

    if not new_countries:
        print("All 20 expanded profiles already exist. Nothing to do.")
        return

    print(f"Building {len(new_countries)} new safety profiles...")
    built = []
    for iso2, config in sorted(new_countries.items()):
        print(f"  \u270d\ufe0f  {iso2} ({config['name']})...")
        profile = build_profile(iso2, config)
        out_path = SAFETY_DIR / f"{iso2.lower()}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        built.append(iso2)

    print(f"\n\u2705 Built {len(built)} new profiles: {', '.join(built)}")
    print(f"\nTotal profiles: {len(list(SAFETY_DIR.glob('*.json')))}")

if __name__ == "__main__":
    main()
