#!/usr/bin/env python3
"""Generate scam pages for all cities based on Barcelona template."""
import json
import os
import glob
from collections import defaultdict

# ── Region-appropriate ride-service advice ─────────────────────────────
_REGION_SETS = {
    "southeast_asia": {"th", "vn", "kh", "la", "my", "id", "ph", "sg", "mm"},
    "east_asia": {"jp", "kr", "tw", "cn", "hk", "mo"},
    "south_asia": {"in", "np", "lk", "bd"},
    "europe": {
        "gb", "fr", "de", "it", "es", "pt", "nl", "be", "at", "ch", "ie", "se",
        "dk", "no", "fi", "is", "gr", "tr", "pl", "cz", "sk", "hu", "ro", "bg",
        "hr", "si", "rs", "ba", "me", "al", "mk", "xk", "lt", "lv", "ee",
        "ua", "ru", "ge", "am", "az", "mc", "mt", "cy", "lu", "li", "ad", "sm",
        "va", "kz", "uz",
    },
    "north_america": {"us", "ca", "pr"},
    "latin_america_caribbean": {
        "mx", "gt", "bz", "sv", "hn", "ni", "cr", "pa",
        "co", "ve", "ec", "pe", "bo", "cl", "ar", "uy", "py", "br", "gy", "sr",
        "jm", "ht", "do", "tt", "bb", "lc", "ag", "bs", "ky", "tc", "cw",
        "gd", "dm", "kn", "vc",
    },
    "middle_east": {"ae", "qa", "jo", "il", "sa", "om", "lb", "bh", "kw", "iq", "ye"},
    "africa": {
        "za", "ke", "tz", "eg", "ma", "ng", "gh", "sn", "et", "ug", "rw",
        "zm", "mz", "na", "tn", "dj", "sc", "mu", "mg", "cm", "ci",
        "bw", "zw", "mw", "ao", "cd", "cg", "ga", "ne",
    },
    "oceania": {"au", "nz", "fj", "pf", "mv"},
    "cuba": {"cu"},
}
_RIDE_ADVICE = {
    "southeast_asia": "Use app-based ride services (Grab, Gojek) instead of street taxis \u2014 always confirm the fare before departure",
    "east_asia": "Use app-based ride services or official metered taxis \u2014 avoid unmarked vehicles near tourist areas",
    "south_asia": "Use app-based ride services (Uber, Ola) instead of street taxis \u2014 always confirm the fare before departure",
    "europe": "Use app-based ride services (Uber, Bolt) or official metered taxis instead of unmarked vehicles",
    "north_america": "Use app-based ride services (Uber, Lyft) instead of unmarked vehicles or unlicensed cabs",
    "latin_america_caribbean": "Use app-based ride services (Uber, DiDi) instead of street taxis \u2014 avoid unmarked vehicles, especially at night",
    "middle_east": "Use app-based ride services (Uber, Careem) or official metered taxis instead of unmarked vehicles",
    "africa": "Use app-based ride services (Uber, Bolt) instead of unmarked taxis \u2014 always confirm the fare before departure",
    "oceania": "Use app-based ride services (Uber) or official metered taxis instead of unmarked vehicles",
    "cuba": "Negotiate taxi fares before departure and use official yellow taxis or your hotel\u2019s recommended transport",
}

def _get_ride_advice(country_code):
    """Return region-appropriate ride-service advice based on country code."""
    cc = country_code.lower().strip() if country_code else ""
    for region, codes in _REGION_SETS.items():
        if cc in codes:
            return _RIDE_ADVICE[region]
    # Fallback for unmapped countries
    return "Use app-based ride services or official metered taxis instead of unmarked vehicles"

# Emergency numbers per country
EMERGENCY_INFO = {
    "United Kingdom": {
        "police_name": "Metropolitan Police",
        "police_number": "999 (emergency) or 101 (non-emergency)",
        "emergency_number": "999",
        "report_url": "https://www.met.police.uk/ro/report/",
        "report_site": "met.police.uk",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 33 Nine Elms Lane, London SW11 7US. For emergencies: +44 20 7499 9000.",
    },
    "Japan": {
        "police_name": "Japanese Police (Keisatsu)",
        "police_number": "110",
        "emergency_number": "119",
        "report_url": "https://www.keishicho.metro.tokyo.lg.jp/multilingual/english/",
        "report_site": "keishicho.metro.tokyo.lg.jp",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 1-10-5 Akasaka, Minato-ku, Tokyo. For emergencies: +81 3-3224-5000.",
    },
    "United Arab Emirates": {
        "police_name": "Dubai Police",
        "police_number": "999",
        "emergency_number": "998",
        "report_url": "https://www.dubaipolice.gov.ae/wps/portal/home/crimes/reportacrime",
        "report_site": "dubaipolice.gov.ae",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General is at Corner of Al Seef Road & Sheikh Khalifa Bin Zayed Road, Dubai. For emergencies: +971 4-309-4000.",
    },
    "Netherlands": {
        "police_name": "Dutch Police (Politie)",
        "police_number": "0900-8844 (non-emergency) or 112 (emergency)",
        "emergency_number": "112",
        "report_url": "https://www.politie.nl/aangifte-of-melding-doen/aangifte-doen.html",
        "report_site": "politie.nl",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate Amsterdam is at Museumplein 19, 1071 DJ Amsterdam. For emergencies: +31 70 310 2209.",
    },
    "Singapore": {
        "police_name": "Singapore Police Force",
        "police_number": "999",
        "emergency_number": "995",
        "report_url": "https://www.police.gov.sg/I-Witness",
        "report_site": "police.gov.sg",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 27 Napier Road, Singapore 258508. For emergencies: +65 6476-9100.",
    },
    "Hong Kong": {
        "police_name": "Hong Kong Police Force",
        "police_number": "999",
        "emergency_number": "999",
        "report_url": "https://www.police.gov.hk/ppp_en/04_crime_matters/",
        "report_site": "police.gov.hk",
        "lost_passport": "Contact your nearest consulate. The US Consulate General is at 26 Garden Road, Central, Hong Kong. For emergencies: +852 2523-9011.",
    },
    "Malaysia": {
        "police_name": "Royal Malaysia Police (PDRM)",
        "police_number": "999",
        "emergency_number": "994",
        "report_url": "https://www.rmp.gov.my/",
        "report_site": "rmp.gov.my",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at No. 376, Jalan Tun Razak, 50400 Kuala Lumpur. For emergencies: +60 3-2168-5000.",
    },
    "South Korea": {
        "police_name": "Korean National Police",
        "police_number": "112",
        "emergency_number": "119",
        "report_url": "https://www.police.go.kr/eng/",
        "report_site": "police.go.kr",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 188 Sejong-daero, Jongno-gu, Seoul. For emergencies: +82 2-397-4114.",
    },
    "Portugal": {
        "police_name": "PSP (Polícia de Segurança Pública)",
        "police_number": "112",
        "emergency_number": "112",
        "report_url": "https://www.psp.pt/Pages/reportarcrime.aspx",
        "report_site": "psp.pt",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Av. das Forças Armadas, 1600-081 Lisbon. For emergencies: +351 21 727-3300.",
    },
    "Greece": {
        "police_name": "Tourist Police (Τουριστική Αστυνομία)",
        "police_number": "171 (Tourist Police, English-speaking, 24/7) or 100 (General Police)",
        "emergency_number": "112 (General Emergency), 166 (Medical), 171 (Tourist Police)",
        "report_url": "https://www.astynomia.gr/",
        "report_site": "astynomia.gr",
        "lost_passport": "For passport replacement, contact the US Embassy Athens at 91 Vassilisis Sophias Avenue, 10160 Athens (+30 210-721-2951, 24/7 emergency). The UK Embassy is at 1 Ploutarchou Street, Athens (+30 210-727-2600). The Australian Embassy is at Level 6, Thon Building, Kifisias & Alexandras Avenues, Athens (+30 210-870-4000). Always call Tourist Police 171 first — they speak English and will file the police report you need for passport replacement and insurance claims.",
    },
    "Germany": {
        "police_name": "German Police (Polizei)",
        "police_number": "110",
        "emergency_number": "112",
        "report_url": "https://www.berlin.de/polizei/",
        "report_site": "berlin.de/polizei",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Pariser Platz 2, 10117 Berlin. For emergencies: +49 30 8305-0.",
    },
    "Spain": {
        "police_name": "Policía Nacional or Guardia Civil",
        "police_number": "091 (Policía Nacional) or 112 (emergency)",
        "emergency_number": "112",
        "report_url": "https://www.policia.es/denuncia_web/index.html",
        "report_site": "policia.es",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Calle de Serrano, 75, 28006 Madrid. For emergencies: +34 91 587-2200.",
    },
    "Vietnam": {
        "police_name": "Vietnamese Police (Công An)",
        "police_number": "113",
        "emergency_number": "115",
        "report_url": "https://hanoi.gov.vn/",
        "report_site": "hanoi.gov.vn",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 7 Lang Ha Street, Ba Dinh District, Hanoi. For emergencies: +84 24 3850-5000.",
    },
    "Mexico": {
        "police_name": "Mexican Police (Policía)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.gob.mx/policiafederal",
        "report_site": "gob.mx",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Paseo de la Reforma 305, Cuauhtémoc, 06500 Mexico City. For emergencies: +52 55-5080-2000.",
    },
    "Brazil": {
        "police_name": "Civil Police (Polícia Civil)",
        "police_number": "190 (emergency) or 197 (civil police)",
        "emergency_number": "192",
        "report_url": "https://www.delegaciaonline.rj.gov.br/",
        "report_site": "delegaciaonline.rj.gov.br",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General is at Av. Presidente Wilson, 147, Centro, Rio de Janeiro. For emergencies: +55 21 3823-2000.",
    },
    "Peru": {
        "police_name": "Peruvian National Police (PNP)",
        "police_number": "105",
        "emergency_number": "116",
        "report_url": "https://www.pnp.gob.pe/",
        "report_site": "pnp.gob.pe",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Av. La Encalada Cdra. 17 s/n, Surco, Lima. For emergencies: +51 1-618-2000.",
    },
    "Poland": {
        "police_name": "Polish Police (Policja)",
        "police_number": "997 or 112",
        "emergency_number": "112",
        "report_url": "https://www.policja.pl/",
        "report_site": "policja.pl",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate in Krakow is at ul. Stolarska 9, 31-043 Krakow. For emergencies: +48 12 424-5100.",
    },
    "France": {
        "police_name": "Police Nationale / SAMU",
        "police_number": "17 (Police) or 15 (SAMU medical)",
        "emergency_number": "112",
        "report_url": "https://www.pre-plainte-en-ligne.interieur.gouv.fr/",
        "report_site": "pre-plainte-en-ligne.interieur.gouv.fr",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Paris is at 2 Avenue Gabriel, 75008 Paris. For emergencies: +33 1 43-12-22-22.",
    },
    "Italy": {
        "police_name": "Carabinieri / Polizia di Stato",
        "police_number": "112 (Carabinieri) or 113 (Polizia)",
        "emergency_number": "118",
        "report_url": "https://www.poliziadistato.it/",
        "report_site": "poliziadistato.it",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Rome is at Via Vittorio Veneto 121, 00187 Rome. For emergencies: +39 06-4674-1.",
    },
    "Thailand": {
        "police_name": "Tourist Police",
        "police_number": "1155 (Tourist Police) or 191 (General Police)",
        "emergency_number": "191",
        "report_url": "https://www.touristpolice.go.th/",
        "report_site": "touristpolice.go.th",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Bangkok is at 95 Wireless Road, Pathumwan, Bangkok 10330. For emergencies: +66 2-205-4000.",
    },
    "Turkey": {
        "police_name": "Turkish National Police (Emniyet)",
        "police_number": "155 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.egm.gov.tr/",
        "report_site": "egm.gov.tr",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Istanbul is at Kaplicalar Mevkii No. 2, İstinye, 34460 Istanbul. For emergencies: +90 212-335-9000.",
    },
    "Czech Republic": {
        "police_name": "Czech Police (Policie ČR)",
        "police_number": "158 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.policie.cz/",
        "report_site": "policie.cz",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Prague is at Tržiště 15, 118 01 Prague 1. For emergencies: +420 257-022-000.",
    },
    "Morocco": {
        "police_name": "Sûreté Nationale (DGSN)",
        "police_number": "19 (Police) or 15 (Emergency/SAMU)",
        "emergency_number": "15",
        "report_url": "https://www.dgsn.ma/",
        "report_site": "dgsn.ma",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Casablanca is at 8 Boulevard Moulay Youssef, Casablanca. For emergencies: +212 522-64-2099.",
    },
    "Egypt": {
        "police_name": "Egyptian Police / Tourist Police",
        "police_number": "122 (Police) or 123 (Emergency)",
        "emergency_number": "123",
        "report_url": "https://www.moi.gov.eg/",
        "report_site": "moi.gov.eg",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Cairo is at 5 Tawfik Diab Street, Garden City, Cairo. For emergencies: +20 2-2797-3300.",
    },
    "Argentina": {
        "police_name": "Policía Federal Argentina",
        "police_number": "911 (Police) or 107 (Medical Emergency)",
        "emergency_number": "107",
        "report_url": "https://www.fiscales.gob.ar/",
        "report_site": "fiscales.gob.ar",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Buenos Aires is at Avenida Colombia 4300, C1425GMN Buenos Aires. For emergencies: +54 11-5777-4533.",
    },
    "United States": {
        "police_name": "Local Police Department",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.usa.gov/crimes",
        "report_site": "usa.gov/crimes",
        "lost_passport": "Visit the nearest US Passport Agency. For international visitors, contact your country's consulate or embassy directly. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "United States (New York City)": {
        "police_name": "New York City Police Department (NYPD)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.nyc.gov/site/nypd/index.page",
        "report_site": "nyc.gov/nypd",
        "lost_passport": "Visit the nearest US Passport Agency. The New York Passport Agency is at 376 Hudson Street, New York, NY 10014. For international visitors, contact your country's consulate directly.",
    },
    "United States (New Orleans)": {
        "police_name": "New Orleans Police Department (NOPD)",
        "police_number": "911 (Emergency) or 504-821-2222 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://nola.gov/next/nopd/",
        "report_site": "nola.gov/nopd",
        "lost_passport": "For international visitors, contact your country's consulate. Many nations maintain consulates in New Orleans or Houston. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "Austria": {
        "police_name": "Austrian Federal Police (Bundespolizei)",
        "police_number": "133 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.polizei.gv.at/",
        "report_site": "polizei.gv.at",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Vienna is at Boltzmanngasse 16, 1090 Vienna. For emergencies: +43 1-31339-0.",
    },
    "Canada": {
        "police_name": "Vancouver Police Department (VPD)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://vpd.ca/",
        "report_site": "vpd.ca",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Vancouver is at 1075 West Pender Street, Vancouver, BC V6E 2M6. For emergencies: +1 604-685-4311.",
    },
    "Ireland": {
        "police_name": "An Garda Síochána",
        "police_number": "999 or 112",
        "emergency_number": "999",
        "report_url": "https://www.garda.ie/",
        "report_site": "garda.ie",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Dublin is at 42 Elgin Road, Ballsbridge, Dublin 4. For emergencies: +353 1-668-8777.",
    },
    "Denmark": {
        "police_name": "Danish Police (Politi)",
        "police_number": "114 (non-emergency) or 112 (emergency)",
        "emergency_number": "112",
        "report_url": "https://politi.dk/en",
        "report_site": "politi.dk",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Copenhagen is at Dag Hammarskjölds Allé 24, 2100 Copenhagen. For emergencies: +45 33 41 71 00.",
    },
    "Hungary": {
        "police_name": "Hungarian Police (Rendőrség)",
        "police_number": "107 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.police.hu/en",
        "report_site": "police.hu",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Budapest is at Szabadság tér 12, 1054 Budapest. For emergencies: +36 1-475-4400.",
    },
    "Croatia": {
        "police_name": "Croatian Police (Policija)",
        "police_number": "192 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://mup.gov.hr/",
        "report_site": "mup.gov.hr",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Zagreb is at Ulica Thomasa Jeffersona 2, 10010 Zagreb. For emergencies: +385 1-661-2200.",
    },
    "Jordan": {
        "police_name": "Public Security Directorate (PSD)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.psd.gov.jo/",
        "report_site": "psd.gov.jo",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Amman is at Al-Umayyaween Street, Abdoun, Amman. For emergencies: +962 6-590-6000.",
    },
    "Israel": {
        "police_name": "Israel Police (Mishtara)",
        "police_number": "100 (Police) or 101 (Ambulance)",
        "emergency_number": "100",
        "report_url": "https://www.police.gov.il/",
        "report_site": "police.gov.il",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Jerusalem is at 14 David Flusser Street, Jerusalem 9378322. For emergencies: +972 2-630-4000.",
    },
    "Iceland": {
        "police_name": "Icelandic Police (Lögreglan)",
        "police_number": "112",
        "emergency_number": "112",
        "report_url": "https://www.logreglan.is/english/",
        "report_site": "logreglan.is",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Reykjavik is at Laufásvegur 21, 101 Reykjavik. For emergencies: +354 595-2200.",
    },
    "Belgium": {
        "police_name": "Belgian Federal Police (Politie/Police)",
        "police_number": "101 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.police.be/",
        "report_site": "police.be",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Brussels is at Boulevard du Régent 27, 1000 Brussels. For emergencies: +32 2-811-4000.",
    },
    "Cambodia": {
        "police_name": "Cambodian Tourist Police",
        "police_number": "117 (Police) or 119 (Emergency)",
        "emergency_number": "119",
        "report_url": "https://www.tourismcambodia.com/",
        "report_site": "tourismcambodia.com",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Phnom Penh is at #1, Street 96, Sangkat Wat Phnom, Khan Daun Penh. For emergencies: +855 23-728-000.",
    },
    "Philippines": {
        "police_name": "Philippine National Police (PNP)",
        "police_number": "911 or 117 (PNP Hotline)",
        "emergency_number": "911",
        "report_url": "https://pnp.gov.ph/",
        "report_site": "pnp.gov.ph",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Manila is at 1201 Roxas Boulevard, Ermita, Manila 1000. For emergencies: +63 2-5301-2000.",
    },
    "Cuba": {
        "police_name": "Policía Nacional Revolucionaria (PNR)",
        "police_number": "106 (Police) or 104 (Ambulance)",
        "emergency_number": "106",
        "report_url": "https://www.minint.gob.cu/",
        "report_site": "minint.gob.cu",
        "lost_passport": "Contact the US Embassy in Havana at Calzada between L & M Streets, Vedado, Havana. For emergencies: +53 7-839-4100.",
    },
    "Puerto Rico": {
        "police_name": "Puerto Rico Police Bureau (PRPB)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://policia.pr.gov/",
        "report_site": "policia.pr.gov",
        "lost_passport": "Puerto Rico is a US territory. Visit the nearest US Passport Agency or Federal Building at 150 Carlos Chardon Ave, San Juan, PR 00918. For general assistance: +1 787-766-5000.",
    },
    "Colombia": {
        "police_name": "Colombian National Police (Policía Nacional)",
        "police_number": "123 (Emergency) or 112",
        "emergency_number": "123",
        "report_url": "https://www.policia.gov.co/",
        "report_site": "policia.gov.co",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Bogotá is at Calle 24 Bis No. 48-50, Bogotá. For emergencies: +57 1-275-2000.",
    },
    "Scotland": {
        "police_name": "Police Scotland",
        "police_number": "999 (emergency) or 101 (non-emergency)",
        "emergency_number": "999",
        "report_url": "https://www.scotland.police.uk/",
        "report_site": "scotland.police.uk",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Edinburgh is at 3 Regent Terrace, Edinburgh EH7 5BW. For emergencies: +44 131 556 8315.",
    },
    "Indonesia": {
        "police_name": "Indonesian National Police (Polri)",
        "police_number": "110 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.polri.go.id/",
        "report_site": "polri.go.id",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Jakarta is at Jl. Merdeka Selatan No. 3-5, Jakarta 10110. For emergencies: +62 21-5083-1000.",
    },
    "India": {
        "police_name": "Indian Police",
        "police_number": "100 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.citizenservices.gov.in/",
        "report_site": "citizenservices.gov.in",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in New Delhi is at Shantipath, Chanakyapuri, New Delhi 110021. For emergencies: +91 11-2419-8000.",
    },
    "Taiwan": {
        "police_name": "National Police Agency (NPA)",
        "police_number": "110 (Police) or 119 (Fire/Ambulance)",
        "emergency_number": "110",
        "report_url": "https://www.npa.gov.tw/",
        "report_site": "npa.gov.tw",
        "lost_passport": "Contact the American Institute in Taiwan (AIT) at No. 100, Jinhu Road, Neihu District, Taipei 11461. For emergencies: +886 2-2162-2000.",
    },
    "Nepal": {
        "police_name": "Nepal Police",
        "police_number": "100 (Police) or 102 (Emergency)",
        "emergency_number": "100",
        "report_url": "https://www.nepalpolice.gov.np/",
        "report_site": "nepalpolice.gov.np",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Kathmandu is at Maharajgunj, Kathmandu. For emergencies: +977 1-423-4000.",
    },
    "China": {
        "police_name": "Chinese Police (公安局)",
        "police_number": "110 (Police) or 120 (Ambulance)",
        "emergency_number": "110",
        "report_url": "https://www.mps.gov.cn/",
        "report_site": "mps.gov.cn",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Beijing is at No. 55 An Jia Lou Road, Chaoyang District, Beijing 100600. For emergencies: +86 10-8531-3000.",
    },
    "China (SAR)": {
        "police_name": "Hong Kong Police Force",
        "police_number": "999",
        "emergency_number": "999",
        "report_url": "https://www.police.gov.hk/ppp_en/04_crime_matters/",
        "report_site": "police.gov.hk",
        "lost_passport": "Contact the US Consulate General in Hong Kong at 26 Garden Road, Central, Hong Kong. For emergencies: +852 2523-9011.",
    },
    "Laos": {
        "police_name": "Lao Police",
        "police_number": "1191 (Police) or 1195 (Ambulance)",
        "emergency_number": "1191",
        "report_url": "https://www.laopdr.gov.la/",
        "report_site": "laopdr.gov.la",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Vientiane is at Thadeua Road, Km 9, Ban Somvang Tai, Hatsayfong District, Vientiane. For emergencies: +856 21-48-7000.",
    },
    "Romania": {
        "police_name": "Romanian Police (Poliția Română)",
        "police_number": "112",
        "emergency_number": "112",
        "report_url": "https://www.politiaromana.ro/",
        "report_site": "politiaromana.ro",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Bucharest is at Bulevardul Dr. Liviu Librescu 4-6, Sector 1, 015118 Bucharest. For emergencies: +40 21-200-3300.",
    },
    "Bulgaria": {
        "police_name": "Bulgarian Police (Полиция)",
        "police_number": "166 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.mvr.bg/",
        "report_site": "mvr.bg",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Sofia is at 16 Kozyak Street, Sofia 1408. For emergencies: +359 2-937-5100.",
    },
    "Serbia": {
        "police_name": "Serbian Police (Полиција)",
        "police_number": "192 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.mup.gov.rs/",
        "report_site": "mup.gov.rs",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Belgrade is at Bulevar kneza Aleksandra Karađorđevića 92, 11040 Belgrade. For emergencies: +381 11-706-4000.",
    },
    "Estonia": {
        "police_name": "Estonian Police and Border Guard Board",
        "police_number": "110 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.politsei.ee/",
        "report_site": "politsei.ee",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Tallinn is at Kentmanni 20, 15099 Tallinn. For emergencies: +372 668-8100.",
    },
    "Montenegro": {
        "police_name": "Montenegrin Police (Uprava Policije)",
        "police_number": "122 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.gov.me/mup",
        "report_site": "gov.me/mup",
        "lost_passport": "Contact the US Embassy in Podgorica at Dzona Dzeksona bb, 81000 Podgorica. For emergencies: +382 20-410-500.",
    },
    "South Africa": {
        "police_name": "South African Police Service (SAPS)",
        "police_number": "10111 (Police) or 112 (Emergency from mobile)",
        "emergency_number": "10111",
        "report_url": "https://www.saps.gov.za/",
        "report_site": "saps.gov.za",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Cape Town is at 2 Reddam Avenue, Westlake 7945. For emergencies: +27 21-702-7300.",
    },
    "Kenya": {
        "police_name": "Kenya Police Service",
        "police_number": "999 or 112 (Emergency)",
        "emergency_number": "999",
        "report_url": "https://www.nationalpolice.go.ke/",
        "report_site": "nationalpolice.go.ke",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Nairobi is at United Nations Avenue, Gigiri, Nairobi. For emergencies: +254 20-363-6000.",
    },
    "Tanzania": {
        "police_name": "Tanzania Police Force",
        "police_number": "112 or 114 (Police)",
        "emergency_number": "112",
        "report_url": "https://www.polisi.go.tz/",
        "report_site": "polisi.go.tz",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Dar es Salaam is at 686 Old Bagamoyo Road, Msasani, Dar es Salaam. For emergencies: +255 22-229-4000.",
    },
    "Ghana": {
        "police_name": "Ghana Police Service",
        "police_number": "191 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://police.gov.gh/",
        "report_site": "police.gov.gh",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Accra is at No. 24, Fourth Circular Road, Cantonments, Accra. For emergencies: +233 30-274-1000.",
    },
    "Australia": {
        "police_name": "Australian Federal Police / State Police",
        "police_number": "000 (Emergency) or 131 444 (Non-emergency)",
        "emergency_number": "000",
        "report_url": "https://www.police.nsw.gov.au/",
        "report_site": "police.nsw.gov.au",
        "lost_passport": "Contact your nearest embassy or consulate. The US Consulate General in Sydney is at MLC Centre, Level 10, 19-29 Martin Place, Sydney NSW 2000. For emergencies: +61 2-9373-9200.",
    },
    "Sri Lanka": {
        "police_name": "Sri Lanka Police",
        "police_number": "119 (Police) or 110 (Emergency)",
        "emergency_number": "119",
        "report_url": "https://www.police.lk/",
        "report_site": "police.lk",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Colombo is at 210 Galle Road, Colombo 03. For emergencies: +94 11-249-8500.",
    },
    "The Bahamas": {
        "police_name": "Royal Bahamas Police Force",
        "police_number": "919 (Police) or 911 (Emergency)",
        "emergency_number": "919",
        "report_url": "https://www.royalbahamaspolice.org/",
        "report_site": "royalbahamaspolice.org",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Nassau is at 42 Queen Street, Nassau. For emergencies: +1 242-322-1181.",
    },
    "Aruba": {
        "police_name": "Korps Politie Aruba (KPA)",
        "police_number": "100 (Police) or 911 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://kpa.aw/",
        "report_site": "kpa.aw",
        "lost_passport": "Contact the US Consulate General in Curacao at +(599)(9) 461-3066. After-hours: +(599)(9) 510-6870. There is no US embassy on Aruba — the nearest consular services are in Curacao.",
    },
    "Dominican Republic": {
        "police_name": "POLITUR (Tourist Police)",
        "police_number": "+1 809-200-3500 (Tourist Police) or 911 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://politur.gob.do/",
        "report_site": "politur.gob.do",
        "lost_passport": "Contact the US Embassy in Santo Domingo at +1 (809) 567-7775 (24/7). Address: 57 Avenida Republica de Colombia, Arroyo Hondo, Santo Domingo.",
    },
    "Antigua and Barbuda": {
        "police_name": "Royal Police Force of Antigua and Barbuda",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://police.gov.ag/",
        "report_site": "Royal Police Force of Antigua and Barbuda",
        "lost_passport": "Contact the U.S. Embassy in Bridgetown, Barbados (which covers Antigua) at +1 (246) 227-4000. File a police report first with the Royal Police Force at 911 or Police HQ at +268 462-0125. Bring the police report and proof of identity to the embassy for an emergency travel document. From the U.S., call 1-888-407-4747 for after-hours emergencies.",
    },
    "Honduras": {
        "police_name": "Policia Nacional de Honduras",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://roatantourismbureau.com/emergency-numbers",
        "report_site": "Roatan Tourism Bureau Emergency Numbers",
        "lost_passport": "Contact the U.S. Embassy in Tegucigalpa at +(504) 2217-5000. File a police report locally first, then appear in person at the Embassy in Tegucigalpa or the Consular Agency in San Pedro Sula with a completed DS-64 form (Statement Regarding Lost or Stolen Passport) and your police report. From the U.S., call 1-888-407-4747 for after-hours emergencies. Note: there is no U.S. consulate on Roatan — the nearest is on the mainland.",
    },
    "Colombia (Cartagena)": {
        "police_name": "Policía Nacional de Colombia / Policía de Turismo",
        "police_number": "123 (emergency) / 112 (national line)",
        "emergency_number": "123",
        "report_url": "https://adenunciar.policia.gov.co/adenunciar/",
        "report_site": "ADenunciar (Colombian National Police Online Report - Spanish only)",
        "lost_passport": "File a police report (denuncia) at the nearest CAI (police station) or through ADenunciar online. Contact your embassy: the U.S. Embassy in Bogotá (+57-601-275-2000) can coordinate with the honorary consular agent in Cartagena. Bring a passport photo and any identification for an emergency travel document. The process typically takes one to three business days.",
    },
    "United States (Chicago)": {
        "police_name": "Chicago Police Department (CPD)",
        "police_number": "911 (Emergency) or 311 / (312) 746-6000 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.chicago.gov/city/en/depts/cpd.html",
        "report_site": "chicago.gov/cpd",
        "lost_passport": "For international visitors, contact your country's consulate in Chicago. Many nations maintain consulates downtown. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "United States (Boston)": {
        "police_name": "Boston Police Department (BPD)",
        "police_number": "911 (Emergency) or (617) 343-4200 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.boston.gov/departments/police",
        "report_site": "boston.gov/police",
        "lost_passport": "For international visitors, contact your country's consulate in Boston. Many nations maintain consulates in the city. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "United States (San Diego)": {
        "police_name": "San Diego Police Department (SDPD)",
        "police_number": "911 (Emergency) or (619) 531-2000 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.sandiego.gov/police",
        "report_site": "sandiego.gov/police",
        "lost_passport": "For international visitors, contact your country's consulate in San Diego. Mexico maintains a consulate at 1549 India St. — (619) 231-8414. US State Department emergency line: +1-888-407-4747.",
    },
    "United States (Seattle)": {
        "police_name": "Seattle Police Department (SPD)",
        "police_number": "911 (Emergency) or (206) 625-5011 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.seattle.gov/police/need-help",
        "report_site": "seattle.gov/police",
        "lost_passport": "For international visitors, contact your country's consulate. Many nations maintain consulates in Seattle. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "United States (Nashville)": {
        "police_name": "Metro Nashville Police Department (MNPD)",
        "police_number": "911 (Emergency) or 615-862-8600 (Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.nashville.gov/departments/police",
        "report_site": "nashville.gov/police",
        "lost_passport": "For international visitors, contact your country's consulate. The nearest major consulates are in Atlanta. US State Department emergency line: +1-888-407-4747 (from US) or +1-202-501-4444 (international).",
    },
    "Panama": {
        "police_name": "Panama National Police (Policía Nacional de Panamá)",
        "police_number": "911 (Emergency) or 104 (Police Non-Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.policia.gob.pa/",
        "report_site": "policia.gob.pa",
        "lost_passport": "Contact the US Embassy at Building 783, Demetrio Basilio Lakas Avenue, Clayton, Panama. Emergency phone: +507-317-5000. From the US: 011-507-317-5000. The Embassy can issue emergency travel documents.",
    },
    "Colombia (Bogota)": {
        "police_name": "Colombian National Police (Policía Nacional)",
        "police_number": "123 (Emergency) or 112",
        "emergency_number": "123",
        "report_url": "https://www.policia.gov.co/",
        "report_site": "policia.gov.co",
        "lost_passport": "Contact the US Embassy in Bogotá at Carrera 45 No. 24B-27, Bogotá. Phone: +(57)(1) 275-2000. After-hours emergencies: +(57)(1) 275-4021. From the US: +1-202-501-4444 (24/7). The Embassy can issue emergency travel documents.",
    },
    "El Salvador": {
        "police_name": "Policía Nacional Civil (PNC)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.pnc.gob.sv/",
        "report_site": "pnc.gob.sv",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at Final Boulevard Santa Elena Sur, Antiguo Cuscatlán, La Libertad. For emergencies: +(503) 2501-2999.",
    },
    "Jamaica": {
        "police_name": "Jamaica Constabulary Force",
        "police_number": "119",
        "emergency_number": "110 (fire and ambulance) or 119 (police)",
        "report_url": "https://jcf.gov.jm/contact/",
        "report_site": "jcf.gov.jm",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 142 Old Hope Road, Kingston 6. For emergencies: +1 876 702-6000.",
    },
    "United States (Washington DC)": {
        "police_name": "Metropolitan Police Department (MPDC)",
        "police_number": "(202) 727-9099",
        "emergency_number": "911",
        "report_url": "https://mpdc.dc.gov",
        "report_site": "MPDC Online Reporting",
        "lost_passport": "Contact your embassy on Embassy Row along Massachusetts Avenue NW; most embassies are located between Dupont Circle and the Naval Observatory",
    },
    "Turkey (Antalya)": {
        "police_name": "Turkish National Police (Emniyet Genel Mudurlugu)",
        "police_number": "155",
        "emergency_number": "112",
        "report_url": "https://www.egm.gov.tr",
        "report_site": "Turkish National Police Online Portal",
        "lost_passport": "Contact your country's nearest consulate; many European countries maintain honorary consulates in Antalya. The nearest US Consulate is in Adana. Carry a photocopy of your passport separately from the original.",
    },
    "Egypt (Hurghada)": {
        "police_name": "Egyptian Tourist Police",
        "police_number": "126",
        "emergency_number": "122",
        "report_url": "https://www.egypt.travel",
        "report_site": "Egypt Tourism Authority",
        "lost_passport": "Contact your country's embassy or consulate in Cairo; the nearest consulates for most countries are in Cairo. File a police report at the local Tourist Police station in Hurghada and bring a photocopy of your passport for faster processing.",
    },
    "United States (Portland)": {
        "police_name": "Portland Police Bureau",
        "police_number": "(503) 823-3333",
        "emergency_number": "911",
        "report_url": "https://www.portland.gov/police/cor",
        "report_site": "Portland Police Online Reporting",
        "lost_passport": "Contact your country's consulate; Portland has honorary consulates for several countries. The nearest full-service consulates for most nations are in Seattle or San Francisco. File a police report online at portland.gov for documentation.",
    },
    "United States (Denver)": {
        "police_name": "Denver Police Department",
        "police_number": "720-913-2000",
        "emergency_number": "911",
        "report_url": "https://www.denvergov.org/police",
        "report_site": "Denver Police Online Reporting",
        "lost_passport": "U.S. does not require a passport for domestic travel. International visitors who lose their passport should contact their country's nearest consulate in Denver or the embassy in Washington, D.C.",
    },
    "Cayman Islands": {
        "police_name": "Royal Cayman Islands Police Service (RCIPS)",
        "police_number": "949-4222",
        "emergency_number": "911",
        "report_url": "https://www.rcips.ky",
        "report_site": "Royal Cayman Islands Police Service",
        "lost_passport": "Contact your country's nearest consulate. The U.S. Consular Agency in Grand Cayman is located at the Cayman Corporate Centre, George Town. Call +1 345-945-8173.",
    },
    "Canada (Toronto)": {
        "police_name": "Toronto Police Service",
        "police_number": "416-808-2222",
        "emergency_number": "911",
        "report_url": "https://www.tps.ca/online-reporting/",
        "report_site": "Toronto Police Online Reporting",
        "lost_passport": "Contact your country's consulate in Toronto. The U.S. Consulate General is at 360 University Ave (416-595-1700). For UK citizens, the British Consulate is at 777 Bay Street (416-593-1290).",
    },
    "Spain (Tenerife)": {
        "police_name": "Policía Nacional / Guardia Civil",
        "police_number": "091 (Policía Nacional) / 062 (Guardia Civil)",
        "emergency_number": "112",
        "report_url": "https://www.policia.es/",
        "report_site": "Spanish National Police (Policía Nacional)",
        "lost_passport": "Contact your country's consulate. The British Vice Consulate in Tenerife is in Santa Cruz de Tenerife (928-262-508). The U.S. has no consulate in Tenerife — contact the U.S. Embassy in Madrid (+34 91-587-2200) or the Consulate in Barcelona.",
    },
    "Morocco (Casablanca)": {
        "police_name": "Sûreté Nationale (National Police)",
        "police_number": "19",
        "emergency_number": "112",
        "report_url": "https://www.police.gov.ma",
        "report_site": "Sûreté Nationale Website",
        "lost_passport": "Report to the nearest police station and obtain a police report, then contact your country's embassy or consulate in Casablanca. Tourist police hotline: 177.",
    },
    "United Kingdom (Belfast)": {
        "police_name": "Police Service of Northern Ireland (PSNI)",
        "police_number": "101",
        "emergency_number": "999",
        "report_url": "https://www.psni.police.uk/report",
        "report_site": "PSNI Online Reporting",
        "lost_passport": "Report to the nearest PSNI station and obtain a crime reference number, then contact your country's embassy or consulate. The nearest US consulate is in Belfast at Danesfort House, 223 Stranmillis Road.",
    },
    "Qatar (Doha)": {
        "police_name": "Ministry of Interior — Qatar Police",
        "police_number": "999",
        "emergency_number": "999",
        "report_url": "https://portal.moi.gov.qa",
        "report_site": "Ministry of Interior Portal / Metrash2 App",
        "lost_passport": "Report to the nearest police station and file a report through the Metrash2 app, then contact your country's embassy immediately. Tourism hotline: 106.",
    },
    "Nigeria (Lagos)": {
        "police_name": "Nigeria Police Force — Lagos Command",
        "police_number": "112",
        "emergency_number": "112",
        "report_url": "https://www.npf.gov.ng",
        "report_site": "Nigeria Police Force Website",
        "lost_passport": "Report to the nearest police station and obtain a report, then contact your country's embassy or high commission in Lagos or Abuja. US Consulate Lagos: +234 1 460 3400. Lagos State Emergency: 767.",
    },
    "Ecuador (Quito)": {
        "police_name": "Policía Nacional del Ecuador",
        "police_number": "911 (ECU 911)",
        "emergency_number": "911",
        "report_url": "https://www.ecu911.gob.ec/",
        "report_site": "ecu911.gob.ec",
        "lost_passport": "Contact the US Embassy in Quito at Avenida Avigiras E12-170 y Avenida Eloy Alfaro. Emergency phone: +593-2-398-5000. For other nationalities, check your embassy's location in the Iñaquito district of Quito.",
    },
    "Israel (Tel Aviv)": {
        "police_name": "Israel Police (Mishtara)",
        "police_number": "100",
        "emergency_number": "112 (universal) or 100 (police), 101 (ambulance), 102 (fire)",
        "report_url": "https://www.gov.il/en/departments/israel_police",
        "report_site": "gov.il/israel_police",
        "lost_passport": "Contact the US Embassy in Tel Aviv at 71 HaYarkon Street, Tel Aviv. Phone: +972-3-519-7575. For emergencies after hours: +972-3-519-7551. Other nationalities should check their embassy's Tel Aviv location.",
    },
    "Slovakia (Bratislava)": {
        "police_name": "Polícia Slovenskej republiky (Slovak Police)",
        "police_number": "158",
        "emergency_number": "112 (universal European emergency number)",
        "report_url": "https://www.minv.sk/",
        "report_site": "minv.sk",
        "lost_passport": "Contact the US Embassy in Bratislava at Hviezdoslavovo námestie 4. Phone: +421-2-5443-0861. For after-hours emergencies: +421-2-5443-0861 (follow prompts). Other nationalities should check their embassy's Bratislava location.",
    },
    "Lebanon (Beirut)": {
        "police_name": "Internal Security Forces (ISF / Quwwa al-Amn ad-Dakhili)",
        "police_number": "112",
        "emergency_number": "112",
        "report_url": "https://www.isf.gov.lb/",
        "report_site": "isf.gov.lb",
        "lost_passport": "Contact the US Embassy in Beirut at Awkar, facing the Municipality. Phone: +961-4-542-600. For after-hours emergencies: +961-4-543-600. Other nationalities should check their embassy or consulate location in the Beirut area.",
    },
    "United States (Austin)": {
        "police_name": "Austin Police Department (APD)",
        "police_number": "911 (emergency) or 311 (non-emergency)",
        "emergency_number": "911",
        "report_url": "https://www.austintexas.gov/department/police",
        "report_site": "austintexas.gov/police",
        "lost_passport": "Contact the nearest passport office. The closest regional passport agency is in Houston at the Mickey Leland Federal Building, 1919 Smith Street. For emergencies, call the US State Department at 1-888-407-4747. Foreign nationals should contact their country's nearest consulate.",
    },
    "Russia": {
        "police_name": "Russian Police (Politsiya)",
        "police_number": "102 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://мвд.рф/",
        "report_site": "mvd.rf",
        "lost_passport": "Contact your embassy. The US Embassy in Moscow is at Bolshoy Deviatinsky Pereulok 8. For emergencies: +7 495-728-5000.",
    },
    "Latvia": {
        "police_name": "Latvian State Police (Valsts Policija)",
        "police_number": "110 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.vp.gov.lv/",
        "report_site": "vp.gov.lv",
        "lost_passport": "Contact the US Embassy in Riga at Samnera Velsa iela 1. For emergencies: +371 6710-7000.",
    },
    "Azerbaijan": {
        "police_name": "Azerbaijan Police",
        "police_number": "102 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.mia.gov.az/",
        "report_site": "mia.gov.az",
        "lost_passport": "Contact the US Embassy in Baku at 111 Azadlig Avenue. For emergencies: +994 12-488-3300.",
    },
    "French Polynesia": {
        "police_name": "Gendarmerie Nationale",
        "police_number": "17 (Police) or 15 (SAMU)",
        "emergency_number": "15",
        "report_url": "https://www.service-public.pf/",
        "report_site": "service-public.pf",
        "lost_passport": "Contact the US Consular Agency in Papeete. The nearest US Embassy is in Suva, Fiji: +679 331-4466.",
    },
    "Tunisia": {
        "police_name": "Tunisian National Police",
        "police_number": "197 (Police) or 190 (Emergency)",
        "emergency_number": "197",
        "report_url": "https://www.interieur.gov.tn/",
        "report_site": "interieur.gov.tn",
        "lost_passport": "Contact the US Embassy in Tunis at Les Berges du Lac. For emergencies: +216 71-107-000.",
    },
    "Albania": {
        "police_name": "Albanian State Police (Policia e Shtetit)",
        "police_number": "129 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.asp.gov.al/",
        "report_site": "asp.gov.al",
        "lost_passport": "Contact the US Embassy in Tirana at Rruga Stavro Vinjau 14. For emergencies: +355 4-2247-285.",
    },
    "Georgia": {
        "police_name": "Georgian Police (Patrol Police)",
        "police_number": "112 (Emergency) or 022-241-106 (Police)",
        "emergency_number": "112",
        "report_url": "https://police.ge/",
        "report_site": "police.ge",
        "lost_passport": "Contact the US Embassy in Tbilisi at 11 George Balanchine Street. For emergencies: +995 32-227-7000.",
    },
    "Uruguay": {
        "police_name": "Uruguayan National Police",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.minterior.gub.uy/",
        "report_site": "minterior.gub.uy",
        "lost_passport": "Contact the US Embassy in Montevideo at Lauro Muller 1776. For emergencies: +598 1770-2000.",
    },
    "Switzerland": {
        "police_name": "Swiss Cantonal Police (Kantonspolizei)",
        "police_number": "117 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.police.ch/",
        "report_site": "police.ch",
        "lost_passport": "Contact the US Embassy in Bern at Sulgeneckstrasse 19. For emergencies: +41 31-357-7011.",
    },
    "Ukraine": {
        "police_name": "National Police of Ukraine",
        "police_number": "102 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.npu.gov.ua/",
        "report_site": "npu.gov.ua",
        "lost_passport": "Contact the US Embassy in Kyiv at 4 A.I. Sikorsky Street. For emergencies: +380 44-521-5000.",
    },
    "Senegal": {
        "police_name": "Senegalese National Police",
        "police_number": "17 (Police) or 15 (Emergency)",
        "emergency_number": "17",
        "report_url": "https://www.police.gouv.sn/",
        "report_site": "police.gouv.sn",
        "lost_passport": "Contact the US Embassy in Dakar at Route des Almadies. For emergencies: +221 33-879-4000.",
    },
    "Monaco": {
        "police_name": "Monaco Police (Sûreté Publique)",
        "police_number": "17 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.gouv.mc/",
        "report_site": "gouv.mc",
        "lost_passport": "Contact the US Consulate General in Marseille. The nearest US Consulate is at Place Varian Fry, 13006 Marseille: +33 1-43-12-22-22.",
    },
    "Oman": {
        "police_name": "Royal Oman Police",
        "police_number": "9999 (Police) or 9999 (Emergency)",
        "emergency_number": "9999",
        "report_url": "https://www.rop.gov.om/",
        "report_site": "rop.gov.om",
        "lost_passport": "Contact the US Embassy in Muscat at PCRS, Way 3007, Al Sarooj. For emergencies: +968 2464-3400.",
    },
    "Saudi Arabia": {
        "police_name": "Saudi Arabian Police",
        "police_number": "999 (Police) or 911 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.moi.gov.sa/",
        "report_site": "moi.gov.sa",
        "lost_passport": "Contact the US Embassy in Riyadh at PO Box 94309. For emergencies: +966 11-488-3800.",
    },
    "Turks and Caicos Islands": {
        "police_name": "Royal Turks and Caicos Islands Police Force (RTCIPF)",
        "police_number": "911 or 999",
        "emergency_number": "911",
        "report_url": "https://www.rtcipf.tc/",
        "report_site": "rtcipf.tc",
        "lost_passport": "Contact the US Embassy in Nassau, Bahamas at +1 242-322-1181. There is no US consulate in TCI — the nearest is in Nassau.",
    },
    "Myanmar": {
        "police_name": "Myanmar Police Force",
        "police_number": "199 (Police) or 191 (Emergency)",
        "emergency_number": "199",
        "report_url": "https://www.moi.gov.mm/",
        "report_site": "moi.gov.mm",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Yangon is at 110 University Avenue, Kamayut Township, Yangon. For emergencies: +95 1-753-6509.",
    },
    "Bangladesh": {
        "police_name": "Bangladesh Police",
        "police_number": "999 (Emergency) or 100 (Police)",
        "emergency_number": "999",
        "report_url": "https://www.police.gov.bd/",
        "report_site": "police.gov.bd",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy in Dhaka is at Madani Avenue, Baridhara, Dhaka-1212. For emergencies: +880 2-5566-2000.",
    },
    "Uzbekistan": {
        "police_name": "Uzbekistan Police (Militsiya)",
        "police_number": "102 (Police) or 101 (Fire) or 103 (Ambulance)",
        "emergency_number": "102",
        "report_url": "https://www.iiv.uz/",
        "report_site": "iiv.uz",
        "lost_passport": "Contact the US Embassy in Tashkent at 3 Moyqorghon Street, Tashkent 100093. For emergencies: +998 78-120-5450.",
    },
    "Kazakhstan": {
        "police_name": "Kazakhstan Police",
        "police_number": "102 (Police) or 103 (Ambulance)",
        "emergency_number": "112",
        "report_url": "https://www.gov.kz/",
        "report_site": "gov.kz",
        "lost_passport": "Contact the US Embassy in Astana or Consulate in Almaty at 97 Zholdasbekov Street, Almaty 050010. For emergencies: +7 727-250-4802.",
    },
    "Armenia": {
        "police_name": "Armenian Police",
        "police_number": "102 (Police) or 103 (Ambulance)",
        "emergency_number": "911",
        "report_url": "https://www.police.am/",
        "report_site": "police.am",
        "lost_passport": "Contact the US Embassy in Yerevan at 1 American Avenue, Yerevan 0082. For emergencies: +374 10-464-700.",
    },
    "Lithuania": {
        "police_name": "Lithuanian Police (Policija)",
        "police_number": "112 (Emergency) or 02 (Police)",
        "emergency_number": "112",
        "report_url": "https://www.policija.lt/",
        "report_site": "policija.lt",
        "lost_passport": "Contact the US Embassy in Vilnius at Akmenu gatve 6, LT-03106 Vilnius. For emergencies: +370 5-266-5500.",
    },
    "Nicaragua": {
        "police_name": "Nicaraguan National Police (Policía Nacional)",
        "police_number": "118 (Police) or 911 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.policia.gob.ni/",
        "report_site": "policia.gob.ni",
        "lost_passport": "Contact the US Embassy in Managua at Km 5.5 Carretera Sur, Managua. For emergencies: +505 2252-7100.",
    },
    "Barbados": {
        "police_name": "Royal Barbados Police Force",
        "police_number": "211 (Police) or 511 (Emergency)",
        "emergency_number": "511",
        "report_url": "https://www.barbadospolice.gov.bb/",
        "report_site": "barbadospolice.gov.bb",
        "lost_passport": "Contact the US Embassy in Bridgetown at Wildey Business Park, Wildey, St. Michael. For emergencies: +1 246-227-4000.",
    },
    "Saint Lucia": {
        "police_name": "Royal Saint Lucia Police Force",
        "police_number": "999 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.rslpf.com/",
        "report_site": "rslpf.com",
        "lost_passport": "Contact the US Embassy in Bridgetown, Barbados (which covers Saint Lucia) at +1 246-227-4000. File a police report first, then contact the embassy for an emergency travel document.",
    },
    "Uganda": {
        "police_name": "Uganda Police Force",
        "police_number": "999 (Police) or 112 (Emergency)",
        "emergency_number": "999",
        "report_url": "https://www.upf.go.ug/",
        "report_site": "upf.go.ug",
        "lost_passport": "Contact the US Embassy in Kampala at 1577 Ggaba Road, Kampala. For emergencies: +256 414-259-791.",
    },
    "Zambia": {
        "police_name": "Zambia Police Service",
        "police_number": "999 (Police) or 991 (Ambulance)",
        "emergency_number": "999",
        "report_url": "https://www.zambiapolice.gov.zm/",
        "report_site": "zambiapolice.gov.zm",
        "lost_passport": "Contact the US Embassy in Lusaka at Eastern End of Kabulonga Road, Ibex Hill, Lusaka. For emergencies: +260 211-357-000.",
    },
    "Namibia": {
        "police_name": "Namibian Police Force (NAMPOL)",
        "police_number": "10111 (Police) or 211111 (Emergency)",
        "emergency_number": "10111",
        "report_url": "https://www.nampol.gov.na/",
        "report_site": "nampol.gov.na",
        "lost_passport": "Contact the US Embassy in Windhoek at 14 Lossen Street, Windhoek. For emergencies: +264 61-295-8500.",
    },
    "Rwanda": {
        "police_name": "Rwanda National Police",
        "police_number": "112 (Emergency) or 113 (Police)",
        "emergency_number": "112",
        "report_url": "https://www.police.gov.rw/",
        "report_site": "police.gov.rw",
        "lost_passport": "Contact the US Embassy in Kigali at 2657 Avenue de la Gendarmerie, Kacyiru, Kigali. For emergencies: +250 252-596-400.",
    },
    "Mozambique": {
        "police_name": "Mozambique Police (PRM)",
        "police_number": "119 (Police) or 112 (Emergency)",
        "emergency_number": "112",
        "report_url": "https://www.mint.gov.mz/",
        "report_site": "mint.gov.mz",
        "lost_passport": "Contact the US Embassy in Maputo at Avenida Kenneth Kaunda 193, Maputo. For emergencies: +258 21-492-797.",
    },
    "Fiji": {
        "police_name": "Fiji Police Force",
        "police_number": "917 (Police) or 911 (Emergency)",
        "emergency_number": "911",
        "report_url": "https://www.police.gov.fj/",
        "report_site": "police.gov.fj",
        "lost_passport": "Contact the US Embassy in Suva at 158 Princes Road, Tamavua, Suva. For emergencies: +679 331-4466.",
    },
}

# Country to health page slug mapping
COUNTRY_HEALTH_SLUGS = {
    "United Kingdom": "united-kingdom", "Japan": "japan", "United Arab Emirates": "united-arab-emirates",
    "Netherlands": "netherlands", "Singapore": "singapore", "Malaysia": "malaysia",
    "South Korea": "south-korea", "Portugal": "portugal", "Greece": "greece",
    "Germany": "germany", "Spain": "spain", "Vietnam": "vietnam", "Mexico": "mexico",
    "Brazil": "brazil", "Peru": "peru", "Poland": "poland", "France": "france",
    "Italy": "italy", "Thailand": "thailand", "Turkey": "turkey", "Czech Republic": "czech-republic",
    "Morocco": "morocco", "Egypt": "egypt", "Argentina": "argentina", "United States": "united-states",
    "Austria": "austria", "Canada": "canada", "Ireland": "ireland", "Denmark": "denmark",
    "Hungary": "hungary", "Croatia": "croatia", "Jordan": "jordan", "Israel": "israel",
    "Iceland": "iceland", "Belgium": "belgium", "Cambodia": "cambodia", "Philippines": "philippines",
    "Cuba": "cuba", "Puerto Rico": "puerto-rico", "Colombia": "colombia", "Scotland": "united-kingdom",
    "Indonesia": "indonesia-bali", "India": "india", "Taiwan": "taiwan", "Nepal": "nepal",
    "China": "china", "Laos": "laos", "Romania": "romania", "Bulgaria": "bulgaria",
    "Serbia": "serbia", "Estonia": "estonia", "Montenegro": "montenegro",
    "South Africa": "south-africa", "Kenya": "kenya", "Tanzania": "tanzania",
    "Ghana": "ghana", "Australia": "australia", "Sri Lanka": "sri-lanka",
    "The Bahamas": "bahamas", "Aruba": "aruba", "Dominican Republic": "dominican-republic",
    "Antigua and Barbuda": "antigua-and-barbuda", "Honduras": "honduras",
    "Panama": "panama", "Costa Rica": "costa-rica", "Jamaica": "jamaica",
    "Hong Kong": "hong-kong", "Switzerland": "switzerland", "Finland": "finland",
    "Sweden": "sweden", "Norway": "norway", "New Zealand": "new-zealand",
    "Turks and Caicos Islands": "turks-and-caicos-islands",
    "Myanmar": "myanmar", "Bangladesh": "bangladesh", "Uzbekistan": "uzbekistan",
    "Kazakhstan": "kazakhstan", "Armenia": "armenia", "Lithuania": "lithuania",
    "Nicaragua": "nicaragua", "Barbados": "barbados", "Saint Lucia": "saint-lucia",
    "Uganda": "uganda", "Zambia": "zambia", "Namibia": "namibia",
    "Rwanda": "rwanda", "Mozambique": "mozambique", "Fiji": "fiji",
    "Russia": "russia", "Guatemala": "guatemala", "Saudi Arabia": "saudi-arabia",
}

# City slugs mapping
CITY_SLUGS = {
    "London": "london",
    "Tokyo": "tokyo",
    "Dubai": "dubai",
    "Amsterdam": "amsterdam",
    "Singapore": "singapore",
    "Hong Kong": "hong-kong",
    "Kuala Lumpur": "kuala-lumpur",
    "Seoul": "seoul",
    "Lisbon": "lisbon",
    "Athens": "athens",
    "Berlin": "berlin",
    "Madrid": "madrid",
    "Hanoi": "hanoi",
    "Mexico City": "mexico-city",
    "Rio de Janeiro": "rio-de-janeiro",
    "Lima": "lima",
    "Krakow": "krakow",
    "Paris": "paris",
    "Rome": "rome",
    "Bangkok": "bangkok",
    "Istanbul": "istanbul",
    "Prague": "prague",
    "Marrakech": "marrakech",
    "Cairo": "cairo",
    "Buenos Aires": "buenos-aires",
    "New York City": "new-york-city",
    "Cancún": "cancun",
    "Vienna": "vienna",
    "Vancouver": "vancouver",
    "Florence": "florence",
    "Dublin": "dublin",
    "Copenhagen": "copenhagen",
    "Budapest": "budapest",
    "Dubrovnik": "dubrovnik",
    "Santorini": "santorini",
    "Phuket": "phuket",
    "Ho Chi Minh City": "ho-chi-minh-city",
    "Ninh Binh": "ninh-binh",
    "Petra": "petra",
    "Jerusalem": "jerusalem",
    "Reykjavik": "reykjavik",
    "Edinburgh": "edinburgh",
    "Bruges": "bruges",
    "Nice": "nice",
    "Split": "split",
    "Phnom Penh": "phnom-penh",
    "Siem Reap": "siem-reap",
    "Manila": "manila",
    "Havana": "havana",
    "San Juan": "san-juan",
    "Medellín": "medellin",
    "Osaka": "osaka",
    "Bali": "bali",
    "Delhi": "delhi",
    "Mumbai": "mumbai",
    "Jaipur": "jaipur",
    "Goa": "goa",
    "Chiang Mai": "chiang-mai",
    "Taipei": "taipei",
    "Kathmandu": "kathmandu",
    "Macau": "macau",
    "Kyoto": "kyoto",
    "Kuching": "kuching",
    "Vientiane": "vientiane",
    "Venice": "venice",
    "Milan": "milan",
    "Brussels": "brussels",
    "Porto": "porto",
    "Seville": "seville",
    "Munich": "munich",
    "Salzburg": "salzburg",
    "Warsaw": "warsaw",
    "Bucharest": "bucharest",
    "Sofia": "sofia",
    "Belgrade": "belgrade",
    "Tallinn": "tallinn",
    "Mykonos": "mykonos",
    "Heraklion": "heraklion",
    "Thessaloniki": "thessaloniki",
    "Rhodes": "rhodes",
    "Corfu": "corfu",
    "Chania": "chania",
    "Paros": "paros",
    "Naxos": "naxos",
    "Kotor": "kotor",
    "Los Angeles": "los-angeles",
    "Miami": "miami",
    "Cape Town": "cape-town",
    "Nairobi": "nairobi",
    "Zanzibar": "zanzibar",
    "Fez": "fez",
    "Accra": "accra",
    "Dar es Salaam": "dar-es-salaam",
    "Johannesburg": "johannesburg",
    "Amman": "amman",
    "Sydney": "sydney",
    "Beijing": "beijing",
    "Shanghai": "shanghai",
    "Colombo": "colombo",
    "Las Vegas": "las-vegas",
    "San Francisco": "san-francisco",
    "Nassau": "nassau",
    "Aruba": "aruba",
    "Puerto Vallarta": "puerto-vallarta",
    "Cabo San Lucas": "cabo-san-lucas",
    "Punta Cana": "punta-cana",
    "Turks and Caicos": "turks-and-caicos",
    "Washington DC": "washington-dc",
    "Antalya": "antalya",
    "Hurghada": "hurghada",
    "Portland": "portland",
    "Abu Dhabi": "abu-dhabi",
    "Denver": "denver",
    "Grand Cayman": "grand-cayman",
    "Toronto": "toronto",
    "Fiji": "fiji",
    "Tenerife": "tenerife",
    "Casablanca": "casablanca",
    "Belfast": "belfast",
    "Doha": "doha",
    "Seychelles": "seychelles",
    "Lagos": "lagos",
    "Quito": "quito",
    "Tel Aviv": "tel-aviv",
    "Bratislava": "bratislava",
    "Beirut": "beirut",
    "Austin": "austin",
    "Tangier": "tangier",
    "San Miguel de Allende": "san-miguel-de-allende",
    "Maldives": "maldives",
    "Orlando": "orlando",
    "Marseille": "marseille",
    "Montreal": "montreal",
    "Bodrum": "bodrum",
    "Ibiza": "ibiza",
    "Guatemala City": "guatemala-city",
    "Stockholm": "stockholm",
    "Palermo": "palermo",
    "Djerba": "djerba",
    "Riga": "riga",
    "Jakarta": "jakarta",
    "Tunis": "tunis",
    "Baku": "baku",
    "Gran Canaria": "gran-canaria",
    "Bora Bora": "bora-bora",
    "Belize City": "belize-city",
    "Honolulu": "honolulu",
    "Puerto Escondido": "puerto-escondido",
    "Malaga": "malaga",
    "Addis Ababa": "addis-ababa",
    "Sarajevo": "sarajevo",
    "Marmaris": "marmaris",
    "Labadee": "labadee",
    "Tirana": "tirana",
    "Durban": "durban",
    "Tbilisi": "tbilisi",
    "Liverpool": "liverpool",
    "Mombasa": "mombasa",
    "Key West": "key-west",
    "Moscow": "moscow",
    "Lanzarote": "lanzarote",
    "Frankfurt": "frankfurt",
    "Valencia": "valencia",
    "Ocho Rios": "ocho-rios",
    "Montevideo": "montevideo",
    "Zurich": "zurich",
    "Negril": "negril",
    "Rhodes": "rhodes",
    "Guayaquil": "guayaquil",
    "Kyiv": "kyiv",
    "Riyadh": "riyadh",
    "Tamarindo": "tamarindo",
    "Corfu": "corfu",
    "Dakar": "dakar",
    "Sardinia": "sardinia",
    "Santa Marta": "santa-marta",
    "Jeddah": "jeddah",
    "Monaco": "monaco",
    "Salvador": "salvador",
    "Cebu": "cebu",
    "Muscat": "muscat",
    "Cali": "cali",
    "Pattaya": "pattaya",
    "Melbourne": "melbourne",
    "Lviv": "lviv",
    "New Orleans": "new-orleans",
    "Curacao": "curacao",
    "Antigua": "antigua",
    "Roatan": "roatan",
    "Barcelona": "barcelona",
    "Naples": "naples",
    "Cartagena": "cartagena",
    "Chicago": "chicago",
    "Boston": "boston",
    "San Diego": "san-diego",
    "Guadalajara": "guadalajara",
    "Tulum": "tulum",
    "Playa del Carmen": "playa-del-carmen",
    "Cozumel": "cozumel",
    "Oaxaca": "oaxaca",
    "Seattle": "seattle",
    "Nashville": "nashville",
    "Panama City": "panama-city",
    "Bogota": "bogota",
    "Mauritius": "mauritius",
    "San Salvador": "san-salvador",
    "Montego Bay": "montego-bay",
    "Agra": "agra",
    "Amalfi Coast": "amalfi-coast",
    "Arusha": "arusha",
    "Bariloche": "bariloche",
    "Bologna": "bologna",
    "Boracay": "boracay",
    "Bordeaux": "bordeaux",
    "Budva": "budva",
    "Cairns": "cairns",
    "Chefchaouen": "chefchaouen",
    "Chiang Rai": "chiang-rai",
    "Cinque Terre": "cinque-terre",
    "Cusco": "cusco",
    "Da Nang": "da-nang",
    "Dalat": "dalat",
    "Phu Quoc": "phu-quoc",
    "Can Tho": "can-tho",
    "El Nido": "el-nido",
    "Essaouira": "essaouira",
    "Gold Coast": "gold-coast",
    "Hoi An": "hoi-an",
    "Hvar": "hvar",
    "Koh Phangan": "koh-phangan",
    "Koh Samui": "koh-samui",
    "Krabi": "krabi",
    "La Paz": "la-paz",
    "Lake Bled": "lake-bled",
    "Lake Como": "lake-como",
    "Gili Islands": "gili-islands",
    "Langkawi": "langkawi",
    "Lombok": "lombok",
    "Luang Prabang": "luang-prabang",
    "Lyon": "lyon",
    "Maui": "maui",
    "Phoenix": "phoenix",
    "Sedona": "sedona",
    "Savannah": "savannah",
    "Charleston": "charleston",
    "San Antonio": "san-antonio",
    "Fort Lauderdale": "fort-lauderdale",
    "Galveston": "galveston",
    "Anaheim": "anaheim",
    "Memphis": "memphis",
    "Gatlinburg": "gatlinburg",
    "Myrtle Beach": "myrtle-beach",
    "Napa Valley": "napa-valley",
    "Branson": "branson",
    "Asheville": "asheville",
    "St. Louis": "st-louis",
    "Mendoza": "mendoza",
    "Nha Trang": "nha-trang",
    "Nusa Penida": "nusa-penida",
    "Pai": "pai",
    "Penang": "penang",
    "Positano": "positano",
    "Queenstown": "queenstown",
    "Rishikesh": "rishikesh",
    "San Jose": "san-jose-costa-rica",
    "Santiago": "santiago",
    "Santiago de Compostela": "santiago-de-compostela",
    "Sapa": "sapa",
    "Siargao": "siargao",
    "Sorrento": "sorrento",
    "Stone Town": "stone-town",
    "Ubud": "ubud",
    "Udaipur": "udaipur",
    "Valparaíso": "valparaiso",
    "Varanasi": "varanasi",
    "Yogyakarta": "yogyakarta",
    # New batch — 50 cities
    "Luxor": "luxor",
    "Sharm El Sheikh": "sharm-el-sheikh",
    "Aswan": "aswan",
    "Alexandria": "alexandria",
    "Kolkata": "kolkata",
    "Chennai": "chennai",
    "Bangalore": "bangalore",
    "Hyderabad": "hyderabad",
    "Cappadocia": "cappadocia",
    "Kusadasi": "kusadasi",
    "Ephesus": "ephesus",
    "Pamukkale": "pamukkale",
    "Fethiye": "fethiye",
    "Alanya": "alanya",
    "Side": "side-turkey",
    "Izmir": "izmir",
    "Konya": "konya",
    "St. Petersburg": "st-petersburg",
    "Yangon": "yangon",
    "Mandalay": "mandalay",
    "Dhaka": "dhaka",
    "Sao Paulo": "sao-paulo",
    "Recife": "recife",
    "Fortaleza": "fortaleza",
    "Xi'an": "xian",
    "Guilin": "guilin",
    "Chengdu": "chengdu",
    "Shenzhen": "shenzhen",
    "Lijiang": "lijiang",
    "Yangshuo": "yangshuo",
    "Chongqing": "chongqing",
    "Zhangjiajie": "zhangjiajie",
    "Pingyao": "pingyao",
    "Harbin": "harbin",
    "Vilnius": "vilnius",
    "Antigua Guatemala": "antigua-guatemala",
    "Granada": "granada-nicaragua",
    "Granada (Spain)": "granada-spain",
    "Toledo": "toledo",
    "Bilbao": "bilbao",
    "San Sebastián": "san-sebastian",
    "Córdoba": "cordoba",
    "Arequipa": "arequipa",
    "Santo Domingo": "santo-domingo",
    "Kingston": "kingston",
    "Bridgetown": "bridgetown",
    "Castries": "castries",
    "Kampala": "kampala",
    "Lusaka": "lusaka",
    "Windhoek": "windhoek",
    "Kigali": "kigali",
    "Maputo": "maputo",
    "Tashkent": "tashkent",
    "Samarkand": "samarkand",
    "Yerevan": "yerevan",
    "Almaty": "almaty",
    "Battambang": "battambang",
    "San Cristobal de las Casas": "san-cristobal-de-las-casas",
    "Ouarzazate": "ouarzazate",
    "Suva": "suva",
    "Pokhara": "pokhara",
    "Kandy": "kandy",
    "Galle": "galle",
    "Agadir": "agadir",
    "Hammamet": "hammamet",
    "Hue": "hue",
    "Johor Bahru": "johor-bahru",
    "Bukhara": "bukhara",
    "Mecca": "mecca",
    # Batch 3 — 50 cities
    "Guangzhou": "guangzhou",
    "Medina": "medina",
    "Ha Long Bay": "ha-long-bay",
    "Auckland": "auckland",
    "Fukuoka": "fukuoka",
    "Batam": "batam",
    "Jeju": "jeju",
    "Palma de Mallorca": "palma-de-mallorca",
    "Busan": "busan",
    "Hangzhou": "hangzhou",
    "Helsinki": "helsinki",
    "Oslo": "oslo",
    "Hamburg": "hamburg",
    "Manchester": "manchester",
    "Sapporo": "sapporo",
    "Perth": "perth",
    "Geneva": "geneva",
    "Verona": "verona",
    "Thessaloniki": "thessaloniki",
    "Acapulco": "acapulco",
    "Pisa": "pisa",
    "Innsbruck": "innsbruck",
    "Lucerne": "lucerne",
    "Paphos": "paphos",
    "Faro": "faro",
    "Gothenburg": "gothenburg",
    "Interlaken": "interlaken",
    "Bermuda": "bermuda",
    "St Maarten": "st-maarten",
    "Hiroshima": "hiroshima",
    "Okinawa": "okinawa",
    "Niagara Falls": "niagara-falls",
    "Quebec City": "quebec-city",
    "Banff": "banff",
    "Jasper": "jasper",
    "Whistler": "whistler",
    "Victoria": "victoria-bc",
    "Halifax": "halifax",
    "Calgary": "calgary",
    "Ottawa": "ottawa",
    "Philadelphia": "philadelphia",
    "Nuremberg": "nuremberg",
    "Ghent": "ghent",
    "Taormina": "taormina",
    "Nara": "nara",
    "Annecy": "annecy",
    "St Tropez": "st-tropez",
    "Yokohama": "yokohama",
    "Dammam": "dammam",
    "Kunming": "kunming",
    "Suzhou": "suzhou",
    "Düsseldorf": "dusseldorf",
    "Birmingham": "birmingham",
    "Atlanta": "atlanta",
    "Mazatlán": "mazatlan",
    "Mérida": "merida",
    "Strasbourg": "strasbourg",
    "Carmel": "carmel",
    "Cannes": "cannes",
    "Avignon": "avignon",
    "Toulouse": "toulouse",
    "Montpellier": "montpellier",
    "Colmar": "colmar",
    "Chamonix": "chamonix",
    "Mont-Saint-Michel": "mont-saint-michel",
    "Biarritz": "biarritz",
}

# City-specific safety tips
SAFETY_TIPS = {
    "Philadelphia": [
        "From PHL airport, confirm the $28.50 Center City flat-rate taxi before boarding, use Uber/Lyft from Zone 2 with fare estimate screenshot, or take SEPTA Airport Line ($6.75, 30 min) — never engage drivers soliciting at baggage claim",
        "Book Independence Hall timed-entry tickets at recreation.gov or nps.gov/inde ($1 reservation fee) — Liberty Bell is always free; reject third-party 'skip-the-line' resellers at $20+",
        "For cheesesteaks, visit John's Roast Pork (Snyder Ave, $12–$14), Dalessandro's (Roxborough), or Reading Terminal Market — avoid South Street tourist-strip cheesesteaks at $20+",
        "Philadelphia Art Museum (the 'Rocky Steps') is free to climb — refuse 'professional photographer' touts at the Rocky statue; museum admission is $30 direct at philamuseum.org",
        "For Airbnb, book only through Airbnb/VRBO platform payment — refuse Zelle/Venmo/wire transfer from 'hosts'; licensed hotels: Ritz-Carlton, Four Seasons, Kimpton Palomar, Loews, Hyatt Centric",
    ],
    "Atlanta": [
        "From ATL airport, take MARTA Red/Gold Line to downtown Five Points ($2.50, 20 min) — scam-proof; licensed taxi with meter $30–$45; Uber/Lyft from designated pickup zones (North/South Terminal Economy Parking)",
        "HANG UP on any caller claiming to be US Customs/CBP from a 404 area code — r/Scams 'Got a Call from Atlanta's US Customs and Border Protection' (comments/1p1lnfu, 2025) documents the 2025 phone scam; CBP never demands payment by phone",
        "Book Georgia Aquarium ($49.95 adult) + World of Coca-Cola ($22) direct via official sites; Atlanta CityPASS at citypass.com ($85-$95) — avoid Google ads and third-party resellers at $75+",
        "MLK Center and Ebenezer Baptist Church are FREE — reserve birthplace home at recreation.gov; skip paid 'MLK walking tours' at $80+",
        "For convention-season Atlanta lodging (Dragon Con, Music Midtown, SEC Championship), book 3+ months ahead via Airbnb/Booking.com; refuse off-platform 'host' requests for Zelle/Venmo payment",
    ],
    "Phoenix": [
        "NEVER hand an unlocked phone to a stranger in Old Town Scottsdale — the 2024-2025 'skin' scam sends $500–$3,000 via Venmo before the phone is returned; r/Scottsdale 'Beware of Scam in old town Scottsdale' (comments/1dt506e) + 'cart driver and skins scammed them' (comments/1qvhes6, 2025) are named anchors. Enable PIN on Venmo/Zelle/Cash App/PayPal.",
        "From PHX Sky Harbor, take free SkyTrain to 44th Street/Washington, then Valley Metro light rail to downtown ($2) — or Uber/Lyft at the designated pickup zone ($18–$35) with fare screenshot; licensed taxi with meter $30–$45; refuse any driver soliciting at baggage claim",
        "Book Grand Canyon day trips direct via Viator, GetYourGuide, or Detours American West ($150–$250) — not hotel concierge packages at $300+; helicopter: Maverick or Papillon direct ($250–$400); Grand Canyon NP entry is $35/vehicle for 7-day pass if self-driving",
        "Refuse ALL 'free gift' timeshare-presentation offers in Scottsdale/Phoenix — the 90-minute pitch runs 2–4 hours with $15k–$50k purchase pressure; Arizona has a 7-day right of rescission (azag.gov) — avoid 'exit' companies charging $5k+",
        "At PHX rental car center, avoid Fox, Payless, Sixt — use Hertz, Enterprise, or Alamo; video walk-around at pickup narrating every scratch and tire; decline 'zero-excess' insurance if your credit card covers rentals (Chase Sapphire, Amex Platinum, most Visa Signature do); skip 'automatic toll plan' at $15/toll — pre-arrange SunPass or pay cash",
    ],
    "Sedona": [
        "Sedona's four 'energy vortex' sites (Airport Mesa, Cathedral Rock, Bell Rock, Boynton Canyon) are all FREE public-land hikes with a Red Rock Pass ($5/day, $15/week, $20/annual) — skip 'certified vortex experience' tours at $150–$400 per person; r/arizona 'are the energy vortexes real or a tourist trap?' (comments/lpdsug) captures the community skepticism",
        "Book Pink Jeep Tours direct at pinkjeeptours.com or the uptown office ($100–$250) — not hotel concierge at $180+ markup; Broken Arrow is the signature route ($130, 2.5h); for mobility concerns, request Scenic Rim or Ancient Ruin (smoother roads); skip third-party 'discount Pink Jeep' resellers (all are markups)",
        "Buy Red Rock Pass ONLY at Sedona Visitor Center (Hwy 89A), Forest Service office, or trailhead self-pay kiosk — refuse any 'parking attendant' in a reflective vest demanding cash at trailheads (no legitimate attendants exist); National Parks Annual Pass ($80) is better if visiting 3+ federal sites",
        "For Native American jewelry, shop only at IACA-certified galleries (iaca.com list) — ask for artist hallmark stamp + certificate of authenticity with tribal affiliation; genuine sterling from Mexico is $20–$80 (legitimate but NOT 'Native American' at $150–$500); compare 2–3 Tlaquepaque galleries before buying over $100",
        "Phoenix-to-Sedona (120 miles): Groome Transportation shuttle direct at groometransportation.com ($78 one-way, 2.5h, 10x daily) — avoid third-party 'Sedona transfer' websites at $250–$400; rental car self-drive via I-17 North is 2h; Sedona Airport (SDL) is general aviation only — no commercial flights",
    ],
    "Savannah": [
        "From SAV airport to downtown Savannah (12 miles), use Uber/Lyft at the designated pickup zone ($20–$32 with fare screenshot) or licensed taxi with meter ($25–$35) — r/savannah 'Airport taxi scam' (comments/1grpmor) documents the 'flat $45–$60' and 'meter is broken' patterns; for Hilton Head, book Low Country Adventures shuttle direct ($37) not touts at $150+",
        "REFUSE all unsolicited 'gifts' on River Street, Factors Walk, and City Market — the 2025 'monk' bracelet scam per r/savannah 'What's up with the monk on River Street?' (comments/1kmjc3m, 2025) places items on your wrist then demands $20–$100; keep hands in pockets and walk past without eye contact",
        "Book ghost tours direct with Ghost City Tours ($25), Old Savannah Tours ($29), or Savannah Haunted History ($35) — reject curb touts with 'tonight only $45' inflated pricing; Colonial Park Cemetery is free to walk in daylight, no 'VIP access' exists; for mobility concerns, Old Town Trolley ($45 hop-on all day) includes ghost narration",
        "Carriage tours run $30–$50 direct via Historic Savannah Carriage Tours or Plantation Carriage — ride early morning or after 6pm to avoid summer heat; city ordinance suspends tours above 98°F; refuse operators willing to run in extreme heat — that's an illegal operator",
        "Book Savannah accommodation ONLY via Airbnb / VRBO / Booking.com platform payment — NEVER Zelle, Venmo, or wire transfer; verify STR certificate in savannahga.gov STVR registry; r/savannah 'Will Savannah ever ban STRs like Tybee?' (comments/1l51so0, 2025) tracks regulation changes; legitimate hotels: Mansion on Forsyth, The DeSoto, Perry Lane, Hyatt Regency, Marriott Riverfront",
    ],
    "Charleston": [
        "From CHS airport to downtown (12 miles), use Uber/Lyft at Garage Level 3 pickup ($22–$35) or licensed taxi at the taxi stand ($30–$42) — r/Charleston 'CHS Airport Uber' (comments/1nucopj, 2025) + 'Rideshare options/availability?' (comments/1q5ldef, 2025) are 2025 named anchors; refuse drivers soliciting at baggage claim offering 'flat $55'",
        "Keep hands in pockets near City Market and Meeting Street — refuse all unsolicited 'palmetto rose' gifts per r/Charleston 'Oldest scam in the book' (comments/1kq8w1k, 2025) NAMED 2025 anchor; if one is placed in your hand, return it immediately without paying; buy genuine palmetto roses at Gullah artisan stalls with posted $3–$10 prices",
        "For verified local shrimp (not imported farm-raised at 91% fraud rate per r/Charleston '90% of Charleston restaurants were found to be deceiving' comments/1l80u7c, 2025), use certifiedsc.com — Magnolia's, Husk, FIG, Hominy Grill are verified; always check bill for auto-gratuity, service charge, and tip-on-tax BEFORE signing; fill in TOTAL line yourself — never leave blank",
        "Book carriage tours direct: Palmetto Carriage Works ($34), Old South Carriage Company ($38), or Classic Carriage Works ($33) — Charleston suspends carriage tours above 95°F per city ordinance; walking tours: Charleston Footprints ($25) or Bulldog Tours ($30); skip curb touts at $45+",
        "REFUSE ALL 'free gift' timeshare-presentation offers on Meeting Street — r/Charleston 'Great Vacations,LLC Travel Club Scam 180 meeting St' (comments/1jpvapu, 2025) is the NAMED 2025 anchor; SC has a 5-day right of rescission (scconsumer.gov) — avoid 'exit' companies charging $5k+",
    ],
    "Pingyao": [
        "Buy Pingyao Ancient City Tongpiao (通票, ¥125) at the South Gate ticket office or via Trip.com / Ctrip — covers 3 days + 20+ monuments; skip 'combo' or 'VIP' packages at ¥300–¥500 per person",
        "Take Taiyuan-Pingyao high-speed rail (¥23, 1.5h) from Taiyuan South — refuse taxi touts quoting ¥300+ 'private car' per r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025)",
        "SKIP 'silk workshop' and 'ancient currency museum' venues on South Street — r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024) documents the commission-shopping ecosystem; for silk, visit Suzhou Silk Museum or Taobao",
        "Book courtyard guesthouses only through Booking.com / Agoda / Trip.com (¥150–¥400/night) — refuse off-platform 'WeChat direct booking' offers from strangers at stations",
        "For genuine Shanxi noodles, walk one block off South Street to Deju Yuan Noodle (¥18–¥30), Yun Jin Cheng (¥15–¥25), or Xiangtie Tang (¥25–¥40)",
    ],
    "Harbin": [
        "Book Harbin Ice and Snow World direct via Ctrip / Trip.com (¥330 day / ¥460 evening) — r/harbin_china 'Looking for Harbin travel experience' (comments/1i1e0t7, 2025) is the 2025 named anchor; evening with lit ice sculptures is worth the premium",
        "SKIP Snow Village (Xuexiang) — r/harbin_china (comments/1i1e0t7, 2025) confirms 'Snow Village is a scam'; alternatives: Yabuli Ski Resort (¥250–¥400), Volga Manor (¥115), Siberian Tiger Park (¥95)",
        "From Harbin Taiping Airport (HRB), take Airport Shuttle Bus Line 1 to Zhongyang Street (¥20, 45 min, heated) — refuse 'winter surcharge' taxi claims (no official surcharge exists)",
        "For Russian souvenirs, buy matryoshka at residential department stores (¥30–¥100) and Russian chocolate at Chao Shi Fa or Walmart (¥15–¥30) — skip Zhongyang Street tourist markups 3–5x",
        "For authentic Russian dinner, book Lucia Russian Restaurant, Harbin Portman, or Russian Russia Restaurant via Dianping (¥100–¥200 per person) — avoid Zhongyang Street 'Stalin's favorite' venues at ¥300–¥700",
    ],
    "Chongqing": [
        "For Yangtze River cruise bookings, use ONLY verified cruise lines: Victoria Cruises, Century Cruises, Sanctuary Yangzi, or President Cruises — r/China 'Tours with forced shopping stops' (comments/1sbqo0g, 2025) confirms 2025 third-party 'discount' resellers are unreliable; reject any 4-day Yangtze cruise under ¥2,500 per person",
        "From Chongqing Jiangbei Airport (CKG), take Metro Line 10 (¥6–¥8, 45 min) — avoid taxi touts; r/travelchina 'Ask me anything about chongqing and chengdu' (comments/1smy9iz, 2025) is the 2025 Chongqing community anchor",
        "For authentic Chongqing hotpot, walk one block off Jiefangbei/Hongyadong to Liuyishou, Qiqi, Dezhuang, or Xiao Jiang (¥90–¥160 per person) — skip tourist-strip laminated-English-menu venues at ¥200–¥400",
        "For Dazu Rock Carvings, take Chongqing-Dazu coach from Caiyuanba (¥65, 2h) + entry ¥115–¥140 + return ¥65 = ¥270 self-guided vs hotel-package ¥350–¥800 with shopping stops",
        "At Hongyadong viewpoint, take your own photos from Qiansimen Bridge 7:30–8:30 PM — refuse 'professional photographer' touts; r/China 'Common scams' (comments/2aqq6l) documents the photo-tout pattern",
    ],
    "Zhangjiajie": [
        "Buy Zhangjiajie National Forest Park 4-day ticket (¥228) at the park entrance or via Trip.com/Ctrip — refuse all third-party WeChat resellers; r/Scams 'CHINA Group Tour at Zhuhai' (comments/1gv3wru, 2024) documents the Beijing+Zhangjiajie tour-scam bundle",
        "Skip hotel-concierge 'Zhangjiajie 3-day all-inclusive' tours at ¥1,500–¥3,000 per person — all include Tujia village shopping stops per r/travelchina 'Are tours in China still sketchy' (comments/1k85j1d, 2025); self-guide at ~¥1,100 for 3 days",
        "From Zhangjiajie Hehua Airport (DYG), use the direct airport-to-Wulingyuan shuttle (¥30, 50 min, hourly) — r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025) confirms DiDi works in Zhangjiajie",
        "At Tianmen Mountain, buy standard ¥258 ticket (includes cable car + all shuttles + Heaven's Gate) — refuse 'VIP tour' at ¥500+; escalator ¥32 one-way if mobility concern on the 999-step staircase",
        "For authentic Tujia culture, visit Furong Ancient Town (¥75 standalone) rather than hotel-tour 'Tujia village visits' — commission-driven shopping per r/China (comments/1hfcgv5, 2024)",
    ],
    "Lijiang": [
        "Pay the Old Town Maintenance Fee (¥80) at an official checkpoint only — refuse touts selling 'skip-the-line' at ¥150+; r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025) gives the Yunnan context",
        "For Yulong Snow Mountain, self-book via official WeChat or Trip.com: entry ¥100 + big cable car ¥180 + eco bus ¥50 + shared taxi ¥80 = ¥440 per person — skip hotel-concierge packages at ¥500–¥1,200 with shopping stops",
        "For authentic Naxi culture, visit Dongba Cultural Museum (¥30 entry) and Naxi Ancient Music concert by Master Xuan Ke's orchestra (¥150–¥280) — skip hotel 'Naxi cultural experience' packages at ¥600+",
        "Never follow Old Town bar-street touts promising 'free entry, free first drink' — r/chinalife 'Random meeting with Chinese lady' (comments/1gbkj16) documents Lijiang after-hours bar-trap approaches",
        "Use DiDi or LJG Airport Shuttle Bus (¥25, 45 min) — r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025) confirms DiDi reliability in Yunnan",
    ],
    "Yangshuo": [
        "Book Yulong River bamboo-raft via your guesthouse with posted prices (¥150–¥200 per 2-person, 90-min route) — refuse West Street touts offering 'discount ¥80 raft'; r/chinatravel 'Traveling to China' (comments/1fjwbtc, 2024) warns about Yangshuo rural-scam density",
        "Avoid West Street bars after 10 PM — hostess-bar / drink-spiking / ¥300+ drink scams per r/travelchina 'Did I nearly get scammed?' (comments/1n4pjbk, 2025) with ¥6 Qingdao beer as reference; eat earlier at Dianping-verified venues",
        "Book Impression Liu Sanjie show at liusanjie.net or Trip.com (official ¥220–¥680) — avoid hotel-concierge packages at ¥500–¥1,200",
        "For beer fish, walk one block off West Street to Fang Weng, Cloud 9, or Lucy's Kitchen (¥80–¥220 per 2-person) — avoid West Street tourist-menu at ¥250–¥450",
        "Rent bikes at guesthouse-affiliated shops (¥30–¥50 regular, ¥80–¥120 e-bike, ¥100–¥200 deposit) — video walk-around at pickup to avoid damage-dispute scams",
    ],
    "Guangzhou": [
        "Guangzhou has China's most-complained-about taxi-scam density per r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025) — use Metro Line 3 from CAN airport (¥6–¥8, 60 min) or DiDi at the official rideshare zone",
        "At Canton Fair / business dinners, NEVER let a contact or stranger choose the venue — insist on hotel restaurant or Dianping-verified 4.5+ venue; r/travelchina 'Did I nearly get scammed?' (comments/1n4pjbk, 2025) documents ¥300+ beer scams",
        "Walk past any stranger at Huacheng Plaza, Shamian Island, or Canton Tower inviting you to tea or art — r/guangzhou 'What are some common scams in Guangzhou' (comments/8bb5gs) places tea-house scam alongside taxi scams as Guangzhou's top two",
        "For shopping, treat Beijing Road and Shangxiajiu as window-shopping only; for genuine brands visit IFC Mall, Grandview Mall, or TaiKoo Hui",
        "Examine ¥100 notes for watermark + color-shifting ink + raised-texture portrait; NEVER accept 'replacement' for a bill you handed over — counterfeit-bill substitution is Guangzhou's signature scam per r/guangzhou (comments/8bb5gs)",
    ],
    "Kunming": [
        "SKIP all-inclusive Yunnan tours at ¥600–¥1,500 per person — guaranteed forced-shopping per r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025); expect ¥3,500–¥6,000 for genuine 5–7 day tour via Ctrip/Viator",
        "Self-guide Yunnan via train/bus: Kunming-Dali train ¥140 (4h), Dali-Lijiang bus ¥50 (2h), Lijiang-Shangri-La bus ¥80 (4h) — total ~¥270 transport; r/chinatravel (comments/1o2bp2j, 2025) confirms self-guided with DiDi works",
        "From Kunming Changshui Airport (KMG), take Metro Line 6 (¥6–¥9, 45 min) — avoid taxi touts",
        "For Pu'er tea, buy at Kunming Flower Market with posted prices (¥80–¥3,000 per cake); SKIP 'Pu'er plantation' tour stops — r/travelchina 'I never knew I would get scammed in China' (comments/1cxb3pv, 2024) documents the shopping-tour ecosystem",
        "NEVER visit 'Yunnan TCM clinic' consultations offered by tour guides — medical fraud diagnosing invented conditions requiring ¥1,000+ herb purchases per r/China (comments/1hfcgv5, 2024)",
    ],
    "Hangzhou": [
        "Walk past any English-speaking stranger at West Lake, Broken Bridge, Su Causeway, or Leifeng Pagoda offering tea — the West Lake teahouse scam is THE canonical China tea-scam anchor per r/travelchina 'A local guide's advice on avoiding the 3 biggest tourist' (comments/1qgbdzg, 2025)",
        "For genuine Longjing tea, visit Meijiawu Tea Village's Longjing Tea Research Institute (posted prices ¥200–¥600 per 250g for certified Xihu Longjing) — avoid 'tea master's home' invitations; r/tea 'Understanding the Real Cost of Longjing Tea' (comments/1juy7mf, 2025) documents widespread counterfeit pricing",
        "From Hangzhou Xiaoshan Airport (HGH), take Metro Line 19 + Line 1 (¥8–¥12, 60 min) or Airport Bus (¥20, 60 min) — avoid taxi touts per r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025)",
        "On West Lake, buy boat tickets at official dockside booths (electric sightseeing ¥70, private rowing ¥150/hr, dragon boat to Santan Yinyue ¥55) — refuse touts selling 'private boat' or 'professional photographer' services",
        "Verify merchant name on Alipay/WeChat Pay confirmation screen BEFORE paying — r/chinalife 'I've learned about these two scams in China in 2024' (comments/1ds004e, 2024) documents QR-code payment-diversion where scammer stickers cover legitimate merchant codes",
    ],
    "Suzhou": [
        "Book Classical Gardens tickets via official WeChat mini-programs (拙政园 Humble Administrator, 留园 Lingering Garden) or Trip.com/Ctrip — r/travelchina 'Planning a trip to Suzhou' (comments/1kyyehv, 2025) recommends official booking; avoid 'skip-the-line' at ¥200+ per garden (official fees ¥40–¥80)",
        "Suzhou Museum requires free advance WeChat booking 1–7 days ahead — skip tout offers for 'museum tickets' near Humble Administrator's Garden",
        "SKIP hotel-concierge 'silk factory tours' entirely — r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024) documents the high-pressure sales at ¥3,000–¥15,000 silk quilts (Taobao price ¥500–¥900 for genuine product)",
        "For Shanghai-to-Suzhou day trip, self-guide: G-series high-speed rail Shanghai Hongqiao to Suzhou Station (¥40, 25 min) + Suzhou Metro Line 2 (¥3–¥6) — total ~¥250–¥350 per person vs hotel-package ¥600+",
        "Walk past any English-speaking stranger on Pingjiang Road offering 'traditional Wu culture tea ceremony' — the Suzhou variant of the tea-scam ring; for genuine Biluochun, visit Dongshan Biluochun Tea Village (bus ¥10, 90 min)",
    ],
    "Macau": [
        "At Outer Harbour Ferry Terminal, Taipa Ferry Terminal, and MFM airport, use free casino shuttle buses (Venetian, Galaxy, MGM, Wynn, City of Dreams all run free shuttles) or the Macau LRT — r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025) confirms southern-China taxi-scam density",
        "Play only on licensed main casino floors (Venetian, Galaxy, Wynn, MGM, City of Dreams, Parisian) — decline ALL 'private room' or 'VIP' introductions from hotel staff; NEVER accept credit markers",
        "Eat Macanese cuisine at Taipa Village and Coloane Village (Lord Stow's egg tarts MOP$10, Tai Lei Loi Kei pork-chop bun MOP$45, Fernando's MOP$150–$300) — skip Senado Square tourist-strip versions at 2–3x prices",
        "Use licensed banks (Bank of China Macau, HSBC, ICBC) for currency exchange — avoid unlicensed Senado-area booths; r/China 'Common scams' (comments/2aqq6l) documents counterfeit-bill swaps at unlicensed exchangers",
        "For accommodation, verify MGTO licence number on listing (macaotourism.gov.mo) — major licensed hotels (Venetian, Galaxy, Wynn, MGM, City of Dreams, Grand Lisboa Palace, Banyan Tree, St. Regis) via Booking/Agoda/Trip.com are all legitimate",
    ],
    "Guilin": [
        "Book the Li River cruise (¥215 tourist class, ¥310 deluxe) via Trip.com / Viator / Ctrip — avoid hotel-lobby 'Li River package' at ¥500+ which are commission markups; r/China 'Common scams you should know' (comments/2aqq6l) documents the overpriced-cruise pattern",
        "At Yangshuo, book bamboo-raft via guesthouse with posted prices (¥150–¥200 per 2-person for 90-min route) — refuse West Street touts and 'cormorant fishing shows' per r/chinatravel 'Traveling to China' (comments/1fjwbtc, 2024)",
        "From Guilin Liangjiang Airport (KWL), take the Airport Shuttle Bus (¥25, 45 min) or DiDi — r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025) warns about airport-terminal touts across China",
        "For Longji Rice Terraces, book a 1-night guesthouse stay (¥300–¥600/night) via Ctrip/Trip.com + Longji entry (¥80) + bus from Qintan (¥25, 2.5h) — total ~¥400 vs hotel-concierge day trips at ¥400–¥800",
        "NEVER book Guilin day trips via hotel concierge — r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024) documents the jade/silk/rice-wine shopping-stop ecosystem; use Trip.com, Viator, GetYourGuide with 'ZERO shopping stops' in writing",
    ],
    "Shenzhen": [
        "At Luohu border crossing, take Shenzhen Metro Line 1 directly from the Luohu Station (¥3 to Futian East, ¥8 to Shekou) — faster than taxi and scam-proof per r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025)",
        "At Shenzhen Bao'an Airport (SZX), take Metro Line 11 to Futian (¥7–¥12, 45 min) — avoid terminal-door taxi touts; licensed taxi rank with 'da biao' (打表) quotes ¥150–¥200 on meter",
        "At Huaqiangbei electronics market, treat as window-shopping only — r/chinatravel 'Which tourist attractions in China do you think are' (comments/1mia1ne, 2025) includes it on 2025 tourist-trap lists; for genuine electronics, Apple Store MixC Mall, Xiaomi flagship Coco Park are authorised retailers",
        "Use licensed Bank of China, HSBC, or Standard Chartered for currency exchange; AVOID Luohu Commercial City unlicensed booths (3–8% markup plus counterfeit-bill risk per r/China 'Common scams' comments/2aqq6l)",
        "SKIP 'TCM clinic' consultations offered by tour guides or concierges — r/travelchina 'I never knew I would get scammed in China' (comments/1cxb3pv, 2024) documents the invented-diagnosis / herb-purchase scam across China including Shenzhen",
    ],
    "Xi'an": [
        "Book Terracotta Warriors tickets (¥120) via the official WeChat mini-program 'Qin Shi Huang Di Ling Bowu Yuan' or Trip.com — r/travelchina 'Don't be scammed in Xi'an in visiting the fake terracotta army' (comments/5nbrg1) warns about fake Terracotta venues on the route",
        "Take Tourist Bus Line 5 (游5) from Xi'an Railway Station East Plaza to Lintong (¥8, 1h) — the scam-free independent option; avoid hotel-lobby 'Terracotta tours' under ¥250 which always include jade/TCM/silk shopping stops",
        "Eat one street off Beiyuanmen in the Muslim Quarter — r/travelchina 'Xi'an Survival Guide' (comments/1r7si9e, 2025) names Lao Sun Jia, Jia San, and Yongxing Fang food court as posted-price alternatives; NEVER buy 'Xinjiang cake' from a pushcart vendor",
        "From XIY airport, take Metro Line 14 (¥17, 70 min) or DiDi at the official rideshare zone — r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025) warns about terminal-approach taxi touts",
        "Walk past ANY stranger near Bell Tower, Drum Tower, or Muslim Quarter who invites you to tea or cultural experience — the same Dong Bei tea-scam ring operates in Xi'an per r/China 'Travelling to China' (comments/16qhsl2)",
    ],
    "Chengdu": [
        "Book Panda Base entry (¥55) via WeChat '成都大熊猫繁育研究基地' or Trip.com; arrive before 8:30 AM — r/Chengdu 'Panda Base visit' (comments/1md57l8, 2025) confirms early arrival avoids tour-group crowds",
        "From Tianfu (TFU), take Metro Line 18 (¥9, 47 min) or DiDi at the official rideshare zone — r/Chengdu 'Where to pick up DiDi at Tianfu' (comments/1deo34t, 2024) warns 'Don't go with the guys waving at you at arrivals'",
        "For Tibet tours from Chengdu, book only Tibet Travel Permit-licensed operators (Tibet Vista, Explore Tibet) — r/singapore 'Singaporean singer recounts ordeal with China tour guide' (comments/1p8r1zn, 2025) documents a 2025 named fraud case; expect ¥6,000–¥12,000 per person, reject anything under ¥3,000",
        "For hotpot, walk one street off Kuanzhai Alley and Jinli to reach honest venues like Shu Jiu Xiang, Huang Cheng Lao Ma, Da Long Yi (¥90–¥180 per person) — r/travelchina 'Chengdu 101' (comments/1rmboro, 2025) is the 2025 local guide",
        "For genuine Sichuan tea, visit People's Park Heming Tea Garden (¥15–¥30 per pot, bottomless refills) or Wenshu Monastery tea garden — never follow strangers to side-street 'tea ceremonies' per r/chinatravel (comments/1nqcbht, 2025)",
    ],
    "Beijing": [
        "At PEK and Daxing (PKX) airports, walk past anyone offering 'taxi' inside the terminal — use the Airport Express train (¥25 from PEK, ¥35 from PKX) or the official outdoor taxi queue with 'da biao' (打表) before boarding; r/travelchina 'Beijing International Airport taxi scammers' (comments/1o7pp36, 2025) is the 2025 anchor",
        "Walk past any stranger near Wangfujing, Tiananmen, or Qianmen who speaks fluent English and invites you to tea, art exhibitions, or 'cultural experiences' — r/travelchina 'Beijing Art Teacher Scam' (comments/1fa4xwf, 2024) and r/shanghai 'Teahouse scam' (comments/17cyvmv, 2023) both document the same ring running Wangfujing → ¥3,000–¥8,000 bills",
        "Book Great Wall via the S2 train from Huangtudian to Badaling (¥6, 1h15m) or licensed operators (Viator, GetYourGuide, Beijing Hikers) — avoid hotel-lobby 'all-inclusive' tours at ¥150–¥250 per r/travelchina 'Are tours in China still sketchy' (comments/1k85j1d, 2025)",
        "For Peking duck, book Da Dong (dadongdadong.com), Siji Minfu, or Quanjude direct — never follow a driver's or tout's 'famous restaurant' recommendation; r/China 'Travel scams in Beijing' (comments/3pbvi9) warns all near-Qianmen gold-lettered 'Peking duck' venues pay driver commissions",
        "Save English-line 12315 (consumer complaints) and 110 (police) — r/travelchina 'Falling for the oldest scam in Beijing' (comments/1pkhqpw, 2025) confirms 12315 handles tourist scams in English and the line is responsive",
    ],
    "Shanghai": [
        "At Pudong (PVG), take Metro Line 2 to central Shanghai (¥7, 90 min) — r/shanghai 'Taxi fare extra cost scam' (comments/1otjyot, 2025) documents 2025 overcharge scams even at the official PVG taxi queue; install DiDi before arrival for app-regulated fares",
        "Walk past ANY stranger near Nanjing Road, the Bund, or People's Square inviting you to tea, art shows, or 'cultural experiences' — r/shanghai 'My experience of the Nanjing road scams' (comments/1kmmutc, 2025) is the 28-year-resident 2025 anchor; specific flagged venues include 510 Tianjin Road (SMOOTH dining bar)",
        "For Bund-view drinks, book published venues only: M on the Bund, Bar Rouge, Waldorf Long Bar, Peace Hotel Jazz Bar — never accept a 'local bar' invitation from a Bund stranger; r/shanghai 'Scam attempt on the Bund' (comments/1qp6db5, 2025) documents 2025 approaches",
        "At Yu Garden, visit genuine Huxinting Teahouse (the 1855 pavilion in the pond, ¥150–¥300) — ignore anyone asking you to 'practice English' or 'take a photo' at the bazaar approach",
        "If defrauded, pay with credit card (chargeback leverage), screenshot bill, and call 12315 (English-line consumer protection) — r/shanghai 'Tea house scam part 3: GOT THE MONEY BACK!' (comments/yojc11) documents the 2022 recovery process still valid in 2025",
    ],
    "London": [
        "Keep your phone in your pocket until you're inside a building — never use it openly on the street near tube exits",
        "Book taxis only through apps (Uber, Bolt, black cab hail) — never accept rides from touts at stations",
        "At restaurants near Leicester Square and Covent Garden, always ask if the service charge is included and specify tap water",
        "If someone with a clipboard approaches you on Oxford Street, keep moving — don't stop to read it",
    ],
    "Tokyo": [
        "Never enter a bar with a recruiter standing outside — the inside is almost certainly a bottakuri (rip-off) bar",
        "Virtually no one with good intentions will approach you and try to take you somewhere — keep your radar high in entertainment districts",
        "Book taxis through the Go app for pre-set fares; trains are almost always faster and cheaper",
        "Near Sensoji and Shibuya, don't accept trinkets or items placed in your hands by strangers in robes",
    ],
    "Dubai": [
        "Choose your own venue for any date arranged through apps — never let your match pick the bar",
        "Only take taxis from the official rank inside the terminal or use the Careem/Uber app",
        "In the Gold Souk, inspect the exact piece you paid for before leaving — ask for a receipt and hallmark certificate",
        "Any desert safari under AED 150 is almost certainly a low-quality middleman product — book through your hotel",
    ],
    "Amsterdam": [
        "Use only official metered taxis (TCA) or Uber/Bolt — never accept rides from people who approach you at Centraal",
        "Buy cannabis only from licensed coffeeshops — street dealers sell unknown substances and are illegal",
        "Be extra careful at ATMs near tourist areas, especially Leidseplein and the Red Light District",
        "Bicycle theft is endemic — rent from an established shop and use the provided lock religiously",
    ],
    "Singapore": [
        "Singapore is one of the safer cities in Asia but stay alert at Orchard Road and MRT station exits with phones out",
        "Ignore anyone who approaches you in the tourist districts with unsolicited 'lucky draw' or 'free gift' offers",
        "Book taxis through GrabTaxi or ComfortDelGro app — never accept touts at the airport",
        "Buy gem or jewelry items only from certified jewelers — fake gem quality claims are a known issue at Sim Lim Square",
    ],
    "Hong Kong": [
        "Book electronics only from certified retailers like Broadway or 3C — Sim-style shops in tourist areas use bait-and-switch tactics",
        "Only use registered taxis (red for urban, green for NT, blue for Lantau) — note the license plate number",
        "Avoid any tour or activity where you haven't independently researched the operator on TripAdvisor",
        "Keep phones pocketed near Nathan Road — pickpocket teams work the busy pavement",
    ],
    "Kuala Lumpur": [
        "Book Grab (local Uber) for all airport trips — avoid taxi touts and always negotiate meter-on before riding official taxis",
        "In Chinatown and Petaling Street, be suspicious of overly friendly strangers who steer you toward specific shops",
        "Gemstones and 'investment' items sold by strangers on the street are almost always worthless",
        "Keep bags in front of your body on the LRT/Monorail — particularly between KL Sentral and Bukit Bintang",
    ],
    "Seoul": [
        "In Itaewon and Hongdae nightlife areas, check that any bar you enter has visible prices before ordering",
        "Book taxis through KakaoTaxi app for metered, accountable rides — avoid street hails at night in entertainment districts",
        "Ignore anyone who says you've won a prize, been 'selected,' or offers unsolicited help near Gyeongbokgung",
        "At hanbok rental shops, confirm what's included before paying — surprise photo service charges are common",
    ],
    "Lisbon": [
        "Keep phones in pockets on Tram 28 — it's the single highest-pickpocket route in Lisbon due to tourist concentration",
        "Book taxis through the Uber or Bolt app or use official metered yellow-and-green taxis — avoid unlicensed operators",
        "At Alfama restaurants, check prices on the menu before sitting — cover charges and couvert are legally required to be shown",
        "In Baixa and Chiado, be wary of anyone who offers to take your photo — they may run off with your phone",
    ],
    "Athens": [
        "From Athens Airport (ATH), the legal taxi flat rate to the city centre is €40 daytime and €54 overnight — posted at the queue; anything else is a scam",
        "Book Acropolis tickets only at hhticket.gr, GetYourGuide, Viator, or Tiqets — sites like acropolisticket.com are documented fakes that send invalid QR codes",
        "Politely decline any drink invitation from a 'friendly local' in Plaka or Monastiraki — a real Athenian does not recruit tourists for unfamiliar bars",
        "If someone with a bracelet or flower approaches at Syntagma or Monastiraki, cross your arms and step back — the item is a distraction for a team pickpocket",
        "Save Tourist Police 171 (English-speaking, 24/7) — they mediate bar bills, rental disputes, and taxi overcharges effectively",
    ],
    "Berlin": [
        "Validate your U-Bahn/S-Bahn ticket every time — plain-clothes fare inspectors work tourist routes and fines are €60+",
        "Ignore aggressive souvenir hawkers at the Brandenburg Gate and Checkpoint Charlie who wave hats/items at you",
        "At Alexanderplatz, watch for the three-card monte (Hütchenspiel) — all bystanders winning are accomplices",
        "Book airport taxis through the official rank only — unofficial touts work outside both TXL and BER arrivals",
    ],
    "Madrid": [
        "From Madrid Barajas Airport (MAD), the legal taxi flat rate to anywhere inside the M-30 ring road is €33 — posted on signs at every taxi queue; anything above is overcharging",
        "Metro Line 8 from Barajas to Nuevos Ministerios is €5 (includes €3 airport supplement) — the scam-free alternative to taxis",
        "If something wet hits you at Puerta del Sol or Plaza Mayor, walk immediately to an indoor space before cleaning — the 'bird poop' distraction is a team pickpocket",
        "Book Prado Museum tickets only at museodelprado.es and Royal Palace only at patrimonionacional.es — 'skip-the-line' third-party sites routinely send invalid QR codes",
        "Save Policía Nacional Comisaría de Centro (Calle Leganitos 19) for tourist crime reports within 24 hours for insurance documentation",
    ],
    "Santiago de Compostela": [
        "Never loan money to a fellow pilgrim regardless of how many days you've walked together — the 'peregrino' long-con is documented on r/CaminoDeSantiago",
        "The last 100 km of the Camino Francés must be walked continuously for the Compostela certificate — taxis and buses invalidate your credential",
        "For luggage transfer, use JacoTrans (jacotrans.com) or Correos Paq Mochila (elcaminoconcorreos.com) at €5–€8 per bag per day with online booking",
        "The Pilgrim Mass at Santiago Cathedral is free and open to all — ignore anyone selling 'reserved seats' or 'Botafumeiro access' outside",
        "The Compostela certificate is free from the Oficina del Peregrino (Rúa Carretas, 33, +34 881 252 139) — no other fees apply for authentication",
    ],
    "Hanoi": [
        "From Noi Bai Airport (HAN), book Grab/Be yourself on airport Wi-Fi AFTER luggage pickup — r/VietNam 'Scammed by a local driver at Hanoi's Noi Bai International' (comments/1s1bw6x, 2025) warns: never accept drivers who approach inside arrivals",
        "Use ONLY Mai Linh (white, green stripe), Vina Sun, or Xanh SM (VinFast electric) taxis; insist on the meter — r/VietNam 'HANOI TAXI SCAM' (comments/1je60u6, 2025) warns 95% of non-branded taxis are scams",
        "Never let anyone touch your shoes on Hoan Kiem Lake perimeter — r/VietNam 'The shoe shining scam' (comments/1axr63k) documents €8–€20 aggressive upcharge for 30-second work",
        "Refuse 'friendly local' motorbike city tours — r/Vietnamese 'Beware of Scammers in Hanoi' (comments/1pcanss, 2025) documents 400,000 VND starting rate escalating to 1.5M–2.5M VND",
        "For solo male travellers using dating apps, YOU pick the venue — r/southeastasia 'Disrupting The Tinder Scam Operation in Old Town Hanoi' (comments/1q4eea7, 2025) documents 15M–50M VND hostess-bar extortion",
    ],
    "Ha Long Bay": [
        "Book ONLY via Bhaya, Paradise, Heritage, Orchid, Indochina Sails, or Emperor Cruises — verify URL exactly (bhayacruises.com, paradisevietnam.com); r/VietNam 'I want to make sure I'm not getting scammed - Ha Long Bay' (comments/1g0jp8s, 2025) warns: pay by credit card only, never wire transfer",
        "Expect $150–$250 per person for 2-day/1-night cruise — anything under $80 is scam-tier per r/VietNam 'Ha long bay cruise - friend telling me I overpaid' (comments/1gumsuu, 2025)",
        "For Hanoi–Ha Long transfers, use The Sinh Tourist (thesinhtourist.vn — verify URL exactly) or Klook/12Go; avoid Old Quarter 'tourist office' copycats per r/VietNam '(Scam) The Sinh Tourist - Ha Noi' (comments/1af6jrg)",
        "On Booking.com/Agoda cruise bookings, IGNORE any 'payment verification' WhatsApp messages — r/VietNam 'Hotel payment - Is this legitimate?' (comments/1jookvm, 2025) documents the 2025 off-platform phishing pattern",
        "Request Lan Ha Bay route (Cat Ba) instead of Ha Long main — fewer ships, more authentic kayaking per r/Vietnam_Tourism 'Is ha long bay worth it?' (comments/1mtdro3, 2025)",
    ],
    "Mexico City": [
        "Only use official CDMX airport taxis (pre-pay at authorized booths inside the terminal) or book Uber before landing",
        "At Chapultepec and tourist markets, keep phones in front pockets or bags — pickpockets are active in crowds",
        "Express kidnapping risk: take Uber over street taxis, especially at night and near nightlife areas",
        "Keep valuables minimal when visiting markets and historic center sites — travel with replaceable items only",
    ],
    "Rio de Janeiro": [
        "Leave all valuables — jewelry, expensive watches, and non-essential electronics — at your hotel safe",
        "Use 99Taxi or Uber exclusively; never hail street taxis or accept offers from drivers at the airport",
        "At beaches, only bring exactly what you're willing to lose — keep phones and wallets hidden under towels or at the hotel",
        "Avoid ATM use at night and in deserted areas — use hotel ATMs or those inside shopping malls during the day",
    ],
    "Lima": [
        "Use InDriver or Uber for all transportation — avoid street taxis entirely, which have no accountability",
        "In Miraflores and Barranco (safe zones), phone snatches still happen — keep devices pocketed while walking",
        "Only exchange currency at banks or official exchange houses (casas de cambio) — never on the street",
        "Book Machu Picchu and Inca Trail tickets only through the official government portal or your hotel",
    ],
    "Krakow": [
        "In the Old Town, confirm prices before entering a restaurant — the tourist restaurant zone near Market Square has overcharging issues",
        "Use licensed taxi apps (Bolt, FreeNow) over street hails — especially at night from bars in Kazimierz",
        "Don't accept 'free samples' from street vendors unless you're willing to pay for them",
        "Keep bags closed and in front of you on crowded tourist trams near the Old Town",
    ],
    "Paris": [
        "On the RER B from CDG airport, keep bags on your lap — it's the highest-density pickpocket corridor in France",
        "Never sign a petition or receive a 'friendship bracelet' from strangers near the Eiffel Tower or Sacré-Cœur",
        "At restaurants, ask for the menu to verify prices — cover charges and tourist menu markups are common near Notre-Dame and Montmartre",
        "Book taxis via G7 or Uber app — never accept unlicensed drivers offering rides at train stations or tourist sites",
    ],
    "Rome": [
        "On the Metro A line (Vatican to Termini), keep bags in front of you — it's Rome's busiest pickpocket route",
        "Never let anyone place a rosemary sprig, bracelet, or any item in your hand near tourist sites — you'll be aggressively charged",
        "Check restaurant bills carefully near the Colosseum and Trevi Fountain — 'coperto' (cover charge) is legal, but surprise extras are not",
        "Only take taxis from official white taxi ranks (not touts who approach you) — fares from Fiumicino to city center are fixed at €48",
    ],
    "Bangkok": [
        "If a tuk-tuk driver offers a sightseeing tour for 20 baht, it's a gem store commission scam — avoid entirely",
        "Always insist the taxi meter is running before the ride starts — 'meter broken' means find another cab",
        "Grand Palace is never closed — anyone who tells you it is and offers an alternative tour is a scammer",
        "Use the BTS Skytrain or MRT for most travel — it's fast, air-conditioned, and eliminates taxi negotiation entirely",
    ],
    "Istanbul": [
        "Around Sultanahmet (Blue Mosque / Hagia Sophia / Topkapi), ignore anyone who initiates conversation with 'Where are you from?' or 'Let me show you a tea house' — r/istanbul 'Continually harassed by rug company' (comments/1pb9rl9, 2025) documents the carpet-shop pipeline that starts with these openers",
        "At the Grand Bazaar, treat all first-quoted prices as 50%+ inflated; polite negotiation is expected per r/AskTurkey 'READ THIS if you're planning to visit Turkey' (comments/1jqcxqp, 2025); never enter a shop's back room or 'private viewing area'",
        "Use IstanbulKart for all public transport (Metro, Marmaray, ferries, buses) — buying single tickets is 2–3x more expensive; load €10–€20 on arrival at any kiosk",
        "NEVER accept unsolicited invitations to a 'local bar' from men near Taksim Square or Istiklal Caddesi — r/solotravel 'I met a lot of creepy people while I was in Istanbul' (comments/yctw4z, 2024) documents the basement-bar drink-scam pattern with bills of €500–€2,500",
        "Don't get scammed at Hagia Sophia — r/istanbul_tips 'Don't get scammed at Hagia Sophia' (comments/1sdtbmf, 2025) warns about the calculator-trick where the cashier shows one ticket price but charges a higher amount on the credit card terminal; book Hagia Sophia + Topkapi tickets in advance via the official Müze app at muze.gov.tr",
    ],
    "Prague": [
        "In bars near Old Town Square and Wenceslas Square, always ask for a menu with prices before ordering — some bars charge tourist rates 10x above normal",
        "Use Bolt or Liftago apps for taxis — unlicensed taxi drivers at tourist spots are notorious for overcharging by 5–10x",
        "Exchange currency only at banks or official exchange houses showing buy/sell rates — zero-commission kiosks often have terrible hidden rates",
        "Keep a firm grip on bags in the Old Town Square crowds and on tram lines 17 and 18",
    ],
    "Marrakech": [
        "In the Medina, a 'free' guide who approaches you will expect substantial payment at the end — agree on a price upfront for any guide",
        "At Djemaa el-Fna square, entertainers (snake charmers, monkey handlers) will demand payment if you photograph them — agree on a price first or don't photograph",
        "Negotiate all prices before shopping in the souks — initial prices are almost always dramatically inflated",
        "Book taxis through your riad — street taxi prices for tourists are rarely metered and require firm pre-negotiation",
    ],
    "Cairo": [
        "At the Pyramids, anyone who approaches you on a horse, camel, or on foot offering help is not free — agree on a firm price for everything before accepting",
        "Use Uber or Careem for all transport in Cairo — metered taxis rarely use meters with tourists",
        "Never accept 'papyrus' or other items placed in your hands near temples or museums — you'll be pressured to pay",
        "Ignore claims that a museum or attraction is 'closed today' from anyone not wearing an official uniform — it's a scam to redirect you to a shop",
    ],
    "Buenos Aires": [
        "Be alert to fake police officers who ask to check your wallet for 'counterfeit bills' — real police do not do this",
        "Use official remise (radio-dispatched) cars or Uber for airport trips — unlicensed taxis at EZE are a known safety risk",
        "Only exchange currency at legal exchange houses (cambios) or banks — while the black market rate is tempting, it exposes you to counterfeit bills and robbery",
        "In La Boca neighborhood, stay on the main tourist street (Caminito) during the day and don't wander into residential blocks",
    ],
    "New York City": [
        "Ignore anyone offering you a CD, friendship bracelet, or any unsolicited item on Times Square — it will cost you",
        "Use only licensed yellow cabs (medallion taxis), green boro taxis, or the Uber/Lyft apps — unlicensed cars are illegal and unaccountable",
        "Keep phones in pockets at all times on the subway — phone snatches through closing doors are a known and increasing pattern",
        "At Times Square and Penn Station, ignore scalpers offering discounted Broadway or concert tickets — use TodayTix or official box offices",
    ],
    "Vienna": [
        "Mozart/Strauss concert ticket sellers near St. Stephen's Cathedral are legitimate, but compare prices — street hawkers charge significantly more than booking online",
        "Taxis are metered and honest, but fares from Vienna Airport are significantly cheaper by train (CAT or S-Bahn) — €4 vs €40",
        "At coffee houses near tourist sites, the 'tourist menu' is often poor value — ask for the Tageskarte (daily specials) or Mittagsmenü instead",
        "Pickpocketing happens on U-Bahn lines U1 and U4 at peak times near tourist stops — keep bags closed and in front",
    ],
    "Vancouver": [
        "Book airport taxis only via the official regulated taxi queue or use Uber/Lyft — unlicensed drivers are rare but overcharging at YVR is documented",
        "In Gastown and the Downtown Eastside, be aware of aggressive panhandling — this is manageable but can be intimidating for first-time visitors",
        "At the Canada Place cruise terminal, avoid touts offering 'better' city tours — book directly with operators like Landsea Tours for accountability",
        "Keep bikes locked with a quality U-lock — bike theft is Vancouver's #1 property crime and even 'cheap' bikes disappear quickly",
    ],
    "Florence": [
        "Keep hands in pockets near the Duomo and Ponte Vecchio — bracelet scammers will try to grab your wrist and tie one on before you react",
        "Walk one or two streets away from major sights for restaurants — tourist-facing places near Piazza della Repubblica routinely add hidden cover charges",
        "On ATAF buses (especially lines 1 and 7), keep phones and wallets in front pockets — organized pickpocket teams work these routes daily",
        "Watch your step near the Uffizi — street vendors lay paintings in walkways hoping you'll step on one and pay for 'damage'",
    ],
    "Dublin": [
        "Use only metered taxis or ride apps like Free Now — never accept a 'flat rate' from a driver, especially at Dublin Airport",
        "In Temple Bar, choose your own pub — locals who invite you to 'the best place' around the corner often lead to overcharging bars",
        "Keep phones in pockets on Grafton Street and at Luas stops — phone snatching on foot and by bicycle is increasing",
        "Cover your PIN at ATMs and use machines inside banks — card skimming devices have been found on ATMs near O'Connell Street",
    ],
    "Copenhagen": [
        "Keep bags zipped and in front on the Metro and at Nyhavn — pickpocketing is Copenhagen's most common tourist crime",
        "At Strøget and Tivoli, be wary of anyone who bumps into you or creates a distraction — it's often a coordinated pickpocket team",
        "Use Rejsekort or contactless payment for transport — buying single tickets is expensive and ticket inspectors fine without warning",
        "Don't leave bikes unlocked even briefly — bike theft is rampant and rental shops will charge you the full replacement cost",
    ],
    "Budapest": [
        "Never follow attractive strangers to a bar in the District V area — the 'pretty girl bar scam' can result in bills of hundreds of euros enforced by bouncers",
        "Exchange currency only at banks or official exchange offices — the exchange booths on Váci utca are notorious for hidden fees and terrible rates",
        "On tram lines 4/6 and the M1 metro, keep valuables in front pockets — organized pickpocket groups target tourists on these routes",
        "At restaurants near the Danube and Fisherman's Bastion, always check the bill line by line — surprise charges for bread, music, and service are common",
    ],
    "Dubrovnik": [
        "Book Game of Thrones tours only through licensed operators with TripAdvisor reviews — unlicensed guides charge premium prices for basic walks",
        "In the Old Town, check restaurant prices before sitting — menus near the Stradun can charge 3x what restaurants just outside the walls charge",
        "Use the city bus or walk between beaches and Old Town — unlicensed taxi boats sometimes overcharge and lack safety equipment",
        "Keep bags closed in crowds at the Pile Gate entrance — the morning cruise ship crush is prime pickpocket territory",
    ],
    "Santorini": [
        "At Athinios Port, walk past the 'public bus €15' recruiters — the real KTEL public bus is €2.40 to Fira and €2 to Oia; the ktel-santorini.gr site posts timetables",
        "At restaurants on the caldera rim, demand per-portion prices in writing for fish — 'per kilo' billing routinely produces €200+ bills for a single seabass",
        "Rent cars by credit card only (never cash), photograph every panel including the underside, and choose vetted agencies: Santorini-Rentacar, Kosmos, Damigos",
        "For Fira to old port transport, take the cable car (€6, every 20 min) rather than donkeys — faster, safer, and avoids the mid-descent price-hike scam",
        "Confirm your hotel reservation by phone 48 hours before arrival using the Google Maps number; never pay via links in emails, even ones that look like Booking.com",
    ],
    "Mykonos": [
        "Do not eat at DK Oyster on Platys Gialos Beach — Metro and The Sun ran 2025 stories of £1,000 and €1,350 bills; the scam has run at this venue for over a decade",
        "Greek law prohibits unlisted cover charges — restaurants can be fined €500 for bread/olives added without menu disclosure; refuse welcome items explicitly",
        "Use KTEL buses (€2 from Fabrika station to Paradise Beach, Platys Gialos, Ornos) rather than Old Port taxis quoting €40 for the same routes",
        "Ignore any Mykonos reservation or tour offer received via Instagram DM or Reddit DM — the r/Mykonos moderators posted an explicit 2024 scam warning",
        "For luxury shopping, buy only at official brand stores (Gucci, LV, Valentino) on Matoyianni — 'designer' items at 20% of real price are counterfeit and will be seized at UK/US customs",
    ],
    "Heraklion": [
        "Rent cars from major brands at Heraklion Airport (Avis, Budget, Hertz, Europcar, Sixt) — not Heraklion Town storefronts like Abbycar Crete that are community-flagged for damage scams",
        "Photograph every panel of a rental car (including underside and wheel wells), get a written damage inspection signed, and pay by credit card for chargeback leverage",
        "At Knossos Palace, look for the yellow Greek Federation of Tourist Guides badge — public group tours are €20–€25 per person; 'private tours' quoted at €80–€120 are dramatically overpriced for the same content",
        "At Elafonissi and Balos beaches, drive past the first few parking attendants — 'the closer lots are full' claims are routinely false (€5 lots redirect you from €3 lots)",
        "Buy Cretan olive oil at supermarkets (Sklavenitis, AB Vasilopoulos) — Leventakis and Sitia Co-op at €6–€10 per 500ml; tourist shops charge €25+ for 250ml of the same quality",
    ],
    "Thessaloniki": [
        "Screenshot FreeNow or Beat app fare estimates before any SKG airport ride — drivers add 'tolls' and 'surcharges' that the 2025 r/uber Thessaloniki case documents clearly",
        "From Thessaloniki Airport, take the 01X or 78N public bus for €2 — 45–60 min to the city, scam-free; the KTEL website posts live schedules",
        "Refuse welcome bread, olives, tzatziki at Ladadika and White Tower waterfront restaurants — Greek law prohibits unlisted cover charges (€500 fines)",
        "Do not attempt Meteora as a day trip from Thessaloniki — the 10-hour total drive time makes it a rushed, low-value experience; overnight in Kalambaka instead",
        "At Aristotelous Square and the White Tower promenade, cross your arms immediately if anyone approaches with a bracelet or flower — team pickpockets operate here June–September",
    ],
    "Rhodes": [
        "Rhodes Old Town bars using no-menu or 'novelty glass' pricing were specifically named in Daily Mail and Greek Herald June 2025 coverage — always verify a printed drink menu before sitting",
        "Walk from Kolona cruise port to Rhodes Old Town — it is 5 minutes on foot; taxis quoting €15+ for this route are overcharging",
        "From Diagoras Airport (RHO), use the KTEL bus (€2.40, 30–45 min) or FreeNow/Beat apps for regulated fares",
        "For Lindos Acropolis, walk the 10-minute steep path — do not ride the donkeys (mid-ascent price hikes and documented welfare issues)",
        "Do not buy counterfeit designer goods in the Sokratous Street 'fake market' — UK and US customs will seize at the border",
    ],
    "Corfu": [
        "Walk from Kerkyra cruise port to Corfu Old Town — it is 10 minutes along a flat scenic waterfront; taxis quoting €40 for this route are overcharging",
        "Use Green Bus (KTEL Kerkyras) for Achilleion (bus 10, €3), Paleokastritsa (bus 8, €5), and Kanoni (walkable 45 min) — published at greenbuses.gr",
        "For Porto Timoni, hike in the cool morning (before 10 AM) with proper shoes — refuse ATV 'transportation' at the Afionas trailhead (€10 quote escalates to €30)",
        "Rent cars from major brands at Corfu Airport (CFU) — avoid Carwiz specifically and resort-area storefronts in Dassia, Ypsos, Paleokastritsa",
        "At Liston and the Old Town, enjoy one tourist-priced coffee or cocktail for the experience; walk inland for actual meals (Pane & Souvlaki, Chrisomalis, Aegli)",
    ],
    "Chania": [
        "At the Old Venetian Harbour, budget for one coffee or cocktail as the tourist premium; eat meals two or three blocks inland where local tavernas serve at half the price",
        "From Chania Airport (CHQ), take the KTEL bus to Old Town for €2.50 every 30 min — or demand the meter (€1.06/km) on any taxi; real fare €25–€35",
        "For Balos, take the direct Balos Cruise ferry from Kissamos Port (€30–€35) — do not book €70+ tour packages from Chania storefronts",
        "For Elafonissi, drive past the first few parking attendants — 'closer lots are full' claims are the 2025 viral scam variant",
        "Pay petrol by credit card at all Crete stations — the Souda Shell station is specifically named on r/crete for short-change scams",
    ],
    "Paros": [
        "Pre-book a hotel transfer (€15–€25) from Parikia port rather than using the port taxi rank — drivers quote €40 for 5-minute rides to central Parikia",
        "Greek minimum taxi fare is €4 plus €1 port surcharge — anything above €15 for a short ride is overcharging",
        "For Antiparos, take the Pounda–Antiparos ferry yourself (€2.50 each way, every 30 min) — storefront 'Antiparos day tours' at €60–€90 are dramatic markups on what should be €15",
        "Rent cars at Paros Airport (PAS) from major brands (Avis, Europcar, Hertz, Sixt) — avoid Carwiz specifically across all Greek markets",
        "Never click payment links in 'Booking.com' emails — log into the platform directly; Paros hotel off-platform scams target peak-season bookings",
    ],
    "Naxos": [
        "Never rent from Matha Rent a Car on Naxos — r/GreeceTravel posted an explicit 'DO NOT RENT WITH MATHA' community warning; prefer Europcar at Naxos Airport (JNX)",
        "For sunbeds at Plaka, Agios Prokopios, or Alyko beaches, ask for total price in writing for full day, two chairs and umbrella — avoid per-chair-per-hour pricing ambiguity",
        "Take KTEL Naxos buses for villages: Apiranthos €4, Halki €2.50, Filoti €2.50 — 'Traditional Village Tour' packages at €55–€85 per person are dramatic markups",
        "Pay rental cars only with a dedicated travel credit card you can lock after return — Naxos shops have been flagged for post-return fraud charges",
        "Pre-book hotel transfers for Naxos port or airport arrivals — port taxi quotes of €20 for 1 km walk to Chora are overcharging",
    ],
    "Phuket": [
        "Never accept a tuk-tuk or taxi ride without agreeing on the price first — meters don't exist and prices triple for tourists who don't negotiate",
        "At Patong Beach, jet ski operators will claim you damaged the equipment and demand thousands of baht — avoid jet ski rentals from beach touts entirely",
        "Book boat tours to Phi Phi and James Bond Island through your hotel — street-booked tours often use unsafe boats with no insurance",
        "Ignore gem shop tours offered by tuk-tuk drivers — the 'government gem sale' is Thailand's most persistent tourist scam",
    ],
    "Ho Chi Minh City": [
        "From Tan Son Nhat Airport (SGN), book Grab/Be yourself on airport Wi-Fi AFTER luggage pickup — r/VietNam 'HCMC Airport (Grab prentending) taxi Scam' (comments/1p3puug, 2025) warns about fake-Grab-driver scams in arrivals hall",
        "Use ONLY Vinasun (white/red/gold, phone 1900-1055) or Mai Linh (green, 1055) licensed taxis; insist on the meter — r/VietNam 'HCMC taxi scam, a cautionary tale' (comments/dzk58l) documents Vinasun copycats with near-identical branding",
        "NEVER carry phone in hand while walking in District 1 — r/VietNam 'Moped following me at night in the dark in HCMC?' (comments/1ncdomn, 2025) documents 2025 motorbike bag/phone snatches; wear crossbody zipped in front",
        "For solo male travellers, stay on the main Bui Vien pedestrian strip — r/VietNam 'Ho Chi Minh City Walking Street (Bùi Viện) 4 million VND Scam' (comments/1lf9jl6, 2025) documents side-street bar extortion",
        "Skip Ben Thanh Market for shopping; cross to Saigon Square instead — r/VietNam 'Saigon Square is what tourists think Ben Thanh Market is' (comments/1n9nxdg, 2025) names locals' fixed-price alternative",
    ],
    "Hue": [
        "From Phu Bai Airport (HUI), book Grab/Be yourself — expected 150K–220K VND to central Hue; r/VietNam 'Grab scammers Dong Hoi & Hue targeting tourists' (comments/1azj3g1, 2025) documents 700K VND overcharges",
        "Buy Imperial City tickets at OFFICIAL Ngọ Môn Gate booth (200K VND adult, 420K combined with 2 tombs) — SINGLE ENTRY; plan 3–4 hours without exiting per r/VietNam (comments/1scth5u, 2025)",
        "Agree TOTAL cyclo price (not per person) in writing before boarding — typical 50K–100K VND for 15–30 min; use GrabBike (30K–50K VND) as alternative",
        "Never hand large-denomination notes (500K, 200K) to street vendors — r/VietNam 'Got scammed twice in a matter of few moments' (comments/1rx8yd1, 2025) documents the bicycle-pusher switch scam",
        "For motorbike experiences, use Easy Rider pillion operators ($50–$80/day) rather than DIY — safer for older travellers given Vietnamese traffic",
    ],
    "Hoi An": [
        "Use community-verified tailors (Yaly Couture, Bebe Tailor, A Dong Silk) with 2–3 days for fittings — r/VietNam 'Worst Tailor in Hoi An' (comments/1inj004, 2025) warns about 24-hour rush jobs and fabric markup",
        "Book Ancient Town ticket at OFFICIAL booths (120K VND adult, 2025) — covers 5 of 20+ monuments; refuse 'combo ticket' touts per r/VietNam 'Tickets for old town hoi an' (comments/1hos5u9, 2025)",
        "Book river boat rides ONLY at posted-price Bach Dang dock (150K–200K VND for 20–30 min) — r/VietNam 'BEWARE HOI AN SCAM' (comments/1l80zcz, 2025) warns about mid-aged women booking 3–5x markup",
        "NEVER try on fruit-basket props offered by street women — r/DaNang 'What to scams to look out for in Hoi Ann' (comments/1k18dh6, 2025) documents photo-demand scam",
        "Book cooking classes and tours DIRECT (Red Bridge, Morning Glory, Vy's Market) or via Klook — r/VietNam 'Scams after scams' (comments/1s5018d, 2025) warns about hotel 'partner' kickbacks",
    ],
    "Ninh Binh": [
        "Book Trang An boat tour at the OFFICIAL ticket counter (150,000 VND/person, 2025) — never at roadside 'booths' per r/VietNam 'Warning - Trang An/Ninh Binh experience with abusive kids' (comments/1h0br4q, 2025)",
        "Book Hanoi-Ninh Binh train only at dsvn.vn, baolau.com, or 12go.asia — r/hanoi 'Warning : taking the train is a scam!' (comments/1p67b98, 2025) warns about clone sites marking up 2-3x",
        "On overnight train Ninh Binh-Hue, REFUSE any attendant demanding cash for 'bed/sheets/AC' — r/VietNam 'Brazen scam on overnight train from Ninh Binh to Hue' (comments/1c0bzbj, 2024) documents this",
        "Pay Tam Coc sampan rower 150,000 VND (official ticket) + 50K–100K tip at end only — decline ALL mid-river drink/souvenir/photo sales per r/travel 'Took a $5 boat ride in Ninh Binh' (comments/5o6v7x)",
        "For rides, use Grab or Be app (highway tolls INCLUDED); refuse off-app deals — r/VietNam 'Do you have to pay highway ticket on top of Grab ride' (comments/1ivi8la, 2025) is the named 2025 highway-fee-scam anchor",
    ],
    "Da Nang": [
        "From Da Nang Airport (DAD), book Grab/Be yourself on airport Wi-Fi AFTER luggage — r/DaNang 'What to scams to look out for in Hoi Ann' (comments/1k18dh6, 2025) specifically warns about DAD copycat taxis",
        "For Ba Na Hills, book DIRECT at banahills.sunworld.vn ($45 USD adult) — skip hotel 'partner tour' at $80+; visit Mar–Nov for reliable weather per r/VietNam (comments/1hk0reg, 2025)",
        "At Marble Mountains, buy entrance ticket (40K VND) at official booth; skip ALL base souvenir shops — r/VietNam (comments/193vmix, 2024) documents jade/marble kickback scams",
        "NEVER follow a 'friendly local' couple home — r/DaNang 'The Where are you from? couple in An Thuong' (comments/1jrd6sn, 2025) documents tea/silk/herbs upsell pattern",
        "At Dragon Bridge Sat/Sun 9 PM fire show, wear crossbody zipped in front and use phone wrist strap — dense crowd creates pickpocket risk",
    ],
    "Nha Trang": [
        "From Cam Ranh Airport (CXR), use Grab/Xanh SM — expected CXR-Nha Trang fare 300K–450K VND; r/Vietnam_Tourism 'Nha Trang train taxi scam' (comments/1qw9eqh, 2025) documents 10x overcharges at train station",
        "NEVER leave phone on beachfront café table or pool-side towel — r/VietNam 'Just had my iPhone stolen in Nha Trang' (comments/1pw1f3k, 2025) documents 2025 beach/pool thefts; use hotel safe + waterproof pouch",
        "NEVER follow late-night street solicitor to any 'massage' or 'bar' — r/nhatrang 'Nha Trang Massage Scam' (comments/1e3klo8, 2025) documents 3 AM inflated-bill extortion; book only at resort spas",
        "Ask for the Vietnamese-language menu at restaurants — per r/VietNam 'I am disgusted that some people defend the act of charging' (comments/1bfnsng, 2024), English/Russian menus routinely show 2-3x pricing",
        "Book 4-island boat tour via Klook/GetYourGuide at $25-35 per person — skip hotel 'partner' packages at $60-80 and 'booze cruise' versions",
    ],
    "Sapa": [
        "Book Hanoi-Lao Cai train only at dsvn.vn, baolau.com, or 12go.asia, then Grab/Xanh SM for Lao Cai-Sapa — r/VietNam 'Defrauded in Sapa even when booked through official' (comments/1pxdugb, 2025) documents 2025 station-transfer fraud",
        "Book trekking guides DIRECTLY (Sho +84 365 645 165, Mayland Trekking) — r/VietNam 'Local Trekking Guide recomandation for Sapa' (comments/1bbyoa3, 2024); skip hotel-concierge packages at $40-60",
        "REFUSE village 'family shop' pressure sales — buy Hmong textiles at Bac Ha Sunday Market for fair prices; verify 'silver' with magnet test (real silver is non-magnetic)",
        "For Fansipan cable car, buy direct at fansipanlegend.sunworld.vn (~800K VND) and check weather/status that morning — r/Vietnam_Tourism 'Fansipan funicular & cable car closed during my trip' (comments/1o630yd, 2025) documents closure fraud",
        "In Sapa town, walking distance to most attractions is under 500m — electric cart rides should cost 10K-20K VND per ride; refuse 50K+ quotes per r/VietNam 'Just got scammed by a local driver in Sa Pa' (comments/1sifegb, 2025)",
    ],
    "Phu Quoc": [
        "At Phu Quoc Airport (PQC), use Xanh SM (VinFast electric) or Grab — expected fare to Duong Dong 150K–200K VND per r/VietNam 'Grab in Phu Quoc' (comments/1eyk3ng, 2024); REFUSE drivers claiming 'no Grab here'",
        "SKIP pearl-farm 'educational tour' stops — they are sales funnels; r/VietNam 'Phu Quoc scam?' (comments/1iiex7f, 2025) is the named 2025 anchor; buy genuine pearls only at Long Beach Pearl Farm with GIA certification",
        "SKIP jet-ski and parasailing rentals — r/Scams 'DO NOT RENT JETSKIS IN THAILAND' (comments/1gdyd5g, 2024) Southeast-Asia damage-deposit pattern applies in Phu Quoc; NEVER leave passport as deposit",
        "Book massages ONLY at named resort spas (Vinpearl, La Veranda, JW Marriott, Sol by Meliá) — r/VietNam 'I just had super weird experience' (comments/1jjo7c6, 2025) documents tourist-strip upcharge pressure",
        "Book Cable Car + 3-island tour via Klook/GetYourGuide ($35-50) — skip 4-island version and $120 'VIP' packages per r/VietNam 'Phu Quoc which 4-island tour option is better?' (comments/1rfh3n4, 2025)",
    ],
    "Dalat": [
        "From Dalat Lien Khuong Airport (DLI), use Grab or Xanh SM — expected 250K–350K VND to city centre; r/VietNam 'Đalat Scam?' (comments/1o70zlp, 2025) warns about 'officials' demanding fraudulent airport fees",
        "For canyoning, use ONLY licensed operators (Viet Challenge, Phat Tire Ventures, Highland Sport Travel) at $55-80/day — skip $25-35 budget operators that lack insurance and certified gear",
        "Refuse 'free photographer' at Valley of Love — charges 200K+ per print; bring your own camera per r/VietNam (comments/yrge82, 2024)",
        "Book Dalat hotels ONLY via Booking.com/Agoda — r/VietNam 'I got scammed trying to book a stay in Da Lat' (comments/1jb702w, 2025) documents fake-resort-page fraud targeting direct bookings",
        "At Dalat Night Market, expected local prices: bánh tráng nướng 20-30K, strawberries 50K/500g, soy milk 10K — carry small notes to avoid 'no change' scams per r/VietNam (comments/1cg48yb, 2025)",
    ],
    "Can Tho": [
        "SKIP HCMC one-day Mekong Delta tours — kickback stops at 'coconut candy factory' and 'honey bee farm' per r/VietNam (comments/1irke41, 2025); book 2D/1N via TNK Travel ($60-80) instead",
        "At Cai Rang Floating Market, arrive by 5:30-6 AM; book boat at posted-price dock (150K-200K VND/hour) — r/VietNam 'Cai Rang market in Can Tho is it still good?' (comments/1h79j01, 2024) documents the declining authenticity",
        "Book Mekong homestays via Booking.com/Agoda only — community-recommended: Ecoco Homestay (Ben Tre), Nguyen Shack (Can Tho); r/VietNam (comments/1fnt2d6, 2025) is named anchor",
        "For Can Tho taxis, use Grab or Xanh SM — airport VCA to centre 150K-200K VND; refuse hotel-doorstep 'local driver' solicitations quoting 1M+ VND/day tours",
        "Verify tour operator International Tour Operator License via vietnamtourism.gov.vn — r/VietNam 'It's a bit late now, but is this a legitimate company?' (comments/1rypfl0, 2025) documents unlicensed-operator fraud",
    ],
    "Petra": [
        "Never accept a 'free' camel or donkey ride inside Petra — the handler will block your path and demand $50+ when you try to dismount",
        "Hire guides only through the official Petra Visitor Centre — unlicensed guides who approach at the entrance will overcharge and pressure for tips",
        "Bargain aggressively for souvenirs inside Petra — first-quoted prices are typically 3-5x the fair price for tourists",
        "Stick to official marked trails — locals who lead you to 'secret viewpoints' will demand payment for access to what is often public land",
    ],
    "Jerusalem": [
        "In the Old City markets, never accept a 'free' tour from shopkeepers — it always ends at their store with aggressive sales pressure",
        "Use only licensed taxis with meters or book through Gett app — unlicensed drivers near Damascus Gate routinely overcharge tourists",
        "At the Western Wall plaza, ignore anyone offering to write prayers for you for a 'donation' — it's a common hustle targeting visitors",
        "Be cautious of guides who offer to take you to rooftop viewpoints in the Muslim Quarter — some demand payment after and the locations may be unsafe",
    ],
    "Reykjavik": [
        "Book Northern Lights tours and glacier excursions only through operators with verifiable reviews — some budget operators cancel without refunds",
        "Car rental damage scams are common — photograph your rental from every angle before driving off and decline unnecessary insurance upsells",
        "Restaurants in central Reykjavik are legitimately expensive (not a scam), but 10-101 Reykjavik and Hlemmur Mathöll food hall offer better value",
        "Don't leave valuables visible in rental cars at tourist stops — car break-ins at remote sites like Seljalandsfoss happen despite Iceland's low crime rate",
    ],
    "Edinburgh": [
        "On the Royal Mile, ghost tour companies are generally legitimate — but compare prices online before booking from street hawkers who charge premiums",
        "Keep phones and wallets secure in crowds during the Edinburgh Festival (August) — the massive crowd density creates pickpocket opportunities",
        "Use Lothian Buses or walk — unlicensed 'taxi' drivers outside pubs on Cowgate and Grassmarket at night occasionally overcharge tourists",
        "At whisky shops near the Castle, compare prices with supermarkets — tourist shops mark up standard bottles by 50-100%",
    ],
    "Bruges": [
        "In the Markt square, horse-drawn carriage prices should be posted — confirm the route and price before boarding to avoid surprise charges",
        "Tourist restaurants on the Markt charge 2-3x local prices — walk two blocks to any side street for the same Belgian cuisine at fair rates",
        "Chocolate shops near the Belfry are often overpriced tourist traps — locals shop at Dumon, The Chocolate Line, or BbyB for quality at better prices",
        "Bike rental shops should provide a lock — if yours doesn't, buy one, as bike theft happens even in small, safe Bruges",
    ],
    "Nice": [
        "On the Promenade des Anglais, keep phones in pockets — motorbike snatches happen along the beachfront, especially near the Old Town end",
        "At restaurants in Vieux Nice, ask for the menu with prices — some waiters quote verbally then add extras on the bill",
        "Use the Lignes d'Azur tram and bus system — taxis from the airport to the city center should cost €20-32 by meter, anything more is overcharging",
        "On the beach, never leave bags unattended — opportunistic theft from beach towels is Nice's most common tourist crime",
    ],
    "Split": [
        "Inside Diocletian's Palace, be skeptical of 'impromptu' guides who approach you — agree on a price before any tour or politely decline",
        "At the Riva waterfront restaurants, always check the bill — tourist-facing places sometimes add undisclosed cover charges and bread fees",
        "Book island ferries (Hvar, Brač) through Jadrolinija's official website — touts at the port sell overpriced 'fast boat' tickets for the same routes",
        "Use Uber or Bolt in Split — street taxis at the bus station and ferry port occasionally refuse meters and quote inflated prices",
    ],
    "Phnom Penh": [
        "Use the PassApp or Grab app for tuk-tuks and taxis — street tuk-tuk drivers near the Royal Palace overcharge tourists by 3-5x",
        "Never accept tours to 'shooting ranges' outside the city from tuk-tuk drivers — these operations are unlicensed and occasionally dangerous",
        "Keep bags on your lap in tuk-tuks, not on the seat — motorbike bag snatches from moving tuk-tuks are common along the riverside",
        "At the Russian Market and Central Market, bargain to 40-50% of the first quoted price — initial tourist prices are always dramatically inflated",
    ],
    "Siem Reap": [
        "Book Angkor Wat tours only through your hotel or licensed operators — tuk-tuk drivers who approach at the airport often overcharge and skip temples",
        "Buy your Angkor pass only at the official ticket office on Apsara Road — anyone selling tickets elsewhere is selling fakes",
        "At Pub Street restaurants, check prices before ordering — some menus show USD prices that are 2-3x the local price",
        "Be cautious of children selling souvenirs or postcards near temples — while sympathetic, buying encourages child labor and the money rarely reaches them",
    ],
    "Manila": [
        "Use Grab exclusively for transportation — regular taxis in Manila frequently have rigged meters or refuse to use them entirely",
        "In Intramuros and Rizal Park, ignore anyone offering unsolicited tours or 'help' getting somewhere — it invariably leads to a request for money",
        "Keep phones and valuables completely hidden in crowded areas like Divisoria Market — phone snatching and pickpocketing are extremely common",
        "Never exchange money on the street — use bank ATMs or licensed exchange offices in shopping malls",
    ],
    "Havana": [
        "Only use official yellow taxis or negotiate with classic car drivers before getting in — unlicensed taxi drivers overcharge dramatically",
        "At restaurants and paladares, confirm if prices are in CUP (Cuban pesos) or USD — some menus show CUP prices but charge USD",
        "Ignore jineteros (hustlers) who approach offering cheap cigars, restaurants, or casa particular recommendations — they earn commissions that inflate your price",
        "Buy cigars only from official La Casa del Habano shops — street cigars are almost always counterfeit, even when they look authentic",
    ],
    "San Juan": [
        "In Old San Juan, use only clearly marked taxis or Uber — unlicensed drivers near the cruise port occasionally overcharge tourists",
        "At Condado Beach, don't leave valuables unattended — opportunistic beach theft is the most common tourist crime in San Juan",
        "Book excursions to El Yunque and bioluminescent bays through verified operators — street touts sometimes sell tours that get cancelled without refunds",
        "At souvenir shops in Old San Juan, compare prices — items near cruise ship docks are marked up 50-200% over shops a few blocks inland",
    ],
    "Medellín": [
        "Use Uber or InDriver exclusively — never hail street taxis, especially at night, as express robbery via unlicensed taxis is a documented risk",
        "In El Poblado and Parque Lleras, don't accept drinks from strangers — scopolamine (burundanga) drugging is a real and serious threat in Medellín",
        "Keep phones completely hidden when walking — phone snatching by motorbike is common, especially along busy streets in Centro",
        "Book Comuna 13 tours through established operators with TripAdvisor reviews — unlicensed 'guides' who approach at the base sometimes lead to unsafe areas",
    ],
    "Osaka": [
        "In Dotonbori, be cautious of touts outside bars — while less dangerous than Tokyo's Kabukicho, some bars overcharge tourists who are led in by recruiters",
        "Use the Osaka Metro or JR lines instead of taxis — taxi fares in Osaka are legitimate but expensive, and trains go everywhere tourists need",
        "At Kuromon Market, prices have risen significantly for tourists — compare stall prices before buying, as some charge 3x for the same sashimi",
        "Keep wallets secure in crowds at Shinsekai and Namba — while Osaka is very safe, pickpocketing in dense tourist areas has been increasing",
    ],
    "Aruba": [
        "Aruba's taxis have no meters — fares are government-fixed by destination. Airport to Palm Beach is approximately $22-25 USD. Only use vehicles with 'TX' license plates and a roof-mounted taxi sign",
        "Avoid the San Nicolas district after dark — while daytime street art and Charlie's Bar are legitimate, the area has a documented reputation for car break-ins and confrontational individuals at night",
        "Leave your actual passport locked in your hotel safe — carry a photocopy and a photo on your phone. Police accept copies for routine checks",
        "The east and north coasts have powerful Atlantic surf with dangerous rip currents and no lifeguards — stick to calm west coast beaches (Palm Beach, Eagle Beach) for swimming",
    ],
    "Puerto Vallarta": [
        "Download offline maps before exploring — cell service is spotty outside the Zona Romantica and hotel zone, and getting lost triggers aggressive tuk-tuk and tour approaches",
        "Use Uber for all transport — it works throughout PV and eliminates taxi negotiation. If you must take a taxi, agree on the fare in pesos before getting in",
        "At restaurants, always ask for 'la cuenta desglosada' (itemized bill) and check if service charge is already included before tipping on top",
        "Walk straight through the airport arrivals area without stopping — the gauntlet of timeshare promoters is designed to intercept you before you reach your transfer",
    ],
    "Cabo San Lucas": [
        "Always pay in Mexican pesos (MXN) rather than USD — restaurants, taxis, and shops that accept dollars set their own exchange rates, typically 5-15% worse than the bank rate",
        "Pre-book all airport transportation before you land — the walk from SJD arrivals runs a gauntlet of timeshare promoters and pirate taxi operators",
        "Stick to licensed vendors on Medano Beach who wear white uniforms with visible ID badges — unlicensed operators in street clothes are most likely to overcharge or run damage scams",
        "Uber works in Cabo and is significantly safer and cheaper than street taxis — download the app before your trip, especially for nighttime rides near the bar district",
    ],
    "Punta Cana": [
        "Do not drink tap water anywhere in Punta Cana, including at all-inclusive resorts — stick to sealed bottled water and avoid ice at non-resort establishments",
        "Apply mosquito repellent every evening, especially during sunset — Dengue fever is present in the region and prevention through avoiding bites is the only protection",
        "Carry only small amounts of cash and leave your passport in the hotel safe — credit card cloning is widespread, so use cash outside your resort whenever possible",
        "Avoid walking outside resort areas after dark — use Uber Select or arrange transportation through your hotel rather than flagging unmarked vehicles",
    ],
    "Turks and Caicos": [
        "Bringing even a single round of ammunition into TCI is a criminal offense carrying mandatory prison time — check all bags carefully before travel if you are a firearm owner",
        "Avoid the 'Five Cays' and 'The Bight' areas of Providenciales after dark — these neighborhoods have higher crime rates than the Grace Bay tourist corridor",
        "Check restaurant bills for automatic gratuity before tipping — many tourist restaurants add 15-18% service charge that is easy to miss",
        "TCI has limited medical facilities — travel with comprehensive health insurance that includes medical evacuation, as serious conditions require airlifting to Miami or Nassau",
    ],
    "Curacao": [
        "Always lock your rental car and store all belongings out of sight in the trunk, especially at beach parking lots like Mambo Beach where car break-ins via smashed windows are regularly reported",
        "Stick to well-lit main streets in Punda and Pietermaai at night and avoid walking alone through Otrobanda after dark, as most crime incidents involve poorly lit or isolated areas",
        "Use only ATMs inside bank branches (MCB, Banco di Caribe) in Willemstad and avoid standalone machines, which are targets for skimming devices",
        "Contact Politur Curacao, the dedicated tourism police force, at any time for safety concerns or to report incidents — they have the same authority as regular police and are focused on visitor safety",
    ],
    "Antigua": [
        "Confirm taxi fares and currency (EC$ vs US$) before every transaction — the dual-currency system is the most exploited confusion point for tourists in Antigua",
        "Stick to well-known beaches like Dickenson Bay and Jolly Beach where security patrols are present, and avoid isolated beaches alone, especially after the robbery pattern at Little Ffryes Beach",
        "Book tours and water sports only through licensed operators verified by your hotel or cruise line — never hand your passport to a beach vendor as a security deposit",
        "Walk through Heritage Quay's taxi gauntlet without stopping and find the official taxi stand with posted government rates — knowing the standard fare to your destination in advance is your best defense",
    ],
    "Roatan": [
        "Stay within the tourist corridor of West End, West Bay, and the cruise port areas where security is concentrated — venturing into Coxen Hole town or other areas alone is not recommended, especially after dark",
        "Book all tours and transportation through your cruise line, hotel, or verified operators with TripAdvisor reviews — pre-payment scams from unknown websites are a significant risk in Roatan",
        "Photograph the official taxi fare zone chart at the cruise port before venturing out, and always negotiate the total fare before getting into any vehicle",
        "Keep valuables in your hotel or cruise ship safe and carry only what you need for the day in a waterproof pouch — Roatan's biggest tourist risk is petty theft on the beach rather than violent crime",
    ],
    "Barcelona": [
        "Wear your backpack across your chest on packed L3 metro trains near Passeig de Gràcia, Liceu, and Sagrada Família stations — r/AskBarcelona (comments/1kyzlwq, 2025) names this the single rule locals give every new arrival",
        "From El Prat Airport (BCN), use the Aerobús (€7.25) or RENFE R2 Nord train (€4.90 with T-Casual) to the city — taxi is €39 fixed, but the airport train is 'lousy with pickpockets' per r/askspain (comments/t2l6xx); Uber, Bolt, FreeNow, and Cabify all work with app-regulated fares",
        "Book Sagrada Família tickets only at sagradafamilia.org — 2025 r/AskBarcelona and r/GoingToSpain threads document fake 'skip-the-line' sites (sagradafamilietickets.org and similar) charging double for invalid QR codes",
        "Never let a stranger touch your wrist, tie a bracelet on you, or hand you rosemary, flowers, or petitions on La Rambla, near Plaça de Catalunya, or outside Sagrada Família — walk past with 'no, gracias' and hands in pockets",
        "Save the Mossos d'Esquadra tourist police office (La Rambla 43, +34 932 903 000) and call 112 for emergencies — a denuncia filed within 48 hours is required for travel-insurance claims",
    ],
    "Seville": [
        "Book Real Alcázar tickets only at realacazarsevilla.cliqueo.es — r/Chase 'Got scammed by a fake Official ticket site for Real Alcázar' (comments/1rrahxh, 2025) and r/GoingToSpain 'Reservas Feel The City Tours - BEWARE' (comments/1rq18qi, 2025) document fake sites charging double for invalid tickets",
        "From Seville Airport (SVQ), use the EA bus (€4) to Plaza de Armas or a licensed taxi (€25 flat to center on weekdays, €27 weekends) — r/Seville 'FREENOW taxi scam' (comments/1n5q7dy, 2025) and 'Cabify and Uber pickup at airport' (comments/1n7c630, 2025) warn that app pickups at the rank are routinely overcharged",
        "Stand at the bar rather than sitting at a table in Santa Cruz and El Arenal tapas bars — menu prices are lower and r/Seville 'Good food - authentic not tourist traps!' (comments/1ommfty, 2025) points to locals-only side streets one block off Calle San Jacinto for honest pricing",
        "Never accept rosemary, flowers, or trinkets from women in traditional dress near the Cathedral and Giralda — keep hands in pockets and say 'no, gracias' before any physical contact; r/GoingToSpain 'Places to avoid? - South Spain' (comments/1d5xpqm) documents the €10–€20 shake-down pattern",
        "Save Policía Nacional Seville (Plaza de la Concordia 1, +34 954 289 300) and the tourist-aid SATE line — file denuncia within 48 hours for insurance and report fake parking-vest collectors at cathedral-area free zones to Policía Local (092)",
    ],
    "Granada (Spain)": [
        "Book Alhambra General Visit tickets (€19.09) only at tickets.alhambra-patronato.es — r/Granada '[IMPORTANT] Do not buy Alhambra tickets through Alhambra.org website' (comments/17to9yp) and r/GoingToSpain 'Misadventure in Granada - Alhambra tickets' (comments/1ki2yxv, 2025) confirm fake sites charge up to €261 for €60 rides",
        "From Federico García Lorca Airport (GRX), the Airport Bus is €3 every 30–90 minutes to the city center — r/travel 'Is there an Uber or equivalent app service for taxi rides in' (comments/1co6ca8, 2025) documents €40 Easter-weekend fixed-price taxi overcharges",
        "Keep a crossbody bag in front on the climb from Plaza Nueva to the Alhambra and in Albaicín alleys — r/GoingToSpain '$6500 item stolen in Granada - police unhelpful with airtags' (comments/1hcartm, 2025) and r/Granada 'PSA Alhambra pick-pockets' (comments/1je5jm3, 2025) document 2025 cases at Granada Station and Alhambra queue",
        "Walk two streets uphill from the Cathedral for honest free-tapas bars — r/Granada 'Beware of Sabor Alhambra' (comments/1dmlkg6) names one trap, and r/TravelHacks (comments/16d9fh5) confirms Calle Calderería Vieja and Plaza Larga serve genuine €2–€3 caña + free tapa culture",
        "Book flamenco only at community-respected cave venues — Cueva de la Rocío (cuevalarocio.es), La Chumbera, Venta el Gallo — never from a street tout; r/GoingToSpain '4 day trip to Granada' (comments/1saj3et, 2025) flags Cathedral-area flamenco ticket sellers specifically",
    ],
    "Tenerife": [
        "Avoid Europcar at TFS, Goldcar, Centauro, OK Mobility for rental cars — r/GoingToSpain 'Beware of latest rental car scam in Spain' (comments/1ei4kan, 2025) specifically flags Europcar Tenerife Sur; book Cicar (Canary-Islands-local) or Hertz direct",
        "NEVER accept 'free scratchcards' from street touts in Playa de las Américas, Los Cristianos, or Costa Adeje — r/TenerifeNews 'Tenerife links to monster £28m UK timeshare scam' (comments/1oa9jvn, 2025) documents the elder-targeting fraud network",
        "Book Mount Teide cable car at volcanoteide.com (€45.50 adult) and summit-permit hike at reservasparquesnacionales.es (free, 3+ months ahead) — skip hotel-concierge 'Teide excursion' packages at €80–€150",
        "Wear crossbody bag in front on Playa de las Américas and Veronicas strip — r/Tenerife 'Robbed in Las Americas, real' (comments/1888q1z, 2024) documents armed robberies and persistent pickpocketing",
        "Save Policía Local Arona (+34 922 757 610) and Policía Nacional Tenerife Santa Cruz (Ramón y Cajal 2, +34 922 849 500) — file denuncia within 48 hours for insurance",
    ],
    "Gran Canaria": [
        "Book Cicar (cicar.com) or AutoReisen (autoreisen.com) for rental cars — r/grancanaria 'Car rent online or local?' (comments/1aqmiy8, 2024) is the community-canonical recommendation; avoid Europcar, Goldcar, Centauro, Doyouspain at LPA",
        "NEVER follow an unsolicited 'friendly stranger' to a bar — r/Ratschlag (comments/1nctef6, 2025) documents €100-per-glass 'hostess bar' scams targeting solo male travelers in Playa del Inglés backstreets",
        "For LPA-to-Maspalomas transfer (50 km), use Bolt app or Global bus line 66 (€7, 45 min) — confirm licensed taxi fare €45–€55 before boarding; decline hotel-concierge 'partner' transfers at 2x legitimate rate",
        "NEVER accept 'free scratchcards' in Maspalomas or Playa del Inglés — the £28m UK timeshare elder-fraud network operates on Gran Canaria alongside Tenerife",
        "For accommodation, book only Airbnb/Booking/VRBO with platform-verified payment — r/Scams '[ES] lodiautos.com' (comments/1o90q8p, 2025) documents 2025 fake-website booking fraud; refuse all off-platform WhatsApp payment requests",
    ],
    "Malaga": [
        "From Málaga Airport (AGP), take the Renfe Cercanías C1 train (€2.05, every 20 min, 30 min to centre) between 5 AM and midnight — the overcharge-proof option; r/GoingToSpain 'Late-night arrival at Málaga Airport' (comments/1r83qwu, 2025) warns €50–€80 late-night taxi quotes",
        "At AGP rental desks, AVOID Goldcar, Centauro, OK Mobility, Doyouspain, and budget AVIS/Budget — r/GoingToSpain 'AVIS BUDGET SCAMS IN MALAGA' (comments/1jit8wl, 2025) and r/Malaga 'Car rental at airport' (comments/1fd3h9v, 2024) document repeat damage-claim scams",
        "Book Alcazaba (€3.50, combo €5.50) at malagaturismo.com and Picasso Museum (€9.50) at museopicassomalaga.org — take Sunday afternoon and last-two-hours free-entry windows",
        "Walk away from promoters grabbing arms on Plaza de la Merced or Calle Larios — r/Malaga 'People outside Bars/Nightclubs' (comments/zwvpos) documents tout commission pressure; walk directly to named venues (Pimpi, Casa Aranda, Uvedoble Taberna)",
        "For Airbnb, refuse all off-platform ID-scan requests — r/Malaga 'AirBnB scam? Asking for my ID' (comments/1816csz) documents ID-theft patterns; report suspicious hosts to Airbnb immediately",
    ],
    "Ibiza": [
        "At Ibiza Airport (IBZ), use ONLY the licensed yellow taxi rank immediately outside Arrivals — r/ibiza 'People posing as taxi drivers at Ibiza Airport | WARNING' (comments/1k8xdeo, 2025) documents 2025 unauthorised drivers quoting €60–€120 for €20–€35 rides",
        "Book club tickets directly from official sites (pacha.com, amnesia.es, ushuaiaibiza.com, hiibiza.com, dc10ibiza.com) — r/ibiza 'Rep ticket scam' (comments/14a7oiw) warns about street-rep markups and counterfeit wristbands",
        "NEVER leave a drink unattended in Ibiza nightlife — r/NoStupidQuestions 'Was I spiked' (comments/1h59i1f, 2025) documents a 2025 Ibiza spiking incident; decline 'private villa' or 'after-hours' invitations from strangers",
        "AVOID Mr Rental Ibiza, Okmobility, Doyouspain, Goldcar, Centauro for scooter and car rental — r/ibiza 'Mr Rental Ibiza - my journey with scammers' (comments/1oiesgs, 2025) is a named 2025 anchor; use Hertz, Europcar, or Class Rent a Car",
        "At beach clubs (O Beach, Ushuaïa, Nikki Beach), request minimum-spend contract in writing at seating — r/ibiza 'O Beach what an absolute nightmare' (comments/1eoy7mr, 2025) and 'Ushuaia: don't fall for waiter scam' (comments/1mesjt2, 2025) document waiters adding unordered items",
    ],
    "Palma de Mallorca": [
        "Use licensed yellow taxis at PMI arrivals (queue at Terminal A) — €20–€30 to Palma centre, €25–€35 to cruise port or El Arenal; r/VisitingMallorca 'Airport Taxi' (comments/1kya2nr, 2025) gives the 2025 regulated-rate baseline. Uber does NOT operate in Mallorca — only Cabify and licensed taxis are legitimate",
        "At El Arenal and Magaluf, rent a beachfront locker (€3–€5) for phone and wallet during swims; r/Scams '[ES] iPhone stolen in Mallorca (El Arenal)' (comments/1n3xfrs, 2025) documents 2025 phone theft with phishing follow-ups",
        "Decline cruise-line Palma excursions at €80–€150 per person — a self-guided Cathedral + old-town day costs €30–€50; take the port shuttle or Cabify (€15) to centre",
        "Video-walk-around your rental car at pickup narrating visible marks; decline hotel-recommended rental operators with no independent Google reviews",
        "For apartment rentals, book only via Airbnb or Booking — r/mallorca 'Did we just escape a scam?' (comments/135f61s) documents off-platform payment fraud; check for hidden cameras on arrival per 2025 r/AirBnB reports",
    ],
    "Lanzarote": [
        "At Arrecife Airport (ACE), confirm fare before boarding: €18–€22 Puerto del Carmen, €25–€30 Costa Teguise, €50–€60 Playa Blanca; r/GoingToSpain 'Beware of this taxi scam' (comments/1mk8n4c, 2025) documents 2025 blurry-meter overcharges",
        "For rental cars, use Cicar or Auto Reisen (community-vetted) rather than Goldcar or Centauro — r/lanzarote 'Few questions about Lanzarote' (comments/1hvyvgy, 2025) documents hotel-recommended rental scams",
        "Book Timanfaya Tremesana route 2–3 months ahead at timanfaya.com (€15 adult) — the best-value experience; skip hotel-concierge 'Timanfaya excursion' packages at €45–€80",
        "Watch the pump counter reset to zero before fuel flows; decline 'oil top-up' or 'windscreen wipe' offers — r/lanzarote 'I've been ripped off by a service station' (comments/1b2cgh2, 2025) documents €500 disputes",
        "For post-return speeding-ticket letters from Mallorca rentals, verify via DGT directly (+34 060 or dgt.es) — r/mallorca 'Fake speeding ticket' (comments/1cho5y7) documents the scam with correct personal data from leaked rental records",
    ],
    "Córdoba": [
        "Book Mezquita-Catedral tickets only at mezquita-catedraldecordoba.es (€13 adult) — r/GoingToSpain 'Mezquita-Catedral Ticket' (comments/1pbjemo, 2025) warns clone sites charge €25–€45",
        "At Córdoba AVE station, use Cabify or Bolt for the €6–€9 metered trip to Mezquita — r/BuenosAires 'Cabify without GPS' (comments/1n57saj, 2025) documents 2025 Córdoba fare-manipulation variants",
        "Walk two streets off Calle Cardenal Herrero for honest tapas — Taberna Salinas, Bodegas Campos, Bar Santos (giant tortilla), Casa Mazal are community-recommended",
        "Check parking signs before paying anyone in a vest — Córdoba Judería zones are free Sunday and weekday evenings after 8 PM per r/spain 'Fake parking attendants? Andalucia' (comments/6qkmks)",
        "For May Patios Festival, book tickets only at patios.cordoba.es (€8 per route); visit 10 AM rather than 1–4 PM to avoid peak pickpocket crowds per r/GoingToSpain '2026 Courtyards Festival' (comments/1rmrsoc, 2025)",
    ],
    "Valencia": [
        "Skip Malvarrosa beachfront 'paella restaurants' entirely — book Casa Carmela, La Pepica, or Restaurante La Riua (Ciutat Vella) instead; r/valencia 'Every city has one' (comments/1kn9azh, 2025) names Casa Patacona as a documented tourist trap",
        "Rent a beachfront locker at Malvarrosa chiringuitos (€3–€5) for valuables during swims — r/valencia 'Got robbed at the beach' (comments/1fp6gam, 2025) documents coordinated scarf-seller crews who target empty-handed victims",
        "For Las Fallas (March 15–19), book accommodation 6+ months ahead with full refundability via Airbnb or Booking — r/travel (comments/1rsjbv5, 2025) warns of 3–5x Fallas-week price gouging",
        "Never pay cash to a 'parking attendant' in a vest — Malvarrosa Calle del Doctor Lluch and Calle Pavía are free evenings after 8 PM; use the PARKman Valencia or EysaPay app to verify",
        "For apartment rentals longer than a weekend, book only via Airbnb or Booking.com — r/GoingToSpain 'PSA: Documented rental scam at Avenida de Burjassot' (comments/1s63ana, 2025) is the named 2025 police-investigation anchor",
    ],
    "Bilbao": [
        "From Bilbao Airport (BIO), use Bizkaibus A3247 express (€3, every 15–30 min, 25 min to Plaza Moyua) rather than taxi — r/Bilbao 'Landing in Bilbao at 7:20 PM' (comments/1kotd38, 2025) warns peak-event taxi rates double",
        "For Bilbao-to-San Sebastián transfers, use PESA bus (€7–€12, 80 min from airport or Termibus) — r/Bilbao 'Getting to San Sebastian tomorrow' (comments/1sc3uye, 2025) documents €350 hotel-concierge taxi quotes",
        "At rental-car pickup, video-walk-around the vehicle and narrate visible marks before signing — r/GoingToSpain 'Beware Europcar scratch scam' (comments/1o00jtv, 2025) is the 2025 named anchor for $200 bogus damage claims",
        "Keep crossbody bag zipped and in front during Casco Viejo pintxos crawls — r/Bilbao 'Phone Pick-pocketed in Bilbao' (comments/1lq8q1m, 2025) documents 2025 lifts in narrow streets around San Francisco",
        "Save Ertzaintza Bilbao (Deusto station, Avenida Ramón y Cajal, +34 94 607 0000) — file denuncia within 48 hours for insurance claims",
    ],
    "San Sebastián": [
        "From Bilbao Airport to Donostia, use PESA bus direct (€7–€12, 80 min to Termibus) — r/GoingToSpain 'Travelling to San Sebastian' (comments/1ckms4k, 2025) documents licensed taxi baseline at €120; quotes over €200 are overcharges",
        "Rent a beachfront locker (€3–€5) at Playa de la Concha for valuables during swims — r/Bilbao 'Phone Pick-pocketed in Bilbao' (comments/1lq8q1m, 2025) confirms SS beach theft with year-long recovery delays",
        "Skip Fermín Calbetón and Calle 31 de Agosto's first two blocks for pintxos; walk deeper to Bar Nestor (tortilla), Ganbara (ham/mushroom), Borda Berri, La Cuchara de San Telmo — r/finedining (comments/1mggmsn, 2025) names these as locals-first venues",
        "For accommodation, book only Airbnb or Booking.com with platform-protected payment — r/GoingToSpain 'Looking for a shared room in San Sebastian (Donostia)' (comments/1mr4kul, 2025) documents persistent transfer-before-viewing fraud on Idealista and private listings",
        "Save Policía Municipal Donostia (+34 943 450 000) and Ertzaintza Donostia (Plaza Bizkaia, +34 943 408 800) — file denuncia within 48 hours for insurance claims",
    ],
    "Toledo": [
        "Buy the Pulsera Turística wristband (€12 for 7 monuments) at any participating site on arrival — or book Cathedral only at catedralprimada.es and Alcázar at ejercito.defensa.gob.es; r/GoingToSpain '5 days Madrid - day trip to Toledo & Segovia?' (comments/1rwp9nq, 2025) flags the ticket-overcharge ecosystem",
        "At Toledo Train Station, use Cabify or Uber (€5–€7 to Plaza de Zocodover) — the station taxi rank routinely quotes €10–€15 'fixed prices' per r/GoingToSpain 'Taxi or Cabify in Spain' (comments/1h9m5lm, 2025)",
        "For damascene knives or swords as gifts, visit Mariano Zamorano (Calle Ciudad 19) or Simón Cortés (Paseo de San Cristobal) — r/spain 'Toledo and its Knives!' (comments/4zj2gq) warns the Calle del Comercio tourist shops sell decorative replicas, not genuine forged damascene",
        "Keep crossbody bag in front in narrow Judería alleys and Plaza de Zocodover during 10 AM / 2 PM tour-group transitions — r/askspain 'I'm traveling through Calatayud, Toledo' (comments/1lxwowm, 2025) notes Toledo distraction pickpockets specifically target 'relaxed' day-trippers",
        "Walk two streets off Plaza de Zocodover for lunch — Alfileritos 24, Bar Ludeña, and El Trebol have honest €13–€16 Menú del Día per r/GoingToSpain 'Toledo Day Trip - how to structure day?' (comments/1ch0yss, 2025)",
    ],
    "Naples": [
        "Carry your bag on the building side of the sidewalk and wear it crossbody to defend against scippatori on mopeds; never dangle your phone while walking.",
        "Know the fixed taxi rates before arriving (airport to city center: 16 to 23 euros by zone) and only use licensed taxis from official stands.",
        "Avoid lingering in Piazza Garibaldi outside the train station; walk purposefully to your destination, and do not engage with anyone offering games, petitions, or help with tickets.",
        "Leave luxury watches and visible jewelry at home; Naples' street thieves specifically target high-value visible accessories.",
    ],
    "Cartagena": [
        "Never leave drinks unattended in bars or accept beverages from strangers; scopolamine drugging is a documented threat in Cartagena's nightlife scene.",
        "Agree on taxi fares before getting in the car and keep a list of standard rates on your phone; alternatively, use Uber or InDriver for transparent pricing.",
        "Keep a photocopy of your passport in your hotel and carry it instead of the original; store valuables in the hotel safe with a code only you know.",
        "Stay in well-lit, populated areas after dark and avoid walking alone in Getsemaní or the Walled City side streets late at night; use taxis or ride-hail apps for nighttime transport.",
    ],
    "Chicago": [
        "Keep your phone in a front pocket or zipped crossbody bag, especially on the CTA and along the Magnificent Mile — organized pickpocket teams actively work these areas",
        "Use only official rideshare apps (Uber/Lyft) or taxis from designated stands — never accept rides from anyone who approaches you inside O'Hare or Midway terminals",
        "Stick to well-lit, busy areas in the Loop, River North, and Streeterville after dark — most violent crime in Chicago occurs in neighborhoods far from tourist zones",
        "Report scams or non-emergency incidents by calling 311 or (312) 746-6000 — save these numbers in your phone before arriving",
    ],
    "Boston": [
        "Boston is one of the safest major US cities for tourists — the main risks are petty theft, overcharging, and parking-related scams rather than violent crime",
        "Walk two to three blocks away from the Freedom Trail and Faneuil Hall to find restaurants with local pricing and no hidden surcharges",
        "The MBTA is generally safe but keep valuables secured on crowded Green and Red Line trains — pickpockets target distracted riders during rush hour",
        "If driving, use the official ParkBoston app and ignore any QR code stickers on meters or text messages about unpaid tickets — these are phishing scams",
    ],
    "San Diego": [
        "San Diego is one of the safest large US cities for tourists — the main risks are overcharging scams in the Gaslamp Quarter, pedicab hustles, and phishing schemes rather than violent crime",
        "If crossing into Tijuana, use only official border facilities and do not engage with anyone offering line-cutting, visa help, or 'expedited' crossing services",
        "Buy tickets to the San Diego Zoo, SeaWorld, and LEGOLAND only from official websites or authorized sellers like Costco — never from Craigslist or street vendors",
        "Pay for parking only through official kiosks or apps — ignore any text messages about unpaid parking tickets and QR code stickers on meters",
    ],
    "Guadalajara": [
        "Use Uber or Didi instead of hailing street taxis — both apps work reliably throughout Guadalajara and provide GPS tracking, upfront pricing, and driver identification.",
        "Stay in well-known neighborhoods for tourists such as the Centro Historico, Chapultepec, and Tlaquepaque during the day, and avoid wandering into unfamiliar residential areas after dark.",
        "Withdraw cash only from ATMs inside bank branches (BBVA, Santander, Banorte) and always select Mexican pesos when the machine asks about currency conversion.",
        "Keep your passport in the hotel safe and carry a photocopy plus a photo on your phone — this satisfies most identification requests while protecting your original document.",
    ],
    "Tulum": [
        "Rent a bicycle to get around Tulum — the town is flat and bikeable, and this avoids the taxi mafia's inflated prices entirely while giving you independence.",
        "Under Mexican law, all beaches are public property. No beach club, hotel, or security guard can legally deny you access to the waterline. Walk through confidently if challenged.",
        "Carry your physical driver's license at all times when driving, as police have used the lack of a physical document as a pretext for extortion stops on Kukulkan Avenue.",
        "Book cenotes, tours, and transfers directly through verified online platforms or your hotel rather than accepting offers from people on the street or roadside.",
    ],
    "Playa del Carmen": [
        "Remove or cover your hotel wristband when walking Fifth Avenue — timeshare promoters read the hotel name to fake familiarity and target you for presentations.",
        "Never use any ATM on Fifth Avenue or in a convenience store. Walk to an actual bank branch (BBVA, Santander, Scotiabank) for withdrawals, even if it is a few blocks away.",
        "Eat one or two blocks off Fifth Avenue for genuine local food at 40-60 percent lower prices, and always check your bill for automatically added gratuities before tipping again.",
        "Stick to groups when exploring the 12th Street nightlife area, never leave drinks unattended, and avoid engaging with anyone offering drugs on the street.",
    ],
    "Cozumel": [
        "Photograph the official taxi rate chart at the cruise pier before approaching any driver — this gives you a reference to push back on inflated quotes.",
        "Do not buy jewelry at cruise port shops unless you are prepared to get it independently appraised — counterfeit gemstones and fake silver are pervasive in port shopping areas.",
        "Book all tours and excursions in advance through your cruise line, Viator, or the operator's official website rather than from sellers at the pier or ferry terminal.",
        "Only use pharmacies that serve the local population (Farmacias del Ahorro, Farmacia Guadalajara) rather than tourist-area shops near the cruise pier.",
    ],
    "Oaxaca": [
        "Visit artisan villages directly (Teotitlan del Valle, San Bartolo Coyotepec, San Martin Tilcajete) to buy genuine crafts at fair prices and ensure your money goes directly to the makers.",
        "Exchange money only inside banks or official casas de cambio — never with anyone on the street, regardless of the rate they offer.",
        "Use the Didi app or have your hotel call a taxi for fair pricing. For Monte Alban, take the shared shuttle from Hotel Rivera del Angel to avoid taxi overcharging.",
        "Eat at local fondas and the Mercado 20 de Noviembre for authentic Oaxacan food at honest prices — tourist restaurants around the Zocalo charge significantly more and may add hidden fees.",
    ],
    "Seattle": [
        "Avoid 3rd Avenue between Pike and Pine — use parallel streets like 1st or 2nd Avenue to reach Pike Place Market",
        "Never use tap-to-pay for street donations and never accept items pressed into your hands by strangers",
        "Leave nothing visible in your car, especially near tourist areas — Seattle car prowl rates are extremely high",
        "Use the Seattle Monorail, Link Light Rail, or rideshare apps instead of navigating unfamiliar parking areas",
    ],
    "Nashville": [
        "Always ask drink prices before ordering on Broadway — if they won't tell you, walk out and try the next bar",
        "Never tap your card for parking lot fundraisers or street charity collectors — offer cash or decline entirely",
        "Verify your rideshare driver's name, photo, and license plate in the app before getting into any car after midnight",
        "Buy concert and event tickets only through official platforms — never from individuals outside venues",
    ],
    "Panama City": [
        "Use Uber or InDriver instead of street taxis — always agree on the total fare before getting in any vehicle",
        "Use ATMs only inside bank branches or shopping malls, never standalone machines on the street",
        "Keep your phone in a zippered front pocket in Casco Viejo and never hand it to strangers",
        "If anyone claiming to be police asks to inspect your wallet or cash, refuse and walk toward a busy area",
    ],
    "Bogota": [
        "Never hail taxis on the street — always use Uber, DiDi, or InDriver for tracked rides with verified drivers",
        "Keep your phone in a deep front pocket at all times — never use it visibly on the street or on TransMilenio",
        "Watch your drinks being prepared and never leave them unattended — scopolamine drugging is a real and documented threat",
        "Carry a photocopy of your passport and leave the original in your hotel safe — never hand documents to plainclothes 'police'",
    ],
    "Mauritius": [
        "Mauritius is generally very safe for tourists with a low violent crime rate, but opportunistic scams targeting visitors are common in tourist areas — stay alert in Port Louis, Grand Baie, and beach zones",
        "Official taxis are white with white license plates, a rooftop taxi sign, and yellow stickers on each front door — never get in an unmarked vehicle",
        "Keep original passports in your hotel safe and carry a photocopy — the Tourism Police number is 210 3894 for non-emergency tourist issues",
        "The Mauritius Rupee is the only legal currency — exchange only at banks or authorized bureaux de change, and be cautious of counterfeit notes in larger denominations",
    ],
    "San Salvador": [
        "El Salvador has become dramatically safer under the state of exception, but tourist-targeting crimes like express robbery, phone snatching, and scams persist — always stay alert in public",
        "Use Uber or pre-arranged hotel transport exclusively — never accept rides from unofficial taxi drivers, especially at the airport or after dark",
        "Carry only small USD bills and keep your phone hidden when on the street — motorcycle snatch-and-grab is the most common street crime targeting tourists",
        "POLITUR (tourist police) can be reached at 2511-8302 and provides security at major tourist sites — save this number before arriving",
    ],
    "Montego Bay": [
        "Stick to established tourist areas like the Hip Strip, resort zones, and managed attractions — Montego Bay has a higher crime rate outside these areas, particularly in neighborhoods like Flankers, Glendevon, and Rose Heights",
        "Pre-arrange all transportation through your hotel and always agree on total fares before getting in any taxi — Jamaica has no metered taxis and no reliable rideshare apps",
        "Never buy drugs from street sellers — it is illegal, dangerous, and the seller-and-fake-police extortion scam is well-documented",
        "Book all tours and water sports through your hotel or established platforms with buyer protection — street operators on the Hip Strip are the most common source of tourist scams",
    ],
    "Washington DC": [
        "Stick to well-lit, populated areas around the National Mall, Georgetown, and Dupont Circle; avoid walking alone east of the Capitol or in Southeast DC at night",
        "Use the Metro or official DC taxi services (identified by dome lights and proper licensing) rather than accepting rides from strangers outside Metro stations",
        "All Smithsonian museums and National Mall memorials are completely free; never pay anyone claiming to offer skip-the-line access or reserved entry",
        "Download the official WMATA app for Metro schedules and use SmarTrip cards instead of carrying large amounts of cash for transit",
    ],
    "Antalya": [
        "Use BiTaksi or Marti TAG app for taxis with tracked routes and pre-estimated fares — r/Antalya 'Tourist little scams' confirms 'Always ask to put the meter' is the country-wide rule from AYT airport and in Old Town Kaleici",
        "Photograph menus and prices before ordering at any restaurant on Kaleici alleys or Lara Beach strip; check the bill line-by-line per r/Antalya 'How to know the legit/normal price for stuff?' — 'If a shop doesn't have price tags, it's likely a tourist scam'",
        "Use ATMs inside bank branches (Türkiye İş Bankası, Akbank, Garanti) and enable real-time transaction alerts; never pay cash at bars on Kaleici nightlife strip — 'Let's Have a Drink' scams target solo male travelers",
        "Book Antalya day-trips (Pamukkale, Aspendos, Side, Manavgat) only via vetted operators — r/Antalya 'Few days in Antalya - Best organized 1 day tours' (comments/1l96cn0, 2025) is the named 2025 vetted-operator thread; AVOID hotel-concierge bookings under €30/person which force shopping stops",
        "For carpets, NEVER buy from a shop you were led to by a street tout; pay by credit card for dispute protection per r/orientalrugs 'Help please. Ripped off? Kusadasi - Turkey' (comments/1o7f436, 2025) which documents post-purchase value disputes across the Aegean",
    ],
    "Marmaris": [
        "From Dalaman Airport (DLM), use TUI/Jet2/Tez Tour included transfer or Havaş bus to Marmaris otogar (€8/person, 90 min) — taxi 'fixed price' quotes over €60 are overcharges (legitimate metered ₺1,200–₺1,600)",
        "Book Marmaris boat trips with Bayan Boat Tours or Tradewinds Sailing at €25–€40/person — under €20 means hidden drink charges, mandatory tips, and Hisarönü/İçmeler shopping stops on return per r/AskTurkey 'Travelling to Dalaman, Pamukkale and Marmaris' (comments/1cg6m8l)",
        "Avoid Bar Street venues with no posted prices — r/Alanya 'Be aware of this scam' card-skimming pattern operates equally in Marmaris bar district; pay cash at small bills",
        "For Rhodes day-trip ferries (€60–€85 round-trip), book direct with Yeşil Marmaris (yesilmarmaris.com) — third-party resellers add 30–50% markup and may use unlicensed operators",
        "AVOID 'authentic Turkish bath' resort-strip hammam packages over €70/person — for genuine experience visit Sultan Saray Hamam (Old Town) at €25–€35 with posted prices",
    ],
    "Bodrum": [
        "From Milas-Bodrum Airport (BJV), use Havaş bus to Bodrum otogar (₺250/person, 50 min) — taxi 'fixed price' quotes over €60 are overcharges (legitimate metered ₺1,000–₺1,400)",
        "Bodrum nightclub strip on Cumhuriyet Caddesi has 2024-2025 documented card-skimming and bill-padding — pay cash at bars and refuse 'didn't go through' card retries per the Alanya pattern (r/Alanya 'Be aware of this scam')",
        "For Bodrum yacht/gulet day cruises, book with vetted operators (Bodrum Cruises, Yacht Adriatic) at €30–€50/person — under €20 means shortcuts and hidden charges",
        "AVOID hotel-concierge 'special excursion' packages over €60/person to Pamukkale, Ephesus, or other Aegean destinations — tour-bundle math forces shopping stops; book direct via GetYourGuide with TÜRSAB licensing verified",
        "Bodrum Castle (Underwater Archaeology Museum) entry is ₺200 (~€5) — buy at the official ticket booth or via muze.gov.tr; decline 'skip-the-line' touts at the entrance (this attraction rarely has queues)",
    ],
    "Cappadocia": [
        "Hot-air balloon flights from licensed operators (Royal Balloon, Butterfly Balloons, Voyager Balloons, Turkiye Balloons) cost €180–€280/person — anything under €120 signals an unlicensed operator with skipped maintenance schedules; verify Turkish DGCA SHGM licensing",
        "From Nevşehir/Kayseri Airport, use the Cappadocia Express shuttle (€15/person, included with most balloon bookings) or Havaş bus — taxi quotes over €60 to Goreme/Ürgüp are overcharges (legitimate metered ₺900–₺1,400)",
        "For Goreme Open Air Museum (₺1,000 / ~€25), book via official Müze app at muze.gov.tr — r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) documents the broader Turkish-attraction reseller-scam pattern that applies at Cappadocia entry points",
        "Avoid hotel-concierge 'all-inclusive Cappadocia day' packages under €40/person — the math forces 60-90 minute stops at onyx workshops, carpet 'cooperatives,' or pottery demonstrations; demand 'no shopping stops' in writing",
        "For ATV/horseback/quad tours in Goreme, book with named vetted operators (Mehmet Cappadocia, Ürgüp Horse Riding) at €40–€60/person — accept-no-substitutes booking; never pay touts at the trail head who claim to represent the same operator",
    ],
    "Kusadasi": [
        "Never buy 'ancient coins' or 'antiquities' from any vendor in Kuşadası or at Ephesus — r/Cruise 'Avoid the Ancient Coin scam' (comments/1qvm7tz, 2025) documents the mass-produced-fake operation; export of genuine antiquities is also a Turkish criminal offence",
        "Use BiTaksi app for all taxi trips — r/kusadasi 'Scammed by this taxi driver' (comments/1m2wfds, 2025) documents a ₺1,400 overcharge for what should be a ₺200 port-to-hotel trip; Uber does NOT operate in Kuşadası",
        "When booking shore excursions, request 'no shopping stops, no carpet demonstration' in writing — r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024) documents the corral-into-back-room mechanic that operates on most cruise-line and unvetted private tours",
        "For Ephesus, use Ephesus Shuttle (ephesusshuttle.com) — community-vetted operator with port-time guarantee and no-shopping policy in writing; cruise-line tours cost 2x with the same itinerary plus a forced carpet stop",
        "Walk one block off Barbaros Caddesi for honest tapas — Ferah Restaurant (Atatürk Bulvarı), Avlu (Cephane Sokak), Café Karavan (Old Town); decline complimentary bread/olives unless prices are confirmed",
    ],
    "Ephesus": [
        "Book Ephesus tickets only at the gate (cash) or via the official Müze app at muze.gov.tr — official rate is ₺700 (~€18) for the main site; clone-site resellers charge €35–€60 with no actual benefit",
        "If booking a guided tour, request 'no carpet stops, no silk demonstrations, no cultural cooperatives' in writing — r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024) and r/orientalrugs 'Help please. Ripped off? Kusadasi' (comments/1o7f436, 2025) document the corral-into-room sales mechanic",
        "Never buy 'Roman coins' or 'antiquities' from on-site vendors — r/Cruise 'Avoid the Ancient Coin scam' (comments/1qvm7tz, 2025) is the canonical PSA; for genuine replicas, buy at Ephesus Museum (Selçuk) with provenance papers",
        "From Selçuk to Ephesus, use the dolmuş from Selçuk otogar (₺25 per person, every 30 min, 8 AM–6 PM) — taxis quote 'fixed price' over ₺500 for what should be ₺200–₺300 on the meter",
        "For Catholic pilgrim visits to House of the Virgin Mary, use Ephesus Shuttle combined tour or Cosmos Catholic Tours — avoid generic 'Ephesus + Mary + cultural stop' bundles which are carpet-shop code",
    ],
    "Pamukkale": [
        "Book Pamukkale + Hierapolis tickets in advance via official Müze app at muze.gov.tr (₺1,200 / ~€30) — bypasses the north-gate ticket booth bundling scam documented in r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025)",
        "Decline ALL audio-guide rentals at the gate — r/Turkey 'Headphone scam Pamukkale' (comments/1fjcgk3, 2024) documents bait-and-switch pricing; use GPSmyCity Pamukkale app (€3.99) for self-guided audio",
        "From Denizli otogar, take the public dolmuş to Pamukkale (₺25, every 15–30 min) — taxi 'fixed prices' run ₺800–₺1,500 for a 17-km trip that should be ₺250–₺350 metered",
        "AVOID day-trip tours under €30/person from Antalya/Bodrum/Marmaris — the math forces 2–3 'cooperative' shopping stops; r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) documents the broader pattern",
        "For hot-air balloons, book Pamukkale Balloons (pamukkaleballoons.com), Sky Pamukkale, or Royal Balloon at €120–€180/person — anything under €100 signals unlicensed operator (DGCA SHGM compliance matters for safety)",
    ],
    "Fethiye": [
        "DO NOT enter Turkish Delight, tea, or spice shops in Old Town tourist strips — r/travel 'My experience in Türkiye: beware of vendors' (comments/1n2jk3z, 2025) documents an actual physical assault in a Fethiye Old Town lokum shop",
        "Book Ölüdeniz tandem paragliding only with Sky Sports Turkey, Reaction Paragliding, Easy Riders, or Babadağ Paragliding at €110–€160/person — r/freeflight 'WARNING: Potential scam company in Oludeniz' (comments/1ookhl3, 2025) flags unlicensed operators with safety-variance issues",
        "Book 12 Islands boat tours with Bayan Boat Tours, Tradewinds Sailing, or V-Go Yachting at €25–€40/person — under €20 means hidden drink charges, mandatory tips, and Hisarönü shopping stops",
        "From Dalaman Airport (DLM), use TUI/Jet2/easyJet included transfer or Welcome Pickups (€30–€40 per car for 4) — taxi quotes over €50 to Fethiye are overcharges (legitimate metered fare is €23–€30)",
        "For genuine Turkish hammam, take the bus to Fethiye centre (Eski Kapı Hamamı €20–€30, Sultan Hamam €25–€40) — skip Hisarönü resort-strip 'authentic Turkish bath' packages at €80–€150 with mandatory product upsells",
    ],
    "Alanya": [
        "NEVER follow an unsolicited 'friendly local' to any bar — r/Alanya 'Be aware of this scam' documents a card-skimming pattern where charges of €800–€2,500 land within hours; pay cash for drinks at small bills",
        "From AYT (Antalya Airport, 130 km), use TUI/Jet2/Tez Tour included transfer or Havaş bus (₺250, 2.5 hr) — taxi 'fixed prices' over €100 are overcharges (legitimate metered ₺2,000–₺2,500)",
        "Cleopatra Beach taxi from Alanya centre: ₺140–₺200 metered (€3.50–€5), NOT €15–€20 'fixed price' per r/Alanya 'Just got back from alanya' community baseline",
        "Avoid hotel-concierge excursions over €60/person — book Manavgat/Side/Aspendos via GetYourGuide or Viator with 'no shopping stops' filter and TÜRSAB licensing verified",
        "Damlataş Cave (₺120), Alanya Castle (₺240), Red Tower (₺120) — all walk-up at official prices; decline 'skip-the-line' offers from touts (these attractions rarely have queues)",
    ],
    "Izmir": [
        "From ADB (Adnan Menderes Airport), use Izban suburban train to Alsancak (₺25, 30 min) — cheapest scam-free option; install Marti TAG and BiTaksi for app-regulated taxi fares",
        "Refuse Çeşme/Alaçatı transfer quotes over €120 round-trip; legitimate Havaş bus is €10/person 70 min, taxi €100–€140 round-trip per r/Izmir 'Alaçatı tatili, kiralık araba mı, taxi mi?'",
        "AVOID Kemeraltı Bazaar carpet/jewelry shops without prior vetting — r/Turkey 'Turkey trip report February 2025: Multiple scams' (comments/1ixwq20, 2025) documents a $250 victim; for gold visit Konak Kuyumcular Çarşısı with spot-rate prices",
        "On Alsancak nightlife strip, NEVER follow unsolicited 'friendly local' to a bar — same card-skimming pattern as Alanya documented in r/Alanya 'Be aware of this scam'; pay cash at small bills",
        "For long-stay apartment rentals, book only Airbnb/Booking/VRBO with platform-verified payment — r/Izmir 'About buying a house' and 'A guy from İzmir is committing fraud worldwide' document the persistent fake-listing fraud ecosystem",
    ],
    "Konya": [
        "The genuine Sema (Whirling Dervish) ceremony is FREE every Saturday 7 PM at Mevlana Kültür Merkezi — arrive 6 PM for seating, dress modestly; r/istanbul 'Is Dervish whirling show worth it?' confirms commercial Cappadocia/Istanbul 'shows' are not the real ritual",
        "Mevlana Museum entry is FREE — decline ALL photographer touts at the entrance and buy memorabilia at official museum gift shop with marked prices (rosary €4–€8) per r/AskTurkey 'Konya - the hidden gem of Turkey'",
        "Refuse 'KDV ek' (extra VAT) on restaurant bills — Turkish KDV is LEGALLY INCLUDED in menu prices per r/istanbul 'Did I get scammed?'; community-recommended Konya: Mehmet Konyalı (etli ekmek), Şifa Lokantası, Konya Mutfağı",
        "From Konya YHT station, use BiTaksi (₺250–₺350) or tram (₺25) — r/AskTurkey 'How to go from Selçuklu YHT station to Konya' is the canonical community guide",
        "AVOID Cappadocia hotel-concierge 'Konya day-trip' packages under €60/person — math forces shopping stops; for Saturday Sema, take Pamukkale Turizm bus (₺350 each way, 9 hr) and overnight in Konya",
    ],
    "Side": [
        "Apollo Temple ruins are FREE — walk the peninsula via the pedestrianized main street; decline 'professional photographer' offers (€15–€25 demanded after the shot)",
        "NEVER buy 'archaeological fragments,' 'authentic ancient stones,' or 'Roman coins' — fake (worthless) or genuine (Turkish criminal-export issue under Law 2863)",
        "For Manavgat Waterfall + boat tour, book via GetYourGuide or Viator at €20–€30/person — under €15 means the day spends 2+ hours at Manavgat Bazaar shopping stops",
        "Avoid Liman Caddesi seafront restaurants with English-only photo menus; community-recommended: Side Garden Restaurant, Lale Restaurant, Şinasi Köşkü (one block back)",
        "For Aspendos + Perge combo day tour, use GetYourGuide/Viator with TÜRSAB licensing at €40–€60/person — under €25 forces shopping stops; 7+ hours of attraction content is the minimum legitimate duration",
    ],
    "Hurghada": [
        "Stay within resort areas and the well-patrolled Hurghada Marina for evening entertainment; avoid walking alone in El Dahar old town after dark",
        "Always agree on prices before any transaction including taxi rides, camel rides, tours, and restaurant orders; get agreements in writing when possible",
        "Purchase your Egyptian visa at the official bank counter inside the airport for exactly $25 and ignore anyone offering to help in the arrivals hall",
        "Carry small bills in Egyptian pounds for daily transactions and keep larger amounts in a hotel safe; avoid displaying large amounts of cash in shops or markets",
    ],
    "Portland": [
        "Avoid the Old Town/Chinatown district after dark and exercise caution in the Burnside corridor; stick to well-populated neighborhoods like the Pearl District, Hawthorne, Alberta, and Division Street",
        "Never leave anything visible in your parked car, especially at trailheads and downtown parking areas; Portland's car break-in rates are significantly above the national average",
        "Use TriMet MAX light rail and buses to reach most tourist areas, reducing the need for parking and car break-in exposure; purchase a day pass for $5",
        "Portland's food cart culture is generally safe and authentic, but stick to established pods with posted health inspection certificates and pay with a credit card when possible",
    ],
    "Abu Dhabi": [
        "Abu Dhabi is one of the safest cities in the world for violent crime, but property scams and overcharging remain real risks for tourists; stay alert in commercial and tourism contexts",
        "Use only official Abu Dhabi taxis (silver with TransAD logo) or ride-hailing apps like Careem and Uber; never accept rides from unlicensed drivers at the airport or attractions",
        "Respect local customs and laws: public displays of affection, loud behavior, and immodest dress can result in fines; alcohol is only legal in licensed venues, and being drunk in public is a criminal offense",
        "Download the AD Police App and Darb (Mawaqif parking) app before arrival; these official tools help with reporting incidents and managing parking payments legitimately",
    ],
    "Denver": [
        "Stay on the 16th Street Mall during daylight hours and avoid wandering east of Broadway on Colfax Avenue at night",
        "Use rideshare apps instead of hailing random cabs, and always verify the driver's identity in the app before getting in",
        "Never leave any valuables visible in your rental car, especially at trailheads and airport parking — Colorado has one of the highest vehicle break-in rates in the US",
        "Denver's altitude (5,280 feet) amplifies the effects of alcohol and cannabis — pace yourself and stay hydrated to keep your awareness sharp",
    ],
    "Grand Cayman": [
        "Grand Cayman is one of the safest Caribbean islands but petty crime targeting tourists occurs near the cruise port and at Seven Mile Beach — keep valuables secure",
        "Always confirm whether prices are in KYD or USD and request to be charged in KYD on credit card transactions to avoid unfavorable conversion markups",
        "Book water sports and excursions through licensed operators with physical offices at marinas — avoid beach vendors and too-good-to-be-true online deals",
        "The public bus system is cheap ($2.50 per ride) and efficient along the West Bay Road — use it instead of overpriced port taxis",
    ],
    "Toronto": [
        "Toronto is very safe overall, but stay alert for pickpockets in crowded areas like Yonge-Dundas Square, Eaton Centre, and on the TTC during rush hour",
        "Use Uber or Lyft instead of street-hail taxis at night to avoid the documented taxi card-swap fraud ring that stole over $500,000 from passengers",
        "Apply for your Canada eTA only at the official government website (canada.ca/eta) for $7 CAD — any other site is a third-party markup",
        "Keep your phone and wallet in front pockets, especially in the Entertainment District and at major tourist attractions",
    ],
    "Fiji": [
        "Fiji is generally very safe, but stay alert in Nadi Town and Suva city centre where petty crime and tourist-targeted scams are most common",
        "Use only taxis with yellow 'LT' license plates and always insist the meter is running — unregistered vehicles are unsafe and prone to overcharging",
        "Book all boat excursions and island-hopping tours through operators with a physical office at Port Denarau Marina and Tourism Fiji accreditation",
        "Politely decline invitations from friendly strangers on Nadi Main Street — the 'Where are you from?' opener is almost always the start of a shopping scam",
    ],
    "Quebec City": [
        "Avoid Rue Saint-Louis tourist-strip restaurants and the Petit Champlain shopping arcade for sit-down meals — r/quebeccity 'don't want to fall into the trap!' (comments/1dii1iw, 2024) names La Bûche specifically; walk to Saint-Roch (Le Clocher Penché, Buffet de l'Antiquaire) for honest pricing",
        "YQB airport-to-Old-Town flat fare is regulated at $36.40 day / $42 night — refuse quotes above; pre-book Taxi Coop Québec (+1-418-525-5191) for early/late flights per r/quebeccity (comments/13fvoh3, 2024)",
        "For maple syrup, buy at Provigo/Metro/IGA grocery at $8–$12 per 250 ml — Old Town tourist shops charge $25–$45 for the identical product per r/montreal 'Hot take: sugar shacks are a scam' (comments/1s07i9k, 2025)",
        "Calèche carriage tours: $100–$130 for 35 min, $160–$200 for 1 hr — book ONLY at official Place d'Armes stand with posted rates; refuse 'special' quotes over $150 for the standard loop",
        "Skip cruise-line shore excursions to Montmorency Falls — take RTC bus 800 ($3.75) or metered taxi ($30–$40); confirm 'no shopping stops' in writing for any small-group tour",
    ],
    "Victoria": [
        "Book BC Ferries ONLY at bcferries.com — r/VictoriaBC 'Do not purchase BC Ferries Experience Cards' warns the Facebook Marketplace prepaid-card market is fraud; reserve sailings 2 weeks ahead in summer ($25 fee guarantees your spot)",
        "For whale watching, book vetted operators (Prince of Whales, Eagle Wing Tours, BC Whale Tours, Orca Spirit Adventures) at $130–$180/person — refuse 'whale watching specials' under $100 (no qualified marine biologist + likely Marine Mammal Regulations violations)",
        "Butchart Gardens admission is $40 adult direct at butchartgardens.com — refuse cruise-line 'Butchart shore excursion' at $129–$179 per person; BC Transit route 75 ($2.50) or CVS Tours shuttle ($20 round-trip including admission) is the legitimate route",
        "NEVER accept rides from strangers on Vancouver Island — r/VictoriaBC 'Possible Scam + Safety Warning in Langford' is a documented trafficking warning; use Victoria Taxi (+1-250-383-7111), Uber, or Lyft only",
        "YYJ-to-downtown taxi is $60–$75 metered — refuse 'fixed price' over $80; pre-book Victoria Taxi for early/late flights, especially for late-night arrivals where supply is limited",
    ],
    "Halifax": [
        "Halifax Stanfield (YHZ) airport-to-downtown taxi is regulated FLAT $73 — refuse any quote above; if Uber driver asks you to cancel and pay cash (r/halifax 'Uber at YHZ' documented anchor), exit and request another driver",
        "For Peggy's Cove, skip cruise-line 'Halifax + Peggy's Cove' bundles at $199–$299/person — independent rental car or Welcome Pickups private driver ($150–$250 round-trip for 4) is half the cost; Casino Taxi (+1-902-429-6666) for $120–$160 round-trip",
        "Citadel Hill is FREE June 1 to September 1 every year (otherwise $13.50 adult); Maritime Museum of the Atlantic is $13.50 adult — decline ALL 'skip-the-line' tout offers",
        "Avoid Lower Water Street and Cable Wharf restaurants for sit-down meals — walk 5–10 min inland to The Wooden Monkey (Argyle), Heartwood Vegan (Quinpool), Battery Park (Halifax craft brewery); for cheap lobster, drive to Eastern Passage Fisherman's Cove",
        "For accommodation longer than a hotel weekend, book ONLY via Airbnb/Vrbo/Booking — r/halifax 'What are the odds this is a scam? Fully furnished 2 bed' confirms persistent Facebook Marketplace and Kijiji rental fraud; verify HRM short-term-rental registration number",
    ],
    "Jasper": [
        "AVOID Pursuit Collection combo passes (Jasper SkyTram + Maligne Lake Cruise + Columbia Icefield) — r/jasper 'PSA: Pursuit is an American company' (comments/1inuhkf, 2025) flags the monopoly; use SunDog Tours (Canadian-owned) or self-drive",
        "Maligne Lake Cruise to Spirit Island is the ONLY way to reach the famous viewpoint ($112 direct at malignelake.com) — refuse $200+ 'day-tour' bundles and 'private boat' offers (which are illegal)",
        "From YEG Edmonton (4 hr) or YYC Calgary (5 hr) airports, use round-trip rental for cheapest rate — refuse one-way drop fees over $200; SunDog Tours through-tickets $130–$180/person are the no-car alternative",
        "Carry bear spray ($45 at any Jasper outdoor shop) when hiking — wildlife encounters are real; for self-drive wildlife viewing, drive Highway 16 east at dawn/dusk for FREE bear, elk, bighorn sightings",
        "After the 2024 wildfire, beware accommodation rental fraud on Facebook Marketplace and Kijiji — book ONLY via Airbnb/Vrbo/Booking; donate to wildfire recovery ONLY through Red Cross Canada or Jasper Community Team Society",
    ],
    "Whistler": [
        "NEVER scan QR codes on parking meters — r/Whistler 'It's not legitimate: 24 fraudulent parking QR codes found in' is the named CBC-documented 2024 anchor; use PayByPhone app (downloaded from official App Store) with manually-entered lot codes",
        "Book accommodation ONLY via Airbnb/Vrbo/Booking.com — r/Whistler 'Craigslist scams' and 'DO NOT RENT FROM HERE' document Mountaincountry-style fake-agency fraud; verify Whistler Tourist Accommodation license number AND address match",
        "Buy lift tickets ONLY at whistlerblackcomb.com or via official Vail Resorts Epic Pass — r/Whistler 'Discount Lift tickets scam?' confirms third-party 'discount' tickets are universally fraud; senior discount (65+) is $193/day at the window",
        "Check restaurant bills line-by-line — r/Whistler 'Subtle not so subtle scamming at Whistler restaurants' documents servers adding extra rounds and side dishes; honest-priced venues: Bearfoot Bistro, Caramba Restaurante, Sushi Village, Pasta Lupino",
        "From YVR Vancouver, use Pacific Coach ($60), Epic Rides ($45), or Whistler Connection ($55) shuttle — refuse hotel-concierge 'private transfer' over $200; Sea-to-Sky Highway requires winter tires Oct–Apr per BC law",
    ],
    "Banff": [
        "AVOID Pursuit Collection combo passes — r/Banff 'Pursuit is an American company' (comments/1j3kre8, 2025) flags the monopoly; use Canadian-owned operators (White Mountain Adventures, Discover Banff Tours) and skip the Glacier Skywalk add-on (5-min photo-op for $30)",
        "Book Moraine Lake / Lake Louise shuttles ONLY at reservations.pc.gc.ca ($8 round-trip) — r/Banff 'Shuttle Reservation' (comments/1sm76ci, 2025) documents 27,000-person queues; decline third-party 'guaranteed shuttle' offers over $30/person",
        "From YYC Calgary Airport, use Brewster Express or Banff Airporter ($60–$80/person) — refuse third-party 'private transfer' over $120; On-It Regional Transit ($10/person, weekends) is the budget option",
        "For accommodation, book ONLY via Airbnb/Vrbo/Booking.com — r/Banff 'Banff rental scams' (comments/1g0vd2m, 2025) documents persistent Facebook Marketplace and Kijiji deposit fraud; verify Banff Town short-term rental license number",
        "For honest-priced meals, drive 25 min to Canmore (Communitea Café, Crazyweed Kitchen, Iron Goat) — Banff Avenue restaurants charge $35–$55 entrées for $20–$30 Calgary-equivalent food per r/Banff 'Is it worth it?' (comments/179x003)",
    ],
    "Casablanca": [
        "Learn a few phrases in French and Darija (Moroccan Arabic) — 'la shukran' (no thank you) and 'le compteur s'il vous plaît' (the meter please) are essential for declining scammers and getting fair taxi fares",
        "Use ride-hailing apps like Careem or InDrive in Casablanca for transparent, GPS-tracked fares instead of negotiating with street taxis",
        "Dress modestly and avoid displaying expensive jewelry or electronics, especially in the medina and market areas, to reduce unwanted attention",
        "Keep a photocopy of your passport in your hotel safe and carry only a photo on your phone — the tourist police number is 177 for any incidents",
    ],
    "Belfast": [
        "Belfast is one of the safest cities in the UK for tourists — violent crime against visitors is extremely rare and most scams are opportunistic petty theft rather than organized fraud",
        "Avoid discussing politics, religion, or 'the Troubles' with strangers, especially after dark in pub settings — Northern Ireland's history means these topics can provoke strong reactions",
        "The PSNI non-emergency number is 101 and the emergency number is 999 — officers are generally helpful and approachable toward tourists",
        "Book licensed taxis through fonaCab or Value Cabs apps, and always use established booking platforms for accommodation rather than Facebook Marketplace or classified ads",
    ],
    "Doha": [
        "Qatar is one of the safest countries in the world for violent crime — the main risks for tourists are financial scams like taxi overcharging, counterfeit goods, and phishing rather than physical danger",
        "Respect local customs: dress modestly (shoulders and knees covered in public areas), avoid public displays of affection, and do not photograph people without permission — violating these norms can lead to fines or legal trouble",
        "Use the Doha Metro for cheap, efficient, and scam-free transportation between the airport, West Bay, Souq Waqif, and other major areas — single rides cost just 2 QAR",
        "Download the Metrash2 app for official government services, reporting incidents, and verifying official communications — any government notice that doesn't come through this app is likely a scam",
    ],
    "Seychelles": [
        "Seychelles is one of the safest destinations in Africa — violent crime against tourists is extremely rare, and most risks involve petty theft and tourist price inflation rather than scams or physical danger",
        "Rent a car for the best value and flexibility — public buses on Mahé cost just 7 SCR per ride, and taxis are the most expensive (and least regulated) transport option",
        "Always pay in Seychellois Rupees rather than euros or dollars — paying in foreign currency triggers unfavorable conversion rates that cost you 5-15% more",
        "Book all excursions and accommodations through licensed operators or established platforms with buyer protection — never pay cash deposits to beach vendors for boat trips",
    ],
    "Lagos": [
        "Pre-arrange all transportation through your hotel, a trusted contact, or ride-hailing apps (Uber, Bolt) — never flag down unmarked vehicles or board random danfos, especially to avoid the deadly 'One Chance' robbery",
        "Keep a low profile: avoid wearing expensive jewelry or watches, carrying visible electronics, or displaying large amounts of cash — visible wealth attracts criminal attention in Lagos",
        "Travel during daylight hours whenever possible and avoid walking alone at night, even in upscale neighborhoods like Victoria Island and Lekki",
        "Keep your embassy's emergency number saved in your phone and carry certified copies of your passport — leave the original in your hotel safe with other valuables",
    ],
    "Quito": [
        "Quito has made significant safety improvements — all official taxis now have security cameras and panic buttons, and crime against tourists dropped 40% in the first half of 2024 — but street crime remains a daily reality in the Centro Histórico and La Mariscal",
        "Never hail taxis from the street — use inDriver, Cabify, or have your hotel call a registered company. Official taxis have orange plates or white plates with an orange stripe and security cameras with intact white tape",
        "La Mariscal (Plaza Foch area) is vibrant but requires caution at night — stay on main, well-lit streets, travel in groups, and never accept drinks from strangers due to the scopolamine risk",
        "Leave your passport and extra valuables in your hotel safe. Carry a photocopy of your passport, only the cash you need for the day, and keep your phone in a zippered front pocket — never use it visibly on the street",
    ],
    "Tel Aviv": [
        "Tel Aviv is one of the safest major cities in the Middle East for tourists — street crime is mostly non-violent and consists of taxi scams, beach theft, and market overcharging rather than muggings or violent robbery",
        "Always insist on the meter ('Moneh') in taxis or use the Gett app — from Ben Gurion Airport, the fixed fare to central Tel Aviv should be 170-200 NIS. Note the driver's ID number displayed in the cab",
        "Beach theft is the most common property crime — use waterproof pouches for phone and cash, and never leave valuables unattended on the sand while swimming",
        "Scams in Tel Aviv are primarily financial rather than dangerous — overcharging, hard-sell pressure, and rental fraud are the main risks. Using reputable booking platforms and confirming prices in advance prevents most issues",
    ],
    "Bratislava": [
        "Bratislava is one of the safest capital cities in Europe — violent crime against tourists is extremely rare, but taxi scams, bar scams, and pickpocketing are real risks in the tourist center",
        "Never take a street taxi from the train station or airport — always use Bolt, Uber, or the local Hopin app. A ride from the station to the Old Town should cost €5-9, not €30-50",
        "Be extremely cautious if strangers (especially attractive women) approach you on the street and suggest going to a specific bar — the 'pretty woman' drink scam is Bratislava's most notorious tourist trap",
        "Always validate your tram or bus ticket immediately after boarding by stamping it in the small yellow machine — unvalidated tickets result in fines of up to €80 from inspectors who specifically target tourists",
    ],
    "Beirut": [
        "Beirut is generally safe for tourists within the main urban areas — Hamra, Gemmayzeh, Mar Mikhael, Downtown, and Raouché — but always check current travel advisories due to the evolving security situation in Lebanon",
        "Taxis in Beirut do not use meters — always agree on a price before getting in the car or use Bolt/Uber for transparent pricing. Airport to Hamra should cost $10-15, not $40-70",
        "Since 2024, the official bank exchange rate matches the street rate — there is no longer any advantage to exchanging money on the street. Use bank ATMs and licensed exchange offices only",
        "Beirut's nightlife in Gemmayzeh and Mar Mikhael is legendary but keep your guard up — stick to well-reviewed venues, watch your drinks, and use ride-hailing apps to get home safely",
    ],
    "Austin": [
        "Austin is a generally safe city for tourists, but Dirty Sixth Street (East 6th between Congress and I-35) requires serious caution late at night — fights, aggressive panhandling, and fake rideshare drivers are common after midnight",
        "Never scan QR codes on parking meters in Austin — the city does not use QR codes for parking. Use the Park ATX app, coins, or insert your card directly into the pay station",
        "During SXSW, ACL, and F1 weekends, scammers are especially active — buy tickets only from official sources, verify vacation rentals through major platforms, and watch for fake parking attendants in downtown lots",
        "Use Uber and Lyft for late-night transportation, but always verify the driver's name, photo, and license plate in the app before getting in. Never get into an unmarked vehicle, even if you are tired of waiting",
    ],
    "New Orleans": [
        "Regulate your alcohol on Bourbon Street — intoxicated tourists are the #1 target for pickpockets and scammers, and open container laws make it easy to drink more than you realize while walking between bars",
        "Take Uber or Lyft after dark rather than walking — stick to well-lit main streets like Bourbon, Royal, and Decatur, and travel in groups of three or more",
        "Dress down and blend in — visible Mardi Gras beads, tourist T-shirts, and fanny packs mark you as a visitor and make you a magnet for every hustler in the Quarter",
        "Never accept a bet from a stranger on the street — whether it's about your shoes, your name, or anything else, the answer is always a wordplay trick designed to take your money",
    ],
    "Jakarta": [
        "From Soekarno-Hatta Airport (CGK), ignore EVERY 'taxi sir' approach inside the terminal — all official pickup is outdoors. Book Grab/Gojek on airport Wi-Fi OR use metered Blue Bird (bright blue, 'Blue Bird Group' text) — r/indonesia 'Scammed 1500k idr for Airport to City in Jakarta' (comments/yigy0u) documents 4–8x overcharge",
        "Verify the REAL Blue Bird taxi: bluebird-silhouette logo + 'BLUE BIRD GROUP' text + driver ID on dashboard + flag-drop 6,500–7,500 IDR — r/jakarta 'Appreciation post for Jakarta' (comments/1gsifye, 2024) is the community verification guide; impersonators with near-identical blue paint are common",
        "Pay ONLY in-app via GrabPay or GoPay (linked credit card, auto IDR conversion) — NEVER cash; refuse any driver requesting cancellation or saying 'app broken' per r/indonesia 'Grab driver tried negotiating a different fare?' (comments/c6k0cv)",
        "Use ONLY bank-branch ATMs during business hours (BCA, Mandiri, BNI, BRI, CIMB) — never freestanding mall or convenience-store ATMs — r/indonesia 'Ilegal thing in Indonesia that foreigns doesn't know' (comments/16kpfcg) documents Jakarta ATM-skimming as pervasive",
        "For solo male travellers using dating apps, YOU pick the venue — r/indonesia 'My one terrible night in Indonesia' (comments/243ly1) documents Blok M/Kemang honeypot-bar extortion at Rp 15M–40M; use reputable bars (Kilo Lounge, Awan, Cork & Screw) with posted menu prices"
    ],
    "Yogyakarta": [
        "IGNORE every 'batik exhibition today only' or 'government art show' approach on Malioboro — r/indonesia 'How we got scammed in Yogyakarta today' (comments/1m4ju1g, 2025) is the named 2025 anchor; this is Yogya's #1 tourist scam",
        "Refuse EVERY becak 'Yogya tour 20,000 rupiah 2 hours all places' offer — r/travel 'So many scams in Yogyakarta' (comments/1q7dzfj, 2025) documents the commission-kickback pattern; walk Malioboro on foot",
        "Book Borobudur sunrise ONLY via manoharaborobudur.com (Rp 600K–800K direct) — reject all Rp 1.5M+ 'skip-the-line' sites; daytime entry Rp 455K buys you upper-terrace stupa access (no tips needed)",
        "For Yogyakarta International Airport (YIA, Kulon Progo), book Grab yourself (Rp 250K–350K to city) or use DAMRI shuttle bus (Rp 75K) — IGNORE arrivals 'premium taxi' quoting Rp 500K+ per r/indonesia 'Visiting Yogyakarta in late April' (comments/1shrjdb, 2025)",
        "For Merapi lava-jeep tours, book direct at Kaliurang at Rp 450K–650K PER JEEP (4 people) — refuse hotel 'Rp 1.2M per person' quotes and 'VIP route' upsells per r/travel 'So many scams in Yogyakarta' (comments/1q7dzfj, 2025)"
    ],
    "Lombok": [
        "From Lombok Praya Airport (LOP), book Grab/Gojek yourself — typical fare Rp 200K–300K to Kuta-Lombok (45–60 min); IGNORE arrivals kiosks and sign-holders quoting Rp 500K–1M per r/Lombok 'Intro to Kuta, Lombok: What to expect' (comments/1q921cy, 2025)",
        "For Bali-Lombok fast-boat tickets, book ONLY via 12go Asia, Klook, or operator direct (Gili Getaway, Blue Water Express, Eka Jaya) — AVOID Semaya One and Manta Express per r/bali 'Do NOT book Semaya One fast boat if you want to live' (comments/16e1lgw)",
        "For Mount Rinjani treks, use ONLY licensed operators (Rudy Trekker, John's Adventures, Rinjani Trekking Club) at Rp 2.5M–5M with porter-load ≤25 kg — refuse Rp 1.8M 'specials' per r/travel 'Indonesia Mt Rinjani hike' (comments/1ewqhi0, 2024)",
        "For Kuta-Lombok scooter rentals, SKIP and hire a driver instead (Rp 500K–700K/day via hotel); or if renting, document every scratch on video and keep the key — r/travel 'Lombok, Indonesia getting around' (comments/1q25n3t, 2025) documents pre-damage + spare-key theft",
        "At Padang Bai port, exit Grab 300–500m BEFORE the port entrance and walk in — r/bali 'What is this Padang Bai grab scam?' (comments/1m74w1b, 2025) is the named 2025 anchor for the taxi-mafia Grab blockade"
    ],
    "Gili Islands": [
        "Book Gili fast-boat tickets ONLY via 12go Asia, Klook, or operator direct (Gili Getaway, Blue Water Express) — r/bali 'WARNING MANTA EXPRESS TO/FROM GILI ISLANDS' (comments/1bdrlbz) warns against cheap operators with safety complaints",
        "At jetty arrival, DO NOT let any porter grab your luggage until you see your pre-booked hotel's sign with your name; if using a porter, agree Rp 30K–50K per bag BEFORE transfer",
        "For snorkelling tours, book via hotel or Blue Marlin / Go Gili Trawangan at Rp 150K–250K per person group tour — REFUSE 'National Park fee Rp 100K per person' at turtle reef (fake fee)",
        "AVOID 'magic mushroom shakes' entirely — Indonesia's drug laws carry severe penalties and dosing is unregulated; at Blue Marlin/Rudy's parties, order ONLY sealed bottles watched opened per r/indonesia 'So, how serious is drugs in Indonesia?' (comments/2ugvea)",
        "For cidomo (horse cart) transfers, agree price BEFORE boarding (Rp 50K–100K for 5–10 min is fair) — r/bali 'Gili T: Best stays and Must-dos?' (comments/175imhe, 2024) documents the cidomo-monopoly overcharge pattern"
    ],
    "Bali": [
        "From Ngurah Rai Airport (DPS), walk OUT to the designated Grab/Gojek pickup zone ~50m from terminal exit — drivers are NOT allowed inside. r/BaliTravelTips 'I ran into the Bali Taxi Mafia' (comments/1onardi, 2025) documents scammers holding 'Grab' signs INSIDE the terminal at 2–4x app rates",
        "Use ONLY bank-branch ATMs during business hours (BCA, Mandiri, BNI, BRI) — never freestanding convenience-store ATMs. r/bali 'Card skimming' (comments/1hqajly, 2025) documents a 2025 Uluwatu ATM cloning case where the card was cloned within 20 minutes",
        "NEVER exchange money at kiosks offering '+4% better rate' without counting bills — r/bali 'SCAM ALERT in Bali – Please Read Before Exchanging' (comments/1r80hy6, 2025) is the named 2025 anchor; use ONLY PT Central Kuta Money Changer or BMC (Bali Maspintjinra)",
        "For scooter rental, ONLY go through your hotel or Biker Bali / Wira Rental (verified Google 4.8+); document EVERY scratch on video with timestamp before signing. r/bali 'Scooter scam' (comments/1ortjng, 2025) documents 'spare key theft' where scammers steal their own rental and claim 5–10M IDR",
        "For solo female travellers or drinking at Canggu/Seminyak beach clubs, NEVER leave your drink unattended and refuse free drinks from strangers — r/TwoXChromosomes 'Warning for women in Bali… organised drink spiking' (comments/1p9euy3, 2025) is a named 2025 first-person anchor documenting Finns Beach Club spiking patterns",
    ],
    "Ubud": [
        "At the Sacred Monkey Forest, leave ALL valuables (sunglasses, earrings, smartphones, passport) in your hotel safe — r/bali 'Monkey steals passports and money at Ubud monkey Forest' (comments/z9loss, 2025) is the named anchor; the monkeys are trained to trade stolen items back for food via staff commission",
        "AVOID any 'Kopi Luwak coffee plantation' tour — r/bali 'Kopi luwak farms and animal welfare in Bali' (comments/1bx3nyi, 2025) documents civet caging is near-universal; buy certified wild-sourced beans from Seniman Coffee Studio or skip entirely",
        "Research yoga retreats on r/digitalnomad 'Bali Ubud and Yoga Barn such a toxic place' (comments/10zcfl5, 2025) and r/yoga before booking; avoid any 'spiritual healing' or 'one-on-one clearing session' upcharges ($200–$2,000)",
        "Book Grab/Gojek for rides — Ubud has an entrenched 'taxi mafia' per r/bali 'Taxi mafia. What it is and how real it is?' (comments/1fo62fm, 2025); meet your driver 100–200m AWAY from restaurant clusters on Jalan Monkey Forest to avoid forced pickup transfers",
        "At Tegallalang Rice Terraces, refuse any 'mandatory guide' (none is required); pay ONLY the 25,000 IDR entry fee at the official booth — r/bali 'Tegallalang rice terrace entrance fees' (comments/1l3jfkq, 2025) documents 'path maintenance' scams at 50K–200K IDR",
    ],
}

# City-specific FAQ
FAQS = {
    "Philadelphia": [
        ("Is Philadelphia safe for tourists?",
         "Philadelphia is generally safe for tourists in the Center City, Old City, Rittenhouse Square, University City, and Independence Mall tourist zones. Violent crime is concentrated in neighborhoods outside the tourist circuit. The practical risks are financial: PHL airport taxi and rideshare overcharges; Independence Hall / Liberty Bell 'skip-the-line' reseller scams (the sites are free or $1); Rocky Steps 'professional photographer' touts; Reading Terminal Market tourist-stall pricing; Center City pickpockets at SEPTA stations; and Airbnb short-term rental fraud. Save Philadelphia Police non-emergency (215-686-8477) and 911 for emergencies."),
        ("How do I get from PHL airport to Center City safely?",
         "The legitimate PHL taxi Center City flat rate is $28.50 (regulated, posted at the taxi stand — any driver refusing this rate or quoting higher is running a scam). Uber and Lyft operate from Zone 2 pickup at both terminals with app-regulated fares $25–$45 depending on surge. SEPTA Airport Line train runs to Jefferson Station for $6.75 every 30 minutes (scam-proof, 25 minutes). AVOID drivers soliciting at baggage claim offering '$50 flat' or 'limo' service — these are unlicensed. Keep a photo of the PHL taxi rate card on your phone as reference for the $28.50 regulated rate."),
        ("How do I visit Independence Hall and the Liberty Bell without getting scammed?",
         "Liberty Bell Center is FREE — no ticket needed, walk in March-December open 9 AM–5 PM. Independence Hall requires a free timed-entry ticket March–December via recreation.gov or nps.gov/inde ($1 reservation fee). January–February: no ticket required, walk-in admission. AVOID third-party reseller websites charging $20–$60 per person for 'skip-the-line' tickets — these are selling free tickets or invalid passes. The 45-minute ranger-led Independence Hall tour includes the Assembly Room where the Declaration of Independence and Constitution were signed — the highlight of the visit."),
        ("Where should I eat Philly cheesesteaks without tourist-trap overcharging?",
         "Avoid South Street cheesesteak venues — all are tourist-priced at $20+ with laminated photo menus and lower quality. Community-verified authentic cheesesteaks at residential pricing: (1) John's Roast Pork (Snyder Ave, widely considered Philly's best, $12–$14); (2) Dalessandro's (Henry Ave, Roxborough, $10–$12); (3) Angelo's Pizzeria (9th/Fitzwater, $13). Reading Terminal Market is the safest one-stop Philly food experience with DiNic's roast pork ($12–$14), Tommy DiNic's, and Beiler's Donuts at posted prices. Pat's vs Geno's at 9th/Passyunk is experience-tourism ($15–$16) — go for the photo, not the food. Learn the lingo: 'wit' (with onions) or 'witout'."),
        ("How do I book Philadelphia accommodation safely?",
         "Book only through Airbnb, VRBO, or Booking.com with platform-verified payment and cancellation protection. REFUSE Zelle, Venmo, or bank transfer payment requests from any 'host' — these are red flags for fraud. Refuse off-platform ID-scan or credit-card-photo requests; Airbnb handles ID verification on-platform. Verify listings with at least 20+ reviews from the last 12 months. Licensed Philadelphia hotels with posted prices: The Ritz-Carlton Philadelphia ($350–$550), Four Seasons Hotel Philadelphia ($500–$800), Kimpton Hotel Palomar ($220–$380), Loews Philadelphia Hotel ($180–$320), Hyatt Centric Center City ($160–$280)."),
    ],
    "Atlanta": [
        ("Is Atlanta safe for tourists?",
         "Atlanta is generally safe for tourists in the Downtown/Centennial Park, Midtown, Buckhead, and Virginia-Highland areas. The practical risks are financial: ATL airport rideshare and taxi overcharges; the high-impact 2025 'US Customs and Border Protection' phone scam per r/Scams 'Got a Call from Atlanta's US Customs and Border Protection' (comments/1p1lnfu, 2025); Georgia Aquarium / World of Coca-Cola ticket reseller scams; MLK Center tour touts (the sites are free); Ponce City Market / BeltLine tourist-menu overcharging; and convention-season Airbnb short-term rental fraud. Save Atlanta Police non-emergency (404-614-6544) and 911 for emergencies."),
        ("What is the 'US Customs and Border Protection' phone scam?",
         "r/Scams 'Got a Call from Atlanta's US Customs and Border Protection' (comments/1p1lnfu, 2025) is the named 2025 anchor. Scammers spoof a 404-area-code phone number, claim to be CBP officers, and tell the victim that a 'package containing illegal substances' has been seized at ATL airport. They demand payment of $1,000–$5,000 via Zelle, Venmo, gift cards, or wire transfer to 'avoid arrest.' CRITICAL: US Customs and Border Protection NEVER calls travelers demanding payment by phone — all communications are in writing via USPS mail. Hang up immediately. Report to Federal Trade Commission at reportfraud.ftc.gov. Verify legitimate CBP concerns by calling CBP directly at 1-877-CBP-5511."),
        ("How do I get from Atlanta airport (ATL) to downtown safely?",
         "MARTA Red or Gold Line runs from ATL station directly to downtown Five Points in 20 minutes for $2.50 — scam-proof and the fastest/cheapest option. Uber and Lyft operate from designated pickup zones (North Terminal: North Economy Parking; South Terminal: South Economy Parking) with app-regulated fares $20–$35 depending on surge. Licensed taxis with meter running are $30–$45 to downtown. AVOID drivers soliciting at baggage claim offering 'flat $60' — these are unlicensed. Ignore fake 'MARTA ticket agents' in the terminal — buy Breeze Card at the official MARTA station kiosk for $2.50."),
        ("How do I book Georgia Aquarium and World of Coca-Cola tickets without getting overcharged?",
         "Book direct at the official sites: Georgia Aquarium ($49.95 adult at georgiaaquarium.org), World of Coca-Cola ($22 at worldofcoca-cola.com). For multiple attractions, the genuine Atlanta CityPASS ($85-$95 depending on dates at citypass.com — the ONLY legitimate CityPASS site) covers 5 attractions: Georgia Aquarium, World of Coca-Cola, Zoo Atlanta, Fernbank Museum, College Football Hall of Fame. Third-party resellers charge $75+ for Georgia Aquarium alone — 50%+ markup for the same tickets. AVOID Google ads for 'Atlanta Aquarium tickets' which lead to resellers; scroll past sponsored results to georgiaaquarium.org directly."),
        ("How do I visit the MLK Historical Park?",
         "The entire Martin Luther King Jr. National Historical Park is FREE: MLK Center (tomb and reflection pool), Ebenezer Baptist Church (historical site, not the current active congregation), King Center, and the MLK birthplace home. Reserve the free birthplace home tour at recreation.gov 1–7 days ahead (limited daily spots). NPS ranger-led tours are comprehensive and free. AVOID paid 'MLK Walking Tour' packages at $80+ per person — these charge for free self-guided content. The Sweet Auburn historic district surrounding the park is a free pedestrian heritage zone best explored on foot at your own pace. For older travelers, Auburn Avenue is walkable but the full park spans about a 0.5 mile walk end to end."),
    ],
    "Phoenix": [
        ("Is Phoenix / Scottsdale safe for tourists?",
         "Phoenix and Scottsdale are generally safe tourist destinations — violent crime against visitors is uncommon in Downtown Phoenix, Old Town Scottsdale, the Scottsdale Waterfront, Camelback Corridor, Biltmore, and resort areas. The practical risks are financial: the 2024-2025 'skin' / phone-handoff scam in Old Town Scottsdale (r/Scottsdale 'Beware of Scam in old town Scottsdale' comments/1dt506e + 'cart driver and skins scammed them' comments/1qvhes6, 2025 named anchors); PHX Sky Harbor rideshare and taxi overcharging; Grand Canyon day-trip package markups from hotel concierges; aggressive Scottsdale timeshare presentation hustles; resort auto-gratuity surprises; and PHX rental-car damage-claim and insurance-upsell scams. Save Phoenix PD non-emergency (602-262-6151), Scottsdale PD (480-312-5000), and 911."),
        ("What is the Old Town Scottsdale 'skin' scam?",
         "r/Scottsdale 'Beware of Scam in old town Scottsdale' (comments/1dt506e) is the named anchor and r/Scottsdale 'My friend said this cart driver and skins scammed them' (comments/1qvhes6, 2025) documents the 2025 continuation. A stranger in Old Town Scottsdale's bar strip approaches and asks to 'borrow your phone' to call an Uber or make an emergency call. If your Venmo, Zelle, or Cash App lacks PIN protection, the scammer quickly sends themselves $500–$3,000 before returning the phone. The 2025 variant uses golf-cart drivers offering 'free rides' who extract payment during the ride. Defense: NEVER hand an unlocked phone to a stranger — if someone genuinely needs help, offer to call 911 yourself on speaker. Enable PIN protection on all payment apps. r/arizona 'Fraud PSAs posted in Scottsdale' (comments/1leqx1i, 2025) confirms Scottsdale has posted official fraud warnings in tourist areas."),
        ("How do I get from Phoenix Sky Harbor (PHX) to downtown or Scottsdale?",
         "The safest/cheapest is the free PHX SkyTrain from any terminal to 44th Street/Washington station, then Valley Metro light rail to downtown for $2 per ride. Uber/Lyft from the designated rideshare pickup zone (Terminal 3/4 curb) runs $18–$35 to downtown, $25–$40 to Scottsdale — screenshot the fare estimate before boarding. Licensed taxis with meter running are $30–$45 to downtown. AVOID drivers soliciting at baggage claim offering 'flat $60' or 'limo' touts quoting $100+ for standard trips. If a rideshare driver demands a cash tip beyond the app total at drop-off, refuse and report via the app. For older travelers, Valley Metro light rail has elevator access at 44th Street station and is fully accessible."),
        ("How do I book a Grand Canyon day trip from Phoenix without getting overcharged?",
         "Grand Canyon South Rim is 3.5 hours drive from Phoenix (230 miles). Legitimate full-day bus tours via Viator, GetYourGuide, or Detours American West run $150–$250 per person including park entry. Hotel-concierge 'Grand Canyon day trip' packages mark up 30–80% to $300–$450 for the same experience. For helicopter tours, book direct with Maverick Helicopters or Papillon ($250–$400) — not hotel 'helicopter package' upsells at $500+. If self-driving, the park entry fee is $35 per vehicle for a 7-day pass. For Antelope Canyon + Grand Canyon combo tours, expect $350–$450 direct — not $600+ from third-party resellers. Always pay with credit card for chargeback leverage if the tour operator disappears."),
        ("Should I accept a 'free gift' Scottsdale timeshare presentation offer?",
         "NO — the time cost and high-pressure sales tactics make it net negative even with the 'free gift' (round of golf, spa treatment, or $100 dinner voucher). The advertised 90-minute presentation actually runs 2–4 hours with aggressive pushing of $15,000–$50,000 timeshare purchases. If you did sign under pressure, Arizona offers a 7-day right of rescission for timeshare contracts — cancel within 7 days by certified mail. For genuine rescission assistance, contact the Arizona Attorney General Consumer Protection office (azag.gov) directly — AVOID 'exit' companies charging $5,000–$15,000 upfront, many of which are themselves scams. r/Charleston 'Great Vacations,LLC Travel Club Scam' (comments/1jpvapu, 2025) and r/bransonmo 'Branson Travel Group is a scam' (comments/15oum98) show the US-wide pattern."),
    ],
    "Sedona": [
        ("Is Sedona safe for tourists?",
         "Sedona is very safe for tourists — violent crime is nearly nonexistent and the small town sees millions of visitors annually to its red-rock vortex sites. The practical risks are financial tourist-trap patterns: 'energy vortex tour' overcharges for free public-land hikes (r/arizona 'are the energy vortexes real or a tourist trap?' comments/lpdsug named anchor); Pink Jeep Tour hotel-concierge markups; Red Rock Pass and parking-ticket confusion; misrepresented 'certified Native American' jewelry; and Phoenix-to-Sedona transfer scams. r/Sedona 'Honest review of Sedona from a tourist' (comments/14vjyr8) frames the community view on tourist-trap pricing. The main physical risks are heat (May–September can exceed 105°F) and trail-related falls on slickrock — not crime. Save Sedona PD non-emergency (928-282-3100) and 911 for emergencies."),
        ("Are Sedona's 'energy vortexes' real or a tourist trap?",
         "Sedona's four 'energy vortex' sites — Airport Mesa, Cathedral Rock, Bell Rock, Boynton Canyon — are Forest Service public-land red-rock formations, all FREE to hike with a Red Rock Pass ($5/day). The 'energy' claim has no scientific basis; r/arizona 'are the energy vortexes real or a tourist trap?' (comments/lpdsug) captures community skepticism ('felt nothing at Sedona'). Hotel concierges sell 'certified vortex experience' tours at $150–$400 per person for the same public-land hikes — these are pure markup. 'Aura photography' ($50–$150) uses standard thermal cameras with no scientific validity. 'Certified Sedona shaman' private sessions ($300+) are unregulated. Go self-guided to the free viewpoints with a $5 Red Rock Pass — the rocks are stunning regardless of whether 'energy' is real."),
        ("How do I book a Sedona jeep tour without getting overcharged?",
         "Pink Jeep Tours is Sedona's dominant and legitimate operator — book direct at pinkjeeptours.com or the uptown Sedona office for best rates ($100–$250). Broken Arrow is their signature 2.5-hour route ($130). For older travelers concerned about rough off-road terrain, request Scenic Rim or Ancient Ruin tours which use softer roads. Hotel concierges typically mark up Pink Jeep by $30–$80 per person — book direct instead. AVOID third-party 'discount Pink Jeep' resellers — all charge more than pinkjeeptours.com direct. 'Private charter' upsells at $500–$1,000 are markups on what are standard shared 2.5-hour tours. Book 1–3 days ahead in peak season (March–May, September–November). Pay with credit card, never Zelle/Venmo."),
        ("How do I handle Red Rock Pass and trailhead parking in Sedona?",
         "Sedona trailhead parking requires a Red Rock Pass ($5/day, $15/week, $20/annual per vehicle) — a Forest Service permit displayed on the dashboard. Buy ONLY at: Sedona Visitor Center (Hwy 89A), Forest Service office, Sedona Ranger District (8375 Hwy 179), or any trailhead self-pay kiosk. If you visit 3+ federal sites per year, the America the Beautiful National Parks Annual Pass ($80) covers Red Rock Passes and is better value. REFUSE any 'parking attendant' in a reflective vest demanding $20 cash at a trailhead — no legitimate attendants exist at Sedona trailheads; this is a scam. AVOID third-party websites selling 'Sedona Parking Pass' at $20–$40 per day (actual $5). Park only in designated trailhead lots — Sedona enforces strict no-roadside-parking rules."),
        ("How do I get from Phoenix Sky Harbor to Sedona?",
         "Sedona is 120 miles (2 hours via I-17 North) from PHX airport — note that Sedona Airport (SDL) is general aviation only, no commercial flights. Legitimate options: (1) Groome Transportation shuttle direct at groometransportation.com — $78 one-way per person, 2.5 hours, runs 10 times daily, the scam-proof default choice; (2) rental car self-drive via I-17 North if you plan to explore Arizona further (~2 hours); (3) hotel-arranged private transfer for Enchantment Resort, L'Auberge de Sedona, or similar properties at $300–$500 is legitimate if booked through the hotel direct. AVOID third-party 'Sedona transfer' websites charging $250–$400 for what Groome does for $78. Uber/Lyft is possible but rare with surge pricing at $250–$400+."),
    ],
    "Savannah": [
        ("Is Savannah safe for tourists?",
         "Savannah's historic district is generally safe for tourists — violent crime against visitors is uncommon in the River Street, Factors Walk, City Market, Forsyth Park, and Historic District zones during daytime. The practical risks are financial: SAV airport taxi overcharging (r/savannah 'Airport taxi scam' comments/1grpmor named anchor); the 2025 'fake monk' bracelet-donation scam on River Street (r/savannah 'What's up with the monk on River Street?' comments/1kmjc3m, 2025); inflated ghost-tour pricing from curb touts; River Street auto-gratuity and 'souvenir cup' overcharges; carriage-tour animal-welfare concerns; and STR (Airbnb) off-platform booking fraud. Save Savannah Police non-emergency (912-651-6675) and 911 for emergencies. Avoid eastern parts of the city outside the Historic District after dark."),
        ("What is the 'monk' scam on Savannah's River Street?",
         "r/savannah 'What's up with the monk on River Street?' (comments/1kmjc3m, 2025) is the 2025 named anchor. Individuals wearing orange or saffron robes approach tourists on River Street, Factors Walk, or City Market, place a bracelet or small trinket on your wrist 'as a gift,' then demand $20–$100 'donation for the temple.' They are NOT affiliated with any legitimate Buddhist monastery — genuine Buddhist monks do not solicit money on streets. The same scam runs in NYC, San Francisco, Paris, Rome, and Barcelona. Defense: REFUSE all items handed by strangers. If a bracelet is already on your wrist, remove it and return it without entering into negotiation — do NOT pay. Keep walking firmly. Report aggressive demands to Savannah PD non-emergency (912-651-6675)."),
        ("How do I book a Savannah ghost tour without getting overcharged?",
         "Book direct with reputable operators: Ghost City Tours (ghostcitytours.com, $25), Old Savannah Tours ($29), or Savannah Haunted History ($35). These are all 90-minute walking tours covering Colonial Park Cemetery, the Kehoe House, the Moon River Brewing Company, and other haunted sites. AVOID curb touts with laminated signs quoting '$45 tonight only' — legitimate operators don't sell at 2x in the curb. Hotel-concierge 'ghost tour package' markups run $65+ per person for what's bookable at $25 direct. Colonial Park Cemetery is free to walk during daylight hours — no 'VIP cemetery access' exists. For older travelers with mobility concerns, Old Town Trolley ($45 hop-on all day) includes ghost narration and is more accessible than walking tours. Book 1–3 days ahead in October peak season."),
        ("Is the SAV airport taxi scam real, and what should I do?",
         "Yes — r/savannah 'Airport taxi scam' (comments/1grpmor) is the direct named anchor documenting the pattern. Drivers at the SAV taxi queue quote a 'flat $45–$60' to downtown Savannah (legitimate metered fare is $25–$35), insist the meter is 'broken,' or add surprise 'surcharges' for luggage, airport fees, or 'night rate.' Clean alternatives: (1) Uber or Lyft at the designated rideshare pickup zone with fare screenshot before boarding — $20–$32 to downtown; (2) licensed taxi with meter running: $25–$35 to downtown (refuse 'flat rate' offers); (3) for Hilton Head Island, book Low Country Adventures shuttle direct (lowcountryadventures.com, $37 one-way) — avoid airport touts at $150+. If a driver claims the meter is 'broken,' exit immediately and take the next licensed cab."),
        ("How do I avoid short-term rental (STR) fraud in Savannah?",
         "Savannah is debating tightening STR regulations similar to Tybee Island's ban — r/savannah 'Will Savannah ever \"ban\" STRs like Tybee?' (comments/1l51so0, 2025) is the 2025 named anchor. Booking protection: (1) book ONLY through Airbnb, VRBO, or Booking.com platform payment — NEVER Zelle, Venmo, Cash App, or wire transfer, regardless of what 'discount' the 'host' offers; (2) verify the Savannah STR certificate number by searching the savannahga.gov STVR registry before paying; (3) for peak seasons (St. Patrick's Day March, October, Thanksgiving, Christmas), book 3–6 months ahead; (4) legitimate hotels: Mansion on Forsyth Park, The DeSoto, Perry Lane Hotel, Hyatt Regency Savannah, Marriott Riverfront; (5) for Tybee Island, only already-registered STRs are legal — book via Airbnb/VRBO with the license number visible on the listing."),
    ],
    "Charleston": [
        ("Is Charleston SC safe for tourists?",
         "Charleston's historic peninsula is generally safe for tourists — violent crime against visitors is uncommon in the Broad Street, Meeting Street, King Street, Battery, and Rainbow Row areas during daytime. The practical risks are financial: the 2025 'palmetto rose' / 'oldest scam in the book' hustle at City Market per r/Charleston 'Oldest scam in the book' (comments/1kq8w1k, 2025) named anchor; the 2025 local-shrimp restaurant-deception scandal (91% of 44 tested restaurants served imported farm-raised shrimp as 'local' per r/Charleston '90% of Charleston restaurants were found to be deceiving' comments/1l80u7c, 2025); auto-gratuity tipping overcharges per r/CapitalOne_ '523% tip? I think not' (comments/1qo0z70, 2025); carriage-tour hotel-concierge markups; the 'Great Vacations LLC' Meeting Street timeshare hustle; and CHS airport rideshare/taxi overcharging. Save Charleston Police (843-743-7200) and 911 for emergencies."),
        ("What is the 'oldest scam in the book' at Charleston's City Market?",
         "r/Charleston 'Oldest scam in the book - but why is it allowed?' (comments/1kq8w1k, 2025) is the 2025 named anchor referring to Charleston's long-running palmetto-rose hustle. Individuals at City Market and Meeting Street weave a palmetto-frond rose in 10 seconds, hand it to a spouse or older traveler 'as a gift,' then demand $10–$30 cash 'for the art.' The target feels obligated because the rose is already in their hand. Variants: fake 'charity' buckets with sob-story cards; aggressive 'fortune teller' who grabs your hand before reading; fake 'photographer' who photographs you unsolicited then demands $15–$25. Defense: keep hands in pockets, refuse all unsolicited 'gifts,' return the palmetto rose immediately if placed in your hand, and buy genuine palmetto roses at Gullah artisan stalls inside City Market with posted $3–$10 prices."),
        ("Is the Charleston local-shrimp scandal real, and where can I eat verified local shrimp?",
         "Yes — r/Charleston '90% of Charleston restaurants were found to be deceiving' (comments/1l80u7c, 2025) and 'Local Shrimp Scandal Releases 25 Named Restaurants' (comments/1lq2r20, 2025) are the NAMED 2025 anchors. SC DNR and the South Carolina Environmental Law Project tested shrimp at 44 restaurants advertising 'local shrimp' and found 40 (91%) served imported farm-raised shrimp from Asia priced at a local-shrimp premium ($28–$38 per dish). For verified local shrimp, use the SC Shrimpers Association 'Certified SC' list at certifiedsc.com. Verified restaurants include: Magnolia's, Husk, FIG, Hominy Grill, and Slightly North of Broad. At Shem Creek, Red's Ice House and Shem Creek Bar & Grill are verified local. Always ask the server directly: 'Is this wild-caught local or imported farm-raised?' — honest restaurants will tell you. Report menu-claim fraud to scdnr.gov."),
        ("How do I book a Charleston carriage tour without getting overcharged?",
         "Book direct with reputable operators: Palmetto Carriage Works (palmettocarriage.com, $34), Old South Carriage Company ($38), or Classic Carriage Works ($33). Charleston carriage routes are randomized by city medallion lottery — any 'route upgrade' offered at $20+ is a scam since no operator controls which route you get. Hotel-concierge markups run $65–$95 per person for what's $30–$50 direct. 'Private charter' upsells at $300–$500 are markups on shared 16-passenger carriages. IMPORTANT: Charleston city ordinance suspends carriage tours when temperatures exceed 95°F for animal welfare — on hot summer days, confirm the tour will actually run before booking, and refuse operators willing to run illegally in extreme heat. Ride in early morning (9–11am) or late afternoon (after 4pm) in summer."),
        ("How do I get from Charleston International (CHS) to downtown safely?",
         "r/Charleston 'CHS Airport Uber' (comments/1nucopj, 2025) and 'Rideshare options/availability?' (comments/1q5ldef, 2025) are the 2025 named anchors confirming Uber/Lyft dominance. Legitimate fares: Uber/Lyft $22–$35 depending on surge (pickup at Garage Level 3); licensed taxi with meter $30–$42 at the taxi stand; CARTA airport express bus $3.50 (schedule-limited, check carta.com). AVOID drivers soliciting at baggage claim offering 'flat $55 to downtown' — these are unlicensed and overcharging by 50%+. 'Limo' or 'black car' touts quoting $100+ for standard trips are also scams. During peak Uber surge (Friday evening, Sunday afternoon), compare the Uber price to the taxi stand rate — taxi is often cheaper at those times. Never pay a cash tip beyond the Uber app total — app-entered tips are already processed."),
    ],
    "Pingyao": [
        ("Is Pingyao safe for tourists?",
         "Pingyao is generally very safe — violent crime against foreigners is extremely rare, and the UNESCO ancient city is well-preserved and walkable. The practical risks are financial tourist-trap patterns: Ancient City ticket bundle overcharges with fake skip-the-line; 'silk workshop' and 'ancient currency museum' commission shopping per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024); courtyard guesthouse off-platform booking fraud; Taiyuan-Pingyao transit tout scams; and South Street tourist-menu restaurant overcharging. Note: r/travelchina 'Travelling to China for 19 days' (comments/24g5fu) frames the tourist consensus — 'skip pingyao. it's a tourist trap' — meaning Pingyao's commercial overlay is widely acknowledged, though the UNESCO heritage itself is worth seeing with defensive booking. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I visit Pingyao Ancient City affordably?",
         "Buy the Ancient City Tongpiao (通票) at ¥125 per person at the South Gate ticket office or via Trip.com / Ctrip. The Tongpiao is valid for 3 days and covers access to 20+ monuments inside: Rishengchang Exchange Shop (China's first bank), Confucius Temple, City Tower, Qing government offices, ancient city walls (6 km walkable), and Mingqing Street historic mansions. No 'combo' or 'VIP' upgrades exist — these are commission markups. Walk the ancient walls from North Gate or South Gate entrances — they're included in Tongpiao and offer the best views. AVOID third-party 'skip-the-line' resellers at ¥250+ — there is NO official skip-the-line; the queue is 2–5 minutes even in peak season."),
        ("How do I get from Taiyuan to Pingyao safely?",
         "Take the Taiyuan-Pingyao high-speed rail (¥23 per person, 1.5 hours) from Taiyuan South Railway Station (or Taiyuan Railway Station). Alternative: slow local train (¥7.5, 1h45m) is the budget option. Book via Trip.com or 12306.cn. At Pingyao Railway Station, walk to Pingyao Ancient City South Gate (2.5 km, 25 min via well-signed street) or use DiDi / local taxi with 'da biao' expect ¥10–¥15 on meter. REJECT taxi touts at Taiyuan South quoting ¥300+ 'private car' per r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) — the train is cheaper and faster. If you arrive at Taiyuan Wusu Airport (TYN), use the high-speed rail from Taiyuan South rather than a 'direct transfer shuttle' at markup."),
        ("How do I avoid the Pingyao silk-workshop and museum scams?",
         "SKIP all 'Pingyao Silk Workshop,' 'Ancient Chinese Currency Museum,' 'Shanxi Black Vinegar Distillery,' and similar South Street 'museum' venues that include product demonstrations. These are commission-driven shopping traps — 10-min 'demonstration' followed by 60–90 min of pressure sales for silk quilts ¥3,000–¥15,000, 'rare ancient coins' ¥500–¥5,000, and 'family-recipe vinegar' ¥200–¥800. Rishengchang Exchange Shop (included in your ¥125 Tongpiao) is the GENUINE historical bank museum with posted exhibitions. Shuanglin Temple (20 km outside Pingyao, ¥35 entry + ¥15 bus) is a genuine Ming Dynasty Buddhist temple. For silk, go to Suzhou Silk Museum or Taobao.com. For Shanxi vinegar, residential supermarkets sell Shuita (水塔) or Dongxing (东兴) brands at ¥20–¥60 per bottle."),
        ("Where should I stay in Pingyao?",
         "Book courtyard guesthouses through Booking.com, Agoda, or Trip.com with platform-verified payment — NEVER accept off-platform 'WeChat direct booking' offers from strangers at Taiyuan or Pingyao stations. Legitimate rates: ¥150–¥300/night for basic authentic courtyard rooms; ¥400–¥800/night for boutique refurbished courtyards. Community-recommended: Harmony Guesthouse (¥180–¥300, authentic siheyuan), Yide Hotel (¥200–¥400, mid-tier), Jing's Residence (¥600–¥1,000, boutique upscale — legitimate). On arrival, verify the booking confirmation matches what you pay at check-in — screenshot any discrepancies. Refuse 'courtyard upgrade' pitches at ¥100+. For authentic Pingyao cuisine, walk one block off South Street to Deju Yuan Noodle (¥18–¥30), Yun Jin Cheng (¥15–¥25), or for Pingyao beef visit Pingyao Guanyun Beef Company flagship (¥50–¥100)."),
    ],
    "Harbin": [
        ("Is Harbin safe for tourists?",
         "Harbin is generally safe — violent crime against foreigners is very rare, and the city's winter tourism (December–February) is well-organized. r/travelchina 'from being paranoid to actually relaxed - china wasnt what' (comments/1q9t4nq, 2025) captures the 2025 reassuring view. The practical risks are tour/ticket-related: Harbin Ice and Snow Festival ticket overcharges; 'Snow Village' (Xuexiang) day-trip scam per r/harbin_china 'Looking for Harbin travel experience' (comments/1i1e0t7, 2025) named anchor; HRB airport winter taxi overcharges with fake 'snow surcharge'; Zhongyang Street Russian 'souvenir' and fur-coat counterfeits; tourist-menu 'Russian restaurant' overcharging; and overnight Snow Village package scams. Save 12315 (English consumer complaints) and 110 (police). Winter safety note: Harbin reaches -30°C in January — pack serious cold-weather gear, thermal underwear, snow boots, and hand warmers."),
        ("How do I book the Harbin Ice and Snow Festival affordably?",
         "Book Harbin Ice and Snow World direct via Ctrip / Trip.com at official prices: ¥330 day entry (Dec 23 – Feb 25) or ¥460 evening entry (5 PM – 9:30 PM). The evening entry is worth the premium — ice sculptures are lit with LEDs creating the dramatic photos the festival is famous for. AVOID third-party WeChat / Facebook resellers offering 'VIP' tickets at ¥800–¥1,200 per person — no official VIP exists. For older travelers, arrive 5:00–5:30 PM to see sculptures in both daylight and lit-up transition; bring hand warmers and thick gloves (minus-20 to minus-30°C conditions). r/harbin_china 'Looking for Harbin travel experience' (comments/1i1e0t7, 2025) is the 2025 Harbin community anchor."),
        ("Should I go to Snow Village (Xuexiang)?",
         "No — r/harbin_china 'Looking for Harbin travel experience' (comments/1i1e0t7, 2025) is blunt: 'Snow Village is a scam... You c' an see similar scenery around Harbin for free. Hotel-concierge 'Snow Village 2-day overnight' packages at ¥1,500–¥3,500 per person deliver commission-driven photo spots, expensive lodging, and ¥200–¥500 horse-sleigh rides that cost ¥80 residential. If you insist on visiting, self-guided cost is ~¥500–¥800 per person. The better winter-experience alternatives around Harbin: (1) Yabuli Ski Resort (¥250–¥400 day-pass for skiing/scenery, 2.5h drive); (2) Volga Manor (Russian-themed cultural park, ¥115 entry, authentic architecture); (3) Siberian Tiger Park (¥95 entry); (4) Zhongyang Street + St. Sophia Cathedral (¥30) for Russian-Harbin architecture walking tour. The genuine Harbin highlight remains the Ice and Snow World festival itself."),
        ("How do I get from Harbin airport (HRB) to central Harbin in winter?",
         "Airport Shuttle Bus Line 1 runs HRB to Zhongyang Street (Central Street) for ¥20 per person in 45 minutes — heated, runs through winter conditions. Airport Shuttle Bus Line 2 to Harbin Railway Station is ¥20 in 50 min. DiDi with international-number sign-up works at the official rideshare pickup zone. If licensed taxi, 'da biao' (打表) and expect ¥110–¥180 HRB-to-centre (upper range in winter conditions due to slow driving). REJECT any 'snow surcharge' or 'winter supplement' claims — there is NO official winter surcharge in Harbin per Heilongjiang transportation authority. Drivers refusing the meter citing 'winter operations' are running the scam. Photograph taxi plate number before boarding. For winter travel, wear the heaviest coat you own for the outdoor waits — Harbin reaches -30°C."),
        ("Where should I eat in Harbin for authentic Russian cuisine?",
         "Community-vetted Russian restaurants with posted prices (book via Dianping, 4.5+ ratings reliable): (1) Lucia Russian Restaurant (¥150–¥300 per person — institution with genuine Russian chef lineage); (2) Harbin Portman Western Restaurant (¥120–¥200 — longstanding Harbin name); (3) Russian Russia Restaurant (¥100–¥180); (4) Modern Hotel's Russian Bar (Harbin heritage venue, ¥100–¥200). AVOID Zhongyang Street 'Russian' venues with laminated English/Russian photo menus at ¥300–¥700 per person — the same borscht and chicken kiev at 2–3x residential pricing. Order signatures: borscht (red beet soup, residential ¥25–¥45), chicken kiev (¥80–¥120), beef stroganoff (¥100–¥150), Russian bread 'gelieba' (hardtack-style, ¥20–¥40), Harbin smoked sausage 'hongchang' (¥40–¥80). For authentic Harbin-Russian atmosphere without premium-dining prices, Modern Hotel's Russian Bar is the older-traveler-friendly choice."),
    ],
    "Chongqing": [
        ("Is Chongqing safe for tourists?",
         "Chongqing is generally safe — violent crime against foreigners is very rare. The practical risks are financial: Yangtze River cruise ticket overcharges and fake-operator scams per r/China 'Tours with forced shopping stops' (comments/1sbqo0g, 2025); CKG airport taxi overcharges per r/travelchina (comments/1ks12o9, 2025); Jiefangbei/Hongyadong tourist-strip hotpot overcharging; Dazu Rock Carvings hotel-concierge day-trip markup; on-cruise shore-excursion upsells; and Hongyadong 'professional photographer' touts. r/travelchina 'Ask me anything about chongqing and chengdu' (comments/1smy9iz, 2025) is the 2025 Chongqing community anchor. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I book a Yangtze River cruise without getting scammed?",
         "Book ONLY with verified cruise lines: Victoria Cruises (victoriacruises.com), Century Cruises (centurycruises.com.cn), Sanctuary Yangzi (sanctuaryretreats.com), or President Cruises (presidentcruise.com) — all have English-language websites with posted itineraries. Alternatively, book via Trip.com, Viator, or hotel's Ctrip partnership with the cruise line named. Confirm in writing: cabin category, all inclusions, all shore-excursion specifics. Pay with credit card for chargeback leverage. REJECT any Yangtze cruise under ¥2,500 per person for 4 days — price floor for legitimate product per r/China 'Tours with forced shopping stops' (comments/1sbqo0g, 2025). Third-party 'discount' sellers on WeChat/Facebook promising ¥1,200–¥2,000 4-day cruises are either fake or lead to non-cruise 'river experiences.' Three Gorges highlights worth seeing: Shibaozhai, Qutang Gorge, Wu Gorge, Xiling Gorge, Three Gorges Dam viewpoint."),
        ("How do I get from Chongqing airport (CKG) to the city?",
         "Metro Line 10 from CKG to Hongtu Didi Square (downtown): ¥6–¥8, 45 min, scam-proof. DiDi with international-number sign-up works at the official rideshare pickup zone. If licensed taxi, 'da biao' (打表) and expect ¥60–¥90 CKG-to-centre. Chongqing's vertical mountain-city geography creates navigation confusion that scam drivers exploit — screenshot a DiDi fare estimate BEFORE boarding any taxi, and verify routes via DiDi GPS in real-time. AVOID drivers approaching inside the terminal with 'fixed price' quotes of ¥150+ per r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025). Photograph taxi plate number from the rear windscreen."),
        ("Where should I eat Chongqing hotpot?",
         "Walk one block off Jiefangbei pedestrian zone or Hongyadong scenic area for authentic Chongqing hotpot. Community-vetted names: Liuyishou (六一手, national chain with consistent Chongqing quality ¥90–¥140 per person), Qiqi Hotpot (¥80–¥130), Dezhuang (¥100–¥160), Xiao Jiang Hotpot (¥90–¥130). Use the Dianping app (Chinese Yelp) with 4.5+ ratings. Expect ¥90–¥160 per person at authentic venues; tourist-strip laminated-English-menu hotpot at ¥200–¥400 is overcharge. For first-time Sichuan-pepper experience, order yuanyang (鸳鸯) half-spicy half-mild broth and ask 'yi dian dian la' (slightly spicy). AVOID tout-driven restaurants with English-only photo menus at Jiefangbei or Hongyadong complex."),
        ("How do I visit Dazu Rock Carvings without tour-package markup?",
         "Self-guided total ~¥270 per person vs hotel-concierge packages at ¥350–¥800. Steps: (1) Chongqing-Dazu coach from Chongqing Caiyuanba Bus Station ¥65 per person (2h); (2) on arrival at Dazu, local taxi or bus to Baoding Mountain ¥20 (30 min); (3) buy entry ticket at Baoding Mountain ¥115 or Beishan ¥70 or combined ¥140 at the ticket office or via Trip.com; (4) self-guided visit 3–4 hours exploring the UNESCO-listed Buddhist/Taoist rock-cut caves; (5) return coach Dazu-Chongqing ¥65. Hotel-concierge Dazu day-trip packages ALWAYS include 60–90 min of 'Dazu traditional crafts' or 'Buddhist statue' shopping stops per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024)."),
    ],
    "Zhangjiajie": [
        ("Is Zhangjiajie safe for tourists?",
         "Zhangjiajie is generally safe — violent crime against foreigners is very rare, and the UNESCO national forest park area is well-monitored for tourist safety. r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025) captures the 2025 self-guided view: 'Also, didn't get scammed in Zhangjiajie. Still used didi to' navigate. The practical risks are financial: Zhangjiajie National Forest Park and Tianmen Mountain ticket overcharges with fake skip-the-line; hotel-concierge multi-day tour packages at ¥1,500–¥3,000 per person with commission shopping stops per r/Scams 'CHINA Group Tour at Zhuhai Jewelry Museum/Shop' (comments/1gv3wru, 2024); DYG airport taxi overcharges; Wulingyuan tourist-menu restaurant overcharging; Tianmen Mountain 'VIP tour' upsells; and Tujia ethnic-minority village commission shopping. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I visit Zhangjiajie National Forest Park affordably?",
         "Buy the Zhangjiajie National Forest Park 4-day multi-entry ticket at ¥228 per person — this includes all park shuttle buses within. Buy at the park entrance or via Trip.com / Ctrip / official WeChat mini-program. Stay 2–3 nights at a Wulingyuan-area hotel (¥200–¥500/night via Booking.com or Trip.com) to cover all major areas: Zhangjiajie (Yuanjiajie, Tianzi Mountain, Yellowstone Village), Suoxiyu Valley, and Yangjiajie. Use Bailong Elevator (¥72) for Yuanjiajie access if mobility concern. Self-guided total with 3-day park visit: ~¥700–¥1,000 per person including accommodation vs hotel-concierge tour packages at ¥1,500–¥3,000. r/travelchina 'Is this legit?' (comments/1qa5xxk, 2025) is the 2025 tour-verification anchor."),
        ("How do I visit Tianmen Mountain without getting overcharged?",
         "Buy the ¥258 standard Tianmen Mountain ticket at the ticket office or via Trip.com — includes: (1) cable car up (the world's longest passenger cable car at 7.5 km, 30-min ride); (2) all on-top shuttles; (3) shuttle down the 99 bends road to Tianmen Cave; (4) Heaven's Gate viewing. The 999-step staircase to Heaven's Gate is strenuous — for mobility concerns, use the escalator (¥32 one-way from mid-mountain). Glass walkway shoe-cover rental is ¥10–¥15 at the entrance. Take your own photos at Heaven's Gate — refuse 'professional photographer' touts. AVOID hotel-concierge 'Tianmen Mountain VIP tour' at ¥500+ per person — the standard ticket includes everything. r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025) confirms self-guided works at Zhangjiajie."),
        ("Should I book a Zhangjiajie multi-day tour package?",
         "Only if paid at the high end. AVOID hotel-concierge 'Zhangjiajie 3-day all-inclusive' at ¥1,500–¥3,000 per person — r/Scams 'CHINA Group Tour at Zhuhai Jewelry Museum/Shop' (comments/1gv3wru, 2024) documents the canonical Beijing+Zhangjiajie scam format with Tujia village, silver workshop, and 'traditional Tibetan medicine clinic' commission stops. Self-guided: book hotel direct via Booking.com (¥200–¥500/night Wulingyuan area) + buy park tickets yourself + use DiDi for intra-area transit. Total: ~¥1,100 per person for 3 days vs ¥1,500–¥3,000 package. For authentic Tujia culture (if interested), visit Furong Ancient Town (芙蓉镇, ¥75 entry) as a standalone day trip rather than packaged tour."),
        ("How do I get from Zhangjiajie airport (DYG) to Wulingyuan?",
         "The direct airport-to-Wulingyuan shuttle runs ¥30 per person in 50 minutes, hourly throughout the day — the most practical option for older travelers with luggage. Alternatively: Airport Shuttle Bus DYG to Zhangjiajie City is ¥8, then Wulingyuan bus is ¥15 (total ¥23, slower). DiDi with international-number sign-up at official rideshare pickup zone is also reliable in Zhangjiajie per r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025). Licensed taxi with 'da biao' (打表) from DYG to Wulingyuan is ¥80–¥120 on meter; refuse drivers approaching inside the terminal quoting ¥200–¥400 'fixed prices.' For Zhangjiajie-Changsha connections, use the high-speed rail from Zhangjiajie West Station."),
    ],
    "Lijiang": [
        ("Is Lijiang safe for tourists?",
         "Lijiang is generally safe — violent crime against foreigners is very rare, and r/travelchina 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bp2j, 2025) captures the 2025 view: 'No one scammed me in Lijiang, Xianggelila Yunnan' for self-guided travel. The practical risks concentrate at packaged-tour and nightlife touchpoints: Old Town entry-fee confusion and fake-ticket touts; hotel-concierge day-trip packages to Yulong Snow Mountain + Tiger Leaping Gorge + Shangri-La at ¥500–¥1,200 per person (vs self-guided ~¥440); Naxi 'cultural experience' overcharges; Old Town bar-street dating-app/hostess-bar traps after 10 PM per r/chinalife 'Random meeting with Chinese lady' (comments/1gbkj16); LJG airport taxi overcharges; and silver/Dongba handicraft counterfeits. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I visit Lijiang's Yulong Snow Mountain safely and affordably?",
         "Self-guided total cost ~¥440 per person vs hotel-concierge packages at ¥500–¥1,200. Breakdown: (1) shared taxi or bus Lijiang Old Town to Yulong Snow Mountain gate ¥80 per person; (2) entry ticket ¥100 (book via official WeChat '玉龙雪山' mini-program or Trip.com); (3) big cable car to 4,506m Glacier Park ¥180; (4) eco bus ¥50; (5) oxygen can rental ¥30 (recommended for altitude). r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025) confirms the Yunnan tour-scam context — avoid any hotel-lobby packages. Arrive early morning (first cable car 8 AM) to beat altitude sickness and tour-group crowds. Consider altitude medication if you're over 60 or have heart conditions — the 4,506m elevation is significant."),
        ("How do I experience authentic Naxi culture without getting overcharged?",
         "Free and genuine options: (1) Dongba Cultural Museum ¥30 entry — genuine Naxi pictographic script, posted exhibitions with English context; (2) Naxi Ancient Music concert at Naxi Music Hall in Old Town — Master Xuan Ke's orchestra, ¥150–¥280 direct ticket (a legitimate artistic lineage, not a commercial tourist show); (3) Sifang Square and Black Dragon Pool host free public Naxi music and dance performances; (4) for genuine Naxi cuisine, walk to Baisha Village (the traditional Naxi village north of Lijiang Old Town) — residential restaurants at ¥40–¥80 per person. SKIP hotel-concierge 'Naxi cultural experience' packages at ¥600+ per person — all are commission-driven with staged performances. Buy Dongba script items at the Dongba Cultural Research Institute gift shop (posted prices, certified)."),
        ("Should I go on a Tiger Leaping Gorge / Shangri-La day trip?",
         "If yes, self-guide rather than hotel-package. Tiger Leaping Gorge upper viewpoint day trip: Lijiang local bus ¥35 (2h each way) + entry ¥45 per person = ¥80 self-guided vs ¥400+ package. For Shangri-La, the Lijiang-Shangri-La bus is ¥80 per person (4h) one-way — stay overnight at Shangri-La Old Town (accommodation ¥300–¥700/night via Booking.com) rather than cramming Shangri-La into a day trip. SKIP hotel-concierge multi-day Yunnan tours at ¥600–¥1,500 per person — r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025) confirms these are guaranteed shopping-stop scams with 4+ hours daily at jade/silver/Pu'er commission venues."),
        ("How do I get from Lijiang airport (LJG) to the Old Town?",
         "Three options: (1) Airport Shuttle Bus LJG to Lijiang Railway Station ¥25 per person, 45 min — then Metro Line 1 or taxi ¥25 to Old Town; (2) DiDi with international-number sign-up at the official rideshare pickup zone — app-regulated fare ~¥90–¥120; (3) licensed taxi with 'da biao' (打表), expect ¥80–¥120 to Old Town. AVOID drivers approaching inside the terminal with 'fixed price' quotes of ¥250+ per r/travelchina 'Taxi drivers in China airports' (comments/1ks12o9, 2025). Photograph taxi plate number from rear windscreen before boarding. For Lijiang-Dali or Lijiang-Kunming, use the high-speed rail from Lijiang Railway Station (Lijiang-Kunming ¥220, 3.5h; Lijiang-Dali ¥50, 2h)."),
    ],
    "Yangshuo": [
        ("Is Yangshuo safe for tourists?",
         "Yangshuo is generally safe during daytime — violent crime is rare, and the rural karst landscape makes it a beloved independent-traveler destination. However, West Street after 10 PM has a documented scam density per r/chinatravel 'Traveling to China - What I learned' (comments/1fjwbtc, 2024): 'in some rural areas (we went to Yangshuo) they tried to scam us a lot even tho we travelled with a Chinese friend.' The practical risks: West Street bar touts and drink-spiking; Yulong River bamboo-raft tourist-price flips; cormorant-photo-tout scams on Li River cruise; Impression Liu Sanjie show ticket overcharges; tourist-strip beer-fish restaurant overcharges; and bike rental damage-dispute scams. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I do the Yulong River bamboo-raft trip without getting scammed?",
         "Book via your Yangshuo guesthouse with posted prices: ¥150–¥200 per 2-person raft for the full 90-minute Yulong Qiao to Gongnong Qiao route. AVOID West Street touts offering 'discount raft ¥80' — these deliver 30 min in a stagnant backwater and often demand additional 'tipping' during the ride per r/chinatravel 'Traveling to China - What I learned' (comments/1fjwbtc, 2024). Depart from the official Yulong Qiao raft dock only. The fair rate doesn't change at sunset — 'sunset private raft' at ¥500+ is markup. On the Li River cruise (Guilin to Yangshuo), decline cormorant-fisherman photo requests — the fisherman with straw hat and two cormorants is staged for tourist photos at ¥20–¥50 per shot; if you want the photo, ¥10 is fair."),
        ("How do I book the Impression Liu Sanjie show affordably?",
         "Book tickets directly via the official show website (liusanjie.net) or Trip.com / Ctrip at published rates: 'A' seat ¥280, 'B' seat ¥220, 'VIP' section ¥400–¥680 depending on seat location. The 70-minute outdoor Zhang Yimou-directed show features 600+ performers on the Li River and runs nightly at 7:45 PM (plus a 9:20 PM second show on weekends/holidays). AVOID hotel-concierge packages at ¥500–¥1,200 per person — all are commission markups. Get to the venue via Yangshuo local bus from West Street (¥3, 15 min). Dress warmly (outdoor riverside seating) and bring insect repellent for summer shows. Arrive 30 minutes early for best seat selection within your ticket category."),
        ("How do I avoid West Street bar scams in Yangshuo?",
         "West Street after 10 PM has aggressive tout-driven bar scams: 'free entry, free first drink' invitations lead to ¥2,000–¥6,000 bills with drinks at ¥300+ each. r/travelchina 'Did I nearly get scammed?' (comments/1n4pjbk, 2025) applies the universal 2025 bar-price anchor — a Qingdao beer should be ¥6–¥30 residential, not ¥300+. Defences: (1) eat and drink before 10 PM at Dianping-verified venues (4.5+ ratings reliable); (2) reject ALL tout 'free entry' invitations; (3) for genuine local bar experience, ask your guesthouse for recommendations one street OFF West Street where locals drink at fair prices; (4) never leave a drink unattended — drink-spiking incidents documented in 2024–2025; (5) hotel bar at your accommodation is the safest option; (6) if drugging suspected, call 110 immediately."),
        ("Where should I eat beer fish in Yangshuo?",
         "Community-vetted authentic venues (all one block off West Street for honest pricing): Fang Weng (small family-run, ¥80–¥120 per 2-person beer fish, ¥40–¥60 per vegetable side), Cloud 9 (mid-tier with posted prices, ¥120–¥180 per 2-person), Lucy's Kitchen (Yangshuo institution, ¥150–¥220). AVOID West Street restaurants with English-speaking touts outside and laminated English-photo menus — the same beer fish costs ¥250–¥450 at 2–3x pricing. Ask your guesthouse for residential recommendations or walk into any restaurant that's full of Chinese diners (the quality signal). Book via the Dianping app (Chinese Yelp) with 4.5+ ratings. For genuine Yangshuo cuisine beyond beer fish, try stuffed Yangshuo snail (tianluo) and pipiwang (steamed river fish)."),
    ],
    "Guangzhou": [
        ("Is Guangzhou safe for tourists?",
         "Guangzhou is generally safe from violent crime — foreigners are rarely targeted. However, Guangzhou has China's most-complained-about taxi-scam density per r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025): '99% of the time I don't get scammed in Shenzhen taxis. 99% of the time I DO get scammed in Guangzhou taxis.' Beyond taxi and counterfeit-bill scams (r/guangzhou comments/8bb5gs), the practical risks are: Canton Fair hostess-bar / contract-dinner scams; Huacheng Plaza and Shamian Island tea-house / art-student scams; Beijing Road and Shangxiajiu fake-goods bait-and-switch; Shamian Island dim sum tourist-menu overcharging. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I get from Guangzhou airport (CAN) safely?",
         "Metro Line 3 runs from CAN to Tiyu Xilu (central Guangzhou) for ¥6–¥8 in 60 min — scam-proof. DiDi with international-number sign-up works at the official rideshare pickup zone. If licensed taxi, 'da biao' (打表) and expect ¥140–¥180 CAN-to-centre. NEVER accept a driver approaching inside the terminal with 'fixed price' quotes of ¥300+. r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) and r/guangzhou 'What are some common scams in Guangzhou' (comments/8bb5gs) both warn about Guangzhou's particularly aggressive airport taxi touts. Photograph the taxi plate number from the rear windscreen before boarding."),
        ("How do I avoid counterfeit-bill scams in Guangzhou?",
         "The scam: driver, vendor, or market stall claims a ¥100 note you handed over is 'counterfeit' and offers to 'replace' it — the note you receive back is actually counterfeit. r/guangzhou 'What are some common scams in Guangzhou dealt with' (comments/8bb5gs) is blunt: 'Taxi scam is by far the most prevalent. Either not running the meter, or slipping you bad bills.' Defences: (1) pay by Alipay or WeChat Pay where possible (cashless payments eliminate the scam exposure); (2) if paying cash, examine each ¥100 for the watermark (Mao portrait visible when held up), color-shifting ink on the '100,' and raised-ink texture on Mao's portrait BEFORE handing over; (3) NEVER accept a 'replacement' bill — keep the note and take it to a Bank of China branch for verification; (4) withdraw cash only from ICBC, Bank of China, China Construction Bank, ABC ATMs — no counterfeit bills from bank machines."),
        ("Should I attend Canton Fair or do business in Guangzhou?",
         "If yes, apply defensive posture to dinners and social events: (1) NEVER let a business contact or stranger choose the venue — insist on a hotel restaurant or Dianping-verified 4.5+ venue; (2) look up expected prices (residential beer ¥15–¥30, hotel bar ¥40–¥80; above ¥150 signals tourist-pricing scam venue per r/travelchina 'Did I nearly get scammed?' comments/1n4pjbk, 2025); (3) set a hard spending limit before any business dinner; (4) pay with credit card for chargeback leverage; (5) if trapped with a ¥10,000+ bill at a hostess bar or 'contract dinner,' refuse to pay more than reasonable consumption and call 110 — Guangzhou police have become more responsive to Canton Fair fraud complaints in 2024–2025."),
        ("Where should I eat dim sum in Guangzhou without getting overcharged?",
         "Community-vetted dim sum venues: (1) Lin Heung Tea House Guangzhou branch (1889 Hong Kong brand, dim sum ¥15–¥35 per basket); (2) Tao Heung (multiple Guangzhou branches, ¥80–¥120 per person); (3) Dim Sum Icon (modern upscale, ¥150–¥200); (4) Panxi Restaurant (Liwan Park institution, ¥120–¥250 per person — legitimate tourist-worthy); (5) Banxi Restaurant (historical with posted prices). AVOID Shamian Island and Beijing Road tourist-strip dim sum at ¥200–¥450 per person for same items at 2–3x pricing. Book via Dianping (Chinese Yelp, 4.5+ ratings reliable) or your hotel concierge at residential venues. For authentic Cantonese experience, eat breakfast dim sum (7–11 AM) when local Cantonese traditionally dine — prices are usually 20–30% lower than evening."),
    ],
    "Kunming": [
        ("Is Kunming safe for tourists?",
         "Kunming is generally safe — violent crime against foreigners is very rare, and the city is a comfortable Yunnan gateway. The practical risks are tour-related: Yunnan tour packages at ¥600–¥1,500 per person for 7 days are guaranteed forced-shopping scams per r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025); Stone Forest (Shilin) hotel-concierge day-trip overcharges; KMG airport and Railway Station taxi overcharges per r/travelchina (comments/1ks12o9, 2025); Pu'er tea plantation shopping scams and Yunnan TCM clinic fraud per r/China (comments/1hfcgv5, 2024); Cuihu Park tea-house scam (the Kunming variant of the nationwide tea-scam ring); and Kundu Bar Street dating-app bar traps. Save 12315 (English consumer complaints) and 110 (police)."),
        ("Should I book a Yunnan tour package from Kunming?",
         "ONLY if you pay ¥3,500–¥6,000+ per person for a 5–7 day licensed tour with 'ZERO shopping stops' verified in writing. SKIP all-inclusive Yunnan tours at ¥600–¥1,500 per person — r/chinatravel 'Is Yunnan suitable for non Mandarin speakers?' (comments/1o2bop0, 2025) is blunt: 'if you go for a tour with reasonable price it should be ok' — meaning cheap tours are guaranteed scams with 4+ hours daily of forced shopping at jade, Tibetan medicine, Pu'er tea, silver jewelry, and 'ethnic minority village' commission venues. Alternatively, self-guide: Kunming-Dali train ¥140 (4h), Dali-Lijiang bus ¥50 (2h), Lijiang-Shangri-La bus ¥80 (4h) — total transport ~¥270 per person plus accommodation ¥300–¥700/night. r/chinatravel (comments/1o2bp2j, 2025) confirms self-guided works: 'Still used didi to' navigate."),
        ("How do I visit Stone Forest (Shilin) without tour-package markup?",
         "Self-guided: take the Kunming-Shilin bus from Kunming East Bus Station (¥25 one-way, 90 min) or the 9-56 train from Kunming Railway Station (¥30 one-way, 70 min). Entry ticket is ¥130 peak season / ¥95 off-season at the gate or via Trip.com. Electric shuttle within the park is ¥20 one-way (optional). Total self-guided day: ~¥230 per person all-in vs hotel-concierge packages at ¥400–¥800 per person. Hotel packages ALWAYS include commission-driven stops at silver jewelry workshops, 'Yi ethnic minority village' shopping venues, or jade 'museums' per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024)."),
        ("How do I buy genuine Pu'er tea?",
         "Buy at Kunming Flower Market or Xiangyun Flower Market — authentic vendors with posted prices: ¥80–¥800 per 357g cake for 'young' Pu'er (recent harvest), ¥500–¥3,000 for genuinely aged (5–15 years). For truly aged (20+ years), prices rise significantly but so does counterfeit risk; Taobao.com with CNY card access for verified aged Pu'er from authenticated producers is the safer option. NEVER buy from 'Pu'er plantation tour' stops — all are commission-driven with opaque provenance and prices at ¥3,000–¥15,000 per cake (5–10x market). Verify production-year seals and producer stamps on aged Pu'er cakes. r/travelchina 'I never knew I would get scammed in China' (comments/1cxb3pv, 2024) documents the Yunnan tea-tour shopping ecosystem."),
        ("How do I get from Kunming airport (KMG) to the city?",
         "Metro Line 6 runs from KMG (Changshui Airport) to central Kunming for ¥6–¥9 in 45 minutes — the scam-proof default. DiDi with international-number sign-up works at the official rideshare pickup zone. If licensed taxi, 'da biao' (打表) and expect ¥90–¥130 KMG-to-centre on meter. AVOID drivers approaching inside the terminal — r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) applies the 2025 China-wide rule. For Kunming-Dali and Kunming-Lijiang onward transit, use the high-speed rail from Kunming Railway Station or Kunming South Railway Station — walking past taxi touts at the station arrivals hall to reach Metro Line 3 (¥3) for intra-city connections."),
    ],
    "Hangzhou": [
        ("Is Hangzhou safe for tourists?",
         "Hangzhou is generally very safe for tourists — violent crime against foreigners is extremely rare, and the West Lake core is well-policed. The practical risks are financial scams concentrated at West Lake and tourist routes: the West Lake teahouse scam (THE canonical China tea-scam anchor per r/travelchina 'A local guide's advice' comments/1qgbdzg, 2025); Longjing Village tea-plantation shopping tours with counterfeit-tea pricing per r/tea 'Understanding the Real Cost of Longjing Tea' (comments/1juy7mf, 2025); HGH airport and Hangzhou East Railway Station taxi overcharges; West Lake boat 'upgrade' and photo-trap scams; QR-code payment-diversion per r/chinalife (comments/1ds004e, 2024); and Hefang Street tourist-menu restaurant overcharging. Save 12315 (English consumer complaints) and 110 (police)."),
        ("What is the most common Hangzhou scam in 2025?",
         "The West Lake teahouse scam tops the list — fluent-English strangers on West Lake walking paths invite tourists to 'traditional Hangzhou tea ceremony featuring Longjing,' bill arrives at ¥3,000–¥10,000, door locks. r/travelchina 'A local guide's advice on avoiding the 3 biggest tourist' (comments/1qgbdzg, 2025) places tea scams as Hangzhou's #1 tourist risk. Longjing Village tea-plantation shopping tours with counterfeit-tea pricing (¥1,500–¥4,000 per 250g for non-protected-origin tea) are second most common per r/tea 'Understanding the Real Cost of Longjing Tea' (comments/1juy7mf, 2025). HGH airport/taxi overcharges, West Lake boat 'upgrade' scams, QR-code payment diversion, and Hefang Street tourist-menu restaurants round out the top six."),
        ("How do I buy genuine Longjing tea?",
         "Authentic Xihu Longjing (West Lake Dragon Well) is a protected-geographic-indicator tea strictly limited to a specific area around West Lake. Legitimate sources: (1) Meijiawu Tea Village's official Longjing Tea Research Institute visitor centre — posted prices ¥200–¥600 per 250g for genuine protected-origin tea; (2) Hangzhou National Tea Museum gift shop — certified products; (3) Taobao.com with CNY-linked card for verified Xihu Longjing from named producers (¥300–¥800 per 250g). r/tea 'Grandmother brought this back from China for me, says it's' (comments/1q0srv6, 2025) confirms authentic Xihu Longjing bears an official protected-origin seal. Reject any tea at ¥2,000+ per 250g without this seal — it's either counterfeit or generic Zhejiang green tea being sold at 10–50x market price per r/tea '\"Fake\" Xihu longjing tea?' (comments/3nxih8)."),
        ("How do I get from Hangzhou airport (HGH) to the city?",
         "Metro Line 19 connects HGH directly to central Hangzhou — transfer to Line 1 at Jianshe Sanlu and continue to West Lake (Long Xiangqiao station) for ¥8–¥12 total, ~60 minutes. The Airport Bus runs to Wulin Square (city centre) for ¥20, 60 min. DiDi with international-number sign-up works at the official rideshare pickup zone. If licensed taxi, 'da biao' (打表) and expect ¥130–¥170 HGH-to-West-Lake on meter. r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) warns about terminal-door taxi touts quoting ¥250+ fixed prices. For Shanghai-Hangzhou connection, the Shanghai Hongqiao-to-Hangzhou East high-speed rail is ¥73 (45 min)."),
        ("Where should I stay and eat in Hangzhou?",
         "For accommodation near West Lake: Fuchun Resort (luxury on Yangtze), Four Seasons Hotel Hangzhou at West Lake (1930s mansion), Amanfayun (near Lingyin Temple), Westin Xihu, Hyatt Regency Hangzhou — all book via Booking.com / Trip.com. Mid-range: Lakeside Cozy Hotel, West Lake No. 8 Hotel. For food, community favourites on or near West Lake: Lou Wai Lou (West Lake landmark restaurant, Dongpo pork ¥150–¥250 per person — legitimate tourist institution), Zhi Wei Guan (Hangzhou cuisine specialist, ¥80–¥150), Wai Po Jia / Grandma's Home (Chinese chain ¥60–¥100). Avoid Hefang Street tourist restaurants (2x–3x residential rates). For tea ceremonies without scam risk, book via hotel concierge at a published-price venue rather than accepting a stranger's invitation."),
    ],
    "Suzhou": [
        ("Is Suzhou safe for tourists?",
         "Suzhou is generally very safe for tourists — violent crime against foreigners is extremely rare, and the garden-heavy tourist core is walkable and well-policed. The practical risks are financial: silk factory 'tour' high-pressure sales per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024); Classical Gardens fake-ticket and skip-the-line overcharges; Pingjiang Road tea-house scam (the Suzhou regional variant of the nationwide tea-scam ring); rickshaw/pedicab price flips; Shanghai-to-Suzhou day-trip hotel-concierge package markups. Save 12315 (English consumer complaints) and 110 (police). r/travelchina 'Planning a trip to Suzhou? OMG, you HAVE to do the' (comments/1kyyehv, 2025) is the 2025 community guide."),
        ("How do I do a Shanghai-to-Suzhou day trip without getting scammed?",
         "The self-guided option costs ¥250–¥350 per person vs ¥600+ hotel-concierge packages. Step-by-step: (1) book high-speed rail (Shanghai Hongqiao to Suzhou Station) via Trip.com or 12306.cn — ¥40 one-way, 25 min; (2) at Suzhou Station, take Metro Line 2 (¥4) to Beisita (North Temple Pagoda) station near Humble Administrator's Garden; (3) book Humble Administrator's Garden entry (¥80) via WeChat mini-program '拙政园' 1 day ahead; (4) walk 10 min to Lion Grove Garden (¥40) and 15 min to Pingjiang Road for lunch; (5) return via Suzhou Railway Station to Hongqiao (¥40, 25 min). r/travelchina 'Many people visit Suzhou as a day trip from Shanghai, but' (comments/1kwbyaa, 2025) is the 2025 named community guide. AVOID hotel concierge packages — all include silk-factory shopping stops per r/China (comments/1hfcgv5, 2024)."),
        ("How do I visit Suzhou's Classical Gardens without getting overcharged?",
         "Official entry fees (book 1 day ahead via WeChat mini-programs): Humble Administrator's Garden (Zhuozheng Yuan, 拙政园) ¥80 peak / ¥70 off; Lingering Garden (Liu Yuan, 留园) ¥55/¥45; Master of the Nets (Wangshi Yuan, 网师园) ¥40; Lion Grove (Shizi Lin, 狮子林) ¥40; Suzhou Museum — free but requires advance WeChat booking 1–7 days ahead. The Suzhou Garden Pass combo covering 4 main gardens is ¥150–¥200 via Trip.com — good value if you plan to visit all four. AVOID third-party 'skip-the-line' tickets at ¥200–¥400 per garden — r/travelchina 'Planning a trip to Suzhou' (comments/1kyyehv, 2025) confirms official booking is reliable. Audio guides at each garden's entrance rent for ¥30 per device — cheaper and more flexible than paid guided tours."),
        ("Should I go on a Suzhou silk factory tour?",
         "No. Suzhou's 'silk factory tours' are the canonical example of China's 'government museum' shopping-tour scam per r/China 'Government facilities in travel tour scams? (Jade, TCM)' (comments/1hfcgv5, 2024). A 10-minute 'demonstration' is followed by 60–90 minutes of high-pressure sales — silk quilts at ¥3,000–¥15,000 that retail ¥500–¥900 on Taobao for genuine Jiangsu silk. If you want genuine Suzhou silk: (1) Suzhou Silk Museum (Renmin Road) has a legitimate educational experience with posted gift-shop prices; (2) Matro and New World department stores in Suzhou sell silk at mall rates; (3) Taobao.com with CNY card access for 1/3 to 1/10 the 'factory tour' prices. Reject ANY hotel-concierge 'silk factory' addition to day-trip itineraries."),
        ("Where should I eat in Suzhou without tourist-strip overcharging?",
         "Pingjiang Road and Guanqian Street have the highest tourist-menu markup in Suzhou. Walk one block off to find residential restaurants. Community favourites: Songhelou (Guanqian Street but historical 1757 institution with posted prices — squirrel-shaped mandarin fish ¥120–¥180), Wumen Renjia (Pingjiang area but authentic — noodles ¥15–¥30), Zhu Hong Xing (multiple residential branches — noodles and dumplings ¥20–¥50), Xin Mei Hua (dim sum and local cuisine ¥40–¥80 per person). For Biluochun tea, skip Pingjiang Road tea-house invitations — visit Dongshan Biluochun Tea Village by bus (¥10, 90 min) for genuine plantation experience with posted prices. Book via the Dianping app (Chinese Yelp); 4.5+ ratings are reliable."),
    ],
    "Macau": [
        ("Is Macau safe for tourists?",
         "Macau is one of Asia's safest cities for tourists — violent crime against foreigners is extremely rare, and the casino-heavy economy produces above-average policing. The practical risks: (1) 'black taxi' overcharges at Outer Harbour Ferry Terminal, Taipa Ferry Terminal, and MFM airport per r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025); (2) casino VIP-room / junket private-game scams (rigged games, credit-marker traps); (3) Senado Square tourist-menu restaurant overcharging; (4) unlicensed currency-exchange booths with counterfeit-note risk; (5) fake Macau Airbnb/hotel listings without MGTO licence; (6) opportunistic pickpockets at Ruins of St. Paul's and A-Ma Temple. Save Macau Judiciary Police (PJ) +853 2855 7111, emergency 999."),
        ("How do I get around Macau without getting scammed by taxis?",
         "Macau has excellent free casino shuttle buses — Venetian, Galaxy, Wynn, MGM, City of Dreams, Parisian ALL run free shuttle buses connecting their properties to every ferry terminal and MFM airport, even if you're not staying at that casino. The Macau Light Rapid Transit (LRT) connects Taipa Ferry Terminal to the Cotai casino district for MOP$6 (15 min). If you must take a taxi, walk to the official outdoor rank (black and yellow cabs); say 'da biao' (打表); legitimate meter fares are MOP$50–$80 Outer Harbour-to-Senado, MOP$80–$120 Outer Harbour-to-Cotai, MOP$60–$100 MFM-to-Cotai. Pay in MOP (not HKD — the actual rate is 1 HKD = 1.03 MOP, not 1:1). AVOID any driver soliciting rides inside or just outside terminal doors."),
        ("Should I gamble at Macau casinos? How do I avoid VIP-room scams?",
         "Play ONLY on licensed main gaming floors: Venetian Piazza, Galaxy, Wynn, MGM, City of Dreams, Parisian — all are DICJ-licensed (Macau Gaming Inspection and Coordination Bureau) with published house rules. NEVER accept a 'private room' or 'VIP' introduction from a hotel host, casino staffer, or 'helpful local' — the VIP system exists for high rollers bringing millions, not tourists, and unlicensed junket operators have been documented for rigged games and predatory credit-marker scams. Decline ALL credit-marker offers; pay only in cash or certified chips. Set a hard gambling budget before entering the casino floor and stop at the limit. If threatened or intimidated over gambling debts, contact Macau Judiciary Police (PJ) at +853 2855 7111 or your consulate immediately."),
        ("Where should I eat authentic Macanese food without tourist-strip overcharging?",
         "Skip Senado Square, Rua da Felicidade, and the Ruins of St. Paul's approach for food — all 2–3x residential rates with laminated English-photo menus. Take the Macau public bus (MOP$6 flat fare) to Taipa Village and Coloane Village for authentic Macanese: (1) Lord Stow's Bakery (Coloane) — the original Portuguese egg tart at MOP$10; (2) Tai Lei Loi Kei (Taipa Village) — legendary pork-chop bun at MOP$45; (3) Fernando's (Hac Sa Beach, Coloane) — landmark Portuguese-Macanese at MOP$150–$300 per person; (4) Restaurante Litoral (Taipa) — mid-range authentic Macanese. Bus 22, 26A, 28A from Senado serve Taipa Village; Bus 15, 21A, 25 serve Coloane. For egg tarts specifically, Margaret's Café e Nata at Grand Lisboa is the other authentic hand-baked option in downtown Macau."),
        ("How do I book accommodation in Macau safely?",
         "Book only MGTO-licensed hotels via Booking.com, Agoda, or Trip.com. Verify the hotel appears on the MGTO Registered Hotels list at macaotourism.gov.mo — every licensed Macau hotel has a visible MGTO registration number. Major legitimate hotels: Venetian, Galaxy, Wynn, MGM, City of Dreams, Grand Lisboa Palace, Sheraton Grand, Banyan Tree, St. Regis (all Cotai or Peninsula). For budget stays, 3-star Cotai or Peninsula guesthouses via Booking/Agoda are also MGTO-licensed. AVOID Airbnb listings and Facebook/WeChat-referred private rentals without an MGTO number — unlicensed short-term rentals are illegal in Macau and guests can be required to leave if authorities inspect. If defrauded on arrival, contact Macau Tourism Crisis Management Office: +853 2833 3000."),
    ],
    "Guilin": [
        ("Is Guilin safe for tourists?",
         "Guilin is generally safe — violent crime against foreigners is very rare, and the scenic core is walkable. The practical risks are financial scams: Li River cruise hotel-lobby package overcharges per r/China 'Common scams you should know' (comments/2aqq6l); Yangshuo bamboo-raft and cormorant-photo trap scams per r/chinatravel 'Traveling to China' (comments/1fjwbtc, 2024); Guilin Airport (KWL) and Railway Station taxi overcharges; Elephant Trunk Hill / Seven Star Park tea-house invitations (the regional variant of the nationwide tea-scam ring); Longji Rice Terraces hotel-concierge day-trip markups; Zhengyang Pedestrian Street tourist-menu restaurant overcharging; and hotel-concierge 'all-inclusive' tour commissions. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I book the Li River cruise without getting scammed?",
         "Book the standard 4-hour Li River cruise (Guilin to Yangshuo) via Trip.com, Viator, or Ctrip at ¥215–¥310 per person. Avoid hotel-lobby 'Li River cruise package' at ¥500+ per person — all are commission markups. The cruise departs from Magu Pier (40 km south of Guilin); pre-arranged transfer bus is ¥50–¥80 per person shared. At Yangshuo arrival, pre-book your hotel pickup rather than accepting touts at the dock. AVOID any 'all-in-one Guilin + Yangshuo tour' under ¥600 per person — these include 'jade museum,' 'silk factory,' or 'tea ceremony' shopping stops per r/travelchina 'Are tours in China still sketchy' (comments/1k85j1d, 2025)."),
        ("What is the best way to see Yangshuo without scams?",
         "Take the Li River cruise one-way from Magu Pier to Yangshuo (¥215), then spend 1–2 nights in Yangshuo itself. Book guesthouses directly via Booking.com / Agoda / Ctrip (¥150–¥400/night). Yulong River bamboo-raft trip: ¥150–¥200 per 2-person raft for a 90-minute route — book via your guesthouse, NOT West Street touts. Skip 'cormorant fishing shows' — they are staged performances. Walk one block off West Street for honest food. r/chinatravel 'Traveling to China - What I learned' (comments/1fjwbtc, 2024) warns about Yangshuo rural-scam density: 'in some rural areas (we went to Yangshuo) they tried to scam us a lot even tho we travelled with a Chinese friend.' Return to Guilin via ¥25 bus (1.5h) or taxi with 'da biao' (~¥300)."),
        ("How do I visit Longji Rice Terraces safely and affordably?",
         "Book a 1-night guesthouse at Ping'an Zhuang or Dazhai Yao village directly via Ctrip / Trip.com / Booking.com (¥300–¥600 per room). Take bus from Guilin Qintan Bus Station to Longji for ¥25 (2.5h). Longji entrance ticket is ¥80 at the gate. Total self-guided overnight is ~¥400 per person all-in — vs hotel-concierge day-trip packages at ¥400–¥800 per person that include 'Miao long-hair show' (staged for tourists) and 'hand-loom demonstrations' with forced ¥200–¥500 scarf purchases. Skip the cultural shows and focus on walking the terrace trails at sunrise. r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024) documents the ethnic-minority tour shopping-stop pattern."),
        ("Where should I eat in Guilin without tourist-strip overcharging?",
         "Walk one block off Zhengyang Pedestrian Street for honest Guilin rice noodles (¥8–¥15 per bowl, vs ¥30–¥50 at tourist strip). Community favourites: Chong Shan Rice Noodle (¥10), Yi Cun Yi Wei (¥12). For beer fish (Yangshuo specialty), wait until Yangshuo and eat at a residential restaurant for ¥80–¥150 rather than the Guilin tourist-strip ¥180–¥300 version. Skip night-market stalls with English signs — the same dishes at 2–3x price. Any restaurant with an English-speaking tout outside is targeting tourists; walk past to the restaurants one street back with Chinese-only menus."),
    ],
    "Shenzhen": [
        ("Is Shenzhen safe for tourists?",
         "Shenzhen is one of China's safest major cities. r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025) captures the community view: '99% of the time I don't get scammed in Shenzhen taxis' — meaning licensed metered taxis are reliable IF you avoid terminal-door touts. The practical risks for older travelers: Luohu border crossing fake-taxi touts; Huaqiangbei electronics market counterfeit and bait-and-switch per r/chinalife 'I've learned about these two scams in China in 2024' (comments/1ds004e); SZX airport black-taxi and meter-tampering per r/shanghai (comments/1owloe6, 2025); Dongmen pedestrian opportunistic pickpockets; unlicensed HKD↔CNY exchange at Luohu Commercial City; and massage/spa/TCM 'clinic' overcharges recommended by taxi drivers or concierges. Save 12315 (English consumer complaints) and 110 (police)."),
        ("How do I cross the Luohu border without getting scammed?",
         "Take Shenzhen Metro Line 1 directly from the Luohu Station inside the border building. Line 1 to Futian East is ¥3 (7 min) and to Shekou is ¥8 (45 min) — the scam-free default. AVOID unlicensed drivers soliciting outside the border building. If you need a taxi, walk to the official outdoor rank (not the border-door area), say 'da biao' (打表), and expect ¥25–¥45 on the meter to central Shenzhen. Install DiDi before crossing for app-regulated fares with digital receipts. r/China 'Did I just get scammed real bad by an \"official\" taxi' (comments/1oo4dpl, 2025) gives the nuanced view: Shenzhen licensed taxis are among China's most reliable, but only if you reach the official rank."),
        ("Should I shop for electronics at Huaqiangbei?",
         "Treat Huaqiangbei as window-shopping only — assume everything is counterfeit unless from a name-brand authorised retailer. The common scams: 'Apple AirPods' at ¥150 (genuine retail ¥1,299), iPhone 'refurbished' at ¥2,000 (actually Android with cloned iOS skin), 'GoPro' clones at ¥400 (unbranded action cameras). For genuine electronics in Shenzhen, visit Apple Store (MixC Mall), Xiaomi flagship (Coco Park), Huawei flagship (COCO Park) — all authorised retailers with posted pricing and warranties. r/chinalife 'I've learned about these two scams in China in 2024' (comments/1ds004e, 2024) warns: 'anything expensive you buy that has a lot of options is potentially a sc' am — and bringing counterfeit Apple/Sony/Bose products home is illegal in the US, UK, EU, Canada, and Australia, with customs confiscation risk."),
        ("How do I get from SZX airport to central Shenzhen safely?",
         "Metro Line 11 runs from SZX (Shenzhen Bao'an) to Futian for ¥7–¥12 in 45 minutes — the scam-free default. DiDi with international-number sign-up operates at the official rideshare pickup zone for app-regulated fares. If licensed taxi, walk past solicitors inside the terminal to the official outdoor rank, say 'da biao' (打表), and expect ¥150–¥200 on the meter. Screenshot a DiDi fare estimate before boarding any taxi. Unofficial drivers at arrivals quote ¥300–¥500 'fixed prices' — r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) confirms the universal rule. Don't accept anyone approaching inside the terminal."),
        ("Where should I exchange currency at the Hong Kong / Shenzhen border?",
         "Use licensed banks: Bank of China, HSBC, Standard Chartered, or Wing Lung licensed money-changers — all have visible branded signs and posted rates. Alternatively, use a multi-currency card (Wise, Revolut, Payoneer) at a Bank of China ATM for ~1% forex margin. AVOID Luohu Commercial City unlicensed exchange booths — they charge 3–8% above the posted rate and sometimes slip counterfeit ¥100 notes among the currency. r/China 'Common scams you should know' (comments/2aqq6l) documents the counterfeit-bill variant: 'vendors receiving an RMB 50 or RMB 100 bill from you, telling you it's a fake and asking' you to exchange for a 'better' note. Hotel-concierge 'friendly rate' offers are always 3–5% worse than licensed banks — decline."),
    ],
    "Beijing": [
        ("Is Beijing safe for tourists?",
         "Beijing is generally very safe for tourists — violent crime against foreigners is extremely rare. The practical risks are financial scams concentrated in four tourist zones: Wangfujing, Tiananmen/Qianmen, Forbidden City approach, and Sanlitun. Most documented scams: art-student gallery trap (r/travelchina 'Beijing Art Teacher Scam' comments/1fa4xwf, 2024), Wangfujing tea-house scam (r/shanghai 'Teahouse scam' comments/17cyvmv), Forbidden City trishaw price flips (r/travelchina comments/1gw5c89, 2024), Great Wall 'all-inclusive' shopping tours, Peking duck driver-commission swaps, and Sanlitun Tinder/bar traps. Save 12315 (English consumer complaints) and 110 (police)."),
        ("What is the most common Beijing scam in 2025?",
         "The Wangfujing/Qianmen tea-house scam tops the list — fluent-English strangers invite you to 'traditional tea ceremony,' bill arrives at ¥3,000–¥8,000, door locks. r/travelchina 'Constantly being stopped by scammers in Beijing' (comments/1jnd6na, 2025) documents the 2025 pattern. PEK and PKX airport taxi overcharges are second most common per r/travelchina 'Beijing International Airport taxi scammers' (comments/1o7pp36, 2025). Forbidden City trishaw price flips, Great Wall shopping-stop tours, Peking duck driver-commission restaurants, and Sanlitun dating-app bar traps round out the top six."),
        ("How do I get from Beijing airports to the city safely?",
         "From PEK: Airport Express train ¥25, 25 min to Dongzhimen, every 10 min. From Daxing (PKX): Daxing Airport Express metro line ¥35, 19 min to Caoqiao. For taxis, use the official outdoor rank, say 'da biao' (打表) before boarding. Legitimate PEK-to-centre meter fare ¥90–¥120 (30–40 min); PKX-to-centre ¥140–¥180 (46 km). Install DiDi before arriving — English interface, international-number sign-up, regulated fares with digital receipts. r/travelchina 'Who are all the guys offering rides at the airport?' (comments/1fn0zz1, 2024) warns anyone soliciting inside the terminal is unauthorised."),
        ("How do I visit the Great Wall without getting scammed?",
         "Three scam-free options: (1) S2 suburban train from Huangtudian to Badaling ¥6, 1h15m, every 60 min — cheapest and well-signed in English; (2) Book Mutianyu (less-crowded, cable-car accessible) via Viator, GetYourGuide, or Tiqets — ¥400–¥600 per person with NO shopping stops; (3) For Jinshanling, use Beijing Hikers or similar licensed small-group operators. AVOID hotel-lobby 'all-inclusive' tours under ¥250 — these always include 3–4 jade/tea/silk 'museums' with high-pressure shopping per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024). Always verify ZERO shopping stops in writing."),
        ("Where should I eat Peking duck in Beijing?",
         "Community-verified names: Da Dong (dadongdadong.com, ¥300–¥450 per person — modern), Siji Minfu (four locations, ¥200–¥300 — classic), Quanjude (iconic but tourist-priced ¥400–¥600), Lao Beijing (residential branches ¥150–¥250). NEVER follow a taxi driver, trishaw driver, or street tout's 'famous duck restaurant' recommendation — r/China 'Travel scams in Beijing' (comments/3pbvi9) confirms all pay commission. Gold-lettered English-menu venues near Qianmen are tourist-commission traps at ¥600–¥1,200. Book via Dianping (Chinese Yelp) or restaurant's WeChat mini-program."),
    ],
    "Shanghai": [
        ("Is Shanghai safe for tourists?",
         "Shanghai is one of Asia's safest major cities — violent crime is extremely rare. The practical risks are financial: Pudong (PVG) airport taxi overcharges per r/shanghai 'Taxi fare extra cost scam' (comments/1otjyot, 2025); Nanjing Road / Bund tea-house ring per r/shanghai 'My experience of the Nanjing road scams' (comments/1kmmutc, 2025); Bund wine/champagne bar overcharges per r/shanghai 'Scam attempt on the Bund' (comments/1qp6db5, 2025); Yu Garden tea-ceremony ambushes; Shanghai Disneyland fake-ticket resellers; AP Xinyang 'fake market' bait-and-switch; and PVG SIM-card tout markups. Save 12315 (English consumer complaints) and 110."),
        ("What is the most common Shanghai scam in 2025?",
         "The Nanjing Road teahouse / bar scam tops the list — r/shanghai 'My experience of the Nanjing road scams' (comments/1kmmutc, 2025) is the 28-year-resident anchor, with specific flagged venue '510 Tianjin Road (SMOOTH dining bar)' per r/shanghai (comments/17xh9a7). Pudong airport taxi overcharges are second most common — r/shanghai (comments/1otjyot, 2025) documents 2025 cases even at the official queue. Bund wine/champagne bar overcharge, Yu Garden tea-ceremony ambush, Shanghai Disneyland fake-ticket resellers, AP Xinyang bait-and-switch, and PVG SIM-card tout markups round out the top seven."),
        ("How do I get from Pudong Airport (PVG) to central Shanghai safely?",
         "Three scam-free options: (1) Shanghai Metro Line 2 from PVG (Pudong International Airport station) to People's Square / Nanjing East Road for ¥7 in 90 minutes; (2) DiDi at the official rideshare pickup zone — English interface, international-number sign-up, regulated fares; (3) Licensed taxi with 'da biao' (打表) before boarding, screenshot DiDi fare as reference. Legitimate PVG-to-centre meter fare ¥180–¥220 (45 km, 50–60 min). The Maglev train to Longyang Road (¥50, 8 min) is fastest but r/shanghai 'Taxis to avoid in Pudong Airport' (comments/1csmz6w, 2024) warns the Longyang Road taxi rank has higher scam density than PVG — transfer to Metro Line 2/7 rather than taking a taxi."),
        ("How do I avoid the Nanjing Road tea-house scam?",
         "The rule is absolute: ANY stranger approaching in fluent English near Nanjing Road, People's Square, or the Bund with an invitation to 'tea,' 'cultural experience,' 'traditional ceremony,' 'photo help,' or 'English practice' is running the scam. Walk past with 'bu yao xie xie' (不要谢谢). Do not take photos for strangers who strike up conversation — it is the opening move. Specific flagged address: 510 Tianjin Road (SMOOTH dining bar) per r/shanghai (comments/17xh9a7). For genuine Shanghai tea, visit Huxinting Teahouse inside Yu Garden (the 1855 pavilion, ¥150–¥300 per person). If trapped, pay with credit card (for chargeback), photograph the bill, call 12315. r/shanghai 'Tea house scam part 3: GOT THE MONEY BACK!' (comments/yojc11) documents successful recovery."),
        ("Where should I eat and drink for Bund sunset views without getting overcharged?",
         "Community-verified Bund-area venues with published pricing: M on the Bund (7th floor, mrestaurantgroup.com, dinner ¥600–¥1,000), Bar Rouge (7th floor Bund 18, cocktails ¥120–¥180), Hakkasan (5th floor Bund 18), Waldorf Astoria's Long Bar (Bund 2, cocktails ¥100–¥150), Peace Hotel Jazz Bar (Bund 20, music charge ¥200 plus drinks). All have posted English menus, card payment, digital receipts. NEVER accept a bar recommendation from a stranger on the Bund — r/shanghai 'Scam attempt on the Bund' (comments/1qp6db5, 2025) documents 2025 approaches where the pitch is framed as 'sales commission' but inflated bill is the same outcome."),
    ],
    "Xi'an": [
        ("Is Xi'an safe for tourists?",
         "Xi'an is generally safe — violent crime against tourists is very rare, and the old-city core is walkable and friendly. The practical risks are financial scams: fake Terracotta Army sites on the route to Lintong per r/travelchina 'Don't be scammed in Xi'an' (comments/5nbrg1); Muslim Quarter tourist-menu overcharges and the 'Xinjiang cake' pushcart scam per r/AskChina 'Is it True Xinjiang Hawkers on Street Are Dangerous?' (comments/1q1rphd, 2025); XIY airport taxi overcharges per r/travelchina (comments/1ks12o9, 2025); forced-shopping 'all-inclusive' tour buses per r/China (comments/1hfcgv5, 2024); Bell Tower/Drum Tower opportunistic pickpockets; Tang Dynasty Show hotel-concierge markups; and the Xi'an extension of the Beijing/Shanghai tea-house scam ring. Save 12315 (English consumer complaints) and 110."),
        ("How do I visit the real Terracotta Army without getting scammed?",
         "The real Terracotta Army is at Lintong, 35 km east of Xi'an, operated by Shaanxi Provincial Bureau of Cultural Heritage — official name 'Emperor Qin Shi Huang's Mausoleum Site Museum.' Book entry (¥120 adult) via the official WeChat mini-program 'Qin Shi Huang Di Ling Bowu Yuan' (秦始皇帝陵博物院) or on Trip.com. Take Tourist Bus Line 5 (游5) from Xi'an Railway Station East Plaza — ¥8, 1 hour, every 20 minutes. AVOID any tour under ¥250 per person — r/travelchina 'Don't be scammed in Xi'an in visiting the fake terracotta army' (comments/5nbrg1) documents entire fake 'Terracotta' venues on the route. Verify the destination is 'Emperor Qin Shi Huang's Mausoleum Site Museum' before paying any tour deposit."),
        ("Where should I eat in Xi'an without tourist-strip overcharging?",
         "Walk one street off Beiyuanmen (the Muslim Quarter main street) to find honest prices. r/travelchina 'Xi'an Survival Guide: The Local's Insider Tips' (comments/1r7si9e, 2025) names Yongxing Fang food court (posted prices, showcases Shaanxi cuisine), Lao Sun Jia (1898 institution, yangrou paomo ¥45 per bowl), and Jia San Guantang Baozi (soup dumplings ¥30 per basket). NEVER buy 'Xinjiang cake' from a pushcart vendor — the weighing scam charges ¥2,000+ for a 'small piece.' For modern Xi'an food, the Yongxing Fang complex has 20+ regional specialties with published prices. Confirm 'duo shao qian' (how much) before any vendor starts cutting or serving."),
        ("How do I get from Xi'an Airport (XIY) safely?",
         "Airport Metro Line 14 runs from XIY to Xi'an Railway Station for ¥17 in 70 minutes — scam-proof. Airport shuttle buses to Xi'an Railway Station (¥25, 60 min) and Longhai Hotel (¥30) are the second budget option. For taxis, use the official outdoor rank, say 'da biao' (打表), and expect ¥120–¥160 on the meter. DiDi with international-number sign-up works at XIY — use the official rideshare pickup zone. r/travelchina 'Taxi drivers in China airports and train station' (comments/1ks12o9, 2025) warns 'They are scams and trying to overcharge you. Go straight to the real taxi stand' — walk past anyone soliciting rides inside the terminal. If a stranger at arrivals asks to 'borrow your phone,' it is a scam — never unlock your phone for a stranger."),
        ("How do I book the Tang Dynasty Show and evening entertainment?",
         "Book the Tang Dynasty Show (at the Xi'an Hotel, ¥298 standard / ¥398 VIP / ¥598 dinner+show) directly via the venue's WeChat mini-program or Trip.com / Ctrip. Huaqing Palace evening show 'Song of Everlasting Sorrow' (¥298–¥498) and Tang Paradise water show (¥298–¥398) follow the same booking pattern. IGNORE hotel-concierge 'exclusive' packages over ¥600 per person — all are commission markups. For transportation, Metro Line 2 serves the Tang Paradise area (¥5); Huaqing Palace reached via Lintong tourist bus ¥8 + taxi ¥20. r/travelchina 'How to book Terracotta Warriors tickets on Wechat Xi'an' (comments/1meow6w, 2025) confirms the 2025 WeChat mini-program method applies across Xi'an venue bookings."),
    ],
    "Chengdu": [
        ("Is Chengdu safe for tourists?",
         "Chengdu is generally safe — violent crime against foreigners is very rare, and the city is relaxed and walkable. The practical risks for older travelers are financial: Tianfu (TFU) and Shuangliu (CTU) airport taxi overcharges per r/Chengdu 'Where to pick up DiDi at Tianfu' (comments/1deo34t, 2024); Tibet tour permit fraud per r/singapore 'Singaporean singer recounts ordeal' (comments/1p8r1zn, 2025); Panda Base hotel-concierge tour markups; Kuanzhai Alley and Jinli tea-house scams (the Chengdu variant of the Beijing/Shanghai ring) per r/chinatravel (comments/1nqcbht, 2025); Sichuan hotpot tourist-menu overcharging; forced-shopping 'all-inclusive' bus tours per r/China 'Government facilities in travel tour scams?' (comments/1hfcgv5, 2024); and Jinli/Kuanzhai souvenir markups. Save 12315 (English consumer line) and 110."),
        ("How do I visit the Panda Base without getting scammed?",
         "Book Panda Base entry (¥55 adult) directly via the official WeChat mini-program '成都大熊猫繁育研究基地' or Trip.com / Ctrip. Take Metro Line 3 to Panda Avenue Station (Panda Dadao, ¥4), then shuttle bus #16 to the park entrance. Arrive BEFORE 8:30 AM — pandas are most active 8:30–10:00 AM, and tour-group crowds dominate after 10:00. r/Chengdu 'Panda Base visit' (comments/1md57l8, 2025) is the 2025 community anchor. AVOID hotel-concierge 'Panda Base VIP tour' packages over ¥300 per person — a self-guided visit costs ~¥90 per person including transport. Any offer of 'photo with panda' for adult foreign tourists is a scam — that opportunity is NOT available to visitors at Chengdu Research Base."),
        ("How do I get from Chengdu airports to the city?",
         "From Tianfu (TFU, 50 km): Metro Line 18 to Tianfu Square for ¥9 in 47 minutes — scam-proof. DiDi at official rideshare zone ~¥150. If taxi, 'da biao' and expect ¥180–¥220. From Shuangliu (CTU, 16 km): Metro Line 10 to Taipingyuan for ¥6, 25 min. If taxi, expect ¥80–¥110 on meter. r/Chengdu 'Where to pick up DiDi at Tianfu' (comments/1deo34t, 2024) is blunt: 'Don't go with the guys waving at you at arrivals and asking if you need a taxi, scam city.' Walk past anyone approaching inside either terminal. For older travelers with luggage, DiDi at the official pickup zone is the easiest reliable option."),
        ("Should I book a Tibet tour from Chengdu?",
         "If yes, use ONLY Tibet Travel Permit-licensed operators: Tibet Vista (tibettravel.org), Explore Tibet, Great Tibet Tour, Budget Tibet Tour are community-vetted. Pay via credit card for chargeback leverage — never Bizum, Alipay, or bank transfer. Expect ¥6,000–¥12,000 per person for a 4–8 day Lhasa tour. Reject anything under ¥3,000 — r/singapore 'Singaporean singer recounts ordeal with China tour guide' (comments/1p8r1zn, 2025) documents a named 2025 case where a ¥600–¥800 'Tibet tour' was outright fraud with no permit obtained. Verify your Tibet Travel Permit number via the Tibet Tourism Bureau website before traveling. Confirm written itinerary with ZERO shopping stops and specific named sites."),
        ("Where should I eat Sichuan hotpot without tourist-strip overcharging?",
         "Walk one street off Kuanzhai Alley and Jinli Ancient Street to reach residential-quality venues. r/travelchina 'Chengdu 101: Comprehensive Travel Manual for First' (comments/1rmboro, 2025) names community favourites: Shu Jiu Xiang (¥90–¥130 per person, multiple locations), Huang Cheng Lao Ma (¥120–¥180), Da Long Yi (¥130–¥170, high quality), Xiao Long Kan (¥100–¥140, nationwide chain). Book via the Dianping app (Chinese Yelp) — 4.5+ ratings are reliable. Expect ¥90–¥170 per person at genuine venues; laminated-English-menu tourist-strip hotpot at ¥300+ is an overcharge. For the spiciest authentic experience, order Shu Jiu Xiang with yuanyang (half-spicy half-mild) broth. NEVER follow a tout's 'famous hotpot' recommendation."),
    ],
    "London": [
        ("Is London safe for tourists?",
         "London is generally very safe for tourists, though petty crime like phone theft and pickpocketing is increasing. The areas around major tube stations and Oxford Street have the highest rates. Violent crime targeting tourists is rare. Stay aware of your surroundings, keep devices pocketed, and you'll have no issues."),
        ("What is the most common scam in London?",
         "Mobile phone theft is currently the #1 crime tourists face in London — particularly moped-based snatches near tube exits. Pickpocketing on the Underground, particularly on the Circle and District lines around tourist stops, is also extremely common."),
        ("Are London black cabs safe?",
         "Black cabs (hackney carriages) are one of the safest transport options in London. Drivers undergo 3–4 years of training ('The Knowledge'), are fully licensed, and meters are regulated by law. Avoid unlicensed minicabs, especially those that approach you outside clubs or stations at night."),
        ("What should I do if my phone is stolen in London?",
         "Report it to the Metropolitan Police at met.police.uk or at your nearest police station. Get a crime reference number for insurance. Call your phone provider to block the IMEI. If using Apple or Google, activate remote lock immediately from another device."),
        ("Do I need to tip in London restaurants?",
         "Service charge (usually 12.5%) is often added automatically, which functions as the tip. Check your bill before adding more. You are legally entitled to ask for the service charge to be removed if you received poor service — it is optional regardless of what the menu says."),
    ],
    "Tokyo": [
        ("Is Tokyo safe for tourists?",
         "Tokyo is one of the safest major cities in the world for tourists. Violent crime is extremely rare. The risks are primarily in specific nightlife districts (Roppongi, Kabukicho) and involve scams rather than physical danger. Outside those areas, Tokyo is exceptionally safe even late at night."),
        ("What is the most common scam in Tokyo?",
         "Bottakuri (rip-off) bars in Roppongi and Kabukicho are the most dangerous scam for tourists. They use deceptive pricing, intimidation tactics, and target tourists who wander in after being approached by touts outside. Never enter a bar where someone is actively recruiting customers from the street."),
        ("Are there pickpockets in Tokyo?",
         "Pickpocketing is relatively rare in Tokyo compared to European cities. The main risks are in crowded train stations and at festivals. That said, phone theft has been increasing in entertainment districts. The bigger risks are overcharging and scam bars, not pickpocketing."),
        ("Is it safe to go out at night in Tokyo?",
         "Yes — Tokyo is overwhelmingly safe at night. The main caveat is avoiding Roppongi and Kabukicho if you're not familiar with the area, and specifically not entering venues at the suggestion of street touts. Most neighborhoods, including Shinjuku, Shibuya, and Shimokitazawa, are perfectly safe for solo travelers at any hour."),
        ("Do I need to negotiate taxi prices in Tokyo?",
         "No — Tokyo taxis are metered and generally honest. The Go taxi app provides pre-set fares. Metered taxis are reliable, but the late-night surcharge (after 10pm) is legitimate. Train and subway remain significantly cheaper for most tourist-area travel."),
    ],
    "Dubai": [
        ("Is Dubai safe for tourists?",
         "Dubai is one of the safer destinations in the Middle East with a low violent crime rate. The main tourist risks are financial scams (overcharging, fake products) and fraudulent service providers. Be particularly cautious in nightlife settings and with strangers who approach you in tourist areas."),
        ("What is the most common scam in Dubai?",
         "The Tinder/dating app bar trap is the most financially damaging scam — tourists are lured to bars where drinks are secretly priced at thousands of dirhams and charged under duress. Unofficial taxi overcharging from the airport is the most common lower-stakes scam."),
        ("Is alcohol legal in Dubai?",
         "Alcohol is legal in Dubai but only served in licensed hotels, bars, and clubs. It is not available in dry areas, and drinking in public or being drunk in public is illegal. The 'zero tolerance' DUI law means even a trace amount of alcohol can result in arrest for driving."),
        ("What should I do if I'm overcharged at a bar in Dubai?",
         "Document everything — photograph the bill, record the environment if possible. Contact Dubai Police (999) and file a report. If you signed a credit card slip under duress, contact your bank immediately to initiate a chargeback. Some victims have successfully recovered funds via this route."),
        ("Can I use Uber in Dubai?",
         "Yes, Uber operates fully in Dubai and is one of the safest transport options. Careem (owned by Uber) is the dominant local app. Both provide metered rides, driver identification, and route tracking — far safer than informal taxis or accepting rides from touts."),
    ],
    "Amsterdam": [
        ("Is Amsterdam safe for tourists?",
         "Amsterdam is generally safe but has above-average petty crime for a European city. Pickpocketing, bicycle theft, and drug-related scams are the main tourist risks. The Red Light District is safe to walk through as a tourist but do pay attention to your pockets in crowds. Violent crime targeting tourists is uncommon."),
        ("What is the most common scam in Amsterdam?",
         "Taxi overcharging from Centraal station is consistently the most reported scam. Always use metered official taxis or booking apps. Fake/stepped-on cannabis near coffeeshops is the second most common issue — buy only from licensed coffeeshops."),
        ("Are coffeeshops in Amsterdam safe?",
         "Licensed coffeeshops in Amsterdam are legal, regulated, and generally safe. Products are tested for quality. The risk comes from buying cannabis from street dealers who are selling unknown or adulterated products. If you use coffeeshops, start with a small amount — Dutch cannabis is significantly stronger than many tourists expect."),
        ("What's the best way to get from Amsterdam Centraal to my hotel?",
         "Take the GVB tram (multiple lines from the front of the station), metro, or book an Uber/Bolt from the app before you exit the building. The official taxi rank (TCA taxis with blue TCA logo) is also safe. Avoid any drivers who approach you inside or outside the station."),
        ("Are there pickpockets on Amsterdam trams?",
         "Yes — trams 2, 11, 12, and 13 (tourist routes through the center) and the busy stops at Centraal, Leidseplein, and Rembrandtplein have pickpocket activity. Keep bags in front of you, don't use phones visibly in crowded cars, and be alert when boarding and alighting."),
    ],
    "Singapore": [
        ("Is Singapore safe for tourists?",
         "Singapore is consistently rated one of the safest cities in the world. Violent crime is extremely rare, and petty theft is uncommon by Asian city standards. The main tourist risks are financial scams and counterfeit goods. Singapore's strict laws mean penalties for even minor offenses are severe — respect local regulations."),
        ("What is the most common scam in Singapore?",
         "Overpriced electronics and gem/jewelry scams (particularly at Sim Lim Square) are the most documented tourist scams. Fake 'lucky draw' promotions and unlicensed tour operators are also common. Overall, Singapore has one of the lowest scam rates in the region."),
        ("Is it safe to eat street food in Singapore?",
         "Yes — hawker centres are government-licensed, regularly inspected, and serve some of the best food in the city. The main thing to watch for is pricing: some hawker centres in tourist areas (like Newton Food Centre) have vendors who quote high prices orally then add extras. Ask for prices before ordering."),
        ("What should I do if I buy a fake item in Singapore?",
         "File a report with the Singapore Police at police.gov.sg. You can also report to the Competition and Consumer Commission of Singapore (CCCS). For credit card purchases, initiate a chargeback with your bank. Keep receipts and document everything."),
        ("Can I use Grab in Singapore?",
         "Yes — Grab is the dominant ride-hailing app in Singapore and is fully safe. Gojek also operates. Both provide metered rides and full driver accountability. Licensed taxis (ComfortDelGro, SMRT) are also reliable and metered. The MRT is the cheapest and fastest option for most tourist journeys."),
    ],
    "Hong Kong": [
        ("Is Hong Kong safe for tourists?",
         "Hong Kong remains one of Asia's safer cities for tourists. Violent crime targeting visitors is rare. The main risks are financial scams (electronics shops, gem sellers) and pickpocketing in crowded tourist areas. Nathan Road in Tsim Sha Tsui and the Peak tram queue have higher pickpocket activity."),
        ("What is the most common scam in Hong Kong?",
         "Electronics bait-and-switch at unlicensed shops in Tsim Sha Tsui is the most documented tourist scam. The pattern is consistent: quoted low price, forced to buy accessories, product swapped or fake. Gem and jewelry scams in tourist shops are the second most common."),
        ("Are Hong Kong taxis safe?",
         "Licensed Hong Kong taxis (red for urban, green for NT, blue for Lantau) are metered and generally honest. Note the taxi number before getting in. The Octopus card works in most red taxis now. Avoid unlicensed 'private cars' outside tourist attractions — they're illegal and unaccountable."),
        ("Where should I buy electronics in Hong Kong?",
         "Stick to certified retailers: Broadway, 3C (giftcard), or authorized brand stores in shopping malls. Avoid any shop in tourist areas that isn't in a shopping mall with clear posted prices. Mongkok Computer Centre and Sham Shui Po are authentic tech districts but require knowing current market prices."),
        ("Is the Star Ferry safe?",
         "Yes — the Star Ferry is one of Hong Kong's iconic legitimate transport services, crossing Victoria Harbour between Central/Wan Chai and Tsim Sha Tsui. It's one of the world's great commuter experiences and costs just a few HKD. No scam risk on the ferry itself."),
    ],
    "Kuala Lumpur": [
        ("Is Kuala Lumpur safe for tourists?",
         "Kuala Lumpur is generally safe for tourists though petty crime (bag snatching, phone theft) is more common than in Singapore or Tokyo. The main tourist areas — KLCC, Bukit Bintang, and Brickfields — are safe during the day. Take extra care at night in less-lit areas and always keep bags on the side away from the road."),
        ("What is the most common scam in Kuala Lumpur?",
         "Taxi overcharging (refusing to use meters) is the most consistent tourist complaint in KL. Gem investment scams targeting tourists in Chinatown and Petaling Street are the most financially damaging. Use Grab for all transport and be skeptical of overly friendly strangers offering tours or 'special deals.'"),
        ("Is Grab safe in Kuala Lumpur?",
         "Yes — Grab is by far the safest and most reliable transport option in KL. All drivers are registered, prices are fixed before the ride, and you have full trip history. Avoid metered taxis unless the driver explicitly agrees to use the meter before you get in — many refuse and overcharge tourists."),
        ("Where is it safe to walk in Kuala Lumpur?",
         "KLCC/Bukit Bintang (connected by free mall walkway), the Brickfields neighborhood, and Bangsar are all relatively safe for tourist walking. Petaling Street/Chinatown is safe during the day but be alert for bag-snatching motorcycles and con artists. The golden mile is Jalan Bukit Bintang to KLCC."),
        ("Is it safe to change money on the street in Kuala Lumpur?",
         "No — never change currency with street changers. Use licensed money changers (prevalent in shopping malls and the Chinatown area) or bank ATMs. Licensed money changers in Jalan Masjid India and Brickfields often have better rates than banks, but always count your notes before walking away."),
    ],
    "Seoul": [
        ("Is Seoul safe for tourists?",
         "Seoul is one of Asia's safest cities. Violent crime targeting tourists is extremely rare. The main risks are financial — overcharging in tourist areas, scam bars in Itaewon and Hongdae, and counterfeit goods at Dongdaemun Market. Solo female travelers consistently rate Seoul as comfortable even at night."),
        ("What is the most common scam in Seoul?",
         "Overpriced bars in Itaewon and Hongdae that don't display prices clearly are the most common financial trap. Street games (card games, three-cup monte) near Gyeongbokgung and Insadong have been reported. Aggressive commission-based tour guides at major sites sometimes quote inflated optional 'extras.'"),
        ("Are Seoul taxis safe?",
         "Licensed Seoul taxis (orange/silver: regular, black: deluxe) are metered and generally safe. The KakaoTaxi app is the most reliable way to book — it shows the driver's rating, route, and fare. Language can be an issue, so show your destination written in Korean if possible. Late-night taxis in entertainment areas occasionally overcharge tourists."),
        ("Is Itaewon safe for tourists?",
         "Itaewon is generally safe and remains Seoul's most international neighborhood. The main caution is in nightlife venues — check that the bar you're entering has visible prices, and don't rely solely on the recommendation of a new acquaintance. The Halloween tragedy of 2022 has prompted significant safety changes in the area's crowd management."),
        ("What's the best way to get from Incheon Airport to Seoul?",
         "The AREX (Airport Railroad Express) is the fastest and most reliable option — direct trains to Seoul Station take 43 minutes and cost ₩9,500. All-stop trains take 66 minutes and cost less. Avoid taxis and private transfer operators at arrival unless pre-booked through a verified service — metered taxis to central Seoul can cost ₩60,000–₩90,000."),
    ],
    "Lisbon": [
        ("Is Lisbon safe for tourists?",
         "Lisbon is generally safe with a low violent crime rate. Pickpocketing is the primary tourist risk, concentrated on Tram 28, the Alfama neighborhood, and Baixa/Chiado. The city has seen an increase in petty theft with the tourism boom. Avoid displaying expensive items in crowded tourist areas and you'll have a pleasant experience."),
        ("What is the most common scam in Lisbon?",
         "Pickpocketing on Tram 28 is the single most reported tourist incident in Lisbon. The tram's popularity with tourists, combined with its crowding, makes it prime territory. Taxi overcharging from the airport and restaurant overcharging in Alfama are the next most common complaints."),
        ("How do I get from Lisbon airport to the city?",
         "The Metro Red Line (Linha Vermelha) runs directly from the airport to Alameda (transfer point) in about 20 minutes and costs just €1.65 with a rechargeable Viva Viagem card. Uber and Bolt are also reliable and metered. Avoid taxis from touts outside the terminal — only use official rank taxis inside."),
        ("What's Tram 28 really like?",
         "Tram 28 is a genuinely beautiful journey through Alfama and Graça with historic yellow trams — but it's extremely crowded and pickpockets specifically work it. Go at opening hours (around 6am) for fewer crowds, or take it knowing your pockets are empty of valuables. Many tourists skip it and walk the hills, which is equally scenic."),
        ("Is the Pastel de Nata at the tourist spots good?",
         "The original Pastéis de Belém shop in Belém (not to be confused with generic 'pastel de nata' chains everywhere) is genuinely worth the queue. At most tourist-facing cafés and restaurants, pastéis de nata are overpriced — €1.50–€2.50 versus 80 cents at a proper local padaria. Walk one street back from any tourist area to find the local price."),
    ],
    "Athens": [
        ("Is Athens safe for tourists?",
         "Athens is generally safe for tourists, including older travellers visiting by cruise, on guided tours, or independently. Violent crime against visitors is rare. The main risks are financial — taxi overcharging, tourist-menu restaurants in Plaka, and Acropolis ticket fraud online — along with pickpocketing on the Metro and at the Acropolis queue. Omonia Square has more street-level issues and is best avoided after dark. Save Tourist Police 171 (English-speaking, 24/7) before your trip — they actively mediate tourist disputes and their response in 2025 has been effective."),
        ("What is the most common scam in Athens?",
         "Taxi overcharging from Athens Airport (ATH) and Piraeus cruise port is the most reported scam. The legal flat rate from the airport is €40 daytime (5 AM–midnight) and €54 overnight — posted on signs at the queue. Anything else is a scam. Fake Acropolis ticket websites (particularly acropolisticket.com) are the second most common issue — always book through hhticket.gr, GetYourGuide, Viator, or Tiqets. The 'friendly local' drink invitation scam in Plaka, where a stranger leads tourists to an unfamiliar bar with escalating bills, is the third most common and can reach €200–€400 per victim."),
        ("How do I get from Athens Airport to the city?",
         "The Metro Line 3 (blue line) runs directly from the airport to Syntagma Square in 40 minutes and costs €9 per person. The X95 express bus runs 24 hours for €6 and reaches Syntagma in about 60 minutes. If you prefer a taxi, use Uber, Bolt, FreeNow, or Beat — all four apps work in Athens and show fixed prices before you commit. Licensed airport taxis charge a flat €40 daytime or €54 overnight. Your hotel concierge can also pre-arrange a fixed-price transfer for €45–€55 if you prefer the certainty."),
        ("How do I buy genuine Acropolis tickets?",
         "Book online only through hhticket.gr (the official Ministry of Culture site) or verified resellers GetYourGuide, Viator, or Tiqets. Avoid acropolisticket.com and similar lookalike sites — they send invalid QR codes and require credit card chargeback to recover. The combined Acropolis ticket (€30 in summer, €20 in winter as of 2025) covers the Acropolis plus six ancient sites for five days. At the site, buy tickets at the official booth next to the main gate; ignore anyone approaching you in the queue with 'skip-the-line' offers. Licensed Greek guides wear a yellow certification badge — ask to see it before hiring on-site. The climb is steep and uneven; go early morning to avoid heat and queues."),
        ("What areas should older travellers avoid in Athens?",
         "Omonia Square at night and in early morning hours has concentrated pickpocket and 'fake police' activity — avoid the area after dark. Exarchia sees political demonstrations and is less tourist-friendly. Plaka, Monastiraki, and Syntagma are safe to walk day and evening, but be alert to the bracelet and flower distraction-theft crews at metro exits. Koukaki (south of the Acropolis), Kolonaki, and Pangrati are excellent neighbourhoods for dining and walking, with lower scam exposure and gentler cobblestones than Plaka's steeper lanes."),
    ],
    "Berlin": [
        ("Is Berlin safe for tourists?",
         "Berlin is generally safe. It has lower violent crime than many capitals, but pickpocketing is active on tourist routes, particularly the U-Bahn and S-Bahn, at Alexanderplatz, and near the Brandenburg Gate. Fare dodging fines catch many tourists — always validate your ticket. The club and nightlife scene is legitimate and safe, though very late nights benefit from basic awareness."),
        ("What is the most common scam in Berlin?",
         "Fare evasion fines are technically the most common 'tourist mistake' — €60 every time. Plain-clothes BVG inspectors work tourist routes. Three-card monte (Hütchenspiel) operators at Alexanderplatz are the most common intentional scam. Unofficial taxi overcharging from Schönefeld/BER airport also appears regularly."),
        ("How does Berlin's public transport work?",
         "The BVG system (U-Bahn, S-Bahn, trams, buses) requires a validated ticket for every journey. The Berlin Welcome Card provides unlimited travel and museum discounts. Buy and validate tickets at machines before boarding — 'I didn't know' is not accepted by plain-clothes inspectors. Zone ABC covers all major tourist sites including the airports."),
        ("Is the Berlin club scene tourist-friendly?",
         "Berlin has a world-famous club scene (Berghain, Tresor, Watergate) but many venues have strict door policies and don't admit obvious tourists or groups. Berghain's door is deliberately unpredictable. Don't take it personally — the scene is legitimate and safe, just selective. The Neukölln and Prenzlauer Berg neighborhoods have more accessible bars and smaller clubs."),
        ("What should I do if I get pickpocketed in Berlin?",
         "File a report at the nearest Polizei station or at polizei.berlin.de. Get an 'Aktenzeichen' (case number) for insurance. Cancel your cards immediately. For stolen passports, contact your embassy — the US Embassy is at Pariser Platz 2, open weekdays."),
    ],
    "Madrid": [
        ("Is Madrid safe for tourists?",
         "Madrid is generally safe, particularly for older travellers — violent crime against visitors is rare and the city has one of Spain's lower crime rates for a capital. The genuine risks are financial: Barajas Airport (MAD) taxi overcharging (documented in 2025 r/MadridTravelGuide warnings), Metro Sol and Atocha pickpocket teams, the 'bird poop' distraction scam in Puerta del Sol, bracelet and clipboard-petition crews at the Royal Palace, and fake Prado/Royal Palace ticket websites. Omonia's counterpart Lavapiés has higher street-level issues but is best avoided at night. Save Policía Nacional Comisaría de Centro (Calle Leganitos 19) and the SATE tourist-assistance police for disputes."),
        ("What is the most common scam in Madrid?",
         "Barajas Airport taxi overcharging is the most common — the legal flat rate to anywhere inside the M-30 ring is €33, but drivers routinely quote €60–€110 using 'broken meter,' 'luggage fees,' or indirect routes via the M-40. r/MadridTravelGuide 'Legal taxi scam at Madrid airport traveling between terminals' (2025) and r/MadridTravelGuide 'A dishonest airport taxi' are the community-anchor threads. Metro Line 1 pickpocket teams at Sol and Atocha stations are the second most common — teams of three or four operate at carriage doors and on escalators. The Puerta del Sol 'bird poop' distraction and clipboard-petition crews round out the top four."),
        ("How do I get from Barajas Airport to Madrid centre safely?",
         "Metro Line 8 runs from T1/T2/T3 and T4 directly to Nuevos Ministerios in 30 minutes for €5 (€3 airport supplement included) — the scam-free option. From there, transfer to Metro lines 10, 6, or 8 for your final destination. The Renfe Cercanías C-1 commuter train from T4 to Atocha or Chamartín is €2.60 (25 minutes). If you take a taxi, the legal flat rate is €33 inside the M-30 ring (posted at the queue); anything above is overcharging. For app-regulated fares, Uber, Bolt, FreeNow, and Cabify all work in Madrid. Your hotel concierge can pre-arrange a fixed-price transfer."),
        ("How do I book genuine Prado Museum and Royal Palace tickets?",
         "Book Prado tickets only at museodelprado.es (the official Museo Nacional del Prado site). Royal Palace tickets only at patrimonionacional.es. Verified third-party resellers with customs guarantees include GetYourGuide, Viator, and Tiqets. The Prado admission is €15, with free entry in the final two hours daily (6–8 PM). The Royal Palace is €14. Any 'skip-the-line' or 'official Spain ticket' reseller charging €30+ per person for tickets that cost €15 is marking up or producing fake QR codes. At the site, buy tickets at the official booth; licensed Spanish tour guides wear a Ministerio de Industria yellow credential card."),
        ("What areas of Madrid are best for older travellers?",
         "The historic centre (Sol, Mayor, La Latina) is the most interesting for first-timers with flat walks between main sights. Salamanca district is upscale with excellent restaurants, wider streets, and gentler cobblestones. Chueca and Malasaña have genuine tapas bars a street or two from the tourist core. For dining, walk one block away from Plaza Mayor — La Latina's Cava Baja has honest-priced tapas bars (Casa Lucio, Casa Labra are community-respected). Avoid eating anywhere you were actively recruited from the street; avoid Lavapiés at night."),
    ],
    "Santiago de Compostela": [
        ("Is Santiago de Compostela safe for tourists?",
         "Santiago is one of Spain's safest cities — violent crime is very rare, and the Old Town is walkable on mostly flat cobbled streets. The unique risk here is the 'peregrino long-con' scam on the Camino de Santiago: fellow pilgrims who develop friendship over 3–5 days before requesting loans, documented on r/CaminoDeSantiago 'Conned by a peregrino' (€150 and €400 losses). Taxi overcharging at Santiago Airport (SCQ) and Old Town tourist-menu restaurants on Rúa do Franco are the standard Spanish scams applied locally. Save Policía Nacional Santiago at Rúa Doutor Teixeiro 23 and the Oficina del Peregrino (+34 881 252 139)."),
        ("What is the most common scam in Santiago de Compostela?",
         "The 'peregrino long-con' is the highest-damage single scam — fellow pilgrims who walk alongside you for a week before requesting a €150–€400 loan 'until the bank opens tomorrow.' r/CaminoDeSantiago community threads warn that the Camino's culture of trust makes this disproportionately effective. Camino 'shortcut' bus and taxi scams that invalidate your Compostela certificate are the second most common. Old Town restaurant tourist-menu overcharging (€18–€25 menú peregrino for what should be €10–€14 menú del día) and airport taxi overcharging round out the top four."),
        ("How do I walk the Camino safely?",
         "The last 100 km of the Camino Francés (from Sarria to Santiago) must be walked continuously for the Compostela certificate — taxis and buses for this section invalidate your credential. Get sellos (stamps) only at official albergues, churches, and approved cafés along the yellow-arrow path. For luggage transfer, use JacoTrans (jacotrans.com) or Correos Paq Mochila (elcaminoconcorreos.com) at €5–€8 per bag per day — both have English websites and online booking. Never loan money to a fellow pilgrim regardless of how many days you've walked together; direct any emergency to their embassy or the Oficina del Peregrino (+34 881 252 139)."),
        ("How does the Pilgrim Mass and Compostela certificate work?",
         "The Pilgrim Mass at Santiago Cathedral is free and open to all, held daily at 12:00 and 19:30. Arrive 30–45 minutes early for seated attendance; the nave accommodates about 1,000 people. The Botafumeiro (giant silver censer) swings on a published schedule at catedraldesantiago.es — no tickets needed. The Compostela certificate is free from the Oficina del Peregrino (Rúa Carretas, 33) with your valid stamped credential; the longer Certificate of Distance is €3. Anyone outside the cathedral offering 'reserved seats,' 'VIP Botafumeiro access,' or paid 'Compostela authentication' services is running a scam."),
        ("Where should I eat in Santiago de Compostela?",
         "For authentic Galician food at honest prices, walk 15 minutes from the cathedral to the Ensanche (new town) or the Pombal/San Lourenzo neighbourhoods. Community-recommended posted-price restaurants with 4.4+ Google ratings include O Curro da Parra, Bodeguilla de San Roque, Abastos 2.0 (at the market), Casa Marcelo (Michelin Bib Gourmand), and Pulpería A Parada for pulpo. Rúa do Franco and Rúa do Vilar near the cathedral have 'menú peregrino' at €18–€25 that routinely delivers frozen pulpo and industrial empanada — a proper menú del día in residential neighbourhoods is €10–€14."),
    ],
    "Hanoi": [
        ("Is Hanoi safe for tourists?",
         "Hanoi is generally safe for tourists though petty crime — particularly bag snatching from motorbikes and aggressive overcharging — is more common than in more developed Asian cities. Violent crime targeting tourists is rare. The Old Quarter is safe to walk at night but be alert for drive-by bag snatches and keep bags on the far side from the road."),
        ("What is the most common scam in Hanoi?",
         "Cyclo/xe om overcharging is the most reported tourist complaint — always agree on a firm price before getting in. Fake travel agencies selling counterfeit Ha Long Bay tour tickets are the most financially damaging scam. The 'friendly local' bar invitation is also well-documented in the Old Quarter."),
        ("How do I book a Ha Long Bay tour from Hanoi?",
         "Book through a licensed travel agency with verified Google reviews and TripAdvisor listing — not a street kiosk or hotel lobby agent who can't show credentials. Reputable operators include Indochina Junk, Athena Cruises, and Era Cruises. Day trips for under $30 are typically severely cut-rate; overnight cruises start around $80-100 for a decent experience."),
        ("What's the best transport from Hanoi's airport?",
         "The 86 and 17 buses are the cheapest option (VND 35,000) but slow. The Grab app is the safest and most reliable option — book a car from inside the terminal before exiting. Metered taxis from the official ranks (Noi Bai, Hanoi Taxi) are legitimate but agree on meter use before entering. Avoid all 'fixed price' offers from touts outside."),
        ("Is street food safe in Hanoi?",
         "Hanoi's street food is one of the highlights of Vietnam travel and generally safe if you choose busy stalls with high turnover and visible cooking. Bun cha, pho, and banh mi from street vendors are iconic, delicious, and priced at 40,000–80,000 VND ($1.60–$3.20) per dish. The scam risk is NOT food safety but price-gouging at tourist-area restaurants that serve sanitised, mediocre versions at 150,000–300,000 VND per dish. Walk one street off Ma May, Ta Hien, or Cau Go to find authentic stalls where locals eat. Community-recommended names: Pho Gia Truyen (Bat Dan), Bun Cha Huong Lien (Le Van Huu — Obama's spot), Banh Cuon Ba Hanh (Ba Trieu), Cha Ca Thang Long (Cha Ca). Avoid any restaurant with a tout outside recruiting passing tourists."),
    ],
    "Ha Long Bay": [
        ("Is Ha Long Bay safe for tourists?",
         "Ha Long Bay is generally safe — violent crime against tourists is very rare. The practical risks for older travellers are financial: fake cruise-booking websites and clone operators per r/VietNam 'Booked a Ha Long Cruise: Am I about to get scammed or is' (comments/16auijg, 2024) and 'Ha Long Bay Cruise HELP SCAM?' (comments/1jcguad, 2025); Hanoi-to-Ha Long shuttle and transfer overcharges (Old Quarter copycat 'Sinh' offices); onboard cruise upsells (kayak supplement, photo packages, cabin upgrades); fake 'floating village' visits with diesel-sampan swap per r/travel (comments/dny5kt); Ha Long City / Tuan Chau pier taxi overcharge; and Booking.com / Agoda off-platform payment fraud per r/VietNam 'Hotel payment - Is this legitimate?' (comments/1jookvm, 2025)."),
        ("What is the most common Ha Long Bay scam in 2025?",
         "Fake cruise-booking websites top the list — clone sites mimic Bhaya, Paradise, Indochina Sails, and Orchid domains, charge via wire transfer, then disappear. Onboard cruise upcharges are second most common: 'kayaking included' becomes a 300K–500K VND supplement, 'free photos' become a 2M+ VND USB-drive sale, and 'premium cabin upgrade' is offered when your booked cabin is suddenly 'unavailable.' Fake 'floating village' tours with diesel-sampan swap per r/travel (comments/dny5kt), Hanoi-to-Ha Long shuttle overcharges via Old Quarter 'tourist offices,' Ha Long City/Tuan Chau pier taxi scams, and the 2025 Booking.com/Agoda off-platform WhatsApp payment-verification phishing per r/VietNam 'Hotel payment - Is this legitimate?' (comments/1jookvm, 2025) round out the top six."),
        ("How do I get from Hanoi to Ha Long Bay safely?",
         "The 3.5–4 hour drive between Hanoi and Ha Long / Tuan Chau has three legitimate options: (1) cruise-operator included transfer (most packages include it — use this); (2) shuttle bus via The Sinh Tourist (thesinhtourist.vn — verify URL EXACTLY, multiple copycats per r/VietNam '(Scam) The Sinh Tourist' comments/1af6jrg) at 300K–500K VND per person; (3) private car via Klook or 12Go Asia at $100–$160 one-way. Avoid Old Quarter 'tourist offices' quoting 'special deals' — they are aggregators with 3–5x markup per r/hanoi 'Am I being taken advantage of?' (comments/1b2wy9q, 2024). The 'VIP faster route' doesn't exist — all routes take ~4 hours."),
        ("What should I expect on a Ha Long Bay cruise?",
         "A legitimate 2-day/1-night Ha Long cruise at $150–$250 per person includes: round-trip Hanoi transfer, one night onboard in a cabin, three meals (lunch, dinner, breakfast), kayaking or rowing sampan session (verify 'included' not 'supplement' at booking), visit to one cave (Sung Sot or Luon), and one 'floating village' photo stop. r/Vietnam_Tourism 'Is ha long bay worth it?' (comments/1mtdro3, 2025) recommends requesting the Lan Ha Bay route (from Cat Ba Island) instead of the main Ha Long Bay — fewer ships, quieter kayaking, more authentic. Decline onboard upsells: take your own photos, bring your own snorkel/reading material, skip the 'pearl farm' visit selling paste-pearls at inflated prices per r/travel (comments/dny5kt). Check the final bill item-by-item before settling."),
        ("What's the difference between Ha Long Bay and Lan Ha Bay?",
         "Ha Long Bay is the UNESCO-famous main destination — overcrowded during peak season (April–October) with 500+ cruise ships circulating the same routes. Lan Ha Bay, accessed from Cat Ba Island (reached via Tuan Chau speedboat or car ferry), is a smaller quieter bay just south of Ha Long proper with equally dramatic karst limestone formations, significantly fewer ships, and genuine small fishing-village visits. r/Vietnam_Tourism 'Is ha long bay worth it?' (comments/1mtdro3, 2025) is blunt: 'I would recommend Lan Ha Bay over Ha Long bay if you're worried about the overcrowding.' For older travellers who prefer calmer water and kayaking over party-boat atmosphere, Lan Ha Bay operators (Indochina Junk, Signature Cruise, Perla Dawn Sails) offer comparable quality at similar prices with far better experience."),
    ],
    "Mexico City": [
        ("Is Mexico City safe for tourists?",
         "Mexico City has improved significantly in safety for tourist areas. The Roma, Condesa, Polanco, and Coyoacán neighborhoods are as safe as any major European city. The historic center is safe during the day. Avoid Tepito, Doctores, and the airport surroundings at night. The main risks are taxi-related crime, express kidnapping, and pickpocketing — manageable with the right precautions."),
        ("What is the most common scam in Mexico City?",
         "Express kidnapping via unofficial taxis (piratas) is the most dangerous and most reported serious crime affecting tourists. The solution is simple: only use Uber or book official taxis through SITEUR (airport official taxis) or your hotel. Pickpocketing in the historic center and at Chapultepec is also common."),
        ("Is Uber safe in Mexico City?",
         "Yes — Uber is widely considered the safest transport option in CDMX. It provides driver identification, GPS tracking, and full trip history. Book from inside the terminal or your hotel before stepping outside. Mexico City also has Cabify and DiDi as alternatives. Avoid any car that approaches you proactively."),
        ("Are there areas of Mexico City tourists should avoid?",
         "Tepito (market area known for contraband), Doctores, and parts of Iztapalapa have significantly higher crime rates and aren't on the typical tourist circuit. The historic center, Roma Norte/Sur, Condesa, Polanco, Coyoacán, and San Ángel are all relatively safe for daytime tourism. At night, stick to the neighborhood where you're eating or drinking and take Uber between areas."),
        ("Is tap water safe in Mexico City?",
         "No — tap water in CDMX is not safe to drink and causes stomach issues for most visitors. Drink bottled or filtered water. Most hotels provide purified water; many AirBnBs have filters. Brush your teeth with tap water is fine for most people, but drinking it is not recommended. Large 20-liter garrafones of purified water are very cheap at OXXO stores."),
    ],
    "Rio de Janeiro": [
        ("Is Rio de Janeiro safe for tourists?",
         "Rio requires more vigilance than most tourist destinations. Tourist areas like Ipanema, Leblon, Santa Teresa, and the historic center are manageable with proper precautions, but violent crime does occur. The golden rule: leave your valuables at the hotel. Use Uber, stay in well-lit areas at night, and follow local advice about which neighborhoods and times to avoid."),
        ("What is the most common scam in Rio?",
         "Beach robbery (arrastão — organized group theft sweeping a beach section) is the most high-profile crime. Express robbery (being walked to an ATM at gunpoint) and taxi overcharging are also common. The biggest risk mitigation: only take to the beach what you can afford to lose."),
        ("Which beaches in Rio are safe for tourists?",
         "Ipanema and Leblon are the safest beaches and have police presence. Copacabana has more crime but is heavily tourist-trafficked. Arpoador (between Ipanema and Copacabana) is good for surf viewing. Avoid isolated beaches without lifeguards or tourist presence. On any beach: rent a chair (they watch your things), don't bring valuables, and never leave belongings unattended."),
        ("What should I do if I'm robbed in Rio?",
         "Hand over whatever is demanded — no possession is worth your safety. Brazilian criminals typically want your items, not confrontation. Once safe, go to the nearest Delegacia de Atendimento ao Turista (tourist police) for a Boletim de Ocorrência (police report) — essential for insurance claims. The tourist police speak English at major precincts."),
        ("Is Carnival safe for tourists?",
         "Carnival is genuinely festive and overwhelmingly positive, but crime spikes significantly during the event. Wear a money belt, keep phones in front pockets (or better, at the hotel), and stay with your group. The official Sambódromo parade is safer than street blocos from a theft perspective. Book tickets through official Liesa outlets only — counterfeit tickets are common."),
    ],
    "Lima": [
        ("Is Lima safe for tourists?",
         "Lima is manageable for tourists who stay in the main tourist districts: Miraflores, Barranco, and San Isidro are as safe as most Latin American cities. Centro Histórico is safe during the day for sightseeing. The main risks are taxi-related crime, street theft, and scams at currency exchange. Avoid displaying jewelry or expensive electronics in any district."),
        ("What is the most common scam in Lima?",
         "Taxi crime (fake taxis taking tourists to isolated areas) is the most dangerous and most consistently reported risk. Use InDriver or Uber exclusively — never take street taxis. Currency exchange scams (counterfeit bills or bad rates) and fake tour operators for Machu Picchu are common financial scams."),
        ("How do I get to Machu Picchu from Lima?",
         "Fly to Cusco (1 hour, multiple daily flights) rather than the 24-hour bus journey. From Cusco, take a train to Aguas Calientes (the town below Machu Picchu) — Peru Rail and Inca Rail are the two licensed operators. Book train tickets well in advance through official websites. Machu Picchu entry requires advance booking through culturaqosqo.gob.pe."),
        ("Is altitude sickness a concern in Lima?",
         "Lima itself is at sea level — no altitude concern. However, if you travel to Cusco (3,399m), Machu Picchu (2,430m), or Lake Titicaca (3,812m), altitude sickness is a real issue for many visitors. Spend 1–2 days acclimatizing in Cusco before physical activity, stay hydrated, avoid alcohol for the first day, and consider altitude medication (acetazolamide/Diamox) on advice from your doctor."),
        ("Is Peruvian street food safe to eat?",
         "Peru has an extraordinary food culture and street food is generally safe in Miraflores and Barranco from busy, established carts. Ceviche in Lima is world-famous and genuinely excellent — but only from established restaurants, not street stalls, as it requires fresh ingredients handled properly. The classic sandwich vendor at Barranco's bridge is a famous safe option."),
    ],
    "Krakow": [
        ("Is Krakow safe for tourists?",
         "Krakow is one of Poland's safest cities and is very tourist-friendly. Violent crime targeting visitors is extremely rare. The main risks are bar overcharging in the Old Town, unofficial taxis, and the occasional pickpocket in crowded market areas. The Kazimierz (Jewish Quarter) and Podgórze neighborhoods are safe at night."),
        ("What is the most common scam in Krakow?",
         "Restaurant overcharging near Market Square (Rynek Główny) is the most consistent tourist complaint — unlisted bread charges, couvert fees, and service charges that appear without warning. Unofficial taxi overcharging (particularly late at night from the Old Town to hotels) is the second most common issue. Use Bolt or FreeNow."),
        ("How do I get from Krakow Airport to the city center?",
         "The train (Krakow Airport Express) runs from the airport to the main Krakow Główny station in 17 minutes — cheap, fast, and reliable. Bolt and Uber also operate from the airport at standard rates. Avoid taxi drivers who approach you in the arrivals hall — official taxis are at the rank outside."),
        ("Is Auschwitz worth visiting from Krakow?",
         "Auschwitz-Birkenau is a profoundly important historical site located 70km from Krakow. Entry to the main Auschwitz I site is free but requires advance booking at auschwitz.org. Guided tours can be booked on-site or through licensed operators in Krakow — verify the operator's license and read TripAdvisor reviews before booking. Budget 4–5 hours minimum."),
        ("What's the local beer culture like in Krakow?",
         "Krakow has an excellent craft beer scene centered on Kazimierz. The rule: avoid any bar right on the Market Square, as they charge tourist prices (300-400% markup). Walk two blocks into Kazimierz for the same drinks at local prices. Żywiec, Tyskie, and Okocim are the mass-market lagers; craft breweries like Browar Lubicz and Forum offer excellent local options. One pilsner at a Kazimierz bar costs half what it does in a tourist trap."),
    ],
    "Florence": [
        ("Is Florence safe for tourists?",
         "Florence is generally safe for tourists. Violent crime targeting visitors is rare. The main risks are pickpocketing in crowded tourist areas (Duomo, Ponte Vecchio, ATAF buses), bracelet/rose scams near major monuments, and restaurant overcharging in the tourist center. Exercise the same awareness you would in any busy European city."),
        ("What is the most common scam in Florence?",
         "The friendship bracelet scam near the Duomo and Ponte Vecchio is Florence's most persistent tourist scam — vendors grab your wrist and tie a bracelet before you can refuse, then demand €10-20. Pickpocketing on crowded ATAF buses (especially lines 1 and 7) is the most common non-scam crime."),
        ("How do I avoid restaurant scams in Florence?",
         "Walk one or two streets away from major sights for significantly better value. Always check for 'coperto' (cover charge) on the menu before sitting. Refuse bread, olives, or drinks you didn't order — these are charged separately. The Mercato Centrale upstairs food court offers quality food at transparent prices."),
        ("Is the Uffizi Gallery safe?",
         "The Uffizi itself is perfectly safe. The risk is outside — street vendors lay paintings on the walkway hoping you'll step on one and pay for 'damage,' and clipboard petition scammers work the queues. Book skip-the-line tickets online to minimize time exposed to exterior scams."),
        ("What areas should I avoid in Florence?",
         "Florence doesn't have dangerous neighborhoods in the way larger cities do. The train station area (Santa Maria Novella) and Cascine Park after dark have slightly higher petty crime rates. The centro storico is safe at night. The main risk everywhere is pickpocketing and street vendor scams, not violent crime."),
    ],
    "Dublin": [
        ("Is Dublin safe for tourists?",
         "Dublin is generally safe for tourists. Violent crime targeting visitors is uncommon. The main risks are phone snatching (increasingly common on Grafton Street and at Luas stops), ATM card skimming near O'Connell Street, and taxi overcharging from Dublin Airport. The Temple Bar area is safe but attracts overcharging pubs."),
        ("What is the most common scam in Dublin?",
         "Taxi overcharging — particularly from Dublin Airport into the city center — is the most consistently reported tourist complaint. The ride should cost €25-35 by meter. Phone snatching on busy shopping streets and at Luas tram stops is the most common theft crime targeting tourists."),
        ("Is Temple Bar worth visiting?",
         "Temple Bar is Dublin's famous pub district and worth experiencing for the atmosphere, live music, and energy. However, drinks are significantly more expensive than pubs a few streets away — a pint of Guinness costs €6-7 at a normal pub vs €8-9+ in Temple Bar. The best strategy: visit for the atmosphere, then drink in the Liberties or Stoneybatter for local prices."),
        ("How do I get from Dublin Airport to the city?",
         "The Airlink Express bus (routes 747/757) is the cheapest reliable option at €7-8. Dublin Bus also runs routes. Taxis from the official rank should cost €25-35 to city center by meter. Free Now app is the safest taxi option. Avoid any driver inside the terminal offering 'flat rates.'"),
        ("Are there areas to avoid in Dublin?",
         "Dublin is largely safe but some areas north of the Liffey around O'Connell Street can feel less comfortable at night. The north inner city has higher petty crime rates. Sheriff Street and parts of Ballymun are best avoided. South of the Liffey — including Temple Bar, Grafton Street, and St. Stephen's Green — is very safe."),
    ],
    "Copenhagen": [
        ("Is Copenhagen safe for tourists?",
         "Copenhagen is one of Europe's safest capitals. Violent crime is very rare. The main risks are pickpocketing on the Metro and at crowded tourist attractions like Nyhavn and Tivoli Gardens. Bicycle theft is extremely common. Overall, Copenhagen requires minimal safety awareness compared to most European cities."),
        ("What is the most common scam in Copenhagen?",
         "Pickpocketing at Nyhavn, on the Metro, and at Tivoli Gardens is the most common tourist crime. Copenhagen doesn't have the aggressive street scam culture of some southern European cities. The main financial trap is the general expense — Denmark is genuinely expensive and what feels like overcharging is often just normal pricing."),
        ("Is Christiania safe to visit?",
         "Freetown Christiania is generally safe for tourists during the day. Photography is strictly prohibited on Pusher Street and can provoke aggressive reactions. Don't buy or carry drugs — police conduct raids. The area around Christiania is safe. Visit during daylight hours, respect the community's rules, and you'll have no issues."),
        ("How expensive is Copenhagen?",
         "Copenhagen is legitimately one of Europe's most expensive cities. A meal at a mid-range restaurant costs 150-250 DKK (€20-33). Beer is 60-80 DKK (€8-11). This is normal pricing, not a tourist trap. Save money at street food markets like Reffen and Torvehallerne, and use a Copenhagen Card for transport and museum entry."),
        ("What's the best transport in Copenhagen?",
         "The Metro, S-train, and buses use the same ticket system (Rejsekort or DOT single tickets). A Rejsekort saves about 50% on fares. Copenhagen is extremely bicycle-friendly — rent a city bike or use the Donkey Republic app. Taxis are metered and honest but expensive (starting fare ~40 DKK). Never accept unlicensed rides."),
    ],
    "Budapest": [
        ("Is Budapest safe for tourists?",
         "Budapest is generally safe for tourists but requires more awareness than some Western European capitals. The 'pretty girl bar scam' in District V is a genuine and well-documented risk. Pickpocketing on trams and the Metro is common. The ruin bar district (District VII) is safe and legitimate. Violent crime targeting tourists is rare."),
        ("What is the most common scam in Budapest?",
         "The 'pretty girl bar scam' is Budapest's most notorious and financially damaging scam — attractive women invite tourists to a specific bar where drinks cost €50-100 each, enforced by bouncers. Currency exchange fraud on Váci utca (terrible hidden rates at 'zero commission' booths) is the second most common."),
        ("How should I exchange money in Budapest?",
         "Use ATMs from major Hungarian banks (OTP, K&H, Erste) — always decline the 'dynamic currency conversion' and withdraw in HUF. Avoid exchange booths on Váci utca entirely. The Correct Change exchange offices in the city have fair rates. Never exchange money with strangers on the street."),
        ("Are Budapest ruin bars safe?",
         "The famous ruin bars in District VII (Szimpla Kert, Instant, etc.) are legitimate, iconic experiences and generally safe. The risk is pickpocketing in the crowded spaces, especially on weekend nights. Keep phones and wallets in front pockets. The bars themselves have fair pricing — it's the unofficial venues that scam."),
        ("How do I get from Budapest Airport to the city?",
         "The 100E airport bus runs directly to Deák Ferenc tér (city center) for 2,200 HUF — fast and reliable. Bolt and Uber operate from the airport at standard rates (~8,000-10,000 HUF to center). MiniBUD shared shuttles are budget-friendly. Avoid taxi drivers who approach you inside arrivals — use the official Főtaxi rank outside."),
    ],
    "Dubrovnik": [
        ("Is Dubrovnik safe for tourists?",
         "Dubrovnik is one of Croatia's safest destinations. Violent crime is extremely rare. The main risks are overcharging at restaurants inside the Old Town walls, unlicensed tour operators (especially Game of Thrones tours), and pickpocketing in the crush at Pile Gate when cruise ships are in port. Overall, Dubrovnik is very safe."),
        ("What is the most common scam in Dubrovnik?",
         "Restaurant overcharging inside the Old Town walls is the most consistent complaint. Menus near the Stradun charge 2-3x what restaurants just outside the walls charge for the same dishes. Unlicensed Game of Thrones tour operators who charge premium prices for basic walks are also commonly reported."),
        ("How do I avoid cruise ship crowds?",
         "Cruise ships arrive between 8-10am and passengers typically leave by 4-5pm. Visit the Old Town walls early morning (opening time) or late afternoon. The city installed crowd counters at Pile Gate — check dubrovnik.hr for real-time density. Alternatively, explore Lokrum Island or Lapad Beach while ships are docked."),
        ("Is it worth eating inside the Old Town?",
         "Some restaurants inside the walls are excellent, but the tourist traps near the Stradun are overpriced. Walk to side streets like Od Puča or climb to the upper residential streets for local-quality food at 40-60% lower prices. Alternatively, eat just outside the Ploče Gate or in the Lapad neighborhood."),
        ("How do I get around Dubrovnik?",
         "Dubrovnik's Old Town is car-free and walkable. The Libertas city bus connects Lapad, Gruž port, and the Old Town. Uber operates but coverage is limited — local taxis at official ranks are metered and generally honest. Water taxis to Lokrum and Cavtat are fun and fairly priced. Avoid unlicensed boat operators at the harbor."),
    ],
    "Santorini": [
        ("Is Santorini safe for tourists?",
         "Santorini is one of the safest tourist destinations in Greece — violent crime against visitors is effectively nonexistent. The genuine risks are financial: restaurant per-kilo fish billing on Oia's caldera, fake 'public bus' shuttles at Athinios Port, rental car damage deposit shakedowns, and hotel overbooking forced 'upgrades.' Sun, heat, and the steepness of Fira's and Oia's cobbled streets are practical concerns for older travellers — wear supportive shoes and pace yourself. Save Tourist Police 171 (English, 24/7) before your trip."),
        ("What is the most common scam in Santorini?",
         "At Oia and Fira caldera restaurants, fish priced 'per kilo' rather than per portion produces routine €200+ bills for a single seabass — always ask for per-portion prices in writing before ordering. The Athinios Port fake public bus scam (€15 for what the real KTEL bus charges €2.40) targets every ferry arrival. Rental car agencies claiming 'damage' on return for pre-existing scratches, and hotels forcing an 'upgrade' to an inferior property on arrival, round out the top four high-value scams. Donkey handlers demanding mid-ride price increases is the most common low-value scam."),
        ("How do I get to Santorini from the ferry port?",
         "At Athinios Port, the official KTEL public bus charges €2.40 to Fira and runs every 30 minutes during tourist season — timetables are posted at ktel-santorini.gr. Look for the official blue-and-white livery with a printed route number. The men in vests yelling 'public bus €15' at the ferry exit are running a private shuttle at six times the real rate. A hotel-arranged private transfer costs €15–€25 for a clearly-contracted car — this is often the best choice for older travellers arriving with luggage after a long ferry crossing."),
        ("Should I ride the donkeys in Santorini?",
         "No, for three reasons. First, the 'traditional' framing is largely a tourist construct — most Santorini Greeks do not ride donkeys today. Second, handlers frequently escalate the price mid-descent ('€5' becomes '€20 because of the incline'). Third, there are documented animal welfare concerns — the Greek government enacted a 100-kilogram rider weight limit in 2018 because donkeys have suffered spinal injuries from the workload. For Fira-to-port transport, the cable car is €6 each way and runs every 20 minutes — safer, faster, and avoids the ethical concerns. In Oia, the 214 steps to Ammoudi Bay take 15 minutes downhill at a slow pace."),
        ("How do I avoid restaurant overcharging on the caldera?",
         "Three rules. First, fish must be priced per portion (e.g., 'seabass 300g €32') rather than per kilogram — refuse any 'we'll weigh it after cooking' arrangement. Second, refuse welcome bread, olives, and bottled water when they arrive — 'ochi, efcharisto' politely waves them off. Third, for dinner, drive or bus inland to Pyrgos, Megalochori, or Karterados villages where local tavernas serve better Greek food at half the caldera prices — then return to Oia purely for sunset at a free public viewpoint. Community-recommended honestly-priced Oia restaurants include Lauda, Santo Souvlaki, and Pelekanos (all 4.4+ Google ratings)."),
    ],
    "Mykonos": [
        ("Is Mykonos safe for tourists?",
         "Mykonos is physically safe — violent crime against tourists is very rare. The serious risks are financial: DK Oyster and similar beach-restaurant overcharging (documented in Metro and The Sun July 2025 with £1,000 and €1,350 bills), taxi/ATV rental scams at the Old Port, and accommodation overbooking scams. Mykonos Town's cobbled streets are pedestrian-only and charming but steeply stepped in places; older travellers with mobility concerns may prefer staying in Ornos or Platys Gialos where hotel access is flatter. Save Tourist Police 171 (English, 24/7)."),
        ("What is the most common scam in Mykonos?",
         "DK Oyster beach club on Platys Gialos remains Europe's most infamous restaurant scam, with bills of £1,000+ for three dishes reported in 2025 national UK media. The mechanic is per-kilogram fish pricing plus unordered bread, olives, and 'sparkling water' added to the bill. Restaurant overcharging at Little Venice and Matoyianni Street in Chora — often via no-menu or menu-without-prices tactics — is the second most common. Illegal cover charges for bread and olives are specifically prohibited by Greek law and carry €500 fines, yet the practice continues due to weak enforcement."),
        ("How do I get around Mykonos from the cruise port?",
         "Cruise ships tender passengers into the Old Port, a 15-minute walk from Chora (pleasant, flat-ish, scenic). From Chora, the Fabrika bus station is another 10 minutes' walk; from there, KTEL buses run to Paradise Beach, Platys Gialos, Ornos, and Elia for €2 per person. Taxis from the Old Port quoting €40 to Paradise Beach are overcharging — the bus is €2 and Mykonos has only 30 official taxis for the whole island, so walking + bus is often faster than waiting. For time-constrained cruise passengers, Mykonos Yachting-organised private boat or car transfers via the hotel concierge eliminate the uncertainty."),
        ("Where should I eat in Mykonos to avoid overcharging?",
         "Avoid Little Venice waterfront and Matoyianni Street restaurants for dinner — these are the highest overcharge zones. Instead, eat in Ano Mera village (8 km inland from Chora) or in quieter Chora back streets. Community-recommended honestly-priced tavernas include Joanna's Nikos Place in Megali Ammos, Kiki's Tavern in Agios Sostis (no electricity, posted prices, authentic), and Funky Kitchen in Chora. At any restaurant, request a printed menu with per-portion prices before sitting; refuse welcome bread, olives, and bottled water when they arrive. The Little Venice sunset is best enjoyed at 180° Sunset Bar or Galleraki — have a single cocktail there, then walk inland for dinner."),
        ("Should I book Mykonos reservations or tours through social media?",
         "No. The r/Mykonos moderator team posted a 2024 scam alert explicitly warning: 'DON'T TRUST ANY OFFERS YOU RECEIVE THROUGH REDDIT.' Instagram DMs and WhatsApp offers for Scorpios, Nammos, or SantAnna reservations at 'VIP prices' are near-universally scams. Payment is typically via PayPal, Venmo, or bank transfer (irrecoverable). Book Scorpios, Nammos, SantAnna directly through their verified websites, book private boats through Mykonos Yachting or Delos Tours, and require written contracts for any high-value booking. If a stranger contacts you first on social media about a Mykonos experience, treat it as a scam until verified."),
    ],
    "Thessaloniki": [
        ("Is Thessaloniki safe for tourists?",
         "Thessaloniki is Greece's second city and is generally safe for tourists. Violent crime against visitors is rare; most areas including Ladadika (old Ottoman restaurant quarter), Aristotelous Square, and the White Tower promenade are walkable day and night. The genuine risks are financial: Uber and taxi overcharging from Thessaloniki Airport (SKG), tourist-menu restaurants in Ladadika, nightclub 'minimum consumption' traps, and bracelet distraction pickpockets in Aristotelous. For older travellers, note that Ano Poli (the upper town) has steep cobblestone streets but the main city is largely flat and walkable. Save Tourist Police 171."),
        ("What is the most common scam in Thessaloniki?",
         "Taxi and Uber overcharging from Thessaloniki Airport (SKG) is the most common — 2025 r/uber documented an airport-to-Parea-Beach ride estimated at €10–€14 that was charged €24 after unexplained 'tolls' were added. Bar and nightclub 'minimum consumption' surprise charges at Ladadika and Valaoritou are the second most common, with €50–€150 per person minimums disclosed only after seating. Restaurant overcharging at White Tower waterfront cafés (€7 cappuccinos vs €2.50 local price) and bracelet distraction pickpockets at Aristotelous Square round out the top four."),
        ("How do I get from Thessaloniki Airport to the city?",
         "The 01X and 78N public buses run from Thessaloniki Airport (Makedonia, SKG) to the city centre for €2 per person, taking 45–60 minutes. This is the scam-free option. For taxis, use FreeNow or Beat apps — the legitimate metered fare to the city centre is €15–€22 plus €4 airport surcharge. Screenshot the app estimate before the ride; if the final charge exceeds the estimate by more than €3, dispute within 24 hours via the app. Avoid roadside taxi hails from the airport rank — drivers there routinely claim the meter is broken and quote €40–€60 flat."),
        ("Is Meteora worth a day trip from Thessaloniki?",
         "Not really. The r/GreeceTravel community consensus is clear: a Meteora day trip from Thessaloniki involves approximately 10 hours of total drive time for 3 hours on-site, which is rushed and tiring. The far better approach is to take the train from Thessaloniki to Kalambaka (€20, 3 hours), overnight in Kalambaka at a hotel with clifftop views, and return the next day. For older travellers, this is less physically demanding and delivers a much better experience. Booked tour operators offering 14-hour Meteora day trips under €60 are mathematically impossible to deliver well — suspect commission stops at souvenir workshops and gift shops."),
        ("Where should I eat in Thessaloniki?",
         "Ladadika (the restored Ottoman-era quarter) has charming atmosphere but some tourist-trap restaurants — choose venues with posted menus, 4.4+ Google ratings, and 500+ reviews (Mourga, Nea Folia, To Nisaki are community favourites). For local prices and better food, eat in Ano Poli (upper town) or the Kalamaria seafront district. The White Tower waterfront cafés charge €7 for a coffee that costs €2.50 one block inland; enjoy one seafront coffee as a tourist experience, then move inland for actual meals. Decline welcome bread, olives, and bottled water when they arrive — Greek law prohibits unlisted cover charges."),
    ],
    "Paros": [
        ("Is Paros safe for tourists?",
         "Paros is generally safe for tourists — violent crime against visitors is very rare. The serious risks are financial: Parikia port and Naoussa taxi overcharging (€40 for 5-minute rides documented on r/GreeceTravel), rental car damage claims (Carwiz and small storefronts), Naoussa Old Port tourist-menu restaurants, and hotel off-platform payment fraud. Paros has the genuine advantage of being walkable in Parikia and Naoussa centres; older travellers can do most short sightseeing on foot. Save Tourist Police 171 and Paros office +30 22840-21673."),
        ("What is the most common scam in Paros?",
         "Taxi overcharging at Parikia port is the most reported — r/GreeceTravel 'Taxi service in Paros' documents a €40 quote for a 5-minute ride (Greek minimum fare is €4 + €1 port surcharge = €5 legal minimum). Hotel off-platform payment fraud (r/GreeceTravel 'Booking a hotel in Greece - Paros island' specifically) is the second most damaging — scammers impersonate Booking.com and request deposit via fake payment links. Naoussa Old Port tourist-menu restaurants and car rental damage claims round out the top four. The 'Antiparos day tour' markup (€60–€90 per person for what should be €15 DIY) is the most commonly encountered lower-value scam."),
        ("How do I get from Parikia port to my hotel?",
         "Pre-book a hotel transfer (€15–€25 through most Paros hotels) with a written quote; this is the cleanest option for older travellers arriving with luggage after a four-hour ferry. The KTEL Parou public bus from Parikia to Naoussa is €1.80 and runs every 30 minutes in summer (schedule at ktelparou.gr). If you take a taxi, demand the meter (tariff 1 €1.06/km plus €1 port surcharge); the legitimate fare from port to central Parikia hotels is €5–€10 under Greek law. Refuse any 'broken meter' flat-rate quote and try the next taxi. For Naoussa, the metered taxi fare is €25–€35."),
        ("Should I visit Antiparos on a tour or DIY?",
         "DIY is dramatically cheaper and better. Take the KTEL bus from Parikia to Pounda (€1.80, 20 minutes), then the Pounda–Antiparos car ferry (€2.50 each way for foot passengers, every 30 minutes). Walking to the Antiparos harbour and exploring on foot is easy and pleasant. The Antiparos Cave charges €6 entry with a €1.50 bus from Antiparos village. The entire self-directed day costs €15 combined for a couple; storefront 'Antiparos day tour' packages at €60–€90 per person add rushed group logistics without real value. For private yacht charters (if that appeals), book through Paros Yacht Club or Cyclades Sailing with published rates — not storefront 'private yacht day' quotes that are actually shared motor-boat tours."),
        ("How do I rent a car safely in Paros?",
         "Rent from major international brands at Paros Airport (PAS) only — Avis, Europcar, Hertz, Sixt. Avoid Carwiz specifically (multiple 2024–2025 Greek market warnings) and small Parikia or Naoussa storefronts with unverifiable brand names. Photograph every panel including underside, wheel wells, windshield, and interior with timestamps before driving off; upload to email or cloud backup. Get a written damage inspection form signed by the agent listing every existing scratch. Pay by credit card only (never cash deposit) — use a premium travel credit card (Chase Sapphire Reserve, Amex Platinum) with primary rental car insurance. If a false damage claim is made on return, refuse to pay beyond the deposit and file with Paros Tourist Police +30 22840-21673."),
    ],
    "Naxos": [
        ("Is Naxos safe for tourists?",
         "Naxos is generally safe for tourists — violent crime against visitors is very rare, and Naxos is often recommended for older travellers because Chora is pedestrian-friendly and the Kastro old town is atmospheric but manageable. The serious risks are financial: Matha Rent a Car named scooter/car damage scam (explicit r/GreeceTravel warning thread), beach chair 'per chair per hour' pricing ambiguity, hotel off-platform booking fraud, and Chora tourist-menu restaurants. Naxos buses are slow but reliable; the island rewards visitors willing to walk and use public transport. Save Tourist Police 171 and Naxos office +30 22850-22100."),
        ("What is the most common scam in Naxos?",
         "The Matha Rent a Car scam is the most dangerous single-operator named warning on the island — r/GreeceTravel 'DO NOT RENT WITH MATHA RENT A CAR' is the anchor thread. The mechanic combines manufactured 'damage' charges with post-return credit card fraud where shops charge your card days after you leave the island. Beach chair pricing ambiguity (€5 'per chair' quoted as total but billed per hour) at Plaka, Agios Prokopios, and Alyko beaches is the second most common. Chora tourist-menu restaurant overcharging and port-area taxi quotes of €20 for 1-kilometre rides round out the top four."),
        ("How do I rent a car in Naxos without being scammed?",
         "Do not rent from Matha Rent a Car — explicit community warning. Rent from Europcar at Naxos Airport (JNX) or major brands only, and still follow the full protection protocol: photograph every panel with timestamps before driving off, get a written damage inspection signed, pay by credit card only. Use a dedicated travel credit card you can lock after return if suspicious 'damage' charges appear days or weeks after you leave the island — Naxos shops have been flagged for post-return fraud specifically. Use a premium travel credit card (Chase Sapphire Reserve, Amex Platinum) with primary rental car insurance that replaces the agency's ambiguous 'full cover' offering. File charges with your credit card issuer immediately if disputed charges appear."),
        ("How do I avoid beach chair pricing scams in Naxos?",
         "At any Naxos beach (Plaka, Agios Prokopios, Agia Anna, Mikri Vigla, Alyko), ask for total price in writing for the full day for two chairs plus umbrella before sitting — 'total, four hours, two chairs with umbrella, confirmed.' Get a written receipt. Refuse 'per chair per hour' pricing unless it is clearly posted and acceptable. Look for a printed price board or municipal licence number at the concession kiosk; legitimate operators have one visible. For Alyko, drive past parking attendants to see actual availability at closer lots — 'closer lots are full' claims are often false, mirroring the 2025 Elafonissi parking scam on Crete. Greek public beaches are legally accessible to the high-tide line, so bringing your own towel is always an option."),
        ("Is Naxos worth a day trip from Paros or Santorini?",
         "Yes, but a day trip compresses what is genuinely a two-to-three-day destination. Naxos Town (Chora) with the Venetian Kastro takes half a day; Portara (the marble temple gateway at the harbour entrance) is the iconic sunset photograph. The interior villages — Apiranthos, Halki, Filoti — are each worth a half-day and reachable by KTEL Naxos bus (€2.50–€4 each way, schedules at ktelnaxos.gr) or rental car (€30–€50 per day from major brands at Naxos Airport). Plaka Beach and Agios Prokopios are a KTEL bus ride from Chora (€2.50, 30 minutes). For older travellers, Naxos is often recommended as the Cycladic base of choice because it is less crowded than Santorini and Mykonos, with more authentic Greek food and more manageable prices."),
    ],
    "Corfu": [
        ("Is Corfu safe for tourists?",
         "Corfu is generally safe for tourists, particularly older travellers arriving by cruise or on guided tours. Violent crime against visitors is very rare. The serious risks are financial: cruise-port and airport taxi overcharging (cited in the 2025 r/travel 'Two Corfu scams to avoid' thread), Porto Timoni boat-tour fraud, car rental damage claims (particularly Carwiz and small resort storefronts), and tourist-menu restaurant overcharging at the Liston. Corfu Old Town's cobbled lanes are mostly flat but uneven in places — supportive shoes essential. Save Tourist Police 171 and Corfu office +30 26610-30265."),
        ("What is the most common scam in Corfu?",
         "Cruise-port and airport taxi overcharging is the most reported — drivers at Kerkyra port quote €40 for the 10-minute walk to Old Town and €100+ for day trips to Achilleion or Paleokastritsa. r/GreeceTravel 'Taxis in Corfu — an absolute disgrace' (comments/1df8zd8) is the canonical community warning. The Porto Timoni boat-tour scam (named in the 2025 r/travel anchor thread) is second most common — operators advertise landings at the famous double-beach but deliver 20-minute swimming stops at adjacent beaches instead. Car rental damage claims (Carwiz is specifically flagged across Greek markets) round out the top three."),
        ("How do I get around Corfu without being overcharged?",
         "Walk from Kerkyra cruise port to Corfu Old Town — it is 10 minutes along a scenic, flat waterfront. For Achilleion Palace and Paleokastritsa, take the Green Bus (KTEL Kerkyras) for €3–€5 per person — schedule at greenbuses.gr. From Corfu Airport (CFU), bus 15 runs to Corfu Town in 15 minutes for €1.70. For taxis, use FreeNow or Beat where available (coverage is limited outside Corfu Town); if taking a regular taxi, demand the meter (tariff 1 at €1.06/km) and refuse any 'broken meter' flat-rate quote. Your cruise ship's shore excursion office can pre-book private cars at posted rates."),
        ("Should I visit Porto Timoni?",
         "Only if you can hike the steep 30-minute descent and 40-minute ascent on rough stone paths. The 'Instagram-famous double beach' is real but physically demanding to reach. The 2025 r/travel scam warning highlighted that boat tours quoted at €30–€60 per person often do not actually land at Porto Timoni — they stop at adjacent beaches and photograph the view from the water. ATV 'transportation' at the Afionas trailhead starts at €10 and escalates to €30 after boarding. For older travellers with mobility concerns, skip Porto Timoni entirely; Glyfada, Dassia, and Ypsos are accessible alternatives with similar water quality. If you can hike, go in the cool morning (before 10 AM) with proper shoes and 2 litres of water."),
        ("How do I rent a car in Corfu?",
         "Rent from major international brands at Corfu Airport (CFU) only — Avis, Budget, Hertz, Europcar, Sixt, National. Avoid Carwiz specifically (multiple 2024–2025 warnings across Greek markets) and small resort storefronts in Dassia, Ypsos, Kavos, or Paleokastritsa where the brand names are not internationally affiliated. Photograph every panel including underside, wheel wells, and interior before driving off. Get a written damage inspection form signed by the agent. Pay by credit card only (never cash deposit) for chargeback leverage. Use a premium travel credit card with primary rental car insurance to replace the agency's ambiguous 'full cover' offering."),
    ],
    "Chania": [
        ("Is Chania safe for tourists?",
         "Chania (the capital of western Crete) is generally safe for tourists, including older travellers. Violent crime against visitors is rare. The serious risks are financial: tourist-menu overcharging at the Old Venetian Harbour, car rental damage claims (Chania storefronts are community-flagged for the same scams as Heraklion), Balos Lagoon boat-tour markups, and petrol station short-change at the named Souda junction Shell. Chania's Old Venetian Harbour is beautifully photogenic and walkable on mostly flat cobblestones; the Old Town streets behind the harbour are narrower but generally manageable. Save Tourist Police 171 and Chania office +30 28210-73333."),
        ("What is the most common scam in Chania?",
         "Old Venetian Harbour restaurant overcharging is the most common — €60–€90 per person for food that costs €20–€25 at neighbourhood tavernas, plus 'cutlery charges' and unordered welcome items. The Tamam restaurant €2.60 cutlery debate (r/crete community thread) highlights that unlisted cover charges are technically illegal in Greece under consumer law. Car rental damage claims at Chania Airport (CHQ) and Old Town storefronts are the second most common — r/crete 'Trustable Car Rental Service in Chania?' has 'It's a scam' as the top community reply. Balos Lagoon boat-tour package markup (paying €70+ for what should be a €30–€35 direct ferry) is also frequently reported."),
        ("How do I get to Balos Lagoon and Elafonissi from Chania?",
         "For Balos, take the direct Balos Cruise ferry from Kissamos Port (€30–€35 per person round trip; baloscruise.com has the schedule). Drive yourself to Kissamos (1 hour from Chania) and park at the port for €3–€5. The ferry is safer for older travellers than the unpaved drive to Balos, which requires low-clearance vehicle skill for the last kilometre. For Elafonissi, drive yourself (45 minutes from Chania) — but drive past the first few parking attendants on arrival, as the 2025 viral Elafonissi scam (r/GreeceTravel 99-upvote warning) redirects visitors to pricier €5 lots claiming closer €3 lots are 'full.' Arrive at either beach before 10 AM in summer for parking, cooler temperatures, and thinner crowds."),
        ("Where should I eat in Chania Old Town?",
         "For the harbour experience, enjoy one coffee or cocktail at a harbour café as the tourist premium (€6–€8). For meals, walk two or three blocks inland. Community-recommended posted-price Chania tavernas include Tamam (despite the community 'cutlery charge' debate, the food is excellent and prices are posted — just decline the cutlery charge), Chrisostomos in Kastelli old town (500+ Google reviews at 4.6+), Oinoa Wine Bar (local wine with real menu), and Bougatsa Iordanis for breakfast. Confirm the outside menu matches the table menu before sitting; refuse welcome bread, olives, and bottled water when they arrive. Greek law prohibits unlisted cover charges (€500 fines)."),
        ("How do I rent a car in Chania without being scammed?",
         "Rent from major international brands at Chania Airport (CHQ) — Avis, Budget, Hertz, Europcar, Sixt, National. Avoid Carwiz specifically and Chania Old Town storefronts that are community-flagged for damage scams. Photograph every panel including underside, wheel wells, windshield, and interior before driving off. Get a written damage inspection form signed by the agent. Pay by credit card only for chargeback leverage. Use a premium travel credit card with primary rental car insurance. When fuelling, pay by card at all stations — the Souda junction Shell is specifically named on r/crete for short-change scams, and the Chania–Rethymnon highway has similar attendant patterns."),
    ],
    "Rhodes": [
        ("Is Rhodes safe for tourists?",
         "Rhodes is generally safe for tourists, including older travellers arriving by cruise or on guided tours. Violent crime is rare. The serious risks are financial, concentrated in Rhodes Old Town (bar bill extortion, tourist-menu restaurants) and Faliraki (resort-strip overcharging). Rhodes Old Town is a UNESCO World Heritage medieval city with cobblestones, uneven surfaces, and some steep passages — supportive shoes are essential. The walk from Kolona cruise port to Old Town is 5 minutes and mostly flat. Save Tourist Police 171 — Rhodes has an active Old Town Tourist Police post at the Eleftherias Gate during summer."),
        ("What is the most common scam in Rhodes?",
         "Old Town bar bill extortion is the most reported — Daily Mail and Greek Herald June 2025 coverage documented bars charging €40–€80 per drink via no-menu or 'novelty glass' tactics. Faliraki 'all-inclusive' and 'VIP bottle service' packages with small-print surcharges are the second most common. Old Town tourist-menu restaurants charging 2–3x local prices (the Daily Mail named several in its 2025 investigation) and bracelet-flower distraction pickpocket crews at the Eleftherias Gate round out the top four. Rhodes authorities began fining named venues in 2025 but enforcement is reactive."),
        ("How do I get around Rhodes?",
         "From Diagoras Airport (RHO), the KTEL bus runs to the city centre for €2.40 every 30–60 minutes. From Rhodes Town to Lindos, the KTEL bus costs €5.50 and runs every 30 minutes in peak season (50–55 minute drive). For the Old Town and Mandraki Harbour, walk — these areas are pedestrian. From the Kolona cruise port to the Old Town is 5 minutes on foot. For taxis, FreeNow and Beat apps work in Rhodes Town; the legitimate metered fare from the airport to Rhodes Town is €25–€30. Resort hotels in Ixia or Faliraki are best reached by the KTEL bus or a pre-booked transfer; beach-strip taxis operate as a cartel that sometimes refuses app pickups."),
        ("Should I visit Lindos and how?",
         "Yes — Lindos is one of the most beautiful villages in Greece, with the Acropolis of Lindos on a hilltop overlooking a white-sand beach. Take the KTEL bus from Rhodes Town (€5.50 each way, every 30 minutes in peak season). The walk from Lindos village to the Acropolis is 10 minutes up steep stone steps — slow but manageable for most older travellers with good footwear. Do not ride the donkeys offered at the trailhead — mid-ascent price hikes are common (€5 becomes €15 halfway up) and there are documented animal welfare concerns. For visitors with genuine mobility issues, cruise shore excursions with golf-cart transfers are the ethical alternative."),
        ("Where should I eat in Rhodes Old Town?",
         "Choose restaurants with menus posted visibly outside and with 4.4+ Google ratings plus 500+ reviews. Community-recommended posted-price Old Town dining includes Nireas Restaurant, Hatzikelis (old Turkish fountain setting), To Meltemi, and Alexis Palace. Avoid any restaurant without a visible menu or where the outside menu differs from the table menu — this is the Daily Mail 2025 documented scam pattern. For lunch during a cruise excursion, walk inland toward Pythagora Street or the Municipal Market where local tavernas serve residents at half the Old Town tourist prices. Refuse welcome bread, olives, tzatziki when they arrive; Greek law prohibits unlisted cover charges (€500 fines per violation)."),
    ],
    "Heraklion": [
        ("Is Heraklion safe for tourists?",
         "Heraklion (Crete's capital) is generally safe — violent crime against tourists is rare. The serious risks are financial, concentrated in three areas: rental car damage fee shakedowns (r/greece documented a €500 charge for a superficial scratch), Knossos Palace 'private guide' overcharges, and Elafonissi Beach parking scams. Cruise passengers arriving at Heraklion's port face taxi overcharging similar to Athens' Piraeus. Older travellers should note that Heraklion Town's Venetian walls and Knossos site involve uneven stone and some steps — comfortable shoes are essential. Save Tourist Police 171."),
        ("What is the most common scam in Heraklion?",
         "Rental car damage claims are the most damaging — agencies rent cars with pre-existing cosmetic damage, then charge €400–€700 for 'new' scratches on return. r/greece's 2023 thread on a €500 scratch charge remains the canonical warning; r/UKPersonalFinance and r/legaladviceireland have 2024–2025 parallel cases. The 'full insurance' offered at pickup often has hidden deductibles that the agency uses to charge on minor marks. The 2025 Elafonissi Beach parking scam (r/GreeceTravel 99-upvote viral warning) is the most commonly encountered summer scam — attendants redirect visitors to paid €5 lots, claiming the closer free lots are full."),
        ("How do I rent a car in Crete without getting scammed?",
         "Rent from major international brands (Avis, Budget, Hertz, Europcar, Sixt) at Heraklion Airport — not small Heraklion Town storefronts like Abbycar Crete that are specifically named in r/cretetravel scam warnings. Photograph every panel of the car including underside, wheel wells, windshield, and interior before driving off; get a written damage inspection form signed by the agent listing every existing scratch. Pay the rental and deposit by credit card only for chargeback leverage. Use a premium travel credit card with primary rental car insurance (Chase Sapphire, Amex Platinum) to replace the agency's ambiguous 'full insurance' offering."),
        ("How do I visit Knossos Palace without overpaying for a guide?",
         "Knossos has three tiers: standard ticket €15 at the booth, public group tour €20–€25 per person (licensed Greek guide, 90 minutes, 15–25 person group that forms at regular intervals at the entrance), and private tour €80–€120 per person (same content, smaller group). The scam version is 'official guides' at the entrance offering private tours for private-tier prices but delivering public-tier content. Look for the yellow Greek Federation of Tourist Guides badge and ask for the certification number. The €5 audio guide is an excellent self-guided alternative. Cruise shore excursions typically include a guide; do not pay extras on-site if you booked a package."),
        ("Is it worth visiting Elafonissi or Balos beaches?",
         "Yes — both are world-class beaches — but arrive prepared. The 2025 Elafonissi parking scam redirects visitors to €5 lots claiming the closer €3 lots are 'full.' Drive past the first few attendants to see actual availability; the municipal-licensed lots are often available. For Balos, consider the boat from Kissamos port (€30 round trip, runs daily) rather than driving — the last kilometre of the access road is narrow, unpaved, and can be genuinely difficult. Arrive at either beach before 10 AM in summer: parking is easier, crowds thin, and heat is manageable. Cruise passengers should consider Balos as a half-day boat excursion rather than attempting a drive."),
    ],
    "Phuket": [
        ("Is Phuket safe for tourists?",
         "Phuket is generally safe but requires significantly more awareness than many Southeast Asian destinations. Jet ski scams, tuk-tuk overcharging, and nightlife drink spiking are real risks. The tourist areas (Patong, Kata, Karon) are safe for walking. Motorbike accidents are the #1 cause of tourist injury — not crime."),
        ("What is the most common scam in Phuket?",
         "The jet ski damage scam on Patong Beach is Phuket's most notorious tourist scam — operators claim you damaged the jet ski and demand thousands of baht, sometimes involving police who side with the operator. Tuk-tuk overcharging and gem shop scams ('government gem sale') are the next most common."),
        ("Are tuk-tuks safe in Phuket?",
         "Phuket tuk-tuks are safe physically but financially predatory. There are no meters — you must negotiate every ride. A fair price from Patong Beach to Phuket Town is 400-500 baht. Drivers often quote 1,000+ baht. The Grab app works in Phuket and provides fixed, fair pricing — use it instead of negotiating."),
        ("Is Patong Beach safe at night?",
         "Bangla Road in Patong is Phuket's nightlife center and is generally safe to walk through. The risks are drink spiking (never leave drinks unattended), aggressive bar girls/ladyboys demanding money, and ping pong show scams (billed per 'act' at outrageous prices). Stay alert and avoid venues with aggressive touts."),
        ("Should I rent a motorbike in Phuket?",
         "Motorbike accidents are the leading cause of tourist injuries in Phuket. Roads are hilly, narrow, and local driving is aggressive. If you rent, wear a helmet (legally required), have an international driving permit, and check your travel insurance covers motorbike injuries — many policies don't. Grab is a safer alternative for most tourist trips."),
    ],
    "Ho Chi Minh City": [
        ("Is Ho Chi Minh City safe for tourists?",
         "Ho Chi Minh City (Saigon) is generally safe from violent crime against tourists, but 2025 Reddit reports document an escalation in petty crime. r/VietNam 'Definitely Vietnam is not as safe as you might think' (comments/1s17w2d, 2025) captures the shift. The practical risks for older travellers: Tan Son Nhat fake-Grab drivers per r/VietNam 'HCMC Airport (Grab prentending) taxi Scam' (comments/1p3puug, 2025); Vinasun/Mai Linh copycat taxis per r/VietNam 'HCMC taxi scam' (comments/dzk58l); Bui Vien 4M VND bar extortion per r/VietNam 'Ho Chi Minh City Walking Street (Bùi Viện) 4 million VND Scam' (comments/1lf9jl6, 2025); District 1 motorbike bag/phone snatches per r/VietNam 'Moped following me at night' (comments/1ncdomn, 2025); Ben Thanh Market 3-5x tourist overcharging; and Booking.com hotel fraud per r/VietNam '[Warning] Scam hotel chain in Ho Chi Minh City' (comments/1m8qxgt, 2025). Save HCMC Tourist Police (+84 28 3838 2990)."),
        ("What is the most common HCMC scam in 2025?",
         "Tan Son Nhat airport fake-Grab-driver scams top the list — r/VietNam 'Double scammed by cab pretending to be Grab in Saigon' (comments/1n2j3b3, 2025) documents the 2025 pattern. Motorbike bag snatches and phone-grab attacks from mopeds are second most common and most physically dangerous per r/VietNam 'Concerned about bag snatchers and pickpockets' (comments/1gii41b, 2024) and 'Moped following me at night' (comments/1ncdomn, 2025) — thieves can pull victims off their feet into traffic. Vinasun/Mai Linh copycat taxi overcharging, Bui Vien 4M VND hostess-bar extortion, Ben Thanh Market 3-5x tourist pricing, and Booking.com/Agoda off-platform payment fraud per r/VietNam '[Warning] Scam hotel chain' (comments/1m8qxgt, 2025) round out the top six."),
        ("How do I get from Tan Son Nhat Airport (SGN) to District 1 safely?",
         "Book Grab or Be yourself on airport Wi-Fi AFTER you have your luggage — verify licence plate matches the app. Typical fare: 150,000–230,000 VND to District 1. Licensed Vinasun (white/red/gold, 1900-1055) or Mai Linh (green, 1055) taxis charge 150,000–200,000 VND with meter. The 152 public bus runs SGN to Ben Thanh for 5,000 VND (slow, luggage-unfriendly). IGNORE every person in the arrivals hall offering 'taxi' or 'Grab' — all are unauthorised per r/VietNam 'Robbed at HCM airport by fake Grab driver. Be' (comments/1js1uqh, 2025). The official Grab/Be pickup counter is past the car park — wait there, not in arrivals. Avoid 'fixed price' quotes of 600,000+ VND; the pattern is documented per r/VietNam 'HCMC - scams, scams and not scams' (comments/1os81k3, 2025)."),
        ("How do I safely visit Ben Thanh Market?",
         "Treat Ben Thanh as a photo-stop, NOT a shopping destination. r/VietNam 'First Time in Saigon! Any tips for Ben Thanh Market?' (comments/1ogf62h, 2025) is blunt: 'Ben Thanh market is a total scam. Everything is priced between 3 to 5x' fair market. For clothes, bags, and electronics, cross the road to Saigon Square (indoor shopping centre, fixed prices, locals shop there) per r/VietNam 'Saigon Square is what tourists think Ben Thanh Market is' (comments/1n9nxdg, 2025). For authentic Trung Nguyen coffee, visit the OFFICIAL store on Nguyen Hue — NOT the Ben Thanh vendors, who sell knock-offs at 5x prices per r/VietNam 'Bought coffee from the local market' (comments/1gzjb5v, 2025). If you must buy at Ben Thanh, start negotiating at 30% of the quoted price. Never touch or try on items unless you intend to buy — vendors lock you into purchase obligation via social pressure."),
        ("Is street food safe in Ho Chi Minh City?",
         "Saigon has extraordinary street food and it's generally safe at busy stalls with high turnover. Community-recommended iconic dishes at their iconic stalls: Bánh mì Huỳnh Hoa (Le Thi Rieng), Phở Hòa (Pasteur), Com Tam Ba Ghien (Le Van Sy), Bún Thịt Nướng Chị Tuyền (Co Giang). The scam risk is NOT food safety but price-gouging at tourist-facing restaurants near Bui Vien and Ben Thanh that charge 3–5x the real street-stall rate. Walk one street off Bui Vien or Ben Thanh to find authentic stalls where locals eat. Drink bottled water only; avoid ice from street stalls unless commercially produced (cylindrical shape with a hole). Phone in zipped inner pocket — District 1 sidewalk motorbike snatch targets tourists with visible phones during food tours."),
    ],
    "Hue": [
        ("Is Hue safe for tourists?",
         "Hue is generally safe — violent crime against tourists is very rare. The practical risks for older travellers are financial: Phu Bai Airport and street taxi overcharges per r/VietNam 'Grab scammers Dong Hoi & Hue targeting tourists' (comments/1azj3g1, 2025) documenting 700K VND for 200K rides; Hue cyclo mid-ride price escalation and 'friend's shop' kickback detours; Perfume River dragon boat pressure sales and 'cultural performance' supplements; Imperial City single-entry ticket confusion per r/VietNam (comments/1scth5u, 2025); bicycle-pusher change-switch scams per r/VietNam 'Got scammed twice in a matter of few moments' (comments/1rx8yd1, 2025); and motorbike rental damage claims on Hai Van Pass trips. Save Hue Tourist Police (Le Loi Street, +84 234 3823 131)."),
        ("What is the most common Hue scam in 2025?",
         "Grab and street taxi 700K VND overcharges at Phu Bai Airport and Dong Hoi train station top the list — r/VietNam 'Grab scammers Dong Hoi & Hue targeting tourists' (comments/1azj3g1, 2025) is the named 2025 anchor. Cyclo tourist-price mid-ride extortion is second most common, with short rides quoted at 5-10x legitimate rates. The Perfume River dragon-boat pressure sales, Imperial City single-entry ticket trap, bicycle-pusher change-switch scams, and Easy Rider motorbike-rental damage claims round out the top six."),
        ("How do I visit the Hue Imperial City (Dai Noi) without overpaying?",
         "Buy tickets at the OFFICIAL Ngọ Môn Gate (Noon Gate) booth — 200,000 VND adult, 40,000 VND children (2025 rate); the combined ticket with two royal tombs (Tu Duc + Minh Mang + Khai Dinh) is 420,000 VND. CRITICAL per r/VietNam 'Hue imperial city - missed the main attraction' (comments/1scth5u, 2025): the Imperial City ticket is SINGLE ENTRY — you cannot exit and re-enter on the same ticket. Plan a full 3–4 hour visit without exiting. Bring your own water and snacks OR use the posted-price canteen INSIDE. Refuse 'combo ticket' touts outside the gate; buy at the official booth only. For older travellers, consider a guided tour via Klook/GetYourGuide at $20–$35 per person (includes English guide, entry, round-trip transfer)."),
        ("How do I take a Perfume River dragon-boat cruise safely?",
         "Book via a licensed operator (Hue Dragon Boat Tours, hue-dragon-boats.com) with fixed upfront pricing ($15–$25 per person). VERIFY in writing what's included: Thien Mu Pagoda stop, pagoda entry fees, return transfer, performances. r/solotravel 'Had an interesting experience in Vietnam (Hue) last night' (comments/6dz5m9) warns that dock-side operators pivot mid-river to 'cultural performance' or 'sunset premium' supplements. Refuse ALL mid-river refreshment and performance upsells. For older travellers, daytime tours (10 AM–3 PM) are significantly less crowded and pressured than sunset tours. Tip 50K–100K VND at end ONLY if the service was good."),
        ("What's the best way to explore Hue beyond the Imperial City?",
         "The standard 2-day Hue itinerary includes: Day 1 Imperial City (3-4 hours) + Thien Mu Pagoda (1 hour) + dinner at posted-price Com Am Phu (Nguyen Sinh Cung). Day 2 three royal tombs (Tu Duc, Minh Mang, Khai Dinh) + Dong Ba Market lunch. For older travellers, skip the motorbike tour of Hai Van Pass entirely (Vietnamese traffic is intense, pass is 21 km of switchbacks) and book a private car via Klook at $50–$80 for Hue-Da Nang via Hai Van Pass + Lang Co Beach stop. If you must rent a bike, use Easy Rider pillion operators (Hue Easy Rider, OneTrip Hai Van) where you ride behind an experienced local driver for $50–$80/day per r/VietNam 'Motorcycle rental Hue' (comments/bb1nah). Decline hotel-recommended 'local' rental shops — kickback arrangements and damage-claim disputes are documented."),
    ],
    "Hoi An": [
        ("Is Hoi An safe for tourists?",
         "Hoi An is broadly safe from violent crime, but 2025 Reddit reports document a heavily commercialised scam ecosystem. r/VietNam 'Hoi An: a rant' (comments/1mbtpwn, 2025) captures the sentiment: 'the motto is Cram them in and extract every dong.' The practical risks for older travellers: tailor-scam fabric markup and rushed construction per r/VietNam 'Worst Tailor in Hoi An' (comments/1inj004, 2025); lantern-boat mid-ride price escalation and fake monks per r/VietNam 'BEWARE HOI AN SCAM' (comments/1l80zcz, 2025); Ancient Town ticket and fake-ticket-checker confusion; aggressive 'fruit ladies' photo demands; cooking class and tour kickback fraud per r/VietNam 'Scams after scams' (comments/1s5018d, 2025); and beach bicycle/motorbike rental damage claims. Save Hoi An Tourist Police (Hoang Dieu Street, +84 235 3861 234)."),
        ("What is the most common Hoi An scam in 2025?",
         "Tailor scams top the list — r/VietNam 'Worst Tailor in Hoi An' (comments/1inj004, 2025) documents 'Italian wool' fabric upsells at 3x market rate, rushed 24-hour construction that fails after one wash, and hotel-concierge 'partner tailor' kickback arrangements. Lantern-boat pushy-vendor scams per r/VietNam 'BEWARE HOI AN SCAM' (comments/1l80zcz, 2025) are second most common. Ancient Town ticket and fake-checker confusion, 'fruit ladies' photo-demand traps, cooking class and day-tour kickback fraud, and beach bicycle/motorbike rental damage claims round out the top six."),
        ("How do I buy a quality tailored suit or dress in Hoi An?",
         "Use ONLY community-verified tailors with 4.5+ Google ratings and long review histories. The three most-consistently-recommended: Yaly Couture (Nguyen Thai Hoc, 450+ reviews), Bebe Tailor (Tran Phu, 900+ reviews), and A Dong Silk (Le Loi, 200+ reviews). Allow 2–3 days minimum for proper fittings (construction + 2–3 fitting sessions). Bring a reference garment for fit matching. REFUSE hotel concierge 'partner tailor' recommendations — they operate kickback arrangements that inflate prices 30–50% per r/VietNam 'Worst Tailor in Hoi An' (comments/1inj004, 2025). Verify fabric by touch and burn-test. Expected: $150–$250 for a quality suit, $80–$150 for a tailored dress. Pay 50% deposit, 50% on final fitting — NEVER 100% upfront. For older cruise travellers on day trips, skip tailoring entirely; the 1-day rush produces poor quality."),
        ("How do the Hoi An Ancient Town ticket and full-moon festival work?",
         "The Ancient Town entry ticket (120,000 VND adult, 2025) is required to enter the UNESCO heritage zone and provides access to 5 of 20+ monuments of your choice. Buy at the OFFICIAL booths at main Ancient Town entry points per r/VietNam 'Tickets for old town hoi an' (comments/1hos5u9, 2025). Community-recommended 5-monument choice: Japanese Covered Bridge, Phung Hung Ancient House, Hai Nan Assembly Hall, Tran Family Chapel, Quan Cong Temple. Keep your ticket visible — checkers occasionally verify at the QR gate. REFUSE unofficial 'ticket checkers' demanding additional cash if you already have a ticket; the scam pattern is documented. The monthly full-moon festival (14th day of lunar month, street lights off, lanterns on) is FREE with your regular Ancient Town ticket — no additional fee required despite what touts may claim."),
        ("Where should I book cooking classes and day tours in Hoi An?",
         "Book cooking classes DIRECTLY via the venue's own website — community-recommended: Red Bridge Cooking School (redbridgecookingschool.com), Morning Glory Cooking School (facebook.com/morningglorycooking), Vy's Market Restaurant Cooking Class. Expect $25–$40 per person for a 4-hour class including market visit. For My Son temples, book via Klook or GetYourGuide at $20–$30 half-day with guide. For Cham Island snorkelling, book via Klook or at the An Bang Beach jetty at $40–$55 per person. REFUSE hotel 'partner' recommendations and Ancient Town tout offers per r/VietNam 'Scams after scams' (comments/1s5018d, 2025) — the kickback arrangements inflate prices 30–100% above direct-booking rates. For older travellers, skip the rushed cruise-excursion cooking class entirely; genuine quality requires 4 hours and unhurried pace."),
    ],
    "Ninh Binh": [
        ("Is Ninh Binh safe for tourists?",
         "Ninh Binh is moderately safe — violent crime against tourists is very rare, but r/VietNam 'Warning - Trang An/Ninh Binh experience with abusive kids, sellers and scammers' (comments/1h0br4q, 2025) documents a 2025 escalation in tourist-targeting scams. The practical risks for older travellers: fake parking attendants and entry-fee collectors in Trang An/Tam Coc zones; Tam Coc sampan rower tip demands and mid-river sales pressure; Hanoi-Ninh Binh train booking website fraud per r/hanoi 'Warning : taking the train is a scam!' (comments/1p67b98, 2025); overnight train attendant extortion per r/VietNam 'Brazen scam on overnight train from Ninh Binh to Hue' (comments/1c0bzbj, 2024); homestay fake-review fraud per r/VietNam 'Worried about fake reviews - need legit lodging' (comments/1i9uszt, 2025); and Grab off-app highway-fee overcharges per r/VietNam 'Do you have to pay highway ticket on top of Grab ride' (comments/1ivi8la, 2025). Save Ninh Binh Tourist Police (Tran Hung Dao, +84 229 3871 113)."),
        ("What is the most common Ninh Binh scam in 2025?",
         "Fake parking attendants and 'entry fee' collectors at Trang An and Tam Coc zones top the list — r/VietNam 'Warning - Trang An/Ninh Binh experience with abusive kids' (comments/1h0br4q, 2025) documents vest-wearing scammers demanding 30K–50K VND in free-parking zones and 50K–100K VND at pagoda approaches where real tickets are further in. Tam Coc sampan rower tip demands are second most common. Hanoi-Ninh Binh train booking website fraud, overnight train attendant extortion on the Ninh Binh-Hue sleeper, homestay fake-review fraud, and Grab off-app highway-fee overcharges per r/VietNam (comments/1ivi8la, 2025) round out the top six."),
        ("How do I get from Hanoi to Ninh Binh safely?",
         "Three legitimate options: (1) train (2 hours, 100K–300K VND) — book ONLY via dsvn.vn, baolau.com, or 12go.asia; r/hanoi 'Warning : taking the train is a scam!' (comments/1p67b98, 2025) warns clone sites mark up 2-3x; (2) bus via The Sinh Tourist (thesinhtourist.vn — verify URL exactly, multiple copycats exist) at ~250K VND for 2.5 hours; (3) Grab or private car via Klook/12Go Asia at 800K–1.2M VND / $60–$100 for the 2-hour drive. Pay by credit card only; refuse wire transfer or cryptocurrency. For older travellers with luggage, the private car is easiest. For older travellers booking a return sleeper train to Hue, consider the daytime train (6–7 hours) or a 1-hour Vietnam Airlines flight instead to avoid the overnight-attendant extortion window per r/VietNam (comments/1c0bzbj, 2024)."),
        ("How do I visit Trang An and Tam Coc without getting scammed?",
         "Book tickets ONLY at the official counters: Trang An boat tour is 250,000 VND/person, Tam Coc boat tour is 150,000 VND/person (2025 rates — boat tour included in entrance ticket). Park only in signed paid-parking zones and refuse vest 'attendants' in unsigned areas per r/VietNam 'Warning - Trang An/Ninh Binh' (comments/1h0br4q, 2025). For the sampan ride, carry small-change notes (50K, 100K) for a reasonable end-tour tip at your discretion — a tip of 50K–100K VND is standard if the service was good. Decline ALL mid-river drink, snack, souvenir, or photo sales — they are not part of the legitimate tour. If the rower demands extra payment mid-river, say 'không' firmly and reference the official ticket price. For older travellers, the Trang An motorised boats (larger, 60-person capacity) are more stable and have fewer tip-pressure encounters than Tam Coc's rowed sampans."),
        ("Where should I stay in Ninh Binh?",
         "Book only through Booking.com, Agoda, or VRBO with platform-verified payment. Skip properties with suspicious review patterns (50+ 5-star reviews in a 2-week window) per r/VietNam 'Beware fake hotel reviews' (comments/1i8rtqj, 2025). Community-recommended properties with long-standing verified review histories: Tam Coc Garden Resort, Ninh Binh Hidden Charm Hotel & Resort, Trang An Retreat, Aravinda Resort, Chez Beo Homestay. Reverse-image-search homestay photos on Google Images before booking per r/VietNam 'Worried about fake reviews - need legit lodging' (comments/1i9uszt, 2025). REFUSE any WhatsApp 'payment verification' or 'deposit' requests off-platform — r/VietNam 'Hotel payment - Is this legitimate?' (comments/1jookvm, 2025) documents the pattern. Stay in Tam Coc village (5 min from boat dock) or Trang An area (5 min from boat dock) for best access to both boat tours."),
    ],
    "Da Nang": [
        ("Is Da Nang safe for tourists?",
         "Da Nang is broadly safe from violent crime, but r/DaNang 'Don't like Danang 2026' (comments/1qbqqxr, 2025) captures a 2025–2026 escalation: 'Scams are increasing in Da Nang.' The practical risks for older travellers: DAD airport fake-Grab and late-night taxi overcharges per r/DaNang 'What to scams to look out for in Hoi Ann' (comments/1k18dh6, 2025); Ba Na Hills winter fog and tour-package overcharges per r/VietNam 'One destination ruined the whole trip' (comments/1hk0reg, 2025); Marble Mountains jade/marble souvenir pressure sales; My Khe/An Thuong 'Where are you from?' couple tea scam per r/DaNang (comments/1jrd6sn, 2025); Dragon Bridge weekend fire-show pickpockets; and self-drive rental car damage claims. Save Da Nang Tourist Police (24 Tran Phu, +84 236 3860 444)."),
        ("What is the most common Da Nang scam in 2025?",
         "Airport fake-Grab and taxi overcharges top the list — the same Vietnam-wide pattern Hanoi and HCMC share. Ba Na Hills tour-package overcharges (hotel concierge $80-120 per person for direct-bookable $45 experience) are second most common per r/VietNam (comments/1hk0reg, 2025). Marble Mountains jade/marble kickback shops, An Thuong 'Where are you from?' couple tea scams per r/DaNang (comments/1jrd6sn, 2025), Dragon Bridge weekend pickpockets, and self-drive rental car damage claims round out the top six. r/DaNang '17 Scams in Vietnam to Avoid' (comments/1n50brt, 2025) is the 2025 community compilation."),
        ("How do I get from Da Nang Airport to my accommodation?",
         "Book Grab or Be yourself on airport Wi-Fi AFTER luggage. Expected fares: central Da Nang 100K–150K VND, Hoi An 250K–350K VND, Hue (via Hai Van Pass) 1.2M–1.8M VND. Licensed Mai Linh (green, 1055) or Vinasun taxis are the backup; insist on the meter. For late-night arrivals, pre-arrange hotel transfer via your accommodation's official booking per r/DaNang 'Can I take a taxi from the airport to the city at night?' (comments/1bn4cum, 2024). IGNORE every person in arrivals offering 'taxi' or 'Grab' — all are unauthorised per r/DaNang (comments/1k18dh6, 2025). For Hoi An specifically, the going Grab rate is 250K per r/DaNang 'Grab taxi from Da nang airport to Hoi Ann' (comments/1k189nz, 2025); any quote over 700K is overcharging."),
        ("Is Ba Na Hills worth visiting?",
         "Yes in Mar–Nov, probably not in Dec–Feb. Ba Na Hills has the world-famous Golden Bridge, French Village, and cable car — legitimately spectacular. But r/VietNam 'One destination ruined the whole trip. (Ba Na Hill is a scam in Winter months)' (comments/1hk0reg, 2025) documents that December–February often has 95%+ fog at the summit, rendering the experience a washout with no refund. Book the Ba Na Hills combo ticket (1,150,000 VND / $45 USD adult, includes cable car + Alpine Coaster + Fantasy Park) DIRECTLY at banahills.sunworld.vn. Skip hotel 'partner tour' packages at $80-120 per person; book via Klook or GetYourGuide at $60-80 all-in with transfer if you need a guided option. Plan a full day (9 AM arrival, 4 PM departure). At the summit, skip $15 photo-setups and $25 'souvenir jade' shops — both heavily marked up."),
        ("How do I avoid tourist traps in Da Nang and Hoi An?",
         "r/DaNang 'What to scams to look out for in Hoi Ann' (comments/1k18dh6, 2025) gives the 2025 community rule: use Grab for airport transit, skip base-of-Marble-Mountains souvenir shops, and decline all unsolicited 'friendly local' approaches. For My Khe Beach and An Thuong district, NEVER follow a 'friendly local' couple home per r/DaNang 'The Where are you from? couple' (comments/1jrd6sn, 2025) — the 'tea at our family home' pitch leads to overpriced silk/herbs/tea sales. At Dragon Bridge, view the Sat/Sun 9 PM fire show from the railing but arrive 30 minutes early to secure a spot without pushing through crowds. For serious tours (Marble Mountains, Ba Na Hills, Hai Van Pass), book direct via Klook/GetYourGuide — skip hotel-concierge 'partner' kickback arrangements."),
    ],
    "Phu Quoc": [
        ("Is Phu Quoc safe for tourists?",
         "Phu Quoc is broadly safe from violent crime, but 2025 Reddit reports document a specific scam ecosystem around the island's developing-tourism infrastructure. The practical risks for older travellers: PQC airport taxi overcharges and 'no Grab here' claims per r/VietNam 'Grab in Phu Quoc' (comments/1eyk3ng, 2024); pearl farm 'educational tour' hard sells per r/VietNam 'Phu Quoc scam?' (comments/1iiex7f, 2025) — the named 2025 anchor; jet-ski and water-sports damage-deposit scams; massage/spa upcharge pressure per r/VietNam 'I just had super weird experience' (comments/1jjo7c6, 2025); Cable Car 4-island tour package upsells; and hotel/Airbnb off-platform booking fraud per r/VietNam 'Phu quoc hotels full of scam?' (comments/1pj2jm0, 2025). Save Phu Quoc Tourist Police (+84 297 3846 113)."),
        ("What is the most common Phu Quoc scam in 2025?",
         "Pearl farm 'educational tour' hard sells top the list — r/VietNam 'Phu Quoc scam?' (comments/1iiex7f, 2025) and 'Phu Quoc fake pearls?' (comments/1h9j59m, 2025) are the named 2025 anchors documenting 1.2M+ VND fake-pearl necklaces. PQC airport taxi overcharges (drivers quoting 400K+ VND for 150K routes, claiming 'no Grab here') are second most common. Jet-ski deposit-damage scams following the Phuket pattern, massage/spa upcharge pressure, Cable Car 4-island tour upsells ($120 'VIP' versions of $45 standard packages), and hotel/Airbnb off-platform booking fraud round out the top six."),
        ("How do I get from Phu Quoc Airport (PQC) safely?",
         "Book Grab or Xanh SM (VinFast electric) on airport Wi-Fi AFTER luggage. Xanh SM has better 2025 Phu Quoc coverage per r/VietNam 'Grab in Phu Quoc' (comments/1eyk3ng, 2024). Expected fares: PQC to Duong Dong centre 150K–200K VND; to Long Beach 200K–280K VND; to Sunset Town/Vinpearl 250K–350K VND. REFUSE any driver claiming 'no Grab here' — it's false. For Vinpearl resort transfers, use Grab/Xanh SM rather than paying 'official' resort rate 2-3x higher. Many 4-5 star hotels include free airport transfer — verify at booking. If using the airport taxi queue, insist on the meter or confirm fare range above. NEVER accept fixed-price quotes over 400K for central runs."),
        ("How do I buy genuine Phu Quoc pearls without getting scammed?",
         "Skip ALL pearl-farm tour stops — they are sales funnels, not educational per r/VietNam 'Phu Quoc scam?' (comments/1iiex7f, 2025). If you want genuine pearls, visit Long Beach Pearl Farm (Ngọc Trai Phu Quoc, longbeachpearls.com) or Le Quang Pearl — both have fixed prices and GIA certification. Expected genuine prices: $30-60 single freshwater pearl, $100-200 small strand, $200+ small saltwater South Sea strand. NEVER buy pearls at Phu Quoc Night Market — per r/VietNam 'Phu Quoc fake pearls?' (comments/1h9j59m, 2025), 'pearl necklaces' starting at 1.25M VND bargain-down to $50 'final prices' are resin or low-quality freshwater, worth $5-20. Verify pearls with a flashlight test (genuine shows concentric layers) and never accept on-site 'certificate of authenticity' — only GIA or international certification is legitimate."),
        ("Should I book a 4-island boat tour + cable car package?",
         "Book it directly — but choose the 3-island version, not the 4-island. r/VietNam 'Phu Quoc: which 4-island tour option is better? (vs cable' (comments/1rfh3n4, 2025) is the 2025 community-comparison anchor: '3 island + cable car package tour, 4 island is a bit too much' rushed. Book via Klook or GetYourGuide at $35-50 per person (includes boat tour, snorkel gear, lunch). Skip hotel-concierge packages at $70-90 per person and 'VIP island tour' upsells at $120+. The Cable Car standalone is 350K VND one-way / 500K VND return at hontomisland.com. For older travellers or safety-sensitive visitors, r/VietNam 'Phu Quoc, hit or miss?' (comments/1l29ssq, 2025) notes that 'Vinwonders is the last thing to see on Phu Quoc and it has questionable safety standards' — skip VinWonders theme-park add-ons. Pack sunscreen, a hat, and waterproof phone case for the boat portion."),
    ],
    "Nha Trang": [
        ("Is Nha Trang safe for tourists?",
         "Nha Trang is moderately safe — violent crime against tourists is rare but 2025 Reddit reports document escalating theft and scam pressure. r/VietNam 'Việt Nam is not so safe for foreign tourist as everybody talk' (comments/18hi2n1, 2024) captures the harsher community view. The practical risks for older travellers: Cam Ranh Airport (CXR) and street taxi overcharges; beachfront iPhone and valuables theft per r/VietNam 'Just had my iPhone stolen in Nha Trang' (comments/1pw1f3k, 2025); late-night massage/bar solicitation scams per r/nhatrang 'Nha Trang Massage Scam' (comments/1e3klo8, 2025); 4-island booze cruise upsells; Russian-tourist-area dual-menu price discrimination; and hotel off-platform payment fraud. Save Nha Trang Tourist Police (36 Tran Phu, +84 258 3523 273)."),
        ("What is the most common Nha Trang scam in 2025?",
         "Cam Ranh Airport and Nha Trang train station taxi overcharges top the list — r/Vietnam_Tourism 'Nha Trang train taxi scam' (comments/1qw9eqh, 2025) documents a 10x overcharge case (quoted 90K, demanded 900K at destination). Beachfront and pool-side iPhone theft per r/VietNam (comments/1pw1f3k, 2025) is second most common, followed by late-night street-solicited massage scams per r/nhatrang (comments/1e3klo8, 2025), 4-island booze cruise upsells, Russian-tourist-area dual-menu price discrimination, and Booking.com/Agoda off-platform payment fraud."),
        ("How do I get from Cam Ranh Airport to central Nha Trang?",
         "Cam Ranh Airport (CXR) is 35 km south of central Nha Trang — one of Vietnam's longest airport transfers. Legitimate fare: 300K–450K VND by Grab/Xanh SM, 400K–500K VND by licensed Mai Linh (green, 1055) or Vinasun taxi on meter (includes highway toll). The Cam Ranh-Nha Trang shuttle bus is 50K VND but takes 90 minutes. Pre-book hotel transfer if your property offers free CXR pickup — many 4-5 star hotels do. IGNORE every driver approaching in arrivals offering 'Grab ride' or 'taxi' — all are unauthorised. Avoid 'fixed price' quotes of 800K+ VND. r/VietNam 'Why is the ride out of Cam Ranh airport cheaper?' (comments/1cckqw0, 2024) documents the 50-100% price asymmetry favoring the reverse trip; airport-to-city is the higher-scam window."),
        ("Where should I eat in Nha Trang to avoid tourist pricing?",
         "Ask for the Vietnamese-language menu at any restaurant — if they refuse or claim there isn't one, leave. r/VietNam 'I am disgusted that some people defend the act of charging' (comments/1bfnsng, 2024) documents the 'foreigner tax' rationalisation where English/Russian menus show 2-3x the local price for identical dishes. Community-recommended honest-priced Nha Trang venues: Lac Canh Restaurant (Nguyen Binh Khiem — BBQ beef), Yen's Restaurant (Tran Phu — Vietnamese cuisine), Thuan Ngoc Seafood (Cau Da pier — fresh catch), Cafe So 4 (posted-price local). Avoid Tran Phu beachfront restaurants with laminated English/Russian menus and touts outside. For drinks, one block off Tran Phu has beer at 15K-30K VND vs tourist-strip 60K-100K."),
        ("Is Nha Trang worth visiting given all the scams?",
         "Opinions are divided. r/VietNam 'Anybody else find Nha Trang to be pretty good?' (comments/1jvvpq0, 2025) is a 2025 positive community view: 'The people of Nha Trang were wonderful and so welcoming. We ate great food, enjoyed amazi' ng beaches. r/VietNam 'Nha Trang, What to see and skip?' (comments/1oqkirm, 2025) gives the balanced 2025 view. For older travellers, Nha Trang is best as a 2-3 night stop within a broader Vietnam itinerary — long enough to enjoy beach, snorkelling, and the Po Nagar Cham Towers, short enough to avoid the scam-fatigue that 2025 community threads document. Stay at a reputable 4-5 star beachfront resort (InterContinental Nha Trang, Sheraton Nha Trang, Mia Resort, An Lam Retreats Ninh Van Bay); use Grab; skip booze cruises and late-night solicited massages; eat at community-recommended venues. The scam risk is manageable with these rules."),
    ],
    "Sapa": [
        ("Is Sapa safe for tourists?",
         "Sapa is broadly safe from violent crime, but 2025 Reddit reports document a significant rise in transfer fraud and trekking-guide kickback scams. r/VietNam 'Defrauded in Sapa even when booked through official' (comments/1pxdugb, 2025) is a named 2025 anchor. The practical risks for older travellers: Lao Cai station and Sapa bus transfer fraud; Hmong trekking guide kickback-to-shop pressure; hotel/homestay arrival 'upgrade' overcharges per r/VietNam (comments/1pxdugb, 2025); Fansipan cable car weather-closure non-refunds; 'local driver' electric-cart overcharges per r/VietNam 'Just got scammed by a local driver in Sa Pa' (comments/1sifegb, 2025); and village handicraft pressure sales. Save Sapa Tourist Police (Tran Hung Dao Street, Sapa Town)."),
        ("What is the most common Sapa scam in 2025?",
         "Lao Cai station and Hanoi-Sapa bus transfer fraud top the list — r/VietNam 'Defrauded in Sapa even when booked through official' (comments/1pxdugb, 2025) documents multiple 2025 first-person cases where pre-paid packages arrived without the promised last-mile transfer. Hmong trekking guide kickback-to-shop pressure sales are second most common per r/VietNam 'Trip to Sapa, Vietnam: A Mix of Beauty and Beware' (comments/1aom9z8, 2024). Hotel/homestay arrival 'upgrade' demands, Fansipan cable car weather-closure non-refunds, electric-cart 'local driver' overcharges, and village handicraft pressure sales round out the top six."),
        ("How do I get from Hanoi to Sapa safely?",
         "Two legitimate routes: (1) train Hanoi to Lao Cai (9 hours overnight, 400K–1M VND) via dsvn.vn, baolau.com, or 12go.asia, then Grab/Xanh SM from Lao Cai to Sapa (38 km, ~200K VND); (2) bus via The Sinh Tourist (thesinhtourist.vn — verify URL exactly, multiple copycats) at ~600K VND Hanoi-Sapa (6 hours day trip, includes Lao Cai-Sapa last-mile); or private car via Klook/12Go at $80-120 one-way. REFUSE Hanoi Old Quarter 'tourist office' packages — kickback arrangements and missing last-mile transfers per r/VietNam (comments/1pxdugb, 2025). At Lao Cai station, REFUSE any driver claiming to be your pre-paid operator without verification; contact the operator directly. For older travellers, the overnight train sleeper is comfortable (soft sleeper 500K–1M VND per person), and the morning arrival gives a full day in Sapa."),
        ("How do I book a Sapa trek without getting kickback-scammed?",
         "Book trekking guides DIRECTLY via community-recommended operators — r/VietNam 'Local Trekking Guide recomandation for Sapa' (comments/1bbyoa3, 2024) names Sho (WhatsApp +84 365 645 165); r/VietNam 'Sapa and Hà Giang recommendations' (comments/1ghxle8, 2024) names Mayland Trekking. Expected 2025 rate: 500K–800K VND per person for a day trek with lunch, 1-2 villages. REFUSE hotel-concierge 'Sapa trekking' packages at $40-60 per person — kickback arrangements. At villages, REFUSE 'family shop' pressure sales per r/VietNam 'Trip to Sapa' (comments/1aom9z8, 2024); if you want Hmong textiles, visit Bac Ha Sunday Market (2 hours from Sapa by tour) with fixed prices. If Hmong women start following you asking to be 'your guide,' politely decline from the FIRST interaction — agreeing implies acceptance of tip demand at the end."),
        ("Is the Fansipan cable car worth it?",
         "Yes in Mar–Oct with clear weather; probably not in Nov–Feb or during confirmed closure. Fansipan (Vietnam's highest peak, 3,143 m) is served by the world's longest non-stop cable car + funicular. Buy cable car ticket DIRECTLY at fansipanlegend.sunworld.vn (~800K VND adult, 2025) and check weather + Fansipan operational status on the morning of your planned visit — r/Vietnam_Tourism 'Fansipan funicular & cable car closed during my trip' (comments/1o630yd, 2025) documents 2025 closure cases without refund for pre-paid tours. REFUSE hotel-concierge 'Fansipan combo' at $40-60 per person — skip this and book direct. If the cable car is closed, Sapa has alternative day-trip options: Cat Cat Hmong village walk (easy 1-hour flat route), Lao Chai/Ta Van trek, Ham Rong Mountain Park, and Bac Ha Sunday Market. For older travellers or mobility-limited visitors, the cable car is preferable to trekking; bring warm layers (summit is often 10-15°C cooler than Sapa town)."),
    ],
    "Dalat": [
        ("Is Dalat safe for tourists?",
         "Dalat is broadly safe with mild mountain weather and a relaxed atmosphere — violent crime against tourists is very rare. The practical risks for older travellers: Lien Khuong Airport (DLI) taxi overcharge and 'officials' scam per r/VietNam 'Đalat Scam?' (comments/1o70zlp, 2025); unlicensed canyoning operators (2015 British tourist deaths at Datanla Waterfall set the safety baseline); Valley of Love photo-and-ticket pressure per r/VietNam (comments/yrge82, 2024); fake Dalat resort booking pages per r/VietNam 'I got scammed trying to book a stay in Da Lat' (comments/1jb702w, 2025); Night Market food vendor overcharging per r/VietNam (comments/1cg48yb, 2025); and Easy Rider motorbike tour operator fraud. Save Dalat Tourist Police (Tran Phu Street, +84 263 3822 054)."),
        ("What is the most common Dalat scam in 2025?",
         "Fake Dalat resort booking page fraud tops the list — r/VietNam 'I got scammed trying to book a stay in Da Lat' (comments/1jb702w, 2025) documents clone pages that look exactly like legitimate Dalat resorts but take wire-transfer payments for non-existent bookings. Lien Khuong Airport taxi overcharges (with the unusual 'airport officials demanding fees' variant per r/VietNam 'Đalat Scam?' comments/1o70zlp, 2025) are second most common. Canyoning safety-and-pricing scams (unlicensed operators at $25-35 vs. licensed $55-80), Valley of Love photographer-demand scams, Night Market food overcharging, and Easy Rider motorbike tour pricing fraud round out the top six."),
        ("How do I visit Dalat safely and what's worth doing?",
         "Dalat is a highland resort town with a cool climate (16-23°C year-round), French colonial architecture, flower gardens, and coffee plantations. Must-do: Crazy House (Hang Nga Guesthouse, 60K VND), Truc Lam Zen Monastery (free, cable-car access), Dalat Cable Car + Linh Phuoc Pagoda, Dalat Flower Park (60K VND), Datanla Waterfall (80K VND entrance, NOT canyoning for older travellers), Me Linh Coffee Garden. For older travellers considering canyoning: skip it unless you're in excellent physical condition; the 2015 British tourist deaths established that canyoning requires professional operation. Use licensed operators (Viet Challenge, Phat Tire Ventures, Highland Sport Travel) at $55-80/day — refuse $25-35 budget tours per r/solotravel (comments/5y08n4)."),
        ("Should I rent a motorbike or take an Easy Rider tour in Dalat?",
         "Easy Rider pillion tours are community-recommended for older travellers who want to experience the Central Highlands without driving themselves. Use community-vetted operators: Dalat Easy Riders (dalat-easyrider.com), Vietnam Easy Riders, OneTrip Vietnam at $60-80/day full-service including insurance, gear, and luggage transport per r/VietNam 'Thinking about riding a motorcycle from Da Nang to Dalat' (comments/1lak1jo, 2025). A multi-day Dalat-Hoi An Easy Rider trip is $350-450 for 5-6 days. REFUSE street-solicitor offers at $35/day — insurance-less and often unsafe. Alternative for older travellers: pre-book a private car-with-driver via Klook at $60-100/day for local Dalat exploration, $500-700 for Dalat-Hoi An multi-day. Self-drive is NOT recommended — Vietnamese traffic is extreme for international drivers."),
        ("How do I eat at Dalat Night Market without getting overcharged?",
         "Observe what locals pay before ordering — watch which stalls have Vietnamese customers vs tourist-only. Ask price BEFORE ordering, and carry small-denomination notes (10K, 20K, 50K) to avoid 'no change' scams per r/VietNam 'Why do the street food vendors in Da Lat's night market' (comments/1cg48yb, 2025). Expected local prices: bánh tráng nướng (Vietnamese pizza) 20K-30K, strawberries 50K per 500g, soy milk 10K, meat skewers 15-20K each. For sit-down meals off the market, community-recommended posted-menu venues: Long Hoa Restaurant (Nguyen Du), Trong Dong Restaurant (Bac Lieu), Nhat Ly (Khu Hoa Binh). The Night Market is best treated as a photo-stop and light-snack experience rather than a full dinner destination."),
    ],
    "Can Tho": [
        ("Is Can Tho safe for tourists?",
         "Can Tho is broadly safe — r/VietNam 'Planning to go to VN - Can Tho' (comments/1o78ucr, 2025) documents the 2025 local view: 'The living cost in Can Tho is pretty low, it is also quite safe.' The practical risks for older travellers: HCMC-based Mekong Delta day tour kickback stops per r/VietNam 'Is a Mekong Delta day tour from HCMC worth it?' (comments/1irke41, 2025); Cai Rang Floating Market boat overcharges and declining authenticity per r/VietNam (comments/1h79j01, 2024); Can Tho taxi overcharges; Mekong homestay fake-listing fraud; 'coconut candy factory' and 'honey bee farm' commission stops; and unlicensed tour operator fraud per r/VietNam 'It's a bit late now, but is this a legitimate company?' (comments/1rypfl0, 2025). Save Can Tho Tourist Police (Hoa Binh Boulevard)."),
        ("Should I visit the Mekong Delta from HCMC as a day trip?",
         "Probably not as a one-day trip — the community 2025 consensus is that HCMC day tours feel rushed and commercial. r/VietNam 'Is a Mekong Delta day tour from HCMC worth it?' (comments/1irke41, 2025) documents the baseline: 12-hour day with only 90 minutes of actual Mekong experience, mandatory kickback stops at 'coconut candy factory,' 'honey bee farm,' 'traditional music performance,' and tour-operator-owned lunch restaurants. Better options: (1) 2-day/1-night tour with Can Tho overnight via TNK Travel at $60-80 including Cai Rang floating market; (2) travel independently from HCMC to Can Tho by bus (3 hours, 200K VND), stay at community-recommended Nam Bo Boutique Hotel or Ecoco Homestay (Ben Tre), book Cai Rang boat direct at 150-200K VND/hour. For older travellers, the 2-night Ben Tre homestay experience delivers genuine Mekong small-village life vs. tourist-factory loops."),
        ("How do I visit Cai Rang Floating Market at its best?",
         "Arrive at Ninh Kieu Wharf by 5:30-6 AM — Cai Rang is active early morning (5-8 AM) and winds down by mid-day per r/VietNam 'What Are The Hours For Cai Rang Floating Market?' (comments/1iabo9b, 2025). Book boat at the posted-price dock (150K-200K VND per hour for a 2-3 person boat, 2025 rate). A 2-hour tour includes 1 hour upstream to Cai Rang and 1 hour return. r/VietNam 'Cái Răng market in Can tho: is it still good?' (comments/1h79j01, 2024) notes the declining authenticity since 2020 — Cai Rang has fewer floating vendors than in previous decades. Manage expectations: it's a pleasant river experience but not the bustling market of 2010. For 'floating breakfast,' eat at local noodle boats at 30-50K VND rather than the 300K+ VND tourist-boat upsell. For authentic Mekong life, consider overnight at a Ben Tre or Can Tho homestay with cycling through smaller villages."),
        ("Where should I stay in Can Tho and the Mekong Delta?",
         "Book ONLY via Booking.com, Agoda, Airbnb, or Vrbo with platform-verified payment. Skip properties with suspicious review patterns (50+ 5-star in 2-week window). Community-recommended Can Tho hotels: Nam Bo Boutique Hotel (French Colonial, Ninh Kieu Wharf — central, 4.5+ reviews), Vinpearl Hotel Can Tho (5-star riverside), Muong Thanh Luxury Can Tho, TTC Hotel Premium. For authentic Mekong homestays, r/VietNam 'less-touristy Mekong Delta tours?' (comments/1fnt2d6, 2025) names Ecoco Homestay (Ben Tre — 'super lovely family running the place'). Other community-recommended: Nguyen Shack (Can Tho — boutique homestay), Mango Home Riverside (Ben Tre), Lien Hiep Thanh Homestay. Expected cost: $15-30 per person per night including breakfast at homestays, $50-80 at 3-star hotels, $100+ at Nam Bo Boutique or Vinpearl. REFUSE WhatsApp off-platform deposit requests."),
        ("How do I pick a legitimate Mekong Delta tour operator?",
         "Book ONLY via licensed platforms: Klook, GetYourGuide, Viator, TripAdvisor Experiences — each requires operator verification. If booking directly, ask for the International Tour Operator License (Giấy phép kinh doanh lữ hành quốc tế) and verify at vietnamtourism.gov.vn per r/VietNam 'It's a bit late now, but is this a legitimate company?' (comments/1rypfl0, 2025). Pay by credit card only — refuse wire transfer, Bizum, or cryptocurrency. Community-recommended Mekong tour operators: TNK Travel (tnktravel.com), Les Rives (lesrivesexperience.com), Saigon Happy Tour (saigonhappytour.com), Ecoco Homestay (ecocohomestay.com for 2-day/1-night Ben Tre overnights). Expected 2D/1N Mekong tour cost: $60-100 per person; anything under $40 is scam-tier or unlicensed. Decline operator 'coconut candy factory' and 'honey bee farm' kickback stops — they're pure sales funnels."),
    ],
    "Petra": [
        ("Is Petra safe for tourists?",
         "Petra and the town of Wadi Musa are generally safe for tourists. Jordan has a relatively low crime rate. The main risks are financial — overpriced animal rides, unofficial guides charging inflated rates, and vendors dramatically overcharging for souvenirs. The Bedouin romance scam targeting solo female travelers is a more serious concern."),
        ("What is the most common scam in Petra?",
         "The 'free' animal ride scam is Petra's most persistent issue — handlers offer a 'free' camel or donkey ride then demand $50+ when you try to dismount. Unofficial guides who approach at the entrance and later demand inflated fees are the second most common complaint. Always agree on prices before accepting any service."),
        ("How much does Petra cost?",
         "A one-day Petra entry ticket costs 50 JD (~$70) for foreigners, 55 JD for two days, 60 JD for three days. The Jordan Pass (from 70 JD) includes Petra entry and visa fee — it's the best value for most visitors. Guide prices at the official Visitor Centre start around 50 JD for a half-day. Budget 50-100 JD per day total including food and transport."),
        ("Is the Bedouin romance scam real?",
         "Yes — it's well-documented in online forums and by local authorities. Young Bedouin men build fast romantic connections with female tourists, ultimately requesting money, gifts, or visa assistance. Facebook groups like 'Stop the Petra Bedouin Women Scammers' contain detailed firsthand accounts. Be cautious of fast-moving romantic interest from anyone you meet inside the archaeological site."),
        ("How long do I need at Petra?",
         "A minimum of one full day is needed to see the main sites (Siq, Treasury, Street of Facades, Monastery). Two days allows you to explore at a more relaxed pace and see lesser-known trails. The walk from the entrance to the Monastery is 8km round trip — wear comfortable shoes and bring plenty of water."),
    ],
    "Jerusalem": [
        ("Is Jerusalem safe for tourists?",
         "Jerusalem is generally safe for tourists in the main tourist areas — the Old City, Western Wall, Mount of Olives, and modern West Jerusalem. The political situation can cause sudden security incidents, so check current advisories before visiting. The Old City is heavily policed and safe for walking. Use common sense about demonstrations and avoid border areas."),
        ("What is the most common scam in Jerusalem?",
         "Overcharging at Old City market shops and aggressive shopkeepers who pressure tourists into purchases are the most common complaints. Unlicensed tour guides who demand inflated fees and taxi overcharging near Damascus Gate are also frequently reported. The 'free tour' that ends at a specific shop is a classic Old City move."),
        ("How do I get around Jerusalem?",
         "The Jerusalem Light Rail runs from Mount Herzl through the city center to Pisgat Ze'ev. Egged buses cover most areas. The Gett app works for taxis — metered rides are reliable. Walking is the best way to explore the Old City (it's compact — under 1 km across). Avoid accepting rides from unlicensed drivers near tourist sites."),
        ("Is the Old City safe to walk through?",
         "The Old City is safe to walk through during the day, including all four quarters (Jewish, Christian, Muslim, Armenian). The Muslim Quarter is the most atmospheric market area. At night, stick to well-lit areas and main routes. Israeli police and military presence is constant and visible. Be respectful of religious customs at all holy sites."),
        ("What should I wear in Jerusalem?",
         "Modest dress is expected at all religious sites — shoulders and knees covered for both men and women. The Western Wall, Church of the Holy Sepulchre, and Al-Aqsa Mosque all enforce this. Carry a scarf or shawl. In modern West Jerusalem (Mamilla, Ben Yehuda Street), casual dress is fine. Comfortable walking shoes are essential for the Old City's stone streets."),
    ],
    "Reykjavik": [
        ("Is Reykjavik safe for tourists?",
         "Reykjavik is one of the safest capitals in the world. Violent crime is virtually nonexistent. The main tourist risks are financial — rental car damage scams, overpriced tours, and the general high cost of everything in Iceland. Nature-related risks (weather, terrain) are more dangerous than any human threat."),
        ("What is the most common scam in Reykjavik?",
         "Rental car damage claims are Iceland's most reported tourist scam — agencies charge tourists for pre-existing damage to gravel-road vehicles. Photograph every angle of your rental before driving. Budget tour operators who cancel Northern Lights trips without refunds are the second most common complaint."),
        ("How expensive is Iceland really?",
         "Very expensive — budget $75-100/day minimum for food alone. A restaurant meal costs $25-40, a beer $10-15, gas $2.50/liter. The Bonus supermarket (look for the pink pig logo) is the budget traveler's best friend. Hot dogs from Bæjarins Beztu are a cheap Reykjavik institution at ~$5. Accommodation outside Reykjavik is significantly cheaper."),
        ("Do I need a car in Iceland?",
         "For the Golden Circle and Ring Road, yes — a car is essential. In Reykjavik itself, walking covers all major attractions. Book rental cars well in advance in summer. Choose full coverage insurance (especially gravel/ash protection for the highlands). A 4WD is required for F-roads and strongly recommended for winter travel."),
        ("When can I see the Northern Lights?",
         "Northern Lights are visible from September through March, with peak viewing in October-February. No tour can guarantee sightings — they depend on solar activity, cloud cover, and darkness. Book with operators who offer free rebooking if lights aren't seen. The Icelandic Met Office (vedur.is) has a real-time aurora forecast."),
    ],
    "Edinburgh": [
        ("Is Edinburgh safe for tourists?",
         "Edinburgh is one of the safest major cities in Europe. Violent crime targeting tourists is extremely rare. The main risks are pickpocketing during the Edinburgh Festival (August), minor overcharging at Royal Mile tourist shops, and the occasional unlicensed taxi at night near Cowgate and Grassmarket pubs."),
        ("What is the most common scam in Edinburgh?",
         "Tourist markup at whisky shops and souvenir stores on the Royal Mile is the most common complaint — prices are 50-100% higher than at supermarkets or specialist shops off the Mile. Pickpocketing in Festival crowds (August) is the most common crime. Edinburgh doesn't have the aggressive street scam culture of larger European cities."),
        ("Is the Edinburgh Festival safe?",
         "The Edinburgh Fringe (August) is one of the world's great cultural events and is overwhelmingly safe. The massive crowds do create pickpocket opportunities — keep valuables secure in front pockets. Book accommodation well in advance as prices triple. Free shows (PBH Free Fringe) are genuinely excellent and save money."),
        ("How do I get from Edinburgh Airport to the city?",
         "The Airlink 100 bus runs every 10 minutes to Waverley Bridge (city center) for £4.50 — fast and reliable. The tram runs to York Place via Princes Street for £6.50. Taxis cost £25-35 by meter. Uber operates. All are safe options. Avoid any driver who approaches you inside the terminal."),
        ("What areas of Edinburgh are best for tourists?",
         "The Old Town (Royal Mile, Grassmarket, Cowgate) has the historic attractions, restaurants, and nightlife. The New Town (Princes Street, George Street) has shopping and elegant architecture. Leith has Edinburgh's best restaurant scene at more reasonable prices. Stockbridge has excellent local cafes and the Sunday market. All are safe areas."),
    ],
    "Bruges": [
        ("Is Bruges safe for tourists?",
         "Bruges is one of the safest cities in Europe. Violent crime is virtually nonexistent. The main risks are tourist overcharging at restaurants on the Markt square and overpriced chocolate shops near the Belfry. Bike theft happens but is the only notable property crime. Bruges requires minimal safety awareness."),
        ("What is the most common scam in Bruges?",
         "Restaurant overcharging on the Markt square is the most consistent complaint — the same Belgian dishes cost 2-3x more than at restaurants on side streets just meters away. Overpriced chocolate at tourist-facing shops near the Belfry is the second most common trap. Neither is aggressive or dangerous — just expensive."),
        ("Is Belgian chocolate from tourist shops good?",
         "The chocolate itself is usually decent but dramatically overpriced near the Markt and Belfry. Locals buy from Dumon (quiet street near the Markt), The Chocolate Line (creative flavors), or BbyB (ultra-premium). Leonidas is mass-market but consistently good value. A 250g box at a tourist shop costs what a 500g box costs at a local chocolatier."),
        ("How do I get from Brussels to Bruges?",
         "Direct trains from Brussels-Midi/Zuid run every 30 minutes and take 55-65 minutes. Buy tickets at the NMBS/SNCB counter or app — prices are fixed (no advance booking advantage). Bruges station is a 15-minute walk from the Markt. Don't take a taxi from the station unless you have heavy luggage — the walk is pleasant and safe."),
        ("Can I do Bruges as a day trip?",
         "Yes — Bruges is compact and walkable, and most visitors see the highlights in one day. However, staying overnight lets you experience the magical emptiness after day-trippers leave (by 6pm, the Markt is quiet). An overnight also lets you visit the lesser-known spots like the Begijnhof at dawn and the quiet canals without crowds."),
    ],
    "Nice": [
        ("Is Nice safe for tourists?",
         "Nice is generally safe for tourists. The main risks are pickpocketing on the Promenade des Anglais, motorbike-based phone/bag snatching near the Old Town, and beach theft. The Vieux Nice (Old Town) area is safe to walk at night. Nice has lower crime rates than Paris or Marseille but higher than smaller Riviera towns."),
        ("What is the most common scam in Nice?",
         "Beach theft — bags and valuables stolen from unattended towels — is Nice's most common tourist crime. Motorbike snatches of phones and bags along the Promenade des Anglais are the second most reported issue. Restaurant overcharging in Vieux Nice (verbal prices differing from the bill) is also documented."),
        ("How do I get from Nice Airport to the city?",
         "Tram Line 2 runs from the airport to the city center (Jean Médecin, Garibaldi) for €1.50 — fast and easy. Bus 98 goes to the port. Airport taxis have fixed rates: €20 to the city center (left bank), €32 to the right bank. Any taxi charging more is overcharging. Uber also operates from the airport."),
        ("Is the French Riviera expensive?",
         "Nice is expensive by French standards but more affordable than Monaco or Saint-Tropez. A restaurant meal costs €15-25, a coffee €2-4. The Cours Saleya market has fresh produce at reasonable prices. Free beaches exist alongside private beach clubs. Budget accommodation exists in the Nice Riquier and Liberation neighborhoods."),
        ("What beaches are free in Nice?",
         "Most of Nice's beach along the Promenade des Anglais is public and free — look for the open sections between the private beach clubs. The beaches are pebble, not sand. Bring a towel and water shoes. Castel Plage (below the Castle Hill) is a popular free section. Don't leave valuables on your towel — bring only what you can watch."),
    ],
    "Split": [
        ("Is Split safe for tourists?",
         "Split is one of Croatia's safest cities for tourists. Violent crime is very rare. The main risks are minor overcharging at waterfront restaurants on the Riva, unlicensed taxi overcharging at the ferry port, and occasional pickpocketing in Diocletian's Palace crowds. Overall, Split is very safe and tourist-friendly."),
        ("What is the most common scam in Split?",
         "Restaurant overcharging on the Riva waterfront — unlisted cover charges, bread fees, and service charges appearing on bills — is the most common complaint. Unlicensed taxi overcharging at the bus station and ferry port, particularly refusing to use meters, is the second most reported issue. Use Bolt or Uber."),
        ("How do I get to Hvar from Split?",
         "Jadrolinija operates car ferries from Split to Stari Grad (Hvar) — about 2 hours. Krilo and TP Line run high-speed catamarans from Split to Hvar Town in about 1 hour. Book through the official Jadrolinija website or the Krilo website. Touts at the port sell the same tickets at inflated prices — buy direct."),
        ("Is Diocletian's Palace safe to explore?",
         "Diocletian's Palace is Split's main attraction and is perfectly safe. It's a living part of the city with shops, restaurants, and residences inside the ancient walls. 'Impromptu' guides who approach at the entrance are the main annoyance — they're not dangerous but agree on a price if you accept their services. Self-guided visits are easy."),
        ("What's the best way to eat in Split?",
         "Avoid restaurants directly on the Riva waterfront for the best value. Walk into the residential streets behind the Palace (Varoš neighborhood) or east toward Bačvice for local-quality food at 40-60% lower prices. The Green Market (Pazar) has fresh produce. Konoba-style restaurants serve traditional Dalmatian food and are generally honest about pricing."),
    ],
    "Phnom Penh": [
        ("Is Phnom Penh safe for tourists?",
         "Phnom Penh requires more awareness than many Southeast Asian capitals. Bag snatching from motorbikes is a real and common risk. The tourist areas (Riverside, BKK1, Russian Market) are manageable with basic precautions. Violent crime targeting tourists is uncommon but petty theft is frequent. Keep bags secure and use ride apps."),
        ("What is the most common scam in Phnom Penh?",
         "Motorbike bag snatching is the most common and most dangerous crime — thieves on motorbikes grab bags from pedestrians and tuk-tuk passengers. Tuk-tuk overcharging near the Royal Palace and at the airport is the most common scam. 'Shooting range' tour scams outside the city are also well-documented."),
        ("How do I get around Phnom Penh safely?",
         "Use the PassApp or Grab app for tuk-tuks and taxis — prices are fixed and drivers are accountable. Keep bags on your lap (not the seat) in tuk-tuks. Walking is fine in BKK1 and along the Riverside but keep bags on the shoulder away from the road. Motorbike taxis (motos) are cheap but riskier for bag theft."),
        ("Is the Killing Fields safe to visit?",
         "The Choeung Ek Killing Fields memorial is 15km outside the city and is safe to visit. Take a tuk-tuk or Grab there and back. The audio tour is highly recommended. The site is a deeply moving historical experience. Book your transport in advance and agree on a round-trip price including waiting time at the site."),
        ("What areas of Phnom Penh are best for tourists?",
         "BKK1 (Boeung Keng Kang 1) is the safest and most convenient neighborhood for tourists — walkable, with excellent restaurants and cafes. The Riverside area near the Royal Palace is atmospheric but more targeted by bag snatchers. The Russian Market area (Toul Tom Poung) is great for shopping and dining. Avoid wandering alone in unfamiliar areas at night."),
    ],
    "Siem Reap": [
        ("Is Siem Reap safe for tourists?",
         "Siem Reap is generally safe and very tourist-oriented. The town exists primarily to serve Angkor Wat visitors. Violent crime targeting tourists is rare. The main risks are tuk-tuk/tour overcharging, fake Angkor tickets, and overpriced restaurants on Pub Street. Keep phones and bags secure and you'll have a comfortable visit."),
        ("What is the most common scam in Siem Reap?",
         "Tuk-tuk drivers who overcharge for Angkor temple tours or skip temples to save fuel are the most common complaint. Fake Angkor passes (sold anywhere other than the official ticket office on Apsara Road) are a serious scam. Restaurant price inflation on Pub Street — particularly menus showing USD instead of local prices — is also common."),
        ("How much should an Angkor tuk-tuk tour cost?",
         "A full-day tuk-tuk tour of the main Angkor temples (small circuit) should cost $15-20 USD. The Grand Circuit adds $5-10. Sunrise tours start at $12-15. Agree on the itinerary and price before starting. Your hotel can arrange a reputable driver — this is usually the safest option and prices are standard."),
        ("Should I buy an Angkor pass in advance?",
         "Angkor passes can only be purchased at the official ticket office on Apsara Road or online at angkorwat.online. One-day ($37), three-day ($62), or seven-day ($72) passes are available. The ticket office opens at 5:00am for sunrise visitors. Never buy from touts, hotels, or third parties — they're either fake or resold at a markup."),
        ("Is Pub Street safe at night?",
         "Pub Street is Siem Reap's nightlife center and is generally safe — it's well-lit, busy, and has a party atmosphere. The main risks are overpriced drinks (check prices before ordering), bag theft in crowded bars, and over-enthusiastic bar promoters. Don't leave drinks unattended. The surrounding streets are safe to walk back to nearby hotels."),
    ],
    "Manila": [
        ("Is Manila safe for tourists?",
         "Manila requires significant awareness compared to other Southeast Asian capitals. The tourist areas (Intramuros, Makati, BGC) are manageable, but phone/bag snatching and pickpocketing are extremely common in crowded areas like Divisoria Market. Violent crime exists but rarely targets tourists in tourist zones. Use Grab for all transport."),
        ("What is the most common scam in Manila?",
         "Taxi meter fraud is Manila's most persistent tourist scam — drivers either have rigged meters, refuse to use them, or 'forget' to turn them on. Grab has largely solved this problem. Phone snatching in crowded markets and on jeepneys is the most common theft crime. Keep electronics completely hidden in crowds."),
        ("Is Grab safe in Manila?",
         "Yes — Grab is by far the safest transport option in Manila. All drivers are registered, prices are fixed, and you have GPS tracking. It eliminates the taxi meter scam entirely. GrabCar is preferred over GrabTaxi (which uses regular taxis). Book rides from inside buildings when possible."),
        ("What areas of Manila are safe for tourists?",
         "Makati (business district), BGC/Taguig (modern, walkable), and Intramuros (historic walled city) are the safest tourist areas. Mall of Asia area is safe. Avoid Tondo, parts of Quiapo, and unfamiliar areas outside the tourist circuit at night. Divisoria Market is a must-see but requires extreme vigilance with belongings."),
        ("How do I get from Manila Airport to the city?",
         "Grab is the safest and most reliable option — book from inside the terminal. The fixed-rate yellow airport taxis are the next best option (coupon system from the taxi counter inside arrivals). Regular white taxis are less reliable. Avoid anyone approaching you inside the terminal offering rides. A Grab to Makati costs 200-400 PHP."),
    ],
    "Havana": [
        ("Is Havana safe for tourists?",
         "Havana is one of the safer capitals in Latin America — violent crime targeting tourists is relatively rare. The main risks are pervasive hustling (jineteros), taxi overcharging, counterfeit cigars, and currency confusion. The tourist areas (Old Havana, Vedado, Miramar) are safe for walking day and night with basic awareness."),
        ("What is the most common scam in Havana?",
         "Jineteros (hustlers) are Havana's most pervasive issue — they approach tourists offering cigars, restaurants, taxis, and casa particular recommendations at inflated prices that include their commission. Counterfeit cigars sold on the street (even in convincing boxes) are the most common product scam. Buy only from official La Casa del Habano shops."),
        ("How does currency work in Havana?",
         "Cuba primarily uses the Cuban Peso (CUP). The old dual-currency system (CUC/CUP) ended in 2021. Some tourist businesses quote in USD. Confirm which currency you're being charged in before paying. ATMs dispense CUP but may not work with all foreign cards. Bring clean USD or EUR cash as backup and exchange at official CADECA offices."),
        ("Are classic car taxis safe?",
         "Classic American car taxis are one of Havana's iconic experiences and generally safe. Negotiate the fare before getting in — there are no meters. A ride within Old Havana should cost 5-10 USD. Airport to Old Havana is 25-30 USD. Official yellow taxis (modern cars) are also reliable. Avoid unlicensed vehicles."),
        ("Can I use the internet in Havana?",
         "Internet access in Cuba is limited and expensive. ETECSA WiFi cards provide 1 hour of access at public hotspots (parks, hotels). Some hotels have WiFi. Mobile data packages are available but slow. Don't rely on internet for navigation — download offline maps before arriving. Many restaurants and casa particulares now offer WiFi."),
    ],
    "San Juan": [
        ("Is San Juan safe for tourists?",
         "Old San Juan and the Condado/Isla Verde hotel zones are generally safe for tourists. Puerto Rico is a US territory, so familiar safety standards apply. Petty theft — particularly beach theft and phone snatching — is the main risk. Some neighborhoods outside the tourist zones have higher crime rates. Use standard urban awareness."),
        ("What is the most common scam in San Juan?",
         "Beach theft — bags and valuables stolen from unattended towels at Condado Beach and Isla Verde — is the most common tourist crime. Overcharging at souvenir shops near the cruise port (50-200% markup over shops a few blocks inland) is the most common financial trap. Both are easily avoidable."),
        ("How do I get around San Juan?",
         "Uber and Lyft operate throughout San Juan and are reliable. The AMA bus system covers major routes but can be slow. Old San Juan is compact and walkable. Taxis use meters — from the airport to Condado costs about $15-20. The ferry to Cataño ($0.50) is a fun, cheap harbor experience. Rental cars are useful for exploring outside San Juan."),
        ("Is Old San Juan worth visiting?",
         "Absolutely — Old San Juan is one of the oldest European-founded settlements in the Americas. The forts (El Morro and San Cristóbal) are free on some days and always affordable. The colorful colonial streets are beautiful for walking. Visit on a non-cruise-ship day for fewer crowds. Evening on the city walls watching sunset is spectacular and free."),
        ("What's the food scene like in San Juan?",
         "San Juan has an excellent food scene. Mofongo, lechón, and local seafood are highlights. La Placita de Santurce (Saturday night) is a must-experience local food and nightlife market. Old San Juan restaurants near the cruise port are tourist-priced — walk a few blocks inland for better value. Pincho stands and local bakeries offer the best cheap eats."),
    ],
    "Medellín": [
        ("Is Medellín safe for tourists?",
         "Medellín has improved dramatically in safety but still requires more vigilance than most tourist destinations. El Poblado and Laureles are the safest neighborhoods for tourists. Phone snatching, express robbery via unlicensed taxis, and scopolamine drugging are real risks. Use Uber/InDriver exclusively for transport. Never accept drinks from strangers."),
        ("What is the most common scam in Medellín?",
         "Scopolamine (burundanga) drugging is Medellín's most dangerous and well-documented tourist threat — victims are drugged via drinks, food, or even paper, then robbed of everything. Phone snatching by motorbike is the most common daily crime. Express robbery in unlicensed taxis also occurs — use Uber or InDriver exclusively."),
        ("Is El Poblado safe?",
         "El Poblado is the safest neighborhood for tourists in Medellín and where most visitors stay. Parque Lleras has restaurants, bars, and nightlife. The neighborhood is walkable during the day. At night, take Uber between venues even within El Poblado. Keep phones hidden when walking. The Metro connects El Poblado to the rest of the city safely."),
        ("Should I visit Comuna 13?",
         "Comuna 13 is one of Medellín's most popular tourist attractions — the outdoor escalators, street art, and transformation story are genuinely impressive. Visit with a licensed tour operator (book through your hotel or on TripAdvisor). Unlicensed guides who approach at the base may lead to less safe areas. Go during daylight hours."),
        ("How do I get from Medellín Airport to the city?",
         "José María Córdova International Airport is 45 minutes from the city. Official airport buses run to the San Diego mall terminal in El Poblado — safe and cheap. Uber operates from the airport. Official airport taxis have fixed rates (~80,000-100,000 COP to El Poblado). Never accept rides from drivers who approach you inside the terminal."),
    ],
    "Osaka": [
        ("Is Osaka safe for tourists?",
         "Osaka is extremely safe — one of the safest major cities in the world. Violent crime targeting tourists is virtually nonexistent. The main risks are minor — overcharging at tourist-facing Dotonbori restaurants, bar touts in Namba, and increasing pickpocketing in very crowded areas. Osaka is significantly more relaxed than Tokyo about nightlife."),
        ("What is the most common scam in Osaka?",
         "Overcharging at Kuromon Market (prices have risen 2-3x for tourists in recent years) is the most common complaint. Bar touts in Dotonbori and Namba occasionally lead tourists to overpriced venues, though this is far less prevalent than in Tokyo's Kabukicho. Overall, Osaka has very few active scams — it's remarkably honest."),
        ("Is Dotonbori safe at night?",
         "Dotonbori is safe at night and is one of Osaka's best nighttime experiences — the neon signs, Glico Man, and street food are iconic. Keep wallets secure in the crowds (front pockets) and be cautious of bar touts, but the area is overwhelmingly safe. Shinsekai, another atmospheric nightlife district, is also safe."),
        ("How do I get from Kansai Airport to Osaka?",
         "The Haruka Express train runs from KIX to Tennoji (35 min) and Shin-Osaka (50 min). The Nankai Rapi:t goes to Namba (34 min) — both are fast and reliable. Limousine buses run to multiple hotels. Taxis are metered and honest but very expensive (~¥15,000+). The JR Kansai Airport Rapid is the cheapest option (~¥1,210 to Osaka Station)."),
        ("What street food should I try in Osaka?",
         "Osaka is Japan's street food capital. Must-try items: takoyaki (octopus balls), okonomiyaki (savory pancakes), kushikatsu (deep-fried skewers), and gyoza. Dotonbori and Shinsekai are the classic street food areas. Kuromon Market has high-quality seafood but at tourist-inflated prices — Namba Yasaka Shrine area stalls offer better value for similar quality."),
    ],
    "Paris": [
        ("Is Paris safe for tourists?",
         "Paris is generally safe for tourists, though pickpocketing is endemic at tourist hotspots — the Eiffel Tower, Louvre, Notre-Dame, and the RER B airport line see the highest rates. Violent crime targeting tourists is uncommon. The main districts — 1st through 8th arrondissements — are safe to walk day and night. Stay aware in crowded metro carriages and keep valuables secured."),
        ("What is the most common scam in Paris?",
         "The 'petition' scam near Sacré-Cœur and the Eiffel Tower is the most reported: groups approach tourists with clipboards for 'deaf children,' distract them, and pick their pockets — or pressure them to donate large sums. The 'friendship bracelet' scam (a string tied to your wrist, then aggressively charged) is the second most common."),
        ("How do I get from Charles de Gaulle Airport to Paris?",
         "The RER B train is the fastest (35 minutes to Châtelet-Les Halles) and cheapest option (€11.80). Keep your bag in your lap the entire journey — it's a known pickpocket corridor. Uber is reliable and takes 45–75 minutes depending on traffic (€50–€70). Official licensed taxis have fixed fares: €52 to the Right Bank, €58 to the Left Bank."),
        ("Are Paris taxis safe?",
         "Licensed Parisian taxis (white cars with the illuminated T on the roof) are metered and regulated. Only take taxis from official ranks or book via the G7 app. Unlicensed touts at CDG and Gare du Nord will approach you — ignore them. The meter should be running from the start of the journey; if not, insist immediately."),
        ("Is it worth buying a Paris Museum Pass?",
         "The Paris Museum Pass (2, 4, or 6 days) provides free entry to 50+ museums including the Louvre, Orsay, and Versailles. It pays for itself if you visit 3+ major museums. Buy only from official tourist offices, the Paris Tourist Office website, or museum ticket desks — counterfeit passes are sold near attractions. It does not include skip-the-line priority; book timed entry slots in advance for the Louvre regardless."),
    ],
    "Rome": [
        ("Is Rome safe for tourists?",
         "Rome is generally safe for tourists but has a higher pickpocketing rate than many European capitals. The Metro A line, the Colosseum area, Trastevere, and Termini station have the most incidents. Violent crime targeting tourists is rare. The main risks are petty theft and restaurant overcharging. Take normal precautions and Rome is a wonderful, manageable city."),
        ("What is the most common scam in Rome?",
         "Pickpocketing on the Metro A line (connecting Vatican, Spanish Steps, and Termini) is the most reported tourist crime. Restaurant overcharging near the Colosseum, Trevi Fountain, and Vatican — including unexpected 'coperto' charges and tourist-priced menus — is the second most common complaint."),
        ("How do I get from Rome's airports to the city?",
         "From Fiumicino (FCO): Leonardo Express train to Termini station takes 32 minutes and costs €14 — the fastest option. Licensed white taxis have a fixed flat rate of €48 to anywhere within the city center. From Ciampino (CIA): Terravision or SIT Bus shuttle coaches run to Termini for €4–€6. Always book buses online in advance."),
        ("What is the 'coperto' charge in Rome restaurants?",
         "'Coperto' is a cover charge (typically €1.50–€3.50 per person) that is legally required to be listed on the menu — it covers bread and table service. It is legitimate when disclosed. The scam version is unlisted coperto appearing on your bill for the first time. Always review your printed bill against the menu, and if a charge wasn't on the menu, you can legally refuse it."),
        ("Are the Colosseum skip-the-line tickets worth buying?",
         "Yes — absolutely buy timed entry tickets online in advance from the official site (coopculture.it). The queue for walk-up tickets can be 2–3 hours in peak season. 'Skip-the-line' tickets from street sellers outside are frequently counterfeit or expired. Only buy from the official website or from verified resellers like GetYourGuide and Viator, who guarantee replacement if tickets fail."),
    ],
    "Bangkok": [
        ("Is Bangkok safe for tourists?",
         "Bangkok is generally safe for tourists. Violent crime against visitors is rare, and the city is overwhelmingly welcoming. The primary risks are financial scams — gem scams, tuk-tuk tours, and taxi overcharging — rather than physical danger. Neighborhoods like Sukhumvit, Silom, and the old town are safe to walk at night with basic awareness."),
        ("What is the most common scam in Bangkok?",
         "The gem scam is Bangkok's most financially devastating tourist con — tourists are taken to gem stores via tuk-tuk drivers or 'friendly locals,' told a false story about a special one-day export event, and sold worthless stones at vastly inflated prices. The Grand Palace 'closed today' redirect scam (to a gem store) is the most common entry point."),
        ("How do I get from Suvarnabhumi Airport to Bangkok?",
         "The Airport Rail Link (City Line) runs every 12 minutes to Phaya Thai station (47 minutes, ฿45) — cheapest option. The Express Line to Makkasan or Phaya Thai takes 17–18 minutes (฿150). Metered taxis from the official rank in the basement are reliable — insist on the meter and budget ฿200–฿350 plus expressway tolls (฿45–฿75). Avoid any driver who quotes a flat price above the expected meter fare."),
        ("Are tuk-tuks safe in Bangkok?",
         "Tuk-tuks are safe as a transport mode and are a genuine local experience. The scam to avoid is a driver offering a 'tour' for an impossibly low price (20–50 baht) — the route will include gem stores, tailor shops, or Buddha amulet vendors who pay the driver commission. You'll be pressured to buy. Pay a normal tuk-tuk fare (฿50–฿150 per trip) and tell the driver specifically where you want to go."),
        ("What neighborhoods are best in Bangkok?",
         "Sukhumvit (Nana to Ekkamai) has excellent food, bars, and nightlife. Silom/Sathon is the financial district with great restaurants. The Old Town (Rattanakosin) has all the historic temples — Wat Pho, Grand Palace, Wat Arun. Ari is the trendy local neighborhood for cafés. Avoid the Khao San Road party area if you prefer a less tourist-saturated experience, though it's perfectly safe."),
    ],
    "Istanbul": [
        ("Is Istanbul safe for tourists?",
         "Istanbul is generally safe for tourists in the main tourist areas — Sultanahmet, Beyoğlu/Taksim, and Kadiköy. Violent crime targeting visitors is uncommon. The primary risks are financial scams (carpet shops, tea invitations, bar traps) and petty theft in crowded markets. Solo female travelers report more harassment than in Western European cities but the city is manageable with awareness."),
        ("What is the most common scam in Istanbul?",
         "The 'friendly local' bar trap near Taksim and Sultanahmet is the most financially damaging scam — tourists are befriended, taken to a bar, and presented with a bill for hundreds or thousands of dollars for drinks. The carpet shop 'tea invitation' is the most common lead-in scam: a friendly chat, free tea, then aggressive sales pressure in a shop you didn't plan to enter."),
        ("How do I get from Istanbul Airport to the city?",
         "The Havataş airport bus to Taksim Square takes 45–75 minutes and costs ₺250. Metro line M11 to Gayrettepe (connection to M2 for Taksim) takes about 38 minutes and costs ₺44. Official taxis from the airport are metered — expect ₺700–₺1,200 to central Istanbul. Uber operates as a premium option. Avoid any drivers who approach you before the official taxi rank."),
        ("Is the Grand Bazaar safe?",
         "The Grand Bazaar is safe to walk through and is a genuine historic market experience. The risks are financial rather than physical: all initial prices are massively inflated for tourists, persistent sales pressure can be uncomfortable, and there are occasional reports of short-changing. Treat it as a browsing experience, negotiate firmly on anything you want to buy (start at 25–30% of the quoted price), and don't feel obligated to buy because you were shown many items."),
        ("Can I drink alcohol in Istanbul?",
         "Yes — Turkey is a secular country and alcohol is legal and widely available in Istanbul. Raki (anise spirit) is the traditional drink. The main practical concern is price: tourist-area bars charge significantly more than local meyhane (tavern) venues. Avoid any bar that doesn't have a visible menu with prices — this is where the bar trap scam starts per r/solotravel 'I met a lot of creepy people while I was in Istanbul' (comments/yctw4z, 2024). Alcohol is not served in conservative neighborhoods like Fatih."),
    ],
    "Marmaris": [
        ("Is Marmaris safe for tourists?",
         "Marmaris is broadly safe for older package-holiday travelers — violent crime against tourists is rare and resort areas are well-policed. The practical risks are financial: Dalaman Airport (DLM) transfer overcharges, Bar Street card-skimming (cross-pattern with Alanya per r/Alanya 'Be aware of this scam'), İçmeler beach restaurant tourist-menu inflation, boat tour bundle hidden charges, Rhodes ferry reseller markups, and resort-strip 'authentic Turkish bath' hammam upsells. Save Tourism Police 155 and Marmaris Belediyesi Tourism Office +90 252 412 1035."),
        ("How do I get from Dalaman Airport (DLM) to Marmaris?",
         "Most package-tour operators (TUI, Jet2, easyJet Holidays, Tez Tour, Anex Tour) include free coach transfer from DLM — confirm this BEFORE arrival. For independent travelers, the Havaş airport bus to Marmaris otogar runs €8 per person in 90 min. Licensed taxi from DLM (90 km) is ₺1,200–₺1,600 (€30–€40) on Tarife 1. Refuse 'fixed price' quotes over €60. Welcome Pickups (€35–€45 per car for up to 4 people) is the vetted private alternative. Uber does NOT operate in Marmaris; only BiTaksi and licensed taxis."),
        ("How do I avoid Marmaris boat-tour overcharging?",
         "Book with named vetted operators (Bayan Boat Tours, Tradewinds Sailing, V-Go Yachting) at €25–€40 per person — anything under €20 means hidden drink charges, mandatory tips, and Hisarönü/İçmeler shopping stops on return per r/AskTurkey 'Travelling to Dalaman, Pamukkale and Marmaris' (comments/1cg6m8l). Confirm in writing: lunch included, drinks at posted prices, no shopping stop on return, no 'mandatory tip,' specific number of swim stops. Bring your own swimwear, towel, sunscreen, and refillable water bottle to avoid on-board upsells."),
        ("Is the Marmaris-Rhodes ferry safe?",
         "Yes — the daily catamaran ferry from Marmaris to Rhodes (Greek island, EU territory) is a legitimate 50-min trip. Book direct with Yeşil Marmaris (yesilmarmaris.com) at €60–€85 round-trip — third-party resellers add 30–50% markup and may use unlicensed operators. Bring your passport for EU border control on arrival in Rhodes. Day-trip tickets allow same-day return; multi-day tickets allow extended stays. Schedule runs more frequently April–October."),
        ("Where should I eat in Marmaris without overcharging?",
         "Walk one street back from the harbor and Bar Street to find restaurants where Turkish residents eat. Community-recommended Marmaris names: Liman Restaurant (harbor area, fish), Ney Restaurant (Old Town, traditional Turkish), Mezzaluna (modern Mediterranean). Order from Turkish-language menus or chalkboards (not English-only photo menus). For fish, ask to see the fish before ordering AND have it weighed in your presence. Refuse complimentary bread/olives unless prices are confirmed. Check the bill line-by-line and dispute any item not ordered. Bargaining 30–40% off the first quote is reasonable in tourist-tier shops."),
    ],
    "Bodrum": [
        ("Is Bodrum safe for tourists?",
         "Bodrum is broadly safe — the marina/yacht hub atmosphere is relatively low-pressure compared to other Turkish resort cities. The practical risks are financial: Milas-Bodrum Airport (BJV) transfer overcharges, Cumhuriyet Caddesi nightlife card-skimming, yacht/gulet day-cruise hidden charges, hotel-concierge excursion markups to Pamukkale/Ephesus, and Bodrum Castle 'skip-the-line' tout pressure. Save Tourism Police 155 and Bodrum Belediyesi Tourism +90 252 316 1091."),
        ("How do I get from Milas-Bodrum Airport (BJV) to Bodrum?",
         "Havaş airport bus to Bodrum otogar runs ₺250 (~€6.50) per person in 50 min — the cheapest scam-free option. Licensed taxi (35 km) is ₺1,000–₺1,400 (€25–€35) on Tarife 1. Refuse 'fixed price' quotes over €60. Welcome Pickups (€30–€40 per car for up to 4 people) is the vetted private alternative. From Bodrum to other peninsula towns (Türkbükü, Yalıkavak, Gümüşlük), the dolmuş from Bodrum otogar runs ₺50–₺100 per person — far cheaper than the €30–€60 hotel-concierge 'private transfers.' Uber operates in Istanbul but not in Bodrum."),
        ("How do I book a yacht/gulet day-cruise without hidden charges?",
         "Book with vetted operators (Bodrum Cruises, Yacht Adriatic, Gocek Sailing) at €30–€50 per person for a 6-hour day-cruise with 4–5 swim stops and lunch included. Anything under €20 signals shortcuts and hidden charges (drinks at €15–€25 each, mandatory tip €10–€15, surprise stops at İçmeler shopping). Confirm in writing: lunch included, drinks at posted prices, no shopping stop, specific swim stops. Older travelers should confirm: handrails on swim ladder, covered shaded area on deck, accessible toilet."),
        ("How do I avoid hotel-concierge excursion markups for Pamukkale/Ephesus?",
         "Book Pamukkale or Ephesus day-trips from Bodrum only via GetYourGuide or Viator with TÜRSAB Turkish Ministry of Culture licensing verified and 'no shopping stops' filter active at €40–€80 per person. AVOID hotel-concierge bookings under €30 — the math forces 60–90 minute stops at onyx workshops, leather shows, or 'cooperative' lunches. The drive from Bodrum to Pamukkale is 4 hours each way; to Ephesus is 3.5 hours each way. For older travelers, the Pamukkale day-trip is exhausting — consider an overnight in Pamukkale village (€30–€60/night) and a separate Ephesus day-trip from Kuşadası or Selçuk via the Ephesus Shuttle vetted operator."),
        ("How do I visit Bodrum Castle (Underwater Archaeology Museum)?",
         "Bodrum Castle and its Museum of Underwater Archaeology is the city's headline attraction. Entry is ₺200 (~€5) — buy at the official ticket booth at the castle entrance or via muze.gov.tr. Decline 'skip-the-line' touts at the entrance — this attraction rarely has queues except during cruise mornings. Visit takes 90 minutes for the basic castle and another 30–60 min for the underwater archaeology exhibits (Bronze Age shipwrecks). The castle has steep stairs and uneven medieval pathways — older travelers with mobility concerns should plan for slow progress and use the handrails."),
    ],
    "Cappadocia": [
        ("Is Cappadocia safe for tourists?",
         "Cappadocia is broadly safe — the Goreme/Ürgüp/Avanos area is well-policed and the cave-hotel atmosphere is comfortable for older travelers. The practical risks are financial: hot-air balloon operator pricing variance and safety concerns (anything under €120/person signals unlicensed operator), airport transfer overcharges from Nevşehir/Kayseri, hotel-concierge 'all-inclusive Cappadocia day' packages with shopping stops, Goreme Open Air Museum reseller scams, and ATV/horseback tour tout pressure at trail heads. Save Tourism Police 155 and Nevşehir İl Emniyet Müdürlüğü +90 384 213 1700."),
        ("How do I book a Cappadocia hot-air balloon flight safely?",
         "Book directly with vetted operators: Royal Balloon (royalballoon.com), Butterfly Balloons (butterflyballoons.com), Voyager Balloons, or Turkiye Balloons. Pay €180–€280 per person — anything under €120 signals an unlicensed operator. Verify the operator's Turkish DGCA SHGM licensing number on their website. Cappadocia balloon accidents have happened (the worst in 2013 with multiple fatalities) and most have involved either unlicensed operators or operators flying in unsafe conditions to avoid refunds. For older travelers (suitable up to ~85 kg without back/neck/heart issues), the basket steps are 1.2 m high and the landing is rough — discuss with the operator and ask for a basket with low-step entry. Check weather conditions the night before; legitimate operators automatically reschedule for high-wind days."),
        ("How do I get from Nevşehir/Kayseri Airport to Goreme safely?",
         "Most balloon-package bookings include free shuttle from Nevşehir Airport (NAV) or Kayseri Airport (ASR) to your Goreme/Ürgüp hotel — confirm this BEFORE booking. Otherwise: Cappadocia Express shuttle €15 per person; Havaş bus from NAV €5 per person to Goreme; from ASR (75 km) is longer at €10. Licensed taxi from NAV is ₺900–₺1,200 (€23–€30) on the meter to Goreme; from ASR ₺1,400–₺1,800 (€35–€45). Refuse 'fixed price' quotes over €60. Uber does NOT operate in Cappadocia; only BiTaksi and licensed taxis."),
        ("Should I book a guided Cappadocia day-tour?",
         "For first-time visitors, yes — Cappadocia is geographically spread and a guided 'Red Tour' (Goreme, Devrent Valley, Pasabag, Avanos pottery) or 'Green Tour' (Derinkuyu underground city, Ihlara Valley) provides context that's hard to get independently. Book with vetted operators (Mehmet Cappadocia, Nomad Travel, Turkiye Balloons-affiliated tours) at €40–€60 per person with 'no shopping stops' confirmed in writing. AVOID hotel-concierge 'all-inclusive Cappadocia day' packages under €40 — the math forces 60–90 minute stops at onyx workshops, carpet 'cooperatives,' or pottery demonstrations. The Avanos pottery stop on Red Tour is sometimes legitimate (a real artisan demonstration) and sometimes a high-pressure sales venue — confirm with your operator which version."),
        ("How do I visit Goreme Open Air Museum safely?",
         "Goreme Open Air Museum (the rock-cut Byzantine churches) is the area's cultural highlight. Entry is ₺1,000 (~€25) — buy at the official ticket booth at the museum entrance or via muze.gov.tr. The Karanlık Kilise (Dark Church) is a separate ₺200 (~€5) add-on but houses the best-preserved frescoes and is worth the additional charge. r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) documents the broader Turkish-attraction reseller-scam pattern that applies at Cappadocia entry points — avoid clone sites charging €50+ for what should be €25. Visit early morning (8 AM opening) to avoid both balloon-day crowds and the heat. For older travelers, the museum involves walking on uneven volcanic-rock paths and stooping to enter low cave doorways — the visit takes 90 minutes at a comfortable pace."),
    ],
    "Prague": [
        ("Is Prague safe for tourists?",
         "Prague is very safe for tourists with low violent crime. The main risks are financial — bar overcharging in the Old Town, taxi scams, and currency exchange fraud. The Old Town, Malá Strana, and Vinohrady neighborhoods are all safe to walk at night. Be alert near Wenceslas Square late at night, which has a higher rate of petty crime."),
        ("What is the most common scam in Prague?",
         "Bar and restaurant overcharging in the Old Town Square area is the most consistent tourist complaint — some venues have two menus (one for locals, one shown to tourists with 3–5x prices). Taxi overcharging, particularly from Václav Havel Airport and train stations, is the second most common issue. Use Bolt or Liftago always."),
        ("How do I exchange money in Prague?",
         "Use bank ATMs (Česká spořitelna, ČSOB, Komerční banka) for the best rates. If using exchange offices, look for clearly posted buy/sell rates — the 'zero commission' offices often have deliberately bad rates built in. Never exchange money at Wenceslas Square kiosks. The Czech koruna (CZK) is still the currency — euro is not accepted outside tourist traps, which typically quote poor exchange rates."),
        ("How do I get from Prague Airport to the city?",
         "Bus 119 to Nádraží Veleslavín (then Metro A to Old Town) costs CZK 40 and takes about 35 minutes. The Airport Express (AE) bus goes directly to Prague hlavní nádraží (main station) for CZK 100. Bolt and Uber operate at standard rates. Avoid taxis at the airport rank — they are legally allowed to charge significantly more than app taxis and frequently do."),
        ("Is Prague nightlife safe?",
         "Prague has a vibrant and generally safe nightlife scene. The main hazards are financial — bars in the Old Town that overcharge and strip clubs/hostess bars near Wenceslas Square that use manipulative pricing. Stick to venues in Vinohrady, Žižkov, or Holešovice for local-priced bars. Never enter a bar at the direct suggestion of a street tout — they receive commission and will lead you to expensive venues."),
    ],
    "Marrakech": [
        ("Is Marrakech safe for tourists?",
         "Marrakech is generally safe for tourists though it requires more vigilance than European cities. The main risks are persistent harassment and financial scams in the Medina and souks — aggressive touts, unsolicited 'guides,' and manipulation into shops. Violent crime against tourists is uncommon. Solo female travelers report higher harassment levels and may prefer to explore with a companion or organized tours."),
        ("What is the most common scam in Marrakech?",
         "The 'free guide' who leads you through the Medina then demands large payment is the most reported scam. Anyone who approaches you and offers to show you to your riad, the main square, or 'a shortcut' is almost certainly expecting payment. The Djemaa el-Fna square entertainment trap (photographing performers without agreeing on a price) is the second most common complaint."),
        ("How do I navigate the Medina in Marrakech?",
         "Download an offline map (Maps.me or Google Maps offline) before entering the Medina — navigation without a guide is entirely possible. When approached by someone offering directions, be firm but polite: 'La shukran' (No thank you). If you want a guide, arrange one in advance through your riad at a fixed price. Getting lost in the souks is part of the experience — just navigate back to a landmark."),
        ("What's the best way to shop in the souks?",
         "Expect to negotiate everything. The standard approach: ask the price, offer 25–30% of what's quoted, and settle somewhere around 40–60% of original. Walking away often results in the seller calling you back at a lower price. Don't feel pressured to buy after spending time looking — 'just looking' is legitimate. Avoid buying anything in the first souk you visit; get a feel for prices first."),
        ("Is it safe to eat street food in Djemaa el-Fna?",
         "The food stalls in Djemaa el-Fna are a famous experience, but the pricing system requires care: stall hawkers will aggressively try to seat you, and the prices are higher than they appear. Agree on prices before sitting and eating. The snail soup, orange juice, and lamb tagines are genuinely good and safe. For the best street food at local prices, explore one block into the Medina rather than eating in the square itself."),
    ],
    "Cairo": [
        ("Is Cairo safe for tourists?",
         "Cairo's main tourist areas — Giza, Islamic Cairo, Khan el-Khalili, and the Nile Corniche — are generally safe for tourists with a police presence. Violent crime against visitors is uncommon. The primary challenges are aggressive touting at tourist sites, traffic, and scams near the Pyramids. Exercise standard caution, use official tour guides, and stay in well-trafficked areas."),
        ("What is the most common scam in Cairo?",
         "The Pyramids of Giza complex is the most scam-dense tourist site in Egypt. Freelance guides, horse/camel riders, and vendors all demand payment for services rendered before prices were agreed upon. 'Free' items placed in your hands become expensive purchases. Always agree on any price, in writing if possible, before accepting any service or item near the Pyramids."),
        ("How do I get around Cairo safely?",
         "Uber and Careem are the safest and most reliable transport options in Cairo — fixed prices, driver tracking, and no negotiation. The Cairo Metro (Lines 1, 2, and 3) is safe, cheap, and fast for cross-city travel (note: there are women-only carriages on most trains). Street taxis rarely use meters with tourists — always negotiate firmly before entering, or use an app. Avoid any transport arranged by touts outside tourist sites."),
        ("What do I need to know about visiting the Pyramids?",
         "Buy tickets only at the official GIZA ticket office (not from anyone outside the gate). Standard admission covers the plateau; entering the pyramids requires separate tickets (limited daily). The Solar Boat Museum has an additional fee. Hiring an official licensed guide (book through your hotel or the Egyptian Tourism Authority website) significantly improves the experience and shields you from constant touting. Early morning arrival (gates open at 8am) has fewer crowds and cooler temperatures."),
        ("Is it safe to travel in Egypt beyond Cairo?",
         "Yes — Luxor, Aswan, and the Red Sea coast (Hurghada, Sharm el-Sheikh) are all popular and relatively safe tourist destinations. Travel between cities is best done by EgyptAir domestic flights, tourist trains, or organized tours rather than public buses. The Nile cruise (Luxor to Aswan) is a classic experience and generally very safe. Check your government's current travel advisory before visiting destinations in Sinai or areas near the Libyan or Sudanese borders."),
    ],
    "Buenos Aires": [
        ("Is Buenos Aires safe for tourists?",
         "Buenos Aires has improved significantly for tourists in recent years. The main tourist neighborhoods — Palermo, Recoleta, San Telmo, and Puerto Madero — are manageable with standard urban awareness. Petty theft and express robbery exist but violent crime targeting tourists is uncommon in tourist areas. Avoid Constitución and La Boca outside the main tourist strip, especially at night."),
        ("What is the most common scam in Buenos Aires?",
         "The fake police officer scam — where someone posing as a plainclothes cop asks to check your wallet for 'counterfeit bills' — is the most reported tourist scam. Real Argentine police never do this. Mustard/ketchup squirt distractions (someone 'accidentally' sprays something on you, a helper appears to clean it and pickpockets you) are also well-documented."),
        ("Is Uber safe in Buenos Aires?",
         "Uber operates in Buenos Aires and is generally safe, though the app has had intermittent legal status conflicts with local taxi unions — drivers sometimes ask you to sit in front to avoid identification as Uber. Cabify is a fully legal and equally reliable alternative. For longer trips, book a remise (radio-dispatched car with fixed prices) through your hotel — far safer than street taxis for airport runs."),
        ("What's the best neighborhood to stay in Buenos Aires?",
         "Palermo Soho/Hollywood is the most tourist-friendly with excellent restaurants, cafés, and nightlife at reasonable prices. Recoleta is upscale and safe near the famous cemetery. San Telmo has the best antique markets and tango scene. Avoid staying in Constitución or Once (cheaper but higher crime). Puerto Madero is modern and very safe but expensive and somewhat sterile."),
        ("What should I know about tipping in Buenos Aires?",
         "Tipping is expected but not mandatory in restaurants — 10% is standard, 15% for excellent service. The tip (propina) is left in cash on the table rather than added to a card payment. Some tourist-oriented restaurants near Puerto Madero or Recoleta have started adding mandatory service charges to bills — check before adding more. At tango shows, tipping performers and musicians is appreciated."),
    ],
    "New York City": [
        ("Is New York City safe for tourists?",
         "New York City is significantly safer than its reputation suggests, and the main tourist areas — Midtown, Lower Manhattan, Brooklyn Bridge, Central Park — are extremely well-patrolled and safe during the day. Petty theft (phone snatches, pickpocketing) has increased in recent years, particularly on the subway. Violent crime targeting tourists is rare. Stay aware on the subway, especially after midnight, and keep phones pocketed on the platform."),
        ("What is the most common scam in New York City?",
         "Phone snatching on the subway (grabbing a phone through closing doors as the train departs) is the most reported tourist crime. Times Square CD scams (someone presses a CD into your hand, claims it's a 'gift,' then aggressively demands $20–$50) are the second most common. Unlicensed airport taxis overcharging travelers, particularly at JFK, are also well-documented."),
        ("How do I get from JFK Airport to Manhattan?",
         "The AirTrain to Jamaica Station, then LIRR to Penn Station costs about $15 total and takes 45–55 minutes — cheap but requires luggage management. The AirTrain to Jamaica then E/J/Z subway costs about $8.75 and takes 60–70 minutes. Licensed yellow taxis have a flat rate of $70 to Manhattan (plus tolls and tip). Uber/Lyft are typically $55–$90 depending on traffic. Avoid any driver who approaches you inside the airport."),
        ("Is the New York City subway safe?",
         "The NYC subway runs 24 hours a day, 7 days a week and is used by millions daily. It's generally safe during commuting hours. Late night (midnight–5am) is when caution is warranted — wait in well-lit sections of the platform near the conductor's car, avoid empty cars, and keep your phone and valuables out of sight. The main risk is opportunistic theft rather than targeted violence."),
        ("Are there good free things to do in NYC?",
         "Many of New York's best experiences are free: walking the Brooklyn Bridge, exploring Central Park, visiting the High Line, the Staten Island Ferry (with Manhattan skyline views), most of the DUMBO waterfront, and street-level views of the architecture in every neighborhood. Many world-class museums suggest a donation rather than charging fixed admission — the Met, MoMA PS1, and the American Museum of Natural History all offer pay-what-you-wish periods. The TKTS booth in Times Square offers 20–50% discounts on same-day Broadway tickets."),
    ],
    "Vienna": [
        ("Is Vienna safe for tourists?",
         "Vienna consistently ranks among the safest cities in the world and is exceptionally tourist-friendly. Violent crime is extremely rare. The main tourist risks are pickpocketing near St. Stephen's Cathedral and on the U1 and U4 U-Bahn lines, and minor overcharging at restaurants near tourist sites. The Innere Stadt (1st district) and Mariahilfer Strasse area are safe at all hours."),
        ("What is the most common scam in Vienna?",
         "Overpriced restaurant meals near the tourist core (Stephansplatz, Graben) where tourist menus are significantly more expensive than the regular card are the most common complaint. Concert ticket sellers near St. Stephen's Cathedral selling Mozart/Strauss performances at inflated rates compared to booking directly are the second most common issue."),
        ("How do I get from Vienna Airport to the city?",
         "The CAT (City Airport Train) runs non-stop to Wien Mitte/Landstraße in 16 minutes and costs €14.90 (one-way). The cheaper S7 S-Bahn train goes to the same station in about 25 minutes and costs €4.20 with a standard city ticket. Taxis are metered from the airport — fixed rate approximately €36–€40 to the 1st district. Uber also operates. The train options are far better value."),
        ("What should I order at a Viennese coffeehouse?",
         "The Viennese coffeehouse (Kaffeehaus) is a UNESCO-recognized cultural institution. A Melange (similar to a cappuccino) or Wiener Schwarzer (black coffee) with a Strudel or Torte is the classic order. Coffeehouses are designed for lingering — a single coffee gives you the right to sit for hours reading newspapers. Prices at tourist-facing coffeehouses near the Opera are 30–50% higher than at local Kaffeehäuser in the 7th (Neubau) or 8th (Josefstadt) districts."),
        ("Is the Vienna Museum Pass worth it?",
         "The Vienna City Card (24/48/72 hours) combines unlimited public transport with museum discounts and is good value if you plan to use public transport extensively. The Vienna Museum Pass (separate) covers many of the state museums. The Kunsthistorisches Museum, Belvedere, and Albertina are the must-sees — book timed entry slots in advance online to avoid queues. The Belvedere's Klimt collection (The Kiss) is the single most visited artwork."),
    ],
    "Vancouver": [
        ("Is Vancouver safe for tourists?",
         "Vancouver is one of Canada's safer major cities for tourists. The main tourist areas — Downtown, Gastown, Granville Island, Stanley Park, and Kitsilano — are generally safe. The Downtown Eastside (DTES) neighborhood has a significant open drug use and mental health crisis and is not a tourist destination. Petty theft (bike theft, car break-ins) is Vancouver's primary crime issue — don't leave anything visible in rental cars."),
        ("What is the most common scam in Vancouver?",
         "Car break-ins targeting rental cars with visible luggage are technically the most common property crime affecting visitors. Tour operator overcharging (particularly for whale-watching and Whistler transfers) and unlicensed airport taxi overcharging are the most common financial scams. Vancouver is relatively low-scam by major city standards."),
        ("How do I get from YVR Airport to Vancouver?",
         "Canada Line SkyTrain from YVR to Waterfront Station (Downtown Vancouver) takes 26 minutes and costs $10.95 with a Compass Card or $11.25 cash. It's fast, reliable, and runs until 1am. Official taxis from the taxi rank outside arrivals are metered — approximately $35–$45 to Downtown. Uber and Lyft both operate. Avoid any unlicensed driver who approaches you in the terminal."),
        ("What are the best day trips from Vancouver?",
         "Whistler is the most popular day trip (2 hours by car or the Whistler Mountaineer bus) for skiing in winter and hiking/biking in summer. The Sea-to-Sky Highway drive is spectacular. Squamish (1 hour north) has world-class rock climbing and the Sea to Sky Gondola. Victoria on Vancouver Island requires a 1.5-hour BC Ferries trip — book crossings in advance in summer. All are well-organized with legitimate operators; book direct or through Tourism Vancouver."),
        ("Is Vancouver good for hiking?",
         "Yes — Vancouver's proximity to the North Shore Mountains makes it exceptional for accessible hiking. Grouse Grind (nicknamed 'Mother Nature's Stairmaster') is 45 minutes from Downtown by public transit. Lynn Canyon offers free suspension bridge and swimming holes (vs the expensive Capilano bridge). Mount Seymour and Cypress Provincial Park have trails for all levels. Always inform someone of your hiking plans, carry water and a rain layer — Vancouver weather changes quickly."),
    ],
    "Quebec City": [
        ("Is Quebec City safe for tourists?",
         "Quebec City is consistently ranked the safest city in North America for violent crime — Old Quebec is genuinely walkable day or night. The practical risks are financial: r/quebeccity 'don't want to fall into the trap!' (comments/1dii1iw, 2024) names La Bûche and the Rue Saint-Louis tourist-strip restaurants for overcharging; Petit Champlain souvenir markup at $25–$45 for $8 maple syrup per r/quebeccity (comments/1iid0qa, 2025); calèche carriage tour pricing manipulation at Place d'Armes; cruise-day shore-excursion reseller markups for Montmorency/Île d'Orléans/Sainte-Anne; YQB airport taxi overcharges (legitimate flat rate is regulated at $36.40 day / $42 night); and packaged sugar-shack day tours at $80–$140 per person for what's $25–$40 at the actual cabane. Save Quebec City Police 311 (non-emergency) and 911."),
        ("What is the most common Quebec City scam in 2025?",
         "Old Town tourist-strip restaurant overcharging tops the list — r/quebeccity 'don't want to fall into the trap!' (comments/1dii1iw, 2024) and r/quebeccity 'Highlights of our visit' (comments/1lsac8n, 2025) both name La Bûche specifically: 'We really regretted going to La Bûche because it was overpriced and not that great.' Petit Champlain 'authentic Québécois' souvenir markup is second most common — $25–$45 for $8–$12 maple syrup, fake Inuit art without Igloo tag certification per r/quebeccity (comments/1iid0qa, 2025). Calèche carriage tour pricing manipulation, cruise-day excursion reseller markups, YQB airport taxi overcharges, and packaged sugar-shack day-tour bundles round out the top six."),
        ("How do I eat in Quebec City without overcharging?",
         "Walk five minutes uphill from Vieux-Québec to Saint-Roch (Rue Saint-Joseph East) where local Quebec residents eat at honest prices. Community-recommended venues with posted prices: Le Clocher Penché (Saint-Roch, modern Québécois, $25–$40 mains), Buffet de l'Antiquaire (Saint-Roch, classic Québécois, $15–$25), Le Lapin Sauté (Petit Champlain — but ask for the residential menu). For poutine, La Bête Burger or Chez Ashton (Quebec institutions, $8–$14) rather than Old Town tourist venues. Avoid Rue Saint-Louis, Place Royale, and the Château Frontenac perimeter for sit-down meals — these zones are calibrated for one-time cruise-day diners. Confirm gratuity policy at seating; refuse pre-added tips above 15%. For cruise passengers, eating back on the ship is often the best value."),
        ("How do I get from Quebec City Airport (YQB) safely?",
         "The YQB-to-Old-Town flat fare is regulated by Quebec City at $36.40 (day) / $42 (after midnight) — refuse any quote above. Pre-book Taxi Coop Québec (+1-418-525-5191) for guaranteed pickup, especially before 5 AM or after 11 PM per r/quebeccity 'Early morning taxi to YQB?' (comments/13fvoh3, 2024). Uber operates in Quebec City but supply is limited — verify before relying on it. The airport bus (RTC route 78) runs $3.75 to downtown but only 6 AM to 11 PM. For Old Town taxis, board at official Place d'Armes or Place de l'Hôtel-de-Ville stands rather than hailing on Rue Saint-Louis. For cruise-pier rides, the legitimate metered fare to Place d'Armes is $8–$12 — refuse 'cruise day' inflated quotes."),
        ("Should I book a calèche horse-drawn carriage tour?",
         "Yes — calèche tours are an iconic Quebec City photo opportunity and a genuine 19th-century tradition. Book ONLY at the official Place d'Armes stand (in front of Château Frontenac) or Place de l'Hôtel-de-Ville where prices are posted: $100–$130 for the standard 35-minute Old Town circuit, $160–$200 for a 1-hour extended route. Refuse 'special prices' over $150 for the standard loop. Tipping is OPTIONAL — $10–$20 is generous and never demanded. Avoid cruise-pier pickups; walk the 8 minutes uphill to Place d'Armes for posted-rate pricing. For travelers with mobility concerns, the carriage step is high — drivers are required to provide a step-stool but may not offer one unless asked. The funicular ($5 round-trip) from Lower Town to Upper Town is more practical for many older travelers than a calèche."),
    ],
    "Banff": [
        ("Is Banff safe for tourists?",
         "Banff is broadly safe — violent crime against visitors is essentially nonexistent and the town is well-policed. The practical risks are financial: Pursuit Collection combo-pass monopoly pricing per r/Banff 'Pursuit is an American company' (comments/1j3kre8, 2025) which documents the Canadian Competition Bureau complaint; Columbia Icefield Adventure & Glacier Skywalk markup at $145 for a 90-min experience; Moraine Lake / Lake Louise shuttle reservation reseller fraud per r/Banff 'Shuttle Reservation' (comments/1sm76ci, 2025) with 27,000-person queues; Banff Town restaurant and hotel pricing inflation per r/Banff 'Is it worth it?' (comments/179x003); vacation rental fraud per r/Banff 'Banff rental scams' (comments/1g0vd2m, 2025); and YYC Calgary Airport-to-Banff shuttle overcharges. Wildlife is the actual safety risk — bear and elk encounters require carrying bear spray ($45 at any Banff outdoor shop)."),
        ("What is the most common Banff scam in 2025?",
         "Pursuit Collection combo-pass pricing tops the list as a structural concern — r/Banff 'Pursuit is an American company' (comments/1j3kre8, 2025) and r/alberta 'Competitors cry monopoly as American company buys' (comments/1fajkdn, 2024) both document the Canadian Competition Bureau complaint about Pursuit's monopoly hold on Banff/Jasper attractions (Banff Gondola, Columbia Icefield Adventure, Glacier Skywalk, Lake Minnewanka Cruise, Maligne Lake Cruise). Moraine Lake shuttle reservation reseller fraud is second most common — clone websites mimicking reservations.pc.gc.ca and hotel-arranged 'guaranteed shuttle' upsells at $80–$150 per person for what costs $8 official. Vacation rental fraud on Facebook Marketplace and Kijiji per r/Banff (comments/1g0vd2m, 2025), Columbia Icefield + Skywalk tour packages, Banff Town restaurant pricing, and YYC airport transfer overcharges round out the top six."),
        ("How do I avoid the Pursuit Collection monopoly pricing?",
         "AVOID Pursuit combo passes — they lock you into 4–6 attractions when 1–2 are sufficient. The Banff Gondola is genuinely scenic but $76 — consider the FREE alternative: drive or shuttle to Sulphur Mountain Hot Springs ($16 entry) for similar views. For the Columbia Icefield, the basic glacier walk (Toe of the Athabasca Glacier Walk, FREE) gets you within 100 metres of the ice — skip the bus + Skywalk combo at $145 which delivers a 5-min glass-floor walkway. If you want to walk on the glacier itself (genuine experience), book IceWalks guided glacier hike ($90 adult, 3 hours, with crampons + certified guide) — this is the Canadian-owned alternative to Pursuit's bus tour. Lake Louise and Moraine Lake are FREE to access (just shuttle reservation needed). Canadian-owned alternatives: White Mountain Adventures (small group hiking), Discover Banff Tours, Sundance Tours."),
        ("How do I book Moraine Lake and Lake Louise shuttles?",
         "Book Moraine Lake / Lake Louise shuttles ONLY at reservations.pc.gc.ca (the official Parks Canada system) — $8 round-trip. Reservations open 8 AM Mountain Time in batches; r/Banff 'Shuttle Reservation' (comments/1sm76ci, 2025) documents 27,000+ queues. Set a calendar reminder for the booking window opening date for your travel dates (typically 90 days ahead, with last-minute slots 2 days ahead per r/Banff 'Lake Louise/Moraine Shuttle Reservation Tips!' (comments/1enazwt, 2024)). If your hotel offers a free shuttle to Lake Louise/Moraine Lake as a guest perk, use it. Decline ALL third-party 'guaranteed shuttle' or 'private transfer' offers over $30 per person — these are clone-site scams. For the Moraine Lake sunrise experience, aim for the 5:30 AM shuttle window and bring layers — temperatures drop to 0–5°C even in July."),
        ("How do I get from Calgary Airport (YYC) to Banff safely?",
         "Use Brewster Express or Banff Airporter ($60–$80 per person, both with digital booking and luggage handling) for the 130-km / 1.5-hour transfer. On-It Regional Transit ($10/person, weekends only) is the budget option but no luggage assistance. Refuse third-party 'private transfer' quotes over $120 per person. For rental cars, the YYC airport rental hub has all major operators (Hertz, Avis, Enterprise, Budget) — book direct, not through third-party aggregators. Confirm hotel parking fees BEFORE booking — Banff Town hotels charge $19–$45/night per r/marriott 'Moxy Banff' (comments/1lod04m, 2025); outlying hotels and Canmore properties are often free. For day-parking in Banff Town, use the FREE Banff High School park-and-ride with a free shuttle to downtown — saves the $25–$40 day-parking-lot fee and the parking-ticket risk per r/Banff 'Any success appealing parking ticket?' (comments/1dog97k, 2024). Buy a Parks Canada parking pass at $11.25/day or $75 annual for any roadside parking in the National Park."),
    ],
    "Jasper": [
        ("Is Jasper safe for tourists?",
         "Jasper is broadly safe — violent crime against visitors is essentially nonexistent. The 2024 wildfire destroyed 30% of Jasper Town buildings; tourism has resumed in stages through 2025, and most accommodations have reopened. The practical risks are financial: Pursuit Collection cross-park combo-pass monopoly per r/jasper 'PSA: Pursuit is an American company' (comments/1inuhkf, 2025); Maligne Lake Cruise upsell pressure to 'premium' tier; YEG/YYC rental car one-way drop fees $200+; vacation rental fraud on Facebook Marketplace and Kijiji per r/jasper post-wildfire context; wildfire-recovery donation phishing emails; and 'guaranteed bear sighting' wildlife tour markups. Wildlife is the actual safety risk — bear and elk encounters require carrying bear spray ($45 at any Jasper outdoor shop)."),
        ("What is the most common Jasper scam in 2025?",
         "Pursuit Collection cross-park monopoly pricing tops the list as a structural concern — r/jasper 'PSA: Pursuit is an American company' (comments/1inuhkf, 2025) and r/Banff 'Pursuit is an American company' (comments/1j3kre8, 2025) both document the Canadian Competition Bureau complaint about Pursuit's hold on Banff/Jasper attractions. Maligne Lake Cruise upsell pressure (from $112 classic to $149 premium for 15 extra minutes ashore) is second most common. Post-wildfire vacation rental fraud on Facebook Marketplace and Kijiji per r/jasper 'Worth it to travel to Banff/area still?' (comments) confirms the displaced-rental-supply problem. YEG/YYC rental car one-way drop fees, wildlife-tour markups, and Jasper Town restaurant/hotel parking inflation round out the top six."),
        ("How do I visit Maligne Lake and Spirit Island?",
         "The Maligne Lake Cruise is the ONLY way to legally reach Spirit Island (no private boats permitted on the lake). Book direct at malignelake.com at $112 adult for the 90-min classic cruise — refuse $200+ 'day-tour' bundles and any 'private boat' offers (which are illegal scams). For transport from Jasper Town (48 km), drive yourself or use SunDog Tours shuttle ($35 round-trip). Book the morning 9:30 AM or 10:30 AM cruise for best Spirit Island light. Decline the 'premium' upgrade ($149 for 15 extra minutes ashore — not meaningful). For older travelers without time for the full Maligne Lake trip, the FREE viewpoints at the parking-lot end of the lake are dramatic in their own right."),
        ("How do I get from Edmonton (YEG) or Calgary (YYC) airports to Jasper?",
         "From YEG (365 km / 4 hours via Yellowhead Highway 16 — the spectacular alternative): rental car is cheapest if doing a round-trip; one-way drop fees to YYC typically $150–$250. From YYC (410 km / 5 hours via Banff): rental car gives you Banff–Jasper road-trip flexibility but commits you to the longer drive. For non-drivers, SunDog Tours offers Calgary-Jasper-Edmonton through-tickets at $130–$180 per person — much cheaper than one-way rentals. r/jasper 'Looking for Budget-Friendly One-Way Car Rental' (comments) confirms: 'It genuinely might be cheaper to just take buses to/from Banff & jasper.' For older travelers uncomfortable driving the Icefields Parkway in winter (October–April), rent a 4WD/AWD vehicle and confirm winter-tire equipment per Alberta law."),
        ("How do I avoid wildfire-recovery donation scams in Jasper?",
         "The 2024 Jasper wildfire created a parallel scam economy of phishing emails and fake donation appeals targeting visitors. For genuine wildfire-recovery donations, donate ONLY through Red Cross Canada (redcross.ca) or the Jasper Community Team Society (jaspercommunityteam.ca) — verify the URL manually rather than clicking email links. r/HikingAlberta 'Email from Parks Canada - Is this legit?' (comments) documents the parallel Parks Canada email phishing pattern: 'It's a classic we aren't providing stoves scam. Don't fall for it.' For accommodation, book ONLY via Airbnb/Vrbo/Booking.com — Facebook Marketplace and Kijiji listings claiming 'survived the wildfire' are high-risk for fraud. Demand a video call with the property visible BEFORE any deposit. The major chain hotels (Marmot Lodge, Tonquin Inn, Sawridge Inn) survived the wildfire and offer guaranteed booking through their corporate websites."),
    ],
    "Victoria": [
        ("Is Victoria safe for tourists?",
         "Victoria is broadly safe — violent crime against tourists is rare. The practical risks are financial and personal-safety: BC Ferries Experience Card resale fraud on Facebook Marketplace per r/VictoriaBC 'Do not purchase BC Ferries Experience Cards'; whale-watching operator variance with off-brand operators charging $80 'specials' that violate Marine Mammal Regulations; Butchart Gardens cruise-line shore-excursion 2-3x markup; YYJ airport taxi overcharges; Vancouver Island trafficking warnings per r/VictoriaBC 'Possible Scam + Safety Warning in Langford' (NEVER accept rides from strangers); and apartment rental + door-to-door donation fraud. Save Victoria Police non-emergency at 250-995-7654 and the Crime Stoppers tip line +1-800-222-8477."),
        ("What is the most common Victoria scam in 2025?",
         "BC Ferries Experience Card resale fraud on Facebook Marketplace tops the list — r/VictoriaBC 'Do not purchase BC Ferries Experience Cards' is the named community PSA: 'the only experience you're buying is the one when' the card has been emptied. Whale-watching operator variance is second most common — off-brand operators sell '$80 specials' that violate Marine Mammal Regulations approach distances. Butchart Gardens cruise-line shore-excursion 2-3x markup, YYJ taxi overcharges, Vancouver Island trafficking warnings, and apartment rental + door-to-door donation fraud round out the top six."),
        ("How do I get from Vancouver to Victoria via BC Ferries?",
         "Book BC Ferries reservations ONLY at bcferries.com (the official site) — NEVER buy Experience Cards or prepaid passes on Facebook Marketplace, Craigslist, or third-party sites per r/VictoriaBC 'Do not purchase BC Ferries Experience Cards'. For the busy summer season (June–September) and weekend departures, book reservations 2 weeks ahead — the $25 reservation fee guarantees your sailing. If you don't reserve, arrive 60 min before sailing for vehicle or 30 min for foot passenger. Pacific Coach ferry-bus combo ($63 from Vancouver to Victoria) bundles legitimate ferry fare with bus transit for non-vehicle travel. The premium alternative is Helijet helicopter from Vancouver harbour to Victoria harbour ($249 each way, 35 min) — fast and no ferry waiting."),
        ("How do I visit Butchart Gardens without overpaying?",
         "Buy Butchart admission direct at butchartgardens.com ($40 adult summer rate, $26 winter). For transport from Inner Harbour, take BC Transit route 75 ($2.50 each way, 50 min) or the CVS Tours shuttle ($20 round-trip including admission discount). AVOID cruise-line 'Butchart Gardens shore excursion' at $129–$179 per person — the math is 2-3x independent cost. Per r/HollandAmerica 'Alaska cruise Butchart Gardens': 'It's possible to do on a 4 hour stop, but it's probably only ~1 hours (at most) at the gardens.' For full visits, plan 2-3 hours on site; the cruise-stop 60-90 min window is rushed. Cruise-line excursion only worth markup if mobility-limited (guaranteed return-to-ship). Butchart's Saturday summer fireworks (June–September) are spectacular but require a 4+ hour visit window — not feasible on cruise-day."),
        ("How do I avoid Vancouver Island trafficking and stranger-car safety scams?",
         "NEVER accept rides from strangers on Vancouver Island — even helpful-seeming offers. r/VictoriaBC 'Possible Scam + Safety Warning in Langford' is a named 2024-25 community safety warning that reframes 'rideshare' offers as a trafficking pattern: 'Yes, this is a scam. Please don't ever get into a stranger's car again. There is trafficking on the island.' Use only licensed transportation: Victoria Taxi (+1-250-383-7111), Bluebird Cabs (+1-250-382-2222), Yellow Cab (+1-250-381-2222), Uber, or Lyft (both operate in Victoria). At the Swartz Bay ferry terminal, the BC Transit route 70 ($2.50) connects to downtown — wait at the official transit stop, not at the highway pull-off. For late-night Inner Harbour walks (after 10 PM), stay on Wharf Street and Government Street where police presence is visible. Avoid hitchhiking on Vancouver Island highways. Report any suspicious approach to Victoria Police at non-emergency 250-995-7654 or RCMP at 911."),
    ],
    "Halifax": [
        ("Is Halifax safe for tourists?",
         "Halifax is one of Canada's safest cruise-port cities — violent crime against tourists is rare and the waterfront is well-policed. The practical risks are financial: cruise-day shore excursion markups for Peggy's Cove (cruise-line bundles at $199–$299/person versus $80–$120 independent); YHZ airport taxi overcharges and Uber 'cancel-and-cash' scam per r/halifax 'Uber at YHZ' anchor; Halifax Waterfront restaurant tourist-trap pricing (Bluenose II, Cable Wharf seafood); Maritime Museum + Citadel Hill 'skip-the-line' tout pressure (Citadel Hill is FREE June 1 - September 1 every year); Halifax vacation rental fraud per r/halifax 'What are the odds this is a scam?' on Facebook Marketplace; and Lunenburg/South Shore tour bundle reseller markups. Save Halifax Regional Police non-emergency at 902-490-5020."),
        ("What is the most common Halifax scam in 2025?",
         "Cruise-day shore excursion markups for Peggy's Cove top the list — cruise-line 'Halifax + Peggy's Cove' bundles at $199–$299/person are 2x the independent rental-car or private-driver cost ($150–$250 round-trip for 4 people via Welcome Pickups). YHZ airport Uber 'cancel-and-cash' scam is second most common — r/halifax 'Uber at YHZ' is the named anchor: drivers ask passengers to cancel the Uber booking and pay $80–$120 cash without the regulated app fare. Halifax Waterfront restaurant tourist-trap pricing (lobster $59–$89), Maritime Museum/Citadel Hill 'skip-the-line' tout pressure, vacation rental fraud, and Lunenburg/South Shore tour bundles round out the top six."),
        ("How do I get from Halifax Stanfield Airport (YHZ) safely?",
         "The YHZ-to-downtown taxi is regulated FLAT $73 — refuse any quote above. For Uber, NEVER cancel the booking at the driver's request — if a driver asks to cancel and pay cash (per r/halifax 'Uber at YHZ' documented anchor), immediately exit and request another Uber driver. Halifax Transit MetroX bus 320 from YHZ to downtown is $4.25 per person, runs every 30-60 min — the cheapest and most overcharge-proof option. For older travelers with luggage, the airport shuttle Maritime Bus ($23 one-way) drops at downtown bus terminal. For late-night arrivals, pre-book Casino Taxi (+1-902-429-6666) or Aerocar Taxi (+1-902-429-9999) for guaranteed pickup. Verify Uber driver and vehicle match the app BEFORE entering the vehicle. Tip via the Uber app rather than cash to avoid tip-skimming concerns per r/halifax 'Taxi services or Uber?'."),
        ("Should I book a cruise-line Peggy's Cove tour?",
         "Usually no. Cruise-line 'Halifax + Peggy's Cove' bundles at $199–$299 per person are 2x the independent cost. Better alternatives: (1) rent a car at Halifax Stanfield Airport ($60–$80/day) or downtown ($80–$100/day), drive 45 min to Peggy's Cove, spend 1 hour at the lighthouse, drive back — total $80–$120 per person for 2 people; (2) Welcome Pickups private driver ($150–$250 round-trip for up to 4 people) with no shopping stops; (3) Casino Taxi (+1-902-429-6666) for $120–$160 round-trip. AVOID Ambassatours bundled tours over $150 per person — these include 'shopping stops' at Halifax waterfront souvenir shops per r/halifax 'How to get to Peggy's Cove?' For 4-hour cruise stops, skip Peggy's Cove entirely and walk Halifax waterfront (Maritime Museum + Citadel Hill + Public Gardens — all within 20-min walk of cruise terminal). Confirm 'no shopping stops' in writing for any small-group tour."),
        ("Where should I eat in Halifax without overcharging?",
         "Avoid Lower Water Street and Cable Wharf restaurants for sit-down meals — these are calibrated for one-time cruise-day diners with 'lobster dinner' specials at $59–$89 per person. Walk 5–10 minutes inland to community-recommended Halifax venues: The Wooden Monkey (Argyle Street, modern Atlantic, $22–$38 mains), Heartwood Vegan & Whole Foods (Quinpool Road, plant-based $16–$28), Battery Park Bar & Beerstillery (Halifax craft brewery + restaurant, $18–$32). For genuine cheap lobster, drive (or take Halifax Transit) to Eastern Passage's Fisherman's Cove — actual fisherman-direct lobster at $15–$25/lb cooked. For Halifax craft beer, visit the actual breweries (Garrison Brewing, Propeller Brewing, Good Robot Brewing) for honest tasting flight prices ($12–$18 vs $25–$35 at waterfront). Check the bill for pre-added gratuity before tipping. Cruise passengers should eat back on the ship rather than pay $80+ for harbor-front 'Atlantic experiences.'"),
    ],
    "Whistler": [
        ("Is Whistler safe for tourists?",
         "Whistler is broadly safe — violent crime against visitors is rare. The practical risks are financial: r/Whistler 'It's not legitimate: 24 fraudulent parking QR codes found in' is the named CBC-documented 2024 anchor for the parking QR-code skimming scam; vacation rental fraud per r/Whistler 'Craigslist scams' and 'DO NOT RENT FROM HERE'; Whistler Blackcomb lift-ticket resale fraud per r/Whistler 'Discount Lift tickets scam?'; restaurant 'subtle' bill-padding per r/Whistler 'Subtle not so subtle scamming at Whistler restaurants'; YVR-to-Whistler shuttle markups; and hotel parking + resort-fee inflation. Save Whistler RCMP non-emergency at +1-604-932-3044 and Whistler Bylaw Services at +1-604-935-8132 (for QR-code fraud reports)."),
        ("What is the most common Whistler scam in 2025?",
         "Fraudulent parking QR code stickers top the list — r/Whistler 'It's not legitimate: 24 fraudulent parking QR codes found in' is the CBC-documented 2024 anchor with 24 stickers found in the initial sweep and additional waves through 2025. The scam: tourist scans QR sticker on parking meter, gets directed to fake payment page, enters credit card details, gets no real parking authorization plus card-skimming follow-up charges. Vacation rental fraud (Mountaincountry-style fake agencies) is second most common per r/Whistler 'Craigslist scams' and 'DO NOT RENT FROM HERE.' Whistler Blackcomb 'discount lift ticket' resale fraud, restaurant subtle bill-padding, YVR-to-Whistler shuttle markups, and hotel parking + resort-fee inflation round out the top six."),
        ("How do I avoid the Whistler parking QR code scam?",
         "NEVER scan QR codes on parking meters or signs — even if they look official. Use the PayByPhone app (download from Apple App Store or Google Play directly, NOT via any QR code) and enter the parking lot code manually as posted on the meter signage. Alternative: use the physical pay-and-display machines (with your credit card swiped or chipped, not a QR code). Whistler Village Day Lots 1-2 are FREE for the first 90 minutes — confirm signage at entry. If you've already scanned a suspicious QR code, freeze your card via your bank app immediately and call your bank's fraud line. Report fraudulent QR stickers to Whistler Bylaw Services at +1-604-935-8132. r/Whistler 'It's not legitimate: 24 fraudulent parking QR codes found in' (CBC News 2024) is the named anchor."),
        ("How do I get from Vancouver (YVR) to Whistler safely?",
         "For shuttle service, use Pacific Coach Lines ($60 per person, the longest-established operator), Epic Rides ($45 per person, budget option), or Whistler Connection ($55 per person, includes late-night arrivals to 10 PM). Refuse hotel-concierge 'private transfer' quotes over $200 round-trip. For rental cars from YVR, Discount Car & Truck Rental at $50–$75/day is the cheapest option. The Sea-to-Sky Highway is genuinely spectacular but requires winter tires October–April per BC law. For older travelers without Canadian winter-driving experience, the SkyLynx shared shuttle ($50/person) is the comfortable middle option. r/Whistler 'Renting car vs shuttle?' (comments) confirms: 'The latest shared shuttle option is Whistler connection, if your flight lands by 10pm they'll take you.' Uber/Lyft surge pricing typically makes them more expensive than named shuttles ($150–$300 one-way)."),
        ("Should I buy lift tickets from third-party 'discount' sellers?",
         "NEVER. r/Whistler 'Discount Lift tickets scam?' is the canonical community anchor: 'This is 100% a scam.' All third-party 'discount Whistler lift ticket' offers on Craigslist, Facebook Marketplace, or street touts are fraud — fake codes that don't scan at the gate, stolen 'Buddy' tickets, or completely invented pass-transfers. Buy lift tickets ONLY at whistlerblackcomb.com or via the Vail Resorts Epic Pass program. The Epic Pass ($1,051 USD unlimited or $451 USD 4-day) is structurally cheaper than walk-up day tickets (now $270+) for any 4+ day ski trip — buy by Labor Day for the deepest discount. The senior discount (65+) at $193/day is significant — present ID at the lift ticket window. For non-skiing travelers, the Peak 2 Peak Gondola sightseeing ticket ($89) is honest-priced and provides spectacular Whistler-Blackcomb panoramic views. Report ticket fraud to Whistler Blackcomb security at +1-604-967-8950."),
    ],
    "Aruba": [
        ("Is Aruba safe for tourists?",
         "Aruba is widely considered one of the safest Caribbean islands for tourists. The US State Department assigns it the lowest risk Level 1 advisory. The tourist zones of Palm Beach, Eagle Beach, and Oranjestad are well-lit with visible police presence. Violent crime against visitors is rare. The primary risks are financial scams — timeshare traps, rental car damage shakedowns, and watersport hustles. Avoid the San Nicolas district after dark and take standard precautions."),
        ("How much should a taxi cost in Aruba?",
         "Aruba taxis operate on a government-fixed flat-rate system with no meters. Airport to Palm Beach high-rise area is approximately $22-25, Airport to Eagle Beach is approximately $20, Airport to Oranjestad is approximately $10. These rates are per trip, not per person, for up to 4 passengers. Only use taxis with 'TX' license plates and a roof-mounted sign. There is no Uber or Lyft in Aruba."),
        ("Is it safe to rent a car in Aruba?",
         "Driving in Aruba is straightforward — traffic drives on the right and the island is only 20 miles long. However, rental car break-ins are common at remote parking areas like the Natural Pool trailhead. Some budget rental companies charge for pre-existing damage upon return. Use a credit card with built-in rental protection, photograph the vehicle thoroughly at pickup, and never leave valuables inside. Off-road driving may void your basic insurance."),
        ("What should I do if my passport is stolen in Aruba?",
         "File a police report with the Korps Politie Aruba by calling 100. Then contact the US Consulate General in Curacao at +(599)(9) 461-3066 — there is no US embassy on Aruba itself. The consulate can issue an emergency passport but the process may take several days. Always keep a photocopy stored separately from the original."),
        ("Are there dangerous areas in Aruba?",
         "Aruba is generally very safe, but avoid the San Nicolas district after dark — while daytime street art is a legitimate attraction, the area has higher crime rates at night. The east and north coasts have powerful Atlantic surf with dangerous rip currents and no lifeguards. Stick to west coast beaches for swimming. Remote parking areas at Arikok National Park trailheads are hotspots for car break-ins."),
    ],
    "Puerto Vallarta": [
        ("Is Puerto Vallarta safe for tourists?",
         "Puerto Vallarta is one of Mexico's safest tourist destinations. The Zona Romantica, Malecon, and hotel zone are heavily patrolled and welcoming. Violent crime targeting tourists is rare. The primary risks are timeshare presentations, taxi overcharging, and ATM skimming. Use Uber, stay in well-trafficked areas, and avoid walking alone on isolated streets late at night."),
        ("Should I use taxis or Uber in Puerto Vallarta?",
         "Uber is generally safer and cheaper. PV taxis have no meters — all fares are negotiated, putting tourists at a disadvantage. If you must take a taxi, agree on the price in pesos before getting in. Never take an unmarked vehicle. From the airport, pre-book a transfer or use the official taxi counter inside the terminal."),
        ("How do I avoid timeshare salespeople at the airport?",
         "Walk straight through arrivals to your pre-booked transportation without stopping. Do not make eye contact or accept 'free' tequila or gifts. A firm 'No gracias' without slowing down is the most effective response. If someone claims your shuttle didn't show up, verify with your hotel by phone before accepting any alternative ride."),
        ("Is the Malecon safe to walk at night?",
         "The Malecon boardwalk is generally safe in the evening due to regular police patrols, street performers, and restaurant crowds. Be aware of the mustard/sauce distraction theft scam and keep phones in front pockets. The busiest and safest stretch is between the amphitheater and the Hotel Rosita. Avoid the far ends of the Malecon past midnight."),
        ("Is tap water safe in Puerto Vallarta?",
         "No — tap water in PV is not safe to drink. Stick to sealed bottled water or filtered water. Most restaurants use purified water for cooking and ice, but street stalls may not. The large 20-liter garrafones of purified water available at OXXO stores are very cheap if you're staying in an Airbnb."),
    ],
    "Cabo San Lucas": [
        ("Is Cabo San Lucas safe for tourists?",
         "Cabo San Lucas remains one of Mexico's safest tourist destinations. Approximately 89% of tourists report feeling safe during their visit. The primary risks are financial scams — timeshare pressure, taxi overcharging, jet ski damage shakedowns, and restaurant bill padding. The Tourist Corridor is heavily patrolled. The US State Department rates Baja California Sur at Level 2, the same as most of Europe."),
        ("Should I use taxis or Uber in Cabo?",
         "Uber is generally safer and more affordable. It provides upfront pricing, GPS tracking, and receipts. Cabo taxis don't use meters — all fares are negotiated. Official airport taxis cost $50-70 USD one way to the Hotel Zone; Uber is usually $25-40. Avoid pirate taxis — unlicensed vehicles posing as taxis that have no insurance or accountability."),
        ("How do I avoid timeshare salespeople at Cabo airport?",
         "The area past customs at SJD is called the 'Shark Tank.' Pre-book your transfer and walk directly to your confirmed ride. Don't make eye contact, don't accept gifts, and don't reveal your hotel name. A firm 'No gracias' without stopping is the most effective strategy. If someone claims your shuttle didn't show, verify by phone before accepting alternatives."),
        ("Is it safe to rent jet skis on Medano Beach?",
         "Jet ski rentals can be safe with precautions, but the damage-shakedown scam is well-documented. Only use licensed operators with branded tents (not freelancers in street clothes). Record a 360-degree video of the equipment before riding. Never hand over your passport. Use a credit card with fraud protection. If confronted with a fake damage claim, show your video and refuse to pay cash."),
        ("What should I do if police ask me for money in Cabo?",
         "Police bribery ('mordida') does occur during traffic stops. Remain calm, be polite, ask to see the badge and write down the number. Request a formal written citation rather than paying any on-the-spot 'fine.' Real fines are paid at a government office, never in cash to an officer. If threatened, call the US Consular Agency in Los Cabos at +52 (624) 143-3566."),
    ],
    "Punta Cana": [
        ("Is Punta Cana safe for tourists?",
         "Punta Cana is generally considered one of the safest Caribbean destinations. The Dominican government invests heavily in tourism security, and POLITUR (tourist police) patrols resort areas 24/7. Violent crime against tourists is rare within the resort zones. However, petty crime, scams, and overcharging are common outside resort grounds. The resort areas are significantly safer than Dominican cities like Santo Domingo."),
        ("Should I exchange money at the Punta Cana airport?",
         "No. Airport exchange booths offer rates approximately 15-20% worse than the real rate. Withdraw Dominican pesos from bank ATMs (Banreservas, Popular, BHD Leon) instead. Many places accept US dollars. For credit card purchases, always confirm the exchange rate being applied. Bring some USD cash for tips and use a no-foreign-transaction-fee card for larger expenses."),
        ("Are excursions booked on the beach safe?",
         "Generally no. Beach vendors operate without licenses, insurance, or accountability. If a tour goes wrong, you have zero recourse. Book through Viator, GetYourGuide, or your resort's official concierge. You'll pay $10-20 more but get insured boats, English-speaking guides, and cancellation policies. Verify whether lobby 'tour desks' are hotel-operated or independent."),
        ("Is Uber available in Punta Cana?",
         "Yes, Uber operates in Punta Cana. Uber Select uses licensed cab drivers with upfront pricing and GPS tracking. Standard taxis have no meters and fares must be negotiated. A taxi from the airport to Bavaro should cost $25-40 when pre-booked, but unlicensed drivers at the airport have charged $200-300 for the same trip."),
        ("What is the Sanky Panky scam?",
         "Sanky Panky is well-known Dominican slang for professional romance scammers who work as resort staff — bartenders, entertainers, or beach activity coordinators. They target solo female travelers, escalate to declarations of love within days, then extract money via wire transfers over months after you return home. Never send money to anyone you met on vacation."),
    ],
    "Turks and Caicos": [
        ("Is Turks and Caicos safe for tourists?",
         "TCI is one of the safest Caribbean destinations. Grace Bay and the resort areas of Providenciales are very well-maintained and secure. Violent crime against tourists is rare. The main risks are financial — taxi overcharging, unlicensed water sports operators, and vacation rental scams. Avoid the Five Cays and The Bight areas after dark."),
        ("Are there Uber or ride-sharing apps in TCI?",
         "No, there is no Uber or Lyft in Turks and Caicos. Taxis are the primary transport and do not use meters — fares are per person, not per trip, which surprises many visitors. Agree on the total fare before getting in. Pre-book airport transfers through your hotel. Renting a car is recommended for flexibility, though driving is on the left side of the road."),
        ("What is the ammunition law in Turks and Caicos?",
         "Bringing even a single round of ammunition into TCI is a criminal offense carrying mandatory prison time of up to 12 years. This has caught several US tourists unaware — a stray round in a range bag or carry-on can lead to arrest. Check all bags thoroughly before travel if you are a firearm owner. TCI customs actively scans for ammunition."),
        ("Is it safe to rent a car in Turks and Caicos?",
         "Renting a car is generally safe and recommended for exploring beyond Grace Bay. Drive on the left side of the road. Be aware that international brand rental companies in TCI are actually independent local licensees, so corporate offices may not help with disputes. Photograph the vehicle thoroughly at pickup and review your insurance terms carefully."),
        ("What should I do if I get scammed in TCI?",
         "Contact the Royal Turks and Caicos Islands Police Force (RTCIPF) at 911 or 999. For anonymous tips, use Crime Stoppers at 1-800-8477. For US citizens needing consular assistance, contact the US Embassy in Nassau at +1 242-322-1181 — there is no US consulate in TCI. Report vacation rental fraud to the TCI Tourist Board."),
    ],
    "Curacao": [
        ("Is Curacao safe for tourists?",
         "Curacao is considered one of the safer Caribbean islands for tourists. Most visited areas like Punda, Pietermaai, Mambo Beach, and Jan Thiel are well-patrolled and safe during the day. Violent crime against tourists is rare. The main risks are petty theft (pickpocketing in crowded areas, car break-ins at beaches) and opportunistic scams (taxi overcharging, rental car damage claims). Exercise normal precautions, avoid walking alone in poorly lit areas at night, and secure your valuables."),
        ("Should I rent a car in Curacao?",
         "Renting a car is the best way to explore Curacao's beaches and attractions, but take precautions. Photograph the vehicle thoroughly before driving away and insist on a written damage report signed by the agent. Use a credit card with rental car insurance. Avoid leaving any valuables visible in the car, especially at beach parking lots. The roads have potholes, so tire damage is common — confirm your insurance covers this. Reputable companies include Avis and Hertz at the airport."),
        ("What currency should I use in Curacao?",
         "Curacao uses the Netherlands Antillean guilder (ANG), but US dollars are widely accepted. The official exchange rate is approximately 1.78 ANG to 1 USD. Always ask whether prices are quoted in USD or ANG before paying. Use credit cards when possible for the best exchange rate and dispute protection. If you need cash, exchange at banks in Willemstad rather than at the airport or tourist shops, which offer worse rates."),
        ("Are the beaches safe in Curacao?",
         "Curacao's beaches are generally safe. Popular beaches like Mambo Beach, Jan Thiel, and Cas Abao have security and amenities. The main risk is theft from unattended belongings or parked cars. Never leave valuables on the beach or visible in your car. At the Mambo Beach parking lot, car window smashing is a known issue. Bring a waterproof pouch for your phone and cash, and use the hotel safe for passports and extra money."),
        ("How do I get around Curacao safely?",
         "Licensed taxis with 'TX' plates are the safest option if you are not renting a car. Always confirm the total fare before getting in. Pre-book airport transfers through your hotel. Avoid unlicensed taxis that approach you at the airport or cruise terminal. There is no Uber in Curacao. For exploring, rental cars are popular but inspect them carefully. Public buses run between Punda, Otrobanda, and some beaches but are limited in frequency and coverage."),
    ],
    "Antigua": [
        ("Is Antigua safe for tourists?",
         "Antigua is considered one of the safest Caribbean islands for tourists, with a low crime rate overall. The main risks are petty theft (pickpocketing in crowded areas, beach theft), taxi overcharging at the cruise port, and occasional robbery at isolated beaches. Tourist areas like Dickenson Bay, Jolly Harbour, and English Harbour are well-patrolled. Exercise normal precautions, avoid walking alone at night in unfamiliar areas, and secure valuables in your hotel safe."),
        ("How do taxis work in Antigua?",
         "Taxis in Antigua use fixed fares set by the Antigua and Barbuda Transport Board based on specific routes. There are no meters. The fare is per vehicle, not per person, whether you have one or four passengers. Always confirm the total fare and currency before getting in. Official taxis display Transport Board identification. From the cruise port to Dickenson Bay is approximately $15-20 per vehicle. Report overcharging to the tourist police at +268 462-3913."),
        ("What currency should I use in Antigua?",
         "Antigua uses the East Caribbean Dollar (XCD/EC$), but US dollars are widely accepted. The exchange rate is 2.70 XCD to 1 USD. Always ask 'Is that EC or US?' before any transaction. When paying by credit card at restaurants, request to be charged in XCD for the better rate. Banks in St. John's offer better exchange rates than the airport or tourist shops. Credit cards are accepted at most hotels and restaurants but carry cash for smaller vendors and taxis."),
        ("Are the cruise port areas in St. John's safe?",
         "The Heritage Quay and Redcliffe Quay areas at St. John's cruise port are safe and well-patrolled during the day. The main nuisance is aggressive taxi drivers and vendors. Walk confidently, decline firmly, and head to the official taxi stand for fair rates. The shopping areas within the port complex are secure. Venturing into surrounding neighborhoods of St. John's is generally fine during daylight but exercise caution at night and avoid poorly lit side streets."),
        ("Is it safe to rent a car in Antigua?",
         "Renting a car is a popular way to explore Antigua's 365 beaches. Drive on the left side of the road (British style). Roads can be narrow and poorly maintained outside main routes. A temporary local driving permit ($50 XCD) is required and usually arranged by the rental company. Lock the car and keep valuables out of sight. The main hazard is other drivers rather than crime. Reputable agencies operate from the airport and major hotels."),
    ],
    "Roatan": [
        ("Is Roatan safe for cruise ship passengers?",
         "Roatan is generally safe within the tourist areas of West Bay, West End, and the cruise port complexes at Mahogany Bay and Coxen Hole. Honduras has a Level 3 travel advisory, but the Bay Islands (including Roatan) have a much lower crime rate than the mainland. The main risks for cruise passengers are taxi overcharging, beach vendor scams, and the port exit fee hustle. Stay within the tourist corridor, use organized excursions or official taxi services, and you will have a safe visit."),
        ("How do I get from the cruise port to West Bay Beach?",
         "From Mahogany Bay, official Taxi Association vehicles charge $10-20 per person depending on group size, with rates posted at the port. From Coxen Hole, the official rate is $20 for one person or $25 for two. A cheaper option is to take a taxi to West End ($10-15) and then a water taxi to West Bay for $3 per person. West Bay Beach is public and free — do not pay any 'beach access fee' or let a driver divert you to a private beach club."),
        ("Is diving safe in Roatan?",
         "Diving in Roatan is world-class, with the Mesoamerican Barrier Reef right offshore. Stick to PADI or SSI affiliated dive shops with strong TripAdvisor reviews. Established shops like Sundiver Roatan, West End Divers, and Roatan Divers have excellent safety records. Confirm all-inclusive pricing, check equipment condition, and verify group sizes (no more than 6-8 divers per divemaster). Roatan has a hyperbaric recompression chamber on the island in case of emergency."),
        ("Do I need to speak Spanish in Roatan?",
         "English is widely spoken in Roatan's tourist areas, especially West Bay, West End, and the cruise ports. Many locals are bilingual. However, emergency services (police, ambulance) may primarily speak Spanish, and communication can be challenging in an emergency. Having basic Spanish phrases or a translation app is helpful. Outside the tourist areas, Spanish is the primary language."),
        ("Should I leave the cruise port area in Roatan?",
         "Yes, but with planning. West Bay Beach and West End village are the main attractions and are generally safe. Use official taxi services with posted rates or book a cruise line excursion. Avoid wandering into Coxen Hole town on foot. Do not accept rides from unmarked vehicles. Return to the port well before your ship's departure time, as traffic can be unpredictable. The port shopping complexes at Mahogany Bay offer restaurants, shops, and a beach if you prefer to stay close."),
    ],
    "Barcelona": [
        ("Is Barcelona safe for tourists?",
         "Barcelona is safe from violent crime — visitors are overwhelmingly at risk only from petty theft and pickpocketing, which remains the most reported crime in the city. Catalan police statistics show pickpocketing accounted for 48.1 percent of all crimes in 2023, and while thefts dropped 6.3 percent in 2024, the problem is deeply entrenched. r/travel 'Visiting Barcelona, Madrid, and Lisbon. How bad are the pickpockets?' (comments/1j5t2zw, 2025) captures the local sentiment: 'Barcelona is notorious for pickpocketing because there are no real consequences.' For older travellers, the practical risk is highest on L3 metro stations (Liceu, Passeig de Gràcia, Sagrada Família), on La Rambla, at Barceloneta Beach, and around Park Güell. By wearing a crossbody bag on your chest, avoiding back pockets, and staying alert in crowds, most visitors have a trouble-free experience."),
        ("What are the most common scams in Barcelona in 2025?",
         "The top scams targeting tourists are: (1) coordinated pickpocket teams on La Rambla and the L3 metro — r/AskBarcelona 'How common are pickpockets in Barcelona actually?' (comments/1irmp3r) documents first-hand accounts; (2) the 'bird poop' distraction robbery on side streets off La Rambla and Eixample; (3) fake Sagrada Família ticket sites (sagradafamilietickets.org and copycats) flagged by r/GoingToSpain 'Just realized my Sagrada Família tickets were a scam' (comments/1s733pf, 2025); (4) the African friendship-bracelet hustle on La Rambla and at Park Güell, documented by r/Barcelona 'African guy gifted us these bracelets' (comments/18hs0vl); and (5) clipboard-petition pickpocket teams at Plaça de Catalunya. The fake-police wallet check and restaurant overcharging round out the top eight."),
        ("What should I do if I get pickpocketed in Barcelona?",
         "File a police report (denuncia) immediately. The most convenient option for tourists is the dedicated tourist-police office at La Rambla 43, or the Mossos d'Esquadra station at Carrer Nou de la Rambla 76–80. You can also start a report by calling 902 102 112 (English-speaking line, seven languages supported) and must confirm it in person within 48 hours. Freeze cards immediately through your bank's app; block the phone via Apple's Find My or Google's Find My Device. You will need the denuncia number for travel-insurance claims — no denuncia, no reimbursement. If your passport is stolen, your consulate can issue an emergency replacement with the denuncia and a photo."),
        ("How do I get from Barcelona Airport safely — taxi, train, or rideshare?",
         "The RENFE R2 Nord train (T2 station, €4.90 with T-Casual card, 25 minutes to Passeig de Gràcia) is the cheapest option but r/askspain 'Do all taxis take credit card?' (comments/t2l6xx) warns it is 'lousy with pickpockets' — wear bag on chest. The Aerobús (€7.25 one-way, 35 minutes, runs to Plaça Catalunya) is comfortable for travellers with luggage. Licensed taxis charge a €39 flat rate to central Barcelona on weekdays (€41 weekends) — r/AskBarcelona 'Taxi scam?' (comments/1hh8tvn) and 'Uber airport scam' (comments/1g4xdlk) document overcharges of €50+ when drivers invoke 'luggage fees' or 'wrong terminal' tricks. Uber, Bolt, FreeNow, and Cabify all work in Barcelona with app-regulated fares and digital receipts — the safer choice for older travellers carrying bags."),
        ("How do I buy genuine Sagrada Família and Park Güell tickets?",
         "Book Sagrada Família only at sagradafamilia.org (the official Fundació Junta Constructora del Temple Expiatori de la Sagrada Família site) and Park Güell only at parkguell.barcelona. Licensed third-party resellers with buyer guarantees include GetYourGuide, Tiqets, and Viator. r/AskBarcelona '[PSA] Don't buy Sagrada Família tickets from www...' (comments/1o4t8gy, 2025) and r/GoingToSpain 'Just realized my Sagrada Família tickets were a scam' (comments/1s733pf, 2025) both warn about copycat sites with misspelled domains like sagradafamilietickets.org that produce invalid QR codes. The official Sagrada Família general ticket is €26; anything charging €50+ is marking up or running a scam. Book at least 10 days ahead in peak season — both attractions genuinely sell out, which is the pressure fake sites exploit."),
    ],
    "Seville": [
        ("Is Seville safe for tourists?",
         "Seville is one of Spain's safer major cities — violent crime against tourists is very rare. The practical risks for older travellers are financial: fake Real Alcázar ticket websites documented by r/Chase 'Got scammed by a fake Official ticket site for Real Alcázar' (comments/1rrahxh, 2025); airport and street-taxi overcharging flagged by r/Seville 'FREENOW taxi scam' (comments/1n5q7dy, 2025); the rosemary/flower-pressing shake-down near the Cathedral and Giralda; tapas-bar bill padding in Santa Cruz; and unlicensed horse-carriage pricing swaps near the Cathedral. r/sevilla 'Problem solved: no more local police!' (comments/1mhrkuw, 2025) — whose top comment mentions 'They tried to scam me with a fake cop thing' — shows local enforcement has gaps, so save tourist-police contacts in advance and file denuncias within 48 hours."),
        ("What is the most common scam in Seville?",
         "Fake Real Alcázar ticket websites top the list — r/GoingToSpain 'Reservas Feel The City Tours - BEWARE' (comments/1rq18qi, 2025) and r/Seville 'Alcazar tickets' (comments/1jsos1y, 2025) document clone sites charging €35 for what costs €14.50 on the official page, with some tickets refused at the gate. The rosemary/flower pressing scam near the Cathedral is the second most common — older women press rosemary into your hand then demand €10–€20 for a 'gift,' as r/GoingToSpain 'Places to avoid? - South Spain' (comments/1d5xpqm) documents. Airport and city taxi overcharging (flagged by multiple 2025 r/Seville threads), overpriced flamenco packages pushed by hotel concierges, tapas-bar bill padding in Santa Cruz, and fake parking-vest collectors at Cathedral free zones round out the top six."),
        ("How do I book genuine Real Alcázar and Cathedral tickets?",
         "Book Real Alcázar only at realacazarsevilla.cliqueo.es (the official booking site of the Patronato del Real Alcázar), and the Cathedral/Giralda at catedraldesevilla.es. r/Chase 'Got scammed by a fake Official ticket site for Real Alcázar' (comments/1rrahxh, 2025) documents the full chargeback experience after paying a clone. r/GoingToSpain 'Cannot purchase Alcazar tickets from their site' (comments/1skdnbb, 2025) offers the practical remedy if you've already paid a fake site: call your credit card fraud line and request a bypass while you book the official tickets in parallel. The Alcázar general ticket is €14.50; the Cathedral combined entry is €12. Anything charging €25–€35 is either markup or outright fraud. Book at least two weeks ahead in peak season — both attractions genuinely sell out."),
        ("How do I get from Seville Airport safely?",
         "The EA Airport Bus (€4, runs every 30 minutes, terminates at Plaza de Armas bus station) is the cheapest option and well-signed from arrivals. Licensed Seville airport taxis charge a flat €25 to the city centre on weekdays and €27 weekends — but r/Seville 'FREENOW taxi scam' (comments/1n5q7dy, 2025) and r/Seville 'Be careful of bolt scam' (comments/1iwkvix, 2025) document drivers changing the starting location on app pickups to inflate the fare. r/Seville 'Cabify and Uber pickup at airport' (comments/1n7c630, 2025) is blunt: 'the airport taxis are a scam; judges have ruled many times that it's one big criminal organization.' The practical rule: if you take a taxi, confirm the €25/€27 flat rate before departure; if you use an app, screenshot the fare estimate and trip map and dispute charges that don't match. Your hotel concierge can pre-arrange a fixed-price transfer."),
        ("Where should I eat in Seville without getting overcharged?",
         "Authentic tapas culture in Seville means standing at the bar, ordering in Spanish, and paying €2–€3 per tapa. Sitting at a table on a laminated-English-menu terrace in Santa Cruz or near the Cathedral will cost three to four times more for the same food. r/Seville 'Good food - authentic not tourist traps!' (comments/1ommfty, 2025) recommends side streets off Calle San Jacinto in Triana as the locals-only zone. Recommended posted-price bars: Bar Alfalfa (Calle Alfalfa), Bodega Santa Cruz 'Las Columnas' (Rodrigo Caro), Casa Moreno (Gamazo), and for a sit-down meal Abades Triana or Eslava (San Lorenzo). Walk at least two streets away from the Cathedral and Alcázar; order in Spanish or point at the Spanish menu; check your bill line-by-line before paying."),
    ],
    "Granada (Spain)": [
        ("Is Granada safe for tourists?",
         "Granada is safer than Barcelona or Madrid, and violent crime against tourists is very rare. The practical risks for older travellers are financial: fake Alhambra ticket websites (tiskets-alhambra-palace.com, alhambra.org, Walker Tours) documented across 2024–2025 in r/Granada and r/GoingToSpain; unofficial 'guided tour' resellers (Feel the City Tours) that either cancel after confirmation or deliver €70+ substitutes; pickpockets at Granada Station and in the Alhambra queue per r/GoingToSpain '$6500 item stolen in Granada' (comments/1hcartm, 2025) and r/Granada 'PSA Alhambra pick-pockets' (comments/1je5jm3, 2025); the Romani rosemary/palm-reading 'bruja' scam at Plaza Nueva and Sacromonte; and 'Free Tapas' tourist-trap restaurants near the Cathedral. Save Policía Nacional at Jefatura Superior (Plaza de los Campos, +34 958 808 000) and file a denuncia within 48 hours for insurance. The old town is walkable and the Alhambra accessible by bus line C3 from Plaza Nueva, but the steep Albaicín cobblestones are slippery when wet."),
        ("What is the most common Granada scam in 2025?",
         "Fake Alhambra ticket websites top the list — r/GoingToSpain 'Misadventure in Granada - Alhambra tickets' (comments/1ki2yxv, 2025), r/Granada 'SCAM Warning - Don't buy Alhambra tickets through tiskets-alhambra-palace.com' (comments/1ds3qjl) documenting €261 charged for €60 tickets, and r/GoingToSpain 'Fell for Alhambra Website Scam' (comments/1rg4r0g, 2025) are the canonical community anchors. The unofficial 'guided tour' resellers — Feel the City Tours (flagged on r/GoingToSpain comments/1n0r8wa, 2025), Walker Tours (r/GoingToSpain comments/1nik5t1, 2025 with a community sticky) — are second most common. Pickpocket teams at Granada Station and the Alhambra queue, the rosemary/palm-reading 'bruja' scam, 'Free Tapas' tourist-trap bait-and-switch, taxi overcharges at the GRX airport, and Sacromonte flamenco cave-tour touts round out the top seven."),
        ("How do I book genuine Alhambra tickets?",
         "The only legitimate primary booking site is tickets.alhambra-patronato.es (Patronato de la Alhambra). Book the General Visit ticket (€19.09, includes Nasrid Palaces + Generalife + Alcazaba) 2–3 months ahead for June–October visits; peak dates sell out quickly. If the official site is sold out, use only GetYourGuide, Viator (with caution on operator selection), or Tiqets — these are licensed resellers with buyer protection. Avoid any site charging over €40 for a single General Visit ticket; clone sites have been documented charging up to €261 per r/Granada (comments/1ds3qjl). Type the URL manually rather than clicking Google ads, which are routinely fake-reseller listings. If you have already paid a fake site, call your credit card fraud line immediately and request a chargeback while booking official tickets in parallel per r/GoingToSpain 'Cannot purchase Alcazar tickets from their site' (comments/1skdnbb, 2025) guidance."),
        ("How do I get from Granada Airport (GRX) to the city?",
         "Federico García Lorca Granada Airport (GRX) is 15 km west of the city centre. The Airport Bus (Alsa, €3) runs every 30–90 minutes directly to Palacio de Congresos and terminates at Plaza Gran Vía — the cheapest and most reliable option. Licensed taxis charge approximately €29–€35 to the centre with the meter running; r/travel (comments/1co6ca8, 2025) documents 2025 Easter-weekend overcharges of €40 fixed. For older travellers with luggage, Cabify or Uber provide app-regulated fares with digital receipts and screenshot protection. In the city, the regular bus (€1.40 with Credibus card) serves the Alhambra as line C3 from Plaza Nueva. r/Granada 'Transportation to Granada City Centre from GRX Airport' (comments/1ildr62, 2025) is the canonical community guide."),
        ("Where should I eat in Granada to avoid tourist traps?",
         "Granada's free-tapa tradition is real in authentic venues: order a drink at a bar and a tapa arrives complimentary. The scam is restaurants near the Cathedral and on Calle Elvira advertising 'Free Tapas!' in English while charging €8 for a drink that should be €2–€3. Walk two streets uphill into the Albaicín: Calle Calderería Vieja and Plaza Larga have posted-Spanish-menu bars with honest pricing. Community-recommended venues: Bodegas Castañeda (Calle Almireceros), Los Diamantes (Calle Rosario), Bar Ávila (Verónica de la Magdalena), Poë (Plaza Silveria). For Sacromonte flamenco evenings, book only at Cueva de la Rocío (cuevalarocio.es), La Chumbera, or Venta el Gallo per r/GoingToSpain '4 day trip to Granada' (comments/1saj3et, 2025). Avoid 'Free Tapas' signs in English, touts outside the Cathedral, and any hotel-pushed 'exclusive' cave flamenco package."),
    ],
    "Tenerife": [
        ("Is Tenerife safe for tourists?",
         "Tenerife is moderately safe, but Playa de las Américas has documented 2024–2025 street-crime problems per r/Tenerife 'Robbed in Las Americas, real' (comments/1888q1z, 2024) including armed robberies. r/Tenerife 'Is thievery a problem in Tenerife?' (comments/xe6ut1) gives the baseline: opportunistic crime concentrated at tourist-heavy locations. The practical risks for older travelers: TFS/TFN airport taxi overcharges; Europcar-TFS and budget-aggregator rental-car scams per r/GoingToSpain (comments/1ei4kan, 2025); timeshare pressure sales targeting elderly UK travelers per r/TenerifeNews 'Tenerife links to monster £28m UK timeshare scam' (comments/1oa9jvn, 2025); Teide National Park excursion upsells; Las Américas pickpockets and occasional armed robberies; and Airbnb camper-van/short-term rental fraud per r/GoingToSpain 'Tenerife Airbnb Scam' (comments/1rbvf8i, 2025). Save Policía Local Arona (+34 922 757 610) and Policía Nacional Santa Cruz (+34 922 849 500)."),
        ("What is the most common Tenerife scam in 2025?",
         "Timeshare pressure sales top the list for older UK travelers — r/TenerifeNews 'Tenerife links to monster £28m UK timeshare scam' (comments/1oa9jvn, 2025) documents a named police investigation of a £28 million UK fraud network targeting elderly victims via 'free scratchcards' and high-pressure presentation rooms. Rental-car scams at TFS airport are second most common — Europcar specifically flagged per r/GoingToSpain 'Beware of latest rental car scam in Spain' (comments/1ei4kan, 2025), alongside Goldcar, Centauro, and OK Mobility. Playa de las Américas pickpockets and robberies, Teide National Park permit/excursion scams, TFS/TFN airport taxi overcharges, and Airbnb camper-van fraud round out the top six."),
        ("How do I avoid the Tenerife timeshare scam?",
         "NEVER accept 'free scratchcards' from street touts in Playa de las Américas, Los Cristianos, or Costa Adeje — these are the entry point to high-pressure 90-minute 'presentations' that bind victims to €10,000–€50,000+ timeshare obligations. Decline all invitations to 'presentations,' 'holiday-club meetings,' or 'resort tours' with transport provided. If you've already attended a presentation and signed anything, Spain's 14-day cooling-off period (Ley 4/2012) allows you to rescind — contact a Spanish timeshare solicitor (timeshare-consumer.org) within that window. Do NOT pay any 'deposit' or 'activation fee' at the venue. If you suspect the £28m UK scam network per r/TenerifeNews (comments/1oa9jvn, 2025), contact UK Action Fraud and Spanish Guardia Civil (+34 062). r/TimeshareOwners 'PLS READ: Spanish timeshare contracts can' (comments/1mumgdg, 2025) documents the 2025 legal remedies available to victims."),
        ("How do I rent a car safely at TFS/TFN airports?",
         "AVOID Europcar at TFS, Goldcar, Centauro, OK Mobility — community-flagged repeat offenders per r/GoingToSpain 'Beware of latest rental car scam in Spain' (comments/1ei4kan, 2025) and r/VisitingTenerife 'Car Rental Scams' (comments/1qscrkn, 2025). Book direct with Cicar (Canary-Islands-based, high community trust) or Hertz. At pickup, video a walk-around narrating visible marks before signing any paperwork. Photograph all four sides, roof, wheels, and undercarriage via phone camera through the wheel well. Decline collision-damage-waiver upsells if your credit card provides car-rental insurance (Visa/MC/Amex premium typically do). On return, video the returned vehicle and retain the fuel receipt. For any post-return damage claim, dispute with your credit card within 48 hours using your evidence."),
        ("How do I visit Mount Teide without overpaying?",
         "Book the Teide cable car direct at volcanoteide.com (€45.50 adult) — this is the OFFICIAL Teleférico del Teide site despite similar-sounding third-party operators. Teide National Park general entry is FREE; reject any 'ecological fee' claims. For the final 200 m summit hike (above the cable-car station), book the free permit at reservasparquesnacionales.es 3+ months ahead during peak season — r/VisitingTenerife 'A bit confused on Teide permit' (comments/1o16l6w, 2025) confirms permits sell out. Skip hotel-concierge 'Teide excursion' packages at €80–€150 per person — a self-guided rental-car + cable-car visit costs €45 per person. Also skip 'Güimar Pyramids' tourist trap per r/Tenerife (comments/1j04f29, 2025) — they are 19th-century agricultural terraces, not ancient archaeology."),
    ],
    "Gran Canaria": [
        ("Is Gran Canaria safe for tourists?",
         "Gran Canaria is moderately safe. The practical risks for older travelers: LPA airport and Maspalomas taxi transfer overcharges; Europcar/Goldcar/Centauro rental-car scams per r/GoingToSpain 'Beware of latest rental car scam in Spain' (comments/1ei4kan, 2025); Maspalomas and Playa del Inglés timeshare pressure sales (same £28m UK elder-fraud network as Tenerife per r/TenerifeNews comments/1oa9jvn, 2025); Playa del Inglés 'hostess bar' drinks scams targeting solo male travelers per r/Ratschlag (comments/1nctef6, 2025) documenting €100/glass bills; fake websites and WhatsApp booking scams per r/Scams '[ES] lodiautos.com' (comments/1o90q8p, 2025); and opportunistic pickpocket activity in Las Palmas Vegueta and Maspalomas boardwalk crowds. Save Policía Nacional Las Palmas (+34 928 296 600)."),
        ("What is the most common Gran Canaria scam in 2025?",
         "Timeshare pressure sales top the list — the £28m UK elder-fraud network documented in r/TenerifeNews (comments/1oa9jvn, 2025) operates on both Canary Islands. Rental-car scams at LPA airport are second most common — use community-trusted Cicar or AutoReisen per r/grancanaria 'Car rent online or local?' (comments/1aqmiy8, 2024). The Playa del Inglés 'hostess bar' drinks scam per r/Ratschlag (comments/1nctef6, 2025) targets solo male travelers. LPA-Maspalomas taxi overcharges, fake-website booking fraud (lodiautos.com flagged), and pickpockets in Las Palmas Vegueta and Maspalomas round out the top six."),
        ("How do I get from LPA airport to Maspalomas safely?",
         "The legitimate licensed taxi fare from LPA to Maspalomas (50 km) is €45–€55 on the meter. Insist on the meter before boarding. Bolt app operates on Gran Canaria with app-regulated fares and digital receipts — the strongest defence against overcharges. The Global bus line 66 runs LPA to Maspalomas for €7 in 45 minutes — cheapest option for luggage-light travelers. r/grancanaria 'Taxi' (comments/1bmw6gs, 2024) notes the community uses pre-booked transfers for Maspalomas specifically to avoid overcharge pressure. Decline hotel-concierge 'partner' transfers quoted over €80; any quote over €70 for LPA-Maspalomas is overcharging. Photograph the taxi plate number from the rear windscreen on entering any licensed cab."),
        ("How do I avoid the Playa del Inglés hostess-bar scam?",
         "r/Ratschlag 'Did I just almost get scammed/robbed, or did I turn down a' (comments/1nctef6, 2025) documents the named pattern: a 'friendly local' or tourist approaches solo male travelers on the street, invites them to a 'nice bar nearby,' orders drinks with an unseen 'hostess,' and produces a bill of €200–€1,000+ for drinks that should have cost €30–€50. The defence: (1) NEVER follow an unsolicited 'friendly stranger' (particularly someone approaching with excessive friendliness) to a bar you have not chosen yourself; (2) never enter a bar without first checking prices on display at the entrance; (3) never order drinks for 'ladies' or 'hostesses' at a bar a stranger brought you to; (4) if trapped with an inflated bill, pay only what you actually consumed at reasonable rates and call Policía Nacional (+34 091) from the venue; (5) stay on the main Maspalomas or Playa del Inglés promenades; avoid side-street unmarked bars."),
        ("How do I rent a car safely at LPA airport?",
         "Book Cicar (cicar.com) or AutoReisen (autoreisen.com) — the community-canonical Canary-Islands-trusted operators per r/grancanaria 'Car rent online or local?' (comments/1aqmiy8, 2024) and r/ViaggiITA 'Car rental Gran Canaria' (comments/1m396sh, 2025). AVOID Europcar, Goldcar, Centauro, OK Mobility, Doyouspain at LPA — community-flagged repeat offenders. At pickup, video a walk-around narrating visible marks before signing paperwork. Photograph all sides, roof, wheels, and undercarriage via phone camera through the wheel well. Decline collision-damage-waiver upsells if your credit card provides car-rental insurance. For fake-website fraud per r/Scams '[ES] lodiautos.com' (comments/1o90q8p, 2025), verify any car-rental website's registered business address on Google Maps before booking — residential addresses are a clear fraud signal."),
    ],
    "Malaga": [
        ("Is Malaga safe for tourists?",
         "Malaga is moderately safe — violent crime against tourists is rare, but the 2020s have seen steady pickpocket and rental-car-scam activity particularly at the airport. r/askspain 'Where are pickpocketing and scams commonly occur in' (comments/wwj887) places Malaga on the moderate Spanish tier. The practical risks for older travelers are: AGP airport taxi overcharges especially late-night per r/GoingToSpain 'Late-night arrival at Málaga Airport' (comments/1r83qwu, 2025); AVIS/Budget/Goldcar rental-car scams per r/GoingToSpain 'AVIS BUDGET SCAMS IN MALAGA' (comments/1jit8wl, 2025); Old Town pickpockets on Calle Larios and at Alcazaba queues; Costa del Sol beach theft at Malagueta and Torremolinos; fake Alcazaba/Gibralfaro/Picasso Museum ticket resellers; and Airbnb ID-theft per r/Malaga 'AirBnB scam? Asking for my ID' (comments/1816csz). Save Policía Nacional Malaga (Plaza Manuel Azaña 1, +34 951 939 000)."),
        ("What is the most common Malaga scam in 2025?",
         "AGP airport rental-car scams top the list — r/GoingToSpain 'AVIS BUDGET SCAMS IN MALAGA' (comments/1jit8wl, 2025) names AVIS/Budget specifically for fabricated damage claims; r/Malaga 'Car rental at airport' (comments/1fd3h9v, 2024) documents two-year disputes to recover funds. Community-flagged operators to avoid: Goldcar, Centauro, OK Mobility, Doyouspain. AGP late-night taxi overcharges are second most common — €50–€80 quotes for trips that should be €20–€30. Old Town pickpockets on Calle Larios and at Alcazaba queues, Costa del Sol beach theft, fake Alcazaba/Picasso Museum ticket resellers, and Airbnb ID-theft scams round out the top six."),
        ("How do I get from Málaga Airport (AGP) safely?",
         "Between 5 AM and midnight, take the Renfe Cercanías C1 train (€2.05, every 20 minutes, 30-minute journey) to Malaga-María Zambrano station — the cheapest and overcharge-proof option. After midnight, your only option is taxi — budget €50–€80 and insist on the meter per r/GoingToSpain 'Late-night arrival at Málaga Airport' (comments/1r83qwu, 2025). Uber, Bolt, and FreeNow operate at AGP with app-regulated fares and digital receipts. For Marbella transfers (60 km west), licensed taxis charge €60–€90 day rate with overnight supplements; the Avanza bus (avanzabus.com) runs AGP to Marbella for €6 in 50 minutes. Photograph the taxi plate number from the rear windscreen on entering any licensed cab."),
        ("How do I rent a car safely in Malaga?",
         "Avoid community-flagged operators at AGP: Goldcar, Centauro, OK Mobility, Doyouspain, budget AVIS/Budget per r/GoingToSpain 'AVIS BUDGET SCAMS IN MALAGA' (comments/1jit8wl, 2025) and r/spain 'Doyouspain and Okmobility' (comments/1dd8x7w, 2025). Book direct with Hertz, Europcar, or local Cicar for better reliability (still requires walk-around discipline). At pickup, video a walk-around narrating visible marks before signing any paperwork; photograph all four sides, roof, wheels, and undercarriage via phone camera through the wheel well. Decline collision-damage-waiver upsells if your credit card provides car-rental insurance — Visa, Mastercard, and Amex premium cards typically do. On return, video the returned vehicle and retain the fuel receipt. For any post-return damage claim, dispute with your credit card within 48 hours using your photo/video evidence."),
        ("Where should I eat in Malaga without getting overcharged?",
         "Walk one street off Calle Larios (the tourist shopping strip) to find honest-priced restaurants. Community-recommended names: Pimpi (Calle Granada — Malaga institution with posted prices), Casa Aranda (Calle Herrería del Rey — famous for churros y chocolate), Uvedoble Taberna (Calle Císter — creative Andalusian tapas), El Mesón de Cervantes (Calle Álamos — quality tapas). Avoid tout-driven bars off Plaza de la Merced — r/Malaga 'People outside Bars/Nightclubs' (comments/zwvpos) documents the commission-pressure pattern. Order tapas at €2–€4 each and a glass of wine at €2.50–€3.50; above €5 for a caña signals tourist pricing. For serious Malaga food, take the train to Pedregalejo or El Palo where seafood chiringuitos serve fresh espetos (grilled sardines) at residential-quality prices."),
    ],
    "Ibiza": [
        ("Is Ibiza safe for tourists?",
         "Ibiza is moderately safe — violent crime against tourists is rare outside specific nightlife incidents, but the island's club-scene concentration creates distinct scam and safety risks not present in other Spanish destinations. The practical risks: IBZ airport fake-taxi drivers per r/ibiza 'People posing as taxi drivers at Ibiza Airport | WARNING' (comments/1k8xdeo, 2025); nightclub 'rep ticket' counterfeit wristbands; drink spiking and nightlife theft per r/NoStupidQuestions 'Was I spiked' (comments/1h59i1f, 2025); scooter and rental-car scams (Mr Rental Ibiza flagged in r/ibiza comments/1oiesgs, 2025); beach-club restaurant minimum-spend and waiter overcharging at O Beach and Ushuaïa per r/ibiza (comments/1eoy7mr, 2025); and villa Airbnb fraud per r/ibiza 'PSA: Please be careful booking Airbnbs in Ibiza' (comments/1mwbnu9, 2025). Save Policía Nacional Ibiza (+34 971 301 100)."),
        ("What is the most common Ibiza scam in 2025?",
         "Fake taxi drivers at IBZ airport top the list — r/ibiza 'People posing as taxi drivers at Ibiza Airport | WARNING' (comments/1k8xdeo, 2025) is a named 2025 community warning about unauthorised drivers inside the terminal quoting €60–€120 for €20–€35 rides. Mr Rental Ibiza and other scooter/rental-car operators are second most common — r/ibiza 'Mr Rental Ibiza - my journey with scammers' (comments/1oiesgs, 2025) documents repeated damage-claim fraud. Nightclub 'rep ticket' counterfeit wristbands, drink spiking in clubs, beach-club restaurant minimum-spend and waiter overcharging, and villa Airbnb fraud round out the top six."),
        ("How do I get from Ibiza Airport (IBZ) safely?",
         "Use ONLY the licensed yellow taxi rank immediately outside Arrivals — NEVER engage with drivers inside the terminal or in 'pickup zones' per r/ibiza 'People posing as taxi drivers at Ibiza Airport | WARNING' (comments/1k8xdeo, 2025). Confirm the fare before boarding: €20–€25 to Ibiza Town, €25–€35 to San Antonio or Santa Eulalia, €15–€20 to Playa d'en Bossa. Insist on the meter and note the modo setting. Photograph the taxi licence number from the rear windscreen. Cabify operates on some Ibiza routes with app-regulated fares. Many Ibiza hotels offer fixed-price airport transfers — verify the rate against the taxi-meter baseline before accepting. The L1 public bus serves Ibiza Town–IBZ for €2 in 15 minutes but runs infrequently."),
        ("How do I avoid drink spiking in Ibiza?",
         "Ibiza has documented 2025 drink-spiking incidents — r/NoStupidQuestions 'Was I spiked' (comments/1h59i1f, 2025) is a named first-person account. The defence: (1) NEVER leave a drink unattended — not even for 60 seconds; (2) order bottled drinks where possible and open them yourself; (3) decline drinks handed to you by strangers rather than delivered by the bartender; (4) travel with a trusted companion and set 2–3 AM and 5 AM buddy check-in rules; (5) decline all invitations to 'private villas' or 'after-hours' parties from strangers; (6) if you feel unexpectedly disoriented, ask bar staff for help IMMEDIATELY — Ibiza clubs have trained medical protocols and can call ambulances fast. r/ibiza 'Freaking out because I'm not much of an experienced party' (comments/1d8yrmw, 2025) gives the 2025 community calibration: rare but real, increasing concern. Notify hotel and Policía Nacional Ibiza (+34 971 301 100) immediately if spiking suspected."),
        ("How do I book a safe Ibiza villa or Airbnb?",
         "Book only through Airbnb, Booking.com, or VRBO with platform-verified payment and cancellation protection. Verify the property has an Ibiza Tourist Registration (VT) number — required for all licensed short-term rentals in the Balearic Islands. Demand a video call with the villa visible before any deposit. Reverse-image-search villa photos on Google Images before paying. Refuse Bizum, Western Union, or cryptocurrency payment for any deposit. r/ibiza 'PSA: Please be careful booking Airbnbs in Ibiza' (comments/1mwbnu9, 2025) warns there is 'an incredible amount of scams' in the Ibiza villa market — particularly during the May–October peak season when demand is extreme. For villa agencies, verify Ibiza Council licensing through Consell de Eivissa (ibiza.travel). If defrauded on arrival, file a denuncia at Policía Nacional Ibiza (+34 971 301 100) immediately."),
    ],
    "Palma de Mallorca": [
        ("Is Palma de Mallorca safe for tourists?",
         "Palma de Mallorca is broadly safe, but pickpocket activity is concentrated during cruise-ship crowds and summer peak. r/mallorca 'Is Mallorca safe?' (comments/18v4my5) summarises: 'Aside from pickpockets, it's very safe.' The practical risks for older travelers are: PMI airport taxi overcharges (r/VisitingMallorca 'Airport Taxi' comments/1kya2nr, 2025); Palma old town pickpockets at the Cathedral (La Seu) queue during cruise-morning hours; El Arenal and Magaluf beach/nightlife phone theft per r/Scams '[ES] iPhone stolen in Mallorca (El Arenal)' (comments/1n3xfrs, 2025) with phishing follow-ups; fake speeding-ticket letters after rental-car holidays (r/mallorca 'Fake speeding ticket' comments/1cho5y7); cruise-excursion overcharges; and short-term rental fraud on Airbnb and Idealista. Save Policía Nacional Palma (Calle Simó Ballester 1, +34 971 225 500)."),
        ("What is the most common Palma scam in 2025?",
         "PMI airport taxi overcharging tops the list — the legitimate fare to Palma centre is €20–€30, but unofficial operators quote €50–€70 with blurry meters. El Arenal and Magaluf phone-theft schemes are second most common — r/Scams '[ES] iPhone stolen in Mallorca' (comments/1n3xfrs, 2025) documents the full sequence: steal phone → trigger iCloud-delete attempts → phish victim with fake 'Apple unlock' messages. Palma Cathedral pickpocket teams during cruise-peak hours, fake post-trip speeding-ticket letters, cruise-excursion overcharges (€80–€150 per person for experiences available independently at €30), and Airbnb hidden-camera/off-platform-payment scams round out the top six."),
        ("How do I get from PMI airport to Palma or cruise port?",
         "Use the licensed yellow taxi rank at Terminal A arrivals. Confirm the approximate fare before boarding: €20–€30 to Palma centre, €25–€35 to the cruise port or El Arenal, €45–€60 to Sóller or Alcúdia per r/VisitingMallorca 'Airport Taxi' (comments/1kya2nr, 2025). Insist on the meter and photograph the taxi plate number. IMPORTANT: Uber does NOT operate in Mallorca — only Cabify (app-regulated) and licensed taxis are legitimate. A 'fake Uber' approach at the terminal is a scam variant. For older cruise passengers, the TIB public bus A1 runs from PMI to Plaça Espanya in Palma centre every 15 minutes for €5 — a reliable budget alternative. Private transfers pre-booked via 'Welcome Pickups' or similar aggregators are often lower-quality than licensed taxis at 3x the cost."),
        ("How do I avoid the El Arenal and Magaluf phone-theft scam?",
         "Rent a beachfront locker at the chiringuito (€3–€5 per session) for phone and wallet during swims. Use a waterproof pouch around your neck for phone and one card only. CRITICAL 2025 RULE per r/Scams '[ES] iPhone stolen in Mallorca (El Arenal)' (comments/1n3xfrs, 2025): if your phone is stolen, activate Find My iPhone's Lost Mode — do NOT attempt a full iCloud wipe, as wipe attempts are exploited for the phishing follow-up. Do not respond to any 'Apple unlock' or 'iCloud recovery' messages after a theft; all such messages are phishing attempts designed to bypass the phone's Activation Lock. File a denuncia at Policía Nacional Palma (+34 971 225 500) within 24 hours for insurance. For older travelers on a cruise day, keep phones and wallets locked in the cabin safe rather than carrying them to El Arenal."),
        ("Should I book a cruise-line Palma excursion?",
         "Usually no. Cruise-line 'Palma highlights' excursions charge €80–€150 per person for experiences that cost €30–€50 independently. The cruise-provided port shuttle (free or €5) or a Cabify ride (€15) gets you to central Palma. Cathedral admission is €10 at catedraldemallorca.org. A walk through Plaça Major, Paseo del Born, and Santa Catalina is at your own pace with no extra cost. r/Cruise 'Which ports don't require some sort of tour/excursion?' (comments/1g7ov53, 2024) gives the veteran-cruiser's view — Palma is absolutely doable independently. If you want a guided experience, book a small-group tour on GetYourGuide or Tiqets (€35–€50) rather than the cruise-line package — same content, flexible timing, half the price. Refunds for cancelled cruise-line excursions are notoriously difficult per r/Cruise 'Spanish flair and solar eclipse possible scam' (comments/1r9dy6p, 2025)."),
    ],
    "Lanzarote": [
        ("Is Lanzarote safe for tourists?",
         "Lanzarote is broadly safe — violent crime against tourists is very rare, and the island's small-town atmosphere makes it friendlier than mainland resort corridors. r/lanzarote 'Lanzarote with no rental car is it possible' (comments/1lpwcxd, 2025) captures the locals-first framing: 'In my experience, Spanish companies and businesses dont try to scam you. Its a refreshing change from the UK.' The practical risks for older travelers are financial: ACE airport and Puerto del Carmen taxi overcharges per r/GoingToSpain 'Beware of this taxi scam' (comments/1mk8n4c, 2025); rental-car 'scratch scam' damage claims documented across r/lanzarote and r/GoingToSpain 2025 threads; Timanfaya National Park excursion package upsells; all-inclusive resort drink and dining upsells per r/HENRYUK (comments/1n5jjb9, 2025); service-station fuel rip-offs per r/lanzarote 'I've been ripped off by a service station' (comments/1b2cgh2, 2025); and Puerto del Carmen resort-strip restaurant overcharging."),
        ("What is the most common Lanzarote scam in 2025?",
         "Rental-car 'scratch scam' damage claims top the list for any traveler who rents a vehicle — which is almost every Lanzarote holidaymaker. r/lanzarote 'Few questions about Lanzarote' (comments/1hvyvgy, 2025) documents hotel-recommended operators that quote surprise post-return damage. Community-vetted alternatives: Cicar and Auto Reisen. ACE airport taxi overcharges are second most common — the legitimate Puerto del Carmen fare is €18–€22 but blurry-meter quotes up to €35 are documented. Timanfaya excursion package upsells (hotel concierge at €45–€80 for experiences costing €12 independently at the park entrance), all-inclusive resort upsells (premium bar, à-la-carte supplements), service-station fuel rip-offs, and resort-strip tourist-menu overcharging round out the top six."),
        ("How do I get from Arrecife Airport (ACE) to the resort strips?",
         "Licensed taxi is the default: Puerto del Carmen €18–€22, Costa Teguise €25–€30, Playa Blanca €50–€60. r/GoingToSpain 'Beware of this taxi scam' (comments/1mk8n4c, 2025) warns about blurry-meter overcharges; insist on the meter and note the 'modo' setting (modo 1 = day rate, modo 2 = night/weekend). Alternatively, pre-book a 'shuttle' service through your package-holiday operator — included in many UK/Irish package deals. The Línea 22 public bus runs ACE to Puerto del Carmen for €1.40 but is infrequent and less suitable for older travelers with luggage. For late-night nightlife returns, r/lanzarote 'Taxis' (comments/1hoax0k, 2025) warns capacity is severely limited after midnight — pre-book through resort reception rather than hailing on the street."),
        ("How do I visit Timanfaya National Park without overpaying?",
         "Book the Tremesana ranger-guided walking route 2–3 months ahead at timanfaya.com (€15 per adult, limited spots, free for residents) — the best-value Timanfaya experience per r/lanzarote 'Help with Timanfaya and other must-book experiences' (comments/1isawp6, 2025). For the standard Route of the Volcanoes bus tour, show up at the park entrance and pay €12 per adult (no advance booking needed). The camel ride at the park entrance is €12 per adult (20 minutes); do NOT pre-book via hotel at €40+. Skip hotel-concierge 'Timanfaya excursion' packages at €45–€80 per person — the standalone park experience is cheaper and more flexible. Combine Timanfaya with Jameos del Agua and Cueva de los Verdes independently for ~€35 total rather than €100+ packaged. Public-bus access from Tías is available but infrequent; a rental car is the practical solution."),
        ("How do I avoid rental-car and post-rental scams in Lanzarote?",
         "Use community-vetted rental operators rather than budget aggregators. r/lanzarote 'Car rental' (comments/1ikwsp1, 2025) recommends Cicar (locally owned, high reputation, 'same to same' fuel policy) and Auto Reisen (airport-based, quality service). Avoid Goldcar, Centauro, and hotel-recommended 'local' operators flagged in r/lanzarote 'Few questions about Lanzarote' (comments/1hvyvgy, 2025). At pickup, video a walk-around narrating visible marks before signing any paperwork. Photograph every side, roof, wheels, and undercarriage via phone camera through the wheel well. Decline collision-damage-waiver upsells if your credit card provides car-rental insurance (Visa, Mastercard, Amex premium cards typically do). On return, video the vehicle and retain the fuel receipt. For post-trip fake speeding-ticket letters, verify via DGT directly (+34 060 or dgt.es) before paying anything — r/mallorca 'Fake speeding ticket' (comments/1cho5y7) documents the cross-island scam using correct personal data from leaked rental records."),
    ],
    "Córdoba": [
        ("Is Córdoba safe for tourists?",
         "Córdoba is one of Spain's safer tourist cities — r/GoingToSpain 'Is it worth going Cordoba?' (comments/1qwqtj9, 2025) and r/howislivingthere 'What is it like living in Córdoba Spain?' (comments/1si42le, 2025) both describe it as less-touristed and friendlier than Seville or Granada. Violent crime against tourists is very rare. The practical risks for older travelers are financial: fake Mezquita-Catedral ticket websites charging €25–€45 for €13 tickets; Judería narrow-alley pickpockets during peak Mezquita hours and May Patios Festival queues; fake parking attendants in Judería free-zone hours per r/spain 'Fake parking attendants? Andalucia' (comments/6qkmks); tourist-menu overcharging near the Mezquita; AVE station taxi overcharges; and Idealista apartment-rental fraud per r/GoingToSpain 'looking for a room/flat in Cordoba' (comments/1jcc510, 2025). Save Policía Nacional Córdoba (Avenida de Medina Azahara, +34 957 594 500)."),
        ("What is the most common Córdoba scam in 2025?",
         "Fake Mezquita-Catedral ticket websites top the list — r/GoingToSpain 'Mezquita-Catedral Ticket' (comments/1pbjemo, 2025) documents the community confusion: 'Where do I purchase the tickets for Mezquita Catedral Cordoba online? I see three different websites with different pricings' — the legitimate site is mezquita-catedraldecordoba.es at €13. Fake parking attendants demanding €3–€10 at Judería and riverside free zones are second most common. Córdoba AVE station taxi overcharges, Judería pickpockets during Mezquita peak hours, tourist-menu restaurant overcharging near the Mezquita, and Idealista rental fraud round out the top six."),
        ("How do I visit the Mezquita-Catedral without getting scammed?",
         "Book tickets only at mezquita-catedraldecordoba.es — adult general admission is €13. The monument offers free entry 8:30–9:30 AM Monday–Saturday (limited, arrive early). Licensed third-party resellers: GetYourGuide and Tiqets only. Avoid Google ads for 'Mezquita tickets' — these routinely lead to clone sites and third-party resellers at €25–€45. r/GoingToSpain 'What places are guided tours worth it?' (comments/1p1v3i5, 2025) recommends skipping the guided tour since the monument's audio guide is already excellent. For older travelers, plan a 90-minute visit at 10–11 AM on weekdays to avoid both the 8:30 AM queue rush and the 1–3 PM peak tour-group density."),
        ("How do I get from Córdoba AVE station to the old town?",
         "The legitimate taxi fare from Córdoba AVE station to the Mezquita area is €6–€9 on the meter. Use Cabify or Bolt for app-regulated fares with digital receipts and starting-location screenshots. r/BuenosAires 'Cabify without GPS' (comments/1n57saj, 2025) documents a 2025 Córdoba-specific variant where drivers claim the app 'didn't register' and demand cash — insist on app-registered trips only. If using a licensed taxi, insist on the meter and confirm the €6–€9 range before boarding. The 25-minute walk from the station via Paseo de la Ribera is feasible for most mobility levels with rolling luggage. Avoid fixed 'flat fare' quotes of €12–€18 which are overcharges."),
        ("Where should I eat in Córdoba without tourist-trap overcharging?",
         "Walk at least two streets off Calle Cardenal Herrero (the tourist strip surrounding the Mezquita) to find locals-first restaurants. r/GoingToSpain 'Review of my Two Trips to Spain' (comments/1f4igxh, 2024) names honest venues: Taberna Salinas (Calle Puerto — classic Andalucían), Bodegas Campos (Calle Lineros — cellar atmosphere), Bar Santos (Calle Magistral Gonzalez Francés — famous giant tortilla), Casa Mazal (Calle Tomás Conde — Moroccan-Sephardic). Order tapas at €2–€4 each rather than a tourist 'menú del día' at €25+. Authentic Córdoba specialties to order: salmorejo (cold tomato soup), flamenquín (rolled pork), rabo de toro (oxtail stew), berenjenas con miel (eggplant with cane honey). Refuse any bread or olives not explicitly ordered."),
    ],
    "Valencia": [
        ("Is Valencia safe for tourists?",
         "Valencia is moderately safe — violent crime against tourists is very rare, but the 2020s have seen a documented escalation in organised pickpocket and beach-theft activity. r/askspain 'Where are pickpocketing and scams commonly occur in' (comments/wwj887) captures the 2025 community view: 'Getting worse in Valencia too. Lots of tourist get robbed, especially on the beach, when people at drunk. Organised crim' e teams now operate at Malvarrosa Beach and in the Ciutat Vella. r/valencia 'Got robbed at the beach' (comments/1fp6gam, 2025) documents a coordinated scarf-seller crew targeting swim victims. Other practical risks: paella tourist-trap restaurants (r/valencia 'Every city has one' comments/1kn9azh, 2025 names Casa Patacona); fake parking attendants at Malvarrosa; Las Fallas festival pricing gouges (3–5x inflation in March); Ciutat Vella pickpocket teams at Plaza de la Reina and Valencia Nord station; and heavy Idealista rental fraud with the 2025 Avenida de Burjassot police investigation (r/GoingToSpain comments/1s63ana). Save Policía Nacional Valencia (Gran Vía de Ramón y Cajal, +34 963 539 400)."),
        ("What is the most common Valencia scam in 2025?",
         "Malvarrosa Beach theft leads — r/valencia 'Got robbed at the beach. the people of Valencia were' (comments/1fp6gam, 2025) documents the coordinated 'scarf-seller' crew pattern where Team A steals bags while you swim and Team B sells you a scarf to cover up. Paella tourist-trap restaurant overcharging is second most common — r/valencia 'Every city has one: Valencia Edition' (comments/1kn9azh, 2025) and r/valencia 'All the restaurants say paella price is per person' (comments/1l0qd7c, 2025) both document per-person pricing at €30+ for reheated paella. Ciutat Vella pickpocket gangs at Plaza de la Reina and Valencia Nord, Idealista rental fraud per r/GoingToSpain 'PSA: Documented rental scam' (comments/1s63ana, 2025), Las Fallas festival 3–5x price gouging per r/travel (comments/1rsjbv5, 2025), and fake parking attendants at Malvarrosa free-evening zones round out the top six."),
        ("How do I eat authentic Valencian paella without getting scammed?",
         "Skip Malvarrosa beachfront 'paella restaurants' entirely — all are marketed to one-time tourists. For authentic paella, book Casa Carmela (Calle Isabel de Villena, 1930s family operation, beachfront but respected), La Pepica (same Malvarrosa strip but Hemingway-era genuine), or Restaurante La Riua (Ciutat Vella). Eat paella at lunchtime only — dinner paella is always reheated. Expect €18–€25 per person at authentic restaurants, €15–€18 in residential Ruzafa. Authentic Valencian paella includes chicken, rabbit, garrofón beans, green beans, and tomato — any menu adding chorizo or shrimp is deviating from tradition per r/GoingToSpain 'Paella' (comments/1of6f8t, 2025). r/valencia 'All the restaurants say paella price is per person' (comments/1l0qd7c, 2025) captures the frustration: 'Run away from restaurant paella, it's a tourist trap and a robbery for mere rice with things.'"),
        ("How do I stay safe at Malvarrosa Beach?",
         "Rent a beachfront locker at Malvarrosa chiringuito kiosks (€3–€5 per session) for valuables before your swim. Use a waterproof pouch around your neck for phone and one card during swims. Never leave bags unattended on a towel — r/valencia 'Got robbed at the beach. the people of Valencia were' (comments/1fp6gam, 2025) documents coordinated crews that operate here. Beware the 'scarf-seller' follow-up: if you return to find your bag stolen and someone immediately approaches selling scarves or cover-ups, they are part of the same crew — walk away and go directly to the nearest chiringuito for help. File a denuncia at Policía Nacional Valencia (+34 963 539 400) within 48 hours for insurance claims. For older travelers, Las Arenas section is slightly less crowded and better-observed than central Malvarrosa; chiringuitos there are the best spot for lockers and watchful staff."),
        ("How do I avoid accommodation scams in Valencia?",
         "Book only through Airbnb or Booking.com with platform-verified payment and cancellation protection. For Idealista listings (common for stays over a week), r/GoingToSpain 'PSA: Documented rental scam at Avenida de Burjassot' (comments/1s63ana, 2025) is the named 2025 police-investigation anchor — 18+ illegal units in a single building, 3 police reports, criminal investigation open. Demand a video call with the apartment visible before transferring any money, reverse-image-search listing photos on Google Images, and refuse Western Union, Bizum, or cryptocurrency payments for accommodation. r/valencia 'How do I know I'm not being scammed while apartment' (comments/1dpr8ge) gives the universal Spanish-rental rule: 'neither pay anything nor sign any contract until you have personally seen the apartment.' For Las Fallas (March 15–19), book 6+ months ahead — prices triple and scam listings proliferate. If defrauded, file a denuncia at Policía Nacional Valencia (Gran Vía de Ramón y Cajal) immediately."),
    ],
    "Bilbao": [
        ("Is Bilbao safe for tourists?",
         "Bilbao is among Spain's safest major cities — violent crime against tourists is very rare and the Guggenheim corridor is heavily CCTVed. r/Bilbao 'Is this area safe?' (comments/1ghv74v, 2025) summarises the local view: serious pickpocket operations work 'train stations and crowded areas' rather than the tourist-core streets. The practical risks for older travellers are financial: rental-car 'scratch scam' damage claims flagged by r/GoingToSpain 'Beware Europcar scratch scam' (comments/1o00jtv, 2025); airport and Bilbao-to-Donostia transfer overcharges (€350 quotes documented for what should be €7–€12 PESA bus); fake Guggenheim 'skip-the-line' tour resellers; fake-police 'traffic fine' confidence scams per r/GoingToSpain 'What happened yesterday..' (comments/1ppn0bj, 2025); and moderate pickpocket activity at Abando train station and during Casco Viejo pintxos crawls. Save Ertzaintza Deusto (Avenida Ramón y Cajal, +34 94 607 0000) for denuncia filing within 48 hours for insurance claims."),
        ("What is the most common Bilbao scam in 2025?",
         "Rental-car 'scratch scam' damage claims top the list for any traveller who rents a vehicle — r/GoingToSpain 'Beware Europcar scratch scam' (comments/1o00jtv, 2025) documents a $200 bogus charge for water-spot-like marks, and the pattern recurs across Europcar, Sixt, Hertz, and budget aggregators. Airport transfer overcharges are second most common — the legitimate BIO-to-centre fare is €30–€35 on the meter, but peak-event drivers quote €50–€70 and Bilbao-to-Donostia private transfers can quote €350 versus the €7–€12 PESA bus rate per r/Bilbao 'Getting to San Sebastian tomorrow' (comments/1sc3uye, 2025). Casco Viejo pintxos-crawl pickpockets, fake Guggenheim ticket resellers, and fake-police 'traffic fine' shakedowns round out the top five."),
        ("How do I get from Bilbao Airport (BIO) to the city?",
         "The Bizkaibus A3247 airport express runs every 15–30 minutes, takes 25 minutes to Plaza Moyua in central Bilbao, and costs €3 — by far the cheapest and most reliable option. Licensed taxis charge approximately €30–€35 on the meter; r/Bilbao 'Landing in Bilbao at 7:20 PM' (comments/1kotd38, 2025) warns peak-event pricing doubles on major football or convention nights. Cabify and Bolt operate with app-regulated fares and digital receipts — the safer choice if you must use a car. For Bilbao-to-San Sebastián transfers (100 km), take the PESA bus (pesa.net) from Bilbao Airport directly to San Sebastián Termibus at €7–€12 in 80 minutes rather than a €110–€130 licensed taxi or €350 private-transfer aggregator. Avoid pre-booked 'airport transfer' services like Welcome Pickups which r/travel (comments/16xzfv9) flags as unregulated."),
        ("How do I buy genuine Guggenheim Bilbao tickets?",
         "Book Guggenheim tickets only at guggenheim-bilbao.eus — adult admission is €18. Licensed third-party resellers with buyer protection include GetYourGuide and Tiqets. Avoid Google ads for 'Guggenheim Bilbao tickets' which lead to clone sites and resellers charging €35–€60. r/Bilbao 'Give away : Guggenheim tickets' (comments/1mr6q01, 2025) and r/Bilbao 'Visiting recommendations' (comments/16knogf) both recommend going direct rather than any packaged tour. The museum walks easily from the Guggenheim metro stop (Line 1) or a 10-minute walk from Abando/Termibus. For cruise arrivals at the Port of Bilbao/Getxo, take Metro L1 to Moyúa (€2.45) rather than cruise-excursion 'Guggenheim Plus' packages at €80+ per person. Decline 'Bilbao day trip from Madrid' packages at €120+ per person — self-guided visits cost €25 plus train fare."),
        ("Where should I eat in Bilbao without tourist-trap overcharging?",
         "Bilbao's pintxos scene is widely considered better-value than San Sebastián's — r/PutAnEggOnIt 'El Huevo Frito in Bilbao' (comments/bnqx8j) sums it up: 'Less tourism = less tourist traps = higher quality food.' r/Bilbao 'Short trip to Bilbao' (comments/1lqva7j, 2025) confirms the 2025 consensus: 'tourist trap food places are not existing here.' For honest pricing, walk one block off Plaza Nueva into Calle Perro, Calle Somera, or Calle Barrenkale. Community-recommended names: La Viña (jamon specialist), El Globo (txangurro, near Diputación), La Octava, Cafe Bar Bilbao (Plaza Nueva corner), and for serious eaters, Asador Etxebarri (Axpe, 50 km outside Bilbao — book 3 months ahead for Michelin-starred wood-fire cooking). Order pintxos one-by-one at €2–€3 each rather than a fixed 'pintxos menu' at €20+ per person. Evenings 8 PM onwards are the local standard; lunchtime Plaza Nueva arcade is tourist pricing."),
    ],
    "San Sebastián": [
        ("Is San Sebastián safe for tourists?",
         "San Sebastián (Donostia) is one of Spain's safer major cities — violent crime against visitors is very rare, and the Parte Vieja is well-policed. r/solotravel 'Spain pick pocketing' (comments/aoees1) places the Basque Country on the safer end of the Spanish spectrum. The practical risks for older travellers are financial: airport and Bilbao-to-Donostia transfer overcharges up to €350 per r/Bilbao 'Getting to San Sebastian tomorrow' (comments/1sc3uye, 2025); opportunistic beach theft at Playa de la Concha per r/Bilbao 'Phone Pick-pocketed in Bilbao' (comments/1lq8q1m, 2025); Parte Vieja pintxos tourist-menu overcharging per r/GoingToSpain 'San Sebastián' (comments/1q63hg4, 2025) which flags 2025 gentrification; overpriced 'private pintxos tour' hotel-concierge packages; and short-term rental fraud on Idealista per r/GoingToSpain 'Looking for a shared room in San Sebastian' (comments/1mr4kul, 2025). Save Policía Municipal Donostia (+34 943 450 000) and Ertzaintza Donostia (Plaza Bizkaia, +34 943 408 800)."),
        ("What is the most common San Sebastián scam in 2025?",
         "Airport and Bilbao-to-Donostia transfer overcharging tops the list — legitimate rates are PESA bus €7–€12 and licensed taxi €110–€130 for the 100 km, but hotel concierges quote €250–€350 per r/Bilbao 'Getting to San Sebastian tomorrow' (comments/1sc3uye, 2025). Parte Vieja pintxos-bar tourist-menu overcharging is second most common — laminated-English-photo menu bars on Fermín Calbetón charge €6–€8 per pintxo when the genuine rate is €3–€4 per r/PutAnEggOnIt 'El Huevo Frito in Bilbao' (comments/bnqx8j). Playa de la Concha beach theft of unattended phones and wallets, overpriced packaged 'private pintxos tour' concierge upsells, Donostia train-station pickpockets, and short-term rental/Idealista apartment-booking fraud per r/GoingToSpain 'Why am I seeing a lot of SCAM posts related to housing/' (comments/1ed4g94) round out the top six."),
        ("How do I get from Bilbao Airport to San Sebastián?",
         "The PESA bus (pesa.net) runs directly from Bilbao Airport to San Sebastián Termibus at €7–€12, 80 minutes, every hour from 5 AM to 11 PM — the cheapest and most reliable option. Licensed taxis charge approximately €110–€130 on the meter per r/GoingToSpain 'Travelling to San Sebastian' (comments/1ckms4k, 2025); insist on the meter and confirm the range before departure. r/Bilbao 'Getting to San Sebastian tomorrow' (comments/1sc3uye, 2025) documents hotel concierge quotes up to €350 — any quote above €150 is overcharging and you should decline and use PESA instead. The small San Sebastián Airport (EAS, Hondarribia) has limited flights; if you fly in, the E21 Ekialdebus (€2.55) or licensed taxi (€30–€35) serves the centre. For late-night arrivals, r/GoingToSpain 'San Sebastián taxis after 11PM' (comments/1n57nxn, 2025) warns of scarcity pressure — book in advance with Radio Taxi Donosti (+34 943 464 646)."),
        ("How do I eat pintxos like a local in San Sebastián?",
         "Walk past Fermín Calbetón and Calle 31 de Agosto's first two blocks — the tourist strip — to find locals-first bars. r/finedining 'First visit to San Sebastian/Donostia' (comments/1mggmsn, 2025) names the honest-pricing venues: Bar Nestor (tortilla and beef, queue discipline required — two sittings at 1 PM and 8 PM), Ganbara (ham and mushroom pintxos), Borda Berri (creative Basque), La Cuchara de San Telmo (beef cheeks and foie gras). Order pintxos one-by-one at €3–€4 each rather than a fixed 'pintxos menu' at €20+ per person. Eat at 8 PM onwards (txikiteo hour) with locals rather than 2 PM with cruise crowds. For serious Michelin experience, book Akelaré, Arzak, or Mugaritz directly from each restaurant's website at €250–€350 per person. Avoid hotel-concierge 'private pintxos tours' priced €80–€120 per person — a self-guided evening visiting five genuine bars costs €35–€45."),
        ("How do I avoid accommodation scams in San Sebastián?",
         "Book only through Airbnb or Booking.com with platform-protected payment and cancellation protection. For Idealista listings (common for stays over a week), r/GoingToSpain 'Looking for a shared room in San Sebastian' (comments/1mr4kul, 2025) documents persistent fraud where 'owners' demand full deposits before any viewing. Demand a video call with the apartment visible before transferring any money, reverse-image-search listing photos on Google Images, and refuse Western Union, Bizum, or cryptocurrency payments for accommodation. For hotels, Hotel Maria Cristina (Luis Martín Santos, iconic), Hotel de Londres (beachfront on La Concha), and Hotel Codina (Ondarreta) are community-verified. The housing-supply crunch driven by tourism gentrification has made Donostia Spain's top-ranked fraud hotspot for short-term rentals per r/GoingToSpain 'Why am I seeing a lot of SCAM posts related to housing/' (comments/1ed4g94, 2024). If defrauded, file a denuncia at Ertzaintza Donostia (Plaza Bizkaia, +34 943 408 800) immediately for both police pursuit and credit card chargeback paperwork."),
    ],
    "Toledo": [
        ("Is Toledo safe for tourists?",
         "Toledo is one of Spain's safer tourist cities — violent crime against day-trippers is virtually non-existent, and the compact old town is walkable in a day. The practical risks for older travellers on a Madrid day trip are: fake combo-ticket websites (clones of catedralprimada.es and Patrimonio Nacional) charging €30–€45 for the €12 Pulsera Turística that covers 7 monuments; decorative-replica knife and sword shops marketing mass-produced replicas as 'authentic Toledo damascene' per r/spain 'Toledo and its Knives!' (comments/4zj2gq); distraction pickpockets in Plaza de Zocodover and the narrow Judería alleys per r/askspain (comments/1lxwowm, 2025); tourist-menu restaurant overcharging on the Zocodover perimeter; 'free walking tour' guilt-trip tip demands that funnel into commission shops; and taxi overcharges at Toledo Train Station on arrival from Madrid's AVE. Save Policía Nacional Toledo (Comisaría de Toledo, Calle Peñas de la Cruz, +34 925 284 000) and file a denuncia within 48 hours for insurance."),
        ("What is the best way to visit Toledo on a Madrid day trip?",
         "The AVE high-speed train from Madrid's Atocha station to Toledo runs every 60–90 minutes, takes 33 minutes each way, and costs €13–€23 depending on advance booking. Book round-trip tickets via renfe.com with a 30-minute arrival buffer at Atocha for security screening. On arrival at Toledo Station, either take the 15-minute steep walk up Cuesta de la Vega (r/spaintravel comments/1klt3sy, 2025 calls it 'picturesque but steep') or a Cabify/Uber ride (€5–€7) — the station taxi rank routinely quotes €10–€15 fixed prices. Spend 5–6 hours in the old town (Cathedral, Alcázar, one synagogue, lunch off Plaza de Zocodover), then return on a late-afternoon AVE. For older travellers or those with mobility concerns, use the free outdoor Escalera Mecánica (covered escalator) between Paseo de Recaredo and the Alcázar."),
        ("How do I buy genuine Toledo Cathedral and Alcázar tickets?",
         "The Pulsera Turística wristband (€12 at any of the 7 participating monuments on arrival) covers Cathedral, two synagogues, San Juan de los Reyes, Santo Tomé, Mezquita Cristo de la Luz, and Iglesia de los Jesuitas — the cheapest and most flexible option. For online pre-booking, the Cathedral is catedralprimada.es (€12), the Alcázar/Museo del Ejército is ejercito.defensa.gob.es (€5), and individual synagogues are Sinagoga del Tránsito (€3) and Santa María la Blanca (€4). Licensed third-party resellers with buyer protection: Tiqets (recommended on r/Madrid comments/125y6yf for the Alcázar) and GetYourGuide. Avoid Google ads for 'Toledo tickets' which routinely lead to clone sites charging €30–€45 for the €12 wristband equivalent. r/GoingToSpain 'Toledo: Which places should I buy tickets for?' (comments/1j92hpv, 2025) is the canonical community planning thread."),
        ("Are Toledo knives and swords genuine or a tourist trap?",
         "It depends entirely on where you buy. Genuine Toledo damascene is still made by a small number of traditional workshops — Mariano Zamorano (Calle Ciudad 19) and Simón Cortés (Paseo de San Cristobal) are the most respected — where a real folding knife starts around €120 and a sword can exceed €500. The tourist shops along Calle del Comercio and around Plaza de Zocodover sell mass-produced replicas (often outsourced; r/knives comments/1ieuv0p documents one 'Toledo' knife with an Oklahoma seal) priced €40–€90. r/spain 'Toledo and its Knives!' (comments/4zj2gq) is blunt: 'Toledo is now better known for their decorative replicas (mostly swords), so technically speaking nothing is real.' r/knives 'My friend got me a Damascus folding knife from Toledo' (comments/1mvz1be, 2025) questions even some named-workshop output. If you want a real piece, visit the workshop and pay workshop prices. Otherwise, accept that the €60 souvenir blade is a decorative replica — pretty, but not hand-forged damascene. Confirm your home country's knife-import rules before purchasing."),
        ("Where should I eat in Toledo?",
         "Walk at least two streets off Plaza de Zocodover before sitting down. Restaurants directly on the plaza and the Cathedral square price for day-trippers who won't return — €18–€25 'Menú del Día' that is actually the tourist menu, unlisted cover charges, and terrace supplements not mentioned at seating. Honest local venues repeatedly mentioned on r/GoingToSpain: Alfileritos 24 (Calle Alfileritos — honest €16 Menú del Día), Bar Ludeña (Plaza Magdalena — classic perdiz estofada), Restaurante Adolfo (Calle Hombre de Palo — upscale but honest), and El Trebol (Calle de los Reyes Católicos). Order in Spanish, check drink prices before ordering (€3 for a caña or vino tinto is fair; above €5 signals tourist pricing), and refuse any bread, olives, or water not explicitly ordered. For sweet carcamusas or mazapán from the cloistered Santa Isabel de los Reyes convent, drop €5–€8 in the turno (rotating wheel) for genuine cloister-baked product."),
    ],
    "Naples": [
        ("Is Naples safe for tourists?",
         "Naples is safe for the vast majority of tourists, though it requires more street awareness than northern Italian cities. Violent crime against tourists is very rare. The main risks are pickpocketing (concentrated around Napoli Centrale station and on the Circumvesuviana train), moped bag-snatching (scippatori), and overcharging at tourist restaurants. The historic center, Vomero, and Chiaia neighborhoods are generally safe at all hours. With basic precautions like securing your bag and being aware of your surroundings, most visitors have a positive experience."),
        ("Which areas of Naples should tourists avoid?",
         "The area immediately around Napoli Centrale station and Piazza Garibaldi requires extra caution, especially at night. The Forcella neighborhood east of Spaccanapoli and parts of the Quartieri Spagnoli can feel intimidating after dark but are generally safe during the day. Scampia and Secondigliano in the northern suburbs are residential areas with organized crime presence and no tourist attractions. Stick to the main tourist circuit (Spaccanapoli, Via dei Tribunali, Vomero, waterfront, Chiaia) and you will be fine."),
        ("How do I get from Naples airport to the city safely?",
         "The safest option is the Alibus shuttle (5 euros, runs every 15 to 20 minutes) which goes directly to Napoli Centrale station and the port. For taxis, use the official stand outside arrivals and confirm the fixed-rate fare before departure (16 to 23 euros to the city center depending on your zone). Do not accept offers from anyone approaching you inside the terminal. Uber and Free Now apps also work in Naples and provide GPS-tracked, pre-priced rides."),
        ("Is the Circumvesuviana train safe?",
         "The Circumvesuviana is safe to ride but is a known hotspot for pickpockets targeting tourists heading to Pompeii and Sorrento. Keep all bags zipped and in front of your body. Stand with your back to a wall if possible. Be extra cautious at station stops during boarding and exiting. For a more comfortable experience, the Campania Express offers reserved seating on the same route for a few euros more. Avoid empty carriages, especially late in the day."),
        ("Can I use Uber in Naples?",
         "Uber operates in Naples but availability can be limited compared to other European cities. The Free Now app (formerly MyTaxi) is more widely used in Naples and connects to licensed taxi drivers with app-based pricing. Both apps provide the advantage of GPS tracking, upfront pricing, and a digital receipt, eliminating the risk of meter manipulation or route padding. Regular licensed taxis are also reliable when taken from official stands."),
    ],
    "Cartagena": [
        ("Is Cartagena safe for tourists?",
         "The tourist areas of Cartagena, including the Walled City, Getsemaní, and Bocagrande, are generally safe during the day and into the early evening. Tourist police (Policia de Turismo) patrol the main areas and are identifiable by their labeled vests. The primary risks are petty scams (overcharging, bracelet sellers, vendor pressure), drink spiking in nightlife settings, and opportunistic theft. Violent crime against tourists is rare but not unheard of. Most visitors who exercise normal precautions have a safe and enjoyable trip."),
        ("Which areas of Cartagena should tourists avoid?",
         "Stay within the Walled City, Getsemaní, Bocagrande, Manga, and Castillogrande. Avoid the neighborhoods of Nelson Mandela, Olaya Herrera, and El Pozzón, which are residential areas with higher crime rates and no tourist infrastructure. Even within safe zones, be cautious on quiet side streets in Getsemaní after midnight. The area immediately outside the Walled City walls can be sketchy at night, particularly near the India Catalina statue and along the road toward La Boquilla."),
        ("Is it safe to use Uber in Cartagena?",
         "Uber operates in Cartagena and is generally the safest transportation option because it provides GPS tracking, upfront pricing, and a digital record of your trip. InDriver is another popular app where you can negotiate fares. Both are safer than hailing random taxis on the street. Note that Uber operates in a legal gray area in Colombia, so drivers may ask you to sit in the front seat and may not display an Uber sticker."),
        ("What should I do if I am drugged with scopolamine in Cartagena?",
         "If you suspect drugging, call 123 (Colombia emergency line) immediately and get to the nearest hospital. Clínica Boca Grande and Hospital Universitario del Caribe are the main facilities. Do not go back to your hotel alone. Alert someone you trust. File a police report (denuncia) even if you do not remember details, as toxicology tests can confirm the substance. Contact your embassy for assistance, especially if your passport or important documents were stolen."),
        ("How much should a taxi cost in Cartagena?",
         "Cartagena taxis do not use meters; fares are negotiated. Standard rates: within the Walled City or Getsemaní, 8,000 to 12,000 COP; Walled City to Bocagrande, 10,000 to 15,000 COP; airport to Walled City, 15,000 to 25,000 COP; Walled City to La Boquilla, 20,000 to 30,000 COP. Late-night fares (after midnight) are typically 20 to 30 percent higher. Always agree on the fare before entering the vehicle and have the exact amount ready in small bills."),
    ],
    "Chicago": [
        ("Is downtown Chicago safe for tourists?",
         "Yes — the Loop, Magnificent Mile, River North, Lincoln Park, and Streeterville are heavily patrolled and generally safe during the day and evening. Most violent crime in Chicago occurs in specific South and West Side neighborhoods far from where tourists spend time. Standard urban precautions apply: be aware of your surroundings, avoid isolated areas late at night, and keep valuables secured."),
        ("Are the CTA trains safe to ride as a tourist?",
         "CTA trains are generally safe during daytime and early evening hours. Ride in the car closest to the operator for added security. Avoid riding alone late at night — use rideshare services after 10 PM if traveling solo. Keep your phone out of sight and your bag zipped. The Blue Line to O'Hare and the Brown Line to popular North Side neighborhoods are among the safest routes."),
        ("Should I take a taxi or rideshare from O'Hare Airport?",
         "Use the official taxi queue outside the terminal or request a ride through the Uber or Lyft app. Never accept a ride from anyone who approaches you inside the terminal — these are unlicensed 'pirate taxi' operators who may overcharge five times the normal fare. The standard metered taxi fare from O'Hare to downtown is approximately $40-50. The CTA Blue Line train runs directly from O'Hare to downtown for $5."),
        ("How do I avoid getting scammed on the Magnificent Mile?",
         "Keep your valuables secured in front pockets or zippered bags. Decline all unsolicited offers of bracelets, CDs, or charity donations with a firm 'no thank you' while continuing to walk. Never stop for shell games or street gambling. Be especially alert during the holiday shopping season when pickpocket teams are most active."),
        ("What should I do if I'm pickpocketed in Chicago?",
         "Immediately lock your phone remotely using Find My iPhone or Google Find My Device. Call your bank to freeze cards. File a police report with CPD — you can do this by calling 311 or visiting the nearest district station. If your passport was stolen, contact your country's consulate. Many nations maintain consulates in downtown Chicago. For US passport holders, call the State Department at 1-877-487-2778."),
    ],
    "Boston": [
        ("Is Boston safe for tourists?",
         "Boston is one of the safest major cities in the United States for tourists. The areas visitors frequent — Back Bay, Beacon Hill, the North End, the Freedom Trail, Cambridge, and the waterfront — have low crime rates. The main risks are pickpocketing in crowded areas, tourist overcharging near Faneuil Hall, and parking-related scams. Standard urban awareness is sufficient for a safe visit."),
        ("Are there areas of Boston tourists should avoid?",
         "The vast majority of Boston's tourist attractions are in safe neighborhoods. Areas with higher crime rates — parts of Roxbury, Dorchester, and Mattapan — are residential neighborhoods well away from tourist destinations. At night, stick to well-lit areas and avoid empty side streets in any neighborhood. The MBTA is safe during operating hours but use rideshare late at night."),
        ("How do I avoid getting overcharged at restaurants near Faneuil Hall?",
         "Always check for a menu with visible prices before sitting down. Read recent Google and Yelp reviews. Ask upfront about service charges or automatic gratuity. Better yet, walk a few blocks to the North End for authentic Italian food at fair prices, or try restaurants in Fort Point and the South End for excellent meals without the tourist markup."),
        ("Is it safe to drive and park in Boston as a tourist?",
         "Driving in Boston is notoriously challenging due to narrow streets, aggressive drivers, and confusing rotaries. Parking is expensive and regulations are strict — the city tows aggressively. If you must drive, use the ParkBoston app and read all posted signage carefully. Many visitors find it easier to walk, use the T, or take rideshares. Never scan QR codes on meters or respond to parking ticket text messages."),
        ("Can I buy tickets to Fenway Park safely from scalpers?",
         "Street scalpers outside Fenway frequently sell counterfeit tickets with duplicated barcodes. The safest options are the official Red Sox website, the MLB Ballpark app, or guaranteed resale platforms like StubHub. There is a 'no scalp' zone near the Ted Williams statue where fans sell extra tickets at face value — this is the safest street option. Single tickets sometimes appear at the box office on game day."),
    ],
    "San Diego": [
        ("Is San Diego safe for tourists?",
         "San Diego is considered one of the safest large cities in the United States. Tourist areas like the Gaslamp Quarter, La Jolla, Coronado, Balboa Park, and the beach communities have low crime rates. The main risks for visitors are scam-related — pedicab overcharging, fake attraction tickets, and parking phishing — rather than violent crime. Standard urban awareness is more than sufficient for a safe visit."),
        ("Is it safe to walk across the border to Tijuana from San Diego?",
         "Many tourists safely make day trips to Tijuana via the San Ysidro pedestrian crossing. The main risks are scammers near the border offering fake services, overcharging taxi drivers on the Mexican side, and long return wait times. Use only official border facilities, check CBP wait times in advance, carry your passport, and avoid engaging with unofficial helpers. Do not carry large amounts of cash."),
        ("How do I avoid getting scammed by pedicabs in the Gaslamp Quarter?",
         "Always demand the total fare in writing for all passengers before boarding. Confirm whether the rate is per person, per minute, or a flat fee. Take a photo of any posted rate card. Better yet, walk or use a rideshare app — the Gaslamp Quarter is compact and most destinations are within a 10-minute walk. San Diego adopted stricter pedicab regulations in 2024, but enforcement is still catching up."),
        ("Are San Diego Zoo tickets sold on Craigslist legitimate?",
         "Almost never. The San Diego Zoo prohibits ticket resale, and membership passes require matching photo ID at the gate. Tickets sold on Craigslist, Facebook Marketplace, or eBay are frequently expired, already used, or completely fake. Buy only from the official zoo website, Costco, AAA, or authorized platforms like Go City San Diego."),
        ("What should I do if I receive a text about an unpaid San Diego parking ticket?",
         "Delete it immediately — it is a phishing scam. The City of San Diego does not send parking ticket notifications via text message. Do not click any links or scan QR codes. If you genuinely think you received a parking ticket, check at sandiego.gov/parking or call (619) 236-5444 to verify. Report the scam text to the city."),
    ],
    "Guadalajara": [
        ("Is Guadalajara safe for tourists in 2025-2026?",
         "Guadalajara is generally safe for tourists who stay in established neighborhoods like the Centro Historico, Chapultepec, and Tlaquepaque. The main risks are petty crime like pickpocketing and taxi scams rather than violent crime targeting visitors. Use ride-sharing apps, stay aware in crowded markets, and avoid walking alone in unfamiliar areas after dark."),
        ("Should I use taxis or Uber in Guadalajara?",
         "Uber and Didi are strongly recommended over street taxis. Both apps provide upfront pricing, GPS-tracked routes, and driver identification, eliminating the meter manipulation and overcharging scams common with some street taxis. If you must take a taxi, use only authorized sitio taxis from official stands and agree on the fare in pesos before getting in."),
        ("Is Mercado San Juan de Dios safe to visit?",
         "Yes, Mercado San Juan de Dios is safe and worth visiting, but you need to take precautions against pickpockets. Visit early in the morning when it is less crowded, wear a crossbody bag in front, carry only the cash you need, and be alert to distraction techniques. Many visitors report positive experiences when they take basic precautions."),
        ("What should I do if a police officer asks me for money on the street?",
         "Legitimate Mexican police never collect fines on the street — all fines must be paid at a police station. If someone claiming to be an officer demands cash, calmly ask for their badge number, say you want to call your consulate, and dial 911 to verify. Real officers will not object to verification. Fake officers will usually back off when you demonstrate knowledge of the system."),
        ("How much should I expect to pay for a taxi from Guadalajara airport?",
         "A taxi from GDL airport to the Centro Historico should cost approximately 250-350 pesos ($15-20 USD) using an authorized taxi with a pre-purchased voucher from the booth inside the terminal. Uber and Didi are also available and typically charge 150-250 pesos for the same route. Never accept a ride from someone soliciting you in the arrivals hall."),
    ],
    "Tulum": [
        ("Is Tulum safe for tourists in 2025-2026?",
         "Tulum is generally safe for tourists in the main tourist areas — Tulum Pueblo and the beach zone. The primary risks are financial scams such as taxi overcharging, police extortion, and beach club rip-offs rather than violent crime against visitors. Take standard precautions, avoid driving at night on isolated roads, and be aware of the specific scams common in the area."),
        ("How do I avoid taxi scams in Tulum?",
         "The best strategy is to avoid taxis when possible. Rent a bicycle for the Pueblo-to-beach route, use colectivo vans for longer distances along Highway 307, and pre-book airport transfers through your hotel. If you must take a taxi, ask your hotel for the correct fare, agree on the price in pesos before getting in, and have small bills ready to pay the exact amount."),
        ("Are the beach clubs in Tulum a rip-off?",
         "Some are. Many beach clubs charge $50-100 USD per person as a minimum spend, with overpriced drinks and food. However, all beaches in Mexico are legally public. You can access the beach by walking through any club to the waterline. For free beach access, try Playa Paraiso or the beach below the ruins. If you choose a beach club, ask for the menu and minimum spend before sitting down."),
        ("What should I do if police stop me and demand money in Tulum?",
         "Stay calm. Legitimate fines are never collected on the street or via portable card terminals. Ask for badge numbers, insist on going to the official police station to pay any fine, and call 911 to verify the officers. Recording the interaction on your phone is legal in Mexico and often deters corrupt officers. The state government has specifically ordered investigations into police extortion in Tulum."),
        ("How much should Tulum ruins tickets cost?",
         "The official total entry fee is approximately 515 MXN (about $28 USD), collected across three separate ticket booths: Jaguar Park entry (295 MXN), INAH archaeological zone (100 MXN), and CONANP conservation fee (120 MXN). Buy tickets only at the official booths at the entrance, not from anyone in the parking lot. Arrive at 8 AM to avoid crowds."),
    ],
    "Playa del Carmen": [
        ("Is Playa del Carmen safe for tourists?",
         "Playa del Carmen is generally safe in the main tourist areas including Fifth Avenue, the beach, and major resorts. The primary risks are financial scams like bill padding, timeshare pressure, and ATM skimming rather than violent crime against visitors. Exercise standard precautions, especially around the nightlife area on 12th Street after midnight."),
        ("How do I avoid the timeshare salespeople on Fifth Avenue?",
         "The most important step is to cover or remove your hotel wristband — promoters read the hotel name to fake familiarity. Beyond that, simply say 'No gracias' once and keep walking without slowing down. Do not explain, negotiate, or share any personal information. They will stop following after a few steps if you do not engage."),
        ("Is Fifth Avenue safe at night?",
         "Fifth Avenue itself is well-lit and heavily trafficked, making it relatively safe. The riskier areas are the side streets off Quinta Avenida and the 12th Street nightclub zone late at night. Travel in groups after midnight, avoid dark side streets, and do not engage with anyone offering drugs. Uber works in Playa del Carmen for safe rides back to your hotel."),
        ("Can restaurants legally add a mandatory tip to my bill in Playa del Carmen?",
         "No. Under Mexican consumer protection law (PROFECO), tips are strictly voluntary and restaurants cannot force you to pay one. If you find an automatic gratuity on your bill, you have the right to request it be removed. However, many tourists do not know this and pay it automatically. Always review your bill line by line before paying."),
        ("Where should I withdraw cash in Playa del Carmen?",
         "Only use ATMs inside physical bank branches such as BBVA, Santander, Scotiabank, or Banorte. The standalone ATMs on Fifth Avenue and in convenience stores are frequently compromised by skimming devices. Always cover the keypad when entering your PIN and select Mexican pesos when given a currency choice to avoid a 7-10 percent conversion markup."),
    ],
    "Cozumel": [
        ("Is Cozumel safe for cruise passengers?",
         "Cozumel is one of the safest destinations in Mexico and violent crime against tourists is extremely rare. The main risks are financial: taxi overcharging, fake jewelry, snorkel tour bait-and-switch, and aggressive timeshare sales. Stay in San Miguel and established beach clubs, book tours in advance, and verify prices before paying."),
        ("How much should a taxi cost in Cozumel?",
         "Official taxi rates are posted at the cruise piers. Common fares include approximately $8-12 USD from the International Pier to San Miguel, $12-18 to Playa Mia, and $20-25 to the southern beach clubs. Always confirm the total fare for all passengers and pay in pesos for the best rate. Photograph the rate chart at the pier for reference."),
        ("Is the jewelry sold at Cozumel cruise port real?",
         "Many items are not. Independent appraisals have revealed synthetic stones sold as natural gems, gold-filled chains sold as solid gold, and silver-plated base metals sold as sterling silver. Carnival Cruise Lines has officially stated they do not control port shops and cannot close them. If you buy jewelry, insist on a GIA appraisal certificate and pay with a credit card for dispute protection."),
        ("Should I buy medication at pharmacies in Cozumel?",
         "Only from legitimate first-class pharmacy chains like Farmacias del Ahorro. Tourist-area pharmacies near the cruise pier have been documented selling counterfeit or mislabeled medications. Never buy controlled substances or opioids — they are illegal in Mexico and may contain dangerous adulterants. Bring sufficient medication from home for your trip."),
        ("How do I avoid timeshare presentations in Cozumel?",
         "Say 'No gracias' once and keep walking. Never accept free tours, meals, or gifts — they always come with a multi-hour high-pressure sales pitch. Your limited port time in Cozumel is far more valuable than any freebie offered. Book your own excursions in advance and ignore all solicitors at the ferry terminal and pier exits."),
    ],
    "Oaxaca": [
        ("Is Oaxaca safe for tourists?",
         "Oaxaca is widely considered one of the safest tourist destinations in Mexico. Unlike many other Mexican cities, there are relatively few scams targeting tourists and violent crime against visitors is very rare. The main risks are taxi overcharging, market vendor pressure, and fake artisan crafts. Standard precautions are sufficient for a safe and enjoyable visit."),
        ("How can I tell if Oaxacan crafts are authentic?",
         "Visit artisan villages directly and watch the production process. Genuine hand-woven rugs show slight irregularities in the weave, natural dyes produce rich but varied colors, and true artisans can explain their techniques. Look for FONART certification labels and buy from cooperatives. If multiple identical pieces are available or the price seems too low, the item is likely mass-produced."),
        ("What is the best way to get to Monte Alban?",
         "The cheapest and most reliable option is the shared shuttle bus that departs frequently from Hotel Rivera del Angel on Calle Mina 518. Round-trip tickets cost approximately 80 pesos. If you take a taxi, agree on a round-trip fare of no more than 250-300 pesos and pay only half on arrival, with the rest upon return pickup."),
        ("Are mezcal tours worth it in Oaxaca?",
         "Absolutely, but quality varies enormously. Licensed operators like Mezcal Educational Tours and Oaxacking visit real artisan palenques where mezcal is actually produced. Avoid street-booked tours that spend most of the time in commission-paying retail shops. A good tour visits multiple production sites and costs $50-80 USD per person. Buy mezcal at Mercado Benito Juarez for the best prices."),
        ("Is it safe to exchange money on the street in Oaxaca?",
         "No. Street money exchangers are a well-documented scam. They offer attractive rates but shortchange you by switching bills during the rapid count. Only exchange money inside bank branches or official casas de cambio with a displayed license. For the best rates, use ATMs inside banks and always select Mexican pesos when prompted."),
    ],
    "Seattle": [
        ("Is Seattle safe for tourists?",
         "Seattle is generally safe for tourists, though property crime rates are above the national average. The main risks are car break-ins, phone theft, and street scams in specific downtown corridors. Violent crime targeting tourists is uncommon. Stay aware of your surroundings, avoid 3rd Avenue between Pike and Pine, and keep valuables secured."),
        ("What is the most common scam in Seattle?",
         "The tap-to-pay charity scam is currently the most financially damaging scam targeting Seattle visitors, with victims losing hundreds to thousands of dollars from a single tap. Street-level CD hustles and fake monk donation requests are the most frequently encountered lower-stakes scams near Pike Place Market and Seattle Center."),
        ("Is Pike Place Market safe?",
         "Pike Place Market is safe during operating hours with heavy foot traffic and vendor presence. The main risks are pickpocketing in crowded areas and CD/mixtape hustlers near the entrances. Keep your phone in a front pocket, don't accept items from strangers, and be aware that the surrounding streets can feel different from the market itself, especially after dark."),
        ("Are car break-ins really that common in Seattle?",
         "Yes — Seattle records over 12,000 car prowls annually, and rental cars are disproportionately targeted because thieves know tourists store valuables in them. Never leave anything visible in your vehicle, not even an empty bag or jacket. Place items in the trunk before arriving at your destination, not after parking where someone might see you stow them."),
        ("What is the safest way to get around Seattle?",
         "The Link Light Rail, Seattle Monorail, and rideshare apps (Uber, Lyft) are the safest transport options. The light rail connects the airport to downtown and Capitol Hill. For the Space Needle area, the Monorail from Westlake Center is convenient and avoids parking scam risks entirely."),
    ],
    "Nashville": [
        ("Is Nashville safe for tourists?",
         "Nashville is generally safe for tourists, especially in the main entertainment areas where there is heavy foot traffic and police visibility. The main risks are financial — overcharged bar tabs, fake parking tickets, and parking lot scams. Stay in groups after 10 PM on Broadway, use rideshare apps rather than accepting rides from strangers, and watch your drink at all times."),
        ("What is the most common scam in Nashville?",
         "Bar tab inflation on Lower Broadway is the most frequently reported tourist complaint — drinks can cost $15-25 each without prices being clearly posted. The fake parking ticket QR code scam and parking lot fundraiser drain are the most financially dangerous, as they can result in stolen credit card data or thousands in unauthorized charges."),
        ("Is Broadway in Nashville safe at night?",
         "Broadway is safe in terms of violent crime, with a strong police presence and constant foot traffic. The risks are mainly financial: overpriced drinks, aggressive touts pulling you into bars, and the chaos of the late-night crowd. Walk in groups, don't leave drinks unattended, and use rideshare apps with verified drivers for late-night transportation."),
        ("Are Nashville parking tickets real?",
         "Real Nashville parking tickets are issued by Metro Nashville and direct you to official .gov payment sites. If you find a ticket with a QR code directing you to a non-government website like metronashvilleparking.com, it is a scam. Verify any ticket by calling the MNPD non-emergency line at 615-862-8600 or visiting nashville.gov directly."),
        ("How do I avoid getting overcharged at Nashville bars?",
         "Ask for prices before ordering, pay cash per round instead of opening a tab, and check recent Google reviews before entering a bar. Walk one or two blocks off Lower Broadway for significantly better prices and atmosphere. Celebrity-branded bars on Broadway are generally the most expensive — local favorites off the main strip offer better value."),
    ],
    "Panama City": [
        ("Is Panama City safe for tourists?",
         "Panama City is moderately safe for tourists who take standard precautions. The main tourist areas — Casco Viejo during the day, the banking district, and the Amador Causeway — have visible police presence. The primary risks are taxi overcharging, pickpocketing in Casco Viejo, and ATM-related crime. Avoid walking alone in Calidonia, El Chorrillo, and Curundú neighborhoods."),
        ("What is the most common scam in Panama City?",
         "Taxi fare gouging is the most common and unavoidable tourist annoyance since Panama City taxis have no meters. Drivers routinely double or triple the fare for obvious tourists. The most effective countermeasure is using Uber or InDriver, which provide transparent pricing and tracked routes."),
        ("Is Casco Viejo safe to visit?",
         "Casco Viejo is safe to visit during daylight hours when there is tourist and police presence. It is the most popular historical area in Panama City and well-patrolled. However, it borders the El Chorrillo neighborhood which is unsafe, and the narrow streets become riskier after dark. Visit during the day, keep valuables secured, and take Uber back to your hotel after dinner."),
        ("Can I use Uber in Panama City?",
         "Yes — Uber operates fully in Panama City and is generally the safest and most reliable transport option. InDriver is a popular alternative that lets you propose your own fare. Both apps provide GPS-tracked routes, driver identification, and digital payment records. They are strongly recommended over street taxis."),
        ("What should I do if I'm a victim of crime in Panama City?",
         "Call 911 for emergencies or 104 for police. Contact the Tourist Police at 511-9260. File a police report at the nearest station for insurance purposes. US citizens should contact the US Embassy at +507-317-5000. If your credit card was compromised, call your bank immediately to freeze the card."),
    ],
    "Bogota": [
        ("Is Bogota safe for tourists?",
         "Bogotá requires more caution than most tourist cities but is visited safely by millions each year. The main risks are phone snatching, pickpocketing, drink spiking with scopolamine, and express taxi kidnapping. Stay in well-trafficked areas during the day, use ride-hailing apps exclusively, don't flash valuables, and exercise extreme caution in nightlife settings. La Candelaria is safe during daylight with police presence but risky after dark."),
        ("What is scopolamine and how dangerous is it?",
         "Scopolamine (called burundanga locally or 'devil's breath') is an odorless, tasteless drug that causes memory loss and makes victims highly suggestible. It can be slipped into drinks, food, or even applied to paper or business cards. Bogotá recorded over 1,400 cases in 2023. Victims typically lose consciousness and wake up hours later with no memory, having been robbed of all possessions. Never accept drinks from strangers and always watch your drink being prepared."),
        ("What does 'no dar papaya' mean?",
         "It's a Colombian expression meaning 'don't give papaya' — essentially, don't make yourself an easy target. This means not using your phone on the street, not wearing flashy jewelry or watches, keeping your bag secured in front of you, and not walking alone in quiet areas after dark. Colombians live by this principle daily, and tourists should adopt it immediately."),
        ("Is Uber safe to use in Bogota?",
         "Uber, DiDi, and InDriver are significantly safer than street taxis in Bogotá and are strongly recommended. They provide driver identification, GPS-tracked routes, and digital payment records. The risk of express kidnapping is virtually eliminated when using ride-hailing apps compared to hailing taxis on the street. Share your ride details with someone and verify the driver and vehicle match the app."),
        ("What should I do if I'm drugged or robbed in Bogota?",
         "Call 123 immediately for police and emergency services. Go to the nearest hospital if you suspect drugging. Contact the Tourist Police at +57 601 337 4413. US citizens should call the US Embassy at +(57)(1) 275-2000 or after-hours at +(57)(1) 275-4021. File a police report (denuncia) at the nearest CAI station for insurance claims. Cancel all cards and change banking passwords immediately."),
    ],
    "Mauritius": [
        ("Is Mauritius safe for tourists?",
         "Mauritius is one of the safest destinations in Africa with a low violent crime rate. Criminal cases decreased 16% from 2023 to 2024. Most tourist-related issues involve non-violent scams like overcharging, fake excursion operators, and beach vendor pressure. Stay alert in crowded areas like Port Louis Central Market and always use official taxis."),
        ("How do I avoid taxi scams at the Mauritius airport?",
         "Use the pre-paid taxi desk inside SSR International Airport terminal where fares are fixed by destination. Official taxis are white with white plates, a rooftop sign, and yellow door stickers. Alternatively, pre-arrange airport transfers through your hotel. Never get into an unmarked vehicle with a driver who approaches you in the arrivals hall."),
        ("Is it safe to buy excursions from beach vendors in Mauritius?",
         "No. The UK Foreign Office explicitly warns against buying from beach vendors. Multiple documented fraud cases involve operators taking advance payment and disappearing. Always book through your hotel, a licensed operator with a physical office, or platforms like Viator. Verify licenses with the Mauritius Tourism Promotion Authority."),
        ("What should I know about bargaining at Port Louis Central Market?",
         "Vendors routinely quote prices 3-5 times the local rate for tourists. Walk the entire market first to compare prices, start negotiations at 30-40% of the quoted price, and be prepared to walk away. Buy spices from shops with certified scales and visible price tags. Pickpocketing is also a risk in the crowded aisles."),
        ("Are there areas to avoid in Mauritius?",
         "Mauritius has no major no-go zones for tourists, but exercise extra caution in Port Louis city center after dark, particularly around the Central Market and bus station area. Avoid walking alone on unlit beaches at night. Stick to well-traveled routes and tourist areas, especially in the evening."),
    ],
    "San Salvador": [
        ("Is El Salvador safe for tourists in 2025?",
         "El Salvador has transformed dramatically under President Bukele's state of exception. The country is now statistically safer than many US cities, with gang violence reduced by over 90%. However, tourist-targeting crimes like phone snatching, express robbery, ATM skimming, and scams still occur. Stay in tourist areas, use organized transport, and avoid displaying valuables."),
        ("Is Bitcoin Beach (El Zonte) safe to visit?",
         "El Zonte is generally considered quite safe with a relaxed surf-town atmosphere. The biggest risk is petty theft — don't leave phones on beach towels. Be cautious with cryptocurrency transactions: never let strangers handle your phone or wallet app, carry backup USD cash, and verify QR codes are displayed by the actual business."),
        ("Should I use Bitcoin or USD in El Salvador?",
         "While Bitcoin is legal tender, USD cash is far more practical and safer for tourists. Most places accept dollars, and using cash avoids digital scam risks. If you want to try Bitcoin, keep small amounts in your wallet and understand transaction fees. Many vendors still prefer cash, especially smaller businesses and market stalls."),
        ("What areas should I avoid in San Salvador?",
         "Avoid neighborhoods outside the main tourist and commercial zones, particularly after dark. Stick to areas like Zona Rosa, Colonia Escalón, and Santa Elena for dining and nightlife. Avoid walking alone in Centro Histórico after dark, and do not venture into residential neighborhoods without a local guide. The areas around Metrocentro and Multiplaza malls are generally safe during daytime."),
        ("How do I get safely from the airport to San Salvador?",
         "Pre-arrange a hotel shuttle or use the Uber app. The road from the international airport to San Salvador is flagged by multiple government advisories as a robbery risk area, especially at night. Never accept rides from unofficial drivers. If possible, book flights that arrive during daylight hours."),
    ],
    "Montego Bay": [
        ("Is Montego Bay safe for tourists?",
         "Tourist areas in Montego Bay including the Hip Strip, resort zones, and major attractions are generally safe with increased security presence. However, venturing outside these areas, especially at night, carries significant risk. Stick to established tourist zones, use hotel-arranged transport, and avoid the neighborhoods of Flankers, Barrett Town, Glendevon, Rose Heights, and Mount Salem."),
        ("How aggressive are the vendors on the Hip Strip?",
         "Vendor harassment on Gloucester Avenue is the most common tourist complaint about Montego Bay. You will be approached repeatedly, sometimes physically grabbed or steered toward shops. A firm 'no thank you' without stopping or making eye contact is most effective. The vendors are generally not dangerous — the experience is more annoying than threatening — but it can be overwhelming for first-time visitors."),
        ("Can I leave my all-inclusive resort in Montego Bay?",
         "Yes, but with precautions. The Hip Strip and established attractions are safe during the day. Use hotel-arranged transportation, avoid walking alone after dark, and don't display expensive jewelry or electronics. Many resorts offer organized excursions that include transport — these are the safest way to explore outside the resort."),
        ("Is marijuana legal in Jamaica?",
         "Jamaica decriminalized possession of small amounts (under 2 ounces) in 2015, but buying from street sellers is still illegal. The only legal purchase point is licensed 'herb house' dispensaries. Street sellers are often part of entrapment scams where a fake police officer appears after the purchase and demands a cash bribe. Never buy from anyone on the beach or street."),
        ("How do I avoid getting overcharged for taxis in Montego Bay?",
         "Jamaica has no metered taxis, so all fares are negotiated. Always agree on the total fare for all passengers and luggage before getting in. Use official JUTA taxis from designated stands or pre-arrange transfers through your hotel. Ask the hotel front desk for typical fare amounts so you can negotiate from an informed position. Keep luggage in the backseat, not the trunk."),
    ],
    "Washington DC": [
        ("Is the National Mall safe to walk at night?",
         "The National Mall is patrolled by US Park Police 24/7 and is generally safe for evening walks near the well-lit memorials. However, the less-trafficked areas between monuments can be isolated after dark, so stick to lit pathways and visit popular memorials like the Lincoln and WWII memorials where other visitors are present."),
        ("Are the Metro stations safe for tourists?",
         "DC Metro stations are generally safe, especially during daytime hours. Metro Transit Police patrol stations, but tourists should remain alert for pickpockets during rush hour and large events. Avoid empty rail cars late at night and stay near other passengers."),
        ("Should I tip tour guides in Washington DC?",
         "For legitimate paid tours, a tip of 15-20% is customary. For free National Park Service ranger talks, tips are not expected or accepted. Never tip or pay someone who approaches you unsolicited offering a tour."),
        ("Is it safe to drive and park in downtown DC?",
         "Driving in DC is challenging due to traffic circles, restricted lanes, and aggressive parking enforcement. Street parking is expensive and confusing, and predatory towing is common. Consider using Metro instead, which reaches all major tourist sites."),
    ],
    "Antalya": [
        ("Is Antalya safe for solo female travelers?",
         "Antalya is generally safe for solo female travelers during the day in tourist areas like Kaleici and Lara Beach. However, exercise extra caution in the bar district at night, avoid accepting drinks from strangers, and be aware of the 'Let's Have a Drink' scam that specifically targets solo tourists. Dress modestly when visiting mosques and more conservative neighborhoods."),
        ("Should I use Turkish lira or euros in Antalya?",
         "Always use Turkish lira for the best exchange rates. While many tourist establishments accept euros, they set their own exchange rates which are typically 10-20% worse than the official rate. Withdraw lira from bank-branch ATMs for the best rates and avoid street money changers."),
        ("How much should a taxi from Antalya Airport cost?",
         "A metered taxi from Antalya Airport to Kaleici Old Town should cost approximately 350-500 TL, and to Lara Beach 250-400 TL (2025 prices). Always insist on the meter. Pre-booked hotel transfers are generally 20-30% more but remove all uncertainty and scam risk."),
        ("Is it safe to buy carpets in Antalya?",
         "Buying carpets can be safe if you use reputable, review-verified dealers and have any purchase independently appraised. Never buy from a shop you were led to by a street tout. Pay by credit card for dispute protection, and be extremely skeptical of claims about age, materials, or origin without independent certification. r/orientalrugs 'Help please. Ripped off? Kusadasi - Turkey' (comments/1o7f436, 2025) documents the cross-Aegean post-purchase value disputes — the same operator network operates in Antalya."),
        ("How do I book Antalya day trips to Pamukkale, Aspendos, or Side without scams?",
         "Use vetted operators only — r/Antalya 'Few days in Antalya - Best organized 1 day tours' (comments/1l96cn0, 2025) is the named 2025 community thread for vetted operators. Book via GetYourGuide or Viator with TÜRSAB Turkish Ministry of Culture licensing verified and 'no shopping stops' filter active at €30–€60 per person. AVOID hotel-concierge bookings under €25 — the math forces 'onyx workshop,' 'leather show,' or 'cooperative lunch' stops that consume hours of the day. r/Antalya 'Tourist little scams' frames the broader regional context. For Aspendos specifically (45 km east), the legitimate combo with Perge needs 7+ hours of attraction content; Aspendos hosts the Antalya Opera & Ballet Festival (June–September) for evening performances."),
    ],
    "Kusadasi": [
        ("Is Kuşadası safe for cruise passengers?",
         "Kuşadası is broadly safe — violent crime against tourists is very rare, and the cruise port has visible police presence. The practical risks are financial: r/Cruise 'Avoid the Ancient Coin scam' (comments/1qvm7tz, 2025) documents the named cruise-pier vendor scam selling fake Roman coins; r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024) documents the corral-into-back-room carpet sales mechanic on cruise excursions; r/kusadasi 'Scammed by this taxi driver' (comments/1m2wfds, 2025) documents a ₺1,400 port-to-hotel taxi overcharge for what should be ₺200; r/orientalrugs 'Help please. Ripped off? Kusadasi' (comments/1o7f436, 2025) documents post-purchase rug-value disputes. Save Tourism Police 155 and the Kuşadası Coastguard +90 256 614 1010."),
        ("What is the most common Kuşadası scam in 2025?",
         "Cruise-excursion forced carpet-shop stops top the list — r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024) is the canonical anchor: 'The private tours that end at a carpet tour are very awkward. They corral you into a room, close the doors, and a bunch of guys in tie' s start the high-pressure sale. Cruise-pier 'ancient coin' fake-antiquity sales are second most common per r/Cruise 'Avoid the Ancient Coin scam' (comments/1qvm7tz, 2025). Port-area taxi overcharges per r/kusadasi (comments/1m2wfds, 2025), Old Town Bazaar counterfeit 'brand-name' merchandise, restaurant tout-driven tourist-menu inflation, and off-brand independent excursion reseller fraud round out the top six."),
        ("How do I visit Ephesus from Kuşadası safely?",
         "Use Ephesus Shuttle (ephesusshuttle.com) — community-vetted operator with port-time guarantee, no-shopping-stops policy in writing, and small-group pricing of €40–€60 per person per r/Cruise 'Best excursions in Ephesus?' (comments/1oq4kz0, 2025). Avoid cruise-line excursions which cost 2x the price and routinely include a 60–90 minute carpet-shop stop. For independent visits, take the public dolmuş from Kuşadası to Ephesus (₺50, 30 min). Build a 90-minute return buffer before all-aboard time. Verify any private operator carries Turkish TÜRSAB Ministry of Culture licensing. Avoid online operators with no Google reviews, no TÜRSAB number, or no Turkish phone."),
        ("How do I avoid the cruise-day rug scam in Kuşadası?",
         "The cruise-line and unvetted private tour ecosystems are designed around delivering you to a carpet shop for a 30–40% commission to the operator. r/CarnivalCruiseFans '13 day Mediterranean quick review' (comments/1p0vbqu, 2025) frames the proud-escape narrative: 'Scammed our way out of the rug scam and got dropped off at the port to explore.' The defensive playbook: (1) when booking shore excursions, request 'no shopping stops, no carpet demonstration, no silk cooperative' in writing; (2) read the operator's Google reviews specifically searching for 'carpet' or 'shopping' to spot stop-adding patterns; (3) if your bus stops at a 'cultural cooperative' or 'silk demonstration,' stay on the bus and refuse to enter; (4) decline the apple tea — accepting starts the social-pressure script; (5) never sign a sale agreement at a tour stop; legitimate Turkish carpet purchases happen in vetted shops with cooling-off periods."),
        ("Where should I eat in Kuşadası without overcharging?",
         "Walk one block off Barbaros Caddesi (the tourist-tout strip) to find restaurants where Turkish residents eat. r/AskTurkey 'Kusadasi' (comments/1ms5ey5, 2025) gives the community recommendation flow. Honest-pricing venues: Ferah Restaurant (Atatürk Bulvarı, Aegean fish), Avlu (Cephane Sokak, traditional meze), Café Karavan (Old Town atmosphere), and the Holiday Inn restaurant for cruise-day reliability. Order from the menu with posted prices in Turkish or English; refuse complimentary bread/olives unless prices are confirmed; check the bill line-by-line and dispute any item not ordered. Avoid restaurants with touts on the sidewalk per r/AskTurkey 'What's a common scam in Turkey people should know' (comments/1qsrs8a, 2025): 'If a restaurant has a dude out front who comes up even before you look at the menu, keep walking.'"),
    ],
    "Ephesus": [
        ("Is Ephesus safe for tourists?",
         "Ephesus itself is broadly safe — Turkey's #2 most-visited site after Hagia Sophia, with strong site security and well-marked paths. The practical risks for older travelers are financial: fake 'skip-the-line' ticket reseller sites at €35–€60 for what costs €18 at the gate; mandatory carpet-shop stops on 'private' tours per r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024); on-site 'ancient Roman coin' vendor scams per r/Cruise 'Avoid the Ancient Coin scam' (comments/1qvm7tz, 2025); Selçuk Old Town carpet-shop basement pressure sales per r/solotravel 'I met a lot of creepy people while I was in Istanbul' (comments/yctw4z, 2024) where the same operator network operates regionally; House of the Virgin Mary tour bundle upsells; and Selçuk-to-Ephesus taxi overcharges. Save Tourism Police 155 and Selçuk Police +90 232 892 6021."),
        ("What is the most common Ephesus scam in 2025?",
         "Mandatory carpet-shop stops on private and cruise tours top the list. r/celebritycruises 'Ephesus tours' (comments/1f4mubo, 2024) describes the mechanic: 'The private tours that end at a carpet tour are very awkward. They corral you into a room, close the doors, and a bunch of guys in tie' s start the high-pressure sale. Fake 'skip-the-line' ticket reseller sites are second most common per r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) which documents the broader Turkish-attraction reseller pattern. On-site 'Roman coin' vendor scams per r/Cruise (comments/1qvm7tz, 2025), Selçuk basement carpet pressure sales, House of Virgin Mary bundled tour upsells, and Selçuk-to-Ephesus taxi overcharges round out the top six."),
        ("How do I buy genuine Ephesus tickets?",
         "Book Ephesus tickets only at the gate (cash or Turkish card) or via the official Müze app at muze.gov.tr — the only legitimate digital channel. Official prices: ₺700 (~€18) for the main site, ₺520 (~€13) for the Terrace Houses add-on. Licensed third-party resellers with buyer protection: GetYourGuide, Tiqets, and Viator (verify the listing's TÜRSAB Turkish Ministry of Culture operator number). Avoid Google ads for 'Ephesus tickets' which routinely lead to clone sites and resellers at 2–3x the price. Never book a ticket via WhatsApp or off-platform messaging from an unverified seller. The site rarely has queues except at the upper gate during cruise mornings, so 'skip-the-line' marketing is itself a red flag."),
        ("How do I book a private Ephesus tour without forced carpet stops?",
         "Use Ephesus Shuttle (ephesusshuttle.com) or Romeo's Place Tours — the two community-vetted operators with explicit no-shopping-stops policies in writing per r/Cruise 'Best excursions in Ephesus?' (comments/1oq4kz0, 2025). Pricing is €40–€60 per person for small-group tours. Verify the operator carries Turkish TÜRSAB Ministry of Culture licensing. Confirm in writing what stops are included and excluded — the magic phrase is 'no carpet stops, no silk demonstrations, no cultural cooperatives.' Get the operator's mobile number for emergencies. Read the operator's recent Google and TripAdvisor reviews specifically searching for 'carpet' or 'shopping' to spot operators who add stops mid-tour. If your tour stops at a carpet shop anyway, stay on the bus and refuse to enter."),
        ("How do I get from Selçuk to Ephesus on a budget?",
         "The dolmuş (shared minibus) from Selçuk otogar (bus station) to Ephesus runs every 30 minutes and costs ₺25 per person — by far the cheapest and most overcharge-proof option. Hours: 8 AM to 6 PM. If you prefer a taxi, the legitimate metered fare from Selçuk centre to Ephesus's upper gate is ₺200–₺300 (€5–€8); to the lower gate ₺150–₺200. Decline hotel-arranged 'private transfers' quoted over ₺500 — same trip on the meter. For the return ride from Ephesus, walk 35 minutes downhill on a flat path to Selçuk OR take the dolmuş that loops back. Avoid taxis hailed at the Ephesus lower gate carpark — many are unlicensed and quote inflated 'fixed prices.' Use BiTaksi app if you must hail a taxi."),
    ],
    "Pamukkale": [
        ("Is Pamukkale safe for tourists?",
         "Pamukkale is broadly safe — violent crime against tourists is essentially nonexistent. The practical risks are financial: r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) is the canonical 2025 named anchor for the north-gate ticket-booth bundling scam where cashiers refuse the ₺1,200 (~€30) basic ticket and force €60–€75 packages. r/Turkey 'Headphone scam Pamukkale' (comments/1fjcgk3, 2024) documents the audio-guide bait-and-switch. Day-trip tour bundling with shopping stops, Cleopatra Pool add-on upsells, hot-air balloon operator pricing variance, and Denizli-to-Pamukkale taxi overcharges round out the top six. r/Turkey 'Turkey trip report February 2025' (comments/1ixwq20, 2025) confirms the 2025 escalation. Save Pamukkale Tourism Office (+90 258 272 2077) and Tourism Police 155."),
        ("What is the most common Pamukkale scam in 2025?",
         "The north-gate ticket-booth bundling scam tops the list — r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025) is the named 2025 anchor: cashiers refuse to sell the basic ₺1,200 (~€30) entry ticket and insist on a 'mandatory' €60–€75 combo with Antique Pool, Laodicea, museum, and audio guide bundled. r/Turkey 'Turkey trip report February 2025' (comments/1ixwq20, 2025) confirms €40 bundled tickets being sold by default. Day-trip tour bundling with shopping stops is second most common (any tour priced under €30 from Antalya/Bodrum/Marmaris forces 2–3 'cooperative' stops). Audio-guide rental bait-and-switch, Cleopatra Pool add-on upsells, hot-air balloon operator pricing variance, and Denizli-to-Pamukkale taxi overcharges round out the top six."),
        ("How do I buy genuine Pamukkale tickets?",
         "Book Pamukkale + Hierapolis tickets in advance via the official Müze app at muze.gov.tr — official adult rate is ₺1,200 (~€30) covering both the travertines and Hierapolis archaeological site. Having the digital ticket bypasses the gate booth's bundling pressure entirely. If buying at the gate, insist firmly on the basic ticket and refuse 'mandatory' add-ons — they are not mandatory per Turkish Ministry of Culture rules. Pay with credit card and photograph the terminal screen showing the amount before approving — r/istanbul_tips 'Don't get scammed at Hagia Sophia' (comments/1sdtbmf, 2025) documents the calculator-trick variant where one price is shown and a higher amount is charged. The Cleopatra Antique Pool inside the site is a separate ₺240 (~€6) entry — confirm the price at the booth and skip if mobility is a concern (rocky uneven entry steps)."),
        ("How do I get to Pamukkale from Antalya, Bodrum, or Marmaris?",
         "Three options ranked by quality: (1) BEST: Overnight in Pamukkale village (€30–€60/night hotels with sunrise/sunset travertine access when day-trippers are absent); (2) GOOD: Hire a private driver from Antalya (€150–€250 round-trip for a private car) — bypasses tour-bundle shopping stops; (3) AVOID: Tour-operator day trips under €30 per person — the math forces 2–3 shopping stops at onyx workshops, leather shows, and 'cooperative' lunches per r/travel 'Pamukkale, Türkiye Scam' (comments/1r10ie1, 2025). For tours €40–€80, demand 'no shopping stops, no demonstrations, no cooperative lunches' in writing before paying any deposit. From Selçuk/Kuşadası, the train + bus combination via Denizli is comfortable and scam-free. From Denizli otogar, take the public dolmuş to Pamukkale (₺25, every 15–30 min)."),
        ("Are Pamukkale hot-air balloons safe?",
         "Yes, with a vetted operator. Pamukkale is the second-largest hot-air-balloon market in Turkey after Cappadocia. Book directly with named operators: Pamukkale Balloons (pamukkaleballoons.com), Sky Pamukkale, or Royal Balloon at €120–€180 per person for a 60–75 minute sunrise flight. Verify the operator's Turkish DGCA SHGM licensing number on their website or by request. Anything under €100 per person signals an unlicensed operator with skipped maintenance schedules and pilots without proper tandem licensing — the safety stakes matter and the worst incidents in Turkey have involved unlicensed operators. For older travelers with mobility concerns, the basket steps are 1.2 m high and the landing is rough — discuss with the operator and ask for a basket with a low-step entry. Check weather conditions the night before; legitimate operators automatically reschedule for high-wind days."),
    ],
    "Fethiye": [
        ("Is Fethiye safe for tourists?",
         "Fethiye is broadly safe but has Turkey's most-documented Old Town vendor-scam ecosystem. r/travel 'My experience in Türkiye: beware of vendors' (comments/1n2jk3z, 2025) is the canonical 2025 named anchor — it documents an actual physical assault in a Turkish Delight store in Fethiye's Old Town: 'I did get physically assaulted in a Turkish Delight store in the middle of Fethiye's busy Old Town market.' Other practical risks: Ölüdeniz tandem paragliding operator safety variance per r/freeflight 'WARNING: Potential scam company in Oludeniz' (comments/1ookhl3, 2025); 12 Islands boat tour bundling and hidden charges; Tuesday Market and Old Town tourist-menu price inflation per r/travel 'Leaving Türkiye heartbroken' (comments/1epj1jn, 2024); Dalaman Airport (DLM) transfer overcharges; and Hisarönü resort-strip 'authentic Turkish bath' hammam upsells. Save Tourism Police 155 and Fethiye Belediyesi Tourism Office +90 252 614 1527."),
        ("What is the most common Fethiye scam in 2025?",
         "Old Town Turkish Delight 'welcome juice' traps top the list — r/travel 'My experience in Türkiye: beware of vendors' (comments/1n2jk3z, 2025) documents the named 2025 physical-assault anchor in a Fethiye lokum shop. The pattern: vendor pounces on entry, offers free tasting, assembles a box without asking, presents bill of €40–€80 for what should be €5. When victims refuse, vendors escalate to physical force. Ölüdeniz paragliding operator scams are second most common per r/freeflight (comments/1ookhl3, 2025) — unlicensed operators sell €60–€80 'special tandem flights' that turn out to be 8–10 minute Faralya launches instead of the promised 30+ minute Babadağ summit flights. 12 Islands boat tour hidden charges, Tuesday Market tourist-menu inflation, Dalaman Airport transfer overcharges, and Hisarönü hammam upsells round out the top six."),
        ("How do I avoid the Fethiye Old Town vendor assault scam?",
         "DO NOT enter Turkish Delight, tea, or spice shops in Fethiye Old Town tourist-strip zones. r/travel 'My experience in Türkiye: beware of vendors' (comments/1n2jk3z, 2025) is the canonical 2025 named anchor documenting a physical assault when a tourist tried to leave a lokum shop. The defensive playbook: (1) buy lokum at Migros (€2–€5/box), Hafiz Mustafa (heritage chain with posted prices, €8–€15), or Saray Muhallebicisi — never at tourist-strip Old Town vendor shops; (2) decline 'welcome juice' and 'free tasting' offers — accepting begins the social-debt mechanic; (3) NEVER let a vendor assemble a box for you 'just to show you' — the box becomes the demanded purchase; (4) if pressured, say loudly 'I am not buying — I am leaving' and walk to the door; if the vendor blocks you, immediately call Tourism Police 155; (5) report the shop to Fethiye Belediyesi Tourism Office and leave a 1-star Google review naming the venue. r/europe 'Turkey in panic as British holidaymakers abandon country' (comments/1fxi9wd, 2024) confirms the pattern is documented across Turkish tourist zones."),
        ("How do I book Ölüdeniz paragliding safely?",
         "Book directly with vetted operators: Sky Sports Turkey (skysports-turkey.com), Reaction Paragliding (reactionparagliding.com), Easy Riders, or Babadağ Paragliding. Pay €110–€160 per person — anything under €100 signals an unlicensed operator. r/freeflight 'WARNING: Potential scam company in Oludeniz' (comments/1ookhl3, 2025) is the named 2025 paragliding-community anchor warning about flagged unlicensed operators. Verify the pilot has Turkish DGCA SHGM tandem licensing (operators should show this on request). The standard flight is 30+ minutes from the Babadağ summit (1,969 m); if quoted shorter, you're being sold the cheap Faralya launch. Check weather the morning of — most operators automatically reschedule for high-wind days, but unlicensed operators sometimes fly in unsafe conditions to avoid refunds. For older travelers (suitable up to ~85 kg without back/neck/heart issues), the takeoff run is 5–10 paces downhill and landing is on the beach with assistance — discuss specific physical concerns with the operator before booking."),
        ("How do I get from Dalaman Airport (DLM) to Fethiye safely?",
         "Most package-tour operators (TUI, Jet2, easyJet Holidays, Thomas Cook successors) include free coach transfer from DLM to your hotel — confirm this BEFORE arrival and wait at the designated meeting point. For independent travelers, book a private transfer in advance via Welcome Pickups (€30–€40 per car for up to 4 people) — vetted operators with fixed prices and no taxi-rank pressure. If taking a metered taxi, the legitimate fare from DLM to Fethiye (50 km) is ₺900–₺1,200 (€23–€30) on Tarife 1 (day rate); to Ölüdeniz (60 km) ₺1,100–₺1,400. Refuse 'fixed price' quotes over €50 — these are overcharges. The Havaş airport bus serves Fethiye otogar at €8 per person (1 hr) for luggage-light travelers. Uber does NOT operate in Dalaman; only BiTaksi and licensed taxis are legitimate. For late-night Hisarönü return rides from nightlife, pre-book through your hotel reception rather than hailing on the street."),
    ],
    "Alanya": [
        ("Is Alanya safe for tourists?",
         "Alanya is broadly safe for older package-holiday travelers — violent crime is rare and resort areas are well-policed. The practical risks are financial: r/Alanya 'Be aware of this scam' documents the Bar Street card-skimming pattern where 'friendly locals' steer tourists to flagged bars and €800–€2,500 unauthorised charges land within hours. r/Alanya 'Just got back from alanya' documents Cleopatra Beach taxi overcharges. r/Alanya 'What has happened with the prices around Alanya?' captures the 2024–2025 restaurant inflation. r/Alanya 'Question about excursion reps/travel agency reps' documents commission-driven hotel-concierge tour reseller patterns. AYT/GZP airport transfer overcharges, Damlataş Cave/Castle skip-the-line touts, and bazaar counterfeit pressure round out the top six. Save Tourism Police 155 and Alanya Belediyesi Tourism Office +90 242 519 4321."),
        ("What is the most common Alanya scam in 2025?",
         "Bar Street card-skimming tops the list — r/Alanya 'Be aware of this scam,' 'Warning,' and 'Why did this creepy guy approach me for?' all document the same social-engineering pattern: fluent-English 'friendly local' steers solo male tourists to a bar, drinks ordered, card terminal brought to the table, multiple 'didn't go through' retries during which the card data is captured for unauthorised follow-up charges. r/Alanya 'Questions about Alanya' (2025) confirms the 2025 escalation. Cleopatra Beach taxi overcharges are second most common per r/Alanya 'Just got back from alanya' — drivers refuse the meter and quote ₺500–₺800 for a ₺140–₺200 trip. Restaurant tourist-menu inflation, AYT/GZP airport transfer overcharges, hotel-concierge excursion reseller markups, and Damlataş Cave/Castle skip-the-line touts round out the top six."),
        ("How do I get from Antalya Airport (AYT) to Alanya safely?",
         "AYT is 130 km west of Alanya — most package-tour operators (TUI, Jet2, easyJet Holidays, Tez Tour, Anex Tour) include free coach transfer; confirm this BEFORE arrival and wait at the designated meeting point. For independent travelers, the Havaş airport bus serves Alanya otogar at ₺250 per person (~€6.50, 2.5 hr) — the budget-friendly option. If taking a metered taxi, confirm the ₺2,000–₺2,500 (€50–€63) range upfront and insist on Tarife 1 (day rate). Refuse 'fixed price' quotes over €100. Book Welcome Pickups in advance for AYT-to-Alanya (€60–€80 per car for up to 4 people) — vetted operators with fixed prices. From Gazipaşa-Alanya Airport (GZP, 40 km east), the metered taxi fare to central Alanya is ₺600–₺900 (€15–€22); refuse fixed quotes over €30. Uber does NOT operate in Alanya; only BiTaksi and licensed taxis are legitimate."),
        ("How do I avoid the Alanya Bar Street card-skimming scam?",
         "r/Alanya 'Be aware of this scam' documents the named pattern: a fluent-English 'friendly local' approaches you on Bar Street (Damlataş Caddesi) and invites you to a 'nice bar nearby.' You buy four drinks. The card terminal is brought to your table. The waiter taps the screen multiple times saying 'didn't go through.' By morning, your card has €800–€2,500 in additional charges to bars you never entered. The defensive playbook: (1) NEVER follow an unsolicited 'friendly local' to a bar you haven't chosen yourself; (2) at any bar, pay cash for drinks (small bills only — never ₺500 notes); (3) if you must pay by card, watch the terminal stay at your table and refuse 'didn't go through, let me try again' retries; (4) photograph the amount on any signed paper receipt BEFORE signing; (5) check your bank app immediately after each transaction; (6) if you suspect skimming, freeze the card via your bank app within 60 seconds; (7) report the venue to Tourism Police 155 with venue name and address."),
        ("Where should I eat in Alanya without getting overcharged?",
         "Walk one block off Bar Street and the Cleopatra Beach strip to find restaurants where Turkish residents eat. r/Alanya 'What has happened with the prices around Alanya?' documents the 2024–2025 inflation: 'Prices have actually tripled or even quadrupled over the last 2 years' in tourist zones. Community-recommended honest-pricing venues: Köşem Restaurant (Atatürk Caddesi, Turkish home cooking), Sofra (Old Town, regional specialties), Mahmutlar Manti House (Mahmutlar, posted prices), Iskele Sofrası (harbor area, fish). Order from Turkish-language menus or chalkboards (not English-only photo menus). For fish, ask to see the fish before ordering AND have it weighed in your presence; get the per-kg price IN WRITING. Refuse complimentary bread/olives unless prices are confirmed. Check the bill line-by-line against the menu and dispute any item not ordered. Bargaining 30–40% off the first quote is reasonable in tourist-tier shops per r/AskTurkey 'READ THIS if you're planning to visit Turkey' (comments/1jqcxqp, 2025)."),
    ],
    "Side": [
        ("Is Side safe for tourists?",
         "Side is broadly safe — the small Old Town peninsula is well-policed and the ancient ruins are integrated into the modern village. The practical risks are financial: r/Antalya 'Bought this at the manavgat market what is this?' documents the Manavgat Bazaar fake-product ecosystem; r/Antalya 'Eating out in Side/Manavgat' frames the harbor-strip restaurant overcharge pattern; r/Antalya 'Few days in Antalya - Best organized 1 day tours' (comments/1l96cn0, 2025) covers the Aspendos/Perge bundle-tour shopping-stop pattern. Photographer touts at the Apollo Temple sunset, hotel-concierge excursion markups, hammam upsells, and bazaar counterfeit pressure round out the top six. Save Tourism Police 155 and Manavgat Belediyesi Tourism +90 242 753 1004."),
        ("What is the most common Side scam in 2025?",
         "Hotel-concierge excursion reseller markups top the list — r/Antalya 'Few days in Antalya - Best organized 1 day tours' (comments/1l96cn0, 2025) documents the structural problem: legitimate vetted operators sell Aspendos + Perge + Side combos at €40–€60/person via TÜRSAB-licensed small-group tours, but hotel-concierge bookings under €25 force 2–3 'cooperative' shopping stops (onyx, leather, carpets) that consume the bulk of the day. Manavgat Bazaar fake-product sales (saffron, spices, herbs) are second most common per r/Antalya 'Bought this at the manavgat market what is this?' Restaurant tourist-menu inflation on Liman Caddesi, Apollo Temple photographer touts demanding €15–€25 after-the-fact, hammam resort-bundle upsells, and bazaar counterfeit brand pressure round out the top six."),
        ("How do I visit Side Ancient City safely?",
         "Side's Apollo Temple ruins, Theatre approach, and Agora are FREE — they're integrated into the modern Old Town pedestrianized zone. Walk via the main street to the peninsula tip for sunset (one of the Mediterranean's iconic views). Decline ALL 'professional photographer' offers — modern phone cameras handle the sunset, the location is well-marked, and photographers demand €15–€25 after taking the shot. Decline 'guided tour' offers of the free ancient city — every signpost has English/Turkish/German interpretation. The Side Museum (₺120 / ~€3) is genuinely interesting for a 30-minute visit and is the only fee-paying attraction worth your money. The Side Theatre (₺240) is the second legitimate paid attraction — visit at sunset for atmosphere. NEVER buy 'archaeological fragments,' 'authentic ancient stones,' or 'Roman coins' from any vendor — these are either fake (and worthless) or genuine (and a Turkish criminal-export issue under Law 2863 on Cultural Heritage)."),
        ("How do I do a Manavgat Waterfall + boat trip without overcharging?",
         "Book the Manavgat combo via GetYourGuide or Viator with the 'no shopping stops' filter active at €20–€30 per person — the legitimate small-group price. Avoid hotel-concierge bookings under €15 — the math forces 2+ hours at Manavgat Bazaar shopping stops where every stall pays the operator commission. r/Antalya 'Bought this at the manavgat market what is this?' documents the bazaar fake-product ecosystem: 'These are some tourist scam products that local people never ever use, even ever heard. It could be some suga' r-bag or chemical compound mislabeled as 'authentic Turkish craft.' If you want to see Manavgat Bazaar independently, take the public dolmuş from Side to Manavgat (₺25, 15 min) and visit for 30 minutes. Confirm boat trip duration is 1.5–2 hours with multiple river stops; if quoted 30–45 min, you got the cheap version. NEVER buy 'authentic saffron,' 'special spices,' or 'medicinal herbs' from Manavgat Bazaar vendors — these are mostly mislabeled chemical compounds."),
        ("Should I do an Aspendos + Perge day-tour from Side?",
         "Yes — Aspendos (best-preserved Roman theatre in the Mediterranean) and Perge (large city ruins) are both worth the day; the question is which operator. Book via GetYourGuide or Viator with TÜRSAB Turkish Ministry of Culture licensing verified and 'no shopping stops' filter active at €40–€60 per person. r/Antalya 'Few days in Antalya - Best organized 1 day tours' (comments/1l96cn0, 2025) is the named 2025 vetted-operator thread. Avoid hotel-concierge bookings under €25 — the math forces 'onyx workshop,' 'leather show,' or 'cooperative lunch' stops that consume hours of the day. Real combo content needs 7+ hours: Aspendos 90 min, Perge 60–90 min, Side time, lunch, transit. For older travelers with mobility concerns, ask whether the operator provides shaded seating at Aspendos (the amphitheatre has minimal natural shade and the climb to the upper rows is steep). Aspendos hosts the annual Antalya Opera & Ballet Festival (June–September) — evening performances are stunning if your trip aligns. As a private alternative, hire a driver via Welcome Pickups (€100–€150 round-trip from Side for up to 4 people)."),
    ],
    "Izmir": [
        ("Is Izmir safe for tourists?",
         "Izmir is broadly safe — Turkey's third-largest city is comfortable, walkable, and less aggressive on tourist scams than Istanbul or the resort coasts. The practical risks are financial: ADB airport taxi overcharges per r/Izmir 'Help a tourist get from ADB to izmir city center'; Kemeraltı Bazaar carpet/jewelry pressure (r/Turkey 'Turkey trip report February 2025: Multiple scams' (comments/1ixwq20, 2025) documents a $250 victim); Konak/Alsancak restaurant tourist-menu inflation; Izmir real-estate fake-listing fraud per r/Izmir 'About buying a house' and 'A guy from İzmir is committing fraud worldwide'; Alsancak nightlife card-skimming (cross-pattern with Alanya); and Çeşme/Alaçatı transfer markups. Save Tourism Police 155 and İzmir Emniyet Müdürlüğü +90 232 463 1500."),
        ("What is the most common Izmir scam in 2025?",
         "Kemeraltı Bazaar carpet and jewelry pressure tops the list — r/Turkey 'Turkey trip report February 2025: Multiple scams' (comments/1ixwq20, 2025) is the named 2025 anchor: '$250 dollars (6000 lira approx.)' lost to a Kemeraltı vendor's carpet pitch. ADB airport taxi overcharges are second most common — drivers refuse the meter and quote €30–€60 for the 18-km Izmir centre trip that should be ₺350–₺500 (€9–€13). Konak/Alsancak restaurant tourist-menu inflation, Izmir Idealista/sahibinden.com fake-listing apartment fraud, Alsancak nightlife card-skimming, and Çeşme/Alaçatı hotel-concierge transfer markups round out the top six."),
        ("How do I get from Izmir Airport (ADB) to the city safely?",
         "Use the Izban suburban train from ADB to Alsancak — ₺25 (~€0.65), 30 min, runs 4 AM to 11 PM. This is the cheapest and most overcharge-proof option for older travelers. Alternative: Havaş airport bus to Konak Square at ₺250 (~€6.50) in 35 min for luggage-light travelers. If using a metered taxi, insist on Tarife 1 (day rate) and confirm the ₺350–₺500 (€9–€13) range to Konak/Alsancak before boarding. Install Marti TAG (Izmir-specific ride-hailing app) and BiTaksi (Turkey-wide app) BEFORE arrival for app-regulated fares with digital receipts per r/Izmir 'Help a tourist get from ADB to izmir city center.' Uber operates in Izmir centre but not at ADB or in Çeşme/Alaçatı. For Çeşme transfers, take the Havaş bus from ADB at €10 per person in 70 min — far cheaper than the €120+ hotel-concierge 'private transfer' packages."),
        ("How do I avoid the Kemeraltı Bazaar carpet scam in Izmir?",
         "r/Turkey 'Turkey trip report February 2025: Multiple scams' (comments/1ixwq20, 2025) documents a $250 victim at a Kemeraltı carpet shop — the same corral-into-back-room mechanic that operates in Kuşadası, Selçuk, and Istanbul. The defensive playbook: (1) AVOID Kemeraltı carpet, jewelry, and 'authentic Turkish' shops without prior vetting via Turkish Carpet Trade Association; (2) the legitimate Kemeraltı residential market for textiles, food, and small souvenirs is fine — pay marked prices and bargain 30–40% on unmarked items; (3) for genuine Turkish gold, visit Konak Kuyumcular Çarşısı (gold quarter) where prices are tied to international gold-spot rates; (4) NEVER enter a shop's back room or 'private viewing area' for any merchandise; (5) decline 'welcome juice' and 'free tea' offers that begin the social-debt mechanic; (6) carry only enough cash for small souvenirs; lock major valuables in hotel safe; (7) ignore post-visit WhatsApp or hotel-call follow-up — these are operator pressure tactics."),
        ("How do I day-trip from Izmir to Çeşme or Alaçatı affordably?",
         "Three options ranked: (1) BEST budget: Eshot bus from Üçkuyular bus terminal (Izmir centre) to Çeşme — ₺45 per person (~€1.10), 90 min; (2) FROM AIRPORT: Havaş bus from ADB direct to Çeşme — €10 per person, 70 min; (3) MID-RANGE: Marti TAG or BiTaksi metered round-trip taxi from Izmir centre — €100–€140 round-trip per r/Izmir 'Alaçatı tatili, kiralık araba mı, taxi mi?' baseline. AVOID hotel-concierge 'private transfer' packages over €120 round-trip. For multi-day Çeşme/Alaçatı stays, rent a car at ADB with vetted operators (Cicar, Hertz, Europcar) at €40–€60/day plus fuel — apply the rental-car video-walk-around discipline from the Spain library to avoid post-return damage claims. Uber does not operate on the Çeşme route."),
    ],
    "Konya": [
        ("Is Konya safe for tourists?",
         "Konya is one of Turkey's safest tourist cities — violent crime against visitors is essentially nonexistent, and the city's pilgrimage character (Rumi's tomb, Mevlevi Order centre) creates a genuinely respectful atmosphere. The practical risks are financial: hotel-concierge 'authentic Konya Sema' tour resellers from Cappadocia/Istanbul that charge €40–€80 for what is FREE per r/istanbul 'Is Dervish whirling show worth it?'; Mevlana Museum photographer/tout pressure at the entrance; Konya restaurant 'KDV ek' (illegal extra VAT) on bills per r/istanbul 'Did I get scammed?'; YHT station taxi overcharges; Cappadocia-Konya day-tour bundle reseller markups; and tourist-strip sweet shop 'tasting' pressure. Save Tourism Police 155 and Konya İl Emniyet Müdürlüğü +90 332 322 0888."),
        ("What is the most common Konya scam in 2025?",
         "Hotel-concierge 'authentic Konya Sema' tour resellers from Cappadocia and Istanbul top the list — r/istanbul 'Is Dervish whirling show worth it?' confirms the genuine 7 PM Saturday Sema at Mevlana Kültür Merkezi is FREE; commercial 'whirling dervish dinner shows' at Istanbul/Cappadocia tourist venues are not the religious ceremony. Mevlana Museum photographer touts at the entrance demanding €10–€25 after-the-fact are second most common. Konya restaurant 'KDV ek' (illegal extra VAT charges on top of menu prices), YHT station taxi 'fixed price' overcharges (₺500+ for ₺250–₺350 metered fare), Cappadocia-Konya day-tour bundles with shopping stops, and tourist-strip sweet/spice shop 'tasting' pressure round out the top six."),
        ("How do I attend the genuine Whirling Dervish Sema ceremony?",
         "The genuine Sema (Mevlevi religious ceremony) is held at Mevlana Kültür Merkezi (Aslanlı Kışla Caddesi 4, Konya) every SATURDAY at 7 PM. Entry is FREE — no tickets required. Arrive at 6 PM for seating (capacity ~700, fills quickly during summer). Dress modestly (covered shoulders, knees, no shorts). Photography permitted in some seasons but flash always prohibited. The ceremony lasts ~90 minutes and includes 4 'salaams' (movements) — silence and reverence expected. NEVER pay €40–€80 for hotel-arranged 'Konya Sema' tours from Cappadocia — these miss the actual Saturday ceremony or substitute commercial 'whirling dervish shows' that are not the religious ritual. For Istanbul-based travelers who cannot travel to Konya, the Galata Mevlevihanesi in Istanbul (Tunel area) holds monthly genuine Sema ceremonies with ₺200 entry. r/istanbul 'Is Dervish whirling show worth it?' confirms: 'I live in Konya and I regularly attend the ceremony but not to watch the dervishes to listen the mus' ic."),
        ("How do I visit the Mevlana Museum without paying tout fees?",
         "The Mevlana Museum (Rumi's tomb and former Mevlevi monastery) entry is FREE — walk in via the official entrance on Mevlana Caddesi. Visit takes 60–90 minutes. Decline ALL 'professional photographer' offers at the entrance — phones are permitted (no flash inside the tomb chamber), and photographer touts demand €10–€25 after taking the shot. For genuine Mevlevi memorabilia, buy at the official museum gift shop with marked prices (rosary €4–€8, books €5–€15, replica dervish hat €10–€20). Decline tout offers of 'authentic' items at the gate — these are mass-produced replicas at 3x the museum-shop price. Dress modestly: covered shoulders and knees, head-covering required for women in the tomb chamber (free shawls available at entrance). r/AskTurkey 'Konya - the hidden gem of Turkey, the land of Whirling' is the canonical community anchor for the genuine experience."),
        ("Should I do a Cappadocia-Konya day trip or overnight in Konya?",
         "For the Saturday Sema specifically, OVERNIGHT in Konya. The Pamukkale Turizm bus from Cappadocia (Nevşehir otogar) to Konya runs ₺350 each way and takes 9 hours — too long for a day-trip that needs to attend the 7 PM Saturday ceremony. Plan: arrive Friday evening, attend Sema Saturday 7 PM, depart Sunday morning. AVOID Cappadocia hotel-concierge 'Konya day-trip' packages under €60 per person — the math forces 30-min Museum visits, 60–90 minute carpet/onyx 'cooperative' shopping stops, and either no Sema attendance (weekday tours) or rushed entry. For €80–€120 small-group tours WITHOUT shopping stops, verify TÜRSAB licensing and 'no shopping stops' contract in writing. For older travelers preferring private comfort, hire a driver via Welcome Pickups for the Cappadocia-Konya day at €220–€320 round-trip for up to 4 people. Sultan Han Caravanserai (45 km east of Konya) is a stunning 13th-century Seljuk caravanserai worth a 30-min stop on driving routes."),
    ],
    "Hurghada": [
        ("Is it safe to swim and snorkel in the Red Sea from Hurghada?",
         "The Red Sea is generally safe for swimming and snorkeling at resort beaches and established dive sites. However, book through licensed operators with safety equipment, check weather conditions, and never snorkel alone. Avoid touching coral or marine life, and be aware that strong currents can develop quickly at certain sites."),
        ("How much should I tip in Hurghada?",
         "Tipping (baksheesh) is expected but should be proportional. Hotel housekeeping earns 20-50 EGP per day, restaurant tips are 10-15% if service charge is not included, and small tips of 10-20 EGP are customary for porters and helpful staff. Do not feel pressured into tipping for unsolicited services."),
        ("Is the tap water safe to drink in Hurghada?",
         "No, do not drink tap water in Hurghada. Drink only bottled water with an intact seal, and use bottled water for brushing teeth as well. Most hotels provide complimentary bottled water. Be cautious with ice in drinks outside resort areas."),
        ("Can I use US dollars or euros in Hurghada?",
         "While many tourist establishments accept USD and EUR, you will generally get better value using Egyptian pounds. Exchange money at official bank branches or licensed exchange offices for the best rates. Always clarify which currency a price is quoted in before agreeing to pay."),
    ],
    "Portland": [
        ("Is Portland safe to visit in 2025-2026?",
         "Portland has seen significant safety improvements, with violent crime down 17% and homicides down 51% recently. Popular tourist areas like the Pearl District, Hawthorne, Alberta Arts, and Division Street are generally safe during the day. Exercise normal urban precautions and avoid Old Town/Chinatown at night."),
        ("Is it true that Portland has a homeless problem?",
         "Portland does have visible homelessness, primarily in downtown and along the Burnside corridor. Most interactions are non-threatening, but some aggressive panhandling occurs. Tourists should not engage with anyone making them uncomfortable and should walk confidently through these areas during daylight hours."),
        ("Do I need a car to visit Portland?",
         "A car is useful for day trips to the coast or Columbia Gorge, but unnecessary for city exploration. TriMet's MAX light rail and bus system covers most tourist areas, and Portland is extremely walkable and bikeable. Not having a car eliminates the significant risk of vehicle break-ins."),
        ("Is Portland's tap water safe to drink?",
         "Portland has some of the best tap water in the United States, sourced from the protected Bull Run Watershed. Bring a reusable water bottle and enjoy the tap water freely at restaurants and hotels."),
    ],
    "Abu Dhabi": [
        ("Is Abu Dhabi safe for tourists?",
         "Abu Dhabi is consistently ranked among the safest cities in the world, with extremely low rates of violent crime. The main risks for tourists are financial scams like taxi overcharging, fake luxury goods, and rental fraud rather than personal safety threats. Exercise normal precautions and the vigilance you would in any major city."),
        ("Can I drink alcohol in Abu Dhabi?",
         "Alcohol is legal in Abu Dhabi but only in licensed venues such as hotel restaurants, bars, and clubs. Being intoxicated in public is a criminal offense. Tourists can purchase alcohol at licensed stores with a temporary tourist license. Never drink and drive, as the UAE has a zero-tolerance policy for alcohol and driving."),
        ("Do I need to dress conservatively in Abu Dhabi?",
         "While Abu Dhabi is more liberal than some other Gulf states, modest dress is expected in public, especially when visiting mosques and government buildings. At the Sheikh Zayed Grand Mosque, women must wear loose-fitting clothing covering arms and legs, and a headscarf. Beach and pool attire is acceptable at resorts and beach clubs."),
        ("How much does a taxi cost in Abu Dhabi?",
         "Official Abu Dhabi taxis use meters with a base fare of 5 AED, minimum fare of 12 AED, and a 25 AED airport surcharge. A ride from the airport to downtown is typically 70-100 AED. Always insist on the meter and use official taxis or ride-hailing apps to avoid overcharging."),
    ],
    "Denver": [
        ("Is Denver safe for tourists?",
         "Denver is generally safe for tourists who stick to popular areas like LoDo, RiNo, Capitol Hill, and Cherry Creek. The 16th Street Mall has improved significantly after renovation, but petty theft remains an issue. Avoid walking alone on Colfax Avenue east of Broadway at night, and be alert around Union Station after dark."),
        ("Is the 16th Street Mall dangerous?",
         "The 16th Street Mall is not dangerous during the day but has documented issues with aggressive panhandling, pickpocketing, and distraction theft, especially after dark. Over 900 crimes were reported there in a recent two-year period. Stay aware, keep belongings secured, and avoid engaging with aggressive solicitors."),
        ("Should I rent a car in Denver?",
         "A rental car is useful for ski trips and mountain excursions but is a liability downtown. Vehicle break-ins are common at trailheads, and some budget rental companies at DEN are known for post-rental damage scams. Rent from major brands, photograph the car thoroughly, and never leave valuables inside."),
        ("Is it safe to buy cannabis in Denver as a tourist?",
         "Yes, if you buy from licensed dispensaries. Stick to shops with good reviews on Weedmaps, avoid delivery services (recreational delivery is illegal in Denver), and don't buy from anyone on the street. Prices vary widely — check online before visiting to avoid tourist markup."),
    ],
    "Grand Cayman": [
        ("Is Grand Cayman safe for tourists?",
         "Grand Cayman is very safe with low violent crime rates. The Cayman Islands consistently rank among the safest Caribbean destinations. Petty crime like pickpocketing can occur in George Town near the cruise port and at busy beaches, but serious crime against tourists is rare. Use normal precautions with valuables."),
        ("Do I need to exchange money in Grand Cayman?",
         "No. U.S. dollars are accepted everywhere in Grand Cayman. However, be aware that the Cayman Islands Dollar (KYD) is worth more than USD ($1 KYD = $1.25 USD). Always ask which currency prices are quoted in, and request credit card charges in KYD to get better exchange rates from your bank."),
        ("Are the taxi fares regulated in Grand Cayman?",
         "Yes, taxi fares are set by a government-published rate schedule, but taxis do not have meters. The rate from George Town to Seven Mile Beach should be about $25 for the car (not per person). Ask to see the official rate card, or take the public bus for $2.50 per person."),
        ("How do I avoid getting ripped off on excursions from the cruise port?",
         "Book through established operators like Captain Marvin's or Red Sail Sports, or pre-book through your cruise line. Avoid beach vendors offering last-minute deals. Verify any online operator has recent positive reviews on TripAdvisor and a physical office you can confirm."),
    ],
    "Toronto": [
        ("Is Toronto safe for tourists?",
         "Toronto is one of the safest major cities in North America. Violent crime against tourists is rare. The main risks are pickpocketing in crowded tourist areas, taxi-related fraud in nightlife districts, and online scams like fake eTA websites. Use normal big-city precautions and you'll be fine."),
        ("Is the TTC subway safe?",
         "The TTC is generally safe, including at night, though you should stay alert for pickpockets during rush hour at busy stations like Bloor-Yonge and Union. Avoid empty subway cars late at night and stand near the Designated Waiting Area marked on the platform. Buy Presto cards only from official machines or Shoppers Drug Mart."),
        ("Do I need a visa or eTA for Canada?",
         "Citizens of visa-exempt countries (US, UK, EU, Australia, etc.) need an Electronic Travel Authorization (eTA) costing $7 CAD, available ONLY at canada.ca/eta. U.S. citizens entering by air need a valid passport but not an eTA. Beware fake eTA websites charging $80-$120 for the same $7 application."),
        ("Are taxis safe in Toronto?",
         "Most Toronto taxis are safe and legitimate, but a major fraud ring was busted in 2024-2025 involving fake taxis and card-swapping schemes. Protect yourself by paying cash or tapping a credit card — never insert a debit card and enter your PIN. Verify the taxi has a City of Toronto license plate and visible driver ID."),
    ],
    "Fiji": [
        ("Is Fiji safe for tourists?",
         "Fiji is one of the safest South Pacific destinations. Violent crime against tourists is very rare. The main risks are petty theft in Nadi and Suva, taxi overcharging, and tourist-trap shopping scams. The resort islands (Mamanucas, Yasawas) are extremely safe. Exercise normal precautions and you'll have no issues."),
        ("Should I do a kava ceremony in Fiji?",
         "Absolutely — kava is central to Fijian culture and participating in a ceremony is a wonderful experience. Just make sure you do it through your resort, a licensed cultural tour, or in an actual village visit rather than in a souvenir shop on Nadi Main Street. The shop version is a sales trap, not a cultural exchange."),
        ("How do I get from Nadi Airport to my resort?",
         "Pre-book a transfer through your resort — most Fiji resorts offer airport shuttles. If you must take a taxi, use only LT-plated vehicles and insist the meter runs. The fare from Nadi Airport to Denarau should be $25-35 FJD. For island resorts, you'll need to get to Port Denarau Marina for a ferry or seaplane — book these transfers in advance."),
        ("Is it safe to drink kava?",
         "Traditional kava is safe to drink in moderate amounts. It produces a mild numbing and relaxing effect. However, be cautious about accepting any drink from strangers at bars — drink spiking has been reported in Fiji, particularly in Nadi and Suva nightlife areas. Stick to resort bars and kava ceremonies at licensed venues."),
    ],
    "Casablanca": [
        ("Is Casablanca safe for tourists?",
         "Casablanca is generally safe for tourists who exercise normal urban precautions. Most scams are low-level financial tricks like taxi overcharging and market inflation rather than violent crime. The city center, Hassan II Mosque area, and Corniche are well-patrolled. Avoid the Hay Mohammadi and Derb Sultan neighborhoods after dark, and stay alert in the Old Medina. Casablanca is safer than Marrakech for tourist scams simply because it has fewer tourists and less of a scam infrastructure."),
        ("How much should a taxi cost in Casablanca?",
         "Petit taxis (red) within the city should always use the meter. A typical ride within the city center costs 10-30 MAD. The airport to city center by official grand taxi costs around 300 MAD during the day. Never accept a fare without the meter running — if the driver refuses, exit and take another taxi. Apps like Careem show fair prices for comparison."),
        ("Is the Hassan II Mosque safe to visit?",
         "Yes, the Hassan II Mosque is a well-guarded landmark and one of the safest tourist sites in Casablanca. Entry tickets cost 120 MAD for a full interior tour. The main risk is henna sellers and unofficial guides approaching you outside the mosque — simply decline firmly and walk past them."),
        ("Should I exchange money at Casablanca airport?",
         "Avoid the Global Exchange counters at Mohammed V Airport, which have been repeatedly reported on TripAdvisor for extremely poor rates and hidden fees. Instead, use an ATM from a major Moroccan bank (Attijariwafa, BMCE, or Banque Populaire) in the arrivals hall, or exchange only a small amount at the airport and get a better rate in the city."),
        ("Is it safe to eat at the Marché Central?",
         "The Central Market itself is a vibrant and legitimate Casablanca experience, but the seafood restaurants inside are known for tourist overcharging. Buy your own fish from the fishmongers, then negotiate a fixed cooking fee (20-30 MAD) with a restaurant before sitting down. Refuse any dishes you didn't order."),
    ],
    "Belfast": [
        ("Is Belfast safe for tourists?",
         "Yes, Belfast is one of the safest capital cities in the UK and Europe. Violent crime against tourists is extremely rare. The main risks are petty theft, car break-ins at tourist sites, and the occasional taxi overcharge. The city center, Cathedral Quarter, Titanic Quarter, and university area are all very safe for walking around day and night. Exercise normal big-city precautions and you'll have no problems."),
        ("Are there areas to avoid in Belfast?",
         "Most of Belfast is safe for tourists. However, some residential areas like parts of North Belfast, West Belfast beyond the tourist murals, and certain interface areas between communities can be less welcoming after dark. Stick to the main tourist areas (city center, Cathedral Quarter, Titanic Quarter, Queen's Quarter) and you'll be fine. The PSNI provides regular safety updates."),
        ("Do I need cash in Belfast?",
         "Belfast is highly card-friendly and you can pay by contactless almost everywhere, including pubs, markets, and taxis. Carrying some cash (£20-30) is useful for St. George's Market vendors and small shops, but you don't need large amounts. Use bank-attached ATMs rather than standalone machines to avoid card skimming."),
        ("Is it safe to drive a rental car in Northern Ireland?",
         "Driving is the best way to see the Causeway Coast and other attractions, but rental car break-ins at tourist parking areas are a known risk. Put all bags in the boot out of sight before arriving at a car park, remove rental company stickers, and use official car parks with CCTV. Never leave valuables in the vehicle."),
        ("How do I get from the airport safely?",
         "Belfast has two airports. George Best Belfast City Airport has official taxis and the Airport Express 600 bus into the city center. Belfast International Airport (Aldergrove) is 30 minutes away with the Airport Express 300 bus. Both airports have official taxi ranks — always use the rank rather than accepting rides from drivers who approach you inside the terminal."),
    ],
    "Doha": [
        ("Is Doha safe for tourists?",
         "Qatar is extremely safe for tourists — it has one of the lowest violent crime rates in the world. The main risks are low-level financial scams like taxi overcharging and counterfeit goods at markets. The streets are safe to walk at any hour, and the police are professional and responsive. However, be aware of strict local laws regarding dress codes, alcohol consumption (only in licensed venues), and public behavior."),
        ("How do I get around Doha safely?",
         "The Doha Metro is the safest and cheapest option, connecting the airport to West Bay and Souq Waqif for just 2 QAR per ride. Uber and Careem operate with transparent pricing. If taking a taxi, ensure it has yellow 'T' plates and the meter is running from the base fare of 4 QAR. Avoid accepting rides from unmarked vehicles."),
        ("Is it safe to drink alcohol in Qatar?",
         "Alcohol is legal but heavily regulated. It is only served in licensed hotel restaurants and bars, and you must be 21 or over. Public intoxication is a criminal offense that can result in arrest, fines, or deportation. It is illegal to bring alcohol into the country. The bar scam (being lured to an overpriced venue) exploits the limited nightlife scene."),
        ("How do I bargain at Souq Waqif?",
         "Bargaining is expected at market stalls but not in shops with displayed prices. Start at 40-50% of the asking price and negotiate up. Be wary of claims about 'authentic Qatari pearls' at low prices — genuine natural pearls cost 5,000-30,000 QAR. For gold, stick to the Gold Souq where shops are more regulated and provide stamped receipts."),
        ("What should I know about tipping in Qatar?",
         "Tipping is not expected in Qatar as most restaurants include a service charge, but rounding up or leaving 10% is appreciated. Taxi drivers do not expect tips. This means you should not feel pressured to add large tips — if someone suggests otherwise, they may be trying to overcharge you."),
    ],
    "Seychelles": [
        ("Is Seychelles safe for tourists?",
         "Seychelles is very safe for tourists. It has one of the lowest crime rates in Africa, and violent crime against visitors is extremely rare. The main risks are petty theft at beaches and tourist price inflation. Exercise normal precautions — don't leave valuables unattended, use hotel safes, and verify prices before purchasing. All three main islands (Mahé, Praslin, La Digue) are safe to explore independently."),
        ("How expensive is Seychelles really?",
         "Seychelles is one of the world's most expensive tourist destinations. Budget travelers can expect to spend 100-150 EUR per day for basic accommodation, food, and transport. Mid-range is 200-400 EUR. Eating at local 'takeaway' shops and using public buses can cut costs significantly. Pay in Seychellois Rupees rather than euros to avoid markup."),
        ("Do I need a car in Seychelles?",
         "On Mahé, renting a car (40-50 EUR/day) is highly recommended for flexibility and cost savings compared to taxis. On Praslin, a car is useful but buses also cover the island. On La Digue, bicycles are the main transport. Take extensive photos of any rental car at pickup to protect against damage claim scams."),
        ("Is it safe to swim at Seychelles beaches?",
         "Most Seychelles beaches are safe for swimming, but some have strong currents and no lifeguards. Anse Lazio and Beau Vallon are generally safe. Anse Intendance on Mahé and some south-coast beaches have dangerous currents. Always check local conditions and never leave valuables unattended on the sand while swimming."),
        ("Should I exchange money at the airport?",
         "Yes — the airport exchange offices on Mahé offer the best rates in the country. Exchange what you need upon arrival. Never exchange money with unauthorized individuals, even if they offer better rates. Use ATMs from major banks (MCB, Nouvobanq) for additional cash, and always pay in Seychellois Rupees rather than euros for better value."),
    ],
    "Lagos": [
        ("Is Lagos safe for tourists?",
         "Lagos requires significantly more security awareness than most tourist destinations. The US State Department issues a Level 3 advisory (Reconsider Travel) for Nigeria. That said, many foreigners live and work in Lagos safely. The key is preparation: use pre-arranged transport, stay in secure neighborhoods (Victoria Island, Ikoyi, Lekki), avoid carrying valuables, and travel with local contacts when possible. Business travelers visit regularly without incident."),
        ("What neighborhoods are safest in Lagos?",
         "Victoria Island, Ikoyi, and the Lekki peninsula are the safest and most developed areas, with international hotels, restaurants, and security infrastructure. Lagos Island (commercial district) is safe during business hours. Avoid Oshodi, Mushin, Ajegunle, and areas along the Oshodi-Apapa Expressway, especially after dark."),
        ("How do I get from the airport safely?",
         "Pre-arrange pickup through your hotel or a verified contact. If that's not possible, use Uber or Bolt from the designated ride-share area — never accept rides from greeters who approach you in the arrivals hall. The drive from the airport to Victoria Island takes 30-90 minutes depending on traffic. Confirm your driver's identity before getting into any vehicle."),
        ("Is it safe to use ATMs in Lagos?",
         "Use ATMs inside bank branches during business hours only. Avoid standalone ATMs, machines at convenience stores, and any ATM after dark. Always cover the keypad when entering your PIN and set a low daily withdrawal limit. Card skimming and armed ATM robberies are documented risks."),
        ("What about the famous 'Nigerian scams'?",
         "While Nigeria is known for online advance-fee fraud ('419' scams), the risks for visitors in Lagos are more about street-level crime: one-chance robberies, police checkpoint extortion, airport scams, and petty theft. The email scams target people internationally and are unlikely to affect you as a visitor. Focus your safety awareness on transport and personal security."),
    ],
    "Quito": [
        ("Is Quito safe for tourists in 2025?",
         "Quito is generally as safe as many South American capitals. Between January and July 2024, only 175 crimes against tourists were reported among over 357,000 visitors — a 40% decrease from 2023. Homicides also dropped 19%. However, petty crime like pickpocketing, phone snatching, and the mustard scam remain daily risks in tourist areas. Use ride-hailing apps instead of street taxis, stay alert in the Centro Histórico and La Mariscal, and avoid displaying valuables."),
        ("What areas should I avoid in Quito?",
         "Avoid the southern neighborhoods of La Ecuatoriana, Chillogallo, and Turubamba. The Centro Histórico (Old Town) is generally safe during the day with police presence but should be avoided at night. La Mariscal is Quito's main tourist and nightlife district — it is lively but requires extra caution after dark. Stick to main streets and well-lit areas, and avoid wandering off established routes."),
        ("How do I take safe taxis in Quito?",
         "Never flag a taxi on the street in Quito. Use ride-hailing apps like inDriver or Cabify, or ask your hotel to call a registered taxi company. Official taxis have orange license plates or white plates with an orange stripe, a visible driver ID, and a security camera with intact white tamper-proof tape. Verify these before getting in. The camera and panic button systems are mandatory in Quito and significantly reduce the risk of express kidnapping."),
        ("Is the mustard scam still common in Quito?",
         "Yes, the mustard (or ketchup) distraction scam remains one of the most frequently reported tourist crimes in Quito. It happens daily in the Centro Histórico, on public buses, and in La Mariscal. The key defense is simple: if anyone points out a stain on your clothing, do not stop. Walk away immediately to a safe area before checking yourself. The stain is always planted by the scammer or an accomplice."),
        ("Is it safe to go out at night in Quito?",
         "Nightlife in La Mariscal around Plaza Foch is popular with both locals and tourists, but requires serious caution. Never accept drinks from strangers — scopolamine drugging is a documented risk. Travel in groups, use ride-hailing apps to get to and from venues, and avoid walking on quiet side streets after dark. The Centro Histórico and most of Quito outside the main nightlife strips should be avoided on foot after dark."),
    ],
    "Tel Aviv": [
        ("Is Tel Aviv safe for tourists?",
         "Tel Aviv is generally very safe for tourists. Street crime rates are low compared to most major Western cities. The main risks are non-violent scams: taxi overcharging, beach theft, and aggressive sales pressure for Dead Sea products. Security concerns related to the broader regional conflict exist but are managed through one of the world's most extensive security infrastructures. Follow local news and government advisories for up-to-date security information."),
        ("How much should a taxi cost from Ben Gurion Airport to Tel Aviv?",
         "The official fixed fare from Ben Gurion Airport to central Tel Aviv is approximately 170-200 NIS (about $45-55 USD). Use the official taxi rank outside the terminal and confirm the fixed fare before getting in. At night (after 9pm) and on Shabbat/holidays, the rate is about 25% higher. The Gett ride-hailing app is a reliable alternative with transparent pricing. The train from the airport to Tel Aviv costs about 13.5 NIS but does not run on Shabbat."),
        ("Is the Carmel Market safe to visit?",
         "Yes, the Carmel Market is safe and a must-visit attraction. The main risk is paying tourist-inflated prices for souvenirs and spices. Food items are fairly priced. Haggle for non-food items starting at 40-50% of the asking price. Keep your phone and wallet in front zippered pockets, as pickpocketing can occur in the crowded aisles, though it is not especially common in Tel Aviv."),
        ("Should I haggle in Tel Aviv?",
         "At the Carmel Market and souvenir shops, haggling is expected for non-food items like textiles, ceramics, and spices. Start at about half the asking price. In restaurants, cafes, supermarkets, and most retail shops, prices are fixed and haggling is not appropriate. For taxis, insist on the meter or agree on a price before the ride — do not negotiate after arriving."),
        ("Are there areas to avoid in Tel Aviv?",
         "Tel Aviv has no major no-go zones for tourists. The area around the Central Bus Station (Tachanah Merkazit) in southern Tel Aviv is rougher and best avoided after dark. The southern neighborhoods of Neve Sha'anan can feel sketchy at night. Otherwise, most tourist areas — the beachfront, Jaffa, Florentin, Rothschild, Carmel Market — are safe day and night."),
    ],
    "Bratislava": [
        ("Is Bratislava safe for tourists?",
         "Bratislava is very safe for tourists, with one of the lowest violent crime rates among European capitals. The main risks are non-violent scams: taxi overcharging at the train station, the 'pretty woman' bar scam, public transit ticket fines, and pickpocketing on crowded trams. Use ride-hailing apps, choose your own bars, validate your transit tickets, and keep valuables secure."),
        ("How do I avoid the bar scam in Bratislava?",
         "Never go to a bar suggested by someone who approaches you on the street, no matter how attractive or friendly they are. If you meet someone interesting, suggest a venue you have already chosen — a well-reviewed bar from TripAdvisor or Google Maps. Inside any bar, always ask for a menu with prices before ordering. If a bar has no menu, dim lighting, and aggressive staff, leave immediately."),
        ("Do I need to validate my tram ticket in Bratislava?",
         "Yes. You must stamp your paper ticket in the small yellow validation machine on board immediately after boarding. An unvalidated ticket is treated the same as no ticket — the fine is up to €80. Alternatively, use SMS tickets, the IDS BK mobile app, or buy a 24-hour/72-hour tourist pass to avoid this issue entirely."),
        ("How much should a taxi cost in Bratislava?",
         "From the main railway station to the Old Town should cost €5-9 via Bolt, Uber, or Hopin app. From the airport to the city center should be €15-25. If a taxi driver quotes €30 or more for a short city ride, walk away and use an app instead. Always ensure the meter is running and demand a receipt."),
        ("Is Bratislava a good base for day trips?",
         "Yes, Bratislava is excellent for day trips to Vienna (1 hour by train), Budapest (2.5 hours), and the Slovak countryside. Be cautious with transportation scams when crossing borders — pre-book train tickets online or use RegioJet and FlixBus for transparent pricing. Avoid accepting private transfer offers from people at the train station."),
    ],
    "Beirut": [
        ("Is Beirut safe for tourists right now?",
         "Beirut's safety situation depends on the current geopolitical context. The city center — including Hamra, Gemmayzeh, Mar Mikhael, Downtown, and Raouché — is generally safe for tourists during stable periods. Always check your government's latest travel advisory before visiting. Within the tourist areas, the primary risks are non-violent scams like taxi overcharging and restaurant tourist menus rather than violent crime."),
        ("How does money work in Lebanon for tourists?",
         "Lebanon has a dual-currency system. US dollars are widely accepted, especially at hotels, high-end restaurants, and shops. Lebanese lira is used for taxis, street food, and small purchases. Since 2024, the official bank rate matches the market rate, so exchange at banks or licensed sarrafs only. ATMs dispense both USD and LBP depending on the bank. Carry small-denomination USD bills as many places price in dollars."),
        ("How do I take taxis safely in Beirut?",
         "Use Bolt or Uber for transparent pricing. If taking a street taxi, agree on the fare before getting in and specify whether the price is in USD or LBP. For short trips within a neighborhood, use the 'service' (shared taxi) system — a set route costs about 100,000 LBP. From the airport, pre-arrange pickup through your hotel or use a ride-hailing app."),
        ("What areas should I avoid in Beirut?",
         "Avoid the southern suburbs (Dahieh), areas near the Palestinian refugee camps, and the area south of the airport unless accompanied by a knowledgeable local. Check security briefings about protest routes before visiting, as demonstrations can block major roads. The tourist areas of Downtown, Hamra, Gemmayzeh, Mar Mikhael, and Raouché are generally the safest zones."),
        ("Is the nightlife in Beirut safe?",
         "Beirut has some of the best nightlife in the Middle East, concentrated in Gemmayzeh and Mar Mikhael. These areas are heavily patrolled and generally safe. Watch your drink at all times, do not leave a drink unattended, and use Bolt or Uber to get home. The main risk is overpriced drinks at tourist-oriented venues — check reviews before choosing a bar."),
    ],
    "Austin": [
        ("Is Austin safe for tourists?",
         "Austin is one of the safer major cities in Texas. Violent crime against tourists is rare. The main risks are property crimes and scams: fake parking attendants, QR code phishing on meters, pedicab overcharging, and fake rideshare drivers on Sixth Street late at night. Exercise normal urban awareness, especially on Dirty Sixth (East 6th) after midnight."),
        ("Is Sixth Street safe at night?",
         "East 6th Street ('Dirty Sixth') between Congress Avenue and I-35 is Austin's rowdiest nightlife strip. While it is generally safe early in the evening, it gets unpredictable after midnight, especially on weekends — fights, aggressive behavior, and petty crime increase. APD maintains a heavy presence. West 6th Street and Rainey Street are calmer alternatives with a similar bar scene."),
        ("How do I avoid parking scams in downtown Austin?",
         "Use the Park ATX app for street parking — Austin does NOT use QR codes on meters, so never scan one. For surface lots, only use ones with visible company signage, posted rates, and legitimate receipt machines. During events, book parking in advance through SpotHero. If someone in a vest tries to collect cash for parking, verify their company affiliation before paying."),
        ("Are pedicabs in Austin a scam?",
         "Not inherently — pedicabs are a legitimate form of transportation in Austin. However, there are no set rates, and drivers rely on tips/voluntary fares, which can lead to disputes. Always agree on a total fare before getting in. For short distances on 6th Street, walking is usually faster and free. A fair pedicab rate is roughly $1-2 per block per person."),
        ("How do I safely buy tickets for ACL or SXSW?",
         "Buy only from official sources: Front Gate Tickets for ACL, the official SXSW website for badges. For resale, use StubHub or other platforms with buyer protection guarantees. Never buy wristbands from strangers outside the venue — documented scams involve sellers re-entering the festival, removing the wristband, and reselling it. Register wristbands to your name immediately after purchase."),
    ],
    "New Orleans": [
        ("Is the French Quarter safe at night?",
         "The main streets — Bourbon, Royal, and Decatur — are generally safe at night due to heavy foot traffic and police patrols. The risk increases on darker side streets, especially after midnight when you're alone or visibly intoxicated. Stick to streets with open businesses, walk with at least one other person, and avoid blocks between Bourbon and Rampart or near Armstrong Park after dark."),
        ("What is the most common scam in New Orleans?",
         "The 'I bet I can tell you where you got your shoes' hustle is the most frequently reported scam and has operated for decades. A man makes the bet, reveals the wordplay answer ('You got your shoes on your feet, and your feet are on Bourbon Street'), then demands payment. Simply say 'no thanks' and keep walking. The freestyle rap welcome and bead/bracelet force are close runners-up."),
        ("Which areas of New Orleans should tourists avoid?",
         "Avoid Central City (away from Oretha Castle Haley Boulevard), the Desire and Florida neighborhoods, and Hoffman Triangle — these are high-crime residential areas far from attractions. Within the tourist zone, use caution around Rampart Street, Armstrong Park after dark, and the Irish Channel near the waterfront at night."),
        ("Is it safe to use ATMs in the French Quarter?",
         "Use ATMs inside banks or hotels, not standalone machines on the street or in bars. The French Quarter has documented cases of skimming devices. Always inspect the card reader, cover the keypad when entering your PIN, and use tap-to-pay or chip transactions. Set up transaction alerts on your banking app."),
        ("How can I tell if a street performer is running a scam?",
         "Legitimate buskers set up in a fixed spot, perform for anyone, and have a tip jar — they never demand a specific amount. Scammers approach you directly, ask personal questions, initiate an unsolicited performance, then demand payment. The key is consent: if you chose to stop and watch, tipping is courteous. If someone targeted you, that's a hustle."),
    ],
    "Jakarta": [
        ("Is Jakarta safe for tourists in 2026?",
         "Jakarta is generally safe for tourists though it has Indonesia's densest tourist-financial-scam ecosystem — particularly airport taxi overcharging, Blue Bird impersonators, Grab/Gojek off-app cash negotiation, ATM skimming at malls and convenience stores, Kota Tua becak touts, and Blok M/Kemang honeypot-bar extortion. Violent crime against foreign visitors is rare in central areas; the practical risk is financial loss of US$30–$2,500. r/jakarta 'Visiting Jakarta: Is it really dangerous?' (comments/bbxb3t) is the community safety baseline. Save Jakarta Tourist Police (+62 21 570 9111) and Polda Metro Jaya (+62 21 523 4000)."),
        ("What is the most common scam in Jakarta?",
         "Soekarno-Hatta Airport (CGK) taxi overcharging is the most-reported entry scam — 'premium taxi' kiosks and arrivals-hall sign-holders quote Rp 500K–1.5M (US$30–$95) for central Jakarta transfers vs the real Grab/Blue Bird rate of Rp 150K–300K (US$10–$18) per r/indonesia 'Scammed 1500k idr for Airport to City in Jakarta' (comments/yigy0u). Blue Bird taxi impersonation is the second-most-common — non-affiliated blue-painted cars with tampered meters per r/jakarta 'Appreciation post for Jakarta' (comments/1gsifye, 2024). ATM skimming at mall and convenience-store ATMs is the highest-value loss category."),
        ("How do I get from CGK Airport to central Jakarta safely?",
         "Book Grab or Gojek yourself on airport Wi-Fi AFTER luggage — typical fare Rp 150K–250K (US$10–$16) to central Jakarta (Menteng, Sudirman, Kuningan), 45–90 min depending on traffic. For metered taxi, use ONLY Blue Bird (bright blue, 'Blue Bird Group' text, driver ID on dashboard) from the outdoor queue — Rp 200K–300K. The DAMRI airport bus to Gambir Station is Rp 75K for budget travellers (2 hours). IGNORE every 'taxi sir' approach inside the terminal — all legitimate pickup is outdoors. Avoid 'Premium Taxi' kiosks with flat cash-only rates."),
        ("Is Grab or Gojek safer than street taxis in Jakarta?",
         "YES for foreigners. Grab and Gojek are app-based with in-app pricing, GPS tracking, driver ratings, and GrabPay/GoPay cashless payment — eliminating nearly all scam vectors present in street taxis. r/indonesia 'How do Indonesians feel about Grab?' (comments/1mm9qmf, 2025) is the named 2025 community baseline confirming Grab is the de-facto foreigner-safe choice. Use ONLY the in-app payment method, never cash, and refuse any driver who requests cancellation or claims 'app broken' — this is the 2025 off-app negotiation scam per r/indonesia 'Grab driver tried negotiating a different fare?' (comments/c6k0cv). Blue Bird taxi is also safe IF you verify the logo and driver ID."),
        ("What should solo male travellers know about Jakarta nightlife?",
         "Blok M, Kemang, and certain SCBD bar strips host a documented 2025 honeypot-bar extortion pattern targeting foreign men via dating apps (Tinder, Bumble, Badoo). r/indonesia 'My one terrible night in Indonesia' (comments/243ly1) is the named anchor. The pattern: a dating-app match insists on a specific unmarked venue; hostesses join your table uninvited; mid-shelf whisky bottles appear priced at Rp 4M–15M; bouncers block the exit until card payment. ALWAYS pick the venue yourself (reputable named bars: Kilo Lounge Senopati, Awan Lounge, Cork & Screw in Kemang); ask for the written menu BEFORE ordering; refuse uninvited hostesses; pay only by credit card for chargeback capability. Immigration-threat extortion is bluff per r/indonesia 'Immigration officers foiled a love scam attempt' (comments/1m2sbwf, 2025)."),
    ],
    "Yogyakarta": [
        ("Is Yogyakarta safe for tourists in 2026?",
         "Yogyakarta is physically very safe — violent crime against foreign tourists is extremely rare — but it has one of Southeast Asia's densest tourist-commercial-scam ecosystems centred on Malioboro batik-gallery commissions, becak/andong 'free tour' kickbacks, Borobudur sunrise-ticket fraud, Prambanan 'mandatory guide' upsells, and Merapi jeep-tour overcharging. r/indonesia 'How we got scammed in Yogyakarta today' (comments/1m4ju1g, 2025) and r/travel 'So many scams in Yogyakarta' (comments/1q7dzfj, 2025) are the two named 2025 anchors. Save Yogya Tourist Police (+62 274 585 123) and Polda DIY (+62 274 551 077)."),
        ("What is the most common scam in Yogyakarta?",
         "The Malioboro batik-gallery commission scam is Yogya's #1 and most-documented tourist scam. A friendly English-speaking local (often via a becak driver) approaches near Malioboro or the Kraton with 'today only batik exhibition' or 'government art school' framing, walks the tourist 5–15 minutes off-route to a commission warehouse, and aggressively pitches mass-produced cotton batik at Rp 3M–15M (US$200–$950) vs a real price of Rp 200K–500K. r/indonesia 'How we got scammed in Yogyakarta today' (comments/1m4ju1g, 2025) is the canonical 2025 anchor. IGNORE every 'exhibition today only' approach — there is NO legitimate free batik exhibition."),
        ("How do I visit Borobudur temple affordably and ethically?",
         "Buy the daytime entry ticket at Rp 455,000 for foreigners (post-2023 reform) — at the official Borobudur ticket office OR via tiket.com / Traveloka. This includes upper-terrace stupa access with official guide rotation — no extra tips, no 'private access' upgrades exist. For the sunrise programme, book ONLY via Manohara Resort (manoharaborobudur.com) at Rp 600K–800K direct — reject every third-party 'skip-the-line sunrise' at Rp 1.5M+ (these are fake or re-sold with markup). For sunrise photo WITHOUT temple access, go to Punthuk Setumbu hill viewpoint at Rp 50K (self-arrange with Grab). The combo Borobudur + Prambanan ticket at Rp 680K via tiket.com saves Rp 150K vs separate purchases."),
        ("How do I avoid becak and andong tour scams in Yogyakarta?",
         "Refuse EVERY 'free tour' or 'Yogya tour 20,000 rupiah 2 hours all places' offer from becak or andong drivers on Malioboro — r/travel 'So many scams in Yogyakarta' (comments/1q7dzfj, 2025) documents the commission-kickback pattern where drivers earn 30–50% from silver/batik/herbal-medicine shops. Walk Malioboro on foot (it's only 1 km) and use Grab or Gojek for transfers between the Kraton, Taman Sari, and Borobudur/Prambanan day trips. For legitimate guided tours, book through licensed operators via Klook or Viator at Rp 300K–600K per person for half-day with published itinerary. If you want an authentic andong ride, take the fixed-price loop at Alun-Alun Utara at Rp 50K for 15 minutes (no commission stops)."),
        ("What's the best way from Yogya Airport (YIA) to the city?",
         "Yogyakarta International Airport (YIA) is at Kulon Progo, 45 km SW of central Yogya (60–75 min drive). Book Grab or Gojek yourself on airport Wi-Fi after luggage — typical fare Rp 250K–350K. For budget, use the DAMRI airport shuttle bus (Rp 75K, 90 min with stops, every 30 min 5 AM–9 PM). For direct YIA-to-Borobudur transfer (if sunrise tour booked), pre-book via Klook at Rp 600K–800K. IGNORE every 'premium taxi' kiosk quoting Rp 500K+ and every sign-holder offering 'direct to Borobudur' at Rp 1.5M+ per r/indonesia 'Visiting Yogyakarta in late April' (comments/1shrjdb, 2025). Old Adisutjipto Airport (JOG) has only limited domestic flights now; same Grab protocol applies."),
    ],
    "Lombok": [
        ("Is Lombok safe for tourists in 2026?",
         "Lombok is generally safe — less dense tourist infrastructure than Bali means less scam-pressure in quieter areas, but the main tourist nodes (Kuta-Lombok, Senggigi, Praya Airport) have an entrenched 2025 taxi-mafia, scooter-rental, and trek-operator overcharge ecosystem. r/Lombok 'Intro to Kuta, Lombok: What to expect' (comments/1q921cy, 2025) is the 2025 community anchor. Violent crime against foreigners is rare; practical risk is financial loss of US$50–$800. Save Polres Lombok Tengah (+62 370 628 555) for Kuta-Lombok area and Polres Mataram (+62 370 632 733) for Senggigi/Mataram."),
        ("What is the most common scam in Lombok?",
         "Lombok Praya Airport (LOP) taxi overcharging is the most-reported entry scam — arrivals kiosks and sign-holders quote Rp 500K–1M to Kuta-Lombok while the real Grab rate is Rp 200K–300K, per r/Lombok 'Intro to Kuta, Lombok: What to expect' (comments/1q921cy, 2025). Bali-Lombok fast-boat ticket fraud is the second-most-common — fake-operator websites and pier-front kiosks selling at 2–3x real rates. Mount Rinjani trek operators with porter overload (50–80 kg vs 25 kg legal limit) and skipped National Park permits are the highest-ethical-concern category per r/travel 'Indonesia Mt Rinjani hike' (comments/1ewqhi0, 2024)."),
        ("How do I get from Lombok Praya Airport (LOP) to Kuta-Lombok safely?",
         "Book Grab or Gojek yourself on airport Wi-Fi AFTER luggage — typical fare Rp 200K–300K (US$13–$20) for the 40-km/45–60 min drive. If Grab has no cars (Lombok supply is thinner than Bali), the airport Koperasi Taxi counter IS legitimate — rate sheet starts at Rp 350K (1.5x Grab but fair fallback). IGNORE every arrivals-kerb sign-holder or kiosk quoting Rp 500K–1M. Most Kuta-Lombok hotels include free airport pickup with advance notice — confirm at booking. For older travellers, the Koperasi Taxi counter is the easiest pre-app option."),
        ("Should I climb Mount Rinjani?",
         "Mount Rinjani (3,726m) is a serious strenuous multi-day trek — NOT recommended for travellers above 65 with mobility, heart, or breathing conditions. Ethical Rinjani: book ONLY licensed operators (Rudy Trekker, John's Adventures, Rinjani Trekking Club) at Rp 2.5M–5M per person with porter-load ≤25 kg per porter (legal limit). REFUSE any 'Rinjani special Rp 1.8M' — these skip the National Park permit (illegal, you'll be fined) or overload porters. r/travel 'Indonesia Mt Rinjani hike' (comments/1ewqhi0, 2024) documents the operator landscape. For older fit travellers, choose 3-day-2-night route (NOT exhausting 2D1N). Purchase trip insurance with helicopter evacuation coverage. If unsure, do Mount Batur in Bali instead (gentler one-day sunrise trek)."),
        ("What's the safest fast-boat from Bali to Lombok / Gili?",
         "Gili Getaway and Blue Water Express have the best 2025 safety records and on-time reliability — Rp 300K–500K one-way via the operator's direct website or 12go Asia / Klook. Eka Jaya is budget-friendly but slower and complaint-prone per r/bali 'Eka Jaya disappointment and Padang Bai taxi mafia' (comments/1mj47gv, 2025). AVOID Semaya One and Manta Express per r/bali 'Do NOT book Semaya One fast boat if you want to live' (comments/16e1lgw) and r/bali 'WARNING MANTA EXPRESS TO/FROM GILI ISLANDS' (comments/1bdrlbz) — overcrowding and safety concerns. For the Padang Bai taxi-mafia Grab blockade, exit Grab 300–500m BEFORE the port entrance and walk in."),
    ],
    "Gili Islands": [
        ("Are the Gili Islands safe for tourists in 2026?",
         "The Gili Islands (Trawangan, Air, Meno) are generally safe — no cars, no motorbikes, small tropical reef islands with low violent crime — but they host an entrenched 2025 scam ecosystem around fast-boat tickets, snorkelling tours, cidomo (horse cart) overcharging, dive-shop quality variance, and (at Gili Trawangan) magic-mushroom + drink-spiking nightlife. Gili Air and Gili Meno have significantly calmer commercial atmosphere than Gili Trawangan. r/bali 'Gili T: Best stays and Must-dos?' (comments/175imhe, 2024) is a community anchor. Save Gili Trawangan medical clinic (+62 370 613 2582) and Gili emergency WhatsApp (+62 812 3876 2345)."),
        ("How do I get to the Gili Islands from Bali safely?",
         "Book fast-boat tickets ONLY via 12go Asia, Klook, or the operator's direct website (Gili Getaway, Blue Water Express, Eka Jaya, Idola Express) — Rp 300K–500K one-way. The Serangan/Sanur (Bali) direct route to Gili Trawangan is faster (2 hours) and skips the Padang Bai taxi-mafia blockade entirely. AVOID Semaya One and Manta Express per community safety warnings. At Padang Bai (if routed there), exit your Grab 300–500m BEFORE the port entrance and walk in to bypass the taxi-mafia blockade documented in r/bali 'What is this Padang Bai grab scam?' (comments/1m74w1b, 2025). Print AND save PDF of your ticket."),
        ("Which Gili Island should I stay on?",
         "For older travellers and peace-seekers, stay on Gili Air (small bar scene, reef snorkelling, family-friendly) or Gili Meno (smallest, quietest, most rustic). Gili Trawangan has the party scene, best restaurants, and most accommodation BUT significantly more aggressive touts and the magic-mushroom/drink-spiking risk — best for day-tripping from Gili Air. r/bali 'Which is the quietest Gili Island?' (comments/1i3akc8) and 'Gili Air or Gili Meno?' (comments/139gdxe) are community anchors for the island-choice question. Inter-island hopping is easy via public ferry (Rp 35K) or GA boat."),
        ("How do I book a snorkelling tour on the Gili Islands without getting scammed?",
         "Book the standard 3-stop snorkelling tour (Gili Meno turtle reef, Gili Air wall, Gili Trawangan north reef) through your hotel or reputable agents (Go Gili Trawangan, Blue Marlin, Trawangan Dive Centre) at Rp 150K–250K per person group tour, 4 hours, mask/snorkel/fins/life-jacket included. REFUSE 'private boat' upgrades at Rp 800K–1.5M claiming 'exclusive turtle spots' (the reefs are public). REFUSE 'National Park fee Rp 100K per person' at the turtle reef — no such fee exists at Gili. VERIFY life jackets BEFORE boarding. Bring reef-safe zinc-based sunscreen — the reefs are under coral-bleaching stress."),
        ("Is it safe to get PADI certified on the Gili Islands?",
         "YES at reputable PADI/SSI 5-Star shops — but quality varies wildly across the 20+ Gili Trawangan and 8+ Gili Air dive operators. Reputable: Blue Marlin Dive, Manta Dive Trawangan, Oceans 5 Gili Air, Trawangan Dive Centre (all PADI/SSI 5-Star, Google 4.7+ with 100+ reviews). REFUSE any '2-day Open Water Express' at Rp 3.5M — full 4-day course (Rp 5.5M–6.5M) is safety-critical. ALWAYS check tank pressure gauge BEFORE each dive (210 bar is full; refuse 180 bar). Purchase DAN dive insurance (US$40/year) — chamber treatment is Rp 15M+ if uninsured. For older travellers, Discover Scuba (one-day intro) at Rp 850K–1.1M is safer than rushed certification. r/bali 'Gili T surf/dive schools recommendations' (comments/vshd9j) is the community-reviewed anchor."),
    ],
    "Bali": [
        ("Is Bali safe for tourists in 2026?",
         "Bali remains Indonesia's most tourist-friendly destination but has one of Asia's highest densities of documented financial scams targeting visitors — particularly airport taxi mafia, ATM skimming, scooter-rental 'pre-damage' fraud, money-changer sleight-of-hand, and (at Canggu/Seminyak beach clubs) organised drink spiking. Violent crime against foreigners is very rare; the practical risk is financial loss of US$200–$5,000 through well-run scam operations. r/bali 'What are the most common SCAMS on Bali? - First Time' (comments/np4ipb) is the community baseline. Save Polda Bali (+62 361 227 274) and the 24/7 Bali Tourist Police hotline (+62 361 759 687)."),
        ("What is the most common scam in Bali?",
         "Airport taxi overcharging is the most reported — scammers inside Ngurah Rai arrivals hall hold 'Grab' signs and quote 'fixed prices' 2–4x legitimate app rates (250K+ IDR to Kuta vs 60–100K via Grab). ATM skimming is the most financially damaging — r/bali 'Card skimming' (comments/1hqajly, 2025) and 'ATM Skimming $2000' (comments/1gsd3w5, 2025) document 2025 cases with $2,000+ losses from Uluwatu and Kuta ATMs. Scooter-rental 'spare key theft' (where operators claim 5–10M IDR for a scooter they stole back themselves) is the emerging 2025 pattern per r/bali 'Scooter scam' (comments/1ortjng, 2025)."),
        ("How do I get from Ngurah Rai Airport (DPS) to my hotel safely?",
         "Walk OUT of the arrivals hall to the designated Grab/Gojek pickup zone ~50m from terminal exit — drivers are NOT allowed inside. Book Grab or Gojek yourself on airport Wi-Fi AFTER collecting luggage; verify the licence plate matches the app. Typical fare: 60–100K IDR to Kuta, 80–140K to Seminyak, 300–400K to Ubud (1-hour drive). For Ubud, pre-book a Klook transfer (250–350K IDR) or use your hotel's free pickup. IGNORE every 'Grab' sign-holder inside the terminal — all are unauthorised. r/BaliTravelTips 'I ran into the Bali Taxi Mafia' (comments/1onardi, 2025) is the 2025 first-person anchor."),
        ("Where should I exchange money in Bali?",
         "Use ONLY PT Central Kuta Money Changer or BMC (Bali Maspintjinra) — both have verified Google 4.7+ reviews and published daily rates on their windows. AVOID any kiosk offering '+4% better rate' or labelled 'Authorised Money Changer' on a side street — r/bali 'SCAM ALERT in Bali – Please Read Before Exchanging' (comments/1r80hy6, 2025) documents the sleight-of-hand count where stacks of 100K IDR notes are short-counted 200K–500K during the hand-over. Always count bills yourself IN FRONT of the teller before leaving the counter, and compare to the day's published Bank Indonesia rate."),
        ("Is the Bali Tourist Tax (Rp 150,000) legitimate?",
         "Yes — the Bali Tourist Levy was introduced 14 February 2024 at Rp 150,000 (~US$10) per foreign visitor. Pay ONLY via the official 'Love Bali' portal (lovebali.baliprov.go.id) BEFORE arrival or at dedicated airport counters with digital receipt. Many scam sites have since emerged charging US$15–25 for 'processing'; r/bali 'Bali Tourist Tax - Scams' (comments/1amjrf2, 2025) documents the fake-portal pattern. Never pay any 'additional tourist tax' to a taxi driver, hotel clerk, or temple attendant — there is only ONE legitimate fee, paid ONCE per trip, via the official government portal."),
    ],
    "Ubud": [
        ("Is Ubud safe for tourists in 2026?",
         "Ubud is physically very safe — it's Bali's cultural heartland, village-scale, and violent crime against foreigners is essentially unknown. The practical risks are different from coastal Bali: Sacred Monkey Forest trained-theft (passports, sunglasses, phones), unethical Kopi Luwak 'coffee plantation' tours, fake-guru yoga/spiritual healing upcharges, an entrenched Ubud taxi mafia that blocks Grab pickup, and pushy massage/'extended service' pressure. r/digitalnomad 'Bali Ubud and Yoga Barn such a toxic place' (comments/10zcfl5, 2025) is the named 2025 community anchor for yoga-scene scepticism. Save +62 361 975 316 (Ubud Police)."),
        ("How do I visit the Sacred Monkey Forest safely?",
         "Leave ALL valuables in your hotel safe: sunglasses, earrings, smartphones, cameras with straps, and especially passports. r/bali 'Monkey steals passports and money at Ubud monkey Forest' (comments/z9loss, 2025) is the named anchor — monkeys are trained to target glittery or pocketed items. If a monkey grabs something, DO NOT chase or grab back; staff will 'recover' the item via food exchange for a 'tip' of 50–200K IDR (a documented commission loop). Pay the 80,000 IDR entry fee ONLY at the official ticket booth; no 'guide' is required or included. Visit early (9–10 AM) before feeding time aggression peaks."),
        ("Are Ubud's Kopi Luwak coffee tours ethical?",
         "Almost universally NO. r/bali 'Kopi luwak farms and animal welfare in Bali' (comments/1bx3nyi, 2025) documents near-universal civet caging at 'plantation' tours where animals are force-fed coffee cherries in cramped conditions — completely unlike the wild-foraged original tradition. Authentic wild-sourced Kopi Luwak is rare and expensive (~$150+ per 100g); the $20 'plantation' versions are almost always caged-civet or straight coffee labelled as Luwak. If you want to support ethical Balinese coffee, visit Seniman Coffee Studio in central Ubud (Jalan Sriwedari) — they source single-origin beans directly from Kintamani farmers with transparent traceability."),
        ("How do I get around Ubud without taxi scams?",
         "Use Grab or Gojek app — but meet your driver 100–200m AWAY from restaurant clusters on Jalan Monkey Forest, Jalan Raya Ubud, or Jalan Hanoman. r/bali 'Taxi mafia. What it is and how real it is?' (comments/1fo62fm, 2025) documents how local taxi drivers block Grab from central pickup points and physically pressure the Grab driver to hand the passenger over at 2x fare. For short distances in Ubud's small core, walking is often fastest. For Tegallalang Rice Terraces, Campuhan Ridge, or day trips, pre-book a full-day driver through your hotel (~600K IDR / 8 hours) to avoid the scam."),
        ("How do I book a yoga retreat or spiritual healing without getting scammed?",
         "Stick to established studios with transparent per-class pricing: Yoga Barn (120–150K IDR drop-in), Radiantly Alive (100–130K), or The Practice (100K). AVOID any Ubud 'guru' or 'shaman' offering 'one-on-one clearing sessions', 'past-life regression', or 'energy blockage removal' at $200–$2,000 — these are unregulated and r/digitalnomad 'Bali Ubud and Yoga Barn such a toxic place' (comments/10zcfl5, 2025) documents emotional manipulation and financial coercion patterns. Research any retreat on r/yoga and the Retreat Guru platform before paying deposits; never pay cash-only deposits above 20% of the total."),
    ],
}

def danger_badge(level):
    level = level.lower()
    if level == "high":
        return '<span class="danger-badge danger-high">⚠️ High</span>'
    elif level == "medium":
        return '<span class="danger-badge danger-medium">🔶 Medium</span>'
    else:
        return '<span class="danger-badge danger-low">🟢 Low</span>'

def make_tldr(story):
    """Extract first sentence as TL;DR bold summary."""
    # Split on first period followed by a space (to avoid breaking on abbreviations like "St.")
    for delim in ['. ', '— ', ' — ']:
        idx = story.find(delim)
        if idx != -1 and idx < 120:
            return story[:idx + len(delim)].rstrip(), story[idx + len(delim):]
    # Fallback: first 100 chars to nearest word
    if len(story) > 100:
        cut = story[:100].rfind(' ')
        if cut > 40:
            return story[:cut] + ' ...', story
    return None, story


def generate_scam_cards(scams, city="", n=0):
    html = ""
    for i, scam in enumerate(scams, 1):
        red_flags_html = "\n".join(f"                    <li>{rf}</li>" for rf in scam.get("red_flags", []))
        avoid_html = "\n".join(f"                    <li>{av}</li>" for av in scam.get("how_to_avoid", []))

        # TL;DR + remaining story (supports multi-paragraph stories via \n\n)
        story = scam.get('story', '')
        tldr, rest = make_tldr(story)
        def _render_paragraphs(text, cls):
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            if len(paragraphs) <= 1:
                return f'<p class="{cls}">{text}</p>'
            return "\n        ".join(f'<p class="{cls}">{p}</p>' for p in paragraphs)
        if tldr:
            story_html = f'<p class="scam-tldr">{tldr}</p>\n        ' + _render_paragraphs(rest, 'scam-story-body')
        else:
            story_html = _render_paragraphs(story, 'scam-story-body')

        html += f"""
    <!-- Scam {i} -->
    <div class="scam-card" id="scam-{i}">
        <div class="scam-header">
            <div>
                <div class="scam-number">Scam #{i}</div>
                <div class="scam-title">{scam['scam_name']}</div>
            </div>
            {danger_badge(scam['danger_level'])}
        </div>
        <div class="scam-location">📍 {scam['location']}</div>
        {story_html}
        <div class="scam-details">
            <div class="detail-block red-flags">
                <h4>Red Flags</h4>
                <ul>
{red_flags_html}
                </ul>
            </div>
            <div class="detail-block avoid">
                <h4>How to Avoid</h4>
                <ul>
{avoid_html}
                </ul>
            </div>
        </div>
    </div>
"""
        # Mid-content CTA after scam #3 (for pages with 5+ scams)
        if i == 3 and n >= 5:
            html += f"""
    <div class="mid-cta">
        <p>Like what you're reading? Get a full {city} itinerary with safety tips built in.</p>
        <a href="/plan/">Get Free Itinerary &rarr;</a>
    </div>
"""
    return html

def generate_toc(scams):
    """Generate a Table of Contents linking to each scam by anchor."""
    items = ""
    for i, scam in enumerate(scams, 1):
        level = scam.get("danger_level", "low").lower()
        badge_cls = level if level in ("high", "medium", "low") else "low"
        label = level.capitalize()
        items += f"""
            <li><a href="#scam-{i}"><span class="toc-badge {badge_cls}">{label}</span> {scam['scam_name']}</a></li>"""
    return f"""
    <div class="toc">
        <h2>Jump to a Scam</h2>
        <ol class="toc-list">{items}
        </ol>
    </div>"""


def generate_faq_schema(city, faqs):
    items = []
    for q, a in faqs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return items

def generate_faq_html(faqs):
    html = ""
    for q, a in faqs:
        html += f"""
        <div class="faq-item">
            <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
                {q}
                <span class="faq-arrow">▼</span>
            </button>
            <div class="faq-a">{a}</div>
        </div>
"""
    return html

def generate_page(city_data, related_cities_map):
    city = city_data["city"]
    country = city_data["country"]
    flag = city_data.get("flag", "🌍")
    scams = city_data["scams"]
    slug = CITY_SLUGS[city]
    n = len(scams)
    
    # Check for city-specific emergency info first, then country, then fallback
    em = EMERGENCY_INFO.get(f"{country} ({city})", EMERGENCY_INFO.get(country, EMERGENCY_INFO["United Kingdom"]))
    safety_tips = SAFETY_TIPS.get(city, [
        "Keep phones and valuables in secure pockets when in crowded areas",
        "Use only licensed taxis or app-based ride services",
        "Book tours and tickets through verified operators with online reviews",
        "Keep a copy of your passport separate from the original",
    ])
    faqs = FAQS.get(city, [])
    
    safety_tips_html = "\n".join(f"            <li>{tip}</li>" for tip in safety_tips)
    
    scam_cards = generate_scam_cards(scams, city=city, n=n)
    toc_html = generate_toc(scams)

    # Severity counts for hero summary
    high_count = sum(1 for s in scams if s.get("danger_level", "").lower() == "high")
    medium_count = sum(1 for s in scams if s.get("danger_level", "").lower() == "medium")
    low_count = sum(1 for s in scams if s.get("danger_level", "").lower() == "low")
    severity_pills = []
    if high_count:
        severity_pills.append(f'<span class="severity-pill high">{high_count} High Risk</span>')
    if medium_count:
        severity_pills.append(f'<span class="severity-pill medium">{medium_count} Medium</span>')
    if low_count:
        severity_pills.append(f'<span class="severity-pill low">{low_count} Low</span>')
    severity_html = f'\n    <div class="severity-summary">{"".join(severity_pills)}</div>' if severity_pills else ""

    # Reading time estimate (~200 words per minute)
    total_words = sum(len(s.get('story', '').split()) for s in scams)
    total_words += sum(len(' '.join(s.get('red_flags', [])).split()) for s in scams)
    total_words += sum(len(' '.join(s.get('how_to_avoid', [])).split()) for s in scams)
    read_min = max(2, round(total_words / 200))

    country_code = city_data.get("country_code", "")

    # Cross-links to health guide and country scam page
    health_slug = COUNTRY_HEALTH_SLUGS.get(country, "")
    cc_lower = country_code.lower() if country_code else ""
    cross_links = []
    if health_slug:
        cross_links.append(f'<a href="/health/{health_slug}/" class="cross-link">&#127973; {country} Health Guide</a>')
    if cc_lower:
        cross_links.append(f'<a href="/scams/country/{cc_lower}/" class="cross-link">&#128506; All {country} Scam Guides</a>')
    cross_links.append(f'<a href="/plan/" class="cross-link">&#128203; Free {city} Itinerary</a>')
    cross_links_html = f'\n    <div class="cross-links">{"".join(cross_links)}</div>' if cross_links else ""

    faq_schema_items = generate_faq_schema(city, faqs)

    faq_html = generate_faq_html(faqs) if faqs else ""

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Scams", "item": "https://tabiji.ai/scams/"},
                    {"@type": "ListItem", "position": 3, "name": city, "item": f"https://tabiji.ai/scams/{slug}/"}
                ]
            },
            {
                "@type": "Article",
                "headline": f"{n} Tourist Scams in {city} (2026)",
                "description": f"{n} real {city} tourist scams documented from Reddit travelers in 2026. Know what to watch for before you arrive.",
                "url": f"https://tabiji.ai/scams/{slug}/",
                "image": f"https://img.tabiji.ai/scams-{slug}-og.jpg",
                "datePublished": "2026-03-29",
                "dateModified": "2026-04-07",
                "author": {"@type": "Organization", "name": "tabiji.ai"},
                "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/", "logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"}},
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".takeaways-box"] + ([".faq-a"] if faqs else [])
                }
            },
            *(
                [{
                    "@type": "FAQPage",
                    "mainEntity": faq_schema_items
                }] if faq_schema_items else []
            ),
            {
                "@type": "Place",
                "name": city,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": city,
                    "addressCountry": country_code
                }
            }
        ]
    }
    
    schema_json = json.dumps(schema, indent=4, ensure_ascii=False)
    
    # Build key takeaways from scam data
    scam_names = [s['scam_name'] for s in scams]
    high_risk = [s['scam_name'] for s in scams if s.get('danger_level', '').lower() == 'high']
    takeaway_top = f"The #1 reported scam is the {scam_names[0] if scam_names else 'financial deception'}"
    takeaway_high = f"{len(high_risk)} of {n} scams are rated high risk" if high_risk else f"Most scams in {city} are low-to-medium risk"
    no_rideshare_cities = {"Aruba", "Turks and Caicos"}
    takeaway_transport = "Only use official taxis with government-set rates \u2014 confirm the fare before getting in" if city in no_rideshare_cities else _get_ride_advice(country_code)
    takeaway_avoid = f"Never accept unsolicited offers from strangers near tourist sites in {city}"

    takeaways_html = f"""            <li>{takeaway_top}</li>
            <li>{takeaway_high}</li>
            <li>{takeaway_transport}</li>
            <li>{takeaway_avoid}</li>"""

    # Build related cities section — split same-country + nearby
    related_html = ""
    if city in related_cities_map and related_cities_map[city]:
        same = []
        nearby = []
        for rc in related_cities_map[city]:
            rc_slug = CITY_SLUGS.get(rc["city"], "")
            if not rc_slug:
                continue
            card = f"""
            <a href="/scams/{rc_slug}/" class="related-card">
                <span class="related-flag">{rc.get('flag', '🌍')}</span>
                <span class="related-info">
                    <span class="related-city">{rc['city']}</span>
                    <span class="related-country">{rc['country']}</span>
                </span>
            </a>"""
            if rc["country"] == country:
                same.append(card)
            else:
                nearby.append(card)

        sections = ""
        if same:
            sections += f"""
        <h3 style="font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);margin:0 0 0.5rem;">More in {country}</h3>
        <div class="related-grid">{"".join(same)}
        </div>"""
        if nearby:
            sections += f"""
        <h3 style="font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted);margin:1rem 0 0.5rem;">Popular Nearby Destinations</h3>
        <div class="related-grid">{"".join(nearby)}
        </div>"""
        if sections:
            related_html = f"""
    <div class="related-section">
        <h2 class="section-heading">More Scam Guides</h2>{sections}
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{n} Tourist Scams in {city} (2026) — Real Stories & How to Avoid Them | tabiji.ai</title>
    <meta name="description" content="{n} real {city} tourist scams documented from Reddit travelers in 2026. Know what to watch for before you arrive — and exactly how to stay safe.">
    <meta property="og:title" content="{n} Tourist Scams in {city} (2026) — tabiji.ai">
    <meta property="og:description" content="{n} real {city} tourist scams documented from Reddit travelers in 2026. Know what to watch for before you arrive — and exactly how to stay safe.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/scams/{slug}/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta property="og:image" content="https://img.tabiji.ai/scams-{slug}-og.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="article:published_time" content="2026-03-29">
    <meta property="article:modified_time" content="2026-04-07">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{n} Tourist Scams in {city} (2026)">
    <meta name="twitter:description" content="Real scams, real stories, real advice. From Reddit travelers who got caught out in {city}.">
    <meta name="twitter:image" content="https://img.tabiji.ai/scams-{slug}-og.jpg">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai/scams/{slug}/">
    <link rel="stylesheet" href="/assets/shared-shell.css">
    <link rel="stylesheet" href="/assets/scams.css">

    <script type="application/ld+json">
    {schema_json}
    </script>
</head>
<body>
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/credit-cards/">💳 Credit Card Benefits</a>
                <a href="/health/">🏥 Travel Health Tips</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/scams/">Tourist Scams</a>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan/" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>

<div class="breadcrumb">
    <a href="/">Home</a><span>›</span><a href="/scams/">Scams</a><span>›</span>{city}
</div>

<main>
<div class="hero">
    <div class="hero-badge">🚨 Scam Guide · 2026</div>
    <h1>{n} Tourist Scams in {city}</h1>
    <p>Real stories from Reddit travelers. Know what to watch for before you arrive.</p>
    <div class="hero-meta">
        <span>📍 {city}, {country}</span>
        <span>📅 Updated April 2026</span>
        <span>💬 {n} scams documented</span>
        <span>⭐ Reddit-sourced & verified</span>
    </div>{severity_html}
    <div class="reading-time">&#128214; {read_min} min read</div>
</div>

<div class="content">
{cross_links_html}

    <div class="takeaways-box">
        <h2>Key Takeaways</h2>
        <ul>
{takeaways_html}
        </ul>
    </div>

    <div class="safety-box">
        <h2>⚡ Quick Safety Tips</h2>
        <ul>
{safety_tips_html}
        </ul>
    </div>

{toc_html}

    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
        <h2 class="section-heading" style="margin-bottom:0;border-bottom:none;padding-bottom:0;">The {n} Scams</h2>
        <button class="share-btn" onclick="if(navigator.share)navigator.share({{title:document.title,url:location.href}});else{{navigator.clipboard.writeText(location.href);this.textContent='&#10003; Link copied!';setTimeout(()=>this.innerHTML='&#128279; Share this guide',2000)}}">&#128279; Share this guide</button>
    </div>
    <hr style="border:none;border-top:2px solid var(--sand);margin:0.6rem 0 1.25rem;">
{scam_cards}

    <!-- What to do -->
    <div class="action-section" id="emergency">
        <h2>🆘 What to Do If You Get Scammed</h2>
        <div class="action-grid">
            <div class="action-item">
                <h3>📋 File a Police Report</h3>
                <p>Go to the nearest <strong>{em['police_name']}</strong> station. Call <strong>{em['police_number']}</strong>. Get an official crime report — you'll need this for insurance claims. You can also report online at <a href="{em['report_url']}" target="_blank" rel="noopener">{em['report_site']}</a>.</p>
            </div>
            <div class="action-item">
                <h3>💳 Cancel Your Cards</h3>
                <p>Call your bank immediately. Most have 24/7 numbers on the back of the card (keep a photo saved separately). Block any suspicious transactions before the thieves use your details.</p>
            </div>
            <div class="action-item">
                <h3>🛂 Lost Passport?</h3>
                <p>{em['lost_passport']}</p>
            </div>
            <div class="action-item">
                <h3>📱 Track Your Device</h3>
                <p>If your phone was stolen, use Find My (iPhone) or Find My Device (Android) from another device. Don't confront thieves yourself — share the location with police instead.</p>
            </div>
        </div>
    </div>

    {"" if not faq_html else '''<!-- FAQ -->
    <div class="faq-section">
        <h2 class="section-heading">Frequently Asked Questions</h2>
''' + faq_html + '''
    </div>'''}
{related_html}

    <!-- CTA -->
    <div class="cta-box">
        <h2>Ready to Plan Your {city} Trip?</h2>
        <p>Now you know what to watch for. Get a custom {city} itinerary with local tips, hidden spots, and restaurant picks — free.</p>
        <a href="/plan/" class="cta-btn">Plan Your {city} Trip →</a>
    </div>

</div>
</main>

<footer>
    <p>© 2026 tabiji.ai · <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> · <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> · <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> · <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> · <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>

<a href="#emergency" class="emergency-fab" aria-label="Emergency help">🆘</a>
<span class="emergency-fab-tooltip">Been scammed? Get help</span>
<a href="#" class="back-to-top" id="btt" aria-label="Back to top">&#9650;</a>

<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
<script>
(function(){{var b=document.getElementById('btt');if(!b)return;window.addEventListener('scroll',function(){{b.classList.toggle('visible',window.scrollY>600)}},{{passive:true}});b.addEventListener('click',function(e){{e.preventDefault();window.scrollTo({{top:0,behavior:'smooth'}})}});}})();
</script>
</body>
</html>"""
    return html


def build_related_cities_map(all_cities):
    """Build a mapping of city -> list of related cities.

    Strategy: up to 3 same-country cities + up to 3 popular cross-country
    cities from the same region or global popular list. This gives travelers
    useful links to nearby destinations they're likely also visiting.
    """
    # Group cities by country
    country_cities = defaultdict(list)
    city_lookup = {}
    for city_data in all_cities:
        city = city_data["city"]
        if city in CITY_SLUGS:
            entry = {
                "city": city,
                "country": city_data["country"],
                "flag": city_data.get("flag", "🌍"),
                "scam_count": len(city_data.get("scams", [])),
            }
            country_cities[city_data["country"]].append(entry)
            city_lookup[city] = entry

    # Region-based popular cities for cross-country recommendations
    region_popular = {
        "Europe": ["Paris", "Rome", "Barcelona", "Istanbul", "Prague", "Amsterdam", "London", "Berlin"],
        "Southeast Asia": ["Bangkok", "Bali", "Ho Chi Minh City", "Manila", "Phnom Penh", "Chiang Mai"],
        "East Asia": ["Tokyo", "Seoul", "Taipei", "Beijing", "Shanghai", "Kyoto"],
        "South Asia": ["Delhi", "Mumbai", "Kathmandu", "Colombo"],
        "Middle East": ["Istanbul", "Cairo", "Amman", "Jerusalem", "Dubai", "Marrakech"],
        "Africa": ["Cape Town", "Nairobi", "Marrakech", "Cairo", "Accra", "Zanzibar"],
        "North America": ["New York City", "Los Angeles", "Miami", "Cancún", "Las Vegas", "San Francisco"],
        "Central America & Caribbean": ["Cancún", "Havana", "San Juan", "Cartagena", "Panama City"],
        "South America": ["Buenos Aires", "Rio de Janeiro", "Lima", "Cusco", "Medellín", "Cartagena"],
        "Oceania": ["Sydney", "Melbourne", "Fiji", "Queenstown"],
    }
    country_to_region = {}
    europe = {"France", "Italy", "Spain", "Germany", "United Kingdom", "Netherlands", "Portugal",
              "Greece", "Czech Republic", "Austria", "Poland", "Hungary", "Croatia", "Belgium",
              "Ireland", "Denmark", "Iceland", "Scotland", "Romania", "Bulgaria", "Serbia",
              "Estonia", "Montenegro", "Switzerland", "Finland", "Sweden", "Norway", "Monaco"}
    sea = {"Thailand", "Vietnam", "Cambodia", "Philippines", "Indonesia", "Malaysia", "Laos", "Singapore"}
    ea = {"Japan", "South Korea", "Taiwan", "China", "Hong Kong", "Macau"}
    sa = {"India", "Nepal", "Sri Lanka"}
    me = {"Turkey", "Egypt", "Jordan", "Israel", "Morocco", "United Arab Emirates",
          "Saudi Arabia", "Qatar", "Oman", "Lebanon"}
    af = {"South Africa", "Kenya", "Tanzania", "Ghana", "Ethiopia", "Nigeria", "Senegal", "Mauritius", "Seychelles"}
    na = {"United States", "Canada"}
    ca = {"Mexico", "Cuba", "Puerto Rico", "Dominican Republic", "Costa Rica", "Panama",
          "Honduras", "Antigua and Barbuda", "Jamaica", "Aruba", "The Bahamas", "Turks and Caicos Islands",
          "Belize", "Guatemala", "El Salvador"}
    sam = {"Brazil", "Argentina", "Peru", "Colombia", "Chile", "Ecuador", "Bolivia", "Uruguay"}
    oc = {"Australia", "New Zealand", "Fiji"}
    for c in europe: country_to_region[c] = "Europe"
    for c in sea: country_to_region[c] = "Southeast Asia"
    for c in ea: country_to_region[c] = "East Asia"
    for c in sa: country_to_region[c] = "South Asia"
    for c in me: country_to_region[c] = "Middle East"
    for c in af: country_to_region[c] = "Africa"
    for c in na: country_to_region[c] = "North America"
    for c in ca: country_to_region[c] = "Central America & Caribbean"
    for c in sam: country_to_region[c] = "South America"
    for c in oc: country_to_region[c] = "Oceania"

    related_map = {}

    for city_data in all_cities:
        city = city_data["city"]
        if city not in CITY_SLUGS:
            continue
        country = city_data["country"]
        region = country_to_region.get(country, "")

        # Same-country cities (up to 3)
        same_country = [c for c in country_cities[country] if c["city"] != city][:3]

        # Cross-country: pick from same region, then global fallback
        cross_country = []
        used = {city} | {c["city"] for c in same_country}
        if region and region in region_popular:
            for rc in region_popular[region]:
                if rc not in used and rc in city_lookup and city_lookup[rc]["country"] != country:
                    cross_country.append(city_lookup[rc])
                    used.add(rc)
                if len(cross_country) >= 3:
                    break

        # If still short, add global popular
        global_fallback = ["Paris", "Bangkok", "Rome", "Tokyo", "Istanbul", "Prague", "Marrakech", "Cairo"]
        if len(cross_country) < 3:
            for gf in global_fallback:
                if gf not in used and gf in city_lookup:
                    cross_country.append(city_lookup[gf])
                    used.add(gf)
                if len(cross_country) >= 3:
                    break

        related_map[city] = same_country + cross_country

    return related_map


def generate_country_page(country, country_code, flag, cities_data, all_scams_count):
    """Generate an enriched country-level scam page."""
    cc_lower = country_code.lower()
    n_cities = len(cities_data)
    total_scams = sum(c["scam_count"] for c in cities_data)

    # Collect scam types across cities + count danger levels + build per-city scam-type previews
    # Curated categories map: keyword (lowercase) → display label.
    # Excludes vague words like "fake"/"restaurant" alone — they over-match and read as meaningless.
    SCAM_CATEGORIES = [
        ("pickpocket", "Pickpocketing"),
        ("taxi", "Taxi rigging"),
        ("overcharge", "Overcharging"),
        ("bracelet", "Bracelet scam"),
        ("petition", "Petition scam"),
        ("fake police", "Fake police"),
        ("fake monk", "Fake monk"),
        ("fake ticket", "Fake tickets"),
        ("atm", "ATM skimming"),
        ("currency", "Currency swap"),
        ("gps", "GPS rerouting"),
        ("meter", "Meter rigging"),
        ("card skim", "Card skimming"),
    ]
    scam_type_counts = defaultdict(int)
    danger_counts = {"high": 0, "medium": 0, "low": 0}
    city_types = {}  # slug → list of top 2 category labels for that city
    for cd in cities_data:
        slug = cd["slug"]
        city_cat_counts = defaultdict(int)
        for s in cd.get("scams_raw", []):
            name = (s.get("scam_name", "") or "").lower()
            level = (s.get("danger_level", "") or "").lower()
            if level in danger_counts:
                danger_counts[level] += 1
            for keyword, label in SCAM_CATEGORIES:
                if keyword in name:
                    scam_type_counts[label] += 1
                    city_cat_counts[label] += 1
                    break  # Each scam counts once; prefer the first (most specific) match
        city_types[slug] = [lbl for lbl, _ in sorted(city_cat_counts.items(), key=lambda x: -x[1])[:2]]

    high_count = danger_counts["high"]
    top_types = sorted(scam_type_counts.items(), key=lambda x: -x[1])[:6]
    top_types_html = ""
    if top_types:
        pills = "".join(
            f'<span class="scam-type-pill">{t} <span class="scam-type-count">{c}</span></span>'
            for t, c in top_types
        )
        top_types_html = f"""
    <section class="types-section">
        <h2 class="section-eyebrow">Most common scam types</h2>
        <div class="scam-type-row">{pills}</div>
    </section>"""

    # Emergency info — cleaned up layout: police / emergency / medical (if differs) / report URL
    em = EMERGENCY_INFO.get(country, None)
    emergency_html = ""
    if em:
        police = em.get("police_number", "")
        em_num = em.get("emergency_number", "")
        report_url = em.get("report_url", "")
        report_site = em.get("report_site", "")
        emergency_rows = f'<div class="emergency-item"><span class="emergency-label">Police</span><span class="emergency-value">{police}</span></div>'
        if em_num and em_num != police:
            emergency_rows += f'<div class="emergency-item"><span class="emergency-label">Emergency</span><span class="emergency-value">{em_num}</span></div>'
        if report_url and report_site:
            emergency_rows += f'<div class="emergency-item"><span class="emergency-label">Online report</span><a class="emergency-link" href="{report_url}" target="_blank" rel="noopener">{report_site} &rsaquo;</a></div>'
        emergency_html = f"""
    <aside class="emergency-box" aria-label="Emergency contacts">
        <h2 class="emergency-title">🚨 Emergency numbers in {country}</h2>
        <div class="emergency-grid">{emergency_rows}</div>
    </aside>"""

    # City cards — now with danger badge + scam-type preview line
    city_cards = ""
    for cd in sorted(cities_data, key=lambda x: -x["scam_count"]):
        slug = cd["slug"]
        city_city = cd["city"]
        n = cd["scam_count"]
        # Count danger for this specific city so we can show a high-risk badge
        city_high = sum(
            1 for s in cd.get("scams_raw", [])
            if (s.get("danger_level", "") or "").lower() == "high"
        )
        badge_html = ""
        if city_high > 0:
            badge_html = f'<span class="city-risk-badge" title="{city_high} high-risk scams">🔴 {city_high} high</span>'
        preview = city_types.get(slug, [])
        preview_html = ""
        if preview:
            preview_html = f'<p class="city-card-preview">{" · ".join(preview)}</p>'
        city_cards += f"""
        <a href="/scams/{slug}/" class="city-card">
            <div class="city-card-head">
                <h3>{city_city}</h3>
                {badge_html}
            </div>
            <div class="city-card-count">{n} scam{"s" if n != 1 else ""} documented</div>
            {preview_html}
        </a>"""

    # Danger breakdown strip for the hero — only shown if we have data
    total_with_level = sum(danger_counts.values())
    danger_strip_html = ""
    if total_with_level > 0:
        danger_strip_html = (
            f'<div class="danger-strip">'
            f'<span class="danger-item danger-high"><span class="danger-dot"></span>{danger_counts["high"]} high</span>'
            f'<span class="danger-item danger-med"><span class="danger-dot"></span>{danger_counts["medium"]} medium</span>'
            f'<span class="danger-item danger-low"><span class="danger-dot"></span>{danger_counts["low"]} low</span>'
            f'</div>'
        )

    # Cross-links — adds /books/ link alongside Health + Back
    health_slug = COUNTRY_HEALTH_SLUGS.get(country, "")
    cross_links_items = []
    cross_links_items.append('<a class="cross-link" href="/books/">📚 Travel Safety Series</a>')
    if health_slug:
        cross_links_items.append(f'<a class="cross-link" href="/health/{health_slug}/">🏥 {country} Health Guide</a>')
    cross_links_items.append('<a class="cross-link" href="/scams/">← All scam guides</a>')
    cross_links = "".join(cross_links_items)

    # Overview text
    if high_count > 0:
        risk_note = f"{high_count} scams across {country} are rated high risk."
    else:
        risk_note = f"Most scams in {country} are low-to-medium risk."

    # hasPart array for CollectionPage JSON-LD
    has_part_items = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"name":"{cd["city"]}","url":"https://tabiji.ai/scams/{cd["slug"]}/"}}'
        for i, cd in enumerate(sorted(cities_data, key=lambda x: -x["scam_count"]))
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://img.tabiji.ai">
    <title>Tourist Scams in {country} (2026) &mdash; All Cities | tabiji.ai</title>
    <meta name="description" content="Tourist scam guides for {n_cities} cities in {country}. {total_scams} scams documented from real Reddit traveler stories.">
    <link rel="canonical" href="https://tabiji.ai/scams/country/{cc_lower}/">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="Tourist Scams in {country} (2026) — tabiji.ai">
    <meta property="og:description" content="{total_scams} scams documented across {n_cities} cities in {country}. Real Reddit traveler stories.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/scams/country/{cc_lower}/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Tourist Scams in {country} (2026)">
    <meta name="twitter:description" content="{total_scams} scams across {n_cities} cities. Reddit-sourced.">
    <meta name="twitter:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@graph": [
            {{
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"}},
                    {{"@type": "ListItem", "position": 2, "name": "Scams", "item": "https://tabiji.ai/scams/"}},
                    {{"@type": "ListItem", "position": 3, "name": "{country}", "item": "https://tabiji.ai/scams/country/{cc_lower}/"}}
                ]
            }},
            {{
                "@type": "CollectionPage",
                "name": "Tourist Scams in {country}",
                "description": "Tourist scam guides for {n_cities} cities in {country}, sourced from real Reddit traveler reports.",
                "url": "https://tabiji.ai/scams/country/{cc_lower}/",
                "inLanguage": "en",
                "numberOfItems": {n_cities},
                "hasPart": [{has_part_items}],
                "publisher": {{"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/", "logo": {{"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"}}}}
            }}
        ]
    }}
    </script>
    <style>
        :root {{
            --indigo: #2D3A5C;
            --indigo-light: #3D4E7A;
            --warm-cream: #F5F0E8;
            --sand: #E8DFD0;
            --earth: #8B7355;
            --earth-light: #A6906F;
            --terracotta: #C4704B;
            --deep-brown: #3E2F23;
            --sage: #7A8B6F;
            --white: #FEFCF9;
            --text: #2C2419;
            --text-muted: #6B5D4F;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            color: var(--text); background: var(--white); line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        a {{ color: inherit; text-decoration: none; }}

        .breadcrumb {{
            background: var(--warm-cream);
            padding: 0.7rem 2rem;
            margin-top: 72px; /* clear the fixed site nav */
            font-size: 0.82rem;
            color: var(--text-muted);
            border-bottom: 1px solid var(--sand);
        }}
        .breadcrumb a {{ color: var(--text-muted); }}
        .breadcrumb a:hover {{ color: var(--terracotta); }}
        .breadcrumb span {{ margin: 0 0.4rem; color: var(--earth-light); }}

        .page-hero {{
            background: var(--white);
            padding: 3rem 2rem 2.5rem;
            text-align: center;
        }}
        .page-hero-inner {{ max-width: 820px; margin: 0 auto; }}
        .page-hero-eyebrow {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--terracotta);
            letter-spacing: 0.22em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }}
        .page-hero h1 {{
            font-size: clamp(2rem, 4.5vw, 2.8rem);
            line-height: 1.1;
            font-weight: 800;
            color: var(--text);
            letter-spacing: -0.02em;
            margin-bottom: 0.85rem;
        }}
        .page-hero-flag {{ margin-right: 0.3em; }}
        .page-hero p {{
            font-size: 1.05rem;
            color: var(--text-muted);
            max-width: 640px;
            margin: 0 auto 1.25rem;
        }}
        .page-hero-stats {{
            display: inline-flex; flex-wrap: wrap;
            gap: 0.5rem 0.65rem;
            justify-content: center;
        }}
        .stat-pill {{
            background: var(--warm-cream);
            border: 1px solid var(--sand);
            padding: 0.45rem 1rem;
            border-radius: 100px;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text);
        }}
        .stat-pill strong {{ color: var(--terracotta); font-weight: 700; }}

        .danger-strip {{
            display: inline-flex; flex-wrap: wrap; justify-content: center;
            gap: 0.3rem 1.1rem;
            margin-top: 1.25rem;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .danger-item {{ display: inline-flex; align-items: center; gap: 0.4rem; }}
        .danger-dot {{ width: 9px; height: 9px; border-radius: 50%; display: inline-block; }}
        .danger-high .danger-dot {{ background: var(--terracotta); }}
        .danger-med .danger-dot {{ background: #E0A867; }}
        .danger-low .danger-dot {{ background: var(--sage); }}

        .container {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 2.5rem 2rem 4rem;
        }}

        .emergency-box {{
            background: var(--warm-cream);
            border: 1px solid var(--sand);
            border-left: 4px solid var(--terracotta);
            border-radius: 14px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 2rem;
        }}
        .emergency-title {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--indigo);
            margin-bottom: 0.85rem;
            letter-spacing: -0.01em;
        }}
        .emergency-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.75rem 1.5rem;
        }}
        .emergency-item {{ display: flex; flex-direction: column; gap: 0.1rem; }}
        .emergency-label {{
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--earth);
        }}
        .emergency-value {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text);
        }}
        .emergency-link {{
            font-size: 0.9rem;
            color: var(--terracotta);
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 3px;
        }}
        .emergency-link:hover {{ color: #b5633f; }}

        .section-eyebrow {{
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--earth);
            margin-bottom: 0.85rem;
        }}

        .types-section {{ margin-bottom: 2rem; }}
        .scam-type-row {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
        .scam-type-pill {{
            display: inline-flex; align-items: center; gap: 0.4rem;
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 100px;
            padding: 0.4rem 0.95rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--indigo);
        }}
        .scam-type-count {{
            background: rgba(196,112,75,0.1);
            color: var(--terracotta);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.12rem 0.5rem;
            border-radius: 100px;
        }}

        .city-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        .city-card {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 14px;
            padding: 1.15rem 1.25rem 1.3rem;
            color: inherit;
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
        }}
        .city-card:hover {{
            transform: translateY(-3px);
            border-color: var(--terracotta);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }}
        .city-card-head {{
            display: flex; align-items: center; justify-content: space-between;
            gap: 0.5rem;
            margin-bottom: 0.25rem;
        }}
        .city-card h3 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--indigo);
            line-height: 1.2;
        }}
        .city-risk-badge {{
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            color: var(--terracotta);
            background: rgba(196,112,75,0.1);
            padding: 0.18rem 0.55rem;
            border-radius: 100px;
            white-space: nowrap;
        }}
        .city-card-count {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--terracotta);
            margin-bottom: 0.35rem;
        }}
        .city-card-preview {{
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.4;
        }}

        .cross-links {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--sand);
            display: flex; flex-wrap: wrap; justify-content: center;
            gap: 0.6rem 1.5rem;
            text-align: center;
        }}
        .cross-link {{
            color: var(--terracotta);
            font-weight: 600;
            font-size: 0.92rem;
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 3px;
        }}
        .cross-link:hover {{ color: #b5633f; }}

        footer {{
            padding: 2.5rem 2rem;
            text-align: center;
            border-top: 1px solid var(--sand);
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        @media (max-width: 640px) {{
            .page-hero {{ padding: 4rem 1.25rem 2rem; }}
            .container {{ padding: 2rem 1.25rem 3rem; }}
            .city-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
    <!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">&#9776;</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/api/">&#128268; API</a>
                <a href="/compare/">&#127386; Compare Destinations</a>
                <a href="/credit-cards/">&#128179; Credit Card Benefits</a>
                <a href="/find/">&#128269; Destination Finder</a>
                <a href="/resources/">&#128218; Resources</a>
                <a href="/health/">&#127973; Travel Health Tips</a>
            </div>
        </div>
        <a href="/scams/">Tourist Scams</a>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>
<!-- @include:nav:end -->

<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">
    <a href="/">Home</a><span>&rsaquo;</span><a href="/scams/">Scams</a><span>&rsaquo;</span>{country}
</div>

<header class="page-hero">
    <div class="page-hero-inner">
        <span class="page-hero-eyebrow">Tourist Scams</span>
        <h1><span class="page-hero-flag">{flag}</span>Scams to watch for in {country}</h1>
        <p>Scam guides for {n_cities} cities in {country}, sourced from real Reddit traveler reports. {risk_note}</p>
        <div class="page-hero-stats">
            <span class="stat-pill"><strong>{n_cities}</strong> cities</span>
            <span class="stat-pill"><strong>{total_scams}</strong> scams documented</span>
            <span class="stat-pill">Reddit-sourced</span>
        </div>
        {danger_strip_html}
    </div>
</header>

<main class="container">
{emergency_html}
{top_types_html}
    <section>
        <h2 class="section-eyebrow">City guides</h2>
        <div class="city-grid">{city_cards}
        </div>
    </section>
    <div class="cross-links">
        {cross_links}
    </div>
</main>

<!-- @include:footer:start -->
<footer>
    <p>&copy; 2026 tabiji.ai &middot; <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> &middot; <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> &middot; <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> &middot; <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> &middot; <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> &middot; <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> &middot; <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> &middot; <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> &middot; <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<!-- @include:footer:end -->

<script>
document.addEventListener('click', function(e) {{
    var dd = document.querySelector('.nav-dropdown');
    if (dd && !dd.contains(e.target)) dd.classList.remove('open');
}});
</script>
</body>
</html>"""
    return html


def build_country_data(all_cities):
    """Group cities by country for country page generation."""
    countries = defaultdict(lambda: {"cities": [], "flag": "🌍", "country_code": "", "seen_cities": set()})
    for city_data in all_cities:
        city = city_data["city"]
        if city not in CITY_SLUGS:
            continue
        country = city_data["country"]
        if city in countries[country]["seen_cities"]:
            continue
        countries[country]["seen_cities"].add(city)
        cc = city_data.get("country_code", "")
        flag = city_data.get("flag", "🌍")
        countries[country]["flag"] = flag
        countries[country]["country_code"] = cc
        countries[country]["cities"].append({
            "city": city,
            "slug": CITY_SLUGS[city],
            "scam_count": len(city_data.get("scams", [])),
            "scams_raw": city_data.get("scams", []),
        })
    return countries


def main():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    # Load city data — prefer enriched master if available
    all_cities = []
    enriched_master = os.path.join(base_dir, "research", "enriched_master.json")
    if os.path.exists(enriched_master):
        batch_files = [enriched_master]
        print("Using enriched master data")
    else:
        batch_files = sorted(glob.glob(os.path.join(base_dir, "research", "batch*.json")) +
                             glob.glob(os.path.join(base_dir, "research", "tier_b_batch*.json")) +
                             glob.glob(os.path.join(base_dir, "research", "tier_c_batch*.json")) +
                             glob.glob(os.path.join(base_dir, "research", "tier_d_batch*.json")) +
                             glob.glob(os.path.join(base_dir, "research", "new_batch_*.json")))
    for path in batch_files:
        with open(path) as f:
            data = json.load(f)
            all_cities.extend(data)

    print(f"Loaded {len(all_cities)} cities total")

    # Build related cities map
    related_cities_map = build_related_cities_map(all_cities)

    built = []
    for city_data in all_cities:
        city = city_data["city"]
        if city not in CITY_SLUGS:
            print(f"  Skipping {city} — no slug mapping")
            continue

        slug = CITY_SLUGS[city]
        out_dir = os.path.join(base_dir, slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")

        html = generate_page(city_data, related_cities_map)
        with open(out_path, "w") as f:
            f.write(html)

        print(f"  ✅ {city} → {slug}/index.html ({len(city_data['scams'])} scams, {len(html)} chars)")
        built.append((city, slug, len(city_data['scams'])))

    print(f"\nBuilt {len(built)} pages:")
    for city, slug, n in built:
        print(f"  - {city} ({n} scams) → /scams/{slug}/")

    # Build enriched country pages
    country_data = build_country_data(all_cities)
    country_built = 0
    for country, cdata in sorted(country_data.items()):
        cc = cdata["country_code"]
        if not cc:
            continue
        cc_lower = cc.lower()
        flag = cdata["flag"]
        cities = cdata["cities"]
        if len(cities) < 2:
            continue  # Only build country pages for countries with 2+ cities

        out_dir = os.path.join(base_dir, "country", cc_lower)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")

        html = generate_country_page(country, cc, flag, cities, len(built))
        with open(out_path, "w") as f:
            f.write(html)

        country_built += 1
        print(f"  🌍 {country} ({cc_lower}) → country/{cc_lower}/index.html ({len(cities)} cities)")

    print(f"\nBuilt {country_built} country pages")

    return built

if __name__ == "__main__":
    main()
