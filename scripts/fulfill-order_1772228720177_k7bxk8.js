const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772228720177_k7bxk8',
  email: 'mailannez@gmail.com',
  destination: 'Ireland',
  startDate: '2026-04-20',
  endDate: '2026-04-27',
  groupSize: 1,
  requests: "I'd love recommendations to get to know people during my trip, but I don't like hostels."
};

const itineraryData = {
  destination: 'Ireland',
  countryEmoji: '🇮🇪',
  title: 'Ireland Solo: Pubs, Cliffs & Craic',
  subtitle: '7 days of adventure, culture, and genuine Irish connection for a solo explorer',
  description: "Ireland in April is pure magic — the landscape erupts in fifty shades of green, the pubs are full of locals ready to chat, and the ancient castles feel almost to yourself. This itinerary mixes Dublin's vibrant pub culture, the wild Atlantic coast, the dramatic Cliffs of Moher, and the craic of Galway — all designed for a solo traveler who wants to connect with people, explore on their own terms, and eat brilliantly without breaking the bank. No hostels, all heart.",
  duration: '7 nights',
  dates: 'Apr 20 – Apr 27, 2026',
  budget: '$',
  pace: 'Active',
  bestFor: 'Solo Traveler',
  highlights: [
    'Pub crawl through Dublin\'s Temple Bar and local neighborhoods',
    'Free walking tours to meet fellow travelers and locals',
    'Cliffs of Moher day trip on the Wild Atlantic Way',
    'Galway\'s colorful medieval streets and live music',
    'Blarney Castle and Cork food market',
    'Traditional music sessions in cozy Irish pubs',
    'Giant\'s Causeway coastal scenery'
  ],

  essentials: [
    { title: '🌧️ April Weather', text: 'Expect anything — sun, rain, and wind all in one day. Pack layers, a waterproof jacket, and walking shoes. The rain never lasts long, and the landscapes after a shower are otherworldly.' },
    { title: '🚌 Getting Around', text: 'Dublin has excellent buses and the Luas tram. For day trips, Bus Éireann runs to most destinations, or book organized tours (great for meeting people). Renting a car is ideal for flexibility in the west.' },
    { title: '🍺 Pub Culture', text: 'The pub is Ireland\'s living room. Sitting at the bar almost always leads to conversation. Traditional music sessions (seisiúns) happen most evenings — just pull up a stool and listen. Tipping is appreciated but not mandatory.' },
    { title: '💶 Money', text: 'Ireland uses the Euro. Cards are accepted almost everywhere, but carry €20–40 cash for small pubs and market stalls. Budget €60–80/day covers accommodation, food, and activities comfortably at this price level.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-20',
      neighborhoods: 'Dublin City Centre · Temple Bar · Grafton Street',
      title: 'Dublin Arrival — First Pints & First Friends',
      description: "Touch down in Dublin, drop your bags, and dive straight into one of the world's great city pub cultures. April light lingers late, and the city center is made for wandering. A free walking tour this evening is the single best way to meet fellow travelers and get your bearings.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & First Wander',
              description: "Check into your guesthouse or B&B near the city center. Dublin's south side — around St. Stephen's Green or Portobello — puts you within walking distance of everything. Drop your bags and head straight out.",
              details: [
                '🏨 Recommended areas: Portobello, Ranelagh, or near St. Stephen\'s Green',
                '💰 B&Bs in these neighborhoods run €70–120/night — more personal than hotels',
                '🚌 Dublin Bus or Airlink connects airport to city center in 30–45 min (€7)'
              ]
            },
            {
              title: 'Trinity College & Book of Kells',
              description: "Walk through the cobbled grounds of Trinity College — one of Europe's oldest and most beautiful universities. The Book of Kells exhibition is world-class; queue early as it can get busy.",
              details: [
                '📚 Book of Kells exhibition: €16 entry, worth every cent',
                '🌳 The college grounds are free to wander',
                '📸 The Long Room library is jaw-dropping — a Harry Potter fever dream'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Late Lunch',
              name: 'Bunsen Burger, Wexford St',
              description: 'No-frills, exceptional smash burgers. Tiny menu, huge flavour. A Dublin institution beloved by locals.',
              meta: '💰 $ · 📍 Wexford St, Dublin 2'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Free Walking Tour (Evening)',
              description: "Dublin Discovered and Discover Dublin both run excellent free evening walking tours — perfect for meeting other solo travelers. You'll see Temple Bar, Dublin Castle, and Christ Church while swapping travel stories.",
              details: [
                '🚶 Tours leave from College Green most evenings at 6pm',
                '💬 Free tours attract great people — book online but tip your guide',
                '📍 Meet at the Molly Malone statue, Grafton St'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Drinks & Pub Dinner',
              name: 'The Long Hall, South Great George\'s St',
              description: "One of Dublin's most beautiful Victorian pubs. Ask the bartender for a recommendation — they'll tell you everything worth knowing about Dublin. Great pub grub and Guinness poured perfectly.",
              meta: '💰 $ · 📍 51 South Great George\'s St · No reservations needed'
            }
          ],
          tips: [
            { type: 'tip', text: 'Sit at the bar, not a table — it\'s how you meet people in Ireland. Irish pub culture is open and welcoming; a simple "where are you from?" goes a long way.' }
          ]
        }
      ],
      mapPins: [
        { lat: 53.3438, lng: -6.2546, label: 'Trinity College', num: 1, cat: 'attraction', desc: 'Book of Kells, Long Room, beautiful campus' },
        { lat: 53.3430, lng: -6.2679, label: 'Temple Bar', num: 2, cat: 'attraction', desc: 'Dublin\'s cultural quarter — cobblestones and live music' },
        { lat: 53.3417, lng: -6.2619, label: 'The Long Hall Pub', num: 3, cat: 'food', desc: 'Beautiful Victorian pub, great Guinness, local crowd' },
        { lat: 53.3442, lng: -6.2594, label: 'Molly Malone Statue', num: 4, cat: 'attraction', desc: 'Free walking tour meeting point, Grafton St' },
        { lat: 53.3398, lng: -6.2678, label: 'Dublin Castle', num: 5, cat: 'attraction', desc: 'Historic seat of British rule in Ireland' }
      ]
    },
    {
      num: 2,
      date: '2026-04-21',
      neighborhoods: 'Dublin · Kilmainham · Portobello · Docklands',
      title: 'Dublin Deep Dive — History, Markets & Music',
      description: "A full day immersed in Dublin's layers. Morning at Kilmainham Gaol — the most moving museum in Ireland — then the creative buzz of the Liberties neighborhood, the George's Street Arcade, and finishing with a proper traditional music session.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kilmainham Gaol',
              description: "This Victorian prison held the leaders of the 1916 Easter Rising, who were executed in the courtyard. The guided tour is one of Ireland's most powerful cultural experiences — emotional, informative, and essential for understanding modern Irish identity.",
              details: [
                '🏛️ Book tickets online in advance — sells out weeks ahead',
                '⏱️ Tours run every 30–45 min; allow 1.5–2 hours total',
                '💔 The execution yard where the 1916 leaders were shot is haunting'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Fumbally Café, The Liberties',
              description: 'Dublin\'s most beloved brunch spot — a spacious, relaxed café where creatives, locals, and travelers mix. Big communal tables are perfect for striking up conversations.',
              meta: '💰 $ · 📍 Fumbally Lane, The Liberties · Cash & card accepted'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'George\'s Street Arcade & Portobello',
              description: "Wander through Dublin's oldest market arcade, then explore the vintage shops and coffee bars of Portobello — Dublin's coolest neighborhood. Browse, people-watch, and pick up a second-hand Irish sweater.",
              details: [
                '🛍️ George\'s Street Arcade: vintage clothes, crystals, street food stalls',
                '☕ Industry & Co or Cloud Picker Coffee for excellent coffee',
                '🧶 Aran sweater from a charity shop for €10–20 beats any tourist shop'
              ]
            },
            {
              title: 'EPIC The Irish Emigration Museum',
              description: "This interactive museum in the CHQ building tells the story of Ireland's 10 million emigrants and their impact on the world. Genuinely moving and brilliantly designed — perfect for solo exploration.",
              details: [
                '🏅 Named Europe\'s Leading Tourist Attraction multiple times',
                '💰 €16.50 entry · 📍 CHQ Building, Custom House Quay',
                '⏱️ Allow 1.5–2 hours'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Traditional Music Session',
              description: "Head to Mulligan's of Poolbeg Street or The Cobblestone in Smithfield for a genuine traditional music session. These are locals' pubs where the music flows naturally from 9pm onward — just find a spot and let the sound wash over you.",
              details: [
                '🎻 The Cobblestone, Smithfield: legendary trad sessions nightly',
                '🥁 O\'Donoghue\'s, Merrion Row: where The Dubliners got their start',
                '🍺 Arrive by 8:30pm to get a seat — sessions fill up fast'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Grano, Ranelagh',
              description: 'Italian-Irish fusion in a warm, relaxed neighborhood spot. Outstanding pasta, natural wines, and a lively crowd. One of the best value dinners in Dublin.',
              meta: '💰 $$ · 📍 Ranelagh Village · Book a day ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.3417, lng: -6.3102, label: 'Kilmainham Gaol', num: 1, cat: 'attraction', desc: 'The most powerful museum in Ireland — 1916 Rising history' },
        { lat: 53.3411, lng: -6.2763, label: 'Fumbally Café', num: 2, cat: 'food', desc: 'Dublin\'s most beloved brunch — communal tables, great craic' },
        { lat: 53.3416, lng: -6.2636, label: 'George\'s Street Arcade', num: 3, cat: 'attraction', desc: 'Victorian market arcade with vintage, food, and crafts' },
        { lat: 53.3474, lng: -6.2456, label: 'EPIC Emigration Museum', num: 4, cat: 'attraction', desc: 'Europe\'s leading tourist attraction — Irish diaspora story' },
        { lat: 53.3487, lng: -6.2779, label: 'The Cobblestone', num: 5, cat: 'food', desc: 'Legendary trad music sessions, locals\' pub in Smithfield' }
      ]
    },
    {
      num: 3,
      date: '2026-04-22',
      neighborhoods: 'Dublin · Howth · Malahide',
      title: 'Coastal Escape — Howth Cliff Walk & Seafood',
      description: "Take the DART train north to Howth, a fishing village perched on a dramatic headland. Walk the cliff loop trail with sweeping Irish Sea views, visit the harbor, and feast on the freshest seafood you've ever eaten — straight off the boats.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'DART to Howth',
              description: "The Dublin Area Rapid Transit (DART) hugs the coast from Connolly Station to Howth — 35 minutes of sea views. Arrive in Howth by 9:30am before the day-trippers arrive.",
              details: [
                '🚂 DART from Connolly or Tara St Station to Howth (€4.20 each way)',
                '⏱️ 35 minutes, runs every 30 min',
                '🎒 Bring snacks and a water bottle for the cliff walk'
              ]
            },
            {
              title: 'Howth Cliff Walk',
              description: "The Howth Cliff Walk is one of Ireland's best coastal hikes — dramatic sea stacks, heather moorland, and views across Dublin Bay to the Wicklow Mountains. The full loop is 14km (3 hours), but the shorter summit loop (5km, 1.5 hours) is stunning.",
              details: [
                '🥾 Full loop: 14km, 3–4 hours · Short loop: 5km, 1.5 hours',
                '🌊 The eastern cliffs drop dramatically — stay on the path',
                '🌸 April: gorse and heather begin blooming — extraordinary colors',
                '📸 Baily Lighthouse on the southern tip is the must-see'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Howth Harbour & Fish Market',
              description: "After the walk, stroll back to the harbor. Howth's fishing boats bring in fresh catches every day. The harbor area has excellent chippers and seafood restaurants where you can eat outside watching boats return.",
              details: [
                '🦞 Octopussy\'s Seafood Shack: lobster rolls, crab claws, langoustines',
                '🐟 Wrights of Howth: fresh fish and chips eaten on the pier',
                '🛍️ The West Pier has a small artisan market on weekends'
              ]
            }
          ],
          meals: [
            {
              type: '🦀 Seafood Lunch',
              name: 'Octopussy\'s Seafood Shack',
              description: 'Fresh-caught seafood eaten at outdoor tables overlooking the harbor. The lobster roll and crab claws are legendary. This is what you came to Ireland for.',
              meta: '💰 $$ · 📍 Howth Harbour West Pier · Cash preferred'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Dublin — Docklands Evening',
              description: "DART back to the city center, then explore the Docklands area around Grand Canal Dock — Dublin's creative tech quarter — before heading back to Temple Bar for an evening pint.",
              details: [
                '🏗️ Grand Canal Dock: Google, Facebook, Airbnb HQs and hip bars',
                '🎭 Bord Gáis Energy Theatre nearby for evening shows (check listings)',
                '🌙 Mulligan\'s of Poolbeg Street for a late pint — Dublin\'s oldest pub (est. 1782)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Leo Burdock\'s Fish & Chips',
              description: "Dublin's most famous chipper. Simple, perfect fish and chips wrapped in paper, eaten walking along the Liffey quays. The unofficial Dublin ritual.",
              meta: '💰 $ · 📍 Multiple locations · Cash · Eat standing up by the river'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.3899, lng: -6.0640, label: 'Howth Cliff Walk', num: 1, cat: 'attraction', desc: 'Dramatic coastal hike with sea stacks and sea views' },
        { lat: 53.3875, lng: -6.0699, label: 'Howth Harbour', num: 2, cat: 'attraction', desc: 'Fishing village harbor with fresh seafood shacks' },
        { lat: 53.3878, lng: -6.0718, label: 'Octopussy\'s Seafood Shack', num: 3, cat: 'food', desc: 'Best seafood in Howth — lobster rolls at harbor edge' },
        { lat: 53.3423, lng: -6.2498, label: 'Grand Canal Dock', num: 4, cat: 'attraction', desc: 'Dublin\'s creative tech hub — bars, theatre, waterside walks' },
        { lat: 53.3452, lng: -6.2666, label: 'Mulligan\'s Pub', num: 5, cat: 'food', desc: 'Dublin\'s oldest pub (est. 1782) — proper Guinness' }
      ]
    },
    {
      num: 4,
      date: '2026-04-23',
      neighborhoods: 'Cork · English Market · Shandon · Blarney',
      title: 'Cork & Blarney — Ireland\'s Food Capital',
      description: "Train south to Cork — Ireland's culinary capital and the country's second city. A fiercely independent city with its own culture, slang, and extraordinary food scene. Morning at the legendary English Market, afternoon at Blarney Castle, and an evening exploring Cork's lively bar scene.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Cork & Check In',
              description: "Irish Rail runs hourly from Heuston Station, Dublin to Cork Kent — 2.5 hours through rolling Irish countryside. Arrive in Cork and drop your bags at your guesthouse in the city center.",
              details: [
                '🚂 Irish Rail Dublin Heuston → Cork Kent: €29–55 (book ahead for best price)',
                '⏱️ 2.5 hours — comfortable seats, café car, stunning scenery',
                '🏨 Recommended: Jurys Inn Cork or a B&B on MacCurtain Street (~€80–100/night)'
              ]
            },
            {
              title: 'English Market',
              description: "One of the finest food markets in Europe, operating continuously since 1788. Butchers, fishmongers, cheesemongers, artisan bakers, and street food traders. This is Cork at its finest — vibrant, local, proud.",
              details: [
                '🛒 Free to enter · Open Mon–Sat 8am–6pm',
                '🧀 Iago cheese stall: best Irish farmhouse cheese selection',
                '🥐 The Market Café upstairs has a brilliant lunch menu',
                '🐟 Sean Calder-Potts: Cork\'s legendary fishmonger'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Market Lane, Cork',
              description: 'Beloved Cork institution near the English Market. Modern Irish cuisine with incredible local produce. The weekend lunch is excellent value and draws a mix of Cork regulars and visitors.',
              meta: '💰 $$ · 📍 5 Oliver Plunkett St · Book ahead for lunch'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Blarney Castle & Gardens',
              description: "Take a bus (or taxi, €15) 8km northwest of Cork to Blarney Castle. Climb the medieval tower and kiss the Blarney Stone for the 'gift of the gab'. The castle grounds — gardens, poison garden, wishing steps — are extensive and atmospheric.",
              details: [
                '🏰 Entry: €18 · Gardens included · Allow 2–3 hours',
                '💋 The Blarney Stone: lean over backwards on top of the tower to kiss it — a guide holds you',
                '🌿 The Rock Close: druid\'s garden with ancient yew trees and wishing steps',
                '🚌 Bus 215 from Parnell Pl, Cork city, takes 30 min (€3 each way)'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Cork Evening — Live Music on Leeside',
              description: "Cork's bar scene is excellent and far less touristy than Dublin's. The Douglas Hyde area and South Main Street have brilliant pubs with live music. Sin É bar on Coburg Street is a Cork institution for trad music.",
              details: [
                '🎸 Sin É Bar: nightly live music, all genres, brilliant atmosphere',
                '🍺 The Franciscan Well Brewpub: Cork\'s best craft brewery with outdoor garden',
                '🎵 The Oliver Plunkett Bar: great late-night live bands'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner & Drinks',
              name: 'The Franciscan Well Brewpub',
              description: "Cork's most celebrated craft brewery, housed in a former Franciscan monastery with a sprawling outdoor courtyard. Excellent pizzas from their wood-fired oven alongside their own-brewed beers.",
              meta: '💰 $ · 📍 14 North Mall, Cork · No reservation needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.8979, lng: -8.4731, label: 'English Market', num: 1, cat: 'attraction', desc: 'Europe\'s finest Victorian food market — Cork\'s soul' },
        { lat: 51.8980, lng: -8.4747, label: 'Market Lane Restaurant', num: 2, cat: 'food', desc: 'Modern Irish cuisine with local Cork produce' },
        { lat: 51.9290, lng: -8.5701, label: 'Blarney Castle', num: 3, cat: 'attraction', desc: 'Kiss the Blarney Stone — medieval tower and gardens' },
        { lat: 51.9010, lng: -8.4685, label: 'Franciscan Well Brewpub', num: 4, cat: 'food', desc: 'Cork\'s best craft brewery — pizza and outdoor courtyard' },
        { lat: 51.9002, lng: -8.4741, label: 'Sin É Bar', num: 5, cat: 'food', desc: 'Cork institution — nightly live music and trad sessions' }
      ]
    },
    {
      num: 5,
      date: '2026-04-24',
      neighborhoods: 'Galway City · Latin Quarter · West End',
      title: 'Galway — The City of the Tribes',
      description: "Bus or train to Galway — the beating creative heart of the west of Ireland. A medieval city with a colorful, pedestrian-friendly center, a world-class arts scene, and the most vibrant pub culture in the country. Galway is the city where Ireland feels most alive.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bus/Train to Galway',
              description: "Bus Éireann runs from Cork to Galway (changing at Limerick or direct via Citylink). Alternatively, trains run Dublin → Galway in under 2 hours (if you prefer routing back through Dublin).",
              details: [
                '🚌 Citylink Cork → Galway: 3.5 hours, direct, €15–20',
                '🚂 Alternative: Cork → Limerick Junction → Galway by train',
                '🏨 Galway city center B&Bs: Adare Guest House, Sleepzone B&B (~€70–90/night)'
              ]
            },
            {
              title: 'Galway City Wander',
              description: "Galway's medieval Latin Quarter is entirely walkable — Shop Street, Quay Street, and the Spanish Arch are full of buskers, street art, and independent cafés. The city feels like a festival every day.",
              details: [
                '🎸 Shop Street: Ireland\'s best busking pitch — world-class street musicians',
                '⛪ Galway Cathedral: free, magnificent limestone building on the River Corrib',
                '🌊 Spanish Arch: 16th-century city gate where locals sunbathe by the river'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Ard Bia at Nimmos, Galway',
              description: "Set in a medieval stone building by the Spanish Arch, Ard Bia is Galway's most beloved brunch spot. West of Ireland produce, open kitchen, and a crowd that perfectly represents Galway — creative, friendly, and unhurried.",
              meta: '💰 $$ · 📍 Spanish Arch, Galway · Queue early weekends'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Galway City Museum & Salthill Walk',
              description: "The free Galway City Museum tells the story of the city from medieval times to today. Then stroll 2km along the prom to Salthill — the classic Galway promenade beside Galway Bay — and kick the wall at the end (a local tradition).",
              details: [
                '🏛️ Galway City Museum: free entry, excellent exhibitions',
                '🌊 The Salthill promenade: 2km seafront walk with Aran Islands views on clear days',
                '👟 Kicking the wall at the end of the prom is a Galway tradition — locals do it every walk'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Galway Pub Crawl & Trad Music',
              description: "Galway has Ireland's highest concentration of pubs per capita. The Quays, Tigh Coili, and Tig Cóilí are legendary for nightly trad sessions. The city center is so compact that pub hopping requires no planning at all — just follow the music.",
              details: [
                '🎻 Tigh Coilí, Mainguard St: legendary trad sessions from 6pm daily',
                '🎵 The Quays: massive medieval pub in a converted church',
                '🍺 Monroe\'s Tavern: brilliant trad + set dancing on weekend nights',
                '💬 Galway is incredibly social — sit at the bar anywhere and you\'ll have company within minutes'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Wa Café, Galway',
              description: "Galway's beloved Japanese café — seriously good ramen and gyoza at budget prices. Tiny, cosy, and packed with a mix of students, locals, and travelers. Perfect solo dining spot.",
              meta: '💰 $ · 📍 Dominick St Upper · No reservations, turn up early'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 53.2719, lng: -9.0534, label: 'Shop Street / Latin Quarter', num: 1, cat: 'attraction', desc: 'Galway\'s pedestrian heart — buskers, shops, pubs' },
        { lat: 53.2699, lng: -9.0547, label: 'Spanish Arch', num: 2, cat: 'attraction', desc: '16th-century gate, river sunbathing spot, Ard Bia nearby' },
        { lat: 53.2697, lng: -9.0543, label: 'Ard Bia at Nimmos', num: 3, cat: 'food', desc: 'Galway\'s best brunch in a medieval stone building' },
        { lat: 53.2618, lng: -9.0809, label: 'Salthill Prom', num: 4, cat: 'attraction', desc: 'Seafront walk with Galway Bay views and the famous wall-kick' },
        { lat: 53.2741, lng: -9.0546, label: 'Tigh Coilí', num: 5, cat: 'food', desc: 'Legendary trad music sessions from 6pm daily' }
      ]
    },
    {
      num: 6,
      date: '2026-04-25',
      neighborhoods: 'Cliffs of Moher · Burren · Doolin',
      title: 'Cliffs of Moher & The Burren',
      description: "The day trip Ireland is famous for. The Cliffs of Moher plunge 214m into the wild Atlantic — one of the most dramatic natural sights in Europe. Combine with the otherworldly limestone landscape of The Burren and the traditional music village of Doolin for a perfect Wild Atlantic Way day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cliffs of Moher Tour from Galway',
              description: "Join a guided day tour from Galway — they leave from Eyre Square from 9am and include the Cliffs, the Burren, and Doolin village. Organized tours are great for meeting fellow travelers. Alternatively, rent a car and drive solo for more flexibility.",
              details: [
                '🚌 Paddywagon or Galway Tour Company day tours: €30–35 per person',
                '🚗 Car rental from Galway: ~€45–60/day — gives you total freedom',
                '⏱️ Full day trip: depart 9am, return 6:30pm',
                '🎒 Bring layers — the cliffs are extremely exposed to Atlantic wind'
              ]
            },
            {
              title: 'Cliffs of Moher',
              description: "Stand at the edge of Europe. The cliffs stretch 14km along the Clare coast and rise to 214m at their highest point. O'Brien's Tower at the highest point offers 360° views. April light makes the green fields against the black cliffs extraordinary.",
              details: [
                '🌊 Entry to cliff walk: €8 (covers visitor centre)',
                '⚠️ Stay well back from the unfenced sections — winds can be sudden and fierce',
                '📸 Walk south of the visitor center to leave the crowds behind',
                '🐦 Puffins begin arriving in April — look on the cliff faces below'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Burren',
              description: "Drive or be driven through the Burren — 250 square kilometres of exposed limestone pavements that look like the surface of the moon. Yet between the rocks, rare Arctic and Mediterranean wildflowers bloom in April. Stop at Poulnabrone Dolmen — a 5,000-year-old portal tomb in the middle of nowhere.",
              details: [
                '🪨 Poulnabrone Dolmen: Neolithic burial tomb, free access',
                '🌸 April: first Burren wildflowers including spring gentian and mountain avens',
                '🦎 The Burren supports 22 of Ireland\'s 27 butterfly species',
                '📍 Kilfenora village has a free Burren Centre exhibition'
              ]
            },
            {
              title: 'Doolin Village',
              description: "A tiny fishing village that somehow became the epicenter of Irish traditional music. McGann's, O'Connor's, and McDermott's pubs have live trad sessions most afternoons and evenings. Very social — join a table and you'll be part of an impromptu session.",
              details: [
                '🎵 McGann\'s Pub: afternoon trad sessions from 3pm',
                '🚢 Doolin Ferry to the Aran Islands (30 min) — check schedules if keen',
                '🍺 O\'Connor\'s Pub: another legendary Doolin trad institution'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Doolin Café',
              description: "Simple, excellent seafood and home cooking in the heart of the music village. The chowder is legendary — thick, cream-based, loaded with Doolin seafood.",
              meta: '💰 $ · 📍 Doolin Village · Order the chowder, always'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Galway — Night Out',
              description: "Back in Galway by 7pm. Tonight, explore the West End bars of Dominick Street — grittier and more local than the tourist quarter. The Crane Bar has outstanding trad sessions, and Monroe's hosts set dancing on Tuesdays.",
              details: [
                '🎻 The Crane Bar, Sea Road: possibly the best trad session in Galway',
                '💃 Monroe\'s Tavern: set dancing Tuesday nights — join in, no experience needed',
                '🌙 Galway is a late-night city — things get going after 10pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Late Dinner',
              name: 'Dough Bros, Galway',
              description: 'Galway\'s most celebrated pizza — sourdough bases, Irish toppings, local ingredients. A Galway institution that somehow keeps getting better.',
              meta: '💰 $ · 📍 Middle Street · Turn up early, queues form fast'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 52.9720, lng: -9.4265, label: 'Cliffs of Moher', num: 1, cat: 'attraction', desc: '214m cliffs plunging into the Atlantic — Ireland\'s greatest spectacle' },
        { lat: 53.0317, lng: -9.1341, label: 'Poulnabrone Dolmen', num: 2, cat: 'attraction', desc: '5,000-year-old portal tomb in the Burren limestone' },
        { lat: 53.0135, lng: -9.4010, label: 'Doolin Village', num: 3, cat: 'attraction', desc: 'Tiny music village — Ireland\'s trad music heartbeat' },
        { lat: 53.0122, lng: -9.4018, label: 'Doolin Café', num: 4, cat: 'food', desc: 'Famous seafood chowder and home cooking' },
        { lat: 53.2745, lng: -9.0602, label: 'The Crane Bar, Galway', num: 5, cat: 'food', desc: 'Galway\'s finest trad music session pub' }
      ]
    },
    {
      num: 7,
      date: '2026-04-26',
      neighborhoods: 'Galway · Connemara · Clifden',
      title: 'Connemara — Wild Landscape & Slow West',
      description: "Your last full day in the west. Connemara is the Ireland of imagination — wild bogland, mirror lakes, looming mountains, and tiny white cottages scattered across an ancient landscape. A morning tour of this UNESCO-worthy region ends with a perfect Sunday session back in Galway.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Connemara Day Tour',
              description: "Connemara is only accessible by car or organized tour (no public bus). Take a half-day tour from Galway — Connemara on Tour or Lally Tours are excellent. You'll drive through Maam Cross, along the shore of Lough Corrib, and into Connemara National Park.",
              details: [
                '🚌 Lally Tours or Connemara on Tour: €30–40 half day from Galway',
                '🏔️ Twelve Bens mountains: dramatic quartzite peaks rising from the bog',
                '🦢 Kylemore Abbey: Victorian castle on a lake in a glacial valley (extra entry fee)',
                '🌿 Connemara National Park: free, excellent 5km Diamond Hill walk'
              ]
            },
            {
              title: 'Connemara National Park',
              description: "The Diamond Hill loop walk through Connemara National Park is one of Ireland's best short hikes. Bog flowers, ancient red deer, and a 360° panorama of the Atlantic coast from the summit.",
              details: [
                '🥾 Diamond Hill loop: 7km, 2.5 hours, moderate difficulty',
                '🦌 Red deer roam the park — most active at dawn and dusk',
                '🌸 April: bog cotton, yellow gorse, and the first purple heather',
                '💰 Free entry to the National Park'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Clifden Town & Slow Afternoon',
              description: "Clifden is the 'capital' of Connemara — a colourful market town with excellent pubs and restaurants. Browse the craft shops, have a long lunch, and absorb the end-of-the-world Atlantic atmosphere before heading back to Galway.",
              details: [
                '🍦 E.J. King\'s pub: Clifden\'s most authentic local pub, Sunday sessions',
                '🎨 Connemara Marble Factory Shop: the green marble is genuinely beautiful',
                '🌊 Clifden Bay: a short walk from the town square for Atlantic views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Lowry\'s Bar, Clifden',
              description: "Clifden's most beloved pub lunch spot — outstanding seafood chowder, brown bread, and a pint of Guinness. Locals, farmers, and visitors all sit together. The perfect Connemara afternoon.",
              meta: '💰 $ · 📍 Clifden town square · No reservations'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Night in Galway',
              description: "Back in Galway for your last night on the west coast. Tonight, do whatever felt unfinished — explore a different neighborhood, try a cooking class (Galway Food Tours runs evening experiences), or simply find a perfect pub and stay until closing.",
              details: [
                '🍳 Galway Food Tours: evening food experiences, great for meeting people',
                '🎶 Taaffes Bar, Shop Street: reliable trad from 5:30pm, always packed',
                '🌙 The Quays Bar: classic late-night Galway — massive atmosphere, live bands'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Kai Restaurant, Galway',
              description: "Galway's most celebrated restaurant — seasonal West of Ireland ingredients, open kitchen, and a genuinely warm atmosphere. Run by New Zealander Jess Murphy and her Irish husband David, Kai embodies everything that makes Galway special.",
              meta: '💰 $$$ · 📍 Sea Road · Book ahead — always full'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book Kai at least a week ahead — it\'s small and incredibly popular. The Sunday roast is legendary if you\'re there on a Sunday.' }
          ]
        }
      ],
      mapPins: [
        { lat: 53.5512, lng: -9.9370, label: 'Connemara National Park', num: 1, cat: 'attraction', desc: 'Diamond Hill walk — bog, mountains, Atlantic panoramas' },
        { lat: 53.4884, lng: -10.0209, label: 'Clifden', num: 2, cat: 'attraction', desc: 'Capital of Connemara — colourful market town on the Atlantic' },
        { lat: 53.5284, lng: -9.9012, label: 'Kylemore Abbey', num: 3, cat: 'attraction', desc: 'Victorian castle on a mountain lake — Ireland\'s most romantic building' },
        { lat: 53.4884, lng: -10.0209, label: 'Lowry\'s Bar, Clifden', num: 4, cat: 'food', desc: 'Best seafood chowder in Connemara, true locals\' pub' },
        { lat: 53.2733, lng: -9.0615, label: 'Kai Restaurant', num: 5, cat: 'food', desc: 'Galway\'s finest restaurant — seasonal west coast ingredients' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (B&B / guesthouse)', budget: '€70–100/night', midrange: '€100–160/night', luxury: '€160–300/night' },
    { category: 'Meals (per day)', budget: '€30–50/day', midrange: '€50–80/day', luxury: '€80–150/day' },
    { category: 'Transport (per day)', budget: '€10–25/day', midrange: '€25–50/day', luxury: '€50–100/day' },
    { category: 'Activities & tours', budget: '€15–30/day', midrange: '€30–60/day', luxury: '€60–120/day' },
    { category: '7-Day Total (solo)', budget: '€800–1,400', midrange: '€1,400–2,200', luxury: '€2,200–4,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Dublin Airport (DUB) has direct flights from North America, Europe, and UK', 'Ryanair, Aer Lingus, and others serve Dublin from €40–150 from major European cities', 'Shannon Airport (SNN) is closer to Galway and Cliffs of Moher — consider flying in/out there'] },
    { title: '🏨 Where to Stay', items: ['Dublin: B&Bs in Portobello, Ranelagh, or near St. Stephen\'s Green for local feel', 'Cork: City center guesthouses on MacCurtain Street area', 'Galway: Self-catering or B&B near Salthill or Dominick Street West End', 'Avoid: expensive chain hotels in tourist centers'] },
    { title: '🌡️ April Weather', items: ['Average 8–14°C (46–57°F) — cool but not cold', 'April gets ~14 days of rain — pack a proper waterproof jacket', 'Daylight: sunrise ~6:30am, sunset ~8:30pm — long, beautiful evenings', 'Layers are essential: mornings cold, afternoons can warm up pleasantly'] },
    { title: '🤝 Meeting People', items: ['Free walking tours: the #1 way to meet solo travelers', 'Sit at the bar, never at a table — Irish pub culture rewards this', 'Join guided day tours to Cliffs of Moher, Connemara — organized groups are social', 'Traditional music sessions: pull up a stool and join the audience naturally', 'Food markets and cooking experiences attract curious, friendly people'] },
    { title: '📱 Connectivity', items: ['Buy a Three Ireland or Vodafone Ireland SIM at the airport (€20–30, includes generous data)', 'Coverage is excellent in cities, reasonable on the Wild Atlantic Way', 'Most pubs, cafés, and B&Bs have free WiFi'] }
  ]
};

fulfillOrder(order, itineraryData);
