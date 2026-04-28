# Pass 3 · Design & Template

Validates conformance to `page-anatomy.yaml` and `variant-template.yaml`.

## Page anatomy conformance

For each section in `page-anatomy.yaml`:
- [ ] Section is present in the rendered HTML
- [ ] All `required` fields are filled
- [ ] Class attribute matches the spec
- [ ] Word counts are within `max_words` / `min_words` bounds (if specified)

## Variant template conformance

For each `<div class="scam-card">`:
- [ ] Header has variant_number + title + severity_badge
- [ ] Channel field uses correct emoji for channel type
- [ ] TLDR is ≤30 words and ends in `.` `!` or `?` (Rule 18)
- [ ] Exactly 3 story paragraphs in `.scam-story-body`
- [ ] Mechanics paragraph contains `<strong>` takeaway
- [ ] Exactly 5 red flags in `.detail-block.red-flags`
- [ ] Exactly 5 defenses in `.detail-block.avoid`
- [ ] At least 1 `.reddit-quote` per variant (with verbatim quote + URL)
- [ ] Transition line follows variant (except last variant)

## CSS / styling conformance

- [ ] No inline `style="..."` attributes (all styling via classes)
- [ ] Page-specific styles use the established class names (`.tldr-box`, `.hook-section`, `.assessment-box`, `.context-sidebar`, `.glossary-toggle`, `.transition-line`, `.assessment-skip`, `.stat-strip`, `.legal-disclaimer`, `.intl-list`, `.help-list`, `.phase-list`)
- [ ] All emojis match the channel/section type (no 📞 for online-only channels; no 📍 since these aren't location-bound)
- [ ] Color tokens reference CSS variables (`var(--terracotta)` not hex)

## Meta tags

- [ ] `<title>` is ≤70 chars
- [ ] `<meta description>` is 150-160 chars
- [ ] `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name`, `og:image` all present
- [ ] `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` all present
- [ ] `og:image` and `twitter:image` URLs return 2xx (or fall back to default)
- [ ] `<link rel="canonical">` matches the page URL
- [ ] `<meta name="robots">` is `index, follow, max-image-preview:large`

## Schema

- [ ] `Article` schema present with required fields (headline, description, datePublished, dateModified, author, publisher)
- [ ] `BreadcrumbList` schema present, 4 levels (Home > Scams > Everywhere > <slug>)
- [ ] `FAQPage` schema present with 8-10 questions
- [ ] `HowTo` schema present with 5 steps
- [ ] All JSON-LD parses validly (run through validator)
- [ ] No schema field references a URL or value that's been changed since v1

## Mobile / responsive

- [ ] Page layout intact at 360px viewport (smallest common mobile)
- [ ] Page layout intact at 768px viewport (tablet)
- [ ] Page layout intact at 1440px viewport (desktop)
- [ ] No horizontal scroll at any viewport
- [ ] Touch targets ≥ 44×44px (FAQ buttons, links, CTAs)
