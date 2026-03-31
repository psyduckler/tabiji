#!/usr/bin/env python3
"""
Task 3a: Add emergencyWorkflows to all api/v1/safety/ profiles.
Idempotent — skips files that already have emergencyWorkflows.
Uses actual embassy/emergency values from each file.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SAFETY_DIR = ROOT / "api" / "v1" / "safety"


def driving_note(data: dict) -> str:
    side = (data.get("practical") or {}).get("drivingSide", "right")
    side_upper = side.upper()
    if side == "left":
        return (
            "Traffic drives on the LEFT. An International Driving Permit (IDP) is required "
            "for most foreign licenses. Rental vehicles are available at major airports and cities."
        )
    return (
        "Traffic drives on the RIGHT. An International Driving Permit (IDP) is recommended "
        "for most foreign licenses. Rental vehicles are available at major airports and cities."
    )


def build_workflows(data: dict) -> dict:
    em = data.get("emergency") or {}
    embassies = data.get("embassies") or []
    first_embassy = embassies[0] if embassies else {}

    embassy_phone = first_embassy.get("emergencyPhone") or first_embassy.get("phone") or "Contact the nearest US Embassy"
    embassy_url = first_embassy.get("website") or "https://www.usembassy.gov/"
    police_number = em.get("police") or "local police"
    ambulance_number = em.get("ambulance") or "local ambulance service"

    return {
        "stolenPassport": {
            "steps": [
                "File a police report immediately — get the report number, you will need it",
                f"Contact the US Embassy or nearest consulate: {embassy_phone}",
                "Bring the police report + any ID you have (driver's license, copy of passport)",
                "Apply for an Emergency Passport (usually issued within 1-2 business days)",
                "Notify your travel insurance and airline of the situation",
            ],
            "embassyPhone": embassy_phone,
            "embassyUrl": embassy_url,
            "notes": (
                "Keep a digital copy of your passport in cloud storage (Google Photos, iCloud) "
                "and email yourself a scan before travel."
            ),
        },
        "policeReport": {
            "steps": [
                f"Go to the nearest police station (or call {police_number})",
                "Bring ID or a copy of your passport if available",
                "Request a written report — ask for an English copy or certified translation if needed",
                "Keep the report number safe — required for insurance claims",
                "For theft: list all stolen items with approximate values",
            ],
            "policeNumber": police_number,
            "notes": (
                "In many countries, tourist police stations are available in major cities — "
                "they have English-speaking staff. Ask your hotel concierge for the nearest tourist police."
            ),
        },
        "roadsideAssistance": {
            "steps": [
                "If involved in an accident: do not move vehicles if anyone is injured",
                f"Call police ({police_number}) and ambulance ({ambulance_number}) if there are injuries",
                "Exchange contact, license, and insurance details with other parties",
                "Document the scene with photos before moving vehicles",
                "Contact your rental car company's emergency line",
                "Contact your travel insurance's 24h assistance line",
            ],
            "policeNumber": police_number,
            "ambulanceNumber": ambulance_number,
            "notes": driving_note(data),
        },
    }


def process_file(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))

    if "emergencyWorkflows" in data:
        print(f"  SKIP (already has emergencyWorkflows): {path.name}")
        return False

    data["emergencyWorkflows"] = build_workflows(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  PATCHED: {path.name}")
    return True


def main():
    files = sorted(SAFETY_DIR.glob("*.json"))
    files = [f for f in files if f.name != "safety.json"]

    patched = 0
    skipped = 0
    for f in files:
        if process_file(f):
            patched += 1
        else:
            skipped += 1

    print(f"\nDone. Patched={patched}, Skipped={skipped}, Total={len(files)}")


if __name__ == "__main__":
    main()
