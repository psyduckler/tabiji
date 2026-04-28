# Pass 4 · Editorial Style, Expertise, Authority

Validates that the page's claims are sourced and labeled correctly.

## Source diversity (per `source-mapping.json` floor)

- [ ] At least 1 federal source cited inline (FBI / FTC / OFAC / DOJ / FCC / SEC / CFPB / state AG)
- [ ] At least 1 academic or NGO source cited inline (USIP / AARP / Chainalysis-research / academic study / consumer-protection nonprofit)
- [ ] At least 1 industry / vendor source cited inline (Krebs / Mandiant / Pindrop / TRM Labs / etc., depending on scam type)
- [ ] At least 1 mainstream press source cited inline (NYT / WSJ / Reuters / BBC / AP / Wired / 404 Media)

## Citation discipline

- [ ] Every numerical claim has an inline link to a source URL
- [ ] Every named entity (Wealth Fims, Operation Shamrock, etc.) is sourced
- [ ] Every Reddit thread reference includes the verbatim title in quotes + the upvote count + access date ("as of Apr 2026")
- [ ] No claim references a URL not also in `tmp/scam-skill/<slug>/sources.md`
- [ ] No source from `sources.md` is missing a verbatim quote in the audit trail

## Verified vs Estimated labeling

- [ ] Stat strip cards show source attribution + ✓verified or ⚠estimated label
- [ ] ⚠estimated stats use NGO/academic/industry sources (not government)
- [ ] No stat in the page comes from a `❌unverifiable` source

## Claim softening

- [ ] No "ends careers" / "ruins lives" dramatic absolutes
- [ ] No "always" / "never" claims about scammer behavior (use "typically" / "usually")
- [ ] Specific named banks / corporations are softened ("major U.S. banks" not "Wells Fargo, Chase, BofA, Citi" unless each is independently sourced)
- [ ] Date claims have hedge ranges where research is uncertain ("between roughly 2016 and 2018" not "in 2016")
- [ ] Generic-sounding example names (e.g., "BitForex Pro") are removed if they collide with real entity names

## Disclaimer correctness

- [ ] Legal disclaimer accurately states the corpus size from `corpus.json`
- [ ] Legal disclaimer cites the right "as of Month Year" timestamp
- [ ] Legal disclaimer names a refresh date (today + 90 days)
- [ ] Legal disclaimer notes archive.org backup availability
- [ ] Legal disclaimer disclaims as "consumer education, not legal or financial advice"

## Author + publisher

- [ ] Article schema author = Bernard Huang (or whoever the editor-of-record is)
- [ ] Author has `worksFor` Organization in schema
- [ ] Page byline div present with author name + title

## Cross-checks

- [ ] All numbers in the body match the numbers in the stat strip
- [ ] All numbers in the FAQ answers match the numbers in the body
- [ ] All Reddit upvote counts in the body match the source threads section
- [ ] No corpus-size claim drifts from the actual `corpus.json` size
