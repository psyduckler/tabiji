const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771869372670_na63ll',
  email: 'gjdudh@gmail.com',
  destination: 'Orlando, FL, USA',
  startDate: '2026-02-27',
  endDate: '2026-03-05',
  groupSize: 2,
  travelStyle: 'Adventure, Relaxation',
  dining: 'Mix of everything',
  budget: '',
  requests: ''
};

const itineraryData = {
  destination: 'Orlando, Florida',
  countryEmoji: '🎢',
  title: 'Orlando: Theme Park Thrills & Florida Relaxation',
  subtitle: '7 days of epic rides, crystal springs, space launches & unforgettable dining for two',
  description: "Orlando is the world's theme park capital — but it's also Florida's best-kept secret for natural adventures, crystal-clear springs, and surprising culinary depth. This itinerary balances the adrenaline of Universal's brand-new Epic Universe and Disney's Magic Kingdom with kayaking wild rivers, swimming with dolphins at Discovery Cove, and a rocket-fueled day at Kennedy Space Center. Evenings wind down with everything from Spanish tapas on International Drive to fine dining in charming Winter Park. Orlando in late February is perfection: warm, sunny, and just before spring break crowds.",
  duration: '6 nights',
  dates: 'Feb 27 – Mar 5, 2026',
  budget: '$$–$$$',
  pace: 'Active with downtime',
  bestFor: 'Adventurous Couples',
  highlights: [
    "Universal Epic Universe — Orlando's spectacular new theme park (opened May 2025)",
    'Swim with dolphins at Discovery Cove — ultimate adventure + relaxation',
    'Kennedy Space Center: launch pads, astronaut training & rocket garden',
    'Kayaking crystal-clear Wekiwa Springs with manatees and wildlife',
    'Disney Magic Kingdom after dark — fireworks from the castle'
  ],

  essentials: [
    { title: '🌤️ Late February Weather', text: "Orlando in late February is gorgeous: 72–80°F (22–27°C), low humidity, and mostly sunny skies. Pack light layers for air-conditioned parks and light rain gear just in case. It's the sweet spot before spring break crowds hit." },
    { title: '🚗 Getting Around', text: 'A rental car is recommended — it unlocks Kennedy Space Center, Wekiwa Springs, and Winter Park. Rideshare (Uber/Lyft) works well for International Drive and Disney/Universal area. I-4 can be slow during rush hour (8–9am, 4–6pm).' },
    { title: '🎢 Park Strategy', text: 'Buy theme park tickets in advance online (always cheaper). At Universal and Disney, use the Express/Lightning Lane passes to skip lines on headliner rides. Arrive at rope drop (opening time) for shortest waits on top attractions.' },
    { title: '🐬 Discovery Cove Tips', text: 'Discovery Cove limits daily guests to ~1,000 — book as early as possible. The dolphin swim experience is ~30 minutes and includes all-day access to the reef, lazy river, and aviary. All food and drinks are included in the ticket price.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-27',
      neighborhoods: 'International Drive · Disney Springs',
      title: 'Arrival — The World\'s Theme Park Capital Awaits',
      description: "Touch down in Orlando and feel the energy immediately. Get oriented on International Drive — the 11-mile corridor of entertainment, dining, and attractions — then ease into the trip with a sunset stroll and dinner. Disney Springs makes for a perfect low-key first evening: outdoor waterfront shopping, live music, and restaurants ranging from a craft beer hall to high-end steakhouses.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Get Oriented',
              description: "Pick up your rental car and check into your hotel. The International Drive / Convention Center area puts you at the center of everything — Disney, Universal, and SeaWorld are all within 15 minutes. I-Drive itself is worth a walk for the vibe.",
              details: [
                '🏨 Great base options: Hyatt Regency, Rosen Shingle Creek, or Loews Sapphire Falls',
                '🚗 Rental cars: pick up at MCO — budget 30 mins for rental + drive to hotel',
                '📍 International Drive runs south–north along the theme park corridor'
              ]
            },
            {
              title: 'Pointe Orlando & I-Drive Exploration',
              description: "Take a walk along International Drive to get your bearings. Pointe Orlando is an outdoor mall and entertainment complex with restaurants, a comedy club, and a rooftop bar. The giant ICON Park Ferris wheel (400 feet tall) is a great first Orlando photo.",
              details: [
                '🎡 ICON Park observation wheel — 400ft tall, panoramic views of Orlando',
                '🏬 Pointe Orlando: outdoor dining, entertainment, casual browsing',
                '🍦 Grab a snack at any of the dozens of food spots along the strip'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Grocery run tip: Hit a Publix or Whole Foods near your hotel on arrival day. Stocking up on breakfast items, snacks, and drinks saves significant money during a theme park trip." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Disney Springs Waterfront Stroll',
              description: "Drive 15 minutes to Disney Springs for a magical first evening in Orlando. This free-entry outdoor complex sits on Village Lake with live entertainment, boutique shops, and a huge range of restaurants. No Disney ticket needed — just show up and enjoy the atmosphere.",
              details: [
                '🎵 Live music at multiple venues — Blues Brothers show is a crowd favorite',
                '🛍️ World of Disney is the largest Disney store on Earth',
                '🍺 Jock Lindsey\'s Hangar Bar has creative cocktails with Indiana Jones theming'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Wine Bar George at Disney Springs',
              description: "Master Sommelier George Miliotes runs this acclaimed wine bar with small plates perfect for sharing — charcuterie, flatbreads, roasted chicken, and a knockout cheese selection. One of Orlando's top-rated restaurants.",
              meta: '💰 $$$ · 📍 Disney Springs, Lake Buena Vista · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.4447, lng: -81.4668, label: 'International Drive', num: 1, cat: 'attraction', desc: 'Orlando\'s entertainment corridor — 11 miles of parks, dining & fun' },
        { lat: 28.4452, lng: -81.4665, label: 'ICON Park / Ferris Wheel', num: 2, cat: 'attraction', desc: '400-foot observation wheel with panoramic Orlando views' },
        { lat: 28.4440, lng: -81.4675, label: 'Pointe Orlando', num: 3, cat: 'attraction', desc: 'Outdoor shopping and entertainment complex on I-Drive' },
        { lat: 28.3699, lng: -81.5169, label: 'Disney Springs', num: 4, cat: 'attraction', desc: 'Free-entry waterfront complex — shops, restaurants, live music' },
        { lat: 28.3705, lng: -81.5162, label: 'Wine Bar George', num: 5, cat: 'food', desc: 'Award-winning wine bar with charcuterie and small plates' }
      ]
    },
    {
      num: 2,
      date: '2026-02-28',
      neighborhoods: 'Universal Orlando Resort · Epic Universe',
      title: 'Universal Epic Universe — The Future of Theme Parks',
      description: "Epic Universe opened in May 2025 and instantly became one of the world's greatest theme parks. Five immersive worlds await: the Wizarding World of Harry Potter (Ministry of Magic), How to Train Your Dragon Isle, Super Nintendo World, Monster-Verse, and Celestial Park. Plan a full day here — there's more than enough to fill it, and the rides are genuinely groundbreaking.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Epic Universe Rope Drop',
              description: "Arrive 30 minutes before park opening for rope drop. Head straight to the most popular attractions first — Super Nintendo World's Mario Kart: Bowser's Challenge and Harry Potter's Ministry of Magic rides will have the longest waits. Morning hours are your golden window.",
              details: [
                '⏰ Park typically opens at 9am — arrive by 8:30am',
                '🎮 Super Nintendo World: Mario Kart ride + interactive wristband experiences',
                '🧙 Wizarding World (Ministry of Magic): brand-new Harry Potter storyline, set in 1920s Paris',
                '🐉 How to Train Your Dragon Isle: Hiccup & Toothless flying coaster',
                '👹 Monster-Verse: Universal classic monsters reimagined'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Buy the Universal Express Pass for Epic Universe — it's worth it for a one-day visit to avoid 60–90 minute waits on the top rides. Purchase in advance online." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Celestial Park & Slower Exploration',
              description: "After hitting the big rides, take time to explore Celestial Park — the beautiful hub of Epic Universe. The theming is extraordinary throughout: every land feels like a separate world. Don't rush; the atmosphere and details are half the experience.",
              details: [
                '🌌 Celestial Park is the central hub — gorgeous stargazing theming',
                '🎠 Carousel of Progress-style slower rides and shows throughout the park',
                '📸 The park is extraordinarily photogenic — every corner is a backdrop'
              ]
            }
          ],
          meals: [
            {
              type: '🍻 Lunch',
              name: 'The Helios Grand Hotel (Epic Universe)',
              description: 'The themed hotel restaurant inside Epic Universe serves elevated park food — burgers, flatbreads, and cocktails in a stunning early-20th-century European hotel setting.',
              meta: '💰 $$ · 📍 Inside Epic Universe, Celestial Park hub'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Universal CityWalk Nightcap',
              description: "After Epic Universe, wander over to Universal CityWalk for dinner or drinks. The Hard Rock Live, Bob Marley's, and The Cowfish (sushi-burger fusion) are all solid choices. CityWalk buzzes well into the evening.",
              details: [
                '🎸 Hard Rock Café: classic American burgers in rock memorabilia surroundings',
                '🐟 The Cowfish: wildly creative sushi-burger mashup menu',
                '🌮 Vivo Italian Kitchen: fresh pasta and cocktails with great atmosphere'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'The Cowfish Sushi Burger Bar',
              description: "Unique concept: hand-crafted burgers AND sushi rolls, plus \"burgushi\" — the mashup you didn't know you needed. Huge menu, craft cocktails, and one of Universal CityWalk's most popular spots.",
              meta: '💰 $$ · 📍 Universal CityWalk · No reservation needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.4503, lng: -81.4779, label: 'Universal Epic Universe', num: 1, cat: 'attraction', desc: "World's newest mega theme park — 5 immersive worlds" },
        { lat: 28.4503, lng: -81.4779, label: 'Super Nintendo World', num: 2, cat: 'attraction', desc: 'Mario Kart ride + interactive Bowser\'s Castle experiences' },
        { lat: 28.4503, lng: -81.4779, label: 'Wizarding World - Ministry of Magic', num: 3, cat: 'attraction', desc: '1920s Paris Harry Potter world with groundbreaking rides' },
        { lat: 28.4747, lng: -81.4679, label: 'Universal CityWalk', num: 4, cat: 'attraction', desc: 'Dining and nightlife hub between Universal parks' },
        { lat: 28.4745, lng: -81.4685, label: 'The Cowfish', num: 5, cat: 'food', desc: 'Sushi + burger mashup — craft cocktails, wild menu' }
      ]
    },
    {
      num: 3,
      date: '2026-03-01',
      neighborhoods: 'Disney\'s Magic Kingdom · Disney\'s Hollywood Studios',
      title: 'Disney Magic & Cinematic Adventures',
      description: "Walt Disney World turns the imagination dial to eleven. Start your Disney day at Magic Kingdom — the most visited theme park on Earth — for classic rides, Cinderella's Castle, and evening fireworks that genuinely take your breath away. If you have energy, hop to Hollywood Studios for Millennium Falcon and Star Wars: Galaxy's Edge.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Magic Kingdom Rope Drop',
              description: "Arrive before the gates open. Hit Tomorrowland first for Space Mountain and TRON Lightcycle Run (the park's newest and fastest coaster), then double back to Fantasyland. The morning light on Cinderella's Castle is genuinely magical.",
              details: [
                '🚀 TRON Lightcycle Run: newest attraction, book Lightning Lane early',
                '🎢 Space Mountain: classic dark ride through the cosmos',
                '🏰 Cinderella\'s Castle: beautiful inside and out — walk through the mosaic hall',
                '🎡 Seven Dwarfs Mine Train: smooth family coaster with charming theming'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'The Plaza Restaurant',
              description: "Victorian-era charm inside Magic Kingdom, right on Main Street USA. Classic American breakfast with views down Main Street toward the castle. A quintessential Disney morning.",
              meta: '💰 $$ · 📍 Main Street USA, Magic Kingdom · Reservations via My Disney Experience app'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Adventureland & Liberty Square',
              description: "After the big thrill rides, slow down in Adventureland. Pirates of the Caribbean is still one of the all-time great theme park rides. The Haunted Mansion in Liberty Square is another timeless classic. Take photos in front of the castle and enjoy the quintessential Disney atmosphere.",
              details: [
                '🏴‍☠️ Pirates of the Caribbean: the original — timeless and still brilliant',
                '👻 Haunted Mansion: atmospheric and cleverly designed',
                '🌴 Jungle Cruise: corny jokes and animatronic animals — a classic',
                '🎠 Take the Walt Disney World Railroad around the park perimeter'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Park hop to Hollywood Studios for the afternoon if you can — Star Wars: Galaxy's Edge (Millennium Falcon: Smugglers Run + Rise of the Resistance) is a must for adventure-lovers and is only 15 minutes away via Disney transport." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Magic Kingdom Fireworks: Happily Ever After',
              description: "Stay for the evening fireworks show — it's one of the most spectacular displays you'll ever see, and it's included in your park ticket. Find a spot on Main Street USA or near the castle hub 30 minutes before showtime. This is the defining Orlando memory.",
              details: [
                '🎆 \"Happily Ever After\" fireworks: nightly, check Disney app for exact time',
                '📍 Best view: Hub in front of the castle, or Main Street USA for the full framing',
                '🍦 Get a Dole Whip from Adventureland before the show'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'California Grill',
              description: "Perched atop Disney's Contemporary Resort with floor-to-ceiling windows facing Magic Kingdom. Watch the fireworks from your table — the restaurant dims the lights and plays the park audio during the show. A magical, unmissable dinner.",
              meta: '💰 $$$$ · 📍 Disney\'s Contemporary Resort · Book 60 days in advance on My Disney Experience'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.4177, lng: -81.5812, label: 'Magic Kingdom', num: 1, cat: 'attraction', desc: 'The most visited theme park on Earth — castle, fireworks, classics' },
        { lat: 28.4156, lng: -81.5791, label: 'California Grill', num: 2, cat: 'food', desc: 'Rooftop dining at Contemporary Resort with fireworks view' },
        { lat: 28.3575, lng: -81.5588, label: "Disney's Hollywood Studios", num: 3, cat: 'attraction', desc: "Star Wars Galaxy's Edge, Millennium Falcon & Tower of Terror" },
        { lat: 28.3747, lng: -81.5494, label: 'EPCOT', num: 4, cat: 'attraction', desc: 'World Showcase pavilions and Guardians of the Galaxy coaster' },
        { lat: 28.3553, lng: -81.5898, label: "Disney's Animal Kingdom", num: 5, cat: 'attraction', desc: "Avatar Flight of Passage and Kilimanjaro Safari" }
      ]
    },
    {
      num: 4,
      date: '2026-03-02',
      neighborhoods: 'Discovery Cove · SeaWorld Area',
      title: 'Discovery Cove — Swim with Dolphins & Float the Day Away',
      description: "Discovery Cove is the most exclusive — and most unforgettable — experience in Orlando. A maximum of 1,000 guests per day access this all-inclusive paradise: a 30-minute dolphin swim in the lagoon, snorkeling through a tropical coral reef with thousands of fish, hand-feeding birds in a free-flight aviary, and unlimited food, drinks (including alcohol), and snorkel gear. This is your adventure + relaxation day rolled into one.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrival & Dolphin Swim Experience',
              description: "Arrive at opening (8am) to check in and get oriented. Your dolphin swim is assigned a timeslot — if it's in the morning, head straight to the Dolphin Lagoon. Trainers guide you through the interaction: belly rubs, a dorsal-fin ride, and a dolphin push (where the dolphin propels you by your feet). It's surreal and completely joyful.",
              details: [
                '🐬 30-minute guided dolphin interaction with a professional trainer',
                '🤿 Full wetsuit provided — the water is kept at a comfortable 77°F',
                '📸 Professional underwater photos available to purchase at the park',
                '⏰ Park opens 8am — arrive early for best dolphin time slot selection'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Discovery Cove (All-Inclusive)',
              description: "Continental breakfast included in your admission — fresh pastries, fruit, yogurt, and coffee at the Explorer's Aviary café area. Your entire day of food and beverages is included.",
              meta: '✅ Included · 📍 Discovery Cove · All meals, snacks & drinks included all day'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Grand Reef Snorkeling & Lazy River',
              description: "The Grand Reef at Discovery Cove is one of the most incredible snorkeling experiences outside of a natural ocean — thousands of tropical fish, rays, and sharks (behind safety glass) in a beautifully designed reef environment. Then hop on the Wind-Away River, a slow-moving lazy river that winds through jungle, waterfalls, and a massive tropical aviary.",
              details: [
                '🐠 Grand Reef: tropical fish, eagle rays, and nurse sharks in crystal water',
                '🦜 Freshwater Oasis: freshwater swim-through with otters and marmosets',
                '🌊 Wind-Away River: lazy float through jungle, waterfalls, and open aviary',
                '🌴 Serenity Bay: private beach area, lounge chairs, hammocks'
              ]
            },
            {
              title: 'Aviary & Serenity Bay',
              description: "The tropical aviary is a walk-through experience where hundreds of free-flying exotic birds land on your outstretched arm for feed. Then settle into Serenity Bay — a private beach with hammocks, lounge chairs, and waiter service. This is the \"relaxation\" half of the day.",
              details: [
                '🦜 Hand-feed tropical birds in the free-flight aviary',
                '🏖️ Serenity Bay has hammocks, lounge chairs, and beach access',
                '🍹 Unlimited beverages including beer and cocktails all day'
              ]
            }
          ],
          meals: [
            {
              type: '🍔 Lunch',
              name: 'Discovery Cove (All-Inclusive)',
              description: "Lunch is served buffet-style at Seafire Inn — grilled meats, fish, salads, pasta, and desserts. Fresh and plentiful. Grab cocktails and cold beer at the swim-up bar.",
              meta: '✅ Included · 📍 Seafire Inn, Discovery Cove'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Rest & Recovery',
              description: "After a day in the water and sun, you'll be gloriously tired. Head back to the hotel for a shower, an early evening rest, and a casual dinner nearby.",
              details: [
                '🛁 A shower and nap might be the best thing you\'ve ever done',
                '🌅 Discovery Cove closes at 5:30pm — plan accordingly'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Dinner',
              name: 'Tapa Toro',
              description: "Authentic Spanish tapas and a wood-burning paella bar right on International Drive. The live flamenco show turns dinner into an event. Order a pitcher of sangria and a selection of tapas — the garlic shrimp and croquetas are standouts.",
              meta: '💰 $$$ · 📍 ICON Park, International Drive · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.4091, lng: -81.4614, label: 'Discovery Cove', num: 1, cat: 'attraction', desc: 'All-inclusive dolphin swim paradise — max 1,000 guests/day' },
        { lat: 28.4091, lng: -81.4614, label: 'Grand Reef Snorkeling', num: 2, cat: 'attraction', desc: 'Tropical reef with thousands of fish and eagle rays' },
        { lat: 28.4091, lng: -81.4614, label: 'Wind-Away River', num: 3, cat: 'attraction', desc: 'Lazy river through jungle and free-flight aviary' },
        { lat: 28.4091, lng: -81.4614, label: 'Serenity Bay', num: 4, cat: 'attraction', desc: 'Private beach with hammocks and waiter service' },
        { lat: 28.4447, lng: -81.4668, label: 'Tapa Toro', num: 5, cat: 'food', desc: 'Spanish tapas + paella bar + live flamenco on I-Drive' }
      ]
    },
    {
      num: 5,
      date: '2026-03-03',
      neighborhoods: 'Kennedy Space Center · Cocoa Beach',
      title: 'To Infinity & Beyond — Kennedy Space Center & Cocoa Beach',
      description: "One hour east of Orlando lies one of America's most awe-inspiring destinations: the Kennedy Space Center. NASA's active launch facility lets you stand beneath Saturn V rockets, walk through mission control rooms, and see real spacecraft up close. Pair it with a stop at Cocoa Beach — your closest Atlantic Ocean beach — and you've got the perfect adventure day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kennedy Space Center Explorer',
              description: "Arrive at KSC at opening and head straight to the Saturn V Center — where you'll stand beneath the largest rocket ever built, hear recordings of mission controllers at the Apollo 8 launch, and see actual moon rocks. Then explore the Space Shuttle Atlantis pavilion (Atlantis is displayed in its re-entry configuration, just as it returned from space).",
              details: [
                '🚀 Saturn V rocket: 363 feet long, displayed horizontally in its own pavilion — scale is incomprehensible',
                '🛸 Space Shuttle Atlantis: the actual orbiter, tilted as if entering the atmosphere',
                '👨‍🚀 Astronaut Encounter: daily talk with a real NASA astronaut — schedule on arrival',
                '🔭 Heroes & Legends pavilion: Mercury, Gemini, and Apollo astronaut history'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Grab & Go from Hotel',
              description: 'Early start for the drive east — grab coffee and pastries from your hotel or a Dunkin\' on US-528. You want to arrive at KSC by 9am.',
              meta: '💰 $ · Grab from hotel before the drive'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cocoa Beach & Atlantic Ocean',
              description: "After KSC, drive 15 minutes to Cocoa Beach — the closest Atlantic Ocean beach to Orlando. Ron Jon Surf Shop is a landmark (open 24/7, the largest surf shop in the world). The beach itself is wide, uncrowded in late February, and perfect for a walk along the shore.",
              details: [
                '🏄 Ron Jon Surf Shop: 52,000 sq ft, open 24/7 — an experience in itself',
                '🌊 Cocoa Beach: calm Atlantic waves, good for swimming in late February',
                '🦀 The beach area is known for fresh seafood restaurants'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Lunch',
              name: 'Coconuts on the Beach',
              description: "Right on the Atlantic with outdoor tables on the sand. Fresh seafood — grouper sandwiches, shrimp baskets, fish tacos — with your feet in the sand and waves in view. Exactly what a Florida beach lunch should be.",
              meta: '💰 $$ · 📍 Cocoa Beach, A1A · Outdoor beach seating'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Drive Back & Relax',
              description: "The drive back to Orlando is about an hour. Stop at a Publix or Total Wine on the way back and grab supplies for a relaxed evening in. You've had two very active days — tonight is for room service, a movie, and recharging.",
              details: [
                '🛒 Publix Supermarket on the way back for snacks and drinks',
                '🛁 Hotel pool or hot tub — perfect way to end a KSC day',
                '🍕 Order pizza to the room: Pizza Hut or local delivery'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Downtown Credo (Winter Park)',
              description: "On the drive back, detour 10 minutes to the charming city of Winter Park for dinner at one of Orlando's best neighborhoods. The Ravenous Pig — a beloved James Beard-nominated gastropub — is a local institution with superb craft cocktails and creative American food.",
              meta: '💰 $$$ · 📍 Winter Park, FL (detour off I-4) · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.5234, lng: -80.6810, label: 'Kennedy Space Center', num: 1, cat: 'attraction', desc: 'NASA\'s active launch facility — Saturn V, Space Shuttle Atlantis' },
        { lat: 28.5234, lng: -80.6810, label: 'Saturn V Center', num: 2, cat: 'attraction', desc: 'Stand beneath the world\'s largest rocket in its own pavilion' },
        { lat: 28.5234, lng: -80.6810, label: 'Space Shuttle Atlantis', num: 3, cat: 'attraction', desc: 'The actual orbiter, displayed as if returning from space' },
        { lat: 28.3200, lng: -80.6082, label: 'Cocoa Beach', num: 4, cat: 'attraction', desc: 'Closest Atlantic beach to Orlando — wide, uncrowded in Feb' },
        { lat: 28.3200, lng: -80.6082, label: 'Coconuts on the Beach', num: 5, cat: 'food', desc: 'Fresh Florida seafood with Atlantic Ocean views' },
        { lat: 28.5989, lng: -81.3579, label: 'The Ravenous Pig (Winter Park)', num: 6, cat: 'food', desc: 'James Beard-nominated gastropub with craft cocktails' }
      ]
    },
    {
      num: 6,
      date: '2026-03-04',
      neighborhoods: 'Wekiwa Springs · Winter Park',
      title: 'Wild Florida — Kayaking Crystal Springs & Charming Winter Park',
      description: "Today is pure Florida magic — the kind most tourists never find. Wekiwa Springs State Park sits just 30 minutes north of downtown Orlando, where crystal-clear 68°F water bubbles up from underground springs and flows through a pristine wilderness teeming with manatees, ospreys, and alligators. After paddling the jungle river, wind down in Winter Park: a stunning lakeside city with art museums, brick-lined streets, and the best dining scene in the Orlando area.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Wekiwa Springs Kayaking',
              description: "Rent a kayak or canoe at Wekiwa Springs State Park and paddle the 16-mile Wekiva River. The water is crystal clear and a constant 68°F — you can see the sandy bottom even in deep sections. In late February, manatees shelter here in the warm spring water. Keep an eye out for otters, herons, ospreys, and the occasional alligator on the banks.",
              details: [
                '🛶 Canoe Wekiva rents kayaks and canoes right at the park',
                '🦦 Wildlife: manatees, river otters, osprey, great blue herons, gators on banks',
                '🌡️ Spring water stays 68°F year-round — refreshing but not cold',
                '⏰ Morning is the best time: calm water, wildlife active, cool air'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'The Toasted — College Park',
              description: "A beloved local breakfast spot (multiple Orlando locations) serving loaded eggs Benedict, creative pancakes, and excellent cold brew. Fuel up before the paddle.",
              meta: '💰 $$ · 📍 College Park, Orlando (on the way to Wekiwa)'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Winter Park — Park Avenue & Morse Museum',
              description: "Drive from Wekiwa to Winter Park (30 minutes). Park Avenue is one of Florida's most beautiful streets: brick sidewalks, leafy oaks, boutiques, art galleries, and café terraces overlooking a series of interconnected lakes. The Charles Hosmer Morse Museum of American Art houses the world's most comprehensive collection of Louis Comfort Tiffany art.",
              details: [
                '🏛️ Morse Museum: extraordinary Tiffany glass collection — chapel interior is breathtaking',
                '🛍️ Park Avenue: boutique shopping, gallery hopping, art browsing',
                '⛵ Scenic Boat Tours: narrated 1-hour pontoon tour of Winter Park\'s connected lakes',
                '🌳 Central Park, Winter Park: a lovely green strip along Park Avenue'
              ]
            }
          ],
          meals: [
            {
              type: '🍝 Lunch',
              name: 'Prato',
              description: "Beloved Italian restaurant on Park Avenue with wood-fired pizzas, handmade pastas, and a superb Negroni. The covered outdoor terrace is the perfect Winter Park lunch setting — elegant but not stuffy.",
              meta: '💰 $$$ · 📍 124 N Park Ave, Winter Park · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Winter Park Lakes',
              description: "Walk along the lakefront at Lake Osceola or take the Winter Park Scenic Boat Tour (last tour departs around 4pm). The sunset light on the cypress-lined lakes is stunning. Then settle in for dinner on Park Avenue before heading back.",
              details: [
                '⛵ Scenic Boat Tours: $16/person, 1-hour narrated tour through 7 lakes',
                '🌅 Sunset walk along Lake Osceola waterfront — beautiful golden light',
                '🍹 Pre-dinner cocktails at The Ritz-Carlton Winter Park terrace'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'The Ravenous Pig',
              description: "If you didn't make it last night, tonight is the night for Winter Park's most celebrated restaurant. The menu is creative American with hyper-local ingredients: pork belly with peach gastrique, Florida fish, and cocktails that rival the best bars in Miami. James Beard-nominated for good reason.",
              meta: '💰 $$$ · 📍 565 W Fairbanks Ave, Winter Park · Reservations required'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.7171, lng: -81.4626, label: 'Wekiwa Springs State Park', num: 1, cat: 'attraction', desc: 'Crystal-clear 68°F springs with manatees and wildlife kayaking' },
        { lat: 28.6717, lng: -81.4234, label: 'Wekiva River Paddling', num: 2, cat: 'attraction', desc: '16-mile jungle river — crystal water, alligators, otters, herons' },
        { lat: 28.5990, lng: -81.3537, label: 'Winter Park, FL', num: 3, cat: 'attraction', desc: 'Stunning lakeside city with art, dining, and Park Avenue charm' },
        { lat: 28.5999, lng: -81.3548, label: 'Morse Museum of Art', num: 4, cat: 'attraction', desc: "World's finest Tiffany glass collection — chapel interior" },
        { lat: 28.5990, lng: -81.3537, label: 'Prato Restaurant', num: 5, cat: 'food', desc: 'Wood-fired Italian on Park Avenue — beloved local institution' },
        { lat: 28.5989, lng: -81.3579, label: 'The Ravenous Pig', num: 6, cat: 'food', desc: 'James Beard-nominated gastropub — best restaurant in Winter Park' }
      ]
    },
    {
      num: 7,
      date: '2026-03-05',
      neighborhoods: 'EPCOT · Disney Springs · International Drive',
      title: 'Final Day — EPCOT\'s World Showcase & Sweet Farewell',
      description: "Your last day deserves something special. EPCOT's World Showcase is essentially an international food and culture festival with 11 country pavilions — you can eat and drink your way around the world in a single afternoon. Ride the incredible Guardians of the Galaxy coaster in the morning, then take the afternoon slow: pastries in France, sake in Japan, fish & chips in England. End with a final dinner back on International Drive before heading to the airport.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'EPCOT — Guardians of the Galaxy & Future World',
              description: "Hit the Guardians of the Galaxy: Cosmic Rewind roller coaster first — it's the world's largest indoor reverse-launch coaster and uses a 'reverse omnicoaster' vehicle that rotates to face the screen. Truly mind-blowing. Then explore Journey of Water (a Moana walk-through), Test Track, and Soarin' Around the World in Future World.",
              details: [
                '🎢 Guardians of the Galaxy: Cosmic Rewind — book Lightning Lane in advance (sells out at 7am)',
                '🌍 Soarin\' Around the World: stunning hang-gliding simulation over global landmarks',
                '🚗 Test Track: design your own concept car and race it through a test circuit',
                '💧 Journey of Water: relaxing walk-through inspired by Moana — beautiful for photos'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Sunshine Seasons (EPCOT)',
              description: "The Land pavilion's cafeteria-style restaurant serves some of the freshest theme park food in Disney — ingredients grown in the park's greenhouse literally feet away. Yogurt parfaits, sandwiches, and excellent coffee.",
              meta: '💰 $$ · 📍 The Land Pavilion, EPCOT · Quick service, no reservation needed'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'World Showcase Eat & Drink Tour',
              description: "The World Showcase is EPCOT's crown jewel — 11 country pavilions circling a massive lagoon. Each pavilion has its own restaurants, street food, unique architecture, and live entertainment. Take a full lap sampling from each: croissants and wine in France, takoyaki and sake in Japan, pretzels and beer in Germany, fish & chips in the UK.",
              details: [
                '🥐 France: La Vie En Rose bakery — croissants and crème brûlée',
                '🍶 Japan: Katsura Grill — sake sampling and teriyaki',
                '🥨 Germany: Biergarten beer hall — enormous German buffet',
                '🐟 United Kingdom: Rose & Crown Pub — pints and fish & chips',
                '🌮 Mexico: La Cava del Tequila — tequila flights in a cave atmosphere'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'EPCOT Luminous Nighttime Spectacular',
              description: "EPCOT's new nighttime show \"Luminous the Symphony of Us\" lights up the World Showcase lagoon with fireworks, fountains, and projections across the water. It's a beautiful farewell to your Orlando trip.",
              details: [
                '🎆 \"Luminous\" show: fireworks + water projections on World Showcase Lagoon',
                '📍 Best views: International Gateway or the UK pavilion waterfront',
                '⏰ Check the Disney app for exact show time — usually 9pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Christini\'s Ristorante Italiano',
              description: "A true Orlando institution celebrating over 40 years. This formal Italian restaurant on International Drive is the city's quintessential celebration dinner: strolling violinist, classic Italian cuisine (the veal chop and handmade pasta are extraordinary), and romantic candlelit atmosphere. The perfect end to an epic trip.",
              meta: '💰 $$$$ · 📍 7600 Dr Phillips Blvd, Orlando · Reservations required'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 28.3747, lng: -81.5494, label: 'EPCOT', num: 1, cat: 'attraction', desc: 'Future World rides + World Showcase — 11 international pavilions' },
        { lat: 28.3740, lng: -81.5490, label: 'Guardians of the Galaxy Ride', num: 2, cat: 'attraction', desc: "World's largest indoor reverse-launch roller coaster" },
        { lat: 28.3725, lng: -81.5478, label: 'World Showcase Lagoon', num: 3, cat: 'attraction', desc: 'Luminous nighttime spectacular — fireworks over the water' },
        { lat: 28.3740, lng: -81.5503, label: 'La Cava del Tequila (Mexico)', num: 4, cat: 'food', desc: 'Tequila flights and margaritas in an underground cave atmosphere' },
        { lat: 28.4559, lng: -81.4578, label: "Christini's Ristorante Italiano", num: 5, cat: 'food', desc: '40-year Orlando institution — strolling violin, classic Italian farewell' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$120–180/night', midrange: '$200–350/night', luxury: '$400–700/night' },
    { category: 'Meals (per couple/day)', budget: '$60–100/day', midrange: '$100–200/day', luxury: '$200–400/day' },
    { category: 'Transport (rental car)', budget: '$40–60/day', midrange: '$60–100/day', luxury: '$100–200/day' },
    { category: 'Epic Universe (per person)', budget: '$139+', midrange: '$179+ w/ Express', luxury: '$250+ VIP' },
    { category: 'Disney (per person/day)', budget: '$109–129', midrange: '$149+ w/ Lightning Lane', luxury: '$250+ VIP' },
    { category: 'Discovery Cove (per person)', budget: '$199–299', midrange: '$299 w/ dolphin swim', luxury: '$449 Ultimate' },
    { category: 'Kennedy Space Center (per person)', budget: '$75', midrange: '$75 + tours', luxury: '$75 + astronaut training' },
    { category: '7-Day Total (couple)', budget: '$3,500–5,000', midrange: '$5,500–8,000', luxury: '$9,000–14,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Orlando International Airport (MCO) — major hub with direct flights from most US cities', 'Uber/Lyft from airport to I-Drive area: ~$25–40', 'Rental cars: pick up at MCO on arrival, drop off before your flight home'] },
    { title: '🏨 Where to Stay', items: ['International Drive: best location, near everything (Hyatt, Rosen, Hilton)', 'Disney Resort Hotels: on-site magic + free transport but expensive', 'Universal on-site Hotels: early park admission perk for Epic Universe', 'Disney Springs area: good value, Disney transport access without full resort prices'] },
    { title: '🌡️ Late February Weather', items: ['Average high 78°F (25°C), average low 57°F (14°C)', 'Mostly sunny with occasional afternoon showers', 'Comfortable theme park weather — no summer heat/humidity yet', 'Light jacket for evenings and heavily air-conditioned parks'] },
    { title: '💳 Money & Tickets', items: ['Buy all park tickets online in advance (Disney, Universal, Discovery Cove)', 'Lightning Lane (Disney) and Universal Express Pass are worth it for 1-day visits', 'Discovery Cove is all-inclusive — one ticket covers everything all day', 'Credit cards accepted everywhere — tap to pay widely supported'] },
    { title: '📱 Apps to Download', items: ['My Disney Experience: mobile ordering, Lightning Lane, wait times', 'Universal Orlando App: Express Pass, wait times, maps', 'Google Maps: essential for driving in the I-4 corridor'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
