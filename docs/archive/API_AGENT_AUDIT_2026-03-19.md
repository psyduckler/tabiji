# Tabiji API audit — discoverability + agent usefulness

Date: 2026-03-19

## Verdict

The API is already close to agent-usable because it has:
- a public docs page
- `openapi.json`
- `llms.txt`
- `.well-known/agents.json`
- predictable static JSON URLs
- no auth friction

But it is **not yet trustworthy enough for agents by default** because the machine-readable surfaces drift from the actual data, and a few generated payloads are lossy or wrong.

## Highest-priority issues

### 1) Public docs and OpenAPI drift from reality

Observed drift:
- `tabiji/api/index.html` still says **345 picks / 324 itineraries / 50 comparisons**
- `tabiji/api/openapi.json` still says **345 picks / 324 itineraries / 50 comparisons**
- `tabiji/llms.txt` still says **345 picks / 324 itineraries**
- actual data in `tabiji/api/v1/index.json` is **389 picks / 344 itineraries / 40 comparisons**

Impact:
- agents and developers will assume stale inventory counts
- trust drops immediately when examples disagree with live endpoints
- tool wrappers built from OpenAPI will inherit bad descriptions/examples

### 2) Destination inventory count is wrong

Observed:
- `tabiji/api/v1/destinations.json` advertises **706** destinations
- actual per-destination files in `tabiji/api/v1/destinations/*.json` = **704**
- builder collision source appears to be duplicate slug generation:
  - `Medellín` vs `Medellin`
  - `Medellin, Colombia` vs `Medellín, Colombia`

Impact:
- agents can list destinations that do not have unique backing detail files
- retrieval pipelines will see silent overwrites

### 3) Comparison docs examples are wrong

In `tabiji/api/index.html` and `tabiji/api/openapi.json`, the comparison examples are internally inconsistent:
- slug shown: `tokyo-vs-kyoto`
- title shown: `Bali vs Thailand: Which Should You Visit?`
- destinations shown: `Bali` and `Thailand`
- URL shown: `/compare/tokyo-vs-kyoto/`

Impact:
- obvious credibility hit
- bad few-shot signal for agent planning and codegen

### 4) Itinerary slugs/details are inconsistent

Observed example:
- file path: `tabiji/api/v1/itineraries/itineraries-5-day-tokyo-food-nightlife.json`
- payload `slug`: `5-day-tokyo-food-nightlife`
- docs/OpenAPI describe slug examples including the `itineraries-` prefix

Also in that same payload:
- `destination` becomes `Tokyo Food` instead of `Tokyo`
- `dayCount` is `8` even though only 5 entries are real trip days; informational sections get counted as days

Impact:
- agents cannot reliably construct or round-trip itinerary IDs
- destination-based filtering becomes noisy
- planners may overcount itinerary length

### 5) Compare payloads are lossy and messy

Example: `tabiji/api/v1/compare/tokyo-vs-kyoto.json`
- reddit quotes are flattened badly: quote + source are jammed together
- summaries are hard-truncated mid-word
- verdict is a blob of concatenated UI text instead of a clean structured verdict
- decision-framework section is emitted as a category with empty summary

Impact:
- poor downstream summarization quality
- harder for agents to cite or reason over comparisons
- increased cleanup burden in every client

### 6) Picks payloads still contain presentation artifacts

Example: `tabiji/api/v1/picks/amsterdam-brunch.json`
- `priceRange` includes leading emoji/text artifact: `💴 €15–€25/person`

Impact:
- weak normalization for filtering/sorting
- downstream UIs and agents need cleanup logic

## Secondary discoverability gaps

### 7) API index is too thin for agent routing

`tabiji/api/v1/index.json` is useful, but it should probably also expose:
- canonical inventory counts derived from current files
- example slugs per collection
- last build time per collection
- schema/version per collection
- optional dataset changelog / freshness notes
- links to `llms.txt` and `agents.json`

### 8) No agent-first query surface

Right now discovery is list-then-filter client-side.
That works, but it is clumsy for agents.

High-value additions:
- `/api/v1/search.json?q=...&type=destination|pick|itinerary|compare`
- `/api/v1/destinations/by-country/{country}.json`
- `/api/v1/destinations/by-continent/{continent}.json`
- `/api/v1/picks/by-city/{city}.json`
- `/api/v1/itineraries/by-destination/{destination}.json`
- `/api/v1/compare/by-destination/{slug}.json`

Even a static precomputed search index would help a lot.

### 9) Missing stronger machine-readable semantics

OpenAPI covers endpoints, but not enough semantics for agents.
Useful additions:
- explicit `x-ai-hints` / `x-agent-notes` per endpoint
- stable enums for `budget`, `continent`, common `vibes`, `tripType`
- structured freshness metadata
- structured citation/source fields where Reddit/blog/forum evidence exists
- normalized IDs distinct from display slugs when collisions exist

### 10) `agents.json` is present but fairly shallow

Good start, but it should be stronger for actual orchestration:
- include precise input schemas or parameter extraction hints
- reference example slugs and endpoint response fields
- include failure modes and fallback steps
- add a skill for destination discovery and one for cross-dataset planning
- ideally point to search/index endpoints once they exist

## Recommended fix order

### Phase 1 — trust repair
1. Regenerate/fix all stale counts and examples in:
   - `api/index.html`
   - `api/openapi.json`
   - `llms.txt`
   - `agents.json` where needed
2. Fix destination slug collisions so collection count matches detail files.
3. Fix itinerary slug consistency.
4. Clean compare extraction so verdicts, quotes, and categories are structured.

### Phase 2 — make it agent-friendly
5. Add a proper search/index endpoint across all content types.
6. Add collection-specific filter/index endpoints.
7. Add normalized enums + stronger schema definitions.
8. Expand `agents.json` and `llms.txt` with concrete task flows and examples.

### Phase 3 — make it excellent
9. Add dataset freshness metadata and changelog/versioning.
10. Add explicit provenance blocks for extracted claims and quotes.
11. Add JSON Schema files per collection alongside OpenAPI.

## Recommended product direction

If the goal is “discoverable and useful for agents,” I’d optimize for this sentence:

> An agent should be able to discover the API, understand the collections, find the right record in one or two calls, and trust that IDs, counts, and examples are accurate.

Right now discoverability is decent, but trust and retrieval ergonomics are the weak points.

## Concrete next build I’d ship

If we want a tight next step, I’d ship this bundle first:
- fix stale docs/OpenAPI/llms examples and counts
- fix destination slug collisions
- fix itinerary slug + `dayCount` extraction
- improve compare JSON structure
- add one cross-collection `search.json`

That would move the API from “interesting static data dump” to “something agents can use confidently.”
