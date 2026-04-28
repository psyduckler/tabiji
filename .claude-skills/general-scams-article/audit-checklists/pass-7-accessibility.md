# Pass 7 · Accessibility (WCAG 2.1 AA)

Validates the page for WCAG 2.1 AA conformance. Run with axe-core or a
similar automated tool, plus manual spot checks.

## Color contrast

- [ ] Body text (any color on any background) ≥ 4.5:1 contrast ratio
- [ ] Large text (18pt+ or 14pt+ bold) ≥ 3:1 contrast ratio
- [ ] Severity badges (high / medium / low) meet contrast ratio for their text
- [ ] Stat strip numbers + labels meet contrast on warm-cream background
- [ ] Reddit pull-quote source attribution meets contrast

## Text alternatives

- [ ] Every `<img>` has descriptive `alt` attribute
- [ ] Decorative images have `alt=""`
- [ ] Emoji that convey meaning (🚨, 📞, 💬, 📌) have aria-label or are wrapped in text that describes them
- [ ] Comic illustrations (when present) have alt text describing the scene

## Semantic HTML

- [ ] `<main id="main">` wraps the article content
- [ ] `<h1>` appears exactly once on the page
- [ ] Heading levels follow logical hierarchy (no h2→h4 skips)
- [ ] `<article>` semantic where appropriate
- [ ] `<nav>` for the site nav and TOC
- [ ] `<footer>` for the site footer
- [ ] Lists use `<ul>` / `<ol>` not `<div>` styled as lists

## Keyboard navigation

- [ ] Skip link ("Skip to main content") works on first Tab press
- [ ] All interactive elements (FAQ buttons, dropdowns, links, CTAs) reachable via Tab
- [ ] Visible focus indicator on every focusable element
- [ ] No keyboard traps (can Tab through entire page without getting stuck)
- [ ] FAQ disclosure buttons can be triggered via Enter and Space

## ARIA

- [ ] Hamburger nav has `aria-label` and `aria-expanded`
- [ ] Dropdown toggles have `aria-expanded` that changes state on click
- [ ] FAQ buttons have appropriate `aria-expanded` (or are inside `<details>` which handles it natively)
- [ ] Skip-link has `class="skip-link"` and proper styling
- [ ] No `role` attributes that conflict with native semantic meaning

## Screen-reader experience

- [ ] Reading the page top-to-bottom in screen-reader mode produces a coherent narrative
- [ ] No "click here" or "read more" links — every link text describes its destination
- [ ] Number-heavy stat strip cards announce as "[number] [description]" not just "[number]"
- [ ] Reddit pull-quote attribution is read with quote and source clearly distinguished

## Touch targets

- [ ] All tappable elements ≥ 44×44 CSS pixels (per WCAG 2.5.5)
- [ ] FAQ buttons large enough on mobile
- [ ] Action grid CTA buttons large enough on mobile
- [ ] Dropdown nav items large enough on mobile

## Forms / inputs

- [ ] No `<input>` without associated `<label>`
- [ ] Skip-to-content link visible on focus
- [ ] Self-assessment is not a real form (it's a list of questions to ponder), so no input requirements
