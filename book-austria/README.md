# Austria: Tourist Scams (Volume 12)

## Amazon KDP book description (HTML)

Paste into the KDP **Description** field. 3,815 characters (KDP limit 4,000). KDP supports a narrow HTML subset: `<br> <b> <i> <u> <h4>–<h6> <p> <ol> <ul> <li>` — no links, images, or tables. Full listing copy (title, subtitle, 7 keywords, 3 categories, pricing) lives in `amazon-listing.md`.

<!-- BEGIN KDP DESCRIPTION -->

<h4>Austria is one of the safest countries you'll ever visit. That's exactly why its scams work — and this book gives you the exact phrase that ends each one.</h4>

<p>You've planned this trip for years. The flights are paid for. Your itinerary weaves together Vienna's coffee houses, Salzburg's old town, a Danube cruise through the Wachau, the postcard lake at Hallstatt, and the Alps around Innsbruck and Zell am See. You'll be tired, jet-lagged, and navigating a language you don't speak. That's the moment a scam works.</p>

<p>Nobody is going to mug you in Salzburg. They will, however, hand you a card terminal pre-set to charge your euros in dollars at a markup, quote a "fixed" airport fare that quietly doubles, seat you at a lakeview table where the water you didn't order costs nine euros, or sell you a grand "Mozart concert" that turns out to be three students in a rented room. Vienna alone logs roughly 5,300 pickpocketing cases a year, and its Federal Criminal Police put apartment-rental fraud at about 30 cases a week. Most of these interactions are quiet, legal-looking, and over in under two minutes — you don't have time to look anything up.</p>

<h4>What's inside this book</h4>

<ul>
<li><b>56 documented scams</b> across Vienna, the Wachau, Linz, Salzburg, Hallstatt, Bad Gastein, Zell am See, Innsbruck and Graz — each with the exact move, said calmly, that ends it.</li>
<li><b>6 universal scam patterns</b> so you can spot the dozens of variations still being invented.</li>
<li><b>A print-ready German phrase card</b> — English, German and simple phonetics, including the one line ("Auf Euro, bitte") that defeats the single most common scam in the country.</li>
<li><b>A post-scam recovery playbook</b> — who to call in the first hour, which embassy answers in English, which card issuer to reach first, and exactly how to file an Anzeige (crime report).</li>
<li><b>Emergency contacts verified current for 2026</b> — 112/133 dispatch, embassies in Vienna, English-speaking hospitals in each major city, and police posts at every major station.</li>
<li><b>Original full-color illustrations</b> — nine mid-century travel-poster chapter openers plus a comic for every one of the 56 scams.</li>
</ul>

<h4>Who this book is for</h4>

<p>First-time visitors to Austria. Repeat travelers who've been lucky so far. Solo female travelers who want specific scripts, not vague warnings. Parents traveling with kids. Anyone who's read a generic travel guide and noticed the safety chapter was two pages of "watch your wallet" and nothing actionable.</p>

<h4>Why this book is different</h4>

<p>Most travel-safety content is generic. This book is specific. Every scam was drawn from Austrian press coverage — Der Standard, Die Presse, the Kronen Zeitung, the Kurier and the Salzburger Nachrichten — and cross-referenced against police and Federal Criminal Police warnings, VKI and Arbeiterkammer consumer-protection notices, and firsthand traveler accounts. Where we name operators, case counts or euro amounts, we cite them.</p>

<p>We don't tell you to "be aware of your surroundings." We tell you what to say when an ATM offers to charge you in dollars, what to do when a lakeview restaurant adds a cover charge and a bottled-water line you never agreed to, and how to tell a licensed taxi from an unlicensed "black taxi" at the station.</p>

<h4>About Tabiji</h4>

<p>Tabiji is a travel-safety research organization tracking scams, health risks and local advisories across more than fifty cities worldwide, all published free at tabiji.ai and updated as new reports come in. This is Volume 12 of the Tabiji Travel Safety Series; Volume 1 (Japan) is available on Kindle now.</p>

<p><b>Buy this book before you leave. Screenshot the phrase card onto your phone. Enjoy the Sachertorte.</b></p>

<!-- END KDP DESCRIPTION -->

---

# Book generator — Tabiji Travel Safety Series

Build the Kindle EPUB from structured scam data (`api/v1/scams/*.json`) plus
hand-written manuscript markdown.

## Quickstart

```bash
pip3 install pyyaml
python3 book/build.py
```

Output: `book/build/japan-scams.epub`

## Directory layout

```
book/
  config.yaml              # title, author, cities in reading order
  build.py                 # the generator
  manuscript/              # hand-written chapters
    00-title.md            # title page
    01-copyright.md        # copyright + disclaimer
    02-introduction.md     # "how to use this book" — STUB
    03-red-flag-patterns.md# the 6 universal patterns — STUB
    04-cities-section.md   # intro + <!-- CITIES --> insertion marker
    90-appendix-phrase-card.md  # Japanese exit phrases — STUB, native-speaker review required
    91-appendix-recovery.md     # post-scam playbook — STUB
    92-appendix-contacts.md     # emergency contacts — STUB
    95-about.md                 # about Tabiji — STUB
    99-cta.md                   # review CTA + series tease
  templates/
    style.css              # Kindle-friendly CSS
  assets/
    cover.jpg              # KDP-spec 1600x2560 JPG (produced from Desktop SVG)
  build/                   # generator output (gitignored)
```

## How city chapters are generated

The string `<!-- CITIES -->` in any manuscript file triggers auto-insertion of
one chapter per city in the order defined by `config.yaml`. Chapter content
for each city is drawn from `api/v1/scams/<city>.json`, one section per scam.

To add a written intro for a specific city, drop a file in the manuscript folder
named `cities-<slug>-intro.md` (e.g. `cities-tokyo-intro.md`). The build picks
it up automatically.

## Swapping volumes (Kyoto region, Southeast Asia, etc.)

The generator is data-driven. For a new volume:

1. Copy `book/` to a new directory or branch.
2. Update `config.yaml` — title, subtitle, cities list.
3. Rewrite the front-matter markdown (intro, red-flag patterns for that region).
4. Run `python3 build.py`.

The per-scam rendering is reused for free.

## Validating

```bash
# Install epubcheck (requires Java):
brew install epubcheck

# Check EPUB:
epubcheck book/build/japan-scams.epub
```

## TODO gates (as of v0.1 scaffold)

Run `python3 build.py` and the summary lists remaining `**TODO**` markers.
All TODOs must be resolved before KDP submission.
