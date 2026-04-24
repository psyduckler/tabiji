"""
Tier-1 medication catalog + rich editorial content for the medications rebuild.

Each entry in TIER1 drives a dedicated page at /health/medications/{slug}/.
Matching patterns are case-insensitive substrings — a country's restrictedMeds
name contains ANY pattern → the country is counted under that tier-1 med.

Used by scripts/build-medications.py (hub + tier-1 pages).
"""

from __future__ import annotations


# -------------------------------------------------------------------
# Tier-1 medications — hand-curated, SEO-weighted, highest traveler query
# volume. Each entry becomes /health/medications/{slug}/.
# -------------------------------------------------------------------

TIER1 = [
    {
        "slug": "adderall",
        "canonical_name": "Adderall & ADHD stimulants",
        "page_title": "Adderall & ADHD Stimulants Abroad — Which Countries Ban Them?",
        "meta_description": (
            "Can you bring Adderall, Vyvanse, Ritalin, or other ADHD stimulants abroad? "
            "Country-by-country legal status, import permits, and what to do if your medication is banned at your destination."
        ),
        "icon": "💊",
        "also_known_as": [
            "Adderall", "Vyvanse", "Dexedrine", "Ritalin", "Concerta",
            "methylphenidate", "amphetamine", "dextroamphetamine", "lisdexamfetamine",
        ],
        "match_patterns": ["adderall", "adhd", "amphetamine", "ritalin", "methylphenidate", "stimulant"],
        "summary": (
            "ADHD stimulant medications — Adderall, Vyvanse, Dexedrine, Ritalin, Concerta — "
            "are among the most travel-restricted prescription drugs in the world. Multiple countries "
            "ban them outright, even with a valid US prescription. The penalty for an honest mistake "
            "at customs can be confiscation, detention, or deportation. This is the single most "
            "important medication to research before you fly."
        ),
        "what_travelers_ask": "Can I bring my Adderall to Japan?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "Japan prohibits Adderall and most amphetamine ADHD meds",
                "body": "No import certificate available. Even a valid US prescription does not grant legal entry. Travelers have been detained at Narita and Haneda.",
            },
            {
                "tone": "danger",
                "title": "UAE, Saudi Arabia, and several Gulf states are strict",
                "body": "Amphetamines are treated as controlled narcotics. Pre-approved import permits are required (and often not granted for short trips). Penalties include imprisonment.",
            },
            {
                "tone": "caution",
                "title": "Thailand, South Korea, Singapore, Mexico need permits",
                "body": "Bringing Adderall requires advance pharmaceutical-import permits and documentation. Timelines range from 2–4 weeks.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Check your destination 90 days before you travel",
                "body": "ADHD stimulant rules are destination-specific and change. Check the country's embassy or health ministry site, then cross-reference against our per-country guides.",
            },
            {
                "title": "Request a methylphenidate alternative where possible",
                "body": "Methylphenidate (Ritalin, Concerta) is legal in more countries than amphetamines (Adderall, Vyvanse). If you're going somewhere that bans amphetamines, ask your prescriber about switching to methylphenidate for the trip — where it's legal, the import process is typically easier.",
            },
            {
                "title": "Bring original packaging + doctor's letter + prescription",
                "body": "For every restricted-status country: original pharmacy label, a signed letter from your prescriber on letterhead listing the medication, dosage, and indication, and your prescription itself. Translate the letter where language is a barrier.",
            },
            {
                "title": "Get the import permit where required",
                "body": "Japan's Yakkan Shoumei (when issued) takes 2-4 weeks. Thailand's import approval runs similar. Start early — no permit = no legal entry of the medication, regardless of prescription.",
            },
            {
                "title": "Have a non-stimulant backup plan",
                "body": "Strattera (atomoxetine), Intuniv (guanfacine), and Wellbutrin (bupropion) are legal in most countries that restrict stimulants. Talk to your prescriber about a short-term switch if your destination bans Adderall.",
            },
        ],
        "faqs": [
            {
                "q": "Is Adderall legal in Japan?",
                "a": "No. Adderall and amphetamine-based ADHD medications are prohibited in Japan — no import certificate can make them legal. This includes Vyvanse and Dexedrine. Methylphenidate (Ritalin, Concerta) is legal with an import permit (Yakkan Shoumei).",
            },
            {
                "q": "What's the difference between Adderall and Ritalin for travel?",
                "a": "Adderall is an amphetamine; Ritalin (methylphenidate) is a separate drug class. Many countries that ban amphetamines allow methylphenidate with a permit. If you're going to Japan or parts of Asia, switching to methylphenidate for the trip is worth asking your prescriber about.",
            },
            {
                "q": "Can I just not declare it at customs?",
                "a": "No. Countries with strict enforcement scan baggage and inspect declared medications. Penalties for undeclared controlled substances range from confiscation and deportation to criminal charges. Always declare, always carry documentation.",
            },
            {
                "q": "What if I run out and can't get a prescription abroad?",
                "a": "Most countries that restrict ADHD stimulants also restrict or don't stock them at pharmacies. Bring more than you need, store it in original packaging, and consider a non-stimulant backup prescription for the trip. The US embassy can sometimes help in a true emergency.",
            },
        ],
    },
    {
        "slug": "sudafed",
        "canonical_name": "Sudafed & pseudoephedrine",
        "page_title": "Sudafed & Pseudoephedrine Abroad — Which Countries Ban It?",
        "meta_description": (
            "Can you bring Sudafed or pseudoephedrine abroad? Japan bans it outright. "
            "Country-by-country legal status, travel alternatives, and what to do if your cold medicine is banned at your destination."
        ),
        "icon": "💊",
        "also_known_as": [
            "Sudafed", "pseudoephedrine", "Contac", "Claritin-D", "Zyrtec-D", "Allegra-D",
        ],
        "match_patterns": ["sudafed", "pseudoephedrine"],
        "summary": (
            "Pseudoephedrine — the decongestant behind Sudafed, Contac, Claritin-D, and many "
            "\"-D\" combo allergy medications — is classified as a controlled stimulant in several "
            "countries and outright banned in Japan. The rules catch millions of travelers by "
            "surprise because these are common over-the-counter meds in the US."
        ),
        "what_travelers_ask": "Can I bring Sudafed to Japan?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "Japan bans pseudoephedrine entirely",
                "body": "No import certificate available. Sudafed, Contac, Claritin-D, and any other pseudoephedrine-containing medication is prohibited. Use phenylephrine-based alternatives or skip.",
            },
            {
                "tone": "caution",
                "title": "Mexico, South Korea, and Middle East restrict it",
                "body": "Treated as a controlled substance in several jurisdictions; bringing commercial quantities can trigger scrutiny. For personal use, declare and carry original packaging.",
            },
            {
                "tone": "info",
                "title": "Most of Europe: OTC but sometimes behind the counter",
                "body": "Widely available across most of Europe, though some countries (UK, Sweden) have moved it behind the pharmacist counter. Not a travel issue, just a purchasing note.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Switch to phenylephrine for the trip",
                "body": "Phenylephrine (found in Sudafed PE and many other \"PE\" or \"non-drowsy\" formulas) is legal almost everywhere. Less effective than pseudoephedrine but a fine 1-2 week substitute.",
            },
            {
                "title": "Carry a nasal steroid if you rely on decongestants",
                "body": "Fluticasone (Flonase) and mometasone (Nasonex) are widely legal and often more effective for chronic sinus congestion. Worth discussing with your doctor before a trip.",
            },
            {
                "title": "Saline irrigation + antihistamines for short trips",
                "body": "For acute congestion from flying or dry climates, a saline spray plus a non-drowsy antihistamine (cetirizine, loratadine — both universally legal) handles most cases without pseudoephedrine.",
            },
            {
                "title": "If you absolutely must bring it — check your destination first",
                "body": "For every country on your itinerary: verify pseudoephedrine is legal for personal-use travel. For borderline countries, declare at customs, bring a doctor's letter, and keep it in original US packaging.",
            },
        ],
        "faqs": [
            {
                "q": "Is Sudafed illegal in Japan?",
                "a": "Yes. Pseudoephedrine is on Japan's prohibited substance list — no import certificate makes it legal. This applies to all dosage forms and combination products (Sudafed, Contac, Claritin-D, Allegra-D, etc.).",
            },
            {
                "q": "Is Sudafed PE (phenylephrine) OK to travel with?",
                "a": "Yes, in almost all cases. Phenylephrine is a different drug class and isn't controlled in countries that ban pseudoephedrine. Japan, Mexico, South Korea, and the Middle East generally allow phenylephrine-based decongestants.",
            },
            {
                "q": "What can I buy in Japan instead?",
                "a": "Japanese pharmacies (ドラッグストア — drugstore) stock cold and allergy medications based on phenylephrine, antihistamines, and herbal formulas. Look for kampo (traditional Japanese medicine) products like kakkonto for early cold symptoms.",
            },
            {
                "q": "Does this apply to allergy meds with \"-D\" in the name?",
                "a": "Yes. Claritin-D, Zyrtec-D, Allegra-D, and similar combo products all contain pseudoephedrine as the decongestant component. Switch to the non-D version of the same antihistamine for the trip.",
            },
        ],
    },
    {
        "slug": "codeine",
        "canonical_name": "Codeine",
        "page_title": "Codeine Abroad — Which Countries Restrict or Ban It?",
        "meta_description": (
            "Can you bring codeine abroad? UAE, Japan, and parts of Asia/Middle East strictly control it. "
            "Country-by-country legal status, import-permit requirements, and safer travel alternatives."
        ),
        "icon": "💊",
        "also_known_as": [
            "Tylenol 3", "codeine phosphate", "promethazine with codeine",
            "dihydrocodeine", "co-codamol", "acetaminophen with codeine",
        ],
        "match_patterns": ["codeine"],
        "summary": (
            "Codeine is one of the most widely restricted prescription medications internationally. "
            "Found in countless cough syrups, prescription pain combinations (Tylenol 3), and some OTC "
            "products, it's treated as a controlled narcotic in most of the Middle East and parts of "
            "Asia. Even small personal quantities can be confiscated or trigger legal consequences."
        ),
        "what_travelers_ask": "Can I bring Tylenol with codeine to the UAE?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "UAE, Saudi Arabia, Qatar, Kuwait: strict controlled narcotic",
                "body": "Codeine is a Schedule II controlled substance across most Gulf states. Bringing any without pre-approval from the Ministry of Health is illegal and can result in arrest. This includes combination products like Tylenol 3.",
            },
            {
                "tone": "caution",
                "title": "Japan, Singapore, China: permit required",
                "body": "Small personal quantities may be allowed with a Yakkan Shoumei (Japan) or equivalent import certificate, secured 2-4 weeks before travel. Without the permit, confiscation at customs.",
            },
            {
                "tone": "info",
                "title": "Most of Europe, Australia: prescription required",
                "body": "Codeine was removed from OTC availability in most of Europe and Australia. Travel with a prescription and doctor's letter; generally not a customs issue for personal use.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Switch to non-codeine pain relief for the trip",
                "body": "Acetaminophen (Tylenol regular), ibuprofen (Advil), and naproxen (Aleve) are legal worldwide. For chronic pain, ask your prescriber about a non-opioid alternative for travel.",
            },
            {
                "title": "Non-codeine cough medicine",
                "body": "Dextromethorphan (Robitussin DM) and guaifenesin (Mucinex) are legal almost everywhere. Carry these instead of codeine-containing cough syrup.",
            },
            {
                "title": "If you must carry codeine — get the permit in advance",
                "body": "For Japan: Yakkan Shoumei for quantities over a 1-month supply (though codeine-specific rules vary). For UAE: Ministry of Health pre-approval form. For Saudi Arabia: advance authorization required. All take 2-6 weeks.",
            },
            {
                "title": "Carry full documentation",
                "body": "Original pharmacy label, doctor's letter (translated if possible), prescription itself, and a copy of any import authorization. Declare at customs — don't risk an undisclosed controlled substance.",
            },
        ],
        "faqs": [
            {
                "q": "Can I bring Tylenol 3 to Dubai?",
                "a": "Only with pre-approval from the UAE Ministry of Health and Prevention, applied for 2-4 weeks before travel. Without it, Tylenol 3 is illegal to possess in the UAE. Codeine is classified as a controlled narcotic.",
            },
            {
                "q": "Is codeine in cough syrup treated the same as codeine pills?",
                "a": "Yes. Codeine-containing cough medicine (promethazine with codeine, Tylenol with codeine) falls under the same controlled-substance rules as codeine tablets in most restrictive jurisdictions.",
            },
            {
                "q": "What's co-codamol and is it different?",
                "a": "Co-codamol is a combination of codeine and paracetamol (acetaminophen), common in the UK and Europe. The codeine component is subject to the same international travel restrictions as standalone codeine.",
            },
            {
                "q": "Can I buy codeine abroad instead of bringing mine?",
                "a": "Varies. In France, Spain, Portugal, codeine is available by prescription. In the Middle East and strict Asia, OTC codeine is unavailable and prescription codeine requires a local doctor visit. Plan on bringing non-codeine alternatives.",
            },
        ],
    },
    {
        "slug": "cbd",
        "canonical_name": "CBD & cannabinoid products",
        "page_title": "Can You Travel with CBD? Country-by-Country Legality",
        "meta_description": (
            "Is CBD legal in Japan, UAE, Singapore, or China? CBD with any THC is banned in many countries. "
            "Country-by-country legal status, pure-CBD vs THC rules, and what customs actually checks."
        ),
        "icon": "🌿",
        "also_known_as": [
            "CBD", "cannabidiol", "hemp oil", "CBD tincture", "CBD gummies",
        ],
        "match_patterns": ["cbd", "cannabis", "cannabinoid", "cannabis/cbd"],
        "summary": (
            "CBD (cannabidiol) sits in a legal gray zone that varies wildly country to country. US-legal "
            "CBD products often contain trace THC (<0.3%) that makes them illegal in Japan, UAE, "
            "Singapore, Saudi Arabia, Russia, and many others. Customs in strict jurisdictions test for "
            "THC content — a \"CBD only\" label on your product is not a legal defense."
        ),
        "what_travelers_ask": "Can I bring CBD to Japan?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "Japan, UAE, Singapore, Saudi Arabia, Russia: any THC = illegal",
                "body": "Even trace THC (below US-legal limits) makes a CBD product illegal in these countries. Penalties range from confiscation to criminal charges. Leave it at home.",
            },
            {
                "tone": "danger",
                "title": "China, South Korea, Indonesia: all cannabis products prohibited",
                "body": "Zero-tolerance jurisdictions. Any cannabinoid product — regardless of labeling — is illegal to import. Customs uses THC testing and has prosecuted travelers.",
            },
            {
                "tone": "caution",
                "title": "UK, most of EU: pure CBD isolate OK; full-spectrum murky",
                "body": "Pure CBD isolate (0% THC) is generally legal across Western Europe. Full-spectrum CBD containing any detectable THC is a legal gray zone — verify your specific product's COA (Certificate of Analysis) before traveling.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Default to leaving CBD at home for international travel",
                "body": "The legal risk almost never justifies the benefit for a short trip. For chronic conditions where CBD is essential, consult a travel-medicine doctor before you go — the risk calculus is different for long stays.",
            },
            {
                "title": "If you travel with CBD — carry the COA",
                "body": "The Certificate of Analysis shows third-party lab testing results for THC content. A 0.0% THC CBD isolate COA is your strongest legal defense in countries where pure CBD is legal.",
            },
            {
                "title": "Research destination THC thresholds specifically",
                "body": "\"CBD is legal\" is not the same as \"your CBD product is legal.\" US-legal full-spectrum CBD (<0.3% THC) is illegal in the UK (<0.01% THC threshold) and several other countries with stricter thresholds.",
            },
            {
                "title": "Medical cannabis programs are resident-only in most countries",
                "body": "Thailand's medical cannabis program, Canada's recreational market, and most EU medical programs are for residents — not for tourists to access or bring home. Don't assume local legality means you can travel with the product.",
            },
        ],
        "faqs": [
            {
                "q": "Is CBD legal in Japan?",
                "a": "Only pure CBD isolate with 0.0% THC and no other controlled substances is legal in Japan. Most US-sold CBD products contain trace THC that makes them illegal. Customs has testing equipment and has confiscated CBD from travelers.",
            },
            {
                "q": "Can I travel with CBD gummies?",
                "a": "Depends on destination and product. In strict jurisdictions (UAE, Japan, Singapore), CBD gummies are banned regardless of THC content. In permissive jurisdictions (UK, Germany, Switzerland), pure CBD isolate gummies with 0.0% THC are typically legal.",
            },
            {
                "q": "What about hemp oil supplements from the health food store?",
                "a": "Hemp oil (from hemp seeds, no cannabinoids) is legal almost everywhere. Hemp-derived CBD products (with cannabinoids) fall under the same rules as other CBD. Read labels carefully.",
            },
            {
                "q": "Can I get in trouble for using CBD in the hotel room abroad?",
                "a": "In strict jurisdictions, yes — possession is the legal threshold, not use. Any detectable cannabinoid in the product makes it contraband. Don't pack it, don't order it, don't assume discretion protects you.",
            },
        ],
    },
    {
        "slug": "tramadol",
        "canonical_name": "Tramadol",
        "page_title": "Tramadol Abroad — Which Countries Restrict It?",
        "meta_description": (
            "Can you bring tramadol abroad? Controlled in UAE, Japan, Thailand, India, and much of Asia/Middle East. "
            "Country-by-country legal status, import requirements, and non-opioid alternatives."
        ),
        "icon": "💊",
        "also_known_as": [
            "Tramadol", "Ultram", "ConZip", "Ryzolt",
        ],
        "match_patterns": ["tramadol"],
        "summary": (
            "Tramadol is a prescription opioid pain medication that's been increasingly regulated "
            "worldwide as its addiction potential has been recognized. Many countries that allow "
            "codeine restrict tramadol more strictly, and some Gulf states treat it as a Schedule I "
            "narcotic. Don't assume your US prescription travels."
        ),
        "what_travelers_ask": "Can I bring tramadol to the UAE?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "UAE, Saudi Arabia, Egypt: strict controlled narcotic",
                "body": "Treated as a dangerous drug across most of the Middle East. Pre-approved import permits from the Ministry of Health are required and often not issued for short trips. Possession without approval can result in imprisonment.",
            },
            {
                "tone": "caution",
                "title": "Japan, Thailand, India: permit required",
                "body": "Small personal quantities may be allowed with advance import permits. Yakkan Shoumei for Japan; equivalents for Thailand and India. Without permit, confiscation.",
            },
            {
                "tone": "info",
                "title": "Most of Europe, Australia, Canada: prescription required",
                "body": "Tramadol is a prescription controlled substance but legal to travel with for personal use. Carry original packaging, doctor's letter, and prescription.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Non-opioid alternatives for most pain",
                "body": "For mild to moderate pain: acetaminophen + ibuprofen combined is often as effective as tramadol for short-term needs and legal worldwide. Ask your prescriber about a non-opioid travel plan.",
            },
            {
                "title": "Topical NSAIDs for musculoskeletal pain",
                "body": "Diclofenac gel (Voltaren, available OTC in the US as of 2020) and similar topical NSAIDs handle joint and muscle pain with no controlled-substance concerns.",
            },
            {
                "title": "If you must carry tramadol — get permits early",
                "body": "UAE: Ministry of Health and Prevention pre-approval (allow 4-6 weeks). Japan: Yakkan Shoumei. Saudi Arabia: advance authorization. Bring translated doctor's letter and original packaging regardless.",
            },
            {
                "title": "Declare at customs",
                "body": "Always declare tramadol on arrival in restrictive countries. Undeclared controlled substances triggers escalating penalties. Declared substances with documentation get scrutinized but rarely criminalized.",
            },
        ],
        "faqs": [
            {
                "q": "Is tramadol banned in Dubai?",
                "a": "Tramadol is a controlled narcotic in the UAE. Bringing any without a pre-approved permit from the Ministry of Health and Prevention is illegal. Tourists have been detained at Dubai airport for undeclared tramadol.",
            },
            {
                "q": "What's the difference between tramadol and codeine for travel?",
                "a": "Both are controlled opioids but regulated differently by country. Some places that allow codeine with a permit ban tramadol entirely, and vice versa. Check each destination individually — don't assume one covers the other.",
            },
            {
                "q": "Can I take my tramadol to Egypt if I have a prescription?",
                "a": "Egypt treats tramadol as a dangerous drug. A US prescription alone is not sufficient — you need advance approval from Egyptian authorities. Many travelers have been arrested for tramadol at Cairo airport.",
            },
        ],
    },
    {
        "slug": "xanax",
        "canonical_name": "Xanax & benzodiazepines",
        "page_title": "Xanax & Benzodiazepines Abroad — Which Countries Restrict Them?",
        "meta_description": (
            "Can you bring Xanax, Valium, Klonopin, or Ativan abroad? Restricted in UAE, Japan, Singapore, China, and more. "
            "Country-by-country legal status, import requirements, and flight-anxiety alternatives."
        ),
        "icon": "💊",
        "also_known_as": [
            "Xanax", "alprazolam", "Valium", "diazepam", "Klonopin", "clonazepam",
            "Ativan", "lorazepam", "Restoril", "temazepam",
        ],
        "match_patterns": ["benzodiazepine", "xanax", "alprazolam", "diazepam", "valium", "clonazepam", "lorazepam"],
        "summary": (
            "Benzodiazepines — Xanax, Valium, Klonopin, Ativan, and similar — are prescription anti-"
            "anxiety and sleep medications that carry significant international travel restrictions. "
            "Commonly used for flight anxiety or insomnia, they're controlled narcotics across most "
            "of the Middle East and tightly regulated in much of Asia."
        ),
        "what_travelers_ask": "Can I bring Xanax on a flight to Dubai?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "UAE, Saudi Arabia, Egypt, Qatar: pre-approval required",
                "body": "Benzodiazepines are controlled narcotics across most Gulf states. Ministry of Health pre-approval is required and must be arranged weeks in advance. Possession without approval can result in arrest.",
            },
            {
                "tone": "caution",
                "title": "Japan, Singapore, China: Yakkan Shoumei / permit required",
                "body": "Japan requires an import certificate for quantities over a 1-month supply. Singapore requires a 24-hour pre-approval form. China restricts psychotropic substances broadly.",
            },
            {
                "tone": "info",
                "title": "Most of Europe, Australia: prescription required",
                "body": "Legal to travel with for personal use. Carry original packaging, doctor's letter, and prescription. No special permit needed in most EU countries, UK, Canada, Australia.",
            },
        ],
        "travel_strategy": [
            {
                "title": "For flight anxiety: non-benzo alternatives exist",
                "body": "Beta-blockers (propranolol) and antihistamines (hydroxyzine) handle situational anxiety without controlled-substance issues. Ask your prescriber about a travel-specific non-benzo strategy.",
            },
            {
                "title": "For insomnia: melatonin + sleep hygiene",
                "body": "Melatonin (legal in most destinations — notable exception: UK requires prescription) plus a dark sleep mask and earplugs handles jet lag and travel insomnia for most people without the legal risk of a benzo.",
            },
            {
                "title": "If you must carry benzos — declare + document",
                "body": "Original pharmacy label, doctor's letter on letterhead (translate for Arabic/Chinese destinations), prescription itself, and any required pre-approval. Declare at customs.",
            },
            {
                "title": "Keep quantities reasonable",
                "body": "Carrying a 30-day supply for a 7-day trip attracts scrutiny. Bring only what you'll reasonably use, plus a few extra days for travel delays.",
            },
        ],
        "faqs": [
            {
                "q": "Can I bring Xanax to Dubai for my flight?",
                "a": "Only with pre-approval from the UAE Ministry of Health and Prevention, applied for 2-4 weeks before travel. Xanax (alprazolam) is a controlled narcotic in the UAE. Tourists have been arrested at Dubai airport for undeclared Xanax.",
            },
            {
                "q": "Is Valium easier to travel with than Xanax?",
                "a": "Both fall under the same benzodiazepine regulations in almost every country. Don't expect different treatment. Diazepam (Valium) has a longer half-life, which may be relevant for shorter trips, but the legal rules are the same.",
            },
            {
                "q": "What about just one Xanax for takeoff?",
                "a": "In strict jurisdictions, possession is the legal threshold, not quantity. A single loose pill in your pocket can trigger the same legal issue as a full bottle. Either carry the original labeled container with documentation, or don't carry it.",
            },
            {
                "q": "Is Ambien (zolpidem) treated the same as benzos?",
                "a": "Zolpidem is a non-benzo but falls under similar controlled-substance rules in most strict jurisdictions. Treat it with the same travel precautions as a benzodiazepine.",
            },
        ],
    },
    {
        "slug": "opioids",
        "canonical_name": "Opioids & narcotic pain medication",
        "page_title": "Opioids Abroad — Morphine, Oxycodone, Hydrocodone International Travel",
        "meta_description": (
            "Can you bring oxycodone, hydrocodone, morphine, or fentanyl abroad? Heavily restricted worldwide. "
            "Country-by-country legal status, import permits, and what documentation you need."
        ),
        "icon": "💊",
        "also_known_as": [
            "oxycodone", "OxyContin", "Percocet", "hydrocodone", "Vicodin", "Norco",
            "morphine", "MS Contin", "fentanyl", "Duragesic", "hydromorphone", "Dilaudid",
        ],
        "match_patterns": ["opioid", "narcotic", "oxycodone", "hydrocodone", "morphine", "fentanyl", "hydromorphone"],
        "summary": (
            "Strong opioid pain medications — oxycodone (OxyContin, Percocet), hydrocodone (Vicodin), "
            "morphine, fentanyl — are controlled narcotics in virtually every country and subject to "
            "the strictest international travel rules. Even a legitimate US prescription requires "
            "advance import permits in most destinations. The penalty for an undisclosed opioid at "
            "customs can be severe, including imprisonment."
        ),
        "what_travelers_ask": "Can I bring my oxycodone prescription to the Caribbean?",
        "headline_warnings": [
            {
                "tone": "danger",
                "title": "Every country treats opioids as controlled substances",
                "body": "Unlike stimulants or CBD, there is no jurisdiction where strong opioids travel freely. Every country requires declaration, prescription documentation, and often pre-approval for personal use.",
            },
            {
                "tone": "danger",
                "title": "UAE, Saudi Arabia, Japan, China, Singapore: advance permits mandatory",
                "body": "These countries require pre-travel authorization from their Ministry of Health or pharmaceutical authority. Without it, legal opioids become illegal contraband at the border.",
            },
            {
                "tone": "caution",
                "title": "Even EU/UK/Australia: document everything",
                "body": "Legal to travel with for personal use but requires original packaging, prescription, and doctor's letter. Quantities beyond reasonable personal use draw scrutiny.",
            },
        ],
        "travel_strategy": [
            {
                "title": "Consider non-opioid alternatives for trip duration",
                "body": "For chronic pain patients: discuss with your prescriber whether a non-opioid regimen (gabapentin, duloxetine, topical NSAIDs, physical therapy) can cover a 1-2 week trip. Not always possible, but worth asking.",
            },
            {
                "title": "Get pre-travel permits 6-8 weeks in advance",
                "body": "For UAE: Ministry of Health and Prevention pre-approval. Japan: Yakkan Shoumei. Singapore: Health Sciences Authority form. Saudi Arabia: advance authorization. All take multiple weeks — start the process as soon as you book travel.",
            },
            {
                "title": "Bring exact documentation",
                "body": "Original pharmacy label, signed doctor's letter on letterhead (list: medication, dosage, indication, duration of treatment), prescription itself, import-permit documentation, and a copy of everything in your checked bag in case carry-on is lost.",
            },
            {
                "title": "Declare on arrival, every time",
                "body": "On the customs declaration form, always declare controlled substances. Carry all documentation in hand; expect to be pulled aside for secondary screening. Declared + documented = legal inconvenience; undeclared + documented = legal crisis.",
            },
            {
                "title": "Have a contingency plan for loss or emergency",
                "body": "What if your medication is lost or stolen abroad? Most countries won't honor a US prescription for opioids. Talk to your prescriber before travel about an emergency protocol — some can arrange telemed consultations and a US embassy-assisted emergency supply.",
            },
        ],
        "faqs": [
            {
                "q": "Can I bring oxycodone to Mexico or the Caribbean?",
                "a": "Most Caribbean countries and Mexico allow personal-use opioids with a prescription and original packaging, though you should declare them at customs. The Cayman Islands, Bahamas, and Dominican Republic are typical destinations with established protocols. Verify per destination before traveling.",
            },
            {
                "q": "What's the safest way to travel with morphine?",
                "a": "Get advance authorization from the destination's health ministry where required. Carry original packaging, prescription, doctor's letter, and the import permit. Travel with the minimum quantity you'll reasonably need. Declare at customs. Never carry loose tablets or decanted pills.",
            },
            {
                "q": "What if my opioid is confiscated at customs?",
                "a": "It depends on the country. In permissive jurisdictions you may lose the medication but face no criminal charge. In strict jurisdictions you may be detained. The US embassy can provide assistance but cannot override local law. Prevention via advance permits is the only reliable path.",
            },
            {
                "q": "Is methadone subject to the same rules?",
                "a": "Methadone is tightly regulated worldwide and is especially complicated for travel. Many countries don't recognize foreign methadone prescriptions even with documentation. Long-term methadone patients should work with their clinic on country-specific transfer protocols months in advance.",
            },
        ],
    },
]


