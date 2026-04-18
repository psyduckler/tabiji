#!/usr/bin/env python3
"""Generate scam pages for all cities based on Barcelona template."""
import json
import os
import glob

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
        "police_name": "Hellenic Police (Ελληνική Αστυνομία)",
        "police_number": "100",
        "emergency_number": "112",
        "report_url": "https://www.astynomia.gr/",
        "report_site": "astynomia.gr",
        "lost_passport": "Contact your nearest embassy or consulate. The US Embassy is at 91 Vassilisis Sophias Avenue, 10160 Athens. For emergencies: +30 210-721-2951.",
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
        "police_number": "1155 (Tourist Police, 24/7 English) or 191 (General Police)",
        "emergency_number": "191 (Police), 1669 (Medical), 1155 (Tourist Police)",
        "report_url": "https://www.touristpolice.go.th/",
        "report_site": "touristpolice.go.th",
        "lost_passport": "For passport replacement, contact the US Embassy Bangkok at 95 Wireless Road, Pathumwan, Bangkok 10330 (+66 2-205-4000, 24/7). In Chiang Mai, the US Consulate General is at 387 Witchayanond Road, Chiang Mai 50300 (+66 53-107-700). The UK Embassy is at 14 Wireless Road, Bangkok (+66 2-305-8333). The Australian Embassy is at 181 Wireless Road, Bangkok (+66 2-344-6300). Always call Tourist Police 1155 first — they speak English and will file the police report you need for passport replacement.",
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
        "police_name": "New York City Police Department (NYPD)",
        "police_number": "911",
        "emergency_number": "911",
        "report_url": "https://www.nyc.gov/site/nypd/index.page",
        "report_site": "nyc.gov/nypd",
        "lost_passport": "Visit the nearest US Passport Agency. The New York Passport Agency is at 376 Hudson Street, New York, NY 10014. For international visitors, contact your country's consulate directly.",
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
        "police_name": "Macau Public Security Police (治安警察局)",
        "police_number": "999 (Police) or 110 (Emergency)",
        "emergency_number": "999",
        "report_url": "https://www.fsm.gov.mo/",
        "report_site": "fsm.gov.mo",
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
    "Pattaya": "pattaya",
    "Krabi": "krabi",
    "Koh Samui": "koh-samui",
    "Koh Phangan": "koh-phangan",
    "Koh Phi Phi": "koh-phi-phi",
    "Koh Tao": "koh-tao",
    "Ayutthaya": "ayutthaya",
    "Hua Hin": "hua-hin",
}

