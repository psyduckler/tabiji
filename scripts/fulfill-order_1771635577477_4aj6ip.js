const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771635577477_4aj6ip',
  email: 'psyduckler@gmail.com',
  destination: 'Willamette Valley, Oregon',
  startDate: '2026-06-22',
  endDate: '2026-06-27',
  groupSize: 1,
  travelStyle: 'Cultural',
  requests: ''
};

const itineraryData = {
  destination: 'Willamette Valley, Oregon',
  countryEmoji: '🍷',
  title: 'Wine Country & Wonder: Solo in Willamette Valley',
  subtitle: '5 days of world-class Pinot, living history, lavender fields & farm-to-table Oregon soul',
  description: "Oregon's Willamette Valley is America's answer to Burgundy — rolling hills draped in Pinot Noir vines, misty mornings over the Chehalem Mountains, and a farm-to-table food culture that's as serious as the wine. But Willamette is more than a wine region: it's a place of living history, Indigenous heritage, pioneering aviation, and a community of passionate growers and makers. This solo cultural itinerary moves through iconic estate wineries, the Evergreen Aviation Museum's jaw-dropping Spruce Goose, Salem's Capitol and mission roots, and the lavender-scented back roads of Yamhill County. Late June brings long golden evenings, vine canopies in full flush, and the valley at its most lush and welcoming.",
  duration: '5 nights',
  dates: 'Jun 22 – Jun 27, 2026',
  budget: '$$',
  pace: 'Relaxed',
  bestFor: 'Solo Travelers · Culture & Wine Lovers',

  highlights: [
    'Taste benchmark Pinot Noir at Domaine Drouhin — Burgundy\'s legendary family, Oregon\'s finest terroir',
    'Stand beneath the Spruce Goose at Evergreen Aviation & Space Museum — the largest wooden aircraft ever built',
    'Explore Stoller Family Estate: sweeping Chehalem Mountain views and America\'s first solar-powered winery',
    'Walk McMinnville\'s historic 3rd Street — galleries, bookshops, and James Beard–worthy restaurants',
    'Wander Salem\'s Willamette Heritage Center: Oregon\'s Indigenous and pioneer past brought to life',
    'Discover lavender in full bloom at a Yamhill County farm — late June is peak season'
  ],

  essentials: [
    { title: '☀️ Late June Weather', text: 'Expect 22–28°C (72–82°F) with long daylight until 9pm. Mornings can be misty in the hills — perfect for atmospheric vineyard walks. Pack sunscreen and a light layer for evening tastings on open terraces.' },
    { title: '🚗 Getting Around', text: 'A rental car is essential — wineries are spread across rolling hills and small towns. Pick up at Portland PDX (~45 min to Dundee). Designate a sober driver day or use a winery shuttle service on your big tasting days. Parking is free everywhere.' },
    { title: '🍷 Tasting Tips', text: 'Many top Willamette wineries require advance reservations (especially Domaine Drouhin, Archery Summit, The Allison Inn). Book at least 1 week ahead for summer weekends. Tasting fees run $25–55 but are often waived with a wine purchase.' },
    { title: '📅 June in Willamette', text: 'Late June is just after bloom and before harvest — vines are lush green with tiny grape clusters forming. Lavender peaks in late June. McMinnville\'s Thursday Farmers\' Market (6th & Davis) is a weekly highlight with 60+ vendors.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-22',
      neighborhoods: 'Portland → Newberg → Dundee Hills',
      title: 'Arrival & Dundee Hills — The Heart of Oregon Pinot',
      description: "Drive south from Portland into one of America's greatest wine landscapes. The Dundee Hills are Willamette Valley's most prestigious AVA — ancient volcanic Jory soil producing Pinot Noir of startling elegance. Start with the classics on this arrival day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive from Portland to Dundee (45 min)',
              description: 'Pick up your rental at PDX and head south on Hwy 99W through Newberg into the Dundee Hills. The moment you crest the ridge into Chehalem Valley, vineyard-covered slopes unfold on every side. Stop at a viewpoint pullout on Worden Hill Road for a first survey of the landscape.',
              details: [
                '🚗 PDX → Dundee: 45 min via OR-99W South',
                '📸 Best first viewpoint: Worden Hill Road pullout, elevation ~500 ft',
                '🏨 Base yourself in McMinnville (25 min west) — best restaurant access',
                '📍 Check in early at your accommodation and drop bags before heading out'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Erath Winery — Dundee Hills Pioneer',
              description: 'Dick Erath was a founding father of Oregon wine, planting the Dundee Hills in 1969 when everyone said Pinot couldn\'t grow here. Now owned by Ste. Michelle Wine Estates, the estate has one of the best panoramic views in the valley. The Dundee Hills Pinot Noir is a gateway to Oregon terroir.',
              details: [
                '🍷 Tastings from $25 — the Leland series Pinots are the standout',
                '📸 360° views of the valley from the tasting room terrace',
                '⏰ Open daily 11am–5pm, walk-ins welcome',
                '📍 9009 NE Worden Hill Rd, Dundee'
              ]
            },
            {
              title: 'Archery Summit — Minimalist Pinot Excellence',
              description: 'One of Willamette\'s most revered estate producers, Archery Summit practices nothing but Pinot Noir with near-monastic dedication. Their cave-carved winery on the hillside is an experience in itself — cool underground barrels aging some of Oregon\'s most sought-after juice.',
              details: [
                '🍷 Appointment preferred — book ahead via their website',
                '🍇 Estate-only, single-vineyard Pinots: Red Hills Estate, Archery Summit Estate',
                '🏚️ Underground cave aging facility — a visual highlight of any winery tour',
                '📍 18599 NE Archery Summit Rd, Dayton'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Dundee Hills Pinots tend toward elegance and red fruit — lighter than what most Americans expect from Pinot, closer to a premier cru Burgundy. Taste with an open mind.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Joel Palmer House',
              description: 'A Willamette Valley icon in Dayton — Jack Czarnecki (and now his son Chris) has been foraging wild Oregon mushrooms and pairing them with valley wines for decades. The three-course mushroom menu is a cultural ritual. There is nowhere else like it in the American wine country.',
              meta: '💰 $$$ · 📍 600 Ferry St, Dayton · Reservations strongly recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.2788, lng: -123.0099, label: 'Dundee', num: 1, cat: 'attraction', desc: 'Gateway to the Dundee Hills AVA — Oregon wine country epicenter' },
        { lat: 45.2802, lng: -123.0480, label: 'Erath Winery', num: 2, cat: 'attraction', desc: 'Pioneer Oregon winery with panoramic hilltop views' },
        { lat: 45.2779, lng: -123.0520, label: 'Archery Summit', num: 3, cat: 'attraction', desc: 'Estate Pinot Noir specialist with underground cave winery' },
        { lat: 45.2290, lng: -123.0570, label: 'The Joel Palmer House', num: 4, cat: 'food', desc: 'Legendary wild mushroom restaurant in Dayton' }
      ]
    },
    {
      num: 2,
      date: '2026-06-23',
      neighborhoods: 'McMinnville — Downtown & Evergreen',
      title: 'McMinnville Deep Dive — Aviation Legends & 3rd Street Culture',
      description: "McMinnville is the soul of Willamette Valley — a genuine small city with a walkable historic downtown, James Beard–recognized restaurants, independent bookshops and galleries, and one of the world's most extraordinary aviation museums. Give this day to the town itself.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Evergreen Aviation & Space Museum',
              description: 'One of the great museums in the American Northwest — home to Howard Hughes\'s HK-1 "Spruce Goose," the largest wooden aircraft ever built. The sheer scale of this flying boat (the wingspan is longer than a football field) is impossible to comprehend until you\'re standing under it. The adjacent Space Museum has an SR-71 Blackbird, a Titan II missile, and a full decommissioned Saturn V engine. Plan at least 2–3 hours.',
              details: [
                '✈️ The Spruce Goose flew only once (1947, 1 mile over Long Beach Harbor) — the largest flying boat ever',
                '🚀 Space Museum: SR-71 Blackbird, Titan II missile, and Moon rocks',
                '💰 $35 admission for both museums — one of the best value-per-wonder museums in Oregon',
                '⏰ Open daily 9am–5pm',
                '📍 500 NE Captain Michael King Smith Way, McMinnville'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Golden Valley Brewery & Pub',
              description: 'Right in downtown McMinnville — craft beer, classic pub food, and a lively local crowd. Order the pulled pork sandwich and a pint of their Red Thistle Ale.',
              meta: '💰 $ · 📍 980 NE 4th St, McMinnville'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '3rd Street Arts & Culture Walk',
              description: 'McMinnville\'s historic downtown 3rd Street is one of Oregon\'s finest small-city main streets — Victorian-era storefronts housing independent boutiques, wine bars, galleries, and bookshops. The Yamhill County Museum tells the story of the valley\'s Indigenous Kalapuya people and pioneer settlers. Browse the galleries, dip into Powell\'s-adjacent indie bookshops, and soak up the pace of Oregon wine country town life.',
              details: [
                '🏛️ Yamhill County Museum: open Tue–Sat 10am–4pm, free admission',
                '📚 Third Street Books: beloved local indie bookshop — pick up an Oregon-focused title',
                '🍷 Nick\'s Italian Café: an Oregon institution since 1977, order the house-made pasta',
                '🎨 Several rotating galleries along 3rd and 4th Streets worth ducking into'
              ]
            },
            {
              title: 'Brigittine Monks Monastery Visit',
              description: 'A 20-minute drive takes you to the Brigittine Monks of Our Lady of Consolation in Amity — a contemplative monastery where the monks produce world-class handcrafted fudge and truffles sold from a small shop. An unexpected, deeply peaceful cultural detour into monastic life in the Oregon wine country.',
              details: [
                '🍫 The truffles are genuinely excellent — made by Cistercian monks',
                '⛪ The chapel is open for quiet contemplation',
                '⏰ Shop open Mon–Sat 9am–5pm',
                '📍 23300 Walker Lane, Amity — 20 min from McMinnville'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Park on 3rd Street and walk everything — McMinnville\'s downtown is about 6 blocks of concentrated good stuff. The side streets have great murals too.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Thistle Restaurant',
              description: 'One of McMinnville\'s most acclaimed tables — chef Eric Bechard\'s farm-to-table menu changes daily with the best of what Yamhill County grows. The wine list is an education in Oregon terroir, weighted toward small-production local labels you won\'t find elsewhere.',
              meta: '💰 $$$ · 📍 228 NE Evans St, McMinnville · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.2218, lng: -123.2020, label: 'Evergreen Aviation & Space Museum', num: 1, cat: 'attraction', desc: 'Home of the Spruce Goose — largest wooden aircraft ever built' },
        { lat: 45.2101, lng: -123.1978, label: 'McMinnville Historic Downtown', num: 2, cat: 'attraction', desc: 'Walkable 3rd Street with galleries, bookshops, and wine bars' },
        { lat: 45.2089, lng: -123.1965, label: 'Yamhill County Museum', num: 3, cat: 'attraction', desc: 'Kalapuya and pioneer history of the valley' },
        { lat: 45.1170, lng: -123.3350, label: 'Brigittine Monks Monastery', num: 4, cat: 'attraction', desc: 'Contemplative monastery making world-class fudge and truffles' },
        { lat: 45.2115, lng: -123.1990, label: 'Thistle Restaurant', num: 5, cat: 'food', desc: 'Award-winning farm-to-table dining in McMinnville' }
      ]
    },
    {
      num: 3,
      date: '2026-06-24',
      neighborhoods: 'Chehalem Mountains · Ribbon Ridge · Ponzi Country',
      title: 'Biodynamic Estates & the Chehalem Mountain Trail',
      description: "Today's circuit traces the Chehalem Mountains AVA — a horseshoe of hills north of McMinnville with some of Oregon's oldest and most progressive estate wineries. Stoller runs on solar, Adelsheim was planted in 1971, and Domaine Drouhin brought Burgundy's terroir philosophy to Oregon soil in 1988.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Stoller Family Estate',
              description: 'A sweeping 373-acre estate in the Chehalem Mountains, Stoller was the first winery in America to achieve LEED Gold certification and runs entirely on solar power. The tasting room — all glass and Oregon timber — frames a 270° view of vine-covered slopes. Their Chardonnay is quietly exceptional.',
              details: [
                '☀️ America\'s first LEED Gold-certified winery — sustainability as a philosophy',
                '🍷 Reserve tasting ($45) highlights single-vineyard expressions of Pinot and Chardonnay',
                '📸 Floor-to-ceiling tasting room windows overlooking the entire estate',
                '⏰ Reservation recommended — open daily 11am–5pm',
                '📍 16161 NE McDougall Rd, Dayton'
              ]
            },
            {
              title: 'Adelsheim Vineyard — Oregon\'s Founding Estate',
              description: 'David Adelsheim planted his first vines in 1971, before there was an Oregon wine industry. This estate is living history — the spot where the Willamette Valley Pinot revolution began. Today the winery is known for both its Pinot Noir and its extraordinary advocacy for small growers across the valley.',
              details: [
                '🍇 One of Oregon\'s founding wineries — planted 1971',
                '🌿 Certified sustainable vineyard practices throughout',
                '🍷 Tastings from $30 — the Willamette Valley Pinot Noir is the starting point',
                '📍 16800 NE Calkins Ln, Newberg'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Chez Joly at Domaine Drouhin',
              description: 'Dine with a view of the vineyards at Domaine Drouhin\'s on-site café. Simple, elegant French-Oregon fare paired with DDO wines. The charcuterie board is outstanding.',
              meta: '💰 $$ · 📍 6750 NE Breyman Orchards Rd, Dayton · Open for lunch Fri–Sun'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Domaine Drouhin Oregon — Burgundy in the Willamette',
              description: 'When the Drouhin family of Beaune, Burgundy decided Oregon\'s Dundee Hills were producing wine worthy of their attention, it changed how the world saw American Pinot Noir. Their four-story gravity-flow winery is a masterpiece of architecture and winemaking philosophy. The Laurène Pinot Noir — named for winemaker Véronique Drouhin\'s daughter — is a benchmark of the region.',
              details: [
                '🇫🇷 Established 1988 by Robert Drouhin of Maison Joseph Drouhin, Burgundy',
                '🍷 Estate tasting ($55) — include the Arthur Chardonnay and Laurène Pinot',
                '🏗️ The four-story gravity-flow winery: no pumps, wine moves by gravity alone',
                '⏰ Appointment required — book online ahead of visit',
                '📍 6750 NE Breyman Orchards Rd, Dayton'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Chehalem Mountains run is a half-day circuit: Stoller → Adelsheim → Domaine Drouhin. All three are within 15 minutes of each other and represent Willamette\'s full arc from local pioneer to international prestige.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Jory Restaurant at The Allison Inn & Spa',
              description: 'The most elegant table in wine country — The Allison\'s kitchen-driven menu showcases Oregon\'s finest ingredients matched with an extensive Willamette Valley wine list. Chef Sunny Jin\'s Pacific Northwest cuisine is as good as anything in Portland, without the city noise.',
              meta: '💰 $$$$ · 📍 2525 Allison Ln, Newberg · Reservations required'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.2850, lng: -123.0542, label: 'Stoller Family Estate', num: 1, cat: 'attraction', desc: 'First LEED Gold winery in America — sweeping Chehalem Mountain views' },
        { lat: 45.3042, lng: -122.9892, label: 'Adelsheim Vineyard', num: 2, cat: 'attraction', desc: 'Oregon\'s founding estate, planted 1971' },
        { lat: 45.2737, lng: -123.0602, label: 'Domaine Drouhin Oregon', num: 3, cat: 'attraction', desc: 'Burgundy\'s Drouhin family brings terroir philosophy to Dundee Hills' },
        { lat: 45.3018, lng: -122.9870, label: 'The Allison Inn & Spa', num: 4, cat: 'food', desc: 'Jory Restaurant — finest wine country dining in Willamette Valley' }
      ]
    },
    {
      num: 4,
      date: '2026-06-25',
      neighborhoods: 'Salem · Grand Ronde · Eola-Amity Hills',
      title: 'Salem Heritage Day — Capitals, Missions & Indigenous Culture',
      description: "Today's drive south to Salem reveals Willamette Valley's deeper history — Oregon's state capital, the 1834 Methodist Mission that sparked the Oregon Trail, and the land of the Kalapuya, Molalla and other Indigenous peoples who have called this valley home for 8,000 years. Return to McMinnville in time for the celebrated Thursday Farmers' Market.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Oregon State Capitol & Capitol Mall',
              description: 'Salem\'s Art Deco state capitol building (1938) is one of the finest in America — topped by a 23-foot gold-leafed statue of the Oregon Pioneer. Take the free guided tour of the legislative chambers, murals, and the gold rotunda. The surrounding Capitol Mall is a beautiful lawn of Douglas firs.',
              details: [
                '🏛️ Free guided tours Mon–Fri 9am–4pm, Sat 9am–3pm',
                '🌟 The 23-foot Oregon Pioneer atop the dome is gilded in 24-karat gold leaf',
                '🎨 WPA-era murals inside depicting Oregon\'s settlement — stunning and historically rich',
                '📍 900 Court St NE, Salem'
              ]
            },
            {
              title: 'Willamette Heritage Center',
              description: 'A complex of 13 historic buildings in the heart of Salem — including Thomas Kay Woolen Mill (1895) and the Jason Lee Mission (1841). The Mission Mill Museum tells the story of how Oregon came to be settled: the missionaries, the Kalapuya displacement, the Oregon Trail, and the emergence of Oregon as a state. The water wheel still turns.',
              details: [
                '🏚️ 13 historic buildings on 5 acres — one of Oregon\'s best heritage sites',
                '🌊 The Thomas Kay Woolen Mill is fully restored with working water wheel',
                '📚 Excellent exhibits on Kalapuya culture and displacement',
                '⏰ Open Mon–Sat 10am–5pm; $12 admission',
                '📍 1313 Mill St SE, Salem'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Archive Coffee & Bar',
              description: 'Salem\'s beloved community café in a converted historic building — excellent sandwiches, house-roasted coffee, and a daily changing menu of local ingredients.',
              meta: '💰 $ · 📍 102 Liberty St NE, Salem'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Deepwood Estate & Gardens',
              description: 'An 1894 Queen Anne Victorian mansion set within 5 acres of formal English gardens — one of Salem\'s quiet gems. The Olmsted Brothers (of Central Park fame) designed the gardens in 1929. A peaceful afternoon exploration of Oregon\'s Gilded Age ambitions.',
              details: [
                '🌸 English-style formal gardens by the Olmsted Brothers landscape firm',
                '🏡 Free garden access; mansion tours $7',
                '🌿 Late June: roses, perennial borders, and mature specimen trees in full glory',
                '📍 1116 Mission St SE, Salem'
              ]
            },
            {
              title: 'Drive the Eola-Amity Hills on the return',
              description: 'The scenic route back to McMinnville passes through the Eola-Amity Hills AVA — a cooler sub-appellation where marine air funnels through the Van Duzer Corridor. Pull off at Cristom Vineyards or Bethel Heights for a late-afternoon tasting — both are walk-in friendly and have stunning sunset views.',
              details: [
                '🌬️ The Van Duzer Corridor: cool Pacific air that gives Eola Pinots their edge',
                '🍷 Bethel Heights: walk-in tastings, outstanding estate Pinot since 1984',
                '🍷 Cristom Vineyards: biodynamic, single-vineyard Pinots named for members of the Gerrie family',
                '📍 Route: Salem → OR-22W → S Bethel Rd → McMinnville'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'McMinnville Thursday Farmers\' Market',
              description: 'Every Thursday evening (5–8pm), McMinnville\'s downtown fills with 60+ vendors selling local produce, artisan cheese, Willamette Valley wine, Oregon hazelnut confections, fresh flowers, and hand-crafted goods. This is the community soul of wine country — join locals shopping for dinner ingredients and tasting wines from small producers who don\'t have tasting rooms.',
              details: [
                '🌽 60+ vendors: farm produce, artisan cheese, meat, flowers, wine',
                '🍷 Several small winemakers pour here — some bottles you can\'t get at wineries',
                '🌸 June is peak flower season — incredible lavender, dahlias, and summer blooms',
                '📍 3rd & Davis St, McMinnville · Every Thursday 5–8pm (May–Oct)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bistro Maison',
              description: 'James Beard Award semifinalist Jean-Jacques Chatelard\'s French bistro on 3rd Street — a genuine Alsatian kitchen in Oregon wine country. The duck confit and the choucroute garnie are the benchmarks. The all-Oregon wine list is one of the best curated lists in the region.',
              meta: '💰 $$$ · 📍 729 NE 3rd St, McMinnville · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 44.9389, lng: -123.0297, label: 'Oregon State Capitol', num: 1, cat: 'attraction', desc: 'Art Deco state capitol with gold-leafed Oregon Pioneer statue' },
        { lat: 44.9354, lng: -123.0380, label: 'Willamette Heritage Center', num: 2, cat: 'attraction', desc: '13 historic buildings including Thomas Kay Mill and Jason Lee Mission' },
        { lat: 44.9301, lng: -123.0450, label: 'Deepwood Estate', num: 3, cat: 'attraction', desc: '1894 Victorian mansion with Olmsted-designed English gardens' },
        { lat: 44.9858, lng: -123.1876, label: 'Bethel Heights Vineyard', num: 4, cat: 'attraction', desc: 'Eola-Amity Hills estate Pinot since 1984, walk-in tastings' },
        { lat: 45.2095, lng: -123.1972, label: 'McMinnville Farmers\' Market', num: 5, cat: 'attraction', desc: 'Thursday evening market — 60+ local vendors, wine, produce' }
      ]
    },
    {
      num: 5,
      date: '2026-06-26',
      neighborhoods: 'Carlton · Yamhill · Sokol Blosser · Lavender Country',
      title: 'Carlton Wine Village, Lavender Fields & a Farewell Toast',
      description: "A final golden day through Willamette Valley's quietest and most charming corners — the wine village of Carlton with its artisan producers, Sokol Blosser's biodynamic estate on the Dundee Hills, and a visit to one of Yamhill County's lavender farms at peak bloom. Late June is the best time to see these purple fields in their full glory.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Carlton — Oregon\'s Wine Village',
              description: 'Carlton is a one-street wine village where some of Oregon\'s most ambitious small producers have set up tasting rooms in historic storefronts. The Carlton Winemakers Studio houses eight different winemakers under one roof — a remarkable opportunity to taste eight perspectives on the same AVA side by side.',
              details: [
                '🍷 Carlton Winemakers Studio: 8 winemakers, one address — open daily 11am–5pm',
                '🍷 Retour Wines: elegant négociant Burgundy-style Pinots in a cozy space',
                '🛍️ The Carlton village feel is intimate and unhurried — no tour buses, just real wine lovers',
                '📍 Carlton: 15 min north of McMinnville on OR-47'
              ]
            },
            {
              title: 'Ponzi Vineyards — The Family That Shaped Oregon Wine',
              description: 'Dick and Nancy Ponzi planted their first vineyard in 1969 alongside the Ereths — two families who collectively invented the Oregon wine industry. Now run by the second generation, Ponzi is a living piece of Oregon viticulture history. The hilltop tasting room overlooks the Chehalem Valley.',
              details: [
                '🍇 Established 1969 — one of Oregon\'s founding families',
                '🍷 The Pinot Gris is Oregon\'s most celebrated white wine — try it here at the source',
                '🌿 Chehalem Mountains estate with sweeping valley views',
                '📍 19500 SW Mountain Home Rd, Sherwood (Chehalem Mountains)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Carlton Farms Meat & Charcuterie',
              description: 'Carlton\'s celebrated butcher shop and charcuterie counter — build a picnic spread from local cured meats, artisan cheese, and Oregon hazelnuts. Pair with a bottle from the Winemakers Studio tasting and find a vineyard with picnic tables.',
              meta: '💰 $ · 📍 Carlton Village · Takeaway for vineyard picnic'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sokol Blosser Winery — Biodynamic Pioneers',
              description: 'Founded in 1971, Sokol Blosser was among the first certified biodynamic wineries in Oregon. The tasting room — built into the hillside with a sod roof — is a statement of their relationship to the land. The Evolution White (a nine-variety blend) has introduced more people to Oregon wine than any other bottle.',
              details: [
                '🌿 Demeter-certified biodynamic since 2014',
                '🏗️ Sod-roofed tasting room built into the hillside — architecture and philosophy aligned',
                '🍷 Evolution wines: approachable, fun intro to Oregon blending',
                '🍷 Estate Pinot Noirs for the serious side of the visit',
                '📍 5000 NE Sokol Blosser Ln, Dayton'
              ]
            },
            {
              title: 'Lavender Valley Farm — Peak Bloom',
              description: 'June 22–27 is the height of lavender season in Yamhill County. Lavender Valley Farm near Carlton opens for u-pick lavender each summer — walking through rows of intensely fragrant purple in the warm Oregon afternoon light is one of those simple, transcendent experiences. The farm also sells handcrafted lavender products.',
              details: [
                '💜 Late June = peak lavender bloom — the fields are fully purple and intensely fragrant',
                '✂️ U-pick lavender bundles: ~$10 for a generous bunch',
                '🛍️ Farm shop sells lavender honey, sachets, and essential oil',
                '⏰ Open daily during bloom season, typically 10am–5pm (call ahead)',
                '📍 Lavender farms cluster around Carlton and Yamhill — search "Yamhill County lavender u-pick"'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'June 26 is a Friday — wineries will be busier than the early-week days. Sokol Blosser takes reservations; book ahead to secure your preferred time slot.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Toast at a Chehalem Hilltop',
              description: 'End your Willamette Valley journey with a bottle purchased from a local winery and a sunset view from the Chehalem ridge. The hills look west toward the Coast Range and the valley glows gold. In late June, the sun sets around 8:58pm. This is your Oregon wine country moment.',
              details: [
                '🌅 Sunset: ~8:58pm on June 26 in Yamhill County',
                '🍷 Buy a bottle to go from any winery — ask for something "to drink tonight"',
                '📸 Worden Hill Road viewpoint or any Dundee Hills roadside pullout',
                '🕊️ Quiet, beautiful, and entirely free — the best ending'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Community Plate',
              description: 'McMinnville\'s neighborhood farm-to-table restaurant — unpretentious, seasonal, and genuinely wonderful. Chef Mike Langlois sources everything from within 50 miles and the menu changes weekly. An honest, perfect farewell dinner that tastes like Willamette Valley itself.',
              meta: '💰 $$ · 📍 315 NE 3rd St, McMinnville · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.2935, lng: -123.1756, label: 'Carlton Winemakers Studio', num: 1, cat: 'attraction', desc: '8 Oregon winemakers under one roof in Carlton village' },
        { lat: 45.3680, lng: -122.9570, label: 'Ponzi Vineyards', num: 2, cat: 'attraction', desc: 'Oregon founding family vineyard since 1969 — Chehalem Mountains' },
        { lat: 45.2740, lng: -123.0820, label: 'Sokol Blosser Winery', num: 3, cat: 'attraction', desc: 'Biodynamic pioneer with sod-roofed hillside tasting room' },
        { lat: 45.2950, lng: -123.1800, label: 'Lavender Valley Farm Area', num: 4, cat: 'attraction', desc: 'Yamhill County lavender farms at peak bloom — u-pick in late June' },
        { lat: 45.2802, lng: -123.0480, label: 'Chehalem Ridge Sunset Viewpoint', num: 5, cat: 'attraction', desc: 'Best valley sunset views — golden hour at 8:58pm in late June' },
        { lat: 45.2097, lng: -123.1975, label: 'Community Plate', num: 6, cat: 'food', desc: 'Farm-to-table farewell dinner — everything sourced within 50 miles' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–120/night (motel/guesthouse)', midrange: '$150–250/night', luxury: '$350–600/night (The Allison)' },
    { category: 'Meals (solo)', budget: '$25–45/day', midrange: '$60–100/day', luxury: '$150–250/day' },
    { category: 'Car Rental (PDX)', budget: '$35–55/day economy', midrange: '$60–90/day', luxury: '$100–160/day' },
    { category: 'Winery Tastings', budget: '$25–35 per winery', midrange: '$40–65 per winery', luxury: '$75–120 (private tours)' },
    { category: 'Activities & Museums', budget: '$35–60/day (Evergreen + heritage)', midrange: '$60–90/day', luxury: '$100–180/day (spa, private tours)' },
    { category: '5-Day Total (solo)', budget: '$800–1,200', midrange: '$1,500–2,500', luxury: '$3,000–5,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Portland International Airport (PDX) — the closest major hub', 'Dundee Hills are 45 min; McMinnville is 65 min from PDX via OR-99W', 'Rent a car at the airport — essential for winery touring', 'Amtrak Cascades stops in Salem and Portland; wine country itself requires a car'] },
    { title: '🏨 Where to Stay', items: ['The Allison Inn & Spa (Newberg) — the luxury benchmark of wine country ($350+)', 'McMinnville motels on OR-99W: convenient and affordable ($80–150)', 'Youngberg Hill Vineyard & Inn — romantic hilltop B&B in the vines (~$275)', 'Newberg and Carlton B&Bs for a more intimate wine country experience'] },
    { title: '🌡️ Late June Weather', items: ['Average highs 22–28°C (72–82°F), low humidity compared to East Coast', 'Long daylight: sunrise ~5:30am, sunset ~9pm', 'Mornings can be misty/cool in the hills — perfect for early vineyard walks', 'Sunscreen essential; Oregon UV can surprise at altitude'] },
    { title: '💳 Money & Reservations', items: ['Cards widely accepted; keep $50 cash for farmers\' market and small farms', 'Book popular tasting rooms (Domaine Drouhin, Archery Summit, The Allison) 1–2 weeks ahead', 'Winery tasting fees: $25–55; often refunded with purchase', 'Eating out: plan $60–100/day for full sit-down meals'] },
    { title: '📱 Practical Notes', items: ['Download offline maps — vineyard roads can be spotty for signal', 'Oregon wine country is very solo-traveler friendly — wine bars and tasting rooms welcome singles', 'Many wineries allow BYOP (bring your own picnic) — ask ahead', 'June is busy but not peak harvest crowds — you\'ll have space and attention'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
