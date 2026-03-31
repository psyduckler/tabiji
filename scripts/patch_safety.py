#!/usr/bin/env python3
"""
Patch 40 existing safety JSON files with hospitals and disasterResponse fields.
Fields are inserted after the 'practical' field.
"""

import json
import os
from pathlib import Path

SAFETY_DIR = Path(__file__).parent.parent / "api" / "v1" / "safety"

HOSPITALS_DATA = {
    "ar": [
        {
            "name": "Hospital Italiano de Buenos Aires",
            "address": "Gascon 450, Buenos Aires",
            "city": "Buenos Aires",
            "lat": -34.6124,
            "lng": -58.4271,
            "phone": "+54-11-4959-0200",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "One of the best private hospitals in Argentina. English-speaking staff, international patient services."
        }
    ],
    "au": [
        {
            "name": "Royal Melbourne Hospital",
            "address": "300 Grattan St, Parkville VIC 3050",
            "city": "Melbourne",
            "lat": -37.7990,
            "lng": 144.9558,
            "phone": "+61-3-9342-7000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major public hospital serving Melbourne. Level 1 trauma center."
        },
        {
            "name": "Royal Prince Alfred Hospital",
            "address": "Missenden Rd, Camperdown NSW 2050",
            "city": "Sydney",
            "lat": -33.8890,
            "lng": 151.1867,
            "phone": "+61-2-9515-6111",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major Sydney public hospital with comprehensive emergency services."
        }
    ],
    "br": [
        {
            "name": "Hospital Israelita Albert Einstein",
            "address": "Av. Albert Einstein 627/701, Morumbi, São Paulo",
            "city": "São Paulo",
            "lat": -23.5993,
            "lng": -46.7199,
            "phone": "+55-11-2151-1233",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Ranked among the best hospitals in Latin America. Full international patient services and English staff."
        }
    ],
    "cl": [
        {
            "name": "Clínica Las Condes",
            "address": "Lo Fontecilla 441, Las Condes, Santiago",
            "city": "Santiago",
            "lat": -33.4105,
            "lng": -70.5996,
            "phone": "+56-2-2210-4000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Top private hospital in Chile with international patient services and English-speaking staff."
        }
    ],
    "cn": [
        {
            "name": "Peking Union Medical College Hospital",
            "address": "1 Shuaifuyuan Wangfujing, Dongcheng District, Beijing",
            "city": "Beijing",
            "lat": 39.9097,
            "lng": 116.4072,
            "phone": "+86-10-6915-6114",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Premier hospital in Beijing. International VIP clinic with English-speaking doctors."
        },
        {
            "name": "Shanghai United Family Hospital",
            "address": "1139 Xianxia Road, Changning District, Shanghai",
            "city": "Shanghai",
            "lat": 31.2107,
            "lng": 121.3964,
            "phone": "+86-21-2216-3900",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "International hospital catering to expats and tourists. Full English-speaking staff."
        }
    ],
    "co": [
        {
            "name": "Fundación Santa Fe de Bogotá",
            "address": "Calle 119 No. 7-75, Bogotá",
            "city": "Bogotá",
            "lat": 4.7013,
            "lng": -74.0428,
            "phone": "+57-1-603-0303",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Top private hospital in Bogotá. International patient services, English-speaking staff."
        }
    ],
    "cr": [
        {
            "name": "Hospital CIMA San José",
            "address": "Prospero Fernandez Highway, Escazú, San José",
            "city": "San José",
            "lat": 9.9306,
            "lng": -84.1463,
            "phone": "+506-2208-1000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for tourists in Costa Rica. JCI-accredited, full English services, accepts US insurance."
        }
    ],
    "cz": [
        {
            "name": "Motol University Hospital",
            "address": "V Úvalu 84, Motol, Prague 5",
            "city": "Prague",
            "lat": 50.0746,
            "lng": 14.3465,
            "phone": "+420-224-431-111",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Largest university hospital in Czech Republic. International patient clinic with English-speaking doctors."
        }
    ],
    "de": [
        {
            "name": "Charité – Universitätsmedizin Berlin",
            "address": "Charitéplatz 1, 10117 Berlin",
            "city": "Berlin",
            "lat": 52.5258,
            "lng": 13.3777,
            "phone": "+49-30-450-50",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Europe's largest university hospital. International patients unit with English-speaking staff."
        },
        {
            "name": "Klinikum der Universität München",
            "address": "Marchioninistraße 15, 81377 Munich",
            "city": "Munich",
            "lat": 48.1098,
            "lng": 11.4726,
            "phone": "+49-89-4400-0",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Premier university hospital in Munich. English-speaking staff widely available."
        }
    ],
    "eg": [
        {
            "name": "As-Salam International Hospital",
            "address": "Corniche El Nile, Maadi, Cairo",
            "city": "Cairo",
            "lat": 29.9553,
            "lng": 31.2284,
            "phone": "+20-2-2524-0077",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for tourists in Cairo. English-speaking staff, accepts international insurance."
        }
    ],
    "es": [
        {
            "name": "Hospital La Paz",
            "address": "Paseo de la Castellana 261, 28046 Madrid",
            "city": "Madrid",
            "lat": 40.4810,
            "lng": -3.6886,
            "phone": "+34-91-727-7000",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "One of Madrid's main public hospitals. EU citizens treated under EHIC. Some English-speaking staff."
        },
        {
            "name": "Hospital Clínic de Barcelona",
            "address": "Carrer de Villarroel 170, 08036 Barcelona",
            "city": "Barcelona",
            "lat": 41.3884,
            "lng": 2.1521,
            "phone": "+34-93-227-5400",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major Barcelona hospital with international patient unit and English services."
        }
    ],
    "fr": [
        {
            "name": "Hôpital Lariboisière",
            "address": "2 Rue Ambroise Paré, 75010 Paris",
            "city": "Paris",
            "lat": 48.8823,
            "lng": 2.3564,
            "phone": "+33-1-49-95-65-65",
            "open24h": True,
            "englishSpeaking": False,
            "type": "trauma",
            "notes": "One of Paris's main trauma and emergency hospitals. EU citizens treated under EHIC."
        },
        {
            "name": "American Hospital of Paris",
            "address": "63 Boulevard Victor Hugo, 92200 Neuilly-sur-Seine",
            "city": "Paris",
            "lat": 48.8849,
            "lng": 2.2699,
            "phone": "+33-1-46-41-25-25",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Premier English-language hospital near Paris. Accepts US and international insurance."
        }
    ],
    "gb": [
        {
            "name": "St Thomas' Hospital",
            "address": "Westminster Bridge Road, Lambeth, London SE1 7EH",
            "city": "London",
            "lat": 51.4988,
            "lng": -0.1180,
            "phone": "+44-20-7188-7188",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major NHS hospital opposite Houses of Parliament. Excellent emergency department."
        },
        {
            "name": "Manchester Royal Infirmary",
            "address": "Oxford Road, Manchester M13 9WL",
            "city": "Manchester",
            "lat": 53.4617,
            "lng": -2.2255,
            "phone": "+44-161-276-1234",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Main NHS trauma center serving Greater Manchester."
        }
    ],
    "gr": [
        {
            "name": "Evangelismos General Hospital",
            "address": "Ipsilantou 45-47, Athens 106 76",
            "city": "Athens",
            "lat": 37.9759,
            "lng": 23.7427,
            "phone": "+30-213-204-1000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Athens' main public hospital. EU citizens treated under EHIC. Some English-speaking doctors."
        }
    ],
    "hr": [
        {
            "name": "KBC Zagreb — Rebro",
            "address": "Kišpatićeva ulica 12, 10000 Zagreb",
            "city": "Zagreb",
            "lat": 45.8195,
            "lng": 16.0250,
            "phone": "+385-1-2388-888",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Largest university hospital in Croatia. Main trauma and emergency center for Zagreb."
        },
        {
            "name": "Opća bolnica Dubrovnik",
            "address": "Dr. Roka Mišetića 2, 20000 Dubrovnik",
            "city": "Dubrovnik",
            "lat": 42.6507,
            "lng": 18.0934,
            "phone": "+385-20-431-777",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Main hospital for the Dubrovnik region. English-speaking staff available."
        }
    ],
    "hu": [
        {
            "name": "Semmelweis University Hospital",
            "address": "Üllői út 78, 1082 Budapest",
            "city": "Budapest",
            "lat": 47.4788,
            "lng": 19.0735,
            "phone": "+36-1-210-0278",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major university hospital in Budapest. Some English-speaking doctors."
        },
        {
            "name": "Privatklinik Rózsakerti",
            "address": "Gábor Áron u. 74-78, 1026 Budapest",
            "city": "Budapest",
            "lat": 47.5188,
            "lng": 19.0157,
            "phone": "+36-1-391-5900",
            "open24h": False,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Private clinic catering to foreigners. English-speaking staff, accepts international insurance."
        }
    ],
    "id": [
        {
            "name": "Siloam Hospitals Kebon Jeruk",
            "address": "Jl. Perjuangan Kav. 8, Kebon Jeruk, West Jakarta",
            "city": "Jakarta",
            "lat": -6.1953,
            "lng": 106.7688,
            "phone": "+62-21-2567-7888",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "International-standard hospital in Jakarta. English-speaking staff available."
        },
        {
            "name": "BIMC Hospital Kuta",
            "address": "Jl. By Pass Ngurah Rai 100X, Kuta, Bali",
            "city": "Bali",
            "lat": -8.7262,
            "lng": 115.1770,
            "phone": "+62-361-761-263",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for tourists in Bali. Full English service, accepts international insurance."
        }
    ],
    "in": [
        {
            "name": "Apollo Hospital New Delhi",
            "address": "Sarita Vihar, Delhi–Mathura Road, New Delhi 110076",
            "city": "New Delhi",
            "lat": 28.5399,
            "lng": 77.2922,
            "phone": "+91-11-2692-5858",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "World-class private hospital. International patient services, English-speaking staff throughout."
        },
        {
            "name": "Lilavati Hospital and Research Centre",
            "address": "A-791, Bandra Reclamation, Bandra West, Mumbai",
            "city": "Mumbai",
            "lat": 19.0499,
            "lng": 72.8294,
            "phone": "+91-22-2675-1000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Top private hospital in Mumbai. English-speaking staff, good emergency facilities."
        }
    ],
    "it": [
        {
            "name": "Policlinico Umberto I",
            "address": "Viale del Policlinico 155, 00161 Rome",
            "city": "Rome",
            "lat": 41.9025,
            "lng": 12.5113,
            "phone": "+39-06-4997-1",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Largest public hospital in Rome. EU citizens treated under EHIC. Some English-speaking staff."
        },
        {
            "name": "ASST Grande Ospedale Metropolitano Niguarda",
            "address": "Piazza Ospedale Maggiore 3, 20162 Milan",
            "city": "Milan",
            "lat": 45.5102,
            "lng": 9.1867,
            "phone": "+39-02-6444-1",
            "open24h": True,
            "englishSpeaking": True,
            "type": "trauma",
            "notes": "Major trauma and emergency center in Milan. Level 1 trauma, some English-speaking staff."
        }
    ],
    "jp": [
        {
            "name": "St. Luke's International Hospital",
            "address": "9-1 Akashi-cho, Chuo-ku, Tokyo",
            "city": "Tokyo",
            "lat": 35.6693,
            "lng": 139.7745,
            "phone": "+81-3-5550-7166",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for English-speaking tourists in Tokyo. Full international patient services."
        },
        {
            "name": "Osaka University Hospital",
            "address": "2-15 Yamadaoka, Suita, Osaka",
            "city": "Osaka",
            "lat": 34.8257,
            "lng": 135.5229,
            "phone": "+81-6-6879-5111",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major university hospital serving Osaka. International patient services available."
        }
    ],
    "ke": [
        {
            "name": "Aga Khan University Hospital Nairobi",
            "address": "3rd Parklands Ave, Nairobi",
            "city": "Nairobi",
            "lat": -1.2636,
            "lng": 36.8119,
            "phone": "+254-20-366-2000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital in East Africa for tourists. English-speaking staff, international patient services."
        },
        {
            "name": "Nairobi Hospital",
            "address": "Argwings Kodhek Road, Nairobi",
            "city": "Nairobi",
            "lat": -1.2928,
            "lng": 36.7864,
            "phone": "+254-20-284-5000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Good private hospital with solid emergency facilities."
        }
    ],
    "kr": [
        {
            "name": "Severance Hospital (Yonsei University)",
            "address": "50-1 Yonsei-ro, Seodaemun-gu, Seoul",
            "city": "Seoul",
            "lat": 37.5627,
            "lng": 126.9396,
            "phone": "+82-2-2228-5800",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Premier university hospital with International Health Care Center and English services."
        },
        {
            "name": "Samsung Medical Center",
            "address": "81 Irwon-ro, Gangnam-gu, Seoul",
            "city": "Seoul",
            "lat": 37.4884,
            "lng": 127.0854,
            "phone": "+82-2-3410-2114",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "World-class private hospital with international patient center."
        }
    ],
    "lk": [
        {
            "name": "Lanka Hospitals Corporation",
            "address": "578 Elvitigala Mawatha, Narahenpita, Colombo 5",
            "city": "Colombo",
            "lat": 6.8911,
            "lng": 79.8740,
            "phone": "+94-11-553-0000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital in Sri Lanka for tourists. English-speaking staff, international standard care."
        }
    ],
    "ma": [
        {
            "name": "Clinique Internationale de Marrakech",
            "address": "Av. Ibn Sina, Marrakech",
            "city": "Marrakech",
            "lat": 31.6389,
            "lng": -7.9898,
            "phone": "+212-524-339-494",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Best private hospital for tourists in Marrakech. English and French-speaking staff."
        },
        {
            "name": "CHU Ibn Rushd",
            "address": "Quartier des Hôpitaux, Casablanca",
            "city": "Casablanca",
            "lat": 33.5956,
            "lng": -7.6064,
            "phone": "+212-522-225-325",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Main university hospital in Casablanca. French-speaking primarily."
        }
    ],
    "mx": [
        {
            "name": "Hospital Ángeles Metropolitano",
            "address": "Tlacotalpan 59, Colonia Roma Sur, Mexico City",
            "city": "Mexico City",
            "lat": 19.4075,
            "lng": -99.1665,
            "phone": "+52-55-5229-8500",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Good private hospital in Mexico City. English-speaking staff, accepts US insurance."
        },
        {
            "name": "Hospital Galenia",
            "address": "Av. Bonampak s/n, Super Manzana 10, Cancún",
            "city": "Cancún",
            "lat": 21.1567,
            "lng": -86.8465,
            "phone": "+52-998-891-3700",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital in Cancún resort area. Full English services, JCI-accredited."
        }
    ],
    "my": [
        {
            "name": "Gleneagles Hospital Kuala Lumpur",
            "address": "286 & 288 Jalan Ampang, Kuala Lumpur",
            "city": "Kuala Lumpur",
            "lat": 3.1420,
            "lng": 101.7179,
            "phone": "+60-3-4141-3018",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Top private hospital in KL. International patient services, English-speaking staff throughout."
        },
        {
            "name": "Penang Adventist Hospital",
            "address": "465 Jalan Burma, 10350 Georgetown, Penang",
            "city": "Penang",
            "lat": 5.4141,
            "lng": 100.3289,
            "phone": "+60-4-222-7200",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Leading hospital in Penang with strong international patient services."
        }
    ],
    "no": [
        {
            "name": "Oslo University Hospital Rikshospitalet",
            "address": "Sognsvannsveien 20, 0372 Oslo",
            "city": "Oslo",
            "lat": 59.9463,
            "lng": 10.7376,
            "phone": "+47-23-07-00-00",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Norway's national hospital. English widely spoken by all medical staff."
        },
        {
            "name": "Haukeland University Hospital",
            "address": "Jonas Lies vei 65, 5021 Bergen",
            "city": "Bergen",
            "lat": 60.3771,
            "lng": 5.3614,
            "phone": "+47-55-97-50-00",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Main hospital for western Norway. English spoken by medical staff."
        }
    ],
    "nz": [
        {
            "name": "Auckland City Hospital",
            "address": "2 Park Road, Grafton, Auckland 1023",
            "city": "Auckland",
            "lat": -36.8606,
            "lng": 174.7696,
            "phone": "+64-9-367-0000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "New Zealand's largest public hospital. Comprehensive emergency and specialist services."
        },
        {
            "name": "Wellington Regional Hospital",
            "address": "Riddiford Street, Newtown, Wellington 6021",
            "city": "Wellington",
            "lat": -41.2774,
            "lng": 174.7854,
            "phone": "+64-4-385-5999",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Main hospital for the Wellington region."
        }
    ],
    "pe": [
        {
            "name": "Clínica Anglo Americana",
            "address": "Av. Alfredo Salazar, Cdra. 3, San Isidro, Lima",
            "city": "Lima",
            "lat": -12.0878,
            "lng": -77.0450,
            "phone": "+51-1-616-8900",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best private hospital for tourists in Lima. English-speaking staff, accepts international insurance."
        },
        {
            "name": "Hospital Nacional Cayetano Heredia",
            "address": "Av. Honorio Delgado 262, San Martín de Porres, Lima",
            "city": "Lima",
            "lat": -12.0237,
            "lng": -77.0547,
            "phone": "+51-1-482-0402",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Major public hospital for emergencies. Limited English. Use private clinic for non-emergency care."
        }
    ],
    "ph": [
        {
            "name": "Makati Medical Center",
            "address": "2 Amorsolo Street, Legazpi Village, Makati City",
            "city": "Manila",
            "lat": 14.5565,
            "lng": 121.0159,
            "phone": "+63-2-8888-8999",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Top private hospital in Metro Manila. English-speaking staff, strong emergency facilities."
        },
        {
            "name": "St. Luke's Medical Center BGC",
            "address": "32nd St. corner 5th Ave, Bonifacio Global City, Taguig",
            "city": "Manila",
            "lat": 14.5484,
            "lng": 121.0503,
            "phone": "+63-2-8789-7700",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Modern hospital in BGC. JCI-accredited, full English services, international patient center."
        }
    ],
    "pl": [
        {
            "name": "Szpital Kliniczny im. ks. Anny Mazowieckiej, Warsaw",
            "address": "ul. Karowa 2, 00-315 Warsaw",
            "city": "Warsaw",
            "lat": 52.2330,
            "lng": 21.0132,
            "phone": "+48-22-596-6000",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "University hospital in central Warsaw. EU citizens treated under EHIC."
        },
        {
            "name": "Szpital im. Ludwika Rydygiera w Krakowie",
            "address": "os. Złotej Jesieni 1, 31-826 Kraków",
            "city": "Kraków",
            "lat": 50.0540,
            "lng": 19.9799,
            "phone": "+48-12-646-8111",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Main hospital serving Kraków. EU citizens treated under EHIC."
        }
    ],
    "pt": [
        {
            "name": "Hospital de Santa Maria",
            "address": "Av. Prof. Egas Moniz, 1649-028 Lisbon",
            "city": "Lisbon",
            "lat": 38.7433,
            "lng": -9.1603,
            "phone": "+351-21-780-5000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Main public hospital in Lisbon. EU citizens treated under EHIC. Some English-speaking doctors."
        },
        {
            "name": "Hospital de São João",
            "address": "Al. Prof. Hernâni Monteiro, 4200-319 Porto",
            "city": "Porto",
            "lat": 41.1771,
            "lng": -8.5986,
            "phone": "+351-22-551-2100",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major university hospital in Porto. Good emergency services."
        }
    ],
    "se": [
        {
            "name": "Karolinska University Hospital",
            "address": "Solnavägen 1, 171 76 Stockholm",
            "city": "Stockholm",
            "lat": 59.3538,
            "lng": 18.0268,
            "phone": "+46-8-517-700-00",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Sweden's leading university hospital. English spoken by virtually all medical staff."
        },
        {
            "name": "Sahlgrenska University Hospital",
            "address": "Blå Stråket 5, 413 45 Gothenburg",
            "city": "Gothenburg",
            "lat": 57.6853,
            "lng": 11.9694,
            "phone": "+46-31-342-1000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Major hospital serving Gothenburg and western Sweden."
        }
    ],
    "sg": [
        {
            "name": "Singapore General Hospital",
            "address": "Outram Road, Singapore 169608",
            "city": "Singapore",
            "lat": 1.2797,
            "lng": 103.8352,
            "phone": "+65-6222-3322",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Singapore's largest public hospital. Excellent facilities, English-speaking staff throughout."
        },
        {
            "name": "Mount Elizabeth Hospital",
            "address": "3 Mount Elizabeth, Singapore 228510",
            "city": "Singapore",
            "lat": 1.3069,
            "lng": 103.8331,
            "phone": "+65-6737-2666",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Premier private hospital. International patient services, accepts major international insurance."
        }
    ],
    "th": [
        {
            "name": "Bumrungrad International Hospital",
            "address": "33 Sukhumvit 3, Wattana, Bangkok",
            "city": "Bangkok",
            "lat": 13.7469,
            "lng": 100.5524,
            "phone": "+66-2-066-8888",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "World-renowned hospital serving over 1 million patients/year. Full English services, JCI-accredited."
        },
        {
            "name": "Bangkok Hospital Phuket",
            "address": "2/1 Hongyok-Utis Road, Muang, Phuket",
            "city": "Phuket",
            "lat": 7.8927,
            "lng": 98.3876,
            "phone": "+66-76-254-425",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital in Phuket for tourists. English-speaking staff, accepts international insurance."
        }
    ],
    "tr": [
        {
            "name": "Acıbadem Maslak Hospital",
            "address": "Büyükdere Caddesi 40, Maslak, Istanbul",
            "city": "Istanbul",
            "lat": 41.1048,
            "lng": 29.0241,
            "phone": "+90-212-304-4444",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Top private hospital in Istanbul. International patient services, English-speaking staff."
        },
        {
            "name": "Ankara University Ibn-i Sina Hospital",
            "address": "Talatpaşa Bulvarı, Sıhhiye, 06230 Ankara",
            "city": "Ankara",
            "lat": 39.9209,
            "lng": 32.8623,
            "phone": "+90-312-310-3333",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Main university hospital in Ankara. Limited English. Use private hospitals where possible."
        }
    ],
    "tz": [
        {
            "name": "Aga Khan Hospital Dar es Salaam",
            "address": "Ocean Road, Dar es Salaam",
            "city": "Dar es Salaam",
            "lat": -6.7878,
            "lng": 39.2665,
            "phone": "+255-22-115-0600",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for tourists in Tanzania. English-speaking staff, international standard care."
        },
        {
            "name": "Muhimbili National Hospital",
            "address": "United Nations Road, Upanga West, Dar es Salaam",
            "city": "Dar es Salaam",
            "lat": -6.8009,
            "lng": 39.2622,
            "phone": "+255-22-215-0610",
            "open24h": True,
            "englishSpeaking": False,
            "type": "general",
            "notes": "Tanzania's national referral hospital. Use for emergencies only — limited English."
        }
    ],
    "us": [
        {
            "name": "Massachusetts General Hospital",
            "address": "55 Fruit Street, Boston, MA 02114",
            "city": "Boston",
            "lat": 42.3631,
            "lng": -71.0687,
            "phone": "+1-617-726-2000",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "One of the top hospitals in the US. Harvard Medical School teaching hospital."
        },
        {
            "name": "Cedars-Sinai Medical Center",
            "address": "8700 Beverly Blvd, Los Angeles, CA 90048",
            "city": "Los Angeles",
            "lat": 34.0751,
            "lng": -118.3801,
            "phone": "+1-310-423-3277",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Top-ranked private hospital in Los Angeles."
        },
        {
            "name": "NewYork-Presbyterian Hospital",
            "address": "525 East 68th Street, New York, NY 10065",
            "city": "New York City",
            "lat": 40.7651,
            "lng": -73.9543,
            "phone": "+1-212-746-5454",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "One of the top-ranked hospitals in the US. Affiliated with Weill Cornell and Columbia."
        }
    ],
    "vn": [
        {
            "name": "FV Hospital",
            "address": "6 Nguyen Luong Bang Street, Phu My Hung, District 7, Ho Chi Minh City",
            "city": "Ho Chi Minh City",
            "lat": 10.7280,
            "lng": 106.7220,
            "phone": "+84-28-5411-3333",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "Best hospital for tourists in HCMC. French-Vietnamese hospital, full English services, JCI-accredited."
        },
        {
            "name": "Vinmec International Hospital Hanoi",
            "address": "458 Minh Khai, Hai Ba Trung, Hanoi",
            "city": "Hanoi",
            "lat": 21.0313,
            "lng": 105.7997,
            "phone": "+84-24-3974-3556",
            "open24h": True,
            "englishSpeaking": True,
            "type": "international",
            "notes": "International-standard hospital in Hanoi. English-speaking staff, accepts international insurance."
        }
    ],
    "za": [
        {
            "name": "Groote Schuur Hospital",
            "address": "Main Road, Observatory, Cape Town 7925",
            "city": "Cape Town",
            "lat": -33.9421,
            "lng": 18.4613,
            "phone": "+27-21-404-9111",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Historic hospital (site of world's first heart transplant). Public hospital with good emergency facilities."
        },
        {
            "name": "Netcare Milpark Hospital",
            "address": "9 Guild Road, Parktown West, Johannesburg 2193",
            "city": "Johannesburg",
            "lat": -26.1859,
            "lng": 28.0043,
            "phone": "+27-11-480-5600",
            "open24h": True,
            "englishSpeaking": True,
            "type": "general",
            "notes": "Top private hospital in Johannesburg. Trauma center, English-speaking staff."
        }
    ]
}

DISASTER_RESPONSE_DATA = {
    "ar": {
        "risks": ["earthquakes", "flooding", "thunderstorms", "wildfires"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on under sturdy furniture or against interior wall",
                    "Stay away from windows and exterior walls",
                    "If outdoors, move to open area away from buildings and power lines",
                    "Expect aftershocks following initial earthquake"
                ],
                "after": [
                    "Check for gas leaks and structural damage before re-entering buildings",
                    "Follow INDEC (National Institute of Statistics) and official government alerts",
                    "Contact US Embassy if assistance needed: +54-11-5777-4533"
                ],
                "resources": [
                    "SIFEM (Federal Emergency System): www.argentina.gob.ar",
                    "Police emergency: 911",
                    "Fire: 100"
                ]
            }
        ]
    },
    "au": {
        "risks": ["bushfires", "cyclones", "flooding", "extreme heat", "earthquakes"],
        "protocols": [
            {
                "type": "bushfire",
                "immediate": [
                    "Monitor state fire authority alerts (RFS, CFA, DFES) and ABC Emergency radio",
                    "Activate your Bushfire Survival Plan — do not wait for official evacuation order",
                    "Leave early — 'Leave Early or Stay and Actively Defend' — leaving early is safer",
                    "If trapped: shelter in car below window level away from vegetation",
                    "Cover exposed skin and breathe through a wet cloth"
                ],
                "after": [
                    "Do not return to affected area until emergency services declare it safe",
                    "Watch for falling trees and weakened structures",
                    "Avoid breathing smoke — use P2/N95 masks",
                    "Register with Emergency Registration and Inquiry (1800 512 634) if displaced"
                ],
                "resources": [
                    "NSW Rural Fire Service: www.rfs.nsw.gov.au",
                    "Emergency services: 000",
                    "ABC Emergency radio: 576 AM",
                    "Fires Near Me app (NSW), VicEmergency app (VIC)"
                ]
            },
            {
                "type": "cyclone",
                "immediate": [
                    "Evacuate if instructed by authorities — cyclone shelters are available",
                    "Stay indoors in the strongest part of the building — interior room, away from windows",
                    "Turn off electricity, gas, and water at mains if safe to do so",
                    "The eye of the storm may pass — do not go outside until official all-clear"
                ],
                "after": [
                    "Watch for flash flooding and storm surge after cyclone passes",
                    "Do not drive through flooded roads",
                    "Check for structural damage before re-entering buildings"
                ],
                "resources": [
                    "Bureau of Meteorology: www.bom.gov.au",
                    "Emergency services: 000",
                    "Disaster Assist (Australian Government): www.disasterassist.gov.au"
                ]
            }
        ]
    },
    "br": {
        "risks": ["flooding", "landslides", "tropical storms", "extreme heat", "drought"],
        "protocols": [
            {
                "type": "flooding / landslides",
                "immediate": [
                    "Move to higher ground immediately — do not wait for official order in rapidly rising water",
                    "Avoid all drainage channels, rivers, and low-lying areas during heavy rain",
                    "If driving, do not attempt to cross flooded roads — turn back",
                    "Stay away from hillsides that may be prone to landslides after heavy rain"
                ],
                "after": [
                    "Do not return to flood or landslide area until cleared by Defesa Civil",
                    "Avoid contact with floodwater — contamination risk (leptospirosis)",
                    "Monitor Alerta Rio (Rio) or CEMADEN alerts"
                ],
                "resources": [
                    "Defesa Civil (Civil Defense): 199",
                    "Emergency services: 190 (police), 193 (fire), 192 (ambulance)",
                    "CEMADEN flood alerts: www.cemaden.gov.br"
                ]
            }
        ]
    },
    "cl": {
        "risks": ["earthquakes", "tsunamis", "volcanic eruptions", "wildfires", "flooding"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on — Chile has some of the world's strongest earthquakes",
                    "If near the coast, immediately move inland and uphill after shaking stops — tsunami risk",
                    "Do not use elevators after shaking stops",
                    "Stay outdoors if possible — do not return to buildings until safe"
                ],
                "after": [
                    "If tsunami warning issued, stay at elevation until official all-clear",
                    "Follow SHOA (tsunami authority) and ONEMI (national emergency office) instructions",
                    "Check for gas leaks and structural damage before re-entering buildings"
                ],
                "resources": [
                    "ONEMI (National Emergency Office): www.onemi.gov.cl",
                    "SHOA tsunami warnings: www.shoa.mil.cl",
                    "Emergency: 131 (ambulance), 132 (fire), 133 (police)"
                ]
            }
        ]
    },
    "cn": {
        "risks": ["earthquakes", "typhoons", "flooding", "air pollution", "extreme cold"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on under sturdy desk or against interior wall",
                    "Stay away from windows and heavy shelving",
                    "Move away from buildings if outdoors — China has active seismic zones",
                    "Do not use elevators after shaking"
                ],
                "after": [
                    "Follow instructions from local government and police",
                    "Monitor CCTV News (English) for updates",
                    "Contact US Embassy or Consulate if assistance needed"
                ],
                "resources": [
                    "China Earthquake Networks Center: www.ceic.ac.cn",
                    "Emergency: 110 (police), 120 (ambulance), 119 (fire)",
                    "US Embassy Beijing: +86-10-8531-4000"
                ]
            },
            {
                "type": "typhoon",
                "immediate": [
                    "Monitor China Meteorological Administration (CMA) typhoon warnings",
                    "Stay indoors when Yellow/Orange/Red typhoon signal issued",
                    "Secure loose outdoor items and stay away from coastal areas",
                    "Follow government evacuation instructions"
                ],
                "after": [
                    "Watch for flooding and landslides following typhoon passage",
                    "Check roads before traveling in affected areas"
                ],
                "resources": [
                    "China Meteorological Administration: www.cma.gov.cn",
                    "Emergency: 110 (police), 120 (ambulance)"
                ]
            }
        ]
    },
    "co": {
        "risks": ["earthquakes", "volcanic eruptions", "flooding", "landslides", "tropical storms"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on under sturdy furniture",
                    "Stay away from windows and exterior walls",
                    "If outdoors, move to open area away from buildings",
                    "Expect aftershocks"
                ],
                "after": [
                    "Follow UNGRD (National Disaster Risk Management) instructions",
                    "Check for gas leaks before re-entering buildings",
                    "Contact US Embassy: +57-1-275-2000 if assistance needed"
                ],
                "resources": [
                    "UNGRD: www.gestiondelriesgo.gov.co",
                    "Emergency: 123",
                    "SGC (Geological Survey): www.sgc.gov.co"
                ]
            }
        ]
    },
    "cr": {
        "risks": ["earthquakes", "volcanic eruptions", "flooding", "tropical storms", "landslides"],
        "protocols": [
            {
                "type": "earthquake / volcanic activity",
                "immediate": [
                    "Drop, cover, and hold on during earthquakes",
                    "If near active volcano (Poás, Irazú, Arenal): follow CNE evacuation zones and instructions",
                    "Do not enter restricted volcanic zone — gases can be lethal without warning",
                    "Stay tuned to CNE alerts and hotel/local authority instructions"
                ],
                "after": [
                    "Check OVSICORI (volcano observatory) for eruption status",
                    "Wear N95 mask if volcanic ash in the air",
                    "Do not drive through volcanic ash — it damages engines"
                ],
                "resources": [
                    "CNE (National Emergency Commission): www.cne.go.cr | 911",
                    "OVSICORI volcano alerts: www.ovsicori.una.ac.cr",
                    "Emergency: 911"
                ]
            }
        ]
    },
    "cz": {
        "risks": ["flooding", "severe storms", "extreme cold", "wildfires (increasing)"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Follow evacuation orders from local authorities",
                    "Move to higher ground and away from rivers and streams",
                    "Do not drive through flooded roads",
                    "Disconnect electrical appliances if water enters building"
                ],
                "after": [
                    "Do not return until authorities declare area safe",
                    "Avoid contact with floodwater",
                    "Monitor Czech Hydrometeorological Institute alerts"
                ],
                "resources": [
                    "Czech Hydrometeorological Institute: www.chmi.cz",
                    "Integrated Rescue System: 112",
                    "Flood warnings: povodnovy-plan.cz"
                ]
            }
        ]
    },
    "de": {
        "risks": ["flooding", "severe storms", "extreme heat (increasing)", "wildfires"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Follow evacuation orders from local authorities (Katastrophenschutz)",
                    "Move vehicles and valuables to upper floors or high ground",
                    "Do not drive through flooded roads — floods can sweep vehicles away",
                    "Follow NINA warning app alerts"
                ],
                "after": [
                    "Contact insurer for damage documentation",
                    "Check structural safety before re-entering buildings",
                    "Follow THW (Federal Agency for Technical Relief) instructions"
                ],
                "resources": [
                    "NINA warning app (Bundesamt für Bevölkerungsschutz)",
                    "Emergency: 112",
                    "THW: www.thw.de"
                ]
            }
        ]
    },
    "eg": {
        "risks": ["extreme heat", "sandstorms", "flash flooding", "earthquakes"],
        "protocols": [
            {
                "type": "extreme heat",
                "immediate": [
                    "Stay indoors during peak hours (11am-4pm)",
                    "Drink 3-4 liters of water per day",
                    "Wear loose, light-colored clothing and sun protection",
                    "Avoid prolonged exposure when temperatures exceed 40°C"
                ],
                "after": [
                    "Seek medical care for signs of heat stroke: hot dry skin, confusion",
                    "Monitor Egypt Meteorological Authority alerts"
                ],
                "resources": [
                    "Egypt Meteorological Authority: www.ema.gov.eg",
                    "Emergency: 123 (police), 180 (ambulance)"
                ]
            }
        ]
    },
    "es": {
        "risks": ["wildfires", "flooding", "extreme heat", "earthquakes", "drought"],
        "protocols": [
            {
                "type": "wildfire",
                "immediate": [
                    "Follow evacuation orders immediately — do not delay to collect belongings",
                    "Evacuate perpendicular to fire's path, not ahead of it",
                    "Close windows and doors if sheltering in place but be ready to evacuate",
                    "Avoid breathing smoke — use damp cloth or mask"
                ],
                "after": [
                    "Do not return to burned area until authorized by authorities",
                    "Watch for secondary hazards: falling trees, toxic ash",
                    "Follow AEMET and local emergency alerts"
                ],
                "resources": [
                    "112 Emergency number",
                    "AEMET weather alerts: www.aemet.es",
                    "Civil Protection: www.proteccioncivil.es"
                ]
            }
        ]
    },
    "fr": {
        "risks": ["flooding", "wildfires", "extreme heat", "avalanches", "terrorism"],
        "protocols": [
            {
                "type": "extreme heat",
                "immediate": [
                    "Stay in cool, shaded areas — seek air-conditioned public spaces (museums, malls)",
                    "Drink water frequently — France distributes free cold water at 'fraîcheur' stations during heat waves",
                    "Call 15 (SAMU) if observing heat-related illness in a vulnerable person",
                    "Wet clothing or use fan with cool water spray to reduce body temperature"
                ],
                "after": [
                    "Monitor Météo-France alerts and local news",
                    "Check on elderly neighbors and relatives"
                ],
                "resources": [
                    "Météo-France: www.meteofrance.com",
                    "SAMU medical emergency: 15",
                    "Emergency: 15 (medical), 17 (police), 18 (fire), 112 (universal)"
                ]
            }
        ]
    },
    "gb": {
        "risks": ["flooding", "severe storms", "extreme heat (increasing)", "terrorism"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Check Environment Agency flood alerts at check-for-flooding.service.gov.uk",
                    "Move valuables to upper floors before leaving",
                    "Do not drive through floodwaters — even 30cm can move a vehicle",
                    "Follow local authority evacuation instructions"
                ],
                "after": [
                    "Do not return home until authorities confirm it is safe",
                    "Document flood damage for insurance claims",
                    "Contact local council for flood recovery assistance"
                ],
                "resources": [
                    "Environment Agency: 0345 988 1188 | check-for-flooding.service.gov.uk",
                    "Emergency: 999",
                    "Non-emergency police: 101"
                ]
            }
        ]
    },
    "gr": {
        "risks": ["wildfires", "earthquakes", "extreme heat", "flooding", "tsunamis"],
        "protocols": [
            {
                "type": "wildfire",
                "immediate": [
                    "Evacuate immediately when ordered — Greek wildfires can move extremely fast",
                    "Do not attempt to fight fires yourself — call 199 (fire) immediately",
                    "Drive slowly with headlights on in smoky conditions",
                    "Wet a cloth and breathe through it if caught in smoke"
                ],
                "after": [
                    "Do not return to burned areas until authorized",
                    "Monitor GSCP (Civil Protection) official channels"
                ],
                "resources": [
                    "Greek Civil Protection (GSCP): www.civilprotection.gr | 112",
                    "Fire brigade: 199",
                    "Emergency: 112"
                ]
            },
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on",
                    "If near coast, move inland immediately after shaking stops — tsunami risk",
                    "Stay away from old stone buildings which may collapse"
                ],
                "after": [
                    "Monitor EMSC (European Mediterranean Seismological Centre) updates",
                    "Follow Greek authorities for aftershock and tsunami warnings"
                ],
                "resources": [
                    "Civil Protection: 112",
                    "Geodynamic Institute: www.gein.noa.gr"
                ]
            }
        ]
    },
    "hr": {
        "risks": ["earthquakes", "wildfires", "flooding", "severe storms", "sea storms"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on",
                    "Evacuate damaged buildings immediately after shaking stops",
                    "Avoid tall buildings, bridges, and coastal areas after major quake"
                ],
                "after": [
                    "Follow DUZS (Civil Protection) instructions",
                    "Report gas leaks by calling 112"
                ],
                "resources": [
                    "Croatian Civil Protection: 112",
                    "Seismological Survey: www.pmf.unizg.hr/geof/seizm"
                ]
            }
        ]
    },
    "hu": {
        "risks": ["flooding", "severe storms", "extreme heat", "drought"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Follow Országos Katasztrófavédelmi Főigazgatóság (OKF) flood alerts",
                    "Move to higher ground if near Danube or Tisza river during flood warnings",
                    "Do not drive through flooded roads",
                    "Follow local authority evacuation instructions"
                ],
                "after": [
                    "Report flood damage to local municipality",
                    "Monitor OKF website for situation updates"
                ],
                "resources": [
                    "National Directorate General for Disaster Management (OKF): www.katasztrofavedelem.hu | 112",
                    "Emergency: 112"
                ]
            }
        ]
    },
    "id": {
        "risks": ["earthquakes", "volcanic eruptions", "tsunamis", "flooding", "wildfires"],
        "protocols": [
            {
                "type": "earthquake / tsunami",
                "immediate": [
                    "Drop, cover, and hold on during earthquake",
                    "If near coast or on low ground after earthquake: DO NOT WAIT — move inland immediately",
                    "Natural tsunami warning: strong earthquake + unusual sea withdrawal = evacuate NOW",
                    "Proceed to nearest Titik Kumpul (assembly point) marked with green signs",
                    "Do not return to coastal areas until BMKG issues all-clear"
                ],
                "after": [
                    "Check BMKG website for aftershock and tsunami updates",
                    "Do not enter damaged buildings",
                    "Contact US Embassy Jakarta: +62-21-5083-1000 if assistance needed"
                ],
                "resources": [
                    "BMKG (Meteorology/Geophysics Agency): www.bmkg.go.id | +62-21-4246-321",
                    "BNPB (Disaster Agency): www.bnpb.go.id | 117",
                    "Emergency: 112"
                ]
            },
            {
                "type": "volcanic eruption",
                "immediate": [
                    "Follow evacuation orders from PVMBG (volcano agency) without delay",
                    "Move upwind of volcanic ash clouds",
                    "Wear N95 or double-layer mask if ash is falling",
                    "Do not drive through thick volcanic ash — engines clog"
                ],
                "after": [
                    "Monitor PVMBG alert levels (1-4) for active volcanoes",
                    "Stay indoors and keep windows closed during ash fall",
                    "Do not re-enter exclusion zone until PVMBG lowers alert level"
                ],
                "resources": [
                    "PVMBG (Volcano Observatory): www.vsi.esdm.go.id",
                    "BNPB: 117",
                    "Emergency: 112"
                ]
            }
        ]
    },
    "in": {
        "risks": ["flooding", "cyclones", "earthquakes", "extreme heat", "air pollution"],
        "protocols": [
            {
                "type": "flooding / cyclone",
                "immediate": [
                    "Monitor IMD (India Meteorological Department) cyclone and flood alerts",
                    "Follow NDMA (National Disaster Management Authority) evacuation orders",
                    "Move to higher ground and away from rivers during floods",
                    "During cyclone: shelter in strongest building, stay away from windows"
                ],
                "after": [
                    "Avoid floodwater — contamination and snake risks after floods",
                    "Follow state SDMA (State Disaster Management Authority) updates",
                    "Contact US Embassy New Delhi: +91-11-2419-8000 if needed"
                ],
                "resources": [
                    "NDMA: www.ndma.gov.in | 1078",
                    "IMD: www.imd.gov.in",
                    "Emergency: 112"
                ]
            }
        ]
    },
    "it": {
        "risks": ["earthquakes", "volcanic eruptions", "flooding", "wildfires", "extreme heat"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on — stay away from windows",
                    "If outdoors, move to open area away from buildings",
                    "Central and southern Italy have high seismic risk",
                    "Do not use elevators"
                ],
                "after": [
                    "Follow Dipartimento della Protezione Civile instructions",
                    "Check for gas leaks before re-entering buildings",
                    "Do not enter damaged buildings"
                ],
                "resources": [
                    "Protezione Civile: www.protezionecivile.gov.it | 800 840 840",
                    "Emergency: 112",
                    "INGV earthquake monitoring: www.ingv.it"
                ]
            }
        ]
    },
    "jp": {
        "risks": ["earthquakes", "tsunamis", "typhoons", "volcanic eruptions", "flooding"],
        "protocols": [
            {
                "type": "earthquake / tsunami",
                "immediate": [
                    "Drop, cover, and hold on — Japan has frequent earthquakes",
                    "Register with J-Alert on your phone for automatic earthquake/tsunami notifications",
                    "After major quake near coast: move to high ground immediately — do not wait for tsunami siren",
                    "Japan's buildings are earthquake-resistant — sheltering inside is usually safer than running out",
                    "Follow tsunami evacuation route signs (blue wave symbols) to nearest high ground"
                ],
                "after": [
                    "Follow NHK World English broadcasts for instructions",
                    "Do not return to coastal areas until JMA (Japan Meteorological Agency) issues all-clear",
                    "Register at evacuation centers for safety checks"
                ],
                "resources": [
                    "Japan Meteorological Agency: www.jma.go.jp",
                    "NHK World (English): www3.nhk.or.jp/nhkworld",
                    "Emergency: 110 (police), 119 (fire/ambulance)",
                    "Safety Tip app (Japan Tourism Agency)"
                ]
            },
            {
                "type": "typhoon",
                "immediate": [
                    "Monitor JMA typhoon forecasts — Japan has very accurate 5-day track predictions",
                    "When Special Warning issued: shelter indoors in strongest room away from windows",
                    "Follow evacuation orders (hinan shiji) from local government immediately",
                    "Identify local evacuation center (hinanjo) before typhoon season"
                ],
                "after": [
                    "Stay indoors for several hours after typhoon passes — trailing side can be equally severe",
                    "Watch for mudslides in mountainous areas after heavy rain"
                ],
                "resources": [
                    "JMA typhoon info: www.jma.go.jp",
                    "Emergency: 110 (police), 119 (fire/ambulance)",
                    "Disaster prevention app: Safety Tip"
                ]
            }
        ]
    },
    "ke": {
        "risks": ["flooding", "drought", "terrorism", "wildlife encounters"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Avoid river banks and low-lying areas during heavy rain",
                    "Do not attempt to cross flooded roads on foot or by vehicle",
                    "Move to higher ground if in flood-prone area",
                    "Follow Kenya Red Cross and local authority alerts"
                ],
                "after": [
                    "Avoid contact with floodwater — leptospirosis and cholera risk",
                    "Boil or purify drinking water after floods"
                ],
                "resources": [
                    "Kenya Red Cross: +254-20-395-0000",
                    "Emergency: 999 or 112",
                    "Kenya Meteorological Department: www.meteo.go.ke"
                ]
            }
        ]
    },
    "kr": {
        "risks": ["typhoons", "flooding", "extreme heat", "earthquakes", "air pollution (yellow dust)"],
        "protocols": [
            {
                "type": "typhoon",
                "immediate": [
                    "Monitor KMA (Korea Meteorological Administration) typhoon warnings",
                    "Secure outdoor items and windows before typhoon arrival",
                    "Stay indoors — do not go outside during active typhoon",
                    "Follow local government emergency alerts (sent via text/app)"
                ],
                "after": [
                    "Watch for flooding and landslides in mountainous areas after typhoon",
                    "Check road conditions before traveling"
                ],
                "resources": [
                    "KMA: www.kma.go.kr",
                    "National Disaster and Safety Portal: www.safekorea.go.kr",
                    "Emergency: 119 (fire/ambulance), 112 (police)"
                ]
            }
        ]
    },
    "lk": {
        "risks": ["flooding", "landslides", "monsoon storms", "tsunamis", "drought"],
        "protocols": [
            {
                "type": "flooding / monsoon",
                "immediate": [
                    "Monitor Department of Meteorology Sri Lanka alerts",
                    "Avoid low-lying areas and river banks during heavy rain",
                    "Do not cross flooded roads on foot — current is deceptive",
                    "Move upstairs if building is flooding"
                ],
                "after": [
                    "Boil drinking water after flooding",
                    "Avoid contact with floodwater — disease risk",
                    "Follow Disaster Management Centre (DMC) instructions"
                ],
                "resources": [
                    "Disaster Management Centre: www.dmc.gov.lk | 117",
                    "Emergency: 119 (ambulance), 110 (police)",
                    "Meteorology Department: www.meteo.gov.lk"
                ]
            }
        ]
    },
    "ma": {
        "risks": ["earthquakes", "extreme heat", "flooding", "sandstorms", "drought"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on",
                    "Morocco has experienced major earthquakes — move to open area if outdoors",
                    "Stay away from old medina walls and structures which may collapse",
                    "Do not re-enter damaged buildings"
                ],
                "after": [
                    "Follow CASC (National Seismic Monitoring) and official government alerts",
                    "Contact US Embassy Rabat: +212-537-637-200 if assistance needed"
                ],
                "resources": [
                    "Protection Civile: 150",
                    "Emergency: 190 (police), 150 (ambulance), 15 (fire)",
                    "CASC seismic alerts: www.iam.net.ma"
                ]
            }
        ]
    },
    "mx": {
        "risks": ["earthquakes", "hurricanes", "volcanic eruptions", "flooding", "wildfires"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "When seismic alarm sounds (unique beeping throughout Mexico City): evacuate immediately to open area",
                    "Drop, cover, and hold on if no time to evacuate",
                    "Stay away from buildings, trees, and power lines when outdoors",
                    "Do not use elevators after earthquake"
                ],
                "after": [
                    "Follow CENAPRED and Mexico City (CDMX) government alerts",
                    "Check for gas leaks before re-entering buildings",
                    "Do not re-enter damaged buildings — aftershocks are common"
                ],
                "resources": [
                    "CENAPRED: www.cenapred.unam.mx",
                    "Mexico City seismic system: alertasismicadf.gob.mx",
                    "Emergency: 911"
                ]
            }
        ]
    },
    "my": {
        "risks": ["flooding", "landslides", "haze (air pollution)", "thunderstorms", "tropical storms"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Monitor JPS (Department of Irrigation and Drainage) flood alerts",
                    "Do not cross flooded roads — depths are deceptive",
                    "Move to higher floors if building is flooding",
                    "Follow evacuation to nearest flood relief center (Pusat Pemindahan Sementara)"
                ],
                "after": [
                    "Boil or purify water after flooding",
                    "Avoid contact with floodwater — leptospirosis risk",
                    "Report flood damage to local authority (Jabatan Kerja Raya)"
                ],
                "resources": [
                    "JPS flood info: www.water.jps.gov.my",
                    "NADMA: www.nadma.gov.my",
                    "Emergency: 999"
                ]
            }
        ]
    },
    "no": {
        "risks": ["avalanches", "flooding", "severe winter storms", "wildfires (summer)"],
        "protocols": [
            {
                "type": "avalanche",
                "immediate": [
                    "Check avalanche forecasts (varsom.no) before skiing or hiking in mountain areas",
                    "If caught in avalanche: try to grab a tree, use swimming motion to stay on top",
                    "Create air pocket in front of face when avalanche stops",
                    "Spit to determine which way is down — dig toward the surface"
                ],
                "after": [
                    "Call 112 immediately if others are buried",
                    "Do not move injured victims unless immediate life threat",
                    "Avalanche rescue is time-critical — survival rate drops after 15 minutes"
                ],
                "resources": [
                    "Norwegian avalanche forecast: www.varsom.no",
                    "Emergency: 112",
                    "Norwegian Red Cross mountain rescue: 113 (medical)"
                ]
            }
        ]
    },
    "nz": {
        "risks": ["earthquakes", "tsunamis", "volcanic eruptions", "wildfires", "flooding"],
        "protocols": [
            {
                "type": "earthquake / tsunami",
                "immediate": [
                    "Drop, cover, and hold on",
                    "Long or strong earthquake near coast = natural tsunami warning: move inland immediately",
                    "Follow NZ tsunami evacuation zone signs (blue and white markers)",
                    "Do not wait for official siren — move immediately"
                ],
                "after": [
                    "Do not return to coastal zone until Civil Defence issues all-clear",
                    "Follow GeoNet and Civil Defence for aftershock and tsunami updates",
                    "Check for gas leaks and structural damage"
                ],
                "resources": [
                    "NZ Civil Defence: www.civildefence.govt.nz | 111",
                    "GeoNet earthquake info: www.geonet.org.nz",
                    "Emergency: 111"
                ]
            }
        ]
    },
    "pe": {
        "risks": ["earthquakes", "tsunamis", "flooding (ENSO)", "landslides", "altitude sickness"],
        "protocols": [
            {
                "type": "earthquake / tsunami",
                "immediate": [
                    "Drop, cover, and hold on — Peru sits on the Pacific Ring of Fire",
                    "After coastal earthquake: move inland immediately — no waiting for official alerts",
                    "Follow INDECI tsunami evacuation route signs",
                    "In Machu Picchu: move to open flat ground away from cliff edges"
                ],
                "after": [
                    "Monitor INDECI and SENAMHI for aftershock and flood warnings",
                    "Be aware of landslide risk on Andean roads after earthquakes"
                ],
                "resources": [
                    "INDECI (Civil Defense): www.indeci.gob.pe | 115",
                    "IGP seismic data: www.igp.gob.pe",
                    "Emergency: 105 (ambulance), 116 (fire), 105 (police)"
                ]
            }
        ]
    },
    "ph": {
        "risks": ["typhoons", "earthquakes", "volcanic eruptions", "flooding", "tsunamis"],
        "protocols": [
            {
                "type": "typhoon",
                "immediate": [
                    "Monitor PAGASA typhoon warnings — Philippines has the highest typhoon frequency globally",
                    "Signal 1: prepare. Signal 2: secure loose items. Signal 3+: evacuate if in flood/storm surge zone",
                    "Never ignore Storm Surge warnings — surge can reach 7+ meters and is more deadly than wind",
                    "Evacuate to designated evacuation centers when ordered"
                ],
                "after": [
                    "Watch for flooding and landslides in the days after typhoon",
                    "Do not cross flooded waterways — leptospirosis risk",
                    "Monitor NDRRMC for recovery advisories"
                ],
                "resources": [
                    "PAGASA typhoon info: www.pagasa.dost.gov.ph",
                    "NDRRMC: www.ndrrmc.gov.ph | 911",
                    "Emergency: 911"
                ]
            },
            {
                "type": "volcanic eruption",
                "immediate": [
                    "Follow PHIVOLCS alert level system (0-5) for active volcanoes",
                    "Alert Level 3+: mandatory evacuation — leave immediately",
                    "Wear N95 mask if volcanic ash is falling",
                    "Do not enter permanent danger zone (PDZ) around active volcanoes"
                ],
                "after": [
                    "Monitor PHIVOLCS for alert level changes",
                    "Do not re-enter evacuated area until PHIVOLCS lowers alert level"
                ],
                "resources": [
                    "PHIVOLCS: www.phivolcs.dost.gov.ph",
                    "NDRRMC: 911"
                ]
            }
        ]
    },
    "pl": {
        "risks": ["flooding", "severe storms", "extreme cold", "wildfires (increasing)"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Follow IMGW-PIB (meteorological institute) flood warnings",
                    "Move away from rivers and low-lying areas during heavy rain",
                    "Do not drive through flooded roads",
                    "Follow local authority (voivodeship) evacuation orders"
                ],
                "after": [
                    "Report damage to WOPR (water rescue service) and local municipality",
                    "Avoid contact with floodwater"
                ],
                "resources": [
                    "IMGW-PIB: www.imgw.pl",
                    "Emergency: 112",
                    "Flood alert service: pogodynka.pl"
                ]
            }
        ]
    },
    "pt": {
        "risks": ["wildfires", "extreme heat", "flooding", "earthquakes", "drought"],
        "protocols": [
            {
                "type": "wildfire",
                "immediate": [
                    "Follow ANEPC (emergency authority) and municipal alerts immediately",
                    "Evacuate when ordered — Portuguese wildfires can move faster than walking pace",
                    "Drive with headlights on in smoky conditions",
                    "Call 112 to report fires immediately"
                ],
                "after": [
                    "Avoid burned areas — unstable trees and toxic ash",
                    "Monitor ANEPC for situation updates"
                ],
                "resources": [
                    "ANEPC: www.prociv.pt | 112",
                    "Forest fire monitoring: fogos.pt",
                    "Emergency: 112"
                ]
            }
        ]
    },
    "se": {
        "risks": ["severe winter storms", "wildfires (summer)", "flooding", "extreme cold"],
        "protocols": [
            {
                "type": "severe winter storm",
                "immediate": [
                    "Monitor SMHI (Swedish Meteorological Institute) storm warnings",
                    "Avoid unnecessary travel during Orange or Red weather warnings",
                    "In blizzard: do not leave vehicle if stranded — stay inside and call 112",
                    "Carry emergency winter kit in car: blanket, warm clothing, water"
                ],
                "after": [
                    "Check roof and structures for snow loading after heavy snowfall",
                    "Clear exits from buildings if snow blocks doors"
                ],
                "resources": [
                    "SMHI: www.smhi.se",
                    "Emergency: 112",
                    "Road conditions: trafikverket.se"
                ]
            }
        ]
    },
    "sg": {
        "risks": ["haze (transboundary air pollution)", "flooding", "tropical thunderstorms"],
        "protocols": [
            {
                "type": "haze / air pollution",
                "immediate": [
                    "Monitor NEA PSI (Pollution Standards Index) readings hourly during haze periods",
                    "PSI 101-200 (Unhealthy): minimize outdoor activity, wear N95 mask outdoors",
                    "PSI 201-300 (Very Unhealthy): stay indoors, all outdoor exercise should stop",
                    "PSI >300 (Hazardous): avoid all outdoor exposure, seal windows and doors"
                ],
                "after": [
                    "PSI readings available on myENV app",
                    "Haze typically improves with wind direction changes — monitor NEA forecasts"
                ],
                "resources": [
                    "NEA haze info: www.haze.gov.sg",
                    "myENV app for real-time PSI",
                    "Emergency: 995 (ambulance), 999 (police)"
                ]
            }
        ]
    },
    "th": {
        "risks": ["flooding", "tropical storms", "extreme heat", "tsunamis (Andaman coast)"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Monitor Thai Meteorological Department (TMD) and DDPM flood alerts",
                    "Do not drive through flooded streets — Bangkok floods can exceed vehicle height",
                    "Move to upper floors of hotel or building if in flood-prone area",
                    "Follow instructions from hotel staff during monsoon flooding"
                ],
                "after": [
                    "Avoid contact with floodwater — leptospirosis risk",
                    "Check road and transport conditions before traveling"
                ],
                "resources": [
                    "DDPM (Department of Disaster Prevention): www.disaster.go.th | 1784",
                    "Thai Meteorological Department: www.tmd.go.th",
                    "Emergency: 191 (police), 1669 (ambulance), 199 (fire)"
                ]
            }
        ]
    },
    "tr": {
        "risks": ["earthquakes", "wildfires", "flooding", "extreme heat"],
        "protocols": [
            {
                "type": "earthquake",
                "immediate": [
                    "Drop, cover, and hold on — Turkey is in a major earthquake zone",
                    "Stay away from exterior walls and windows",
                    "If outdoors, move to open ground away from buildings",
                    "Prepare an emergency bag (earthquake kit) before travel to earthquake-prone regions"
                ],
                "after": [
                    "Follow AFAD (Disaster and Emergency Management Authority) instructions",
                    "Do not re-enter buildings until structurally cleared",
                    "Call AFAD coordination center: 122"
                ],
                "resources": [
                    "AFAD: www.afad.gov.tr | 122",
                    "KANDILLI seismic observatory: www.koeri.boun.edu.tr",
                    "Emergency: 112"
                ]
            }
        ]
    },
    "tz": {
        "risks": ["flooding", "drought", "malaria", "wildlife encounters (safari)"],
        "protocols": [
            {
                "type": "flooding",
                "immediate": [
                    "Move to higher ground during heavy rain",
                    "Do not cross flooded roads or streams",
                    "Follow Tanzania Red Cross and local authority guidance"
                ],
                "after": [
                    "Boil or purify drinking water after flooding",
                    "Avoid contact with floodwater — cholera and leptospirosis risk",
                    "Seek medical attention promptly if showing signs of waterborne illness"
                ],
                "resources": [
                    "Tanzania Meteorological Authority: www.meteo.go.tz",
                    "Emergency: 112",
                    "Tanzania Red Cross: +255-22-212-3985"
                ]
            }
        ]
    },
    "us": {
        "risks": ["hurricanes", "tornadoes", "wildfires", "flooding", "earthquakes", "extreme heat"],
        "protocols": [
            {
                "type": "hurricane",
                "immediate": [
                    "Follow mandatory evacuation orders — do not ignore them",
                    "Prepare emergency kit: water (1 gal/person/day for 3 days), food, medications, documents",
                    "If sheltering in place: go to interior room on lowest floor away from windows",
                    "Never drive through flooded roads — 'Turn Around, Don't Drown'"
                ],
                "after": [
                    "Do not return until local authorities declare area safe",
                    "Avoid downed power lines and flooded streets",
                    "Document damage for FEMA and insurance claims"
                ],
                "resources": [
                    "National Hurricane Center: www.nhc.noaa.gov",
                    "FEMA: www.fema.gov | 1-800-621-3362",
                    "Emergency: 911"
                ]
            },
            {
                "type": "tornado",
                "immediate": [
                    "Go immediately to basement or interior room on lowest floor",
                    "Avoid windows, exterior walls, and mobile homes",
                    "If driving: do not try to outrun — leave vehicle and lie flat in low ditch away from trees",
                    "Cover head and neck with arms"
                ],
                "after": [
                    "Watch for downed power lines and structural hazards",
                    "Do not enter damaged buildings until inspected"
                ],
                "resources": [
                    "National Weather Service: www.weather.gov",
                    "Wireless Emergency Alerts on all US phones",
                    "Emergency: 911"
                ]
            }
        ]
    },
    "vn": {
        "risks": ["typhoons", "flooding", "landslides", "tropical storms", "extreme heat"],
        "protocols": [
            {
                "type": "typhoon / flooding",
                "immediate": [
                    "Monitor NCHMF (National Center for Hydro-Meteorological Forecasting) alerts",
                    "Central Vietnam coast is most prone to typhoons (September-November)",
                    "During typhoon warning: shelter in solid building, away from windows",
                    "Do not drive during active typhoon — flooded roads can conceal dangerous depths"
                ],
                "after": [
                    "Watch for flooding and landslides in mountainous areas (Sapa, Hội An)",
                    "Avoid contact with floodwater — disease risk",
                    "Follow local government and hotel instructions for updates"
                ],
                "resources": [
                    "NCHMF: www.nchmf.gov.vn",
                    "Emergency: 113 (police), 115 (ambulance), 114 (fire)",
                    "US Embassy Hanoi: +84-24-3850-5000"
                ]
            }
        ]
    },
    "za": {
        "risks": ["flooding", "wildfires", "drought", "severe thunderstorms", "crime"],
        "protocols": [
            {
                "type": "flooding / severe storm",
                "immediate": [
                    "Monitor South African Weather Service (SAWS) storm warnings",
                    "Move vehicles to high ground during flash flood alerts",
                    "Do not cross flooded roads or low-water bridges",
                    "Follow NDMC (National Disaster Management Centre) advisories"
                ],
                "after": [
                    "Report flood damage to local municipality",
                    "Avoid contact with floodwater — disease risk",
                    "Monitor SAWS for ongoing severe weather"
                ],
                "resources": [
                    "South African Weather Service: www.weathersa.co.za",
                    "NDMC: www.ndmc.gov.za",
                    "Emergency: 10111 (police), 10177 (ambulance), 112 (mobile)"
                ]
            }
        ]
    }
}

