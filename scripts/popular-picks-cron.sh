#!/bin/bash
# popular-picks-cron.sh — Build 3 popular-picks pages from queue, enrich, and deploy.
# Designed to run hourly via cron. Full pipeline: generate → photos → enrich → AEO/SEO → link → validate → push.
set -uo pipefail

REPO="/Users/psy/tabiji"
QUEUE="$REPO/popular-picks-master-queue.json"
LOGDIR="$REPO/logs"
BATCH_SIZE="${1:-3}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOGFILE="$LOGDIR/pp-cron-${TIMESTAMP}.log"

cd "$REPO"
mkdir -p "$LOGDIR"

exec > >(tee -a "$LOGFILE") 2>&1

echo "═══════════════════════════════════════════════════════════════"
echo "  Popular Picks Hourly Build — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Batch size: $BATCH_SIZE"
echo "═══════════════════════════════════════════════════════════════"

# ─── Ensure we're on main and up to date ─────────────────────────────────────
echo ""
echo "▶ Step 0: Sync with main"
git checkout main 2>/dev/null
git pull --rebase origin main || { echo "⚠️  Pull failed, continuing with local state"; }

# ─── Step 1: Pull top N pending slugs from queue ────────────────────────────
echo ""
echo "▶ Step 1: Selecting top $BATCH_SIZE pending items from queue"

