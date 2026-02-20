const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771618323992_mowmb9",
  email: "psyduckler@gmail.com",
  destination: "Reykjavík, Iceland",
  start_date: "2026-06-24",
  end_date: "2026-06-29",
  group_size: "2",
  travel_style: "Adventure, Relaxation",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  status: "pending"
};

const itineraryData = {
  destination: "Reykjavík, Iceland",
  countryEmoji: "🇮🇸",
  title: "Reykjavík & Iceland: 6 Days Under the Midnight Sun",
  subtitle: "Golden Circle · South Coast · Blue Lagoon · Whale Watching · Midnight Sun",
  description: "Iceland in late June is otherworldly — the sun barely dips below the horizon, waterfalls roar with snowmelt, and the dramatic volcanic landscapes feel untouched by time. This 6-day adventure for two balances epic day trips (Golden Circle, South Coast, Blue Lagoon) with genuine relaxation in one of the world's coolest small capitals. No rush, no filler — just Iceland at its absolute peak.",
  duration: "6 days",
  dates: "Jun 24 – 29, 2026",
  budget: "Mid-range ($3,000–5,000 for two)",
  pace: "Active days, relaxed evenings",
  bestFor: "Couples seeking adventure + relaxation",
  highlights: [
    "Golden Circle: Þingvellir, Geysir, and Gullfoss in one epic day",
    "South Coast waterfalls — walk BEHIND Seljalandsfoss",
    "Black sand beach at Reynisfjara and glacier views at Mýrdalsjökull",
    "Soaking in the Blue Lagoon's geothermal milky-blue waters",
    "Whale watching in Faxaflói Bay from Reykjavík Old Harbour",
    "Swimming under the midnight sun at Sundhöllin geothermal pool",
    "Hallgrímskirkja church and the colorful rooftops of Reykjavík",
    "Snorkeling or snorkeling the Silfra fissure (crystal-clear glacial water)"
  ],
  essentials: [
    {
      title: "🚗 Getting Around",
      text: "Rent a car — it's the only way to access Iceland's dramatic landscapes on your own schedule. Book in advance; small cars are ~$60-100/day in summer. Gas is expensive (~$2.50/liter). Flybus or Reykjavík Excursions runs airport transfers if you don't want to drive immediately. Many day trips (Golden Circle, South Coast) can be done via guided tours if preferred."
    },
    {
      title: "💰 Money",
      text: "Icelandic Króna (ISK). ~140 ISK = $1 USD. Iceland is expensive — budget $150-250/day per person. Cards are accepted everywhere (even at roadside hotdog stands). No need for much cash. The famous Bæjarins Beztu Pylsur hot dog is ~$3.50. A restaurant dinner: $50-90/person."
    },
    {
      title: "☀️ Midnight Sun",
      text: "Late June is peak midnight sun — the sun sets around midnight and rises before 3am. It barely gets dark. This is incredible for sightseeing but will mess with your sleep. Bring a sleep mask, invest in blackout curtains at your accommodation, and embrace it. Midnight walks feel magical."
    },
    {
      title: "🌡️ June Weather",
      text: "Expect 10–15°C (50–60°F) with strong winds. Pack waterproof layers you can add and remove. A windproof jacket is non-negotiable. Icelandic saying: 'If you don't like the weather, wait 10 minutes.' It will rain, then sun, then rain again. It's part of the experience."
    },
    {
      title: "🏨 Where to Stay",
      text: "Reykjavík is small and walkable — stay near Laugavegur (the main street) for easy access to restaurants, bars, and attractions. Guesthouses and boutique hotels in the 101 Reykjavík postal code are ideal. For the South Coast day, consider staying in Vík one night to catch Reynisfjara at sunrise."
    },
    {
      title: "📋 Book Ahead",
      text: "Blue Lagoon MUST be booked in advance (sells out weeks ahead). Pre-book whale watching tours. For Silfra snorkeling, book with DIVE.IS or Arctic Adventures. The Golden Circle and South Coast are self-drive — no booking needed beyond car rental. Book your car rental 4-6 weeks out."
    }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & Reykjavík First Impressions",
      neighborhoods: "Keflavík → Reykjavík · Laugavegur · Old Harbour",
      date: "Jun 24",
      mapPins: [
        { lat: 63.9850, lng: -22.6056, label: "Keflavík International Airport (KEF)", num: 1, cat: "transport", desc: "Arrive into Iceland's main airport — 45 min from Reykjavík" },
        { lat: 64.1418, lng: -21.9267, label: "Hallgrímskirkja Church", num: 2, cat: "activity", desc: "Iconic volcanic rock-inspired church with panoramic city views from the tower" },
        { lat: 64.1483, lng: -21.9362, label: "Laugavegur Main Street", num: 3, cat: "activity", desc: "Reykjavík's main drag — boutiques, restaurants, and the pulse of the city" },
        { lat: 64.1502, lng: -21.9347, label: "Old Harbour (Grandi)", num: 4, cat: "activity", desc: "Converted fishing harbour with seafood restaurants, street art, and whale watching piers" },
        { lat: 64.1355, lng: -21.8954, label: "Reykjavík City Centre", num: 5, cat: "activity", desc: "Colorful downtown with Tjörnin lake and the National Museum" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            {
              title: "Arrive at Keflavík → Drive to Reykjavík",
              description: "Pick up your rental car at the airport and enjoy the surreal 45-minute drive to Reykjavík through lava fields. The landscape immediately signals you're somewhere unlike anywhere else on Earth — volcanic rock covered in bright green moss, steaming vents, and wide-open sky.",
              details: [
                "💡 Flybus runs direct airport transfers if you prefer (~35 USD each way). But a rental car is worth it from Day 1.",
                "⚡ Fill up the tank at the airport — city petrol is pricier."
              ]
            },
            {
              title: "Hallgrímskirkja Church Tower",
              description: "Reykjavík's landmark church dominates the skyline with its striking basalt column-inspired architecture. Take the elevator up the 74-meter tower for sweeping views over the rainbow-painted rooftops and Faxaflói Bay. The statue of explorer Leif Erikson out front is a great photo.",
              details: [
                "💡 Tower entry: ~1,000 ISK ($7). Worth it for the view.",
                "📍 Top of the hill on Skólavörðustígur street"
              ]
            }
          ],
          meals: [
            {
              type: "🥗 Late Lunch",
              name: "Bæjarins Beztu Pylsur",
              description: "Iceland's most famous hot dog stand — a Reykjavík institution since 1937. Order 'ein með öllu' (one with everything): crispy onions, raw onions, ketchup, mustard, and remolaði. Bill Clinton ate here. You should too.",
              meta: "~$4 · Tryggvagata, Old Harbour area"
            }
          ],
          tips: [
            { type: "tip", text: "June 24 is close to the summer solstice — the sun won't properly set. Use this jet-lag gift to explore without time pressure. Reykjavík is vibrant and walkable at midnight." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Laugavegur & Skólavörðustígur Stroll",
              description: "Walk the length of Laugavegur — Iceland's main street bursts with color, independent boutiques, bookshops, and café culture. Browse Kronkron for Icelandic design, Reykjavík Record Shop for music, and stop into any of the galleries. The street art on every block is excellent.",
              details: []
            },
            {
              title: "Old Harbour (Grandi) Exploration",
              description: "Walk down to the old fishing harbour, now a cool creative district. The Maritime Museum and Whale of Iceland (huge whale models) are here, plus independent galleries and food trucks. Check out the huge street murals.",
              details: [
                "💡 Whale of Iceland: good quick intro to Icelandic whale species before tomorrow's whale watch"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Sea Baron (Sægreifinn)",
              description: "A legendary no-frills harbour shack famous for its lobster soup — arguably the best $12 you'll spend in Iceland. Also try the grilled minke whale skewer if you're adventurous. Cash-only vibe, communal tables, locals everywhere.",
              meta: "~$20-30/person · Geirsgata 8, Old Harbour"
            }
          ],
          tips: [
            { type: "tip", text: "After dinner it's still bright as noon. Walk along the harbour waterfront and watch the boats. The mountains across the bay are stunning." }
          ]
        },
        {
          label: "Night",
          activities: [
            {
              title: "Midnight Sun Walk & Drinks",
              description: "Reykjavík's weekend nightlife doesn't start until 11pm or midnight — locals eat late and stay out all night. For your first evening, grab drinks at a bar on Laugavegur and watch the sky go from golden to pink and back — it never properly gets dark. The Kex Hostel bar is great for a laidback crowd.",
              details: [
                "💡 Iceland's famous rúgbrauð (dark rye bread baked in hot springs) with smoked salmon or skyr is perfect bar food."
              ]
            }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Golden Circle Classic",
      neighborhoods: "Þingvellir · Geysir · Gullfoss · Reykjavík",
      date: "Jun 25",
      mapPins: [
        { lat: 64.2559, lng: -21.1296, label: "Þingvellir National Park", num: 1, cat: "activity", desc: "UNESCO site — where two tectonic plates meet and Iceland's parliament was founded in 930 AD" },
        { lat: 64.3108, lng: -20.3013, label: "Geysir Hot Spring Area", num: 2, cat: "activity", desc: "Strokkur geyser erupts every 4-10 minutes — standby for a soaking" },
        { lat: 64.3270, lng: -20.1209, label: "Gullfoss Waterfall", num: 3, cat: "activity", desc: "The 'Golden Falls' — Iceland's most iconic waterfall, roaring with glacial power" },
        { lat: 64.1926, lng: -20.4787, label: "Secret Lagoon (Gamla Laugin)", num: 4, cat: "activity", desc: "Iceland's oldest swimming pool — natural hot spring surrounded by geysers" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Drive to Þingvellir National Park (~45 min)",
              description: "Leave by 9am (it's already fully bright). Þingvellir sits in the rift valley between the North American and Eurasian tectonic plates — you can literally walk between continents. It's also where the Vikings established the world's first parliament (Alþing) in 930 AD. The Öxará River cuts through the rift; the views from the Almannagjá fault are extraordinary.",
              details: [
                "💡 The Silfra fissure here is the world's premier snorkeling/diving spot — crystal-clear glacial meltwater with 100m visibility. Pre-book a snorkel tour with DIVE.IS for this morning (~$100-120/person). It's life-changing.",
                "📍 Park entry: free. Parking: ~700 ISK ($5)"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Guesthouse breakfast or Reykjavík bakery",
              description: "Grab pastries and coffee before heading out. Brauð & Co on Frakkastígur makes Iceland's best croissants if you're an early riser.",
              meta: "~$10-15/person"
            }
          ],
          tips: [
            { type: "tip", text: "Þingvellir in June is lush green with wildflowers — bring good shoes for the rift walk. The Hakið viewpoint at the top is a must." }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Geysir Hot Spring Area (~1 hour drive from Þingvellir)",
              description: "Home to the original Geysir (which gave geysers their name) and the ever-reliable Strokkur, which erupts every 4-10 minutes to 20-30 meters. The whole area bubbles, steams, and smells of sulfur. Walk the full geothermal field — there are dozens of hot springs, mud pots, and fumaroles beyond the main geyser. Arrive at Strokkur early before tour buses.",
              details: [
                "💡 Free entry. The gift shop/restaurant is a tourist trap — save your hunger for Gullfoss or Secret Lagoon.",
                "⚠️ Don't step off marked paths — the ground is thin over boiling water."
              ]
            },
            {
              title: "Gullfoss Waterfall (~10 min from Geysir)",
              description: "The 'Golden Falls' — the Hvítá River plunges 32 meters into a dramatic gorge in two cascading steps. On sunny days, rainbows fill the mist. Walk down to the lower viewing platform to feel the spray. In June, snowmelt makes the falls roar at peak force.",
              details: [
                "💡 Free. Parking 500 ISK. Allow 45 min-1 hour to walk both viewing levels."
              ]
            }
          ],
          meals: [
            {
              type: "🥪 Lunch",
              name: "Café Gullfoss (at the falls) or packed lunch",
              description: "The on-site café is pricey but convenient — lamb soup and skyr are solid. Alternatively, pick up sandwiches from a Reykjavík deli before leaving.",
              meta: "~$20-30/person · Gullfoss visitor centre"
            }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Secret Lagoon (Gamla Laugin) — Relaxation Stop",
              description: "Iceland's oldest swimming pool, dating to 1891. Unlike the crowded Blue Lagoon, the Secret Lagoon is genuinely local and relaxed — a natural hot spring (38-40°C) surrounded by smaller geysers that erupt every few minutes. Soak in the warm water while watching the geothermal activity around you. This is the Golden Circle's hidden gem.",
              details: [
                "💡 Entry: ~3,000 ISK ($21). Towel rental available. Near Flúðir village.",
                "💡 Pre-book online at secretlagoon.is to guarantee entry."
              ]
            }
          ],
          meals: [],
          tips: [
            { type: "tip", text: "The Secret Lagoon is far less crowded than the Blue Lagoon and completely outdoors. Bring a book and stay as long as you want." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Return to Reykjavík (~1.5 hours)",
              description: "Drive back along Route 35 as the evening light turns golden (it barely gets dark — the sun just skims the horizon). Stop at any roadside waterfall or panoramic pull-off on the way back.",
              details: []
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Grillmarkaðurinn (The Grill Market)",
              description: "Reykjavík's top farm-to-table restaurant, focusing on Icelandic ingredients cooked over lava rock. The Arctic char, langoustine, and skyr dessert are outstanding. One splurge dinner — this is it.",
              meta: "~$80-120/person · Lækjargata 2A, city centre"
            }
          ],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "South Coast: Waterfalls, Black Sands & Glaciers",
      neighborhoods: "Seljalandsfoss · Skógafoss · Reynisfjara · Vík",
      date: "Jun 26",
      mapPins: [
        { lat: 63.6156, lng: -19.9886, label: "Seljalandsfoss Waterfall", num: 1, cat: "activity", desc: "Walk behind the falls! 60m cascade with a path around the back" },
        { lat: 63.5322, lng: -19.5127, label: "Skógafoss Waterfall", num: 2, cat: "activity", desc: "Powerful 60m falls with a staircase to the top — endless rainbows in sunshine" },
        { lat: 63.4037, lng: -19.0563, label: "Reynisfjara Black Sand Beach", num: 3, cat: "activity", desc: "Dramatic basalt columns, sea stacks (Reynisdrangar), and roaring Atlantic surf" },
        { lat: 63.4182, lng: -19.0048, label: "Vík í Mýrdal", num: 4, cat: "activity", desc: "Iceland's southernmost village — quaint church on a cliff, puffin colony nearby" },
        { lat: 63.5000, lng: -19.0000, label: "Mýrdalsjökull Glacier View", num: 5, cat: "activity", desc: "Sprawling glacier capping Katla volcano — visible from the South Coast" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Drive to Seljalandsfoss (~1.5 hours from Reykjavík)",
              description: "Leave by 8am to beat the crowds. The Ring Road (Route 1) takes you east along the coast — the views of Eyjafjallajökull glacier and the green valley opening up below it are staggering. Seljalandsfoss is the waterfall you can walk behind — a narrow path wraps behind the 60-meter curtain of water. You WILL get wet. Worth every drop.",
              details: [
                "⚠️ WEAR WATERPROOF GEAR to walk behind the falls. There's no avoiding the spray.",
                "💡 Gljúfrabúi (the 'hidden falls') is 500m north — squeeze through a slot canyon to find a magical secret waterfall. Don't skip it.",
                "📍 Parking: 900 ISK. Allow 1 hour."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Þorvaldseyri Visitor Center Café",
              description: "Small farm café at the base of Eyjafjallajökull — locally made skyr, pancakes, and views of the glacier that brought international aviation to a standstill in 2010.",
              meta: "~$12-18/person · Route 1, near Seljalandsfoss"
            }
          ],
          tips: [
            { type: "tip", text: "Puffins nest on the sea cliffs near Vík from May through August. Look for them on the Reynisfjall cliffs above Reynisfjara beach." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            {
              title: "Skógafoss Waterfall",
              description: "Skógafoss is a powerhouse — 60 meters tall, 25 meters wide, with a thundering roar you feel in your chest. On sunny mornings, a double rainbow fills the spray. Climb the 527 steps to the top for a panoramic view of the South Coast, the river's gorge, and glaciers in the distance. The hike along the Skógar river above (Fimmvörðuháls trail) is one of Iceland's best.",
              details: [
                "💡 Free entry. Climb the stairs! The view from the top is worth the burn.",
                "💡 In June, the trail above follows wildflower meadows and cascades — walk 20-30 min upstream for incredible solitude."
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Reynisfjara Black Sand Beach",
              description: "The most dramatic beach in Iceland. Black volcanic sand, basalt column formations straight from Game of Thrones (it was actually filmed here for the Wall), towering sea stacks (Reynisdrangar), and sneaker waves that command respect. Walk to the basalt caves and columns on the west end — hexagonal basalt pillars stacked like organ pipes.",
              details: [
                "⚠️ NEVER TURN YOUR BACK ON THE OCEAN. Sneaker waves here are unpredictable and deadly. Stay well back from the waterline.",
                "💡 Free. The cliffs above the beach are a nesting site for puffins in June."
              ]
            },
            {
              title: "Vík Village",
              description: "Iceland's most southerly village sits below a cliff topped with a white church. Stroll the small main street, visit the Icewear wool shop for quality lopapeysa sweaters, and grab coffee. The red cliffs of Reynisfjall above town are riddled with puffin burrows in June.",
              details: [
                "💡 Vík is a good base if you want to stay the night and catch Reynisfjara at sunrise."
              ]
            }
          ],
          meals: [
            {
              type: "🍲 Lunch",
              name: "Súður-Vík Restaurant",
              description: "Small, unpretentious spot in Vík serving hearty Icelandic lamb soup, fish and chips, and fresh-baked bread. One of the better food options on the South Coast.",
              meta: "~$25-35/person · Vík village"
            }
          ],
          tips: [
            { type: "tip", text: "Take a slow drive back on Route 1 along the coast. Every km has a new waterfall, glacier tongue, or volcanic formation. Endless pull-off moments." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Return Drive to Reykjavík (or stay in Vík)",
              description: "The 2.5-hour return drive to Reykjavík in evening light is gorgeous. Alternatively, spend the night in Vík to catch Reynisfjara in early morning solitude before the tour buses arrive (6-7am it's magical and empty). Many small guesthouses in Vík are excellent.",
              details: []
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Fiskeldar Vatnsholts (if nearby) or dinner in Reykjavík",
              description: "If returning to Reykjavík, try Messinn for the best fish pan (skillet of fresh local catch) in the city. Casual, delicious, and quintessentially Icelandic.",
              meta: "~$40-60/person · Lækjargata 6, Reykjavík"
            }
          ],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Blue Lagoon & Reykjanes Peninsula",
      neighborhoods: "Reykjanes Peninsula · Grindavík · Blue Lagoon",
      date: "Jun 27",
      mapPins: [
        { lat: 63.8800, lng: -22.4452, label: "Blue Lagoon Geothermal Spa", num: 1, cat: "activity", desc: "Iceland's most famous attraction — milky-blue 38-40°C geothermal waters in a lava field" },
        { lat: 63.8342, lng: -22.6826, label: "Gunnuhver Hot Springs", num: 2, cat: "activity", desc: "Iceland's largest hot spring — boiling mud pools and steam vents on the Reykjanes tip" },
        { lat: 63.8173, lng: -22.6867, label: "Reykjanes Lighthouse & UNESCO Geopark", num: 3, cat: "activity", desc: "Rugged lava coastline at Iceland's southwesternmost point" },
        { lat: 63.8427, lng: -22.5522, label: "Bridge Between Continents", num: 4, cat: "activity", desc: "Walk across a footbridge spanning the rift between North American and Eurasian plates" },
        { lat: 63.9850, lng: -22.6056, label: "Keflavík Airport Area", num: 5, cat: "transport", desc: "Nearby area — Reykjanes loop starts and ends near here" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Blue Lagoon (Pre-booked AM Slot)",
              description: "Book the earliest available slot (7am or 8am) to soak in relative peace before the day crowds arrive. The Blue Lagoon's otherworldly milky-blue waters sit in a jagged lava field — it's genuinely as beautiful as the photos. The water is rich in silica and sulphur minerals. Apply the complimentary white silica mud mask. Order a Geothermal Ale or sparkling water from the in-water bar. Pure bliss.",
              details: [
                "⚠️ MUST book in advance at bluelagoon.com. Premium entry with silica mud mask and towel: ~€100/person. Sells out weeks ahead in June.",
                "⚠️ Silica will destroy hair — tie it up or use the conditioner provided immediately. Rinse hair thoroughly before entering.",
                "💡 Leave rings and jewelry in your locker — silica can coat metals."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Blue Lagoon Lava Restaurant or Moss Restaurant",
              description: "The on-site restaurants are expensive but the setting is unreal. Moss Restaurant (inside the complex) serves an excellent Icelandic breakfast with views of the steaming lava field. Or eat at your hotel before driving out.",
              meta: "~$30-50/person · Blue Lagoon complex"
            }
          ],
          tips: [
            { type: "tip", text: "Spend at least 2-3 hours soaking. There's no rush — explore all the pools, saunas, steam caves, and the indoor/outdoor areas. The Retreat Lagoon (adjacent, premium) is quieter if you want to upgrade." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Reykjanes Peninsula Loop Drive",
              description: "The Reykjanes Peninsula is a UNESCO Global Geopark — raw, volcanic, and mostly visited only by people who know. Drive the coastal loop: Gunnuhver's boiling mud pools and steam vents are Iceland's most active geothermal surface features (the steam is incredibly dramatic). The Reykjanes Lighthouse sits at the peninsula's tip amid a moonscape of lava. The Bridge Between Continents lets you literally straddle the rift between tectonic plates for a photo.",
              details: [
                "💡 Free to explore. Allow 2-3 hours for the full loop.",
                "⚠️ This area has been seismically active in recent years — check current conditions at vedur.is."
              ]
            }
          ],
          meals: [
            {
              type: "🥪 Lunch",
              name: "Suðurvíkurbrún Fish & Chips or Grindavík bakery",
              description: "Grindavík is a working fishing town — grab fresh fish and chips or soup from a local spot. No fancy restaurants, just real Icelandic food.",
              meta: "~$15-25/person · Grindavík town"
            }
          ],
          tips: [
            { type: "tip", text: "The 2024 volcanic eruptions on the Reykjanes Peninsula created new lava fields you can now walk on (cooled). Ask locals or check updates for current access." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Return to Reykjavík — Spa or Hot Tub Evening",
              description: "After the Blue Lagoon and peninsula drive, tonight is for recovery. Reykjavík's public swimming pools (sundlaugar) are a local institution — every neighborhood has one with hot tubs, steam rooms, and water slides. Laugardalslaug is the biggest and best. For ~$8, you can soak in naturally heated 40°C hot pots alongside Reykjavík locals for hours.",
              details: [
                "💡 Laugardalslaug open until 10pm daily. Entry: ~1,000 ISK. Bring or rent a towel.",
                "💡 This is WHERE REYKJAVÍK ACTUALLY SOCIALIZES. Conversations happen between strangers in the hot pots. Immerse yourself."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Matur og Drykkur",
              description: "Arguably Reykjavík's most creative Icelandic restaurant — classic Icelandic recipes reimagined with modern technique. The cod's head (þorskhaus) and lamb neck are incredible. Menu changes with seasons and availability. Unique, memorable, and proudly Icelandic.",
              meta: "~$70-100/person · Grandagarður 2, Old Harbour"
            }
          ],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Whale Watching & Reykjavík Deep Dive",
      neighborhoods: "Old Harbour · 101 Reykjavík · Grandi · Perlan",
      date: "Jun 28",
      mapPins: [
        { lat: 64.1502, lng: -21.9347, label: "Reykjavík Old Harbour (Whale Watching)", num: 1, cat: "activity", desc: "Departures for Faxaflói Bay whale watching — minke, humpback, and white-beaked dolphins" },
        { lat: 64.1284, lng: -21.8979, label: "Perlan Museum", num: 2, cat: "activity", desc: "Futuristic dome on a hill — Northern Lights planetarium, glacier tunnel, and 360° views" },
        { lat: 64.1364, lng: -21.9319, label: "Sundhöllin Geothermal Pool", num: 3, cat: "activity", desc: "Beautiful Art Deco outdoor pool in the city centre — swim under the midnight sun" },
        { lat: 64.1471, lng: -21.9421, label: "101 Reykjavík Boutiques", num: 4, cat: "activity", desc: "Independent design shops, galleries, and the best coffee in Iceland" },
        { lat: 64.1451, lng: -21.9317, label: "Tjörnin Lake", num: 5, cat: "activity", desc: "Peaceful city lake with Arctic terns nesting in summer" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Whale Watching Tour from Old Harbour (9am departure)",
              description: "Faxaflói Bay is one of the best spots in Europe for whale watching. Minke whales and humpbacks are common in June; white-beaked dolphins often ride the bow wave. The 3-hour tour departs from the Old Harbour and heads out into the bay — even if you don't see whales, the views of Reykjavík and the Snæfellsnes glacier from the water are phenomenal.",
              details: [
                "💡 Book with Elding Whale Watching (~$65/person) or Special Tours — both have high success rates in June. Book online in advance.",
                "💡 Dress for cold ocean wind regardless of sunshine. The boat provides overalls to borrow but bring extra layers.",
                "💡 June is peak puffin season — you'll see puffins flying over the bay, often in huge flocks."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Brauð & Co or Reykjavík Roasters",
              description: "Brauð & Co makes Iceland's best pastries (kouign-amann, cardamom buns, sourdough). Reykjavík Roasters is the top specialty coffee shop. Both near Hallgrímskirkja. Grab and go before the 9am departure.",
              meta: "~$10-15/person"
            }
          ],
          tips: [
            { type: "tip", text: "Humpback whale breaches are heart-stopping. If you see tail flukes in the distance, ask the crew to position the boat — they're experienced at maximizing sightings without disturbing the whales." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Perlan Museum & 360° Observation Deck",
              description: "Built on top of Reykjavík's hot water storage tanks on Öskjuhlíð hill, Perlan has a spectacular observation deck with 360° views of the city, bay, and surrounding mountains. Inside, the Northern Lights show (planetarium) is well-produced, and the walk-through glacier tunnel (made of real ice) is a surprisingly immersive experience.",
              details: [
                "💡 Entry: ~$30/person. Northern Lights show: +$7. Worth it on a full-day city focus.",
                "💡 Short hike through the birch forest surrounding Perlan — great for seeing the local bird life."
              ]
            },
            {
              title: "Reykjavík Art Walk & Grandi District",
              description: "The Grandi neighbourhood (old harbour turned creative district) has Iceland's best contemporary art. Visit the Whales of Iceland installation, the Harbor House Museum (Hafnarhús) for modern Icelandic art, and browse the independent design shops. The street art throughout the district is world-class.",
              details: []
            }
          ],
          meals: [
            {
              type: "🥗 Lunch",
              name: "Snaps Bistro",
              description: "Franco-Danish bistro on Þórsgata — excellent moules frites, smoked salmon niçoise, and daily fish specials. One of Reykjavík's most consistent locals' favorites.",
              meta: "~$35-50/person · Þórsgata 1"
            }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Sundhöllin — Swim Under the Midnight Sun",
              description: "This 1937 Art Deco outdoor pool in the heart of the city is Reykjavík's most beautiful. The outdoor pool and geothermal hot tubs are open until 10pm. Swimming in 29°C water while the sun hangs at a golden 45° angle at 9pm is one of the most quintessentially Icelandic experiences you can have.",
              details: [
                "💡 Entry: ~1,000 ISK. Bring a swimsuit. Towel rental available.",
                "💡 The outdoor hot tubs have regulars — great conversations happen here."
              ]
            },
            {
              title: "Laugavegur's Nightlife (last big night!)",
              description: "Reykjavík's bar scene is legendary — tiny, eclectic, and impossibly vibrant for a city of 130,000. Kiki Queer Bar, Lebowski Bar, and Kaffibarinn (owned by Blur's Damon Albarn) are classics. The ruin bars have outdoor areas buzzing at midnight with the sky still bright. Icelanders drink late and hard. Join in.",
              details: [
                "💡 Beer is expensive (~$10-12 at bars). Pre-game with duty-free from the airport if you want to save money."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Kopar Restaurant",
              description: "Intimate harbour-front restaurant with an excellent raw bar and creative Icelandic seafood. Arctic char ceviche, langoustine carpaccio, and a superb wine list. Perfect last-night splurge.",
              meta: "~$70-100/person · Geirsgata 3, Old Harbour"
            }
          ],
          tips: [
            { type: "tip", text: "Last night in Reykjavík — if you want to stay out until 3am with full daylight, this is the night to do it. The surreal brightness at 2am hits different when you know it's your last." }
          ]
        }
      ]
    },
    {
      num: 6,
      title: "Departure Morning & Final Bites",
      neighborhoods: "Reykjavík · Laugavegur · Keflavík Airport",
      date: "Jun 29",
      mapPins: [
        { lat: 64.1396, lng: -21.9221, label: "Laugavegur (Final Morning Walk)", num: 1, cat: "activity", desc: "Last stroll down Reykjavík's colorful main street" },
        { lat: 64.1418, lng: -21.9267, label: "Hallgrímskirkja", num: 2, cat: "activity", desc: "One last look at Iceland's iconic landmark" },
        { lat: 64.1451, lng: -21.9317, label: "Tjörnin Lake Morning Walk", num: 3, cat: "activity", desc: "Peaceful morning walk around the city lake with ducks and Arctic terns" },
        { lat: 63.9850, lng: -22.6056, label: "Keflavík International Airport (KEF)", num: 4, cat: "transport", desc: "Depart Iceland — allow 2 hours. Duty-free here is excellent." }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Slow Morning in Reykjavík",
              description: "Last morning — let it unfold slowly. Walk around Tjörnin lake (Arctic terns dive-bomb anyone near their nests in June — hilariously chaotic). Do a final lap of Laugavegur. Look up at the colorful rooftops and the backdrop of the Esja mountain across the bay. Pack the lopapeysa sweater you definitely bought.",
              details: []
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Sandholt Bakery",
              description: "Reykjavík's most beloved bakery — exceptional sourdough, rye bread with smoked salmon and cream cheese, cardamom rolls, and real hot chocolate. The perfect last meal in Iceland.",
              meta: "~$15-20/person · Laugavegur 36"
            }
          ],
          tips: [
            { type: "tip", text: "The Keflavík Airport duty-free is outstanding — local lava salt, skyr, lopapeysa wool goods, and quality Icelandic spirits (Brennivín!) at airport prices. Buy here, not in the city." }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Drive to Keflavík Airport (~45-50 min)",
              description: "Return your rental car at the airport. Allow at least 2 hours before departure — Keflavík can get backed up in summer peak season. On the way, one last look at the lava field moonscape you drove through on arrival. Iceland never gets old.",
              details: [
                "💡 Return the rental car full — petrol stations are right outside the airport.",
                "⚡ Security lines at Keflavík move fast but arrive early on busy summer mornings."
              ]
            }
          ],
          meals: [
            {
              type: "✈️ Airport Meal",
              name: "Prikið at Keflavík Airport",
              description: "If you need one last Icelandic fix, the airport has decent options. The Bæjarins Beztu Pylsur hot dog stand doesn't have an airport outpost, so grab duty-free skyr instead.",
              meta: "Keflavík Airport departures"
            }
          ],
          tips: [
            { type: "tip", text: "Iceland will wreck you in the best way. The landscapes, the light, the people, the geothermal everything. You'll be back. 🇮🇸" }
          ]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "Car Rental (5 days, small 4WD)", low: "$300", high: "$500" },
    { category: "Accommodation (5 nights, mid-range, 2 people)", low: "$800", high: "$1,200" },
    { category: "Blue Lagoon (2 people, premium)", low: "$200", high: "$220" },
    { category: "Golden Circle + Secret Lagoon (2 people)", low: "$60", high: "$90" },
    { category: "Whale Watching (2 people)", low: "$120", high: "$140" },
    { category: "Silfra Snorkeling (2 people, optional)", low: "$200", high: "$240" },
    { category: "Dining (5 days, mix of casual + 2 splurge dinners)", low: "$500", high: "$800" },
    { category: "Petrol (Golden Circle + South Coast + Reykjanes)", low: "$80", high: "$120" },
    { category: "Activities, pools, museums, parking", low: "$100", high: "$180" },
    { category: "Shopping, souvenirs, incidentals", low: "$100", high: "$300" }
  ],
  practicalInfo: [
    {
      title: "🚗 Driving in Iceland",
      items: [
        "Drive on the right. Speed limits: 90 km/h on Ring Road, 80 km/h on gravel, 50 km/h urban.",
        "F-roads (Highland interior) require a proper 4WD and are NOT covered by standard rental insurance — avoid unless you've upgraded.",
        "Sheep wander onto roads constantly — they always have right of way. Slow down on rural roads.",
        "Check road conditions at road.is (F-road closures, highland access dates).",
        "Fill up whenever you see a petrol station — pumps can be far apart in rural areas."
      ]
    },
    {
      title: "🌊 Safety",
      items: [
        "Sneaker waves at coastal beaches (especially Reynisfjara) are extremely dangerous — NEVER turn your back on the ocean.",
        "Geothermal areas: stay on marked paths. The crust is thin above boiling water.",
        "Wind on cliff edges and in mountain areas can be intense — check weather forecasts at vedur.is.",
        "For hiking or remote day trips, log your plan at safetravel.is.",
        "Emergency number: 112 (Iceland Search and Rescue). The 112 Iceland app is worth installing."
      ]
    },
    {
      title: "💊 Health & Practical",
      items: [
        "Pharmacies (apótek) in Reykjavík city centre — Lyfja is the main chain.",
        "Iceland has excellent public hospitals. Travel insurance with medical coverage recommended.",
        "Type F plugs (same as continental Europe), 220V. US visitors need an adapter and converter.",
        "Tap water in Iceland is among the purest in the world — no need to buy bottled water.",
        "Mobile coverage is good throughout the south and the Golden Circle; spotty in remote highlands."
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Reykjavík fulfillment complete:', JSON.stringify(result, null, 2));
