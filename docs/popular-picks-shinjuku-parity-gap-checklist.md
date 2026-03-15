# Shinjuku Parity Gap Checklist

_Last updated: 2026-03-15_

This is the concrete gap list between:

- the live page: `popular-picks/shinjuku-cheap-restaurants/index.html`
- the current generated output from: `popular-picks-data/shinjuku-cheap-restaurants.json`

The point is to separate **must-match parity work** from **nice-to-have polish** so the renderer can move from scaffold to real production confidence.

## Current state

The renderer is now materially closer to the live page:

- hero shell exists
- map block exists on desktop + mobile
- richer pick rendering exists
- hours UI exists
- website / phone / Google Maps utilities exist
- FAQ + schema + related links render correctly

But it is still not full parity.

Rough output size comparison:

- live page: ~104 KB
- current generated page: ~81 KB

That remaining gap mostly comes from page-specific shell details, richer per-pick markup, and live-page interaction behavior.

## Must-match gaps

These are the gaps that matter for real takeover.

### 1. Replace generic pick-card shell with live-style restaurant sections

**Live page uses:**
- `.restaurant-section`
- `.restaurant-header`
- `.restaurant-number`
- `.cuisine-tag`
- `.google-rating`
- `.restaurant-details`
- `.shop-contact`
- `.tabiji-verdict`

**Current generator uses:**
- `.pick-card`
- `.pick-header`
- `.pick-meta`
- `.pick-links`
- generic `.tag`

**Why it matters:**
This is the main markup contract for the page. The current renderer is structurally fine, but it is still visibly “generator-ish” instead of matching the established Popular Picks format.

**Action:**
Refactor generated pick markup to align with the live section structure and class naming.

---

### 2. Restore open/closed status in hours summary

**Live page behavior:**
- hours are shown inside `<details>`
- summary includes current state like `🕐 Closed now` or open status

**Current generator behavior:**
- hours render in a `<details>` block
- summary is generic: `Hours`

**Why it matters:**
The live page is more useful and more product-like. The source already contains `editorialFlags.openNow` on many picks.

**Action:**
Derive summary label from `editorialFlags.openNow`:
- `🕐 Open now`
- `🕐 Closed now`
- fallback `Hours`

---

### 3. Promote phone / website links into live-style contact row

**Live page behavior:**
- utility links appear in a dedicated `.shop-contact` row
- Website and phone are visually separated from the basic detail row

**Current generator behavior:**
- utility links render, but inside generic `.pick-links`

**Why it matters:**
The live page has a cleaner information hierarchy.

**Action:**
Rename and restyle utility row to match `.shop-contact` behavior.

---

### 4. Match the live “What to order” copy pattern

**Live page behavior:**
- `What to order` blocks are formulaic and answer-first
- many include a self-contained leading sentence naming the place, type, and location

**Current generator behavior:**
- uses source `whatToOrder` directly in a styled box

**Why it matters:**
The current source data is not always normalized to the live page’s compiled wording style.

**Action:**
Choose one of these:

1. normalize `whatToOrder` in source data, or
2. add a renderer transform that composes:
   - place name
   - cuisine tag / type
   - location
   - item recommendation

My bias: prefer source normalization for long-term cleanliness.

---

### 5. Restore live-style verdict block semantics

**Live page behavior:**
- uses `.tabiji-verdict`
- verdict reads like the page’s editorial conclusion

**Current generator behavior:**
- uses insider tip as verdict content

**Why it matters:**
`insiderTip` and `verdict` are related, but not always the same thing.

**Action:**
Add a dedicated source field for final editorial verdict, or explicitly declare that `insiderTip` is the verdict field for v1 and normalize the wording.

---

### 6. Tighten FAQ parity

**Live page:** 6 FAQ entries in schema
**Current source:** 7 FAQ entries

**Why it matters:**
This is not necessarily bad, but parity means deciding whether we are:
- reproducing the live page, or
- intentionally improving it

**Action:**
Make the choice explicit.

Recommended stance:
- allow deliberate improvement,
- but keep a parity note documenting any intentional mismatch.

---

### 7. Make map behavior explicit instead of half-derived

**Current generator behavior:**
- map is now derived from taxonomy into a Google Maps embed/search URL
- this is useful, but still generic

**Live page behavior:**
- page-specific map experience
- desktop sidebar + mobile inline map placement
- custom map presentation around actual picks

**Why it matters:**
The derived map gets us functional parity-lite, but not true feature parity.

**Action:**
Add explicit map configuration support for Popular Picks pages, ideally:

```json
"map": {
  "enabled": true,
  "title": "Shinjuku cheap eats map",
  "embedUrl": "...",
  "ctaLabel": "Open in Google Maps",
  "ctaUrl": "...",
  "mode": "embed",
  "markersFromPicks": true
}
```

Longer term, if needed:
- explicit marker payloads
- pick-to-marker sync
- custom JS map bootstrapping

---

### 8. Bring nav/footer shell closer to live Popular Picks pages

**Current generator shell:**
- decent, but simplified

**Live page shell:**
- more complete nav/dropdown behavior and spacing
- matches site-wide page expectations better

**Why it matters:**
For takeover, the generated page should feel native to the site, not like a side project.

**Action:**
Either:
- import/reuse the established nav shell for this page type, or
- make the generator emit the same shell markup/classes the live page expects.

## Nice-to-have gaps

These matter less for proving takeover.

### 9. Cuisine-specific color tag classes
Live page uses classes like:
- `.tag-ramen`
- `.tag-tonkatsu`
- `.tag-yakitori`

Current generator uses a generic `.tag`.

**Nice to have**, not blocker.

---

### 10. Exact hero microstyling parity
Current hero is close enough structurally, but not exact.

Not blocker for first production proof.

---

### 11. Exact live map implementation
The current embedded map is acceptable for proving the system.
Custom marker JS can come after core parity is locked.

---

### 12. Exact per-pick alt text parity
Current image alt text is serviceable, but the live page sometimes uses more specific image descriptions.

Nice to improve later.

## Source-data cleanup needs

These are not renderer bugs. They are source normalization tasks.

### A. `whatToOrder` fields are inconsistent
Some feel like clean structured recommendation copy.
Others still feel inherited from legacy page prose.

### B. `insiderTip` is doing double duty
It is currently functioning as:
- tip
- verdict
- editorial conclusion

That should be separated or normalized.

### C. related links are too thin
Current `related.manual` count is low for a mature page.
Not a blocker, but weak for production polish.

## Recommended next implementation order

### Step 1
Refactor the renderer to emit live-style section class names and hierarchy:
- `.restaurant-section`
- `.restaurant-header`
- `.restaurant-details`
- `.shop-contact`
- `.tabiji-verdict`

### Step 2
Use `editorialFlags.openNow` to generate live-style hours summary labels.

### Step 3
Normalize Shinjuku source fields:
- `whatToOrder`
- verdict/tip handling
- any FAQ intentional mismatches

### Step 4
Decide whether map parity means:
- good-enough embed/search parity, or
- actual custom marker behavior parity

### Step 5
After Shinjuku is clean, convert a second page with fewer quirks to confirm the renderer generalizes.

## Bottom line

The project has crossed the line from theory into real generator work.

The remaining gaps are no longer “we need a plan.”
They are specific implementation choices:

- match the live markup contract more closely
- normalize a few overloaded source fields
- decide how far to go on map fidelity for v1

That is a much better place to be.
