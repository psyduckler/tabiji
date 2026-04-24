"""
Per-carrier rich editorial content for the 15 insurance carrier pages.

Separated from lib.editorial (which holds the lightweight catalog used by the
hub + API) because only the carrier-page builder needs these long narrative
fields.

Each entry keyed by carrier slug, with:
    overview        — 2-3 sentence opening paragraph
    ppo_hmo_note    — plan-type-specific guidance paragraph
    covered         — list of items covered abroad
    not_covered     — list of items not covered abroad
    need_to_know    — list of callouts: {tone, title, body}
    ask_questions   — list of 6 questions tailored to the carrier's structure
    claim_steps     — list of {title, body} for the "filing a claim" walkthrough
    scenario        — concrete cost scenario: {destination, total, reimbursed, your_cost, body}
    supplemental_verdict — carrier-specific supplemental-insurance recommendation paragraph
    faqs            — list of {q, a} Q/A entries
    sources         — list of {name, url} references
"""

from __future__ import annotations


SHARED_ASK_QUESTIONS_BASE = [
    "Is international emergency care covered at in-network or out-of-network rates?",
    "Is medical evacuation included, and if so, what's the dollar cap?",
    "Do I need pre-authorization for non-emergency international care?",
    "What's my out-of-network deductible and coinsurance for international claims?",
    "Is there a per-incident or annual cap on international coverage?",
    "What documentation do I need to file an international claim, and how long does reimbursement take?",
]

SHARED_CLAIM_STEPS = [
    {
        "title": "Call your carrier's assistance line first if possible",
        "body": "For non-emergency care, call before you go in. Many carriers with international assistance lines can locate in-network facilities and arrange direct billing. In an emergency, go to the nearest hospital first; call within 48 hours.",
    },
    {
        "title": "Pay with a credit card",
        "body": "Credit cards create an audit trail and give you dispute leverage if the hospital overbills. Save every charge slip.",
    },
    {
        "title": "Collect every piece of documentation",
        "body": "Itemized bill, medical report, diagnostic codes, discharge summary, and proof of payment. Ask the hospital for English-language copies — most international facilities will provide them on request.",
    },
    {
        "title": "Submit the claim promptly",
        "body": "Most carriers require claim submission within 90–180 days. Include translated copies if your documents are in another language. Track the submission confirmation number.",
    },
    {
        "title": "Expect partial reimbursement",
        "body": "Carriers reimburse at their \"usual and customary\" rates, which can be 30–70% less than what you paid. Plan on a gap. This is the single biggest argument for a supplemental travel policy that direct-pays the hospital instead.",
    },
]


