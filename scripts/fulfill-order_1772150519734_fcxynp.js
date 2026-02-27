const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772150519734_fcxynp',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: '5+',
  requests: 'Group of 5 includes toddlers ages 3 and 2'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo with Tiny Explorers',
  subtitle: '10 days of family adventure, street food & cultural wonder — designed for toddlers ages 2 & 3',
  description: "Tokyo is secretly one of the best cities in the world for families with small children. Spotless streets, stroller-friendly train stations with elevators everywhere, kid-welcoming restaurants, and a culture that genuinely adores little ones. This itinerary balances iconic cultural sites with toddler-speed exploration — built-in nap breaks, play parks between temples, family-friendly conveyor-belt sushi, and enough sensory wonder to keep tiny humans (and their grown-ups) delighted every single day. Late May means perfect weather: warm but not yet rainy season, cherry blossom season's crowds are gone, and the city is lush and green.",
  duration: '9 nights',
  dates: 'May 15 – May 24, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Families with Toddlers',
  highlights: [
    'teamLab Borderless — toddlers lose their minds in the light rooms',
    'Shinjuku Gyoen — wide open lawns perfect for little legs',
    'Conveyor belt sushi — the ultimate toddler dining experience',
    'Ueno Zoo & nearby playgrounds — pandas and puddles',
    'Tokyo Disneyland — Fantasyland is made for this age',
    'Senso-ji Temple — colorful, exciting, stroller-friendly',
    'Odaiba beach & giant Gundam — space to run free',
    'Meiji Shrine forest walk — peaceful stroller stroll'
  ],

  essentials: [
    { title: '👶 Toddler Travel Tips', text: 'Tokyo is incredibly child-friendly. Most train stations have elevators (look for ♿ signs). Convenience stores (konbini) everywhere stock diapers, baby food, wet wipes, and drinks. Department store basements (depachika) have free sample tastings that toddlers love.' },
    { title: '🚇 Getting Around', text: 'Get a Suica or Pasmo IC card for tap-on transit. Kids under 6 ride FREE on trains and buses. Strollers fold for crowded rush-hour trains (avoid 7:30-9am). Most stations have elevators — use the station map apps to find them. Taxis are plentiful and car seats aren\'t legally required.' },
    { title: '🌤️ May Weather', text: 'Late May averages 20-25°C (68-77°F) — ideal. Rain is possible but rainy season (tsuyu) typically starts in early June. Pack a light rain jacket and layers for air-conditioned spaces. UV is moderate — sunscreen for the kids.' },
    { title: '🍜 Eating with Kids', text: 'Japanese restaurants love children. Family restaurants (ファミレス) like Gusto and Saizeriya have kids\' menus, high chairs, and play areas. Conveyor belt sushi (kaitenzushi) is perfect for toddlers — they choose what looks fun. Konbini onigiri and bento boxes are cheap, healthy, and toddler-approved.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Shinjuku · Hotel Area',
      title: 'Arrival Day — Settle In & Shinjuku Stroll',
      description: "Land in Tokyo, get to your hotel, and ease into the city at toddler pace. Shinjuku has wide sidewalks, a gorgeous park, and plenty of easy dining options to recover from the flight without overwhelming little ones.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Airport Transfer & Hotel Check-In',
              description: 'Take the Narita Express (N\'EX) or Limousine Bus to Shinjuku. Both are stroller-friendly with luggage space. Settle into your hotel and let the kids decompress.',
              details: [
                '✈️ Narita Express: ~80 min, reserved seats, luggage racks',
                '🚌 Limousine Bus: ~90 min, no transfers, stroller stays in luggage bay',
                '🏨 Shinjuku or Shibuya area hotels are ideal home bases for families — central, tons of restaurants, easy train access'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag with toddlers is real. Don\'t plan anything ambitious today. Let them nap, explore the hotel, and find a nearby konbini for snacks and supplies.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Evening Walk & Dinner',
              description: 'Take a gentle walk through Shinjuku\'s neon-lit streets. Toddlers are mesmerized by the lights and sounds. Head to a family-friendly restaurant for your first Japanese meal.',
              details: [
                '🌃 Shinjuku\'s east side is flatter and easier with strollers',
                '🎮 Toddlers love looking at the claw machines in game centers (no need to play, just window shop!)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Katsukura Tonkatsu (Shinjuku Takashimaya)',
              description: 'Crispy tonkatsu (breaded pork cutlets) that toddlers devour. High chairs available, and kids can help grind their own sesame seeds — a fun activity that buys you 5 minutes of peace.',
              meta: '💰 $$ · 📍 Takashimaya Times Square, 14F · Kid-friendly'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6917, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Major hub — Narita Express terminal' },
        { lat: 35.6871, lng: 139.7003, label: 'Takashimaya Times Square', num: 2, cat: 'food', desc: 'Department store with family restaurants on upper floors' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Shinjuku Gyoen · Harajuku · Meiji Shrine',
      title: 'Parks, Shrine Forest & Crêpes',
      description: "Start your Tokyo adventure gently with wide-open green spaces. Shinjuku Gyoen is a toddler paradise of lawns and ponds, Meiji Shrine's forest path is stroller-perfect, and Harajuku's crêpe shops will make everyone happy.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'One of Tokyo\'s most beautiful parks — 144 acres of manicured gardens, wide lawns, and a greenhouse. Toddlers can run free on the massive English Landscape Garden lawn while you sit on a bench and breathe.',
              details: [
                '🌳 Enter from Shinjuku Gate (closest to station, elevator access)',
                '🦆 The Japanese Garden pond has koi fish and turtles — toddler magnets',
                '🌺 The greenhouse is warm, colorful, and fascinating for little ones',
                '💴 ¥500 adults, free for kids under 6 · No alcohol, no ball games'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Park-side Konbini Picnic',
              description: 'Grab onigiri, sandwiches, and juice boxes from a 7-Eleven or Lawson near the park entrance. Eat on the lawn — the most relaxed breakfast you\'ll have all trip.',
              meta: '💰 $ · 📍 Any konbini near Shinjuku Gyoen-mae Station'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'Walk through the towering torii gate into a peaceful forest in the middle of Tokyo. The wide gravel path through the trees is stroller-friendly (use big wheels or carry toddlers for the last stretch). The shrine itself is serene and beautiful.',
              details: [
                '⛩️ The approach path is 700m through old-growth forest — magical',
                '🍃 Toddlers love the giant torii gates and the gravel path',
                '🎋 Write a wish on an ema (wooden plaque) — kids can draw on theirs',
                '♿ Main path is wide and mostly flat; gravel can be tricky for small stroller wheels'
              ]
            },
            {
              title: 'Harajuku Takeshita Street & Crêpes',
              description: 'Walk from Meiji Shrine to Harajuku for colorful crêpes and people-watching. Takeshita Street is narrow and crowded — consider the quieter back streets (Cat Street / Ura-Hara) with strollers.',
              details: [
                '🍦 Marion Crêpes or Angels Heart — classic Harajuku crêpes',
                '🛒 Daiso (100-yen shop) on Takeshita Street — cheap toys and stickers for the kids',
                '👶 Cat Street (parallel to Takeshita) is wider and calmer for strollers'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Build in nap time after lunch. Head back to the hotel or find a quiet café. Toddler meltdowns in Tokyo are no fun for anyone — prevention beats cure.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Genki Sushi (Shibuya)',
              description: 'Conveyor belt sushi where you order on a tablet and plates zoom to your table on a little train. Toddlers are absolutely hypnotized. Affordable, fast, and the most entertaining dinner in Tokyo.',
              meta: '💰 $$ · 📍 Shibuya area · High chairs available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '144-acre garden with wide lawns — toddler paradise' },
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 2, cat: 'attraction', desc: 'Serene shrine in a forested park — stroller-friendly path' },
        { lat: 35.6702, lng: 139.7027, label: 'Harajuku / Takeshita Street', num: 3, cat: 'attraction', desc: 'Colorful crêpes, 100-yen shops, and people-watching' },
        { lat: 35.6619, lng: 139.7041, label: 'Genki Sushi Shibuya', num: 4, cat: 'food', desc: 'Conveyor belt sushi with tablet ordering — kids love it' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Asakusa · Sumida · Skytree',
      title: 'Senso-ji, River Cruise & Skytree',
      description: "Explore Tokyo's most photogenic temple, cruise down the Sumida River (toddlers love boats), and see the city from 450 meters up at Tokyo Skytree. A perfect mix of culture, transport-as-entertainment, and wow-factor views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise Shopping Street',
              description: 'Tokyo\'s oldest temple is also its most exciting for kids. The giant red lantern at Kaminarimon Gate, the colorful Nakamise shopping street full of snacks and toys, and the incense-filled temple courtyard create a sensory feast.',
              details: [
                '🏮 Arrive by 9am to beat crowds — Nakamise shops open at 9-10am',
                '🍘 Try ningyo-yaki (custard-filled cakes) and senbei (rice crackers) from stalls',
                '👶 Stroller-friendly throughout — wide paths, flat ground',
                '💨 Let toddlers wave incense smoke over themselves at the main hall (it\'s said to bring good health!)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Asakusa street food stalls',
              description: 'Grab melon pan (sweet bread), taiyaki (fish-shaped cake with filling), and green tea from the stalls around Senso-ji. Eating while exploring is half the fun.',
              meta: '💰 $ · 📍 Along Nakamise-dori and surrounding streets'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sumida River Cruise to Odaiba (or Hinode)',
              description: 'Board a Tokyo Cruise water bus from Asakusa pier. The futuristic Himiko/Hotaluna boats look like spaceships — toddlers go wild. Cruise down the Sumida River past bridges and the Rainbow Bridge.',
              details: [
                '🚢 Asakusa → Hinode Pier: ~40 min · Strollers can stay unfolded',
                '🤖 The Himiko boat has a spaceship interior — book this one if you can',
                '🌊 Sit on the open deck for best views (weather permitting)'
              ]
            },
            {
              title: 'Tokyo Skytree',
              description: 'At 634m, Skytree is the tallest tower in the world. The observation deck at 350m has floor-to-glass windows that toddlers can peer through. The Solamachi shopping complex at the base has a great aquarium and food court.',
              details: [
                '🗼 Book tickets online to skip the line — worth it with kids',
                '🐠 Sumida Aquarium (inside Solamachi) is excellent for toddlers — jellyfish tanks and penguins',
                '🛒 Solamachi has a floor of character shops (Ghibli, Pokémon, etc.)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Sumida Aquarium inside Skytree Solamachi is a perfect rainy-day backup or nap-time alternative. Small, beautiful, and toddler-paced.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sometaro Okonomiyaki (Asakusa)',
              description: 'Cook-your-own okonomiyaki (savory pancakes) on a hot plate at your table. Interactive dining that keeps toddlers fascinated. The traditional tatami room setting is charming.',
              meta: '💰 $$ · 📍 2-2-2 Nishi-Asakusa · Tatami seating (shoes off)'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest and most colorful temple' },
        { lat: 35.7120, lng: 139.7976, label: 'Nakamise Shopping Street', num: 2, cat: 'attraction', desc: 'Traditional snack and souvenir street leading to Senso-ji' },
        { lat: 35.7100, lng: 139.7966, label: 'Asakusa River Cruise Pier', num: 3, cat: 'transport', desc: 'Departure point for Sumida River water bus' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 4, cat: 'attraction', desc: 'World\'s tallest tower — 350m observation deck' },
        { lat: 35.7115, lng: 139.7956, label: 'Sometaro', num: 5, cat: 'food', desc: 'DIY okonomiyaki in a traditional setting' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Ueno · Yanaka',
      title: 'Zoo, Museums & Old Tokyo Charm',
      description: "Ueno is Tokyo's family headquarters — a massive park with a zoo, museums, playgrounds, and a lake with paddle boats. Spend the whole day here without rushing. Wander into nearby Yanaka for a taste of old-school Tokyo.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ueno Zoo',
              description: 'Japan\'s oldest zoo is home to giant pandas, elephants, gorillas, and a petting zoo. It\'s compact enough to cover in a morning without exhausting little legs. The petting area (Children\'s Zoo) lets toddlers touch goats, rabbits, and guinea pigs.',
              details: [
                '🐼 Giant pandas Xiao Xiao and Lei Lei — arrive early for shorter queues',
                '🐐 Children\'s Zoo petting area — goats, bunnies, guinea pigs',
                '♿ Mostly stroller-friendly; a few hilly sections in the western garden',
                '💴 ¥600 adults, free under 12 · Open 9:30am (closed Mondays)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park Exploration',
              description: 'After the zoo, explore the rest of Ueno Park. Rent a swan paddle boat on Shinobazu Pond (toddlers love steering), visit the playground near the fountain, or just let the kids run on the wide paths.',
              details: [
                '🦢 Swan boats on Shinobazu Pond: ~¥700/30min — toddler favorite',
                '🛝 Playground near the central fountain — slides and climbing structures',
                '🏛️ National Museum of Nature and Science has a dinosaur hall (if kids are into dinos)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Ueno Park Starbucks or Ameyoko Food Stalls',
              description: 'Grab lunch at the park Starbucks with outdoor seating, or walk to nearby Ameyoko market street for grilled skewers, fresh fruit, and chocolate-covered strawberries.',
              meta: '💰 $–$$ · 📍 Ueno Park area'
            }
          ],
          tips: [
            { type: 'tip', text: 'Ueno Park has clean restrooms with baby-changing stations throughout. The zoo also has nursing rooms.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yanaka Ginza — Old Tokyo Shopping Street',
              description: 'A 10-minute walk from Ueno, Yanaka Ginza is a charming retro shopping street that feels like 1960s Tokyo. Cat-themed everything, traditional snack shops, and a famous staircase (Yūyake Dandan) perfect for sunset photos.',
              details: [
                '🐱 Yanaka is Tokyo\'s cat town — spot real cats and cat-shaped everything',
                '🍡 Try menchi katsu (fried croquettes) from the street stalls',
                '🌅 Yūyake Dandan staircase faces west — gorgeous sunset spot'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Saizeriya (Family Restaurant)',
              description: 'Italian-Japanese family restaurant chain with incredibly cheap prices, kids\' meals, high chairs, drink bars, and zero judgment about noisy toddlers. Every Japanese family\'s go-to.',
              meta: '💰 $ · 📍 Multiple locations near Ueno · Kids\' menu available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7156, lng: 139.7714, label: 'Ueno Zoo', num: 1, cat: 'attraction', desc: 'Giant pandas, petting zoo — Japan\'s oldest zoo' },
        { lat: 35.7146, lng: 139.7744, label: 'Ueno Park', num: 2, cat: 'attraction', desc: 'Massive park with playgrounds, boats, and museums' },
        { lat: 35.7131, lng: 139.7709, label: 'Shinobazu Pond', num: 3, cat: 'attraction', desc: 'Swan paddle boats — toddler favorite' },
        { lat: 35.7271, lng: 139.7673, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Retro shopping street with cats and street food' },
        { lat: 35.7105, lng: 139.7746, label: 'Ameyoko Market', num: 5, cat: 'food', desc: 'Bustling market street with fresh fruit and snacks' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Maihama · Tokyo Disneyland',
      title: 'Tokyo Disneyland — Magic Kingdom Day',
      description: "The day the kids have been waiting for (even if they don't know it yet). Tokyo Disneyland's Fantasyland is purpose-built for toddlers — gentle rides, character meet-and-greets, parades, and pure magic. Go at toddler pace: ride, snack, nap, repeat.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fantasyland & Toontown',
              description: 'Head straight to Fantasyland when the park opens. It\'s a Small World, Dumbo the Flying Elephant, and the Pooh\'s Hunny Hunt ride are perfect for ages 2-3. Toontown has play areas where toddlers can climb, slide, and explore Minnie\'s house.',
              details: [
                '🏰 Arrive 30 min before park opening for the best start',
                '🎠 Best toddler rides: It\'s a Small World, Dumbo, Castle Carousel, Pooh\'s Hunny Hunt',
                '🏠 Toontown is a giant playground — let kids explore freely',
                '👶 Baby Center near Castle — nursing room, microwave, diapers for sale'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Parade, Character Greetings & Nap Break',
              description: 'Catch the daytime parade from a shady spot (claim your spot 30 min early). After the excitement, find a quiet bench or head to the Baby Center for a toddler nap. Stroller naps work great at Disney.',
              details: [
                '🎪 Daytime parade runs down the main route — watch from Fantasyland end for less crowds',
                '📸 Character greeting spots have organized, short lines — much better than other Disney parks',
                '😴 Stroller nap tip: park near Tom Sawyer Island area — quieter zone'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Queen of Hearts Banquet Hall',
              description: 'Alice in Wonderland-themed buffeteria in Fantasyland. Toddlers love the whimsical decor, and the food is solid (curry, pasta, chicken). No reservation needed.',
              meta: '💰 $$ · 📍 Fantasyland · High chairs available'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tokyo Disneyland is the cleanest, most organized Disney park in the world. Cast members are incredibly helpful with families. Don\'t try to do everything — pick 5-6 rides and enjoy the atmosphere.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening Parade & Fireworks',
              description: 'If the toddlers have gas left in the tank, the evening electrical parade is spectacular. If they\'re done (no shame!), head out before closing to avoid the exit crush.',
              details: [
                '✨ Evening parade is dazzling — but late (usually 7:30-8pm)',
                '🚃 JR Maihama Station is a 5-min walk from the park entrance',
                '👶 Know when to call it — an overtired toddler beats any parade'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'In-park dining or Ikspiari Mall',
              description: 'Eat inside the park, or exit to Ikspiari (shopping mall next to the station) for more variety — ramen, udon, pizza, and family restaurants.',
              meta: '💰 $$  · 📍 Ikspiari Mall, Maihama Station'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6329, lng: 139.8804, label: 'Tokyo Disneyland', num: 1, cat: 'attraction', desc: 'Fantasyland & Toontown — toddler paradise' },
        { lat: 35.6340, lng: 139.8795, label: 'Fantasyland', num: 2, cat: 'attraction', desc: 'It\'s a Small World, Dumbo, Pooh\'s Hunny Hunt' },
        { lat: 35.6365, lng: 139.8802, label: 'Toontown', num: 3, cat: 'attraction', desc: 'Playground and character houses for little ones' },
        { lat: 35.6361, lng: 139.8854, label: 'Ikspiari Mall', num: 4, cat: 'food', desc: 'Restaurant mall next to Disneyland station' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Odaiba · Toyosu',
      title: 'Rest Day — Beach, Gundam & Science Fun',
      description: "After yesterday's Disney marathon, take it easy on the waterfront. Odaiba has a sandy beach for digging, a life-size Gundam statue, and interactive science museums. It's spacious, flat, and designed for families — the perfect recovery day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Odaiba Beach & Gundam Statue',
              description: 'Let the toddlers loose on Odaiba\'s sandy beach along Tokyo Bay. The water is shallow and calm (wading only), and there\'s a stunning view of Rainbow Bridge. Walk to the life-size Unicorn Gundam statue at DiverCity — even if you don\'t know Gundam, it\'s impressive.',
              details: [
                '🏖️ The beach is clean but not for swimming — perfect for sand castles',
                '🤖 Gundam statue is free to see — it transforms on a schedule (check times)',
                '👶 Wide, flat promenades everywhere — stroller heaven',
                '🚆 Take the Yurikamome monorail — toddlers love the driverless front seats'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: 'Immersive digital art that toddlers experience as pure magic. Rooms of flowing light, interactive flowers that bloom when you touch the walls, waterfalls of color, and floating lanterns. Toddlers don\'t need to "understand" art — they just experience the wonder.',
              details: [
                '🎨 Book tickets online in advance — sells out fast',
                '👟 Wear shoes you can take off (some mirror-floor rooms)',
                '👶 Strollers must be parked outside — baby carriers recommended',
                '⏱️ Allow 1.5-2 hours · Some dark rooms — hold toddler hands',
                '📍 Now at Azabudai Hills (moved from Odaiba)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'DiverCity Food Court',
              description: 'Huge food court with everything from ramen to takoyaki to kids\' curry plates. Easy, fast, and toddler-friendly with high chairs throughout.',
              meta: '💰 $–$$ · 📍 DiverCity Tokyo Plaza, Odaiba'
            }
          ],
          tips: [
            { type: 'tip', text: 'teamLab has moved to Azabudai Hills (Roppongi area), not Odaiba anymore. Visit Odaiba in the morning, then take the train to Azabudai Hills for the afternoon.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gonpachi (Nishi-Azabu) — "Kill Bill" Restaurant',
              description: 'The izakaya that inspired the fight scene in Kill Bill. Multiple floors with tatami rooms. Excellent soba, yakitori, and tempura. Kids love the bustling atmosphere.',
              meta: '💰 $$$ · 📍 1-13-11 Nishi-Azabu, Minato · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6250, lng: 139.7753, label: 'Odaiba Beach', num: 1, cat: 'attraction', desc: 'Sandy beach on Tokyo Bay — sand castles with a view' },
        { lat: 35.6252, lng: 139.7754, label: 'Unicorn Gundam Statue', num: 2, cat: 'attraction', desc: 'Life-size Gundam at DiverCity — free to see' },
        { lat: 35.6594, lng: 139.7313, label: 'teamLab Borderless', num: 3, cat: 'attraction', desc: 'Immersive digital art museum — toddlers love it' },
        { lat: 35.6253, lng: 139.7751, label: 'DiverCity Food Court', num: 4, cat: 'food', desc: 'Big food court with family-friendly options' },
        { lat: 35.6596, lng: 139.7277, label: 'Gonpachi', num: 5, cat: 'food', desc: 'The "Kill Bill" izakaya — soba, yakitori, atmosphere' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Shibuya · Shimokitazawa',
      title: 'Shibuya Crossing, Train Museums & Bohemian Village',
      description: "See the world's busiest intersection (from a safe, elevated spot), visit a train museum that toddlers will never want to leave, and explore the laid-back lanes of Shimokitazawa — Tokyo's most walkable bohemian neighborhood.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shibuya Crossing & Hachiko Statue',
              description: 'Watch the famous Shibuya Scramble from the Shibuya Sky observation deck or the Starbucks overlooking the intersection. Toddlers are fascinated by the wave of people. Say hello to the Hachiko dog statue.',
              details: [
                '🐕 Hachiko statue — tell the kids it\'s a real dog story',
                '📸 Starbucks 2F (Tsutaya building) has the classic crossing view',
                '🏙️ Shibuya Sky (rooftop) is amazing but might be too windy/scary for toddlers — use judgment'
              ]
            },
            {
              title: 'TEPCO Electric Energy Museum or Nearby Play',
              description: 'If kids need a break, the Shibuya area has several small parks. The Miyashita Park rooftop has a playground and Starbucks.',
              details: [
                '🛝 Miyashita Park rooftop playground — free, modern, great for toddlers',
                '☕ Starbucks on the rooftop while kids play — parent win'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shimokitazawa Exploration',
              description: 'Take the train two stops to Shimokitazawa — Tokyo\'s coziest neighborhood. Narrow car-free lanes, vintage shops, cozy cafés, and a village-like atmosphere that\'s perfect for a stroller stroll. Much calmer than central Shibuya.',
              details: [
                '🚶 Mostly pedestrian streets — no car stress with toddlers',
                '🎭 Quirky shops, vintage clothes, and tiny cafés',
                '🧸 Look for the used toy and children\'s clothing shops — great finds'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'City Country City (Shimokitazawa)',
              description: 'A cozy café above a used bookstore. Great coffee, curry rice, and a relaxed vibe. The stairs might require stroller folding, but the atmosphere is worth it.',
              meta: '💰 $$ · 📍 Shimokitazawa area'
            }
          ],
          tips: [
            { type: 'tip', text: 'Shimokitazawa recently got a new underground train station with elevators and a lovely park built on the old rail line (Shimokita Linear Park) — great for toddler scooting.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Uobei Sushi (Shibuya)',
              description: 'Ultra-fast conveyor sushi — order on a touchscreen and plates shoot to you on a three-lane express track. At ¥100-180/plate, it\'s cheap thrills. Toddlers are hypnotized by the plate delivery system.',
              meta: '💰 $ · 📍 Shibuya, near Dogenzaka · High chairs available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: 'World\'s busiest intersection — watch from above' },
        { lat: 35.6590, lng: 139.7005, label: 'Hachiko Statue', num: 2, cat: 'attraction', desc: 'Famous loyal dog statue — toddler photo op' },
        { lat: 35.6611, lng: 139.6998, label: 'Miyashita Park', num: 3, cat: 'attraction', desc: 'Rooftop playground and Starbucks — parent win' },
        { lat: 35.6612, lng: 139.6680, label: 'Shimokitazawa', num: 4, cat: 'attraction', desc: 'Bohemian village — car-free lanes and cozy cafés' },
        { lat: 35.6592, lng: 139.6987, label: 'Uobei Sushi', num: 5, cat: 'food', desc: 'Express-track sushi — plates zoom to your seat' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Akihabara · Nihonbashi · Imperial Palace',
      title: 'Trains, Toys & Imperial Gardens',
      description: "A day for the inner child in everyone. Akihabara's toy stores and game centers, the serene Imperial Palace gardens for toddler running, and Tokyo's best toy department store. Balance sensory overload with peaceful green spaces.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Akihabara — Toy & Character Shopping',
              description: 'Even if you\'re not into anime, Akihabara\'s toy stores are incredible for toddlers. Multiple floors of Pokémon, trains, stuffed animals, and building blocks. Yodobashi Camera\'s toy floor is enormous.',
              details: [
                '🧸 Yodobashi Akiba toy floor — massive selection of Tomica cars, Plarail trains',
                '🎮 Gachapon (capsule toy machines) are everywhere — ¥100-500 per turn, toddler crack',
                '🚂 Plarail (toy train) demo tables where kids can play — free',
                '📍 The main strip has elevators and is stroller-manageable'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Imperial Palace East Gardens',
              description: 'A free, beautifully maintained garden in the heart of Tokyo. Wide lawns, ancient stone walls, a moat with swans, and almost no crowds. Toddlers can run freely on the immaculate grass. Perfect for a post-lunch wind-down.',
              details: [
                '🏯 Enter through Ōte-mon gate — free admission, closed Mon & Fri',
                '🦢 Moat has swans and koi — toddler entertainment sorted',
                '🌳 Wide, flat paths perfect for strollers',
                '⏰ Open 9am-4:30pm (last entry 4pm)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Marunouchi Area Family Dining',
              description: 'The Marunouchi Brick Square or KITTE mall near Tokyo Station have excellent family restaurants with kids\' menus. Clean, modern, and spacious.',
              meta: '💰 $$ · 📍 Marunouchi, near Tokyo Station'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Station Character Street',
              description: 'Underground shopping street at Tokyo Station with official character stores — Pokémon Store, Ghibli shop, Tomica Shop, Plarail Shop, and more. Perfect for picking up souvenirs.',
              details: [
                '🛍️ Tokyo Character Street is in the Yaesu underground area',
                '🚂 Tomica & Plarail shops — train-obsessed toddlers will never leave',
                '🍪 Also has regional bento boxes and sweet shops — grab dinner here'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ramen Street (Tokyo Station)',
              description: 'Eight top ramen shops in one underground corridor. Kids love watching noodles being made. Most shops are small but accommodate children — ask for a kids\' portion (kodomo).',
              meta: '💰 $$ · 📍 Tokyo Station First Avenue, B1F'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6984, lng: 139.7714, label: 'Akihabara', num: 1, cat: 'attraction', desc: 'Toy stores and gachapon machines — toddler paradise' },
        { lat: 35.6867, lng: 139.7581, label: 'Imperial Palace East Gardens', num: 2, cat: 'attraction', desc: 'Free peaceful gardens with lawns for running' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 3, cat: 'attraction', desc: 'Character Street and Ramen Street underground' },
        { lat: 35.6819, lng: 139.7643, label: 'KITTE Mall', num: 4, cat: 'food', desc: 'Modern dining near Tokyo Station — family-friendly' },
        { lat: 35.6808, lng: 139.7669, label: 'Ramen Street', num: 5, cat: 'food', desc: 'Eight famous ramen shops underground at Tokyo Station' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Nakano · Kichijoji · Inokashira Park',
      title: 'Hidden Tokyo — Parks, Ponds & Ghibli Vibes',
      description: "Venture beyond the tourist trail to neighborhoods where Tokyo families actually spend their weekends. Inokashira Park is pure magic — paddle boats shaped like swans, a tiny zoo, and paths that feel like a Ghibli movie. Kichijoji's shopping streets are relaxed and family-perfect.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Inokashira Park',
              description: 'This park in Kichijoji is where Tokyo families go on weekends. A beautiful pond with swan paddle boats, a free mini zoo (with guinea pigs, squirrels, and deer), shaded walking paths, and a wonderfully relaxed atmosphere.',
              details: [
                '🦢 Swan boats on the pond — toddlers love steering (¥700/30min)',
                '🐿️ Inokashira Park Zoo — tiny, free-ish (¥400 adults), and perfect for toddlers',
                '🎭 Street performers on weekends near the pond',
                '🌿 Feels like walking into a Miyazaki film — lush and enchanting'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Café du Lièvre (Kichijoji)',
              description: 'French-inspired bakery café near the park. Excellent croissants, quiches, and fresh juice. Relaxed and child-welcoming.',
              meta: '💰 $$ · 📍 Near Kichijoji Station south exit'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kichijoji Sun Road & Harmonica Yokocho',
              description: 'Stroll through Kichijoji\'s covered Sun Road shopping street and the narrow Harmonica Yokocho alley. Grab snacks, browse toy shops, and soak in the local neighborhood vibe.',
              details: [
                '🎵 Harmonica Yokocho — charming narrow alleys with tiny shops and yakitori stalls',
                '🧸 Multiple small toy shops and children\'s clothing stores',
                '🍡 Street snacks: taiyaki, croquettes, melon pan'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Ghibli Museum in Mitaka (next station) requires advance tickets purchased months ahead. If you didn\'t pre-book, don\'t worry — Inokashira Park captures the same magical feeling.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Dinner Preparation',
              description: 'Head back to the hotel area for your last evening in Tokyo. Take it slow — maybe pick up treats from a depachika (department store basement food hall) for an in-room picnic dinner. Toddlers often prefer this to another restaurant.',
              details: [
                '🍱 Depachika highlights: bento boxes, fruit parfaits, wagashi sweets, gyoza',
                '🛒 Isetan Shinjuku or Takashimaya have incredible food halls'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Depachika Feast (Isetan Shinjuku)',
              description: 'Build your own gourmet dinner from the department store basement. Sushi, tempura, wagyu bento, fruit, pastries — all beautifully packaged. Eat in your hotel room while toddlers play in pajamas.',
              meta: '💰 $$–$$$ · 📍 Isetan Shinjuku B1F · Closes 8pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6997, lng: 139.5737, label: 'Inokashira Park', num: 1, cat: 'attraction', desc: 'Swan boats, mini zoo, and Ghibli-like atmosphere' },
        { lat: 35.7031, lng: 139.5794, label: 'Kichijoji Station', num: 2, cat: 'attraction', desc: 'Charming neighborhood — Sun Road and Harmonica Yokocho' },
        { lat: 35.7031, lng: 139.5797, label: 'Harmonica Yokocho', num: 3, cat: 'food', desc: 'Narrow alley with tiny yakitori stalls and bars' },
        { lat: 35.6919, lng: 139.7044, label: 'Isetan Shinjuku', num: 4, cat: 'food', desc: 'World-class depachika — gourmet takeaway feast' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Hotel Area · Airport',
      title: 'Sayonara Day — Last Bites & Departure',
      description: "Your final morning in Tokyo. Keep it simple — a relaxed breakfast, some last-minute souvenir shopping, and head to the airport with full hearts (and suitcases). Tokyo will miss you.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Relaxed Morning & Packing',
              description: 'Sleep in, let the toddlers play in the hotel room, and take your time packing. Check if your hotel offers late checkout — many Japanese hotels are accommodating for families.',
              details: [
                '📦 Yamato Transport (Ta-Q-Bin) can ship luggage to the airport for you — ask the hotel front desk',
                '🧳 Less luggage = easier toddler wrangling on the train'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Hotel Breakfast or Nearby Café',
              description: 'Enjoy a final Japanese breakfast — miso soup, rice, tamagoyaki, and pickles. Or keep it simple with pastries from the nearest konbini.',
              meta: '💰 $–$$ · 📍 Hotel or nearby'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Airport Transfer & Last Shopping',
              description: 'Head to Narita or Haneda. Both airports have excellent souvenir shops and kids\' play areas past security. Arrive early and let toddlers burn energy in the play zones.',
              details: [
                '✈️ Narita: take N\'EX from Shinjuku (~80 min)',
                '✈️ Haneda: take monorail or Keikyu line (~30-45 min from central Tokyo)',
                '🛍️ Airport souvenir picks: Tokyo Banana, KitKat flavors, Pocky sets',
                '🛝 Both airports have kids\' play areas near gates'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Buy a box of Tokyo Banana and assorted KitKat flavors at the airport — they make perfect souvenirs and are way cheaper than tourist shops in the city.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7647, lng: 140.3864, label: 'Narita Airport', num: 1, cat: 'transport', desc: 'Main international airport — souvenir shops and kids\' play areas' },
        { lat: 35.5494, lng: 139.7798, label: 'Haneda Airport', num: 2, cat: 'transport', desc: 'Closer to central Tokyo — domestic and international flights' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$100–180/night', midrange: '$200–400/night', luxury: '$400–800/night' },
    { category: 'Meals (family of 5)', budget: '$60–100/day', midrange: '$120–200/day', luxury: '$250–500/day' },
    { category: 'Transport', budget: '$15–30/day', midrange: '$30–60/day', luxury: '$80–150/day (private)' },
    { category: 'Activities', budget: '$0–30/day', midrange: '$40–100/day', luxury: '$100–250/day' },
    { category: 'Disneyland (family)', budget: '$350–450', midrange: '$450–600', luxury: '$600–900 (Premier)' },
    { category: '10-Day Total (family of 5)', budget: '$3,000–5,000', midrange: '$6,000–12,000', luxury: '$15,000–30,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT): ~80 min to central Tokyo by Narita Express', 'Haneda Airport (HND): ~30 min to central Tokyo — preferred for families', 'Pre-book airport transfers or take the Limousine Bus (easiest with strollers and luggage)'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku — central hub, tons of restaurants, easy train access', 'Shibuya — trendy, walkable, great for families who like energy', 'Ueno — near the zoo and park, slightly calmer, good value', 'Consider a family room or apartment-style hotel (Tokyu Stay, Mimaru) for extra space and kitchen access'] },
    { title: '🌡️ Weather (Late May)', items: ['Average 20-25°C (68-77°F) — warm and pleasant', 'Occasional rain showers — pack light jackets', 'Rainy season (tsuyu) usually starts early June, so you should be fine', 'UV is moderate — sunscreen for the kids'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless but carry some yen for temples, markets, and small shops', 'IC cards (Suica/Pasmo) work for trains, buses, konbini, and vending machines', 'Credit cards widely accepted at restaurants and shops', 'No tipping culture — zero tip everywhere'] },
    { title: '👶 Toddler Essentials', items: ['Diapers, wipes, baby food available at any konbini or drug store (Matsumoto Kiyoshi)', 'Most department stores have nursing rooms with hot water, changing tables, and vending machines', 'Baby carriers recommended for temples and crowded areas — strollers for everything else', 'Kids under 6 ride trains and buses free'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi or buy an eSIM at the airport', 'Google Maps works perfectly for train navigation', 'Download offline maps as backup', 'Free WiFi available at most konbini, stations, and hotels'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