# City-specific safety tips
SAFETY_TIPS = {
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
        "On Monastiraki Square and the Plaka, be alert to distraction techniques — the 'bump and lift' is common",
        "Metered Athens taxis start at €1.30 — if the driver doesn't turn the meter on, ask immediately or get out",
        "At restaurant terraces near Acropolis, always check if service charge and bread/couvert are included",
        "Keep your bag closed and in front of you on the metro between Monastiraki and Syntagma stations",
    ],
    "Berlin": [
        "Validate your U-Bahn/S-Bahn ticket every time — plain-clothes fare inspectors work tourist routes and fines are €60+",
        "Ignore aggressive souvenir hawkers at the Brandenburg Gate and Checkpoint Charlie who wave hats/items at you",
        "At Alexanderplatz, watch for the three-card monte (Hütchenspiel) — all bystanders winning are accomplices",
        "Book airport taxis through the official rank only — unofficial touts work outside both TXL and BER arrivals",
    ],
    "Madrid": [
        "Keep phones in pockets on the Metro Line 8 (Barajas airport line) and at Sol/Gran Vía stations — prime pickpocket territory",
        "At Plaza Mayor restaurants, ask for the menú del día (fixed-price menu) — it's usually excellent value and avoids a la carte traps",
        "Never stop for anyone claiming there's something wrong with you (stain, problem) — it's a distraction technique",
        "Only book flamenco shows through your hotel or official ticket offices — street tickets are often counterfeit",
    ],
    "Hanoi": [
        "Use the Grab app for all transportation — never negotiate a xe om (motorbike taxi) without agreeing on a firm price first",
        "At Hoan Kiem Lake and the Old Quarter, walk purposefully — looking lost triggers aggressive tour/rickshaw approaches",
        "Book Ha Long Bay tours only through licensed travel agencies with verifiable Google reviews",
        "In the Old Quarter, motorbike bag snatches happen — keep bags on the shoulder away from the road",
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
        "The Grand Palace is never 'closed for a royal ceremony' mid-day — anyone who tells you so near the entrance is running the tuk-tuk gem-and-tailor tour; verify on royalgrandpalace.th before you leave your hotel",
        "Insist on the meter at Suvarnabhumi and Don Mueang airports — the metered fare to Sukhumvit is ฿220–฿350 plus ฿45–฿75 toll; anything flat-rate above ฿500 is a scam",
        "Avoid bucket cocktails on Khao San Road — these are the primary delivery vehicle for drink-spiking; order bottled beer or mix-at-bar drinks you can watch being made",
        "On Patpong and Soi Cowboy, pay for each drink individually at the bar rather than running a tab — this caps your exposure when the padded bill arrives",
        "Save Tourist Police 1155 (24/7 English support) — they resolve bar extortion, taxi overcharge, and fake-monk complaints faster than the standard 191 police line",
    ],
    "Pattaya": [
        "On Walking Street, pay for each drink individually at the bar rather than running a tab — go-go 'lady drink' escalation is the #1 scam and caps your exposure",
        "Never accept a 'miracle' hair growth, coconut oil, or Ayurvedic consultation on Beach Road — the 2025 €4,000 and $700 German tourist scams (Khaosod English) were both this exact crew",
        "Do not rent jet skis on Pattaya Beach or Jomtien — the UK and US governments name Pattaya specifically for the jet ski damage shakedown",
        "Never hand your cash, wallet, or passport to a stranger for 'currency collection' or 'demonstration' — the Walking Street money-switch crew is active weekly",
        "Baht bus (songthaew) short-hop rate is ฿10–฿20 shared; anything quoted above that is the 'private charter' overcharge — confirm 'ten baht' out loud before getting in",
    ],
    "Krabi": [
        "Walk 500 meters inland from the Ao Nang beach strip before booking a Grab — the Ao Nang taxi mafia blocks ride-share pickups in the central tourist zone",
        "Benchmark Grab fares: Ao Nang → Tiger Cave ฿280, Ao Nang → Krabi Town ฿200, Ao Nang → KBV airport ฿350 — quotes above these are cartel pricing",
        "Never hand your original passport to a scooter rental — Ao Nang's main strip has passport-hostage damage scams (฿12,000+ demands); Smile Bike in Ao Nang accepts cash deposits",
        "Book Phi Phi ferries directly with Chao Koh or Songserm (฿300–฿450) — booth middleman markup runs ฿600–฿800",
        "For 4-Island longtail tours, book on 12go.asia or compare 3+ pier booths — the real price is ฿800–฿1,200 per person, not ฿3,000+",
    ],
    "Koh Samui": [
        "At Samui Airport (USM) and Nathon Pier, walk 500m away before requesting Grab/Bolt — the taxi mafia blocks ride-share inside the pier perimeter, and drivers will cancel if called too close",
        "Never rent from 'All Way Rent a Car' or 'Hakunarent' — both named in 2025 r/kohsamui SCAM ALERT threads for bogus ฿3,000 smoking fees and manufactured damage claims",
        "Grab benchmarks: USM → Chaweng ฿250, → Bophut ฿300, → Lamai ฿400; anything 2x+ above is cartel pricing",
        "Avoid Soi Green Mango go-go bars — the island's two main gogos have the highest lady-drink escalation rate; pay per drink at the bar",
        "Book tours only via Klook, 12go.asia, or Seatran Discovery (Ang Thong) — named scam operators include 'NCK Travel' and 'Funny Day Tours' per r/kohsamui",
    ],
    "Koh Phangan": [
        "Do not buy, carry, or consume recreational drugs on Phangan — 2025 saw active police stings with ฿30,000+ cash extortion and real arrests (Israeli soldiers, Chinese/Russian dealers all prosecuted Oct–Nov 2025)",
        "Cannabis dispensaries claiming 70%+ THC are running a scam — biological max is 34%; prices above ฿800/gram are 3–5x the Bangkok rate",
        "Walk 200m inland from Thong Sala Pier before calling Grab — pier-parked songthaews quote ฿300+ per person for trips that should be ฿150 shared",
        "Book Haad Rin accommodation 6+ weeks ahead for Full Moon — last-minute bookings are scam-prone and hosts routinely force cancellations to relist at higher prices",
        "Never leave original passport with a Haad Rin scooter rental shop — 2025 Russian rental scam bust and ฿11K–฿13K damage shakedowns are both documented",
    ],
    "Koh Phi Phi": [
        "Maya Bay national park fee is ฿400 per foreigner — book tours with park fee EXPLICITLY LISTED as included, or bring ฿400 cash as backup against double-billing",
        "Phi Phi ferries should cost ฿400–฿500 direct via Chao Koh Ferry or Songserm — booth middleman markup runs ฿1,200+ one-way",
        "Never accept bucket cocktails at Loh Dalum or Tonsai bars — Phi Phi has documented drink-spiking deaths (2025 French tourist, Canadian drowning) and buckets are the main vehicle",
        "Confirm ferry destination in writing before paying: 'Ao Nang beach pier' not just 'Krabi' — Urip Ferry scam routes tourists to Krabi Town pier",
        "For luggage porters at Tonsai Pier, agree total price in writing ('฿100 per bag, 2 bags, ฿200 total') — verbal quotes consistently 'misunderstood' on arrival",
    ],
    "Koh Tao": [
        "Budget ฿11,500–฿12,500 for PADI Open Water — sidewalk prices of ฿9,500 always exclude textbook, mask rental, cert fee, and boat fees",
        "Book with verified long-term dive shops: Black Turtle Dive, Big Blue, Koh Tao Divers, Crystal Dive — avoid shops with 2–3 day compressed courses and minimal pool practice",
        "Most 'beach entrance fees' (฿50–฿200) are illegal — Thai beaches are legally public; Sairee main strip, Mae Haad, and public Chalok Baan Kao sections are free",
        "Consider NOT renting a scooter — Koh Tao roads are notoriously dangerous (multiple tourist deaths) and shops use the ฿20K passport-hostage damage scam",
        "Travel with a buddy, stay on the Sairee main strip after dark, and if a dispute with a local business escalates to threats, leave on the next ferry — Koh Tao is small-island family-run and confrontations escalate faster than elsewhere",
    ],
    "Ayutthaya": [
        "Take the ฿20 SRT 3rd-class train from Bangkok Hua Lamphong — ignore anyone in 'uniform' outside the ticket hall routing you to a ฿1,500 'VIP minibus' (fake SRT scam documented in r/ThailandTourism 2025)",
        "Tuk-tuk benchmark: ฿200–฿300 per HOUR for the whole vehicle for temple hopping — never accept per-person quotes at the Ayutthaya station exit",
        "Never follow a 'Tourist Information Centre' agent to a storefront — the real TAT is at 108 Moo 3 Pratuchai; street recruiters steer you to commission packages",
        "Don't ride elephants in Ayutthaya — 'first price' upsells are standard and the animal ethics are explicitly warned against by every travel guide",
        "Rent a bicycle (฿50/day) for temple hopping — Ayutthaya is compact, bike-friendly, and temple admission is ฿50 per site or ฿220 combined pass",
    ],
    "Hua Hin": [
        "Walk 200–300m from Hua Hin Railway Station and Market Village before requesting Grab — 2025 taxi-mafia incidents included eggs thrown at Grab cars (made the news)",
        "Grab benchmarks: town center → Khao Takiab ฿100, → railway station ฿80, → Cicada Market ฿120 — tuk-tuk quotes of ฿300–฿500 are cartel inflation",
        "At restaurants and attractions (Hua Hin Zoo especially), ask to see both English and Thai menus — dual pricing is extensive and the Thai menu often has real prices",
        "Avoid Soi Bintabaht bars with touts pulling you in — Hua Hin's strip-club bill extortion runs the same pattern as Pattaya's Walking Street",
        "Never pay cash upfront for a condo purchase or long-term rental — use an escrow lawyer; named scam condos are flagged on r/ThailandTourism 2025",
    ],
    "Chiang Mai": [
        "Never enter a bar on Sri Don Chai Road, Loi Kroh Road, or any venue where a tout is standing outside recruiting — the July 2025 Diamond Karaoke assault (9 staff charged) happened after a British tourist followed a street invite",
        "Never hand over your original passport to a scooter rental shop — offer 3,000–5,000 baht cash deposit instead and photograph every panel before driving off (13,500+ baht damage claims are standard)",
        "Any tuk-tuk driver who tells you a temple is 'closed for cleaning' is running the gem shop tour scam — Wat Chedi Luang and Wat Phra Singh are never closed mid-day",
        "Yi Peng lantern festival tickets: only khomloy.com is the official CAD Khomloy event — all other 'premium' ticket sites at $200–$450 are scams or gutted experiences",
        "Save Chiang Mai Tourist Police at 053-247-318 (Charoen Rat Road) and the national hotline 1155 — they respond to bar extortion and passport-hostage cases and speak English",
    ],
    "Istanbul": [
        "Around the Sultanahmet (Blue Mosque / Hagia Sophia) area, ignore anyone who initiates conversation with 'Where are you from?' — it typically leads to a carpet shop or tea scam",
        "At the Grand Bazaar, treat all first-quoted prices as at least 50% inflated — polite negotiation is expected and essential",
        "Use the Istanbul Kart for all public transport — buying single tickets is significantly more expensive",
        "Never accept unsolicited invitations to a 'local bar' from men near Taksim Square — drinks will cost hundreds of dollars",
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
        "Book donkey rides or boat tours only through your hotel or licensed operators — touts at Fira dock frequently overcharge and underdeliver",
        "At Oia sunset viewpoint restaurants, check prices before ordering — some charge steep premiums for the view with no menu warning",
        "Use the cable car or walk the steps in Fira — donkey handlers may demand unexpected tips or overcharge at the bottom",
        "Rent ATVs only from established shops with insurance documentation — unlicensed rentals leave you liable for any damage on Santorini's narrow roads",
    ],
    "Phuket": [
        "Do not rent jet skis on Patong, Karon, Kata, or Kamala beaches — US/UK/AU governments all explicitly name this scam; demands of ฿30,000–฿300,000 for pre-existing scratches are routine",
        "Never leave your original passport with a scooter rental shop — offer a ฿3,000–฿5,000 cash deposit and photograph every panel of the scooter before driving off",
        "Use Grab or Bolt everywhere on Phuket — tuk-tuk mafias on Patong Beach Rd routinely quote 2–3x the app fare and block ride-share pickups at hotels",
        "Book all island tours (Phi Phi, James Bond, Maya Bay) through 12go.asia, Klook, or your hotel — Patong/Bangla storefront travel agencies routinely take cash and disappear",
        "Do not smoke on Phuket beaches — it's genuinely illegal under the 2017 beach smoking ban, and fake 'officers' exploit the ambiguity for cash shakedowns",
    ],
    "Ho Chi Minh City": [
        "Use the Grab app for all transportation — xe om (motorbike taxi) drivers without Grab frequently overcharge by 5-10x",
        "In District 1 and Ben Thanh Market, keep bags on the shoulder away from the street — motorbike bag snatches are common and fast",
        "At restaurants near tourist sites, confirm prices before ordering — some menus show one price but the bill reflects another",
        "Never hand your phone to a stranger for directions or photos — phone snatching by accomplices on motorbikes happens within seconds",
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
}

