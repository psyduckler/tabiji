#!/usr/bin/env python3
"""Generate scam pages for all cities based on Barcelona template."""
import json
import os
import glob
from collections import defaultdict

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
    "Langkawi": "langkawi",
    "Lombok": "lombok",
    "Luang Prabang": "luang-prabang",
    "Lyon": "lyon",
    "Maui": "maui",
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
    "Sapa": "sapa",
    "Siargao": "siargao",
    "Sorrento": "sorrento",
    "Stone Town": "stone-town",
    "Ubud": "ubud",
    "Udaipur": "udaipur",
    "Valparaíso": "valparaiso",
    "Varanasi": "varanasi",
    "Yogyakarta": "yogyakarta",
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
        "If a tuk-tuk driver offers a sightseeing tour for 20 baht, it's a gem store commission scam — avoid entirely",
        "Always insist the taxi meter is running before the ride starts — 'meter broken' means find another cab",
        "Grand Palace is never closed — anyone who tells you it is and offers an alternative tour is a scammer",
        "Use the BTS Skytrain or MRT for most travel — it's fast, air-conditioned, and eliminates taxi negotiation entirely",
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
        "Never accept a tuk-tuk or taxi ride without agreeing on the price first — meters don't exist and prices triple for tourists who don't negotiate",
        "At Patong Beach, jet ski operators will claim you damaged the equipment and demand thousands of baht — avoid jet ski rentals from beach touts entirely",
        "Book boat tours to Phi Phi and James Bond Island through your hotel — street-booked tours often use unsafe boats with no insurance",
        "Ignore gem shop tours offered by tuk-tuk drivers — the 'government gem sale' is Thailand's most persistent tourist scam",
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
        "Keep your valuables in front-facing, zipped pockets or a crossbody bag worn across your chest; never use back pockets or leave bags hanging on chairs in Barcelona.",
        "Carry a photocopy of your passport and leave the original locked in your hotel safe; Spanish police accept copies for routine ID checks.",
        "Avoid using ATMs on the street or in isolated areas; use machines inside bank branches during business hours and always cover the keypad when entering your PIN.",
        "Download the Barcelona Mossos d'Esquadra app or save the tourist police number (La Rambla 43 station) in your phone before you arrive.",
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
        "Use the BiTaksi app for taxis with tracked routes and pre-estimated fares rather than hailing cabs on the street, especially from the airport",
        "Photograph menus and prices before ordering at any restaurant, and check your bill line by line; do not hesitate to dispute incorrect charges",
        "Use ATMs inside bank branches and enable real-time transaction alerts on your banking app to catch unauthorized charges immediately",
        "Keep copies of your passport in your hotel safe and carry only a photocopy; store emergency numbers including the tourist police (155) in your phone",
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
    "Tenerife": [
        "Never accept scratch cards or 'prize' offers from street promoters — they're always the opening move of a timeshare pressure sale",
        "Verify every credit card transaction amount on the terminal screen before entering your PIN — some tourist-area shops add extra zeros to the charge",
        "Photograph your rental car thoroughly at pickup and return, and decline counter insurance only if you've confirmed your credit card coverage in advance",
        "Keep your phone secured in a zipped pocket on Veronica's Strip and never hand it to a stranger, no matter how plausible the request sounds",
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
         "Barcelona is generally safe and violent crime against tourists is rare. The primary risk is petty theft and pickpocketing, which remains the most reported crime in the city. In 2023, pickpocketing accounted for 48.1 percent of all crimes. The risk is concentrated in specific areas like La Rambla, the metro system, Barceloneta Beach, and the Gothic Quarter. By taking basic precautions such as wearing a crossbody bag, avoiding back pockets, and staying alert in crowds, most visitors have a trouble-free experience."),
        ("What are the worst areas for pickpockets in Barcelona?",
         "The highest-risk areas are La Rambla (the entire pedestrian boulevard), the metro system (especially lines L1, L3, and L4 at stations like Liceu, Passeig de Gràcia, and Plaça de Catalunya), Barceloneta Beach, the Gothic Quarter, Park Güell, and the area around Sagrada Família. Pickpockets target crowds, so anywhere large groups gather, including concerts, festivals, and street performer circles, carries elevated risk."),
        ("What should I do if I get pickpocketed in Barcelona?",
         "File a police report (denuncia) immediately. The most convenient station for tourists is the dedicated tourist police office at La Rambla 43, or the Mossos d'Esquadra station at Carrer Nou de la Rambla 76-80. You can also start a report by calling 902 102 112 (English-speaking line, available seven languages) and must confirm it in person within 48 hours. Cancel your cards immediately through your banking app. You will need the police report number (denuncia) for travel insurance claims."),
        ("Are taxis safe in Barcelona?",
         "Official Barcelona taxis are yellow and black with a meter and a visible license. They are generally safe and reliable. Always ensure the meter is running at the start of the trip. From the airport, there are fixed rates to the city center (approximately 39 euros). Avoid unmarked cars or anyone soliciting rides at the airport or train station. Uber operates in Barcelona as an alternative with upfront pricing."),
        ("Is the Barcelona metro safe at night?",
         "The metro is generally safe but pickpockets operate during all hours, with peak risk during crowded periods. At night, be particularly cautious on the last trains when carriages may be less crowded but also less supervised. Avoid empty carriages and stay near other passengers. Keep valuables secured and be alert during boarding and exiting, which is when most thefts occur. The metro closes at midnight on weekdays and runs all night on Saturdays and the eve of public holidays."),
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
         "Buying carpets can be safe if you use reputable, review-verified dealers and have any purchase independently appraised. Never buy from a shop you were led to by a street tout. Pay by credit card for dispute protection, and be extremely skeptical of claims about age, materials, or origin without independent certification."),
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
    "Tenerife": [
        ("Is Tenerife safe for tourists?",
         "Tenerife is generally safe. Violent crime against tourists is very rare. The main risks are tourist-targeted scams in the south coast resort areas — timeshare hustles, electronics shop fraud, taxi overcharging, and phone theft on Veronica's Strip. The north of the island (Puerto de la Cruz, La Laguna) has fewer tourist scams."),
        ("What are the biggest scams in Playa de las Américas?",
         "The south coast resort area including Playa de las Américas, Los Cristianos, and Costa Adeje is Tenerife's scam hotspot. The main ones are timeshare scratch card traps, electronics shops that add extra zeros to credit card charges, fake police wallet inspections late at night, and phone theft on Veronica's Strip. Stay alert and you'll be fine."),
        ("Should I rent a car in Tenerife?",
         "Yes, a rental car is the best way to explore Tenerife's stunning north coast, Teide National Park, and the Anaga Mountains. Just book with reputable companies like Cicar or AutoReisen, photograph the car thoroughly at pickup, and decline counter insurance only if your credit card already covers rental car damage. Avoid budget operators at remote off-airport lots."),
        ("How do I report a scam in Tenerife?",
         "Request a 'Hoja de Reclamaciones' (official complaint form) — all Spanish businesses are legally required to provide one. File it with the local consumer protection office. For serious fraud, report to the Guardia Civil (062) or the Policía Nacional (091). For immediate emergencies, call 112."),
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
}

