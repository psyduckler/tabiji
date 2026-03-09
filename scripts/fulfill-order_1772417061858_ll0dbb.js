const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772417061858_ll0dbb',
  email: 'cdpartner@gmail.com',
  destination: 'Disneyland, Anaheim, CA',
  startDate: '2026-04-10',
  endDate: '2026-04-13',
  groupSize: '3-4',
  requests: ''
};

const itineraryData = {
  destination: 'Disneyland Resort, Anaheim',
  countryEmoji: '🇺🇸',
  title: 'The Ultimate Disneyland Adventure',
  subtitle: '4 days of magic across both parks for your crew of 3–4',
  description: "Four days at the Happiest Place on Earth — strategically planned so you hit every headliner ride, savour the best food in both parks, and still have time to soak in the atmosphere. This itinerary covers Disneyland Park and Disney California Adventure with a smart park-hopper flow, evening spectaculars, and insider tips that'll save you hours in line.",
  duration: '3 nights',
  dates: 'Apr 10 – Apr 13, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups & Friends',
  highlights: [
    'Rise of the Resistance — the best ride in any Disney park',
    'Radiator Springs Racers at golden hour',
    'Blue Bayou dinner inside Pirates of the Caribbean',
    'Fantasmic! and World of Color evening spectaculars',
    'Oga\'s Cantina craft cocktails in Star Wars: Galaxy\'s Edge'
  ],

  essentials: [
    { title: '🎟️ Tickets & Genie+', text: 'Buy multi-day Park Hopper tickets in advance. Lightning Lane Multi Pass lets you skip lines on popular rides — book at 7am on your visit day. Individual Lightning Lane ($$ extra) is worth it for Rise of the Resistance and Radiator Springs Racers.' },
    { title: '📱 Disneyland App', text: 'Download the Disneyland app before you go. It shows real-time wait times, lets you mobile-order food, join virtual queues, and manage Lightning Lane. It\'s essential — not optional.' },
    { title: '🕗 Rope Drop Strategy', text: 'Gates open 30 min before official opening. Be at the entrance by 7:30am. Head straight to the most popular ride in whichever park you start — you\'ll walk on with minimal wait.' },
    { title: '🅿️ Getting There', text: 'The Mickey & Friends parking structure ($35/day) is the main lot. Alternatively, stay at a hotel on Harbor Blvd for walking distance. Uber/Lyft drop-off is at the transport hub.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-10',
      neighborhoods: 'Disneyland Park — Adventureland · New Orleans Square · Frontierland · Star Wars: Galaxy\'s Edge',
      title: 'Disneyland Park — Classics & Galaxy\'s Edge',
      description: "Start your trip at the original Disneyland Park. Hit the west side first — the iconic dark rides, Star Wars: Galaxy\'s Edge, and the timeless attractions that Walt himself built. End the night with Fantasmic!",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rope Drop → Star Wars: Galaxy\'s Edge',
              description: "Arrive early and head straight to Galaxy\'s Edge. Ride Rise of the Resistance first — it\'s the crown jewel of Disney rides, an immersive 18-minute experience that puts you in a Star Wars battle. Then hit Smugglers Run while the land is still quiet.",
              details: [
                '🚀 Rise of the Resistance — arrive by park open, go directly here',
                '🎮 Smugglers Run — you pilot the Millennium Falcon (request pilot seats!)',
                '📸 Photo op: the full-scale Millennium Falcon in the morning light'
              ]
            },
            {
              title: 'Indiana Jones Adventure',
              description: 'Head to Adventureland for Indiana Jones — a thrilling jeep ride through a cursed temple. Lines build fast, so ride before 10am.',
              details: [
                '⚡ One of the park\'s best thrill rides',
                '🎢 Minimum height: 46 inches'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Use Lightning Lane Multi Pass for Indiana Jones and Big Thunder Mountain. Book at 7am sharp — popular slots go fast.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'New Orleans Square & Frontierland',
              description: 'Explore the charm of New Orleans Square — ride Pirates of the Caribbean and Haunted Mansion, two of Disney\'s greatest dark rides. Then head to Frontierland for Big Thunder Mountain Railroad, the wildest ride in the wilderness.',
              details: [
                '🏴‍☠️ Pirates of the Caribbean — the original, 16-minute boat ride',
                '👻 Haunted Mansion — 999 happy haunts, zero jump scares',
                '🤠 Big Thunder Mountain — fun, classic coaster for all comfort levels'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Blue Bayou Restaurant',
              description: 'Dine inside the Pirates of the Caribbean ride — you eat under a starlit bayou sky while boats float past. Cajun-inspired menu with excellent Monte Cristo sandwiches. Reservations essential.',
              meta: '💰 $$$ · 📍 New Orleans Square · Book 60 days ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Oga\'s Cantina',
              description: 'Head back to Galaxy\'s Edge for craft cocktails (and mocktails) in the most immersive bar Disney has ever built. DJ R-3X spins tunes, animatronic creatures lurk in corners, and the drinks are wildly creative.',
              details: [
                '🍸 Must-try: Fuzzy Tauntaun (foam that numbs your lips!)',
                '⏰ 45-minute time limit per party — reservations strongly recommended',
                '🍹 Non-alcoholic options are equally fun'
              ]
            },
            {
              title: 'Fantasmic!',
              description: 'End the night with Fantasmic! on the Rivers of America — a spectacular water, fire, and projection show featuring Mickey battling Disney villains. Arrive 30-45 min early for a good spot.',
              details: [
                '🎆 Check the app for showtimes — usually 9pm or 10pm',
                '📍 Best viewing: center of the river, New Orleans Square side',
                '💡 Dining packages guarantee reserved seating'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Rancho del Zocalo',
              description: 'Solid Mexican food in Frontierland with generous portions. Street tacos, burritos, and churros — great fuel before the evening show.',
              meta: '💰 $$ · 📍 Frontierland · Mobile order recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.8154, lng: -117.9220, label: 'Star Wars: Galaxy\'s Edge', num: 1, cat: 'attraction', desc: 'Rise of the Resistance & Smugglers Run' },
        { lat: 33.8114, lng: -117.9209, label: 'Adventureland', num: 2, cat: 'attraction', desc: 'Indiana Jones Adventure & Jungle Cruise' },
        { lat: 33.8119, lng: -117.9223, label: 'New Orleans Square', num: 3, cat: 'attraction', desc: 'Pirates of the Caribbean & Haunted Mansion' },
        { lat: 33.8127, lng: -117.9234, label: 'Frontierland', num: 4, cat: 'attraction', desc: 'Big Thunder Mountain Railroad' },
        { lat: 33.8119, lng: -117.9223, label: 'Blue Bayou Restaurant', num: 5, cat: 'food', desc: 'Dine inside the Pirates ride under a starlit sky' },
        { lat: 33.8154, lng: -117.9220, label: 'Oga\'s Cantina', num: 6, cat: 'food', desc: 'Immersive Star Wars bar with craft cocktails' }
      ]
    },
    {
      num: 2,
      date: '2026-04-11',
      neighborhoods: 'Disney California Adventure — Cars Land · Avengers Campus · Pixar Pier · Grizzly Peak',
      title: 'California Adventure — Thrills, Heroes & Sunset',
      description: "Today is all about Disney California Adventure. From the neon glow of Cars Land to the superhero action of Avengers Campus, this park packs incredible rides, excellent food, and the stunning World of Color nighttime show.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rope Drop → Radiator Springs Racers',
              description: 'Head straight to Cars Land and ride Radiator Springs Racers — a slot-car race through the stunning desert canyons of Radiator Springs. This ride consistently has 60-90 min waits, but at rope drop you can walk on in 15 minutes.',
              details: [
                '🏎️ The most beautifully themed ride at the resort',
                '📸 Cars Land at rope drop is peaceful and gorgeous',
                '🎢 Gentle enough for most, thrilling enough for coaster fans'
              ]
            },
            {
              title: 'Avengers Campus',
              description: 'Web Slingers: A Spider-Man Adventure is a fun interactive shooter ride. Watch for live superhero encounters — Spider-Man does real stunts on the rooftops and characters roam the campus throughout the day.',
              details: [
                '🕷️ Web Slingers — flick your wrists to sling webs (competitive!)',
                '🦸 Live encounters: Spider-Man, Black Panther, Black Widow, Thor',
                '⚡ Check the app for character appearance times'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Individual Lightning Lane for Radiator Springs Racers is $$ but worth it if you miss rope drop. Buy through the app starting at 7am.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pixar Pier & Grizzly Peak',
              description: 'Ride the Incredicoaster (a full-loop launch coaster along the boardwalk), explore Pixar Pier\'s carnival games, and cool off on Grizzly River Run — you WILL get soaked.',
              details: [
                '🎢 Incredicoaster — launches you through enclosed story scenes',
                '🐻 Grizzly River Run — a whitewater raft ride, bring a poncho or embrace it',
                '🎡 Pixar Pal-A-Round — the swinging gondolas are NOT for the faint of heart'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Lamplight Lounge',
              description: 'The best sit-down restaurant in California Adventure. Waterfront deck overlooking Pixar Pier with excellent lobster nachos, burgers, and creative cocktails.',
              meta: '💰 $$$ · 📍 Pixar Pier · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Cars Land at Night',
              description: "Return to Cars Land after dark — the neon signs light up and the entire land transforms into a glowing Route 66 dreamscape. It\'s one of the most magical sights at any Disney park. Ride Radiator Springs Racers again at night for a completely different experience.",
              details: [
                '🌙 The neon transformation happens at sunset — don\'t miss it',
                '📸 Best photo spot: in front of the Cozy Cone Motel',
                '🏎️ Night ride on Radiator Springs Racers is a must'
              ]
            },
            {
              title: 'World of Color',
              description: 'Disney California Adventure\'s signature nighttime show — massive water fountains, projections, fire, and lasers set to Disney music on Paradise Bay. It\'s emotional, spectacular, and unmissable.',
              details: [
                '🌊 Arrive 30-45 min early for a good spot at Paradise Bay',
                '📍 Best viewing: center rail along the bay',
                '💧 Front rows get misted — embrace it or stand back'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Cozy Cone Motel',
              description: 'Quick-service cones in Cars Land — chili cone queso, bread cones with soup, and the famous popcorn cone. Fun, shareable, and perfect while waiting for World of Color.',
              meta: '💰 $ · 📍 Cars Land'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.8062, lng: -117.9196, label: 'Cars Land', num: 1, cat: 'attraction', desc: 'Radiator Springs Racers & neon Route 66 magic' },
        { lat: 33.8069, lng: -117.9178, label: 'Avengers Campus', num: 2, cat: 'attraction', desc: 'Web Slingers & live superhero encounters' },
        { lat: 33.8048, lng: -117.9213, label: 'Pixar Pier', num: 3, cat: 'attraction', desc: 'Incredicoaster & boardwalk fun' },
        { lat: 33.8070, lng: -117.9230, label: 'Grizzly Peak', num: 4, cat: 'attraction', desc: 'Grizzly River Run whitewater rafting' },
        { lat: 33.8048, lng: -117.9213, label: 'Lamplight Lounge', num: 5, cat: 'food', desc: 'Waterfront dining with lobster nachos & cocktails' },
        { lat: 33.8062, lng: -117.9196, label: 'Cozy Cone Motel', num: 6, cat: 'food', desc: 'Iconic Cars Land quick-service cones' }
      ]
    },
    {
      num: 3,
      date: '2026-04-12',
      neighborhoods: 'Disneyland Park — Fantasyland · Tomorrowland · Main Street U.S.A. · Toontown',
      title: 'Disneyland Deep Dive — Fantasyland, Tomorrowland & Fireworks',
      description: "Back to Disneyland Park to conquer the east side. Fantasyland\'s beloved dark rides, Tomorrowland\'s Space Mountain, Mickey\'s Toontown, and the grand finale — fireworks over Sleeping Beauty Castle.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rope Drop → Matterhorn & Space Mountain',
              description: 'Hit Matterhorn Bobsleds first — it\'s an icon. Then head to Tomorrowland for Space Mountain, the classic indoor roller coaster in pitch darkness. Both have long afternoon waits, so morning is key.',
              details: [
                '🏔️ Matterhorn Bobsleds — the world\'s first tubular steel coaster',
                '🚀 Space Mountain — smooth, dark, and thrilling',
                '🎢 Buzz Lightyear Astro Blasters nearby — a fun competitive shooter ride'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fantasyland & Mickey\'s Toontown',
              description: 'Take in the soul of Disneyland — "it\'s a small world," Peter Pan\'s Flight, Mr. Toad\'s Wild Ride, and the recently reimagined Mickey\'s Toontown. Peter Pan has notoriously long waits, so use Lightning Lane.',
              details: [
                '🧚 Peter Pan\'s Flight — magically flies over London, worth the wait',
                '🐸 Mr. Toad\'s Wild Ride — wonderfully bizarre, Disneyland exclusive',
                '🌎 "it\'s a small world" — the classic boat ride, genuinely charming',
                '🏠 Mickey\'s Toontown — recently reimagined with new play areas'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Café Orléans',
              description: 'Sit-down French-Cajun dining on a beautiful patio in New Orleans Square. Famous for pommes frites (three-cheese monte cristo) and mint juleps.',
              meta: '💰 $$ · 📍 New Orleans Square · Great patio seating'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Main Street U.S.A. & Castle Fireworks',
              description: "As night falls, stroll down Main Street U.S.A. — the iconic entrance boulevard lit with gas lamps and lined with shops. Then find your spot for the fireworks spectacular over Sleeping Beauty Castle. It\'s pure Disney magic.",
              details: [
                '🏰 Wondrous Journeys fireworks — projections on the castle + Main Street buildings',
                '📍 Best spot: in front of the castle hub or halfway down Main Street',
                '⏰ Arrive 30-45 min early — Main Street fills fast',
                '🛍️ Shops on Main Street stay open after fireworks — great for last-minute souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Carthay Circle Restaurant',
              description: 'The signature fine-dining restaurant at California Adventure, inside a replica of the theater where Snow White premiered. Excellent cocktails, upscale American cuisine, and a sophisticated atmosphere.',
              meta: '💰 $$$$ · 📍 Buena Vista Street, DCA · Park Hopper after fireworks'
            }
          ],
          tips: [
            { type: 'tip', text: 'After Disneyland fireworks, park-hop to California Adventure for a late dinner at Carthay Circle — the crowds thin out and the atmosphere is wonderful.' }
          ]
        }
      ],
      mapPins: [
        { lat: 33.8129, lng: -117.9180, label: 'Matterhorn Bobsleds', num: 1, cat: 'attraction', desc: 'Iconic alpine coaster through the mountain' },
        { lat: 33.8124, lng: -117.9167, label: 'Space Mountain', num: 2, cat: 'attraction', desc: 'Classic indoor coaster in pitch darkness' },
        { lat: 33.8137, lng: -117.9188, label: 'Fantasyland', num: 3, cat: 'attraction', desc: 'Peter Pan, Small World, Mr. Toad\'s Wild Ride' },
        { lat: 33.8151, lng: -117.9185, label: 'Mickey\'s Toontown', num: 4, cat: 'attraction', desc: 'Recently reimagined interactive cartoon world' },
        { lat: 33.8116, lng: -117.9196, label: 'Main Street U.S.A.', num: 5, cat: 'attraction', desc: 'The iconic boulevard to Sleeping Beauty Castle' },
        { lat: 33.8119, lng: -117.9223, label: 'Café Orléans', num: 6, cat: 'food', desc: 'French-Cajun patio dining in New Orleans Square' },
        { lat: 33.8084, lng: -117.9190, label: 'Carthay Circle Restaurant', num: 7, cat: 'food', desc: 'Signature fine dining on Buena Vista Street' }
      ]
    },
    {
      num: 4,
      date: '2026-04-13',
      neighborhoods: 'Downtown Disney · Both Parks — Re-rides & Favorites',
      title: 'Victory Lap — Re-rides, Downtown Disney & Farewell',
      description: "Your final day is a flex day — re-ride your favorites, catch anything you missed, explore Downtown Disney\'s shops and restaurants, and soak in the last drops of magic before heading home.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Re-Ride Your Favorites',
              description: "Start the morning re-riding the headliners — Rise of the Resistance, Radiator Springs Racers, or whichever rides your group loved most. Morning lines are shorter, and second rides often reveal details you missed.",
              details: [
                '🔄 Rise of the Resistance has different random scenarios — ride again!',
                '🏎️ Radiator Springs in morning light vs. night — both are gorgeous',
                '🎢 Space Mountain front row vs. back row are totally different experiences'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Downtown Disney District',
              description: "Step outside the parks to Downtown Disney — a free-entry shopping, dining, and entertainment district. Browse the massive World of Disney store, check out LEGO Store builds, and grab some last souvenirs.",
              details: [
                '🛍️ World of Disney — the biggest Disney merchandise store anywhere',
                '🧱 LEGO Store — incredible Disney-themed LEGO builds on display',
                '🎮 Free to enter — no park ticket required'
              ]
            },
            {
              title: 'Catch What You Missed',
              description: 'Head back into the parks for anything left on your list. Jungle Cruise in Disneyland, Guardians of the Galaxy – Mission: BREAKOUT! in DCA, or a second round of Oga\'s Cantina.',
              details: [
                '🚢 Jungle Cruise — the puns alone are worth it',
                '🗼 Guardians: Mission BREAKOUT! — intense drop tower in the Hollywood Tower',
                '🍸 Oga\'s Cantina Round 2 — try different drinks this time'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Tortilla Jo\'s',
              description: 'Upscale Mexican restaurant in Downtown Disney with a fun outdoor patio, tableside guacamole, and strong margaritas. Great for a group celebration.',
              meta: '💰 $$ · 📍 Downtown Disney District'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'One Last Walk Down Main Street',
              description: "Before you leave, take one final stroll down Main Street U.S.A. toward the castle. Look back from the entrance — Sleeping Beauty Castle framed by the gas lamps and turrets — and take your farewell photo. You\'ll be back.",
              details: [
                '📸 The classic Sleeping Beauty Castle shot from the Main Street hub',
                '🍦 Get a Dole Whip from Adventureland as your farewell treat',
                '✨ If timing works, catch the fireworks one more time'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Napa Rose',
              description: 'The finest restaurant at Disneyland Resort, inside Disney\'s Grand Californian Hotel. California wine country cuisine with an extraordinary wine list. The perfect farewell dinner — no park ticket needed.',
              meta: '💰 $$$$ · 📍 Disney\'s Grand Californian Hotel · Reservations essential'
            }
          ],
          tips: [
            { type: 'tip', text: 'Napa Rose is inside the Grand Californian Hotel — accessible from Downtown Disney without a park ticket. Book well ahead, it\'s the best meal at the resort.' }
          ]
        }
      ],
      mapPins: [
        { lat: 33.8095, lng: -117.9260, label: 'Downtown Disney District', num: 1, cat: 'attraction', desc: 'Shopping, dining & entertainment — no ticket needed' },
        { lat: 33.8154, lng: -117.9220, label: 'Galaxy\'s Edge (Re-ride)', num: 2, cat: 'attraction', desc: 'Rise of the Resistance — ride it again!' },
        { lat: 33.8062, lng: -117.9196, label: 'Cars Land (Re-ride)', num: 3, cat: 'attraction', desc: 'Radiator Springs Racers for one more lap' },
        { lat: 33.8069, lng: -117.9178, label: 'Guardians: Mission BREAKOUT!', num: 4, cat: 'attraction', desc: 'Intense drop tower in the Hollywood Tower' },
        { lat: 33.8095, lng: -117.9260, label: 'Tortilla Jo\'s', num: 5, cat: 'food', desc: 'Upscale Mexican with tableside guacamole' },
        { lat: 33.8100, lng: -117.9245, label: 'Napa Rose', num: 6, cat: 'food', desc: 'Grand Californian\'s finest — California wine country cuisine' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Park Tickets (4-day Hopper)', budget: '$350–400pp', midrange: '$400–500pp', luxury: '$500–600pp' },
    { category: 'Lightning Lane', budget: '$30/day pp', midrange: '$30 + ILL $20–25/ride', luxury: 'All ILL rides ($50+/day pp)' },
    { category: 'Accommodation', budget: '$150–250/night', midrange: '$250–450/night', luxury: '$500–900/night (on-property)' },
    { category: 'Meals (per person)', budget: '$40–60/day', midrange: '$80–120/day', luxury: '$150–250/day' },
    { category: 'Parking', budget: '$35/day', midrange: '$35/day', luxury: '$55/day (preferred)' },
    { category: '4-Day Total (group of 4)', budget: '$4,000–6,000', midrange: '$7,000–10,000', luxury: '$12,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into John Wayne (SNA) — 15 min to Disneyland, or LAX — 45 min', 'Uber/Lyft from SNA is ~$20–30, from LAX ~$50–70', 'No rental car needed if staying near the resort — everything is walkable'] },
    { title: '🏨 Where to Stay', items: ['Disney\'s Grand Californian — on-property luxury, early entry perk', 'Disneyland Hotel — classic Disney theming, monorail access', 'Good Neighbor Hotels on Harbor Blvd — walking distance, half the price', 'JW Marriott or Westin Anaheim — upscale off-property options'] },
    { title: '🌡️ Weather (April)', items: ['Expect 65–75°F (18–24°C) — perfect theme park weather', 'Morning fog ("May Gray") can linger but burns off by noon', 'Evenings cool to ~55°F — bring a light jacket for nighttime shows', 'Rain is very unlikely in April'] },
    { title: '💡 Pro Tips', items: ['Rope drop > staying late for shorter waits', 'Mobile order ALL quick-service meals — skip the food lines', 'Bring a portable phone charger — the app drains battery fast', 'Wear comfortable shoes — you\'ll walk 20,000+ steps per day', 'Bring a refillable water bottle — free water at any quick-service counter'] },
    { title: '📱 Must-Have Apps', items: ['Disneyland App — wait times, Lightning Lane, mobile order, virtual queues', 'Google Maps — for navigating Anaheim and getting to/from airport', 'Uber/Lyft — for airport transfers and off-site dining'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
