#!/usr/bin/env python3
"""
Generate health data JSON files for 25 new countries (Batch 2).
Countries: SA, OM, QA, KW, LB, IR, NG, GH, ET, RW, UG, SN,
           CL, EC, DO, JM, PA, GT, BO, UY, PY, HN, SV, FJ, NI
"""

import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "health-data")

COUNTRIES = {
    "SA": {
        "iso2": "SA",
        "countryName": "Saudi Arabia",
        "countrySlug": "saudi-arabia",
        "flag": "\U0001f1f8\U0001f1e6",
        "emergencyNumber": "911 (ambulance, fire, police — unified in Riyadh & Jeddah), 997 (ambulance), 999 (police), 998 (fire)",
        "healthcareSystem": "Government-funded for citizens; tourists must use private healthcare or have insurance. Modern hospitals in major cities.",
        "healthcareSystemType": "mixed",
        "qualityRating": 4,
        "qualityNotes": "Excellent private hospitals in Riyadh, Jeddah, and Makkah with modern equipment and English-speaking staff. Public hospitals are available but prioritize citizens. Rural healthcare is more limited.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies open 9am-12am; many 24/7 in major cities. Closed during prayer times (5 short breaks daily).",
        "pharmacyTips": "Pharmacies are well-stocked and modern. Pharmacists often speak English. Be aware that pharmacies close during prayer times (approximately 20-30 minutes, 5 times daily). Many medications that are OTC elsewhere are controlled in Saudi Arabia.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cough syrup (non-codeine)",
            "oral rehydration salts"
        ],
        "prescriptionRules": "Saudi Arabia has extremely strict drug control laws. Many common medications from other countries are banned or require special permits. All controlled medications require a prescription from a Saudi doctor or pre-approved foreign prescription.",
        "restrictedMeds": [
            {
                "name": "Amphetamines (Adderall, Vyvanse, Dexedrine)",
                "status": "banned",
                "note": "Strictly prohibited. Possession can result in severe criminal penalties including imprisonment. There is zero tolerance."
            },
            {
                "name": "Codeine-containing medications",
                "status": "banned",
                "note": "All codeine products are prohibited. This includes many common cold and pain medications."
            },
            {
                "name": "Tramadol",
                "status": "banned",
                "note": "Classified as a narcotic. Strictly prohibited even with foreign prescription."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Zero tolerance. Possession carries severe penalties including imprisonment and potential corporal punishment."
            },
            {
                "name": "Benzodiazepines (Xanax, Valium, etc.)",
                "status": "restricted",
                "note": "Requires prior approval from Saudi Food & Drug Authority (SFDA). Must carry doctor's letter and original prescription."
            },
            {
                "name": "Psychotropic medications",
                "status": "restricted",
                "note": "Antidepressants and antipsychotics require documentation. Apply for approval from SFDA before travel."
            }
        ],
        "bringDocumentation": "CRITICAL: Saudi Arabia has among the strictest drug laws in the world. Apply for medication approval from the Saudi Food & Drug Authority (SFDA) BEFORE travel. Carry a doctor's letter in English and Arabic listing all medications with generic names. Keep all medications in original packaging. Bring no more than a 30-day supply. Violations can result in imprisonment.",
        "travelInsurance": {
            "recommended": True,
            "required": True,
            "requiredNote": "Health insurance is mandatory for all tourist visa holders. Proof of insurance required for visa application.",
            "averageCost": "$40-80/week",
            "tips": "Private healthcare is expensive — a basic ER visit can cost $300+. Ensure coverage includes medical evacuation and repatriation. Hajj/Umrah pilgrims should get specialized pilgrim insurance covering heat-related illness."
        },
        "vaccinations": {
            "required": [
                "Meningococcal ACWY (required for Hajj/Umrah pilgrims)",
                "Yellow Fever (if arriving from endemic area)",
                "Polio booster (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Routine vaccinations (MMR, DTaP)"
            ],
            "notes": "Meningococcal vaccination is mandatory for Hajj and Umrah pilgrims — must be administered no more than 3 years and no less than 10 days before arrival. Seasonal flu vaccination recommended for pilgrims."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is desalinated and safe to drink in major cities, though most residents and visitors prefer bottled water for taste. Bottled water is inexpensive and ubiquitous.",
        "foodSafetyTips": "Food safety standards are generally high in restaurants and hotels. Be cautious with street food during extreme summer heat. During Hajj/Umrah, eat at established vendors. Stay well-hydrated — summer temperatures regularly exceed 45\u00b0C (113\u00b0F).",
        "medicalTourismNote": "Saudi Arabia is investing heavily in medical tourism as part of Vision 2030. King Faisal Specialist Hospital in Riyadh is world-renowned for oncology and organ transplantation.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Riyadh",
            "Saudi Food & Drug Authority (SFDA)",
            "Saudi Ministry of Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Saudi Arabia. Strict drug laws, banned medications (codeine, Adderall), mandatory insurance, Hajj/Umrah vaccination requirements, and emergency numbers.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "King Faisal Specialist Hospital & Research Centre",
                "nearTouristArea": "Riyadh (Al Maather area)",
                "phone": "+966-11-464-7272",
                "englishSpeaking": True,
                "notes": "World-class specialist hospital. International patient department. Major credit cards accepted."
            },
            {
                "name": "Dr. Sulaiman Al Habib Hospital",
                "nearTouristArea": "Riyadh (Olaya district, near Kingdom Tower)",
                "phone": "+966-11-525-9999",
                "englishSpeaking": True,
                "notes": "Leading private hospital chain. Modern facilities. Multiple locations across the city."
            },
            {
                "name": "International Medical Center (IMC)",
                "nearTouristArea": "Jeddah (near Corniche)",
                "phone": "+966-12-650-9000",
                "englishSpeaking": True,
                "notes": "Premier private hospital in Jeddah. Convenient for Umrah travelers."
            },
            {
                "name": "Saudi German Hospital Jeddah",
                "nearTouristArea": "Jeddah (Al-Salamah district)",
                "phone": "+966-12-683-1000",
                "englishSpeaking": True,
                "notes": "Modern private hospital with emergency department. Multilingual staff."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0623\u062d\u062a\u0627\u062c \u062f\u0648\u0627\u0621 \u0644\u0644\u0635\u062f\u0627\u0639",
                "transliteration": "Ahtaaj dawaa' lil-sudaa'"
            },
            {
                "english": "I need a doctor",
                "local": "\u0623\u062d\u062a\u0627\u062c \u0637\u0628\u064a\u0628",
                "transliteration": "Ahtaaj tabeeb"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0623\u064a\u0646 \u0623\u0642\u0631\u0628 \u0635\u064a\u062f\u0644\u064a\u0629\u061f",
                "transliteration": "Ayn aqrab saidaliyya?"
            },
            {
                "english": "I'm allergic to this medicine",
                "local": "\u0639\u0646\u062f\u064a \u062d\u0633\u0627\u0633\u064a\u0629 \u0645\u0646 \u0647\u0630\u0627 \u0627\u0644\u062f\u0648\u0627\u0621",
                "transliteration": "Indi hasaasiyya min hadha al-dawaa'"
            },
            {
                "english": "I have a stomachache",
                "local": "\u0639\u0646\u062f\u064a \u0623\u0644\u0645 \u0641\u064a \u0627\u0644\u0645\u0639\u062f\u0629",
                "transliteration": "Indi alam fil-ma'ida"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care in Riyadh and Jeddah with modern clinics and internationally trained dentists.",
            "costRange": "SAR 200-500 ($53-133) for consultation; SAR 500-2,000 ($133-533) for fillings or extractions",
            "notes": "Many dental clinics in major cities cater to international patients. Quality is high in private clinics.",
            "emergencyTip": "Hospital emergency departments handle dental emergencies. Many private dental clinics open evenings and weekends. During Hajj season, medical tents in Mina and Arafat provide emergency dental care."
        },
        "mentalHealth": {
            "crisisLine": "920033360 (Ministry of Health mental health helpline)",
            "internationalLine": "Not widely available — contact your embassy for referrals",
            "englishTherapists": "Available in private hospitals in Riyadh and Jeddah. English widely spoken in healthcare settings.",
            "notes": "Mental health services are expanding in Saudi Arabia. Private hospitals offer psychiatric services. Cultural sensitivity around mental health topics — services are confidential."
        },
        "accessibilityInfo": {
            "overview": "Saudi Arabia is improving accessibility as part of Vision 2030. Newer buildings and malls are wheelchair accessible. Holy sites have dedicated accessible areas.",
            "hospitalAccess": "Major private hospitals are fully accessible with elevators and wheelchair ramps.",
            "transport": "Riyadh Metro (opening soon) designed to be fully accessible. Ride-hailing apps (Uber/Careem) available. Airport assistance available.",
            "tips": "The Grand Mosque in Makkah has wheelchair access and electric wheelchair services. Request accessible accommodations well in advance during Hajj/Umrah season."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "No mask mandates. Masks optional in healthcare settings.",
            "testing": "Available at hospitals and some pharmacies.",
            "notes": "Heat-related illness (heatstroke, dehydration) is a far more common health concern, especially during summer months and for Hajj/Umrah pilgrims."
        },
        "insuranceClaimProcess": "Private hospitals typically require insurance authorization or upfront payment. Keep all receipts and request English-language medical reports. Many hospitals can process insurance claims directly. File claims within 30 days of treatment."
    },
    "OM": {
        "iso2": "OM",
        "countryName": "Oman",
        "countrySlug": "oman",
        "flag": "\U0001f1f4\U0001f1f2",
        "emergencyNumber": "9999 (unified emergency — ambulance, police, fire)",
        "healthcareSystem": "Government healthcare free for citizens; tourists use private hospitals or pay at public facilities. Quality care in Muscat.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Good quality healthcare in Muscat with modern private hospitals. Public hospitals adequate but can be crowded. Very limited healthcare outside Muscat and Salalah — remote desert and mountain areas have minimal facilities.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Most pharmacies open 8am-10pm. Limited 24/7 options outside Muscat. Pharmacies close during Friday prayer.",
        "pharmacyTips": "Pharmacies in Muscat are well-stocked. Pharmacists generally speak English. Outside Muscat, pharmacy availability is limited. Stock up on medications before desert excursions or trips to remote areas.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "oral rehydration salts",
            "sunscreen"
        ],
        "prescriptionRules": "Prescription required for most medications. Oman has strict drug control laws similar to other Gulf states. Foreign prescriptions generally not accepted — need Omani doctor's prescription.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "banned",
                "note": "All codeine products are prohibited in Oman."
            },
            {
                "name": "Tramadol",
                "status": "banned",
                "note": "Strictly prohibited. Classified as narcotic."
            },
            {
                "name": "Amphetamines (Adderall, Vyvanse)",
                "status": "banned",
                "note": "Strictly prohibited. Severe criminal penalties for possession."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Zero tolerance. Severe penalties including imprisonment."
            },
            {
                "name": "Psychotropic medications",
                "status": "restricted",
                "note": "Requires documentation from prescribing physician and approval from Omani authorities."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English listing all medications with generic names. Keep medications in original packaging. For controlled substances, obtain prior approval from the Oman Ministry of Health. Bring no more than 3 months' supply.",
        "travelInsurance": {
            "recommended": True,
            "required": True,
            "requiredNote": "Health insurance is required for tourist visa applications.",
            "averageCost": "$35-65/week",
            "tips": "Medical evacuation coverage is essential, especially for adventure travel (desert camping, mountain hiking, diving). The nearest world-class medical facilities are in Muscat or Dubai."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Routine vaccinations"
            ],
            "notes": "No special vaccinations required for most travelers. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is desalinated and safe in cities. Bottled water recommended in rural areas and for taste. Stay extremely hydrated — Oman is one of the hottest countries on Earth.",
        "foodSafetyTips": "Food safety is generally good in hotels and restaurants. Be cautious with street food in summer heat. Fresh seafood is excellent in coastal areas. Stay well-hydrated during desert excursions.",
        "medicalTourismNote": "Oman is not a major medical tourism destination. For specialized treatment, patients typically travel to Dubai or India.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Oman",
            "Oman Ministry of Health",
            "WHO International Travel and Health"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Oman. Emergency number 9999, strict drug laws, pharmacy tips, vaccination requirements, desert safety advice, and travel insurance information.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Royal Hospital",
                "nearTouristArea": "Muscat (Al Ghubra)",
                "phone": "+968-2459-9000",
                "englishSpeaking": True,
                "notes": "Oman's largest government hospital. Emergency department. English widely spoken."
            },
            {
                "name": "Muscat Private Hospital",
                "nearTouristArea": "Muscat (Bausher, near Al Qurum)",
                "phone": "+968-2458-3600",
                "englishSpeaking": True,
                "notes": "Leading private hospital. International patient services. Near tourist beach areas."
            },
            {
                "name": "Starcare Hospital",
                "nearTouristArea": "Muscat (Al Khuwair, near Muscat Grand Mall)",
                "phone": "+968-2455-0600",
                "englishSpeaking": True,
                "notes": "Modern multi-specialty hospital. Convenient location near hotels."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0623\u062d\u062a\u0627\u062c \u062f\u0648\u0627\u0621 \u0644\u0644\u0635\u062f\u0627\u0639",
                "transliteration": "Ahtaaj dawaa' lil-sudaa'"
            },
            {
                "english": "I need a doctor",
                "local": "\u0623\u062d\u062a\u0627\u062c \u0637\u0628\u064a\u0628",
                "transliteration": "Ahtaaj tabeeb"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0623\u064a\u0646 \u0623\u0642\u0631\u0628 \u0635\u064a\u062f\u0644\u064a\u0629\u061f",
                "transliteration": "Ayn aqrab saidaliyya?"
            },
            {
                "english": "I have a fever",
                "local": "\u0639\u0646\u062f\u064a \u062d\u0631\u0627\u0631\u0629",
                "transliteration": "Indi haraara"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care available in Muscat. Limited outside the capital.",
            "costRange": "OMR 15-40 ($39-104) for consultation; OMR 30-100 ($78-260) for fillings",
            "notes": "Private dental clinics in Muscat have modern equipment. Many dentists trained in India, UK, or Egypt.",
            "emergencyTip": "Hospital emergency departments handle urgent dental issues. Book private dental appointments in advance."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact Royal Hospital psychiatric department",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Limited but available in Muscat through private clinics and hospitals.",
            "notes": "Mental health services are developing in Oman. Private hospitals in Muscat offer psychiatric consultations. Cultural sensitivity around mental health is important."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving in newer buildings and hotels but remains limited overall, especially in historic areas and desert terrain.",
            "hospitalAccess": "Major hospitals in Muscat are wheelchair accessible.",
            "transport": "Limited accessible public transport. Taxis and ride-hailing apps available. Airport assistance provided.",
            "tips": "Desert excursions, wadis, and mountain hiking are generally not wheelchair accessible. Newer hotels and malls are accessible. Request ground-floor rooms."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics in Muscat.",
            "notes": "Heat-related illness is the primary health concern. Summer temperatures can exceed 50\u00b0C (122\u00b0F)."
        },
        "insuranceClaimProcess": "Private hospitals may require upfront payment or insurance guarantee. Keep all receipts and medical documentation. Most private hospitals provide English-language reports. File claims with your insurer promptly."
    },
    "QA": {
        "iso2": "QA",
        "countryName": "Qatar",
        "countrySlug": "qatar",
        "flag": "\U0001f1f6\U0001f1e6",
        "emergencyNumber": "999 (ambulance), 999 (police), 999 (fire)",
        "healthcareSystem": "Government-funded for citizens; expatriates and tourists use the Hamad Medical Corporation (public) or private facilities. High-quality modern healthcare.",
        "healthcareSystemType": "mixed",
        "qualityRating": 4,
        "qualityNotes": "Excellent modern healthcare. Hamad Medical Corporation is the main public provider with JCI-accredited hospitals. Sidra Medicine is world-class. English is widely spoken in medical settings.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies open 8am-11pm. Hospital pharmacies open 24/7. Pharmacies close during Friday prayer.",
        "pharmacyTips": "Pharmacies are modern and well-stocked. Pharmacists speak English and Arabic. Qatar has very strict drug laws — verify your medications are legal before bringing them.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cough medicine (non-codeine)",
            "oral rehydration salts"
        ],
        "prescriptionRules": "Qatar has among the strictest drug control laws in the world. Many medications that are OTC or legal elsewhere are banned or controlled. All controlled medications require approval from Qatar's Ministry of Public Health before entry.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "banned",
                "note": "All codeine products prohibited. Includes many common cold and pain medications."
            },
            {
                "name": "Tramadol",
                "status": "banned",
                "note": "Strictly prohibited. Classified as narcotic."
            },
            {
                "name": "Amphetamines (Adderall, Vyvanse, Ritalin)",
                "status": "banned",
                "note": "Strictly prohibited even with foreign prescription. Can result in imprisonment."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Zero tolerance. Even trace amounts can lead to severe criminal penalties."
            },
            {
                "name": "Sleeping pills and benzodiazepines",
                "status": "restricted",
                "note": "Requires advance approval from Ministry of Public Health. Carry doctor's letter."
            }
        ],
        "bringDocumentation": "CRITICAL: Apply for medication import approval from Qatar's Ministry of Public Health BEFORE traveling. Carry a doctor's letter in English listing all medications with generic names and dosages. Keep medications in original packaging with pharmacy labels. Qatar enforces drug laws strictly — violations result in imprisonment.",
        "travelInsurance": {
            "recommended": True,
            "required": True,
            "requiredNote": "Health insurance is mandatory for all visitors. Required for visa/entry permit.",
            "averageCost": "$45-85/week",
            "tips": "Healthcare in Qatar is expensive for non-residents. An ER visit can cost $500+. Ensure coverage includes medical evacuation. Hamad Medical Corporation provides emergency care to all patients regardless of insurance."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations for most travelers. Ensure routine vaccinations are up to date."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is desalinated and technically safe, though bottled water is preferred by most residents. Bottled water is cheap and readily available.",
        "foodSafetyTips": "High food safety standards in restaurants and hotels. The Souq Waqif area has excellent food stalls with good hygiene. Stay hydrated — summer heat is extreme.",
        "medicalTourismNote": "Qatar is developing as a medical tourism hub. Sidra Medicine is a state-of-the-art hospital specializing in women's and children's care. Hamad Medical Corporation provides advanced cardiac and trauma care.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Doha",
            "Qatar Ministry of Public Health",
            "Hamad Medical Corporation"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Qatar. Strict drug laws, banned medications (codeine, Adderall), mandatory insurance, emergency number 999, pharmacy tips, and hospital information.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hamad General Hospital",
                "nearTouristArea": "Doha (near Souq Waqif / Corniche)",
                "phone": "+974-4439-4444",
                "englishSpeaking": True,
                "notes": "Main public hospital. JCI-accredited. 24/7 emergency. Treats all patients including tourists."
            },
            {
                "name": "Sidra Medicine",
                "nearTouristArea": "Doha (Education City / Al Luqta area)",
                "phone": "+974-4003-3000",
                "englishSpeaking": True,
                "notes": "State-of-the-art hospital. Specializes in women's and children's health. World-class facilities."
            },
            {
                "name": "Al Ahli Hospital",
                "nearTouristArea": "Doha (near The Pearl-Qatar)",
                "phone": "+974-4489-8888",
                "englishSpeaking": True,
                "notes": "Modern private hospital. Convenient for Pearl and Katara Cultural Village visitors."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0623\u062d\u062a\u0627\u062c \u062f\u0648\u0627\u0621 \u0644\u0644\u0635\u062f\u0627\u0639",
                "transliteration": "Ahtaaj dawaa' lil-sudaa'"
            },
            {
                "english": "I need a doctor",
                "local": "\u0623\u062d\u062a\u0627\u062c \u0637\u0628\u064a\u0628",
                "transliteration": "Ahtaaj tabeeb"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0623\u064a\u0646 \u0623\u0642\u0631\u0628 \u0635\u064a\u062f\u0644\u064a\u0629\u061f",
                "transliteration": "Ayn aqrab saidaliyya?"
            },
            {
                "english": "I have diarrhea",
                "local": "\u0639\u0646\u062f\u064a \u0625\u0633\u0647\u0627\u0644",
                "transliteration": "Indi is-haal"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care in Doha with modern clinics.",
            "costRange": "QAR 200-500 ($55-137) for consultation; QAR 500-1,500 ($137-412) for fillings",
            "notes": "High-quality dental care available. Many internationally trained dentists.",
            "emergencyTip": "Hamad Dental Centre provides emergency dental services. Private clinics available on evenings and weekends."
        },
        "mentalHealth": {
            "crisisLine": "16000 (Qatar mental health helpline)",
            "internationalLine": "Contact your embassy for English-speaking referrals",
            "englishTherapists": "Available at private clinics and hospitals in Doha. English is widely used in healthcare.",
            "notes": "Mental health services available through Hamad Medical Corporation and private clinics. Confidential services available."
        },
        "accessibilityInfo": {
            "overview": "Qatar invested heavily in accessibility for the 2022 FIFA World Cup. Doha Metro is fully accessible. Modern infrastructure throughout.",
            "hospitalAccess": "All major hospitals are fully wheelchair accessible.",
            "transport": "Doha Metro is fully accessible with elevators and ramps. Accessible taxis available through Karwa. Most modern attractions are accessible.",
            "tips": "Souq Waqif has uneven surfaces in some areas. Modern malls, museums (Museum of Islamic Art, National Museum), and hotels are fully accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Heat-related illness is the primary health concern during summer."
        },
        "insuranceClaimProcess": "Hamad Medical Corporation provides emergency care and bills later. Private hospitals may require upfront payment. Keep all receipts. English medical documentation is standard. File claims with your insurer within 30 days."
    },
    "KW": {
        "iso2": "KW",
        "countryName": "Kuwait",
        "countrySlug": "kuwait",
        "flag": "\U0001f1f0\U0001f1fc",
        "emergencyNumber": "112 (unified emergency — ambulance, police, fire)",
        "healthcareSystem": "Government healthcare for citizens; tourists and expatriates use private hospitals. Good-quality facilities in Kuwait City.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Good healthcare in Kuwait City with modern private hospitals. Public hospitals are available but can be overcrowded. English is widely spoken in medical settings. Limited facilities outside Kuwait City.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Most pharmacies open 8am-12am. Some 24/7 options in hospitals and malls. Closed during Friday prayer.",
        "pharmacyTips": "Pharmacies are well-stocked. Pharmacists speak English and Arabic. Kuwait has strict drug control laws. Verify medications are legal before bringing them.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cough medicine (non-codeine)",
            "oral rehydration salts"
        ],
        "prescriptionRules": "Kuwait has strict drug control laws. Many common medications are restricted or banned. Prescription required for most medications. Foreign prescriptions not accepted.",
        "restrictedMeds": [
            {
                "name": "Codeine-containing medications",
                "status": "banned",
                "note": "All codeine products prohibited."
            },
            {
                "name": "Tramadol",
                "status": "banned",
                "note": "Classified as narcotic. Strictly prohibited."
            },
            {
                "name": "Amphetamines (Adderall, Vyvanse)",
                "status": "banned",
                "note": "Strictly prohibited. Severe criminal penalties."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Zero tolerance. Severe criminal penalties including imprisonment."
            },
            {
                "name": "Benzodiazepines",
                "status": "restricted",
                "note": "Requires documentation and advance approval from Kuwait Ministry of Health."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter in English and Arabic listing all medications. Keep medications in original packaging. For controlled substances, obtain prior approval from Kuwait's Ministry of Health. Drug law violations carry severe penalties.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$35-70/week",
            "tips": "Private healthcare is expensive. ER visits cost $200+. Travel insurance with medical evacuation coverage recommended. Public hospitals may treat emergencies but expect long wait times."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations for most travelers."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is desalinated and safe to drink. Bottled water widely available and preferred by most.",
        "foodSafetyTips": "Good food safety standards in restaurants. Be cautious in extreme summer heat. Excellent Middle Eastern cuisine available at reputable establishments.",
        "medicalTourismNote": "Kuwait is not a major medical tourism destination. Kuwaitis often travel to the UK, US, or Germany for specialized treatment.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Kuwait",
            "Kuwait Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Kuwait. Emergency number 112, strict drug laws, banned medications, pharmacy tips, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Dar Al Shifa Hospital",
                "nearTouristArea": "Kuwait City (Hawally, near The Avenues Mall)",
                "phone": "+965-1802-555",
                "englishSpeaking": True,
                "notes": "Leading private hospital. Modern facilities. International patient services."
            },
            {
                "name": "Al Salam International Hospital",
                "nearTouristArea": "Kuwait City (Salmiya, near Gulf Road)",
                "phone": "+965-2573-6222",
                "englishSpeaking": True,
                "notes": "Established private hospital with 24/7 emergency department."
            },
            {
                "name": "Mubarak Al-Kabeer Hospital",
                "nearTouristArea": "Kuwait City (Jabriya)",
                "phone": "+965-2531-2700",
                "englishSpeaking": True,
                "notes": "Major public teaching hospital. Largest emergency department in Kuwait."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0623\u062d\u062a\u0627\u062c \u062f\u0648\u0627\u0621 \u0644\u0644\u0635\u062f\u0627\u0639",
                "transliteration": "Ahtaaj dawaa' lil-sudaa'"
            },
            {
                "english": "I need a doctor",
                "local": "\u0623\u062d\u062a\u0627\u062c \u0637\u0628\u064a\u0628",
                "transliteration": "Ahtaaj tabeeb"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0623\u064a\u0646 \u0623\u0642\u0631\u0628 \u0635\u064a\u062f\u0644\u064a\u0629\u061f",
                "transliteration": "Ayn aqrab saidaliyya?"
            },
            {
                "english": "I'm allergic to penicillin",
                "local": "\u0639\u0646\u062f\u064a \u062d\u0633\u0627\u0633\u064a\u0629 \u0645\u0646 \u0627\u0644\u0628\u0646\u0633\u0644\u064a\u0646",
                "transliteration": "Indi hasaasiyya min al-bensleen"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Kuwait City with modern private clinics.",
            "costRange": "KWD 15-40 ($49-131) for consultation; KWD 30-100 ($98-327) for procedures",
            "notes": "Many internationally trained dentists. Quality is good at private clinics.",
            "emergencyTip": "Hospital emergency departments handle dental emergencies. Private dental clinics available on weekdays."
        },
        "mentalHealth": {
            "crisisLine": "Contact Kuwait Psychological Association or hospital psychiatric departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available at private hospitals and clinics in Kuwait City.",
            "notes": "Mental health services developing. Private hospitals offer psychiatric consultations."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is improving in newer buildings. Shopping malls and modern hotels are accessible. Older areas have limited accessibility.",
            "hospitalAccess": "Major hospitals are wheelchair accessible.",
            "transport": "Limited accessible public transport. Taxis and ride-hailing available.",
            "tips": "The Avenues Mall and newer attractions are accessible. Kuwait Towers area has some accessible pathways."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Heat-related illness is the primary health concern. Summer temperatures often exceed 50\u00b0C (122\u00b0F)."
        },
        "insuranceClaimProcess": "Private hospitals require upfront payment or insurance authorization. Keep all receipts and medical reports. English documentation available at most facilities."
    },
    "LB": {
        "iso2": "LB",
        "countryName": "Lebanon",
        "countrySlug": "lebanon",
        "flag": "\U0001f1f1\U0001f1e7",
        "emergencyNumber": "140 (Red Cross ambulance), 112 (Internal Security Forces), 175 (fire)",
        "healthcareSystem": "Private healthcare dominant. Public system severely strained due to economic crisis. Many well-trained physicians but hospital resources limited by ongoing crisis.",
        "healthcareSystemType": "private",
        "qualityRating": 3,
        "qualityNotes": "Lebanese doctors and nurses are well-trained (many educated in France, US, UK). Private hospitals in Beirut offer good care. However, the ongoing economic crisis has caused severe shortages of medications, medical supplies, and staff emigration. Conditions are worse outside Beirut.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Most pharmacies open 8am-8pm. Some 24/7 pharmacies in Beirut. Availability has been affected by the economic crisis.",
        "pharmacyTips": "IMPORTANT: Lebanon has experienced severe medication shortages since 2020 due to the economic crisis. Many medications may be unavailable or in short supply. Bring ALL medications you may need for your entire trip. Pharmacists speak Arabic, French, and often English.",
        "commonOTC": [
            "paracetamol (when available)",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "oral rehydration salts",
            "basic first aid supplies"
        ],
        "prescriptionRules": "Prescription enforcement varies. Due to the economic crisis, some medications are rationed. Bring all medications you need from home.",
        "restrictedMeds": [
            {
                "name": "Cannabis/hashish",
                "status": "banned",
                "note": "Illegal despite some legislative reform discussions. Penalties include imprisonment."
            },
            {
                "name": "Amphetamines (Adderall, etc.)",
                "status": "controlled",
                "note": "Controlled substance. Carry doctor's letter and original prescription."
            },
            {
                "name": "Strong opioids",
                "status": "controlled",
                "note": "Controlled. Carry documentation."
            },
            {
                "name": "Benzodiazepines",
                "status": "controlled",
                "note": "Controlled but widely prescribed in Lebanon. Carry documentation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications with generic names. Keep medications in original packaging. Given the medication shortage crisis, bring sufficient supply for your entire trip plus extra. A letter in English or French is acceptable.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-60/week",
            "tips": "Travel insurance with medical evacuation is essential. In the event of a serious medical emergency, evacuation to Turkey, Jordan, or Cyprus may be necessary. Hospitals often require cash payment upfront (USD preferred). The Lebanese pound has lost significant value."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (if visiting rural areas)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Check current CDC travel advisories before travel given the evolving situation."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink in Lebanon. Water infrastructure has deteriorated. Use bottled water for drinking and brushing teeth. Bottled water is affordable and widely available.",
        "foodSafetyTips": "Lebanese cuisine is excellent but be cautious with street food and raw vegetables. Eat at established restaurants in Beirut. Food safety in tourist areas (Gemmayzeh, Hamra, Jounieh) is generally good. Power outages can affect food refrigeration.",
        "medicalTourismNote": "Lebanon was historically a regional medical tourism hub, especially for cosmetic surgery. The economic crisis has significantly impacted this sector, though some clinics still operate at high standards.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Beirut",
            "WHO Lebanon",
            "Lebanese Red Cross"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Lebanon. Emergency numbers (Red Cross 140), medication shortage crisis, pharmacy tips, hospital information, and essential travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "American University of Beirut Medical Center (AUBMC)",
                "nearTouristArea": "Beirut (Hamra / Ras Beirut)",
                "phone": "+961-1-350-000",
                "englishSpeaking": True,
                "notes": "Lebanon's premier hospital. Internationally accredited. English, French, Arabic spoken."
            },
            {
                "name": "Hotel Dieu de France Hospital",
                "nearTouristArea": "Beirut (Achrafieh)",
                "phone": "+961-1-615-300",
                "englishSpeaking": True,
                "notes": "Major hospital near Gemmayzeh nightlife area. French and English spoken."
            },
            {
                "name": "Clemenceau Medical Center",
                "nearTouristArea": "Beirut (Clemenceau / Hamra)",
                "phone": "+961-1-372-888",
                "englishSpeaking": True,
                "notes": "Affiliated with Johns Hopkins. Modern private hospital."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0628\u062f\u064a \u062f\u0648\u0627 \u0644\u0644\u0635\u062f\u0627\u0639",
                "transliteration": "Beddi dawa lal-sudaa' (Lebanese Arabic)"
            },
            {
                "english": "I need a doctor",
                "local": "\u0628\u062f\u064a \u062f\u0643\u062a\u0648\u0631",
                "transliteration": "Beddi docteur"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0648\u064a\u0646 \u0623\u0642\u0631\u0628 \u0635\u064a\u062f\u0644\u064a\u0629\u061f",
                "transliteration": "Wayn aqrab saidaliyye?"
            },
            {
                "english": "Do you have this medicine?",
                "local": "\u0639\u0646\u062f\u0643 \u0647\u0627\u0644\u062f\u0648\u0627\u061f",
                "transliteration": "Andak hal-dawa?"
            },
            {
                "english": "I'm not feeling well",
                "local": "\u0645\u0627 \u0639\u0645 \u062d\u0633 \u0628\u062e\u064a\u0631",
                "transliteration": "Ma am hess bi-kheir"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Beirut. Lebanese dentists are well-trained. Costs are lower than Western countries.",
            "costRange": "$30-80 for consultation; $50-200 for fillings (prices in USD widely accepted)",
            "notes": "Dental tourism was popular pre-crisis. Many dentists still offer excellent care at competitive prices.",
            "emergencyTip": "AUBMC and Hotel Dieu have dental departments for emergencies."
        },
        "mentalHealth": {
            "crisisLine": "1564 (Embrace mental health helpline)",
            "internationalLine": "Embrace: +961-1-341-941",
            "englishTherapists": "Available in Beirut. Many therapists speak English and French. The Lebanese psychological community is well-established.",
            "notes": "Mental health awareness has grown significantly since the 2020 Beirut explosion. Embrace Lifeline (1564) provides 24/7 emotional support."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited in Lebanon. Sidewalks are uneven, many buildings lack elevators, and infrastructure has deteriorated.",
            "hospitalAccess": "Major hospitals like AUBMC have accessibility features. Smaller clinics may not.",
            "transport": "No accessible public transport. Private drivers and taxis are the best option.",
            "tips": "Beirut's hilly terrain and damaged infrastructure make wheelchair navigation challenging. Newer hotels are more accessible. Contact hotels directly about accessibility."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and labs.",
            "notes": "The broader healthcare crisis and medication shortages are more significant health concerns than COVID for travelers."
        },
        "insuranceClaimProcess": "Hospitals often require cash payment upfront (US dollars preferred). Keep all receipts. AUBMC and other major hospitals can provide English-language medical documentation. Insurance companies may have difficulty verifying local charges."
    },
    "IR": {
        "iso2": "IR",
        "countryName": "Iran",
        "countrySlug": "iran",
        "flag": "\U0001f1ee\U0001f1f7",
        "emergencyNumber": "115 (ambulance), 110 (police), 125 (fire)",
        "healthcareSystem": "Government healthcare system with good coverage. Medical care is affordable but quality varies. Major cities have modern hospitals. International sanctions have affected medication availability.",
        "healthcareSystemType": "universal",
        "qualityRating": 3,
        "qualityNotes": "Iranian doctors are well-trained and many speak English. Hospitals in Tehran, Isfahan, and Shiraz offer good care. However, international sanctions have limited access to some medications and medical equipment. Rural healthcare is more limited.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Most pharmacies open 8am-10pm. Hospital pharmacies open 24/7. Limited options in rural areas.",
        "pharmacyTips": "Pharmacists are knowledgeable and many speak English. Some medications may be unavailable due to international sanctions. Iran produces many generic medications domestically. Bring all essential medications from home.",
        "commonOTC": [
            "acetaminophen",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cold medicine",
            "oral rehydration salts"
        ],
        "prescriptionRules": "Prescription required for many medications. Iranian prescriptions needed for controlled substances. Generic alternatives to Western brands are widely available.",
        "restrictedMeds": [
            {
                "name": "All narcotic/opioid medications",
                "status": "banned",
                "note": "Iran has extremely strict anti-narcotics laws. Drug trafficking carries the death penalty. Even small quantities of opioids require extensive documentation."
            },
            {
                "name": "Amphetamines (Adderall, etc.)",
                "status": "banned",
                "note": "Strictly prohibited. No exceptions. Severe criminal penalties."
            },
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Strictly prohibited. Severe criminal penalties including potential death penalty for large quantities."
            },
            {
                "name": "Benzodiazepines",
                "status": "restricted",
                "note": "Available in Iran with local prescription. Carry doctor's documentation for personal use quantities."
            },
            {
                "name": "Alcohol-based medicines",
                "status": "restricted",
                "note": "Alcohol is illegal in Iran. Medicines containing alcohol should be declared and documented."
            }
        ],
        "bringDocumentation": "CRITICAL: Iran has extremely strict drug laws — drug trafficking carries the death penalty. Carry a doctor's letter listing all medications with generic names. Keep medications in original packaging with clear labels. Bring only the amount needed. Declare all medications at customs. A Farsi translation of your medical letter is helpful.",
        "travelInsurance": {
            "recommended": True,
            "required": True,
            "requiredNote": "Travel insurance is mandatory for tourist visa applications. Must include medical coverage.",
            "averageCost": "$30-60/week",
            "tips": "IMPORTANT: Most Western insurance companies and credit cards do NOT cover Iran due to sanctions. Purchase Iran-specific travel insurance from an Iranian provider at the airport or through your tour operator. Medical evacuation may require routing through Turkey or Dubai."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for rural travel)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations for most travelers. Malaria prophylaxis recommended for southeastern provinces (Sistan-Baluchestan) during warmer months."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is generally safe in major cities (Tehran, Isfahan, Shiraz) but quality varies. Bottled water recommended, especially in rural areas and smaller towns.",
        "foodSafetyTips": "Iranian cuisine is generally safe in restaurants. Food hygiene standards are decent in cities. Be cautious with salads and raw vegetables in smaller towns. Kebabs and rice dishes from established restaurants are safe. Avoid raw dairy products in rural areas.",
        "medicalTourismNote": "Iran is a growing medical tourism destination, especially for cosmetic surgery (rhinoplasty), eye surgery, dental work, and cardiac procedures. Costs are a fraction of Western prices with well-trained surgeons.",
        "sources": [
            "CDC Travelers' Health",
            "Swiss Embassy Tehran (US interests section)",
            "Iran Ministry of Health and Medical Education",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Iran. Emergency numbers (115/110/125), extremely strict drug laws, sanctions-related medication shortages, pharmacy tips, and travel insurance requirements.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Parsian Hospital",
                "nearTouristArea": "Tehran (near Vali-e-Asr Square)",
                "phone": "+98-21-8879-5010",
                "englishSpeaking": True,
                "notes": "Private hospital popular with international patients. English-speaking staff."
            },
            {
                "name": "Atieh Hospital",
                "nearTouristArea": "Tehran (Shariati area)",
                "phone": "+98-21-2264-0021",
                "englishSpeaking": True,
                "notes": "Modern private hospital with international patient department."
            },
            {
                "name": "Al-Zahra Hospital",
                "nearTouristArea": "Isfahan (central Isfahan)",
                "phone": "+98-31-3668-2020",
                "englishSpeaking": True,
                "notes": "Major teaching hospital in Isfahan. Near historic tourist areas."
            },
            {
                "name": "Namazi Hospital",
                "nearTouristArea": "Shiraz (near Arg of Karim Khan)",
                "phone": "+98-71-3647-4331",
                "englishSpeaking": True,
                "notes": "Large teaching hospital in Shiraz. Emergency department available."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u0645\u0646 \u062f\u0627\u0631\u0648\u06cc \u0633\u0631\u062f\u0631\u062f \u0646\u06cc\u0627\u0632 \u062f\u0627\u0631\u0645",
                "transliteration": "Man daaruye sardard niyaaz daaram"
            },
            {
                "english": "I need a doctor",
                "local": "\u0645\u0646 \u0628\u0647 \u062f\u06a9\u062a\u0631 \u0646\u06cc\u0627\u0632 \u062f\u0627\u0631\u0645",
                "transliteration": "Man be doktor niyaaz daaram"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u0646\u0632\u062f\u06cc\u06a9\u062a\u0631\u06cc\u0646 \u062f\u0627\u0631\u0648\u062e\u0627\u0646\u0647 \u06a9\u062c\u0627\u0633\u062a\u061f",
                "transliteration": "Nazdiktarin daarukhane kojaast?"
            },
            {
                "english": "I'm allergic to this",
                "local": "\u0645\u0646 \u0628\u0647 \u0627\u06cc\u0646 \u062d\u0633\u0627\u0633\u06cc\u062a \u062f\u0627\u0631\u0645",
                "transliteration": "Man be in hasaasiyat daaram"
            },
            {
                "english": "I have a stomachache",
                "local": "\u0645\u0639\u062f\u0647\u200c\u0627\u0645 \u062f\u0631\u062f \u0645\u06cc\u200c\u06a9\u0646\u062f",
                "transliteration": "Me'de-am dard mikonad"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in major cities. Iran is known for affordable high-quality dental work.",
            "costRange": "$20-50 for consultation; $30-150 for fillings; $100-400 for crowns",
            "notes": "Iran is a popular destination for dental tourism. Dentists in Tehran and Isfahan are well-trained. Costs are significantly lower than Western countries.",
            "emergencyTip": "Hospital emergency departments handle dental emergencies. Many private dental clinics in Tehran."
        },
        "mentalHealth": {
            "crisisLine": "1480 (Social Emergency Hotline — Iran)",
            "internationalLine": "Not available — contact your embassy or tour operator",
            "englishTherapists": "Limited but available in Tehran through private clinics. Iranian psychiatrists are well-trained.",
            "notes": "Mental health services available in major cities. Therapy is becoming more accepted in urban Iran. Cultural sensitivity important."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited in Iran. Historic sites often lack ramps and elevators. Newer hotels and malls are more accessible.",
            "hospitalAccess": "Major hospitals have basic accessibility features.",
            "transport": "Tehran Metro has some accessible stations. Taxis are the most practical option.",
            "tips": "Isfahan's historic bridges and bazaars have limited accessibility. Persepolis is challenging for wheelchair users. Arrange private transport and guides for accessibility needs."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements as of 2026.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals.",
            "notes": "Iran's healthcare system has recovered from COVID. Sanctions-related medication availability is a more relevant concern."
        },
        "insuranceClaimProcess": "Hospitals typically require upfront payment in Iranian rials or sometimes USD. Western credit cards do NOT work in Iran due to sanctions. Bring sufficient cash. Keep all receipts for insurance claims upon return. Documentation available in Farsi (request English translation)."
    },
    "NG": {
        "iso2": "NG",
        "countryName": "Nigeria",
        "countrySlug": "nigeria",
        "flag": "\U0001f1f3\U0001f1ec",
        "emergencyNumber": "112 (emergency line — coverage varies), 199 (fire), 767 (police). In Lagos: 112 or 767",
        "healthcareSystem": "Mixed public-private system. Public healthcare is underfunded. Private hospitals in Lagos and Abuja offer better care. Rural healthcare is very limited.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Lagos and Abuja offer reasonable care. Public hospitals are overcrowded and under-resourced. For serious medical emergencies, evacuation to South Africa, Europe, or the US may be necessary. Bring all medications you may need.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in cities open 8am-9pm. Limited options outside major cities. Be cautious of counterfeit medications from unregistered vendors.",
        "pharmacyTips": "Buy medications only from registered pharmacies (look for Pharmacists Council of Nigeria registration). Counterfeit medications are a serious problem in Nigeria. Major pharmacy chains include HealthPlus and MedPlus. Bring essential medications from home.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials (Coartem/ACT)",
            "oral rehydration salts",
            "antihistamines",
            "insect repellent",
            "anti-diarrheals"
        ],
        "prescriptionRules": "Prescription enforcement is inconsistent. Many medications available without prescription. However, drug quality is a concern — buy from reputable pharmacies only.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Penalties include imprisonment."
            },
            {
                "name": "Codeine-containing cough syrup",
                "status": "banned",
                "note": "Banned since 2018 due to abuse epidemic. Not available in Nigeria."
            },
            {
                "name": "Tramadol (high dose >100mg)",
                "status": "banned",
                "note": "High-dose tramadol banned. Low-dose available by prescription."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry documentation for psychiatric medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications with generic names. Keep medications in original packaging. Bring sufficient supply for your entire trip — availability is unreliable. Be aware of counterfeit medication risks.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$35-70/week",
            "tips": "Travel insurance with medical evacuation coverage is ESSENTIAL. Serious medical cases often require evacuation to South Africa or Europe. Ensure your policy covers malaria treatment and emergency air evacuation ($50,000+). Some insurers charge higher premiums for Nigeria."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers — must have valid certificate)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Meningococcal meningitis (especially during dry season in the north)",
                "Cholera",
                "Rabies (for extended or rural travel)",
                "Malaria prophylaxis (essential — Nigeria has the highest malaria burden globally)",
                "Routine vaccinations (MMR, DTaP, Polio)"
            ],
            "notes": "Yellow Fever vaccination is REQUIRED for all travelers. Malaria is endemic throughout Nigeria — prophylaxis is strongly recommended. Nigeria carries the world's highest malaria burden. Lassa fever occurs in rural areas."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink anywhere in Nigeria. Use only bottled or filtered water for drinking and brushing teeth. Avoid ice in drinks. Sachet water ('pure water') from reputable brands is widely available and affordable.",
        "foodSafetyTips": "Eat at established restaurants. Avoid raw vegetables and salads outside of international hotels. Thoroughly cooked street food (suya, jollof rice) from busy vendors is generally safer. Peel all fruits yourself. Use hand sanitizer frequently.",
        "medicalTourismNote": "Nigeria is not a medical tourism destination. Many Nigerians travel to India, South Africa, or the UK for specialized medical treatment.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Abuja",
            "Nigeria Centre for Disease Control (NCDC)",
            "WHO Nigeria"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Nigeria. Emergency number 112, yellow fever vaccination required, malaria prevention essential, pharmacy safety tips, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Reddington Hospital",
                "nearTouristArea": "Lagos (Victoria Island)",
                "phone": "+234-1-271-2020",
                "englishSpeaking": True,
                "notes": "Leading private hospital in Lagos. Modern facilities. International standard care."
            },
            {
                "name": "Lagoon Hospital (Eko Hospital Group)",
                "nearTouristArea": "Lagos (Victoria Island / Ikoyi)",
                "phone": "+234-1-271-6680",
                "englishSpeaking": True,
                "notes": "Major private hospital near business and tourist areas. 24/7 emergency."
            },
            {
                "name": "National Hospital Abuja",
                "nearTouristArea": "Abuja (Central Business District)",
                "phone": "+234-9-460-0920",
                "englishSpeaking": True,
                "notes": "Nigeria's national referral hospital. Located in the capital."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Mo nilo oogun fun ori fifo",
                "transliteration": "Yoruba (English is widely spoken)"
            },
            {
                "english": "I need a doctor",
                "local": "Mo nilo dokita",
                "transliteration": "Yoruba (English is widely spoken)"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Nibo ni ile itaja oogun ti o sunmo ju?",
                "transliteration": "Yoruba (English is Nigeria's official language)"
            },
            {
                "english": "I need malaria medicine",
                "local": "Mo nilo oogun iba",
                "transliteration": "Yoruba"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Lagos and Abuja. Quality varies significantly.",
            "costRange": "NGN 10,000-50,000 ($6-30) for consultation; NGN 20,000-150,000 ($12-90) for procedures",
            "notes": "Private dental clinics in Lagos offer decent care. Verify credentials and sterilization practices.",
            "emergencyTip": "Hospital emergency departments handle dental emergencies. DentPro and Dental Clinic Lagos are reputable options."
        },
        "mentalHealth": {
            "crisisLine": "0800-1234-5678 (Mentally Aware Nigeria Initiative - MANI)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Lagos and Abuja. English is the official language.",
            "notes": "Mental health services are limited but growing. Stigma around mental health remains. Private therapists available in Lagos."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited throughout Nigeria. Infrastructure is challenging for wheelchair users.",
            "hospitalAccess": "Private hospitals in Lagos have some accessibility features. Most facilities lack proper access.",
            "transport": "No accessible public transport. Private cars with drivers are the best option.",
            "tips": "Lagos traffic can be extreme — plan medical appointments with significant travel time. Many buildings lack elevators and ramps. International hotels are more accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at private hospitals and NCDC labs.",
            "notes": "Malaria, typhoid, and waterborne diseases are far more common health concerns for travelers."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment (cash or card). Keep all receipts. Private hospitals can provide English documentation. Medical evacuation insurance is critical — verify your policy covers Nigeria specifically."
    },
    "GH": {
        "iso2": "GH",
        "countryName": "Ghana",
        "countrySlug": "ghana",
        "flag": "\U0001f1ec\U0001f1ed",
        "emergencyNumber": "112 (emergency services), 193 (fire), 191 (ambulance), 199 (police)",
        "healthcareSystem": "Mixed public-private system. National Health Insurance Scheme (NHIS) covers citizens. Tourists use private hospitals. Good private healthcare in Accra.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Accra offer reasonable care. Public hospitals can be overcrowded. Healthcare quality drops significantly outside Accra and Kumasi. For serious conditions, medical evacuation to South Africa or Europe may be needed.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-8pm in cities. Limited hours in smaller towns. Some hospital pharmacies open 24/7.",
        "pharmacyTips": "Buy from registered pharmacies only. Look for Pharmacy Council of Ghana registration. Counterfeit medications exist — avoid unlicensed vendors and market sellers. Bring essential medications from home. Pharmacists speak English.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials",
            "oral rehydration salts",
            "antihistamines",
            "anti-diarrheals",
            "insect repellent"
        ],
        "prescriptionRules": "Prescription enforcement varies. Many medications available without strict prescription. Buy only from registered pharmacies to ensure quality.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Penalties include imprisonment."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Opioids and strong painkillers are controlled. Carry documentation."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry doctor's letter for psychiatric medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications. Keep medications in original packaging. Bring sufficient supply for your entire trip. Ghana is English-speaking so documentation in English is fine.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation coverage is essential. Serious cases may require evacuation to South Africa or Europe. Ensure coverage includes malaria treatment."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Meningococcal meningitis (for northern Ghana, especially dry season)",
                "Rabies (for extended or rural travel)",
                "Cholera",
                "Malaria prophylaxis (essential — malaria is endemic throughout Ghana)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination is REQUIRED. Malaria prophylaxis is strongly recommended — malaria is the leading cause of illness in Ghana."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled water for drinking and brushing teeth. Sachets of purified water ('pure water') widely available. Avoid ice in drinks outside of international hotels.",
        "foodSafetyTips": "Eat at established restaurants. Street food (grilled tilapia, jollof, kelewele) from busy vendors is generally safer. Avoid raw salads outside upscale restaurants. Peel fruits yourself. Wash hands frequently.",
        "medicalTourismNote": "Ghana is not a major medical tourism destination. Accra has growing private healthcare capacity.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Accra",
            "Ghana Health Service",
            "WHO Ghana"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Ghana. Emergency numbers (112), yellow fever vaccination required, malaria prevention, pharmacy safety, and medical evacuation insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Korle Bu Teaching Hospital",
                "nearTouristArea": "Accra (Korle Bu, near James Town)",
                "phone": "+233-30-267-4091",
                "englishSpeaking": True,
                "notes": "Ghana's largest hospital and main referral center. Can be crowded but has specialists."
            },
            {
                "name": "Nyaho Medical Centre",
                "nearTouristArea": "Accra (Airport Residential Area)",
                "phone": "+233-30-275-2412",
                "englishSpeaking": True,
                "notes": "Leading private hospital. Modern facilities. Popular with expats and tourists."
            },
            {
                "name": "The Trust Hospital",
                "nearTouristArea": "Accra (Osu, near Oxford Street)",
                "phone": "+233-30-276-1974",
                "englishSpeaking": True,
                "notes": "Private hospital near major tourist and shopping area."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Me hia aduro ma me tiri yaw",
                "transliteration": "Twi (English is official and widely spoken)"
            },
            {
                "english": "I need a doctor",
                "local": "Me hia dokota",
                "transliteration": "Twi"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Aduro-ase a \u025bbien no w\u0254 he?",
                "transliteration": "Twi (English is widely understood)"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Accra. Quality varies.",
            "costRange": "GHS 100-300 ($7-20) for consultation; GHS 200-800 ($14-55) for procedures",
            "notes": "Private dental clinics in Accra offer decent care. Verify sterilization practices.",
            "emergencyTip": "Korle Bu Hospital has a dental department. Private dental clinics available in Accra."
        },
        "mentalHealth": {
            "crisisLine": "0244-846-444 (Ghana Mental Health Authority helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Accra. English is the official language.",
            "notes": "Mental health services are limited but growing. Ghana passed a Mental Health Act in 2012. Private therapists available in Accra."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Infrastructure is challenging for wheelchair users.",
            "hospitalAccess": "Private hospitals have some accessibility. Public facilities are generally not accessible.",
            "transport": "No accessible public transport. Private drivers recommended.",
            "tips": "Hotels in Accra vary in accessibility. International chain hotels are more accessible. Cape Coast Castle and Kakum National Park have limited wheelchair access."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics in Accra.",
            "notes": "Malaria is the primary health concern for travelers."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment. Keep all receipts. Private hospitals provide English documentation. Medical evacuation insurance strongly recommended."
    },
    "ET": {
        "iso2": "ET",
        "countryName": "Ethiopia",
        "countrySlug": "ethiopia",
        "flag": "\U0001f1ea\U0001f1f9",
        "emergencyNumber": "907 (ambulance — Addis Ababa), 911 (police), 939 (fire)",
        "healthcareSystem": "Underfunded public system. Private hospitals in Addis Ababa offer better care. Very limited healthcare in rural areas.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Addis Ababa provide reasonable care for common conditions. Public hospitals are severely under-resourced. Outside Addis Ababa, healthcare is extremely limited. For serious conditions, medical evacuation to Nairobi or Dubai is often necessary.",
        "pharmacyAccess": "limited",
        "pharmacyHours": "Pharmacies in Addis Ababa open 8am-8pm. Very limited in rural areas and smaller cities.",
        "pharmacyTips": "Pharmacy availability is limited, especially outside Addis Ababa. Bring ALL medications you will need for your trip. Medication availability is unpredictable. Some basic medications available but quality varies. Buy only from licensed pharmacies.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials",
            "oral rehydration salts",
            "basic antibiotics",
            "insect repellent"
        ],
        "prescriptionRules": "Prescription enforcement is inconsistent. Many medications available without prescription. Quality control is a concern — bring medications from home.",
        "restrictedMeds": [
            {
                "name": "Cannabis/khat-related products",
                "status": "controlled",
                "note": "Cannabis is illegal. Khat is legal and widely used in Ethiopia but illegal to export."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry doctor's letter for psychiatric medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications. Keep medications in original packaging. Bring more than you think you'll need — medications may not be available. English documentation is accepted.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation coverage is ESSENTIAL. Serious medical emergencies often require evacuation to Nairobi ($5,000-15,000). For high-altitude trekking (Simien Mountains), ensure coverage includes altitude sickness and helicopter evacuation."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Cholera",
                "Meningococcal meningitis",
                "Rabies (for animal exposure)",
                "Malaria prophylaxis (essential for areas below 2,000m — NOT needed in Addis Ababa)",
                "Routine vaccinations (MMR, DTaP, Polio)"
            ],
            "notes": "Yellow Fever vaccination required. Malaria is a risk below 2,000m elevation — Addis Ababa (2,400m) is malaria-free. High-altitude trekking in the Simien Mountains requires acclimatization. Altitude sickness is a real risk."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink anywhere in Ethiopia. Use bottled water for drinking and brushing teeth. Avoid ice in drinks. Water purification tablets are useful for trekking.",
        "foodSafetyTips": "Ethiopian cuisine is generally safe in established restaurants. Injera (fermented bread) and wot (stews) served hot are typically safe. Be cautious with raw meat (kitfo/tere siga) — only eat at trusted establishments. Avoid raw vegetables and salads in smaller towns.",
        "medicalTourismNote": "Ethiopia is not a medical tourism destination. For specialized treatment, Ethiopians travel to India, Kenya, or South Africa.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Addis Ababa",
            "Ethiopia Ministry of Health",
            "WHO Ethiopia"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Ethiopia. Emergency numbers, yellow fever required, malaria prevention, altitude sickness risks, pharmacy tips, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Korean Hospital (MCM General Hospital)",
                "nearTouristArea": "Addis Ababa (Bole area, near airport)",
                "phone": "+251-11-662-9090",
                "englishSpeaking": True,
                "notes": "Modern private hospital popular with internationals. Near major hotels and airport."
            },
            {
                "name": "St. Gabriel General Hospital",
                "nearTouristArea": "Addis Ababa (near Meskel Square)",
                "phone": "+251-11-552-6404",
                "englishSpeaking": True,
                "notes": "Well-regarded private hospital. Central location."
            },
            {
                "name": "Hayat Hospital",
                "nearTouristArea": "Addis Ababa (Bole area)",
                "phone": "+251-11-661-4881",
                "englishSpeaking": True,
                "notes": "Private hospital with modern facilities. International patient services."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "\u1208\u1263\u1235 \u121D\u12ED\u1275 \u1218\u12F5\u1210\u1292\u1275 \u12A5\u1348\u120D\u1309\u1308\u120D",
                "transliteration": "Le-ras miyit medhanit ifelgalehu"
            },
            {
                "english": "I need a doctor",
                "local": "\u12D3\u12AD\u121D \u12A5\u1348\u120D\u1309\u1308\u120D",
                "transliteration": "Hakim ifelgalehu"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u1260\u1321\u121D \u12E8\u121D\u1275\u1240\u122D\u1260\u12CD \u12E8\u1218\u12F5\u1210\u1292\u1275 \u1264\u1275 \u12E8\u1275 \u1290\u12CD?",
                "transliteration": "Betam yemitqerbewo ye-medhanit bet yet new?"
            },
            {
                "english": "I feel sick",
                "local": "\u12A0\u121D\u121E\u129D",
                "transliteration": "Ammonye"
            },
            {
                "english": "Help me please",
                "local": "\u12A5\u1263\u12AD\u12CE\u1295 \u12A5\u122D\u12F1\u129D",
                "transliteration": "Ibakwon irdunye"
            }
        ],
        "dentalCare": {
            "availability": "Limited dental care. Private clinics in Addis Ababa provide basic dental services.",
            "costRange": "ETB 500-2,000 ($4-15) for consultation; ETB 1,000-5,000 ($8-38) for procedures",
            "notes": "Dental care is basic. Bring any dental supplies you may need. Resolve dental issues before traveling.",
            "emergencyTip": "St. Gabriel and Korean hospitals have dental services. Private dental clinics in Bole area."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact Amanuel Mental Health Hospital: +251-11-127-7686",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some available in Addis Ababa through private clinics.",
            "notes": "Mental health services are extremely limited in Ethiopia. Amanuel Hospital is the main psychiatric facility. Private therapists in Addis Ababa may speak English."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited throughout Ethiopia. Infrastructure is challenging for wheelchair users.",
            "hospitalAccess": "Private hospitals in Addis Ababa have some accessibility. Most facilities lack proper access.",
            "transport": "No accessible public transport. Private vehicles recommended. Roads can be rough.",
            "tips": "The Simien Mountains and historical sites like Lalibela are very challenging for mobility-impaired travelers. Rock-hewn churches often require climbing. Addis Ababa's light rail has some accessibility features."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in Addis Ababa.",
            "notes": "Malaria, altitude sickness, and waterborne diseases are more common health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment in cash (Ethiopian birr). Keep all receipts. Private hospitals can provide documentation in English. Medical evacuation insurance is critical."
    },
    "RW": {
        "iso2": "RW",
        "countryName": "Rwanda",
        "countrySlug": "rwanda",
        "flag": "\U0001f1f7\U0001f1fc",
        "emergencyNumber": "912 (ambulance), 112 (police), 111 (fire)",
        "healthcareSystem": "Community-based health insurance (Mutuelle de Santé) for citizens. Tourists use private hospitals. Healthcare improving rapidly under government investment.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Healthcare in Kigali is improving rapidly. King Faisal Hospital offers the best care. Rural health centers are basic. For serious medical emergencies, evacuation to Nairobi may be necessary. Rwanda's healthcare system is considered among the best in East Africa for its level of development.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in Kigali open 8am-8pm. Limited options outside the capital.",
        "pharmacyTips": "Pharmacies in Kigali are reasonably well-stocked. Bring essential medications from home, especially for gorilla trekking and rural travel. English and French spoken at pharmacies.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials",
            "oral rehydration salts",
            "antihistamines",
            "insect repellent"
        ],
        "prescriptionRules": "Prescription enforcement varies. Basic medications available over the counter. Bring essential medications from home.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal in Rwanda. Penalties include imprisonment."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for controlled substances."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications. Keep medications in original packaging. English or French documentation accepted. Bring sufficient supply for your entire trip.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation is essential. Gorilla trekking is physically demanding — ensure coverage includes adventure activities and emergency evacuation from remote areas."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (recommended for gorilla trekking and rural areas)",
                "Malaria prophylaxis (essential — malaria is endemic)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination required. Malaria prophylaxis essential for all areas. Gorilla trekking areas (Volcanoes National Park) are at high altitude — some malaria risk still exists."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled water. Clean water widely available in Kigali hotels and restaurants.",
        "foodSafetyTips": "Food in Kigali restaurants is generally safe. Rwanda has high cleanliness standards compared to neighboring countries. Be cautious with street food. Kigali is notably clean.",
        "medicalTourismNote": "Rwanda is not a medical tourism destination but is investing heavily in healthcare infrastructure.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Kigali",
            "Rwanda Biomedical Centre",
            "WHO Rwanda"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Rwanda. Emergency numbers, yellow fever required, malaria prevention for gorilla trekking, pharmacy tips, and travel insurance for adventure activities.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "King Faisal Hospital Kigali",
                "nearTouristArea": "Kigali (Kacyiru, near Kigali Convention Centre)",
                "phone": "+250-252-588-888",
                "englishSpeaking": True,
                "notes": "Rwanda's best hospital. International standard care. English and French spoken."
            },
            {
                "name": "Rwanda Military Hospital (Kanombe)",
                "nearTouristArea": "Kigali (near airport)",
                "phone": "+250-252-585-742",
                "englishSpeaking": True,
                "notes": "Major military hospital that treats civilians. Good trauma care."
            },
            {
                "name": "CHUK (Centre Hospitalier Universitaire de Kigali)",
                "nearTouristArea": "Kigali (city center)",
                "phone": "+250-252-575-555",
                "englishSpeaking": True,
                "notes": "Main university teaching hospital. Emergency services available."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Nkeneye imiti y'umutwe",
                "transliteration": "Kinyarwanda (English and French also spoken)"
            },
            {
                "english": "I need a doctor",
                "local": "Nkeneye muganga",
                "transliteration": "Kinyarwanda"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Farumasi iri hafi iri hehe?",
                "transliteration": "Kinyarwanda (English widely understood in Kigali)"
            },
            {
                "english": "I feel sick",
                "local": "Ndwaye",
                "transliteration": "Kinyarwanda"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care available in Kigali. Limited elsewhere.",
            "costRange": "RWF 10,000-30,000 ($8-23) for consultation; RWF 20,000-80,000 ($15-60) for procedures",
            "notes": "Dental care is basic but improving. Resolve dental issues before traveling.",
            "emergencyTip": "King Faisal Hospital has dental services. Private dental clinics available in Kigali."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact King Faisal Hospital psychiatric department",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Limited. Some available in Kigali. Rwanda has invested in community mental health following the 1994 genocide.",
            "notes": "Mental health services are developing. Rwanda has community-based psychosocial support. Private therapists limited in Kigali."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited. Kigali is hilly with few ramps. Gorilla trekking is physically demanding and not wheelchair accessible.",
            "hospitalAccess": "King Faisal Hospital has accessibility features. Most facilities have limited access.",
            "transport": "No accessible public transport. Private vehicles and motorbike taxis (motos) are common.",
            "tips": "Gorilla trekking requires several hours of hiking through dense forest on steep terrain. Not suitable for significant mobility limitations. Some lodges have accessible rooms — inquire directly."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in Kigali.",
            "notes": "Malaria prevention is the primary health concern for travelers."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment. Keep all receipts. King Faisal Hospital can provide English and French documentation."
    },
    "UG": {
        "iso2": "UG",
        "countryName": "Uganda",
        "countrySlug": "uganda",
        "flag": "\U0001f1fa\U0001f1ec",
        "emergencyNumber": "999 (police), 112 (emergency), 0800-100-066 (ambulance — AAR)",
        "healthcareSystem": "Mixed public-private. Public healthcare is free but severely under-resourced. Private hospitals in Kampala offer better care.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Kampala provide adequate care for common conditions. Public hospitals are overcrowded. Healthcare in rural areas is very limited. For serious medical emergencies, evacuation to Nairobi is common.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in Kampala open 8am-8pm. Very limited in rural areas.",
        "pharmacyTips": "Pharmacies in Kampala are reasonably stocked. Bring essential medications from home. Be cautious of counterfeit medications. English is widely spoken.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials (ACT/Coartem)",
            "oral rehydration salts",
            "antihistamines",
            "insect repellent",
            "anti-diarrheals"
        ],
        "prescriptionRules": "Prescription enforcement is inconsistent. Many medications available without prescription. Bring essential medications from home.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Severe penalties including imprisonment."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry doctor's letter for psychiatric medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications. Keep medications in original packaging. English documentation is fine. Bring more than you need as availability is unreliable outside Kampala.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation is ESSENTIAL. Coverage should include gorilla trekking, safari activities, and emergency helicopter evacuation. Medical evacuation to Nairobi can cost $10,000-20,000."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Cholera",
                "Rabies (for animal exposure, especially for gorilla/chimp trekking)",
                "Meningococcal meningitis",
                "Malaria prophylaxis (essential — Uganda is a high-risk malaria country)",
                "Routine vaccinations (MMR, DTaP, Polio)"
            ],
            "notes": "Yellow Fever vaccination REQUIRED. Malaria is a major risk throughout Uganda including Kampala. Take prophylaxis and use insect repellent. Gorilla trekkers should have rabies vaccination."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled or purified water everywhere. Avoid ice in drinks. Water purification tablets useful for trekking.",
        "foodSafetyTips": "Eat at established restaurants in Kampala. Safari lodge food is generally safe and well-prepared. Be cautious with street food. Peel fruits yourself. Use hand sanitizer frequently.",
        "medicalTourismNote": "Uganda is not a medical tourism destination. For specialized treatment, patients travel to Nairobi or India.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Kampala",
            "Uganda Ministry of Health",
            "WHO Uganda"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Uganda. Emergency numbers, yellow fever required, malaria prevention for gorilla trekking and safaris, and medical evacuation insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "International Hospital Kampala (IHK)",
                "nearTouristArea": "Kampala (Namuwongo, near city center)",
                "phone": "+256-312-200-400",
                "englishSpeaking": True,
                "notes": "Leading private hospital. International standard. Popular with expats and tourists."
            },
            {
                "name": "Norvik Hospital",
                "nearTouristArea": "Kampala (Bukoto, near Acacia Mall)",
                "phone": "+256-414-256-001",
                "englishSpeaking": True,
                "notes": "Private hospital with modern facilities. Emergency department."
            },
            {
                "name": "Mulago National Referral Hospital",
                "nearTouristArea": "Kampala (Mulago Hill)",
                "phone": "+256-414-554-001",
                "englishSpeaking": True,
                "notes": "Uganda's national referral hospital. Public facility — can be crowded but has specialists."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Njagala eddagala ly'omutwe",
                "transliteration": "Luganda (English is official and widely spoken)"
            },
            {
                "english": "I need a doctor",
                "local": "Njagala omusawo",
                "transliteration": "Luganda"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Dduka ly'eddagala eri kumpi li ludda wa?",
                "transliteration": "Luganda (English widely understood)"
            },
            {
                "english": "I have malaria",
                "local": "Nnina omusujja gw'ensiri",
                "transliteration": "Luganda"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care in Kampala. Limited elsewhere.",
            "costRange": "UGX 50,000-150,000 ($13-40) for consultation; UGX 100,000-400,000 ($27-107) for procedures",
            "notes": "Private dental clinics in Kampala offer reasonable care. Resolve dental issues before traveling.",
            "emergencyTip": "International Hospital Kampala has dental services."
        },
        "mentalHealth": {
            "crisisLine": "0800-212-121 (Befrienders Uganda)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Kampala. English is the official language.",
            "notes": "Mental health services are limited but growing. Butabika National Referral Mental Hospital is the main psychiatric facility."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited in Uganda. Infrastructure is challenging for wheelchair users.",
            "hospitalAccess": "International Hospital Kampala has some accessibility features.",
            "transport": "No accessible public transport. Private vehicles recommended. Roads can be rough.",
            "tips": "Gorilla and chimp trekking involves strenuous hiking through dense forest. Not suitable for significant mobility limitations. Safari lodges vary — inquire about accessibility."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in Kampala.",
            "notes": "Malaria and waterborne diseases are the primary health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment. Keep all receipts. Private hospitals provide English documentation. AAR Health Services offers evacuation services."
    },
    "SN": {
        "iso2": "SN",
        "countryName": "Senegal",
        "countrySlug": "senegal",
        "flag": "\U0001f1f8\U0001f1f3",
        "emergencyNumber": "15 (SAMU ambulance), 17 (police), 18 (fire)",
        "healthcareSystem": "Mixed system. Public healthcare is limited. Dakar has good private clinics, many with French-trained doctors. Rural healthcare is basic.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private clinics in Dakar offer good care, often staffed by French-trained doctors. Public hospitals can be overcrowded. Healthcare outside Dakar is very limited. For serious emergencies, evacuation to France or Morocco may be necessary.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in Dakar open 8am-10pm with rotating duty pharmacies (pharmacie de garde) open 24/7. Limited in rural areas.",
        "pharmacyTips": "Pharmacies in Senegal follow the French model and are well-regulated. Look for the green cross. Pharmacists speak French and sometimes English. Medications are generally authentic (Senegal has good pharmaceutical regulation). Bring essential medications from home.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antimalarials",
            "oral rehydration salts",
            "antihistamines",
            "anti-diarrheals",
            "insect repellent"
        ],
        "prescriptionRules": "Prescription required for many medications. French-style pharmaceutical regulation. Pharmacists are well-trained and can advise on common ailments.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Strictly illegal. Severe penalties."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for controlled substances."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry doctor's letter."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications (French translation helpful). Keep medications in original packaging. Bring sufficient supply for your trip.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation coverage is essential. Evacuation to France or Morocco may be needed for serious conditions. Ensure coverage includes malaria treatment."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Meningococcal meningitis (especially during dry season, Dec-June)",
                "Rabies (for extended or rural travel)",
                "Malaria prophylaxis (essential — malaria is endemic throughout Senegal)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination required. Malaria prophylaxis strongly recommended for all areas. Risk is highest during and just after the rainy season (July-October)."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled water for drinking and brushing teeth. Bottled water widely available.",
        "foodSafetyTips": "Senegalese cuisine is excellent. Eat at established restaurants. Thieboudienne (national dish) and grilled fish are generally safe when freshly cooked. Be cautious with raw vegetables and salads. Street food from busy vendors is often safer than from quiet ones.",
        "medicalTourismNote": "Senegal is not a major medical tourism destination. Dakar serves as a regional healthcare hub for West Africa.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Dakar",
            "Senegal Ministry of Health",
            "Institut Pasteur de Dakar"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Senegal. Emergency number SAMU (15), yellow fever required, malaria prevention, French-style pharmacies, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "H\u00f4pital Principal de Dakar",
                "nearTouristArea": "Dakar (Plateau, near Independence Square)",
                "phone": "+221-33-839-5050",
                "englishSpeaking": False,
                "notes": "Major military hospital open to civilians. French-speaking. Good quality care."
            },
            {
                "name": "Clinique de la Madeleine",
                "nearTouristArea": "Dakar (Plateau / Madeleine area)",
                "phone": "+221-33-849-6969",
                "englishSpeaking": False,
                "notes": "Well-regarded private clinic. French-speaking staff."
            },
            {
                "name": "SOS M\u00e9decins Dakar",
                "nearTouristArea": "Dakar (mobile — house calls available)",
                "phone": "+221-33-889-1515",
                "englishSpeaking": False,
                "notes": "French-style house call service. Very useful for tourists in hotels. French-speaking."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "J'ai besoin d'un m\u00e9dicament pour le mal de t\u00eate",
                "transliteration": "French (primary language in healthcare)"
            },
            {
                "english": "I need a doctor",
                "local": "J'ai besoin d'un m\u00e9decin",
                "transliteration": "French"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "O\u00f9 est la pharmacie la plus proche?",
                "transliteration": "French"
            },
            {
                "english": "I feel sick",
                "local": "Damay f\u00e9bar",
                "transliteration": "Wolof (local language)"
            },
            {
                "english": "Help me",
                "local": "Jaaral ma",
                "transliteration": "Wolof"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Dakar. Limited elsewhere.",
            "costRange": "CFA 15,000-40,000 ($24-65) for consultation; CFA 30,000-100,000 ($49-163) for procedures",
            "notes": "Private dental clinics in Dakar offer French-standard care. Dentists are well-trained.",
            "emergencyTip": "H\u00f4pital Principal de Dakar has a dental department. Private dental clinics in Dakar available."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact H\u00f4pital Fann psychiatric department: +221-33-825-0018",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. French-speaking therapists available in Dakar.",
            "notes": "Senegal has a notable psychiatric tradition (Fann Hospital is historically significant in African psychiatry). Services primarily in French."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Streets and sidewalks are uneven. Few buildings have wheelchair access.",
            "hospitalAccess": "Major hospitals have basic accessibility. Most clinics lack proper access.",
            "transport": "No accessible public transport. Private drivers recommended.",
            "tips": "Gor\u00e9e Island involves boat access and steep stairs. Beaches may be difficult to navigate. Newer hotels in Dakar are more accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at Institut Pasteur de Dakar and hospitals.",
            "notes": "Malaria and waterborne diseases are the primary health concerns."
        },
        "insuranceClaimProcess": "Hospitals and clinics often require upfront payment. Keep all receipts. French-language documentation standard — request English if needed. SOS M\u00e9decins can provide receipts for house calls."
    },
    "CL": {
        "iso2": "CL",
        "countryName": "Chile",
        "countrySlug": "chile",
        "flag": "\U0001f1e8\U0001f1f1",
        "emergencyNumber": "131 (ambulance — SAMU), 133 (police), 132 (fire)",
        "healthcareSystem": "Dual public-private system. FONASA (public) and ISAPREs (private). Tourists typically use private clinics. Excellent healthcare in Santiago.",
        "healthcareSystemType": "mixed",
        "qualityRating": 4,
        "qualityNotes": "Chile has the best healthcare system in Latin America. Private clinics in Santiago are world-class (Cl\u00ednica Alemana, Cl\u00ednica Las Condes). Public hospitals are adequate but slower. Healthcare is good throughout major cities but limited in remote Patagonia and Atacama Desert areas.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-10pm. Major chains (Cruz Verde, FASA/Ahumada, Salcobrand) have 24/7 locations in cities.",
        "pharmacyTips": "Chile has excellent pharmacy chains with well-stocked locations. Pharmacists speak Spanish. Some medications that require prescriptions in the US are available OTC in Chile. Prices are reasonable.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cold medicine",
            "altitude sickness pills (acetazolamide in pharmacies near San Pedro de Atacama)"
        ],
        "prescriptionRules": "Many medications available without prescription. Antibiotics technically require a prescription but enforcement varies. Controlled substances require a Chilean prescription.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "controlled",
                "note": "Medical cannabis has some legal framework but recreational use is decriminalized only for personal use in private. Do not bring cannabis products into Chile."
            },
            {
                "name": "Stimulant medications (Adderall, Ritalin)",
                "status": "controlled",
                "note": "Controlled substances. Carry doctor's letter and original prescription."
            },
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Controlled. Carry documentation for personal use."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications with generic names. Spanish translation helpful but not required at major hospitals. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Private healthcare in Santiago is excellent but can be expensive. A clinic visit costs $50-150. Travel insurance with medical evacuation coverage is important for Patagonia, Atacama, and Easter Island travel where facilities are limited."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Chile has no malaria risk. Easter Island (Rapa Nui) may have dengue risk — use insect repellent."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink in major cities. In some rural areas and the Atacama Desert, bottled water is recommended.",
        "foodSafetyTips": "Chile has good food safety standards. Seafood (ceviche, mariscos) is generally safe at established restaurants. Raw seafood from reputable restaurants is safe. Chilean wine regions have excellent food quality.",
        "medicalTourismNote": "Chile is a growing medical tourism destination, especially for dental work, cosmetic surgery, and ophthalmology. Santiago clinics offer high quality at lower costs than the US.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Santiago",
            "Chile Ministry of Health (MINSAL)",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Chile. Emergency numbers (131/133/132), excellent healthcare, pharmacy tips, altitude sickness advice for Atacama, and travel insurance for Patagonia.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Cl\u00ednica Alemana",
                "nearTouristArea": "Santiago (Vitacura, near Las Condes)",
                "phone": "+56-2-2210-1111",
                "englishSpeaking": True,
                "notes": "Chile's top-rated private hospital. JCI-accredited. International patient department. English spoken."
            },
            {
                "name": "Cl\u00ednica Las Condes",
                "nearTouristArea": "Santiago (Las Condes, near Costanera Center)",
                "phone": "+56-2-2210-4000",
                "englishSpeaking": True,
                "notes": "Premier private hospital. Near major shopping and hotel areas."
            },
            {
                "name": "Hospital Regional de Punta Arenas",
                "nearTouristArea": "Punta Arenas (gateway to Torres del Paine)",
                "phone": "+56-61-220-5000",
                "englishSpeaking": False,
                "notes": "Main hospital for Patagonia region. Limited English. Closest facility for Torres del Paine emergencies."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicamento para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un doctor",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have altitude sickness",
                "local": "Tengo mal de altura / puna",
                "transliteration": "Spanish (puna is the local term)"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care in Santiago at significantly lower costs than the US.",
            "costRange": "CLP 30,000-60,000 ($30-65) for consultation; CLP 50,000-200,000 ($55-220) for procedures",
            "notes": "Santiago is a dental tourism destination. Modern clinics with well-trained dentists.",
            "emergencyTip": "Cl\u00ednica Alemana and Cl\u00ednica Las Condes have dental departments. Emergency dental clinics available in Santiago."
        },
        "mentalHealth": {
            "crisisLine": "600 360 7777 (Salud Responde — health helpline)",
            "internationalLine": "Contact your embassy for English-speaking referrals",
            "englishTherapists": "Available in Santiago through private clinics and expat networks.",
            "notes": "Mental health services available in Santiago. Chile has a growing mental health infrastructure."
        },
        "accessibilityInfo": {
            "overview": "Santiago has improving accessibility. Metro is mostly accessible. Patagonia and Atacama have very limited accessibility.",
            "hospitalAccess": "Major hospitals are wheelchair accessible.",
            "transport": "Santiago Metro has elevators at most stations. Accessible taxis can be arranged. Intercity buses rarely accessible.",
            "tips": "Torres del Paine and Atacama Desert excursions are very challenging for mobility-impaired travelers. Santiago city center and Providencia are relatively accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at clinics and pharmacies.",
            "notes": "Altitude sickness (in Atacama, above 3,000m) and sun exposure are more relevant health concerns."
        },
        "insuranceClaimProcess": "Private clinics typically bill insurance directly or require credit card payment. Keep all receipts (boleta). Cl\u00ednicas Alemana and Las Condes have international billing departments. File claims within 30 days."
    },
    "EC": {
        "iso2": "EC",
        "countryName": "Ecuador",
        "countrySlug": "ecuador",
        "flag": "\U0001f1ea\U0001f1e8",
        "emergencyNumber": "911 (unified emergency — ambulance, police, fire)",
        "healthcareSystem": "Mixed public-private. Public system (IESS) for citizens. Private clinics in Quito and Guayaquil for tourists. Limited in rural and Gal\u00e1pagos areas.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Good private hospitals in Quito and Guayaquil. Healthcare in the Gal\u00e1pagos Islands is very limited — serious cases require evacuation to the mainland. Altitude sickness is a real concern in Quito (2,850m) and the highlands.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-10pm. Chains like Fybeca and Pharmacys have 24/7 locations in major cities.",
        "pharmacyTips": "Pharmacies are well-stocked in cities. Many medications available without prescription. Pharmacists speak Spanish. Bring altitude sickness medication (acetazolamide) if heading to the highlands.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "altitude sickness medication",
            "oral rehydration salts",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require a prescription. Antibiotics often available OTC.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "controlled",
                "note": "Personal use quantities decriminalized but import is illegal."
            },
            {
                "name": "Stimulant medications (Adderall)",
                "status": "controlled",
                "note": "Controlled substance. Carry documentation."
            },
            {
                "name": "Opioid medications",
                "status": "controlled",
                "note": "Carry doctor's letter and original prescription."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging. Bring altitude sickness medication if visiting the highlands.",
        "travelInsurance": {
            "recommended": True,
            "required": True,
            "requiredNote": "Travel insurance with medical coverage is required for entry into Ecuador.",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance is mandatory. Ensure coverage includes medical evacuation from the Gal\u00e1pagos Islands (evacuation to mainland: $5,000-15,000) and altitude-related illness. Adventure activity coverage important for climbing."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (recommended for travel to Amazon/Oriente regions below 2,300m)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for Amazon travel)",
                "Malaria prophylaxis (for Amazon lowlands / Oriente)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination strongly recommended for Amazon travel. Malaria risk in lowland Amazon areas only — NOT in Quito, Gal\u00e1pagos, or highlands. Altitude sickness is a serious concern in Quito and above."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is NOT safe to drink in most of Ecuador. Use bottled water. In Quito, some filtered tap water is improving but bottled is still recommended. In the Gal\u00e1pagos, water quality varies by island.",
        "foodSafetyTips": "Eat at established restaurants. Ceviche is popular and generally safe at reputable places. Be cautious with street food and raw vegetables. In the Gal\u00e1pagos, eat at established restaurants or your tour's included meals.",
        "medicalTourismNote": "Ecuador is a growing medical tourism destination, particularly for dental work and cosmetic surgery in Cuenca.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Quito",
            "Ecuador Ministry of Public Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Ecuador. Emergency number 911, altitude sickness in Quito, Gal\u00e1pagos health tips, malaria prevention for Amazon, and mandatory travel insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Metropolitano",
                "nearTouristArea": "Quito (north, near Parque La Carolina)",
                "phone": "+593-2-399-8000",
                "englishSpeaking": True,
                "notes": "Quito's best private hospital. International patient department. Modern facilities."
            },
            {
                "name": "Hospital Vozandes Quito",
                "nearTouristArea": "Quito (near Mariscal Sucre tourist area)",
                "phone": "+593-2-397-1000",
                "englishSpeaking": True,
                "notes": "Well-regarded private hospital. Founded by missionaries. English-speaking staff available."
            },
            {
                "name": "Hospital Oscar Jandl",
                "nearTouristArea": "Puerto Ayora, Santa Cruz (Gal\u00e1pagos Islands)",
                "phone": "+593-5-252-6103",
                "englishSpeaking": False,
                "notes": "Main hospital in the Gal\u00e1pagos. Basic facilities only — serious cases evacuated to mainland."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have altitude sickness",
                "local": "Tengo mal de altura / soroche",
                "transliteration": "Spanish (soroche is the Andean term)"
            },
            {
                "english": "I feel dizzy",
                "local": "Estoy mareado/a",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Quito and Cuenca. Cuenca is a dental tourism hub.",
            "costRange": "$25-60 for consultation; $40-150 for procedures (USD — Ecuador uses US dollars)",
            "notes": "Ecuador uses the US dollar, making pricing transparent. Cuenca is popular for dental tourism with excellent quality at low prices.",
            "emergencyTip": "Hospital Metropolitano has dental services. Emergency dental clinics available in Quito."
        },
        "mentalHealth": {
            "crisisLine": "171 (health information line)",
            "internationalLine": "Contact your embassy for English-speaking referrals",
            "englishTherapists": "Available in Quito and Cuenca through expat networks.",
            "notes": "Mental health services limited. Growing expat community in Cuenca has English-speaking therapists."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited. Colonial centers (Quito, Cuenca) have cobblestone streets and steep hills. Gal\u00e1pagos has natural terrain challenges.",
            "hospitalAccess": "Major hospitals in Quito are accessible.",
            "transport": "Quito's Trolebus has some accessible vehicles. Taxis widely available.",
            "tips": "Quito's Old Town is very hilly with cobblestones. Gal\u00e1pagos involves wet landings from boats and rocky terrain. Altitude adds physical challenge for all visitors."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Altitude sickness is a more relevant health concern for highland visitors."
        },
        "insuranceClaimProcess": "Private hospitals may bill insurance directly or require payment. Ecuador uses US dollars. Keep all receipts. Major hospitals provide documentation in Spanish (request English if needed)."
    },
    "DO": {
        "iso2": "DO",
        "countryName": "Dominican Republic",
        "countrySlug": "dominican-republic",
        "flag": "\U0001f1e9\U0001f1f4",
        "emergencyNumber": "911 (unified emergency)",
        "healthcareSystem": "Mixed public-private. Public hospitals are under-resourced. Private clinics in tourist areas and Santo Domingo offer better care.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Good private hospitals in Santo Domingo and Punta Cana area. Tourist resorts typically have on-site medical clinics. Public hospitals are overcrowded. For serious emergencies, medical evacuation to Miami is common.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-10pm. Chains like Carol, GBC, and Los Hidalgos have extended hours.",
        "pharmacyTips": "Pharmacies are well-stocked and affordable. Many medications available without prescription. Pharmacists speak Spanish. Tourist area pharmacies may have English-speaking staff.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "sunscreen",
            "insect repellent"
        ],
        "prescriptionRules": "Many medications available without prescription. Antibiotics often sold OTC. Controlled substances require a prescription.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Possession can result in arrest."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Keep medications in original packaging. Spanish translation helpful but not essential in tourist areas.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Most resorts include basic medical care. For serious emergencies, medical evacuation to Miami costs $15,000-30,000. Ensure coverage includes water sports and adventure activities."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for extended or rural travel)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Dengue and Zika risk exists — use insect repellent. No malaria risk in tourist areas."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled water. Resorts provide purified water and ice made from purified water. Outside resorts, avoid ice in drinks.",
        "foodSafetyTips": "Resort food is safe. Outside resorts, eat at established restaurants. Be cautious with street food, raw seafood from beach vendors, and unpeeled fruits. Dominican cuisine is generally cooked thoroughly.",
        "medicalTourismNote": "The Dominican Republic is a growing medical tourism destination, especially for cosmetic surgery and dental work in Santo Domingo.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Santo Domingo",
            "Dominican Republic Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for the Dominican Republic. Emergency 911, resort medical care, pharmacy tips, dengue prevention, hurricane season health risks, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Centro M\u00e9dico UCE (CEDIMAT)",
                "nearTouristArea": "Santo Domingo (near Zona Colonial)",
                "phone": "+1-809-688-4411",
                "englishSpeaking": True,
                "notes": "Top private hospital. Internationally recognized. English-speaking staff."
            },
            {
                "name": "Hospiten Bavaro",
                "nearTouristArea": "B\u00e1varo / Punta Cana (near resorts)",
                "phone": "+1-809-686-1414",
                "englishSpeaking": True,
                "notes": "International hospital chain in the main tourist zone. Handles tourist medical needs."
            },
            {
                "name": "Centro M\u00e9dico Punta Cana",
                "nearTouristArea": "Punta Cana (near airport and resorts)",
                "phone": "+1-809-552-1506",
                "englishSpeaking": True,
                "notes": "Private clinic serving the resort area. 24/7 emergency. English-speaking."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have a sunburn",
                "local": "Tengo una quemadura de sol",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Santo Domingo at affordable prices.",
            "costRange": "$30-60 for consultation; $50-200 for procedures (prices in USD accepted)",
            "notes": "Dominican Republic is a dental tourism destination. Quality clinics in Santo Domingo.",
            "emergencyTip": "CEDIMAT has dental services. Resort concierges can arrange dental appointments."
        },
        "mentalHealth": {
            "crisisLine": "1-200-1202 (L\u00ednea de la Vida — crisis helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Limited. Available through private clinics in Santo Domingo and expatriate networks.",
            "notes": "Mental health services limited. Resorts may have access to English-speaking counselors."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited outside of modern resorts. Colonial zones have cobblestones. Beaches may lack accessible pathways.",
            "hospitalAccess": "Major private hospitals are accessible.",
            "transport": "No accessible public transport. Resorts may offer accessible facilities. Private transfers recommended.",
            "tips": "All-inclusive resorts vary in accessibility — inquire before booking. Zona Colonial in Santo Domingo has uneven surfaces. Some beaches have beach wheelchair rentals."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals, clinics, and some resorts.",
            "notes": "Dengue fever, sun exposure, and water safety are more relevant health concerns. Hurricane season (June-November) can disrupt medical services."
        },
        "insuranceClaimProcess": "Private hospitals accept credit cards. Resort clinics may bill directly. Keep all receipts. Major hospitals provide English documentation on request."
    },
    "JM": {
        "iso2": "JM",
        "countryName": "Jamaica",
        "countrySlug": "jamaica",
        "flag": "\U0001f1ef\U0001f1f2",
        "emergencyNumber": "110 (police), 110 (fire), 110 (ambulance)",
        "healthcareSystem": "Mixed public-private. Public hospitals provide free basic care. Private hospitals in Kingston and Montego Bay offer better care. Tourist areas have private clinics.",
        "healthcareSystemType": "mixed",
        "qualityRating": 3,
        "qualityNotes": "Good private hospitals in Kingston and Montego Bay. Tourist areas have private clinics familiar with traveler health needs. Public hospitals are adequate for emergencies but can be crowded. English is spoken everywhere.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-8pm. Fontana Pharmacy chain has extended hours.",
        "pharmacyTips": "Pharmacies are well-stocked and modern. All staff speak English. Many medications available without prescription. Bring specific prescription medications from home.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "sunscreen",
            "insect repellent",
            "oral rehydration salts"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require a prescription. Jamaica is English-speaking so communication is easy.",
        "restrictedMeds": [
            {
                "name": "Cannabis/ganja",
                "status": "controlled",
                "note": "Decriminalized for small amounts (up to 2 oz). Medical cannabis legal. However, do NOT bring cannabis into or out of Jamaica — trafficking is illegal."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry doctor's letter for opioid medications."
            },
            {
                "name": "Psychotropic medications",
                "status": "controlled",
                "note": "Carry documentation for psychiatric medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Keep medications in original packaging. English documentation is fine — Jamaica is English-speaking.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation recommended. For serious emergencies, evacuation to Miami is common ($15,000-30,000). Ensure coverage includes water sports and adventure activities."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Dengue risk exists — use insect repellent. No malaria in Jamaica."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is generally safe in Kingston and major tourist areas. In rural areas, use bottled water. Resort water is safe. When in doubt, use bottled water.",
        "foodSafetyTips": "Jamaican cuisine is generally safe at restaurants. Be cautious with street food (jerk chicken from busy vendors is usually fine). Avoid raw shellfish from beach vendors. Ackee (national fruit) must be properly prepared — eat only at restaurants.",
        "medicalTourismNote": "Jamaica is not a major medical tourism destination. For specialized treatment, patients travel to Miami or other US cities.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Kingston",
            "Jamaica Ministry of Health & Wellness",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Jamaica. Emergency number 110, pharmacy tips, dengue prevention, hurricane season health risks, and medical evacuation insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "University Hospital of the West Indies",
                "nearTouristArea": "Kingston (Mona)",
                "phone": "+1-876-927-1620",
                "englishSpeaking": True,
                "notes": "Jamaica's main teaching hospital. Good quality care. Emergency department."
            },
            {
                "name": "Cornwall Regional Hospital",
                "nearTouristArea": "Montego Bay (near Hip Strip tourist area)",
                "phone": "+1-876-952-5100",
                "englishSpeaking": True,
                "notes": "Main hospital for Montego Bay area. Closest for north coast tourists."
            },
            {
                "name": "MoBay Hope Medical Centre",
                "nearTouristArea": "Montego Bay (Fairview)",
                "phone": "+1-876-953-3649",
                "englishSpeaking": True,
                "notes": "Private clinic in Montego Bay. Familiar with tourist medical needs."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Mi need medicine fi headache",
                "transliteration": "Jamaican Patois (English is official)"
            },
            {
                "english": "I need a doctor",
                "local": "Mi need a doctor",
                "transliteration": "English (official language)"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Where is the nearest pharmacy?",
                "transliteration": "English is used everywhere"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Kingston and Montego Bay. Reasonable quality.",
            "costRange": "J$5,000-15,000 ($32-96) for consultation; J$10,000-50,000 ($64-320) for procedures",
            "notes": "Private dental clinics offer decent care. All staff speak English.",
            "emergencyTip": "University Hospital of the West Indies has dental services. Private dental clinics in tourist areas."
        },
        "mentalHealth": {
            "crisisLine": "888-639-5433 (National Council on Drug Abuse helpline)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Kingston and Montego Bay. English is the official language.",
            "notes": "Mental health services limited but growing. Private therapists available in Kingston."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited. Many buildings and attractions lack wheelchair access. Resort facilities vary.",
            "hospitalAccess": "Major hospitals have some accessibility features.",
            "transport": "No accessible public transport. Private transport and resort shuttles available.",
            "tips": "All-inclusive resorts vary in accessibility — confirm before booking. Dunn's River Falls and Blue Mountains are challenging for mobility-impaired visitors. Beaches may lack wheelchair access."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Dengue, sun exposure, and hurricane season (June-November) are more relevant health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment (JMD or USD). Keep all receipts. English documentation provided. Resort clinics may assist with insurance claims."
    },
    "PA": {
        "iso2": "PA",
        "countryName": "Panama",
        "countrySlug": "panama",
        "flag": "\U0001f1f5\U0001f1e6",
        "emergencyNumber": "911 (unified emergency)",
        "healthcareSystem": "Mixed public-private. Private hospitals in Panama City are excellent. Public hospitals (CSS) are available but slower.",
        "healthcareSystemType": "mixed",
        "qualityRating": 4,
        "qualityNotes": "Panama City has excellent private hospitals, some of the best in Central America. Many doctors trained in the US. Healthcare quality drops outside Panama City. San Blas Islands and Bocas del Toro have very limited facilities.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-10pm. Farmacias Arrocha and Metro chains have 24/7 locations.",
        "pharmacyTips": "Pharmacies are well-stocked and modern. Many medications available without prescription. Prices are reasonable. US dollars used (Panama uses USD). Staff speak Spanish but some speak English in tourist areas.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "insect repellent",
            "oral rehydration salts",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require a prescription.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Penalties include imprisonment."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance recommended especially for travel outside Panama City. Medical evacuation from remote areas (Dari\u00e9n, San Blas) can be costly."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area; required for travel to Dari\u00e9n province)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Malaria prophylaxis (for Dari\u00e9n and some rural areas east of the Canal Zone)",
                "Routine vaccinations"
            ],
            "notes": "Yellow fever vaccination required for Dari\u00e9n province and if arriving from endemic countries. No malaria in Panama City, Bocas del Toro, or Canal Zone. Dengue risk throughout lowland areas."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink in Panama City and most urban areas. In rural areas, Bocas del Toro, and San Blas, use bottled water.",
        "foodSafetyTips": "Food safety is generally good in Panama City restaurants. Fresh ceviche is popular and safe at reputable places. Be cautious with street food and raw vegetables outside the city.",
        "medicalTourismNote": "Panama is a major medical tourism destination with modern hospitals and US-trained doctors at 40-70% lower costs. Popular for dental, cosmetic, and cardiac procedures.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Panama",
            "Panama Ministry of Health (MINSA)",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Panama. Emergency 911, excellent healthcare in Panama City, pharmacy tips, dengue prevention, and medical tourism information.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Punta Pacifica (Johns Hopkins affiliate)",
                "nearTouristArea": "Panama City (Punta Pacifica, near Casco Viejo)",
                "phone": "+507-204-8000",
                "englishSpeaking": True,
                "notes": "JCI-accredited. Johns Hopkins International affiliate. Excellent care. English-speaking staff."
            },
            {
                "name": "Hospital Nacional",
                "nearTouristArea": "Panama City (Avenida Cuba, near banking district)",
                "phone": "+507-207-8100",
                "englishSpeaking": True,
                "notes": "Major private hospital. Modern facilities. International patient services."
            },
            {
                "name": "Centro M\u00e9dico Paitilla",
                "nearTouristArea": "Panama City (Paitilla, near Cinta Costera)",
                "phone": "+507-265-8800",
                "englishSpeaking": True,
                "notes": "Well-established private hospital. Near waterfront and hotel district."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have diarrhea",
                "local": "Tengo diarrea",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Excellent dental care in Panama City at significantly lower costs than the US.",
            "costRange": "$30-70 for consultation; $50-300 for procedures (all prices in USD)",
            "notes": "Panama is a top dental tourism destination. Many US-trained dentists. Modern clinics.",
            "emergencyTip": "Hospital Punta Pacifica has dental services. Many private dental clinics in Panama City."
        },
        "mentalHealth": {
            "crisisLine": "523-6768 (Mental health crisis line)",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Available in Panama City through international clinics and expat networks.",
            "notes": "Mental health services available in Panama City. Growing expat community has English-speaking therapists."
        },
        "accessibilityInfo": {
            "overview": "Panama City has moderate accessibility in newer areas. Casco Viejo (Old Quarter) has cobblestones. Rural areas have limited accessibility.",
            "hospitalAccess": "Major hospitals are fully accessible.",
            "transport": "Panama Metro is accessible. Accessible taxis can be arranged. Public buses have limited accessibility.",
            "tips": "Panama Canal visitor center is accessible. Casco Viejo has uneven surfaces. Bocas del Toro involves boat access."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Dengue and sun exposure are more relevant health concerns."
        },
        "insuranceClaimProcess": "Private hospitals accept credit cards and may bill insurance directly. Keep all receipts. English documentation available at major hospitals. Panama uses USD so pricing is transparent."
    },
    "GT": {
        "iso2": "GT",
        "countryName": "Guatemala",
        "countrySlug": "guatemala",
        "flag": "\U0001f1ec\U0001f1f9",
        "emergencyNumber": "110 (police), 120 (fire), 128 (ambulance — Red Cross)",
        "healthcareSystem": "Mixed public-private. Public hospitals are under-resourced. Private clinics in Guatemala City and Antigua offer better care. Very limited in rural and indigenous areas.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Guatemala City offer reasonable care. Antigua has some private clinics for tourists. Healthcare in rural areas and near Lake Atitl\u00e1n is very basic. For serious emergencies, evacuation to Guatemala City or Mexico City may be needed.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-8pm. Carolina and Galenica chains have longer hours. Limited in rural areas.",
        "pharmacyTips": "Pharmacies in cities are reasonably stocked. Prices are low. Many medications available without prescription. Staff speak Spanish. Bring essential medications for rural travel around Lake Atitl\u00e1n or Tikal.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "insect repellent"
        ],
        "prescriptionRules": "Many medications available without strict prescription. Controlled substances require documentation.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Possession can result in arrest."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for controlled substances."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging. Bring all essential medications from home.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-45/week",
            "tips": "Travel insurance with medical evacuation is essential. Tikal and Lake Atitl\u00e1n are remote — evacuation to Guatemala City can be costly. Ensure coverage includes altitude sickness and adventure activities."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for extended or rural travel)",
                "Malaria prophylaxis (for lowland areas including Pet\u00e9n/Tikal region)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Malaria risk in lowland areas (Pet\u00e9n, Atlantic coast) — prophylaxis recommended for Tikal visits. Dengue and Zika risk in lowlands. Altitude sickness possible at Lake Atitl\u00e1n (1,560m) and higher areas."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink anywhere in Guatemala. Use bottled water for drinking and brushing teeth. Avoid ice outside of tourist restaurants.",
        "foodSafetyTips": "Eat at established restaurants, especially in Antigua and Guatemala City. Be cautious with street food. Avoid raw vegetables and unpeeled fruits. Food at tourist-oriented restaurants in Antigua is generally safe.",
        "medicalTourismNote": "Guatemala is not a major medical tourism destination. Some dental tourism exists in Guatemala City due to low costs.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Guatemala City",
            "Guatemala Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Guatemala. Emergency numbers, malaria prevention for Tikal, pharmacy tips, water safety, and medical evacuation insurance for Lake Atitl\u00e1n.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Herrera Llerandi",
                "nearTouristArea": "Guatemala City (Zona 10)",
                "phone": "+502-2384-5959",
                "englishSpeaking": True,
                "notes": "Leading private hospital. JCI-accredited. Some English-speaking staff."
            },
            {
                "name": "Centro M\u00e9dico Militar",
                "nearTouristArea": "Guatemala City (Zona 16)",
                "phone": "+502-2380-2000",
                "englishSpeaking": False,
                "notes": "Well-equipped military hospital open to civilians. Good trauma care."
            },
            {
                "name": "Hospital Privado Hermano Pedro",
                "nearTouristArea": "Antigua Guatemala (near Central Park)",
                "phone": "+502-7832-1190",
                "englishSpeaking": False,
                "notes": "Private hospital in the main tourist town. Basic but clean. Spanish only."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un doctor",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have diarrhea",
                "local": "Tengo diarrea",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Guatemala City and Antigua at very low costs.",
            "costRange": "Q100-300 ($13-39) for consultation; Q200-800 ($26-103) for procedures",
            "notes": "Low-cost dental care. Quality varies — use recommended clinics.",
            "emergencyTip": "Hospital Herrera Llerandi has dental services. Private dental clinics in Antigua."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact Hospital de Salud Mental Federico Mora",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some English-speaking therapists in Antigua through expat community.",
            "notes": "Mental health services are very limited. Antigua has some international-oriented therapists."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Cobblestone streets in Antigua, uneven terrain at ruins.",
            "hospitalAccess": "Major hospitals in Guatemala City have basic accessibility.",
            "transport": "No accessible public transport. Private drivers recommended.",
            "tips": "Antigua's cobblestone streets are very challenging for wheelchairs. Tikal involves extensive walking on uneven ground. Lake Atitl\u00e1n requires boat access with steep docks."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at private hospitals in Guatemala City.",
            "notes": "Waterborne diseases, dengue, and malaria (in Pet\u00e9n) are more relevant health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment (cash preferred). Keep all receipts. Documentation primarily in Spanish. Major private hospitals can provide English summaries on request."
    },
    "BO": {
        "iso2": "BO",
        "countryName": "Bolivia",
        "countrySlug": "bolivia",
        "flag": "\U0001f1e7\U0001f1f4",
        "emergencyNumber": "118 (ambulance), 110 (police), 119 (fire)",
        "healthcareSystem": "Public healthcare is free but under-resourced. Private clinics in La Paz, Santa Cruz, and Cochabamba offer better care. Rural healthcare is very basic.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private clinics in La Paz and Santa Cruz offer adequate care for common conditions. Public hospitals are crowded and poorly equipped. ALTITUDE IS A MAJOR HEALTH CONCERN — La Paz sits at 3,640m (11,942ft) and many tourist areas are higher. Medical evacuation may be needed for serious conditions.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-8pm. Limited hours in smaller towns. Rotating duty pharmacies (farmacias de turno) for after-hours.",
        "pharmacyTips": "Pharmacies are reasonably stocked in cities. Many medications available without prescription at low cost. Coca leaves and coca tea (mate de coca) are legal, widely available, and commonly used for altitude sickness. Bring essential medications from home.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "altitude sickness medication (acetazolamide/Diamox)",
            "coca tea (mate de coca)",
            "oral rehydration salts",
            "anti-diarrheals",
            "antihistamines",
            "insect repellent"
        ],
        "prescriptionRules": "Most medications available without prescription. Prices are very low. Controlled substances may require documentation.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal in Bolivia."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation. Bolivia has strict anti-narcotics laws."
            },
            {
                "name": "Coca-derived products",
                "status": "controlled",
                "note": "Coca leaves are legal in Bolivia but ILLEGAL to export. Do not bring coca products home."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging. Bring altitude sickness medication (Diamox/acetazolamide) — consult your doctor before traveling to high-altitude Bolivia.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation and altitude sickness coverage is ESSENTIAL. Evacuation from Uyuni salt flats or remote areas to La Paz or Santa Cruz is expensive. Ensure coverage includes high-altitude trekking."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (required for travel to lowland/Amazon regions; recommended for all travelers)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for rural/Amazon travel)",
                "Malaria prophylaxis (for Amazon lowlands only)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination required for lowland/Amazon areas and recommended for all. No malaria risk above 2,500m. ALTITUDE SICKNESS is the biggest health risk — acclimatize gradually. La Paz (3,640m), Uyuni (3,670m), Potosi (4,090m)."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink anywhere in Bolivia. Use bottled water for drinking and brushing teeth. Avoid ice in drinks. Water purification tablets useful for trekking.",
        "foodSafetyTips": "Eat at established restaurants. Avoid raw vegetables, salads, and unpeeled fruits. Street food (salte\u00f1as, anticuchos) from busy vendors is generally safer. At high altitude, appetite is often reduced — eat light meals and stay hydrated.",
        "medicalTourismNote": "Bolivia is not a medical tourism destination. For specialized treatment, patients travel to Brazil, Argentina, or the US.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy La Paz",
            "Bolivia Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Bolivia. Altitude sickness at 3,640m+, emergency numbers, yellow fever required for lowlands, pharmacy tips, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Cl\u00ednica del Sur",
                "nearTouristArea": "La Paz (Obrajes, accessible from Sopocachi tourist area)",
                "phone": "+591-2-278-4001",
                "englishSpeaking": False,
                "notes": "Leading private clinic in La Paz. Has altitude sickness treatment. Spanish-speaking."
            },
            {
                "name": "Cl\u00ednica Foianini",
                "nearTouristArea": "Santa Cruz (central, near Plaza 24 de Septiembre)",
                "phone": "+591-3-336-2211",
                "englishSpeaking": False,
                "notes": "Best private hospital in Santa Cruz. Modern facilities."
            },
            {
                "name": "Cl\u00ednica Cemes",
                "nearTouristArea": "La Paz (Miraflores)",
                "phone": "+591-2-222-6912",
                "englishSpeaking": False,
                "notes": "Private clinic with emergency services. Altitude sickness treatment available."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I have altitude sickness",
                "local": "Tengo mal de altura / soroche",
                "transliteration": "Spanish (soroche is the Andean term)"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "I can't breathe well",
                "local": "No puedo respirar bien",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care in La Paz and Santa Cruz. Very low cost.",
            "costRange": "Bs 100-300 ($14-43) for consultation; Bs 200-700 ($29-101) for procedures",
            "notes": "Dental care is very affordable. Quality varies — use recommended clinics.",
            "emergencyTip": "Cl\u00ednica del Sur has dental services. Private dental clinics in La Paz."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact hospital emergency departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some in La Paz through international community.",
            "notes": "Mental health services are very limited in Bolivia. Private psychologists available in La Paz."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Streets are uneven, many buildings lack elevators. Altitude adds physical challenge for everyone.",
            "hospitalAccess": "Private clinics have limited accessibility. Most lack proper wheelchair access.",
            "transport": "No accessible public transport. Taxis available but may not be accessible. Roads can be rough.",
            "tips": "Uyuni Salt Flats, Death Road, and Tiwanaku are very challenging for mobility-impaired travelers. The combination of altitude and limited infrastructure makes Bolivia difficult for wheelchair users."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in major cities.",
            "notes": "Altitude sickness is the PRIMARY health concern. Acclimatize for at least 24-48 hours upon arriving at high altitude. Drink coca tea, stay hydrated, avoid alcohol initially."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment in cash (Bolivianos or USD). Keep all receipts. Documentation in Spanish — request English translation if needed. Medical evacuation insurance critical for remote areas."
    },
    "UY": {
        "iso2": "UY",
        "countryName": "Uruguay",
        "countrySlug": "uruguay",
        "flag": "\U0001f1fa\U0001f1fe",
        "emergencyNumber": "911 (unified emergency), 105 (ambulance)",
        "healthcareSystem": "Universal healthcare system (SNIS — Sistema Nacional Integrado de Salud). Mutualistas (private nonprofit hospitals) provide good care. Public hospitals available.",
        "healthcareSystemType": "universal",
        "qualityRating": 4,
        "qualityNotes": "Uruguay has one of the best healthcare systems in South America. Private mutualista hospitals (like Hospital Brit\u00e1nico and Asociaci\u00f3n Espa\u00f1ola) offer excellent care. Public hospitals are adequate. English availability is limited — Spanish skills helpful.",
        "pharmacyAccess": "easy",
        "pharmacyHours": "Pharmacies open 8am-10pm. Rotating duty pharmacies (farmacias de turno) available 24/7.",
        "pharmacyTips": "Pharmacies are well-stocked and well-regulated. Many medications available without prescription. Prices are reasonable. Staff speak Spanish.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "cold medicine",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances and some antibiotics require a prescription.",
        "restrictedMeds": [
            {
                "name": "Cannabis",
                "status": "controlled",
                "note": "Uruguay legalized cannabis for residents, but foreigners CANNOT legally purchase it. Do not attempt to buy or bring cannabis."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-45/week",
            "tips": "Healthcare is more affordable than the US, but travel insurance is still recommended. Private hospital visits cost $50-150."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Uruguay has no malaria or yellow fever risk. One of the safest health destinations in South America."
        },
        "waterSafety": "safe",
        "waterNotes": "Tap water is safe to drink throughout Uruguay.",
        "foodSafetyTips": "Uruguay has good food safety standards. Famous for its beef (asado) — safe at restaurants. Fresh seafood along the coast is excellent. Food safety comparable to Southern European standards.",
        "medicalTourismNote": "Uruguay is not a major medical tourism destination but has quality healthcare at reasonable prices.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Montevideo",
            "Uruguay Ministry of Public Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Uruguay. Emergency numbers (911/105), excellent healthcare system, safe tap water, pharmacy tips, and cannabis laws for tourists.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Brit\u00e1nico",
                "nearTouristArea": "Montevideo (Tres Cruces, near Ciudad Vieja)",
                "phone": "+598-2487-1020",
                "englishSpeaking": True,
                "notes": "Uruguay's most prestigious private hospital. Some English-speaking staff. International patient services."
            },
            {
                "name": "Asociaci\u00f3n Espa\u00f1ola",
                "nearTouristArea": "Montevideo (Tres Cruces)",
                "phone": "+598-2480-8020",
                "englishSpeaking": False,
                "notes": "Large private mutualista hospital. Good quality care. Spanish-speaking."
            },
            {
                "name": "Hospital de Punta del Este (Cantegril)",
                "nearTouristArea": "Punta del Este (resort area)",
                "phone": "+598-4249-4133",
                "englishSpeaking": False,
                "notes": "Main hospital serving the beach resort area. Handles tourist medical needs during summer season."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito un remedio para el dolor de cabeza",
                "transliteration": "Spanish (Rioplatense dialect)"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Good dental care in Montevideo at moderate costs.",
            "costRange": "UYU 1,500-3,500 ($35-80) for consultation; UYU 3,000-10,000 ($70-230) for procedures",
            "notes": "Quality dental care available. Dentists well-trained.",
            "emergencyTip": "Hospital Brit\u00e1nico has dental services. Private dental clinics in Montevideo."
        },
        "mentalHealth": {
            "crisisLine": "0800-0767 (L\u00ednea de Prevenci\u00f3n del Suicidio)",
            "internationalLine": "Contact your embassy for English-speaking referrals",
            "englishTherapists": "Limited. Some available in Montevideo.",
            "notes": "Mental health services available in Montevideo. Uruguay has progressive mental health legislation."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is moderate in Montevideo. Improving but still limited in many areas.",
            "hospitalAccess": "Major hospitals are wheelchair accessible.",
            "transport": "Some accessible buses in Montevideo. Taxis available.",
            "tips": "Montevideo's Ciudad Vieja has uneven sidewalks. Punta del Este beach areas may have limited wheelchair access. Colonia del Sacramento has cobblestones."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals and clinics.",
            "notes": "Uruguay is one of the safest health destinations in South America."
        },
        "insuranceClaimProcess": "Private hospitals accept credit cards. Keep all receipts. Documentation in Spanish. Major hospitals can provide English summaries on request."
    },
    "PY": {
        "iso2": "PY",
        "countryName": "Paraguay",
        "countrySlug": "paraguay",
        "flag": "\U0001f1f5\U0001f1fe",
        "emergencyNumber": "911 (unified emergency)",
        "healthcareSystem": "Mixed public-private. Public hospitals are under-resourced. Private clinics in Asunci\u00f3n offer better care.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Asunci\u00f3n provide adequate care. Public hospitals are overcrowded and poorly equipped. Healthcare outside the capital is very limited. For serious conditions, patients often travel to Buenos Aires.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-8pm in cities. Some 24/7 options in Asunci\u00f3n.",
        "pharmacyTips": "Pharmacies in Asunci\u00f3n are reasonably stocked. Many medications available without prescription at low cost. Staff speak Spanish and sometimes Guaran\u00ed.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "insect repellent"
        ],
        "prescriptionRules": "Many medications available without prescription. Prices are very low. Quality control can be inconsistent.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "controlled",
                "note": "Medical cannabis has some legal framework. Recreational use is illegal."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for controlled substances."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-40/week",
            "tips": "Travel insurance with medical evacuation recommended. Serious cases may require evacuation to Buenos Aires."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (recommended for all travelers; required if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for rural travel)",
                "Routine vaccinations"
            ],
            "notes": "Yellow Fever vaccination recommended for all travelers. Dengue risk exists — use insect repellent. No malaria risk."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water quality varies. Safe in Asunci\u00f3n but use bottled water in rural areas. Bottled water widely available.",
        "foodSafetyTips": "Eat at established restaurants. Paraguayan cuisine (chipa, sopa paraguaya) is generally safe when fresh. Be cautious with street food and raw vegetables.",
        "medicalTourismNote": "Paraguay is not a medical tourism destination. Ciudad del Este on the Brazilian border has some lower-cost medical services.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Asunci\u00f3n",
            "Paraguay Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Paraguay. Emergency 911, pharmacy tips, yellow fever vaccination, dengue prevention, and travel insurance advice.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Sanatorio Migone Batt\u00e9",
                "nearTouristArea": "Asunci\u00f3n (center, near Panteón de los Héroes)",
                "phone": "+595-21-498-200",
                "englishSpeaking": False,
                "notes": "Leading private hospital in Asunci\u00f3n. Modern facilities. Spanish and Guaraní spoken."
            },
            {
                "name": "Hospital Italiano",
                "nearTouristArea": "Asunci\u00f3n (center)",
                "phone": "+595-21-200-144",
                "englishSpeaking": False,
                "notes": "Well-regarded private hospital. Spanish-speaking."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito remedio para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un m\u00e9dico",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I feel sick",
                "local": "Che ras\u1ef5",
                "transliteration": "Guaran\u00ed (widely spoken)"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Asunci\u00f3n at very low cost.",
            "costRange": "PYG 150,000-400,000 ($20-53) for consultation; PYG 300,000-1,000,000 ($40-133) for procedures",
            "notes": "Very affordable dental care. Quality varies.",
            "emergencyTip": "Sanatorio Migone has dental services. Private dental clinics in Asunci\u00f3n."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact hospital emergency departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some in Asunci\u00f3n.",
            "notes": "Mental health services are limited in Paraguay."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Infrastructure is challenging.",
            "hospitalAccess": "Private hospitals have some accessibility.",
            "transport": "No accessible public transport. Private transport recommended.",
            "tips": "Asunci\u00f3n city center has uneven sidewalks. Tourist infrastructure is developing."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals.",
            "notes": "Dengue and heat-related illness are more relevant concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment. Keep all receipts. Documentation in Spanish."
    },
    "HN": {
        "iso2": "HN",
        "countryName": "Honduras",
        "countrySlug": "honduras",
        "flag": "\U0001f1ed\U0001f1f3",
        "emergencyNumber": "911 (unified emergency), 195 (Red Cross ambulance), 199 (fire)",
        "healthcareSystem": "Public healthcare is limited. Private hospitals in Tegucigalpa and San Pedro Sula offer better care. Very limited on Bay Islands (Roat\u00e1n).",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Tegucigalpa and San Pedro Sula provide adequate care. Healthcare on Roat\u00e1n and other Bay Islands is very limited — serious cases require evacuation to the mainland or US. Public hospitals are under-resourced.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-7pm. Limited in rural areas and smaller islands.",
        "pharmacyTips": "Pharmacies in cities are reasonably stocked. Many medications available without prescription at low cost. Bring essential medications for island travel. Staff speak Spanish.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "insect repellent",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require documentation.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Strict enforcement."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging. Bring all medications needed for Roat\u00e1n/Bay Islands travel.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$25-50/week",
            "tips": "Travel insurance with medical evacuation is ESSENTIAL, especially for Roat\u00e1n and Bay Islands. Diving decompression chamber on Roat\u00e1n but serious cases need evacuation. Ensure coverage includes diving and water sports."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Malaria prophylaxis (for some mainland areas — NOT Roat\u00e1n)",
                "Rabies (for extended rural travel)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Malaria risk in some mainland lowland areas but NOT on Bay Islands. Dengue and Zika risk throughout. Hurricane season (June-November) can disrupt medical services."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink. Use bottled water for drinking and brushing teeth. On Roat\u00e1n, most resorts provide filtered water.",
        "foodSafetyTips": "Eat at established restaurants. Be cautious with street food. Baleadas (traditional dish) from busy vendors are generally safe. Seafood on the coast is usually fresh and safe at restaurants. Avoid raw shellfish from beach vendors.",
        "medicalTourismNote": "Honduras is not a medical tourism destination.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Tegucigalpa",
            "Honduras Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for Honduras and Roat\u00e1n. Emergency numbers, diving safety, dengue prevention, hurricane season health risks, and medical evacuation insurance for Bay Islands.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Honduras Medical Center",
                "nearTouristArea": "Tegucigalpa (Colonia Lomas del Guijarro)",
                "phone": "+504-2216-1100",
                "englishSpeaking": False,
                "notes": "Leading private hospital. Modern facilities. Spanish-speaking."
            },
            {
                "name": "Hospital del Valle",
                "nearTouristArea": "San Pedro Sula (near city center)",
                "phone": "+504-2516-0142",
                "englishSpeaking": False,
                "notes": "Private hospital. Serves San Pedro Sula area."
            },
            {
                "name": "Clinica Esperanza / Pegasus Foundation",
                "nearTouristArea": "Roat\u00e1n (Sandy Bay / West End area)",
                "phone": "+504-9632-3566",
                "englishSpeaking": True,
                "notes": "Nonprofit clinic on Roat\u00e1n. English-speaking. Basic services — serious cases need evacuation."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un doctor",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Tegucigalpa and San Pedro Sula at very low cost.",
            "costRange": "L 500-1,500 ($20-60) for consultation; L 1,000-5,000 ($40-200) for procedures",
            "notes": "Very affordable dental care. Quality varies.",
            "emergencyTip": "Hospital Honduras Medical Center has dental services."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact hospital emergency departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some on Roat\u00e1n through expat community.",
            "notes": "Mental health services are very limited in Honduras."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited throughout Honduras.",
            "hospitalAccess": "Private hospitals have basic accessibility.",
            "transport": "No accessible public transport. Private transport recommended.",
            "tips": "Roat\u00e1n beaches and dive sites have limited accessibility. Some resorts offer accessible rooms. Copan ruins involve walking on uneven ground."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in major cities.",
            "notes": "Dengue, diving-related decompression sickness (Roat\u00e1n), and hurricane season are more relevant health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment (cash or card). Keep all receipts. Documentation in Spanish. On Roat\u00e1n, basic clinic services may accept USD."
    },
    "SV": {
        "iso2": "SV",
        "countryName": "El Salvador",
        "countrySlug": "el-salvador",
        "flag": "\U0001f1f8\U0001f1fb",
        "emergencyNumber": "911 (unified emergency), 132 (fire)",
        "healthcareSystem": "Public healthcare through ISSS and public hospitals. Private hospitals in San Salvador offer better care. Rural healthcare is limited.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in San Salvador provide adequate care. Public hospitals are overcrowded. Healthcare outside the capital is limited. For serious emergencies, evacuation to Guatemala City or the US may be needed.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-8pm. Some chains have longer hours.",
        "pharmacyTips": "Pharmacies are reasonably stocked. Many medications available without prescription at low cost. El Salvador uses the US dollar. Staff speak Spanish.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "insect repellent",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require documentation.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Strict enforcement."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-45/week",
            "tips": "Travel insurance with medical evacuation recommended. Ensure coverage includes surfing and water sports (El Salvador is a popular surf destination)."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for extended rural travel)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Dengue and Zika risk — use insect repellent. No malaria in El Salvador."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink in most of El Salvador. Use bottled water for drinking and brushing teeth.",
        "foodSafetyTips": "Eat at established restaurants. Pupusas (national dish) from busy vendors are generally safe when freshly made. Be cautious with raw vegetables and unpeeled fruits.",
        "medicalTourismNote": "El Salvador is not a major medical tourism destination but offers affordable dental and medical care in San Salvador.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy San Salvador",
            "El Salvador Ministry of Health",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to El Salvador. Emergency 911, pharmacy tips, dengue prevention, surf safety, and travel insurance for adventure activities.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital de Diagn\u00f3stico Escalon",
                "nearTouristArea": "San Salvador (Colonia Escal\u00f3n)",
                "phone": "+503-2264-4422",
                "englishSpeaking": False,
                "notes": "Leading private hospital. Modern facilities. Spanish-speaking."
            },
            {
                "name": "Hospital de la Mujer",
                "nearTouristArea": "San Salvador (Boulevard de los H\u00e9roes area)",
                "phone": "+503-2226-3086",
                "englishSpeaking": False,
                "notes": "Private hospital with good reputation. Central location."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un doctor",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have a sunburn",
                "local": "Tengo una quemadura de sol",
                "transliteration": "Spanish"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in San Salvador at very affordable prices.",
            "costRange": "$20-50 for consultation; $30-150 for procedures (USD — El Salvador uses US dollars)",
            "notes": "Very affordable dental care. Some dental tourism exists.",
            "emergencyTip": "Hospital de Diagn\u00f3stico has dental services."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact hospital psychiatric departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some in San Salvador.",
            "notes": "Mental health services are limited in El Salvador."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Infrastructure is challenging.",
            "hospitalAccess": "Private hospitals have basic accessibility.",
            "transport": "No accessible public transport. Private transport recommended.",
            "tips": "Surf beaches have limited accessibility. San Salvador has uneven sidewalks. Newer malls and hotels are more accessible."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at private hospitals.",
            "notes": "Dengue and surf-related injuries are more relevant health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment in USD. Keep all receipts. Documentation in Spanish."
    },
    "FJ": {
        "iso2": "FJ",
        "countryName": "Fiji",
        "countrySlug": "fiji",
        "flag": "\U0001f1eb\U0001f1ef",
        "emergencyNumber": "911 (police, fire, ambulance)",
        "healthcareSystem": "Public healthcare available but limited. Private clinics in Suva and Nadi area serve tourists. Very limited on outer islands.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Basic healthcare in Suva and Nadi/Denarau area. The Colonial War Memorial Hospital in Suva is the main facility. Private clinics in tourist areas handle common issues. Outer islands have minimal medical facilities. Serious cases require evacuation to Suva, New Zealand, or Australia.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies open 8am-6pm weekdays, shorter on Saturday. Very limited on outer islands.",
        "pharmacyTips": "Pharmacies in Suva and Nadi are reasonably stocked. Bring ALL medications you need for island travel. Staff speak English. Limited pharmacy options on outer islands.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "oral rehydration salts",
            "insect repellent",
            "sunscreen",
            "anti-diarrheals"
        ],
        "prescriptionRules": "Prescription required for many medications. Basic medications available OTC. English spoken — communication is easy.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal in Fiji. Strict enforcement."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation for opioid medications."
            },
            {
                "name": "Pseudoephedrine (Sudafed)",
                "status": "restricted",
                "note": "Restricted quantities. Declare at customs."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing all medications. Keep in original packaging. English documentation is fine — Fiji is English-speaking. Bring all medications for outer island stays.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$30-55/week",
            "tips": "Travel insurance with medical evacuation is ESSENTIAL. Evacuation from outer islands to Suva and potentially to New Zealand or Australia can cost $20,000-50,000+. Ensure coverage includes water sports, diving, and cyclone-related emergencies."
        },
        "vaccinations": {
            "required": [
                "Yellow Fever (if arriving from endemic area)"
            ],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Routine vaccinations"
            ],
            "notes": "No special vaccinations required for most travelers. Dengue fever risk exists — use insect repellent. No malaria in Fiji. Cyclone season (November-April) can disrupt medical services."
        },
        "waterSafety": "caution",
        "waterNotes": "Tap water is generally safe in Suva and Nadi. On outer islands, use bottled or filtered water. Resorts provide safe drinking water. After cyclones or heavy rain, water quality may be affected.",
        "foodSafetyTips": "Food is generally safe at resorts and established restaurants. Fresh seafood is excellent. Be cautious with raw fish (kokoda) from informal vendors. Avoid reef fish from unverified sources (ciguatera fish poisoning risk).",
        "medicalTourismNote": "Fiji is not a medical tourism destination. For specialized treatment, Fijians travel to New Zealand or Australia.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Suva",
            "Fiji Ministry of Health and Medical Services",
            "WHO Western Pacific"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Fiji. Emergency 911, island health tips, dengue prevention, ciguatera fish warning, cyclone season risks, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Colonial War Memorial Hospital (CWMH)",
                "nearTouristArea": "Suva (city center)",
                "phone": "+679-331-3444",
                "englishSpeaking": True,
                "notes": "Fiji's main hospital. Public facility. Basic but largest in the country."
            },
            {
                "name": "Nadi Hospital",
                "nearTouristArea": "Nadi (near airport and Denarau Island)",
                "phone": "+679-670-1128",
                "englishSpeaking": True,
                "notes": "Public hospital serving the main tourist gateway area."
            },
            {
                "name": "Oceania Hospitals",
                "nearTouristArea": "Suva (Laucala Bay)",
                "phone": "+679-330-5768",
                "englishSpeaking": True,
                "notes": "Private hospital with modern facilities. Best private option in Fiji."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Au via na wainimate ni ulu",
                "transliteration": "Fijian (English is official and widely spoken)"
            },
            {
                "english": "I need a doctor",
                "local": "Au via na vuniwai",
                "transliteration": "Fijian"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "Evei na farmasi e voleka?",
                "transliteration": "Fijian (English widely understood)"
            }
        ],
        "dentalCare": {
            "availability": "Basic dental care in Suva and Nadi. Very limited on outer islands.",
            "costRange": "FJD 50-150 ($22-67) for consultation; FJD 100-400 ($44-178) for procedures",
            "notes": "Dental care is basic. Resolve dental issues before traveling to Fiji.",
            "emergencyTip": "Colonial War Memorial Hospital has a dental clinic. Private dentists available in Suva."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact St. Giles Hospital psychiatric services: +679-332-1404",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Limited but available in Suva. English is official.",
            "notes": "Mental health services are limited in Fiji. St. Giles Hospital is the main psychiatric facility."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is limited. Island terrain, beach access, and older buildings present challenges.",
            "hospitalAccess": "Hospitals have basic accessibility.",
            "transport": "No accessible public transport. Resort transfers can be arranged. Boat access to islands is not wheelchair accessible.",
            "tips": "Resorts on Denarau Island are more accessible than outer island resorts. Beach wheelchairs may be available at some resorts. Inform resorts of accessibility needs well in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in Suva and Nadi.",
            "notes": "Dengue, cyclone-related health risks (Nov-Apr), and marine hazards (reef cuts, jellyfish) are more relevant concerns."
        },
        "insuranceClaimProcess": "Hospitals may require upfront payment. Keep all receipts. English documentation provided. Resort medical clinics can assist with insurance paperwork. Medical evacuation insurance is critical for outer islands."
    },
    "NI": {
        "iso2": "NI",
        "countryName": "Nicaragua",
        "countrySlug": "nicaragua",
        "flag": "\U0001f1f3\U0001f1ee",
        "emergencyNumber": "118 (fire), 128 (Red Cross ambulance), 118 (police)",
        "healthcareSystem": "Public healthcare available but limited. Private hospitals in Managua offer better care. Very limited in rural areas and on Corn Islands.",
        "healthcareSystemType": "mixed",
        "qualityRating": 2,
        "qualityNotes": "Private hospitals in Managua provide adequate care for common conditions. Public hospitals are severely under-resourced. Healthcare in rural areas, San Juan del Sur, and Corn Islands is very basic. Serious cases may require evacuation to Costa Rica or the US.",
        "pharmacyAccess": "moderate",
        "pharmacyHours": "Pharmacies in cities open 8am-8pm. Limited in rural areas and beach towns.",
        "pharmacyTips": "Pharmacies in Managua are reasonably stocked. Many medications available without prescription at very low cost. Bring essential medications for travel to Corn Islands, Ometepe, and rural areas. Staff speak Spanish.",
        "commonOTC": [
            "paracetamol",
            "ibuprofen",
            "antihistamines",
            "antacids",
            "anti-diarrheals",
            "oral rehydration salts",
            "insect repellent",
            "sunscreen"
        ],
        "prescriptionRules": "Many medications available without prescription. Controlled substances require documentation. Prices are very low.",
        "restrictedMeds": [
            {
                "name": "Cannabis/CBD products",
                "status": "banned",
                "note": "Illegal. Strict penalties."
            },
            {
                "name": "Narcotic medications",
                "status": "controlled",
                "note": "Carry documentation."
            }
        ],
        "bringDocumentation": "Carry a doctor's letter listing medications. Spanish translation helpful. Keep medications in original packaging. Bring all medications you'll need.",
        "travelInsurance": {
            "recommended": True,
            "required": False,
            "requiredNote": "",
            "averageCost": "$20-45/week",
            "tips": "Travel insurance with medical evacuation is essential. Evacuation from Corn Islands or rural areas to Managua or Costa Rica can be costly. Ensure coverage includes surfing and volcano activities."
        },
        "vaccinations": {
            "required": [],
            "recommended": [
                "Hepatitis A",
                "Hepatitis B",
                "Typhoid",
                "Rabies (for extended rural travel)",
                "Malaria prophylaxis (for some rural areas — check CDC recommendations)",
                "Routine vaccinations"
            ],
            "notes": "No mandatory vaccinations. Dengue and Zika risk throughout — use insect repellent. Some malaria risk in rural areas. Hurricane season (June-November) can disrupt services."
        },
        "waterSafety": "bottled-only",
        "waterNotes": "Tap water is NOT safe to drink in most of Nicaragua. Use bottled water. Some better hotels may have filtered water but bottled is safest.",
        "foodSafetyTips": "Eat at established restaurants. Gallo pinto (rice and beans) and vigorón are safe when freshly cooked. Be cautious with street food, raw vegetables, and ice. In San Juan del Sur and Granada tourist restaurants, food is generally safe.",
        "medicalTourismNote": "Nicaragua is not a medical tourism destination.",
        "sources": [
            "CDC Travelers' Health",
            "US Embassy Managua",
            "Nicaragua Ministry of Health (MINSA)",
            "WHO"
        ],
        "lastUpdated": "2026-04-08",
        "metaDescription": "Complete health & medication guide for traveling to Nicaragua. Emergency numbers, dengue prevention, pharmacy tips, volcano safety, hurricane season health risks, and medical evacuation insurance.",
        "datePublished": "2026-04-08",
        "eu112": False,
        "hospitals": [
            {
                "name": "Hospital Metropolitano Vivian Pellas",
                "nearTouristArea": "Managua (Carretera a Masaya km 9.5)",
                "phone": "+505-2255-6900",
                "englishSpeaking": True,
                "notes": "Nicaragua's best hospital. Modern facilities. Some English-speaking staff. International patient services."
            },
            {
                "name": "Hospital Bautista",
                "nearTouristArea": "Managua (near city center)",
                "phone": "+505-2264-9020",
                "englishSpeaking": False,
                "notes": "Well-regarded private hospital. Spanish-speaking."
            }
        ],
        "pharmacyPhrases": [
            {
                "english": "I need medicine for a headache",
                "local": "Necesito medicina para el dolor de cabeza",
                "transliteration": "Spanish"
            },
            {
                "english": "I need a doctor",
                "local": "Necesito un doctor",
                "transliteration": "Spanish"
            },
            {
                "english": "Where is the nearest pharmacy?",
                "local": "\u00bfD\u00f3nde est\u00e1 la farmacia m\u00e1s cercana?",
                "transliteration": "Spanish"
            },
            {
                "english": "I have been stung by a jellyfish",
                "local": "Me pic\u00f3 una medusa / aguamala",
                "transliteration": "Spanish (aguamala is the Central American term)"
            }
        ],
        "dentalCare": {
            "availability": "Dental care available in Managua at very low cost.",
            "costRange": "C$500-1,500 ($14-41) for consultation; C$1,000-5,000 ($27-137) for procedures",
            "notes": "Very affordable dental care. Quality varies. Managua has the best options.",
            "emergencyTip": "Hospital Vivian Pellas has dental services."
        },
        "mentalHealth": {
            "crisisLine": "Not widely established — contact hospital emergency departments",
            "internationalLine": "Contact your embassy for referrals",
            "englishTherapists": "Very limited. Some in Granada and San Juan del Sur through expat community.",
            "notes": "Mental health services are very limited in Nicaragua."
        },
        "accessibilityInfo": {
            "overview": "Accessibility is very limited. Infrastructure is challenging for wheelchair users.",
            "hospitalAccess": "Hospital Vivian Pellas has modern accessibility features.",
            "transport": "No accessible public transport. Private transport recommended.",
            "tips": "Colonial cities (Granada, Le\u00f3n) have cobblestone streets. Volcanoes are not wheelchair accessible. Some beach hotels have accessible rooms — inquire directly."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Available at hospitals in Managua.",
            "notes": "Dengue, waterborne diseases, and hurricane season (June-November) are more relevant health concerns."
        },
        "insuranceClaimProcess": "Hospitals require upfront payment (local currency or USD). Keep all receipts. Hospital Vivian Pellas can provide English documentation. Other facilities provide Spanish-only documentation."
    }
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for iso2, data in COUNTRIES.items():
        filepath = os.path.join(OUTPUT_DIR, f"{iso2}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Written: {filepath}")

    print(f"\nDone! Generated {len(COUNTRIES)} health data files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
