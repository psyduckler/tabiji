# Compare Pages — Tiered Keep List

- **Total compare pages on disk:** 1520
- **Data source:** Semrush US database, `phrase_these` endpoint
- **Method:** For each slug `A-vs-B`, we queried both `A vs B` and `B vs A` and summed monthly search volumes.

## ⚠️ Sports/politics caveat — read this first

Raw SEMrush volumes for country-vs-country and major-club city pairs are heavily 
inflated by sports SERPs (football/cricket national teams, La Liga, Premier League, NFL, 
College Football, etc.) — not travel intent. We flag these with `likely_sports=yes` 
in the CSV. **The true editorial priority tier is `likely_sports=no` + Tier 1/2** — 
because those are the pages where the search volume actually reflects travel intent.

- 453 of 1520 rows flagged as likely sports-inflated.
- Tier 1: **55 pure-travel** + 272 sports-inflated
- Tier 2: **124 pure-travel** + 132 sports-inflated
- Tier 3: **198 pure-travel** + 32 sports-inflated

## Tier breakdown

| Tier | Volume range | Total | Pure-travel | Sports-inflated | Action |
|------|--------------|------:|------------:|----------------:|--------|
| **1 — Flagship** | ≥ 2,000 | 327 | 55 | 272 | Heavy content investment; update regularly |
| **2 — Solid**    | 500–1,999 | 256 | 124 | 132 | Moderate upkeep; rewrite when time allows |
| **3 — Maintain** | 100–499 | 230 | 198 | 32 | Keep alive, minimal investment |
| **Drop**         | < 100 | 707 | — | — | Consider deleting |

**Keep (raw):** 813 pages   |   
**Keep (travel-only):** 377 pages   |   
**Drop (< 100 vol):** 707 pages

## Recommended editorial strategy

1. **Invest heavily** in Tier 1 travel-only pages (the ~55 flagship travel comparisons).
2. **Maintain** Tier 2 + Tier 3 travel-only pages (~320 additional pages).
3. **Audit individually** Tier 1 sports-inflated pages — keep only those already ranking or where destination brand is a valid secondary reason for the search.
4. **Delete or archive** the 707 pages with < 100 total search volume.

## Tier 1 — Flagship travel pages (full list)