CARRIER_CONTENT = {
    # ---------------------------------------------------------------
    "blue-cross-blue-shield": {
        "overview": (
            "Blue Cross Blue Shield isn't one company — it's an association of 34 independent licensees "
            "operating state by state. Most BCBS plans offer international emergency coverage through the "
            "BCBS Global Core program, which gives you access to doctors and hospitals in 190+ countries. "
            "Coverage varies significantly between licensees and plan types, so your Texas BCBS plan and a "
            "Massachusetts BCBS plan can behave very differently abroad."
        ),
        "ppo_hmo_note": (
            "PPO plans carry the strongest international benefit: emergency care abroad is covered at "
            "out-of-network rates, and some plans include urgent care. HMO plans typically limit you to "
            "emergencies only. HDHP/HSA plans follow their underlying PPO or HMO rules, but you pay the "
            "full deductible first. If you travel internationally more than once a year and have a BCBS "
            "HMO, a PPO is worth the higher premium."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core network",
            "Emergency hospitalization",
            "Urgent care — on some PPO plans",
            "Emergency ambulance transport",
            "Medical evacuation — varies by licensee; many include it, some don't",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies (most plans)",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "danger",
                "title": "34 different companies, 34 different rules",
                "body": "Your BCBS plan in one state operates completely differently from another. Always verify with YOUR specific licensee — generic BCBS information may not apply to your plan.",
            },
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "1-800-810-BLUE (2583) is the Global Core Service Center. For emergencies, go to the nearest hospital first and call within 48 hours. Many Global Core hospitals can direct-bill BCBS.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment is still common",
                "body": "Even within Global Core, many international hospitals require upfront payment. Keep every receipt and itemized bill — you'll file claims yourself for reimbursement after returning.",
            },
        ],
        "ask_questions": [
            "Does my specific BCBS licensee participate in Global Core?",
            *SHARED_ASK_QUESTIONS_BASE[:5],
        ],
        "scenario": {
            "destination": "Tokyo ER visit for broken arm",
            "total": "$12,000",
            "reimbursed": "$4,800",
            "your_cost": "$7,200",
            "body": (
                "Your BCBS PPO covers the visit at out-of-network rates, billed at BCBS's \"usual and "
                "customary\" rate for that procedure in their determination — which is substantially less "
                "than Tokyo's actual price. You paid $12K upfront (Japan always expects upfront payment), "
                "filed a claim on return, and got back $4,800 after the out-of-network deductible. Net: "
                "$7,200 out of pocket. A supplemental travel policy with direct billing would have fronted "
                "the full cost and cost you ~$40 for the week."
            ),
        },
        "supplemental_verdict": (
            "Strongly recommended. BCBS Global Core is decent for emergencies, but medical evacuation "
            "isn't consistently included across all licensees, and routine care abroad is excluded. If "
            "you're traveling to high-cost countries (Japan, Switzerland, Australia), remote areas, or "
            "staying more than two weeks, supplemental travel insurance is the difference between a "
            "manageable reimbursement gap and a ruinous one."
        ),
        "faqs": [
            {
                "q": "What is BCBS Global Core?",
                "a": "A network of international providers in 190+ countries that BCBS members can access. Call 1-800-810-BLUE (2583) before non-emergency care; for emergencies, go to the nearest hospital and call within 48 hours. Many Global Core hospitals can direct-bill BCBS, reducing your upfront out-of-pocket.",
            },
            {
                "q": "Is my BCBS the same as Anthem, Highmark, or HCSC?",
                "a": "All are BCBS licensees, but each is a separate company with its own plans, rates, and benefit rules. Coverage details can differ substantially even for the same plan type. Check with your specific licensee, not generic BCBS.",
            },
            {
                "q": "What's GeoBlue and how does it relate to BCBS?",
                "a": "GeoBlue is a BCBS-affiliated supplemental travel health insurance product designed for extended international stays. It's not automatic with your regular BCBS plan — you purchase it separately. GeoBlue is widely regarded as one of the better supplemental options for frequent BCBS members.",
            },
            {
                "q": "Does Medicare BCBS Advantage cover me abroad?",
                "a": "BCBS Medicare Advantage plans may include limited international emergency coverage with a lifetime cap (typically $25K–50K). Check your specific plan's Summary of Benefits. For substantial international travel, Medigap + a travel medical policy is the stronger setup.",
            },
        ],
        "sources": [
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "Blue Cross Blue Shield Association", "url": "https://www.bcbs.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "unitedhealthcare": {
        "overview": (
            "UnitedHealthcare is the largest private health insurer in the US. For international travel, "
            "most UHC plans cover emergency care abroad at out-of-network rates through the UHC Global "
            "network. UHC Global also operates a separate international expat insurance product for "
            "long-stay travelers and Americans living abroad."
        ),
        "ppo_hmo_note": (
            "UHC PPOs perform the best internationally — emergency coverage and out-of-network reimbursement "
            "are standard. HMO plans (including Oxford, UHC's HMO brand in some states) cover emergencies "
            "only. HDHP/HSA plans require the full deductible first but otherwise follow the underlying "
            "plan type's rules."
        ),
        "covered": [
            "Emergency room visits abroad at out-of-network rates",
            "Emergency hospitalization and ambulance transport",
            "Urgent care on most PPO plans",
            "Direct billing available at select international hospitals in UHC's network",
            "Medical evacuation on some plans — check your specific benefits",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Planned or elective procedures",
            "Prescription refills at foreign pharmacies",
            "Care in countries subject to US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "UHC Global is a separate expat product",
                "body": "Don't confuse UHC Global Assistance (available to most US members for travel emergencies) with UHC Global expat plans (a separate purchase for long-stay travelers). The expat plan is what you want if you're living abroad for more than 3 months.",
            },
            {
                "tone": "caution",
                "title": "\"Usual and customary\" reimbursement",
                "body": "Like most US carriers, UHC reimburses international care at their determined rates — not what you actually paid. Expect a reimbursement gap of 30–60% on high-cost international care.",
            },
            {
                "tone": "info",
                "title": "Direct billing where available",
                "body": "UHC has direct-billing relationships with hospitals in major cities — Tokyo, Singapore, London, Zurich, etc. Call the member services number on your card before heading to the hospital if possible.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Barcelona emergency appendix surgery",
            "total": "$18,000",
            "reimbursed": "$10,500",
            "your_cost": "$7,500",
            "body": (
                "UHC PPO covers international emergencies at out-of-network rates. You paid the private "
                "Barcelona hospital ~$18K on your credit card, filed a claim with UHC, and got back $10,500 "
                "after the $5K out-of-network deductible and 20% coinsurance. Net: $7,500. A supplemental "
                "travel policy with emergency direct billing would have covered the full cost for ~$80 for "
                "the trip."
            ),
        },
        "supplemental_verdict": (
            "Recommended. UHC PPO is one of the better US carriers abroad, but you still pay upfront and "
            "face reimbursement gaps. Medical evacuation coverage is inconsistent across plans. For trips "
            "longer than two weeks, adventure travel, or high-cost destinations, supplemental travel "
            "insurance pays for itself the first time you use it."
        ),
        "faqs": [
            {
                "q": "Does UHC Global cover me automatically when I travel?",
                "a": "Most UHC members have access to UHC Global Assistance (a 24/7 travel emergency hotline and international provider network) as part of their plan. UHC Global expat insurance is a separate product for long-stay travelers — not the same thing.",
            },
            {
                "q": "Will UHC direct-bill an international hospital?",
                "a": "In select cities, yes. Call the member services number on your card before seeking non-emergency care. For emergencies, go to the nearest hospital first; UHC can often arrange direct billing after the fact.",
            },
            {
                "q": "What about Oxford Health Plans?",
                "a": "Oxford is UHC's HMO brand in the New York tri-state area. Like most HMOs, Oxford limits international coverage to emergencies only. Members traveling internationally should strongly consider supplemental travel insurance.",
            },
        ],
        "sources": [
            {"name": "UnitedHealthcare", "url": "https://www.uhc.com/"},
            {"name": "UHC Global (expat plans)", "url": "https://www.uhcglobal.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "aetna": {
        "overview": (
            "Aetna (now a CVS Health company) covers international emergencies on most commercial plans, "
            "typically at out-of-network rates. For longer trips or expat living, Aetna International is a "
            "separate dedicated product with a global provider network. The distinction matters: a US-based "
            "Aetna commercial plan is a different animal from Aetna International."
        ),
        "ppo_hmo_note": (
            "PPO plans cover international emergencies at out-of-network rates. HMO and EPO plans limit "
            "international coverage to true emergencies. HDHP/HSA plans follow the underlying plan type "
            "with the deductible applied first. For travelers under 65, Aetna International is worth "
            "quoting separately if you're abroad more than 90 days a year."
        ),
        "covered": [
            "Emergency room visits abroad at out-of-network rates",
            "Emergency hospitalization",
            "Emergency ambulance transport",
            "Some urgent care — PPO plans only",
            "Medical evacuation on specific Aetna International plans (not standard commercial)",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Planned surgeries or medical tourism",
            "Prescription refills at foreign pharmacies",
            "Care in countries subject to US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Aetna International is a separate product",
                "body": "If you're living abroad or traveling for 3+ months a year, Aetna International is worth quoting. It includes direct billing at international hospitals, higher evacuation caps, and outpatient coverage — things the standard commercial plan doesn't have.",
            },
            {
                "tone": "caution",
                "title": "Commercial plan = emergency only",
                "body": "Standard US Aetna commercial plans cover emergencies abroad at out-of-network rates, but nothing routine. Budget for a 40–60% reimbursement gap even on covered claims.",
            },
            {
                "tone": "info",
                "title": "Member services handles travel claims",
                "body": "There's no dedicated Aetna travel assistance line for commercial members — call the member services number on your card. Aetna International members have a separate 24/7 assistance number in their plan documents.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "London broken leg with surgery",
            "total": "$22,000",
            "reimbursed": "$12,000",
            "your_cost": "$10,000",
            "body": (
                "An Aetna PPO commercial plan covered the emergency at out-of-network rates. You paid "
                "the London private hospital $22K upfront, filed a claim with Aetna, and got back $12K "
                "after the $7,500 out-of-network deductible and 20% coinsurance on the rest. Net: $10K. "
                "A supplemental travel policy with direct billing (~$75 for the trip) would have eliminated "
                "the gap entirely."
            ),
        },
        "supplemental_verdict": (
            "Recommended. Standard Aetna commercial plans handle emergencies but leave meaningful "
            "reimbursement gaps and exclude evacuation on most plans. For long stays abroad, Aetna "
            "International is a strong primary option. For short trips, a supplemental travel medical "
            "policy alongside your commercial Aetna plan is the cheap, effective combination."
        ),
        "faqs": [
            {
                "q": "What's the difference between Aetna and Aetna International?",
                "a": "Aetna is US-based commercial and Medicare insurance. Aetna International is a separate product for expats and frequent travelers, with a global provider network, direct billing, and outpatient coverage. You can't convert one to the other — they're distinct purchases.",
            },
            {
                "q": "Is Aetna PPO good for travel?",
                "a": "Aetna PPO is average among US carriers — competent for emergencies, weak on evacuation and non-emergency care. Not as good as Cigna or BCBS PPO for international scenarios, but considerably better than Kaiser or Medicaid plans.",
            },
            {
                "q": "Does Aetna Medicare Advantage cover travel?",
                "a": "Limited. Most Aetna Medicare Advantage plans include emergency international coverage with a lifetime cap. For substantial travel, Medigap + a travel medical policy is the stronger combination.",
            },
        ],
        "sources": [
            {"name": "Aetna", "url": "https://www.aetna.com/"},
            {"name": "Aetna International", "url": "https://www.aetnainternational.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "cigna": {
        "overview": (
            "Cigna is the strongest US carrier for international coverage among major domestic insurers. "
            "Standard Cigna commercial PPO plans cover emergencies abroad; Cigna Global is a dedicated "
            "international product with wide worldwide access that's often cited as a top expat choice. "
            "Cigna has invested more in international infrastructure than most domestic peers."
        ),
        "ppo_hmo_note": (
            "Cigna PPOs cover emergency international care at out-of-network rates and often include "
            "urgent care. Cigna HMO/EPO plans are more restrictive, though some have emergency travel "
            "benefits built in. For frequent travelers, Cigna Global is worth pricing separately — it "
            "operates as a true international plan rather than a domestic plan with travel add-ons."
        ),
        "covered": [
            "Emergency room visits abroad at out-of-network rates",
            "Emergency hospitalization and ambulance",
            "Urgent care on most PPO plans",
            "Direct billing available at a large number of international facilities",
            "Medical evacuation — included on many plans; confirm specifics",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision internationally",
            "Pre-planned elective care or medical tourism",
            "Prescription refills at foreign pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Cigna Global is the expat standard",
                "body": "If you're living or working abroad, Cigna Global competes with BUPA and Allianz Care as a top choice. Direct billing at hospitals worldwide, outpatient coverage, and flexible tiered plans.",
            },
            {
                "tone": "info",
                "title": "Standard PPO is above average",
                "body": "Among domestic US carriers, Cigna commercial PPO handles international scenarios better than most. Still plan on a reimbursement gap — no US primary plan fully covers foreign costs.",
            },
            {
                "tone": "info",
                "title": "24/7 assistance on most plans",
                "body": "Cigna includes a 24/7 international assistance line with most commercial plans. Call before non-emergency care or when you need help locating an English-speaking provider.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Singapore chest pain evaluation and observation",
            "total": "$9,000",
            "reimbursed": "$5,500",
            "your_cost": "$3,500",
            "body": (
                "Cigna PPO covered the emergency at out-of-network rates. Singapore's private Mount Elizabeth "
                "Hospital charged ~$9K for an ER visit with overnight observation. Cigna reimbursed $5,500 "
                "after the deductible and coinsurance. Net: $3,500 out of pocket — reasonable by US-carrier "
                "standards, but a supplemental travel policy would have knocked that to near-zero."
            ),
        },
        "supplemental_verdict": (
            "Recommended. Cigna PPO is better than most domestic carriers abroad, but supplemental "
            "insurance still adds medical evacuation coverage, trip cancellation, and out-of-pocket "
            "reimbursement for the gaps Cigna won't cover. For trips longer than 2 weeks or high-cost "
            "destinations, it's the high-value buy."
        ),
        "faqs": [
            {
                "q": "What's the difference between Cigna and Cigna Global?",
                "a": "Cigna is US-based commercial, Medicare, and Medicaid insurance. Cigna Global is a dedicated international plan for expats and frequent travelers with broader coverage and direct hospital billing. They're separate products — you'd buy Cigna Global in addition to or instead of a domestic plan.",
            },
            {
                "q": "Is Cigna better than BCBS for international travel?",
                "a": "Slightly, on average. Cigna tends to have broader direct-billing relationships and more consistent evacuation coverage than BCBS licensees, but specific plans vary. If you travel often, Cigna Global or BCBS GeoBlue are both strong supplemental options.",
            },
            {
                "q": "Does Cigna HMO cover international emergencies?",
                "a": "Most Cigna HMO plans include emergency travel coverage at out-of-network rates. Non-emergency care abroad generally isn't covered. Check your specific plan's Summary of Benefits.",
            },
        ],
        "sources": [
            {"name": "Cigna", "url": "https://www.cigna.com/"},
            {"name": "Cigna Global", "url": "https://www.cignaglobal.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "humana": {
        "overview": (
            "Humana is primarily a Medicare Advantage carrier — the majority of Humana members are Medicare-age. "
            "International emergency coverage is included on most Humana Medicare Advantage plans with a "
            "lifetime cap (typically $25K–50K). Humana's commercial employer plans behave like typical US "
            "PPOs or HMOs, but Humana's footprint in commercial insurance is limited compared to BCBS, UHC, "
            "and Aetna."
        ),
        "ppo_hmo_note": (
            "Most Humana members have a Medicare Advantage plan governed by Medicare Advantage rules — which "
            "means emergency international coverage with a lifetime cap and no routine care abroad. "
            "Humana's commercial PPOs function like typical PPO plans. The bigger issue for Humana members "
            "is almost always the Medicare Advantage lifetime cap, which is easy to blow through on a single "
            "serious incident abroad."
        ),
        "covered": [
            "Emergency care abroad on most Medicare Advantage plans — subject to lifetime cap",
            "Emergency hospitalization and ambulance",
            "Emergency urgent care — typically at out-of-network rates",
            "Limited dental emergency coverage on some plans",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Non-emergency care of any kind",
            "Coverage beyond the lifetime cap (typically $25K–50K)",
            "Medical evacuation on most plans",
            "Prescription refills at foreign pharmacies",
        ],
        "need_to_know": [
            {
                "tone": "danger",
                "title": "Lifetime cap is the critical number",
                "body": "Most Humana Medicare Advantage plans cap foreign emergency coverage at $25,000–50,000 LIFETIME. One serious hospitalization abroad can exhaust it. Budget accordingly — supplemental travel insurance is effectively mandatory.",
            },
            {
                "tone": "caution",
                "title": "Medicare Advantage rules apply",
                "body": "Humana's international coverage follows Medicare Advantage conventions — emergency only, lifetime capped, no routine care. Medigap plans F, G, and N offer a stronger foreign-travel emergency benefit (80% after deductible, $50K lifetime) if you have Original Medicare.",
            },
            {
                "tone": "info",
                "title": "Call member services before traveling",
                "body": "Confirm your specific plan's international cap and any pre-authorization requirements. Requirements vary by state and plan year; get the answer in writing.",
            },
        ],
        "ask_questions": [
            "What is my plan's lifetime cap on international emergency coverage?",
            "How much have I already used toward that cap?",
            "Is medical evacuation included on my plan, and at what dollar limit?",
            "Does my plan require pre-authorization for international care?",
            "What's the process for filing an international claim?",
            "Is a Medigap plan with foreign-travel emergency coverage available to me?",
        ],
        "scenario": {
            "destination": "Costa Rica rural ambulance + ER for fall",
            "total": "$8,500",
            "reimbursed": "$6,800",
            "your_cost": "$1,700",
            "body": (
                "A Humana Medicare Advantage plan covered the emergency up to its lifetime cap. You paid "
                "$8,500 upfront in San José, filed a claim, and got back $6,800 — good on paper, but you "
                "burned ~$7K of your $25K lifetime international cap. If this was your first emergency "
                "abroad and you have more travel ahead, supplemental insurance just became non-optional."
            ),
        },
        "supplemental_verdict": (
            "Essential. Humana members — especially those on Medicare Advantage — should treat supplemental "
            "travel insurance as mandatory. The lifetime cap is too tight, the evacuation coverage is too "
            "thin, and age-related risks amplify the financial exposure. Budget $60–200 per trip for a "
            "policy with evacuation coverage."
        ),
        "faqs": [
            {
                "q": "Does Humana Medicare Advantage cover travel abroad?",
                "a": "Most plans cover emergency care abroad with a lifetime cap (typically $25K–50K). Routine care, follow-up, and most evacuation are not covered. Supplemental travel insurance is effectively required.",
            },
            {
                "q": "Is Humana commercial better than Humana Medicare Advantage for travel?",
                "a": "Humana commercial PPO plans function like typical US PPOs — no lifetime international cap but reimbursement rates apply. Slightly better for travel, but Humana commercial enrollment is small relative to their Medicare Advantage book.",
            },
            {
                "q": "What's Medigap and do I have it?",
                "a": "Medigap (Medicare Supplement Insurance) is a separate policy that fills gaps in Original Medicare. Plans F, G, and N include an 80% foreign-travel emergency benefit up to a $50K lifetime cap — a much better travel profile than Medicare Advantage. You only have Medigap if you bought it separately; check your benefits documents.",
            },
        ],
        "sources": [
            {"name": "Humana", "url": "https://www.humana.com/"},
            {"name": "Medicare.gov — Travel abroad", "url": "https://www.medicare.gov/coverage/travel-needing-health-care-outside-us"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "kaiser-permanente": {
        "overview": (
            "Kaiser Permanente operates as a closed-system HMO in most markets — you see Kaiser doctors at "
            "Kaiser facilities, and the integrated model is one of Kaiser's strengths domestically. "
            "Internationally, the same model is a severe liability. Kaiser covers emergency care abroad "
            "only to stabilize you for transfer back to a Kaiser facility, with no international network "
            "and no direct billing anywhere."
        ),
        "ppo_hmo_note": (
            "Kaiser is HMO-first. Some regions offer a Point-of-Service (POS) option with limited "
            "out-of-network benefits, but this rarely extends meaningfully abroad. There is no standard "
            "Kaiser PPO. If you travel internationally and have a choice at open enrollment, a PPO plan "
            "from another carrier will almost always handle travel scenarios better than any Kaiser product."
        ),
        "covered": [
            "Emergency care to stabilize a life-threatening condition",
            "Emergency ambulance transport",
            "Limited urgent care when you can't reasonably wait until returning home",
        ],
        "not_covered": [
            "Any routine, preventive, or planned care abroad",
            "Follow-up care after emergency stabilization",
            "Prescription medications from international pharmacies",
            "Medical evacuation or repatriation",
            "Mental health care abroad (except life-threatening emergencies)",
            "Dental, vision, and hearing care internationally",
        ],
        "need_to_know": [
            {
                "tone": "danger",
                "title": "Worst major US carrier for international travel",
                "body": "Kaiser's closed-system HMO model makes it the least travel-friendly major US carrier. Traveling internationally with only Kaiser coverage means you are significantly underinsured. Supplemental travel insurance is not optional — it's essential.",
            },
            {
                "tone": "caution",
                "title": "Pay 100% upfront, claim back at Kaiser's rates",
                "body": "Kaiser has no international provider network. You will pay 100% of costs upfront at any international facility, then file for reimbursement. Kaiser reimburses at their determined 'reasonable and customary' rates, which may be far less than what you actually paid.",
            },
            {
                "tone": "info",
                "title": "Kaiser Away From Home Travel Line",
                "body": "Kaiser operates a travel assistance line at 1-951-268-3900 (collect calls accepted). Useful for locating medical facilities abroad, but doesn't translate to direct billing or expanded coverage.",
            },
        ],
        "ask_questions": [
            "What does Kaiser define as an emergency for international coverage?",
            "What is the reimbursement rate for international emergency care, and how is \"reasonable and customary\" determined?",
            "Is there a dollar cap on international emergency coverage?",
            "Does my plan include any travel assistance services beyond the Away From Home line?",
            "What documentation do I need to file an international claim?",
            "How long does Kaiser take to process international claims?",
        ],
        "scenario": {
            "destination": "Paris emergency appendectomy",
            "total": "$16,000",
            "reimbursed": "$5,500",
            "your_cost": "$10,500",
            "body": (
                "Kaiser covered the emergency at their reimbursement rate. You paid the Paris hospital "
                "$16K on your credit card; Kaiser reimbursed $5,500 based on their determination of "
                "\"reasonable and customary\" charges for the procedure. Net: $10,500 out of pocket. A "
                "supplemental travel policy with direct billing (~$50 for the trip) would have paid the "
                "hospital directly and left you with nothing out of pocket."
            ),
        },
        "supplemental_verdict": (
            "Absolutely essential — non-negotiable. Kaiser members should never travel internationally "
            "without supplemental travel health insurance. Kaiser's coverage abroad is bare-minimum "
            "emergency-only with no evacuation coverage and no network access. The gap between what you "
            "pay and what Kaiser reimburses routinely exceeds the cost of a year's worth of travel "
            "insurance."
        ),
        "faqs": [
            {
                "q": "Why is Kaiser so bad for international travel?",
                "a": "Kaiser's value proposition is the integrated care model: your doctors, pharmacy, labs, and specialists are all under the Kaiser umbrella. That integration doesn't exist outside the US, so Kaiser can't leverage its domestic network or direct-billing relationships. You're on your own for billing, paperwork, and follow-up.",
            },
            {
                "q": "Can I use my Kaiser HSA for travel medical expenses?",
                "a": "Yes, qualifying medical expenses incurred abroad are HSA-eligible. Keep itemized bills and translations. This doesn't replace supplemental insurance — it just gives you a tax-advantaged way to pay the gap.",
            },
            {
                "q": "Is Kaiser Senior Advantage (Medicare) any different?",
                "a": "Kaiser Senior Advantage is a Medicare Advantage plan with the same international limitations. Emergency-only, capped, no evacuation. For Medicare-age Kaiser members who travel, Medigap + a travel medical policy on Original Medicare is a significantly stronger setup.",
            },
            {
                "q": "What if I have an emergency abroad and can't reach the Kaiser Travel Line?",
                "a": "Go to the nearest hospital. Pay upfront, save everything, and file a claim on return. The Kaiser Travel Line is useful but not required — don't let inability to reach them delay care.",
            },
        ],
        "sources": [
            {"name": "Kaiser Permanente", "url": "https://healthy.kaiserpermanente.org/"},
            {"name": "Kaiser Away From Home Care", "url": "https://healthy.kaiserpermanente.org/health-wellness/travel"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "anthem": {
        "overview": (
            "Anthem is a Blue Cross Blue Shield licensee covering 14 states, operating under the BCBS "
            "umbrella and using the BCBS Global Core program for international emergency coverage. Anthem "
            "members traveling abroad should expect standard Blue international rules: PPO plans are "
            "strongest, HMO plans are emergency-only, and Global Core gives access to a network of "
            "190+ countries."
        ),
        "ppo_hmo_note": (
            "Anthem PPO plans carry the best international benefit — emergency and sometimes urgent care "
            "abroad at out-of-network rates. Anthem HMO plans limit coverage to emergencies only. HDHP "
            "plans follow the underlying plan type with the deductible applied first. If you travel often, "
            "a PPO is worth the higher premium at open enrollment."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization",
            "Urgent care on some PPO plans",
            "Emergency ambulance transport",
            "Medical evacuation — varies by plan; confirm specifics",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "1-800-810-BLUE (2583) is the Global Core Service Center shared across all BCBS licensees including Anthem. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue rules apply",
                "body": "Global Core network in 190+ countries with direct billing available at many international hospitals. Same program as any other BCBS licensee — Anthem doesn't change the rules, just badges them.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment still common",
                "body": "Even with Global Core, many international hospitals require upfront payment. Save receipts and itemized bills — you'll file claims yourself for reimbursement after returning.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Cancun ER visit for moderate dengue",
            "total": "$4,200",
            "reimbursed": "$2,100",
            "your_cost": "$2,100",
            "body": (
                "Anthem PPO covered the emergency at out-of-network rates. You paid the private Cancun "
                "hospital $4,200 upfront, filed a claim, and got back $2,100 after deductible and "
                "coinsurance. Net: $2,100 — manageable but avoidable. A supplemental travel policy "
                "(~$40 for the week) would have covered the whole thing."
            ),
        },
        "supplemental_verdict": (
            "Recommended. Anthem PPO covers emergencies abroad competently, but medical evacuation "
            "isn't consistently included and routine care is excluded. For trips to high-cost destinations "
            "or anything longer than two weeks, supplemental travel insurance closes the gap for less than "
            "a night's hotel."
        ),
        "faqs": [
            {
                "q": "Is Anthem the same as Blue Cross Blue Shield?",
                "a": "Anthem is one of 34 BCBS licensees. It operates independently but uses BCBS branding and the BCBS Global Core program. Plans, rates, and specific benefits differ from other BCBS licensees even for the same plan type.",
            },
            {
                "q": "What states does Anthem cover?",
                "a": "Anthem operates in 14 states: California, Colorado, Connecticut, Georgia, Indiana, Kentucky, Maine, Missouri, Nevada, New Hampshire, New York (portions), Ohio, Virginia, and Wisconsin. Other BCBS plans in those states may exist alongside Anthem.",
            },
            {
                "q": "Does GeoBlue work with Anthem?",
                "a": "Yes. GeoBlue is a BCBS-affiliated supplemental product available to members of any BCBS licensee including Anthem. Strong option for expats or frequent travelers.",
            },
        ],
        "sources": [
            {"name": "Anthem", "url": "https://www.anthem.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "centene": {
        "overview": (
            "Centene is the largest Medicaid managed-care carrier in the US, operating state Medicaid "
            "plans, Marketplace plans (Ambetter), and Medicare Advantage plans (Wellcare) across 50 "
            "states. International coverage varies dramatically by subsidiary and state — and is almost "
            "nonexistent on most Medicaid products. For Centene members traveling abroad, the default "
            "assumption should be: you are on your own."
        ),
        "ppo_hmo_note": (
            "Centene's Medicaid plans are almost always HMOs with no out-of-network benefits and no "
            "international coverage. Ambetter Marketplace plans vary by state; some include limited "
            "emergency international coverage, most don't. Wellcare Medicare Advantage follows Medicare "
            "Advantage rules with lifetime-capped international emergency coverage."
        ),
        "covered": [
            "On some Marketplace (Ambetter) plans: emergency coverage abroad at out-of-network rates — confirm specifics",
            "On Wellcare Medicare Advantage: emergency care with a lifetime cap",
            "On Medicaid plans: essentially nothing abroad",
        ],
        "not_covered": [
            "Routine or non-emergency care abroad, on any Centene product",
            "Medical evacuation on nearly all plans",
            "Prescription refills at foreign pharmacies",
            "Any care in countries under US sanctions",
            "On Medicaid plans: international care of any kind, with very narrow exceptions",
        ],
        "need_to_know": [
            {
                "tone": "danger",
                "title": "Medicaid plans don't travel",
                "body": "If you have a Centene-managed state Medicaid plan (Fidelis, Superior, Peach State, etc.), there is effectively no international coverage. Supplemental travel medical insurance is non-negotiable if you're traveling abroad.",
            },
            {
                "tone": "caution",
                "title": "Subsidiary matters more than the Centene name",
                "body": "Your specific product — Ambetter, Wellcare, Fidelis, or a state-branded Medicaid plan — has its own rules. Check member documents for your specific brand, not generic Centene materials.",
            },
            {
                "tone": "info",
                "title": "Member services is the starting point",
                "body": "Call the member services number on your card to get your specific plan's international coverage details. Ask for the policy language in writing.",
            },
        ],
        "ask_questions": [
            "Which Centene subsidiary am I enrolled in, and what are its specific international coverage rules?",
            "Is emergency international care covered, and if so at what rate and cap?",
            "Is medical evacuation included on any Centene product I have?",
            "What documentation do I need for an international claim?",
            "Are there any travel-related exclusions I should know about?",
            "Does my plan include any 24/7 travel assistance line?",
        ],
        "scenario": {
            "destination": "Jamaica ER for severe food poisoning",
            "total": "$2,800",
            "reimbursed": "$0–$500",
            "your_cost": "$2,300–$2,800",
            "body": (
                "A Centene-managed Medicaid plan reimbursed nothing — Medicaid doesn't travel. An Ambetter "
                "Marketplace plan might reimburse a portion ($0–$500) depending on the specific plan and "
                "state. Either way, you paid most or all of the $2,800 out of pocket. A supplemental "
                "travel policy would have been ~$30 for the trip."
            ),
        },
        "supplemental_verdict": (
            "Essential — mandatory, not optional. Centene Medicaid members should never travel "
            "internationally without a supplemental travel medical policy. Ambetter Marketplace and "
            "Wellcare Medicare Advantage members should also strongly consider supplemental coverage given "
            "the narrow scope of what's included."
        ),
        "faqs": [
            {
                "q": "What is Centene — is it my insurance?",
                "a": "Centene is the parent company behind brand names including Ambetter (Marketplace), Wellcare (Medicare Advantage), Fidelis (NY Medicaid), Superior (TX Medicaid), Peach State (GA Medicaid), and others. Your plan documents show the specific brand — Centene is the umbrella.",
            },
            {
                "q": "Does Ambetter cover travel?",
                "a": "Varies by state. Some Ambetter plans include emergency international coverage at out-of-network rates; many don't. Check your specific state's Ambetter plan documents.",
            },
            {
                "q": "What should Medicaid members do for travel?",
                "a": "Buy a supplemental travel medical policy before you leave. Plan on $30–80 per week for a policy with evacuation coverage. Treat Medicaid as purely domestic — it doesn't follow you abroad.",
            },
        ],
        "sources": [
            {"name": "Centene Corporation", "url": "https://www.centene.com/"},
            {"name": "Ambetter", "url": "https://www.ambetterhealth.com/"},
            {"name": "Wellcare", "url": "https://www.wellcare.com/"},
            {"name": "Medicaid.gov — Out of country care", "url": "https://www.medicaid.gov/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
        ],
    },
    # ---------------------------------------------------------------
    "molina-healthcare": {
        "overview": (
            "Molina Healthcare is a Medicaid-focused managed-care carrier operating in 18 states, with "
            "some Marketplace and Medicare Advantage products. International coverage is minimal to "
            "nonexistent across Molina's product line — Medicaid plans don't travel, and Molina's "
            "Marketplace and Medicare offerings have narrow international benefits at best."
        ),
        "ppo_hmo_note": (
            "Molina plans are predominantly HMOs with no out-of-network benefits. International travel "
            "scenarios fall outside the plan architecture — there's no mechanism to pay a foreign provider. "
            "Medicare Advantage plans follow MA rules with lifetime-capped emergency coverage; "
            "Marketplace plans vary."
        ),
        "covered": [
            "On Medicare Advantage: emergency care abroad with a lifetime cap",
            "On some Marketplace plans: emergency coverage at out-of-network rates — confirm specifics",
            "On Medicaid plans: essentially nothing abroad",
        ],
        "not_covered": [
            "Routine or non-emergency care abroad on any Molina plan",
            "Medical evacuation on nearly all plans",
            "Prescription refills at foreign pharmacies",
            "Any care in countries under US sanctions",
            "International care of any kind on Medicaid plans",
        ],
        "need_to_know": [
            {
                "tone": "danger",
                "title": "Supplemental travel insurance is essential",
                "body": "Molina's Medicaid and Marketplace products weren't designed with international travel in mind. If you're traveling abroad, a supplemental travel medical policy is the standard of care — don't leave without one.",
            },
            {
                "tone": "caution",
                "title": "Pay upfront, reimbursement unlikely",
                "body": "Molina has no international provider network and no direct-billing relationships abroad. Any foreign care will be paid upfront, and reimbursement is unlikely to meaningfully cover the cost.",
            },
            {
                "tone": "info",
                "title": "Call member services before traveling",
                "body": "Confirm your specific plan's international coverage rules and get answers in writing. Requirements vary by state and plan year.",
            },
        ],
        "ask_questions": [
            "Does my Molina plan include any international coverage?",
            "If I have an emergency abroad, what's the reimbursement process?",
            "Is medical evacuation included on any of my Molina products?",
            "What documentation is required for international claims?",
            "Are there any pre-authorization requirements?",
            "Does my plan include a 24/7 nurse or travel assistance line?",
        ],
        "scenario": {
            "destination": "Dominican Republic ambulance + ER for scooter crash",
            "total": "$6,500",
            "reimbursed": "$0",
            "your_cost": "$6,500",
            "body": (
                "A Molina Medicaid plan reimbursed nothing. You paid the full $6,500 out of pocket on "
                "your credit card. A supplemental travel policy with emergency medical evacuation "
                "coverage (~$50 for the trip) would have paid the hospital directly and covered "
                "transportation back to a US facility if needed."
            ),
        },
        "supplemental_verdict": (
            "Essential — mandatory. Molina members traveling abroad need a supplemental travel medical "
            "policy. Budget $30–80 per week for a policy with emergency evacuation coverage. Skipping it "
            "means paying the full cost of any international incident yourself."
        ),
        "faqs": [
            {
                "q": "Does Medicaid cover me when I travel abroad?",
                "a": "No. Medicaid covers care within the US only, with extremely narrow exceptions for emergencies near the US border. Supplemental travel medical insurance is essential.",
            },
            {
                "q": "What states does Molina operate in?",
                "a": "Molina operates in 18 states including California, Florida, Illinois, Michigan, New Mexico, New York, Ohio, South Carolina, Texas, Utah, Virginia, Washington, and Wisconsin among others. Product mix varies by state.",
            },
            {
                "q": "Does Molina Marketplace cover travel?",
                "a": "Coverage varies by state plan. Some Molina Marketplace plans include emergency international coverage at out-of-network rates; many don't. Check your specific plan's Summary of Benefits and Coverage.",
            },
        ],
        "sources": [
            {"name": "Molina Healthcare", "url": "https://www.molinahealthcare.com/"},
            {"name": "Medicaid.gov", "url": "https://www.medicaid.gov/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "hcsc": {
        "overview": (
            "Health Care Service Corporation (HCSC) is the BCBS licensee for Illinois, Texas, New Mexico, "
            "Oklahoma, and Montana — the largest customer-owned health insurer in the US by membership. "
            "HCSC members get standard BCBS Global Core access for international emergency coverage."
        ),
        "ppo_hmo_note": (
            "HCSC offers PPO, HMO, and HDHP options in each of its five states. PPO plans carry the "
            "strongest international benefit via Global Core. HMO plans limit coverage to emergencies. "
            "HDHP plans require the deductible first. Standard Blue international rules apply."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on some PPO plans",
            "Medical evacuation — varies by plan; confirm specifics",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "1-800-810-BLUE (2583) is the Global Core Service Center used by all BCBS licensees including HCSC. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue international rules",
                "body": "Global Core network in 190+ countries. Direct billing available at many international hospitals. HCSC uses the same BCBS infrastructure as Anthem, Highmark, CareFirst, Premera, and Regence.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment still common",
                "body": "Even within Global Core, many international hospitals require upfront payment. Keep receipts for reimbursement claims.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Madrid ER for kidney stones",
            "total": "$3,800",
            "reimbursed": "$2,300",
            "your_cost": "$1,500",
            "body": (
                "HCSC PPO covered the emergency at out-of-network rates. You paid the Madrid private "
                "hospital $3,800 upfront, filed a claim, and got back $2,300 after deductible and "
                "coinsurance. Net: $1,500. A supplemental travel policy (~$35 for the trip) would have "
                "closed most of the gap."
            ),
        },
        "supplemental_verdict": (
            "Recommended. HCSC PPO handles emergencies abroad competently through Global Core, but "
            "medical evacuation and non-emergency care require supplemental coverage. For trips to "
            "high-cost destinations or longer than two weeks, supplemental insurance is the high-value buy."
        ),
        "faqs": [
            {
                "q": "What states does HCSC cover?",
                "a": "Illinois, Texas, New Mexico, Oklahoma, and Montana. HCSC operates under the Blue Cross and Blue Shield brand in all five states (e.g., \"Blue Cross Blue Shield of Texas\").",
            },
            {
                "q": "Is HCSC the same as BCBS Texas?",
                "a": "HCSC is the parent company; BCBS of Texas (along with IL, NM, OK, MT) is how it operates publicly. Members see the BCBS brand on their card; HCSC is the underwriter behind the scenes.",
            },
            {
                "q": "Does GeoBlue work with HCSC?",
                "a": "Yes. GeoBlue is available to members of any BCBS licensee including HCSC. A strong supplemental option for extended international travel.",
            },
        ],
        "sources": [
            {"name": "HCSC (Health Care Service Corporation)", "url": "https://www.hcsc.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "highmark": {
        "overview": (
            "Highmark is the Blue Cross Blue Shield licensee for Pennsylvania (western + central), West "
            "Virginia, Delaware, and parts of New York. Members access BCBS Global Core for international "
            "emergency coverage — same rules as other BCBS licensees."
        ),
        "ppo_hmo_note": (
            "Highmark PPO plans cover international emergencies at out-of-network rates through Global "
            "Core. HMO plans are emergency-only. HDHP plans require the deductible first. Highmark also "
            "markets Community Blue HMO in some areas — which is a standard HMO for international "
            "purposes."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on some PPO plans",
            "Medical evacuation — varies by plan; confirm specifics",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "Global Core Service Center, shared across all BCBS licensees. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue international rules",
                "body": "Global Core access in 190+ countries. Direct billing available at many international hospitals.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment expectations",
                "body": "Save receipts and itemized bills from any international care — reimbursement claims require documentation.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Edinburgh ER for allergic reaction",
            "total": "$2,100",
            "reimbursed": "$1,250",
            "your_cost": "$850",
            "body": (
                "Highmark PPO covered the emergency at out-of-network rates. You paid the Edinburgh "
                "hospital $2,100 upfront, filed a claim, and got back $1,250 after the deductible. Net: "
                "$850 — manageable, but a $40 supplemental policy would have covered the trip entirely."
            ),
        },
        "supplemental_verdict": (
            "Recommended. Highmark PPO handles emergencies through Global Core but doesn't consistently "
            "include evacuation. For high-cost destinations or longer stays, supplemental travel insurance "
            "is the high-value buy — typically $30–80 a week with evacuation coverage."
        ),
        "faqs": [
            {
                "q": "What area does Highmark cover?",
                "a": "Highmark is the BCBS licensee for western and central Pennsylvania, West Virginia, Delaware, and parts of New York. Eastern Pennsylvania is served by Independence Blue Cross.",
            },
            {
                "q": "Is Highmark the same as Blue Cross Blue Shield?",
                "a": "Highmark is one of 34 BCBS licensees — it operates independently but uses BCBS branding and the Global Core international program. Plans and rates differ from other BCBS licensees.",
            },
            {
                "q": "What's Allegheny Health Network's relationship to Highmark?",
                "a": "AHN is Highmark's integrated delivery network — a group of hospitals and physician practices in western PA that Highmark owns. It's a domestic care model; doesn't affect international coverage.",
            },
        ],
        "sources": [
            {"name": "Highmark", "url": "https://www.highmark.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "independence-blue-cross": {
        "overview": (
            "Independence Blue Cross (IBX) is the BCBS licensee for southeastern Pennsylvania (Philadelphia "
            "and surrounding counties). Members get access to BCBS Global Core for emergency international "
            "coverage, with easy add-on to GeoBlue for extended travel or expat coverage."
        ),
        "ppo_hmo_note": (
            "IBX PPO plans carry the best international benefit — Global Core access and out-of-network "
            "reimbursement for emergencies. Personal Choice (IBX PPO brand) is a common plan. HMO "
            "plans (Keystone Health Plan East) are emergency-only internationally. HDHP plans apply the "
            "deductible first."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on most PPO plans",
            "Medical evacuation — varies; GeoBlue supplement available for consistent coverage",
            "Direct billing at many international hospitals",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "GeoBlue integrates smoothly",
                "body": "As a BCBS licensee, IBX members can easily add GeoBlue for supplemental international coverage — useful for expats, long trips, or frequent travel. Direct billing at international hospitals with evacuation coverage.",
            },
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "Global Core Service Center. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment still common",
                "body": "Save receipts and itemized bills from any international care for reimbursement claims.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Rome private hospital ER for chest pain",
            "total": "$5,500",
            "reimbursed": "$3,400",
            "your_cost": "$2,100",
            "body": (
                "IBX Personal Choice PPO covered the emergency at out-of-network rates. You paid the "
                "Rome hospital $5,500 upfront, filed a claim, and got back $3,400 after deductible and "
                "coinsurance. Net: $2,100. A GeoBlue supplemental (~$60 for the trip) would have "
                "direct-billed and covered the whole thing."
            ),
        },
        "supplemental_verdict": (
            "Recommended. IBX PPO handles emergencies competently through Global Core. For longer trips, "
            "expat stays, or frequent travel, GeoBlue is the natural supplemental choice — same BCBS "
            "umbrella, seamless integration, and broader coverage than your primary plan."
        ),
        "faqs": [
            {
                "q": "What area does IBX cover?",
                "a": "Southeastern Pennsylvania — Philadelphia, Bucks, Chester, Delaware, and Montgomery counties. Other parts of Pennsylvania (western + central) are served by Highmark.",
            },
            {
                "q": "What is Personal Choice?",
                "a": "Personal Choice is IBX's PPO product line. Includes international emergency coverage through Global Core and is the strongest IBX option for travelers.",
            },
            {
                "q": "Is GeoBlue worth it for IBX members?",
                "a": "For frequent travelers or anyone spending more than 2 weeks abroad, yes. GeoBlue adds direct billing at international hospitals, evacuation coverage, and outpatient care — gaps IBX primary plans don't fill.",
            },
        ],
        "sources": [
            {"name": "Independence Blue Cross", "url": "https://www.ibx.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "carefirst": {
        "overview": (
            "CareFirst is the BCBS licensee for Maryland, Washington DC, and northern Virginia. Members "
            "get standard BCBS Global Core access for international emergency coverage, with PPO plans "
            "offering the strongest travel benefits."
        ),
        "ppo_hmo_note": (
            "CareFirst PPO plans cover international emergencies at out-of-network rates through Global "
            "Core. CareFirst BlueChoice HMO plans are emergency-only internationally. HDHP plans apply "
            "the deductible first. Standard Blue international rules throughout."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on some PPO plans",
            "Medical evacuation — varies; confirm with your specific plan",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "Global Core Service Center, shared across all BCBS licensees. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue international rules apply",
                "body": "Global Core network in 190+ countries. Direct billing available at many international hospitals.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment still common",
                "body": "Save receipts from any international care — reimbursement claims require itemized documentation.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Athens ER for moderate concussion",
            "total": "$3,600",
            "reimbursed": "$2,100",
            "your_cost": "$1,500",
            "body": (
                "CareFirst PPO covered the emergency at out-of-network rates. You paid the Athens "
                "private hospital $3,600 upfront, filed a claim, and got back $2,100 after deductible "
                "and coinsurance. Net: $1,500. A supplemental travel policy (~$40 for the trip) would "
                "have closed most of the gap."
            ),
        },
        "supplemental_verdict": (
            "Recommended. CareFirst PPO handles emergencies through Global Core but doesn't consistently "
            "include evacuation. For high-cost destinations, adventure travel, or trips longer than two "
            "weeks, supplemental travel insurance is the high-value buy."
        ),
        "faqs": [
            {
                "q": "What area does CareFirst cover?",
                "a": "Maryland, Washington DC, and northern Virginia. Other parts of Virginia are served by Anthem (BCBS Virginia) and other BCBS licensees.",
            },
            {
                "q": "What's the difference between CareFirst BlueCross BlueShield and CareFirst BlueChoice?",
                "a": "CareFirst BlueCross BlueShield is the traditional PPO offering. CareFirst BlueChoice is the HMO brand. PPO is stronger for international travel.",
            },
            {
                "q": "Does GeoBlue work with CareFirst?",
                "a": "Yes. GeoBlue is available to members of any BCBS licensee including CareFirst. Strong option for expats or frequent travelers.",
            },
        ],
        "sources": [
            {"name": "CareFirst BlueCross BlueShield", "url": "https://www.carefirst.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "premera-blue-cross": {
        "overview": (
            "Premera Blue Cross is the BCBS licensee for Washington State and Alaska. Alaska residents "
            "face a distinctive geography problem — in-state specialty care often requires travel to "
            "Seattle or Anchorage — so evacuation coverage matters more than for most BCBS members."
        ),
        "ppo_hmo_note": (
            "Premera PPO plans carry the strongest international benefit through Global Core. HMO plans "
            "(including Premera's smaller HMO products) are emergency-only. HDHP plans apply the "
            "deductible first. Alaska members: treat evacuation coverage as a baseline requirement, not a "
            "luxury."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on some PPO plans",
            "Medical evacuation — varies by plan; Alaska residents should verify carefully",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "caution",
                "title": "Alaska geography amplifies evacuation risk",
                "body": "Alaska residents can face $50K+ medical transport costs even within the US if specialty care requires Seattle or Anchorage. International scenarios stack on top of that. Evacuation coverage is a priority, not an afterthought.",
            },
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "Global Core Service Center, shared across all BCBS licensees. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue international rules",
                "body": "Global Core access in 190+ countries. Direct billing available at many international hospitals.",
            },
        ],
        "ask_questions": [
            "Is medical evacuation covered on my specific Premera plan, and at what dollar limit?",
            *SHARED_ASK_QUESTIONS_BASE[:5],
        ],
        "scenario": {
            "destination": "Iceland emergency surgery for appendicitis",
            "total": "$28,000",
            "reimbursed": "$18,000",
            "your_cost": "$10,000",
            "body": (
                "Premera PPO covered the emergency at out-of-network rates. Iceland's private hospital "
                "costs are high; you paid $28K upfront, filed a claim, and got back $18K after deductible "
                "and coinsurance. Net: $10K. For a Washington or Alaska member, a supplemental travel "
                "policy (~$60 for the trip) would have saved the $10K gap and added evacuation coverage."
            ),
        },
        "supplemental_verdict": (
            "Recommended — for Alaska members, essential. Premera PPO handles emergencies through Global "
            "Core, but Alaska's geography makes evacuation coverage critical. For any traveler, a "
            "supplemental policy with evacuation limits of $250K+ is the high-value buy."
        ),
        "faqs": [
            {
                "q": "What area does Premera cover?",
                "a": "Washington State (primary market) and Alaska. Other BCBS licensees cover adjacent states (Regence in Oregon and Idaho, for example).",
            },
            {
                "q": "Is Premera the largest insurer in Washington?",
                "a": "Among the largest. Premera competes with Regence and Kaiser Permanente Washington in the state. Alaska members have fewer alternatives — Premera is the dominant BCBS option.",
            },
            {
                "q": "Does GeoBlue work with Premera?",
                "a": "Yes. Available to members of any BCBS licensee including Premera. Alaska members with extensive travel plans should seriously consider it for the evacuation coverage.",
            },
        ],
        "sources": [
            {"name": "Premera Blue Cross", "url": "https://www.premera.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
    # ---------------------------------------------------------------
    "regence": {
        "overview": (
            "Regence is the Blue Cross Blue Shield licensee for Washington, Oregon, Idaho, and Utah. "
            "Members get standard BCBS Global Core access for international emergency coverage. Regence "
            "operates as four affiliated entities (Regence BlueShield, Regence BlueCross BlueShield of "
            "Oregon, etc.) but international rules are consistent."
        ),
        "ppo_hmo_note": (
            "Regence PPO plans carry the best international benefit through Global Core. HMO plans are "
            "emergency-only. HDHP plans apply the deductible first. Standard Blue international rules "
            "throughout Regence's four-state footprint."
        ),
        "covered": [
            "Emergency room visits abroad through Global Core",
            "Emergency hospitalization and ambulance",
            "Urgent care on some PPO plans",
            "Medical evacuation — varies by plan; confirm specifics",
        ],
        "not_covered": [
            "Routine or preventive care abroad",
            "Dental or vision care internationally",
            "Pre-planned surgeries or medical tourism",
            "Prescription refills at international pharmacies",
            "Care in countries under US sanctions",
        ],
        "need_to_know": [
            {
                "tone": "info",
                "title": "Call 1-800-810-BLUE before non-emergency care",
                "body": "Global Core Service Center, shared across all BCBS licensees. For emergencies, go to the nearest hospital first and call within 48 hours.",
            },
            {
                "tone": "info",
                "title": "Standard Blue international rules",
                "body": "Global Core access in 190+ countries. Direct billing available at many international hospitals.",
            },
            {
                "tone": "caution",
                "title": "Upfront payment still common",
                "body": "Save receipts and itemized bills from any international care for reimbursement claims.",
            },
        ],
        "ask_questions": SHARED_ASK_QUESTIONS_BASE,
        "scenario": {
            "destination": "Lisbon ER for severe migraine workup",
            "total": "$2,900",
            "reimbursed": "$1,700",
            "your_cost": "$1,200",
            "body": (
                "Regence PPO covered the emergency at out-of-network rates. You paid the Lisbon "
                "hospital $2,900 upfront, filed a claim, and got back $1,700 after deductible and "
                "coinsurance. Net: $1,200. A supplemental travel policy (~$40 for the trip) would have "
                "closed the gap."
            ),
        },
        "supplemental_verdict": (
            "Recommended. Regence PPO handles emergencies competently through Global Core, but medical "
            "evacuation coverage is inconsistent and routine care is excluded. For high-cost destinations "
            "or trips longer than two weeks, supplemental travel insurance is the high-value buy."
        ),
        "faqs": [
            {
                "q": "What states does Regence cover?",
                "a": "Washington (Regence BlueShield), Oregon (Regence BlueCross BlueShield of Oregon), Idaho (Regence BlueShield of Idaho), and Utah (Regence BlueCross BlueShield of Utah). Four affiliated companies, consistent BCBS rules.",
            },
            {
                "q": "Is Regence the same as Premera in Washington?",
                "a": "Both are BCBS licensees in Washington operating under Blue branding, but they're separate companies with different plans, networks, and rates. Different employer groups may offer one or the other.",
            },
            {
                "q": "Does GeoBlue work with Regence?",
                "a": "Yes. Available to members of any BCBS licensee including Regence. Strong supplemental option for expats or frequent travelers.",
            },
        ],
        "sources": [
            {"name": "Regence", "url": "https://www.regence.com/"},
            {"name": "BCBS Global Core", "url": "https://www.bcbsglobalcore.com/"},
            {"name": "GeoBlue (BCBS supplemental)", "url": "https://www.geo-blue.com/"},
            {"name": "US State Department — Travel Insurance Guide", "url": "https://travel.state.gov/content/travel/en/international-travel/before-you-go/your-health-abroad.html"},
            {"name": "NAIC — National Association of Insurance Commissioners", "url": "https://www.naic.org/"},
        ],
    },
}
