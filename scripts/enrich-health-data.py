#!/usr/bin/env python3
"""
enrich-health-data.py — Add new content sections to all 50 health data JSON files.

Adds: hospitals, pharmacyPhrases, dentalCare, mentalHealth, accessibilityInfo,
      covidStatus, insuranceClaimProcess, datePublished, eu112
Also fixes: Brazil insurance required:true, normalizes waterSafety values

Usage:
    python3 scripts/enrich-health-data.py          # enrich all
    python3 scripts/enrich-health-data.py JP        # enrich single country
"""

import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "health-data"

# ── Per-country enrichment data ──────────────────────────────────────────

ENRICHMENT = {
    "JP": {
        "hospitals": [
            {"name": "St. Luke's International Hospital", "nearTouristArea": "Tsukiji / Ginza, Tokyo", "phone": "+81-3-3541-5151", "englishSpeaking": True, "notes": "Full international department. Major credit cards accepted."},
            {"name": "Tokyo Midtown Medical Center", "nearTouristArea": "Roppongi, Tokyo", "phone": "+81-3-5413-0080", "englishSpeaking": True, "notes": "Walk-in clinic for travelers. Popular among expats."},
            {"name": "Osaka International Clinic", "nearTouristArea": "Central Osaka / Dotonbori", "phone": "+81-6-6120-3500", "englishSpeaking": True, "notes": "English-first clinic for tourists and expats."},
            {"name": "Kameda Medical Center", "nearTouristArea": "Kamogawa (day trip from Tokyo)", "phone": "+81-4-7092-2211", "englishSpeaking": True, "notes": "One of Japan's top-ranked hospitals. International patient services."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "頭痛の薬をください", "transliteration": "Zutsuu no kusuri wo kudasai"},
            {"english": "I have a stomachache", "local": "お腹が痛いです", "transliteration": "Onaka ga itai desu"},
            {"english": "I'm allergic to...", "local": "…にアレルギーがあります", "transliteration": "...ni arerugii ga arimasu"},
            {"english": "Where is the nearest pharmacy?", "local": "一番近い薬局はどこですか？", "transliteration": "Ichiban chikai yakkyoku wa doko desu ka?"},
            {"english": "I need a doctor", "local": "医者に診てもらいたいです", "transliteration": "Isha ni mite moraitai desu"},
        ],
        "dentalCare": {
            "availability": "Excellent dental care available in major cities. Many dental clinics in Tokyo and Osaka have English-speaking dentists.",
            "costRange": "¥3,000-10,000 ($20-70) for a basic consultation; ¥10,000-50,000 ($70-350) for fillings or extractions",
            "notes": "Japanese dental care is technically excellent. International clinics in Tokyo (Tokyo Dental Clinic, Mori Dental) cater to English speakers.",
            "emergencyTip": "For dental emergencies, visit a hospital emergency department. Most dental clinics are closed on Sundays and holidays. Call the Tokyo Medical Information Service at 03-5285-8181 for referrals."
        },
        "mentalHealth": {
            "crisisLine": "0570-064-556 (Yorisoi Hotline — multilingual support, 24/7)",
            "internationalLine": "TELL Lifeline: 03-5774-0992 (English-language counseling in Tokyo)",
            "englishTherapists": "Available in Tokyo and Osaka through TELL (Tokyo English Life Line) and international clinics. Expect ¥10,000-25,000 per session.",
            "notes": "Mental health services in English are limited outside major cities. TELL offers phone and in-person counseling. Many international clinics in Tokyo have psychiatrists."
        },
        "accessibilityInfo": {
            "overview": "Japan has good accessibility infrastructure, especially in major cities. Trains, stations, and public buildings are generally wheelchair accessible.",
            "hospitalAccess": "Major hospitals are wheelchair accessible with accessible restrooms. International hospitals have multilingual accessibility support.",
            "transport": "JR trains and major subway lines have elevators and priority seating. Accessible taxis (UD taxis) available in Tokyo. Wheelchair ramps at most stations.",
            "tips": "Request accessible rooms in advance. The Japan Accessible Tourism Center (accessible-japan.com) provides detailed guides. Sidewalks in older areas may have obstacles."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry as of 2026.",
            "maskPolicy": "Masks are no longer required but remain common in healthcare settings and crowded trains. Many Japanese people continue to wear masks voluntarily.",
            "testing": "PCR tests available at clinics and airports. Cost: ¥15,000-30,000 ($100-200) at private clinics.",
            "notes": "Japan lifted all COVID entry restrictions in 2023. Healthcare facilities may still require masks."
        },
        "insuranceClaimProcess": "Japanese hospitals typically require upfront payment. Keep all receipts (ryoshusho) and ask for an English medical certificate (shindan-sho). Many hospitals can provide documentation in English at international departments. File claims with your insurer within 30 days of treatment.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "AT": {
        "hospitals": [
            {"name": "Allgemeines Krankenhaus Wien (AKH)", "nearTouristArea": "Central Vienna / Ringstrasse", "phone": "+43-1-40400-0", "englishSpeaking": True, "notes": "Vienna's main university hospital. One of Europe's largest. Full emergency department."},
            {"name": "Privatklinik Döbling", "nearTouristArea": "Vienna / Schönbrunn area", "phone": "+43-1-36066-0", "englishSpeaking": True, "notes": "Private hospital with shorter wait times. English-speaking staff."},
            {"name": "Landeskrankenhaus Salzburg", "nearTouristArea": "Salzburg Old Town", "phone": "+43-5-7255-0", "englishSpeaking": True, "notes": "Regional hospital near Salzburg's tourist center."},
            {"name": "Universitätsklinik Innsbruck", "nearTouristArea": "Innsbruck / Ski resorts", "phone": "+43-512-504-0", "englishSpeaking": True, "notes": "Excellent for mountain/ski injuries. University hospital with trauma center."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ich brauche Medizin gegen Kopfschmerzen", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Ich habe Bauchschmerzen", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Ich bin allergisch gegen...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Wo ist die nächste Apotheke?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Ich brauche einen Arzt", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Excellent dental care available throughout Austria. EU citizens can access emergency dental care with EHIC.",
            "costRange": "€50-100 for a consultation; €80-250 for fillings; €100-300 for extractions",
            "notes": "Austrian dental care is high quality. Many dentists in Vienna and tourist areas speak English. Dental tourism is growing due to lower costs than Germany or Switzerland.",
            "emergencyTip": "For dental emergencies outside business hours, call the Zahnärztlicher Notdienst (dental emergency service) at 01-512-20-78 in Vienna. Hospital emergency departments can provide pain relief."
        },
        "mentalHealth": {
            "crisisLine": "142 (Telefonseelsorge — 24/7 crisis line, German-language)",
            "internationalLine": "Crisis Text Line: text HOME to 741741 (English)",
            "englishTherapists": "English-speaking therapists available in Vienna through international practices. Check Psychology Today's international directory.",
            "notes": "Austria has good mental healthcare but services in English are mainly available in Vienna. Most therapists work by appointment. ÖGK (public insurance) covers some therapy sessions for residents."
        },
        "accessibilityInfo": {
            "overview": "Austria has solid accessibility infrastructure. Major cities comply with EU accessibility standards. Historic buildings may have limited access.",
            "hospitalAccess": "Modern hospitals are fully wheelchair accessible. Older clinics in historic buildings may have limited access.",
            "transport": "Vienna's U-Bahn is fully wheelchair accessible. ÖBB trains offer accessible carriages. Taxis with wheelchair access available by request.",
            "tips": "Book accessible accommodations in advance, especially in alpine areas. Ski resorts often have adaptive skiing programs. Vienna's tourist office provides accessibility guides."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates in public spaces. Masks may be required in healthcare facilities during respiratory illness season.",
            "testing": "PCR and antigen tests available at pharmacies and clinics. Cost: €25-80 for PCR.",
            "notes": "Austria lifted all COVID restrictions. Healthcare facilities may have seasonal mask requirements."
        },
        "insuranceClaimProcess": "EU citizens with EHIC receive emergency care at public hospitals at no upfront cost. Non-EU travelers: keep all Rechnung (invoices) and Befund (medical reports). Request English documentation. Private clinics may require payment upfront — get an itemized invoice for insurance claims.",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    "AU": {
        "hospitals": [
            {"name": "Royal Melbourne Hospital", "nearTouristArea": "Melbourne CBD / Federation Square", "phone": "+61-3-9342-7000", "englishSpeaking": True, "notes": "Major public teaching hospital. Full emergency department."},
            {"name": "St Vincent's Hospital Sydney", "nearTouristArea": "Darlinghurst / Sydney CBD", "phone": "+61-2-8382-1111", "englishSpeaking": True, "notes": "Close to Bondi and city center. Emergency department."},
            {"name": "Royal Prince Alfred Hospital", "nearTouristArea": "Camperdown, Sydney", "phone": "+61-2-9515-6111", "englishSpeaking": True, "notes": "One of Australia's top hospitals."},
            {"name": "Cairns Hospital", "nearTouristArea": "Great Barrier Reef / Cairns", "phone": "+61-7-4226-0000", "englishSpeaking": True, "notes": "Nearest major hospital to Great Barrier Reef. Hyperbaric chamber for diving injuries."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "I need medicine for a headache", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Where is the nearest chemist?", "transliteration": "Australians say 'chemist' not 'pharmacy'"},
        ],
        "dentalCare": {
            "availability": "Excellent dental care but expensive. Medicare does not cover dental for most adults. Private dental clinics widely available.",
            "costRange": "AUD $60-100 for a consultation; AUD $150-350 for fillings; AUD $200-400 for extractions",
            "notes": "Dental care in Australia is among the most expensive in the world. Emergency dental is available at hospital emergency departments for severe pain/trauma.",
            "emergencyTip": "For dental emergencies, visit a hospital emergency department or call the Australian Dental Association hotline. After-hours dental clinics exist in major cities."
        },
        "mentalHealth": {
            "crisisLine": "Lifeline: 13 11 14 (24/7 crisis support)",
            "internationalLine": "Beyond Blue: 1300 22 4636 (anxiety and depression support)",
            "englishTherapists": "Widely available. Psychologists and counselors accessible through GP referral or directly.",
            "notes": "Australia has excellent mental health services. Headspace centers for young people (12-25) in most cities. Telehealth counseling widely available."
        },
        "accessibilityInfo": {
            "overview": "Australia has strong disability discrimination laws. Major cities are generally wheelchair accessible with accessible public transport.",
            "hospitalAccess": "All major hospitals are fully wheelchair accessible with accessible parking and restrooms.",
            "transport": "Trains and buses in major cities are wheelchair accessible. Accessible taxis available through booking services. Sydney ferries have wheelchair access.",
            "tips": "National parks have varying accessibility — check Parks Australia for specific trail accessibility. The Companion Card scheme provides free entry for carers at participating venues."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Masks may be requested in healthcare settings.",
            "testing": "RATs available at pharmacies ($5-15 AUD). PCR tests available at pathology clinics.",
            "notes": "All COVID entry restrictions removed. Healthcare facilities may have their own mask policies."
        },
        "insuranceClaimProcess": "Australian public hospitals charge international visitors significant fees (emergency department visit from AUD $500+). Keep all receipts and medical documentation. Request itemized invoices. Most travel insurers have Australian partnerships for direct billing — call your insurer before treatment if possible.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "BR": {
        "hospitals": [
            {"name": "Hospital Israelita Albert Einstein", "nearTouristArea": "Morumbi, São Paulo", "phone": "+55-11-2151-1233", "englishSpeaking": True, "notes": "JCI-accredited. Brazil's top-rated private hospital. International patient department."},
            {"name": "Hospital Copa D'Or", "nearTouristArea": "Copacabana, Rio de Janeiro", "phone": "+55-21-2545-3600", "englishSpeaking": True, "notes": "Private hospital near Copacabana and Ipanema beaches. English-speaking staff."},
            {"name": "Hospital Samaritano", "nearTouristArea": "Botafogo, Rio de Janeiro", "phone": "+55-21-2537-9722", "englishSpeaking": True, "notes": "Close to Sugarloaf Mountain. Good emergency department."},
            {"name": "Hospital Moinhos de Vento", "nearTouristArea": "Porto Alegre", "phone": "+55-51-3314-3434", "englishSpeaking": True, "notes": "JCI-accredited hospital in southern Brazil."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Preciso de remédio para dor de cabeça", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Estou com dor de estômago", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Sou alérgico(a) a...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Onde fica a farmácia mais próxima?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Preciso de um médico", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Brazil is world-renowned for dental care. Private dental clinics widely available and affordable compared to the US.",
            "costRange": "R$100-300 ($20-60) for a consultation; R$200-600 ($40-120) for fillings; R$300-800 ($60-160) for extractions",
            "notes": "Brazil has more dentists per capita than almost any country. Quality is excellent at private clinics in major cities. Dental tourism is a significant industry.",
            "emergencyTip": "UPA (Unidade de Pronto Atendimento) urgent care centers provide emergency dental pain relief. Private dental clinics often have same-day appointments."
        },
        "mentalHealth": {
            "crisisLine": "CVV (Centro de Valorização da Vida): 188 (24/7, Portuguese-language)",
            "internationalLine": "WhatsApp support also available through CVV",
            "englishTherapists": "English-speaking therapists available in São Paulo and Rio through international clinics and online platforms like BetterHelp.",
            "notes": "Public mental health services (CAPS) are available through SUS but mainly in Portuguese. Private English-speaking therapists charge R$200-500 per session."
        },
        "accessibilityInfo": {
            "overview": "Brazil has accessibility laws but enforcement varies. Major cities are improving but sidewalks and older buildings can be challenging.",
            "hospitalAccess": "Private hospitals are generally wheelchair accessible. Public hospitals vary in accessibility.",
            "transport": "Metro systems in São Paulo and Rio have elevators and priority seating. Accessible buses available on main routes. Uber Assist available in major cities.",
            "tips": "Beach wheelchairs (cadeiras anfíbias) are available at some beaches in Rio and other coastal cities. Book accessible accommodations well in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Masks may be required in some healthcare settings.",
            "testing": "Antigen and PCR tests available at pharmacies and labs. Cost: R$80-250 for PCR.",
            "notes": "Brazil removed all COVID entry restrictions. Dengue and Zika remain more significant current health concerns than COVID."
        },
        "insuranceClaimProcess": "Private hospitals in Brazil often require payment upfront or credit card guarantee. SUS (public healthcare) is free but quality varies. Keep all notas fiscais (invoices) and laudos médicos (medical reports). Request English documentation from private hospitals. File claims within your policy deadline.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "GB": {
        "hospitals": [
            {"name": "University College London Hospital (UCLH)", "nearTouristArea": "Central London / British Museum", "phone": "+44-20-3456-7890", "englishSpeaking": True, "notes": "Major teaching hospital in the heart of London. A&E department."},
            {"name": "St Thomas' Hospital", "nearTouristArea": "Westminster / London Eye", "phone": "+44-20-7188-7188", "englishSpeaking": True, "notes": "Directly opposite Houses of Parliament. Major A&E."},
            {"name": "Royal Edinburgh Hospital", "nearTouristArea": "Edinburgh Old Town", "phone": "+44-131-537-6000", "englishSpeaking": True, "notes": "Central Edinburgh location near tourist areas."},
            {"name": "Manchester Royal Infirmary", "nearTouristArea": "Manchester city center", "phone": "+44-161-276-1234", "englishSpeaking": True, "notes": "Major A&E department serving central Manchester."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "I need something for a headache, please", "transliteration": "Ask at Boots or Superdrug pharmacies"},
        ],
        "dentalCare": {
            "availability": "NHS dental care available but very difficult to access for non-residents. Private dentists widely available but expensive.",
            "costRange": "£23-65 for NHS treatment (if available); £50-200+ for private consultation; £100-500 for private fillings",
            "notes": "NHS dental services are heavily oversubscribed. As a visitor, private dental care is your best option. Chains like mydentist and Bupa Dental Care accept walk-ins.",
            "emergencyTip": "Call NHS 111 for dental emergency advice. Hospital A&E departments handle dental trauma (knocked-out teeth, jaw injuries) but not toothache. Use NHS.uk to find emergency dental services."
        },
        "mentalHealth": {
            "crisisLine": "Samaritans: 116 123 (free, 24/7)",
            "internationalLine": "Crisis Text Line: text SHOUT to 85258",
            "englishTherapists": "Widely available. NHS talking therapies available for residents. Private therapists: £40-150 per session.",
            "notes": "The UK has extensive mental health services. NHS 111 can direct you to urgent mental health support. A&E departments handle mental health crises."
        },
        "accessibilityInfo": {
            "overview": "The UK has strong disability rights legislation (Equality Act 2010). Most public buildings, transport, and tourist attractions are wheelchair accessible.",
            "hospitalAccess": "All NHS hospitals are wheelchair accessible with accessible parking, restrooms, and inpatient facilities.",
            "transport": "London Underground has step-free access at many stations (check TfL map). All London buses are wheelchair accessible. National Rail offers assisted travel.",
            "tips": "Blue Badge parking scheme for disabled visitors. Most museums and attractions offer free carer admission. Guide dogs welcome everywhere."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Individual choice in all settings.",
            "testing": "Lateral flow tests available at pharmacies (£2-5). PCR available at private clinics (£50-100).",
            "notes": "All COVID restrictions removed. NHS COVID services scaled down. Antivirals available through NHS for vulnerable groups."
        },
        "insuranceClaimProcess": "NHS A&E treatment is free for everyone regardless of nationality. However, follow-up treatment and hospital admission may be charged to overseas visitors (150% of NHS tariff). EU/EEA citizens with EHIC/GHIC get reduced charges. Keep all documentation and receipts from any private treatment.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "FR": {
        "hospitals": [
            {"name": "Hôpital Américain de Paris", "nearTouristArea": "Neuilly-sur-Seine (near Arc de Triomphe)", "phone": "+33-1-46-41-25-25", "englishSpeaking": True, "notes": "Premier international hospital. Fully English-speaking. Direct billing with many insurers."},
            {"name": "Hôtel-Dieu (AP-HP)", "nearTouristArea": "Île de la Cité / Notre-Dame, Paris", "phone": "+33-1-42-34-82-34", "englishSpeaking": True, "notes": "Historic hospital next to Notre-Dame. Emergency department."},
            {"name": "Hôpital de la Timone", "nearTouristArea": "Marseille city center", "phone": "+33-4-91-38-00-00", "englishSpeaking": True, "notes": "Largest hospital in Marseille. Major emergency department."},
            {"name": "CHU de Nice", "nearTouristArea": "Nice / French Riviera", "phone": "+33-4-92-03-77-77", "englishSpeaking": True, "notes": "Main hospital serving the Côte d'Azur tourist region."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "J'ai besoin d'un médicament contre le mal de tête", "transliteration": ""},
            {"english": "I have a stomachache", "local": "J'ai mal à l'estomac", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Je suis allergique à...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Où est la pharmacie la plus proche ?", "transliteration": ""},
            {"english": "I need a doctor", "local": "J'ai besoin d'un médecin", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Excellent dental care. French dentists are well-trained and clinics are widespread.",
            "costRange": "€23-50 for a consultation; €50-200 for fillings; €80-300 for extractions",
            "notes": "French dental care is partially covered by Sécurité Sociale for residents. Tourists pay out-of-pocket. Quality is high throughout the country.",
            "emergencyTip": "Call 15 (SAMU) for dental emergencies. Hôpitaux universitaires have dental emergency departments (urgences dentaires). Pharmacies can provide pain relief."
        },
        "mentalHealth": {
            "crisisLine": "3114 (national suicide prevention number, 24/7)",
            "internationalLine": "SOS Amitié: 09 72 39 40 50",
            "englishTherapists": "English-speaking therapists available in Paris and major tourist cities. Check Doctolib.fr (France's main healthcare booking platform) for English-speaking practitioners.",
            "notes": "France has CMP (Centre Médico-Psychologique) for free or low-cost mental health consultations. Wait times can be long. Private therapists charge €50-120 per session."
        },
        "accessibilityInfo": {
            "overview": "France has been improving accessibility under EU directives. Major tourist attractions and modern buildings are accessible. Older buildings and cobblestone streets can be challenging.",
            "hospitalAccess": "French hospitals are wheelchair accessible. Most have accessible parking and adapted restrooms.",
            "transport": "Paris Métro has limited wheelchair access (line 14 is fully accessible). All buses are accessible. TGV trains have wheelchair spaces. RATP provides accessibility info.",
            "tips": "Request a 'fauteuil roulant' (wheelchair) when booking trains. Many museums offer priority access for disabled visitors. The Paris tourist office has accessibility guides."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates in public spaces. May be required in some healthcare settings.",
            "testing": "Antigen tests available at pharmacies (€5-15). PCR available at laboratories (€30-50).",
            "notes": "France removed all COVID restrictions. Healthcare professionals may request masks during flu season."
        },
        "insuranceClaimProcess": "French healthcare uses a fee-for-service model. Doctors provide a feuille de soins (care sheet). Keep all receipts and the feuille de soins for insurance claims. EU citizens with EHIC can get partial reimbursement through CPAM. Pharmacies provide itemized receipts (ticket de caisse).",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    "DE": {
        "hospitals": [
            {"name": "Charité – Universitätsmedizin Berlin", "nearTouristArea": "Berlin Mitte / Brandenburg Gate", "phone": "+49-30-450-50", "englishSpeaking": True, "notes": "Europe's largest university hospital. International patient office."},
            {"name": "Klinikum rechts der Isar", "nearTouristArea": "Munich city center / Marienplatz", "phone": "+49-89-4140-0", "englishSpeaking": True, "notes": "Technical University of Munich hospital. Excellent emergency care."},
            {"name": "Universitätsklinikum Hamburg-Eppendorf", "nearTouristArea": "Hamburg city center", "phone": "+49-40-7410-0", "englishSpeaking": True, "notes": "Major university hospital with international patient services."},
            {"name": "Universitätsklinikum Frankfurt", "nearTouristArea": "Frankfurt city center", "phone": "+49-69-6301-0", "englishSpeaking": True, "notes": "University hospital near Frankfurt's main tourist areas."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ich brauche etwas gegen Kopfschmerzen", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Ich habe Magenschmerzen", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Ich bin allergisch gegen...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Wo ist die nächste Apotheke?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Ich brauche einen Arzt", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Excellent dental care throughout Germany. Dentists (Zahnarzt) are plentiful and well-equipped.",
            "costRange": "€30-80 for consultation; €80-300 for fillings; €100-400 for extractions",
            "notes": "German dental care is high quality. Many dentists in tourist areas and cities speak English. Dental emergency services (zahnärztlicher Notdienst) available on weekends.",
            "emergencyTip": "Call 116 117 for the dental emergency service (Zahnärztlicher Bereitschaftsdienst). Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "0800 111 0 111 (Telefonseelsorge — free, 24/7)",
            "internationalLine": "0800 111 0 222 (alternative line)",
            "englishTherapists": "English-speaking therapists available in Berlin, Munich, Frankfurt, and other major cities. International practices cater to expats and travelers.",
            "notes": "Germany has extensive mental health services. Waiting times for therapists can be long (months). Private practitioners may have shorter wait times. Costs: €80-150 per session privately."
        },
        "accessibilityInfo": {
            "overview": "Germany has strong accessibility standards. Modern buildings and public transport are generally accessible. Historic city centers may have cobblestone challenges.",
            "hospitalAccess": "German hospitals are wheelchair accessible with adapted facilities throughout.",
            "transport": "Deutsche Bahn trains have wheelchair spaces and assistance services (book via Mobilitätsservice). U-Bahn/S-Bahn systems have elevators at most stations. Low-floor buses throughout.",
            "tips": "Book Deutsche Bahn Mobilitätsservice at least one day ahead for station assistance. Many tourist attractions offer wheelchair rentals. The ADAC provides accessible travel information."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Individual healthcare facilities may require masks.",
            "testing": "Tests available at pharmacies and Testzentren. Antigen: €5-15. PCR: €50-80.",
            "notes": "Germany removed all COVID restrictions. Some healthcare settings maintain their own mask policies."
        },
        "insuranceClaimProcess": "German doctors provide Rechnungen (invoices) after treatment. Keep all documentation including Arztbrief (medical letter). EU citizens with EHIC can access emergency care. Non-EU travelers should contact their insurer before treatment when possible. Pharmacies provide itemized receipts.",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    "ES": {
        "hospitals": [
            {"name": "Hospital Clínic de Barcelona", "nearTouristArea": "Eixample / near La Sagrada Família", "phone": "+34-93-227-54-00", "englishSpeaking": True, "notes": "Top-ranked public hospital. Large emergency department."},
            {"name": "Hospital Universitario La Paz", "nearTouristArea": "Northern Madrid", "phone": "+34-91-727-70-00", "englishSpeaking": True, "notes": "Major public hospital serving Madrid. International patient services."},
            {"name": "Hospital Quirónsalud Marbella", "nearTouristArea": "Costa del Sol / Marbella", "phone": "+34-952-77-42-00", "englishSpeaking": True, "notes": "Private hospital in the main tourist area. Many English-speaking staff."},
            {"name": "Hospital Universitario Son Espases", "nearTouristArea": "Palma de Mallorca / Balearic Islands", "phone": "+34-871-20-50-00", "englishSpeaking": True, "notes": "Main hospital for Mallorca. Serves the tourist islands."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Tengo dolor de estómago", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Soy alérgico/a a...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "¿Dónde está la farmacia más cercana?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Good dental care available. Spain is a popular dental tourism destination with significantly lower costs than northern Europe.",
            "costRange": "€30-60 for consultation; €50-150 for fillings; €60-200 for extractions",
            "notes": "Dental tourism is popular in Spain, especially in Barcelona and coastal areas. Quality is good and prices are 40-60% lower than the UK. Many clinics cater to English-speaking tourists.",
            "emergencyTip": "Hospital emergency departments handle dental trauma. For dental pain, visit a farmacia for over-the-counter pain relief and ask for a dentist referral."
        },
        "mentalHealth": {
            "crisisLine": "024 (Línea de Atención a la Conducta Suicida — 24/7)",
            "internationalLine": "Teléfono de la Esperanza: 717 003 717",
            "englishTherapists": "English-speaking therapists available in Barcelona, Madrid, and major tourist areas. Online therapy platforms also serve Spain.",
            "notes": "Public mental health services available through the Spanish national health system but mainly in Spanish. Private English-speaking therapists: €50-100 per session."
        },
        "accessibilityInfo": {
            "overview": "Spain has been improving accessibility. Major cities and modern attractions are accessible. Historic old towns with narrow streets and steps can be challenging.",
            "hospitalAccess": "Spanish hospitals are wheelchair accessible with adapted emergency departments.",
            "transport": "Metro systems in Madrid and Barcelona have elevators at most stations. All city buses are low-floor. AVE high-speed trains have wheelchair spaces. RENFE offers mobility assistance.",
            "tips": "Barcelona's beaches have accessible boardwalks and beach wheelchairs. Major museums offer accessibility programs. Request RENFE Atendo service for rail travel assistance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates in public spaces. Still required in healthcare settings and pharmacies.",
            "testing": "Antigen tests at pharmacies (€3-10). PCR at clinics (€40-80).",
            "notes": "Spain maintains mask requirements in healthcare facilities. All other COVID restrictions removed."
        },
        "insuranceClaimProcess": "Spanish public emergency rooms treat everyone regardless of insurance. You may receive a bill later for non-EU visitors. Keep all facturas (invoices) and informes médicos (medical reports). EU citizens with TSE (Spanish EHIC) or EHIC receive free emergency treatment.",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    "IT": {
        "hospitals": [
            {"name": "Ospedale Fatebenefratelli", "nearTouristArea": "Isola Tiberina, Rome (near Trastevere)", "phone": "+39-06-68371", "englishSpeaking": True, "notes": "Central Rome location. Emergency department serves tourist areas."},
            {"name": "Ospedale Santa Maria Nuova", "nearTouristArea": "Florence / Duomo area", "phone": "+39-055-69381", "englishSpeaking": True, "notes": "Oldest hospital in Florence, steps from the Duomo. 24/7 emergency."},
            {"name": "Ospedale Civile SS. Giovanni e Paolo", "nearTouristArea": "Venice / near Rialto Bridge", "phone": "+39-041-529-4111", "englishSpeaking": True, "notes": "Venice's main hospital. Water ambulance access."},
            {"name": "Ospedale Maggiore Policlinico", "nearTouristArea": "Milan city center", "phone": "+39-02-5503-1", "englishSpeaking": True, "notes": "Major university hospital in central Milan."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ho bisogno di una medicina per il mal di testa", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Ho mal di stomaco", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Sono allergico/a a...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Dov'è la farmacia più vicina?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Ho bisogno di un medico", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Good dental care throughout Italy. Private dental clinics common in cities.",
            "costRange": "€50-100 for consultation; €80-250 for fillings; €100-300 for extractions",
            "notes": "Italian dental care quality is high. Dental tourism is growing, especially in southern Italy where prices are lower. Many dentists in tourist areas speak some English.",
            "emergencyTip": "For dental emergencies, go to Pronto Soccorso (emergency room) at the nearest hospital. Guardia medica (after-hours medical service) can also assist."
        },
        "mentalHealth": {
            "crisisLine": "Telefono Amico: 02 2327 2327",
            "internationalLine": "Telefono Azzurro: 19696 (for minors)",
            "englishTherapists": "English-speaking therapists available in Rome, Milan, and Florence through international practices.",
            "notes": "Italy's public mental health centers (CSM) provide free services but mainly in Italian. Private therapists charge €60-120 per session."
        },
        "accessibilityInfo": {
            "overview": "Italy's accessibility is uneven. Modern facilities are accessible but historic cities with cobblestone streets, steps, and old buildings can be very challenging for wheelchair users.",
            "hospitalAccess": "Modern hospitals are wheelchair accessible. Older hospital buildings may have limitations.",
            "transport": "Major metro systems have partial elevator access. All new buses are low-floor. Trenitalia offers assistance for disabled travelers (Sala Blu service).",
            "tips": "Book Trenitalia Sala Blu assistance 48 hours ahead. Venice is particularly challenging for wheelchairs — water buses (vaporetti) have limited access. Rome's cobblestones make manual wheelchairs difficult."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "Masks required in hospitals and healthcare facilities. No mandates elsewhere.",
            "testing": "Antigen tests at pharmacies (€5-15). PCR at labs (€40-60).",
            "notes": "Italy maintains mask rules in healthcare settings. All other COVID restrictions removed."
        },
        "insuranceClaimProcess": "Italian emergency rooms (Pronto Soccorso) provide emergency treatment. Non-EU visitors may receive a bill. Keep all ricevute (receipts) and referti medici (medical reports). EU citizens with TEAM (Italian EHIC) receive free emergency care. Ask for English documentation at larger hospitals.",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    "TH": {
        "hospitals": [
            {"name": "Bumrungrad International Hospital", "nearTouristArea": "Sukhumvit, Bangkok", "phone": "+66-2-066-8888", "englishSpeaking": True, "notes": "JCI-accredited. Southeast Asia's premier international hospital. 40+ specialty centers. Direct billing with most insurers."},
            {"name": "Bangkok Hospital", "nearTouristArea": "Soi Soonvijai, Bangkok", "phone": "+66-2-310-3000", "englishSpeaking": True, "notes": "Part of BDMS network. International patient center with translators."},
            {"name": "Bangkok Hospital Phuket", "nearTouristArea": "Phuket Town (near Patong)", "phone": "+66-76-254-425", "englishSpeaking": True, "notes": "Main international hospital for Phuket tourists. Hyperbaric chamber for diving injuries."},
            {"name": "Bangkok Hospital Chiang Mai", "nearTouristArea": "Chiang Mai city center", "phone": "+66-52-089-888", "englishSpeaking": True, "notes": "International hospital serving northern Thailand tourists."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "ต้องการยาแก้ปวดหัว", "transliteration": "Dtong-gaan yaa gae bpuat hua"},
            {"english": "I have a stomachache", "local": "ปวดท้อง", "transliteration": "Bpuat tong"},
            {"english": "I'm allergic to...", "local": "แพ้...", "transliteration": "Pae..."},
            {"english": "Where is the nearest pharmacy?", "local": "ร้านขายยาใกล้ที่สุดอยู่ที่ไหน", "transliteration": "Raan kaai yaa glai tee sut yoo tee nai?"},
            {"english": "I need a doctor", "local": "ต้องการหมอ", "transliteration": "Dtong-gaan mor"},
        ],
        "dentalCare": {
            "availability": "Thailand is a top dental tourism destination. High-quality clinics widely available at a fraction of Western prices.",
            "costRange": "฿500-1,500 ($15-45) for consultation; ฿2,000-5,000 ($60-150) for fillings; ฿3,000-8,000 ($90-240) for extractions",
            "notes": "Bangkok and Phuket have world-class dental clinics. Many dentists trained in the US, UK, or Australia. Popular for veneers, implants, and cosmetic dentistry. BIDC and Bangkok Smile are well-known chains.",
            "emergencyTip": "International hospitals have 24/7 dental emergency departments. Bumrungrad and Bangkok Hospital both offer emergency dental care."
        },
        "mentalHealth": {
            "crisisLine": "1323 (Department of Mental Health hotline, 24/7, Thai language)",
            "internationalLine": "Samaritans of Thailand: 02-713-6793 (English-speaking)",
            "englishTherapists": "English-speaking therapists and psychiatrists available at international hospitals in Bangkok. Bumrungrad and Bangkok Hospital have mental health departments.",
            "notes": "Mental health services in English are concentrated in Bangkok's international hospitals. Private therapy costs ฿2,000-5,000 ($60-150) per session."
        },
        "accessibilityInfo": {
            "overview": "Thailand's accessibility varies greatly. Modern shopping malls and international hotels are accessible. Streets, temples, and older buildings often lack wheelchair access.",
            "hospitalAccess": "International hospitals are fully wheelchair accessible. Public hospitals may have limited accessibility.",
            "transport": "BTS Skytrain and MRT subway in Bangkok have elevators at most stations. Taxis are cheap but not wheelchair-adapted. Grab (ride-hailing app) available everywhere.",
            "tips": "Temples often have steps and no ramps. Beach access is limited for wheelchairs. Major hotels can arrange accessible transport. Thailand is generally very accommodating — locals often help physically."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Voluntary mask-wearing remains common in crowded areas.",
            "testing": "ATK tests at pharmacies (฿50-200). PCR at hospitals (฿1,500-3,500).",
            "notes": "Thailand removed all COVID entry restrictions. Dengue fever is a more significant current health concern."
        },
        "insuranceClaimProcess": "Thai international hospitals are experienced with insurance claims and often offer direct billing. Bumrungrad and Bangkok Hospital have dedicated insurance desks. For other facilities, pay upfront and keep all receipts and medical reports. Hospitals provide English documentation on request.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "IN": {
        "hospitals": [
            {"name": "Apollo Hospital", "nearTouristArea": "Multiple locations — Delhi, Mumbai, Chennai, Bangalore", "phone": "+91-11-2987-1801 (Delhi)", "englishSpeaking": True, "notes": "India's largest hospital chain. JCI-accredited. International patient department."},
            {"name": "Max Super Speciality Hospital", "nearTouristArea": "Saket, New Delhi (near Qutub Minar)", "phone": "+91-11-2651-5050", "englishSpeaking": True, "notes": "Top private hospital in Delhi. International patient services."},
            {"name": "Fortis Hospital", "nearTouristArea": "Multiple locations — Delhi, Mumbai, Bangalore, Jaipur", "phone": "+91-124-462-1444 (Gurgaon)", "englishSpeaking": True, "notes": "Major private hospital chain with international patient departments."},
            {"name": "Breach Candy Hospital", "nearTouristArea": "South Mumbai / Gateway of India area", "phone": "+91-22-2366-7788", "englishSpeaking": True, "notes": "Premier private hospital in Mumbai. Popular with expats and tourists."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "मुझे सिर दर्द की दवा चाहिए", "transliteration": "Mujhe sir dard ki dawa chahiye"},
            {"english": "I have a stomachache", "local": "मेरे पेट में दर्द है", "transliteration": "Mere pet mein dard hai"},
            {"english": "I'm allergic to...", "local": "मुझे ... से एलर्जी है", "transliteration": "Mujhe ... se allergy hai"},
            {"english": "Where is the nearest pharmacy?", "local": "सबसे नज़दीकी दवाई की दुकान कहाँ है?", "transliteration": "Sabse nazdeeki dawaai ki dukaan kahan hai?"},
            {"english": "I need a doctor", "local": "मुझे डॉक्टर की ज़रूरत है", "transliteration": "Mujhe doctor ki zaroorat hai"},
        ],
        "dentalCare": {
            "availability": "India is a major dental tourism destination. Private clinics offer world-class care at very low prices. Quality varies widely.",
            "costRange": "₹300-1,000 ($4-12) for consultation; ₹1,000-5,000 ($12-60) for fillings; ₹2,000-8,000 ($24-96) for extractions",
            "notes": "Major cities have excellent dental clinics, many catering to medical tourists. Clove Dental and Apollo White Dental are established chains. Delhi, Mumbai, and Bangalore are dental tourism hubs.",
            "emergencyTip": "Private hospitals have 24/7 dental departments. In an emergency, go to Apollo or Fortis hospital emergency departments. Pharmacies can provide pain relief immediately."
        },
        "mentalHealth": {
            "crisisLine": "AASRA: 9820466726 (24/7 crisis helpline)",
            "internationalLine": "Vandrevala Foundation: 1860-2662-345 (24/7, multilingual including English)",
            "englishTherapists": "English-speaking therapists widely available in major cities. Online therapy platforms like Practo and MFine offer English-language sessions.",
            "notes": "India's mental health infrastructure is growing. Private practitioners in cities charge ₹1,000-3,000 ($12-36) per session. International hospitals have psychiatry departments."
        },
        "accessibilityInfo": {
            "overview": "India's accessibility varies enormously. Modern buildings and airports meet international standards. Streets, old buildings, temples, and public transport are often inaccessible.",
            "hospitalAccess": "Private hospitals (Apollo, Max, Fortis) are fully wheelchair accessible. Government hospitals have limited accessibility.",
            "transport": "Delhi Metro has elevators and wheelchair access. Auto-rickshaws and most taxis are not wheelchair friendly. Uber available with regular cars. Accessible transport is very limited.",
            "tips": "Plan accessibility carefully. The Taj Mahal has wheelchair access with assistance. Many heritage sites have steps and no alternatives. Hire a local guide who can help navigate accessibility challenges."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Voluntary mask-wearing varies by region.",
            "testing": "Antigen tests at pharmacies and clinics (₹200-500). PCR at labs (₹500-1,500).",
            "notes": "India removed all COVID entry restrictions. Air quality (pollution) is a more significant respiratory concern, especially in Delhi during winter."
        },
        "insuranceClaimProcess": "Private hospitals in India are accustomed to international insurance. Apollo and Fortis have dedicated TPA (Third Party Administrator) desks for insurance. Pay upfront at smaller facilities and keep all bills (receipts) and discharge summaries. Hospitals provide English documentation as standard.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "EG": {
        "hospitals": [
            {"name": "As-Salam International Hospital", "nearTouristArea": "Maadi, Cairo (near Old Cairo/Coptic area)", "phone": "+20-2-2524-0250", "englishSpeaking": True, "notes": "International hospital with English and Arabic speaking staff."},
            {"name": "Dar Al Fouad Hospital", "nearTouristArea": "6th of October City, Cairo (near Pyramids)", "phone": "+20-2-3835-6030", "englishSpeaking": True, "notes": "JCI-accredited. Close to the Pyramids of Giza."},
            {"name": "Royal Hospital Hurghada", "nearTouristArea": "Hurghada / Red Sea resorts", "phone": "+20-65-344-3024", "englishSpeaking": True, "notes": "Private hospital serving Red Sea tourist area. Hyperbaric chamber for diving injuries."},
            {"name": "Sharm International Hospital", "nearTouristArea": "Sharm El-Sheikh", "phone": "+20-69-366-0893", "englishSpeaking": True, "notes": "Serves the Sharm el-Sheikh resort area. English-speaking staff."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "محتاج دوا للصداع", "transliteration": "Mihtaag dawa lil-sudaa'"},
            {"english": "I have a stomachache", "local": "عندي ألم في بطني", "transliteration": "Andi alam fi batni"},
            {"english": "I'm allergic to...", "local": "عندي حساسية من...", "transliteration": "Andi hasaasiya min..."},
            {"english": "Where is the nearest pharmacy?", "local": "فين أقرب صيدلية؟", "transliteration": "Feen aqrab saidaliyya?"},
            {"english": "I need a doctor", "local": "محتاج دكتور", "transliteration": "Mihtaag duktoor"},
        ],
        "dentalCare": {
            "availability": "Dental care is widely available and very affordable. Cairo and resort areas have modern dental clinics.",
            "costRange": "EGP 200-500 ($4-10) for consultation; EGP 500-2,000 ($10-40) for fillings; EGP 500-1,500 ($10-30) for extractions",
            "notes": "Egypt is an emerging dental tourism destination with prices 70-80% lower than Europe. Quality varies — stick to well-reviewed clinics in Cairo. Several JCI-accredited hospitals have dental departments.",
            "emergencyTip": "Private hospital emergency departments handle dental emergencies. Many pharmacies can provide antibiotics and strong pain relief without prescription."
        },
        "mentalHealth": {
            "crisisLine": "08008880700 (mental health helpline)",
            "internationalLine": "Befrienders Worldwide: check befrienders.org for local contacts",
            "englishTherapists": "English-speaking therapists available in Cairo through international clinics and private practices.",
            "notes": "Mental health services are limited but growing. Private practitioners in Cairo charge EGP 500-1,500 ($10-30) per session. Stigma around mental health remains strong."
        },
        "accessibilityInfo": {
            "overview": "Egypt's accessibility is limited. Modern hotels and international chains are accessible. Streets, temples, and pyramids have significant barriers for wheelchair users.",
            "hospitalAccess": "Private hospitals are generally accessible. Public hospitals have limited wheelchair access.",
            "transport": "Cairo Metro has limited accessibility. Taxis are cheap but not wheelchair adapted. Uber is available in Cairo and offers the most flexible option.",
            "tips": "The Pyramids and Valley of the Kings are extremely challenging for wheelchair users. Many tour operators offer adapted tours. Hotels in tourist areas often have accessible rooms. Hire a guide who can arrange assistance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Some indoor venues may request masks.",
            "testing": "Antigen and PCR tests available at pharmacies, clinics, and airports.",
            "notes": "Egypt removed all COVID entry restrictions. Heat-related illness and gastrointestinal issues are more common health concerns for tourists."
        },
        "insuranceClaimProcess": "Private hospitals may require upfront payment or a credit card deposit. Keep all receipts (iiSaalaat) and medical reports. International hospitals in Cairo can provide English documentation. For diving-related injuries at Red Sea resorts, contact your insurer immediately as recompression treatment is expensive.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "KH": {
        "hospitals": [
            {"name": "Royal Phnom Penh Hospital", "nearTouristArea": "Central Phnom Penh / Riverside", "phone": "+855-23-991-000", "englishSpeaking": True, "notes": "Best private hospital in Cambodia. Part of Bangkok Hospital group. Direct billing with some insurers."},
            {"name": "Sunrise Japan Hospital", "nearTouristArea": "Phnom Penh", "phone": "+855-23-260-152", "englishSpeaking": True, "notes": "Japanese-managed hospital with high standards. English and Japanese speaking staff."},
            {"name": "Royal Angkor International Hospital", "nearTouristArea": "Siem Reap / near Angkor Wat", "phone": "+855-63-761-888", "englishSpeaking": True, "notes": "Nearest quality hospital to Angkor Wat temples. Part of Bangkok Hospital network."},
            {"name": "Naga Clinic", "nearTouristArea": "Phnom Penh (near Russian Market)", "phone": "+855-23-211-300", "englishSpeaking": True, "notes": "French-run clinic popular with expats. Good for non-emergency care."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "ខ្ញុំត្រូវការថ្នាំពេទ្យសម្រាប់ឈឺក្បាល", "transliteration": "Knyom trov-kaa thnam pet samrab chheu kbal"},
            {"english": "I have a stomachache", "local": "ខ្ញុំឈឺពោះ", "transliteration": "Knyom chheu puah"},
            {"english": "I need a doctor", "local": "ខ្ញុំត្រូវការគ្រូពេទ្យ", "transliteration": "Knyom trov-kaa kru pet"},
            {"english": "Where is the nearest pharmacy?", "local": "ឱសថស្ថានជិតបំផុតនៅឯណា?", "transliteration": "Osat-thaan jit bam-phot nov ae-naa?"},
        ],
        "dentalCare": {
            "availability": "Dental care is available in Phnom Penh and Siem Reap. Quality varies widely. International clinics offer acceptable care for basic procedures.",
            "costRange": "$10-30 for consultation; $20-80 for fillings; $20-60 for extractions",
            "notes": "For anything beyond basic dental work, consider traveling to Bangkok. Phnom Penh has some expat-oriented dental clinics (Roomchang Dental, European Dental Clinic). Quality control is limited.",
            "emergencyTip": "Royal Phnom Penh Hospital has a dental department. In Siem Reap, Royal Angkor International Hospital can handle dental emergencies. For serious dental issues, evacuate to Bangkok."
        },
        "mentalHealth": {
            "crisisLine": "No dedicated crisis line. Contact your embassy in an emergency.",
            "internationalLine": "findahelpline.com for international resources",
            "englishTherapists": "Very limited. Some expat counselors available in Phnom Penh. TPO Cambodia provides some mental health services.",
            "notes": "Mental health services in Cambodia are extremely limited. For serious mental health concerns, medical evacuation to Bangkok is recommended. Some NGOs provide community mental health support."
        },
        "accessibilityInfo": {
            "overview": "Cambodia has very limited accessibility infrastructure. Roads are rough, sidewalks are often blocked, and most buildings lack wheelchair access.",
            "hospitalAccess": "International hospitals in Phnom Penh are reasonably accessible. Rural health facilities have minimal accessibility.",
            "transport": "No accessible public transport. Tuk-tuks and taxis are the main options. Wheelchairs can be accommodated with assistance. Uber not available — use Grab or PassApp.",
            "tips": "Angkor Wat's main temple has very steep steps. The outer grounds are manageable with a sturdy wheelchair. Hire a guide for assistance. Hotels in Siem Reap and Phnom Penh are generally more accessible than those in rural areas."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates.",
            "testing": "Tests available at hospitals and some pharmacies in Phnom Penh.",
            "notes": "Cambodia removed all COVID entry restrictions. Dengue fever and gastrointestinal illness are more significant health concerns for tourists."
        },
        "insuranceClaimProcess": "International hospitals accept some direct billing. Most facilities require upfront cash payment. Keep all receipts and get English-language medical reports. For medical evacuation (the most common large claim in Cambodia), contact your insurer immediately — evacuations to Bangkok cost $10,000-30,000+.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "CA": {
        "hospitals": [
            {"name": "Toronto General Hospital", "nearTouristArea": "Downtown Toronto / CN Tower area", "phone": "+1-416-340-4800", "englishSpeaking": True, "notes": "Part of UHN — one of Canada's top hospital networks."},
            {"name": "Vancouver General Hospital", "nearTouristArea": "Fairview, Vancouver", "phone": "+1-604-875-4111", "englishSpeaking": True, "notes": "Major trauma center. Close to downtown Vancouver."},
            {"name": "Montreal General Hospital (MUHC)", "nearTouristArea": "Downtown Montreal / Old Montreal", "phone": "+1-514-934-1934", "englishSpeaking": True, "notes": "English-language hospital in Montreal. Part of McGill University Health Centre."},
            {"name": "Banff Mineral Springs Hospital", "nearTouristArea": "Banff / Rocky Mountains", "phone": "+1-403-762-2222", "englishSpeaking": True, "notes": "Small hospital serving Banff National Park area."},
        ],
        "pharmacyPhrases": [
            {"english": "Where is the nearest pharmacy?", "local": "Where is the nearest pharmacy?", "transliteration": "In Quebec: Où est la pharmacie la plus proche ?"},
        ],
        "dentalCare": {
            "availability": "Excellent dental care but expensive. Not covered by Canadian Medicare for most procedures.",
            "costRange": "CAD $100-250 for consultation; CAD $150-400 for fillings; CAD $200-500 for extractions",
            "notes": "Canadian dental care is high quality but very expensive. Walk-in dental clinics available in major cities. Emergency dental care available at hospital emergency departments.",
            "emergencyTip": "For dental emergencies, visit a hospital emergency department or call your provincial health line (811 in most provinces). Walk-in dental clinics may have same-day appointments."
        },
        "mentalHealth": {
            "crisisLine": "988 (Suicide Crisis Helpline — 24/7, English and French)",
            "internationalLine": "Crisis Text Line: text CONNECT to 686868",
            "englishTherapists": "Widely available. Provincial health lines (811) can provide referrals.",
            "notes": "Canada has comprehensive mental health services. Crisis services available 24/7. Provincial healthcare may cover some therapy for residents. Private therapy: CAD $150-250 per session."
        },
        "accessibilityInfo": {
            "overview": "Canada has strong accessibility legislation (Accessible Canada Act). Major cities are well-equipped for wheelchair users.",
            "hospitalAccess": "All major hospitals are fully wheelchair accessible.",
            "transport": "Public transit in major cities is accessible. Specialized transit services available. Via Rail offers accessible travel. Most taxis have accessible options.",
            "tips": "National parks have varying accessibility — Parks Canada provides detailed accessibility guides. Rick Hansen Foundation provides accessibility ratings for many venues."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry via ArriveCAN.",
            "maskPolicy": "No federal mask mandates. Some healthcare facilities maintain their own policies.",
            "testing": "Rapid tests at pharmacies. PCR available at clinics and pharmacies (CAD $40-150).",
            "notes": "Canada removed all COVID entry restrictions including ArriveCAN requirements. Provincial health authorities manage ongoing public health measures."
        },
        "insuranceClaimProcess": "Canadian healthcare is expensive for visitors — an ER visit can cost CAD $500-1,500+. Hospital admissions may require a deposit. Keep all receipts and medical records. Most hospitals have a billing department that can provide itemized statements for insurance claims.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "MX": {
        "hospitals": [
            {"name": "Hospital Ángeles", "nearTouristArea": "Multiple locations — Mexico City, Cancún, Guadalajara, Tijuana", "phone": "+52-55-5516-9900 (Mexico City)", "englishSpeaking": True, "notes": "Mexico's largest private hospital chain. International patient services."},
            {"name": "Amerimed Hospital Cancún", "nearTouristArea": "Cancún Hotel Zone", "phone": "+52-998-881-3400", "englishSpeaking": True, "notes": "Main hospital serving Cancún's tourist zone. Direct billing with US insurers."},
            {"name": "Hospital CMQ Riviera Nayarit", "nearTouristArea": "Puerto Vallarta", "phone": "+52-322-226-6500", "englishSpeaking": True, "notes": "Private hospital serving Puerto Vallarta tourists. English-speaking staff."},
            {"name": "Médica Sur", "nearTouristArea": "Tlalpan, Mexico City", "phone": "+52-55-5424-7200", "englishSpeaking": True, "notes": "JCI-accredited. One of Mexico City's best private hospitals."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Tengo dolor de estómago", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Soy alérgico/a a...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "¿Dónde está la farmacia más cercana?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Mexico is one of the world's top dental tourism destinations, especially border cities (Tijuana, Los Algodones) and resort areas.",
            "costRange": "$25-60 for consultation; $40-120 for fillings; $50-150 for extractions; dental implants 50-70% cheaper than the US",
            "notes": "Los Algodones ('Molar City') near the US border has hundreds of dental clinics catering to American patients. Cancún, Puerto Vallarta, and Mexico City also have excellent dental clinics. Quality varies — check reviews and credentials.",
            "emergencyTip": "Private hospitals have dental emergency departments. Farmacias Similares (affordable pharmacy chain) often has adjacent affordable medical/dental offices."
        },
        "mentalHealth": {
            "crisisLine": "800 911 2000 (SAPTEL — 24/7 crisis line)",
            "internationalLine": "Línea de la Vida: 800 911 2000",
            "englishTherapists": "English-speaking therapists available in Mexico City, Cancún, and expat communities (San Miguel de Allende, Puerto Vallarta).",
            "notes": "Mental health services in English are available in tourist and expat areas. Private therapy costs $40-80 per session. IMSS and ISSSTE provide public mental health services but mainly in Spanish."
        },
        "accessibilityInfo": {
            "overview": "Mexico's accessibility varies widely. Modern resorts and hotels are generally accessible. Cities have uneven sidewalks, limited ramps, and challenging terrain.",
            "hospitalAccess": "Private hospitals are wheelchair accessible. Public hospitals vary.",
            "transport": "Mexico City Metro has elevators at major stations. Accessible buses on main routes. Taxis are the most flexible option. Uber available in major cities.",
            "tips": "All-inclusive resorts in Cancún and Riviera Maya are generally wheelchair accessible. Archaeological sites (Chichén Itzá, Teotihuacán) have limited accessibility. Beach wheelchairs available at some resort beaches."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry. Mexico never imposed strict entry requirements.",
            "maskPolicy": "No mask mandates.",
            "testing": "Tests available at pharmacies, clinics, and hospitals. Cost: $15-50 for PCR.",
            "notes": "Mexico has minimal COVID restrictions. Dengue and food/water safety are more relevant health concerns for tourists."
        },
        "insuranceClaimProcess": "Private hospitals often accept US insurance or offer direct billing. Get pre-authorization from your insurer when possible. Keep all recibos (receipts) and reportes médicos (medical reports). IMSS (public healthcare) may treat emergencies but quality and wait times vary.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "KR": {
        "hospitals": [
            {"name": "Samsung Medical Center", "nearTouristArea": "Gangnam, Seoul", "phone": "+82-2-3410-2114", "englishSpeaking": True, "notes": "Top-tier hospital with international patient center. English, Chinese, Japanese support."},
            {"name": "Severance Hospital (Yonsei University)", "nearTouristArea": "Sinchon, Seoul (near Hongdae)", "phone": "+82-2-2228-0114", "englishSpeaking": True, "notes": "Major university hospital. International healthcare center."},
            {"name": "Asan Medical Center", "nearTouristArea": "Songpa-gu, Seoul (near Lotte World)", "phone": "+82-2-3010-3114", "englishSpeaking": True, "notes": "One of the world's largest hospitals. International patient department."},
            {"name": "Haeundae Paik Hospital", "nearTouristArea": "Haeundae Beach, Busan", "phone": "+82-51-797-0100", "englishSpeaking": True, "notes": "Near Busan's main beach area. English-speaking staff available."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "두통약이 필요해요", "transliteration": "Dutong-yagi piryohaeyo"},
            {"english": "I have a stomachache", "local": "배가 아파요", "transliteration": "Baega apayo"},
            {"english": "I'm allergic to...", "local": "...에 알레르기가 있어요", "transliteration": "...e allereugiga isseoyo"},
            {"english": "Where is the nearest pharmacy?", "local": "가장 가까운 약국이 어디예요?", "transliteration": "Gajang gakkaun yakgugi eodiyeyo?"},
            {"english": "I need a doctor", "local": "의사가 필요해요", "transliteration": "Uisaga piryohaeyo"},
        ],
        "dentalCare": {
            "availability": "Excellent dental care. South Korea is a major medical tourism destination with state-of-the-art dental clinics.",
            "costRange": "₩30,000-80,000 ($22-60) for consultation; ₩100,000-300,000 ($75-225) for fillings; ₩100,000-400,000 ($75-300) for extractions",
            "notes": "Korea is renowned for dental and cosmetic procedures. Many clinics in Gangnam specialize in dental tourism. Prices are 30-50% lower than the US with comparable quality.",
            "emergencyTip": "Call 1339 (Korea Healthcare Info Line, multilingual including English) for dental emergency referrals. Major hospitals have 24/7 emergency dental departments."
        },
        "mentalHealth": {
            "crisisLine": "1393 (Suicide Prevention Hotline, 24/7)",
            "internationalLine": "1339 (Korea Healthcare Info Line — English available)",
            "englishTherapists": "English-speaking therapists available in Seoul through international clinics. Online therapy platforms serve English speakers.",
            "notes": "Korea's mental health services are primarily in Korean. International clinics in Itaewon and Gangnam areas of Seoul offer English services. Private therapy: ₩80,000-150,000 per session."
        },
        "accessibilityInfo": {
            "overview": "South Korea has been improving accessibility rapidly. Seoul is one of the most accessible cities in Asia with widespread elevator and ramp access.",
            "hospitalAccess": "Major hospitals are fully wheelchair accessible with international patient support.",
            "transport": "Seoul Metro is highly accessible with elevators at all stations. KTX high-speed trains have wheelchair spaces. Low-floor buses on major routes. T-Money transport card works everywhere.",
            "tips": "Traditional hanok houses and some temple stays may not be wheelchair accessible. Palaces in Seoul have partial wheelchair access. Korea Tourism Organization provides accessibility information."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates in most settings. May be required in some healthcare facilities.",
            "testing": "Rapid tests at pharmacies (₩5,000-15,000). PCR at clinics (₩50,000-80,000).",
            "notes": "South Korea removed all COVID entry restrictions. Fine dust (particulate matter) is a more common respiratory concern, especially in spring."
        },
        "insuranceClaimProcess": "Korean hospitals provide itemized bills in Korean (and English at international departments). Keep all receipts and medical certificates (진단서). International patient centers at major hospitals assist with insurance documentation. Many hospitals accept direct billing from international insurers.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "SG": {
        "hospitals": [
            {"name": "Singapore General Hospital", "nearTouristArea": "Outram / Chinatown", "phone": "+65-6222-3322", "englishSpeaking": True, "notes": "Singapore's flagship hospital. Largest acute care hospital."},
            {"name": "Mount Elizabeth Hospital", "nearTouristArea": "Orchard Road shopping district", "phone": "+65-6737-2666", "englishSpeaking": True, "notes": "Premier private hospital on Orchard Road. International patient center."},
            {"name": "Raffles Hospital", "nearTouristArea": "Bugis / near Marina Bay", "phone": "+65-6311-1111", "englishSpeaking": True, "notes": "Private hospital with 24-hour emergency and traveler's clinic."},
            {"name": "Gleneagles Hospital", "nearTouristArea": "Near Botanic Gardens", "phone": "+65-6473-7222", "englishSpeaking": True, "notes": "Part of Parkway Health. International patient services."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "I need medicine for a headache", "transliteration": "English is an official language in Singapore"},
        ],
        "dentalCare": {
            "availability": "World-class dental care available. Singapore is known for exceptional medical and dental quality.",
            "costRange": "SGD $50-150 for consultation; SGD $100-400 for fillings; SGD $150-500 for extractions",
            "notes": "Singapore dental care is expensive but among the best in Asia. Many clinics offer same-day appointments. Q&M Dental is the largest chain.",
            "emergencyTip": "National Dental Centre Singapore handles complex dental emergencies. Hospital emergency departments at SGH and NUH also provide dental emergency care."
        },
        "mentalHealth": {
            "crisisLine": "Samaritans of Singapore: 1-767 (1800-221-4444, 24/7)",
            "internationalLine": "IMH Mental Health Helpline: 6389 2222",
            "englishTherapists": "Widely available. English is an official language. Many international therapists and counselors practice in Singapore.",
            "notes": "Singapore has good mental health services. IMH (Institute of Mental Health) is the main public facility. Private therapists charge SGD $150-300 per session."
        },
        "accessibilityInfo": {
            "overview": "Singapore is one of the most accessible cities in Asia. Strict building codes ensure wheelchair access in modern buildings. Excellent accessible public transport.",
            "hospitalAccess": "All hospitals are fully wheelchair accessible.",
            "transport": "MRT (subway) is fully accessible with elevators and platform screen doors. All public buses are wheelchair accessible. Accessible taxis available through booking.",
            "tips": "Gardens by the Bay, Sentosa, and most attractions are wheelchair accessible. Hawker centres may have limited space. SG Enable provides accessibility resources."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Voluntary use in healthcare settings.",
            "testing": "ART tests at pharmacies (SGD $5-10). PCR at clinics (SGD $60-120).",
            "notes": "Singapore removed all COVID restrictions. Dengue is a more significant ongoing health concern."
        },
        "insuranceClaimProcess": "Singapore hospitals are efficient with insurance documentation. Most private hospitals offer direct billing with international insurers. Keep all receipts and Medisave/insurance claim forms. Hospitals provide English documentation as standard.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "VN": {
        "hospitals": [
            {"name": "FV Hospital", "nearTouristArea": "District 7, Ho Chi Minh City", "phone": "+84-28-5411-3333", "englishSpeaking": True, "notes": "International-standard hospital. English and French speaking. JCI-accredited."},
            {"name": "Vinmec International Hospital", "nearTouristArea": "Multiple locations — Hanoi, HCMC, Nha Trang, Da Nang", "phone": "+84-24-3974-3556 (Hanoi)", "englishSpeaking": True, "notes": "Vietnam's premier private hospital chain. International patient services."},
            {"name": "Family Medical Practice", "nearTouristArea": "District 1, HCMC / Old Quarter, Hanoi / Da Nang", "phone": "+84-28-3822-7848 (HCMC)", "englishSpeaking": True, "notes": "International clinic chain. Walk-in and emergency services. Highly recommended for tourists."},
            {"name": "Hoan My Da Nang Hospital", "nearTouristArea": "Da Nang / near Hoi An", "phone": "+84-236-3650-676", "englishSpeaking": True, "notes": "Private hospital serving central Vietnam's tourist region."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Tôi cần thuốc đau đầu", "transliteration": "Toy kan too-ok dow dow"},
            {"english": "I have a stomachache", "local": "Tôi bị đau bụng", "transliteration": "Toy bee dow bung"},
            {"english": "I'm allergic to...", "local": "Tôi bị dị ứng với...", "transliteration": "Toy bee zee ung voy..."},
            {"english": "Where is the nearest pharmacy?", "local": "Nhà thuốc gần nhất ở đâu?", "transliteration": "Nya too-ok gun nyut uh dow?"},
            {"english": "I need a doctor", "local": "Tôi cần bác sĩ", "transliteration": "Toy kan bak see"},
        ],
        "dentalCare": {
            "availability": "Dental care in major cities is good and very affordable. HCMC and Hanoi have international-standard clinics.",
            "costRange": "$10-30 for consultation; $20-60 for fillings; $15-50 for extractions",
            "notes": "Vietnam is an emerging dental tourism destination. Elite Dental, Westcoast International, and Dr. Hung dental clinics in HCMC are popular with foreigners. Quality varies widely — choose carefully.",
            "emergencyTip": "FV Hospital and Vinmec have dental departments for emergencies. Family Medical Practice clinics can provide referrals."
        },
        "mentalHealth": {
            "crisisLine": "1800 599 920 (Mental Health Hotline, Vietnamese-language)",
            "internationalLine": "Contact your embassy for English-language crisis support",
            "englishTherapists": "Limited. Some available through FV Hospital and Family Medical Practice in HCMC and Hanoi.",
            "notes": "Mental health services in English are very limited in Vietnam. International clinics in HCMC and Hanoi offer psychiatric services. For serious mental health concerns, consider medical evacuation to Bangkok or Singapore."
        },
        "accessibilityInfo": {
            "overview": "Vietnam's accessibility is very limited. Sidewalks are often blocked by motorbikes, streets are chaotic, and most buildings lack wheelchair access.",
            "hospitalAccess": "International hospitals (FV, Vinmec) are wheelchair accessible. Public hospitals have limited access.",
            "transport": "No accessible public transport. Grab (ride-hailing) is the best option. Traffic is chaotic — crossing streets is challenging for anyone.",
            "tips": "Ho Chi Minh City and Hanoi's old quarters are extremely challenging for wheelchair users. Newer areas and resorts are more accessible. Hire a guide for assistance. Ha Long Bay cruises vary in accessibility — confirm before booking."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Some indoor venues may request masks.",
            "testing": "Tests available at hospitals and clinics. Cost: $10-30 for PCR.",
            "notes": "Vietnam removed all COVID entry restrictions. Dengue fever and food/water safety are more relevant health concerns."
        },
        "insuranceClaimProcess": "International hospitals accept direct billing from some insurers. Local facilities require upfront cash payment. Keep all receipts (hóa đơn) and medical reports. Family Medical Practice and FV Hospital provide English documentation as standard. File claims promptly.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "ID": {
        "hospitals": [
            {"name": "BIMC Hospital Kuta", "nearTouristArea": "Kuta Beach, Bali", "phone": "+62-361-761-263", "englishSpeaking": True, "notes": "Bali's premier tourist hospital. 24/7 emergency. Direct billing with many insurers."},
            {"name": "Siloam Hospitals Bali", "nearTouristArea": "Kuta / Seminyak area, Bali", "phone": "+62-361-779-900", "englishSpeaking": True, "notes": "Part of Indonesia's largest private hospital chain. Modern facilities."},
            {"name": "Pondok Indah Hospital", "nearTouristArea": "South Jakarta", "phone": "+62-21-765-7525", "englishSpeaking": True, "notes": "Top private hospital in Jakarta. International patient department."},
            {"name": "RS Kasih Ibu Denpasar", "nearTouristArea": "Denpasar, Bali (near Ubud)", "phone": "+62-361-223-036", "englishSpeaking": True, "notes": "Central Bali location. Good for Ubud-area tourists."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Saya butuh obat sakit kepala", "transliteration": ""},
            {"english": "I have a stomachache", "local": "Saya sakit perut", "transliteration": ""},
            {"english": "I'm allergic to...", "local": "Saya alergi terhadap...", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Di mana apotek terdekat?", "transliteration": ""},
            {"english": "I need a doctor", "local": "Saya butuh dokter", "transliteration": ""},
        ],
        "dentalCare": {
            "availability": "Dental care available in Bali and Jakarta. Quality ranges from basic to international standard.",
            "costRange": "$15-40 for consultation; $25-80 for fillings; $20-60 for extractions",
            "notes": "Bali has several expat-oriented dental clinics (Bali 911 Dental, ARC Dental Clinic). Quality in Ubud and tourist areas is generally good. Jakarta has excellent private dental hospitals.",
            "emergencyTip": "BIMC Hospital Kuta has dental services. For complex procedures, consider Singapore or Bangkok. Dental pain relief available at pharmacies (apotek)."
        },
        "mentalHealth": {
            "crisisLine": "119 ext. 8 (Ministry of Health mental health line)",
            "internationalLine": "Into The Light: support for mental health awareness in Indonesia",
            "englishTherapists": "Limited. Available at BIMC Bali and international clinics in Jakarta. Online therapy platforms accessible.",
            "notes": "Mental health services in English are limited to international clinics in Bali and Jakarta. For serious mental health concerns, medical evacuation to Singapore may be necessary."
        },
        "accessibilityInfo": {
            "overview": "Indonesia's accessibility is very limited, especially in Bali where terrain is hilly and infrastructure is informal. Major hotels and resorts are generally accessible.",
            "hospitalAccess": "International hospitals (BIMC, Siloam) are wheelchair accessible. Local clinics may not be.",
            "transport": "No accessible public transport in Bali. Private drivers are the main transport option. Grab available in major cities. Roads and sidewalks are challenging for wheelchairs.",
            "tips": "Rice terraces, temples, and waterfalls in Bali are largely inaccessible for wheelchair users. Beach resorts are generally the most accessible option. Book accessible rooms well in advance."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates.",
            "testing": "Tests available at hospitals and clinics. PCR: $20-50.",
            "notes": "Indonesia removed all COVID entry restrictions. Dengue fever, rabies (from monkeys), and food/water safety are more significant health concerns in Bali."
        },
        "insuranceClaimProcess": "BIMC Hospital Bali offers direct billing with most international insurers. Other hospitals may require upfront payment. Keep all receipts (kwitansi) and medical reports (surat keterangan medis). Hospitals can provide English documentation on request.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "NZ": {
        "hospitals": [
            {"name": "Auckland City Hospital", "nearTouristArea": "Auckland CBD / Sky Tower", "phone": "+64-9-367-0000", "englishSpeaking": True, "notes": "New Zealand's largest hospital. 24/7 emergency department."},
            {"name": "Wellington Regional Hospital", "nearTouristArea": "Newtown, Wellington", "phone": "+64-4-385-5999", "englishSpeaking": True, "notes": "Capital city hospital. Full emergency department."},
            {"name": "Christchurch Hospital", "nearTouristArea": "Central Christchurch / Canterbury region", "phone": "+64-3-364-0640", "englishSpeaking": True, "notes": "Main hospital for the South Island's largest city."},
            {"name": "Queenstown Lakes District Hospital", "nearTouristArea": "Queenstown / adventure tourism hub", "phone": "+64-3-441-0015", "englishSpeaking": True, "notes": "Serves the Queenstown adventure tourism area. Handles adventure sport injuries."},
        ],
        "pharmacyPhrases": [
            {"english": "Where is the nearest pharmacy?", "local": "Where is the nearest chemist?", "transliteration": "New Zealanders typically say 'chemist' or 'pharmacy'"},
        ],
        "dentalCare": {
            "availability": "Good dental care but expensive. Not covered by public healthcare for adults.",
            "costRange": "NZD $80-150 for consultation; NZD $150-400 for fillings; NZD $200-500 for extractions",
            "notes": "Dental care in New Zealand is high quality but costly. Emergency dental care available in major cities. Most dentists accept walk-ins for emergencies.",
            "emergencyTip": "Call Healthline at 0800 611 116 for dental emergency advice. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "1737 (Need to talk? — free, 24/7, call or text)",
            "internationalLine": "Lifeline: 0800 543 354",
            "englishTherapists": "Widely available. English is the primary language.",
            "notes": "New Zealand has good mental health services. Crisis support available 24/7. GPs can provide mental health referrals. Private therapy: NZD $120-200 per session."
        },
        "accessibilityInfo": {
            "overview": "New Zealand has good accessibility in cities and major tourist attractions. Adventure activities and natural sites may have limitations.",
            "hospitalAccess": "All public hospitals are wheelchair accessible.",
            "transport": "Public buses in major cities are accessible. Mobility parking widely available. Some interisland ferries are accessible. Domestic flights accommodate wheelchairs.",
            "tips": "Many Great Walks have sections accessible to wheelchair users. Milford Sound cruises are accessible. Adventure activity operators in Queenstown increasingly offer adaptive options. CCS Disability Action provides travel information."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates.",
            "testing": "RATs available at pharmacies. PCR available at GP clinics.",
            "notes": "New Zealand removed all COVID entry restrictions. The main health risks for travelers are adventure sports injuries and sun exposure."
        },
        "insuranceClaimProcess": "ACC (Accident Compensation Corporation) covers treatment for injuries sustained in New Zealand, including tourists — at no cost. For illness (non-injury), keep all receipts and GP notes for insurance claims. NZ healthcare for non-residents is not free for illness-related treatment.",
        "eu112": False,
        "datePublished": "2026-03-15",
    },

    "CH": {
        "hospitals": [
            {"name": "Universitätsspital Zürich", "nearTouristArea": "Central Zurich", "phone": "+41-44-255-11-11", "englishSpeaking": True, "notes": "Top-rated university hospital. English widely spoken."},
            {"name": "Hôpitaux Universitaires de Genève (HUG)", "nearTouristArea": "Geneva / Lake Geneva", "phone": "+41-22-372-33-11", "englishSpeaking": True, "notes": "Geneva's main hospital. French and English speaking."},
            {"name": "Inselspital Bern", "nearTouristArea": "Bern Old Town", "phone": "+41-31-632-21-11", "englishSpeaking": True, "notes": "University hospital serving the capital. Excellent trauma center."},
            {"name": "Kantonsspital Graubünden", "nearTouristArea": "Chur (gateway to Davos/St. Moritz)", "phone": "+41-81-256-61-11", "englishSpeaking": True, "notes": "Regional hospital for the ski resort areas. Experienced with mountain injuries."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ich brauche Medizin gegen Kopfschmerzen", "transliteration": "German; French: J'ai besoin d'un médicament contre le mal de tête; Italian: Ho bisogno di una medicina per il mal di testa"},
            {"english": "Where is the nearest pharmacy?", "local": "Wo ist die nächste Apotheke?", "transliteration": "French: Où est la pharmacie la plus proche? Italian: Dov'è la farmacia più vicina?"},
        ],
        "dentalCare": {
            "availability": "Excellent but extremely expensive. Swiss dental care is among the most costly in the world.",
            "costRange": "CHF 150-300 for consultation; CHF 200-500 for fillings; CHF 300-800 for extractions",
            "notes": "Swiss dental care is not covered by mandatory health insurance (KVG/LAMal). Separate dental insurance needed. Quality is world-class. Many people travel to neighboring countries for cheaper dental care.",
            "emergencyTip": "Call the cantonal dental emergency service (Zahnärztlicher Notfalldienst). In Zurich: 044 401 13 13. Hospital emergency departments handle dental trauma."
        },
        "mentalHealth": {
            "crisisLine": "143 (Die Dargebotene Hand / La Main Tendue — 24/7, multilingual)",
            "internationalLine": "147 (Pro Juventute for young people)",
            "englishTherapists": "Available in Zurich, Geneva, Basel, and Bern through international practices. Switzerland has many multilingual therapists.",
            "notes": "Switzerland has excellent but expensive mental health services. Private therapy: CHF 150-250 per session. Basic health insurance covers psychiatric treatment with a referral."
        },
        "accessibilityInfo": {
            "overview": "Switzerland has excellent accessibility infrastructure. Strong legal protections and well-maintained facilities.",
            "hospitalAccess": "All hospitals are wheelchair accessible with modern facilities.",
            "transport": "Swiss trains (SBB) are highly accessible with call-ahead assistance. All major city trams and buses are low-floor. Mountain railways vary — check accessibility before booking.",
            "tips": "Many mountain destinations are accessible via cable cars and cogwheel railways. Swiss tourism offices provide detailed accessibility guides. Mobility International Switzerland provides resources."
        },
        "covidStatus": {
            "entryRequirements": "No COVID testing or vaccination requirements for entry.",
            "maskPolicy": "No mask mandates. Individual choice.",
            "testing": "Available at pharmacies and clinics. PCR: CHF 50-130.",
            "notes": "Switzerland removed all COVID restrictions. Healthcare costs are among the highest in the world — ensure adequate insurance coverage."
        },
        "insuranceClaimProcess": "Swiss healthcare is very expensive — an ER visit can cost CHF 1,000+. Travel insurance is essential. Keep all Rechnungen (invoices) and Arztberichte (medical reports). Swiss hospitals provide detailed documentation for insurance claims. Direct billing is rare — expect to pay upfront.",
        "eu112": True,
        "datePublished": "2026-03-15",
    },

    # ── Remaining countries with essential enrichment data ─────────────

    "AE": {
        "hospitals": [
            {"name": "Cleveland Clinic Abu Dhabi", "nearTouristArea": "Al Maryah Island, Abu Dhabi", "phone": "+971-2-501-9000", "englishSpeaking": True, "notes": "World-class hospital. Part of Cleveland Clinic network."},
            {"name": "Mediclinic City Hospital", "nearTouristArea": "Dubai Healthcare City / Downtown Dubai", "phone": "+971-4-435-9999", "englishSpeaking": True, "notes": "Close to Burj Khalifa and Dubai Mall. Emergency department."},
            {"name": "Rashid Hospital", "nearTouristArea": "Oud Metha, Dubai", "phone": "+971-4-219-2000", "englishSpeaking": True, "notes": "Major public trauma center. 24/7 emergency."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "أحتاج دواء للصداع", "transliteration": "Ahtaaj dawaa' lil-sudaa'"},
            {"english": "I need a doctor", "local": "أحتاج طبيب", "transliteration": "Ahtaaj tabeeb"},
            {"english": "Where is the nearest pharmacy?", "local": "أين أقرب صيدلية؟", "transliteration": "Ayn aqrab saidaliyya?"},
        ],
        "dentalCare": {"availability": "Excellent dental care in Dubai and Abu Dhabi. Modern clinics with latest technology.", "costRange": "AED 200-500 ($55-135) for consultation; AED 500-1,500 ($135-410) for fillings", "notes": "Dental care in the UAE is expensive but high quality. Many dentists trained internationally.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Many dental clinics open evenings and weekends."},
        "mentalHealth": {"crisisLine": "800-HOPE (4673) — Dubai Community Health Center", "internationalLine": "Aman Center: 800-7283", "englishTherapists": "Widely available in Dubai and Abu Dhabi. English is commonly used in healthcare.", "notes": "Mental health services are growing in the UAE. Private therapy: AED 500-1,000 per session."},
        "accessibilityInfo": {"overview": "UAE has good accessibility in modern areas. Dubai Metro is one of the most accessible transit systems globally.", "hospitalAccess": "Modern hospitals are fully accessible.", "transport": "Dubai Metro is fully wheelchair accessible. RTA provides accessible taxis. Most malls and attractions are accessible.", "tips": "Desert safaris and older souks may have limited accessibility. Modern attractions like Dubai Mall and Burj Khalifa are wheelchair accessible."},
        "covidStatus": {"entryRequirements": "No COVID testing or vaccination requirements.", "maskPolicy": "No mask mandates.", "testing": "Available at pharmacies and clinics.", "notes": "UAE removed all COVID restrictions. Heat-related illness is a bigger health concern."},
        "insuranceClaimProcess": "UAE hospitals are accustomed to insurance. Many offer direct billing. Keep all receipts and medical reports in English (standard). Dubai Health Authority regulates healthcare pricing.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "AR": {
        "hospitals": [
            {"name": "Hospital Italiano de Buenos Aires", "nearTouristArea": "Almagro, Buenos Aires", "phone": "+54-11-4959-0200", "englishSpeaking": True, "notes": "Argentina's top-rated hospital. International patient department."},
            {"name": "Hospital Alemán", "nearTouristArea": "Recoleta, Buenos Aires", "phone": "+54-11-4827-7000", "englishSpeaking": True, "notes": "Private hospital in the tourist-friendly Recoleta neighborhood."},
            {"name": "Hospital Británico", "nearTouristArea": "Barracas, Buenos Aires", "phone": "+54-11-4309-6400", "englishSpeaking": True, "notes": "British-founded hospital with English-speaking staff."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicamento para el dolor de cabeza", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "¿Dónde está la farmacia más cercana?", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Good dental care at affordable prices. Buenos Aires is a dental tourism destination.", "costRange": "$20-50 for consultation; $30-100 for fillings", "notes": "Quality is good in Buenos Aires. Argentina is increasingly popular for dental tourism due to favorable exchange rates.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Pharmacies can provide pain relief."},
        "mentalHealth": {"crisisLine": "135 (Centro de Asistencia al Suicida — 24/7)", "internationalLine": "Buenos Aires has a strong psychotherapy culture — therapists widely available.", "englishTherapists": "Available in Buenos Aires, especially in Palermo and Recoleta neighborhoods.", "notes": "Argentina has the highest number of psychologists per capita in the world. Finding an English-speaking therapist in Buenos Aires is relatively easy."},
        "accessibilityInfo": {"overview": "Buenos Aires has been improving accessibility. Newer buses are low-floor. Sidewalks in older neighborhoods can be uneven.", "hospitalAccess": "Private hospitals are wheelchair accessible.", "transport": "Subte (metro) has limited accessibility. Colectivos (buses) are increasingly accessible. Taxis are the most flexible option.", "tips": "San Telmo cobblestones and La Boca sidewalks can be challenging. Puerto Madero is the most accessible neighborhood."},
        "covidStatus": {"entryRequirements": "No COVID requirements for entry.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies and clinics.", "notes": "Argentina removed all COVID restrictions."},
        "insuranceClaimProcess": "Public hospitals (hospitales públicos) provide free emergency care to everyone, including tourists. Private hospitals require payment or insurance. Keep all facturas and medical reports. Request English documentation.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "BE": {
        "hospitals": [
            {"name": "UZ Brussel (Universitair Ziekenhuis)", "nearTouristArea": "Jette, Brussels", "phone": "+32-2-477-41-11", "englishSpeaking": True, "notes": "University hospital. English widely spoken."},
            {"name": "Cliniques Universitaires Saint-Luc", "nearTouristArea": "Woluwe-Saint-Lambert, Brussels", "phone": "+32-2-764-11-11", "englishSpeaking": True, "notes": "Major university hospital. French and English speaking."},
            {"name": "AZ Sint-Jan Brugge", "nearTouristArea": "Bruges city center", "phone": "+32-50-45-21-11", "englishSpeaking": True, "notes": "Main hospital serving Bruges tourists."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "J'ai besoin d'un médicament contre le mal de tête", "transliteration": "French; Dutch: Ik heb medicijn nodig tegen hoofdpijn"},
            {"english": "Where is the nearest pharmacy?", "local": "Où est la pharmacie la plus proche ?", "transliteration": "Dutch: Waar is de dichtstbijzijnde apotheek?"},
        ],
        "dentalCare": {"availability": "Good dental care. EHIC covers emergency dental for EU citizens.", "costRange": "€30-80 for consultation; €60-200 for fillings", "notes": "Belgian dental care is affordable by Western European standards.", "emergencyTip": "Call 1733 for after-hours medical/dental assistance."},
        "mentalHealth": {"crisisLine": "1813 (Zelfmoordlijn — Dutch); 0800 32 123 (Centre de Prévention du Suicide — French)", "internationalLine": "Tele-Onthaal: 106 (Dutch); Télé-Accueil: 107 (French)", "englishTherapists": "Available in Brussels, which is highly international.", "notes": "Belgium has good mental health services. Brussels has many English-speaking therapists due to the EU/NATO presence."},
        "accessibilityInfo": {"overview": "Belgium has good accessibility in modern areas. Historic city centers (Bruges, Ghent) with cobblestones can be challenging.", "hospitalAccess": "Hospitals are wheelchair accessible.", "transport": "Brussels Metro has elevator access. STIB/MIVB buses are low-floor. SNCB trains offer assistance for disabled travelers.", "tips": "Bruges is walkable but cobblestones are difficult for wheelchairs. Ghent's tram system is accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "Belgian healthcare uses a reimbursement system. Keep attestation de soins (care certificates) from doctors. EU citizens with EHIC get partial reimbursement. Non-EU visitors pay upfront and claim from travel insurance.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "CO": {
        "hospitals": [
            {"name": "Fundación Santa Fe de Bogotá", "nearTouristArea": "Northern Bogotá", "phone": "+57-1-603-0303", "englishSpeaking": True, "notes": "JCI-accredited. One of Latin America's best hospitals."},
            {"name": "Hospital Pablo Tobón Uribe", "nearTouristArea": "Medellín", "phone": "+57-4-441-0855", "englishSpeaking": True, "notes": "Top hospital in Medellín. International patient services."},
            {"name": "Clínica Imbanaco", "nearTouristArea": "Cali", "phone": "+57-2-682-1000", "englishSpeaking": True, "notes": "JCI-accredited hospital in Cali."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "¿Dónde está la droguería más cercana?", "transliteration": "Colombians say 'droguería' for pharmacy"},
        ],
        "dentalCare": {"availability": "Colombia is a major dental tourism destination. Excellent care at 50-70% less than US prices.", "costRange": "$20-50 for consultation; $30-100 for fillings; dental implants from $800", "notes": "Bogotá, Medellín, and Cartagena have excellent dental clinics. Many dentists trained in the US.", "emergencyTip": "Hospital emergency departments handle dental emergencies. DentalPlan and Bocca clinics are popular with foreigners."},
        "mentalHealth": {"crisisLine": "106 (Línea 106 — 24/7 crisis line)", "internationalLine": "Línea de la Vida: 01 8000 113 113", "englishTherapists": "Available in Bogotá and Medellín, especially in areas with large expat communities.", "notes": "Colombia's mental health services are growing. Private therapy: $25-60 per session."},
        "accessibilityInfo": {"overview": "Accessibility varies widely. Modern areas in Bogotá and Medellín are improving. Cartagena's old city has cobblestones and steps.", "hospitalAccess": "Major private hospitals are accessible.", "transport": "TransMilenio in Bogotá has accessible stations. Medellín's Metro and cable cars have accessibility features. Taxis are the most flexible option.", "tips": "Medellín's Metro system is one of the most accessible in Latin America. Bogotá's altitude (2,640m) requires acclimatization."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies and clinics.", "notes": "Colombia removed all COVID restrictions. Altitude sickness in Bogotá and dengue in lowland areas are more relevant concerns."},
        "insuranceClaimProcess": "Colombian private hospitals are experienced with international patients. Keep facturas and historias clínicas. Fundación Santa Fe can provide English documentation. Public hospitals provide free emergency care.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "CR": {
        "hospitals": [
            {"name": "Hospital CIMA San José", "nearTouristArea": "Escazú, San José (near city center)", "phone": "+506-2208-1000", "englishSpeaking": True, "notes": "JCI-accredited private hospital. International patient services."},
            {"name": "Clínica Bíblica", "nearTouristArea": "Downtown San José", "phone": "+506-2522-1000", "englishSpeaking": True, "notes": "Historic private hospital. Popular with medical tourists."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Costa Rica is a popular dental tourism destination. High quality at 40-60% less than US prices.", "costRange": "$30-60 for consultation; $50-150 for fillings", "notes": "San José area has many dental clinics catering to North American tourists.", "emergencyTip": "Hospital CIMA and Clínica Bíblica have dental departments."},
        "mentalHealth": {"crisisLine": "Línea de crisis: 2272-3774", "internationalLine": "IAFA (Instituto sobre Alcoholismo y Farmacodependencia): 800-4232-800", "englishTherapists": "Available in San José and tourist areas.", "notes": "Limited English-language mental health services outside San José."},
        "accessibilityInfo": {"overview": "Accessibility is limited. Modern hotels and hospitals are accessible. Streets and nature areas have significant barriers.", "hospitalAccess": "Private hospitals are accessible.", "transport": "Limited accessible public transport. Taxis are the best option.", "tips": "Rainforest and volcano tours have limited wheelchair access. Beach resorts are generally more accessible. Manuel Antonio has some accessible trails."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics.", "notes": "Dengue and food/water safety are more relevant health concerns."},
        "insuranceClaimProcess": "Private hospitals often accept direct billing from US insurers. Keep all receipts. Hospital CIMA has an insurance desk.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "CU": {
        "hospitals": [
            {"name": "Clínica Central Cira García", "nearTouristArea": "Miramar, Havana", "phone": "+53-7-204-2811", "englishSpeaking": True, "notes": "Designated foreigners' clinic. International standard. Payment in CUC/USD."},
            {"name": "Hospital Hermanos Ameijeiras", "nearTouristArea": "Central Havana / Malecón", "phone": "+53-7-876-1000", "englishSpeaking": True, "notes": "Major public hospital. Some doctors speak English."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Dental care available but supplies may be limited. Clínica Cira García serves foreigners.", "costRange": "$20-50 for consultation; $30-80 for fillings", "notes": "Cuba has well-trained dentists but limited supplies and equipment. Bring dental supplies if you have ongoing dental needs.", "emergencyTip": "Go to Clínica Cira García for dental emergencies. Bring cash as payment."},
        "mentalHealth": {"crisisLine": "Contact your embassy or Clínica Cira García", "notes": "Mental health services in English are very limited. Contact your embassy for assistance."},
        "accessibilityInfo": {"overview": "Cuba's accessibility is very limited. Havana's colonial architecture includes many steps and narrow sidewalks.", "hospitalAccess": "Clínica Cira García has some wheelchair access. Other facilities are limited.", "transport": "No accessible public transport. Classic cars used as taxis are not wheelchair friendly.", "tips": "Cuba is very challenging for wheelchair users. Plan carefully and consider hiring a private driver with an accessible vehicle."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals.", "notes": "Cuba removed COVID entry requirements. Bring sufficient medications as pharmacies may have limited stock."},
        "insuranceClaimProcess": "Travel insurance is required for Cuba entry. Clínica Cira García handles foreigner billing. Pay in cash (USD/EUR) and keep all receipts. Cuban medical documentation may need translation for insurance claims.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "CZ": {
        "hospitals": [
            {"name": "Nemocnice Na Homolce", "nearTouristArea": "Prague 5 (accessible from Old Town)", "phone": "+420-257-271-111", "englishSpeaking": True, "notes": "Preferred hospital for foreigners. International department."},
            {"name": "Motol University Hospital", "nearTouristArea": "Prague 5", "phone": "+420-224-431-111", "englishSpeaking": True, "notes": "Largest hospital in the Czech Republic."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Potřebuji lék na bolest hlavy", "transliteration": "Pot-zheh-boo-yee lek na bolest hlavy"},
            {"english": "Where is the nearest pharmacy?", "local": "Kde je nejbližší lékárna?", "transliteration": "Gde ye ney-bleesh-shee le-kar-na?"},
            {"english": "I need a doctor", "local": "Potřebuji lékaře", "transliteration": "Pot-zheh-boo-yee le-ka-zhe"},
        ],
        "dentalCare": {"availability": "Good quality at affordable prices. Czech Republic is a dental tourism destination.", "costRange": "€25-60 for consultation; €40-120 for fillings", "notes": "Prague has many dental clinics catering to tourists. Quality is high and prices are 50-70% lower than Western Europe.", "emergencyTip": "Hospital emergency departments handle dental emergencies."},
        "mentalHealth": {"crisisLine": "116 111 (Linka bezpečí — Czech language)", "internationalLine": "Czech Psychiatric Association can provide English referrals", "englishTherapists": "Available in Prague through international practices.", "notes": "English-language mental health services concentrated in Prague."},
        "accessibilityInfo": {"overview": "Prague's historic center with cobblestones and hills is challenging. Modern areas are better.", "hospitalAccess": "Major hospitals are wheelchair accessible.", "transport": "Prague Metro has limited elevator access. Trams are accessible at low-floor stops. Taxis are the most reliable option.", "tips": "Prague Castle and many historic sites have steps. Some have alternative wheelchair routes — check in advance."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies and clinics.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU citizens with EHIC receive emergency care. Keep all účtenky (receipts) and lékařské zprávy (medical reports). Na Homolce hospital provides English documentation.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "GR": {
        "hospitals": [
            {"name": "Athens Medical Center", "nearTouristArea": "Maroussi, Athens", "phone": "+30-210-686-7000", "englishSpeaking": True, "notes": "Private hospital group. International patient services."},
            {"name": "Hygeia Hospital", "nearTouristArea": "Maroussi, Athens", "phone": "+30-210-686-7000", "englishSpeaking": True, "notes": "Top-rated private hospital. English widely spoken."},
            {"name": "Venizeleio Hospital", "nearTouristArea": "Heraklion, Crete", "phone": "+30-2810-368-000", "englishSpeaking": True, "notes": "Main hospital serving Crete's tourist areas."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Χρειάζομαι φάρμακο για πονοκέφαλο", "transliteration": "Hriazome farmako gia ponokefalo"},
            {"english": "Where is the nearest pharmacy?", "local": "Πού είναι το πλησιέστερο φαρμακείο;", "transliteration": "Pou ine to plisyestero farmakio?"},
            {"english": "I need a doctor", "local": "Χρειάζομαι γιατρό", "transliteration": "Hriazome yatro"},
        ],
        "dentalCare": {"availability": "Good dental care at reasonable prices.", "costRange": "€30-70 for consultation; €50-150 for fillings", "notes": "Greek dental care is affordable. Tourist islands may have limited dental facilities.", "emergencyTip": "Hospital emergency departments handle dental emergencies. On islands, facilities may be basic — consider ferry to Athens for complex issues."},
        "mentalHealth": {"crisisLine": "1018 (Suicide prevention line)", "internationalLine": "Klimaka NGO: +30-210-521-1880", "englishTherapists": "Available in Athens. Limited on islands.", "notes": "Mental health services in English mainly in Athens. Island medical facilities are basic."},
        "accessibilityInfo": {"overview": "Greece's accessibility is challenging. Ancient sites, island terrain, and cobblestone streets create barriers.", "hospitalAccess": "Major hospitals in Athens are accessible. Island hospitals vary.", "transport": "Athens Metro is accessible. Island ferries have some accessibility. Taxis widely available.", "tips": "The Acropolis has a wheelchair-accessible elevator. Many islands have hilly terrain. Santorini's caldera villages are very difficult for wheelchairs."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies.", "notes": "All restrictions removed. Sun and heat-related illness are common tourist health concerns."},
        "insuranceClaimProcess": "EU citizens with EHIC access public hospitals. Greek public hospitals may be overcrowded. Private hospitals require payment — keep all receipts. English documentation available at private hospitals.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "HR": {
        "hospitals": [
            {"name": "KBC Zagreb", "nearTouristArea": "Zagreb city center", "phone": "+385-1-2388-888", "englishSpeaking": True, "notes": "Zagreb's main clinical hospital."},
            {"name": "OB Dubrovnik", "nearTouristArea": "Dubrovnik Old Town", "phone": "+385-20-431-777", "englishSpeaking": True, "notes": "Hospital serving Dubrovnik's tourist area."},
            {"name": "KBC Split", "nearTouristArea": "Split / Diocletian's Palace area", "phone": "+385-21-556-111", "englishSpeaking": True, "notes": "Major hospital serving Split and the Dalmatian coast."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Trebam lijek za glavobolju", "transliteration": ""},
            {"english": "I need a doctor", "local": "Trebam liječnika", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Good dental care. Croatia is a popular dental tourism destination.", "costRange": "€30-60 for consultation; €50-150 for fillings", "notes": "Zagreb and coastal cities have dental clinics catering to tourists. Prices 50-60% lower than Western Europe.", "emergencyTip": "Hospital emergency departments handle dental emergencies."},
        "mentalHealth": {"crisisLine": "Plavi Telefon: 01 4833 888", "englishTherapists": "Limited. Available in Zagreb.", "notes": "English mental health services mainly in Zagreb."},
        "accessibilityInfo": {"overview": "Croatia's accessibility is limited in historic areas. Dubrovnik's Old Town has many steps.", "hospitalAccess": "Major hospitals are accessible.", "transport": "Zagreb trams are partially accessible. Ferries to islands have basic accessibility.", "tips": "Dubrovnik's Old Town is extremely challenging for wheelchairs — steep limestone streets with many steps. Split's waterfront is more manageable."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU citizens with EHIC access public healthcare. Keep receipts and medical documentation. Tourist areas have doctors used to treating international patients.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "HU": {
        "hospitals": [
            {"name": "FirstMed Centers", "nearTouristArea": "District V, Budapest (near Parliament)", "phone": "+36-1-224-9090", "englishSpeaking": True, "notes": "International clinic designed for foreigners. English-first."},
            {"name": "Semmelweis University Hospital", "nearTouristArea": "Central Budapest", "phone": "+36-1-459-1500", "englishSpeaking": True, "notes": "Major university hospital."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Fejfájás elleni gyógyszerre van szükségem", "transliteration": "Fey-fah-yash elleni dyodj-serre van sook-shay-gem"},
            {"english": "Where is the nearest pharmacy?", "local": "Hol van a legközelebbi gyógyszertár?", "transliteration": "Hol van a leg-kuh-zeleb-bee dyodj-sair-tar?"},
            {"english": "I need a doctor", "local": "Orvosra van szükségem", "transliteration": "Or-vosh-ra van sook-shay-gem"},
        ],
        "dentalCare": {"availability": "Hungary is Europe's dental tourism capital, especially Budapest.", "costRange": "€25-50 for consultation; €40-100 for fillings; dental implants from €400-800", "notes": "Budapest has hundreds of dental clinics catering to tourists, especially from the UK and Germany. Quality is high and prices are 50-70% lower than Western Europe.", "emergencyTip": "FirstMed Centers handle dental emergencies with English-speaking dentists."},
        "mentalHealth": {"crisisLine": "116 123 (Lelki Elsősegély — crisis line)", "englishTherapists": "Available in Budapest through FirstMed and international practices.", "notes": "English mental health services concentrated in Budapest."},
        "accessibilityInfo": {"overview": "Budapest has made accessibility improvements but historic areas, especially Buda's Castle District, are challenging.", "hospitalAccess": "Major hospitals are accessible.", "transport": "Budapest Metro Line 4 is fully accessible. Other lines have limited access. Trams vary. Taxis available.", "tips": "Buda Castle hill has limited wheelchair access. Pest side is generally flatter and more accessible. Thermal baths vary in accessibility."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU citizens with EHIC access public healthcare. Private clinics like FirstMed accept many international insurance plans. Keep all receipts and medical documentation.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "IE": {
        "hospitals": [
            {"name": "St James's Hospital", "nearTouristArea": "Dublin 8 (near Guinness Storehouse)", "phone": "+353-1-410-3000", "englishSpeaking": True, "notes": "Ireland's largest hospital. Major emergency department."},
            {"name": "Mater Misericordiae University Hospital", "nearTouristArea": "Dublin 7 (near city center)", "phone": "+353-1-803-2000", "englishSpeaking": True, "notes": "Central Dublin teaching hospital."},
        ],
        "pharmacyPhrases": [{"english": "Where is the nearest pharmacy?", "local": "Where is the nearest chemist?", "transliteration": "Irish people say 'chemist' for pharmacy"}],
        "dentalCare": {"availability": "Good dental care but can be expensive.", "costRange": "€50-100 for consultation; €100-250 for fillings", "notes": "Irish dental care is high quality. Emergency dental services available in Dublin.", "emergencyTip": "Call the Dublin Dental Hospital emergency line: 01-612-7200."},
        "mentalHealth": {"crisisLine": "Samaritans: 116 123 (free, 24/7)", "internationalLine": "Pieta House: 1800 247 247", "englishTherapists": "Widely available.", "notes": "Ireland has good mental health services. HSE provides public mental health care."},
        "accessibilityInfo": {"overview": "Ireland has good accessibility in modern buildings. Rural areas and historic sites vary.", "hospitalAccess": "All hospitals are wheelchair accessible.", "transport": "Dublin Bus and Luas trams are accessible. Irish Rail offers assistance. Taxis available.", "tips": "Cliffs of Moher visitor center is wheelchair accessible. Many castle/historic sites have limited access."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU citizens with EHIC access public emergency care. Non-EU visitors pay for healthcare. Keep all receipts. GPs charge €50-60 per visit.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "IL": {
        "hospitals": [
            {"name": "Ichilov (Tel Aviv Sourasky Medical Center)", "nearTouristArea": "Central Tel Aviv / beach area", "phone": "+972-3-697-4444", "englishSpeaking": True, "notes": "Tel Aviv's main hospital. English widely spoken."},
            {"name": "Hadassah Medical Center", "nearTouristArea": "Ein Kerem, Jerusalem", "phone": "+972-2-677-7111", "englishSpeaking": True, "notes": "World-renowned hospital in Jerusalem."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "אני צריך תרופה לכאב ראש", "transliteration": "Ani tzarich trufa le-ke'ev rosh"},
            {"english": "I need a doctor", "local": "אני צריך רופא", "transliteration": "Ani tzarich rofeh"},
        ],
        "dentalCare": {"availability": "Excellent dental care. Israel is an advanced medical country.", "costRange": "₪200-500 ($55-135) for consultation; ₪400-1,200 ($110-330) for fillings", "notes": "Israeli dental care is high quality but expensive. Many dentists speak English.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Terem urgent care clinics also available."},
        "mentalHealth": {"crisisLine": "ERAN: 1201 (24/7 emotional support, Hebrew/Arabic/English)", "internationalLine": "NATAL: 1-800-363-363 (trauma helpline)", "englishTherapists": "Widely available, especially in Tel Aviv.", "notes": "Israel has extensive mental health services. Many therapists are English-speaking."},
        "accessibilityInfo": {"overview": "Israel has strong accessibility laws. Modern areas are well-equipped. Old cities (Jerusalem's Old City) are very challenging.", "hospitalAccess": "All hospitals are wheelchair accessible.", "transport": "Tel Aviv light rail is accessible. Egged buses are accessible. Taxis available.", "tips": "Jerusalem's Old City is extremely difficult for wheelchairs — narrow stone alleys and many steps. The Western Wall has a wheelchair-accessible area."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics and HMOs.", "notes": "All restrictions removed. Check current security situation before travel."},
        "insuranceClaimProcess": "Israeli hospitals provide detailed documentation in English and Hebrew. Keep all receipts. Kupot Holim (HMOs) provide care for residents. Tourists pay out-of-pocket and claim from travel insurance.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "IS": {
        "hospitals": [
            {"name": "Landspítali (National University Hospital)", "nearTouristArea": "Central Reykjavík", "phone": "+354-543-1000", "englishSpeaking": True, "notes": "Iceland's only major hospital. English universally spoken."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ég þarf lyf gegn höfuðverk", "transliteration": "Yeg tharf leef gegn huh-vuth-verk"},
            {"english": "I need a doctor", "local": "Ég þarf lækni", "transliteration": "Yeg tharf like-nee"},
        ],
        "dentalCare": {"availability": "Dental care available but expensive. Limited outside Reykjavík.", "costRange": "ISK 10,000-25,000 ($70-180) for consultation", "notes": "Iceland has good dental care but it's expensive. Limited options outside Reykjavík.", "emergencyTip": "Landspítali emergency department handles dental emergencies. After-hours dental service available through 1770 health line."},
        "mentalHealth": {"crisisLine": "1717 (Red Cross crisis line)", "internationalLine": "112 for emergencies", "englishTherapists": "Available in Reykjavík. English is widely spoken.", "notes": "Iceland has good mental health services. English widely spoken by healthcare providers."},
        "accessibilityInfo": {"overview": "Reykjavík is reasonably accessible. Natural attractions vary widely.", "hospitalAccess": "Landspítali is fully accessible.", "transport": "Strætó buses are accessible. No rail system. Rental cars are the main transport for tourists.", "tips": "Many natural attractions (waterfalls, glaciers, geysers) have limited accessibility. The Golden Circle has varying trail accessibility. Check specific site accessibility before visiting."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at Landspítali.", "notes": "All restrictions removed. Hypothermia and weather-related injuries are more common health concerns."},
        "insuranceClaimProcess": "Icelandic healthcare is expensive for visitors. Hospital visits can cost ISK 50,000+. Keep all receipts. Landspítali provides documentation in English.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "JO": {
        "hospitals": [
            {"name": "King Hussein Medical Center", "nearTouristArea": "Amman city center", "phone": "+962-6-580-8000", "englishSpeaking": True, "notes": "Major military hospital. Excellent care."},
            {"name": "Jordan Hospital", "nearTouristArea": "Amman", "phone": "+962-6-560-8080", "englishSpeaking": True, "notes": "Private hospital. English widely spoken."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "بدي دوا للصداع", "transliteration": "Biddi dawa lil-sudaa'"},
            {"english": "I need a doctor", "local": "بدي دكتور", "transliteration": "Biddi duktoor"},
        ],
        "dentalCare": {"availability": "Good dental care at affordable prices. Jordan is a medical tourism destination.", "costRange": "JOD 15-40 ($20-55) for consultation; JOD 30-80 ($40-110) for fillings", "notes": "Amman has modern dental clinics. Many dentists speak English.", "emergencyTip": "Hospital emergency departments handle dental emergencies."},
        "mentalHealth": {"crisisLine": "110 (Family Protection Department)", "englishTherapists": "Available in Amman.", "notes": "Mental health services limited but growing. English-speaking therapists in Amman."},
        "accessibilityInfo": {"overview": "Accessibility is limited. Amman is hilly with uneven sidewalks. Petra is extremely challenging for wheelchair users.", "hospitalAccess": "Major hospitals are accessible.", "transport": "Limited public transport. Taxis are the main option.", "tips": "Petra's main trail has some wheelchair access with assistance but the site is mostly inaccessible for wheelchair users. Wadi Rum desert camps vary in accessibility."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals and clinics.", "notes": "Jordan removed all COVID restrictions."},
        "insuranceClaimProcess": "Jordanian hospitals provide documentation in English and Arabic. Keep all receipts. Private hospitals may require upfront payment.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "KE": {
        "hospitals": [
            {"name": "Aga Khan University Hospital", "nearTouristArea": "Nairobi (near Westlands/Karen)", "phone": "+254-20-366-2000", "englishSpeaking": True, "notes": "Kenya's top private hospital. JCI-accredited."},
            {"name": "Nairobi Hospital", "nearTouristArea": "Nairobi city center", "phone": "+254-20-284-5000", "englishSpeaking": True, "notes": "Premier private hospital. International patient department."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ninahitaji dawa ya maumivu ya kichwa", "transliteration": "Swahili (English is also widely spoken)"},
            {"english": "I need a doctor", "local": "Ninahitaji daktari", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Dental care available in Nairobi. Limited in safari/rural areas.", "costRange": "KSh 2,000-5,000 ($15-38) for consultation; KSh 3,000-10,000 ($23-77) for fillings", "notes": "Nairobi has quality dental clinics. Bring dental supplies on safari.", "emergencyTip": "Aga Khan and Nairobi Hospital have dental departments."},
        "mentalHealth": {"crisisLine": "0800 723 253 (Kenya Red Cross helpline)", "englishTherapists": "Available in Nairobi. English is an official language.", "notes": "Mental health services mainly in Nairobi. Limited outside the capital."},
        "accessibilityInfo": {"overview": "Kenya's accessibility is very limited outside modern hotels and hospitals.", "hospitalAccess": "Private hospitals in Nairobi are accessible. Rural facilities are not.", "transport": "Limited accessible transport. Safari vehicles are not wheelchair adapted. Private drivers best option.", "tips": "Safari lodges vary widely in accessibility — confirm before booking. Some lodges offer ground-floor rooms and adapted vehicles. Nairobi National Park has some accessible viewing points."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals in Nairobi.", "notes": "Malaria, typhoid, and safari-related injuries are more relevant health concerns."},
        "insuranceClaimProcess": "Private hospitals require payment upfront or insurance guarantee. Flying Doctors (AMREF) provides medical evacuation from safari areas. Keep all receipts. Aga Khan provides English documentation.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "LK": {
        "hospitals": [
            {"name": "Durdans Hospital", "nearTouristArea": "Colombo 3 (near Galle Face)", "phone": "+94-11-257-5411", "englishSpeaking": True, "notes": "Leading private hospital. English widely spoken."},
            {"name": "Lanka Hospitals", "nearTouristArea": "Colombo 5", "phone": "+94-11-553-0000", "englishSpeaking": True, "notes": "Modern private hospital with international standards."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "මට හිසරදයට බෙහෙත් ඕනෑ", "transliteration": "Mata hisa-radayata behet onay (Sinhala)"},
            {"english": "I need a doctor", "local": "මට වෛද්‍යවරයෙක් ඕනෑ", "transliteration": "Mata vaidya-varayek onay"},
        ],
        "dentalCare": {"availability": "Dental care available in Colombo and major cities.", "costRange": "LKR 2,000-5,000 ($7-17) for consultation; LKR 5,000-15,000 ($17-50) for fillings", "notes": "Very affordable dental care. Quality varies. Stick to private clinics in Colombo for best results.", "emergencyTip": "Hospital emergency departments handle dental emergencies."},
        "mentalHealth": {"crisisLine": "1926 (Sumithrayo — crisis helpline)", "englishTherapists": "Available in Colombo. English widely spoken in healthcare.", "notes": "Mental health services limited but English is widely spoken by healthcare professionals."},
        "accessibilityInfo": {"overview": "Accessibility is limited. Colombo is improving but rural areas and temples have significant barriers.", "hospitalAccess": "Private hospitals in Colombo are accessible.", "transport": "Limited accessible public transport. Tuk-tuks and taxis are main options.", "tips": "Ancient sites like Sigiriya Rock Fortress are extremely challenging for wheelchair users. Coastal resorts are generally more accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals.", "notes": "Dengue and food/water safety are more relevant concerns."},
        "insuranceClaimProcess": "Private hospitals may require upfront payment. Keep all receipts. English documentation available at major hospitals.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "MA": {
        "hospitals": [
            {"name": "Clinique Internationale de Marrakech", "nearTouristArea": "Marrakech (near Medina)", "phone": "+212-524-398-999", "englishSpeaking": True, "notes": "International private clinic. French and English spoken."},
            {"name": "Hôpital Cheikh Zaïd", "nearTouristArea": "Rabat", "phone": "+212-537-688-888", "englishSpeaking": True, "notes": "Modern hospital. International standard."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "بغيت دوا ديال الصداع", "transliteration": "Bghit dwa dyal s-suda' (Darija/Moroccan Arabic)"},
            {"english": "I need a doctor", "local": "بغيت طبيب", "transliteration": "Bghit tbib"},
            {"english": "Where is the nearest pharmacy?", "local": "فين أقرب فارماسي؟", "transliteration": "Fin aqrab pharmacie? (French: Où est la pharmacie la plus proche ?)"},
        ],
        "dentalCare": {"availability": "Dental care available and affordable. French-trained dentists common.", "costRange": "MAD 200-500 ($20-50) for consultation; MAD 500-1,500 ($50-150) for fillings", "notes": "Morocco has well-trained dentists, especially in cities. Many speak French and some English.", "emergencyTip": "Pharmacies can provide pain relief. Private clinics handle dental emergencies."},
        "mentalHealth": {"crisisLine": "Contact your embassy", "englishTherapists": "Limited. French-speaking therapists more common.", "notes": "Mental health services limited, especially in English. French-speaking therapists available in major cities."},
        "accessibilityInfo": {"overview": "Morocco's accessibility is very limited. Medinas have narrow alleys and uneven surfaces. Modern areas are better.", "hospitalAccess": "Private clinics are more accessible than public hospitals.", "transport": "Tramway in Casablanca and Rabat has some accessibility. Taxis are the main option.", "tips": "Medinas in Marrakech and Fez are extremely challenging for wheelchair users. Riads (traditional hotels) often have steps and narrow doorways. Modern hotels in new parts of cities are more accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics.", "notes": "All restrictions removed. Food/water safety and heat are more relevant concerns."},
        "insuranceClaimProcess": "Private clinics require upfront payment. Keep all receipts and ordonnances (prescriptions). Documentation in French and Arabic — request English where possible.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "MY": {
        "hospitals": [
            {"name": "Gleneagles Hospital Kuala Lumpur", "nearTouristArea": "Ampang, KL (near KLCC/Petronas Towers)", "phone": "+60-3-4141-3000", "englishSpeaking": True, "notes": "International hospital. English widely spoken. Direct billing with many insurers."},
            {"name": "Prince Court Medical Centre", "nearTouristArea": "Central KL (near KL Tower)", "phone": "+60-3-2160-0000", "englishSpeaking": True, "notes": "Luxury hospital. International patient department."},
            {"name": "Penang Adventist Hospital", "nearTouristArea": "George Town, Penang", "phone": "+60-4-222-7200", "englishSpeaking": True, "notes": "Serves Penang's tourist area. English spoken."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Saya perlukan ubat untuk sakit kepala", "transliteration": ""},
            {"english": "I need a doctor", "local": "Saya perlukan doktor", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Di mana farmasi yang terdekat?", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Excellent and affordable dental care. Malaysia is a top dental tourism destination.", "costRange": "RM 50-150 ($11-33) for consultation; RM 100-400 ($22-88) for fillings", "notes": "KL and Penang have world-class dental clinics at very affordable prices. Dental tourism is a major industry.", "emergencyTip": "International hospitals have dental departments. Many dental clinics offer same-day appointments."},
        "mentalHealth": {"crisisLine": "Befrienders: 03-7956-8145 (24/7)", "internationalLine": "MIASA: 1-800-18-0066", "englishTherapists": "Available in KL. English is widely spoken in Malaysia.", "notes": "Mental health services available in English. Private therapy: RM 150-400 per session."},
        "accessibilityInfo": {"overview": "Malaysia's accessibility is improving in modern areas. KL's modern infrastructure is accessible. Older areas and nature sites vary.", "hospitalAccess": "International hospitals are fully accessible.", "transport": "KL's LRT/MRT systems are accessible with elevators. KL Monorail has some accessibility. Grab (ride-hailing) widely available.", "tips": "Petronas Towers and KLCC area are wheelchair accessible. Cameron Highlands and Langkawi vary in accessibility."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics and pharmacies.", "notes": "All restrictions removed. Dengue is a more significant ongoing concern."},
        "insuranceClaimProcess": "Malaysian hospitals often offer direct billing with international insurers. Keep receipts and medical reports (in English). Prince Court and Gleneagles have dedicated insurance departments.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "NL": {
        "hospitals": [
            {"name": "Amsterdam UMC", "nearTouristArea": "Amsterdam Zuidas", "phone": "+31-20-566-9111", "englishSpeaking": True, "notes": "Major university hospital. English universally spoken."},
            {"name": "OLVG Hospital", "nearTouristArea": "Amsterdam East / near Vondelpark", "phone": "+31-20-599-9111", "englishSpeaking": True, "notes": "General hospital serving central Amsterdam."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ik heb iets nodig tegen hoofdpijn", "transliteration": ""},
            {"english": "I need a doctor", "local": "Ik heb een dokter nodig", "transliteration": ""},
            {"english": "Where is the nearest pharmacy?", "local": "Waar is de dichtstbijzijnde apotheek?", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Good dental care but can be expensive.", "costRange": "€30-80 for consultation; €60-200 for fillings", "notes": "Dutch dental care is high quality. Dental care is not covered by basic Dutch health insurance.", "emergencyTip": "Call 0900-821-2230 for emergency dental services in Amsterdam."},
        "mentalHealth": {"crisisLine": "113 Zelfmoordpreventie: 0900-0113 (24/7)", "internationalLine": "113 Online: online chat available", "englishTherapists": "Widely available. English is commonly spoken in the Netherlands.", "notes": "Netherlands has excellent mental health services. English-speaking therapists readily available in Amsterdam."},
        "accessibilityInfo": {"overview": "Netherlands is flat and generally accessible. Cobblestones in some areas can be challenging.", "hospitalAccess": "All hospitals are wheelchair accessible.", "transport": "Amsterdam's tram system is accessible. NS trains have wheelchair spaces and assistance. Most buses are low-floor.", "tips": "Canal houses typically have very steep stairs — book ground-floor rooms. The Rijksmuseum and Anne Frank House are wheelchair accessible. Cycling infrastructure can create conflicts for wheelchair users on sidewalks."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at GGD locations and pharmacies.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "Netherlands uses a GP-first system. Visit a huisarts (GP) before hospital. EU citizens with EHIC access emergency care. Keep all receipts and declaratie forms.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "NO": {
        "hospitals": [
            {"name": "Oslo University Hospital (Ullevål)", "nearTouristArea": "Ullevål, Oslo", "phone": "+47-22-11-73-00", "englishSpeaking": True, "notes": "Norway's largest hospital. English universally spoken."},
            {"name": "Haukeland University Hospital", "nearTouristArea": "Bergen city center", "phone": "+47-55-97-50-00", "englishSpeaking": True, "notes": "Serving Bergen and fjord region."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Jeg trenger medisin mot hodepine", "transliteration": ""},
            {"english": "I need a doctor", "local": "Jeg trenger en lege", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Excellent dental care but very expensive.", "costRange": "NOK 500-1,500 ($45-140) for consultation; NOK 1,000-3,000 ($95-280) for fillings", "notes": "Norwegian dental care is among the most expensive in the world. Quality is excellent.", "emergencyTip": "Call 116 117 for after-hours medical and dental assistance."},
        "mentalHealth": {"crisisLine": "Mental Helse: 116 123 (24/7)", "englishTherapists": "Available. English is widely spoken in Norway.", "notes": "Norway has excellent mental health services. English widely spoken by all healthcare providers."},
        "accessibilityInfo": {"overview": "Norway has excellent accessibility. Strong legal protections and well-maintained infrastructure.", "hospitalAccess": "All hospitals are wheelchair accessible.", "transport": "Oslo's T-bane and trams are accessible. NSB trains have wheelchair spaces. Hurtigruten ferries have accessible cabins.", "tips": "Fjord cruises are generally accessible. Hiking trails vary — check ut.no for accessibility ratings. Winter conditions can create additional barriers."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics.", "notes": "All restrictions removed. Cold weather and outdoor activity injuries are more relevant concerns."},
        "insuranceClaimProcess": "Norwegian healthcare is expensive for non-EEA visitors. ER visits: NOK 300-500 copay for EEA citizens. Keep all receipts. English documentation readily available.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "NP": {
        "hospitals": [
            {"name": "CIWEC Hospital Travel Medicine Center", "nearTouristArea": "Lazimpat, Kathmandu (near Thamel)", "phone": "+977-1-442-4111", "englishSpeaking": True, "notes": "Premier clinic for travelers. Highly recommended. Walk-in service."},
            {"name": "Grande International Hospital", "nearTouristArea": "Tokha, Kathmandu", "phone": "+977-1-515-9266", "englishSpeaking": True, "notes": "Modern private hospital. International standard."},
            {"name": "Himalaya Rescue Association", "nearTouristArea": "Thamel, Kathmandu / Pheriche (Everest region)", "phone": "+977-1-444-0292", "englishSpeaking": True, "notes": "Specializes in altitude sickness. Clinics at high altitude on trekking routes."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "मलाई टाउकोको दुखाइको औषधि चाहिन्छ", "transliteration": "Malai tauko-ko dukhai-ko ausadhi chahinchha"},
            {"english": "I need a doctor", "local": "मलाई डाक्टर चाहिन्छ", "transliteration": "Malai doctor chahinchha"},
        ],
        "dentalCare": {"availability": "Basic dental care in Kathmandu. Very limited elsewhere.", "costRange": "$10-25 for consultation; $15-50 for fillings", "notes": "Dental clinics in Kathmandu can handle basic procedures. For complex dental work, consider India.", "emergencyTip": "CIWEC clinic can provide dental referrals. Bring dental supplies for trekking."},
        "mentalHealth": {"crisisLine": "CMC: 1166 (Crisis Management Centre)", "englishTherapists": "Very limited. CIWEC clinic can provide referrals.", "notes": "Mental health services very limited. For serious concerns, medical evacuation to India may be necessary."},
        "accessibilityInfo": {"overview": "Nepal is extremely challenging for wheelchair users. Mountainous terrain, uneven roads, and minimal accessibility infrastructure.", "hospitalAccess": "CIWEC and Grande hospitals have some wheelchair access.", "transport": "No accessible public transport. Roads are rough and congested. Private vehicles are the best option.", "tips": "Trekking is not feasible for wheelchair users without extensive support. Pokhara lakeside and Kathmandu's Thamel are manageable with assistance. Altitude sickness affects everyone above 2,500m."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals in Kathmandu.", "notes": "Altitude sickness, food/water safety, and evacuation access are more significant health concerns. Medical evacuation insurance is essential for trekkers."},
        "insuranceClaimProcess": "CIWEC clinic accepts credit cards and provides English documentation for insurance. Helicopter evacuation (common for trekking injuries/altitude sickness) costs $5,000-10,000+ — ensure your insurance covers this. Keep all receipts.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "PE": {
        "hospitals": [
            {"name": "Clínica Anglo Americana", "nearTouristArea": "San Isidro, Lima", "phone": "+51-1-616-8900", "englishSpeaking": True, "notes": "English-speaking private hospital. International patient services."},
            {"name": "Clínica San Pablo", "nearTouristArea": "Cusco", "phone": "+51-84-270-7000", "englishSpeaking": True, "notes": "Private hospital in Cusco, the gateway to Machu Picchu."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Necesito medicina para el dolor de cabeza", "transliteration": ""},
            {"english": "I need medicine for altitude sickness", "local": "Necesito medicina para el mal de altura", "transliteration": "Altitude sickness (soroche) is common in Cusco and high-altitude areas"},
            {"english": "I need a doctor", "local": "Necesito un médico", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Dental care available and affordable. Lima has quality clinics.", "costRange": "$15-40 for consultation; $25-80 for fillings", "notes": "Lima has good dental clinics. Cusco has basic dental services. Quality varies outside major cities.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Pharmacies can provide pain relief."},
        "mentalHealth": {"crisisLine": "Línea 113: 113 (mental health support)", "englishTherapists": "Available in Lima. Limited in Cusco and tourist areas.", "notes": "Mental health services mainly in Spanish. English-speaking therapists in Lima's international clinics."},
        "accessibilityInfo": {"overview": "Peru's accessibility is very limited. Lima has some accessible infrastructure. Cusco and Machu Picchu are very challenging.", "hospitalAccess": "Private hospitals in Lima are accessible.", "transport": "Lima Metro Line 1 has some accessibility. Taxis are the main option.", "tips": "Machu Picchu has limited wheelchair access — the train to Aguas Calientes is accessible but the site itself requires significant climbing. Cusco's altitude (3,400m) and cobblestone streets add challenges. Acclimatize to altitude before exertion."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "Masks may still be required in healthcare settings.", "testing": "Available at clinics.", "notes": "Altitude sickness is the most significant health concern for tourists visiting Cusco and Machu Picchu. Diamox (acetazolamide) is available at pharmacies."},
        "insuranceClaimProcess": "Private hospitals may require upfront payment. Keep all receipts (boletas) and medical reports. Clínica Anglo Americana provides English documentation. Public hospitals are free but quality varies.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "PH": {
        "hospitals": [
            {"name": "Makati Medical Center", "nearTouristArea": "Makati, Manila", "phone": "+63-2-8888-8999", "englishSpeaking": True, "notes": "Top private hospital. English is an official language."},
            {"name": "St. Luke's Medical Center", "nearTouristArea": "BGC, Taguig, Manila", "phone": "+63-2-8789-7700", "englishSpeaking": True, "notes": "Premium hospital. JCI-accredited."},
            {"name": "Cebu Doctors' University Hospital", "nearTouristArea": "Cebu City (near beaches/resorts)", "phone": "+63-32-253-7511", "englishSpeaking": True, "notes": "Main hospital serving the Visayas region."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Kailangan ko ng gamot sa sakit ng ulo", "transliteration": "English is widely spoken — you can speak English at pharmacies"},
        ],
        "dentalCare": {"availability": "Dental care widely available and very affordable. English spoken everywhere.", "costRange": "PHP 500-1,500 ($9-27) for consultation; PHP 1,000-3,000 ($18-55) for fillings", "notes": "Excellent and affordable dental care. Many Filipino dentists have international training. Manila has modern dental clinics.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Walk-in dental clinics common in malls."},
        "mentalHealth": {"crisisLine": "Hopeline: 804-HOPE (4673) / 0917-558-HOPE", "internationalLine": "NCMH Crisis Hotline: 0917-899-8727", "englishTherapists": "Widely available. English is an official language.", "notes": "Mental health services growing. Private therapy: PHP 1,500-4,000 per session. Online therapy accessible."},
        "accessibilityInfo": {"overview": "Accessibility varies widely. Modern malls and hotels are accessible. Streets, jeepneys, and older buildings are not.", "hospitalAccess": "Private hospitals are wheelchair accessible.", "transport": "MRT/LRT in Manila have some accessibility. Grab widely available. Jeepneys and tricycles are not wheelchair friendly.", "tips": "Boracay's beaches have limited wheelchair access. Island hopping boats are generally not accessible. Modern resorts in Cebu and Bohol are more accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals and clinics.", "notes": "Typhoon and dengue risks are more relevant. Philippines has frequent natural disasters — check weather before travel."},
        "insuranceClaimProcess": "Private hospitals may require upfront payment. English documentation standard. Keep all official receipts and medical certificates.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "PL": {
        "hospitals": [
            {"name": "Medicover Hospital", "nearTouristArea": "Central Warsaw", "phone": "+48-500-900-500", "englishSpeaking": True, "notes": "International private hospital chain. English widely spoken."},
            {"name": "University Hospital Kraków", "nearTouristArea": "Kraków Old Town", "phone": "+48-12-424-73-00", "englishSpeaking": True, "notes": "Major university hospital near tourist center."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Potrzebuję lek na ból głowy", "transliteration": "Pot-sheh-boo-yeh lek na bul gwovy"},
            {"english": "I need a doctor", "local": "Potrzebuję lekarza", "transliteration": "Pot-sheh-boo-yeh le-ka-zha"},
        ],
        "dentalCare": {"availability": "Good dental care at affordable prices. Poland is a dental tourism destination.", "costRange": "PLN 100-250 ($25-60) for consultation; PLN 150-400 ($35-95) for fillings", "notes": "Poland offers quality dental care at 50-70% less than Western Europe. Kraków and Warsaw have clinics catering to tourists.", "emergencyTip": "Hospital emergency departments handle dental emergencies."},
        "mentalHealth": {"crisisLine": "116 123 (Telefon Zaufania — crisis line)", "englishTherapists": "Available in Warsaw and Kraków.", "notes": "English mental health services in major cities. Private therapy: PLN 150-350 per session."},
        "accessibilityInfo": {"overview": "Poland has been improving accessibility. Modern areas are accessible. Historic old towns can be challenging.", "hospitalAccess": "Major hospitals are wheelchair accessible.", "transport": "Warsaw and Kraków have accessible trams and buses. PKP trains offer assistance.", "tips": "Kraków's Old Town is largely flat and manageable. Auschwitz-Birkenau memorial has wheelchair access. Wieliczka Salt Mine has limited accessibility."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies and clinics.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU citizens with EHIC access public emergency care. Private clinics accept international insurance. Keep all rachunki (receipts) and documentation.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "PT": {
        "hospitals": [
            {"name": "Hospital de Santa Maria", "nearTouristArea": "Lisbon (near Baixa/Alfama)", "phone": "+351-217-805-000", "englishSpeaking": True, "notes": "Lisbon's largest public hospital."},
            {"name": "Hospital da Luz", "nearTouristArea": "Lisbon", "phone": "+351-217-104-400", "englishSpeaking": True, "notes": "Modern private hospital. English spoken."},
            {"name": "Hospital São João", "nearTouristArea": "Porto city center", "phone": "+351-225-512-100", "englishSpeaking": True, "notes": "Major hospital serving Porto and northern Portugal."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Preciso de medicamento para dor de cabeça", "transliteration": ""},
            {"english": "I need a doctor", "local": "Preciso de um médico", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Good dental care at reasonable prices.", "costRange": "€30-60 for consultation; €50-150 for fillings", "notes": "Portuguese dental care is affordable by Western European standards. English spoken at many practices in Lisbon and Porto.", "emergencyTip": "Call 808 24 24 24 (SNS 24) for health advice including dental emergencies."},
        "mentalHealth": {"crisisLine": "SOS Voz Amiga: 213 544 545 (daily 16h-24h)", "internationalLine": "SNS 24: 808 24 24 24", "englishTherapists": "Available in Lisbon and Porto. English increasingly common.", "notes": "Portugal's mental health services are improving. Private therapy: €40-80 per session."},
        "accessibilityInfo": {"overview": "Portugal's hilly terrain (especially Lisbon and Porto) makes wheelchair access challenging. Modern areas are accessible.", "hospitalAccess": "Major hospitals are accessible.", "transport": "Lisbon Metro is partially accessible. Porto Metro is more accessible. Trams are historic and not wheelchair friendly.", "tips": "Lisbon's Alfama and Bairro Alto neighborhoods have steep hills and cobblestones. Use the funiculars where possible. Modern Parque das Nações area is fully accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies.", "notes": "All restrictions removed. Sun exposure is a common health concern."},
        "insuranceClaimProcess": "EU citizens with EHIC access public healthcare. Keep receipts (faturas) and medical reports. English documentation available at private hospitals.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "SE": {
        "hospitals": [
            {"name": "Karolinska University Hospital", "nearTouristArea": "Solna, Stockholm", "phone": "+46-8-517-700-00", "englishSpeaking": True, "notes": "Sweden's premier hospital. Home of the Nobel Prize in Medicine. English universally spoken."},
            {"name": "Sahlgrenska University Hospital", "nearTouristArea": "Gothenburg", "phone": "+46-31-342-10-00", "englishSpeaking": True, "notes": "Major university hospital. English widely spoken."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Jag behöver medicin mot huvudvärk", "transliteration": ""},
            {"english": "I need a doctor", "local": "Jag behöver en läkare", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Excellent dental care but expensive.", "costRange": "SEK 500-1,500 ($45-140) for consultation; SEK 1,000-3,000 ($95-280) for fillings", "notes": "Swedish dental care is high quality but costly. Folktandvården (public dental service) available.", "emergencyTip": "Call 1177 (Vårdguiden) for healthcare and dental advice. After-hours dental clinics (Akuttandvård) in major cities."},
        "mentalHealth": {"crisisLine": "Mind Självmordslinjen: 90101 (24/7)", "internationalLine": "1177 Vårdguiden for healthcare advice", "englishTherapists": "Available. English is widely spoken in Sweden.", "notes": "Sweden has excellent mental health services. English widely spoken by all providers."},
        "accessibilityInfo": {"overview": "Sweden has excellent accessibility. Strong legal protections and well-maintained infrastructure.", "hospitalAccess": "All hospitals are fully accessible.", "transport": "Stockholm's tunnelbana (metro) is accessible. SJ trains have wheelchair spaces. All buses are low-floor.", "tips": "Stockholm's Gamla Stan (Old Town) has cobblestones but is largely flat. ICEHOTEL in Lapland has accessibility options."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "EU/EEA citizens with EHIC access subsidized care. Tourist ER visits: SEK 400-500 copay with EHIC. Keep receipts. English documentation readily available.",
        "eu112": True, "datePublished": "2026-03-15",
    },

    "TR": {
        "hospitals": [
            {"name": "American Hospital Istanbul", "nearTouristArea": "Nişantaşı, Istanbul (near Taksim/Sultanahmet)", "phone": "+90-212-444-3777", "englishSpeaking": True, "notes": "JCI-accredited. International patient department. English spoken."},
            {"name": "Acıbadem Hospital", "nearTouristArea": "Multiple locations — Istanbul, Ankara, Antalya", "phone": "+90-444-0-724", "englishSpeaking": True, "notes": "Turkey's largest private hospital chain. International patient services."},
            {"name": "Memorial Hospital Antalya", "nearTouristArea": "Antalya (near resort areas)", "phone": "+90-242-314-6666", "englishSpeaking": True, "notes": "Serves the Mediterranean resort coast. International department."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Baş ağrısı için ilaç lazım", "transliteration": "Bash ar-ruh-suh ichin ilach lazim"},
            {"english": "I need a doctor", "local": "Doktora ihtiyacım var", "transliteration": "Dok-tora ih-tee-ya-jum var"},
        ],
        "dentalCare": {"availability": "Turkey is a major dental tourism destination. Excellent quality at very competitive prices.", "costRange": "TRY 500-1,500 ($15-45) for consultation; dental implants from $300-600", "notes": "Istanbul and Antalya are dental tourism hubs. Prices are 60-80% lower than Europe/US. Many clinics offer package deals including hotel. Quality varies — choose JCI-accredited facilities.", "emergencyTip": "Hospital emergency departments handle dental emergencies. Private dental clinics often open on weekends."},
        "mentalHealth": {"crisisLine": "182 (ALO 182 — social support line)", "englishTherapists": "Available in Istanbul through international practices and American Hospital.", "notes": "Mental health services in English mainly in Istanbul. Private therapy: TRY 1,000-3,000 per session."},
        "accessibilityInfo": {"overview": "Turkey's accessibility is improving. Modern areas in Istanbul and resort areas are accessible. Historic sites and rural areas have significant barriers.", "hospitalAccess": "Private hospitals are wheelchair accessible.", "transport": "Istanbul Metro is accessible. Modern trams are low-floor. Accessible taxis available by request.", "tips": "Hagia Sophia and Blue Mosque have wheelchair access. Grand Bazaar is very challenging. Cappadocia's landscape is not wheelchair friendly. Resort hotels in Antalya are generally accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at clinics and hospitals.", "notes": "All restrictions removed."},
        "insuranceClaimProcess": "Turkish hospitals experienced with international insurance. American Hospital and Acıbadem offer direct billing. Keep all fatura (invoices) and medical reports. English documentation available at international hospitals.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "TZ": {
        "hospitals": [
            {"name": "Aga Khan Hospital Dar es Salaam", "nearTouristArea": "Dar es Salaam city center", "phone": "+255-22-211-5151", "englishSpeaking": True, "notes": "Best hospital in Tanzania. English is an official language."},
            {"name": "CCBRT Hospital", "nearTouristArea": "Dar es Salaam", "phone": "+255-22-260-1231", "englishSpeaking": True, "notes": "Disability and rehabilitation hospital."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "Ninahitaji dawa ya maumivu ya kichwa", "transliteration": "Swahili (English also widely used)"},
            {"english": "I need a doctor", "local": "Ninahitaji daktari", "transliteration": ""},
        ],
        "dentalCare": {"availability": "Basic dental care in Dar es Salaam. Very limited elsewhere.", "costRange": "$20-50 for consultation", "notes": "Limited dental care. For complex procedures, consider Nairobi.", "emergencyTip": "Aga Khan Hospital has dental services. Bring dental supplies for safari."},
        "mentalHealth": {"crisisLine": "Contact your embassy", "englishTherapists": "Very limited. English is official but mental health services are minimal.", "notes": "Mental health infrastructure is very limited. For serious concerns, consider medical evacuation to Nairobi."},
        "accessibilityInfo": {"overview": "Tanzania has very limited accessibility. Safari lodges and National Parks are generally inaccessible for wheelchair users.", "hospitalAccess": "Aga Khan Hospital is reasonably accessible.", "transport": "No accessible public transport. Private vehicles are the only option.", "tips": "Safari vehicles are not wheelchair adapted. Some luxury lodges may offer ground-level rooms. Zanzibar's Stone Town is very challenging. Pre-plan carefully."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at hospitals.", "notes": "Malaria prevention is the most important health consideration for Tanzania. Take antimalarials."},
        "insuranceClaimProcess": "Medical evacuation insurance is essential for Tanzania. Flying Doctors (AMREF) covers safari evacuations. Private hospitals require upfront payment. Keep all receipts.",
        "eu112": False, "datePublished": "2026-03-15",
    },

    "ZA": {
        "hospitals": [
            {"name": "Netcare Milpark Hospital", "nearTouristArea": "Johannesburg (near Sandton)", "phone": "+27-11-480-5600", "englishSpeaking": True, "notes": "Major private hospital. Trauma unit."},
            {"name": "Groote Schuur Hospital", "nearTouristArea": "Cape Town / Table Mountain area", "phone": "+27-21-404-9111", "englishSpeaking": True, "notes": "Famous public hospital. Site of first heart transplant."},
            {"name": "Mediclinic Stellenbosch", "nearTouristArea": "Stellenbosch / Cape Winelands", "phone": "+27-21-861-2000", "englishSpeaking": True, "notes": "Serves the popular wine region."},
        ],
        "pharmacyPhrases": [
            {"english": "I need medicine for a headache", "local": "I need medicine for a headache", "transliteration": "English is widely spoken throughout South Africa"},
        ],
        "dentalCare": {"availability": "Good dental care available, especially in major cities.", "costRange": "ZAR 500-1,200 ($28-67) for consultation; ZAR 800-2,500 ($45-140) for fillings", "notes": "Private dental care is high quality in Cape Town and Johannesburg. Affordable by international standards.", "emergencyTip": "Private hospital emergency departments handle dental emergencies. Dischem and Clicks pharmacies can provide pain relief."},
        "mentalHealth": {"crisisLine": "SADAG: 0800 567 567 (24/7, free)", "internationalLine": "SADAG SMS line: 31393", "englishTherapists": "Widely available. English is commonly spoken.", "notes": "South Africa has good mental health services in urban areas. SADAG provides comprehensive support. Private therapy: ZAR 600-1,500 per session."},
        "accessibilityInfo": {"overview": "South Africa has legal accessibility requirements but enforcement varies. Major cities have improving infrastructure.", "hospitalAccess": "Private hospitals are wheelchair accessible.", "transport": "Gautrain in Johannesburg is accessible. MyCiti buses in Cape Town are accessible. Taxis and Uber widely available.", "tips": "Table Mountain cable car is wheelchair accessible. Kruger National Park has some accessible safari vehicles and lodges. V&A Waterfront in Cape Town is fully accessible."},
        "covidStatus": {"entryRequirements": "No COVID requirements.", "maskPolicy": "No mandates.", "testing": "Available at pharmacies and clinics.", "notes": "Malaria prophylaxis recommended for Kruger Park area. Sun exposure is a significant concern."},
        "insuranceClaimProcess": "Private hospitals require payment or insurance guarantee. Netcare and Mediclinic have insurance departments. Public hospitals treat emergencies at lower cost. Keep all receipts and medical reports.",
        "eu112": False, "datePublished": "2026-03-15",
    },
}

# ── Data fixes ──────────────────────────────────────────────────────────

WATER_SAFETY_FIXES = {
    "KH": "bottled-only",  # was "unsafe" — normalize to known badge value
}

INSURANCE_FIXES = {
    "BR": {"required": False, "requiredNote": ""},  # was incorrectly required:true
}


def enrich_country(iso2: str, data: dict) -> dict:
    """Add enrichment data to a country's health JSON."""

    # Apply water safety fixes
    if iso2 in WATER_SAFETY_FIXES:
        data["waterSafety"] = WATER_SAFETY_FIXES[iso2]

    # Apply insurance fixes
    if iso2 in INSURANCE_FIXES:
        ins = data.get("travelInsurance", {})
        if isinstance(ins, dict):
            ins.update(INSURANCE_FIXES[iso2])
            data["travelInsurance"] = ins

    # Add datePublished if not present
    if "datePublished" not in data:
        data["datePublished"] = "2026-03-15"

    # Apply enrichment if we have it
    if iso2 in ENRICHMENT:
        enr = ENRICHMENT[iso2]
        for key, value in enr.items():
            # Only add if not already present or if we're explicitly overriding
            if key not in data or key in ("eu112", "datePublished", "hospitals", "pharmacyPhrases", "dentalCare", "mentalHealth", "accessibilityInfo", "covidStatus", "insuranceClaimProcess"):
                data[key] = value
    else:
        # Minimal enrichment for countries without detailed data
        if "hospitals" not in data:
            data["hospitals"] = []
        if "pharmacyPhrases" not in data:
            data["pharmacyPhrases"] = []
        if "dentalCare" not in data:
            data["dentalCare"] = {}
        if "mentalHealth" not in data:
            data["mentalHealth"] = {}
        if "accessibilityInfo" not in data:
            data["accessibilityInfo"] = {}
        if "covidStatus" not in data:
            data["covidStatus"] = {
                "entryRequirements": "No COVID testing or vaccination requirements for entry.",
                "maskPolicy": "No mask mandates. Masks may be requested in healthcare settings.",
                "testing": "COVID tests available at hospitals and clinics.",
                "notes": "Most countries have removed COVID entry restrictions. Check current requirements before travel."
            }
        if "eu112" not in data:
            # EU/EEA countries get eu112=True
            eu_countries = {"AT", "BE", "CZ", "DE", "ES", "FR", "GR", "HR", "HU", "IE", "IS", "IT", "NL", "NO", "PL", "PT", "SE", "CH"}
            data["eu112"] = iso2 in eu_countries

    return data


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        # Enrich single country
        iso2 = sys.argv[1].upper()
        path = DATA_DIR / f"{iso2}.json"
        if not path.exists():
            sys.exit(f"No data file for {iso2}")
        data = json.loads(path.read_text(encoding="utf-8"))
        data = enrich_country(iso2, data)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ✅ Enriched {iso2}")
        return

    # Enrich all
    files = sorted(DATA_DIR.glob("*.json"))
    files = [f for f in files if not f.stem.startswith("_")]
    count = 0
    for path in files:
        iso2 = path.stem.upper()
        data = json.loads(path.read_text(encoding="utf-8"))
        data = enrich_country(iso2, data)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ✅ Enriched {iso2}")
        count += 1
    print(f"\nDone — {count} countries enriched.")


if __name__ == "__main__":
    main()