COUNTRIES = [
    "ar", "au", "br", "cl", "cn", "co", "cr", "cz", "de", "eg",
    "es", "fr", "gb", "gr", "hr", "hu", "id", "in", "it", "jp",
    "ke", "kr", "lk", "ma", "mx", "my", "no", "nz", "pe", "ph",
    "pl", "pt", "se", "sg", "th", "tr", "tz", "us", "vn", "za"
]


def patch_country(iso2: str) -> bool:
    filepath = SAFETY_DIR / f"{iso2}.json"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "hospitals" in data and "disasterResponse" in data:
        print(f"  SKIP {iso2}: already has hospitals + disasterResponse")
        return False

    hospitals = HOSPITALS_DATA.get(iso2)
    disaster = DISASTER_RESPONSE_DATA.get(iso2)

    if not hospitals:
        print(f"  WARN {iso2}: no hospital data defined")
    if not disaster:
        print(f"  WARN {iso2}: no disaster response data defined")

    # Rebuild the dict with hospitals and disasterResponse inserted after 'practical'
    new_data = {}
    for key, value in data.items():
        new_data[key] = value
        if key == "practical":
            if hospitals:
                new_data["hospitals"] = hospitals
            if disaster:
                new_data["disasterResponse"] = disaster

    # If 'practical' was not found, append at end
    if "hospitals" not in new_data and hospitals:
        new_data["hospitals"] = hospitals
    if "disasterResponse" not in new_data and disaster:
        new_data["disasterResponse"] = disaster

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"  PATCHED {iso2}: added hospitals ({len(hospitals) if hospitals else 0}) + disasterResponse")
    return True


def main():
    print(f"Patching {len(COUNTRIES)} country files in {SAFETY_DIR}\n")
    patched = 0
    for iso2 in COUNTRIES:
        result = patch_country(iso2)
        if result:
            patched += 1
    print(f"\nDone. Patched {patched}/{len(COUNTRIES)} files.")


if __name__ == "__main__":
    main()