# City-specific FAQ
FAQS = {
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
         "Athens is generally safe for tourists. Petty theft — pickpocketing near the Acropolis, in the Monastiraki flea market, and on the metro — is the main risk. The Omonia area has more street-level crime and is best avoided at night. Violent crime targeting tourists is uncommon. Exercise the same awareness you would in any busy European city."),
        ("What is the most common scam in Athens?",
         "Taxi overcharging — particularly from Piraeus port and Athens airport — is the most reported scam. Restaurants near the Acropolis and Monastiraki Square overcharging with unlisted fees (couvert, bread, service) are the second most common complaint. The meter scam (starting the meter on Tariff 2 during daylight) is well-documented."),
        ("How do I get from Athens airport to the city?",
         "The Metro Line 3 (blue line) runs from the airport to Syntagma Square in 40 minutes and costs €9 (€18 return). Bus X95 to Syntagma runs 24 hours. Licensed airport taxis have a fixed rate of €40 daytime and €55 nighttime to the center — confirm this before getting in. Any quote significantly different is overcharging."),
        ("Are Athens taxis reliable?",
         "Athens taxis are metered and generally reliable, but taxi scams are well-documented. Legitimate practices: Tariff 1 (€1.06/km) within city; Tariff 2 (€1.24/km) outside city limits and midnight–5am. Insist the meter runs on Tariff 1 for daytime city trips. Note the taxi medallion number before getting in."),
        ("What areas should I avoid in Athens?",
         "Omonia Square at night has a higher crime rate and is best avoided after dark. Exarchia is known for political demonstrations and occasional unrest — check current conditions before visiting. The Monastiraki and Psirri areas are safe at night and have good nightlife, just watch your pockets in the flea market crowds."),
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
         "Madrid is generally safe. It has one of Spain's lower crime rates for a major city, but pickpocketing is common at Sol, Gran Vía, and on Metro Line 8 (airport line). The Lavapiés neighborhood has a higher street crime rate than other central areas. Violent crime targeting tourists is rare — the risk is almost entirely petty theft."),
        ("What is the most common scam in Madrid?",
         "Pickpocketing on Metro Line 8 (the Aeropuerto line) is the most reported tourist crime in Madrid — particularly at Nuevos Ministerios where the airport express and city metro connect. Restaurant overcharging near Plaza Mayor (unlisted bread charges, tourist menu traps) is the second most common complaint."),
        ("How do I get from Barajas Airport to Madrid center?",
         "Metro Line 8 runs from T1/T2/T3 and T4 to Nuevos Ministerios, where you transfer to lines 10, 6, or 8. The journey takes about 30 minutes and costs €4.50–€5 (airport supplement included). The Cercanías train from T4 to Atocha is even cheaper. Licensed airport taxis have fixed fares: €33 to any city center address (within the M-30 ring)."),
        ("Is the Menú del Día worth ordering in Madrid?",
         "Absolutely — the menú del día (daily set menu) is one of Spain's best traditions and offers exceptional value. Available at most restaurants at lunchtime (1:30–4pm), it typically includes a starter, main, dessert, bread, and a drink for €12–€18. It's usually the same quality as à la carte dishes at a fraction of the price. Ask for 'el menú' or look for the pizarrón (chalkboard) near the entrance."),
        ("What areas of Madrid are best for tourists?",
         "The historic center (Sol, Mayor, Lavapiés, La Latina) is the most interesting for first-timers. Malasaña and Chueca are the nightlife neighborhoods with genuine bars and restaurants at reasonable prices — a street or two from the tourist core. Salamanca is upscale with higher prices. Avoid eating anywhere you were actively recruited into from the street."),
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
         "Hanoi's street food is one of the highlights of Vietnam travel and generally safe if you choose busy stalls with high turnover and visible cooking. Bun cha, pho, and banh mi from street vendors are iconic and delicious. The risk is at restaurants in heavily-tourist areas that serve sanitized, mediocre versions at inflated prices — walk slightly off the tourist trail for the real thing."),
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
         "Santorini is one of the safest tourist destinations in Greece and Europe. Violent crime is virtually nonexistent. The main risks are tourist overcharging (restaurants, boat tours, transport), aggressive donkey ride operators, and sunburn/heat exhaustion. It's a place to watch your wallet, not your safety."),
        ("What is the most common scam in Santorini?",
         "Overcharging at restaurants with caldera views in Oia and Fira is the most common complaint — some charge steep premiums without menu prices. Unlicensed boat tour operators at Ammoudi Bay and Fira port who overcharge and underdeliver on quality are the second most reported issue."),
        ("Should I ride the donkeys in Santorini?",
         "The donkey path from Fira Old Port to the town is a traditional option, but animal welfare concerns have made it controversial. Some handlers demand unexpected tips or overcharge. The cable car (€6 each way) is faster, cheaper, and avoids the animal welfare issue entirely. The walk up takes about 30 minutes and is scenic."),
        ("How do I get around Santorini?",
         "KTEL buses connect Fira to Oia, Kamari, Perissa, and other villages — cheap and reliable. ATV/quad rentals are popular but rent only from established shops with insurance documentation. The roads are narrow and accidents are common. Taxis are scarce — book through your hotel. The ferry from Athinios port to Fira requires a bus or pre-booked transfer."),
        ("When is the best time to visit Santorini?",
         "May-June and September-October offer the best balance of weather and manageable crowds. July-August is peak season with extreme crowds, highest prices, and temperatures above 35°C. The famous Oia sunset is genuinely spectacular year-round, but arrive 2 hours early in peak season to secure a viewing spot."),
    ],
    "Phuket": [
        ("Is Phuket safe for tourists?",
         "Phuket is generally safe but requires significantly more awareness than many Southeast Asian destinations. Jet ski damage scams on Patong, tuk-tuk mafia overcharging, scooter rental passport-hostage shakedowns (฿30,000+ demands documented on Takuapa Rd in 2025), and Bangla Road drink-bill extortion are the four most reported tourist risks. The tourist areas (Patong, Kata, Karon) are safe to walk day and night, but motorbike accidents remain the #1 cause of tourist injury — not crime. Save Tourist Police 1155 (English, 24/7) before you arrive."),
        ("What is the most common scam in Phuket?",
         "The Patong jet ski damage scam is Phuket's most notorious — UK, US, and Australian governments all name it in their Thailand travel advisories. Operators rent jet skis with pre-existing scratches (often hidden under tape), then demand ฿30,000–฿300,000 for 'damage' on return, backed by a 'police officer' who is often complicit. Bangkok Post's 2024 'Police bust Phuket jet-ski scammers' and Thaiger's 2025 'Phuket jet ski blitz nets 38 illegal rides' confirm the scam is still active despite enforcement. The Patong tuk-tuk mafia overcharge is the second most common, with quotes 2–3x the Grab app fare."),
        ("Are tuk-tuks safe in Phuket?",
         "Phuket tuk-tuks are physically safe but financially predatory — there are no meters and prices are 2–3x the Grab rate. A Grab from Patong to Phuket Town is about ฿350; tuk-tuks quote ฿1,000+. Drivers also physically block Grab pickups at hotel driveways on Patong Beach Rd. Use the Grab app everywhere — if your hotel pickup is blocked, walk one block toward the main road. The official metered taxi counter at Phuket Airport (HKT) inside arrivals is reliable; avoid drivers who approach you outside the terminal."),
        ("Is Patong Beach safe at night?",
         "Bangla Road is Patong's nightlife center and is generally safe to walk through but has three active scams. First, drink-spiking at poorly-reviewed bars — never accept bucket cocktails or leave drinks unattended. Second, ping pong show bill extortion — venues use menu substitution, charge ฿500–฿2,000 per drink, and block exits when bills are questioned (avoid entirely per r/phuket community consensus). Third, the beach smoking 'police' shakedown — smoking on Patong beach is illegal under the 2017 ban and fake officers exploit this for ฿15,000–฿20,000 cash 'fines.' Don't smoke on beaches and stick to bars with Google reviews."),
        ("Should I rent a motorbike in Phuket?",
         "Motorbike accidents are the leading cause of tourist injuries in Phuket — roads are hilly, narrow, and local driving is aggressive. If you do rent, never leave your original passport as deposit (the 2025 Takuapa Road scam documented on r/phuket involved a ฿30,000 damage demand with physical threats while the shop held the renter's passport). Offer a ฿3,000–฿5,000 cash deposit instead, photograph every panel of the scooter from all angles (including underside) before driving off, and insist on a written damage inspection. An International Driving Permit (Class A) is legally required; check your travel insurance covers motorbike injury — most policies don't."),
    ],
    "Ho Chi Minh City": [
        ("Is Ho Chi Minh City safe for tourists?",
         "Ho Chi Minh City (Saigon) is generally safe for tourists, but petty crime — particularly motorbike bag snatching and phone theft — is more common than in most Southeast Asian capitals. The tourist districts (District 1 and District 3) are manageable with basic awareness. Violent crime targeting tourists is uncommon."),
        ("What is the most common scam in Ho Chi Minh City?",
         "Motorbike bag snatching is the most common and most dangerous crime targeting tourists — thieves on motorbikes grab bags from pedestrians and speed away, sometimes causing injury. Xe om (motorbike taxi) and taxi overcharging is the most common scam. Always use Grab for transport."),
        ("How do I get from Tan Son Nhat Airport to the city?",
         "The Grab app is the safest and cheapest option — book a car from inside the terminal. A Grab to District 1 costs 80,000-120,000 VND. Bus 109 runs to the city center for 20,000 VND. Only use official Vinasun (white) or Mai Linh (green) taxis from the rank — rogue taxis with similar logos are common and overcharge."),
        ("Is street food safe in Ho Chi Minh City?",
         "Saigon has extraordinary street food and it's generally safe at busy stalls with high turnover. Bún thịt nướng, phở, and bánh mì from street vendors are iconic. Drink bottled water only, avoid ice from street stalls unless it's clearly commercially produced (cylindrical shape with a hole). Restaurant pricing near Bùi Viện backpacker street is often inflated."),
        ("What areas should I avoid in Ho Chi Minh City?",
         "District 1 and District 3 are the safest tourist areas. Bùi Viện (backpacker street) is safe but attracts scammers and overcharging bars at night. District 4 and parts of District 8 have higher crime rates and aren't on the typical tourist circuit. The area around Bến Thành Market is safe during the day but requires bag awareness due to snatch theft."),
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
         "Bangkok is generally safe — violent crime against tourists is rare and the city is overwhelmingly welcoming. But SCMP and Men's Journal both named Bangkok the world's #1 city for tourist scams in 2025, reflecting the density of financial cons: Grand Palace gem tours, taxi meter refusal, tuk-tuk tailor scams, Patpong bar extortion, and Khao San drink-spiking. Sukhumvit, Silom, and the Old Town are safe to walk at night with basic awareness. Save Tourist Police 1155 (24/7 English support) and travel in pairs after midnight in Khao San and Patpong."),
        ("What is the most common scam in Bangkok?",
         "The 'Grand Palace is closed' tuk-tuk gem tour remains Bangkok's most financially devastating scam — tourists are intercepted at the palace entrance by a 'tourism officer' or 'teacher' who claims the palace is closed for a royal ceremony, then routed through a tuk-tuk loop ending at a gem store or tailor where purchases run $400–$2,000. The Grand Palace is never closed mid-day for a royal ceremony; verify on royalgrandpalace.th. Taxi meter refusal at Suvarnabhumi (flat ฿500–฿800 quotes vs. a ฿220–฿350 metered fare) is the second most common."),
        ("How do I get from Suvarnabhumi Airport to Bangkok?",
         "The Airport Rail Link City Line (฿45, 47 min to Phaya Thai) is the cheapest option and avoids the taxi scam scene entirely. From Phaya Thai take a Grab or BTS to your hotel. Metered taxis from the official basement rank are reliable if you insist on the meter — budget ฿220–฿350 plus ฿45–฿75 in Motorway tolls. Grab works at the designated Level 4 (Departures) pickup zone. Any driver offering a flat rate above ฿500 outside the official queue is scamming; photograph the plate and try the next one."),
        ("Are tuk-tuks safe in Bangkok?",
         "Tuk-tuks are safe as a transport mode and a genuine local experience. The scam to avoid is a driver offering a 'tour' for an impossibly low price (฿20–฿50 per hour) — the route will include gem stores, tailor shops, or Buddha-amulet vendors who pay the driver 30–40% commission on anything you buy. Pay normal tuk-tuk fares (฿80–฿150 per point-to-point trip, not per hour) and tell the driver exactly where you want to go. Better yet, use Grab for a fixed app price. Tuk-tuks that park near tourist sites waiting for fares are always running the tour scam; circulating tuk-tuks are usually fine."),
        ("What neighborhoods are best in Bangkok?",
         "Sukhumvit (Nana to Ekkamai) has excellent food, bars, and nightlife — though Soi 11 is prime territory for the Indian 'lucky face' hair supplement crew. Silom/Sathon is the financial district with great restaurants; Patpong Soi 1/2 within Silom is the main ping pong show scam zone. The Old Town (Rattanakosin) has Wat Pho, Grand Palace, and Wat Arun — approach via the Chao Phraya Express Boat, not by tuk-tuk. Ari is the trendy local neighborhood for cafés with the lowest scam density. Khao San Road is safe but has the highest drink-spike risk in the city — go in a group, avoid buckets."),
    ],
    "Pattaya": [
        ("Is Pattaya safe for tourists?",
         "Pattaya is physically safe for tourists — violent crime against visitors is rare and Beach Road, Central Pattaya, and Jomtien are walkable day and night. But Pattaya has Thailand's highest concentration of financial scams targeting nightlife: go-go bar 'lady drink' escalation, Walking Street money-switch crews, fake Muay Thai fights, and the hair-supplement shops that hit a German tourist for €4,000 (Khaosod English, November 2025). Pattaya Police ran a 'zero-tolerance' anti-scam crackdown in June 2025 (Pattaya Mail) but enforcement on Walking Street remains spotty. Save Tourist Police 1155 before arrival — the line responded to multiple 2025 bar extortion cases."),
        ("What is the most common scam in Pattaya?",
         "Go-go bar lady-drink escalation on Walking Street is the most common financial scam — tourists order one drink for a hostess and end up with ฿5,000–฿20,000 bills for drinks they didn't explicitly order, sometimes with bouncers blocking exits. The Khaosod English 2025 reports of German tourists hit for €4,000 (coconut oil) and $700 (hair growth) show the 'miracle supplement' shop scam is also highly active on Beach Road. The infamous jet ski damage shakedown on Pattaya Beach is the third most common — UK and US travel advisories name Pattaya explicitly."),
        ("How do I get from Suvarnabhumi Airport to Pattaya?",
         "The Bell Travel Service and Roong Reuang Coach shuttle buses from Suvarnabhumi (BKK) cost ฿200–฿250 and take about 2 hours to Pattaya (Jomtien, Central Pattaya stops). Grab from BKK to Pattaya is ฿1,500–฿2,200. From Don Mueang (DMK), the 389 bus to Pattaya runs for ฿119. Inside Pattaya, use the blue baht bus (songthaew) for ฿10 shared fares on Beach Road/Second Road routes — confirm 'ten baht' verbally before getting in, or you'll be quoted 'private charter' at ฿100–฿400."),
        ("Is Walking Street safe at night?",
         "Walking Street is physically safe to walk through — pickpocketing and violent crime against tourists are rare. The risks are financial: bar bill extortion at go-go clubs (bring only ฿2,000 cash, leave cards at hotel), fake Muay Thai fight venues with drink-price upselling, the 'can I see your currency' money-switch scam, and aggressive ladyboy propositions with bill-escalation tricks (r/Pattaya 'Ladyboy Scam' 2025 documented ฿2,000→฿5,000 escalation). Travel in groups, pay for each drink individually at the bar, and do not accept services from anyone who approached you on the street."),
        ("Should I rent a jet ski or scooter in Pattaya?",
         "Do not rent jet skis on Pattaya Beach, Jomtien, or Koh Larn — the jet ski damage scam is called 'infamous' on r/Thailand and named in UK, US, and Australian government travel advisories. Operators rent with pre-existing scratches hidden under tape, then demand ฿25,000–฿100,000 for 'damage' on return, often backed by a 'police officer' who is complicit. For scooters, never leave your original passport as deposit — offer ฿3,000–฿5,000 cash instead. Motorbike accidents remain a top tourist injury cause; wear a helmet and check your travel insurance covers motorbike injuries."),
    ],
    "Krabi": [
        ("Is Krabi safe for tourists?",
         "Krabi and Ao Nang are generally safer than Phuket for violent crime, but the Ao Nang taxi mafia is one of Thailand's most aggressive — Grab and Bolt drivers refuse to pick up in the central Ao Nang strip because of intimidation by local taxi cartels (r/ThailandTourism 2025). The scooter rental passport-hostage scam is active on Ao Nang's main road, and the 4-Island longtail tour market has a 2x–5x pricing spread depending on which booth you book from. Railay Beach is scam-free but only accessible by boat from Ao Nang. Save Tourist Police 1155 and the Ao Nang beach police box location before you go."),
        ("What is the most common scam in Krabi?",
         "The Ao Nang taxi mafia is Krabi's most systemic scam — drivers quote 3x–5x the Grab app rate (Ao Nang → Tiger Cave quoted at ฿1,500 vs. a ฿280 Grab fare, per r/ThailandTourism 'Taxi Mafia in Krabi'), and ride-share drivers are blocked from picking up in the central strip. The 4-Island tour overcharge is the second most common — booth prices of ฿3,000+ per person are 3x the legitimate ฿800–฿1,200 rate. Tiger Cave Temple is correctly labeled 'a well known scam place' on r/ThailandTourism for fake entry fees and guide shakedowns."),
        ("How do I get from Krabi Airport to Ao Nang?",
         "Krabi International Airport (KBV) is 25 km from Ao Nang. The airport shuttle bus costs ฿150 and takes about 45 minutes. A metered taxi from the official counter inside arrivals costs ฿600–฿700 to Ao Nang; Grab costs ฿350–฿400. Do not take taxis outside the terminal — only the counter inside arrivals is regulated. Grab works at Krabi airport but drivers may ask you to walk to the frontage road for pickup; this is legitimate, not a scam."),
        ("How do I avoid the Ao Nang taxi mafia?",
         "The community-verified fix is to walk 500 meters inland from the Ao Nang beach strip (away from the main beach road) before requesting a Grab — outside the cartel's perimeter, Grab works normally. Alternatively, walk to the shuttle bus stop for ฿150 transfers to Krabi Town, then Grab from Krabi Town bus terminal (where ride-share works). For round-trip day tours (Tiger Cave, Hot Springs, Emerald Pool), pre-book an honest driver via your hotel at ฿1,500–฿2,500 for the full day rather than negotiating per-ride with the cartel."),
        ("Is Railay Beach safe and how do I get there?",
         "Railay is a small peninsula reachable only by longtail boat from Ao Nang beach pier (฿100 per person each way, 10-minute ride, boats leave when they reach 8 passengers). It's completely scam-free — the peninsula has only a few resorts, no taxi access, and no motorized transport. Railay is a strong alternative base to Ao Nang if you want to avoid the taxi mafia and restaurant tourist-pricing issues. The main beach (West Railay) is public and free; the rock climbing and Phranang Cave areas are the main draws."),
    ],
    "Koh Samui": [
        ("Is Koh Samui safe for tourists?",
         "Koh Samui is physically safe — violent crime against tourists is rare — but it has one of Thailand's most aggressive taxi mafia operations and a well-documented rental-car/scooter scam scene. Named scam operators like 'All Way Rent a Car' and 'Hakunarent' are flagged in 2025 r/kohsamui threads, and ride-share drivers are blocked from airport and pier pickups. Chaweng and Lamai are safe to walk day and night; the risks are financial. Save Tourist Police 1155 before arrival."),
        ("What is the most common scam in Koh Samui?",
         "The airport taxi mafia is the most systemic — drivers quote 2–3x the Grab rate and physically block ride-share pickups within the airport perimeter (r/kohsamui 'Taxi Mafia Shock'). Car and scooter rental 'damage' or 'smoking fee' shakedowns are the second most common, with named shops 'All Way Rent a Car' (฿3,000 false smoking fee, 2025) and 'Hakunarent' both flagged on Reddit. Booking booth scams via 'NCK Travel' and 'Funny Day Tours' round out the top patterns."),
        ("How do I avoid the Samui taxi mafia?",
         "Walk 500 meters outside the airport perimeter before requesting Grab or Bolt — this puts you outside the cartel zone where drivers will accept pickups. From Nathon Pier, walk 5 minutes inland before calling a ride-share. Benchmark Grab fares from USM: → Chaweng ฿250, → Bophut ฿300, → Lamai ฿400, → Nathon ฿500. Use InDrive as a backup when Grab drivers cancel. Pre-book hotel transfers via your accommodation for arrivals."),
        ("Is it safe to rent a car or scooter on Koh Samui?",
         "Rent cars from major-brand airport counters (Budget, Avis, Thrifty) — not Chaweng/Lamai storefronts. For scooters, never leave your original passport; offer ฿3,000–฿5,000 cash deposit plus photocopy, walk away from shops that refuse. Photograph every panel with timestamps before driving off. Cat Motors Samui and Mr Ting Big Bike are community-recommended. The 'All Way Rent a Car' smoking-fee scam is the named warning; check r/kohsamui for current flagged shops."),
        ("What's the best neighborhood to stay in Koh Samui?",
         "Chaweng is the main nightlife/beach hub with the most amenities and highest scam exposure. Bophut's Fisherman's Village is quieter, more authentic, and has a more legitimate restaurant scene. Lamai is popular with families and long-term visitors — calmer than Chaweng. Choeng Mon in the north offers luxury resorts and calm beaches. Avoid the Soi Green Mango go-go bar immediate area after midnight if you want to avoid the lady-drink scam escalation."),
    ],
    "Koh Phangan": [
        ("Is Koh Phangan safe for tourists?",
         "Koh Phangan is safe physically — violent crime against tourists is uncommon and the island is overwhelmingly welcoming outside the Full Moon week. The primary risk is the drug scene: 2025 saw active police stings with Israeli soldiers, Russian operators, and Chinese dealers all prosecuted (Khaosod English / Bangkok Post coverage October–November 2025). Do not buy, carry, or consume recreational drugs — sting operations are real and extortion (฿30,000+ cash to avoid jail) is routine. Save Tourist Police 1155 before arrival."),
        ("What is the most common scam in Koh Phangan?",
         "Drug-sting cash extortion is the highest-dollar scam — buyers are stopped after transactions, substances 'discovered' on them, and ฿30,000–฿100,000 cash demanded to avoid formal charges. The ฿25,000 beach-smoking fine shakedown (r/ThailandTourism 2025) is a parallel pattern. Scooter rental passport-hostage damage (฿11K–฿13K per scooter for friends in the 2024 r/ThailandTourism 'Ko Pha Ngan' incident) and cannabis dispensary price gouging (฿3,000/gram with fabricated 70% THC claims) round out the top patterns."),
        ("How do I get to Koh Phangan?",
         "Ferries from Koh Samui (Nathon or Maenam piers) take 30–90 minutes to Thong Sala and cost ฿250–฿400. Lomprayah, Seatran Discovery, and Raja Ferry are the main operators. From Surat Thani, overnight boats (Raja Ferry) and Lomprayah combo-bus-ferry services work — book via 12go.asia. At Thong Sala Pier, walk 200m inland before calling a songthaew to avoid pier-cartel pricing."),
        ("What should I know about the Full Moon Party?",
         "The Full Moon Party at Haad Rin draws 30,000+ tourists per month. The party itself is safe for most attendees, but two risks dominate: drug stings (undercover police target beach sellers AND buyers, then extort cash) and drink-spiking (bucket cocktails are the delivery vehicle). Leave all cards and most cash at your accommodation; carry ฿2,000 and one card. Travel in groups. Pre-book Haad Rin accommodation 6+ weeks ahead — last-minute bookings are scam-prone with forced cancellations."),
        ("Is cannabis legal in Thailand right now?",
         "Cannabis was decriminalized in 2022 then partially re-criminalized in 2024–2025 — it now requires a medical prescription in theory, though enforcement on tourist-serving dispensaries is inconsistent. Street cannabis and beach sellers are fully illegal and tied to police sting operations. Dispensary pricing on Phangan is 3–5x the Bangkok rate; claims of 70%+ THC are scams (biological max is 34%). Public consumption (beach, street) can result in ฿25,000+ fines — technically illegal even when dispensaries sell product."),
    ],
    "Koh Phi Phi": [
        ("Is Koh Phi Phi safe for tourists?",
         "Koh Phi Phi is generally safe — violent crime against tourists is uncommon — but 2025 saw multiple alcohol-related tourist deaths (French tourist died at Phi Phi police station after heavy drinking in July 2025; Canadian tourist drowned in November 2025). A March 2025 boat fire off the route left a British tourist missing (BBC). The primary tourist risks are drink-spiking at bucket-cocktail bars, Maya Bay park fee double-billing, and ferry ticket destination switches. Save Tourist Police 1155 before arrival."),
        ("What is the most common scam in Koh Phi Phi?",
         "The Maya Bay national park fee double-bill is the most common — operators bill the ฿400 foreigner fee separately at the dock even when already included in the tour price (r/ThailandTourism 'So what's the deal with the Maya bay entrance'). Ferry ticket destination switches (Urip Ferry routing tourists to Krabi Town instead of Ao Nang) are second (r/ThailandTourism 'Urip Ferry Phi Phi- Ao Nang Rip Off'). Bucket-cocktail drink-spiking at Loh Dalum and Tonsai bars is the highest-damage tourist risk."),
        ("How do I get to Koh Phi Phi?",
         "Ferries from Phuket (Rassada Pier), Krabi Town (Klong Chilad Pier), and Ao Nang run daily. Chao Koh Ferry, Songserm, and Phi Phi Cruiser are legitimate operators; book directly at their official sites for ฿400–฿500 one-way. Booth middlemen in Ao Nang and Patong charge ฿1,200+ for the same ticket. Confirm destination precisely in writing: 'Ao Nang beach pier' not just 'Krabi.' During monsoon (May–October), take larger ferries over speedboats and check Windy for wave conditions before boarding."),
        ("Are Maya Bay and Phi Phi tours worth it?",
         "Maya Bay (from 'The Beach') reopened in 2022 after environmental rehab and is genuinely spectacular but heavily crowded. Book tours on Klook or 12go.asia with park fee listed as 'included' to avoid double-billing. Bring ฿400 cash per person as backup. For Phi Phi Island itself, 2 nights gives you time to hike Phi Phi Viewpoint, snorkel Bamboo Island, and do a long-tail tour. Pay by credit card for chargeback leverage on tour disputes."),
        ("What should I know about nightlife on Phi Phi?",
         "Loh Dalum Beach and Tonsai Village have Phi Phi's main party scene. Do NOT accept bucket cocktails — these are the documented vehicle for drink-spiking (2025 r/travel 'I fell for a tourist scam and feel really stupid'). Order bottled beer or watch-your-drink cocktails. Phi Phi is walk-only (no cars), so Grab is not a rescue option at night — travel in groups and keep most cash/cards at accommodation. Khaosod English July 2025 and Thaiger November 2025 both reported alcohol-related tourist deaths on the island."),
    ],
    "Koh Tao": [
        ("Is Koh Tao safe for tourists?",
         "Koh Tao has a complicated reputation. The island is Thailand's most popular dive certification destination and millions visit safely each year. But it also carries the nickname 'Murder Island' from a decade of unexplained tourist deaths (David Miller and Hannah Witheridge 2014, Elise Dallemagne 2017, multiple 2024–2025 cases including a November 2025 sexual assault attempt on a Canadian tourist). The practical risk to most visitors is low, but travel with a buddy, stay on the Sairee main strip after dark, and don't escalate disputes with local businesses. Save Tourist Police 1155."),
        ("What is the most common scam in Koh Tao?",
         "Dive shop Open Water pricing opacity is the most common — sidewalk prices of ฿9,500 always exclude textbook (฿500), mask rental (฿300), cert card (฿400), and boat fees (฿200/day). Real total: ฿11,500–฿12,500. Beach entrance fees (฿50–฿200 at Freedom Beach, Aow Leuk, Tanote) are technically illegal but widespread. Scooter rental passport-hostage damage (฿20K hostage demands documented back to the 1990s per r/ThailandTourism 'Scratched the bike') remains active."),
        ("Is Koh Tao worth diving?",
         "Yes, with the right shop. Koh Tao is one of the world's cheapest places to get PADI Open Water certified at ฿11,500–฿12,500 total. Book with verified long-term shops: Black Turtle Dive, Big Blue Diving, Koh Tao Divers, Crystal Dive — not cut-rate storefronts. Insist on pool/confined-water practice before open-water dives; 2025 r/scubadiving threads flagged safety issues at shops compressing certification into 2–3 days with minimal skill practice. Post-certification 'fun dives' should be ฿1,000–฿1,400 per dive including equipment."),
        ("Should I rent a scooter on Koh Tao?",
         "Consider NOT renting. Koh Tao's hilly unpaved roads are notoriously dangerous — multiple tourist deaths are documented (r/Thailand 'Mystery as Irish backpacker, 21, is found dead' includes 'Driving a scooter on Koh Tao was imo the most dangerous places of all'). If you do rent, never leave original passport; offer ฿5,000–฿10,000 cash deposit. Park the scooter at the shop outside business hours to prevent fake-damage shakedowns on return (community workaround). Walk or use songthaews within Sairee; the island is small."),
        ("How do I get to Koh Tao?",
         "Ferries from Koh Phangan (Thong Sala) take 1 hour; from Koh Samui (Nathon) 2 hours. Lomprayah, Seatran Discovery, and Songserm are main operators — book at their official sites for ฿600–฿900. From Bangkok, combo overnight bus + ferry via Lomprayah takes 10–12 hours for ฿1,500. Book on 12go.asia for legitimate operators with refunds; avoid booth middlemen. During monsoon (May–October), check conditions and take the larger slower ferries over high-speed catamarans."),
    ],
    "Ayutthaya": [
        ("Is Ayutthaya safe for tourists?",
         "Ayutthaya is generally safe — violent crime against tourists is rare and the UNESCO-listed historic park is walkable and well-populated. The main tourist risks are financial: fake 'SRT officials' at Bangkok Hua Lamphong Station routing you to ฿1,500 minibus 'packages' instead of the ฿20 train, train station 'mafia' tuk-tuks quoting per-person rather than per-vehicle, and commission-shop detours disguised as temple tours. Save Tourist Police 1155."),
        ("What is the most common scam in Ayutthaya?",
         "The 'mafia tuk-tuk' intercept at Ayutthaya Railway Station is the most common — drivers quote ฿800 per person for a 'temple tour' when the fair rate is ฿200–฿300 per HOUR for the whole vehicle. At Bangkok Hua Lamphong, fake 'SRT officials' in fake uniforms route tourists to 'VIP minibus' packages (r/ThailandTourism 'Scammer alert at Bangkok Station' 2025). The fake 'Tourist Information Centre' package-sale scam (฿3,500 for what should cost ฿200) is the third most common."),
        ("How do I get to Ayutthaya from Bangkok?",
         "The cheapest option is the SRT 3rd-class train from Hua Lamphong Station at ฿20 one-way, 2 hours. Buy tickets at the official counter inside the station — not from anyone in 'uniform' outside. Alternative: the ฿60 minivan from Mo Chit bus terminal takes 1.5 hours. A private Grab from Bangkok to Ayutthaya runs ฿1,200–฿1,500. Avoid Khao San Road 'combo day trips' that bundle Ayutthaya with floating markets — structurally impossible to do well in one day."),
        ("Should I hire a tuk-tuk for Ayutthaya temple hopping?",
         "Yes, but at ฿200–฿300 per HOUR for the whole vehicle — not per person. 4–6 hours at ฿800–฿1,200 total for a group covers the main temples (Wat Mahathat, Wat Phra Si Sanphet, Wat Chaiwatthanaram, Wat Yai Chai Mongkhon). At Ayutthaya Railway Station, walk past the waiting 'mafia' tuk-tuks and use Grab/InDrive, then flag a circulating tuk-tuk at your first temple. Alternative: rent a bicycle (฿50/day) — Ayutthaya is bike-friendly and most ruins are within 5 km."),
        ("Do I need to ride elephants in Ayutthaya?",
         "No — and you shouldn't. Ayutthaya's elephant ride operators use bullhook-trained elephants, confine them overnight, and run 'first price' upsells where a ฿400 ride becomes ฿1,000+ mid-route (r/ThailandTourism 'Ayutthaya'). For an ethical elephant experience, visit Elephant Nature Park or BEES Sanctuary in Chiang Mai instead. In Ayutthaya, rent a bicycle and focus on the ruins — the UNESCO park has enough for a full day."),
    ],
    "Hua Hin": [
        ("Is Hua Hin safe for tourists?",
         "Hua Hin is generally safe — it's a Thai royal resort town and violent crime against tourists is rare. But it has a documented aggressive taxi mafia (2025 incidents included eggs thrown at Grab cars, making the news per r/ThailandTourism 'Hua Hin Taxi Threat Incident WARNING'), active strip-club bill extortion on Soi Bintabaht, and structural dual-pricing at attractions and restaurants. Beach and town are walkable day and night. Save Tourist Police 1155."),
        ("What is the most common scam in Hua Hin?",
         "Taxi mafia overcharging + intimidation at the Hua Hin Railway Station and Market Village is the most common — tuk-tuks quote ฿300–฿500 for trips Grab would charge ฿80–฿150 for, and ride-share drivers have been physically attacked. Restaurant/attraction dual pricing (English menu at 2x–3x Thai menu price, especially at Hua Hin Zoo and beachfront restaurants per r/ThailandTourism 'Thai student researching tourist scams') is second most common."),
        ("How do I get to Hua Hin from Bangkok?",
         "The cheapest option is the SRT train from Hua Lamphong Station at ฿50–฿300 depending on class, 4 hours. The Bell Travel Service van from Suvarnabhumi Airport goes directly to Hua Hin for ฿305, 3.5 hours. A private Grab runs ฿2,500–฿3,000. Lomprayah combo-bus services from Bangkok connect to Hua Hin as part of southern-Thailand routes. Most visitors arrive by road — the train is slower but scenic."),
        ("How do I avoid the Hua Hin taxi mafia?",
         "Walk 200–300 meters away from the Hua Hin Railway Station and Market Village before requesting Grab — the cartel operates within specific perimeters. Pre-book hotel transfers via your accommodation for arrivals (฿300–฿500 fixed). Benchmark Grab fares: town center → Khao Takiab ฿100, → railway station ฿80, → Cicada Market ฿120. Report egg-throwing or threatening tuk-tuk incidents to Tourist Police 1155 with photos — 2025 incidents have produced police response."),
        ("What should I know about Hua Hin nightlife?",
         "Soi Bintabaht (sometimes 'Soi Bindabatt') is Hua Hin's main bar strip. Most bars are low-risk but a handful run the bill-extortion scam: hostesses sit down uninvited, drinks appear, final bill is ฿15,000+ with disputed 'bar fine' and 'service' lines. Pay per drink at the bar, not via a tab. Carry ฿2,000 cash only, leave cards at hotel. Monsoon Bar, Hilton Hotel rooftop, and El Murphy's Irish Pub are posted-price legitimate alternatives."),
    ],
    "Chiang Mai": [
        ("Is Chiang Mai safe for tourists?",
         "Chiang Mai is one of Thailand's safer major destinations — violent crime against tourists is rare and the Old City, Nimman, and Santitham neighborhoods are safe to walk day and night. The main tourist risks are financial: bar bill extortion on Sri Don Chai Road (the July 2025 Diamond Karaoke assault is the most prominent recent case), scooter rental damage scams using your passport as leverage, and tuk-tuk gem shop detours. Chiang Mai welcomed 9.35 million tourists January–October 2025 per Chiang Mai Tourism and the overwhelming majority report no incidents. Save the Tourist Police number 1155 before you go."),
        ("What is the most common scam in Chiang Mai?",
         "The tuk-tuk 'closed temple' gem shop tour is Chiang Mai's oldest and most common scam — a driver near Tha Phae Gate claims your temple destination is closed and offers a cheap ride to an 'alternative' that ends at a gem, jade, or tailor shop where you're pressured to buy. The scooter rental damage scam (passport held hostage, 10,000–13,500 baht demanded for cosmetic scratches) is the second most common. For financial damage, the Sri Don Chai Road karaoke bar extortion pattern is the most severe — bills of 20,000–160,000 baht with physical intimidation."),
        ("How do I get from Chiang Mai Airport to the Old City?",
         "Chiang Mai International Airport (CNX) is 4 km from the Old City — the cheapest option is the Airport Shuttle bus (฿40, 20 minutes, drops at Tha Phae Gate). A Grab or Bolt to the Old City costs ฿120–฿180 via app — pick up from the designated frontage road just outside Terminal 1 (not the inner taxi rank, which is controlled by the taxi union). Metered airport taxis from the official counter inside arrivals cost ฿150–฿200. Avoid any driver who approaches you offering a 'flat rate' — the airport taxi rank has posted fixed fares and your best protection is requesting the meter or using Grab."),
        ("Are tuk-tuks and songthaews safe in Chiang Mai?",
         "The red songthaew (rod daeng) is Chiang Mai's iconic shared-taxi truck and is safe and mostly honest — standard rate is ฿30–฿50 per person for a shared ride within the city. The scam is being quoted the 'private charter' rate (฿200–฿300) without being told, or drivers at tourist hotels refusing to share the vehicle. Flag a circulating songthaew from one block away from major hotels to get local pricing. For tuk-tuks, never accept a 'tour' under ฿50 — that's the gem shop commission setup. Use Grab or Bolt for transparent fares whenever possible."),
        ("What neighborhoods are best in Chiang Mai?",
         "The Old City (inside the moat) is the most atmospheric base — walkable access to Wat Chedi Luang, Wat Phra Singh, Sunday Walking Street, and the best cafés. Nimmanhaemin ('Nimman') is Chiang Mai's digital nomad and trendy food/cocktail district — great for longer stays, with One Nimman and the Think Park area as focal points. Santitham (north of the moat) is the local neighborhood with authentic food and lower prices. The Night Bazaar / Chang Klan Road area offers shopping but has the highest concentration of scam venues — Sri Don Chai Road especially — so walk through, don't stay there. Wualai Road (south of the moat) has the Saturday Walking Street and legitimate silver shops."),
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
         "Yes — Turkey is a secular country and alcohol is legal and widely available in Istanbul. Raki (anise spirit) is the traditional drink. The main practical concern is price: tourist-area bars charge significantly more than local meyhane (tavern) venues. Avoid any bar that doesn't have a visible menu with prices — this is where the bar trap scam starts. Alcohol is not served in conservative neighborhoods like Fatih."),
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
}