def danger_badge(level):
    level = level.lower()
    if level == "high":
        return '<span class="danger-badge danger-high">⚠️ High</span>'
    elif level == "medium":
        return '<span class="danger-badge danger-medium">🔶 Medium</span>'
    else:
        return '<span class="danger-badge danger-low">🟢 Low</span>'

def generate_scam_cards(scams):
    html = ""
    for i, scam in enumerate(scams, 1):
        red_flags_html = "\n".join(f"                    <li>{rf}</li>" for rf in scam.get("red_flags", []))
        avoid_html = "\n".join(f"                    <li>{av}</li>" for av in scam.get("how_to_avoid", []))
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
        <p class="scam-story">{scam['story']}</p>
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
    
    scam_cards = generate_scam_cards(scams)
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
                "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/"},
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
    takeaway_transport = "Only use official taxis with government-set rates — confirm the fare before getting in" if city in no_rideshare_cities else "Use app-based ride services (Uber, Grab, Bolt) instead of street taxis"
    takeaway_avoid = f"Never accept unsolicited offers from strangers near tourist sites in {city}"

    takeaways_html = f"""            <li>{takeaway_top}</li>
            <li>{takeaway_high}</li>
            <li>{takeaway_transport}</li>
            <li>{takeaway_avoid}</li>"""

    # Build related cities section
    related_html = ""
    if city in related_cities_map and related_cities_map[city]:
        related_items = ""
        for rc in related_cities_map[city]:
            rc_slug = CITY_SLUGS.get(rc["city"], "")
            if rc_slug:
                related_items += f"""
            <a href="/scams/{rc_slug}/" class="related-card">
                <span class="related-flag">{rc.get('flag', '🌍')}</span>
                <span class="related-info">
                    <span class="related-city">{rc['city']}</span>
                    <span class="related-country">{rc['country']}</span>
                </span>
            </a>"""
        if related_items:
            related_html = f"""
    <div class="related-section">
        <h2 class="section-heading">More Scam Guides</h2>
        <div class="related-grid">{related_items}
        </div>
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
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#2D3A5C">

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
                <a href="/scams/">🚨 Tourist Scams</a>
                <a href="/credit-cards/">💳 Credit Card Benefits</a>
                <a href="/health/">🏥 Travel Health Tips</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
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

    <h2 class="section-heading">The {n} Scams</h2>
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

<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
</body>
</html>"""
    return html


