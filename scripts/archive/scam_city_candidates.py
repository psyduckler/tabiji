#!/usr/bin/env python3
"""
Comprehensive list of 300+ tourist destination cities for scam-related
keyword research. Compiled from multiple angles:

1. Top 100 most-visited cities globally (UNWTO / Euromonitor / Mastercard)
2. Top cruise port cities
3. Popular backpacker / budget travel cities
4. Major pilgrimage / religious tourism cities
5. Popular beach / resort cities
6. Emerging tourism destinations

Focus: cities tourists actually visit, not just large cities.
Disambiguated with country where needed.
"""

SCAM_CITY_CANDIDATES = [
    # =========================================================================
    # 1. TOP MOST-VISITED CITIES GLOBALLY
    #    (Euromonitor Top 100 / Mastercard Global Destinations Cities Index)
    # =========================================================================
    "Bangkok",
    "Paris",
    "London",
    "Dubai",
    "Singapore",
    "Kuala Lumpur",
    "New York City",
    "Istanbul",
    "Tokyo",
    "Antalya",
    "Seoul",
    "Osaka",
    "Mecca",
    "Phuket",
    "Pattaya",
    "Milan",
    "Barcelona",
    "Palma de Mallorca",
    "Bali",
    "Hong Kong",
    "Rome",
    "Taipei",
    "Prague",
    "Amsterdam",
    "Miami",
    "Vienna",
    "Los Angeles",
    "Medina",
    "Ho Chi Minh City",
    "Lisbon",
    "Dublin",
    "Munich",
    "Delhi",
    "Athens",
    "Riyadh",
    "Cancun",
    "Budapest",
    "San Francisco",
    "Macau",
    "Shanghai",
    "Beijing",
    "Shenzhen",
    "Guangzhou",
    "Florence",
    "Venice",
    "Edinburgh",
    "Madrid",
    "Las Vegas",
    "Sydney",
    "Melbourne",
    "Toronto",
    "Vancouver",
    "Doha",
    "Abu Dhabi",
    "Johannesburg",
    "Cape Town",
    "Buenos Aires",
    "Rio de Janeiro",
    "Moscow",
    "St. Petersburg (Russia)",
    "Kyoto",
    "Hanoi",
    "Da Nang",
    "Chiang Mai",
    "Phnom Penh",
    "Siem Reap",
    "Manila",
    "Cebu",
    "Jakarta",
    "Yogyakarta",
    "Colombo",
    "Agra",
    "Jaipur",
    "Mumbai",
    "Goa",
    "Cairo",
    "Marrakech",
    "Nairobi",
    "Dar es Salaam",
    "Addis Ababa",
    "Casablanca",
    "Tunis",
    "Lima",
    "Bogota",
    "Mexico City",
    "Havana",
    "Cusco",
    "Santiago",
    "Cartagena (Colombia)",
    "Medellin",
    "Krakow",
    "Warsaw",
    "Bucharest",
    "Sofia",
    "Brussels",
    "Copenhagen",
    "Oslo",
    "Stockholm",
    "Helsinki",
    "Tallinn",
    "Riga",
    "Vilnius",

    # =========================================================================
    # 2. TOP CRUISE PORT CITIES
    # =========================================================================
    "Nassau",
    "Cozumel",
    "Grand Cayman",
    "St. Thomas",
    "San Juan",
    "St. Maarten",
    "Roatan",
    "Montego Bay",
    "Ocho Rios",
    "Aruba",
    "Curacao",
    "Labadee",
    "Key West",
    "Juneau",
    "Ketchikan",
    "Skagway",
    "Civitavecchia",  # cruise port for Rome
    "Piraeus",        # cruise port for Athens
    "Dubrovnik",
    "Kotor",
    "Split",
    "Mykonos",
    "Santorini",
    "Heraklion",
    "Rhodes",
    "Valletta",
    "Marseille",
    "Nice",
    "Livorno",        # cruise port for Florence/Pisa
    "Naples",
    "Palermo",
    "Malaga",
    "Cadiz",
    "Lisbon",         # also cruise port
    "Funchal",
    "Southampton",
    "Bergen",
    "Reykjavik",
    "Tallinn",        # also cruise port
    "St. Petersburg (Russia)",  # also cruise port
    "Kusadasi",
    "Bodrum",
    "Muscat",

    # =========================================================================
    # 3. POPULAR BACKPACKER / BUDGET TRAVEL CITIES
    # =========================================================================
    "Kathmandu",
    "Pokhara",
    "Vientiane",
    "Luang Prabang",
    "Pai",
    "Krabi",
    "Koh Samui",
    "Koh Phangan",
    "Hoi An",
    "Nha Trang",
    "Dalat",
    "Ella (Sri Lanka)",
    "Kandy",
    "Galle",
    "Kampot",
    "Sihanoukville",
    "El Nido",
    "Siargao",
    "Ubud",
    "Seminyak",
    "Lombok",
    "Penang",
    "Langkawi",
    "Kuching",
    "Kota Kinabalu",
    "Mandalay",
    "Bagan",
    "Yangon",
    "La Paz",
    "Sucre",
    "Quito",
    "Guayaquil",
    "San Pedro de Atacama",
    "Valparaiso",
    "Antigua (Guatemala)",
    "San Cristobal de las Casas",
    "Oaxaca",
    "Playa del Carmen",
    "Tulum",
    "Granada (Nicaragua)",
    "León (Nicaragua)",
    "San José (Costa Rica)",
    "Tamarindo",
    "Panama City",
    "Bocas del Toro",
    "Fez",
    "Chefchaouen",
    "Essaouira",
    "Zanzibar",
    "Stone Town",
    "Arusha",
    "Cape Town",        # also backpacker hub
    "Durban",
    "Maputo",
    "Windhoek",
    "Livingstone",      # Victoria Falls
    "Belgrade",
    "Sarajevo",
    "Mostar",
    "Tirana",
    "Shkoder",
    "Ohrid",
    "Tbilisi",
    "Yerevan",
    "Baku",

    # =========================================================================
    # 4. MAJOR PILGRIMAGE / RELIGIOUS TOURISM CITIES
    # =========================================================================
    "Mecca",
    "Medina",
    "Jerusalem",
    "Vatican City",
    "Varanasi",
    "Haridwar",
    "Rishikesh",
    "Amritsar",
    "Bodh Gaya",
    "Tirupati",
    "Lourdes",
    "Fatima",
    "Santiago de Compostela",
    "Assisi",
    "Bethlehem",
    "Lhasa",
    "Kandy",              # Temple of the Tooth
    "Luang Prabang",      # Buddhist temples
    "Angkor Wat area",    # covered by Siem Reap
    "Shirdi",
    "Karbala",
    "Najaf",
    "Konya",

    # =========================================================================
    # 5. POPULAR BEACH / RESORT CITIES
    # =========================================================================
    # Caribbean & Central America
    "Punta Cana",
    "Negril",
    "Bridgetown",
    "Kralendijk",
    "Turks and Caicos",
    "Cabo San Lucas",
    "Puerto Vallarta",
    "Huatulco",
    "Belize City",
    "Ambergris Caye",
    "Roatan",

    # Mediterranean
    "Bodrum",
    "Fethiye",
    "Marmaris",
    "Alanya",
    "Dubrovnik",
    "Hvar",
    "Zadar",
    "Corfu",
    "Zakynthos",
    "Ibiza",
    "Tenerife",
    "Gran Canaria",
    "Lanzarote",
    "Algarve",
    "Amalfi",
    "Taormina",
    "Sardinia",
    "Cinque Terre",
    "Nice",
    "Saint-Tropez",
    "Monaco",
    "Budva",
    "Saranda",

    # Southeast Asia beaches
    "Boracay",
    "Koh Lipe",
    "Koh Tao",
    "Langkawi",
    "Perhentian Islands",
    "Nusa Penida",
    "Gili Islands",
    "Sihanoukville",
    "Phu Quoc",

    # Indian Ocean
    "Maldives",
    "Mauritius",
    "Seychelles",
    "Zanzibar",

    # Pacific
    "Fiji",
    "Bora Bora",
    "Honolulu",
    "Maui",

    # Africa
    "Hurghada",
    "Sharm el-Sheikh",
    "Djerba",

    # South America
    "Florianopolis",
    "Cartagena (Colombia)",
    "Santa Marta",

    # =========================================================================
    # 6. EMERGING TOURISM DESTINATIONS
    # =========================================================================
    "Tashkent",
    "Samarkand",
    "Bukhara",
    "Almaty",
    "Bishkek",
    "Dushanbe",
    "Tbilisi",          # Georgia boom
    "Batumi",
    "Yerevan",
    "Baku",
    "Muscat",
    "Salalah",
    "Jeddah",
    "AlUla",
    "NEOM",
    "Riyadh",
    "Luanda",
    "Kigali",
    "Kampala",
    "Lagos",
    "Accra",
    "Dakar",
    "Abidjan",
    "Lusaka",
    "Harare",
    "Antananarivo",
    "Nosy Be",
    "São Paulo",
    "Salvador",
    "Montevideo",
    "Asuncion",
    "Georgetown (Guyana)",
    "Paramaribo",
    "Tirana",
    "Pristina",
    "Skopje",
    "Podgorica",
    "Lviv",
    "Kyiv",
    "Minsk",
    "Chisinau",
    "Bratislava",
    "Ljubljana",
    "Zagreb",
    "Novi Sad",

    # =========================================================================
    # 7. ADDITIONAL HIGH-TOURIST-TRAFFIC CITIES
    #    (filling gaps from major tourism corridors)
    # =========================================================================
    # Western Europe extras
    "Berlin",
    "Porto",
    "Seville",
    "Granada (Spain)",
    "Bilbao",
    "Valencia",
    "Bruges",
    "Ghent",
    "Salzburg",
    "Innsbruck",
    "Zurich",
    "Geneva",
    "Lucerne",
    "Interlaken",
    "Lyon",
    "Bordeaux",
    "Strasbourg",
    "Hamburg",
    "Frankfurt",
    "Cologne",
    "Dresden",
    "Nuremberg",
    "Rothenburg ob der Tauber",
    "The Hague",
    "Rotterdam",

    # UK & Ireland extras
    "Bath",
    "Oxford",
    "Cambridge",
    "York",
    "Liverpool",
    "Belfast",
    "Galway",

    # Scandinavia extras
    "Gothenburg",
    "Bergen",
    "Tromso",
    "Rovaniemi",

    # Eastern Europe extras
    "Gdansk",
    "Wroclaw",
    "Poznan",
    "Cesky Krumlov",
    "Brno",
    "Bratislava",
    "Dubrovnik",
    "Sibiu",
    "Cluj-Napoca",
    "Brasov",
    "Plovdiv",

    # Middle East extras
    "Amman",
    "Petra",
    "Aqaba",
    "Tel Aviv",
    "Haifa",
    "Beirut",
    "Muscat",

    # East Asia extras
    "Hiroshima",
    "Nara",
    "Fukuoka",
    "Sapporo",
    "Okinawa",
    "Busan",
    "Jeju",
    "Kaohsiung",
    "Tainan",
    "Hangzhou",
    "Chengdu",
    "Xi'an",
    "Guilin",
    "Lijiang",
    "Lhasa",

    # South Asia extras
    "Udaipur",
    "Jodhpur",
    "Kochi",
    "Chennai",
    "Kolkata",
    "Kathmandu",
    "Lumbini",
    "Thimphu",
    "Paro",
    "Dhaka",

    # Africa extras
    "Luxor",
    "Aswan",
    "Marrakech",
    "Tangier",
    "Tunis",
    "Sidi Bou Said",
    "Victoria Falls",
    "Maun",           # Okavango Delta gateway
    "Swakopmund",
    "Lamu",
    "Mombasa",
    "Entebbe",
    "Addis Ababa",

    # Latin America extras
    "Guatemala City",
    "Flores (Guatemala)",
    "San Salvador",
    "Tegucigalpa",
    "Managua",
    "David (Panama)",
    "Mérida (Mexico)",
    "Guadalajara",
    "San Miguel de Allende",
    "Puerto Escondido",
    "Bariloche",
    "Mendoza",
    "Iguazu Falls",
    "La Paz",
    "Uyuni",
    "Galapagos Islands",
    "Arequipa",
    "Huaraz",
    "Bogota",
    "Cali",
    "Pereira",
    # "Medellín",  # duplicate of Medellin above
    "São Paulo",

    # Oceania extras
    "Auckland",
    "Queenstown",
    "Rotorua",
    "Christchurch",
    "Wellington",
    "Gold Coast",
    "Cairns",
    "Perth",
    "Brisbane",
    "Adelaide",

    # North America extras
    "Chicago",
    "Washington DC",
    "Boston",
    "New Orleans",
    "Nashville",
    "Austin",
    "San Diego",
    "Seattle",
    "Portland (Oregon)",
    "Denver",
    "Orlando",
    "Montreal",
    "Quebec City",
    "Ottawa",
    "Niagara Falls",
    "Havana",
]


def deduplicate(city_list):
    """Remove duplicates while preserving order."""
    seen = set()
    unique = []
    for city in city_list:
        normalized = city.strip().lower()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(city.strip())
    return unique


SCAM_CITY_CANDIDATES = deduplicate(SCAM_CITY_CANDIDATES)

if __name__ == "__main__":
    print(f"Total unique cities: {len(SCAM_CITY_CANDIDATES)}")
    print("=" * 60)
    for i, city in enumerate(SCAM_CITY_CANDIDATES, 1):
        print(f"  {i:3d}. {city}")
