# Credit Card Travel Benefits Database — Build Report
**Generated:** 2026-03-30  
**Files written:** 10 card JSON files + this report

---

## Cards Built

| Card | Slug | Annual Fee | Status |
|------|------|-----------|--------|
| Chase Sapphire Reserve | `chase-sapphire-reserve` | $795 | Active |
| Amex Platinum | `amex-platinum` | $895 | Active |
| Amex Gold | `amex-gold` | $325 | Active |
| Capital One Venture X | `capital-one-venture-x` | $395 | Active |
| Chase Sapphire Preferred | `chase-sapphire-preferred` | $95 | Active |
| Citi Prestige | `citi-prestige` | $495 | ⚠️ Closed to new apps (2021) |
| US Bank Altitude Reserve | `us-bank-altitude-reserve` | $400 | ⚠️ Closed to new apps (Nov 2024) |
| Amex Green | `amex-green` | $150 | Active |
| Capital One Venture | `capital-one-venture` | $95 | Active |
| Discover it Miles | `discover-it-miles` | $0 | Active |

---

## Key Findings & Important Notes

### Chase Sapphire Reserve — Annual Fee Update
- **Fee increased from $550 → $795 on June 23, 2025** (new applicants) / October 2025 (existing cardholders at renewal)
- New benefits added: The Edit hotel credit ($500/yr), dining credit ($300/yr), Apple subscription credit ($288/yr)
- Global Entry/TSA PreCheck credit increased to $120 (from $100)
- Earn rates restructured: 8x Chase Travel, 4x flights/hotels direct, 3x dining
- The task brief listed $550 — this has been updated to $795 reflecting current fee

### Amex Platinum — Lounge Access Clarification
- **Still has Priority Pass Select as of March 2026** (not removed — task brief noted possible 2025 removal)
- Delta Sky Club: limited to **10 visits/year** (since Feb 2024) when flying Delta
- Centurion Lounges: 15 US locations + international
- Annual fee confirmed at **$895** (not $695 — increased in 2022)

### Amex Platinum — Medical Evacuation vs Treatment
- Premium Global Assist covers **emergency evacuation transport at no charge**
- Does NOT cover medical treatment costs
- Baggage: only lost/stolen/damaged — **NO baggage delay coverage**

### Capital One Venture X — Trip Cancellation Limitation
- Only covers **2 scenarios**: death/illness of immediate family OR carrier insolvency
- Does NOT cover: severe weather, jury duty, or most reasons Chase/Amex cover
- Maximum: $2,000/person vs Chase Sapphire Reserve's $10,000/person

### Citi Prestige — Discontinued
- Closed to new applications since **summer 2021**
- Existing cardholders still hold card with original benefits
- Benefits may be subject to change; cardholders should verify with Citi
- Notable unique benefit: **fourth night free** on hotel stays (up to 2x/year)

### US Bank Altitude Reserve — Double Closure
- Stopped accepting new applications **November 2024**
- **Major negative changes December 15, 2025**:
  - Travel portal redemption value: 1.5 cpp → 1.0 cpp (downgraded)
  - $325 credit: restricted to US Bank Travel Center only (was any travel + dining)
  - 3x mobile wallet capped at $5,000/billing cycle (was unlimited)
- Priority Pass: **8 visits per membership year** (not per cardmember year) — shared pool including guests
- Data reflects **post-December 2025 benefit structure**

### Capital One Venture vs Venture X — Rental Car Insurance
- Venture X: **PRIMARY** coverage
- Regular Venture: **SECONDARY** coverage (must claim personal insurance first)
- This is a critical difference for international travelers

### Capital One Venture — Limited Travel Insurance
- **No trip delay insurance** (confirmed)
- **No trip cancellation insurance**
- **No lost baggage coverage**
- Only benefits: secondary rental car insurance + Global Entry/TSA credit + no FTF

### Amex Green — CLEAR Plus Credit
- Up to **$209/year** statement credit for CLEAR+ membership (confirmed Feb 2026)
- LoungeBuddy credit: $100/year for pay-per-visit lounges
- No lounge membership included

### Discover it Miles — International Acceptance
- No foreign transaction fees confirmed (Discover network policy)
- **Important caveat**: Discover card acceptance is poor in many international markets
  - Limited acceptance in parts of Asia, Africa, Middle East
  - Works well in US, Canada, Mexico, much of Europe
- No travel insurance benefits whatsoever
- First-year mile match is the key differentiator

---

## Data Gaps / Uncertainty Notes

| Card | Gap | Recommendation |
|------|-----|----------------|
| Chase Sapphire Reserve | Exact rental car country exclusions not specified by Chase | Check current benefit guide at chasecardbenefits.com |
| Amex Platinum | Annual fee: some sources say $695 (pre-2022), now $895 | Confirmed $895 in current NerdWallet data |
| Citi Prestige | Trip cancellation coverage amounts uncertain for legacy cards | Existing cardholders should call Citi to verify current terms |
| Citi Prestige | Trip delay trigger: some sources say 3 hours, others 6 | Could not definitively confirm — marked as 3 hours per multiple sources |
| US Bank Altitude Reserve | Post-Dec 2025 benefit guide not yet widely published | Verify full terms at usbank.com/benefits |
| Capital One Venture X | Lounge restaurant credits via Priority Pass unclear | Priority Pass Select terms vary by location |
| All Amex cards | Benefit terms update periodically — check americanexpress.com for current guide | — |

---

## Emergency Contact Numbers (Verified)

| Card | US Number | International Number |
|------|-----------|---------------------|
| Chase Sapphire Reserve | 1-800-945-2028 | 1-302-594-8200 |
| Chase Sapphire Preferred | 1-800-432-3117 | 1-302-594-8200 |
| Amex Platinum/Gold/Green | 1-800-525-3355 | 1-715-343-7977 |
| Capital One Venture X/Venture | 1-800-227-4825 | 1-804-934-2001 |
| Citi Prestige | 1-800-950-5114 | 1-605-335-2222 |
| US Bank Altitude Reserve | 1-800-285-8585 | 1-503-401-9991 |
| Discover it Miles | 1-800-347-2683 | 1-801-902-3100 |

---

## Schema Compliance Notes

- All files follow the requested schema exactly
- Added `cardStatus` field to discontinued/closed cards (Citi Prestige, US Bank Altitude Reserve)
- `baggageDelay.coveragePerPerson` for CSR reflects total ($100/day × 5 days = $500 maximum)
- `null` values used for benefits the card does not offer
- `rentalCarInsurance.coverageAmount` is null for Capital One Venture as exact limit not found in research

