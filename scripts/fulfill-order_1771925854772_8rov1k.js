const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771925854772_8rov1k',
  email: 'nihattopal@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-05-20',
  endDate: '2026-05-24',
  groupSize: '3-4',
  travelStyle: 'Cultural, Foodie, Family-friendly',
  dining: 'Fine dining all meals',
  budget: 'Surprise me',
  requests: 'hotel, temple, food, tourist spots, shopping'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo — Fine Dining, Sacred Temples & Family Magic',
  subtitle: '5 days of Michelin-starred omakase, ancient shrines, world-class shopping & unforgettable moments for 3-4 people',
  description: "Tokyo is one of the most extraordinary cities on earth — and for a family that loves culture, temples, and exceptional food, it may be the single best destination in the world. More Michelin stars than Paris and New York combined. Centuries-old shrines tucked between glittering skyscrapers. Shopping that ranges from 1,000-year-old ceramics to bleeding-edge streetwear. May is the perfect month: the heat of summer hasn't arrived, the parks are lush green, irises bloom in palace gardens, and the city hums with a particular vitality that feels impossible to describe and impossible to forget. This itinerary is built for a family who wants the very best — every meal a destination, every neighborhood a discovery. Iyi yolculuklar — bon voyage.",
  duration: '4 nights',
  dates: 'May 20 – May 24, 2026',
  budget: '$$$–$$$$',
  pace: 'Moderate',
  bestFor: 'Families, food lovers, culture seekers',

  highlights: [
    'Michelin-starred omakase sushi — watch a master chef compose 20-course perfection piece by piece',
    'Senso-ji Temple at dawn — Tokyo\'s oldest temple in golden morning light, before the crowds arrive',
    'Meiji Shrine forest walk — 70,000 trees of serene silence minutes from Shinjuku\'s neon chaos',
    'Kaiseki at Nihonryori RyuGin — one of the world\'s great restaurants, where each course tells a story',
    'Ginza shopping — from Uniqlo flagship to Itoya stationery to Cartier, the most refined mile in Asia',
    'teamLab Planets — the world\'s most breathtaking immersive digital art experience (kids go silent with awe)'
  ],

  essentials: [
    {
      title: '🍽️ Fine Dining in Tokyo — Book NOW',
      text: 'Tokyo\'s top restaurants book out weeks to months in advance. For Michelin-starred omakase and kaiseki, use Tableall.com, Omakase.jp, or Pocket Concierge immediately — these are the trusted English-language platforms for hard-to-book Tokyo restaurants. Sukiyabashi Jiro Honten requires an invitation via hotel concierge. Nihonryori RyuGin, Narisawa, and Quintessence can sometimes be booked 4-8 weeks ahead. Your hotel\'s concierge (especially at Park Hyatt or Aman) can often pull strings. Start booking the moment your travel is confirmed.'
    },
    {
      title: '🏨 Where to Stay — Luxury Hotels',
      text: 'For a family of 3-4, we recommend: **Park Hyatt Tokyo** (Shinjuku, floors 41-52, "Lost in Translation" hotel — spectacular views, top-tier pool and spa, ¥60,000-90,000/night), **Aman Tokyo** (Otemachi, temple-like calm in the heart of the city, ¥120,000+/night), or **The Peninsula Tokyo** (Hibiya, Michelin-starred restaurant in-house, perfect for Ginza/Tsukiji days). All three provide concierge services that will help secure restaurant reservations and car transfers.'
    },
    {
      title: '🌤️ May in Tokyo — Perfect Timing',
      text: 'May is arguably the best month to visit Tokyo. Daytime temperatures: 20-26°C (68-79°F), low humidity, clear skies. The city\'s parks are vivid green. Irises bloom in the Imperial Palace East Gardens. Yoyogi Park is at its most beautiful. Crowds are moderate compared to cherry blossom season (March-April). No typhoons yet (those come September-October). Pack light layers — evenings can be cool (15-18°C). One umbrella per family is wise; May has occasional brief showers.'
    },
    {
      title: '🚇 Getting Around Tokyo',
      text: 'For a fine-dining family trip: use a mix of Tokyo Metro and taxis/private transfers. Get a Suica or Pasmo IC card at the airport for trains — tap in/tap out. For dinner evenings (especially after wine or sake), budget ¥1,500-2,500 per taxi ride — they\'re clean, reliable, and the driver will find any address. Your hotel concierge can arrange private car services for airport transfers and special evenings. Google Maps is flawless for navigation in Tokyo.'
    },
    {
      title: '💴 Money & Tipping',
      text: 'Japan is still largely cash-preferring, especially at traditional and upscale restaurants. Hit a 7-Eleven or Japan Post ATM on arrival — they reliably accept foreign cards. Budget ¥50,000-80,000 per person per day (meals, taxis, shopping). Tipping is NOT done in Japan — it can even cause offense. Saying "oishii" (delicious) or "subarashii" (wonderful) is the correct way to compliment a chef. Fine dining restaurants may add a 10-15% service charge; check the menu.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-20',
      neighborhoods: 'Shinjuku · Nishi-Azabu · Shinjuku Gyoen',
      title: 'Arrive in Tokyo — First Night Elegance',
      description: "Touch down and check into one of the world's great hotels. Shinjuku is the natural home base for this trip — central, surrounded by food and culture, with the vast Shinjuku Gyoen garden nearby. Tonight's dinner is a statement: L'Effervescence in Nishi-Azabu, a French-Japanese restaurant that earns its Michelin stars on every plate. Your first night in Tokyo should feel like an arrival.",
      timeBlocks: [
        {
          label: 'Arrival & Afternoon',
          activities: [
            {
              title: 'Arrive at Narita or Haneda — Transfer to Hotel',
              description: "From Narita Airport, the Narita Express (N'EX) runs direct to Shinjuku in about 90 minutes — comfortable, punctual, perfectly designed. From Haneda, the Keikyu Line connects to Shinagawa, then Yamanote Line to Shinjuku (about 45 minutes). Your hotel concierge can arrange a private car transfer if preferred — book in advance. Check in, drop your bags, and let Tokyo begin.",
              details: [
                '✈️ Narita → Shinjuku: N\'EX Limited Express — ¥3,250 adult, ¥1,630 child, ~90 min',
                '✈️ Haneda → Shinjuku: Keikyu Line + Yamanote Line — ¥690 per person, ~45 min',
                '🚗 Private car transfer (recommended for families): book via hotel concierge — ¥15,000-25,000',
                '🏨 Suica/Pasmo IC cards: get them at the airport — use for all trains, buses, convenience stores',
                '🎒 Most hotels accept early luggage drop even before check-in time — arrive relaxed'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden — Afternoon Walk',
              description: "A 10-minute walk from the Park Hyatt, Shinjuku Gyoen is one of Japan's finest gardens — 144 acres of French formal gardens, English landscape lawns, and a traditional Japanese strolling garden. In May, the garden blazes with azaleas, irises, wisteria, and fresh green foliage. The French garden's central lawn is perfect for a post-flight rest — lie on the grass and let the jet lag dissolve.",
              details: [
                '🌿 Entry: ¥500 adults, ¥250 children · Open Tue-Sun, 9am-6pm (May)',
                '🌸 May blooms: azaleas (early May), irises, roses, and fresh green canopy',
                '🌳 The Japanese garden section has a teahouse — try matcha and wagashi (traditional sweets)',
                '📍 Shinjuku Gyoenmae Station (Marunouchi Line) or 10-min walk from Park Hyatt',
                '📸 The English landscape section offers the best photos — wide lawns, mature zelkova trees'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Your first afternoon in Tokyo: resist the urge to run. Shinjuku Gyoen is the perfect decompression chamber — a vast, beautiful park in the middle of the world\'s largest city. Walk slowly. Breathe deeply. Tokyo rewards those who pace themselves.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku at Twilight — Kabukicho Tower & Golden Gai',
              description: "Before dinner, take a 30-minute evening walk through Shinjuku's contrasts. The Kabukicho entertainment district is spectacular at twilight — the new Kabukicho Tower rises 48 floors and its ground-floor entertainment zone is a spectacle worth seeing even without entering. Then find your way to Golden Gai — a tiny labyrinth of over 200 miniature bars packed into six narrow alleys. Each bar seats only 5-8 people. It's a Tokyo institution, and the atmosphere (neon signs, jazz floating from open doors, decades of history in every splinter) is unlike anywhere on earth.",
              details: [
                '🌃 Golden Gai: tucked behind Kabukicho, 5-min walk from Shinjuku Station east exit',
                '🍸 Most Golden Gai bars welcome tourists — look for ones with English signage',
                '🎷 The best bars have live jazz, jazz records, or whisky collections older than you',
                '⏰ Keep it to one pre-dinner drink — tonight\'s dinner deserves your full palate'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: "L'Effervescence — Nishi-Azabu (Michelin 2 Stars)",
              description: "One of Tokyo's most celebrated French-Japanese restaurants. Chef Shinobu Namae trained under Michel Bras and Heston Blumenthal, and his tasting menu is a meditation on Japanese ingredients expressed through French technique. The seasonal menu changes constantly — in May expect course after course built around spring vegetables, freshwater fish, and ingredients sourced from farms Namae works with personally. The dining room is serene and beautiful. Service is impeccable without being stiff. Wine pairings from a thoughtful natural wine-leaning list. Book via Tableall.com or your hotel concierge — typically 4-8 weeks in advance.",
              meta: '💰 ¥30,000-45,000 per person with pairings · 📍 2-26-4 Nishi-Azabu, Minato-ku · Tel: 03-5766-9500 · Book via Tableall.com · Dress code: smart casual'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6917, label: 'Park Hyatt Tokyo', num: 1, cat: 'attraction', desc: '"Lost in Translation" hotel — floors 41-52, breathtaking Shinjuku views' },
        { lat: 35.6851, lng: 139.7103, label: 'Shinjuku Gyoen National Garden', num: 2, cat: 'attraction', desc: '144-acre garden paradise — azaleas, irises, and Japanese traditional strolling garden in May' },
        { lat: 35.6960, lng: 139.7036, label: 'Kabukicho / Golden Gai', num: 3, cat: 'attraction', desc: 'Neon entertainment district + 200-bar labyrinth of tiny jazz bars — Tokyo at its most atmospheric' },
        { lat: 35.6547, lng: 139.7271, label: "L'Effervescence, Nishi-Azabu", num: 4, cat: 'food', desc: 'Michelin 2-star French-Japanese tasting menu — seasonal, ingredient-driven, extraordinary' }
      ]
    },
    {
      num: 2,
      date: '2026-05-21',
      neighborhoods: 'Asakusa · Ueno · Roppongi',
      title: 'Sacred Tokyo — Senso-ji, Old Edo & Kaiseki at RyuGin',
      description: "Today is Tokyo's oldest soul. Rise early and arrive at Senso-ji Temple in Asakusa before 8am — the city's oldest temple complex, golden and incense-filled, belongs to early risers. Walk Nakamise shopping street, cross the river to the Sumida River walk, and then spend the afternoon in Ueno. Tonight is a pinnacle: Nihonryori RyuGin, where chef Seiji Yamamoto has held three Michelin stars for years and runs the most creative kaiseki program in Japan.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple Complex — Asakusa at Dawn',
              description: "Tokyo's oldest and most magnificent temple. Enter through Kaminarimon (Thunder Gate) with its enormous red and black lantern, walk the 250-meter Nakamise shopping street, and arrive at the main temple hall where incense smoke curls into the sky. Early morning is essential — by 9am the crowds are thick; by 7am you may have the temple courtyard almost to yourself. The light at dawn through the incense smoke and ancient wooden structures is one of Tokyo's great visual experiences.",
              details: [
                '⛩️ Free to enter · Temple grounds open 24 hours · Main hall: 6am-5pm',
                '🕕 Arrive before 7:30am — the temple at dawn with minimal crowds is breathtaking',
                '🎋 Omikuji fortune sticks: ¥100 — shake the cylinder, a numbered stick falls out, find your fortune drawer',
                '📸 Best photo: stand inside Nakamise looking back at Kaminarimon gate with morning light behind',
                '🚗 From Park Hyatt Shinjuku: taxi is easiest — ¥1,800-2,500, about 25 minutes'
              ]
            },
            {
              title: 'Nakamise Shopping Street & Surroundings',
              description: "The covered shopping arcade leading to Senso-ji has 89 shops selling traditional crafts and souvenirs — the best in Tokyo for quality traditional items. Look for: handmade tenugui (cotton hand towels with beautiful woodblock-print designs), traditional lacquerware, Japanese fans, and genuine ningyo-yaki (small sponge cakes shaped like Senso-ji symbols, filled with red bean paste). Walk the side streets behind the shopping street — the backstreets of Asakusa feel like old Edo-era Tokyo.",
              details: [
                '🎎 Quality souvenirs: Beniya (lacquerware and ceramics), Nakaya (craft textiles and fans)',
                '🧁 Snack: ningyo-yaki from Kimuraya — fresh from the mold, sweet bean paste inside',
                '⛩️ Side streets behind Nakamise: Dempoin-dori for traditional craft shops and old atmosphere',
                '🌊 Walk 10 min to the Sumida River and look back at the Senso-ji Five-Story Pagoda — perfect'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Kamiya Bar Breakfast / Café Aoiro, Asakusa',
              description: 'Start with breakfast at your hotel, or if arriving in Asakusa early: Café Aoiro near Senso-ji is an elegant little spot with excellent drip coffee, thick toast, and egg dishes. A refined, unhurried morning fuel before the temple walk. Alternatively, the Park Hyatt\'s Peak Lounge breakfast (¥6,000-8,000 per person) with sweeping Shinjuku views is one of Tokyo\'s great hotel breakfasts.',
              meta: '💰 Café Aoiro: ¥800-1,500 · 📍 Near Senso-ji · Opens 8am · Hotel breakfast (Park Hyatt): ¥6,000-8,000'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tokyo National Museum — Ueno Park',
              description: "The Tokyo National Museum is one of the world's great museums — and in May the Ueno Park setting is at its most beautiful. The museum's 110,000-object collection spans 5,000 years of Japanese art and cultural history. The Honkan (Japanese Gallery) main building is essential: samurai armor that makes you stop breathing, Buddhist sculpture of heartbreaking beauty, ancient ceramics, and calligraphy scrolls. The Heiseikan gallery's archaeological exhibits show Japan from the stone age to the imperial era. Give it 2-3 hours.",
              details: [
                '🏛️ Entry: ¥1,000 adults · Free for under 18 · Open Tue-Sun, 9:30am-5pm',
                '⚔️ Don\'t miss: Japanese Swords Gallery (room 13), the lacquerwork collection (room 10)',
                '🪆 The Honkan building itself (1938) is stunning — Romanesque Japanese architecture',
                '🌿 After: stroll Ueno Park\'s tree-lined paths — lush green canopy in May, peaceful and beautiful'
              ]
            },
            {
              title: 'Yanaka — Old Tokyo Backstreets',
              description: "A 20-minute walk from Ueno, Yanaka is one of Tokyo's best-preserved old neighborhoods — it survived both the 1923 earthquake and the WWII firebombing, and its wooden temple alleys and shotengai (old shopping street) feel like 1960s Japan. Yanaka Ginza is a covered street with local butchers, tofu makers, ceramic shops, and the most neighborhood-local atmosphere in central Tokyo. Cats sit in doorways. Old women tend flower pots. It's everything.",
              details: [
                '🐱 Community cats everywhere in Yanaka — stop for photos freely',
                '🍡 Try menchi-katsu (fried beef patty, ¥200) and fresh dango from the stalls',
                '⛩️ Yanaka Cemetery: a peaceful walk through old Tokyo — ancient family graves and mature trees',
                '📍 Access via Nippori Station (JR Yamanote Line), 5-min walk to Yanaka Ginza'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Tempura Kondo — Ginza (Michelin 1 Star)',
              description: 'A slight detour to Ginza for what is considered one of the finest tempura experiences in Tokyo. Chef Fumio Kondo has been frying tempura here for decades and his mastery shows in every bite — the batter is paper-thin, the oil temperature perfect, and the vegetables (sweet potato, burdock root, lotus) are treated with as much reverence as the seafood. The hinoki (cypress) counter seats 12. The lunch courses are more accessible than dinner. Book via Tableall.com.',
              meta: '💰 Lunch: ¥12,000-18,000 per person · 📍 Sakaguchi Building 9F, 5-5-3 Ginza, Chuo-ku · Tel: 03-5568-0923 · Book in advance'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Roppongi Hills — Pre-Dinner Walk',
              description: "Take a 30-minute stroll through Roppongi Hills before dinner — the development built around the Mori Tower is one of Tokyo's most sophisticated mixed-use neighborhoods. The Mori Art Museum (floors 52-53 of Mori Tower) is often spectacular. The outdoor Tokyo City View observatory gives a 360-degree look at the glittering city at dusk. Roppongi is also where RyuGin is located, so you're already in the right neighborhood.",
              details: [
                '🏙️ Tokyo City View Observatory: ¥2,000 adults · Spectacular at dusk — you can see Mt. Fuji on clear days',
                '🎨 Mori Art Museum: check current exhibition — one of Tokyo\'s best contemporary art spaces',
                '🌆 The Louise Bourgeois spider sculpture "Maman" in the plaza is a striking landmark',
                '⏰ Leave the observatory by 7pm for your 7:30pm reservation'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nihonryori RyuGin — Roppongi (Michelin 3 Stars)',
              description: 'Chef Seiji Yamamoto has held three Michelin stars here for well over a decade, and RyuGin remains one of the most exciting kaiseki experiences in Japan. Unlike traditional kaiseki, Yamamoto uses cutting-edge technique to reinterpret Japanese seasonal cuisine — his dishes look like art installations and taste like they were composed by someone who loves Japan\'s culinary heritage too much to leave it unchanged. In May expect mountain vegetables, firefly squid, young bamboo shoots, and early summer fish. The beverage pairing (sake and Japanese whisky) is exceptional. Book via Pocket Concierge or your hotel concierge — 6-8 weeks in advance minimum.',
              meta: '💰 ¥40,000-55,000 per person with pairings · 📍 Side Roppongi Building 1F, 7-17-24 Roppongi · Tel: 03-3423-8006 · Pocket Concierge or hotel concierge booking'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s most ancient temple — arrive before 8am for magical, crowd-free atmosphere' },
        { lat: 35.7143, lng: 139.7964, label: 'Nakamise Shopping Street', num: 2, cat: 'attraction', desc: 'Traditional souvenirs — lacquerware, tenugui, hand fans, ningyo-yaki sweets' },
        { lat: 35.7188, lng: 139.7767, label: 'Tokyo National Museum', num: 3, cat: 'attraction', desc: 'World-class Japanese art — samurai armor, Buddhist sculpture, 5,000 years of history' },
        { lat: 35.7267, lng: 139.7663, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Old Tokyo neighborhood — friendly cats, local butchers, atmosphere frozen in time' },
        { lat: 35.6625, lng: 139.7312, label: 'Tempura Kondo, Ginza', num: 5, cat: 'food', desc: 'Michelin 1-star tempura — paper-thin batter, perfect oil, the finest tempura in Tokyo' },
        { lat: 35.6629, lng: 139.7293, label: 'Nihonryori RyuGin, Roppongi', num: 6, cat: 'food', desc: 'Michelin 3-star kaiseki — innovative, seasonal, ingredient-obsessed. A life-changing dinner.' }
      ]
    },
    {
      num: 3,
      date: '2026-05-22',
      neighborhoods: 'Harajuku · Meiji Shrine · Omotesando · Minami-Aoyama · Shibuya',
      title: 'Meiji Shrine, Harajuku Energy & Narisawa',
      description: "A day of beautiful contrasts: the ancient forest silence of Meiji Shrine, the exuberant kawaii culture of Harajuku, the architectural elegance of Omotesando, and one of the most interesting lunch experiences in Asia — Narisawa, where chef Yoshihiro Narisawa has invented his own cuisine called 'innovative Satoyama.' The evening brings Shibuya's legendary scramble crossing, and dinner at the intimate, thrilling Florilège.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingu Shrine — Forest Walk',
              description: "One of Tokyo's most peaceful and profound experiences. The 70,000 trees surrounding Meiji Shrine — donated from across Japan when the shrine was built in 1920 — have grown into a forest so tall and dense that it feels impossible this is central Tokyo. Walk the gravel path from the outer torii gate through the trees to the main shrine complex. In May, the iris garden (Kitanomaru side of the shrine) is in spectacular bloom — 1,500 irises of 150 varieties. Dedicated to Emperor Meiji and Empress Shoken, the shrine has a profound, meditative quality.",
              details: [
                '⛩️ Free to enter · Open sunrise to sunset (approx 4:55am–6:20pm in May)',
                '🌺 Iris Garden (Meiji Jingu Gyoen): ¥500 · Open 9am–4:30pm during iris season (mid-May to mid-June)',
                '🌲 The 700m walk through forest is the whole point — do it slowly, especially on a weekday morning',
                '👰 Traditional Shinto weddings on weekends — if you see the white-kimono procession, step aside and watch',
                '🎋 Sake barrel display at the entrance: 300+ barrels donated by breweries — beautiful torii photo backdrop'
              ]
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: "A 5-minute walk from Meiji Shrine, Takeshita Street (竹下通り) is the most concentrated expression of Japanese kawaii culture on earth — a 350-meter pedestrian alley packed with crepe stands, rainbow cotton candy, idol merchandise, and fashion that defies categorization. For families, it's joyful and genuinely fun. Try a Harajuku crepe from the Marion Crepes original location (since 1976). The energy is infectious and the people-watching is spectacular.",
              details: [
                '🌈 Harajuku crepes: the original style — thin, filled with strawberries, cream, banana, chocolate',
                '🍬 Rainbow cotton candy on a stick: ¥700-900 — outrageously photogenic',
                '🎌 Peak Harajuku fashion: look for 6%DOKIDOKI, Spinns, and the vintage shops on side streets',
                '⏰ Busy by 11am on weekends — if you\'re going Saturday, arrive by 10:30am'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'The Roastery by Nozy Coffee, Harajuku',
              description: 'One of Tokyo\'s finest specialty coffee shops, a short walk from Meiji Shrine. Single-origin pour-overs, exceptional espresso, and a beautiful interior with wooden beams and curated music. Pair with a fresh pastry. The perfect pre-shrine fuel — unhurried, quality-first, Tokyo at its best.',
              meta: '💰 ¥700-1,200 · 📍 5-17-13 Jingumae, Shibuya · Opens 10am · Perfect for mid-morning coffee after an early shrine visit'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Omotesando — Architecture & Shopping',
              description: "A 5-minute walk from Harajuku, Omotesando is Tokyo's most architecturally significant boulevard — a wide, zelkova-tree-lined avenue flanked by flagship stores designed by the world's top architects. The buildings alone are worth the walk: Prada by Herzog & de Meuron (glass mesh), Dior by SANAA, Tod's by Toyo Ito (concrete trees). The side streets (Ura-Harajuku, Minami-Aoyama) contain Tokyo's best concept stores, galleries, and cafés.",
              details: [
                '🏛️ Architecture stops: Prada Aoyama, Dior Omotesando, Gyre complex (MVRDV), Omotesando Hills',
                '🛍️ Concept stores: Dover Street Market (Ginza branch nearby) — curated designer streetwear',
                '🍦 Japanese soft serve: find black sesame or hojicha flavors at pop-up stands along the boulevard',
                '📚 Spiral Building at Minami-Aoyama: free gallery space inside — interesting art/design exhibitions'
              ]
            }
          ]
        },
        {
          label: 'Afternoon & Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Scramble Square Observatory',
              description: "The Shibuya Scramble Crossing is the most famous intersection on earth — up to 3,000 people surge from all directions simultaneously when the lights change. Experience it at street level (it's gentler than it looks), then head up to Shibuya Sky (the Scramble Square skyscraper's rooftop observatory at 229m) for an aerial view of the crossing and the entire city. In late afternoon, the view from the outdoor rooftop as the city lights turn on and the sky shifts from gold to indigo is unforgettable.",
              details: [
                '🚦 Walk the scramble yourself — it flows organically, just move with the crowd',
                '🏙️ Shibuya Sky observatory: ¥2,000 adults · Book online for timed entry at shibuyasky.jp',
                '🌇 Golden hour hits Shibuya around 6pm in May — the best light show is free',
                '📸 Best ground-level photo spot: the second floor of Mag\'s Park inside the Q-Front building opposite the crossing'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Narisawa — Minami-Aoyama (Michelin 2 Stars)',
              description: "Chef Yoshihiro Narisawa calls his cuisine 'innovative Satoyama' — food that lives at the intersection of Japanese natural philosophy, French technique, and a deep obsession with the ecosystems of Japan's mountains and forests. His bread course is baked tableside in a cast-iron pot and served with a sauce made from soil (yes, edible soil). In May: early summer vegetables, mountain herbs, river fish, and things you couldn't name but will never forget. This is one of the most intellectually interesting restaurants in Asia. Book via Tableall.com or Pocket Concierge — 4-6 weeks in advance.",
              meta: '💰 Lunch: ¥25,000-35,000 per person · 📍 2-6-15 Minami-Aoyama, Minato-ku · Tel: 03-5785-0799 · Tableall.com · Open for lunch Fri-Sun'
            },
            {
              type: '🍽️ Dinner',
              name: 'Florilège — Minami-Aoyama (Michelin 2 Stars)',
              description: "Chef Hiroyasu Kawate's Florilège is one of the most exciting restaurants in Tokyo — an open kitchen counter where 14 guests watch the team compose a 10-12 course tasting menu that is deeply French in technique, deeply Japanese in ingredient and philosophy, and entirely his own in spirit. The wine list is exceptional (natural wines from France and Japan). The energy in the room — intimate, focused, full of pleasure — is unlike anything else in Tokyo. Book via Tableall.com or the restaurant's website directly.",
              meta: '💰 ¥25,000-38,000 per person with wine pairing · 📍 B1F, 2-5-4 Jingumae, Shibuya-ku · Tel: 03-6440-0878 · Book online at florilegetokyo.com'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6763, lng: 139.6993, label: 'Meiji Jingu Shrine', num: 1, cat: 'attraction', desc: 'Ancient forest shrine — 70,000 trees, iris garden in May bloom, profound and serene' },
        { lat: 35.6710, lng: 139.7034, label: 'Takeshita Street, Harajuku', num: 2, cat: 'attraction', desc: 'Kawaii culture explosion — rainbow crepes, cotton candy, pop fashion at its most joyful' },
        { lat: 35.6656, lng: 139.7077, label: 'Omotesando Boulevard', num: 3, cat: 'attraction', desc: 'Tokyo\'s luxury tree-lined avenue — Prada by Herzog & de Meuron, Dior by SANAA' },
        { lat: 35.6672, lng: 139.7142, label: 'Narisawa Restaurant', num: 4, cat: 'food', desc: 'Michelin 2-star — "Innovative Satoyama" cuisine, the most intellectually thrilling meal in Tokyo' },
        { lat: 35.6591, lng: 139.7006, label: 'Shibuya Scramble Crossing', num: 5, cat: 'attraction', desc: 'World\'s most famous pedestrian crossing — walk it, then watch from Shibuya Sky' },
        { lat: 35.6583, lng: 139.7025, label: 'Shibuya Sky Observatory', num: 6, cat: 'attraction', desc: 'Rooftop at 229m — aerial view of the scramble and all of Tokyo at golden hour' },
        { lat: 35.6674, lng: 139.7108, label: 'Florilège, Minami-Aoyama', num: 7, cat: 'food', desc: 'Michelin 2-star — open counter, French-Japanese tasting menu, extraordinary wine list' }
      ]
    },
    {
      num: 4,
      date: '2026-05-23',
      neighborhoods: 'Tsukiji · Imperial Palace · Ginza · Toyosu · Odaiba',
      title: 'Tsukiji Morning, Ginza Afternoon & Omakase Night',
      description: "Today's crown jewel is the evening: an omakase sushi dinner at one of Tokyo's top counters — 20 courses of nigiri composed piece by piece in front of you by a chef who has spent decades perfecting each cut. But first: the legendary Tsukiji Outer Market at its best hour, followed by the Imperial Palace East Gardens in May bloom, and Ginza shopping in the afternoon. teamLab Planets as a digital interlude before the main event.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market — Premium Seafood Breakfast',
              description: "The Inner Market moved to Toyosu in 2018, but the Outer Market remains one of Tokyo's great food experiences — a dense grid of stalls selling the freshest seafood, tamagoyaki, pickles, dashi, and premium ingredients. Arrive at 8:30-9am when stock is freshest. This is a premium grazing experience — budget ¥3,000-4,000 per person and move from stall to stall. The ritual of eating fresh uni (sea urchin) on a spoon from a Tsukiji stall is something you carry with you forever.",
              details: [
                '🦪 Fresh oysters with lemon: ¥300-500 each — look for Hokkaido producers',
                '🍣 Sushi breakfast: several small counters open by 8am — look for fresh maguro and uni',
                '🥚 Tamagoyaki on a stick: ¥150-200, fresh and slightly sweet — Tokyo\'s signature snack',
                '🦑 Grilled scallop with soy butter: ¥500-700 — the smell alone will stop you in your tracks',
                '⏰ Arrive by 8:30am for the freshest selection — many premium items sell out by 10am'
              ]
            },
            {
              title: 'Imperial Palace East Gardens',
              description: "A 15-minute walk from Tsukiji, the Imperial Palace East Gardens are built on the site of Edo Castle's inner compound — the most historically significant land in Japan. In May, the gardens are spectacular: irises in the traditional Japanese garden, peonies and roses along the main paths, and the ancient stone foundations of Edo Castle's towers overgrown with soft moss. The Ninomaru Garden pond reflects the ancient trees above. This is one of Tokyo's most beautiful and underrated spots.",
              details: [
                '🌿 Free admission · Open Tue-Thu, Sat-Sun 9am-4:30pm (closed Monday, Friday)',
                '🌸 May blooms: irises, peonies, roses, and fresh green moss on ancient stone walls',
                '🏯 Edo Castle ruins: the stone keep foundations are as impressive as any castle in Japan',
                '📍 Otemachi Station (multiple subway lines) — entrance at Ote-mon Gate'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza — Serious Shopping',
              description: "Tokyo's most prestigious shopping district — the Fifth Avenue of Asia, but better curated and more interesting. The anchor stores (Mitsukoshi, Matsuya) have excellent basement food halls (depachika) that are themselves worth visiting. Essential stops: Itoya (12-floor stationery paradise), Ginza Six (rooftop garden + every luxury brand), Dover Street Market Ginza (the most interesting fashion concept store in Tokyo), and the craft-focused Okuno Building where independent artists and designers rent tiny galleries.",
              details: [
                '📝 Itoya: 12-floor stationery store — Japanese handmade paper, custom pens, notebooks worth crying over',
                '🛍️ Ginza Six: rooftop garden is free — great city view, and the basement food hall is spectacular',
                '🎨 Dover Street Market Ginza (6-floor): Rei Kawakubo\'s curated fashion universe — the most interesting clothing in Tokyo',
                '☕ Café de l\'Ambre: a legendary coffee bar open since 1948 — aged single-origin, tiny and perfect'
              ]
            },
            {
              title: 'teamLab Planets — Digital Art Immersion',
              description: "Book your timed ticket in advance online — teamLab Planets is the world's most extraordinary immersive art experience and sells out weeks ahead. You enter barefoot and wade through shallow water into rooms where the digital art surrounds you completely: a universe of floating flowers, shimmering light spheres you can bat with your hands, a mirrored room where infinity reflects in every direction. The 'floating flowers' room in spring/summer mode is particularly stunning — cherry blossoms replaced by seasonal arrangements. Absolutely unmissable for families.",
              details: [
                '🎟️ BOOK NOW: teamlab.art/e/planets — timed entry, sells out completely',
                '💰 ¥3,200 adults · ¥1,000 under 15 · Free under 3',
                '🦶 You go barefoot and wade through shallow water — wear easy-to-remove shoes',
                '📍 Shin-Toyosu Station (Yurikamome Line) · 2-min walk',
                '⏰ Afternoon slots (2-4pm) are ideal after Ginza — allow 90 minutes inside'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sushi Sawada — Ginza (Michelin 3 Stars)',
              description: 'One of the most revered omakase sushi restaurants in Japan. Chef Koji Sawada trained at Sushi Kanesaka and his counter in Ginza is a study in restraint and perfection — 12 seats, hinoki cypress counter, zero distraction. The 20-course omakase moves through seasonal nigiri with meticulous pacing: kohada (gizzard shad) aged for precisely the right number of days, chu-toro (medium-fatty tuna) from Oma, uni from Hokkaido in a hand-rolled temaki at the end. Every detail matters. This is sushi as high art. Book via Pocket Concierge or Tableall — 6-8 weeks minimum.',
              meta: '💰 ¥50,000-70,000 per person (omakase, lunch) · 📍 Sato Building 3F, 5-9-19 Ginza · Tel: 03-3571-4711 · Pocket Concierge / hotel concierge booking'
            },
            {
              type: '🍽️ Dinner',
              name: 'Quintessence — Shirokanedai (Michelin 3 Stars)',
              description: "Chef Shuzo Kishida trained under Pierre Gagnaire and his Tokyo restaurant has held three Michelin stars since the first year the guide covered the city — that is a statement almost without parallel. Quintessence is French in discipline but the ingredients are Japanese, the sensibility is quiet and precise, and the tasting menu is a masterclass in what happens when a chef refuses to be distracted from excellence. The dining room is calm, the service is warm, and the wine list is among the finest in Japan. Book via Tableall.com — 6-8 weeks in advance minimum.",
              meta: '💰 ¥45,000-60,000 per person with wine pairing · 📍 1F Garden City Shirokanedai, 6-7-29 Shirokane · Tel: 03-5791-3715 · Tableall.com'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7708, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Premium seafood breakfast — fresh uni on a spoon, tamagoyaki on a stick, grilled scallops' },
        { lat: 35.6852, lng: 139.7528, label: 'Imperial Palace East Gardens', num: 2, cat: 'attraction', desc: 'May iris bloom on ancient Edo Castle grounds — free, beautiful, and deeply historic' },
        { lat: 35.6717, lng: 139.7646, label: 'Ginza District', num: 3, cat: 'attraction', desc: 'Tokyo\'s most refined shopping — Itoya, Ginza Six, Dover Street Market, Café de l\'Ambre' },
        { lat: 35.6726, lng: 139.7701, label: 'Sushi Sawada, Ginza', num: 4, cat: 'food', desc: 'Michelin 3-star omakase counter — sushi as high art, 20 courses of seasonal perfection' },
        { lat: 35.6541, lng: 139.7944, label: 'teamLab Planets, Shin-Toyosu', num: 5, cat: 'attraction', desc: 'The world\'s most extraordinary immersive digital art — BOOK TICKETS NOW, sells out fast' },
        { lat: 35.6349, lng: 139.7262, label: 'Quintessence, Shirokanedai', num: 6, cat: 'food', desc: 'Michelin 3-star French — Tokyo\'s most quietly excellent tasting menu, three stars since day one' }
      ]
    },
    {
      num: 5,
      date: '2026-05-24',
      neighborhoods: 'Nakameguro · Daikanyama · Shibuya · Departure',
      title: 'Farewell Morning — Nakameguro Canal & Final Kaiseki',
      description: "Your last morning in Tokyo belongs to Nakameguro — a neighborhood of narrow canal paths, impeccable coffee shops, and some of the city's most beautiful boutiques. In May, the Meguro River canal is lined with lush green trees and the neighborhood hums with a relaxed, creative energy. Store your bags, take one last long walk, have a final fine farewell lunch, and then make for the airport. Tokyo doesn't let go easily.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nakameguro Canal Walk',
              description: "The Meguro River runs through one of Tokyo's most beautiful residential neighborhoods. The canal-side path is lined with zelkova trees and flanked by independent coffee shops, design boutiques, and excellent restaurants. In May the trees are fully leafed — a green canopy over the water. This walk is the opposite of Shibuya's scramble: narrow, quiet, deeply Tokyo in a different register. Walk from Nakameguro Station south toward Daikanyama — about 1.5km, flat, unhurried.",
              details: [
                '🌿 The Meguro River canal path: 1.5km from Nakameguro to Daikanyama — allow 45 min with coffee stops',
                '☕ Excellent canal-side cafés: Onibus Coffee (single-origin pour-overs), Log Road Daikanyama',
                '📍 Nakameguro Station (Tokyu Toyoko Line / Tokyo Metro Hibiya Line)',
                '🛍️ The boutiques along the canal (concept stores, ceramics, clothing) are among the best in Tokyo'
              ]
            },
            {
              title: 'Daikanyama T-Site — The World\'s Most Beautiful Bookshop',
              description: "A 10-minute walk from Nakameguro, Tsutaya Books Daikanyama is one of the world's great bookstores — a sprawling garden campus with three connected buildings housing books, music, a café, and curated lifestyle products. The architecture is beautiful, the garden between the buildings is peaceful, and the Anjin café (a vintage international magazine library where you drink coffee surrounded by decades of Vogue, National Geographic, and Life) is the perfect final Tokyo moment.",
              details: [
                '📚 Open 7am-2am (café) · Bookshop opens 9am',
                '☕ Anjin café: surrounded by vintage international magazines — coffee in an archive of the 20th century',
                '🌿 The garden campus between buildings: tables outside under mature trees — perfect final morning',
                '🎵 Vinyl record section: curated and eclectic — great last-minute gift for music lovers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Starbucks Reserve Roastery Nakameguro',
              description: 'One of only 6 Reserve Roasteries in the world. The Tokyo location is housed in a stunning 4-floor building right on the Nakameguro canal, designed like a contemporary Japanese teahouse. The specialty coffee is genuinely excellent — not just a brand play. The pastries are Japan-specific (matcha croissants, hojicha lattes). The canal view from the upper terrace with the green May trees overhead is the perfect final Tokyo memory.',
              meta: '💰 ¥700-1,400 · 📍 2-19-23 Aobadai, Meguro (right on the canal) · Opens 7am · Reserve a spot on the upper terrace'
            }
          ]
        },
        {
          label: 'Farewell Lunch & Departure',
          activities: [
            {
              title: 'Head to Airport — Haneda or Narita',
              description: "After farewell lunch, collect your bags from the hotel, and make for the airport. Give yourself generous time — international departures need 3+ hours for check-in and security at Tokyo's airports.",
              details: [
                '✈️ Haneda (HND): Keikyu Line from Shinagawa (~35 min) or Tokyo Monorail from Hamamatsucho (~30 min)',
                '✈️ Narita (NRT): N\'EX from Shinjuku/Tokyo Station — ¥3,250 adult, ~90 min',
                '🚗 Private car (recommended for a family with luggage): book via hotel concierge — ¥15,000-25,000',
                '🛍️ Final gift buying: Tokyo Station\'s Gransta basement is exceptional — Tokyo Banana, matcha KitKats, Toraya wagashi, Shiroi Koibito from Hokkaido'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Lunch',
              name: 'Kikunoi Akasaka — Akasaka (Michelin 2 Stars)',
              description: "The Akasaka branch of the legendary Kikunoi ryotei from Kyoto brings kaiseki to Tokyo in a beautiful traditional setting. Chef Kunio Tsuji\'s cuisine is rooted in the classic Kyoto kaiseki tradition — seasonal, precise, deeply respectful of Japanese culinary heritage — but without the rigidity that sometimes makes traditional kaiseki feel inaccessible. The lunch kaiseki course in May celebrates early summer ingredients: young bamboo, firefly squid, juvenile sweetfish (ayu), plum. The room is serene, the service is warm, and the set menu at lunch is the finest value in Tokyo fine dining. A perfect, meaningful final meal.",
              meta: '💰 Lunch kaiseki: ¥15,000-25,000 per person · 📍 2-4-7 Akasaka, Minato-ku · Tel: 03-3568-6055 · Book via kikunoi.jp or Tableall.com · Closes by 1:30pm last entry'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6413, lng: 139.6986, label: 'Nakameguro Canal', num: 1, cat: 'attraction', desc: 'Tokyo\'s most beautiful canal walk — lush May greenery, coffee shops, boutiques, and calm' },
        { lat: 35.6481, lng: 139.7029, label: 'Starbucks Reserve Roastery Nakameguro', num: 2, cat: 'food', desc: 'World-class coffee on the canal — one of 6 Reserve Roasteries worldwide, perfect final morning' },
        { lat: 35.6484, lng: 139.7003, label: 'Daikanyama T-Site Tsutaya Books', num: 3, cat: 'attraction', desc: 'The world\'s most beautiful bookstore — garden campus, Anjin café, vinyl records' },
        { lat: 35.6726, lng: 139.7365, label: 'Kikunoi Akasaka', num: 4, cat: 'food', desc: 'Michelin 2-star kaiseki — Kyoto tradition in Tokyo, early summer ingredients, a perfect farewell' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station Gransta', num: 5, cat: 'food', desc: 'Best last-minute omiyage: Tokyo Banana, matcha KitKat, Toraya wagashi' },
        { lat: 35.5494, lng: 139.7798, label: 'Haneda Airport (HND)', num: 6, cat: 'attraction', desc: 'Closest airport — 35 min from Shinagawa by Keikyu Line' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Luxury Hotel (per night)', budget: '¥15,000–25,000', midrange: '¥30,000–60,000', luxury: '¥80,000–150,000+' },
    { category: 'Fine Dining (per person per meal)', budget: '¥8,000–15,000', midrange: '¥20,000–35,000', luxury: '¥40,000–70,000' },
    { category: 'Attractions & Experiences', budget: '¥2,000–5,000/day', midrange: '¥5,000–12,000/day', luxury: '¥15,000+/day' },
    { category: 'Transport (metro + taxis)', budget: '¥1,000–2,000/day', midrange: '¥2,000–4,000/day', luxury: '¥5,000+ (private car)' },
    { category: '5-Day Total (3-4 people, fine dining)', budget: '¥400,000–600,000', midrange: '¥800,000–1,500,000', luxury: '¥2,000,000+' }
  ],

  practicalInfo: [
    {
      title: '🍽️ Restaurant Reservations — Act Now',
      items: [
        'Use Tableall.com and Pocket Concierge for English-language bookings at Michelin-starred Tokyo restaurants',
        'Nihonryori RyuGin and Quintessence: book 6-8 weeks in advance minimum',
        'Narisawa and Florilège: 4-6 weeks, sometimes available 2-3 weeks out',
        'Sushi Sawada: 6+ weeks via Pocket Concierge or hotel concierge',
        'Your hotel concierge (Park Hyatt, Aman, Peninsula) can often access reservations that the public cannot — use them'
      ]
    },
    {
      title: '🏨 Recommended Hotels for This Trip',
      items: [
        'Park Hyatt Tokyo (Shinjuku): floors 41-52, "Lost in Translation" hotel, ¥60,000-90,000/night — the classic luxury Tokyo choice',
        'Aman Tokyo (Otemachi): minimalist Japanese luxury, temple-like calm, ¥120,000-200,000/night — the finest hotel in the city',
        'The Peninsula Tokyo (Hibiya): in-house Michelin-starred restaurant, perfectly located for Ginza and Tsukiji, ¥70,000-120,000/night',
        'Mandarin Oriental Tokyo (Nihonbashi): 38th-floor location, stunning city views, impeccable service, ¥80,000-130,000/night',
        'All four hotels have concierge services that can assist with restaurant bookings — this alone is worth the price premium'
      ]
    },
    {
      title: '✈️ Getting There & Around',
      items: [
        'Haneda Airport (HND): closest to Tokyo — 35 min by Keikyu Line from Shinagawa, or private car (¥15,000-25,000)',
        'Narita Airport (NRT): 60-90 min via N\'EX express — ¥3,250/adult, ¥1,630/child to central Tokyo',
        'IC Card (Suica/Pasmo): get at the airport, add ¥5,000-10,000 per person — covers all trains, buses, and convenience stores',
        'Taxis: plentiful, clean, metered, always honest — essential for evenings after fine dining when you\'re not counting coins',
        'Private car service: book via hotel concierge for airport transfers and special evenings'
      ]
    },
    {
      title: '🛍️ Shopping Guide — Fine Goods to Bring Home',
      items: [
        'Ginza Itoya (stationery): Japanese handmade washi paper, Mont Blanc pens, hand-bound notebooks',
        'Nakamise (Asakusa): genuine quality traditional items — tenugui, fans, lacquerware, ningyo-yaki',
        'Ginza Six basement food hall: premium Japanese pantry — yuzu kosho, dashi packs, fine matcha, regional sake',
        'Isetan Shinjuku (basement depachika): the finest food floor in Tokyo — wagashi, bento, premium produce',
        'Tokyo Station Gransta: Tokyo Banana (custard cake), Toraya yokan, Shiroi Koibito, matcha KitKats — the essential omiyage'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ Fulfillment complete!');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('File:', result.filePath);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
