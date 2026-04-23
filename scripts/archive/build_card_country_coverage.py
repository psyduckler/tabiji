#!/usr/bin/env python3
"""
Build credit card coverage recommendations by country based on risk profiles.
Outputs api/v1/cards/coverage-by-country.json
"""

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS_DIR = os.path.join(REPO_ROOT, "api/v1/cards")
SAFETY_DIR = os.path.join(REPO_ROOT, "api/v1/safety")
OUTPUT_FILE = os.path.join(REPO_ROOT, "api/v1/cards/coverage-by-country.json")


def load_cards():
    cards = []
    for fname in sorted(os.listdir(CARDS_DIR)):
        if not fname.endswith(".json") or fname == "coverage-by-country.json":
            continue
        with open(os.path.join(CARDS_DIR, fname)) as f:
            cards.append(json.load(f))
    return cards


def load_safety_profiles():
    profiles = []
    for fname in sorted(os.listdir(SAFETY_DIR)):
        if not fname.endswith(".json") or fname == "safety.json":
            continue
        with open(os.path.join(SAFETY_DIR, fname)) as f:
            profiles.append(json.load(f))
    return profiles


def score_card_for_country(card, country):
    """
    Score a card for a country based on its risk profile.
    Returns (score, relevant_benefits list).
    """
    tb = card.get("travelBenefits", {})
    healthcare = country.get("healthcare", {})
    safety = country.get("safety", {})
    practical = country.get("practical", {})
    advisory = country.get("travelAdvisory", {})

    score = 0
    relevant_benefits = []

    quality_rating = healthcare.get("qualityRating", "")
    malaria_risk = healthcare.get("malariaRisk")
    petty_crime = safety.get("pettyCrime", "")
    driving_side = practical.get("drivingSide", "")
    advisory_level = advisory.get("level", 0) or 0
    try:
        advisory_level = int(advisory_level)
    except (TypeError, ValueError):
        advisory_level = 0

    # No foreign transaction fee — benefits all countries
    if tb.get("noForeignTransactionFee"):
        score += 10
        relevant_benefits.append("No foreign transaction fees")

    # High-risk healthcare: poor/very-poor quality OR malaria risk
    if quality_rating in ("poor", "very-poor") or malaria_risk is True:
        evac = tb.get("emergencyMedical", {}) or {}
        if evac.get("evacuation"):
            score += 30
            evac_coverage = evac.get("evacuationCoverage")
            if evac_coverage:
                relevant_benefits.append(
                    f"Emergency evacuation coverage (${evac_coverage:,})"
                )
            else:
                relevant_benefits.append("Emergency evacuation coverage")

    # High advisory level (>= 3)
    if advisory_level >= 3:
        trip_cancel = tb.get("tripCancellation", {}) or {}
        if (trip_cancel.get("coveragePerTrip") or 0) >= 10000:
            score += 15
            relevant_benefits.append(
                f"Trip cancellation (${trip_cancel['coveragePerTrip']:,}/trip)"
            )
        evac = tb.get("emergencyMedical", {}) or {}
        if evac.get("evacuation"):
            score += 20
            # Only add evacuation benefit label if not already added
            if not any("evacuation" in b.lower() for b in relevant_benefits):
                evac_coverage = evac.get("evacuationCoverage")
                if evac_coverage:
                    relevant_benefits.append(
                        f"Emergency evacuation coverage (${evac_coverage:,})"
                    )
                else:
                    relevant_benefits.append("Emergency evacuation coverage")

    # High driving countries (drivingSide exists)
    if driving_side:
        rental = tb.get("rentalCarInsurance", {}) or {}
        if rental.get("type") == "primary":
            score += 15
            coverage_amt = rental.get("coverageAmount")
            if coverage_amt:
                relevant_benefits.append(
                    f"Primary rental car insurance (${coverage_amt:,})"
                )
            else:
                relevant_benefits.append("Primary rental car insurance")

    # High scam/theft risk
    if petty_crime in ("high", "very-high"):
        lost_bag = tb.get("lostBaggage", {}) or {}
        if (lost_bag.get("coveragePerPerson") or 0) >= 1000:
            score += 10
            relevant_benefits.append(
                f"Lost baggage coverage (${lost_bag['coveragePerPerson']:,})"
            )

    return score, relevant_benefits


def compute_country_scoring_factors(country):
    """Determine which scoring factors apply to a country (regardless of card)."""
    healthcare = country.get("healthcare", {})
    safety = country.get("safety", {})
    practical = country.get("practical", {})
    advisory = country.get("travelAdvisory", {})

    factors = ["noForeignTxFee"]  # always applies

    quality_rating = healthcare.get("qualityRating", "")
    malaria_risk = healthcare.get("malariaRisk")
    if quality_rating in ("poor", "very-poor") or malaria_risk is True:
        factors.append("highRiskHealthcare")

    if practical.get("drivingSide"):
        factors.append("primaryRentalCar")

    petty_crime = safety.get("pettyCrime", "")
    if petty_crime in ("high", "very-high"):
        factors.append("highPettyCrime")

    advisory_level = advisory.get("level", 0) or 0
    try:
        advisory_level = int(advisory_level)
    except (TypeError, ValueError):
        advisory_level = 0
    if advisory_level >= 3:
        factors.append("highAdvisoryLevel")

    return sorted(factors)


def main():
    cards = load_cards()
    profiles = load_safety_profiles()

    print(f"Loaded {len(cards)} cards, {len(profiles)} safety profiles")

    countries_data = {}

    for country in profiles:
        iso2 = (country.get("iso2") or "").upper()
        name = country.get("name", "")
        if not iso2:
            continue

        # Score every card for this country
        card_scores = []
        for card in cards:
            score, benefits = score_card_for_country(card, country)
            if score > 0:
                card_scores.append((score, benefits, card))

        # Sort descending, take top 5
        card_scores.sort(key=lambda x: x[0], reverse=True)
        top5 = card_scores[:5]

        scoring_factors = compute_country_scoring_factors(country)

        top_cards = []
        for score, benefits, card in top5:
            top_cards.append(
                {
                    "slug": card["slug"],
                    "name": card["name"],
                    "score": score,
                    "relevantBenefits": benefits,
                    "cardUrl": f"/api/v1/cards/{card['slug']}.json",
                }
            )

        countries_data[iso2] = {
            "iso2": iso2,
            "name": name,
            "topCards": top_cards,
            "scoringFactors": scoring_factors,
        }

    output = {
        "generatedAt": "2026-03-31T00:00:00Z",
        "description": "Credit card recommendations by country based on healthcare quality, safety risk, and travel benefits",
        "countries": countries_data,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Written {OUTPUT_FILE} with {len(countries_data)} countries")

    # Print a sample
    sample_iso2 = "JP"
    if sample_iso2 in countries_data:
        c = countries_data[sample_iso2]
        print(f"\nSample — {c['name']} ({sample_iso2}):")
        print(f"  scoringFactors: {c['scoringFactors']}")
        for tc in c["topCards"]:
            print(f"  [{tc['score']}] {tc['name']}: {tc['relevantBenefits']}")


if __name__ == "__main__":
    main()
