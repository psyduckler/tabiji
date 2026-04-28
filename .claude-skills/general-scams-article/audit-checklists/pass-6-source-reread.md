# Pass 6 · Source Reread

The defense against post-publication source rot. For every URL cited
inline on the page, re-fetch and validate.

## Procedure

For each entry in `tmp/scam-skill/<slug>/sources.md`:

1. **Re-fetch the URL** via `WebFetch` (or `curl` for direct text)
2. **Locate the verbatim quote** in the fetched content
3. **Compare**:
   - If the quote still appears verbatim → ✓ pass
   - If the page has been reorganized but the claim is still supported → flag as ⚠ for editor review
   - If the quote is no longer present → ❌ hard fail; the claim must be removed or re-sourced

## Checks

- [ ] Every cited URL returns 2xx
- [ ] Every verbatim quote in `sources.md` still appears in the source content
- [ ] Reddit thread upvote counts are within ±20% of the cited number (acceptable drift over 90 days)
- [ ] Reddit threads are not deleted or removed (post body shows actual content, not "[deleted]" or "[removed]")
- [ ] Federal source dates are still current (i.e., FBI IC3 2024 report is still the most recent annual report; if 2025 has dropped, update)
- [ ] OFAC sanctions list still includes the named entities
- [ ] DOJ press releases are still live at their URLs (DOJ sometimes archives)

## When the source has rotted

- **404 / 410** → Use `archive-cache.json` to substitute archive.org URL; add note in `sources.md` that primary is gone
- **Substantively edited** → If the new version still supports the claim, update the verbatim quote; if not, remove the claim from the page
- **Upvote drift > 20%** → Update the page's upvote citation to the current count
- **Deleted Reddit thread** → Use archive.org backup; if no archive, remove the source-thread card and reduce the page's source thread count

## Cadence

Pass 6 runs:
- Pre-launch (mandatory)
- 90 days post-launch (per legal disclaimer's stated refresh cadence)
- On user request (e.g., before a major republication push)
