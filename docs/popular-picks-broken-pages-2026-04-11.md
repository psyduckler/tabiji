# Popular Picks — Broken Pages Checklist

**Audit date:** 2026-04-11  
**Total broken pages:** 421  
**Bug:** Template rendering bug in an earlier popular-picks builder emitted only the first `restaurant-section` (or none at all) before closing the `<section class="pick-list">` wrapper prematurely. H1, schema `numberOfItems`, and hero `📝 N picks` meta all claim the correct count; the rendered body does not match.

## How to use this checklist

1. Pick the next N unchecked rows from the top of a bucket (rows are sorted by search volume descending, then alphabetically).
2. Run the `popular-picks-article-builder` skill on each slug:
   - Read `popular-picks/bogota-arepas/index.html` as the golden template (NOT `detroit-pizza/index.html` — that file is also hit by the bug).
   - Salvage the existing ItemList JSON-LD from the broken page when present — many zero-section pages have full venue data in `<head>` and only need the body re-rendered.
   - Research missing venue data via WebSearch/WebFetch (addresses, coordinates, ratings, hours).
   - For Reddit quotes, search `site:reddit.com r/<city> <category>`. Fall back to community-voice paraphrases with generic attribution if threads are not extractable.
   - Run `python3 scripts/add_photos_for_page.py <slug>` to upload per-venue photos to the R2 CDN.
3. Code-review the rebuilt page: 5 JSON-LD blocks, N restaurant-sections matching H1, ItemList/section/map-config anchor IDs all aligned, no template leaks, no `\u` unicode escapes, coordinates inside the city bbox.
4. Tick the box — `- [ ]` → `- [x]` — in the same commit as the rebuild so the checklist tracks ground truth.
5. If a venue cannot be verified, drop it rather than fabricating. Minimum acceptable: 3–4 picks per page.

## Bug signatures (how to recognize a broken page)

- **Zero sections (103 pages):** body has an empty `<section class="pick-list">` wrapper with no venue entries inside. Often the ItemList schema in `<head>` is fully populated — salvage it.
- **One section (1,057 pages):** body renders the first venue through its `<div class="pick-quick-take">`, then a `<div class="comparison-card">` (or `<div class="what-to-order">`) opens and is immediately closed by `</section>` + `<!-- social-proof:end -->`. The remaining 9–17 venues are never emitted.
- **Partial/short (64 pages):** body renders some venues but fewer than the H1 claim. Usually a mix of the one-section bug partially applied.

## Recently completed (reference rebuilds)

- [x] `amsterdam-stroopwafel` — 9 Best Stroopwafel in Amsterdam (9/9) — rebuilt 2026-04-11, live

---

## Zero sections (103 pages)

Body is empty — `<section class="pick-list">` wrapper with no venues inside. Many have full ItemList data in `<head>` that can be salvaged.

