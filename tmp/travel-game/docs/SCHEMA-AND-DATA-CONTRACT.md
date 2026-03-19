# Tabiji Quest — Schema and Data Contract

This document defines the minimum contract for turning the travel-game prototype into a structured product slice.

The core rule:

**Chat is presentation. Structured state is the product.**

The UI, content packs, and any future LLM layer should all sit on top of the same canonical game/session model.

---

## 1. Design goals

The schema should make it easy to:
- author scenarios without hardcoding them into UI logic
- keep canonical state deterministic
- let a guide speak naturally without inventing state
- generate a clean itinerary handoff payload into Tabiji
- support both scripted branching and future hybrid AI turns

For V1, prioritize:
- explicit turn graph
- readable JSON
- deterministic stat changes
- strong handoff fields

---

## 2. Canonical entities

### 2.1 Scenario
Represents one playable game pack.

```ts
export type Scenario = {
  id: string;
  slug: string;
  title: string;
  region: string;
  version: number;
  tripLengthDays: number;
  budgetStart: number;
  energyStart: number;
  fitStart: number;
  summary: string;
  guide: GuidePersona;
  startState: ScenarioStartState;
  destinationCardIds: string[];
  turnOrder: string[];
};
```

### 2.2 Guide persona
Defines voice and behavior constraints.

```ts
export type GuidePersona = {
  id: string;
  name: string;
  role: string;
  voice: string[];
  systemStyle: string;
};
```

### 2.3 Session state
This is the canonical runtime state for one playthrough.

```ts
export type SessionState = {
  scenarioId: string;
  currentTurnId: string;
  stats: GameStats;
  route: string[];
  flags: string[];
  discoveredPreferences: string[];
  decisions: Record<string, string>;
  eventHistory: string[];
  completed: boolean;
  endingId?: string;
};
```

### 2.4 Game stats
Keep the stat model deliberately small.

```ts
export type GameStats = {
  budget: number;          // 0-100 normalized pool
  daysRemaining: number;   // integer
  energy: number;          // 0-100
  satisfaction: number;    // 0-100
  styleFit: number;        // 0-100
};
```

### 2.5 Destination card
A lightweight info object for UI rendering and recommendation flavor.

```ts
export type DestinationCard = {
  id: string;
  title: string;
  bestFor: string[];
  tradeoff: string;
  greatPairings: string[];
};
```

### 2.6 Turn
One authored game node.

```ts
export type Turn = {
  id: string;
  phase: 'discovery' | 'routing' | 'logistics' | 'taste' | 'event' | 'resolution' | 'ending';
  guideMessage: string;
  eventBanner?: string;
  destinationCards?: string[];
  choices: Choice[];
  endingVariants?: EndingVariant[];
  defaultEnding?: DefaultEnding;
  handoff?: HandoffConfig;
};
```

### 2.7 Choice
A choice mutates canonical state and sends the session to another node.

```ts
export type Choice = {
  id: string;
  label: string;
  playerReply: string;
  effects: Partial<GameStats>;
  discover?: string[];
  setFlags?: string[];
  appendRoute?: string[];
  setRoute?: string[];
  eventBanner?: string;
  nextTurnId: string;
};
```

### 2.8 Ending variant
An ending is selected from state, not improvised by the UI.

```ts
export type EndingVariant = {
  id: string;
  when: EndingPredicate;
  travelerType: string;
  summary: string;
  biggestWin: string;
  cta: string;
};

export type EndingPredicate = {
  allFlags?: string[];
  anyFlags?: string[];
  minStyleFit?: number;
  maxStyleFit?: number;
  minEnergy?: number;
  maxEnergy?: number;
  minBudget?: number;
  maxBudget?: number;
};
```

### 2.9 Itinerary handoff payload
This is the contract between game output and real product value.

```ts
export type ItineraryHandoffPayload = {
  source: 'tabiji-quest';
  scenarioId: string;
  scenarioTitle: string;
  route: string[];
  tripLengthDays: number;
  stats: GameStats;
  flags: string[];
  discoveredPreferences: string[];
  travelerType: string;
  summary: string;
  ctaLabel: string;
  guideId: string;
  guideName: string;
  contentVersion: number;
};
```

---

## 3. Contract rules