| Vol | Best keyword | URL |
|----:|--------------|-----|
| 101,100 | mexico vs canada | [canada-vs-mexico](compare/canada-vs-mexico/) |
| 51,400 | guadalajara vs barcelona | [barcelona-vs-guadalajara](compare/barcelona-vs-guadalajara/) |
| 45,200 | canada vs guatemala | [canada-vs-guatemala](compare/canada-vs-guatemala/) |
| 37,500 | colombia vs canada | [canada-vs-colombia](compare/canada-vs-colombia/) |
| 30,300 | puerto rico vs argentina | [argentina-vs-puerto-rico](compare/argentina-vs-puerto-rico/) |
| 19,200 | canada vs honduras | [canada-vs-honduras](compare/canada-vs-honduras/) |
| 12,500 | california vs hawaii | [california-vs-hawaii](compare/california-vs-hawaii/) |
| 11,000 | canada vs ecuador | [canada-vs-ecuador](compare/canada-vs-ecuador/) |
| 9,400 | jamaica vs curacao | [curacao-vs-jamaica](compare/curacao-vs-jamaica/) |
| 9,000 | seattle vs toronto | [seattle-vs-toronto](compare/seattle-vs-toronto/) |
| 7,800 | jamaica vs bermuda | [bermuda-vs-jamaica](compare/bermuda-vs-jamaica/) |
| 6,400 | canada vs sweden | [canada-vs-sweden](compare/canada-vs-sweden/) |
| 6,400 | new england vs chicago | [chicago-vs-new-england](compare/chicago-vs-new-england/) |
| 6,000 | strasbourg vs marseille | [marseille-vs-strasbourg](compare/marseille-vs-strasbourg/) |
| 5,800 | england vs united kingdom | [england-vs-united-kingdom](compare/england-vs-united-kingdom/) |
| 5,790 | miami vs vancouver | [miami-vs-vancouver](compare/miami-vs-vancouver/) |
| 4,720 | honduras vs curacao | [curacao-vs-honduras](compare/curacao-vs-honduras/) |
| 4,300 | dallas vs houston | [dallas-vs-houston](compare/dallas-vs-houston/) |
| 4,000 | curacao vs trinidad and tobago | [curacao-vs-trinidad-and-tobago](compare/curacao-vs-trinidad-and-tobago/) |
| 4,000 | maui vs kauai | [kauai-vs-maui](compare/kauai-vs-maui/) |
| 3,800 | argentina vs canada | [argentina-vs-canada](compare/argentina-vs-canada/) |
| 3,800 | orlando vs miami | [orlando-vs-miami](compare/orlando-vs-miami/) |
| 3,700 | boston vs new york | [boston-vs-new-york](compare/boston-vs-new-york/) |
| 3,700 | abu dhabi vs dubai | [dubai-vs-abu-dhabi](compare/dubai-vs-abu-dhabi/) |
| 3,700 | thailand vs cambodia | [thailand-vs-cambodia](compare/thailand-vs-cambodia/) |
| 3,500 | costa rica vs belize | [belize-vs-costa-rica](compare/belize-vs-costa-rica/) |
| 3,500 | kyoto vs osaka | [osaka-vs-kyoto](compare/osaka-vs-kyoto/) |
| 3,280 | puerto rico vs dominican republic | [puerto-rico-vs-dominican-republic](compare/puerto-rico-vs-dominican-republic/) |
| 3,200 | bermuda vs trinidad and tobago | [bermuda-vs-trinidad-and-tobago](compare/bermuda-vs-trinidad-and-tobago/) |
| 3,200 | oxford vs cambridge | [oxford-vs-cambridge](compare/oxford-vs-cambridge/) |
| 3,200 | paris vs barcelona | [paris-vs-barcelona](compare/paris-vs-barcelona/) |
| 3,040 | monaco vs strasbourg | [monaco-vs-strasbourg](compare/monaco-vs-strasbourg/) |
| 2,900 | united states vs canada | [canada-vs-united-states](compare/canada-vs-united-states/) |
| 2,900 | porto vs lisbon | [lisbon-vs-porto](compare/lisbon-vs-porto/) |
| 2,900 | mykonos vs santorini | [mykonos-vs-santorini](compare/mykonos-vs-santorini/) |
| 2,900 | vancouver vs portland | [portland-vs-vancouver](compare/portland-vs-vancouver/) |
| 2,780 | mexico vs puerto rico | [mexico-vs-puerto-rico](compare/mexico-vs-puerto-rico/) |
| 2,620 | toronto vs montreal | [toronto-vs-montreal](compare/toronto-vs-montreal/) |
| 2,610 | vancouver vs chicago | [chicago-vs-vancouver](compare/chicago-vs-vancouver/) |
| 2,600 | miami vs atlanta | [atlanta-vs-miami](compare/atlanta-vs-miami/) |
| 2,600 | portland vs seattle | [portland-vs-seattle](compare/portland-vs-seattle/) |
| 2,490 | vancouver vs austin | [austin-vs-vancouver](compare/austin-vs-vancouver/) |
| 2,490 | chicago vs new york | [chicago-vs-new-york](compare/chicago-vs-new-york/) |
| 2,480 | cabo vs cancun | [cabo-vs-cancun](compare/cabo-vs-cancun/) |
| 2,480 | maui vs oahu | [maui-vs-oahu](compare/maui-vs-oahu/) |
| 2,290 | canada vs australia | [australia-vs-canada](compare/australia-vs-canada/) |
| 2,190 | colorado vs portland | [colorado-vs-portland](compare/colorado-vs-portland/) |
| 2,180 | nashville vs austin | [austin-vs-nashville](compare/austin-vs-nashville/) |
| 2,180 | india vs maldives | [india-vs-maldives](compare/india-vs-maldives/) |
| 2,180 | toronto vs vancouver | [toronto-vs-vancouver](compare/toronto-vs-vancouver/) |
| 2,020 | romania vs canada | [canada-vs-romania](compare/canada-vs-romania/) |
| 2,020 | montreal vs quebec city | [quebec-city-vs-montreal](compare/quebec-city-vs-montreal/) |
| 2,020 | toronto vs new york | [toronto-vs-new-york](compare/toronto-vs-new-york/) |
| 2,010 | parma vs bologna | [bologna-vs-parma](compare/bologna-vs-parma/) |
| 2,000 | lyon vs strasbourg | [lyon-vs-strasbourg](compare/lyon-vs-strasbourg/) |

