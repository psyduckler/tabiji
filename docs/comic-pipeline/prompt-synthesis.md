# Per-Scam Prompt Synthesis (v2 — the current pipeline)

Every scam comic script is now **generated bespoke** from the actual scam's
content, one scam at a time, using Gemini 2.5 Pro as the script writer. This
replaces the v1 keyword-classified themed-template approach, which was fast to
build 80+ comics but produced generic comics for multi-mechanic scams.

## Why we changed

The v1 pipeline used a keyword cascade like:

```python
if "pickpocket|u-bahn|s-bahn|metro" in title:
    return pickpocket_template  # generic U-Bahn pickpocket scene
```

This broke on scams like:

- **"Brandenburger Tor Petition & Bracelet Pickpocket Distraction"** — the
  word *pickpocket* hit the cascade first, so the comic rendered a generic
  U-Bahn pickpocket scene instead of the actual petition + bracelet mechanic.
- **"Fake S-Bahn Ticket Inspector Cash Fine Scam"** — *s-bahn* hit first, so
  the comic rendered a pickpocket scene instead of a fake-inspector scene.

These comics look pretty on their own but they are **wrong** — readers land
on a page titled "Brandenburger Tor Petition & Bracelet" and see a subway
pickpocket illustration. For a print book that's a disqualifying error.

## How v2 works

The new pipeline in [`scripts/comic-pipeline/`](../../scripts/comic-pipeline/)
does **per-scam synthesis** via Gemini. For each scam:

1. Extract the scam's **title + location + first paragraph of the story** from
   the city HTML.
2. Call Gemini 2.5 Pro with:
   - a system prompt that describes the 4-character cast and their scam-fit
     pairings
   - the specific scam's content
   - a strict JSON response schema (character + 4 panels with scene + dialogue)
3. Gemini picks the right character and writes a bespoke 4-panel script that
   actually shows **this specific scam's mechanic**.
4. The pipeline assembles the full Nano Banana Pro prompt:
   `{locked country STYLE block}\n\nCHARACTER: {verbatim paragraph}\n\nSCENE:\n{4 panels}`
5. Submit to `/edit` with the country pilot as style anchor.
6. Download + verify (JPEG header + file-size threshold ≥ 120 KB).
7. If quality gate fails, retry once via `/text-to-image` (more permissive
   content filter).
8. If the retry also fails: **flag** for manual review. Do NOT silently replace
   with a template scene.

## The Gemini system prompt (current)

Lives in [`scripts/comic-pipeline/synthesize.py`](../../scripts/comic-pipeline/synthesize.py).
The key points the prompt enforces:

- **Panel 1 = setup**, **2 = mechanic**, **3 = realization/pushback**,
  **4 = lesson/aftermath**
- **One dialogue bubble per panel**, under 8 words, **English only**
- **Specific, not generic** — if the scam is "fake Fahrscheinkontrolleur
  demanding €60 cash", the comic must show fake uniform, Dienstausweis
  refusal, BVG bank-transfer fine — not a generic transit pickpocket
- **One local-flavor phrase OK** per comic if natural ("Grüß Gott!", "Real
  Dienstausweis please!", "Meter please — Motorway!")
- **Landmark integration** — scenes reference specific landmarks from the
  scam's location field when sensible

## Usage

### Quickstart (regenerate one city)

```bash
python3 scripts/comic-pipeline/generate.py germany berlin --force
```

### Regenerate an entire country

```bash
python3 scripts/comic-pipeline/generate.py germany \
  baden-baden berlin bremen cologne dresden dusseldorf frankfurt fussen \
  hamburg heidelberg leipzig munich nuremberg potsdam rothenburg stuttgart \
  --force --batch-size 3
```

### Programmatic use

```python
from scripts.comic_pipeline.synthesize import synthesize_prompt

body = synthesize_prompt("germany", {
    "city": "berlin",
    "title": "Fake S-Bahn Ticket Inspector Cash Fine Scam",
    "location": "S-Bahn platforms (Alexanderplatz, Friedrichstraße, Hauptbahnhof)",
    "story": "A fake inspector demands 60 euros cash on the spot without showing a Dienstausweis badge...",
})
# body is a dict ready to POST to Nano Banana Pro /edit:
#   {"prompt": "...", "images": [pilot], "aspect_ratio": "1:1", "output_format": "jpeg"}
```

## Quality gate

Every generated image goes through three checks before being accepted:

1. **Nano Banana Pro returned `status: completed`** (not `failed` from content filter)
2. **JPEG header valid** (`\xff\xd8\xff`)
3. **File size ≥ 120 KB** (2K JPEG comics typically 400–700 KB; anything smaller is likely a degenerate output)

If any check fails, the pipeline retries once via `/text-to-image`. If that
also fails the scam is **flagged** in `/tmp/<country>-flagged.log` for human
review. Silent-replace is explicitly forbidden — a flagged comic is better
than a wrong comic going to print.

## Audit trail

Every generation writes a line to `/tmp/<country>-audit.jsonl` with:

```json
{"city":"berlin","n":3,"title":"...","status":"ok","character":"margie","prompt":"..."}
```

This makes it possible to go back later and inspect which character + prompt
produced which comic — critical for print-book QA and reproducibility.

## Cost and runtime

Per scam:
- **Gemini 2.5 Pro synthesis**: ~4s + small cost (reasoning tokens)
- **Nano Banana Pro generation**: ~60–90s + ~$0.10–0.20
- **Total**: ~100s per scam at batch-size 3 concurrent

For an 80-scam country: ~50–60 minutes wall time, ~$10–15 in API credits.

**Print-quality is worth the cost.** The earlier v1 approach was faster but
produced enough mis-matched comics to disqualify the output for a printed
book.

## What v1 (themed templates) is good for

Nothing, in the current pipeline. The keyword-classifier approach is
deprecated. Older country batches generated with v1 (Spain, Canada, China,
Indonesia, France, Thailand, Greece) should eventually be regenerated through
v2 if they're going to print — but the web-only versions are acceptable as-is.

Germany was regenerated via v2 as the first production run.
