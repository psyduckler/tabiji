const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773073630484_lczlvy',
  email: 'kialogy@gmail.com',
  destination: 'Kualapuu, HI, USA',
  startDate: '2026-05-11',
  endDate: '2026-05-17',
  groupSize: 2,
  requests: 'Mix of surf, relaxation, beach, adventure, and all the while accommodating a baby.'
};

const itineraryData = {
  destination: 'Molokai, Hawaii',
  countryEmoji: '🌺',
  title: 'Wild & Unhurried: Molokai with Your Little One',
  subtitle: '7 days of surf, beach, aloha spirit, and baby-friendly adventure on Hawaii\'s most authentic island',
  description: "Molokai is Hawaii as it used to be — no traffic lights, no resort strips, just raw coastline, ancient fishponds, and a community that still lives by the land and sea. This itinerary balances your surf sessions and beach adventures with a pace that works for a baby: long mornings on protected sandy beaches, shaded afternoon naps, evenings at the handful of real local restaurants. Kualapuu is your quiet home base in the island's green heart, with the west-end beaches and the east-end surf just a short drive away.",
  duration: '6 nights',
  dates: 'May 11 – May 17, 2026',
  budget: '$$$',
  pace: 'Relaxed',
  bestFor: 'Couple + Baby',
  highlights: [
    'Murphy\'s Beach — reef-protected, calm water perfect for baby\'s first ocean dip',
    'Papohaku Beach — 3-mile white sand stretch with zero crowds',
    'Watching experienced surfers at Rock Point and The Wharf',
    'Halawa Valley hike to a dramatic twin waterfall',
    'Paddlers Restaurant & Bar and Hiro\'s Ohana Grill — Molokai\'s finest tables',
    'Purdy\'s Macadamia Nut Farm — a genuine off-the-grid Hawaii experience'
  ],

  essentials: [
    {
      title: '🍼 Traveling with a Baby on Molokai',
      text: 'Molokai rewards a slow pace — which is perfect with a baby. Most beaches are uncrowded and the island has virtually no tourist infrastructure, which actually means less noise and stimulation. Bring all baby supplies from Oahu or the mainland: Molokai\'s Friendly Market in Kaunakakai carries basics but selection is very limited. A portable shade tent for the beach is essential.'
    },
    {
      title: '🏄 Surf Reality Check',
      text: 'Molokai has real surf at Rock Point, The Wharf, and Halawa — but these are reef breaks for experienced surfers, not beginner spots. With a baby in tow, the smartest play is to watch from shore and enjoy the show. The only truly gentle surf is at Papohaku Beach during south swells (May can have them) and The Wharf on smaller days. Paddleboards are available for rent.'
    },
    {
      title: '🛒 Stock Up in Kaunakakai',
      text: 'Friendly Market (Kaunakakai) is the main grocery store — do a big shop on arrival day. West-end vacation rentals and Hotel Molokai are far from any convenience store. Bring snacks, sunscreen (SPF 50+), reef-safe only, and any specialty baby food you need. There are no major pharmacies outside Kaunakakai.'
    },
    {
      title: '🚗 Getting Around',
      text: 'A rental car is absolutely essential on Molokai — there is no public transit, no Uber, no Lyft. Book your car in advance (Island Air Car Rental or Dollar at the airport). Molokai Adventist Health Center is the only clinic. The one main road — Kamehameha V Highway — connects everything. Kaunakakai to Papohaku Beach: 17 miles west. Kaunakakai to Halawa Bay: 27 miles east.'
    },
    {
      title: '🌊 Ocean Safety',
      text: 'Murphy\'s Beach (Sandy Beach) is the safest swimming beach — protected by a barrier reef with calm, shallow water ideal for babies. Papohaku Beach is beautiful but can have strong shorebreak and rip currents — wade in shallow water only with a baby. Never enter the ocean at Halawa Bay surf breaks with a baby or young child.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-11',
      neighborhoods: 'Molokai Airport · Kaunakakai · Kualapuu',
      title: 'Arrival Day — Land, Stock Up, Settle In',
      description: 'Touch down on this tiny island, do your grocery run in Kaunakakai, and make your way to your west-end home base. Your first evening calls for a sunset walk and a laid-back local dinner — no rushing, no agenda.',
      timeBlocks: [
        {
          label: 'Morning / Midday',
          activities: [
            {
              title: 'Fly into Molokai & Pick Up Your Rental Car',
              description: 'Molokai Airport (MKK) is tiny — 10 gates, no jetways. Pick up your car immediately on arrival; you\'ll need it for everything. Flights connect from Honolulu or Maui on Mokulele Airlines (turboprops — fun for adults, manageable for babies with ear protection).',
              details: [
                '✈️ Mokulele Airlines: HNL–MKK flights, ~25 minutes',
                '🚗 Car rental: Dollar or Island Air Car Rental at the airport — book ahead',
                '🍼 Baby tip: pack ears muffs or noise-canceling headphones for the propeller flight'
              ]
            },
            {
              title: 'Big Shop at Friendly Market, Kaunakakai',
              description: 'This is your one real grocery store on the island. Do a thorough shop: water, snacks, breakfast foods, baby supplies, sunscreen (reef-safe), and anything you might need all week. Supplies at the west-end vacation rentals are very limited.',
              details: [
                '🛒 Friendly Market: open Mon–Fri 7am–8:30pm, Sat 7am–8:30pm, Sun 9am–6pm',
                '📍 Located in downtown Kaunakakai',
                '🧴 Reef-safe sunscreen is required — Hawaiian state law. SPF 50+ minimum in May',
                '🍼 Stock up on baby food, formula, diapers, or any medications you need'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check Into Your West-End Vacation Rental',
              description: 'Most west-end rentals are near Papohaku Beach — some of the most affordable oceanfront accommodations in all of Hawaii. Set up your base, let the baby get familiar with the space, and decompress from the travel day.',
              details: [
                '🏡 Papohaku Beach area vacation rentals: search via Airbnb or VRBO for best selection',
                '🌴 Hotel Molokai (east of Kaunakakai) is the only true hotel — great oceanfront setting but farther from the best beaches',
                '🚿 West-end rentals often have outdoor showers — perfect for rinsing sand off baby gear'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If your rental has an outdoor lanai or deck, spend the first afternoon just breathing in the silence. Molokai has almost zero light or noise pollution — the quiet is startling after any city.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Walk at Papohaku Beach',
              description: 'Drive the five minutes down to Papohaku Beach for your first sunset on Molokai. This 3-mile white sand beach is almost always empty — in May it\'s just you, the waves, and Oahu glowing on the horizon 30 miles away.',
              details: [
                '🌅 Sunset faces west toward Oahu — spectacular on a clear day',
                '🏖️ Papohaku is large but has strong shorebreak — keep the baby in the shallow sandbar area',
                '📸 Bring a camera — the light here is special'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Paddlers Restaurant & Bar',
              description: 'The best sit-down restaurant on Molokai — solid burgers, fresh fish plates, and cold beer. Local crowd, casual vibe, very family-friendly. The short ribs and ahi burgers are crowd favorites.',
              meta: '💰 $$ · 📍 10 Ala Malama Ave, Kaunakakai · Open for dinner most evenings'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1529, lng: -157.0960, label: 'Molokai Airport (MKK)', num: 1, cat: 'attraction', desc: 'Small propeller-plane airport — car rental on-site' },
        { lat: 21.0902, lng: -157.0222, label: 'Friendly Market', num: 2, cat: 'food', desc: 'Main grocery store — stock up for the week here' },
        { lat: 21.1165, lng: -157.2518, label: 'Papohaku Beach', num: 3, cat: 'attraction', desc: '3-mile white sand beach, west end — best sunsets on Molokai' },
        { lat: 21.0902, lng: -157.0222, label: 'Paddlers Restaurant & Bar', num: 4, cat: 'food', desc: 'Best restaurant on Molokai — local crowd, great burgers and fish' },
        { lat: 21.1541, lng: -157.0430, label: 'Kualapuu', num: 5, cat: 'attraction', desc: 'Quiet green-heart town — your home base on the island' }
      ]
    },
    {
      num: 2,
      date: '2026-05-12',
      neighborhoods: 'Murphy\'s Beach · East End · Kaunakakai',
      title: 'Baby\'s First Ocean Day — Murphy\'s Beach & East End Drive',
      description: 'The east end of Molokai is stunning — ancient fishponds line the highway, the mountain drops into the sea, and Murphy\'s Beach offers the calmest, most protected water on the island. This is baby\'s perfect first Hawaiian ocean day.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Murphy\'s Beach (Sandy Beach) — Baby\'s First Ocean',
              description: 'Murphy\'s Beach is protected by a natural barrier reef, creating calm, clear, shallow water that\'s among the safest anywhere in Hawaii. The sandy-bottomed lagoon is ideal for wading with a baby. The reef is also excellent for snorkeling for adults while baby splashes.',
              details: [
                '🪸 Barrier reef creates calm lagoon — perfect for babies and toddlers',
                '🤿 Adult snorkeling: put on a mask and look at the reef right from shore',
                '🌊 Water depth: knee-deep to waist-deep over the inner reef flat',
                '🌴 Shade: bring your own shade tent — there are a few trees but limited shelter',
                '📍 Look for the small parking area on the makai (ocean) side of Kamehameha V Hwy, near mile marker 20'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Murphy\'s Beach is the #1 baby-friendly beach on Molokai. The reef breaks the swell before it reaches the beach, and the water is clear and calm even when it\'s rough elsewhere. Plan at least 2-3 hours here.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'East End Scenic Drive — Fishponds & Ancient Hawaii',
              description: 'Drive the scenic east-end highway past ancient Hawaiian fishponds (some still in use), lush valleys, and dramatic sea cliffs. Stop at Halawa Overlook for a jaw-dropping view of the green valley and the ocean. The narrow winding road is the drive itself — take your time.',
              details: [
                '🐟 Keawanui Fishpond: one of Molokai\'s most intact ancient fishponds, visible from the road',
                '🏔️ Halawa Overlook: stunning view down into the lush valley — great photo spot',
                '🌿 The road narrows to a single lane in places — drive slowly',
                '📍 The drive from Kaunakakai to road\'s end near Halawa Bay is about 30 miles'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hiro\'s Ohana Grill at Hotel Molokai',
              description: 'Oceanfront restaurant at Hotel Molokai, serving locally sourced fish, pesto chicken, and Hawaiian classics. Eat outside on the lanai as the sun sets over the fish ponds and coconut palms.',
              meta: '💰 $$ · 📍 Kamehameha V Hwy, Kaunakakai · Open for dinner nightly'
            }
          ],
          tips: [
            { type: 'tip', text: 'Hotel Molokai\'s oceanfront lanai is one of the most atmospheric dining spots on the island. The fairy lights, palm trees, and ocean sounds make it feel genuinely magical — especially after the baby is fed and happy.' }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0672, lng: -156.8667, label: 'Murphy\'s Beach (Sandy Beach)', num: 1, cat: 'attraction', desc: 'Reef-protected lagoon — safest swimming on Molokai, perfect for babies' },
        { lat: 21.1000, lng: -156.9300, label: 'Keawanui Fishpond', num: 2, cat: 'attraction', desc: 'Ancient Hawaiian fishpond, one of many along the east end highway' },
        { lat: 21.1540, lng: -156.7620, label: 'Halawa Overlook', num: 3, cat: 'attraction', desc: 'Panoramic view of Halawa Valley and the dramatic eastern coastline' },
        { lat: 21.0902, lng: -157.0222, label: 'Hotel Molokai / Hiro\'s Ohana Grill', num: 4, cat: 'food', desc: 'Oceanfront dining — locally sourced fish and Hawaiian classics' },
        { lat: 21.0902, lng: -157.0222, label: 'Kaunakakai Town', num: 5, cat: 'attraction', desc: 'Molokai\'s main town — a genuine old Hawaii small-town feel' }
      ]
    },
    {
      num: 3,
      date: '2026-05-13',
      neighborhoods: 'Rock Point · The Wharf · Kaunakakai',
      title: 'Surf Day — Watch the Breaks, Wade in the Shallows',
      description: 'Today you scout Molokai\'s surf spots — Rock Point and The Wharf are the island\'s most accessible breaks. No paddling out with a baby, but watching from shore is its own pleasure. End the day with a paddle in calm waters and one of Molokai\'s best sunsets.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rock Point Surf Watch',
              description: 'Rock Point is Molokai\'s most consistent surf break — a left and right over shallow reef near the west end. In May, south swells can fire it up. It\'s accessible from shore for watching; experienced local surfers and occasional visitors make it out here. Great photography spot from the bluff.',
              details: [
                '🏄 Consistent left and right breaking over reef — best for experienced surfers',
                '📸 Bluff viewpoint gives a great elevated angle on the break',
                '🌊 May swells: south swell season begins, can produce quality waves here',
                '🍼 Baby tip: a carrier or stroller works on the sandy access path; keep back from the edge'
              ]
            },
            {
              title: 'The Wharf — Watch the Local Crew Surf',
              description: 'The Wharf (near Kaunakakai Harbor) has a fast left and a slower right that local kids and adults surf regularly. It\'s the most social surf spot on the island — you\'ll see families watching from the breakwater while others paddle out. Perfect baby-safe viewing spot.',
              details: [
                '🏄 Fast left / slow right — locals\' home break',
                '👨‍👩‍👧 Families watch from the breakwater — very social and relaxed',
                '🌴 Flat days: the harbor is calm enough for paddleboarding with baby on board'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If it\'s a small-wave day and you want to surf yourself, The Wharf is the most forgiving break. But be honest with yourself — Molokai\'s reef breaks punish mistakes, and with a baby watching from shore, now might be the week to mostly enjoy the view.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Paddleboarding or Kayaking on Kaunakakai Harbor',
              description: 'Rent a stand-up paddleboard or kayak and explore the calm harbor waters. Some rental operators offer tandem boards where a baby can safely sit between your feet on the deck. The harbor has zero surf and the water is warm and clear.',
              details: [
                '🏄 SUP Rental: Molokai Outdoors or ask at your accommodation',
                '🚣 Tandem paddleboarding with a baby: very doable in flat harbor water with a PDF vest for baby',
                '🌊 Kayak along the shoreline past ancient fishponds — unique perspective',
                '☀️ May water temp: ~77°F — warm and inviting'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Papohaku Beach Sunset',
              description: 'Drive back to Papohaku for the evening. In May, south swells sometimes produce rideable waves at Dixies (near the south end of Papohaku). Watch from shore, walk the long empty beach, and let the baby experience the sand at golden hour.',
              details: [
                '🌅 Papohaku sunsets: consistently spectacular in May',
                '🏄 Dixies break (south end of beach): south swell surf spot — watch from shore',
                '🌙 After sunset: little light pollution, stars appear quickly — incredible for baby\'s first star-gazing'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Molokai Pizza Cafe',
              description: 'Casual pizza joint in Kaunakakai — a local favorite for families. Very baby-friendly, no pretensions, good food.',
              meta: '💰 $ · 📍 Kaunakakai · Open evenings, closed some days — check hours locally'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1310, lng: -157.2180, label: 'Rock Point', num: 1, cat: 'attraction', desc: 'Molokai\'s most consistent surf break — left and right over reef' },
        { lat: 21.0913, lng: -157.0278, label: 'The Wharf / Kaunakakai Harbor', num: 2, cat: 'attraction', desc: 'Local surf spot and harbor — great for watching surfers and flat-water paddling' },
        { lat: 21.1165, lng: -157.2518, label: 'Papohaku Beach (Dixies end)', num: 3, cat: 'attraction', desc: 'South-end of Papohaku — Dixies surf break fires on south swells' },
        { lat: 21.0902, lng: -157.0222, label: 'Molokai Pizza Cafe', num: 4, cat: 'food', desc: 'Casual, family-friendly pizza joint in Kaunakakai' },
        { lat: 21.0913, lng: -157.0278, label: 'Molokai Outdoors', num: 5, cat: 'attraction', desc: 'SUP and kayak rentals for exploring the harbor and coastline' }
      ]
    },
    {
      num: 4,
      date: '2026-05-14',
      neighborhoods: 'Halawa Valley · East End',
      title: 'Halawa Valley — Waterfall Hike & Lush Hawaii',
      description: 'The Halawa Valley hike to twin Mo\'oula and Hipuapua waterfalls is one of the most beautiful short treks in Hawaii. You\'ll need a local guide (required), and it\'s doable with a baby in a carrier. The valley is sacred, lush, and unforgettable.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Halawa Valley Waterfall Hike',
              description: 'The hike to Mo\'oula Falls (about 4 miles round trip) passes through taro fields, dense jungle, and stream crossings to reach a stunning plunge pool beneath a 250-foot waterfall. A guided tour is required by the landowners — this also gives you rich cultural context about the valley.',
              details: [
                '🥾 Distance: ~4 miles round trip, moderate terrain with some stream crossings',
                '👶 Baby carrier strongly recommended — baby can ride on your back or chest for the hike',
                '🏛️ Guide required: contact Halawa Valley Cultural Tours or Pilipo Solatorio (book in advance)',
                '⏰ Start early — the valley heats up by midday and the hike takes 3-4 hours',
                '💧 Bring plenty of water — the hike is in a humid valley',
                '🌊 The waterfall pool is cool and refreshing — bring a swimsuit'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book your Halawa Valley guide at least a week in advance — there are only a few operators and availability is limited. Cost is around $30-60 per person. Cash only (no ATM in the valley!). The cultural stories your guide shares make the hike truly special.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Halawa Bay Beach & Stream',
              description: 'After the hike, cool off at Halawa Bay. There\'s a calm, shaded freshwater stream that flows into the bay — perfect for rinsing off and for baby to splash safely. The bay itself can have surf (not safe for babies), but the stream mouth area is always calm.',
              details: [
                '🌊 Halawa Bay surf: can be heavy — adults only, experienced surfers',
                '💧 Freshwater stream: always calm, shaded by hau and breadfruit trees',
                '🍃 The valley is one of the most verdant spots in all of Hawaii — just sit and absorb it',
                '🧺 Bring a lunch from your rental or Kaunakakai bakery — no food vendors in the valley'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Paddlers Restaurant & Bar',
              description: 'Back in Kaunakakai after the long valley day, Paddlers is the perfect reward. Try the fresh fish special if available — the ahi is often caught same-day.',
              meta: '💰 $$ · 📍 10 Ala Malama Ave, Kaunakakai'
            }
          ],
          tips: [
            { type: 'tip', text: 'After a full valley hike day with a baby, dinner at Paddlers and an early bedtime is the perfect end. Halawa is a 27-mile drive from Kaunakakai — it\'s a commitment, but absolutely worth it.' }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1540, lng: -156.7620, label: 'Halawa Valley Trailhead', num: 1, cat: 'attraction', desc: 'Start of guided hike to Mo\'oula Falls — book guide in advance' },
        { lat: 21.1573, lng: -156.7488, label: 'Mo\'oula Falls', num: 2, cat: 'attraction', desc: '250-foot waterfall with plunge pool — highlight of the Halawa Valley hike' },
        { lat: 21.1624, lng: -156.7534, label: 'Halawa Bay', num: 3, cat: 'attraction', desc: 'Scenic bay at the mouth of Halawa Valley — freshwater stream safe for babies' },
        { lat: 21.0902, lng: -157.0222, label: 'Molokai Burger', num: 4, cat: 'food', desc: 'Quick grab on the way out or back — simple local fast food in Kaunakakai' },
        { lat: 21.0902, lng: -157.0222, label: 'Paddlers Restaurant & Bar', num: 5, cat: 'food', desc: 'Kaunakakai\'s best dinner spot — fresh fish and cold beer after the hike' }
      ]
    },
    {
      num: 5,
      date: '2026-05-15',
      neighborhoods: 'Kualapuu · Hoolehua · West End',
      title: 'Farm Day — Macadamia Nuts, Sugar Mill & Slow West End',
      description: 'A slower day exploring Molokai\'s agricultural heart. Purdy\'s Macadamia Nut Farm is one of the most genuine farm experiences in Hawaii. The R.W. Meyer Sugar Mill is a fascinating window into 19th-century island history. End with a long afternoon at Papohaku Beach.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Purdy\'s Macadamia Nut Farm',
              description: 'Tuddie Purdy runs one of the last family macadamia nut farms in Hawaii on his ancestral land in Hoolehua. He personally walks visitors through his 50 trees, explaining how mac nuts grow, how to crack them, and letting you taste nuts fresh off the tree. It\'s completely free — and utterly authentic.',
              details: [
                '🥜 Tuddie Purdy personally leads tours — open Mon–Fri and Sat morning',
                '🌿 No admission fee — donations welcome and appreciated',
                '🍼 Baby-friendly: flat grounds, shade, very relaxed pace',
                '📍 Lihi Pali Ave, Hoolehua (ask locals if lost — everyone knows Purdy\'s)',
                '⏰ Open roughly 9:30am–3:30pm, best to call ahead: (808) 567-6601'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'R.W. Meyer Sugar Mill Museum',
              description: 'The restored R.W. Meyer Sugar Mill (circa 1878) is Hawaii\'s only restored 19th-century sugar mill. It\'s small but fascinating — original machinery still in place, good historical context about Molokai\'s plantation era. Right next to it is the Molokai Museum.',
              details: [
                '🏭 Admission: small fee (~$2.50 adults)',
                '🏛️ Connected to the Molokai Museum — combined ticket available',
                '🌿 Beautiful grounds with mountain views — good lunch picnic spot nearby',
                '📍 Highway 470, near Kualapuu'
              ]
            },
            {
              title: 'Kualapu\'u Cookhouse Lunch',
              description: 'The Kualapu\'u Cookhouse (also known as Coffees of Hawaii Cookhouse) is right near your home base — a relaxed café and lunch spot with good local food and views of the coffee plantation.',
              details: [
                '☕ Local Molokai coffee (grown on-island) — a must-try',
                '🍽️ Simple but good: burgers, local plates, salads',
                '🌴 Views of the Coffees of Hawaii plantation — Molokai\'s famous coffee growing region'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kualapu\'u Cookhouse (Coffees of Hawaii)',
              description: 'Casual café near your home base in Kualapuu — local Molokai coffee, fresh lunch plates, and coffee plantation views. A very baby-friendly stop.',
              meta: '💰 $ · 📍 Farrington Hwy, Kualapuu · Hours can vary — call ahead'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Long Afternoon at Papohaku Beach',
              description: 'Spend the long afternoon hours at Papohaku — your last proper west-end beach day. Three miles of white sand and you might share it with one or two other people. Set up your shade tent, let the baby play in the sand, wade in the shallows. This is what Molokai is all about.',
              details: [
                '🏖️ 3 miles of white sand beach — almost always empty',
                '🌊 May can have gentle to moderate shorebreak — wade close to shore with baby',
                '🌅 Stay for golden hour — the light on this beach is extraordinary',
                '🍹 Papohaku Beach Park has restrooms and a small pavilion area'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Papohaku is one of the most unspoiled beaches in Hawaii. On weekdays in May, you may literally have the entire 3-mile beach to yourselves. Let that sink in.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hiro\'s Ohana Grill — Pesto Chicken Night',
              description: 'Back to Hotel Molokai\'s lanai for another oceanfront dinner. If pesto chicken is on the menu, order it — it\'s a local favorite. The atmosphere at dusk with the ocean sounds is pure magic.',
              meta: '💰 $$ · 📍 Hotel Molokai, Kamehameha V Hwy'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1528, lng: -157.0633, label: 'Purdy\'s Macadamia Nut Farm', num: 1, cat: 'attraction', desc: 'Family-run mac nut farm with personal tours by Tuddie Purdy — free' },
        { lat: 21.1332, lng: -157.0191, label: 'R.W. Meyer Sugar Mill', num: 2, cat: 'attraction', desc: 'Hawaii\'s only restored 19th-century sugar mill, small museum' },
        { lat: 21.1541, lng: -157.0430, label: 'Kualapu\'u Cookhouse / Coffees of Hawaii', num: 3, cat: 'food', desc: 'Local café with Molokai-grown coffee and lunch near your home base' },
        { lat: 21.1165, lng: -157.2518, label: 'Papohaku Beach', num: 4, cat: 'attraction', desc: '3-mile empty white sand beach — perfect afternoon spot' },
        { lat: 21.0902, lng: -157.0222, label: 'Hiro\'s Ohana Grill', num: 5, cat: 'food', desc: 'Oceanfront dinner at Hotel Molokai — local fish and pesto chicken' }
      ]
    },
    {
      num: 6,
      date: '2026-05-16',
      neighborhoods: 'Kalaupapa Lookout · Kapuaiwa · Kawili Beach',
      title: 'North Shore Views, Coconut Grove & Hidden Beach',
      description: 'The dramatic north coast of Molokai has the world\'s tallest sea cliffs. You can\'t go down to Kalaupapa with a baby (permit required, 16+ only), but the lookout above is one of the most awe-inspiring views on Earth. After, explore the ancient Kapuaiwa Coconut Grove and find Kawili Beach for a final afternoon swim.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kalaupapa National Historical Park Lookout',
              description: 'Drive up to Palaau State Park for the Kalaupapa Lookout — a breathtaking view down 1,600 feet of sheer sea cliffs to the isolated Kalaupapa peninsula below. This is where Father Damien ministered to leprosy patients in the 1800s. The view is utterly dramatic; the history is profound.',
              details: [
                '🏔️ Sea cliffs: up to 3,900 feet — among the tallest in the world',
                '🌿 Palaau State Park has a beautiful ironwood forest — cool and shaded',
                '🔭 Bring binoculars: you can see the old settlement and airstrip far below',
                '👶 Baby-friendly: flat boardwalk to the lookout, good safety fencing, shaded park',
                '⚠️ The descent to Kalaupapa (mule ride or hiking) requires a permit and is 16+ — not an option with a baby'
              ]
            },
            {
              title: 'Phallic Rock (Kauleonanahoa)',
              description: 'Right in Palaau State Park is this famous ancient Hawaiian stone formation, associated with fertility legend. It\'s a short walk through the forest — more culturally interesting than visually dramatic, but worth the 5-minute detour.',
              details: [
                '🪨 Ancient Hawaiian cultural site in Palaau State Park',
                '🌲 Beautiful ironwood forest walk to reach it — peaceful and shaded'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Kapuaiwa Coconut Grove',
              description: 'One of the last royal coconut groves in Hawaii, planted in the 1860s by King Kamehameha V. The grove stands on the ocean shore near Kaunakakai — hundreds of coconut palms silhouetted against the water. Visually stunning, historically significant.',
              details: [
                '🌴 Hundreds of coconut palms — one of Hawaii\'s most photogenic spots',
                '⚠️ Do NOT walk under the palms — falling coconuts are a real hazard',
                '📸 Best photos from the road looking toward the ocean — safe and striking',
                '🍼 Short stop — 15-20 minutes is enough to admire and photograph'
              ]
            }
          ],
          meals: [
            {
              type: '🍔 Lunch',
              name: 'Molokai Burger',
              description: 'Simple, affordable, and consistently good. Molokai Burger is a local institution for quick food in Kaunakakai.',
              meta: '💰 $ · 📍 Kamehameha V Hwy, Kaunakakai'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kawili Beach — The Hidden Local Gem',
              description: 'Kawili Beach (also called One Ali\'i Beach Park) is a small, protected beach near Kaunakakai with calm waters and plenty of shade. It\'s local and low-key — no tourists, no hype — just families from the island swimming and relaxing. Perfect for a final gentle swim with baby.',
              details: [
                '🏖️ Calm, protected water — safe for babies and toddlers',
                '🌴 Good shade trees along the beach',
                '🚿 Beach park has restrooms and outdoor rinse area',
                '👨‍👩‍👧 Very family-oriented local beach — a real slice of Molokai daily life'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'One Ali\'i Beach Park (and its neighbor Kiowea Park) are where Molokai families come to relax and picnic on weekends. If you visit on a Saturday afternoon, you may get to experience a real Molokai community gathering — potlucks, kids playing, ukulele. It\'s a genuine gift.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Walk at Papohaku Beach',
              description: 'One final sunset walk on Papohaku — your big, beautiful, empty farewell beach. Walk further than you have before. Find your spot. Watch the sun drop toward Oahu.',
              details: [
                '🌅 Last Molokai sunset — take it slow',
                '📸 Golden light on the white sand and your little family — the best photo of the trip'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Paddlers Restaurant & Bar — Final Dinner',
              description: 'Go back to Paddlers for your last dinner on Molokai. Order something you haven\'t tried yet — the short ribs, the ahi poke appetizer, or whatever the day\'s fresh catch is.',
              meta: '💰 $$ · 📍 10 Ala Malama Ave, Kaunakakai'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1925, lng: -156.9956, label: 'Kalaupapa Lookout / Palaau State Park', num: 1, cat: 'attraction', desc: '1,600-foot view down dramatic sea cliffs to the historic Kalaupapa peninsula' },
        { lat: 21.1925, lng: -156.9956, label: 'Phallic Rock (Kauleonanahoa)', num: 2, cat: 'attraction', desc: 'Ancient Hawaiian cultural rock formation in Palaau State Park forest' },
        { lat: 21.0912, lng: -157.0355, label: 'Kapuaiwa Coconut Grove', num: 3, cat: 'attraction', desc: 'Royal coconut grove planted by Kamehameha V in the 1860s — iconic Molokai view' },
        { lat: 21.0896, lng: -157.0270, label: 'One Ali\'i Beach Park (Kawili Beach)', num: 4, cat: 'attraction', desc: 'Protected local beach with calm water — a true Molokai family hangout' },
        { lat: 21.1165, lng: -157.2518, label: 'Papohaku Beach', num: 5, cat: 'attraction', desc: 'Final farewell sunset on Molokai\'s legendary 3-mile empty beach' },
        { lat: 21.0902, lng: -157.0222, label: 'Paddlers Restaurant & Bar', num: 6, cat: 'food', desc: 'Last dinner on Molokai — fresh ahi and cold beer' }
      ]
    },
    {
      num: 7,
      date: '2026-05-17',
      neighborhoods: 'Kaunakakai · Molokai Airport',
      title: 'Farewell Morning — One Last Beach, Then Fly Home',
      description: 'Checkout morning on Molokai. One early stop at Murphy\'s Beach for baby\'s final ocean moment, then a slow drive to the airport. You\'ll leave this island wondering why more people don\'t come here — and already planning your return.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Return to Murphy\'s Beach',
              description: 'A final morning at Murphy\'s Beach — the place where baby had their first ocean experience. The east-end light in the morning is extraordinary. Wade in the calm lagoon one last time, look out over the reef, let the island say goodbye properly.',
              details: [
                '🌅 Morning light on the east end is spectacular — the water turns brilliant turquoise',
                '🪸 Low tide in the morning often exposes more of the reef — beautiful for photos',
                '🕐 Allow 1-1.5 hours and keep track of your flight time'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Molokai Airport is tiny and flights are short, but Mokulele Airlines can be strict about check-in time (they sometimes close check-in 30 minutes before departure). Don\'t cut it close on your last day.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Return Car & Depart from Molokai Airport',
              description: 'Return your rental car (they\'ll meet you at the airport), check in for your Mokulele flight to Honolulu or Maui, and begin the journey home. The 10-minute takeoff roll gives you a final aerial view of the island you\'ve come to love.',
              details: [
                '✈️ Allow extra time for car return at the small airport',
                '🍰 Molokai Bread from Kanemitsu Bakery — grab a loaf or some hot bread at 7am if you pass through Kaunakakai early (a Molokai legend)',
                '📸 Window seat on departure for aerial views of Papohaku Beach and the north coast cliffs'
              ]
            }
          ],
          meals: [
            {
              type: '🍞 Breakfast',
              name: 'Kanemitsu Bakery — Molokai Bread',
              description: 'Kanemitsu\'s hot bread from the back door (late nights) or fresh bread in the morning is one of Molokai\'s most beloved traditions. A loaf of their famous sweet bread is the perfect final morning.',
              meta: '💰 $ · 📍 79 Ala Malama Ave, Kaunakakai · Early morning pickup'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0672, lng: -156.8667, label: 'Murphy\'s Beach — Final Visit', num: 1, cat: 'attraction', desc: 'Baby\'s first and last ocean stop — perfect calm lagoon goodbye' },
        { lat: 21.0902, lng: -157.0222, label: 'Kanemitsu Bakery', num: 2, cat: 'food', desc: 'Legendary Molokai bread — hot sweet bread, a true local institution' },
        { lat: 21.1529, lng: -157.0960, label: 'Molokai Airport (MKK)', num: 3, cat: 'attraction', desc: 'Return car and depart — window seat for aerial view of Papohaku Beach' },
        { lat: 21.0902, lng: -157.0222, label: 'Kaunakakai Town', num: 4, cat: 'attraction', desc: 'Final drive through the heart of Molokai\'s small-town main street' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (vacation rental)', budget: '$150–200/night', midrange: '$200–350/night', luxury: '$350–600/night' },
    { category: 'Meals (per couple per day)', budget: '$60–80/day', midrange: '$80–150/day', luxury: 'N/A — Molokai has limited fine dining' },
    { category: 'Car Rental', budget: '$60–80/day', midrange: '$80–120/day', luxury: '$120–180/day (4WD SUV)' },
    { category: 'Activities', budget: '$0–30/day', midrange: '$30–80/day', luxury: '$80–150/day' },
    { category: 'Halawa Valley Guide', budget: '$60–120 (couple)', midrange: '$60–120 (couple)', luxury: '$150+ (private)' },
    { category: 'SUP / Kayak Rental', budget: '$30–50/day', midrange: '$50–80/day', luxury: 'Private tour $120+' },
    { category: 'Flights (HNL or OGG to MKK)', budget: '$120–200 pp roundtrip', midrange: '$200–300 pp roundtrip', luxury: 'Charter $600+' },
    { category: '6-Night Total (2 adults + baby)', budget: '$2,500–4,000', midrange: '$4,500–7,000', luxury: '$7,000–10,000' }
  ],

  practicalInfo: [
    {
      title: '✈️ Getting to Molokai',
      items: [
        'Fly into Molokai Airport (MKK) via Mokulele Airlines from Honolulu (HNL) or Maui (OGG)',
        'Flight time: ~25 min from OGG, ~35 min from HNL on small propeller aircraft',
        'Book early — these are small planes with limited seats',
        'Car seat note: car seats can go in the hold on most Mokulele flights — confirm in advance'
      ]
    },
    {
      title: '🏡 Where to Stay',
      items: [
        'West End Vacation Rentals (near Papohaku Beach): best for beach access and sunsets — book on Airbnb or VRBO',
        'Hotel Molokai: the only actual hotel, oceanfront, east of Kaunakakai — great atmosphere, less beach access',
        'Kaunakakai area rentals: central location, closer to restaurants — less dramatic but convenient',
        'Budget estimate: $150–350/night depending on property and season'
      ]
    },
    {
      title: '🍼 Baby Travel Essentials',
      items: [
        'Bring ALL baby supplies from home or Honolulu — Friendly Market stocks basics but selection is limited',
        'Reef-safe sunscreen (SPF 50+) is required by Hawaiian law — bring a large supply',
        'A portable beach shade tent is essential — most beaches have little natural shade',
        'Baby carrier (front or back) is the best way to hike Halawa Valley and explore',
        'Earphones or soft ear muffs for the propeller flight — helpful for sensitive babies',
        'Compact stroller works for flat areas; carrier is better for uneven terrain'
      ]
    },
    {
      title: '🌡️ Weather in May',
      items: [
        'Temperatures: 78–85°F (26–29°C) daily',
        'South swell season begins in May — can produce surf at Papohaku and rock breaks',
        'Trade winds blow reliably from the northeast — afternoons can be breezy on the west end',
        'Rain is possible, especially in the mountains and east end — pack a light layer',
        'Ocean temperature: ~77°F (25°C) — very comfortable for wading and swimming'
      ]
    },
    {
      title: '💳 Money & Logistics',
      items: [
        'Bring cash — many places on Molokai are cash-only or have unreliable card readers',
        'One ATM in Kaunakakai (Bank of Hawaii) — withdraw enough on arrival day',
        'Cell service: limited outside Kaunakakai and the highway corridor — download offline maps',
        'Emergency: Molokai Community Hospital, Kaunakakai — (808) 553-5331',
        'Gas: fill up in Kaunakakai — no gas stations on the west or far east end'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