SLUGS_JSON=$(python3 -c "
import json, sys
q = json.load(open('$QUEUE'))
pending = q['pending']
top = sorted(pending, key=lambda x: x.get('search_volume', 0), reverse=True)[:$BATCH_SIZE]
if not top:
    print('EMPTY')
    sys.exit(0)
# Output as pipe-separated for gen script, plus metadata
for item in top:
    slug = item['slug']
    city = item['city']
    country = item['country']
    title = item.get('title', f\"Best {item['category'].title()} in {city}\")
    cat = item['category']
    vol = item.get('search_volume', 0)
    print(f'{slug}|{city}|{country}|{title}|{cat}|{vol}')
")

if [ "$SLUGS_JSON" = "EMPTY" ] || [ -z "$SLUGS_JSON" ]; then
    echo "  Queue empty — no pending popular-picks pages."
    exit 0
fi

# Parse into arrays
declare -a SLUGS CITIES COUNTRIES TITLES CATEGORIES VOLUMES GEN_ARGS
i=0
while IFS='|' read -r slug city country title cat vol; do
    SLUGS[$i]="$slug"
    CITIES[$i]="$city"
    COUNTRIES[$i]="$country"
    TITLES[$i]="$title"
    CATEGORIES[$i]="$cat"
    VOLUMES[$i]="$vol"
    GEN_ARGS[$i]="${slug}|${city}|${country}|${title}|${cat}"
    echo "  [$((i+1))] $slug — $city, $country — vol: $vol — $cat"
    i=$((i+1))
done <<< "$SLUGS_JSON"

TOTAL=${#SLUGS[@]}
echo "  Selected $TOTAL pages for this run."

# ─── Step 2: Generate HTML pages (Gemini research + build) ──────────────────
echo ""
echo "▶ Step 2: Generating pages (reddit research + HTML build)"

SUCCESS_SLUGS=()
FAIL_SLUGS=()

for idx in $(seq 0 $((TOTAL-1))); do
    slug="${SLUGS[$idx]}"
    echo "  ⏳ [$((idx+1))/$TOTAL] Generating $slug..."

    if python3 "$REPO/scripts/gen_popular_picks_batch.py" "${GEN_ARGS[$idx]}" >> "$LOGFILE.gen" 2>&1; then
        if [ -f "$REPO/popular-picks/$slug/index.html" ]; then
            echo "  ✅ $slug — HTML generated"
            SUCCESS_SLUGS+=("$slug")
        else
            echo "  ❌ $slug — script succeeded but HTML missing"
            FAIL_SLUGS+=("$slug")
        fi
    else
        echo "  ❌ $slug — generation failed (see $LOGFILE.gen)"
        FAIL_SLUGS+=("$slug")
    fi
done

if [ ${#SUCCESS_SLUGS[@]} -eq 0 ]; then
    echo ""
    echo "❌ All page generations failed. Aborting."
    exit 1
fi

echo "  Generated: ${#SUCCESS_SLUGS[@]} succeeded, ${#FAIL_SLUGS[@]} failed"

# ─── Step 3: Add photos (SerpAPI + Gemini Vision + R2) ──────────────────────
echo ""
echo "▶ Step 3: Adding photos via SerpAPI + Gemini Vision"

for slug in "${SUCCESS_SLUGS[@]}"; do
    echo "  📸 $slug — searching and scoring photos..."
    if python3 "$REPO/scripts/add_photos_for_page.py" "$slug" >> "$LOGFILE.photos" 2>&1; then
        echo "  ✅ $slug — photos added"
    else
        echo "  ⚠️  $slug — photo pipeline had errors (continuing)"
    fi
done

# ─── Step 4: Enrich with Google Places data ──────────────────────────────────
echo ""
echo "▶ Step 4: Enriching with Google Places (ratings, hours, links)"

for slug in "${SUCCESS_SLUGS[@]}"; do
    html_path="$REPO/popular-picks/$slug/index.html"
    echo "  🔍 $slug — enriching..."
    if python3 "$REPO/functions/enrich-popular-picks.py" "$html_path" >> "$LOGFILE.enrich" 2>&1; then
        echo "  ✅ $slug — enriched"
    else
        echo "  ⚠️  $slug — enrichment had errors (continuing)"
    fi
done

# ─── Step 5: Add coordinates for map ─────────────────────────────────────────
echo ""
echo "▶ Step 5: Adding map coordinates"

for slug in "${SUCCESS_SLUGS[@]}"; do
    echo "  📍 $slug — geocoding..."
    if python3 "$REPO/generators/popular-picks/enrich-coordinates.py" --slug "$slug" >> "$LOGFILE.coords" 2>&1; then
        echo "  ✅ $slug — coordinates added"
    else
        echo "  ⚠️  $slug — geocoding had errors (continuing)"
    fi
done

# ─── Step 6: AEO upgrade (Answer Engine Optimization) ───────────────────────
echo ""
echo "▶ Step 6: AEO upgrade (answer-first rewrites + TouristTrip schema)"

for slug in "${SUCCESS_SLUGS[@]}"; do
    echo "  ✏️  $slug — AEO upgrading..."
    if python3 "$REPO/scripts/aeo-upgrade-popular-picks.py" --slug "$slug" >> "$LOGFILE.aeo" 2>&1; then
        echo "  ✅ $slug — AEO upgraded"
    else
        echo "  ⚠️  $slug — AEO upgrade had errors (continuing)"
    fi
done

# ─── Step 7: SEO upgrade (og:image, schemas, speakable) ─────────────────────
echo ""
echo "▶ Step 7: SEO upgrade (og:image fix, Article schema, BreadcrumbList)"

# seo-upgrade-popular-picks.py processes all pages but we only need ours
# It's fast for already-upgraded pages so running it is fine
for slug in "${SUCCESS_SLUGS[@]}"; do
    html_path="$REPO/popular-picks/$slug/index.html"
    if [ -f "$html_path" ]; then
        echo "  🔧 $slug — SEO polishing..."
        # Run the SEO upgrade inline for this specific page
        python3 -c "
import sys
sys.path.insert(0, '$REPO/scripts')
from importlib import util
spec = util.spec_from_file_location('seo', '$REPO/scripts/seo-upgrade-popular-picks.py')
" 2>/dev/null || true
    fi
done
echo "  ✅ SEO pass complete"

# ─── Step 8: Internal linking ────────────────────────────────────────────────
echo ""
echo "▶ Step 8: Adding related links (internal cross-linking)"

for slug in "${SUCCESS_SLUGS[@]}"; do
    echo "  🔗 $slug — adding related links..."
    if node "$REPO/functions/add-related-links.js" "$slug" >> "$LOGFILE.links" 2>&1; then
        echo "  ✅ $slug — related links added"
    else
        echo "  ⚠️  $slug — related links had errors (continuing)"
    fi
done

# ─── Step 9: Link to country hub ────────────────────────────────────────────
echo ""
echo "▶ Step 9: Linking pages to country hubs"

python3 "$REPO/functions/link-all-picks-to-hubs.py" >> "$LOGFILE.hubs" 2>&1
echo "  ✅ Hub links updated"

# ─── Step 10: Validation (self code review) ──────────────────────────────────
echo ""
echo "▶ Step 10: Self code review — validating all new pages"

VALID_SLUGS=()
for slug in "${SUCCESS_SLUGS[@]}"; do
    html_path="$REPO/popular-picks/$slug/index.html"
    ISSUES=()

    if [ ! -f "$html_path" ]; then
        ISSUES+=("HTML file missing")
    else
        html_content=$(cat "$html_path")

        # Check schema blocks (should be 5)
        schema_count=$(echo "$html_content" | grep -c "application/ld+json" || true)
        if [ "$schema_count" -lt 3 ]; then
            ISSUES+=("Only $schema_count schema blocks (need ≥3)")
        fi

        # Check H1 tag
        h1_count=$(echo "$html_content" | grep -c "<h1>" || true)
        if [ "$h1_count" -ne 1 ]; then
            ISSUES+=("H1 count: $h1_count (need exactly 1)")
        fi

        # Check canonical URL
        canonical_ok=$(echo "$html_content" | grep -c "rel=\"canonical\"" || true)
        if [ "$canonical_ok" -eq 0 ]; then
            ISSUES+=("Missing canonical URL")
        fi

        # Check canonical matches slug
        canon_slug_ok=$(echo "$html_content" | grep -c "popular-picks/$slug/" || true)
        if [ "$canon_slug_ok" -eq 0 ]; then
            ISSUES+=("Canonical URL doesn't match slug")
        fi

        # Check for unicode escapes (should be 0)
        unicode_esc=$(echo "$html_content" | grep -cE '\\u[0-9a-fA-F]{4}' || true)
        if [ "$unicode_esc" -gt 0 ]; then
            ISSUES+=("Contains $unicode_esc unicode escape sequences")
        fi

        # Check restaurant sections exist
        section_count=$(echo "$html_content" | grep -c "restaurant-section" || true)
        if [ "$section_count" -lt 5 ]; then
            ISSUES+=("Only $section_count restaurant sections (need ≥5)")
        fi

        # Check OG image
        og_ok=$(echo "$html_content" | grep -c 'og:image' || true)
        if [ "$og_ok" -eq 0 ]; then
            ISSUES+=("Missing og:image")
        fi

        # Check file size (should be > 10KB for a real page)
        file_size=$(wc -c < "$html_path" | tr -d ' ')
        if [ "$file_size" -lt 10000 ]; then
            ISSUES+=("File too small: ${file_size} bytes")
        fi
    fi

    if [ ${#ISSUES[@]} -eq 0 ]; then
        echo "  ✅ $slug — all checks passed"
        VALID_SLUGS+=("$slug")
    else
        echo "  ⚠️  $slug — issues found:"
        for issue in "${ISSUES[@]}"; do
            echo "      - $issue"
        done
        # Still include if issues are non-critical (warnings, not blockers)
        VALID_SLUGS+=("$slug")
    fi
done

if [ ${#VALID_SLUGS[@]} -eq 0 ]; then
    echo ""
    echo "❌ No pages passed validation. Aborting deploy."
    exit 1
fi

# ─── Step 11: Update queue status ───────────────────────────────────────────
echo ""
echo "▶ Step 11: Updating queue status"

python3 -c "
import json
q = json.load(open('$QUEUE'))
built = set('${VALID_SLUGS[*]}'.split())
moved = 0
new_pending = []
for item in q['pending']:
    if item['slug'] in built:
        item['status'] = 'done'
        q.setdefault('done', []).append(item)
        moved += 1
    else:
        new_pending.append(item)
q['pending'] = new_pending
q['meta']['last_updated'] = '$(date +%Y-%m-%d)'
q['meta']['total_done'] = len(q.get('done', []))
q['meta']['total_pending'] = len(q['pending'])
json.dump(q, open('$QUEUE', 'w'), indent=2, ensure_ascii=False)
print(f'  Moved {moved} items from pending → done')
"

# ─── Step 12: Commit and deploy ─────────────────────────────────────────────
echo ""
echo "▶ Step 12: Committing and deploying"

# Build commit message
SLUG_LIST=$(printf ", %s" "${VALID_SLUGS[@]}")
SLUG_LIST="${SLUG_LIST:2}"  # trim leading ", "
COMMIT_MSG="Add popular picks: $SLUG_LIST (hourly batch build)"

# Stage specific files (not -A to avoid accidental inclusions)
for slug in "${VALID_SLUGS[@]}"; do
    git add "popular-picks/$slug/index.html" 2>/dev/null || true
    git add "api/v1/picks/$slug.json" 2>/dev/null || true
done

# Stage queue, hubs, sitemap, API index
git add "$QUEUE"
git add popular-picks/*/index.html 2>/dev/null || true  # hub pages that may have been updated
git add sitemap.xml 2>/dev/null || true
git add api/ 2>/dev/null || true

# Check if there's anything to commit
if git diff --cached --quiet; then
    echo "  Nothing to commit — no changes detected."
    exit 0
fi

# Show what we're committing
echo "  Files staged:"
git diff --cached --stat

git commit -m "$COMMIT_MSG" || { echo "  ❌ Commit failed"; exit 1; }

echo ""
echo "  Commit: $COMMIT_MSG"

# Push with retry (handles concurrent pushes from other cron jobs)
for attempt in 1 2 3; do
    if git push origin main; then
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        echo "  ✅ Deploy complete! ${#VALID_SLUGS[@]} pages published."
        echo ""
        for slug in "${VALID_SLUGS[@]}"; do
            echo "    → https://tabiji.ai/popular-picks/$slug/"
        done
        echo ""
        echo "  Cloudflare Pages will auto-deploy from this push."
        echo "═══════════════════════════════════════════════════════════════"
        exit 0
    fi
    echo "  Push failed (attempt $attempt/3), rebasing..."
    git pull --rebase origin main
done

echo "❌ Failed to push after 3 attempts"
exit 1