- [x] `new-york-pizza` — 18 Best Pizza Spots in New York City (18/18) · 49,500/mo — rebuilt 2026-04-11
- [x] `new-york-bagels` — 15 Best Bagels in New York City — The Unfiltered Guide (15/15) · 9,900/mo — rebuilt 2026-04-11
- [x] `kyoto-ramen` — 12 Best Ramen in Kyoto (12/12) · 8,100/mo — rebuilt 2026-04-11
- [SKIP] `los-angeles-tacos` — 11 Best Tacos in Los Angeles 2026 — Reddit-Backed Guide (0/11) · 8,100/mo — no ItemList data, needs full research
- [x] `nashville-bbq` — 12 Best BBQ in Nashville (2026) — Reddit-Backed Guide (12/12) · 6,600/mo — rebuilt 2026-04-11
- [SKIP] `barcelona-tapas` — Best Tapas Bars in Barcelona (0/14) · 4,400/mo — no ItemList data, needs full research
- [x] `hanoi-pho` — 16 Best Phở Spots in Hanoi (18/18) · 4,400/mo — rebuilt 2026-04-11
- [x] `sapporo-ramen` — 13 Best Miso Ramen in Sapporo (13/13) · 4,400/mo — rebuilt 2026-04-11
- [x] `hong-kong-dim-sum` — 14 Best Dim Sum in Central Hong Kong (14/14) · 3,600/mo — rebuilt 2026-04-11
- [x] `austin-coffee-shops` — 15 Best Coffee Shops in Austin (15/15) · 2,900/mo — rebuilt 2026-04-11
- [x] `austin-tacos` — 12 Best Tacos in Austin (2026) — Reddit-Backed Guide (12/12) · 2,400/mo — rebuilt 2026-04-11
- [x] `chicago-brunch-spots` — 12 Best Brunch Spots in Chicago (2026) — Reddit-Backed Guide (12/12) · 2,400/mo — rebuilt 2026-04-11
- [x] `new-york-ramen` — 18 Best Ramen in New York (18/18) · 2,400/mo — rebuilt 2026-04-11
- [x] `rome-pizza` — 15 Best Pizza in Rome (15/15) · 2,400/mo — rebuilt 2026-04-11
- [x] `seattle-coffee-shops` — 12 Best Coffee Shops in Seattle (2026) — Reddit-Backed Guide (12/12) · 2,400/mo — rebuilt 2026-04-11
- [x] `chicago-cocktail-bars` — 14 Best Cocktail Bars in Chicago (14/14) · 1,600/mo — rebuilt 2026-04-11
- [x] `los-angeles-ramen` — 12 Best Ramen in Los Angeles (2026) — Reddit-Backed Guide (12/12) · 1,600/mo — rebuilt 2026-04-12
- [x] `nashville-brunch-spots` — 12 Best Brunch Spots in Nashville (2026) — Reddit-Backed Guide (12/12) · 1,600/mo — rebuilt 2026-04-11
- [x] `philadelphia-coffee-shops` — 12 Best Coffee Shops in Philadelphia 2026 — Reddit-Backed Guide (12/12) · 1,600/mo — rebuilt 2026-04-11
- [x] `portland-vegan-restaurants` — 12 Best Vegan Restaurants in Portland (2026) — Reddit-Backed Guide (12/12) · 1,600/mo — rebuilt 2026-04-11
- [x] `austin-food-trucks` — 12 Best Food Trucks in Austin (2026) — Reddit-Backed Guide (12/12) · 1,300/mo — rebuilt 2026-04-11
- [x] `new-york-dim-sum` — 12 Best Dim Sum in New York City (2026) — Reddit-Backed Guide (12/12) · 1,300/mo — rebuilt 2026-04-11
- [x] `san-diego-brunch-spots` — 12 Best Brunch Spots in San Diego (2026) — Reddit-Backed Guide (12/12) · 1,300/mo — rebuilt 2026-04-11
- [x] `miami-brunch-spots` — 12 Best Brunch Spots in Miami (2026) — Reddit-Backed Guide (12/12) · 1,000/mo — rebuilt 2026-04-11
- [x] `seville-tapas` — 15 Best Tapas Bars in Seville (15/15) · 1,000/mo — rebuilt 2026-04-11
- [x] `taipei-night-markets` — 8 Best Night Markets in Taipei (8/8) · 1,000/mo — rebuilt 2026-04-11
- [x] `vienna-schnitzel` — 10 Best Schnitzel in Vienna (10/10) · 1,000/mo — rebuilt 2026-04-11
- [x] `singapore-rooftop-bars` — 12 Best Rooftop Bars in Singapore (2026) (12/12) · 110/mo — rebuilt 2026-04-11
- [x] `singapore-craft-beer` — 14 Best Craft Beer Bars & Breweries in Singapore (14/14) · 30/mo — rebuilt 2026-04-12
- [x] `austin-bbq` — 12 Best BBQ in Austin (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `austin-breakfast-tacos` — Breakfast Tacos in Austin (12/12) — rebuilt 2026-04-11
- [x] `austin-fine-dining` — 12 Best Fine Dining in Austin (12/12) — rebuilt 2026-04-12
- [x] `baltimore-coffee-shops` — 12 Best Coffee Shops in Baltimore (12/12) — rebuilt 2026-04-12
- [x] `bangkok-street-food` — 12 Best Street Food in Bangkok (12/12) — rebuilt 2026-04-12
- [x] `beijing-hot-pot` — Beijing Hot Pot Scene (2026) (10/10) — rebuilt 2026-04-11
- [x] `berlin-currywurst` — 12 Best Currywurst in Berlin (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `berlin-nightlife` — Club Nightlife in Berlin (12/12) — rebuilt 2026-04-11
- [x] `bilbao-guggenheim` — 10 Best Guggenheim Museum Bilbao Guide (10/10) — rebuilt 2026-04-12
- [x] `boston-clam-chowder` — 12 Best Clam Chowder in Boston (12/12) — rebuilt 2026-04-11
- [x] `budapest-ruin-bars` — 18 Best Ruin Bars in Budapest (18/18) — rebuilt 2026-04-11
- [x] `cartagena-nightlife` — Nightlife in Cartagena (12/12) — rebuilt 2026-04-11
- [x] `chengdu-hot-pot` — 12 Best Hot Pot in Chengdu (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `chicago-art-galleries` — 12 Best Art Galleries in Chicago (12/12) — rebuilt 2026-04-12
- [x] `chicago-brunch` — 12 Best Brunch Restaurants in Chicago (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `chicago-deep-dish-pizza` — 12 Best Deep Dish Pizza Restaurants in Chicago (2026) — Reddit-Backed … (12/12) — rebuilt 2026-04-11
- [x] `chicago-fine-dining` — 12 Best Fine Dining in Chicago (12/12) — rebuilt 2026-04-12
- [x] `chicago-italian-beef` — 12 Best Italian Beef Sandwiches in Chicago (2026) — Reddit-Backed Guid… (12/12) — rebuilt 2026-04-11
- [x] `chongqing-hot-pot` — Chongqing-Style Hot Pot (12/12) — rebuilt 2026-04-11
- [x] `denver-brunch-spots` — 12 Best Brunch Spots in Denver (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `denver-coffee-shops` — 12 Best Coffee Shops in Denver (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `guilin-rice-noodles` — Guilin Rice Noodle Shops (12/12) — rebuilt 2026-04-11
- [x] `hiroshima-okonomiyaki` — 12 Best Okonomiyaki in Hiroshima (12/12) — rebuilt 2026-04-11
- [x] `hyderabad-biryani` — Hyderabad Biryani (12/12) — rebuilt 2026-04-11
- [SKIP] `kobe-beef` — Best Kobe Beef Restaurants in Kobe (0/0) — no ItemList data
- [x] `le-morne-snorkeling` — Le Morne Snorkeling (9/9) — rebuilt 2026-04-12
- [x] `lisbon-day-trips` — Best Day Trips from Lisbon (12/12) — rebuilt 2026-04-11
- [x] `london-afternoon-tea` — 12 Best Afternoon Teas in London 2026 — Reddit-Backed Guide (12/12) — rebuilt 2026-04-12
- [x] `london-free-museums` — 15 Best Free Museums in London (16/16) — rebuilt 2026-04-11
- [x] `london-pubs` — 18 Best Pubs in London — Historic, Cozy & Real Ale Picks (18/18) — rebuilt 2026-04-11
- [x] `london-sunday-roast` — 12 Best Sunday Roasts in London 2026 (12/12) — rebuilt 2026-04-12
- [x] `marrakech-riads` — 12 Best Riads in Marrakech Medina (12/12) — rebuilt 2026-04-11
- [x] `miami-cuban-food` — 12 Best Cuban Food in Miami (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `miami-rooftop-bars` — 12 Best Rooftop Bars in Miami (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `montreal-bagels` — 10 Best Montreal's Wood-Fired Bagels (2026) — Reddit-Backed Guide (10/10) — rebuilt 2026-04-11
- [x] `montreal-poutine` — 12 Best Poutine Spots in Montreal (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `montreal-smoked-meat` — 10 Best Montreal Smoked Meat Delis (2026) — Reddit-Backed Guide (10/10) — rebuilt 2026-04-11
- [x] `naples-sfogliatella` — 12 Best Sfogliatella Shops in Naples (2026) (12/12) — rebuilt 2026-04-11
- [x] `nashville-hot-chicken` — 12 Best Hot Chicken in Nashville (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `new-orleans-beignets` — 12 Best Beignets in New Orleans 2026 — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `new-york-brunch` — 12 Best Brunch Spots in New York City (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `new-york-chopped-cheese` — 12 Best Chopped Cheese in New York City (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `new-york-korean-bbq` — 12 Best Korean BBQ in New York City (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-12
- [x] `okinawa-soba` — 12 Best Okinawa Soba Restaurants (12/12) — rebuilt 2026-04-11
- [x] `osaka-ramen` — Ramen in Osaka (12/12) — rebuilt 2026-04-11
- [x] `philadelphia-brunch` — Brunch in Philadelphia (12/12) — rebuilt 2026-04-11
- [x] `philadelphia-cheesesteaks` — Cheesesteaks in Philadelphia (12/12) — rebuilt 2026-04-11
- [x] `portland-donuts` — Legendary Donut Shops in Portland (12/12) — rebuilt 2026-04-11
- [x] `portland-food-carts` — 11 Best Food Carts in Portland (2026) — Reddit-Backed Guide (11/11) — rebuilt 2026-04-11
- [x] `reykjavik-restaurants` — Restaurants in Reykjavik (12/12) — rebuilt 2026-04-11
- [x] `san-francisco-dim-sum` — Dim Sum in San Francisco's Chinatown (12/12) — rebuilt 2026-04-11
- [x] `san-francisco-sourdough` — 12 Best Sourdough Bakeries in San Francisco (2026) — Reddit-Backed Gui… (12/12) — rebuilt 2026-04-11
- [x] `san-juan-mofongo` — 10 Best Mofongo & Puerto Rican Food in San Juan (10/10) — rebuilt 2026-04-12
- [x] `seattle-seafood` — Fresh Seafood in Seattle (12/12) — rebuilt 2026-04-11
- [x] `seattle-seafood-restaurants` — 12 Best Seafood Restaurants in Seattle (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `seoul-korean-bbq` — 17 Best Korean BBQ in Seoul (18/18) — rebuilt 2026-04-11
- [x] `shanghai-xiaolongbao` — Best Xiaolongbao in Shanghai (2026) (12/12) — rebuilt 2026-04-11
- [x] `strasbourg-christmas-market` — Strasbourg Christmas Market (12/12) — rebuilt 2026-04-11
- [x] `tokyo-day-trips` — Best Day Trips from Tokyo (12/12) — rebuilt 2026-04-11
- [x] `tokyo-sushi` — Sushi Restaurants in Tokyo (12/12) — rebuilt 2026-04-11
- [x] `toronto-night-markets` — Toronto Night Markets (12/12) — rebuilt 2026-04-11
- [x] `tulum-beach-clubs` — 11 Best Beach Clubs in Tulum — The Reddit Guide (11/11) — rebuilt 2026-04-11
- [x] `valencia-paella` — Authentic Paella in Valencia (12/12) — rebuilt 2026-04-11
- [x] `venice-cicchetti` — 11 Best Cicchetti Bars in Venice — The Unfiltered Bàcari Guide (11/11) — rebuilt 2026-04-11
- [x] `venice-ghost-tours` — Ghost Tours in Venice (12/12) — rebuilt 2026-04-11
- [x] `yokohama-ramen` — Yokohama Ramen & Chinatown (12/12) — rebuilt 2026-04-11
- [x] `zhangjiajie-glass-bridge` — Zhangjiajie Glass Bridge (12/12) — rebuilt 2026-04-11

## One section — non-country (1014 pages)

Template cuts after venue #1. Largest bucket — rebuild with full research since existing data is only one venue.

- [x] `st-louis-ribs` — 10 Best Ribs in St. Louis (10/10) · 9,900/mo — rebuilt 2026-04-11
- [x] `rome-gelato` — 18 Best Gelato Shops in Rome (Tourist Traps Flagged) (18/18) · 1,900/mo — rebuilt 2026-04-11
- [x] `chicago-tacos` — 12 Best Tacos in Chicago (2026) — Reddit-Backed Guide (12/12) · 1,600/mo — rebuilt 2026-04-11
- [x] `paris-bakeries` — 18 Best Bakeries & Pâtisseries in Paris (18/18) · 1,300/mo — rebuilt 2026-04-11
- [x] `paris-croissants` — 15 Best Croissants in Paris — The Unfiltered Guide (15/15) · 1,000/mo — rebuilt 2026-04-11
- [x] `miami-coffee-shops` — 12 Best Coffee Shops in Miami (2026) — Reddit-Backed Guide (12/12) · 880/mo — rebuilt 2026-04-11
- [x] `minneapolis-brunch-spots` — 12 Best Brunch Spots in Minneapolis (2026) — Reddit-Backed Guide (12/12) · 880/mo — rebuilt 2026-04-11
- [x] `new-orleans-jazz-bars` — 12 Best Jazz Bars in New Orleans — The Reddit Guide (12/12) · 880/mo — rebuilt 2026-04-11
- [x] `paris-flea-markets` — 10 Best Flea Markets in Paris (10/10) · 880/mo — rebuilt 2026-04-11
- [x] `brussels-waffles` — 10 Best Waffles in Brussels (10/10) · 720/mo — rebuilt 2026-04-11
- [x] `mexico-city-tacos` — 18 Best Tacos in Mexico City — The Reddit-Backed Guide (18/18) · 720/mo — rebuilt 2026-04-11
- [x] `philadelphia-brunch-spots` — 12 Best Brunch Spots in Philadelphia (2026) — Reddit-Backed Guide (12/12) · 720/mo — rebuilt 2026-04-11
- [x] `portland-brunch-spots` — 12 Best Brunch Spots in Portland (2026) — Reddit-Backed Guide (12/12) · 720/mo — rebuilt 2026-04-11
- [x] `hoi-an-banh-mi` — 11 Best Bánh Mì in Hội An (12/12) · 590/mo — rebuilt 2026-04-11
- [SKIP] `london-rooftop-bars` — 12 Best Rooftop Bars in London (2026) — Reddit-Backed Guide (1/12) · 590/mo — no ItemList data
- [x] `osaka-street-food` — 13 Best Street Food Spots in Osaka — The Ultimate Guide (14/14) · 590/mo — rebuilt 2026-04-11
- [x] `bangkok-rooftop-bars` — 16 Best Rooftop Bars in Bangkok (16/16) · 480/mo — rebuilt 2026-04-11
- [x] `rome-cooking-classes` — 9 Best Cooking Classes in Rome (10/10) · 480/mo — rebuilt 2026-04-11
- [x] `singapore-laksa` — 12 Best Laksa in Singapore (2026) — Reddit-Backed Hawker Guide (12/12) · 480/mo — rebuilt 2026-04-12
- [x] `madrid-churros` — 13 Best Churros in Madrid — The Unfiltered Guide (15/15) · 390/mo — rebuilt 2026-04-11
- [x] `copenhagen-bakeries` — 12 Best Bakeries in Copenhagen (12/12) · 320/mo — rebuilt 2026-04-11
- [x] `fukuoka-ramen` — 11 Best Tonkotsu Ramen in Fukuoka (12/12) · 320/mo — rebuilt 2026-04-11
- [x] `mexico-city-coffee-shops` — 14 Best Coffee Shops in Mexico City (14/14) · 320/mo — rebuilt 2026-04-11
- [x] `london-cheap-eats` — 13 Best Cheap Eats in London (13/13) · 260/mo — rebuilt 2026-04-11
- [x] `miami-cocktail-bars` — 12 Best Cocktail Bars in Miami (2026) — Reddit-Backed Guide (12/12) · 260/mo — rebuilt 2026-04-11
- [x] `paris-cheap-eats` — 13 Best Cheap Eats in Paris (13/13) · 260/mo — rebuilt 2026-04-11
- [x] `austin-craft-beer` — 12 Best Craft Beer Breweries in Austin (2026) — Reddit-Backed Guide (12/12) · 210/mo — rebuilt 2026-04-11
- [x] `jerusalem-falafel` — 8 Best Falafel Spots in Jerusalem (9/9) · 210/mo — rebuilt 2026-04-11
- [x] `lisbon-rooftop-bars` — 12 Best Rooftop Bars in Lisbon (12/12) · 210/mo — rebuilt 2026-04-11
- [x] `paris-wine-bars` — 17 Best Wine Bars in Paris (17/17) · 210/mo — rebuilt 2026-04-11
- [x] `shanghai-dim-sum` — 11 Best Dim Sum in Shanghai (2026) — Reddit-Backed Guide (11/11) · 210/mo — rebuilt 2026-04-11
- [x] `kyoto-street-food` — 12 Best Street Food Spots in Kyoto (12/12) · 170/mo — rebuilt 2026-04-11
- [x] `mexico-city-vegan-restaurants` — 10 Best Vegan Restaurants in Mexico City (10/10) · 170/mo — rebuilt 2026-04-11
- [x] `buenos-aires-pizza` — 12 Best Pizza in Buenos Aires (2026) — Reddit-Backed Guide (12/12) · 140/mo — rebuilt 2026-04-11
- [x] `lima-ceviche` — 16 Best Ceviche Spots in Lima (18/18) · 140/mo — rebuilt 2026-04-11
- [x] `oaxaca-street-food` — 12 Best Street Food in Oaxaca (2026) — Reddit-Backed Guide (12/12) · 140/mo — rebuilt 2026-04-11
- [x] `buenos-aires-empanadas` — 15 Best Empanadas in Buenos Aires — The Unfiltered Guide (15/15) · 110/mo — rebuilt 2026-04-11
- [x] `delhi-street-food` — 20 Best Street Food Spots in Delhi (20/20) · 110/mo — rebuilt 2026-04-11
- [x] `guangzhou-dim-sum` — 11 Best Dim Sum in Guangzhou (2026) — Reddit-Backed Guide (11/11) · 110/mo — rebuilt 2026-04-11
- [x] `ho-chi-minh-city-pho` — 12 Best Phở in Ho Chi Minh City (14/14) · 110/mo — rebuilt 2026-04-11
- [x] `istanbul-breakfast` — 12 Best Turkish Breakfast Spots in Istanbul (12/12) · 110/mo — rebuilt 2026-04-11
- [SKIP] `seattle-craft-beer` — 12 Best Craft Beer Breweries in Seattle (2026) — Reddit-Backed Guide (1/12) · 110/mo — minimal ItemList, needs full research
- [x] `amsterdam-cheap-eats` — 18 Best Cheap Eats in Amsterdam (18/18) · 90/mo — rebuilt 2026-04-11
- [x] `cairo-street-food` — 18 Best Street Food Spots in Cairo (18/18) · 90/mo — rebuilt 2026-04-11
- [x] `cartagena-ceviche` — 18 Best Ceviche & Seafood Spots in Cartagena (18/18) · 90/mo — rebuilt 2026-04-11
- [x] `colombo-coffee-shops` — 12 Best Coffee Shops in Colombo (2026) — Reddit-Backed Guide (12/12) · 90/mo — rebuilt 2026-04-11
- [x] `da-nang-coffee-shops` — 13 Best Coffee Shops in Da Nang (13/13) · 90/mo — rebuilt 2026-04-12
- [x] `kanazawa-sushi` — 12 Best Sushi in Kanazawa (12/12) · 90/mo — rebuilt 2026-04-11
- [x] `penang-street-food` — 18 Best Street Food Spots in Penang (20/20) · 90/mo — rebuilt 2026-04-11
- [x] `minneapolis-craft-beer` — 12 Best Craft Breweries in Minneapolis (2026) — Reddit-Backed Guide (12/12) · 70/mo — rebuilt 2026-04-11
- [x] `warsaw-pierogi` — 13 Best Pierogi in Warsaw (2026) (13/13) · 70/mo — rebuilt 2026-04-11
- [x] `chiang-mai-cooking-classes` — 14 Best Cooking Classes in Chiang Mai (14/14) · 50/mo — rebuilt 2026-04-11
- [x] `phnom-penh-rooftop-bars` — 7 Best Rooftop Bars in Phnom Penh (7/7) · 50/mo — rebuilt 2026-04-11
- [x] `prague-cheap-eats` — 19 Best Cheap Eats in Prague (19/19) · 50/mo — rebuilt 2026-04-11
- [x] `bali-cooking-classes` — 8 Best Cooking Classes in Bali (8/8) · 40/mo — rebuilt 2026-04-11
- [x] `kuala-lumpur-rooftop-bars` — 12 Best Rooftop Bars in Kuala Lumpur 2026 — Reddit-Backed Guide (12/12) · 40/mo — rebuilt 2026-04-11
- [SKIP] `melbourne-brunch-spots` — 12 Best Brunch Spots in Melbourne (2026) — Reddit-Backed Guide (1/12) · 40/mo — minimal ItemList, needs full research
- [x] `nara-udon` — 9 Best Udon Restaurants in Nara (10/10) · 30/mo — rebuilt 2026-04-11
- [x] `osaka-craft-beer` — 10 Best Craft Beer Bars in Osaka (11/11) · 30/mo — rebuilt 2026-04-11
- [x] `singapore-late-night-food` — 12 Best Late-Night Food Spots in Singapore (12/12) · 30/mo — rebuilt 2026-04-11
- [SKIP] `auckland-brunch-spots` — 12 Best Brunch Spots in Auckland (2026) — Reddit-Backed Guide (1/12) · 20/mo — minimal ItemList, needs full research
- [x] `buenos-aires-cocktail-bars` — 14 Best Craft Cocktail Bars in Buenos Aires — The Unfiltered Guide (15/15) · 20/mo — rebuilt 2026-04-11
- [x] `osaka-cheap-eats` — 12 Best Cheap Eats in Osaka (Under ¥1,000) (12/12) · 20/mo — rebuilt 2026-04-11
- [x] `paris-natural-wine-bars` — 12 Best Natural Wine Bars in Paris (2026) — Reddit-Backed Guide (12/12) · 20/mo — rebuilt 2026-04-11
- [x] `porto-wine-bars` — 10 Best Wine Bars in Porto — The Reddit Guide (11/11) · 20/mo — rebuilt 2026-04-11
- [x] `tel-aviv-hummus` — 14 Best Hummus Spots in Tel Aviv — The Unfiltered Guide (15/15) · 20/mo — rebuilt 2026-04-11
- [x] `ghent-craft-beer` — 8 Best Craft Beer Spots in Ghent (10/10) · 10/mo — rebuilt 2026-04-11
- [x] `abu-dhabi-cheap-eats` — 12 Best Cheap Eats in Abu Dhabi (12/12) — rebuilt 2026-04-12
- [x] `abu-dhabi-photography-spots` — 12 Best Photography Spots in Abu Dhabi (12/12) — rebuilt 2026-04-12
- [x] `abu-dhabi-street-food` — 10 Best Street Food in Abu Dhabi (10/10) — rebuilt 2026-04-12
- [x] `accra-street-food` — 10 Best Street Food in Accra (10/10) — rebuilt 2026-04-12
- [x] `adelaide-art-galleries` — 10 Best Art Galleries in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-bakeries` — 10 Best Bakeries in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-brunch-spots` — 10 Best Brunch Spots in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-cocktail-bars` — 10 Best Cocktail Bars in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-coffee-shops` — 10 Best Coffee Shops in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-fine-dining` — 10 Best Fine Dining in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-photography-spots` — 10 Best Photography Spots in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-street-food` — 10 Best Street Food Spots in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `adelaide-vegan-restaurants` — 10 Best Vegan Restaurants in Adelaide (10/10) — rebuilt 2026-04-12
- [x] `almaty-street-food` — 10 Best Street Food in Almaty (10/10) — rebuilt 2026-04-12
- [x] `amman-coffee-shops` — 10 Best Coffee Shops in Amman (10/10) — rebuilt 2026-04-12
- [x] `amman-rooftop-bars` — 10 Best Rooftop Bars in Amman (10/10) — rebuilt 2026-04-12
- [x] `amman-shawarma` — 11 Best Shawarma in Amman — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `amman-street-food` — 10 Best Street Food in Amman (10/10) — rebuilt 2026-04-12
- [x] `amritsar-golden-temple-langar` — 10 Best Golden Temple Langar Experiences in Amritsar (10/10) — rebuilt 2026-04-13
- [x] `amsterdam-art-galleries` — 10 Best Art Galleries in Amsterdam (10/10) — rebuilt 2026-04-12
- [x] `amsterdam-brunch` — 10 Best Brunch Spots in Amsterdam (10/10) — rebuilt 2026-04-12
- [x] `amsterdam-craft-beer` — 10 Best Craft Beer in Amsterdam (10/10) — rebuilt 2026-04-12
- [x] `amsterdam-fine-dining` — 10 Best Fine Dining in Amsterdam (10/10) — rebuilt 2026-04-12
- [x] `amsterdam-natural-wine-bars` — 10 Best Natural Wine Bars in Amsterdam (10/10) — rebuilt 2026-04-13
- [x] `amsterdam-photography-spots` — 10 Best Photography Spots in Amsterdam (10/10) — rebuilt 2026-04-13
- [x] `amsterdam-street-food` — 10 Best Street Food in Amsterdam (10/10) — rebuilt 2026-04-13
- [x] `antwerp-art-galleries` — 10 Best Art Galleries in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-brunch` — 10 Best Brunch Spots in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-cheap-eats` — 10 Best Cheap Eats in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-coffee-shops` — 10 Best Coffee Shops in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-diamond-quarter` — 10 Best Diamond Quarter Experiences in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-fashion-shopping` — 10 Best Fashion Shops in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-fine-dining` — 10 Best Fine Dining in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `antwerp-frites` — 8 Best Frites in Antwerp (8/8) — rebuilt 2026-04-11
- [x] `antwerp-street-food` — 10 Best Street Food in Antwerp (10/10) — rebuilt 2026-04-13
- [x] `asakusa-street-food` — 10 Best Street Food in Asakusa (10/10) — rebuilt 2026-04-13
- [x] `asheville-craft-breweries` — 10 Best Craft Breweries in Asheville (10/10) — rebuilt 2026-04-13
- [x] `athens-art-galleries` — 10 Best Art Galleries in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-fine-dining` — 10 Best Fine Dining in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-flea-market` — 10 Best Flea Markets in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-photography-spots` — 10 Best Photography Spots in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-pizza` — 10 Best Pizza in Athens (10/10) — rebuilt 2026-04-11
- [x] `athens-rooftop-bars` — 10 Best Rooftop Bars in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-street-food` — 10 Best Street Food in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-tavernas` — 10 Best Tavernas in Athens (10/10) — rebuilt 2026-04-13
- [x] `athens-viewpoints` — 10 Best Viewpoints in Athens (10/10) — rebuilt 2026-04-13
- [x] `atlanta-craft-breweries` — 10 Best Craft Breweries in Atlanta (10/10) — rebuilt 2026-04-13
- [x] `auckland-art-galleries` — 10 Best Art Galleries in Auckland (10/10) — rebuilt 2026-04-13
- [x] `auckland-fine-dining` — 10 Best Fine Dining in Auckland (10/10) — rebuilt 2026-04-13
- [x] `auckland-night-markets` — 10 Best Night Markets in Auckland (10/10) — rebuilt 2026-04-13
- [x] `auckland-seafood-restaurants` — 10 Best Seafood Restaurants in Auckland (10/10) — rebuilt 2026-04-13
- [x] `auckland-viewpoints` — 10 Best Viewpoints in Auckland (10/10) — rebuilt 2026-04-13
- [x] `austin-art-galleries` — 10 Best Art Galleries in Austin (10/10) — rebuilt 2026-04-13
- [x] `austin-cheap-eats` — 10 Best Cheap Eats in Austin (10/10) — rebuilt 2026-04-13
- [x] `austin-jazz-bars` — 10 Best Jazz Bars in Austin (10/10) — rebuilt 2026-04-13
- [x] `austin-photography-spots` — 10 Best Photography Spots in Austin (10/10) — rebuilt 2026-04-13
- [x] `austin-street-food` — 10 Best Street Food in Austin (10/10) — rebuilt 2026-04-13
- [x] `austin-viewpoints` — 10 Best Viewpoints in Austin (10/10) — rebuilt 2026-04-13
- [x] `ayutthaya-street-food` — 10 Best Street Food in Ayutthaya (10/10) — rebuilt 2026-04-13
- [x] `bagan-hot-air-balloon-sunrise` — 10 Best Hot Air Balloon Experiences in Bagan (10/10) — rebuilt 2026-04-13
- [x] `bagan-lacquerware-workshop` — 10 Best Lacquerware Workshops in Bagan (10/10) — rebuilt 2026-04-13
- [x] `baku-fine-dining` — 10 Best Fine Dining in Baku (10/10) — rebuilt 2026-04-13
- [x] `baku-street-food` — 12 Best Street Food in Baku (12/12) — rebuilt 2026-04-14
- [x] `bali-fine-dining` — 12 Best Fine Dining in Bali (12/12) — rebuilt 2026-04-14
- [x] `bali-instagram-spots` — 12 Best Instagram Spots in Bali (12/12) — rebuilt 2026-04-14
- [x] `bali-night-markets` — 12 Best Night Markets in Bali (12/12) — rebuilt 2026-04-14
- [x] `bali-street-food` — 12 Best Street Food in Bali (12/12) — rebuilt 2026-04-14
- [x] `bali-surf-breaks` — 16 Best Surf Breaks in Bali (16/16) — rebuilt 2026-04-14
- [x] `bali-viewpoints` — 12 Best Viewpoints in Bali (12/12) — rebuilt 2026-04-14
- [x] `bali-yoga-retreats` — Yoga & Wellness Retreats in Bali (12/12) — rebuilt 2026-04-14
- [x] `baltimore-art-galleries` — 12 Best Art Galleries in Baltimore (12/12) — rebuilt 2026-04-14
- [x] `baltimore-bakeries` — 12 Best Bakeries in Baltimore (12/12) — rebuilt 2026-04-14
- [x] `baltimore-blue-crab` — 12 Best Blue Crab Restaurants in Baltimore (12/12) — rebuilt 2026-04-14
- [x] `baltimore-brunch-spots` — 12 Best Brunch Spots in Baltimore (12/12) — rebuilt 2026-04-14
- [x] `baltimore-cheap-eats` — 12 Best Cheap Eats in Baltimore (12/12) — rebuilt 2026-04-14
- [x] `baltimore-cocktail-bars` — 12 Best Cocktail Bars in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-fine-dining` — 12 Best Fine Dining in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-food-markets` — 12 Best Food Markets in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-jazz-bars` — 12 Best Jazz Bars in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-rooftop-bars` — 12 Best Rooftop Bars in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-street-food` — 12 Best Street Food Spots in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `baltimore-vegan-restaurants` — 12 Best Vegan Restaurants in Baltimore (12/12) — rebuilt 2026-04-15
- [x] `bangalore-craft-beer` — 12 Best Microbreweries in Bangalore (12/12) — rebuilt 2026-04-15
- [x] `bangkok-art-galleries` — 12 Best Art Galleries in Bangkok (12/12) — rebuilt 2026-04-15
- [x] `bangkok-day-trips` — 12 Best Day Trips from Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-fine-dining` — 12 Best Fine Dining in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-flower-market` — 12 Best Flower Markets in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-late-night-street-food` — Best Late Night Street Food in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-mango-sticky-rice` — 15 Best Mango Sticky Rice in Bangkok — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `bangkok-night-markets` — 12 Best Night Markets in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-photography-spots` — 12 Best Photography Spots in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-vegetarian-street-food` — Vegetarian Street Food in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-viewpoints` — 12 Best Viewpoints in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `bangkok-vintage-shopping` — Best Vintage Shopping in Bangkok (12/12) — rebuilt 2026-04-16
- [x] `barbados-fish-cakes` — 12 Best Fish Cakes & Street Food in Barbados (12/12) — rebuilt 2026-04-16
- [x] `barcelona-art-galleries` — 12 Best Art Galleries in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `barcelona-brunch` — 16 Best Brunch Spots in Barcelona (16/16) — rebuilt 2026-04-16
- [x] `barcelona-cheap-eats` — 12 Best Cheap Eats in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `barcelona-fine-dining` — 12 Best Fine Dining in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `barcelona-photography-spots` — 12 Best Photography Spots in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `barcelona-street-food` — 12 Best Street Food Spots in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `barcelona-viewpoints` — 12 Best Viewpoints in Barcelona (12/12) — rebuilt 2026-04-16
- [x] `basel-art-museums` — 12 Best Art Museums in Basel (12/12) — rebuilt 2026-04-16
- [x] `beijing-cheap-eats` — 12 Best Cheap Eats in Beijing (12/12) — rebuilt 2026-04-16
- [x] `beijing-craft-beer` — 12 Best Craft Beer Bars & Breweries in Beijing (12/12) — rebuilt 2026-04-16
- [x] `beijing-dumplings` — 12 Best Beijing Dumpling Houses (12/12) — rebuilt 2026-04-16
- [SKIP] `beijing-peking-duck` — 10 Best Peking Duck Restaurants in Beijing (1/10) — minimal ItemList, needs full research
- [x] `beijing-photography-spots` — 12 Best Photography Spots in Beijing (12/12) — rebuilt 2026-04-16
- [x] `beijing-street-food` — 12 Best Street Food in Beijing (12/12) — rebuilt 2026-04-16
- [x] `beirut-nightlife` — 12 Best Nightlife Spots in Beirut (12/12) — rebuilt 2026-04-17
- [x] `beirut-street-food` — 12 Best Street Food in Beirut (12/12) — rebuilt 2026-04-17
- [x] `belgrade-art-galleries` — 12 Best Art Galleries in Belgrade (12/12) — rebuilt 2026-04-17
- [x] `bergen-seafood` — Seafood & Fish Market in Bergen (10/10) — rebuilt 2026-04-17
- [x] `berlin-doner-kebab` — 12 Best Döner Kebab in Berlin (12/12) — rebuilt 2026-04-11
- [x] `berlin-vegan-food` — Vegan Food in Berlin (12/12) — rebuilt 2026-04-17
- [x] `berlin-vegan-restaurants` — Best Vegan Restaurants in Berlin (12/12) — rebuilt 2026-04-17
- [x] `berlin-vintage-shopping` — Best Vintage Shopping in Berlin (12/12) — rebuilt 2026-04-17
- [x] `bilbao-pintxos-bars` — 12 Best Pintxos Bars in Bilbao (12/12) — rebuilt 2026-04-17
- [x] `bogota-street-food` — Street Food & Paloquemao Market in Bogotá (12/12) — rebuilt 2026-04-17
- [x] `bologna-tortellini` — 12 Best Tortellini in Bologna 2026 — Reddit-Backed Guide (12/12) — rebuilt 2026-04-17
- [x] `bordeaux-canele` — 12 Best Canelé in Bordeaux (12/12) — rebuilt 2026-04-17
- [x] `boston-craft-beer` — 12 Best Craft Beer in Boston (12/12) — rebuilt 2026-04-17
- [x] `boston-pizza` — 10 Best Pizza in Boston (10/10) — rebuilt 2026-04-11
- [x] `boston-restaurants` — 10 Best Restaurants in Boston (10/10) — rebuilt 2026-04-11
- [x] `bratislava-street-food` — 12 Best Bratislava Street Food & Trdelník Pastries (12/12) — rebuilt 2026-04-17
- [x] `brisbane-brunch` — 12 Best Brunch Spots in Brisbane (12/12) — rebuilt 2026-04-17
- [x] `bruges-beer-bars` — 10 Best Beer Bars in Bruges (10/10) — rebuilt 2026-04-17
- [x] `bruges-chocolate` — 9 Best Chocolate Shops in Bruges (10/10) — rebuilt 2026-04-11
- [x] `brussels-beer-bars` — 10 Best Beer Bars in Brussels (10/10) — rebuilt 2026-04-11
- [x] `bucharest-coffee-shops` — 12 Best Coffee Shops in Bucharest (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-17
- [x] `bucharest-craft-beer` — 12 Best Craft Beer Bars in Bucharest 2026 — Reddit-Backed Guide (12/12) — rebuilt 2026-04-17
- [x] `bucharest-street-food` — 12 Best Bucharest Street Food & Romanian Cuisine (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-17
- [x] `budapest-langos` — 10 Best Lángos in Budapest (10/10) — rebuilt 2026-04-11
- [x] `buenos-aires-steakhouses` — 18 Best Steakhouses & Parrillas in Buenos Aires (18/18) — rebuilt 2026-04-17
- [x] `busan-milmyeon` — 7 Best Milmyeon in Busan (8/8) — rebuilt 2026-04-11
- [x] `canggu-beach-clubs` — 13 Best Beach Clubs in Canggu — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `cartagena-street-food` — 12 Best Street Food in Cartagena (12/12) — rebuilt 2026-04-17
- [x] `casablanca-art-galleries` — 12 Best Art Galleries in Casablanca (12/12) — rebuilt 2026-04-17
- [x] `casablanca-seafood` — 12 Best Fresh Atlantic Seafood in Casablanca (12/12) — rebuilt 2026-04-17
- [x] `casablanca-street-food` — 12 Best Street Food in Casablanca (12/12) — rebuilt 2026-04-17
- [x] `catania-arancini` — 12 Best Arancini in Catania (12/12) — rebuilt 2026-04-17
- [x] `catania-fish-market` — 12 Best Fish Market Spots in Catania (12/12) — rebuilt 2026-04-17
- [x] `charleston-shrimp-and-grits` — 12 Best Shrimp and Grits in Charleston (12/12) — rebuilt 2026-04-17
- [x] `chengdu-dan-dan-noodles` — 12 Best Dan Dan Noodles in Chengdu (12/12) — rebuilt 2026-04-18
- [x] `chengdu-fine-dining` — 12 Best Fine Dining in Chengdu (12/12) — rebuilt 2026-04-17
- [x] `chengdu-street-food` — 12 Best Chengdu Street Food Spots (12/12) — rebuilt 2026-04-18
- [x] `chennai-filter-coffee` — 12 Best Filter Coffee in Chennai (12/12) — rebuilt 2026-04-18
- [x] `chiang-mai-khao-soi` — 14 Best Khao Soi in Chiang Mai — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `chiang-mai-thai-massage` — 15 Best Traditional Thai Massages in Chiang Mai — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `chicago-pizza` — 10 Best Pizza in Chicago (10/10) — rebuilt 2026-04-11
- [x] `chicago-restaurants` — 10 Best Restaurants in Chicago (1/10) — rebuilt 2026-04-22
- [x] `cusco-restaurants` — Andean Cuisine in Cusco (1/12) — rebuilt 2026-04-22
- [x] `dallas-bbq` — 10 Best BBQ in Dallas (10/10) — rebuilt 2026-04-11
- [x] `dallas-restaurants` — 10 Best Restaurants in Dallas (10/10) — rebuilt 2026-04-22
- [x] `denver-restaurants` — 10 Best Restaurants in Denver (10/10) — rebuilt 2026-04-22
- [x] `denver-steak` — 10 Best Steak in Denver (10/10) — rebuilt 2026-04-22
- [x] `detroit-pizza` — 10 Best Pizza in Detroit (10/10) — rebuilt 2026-04-11
- [x] `edinburgh-pubs` — 14 Best Pubs in Edinburgh (14/14) — rebuilt 2026-04-11
- [x] `essaouira-seafood` — 9 Best Seafood in Essaouira Port (10/10) — rebuilt 2026-04-11
- [x] `fukuoka-yatai` — 9 Best Yatai (Street Food Stalls) in Fukuoka (10/10) — rebuilt 2026-04-11
- [x] `guadalajara-birria` — 11 Best Birria in Guadalajara (11/11) — rebuilt 2026-04-11
- [x] `hamburg-steak` — 10 Best Steak in Hamburg (10/10) — rebuilt 2026-04-11
- [x] `hanoi-bun-rieu` — 9 Best Bún Riêu in Hanoi (2026) — Reddit-Backed Crab Noodle Soup Guide (12/12) — rebuilt 2026-04-11
- [x] `hanoi-egg-coffee` — 12 Best Egg Coffee in Hanoi (12/12) — rebuilt 2026-04-11
- [x] `harbin-ice-sculpture-festival` — Ice Sculpture Festival in Harbin (1/12) — rebuilt 2026-04-22
- [x] `helsinki-restaurants` — Food in Helsinki (1/12) — rebuilt 2026-04-22
- [x] `hoi-an-cao-lau` — 11 Best Cao Lầu in Hội An (12/12) — rebuilt 2026-04-11
- [x] `hong-kong-claypot-rice` — 12 Best Claypot Rice in Hong Kong — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [SKIP] `hong-kong-rooftop-bars` — Rooftop Bars in Hong Kong (1/12) — minimal ItemList, needs full research
- [x] `houston-restaurants` — 10 Best Restaurants in Houston (10/10) — rebuilt 2026-04-11
- [x] `ipoh-dim-sum` — 10 Best Dim Sum in Ipoh (10/10) — rebuilt 2026-04-11
- [x] `istanbul-baklava-shops` — 12 Best Baklava Shops in Istanbul (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `istanbul-rooftop-restaurants` — 15 Best Rooftop Restaurants in Istanbul — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `istanbul-street-food` — Best Street Food in Istanbul (1/12) — rebuilt 2026-04-22
- [SKIP] `jaipur-thali-restaurants` — 11 Best Thali Restaurants in Jaipur (2026) (1/11) — minimal ItemList, needs full research
- [x] `kobe-chinatown` — 9 Best Eats in Kobe Chinatown (Nankinmachi) (9/9) — rebuilt 2026-04-11
- [x] `kobe-sushi` — 10 Best Sushi in Kobe (10/10) — rebuilt 2026-04-11
- [x] `kolkata-street-food` — 12 Best Street Food in Kolkata — The Unfiltered Guide (12/12) — rebuilt 2026-04-11
- [x] `kyoto-coffee` — 12 Best Coffee Shops in Kyoto (12/12) — rebuilt 2026-04-22
- [x] `kyoto-kaiseki` — 12 Best Affordable Kaiseki in Kyoto (12/12) — rebuilt 2026-04-11
- [x] `kyoto-sushi` — 10 Best Sushi in Kyoto (10/10) — rebuilt 2026-04-11
- [x] `kyoto-tofu` — 10 Best Tofu Restaurants in Kyoto (10/10) — rebuilt 2026-04-11
- [x] `le-marais-falafel` — 9 Best Falafel in Le Marais (10/10) — rebuilt 2026-04-11
- [x] `lisbon-pastel-de-nata` — 18 Best Pastéis de Nata in Lisbon (18/18) — rebuilt 2026-04-11
- [x] `london-brunch` — 11 Best Brunch Spots in London (11/11) — rebuilt 2026-04-11
- [x] `los-angeles-restaurants` — 10 Best Restaurants in Los Angeles (10/10) — rebuilt 2026-04-11
- [x] `marrakech-hammams` — 15 Best Hammams in Marrakech (16/16) — rebuilt 2026-04-11
- [SKIP] `marseille-bouillabaisse` — 11 Best Bouillabaisse Restaurants in Marseille (1/11) — minimal ItemList, needs full research
- [x] `medellin-bandeja-paisa` — 10 Best Bandeja Paisa in Medellín (10/10) — rebuilt 2026-04-11
- [x] `merzouga-desert-camps` — 9 Best Desert Camps in Merzouga (10/10) — rebuilt 2026-04-11
- [x] `mexico-city-al-pastor` — 15 Best Al Pastor in Mexico City — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `miami-restaurants` — 10 Best Restaurants in Miami (10/10) — rebuilt 2026-04-11
- [x] `milan-aperitivo` — 15 Best Aperitivo Spots in Milan — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [SKIP] `montreal-brunch` — 10 Best Best Brunch Spots in Montreal (2026) — Reddit-Backed Guide (1/10) — minimal ItemList, needs full research
- [x] `nagoya-hitsumabushi` — 10 Best Hitsumabushi in Nagoya (10/10) — rebuilt 2026-04-11
- [x] `nagoya-sushi` — 10 Best Sushi in Nagoya (10/10) — rebuilt 2026-04-11
- [x] `nagoya-tebasaki` — 10 Best Tebasaki Wings in Nagoya (10/10) — rebuilt 2026-04-11
- [x] `nara-mochi` — 9 Best Mochi & Wagashi in Nara (9/9) — rebuilt 2026-04-11
- [x] `nashville-restaurants` — 10 Best Restaurants in Nashville (10/10) — rebuilt 2026-04-11
- [x] `new-orleans-restaurants` — 10 Best Restaurants in New Orleans (10/10) — rebuilt 2026-04-11
- [x] `new-york-dollar-pizza` — 12 Best Dollar Pizza Spots in New York City (2026) — Reddit-Backed Gui… (12/12) — rebuilt 2026-04-11
- [x] `new-york-fried-chicken` — 10 Best Fried Chicken in New York City (10/10) — rebuilt 2026-04-11
- [x] `new-york-pastrami` — 11 Best Pastrami Spots in NYC (2026) (11/11) — rebuilt 2026-04-11
- [x] `new-york-steak` — 10 Best Steakhouses in New York City (10/10) — rebuilt 2026-04-22
- [x] `osaka-kushikatsu` — 10 Best Kushikatsu in Osaka (10/10) — rebuilt 2026-04-11
- [x] `osaka-okonomiyaki` — 12 Best Okonomiyaki in Osaka (10/10) — rebuilt 2026-04-11
- [x] `osaka-sushi` — 10 Best Sushi in Osaka (10/10) — rebuilt 2026-04-11
- [x] `osaka-takoyaki` — 11 Best Takoyaki in Osaka (11/11) — rebuilt 2026-04-11
- [x] `oslo-restaurants` — New Nordic Restaurants in Oslo (1/12) — rebuilt 2026-04-22
- [x] `paris-banh-mi` — 10 Best Bánh Mì in Paris (10/10) — rebuilt 2026-04-11
- [x] `paris-jazz-clubs` — 15 Best Jazz Clubs in Paris (16/16) — rebuilt 2026-04-11
- [x] `penang-cendol` — 10 Best Cendol in Penang (10/10) — rebuilt 2026-04-11
- [x] `philadelphia-restaurants` — 10 Best Restaurants in Philadelphia (10/10) — rebuilt 2026-04-22
- [x] `porto-francesinha` — 12 Best Francesinhas in Porto — The Reddit Guide (12/12) — rebuilt 2026-04-11
- [x] `prague-svickova` — 9 Best Places for Svíčková in Prague (9/9) — rebuilt 2026-04-11
- [x] `queenstown-restaurants` — Best Restaurants in Queenstown (8/8) — rebuilt 2026-04-22
- [x] `rome-cacio-e-pepe` — 15 Best Cacio e Pepe in Rome — The Unfiltered Guide (15/15) — rebuilt 2026-04-11
- [x] `rome-nightlife` — Nightlife & Aperitivo Spots in Rome (1/12) — rebuilt 2026-04-22
- [x] `san-diego-fish-tacos` — 12 Best Fish Tacos in San Diego (2026) — Reddit-Backed Guide (12/12) — rebuilt 2026-04-22
- [x] `sapporo-soup-curry` — 14 Best Soup Curry in Sapporo (14/14) — rebuilt 2026-04-11
- [x] `sapporo-sushi` — 10 Best Sushi in Sapporo (10/10) — rebuilt 2026-04-11
- [SKIP] `sarajevo-cevapi` — Ćevapi & Bosnian Food in Sarajevo (1/12) — minimal ItemList, needs full research
- [x] `shibuya-ramen` — 18 Best Ramen Shops in Shibuya (18/18) — rebuilt 2026-04-11
- [x] `singapore-hawker-centers` — 20 Best Hawker Stalls in Singapore (20/20) — rebuilt 2026-04-11
- [x] `singapore-noodles` — 10 Best Noodles in Singapore (10/10) — rebuilt 2026-04-11
- [x] `split-beach-bars` — 10 Best Beach Bars in Split (10/10) — rebuilt 2026-04-11
- [SKIP] `strasbourg-tarte-flambee` — 12 Best Tarte Flambée in Strasbourg (1/12) — minimal ItemList, needs full research
- [x] `taipei-beef-noodle-soup` — 10 Best Beef Noodle Soup in Taipei (11/11) — rebuilt 2026-04-11
- [x] `tbilisi-coffee-shops` — 12 Best Coffee Shops in Tbilisi 2026 — Reddit-Backed Guide (12/12) — rebuilt 2026-04-11
- [x] `tel-aviv-nightlife` — Tel Aviv's Legendary Nightlife (12/12) — rebuilt 2026-04-22
- [SKIP] `thessaloniki-bougatsa` — 10 Best Bougatsa in Thessaloniki 2026 — Reddit-Backed Guide (1/10) — no ItemList, needs full research
- [x] `tokyo-depachika` — 12 Best Depachika (Department Store Food Halls) in Tokyo (12/12) — rebuilt 2026-04-11
- [x] `tokyo-street-food` — Tokyo Street Food & Food Stalls (1/12) — rebuilt 2026-04-22
- [SKIP] `toronto-dim-sum` — 10 Best Dim Sum in Toronto's Chinatown (2026) — Reddit-Backed Guide (1/10) — minimal ItemList, needs full research
- [SKIP] `vancouver-sushi` — 10 Best Vancouver's Sushi & Japanese Food Scene (2026) — Reddit-Backed… (1/10) — minimal ItemList, needs full research
- [x] `venice-pizza` — 10 Best Pizza in Venice (10/10) — rebuilt 2026-04-11
- [x] `verona-pizza` — 10 Best Pizza in Verona (10/10) — rebuilt 2026-04-11
- [x] `vienna-heurigen` — 10 Best Heurigen (Wine Taverns) in Vienna (10/10) — rebuilt 2026-04-11

## One section — country hubs (40 pages)

Country landing pages with only one `city-section` rendered. Some may be legitimate (only one covered city in the country) — verify against the master queue before rebuilding.

- [x] `azerbaijan` — 🇦🇿 Azerbaijan (1/0) — rebuilt 2026-04-22 (hub)
- [x] `botswana` — 🇧🇼 Botswana (1/0) — rebuilt 2026-04-22 (hub)
- [x] `iceland` — 🇮🇸 Iceland (1/0) — rebuilt 2026-04-22 (hub)
- [x] `ireland` — 🇮🇪 Ireland (1/0) — rebuilt 2026-04-22 (hub)
- [x] `kazakhstan` — 🇰🇿 Kazakhstan (1/12) — rebuilt 2026-04-22 (hub)
- [x] `lebanon` — 🇱🇧 Lebanon (1/0) — rebuilt 2026-04-22 (hub)
- [x] `mali` — 🇲🇱 Mali (1/0) — rebuilt 2026-04-22 (hub)
- [x] `nigeria` — 🇳🇬 Nigeria (1/0) — rebuilt 2026-04-22 (hub)
- [x] `puerto-rico` — 🇵🇷 Puerto Rico (1/0) — rebuilt 2026-04-22 (hub)
- [x] `serbia` — 🇷🇸 Serbia (1/0) — rebuilt 2026-04-22 (hub)
- [x] `slovakia` — 🇸🇰 Slovakia (1/0) — rebuilt 2026-04-22 (hub)

## Partial / short — non-country (57 pages)

Body renders some venues but fewer than the H1/schema claim. Smaller rebuilds — check if existing venues can be preserved.

- [x] `paris-restaurants` — 10 Best Restaurants in Paris (10/10) · 6,600/mo — rebuilt 2026-04-14
- [x] `cebu-city-lechon` — 10 Best Lechon in Cebu City (12/12) — rebuilt 2026-04-22

## Partial / short — country hubs (7 pages)

Country hubs where hero meta claims more city picks than are actually rendered. Usually a matter of adding pick-cards for already-built cities.

- [x] `canada` — 🇨🇦 Canada (10/12) — rebuilt 2026-04-22 (hub)
- [x] `colombia` — 🇨🇴 Colombia (10/12) — rebuilt 2026-04-22 (hub)
- [x] `denmark` — 🇩🇰 Denmark (4/15) — rebuilt 2026-04-22 (hub)
- [x] `morocco` — 🇲🇦 Morocco (6/12) — rebuilt 2026-04-22 (hub)
- [x] `netherlands` — 🇳🇱 Netherlands (2/12) — rebuilt 2026-04-22 (hub)
- [x] `tanzania` — 🇹🇿 Tanzania (4/12) — rebuilt 2026-04-22 (hub)

---

## Regenerating this list

To regenerate after a batch of rebuilds, re-run the audit:

```bash
python3 scripts/audit-popular-picks.js  # or the inline audit in this commit's history
```

The checklist is a point-in-time snapshot. When the next batch lands, update the top-of-file totals and the recently-completed list.