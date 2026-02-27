const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772142148210_layl1t',
  email: 'tom@kaeko.us',
  destination: 'Tokyo, Japan',
  startDate: '2026-04-28',
  endDate: '2026-05-02',
  groupSize: 2,
  requests: 'Vegetarians. Relaxed pace. Interested in TeamLab, Kamakura, Ghibli Museum, SkyTree, gardens, shrines, parks.'
};

const itineraryData = {
  destination: 'Tokyo & Kamakura, Japan',
  countryEmoji: '🇯🇵',
  title: 'Golden Week Gently: Tokyo & Kamakura for Two',
  subtitle: '5 days of temples, gardens, art & vegetarian feasts at a relaxed pace',
  description: "This itinerary is designed for two vegetarian travelers arriving from Europe and heading onward to Australia — meaning jet lag recovery and a gentle pace are built in from day one. You'll experience Tokyo's most magical corners during Golden Week: the immersive digital art of teamLab Borderless, the serene temples and Great Buddha of Kamakura, the wisteria wonderland of Ashikaga Flower Park, and the peaceful gardens of Shinjuku Gyoen and Meiji Shrine. Every restaurant is vegetarian-friendly, every day has breathing room, and the schedule respects your energy after long-haul flights.",
  duration: '4 nights',
  dates: 'Apr 28 – May 2, 2026',
  budget: '$',
  pace: 'Relaxed',
  bestFor: 'Couples · Vegetarians · Culture Lovers',
  highlights: [
    'teamLab Borderless — immersive digital art at Azabudai Hills',
    'Kamakura day trip — Great Buddha, Hase-dera Temple & seaside gardens',
    'Ashikaga Flower Park — cascading wisteria in peak bloom',
    'Shinjuku Gyoen — Tokyo\'s most beautiful garden in spring',
    'Meiji Shrine & Yoyogi Park — sacred forest in the heart of the city',
    'Tokyo SkyTree — panoramic views with a chance of Mt Fuji on the horizon'
  ],

  essentials: [
    { title: '🌸 Golden Week (Apr 29 – May 5)', text: 'You\'re visiting during Japan\'s biggest holiday week. Showa Day (Apr 29) kicks it off. Expect crowds at popular spots — we\'ve planned around this with early starts and quieter alternatives. Public transport runs normally but trains will be busier.' },
    { title: '🥬 Vegetarian Dining', text: 'Japan\'s Buddhist shojin ryori tradition means excellent vegetarian cuisine exists — but it\'s not always obvious. We\'ve selected restaurants with clear vegetarian menus. Helpful phrase: "Watashi wa bejitarian desu" (I am vegetarian). Watch for hidden dashi (fish stock) in soups — the places we\'ve chosen are safe.' },
    { title: '🚆 Getting Around', text: 'Get a Suica or Pasmo IC card at the airport for seamless train/bus travel. A 72-hour Tokyo Metro pass (¥1,500/~$10) is excellent value. For the Kamakura day trip, use JR trains from Shinjuku or Tokyo Station (~1 hour). Ashikaga is ~90 min by train.' },
    { title: '✈️ Jet Lag Strategy', text: 'Flying from Europe means you\'ll be 7-8 hours ahead. Day 1 is intentionally light — arrive, settle in, gentle evening walk. Resist napping past 3pm, get morning sunlight, and you\'ll adjust by Day 2.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-28',
      neighborhoods: 'Shinjuku · Shinjuku Gyoen',
      title: 'Arrival & Shinjuku Gyoen Gardens',
      description: "Arrive in Tokyo, drop your bags, and ease into Japan with a peaceful afternoon at Shinjuku Gyoen — one of Tokyo's most beautiful gardens. No rushing today. Let the jet lag settle with greenery, fresh air, and a gentle evening stroll through Shinjuku's atmospheric backstreets.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'One of Tokyo\'s finest gardens spanning 58 hectares with Japanese, English, and French landscape styles. In late April, the last cherry blossoms mingle with fresh green foliage and blooming azaleas. A perfect antidote to a long flight — find a bench by the pond, breathe, and let Tokyo reveal itself slowly.',
              details: [
                '🌿 Entry: ¥500 (~$3.50) — one of Tokyo\'s best bargains',
                '⏰ Open 9am–5:30pm (last entry 5pm), closed Mondays (but open during Golden Week)',
                '🍱 No alcohol allowed, but picnics are welcome — grab onigiri from a konbini',
                '📸 The Japanese Traditional Garden with its tea house overlooking the pond is the most peaceful spot'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'From Narita, take the Narita Express (NEX) to Shinjuku (~90 min, ¥3,250). From Haneda, the Keikyu Line or monorail is faster and cheaper. Store luggage at the hotel or station coin lockers before heading to the garden.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Backstreets & Golden Gai',
              description: 'As evening falls, wander through the neon-lit alleyways of Shinjuku. Peek into Golden Gai — a maze of 200+ tiny bars, each seating 5-8 people, crammed into six narrow alleys. You don\'t need to drink; just walking through is an experience. Then stroll through Omoide Yokocho (Memory Lane) for the atmospheric smoky alley vibes.',
              details: [
                '🏮 Golden Gai: many bars charge a ¥500-1,000 cover — check signs before entering',
                '📸 The neon reflections on wet streets after rain are magical',
                '🚶 Don\'t worry about getting lost — that\'s half the fun in Shinjuku'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ain Soph.Journey (Shinjuku)',
              description: 'Tokyo\'s most beloved vegan restaurant chain. The Shinjuku branch serves incredible plant-based Japanese and Western fusion — their fluffy vegan pancakes are legendary, but dinner mains like the heavenly burger and seasonal curry are outstanding. Warm, welcoming atmosphere perfect for jet-lagged travelers.',
              meta: '💰 $$ · 📍 3-8-9 Shinjuku, 2F · Reservations recommended during Golden Week'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '58-hectare garden with Japanese, English & French landscapes' },
        { lat: 35.6938, lng: 139.7035, label: 'Golden Gai', num: 2, cat: 'attraction', desc: 'Maze of 200+ tiny atmospheric bars' },
        { lat: 35.6934, lng: 139.7008, label: 'Omoide Yokocho', num: 3, cat: 'attraction', desc: 'Nostalgic alley of tiny eateries (Memory Lane)' },
        { lat: 35.6920, lng: 139.7050, label: 'Ain Soph.Journey', num: 4, cat: 'food', desc: 'Beloved vegan restaurant with Japanese-Western fusion' }
      ]
    },
    {
      num: 2,
      date: '2026-04-29',
      neighborhoods: 'Kamakura · Hase · Enoshima Coast',
      title: 'Kamakura: Temples, Great Buddha & Seaside Zen',
      description: "Escape Tokyo for a day in Kamakura — Japan's ancient coastal capital. It's Showa Day (Golden Week holiday), so we're starting early to beat crowds. Visit the iconic Great Buddha, the stunning Hase-dera Temple with its ocean-view gardens, and the serene bamboo groves of Hokoku-ji. A vegetarian shojin ryori lunch completes this spiritual day trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kōtoku-in: The Great Buddha (Daibutsu)',
              description: 'The 13-metre bronze Buddha has been sitting in open air since a tsunami washed away his temple hall in 1498. Arriving early (8am opening) means you\'ll have this iconic statue almost to yourselves. You can even step inside the hollow bronze statue for ¥50.',
              details: [
                '🗿 Entry: ¥300 (~$2), inside the statue: ¥50 extra',
                '⏰ Opens 8am — arrive at opening to avoid Golden Week crowds',
                '📸 The best photo angle is from slightly to the right, capturing the curved roofline behind',
                '🚆 Take JR Shonan-Shinjuku Line from Shinjuku to Kamakura (~1 hour), then Enoden Line to Hase Station'
              ]
            },
            {
              title: 'Hase-dera Temple',
              description: 'Just a 5-minute walk from the Great Buddha, Hase-dera is Kamakura\'s most beautiful temple. The hillside gardens overlook the Pacific Ocean, and the 9-metre golden Kannon statue is breathtaking. The cave of Benten and the jizo statues garden are hauntingly beautiful. In late April, fresh greenery and azaleas frame every view.',
              details: [
                '⛩️ Entry: ¥400 (~$2.80)',
                '🌊 The observation deck has panoramic ocean views — on clear days you can see Mt Fuji',
                '🌺 The garden paths wind up the hillside through hydrangeas, peonies, and moss-covered stones',
                '📿 Write a wish on an ema (wooden plaque) and hang it at the temple'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Hachinoki Kamakura (鉢の木)',
              description: 'Elegant shojin ryori (Buddhist vegetarian cuisine) restaurant near Kenchō-ji Temple. Multi-course seasonal meals served in lacquerware — a deeply traditional and entirely vegetarian experience. This is the kind of meal you\'ll remember for years.',
              meta: '💰 $$$ · 📍 7 Yamanouchi, Kamakura · Reservations recommended · Lunch sets from ¥3,300'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hōkoku-ji Temple (Bamboo Temple)',
              description: 'Known as the "Bamboo Temple," Hōkoku-ji hides a serene grove of over 2,000 towering moso bamboo behind its modest entrance. Sit in the tea house within the grove, sip matcha (¥600), and listen to the wind rustling through the bamboo. One of the most peaceful spots in all of Japan.',
              details: [
                '🎋 Entry: ¥300, matcha in the bamboo grove tea house: ¥600',
                '📸 Light filtering through the bamboo canopy is magical — morning light is best but afternoon has fewer visitors',
                '🚌 Take bus #5 from Kamakura Station (10 min) or walk 20 min through residential streets'
              ]
            },
            {
              title: 'Tsurugaoka Hachimangū Shrine',
              description: 'Kamakura\'s most important shrine, reached via a grand approach flanked by cherry trees and lotus ponds. The hilltop main hall offers views over the entire city down to the sea. The shrine was founded in 1063 and served as the center of the Kamakura shogunate.',
              details: [
                '⛩️ Free entry · Main hall at the top of a grand stone staircase',
                '🦷 The approach (Wakamiya Ōji) is lined with shops selling local snacks',
                '📍 Walk from here to Kamakura Station through Komachi-dōri shopping street'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Consider buying an Enoden 1-day pass (¥800) if taking the cute coastal tram between Kamakura and Hase. The ride along the coast with ocean views is lovely.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'T\'s TanTan (Tokyo Station)',
              description: 'Back in Tokyo, stop at this legendary vegan ramen shop inside Tokyo Station (Keiyo Street). Their soy-milk tantanmen is rich, spicy, and entirely plant-based — perfect comfort food after a day of temple-hopping. Always a queue but it moves fast.',
              meta: '💰 $ · 📍 Tokyo Station Keiyo Street (underground) · No reservations, expect 10-15 min wait'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3168, lng: 139.5359, label: 'Great Buddha (Kōtoku-in)', num: 1, cat: 'attraction', desc: '13m bronze Buddha statue from 1252' },
        { lat: 35.3120, lng: 139.5320, label: 'Hase-dera Temple', num: 2, cat: 'attraction', desc: 'Hillside temple with ocean views and golden Kannon' },
        { lat: 35.3240, lng: 139.5600, label: 'Hōkoku-ji (Bamboo Temple)', num: 3, cat: 'attraction', desc: 'Serene grove of 2,000 bamboo with matcha tea house' },
        { lat: 35.3260, lng: 139.5565, label: 'Tsurugaoka Hachimangū', num: 4, cat: 'attraction', desc: 'Kamakura\'s grand Shinto shrine from 1063' },
        { lat: 35.3250, lng: 139.5510, label: 'Hachinoki', num: 5, cat: 'food', desc: 'Elegant shojin ryori Buddhist vegetarian cuisine' },
        { lat: 35.6812, lng: 139.7671, label: 'T\'s TanTan', num: 6, cat: 'food', desc: 'Legendary vegan ramen in Tokyo Station' }
      ]
    },
    {
      num: 3,
      date: '2026-04-30',
      neighborhoods: 'Azabudai Hills · Ueno · Asakusa',
      title: 'teamLab Borderless, Ueno Park & Asakusa',
      description: "Today is your immersive art and culture day. Morning at teamLab Borderless — the world's most extraordinary digital art museum. Afternoon wandering through Ueno Park's temples and museums, then evening in atmospheric Asakusa with the lit-up Sensō-ji Temple and Tokyo SkyTree views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: 'A museum without a map — artworks flow out of rooms, merge with each other, and respond to your presence. Flowers bloom at your feet, waterfalls cascade across walls, and you become part of the art. The new Azabudai Hills location (reopened 2024) is even more stunning than the original. Allow 2-3 hours to fully immerse.',
              details: [
                '🎫 Book tickets online in advance — ¥3,800 adults (~$26). Sells out during Golden Week!',
                '⏰ Opens 10am, last entry varies — book the earliest slot available',
                '👗 Wear dark clothing for the best immersive effect. Avoid short skirts (mirrors on floor). Wear comfortable shoes.',
                '📸 Photography allowed — but put the phone down sometimes and just experience it',
                '📍 Azabudai Hills, Roppongi — direct access from Kamiyachō or Roppongi-Itchōme stations'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Falafel Brothers (Roppongi)',
              description: 'Authentic Middle Eastern falafel wraps and bowls, entirely vegetarian-friendly, right near Azabudai Hills. Fresh, filling, affordable — a welcome change of pace.',
              meta: '💰 $ · 📍 6-1-8 Roppongi · Casual, counter service'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Temples',
              description: 'Tokyo\'s cultural heart — a sprawling park housing world-class museums, ancient temples, and a beautiful shinobazu pond with lotus flowers. Stroll past the Tōshō-gū Shrine (golden Edo-era shrine), visit Kiyomizu Kannon-dō (modeled after Kyoto\'s famous temple), and simply enjoy the park atmosphere with locals.',
              details: [
                '🌳 Free entry to the park · Individual museums have separate admission',
                '⛩️ Ueno Tōshō-gū: ¥500 — stunning gold-leaf shrine from 1627',
                '🏛️ Tokyo National Museum (¥1,000) if you want to explore — Japan\'s oldest and largest museum',
                '🦆 Shinobazu Pond is lovely for a peaceful walk'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dōri',
              description: 'Tokyo\'s oldest temple (founded 645 AD) is spectacular at dusk when the crowds thin and the enormous red lanterns glow. Walk through the Kaminarimon (Thunder Gate), browse the Nakamise-dōri shopping street for traditional snacks and souvenirs, and soak in the atmosphere of old Edo Tokyo.',
              details: [
                '⛩️ Free entry · Temple grounds always open, main hall until 5pm but the exterior is stunning at night',
                '🏮 The massive red lantern at Kaminarimon weighs 700kg',
                '🍘 Try age-manju (fried sweet buns) and senbei (rice crackers) on Nakamise-dōri — both vegetarian',
                '📸 Evening is the most atmospheric time — fewer crowds, beautiful lighting'
              ]
            },
            {
              title: 'Tokyo SkyTree View',
              description: 'At 634 metres, SkyTree is the world\'s tallest tower. From Asakusa, it\'s a beautiful 15-minute walk across the Sumida River — the tower glowing against the night sky is unforgettable. If you want to go up, the observation deck offers 360° views of Tokyo. On clear days, Mt Fuji is visible to the west.',
              details: [
                '🗼 Tembo Deck (350m): ¥2,100, Tembo Galleria (450m): ¥3,100 for both',
                '⏰ Open until 9pm (last entry 8pm)',
                '🏔️ Mt Fuji is best visible on clear mornings, but evening views of the city lights are equally stunning',
                '📸 The view from the Sumida River bank looking up at SkyTree is a great free alternative'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bon (Taito-ku)',
              description: 'Tokyo\'s most celebrated shojin ryori restaurant, run by a Buddhist monk for over 100 years. A multi-course kaiseki-style vegetarian feast served in a traditional tatami room in a serene temple setting. This is a bucket-list meal — possibly the finest vegetarian dining experience in Japan.',
              meta: '💰 $$$ · 📍 1-2-11 Ryusen, Taito-ku · Reservations essential (book weeks ahead) · Lunch ¥5,500, Dinner ¥8,800'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6602, lng: 139.7393, label: 'teamLab Borderless', num: 1, cat: 'attraction', desc: 'Immersive digital art museum at Azabudai Hills' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 2, cat: 'attraction', desc: 'Cultural park with museums, temples & lotus pond' },
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 3, cat: 'attraction', desc: 'Tokyo\'s oldest temple (645 AD) with iconic Thunder Gate' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo SkyTree', num: 4, cat: 'attraction', desc: '634m tower with panoramic views — world\'s tallest' },
        { lat: 35.6610, lng: 139.7340, label: 'Falafel Brothers', num: 5, cat: 'food', desc: 'Vegetarian Middle Eastern food near Azabudai Hills' },
        { lat: 35.7230, lng: 139.7930, label: 'Bon', num: 6, cat: 'food', desc: 'Legendary 100-year-old shojin ryori restaurant' }
      ]
    },
    {
      num: 4,
      date: '2026-05-01',
      neighborhoods: 'Harajuku · Meiji Shrine · Shibuya · Ashikaga (day trip option)',
      title: 'Meiji Shrine, Harajuku & Wisteria Wonderland',
      description: "A day of contrasts — begin in the sacred forest of Meiji Shrine, wander through Harajuku's creative energy, then choose your afternoon: either a half-day trip to Ashikaga Flower Park for wisteria in peak bloom, or a relaxed exploration of Shibuya and Yoyogi Park. Both options are magical.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'Walk through the towering torii gate into a 70-hectare forest that feels a world away from the city. This shrine, dedicated to Emperor Meiji and Empress Shōken, is Tokyo\'s most important Shinto sanctuary. The forest was planted by volunteers in 1920 — now 100,000 trees create a canopy of peaceful green.',
              details: [
                '⛩️ Free entry · Open sunrise to sunset',
                '🌳 The approach through the forest takes 10-15 minutes — don\'t rush it',
                '🍶 Look for the wall of sake barrels (donated by breweries) and wine barrels (donated by Burgundy)',
                '📿 Write a wish on an ema (wooden plaque, ¥500) or draw an omikuji fortune'
              ]
            },
            {
              title: 'Yoyogi Park',
              description: 'Adjacent to Meiji Shrine, Yoyogi Park is where Tokyoites come to breathe. On weekends and holidays, you\'ll find musicians, dancers, picnickers, and dog walkers. Spread a blanket under the trees and people-watch — this is authentic Tokyo leisure.',
              details: [
                '🌳 Free entry, open 24/7',
                '🎵 The area near the main fountain often has street performers on holidays',
                '🐕 The dog-walking scene is excellent entertainment'
              ]
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Step from the tranquil shrine directly into Harajuku\'s creative chaos. Takeshita-dōri is a narrow lane packed with quirky fashion shops, crêpe stands, and kawaii culture. Cat Street (one block over) is more refined — vintage shops, designer boutiques, and excellent cafés.',
              details: [
                '🛍️ Takeshita-dōri is intense — visit before noon for manageable crowds',
                '🍦 Try a Japanese crêpe (many have vegetarian fruit options)',
                '🐱 Cat Street is the cooler, calmer alternative — independent shops and galleries'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Afuri (Harajuku)',
              description: 'Famous for their yuzu shio (citrus salt) ramen — and they have a fully vegan version. Light, fragrant, and utterly delicious. The vegan broth is made with kelp and vegetables, topped with seasonal veg. A must-try.',
              meta: '💰 $ · 📍 1-17-1 Jingumae, Shibuya · Expect a short queue at lunch'
            }
          ]
        },
        {
          label: 'Afternoon — Option A (Recommended)',
          activities: [
            {
              title: '🌸 Ashikaga Flower Park — Great Wisteria Festival',
              description: 'A magical half-day trip to see one of Japan\'s most spectacular sights: cascading wisteria in full bloom. The park\'s 150-year-old Great Wisteria tree covers 1,000 square metres in a canopy of purple, pink, white, and golden flowers. Late April is peak season — the timing could not be better. The evening illumination is especially breathtaking.',
              details: [
                '🌸 Peak wisteria bloom: late April to early May — perfect timing for your visit!',
                '🎫 Entry: ¥1,200–2,300 depending on bloom status (higher = better blooms)',
                '🚆 From Tokyo: JR Ueno/Utsunomiya Line to Oyama, transfer to Ryomo Line → Ashikagaflowerpark Station (~90 min total)',
                '🌙 Evening illumination (light-up) until 9pm is absolutely worth staying for',
                '📸 The reflection of wisteria in the garden ponds is the iconic shot',
                '⚠️ Golden Week crowds — go on a weekday (May 1 is Friday) for slightly fewer visitors'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If Ashikaga feels too ambitious, Option B: spend the afternoon at Yoyogi Park, explore Shibuya Crossing, visit the Shibuya Sky observation deck (¥2,000), and wander through Daikanyama\'s bookshops and cafés. Both are wonderful.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sougo (Roppongi)',
              description: 'Refined shojin ryori in a modern setting — Chef Sougo\'s multi-course vegetarian kaiseki is art on a plate. Each dish uses seasonal ingredients prepared with meticulous care. A beautiful way to celebrate your last full evening in Tokyo.',
              meta: '💰 $$$ · 📍 3-4-15 Roppongi, Minato-ku · Reservations essential · Course menus from ¥6,600'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Tokyo\'s most important Shinto shrine in a 70-hectare forest' },
        { lat: 35.6717, lng: 139.6949, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Spacious park for people-watching and relaxation' },
        { lat: 35.6702, lng: 139.7027, label: 'Harajuku / Takeshita-dōri', num: 3, cat: 'attraction', desc: 'Youth culture, fashion & kawaii central' },
        { lat: 36.3150, lng: 139.5200, label: 'Ashikaga Flower Park', num: 4, cat: 'attraction', desc: 'Cascading wisteria in peak bloom — Great Wisteria Festival' },
        { lat: 35.6690, lng: 139.7040, label: 'Afuri Harajuku', num: 5, cat: 'food', desc: 'Famous yuzu ramen with vegan option' },
        { lat: 35.6640, lng: 139.7310, label: 'Sougo', num: 6, cat: 'food', desc: 'Modern shojin ryori kaiseki — exquisite vegetarian' }
      ]
    },
    {
      num: 5,
      date: '2026-05-02',
      neighborhoods: 'Asakusa · Departure',
      title: 'Morning Calm & Farewell Tokyo',
      description: "Your final morning before flying onward to Australia. Keep it simple and savour these last hours — a peaceful temple visit, a final Japanese breakfast, and some last-minute souvenir shopping. No rushing.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Morning at Sensō-ji (Revisit)',
              description: 'If you\'re up early (jet lag might help!), revisit Sensō-ji before the crowds arrive. At 6-7am, the temple grounds are nearly empty and bathed in soft morning light. Watch the monks\' morning rituals, hear the temple bells, and say goodbye to Tokyo the way you arrived — gently.',
              details: [
                '🌅 Temple grounds open from early morning — the main hall opens at 6am',
                '📸 Morning light through the incense smoke is ethereal',
                '🍵 Pick up one last matcha at a nearby café before heading out'
              ]
            },
            {
              title: 'Nakamise-dōri & Souvenir Shopping',
              description: 'The shops on Nakamise-dōri open around 9-10am. Pick up last souvenirs — traditional fans, chopsticks, tenugui cloths, Japanese sweets, and matcha snacks make perfect gifts. Everything is compact and packable.',
              details: [
                '🎁 Best vegetarian omiyage (gifts): matcha Kit-Kats, senbei, yatsuhashi, dried fruit',
                '🛍️ Kappabashi Street (10 min walk) has the famous kitchen/food replica shops',
                '📦 Most souvenir shops can vacuum-seal food items for travel'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Misojyu (Asakusa)',
              description: 'Beautiful miso soup restaurant near Sensō-ji specializing in artisanal miso soups with seasonal vegetables. Their vegetable miso set with rice and pickles is the quintessential Japanese breakfast — simple, warming, and entirely vegetarian.',
              meta: '💰 $ · 📍 1-7-5 Asakusa · Opens 10am (or grab konbini onigiri earlier)'
            }
          ],
          tips: [
            { type: 'tip', text: 'For afternoon flights from Narita: leave Asakusa by noon at latest. Keisei Skyliner from Ueno is the fastest route (36 min to Narita, ¥2,520). From Haneda, allow 60-90 min from central Tokyo. Send large luggage ahead via takkyubin (hotel front desk can arrange) to travel light to the airport.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Early morning visit — peaceful and atmospheric' },
        { lat: 35.7140, lng: 139.7960, label: 'Nakamise-dōri', num: 2, cat: 'attraction', desc: 'Traditional souvenir shopping street' },
        { lat: 35.7122, lng: 139.7950, label: 'Misojyu', num: 3, cat: 'food', desc: 'Artisanal miso soup — perfect Japanese breakfast' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per couple)', budget: '¥6,000–10,000/night (hostel/capsule)', midrange: '¥15,000–30,000/night', luxury: '¥50,000–100,000/night' },
    { category: 'Meals (for two)', budget: '¥3,000–5,000/day', midrange: '¥6,000–12,000/day', luxury: '¥15,000–30,000/day' },
    { category: 'Transport', budget: '¥1,000–2,000/day (IC card)', midrange: '¥2,000–4,000/day', luxury: '¥5,000–10,000/day (taxi/private)' },
    { category: 'Activities', budget: '¥1,000–2,000/day', midrange: '¥3,000–6,000/day', luxury: '¥8,000–15,000/day' },
    { category: '5-Day Total (couple)', budget: '¥80,000–130,000 ($550–900)', midrange: '¥180,000–300,000 ($1,200–2,000)', luxury: '¥400,000+ ($2,700+)' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport: Narita Express (NEX) to Shinjuku/Tokyo (~90 min, ¥3,250) or budget Keisei Access Express (~70 min, ¥1,270)', 'Haneda Airport: closer to central Tokyo — Keikyu Line to Shinagawa (~20 min, ¥300)', 'Get a Suica or Pasmo IC card at the airport immediately — works on all trains, buses, and many shops', 'Consider a 72-hour Tokyo Metro pass (¥1,500) for excellent value'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku area — central, great transport hub, close to Gyoen. Recommended: Hotel Gracery Shinjuku, Onsen Ryokan Yuen Shinjuku', 'Asakusa — traditional atmosphere, near Sensō-ji & SkyTree. Recommended: Wired Hotel Asakusa, Richmond Hotel Premier Asakusa', 'Budget: consider a ryokan (traditional inn) for at least one night — the experience of tatami rooms and onsen is unforgettable', 'Book well ahead for Golden Week — hotels fill up fast'] },
    { title: '🌡️ Weather', items: ['Late April/early May: 15–22°C (59–72°F) — ideal walking weather', 'Occasional spring rain — pack a compact umbrella', 'Layering is key: warm midday, cool mornings and evenings', 'UV is moderate — sunscreen for full outdoor days'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless but still carry ¥10,000–20,000 cash for small shops and temples', 'IC cards (Suica/Pasmo) work at convenience stores, vending machines, and many restaurants', 'Tipping is not customary in Japan — in fact it can be considered rude', '7-Eleven and Lawson ATMs accept international cards'] },
    { title: '📱 Connectivity & Tips', items: ['Rent a pocket WiFi at the airport or buy an eSIM (Ubigi, Airalo) before arriving', 'Download Google Maps offline and HappyCow app for finding vegetarian restaurants', 'Konbini (convenience stores) are a lifesaver: 7-Eleven, Lawson, FamilyMart have onigiri, edamame, and inari sushi — all vegetarian', 'Learn basic phrases: Sumimasen (excuse me), Arigatou gozaimasu (thank you), Oishii (delicious)'] },
    { title: '🎫 Book Ahead (Essential)', items: ['teamLab Borderless — book tickets online ASAP, sells out during Golden Week', 'Ghibli Museum (if you go) — advance reservation only, tickets release monthly via Lawson Ticket or JTB for overseas visitors. Extremely limited during Golden Week — book 2+ months ahead', 'Bon restaurant — book 2-4 weeks ahead for this beloved shojin ryori experience', 'Ashikaga Flower Park — no reservation needed but buy train tickets early'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