# -------------------------------------------------------------------
# Hub-level FAQs — distinct from tier-1-page FAQs
# -------------------------------------------------------------------

HUB_FAQS = [
    {
        "q": "Which medications are most commonly restricted when traveling?",
        "a": "ADHD stimulants (Adderall, Vyvanse, Ritalin), pseudoephedrine (Sudafed), codeine, benzodiazepines (Xanax, Valium), tramadol, strong opioids (oxycodone, morphine), and CBD/cannabis products are the most frequently restricted. Japan, UAE, Saudi Arabia, Singapore, and China have the strictest enforcement.",
    },
    {
        "q": "What's the difference between banned, restricted, and controlled?",
        "a": "\"Banned\" means the medication cannot be brought in under any circumstances — no permit, no prescription, no exception. \"Restricted\" means it requires advance approval, an import permit, or specific documentation. \"Controlled\" means it's classified as a scheduled substance (typically requiring declaration, original packaging, and prescription) but not prohibited.",
    },
    {
        "q": "How do I get an import permit for a prescription medication?",
        "a": "Country-specific. Japan's Yakkan Shoumei (2-4 weeks via mail) is the best-known example. UAE's Ministry of Health and Prevention pre-approval, Singapore's Health Sciences Authority form, and similar processes exist in most countries with controlled-substance rules. Start the process as soon as you book travel, not the week of departure.",
    },
    {
        "q": "What documentation should I carry for any prescription medication abroad?",
        "a": "Original pharmacy label with your name, a signed letter from your prescriber on letterhead (listing medication, dosage, indication, duration), the prescription itself, and any destination-specific pre-approval paperwork. Keep a copy in your checked bag in case your carry-on is lost.",
    },
    {
        "q": "What if my medication is banned at my destination?",
        "a": "Three options: (1) Ask your prescriber about a legal alternative for the trip duration. (2) Delay the trip until you can get off the medication or switch. (3) Accept the risk and travel without, which may be medically unwise. Never smuggle a banned medication — the consequences range from confiscation to imprisonment.",
    },
    {
        "q": "Can I buy my medication at the destination instead?",
        "a": "Sometimes. In most developed countries, a local doctor can re-prescribe after a consultation. In some destinations, common US prescriptions are available OTC or with a simple pharmacist interaction. In strict jurisdictions, your specific medication may not be available at all. Research before you leave.",
    },
    {
        "q": "What if I run out of medication while traveling?",
        "a": "Contact your travel insurance provider first — most have 24/7 medical assistance lines that can locate English-speaking doctors abroad. The US embassy in-country can sometimes help with emergency prescription refills. Telemedicine services (like your existing US prescriber via video call) can issue a fresh prescription in many destinations, though pharmacy-level acceptance varies.",
    },
    {
        "q": "Does carrying pills in a weekly organizer count as \"original packaging\"?",
        "a": "No. Customs officials need to see the pharmacy label with your name, dosage, and prescriber. Transfer pills to the organizer for daily use but keep the original labeled bottle in your bag. Loose pills in an organizer look like a controlled-substance problem to a customs agent.",
    },
    {
        "q": "Where can I verify current rules for my specific destination?",
        "a": "Check: (1) the destination country's embassy website (most publish controlled-substance import rules), (2) the destination's Ministry of Health (often searchable for prescription medication import), (3) the US State Department's country information pages, and (4) our individual country guides at /health/{country}/ for the traveler-oriented summary.",
    },
    {
        "q": "Does tabiji have affiliate relationships with any travel insurance provider or pharmacy?",
        "a": "No. We don't earn commission from any insurance, pharmacy, telemedicine, or import-permit service mentioned on this site. Our recommendations reflect our editorial view only. If that ever changes, we'll disclose it prominently.",
    },
]


# Countries where the relevant permit process is well-documented — used on
# tier-1 pages' "import process" callouts. Keyed by (tier1_slug, country_slug).
IMPORT_PROCESSES = {
    ("adderall", "japan"): None,  # banned — no process
    ("sudafed", "japan"): None,   # banned — no process
}
