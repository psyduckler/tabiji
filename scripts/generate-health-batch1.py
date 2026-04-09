#!/usr/bin/env python3
"""
Generate health data JSON files for 25 new countries (batch 1).
Run from repo root: python scripts/generate-health-batch1.py
"""

import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "health-data")

COUNTRIES = {
    "CN": {
        "iso2": "CN",
        "countryName": "China",
        "countrySlug": "china",
        "flag": "🇨🇳",
        "emergencyNumber": "120 (ambulance), 110 (police), 119 (fire)",
        "healthcareSystem": "Mixed public-private system. Public hospitals are the backbone, but tourists typically pay out-of-pocket at international departments.",
        "healthcareSystemType": "mixed",
        "qualityRating": 4,
        "qualityNotes": "Tier-1 cities (Beijing, Shanghai, Guangzhou) have world-class hospitals with international wings. Rural areas have limited resources. Overcrowding is common at public hospitals. VIP/international departments offer faster, English-friendly service.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies open 8:30am-9pm daily. 24/7 pharmacies available in major cities.",
        "pharmacyTips": "Look for green cross signs or chains like Guoda Pharmacy (国大药房) and Tongjitang (同济堂). Many OTC medicines are available without prescription. Pharmacists rarely speak English — use a translation app or bring written Chinese.",
        "commonOTC": [
            "ibuprofen (布洛芬)",
            "paracetamol/acetaminophen (对乙酰氨基酚)",
            "cold medicine (感冒药)",
            "stomach/digestive medicine (胃药)",
            "allergy medication (抗过敏药)",
            "band-aids and basic first aid supplies"
        ],
        "prescriptionRules": "Many medications that require prescriptions in Western countries are available OTC in China. However, antibiotics officially require a prescription. Foreign prescriptions are not accepted — you need a Chinese doctor's prescription for controlled medicines.",
        "restrictedMeds": [
            {
                "name": "Pseudoephedrine-containing medications",
                "status": "restricted",
                "note": "Strictly controlled due to methamphetamine precursor laws. Bring only small personal quantities with documentation."
            },
            {
                "name": "Opioid-based painkillers (codeine, tramadol)",
                "status": "controlled",
                "note": "Require documentation. Bring a doctor's letter and keep in original packaging. Large quantities may be confiscated."
            },
            {
                "name": "Psychotropic medications (benzodiazepines, ADHD stimulants)",
                "status": "controlled",
                "note": "Bring a doctor's letter in English and Chinese if possible. Quantities should not exceed personal use for trip duration."
            },
            {
                "name": "Medical cannabis / CBD products",
                "status": "banned",
                "note": "Cannabis in any form is strictly illegal in China. CBD products containing any THC are prohibited."
            }
        ],
        "bringDocumentation": "Carry a bilingual (English/Chinese) doctor's letter listing all medications with generic names. Keep all medicines in original packaging. For controlled substances, carry only trip-duration quantities.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-60/week",
            "tips": "Hospitals require upfront payment (cash, WeChat Pay, or Alipay preferred — credit cards often not accepted outside international departments). Travel insurance with direct billing to international hospital departments is highly recommended."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Japanese Encephalitis (for rural or prolonged stays)",
                "Rabies (for adventure travelers or rural areas)"
            ],
            "notes": "No mandatory vaccinations for most travelers. Ensure routine vaccinations (MMR, tetanus, polio) are up to date."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do not drink tap water in China. Boiled water is safe and widely available (hotels provide electric kettles). Bottled water is inexpensive and available everywhere. Avoid ice in drinks outside high-end establishments.",
        "foodSafetyTips": "Eat freshly cooked food from busy restaurants. Street food is generally safe if cooked to order. Avoid raw vegetables and salads from questionable sources. Wash or peel fruits yourself. Stick to busy, popular food stalls.",
        "medicalTourismNote": "China is an emerging medical tourism destination, particularly for Traditional Chinese Medicine (TCM), dental care, and certain surgical procedures in Shanghai and Beijing.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Beijing",
            "China National Health Commission",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to China. Emergency numbers (120/110/119), pharmacy tips, restricted medications, vaccination info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Beijing United Family Hospital",
                "nearTouristArea": "Chaoyang District, Beijing (near embassies)",
                "phone": "+86-10-5927-7000",
                "englishSpeaking": True,
                "notes": "International-standard private hospital. Direct insurance billing. Major credit cards accepted."
            },
            {
                "name": "Shanghai United Family Hospital",
                "nearTouristArea": "Changning District, Shanghai",
                "phone": "+86-21-2216-3900",
                "englishSpeaking": True,
                "notes": "Full-service international hospital. 24/7 emergency department."
            },
            {
                "name": "Peking Union Medical College Hospital (International Dept)",
                "nearTouristArea": "Dongcheng District, Beijing (near Tiananmen/Wangfujing)",
                "phone": "+86-10-6915-6114",
                "englishSpeaking": True,
                "notes": "One of China's top-ranked public hospitals. International department has English-speaking staff."
            },
            {
                "name": "Guangzhou Global Doctor Clinic",
                "nearTouristArea": "Tianhe District, Guangzhou",
                "phone": "+86-20-2886-7908",
                "englishSpeaking": True,
                "notes": "Foreign-run clinic catering to expats and tourists. Appointments recommended."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "我需要头痛药",
                "transliteration": "Wǒ xūyào tóutòng yào"
            },
            {
                "english": "I have a stomachache",
                "local": "我肚子疼",
                "transliteration": "Wǒ dùzi téng"
            },
            {
                "english": "I'm allergic to...",
                "local": "我对...过敏",
                "transliteration": "Wǒ duì...guòmǐn"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "最近的药店在哪里？",
                "transliteration": "Zuìjìn de yàodiàn zài nǎlǐ?"
            },
            {
                "english": "I need a doctor",
                "local": "我需要看医生",
                "transliteration": "Wǒ xūyào kàn yīshēng"
            }
        ],
        "dentalCare": {
            "availability": "Dental care is widely available in major cities. International dental clinics in Beijing, Shanghai, and Guangzhou offer high-quality care.",
            "costRange": "¥200-800 ($30-110) for a basic consultation; ¥500-3,000 ($70-420) for fillings or extractions",
            "notes": "Arrail Dental and Jiamei Dental are reputable chains with English-speaking dentists in major cities.",
            "emergencyTip": "For dental emergencies, visit a major hospital's dental department. International clinics may have limited weekend hours — call ahead."
        },
        "mentalHealth": {
            "crisisLine": "400-161-9995 (Beijing Psychological Crisis Research and Intervention Center, 24/7)",
            "internationalLine": "Beijing: 010-8295-1332 (International SOS 24-hour assistance)",
            "englishTherapists": "Available in Beijing, Shanghai, and Guangzhou through international clinics. Expect ¥800-2,000 ($110-280) per session.",
            "notes": "English-language mental health services are limited to major cities. International SOS and United Family hospitals offer counseling services."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is improving rapidly in major cities but remains limited in smaller towns and rural areas.",
            "hospitalAccess": "Major international hospitals and new public hospitals are wheelchair accessible. Older hospitals may have limited accessibility.",
            "transport": "Beijing and Shanghai metros have elevators at most stations. Accessible taxis are limited — use Didi app to request wheelchair-accessible vehicles.",
            "tips": "New attractions and hotels generally meet accessibility standards. Older tourist sites (Great Wall, temples) may have significant barriers. Plan ahead and contact attractions directly."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "Masks are no longer required but remain common in healthcare settings and on public transit.",
            "testing": "PCR and antigen tests available at hospitals and designated testing sites. Cost: ¥50-200 ($7-28).",
            "notes": "China lifted COVID entry restrictions in early 2023. Healthcare facilities may still require masks."
        },
        "insuranceClaimProcess": "Chinese hospitals typically require upfront payment. Keep all receipts (发票 fāpiào) and request an English medical certificate. International departments at major hospitals can provide documentation for insurance claims. File claims with your insurer within 30 days."
    },
    "DK": {
        "iso2": "DK",
        "countryName": "Denmark",
        "countrySlug": "denmark",
        "flag": "🇩🇰",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal tax-funded healthcare (primarily for residents). EU/EEA citizens can use EHIC for public healthcare. Non-EU tourists should have travel insurance.",
        "healthcareSystemType": "universal",
        "qualityRating": 5,
        "qualityNotes": "Excellent healthcare system with modern facilities. Most doctors speak fluent English. Wait times for non-emergencies can be long. Emergency care is provided to all regardless of insurance status.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies (apotek) open Mon-Fri 9am-6pm, Sat 9am-2pm. Some 24/7 pharmacies in Copenhagen.",
        "pharmacyTips": "Look for the green 'A' sign for pharmacies (apotek). Steno Apotek in Copenhagen is open 24/7. Pharmacists speak excellent English. Denmark has a strong tradition of pharmacist consultation.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol (Panodil)",
            "cold and flu remedies",
            "antacids and stomach remedies",
            "antihistamines",
            "band-aids and basic first aid"
        ],
        "prescriptionRules": "Denmark follows strict EU prescription requirements. Most medications beyond basic OTC require a Danish prescription. Foreign prescriptions from EU/EEA countries may be honored if they meet EU standards.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Available only by prescription. Bring documentation if carrying personal supply."
            },
            {
                "name": "Strong opioids (morphine, oxycodone)",
                "status": "controlled",
                "note": "Strictly controlled. Requires a Schengen certificate for EU travel or doctor's documentation for non-EU travelers."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substance. Carry a doctor's letter and keep in original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Medical cannabis available by prescription only. Recreational cannabis is illegal. CBD products must meet EU regulations."
            }
        ],
        "bringDocumentation": "EU/EEA travelers carrying controlled substances should obtain a Schengen certificate from their home country. Non-EU travelers should carry a doctor's letter in English. Keep all medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry their EHIC/GHI card for coverage.",
            "averageCost": "$50-90/week",
            "tips": "Denmark is one of the most expensive countries for healthcare. Even with EHIC, supplemental insurance is recommended for non-emergency care and repatriation."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (if visiting rural/forested areas in summer)"
            ],
            "notes": "No mandatory vaccinations. Denmark is a low-risk destination. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is excellent quality throughout Denmark and safe to drink everywhere.",
        "foodSafetyTips": "Denmark has very high food safety standards. All food establishments are regularly inspected (look for the smiley face rating system). Raw preparations like herring and smørrebrød are safe from reputable sources.",
        "medicalTourismNote": "Denmark is known for fertility treatments and cancer research. Copenhagen hosts several internationally recognized research hospitals.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Copenhagen",
            "Danish Health Authority (Sundhedsstyrelsen)",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Denmark. Emergency number 112, pharmacy tips, medication rules, healthcare system info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Rigshospitalet",
                "nearTouristArea": "Central Copenhagen (near Fælledparken)",
                "phone": "+45 35 45 35 45",
                "englishSpeaking": True,
                "notes": "Denmark's largest and most specialized hospital. National trauma center. English widely spoken."
            },
            {
                "name": "Bispebjerg Hospital",
                "nearTouristArea": "Nordvest, Copenhagen",
                "phone": "+45 38 63 50 00",
                "englishSpeaking": True,
                "notes": "Major public hospital with emergency department. Good accessibility."
            },
            {
                "name": "Aarhus University Hospital (Skejby)",
                "nearTouristArea": "Aarhus (central Jutland)",
                "phone": "+45 78 45 00 00",
                "englishSpeaking": True,
                "notes": "Largest hospital in western Denmark. Full emergency services."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Jeg har brug for hovedpinepiller",
                "transliteration": "Yai har broo for ho-veth-pee-neh-pil-er"
            },
            {
                "english": "I have a stomachache",
                "local": "Jeg har ondt i maven",
                "transliteration": "Yai har ont ee ma-ven"
            },
            {
                "english": "I'm allergic to...",
                "local": "Jeg er allergisk over for...",
                "transliteration": "Yai air al-AIR-gisk oh-ver for..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Hvor er det nærmeste apotek?",
                "transliteration": "Vor air deh NAIR-mes-teh ah-po-TEHK?"
            },
            {
                "english": "I need a doctor",
                "local": "Jeg har brug for en læge",
                "transliteration": "Yai har broo for en LAI-eh"
            }
        ],
        "dentalCare": {
            "availability": "High-quality dental care available throughout Denmark. Most dentists speak English.",
            "costRange": "DKK 500-1,500 ($70-220) for a consultation; DKK 1,000-5,000 ($145-725) for fillings or extractions",
            "notes": "Dental care in Denmark is expensive and generally not covered by public healthcare for adults. Book in advance.",
            "emergencyTip": "For dental emergencies, contact Tandlægevagten (dental emergency service) in Copenhagen at +45 35 38 02 51. Available evenings and weekends."
        },
        "mentalHealth": {
            "crisisLine": "70 201 201 (Livslinien — crisis support, daily 11am-5am)",
            "internationalLine": "Psychiatric emergency: 112 or go to nearest hospital emergency department",
            "englishTherapists": "Available in Copenhagen. Many Danish psychologists speak English. Expect DKK 800-1,500 ($115-220) per session.",
            "notes": "Denmark has good mental health services. Psykiatrifonden provides resources and referrals. English-speaking therapists are common in Copenhagen."
        },
        "accessibilityInfo": {
            "overview": "Denmark has excellent accessibility infrastructure. Disability access is mandated by law in public buildings and transport.",
            "hospitalAccess": "All hospitals are fully wheelchair accessible with accessible restrooms and signage.",
            "transport": "Copenhagen metro, buses, and trains are wheelchair accessible. Copenhagen is very bike-friendly but sidewalk curb cuts are standard. Accessible taxis available.",
            "tips": "VisitDenmark.com has accessibility guides. Copenhagen is flat and easy to navigate. Most museums, attractions, and hotels meet high accessibility standards."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements. Masks are rarely worn.",
            "testing": "Tests available at pharmacies and clinics if needed.",
            "notes": "Denmark was one of the first countries to lift all COVID restrictions. No special measures remain."
        },
        "insuranceClaimProcess": "For public hospital treatment, EU/EEA citizens present their EHIC card. Non-EU visitors pay upfront and claim from insurance. Keep all receipts and request English-language medical documentation. Danish hospitals provide detailed invoices suitable for insurance claims."
    },
    "FI": {
        "iso2": "FI",
        "countryName": "Finland",
        "countrySlug": "finland",
        "flag": "🇫🇮",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal tax-funded healthcare. EU/EEA citizens can use EHIC. Non-EU tourists pay for services but at subsidized rates at public facilities.",
        "healthcareSystemType": "universal",
        "qualityRating": 5,
        "qualityNotes": "Excellent healthcare with modern facilities. English widely spoken by medical professionals. Wait times for non-emergencies can be long in public system. Private clinics offer faster service.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies open Mon-Fri 9am-7pm, Sat 9am-3pm. Extended hours at some Helsinki locations.",
        "pharmacyTips": "Pharmacies are called 'apteekki' — look for the green cross sign. Yliopiston Apteekki (University Pharmacy) in Helsinki has extended hours and English-speaking staff. Pharmacists are highly trained and can advise on minor conditions.",
        "commonOTC": [
            "ibuprofen (Burana)",
            "paracetamol (Panadol)",
            "cold and flu remedies",
            "antacids",
            "antihistamines (Cetirizine)",
            "band-aids and basic first aid"
        ],
        "prescriptionRules": "Finland follows EU prescription regulations. Many medications require a Finnish prescription. EU/EEA prescriptions may be accepted. Antibiotics always require a prescription.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only. Small personal amounts with documentation are allowed."
            },
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers. Doctor's letter needed for non-EU travelers."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substances requiring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Cannabis is illegal. CBD products with any THC are prohibited."
            }
        ],
        "bringDocumentation": "Carry a Schengen certificate (EU/EEA travelers) or doctor's letter in English for controlled substances. Keep medications in original packaging with prescription labels.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC for public healthcare access.",
            "averageCost": "$50-85/week",
            "tips": "Finland is expensive for healthcare. Private clinic visits can cost €100-300. Travel insurance with medical evacuation is recommended, especially for Lapland travel."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for outdoor activities in southern/central Finland, May-November)"
            ],
            "notes": "No mandatory vaccinations. Finland is a low-risk destination. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Finland has some of the purest tap water in the world. Safe to drink everywhere, including from many natural springs and streams in wilderness areas.",
        "foodSafetyTips": "Excellent food safety standards. All food establishments are inspected. Raw fish (such as gravlax) is safe from reputable sources. Wild berries and mushrooms should only be consumed if properly identified.",
        "medicalTourismNote": "Finland is recognized for orthopedic surgery, eye surgery, and cancer treatment. Helsinki University Hospital is internationally ranked.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Helsinki",
            "Finnish Institute for Health and Welfare (THL)",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Finland. Emergency number 112, pharmacy tips, medication rules, healthcare system info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "HUS Helsinki University Hospital (Meilahti)",
                "nearTouristArea": "Central Helsinki",
                "phone": "+358 9 4711",
                "englishSpeaking": True,
                "notes": "Finland's largest hospital. Full emergency services. English widely spoken."
            },
            {
                "name": "Mehiläinen Töölö Clinic",
                "nearTouristArea": "Töölö, Helsinki (near city center)",
                "phone": "+358 10 414 00",
                "englishSpeaking": True,
                "notes": "Major private clinic chain. Faster service than public hospitals. Walk-in and appointments."
            },
            {
                "name": "Turku University Hospital",
                "nearTouristArea": "Turku city center",
                "phone": "+358 2 313 0000",
                "englishSpeaking": True,
                "notes": "Major hospital serving southwestern Finland. Emergency department 24/7."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Tarvitsen päänsärkylääkettä",
                "transliteration": "TAR-vit-sen PAAN-saar-kew-laa-ket-ta"
            },
            {
                "english": "I have a stomachache",
                "local": "Minulla on vatsakipua",
                "transliteration": "MI-nul-la on VAT-sa-ki-pu-a"
            },
            {
                "english": "I'm allergic to...",
                "local": "Olen allerginen...",
                "transliteration": "O-len al-LER-gi-nen..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Missä on lähin apteekki?",
                "transliteration": "MIS-sa on LA-hin AP-teek-ki?"
            },
            {
                "english": "I need a doctor",
                "local": "Tarvitsen lääkärin",
                "transliteration": "TAR-vit-sen LAA-ka-rin"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care available. Private dentists easier to access than public dental clinics for tourists.",
            "costRange": "€60-150 for a consultation; €100-400 for fillings or extractions",
            "notes": "Public dental care has long wait times. Private clinics like Oral and Mehiläinen offer faster appointments. Most dentists speak English.",
            "emergencyTip": "For dental emergencies in Helsinki, contact the Haartman Hospital dental emergency clinic. Private dental chains offer same-day emergency appointments."
        },
        "mentalHealth": {
            "crisisLine": "09 2525 0111 (MIELI Crisis Helpline, Mon-Fri 9am-7am, weekends 3pm-7am)",
            "internationalLine": "Crisis text line: text 'MIELI' to 16 117 (Finnish/English)",
            "englishTherapists": "Available in Helsinki through private clinics. Expect €80-150 per session.",
            "notes": "MIELI Mental Health Finland provides resources and referrals. English-speaking therapists available in major cities through private practice."
        },
        "accessibilityInfo": {
            "overview": "Finland has strong accessibility laws and good infrastructure. Winter conditions (ice, snow) can create additional challenges.",
            "hospitalAccess": "All hospitals are wheelchair accessible with modern facilities.",
            "transport": "Helsinki trams, metro, and buses are wheelchair accessible. Trains have accessible carriages. Taxis can accommodate wheelchairs with advance booking.",
            "tips": "Winter months (Nov-Mar) create icy conditions that affect mobility. Indoor attractions are well-adapted. Contact Visit Finland for accessibility-specific travel guides."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements. Masks rarely worn.",
            "testing": "Tests available at pharmacies and health centers if needed.",
            "notes": "Finland lifted all COVID restrictions. No special measures remain in effect."
        },
        "insuranceClaimProcess": "Public hospital fees can be paid on-site. Keep all receipts and request English documentation. Private clinics provide detailed invoices. EU/EEA citizens present EHIC for reduced public healthcare costs. File insurance claims within 30 days."
    },
    "RO": {
        "iso2": "RO",
        "countryName": "Romania",
        "countrySlug": "romania",
        "flag": "🇷🇴",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare funded by social insurance. EU/EEA citizens covered with EHIC for emergency care. Private healthcare is growing rapidly and preferred by many travelers.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Bucharest and major cities offer good care. Public hospitals can be underfunded and overcrowded. English is widely spoken by younger doctors. Private clinics are recommended for tourists.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (farmacie) generally open Mon-Fri 8am-8pm, Sat 8am-2pm. Some 24/7 pharmacies in Bucharest and major cities.",
        "pharmacyTips": "Pharmacies are marked with a green cross. Major chains include Catena, Sensiblu, and HelpNet. Pharmacists often speak English in cities. Prices are significantly lower than Western Europe.",
        "commonOTC": [
            "ibuprofen (Nurofen)",
            "paracetamol (Panadol, Efferalgan)",
            "cold remedies (Coldrex, Theraflu)",
            "stomach remedies (Smecta)",
            "antihistamines",
            "band-aids and first aid supplies"
        ],
        "prescriptionRules": "Many medications available OTC in Romania that require prescriptions elsewhere. Antibiotics officially require a prescription but enforcement varies. EU prescriptions may be accepted.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require prescription and documentation. Carry a doctor's letter."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substance. Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Romania. CBD products with THC are prohibited."
            },
            {
                "name": "Pseudoephedrine",
                "status": "restricted",
                "note": "Available only from behind the pharmacy counter with ID."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate for controlled substances. Non-EU travelers should bring a doctor's letter in English. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$25-50/week",
            "tips": "Healthcare is affordable but private facilities preferred for tourists. Travel insurance is strongly recommended for access to private hospitals and medical evacuation if needed."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Tick-borne Encephalitis (for rural/forested areas)",
                "Rabies (for extended rural stays)"
            ],
            "notes": "No mandatory vaccinations. Romania has had measles outbreaks — ensure MMR vaccination is current."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is generally safe in major cities (Bucharest, Cluj-Napoca, Timișoara) but quality varies in rural areas. Bottled water is cheap and widely available. When in doubt, drink bottled water.",
        "foodSafetyTips": "Romanian food is generally safe. Eat at busy, popular restaurants. Traditional dishes are hearty and well-cooked. Be cautious with dairy products in rural areas during hot weather.",
        "medicalTourismNote": "Romania is a growing medical tourism destination, especially for dental care, cosmetic surgery, and eye surgery. Costs are 50-70% lower than Western Europe.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Bucharest",
            "Romanian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Romania. Emergency number 112, pharmacy tips, hospital info, vaccination advice, and travel insurance tips for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "MedLife Grivița Hospital",
                "nearTouristArea": "Central Bucharest",
                "phone": "+40 21 9886",
                "englishSpeaking": True,
                "notes": "Leading private hospital chain. Modern facilities, English-speaking staff."
            },
            {
                "name": "Regina Maria Central Clinic",
                "nearTouristArea": "Bucharest city center",
                "phone": "+40 21 9555",
                "englishSpeaking": True,
                "notes": "Major private healthcare network. Walk-in and appointments available."
            },
            {
                "name": "Cluj-Napoca Emergency County Hospital",
                "nearTouristArea": "Cluj-Napoca (Transylvania)",
                "phone": "+40 264 592 771",
                "englishSpeaking": True,
                "notes": "Major public hospital in Transylvania. English-speaking doctors available."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Am nevoie de medicamente pentru durere de cap",
                "transliteration": "Am neh-VOY-eh deh meh-dee-kah-MEN-teh PEN-troo doo-REH-reh deh kap"
            },
            {
                "english": "I have a stomachache",
                "local": "Mă doare stomacul",
                "transliteration": "Ma DOA-reh sto-MA-kool"
            },
            {
                "english": "I'm allergic to...",
                "local": "Sunt alergic la...",
                "transliteration": "Soont ah-LEHR-jik la..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Unde este cea mai apropiată farmacie?",
                "transliteration": "OON-deh YES-teh cha my ah-pro-pee-AH-ta far-ma-CHEE-eh?"
            },
            {
                "english": "I need a doctor",
                "local": "Am nevoie de un doctor",
                "transliteration": "Am neh-VOY-eh deh oon DOK-tor"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care at very affordable prices. Romania is a top dental tourism destination.",
            "costRange": "€20-50 for a consultation; €30-150 for fillings; €50-200 for extractions",
            "notes": "Many dental clinics in Bucharest and Cluj cater specifically to international patients. Quality is on par with Western Europe at a fraction of the cost.",
            "emergencyTip": "Most dental clinics have emergency slots. In Bucharest, several private dental clinics offer weekend emergency services."
        },
        "mentalHealth": {
            "crisisLine": "0800 801 200 (Telefonul Sufletului — crisis line, free)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Bucharest through private practice. Expect €40-80 per session.",
            "notes": "Mental health services are developing. English-speaking therapists available in major cities. Online therapy options are growing."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving but remains a challenge. Newer buildings meet EU standards but older infrastructure has barriers.",
            "hospitalAccess": "Private hospitals are generally wheelchair accessible. Older public hospitals may have limited accessibility.",
            "transport": "Bucharest metro is partially accessible. Newer buses and trams have low floors. Accessible taxis available with advance booking.",
            "tips": "Cobblestone streets in historic areas can be difficult for wheelchairs. Newer attractions and shopping centers are well-adapted. Contact hotels in advance about accessibility."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Romania has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics accept payment by card and provide detailed receipts and medical reports in English on request. Public hospitals may require cash. Keep all documentation for insurance claims. File within 30 days of treatment."
    },
    "BG": {
        "iso2": "BG",
        "countryName": "Bulgaria",
        "countrySlug": "bulgaria",
        "flag": "🇧🇬",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare funded by national health insurance. EU/EEA citizens covered with EHIC. Private clinics are recommended for tourists.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Sofia and major cities offer modern care. Public hospitals can be underfunded. Younger doctors often speak English. Private healthcare is affordable and preferable for visitors.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (аптека) typically open Mon-Fri 8:30am-8pm, Sat 9am-3pm. 24/7 pharmacies available in Sofia and larger cities.",
        "pharmacyTips": "Pharmacies are marked with a green cross. Chains include Subra and Sopharmacy. Many medications are available OTC at very affordable prices. Pharmacists may speak limited English — bring written requests.",
        "commonOTC": [
            "ibuprofen (Nurofen, Ibuprofen)",
            "paracetamol (Panadol, Analgin)",
            "cold medicine (Coldrex)",
            "stomach remedies",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Many medications are available OTC. Antibiotics technically require a prescription but are sometimes dispensed without one. EU prescriptions may be honored.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require documentation. Carry a doctor's letter."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substances. Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Bulgaria. CBD products with THC are prohibited."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter in English. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$20-45/week",
            "tips": "Healthcare is affordable but private facilities are strongly recommended for tourists. Insurance ensures access to the best private clinics."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Tick-borne Encephalitis (for rural/forested areas)"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is generally safe in Sofia and major cities but can be unreliable in rural areas. Bottled water is very cheap and widely available.",
        "foodSafetyTips": "Bulgarian cuisine is hearty and well-cooked. Yogurt is famously safe and healthy. Be cautious with dairy products in extreme heat. Eat at busy restaurants.",
        "medicalTourismNote": "Bulgaria is a growing medical tourism destination for dental care, cosmetic surgery, and spa/thermal treatments. Costs are among the lowest in the EU.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Sofia",
            "Bulgarian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Bulgaria. Emergency number 112, pharmacy tips, hospital recommendations, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Tokuda Hospital Sofia",
                "nearTouristArea": "Sofia (Lozenets district)",
                "phone": "+359 2 403 4000",
                "englishSpeaking": True,
                "notes": "Modern private hospital with international standards. English-speaking staff."
            },
            {
                "name": "Acibadem City Clinic Sofia",
                "nearTouristArea": "Central Sofia",
                "phone": "+359 2 960 4601",
                "englishSpeaking": True,
                "notes": "Part of international Acibadem healthcare group. Modern facilities."
            },
            {
                "name": "UMBAL Sv. Georgi (St. George University Hospital)",
                "nearTouristArea": "Plovdiv city center",
                "phone": "+359 32 602 851",
                "englishSpeaking": True,
                "notes": "Major public university hospital in Plovdiv. Emergency services 24/7."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Имам нужда от лекарство за главоболие",
                "transliteration": "Imam nuzhda ot lekarstvo za glavobolie"
            },
            {
                "english": "I have a stomachache",
                "local": "Боли ме стомахът",
                "transliteration": "Boli me stomakhut"
            },
            {
                "english": "I'm allergic to...",
                "local": "Алергичен/Алергична съм към...",
                "transliteration": "Alergichen/Alergichna sum kum..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Къде е най-близката аптека?",
                "transliteration": "Kude e nay-blizkata apteka?"
            },
            {
                "english": "I need a doctor",
                "local": "Имам нужда от лекар",
                "transliteration": "Imam nuzhda ot lekar"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care at very affordable prices. Many clinics cater to international patients.",
            "costRange": "€15-40 for consultation; €25-100 for fillings; €30-120 for extractions",
            "notes": "Sofia and Varna are popular dental tourism hubs. Quality is good and prices are among the lowest in the EU.",
            "emergencyTip": "Most private dental clinics have emergency appointments available. Hospital emergency departments can handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "0035 42 981 76 86 (National Crisis Line)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Sofia through private practice. Expect €30-60 per session.",
            "notes": "Mental health services are developing. English-speaking therapists available in Sofia. Online therapy platforms serve English speakers."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving, especially in newer buildings, but older infrastructure and cobblestone streets present challenges.",
            "hospitalAccess": "Private hospitals are wheelchair accessible. Older public hospitals may have limited access.",
            "transport": "Sofia metro is accessible. Newer buses have low floors. Accessible taxis limited — book in advance.",
            "tips": "Historic old towns have cobblestones and uneven surfaces. Newer shopping centers, hotels, and attractions are better adapted."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Bulgaria has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics provide receipts and medical reports. Request English-language documentation. Public hospitals may provide documentation in Bulgarian only — ask for translation. Keep all receipts for insurance claims."
    },
    "RS": {
        "iso2": "RS",
        "countryName": "Serbia",
        "countrySlug": "serbia",
        "flag": "🇷🇸",
        "emergencyNumber": "194 (ambulance), 192 (police), 193 (fire)",
        "healthcareSystem": "Public healthcare funded by mandatory health insurance. Tourists pay out-of-pocket. Private clinics are widely available and affordable.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Belgrade offer good modern care. Public hospitals can be underfunded and overcrowded. Many Serbian doctors train abroad and speak English. Private healthcare is recommended for tourists.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (apoteka/апотека) open Mon-Fri 7:30am-8pm, Sat 8am-3pm. 24/7 pharmacies available in Belgrade.",
        "pharmacyTips": "Pharmacies are marked with a green cross. Prices are very affordable. Many medications available OTC that require prescriptions in Western countries. Pharmacists may speak basic English in Belgrade.",
        "commonOTC": [
            "ibuprofen (Brufen)",
            "paracetamol (Panadol, Paracetamol)",
            "cold medicine",
            "stomach remedies (Ranisan)",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Many medications available without prescription in Serbia. Antibiotics can sometimes be obtained OTC. Controlled substances always require a prescription.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require documentation. Carry a doctor's letter."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substance. Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Serbia."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English listing all medications. Keep controlled substances in original packaging with prescription labels.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-40/week",
            "tips": "Healthcare is very affordable but travel insurance is recommended for private hospital access and potential medical evacuation. Serbia is not in the EU so EHIC is not valid."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Tick-borne Encephalitis (for rural areas)"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink in Belgrade and major cities. Water quality can vary in rural areas — bottled water is cheap and widely available.",
        "foodSafetyTips": "Serbian food is hearty and generally safe. Grilled meats (ćevapi, pljeskavica) are cooked thoroughly. Dairy products are fresh and of good quality. Eat at busy restaurants for the freshest food.",
        "medicalTourismNote": "Serbia is emerging as a medical tourism destination for dental care, cosmetic surgery, fertility treatments, and eye surgery. Costs are very competitive.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Belgrade",
            "Serbian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Serbia. Emergency numbers (194/192/193), pharmacy tips, hospital recommendations, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "BelMedic General Hospital",
                "nearTouristArea": "New Belgrade",
                "phone": "+381 11 309 1000",
                "englishSpeaking": True,
                "notes": "Leading private hospital in Belgrade. Modern facilities, international standards."
            },
            {
                "name": "MediGroup Hospital",
                "nearTouristArea": "Central Belgrade",
                "phone": "+381 11 418 5100",
                "englishSpeaking": True,
                "notes": "Private hospital with English-speaking staff. Good emergency department."
            },
            {
                "name": "Clinical Center of Serbia (Klinički centar Srbije)",
                "nearTouristArea": "Central Belgrade (near Vračar)",
                "phone": "+381 11 366 1122",
                "englishSpeaking": True,
                "notes": "Largest public hospital complex in Serbia. Major trauma center."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Треба ми лек за главобољу",
                "transliteration": "Treba mi lek za glavobolju"
            },
            {
                "english": "I have a stomachache",
                "local": "Боли ме стомак",
                "transliteration": "Boli me stomak"
            },
            {
                "english": "I'm allergic to...",
                "local": "Алергичан/Алергична сам на...",
                "transliteration": "Alergičan/Alergična sam na..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Где је најближа апотека?",
                "transliteration": "Gde je najbliža apoteka?"
            },
            {
                "english": "I need a doctor",
                "local": "Треба ми лекар",
                "transliteration": "Treba mi lekar"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care at very affordable prices. Many clinics in Belgrade cater to international patients.",
            "costRange": "€15-40 for consultation; €25-80 for fillings; €30-100 for extractions",
            "notes": "Belgrade is becoming a popular dental tourism destination. Quality is high and prices are very competitive.",
            "emergencyTip": "Private dental clinics in Belgrade often offer emergency appointments. Major hospitals have oral surgery departments."
        },
        "mentalHealth": {
            "crisisLine": "011 7572 985 (Centar Srce — crisis support)",
            "internationalLine": "194 for emergency psychiatric help",
            "englishTherapists": "Available in Belgrade. Expect €30-60 per session.",
            "notes": "Mental health services are available but somewhat limited. English-speaking therapists available in Belgrade through private practice."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving but remains limited in many areas. Newer buildings meet modern standards but older infrastructure has barriers.",
            "hospitalAccess": "Private hospitals are wheelchair accessible. Older public hospitals may have limited access.",
            "transport": "Belgrade buses are partially accessible. Some newer trams have low floors. Accessible taxis limited.",
            "tips": "Belgrade Fortress and Kalemegdan can be challenging for wheelchair users. Newer shopping centers and hotels are well-adapted."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at clinics and hospitals.",
            "notes": "Serbia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics in Serbia accept card payments and provide English-language receipts and medical reports. Public hospitals may require cash. Keep all documentation for insurance claims."
    },
    "ME": {
        "iso2": "ME",
        "countryName": "Montenegro",
        "countrySlug": "montenegro",
        "flag": "🇲🇪",
        "emergencyNumber": "124 (ambulance), 122 (police), 123 (fire)",
        "healthcareSystem": "Public healthcare system funded by mandatory health insurance. Tourists pay out-of-pocket. Limited private healthcare options available, mainly in Podgorica.",
        "healthcareSystemType": "universal",
        "qualityRating": 2,
        "qualityNotes": "Healthcare is basic but adequate for emergencies. Podgorica has the best facilities. Coastal areas have seasonal clinics in summer. For serious conditions, medical evacuation to Serbia or Western Europe may be necessary.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies (apoteka) open Mon-Fri 7:30am-8pm, Sat 8am-2pm. Limited options on evenings and weekends outside Podgorica.",
        "pharmacyTips": "Green cross marks pharmacies. Montefarm is the main pharmacy chain. Prices are affordable. English may not be widely spoken — bring written medication names.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol",
            "cold remedies",
            "stomach medication",
            "antihistamines",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Similar to Serbia — many medications available OTC. Controlled substances require prescriptions. Foreign prescriptions are generally not accepted.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require documentation. Bring a doctor's letter."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Montenegro."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English listing all medications. Keep medicines in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-40/week",
            "tips": "Travel insurance is essential due to limited healthcare infrastructure. Ensure your policy covers medical evacuation, especially if visiting remote mountain areas."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe in most towns and cities. Mountain spring water is generally excellent. Bottled water is cheap and widely available.",
        "foodSafetyTips": "Montenegrin cuisine features grilled meats, fresh seafood on the coast, and dairy products. Food is generally safe at restaurants. Seafood on the coast is fresh and well-prepared.",
        "medicalTourismNote": "Montenegro is not a major medical tourism destination. Most medical tourists travel to Serbia or Croatia for advanced procedures.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Podgorica",
            "Montenegrin Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Montenegro. Emergency numbers, pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Clinical Center of Montenegro",
                "nearTouristArea": "Podgorica",
                "phone": "+382 20 412 412",
                "englishSpeaking": True,
                "notes": "Main hospital in Montenegro. Emergency department 24/7. English spoken by some doctors."
            },
            {
                "name": "General Hospital Kotor",
                "nearTouristArea": "Kotor (Bay of Kotor, popular tourist area)",
                "phone": "+382 32 330 730",
                "englishSpeaking": False,
                "notes": "Nearest hospital to the popular Bay of Kotor area. Basic emergency services."
            },
            {
                "name": "General Hospital Budva (Seasonal Clinic)",
                "nearTouristArea": "Budva (main beach resort town)",
                "phone": "+382 33 402 402",
                "englishSpeaking": False,
                "notes": "Seasonal healthcare available in peak summer months. For serious conditions, transfer to Podgorica."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Treba mi lijek za glavobolju",
                "transliteration": "TREH-bah mee lee-YEK za glah-voh-BOL-yoo"
            },
            {
                "english": "I have a stomachache",
                "local": "Boli me stomak",
                "transliteration": "BOH-lee meh STOH-mak"
            },
            {
                "english": "I'm allergic to...",
                "local": "Alergičan/Alergična sam na...",
                "transliteration": "ah-lehr-GEECH-ahn sahm nah..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Gdje je najbliža apoteka?",
                "transliteration": "GDYEH yeh NAY-blee-zhah ah-poh-TEH-kah?"
            },
            {
                "english": "I need a doctor",
                "local": "Treba mi doktor",
                "transliteration": "TREH-bah mee DOK-tor"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Podgorica and coastal towns. Private dental clinics offer good care at affordable prices.",
            "costRange": "€15-35 for consultation; €25-80 for fillings; €30-100 for extractions",
            "notes": "Quality dental care available at affordable prices. Limited English may be an issue outside Podgorica.",
            "emergencyTip": "Private dental clinics in Podgorica and Budva may offer emergency slots. Otherwise, visit the Clinical Center of Montenegro."
        },
        "mentalHealth": {
            "crisisLine": "124 for emergency services including psychiatric emergencies",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some English-speaking therapists in Podgorica.",
            "notes": "Mental health services are limited in Montenegro. For English-speaking support, contact your embassy or use international online platforms."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is limited. Newer buildings are better adapted but older areas, especially historic old towns, can be very challenging.",
            "hospitalAccess": "The Clinical Center in Podgorica is accessible. Smaller regional hospitals have limited accessibility.",
            "transport": "Public transport has limited accessibility. Taxis are the most practical option. Wheelchair-accessible vehicles may need advance booking.",
            "tips": "Kotor and Budva old towns have steep, narrow streets with cobblestones. Coastal promenades are generally flat and accessible. Contact hotels in advance about room accessibility."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at the Clinical Center and some private clinics.",
            "notes": "Montenegro has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Healthcare facilities in Montenegro provide basic receipts. Request English documentation when possible. Keep all payment records for insurance claims. Some smaller facilities only accept cash."
    },
    "AL": {
        "iso2": "AL",
        "countryName": "Albania",
        "countrySlug": "albania",
        "flag": "🇦🇱",
        "emergencyNumber": "127 (ambulance), 129 (police), 128 (fire)",
        "healthcareSystem": "Public healthcare system with mandatory health insurance for residents. Tourists pay out-of-pocket. Private healthcare is growing and recommended for visitors.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private clinics in Tirana offer adequate care. Public hospitals are underfunded with aging equipment. English-speaking doctors available in Tirana. For serious conditions, medical evacuation to Greece or Italy may be necessary.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (farmaci) open Mon-Sat 8am-8pm. 24/7 pharmacies available in Tirana.",
        "pharmacyTips": "Green cross marks pharmacies. Many medications are available OTC at very low prices. Antibiotics often dispensed without prescription. Pharmacists may speak limited English.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol",
            "cold remedies",
            "stomach medication",
            "antibiotics (often available OTC)",
            "antihistamines",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Many medications available OTC including antibiotics. Controlled substances require prescriptions. Foreign prescriptions not formally accepted.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require documentation. Bring a doctor's letter."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Albania despite widespread cultivation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for controlled medications. Keep all medicines in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$15-35/week",
            "tips": "Travel insurance is essential due to limited healthcare infrastructure. Ensure medical evacuation coverage, especially for remote areas and mountain regions."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Rabies (for adventure travelers or rural areas)"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water in Tirana is generally safe but quality varies. Bottled water is recommended, especially outside the capital and in summer. Bottled water is very cheap.",
        "foodSafetyTips": "Albanian cuisine is Mediterranean-influenced and generally safe. Grilled meats and fresh salads are common. Eat at busy restaurants. Coastal seafood is fresh but ensure it's from a reputable restaurant.",
        "medicalTourismNote": "Albania is emerging as a dental tourism destination with very affordable prices. Medical tourism is in early stages.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Tirana",
            "Albanian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Albania. Emergency numbers (127/129/128), pharmacy tips, hospital info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "American Hospital Tirana",
                "nearTouristArea": "Central Tirana",
                "phone": "+355 4 235 7535",
                "englishSpeaking": True,
                "notes": "Leading private hospital. International standards. English-speaking doctors."
            },
            {
                "name": "Hygeia Hospital Tirana",
                "nearTouristArea": "Tirana",
                "phone": "+355 4 239 0000",
                "englishSpeaking": True,
                "notes": "Part of Greek Hygeia Group. Modern private hospital with international standards."
            },
            {
                "name": "University Hospital Center Mother Teresa (QSUT)",
                "nearTouristArea": "Central Tirana",
                "phone": "+355 4 234 9209",
                "englishSpeaking": True,
                "notes": "Main public hospital. Largest in Albania. Emergency services 24/7."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Kam nevojë për ilaç kundër dhimbjes së kokës",
                "transliteration": "Kam neh-VOY-uh puhr ee-LACH koon-DUHR DHEEM-byehs suh KO-kuhs"
            },
            {
                "english": "I have a stomachache",
                "local": "Më dhemb barku",
                "transliteration": "Muh dhemb BAR-koo"
            },
            {
                "english": "I'm allergic to...",
                "local": "Jam alergjik ndaj...",
                "transliteration": "Yam ah-ler-JHEEK ndai..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Ku është farmacia më e afërt?",
                "transliteration": "Koo UHSH-tuh far-ma-TSEE-ah muh eh AH-fuhrt?"
            },
            {
                "english": "I need a doctor",
                "local": "Kam nevojë për mjek",
                "transliteration": "Kam neh-VOY-uh puhr myehk"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care available in Tirana at very affordable prices. Growing dental tourism industry.",
            "costRange": "€10-30 for consultation; €20-60 for fillings; €20-80 for extractions",
            "notes": "Tirana has modern private dental clinics. Prices are among the lowest in Europe. Some clinics specifically target dental tourists.",
            "emergencyTip": "Private dental clinics in Tirana offer emergency appointments. Hospital emergency departments can handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "116 123 (National Crisis Helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some English-speaking psychologists in Tirana.",
            "notes": "Mental health services are limited. English-speaking support mainly available through private clinics in Tirana or international online platforms."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited throughout Albania. Newer buildings in Tirana are improving but older areas and smaller cities have significant barriers.",
            "hospitalAccess": "Private hospitals are somewhat accessible. Public hospitals have limited accessibility features.",
            "transport": "Public transport is not wheelchair accessible. Taxis are the most practical option. Wheelchair-accessible vehicles require advance arrangement.",
            "tips": "Tirana's new Skanderbeg Square area is relatively accessible. Historic sites, Berat, Gjirokastër, and the Albanian Riviera have significant accessibility challenges. Plan carefully and contact accommodations in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at private clinics in Tirana.",
            "notes": "Albania has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics can provide receipts and English-language documentation. Public hospitals may only issue documentation in Albanian. Keep all payment records. Cash is often required at public facilities."
    },
    "GE": {
        "iso2": "GE",
        "countryName": "Georgia",
        "countrySlug": "georgia",
        "flag": "🇬🇪",
        "emergencyNumber": "112 (universal), 113 (ambulance)",
        "healthcareSystem": "Mixed public-private system. Universal Healthcare Programme covers basic services for Georgian citizens. Tourists pay out-of-pocket. Private healthcare is growing rapidly.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Tbilisi offer good modern care. Healthcare quality drops significantly outside the capital. Many Georgian doctors trained in Europe speak English. Private facilities recommended for tourists.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (აფთიაქი) open daily 8am-10pm. Many 24/7 pharmacies in Tbilisi, including GPC and PSP chains.",
        "pharmacyTips": "Pharmacies are very common in Georgia. GPC (Green Pharmacy Chain) and PSP are major chains. Many medications available OTC including antibiotics. Prices are very low. Pharmacists may speak limited English.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol",
            "antibiotics (widely available OTC)",
            "cold remedies",
            "stomach medication",
            "antihistamines",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Georgia has relaxed prescription requirements. Many medications including antibiotics are available OTC. Some controlled substances require a prescription.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Strictly controlled. Georgia has very strict anti-drug laws."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Require prescription. Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Personal use decriminalized but possession/cultivation remains illegal. Do not bring cannabis products."
            },
            {
                "name": "Tramadol and similar analgesics",
                "status": "controlled",
                "note": "Controlled substance. Must have documentation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for all controlled medications. Georgia has strict drug laws — ensure all medications are clearly documented and in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$15-35/week",
            "tips": "Healthcare is very affordable but insurance is recommended for private hospital access and medical evacuation if needed, especially for mountain regions (Svaneti, Kazbegi)."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Rabies (for rural or adventure travel)"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water in Tbilisi is generally safe. Water quality varies in other cities and rural areas. Bottled water is cheap and widely available. Many natural springs in the countryside are safe.",
        "foodSafetyTips": "Georgian cuisine is excellent and generally safe. Khinkali, khachapuri, and grilled meats are well-cooked. Wine culture is strong — drink from reputable sources. Street food markets are popular and generally safe.",
        "medicalTourismNote": "Georgia is a growing medical tourism destination, particularly for dental work, cosmetic surgery, and fertility treatments at very affordable prices.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Tbilisi",
            "Georgian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Georgia. Emergency numbers (112/113), pharmacy tips, hospital recommendations, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Todua Clinic (MediClubGeorgia)",
                "nearTouristArea": "Central Tbilisi (Vake district)",
                "phone": "+995 32 225 1991",
                "englishSpeaking": True,
                "notes": "Leading private clinic. Modern equipment. English-speaking doctors."
            },
            {
                "name": "Evex Medical Corporation (Tbilisi)",
                "nearTouristArea": "Tbilisi",
                "phone": "+995 32 255 0055",
                "englishSpeaking": True,
                "notes": "Largest private healthcare group in Georgia. Multiple locations."
            },
            {
                "name": "National Center for Disease Control (NCDC) / Tbilisi Central Hospital",
                "nearTouristArea": "Central Tbilisi",
                "phone": "+995 32 239 8946",
                "englishSpeaking": True,
                "notes": "Major public hospital. Emergency department 24/7."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "თავის ტკივილის წამალი მჭირდება",
                "transliteration": "Tavis t'k'ivilis ts'amali mch'irdeba"
            },
            {
                "english": "I have a stomachache",
                "local": "მუცელი მტკივა",
                "transliteration": "Mutseli mt'k'iva"
            },
            {
                "english": "I'm allergic to...",
                "local": "ალერგია მაქვს...",
                "transliteration": "Alergia makvs..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "სად არის უახლოესი აფთიაქი?",
                "transliteration": "Sad aris uakhloesi apt'iaqi?"
            },
            {
                "english": "I need a doctor",
                "local": "ექიმი მჭირდება",
                "transliteration": "Eqimi mch'irdeba"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Tbilisi at very affordable prices. Georgia is emerging as a dental tourism hub.",
            "costRange": "GEL 30-80 ($10-30) for consultation; GEL 80-300 ($30-110) for fillings; GEL 100-400 ($35-150) for extractions",
            "notes": "Many modern dental clinics in Tbilisi. Some cater specifically to medical tourists. Quality is improving rapidly.",
            "emergencyTip": "Private dental clinics in Tbilisi offer emergency appointments. Several clinics near the tourist center are open evenings and weekends."
        },
        "mentalHealth": {
            "crisisLine": "112 for emergency services",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Tbilisi through private practice. Expect GEL 100-200 ($35-75) per session.",
            "notes": "Mental health services are limited but growing. English-speaking therapists available in Tbilisi. Online therapy platforms serve English speakers."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is limited. Tbilisi is hilly with uneven sidewalks. Newer buildings are somewhat accessible but older areas have significant barriers.",
            "hospitalAccess": "Private hospitals are generally accessible. Public hospitals have limited accessibility.",
            "transport": "Tbilisi metro has limited accessibility. Taxis are the most practical option. Wheelchair-accessible vehicles require advance booking.",
            "tips": "Tbilisi's Old Town has steep cobblestone streets. Newer areas like Vake and Saburtalo are more accessible. Contact accommodations in advance about accessibility needs."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at clinics and hospitals in Tbilisi.",
            "notes": "Georgia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics provide receipts and medical documentation in English on request. Healthcare costs are low — some travelers pay out-of-pocket. Keep all documentation for insurance claims."
    },
    "LV": {
        "iso2": "LV",
        "countryName": "Latvia",
        "countrySlug": "latvia",
        "flag": "🇱🇻",
        "emergencyNumber": "113 (ambulance), 112 (general emergency)",
        "healthcareSystem": "Universal public healthcare system. EU/EEA citizens covered with EHIC. Non-EU tourists pay out-of-pocket. Private healthcare available in Riga.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Riga offer good care. Public system is functional but underfunded. Younger doctors often speak English. Private healthcare recommended for visitors.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (aptieka) open Mon-Fri 8am-8pm, Sat 9am-5pm. 24/7 pharmacies available in Riga.",
        "pharmacyTips": "Look for the green cross. Mēness aptieka is the largest pharmacy chain. Pharmacists are well-trained and some speak English. Prices are moderate.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol",
            "cold and flu remedies",
            "stomach remedies",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Latvia follows EU prescription regulations. Many medications require a prescription. EU/EEA prescriptions may be accepted.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only."
            },
            {
                "name": "Opioids and benzodiazepines",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers; doctor's letter for non-EU travelers."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Latvia."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$30-55/week",
            "tips": "Healthcare in Latvia is reasonably priced but travel insurance is recommended for private hospital access."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for rural and forested areas, spring through autumn)"
            ],
            "notes": "No mandatory vaccinations. Latvia has a high incidence of tick-borne encephalitis in forested areas. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink in Riga and major cities. Quality is good throughout the country.",
        "foodSafetyTips": "Food safety standards are good. Local cuisine is hearty and well-cooked. Dairy products and smoked fish are safe from reputable sources.",
        "medicalTourismNote": "Latvia is known for affordable dental care and cosmetic procedures. Riga has several clinics catering to international patients.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Riga",
            "Latvian Centre for Disease Prevention and Control",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Latvia. Emergency numbers (113/112), pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Pauls Stradiņš Clinical University Hospital",
                "nearTouristArea": "Central Riga",
                "phone": "+371 67 069 600",
                "englishSpeaking": True,
                "notes": "Major public university hospital. Emergency department 24/7. English-speaking doctors available."
            },
            {
                "name": "ARS Medical Centre",
                "nearTouristArea": "Riga Old Town area",
                "phone": "+371 67 201 007",
                "englishSpeaking": True,
                "notes": "Leading private clinic. International standards. English-speaking staff."
            },
            {
                "name": "Riga East University Hospital",
                "nearTouristArea": "Riga",
                "phone": "+371 67 042 001",
                "englishSpeaking": True,
                "notes": "Largest hospital in the Baltic states. Full range of services."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Man vajag zāles pret galvassāpēm",
                "transliteration": "Man VA-yag ZAA-les pret GAL-vas-saa-pehm"
            },
            {
                "english": "I have a stomachache",
                "local": "Man sāp vēders",
                "transliteration": "Man saap VEH-ders"
            },
            {
                "english": "I'm allergic to...",
                "local": "Man ir alerģija pret...",
                "transliteration": "Man ir ah-LEHR-gee-ya pret..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Kur ir tuvākā aptieka?",
                "transliteration": "Kur ir TOO-vaa-kaa AP-tee-eh-ka?"
            },
            {
                "english": "I need a doctor",
                "local": "Man vajag ārstu",
                "transliteration": "Man VA-yag AAHR-stoo"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care available in Riga at affordable prices.",
            "costRange": "€30-70 for consultation; €40-150 for fillings; €50-200 for extractions",
            "notes": "Riga has modern dental clinics. Several cater to dental tourists from Scandinavia and the UK. Good quality at lower prices than Western Europe.",
            "emergencyTip": "Private dental clinics in Riga offer emergency appointments. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "116 123 (Crisis Helpline, 24/7, free)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Riga. Expect €40-80 per session.",
            "notes": "Mental health services are available in Riga. English-speaking therapists can be found through private practice and expat networks."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving in Latvia. Riga's Art Nouveau district and Old Town have cobblestones that can be challenging.",
            "hospitalAccess": "Major hospitals and private clinics are wheelchair accessible.",
            "transport": "Riga trams and newer buses have low floors. Riga International Airport is accessible. Accessible taxis available with advance booking.",
            "tips": "Riga Old Town has cobblestone streets. Newer areas are more accessible. Many hotels and restaurants in the city center are adapted."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at clinics and pharmacies.",
            "notes": "Latvia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics provide English-language receipts and documentation. Public hospitals issue invoices that can be used for insurance claims. EU/EEA citizens present EHIC for public care. Keep all documentation for claims."
    },
    "LT": {
        "iso2": "LT",
        "countryName": "Lithuania",
        "countrySlug": "lithuania",
        "flag": "🇱🇹",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare funded by mandatory health insurance. EU/EEA citizens covered with EHIC. Private healthcare available in major cities.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private clinics in Vilnius and Kaunas offer good care. Public system is functional. Younger doctors speak English well. Private healthcare recommended for tourists.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (vaistinė) open Mon-Fri 8am-8pm, Sat 9am-5pm. Some 24/7 pharmacies in Vilnius.",
        "pharmacyTips": "Eurovaistinė and Camelia are major pharmacy chains. Green cross marks pharmacies. Pharmacists are knowledgeable and many speak English in Vilnius.",
        "commonOTC": [
            "ibuprofen (Nurofen)",
            "paracetamol",
            "cold remedies",
            "stomach medication",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Lithuania follows EU prescription regulations. Many medications require a prescription. EU/EEA prescriptions may be accepted at pharmacies.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only in Lithuania."
            },
            {
                "name": "Opioids and benzodiazepines",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers; doctor's letter for non-EU travelers."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Lithuania. CBD products may be restricted."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter in English. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$25-50/week",
            "tips": "Healthcare is affordable. Insurance recommended for private hospital access and medical evacuation."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for rural/forested areas, especially Curonian Spit and eastern Lithuania)"
            ],
            "notes": "No mandatory vaccinations. Lithuania has tick-borne encephalitis risk in forested areas. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink throughout Lithuania.",
        "foodSafetyTips": "Lithuanian food is hearty and safe. Traditional dishes like cepelinai and šaltibarščiai are well-prepared. Dairy products are of good quality.",
        "medicalTourismNote": "Lithuania is popular for dental tourism and cosmetic procedures, with prices well below Western European levels.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Vilnius",
            "Lithuanian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Lithuania. Emergency number 112, pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Vilnius University Hospital Santaros Klinikos",
                "nearTouristArea": "Vilnius (accessible from Old Town)",
                "phone": "+370 5 236 5000",
                "englishSpeaking": True,
                "notes": "Lithuania's largest and most advanced hospital. Full emergency services. English spoken."
            },
            {
                "name": "Baltic American Medical & Surgical Clinic",
                "nearTouristArea": "Vilnius Old Town area",
                "phone": "+370 5 234 2020",
                "englishSpeaking": True,
                "notes": "Private clinic catering to English-speaking patients. Walk-in accepted."
            },
            {
                "name": "Kaunas Clinics (LSMU Kauno Klinikos)",
                "nearTouristArea": "Kaunas",
                "phone": "+370 37 326 000",
                "englishSpeaking": True,
                "notes": "Major university hospital. Emergency services 24/7."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Man reikia vaistų nuo galvos skausmo",
                "transliteration": "Man RAY-kya VAIS-too nuo gal-VOS SKAUS-mo"
            },
            {
                "english": "I have a stomachache",
                "local": "Man skauda pilvą",
                "transliteration": "Man SKAU-da PIL-vah"
            },
            {
                "english": "I'm allergic to...",
                "local": "Aš esu alergiškas/alergiška...",
                "transliteration": "Ash EH-soo ah-lehr-GISH-kas..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Kur yra artimiausia vaistinė?",
                "transliteration": "Kur EE-ra ar-tee-MYAU-sya VAIS-tee-neh?"
            },
            {
                "english": "I need a doctor",
                "local": "Man reikia gydytojo",
                "transliteration": "Man RAY-kya gee-DEE-to-yo"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Vilnius and Kaunas at affordable prices.",
            "costRange": "€25-60 for consultation; €40-120 for fillings; €40-150 for extractions",
            "notes": "Several dental clinics in Vilnius cater to international patients. Good quality, competitive prices.",
            "emergencyTip": "Private dental clinics offer emergency appointments. Hospital emergency departments available for dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "116 123 (Emotional Support Line, free, 24/7)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Vilnius. Expect €40-70 per session.",
            "notes": "Mental health services available in Vilnius. English-speaking therapists can be found through private practice."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving. Vilnius Old Town has cobblestones that pose challenges, but newer areas are better adapted.",
            "hospitalAccess": "Major hospitals are wheelchair accessible.",
            "transport": "Vilnius buses are partially accessible. Accessible taxis available with booking.",
            "tips": "Vilnius Old Town is hilly with cobblestones. The new city center and shopping areas are more accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Lithuania has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private clinics provide English-language documentation. Public hospitals provide invoices. EU/EEA citizens present EHIC. Keep all receipts and medical records for insurance claims."
    },
    "EE": {
        "iso2": "EE",
        "countryName": "Estonia",
        "countrySlug": "estonia",
        "flag": "🇪🇪",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare funded by social tax. EU/EEA citizens covered with EHIC. Good private healthcare available, especially in Tallinn.",
        "healthcareSystemType": "universal",
        "qualityRating": 4,
        "qualityNotes": "Good healthcare system with modern digital infrastructure (e-Health system). Most doctors in Tallinn speak English. Estonia is one of the most digitally advanced countries in the world — medical records are electronic.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (apteek) open Mon-Fri 8am-8pm, Sat 9am-5pm. Extended hours at some Tallinn locations.",
        "pharmacyTips": "Apotheka and Südameapteek are major pharmacy chains. Pharmacists are highly trained and often speak English, especially in Tallinn.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol",
            "cold and flu remedies",
            "stomach medication",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Estonia follows EU prescription regulations. Many medications require a prescription. EU/EEA prescriptions accepted through the EU cross-border prescription system.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only."
            },
            {
                "name": "Opioids and benzodiazepines",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers. Doctor's letter for non-EU travelers."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Estonia. Some CBD products may be available in limited forms."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$30-55/week",
            "tips": "Healthcare is reasonably priced. Insurance recommended for private care access and medical evacuation."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for rural/forested areas, spring through autumn)"
            ],
            "notes": "No mandatory vaccinations. Estonia has tick-borne encephalitis risk. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink throughout Estonia.",
        "foodSafetyTips": "Good food safety standards. Estonian cuisine features rye bread, smoked fish, and dairy products — all safe from reputable sources.",
        "medicalTourismNote": "Estonia is known for dental tourism and health IT services. Tallinn has modern dental clinics at competitive prices.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Tallinn",
            "Estonian Health Board",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Estonia. Emergency number 112, pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "East Tallinn Central Hospital (Ida-Tallinna Keskhaigla)",
                "nearTouristArea": "Central Tallinn",
                "phone": "+372 666 1900",
                "englishSpeaking": True,
                "notes": "Major hospital with emergency department. English spoken. Modern facilities."
            },
            {
                "name": "North Estonia Medical Centre (PERH)",
                "nearTouristArea": "Tallinn (Mustamäe district)",
                "phone": "+372 617 1300",
                "englishSpeaking": True,
                "notes": "Largest hospital in Estonia. Full emergency services 24/7."
            },
            {
                "name": "Tartu University Hospital",
                "nearTouristArea": "Tartu (Estonia's second city)",
                "phone": "+372 731 8111",
                "englishSpeaking": True,
                "notes": "Major university hospital. Full range of services."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Mul on vaja peavalurohtu",
                "transliteration": "Mul on VA-ya PEA-va-lu-roh-tu"
            },
            {
                "english": "I have a stomachache",
                "local": "Mul on kõhuvalu",
                "transliteration": "Mul on KUH-hu-va-lu"
            },
            {
                "english": "I'm allergic to...",
                "local": "Mul on allergia...",
                "transliteration": "Mul on al-LEHR-gee-a..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Kus on lähim apteek?",
                "transliteration": "Kus on LA-him AP-teek?"
            },
            {
                "english": "I need a doctor",
                "local": "Mul on vaja arsti",
                "transliteration": "Mul on VA-ya ARS-ti"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Tallinn and Tartu. Modern clinics with English-speaking dentists.",
            "costRange": "€30-70 for consultation; €50-150 for fillings; €50-200 for extractions",
            "notes": "Tallinn dental clinics cater to Nordic dental tourists. Good quality at competitive prices.",
            "emergencyTip": "Private dental clinics offer emergency slots. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "116 123 (Crisis Helpline, 24/7, free)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Tallinn. Expect €50-90 per session.",
            "notes": "Estonia has good digital health services. English-speaking therapists available in Tallinn through private practice."
        },
        "accessibilityInfo": {
            "overview": "Good accessibility in newer buildings. Tallinn Old Town has cobblestones and some steep areas that are challenging.",
            "hospitalAccess": "Major hospitals are wheelchair accessible with modern facilities.",
            "transport": "Tallinn trams and buses are largely accessible. Free public transport for Tallinn residents. Accessible taxis available.",
            "tips": "Tallinn Old Town's lower town is more accessible than the upper town (Toompea). Most museums and new buildings are well-adapted."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Estonia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Estonia's digital health system means records are well-organized. Private clinics provide English documentation. EU/EEA citizens present EHIC. Keep all receipts for claims."
    },
    "SK": {
        "iso2": "SK",
        "countryName": "Slovakia",
        "countrySlug": "slovakia",
        "flag": "🇸🇰",
        "emergencyNumber": "112 (general), 155 (ambulance)",
        "healthcareSystem": "Universal public healthcare funded by mandatory health insurance. EU/EEA citizens covered with EHIC. Private healthcare growing in Bratislava.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Private hospitals in Bratislava offer good care. Public hospitals are functional but can be crowded. Many younger doctors speak English. Private healthcare recommended for visitors.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (lekáreň) open Mon-Fri 7:30am-6pm, Sat 8am-12pm. Extended hours and 24/7 pharmacies available in Bratislava.",
        "pharmacyTips": "Green cross marks pharmacies. Dr. Max is the largest pharmacy chain. Pharmacists are knowledgeable. Some speak English in Bratislava.",
        "commonOTC": [
            "ibuprofen (Ibalgin, Nurofen)",
            "paracetamol (Paralen)",
            "cold remedies (Coldrex, Theraflu)",
            "stomach medication",
            "antihistamines (Zyrtec)",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Slovakia follows EU prescription regulations. Antibiotics and many medications require a prescription. EU/EEA prescriptions may be accepted.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only."
            },
            {
                "name": "Opioids and benzodiazepines",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers. Doctor's letter for others."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Slovakia. Possession can lead to imprisonment."
            }
        ],
        "bringDocumentation": "EU/EEA travelers should carry a Schengen certificate. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$25-50/week",
            "tips": "Healthcare is affordable. Insurance recommended for private care access and any adventure activities in the Tatra Mountains."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for hiking in forested/mountain areas)"
            ],
            "notes": "No mandatory vaccinations. Tick-borne encephalitis is present in forested areas. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink throughout Slovakia. Mountain spring water is generally excellent.",
        "foodSafetyTips": "Slovak cuisine is hearty and safe. Traditional dishes like bryndzové halušky are well-prepared. Food safety standards are good.",
        "medicalTourismNote": "Slovakia offers affordable dental care and spa/thermal treatments. Piešťany and Bardejov are famous spa towns.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Bratislava",
            "Slovak Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Slovakia. Emergency numbers (112/155), pharmacy tips, hospital info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "University Hospital Bratislava (Nemocnica Ružinov)",
                "nearTouristArea": "Bratislava (Ružinov district)",
                "phone": "+421 2 4823 4111",
                "englishSpeaking": True,
                "notes": "Largest hospital in Slovakia. Emergency department 24/7."
            },
            {
                "name": "Medissimo Clinic",
                "nearTouristArea": "Central Bratislava",
                "phone": "+421 2 5441 8626",
                "englishSpeaking": True,
                "notes": "Private clinic with English-speaking doctors. Good for tourist visits."
            },
            {
                "name": "University Hospital Martin",
                "nearTouristArea": "Martin (near Tatra Mountains)",
                "phone": "+421 43 420 3111",
                "englishSpeaking": True,
                "notes": "Major hospital serving the central Slovakia/Tatra region."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Potrebujem liek na bolesť hlavy",
                "transliteration": "Po-TREH-boo-yem lee-ek na BO-lest HLA-vee"
            },
            {
                "english": "I have a stomachache",
                "local": "Bolí ma brucho",
                "transliteration": "BO-lee ma BROO-kho"
            },
            {
                "english": "I'm allergic to...",
                "local": "Som alergický/alergická na...",
                "transliteration": "Som ah-LEHR-gits-kee na..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Kde je najbližšia lekáreň?",
                "transliteration": "Kdeh yeh NAY-bleezh-shya LEH-kaa-ren?"
            },
            {
                "english": "I need a doctor",
                "local": "Potrebujem lekára",
                "transliteration": "Po-TREH-boo-yem LEH-kaa-ra"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Bratislava and major cities. Affordable prices.",
            "costRange": "€20-50 for consultation; €30-100 for fillings; €40-120 for extractions",
            "notes": "Bratislava has good dental clinics. Popular with Austrian dental tourists due to proximity to Vienna.",
            "emergencyTip": "Private dental clinics offer emergency appointments. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "0800 500 333 (Linka dôvery — crisis line, free)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Limited but available in Bratislava. Expect €40-70 per session.",
            "notes": "Mental health services available. English-speaking therapists available in Bratislava through private practice."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving. Bratislava's Old Town has cobblestones but newer areas are well-adapted.",
            "hospitalAccess": "Major hospitals are wheelchair accessible.",
            "transport": "Bratislava public transport is partially accessible. Newer trams and buses have low floors. Accessible taxis available.",
            "tips": "Bratislava Old Town and Tatra Mountain trails can be challenging. Newer hotels and shopping centers are accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Slovakia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Clinics provide receipts and documentation. Request English-language medical reports. EU/EEA citizens present EHIC at public facilities. Keep all documentation for insurance claims."
    },
    "SI": {
        "iso2": "SI",
        "countryName": "Slovenia",
        "countrySlug": "slovenia",
        "flag": "🇸🇮",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare funded by mandatory health insurance. EU/EEA citizens covered with EHIC. Good quality healthcare system.",
        "healthcareSystemType": "universal",
        "qualityRating": 4,
        "qualityNotes": "Good healthcare system with modern facilities. Ljubljana has excellent hospitals. Most doctors speak English. Wait times for non-emergencies can be long in the public system.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies (lekarna) open Mon-Fri 7:30am-7pm, Sat 8am-1pm. 24/7 pharmacy in Ljubljana (Central Pharmacy, Prešernov trg).",
        "pharmacyTips": "Green cross marks pharmacies. Lekarna Ljubljana is the main pharmacy network. Pharmacists are highly trained and speak English.",
        "commonOTC": [
            "ibuprofen (Ibuprofen Krka)",
            "paracetamol (Lekadol)",
            "cold remedies",
            "stomach medication",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Slovenia follows EU prescription regulations strictly. Many medications require a prescription. EU/EEA prescriptions are accepted.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "restricted",
                "note": "Prescription only."
            },
            {
                "name": "Opioids and benzodiazepines",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Medical cannabis available by prescription. Recreational use is decriminalized for small amounts but still illegal."
            }
        ],
        "bringDocumentation": "EU/EEA travelers carry a Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$30-55/week",
            "tips": "Insurance recommended for adventure sports (skiing, hiking, canyoning) coverage and private healthcare access."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Tick-borne Encephalitis (for outdoor activities in forested areas)"
            ],
            "notes": "No mandatory vaccinations. Tick-borne encephalitis present in forested areas. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Slovenia has excellent tap water quality. Many natural springs are also safe to drink from. The country is known for pristine water sources.",
        "foodSafetyTips": "Excellent food safety standards. Local cuisine is a mix of Mediterranean, Central European, and Balkan influences. All food is safe at restaurants.",
        "medicalTourismNote": "Slovenia offers thermal spa treatments and dental tourism. Prices are lower than Austria or Italy but quality is comparable.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Ljubljana",
            "National Institute of Public Health of Slovenia",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Slovenia. Emergency number 112, pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "University Medical Centre Ljubljana (UKC Ljubljana)",
                "nearTouristArea": "Central Ljubljana",
                "phone": "+386 1 522 5050",
                "englishSpeaking": True,
                "notes": "Largest hospital in Slovenia. Full emergency services 24/7. English spoken by most staff."
            },
            {
                "name": "Medicor Medical Center",
                "nearTouristArea": "Ljubljana",
                "phone": "+386 1 530 1800",
                "englishSpeaking": True,
                "notes": "Private medical center. Good for non-emergency tourist consultations."
            },
            {
                "name": "General Hospital Izola",
                "nearTouristArea": "Slovenian Coast (Piran/Portorož area)",
                "phone": "+386 5 660 6000",
                "englishSpeaking": True,
                "notes": "Nearest hospital to the popular coastal resort area."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Potrebujem zdravilo za glavobol",
                "transliteration": "Po-TREH-boo-yem ZDRA-vee-lo za GLA-vo-bol"
            },
            {
                "english": "I have a stomachache",
                "local": "Boli me trebuh",
                "transliteration": "BO-lee meh TREH-booh"
            },
            {
                "english": "I'm allergic to...",
                "local": "Alergičen/Alergična sem na...",
                "transliteration": "ah-lehr-GEECH-en sem na..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Kje je najbližja lekarna?",
                "transliteration": "Kyeh yeh NAY-bleezh-ya LEH-kar-na?"
            },
            {
                "english": "I need a doctor",
                "local": "Potrebujem zdravnika",
                "transliteration": "Po-TREH-boo-yem ZDRAV-nee-ka"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care throughout Slovenia. Modern clinics with English-speaking dentists.",
            "costRange": "€30-70 for consultation; €50-150 for fillings; €60-200 for extractions",
            "notes": "Quality dental care at lower prices than neighboring Austria or Italy. Ljubljana has excellent dental clinics.",
            "emergencyTip": "Emergency dental service available through UKC Ljubljana. Private clinics also offer emergency slots."
        },
        "mentalHealth": {
            "crisisLine": "116 123 (Crisis Line, free, 24/7)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available in Ljubljana. Expect €50-90 per session.",
            "notes": "Good mental health services. English-speaking therapists available in Ljubljana."
        },
        "accessibilityInfo": {
            "overview": "Good accessibility in newer infrastructure. Ljubljana is relatively flat and navigable. Some older buildings and mountain areas have limitations.",
            "hospitalAccess": "Major hospitals are fully wheelchair accessible.",
            "transport": "Ljubljana buses are accessible. Trains have some accessible carriages. Accessible taxis available.",
            "tips": "Ljubljana city center is relatively accessible. Lake Bled has some accessible paths. Postojna Cave has wheelchair-accessible tours. Mountain areas require planning."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Slovenia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Hospitals provide receipts and medical documentation. English-language reports available on request. EU/EEA citizens present EHIC. Keep all documentation for insurance claims."
    },
    "CY": {
        "iso2": "CY",
        "countryName": "Cyprus",
        "countrySlug": "cyprus",
        "flag": "🇨🇾",
        "emergencyNumber": "112 (general), 199 (ambulance)",
        "healthcareSystem": "General Healthcare System (GHS/GESY) introduced in 2019 providing universal coverage for residents. EU/EEA citizens covered with EHIC. Good private healthcare widely available.",
        "healthcareSystemType": "universal",
        "qualityRating": 4,
        "qualityNotes": "Good healthcare, especially in private facilities. Most doctors trained in UK or Greece and speak excellent English. Private hospitals in Limassol and Nicosia are modern. A popular retirement destination partly due to healthcare quality.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open Mon-Fri 8am-6pm (with afternoon break 1-3pm in summer), Sat 8am-1pm. Rotating duty pharmacies cover nights and weekends.",
        "pharmacyTips": "Green cross marks pharmacies. Pharmacists speak excellent English. Many medications available OTC that require prescriptions elsewhere in Europe. Check duty pharmacy schedules posted on pharmacy doors.",
        "commonOTC": [
            "ibuprofen (Nurofen)",
            "paracetamol (Panadol, Depon)",
            "cold remedies",
            "stomach medication (Gaviscon)",
            "antihistamines",
            "sunscreen and after-sun care",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Some EU prescription rules apply. Many medications more easily accessible OTC than in other EU countries. EU prescriptions accepted.",
        "restrictedMeds": [
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Medical cannabis recently legalized. Recreational use is illegal. CBD products must meet EU regulations."
            }
        ],
        "bringDocumentation": "EU/EEA travelers carry Schengen certificate for controlled substances. Non-EU travelers bring a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$35-60/week",
            "tips": "Insurance recommended for private healthcare access. Cyprus has good healthcare but costs add up. Ensure water sports and adventure activity coverage if applicable."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B"
            ],
            "notes": "No mandatory vaccinations. Cyprus is a low-risk destination. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink but can taste slightly mineral/chlorinated. Many locals prefer bottled water. Bottled water is cheap.",
        "foodSafetyTips": "Excellent food safety. Mediterranean cuisine with fresh ingredients. Meze, halloumi, and fresh seafood are safe. Restaurants maintain good hygiene standards.",
        "medicalTourismNote": "Cyprus is a growing medical tourism destination, particularly for fertility treatments (IVF), dental care, and cosmetic surgery.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Nicosia",
            "Cyprus Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Cyprus. Emergency numbers (112/199), pharmacy tips, hospital info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Nicosia General Hospital",
                "nearTouristArea": "Nicosia",
                "phone": "+357 22 603 000",
                "englishSpeaking": True,
                "notes": "Largest public hospital. Emergency services 24/7. English widely spoken."
            },
            {
                "name": "Apollonion Private Hospital",
                "nearTouristArea": "Limassol (near tourist area)",
                "phone": "+357 25 858 100",
                "englishSpeaking": True,
                "notes": "Modern private hospital. Popular with expats and tourists."
            },
            {
                "name": "Paphos General Hospital",
                "nearTouristArea": "Paphos (major tourist area)",
                "phone": "+357 26 803 100",
                "englishSpeaking": True,
                "notes": "Main hospital serving the popular Paphos tourist region."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Χρειάζομαι φάρμακο για πονοκέφαλο",
                "transliteration": "Hriazome farmako ya ponokefalo"
            },
            {
                "english": "I have a stomachache",
                "local": "Έχω πόνο στο στομάχι",
                "transliteration": "Echo pono sto stomachi"
            },
            {
                "english": "I'm allergic to...",
                "local": "Είμαι αλλεργικός/αλλεργική σε...",
                "transliteration": "Ime aleryikos/aleryiki se..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Πού είναι το πιο κοντινό φαρμακείο;",
                "transliteration": "Pou ine to pio kontino farmakio?"
            },
            {
                "english": "I need a doctor",
                "local": "Χρειάζομαι γιατρό",
                "transliteration": "Hriazome yatro"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care. Many dentists trained in the UK. English widely spoken.",
            "costRange": "€30-60 for consultation; €50-150 for fillings; €60-200 for extractions",
            "notes": "Cyprus has excellent dental clinics. Dental tourism is growing. Quality comparable to the UK at lower prices.",
            "emergencyTip": "Most dental clinics offer emergency appointments. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "1466 (Mental Health Helpline)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Widely available in all major cities. Many Cypriot therapists trained in the UK. Expect €50-80 per session.",
            "notes": "Good availability of English-speaking mental health professionals due to large expat community."
        },
        "accessibilityInfo": {
            "overview": "Accessibility has improved significantly in recent years. Newer buildings and tourist areas are generally well-adapted.",
            "hospitalAccess": "Hospitals are wheelchair accessible.",
            "transport": "Buses in major cities are increasingly accessible. Taxis are the most flexible option. Wheelchair-accessible taxis available.",
            "tips": "Beach resorts often have accessible paths to the beach. Historic sites like Kourion have some accessible routes. Contact hotels in advance about accessibility."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Cyprus has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Private hospitals provide detailed English-language documentation and invoices. EU/EEA citizens present EHIC at public facilities. Keep all receipts for insurance claims."
    },
    "MT": {
        "iso2": "MT",
        "countryName": "Malta",
        "countrySlug": "malta",
        "flag": "🇲🇹",
        "emergencyNumber": "112",
        "healthcareSystem": "Universal public healthcare for residents and EU/EEA citizens with EHIC. Good private healthcare available. English is an official language.",
        "healthcareSystemType": "universal",
        "qualityRating": 4,
        "qualityNotes": "Good healthcare system. Mater Dei Hospital is modern and well-equipped. English is spoken everywhere (official language). Private healthcare offers shorter wait times.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open Mon-Fri 9am-1pm and 4pm-7pm, Sat 9am-1pm. Duty pharmacies cover nights, Sundays, and holidays (schedule posted in all pharmacies).",
        "pharmacyTips": "Look for the green cross. Pharmacists speak fluent English. Many medications available OTC. The duty pharmacy system ensures one pharmacy is always open in each district.",
        "commonOTC": [
            "ibuprofen (Nurofen)",
            "paracetamol (Panadol, Calpol)",
            "cold remedies",
            "stomach medication (Gaviscon)",
            "antihistamines",
            "sunscreen",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Follows EU prescription standards. Many common medications available OTC. Antibiotics require a prescription.",
        "restrictedMeds": [
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Schengen certificate required for EU travelers."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Malta legalized personal cannabis use in 2021 (first in EU). CBD products available. Do NOT purchase cannabis for export."
            }
        ],
        "bringDocumentation": "EU/EEA travelers carry Schengen certificate for controlled substances. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$35-60/week",
            "tips": "Insurance recommended for private healthcare access and water sports coverage."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A"
            ],
            "notes": "No mandatory vaccinations. Malta is a low-risk destination. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe but tastes heavily chlorinated and mineral. Most residents and visitors drink bottled water or filtered water. Bottled water is inexpensive.",
        "foodSafetyTips": "Good food safety standards. Mediterranean and British-influenced cuisine. Fresh seafood is excellent. Pastizzi and other local snacks are safe from bakeries.",
        "medicalTourismNote": "Malta attracts medical tourists for fertility treatments, cosmetic surgery, and dental care. English-speaking healthcare is a major advantage.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Valletta",
            "Malta Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Malta. Emergency number 112, pharmacy tips, hospital info, and travel insurance advice for tourists.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Mater Dei Hospital",
                "nearTouristArea": "Msida (near Valletta/Sliema)",
                "phone": "+356 2545 0000",
                "englishSpeaking": True,
                "notes": "Malta's main public hospital. Modern facility opened in 2007. Emergency department 24/7. English spoken by all staff."
            },
            {
                "name": "St. James Hospital",
                "nearTouristArea": "Sliema (main tourist/dining area)",
                "phone": "+356 2329 1000",
                "englishSpeaking": True,
                "notes": "Private hospital in prime tourist area. Walk-in consultations available."
            },
            {
                "name": "Gozo General Hospital",
                "nearTouristArea": "Victoria, Gozo",
                "phone": "+356 2156 1600",
                "englishSpeaking": True,
                "notes": "Main hospital on Gozo island. Essential for tourists visiting Gozo."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Għandi bżonn mediċina għall-uġigħ ta' ras",
                "transliteration": "AN-dee BZONN meh-dee-CHEE-na al-OO-jee ta ras"
            },
            {
                "english": "I have a stomachache",
                "local": "Għandi uġigħ ta' żaqqi",
                "transliteration": "AN-dee OO-jee ta ZAK-kee"
            },
            {
                "english": "I'm allergic to...",
                "local": "Għandi allerġija għal...",
                "transliteration": "AN-dee al-lehr-JEE-ya al..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Fejn hi l-eqreb spiżerija?",
                "transliteration": "Feyn hee LEK-reb spee-zeh-REE-ya?"
            },
            {
                "english": "I need a doctor",
                "local": "Għandi bżonn ta' tabib",
                "transliteration": "AN-dee BZONN ta ta-BEEB"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care. English-speaking dentists throughout the island.",
            "costRange": "€30-60 for consultation; €50-150 for fillings; €60-200 for extractions",
            "notes": "Malta has good dental clinics. All dentists speak English. Prices are moderate — lower than UK but higher than Eastern Europe.",
            "emergencyTip": "Mater Dei Hospital has a dental emergency department. Private dentists often accommodate emergencies."
        },
        "mentalHealth": {
            "crisisLine": "179 (Supportline, free, 24/7)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Widely available. English is an official language — all therapists speak it. Expect €40-70 per session.",
            "notes": "Good availability of mental health services. Richmond Foundation provides support and referrals."
        },
        "accessibilityInfo": {
            "overview": "Malta has challenges with accessibility due to historical architecture, but improvements continue. Newer buildings are accessible.",
            "hospitalAccess": "Mater Dei Hospital is fully wheelchair accessible. Older health centers may have limitations.",
            "transport": "Malta's public buses are wheelchair accessible. Accessible taxis available. The Malta airport is accessible.",
            "tips": "Valletta has steep streets but a lift from the waterfront. Some historic sites are challenging. Beach access can be limited — some beaches have accessible facilities."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies.",
            "notes": "Malta has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Mater Dei Hospital provides receipts and documentation in English. Private clinics issue detailed invoices. EU/EEA citizens present EHIC at public facilities. Keep all documentation for insurance claims."
    },
    "LU": {
        "iso2": "LU",
        "countryName": "Luxembourg",
        "countrySlug": "luxembourg",
        "flag": "🇱🇺",
        "emergencyNumber": "112",
        "healthcareSystem": "Excellent universal healthcare system funded by mandatory social insurance. EU/EEA citizens covered with EHIC. One of the best-funded healthcare systems in Europe.",
        "healthcareSystemType": "universal",
        "qualityRating": 5,
        "qualityNotes": "Outstanding healthcare quality. Modern facilities. Most medical staff speak multiple languages (French, German, English, Luxembourgish). Short wait times compared to neighboring countries.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open Mon-Fri 8am-6:30pm, Sat 8am-12:30pm. Duty pharmacies cover nights, weekends, and holidays.",
        "pharmacyTips": "Green cross marks pharmacies. Pharmacists speak multiple languages. Well-stocked pharmacies with high standards. Check the duty pharmacy schedule (pharmacie de garde) for after-hours needs.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol (Dafalgan)",
            "cold and flu remedies",
            "stomach medication",
            "antihistamines",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Follows EU prescription regulations strictly. Many medications require a prescription. EU/EEA prescriptions accepted.",
        "restrictedMeds": [
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Schengen certificate required."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "restricted",
                "note": "Luxembourg legalized personal cannabis cultivation and use in 2023. CBD products must meet EU regulations."
            }
        ],
        "bringDocumentation": "EU/EEA travelers carry a Schengen certificate. Non-EU travelers need a doctor's letter. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "EU/EEA citizens should carry EHIC.",
            "averageCost": "$50-90/week",
            "tips": "Luxembourg has excellent but expensive healthcare. Insurance is strongly recommended for non-EU visitors."
        },
        "vaccinations": {
            "required": [],
            "recommended": [],
            "notes": "No mandatory or specially recommended vaccinations. Luxembourg is a very low-risk destination. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is excellent quality and safe to drink everywhere in Luxembourg.",
        "foodSafetyTips": "Excellent food safety standards. Diverse culinary scene reflecting French, German, and international influences. All food establishments maintain high hygiene standards.",
        "medicalTourismNote": "Luxembourg is not a typical medical tourism destination due to high costs, but offers exceptional quality for those who seek it.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Luxembourg",
            "Luxembourg Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Luxembourg. Emergency number 112, pharmacy tips, hospital info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": True,
        "hospitals": [
            {
                "name": "Centre Hospitalier de Luxembourg (CHL)",
                "nearTouristArea": "Luxembourg City center",
                "phone": "+352 44 11 11",
                "englishSpeaking": True,
                "notes": "Main hospital. Full emergency services 24/7. Multilingual staff (French, German, English, Luxembourgish)."
            },
            {
                "name": "Hôpitaux Robert Schuman (HRS)",
                "nearTouristArea": "Luxembourg City (Kirchberg)",
                "phone": "+352 2468 1",
                "englishSpeaking": True,
                "notes": "Major hospital group. Modern facilities near the European institutions area."
            },
            {
                "name": "Centre Hospitalier du Nord (CHdN)",
                "nearTouristArea": "Ettelbruck (northern Luxembourg, Ardennes region)",
                "phone": "+352 81 66 1",
                "englishSpeaking": True,
                "notes": "Main hospital for northern Luxembourg and the Ardennes tourist region."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "J'ai besoin d'un médicament contre le mal de tête",
                "transliteration": "Zhay beh-ZWAN dun may-dee-kah-MON kontr luh mal duh tet"
            },
            {
                "english": "I have a stomachache",
                "local": "J'ai mal au ventre",
                "transliteration": "Zhay mal oh vontr"
            },
            {
                "english": "I'm allergic to...",
                "local": "Je suis allergique à...",
                "transliteration": "Zhuh swee ah-lehr-ZHEEK ah..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Où est la pharmacie la plus proche?",
                "transliteration": "Oo ay la far-ma-SEE la ploo prosh?"
            },
            {
                "english": "I need a doctor",
                "local": "J'ai besoin d'un médecin",
                "transliteration": "Zhay beh-ZWAN dun may-deh-SAN"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care. Multilingual dentists throughout the country.",
            "costRange": "€50-120 for consultation; €80-250 for fillings; €100-300 for extractions",
            "notes": "High-quality dental care but expensive. Most dentists speak French, German, and English.",
            "emergencyTip": "Call CHL (Centre Hospitalier de Luxembourg) for dental emergencies outside regular hours."
        },
        "mentalHealth": {
            "crisisLine": "454545 (SOS Détresse, 24/7, multilingual)",
            "internationalLine": "112 for psychiatric emergencies",
            "englishTherapists": "Available. Luxembourg's international population means many therapists speak English. Expect €80-120 per session.",
            "notes": "Good mental health services in multiple languages. Large international community means English-speaking options are common."
        },
        "accessibilityInfo": {
            "overview": "Good accessibility infrastructure. Luxembourg has invested in accessible public spaces and transport.",
            "hospitalAccess": "All hospitals are wheelchair accessible with modern facilities.",
            "transport": "Luxembourg has free public transport since 2020. Buses and trams are wheelchair accessible. The modern tram system is fully accessible.",
            "tips": "Luxembourg City's Grund (lower town) is accessed by elevator. The Kirchberg district is modern and accessible. Historical old town has some cobblestone areas."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at pharmacies and clinics.",
            "notes": "Luxembourg has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Luxembourg hospitals provide detailed multilingual documentation. EU/EEA citizens present EHIC. Non-EU visitors pay upfront and claim from insurance. Healthcare costs are high — keep all receipts."
    },
    "HK": {
        "iso2": "HK",
        "countryName": "Hong Kong",
        "countrySlug": "hong-kong",
        "flag": "🇭🇰",
        "emergencyNumber": "999 (general emergency), 112 (mobile phones)",
        "healthcareSystem": "Dual public-private system. Public hospitals (Hospital Authority) provide subsidized care. Private hospitals offer premium care. Tourists typically use Accident & Emergency departments or private hospitals.",
        "healthcareSystemType": "mixed",
        "qualityRating": 5,
        "qualityNotes": "World-class healthcare with some of the best hospitals in Asia. English widely spoken in hospitals. Public hospitals have long wait times for non-emergencies. Private hospitals offer faster, premium service.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open daily 9am-10pm. Mannings and Watsons chains have extended hours. Some 24/7 pharmacies in busy areas.",
        "pharmacyTips": "Mannings and Watsons are the major pharmacy chains (found in every MTR station area). Pharmacists speak English. Many medications available OTC. Traditional Chinese medicine shops (涼茶鋪) are also widespread.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol (Panadol — very popular brand)",
            "cold and flu remedies",
            "stomach medication",
            "antihistamines",
            "Tiger Balm and traditional remedies",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Many medications available OTC in Hong Kong. Antibiotics available at pharmacies without prescription in practice. Controlled substances require a prescription.",
        "restrictedMeds": [
            {
                "name": "Strong opioids (morphine, methadone)",
                "status": "controlled",
                "note": "Strictly controlled. Bring documentation."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring a doctor's letter and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis in any form is strictly illegal in Hong Kong, including CBD products."
            },
            {
                "name": "Pseudoephedrine",
                "status": "restricted",
                "note": "Controlled quantity. Available in pharmacies with purchase limits."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for controlled substances. Keep medications in original packaging. Declare controlled medications at customs if quantities are significant.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$40-75/week",
            "tips": "Public hospital A&E charges are HKD 1,590 (~$200) for non-residents. Private hospitals are expensive ($500+ for a basic visit). Insurance is strongly recommended."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B"
            ],
            "notes": "No mandatory vaccinations. Hong Kong is a modern, low-risk destination. Ensure routine vaccinations are current."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water meets WHO standards but many locals boil or filter it due to concerns about building pipes. Bottled water is widely available and inexpensive.",
        "foodSafetyTips": "Hong Kong has high food safety standards. Street food and dai pai dong (outdoor food stalls) are a highlight and generally safe. Dim sum restaurants and local cha chaan teng maintain good hygiene.",
        "medicalTourismNote": "Hong Kong is known for advanced medical care, particularly orthopedics, cancer treatment, and Traditional Chinese Medicine.",
        "sources": [
            "CDC Travelers' Health",
            "US Consulate Hong Kong",
            "Hong Kong Department of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Hong Kong. Emergency number 999, pharmacy tips, hospital recommendations, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Queen Mary Hospital",
                "nearTouristArea": "Pokfulam, Hong Kong Island (near HKU)",
                "phone": "+852 2255 3838",
                "englishSpeaking": True,
                "notes": "Top-ranked public hospital. Major trauma center. English widely spoken."
            },
            {
                "name": "Matilda International Hospital",
                "nearTouristArea": "The Peak, Hong Kong Island",
                "phone": "+852 2849 0111",
                "englishSpeaking": True,
                "notes": "Private international hospital. Popular with expats and tourists. English-first service."
            },
            {
                "name": "Hong Kong Adventist Hospital",
                "nearTouristArea": "Stubbs Road, Hong Kong Island (near Happy Valley)",
                "phone": "+852 3651 8888",
                "englishSpeaking": True,
                "notes": "Private hospital with international standards. Good for tourist medical needs."
            },
            {
                "name": "Queen Elizabeth Hospital",
                "nearTouristArea": "Yau Ma Tei, Kowloon (near Tsim Sha Tsui)",
                "phone": "+852 3506 8888",
                "englishSpeaking": True,
                "notes": "Major public hospital in Kowloon, near the main tourist hotel district."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "我需要頭痛藥",
                "transliteration": "Ngo seui-yiu tau-tung yeuk (Cantonese)"
            },
            {
                "english": "I have a stomachache",
                "local": "我肚痛",
                "transliteration": "Ngo tou-tung (Cantonese)"
            },
            {
                "english": "I'm allergic to...",
                "local": "我對...敏感",
                "transliteration": "Ngo deui...man-gam (Cantonese)"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "最近嘅藥房喺邊度？",
                "transliteration": "Jeui-kan ge yeuk-fong hai bin-dou? (Cantonese)"
            },
            {
                "english": "I need a doctor",
                "local": "我需要睇醫生",
                "transliteration": "Ngo seui-yiu tai yi-sang (Cantonese)"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care. Many dentists trained internationally. English widely spoken.",
            "costRange": "HKD 500-1,500 ($65-195) for consultation; HKD 1,000-5,000 ($130-650) for fillings",
            "notes": "High-quality dental care but expensive. Quality Dental in Central and other private practices cater to English speakers.",
            "emergencyTip": "Public hospital A&E departments handle dental emergencies. Private dental clinics in Central and Tsim Sha Tsui offer emergency appointments."
        },
        "mentalHealth": {
            "crisisLine": "2382 0000 (Samaritans, 24/7, English and Cantonese)",
            "internationalLine": "2896 0000 (The Samaritan Befrienders, multilingual)",
            "englishTherapists": "Widely available. Many international therapists. Expect HKD 1,000-2,500 ($130-325) per session.",
            "notes": "Good availability of English-speaking mental health professionals. Mind HK provides resources and referrals."
        },
        "accessibilityInfo": {
            "overview": "Good accessibility in modern areas. MTR is fully accessible. Hong Kong is hilly with many steps in older areas.",
            "hospitalAccess": "All public and major private hospitals are wheelchair accessible.",
            "transport": "MTR is fully wheelchair accessible with elevators and tactile floor tiles. Buses are partially accessible. Accessible taxis available but limited — book in advance.",
            "tips": "Hong Kong is hilly — use the MTR for the most accessible travel. Mid-Levels Escalator is helpful but has stairs at some points. Many shopping malls provide barrier-free access."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "Masks no longer required. Still commonly worn by locals.",
            "testing": "Tests available at clinics and hospitals.",
            "notes": "Hong Kong lifted all COVID restrictions in 2023."
        },
        "insuranceClaimProcess": "Public hospitals provide receipts and medical documentation in English. Private hospitals issue detailed English invoices. Keep all documentation for insurance claims. Most private hospitals can arrange direct billing with international insurers."
    },
    "TW": {
        "iso2": "TW",
        "countryName": "Taiwan",
        "countrySlug": "taiwan",
        "flag": "🇹🇼",
        "emergencyNumber": "119 (ambulance/fire), 110 (police)",
        "healthcareSystem": "Universal National Health Insurance (NHI) covers residents. Tourists pay out-of-pocket but costs are very affordable. Excellent quality throughout.",
        "healthcareSystemType": "universal",
        "qualityRating": 5,
        "qualityNotes": "Excellent healthcare system consistently ranked among the best globally. Modern hospitals with advanced technology. English spoken at major hospitals in Taipei. Very affordable even without insurance.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open daily 9am-10pm. Watson's and Cosmed chains found everywhere. Hospital pharmacies and some chain pharmacies open extended hours.",
        "pharmacyTips": "Look for 藥局 (pharmacy) signs. Watson's and Cosmed are major chains. Many medications available OTC at low prices. Pharmacists in Taipei often speak some English.",
        "commonOTC": [
            "ibuprofen",
            "paracetamol (普拿疼 Panadol — very common)",
            "cold medicine (感冒藥)",
            "stomach medication",
            "antihistamines",
            "Tiger Balm and medicated patches",
            "band-aids and first aid"
        ],
        "prescriptionRules": "Many medications available OTC that require prescriptions elsewhere. Antibiotics available at pharmacies. Controlled substances require a local prescription.",
        "restrictedMeds": [
            {
                "name": "Amphetamines/ADHD medications",
                "status": "controlled",
                "note": "Controlled substances. Bring documentation and keep in original packaging."
            },
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Strictly regulated. Bring a doctor's letter and customs declaration."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled substance. Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is strictly illegal in Taiwan. Penalties are severe."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English (and Chinese if possible) for controlled medications. Keep all medicines in original packaging. For large quantities, declare at customs.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Healthcare in Taiwan is very affordable — an ER visit may cost only $20-50 without insurance. Insurance still recommended for hospital stays and medical evacuation."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Japanese Encephalitis (for rural areas or extended stays)"
            ],
            "notes": "No mandatory vaccinations. Ensure routine vaccinations are current."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water should be boiled before drinking in Taiwan. Most hotels and restaurants provide boiled or filtered water. Bottled water is cheap and available everywhere.",
        "foodSafetyTips": "Taiwan is a food paradise with excellent food safety at most establishments. Night market food is legendary and generally safe — stick to busy stalls. Fruits should be washed or peeled.",
        "medicalTourismNote": "Taiwan is a top medical tourism destination, especially for health checkups, cosmetic surgery, dental care, and Traditional Chinese Medicine. Costs are 50-70% less than the US.",
        "sources": [
            "CDC Travelers' Health",
            "American Institute in Taiwan",
            "Taiwan Centers for Disease Control",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Taiwan. Emergency numbers (119/110), pharmacy tips, hospital info, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "National Taiwan University Hospital (NTUH)",
                "nearTouristArea": "Zhongzheng District, Taipei (near Chiang Kai-shek Memorial)",
                "phone": "+886 2 2312 3456",
                "englishSpeaking": True,
                "notes": "Taiwan's top-ranked hospital. International medical service center for foreign patients."
            },
            {
                "name": "Taipei Veterans General Hospital",
                "nearTouristArea": "Beitou, Taipei (near hot springs area)",
                "phone": "+886 2 2871 2121",
                "englishSpeaking": True,
                "notes": "Major medical center with international patient services."
            },
            {
                "name": "Mackay Memorial Hospital",
                "nearTouristArea": "Zhongshan District, Taipei (near Zhongshan MRT)",
                "phone": "+886 2 2543 3535",
                "englishSpeaking": True,
                "notes": "Well-known private hospital. International patient center. Good English service."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "我需要頭痛藥",
                "transliteration": "Wǒ xūyào tóutòng yào"
            },
            {
                "english": "I have a stomachache",
                "local": "我肚子痛",
                "transliteration": "Wǒ dùzi tòng"
            },
            {
                "english": "I'm allergic to...",
                "local": "我對...過敏",
                "transliteration": "Wǒ duì...guòmǐn"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "最近的藥局在哪裡？",
                "transliteration": "Zuìjìn de yàojú zài nǎlǐ?"
            },
            {
                "english": "I need a doctor",
                "local": "我需要看醫生",
                "transliteration": "Wǒ xūyào kàn yīshēng"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care at very affordable prices. Many dentists speak English in Taipei.",
            "costRange": "TWD 500-2,000 ($15-65) for consultation; TWD 1,000-5,000 ($30-160) for fillings",
            "notes": "Dental care in Taiwan is excellent and very affordable. Many dental clinics in Taipei cater to international patients.",
            "emergencyTip": "Major hospitals have dental departments. Many private dental clinics in Taipei offer same-day emergency appointments."
        },
        "mentalHealth": {
            "crisisLine": "1925 (Suicide Prevention Hotline, 24/7)",
            "internationalLine": "0800-788-995 (Community Mental Health Center, free)",
            "englishTherapists": "Available in Taipei. Expect TWD 2,000-4,000 ($65-130) per session.",
            "notes": "English-speaking mental health services available in Taipei through international clinics and private practice."
        },
        "accessibilityInfo": {
            "overview": "Good accessibility in Taipei. MRT is fully accessible. Improvements continue but older areas may have barriers.",
            "hospitalAccess": "Major hospitals are fully wheelchair accessible with excellent facilities.",
            "transport": "Taipei MRT is fully wheelchair accessible. Buses have low floors. Accessible taxis available. YouBike system not wheelchair accessible.",
            "tips": "Taipei is generally accessible with good sidewalk infrastructure. Night markets can be crowded. National Palace Museum and major attractions are accessible. Jiufen Old Street has many stairs."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "Masks no longer required. Still commonly worn on public transit.",
            "testing": "Tests available at hospitals, clinics, and pharmacies.",
            "notes": "Taiwan lifted all COVID restrictions. Some healthcare settings may still request masks."
        },
        "insuranceClaimProcess": "Taiwanese hospitals provide detailed receipts and English-language medical certificates on request. International departments assist with insurance documentation. Costs are low — many travelers pay out-of-pocket. File claims with your insurer within 30 days."
    },
    "LA": {
        "iso2": "LA",
        "countryName": "Laos",
        "countrySlug": "laos",
        "flag": "🇱🇦",
        "emergencyNumber": "1195 (ambulance), 1191 (police), 1190 (fire)",
        "healthcareSystem": "Public healthcare system with limited resources. Quality varies greatly. Serious conditions require evacuation to Thailand. Limited private options in Vientiane.",
        "healthcareSystemType": "mixed",
        "qualityRating": 1,
        "qualityNotes": "Healthcare facilities are basic, especially outside Vientiane. The best option in Laos is the Alliance International Medical Center in Vientiane. For serious conditions, medical evacuation to Udon Thani or Bangkok, Thailand is standard practice.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open daily 8am-8pm in cities. Limited hours and availability in rural areas.",
        "pharmacyTips": "Pharmacies (ฮ້ານຂາຍຢາ) vary in quality. In Vientiane, there are modern pharmacies near the Morning Market area. Many medications available OTC including antibiotics. Quality of medications can be questionable — buy from reputable pharmacies only.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "oral rehydration salts",
            "anti-diarrheal medication",
            "antibiotics (widely available OTC)",
            "antimalarials",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Very relaxed prescription requirements. Most medications available OTC. Quality and authenticity of medications should be verified — counterfeit drugs are a concern.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Bring documentation. Laos has strict drug penalties."
            },
            {
                "name": "Amphetamines/stimulants",
                "status": "banned",
                "note": "Laos has very strict drug laws with severe penalties including death."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal. Severe penalties including long imprisonment."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for all prescription medications. Laos has very strict drug laws — ensure all medications are clearly documented with a prescription. Keep in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-40/week",
            "tips": "Travel insurance with medical evacuation coverage to Thailand is ESSENTIAL. Healthcare in Laos is very limited. Ensure your policy covers helicopter evacuation from remote areas."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Japanese Encephalitis",
                "Rabies (strongly recommended due to stray dogs)",
                "Malaria prophylaxis (for rural and border areas)"
            ],
            "notes": "Malaria risk exists in rural areas. Dengue fever is present — use mosquito repellent. Yellow fever certificate required if arriving from an endemic area."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do NOT drink tap water. Always use bottled or boiled water. Avoid ice in drinks except at upscale restaurants. Use bottled water even for brushing teeth in remote areas.",
        "foodSafetyTips": "Eat freshly cooked food from busy establishments. Avoid raw vegetables and unpeeled fruits from street vendors. Laap (minced meat salad) should be well-cooked, not raw. Sticky rice and grilled dishes are generally safe when fresh.",
        "medicalTourismNote": "Laos is not a medical tourism destination. Medical tourists in the region typically go to Thailand.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Vientiane",
            "Lao Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Laos. Emergency numbers, pharmacy tips, hospital info, vaccination requirements, and why medical evacuation insurance is essential.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Alliance International Medical Center",
                "nearTouristArea": "Vientiane (near city center)",
                "phone": "+856 21 513 095",
                "englishSpeaking": True,
                "notes": "Best medical facility in Laos. French and English-speaking staff. For serious conditions, they arrange evacuation to Thailand."
            },
            {
                "name": "Mahosot Hospital (International Clinic)",
                "nearTouristArea": "Vientiane (near Mekong riverside)",
                "phone": "+856 21 214 022",
                "englishSpeaking": True,
                "notes": "Main public hospital. International clinic section has some English-speaking doctors."
            },
            {
                "name": "Luang Prabang Provincial Hospital",
                "nearTouristArea": "Luang Prabang (major tourist city)",
                "phone": "+856 71 254 023",
                "englishSpeaking": False,
                "notes": "Basic hospital. For serious conditions, evacuation to Vientiane or Thailand required."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "ຂ້ອຍຕ້ອງການຢາແກ້ປວດຫົວ",
                "transliteration": "Khoi tong-kaan yaa kae puad hua"
            },
            {
                "english": "I have a stomachache",
                "local": "ຂ້ອຍເຈັບທ້ອງ",
                "transliteration": "Khoi jep thong"
            },
            {
                "english": "I'm allergic to...",
                "local": "ຂ້ອຍແພ້...",
                "transliteration": "Khoi phae..."
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "ຮ້ານຂາຍຢາໃກ້ທີ່ສຸດຢູ່ໃສ?",
                "transliteration": "Haan khai yaa kai thi sut yu sai?"
            },
            {
                "english": "I need a doctor",
                "local": "ຂ້ອຍຕ້ອງການໝໍ",
                "transliteration": "Khoi tong-kaan maw"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care in Vientiane. Very limited elsewhere. Consider crossing to Thailand for dental work.",
            "costRange": "$10-30 for consultation; $15-50 for fillings; $10-40 for extractions",
            "notes": "Dental facilities are basic. For anything beyond emergencies, Udon Thani (Thailand) is a short drive from Vientiane and has excellent dental clinics.",
            "emergencyTip": "For dental emergencies, visit Alliance International Medical Center in Vientiane or cross to Thailand."
        },
        "mentalHealth": {
            "crisisLine": "No dedicated crisis line available",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some available through Alliance International Medical Center.",
            "notes": "Mental health services are very limited in Laos. For English-speaking support, contact your embassy or use international online platforms."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited in Laos. Most buildings, roads, and transport are not wheelchair accessible.",
            "hospitalAccess": "Alliance International Medical Center has basic accessibility. Public hospitals have very limited accessibility.",
            "transport": "No accessible public transport. Private vehicles or tuk-tuks are the main options. Roads are often unpaved.",
            "tips": "Laos is very challenging for travelers with mobility limitations. Luang Prabang's streets are relatively flat but narrow. Vientiane's main areas are more navigable. Contact tour operators specializing in accessible travel for advice."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at some clinics in Vientiane.",
            "notes": "Laos has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "Alliance International Medical Center provides English-language documentation. Public hospitals provide basic receipts that may be in Lao only. Medical evacuation to Thailand is common — ensure your insurance covers this. Keep all documentation."
    },
    "MM": {
        "iso2": "MM",
        "countryName": "Myanmar",
        "countrySlug": "myanmar",
        "flag": "🇲🇲",
        "emergencyNumber": "192 (ambulance), 199 (police), 191 (fire)",
        "healthcareSystem": "Public healthcare system severely underfunded. Private clinics in Yangon and Mandalay offer better care. Medical evacuation to Thailand or Singapore recommended for serious conditions.",
        "healthcareSystemType": "mixed",
        "qualityRating": 1,
        "qualityNotes": "Healthcare is very limited, particularly since the 2021 political crisis. Private hospitals in Yangon offer the best available care. For serious conditions, medical evacuation to Bangkok is standard. Bring all medications you might need.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in cities open daily 8am-9pm. Very limited in rural areas.",
        "pharmacyTips": "AA Pharmacy and City Pharmacy are larger chains in Yangon. Many medications available OTC but quality can vary. Counterfeit medicines are a concern — buy from reputable pharmacies in cities only.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "oral rehydration salts",
            "anti-diarrheal medication",
            "antibiotics (widely available OTC)",
            "antimalarials",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Very relaxed prescription requirements. Most medications available without prescription. Quality and authenticity are concerns. Bring essential medications from home.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Myanmar has extremely strict drug laws. Bring documentation."
            },
            {
                "name": "Amphetamines/stimulants",
                "status": "banned",
                "note": "Extremely strict penalties including death penalty."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Strictly illegal. Severe penalties."
            }
        ],
        "bringDocumentation": "Carry a detailed doctor's letter in English for ALL prescription medications. Myanmar has extremely strict drug laws. Keep all medications in original packaging with clear labels.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation coverage is ABSOLUTELY ESSENTIAL. Must cover evacuation to Bangkok, Thailand or Singapore. Healthcare in Myanmar is severely limited."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Japanese Encephalitis",
                "Rabies (strongly recommended)",
                "Malaria prophylaxis (for many regions)",
                "Yellow fever (required if arriving from endemic area)"
            ],
            "notes": "Malaria is present in many regions. Dengue fever is common. Consult a travel medicine specialist well before departure."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do NOT drink tap water. Use bottled water only. Avoid ice in drinks except at upscale hotels. Use bottled water for brushing teeth.",
        "foodSafetyTips": "Eat freshly cooked food only. Avoid raw vegetables, salads, and unpeeled fruit. Street food should be very hot and freshly prepared. Mohinga (fish soup) and grilled dishes from busy stalls are safest.",
        "medicalTourismNote": "Myanmar is not a medical tourism destination. Travelers needing medical care typically evacuate to Thailand or Singapore.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Yangon",
            "WHO Myanmar",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Myanmar. Emergency numbers, pharmacy tips, limited hospital options, vaccination requirements, and essential medical evacuation insurance info.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Pun Hlaing Siloam Hospital",
                "nearTouristArea": "Hlaing Tharyar, Yangon",
                "phone": "+95 1 684 323",
                "englishSpeaking": True,
                "notes": "Best private hospital in Myanmar. International standards. English-speaking doctors."
            },
            {
                "name": "Asia Royal Hospital",
                "nearTouristArea": "Yangon (near Shwedagon Pagoda area)",
                "phone": "+95 1 538 055",
                "englishSpeaking": True,
                "notes": "Private hospital with English-speaking doctors. Good for tourist medical needs."
            },
            {
                "name": "Mandalay General Hospital",
                "nearTouristArea": "Mandalay",
                "phone": "+95 2 396 2100",
                "englishSpeaking": False,
                "notes": "Main public hospital in Mandalay. Basic facilities. For serious conditions, evacuation recommended."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "ခေါင်းကိုက်ဆေး လိုပါတယ်",
                "transliteration": "Khoun-gaike-hsay lo-ba-deh"
            },
            {
                "english": "I have a stomachache",
                "local": "ဗိုက်နာပါတယ်",
                "transliteration": "Baike-na-ba-deh"
            },
            {
                "english": "I'm allergic to...",
                "local": "ကျွန်တော်/ကျွန်မ ...ဓါတ်မတည့်ပါ",
                "transliteration": "Kya-naw/kya-ma ...dat-ma-teh-ba"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "အနီးဆုံးဆေးဆိုင် ဘယ်မှာလဲ",
                "transliteration": "A-ni-zone-hsay-saing beh-hma-leh?"
            },
            {
                "english": "I need a doctor",
                "local": "ဆရာဝန် လိုပါတယ်",
                "transliteration": "Hsaya-wun lo-ba-deh"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care available in Yangon. Very limited elsewhere.",
            "costRange": "$5-20 for consultation; $10-40 for fillings",
            "notes": "Dental facilities are basic. For anything beyond emergencies, consider evacuation to Bangkok.",
            "emergencyTip": "For dental emergencies in Yangon, visit Pun Hlaing Siloam Hospital or Asia Royal Hospital."
        },
        "mentalHealth": {
            "crisisLine": "No dedicated crisis line available",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some available through international clinics in Yangon.",
            "notes": "Mental health services are extremely limited in Myanmar. For English-speaking support, contact your embassy."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited throughout Myanmar. Most buildings and transport are not accessible.",
            "hospitalAccess": "Private hospitals in Yangon have some accessibility. Public hospitals have very limited accessibility.",
            "transport": "No accessible public transport. Private vehicles are the main option. Roads are often poor quality.",
            "tips": "Myanmar is very challenging for travelers with mobility limitations. Plan carefully, use private transport, and contact your hotel in advance. Major temples (Shwedagon) have some accessible routes."
        },
        "covidStatus": {
            "entryRequirements": "Check current requirements before travel as they may change. Some documentation may be required.",
            "maskPolicy": "Follow local guidance.",
            "testing": "Tests available at private hospitals in Yangon.",
            "notes": "Check latest travel advisories before visiting Myanmar."
        },
        "insuranceClaimProcess": "Private hospitals provide English-language documentation. Public hospitals provide basic receipts in Burmese. Medical evacuation to Thailand is common and expensive — ensure insurance covers this. Keep all documentation."
    },
    "MN": {
        "iso2": "MN",
        "countryName": "Mongolia",
        "countrySlug": "mongolia",
        "flag": "🇲🇳",
        "emergencyNumber": "103 (ambulance), 102 (police), 101 (fire)",
        "healthcareSystem": "Public healthcare system with growing private sector. Quality healthcare concentrated in Ulaanbaatar. Outside the capital, facilities are very basic.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Ulaanbaatar offer adequate care. Public hospitals are underfunded. For serious conditions, medical evacuation to Seoul or Beijing may be necessary. Healthcare in rural areas is very limited.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies (эмийн сан) open daily 9am-8pm in Ulaanbaatar. Very limited in rural areas.",
        "pharmacyTips": "Pharmacies in Ulaanbaatar are well-stocked. Monos, Intermed, and E-Mart pharmacies are reliable. English is limited — bring written medication names or a translation app. Bring all essential medications for trips outside Ulaanbaatar.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "cold remedies",
            "stomach medication",
            "antihistamines",
            "altitude sickness medication (useful for western Mongolia)",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Many medications available OTC. Controlled substances require a prescription. Foreign prescriptions not formally accepted.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Require documentation."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Bring documentation and original packaging."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Mongolia."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for controlled medications. Keep in original packaging. Bring sufficient quantities for your entire trip — medications are not reliably available outside Ulaanbaatar.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation coverage is ESSENTIAL, especially for travel outside Ulaanbaatar. Helicopter evacuation from remote areas can cost $10,000+. Ensure coverage for adventure activities (horse riding, hiking)."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (recommended due to stray dogs and rural travel)",
                "Tick-borne Encephalitis (for forested areas in northern Mongolia)"
            ],
            "notes": "No mandatory vaccinations. Plague cases occasionally reported in western Mongolia — avoid marmot contact. Ensure routine vaccinations are current."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do not drink tap water. Use bottled or boiled water. In the countryside, boil river/stream water. Bottled water available in Ulaanbaatar and larger towns.",
        "foodSafetyTips": "Mongolian cuisine is meat and dairy heavy. Buuz (dumplings) and khuushuur (fried pastries) are well-cooked and safe when fresh. Be cautious with airag (fermented mare's milk) if you have a sensitive stomach. In ger camps, food is freshly prepared.",
        "medicalTourismNote": "Mongolia is not a medical tourism destination. Travelers needing advanced care typically go to Seoul, Beijing, or Bangkok.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Ulaanbaatar",
            "Mongolian Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Mongolia. Emergency numbers (103/102/101), pharmacy tips, hospital info, and essential medical evacuation insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "SOS Medica Mongolia",
                "nearTouristArea": "Ulaanbaatar (near city center)",
                "phone": "+976 11 464 325",
                "englishSpeaking": True,
                "notes": "International clinic run by SOS International. Best option for foreigners. English-speaking doctors. Can arrange medical evacuation."
            },
            {
                "name": "Intermed Hospital",
                "nearTouristArea": "Ulaanbaatar",
                "phone": "+976 11 320 280",
                "englishSpeaking": True,
                "notes": "Modern private hospital. Good facilities by Mongolian standards."
            },
            {
                "name": "Songdo Hospital",
                "nearTouristArea": "Ulaanbaatar",
                "phone": "+976 11 310 945",
                "englishSpeaking": True,
                "notes": "Korean-Mongolian private hospital. Modern equipment. English and Korean speaking."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Надад толгой өвдөлтийн эм хэрэгтэй",
                "transliteration": "Nadad tolgoi uvdultin em kheregtei"
            },
            {
                "english": "I have a stomachache",
                "local": "Миний гэдэс өвдөж байна",
                "transliteration": "Minii gedes uvduj baina"
            },
            {
                "english": "I'm allergic to...",
                "local": "Надад ... харшил байна",
                "transliteration": "Nadad ... kharshil baina"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Хамгийн ойр эмийн сан хаана байна?",
                "transliteration": "Khamgiin oir emiin san khaana baina?"
            },
            {
                "english": "I need a doctor",
                "local": "Надад эмч хэрэгтэй",
                "transliteration": "Nadad emch kheregtei"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Ulaanbaatar. Limited elsewhere.",
            "costRange": "$15-40 for consultation; $20-80 for fillings; $20-60 for extractions",
            "notes": "Several modern dental clinics in Ulaanbaatar. Quality has improved in recent years.",
            "emergencyTip": "Visit SOS Medica Mongolia or Intermed Hospital for dental emergencies. Outside Ulaanbaatar, dental care is very limited."
        },
        "mentalHealth": {
            "crisisLine": "108 (Mongol Emergency Helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. SOS Medica Mongolia may provide referrals.",
            "notes": "Mental health services are very limited. For English-speaking support, contact SOS Medica or your embassy."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited, especially outside Ulaanbaatar. Ger camps and rural areas are not accessible.",
            "hospitalAccess": "Private hospitals in Ulaanbaatar have some accessibility. Public hospitals are limited.",
            "transport": "No accessible public transport. Private vehicles are the main option. Roads outside Ulaanbaatar are often unpaved tracks.",
            "tips": "Mongolia is very challenging for travelers with mobility limitations. Ger camp stays involve ground-level entry. Ulaanbaatar's newer buildings have better access. Discuss specific needs with tour operators well in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at hospitals in Ulaanbaatar.",
            "notes": "Mongolia has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "SOS Medica Mongolia can assist with insurance documentation in English. Private hospitals provide receipts. Keep all documentation. Medical evacuation costs should be documented thoroughly for insurance claims."
    },
    "MV": {
        "iso2": "MV",
        "countryName": "Maldives",
        "countrySlug": "maldives",
        "flag": "🇲🇻",
        "emergencyNumber": "102 (ambulance), 119 (police), 118 (fire)",
        "healthcareSystem": "Public healthcare centered on Malé. Resort islands have their own medical facilities (usually a resident doctor or nurse). Serious conditions require evacuation to Malé or Sri Lanka/India.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Healthcare in Malé is adequate for basic needs. Resort medical facilities vary — luxury resorts have well-equipped clinics while budget options have basic first aid. For serious conditions, medical evacuation to Sri Lanka, India, or Singapore is standard.",
        "pharmacyAccess": "limited",
        "pharmacyHours": "Pharmacies in Malé open 8am-10pm. Resort islands may have limited medication through the resort clinic. Limited pharmacies on local islands.",
        "pharmacyTips": "STO Pharmacy and ADK Hospital pharmacy in Malé are well-stocked. Resorts provide basic medications through their clinics. Bring ALL medications you might need — pharmacies on resort islands are nonexistent.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "anti-diarrheal medication",
            "oral rehydration salts",
            "seasickness medication",
            "sunscreen and after-sun care",
            "band-aids and coral cut treatment"
        ],
        "prescriptionRules": "Basic medications available OTC. Limited selection even with a prescription. Bring all essential medications from home.",
        "restrictedMeds": [
            {
                "name": "Alcohol-based medications",
                "status": "restricted",
                "note": "Alcohol is banned on local islands (permitted at resorts). Alcohol-based medicines require documentation."
            },
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Strictly controlled. Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Strictly illegal. Severe penalties."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Bring a doctor's letter and keep in original packaging."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for ALL prescription medications. Keep in original packaging. Maldivian customs may inspect medications — clear labeling is essential.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$35-65/week",
            "tips": "Travel insurance with medical evacuation by seaplane/speedboat is ESSENTIAL. Evacuation from remote atolls to Malé can be very expensive. Ensure coverage for water sports, diving, and snorkeling."
        },
        "vaccinations": {
            "required": [
                "Yellow fever (if arriving from an endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid"
            ],
            "notes": "Yellow fever certificate required if arriving from an endemic country. Dengue is present — use mosquito repellent."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water on local islands is desalinated and generally safe but often tastes poor. Resorts provide safe drinking water (often desalinated or bottled). Bottled water available everywhere. Do not drink tap water on local islands.",
        "foodSafetyTips": "Resort food follows international safety standards. On local islands, eat freshly cooked food. Fresh tuna and seafood are safe from reputable sources. Drink plenty of water to stay hydrated in the tropical heat.",
        "medicalTourismNote": "The Maldives is not a medical tourism destination. Some resorts offer wellness and spa treatments.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy (Sri Lanka, covering Maldives)",
            "Maldives Health Protection Agency",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Maldives. Emergency numbers, resort medical info, medication tips, and why evacuation insurance is essential.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "ADK Hospital",
                "nearTouristArea": "Malé (main island)",
                "phone": "+960 331 3553",
                "englishSpeaking": True,
                "notes": "Best private hospital in Maldives. 24/7 emergency. English spoken. Can arrange evacuations."
            },
            {
                "name": "Indira Gandhi Memorial Hospital (IGMH)",
                "nearTouristArea": "Malé",
                "phone": "+960 331 6647",
                "englishSpeaking": True,
                "notes": "Main public hospital. Emergency services 24/7. Located in central Malé."
            },
            {
                "name": "Tree Top Hospital",
                "nearTouristArea": "Hulhumalé (near Malé airport island)",
                "phone": "+960 331 0008",
                "englishSpeaking": True,
                "notes": "Modern hospital near the airport. Good for pre-departure medical needs."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "އަޅުގަނޑަށް ބޮލުގައި ރިއްސާ ބޭސް ބޭނުން",
                "transliteration": "Alhugandah bolugai rissa beys beynun"
            },
            {
                "english": "I have a stomachache",
                "local": "އަޅުގަނޑު ބަނޑުގައި ރިއްސަނީ",
                "transliteration": "Alhugandu bandugai rissanee"
            },
            {
                "english": "I'm allergic to...",
                "local": "އަޅުގަނޑަށް... އެލާޖީ ވޭ",
                "transliteration": "Alhugandah... allergy vey"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "އެންމެ ކައިރީގައި ހުރި ބޭސް ފިހާރަ ކޮބާ?",
                "transliteration": "Emme kaireega huri beys fihaara kobaa?"
            },
            {
                "english": "I need a doctor",
                "local": "އަޅުގަނޑަށް ޑޮކްޓަރެއް ބޭނުން",
                "transliteration": "Alhugandah doctarey beynun"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care in Malé. Not available on resort islands.",
            "costRange": "$20-50 for consultation; $30-100 for fillings",
            "notes": "ADK Hospital has a dental department. For significant dental work, consider Sri Lanka or Singapore.",
            "emergencyTip": "For dental emergencies on a resort, the resort doctor can provide pain management. Transfer to Malé may be needed."
        },
        "mentalHealth": {
            "crisisLine": "1412 (Family and Child Protection hotline)",
            "internationalLine": "Contact your resort or embassy for referrals",
            "englishTherapists": "Very limited. Some available through ADK Hospital.",
            "notes": "Mental health services are very limited. Resorts may have wellness staff who can help with basic support. For serious concerns, contact your embassy."
        },
        "accessibilityInfo": {
            "overview": "Accessibility varies greatly. Luxury resorts often have accessible options. Local islands and budget guesthouses have very limited accessibility.",
            "hospitalAccess": "ADK Hospital and IGMH have basic wheelchair access.",
            "transport": "Seaplanes and speedboats are not wheelchair accessible. Airport transfers may be arranged with advance notice. Some resorts have buggy transport.",
            "tips": "Contact resorts directly about accessibility — many luxury resorts can accommodate wheelchair users with advance notice. Water villas have specific access challenges. Beach villas are generally more accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask requirements.",
            "testing": "Tests available at hospitals in Malé.",
            "notes": "Maldives has lifted all COVID restrictions."
        },
        "insuranceClaimProcess": "ADK Hospital provides English documentation. Resort medical clinics provide basic receipts. Medical evacuation costs can be very high — keep all documentation. Ensure your insurer is notified of any evacuation in advance if possible."
    },
    "BD": {
        "iso2": "BD",
        "countryName": "Bangladesh",
        "countrySlug": "bangladesh",
        "flag": "🇧🇩",
        "emergencyNumber": "999 (national emergency), 199 (ambulance)",
        "healthcareSystem": "Public healthcare system supplemented by growing private sector. Private hospitals in Dhaka offer adequate care. Public hospitals are overcrowded and under-resourced.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Dhaka (Square, United, Apollo) offer reasonable care. Public hospitals are severely overcrowded. English spoken at major private hospitals. For serious conditions, medical evacuation to Bangkok, Singapore, or India is common.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open daily 8am-10pm in cities. Many 24/7 pharmacies in Dhaka.",
        "pharmacyTips": "Lazz Pharma and other pharmacy chains are widespread. Most medications available without prescription at very low prices. Pharmacists may have limited training — self-prescribing is common. Bring your own essential medications to ensure quality.",
        "commonOTC": [
            "paracetamol (Napa, Ace)",
            "ibuprofen",
            "oral rehydration salts (ORSaline — critical for traveler's diarrhea)",
            "anti-diarrheal medication",
            "antibiotics (widely available OTC)",
            "antihistamines",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Very few prescription requirements in practice. Almost all medications available OTC. Bring essential medications from home for quality assurance.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Strictly illegal in Bangladesh. Severe penalties."
            },
            {
                "name": "Sleeping pills / sedatives",
                "status": "controlled",
                "note": "Bring a doctor's letter."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for all prescription medications. Keep in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-40/week",
            "tips": "Travel insurance with medical evacuation coverage is ESSENTIAL. Ensure coverage for evacuation to Bangkok, India, or Singapore for serious conditions."
        },
        "vaccinations": {
            "required": [
                "Yellow fever (if arriving from an endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies",
                "Japanese Encephalitis",
                "Cholera (oral vaccine for high-risk areas)"
            ],
            "notes": "Yellow fever certificate required from endemic countries. Cholera and traveler's diarrhea are significant risks. Malaria risk in some border areas — consult a travel doctor."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do NOT drink tap water. Use bottled water only. Avoid ice in drinks. Use bottled water for brushing teeth. Arsenic contamination affects some groundwater sources in rural areas.",
        "foodSafetyTips": "Eat freshly cooked, hot food only. Avoid raw vegetables, salads, and unpeeled fruit. Street food should be piping hot. Biryani and curries from busy restaurants are generally safe. Avoid buffets that have been sitting.",
        "medicalTourismNote": "Bangladesh is not a medical tourism destination. Many Bangladeshis travel to India, Thailand, or Singapore for advanced medical care.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Dhaka",
            "Bangladesh Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Bangladesh. Emergency number 999, pharmacy tips, hospital info, vaccination requirements, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Square Hospital",
                "nearTouristArea": "Panthapath, Dhaka",
                "phone": "+880 2 8142 141",
                "englishSpeaking": True,
                "notes": "Leading private hospital. Modern facilities. English-speaking doctors. 24/7 emergency."
            },
            {
                "name": "United Hospital",
                "nearTouristArea": "Gulshan, Dhaka (diplomatic/expat area)",
                "phone": "+880 2 8836 000",
                "englishSpeaking": True,
                "notes": "Modern private hospital in expat area. Good for tourist medical needs."
            },
            {
                "name": "Apollo Hospital Dhaka",
                "nearTouristArea": "Bashundhara, Dhaka",
                "phone": "+880 2 8431 661",
                "englishSpeaking": True,
                "notes": "Part of Apollo international chain. International patient services."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "আমার মাথা ব্যথার ওষুধ দরকার",
                "transliteration": "Amar matha byathar oshudh dorkar"
            },
            {
                "english": "I have a stomachache",
                "local": "আমার পেট ব্যথা করছে",
                "transliteration": "Amar pet byatha korche"
            },
            {
                "english": "I'm allergic to...",
                "local": "আমার ...এ এলার্জি আছে",
                "transliteration": "Amar...e allergy achhe"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "নিকটতম ফার্মেসি কোথায়?",
                "transliteration": "Nikottomo pharmacy kothay?"
            },
            {
                "english": "I need a doctor",
                "local": "আমার ডাক্তার দরকার",
                "transliteration": "Amar daktar dorkar"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Dhaka at private clinics. Quality varies.",
            "costRange": "$5-20 for consultation; $10-40 for fillings",
            "notes": "Private dental clinics in Dhaka's Gulshan and Banani areas serve international patients. Basic care is affordable.",
            "emergencyTip": "Square Hospital and United Hospital have dental departments for emergencies."
        },
        "mentalHealth": {
            "crisisLine": "16789 (Kaan Pete Roi — emotional support helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Limited. Some available through private hospitals in Dhaka.",
            "notes": "Mental health services are limited. English-speaking support mainly available through private hospitals and expatriate networks."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited in Bangladesh. Sidewalks, buildings, and transport are generally not accessible.",
            "hospitalAccess": "Major private hospitals have some accessibility. Public hospitals have very limited access.",
            "transport": "No accessible public transport. Rickshaws and private cars are the main options. Traffic congestion in Dhaka is extreme.",
            "tips": "Bangladesh is very challenging for travelers with mobility limitations. Plan all logistics carefully. Use private transport and contact hotels/tour operators in advance about specific needs."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No formal requirements but masks may be recommended in crowded areas.",
            "testing": "Tests available at private hospitals and clinics in Dhaka.",
            "notes": "Bangladesh has lifted most COVID restrictions."
        },
        "insuranceClaimProcess": "Private hospitals provide English-language documentation and receipts. Keep all records. Medical evacuation to India or Thailand is common — ensure your insurer is notified promptly. File claims within 30 days."
    },
    "PK": {
        "iso2": "PK",
        "countryName": "Pakistan",
        "countrySlug": "pakistan",
        "flag": "🇵🇰",
        "emergencyNumber": "1122 (Rescue, in Punjab & some provinces), 115 (Edhi ambulance nationwide)",
        "healthcareSystem": "Mixed public-private system. Public healthcare is underfunded. Private hospitals in major cities offer reasonable care. Quality varies greatly by region.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Lahore, Islamabad, and Karachi offer adequate care. Public hospitals are overcrowded. Many Pakistani doctors train abroad and speak English. For serious conditions, medical evacuation to Dubai, Singapore, or Thailand may be necessary.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open daily 9am-10pm in cities. Many 24/7 pharmacies in major cities.",
        "pharmacyTips": "Pharmacies (dawakhana/medical store) are everywhere. D. Watson's, Fazal Din's, and Shaheen Chemist are reputable chains. Most medications available without prescription at very low prices. Bring essential medications from home to ensure quality.",
        "commonOTC": [
            "paracetamol (Panadol — ubiquitous)",
            "ibuprofen (Brufen)",
            "oral rehydration salts",
            "anti-diarrheal medication (Imodium)",
            "antibiotics (widely available OTC)",
            "antihistamines",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Very relaxed prescription requirements. Most medications available OTC. Some controlled substances may require a prescription in practice. Bring quality medications from home.",
        "restrictedMeds": [
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Bring documentation."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Cannabis is illegal in Pakistan. Severe penalties."
            },
            {
                "name": "Alcohol-based medications",
                "status": "restricted",
                "note": "Pakistan is an Islamic republic — bring documentation for alcohol-containing medicines."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English for all prescription medications, especially controlled substances and alcohol-containing medicines. Keep in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation coverage is ESSENTIAL, especially for northern areas (Hunza, Gilgit-Baltistan). Ensure coverage for adventure activities (trekking, mountaineering) and helicopter evacuation."
        },
        "vaccinations": {
            "required": [
                "Polio (some travelers may need to show proof)",
                "Yellow fever (if arriving from an endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies",
                "Malaria prophylaxis (for certain regions)"
            ],
            "notes": "Pakistan is one of the last countries with endemic polio — ensure your polio vaccination is current. Dengue is present in urban areas. Malaria risk in some regions."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Do NOT drink tap water. Use bottled water only. Avoid ice in drinks. Use bottled water for brushing teeth. Nestle Pure Life and other sealed bottled water brands are widely available.",
        "foodSafetyTips": "Eat freshly cooked, hot food. Pakistani cuisine is flavorful — stick to busy restaurants. Avoid raw vegetables and salads. Street food biryani and kebabs are generally safe when freshly cooked. Lassi from busy shops is usually fine.",
        "medicalTourismNote": "Pakistan is not typically a medical tourism destination, though some Pakistani diaspora return for affordable dental and cosmetic procedures.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Islamabad",
            "Pakistan Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Pakistan. Emergency numbers (1122/115), pharmacy tips, hospital info, vaccination requirements, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Shifa International Hospital",
                "nearTouristArea": "Islamabad (H-8 sector, near Faisal Mosque area)",
                "phone": "+92 51 846 4646",
                "englishSpeaking": True,
                "notes": "Leading private hospital. JCI accredited. English-speaking staff. 24/7 emergency."
            },
            {
                "name": "Aga Khan University Hospital",
                "nearTouristArea": "Karachi (Stadium Road)",
                "phone": "+92 21 111 911 911",
                "englishSpeaking": True,
                "notes": "Pakistan's top-ranked hospital. International standards. Excellent English service."
            },
            {
                "name": "Doctors Hospital Lahore",
                "nearTouristArea": "Lahore (Johar Town, accessible from Mughal-era sites)",
                "phone": "+92 42 111 626 262",
                "englishSpeaking": True,
                "notes": "Modern private hospital. Good emergency department. English-speaking doctors."
            },
            {
                "name": "Combined Military Hospital (CMH) Gilgit",
                "nearTouristArea": "Gilgit (Karakoram Highway/Hunza region)",
                "phone": "+92 5811 920 426",
                "englishSpeaking": True,
                "notes": "Best hospital in the northern areas. Military hospital open to civilians for emergencies. Critical for Karakoram/Hunza trekking injuries."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "مجھے سر درد کی دوائی چاہیے",
                "transliteration": "Mujhe sar-dard ki dawai chahiye"
            },
            {
                "english": "I have a stomachache",
                "local": "میرے پیٹ میں درد ہے",
                "transliteration": "Mere pait mein dard hai"
            },
            {
                "english": "I'm allergic to...",
                "local": "مجھے...سے الرجی ہے",
                "transliteration": "Mujhe...se allergy hai"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "قریب ترین میڈیکل سٹور کہاں ہے؟",
                "transliteration": "Qareeb tareen medical store kahan hai?"
            },
            {
                "english": "I need a doctor",
                "local": "مجھے ڈاکٹر کی ضرورت ہے",
                "transliteration": "Mujhe doctor ki zaroorat hai"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in major cities. Private dental clinics in Islamabad, Lahore, and Karachi offer good care.",
            "costRange": "PKR 1,000-3,000 ($3-10) for consultation; PKR 3,000-10,000 ($10-35) for fillings",
            "notes": "Very affordable dental care in cities. Quality varies — choose established clinics with qualified dentists.",
            "emergencyTip": "Major private hospitals have dental departments for emergencies."
        },
        "mentalHealth": {
            "crisisLine": "0311 7786264 (Umang Mental Health Helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Islamabad, Lahore, and Karachi through private practice. Expect PKR 3,000-8,000 ($10-28) per session.",
            "notes": "Mental health services are limited but growing. English-speaking therapists available in major cities. Online therapy platforms serve English speakers."
        },
        "accessibilityInfo": {
            "overview": "Accessibility infrastructure is very limited. Most buildings, roads, and transport are not wheelchair accessible.",
            "hospitalAccess": "Major private hospitals have basic accessibility. Public hospitals have very limited access.",
            "transport": "No accessible public transport. Private vehicles are the main option. Roads can be challenging.",
            "tips": "Pakistan is very challenging for travelers with mobility limitations. Northern mountain areas are particularly difficult. Plan all logistics with a reliable tour operator. Contact hotels in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No formal requirements.",
            "testing": "Tests available at private hospitals and clinics.",
            "notes": "Pakistan has lifted most COVID restrictions."
        },
        "insuranceClaimProcess": "Private hospitals provide English-language documentation and receipts. Military hospitals provide basic documentation. Keep all records. Medical evacuation from northern areas can be very expensive — ensure insurance is notified promptly."
    }
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for iso2, data in COUNTRIES.items():
        filepath = os.path.join(OUTPUT_DIR, f"{iso2}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Written: {filepath}")

    print(f"\nDone! Generated {len(COUNTRIES)} health data files.")


if __name__ == "__main__":
    main()
