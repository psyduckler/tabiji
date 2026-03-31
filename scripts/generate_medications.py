#!/usr/bin/env python3
"""
Generate medications data for countries missing it in both api/v1/safety/ and kit/data/safety/.
"""
import json, os

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDICATIONS = {
    "ar": {
        "generalAdvice": "Argentina follows international drug conventions. Carry original prescriptions for any controlled substances. Customs may inspect medications — keep all meds in original labeled packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Illegal for recreational use. Medical cannabis exists but not accessible to tourists. Do not carry."},
            {"drug": "Cocaine / coca products", "status": "banned", "note": "Strictly illegal despite regional perception. Severe penalties for possession."},
            {"drug": "Adderall / amphetamines", "status": "restricted", "note": "Carry original prescription and doctor letter. Quantity limited to treatment duration."},
            {"drug": "Benzodiazepines (Xanax, Valium)", "status": "restricted", "note": "Require valid prescription. Carry original packaging and prescription documentation."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Import quantities limited. Declare at customs if carrying more than 30-day supply."}
        ]
    },
    "br": {
        "generalAdvice": "Brazil requires prescriptions for controlled substances. ANVISA (Brazilian Health Agency) regulates imports. Keep medications in original packaging with prescriptions.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Illegal. Medical cannabis exists under strict regulation but not accessible to tourists."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines including Adderall are classified as controlled and generally prohibited for import."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with original prescription and doctor letter. Carry 30-day supply maximum."},
            {"drug": "Benzodiazepines (Xanax, Valium)", "status": "restricted", "note": "Prescription required. Keep in original packaging. Declare at customs."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Quantities strictly limited. Medical certificate recommended."}
        ]
    },
    "cl": {
        "generalAdvice": "Chile follows INCB international conventions. Carry certified prescriptions for controlled substances — ideally apostilled or with official translation. Keep all meds in original packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Medical cannabis exists domestically but tourists cannot import. CBD products prohibited."},
            {"drug": "Adderall / amphetamines", "status": "restricted", "note": "Require original prescription plus certified doctor letter. Quantities limited to trip duration."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with valid prescription. Carry original packaging and medical documentation."},
            {"drug": "Benzodiazepines (Xanax, Valium)", "status": "restricted", "note": "Prescription required. Declare at customs for quantities over 30-day supply."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strict prescription requirements. Notify Chilean health authority (ISP) for imports of Schedule I substances."}
        ]
    },
    "cn": {
        "generalAdvice": "China has extremely strict narcotics laws. ANY amount of many substances triggers severe criminal penalties. Carry only essential medications with official Chinese-translated prescriptions and doctor letters. Do NOT bring opioids, psychotropics, or stimulants without advance NMPA approval.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Zero tolerance. Even trace amounts can lead to arrest and imprisonment. CBD products also prohibited."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Strictly prohibited. No import exemption. Carrying results in criminal prosecution."},
            {"drug": "Opioids (morphine, oxycodone, fentanyl)", "status": "banned", "note": "Prohibited without advance NMPA (National Medical Products Administration) approval, which is rarely granted to tourists."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Requires advance approval from NMPA. Carry original prescription with Chinese translation. Strictly limit to personal use quantities."},
            {"drug": "Benzodiazepines (Xanax, Valium, Klonopin)", "status": "restricted", "note": "Carry original prescription with official Chinese translation. Declare at customs. Maximum 1-month supply."},
            {"drug": "Pseudoephedrine (Sudafed)", "status": "banned", "note": "Prohibited. Use alternative decongestants containing phenylephrine only."}
        ]
    },
    "cz": {
        "generalAdvice": "Czech Republic follows EU drug regulations. EU prescriptions are generally honored. Carry original prescriptions for any controlled substances and keep medications in original packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "restricted", "note": "Medical cannabis legal with EU prescription. Recreational cannabis decriminalized in small amounts but still illegal. Do not attempt to import."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines prohibited. Czech prescriptions for stimulants use different medications (methylphenidate preferred)."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with valid EU or foreign prescription. Carry original packaging and medical letter."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. EU prescriptions valid. Non-EU travelers should carry original prescription with Czech/English translation."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Declare at customs. EU Schengen certificate recommended for travel within EU."}
        ]
    },
    "eg": {
        "generalAdvice": "Egypt has strict drug laws. Psychotropics, narcotics, and stimulants require prior approval from the Egyptian Ministry of Health. Carry original prescriptions with Arabic translation and doctor letters. Border checks are thorough.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Zero tolerance. Severe criminal penalties including imprisonment. CBD also prohibited."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Strictly prohibited. Do not attempt to carry into Egypt."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Requires advance approval from Egyptian Ministry of Health. Carry prescription with Arabic translation."},
            {"drug": "Benzodiazepines (Xanax, Valium)", "status": "restricted", "note": "Requires Ministry of Health permit for import. Carry prescription with Arabic translation. Strict quantity limits."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strictly controlled. Prior approval required. Carry detailed medical documentation. Declare at customs."},
            {"drug": "Tramadol", "status": "banned", "note": "Frequently misused substance — Egypt treats it as a narcotic. Do not carry tramadol into Egypt."}
        ]
    },
    "hr": {
        "generalAdvice": "Croatia follows EU drug regulations. EU prescriptions are recognized. Non-EU travelers should carry prescriptions in English or Croatian with a doctor letter. Keep medications in original packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "restricted", "note": "Medical cannabis available with Croatian prescription. CBD products with <0.2% THC tolerated. Do not import cannabis."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines not prescribed in Croatia. Do not import Adderall."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with valid prescription. Carry medical letter for non-EU travelers."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. EU Schengen certificate recommended for travel with controlled substances."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Declare at customs. Carry EU travel certificate if transiting multiple EU countries."}
        ]
    },
    "hu": {
        "generalAdvice": "Hungary follows EU/Schengen drug regulations. Carry original prescriptions and doctor letters for controlled substances. EU travelers may use a Schengen controlled substance travel certificate for multi-country trips.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Hungary has no medical cannabis program. Cannabis products prohibited. Zero tolerance policy."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines prohibited. Hungary does not prescribe them."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with prescription. Non-EU travelers should carry medical letter and original packaging."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Schengen travel certificate recommended for EU multi-country travel."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Declare at customs. Carry documentation for all opioid medications."}
        ]
    },
    "in": {
        "generalAdvice": "India's Narcotic Drugs and Psychotropic Substances Act (NDPS) imposes severe penalties. Carry original prescriptions with doctor letter for ANY controlled substance. Keep medications in original packaging and declare at customs.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Illegal under NDPS Act. Severe penalties including minimum 6-month imprisonment. CBD also prohibited."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Strictly prohibited under NDPS. Do not carry into India."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Carry original prescription with doctor letter. Declare at customs. Limited to 30-day personal supply."},
            {"drug": "Benzodiazepines (Xanax, Valium)", "status": "restricted", "note": "Require original prescription. Carry sufficient supply as availability varies. Declare at customs."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strictly controlled under NDPS. Carry original prescription and medical certificate. Declare at customs. Quantity strictly limited."},
            {"drug": "Tramadol", "status": "restricted", "note": "Controlled under NDPS. Carry original prescription. Misuse penalties are severe."}
        ]
    },
    "ke": {
        "generalAdvice": "Kenya requires prescriptions for all controlled substances. Carry medications in original packaging with doctor letters. Customs checks medications thoroughly — undeclared controlled substances can lead to arrest.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Strictly illegal. Severe criminal penalties. CBD products also prohibited."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Prohibited. Do not carry into Kenya."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Carry original prescription and doctor letter. Declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Carry original packaging and doctor letter."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strictly controlled. Carry original prescription and medical letter. Declare at customs. Quantity limited to trip duration."}
        ]
    },
    "lk": {
        "generalAdvice": "Sri Lanka has strict drug laws. Carry original prescriptions for all controlled medications. Declare at customs and keep medications in original labeled packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Strictly illegal with severe penalties. Cannabis decriminalization discussed but not enacted."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Prohibited. Do not carry into Sri Lanka."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Carry original prescription and doctor letter. Declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Original packaging and doctor letter recommended."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strictly controlled. Doctor letter and original prescription mandatory. Declare at customs."}
        ]
    },
    "my": {
        "generalAdvice": "Malaysia has mandatory death penalty for drug trafficking above threshold amounts. ANY controlled substance requires advance Health Ministry approval. Carry original prescriptions and doctor letters. Declare everything at customs.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Death penalty for trafficking. Zero tolerance for any amount. CBD also illegal."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Methamphetamine and amphetamines carry death penalty for trafficking. Do not carry."},
            {"drug": "Opioids (morphine, oxycodone)", "status": "restricted", "note": "Requires advance approval from Malaysian Ministry of Health. Carry all documentation and declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Prior approval recommended. Carry original packaging with prescription."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Carry original prescription with doctor letter. Advance approval from Ministry of Health recommended."},
            {"drug": "Tramadol", "status": "restricted", "note": "Controlled substance. Carry prescription and declare at customs. Do not carry unmarked tablets."}
        ]
    },
    "no": {
        "generalAdvice": "Norway follows strict Nordic drug regulations. Schengen travel certificate required for controlled substances when crossing EU/EEA borders. Carry original prescriptions for all medications.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Illegal for recreational use. Medical cannabis available under strict prescription. Do not import."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Adderall not prescribed in Norway. Amphetamines strictly controlled. Do not carry."},
            {"drug": "Methylphenidate (Ritalin/Concerta)", "status": "restricted", "note": "Allowed with Norwegian or foreign prescription. Schengen travel certificate required for multi-country EU travel."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Norway has strict prescribing limits — carry sufficient supply from home country with doctor letter."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Codeine available OTC in limited quantities. Stronger opioids require prescription. Schengen certificate for EU travel."}
        ]
    },
    "ph": {
        "generalAdvice": "The Philippines has extremely strict drug laws under the Comprehensive Dangerous Drugs Act. Death penalty was historically applied and remains on the table politically. ANY controlled substance requires a PNP (Philippine National Police) permit to import. Carry original prescriptions and declare everything.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Zero tolerance. Death penalty territory for trafficking. CBD also prohibited regardless of THC content."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Methamphetamine (shabu) is the Philippines' biggest drug crisis — all amphetamines treated with extreme severity."},
            {"drug": "Opioids (morphine, oxycodone, fentanyl)", "status": "restricted", "note": "Requires PNP Drug Enforcement Group import permit obtained before travel. Carry all permits, prescriptions, and doctor letters."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Requires PNP permit prior to import. Carry original prescription and doctor letter. Declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Controlled substance. Carry original prescription. PNP permit recommended for extended stays."},
            {"drug": "Tramadol", "status": "restricted", "note": "Classified as controlled. Carry prescription and declare at customs."}
        ]
    },
    "pl": {
        "generalAdvice": "Poland follows EU/Schengen drug regulations. EU prescriptions are valid. Schengen controlled substance travel certificate recommended for trips involving multiple EU countries. Keep medications in original packaging.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "restricted", "note": "Medical cannabis available with Polish prescription. CBD <0.2% THC technically tolerated. Do not import recreational cannabis."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines prohibited in Poland. Not prescribed here — do not import Adderall."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with EU or foreign prescription and doctor letter. Schengen travel certificate for multi-country EU trips."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. EU Schengen certificate recommended. Original packaging required."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Prescription required. Declare at customs for quantities over 30-day supply. Schengen certificate recommended."}
        ]
    },
    "se": {
        "generalAdvice": "Sweden has strict drug enforcement. Schengen travel certificate required for controlled substances when crossing borders. Sweden prescribes pain medications more conservatively than the US — carry sufficient supply from home.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Illegal. Sweden has no recreational or medical cannabis program. Zero tolerance."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Adderall not prescribed in Sweden. Do not carry — amphetamines are strictly controlled."},
            {"drug": "Methylphenidate (Ritalin/Concerta)", "status": "restricted", "note": "Allowed with prescription. Schengen travel certificate required for multi-EU travel. Carry 30-day supply max."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Sweden limits benzodiazepine prescribing — carry supply from home with doctor letter."},
            {"drug": "Opioids / strong pain medications", "status": "restricted", "note": "Strictly controlled. Swedish prescriptions rare for opioids. Carry doctor letter explaining medical necessity."}
        ]
    },
    "sg": {
        "generalAdvice": "Singapore has zero tolerance for drug offenses. Mandatory death penalty applies to trafficking above threshold amounts. ANY controlled substance requires Health Sciences Authority (HSA) import authorization before travel. Declare everything.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Death penalty for trafficking. Zero tolerance. CBD products also completely banned — do not carry any cannabis-derived product."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Strictly prohibited. Death penalty territory for trafficking amounts."},
            {"drug": "Opioids (morphine, oxycodone, fentanyl)", "status": "restricted", "note": "Requires advance HSA import authorization. Carry authorization letter, original prescription, and declare at customs."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Requires HSA import authorization. Obtain before travel. Carry all documentation."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Require HSA authorization. Carry original prescription and authorization letter. Declare at customs."},
            {"drug": "Tramadol", "status": "restricted", "note": "Controlled substance. HSA authorization required. Carry prescription and declare."}
        ]
    },
    "tz": {
        "generalAdvice": "Tanzania has strict drug laws. Carry original prescriptions for all controlled medications in original packaging. Declare controlled substances at customs — undeclared medications can lead to detention.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "banned", "note": "Strictly illegal. Tanzania is a major regional enforcement country. Severe criminal penalties."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Prohibited. Do not carry into Tanzania."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Carry original prescription and doctor letter. Declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Original packaging and doctor letter essential."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Strictly controlled. Carry original prescription and medical letter. Declare at customs. Limited to trip duration supply."}
        ]
    },
    "us": {
        "generalAdvice": "The US has complex federal and state drug laws. Cannabis is federally illegal despite state legalization — international travelers may NOT bring cannabis into the US. Prescription medications must be in original containers with the prescribing label. TSA checks medications but focuses primarily on security threats.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD (from abroad)", "status": "banned", "note": "Federally illegal to bring cannabis into the US, even from countries where legal. CBD from hemp may be permitted but high legal uncertainty — do not bring."},
            {"drug": "Opioids (morphine, oxycodone, fentanyl)", "status": "restricted", "note": "US prescriptions required. Foreign visitors must carry valid prescription with doctor letter and keep in original labeled container."},
            {"drug": "Adderall / amphetamines", "status": "restricted", "note": "Schedule II controlled substance. Must be in original prescription container with your name on label. Carry prescription documentation."},
            {"drug": "Benzodiazepines (Xanax, Valium, Klonopin)", "status": "restricted", "note": "Schedule IV controlled substance. Keep in original prescription container. Carry valid prescription."},
            {"drug": "Psilocybin / MDMA", "status": "banned", "note": "Schedule I substances — federally illegal regardless of decriminalization in some states. Do not carry."}
        ]
    },
    "za": {
        "generalAdvice": "South Africa has strict Medicines and Related Substances Act. Cannabis was decriminalized for personal use domestically but remains illegal to import/export. Carry original prescriptions for all controlled substances.",
        "controlledSubstances": [
            {"drug": "Cannabis / CBD", "status": "restricted", "note": "Personal use decriminalized domestically, but importing cannabis into SA is still illegal. CBD products with low THC available."},
            {"drug": "Adderall / amphetamines", "status": "banned", "note": "Amphetamines not prescribed in South Africa. Do not carry Adderall into SA."},
            {"drug": "Methylphenidate (Ritalin)", "status": "restricted", "note": "Allowed with original prescription and doctor letter. Declare at customs."},
            {"drug": "Benzodiazepines", "status": "restricted", "note": "Prescription required. Keep in original packaging. Declare at customs."},
            {"drug": "Opioids / codeine", "status": "restricted", "note": "Codeine recently moved to prescription-only. Stronger opioids require original prescription and declaration at customs."}
        ]
    },
}

def patch_file(filepath, iso):
    if not os.path.exists(filepath):
        print(f"  SKIP {filepath}: not found")
        return False
    with open(filepath) as fh:
        d = json.load(fh)
    if d.get("medications"):
        print(f"  SKIP {iso}: already has medications")
        return False
    d["medications"] = MEDICATIONS[iso]
    with open(filepath, "w") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return True

api_dir = os.path.join(repo, "api/v1/safety")
kit_dir = os.path.join(repo, "kit/data/safety")

for iso in sorted(MEDICATIONS.keys()):
    api_path = os.path.join(api_dir, f"{iso}.json")
    kit_path = os.path.join(kit_dir, f"{iso}.json")
    api_ok = patch_file(api_path, iso)
    kit_ok = patch_file(kit_path, iso)
    if api_ok or kit_ok:
        print(f"  Patched {iso}: api={api_ok} kit={kit_ok}")

print("\nDone.")
