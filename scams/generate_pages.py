#!/usr/bin/env python3
"""Generate scam pages for all cities based on Barcelona template."""
import json
import os

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
    for batch_file in ["batch1.json", "batch2.json", "batch3.json", "batch5.json"]:
        path = os.path.join(base_dir, "research", batch_file)
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
