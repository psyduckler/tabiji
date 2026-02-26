const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771972388001_bumqyt',
  email: 'bernard@clearscope.io',
  destination: 'Yerevan, Armenia',
  start_date: '2026-02-26',
  end_date: '2026-03-01',
  startDate: '2026-02-26',
  endDate: '2026-03-01',
  groupSize: '3-4',
  budget: '$0.00',
  requests: 'Nightlife, Family-friendly'
};

const itineraryData = {
  destination: 'Yerevan, Armenia',
  countryEmoji: '🇦🇲',
  title: 'Pink City After Dark — Yerevan with Family & Nightlife',
  subtitle: '3 nights of ancient culture by day, craft cocktails by night in the world\'s oldest capital',
  description: 'Yerevan is a city of contradictions that somehow all make sense. By day it\'s a family paradise — open-air cafés, the magnificent Cascade art complex, sprawling parks, and day trips to temples older than Rome. By night it transforms into one of the Caucasus\'s best-kept nightlife secrets: underground wine bars, rooftop cocktail lounges overlooking Mount Ararat, and a jazz scene that punches absurdly above its weight. Built from pink volcanic tuff stone that glows amber at sunset, Yerevan feels simultaneously ancient and brand new. Your 3-night trip threads both worlds together — mornings at Garni Temple and Geghard Monastery with the family, evenings in the bars and clubs of the Northern Avenue and Saryan Street wine district. Late February means crisp winter air, snow-dusted Ararat on the horizon, and a city that\'s cozy, affordable, and wonderfully uncrowded.',
  duration: '3 nights',
  dates: 'Feb 26 – Mar 1, 2026',
  budget: '$',
  pace: 'Balanced',
  bestFor: 'Families, Nightlife Lovers, Culture & History',
  highlights: [
    'Cascade Complex — monumental stairway of contemporary art with panoramic city views',
    'Garni Temple & Geghard Monastery day trip — pagan temple + UNESCO cave monastery',
    'Saryan Street wine bars — Armenia\'s legendary wine culture in one buzzing block',
    'Republic Square at night — fountains, illuminated Soviet-era architecture, café culture',
    'Vernissage open-air market — handcrafted souvenirs, chess sets, carpets, and curiosities',
    'Mezzo Classic House — Yerevan\'s iconic jazz and live music venue',
    'Armenian cuisine deep dive — lavash, khorovats, dolma, and pomegranate everything',
    'Mount Ararat views from every rooftop bar — the sacred mountain just across the border'
  ],
  essentials: [
    {
      title: '✈️ Getting There',
      text: 'Fly into Zvartnots International Airport (EVN), 12 km west of central Yerevan. Direct flights from Dubai, Istanbul, Moscow, Vienna, and many European hubs. A taxi to the city centre costs ~3,000–4,000 AMD ($8–10) or use the airport shuttle bus. Visa-free for most nationalities (US, EU, UK, etc.) for up to 180 days.'
    },
    {
      title: '💰 Money & Costs',
      text: 'Armenian Dram (AMD): ~390 AMD = $1 USD. Yerevan is extraordinarily affordable. A full dinner with wine for four: $40–60. Craft cocktails: $4–6. Museum entry: $2–5. Taxis across the city: $2–4. ATMs are everywhere; cards accepted at most restaurants and bars. Budget for the whole trip (excluding flights): $300–500 for a group of 3–4.'
    },
    {
      title: '🌡️ Weather in Late February',
      text: 'Late February in Yerevan is cold but manageable: daytime highs around 5–10°C (41–50°F), nights dropping to -3 to 2°C (27–36°F). Dress in layers. Snow is possible but not guaranteed. The air is dry and crisp. Mount Ararat will be fully snow-capped and spectacular. Indoor heating is excellent everywhere.'
    },
    {
      title: '👨‍👩‍👧‍👦 Family-Friendly Notes',
      text: 'Armenians adore children — expect your kids to be welcomed warmly everywhere, including restaurants late at night (dinner at 9 PM with kids is completely normal here). The Cascade complex, parks, and GUM Market are all excellent for families. Most museums are interactive enough for older kids. Yerevan is very safe and walkable.'
    },
    {
      title: '🍷 Nightlife Overview',
      text: 'Yerevan\'s nightlife centres on a few key zones: Saryan Street (wine bars, craft cocktails), Northern Avenue (upscale lounges), and the Cascade area (rooftop bars). The scene starts late — dinner at 8–9 PM, bars from 10 PM, clubs from midnight. Mezzo Classic House is the legendary jazz venue. Paparazzi Club and Kami Club are the main dance clubs. The vibe is sophisticated, friendly, and remarkably affordable.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-26',
      neighborhoods: 'Republic Square · Northern Avenue · Saryan Street',
      title: 'Arrival — Pink Stone, First Impressions & Saryan Street by Night',
      description: 'Land in Yerevan, settle into your hotel near Republic Square, and get your bearings in this compact, walkable city. The afternoon is for the iconic sights within walking distance — Republic Square, the History Museum, and a stroll up Northern Avenue. As evening falls, Yerevan\'s nightlife awakens on Saryan Street, where a block of wine bars pours Armenia\'s extraordinary wines late into the night.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Republic Square — The Heart of Yerevan',
              description: 'Start at Republic Square, the grand Soviet-era plaza ringed by pink tuff buildings that define Yerevan\'s aesthetic. The History Museum of Armenia anchors one side (excellent for kids — Urartian artefacts, ancient armour, and the world\'s oldest leather shoe from 3500 BC). In winter the square is quieter than summer but no less beautiful — the buildings glow in the low afternoon light.',
              details: [
                '🏛️ History Museum: open Tue–Sun 11 AM–5:30 PM, entry ~2,000 AMD ($5). Allow 1.5 hours',
                '👟 The Areni-1 shoe (3500 BC) — the world\'s oldest leather shoe, found in a cave — mesmerises kids',
                '⛲ The musical fountains run in summer only, but the square\'s architecture is stunning year-round',
                '📸 Best photo angle: from the corner near the Marriott, capturing the full sweep of the government buildings'
              ]
            },
            {
              title: 'Northern Avenue Stroll',
              description: 'Walk the pedestrianised Northern Avenue — Yerevan\'s most elegant boulevard connecting Republic Square to the Opera House. Lined with upscale cafés, boutiques, and gelato shops, it\'s a perfect family promenade. Kids will enjoy the street performers and the open feel.',
              details: [
                '🛍️ Window shopping: Armenian jewellery, obsidian crafts, and pomegranate-themed everything',
                '🍦 Jazzve Café for hot chocolate — perfect winter warm-up for the family',
                '🎭 The Opera House at the far end is a beautiful Soviet-Armenian landmark'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Late Lunch',
              name: 'Lavash Restaurant',
              description: 'Traditional Armenian cuisine in a warm, family-friendly setting near Republic Square. Try the lavash bread baked in a tonir (underground clay oven), cheese-stuffed jingalov hats, and khorovats (Armenian BBQ). Kids love watching the lavash being made.',
              meta: '💰 8,000–15,000 AMD ($20–38) for the group · 📍 Northern Avenue area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Saryan Street Wine District — Armenia\'s Wine Revolution',
              description: 'After the kids are settled (or bring them — Armenians don\'t bat an eye), head to Saryan Street — a single block that\'s become the epicentre of Armenia\'s booming wine scene. Armenia has 6,000 years of winemaking history (the oldest known winery was found in the Areni-1 cave), and the new generation of winemakers is producing extraordinary natural wines. Bar hop between In Vino, Wine Republic, and Stoyka for tastings.',
              details: [
                '🍷 In Vino: the original Saryan wine bar — excellent Armenian wine flights, knowledgeable staff',
                '🍷 Wine Republic: broader selection, great cheese boards, lively atmosphere',
                '🍷 Stoyka: standing-room wine bar, younger crowd, natural wines, very cool vibe',
                '💰 Wine tastings: 3,000–5,000 AMD ($8–13) for a flight of 4–5 wines',
                '🧀 Armenian cheeses pair beautifully — try chechil (braided string cheese) and lori'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sherep Restaurant',
              description: 'Modern Armenian cuisine with a creative twist, one block from Saryan Street. Excellent pomegranate salads, lamb dishes, and a wine list showcasing the best Armenian producers. Warm atmosphere, family-friendly until about 10 PM, then transitions to a more bar-like vibe.',
              meta: '💰 15,000–25,000 AMD ($38–65) for the group · 📍 Amiryan Street'
            }
          ],
          tips: [
            { type: 'tip', text: 'Armenian wine is the country\'s best-kept secret. The Areni grape (indigenous, only grows here) produces reds with a Pinot Noir-like elegance. Ask for Areni Noir at any wine bar — you\'ll be amazed.' }
          ]
        }
      ],
      mapPins: [
        { lat: 40.1776, lng: 44.5126, label: 'Republic Square', num: 1, cat: 'attraction', desc: 'Grand central plaza — pink tuff architecture, History Museum, fountains' },
        { lat: 40.1830, lng: 44.5100, label: 'Northern Avenue', num: 2, cat: 'attraction', desc: 'Elegant pedestrian boulevard — cafés, boutiques, street performers' },
        { lat: 40.1850, lng: 44.5070, label: 'Opera House', num: 3, cat: 'attraction', desc: 'Soviet-Armenian landmark — concerts and ballet performances' },
        { lat: 40.1870, lng: 44.5080, label: 'Saryan Street Wine District', num: 4, cat: 'nightlife', desc: 'Block of wine bars — In Vino, Wine Republic, Stoyka' },
        { lat: 40.1810, lng: 44.5130, label: 'Lavash Restaurant', num: 5, cat: 'food', desc: 'Traditional Armenian cuisine — lavash baked in tonir oven' },
        { lat: 40.1845, lng: 44.5105, label: 'Sherep Restaurant', num: 6, cat: 'food', desc: 'Modern Armenian — pomegranate salads, lamb, great wine list' }
      ]
    },
    {
      num: 2,
      date: '2026-02-27',
      neighborhoods: 'Garni · Geghard · Symphony of Stones · Cascade',
      title: 'Temples, Caves & Cascades — Then Jazz After Dark',
      description: 'The day trip that justifies the entire visit. Drive 30 km east to the Garni Temple — a Greco-Roman pagan temple perched on a gorge that predates Christianity in Armenia — then continue to the UNESCO-listed Geghard Monastery, partly carved into the living rock of a cliff. On the way back, stop at the Symphony of Stones basalt columns. Evening: the Cascade complex at sunset, then Mezzo Classic House for world-class jazz.',
      timeBlocks: [
        {
          label: 'Morning (9 AM departure)',
          activities: [
            {
              title: 'Garni Temple — Armenia\'s Greco-Roman Jewel',
              description: 'Drive 30 minutes east to the village of Garni, where a 1st-century Hellenistic temple stands on the edge of the Azat River gorge. Built by King Trdat I in 77 AD and dedicated to the sun god Mihr, it\'s the only standing Greco-Roman colonnaded building in the former Soviet Union. The gorge below reveals the incredible Symphony of Stones — hexagonal basalt columns formed by volcanic cooling.',
              details: [
                '🏛️ Entry: 1,500 AMD ($4). Open daily 9 AM–6 PM (winter hours may be shorter)',
                '👨‍👩‍👧‍👦 Kids love the gorge viewpoint — dramatic drop with the river far below',
                '📸 Best photos: from the southeast, capturing the temple columns against the gorge',
                '🌋 Symphony of Stones: accessible via a short trail from the temple — stunning hexagonal basalt'
              ]
            },
            {
              title: 'Symphony of Stones — Nature\'s Organ Pipes',
              description: 'Hike down (or drive to the lower viewpoint) to see the Symphony of Stones — towering hexagonal basalt columns that look like a giant pipe organ carved into the cliff face. Formed by volcanic lava cooling in geometric perfection. Kids are fascinated by the science; photographers by the scale.',
              details: [
                '🪨 The columns are 50+ metres tall and perfectly hexagonal — like Giant\'s Causeway but vertical',
                '🥾 Trail from Garni: 15–20 minutes down (steep in places, watch footing in winter)',
                '📸 The river at the base reflects the columns beautifully in the morning light'
              ]
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Geghard Monastery — Carved from the Mountain',
              description: 'Continue 9 km to Geghard Monastery (UNESCO World Heritage Site), a 4th-century monastic complex partly carved into the cliff face. The acoustics inside the rock-hewn chapels are otherworldly — if you\'re lucky, a small choir will be singing Armenian sacred music inside. The name means "Spear" — it once housed the spear that pierced Christ\'s side, now in Echmiadzin.',
              details: [
                '⛪ Entry: free. Open daily 8 AM–6 PM',
                '🎵 The acoustics: stand in the main rock-hewn chapel and listen to the echo — goosebumps guaranteed',
                '🕯️ Light a candle in the khachkar-lined courtyard — a moving experience even for non-believers',
                '👨‍👩‍👧‍👦 Kids: the cave chambers and secret passages are genuinely exciting to explore',
                '🍞 Local women sell gata (sweet Armenian pastry) and dried fruit at the entrance — buy some'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Garni Village Restaurant',
              description: 'Stop at one of the family-run restaurants in Garni village for lavash baked in a tonir, herb-stuffed tolma (grape leaf dolma), and grilled pork khorovats. Many restaurants let you watch the lavash being prepared — a performance in itself.',
              meta: '💰 10,000–18,000 AMD ($25–46) for the group · 📍 Garni village'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Cascade — Art, Views & Mount Ararat',
              description: 'Back in Yerevan, head to the Cascade — a monumental limestone stairway and outdoor art gallery climbing up a hillside in central Yerevan. Inside the Cascade is the Cafesjian Center for the Arts (contemporary sculpture and art). From the top, on a clear day, Mount Ararat fills the horizon — snow-capped, impossibly close, impossibly beautiful. Kids can run up and down the steps; adults can take the escalator inside.',
              details: [
                '🎨 Cafesjian Center: free entry to outdoor sculptures; museum inside 1,000 AMD ($2.50)',
                '🗿 Outdoor art includes a Fernando Botero cat sculpture — kids\' favourite photo spot',
                '🏔️ Mount Ararat view from the top is the quintessential Yerevan moment',
                '📸 Sunset light on the Cascade steps is magical — arrive by 4:30 PM in winter',
                '☕ Café at the top has excellent coffee and the best panorama in the city'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Mezzo Classic House — Jazz in the Pink City',
              description: 'Yerevan\'s legendary live music venue. Mezzo hosts world-class jazz, classical, and fusion performances nightly in an intimate, elegant setting. The cocktails are excellent, the acoustics perfect, and the atmosphere is pure Yerevan sophistication. Book a table in advance — it fills up, even in winter.',
              details: [
                '🎵 Shows typically start at 9–9:30 PM. Arrive by 8:30 PM for good seats',
                '🍸 Cocktail menu: try the Armenian-twist cocktails with pomegranate and apricot',
                '💰 No cover charge; cocktails 3,000–5,000 AMD ($8–13)',
                '📍 2 Mashtots Avenue — easy walk from the Cascade',
                '🎶 Music ranges from jazz quartet to Armenian folk-jazz fusion — always excellent'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dolmama Restaurant',
              description: 'One of Yerevan\'s most celebrated restaurants — Armenian fine dining without pretension. The dolma (stuffed grape leaves, the restaurant\'s namesake) is legendary. Excellent wine pairings. Warm, candlelit atmosphere perfect for a special evening.',
              meta: '💰 20,000–35,000 AMD ($50–90) for the group · 📍 Pushkin Street'
            }
          ],
          tips: [
            { type: 'tip', text: 'If the group splits for nightlife — one parent stays with kids while the other hits the bars — the Cascade area is ideal. Plenty of rooftop bars within walking distance of family-friendly hotels.' }
          ]
        }
      ],
      mapPins: [
        { lat: 40.1121, lng: 44.7310, label: 'Garni Temple', num: 1, cat: 'attraction', desc: '1st-century Greco-Roman temple on a dramatic gorge — Armenia\'s icon' },
        { lat: 40.1100, lng: 44.7280, label: 'Symphony of Stones', num: 2, cat: 'attraction', desc: 'Hexagonal basalt columns in the Azat River gorge — volcanic marvel' },
        { lat: 40.1405, lng: 44.8178, label: 'Geghard Monastery', num: 3, cat: 'attraction', desc: 'UNESCO site — 4th-century monastery carved into the cliff, extraordinary acoustics' },
        { lat: 40.1919, lng: 44.5156, label: 'Cascade Complex', num: 4, cat: 'attraction', desc: 'Monumental stairway, outdoor art, and the best Mount Ararat panorama' },
        { lat: 40.1880, lng: 44.5090, label: 'Mezzo Classic House', num: 5, cat: 'nightlife', desc: 'Legendary jazz venue — nightly live performances, excellent cocktails' },
        { lat: 40.1835, lng: 44.5130, label: 'Dolmama Restaurant', num: 6, cat: 'food', desc: 'Armenian fine dining — famous dolma, candlelit atmosphere' }
      ]
    },
    {
      num: 3,
      date: '2026-02-28',
      neighborhoods: 'Kond · GUM Market · Vernissage · Blue Mosque · Hrazdan Gorge',
      title: 'Markets, Hidden Quarters & the Final Night Out',
      description: 'Your last full day explores the Yerevan the tourists miss — the ancient Kond neighbourhood with its winding lanes and crumbling stone houses, the sensory overload of GUM Market, and the treasure-hunt of Vernissage flea market. Afternoon: the serene Blue Mosque and Hrazdan Gorge for a family walk. Night: go all out on Yerevan\'s cocktail and club scene for a proper send-off.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'GUM Market — Armenia in Every Stall',
              description: 'Yerevan\'s covered central market is a sensory explosion: mountains of dried fruits and churchkhela (walnut-stuffed grape candy), barrels of spices, wheels of cheese, jars of honey, and vendors offering endless samples. This is Armenia\'s larder, and it\'s magnificent. Kids get to taste everything; adults get to buy everything.',
              details: [
                '🍯 Must-try: Armenian honey varieties — wildflower, mountain, and the rare alpine honey',
                '🍬 Churchkhela: grape juice and walnut "candles" — the original energy bar, 2,000+ years old',
                '🧀 Lori cheese: semi-hard, slightly tangy, incredible with dried apricots',
                '💰 Budget 5,000–10,000 AMD ($13–25) for a haul of dried fruits, spices, and sweets',
                '📍 Mesrop Mashtots Avenue — open daily 8 AM–7 PM'
              ]
            },
            {
              title: 'Vernissage Open-Air Market',
              description: 'Adjacent to Republic Square, Vernissage is Yerevan\'s legendary weekend flea and craft market. Handmade chess sets, Soviet memorabilia, Armenian carpets, obsidian jewellery, hand-painted ceramics, and backgammon boards cover hundreds of stalls. Bargaining is expected and fun.',
              details: [
                '♟️ Hand-carved chess and backgammon sets — the signature souvenir, $15–50',
                '🖼️ Armenian miniature paintings on stone — unique, lightweight souvenirs',
                '📍 Open weekends (Sat–Sun) primarily, but some stalls operate daily',
                '👨‍👩‍👧‍👦 Kids love the toy stalls and the treasure-hunt atmosphere'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Artbridge Bookstore Café',
              description: 'A bookshop-café hybrid near the Opera House with excellent coffee, Armenian pastries (gata, nazook), and a cozy literary atmosphere. Great for a slow family morning.',
              meta: '💰 4,000–8,000 AMD ($10–20) for the group · 📍 Abovyan Street'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Kond — Yerevan\'s Oldest Neighbourhood',
              description: 'Kond is a hidden world within Yerevan — a hilltop tangle of narrow stone lanes, 18th-century houses, and courtyard gardens that has somehow survived Soviet-era demolition and modern development. It\'s atmospheric, slightly crumbling, and utterly authentic. Walk the lanes, peer into courtyards, and imagine Yerevan before the Soviet grid was imposed.',
              details: [
                '🏘️ The oldest houses date to the 1700s — thick stone walls, wooden balconies, grapevine-covered courtyards',
                '📸 Photogenic at every turn — the patina of old Yerevan against the modern city skyline',
                '⚠️ Some lanes are steep and uneven — not ideal for strollers',
                '🐈 Yerevan\'s cat population is concentrated here — kids will love the neighbourhood cats'
              ]
            },
            {
              title: 'Blue Mosque — Yerevan\'s Persian Heritage',
              description: 'The 18th-century Blue Mosque is Yerevan\'s only surviving mosque — a beautifully restored Persian-era structure with a turquoise-tiled dome, peaceful courtyard garden, and an excellent exhibition on Armenian-Iranian cultural connections. A reminder that Yerevan was once part of the Persian world.',
              details: [
                '🕌 Entry: free. Open daily 10 AM–6 PM. Respectful dress required.',
                '💙 The turquoise tilework dome and minaret are stunning against winter sky',
                '📚 Small museum inside on Armenian-Iranian cultural exchange — fascinating for history buffs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Pandok Yerevan (Tumanyan Street)',
              description: 'Rustic Armenian tavern atmosphere with hearty winter-perfect food: khash (traditional winter bone broth), spas (yogurt soup), and massive khorovats platters. Live folk music on weekends. Very family-friendly — big portions, warm service.',
              meta: '💰 12,000–20,000 AMD ($30–50) for the group · 📍 Tumanyan Street'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hrazdan Gorge Walk & Children\'s Railway',
              description: 'The Hrazdan River gorge cuts through central Yerevan — a surprising natural canyon in the middle of the city with walking paths along the river. In winter the bare trees and rocky gorge have a stark beauty. The Soviet-era Children\'s Railway (a miniature railway operated by children, running seasonally) may not be operating in February, but the gorge walk itself is lovely.',
              details: [
                '🌉 Access from Victory Bridge or Kievyan Bridge — both have paths down to the gorge',
                '🥾 Allow 45–60 minutes for a gentle walk along the river',
                '👨‍👩‍👧‍👦 Safe, flat paths suitable for families — the gorge walls are dramatic and photogenic'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Night Out — Rooftop Cocktails & Yerevan After Dark',
              description: 'Your last night in Yerevan calls for the full treatment. Start with rooftop cocktails at The Loft (13th floor of the Tufenkian Hotel, overlooking the Cascade), then move to Calumet Ethnic Lounge for creative cocktails in a bohemian setting. If the energy is right, finish at Paparazzi Club or Kami Club for dancing until the early hours.',
              details: [
                '🍸 The Loft: rooftop bar with Ararat views, sophisticated cocktails, 4,000–6,000 AMD ($10–15)',
                '🍹 Calumet Ethnic Lounge: Abovyan Street — bohemian vibe, world music, creative cocktails',
                '💃 Paparazzi Club: Yerevan\'s biggest nightclub — EDM, hip-hop, packed weekends',
                '🎵 Kami Club: more intimate, better music curation, strong cocktails',
                '⏰ Clubs peak around 1–2 AM. Dress code: smart casual (no shorts/sandals)',
                '🚕 GG Taxi app for safe rides home — Yerevan is very safe but taxis are cheap and easy'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Caucasus Tavern',
              description: 'Grand Armenian feast in a traditional tavern setting. Order the family-style spread: cheese platters, herb salads, khorovats (BBQ), ghapama (stuffed pumpkin, if in season), and Armenian brandy for a toast. Live duduk (Armenian oboe) music most evenings — hauntingly beautiful.',
              meta: '💰 20,000–30,000 AMD ($50–75) for the group · 📍 Hanrapetutyan Street'
            }
          ],
          tips: [
            { type: 'tip', text: 'Armenian brandy (konyak) is world-famous — Churchill allegedly said he preferred it to French cognac. Order a glass of Ararat 10-year at any bar. It\'s exceptional and costs a fraction of comparable French brandy.' }
          ]
        }
      ],
      mapPins: [
        { lat: 40.1800, lng: 44.5060, label: 'GUM Market', num: 1, cat: 'attraction', desc: 'Covered central market — dried fruits, spices, honey, churchkhela' },
        { lat: 40.1770, lng: 44.5140, label: 'Vernissage Market', num: 2, cat: 'attraction', desc: 'Legendary flea market — chess sets, carpets, Soviet memorabilia' },
        { lat: 40.1820, lng: 44.5030, label: 'Kond Neighbourhood', num: 3, cat: 'attraction', desc: 'Oldest quarter — 18th-century stone lanes, grapevine courtyards' },
        { lat: 40.1760, lng: 44.5080, label: 'Blue Mosque', num: 4, cat: 'attraction', desc: '18th-century Persian mosque — turquoise dome, peaceful garden' },
        { lat: 40.1950, lng: 44.5050, label: 'Hrazdan Gorge', num: 5, cat: 'attraction', desc: 'Urban canyon walk — river paths, dramatic gorge walls' },
        { lat: 40.1920, lng: 44.5155, label: 'The Loft Rooftop Bar', num: 6, cat: 'nightlife', desc: 'Rooftop cocktails with Cascade and Ararat views' },
        { lat: 40.1825, lng: 44.5120, label: 'Calumet Ethnic Lounge', num: 7, cat: 'nightlife', desc: 'Bohemian cocktail bar — world music, creative drinks' },
        { lat: 40.1815, lng: 44.5095, label: 'Caucasus Tavern', num: 8, cat: 'food', desc: 'Grand Armenian feast — khorovats, duduk music, brandy' }
      ]
    },
    {
      num: 4,
      date: '2026-03-01',
      neighborhoods: 'Yerevan Centre · Zvartnots Airport',
      title: 'Last Morning — Coffee, Cognac & Goodbye',
      description: 'A relaxed final morning in Yerevan. No rush — savour a long Armenian breakfast, pick up last-minute souvenirs, and maybe squeeze in the Armenian Genocide Memorial if the group is up for it. Then taxi to Zvartnots Airport and carry home the warmth of Armenia.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Armenian Breakfast & Last Stroll',
              description: 'Enjoy a long, slow Armenian breakfast at your hotel or a neighbourhood café. Armenian breakfast is a production: fresh bread, honey, butter, cheese, herbs, eggs, and endless coffee. After breakfast, walk through the city one last time — Republic Square in the morning light, a final coffee near the Opera, maybe a last look at Ararat from the Cascade.',
              details: [
                '☕ Armenian coffee (soorj): thick, strong, served in small cups — order sweet (shakarov) or without (sev)',
                '🍯 Armenian breakfast staples: lavash, white cheese, tomatoes, herbs, fried eggs, honey',
                '📸 Last chance for that perfect Ararat shot — mornings are often clearest'
              ]
            },
            {
              title: 'Ararat Brandy Factory (Optional)',
              description: 'If time allows, the Ararat Brandy Company offers 45-minute tours of their historic distillery — you\'ll taste the legendary 10- and 20-year brandies in the same cellars where Churchill\'s personal barrel was stored. Perfect final Yerevan experience.',
              details: [
                '🥃 Tours: 3,500 AMD ($9) including tasting. Book online or walk in.',
                '📍 Admiral Isakov Avenue — 10 min taxi from centre',
                '⏰ Morning tours at 10 AM and 11 AM — schedule around your flight'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Hotel Breakfast or Café Central',
              description: 'Full Armenian spread — lavash, cheeses, herbs, honey, eggs, and soorj coffee. Take your time.',
              meta: '📍 Your hotel or any café near Republic Square'
            }
          ]
        },
        {
          label: 'Midday — Departure',
          activities: [
            {
              title: 'Transfer to Zvartnots Airport',
              description: 'Taxi or pre-arranged transfer to Zvartnots International Airport (EVN), 12 km west of the city centre. Allow 30–40 minutes for the drive. At the airport, pick up last boxes of churchkhela and dried fruit from the duty-free — Armenian products are excellent and cheap even at the airport.',
              details: [
                '🚕 GG Taxi to airport: ~3,000–4,000 AMD ($8–10)',
                '✈️ Arrive 2.5 hours before international flights',
                '🍬 Duty-free: churchkhela, dried apricots, Armenian coffee, and Ararat brandy miniatures'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.1776, lng: 44.5126, label: 'Republic Square (Final Visit)', num: 1, cat: 'attraction', desc: 'Morning light on the pink tuff buildings — last Yerevan moment' },
        { lat: 40.1810, lng: 44.4930, label: 'Ararat Brandy Factory', num: 2, cat: 'attraction', desc: 'Historic brandy distillery — tours and tastings of legendary Armenian konyak' },
        { lat: 40.1473, lng: 44.3959, label: 'Zvartnots Airport (EVN)', num: 3, cat: 'transport', desc: 'International airport — 12 km west of city centre, 30 min by taxi' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (3 nights)', budget: '60,000 AMD (~$150)', midrange: '120,000 AMD (~$310)', luxury: '250,000+ AMD (~$640+)' },
    { category: 'Meals & Drinks', budget: '40,000 AMD (~$100)', midrange: '80,000 AMD (~$205)', luxury: '150,000+ AMD (~$385+)' },
    { category: 'Activities & Entry Fees', budget: '8,000 AMD (~$20)', midrange: '15,000 AMD (~$38)', luxury: '30,000+ AMD (~$77+)' },
    { category: 'Transport (incl. day trip)', budget: '20,000 AMD (~$50)', midrange: '35,000 AMD (~$90)', luxury: '60,000+ AMD (~$155+)' },
    { category: 'Nightlife & Bars', budget: '15,000 AMD (~$38)', midrange: '30,000 AMD (~$77)', luxury: '60,000+ AMD (~$155+)' },
    { category: '3-Night Group Total (3-4 ppl)', budget: '$360–450', midrange: '$700–900', luxury: '$1,400+' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Zvartnots International Airport (EVN) — 12 km west of city centre', 'Direct flights from Istanbul, Dubai, Vienna, Athens, Moscow, and many European cities', 'Airport taxi: 3,000–4,000 AMD ($8–10) — use GG Taxi app or pre-book', 'Visa-free for US, EU, UK, and most nationalities (up to 180 days)'] },
    { title: '🏨 Where to Stay', items: ['The Alexander (luxury) — best location on Northern Avenue, family suites available', 'Tufenkian Historic Yerevan (mid-range) — boutique, near Republic Square, excellent service', 'Daniel Boutique Hotel (budget-mid) — central, cozy, great value', 'Airbnb: excellent selection of 2–3 bedroom apartments near the centre, $40–80/night'] },
    { title: '🚕 Getting Around', items: ['Yerevan is very walkable — most sights within 20 min walk of Republic Square', 'GG Taxi app: reliable, safe, incredibly cheap ($2–4 across the city)', 'Metro: one line, useful but limited coverage. 100 AMD ($0.25) per ride', 'Day trip to Garni/Geghard: hire a driver ($30–40 round trip) or join a group tour ($15/person)'] },
    { title: '🗣️ Language & Culture', items: ['Armenian (Hayeren) is the local language — unique alphabet, Indo-European family', 'Russian widely spoken by older generation; English increasingly common among youth', 'Armenians are famously hospitable — expect warmth, generosity, and endless invitations to eat', 'Tipping: 10% is generous and appreciated; not always expected'] }
  ]
};

fulfillOrder(order, itineraryData).then(result => {
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