def build_related_cities_map(all_cities):
    """Build a mapping of city -> list of related cities (same country + nearby popular cities)."""
    # Group cities by country
    country_cities = defaultdict(list)
    for city_data in all_cities:
        city = city_data["city"]
        if city in CITY_SLUGS:
            country_cities[city_data["country"]].append({
                "city": city,
                "country": city_data["country"],
                "flag": city_data.get("flag", "🌍"),
                "scam_count": len(city_data.get("scams", [])),
            })

    # For each city, related = same-country cities + a few popular global cities
    popular_global = ["Paris", "Bangkok", "Rome", "Tokyo", "Istanbul", "Prague", "Marrakech", "Cairo"]
    related_map = {}

    for city_data in all_cities:
        city = city_data["city"]
        if city not in CITY_SLUGS:
            continue
        country = city_data["country"]

        # Same-country cities (excluding self)
        same_country = [c for c in country_cities[country] if c["city"] != city]

        # Add popular global cities if we have fewer than 4 related
        related = same_country[:]
        if len(related) < 4:
            for pg in popular_global:
                if pg != city and pg not in [r["city"] for r in related]:
                    for cd in all_cities:
                        if cd["city"] == pg and pg in CITY_SLUGS:
                            related.append({
                                "city": pg,
                                "country": cd["country"],
                                "flag": cd.get("flag", "🌍"),
                                "scam_count": len(cd.get("scams", [])),
                            })
                            break
                if len(related) >= 6:
                    break

        related_map[city] = related[:6]

    return related_map


