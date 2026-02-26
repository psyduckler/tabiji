const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771979889701_tm83pv',
  email: 'melanienelson1@me.com',
  destination: 'Porto, Portugal',
  startDate: '2026-02-18',
  endDate: '2026-02-24',
  groupSize: 1,
  requests: 'O idols chocolate festival'
};

const itineraryData = {
  destination: 'Porto, Portugal',
  countryEmoji: '🇵🇹',
  title: 'Soul, Azulejos & Port Wine in Porto',
  subtitle: '6 days of tile-clad streets, riverside feasts & chocolate indulgence for one',
  description: "Porto is a city that rewards the solo wanderer — every narrow alley reveals hand-painted azulejo tiles, every café serves a pastel de nata still warm from the oven, and the Douro River glows golden at sunset. This itinerary blends Porto's deep cultural soul with its legendary food scene, from crispy francesinhas to port wine cellars carved into Gaia's hillside. You'll visit the stunning Chocolate Experience at WOW (a nod to your love of chocolate festivals), explore medieval churches, relax along the Atlantic coast at Foz do Douro, and discover why Porto was named Europe's best destination — twice.",
  duration: '6 nights',
  dates: 'Feb 18 – Feb 24, 2026',
  budget: '$',
  pace: 'Relaxed',
  bestFor: 'Solo Travelers',
  highlights: [
    'Port wine tasting in the historic Gaia cellars',
    'The Chocolate Experience at WOW — Porto\'s chocolate museum',
    'Sunset over the Douro from Jardim do Morro',
    'Iconic francesinha at Café Santiago',
    'São Bento Station\'s breathtaking azulejo hall',
    'Atlantic sunset walk along Foz do Douro promenade'
  ],

  essentials: [
    { title: '🌧️ February Weather', text: 'Expect 8–15°C with occasional rain. Pack layers, a waterproof jacket, and comfortable walking shoes. Sunny spells between showers are common — Porto\'s winter light is gorgeous.' },
    { title: '🚇 Getting Around', text: 'Porto\'s metro, buses, and trams are covered by the Andante card (reloadable). The historic Tram 1 runs along the river to Foz. Walking is the best way to explore the hilly centre — wear sturdy shoes.' },
    { title: '💰 Budget-Friendly', text: 'Porto is one of Europe\'s best-value cities. A full meal costs €8–15, espresso (bica) is €0.70, museum entries are €3–10, and port tastings start at €5. Your budget goes far here.' },
    { title: '🍫 Chocolate Note', text: 'The famous Óbidos International Chocolate Festival runs in March–April (after your visit), but Porto\'s WOW district has the permanent Chocolate Experience museum — a deep dive into cacao history with tastings. It\'s excellent.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-18',
      neighborhoods: 'Aliados · Bolhão · São Bento',
      title: 'Arrival — Grand Avenues & Golden Tiles',
      description: "Arrive in Porto and plunge straight into the city's heart. The grand Avenida dos Aliados, the dazzling azulejos of São Bento Station, and the buzzing Bolhão Market set the stage for an unforgettable week.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'São Bento Station & Avenida dos Aliados',
              description: 'Start at São Bento Station — not to catch a train, but to stand in awe of 20,000 azulejo tiles depicting Portuguese history. Step outside and walk up Avenida dos Aliados, Porto\'s grand Beaux-Arts boulevard lined with ornate facades.',
              details: [
                '🎨 São Bento\'s tiles took artist Jorge Colaço 11 years to complete',
                '📸 Best photos: stand at the back of the hall for the full panorama',
                '🏛️ Aliados is Porto\'s Times Square — grand, photogenic, alive'
              ]
            },
            {
              title: 'Mercado do Bolhão',
              description: 'The recently restored Bolhão Market is Porto\'s culinary soul — two floors of fresh produce, cured meats, cheeses, flowers, and local vendors who\'ve been here for generations. Grab a bifana (pork sandwich) and soak up the energy.',
              details: [
                '🥩 Try a bifana from any vendor — Porto\'s beloved street snack',
                '🧀 Pick up queijo da Serra for later — creamy mountain cheese',
                '🌸 The Art Nouveau ironwork is stunning after the 2022 restoration'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Porto\'s centre is compact but hilly. Wear comfortable shoes and embrace the stairs — the views from every climb are worth it.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Rua das Flores Sunset Stroll',
              description: 'Walk down Rua das Flores, one of Porto\'s most charming pedestrian streets. Lined with tile-fronted buildings, independent shops, and café terraces, it leads you naturally toward the river.',
              details: [
                '☕ Stop at Combi Coffee Roasters for a specialty flat white',
                '🎵 Street musicians often play in the early evening'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cantinho do Avillez',
              description: 'Chef José Avillez\'s casual Porto outpost — refined Portuguese comfort food in a relaxed setting. Solo diners are welcomed warmly at the bar.',
              meta: '💰 €20–30 · 📍 Rua de Mouzinho da Silveira 166'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1459, lng: -8.6103, label: 'São Bento Station', num: 1, cat: 'attraction', desc: 'Railway station with 20,000 hand-painted azulejo tiles' },
        { lat: 41.1496, lng: -8.6110, label: 'Avenida dos Aliados', num: 2, cat: 'attraction', desc: 'Grand Beaux-Arts boulevard — Porto\'s civic heart' },
        { lat: 41.1494, lng: -8.6060, label: 'Mercado do Bolhão', num: 3, cat: 'food', desc: 'Restored Art Nouveau market with local vendors' },
        { lat: 41.1457, lng: -8.6146, label: 'Rua das Flores', num: 4, cat: 'attraction', desc: 'Charming pedestrian street with tiles and cafés' },
        { lat: 41.1448, lng: -8.6140, label: 'Cantinho do Avillez', num: 5, cat: 'food', desc: 'José Avillez\'s casual Portuguese dining' }
      ]
    },
    {
      num: 2,
      date: '2026-02-19',
      neighborhoods: 'Ribeira · Dom Luís I Bridge · Vila Nova de Gaia',
      title: 'Ribeira, the Bridge & Port Wine Cellars',
      description: "Today is Porto at its most iconic — the colourful Ribeira waterfront, the double-decker Dom Luís I Bridge, and an afternoon tasting your way through the legendary port wine cellars of Vila Nova de Gaia.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ribeira Waterfront',
              description: 'Wander through Porto\'s UNESCO-listed Ribeira district — a tumble of medieval houses painted in ochre, terracotta, and blue, cascading down to the Douro. Grab a coffee at a riverside terrace and watch the rabelo boats drift by.',
              details: [
                '🏘️ Ribeira is a UNESCO World Heritage Site since 1996',
                '📸 Best viewpoint: the riverside promenade (Cais da Ribeira)',
                '☕ Café terraces line the waterfront — pick any with a view'
              ]
            },
            {
              title: 'Walk Across Dom Luís I Bridge',
              description: 'Cross the iconic double-decker iron bridge on the upper level for jaw-dropping views of both Porto and Gaia. Designed by a student of Gustave Eiffel, the bridge is Porto\'s most recognizable landmark.',
              details: [
                '🌉 Upper deck: pedestrians + metro — the view is extraordinary',
                '📸 Stop in the middle for the classic Ribeira panorama',
                '💨 It can be windy on top — hold onto hats!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Port Wine Cellars — Gaia',
              description: 'Cross into Vila Nova de Gaia and enter the cool, barrel-lined caves of the port wine lodges. Taylor\'s, Graham\'s, and Sandeman all offer excellent tours with tastings. As a solo traveler, you\'ll often join a small group — a great way to meet people.',
              details: [
                '🍷 Taylor\'s — stunning terrace with panoramic views (€15 tasting)',
                '🍷 Graham\'s — intimate lodge with excellent vintage ports',
                '🍷 Sandeman — the classic, with its iconic caped figure logo',
                '⏰ Tours run hourly, about 45–60 mins each'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Taberninha do Manel',
              description: 'Tiny, beloved tasca in Ribeira. Daily specials on a chalkboard — fresh grilled fish, stewed meats, and house wine by the jug. This is real Porto.',
              meta: '💰 €8–12 · 📍 Ribeira district'
            }
          ],
          tips: [
            { type: 'tip', text: 'Port comes in many styles — try a tawny (smooth, caramel notes), a ruby (fruity, bold), and a white port with tonic (Porto\'s signature aperitif). Ask for a white port & tonic at any cellar bar.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from Jardim do Morro',
              description: 'End the day at Jardim do Morro, the garden on the Gaia hilltop beside the bridge. Locals and travelers gather here every evening to watch the sun set over Porto\'s skyline — it\'s pure magic.',
              details: [
                '🌅 Arrive 30 mins before sunset for the best spot',
                '🎸 Street musicians play as the sky turns pink',
                '🍺 Grab a Super Bock from a nearby café to sip during the show'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Dick\'s Bar at The Yeatman',
              description: 'Elevated bar dining at Gaia\'s finest hotel. Incredible views over Porto, creative tapas, and an encyclopedic port wine list. Dress smart-casual.',
              meta: '💰 €25–40 · 📍 The Yeatman Hotel, Gaia'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1407, lng: -8.6132, label: 'Cais da Ribeira', num: 1, cat: 'attraction', desc: 'UNESCO-listed medieval waterfront district' },
        { lat: 41.1395, lng: -8.6097, label: 'Dom Luís I Bridge', num: 2, cat: 'attraction', desc: 'Iconic double-decker iron bridge over the Douro' },
        { lat: 41.1373, lng: -8.6128, label: 'Taylor\'s Port', num: 3, cat: 'attraction', desc: 'Historic port wine lodge with panoramic terrace' },
        { lat: 41.1367, lng: -8.6157, label: 'Graham\'s Port Lodge', num: 4, cat: 'attraction', desc: 'Premium port tasting with river views' },
        { lat: 41.1371, lng: -8.6098, label: 'Jardim do Morro', num: 5, cat: 'attraction', desc: 'Hilltop garden — best sunset in Porto' },
        { lat: 41.1353, lng: -8.6148, label: 'The Yeatman', num: 6, cat: 'food', desc: 'Luxury hotel bar with sweeping Porto panorama' }
      ]
    },
    {
      num: 3,
      date: '2026-02-20',
      neighborhoods: 'WOW · Gaia Waterfront · Cedofeita',
      title: 'Chocolate, Culture & Creative Porto',
      description: "Dive into Porto's chocolate connection at WOW's Chocolate Experience, explore the vibrant cultural quarter of WOW, then cross back to Porto's creative Cedofeita neighbourhood for street art, vinyl shops, and a legendary francesinha.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'WOW — World of Wine & The Chocolate Experience',
              description: 'WOW is a massive cultural district in Gaia with seven museums. Head straight to The Chocolate Experience — an immersive journey through cacao\'s 5,000-year history, from Aztec rituals to modern artisan chocolate-making, complete with tastings.',
              details: [
                '🍫 The Chocolate Experience: interactive museum with tasting room',
                '🎟️ Entry €10–15 per museum, combo tickets available',
                '🍷 Also visit The Wine Experience or The Bridge Collection if time allows',
                '☕ WOW has excellent cafés and a chocolate shop for souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'WOW Chocolate Café',
              description: 'Start the day with artisan hot chocolate and fresh pastries at the WOW complex café. Rich, thick Portuguese-style hot chocolate made from single-origin cacao.',
              meta: '💰 €5–8 · 📍 WOW, Vila Nova de Gaia'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cedofeita — Street Art & Creative Quarter',
              description: 'Cross back to Porto and explore Cedofeita, the city\'s hippest neighbourhood. Rua de Miguel Bombarda is lined with art galleries, while the surrounding streets are covered in murals and street art. Browse vintage shops and independent boutiques.',
              details: [
                '🎨 Rua de Miguel Bombarda — gallery row, opening nights on Saturdays',
                '🖼️ Half-Rabbit mural on Rua das Flores — iconic Porto street art',
                '🎵 Browse vinyl at Matéria Prima record shop'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Café Santiago',
              description: 'Porto\'s most famous francesinha — a towering sandwich of ham, sausage, and steak smothered in melted cheese and a secret beer-tomato sauce, served with fries. It\'s a rite of passage.',
              meta: '💰 €12–15 · 📍 Rua de Passos Manuel 226 · Expect a queue — worth it'
            }
          ],
          tips: [
            { type: 'tip', text: 'The francesinha is enormous — skip breakfast or share. Most locals eat it for lunch, not dinner. Pair with a Super Bock beer.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Live Fado in Porto',
              description: 'Porto has its own fado tradition, different from Lisbon\'s. Seek out an intimate fado house for an evening of soulful Portuguese music. Casa da Guitarra or Ideal Clube de Fado offer authentic performances.',
              details: [
                '🎵 Porto fado tends to be more raw and intimate than Lisbon\'s',
                '🍷 Most fado houses include a drink — usually port wine',
                '⏰ Shows typically start at 9 or 9:30pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Jimão Tapas e Vinhos',
              description: 'Relaxed wine bar with excellent petiscos (Portuguese tapas). Great for solo diners — sit at the bar, chat with the staff, and graze on cured meats, cheese, and small plates.',
              meta: '💰 €15–20 · 📍 Praça Guilherme Gomes Fernandes'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1365, lng: -8.6130, label: 'WOW — World of Wine', num: 1, cat: 'attraction', desc: 'Cultural district with The Chocolate Experience museum' },
        { lat: 41.1520, lng: -8.6230, label: 'Rua de Miguel Bombarda', num: 2, cat: 'attraction', desc: 'Gallery row and creative quarter' },
        { lat: 41.1490, lng: -8.6060, label: 'Café Santiago', num: 3, cat: 'food', desc: 'Porto\'s legendary francesinha' },
        { lat: 41.1456, lng: -8.6158, label: 'Casa da Guitarra', num: 4, cat: 'attraction', desc: 'Intimate fado performances' },
        { lat: 41.1478, lng: -8.6170, label: 'Jimão Tapas e Vinhos', num: 5, cat: 'food', desc: 'Wine bar with Portuguese tapas' }
      ]
    },
    {
      num: 4,
      date: '2026-02-21',
      neighborhoods: 'Clérigos · Lello · Sé · Miragaia',
      title: 'Towers, Bookshops & Cathedral Views',
      description: "Porto's most iconic landmarks in one glorious day — climb the Clérigos Tower for a 360° panorama, step inside the world-famous Livraria Lello, explore the medieval Sé Cathedral, and wind through the ancient Miragaia quarter.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Torre dos Clérigos',
              description: 'Climb the 240 steps of Porto\'s landmark baroque tower for the best panoramic view of the city. On a clear February morning, you can see all the way to the Atlantic. The attached church is a masterpiece of baroque architecture.',
              details: [
                '🗼 76 metres tall — Porto\'s tallest structure for centuries',
                '⏰ Opens at 9am — go early to avoid crowds',
                '📸 360° views of the red rooftops, river, and ocean',
                '🎟️ €8 entry, includes tower + church + museum'
              ]
            },
            {
              title: 'Livraria Lello',
              description: 'One of the world\'s most beautiful bookshops, with a neo-Gothic facade, stained glass ceiling, and a famous crimson staircase. Often cited as J.K. Rowling\'s inspiration (she lived in Porto). Buy your ticket online to skip the queue.',
              details: [
                '📚 Book online (€8 voucher redeemable against a purchase)',
                '📸 The crimson staircase is extraordinary — go early for photos without crowds',
                '🧙 Rowling taught English in Porto 1991–93; Lello\'s influence on Hogwarts is debated but undeniable'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sé do Porto (Cathedral)',
              description: 'Porto\'s fortress-like Romanesque cathedral dominates the skyline. The Gothic cloisters are decorated with beautiful azulejos, and the terrace offers sweeping views over Ribeira and the river.',
              details: [
                '⛪ Free entry to the cathedral; cloisters €3',
                '🎨 14th-century Gothic cloisters with blue-and-white azulejos',
                '📸 The terrace view down to the Douro is stunning'
              ]
            },
            {
              title: 'Igreja de São Francisco',
              description: 'Step inside Porto\'s most lavishly decorated church — every surface is covered in gilded carved wood. The interior used an estimated 300kg of gold. The catacombs beneath are hauntingly atmospheric.',
              details: [
                '✨ 300–400kg of gold covers the baroque interior',
                '💀 The catacombs are fascinating but not for the faint-hearted',
                '🎟️ €9 entry'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Gazela Cachorrinhos',
              description: 'A Porto institution — tiny counter-service spot famous for cachorrinhos (small spicy sausage hot dogs) and ice-cold imperial (draught beer). Quick, cheap, and absolutely delicious.',
              meta: '💰 €3–5 · 📍 Travessa de Cedofeita 8B'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Miragaia Quarter Wander',
              description: 'Walk through the quiet, ancient Miragaia neighbourhood below the Sé. Narrow medieval streets, laundry hanging between buildings, neighbourhood tascas, and almost no tourists. This is the Porto that locals love.',
              details: [
                '🏘️ One of Porto\'s oldest parishes — medieval atmosphere',
                '😺 Keep an eye out for Porto\'s many street cats',
                '🌅 Beautiful golden-hour light on the tile facades'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Adega São Nicolau',
              description: 'Riverside restaurant in Ribeira serving traditional Porto cuisine. Try the polvo à lagareiro (roasted octopus with crushed potatoes) — it\'s legendary.',
              meta: '💰 €15–22 · 📍 Rua de São Nicolau 1 · River views from the terrace'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1458, lng: -8.6148, label: 'Torre dos Clérigos', num: 1, cat: 'attraction', desc: 'Baroque bell tower with 360° city panorama' },
        { lat: 41.1468, lng: -8.6152, label: 'Livraria Lello', num: 2, cat: 'attraction', desc: 'World-famous neo-Gothic bookshop' },
        { lat: 41.1429, lng: -8.6115, label: 'Sé do Porto', num: 3, cat: 'attraction', desc: 'Romanesque cathedral with azulejo cloisters' },
        { lat: 41.1413, lng: -8.6163, label: 'Igreja de São Francisco', num: 4, cat: 'attraction', desc: 'Gilded baroque church interior — 300kg of gold' },
        { lat: 41.1485, lng: -8.6085, label: 'Gazela Cachorrinhos', num: 5, cat: 'food', desc: 'Iconic spicy hot dogs and draught beer' },
        { lat: 41.1410, lng: -8.6190, label: 'Miragaia', num: 6, cat: 'attraction', desc: 'Ancient medieval quarter with authentic local life' },
        { lat: 41.1405, lng: -8.6140, label: 'Adega São Nicolau', num: 7, cat: 'food', desc: 'Traditional riverside restaurant with octopus' }
      ]
    },
    {
      num: 5,
      date: '2026-02-22',
      neighborhoods: 'Foz do Douro · Matosinhos · Atlantic Coast',
      title: 'Ocean Air — Foz, Beaches & Seafood',
      description: "Trade the city for the coast. Take the historic tram to Foz do Douro where the Douro meets the Atlantic, stroll along windswept beaches, then continue to Matosinhos for what might be the best grilled fish lunch of your life.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tram 1 to Foz do Douro',
              description: 'Board the charming vintage Tram 1 along the Douro riverfront — it rattles past old warehouses and riverside gardens all the way to the ocean. Foz do Douro is Porto\'s elegant seaside district where the river meets the Atlantic.',
              details: [
                '🚋 Tram 1 departs from Infante, near Ribeira — a 30-min scenic ride',
                '🎟️ €3.50 one-way — pay on board',
                '📸 Sit on the left side for river views'
              ]
            },
            {
              title: 'Foz Promenade & Farol de Felgueiras',
              description: 'Walk along the Foz promenade beside the crashing Atlantic waves. Follow the path to the Farol de Felgueiras lighthouse at the very tip of the Douro\'s mouth — the sound and spray of the ocean here is invigorating.',
              details: [
                '🌊 The Pérgola da Foz — Art Deco seaside walkway',
                '🔭 Felgueiras Lighthouse sits on a dramatic rocky breakwater',
                '☕ Plenty of seaside cafés for a mid-morning galão (latte)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Matosinhos — Grilled Fish Capital',
              description: 'Continue north to Matosinhos, Porto\'s fishing neighbourhood. The streets near the fish market are lined with restaurants grilling sardines, sea bass, and turbot over charcoal right on the pavement. Choose any place with smoke billowing out — they\'re all excellent.',
              details: [
                '🐟 Rua Heróis de França — the grilled fish street',
                '🔥 Fish is grilled whole over charcoal and served with boiled potatoes and salad',
                '💰 A massive grilled fish lunch with wine: €12–18'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'O Gaveto',
              description: 'Matosinhos institution for impeccably fresh seafood. The arroz de marisco (seafood rice) is a revelation. Solo diners can eat at the bar and watch the kitchen work.',
              meta: '💰 €18–25 · 📍 Rua Roberto Ivens 826, Matosinhos'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Praia do Carneiro',
              description: 'Return to Foz and find a spot on Praia do Carneiro or along the rocks near the Pérgola to watch the sun sink into the Atlantic. February sunsets in Porto are early (around 6pm) but vivid — deep oranges and pinks over the ocean.',
              details: [
                '🌅 Sunset around 6pm in February — golden light from 5pm',
                '🍸 Pop into Praia da Luz beach bar if it\'s open, or bring a bottle of port'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Cafeína',
              description: 'Stylish Foz do Douro restaurant with creative Portuguese cuisine. The terrace overlooks the ocean, and the risottos and grilled meats are superb. A favourite with Porto\'s locals.',
              meta: '💰 €18–28 · 📍 Rua do Padrão 100, Foz do Douro'
            }
          ],
          tips: [
            { type: 'tip', text: 'Take the bus or Uber back to the centre after dinner — the tram stops running in the evening. Bus 500 follows the coast road back to Ribeira.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1470, lng: -8.6290, label: 'Tram 1 Stop (Infante)', num: 1, cat: 'attraction', desc: 'Catch the vintage riverside tram to Foz' },
        { lat: 41.1507, lng: -8.6770, label: 'Foz do Douro', num: 2, cat: 'attraction', desc: 'Elegant seaside district where river meets ocean' },
        { lat: 41.1485, lng: -8.6805, label: 'Farol de Felgueiras', num: 3, cat: 'attraction', desc: 'Lighthouse at the Douro\'s mouth' },
        { lat: 41.1832, lng: -8.6878, label: 'Matosinhos', num: 4, cat: 'food', desc: 'Fishing district — grilled fish capital' },
        { lat: 41.1847, lng: -8.6910, label: 'O Gaveto', num: 5, cat: 'food', desc: 'Legendary seafood restaurant' },
        { lat: 41.1510, lng: -8.6790, label: 'Cafeína', num: 6, cat: 'food', desc: 'Oceanside creative dining in Foz' }
      ]
    },
    {
      num: 6,
      date: '2026-02-23',
      neighborhoods: 'Douro Valley · Régua · Pinhão',
      title: 'Douro Valley — Vineyards, River & Quintas',
      description: "Take a day trip to the UNESCO-listed Douro Valley — one of the world's most beautiful wine regions. Terraced vineyards cascade down to the river, quintas (wine estates) welcome visitors with tastings, and the train ride from Porto is one of Europe's most scenic.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Scenic Train to the Douro Valley',
              description: 'Board the train at São Bento or Campanhã station for the stunning 2-hour ride along the Douro River to Régua or Pinhão. The railway hugs the riverbank through narrow gorges and past terraced vineyards — it\'s one of Europe\'s greatest train journeys.',
              details: [
                '🚂 Depart around 8:30am from Campanhã station',
                '📸 Sit on the right side for the best river views',
                '🎟️ €12–15 each way, second class — book at cp.pt',
                '⏰ Journey: ~2 hours to Régua, ~2.5 hours to Pinhão'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Quinta Visit & Wine Tasting',
              description: 'Visit a traditional quinta (wine estate) for a tour of the vineyards and a tasting. Quinta da Pacheca, Quinta do Vallado, or Quinta do Crasto all welcome solo visitors. The valley in February is quiet and misty — hauntingly beautiful.',
              details: [
                '🍷 Tastings typically include 3–5 wines (€10–20)',
                '🏡 Quinta da Pacheca also has famous wine-barrel hotel rooms',
                '🌿 February: vines are dormant, but the terraced landscape is dramatic'
              ]
            },
            {
              title: 'Pinhão Village',
              description: 'If you make it to Pinhão, don\'t miss the tiny station decorated with azulejo panels depicting the Douro wine harvest. The village itself is a handful of streets between vineyards and the river — beautifully tranquil.',
              details: [
                '🎨 Pinhão station azulejos show traditional grape-treading scenes',
                '🚣 River cruises available from Pinhão (1 hour, ~€10)',
                '☕ Tiny cafés in the village serve local wines and snacks'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'DOC Restaurant',
              description: 'Chef Rui Paula\'s riverside restaurant in the heart of the Douro Valley. Floor-to-ceiling windows frame the terraced vineyards. Modern Portuguese cuisine with local wines — an extraordinary solo lunch.',
              meta: '💰 €25–40 · 📍 Estrada Nacional 222, Folgosa · Reservations essential'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Train Back to Porto',
              description: 'Catch the late afternoon train back to Porto as the sun sets over the valley. The return journey in golden light is even more beautiful than the morning ride.',
              details: [
                '🚂 Last trains from Pinhão around 5–6pm — check schedules',
                '🌅 The sunset over the terraced hillsides is magical from the train'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Tapabento',
              description: 'Back in Porto, end the day at this beloved petiscos restaurant near São Bento. Small plates, natural wines, and a bustling atmosphere. The perfect casual farewell dinner.',
              meta: '💰 €15–22 · 📍 Rua da Madeira 222 · No reservations — arrive early'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book train tickets in advance at cp.pt — the Douro line is popular even in winter. Regional trains have no assigned seats, so boarding early gets you a window.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.1459, lng: -8.6103, label: 'São Bento Station', num: 1, cat: 'attraction', desc: 'Departure point for the Douro Valley train' },
        { lat: 41.1629, lng: -7.7900, label: 'Régua', num: 2, cat: 'attraction', desc: 'Douro Valley town — gateway to the quintas' },
        { lat: 41.1895, lng: -7.5462, label: 'Pinhão', num: 3, cat: 'attraction', desc: 'Charming village with azulejo station' },
        { lat: 41.1640, lng: -7.7850, label: 'Quinta da Pacheca', num: 4, cat: 'attraction', desc: 'Historic wine estate with tastings' },
        { lat: 41.1670, lng: -7.7750, label: 'DOC Restaurant', num: 5, cat: 'food', desc: 'Riverside fine dining in the Douro Valley' },
        { lat: 41.1460, lng: -8.6110, label: 'Tapabento', num: 6, cat: 'food', desc: 'Petiscos and natural wines near São Bento' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '€25–40/night (hostel)', midrange: '€60–100/night', luxury: '€150–300/night' },
    { category: 'Meals (solo)', budget: '€15–25/day', midrange: '€30–50/day', luxury: '€60–100/day' },
    { category: 'Transport', budget: '€5–10/day', midrange: '€10–20/day', luxury: '€30–60/day' },
    { category: 'Activities', budget: '€0–10/day', midrange: '€10–25/day', luxury: '€25–50/day' },
    { category: 'Port Tastings', budget: '€5–10/session', midrange: '€15–25/session', luxury: '€30–60/session' },
    { category: '6-Day Total (solo)', budget: '€350–600', midrange: '€600–1,200', luxury: '€1,500–3,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Porto Airport (OPO) is 11km from the city centre', 'Metro line E (Violet) runs directly to the centre — 30 mins, €2.60', 'Uber/taxi from airport costs €20–25'] },
    { title: '🏨 Where to Stay', items: ['Gallery Hostel — beautifully designed hostel on Rua de Miguel Bombarda (solo travelers love it)', 'Pestana Porto — A Brasileira, iconic café-hotel on Aliados', 'Rosa et Al Townhouse — boutique B&B with personal touches', 'Ribeira district — most atmospheric, right on the river'] },
    { title: '🌡️ Weather', items: ['February averages 8–15°C (46–59°F)', 'Expect rain — Porto gets about 14 rainy days in February', 'Sunny breaks are common and the light is beautiful', 'Pack layers, waterproof jacket, and sturdy walking shoes'] },
    { title: '💳 Money', items: ['Euro (€) — tap-and-go payments widely accepted', 'Cash still useful at small tascas and markets', 'Tipping: round up or leave 5–10% for good service', 'ATMs (Multibanco) are everywhere — avoid currency conversion options'] },
    { title: '📱 Connectivity', items: ['Buy an eSIM or prepaid NOS/Vodafone SIM at the airport', 'Free WiFi in most cafés, hotels, and public spaces', 'Coverage is excellent throughout Porto and the Douro Valley'] }
  ]
};

fulfillOrder(order, itineraryData);
