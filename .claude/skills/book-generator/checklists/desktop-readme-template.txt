{COUNTRY-NAME}: Tourist Scams — Volume {VOL-NUM} of the Tabiji Travel Safety Series
{underline with equal signs matching the length of the title line above}

Complete asset bundle. {SCAM-COUNT} scams across {CITY-COUNT} {COUNTRY-ADJECTIVE} cities{optionally: and scenic regions}.
Built {DATE} from the tabiji.ai repo.


================================================================================
AMAZON KDP LISTING — copy/paste ready
================================================================================

TITLE
-----
{TITLE — from config.yaml `title` field. Plain text. KDP title field caps at
~200 chars but aim for under 60 so the full title shows on mobile thumbnails.}

SUBTITLE
--------
{SUBTITLE — from config.yaml `subtitle` field. Plain text. Use this to load
the listing with secondary keywords (city names, source publications, year).
Combined Title + Subtitle should fit under ~200 chars to avoid mobile
truncation.}

DESCRIPTION (~4,000 characters, KDP HTML supported)
----------------------------------------------------
{4000-char marketing description in KDP-allowed HTML. KDP allows: <h4>, <h5>,
<h6>, <p>, <br>, <b>/<strong>, <i>/<em>, <u>, <ul>, <li>, <ol>. Banned:
<h1>, <h2>, <h3>, <div>, inline styles, <img>, <a href>. Structure to use:

  1. Hook headline (<h4>) with the dollar threat + scope ("Don't lose AUD
     $1,000 in Australia. 84 scams across 14 cities, decoded.")
  2. Opening paragraph (<p>): the unique angle — that this is sourced from
     real reports (Reddit, police, press), not generic travel advice.
  3. "What's inside" (<h4> + <ul>): 5-7 bullet points calling out specific
     scams + their dollar amounts (e.g. "Sydney Airport taxi 'top-up' that
     pushed one traveler from $48 to $185"). Use scam names from the book.
  4. "Who this book is for" (<h4> + <ul>): 4-6 traveler personas
     (first-time visitor, working-holiday, returning, family, business).
  5. "Why we wrote it" (<p>): editorial credibility — sources cited, every
     scam has a venue/dollar amount, updates annually.
  6. Closing paragraph (<p>): direct CTA — "Read this before you book your
     flight." Single sentence.

Total budget ~3,800-4,000 chars including HTML tags. Verify with
`wc -c` before pasting into KDP. Aim within 50 chars of 4000 — KDP truncates
above that and Amazon penalizes thin descriptions.}

KDP KEYWORDS (7 max, each ≤ 50 characters)
-------------------------------------------
{Pick 7 keyword phrases that real Amazon shoppers would type. Best practice:
mix exact-match high-volume terms (e.g. "australia travel guide 2026") with
specific intent terms (e.g. "sydney scam warning"). Each keyword can be a
phrase. Don't repeat words already in the title/subtitle — those are
auto-indexed. Suggested distribution:
  - 2 country/region terms (e.g. "australia travel safety", "outback safety")
  - 2 traveler-persona terms (e.g. "backpacker scam guide australia")
  - 2 specific-pain terms (e.g. "rental car damage scam", "airport taxi
    overcharge")
  - 1 emergency/recovery term (e.g. "travel scam recovery guide")
Verify each is ≤50 chars with `awk '{print length, $0}'`.}

  1. {KEYWORD-1}
  2. {KEYWORD-2}
  3. {KEYWORD-3}
  4. {KEYWORD-4}
  5. {KEYWORD-5}
  6. {KEYWORD-6}
  7. {KEYWORD-7}


================================================================================

{OPTIONAL: Scope note. Used by books that cover a subset of a country or
that explicitly exclude regions like SARs or overseas territories.
E.g., for China: "This volume covers mainland China only. Hong Kong and
Macau are Special Administrative Regions with separate legal systems
and currencies — they are covered in their own dedicated volumes."}

{OPTIONAL: Country-name convention note. E.g., for Turkey: "The Republic
of Türkiye's English name was officially changed from 'Turkey' to
'Türkiye' in 2022. This volume uses 'Turkey' in running text and
'Türkiye' in formal contexts."}

Folder map
----------

01-final-deliverables/        Ready-to-upload files
  - {country}-scams.epub                              Kindle eBook ({size}, {word-count} words)
  - {country}-scams-paperback-interior.pdf            KDP paperback interior ({pages} pp, 6x9 trim, TOC with page numbers)
  - {country}-paperback-wraparound-cover.pdf          KDP wraparound cover ({cover-width}" x 9.25", {spine}" spine)
  - {country}-kindle-cover-1600x2560.jpg              Amazon KDP Kindle cover (exact KDP spec)

02-cover-art/                 Cover source art
  - front-raw.jpg                                     {one-line description of front-cover scene}
  - back-raw.jpg                                      {one-line description of back-cover scene}
  - front-with-text-overlay.svg                       Composed front cover with title/subtitle/stat text
  - back-with-text-overlay.svg                        Composed back cover with pitch/inside/plus text

03-city-illustrations/        {CITY-COUNT} flat-vector mid-century travel-poster illustrations (Wavespeed)
  - {comma-list of city-slug filenames}

04-scam-comics/               {SCAM-COUNT} four-panel watercolor-storybook scam comics (R2-sourced)
  - Filename format: <city-slug>-NN.jpg  (e.g. {example-city-slug}-01.jpg)

05-manuscript-source/         Editable source (markdown)
  - 01-copyright.md, 02-introduction.md, 03-red-flag-patterns.md, 04-cities-section.md
  - cities-<slug>-intro.md ({CITY-COUNT} city intros)
  - 90-appendix-phrase-card.md ({LANGUAGE} exit phrases with pronunciation cues)
  - 91-appendix-recovery.md (post-scam playbook, {police-force} desk directory)
  - 92-appendix-contacts.md ({tourist-police} + hospitals + embassies)
  - 95-about.md, 99-cta.md
  - config.yaml (series/volume metadata + city reading order)

06-build-scripts/             Reproducibility
  - build.py                                  Main EPUB builder (pandoc)
  - build_paperback_interior.py               Paperback PDF builder (pandoc + xelatex)
  - build_paperback_cover.py                  Wraparound cover PDF builder (rsvg-convert)
  - gen_city_illustrations.py                 Wavespeed city-illustration generator ({CITY-COUNT} cities)
  - gen_comics.py                             Wavespeed cover-art generator (front + back)
  - style.css                                 Kindle EPUB CSS
  - header-includes.tex                       LaTeX override: unnumbered chapters update running head

07-build-artifacts/           Intermediate files (reference only)
  - assembled-manuscript-epub.md              The full EPUB-bound markdown
  - assembled-manuscript-paperback.md         The full paperback-bound markdown
  - {country}-paperback-cover-source.svg      Pre-rendered wraparound SVG

Build stats
-----------
  Scam count:       {SCAM-COUNT}
  City count:       {CITY-COUNT}
  Word count:       ~{WORD-COUNT}
  Paperback pages:  {PAGE-COUNT}
  Paperback trim:   6" x 9"
  Paper:            cream (0.0025" per page)
  Spine width:      {SPINE}"
  Wraparound size:  {COVER-WIDTH}" x 9.25" (including 0.125" bleed)
  Kindle cover:     1600 x 2560 JPG (KDP spec)

{OPTIONAL: Currency note if a build-time normalizer is in place, e.g.:
"Every instance of the {CURRENCY-SYMBOL} (U+XXXX) in the source JSON
data is replaced at build time with '{ABBREVIATION}' because Arial
Unicode MS — the paperback body font — does not carry the glyph."}

Series context
--------------
  Vol 1: Japan (live)
  Vol 2: Italy (live)
  Vol 3: France (live)
  Vol 4: Thailand (live)
  Vol 5: Spain (live)
  Vol 6: Vietnam (live)
  Vol 7: China (live)
  Vol 8: Indonesia (live)
  Vol 9: Turkey (live)
  Vol 10: Canada (live)
  Vol {VOL-NUM}: {COUNTRY-NAME} — this bundle

Online references
-----------------
  Book page:    https://tabiji.ai/books/{country}-tourist-scams/
  Series hub:   https://tabiji.ai/books/
  Free data:    https://tabiji.ai/scams/country/{ISO}/

Editorial process
-----------------
  5x copyedit passes (typography, content, voice, {COUNTRY-ADJECTIVE} terminology, structure)
  3x publisher-editor audits (content fact-check, layout/typography, master-reader voice)
  All audit findings applied. {Summary of top-3 fixes applied in the editorial cycle.}
  Book is publish-ready.

KDP upload checklist
--------------------
  Kindle:
    - Cover:      01-final-deliverables/{country}-kindle-cover-1600x2560.jpg
    - Manuscript: 01-final-deliverables/{country}-scams.epub
    - BISAC:      TRV000000 (Travel), TRV002050 (Travel / Special Interest / Safety)
    - Title:      {COUNTRY-NAME}: Tourist Scams
    - Subtitle:   {full-subtitle-from-config}
    - Price:      $4.99 USD
    - Territories: World
  Paperback:
    - Interior:   01-final-deliverables/{country}-scams-paperback-interior.pdf
    - Cover:      01-final-deliverables/{country}-paperback-wraparound-cover.pdf
    - Trim:       6" x 9"
    - Paper:      Cream
    - Bleed:      Yes (0.125")
    - Page count: {PAGE-COUNT}

Key {COUNTRY-ADJECTIVE} helpline numbers (from the recovery appendix)
--------------------------------------------------------------------
  {NUMBER}    {PRIMARY-POLICE-FORCE-NAME}
  {NUMBER}    {SECONDARY-FORCE}
  {NUMBER}    Medical emergency / ambulance
  {NUMBER}    Fire
  {NUMBER}    {TOURIST-HELP-SERVICE}
  {NUMBER}    {CONSUMER-PROTECTION}

{OPTIONAL: Major Tourist Police / SATE / Turizm Polisi desk directory
if the country has dedicated tourist-police addresses. 5-10 rows,
formatted:
  Istanbul:   Yerebatan Caddesi 4/6, Sultanahmet.      +90 212 527 4503
  Antalya:    Cumhuriyet Caddesi 4, Kaleiçi.           +90 242 247 2400
  ...}