## Tier 1 — Sports-inflated (review individually, top 40)

These have huge raw volumes but the SERP is dominated by sports matches. 
Low ROI unless the page already ranks for a travel-intent query. See full list in `compare-tiers.csv`.

| Vol | Slug |
|----:|------|
| 640,500 | england-vs-india |
| 466,000 | portugal-vs-spain |
| 366,000 | mexico-vs-usa |
| 275,000 | australia-vs-india |
| 225,500 | spain-vs-france |
| 214,500 | honduras-vs-mexico |
| 159,500 | brazil-vs-argentina |
| 150,500 | india-vs-south-africa |
| 143,100 | mexico-vs-panama |
| 140,000 | guatemala-vs-usa |
| 137,100 | georgia-vs-texas |
| 131,000 | argentina-vs-colombia |
| 128,100 | colombia-vs-mexico |
| 114,500 | valencia-vs-barcelona |
| 93,600 | brazil-vs-colombia |
| 92,100 | denmark-vs-portugal |
| 90,000 | germany-vs-portugal |
| 83,900 | florida-vs-georgia |
| 82,700 | india-vs-new-zealand |
| 78,600 | guatemala-vs-panama |
| 78,400 | japan-vs-mexico |
| 75,300 | dominican-republic-vs-mexico |
| 73,600 | barcelona-vs-mallorca |
| 70,400 | ecuador-vs-mexico |
| 68,600 | costa-rica-vs-usa |
| 67,600 | madrid-vs-barcelona |
| 67,600 | netherlands-vs-spain |
| 62,700 | argentina-vs-uruguay |
| 62,700 | chile-vs-argentina |
| 58,600 | armenia-vs-portugal |
| 58,600 | brazil-vs-ecuador |
| 55,300 | croatia-vs-france |
| 54,900 | mexico-vs-uruguay |
| 54,200 | ireland-vs-portugal |
| 52,400 | costa-rica-vs-mexico |
| 51,200 | costa-rica-vs-honduras |
| 45,900 | panama-vs-usa |
| 45,200 | australia-vs-south-africa |
| 45,200 | bolivia-vs-brazil |
| 45,200 | france-vs-germany |
| ... | 232 more in CSV |

## Tier 2 — Solid travel pages (top 40)