def danger_badge(level):
    level = level.lower()
    if level == "high":
        return '<span class="danger-badge danger-high">⚠️ High</span>'
    elif level == "medium":
        return '<span class="danger-badge danger-medium">🔶 Medium</span>'
    else:
        return '<span class="danger-badge danger-low">🟡 Low</span>'

def generate_scam_cards(scams):
    html = ""
    for i, scam in enumerate(scams, 1):
        red_flags_html = "\n".join(f"                    <li>{rf}</li>" for rf in scam.get("red_flags", []))
        avoid_html = "\n".join(f"                    <li>{av}</li>" for av in scam.get("how_to_avoid", []))
        # Support multi-paragraph stories (paragraphs separated by blank lines)
        paragraphs = [p.strip() for p in scam['story'].split("\n\n") if p.strip()]
        story_html = "\n        ".join(f'<p class="scam-story">{p}</p>' for p in paragraphs)
        html += f"""
    <!-- Scam {i} -->
    <div class="scam-card">
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
    return html

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

def generate_page(city_data):
    city = city_data["city"]
    country = city_data["country"]
    flag = city_data.get("flag", "🌍")
    scams = city_data["scams"]
    slug = CITY_SLUGS[city]
    n = len(scams)
    
    em = EMERGENCY_INFO.get(country, EMERGENCY_INFO["United Kingdom"])
    safety_tips = SAFETY_TIPS.get(city, [
        "Keep phones and valuables in secure pockets when in crowded areas",
        "Use only licensed taxis or app-based ride services",
        "Book tours and tickets through verified operators with online reviews",
        "Keep a copy of your passport separate from the original",
    ])
    faqs = FAQS.get(city, [])
    
    safety_tips_html = "\n".join(f"            <li>{tip}</li>" for tip in safety_tips)
    
    scam_cards = generate_scam_cards(scams)
    
    faq_schema_items = generate_faq_schema(city, faqs)
    
    faq_html = generate_faq_html(faqs)
    
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
                "datePublished": "2026-03-29",
                "dateModified": "2026-03-29",
                "author": {"@type": "Organization", "name": "tabiji.ai"},
                "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/"}
            },
            {
                "@type": "FAQPage",
                "mainEntity": faq_schema_items
            }
        ]
    }
    
    schema_json = json.dumps(schema, indent=4, ensure_ascii=False)
    
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
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{n} Tourist Scams in {city} (2026)">
    <meta name="twitter:description" content="Real scams, real stories, real advice. From Reddit travelers who got caught out in {city}.">
    <meta name="twitter:image" content="https://img.tabiji.ai/scams-{slug}-og.jpg">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai/scams/{slug}/">
    <link rel="stylesheet" href="/assets/shared-shell.css">

    <script type="application/ld+json">
    {schema_json}
    </script>

    <style>
        :root {{
            --indigo: #2D3A5C;
            --indigo-light: #3D4E7A;
            --warm-cream: #F5F0E8;
            --sand: #E8DFD0;
            --earth: #8B7355;
            --terracotta: #C4704B;
            --white: #FEFCF9;
            --text: #2C2419;
            --text-muted: #6B5D4F;
            --danger: #DC2626;
            --danger-bg: #FEF2F2;
            --warning: #F59E0B;
            --warning-bg: #FFFBEB;
            --low: #16A34A;
            --low-bg: #F0FDF4;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            color: var(--text);
            background: var(--white);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        /* Hero */
        .hero {{
            background: var(--indigo);
            color: white;
            padding: 5rem 2rem 3rem;
            text-align: center;
        }}
        .hero-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.15);
            color: rgba(255,255,255,0.9);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.35rem 0.9rem;
            border-radius: 99px;
            margin-bottom: 1.25rem;
        }}
        .hero h1 {{
            font-size: clamp(1.8rem, 5vw, 3rem);
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }}
        .hero p {{
            font-size: 1.1rem;
            color: rgba(255,255,255,0.8);
            max-width: 600px;
            margin: 0 auto 1.5rem;
        }}
        .hero-meta {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            font-size: 0.85rem;
            color: rgba(255,255,255,0.65);
        }}
        .hero-meta span {{ display: flex; align-items: center; gap: 0.35rem; }}

        /* Breadcrumb */
        .breadcrumb {{
            background: var(--sand);
            padding: 0.6rem 2rem;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        .breadcrumb a {{ color: var(--text-muted); text-decoration: none; }}
        .breadcrumb a:hover {{ color: var(--indigo); }}
        .breadcrumb span {{ margin: 0 0.4rem; }}

        /* Content */
        .content {{
            max-width: 860px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }}

        /* Safety box */
        .safety-box {{
            background: var(--warning-bg);
            border: 1.5px solid var(--warning);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2.5rem;
        }}
        .safety-box h2 {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .safety-box ul {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .safety-box li {{
            font-size: 0.92rem;
            color: var(--text);
            display: flex;
            gap: 0.5rem;
        }}
        .safety-box li::before {{ content: "✓"; color: var(--low); font-weight: 700; flex-shrink: 0; }}

        /* Section heading */
        .section-heading {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--indigo);
            margin-bottom: 1.25rem;
            padding-bottom: 0.6rem;
            border-bottom: 2px solid var(--sand);
        }}

        /* Scam card */
        .scam-card {{
            background: var(--white);
            border: 1.5px solid var(--sand);
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
            transition: box-shadow 0.2s;
        }}
        .scam-card:hover {{ box-shadow: 0 4px 20px rgba(45,58,92,0.08); }}

        .scam-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.9rem;
            flex-wrap: wrap;
        }}
        .scam-number {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .scam-title {{
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--indigo);
            margin-top: 0.2rem;
        }}
        .danger-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.65rem;
            border-radius: 99px;
            white-space: nowrap;
            flex-shrink: 0;
        }}
        .danger-high {{ background: var(--danger-bg); color: var(--danger); }}
        .danger-medium {{ background: var(--warning-bg); color: #B45309; }}
        .danger-low {{ background: var(--low-bg); color: var(--low); }}

        .scam-location {{
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-bottom: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}
        .scam-story {{
            font-size: 0.97rem;
            color: var(--text);
            margin-bottom: 1rem;
            line-height: 1.7;
        }}
        .scam-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}
        @media (max-width: 600px) {{
            .scam-details {{ grid-template-columns: 1fr; }}
        }}
        .detail-block h4 {{
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}
        .detail-block ul {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}
        .detail-block li {{
            font-size: 0.87rem;
            color: var(--text);
            display: flex;
            gap: 0.5rem;
        }}
        .red-flags li::before {{ content: "🚩"; flex-shrink: 0; }}
        .avoid li::before {{ content: "✓"; color: var(--low); font-weight: 700; flex-shrink: 0; }}

        /* What to do section */
        .action-section {{
            background: var(--indigo);
            color: white;
            border-radius: 14px;
            padding: 2rem;
            margin: 2.5rem 0;
        }}
        .action-section h2 {{
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 1.25rem;
        }}
        .action-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
        }}
        .action-item {{
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 1rem;
        }}
        .action-item h3 {{
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .action-item p {{
            font-size: 0.85rem;
            color: rgba(255,255,255,0.8);
            line-height: 1.5;
        }}
        .action-item a {{ color: #93C5FD; }}

        /* FAQ */
        .faq-section {{ margin: 2.5rem 0; }}
        .faq-item {{
            border: 1.5px solid var(--sand);
            border-radius: 10px;
            margin-bottom: 0.75rem;
            overflow: hidden;
        }}
        .faq-q {{
            width: 100%;
            background: none;
            border: none;
            padding: 1rem 1.25rem;
            text-align: left;
            font-size: 0.97rem;
            font-weight: 700;
            color: var(--text);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .faq-q:hover {{ background: var(--warm-cream); }}
        .faq-arrow {{ font-size: 0.9rem; transition: transform 0.2s; }}
        .faq-item.open .faq-arrow {{ transform: rotate(180deg); }}
        .faq-a {{
            display: none;
            padding: 0 1.25rem 1rem;
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.65;
        }}
        .faq-item.open .faq-a {{ display: block; }}

        /* CTA */
        .cta-box {{
            background: var(--warm-cream);
            border: 1.5px solid var(--sand);
            border-radius: 14px;
            padding: 2rem;
            text-align: center;
            margin: 2.5rem 0;
        }}
        .cta-box h2 {{
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--indigo);
            margin-bottom: 0.5rem;
        }}
        .cta-box p {{
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.25rem;
        }}
        .cta-btn {{
            display: inline-block;
            background: var(--terracotta);
            color: white;
            padding: 0.8rem 1.75rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.97rem;
            text-decoration: none;
            transition: opacity 0.2s;
        }}
        .cta-btn:hover {{ opacity: 0.88; }}
    </style>
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
                <a href="/spin/">🌎 Spin the Globe</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/owl/">🧭 Tabiji Travel Agency</a>
                <a href="/trends/">📊 Travel Trends</a>
                <a href="/alerts/">🚨 Travel Alerts</a>
                <a href="/scams/">🚨 Tourist Scams</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/itineraries/">Itineraries</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>

<div class="breadcrumb">
    <a href="/">Home</a><span>›</span><a href="/scams/">Scams</a><span>›</span>{city}
</div>

<div class="hero">
    <div class="hero-badge">🚨 Scam Guide · 2026</div>
    <h1>{n} Tourist Scams in {city}</h1>
    <p>Real stories from Reddit travelers. Know what to watch for before you arrive.</p>
    <div class="hero-meta">
        <span>📍 {city}, {country}</span>
        <span>📅 Updated March 2026</span>
        <span>💬 {n} scams documented</span>
        <span>⭐ Reddit-sourced & verified</span>
    </div>
</div>

<div class="content">

    <div class="safety-box">
        <h2>⚡ Quick Safety Tips</h2>
        <ul>
{safety_tips_html}
        </ul>
    </div>

    <h2 class="section-heading">The {n} Scams</h2>
{scam_cards}

    <!-- What to do -->
    <div class="action-section">
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

    <!-- FAQ -->
    <div class="faq-section">
        <h2 class="section-heading">Frequently Asked Questions</h2>
{faq_html}
    </div>

    <!-- CTA -->
    <div class="cta-box">
        <h2>Ready to Plan Your {city} Trip?</h2>
        <p>Now you know what to watch for. Get a custom {city} itinerary with local tips, hidden spots, and restaurant picks — free.</p>
        <a href="/plan" class="cta-btn">Plan Your {city} Trip →</a>
    </div>

</div>

<footer>
    <p>© 2026 tabiji.ai · <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> · <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> · <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> · <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> · <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>

<script defer src="/assets/shared-shell.js"></script>
</body>
</html>"""
    return html


def main():
    base_dir = os.path.expanduser("~/tabiji/scams")
    
    # Load all batch files
    all_cities = []
    batch_files = sorted(glob.glob(os.path.join(base_dir, "research", "batch*.json")))
    for path in batch_files:
        with open(path) as f:
            data = json.load(f)
            all_cities.extend(data)
    
    print(f"Loaded {len(all_cities)} cities total")
    
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
        
        html = generate_page(city_data)
        with open(out_path, "w") as f:
            f.write(html)
        
        print(f"  ✅ {city} → {slug}/index.html ({len(city_data['scams'])} scams, {len(html)} chars)")
        built.append((city, slug, len(city_data['scams'])))
    
    print(f"\nBuilt {len(built)} pages:")
    for city, slug, n in built:
        print(f"  - {city} ({n} scams) → /scams/{slug}/")
    
    return built

if __name__ == "__main__":
    main()
