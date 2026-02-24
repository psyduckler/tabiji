const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771940830745_im1rit',
  email: 'galaxycats510@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-14',
  endDate: '2026-03-19',
  groupSize: '3-4',
  style: 'Adventure, Cultural, Relaxation, Family-friendly',
  dining: 'Casual throughout',
  budget: 'Surprise me',
  requests: 'Dad is vegetarian. DisneySea is a must. Shopping, city lights, scenic views, fun activities. Open to day trips outside Tokyo.'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo in Full Bloom — Family Adventure Edition',
  subtitle: '6 days of cherry blossoms, DisneySea magic, ancient temples & neon city lights for the whole crew',
  description: "Tokyo in mid-March is a once-in-a-lifetime spectacle — the city transforms as the first cherry blossoms open, casting pink-tinged light over everything from ancient shrine grounds to neon-lit canals. This itinerary is built around your group's wishlist: a full day at the legendary DisneySea, a scenic escape to Kamakura's giant Buddha, a vegetarian-friendly tour through Tokyo's best food spots, and enough shopping districts to keep everyone happy. Every restaurant pick either offers great vegetarian mains or is fully plant-based. Pace is family-friendly — mornings are never rushed.",
  duration: '5 nights',
  dates: 'Mar 14 – Mar 19, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Families & Groups',
  highlights: [
    'Full day at Tokyo DisneySea — with a pre-booked Sailing Day Buffet for vegetarian-friendly dining',
    'Early cherry blossoms at Shinjuku Gyoen and Ueno Park',
    'Day trip to Kamakura — Great Buddha, seaside temples & veg-friendly lunch',
    'Senso-ji Temple by morning light, then neon Shibuya at night',
    'Tokyo Skytree observation deck — glittering city from 450m up',
    'Harajuku & Takeshita Street, Akihabara, Shinjuku shopping'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Timing', text: 'Mid-March marks the start of sakura season in Tokyo. Expect early blooms — scattered flowers with "first opening" announcements typical around March 14–18. Full bloom usually arrives late March. Shinjuku Gyoen and Ueno Park have thousands of early-variety trees. It is still stunning even before peak.' },
    { title: '🎟️ DisneySea Tickets', text: 'Book Tokyo DisneySea tickets online in advance at tokyodisneyresort.jp — they sell out weeks ahead, especially on weekends. For vegetarian dining, pre-book the Sailing Day Buffet (reservation system opens online). The park is massive; arrive at opening (8:30am) and prioritize Journey to the Center of the Earth and Indiana Jones early.' },
    { title: '🚇 Getting Around', text: 'The Tokyo Metro and JR Yamanote Line connect everything. An IC card (Suica or Pasmo) loaded with cash works on all trains, buses, and even convenience stores. For the Kamakura day trip, the JR Pass covers the Yokosuka Line. Taxis are expensive but convenient for late nights.' },
    { title: '🥗 Vegetarian Tokyo', text: "Vegetarian options have exploded in Tokyo. Look for signs saying 'vegan', 'plant-based', or 'sai shoku'. Convenience stores (7-Eleven, FamilyMart) always have onigiri with vegetarian fillings. T's Tan Tan in Tokyo Station is a must-visit for vegan ramen. Every restaurant in this itinerary has solid vegetarian mains — no compromise needed." },
    { title: '💴 Money & Payments', text: 'Japan is still largely cash-friendly. Withdraw yen from 7-Eleven or Japan Post ATMs (international cards accepted). Most mid-range restaurants and shops also accept cards now. Budget ¥15,000–25,000 per person per day (about $100–170 USD) for a comfortable experience.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-14',
      neighborhoods: 'Shinjuku · Shibuya · Omoide Yokocho',
      title: 'Arrival Day — Neon Nights & First Impressions',
      description: "Touch down in Tokyo and let the city's electric energy hit you. After settling in, head straight for Shinjuku — a sensory overload of skyscrapers, glowing signboards, and narrow alleys crammed with yakitori smoke. Tonight is about first impressions and getting your Tokyo legs.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Get Your Bearings',
              description: "Most hotels in Shinjuku or Shibuya have check-in from 3pm. Drop your bags and take a first walk through the neighbourhood. Shinjuku station is the world's busiest — navigating it is its own adventure.",
              details: [
                '🏨 Stay in Shinjuku or Shibuya for central access to everything',
                '🗺️ Pick up a free tourist map at the hotel — Tokyo is large but well-signposted',
                '🛒 Stop at a konbini (convenience store) for snacks — 7-Eleven and FamilyMart are everywhere'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet-lagged? The best cure is natural light and walking. Head outside instead of napping — you\'ll sleep much better tonight and adjust faster.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kabukicho & Shinjuku Neon District Walk',
              description: "Stroll through Kabukicho — Tokyo's glittering entertainment district. The robot-themed towers, illuminated signboards, and packed izakaya lanes are pure sensory overload. Cross into Golden Gai: 200 tiny bars crammed into six narrow alleys, each seating 8–10 people.",
              details: [
                '📸 Best photo spot: the Kabukicho Tower at night with all the neon',
                '🏮 Omoide Yokocho (Memory Lane) — tiny smoky yakitori alley, atmospheric even just to walk through',
                '⚠️ Golden Gai bars may have cover charges (¥500–1,000) but you\'re paying for a one-of-a-kind experience'
              ]
            },
            {
              title: 'Tokyo Metropolitan Government Building Observation Deck',
              description: "Take the free elevator to the 45th floor of the Tokyo Metropolitan Government Building for a stunning panoramic view of the city at night. On clear days you can see Mt. Fuji at sunset.",
              details: [
                '🆓 Free admission — open until 10:30pm (check for closures on Mondays)',
                '🗻 Mt. Fuji visible from north observatory on clear evenings',
                '🌃 The city grid of lights stretching to the horizon is jaw-dropping'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'T\'s Tan Tan (Tokyo Station) — or Tosca Verde Shinjuku',
              description: 'T\'s Tan Tan inside Tokyo Station is one of Japan\'s most celebrated vegan ramen restaurants. Rich sesame-based broths, chewy noodles, and zero animal products. If you\'re already in Shinjuku, Tosca Verde is a brilliant Italian-Japanese vegetarian restaurant with a warm atmosphere.',
              meta: '💰 $$ · 🌱 Fully vegan/vegetarian · 📍 T\'s Tan Tan: JR Tokyo Station (Keiyo St. concourse) | Tosca Verde: Shinjuku 3-chome'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6917, label: 'Shinjuku Station', num: 1, cat: 'attraction', desc: 'World\'s busiest station — your hub for the trip' },
        { lat: 35.6940, lng: 139.7036, label: 'Kabukicho Entertainment District', num: 2, cat: 'attraction', desc: 'Tokyo\'s neon-lit entertainment hub — dazzling at night' },
        { lat: 35.6938, lng: 139.6960, label: 'Omoide Yokocho', num: 3, cat: 'attraction', desc: 'Atmospheric narrow alley with tiny smoky yakitori stalls' },
        { lat: 35.6896, lng: 139.6923, label: 'Golden Gai', num: 4, cat: 'attraction', desc: '200 tiny intimate bars in six narrow alleys' },
        { lat: 35.6896, lng: 139.6914, label: 'Tokyo Metropolitan Government Observatory', num: 5, cat: 'attraction', desc: 'Free 45th floor view — city lights to the horizon' },
        { lat: 35.6814, lng: 139.7671, label: 'T\'s Tan Tan Ramen', num: 6, cat: 'food', desc: 'Legendary vegan ramen in Tokyo Station — rich sesame broth' }
      ]
    },
    {
      num: 2,
      date: '2026-03-15',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Ancient Tokyo — Senso-ji, Ueno Park & Electric Town',
      description: "Start with Tokyo at its most ancient — Senso-ji Temple glowing in morning light before the crowds arrive. Catch the first cherry blossoms at Ueno Park. Then swing into Akihabara's hyper-modern world of electronics, anime, and gaming culture.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple at Dawn',
              description: "Arrive at Senso-ji by 7–8am to experience Tokyo's oldest temple before tour groups arrive. The Kaminarimon gate with its massive red lantern, the Nakamise shopping street, and the five-storey pagoda are extraordinary in early morning light. Look for street food vendors setting up.",
              details: [
                '🏮 Kaminarimon Gate — the iconic red lantern gate is the most photographed spot in Asakusa',
                '🎋 Draw an omikuji fortune slip (¥100) at the main hall',
                '🛍️ Nakamise Dori: souvenir street leading to the temple — picks up by 9am',
                '📸 Best angle: from Kaminarimon looking toward the pagoda in morning mist'
              ]
            },
            {
              title: 'Asakusa Neighbourhood Wander',
              description: "After the temple, explore the backstreets of Asakusa — a neighbourhood that still feels old Tokyo. Rickshaw pullers, traditional craft shops, and the Sumida River with Tokyo Skytree framed behind it.",
              details: [
                '🛶 Walk along the Sumida River for the iconic Skytree reflection photo',
                '🎎 Kappabashi Kitchenware Street (10 min walk) — famous for food models and unique cooking tools'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Daikokuya Tempura (vegetarian sets available) or Pelican Café',
              description: 'Daikokuya has been serving tempura and vegetable donburi in Asakusa since 1887. Order the vegetable tempura set — crispy, golden perfection. Alternatively, Pelican Café (nearby) is a beloved locals\' spot for thick toast and coffee.',
              meta: '💰 $ · 🌱 Vegetable tempura sets available · 📍 Asakusa 1-chome'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park — First Cherry Blossoms',
              description: "A short subway ride to Ueno Park — home to over 1,000 cherry trees lining the main promenade. In mid-March you'll catch the first blooms — scattered but magical. The park also hosts Ueno Zoo (great for families!), several world-class museums, and Shinobazu Pond covered in lotus.",
              details: [
                '🌸 Mid-March = early sakura — expect 10–30% bloom, still beautiful with fewer crowds',
                '🦁 Ueno Zoo — Japan\'s oldest zoo, kids love the giant pandas',
                '🏛️ Tokyo National Museum (¥1,000 admission) — world\'s largest collection of Japanese art',
                '🧺 Local families set up hanami (blossom viewing) picnics — join the festive atmosphere'
              ]
            },
            {
              title: 'Akihabara Electric Town',
              description: "Walk or take a train to Akihabara — Tokyo's electronics and anime district. Multi-storey shops stack manga, video games, figurines, retro electronics, and the latest tech. Even non-gamers are wide-eyed here.",
              details: [
                '🎮 Yodobashi Akiba — 9-storey electronics megastore',
                '🎌 Animate Akihabara — 8 floors of manga and anime goods',
                '🕹️ Super Potato — retro gaming paradise (vintage Famicom, Sega)',
                '🍱 Tsukumo Games has a vegetarian-friendly curry restaurant on the top floor'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Komaki Shokudo Akihabara',
              description: 'A beloved vegetarian shokudo (diner) in Akihabara serving set meals of brown rice, miso soup, and rotating seasonal vegetables. Wholesome, affordable, and quietly popular with locals.',
              meta: '💰 $ · 🌱 Fully vegetarian/vegan · 📍 Near Akihabara Station'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Skytree Observation Deck at Dusk',
              description: "Head to the Tokyo Skytree — the world's second-tallest structure at 634 metres. The Tembo Deck at 350m and Tembo Galleria at 450m offer 360-degree views of the Tokyo metropolis glowing as dusk falls. On a clear evening, Mt. Fuji appears on the horizon.",
              details: [
                '🎫 Book tickets online at tokyo-skytree.jp — queues are shorter',
                '🌅 Arrive 30 min before sunset for the sky colour show',
                '🗻 Mt. Fuji visible from the west side on clear days',
                '🛍️ Tokyo Solamachi shopping complex at the base — 300+ shops and restaurants'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Nagi Shokudo (Shibuya) or Soranoiro Ramen',
              description: 'Nagi Shokudo in Shibuya is a popular plant-based Japanese restaurant doing beautiful vegan ramen, curries, and seasonal specials. Warm, casual atmosphere. Alternatively, Soranoiro in Nagatacho was Japan\'s first vegan ramen restaurant.',
              meta: '💰 $$ · 🌱 Fully vegetarian-friendly · 📍 Shibuya / Nagatacho'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — iconic red Kaminarimon gate' },
        { lat: 35.7155, lng: 139.7961, label: 'Nakamise Shopping Street', num: 2, cat: 'attraction', desc: 'Traditional souvenir street leading to Senso-ji' },
        { lat: 35.7173, lng: 139.7745, label: 'Ueno Park', num: 3, cat: 'attraction', desc: '1,000 cherry trees — first blooms arrive mid-March' },
        { lat: 35.6993, lng: 139.7713, label: 'Akihabara Electric Town', num: 4, cat: 'attraction', desc: 'Electronics, anime, gaming — multi-storey sensory overload' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 5, cat: 'attraction', desc: '634m tower — stunning night views from 450m' },
        { lat: 35.7104, lng: 139.7935, label: 'Daikokuya Tempura', num: 6, cat: 'food', desc: 'Historic Asakusa tempura since 1887 — vegetable sets available' }
      ]
    },
    {
      num: 3,
      date: '2026-03-16',
      neighborhoods: 'Urayasu (DisneySea) · Tokyo Bay',
      title: 'Full Day at Tokyo DisneySea — The World\'s Best Theme Park',
      description: "Today is all about DisneySea — widely considered the world's most beautifully designed theme park. Unlike any other Disney park, it's structured around seven \"ports\" with an adult sophistication that makes it magical for all ages. Plan your day strategically and pre-book the Sailing Day Buffet for a proper vegetarian-friendly meal.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Arrive at Park Opening (8:30am)',
              description: "DisneySea opens at 8:30am and the first two hours are golden — short queues everywhere. Head immediately to Mediterranean Harbour, then straight to Mysterious Island for Journey to the Center of the Earth. This is the park's most thrilling ride and queues balloon to 90+ minutes by 10am.",
              details: [
                '🎢 Journey to the Center of the Earth — volcanic launch ride, absolute priority',
                '🎡 Indiana Jones Adventure: Temple of the Crystal Skull — second stop',
                '⚡ Use the Disney Premier Access app for skip-the-line purchases if needed',
                '🚢 Pick up your park map at the entrance and plan your route before going in'
              ]
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tower of Terror & Arabian Coast',
              description: "After the main thrill rides, make your way to American Waterfront for the Tower of Terror — then loop through Arabian Coast, one of the park's most exotic and photogenic areas. The Sindbad's Storybook Voyage is gentle and fun for all ages.",
              details: [
                '👻 Tower of Terror — randomised drop sequences make every ride different',
                '🧞 Sindbad\'s Storybook Voyage — beautiful, suitable for all ages',
                '🎭 Watch for character meet-and-greets in American Waterfront (rare Mickey/Minnie appearances)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sailing Day Buffet (Pre-booked)',
              description: 'This is the park\'s premier dining experience and the best option for your vegetarian dad. The buffet includes dedicated plant-based and vegetarian dishes alongside seafood and meat options. Pre-book at least 2 weeks ahead via the Tokyo Disney Resort app — tables disappear fast.',
              meta: '💰 $$$ · 🌱 Vegetarian buffet options clearly labelled · 📍 American Waterfront · MUST PRE-BOOK'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lost River Delta, Mermaid Lagoon & Port Discovery',
              description: "Spend the afternoon working through the remaining ports. Mermaid Lagoon has indoor attractions perfect if anyone needs a rest. 20,000 Leagues Under the Sea in Mysterious Island is atmospheric and unique. Toy Story Mania in American Waterfront is a crowd-pleaser for the whole family.",
              details: [
                '🌊 Mermaid Lagoon Theatre — beautiful undersea Broadway-style show',
                '🎯 Toy Story Mania — competitive shooting game, endlessly fun',
                '🦈 Nemo & Friends SeaRider in Port Discovery — gentle ride with gorgeous visuals',
                '🌋 20,000 Leagues Under the Sea — classic atmospheric submarine adventure'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'DisneySea at Night — Spectacular Finale',
              description: "DisneySea is even more magical after dark. The Mediterranean Harbour becomes enchanting as all the lights reflect on the water. Stay for the evening spectacular — a mix of projection mapping, fireworks (weather permitting), and live music around the harbour. Pure magic for the whole family.",
              details: [
                '🌙 Find a spot around Mediterranean Harbour 30 minutes before the evening show',
                '🎆 Fantasy Springs (new area opened 2024) has evening illumination',
                '📸 The Skytree is visible from outside the park — one last photo before heading back'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Snacks & Dinner',
              name: 'DisneySea Snacks Throughout the Day',
              description: 'Beyond Sailing Day Buffet, grab plant-based snacks throughout the park: gyoza at Miguel\'s El Dorado Cantina (ask for cheese-free), popcorn at the many carts (plain is vegan), Mickey-shaped waffles with fruit toppings, and gelato at Mediterranean Harbour.',
              meta: '💰 $ · 🌱 Popcorn, fruit waffles, gelato all vegan-friendly · Varies by location'
            }
          ],
          tips: [
            { type: 'tip', text: 'The park can run late (10pm on busy days). Pace yourselves — DisneySea rewards those who slow down to appreciate the incredible theming and atmosphere. Don\'t rush every ride; soak in the views too.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6267, lng: 139.8842, label: 'Tokyo DisneySea', num: 1, cat: 'attraction', desc: 'The world\'s most beautifully designed theme park — full day here' },
        { lat: 35.6267, lng: 139.8842, label: 'Mediterranean Harbour', num: 2, cat: 'attraction', desc: 'Heart of the park — evening show location' },
        { lat: 35.6267, lng: 139.8842, label: 'Mysterious Island', num: 3, cat: 'attraction', desc: 'Journey to the Center of the Earth — go here first!' },
        { lat: 35.6267, lng: 139.8842, label: 'Sailing Day Buffet', num: 4, cat: 'food', desc: 'Best vegetarian-friendly dining in the park — pre-book!' },
        { lat: 35.6267, lng: 139.8842, label: 'American Waterfront', num: 5, cat: 'attraction', desc: 'Tower of Terror + Toy Story Mania hub' },
        { lat: 35.6267, lng: 139.8842, label: 'Fantasy Springs', num: 6, cat: 'attraction', desc: 'Newest area — opened 2024, beautiful at night' }
      ]
    },
    {
      num: 4,
      date: '2026-03-17',
      neighborhoods: 'Kamakura (Day Trip) · Hase · Yuigahama Beach',
      title: 'Kamakura Day Trip — Giant Buddha, Seaside Temples & Sea Air',
      description: "Take the 60-minute JR train south of Tokyo to Kamakura — a coastal city that served as Japan's medieval capital. The Great Buddha stands 13 metres tall against a forested hillside, surrounded by ancient zen temples. Finish with feet in the sand at Yuigahama Beach as the sun sinks into Sagami Bay.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Kamakura',
              description: "Catch the JR Yokosuka Line from Shinjuku or Tokyo Station — it runs directly to Kamakura Station. The ride takes about 55-65 minutes and passes through the outskirts of Yokohama. Arrive early before tour groups.",
              details: [
                '🚆 JR Yokosuka Line from Shinjuku: ~1 hour, no transfers needed',
                '💴 Round trip: ~¥1,900 per person (covered by JR Pass if you have one)',
                '⏰ Aim for the 8:00–9:00am departure to arrive by 9:30am'
              ]
            },
            {
              title: 'Kotoku-in — The Great Buddha (Kamakura Daibutsu)',
              description: "Walk 20 minutes (or take a local bus) from Kamakura Station to the Kotoku-in temple and come face-to-face with the Great Buddha. This 13.35m bronze Amida Buddha has stood here since 1252. You can enter the hollow statue for ¥50 extra. The setting — green hills, ancient stone lanterns — is sublime.",
              details: [
                '⛩️ Admission: ¥300 adults, ¥150 children',
                '📸 Morning light from the east hits the bronze beautifully',
                '🧘 The Buddha faces southwest — best photos from the front-left angle'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'GOOD MORNING KAMAKURA (café near station)',
              description: 'A beloved Kamakura café serving excellent Japanese breakfasts with vegetarian sets — rice, miso soup, pickles, and tamagoyaki (egg omelette). Simple, perfect, and local.',
              meta: '💰 $ · 🌱 Vegetarian breakfast sets · 📍 Near Kamakura Station'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hase-dera Temple',
              description: "One of the most beautiful temple complexes in all of Japan. The 9.18m gilded wooden Kannon statue is breathtaking. The hillside garden overlooks the ocean, and in mid-March there are early plum blossoms and spring flowers throughout. A peaceful, moving experience.",
              details: [
                '⛩️ Admission: ¥400',
                '🌺 Garden with panoramic ocean views from the upper terrace',
                '🪷 Thousands of small jizo statues (guardian deities) fill the caves',
                '📸 Sea view bench at the top — Sagami Bay stretching to the horizon'
              ]
            },
            {
              title: 'Komachi-dori Shopping Street',
              description: "Walk back through Kamakura's charming main shopping street for local snacks, crafts, and gifts. The street is lined with boutiques selling locally-made pottery, traditional sweets, and Kamakura-branded goods.",
              details: [
                '🍡 Mitarashi dango (rice dumplings) from street stalls — vegetarian',
                '🫖 Kamakura Beniya — beautiful Japanese confectionery',
                '🛍️ Pottery, wooden crafts, and silk goods make great souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🥢 Lunch',
              name: 'Hachi no Ki Restaurant (or Guesthouse & Café Oasis)',
              description: 'Hachi no Ki is famous for kaiseki-style vegetarian shojin ryori (Buddhist temple cuisine). A full set of multiple small vegetarian dishes — unique and deeply local. Book ahead or arrive at opening (11:30am). Guesthouse Oasis nearby is a simpler but excellent vegetarian café if Hachi no Ki is full.',
              meta: '💰 $$–$$$ · 🌱 Fully vegetarian Buddhist temple cuisine · 📍 Near Kita-Kamakura Station'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yuigahama Beach Sunset',
              description: "End the day at Yuigahama Beach — a wide sandy beach facing Sagami Bay. In the late afternoon the light turns golden and surfers paddle in the calm March swell. A rare moment of ocean calm before heading back to the city.",
              details: [
                '🌅 Sunset faces southwest — beautiful if skies are clear',
                '🏄 Local surfers in the water even in March (wetsuits on)',
                '🚆 Trains back to Tokyo run until midnight — no rush'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Back in Tokyo — T\'s Tan Tan or Ain Soph Journey Shinjuku',
              description: "After returning to Tokyo, refuel at Ain Soph Journey in Shinjuku — one of Tokyo's premier vegan restaurants serving innovative plant-based cuisine including fluffy pancakes, burgers, and Japanese-Western fusion dishes. Warm and family-friendly atmosphere.",
              meta: '💰 $$ · 🌱 Fully vegan restaurant · 📍 Shinjuku 3-chome'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3167, lng: 139.5500, label: 'Kamakura Station', num: 1, cat: 'attraction', desc: 'Base for the day — JR Yokosuka Line from Tokyo' },
        { lat: 35.3167, lng: 139.5359, label: 'Kotoku-in Great Buddha', num: 2, cat: 'attraction', desc: '13.35m bronze Amida Buddha — Japan\'s most iconic statue' },
        { lat: 35.3167, lng: 139.5365, label: 'Hase-dera Temple', num: 3, cat: 'attraction', desc: 'Golden Kannon statue + ocean views from hillside garden' },
        { lat: 35.3216, lng: 139.5537, label: 'Komachi-dori Shopping Street', num: 4, cat: 'attraction', desc: 'Kamakura\'s charming main street for snacks and crafts' },
        { lat: 35.3083, lng: 139.5416, label: 'Yuigahama Beach', num: 5, cat: 'attraction', desc: 'Sandy Pacific beach — perfect for sunset watching' },
        { lat: 35.3333, lng: 139.5483, label: 'Hachi no Ki Restaurant', num: 6, cat: 'food', desc: 'Buddhist vegetarian shojin ryori — exquisite set meals' }
      ]
    },
    {
      num: 5,
      date: '2026-03-18',
      neighborhoods: 'Shinjuku Gyoen · Harajuku · Shibuya · Meiji Shrine',
      title: 'Cherry Blossoms, Harajuku Fashion & Shibuya Crossing',
      description: "The ultimate Tokyo day: morning cherry blossoms in one of Japan's finest gardens, an afternoon of shopping from Harajuku's wild street fashion to Shibuya's international brands, and an evening at the world's most famous intersection. Cap it with city lights from Tokyo Tower.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine at Dawn',
              description: "Start at Meiji Shrine — a Shinto shrine set in 70 hectares of forested parkland, a surprising green sanctuary in the middle of the city. The long gravel path through towering cedar trees is serene even when busy. The shrine is dedicated to Emperor Meiji and Empress Shoken.",
              details: [
                '🌲 Meiji Jingu forest: 120,000 trees planted by volunteers in 1920',
                '⛩️ Free admission — opens at sunrise',
                '🪅 Watch the morning prayer ceremony if timing allows (weekday mornings)',
                '🍶 The inner garden (Iris Garden) is beautiful even before peak bloom — ¥500 entry'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "A 10-minute walk brings you to Shinjuku Gyoen — the best cherry blossom spot in Tokyo. This vast 58-hectare garden contains both Japanese and French-style gardens, greenhouses, and over 1,000 cherry trees of multiple varieties. The earliest varieties (kanhi-zakura, kawazu-zakura) are often in full bloom by mid-March.",
              details: [
                '🌸 Early varieties include Kawazu-zakura (full bloom early March) — larger pink flowers',
                '🎫 Admission: ¥500 per person — worth every yen',
                '📸 The French formal garden with sakura backdrop is stunning',
                '🥢 Bring a picnic — you can picnic on the lawns (no alcohol)',
                '⏰ Opens at 9am — arrive early for the best light and fewer people'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Viron Boulangerie (Shibuya) or Fuglen Tokyo (Yoyogi)',
              description: 'Viron near Shibuya Station has one of Tokyo\'s finest breakfast spreads — buttery croissants, jam, fresh juice, and good coffee. All pastries are vegetarian. Fuglen (a Norwegian café transplant in Yoyogi) serves outstanding single-origin coffee and vegetarian snacks in a gorgeous design space.',
              meta: '💰 $ · 🌱 All-vegetarian breakfast options · 📍 Shibuya or Yoyogi'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku — Takeshita Street & Omotesando',
              description: "A 10-minute walk from Meiji Shrine gets you to Harajuku. Takeshita Street is Tokyo's famous youth fashion corridor — wild, colourful, and packed with crepe stands, vintage shops, and fast fashion. For more refined shopping, Omotesando Avenue is Tokyo's Champs-Élysées lined with flagship stores from Chanel to Issey Miyake.",
              details: [
                '🎀 Takeshita Street: cotton candy, fairy kei fashion, vintage shops — pure chaos',
                '🏬 LaForet Harajuku — 8 floors of Japan\'s most interesting designers',
                '🌿 Omotesando Hills — spiral interior shopping complex, beautiful architecture',
                '🧁 Crepes at Marion Crepes — Harajuku\'s most famous crepe stand (fruit options are vegetarian)'
              ]
            },
            {
              title: 'Shibuya — Crossing, 109 & Cat Street',
              description: "Shibuya Scramble Crossing — the world's busiest pedestrian crossing. Up to 3,000 people cross at once. Watch from the Starbucks or Mag\'s Park terrace above for the overhead view. Then explore: Shibuya 109 for Japan-local fashion, and Cat Street for boutique vintage and designer streetwear.",
              details: [
                '📸 Best crossing photo: Starbucks Shibuya Tsutaya (second floor window, get there early) or Shibuya Sky rooftop deck',
                '🏬 Shibuya 109 — Japan\'s most famous youth fashion department store',
                '🛍️ Cat Street (Ura-Harajuku) — curated vintage and Japanese designer boutiques'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Plant Based Tokyo (Shibuya)',
              description: 'One of Tokyo\'s leading vegan restaurants in the heart of Shibuya. Japanese-fusion plant-based cuisine: tofu karaage, vegan sushi, seitan gyoza, and seasonal specials. Bright, modern interior — popular with both vegans and omnivores.',
              meta: '💰 $$ · 🌱 Fully plant-based restaurant · 📍 Shibuya 2-chome'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Tower Night View',
              description: "End the evening at Tokyo Tower — the city's beloved 333m red-and-white tower, built in 1958 and modelled after the Eiffel Tower. The Main Deck (150m) and Top Deck (250m) offer stunning views of the illuminated city grid. The tower itself is beautifully lit in orange-white every night.",
              details: [
                '🗼 Top Deck Tour: ¥3,000 adults, ¥2,000 children (includes Main Deck)',
                '🌙 Night views from 7–9pm are magical — city grid stretches to every horizon',
                '📸 Best exterior photo: from Shiba Park below, especially at blue hour',
                '🛍️ Foot Town (base of tower) has restaurants and shops'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Tenku no Niwa or a Soba Restaurant near Shiba Park',
              description: 'A soba specialist near Tokyo Tower is the perfect end-of-day meal. Traditional hand-cut buckwheat soba with vegetarian broths (cold dipping soba — "zaru soba" — is naturally vegetarian). Look for restaurants in Shiba and Azabu neighbourhoods near the tower.',
              meta: '💰 $$ · 🌱 Zaru soba and vegetable tempura soba are fully vegetarian · 📍 Shiba / Azabu area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6763, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in 70ha of forested parkland' },
        { lat: 35.6851, lng: 139.7101, label: 'Shinjuku Gyoen', num: 2, cat: 'attraction', desc: 'Best cherry blossom garden in Tokyo — 1,000+ sakura trees' },
        { lat: 35.6695, lng: 139.7025, label: 'Takeshita Street, Harajuku', num: 3, cat: 'attraction', desc: 'Tokyo\'s wild youth fashion street — crepes and cotton candy' },
        { lat: 35.6655, lng: 139.7057, label: 'Omotesando Avenue', num: 4, cat: 'attraction', desc: 'Tokyo\'s most fashionable boulevard with flagship boutiques' },
        { lat: 35.6595, lng: 139.7005, label: 'Shibuya Scramble Crossing', num: 5, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing — 3,000 people at once' },
        { lat: 35.6585, lng: 139.7454, label: 'Tokyo Tower', num: 6, cat: 'attraction', desc: '333m orange-white tower — iconic night views of the city' },
        { lat: 35.6607, lng: 139.6977, label: 'Plant Based Tokyo', num: 7, cat: 'food', desc: 'Excellent fully plant-based restaurant in Shibuya' }
      ]
    },
    {
      num: 6,
      date: '2026-03-19',
      neighborhoods: 'Tsukiji · Ginza · Odaiba · Departure',
      title: 'Final Morning — Tsukiji Market, Ginza & Goodbye Tokyo',
      description: "Your last morning in Tokyo starts at the legendary Tsukiji Outer Market for fresh sushi and street food (vegetarian options plentiful), a final stroll through elegant Ginza, and a peaceful send-off from Odaiba with views of the Rainbow Bridge before heading to the airport.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: "The Tsukiji Outer Market is one of Tokyo's greatest food experiences — a dense grid of stalls selling fresh seafood, produce, street food, and kitchen goods. For vegetarians there are tamago-yaki (sweet omelette on a stick), fresh fruit, taiyaki (fish-shaped bean paste cakes), and excellent coffee.",
              details: [
                '🥚 Tamagoyaki at Tsukiji Tamago: fluffy sweet omelette from the famous egg specialty stalls',
                '🐡 Taiyaki (bean paste cakes) — available everywhere, vegetarian',
                '🍓 Seasonal fruit skewers — perfect March strawberries',
                '⏰ Market runs from 5am but best from 7–9am for fresh produce and atmosphere'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Breakfast',
              name: 'Tsukiji Market Street Food (self-assembled)',
              description: 'Build your own breakfast from market stalls: tamagoyaki on a stick, pickled vegetables, miso soup from a stall, fresh strawberries, and strong drip coffee. The vegetarian-friendly options are abundant — just avoid the seafood stalls.',
              meta: '💰 $ · 🌱 Tamagoyaki, taiyaki, fruit, miso all vegetarian · 📍 Tsukiji Outer Market'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Ginza Window Shopping',
              description: "Walk north to Ginza — Tokyo's most exclusive shopping district. Even if you\'re not buying at Hermès, the architecture and window displays are worth seeing. Itoya (stationery store, 12 floors!) is a must for anyone who loves beautiful paper goods.",
              details: [
                '✒️ Itoya Ginza — 12-floor stationery paradise, Japanese pens and notebooks',
                '🏬 Ginza Six — high-end mall with rooftop garden open to the public',
                '☕ Café de l\'Ambre — legendary kissaten (old-style coffee shop) since 1948 (vegetarian-friendly)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Odaiba — Rainbow Bridge & Teamlab (Optional)',
              description: "If your flight is late afternoon or evening, Odaiba on Tokyo Bay is a perfect final stop. This futuristic artificial island has views of the Rainbow Bridge, a replica Statue of Liberty, and TeamLab Borderless (now in Azabudai Hills — digital art museum). It\'s a gentle, family-friendly afternoon.",
              details: [
                '🌉 Rainbow Bridge — best photographed from Odaiba Marine Park or the Yurikamome monorail',
                '🎨 TeamLab Borderless (Azabudai Hills) — one of the world\'s most extraordinary art experiences',
                '🚡 The Yurikamome elevated monorail to Odaiba has incredible bay views — choose a front seat',
                '⏰ Allow at least 3 hours before your departure if flying from Haneda (HND) — 30 min away'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Final Lunch',
              name: 'Ain Soph Ripple (Shinjuku) or Daigo (Azabu)',
              description: 'One last proper vegetarian meal. Ain Soph Ripple in Shinjuku does excellent plant-based burgers, soups, and their famous fluffy pancakes. If budget allows, Daigo near Azabudai Hills is a Michelin-starred shojin ryori restaurant serving stunning vegetarian kaiseki — a worthy final dining memory.',
              meta: '💰 $$–$$$$ · 🌱 Fully vegetarian options at both · 📍 Shinjuku or Azabu'
            }
          ],
          tips: [
            { type: 'tip', text: 'Narita Airport (NRT) is 60-75 minutes from central Tokyo by Narita Express. Haneda Airport (HND) is only 30-40 minutes. Check your terminal carefully — Narita has three separate buildings. Allow extra time for international security and immigration.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6655, lng: 139.7702, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Tokyo\'s legendary food market — street food breakfast' },
        { lat: 35.6717, lng: 139.7645, label: 'Ginza Shopping District', num: 2, cat: 'attraction', desc: 'Tokyo\'s most elegant shopping district — Itoya stationery is a must' },
        { lat: 35.6260, lng: 139.7752, label: 'Odaiba Marine Park', num: 3, cat: 'attraction', desc: 'Artificial bay island — Rainbow Bridge views and final farewell' },
        { lat: 35.6592, lng: 139.7594, label: 'TeamLab Borderless (Azabudai Hills)', num: 4, cat: 'attraction', desc: 'Immersive digital art museum — unforgettable family experience' },
        { lat: 35.6673, lng: 139.7540, label: 'Ginza Six Rooftop Garden', num: 5, cat: 'attraction', desc: 'Free rooftop garden above Ginza\'s most beautiful mall' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (3-4 pax)', budget: '¥20,000–35,000/night', midrange: '¥35,000–60,000/night', luxury: '¥70,000–150,000/night' },
    { category: 'Meals (per person/day)', budget: '¥2,000–3,000', midrange: '¥4,000–8,000', luxury: '¥10,000–30,000' },
    { category: 'DisneySea (per person)', budget: '¥9,900', midrange: '¥9,900 + ¥3,000 dining', luxury: '¥9,900 + Premier Access' },
    { category: 'Transport (daily)', budget: '¥800–1,500/person', midrange: '¥1,500–3,000/person', luxury: '¥5,000+ (taxis)' },
    { category: 'Activities & Entry', budget: '¥1,000–2,000/day', midrange: '¥3,000–6,000/day', luxury: '¥8,000+/day' },
    { category: '6-Day Total (group of 4)', budget: '¥300,000–400,000', midrange: '¥500,000–700,000', luxury: '¥900,000+' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Tokyo has two airports: Narita (NRT) and Haneda (HND)', 'Haneda is closer (30-40 min to city by monorail or train)', 'Narita Express (N\'EX) to Shinjuku/Shibuya: ~60-75 min, ¥3,070', 'Book transport to hotel before you land — especially with luggage'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku: most central for transport, restaurants, nightlife', 'Shibuya: trendy, excellent for shopping and youth culture', 'Asakusa: traditional atmosphere, walking distance to Senso-ji', 'Budget option: Khaosan Tokyo hostel chain (private rooms available)', 'Luxury: Park Hyatt Tokyo (Lost in Translation hotel), Andaz Shinjuku, The Tokyo Edition Toranomon'] },
    { title: '🌡️ March Weather', items: ['Average temperatures: 8–14°C (46–57°F) — cool but pleasant', 'Light jacket/sweater essential for evenings', 'Cherry blossom season means busier parks and higher hotel rates', 'Rain is possible — pack a compact umbrella (or buy a ¥300 konbini one)'] },
    { title: '🗣️ Language Tips', items: ['Google Translate with camera mode reads Japanese menus instantly', 'Most major tourist areas have English signage', 'Download the Google Maps Tokyo offline map before you go', '"Sumimasen" (excuse me) goes a long way', 'Convenience store staff will understand "vegetarian" + show ingredient lists'] },
    { title: '📱 Connectivity', items: ['Pocket WiFi rental from the airport is seamless (return at airport on departure)', 'Data-only SIM from airports (IIJmio, Sakura Mobile)', 'Japan Maps (offline capable) is better than Google Maps for train routing', 'Hyperdia app for train times and fares'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