### 3.1 Canonical state rules
- UI never invents state transitions.
- State changes only through structured `Choice.effects`, route ops, and flag ops.
- If an LLM is used later, it should receive state but not directly mutate it.

### 3.2 Routing rules
- `setRoute` replaces the current route.
- `appendRoute` adds route nodes only if absent unless duplicates are explicitly allowed.
- Destination names shown in UI should map cleanly to internal IDs if production data expands later.

### 3.3 Stat rules
Recommended clamps:
- `budget`: 0–100
- `energy`: 0–100
- `satisfaction`: 0–100
- `styleFit`: 0–100
- `daysRemaining`: integer floor at 0

### 3.4 Choice design rules
Each turn should usually offer:
- 2 to 4 choices
- at least one “tasteful / lower-chaos” option
- at least one “tempting but costly” option when relevant

Choices should not be fake branches. If outcomes converge, the stat and flag differences still need to matter.

### 3.5 Ending rules
- Endings should be selected by predicates against canonical state.
- There should always be a default fallback ending.
- Endings should summarize what kind of traveler the player turned out to be.

---

## 4. File structure recommendation

For the `tmp/travel-game/` slice:

```text
/tmp/travel-game/
  index.html
  app.js                # later split from inline JS
  styles.css            # later split from inline CSS
  content/
    japan-first-timer.json
  docs/
    SCHEMA-AND-DATA-CONTRACT.md
    IMPLEMENTATION-PLAN.md
```

If the concept graduates from `tmp/` to product surface:

```text
/travel-game/
  index.html or route entry
  content/
  components/
  lib/
    game-engine.ts
    handoff.ts
    scenario-loader.ts
```

---

## 5. Runtime turn pipeline

### V1 scripted pipeline
1. Load scenario pack
2. Initialize session state from `startState`
3. Render current turn
4. Player selects choice
5. Apply deterministic updates
6. Persist session state
7. Render next turn or compute ending
8. Build itinerary handoff payload

### Future hybrid AI pipeline
1. Deterministic engine computes valid recommendations and current state
2. LLM receives:
   - guide persona
   - session state
   - current turn metadata
   - valid choices
   - destination cards
3. LLM returns only presentation text:
   - rewritten guide message
   - optional rationale
   - optional flavor copy
4. Engine still controls state mutation and branching

That separation matters. Without it, the experience turns into a mushy chatbot.

---

## 6. Authoring guidelines

Scenario writers should aim for:
- short guide messages
- clear tradeoffs
- real travel logic
- visible consequences
- strong opinion where useful

Avoid:
- generic “it depends” travel advice
- bloated exposition
- random punishment events
- fake luxury writing with no actual recommendation content

A good turn usually does one of three things:
- discover preference
- force tradeoff
- reward coherence

---

## 7. Example handoff payload

```json
{
  "source": "tabiji-quest",
  "scenarioId": "japan-first-timer",
  "scenarioTitle": "First Time in Japan, No Regrets",
  "route": ["Tokyo", "Kyoto", "Nara"],
  "tripLengthDays": 8,
  "stats": {
    "budget": 63,
    "daysRemaining": 6,
    "energy": 82,
    "satisfaction": 38,
    "styleFit": 87
  },
  "flags": [
    "route-clean",
    "smart-hotel-choice",
    "splurge-meal",
    "daytrip-nara",
    "handled-rain-smartly",
    "kyoto-atmospheric-stay",
    "scene-ending"
  ],
  "discoveredPreferences": [
    "food-priority",
    "atmosphere-priority",
    "high-low-food"
  ],
  "travelerType": "A high-taste traveler who likes cities best when they still leave room to breathe.",
  "summary": "You built a coherent first Japan trip with enough atmosphere, enough appetite, and not too much transit stupidity.",
  "ctaLabel": "Turn this run into a real Tabiji itinerary",
  "guideId": "ren",
  "guideName": "Ren",
  "contentVersion": 1
}
```

---

## 8. Immediate recommendation

For the next implementation pass:
- migrate hardcoded prototype turns into `content/japan-first-timer.json`
- keep the engine deterministic
- keep the guide authored first
- make the itinerary handoff payload real enough to plug into Tabiji later

That gives us a prototype with structure instead of vibes.
