const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771963420778_0c2uvp',
  email: 'kathryn.le@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-04-25',
  endDate: '2026-04-29',
  groupSize: 2,
  requests: ''
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo: Adventure, Flavor & Zen',
  subtitle: '4 days of street food crawls, hidden temples & electric neighborhoods for two',
  description: "Tokyo is a city of extraordinary contrasts — neon-drenched Shibuya sits minutes from the serene gardens of Meiji Shrine, Michelin-starred sushi bars share blocks with ¥500 ramen counters, and ancient temples hide behind futuristic skyscrapers. This late-April itinerary catches the tail end of cherry blossom season, weaves through Tokyo's most exciting neighborhoods, and balances thrilling urban exploration with moments of pure calm. Designed for two adventurous foodies who also know when to slow down.",
  duration: '4 nights',
  dates: 'Apr 25 – Apr 29, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Couples · Foodies · Adventurers',
  highlights: [
    'Tsukiji Outer Market street food crawl at dawn',
    'Shibuya Crossing & Harajuku backstreet exploration',
    'Meiji Shrine morning walk through the forest',
    'Golden Gai tiny bar hopping in Shinjuku',
    'Onsen soak at a traditional bathhouse',
    'Senso-ji Temple at sunrise before the crowds'
  ],

  essentials: [
    { title: '🌸 Late April Weather', text: 'Expect 15–22°C (60–72°F) with occasional rain. Late cherry blossoms may still cling to trees — check Shinjuku Gyoen and Ueno Park. Pack layers and a light rain jacket.' },
    { title: '🚇 Getting Around', text: 'Get a 72-hour Tokyo Subway Ticket (¥1,500/~$10) for unlimited metro rides. IC cards (Suica/Pasmo) work on everything else. Tokyo is incredibly walkable — many neighborhoods are best explored on foot.' },
    { title: '💴 Budget Tips', text: 'Tokyo is surprisingly affordable for food. Convenience stores (konbini) serve excellent onigiri and bento for ¥200-500. Standing sushi and ramen shops are ¥800-1,200. Department store basement food halls (depachika) are free-sample heaven.' },
    { title: '⚡ Golden Week Alert', text: 'April 29 is Showa Day — the start of Golden Week. Expect larger crowds at popular spots. Visit temples and shrines early morning. Book any restaurants in advance.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-25',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Old Tokyo — Temples, Parks & Electric Town',
      description: "Start with Tokyo's traditional heart. Senso-ji at dawn is transcendent — incense smoke, the massive red lantern, and almost no tourists. Then contrast with the anime-fueled chaos of Akihabara. This is Tokyo's split personality in one day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple at Sunrise',
              description: "Tokyo's oldest temple is magical before 8am. Walk through the iconic Kaminarimon gate, browse the Nakamise-dori shopping street as vendors set up, and watch locals pray at the main hall. The five-story pagoda glows in morning light.",
              details: [
                '⛩️ Kaminarimon (Thunder Gate) — the giant red lantern is Tokyo\'s most iconic image',
                '🕐 Arrive by 7am to beat tour groups',
                '🍘 Nakamise-dori has fresh senbei (rice crackers) and ningyo-yaki (filled cakes)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café',
              description: 'Legendary bakery in Asakusa since 1942. Their thick-cut toast with butter is a Tokyo institution. Simple, perfect, and deeply Japanese.',
              meta: '💰 $ · 📍 Asakusa · Opens 8am · Cash only'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Ameyoko Market',
              description: "Stroll through Ueno Park — if you're lucky, late cherry blossoms will still be hanging on. Then dive into Ameyoko, the raucous open-air market under the train tracks. Vendors shout over each other selling everything from fresh seafood to sneakers.",
              details: [
                '🌸 Ueno Park has 800+ cherry trees — some late-blooming varieties last into late April',
                '🐼 Tokyo National Museum is here if you want world-class Japanese art (¥1,000)',
                '🦐 Ameyoko fresh fruit stalls sell huge strawberry packs for ¥500'
              ]
            },
            {
              title: 'Akihabara Electric Town',
              description: "Walk south to Akihabara — Tokyo's anime, manga, and gaming district. Even if you're not an otaku, the sensory overload is an adventure. Multi-floor arcades, retro game shops, and maid cafés line the streets.",
              details: [
                '🕹️ Super Potato — legendary retro gaming shop across multiple floors',
                '🎮 Sega arcades have crane games, rhythm games, and photo booths',
                '📦 Don Quijote (Donki) — the chaotic discount store is an experience itself'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Ameyoko street food',
              description: 'Graze through Ameyoko market — grilled seafood skewers, fresh fruit, takoyaki (octopus balls), and kebabs. No single restaurant needed; the market IS the meal.',
              meta: '💰 $ · 📍 Under the JR tracks between Ueno & Okachimachi'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Asakusa Evening & Sumida River Walk',
              description: "Return to Asakusa for the evening. Senso-ji is beautifully illuminated at night with far fewer people. Walk along the Sumida River for views of Tokyo Skytree lit up against the night sky.",
              details: [
                '🌃 Senso-ji is open 24/7 — nighttime visits are atmospheric',
                '🗼 Asahi Beer Hall\'s golden flame sculpture is a fun photo op',
                '🌉 Sumida River promenade has benches with Skytree views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sometaro',
              description: 'A charming okonomiyaki (savory pancake) spot in a traditional wooden house. You cook your own pancakes on a griddle built into your table — fun, interactive, and delicious.',
              meta: '💰 $ · 📍 Asakusa · Cash preferred · Expect a short wait'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: "Tokyo's oldest temple — iconic Kaminarimon gate" },
        { lat: 35.7131, lng: 139.7970, label: 'Nakamise-dori', num: 2, cat: 'attraction', desc: 'Traditional shopping street leading to Senso-ji' },
        { lat: 35.7146, lng: 139.7966, label: 'Pelican Café', num: 3, cat: 'food', desc: 'Legendary bakery — thick-cut toast since 1942' },
        { lat: 35.7126, lng: 139.7740, label: 'Ueno Park', num: 4, cat: 'attraction', desc: 'Vast park with museums and cherry blossoms' },
        { lat: 35.7084, lng: 139.7745, label: 'Ameyoko Market', num: 5, cat: 'food', desc: 'Lively open-air market under the train tracks' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 6, cat: 'attraction', desc: 'Electric Town — anime, gaming, and tech paradise' },
        { lat: 35.7100, lng: 139.7969, label: 'Sometaro', num: 7, cat: 'food', desc: 'Cook-your-own okonomiyaki in a traditional house' }
      ]
    },
    {
      num: 2,
      date: '2026-04-26',
      neighborhoods: 'Harajuku · Shibuya · Shinjuku',
      title: 'Electric Tokyo — Fashion, Crossing & Nightlife',
      description: "Today is pure modern Tokyo energy. Start in the forested calm of Meiji Shrine, explode into Harajuku's backstreet fashion scene, witness the world's busiest intersection at Shibuya, and end the night bar-hopping through Golden Gai's impossibly tiny bars.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine Forest Walk',
              description: "Step through the massive torii gate and leave the city behind. The forested path to Meiji Shrine is a living meditation — towering trees filter the light, and the only sounds are birdsong and crunching gravel. The shrine itself honors Emperor Meiji and is beautifully understated.",
              details: [
                '⛩️ The 12m-tall torii gate at the entrance is made from 1,500-year-old cypress',
                '🌳 The forest was planted in 1920 with 100,000 donated trees from across Japan',
                '🎋 Write a wish on an ema (wooden plaque) and hang it at the shrine'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bills Omotesando',
              description: "The famous Australian café's Tokyo outpost. Their ricotta hotcakes are legendary — fluffy, creamy, and worth the hype. Great coffee too.",
              meta: '💰 $$ · 📍 Omotesando · Opens 8:30am · Expect a queue on weekends'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku Backstreets & Takeshita-dori',
              description: "Harajuku is Tokyo's fashion laboratory. Takeshita-dori is a narrow lane packed with wild fashion boutiques, crêpe stands, and rainbow cotton candy. But the real treasures are in the backstreets — Cat Street and the Ura-Hara lanes have vintage shops, independent designers, and hidden cafés.",
              details: [
                '🛍️ Cat Street — the cooler, calmer alternative to Takeshita-dori',
                '🍦 Marion Crêpes — the original Harajuku crêpe, iconic since the 70s',
                '👗 Ura-Harajuku backstreets for vintage and streetwear'
              ]
            },
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: "The world's busiest pedestrian crossing is mesmerizing — up to 3,000 people cross at once. Watch from the Starbucks above or walk it yourself. Then head up Shibuya Sky for a 360° observation deck 230m above the city.",
              details: [
                '📸 Mag\'s Park rooftop (free) gives a great elevated view of the crossing',
                '🏙️ Shibuya Sky tickets: ¥2,000 — book online to skip the line',
                '🐕 Hachiko statue outside Shibuya Station — pay respects to the loyal dog'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Fuunji',
              description: 'One of Tokyo\'s best tsukemen (dipping ramen) shops. Thick, rich fish-pork broth with firm noodles you dip yourself. The queue moves fast.',
              meta: '💰 $ · 📍 Near Shinjuku Station · Counter seating only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Golden Gai Bar Hopping',
              description: "Shinjuku's Golden Gai is a labyrinth of 200+ tiny bars crammed into six narrow alleys. Most seat only 6-8 people. Each has its own theme and personality — jazz bars, horror-themed bars, cinema bars, bars where the mama-san tells your fortune. This is nightlife you can't get anywhere else on Earth.",
              details: [
                '🍶 Many bars charge a small seating fee (¥500-1,000) — totally normal',
                '🚪 Look for bars with English signs or open doors if it\'s your first time',
                '🎵 Bar Albatross is a good starter — three floors, friendly, open to tourists',
                '🥃 Try Japanese whisky — Toki highball is refreshing and affordable'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Omoide Yokocho (Memory Lane)',
              description: "Also called Piss Alley (affectionately) — narrow lanes of tiny yakitori joints under the train tracks near Shinjuku Station. Smoke, sizzling meat, cold beer, and elbow-to-elbow seating. Utterly authentic.",
              meta: '💰 $ · 📍 West side of Shinjuku Station · Best after 6pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in a 100-year-old forest' },
        { lat: 35.6714, lng: 139.7025, label: 'Harajuku / Takeshita-dori', num: 2, cat: 'attraction', desc: "Tokyo's fashion and youth culture epicenter" },
        { lat: 35.6619, lng: 139.7041, label: 'Shibuya Crossing', num: 3, cat: 'attraction', desc: "World's busiest intersection — mesmerizing to watch" },
        { lat: 35.6584, lng: 139.7024, label: 'Shibuya Sky', num: 4, cat: 'attraction', desc: '230m observation deck with 360° city views' },
        { lat: 35.6938, lng: 139.7035, label: 'Fuunji', num: 5, cat: 'food', desc: "Tokyo's best tsukemen dipping ramen" },
        { lat: 35.6938, lng: 139.7040, label: 'Golden Gai', num: 6, cat: 'attraction', desc: '200+ tiny themed bars in narrow alleys' },
        { lat: 35.6935, lng: 139.6988, label: 'Omoide Yokocho', num: 7, cat: 'food', desc: 'Smoky yakitori alley under the train tracks' }
      ]
    },
    {
      num: 3,
      date: '2026-04-27',
      neighborhoods: 'Tsukiji · Ginza · Odaiba · Roppongi',
      title: 'Market Mornings, Bay Views & Art After Dark',
      description: "Dawn start at Tsukiji for the freshest seafood breakfast of your life, refined Ginza for window shopping and matcha, a futuristic detour to Odaiba on the bay, and world-class art at teamLab Borderless to close the day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market Food Crawl',
              description: "The inner wholesale market moved to Toyosu, but Tsukiji's outer market is still the beating heart of Tokyo's food scene. Over 400 stalls and shops serve the freshest seafood, tamagoyaki (rolled omelette), and street food. Arrive hungry.",
              details: [
                '🐟 Arrive by 7:30am — stalls start closing by early afternoon',
                '🍣 Get a tuna sashimi bowl or a single piece of otoro (fatty tuna) from a vendor',
                '🥚 Tsukiji Yamachou — watch them make tamagoyaki on long rectangular pans',
                '🍡 Japanese pickles, fresh wasabi, mochi — graze everything'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tsukiji Market Grazing',
              description: 'Skip a sit-down meal — the market IS breakfast. Fresh sashimi, grilled scallops on sticks, tamagoyaki, and melon pan from different stalls. Budget ¥2,000-3,000 for a feast.',
              meta: '💰 $ · 📍 Tsukiji Outer Market · Best 7:30-10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza Stroll & Matcha Break',
              description: "Tokyo's most upscale district. Even if you're not shopping at Chanel, the architecture and window displays are art. The side streets hide incredible kissaten (old-school Japanese coffee shops) and matcha specialists.",
              details: [
                '🍵 Ippodo Tea — Kyoto\'s finest tea house has a Ginza branch. Try the matcha tasting set.',
                '🏬 Ginza Six — stunning department store with a rooftop garden',
                '📸 On weekends, Chuo-dori becomes a pedestrian zone — lovely for strolling'
              ]
            },
            {
              title: 'Odaiba Waterfront',
              description: "Take the Yurikamome monorail over Rainbow Bridge to Odaiba — Tokyo's futuristic waterfront district. There's a small Statue of Liberty replica, sandy beach with city skyline views, and the massive Gundam statue.",
              details: [
                '🤖 Life-size Unicorn Gundam statue — 20m tall, it transforms on the hour',
                '🌉 Rainbow Bridge views back toward the city are stunning at sunset',
                '🛍️ DiverCity and Aqua City malls for shopping and food'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Ginza Kagari',
              description: 'Tiny ramen shop famous for its creamy chicken paitan (white broth) ramen. Rich, silky, and utterly addictive. Worth the queue.',
              meta: '💰 $ · 📍 Ginza · Counter seating · Usually a 20-30 min wait'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: "One of the most mind-blowing art experiences on Earth. Digital art installations flow between rooms without boundaries — waterfalls of light cascade over your body, flowers bloom and scatter at your feet, and entire universes unfold around you. Allow 2-3 hours to wander and get lost.",
              details: [
                '🎨 Book tickets online in advance — they sell out (¥3,800)',
                '👗 Wear light/white clothing — the projections look best on you',
                '📱 Photography allowed and encouraged — no flash',
                '⏰ Evening visits are less crowded and more atmospheric'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gonpachi Nishi-Azabu',
              description: "The restaurant that inspired the crazy fight scene in Kill Bill. Dramatic two-story interior with open kitchen. Great yakitori, soba, and sushi — and the atmosphere is electric.",
              meta: '💰 $$ · 📍 Nishi-Azabu · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: '400+ stalls — the ultimate Tokyo food crawl' },
        { lat: 35.6717, lng: 139.7649, label: 'Ginza', num: 2, cat: 'attraction', desc: "Tokyo's luxury shopping district with stunning architecture" },
        { lat: 35.6711, lng: 139.7654, label: 'Ginza Kagari', num: 3, cat: 'food', desc: 'Famous creamy chicken paitan ramen' },
        { lat: 35.6268, lng: 139.7753, label: 'Odaiba', num: 4, cat: 'attraction', desc: 'Futuristic waterfront with Gundam and Rainbow Bridge views' },
        { lat: 35.6595, lng: 139.7313, label: 'teamLab Borderless', num: 5, cat: 'attraction', desc: 'Immersive digital art museum — a must-visit' },
        { lat: 35.6577, lng: 139.7263, label: 'Gonpachi Nishi-Azabu', num: 6, cat: 'food', desc: 'The Kill Bill restaurant — yakitori and atmosphere' }
      ]
    },
    {
      num: 4,
      date: '2026-04-28',
      neighborhoods: 'Shimokitazawa · Shinjuku Gyoen · Yanaka',
      title: 'Hidden Tokyo — Vinyl, Gardens & Neighborhood Zen',
      description: "Your final full day is about the Tokyo most tourists miss. Start in bohemian Shimokitazawa with vintage shopping and specialty coffee, find peace in Shinjuku Gyoen's gardens, and end in Yanaka — a quiet neighborhood that feels like 1960s Tokyo. Finish with a proper onsen soak.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shimokitazawa — Vintage & Coffee Culture',
              description: "Tokyo's most bohemian neighborhood. Narrow lanes packed with vintage clothing shops, vinyl record stores, independent cafés, and live music venues. It has the energy of Brooklyn meets Kyoto. Perfect for wandering without a plan.",
              details: [
                '☕ Bear Pond Espresso — legendary single-origin espresso (the Angel Stain is famous)',
                '👕 Flamingo and Stick Out — curated vintage from ¥500',
                '🎵 Flash Disc Ranch — incredible vinyl selection for music lovers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bear Pond Espresso',
              description: "Tiny, perfectionist coffee shop run by a barista who trained in NYC. The espresso is world-class — rich, velvety, and worth the pilgrimage. Limited hours and small batches; that's the charm.",
              meta: '💰 $ · 📍 Shimokitazawa · Opens 10am · Cash only · No photos of barista'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "One of Tokyo's most beautiful green spaces — 58 hectares of Japanese, English, and French gardens. In late April, wisteria may be blooming and the greenery is lush. Find a quiet bench under the trees and just breathe. This is where Tokyo's pace finally slows to zero.",
              details: [
                '🌿 ¥500 entry · No alcohol allowed (keeps it peaceful)',
                '🌸 Late-blooming cherry trees (Kanzan variety) can last into late April',
                '🏯 The Japanese garden with its pond and tea house is the most peaceful section',
                '☕ There\'s a Starbucks inside the park with gorgeous garden views'
              ]
            },
            {
              title: 'Yanaka — Old Tokyo Neighborhood',
              description: "Take the train to Yanaka, a neighborhood that survived the war and feels frozen in time. Narrow lanes, old wooden houses, neighborhood cats everywhere, and Yanaka Ginza — a retro shopping street with local snacks and crafts.",
              details: [
                '🐱 Yanaka is famous for its cats — real and sculptural',
                '🍦 Yanaka Ginza shopping street for yakitori, menchi-katsu, and shaved ice',
                '🪦 Yanaka Cemetery — peaceful, atmospheric, with cherry trees'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Shinjuku Gyoen area soba',
              description: 'Simple handmade soba noodles at one of the small shops near the garden. Cold zaru soba with tempura is the perfect light lunch after a morning of walking.',
              meta: '💰 $ · 📍 Shinjuku Gyoen-mae area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Onsen Soak — Thermae-Yu Kabukicho',
              description: "End your Tokyo adventure with a proper Japanese onsen experience. Thermae-Yu in Kabukicho is a multi-floor hot spring complex with natural mineral water, saunas, and relaxation rooms. Melt away four days of walking.",
              details: [
                '♨️ ¥2,405 entry (weekday) — includes towels and yukata',
                '🧖 Multiple baths: indoor, outdoor, jet baths, cold plunge',
                '⏰ Open until late — go in the evening for a relaxing wind-down',
                '💡 Tattoo-friendly (unlike many traditional onsen)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Uoharu Shinjuku',
              description: "Superb izakaya serving creative Japanese small plates and sashimi sourced directly from Toyosu Market. Share plates of uni, grilled fish, and seasonal vegetables — it's the ideal farewell feast.",
              meta: '💰 $$ · 📍 Shinjuku · Reservations recommended · Great sake selection'
            }
          ],
          tips: [
            { type: 'tip', text: "Tomorrow is April 29 (Showa Day) — the first day of Golden Week. If you're heading to the airport, leave extra time as trains and roads will be busier than usual." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6614, lng: 139.6688, label: 'Shimokitazawa', num: 1, cat: 'attraction', desc: 'Bohemian neighborhood — vintage, vinyl, and coffee' },
        { lat: 35.6612, lng: 139.6691, label: 'Bear Pond Espresso', num: 2, cat: 'food', desc: 'World-class espresso in a tiny shop' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 3, cat: 'attraction', desc: '58-hectare garden oasis in the heart of Tokyo' },
        { lat: 35.7271, lng: 139.7671, label: 'Yanaka', num: 4, cat: 'attraction', desc: 'Retro neighborhood with cats, crafts, and old Tokyo charm' },
        { lat: 35.7260, lng: 139.7666, label: 'Yanaka Ginza', num: 5, cat: 'food', desc: 'Retro shopping street with local street food' },
        { lat: 35.6946, lng: 139.7029, label: 'Thermae-Yu Onsen', num: 6, cat: 'attraction', desc: 'Multi-floor hot spring complex in Kabukicho' },
        { lat: 35.6936, lng: 139.7046, label: 'Uoharu Shinjuku', num: 7, cat: 'food', desc: 'Creative izakaya with Toyosu-fresh sashimi' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$40–80/night', midrange: '$80–180/night', luxury: '$200–500/night' },
    { category: 'Meals (per couple)', budget: '$30–50/day', midrange: '$60–120/day', luxury: '$150–400/day' },
    { category: 'Transport', budget: '$10–15/day', midrange: '$15–30/day', luxury: '$50–100/day' },
    { category: 'Activities', budget: '$0–20/day', midrange: '$20–60/day', luxury: '$80–200/day' },
    { category: 'teamLab Borderless', budget: '$25pp', midrange: '$25pp', luxury: '$25pp' },
    { category: '4-Day Total (couple)', budget: '$500–800', midrange: '$900–1,800', luxury: '$2,500–5,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT): 60-90 min to central Tokyo by Narita Express (¥3,250) or budget Keisei Skyliner (¥2,520)', 'Haneda Airport (HND): 30 min to the city by monorail or Keikyu line — much more convenient', 'Pocket WiFi rental at the airport is essential (~$5/day)'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku — best hub for nightlife and transit access', 'Asakusa — traditional charm, quieter at night, near Senso-ji', 'Shibuya — modern, walkable, great for younger travelers', 'Budget: capsule hotels (¥3,000-5,000) or business hotels (¥6,000-10,000)'] },
    { title: '🌡️ Weather', items: ['Late April averages 15–22°C (60–72°F)', 'Occasional spring rain — carry a compact umbrella', 'Cherry blossoms mostly finished but late-bloomers may remain', 'April 29 is Showa Day (Golden Week begins) — expect crowds'] },
    { title: '💳 Money', items: ['Japan is still fairly cash-heavy — carry ¥10,000-20,000 at all times', '7-Eleven and Family Mart ATMs accept foreign cards reliably', 'IC card (Suica/Pasmo) works at konbini, vending machines, and trains', 'Tipping is NOT customary and may cause confusion'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at the airport (Global WiFi, iVideo)', 'eSIM options: Ubigi, Airalo — activate before landing', 'Free WiFi is spotty outside hotels — pocket WiFi is worth it', 'Download Google Maps offline and the Japan Transit app'] }
  ]
};

fulfillOrder(order, itineraryData);