| Vol | Slug |
|----:|------|
| 1,920 | lyon-vs-paris |
| 1,890 | savannah-vs-charleston |
| 1,880 | amalfi-coast-vs-cinque-terre |
| 1,880 | edinburgh-vs-glasgow |
| 1,880 | new-caledonia-vs-new-zealand |
| 1,880 | yosemite-vs-yellowstone |
| 1,780 | cabo-san-lucas-vs-cancun |
| 1,770 | nepal-vs-samoa |
| 1,760 | chicago-vs-miami |
| 1,760 | naxos-vs-paros |
| 1,720 | san-francisco-vs-los-angeles |
| 1,620 | miami-vs-porto |
| 1,620 | montreal-vs-nashville |
| 1,600 | bora-bora-vs-maldives |
| 1,600 | cabo-san-lucas-vs-los-cabos |
| 1,600 | cabo-vs-puerto-vallarta |
| 1,600 | japan-vs-korea |
| 1,600 | tokyo-vs-kyoto |
| 1,590 | boston-vs-philadelphia |
| 1,590 | samoa-vs-tonga |
| 1,480 | canada-vs-curacao |
| 1,480 | cancun-vs-tulum |
| 1,480 | tokyo-vs-osaka |
| 1,470 | canada-vs-namibia |
| 1,470 | san-diego-vs-san-francisco |
| 1,440 | barcelona-vs-granada |
| 1,440 | mallorca-vs-menorca |
| 1,390 | cancun-vs-puerto-vallarta |
| 1,360 | portland-vs-denver |
| 1,350 | colorado-vs-san-francisco |
| 1,350 | madrid-vs-salzburg |
| 1,320 | liverpool-vs-paris |
| 1,310 | aruba-vs-curacao |
| 1,310 | cancun-vs-punta-cana |
| 1,310 | greece-vs-rome |
| 1,310 | hawaii-vs-samoa |
| 1,310 | melbourne-vs-sydney |
| 1,270 | belize-vs-panama |
| 1,270 | tampa-vs-miami |
| 1,260 | maui-vs-big-island |
| ... | 84 more in CSV |

## Tier 3 — Maintain travel pages (top 30)

| Vol | Slug |
|----:|------|
| 490 | krakow-vs-warsaw |
| 490 | sardinia-vs-corsica |
| 480 | antwerp-vs-brussels |
| 480 | dubai-vs-doha |
| 480 | moorea-vs-bora-bora |
| 470 | auckland-vs-wellington |
| 470 | barbados-vs-st-lucia |
| 470 | crete-vs-santorini |
| 470 | cuba-vs-puerto-rico |
| 470 | mumbai-vs-delhi |
| 470 | shanghai-vs-hong-kong |
| 460 | atlanta-vs-nashville |
| 460 | seoul-vs-busan |
| 430 | cali-vs-medellin |
| 430 | costa-rica-vs-hawaii |
| 430 | vienna-vs-prague |
| 430 | vienna-vs-salzburg |
| 420 | dead-sea-vs-red-sea |
| 420 | denver-vs-salt-lake-city |
| 420 | pattaya-vs-phuket |
| 420 | san-diego-vs-miami |
| 420 | serengeti-vs-masai-mara |
| 420 | sydney-vs-brisbane |
| 410 | bonaire-vs-curacao |
| 410 | glacier-national-park-vs-yellowstone |
| 400 | bali-vs-maldives |
| 380 | bali-vs-fiji |
| 370 | brisbane-vs-melbourne |
| 370 | colmar-vs-strasbourg |
| 350 | chicago-vs-los-angeles |
| ... | 168 more in CSV |

## Drop candidates — top 20 of the 707 low-vol pages

| Vol | Slug |
|----:|------|
| 90 | adelaide-vs-melbourne |
| 90 | barbados-vs-trinidad |
| 90 | berlin-vs-prague |
| 90 | cadiz-vs-malaga |
| 90 | croatia-vs-turkey |
| 90 | cuba-vs-jamaica |
| 90 | dolomites-vs-swiss-alps |
| 90 | hue-vs-hoi-an |
| 90 | marrakech-vs-fez |
| 90 | morocco-vs-turkey |
| 90 | nagoya-vs-osaka |
| 90 | queensland-vs-victoria |
| 90 | santorini-vs-amalfi-coast |
| 90 | scottsdale-vs-palm-springs |
| 90 | st-lucia-vs-martinique |
| 90 | trinidad-vs-tobago |
| 80 | auckland-vs-christchurch |
| 80 | auckland-vs-sydney |
| 80 | bangkok-vs-hanoi |
| 80 | goa-vs-kerala |

## Files

- `compare-all-search-volumes.csv` — raw Semrush data, all 1,520 pages
- `compare-tiers.csv` — tiered list with `tier` and `likely_sports` columns (use this for editorial planning)
- `compare-tiers-summary.md` — this file
