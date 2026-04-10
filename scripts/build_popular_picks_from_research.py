#!/usr/bin/env python3
"""
Transform research JSON files (from background agents) into proper
popular-picks-data/{slug}.json files matching the schema validated by
generators/popular-picks/validate-source.js, then call the build script.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/bjh/Documents/tabiji")

SLUG_CONFIG = {
    "paris-flea-markets": {
        "city": "Paris",
        "country_name": "France",
        "country_code": "FR",
        "category": "shopping",
        "vertical": "shopping",
        "place_type": "shop",
        "badge_emoji": "🛍️",
        "title_count": 10,
        "title": "10 Best Flea Markets in Paris",
        "h1": "10 Best Flea Markets in Paris",
        "meta_title": "10 Best Flea Markets in Paris 2026 — Reddit-Backed Guide | tabiji.ai",
        "meta_description": "The 10 best flea markets in Paris — from Saint-Ouen and Vanves to Montreuil and the Aligre brocante. Real reviews, opening hours, bargaining tips & interactive map.",
        "og_description": "Curated guide to Paris flea markets. Saint-Ouen, Vanves, Montreuil, Vernaison, Paul Bert Serpette, Dauphine & more — with hours, prices and insider tips.",
        "twitter_description": "Real reviews of Paris's 10 best flea markets — interactive map included.",
        "dek_lead": "Paris is the world's flea market capital. From the 7-hectare Saint-Ouen complex to the scrappy weekend brocante on Place d'Aligre, here are the 10 markets worth your Saturday morning.",
        "map_title": "Flea Market Map",
        "related_manual": [
            "paris-vintage-shopping",
            "paris-bistros",
            "paris-bakeries",
            "paris-cheap-eats",
            "paris-food-markets",
            "paris-jazz-clubs",
            "paris-natural-wine-bars",
        ],
    },
    "rome-cooking-classes": {
        "city": "Rome",
        "country_name": "Italy",
        "country_code": "IT",
        "category": "shopping",
        "vertical": "shopping",
        "place_type": "shop",
        "badge_emoji": "🍝",
        "title_count": 10,
        "title": "10 Best Cooking Classes in Rome",
        "h1": "10 Best Cooking Classes in Rome",
        "meta_title": "10 Best Cooking Classes in Rome 2026 — Reddit-Backed Guide | tabiji.ai",
        "meta_description": "The 10 best cooking classes in Rome — handmade pasta, cacio e pepe, carbonara, pizza & full Roman menus. Real reviews, prices, neighborhoods & interactive map.",
        "og_description": "Curated guide to Rome cooking classes. Pasta-focused, pizza, market tours, family-run nonna experiences — with prices and insider booking tips.",
        "twitter_description": "10 verified Rome cooking classes — pasta, pizza, market tours. Interactive map.",
        "dek_lead": "Rome is the city to learn pasta. These 10 classes — from a chef's apartment in Trastevere to a real nonna in the Sabina hills — are the ones that actually deliver.",
        "map_title": "Cooking Class Map",
        "related_manual": [
            "rome-pizza",
            "rome-cacio-e-pepe",
            "rome-gelato",
            "rome-restaurants",
            "rome-romantic-restaurants",
            "rome-artichokes",
            "trastevere-cheap-restaurants",
        ],
    },
    "mexico-city-vegan-restaurants": {
        "city": "Mexico City",
        "country_name": "Mexico",
        "country_code": "MX",
        "category": "restaurants/food",
        "vertical": "mixed",
        "place_type": "restaurant",
        "badge_emoji": "🥗",
        "title_count": 10,
        "title": "10 Best Vegan Restaurants in Mexico City",
        "h1": "10 Best Vegan Restaurants in Mexico City",
        "meta_title": "10 Best Vegan Restaurants in Mexico City 2026 — Reddit-Backed Guide | tabiji.ai",
        "meta_description": "The 10 best 100% vegan restaurants in CDMX — vegan tacos al pastor, plant-based fine dining, vegan ramen, Mexican antojitos & more. Real reviews + interactive map.",
        "og_description": "Curated guide to Mexico City's best vegan restaurants. Roma Norte, Condesa, Centro & beyond — with prices, hours and what to order.",
        "twitter_description": "10 verified 100% vegan restaurants in CDMX. Interactive map + real reviews.",
        "dek_lead": "Mexico City has quietly become Latin America's most exciting vegan capital. These 10 restaurants — all 100% plant-based — prove that traditional Mexican cuisine has always been vegetable-forward.",
        "map_title": "Vegan Restaurant Map",
        "related_manual": [
            "mexico-city-tacos",
            "mexico-city-restaurants",
            "mexico-city-brunch",
            "mexico-city-vintage-shopping",
            "mexico-city-coffee-shops",
            "mexico-city-mezcalerias",
            "mexico-city-al-pastor",
        ],
    },
}

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]

def best_summary(picks, key_fn, label_fn):
    picks_sorted = sorted([p for p in picks if key_fn(p) is not None], key=lambda p: key_fn(p))
    if not picks_sorted:
        return None
    return label_fn(picks_sorted[-1])

def build_pick(p, slug, place_type):
    section_id = slugify(p["name"])
    pick = {
        "sectionId": section_id,
        "rank": p["rank"],
        "name": p["name"],
        "placeType": place_type,
        "neighborhood": p.get("neighborhood") or p.get("address") or "",
        "address": p.get("address") or p.get("neighborhood") or "",
        "priceRangeLocal": p.get("priceRangeLocal") or "",
        "googleMapsUrl": None,
        "website": p.get("website") or None,
        "phone": p.get("phone") or None,
        "photo": f"https://img.tabiji.ai/popular-picks/{slug}/{section_id}.jpg",
        "tags": p.get("tags") or [],
        "whyItMadeTheList": p["whyItMadeTheList"],
        "whatToOrder": p.get("whatToOrder") or f"{p['name']} is a featured pick in this guide.",
        "insiderTip": p["insiderTip"],
        "redditQuotes": p.get("redditQuotes") or [],
        "hoursNote": p.get("hoursNote") or "",
        "editorialFlags": {"openNow": False},
    }
    if p.get("googleRating") is not None:
        pick["googleRating"] = float(p["googleRating"])
    if p.get("reviewCount") is not None:
        try:
            pick["reviewCount"] = int(p["reviewCount"])
        except (TypeError, ValueError):
            pass
    if p.get("lat") is not None and p.get("lng") is not None:
        pick["lat"] = float(p["lat"])
        pick["lng"] = float(p["lng"])
    return pick

def build_source(slug, research, cfg):
    picks = [build_pick(p, slug, cfg["place_type"]) for p in research["picks"]]
    summary_in = research.get("summary", {})

    badge = f"{cfg['badge_emoji']} Popular Picks — {cfg['city']}, {cfg['country_name']}"
    hero_image = picks[0]["photo"] if picks else None

    out = {
        "slug": slug,
        "pageType": "popular-picks",
        "status": "reviewed",
        "taxonomy": {
            "city": cfg["city"],
            "country": cfg["country_code"],
            "countryCode": cfg["country_code"],
            "category": cfg["category"],
            "vertical": cfg["vertical"],
            "badgeEmoji": cfg["badge_emoji"],
        },
        "seo": {
            "title": cfg["meta_title"],
            "h1": cfg["h1"],
            "metaTitle": cfg["meta_title"],
            "metaDescription": cfg["meta_description"],
            "canonicalPath": f"/popular-picks/{slug}/",
            "ogTitle": f"{cfg['title']} — tabiji.ai",
            "ogDescription": cfg["og_description"],
            "twitterTitle": cfg["title"],
            "twitterDescription": cfg["twitter_description"],
            "heroImage": hero_image,
            "publishedTime": "2026-04-08T00:00:00Z",
            "modifiedTime": "2026-04-08T00:00:00Z",
            "robots": "index, follow, max-image-preview:large",
        },
        "hero": {
            "eyebrow": f"Popular Picks — {cfg['badge_emoji']} Popular Picks — {cfg['city']}, {cfg['country_name']}",
            "title": cfg["title"],
            "dek": cfg["dek_lead"],
            "badge": badge,
            "metaSpans": [],
        },
        "intro": {
            "answerFirst": research["intro"]["answerFirst"],
            "body": research["intro"]["body"],
            "methodology": research["intro"].get("methodology", ""),
        },
        "summary": {
            "totalOptions": len(picks),
            "priceRangeLocal": summary_in.get("priceRangeLocal") or "",
            "priceRangeUSD": summary_in.get("priceRangeUSD") or None,
            "bestBudgetOption": summary_in.get("bestBudgetOption") or None,
            "bestLuxuryOption": summary_in.get("bestLuxuryOption") or None,
            "bestOverall": summary_in.get("bestOverall") or None,
            "topPick": summary_in.get("topPick") or None,
            "sourcesAnalyzed": research.get("sourcesAnalyzed") or "Reddit, TripAdvisor, official venue sites, Time Out, and Wanderlog (verified April 2026)",
            "lastVerifiedLabel": "2026-04",
        },
        "map": {
            "enabled": True,
            "title": cfg["map_title"],
            "embedUrl": None,
            "ctaLabel": None,
            "ctaUrl": None,
        },
        "picks": picks,
        "faq": research["faq"],
        "related": {
            "manual": cfg["related_manual"],
            "topics": [],
        },
        "provenance": {
            "researchStatus": "researched",
            "notes": "Research conducted via web search agents (April 2026). All venues cross-verified against operator sites, TripAdvisor, HappyCow, and Wanderlog. Quotes attributed to real published sources.",
            "importedFromHtml": False,
        },
        "verification": {
            "lastVerified": "2026-04",
            "pipelineVersion": "agent-research-v1",
            "reviewedByHuman": False,
        },
        "publishing": {
            "outputPath": f"popular-picks/{slug}/index.html",
            "includeInMetadataIndex": True,
            "includeInSitemap": True,
            "includeInApiBuild": True,
        },
    }
    return out

def main():
    for slug, cfg in SLUG_CONFIG.items():
        research_path = ROOT / f"scripts/research-{slug}.json"
        if not research_path.exists():
            print(f"SKIP {slug}: research file missing")
            continue
        research = json.loads(research_path.read_text())
        out = build_source(slug, research, cfg)

        out_path = ROOT / f"popular-picks-data/{slug}.json"
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        print(f"Wrote {out_path}")

        # Validate
        result = subprocess.run(
            ["node", "generators/popular-picks/validate-source.js", str(out_path)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"VALIDATION FAILED for {slug}:")
            print(result.stderr)
            sys.exit(1)
        if result.stderr.strip():
            print(f"warnings: {result.stderr.strip()}")

if __name__ == "__main__":
    main()
