const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772003495492_z3xad7',
  email: 'nonofyourconcern@gmx.at',
  destination: 'Galway, Ireland',
  startDate: '2026-05-01',
  endDate: '2026-05-10',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Galway, Ireland',
  countryEmoji: '🇮🇪',
  title: 'The Wild Atlantic Way: Solo in Galway',
  subtitle: '10 days of trad sessions, Atlantic drama & the soul of the Irish West',
  description: "Galway is Ireland's beating cultural heart — a compact, colourful city where every pub spills traditional music onto cobbled streets, every horizon opens to the savage beauty of Connemara, and every stranger is a conversation waiting to happen. Sitting on the edge of the Atlantic, Galway is the perfect base for some of Ireland's most dramatic landscapes: the cliffs of Moher plunging into the ocean, the ancient limestone plateau of The Burren, mystical Aran Islands rising from the sea, and the wild bogs and mountains of Connemara. May brings mild weather, long evenings, spring wildflowers, and smaller crowds — the absolute sweet spot for Ireland. Solo travel here is effortless: the Irish are famously warm, pub culture is inherently communal, and every session at The Crane Bar will make you feel like a local by the second pint.",
  duration: '9 nights',
  dates: 'May 1 – May 10, 2026',
  budget: '$$',
  pace: 'Balanced',
  bestFor: 'Solo Travelers · Culture & Music · Wild Nature',
  highlights: [
    'Lose yourself in spontaneous trad sessions at The Crane Bar and Tigh Neachtain',
    'Cycle the ancient cliffs of Dún Aonghasa on car-free Inis Mór (Aran Islands)',
    'Stand at the edge of the Cliffs of Moher — 700ft above the crashing Atlantic',
    'Wander the karst moonscape of The Burren scattered with spring wildflowers',
    'Drive the Sky Road loop at Clifden for Connemara\'s most dramatic scenery',
    'Explore Kylemore Abbey and the haunting Connemara bogs',
    'Feast on Galway Bay oysters, smoked salmon & fresh crab at the Saturday Market',
    'Watch the sun sink into the Atlantic from the Salthill promenade'
  ],

  essentials: [
    { title: '🌦️ May in Galway', text: 'May is shoulder season at its finest: 12–17°C, long evenings (light until 9:30pm), spring wildflowers across The Burren, and crowds a fraction of summer peak. Pack layers — Galway is famously changeable, often delivering sunshine and rain in the same hour. A waterproof shell jacket is non-negotiable on the Wild Atlantic Way.' },
    { title: '🚌 Getting Around', text: 'Galway City is entirely walkable. For day trips, Bus Éireann coaches and private tour operators serve Cliffs of Moher and Connemara. The Aran Islands ferry departs Rossaveel (40 min bus from Galway) or from Doolin. Renting a car for 1–2 days unlocks the full Connemara experience at your own pace.' },
    { title: '🎵 Trad Music Guide', text: 'Galway has some of Ireland\'s finest trad sessions. The Crane Bar (west end) and Tigh Neachtain (Latin Quarter) run nightly sessions. Monroe\'s Tavern has legendary Tuesday night sessions with spontaneous dancing. Sessions start around 9pm — arrive by 8:30 to get a seat. No cover charge ever; just buy a pint and listen.' },
    { title: '🦪 Galway Seafood', text: 'Galway Bay oysters are world famous — fresh, briny and best eaten with a pint of stout. The Saturday Market (Eyre Square area) has incredible smoked fish, artisan cheese and local produce. For a seafood feast, Aniar (Michelin-starred), McDonagh\'s (legendary chippie) and Loam are the classics. The oyster festival is in September, but May oysters are still superb.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-01',
      neighborhoods: 'Eyre Square · Shop Street · Latin Quarter',
      title: 'Arrival & First Pint in the Latin Quarter',
      description: "Touch down in the west of Ireland and let Galway cast its spell immediately. The city is tiny enough to navigate on foot but rich enough to fill a month. Eyre Square anchors the centre; Shop Street leads you into the Latin Quarter's tangle of colourful pubs, buskers, and medieval laneways. Tonight: your first trad session.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Eyre Square & City Orientation',
              description: 'Drop your bags and head to Eyre Square — the city\'s central park and gathering place, ringed by hotels and the impressive Brown Thomas department store. The square holds a monument to Pádraic Ó Conaire and sails commemorating the old Galway Hooker fishing boats. Take a slow lap to get your bearings.',
              details: [
                '🌳 Eyre Square is officially Kennedy Memorial Park — JFK visited in 1963',
                '🚂 Bus/train stations are right next to the square — perfect drop point',
                '🛍️ Nearby William Street has all the practical shops if you need anything'
              ]
            },
            {
              title: 'Shop Street & Latin Quarter Wander',
              description: 'Walk down Shop Street — one of Ireland\'s great pedestrian thoroughfares. Street buskers play everything from fiddle to bodhran; medieval guild symbols are carved into building facades; every second doorway is a pub or artisan shop. Turn into the Latin Quarter lanes: Quay Street, Kirwan\'s Lane, Cross Street — each one charming, each one different.',
              details: [
                '🎶 Stop wherever buskers are playing — talent level is genuinely exceptional',
                '💍 Pass Thomas Dillion\'s (est. 1750) — Ireland\'s oldest jeweller and home of the Claddagh ring',
                '📸 Kirwan\'s Lane is the most photogenic medieval alley in Galway'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 First Pint',
              name: 'Tigh Neachtain',
              description: 'A Galway institution since the 1890s — low ceilings, mismatched furniture, turf fire glow, and invariably a session starting in the corner. Order a Guinness and let the city come to you. Solo-traveler heaven: everyone talks to everyone here.',
              meta: '💰 $ · 📍 17 Cross St, Latin Quarter · Trad sessions most evenings'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Trad Session at The Crane Bar',
              description: 'Cross to the West End for your first proper trad session. The Crane Bar is small, atmospheric, and consistently hosts some of Galway\'s best musicians. The upstairs room gets intimate — squeeze in, order a Guinness, and watch master players improvise reels and jigs that have been passed down for generations.',
              details: [
                '🎻 Sessions start ~9pm, arrive by 8:30 for a seat',
                '🍺 Two-floor pub — ground floor is more casual; upstairs is the session room',
                '📍 2 Sea Rd, West End — 10-min walk from Latin Quarter'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ard Bia at Nimmo\'s',
              description: 'Set in a 1270s stone warehouse on the Spanish Arch waterfront, Ard Bia serves earthy, seasonal Irish food: roasted beets, smoked mackerel, lamb from Connemara, chowder with soda bread. One of Galway\'s most beloved restaurants — book ahead.',
              meta: '💰 $$$ · 📍 Long Walk, Spanish Arch · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2743, lng: -9.0489, label: 'Eyre Square', num: 1, cat: 'attraction', desc: 'Central city square — Kennedy Memorial Park' },
        { lat: 53.2726, lng: -9.0518, label: 'Shop Street', num: 2, cat: 'attraction', desc: 'Pedestrian heart of Galway with buskers and medieval buildings' },
        { lat: 53.2714, lng: -9.0533, label: 'Tigh Neachtain', num: 3, cat: 'food', desc: 'Legendary 1890s pub with nightly trad sessions' },
        { lat: 53.2699, lng: -9.0541, label: 'Ard Bia at Nimmo\'s', num: 4, cat: 'food', desc: 'Seasonal Irish cuisine in a 13th-century stone warehouse' },
        { lat: 53.2719, lng: -9.0607, label: 'The Crane Bar', num: 5, cat: 'attraction', desc: 'Best trad sessions in Galway — West End institution' }
      ]
    },
    {
      num: 2,
      date: '2026-05-02',
      neighborhoods: 'Spanish Arch · Galway Cathedral · River Corrib',
      title: 'Medieval Galway, the Cathedral & the Corrib',
      description: "Galway's medieval bones are all around — the Spanish Arch where Armada galleons once unloaded, the hulking Galway Cathedral on the river, the old city walls peeping between modern shopfronts. Today you'll trace the city's history along the River Corrib and prepare for your big day trips ahead.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Spanish Arch & City Museum',
              description: 'The Spanish Arch is a 16th-century remnant of Galway\'s medieval walls, built to protect the quay where Spanish merchant ships unloaded wine and goods. Lean on it, look out at the Claddagh district across the water, and feel centuries of Atlantic trade. The Galway City Museum beside it is small but excellent — free entry.',
              details: [
                '🏛️ Galway City Museum: free entry, covers everything from the Famine to the Tribes of Galway',
                '📸 The arch-and-river view is one of Galway\'s most photographed scenes',
                '🌊 The area in front is a popular summer hangout — locals sunbathing on the stones'
              ]
            },
            {
              title: 'Walk Along the River Corrib',
              description: 'Follow the River Corrib upstream from the Spanish Arch, past the weir where salmon leap in spring, along the Gaol Road riverside walk to the Cathedral. The river is remarkably wild and powerful for a city centre — at the weir you\'ll often see salmon fishermen standing thigh-deep in the current.',
              details: [
                '🐟 May is prime salmon season — look for them leaping at the weir',
                '🚣 Kayakers and rowing clubs use this stretch daily',
                '📍 The walk to the Cathedral takes about 20 minutes'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kai Cafe',
              description: 'The West End\'s beloved neighbourhood café — owners Jess and David source almost everything locally. Eggs from down the road, bread from Tartine, seasonal vegetables. The weekend brunch is legendary; weekday breakfast is quieter and equally good.',
              meta: '💰 $$ · 📍 20 Sea Rd, West End · Opens 9am weekdays'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Galway Cathedral',
              description: 'One of the last great stone cathedrals built in Europe (completed 1965), rising dramatically over the River Corrib. The interior is a riot of coloured stone, intricate mosaics, and stained glass. A famous JFK mosaic graces one wall — the President visited Galway just months before his assassination. Free to enter.',
              details: [
                '⛪ Free entry — open daily 8:30am–6:30pm',
                '🎨 The JFK mosaic is a fascinating slice of 1960s Irish-American history',
                '🎶 Weekend masses often feature the Cathedral Choir — sublime acoustics'
              ]
            },
            {
              title: 'Claddagh Village & Nimmo\'s Pier',
              description: 'Cross to the Claddagh — the ancient fishing village just west of the Spanish Arch where the famous Claddagh ring originated. The old thatched cottages are gone, replaced by modest terrace houses, but the spirit lingers. Walk out to Nimmo\'s Pier for extraordinary views back to the city and out over the bay.',
              details: [
                '💍 The Claddagh ring originated here in the 17th century — hands, heart, crown',
                '🌊 Nimmo\'s Pier at sunset or dusk is one of Galway\'s best views',
                '📸 Look back toward the city centre for classic Galway skyline shots'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'McDonagh\'s Seafood House',
              description: 'A Galway institution since 1902. Downstairs is a traditional fish-and-chip shop (cash only, eat at formica tables with locals); upstairs is a sit-down seafood restaurant. The fish is as fresh as it gets — the catch is delivered daily. Order the chowder and the battered cod for a quintessential Galway meal.',
              meta: '💰 $$ · 📍 22 Quay St · Fish & chips: walk-in, no reservations needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2695, lng: -9.0535, label: 'Spanish Arch', num: 1, cat: 'attraction', desc: '16th-century medieval arch and quay wall' },
        { lat: 53.2694, lng: -9.0535, label: 'Galway City Museum', num: 2, cat: 'attraction', desc: 'Free museum covering Galway history and the Tribes' },
        { lat: 53.2748, lng: -9.0612, label: 'Galway Cathedral', num: 3, cat: 'attraction', desc: 'Stunning 1965 stone cathedral with JFK mosaic' },
        { lat: 53.2681, lng: -9.0580, label: 'Claddagh Village', num: 4, cat: 'attraction', desc: 'Ancient fishing village, birthplace of the Claddagh ring' },
        { lat: 53.2686, lng: -9.0601, label: 'Nimmo\'s Pier', num: 5, cat: 'attraction', desc: 'Pier with sweeping views of Galway Bay' },
        { lat: 53.2713, lng: -9.0539, label: 'McDonagh\'s Seafood House', num: 6, cat: 'food', desc: 'Legendary fish & chips since 1902 on Quay Street' }
      ]
    },
    {
      num: 3,
      date: '2026-05-03',
      neighborhoods: 'Salthill · Galway Bay · West End',
      title: 'Salthill Promenade & Sunset on the Bay',
      description: "Galway's seaside suburb is a short stroll or cycle from the city centre — a long Victorian promenade along Galway Bay, with views across to the Burren hills of County Clare. On a clear day you can see the Aran Islands on the horizon. May brings the prom back to life after winter — joggers, dog walkers, and ice cream queues forming at Moran's.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Galway Saturday Market',
              description: 'If it\'s a Saturday, start here — Galway\'s famous market spreads around St. Nicholas\' Collegiate Church on Market Street. Over 100 stalls sell Connemara smoked salmon, fresh oysters, artisan breads, jams, handmade jewellery, and West of Ireland crafts. It\'s the social heart of the city on weekends.',
              details: [
                '🦪 Connemara Smokehouse stall — the smoked salmon is life-changing',
                '🫙 Local jams, Connemara lamb, organic veg, fresh-baked scones',
                '📍 Market St, beside St. Nicholas\' Church — runs 8am–5pm Saturdays'
              ]
            },
            {
              title: 'St. Nicholas\' Collegiate Church',
              description: 'Founded in 1320, this is the largest medieval parish church still in use in Ireland. Christopher Columbus allegedly prayed here before his voyage to the Americas. The interior has fine medieval carvings, a leper\'s squint, and atmospheric stone vaulting.',
              details: [
                '⛪ Free entry, open Mon–Sat 9am–5:45pm',
                '🧭 Look for the medieval stone carvings and the Crusader tomb',
                '📜 Columbus connection: he visited Galway in 1477, before his famous voyage'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Salthill Promenade Walk',
              description: 'Walk or cycle the 2km Salthill Promenade along the shores of Galway Bay. On a clear day, the Burren\'s limestone hills are visible across the water and the Aran Islands shimmer on the horizon. The local tradition is to "kick the wall" at the end of the prom — you must do this.',
              details: [
                '🦶 Kicking the wall at the end of the prom is a sacred local ritual — do not skip',
                '🏊 Blackrock Diving Board: brave locals leap into the Atlantic from its 10m platform',
                '🏖️ Silver Strand Beach is 5 minutes south — quiet, sandy, and beautiful in May'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch / Ice Cream',
              name: 'Moran\'s Oyster Cottage',
              description: 'Technically in nearby Kilcolgan (20-min drive), but if you have wheels, this is a pilgrimage. Generations-old thatched pub serving Galway Bay oysters, fresh crab claws, and Guinness. The best oysters of your life in a thatched cottage by the sea.',
              meta: '💰 $$$ · 📍 The Weir, Kilcolgan · Worth the trip if you have a car/taxi'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from Salthill & Monroe\'s Trad Session',
              description: 'Time your return to catch sunset from the prom — one of the west of Ireland\'s great spectacles, with colours blazing over Galway Bay. Then head to Monroe\'s Tavern in the West End for their legendary Tuesday night trad session (or check the schedule for other nights).',
              details: [
                '🌅 May sunsets over Galway Bay: approximately 9:00–9:30pm',
                '🎶 Monroe\'s Tuesday sessions are famous — spontaneous dancing breaks out',
                '📍 Monroe\'s: 4 Dominick St Upper, West End'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Loam Restaurant',
              description: 'Michelin-starred, hyper-seasonal Irish cuisine using almost entirely Irish produce. Chef Enda McEvoy\'s tasting menu changes monthly — expect wild sea vegetables, Connemara lamb, foraged herbs, and west coast seafood. One of Ireland\'s great restaurants.',
              meta: '💰 $$$$ · 📍 Fairgreen Rd · Tasting menu only, reservations essential weeks ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2703, lng: -9.0548, label: 'Galway Saturday Market', num: 1, cat: 'attraction', desc: 'Best market in the west — oysters, smoked salmon, crafts' },
        { lat: 53.2704, lng: -9.0545, label: 'St. Nicholas\' Collegiate Church', num: 2, cat: 'attraction', desc: 'Largest medieval parish church in Ireland — Columbus connection' },
        { lat: 53.2604, lng: -9.0820, label: 'Salthill Promenade', num: 3, cat: 'attraction', desc: 'Victorian seaside walk along Galway Bay' },
        { lat: 53.2580, lng: -9.0880, label: 'Blackrock Diving Board', num: 4, cat: 'attraction', desc: 'Iconic diving tower — brave locals leap year-round' },
        { lat: 53.2720, lng: -9.0632, label: 'Monroe\'s Tavern', num: 5, cat: 'attraction', desc: 'West End trad sessions with legendary spontaneous dancing' }
      ]
    },
    {
      num: 4,
      date: '2026-05-04',
      neighborhoods: 'Inis Mór (Aran Islands)',
      title: 'Day Trip: The Aran Islands — Dún Aonghasa & the Edge of the World',
      description: "The Aran Islands are one of Ireland's most extraordinary places — three limestone islands rising from the Atlantic, where Irish is still the first language, where donkeys still work the fields, and where a 3,000-year-old cliff fort clings to a 90-metre precipice above the crashing sea. Inis Mór (Inishmore) is the largest and most visited — still quiet, wild, and utterly unlike anywhere else.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Ferry from Rossaveel to Inis Mór',
              description: 'Take the early shuttle bus from Galway city (departs ~8:30am from outside Galway Tourist Office) to Rossaveel ferry terminal, then the 40-min Aran Island Ferries crossing to Kilronan on Inis Mór. The crossing is exhilarating — Atlantic swells, seabirds, and the islands materialising from the haze.',
              details: [
                '⛴️ Aran Island Ferries: roundtrip €25–30, bus transfer ~€7 extra. Book in advance.',
                '🕗 First ferry departs Rossaveel ~9:00am, last return ~6:00pm',
                '📱 Book at aranislandferries.com or Doolin2AranFerries (from Doolin in Clare)',
                '🌊 Can be rough in bad weather — take seasickness tablets if prone'
              ]
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rent a Bike in Kilronan',
              description: 'The moment you step off the ferry in Kilronan, bicycle rental shops will be waiting. Rent one and you\'ll have the whole island at your pace — 14km long, completely flat, no cars to worry about. Ride west through stone-walled fields to the far end of the island.',
              details: [
                '🚲 Bikes: €10–15 for the day, multiple rental shops at the pier',
                '🗺️ Get a free island map from the rental shop or tourist office',
                '🧱 The stone walls are hand-built — some are 2,000 years old'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Dún Aonghasa (Dun Aengus) — Cliffside Fort',
              description: 'The crown jewel of the Aran Islands — a massive prehistoric stone fort built right on the edge of a sheer 90-metre cliff plunging into the Atlantic. There is no railing, no barrier. You crawl on your hands and knees to the precipice and look straight down into eternity. It\'s terrifying and magnificent in equal measure.',
              details: [
                '🏰 Entry €5, open daily 9:45am–6pm (closes earlier off-season)',
                '⚠️ No safety fence at the edge — genuinely dangerous, genuinely worth it',
                '📸 Wait for a gap in tour groups for clean photos — arrive early or late',
                '🧱 The "chevaux-de-frise" — a field of razor-sharp standing stones — defends the approach'
              ]
            }
          ],
          meals: [
            {
              type: '🥘 Lunch',
              name: 'Joe Watty\'s Bar',
              description: 'Back in Kilronan, Joe Watty\'s is the island\'s favourite pub-restaurant — seafood chowder, crab sandwiches, fresh fish and chips, all washed down with an island Guinness. Traditional music sessions happen spontaneously.',
              meta: '💰 $$ · 📍 Kilronan, Inis Mór · Cash preferred'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Explore the Limestone Landscape & Worm Hole',
              description: 'Cycle or walk to the Poll na bPéist (Worm Hole) — a perfectly rectangular natural tidal pool carved by the sea into the limestone, as if cut by machine. It looks completely artificial. Nearby Dún Dúchathair (Black Fort) is a smaller but equally atmospheric cliff fort, with fewer visitors.',
              details: [
                '🌊 The Worm Hole is used for Red Bull Cliff Diving competitions',
                '🏰 Dún Dúchathair: free entry, dramatically perched on the southern cliffs',
                '🧭 The south coast of the island is wilder and quieter than the north'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.1190, lng: -9.6630, label: 'Kilronan (Inis Mór Ferry Pier)', num: 1, cat: 'attraction', desc: 'Ferry arrival point — bike rental, pubs, tourist office' },
        { lat: 53.1255, lng: -9.7677, label: 'Dún Aonghasa', num: 2, cat: 'attraction', desc: '3,000-year-old cliff fort at 90m above the Atlantic — unmissable' },
        { lat: 53.1164, lng: -9.7594, label: 'Poll na bPéist (Worm Hole)', num: 3, cat: 'attraction', desc: 'Mysterious rectangular natural tidal pool in limestone' },
        { lat: 53.1141, lng: -9.7441, label: 'Dún Dúchathair (Black Fort)', num: 4, cat: 'attraction', desc: 'Wild clifftop fort with fewer crowds than Dún Aonghasa' },
        { lat: 53.1208, lng: -9.6660, label: 'Joe Watty\'s Bar', num: 5, cat: 'food', desc: 'Best pub on the island — seafood, Guinness, occasional sessions' }
      ]
    },
    {
      num: 5,
      date: '2026-05-05',
      neighborhoods: 'Cliffs of Moher · The Burren (County Clare)',
      title: 'Day Trip: Cliffs of Moher & The Burren\'s Moonscape',
      description: "One of Ireland's great days out. The Cliffs of Moher are among the most dramatic coastal scenery in Europe — 214 metres of sheer black rock faces stretching 14km along the Clare coast, battered by the Atlantic. Combine with the utterly alien landscape of The Burren — a vast limestone plateau scattered with Neolithic tombs, rare wildflowers, and medieval abbeys.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bus to the Cliffs of Moher',
              description: 'Take the Galway–Doolin bus (Bus Éireann route or private day tour) through County Clare. The approach to the cliffs is breathtaking — flat farmland suddenly ending in vertical ocean. Buy your ticket online to skip the queues; the visitor centre is well done but the cliffs themselves are the destination.',
              details: [
                '🚌 Bus Éireann route 350 from Galway, or multiple private day-tour operators (~€25)',
                '🎟️ Cliff ticket: €8 adult — prebook online at cliffsofmoher.ie',
                '⏰ Depart Galway by 9am to arrive by 10:30am before tour buses fill the car park',
                '🧥 Always cold and windy at the top — dress warmer than you think'
              ]
            },
            {
              title: 'Cliffs of Moher Walk',
              description: 'Walk south from the visitor centre to O\'Brien\'s Tower for the classic panoramic views, then continue along the coastal path. The further you walk, the fewer people. On a clear day you can see the Aran Islands to the north, the Loop Head Peninsula to the south, and the mountains of Connemara.',
              details: [
                '🏰 O\'Brien\'s Tower: built 1835 as a viewing tower — small extra fee to enter',
                '📸 The south-facing view from past the tower is the best composition',
                '⚠️ Stay behind the barriers — the rock is unstable and the wind is powerful',
                '🦅 Razorbills, puffins, choughs, and peregrine falcons nest in the cliff faces in May'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Burren Limestone Plateau',
              description: 'Drive or take a tour through The Burren — one of Europe\'s most extraordinary geological landscapes. Over 250 square kilometres of exposed grey limestone karst pavement, cut by deep cracks (grykes) where rare orchids and alpine flowers bloom in May. It looks like another planet — simultaneously barren and teeming with life.',
              details: [
                '🌸 May is the best month for Burren wildflowers: mountain avens, spring gentians, orchids',
                '🗿 Poulnabrone Dolmen: a 5,000-year-old Neolithic portal tomb — eerie and magnificent',
                '🏛️ Corcomroe Abbey: 12th-century Cistercian ruin in a hidden valley — few tourists',
                '🧭 The Burren Way is a marked walking trail if you want to go deep'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Burren Smokehouse',
              description: 'Stop in Lisdoonvarna — the Burren Smokehouse sells wild Atlantic smoked salmon and seafood. Buy provisions for a picnic on the limestone pavement, or eat at their simple café.',
              meta: '💰 $$ · 📍 Doolin Rd, Lisdoonvarna · Also visit the attached shop for take-home gifts'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 52.9720, lng: -9.4264, label: 'Cliffs of Moher', num: 1, cat: 'attraction', desc: '214m sea cliffs — one of Ireland\'s most iconic landscapes' },
        { lat: 52.9716, lng: -9.4307, label: 'O\'Brien\'s Tower', num: 2, cat: 'attraction', desc: '1835 viewing tower at the highest point of the cliffs' },
        { lat: 53.0484, lng: -9.1415, label: 'Poulnabrone Dolmen', num: 3, cat: 'attraction', desc: '5,000-year-old Neolithic portal tomb on the Burren plateau' },
        { lat: 52.9946, lng: -9.2876, label: 'Corcomroe Abbey', num: 4, cat: 'attraction', desc: '12th-century Cistercian ruin in the heart of the Burren' },
        { lat: 53.0350, lng: -9.2904, label: 'Burren Smokehouse', num: 5, cat: 'food', desc: 'Wild Atlantic smoked salmon — best in the west' }
      ]
    },
    {
      num: 6,
      date: '2026-05-06',
      neighborhoods: 'Connemara · Kylemore Abbey · Sky Road',
      title: 'Day Trip: Connemara — Wild Bogs, Kylemore & the Sky Road',
      description: "Connemara is Ireland's wild west — a vast landscape of bogland, glittering lakes, jagged mountains, and isolated Irish-speaking villages. The Twelve Bens mountains rise dramatically from the bog; white cottages dot the shore; Kylemore Abbey reflects in its lake like a fairy tale. This is the Ireland of the imagination, and it delivers.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive West into Connemara',
              description: 'Rent a car or join a Connemara day tour from Galway (multiple operators, ~€25–35). The drive west on the N59 is spectacular from the start — bog pools reflecting pink heather, the Twelve Bens mountains building on the horizon, occasional white-washed pubs in tiny villages.',
              details: [
                '🚗 Renting a car is ideal — freedom to stop anywhere. Book online, collect at Galway station',
                '🚌 Bus Éireann connects Galway to Clifden via the coast — or take a tour',
                '🏘️ Drive through the Gaeltacht (Irish-speaking area) — all signs are in Irish first'
              ]
            },
            {
              title: 'Kylemore Abbey',
              description: 'This neo-Gothic castle rising from the shores of Kylemore Lough is one of Ireland\'s most photographed buildings — and it earns every pixel. Built in 1867 by a Manchester millionaire for his wife, it later became a Benedictine convent. The walled Victorian garden is spectacular in May, and the lakeshore walk at dawn beats any photo.',
              details: [
                '🏰 Entry €15 — includes abbey, walled garden, and heritage centre',
                '🌸 The Victorian walled garden is blooming in May — glasshouses full of exotic plants',
                '🙏 Benedictine nuns still live here — their liturgy of the hours echoes through the chapel'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast / Coffee',
              name: 'Mitchell\'s Restaurant, Clifden',
              description: 'Clifden\'s most reliable spot for a solid full Irish breakfast before the day begins. Generous portions, good strong tea, and a view of the town square.',
              meta: '💰 $$ · 📍 Market St, Clifden'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Clifden & the Sky Road Loop',
              description: 'Clifden is the "capital of Connemara" — a beautiful small town with colourful shopfronts, excellent restaurants, and traditional music. Drive (or cycle) the Sky Road loop north of town: 12km of the most dramatic coastal scenery in Ireland, with views over the fjord-like Clifden Bay and the Atlantic beyond.',
              details: [
                '🚗 The Sky Road is 12km — can be done by car, bike, or on foot (allow 3–4hrs on foot)',
                '📸 The view from the top back toward Clifden Castle and the sea is perfection',
                '✈️ Alcock & Brown Memorial marks where the first transatlantic flight landed in 1919 — remarkable'
              ]
            },
            {
              title: 'Connemara National Park',
              description: 'Stop at the National Park visitor centre and take the Diamond Hill loop walk (7km, 2 hrs) — modest altitude but extraordinary views over the Twelve Bens, the bogland, and the coast. In May, the bog cotton is blowing white in the breeze like a ghostly carpet.',
              details: [
                '🏔️ Diamond Hill (445m) — manageable walk, tremendous views',
                '🌿 Park entry is free — just park and walk',
                '🦌 Red deer are often spotted in the bog at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Upstairs Downstairs, Clifden',
              description: 'A Clifden favourite with a cosy upstairs dining room — seafood chowder, Atlantic salmon, and a legendary seafood platter. Relaxed and excellent.',
              meta: '💰 $$ · 📍 Main St, Clifden'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.5578, lng: -9.8930, label: 'Kylemore Abbey', num: 1, cat: 'attraction', desc: 'Neo-Gothic castle and Benedictine convent on Kylemore Lough' },
        { lat: 53.4879, lng: -10.0206, label: 'Clifden Town', num: 2, cat: 'attraction', desc: 'Capital of Connemara — colourful pubs, restaurants, and music' },
        { lat: 53.5131, lng: -10.0492, label: 'Sky Road Viewpoint', num: 3, cat: 'attraction', desc: 'Most dramatic coastal loop in Connemara — Atlantic panoramas' },
        { lat: 53.5505, lng: -9.9497, label: 'Connemara National Park', num: 4, cat: 'attraction', desc: 'Diamond Hill trail — bog cotton, Twelve Bens views, red deer' },
        { lat: 53.5367, lng: -9.9867, label: 'Alcock & Brown Memorial', num: 5, cat: 'attraction', desc: 'Landing site of the world\'s first transatlantic flight, 1919' }
      ]
    },
    {
      num: 7,
      date: '2026-05-07',
      neighborhoods: 'Latin Quarter · West End · Galway Harbour',
      title: 'Galway Food Day & Oyster Feast',
      description: "A day to eat your way through Ireland's food capital. Galway has a remarkable food scene for a city of 80,000 — driven by the exceptional West of Ireland larder: Galway Bay oysters, Connemara lamb, wild Atlantic fish, and artisan producers across the region. Today is no day trips — just wandering, eating, and finding the best session you can.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Oyster Tasting at the Harbour',
              description: 'Galway Bay oysters are world-famous — native flat oysters from the cold, clean waters of the bay. The oyster festival is in September, but May oysters are superb. Head to the harbour area or the Saturday market and order a dozen with a glass of stout for the classic Galway breakfast.',
              details: [
                '🦪 Oyster etiquette: don\'t chew. Tip back, let the brine hit, swallow.',
                '🍺 A pint of Murphy\'s or Guinness stout with oysters is not a cliché — it\'s the perfect pairing',
                '📍 Galway Oyster Company stall at the market, or ask at any harbourside restaurant'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Dela Restaurant',
              description: 'Plant-forward brunch champions using west of Ireland ingredients. The granola parfait with local honey, the shakshuka with Connemara feta, and the excellent coffee all hit perfectly. One of Galway\'s most popular brunch spots — go early or expect a wait.',
              meta: '💰 $$ · 📍 51 Lower Dominick St, West End · Opens 9am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Galway Arts & Craft Shops',
              description: 'Wander the Latin Quarter\'s independent shops — Galway has a thriving craft scene. Look for hand-woven Aran sweaters (the real ones, not Chinese knock-offs), Claddagh rings from Thomas Dillion\'s, contemporary Irish art, and hand-thrown pottery.',
              details: [
                '🧶 Aran Sweater Market on Dominick St — huge selection, genuine Irish wool',
                '💍 Thomas Dillion\'s: est. 1750, the original Claddagh ring makers',
                '🎨 Galway Arts Centre: free gallery exhibitions — check what\'s on'
              ]
            },
            {
              title: 'Lynch\'s Castle & Medieval Galway',
              description: 'Lynch\'s Castle on Shop Street is one of Ireland\'s finest examples of a preserved medieval town mansion — a 16th-century fortified townhouse now functioning as a bank. Look for the carvings of gargoyles and coats of arms. Around the corner, the Lynch Memorial Window marks a dark piece of city history.',
              details: [
                '🏰 Lynch\'s Castle: free to enter the ground floor (it\'s a bank)',
                '🪟 Lynch Memorial Window: according to legend, Mayor Lynch hanged his own son for murder here in 1493',
                '🗺️ The old city walls can be traced through several sections around the town'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Pint at Jurys Inn Rooftop or The Quays',
              description: 'Catch pre-dinner drinks at a spot overlooking the Spanish Arch waterfront — The Quays bar has a spectacular view, or find a perch along the Long Walk with a takeaway can from an off-licence for a very Galway experience.',
              details: [
                '🌅 The Long Walk at golden hour, looking back to the Cathedral, is spectacular',
                '🍺 Off-licences on Quay Street sell single cans to take to the waterfront',
                '🎶 The Quays bar often has live music on weeknight evenings'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Aniar Restaurant',
              description: 'The other Michelin star in Galway — chef JP McMahon\'s love letter to Irish terroir. The tasting menu celebrates west of Ireland ingredients with deep technique: seaweed butter, wild Atlantic fish, hogget from Connemara hills, foraged sea vegetables. Essential.',
              meta: '💰 $$$$ · 📍 53 Lower Dominick St · Tasting menu only, book weeks ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2700, lng: -9.0546, label: 'Galway Saturday Market', num: 1, cat: 'food', desc: 'Oysters, smoked salmon, artisan produce — a feast for the senses' },
        { lat: 53.2717, lng: -9.0542, label: 'Lynch\'s Castle', num: 2, cat: 'attraction', desc: '16th-century medieval townhouse on Shop Street (now a bank)' },
        { lat: 53.2703, lng: -9.0548, label: 'Thomas Dillion\'s Jewellers', num: 3, cat: 'attraction', desc: 'Est. 1750 — original makers of the Claddagh ring' },
        { lat: 53.2727, lng: -9.0617, label: 'Dela Restaurant', num: 4, cat: 'food', desc: 'Plant-forward brunch champion in the West End' },
        { lat: 53.2727, lng: -9.0628, label: 'Aniar Restaurant', num: 5, cat: 'food', desc: 'Michelin-starred Irish terroir — best of the West on a plate' }
      ]
    },
    {
      num: 8,
      date: '2026-05-08',
      neighborhoods: 'Nuns Island · Galway Rowing Club · Bohemian West End',
      title: 'Hidden Galway — Nuns Island, the Corrib & the Bohemian Quarter',
      description: "The Galway that most visitors miss: the quieter west side of the River Corrib, the elegant Victorian Nuns Island theatre, the rowing clubs where Galway lads have rowed since the 1800s, the independent coffee shops and bookshops of the West End. A day for wandering slowly, reading, and discovering the city like a local.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Corrib Walk & Nuns Island',
              description: 'Cross to the west bank of the Corrib via the Wolfe Tone Bridge and follow the river south. The Nuns Island area is peaceful and residential — the Galway Arts Centre occupies a beautifully converted school, and the Dominican church has a remarkable rose window. The weir here is particularly dramatic after rain.',
              details: [
                '🏛️ Galway Arts Centre: free exhibitions, good café inside',
                '🌊 The university weir is where the Corrib is most powerful — spray reaches the path',
                '🚣 Galway Rowing Club has been racing on the Corrib since 1912'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Morning Coffee',
              name: 'Coffeewerk + Press',
              description: 'Galway\'s most serious coffee shop — exceptional single-origin espresso in a beautiful, bookshop-meets-roastery space. They also stock interesting journals, zines, and prints. The perfect quiet morning stop.',
              meta: '💰 $ · 📍 Churchyard St, Latin Quarter'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Galway City Museum Revisit & Long Walk Wander',
              description: 'If you skipped the museum earlier, revisit now — the "This Is Galway" exhibition about the 20th-century city is particularly good, including footage of the old Claddagh village before it was demolished in the 1930s. Then walk the Long Walk along the eastern bank of the Corrib toward the harbour — a genuinely lovely stroll.',
              details: [
                '🎬 Free entry — the film footage of old Galway is moving',
                '🦢 Mute swans nest along the Long Walk in May — keep respectful distance',
                '📸 View back toward the Corrib weir from the Long Walk is one of Galway\'s best'
              ]
            },
            {
              title: 'Galway Farmer\'s Market & Independent Bookshops',
              description: 'Browse the West End\'s independent shops: Charlie Byrne\'s Bookshop is one of Ireland\'s best second-hand bookshops — three rooms of organised chaos selling everything from Irish literature to rare travel books. Could easily lose a morning here.',
              details: [
                '📚 Charlie Byrne\'s: Middle St — ask staff for Galway literature recommendations',
                '🛍️ Galway has the highest concentration of independent shops in Ireland per capita',
                '🎨 Check out the Galway Arts Centre programme for evening events'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Roisín Dubh Live Music',
              description: 'Galway\'s premier live music venue — a basement club that has hosted everyone from Hozier to The Frames to emerging Irish acts. Check the gig guide for what\'s on during your visit. Even without a headline act, the bar itself is great — Guinness on draft, pool table, and the chat.',
              details: [
                '🎸 Check roisindubh.net for the May programme',
                '🎟️ Most gigs are €10–20 — book online to avoid sellouts',
                '📍 Dominick St Lower — 5-min walk from anywhere in the West End'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cava Bodega',
              description: 'Tapas-style small plates with a strong Spanish-Irish identity — Galway had a historic trade connection with Spain, and Cava Bodega celebrates it. Excellent wine list, vibrant atmosphere, and ideal for a solo diner at the bar tasting their way through the menu.',
              meta: '💰 $$$ · 📍 1 Middle St · Walk-ins usually fine, book for weekends'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2755, lng: -9.0628, label: 'Nuns Island', num: 1, cat: 'attraction', desc: 'Quiet west bank riverside — arts centre, convent, rowing clubs' },
        { lat: 53.2708, lng: -9.0562, label: 'Coffeewerk + Press', num: 2, cat: 'food', desc: 'Galway\'s best coffee — single-origin espresso and curated books' },
        { lat: 53.2696, lng: -9.0535, label: 'Galway City Museum', num: 3, cat: 'attraction', desc: 'Free museum with excellent footage of old Galway' },
        { lat: 53.2719, lng: -9.0612, label: 'Charlie Byrne\'s Bookshop', num: 4, cat: 'attraction', desc: 'One of Ireland\'s best second-hand bookshops' },
        { lat: 53.2726, lng: -9.0618, label: 'Roisín Dubh', num: 5, cat: 'attraction', desc: 'Galway\'s best live music venue — always something on' },
        { lat: 53.2723, lng: -9.0580, label: 'Cava Bodega', num: 6, cat: 'food', desc: 'Spanish-Irish tapas bar — great for solo dining at the bar' }
      ]
    },
    {
      num: 9,
      date: '2026-05-09',
      neighborhoods: 'Galway Bay · Connemara Coast Road · Roundstone',
      title: 'The Wild Atlantic Way Coastal Drive',
      description: "Take the scenic coastal road south from Galway — the R336 through Connemara hugs the shores of Galway Bay and the Atlantic, passing through small Irish-speaking villages, passing Mweenish and Lettermullan islands, and eventually reaching Roundstone, one of the most charming fishing villages in Ireland. A day for solitude, big skies, and the sea.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive the Connemara Coastal Road (R336)',
              description: 'Take the southern coastal road from Galway — through Barna, Spiddal, Casla, and into the Gaeltacht heartland. Spiddal has an excellent craft village worth stopping at. The road hugs the rocky Atlantic shore, with views across to the Aran Islands in the distance and Connemara mountains behind.',
              details: [
                '🚗 Route: Galway → Barna → Spiddal → Casla → Carna → Roundstone (~70km one way)',
                '🏘️ Spiddal Craft Village: potters, weavers, jewellers all working from traditional crafts',
                '📡 You\'re now deep in the Gaeltacht — Irish language is alive and everyday'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Roundstone & Malachy Kearns Bodhráns',
              description: 'Roundstone is a tiny fishing village built around a perfect harbour — painted boat hulls, lobster pots on the quay, and the Twelve Bens mountains rising behind. Visit Malachy Kearns\' workshop: the most famous bodhrán (Irish frame drum) maker in the world, crafting drums by hand since 1976.',
              details: [
                '🥁 Malachy Kearns (Roundstone Musical Instruments): watch a bodhrán being made, buy one to play',
                '🦞 The Roundstone harbourside has excellent fresh crab and lobster in season',
                '📸 The view from the quayside at Roundstone is postcard-perfect — Twelve Bens behind'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'O\'Dowd\'s Seafood Bar, Roundstone',
              description: 'The essential Roundstone lunch stop — a traditional pub and restaurant on the harbour serving superb local seafood: Connemara crab claws, smoked salmon, and pints of Guinness with a harbour view.',
              meta: '💰 $$ · 📍 Harbour, Roundstone'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dog\'s Bay & Gurteen Beach',
              description: 'Just outside Roundstone, Dog\'s Bay is one of Ireland\'s most beautiful beaches — a crescent of shell-sand facing an impossibly turquoise lagoon. The sand is made from foraminifera shells rather than quartz, giving it an unusual bright white colour. Almost certainly empty in May.',
              details: [
                '🏖️ Dog\'s Bay: almost certainly empty in May — you may have it to yourself',
                '🐚 The white sand is made from tiny shell fragments — look closely',
                '🌊 The water is clear but cold — hardy swimmers only in May'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Trad Session — Pick Your Favourite Pub',
              description: 'Back in Galway for your last night of sessions. By now you\'ll have favourites. Return to The Crane Bar for the upstairs session, or try Taaffes Bar on Shop Street — one of the most reliably excellent trad pubs in the city. Order a final round, tip the musicians, and soak in every note.',
              details: [
                '🎻 Taaffes: Shop St — known for marathon sessions that go late into the night',
                '🪗 Tig Coili on Mainguard St is another local favourite for sessions',
                '🍺 One more pint of the black stuff — you\'ve earned it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Brasserie on the Corner',
              description: 'Multi-award-winning restaurant in a beautiful Victorian corner building on Eyre Square — exceptional steaks, wild Atlantic seafood, and an outstanding wine list. Perfect for a celebratory last dinner in Galway.',
              meta: '💰 $$$ · 📍 Eglinton St, Eyre Square · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2430, lng: -9.1410, label: 'Spiddal (An Spidéal)', num: 1, cat: 'attraction', desc: 'First major Gaeltacht village — craft shops and sea views' },
        { lat: 53.3879, lng: -9.9821, label: 'Roundstone Village', num: 2, cat: 'attraction', desc: 'Charming fishing harbour with Twelve Bens backdrop' },
        { lat: 53.3825, lng: -9.9201, label: 'Malachy Kearns Bodhráns', num: 3, cat: 'attraction', desc: 'World-famous hand-made bodhrán workshop' },
        { lat: 53.3722, lng: -9.9230, label: 'Dog\'s Bay Beach', num: 4, cat: 'attraction', desc: 'Shell-sand beach of impossible turquoise — often empty in May' },
        { lat: 53.2742, lng: -9.0510, label: 'Brasserie on the Corner', num: 5, cat: 'food', desc: 'Award-winning steaks and seafood on Eyre Square' },
        { lat: 53.2726, lng: -9.0520, label: 'Taaffes Bar', num: 6, cat: 'attraction', desc: 'Reliably excellent late trad sessions on Shop Street' }
      ]
    },
    {
      num: 10,
      date: '2026-05-10',
      neighborhoods: 'Latin Quarter · Shop Street · Claddagh',
      title: 'Last Morning — Soda Bread, Claddagh Rings & Goodbye Galway',
      description: "A gentle final morning before heading home. Buy your Claddagh ring, stock up on smoked salmon and Irish whiskey for friends back home, have one last strong tea and brown bread breakfast, and walk the Corrib one final time. The west of Ireland will call you back — it always does.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Breakfast & Corrib Walk',
              description: 'Start with a proper Irish breakfast — eggs, rashers, white pudding, black pudding, soda bread, and strong tea. Then walk the river one last time. The Corrib in morning light is different from every other time — quieter, more silver, more yours.',
              details: [
                '🍳 Full Irish breakfast is a meal, not a snack — plan accordingly',
                '🦢 The swans are always on the river in the morning',
                '📷 Take the photo you forgot to take earlier — the river, the Cathedral, the weir'
              ]
            },
            {
              title: 'Claddagh Ring Shopping & Last Gifts',
              description: 'If you haven\'t bought a Claddagh ring yet, Thomas Dillion\'s is the only choice — they\'ve been making them since 1750. For food gifts: Sheridan\'s Cheesemongers on Churchyard Street for Irish farmhouse cheese; Moran\'s at the market for smoked salmon vacuum-packed for travel; Celtic Whiskey Shop for a bottle of Connemara single malt.',
              details: [
                '💍 Claddagh ring tradition: worn on right hand, heart pointing out = single; heart in = taken',
                '🧀 Sheridan\'s Cheesemongers: the definitive Irish artisan cheese selection',
                '🥃 Connemara Peated Single Malt — tastes like bog and rain and Atlantic salt'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Last Breakfast',
              name: 'Gourmet Tart Co.',
              description: 'Galway\'s beloved bakery-café chain — extraordinary pastries, proper brown bread with Kerry Gold butter, strong coffee, and everything made on-site. The croissants and brown bread scones are dangerous. The perfect final Galway morning.',
              meta: '💰 $ · 📍 Multiple locations — Eyre Square and Shop Street'
            }
          ],
          tips: [
            { type: 'tip', text: 'Bus Éireann to Dublin Airport runs regularly from Galway Bus Station on Eyre Square — express services take ~3.5 hours. Book online to guarantee your seat and get the best price.' }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2703, lng: -9.0548, label: 'Thomas Dillion\'s Jewellers', num: 1, cat: 'attraction', desc: 'Buy your Claddagh ring from the original — est. 1750' },
        { lat: 53.2712, lng: -9.0556, label: 'Sheridan\'s Cheesemongers', num: 2, cat: 'food', desc: 'Irish farmhouse cheese and artisan food gifts' },
        { lat: 53.2735, lng: -9.0498, label: 'Galway Bus Station (Eyre Square)', num: 3, cat: 'attraction', desc: 'Buses to Dublin Airport and onward connections' },
        { lat: 53.2741, lng: -9.0488, label: 'Gourmet Tart Co.', num: 4, cat: 'food', desc: 'Galway\'s best pastries and brown bread for the road' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (solo)', budget: '€35–60/night (hostel/guesthouse)', midrange: '€90–160/night (B&B/hotel)', luxury: '€180–350/night (boutique)' },
    { category: 'Meals', budget: '€25–40/day', midrange: '€55–90/day', luxury: '€120–250/day' },
    { category: 'Day Trips (transport)', budget: '€20–30/trip (bus tours)', midrange: '€30–60/trip (private tours)', luxury: '€80–150/trip (car hire + guides)' },
    { category: 'Activities & Entries', budget: '€10–20/day', midrange: '€20–40/day', luxury: '€50–100/day' },
    { category: 'Pints & Sessions', budget: '€15–25/day', midrange: '€25–40/day', luxury: 'Unlimited (it\'s Ireland)' },
    { category: '10-Day Total (solo)', budget: '€800–1,200', midrange: '€1,400–2,200', luxury: '€3,000–5,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting to Galway', items: ['Fly into Dublin Airport (DUB) — express Bus Éireann to Galway takes 3.5 hrs (€15–20)', 'Fly into Shannon Airport (SNN) — closer option, Bus Éireann to Galway 1.5 hrs (€12)', 'Train from Dublin Heuston to Galway Ceannt Station: 2hrs 15mins from €15 one way', 'Ireland West Airport Knock (NOC) — budget Ryanair hub, 1hr drive from Galway'] },
    { title: '🏨 Where to Stay', items: ['The Hardiman Hotel — historic 5-star on Eyre Square, the grande dame of Galway', 'Park House Hotel — boutique luxury, walking distance to everything', 'Halo Loft Hostel — excellent social hostel near the Latin Quarter, great for solo travelers', 'The House Hotel — stylish boutique in the Latin Quarter, perfect location', 'Airbnb in the West End — stay in a local neighbourhood for €70–120/night'] },
    { title: '🌡️ May Weather', items: ['Average 12–17°C (54–63°F) — mild but changeable', 'Daylight until ~9:30pm — long Atlantic evenings', 'Rain is likely — pack a good waterproof shell jacket (not optional)', 'May has less rain than winter and far fewer tourists than summer', 'Layers are essential — can be cold at the cliffs even on sunny days'] },
    { title: '💳 Money & Costs', items: ['Euro (€) — Ireland is moderately expensive by EU standards', 'Cards accepted almost everywhere — contactless standard', 'Pubs vary: some session pubs are cash-only', 'Pint of Guinness: €5.50–6.50 in Galway (cheaper than Dublin)', 'Tip: 10–15% at restaurants is appreciated but not obligatory'] },
    { title: '📱 Getting Connected', items: ['Buy a Three Ireland or Vodafone Ireland SIM at the airport or any phone shop', 'eSIM: Airalo offers Ireland plans from €4/GB — activate before you land', 'Most pubs and cafés have free WiFi', 'Offline maps essential for Connemara — signal drops in the bogs', 'Download the Waze or Google Maps area for Connemara before leaving Galway'] },
    { title: '🎵 Trad Music Tips', items: ['Sessions are free — just buy a drink and respect the musicians', 'Best session pubs: The Crane Bar, Tigh Neachtain, Taaffes, Monroe\'s, Tig Coili', 'Sessions start around 9pm — arrive 30 mins early for a seat', 'Never talk over the music — wait for breaks to chat', 'A bodhrán or tin whistle makes a great souvenir if you want to try playing yourself'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
