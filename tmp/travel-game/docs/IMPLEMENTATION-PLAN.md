# Tabiji Quest — Implementation Plan

This document covers the engineering and product path for turning the current `tmp/travel-game/` prototype into a cleaner, more reviewable product slice.

The current prototype proved the concept. The next step is to stop hardcoding everything in one HTML file and split it into a minimal but sane structure.

---

## 1. Scope of this implementation pass

This pass should deliver three things:
1. a real scenario content pack
2. a real schema/data contract
3. a cleaner implementation path for the prototype

It does **not** need to deliver:
- full production integration
- booking or pricing
- multi-scenario support
- open-ended AI conversation

---

## 2. Current state

The current prototype in `tmp/travel-game/index.html` is useful, but limited:
- content is hardcoded inline
- state logic is embedded in page JS
- summary/handoff is mostly illustrative
- there is no reusable scenario pack format yet

That was correct for the first PR. It is not the right shape for iteration.

---

## 3. Target state after this pass

After the next implementation pass, the `tmp/travel-game/` slice should look like this:

```text
/tmp/travel-game/
  index.html
  app.js
  styles.css
  content/
    japan-first-timer.json
  docs/
    SCHEMA-AND-DATA-CONTRACT.md
    IMPLEMENTATION-PLAN.md
```

And the runtime behavior should be:
- load JSON scenario data
- initialize game state
- render current turn
- apply deterministic choice effects
- compute ending
- generate itinerary handoff payload

---

## 4. Implementation phases

## Phase 1 — Refactor prototype into structured files

### Goal
Keep behavior mostly the same while improving maintainability.

### Tasks
- split inline CSS into `styles.css`
- split inline JS into `app.js`
- move scenario content into `content/japan-first-timer.json`
- build a small scenario loader
- build a deterministic choice application function

### Deliverable
A functionally similar prototype, but content-driven instead of hardcoded.

### Why this matters
Without this step, every content change becomes UI surgery.

---

## Phase 2 — Implement a tiny game engine

### Goal
Separate presentation from canonical state updates.

### Needed functions
```ts
loadScenario(id)
initSession(scenario)
renderTurn(turn, state)
applyChoice(state, choice)
resolveEnding(state, endingVariants, defaultEnding)
buildHandoffPayload(state, scenario, ending)
```

### Engine rules
- clamp stats after each choice
- append route entries safely
- dedupe flags and preferences
- persist decision history
- do not let UI mutate state directly

### Deliverable
A small engine file or section inside `app.js` with explicit state transitions.

---

## Phase 3 — Improve the summary and handoff

### Goal
Make the end of the run feel product-real instead of concept-only.

### Tasks
- display ending variant chosen
- show route, traveler type, key tradeoffs, and biggest win
- surface inferred preferences cleanly
- display the exact handoff payload or a humanized summary of it
- include a realistic CTA to continue planning in Tabiji

### Deliverable
A summary screen that feels like the bridge into an actual itinerary product.

---

## Phase 4 — Add light instrumentation

### Goal
Make the prototype testable with real behavior data.

### Minimum events
- `travel_game_viewed`
- `travel_game_started`
- `travel_game_choice_selected`
- `travel_game_completed`
- `travel_game_itinerary_cta_clicked`

### Event payload suggestions
- scenario id
- turn id
- choice id
- route length
- current stats snapshot

### Deliverable
If analytics hooks already exist in Tabiji, wire into them. If not, at least stub the event shape in code comments or a tiny logging utility.

---

## 5. Recommended file responsibilities

### `index.html`
Responsibilities:
- shell layout
- semantic containers
- load `styles.css` and `app.js`
- minimal bootstrapping markup

### `styles.css`
Responsibilities:
- visual system
- layout
- card and chat styling
- mobile behavior

### `app.js`
Responsibilities:
- load scenario content
- initialize state
- render turns
- handle choice clicks
- compute ending
- build handoff payload

### `content/japan-first-timer.json`
Responsibilities:
- all authored scenario content
- destination cards
- turn graph
- ending variants

### `docs/*`
Responsibilities:
- schema explanation
- implementation intent
- future developer handoff

---

## 6. Engineering constraints

### Constraint 1: keep it static-friendly
The current deployment path is simple static hosting. Avoid requiring a backend just to prove the game loop.

### Constraint 2: do not add uncontrolled AI yet
If freeform AI is added too early, the product gets less consistent and harder to review.

### Constraint 3: keep the page lightweight
This is still a `tmp/` review surface. It should load fast and work as a standalone static page.

### Constraint 4: optimize for iteration speed
Content writers should be able to update scenario JSON without reworking rendering logic.

---

## 7. Suggested implementation order

### Step 1
Move all styling into `styles.css`.

### Step 2
Move current JS into `app.js` and isolate state helpers.

### Step 3
Replace hardcoded turns with JSON-loaded scenario content.

### Step 4
Render destination cards from scenario data.

### Step 5
Implement ending resolution from predicates.

### Step 6
Build the itinerary handoff payload object.

### Step 7
Add analytics hooks or event stubs.

That order gives useful progress early without getting lost in polish.

---

## 8. QA checklist

Before opening the next prototype PR, verify:
- page loads with no console errors
- scenario JSON parses cleanly
- every choice leads to a valid next turn
- stats clamp correctly
- route updates correctly
- ending always resolves
- summary screen shows coherent output
- handoff payload contains route + preferences + stats
- mobile layout is still usable

---

## 9. What should happen after this pass

If this pass lands cleanly, the next step should be one of these:

### Option A — Better prototype quality
- stronger visual polish
- richer cards
- shareable result card
- better copy pass

### Option B — Productization
- create a real route instead of `tmp/`
- connect handoff to itinerary generation
- add saved sessions
- add more scenarios

### Option C — Hybrid AI layer
- keep deterministic content graph
- let an LLM rewrite guide copy or answer limited follow-up questions
- maintain strict state control in the engine

My recommendation:
**Do A first, then B. Delay C until the structured product loop feels good.**

---

## 10. Immediate recommendation

The cleanest next PR after this docs/content pass is:
- refactor `tmp/travel-game/index.html` into `index.html + app.js + styles.css`
- wire it to `content/japan-first-timer.json`
- keep the same visible product shape
- improve the final handoff screen

That would be the first version that feels like a real build, not a concept artifact.