def generate_country_page(country, country_code, flag, cities_data, all_scams_count):
    """Generate an enriched country-level scam page."""
    cc_lower = country_code.lower()
    n_cities = len(cities_data)
    total_scams = sum(c["scam_count"] for c in cities_data)

    # Collect all scam types across cities to find most common
    scam_type_counts = defaultdict(int)
    high_count = 0
    for cd in cities_data:
        for s in cd.get("scams_raw", []):
            name = s.get("scam_name", "")
            level = s.get("danger_level", "").lower()
            if level == "high":
                high_count += 1
            # Normalize common scam keywords for grouping
            for keyword in ["pickpocket", "taxi", "overcharge", "fake", "bracelet", "petition", "restaurant"]:
                if keyword in name.lower():
                    scam_type_counts[keyword.capitalize()] += 1

    top_types = sorted(scam_type_counts.items(), key=lambda x: -x[1])[:5]
    top_types_html = ""
    if top_types:
        pills = "".join(f'<span style="display:inline-block;background:#EFF6FF;border:1px solid #93C5FD;border-radius:99px;padding:0.25rem 0.75rem;font-size:0.8rem;font-weight:600;color:#2D3A5C;">{t} ({c})</span>' for t, c in top_types)
        top_types_html = f"""
    <div style="margin-bottom:1.5rem;">
        <h3 style="font-size:0.85rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B5D4F;margin-bottom:0.6rem;">Most Common Scam Types</h3>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">{pills}</div>
    </div>"""

    # Emergency info
    em = EMERGENCY_INFO.get(country, None)
    emergency_html = ""
    if em:
        emergency_html = f"""
    <div style="background:#2D3A5C;color:white;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <h3 style="font-size:1rem;font-weight:700;margin-bottom:0.75rem;">&#x1F6A8; Emergency Numbers in {country}</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;font-size:0.9rem;">
            <div><strong>Police:</strong> {em['police_number']}</div>
            <div><strong>Emergency:</strong> {em['emergency_number']}</div>
            <div><strong>Online Report:</strong> <a href="{em['report_url']}" target="_blank" rel="noopener" style="color:#93C5FD;">{em['report_site']}</a></div>
        </div>
    </div>"""

    # City cards
    city_cards = ""
    for cd in sorted(cities_data, key=lambda x: -x["scam_count"]):
        slug = cd["slug"]
        city_cards += f"""
        <a href="/scams/{slug}/" class="city-card">
            <h3>{cd["city"]}</h3>
            <div class="scam-count">{cd["scam_count"]} scams documented</div>
        </a>"""

    # Cross-links
    health_slug = COUNTRY_HEALTH_SLUGS.get(country, "")
    cross_links = ""
    if health_slug:
        cross_links += f'<a href="/health/{health_slug}/" style="color:#C4704B;font-weight:600;text-decoration:none;">&#127973; {country} Health Guide</a>'
        cross_links += '<span style="margin:0 1rem;color:#d1d5db;">|</span>'
    cross_links += '<a href="/scams/" style="color:#C4704B;font-weight:600;text-decoration:none;">&larr; Back to all scam guides</a>'

    # Overview text
    if high_count > 0:
        risk_note = f"{high_count} scams across {country} are rated high risk."
    else:
        risk_note = f"Most scams in {country} are low-to-medium risk."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourist Scams in {country} (2026) &mdash; All Cities | tabiji.ai</title>
    <meta name="description" content="Tourist scam guides for {n_cities} cities in {country}. {total_scams} scams documented from real Reddit traveler stories.">
    <link rel="canonical" href="https://tabiji.ai/scams/country/{cc_lower}/">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="Tourist Scams in {country} (2026) — tabiji.ai">
    <meta property="og:description" content="{total_scams} scams documented across {n_cities} cities in {country}. Real Reddit traveler stories.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/scams/country/{cc_lower}/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Tourist Scams in {country} (2026)">
    <meta name="twitter:description" content="{total_scams} scams across {n_cities} cities. Reddit-sourced.">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <link rel="stylesheet" href="/assets/shared-shell.css">
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
                "numberOfItems": {n_cities},
                "publisher": {{"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/"}}
            }}
        ]
    }}
    </script>
    <style>
        .page-hero {{ background: linear-gradient(135deg, #2D3A5C, #3D4E7A); color: white; padding: 7rem 2rem 3rem; text-align: center; }}
        .page-hero h1 {{ font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 800; margin-bottom: 0.75rem; }}
        .page-hero p {{ font-size: 1.05rem; opacity: 0.85; max-width: 600px; margin: 0 auto; }}
        .page-hero-stats {{ display: flex; justify-content: center; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap; }}
        .page-hero-stat {{ background: rgba(255,255,255,0.12); border-radius: 99px; padding: 0.3rem 0.9rem; font-size: 0.82rem; font-weight: 600; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
        .city-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
        .city-card {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.25rem; text-decoration: none; color: #2C2419; transition: box-shadow 0.2s, transform 0.2s; }}
        .city-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.08); transform: translateY(-2px); }}
        .city-card h3 {{ font-size: 1rem; color: #2D3A5C; margin-bottom: 0.3rem; }}
        .city-card .scam-count {{ font-size: 0.8rem; color: #dc2626; font-weight: 600; }}
        .breadcrumb {{ background: #E8DFD0; padding: 0.6rem 2rem; font-size: 0.8rem; color: #6B5D4F; }}
        .breadcrumb a {{ color: #6B5D4F; text-decoration: none; }}
        .breadcrumb a:hover {{ color: #2D3A5C; }}
        .breadcrumb span {{ margin: 0 0.4rem; }}
    </style>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
</head>
<body>
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
                <a href="/scams/">&#128680; Tourist Scams</a>
                <a href="/health/">&#127973; Travel Health Tips</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>

<div class="breadcrumb">
    <a href="/">Home</a><span>&rsaquo;</span><a href="/scams/">Scams</a><span>&rsaquo;</span>{country}
</div>

<div class="page-hero">
    <h1>{flag} Tourist Scams in {country}</h1>
    <p>Scam guides for {n_cities} cities in {country}, sourced from real Reddit traveler reports. {risk_note}</p>
    <div class="page-hero-stats">
        <span class="page-hero-stat">{n_cities} Cities</span>
        <span class="page-hero-stat">{total_scams} Scams Documented</span>
        <span class="page-hero-stat">Reddit-Sourced</span>
    </div>
</div>
<div class="container">
{emergency_html}
{top_types_html}
    <h2 style="font-size:0.85rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B5D4F;margin-bottom:0.5rem;">City Guides</h2>
    <div class="city-grid">{city_cards}
    </div>
    <div style="margin-top:2rem;text-align:center;">
        {cross_links}
    </div>
</div>
<footer>
    <p>&copy; 2026 tabiji.ai &middot; <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> &middot; <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> &middot; <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> &middot; <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> &middot; <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> &middot; <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> &middot; <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> &middot; <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> &middot; <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<script defer src="/assets/shared-shell.js"></script>
</body>
</html>"""
    return html


def build_country_data(all_cities):
    """Group cities by country for country page generation."""
    countries = defaultdict(lambda: {"cities": [], "flag": "🌍", "country_code": ""})
    for city_data in all_cities:
        city = city_data["city"]
        if city not in CITY_SLUGS:
            continue
        country = city_data["country"]
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

    # Load all batch files
    all_cities = []
    batch_files = sorted(glob.glob(os.path.join(base_dir, "research", "batch*.json")) +
                         glob.glob(os.path.join(base_dir, "research", "tier_b_batch*.json")) +
                         glob.glob(os.path.join(base_dir, "research", "tier_c_batch*.json")) +
                         glob.glob(os.path.join(base_dir, "research", "tier_d_batch*.json")))
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
