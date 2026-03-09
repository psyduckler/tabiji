const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772493708105_mmggtc',
  email: 'm.maltenfort@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-31',
  endDate: '2026-04-12',
  groupSize: 2,
  requests: 'Onsen or ryokan (2 days min), whiskey/beer/sake tasting, bluefin tuna, bullet train, hiking for one day, 2 days in tokyo at the end of the trip for shopping, head/scalp massage. Public transit only.'
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossoms, Hot Springs & Hidden Flavors of Japan',
  subtitle: '12 days through Tokyo, Kyoto, Hakone & Osaka — sake, onsen, bullet trains & sakura for two',
  description: "This trip lands you in Japan at the most magical time of year: cherry blossom season. From the neon-lit streets of Tokyo to the ancient temples of Kyoto draped in pink petals, the steaming onsen of Hakone with views of Mt. Fuji, and the street food paradise of Osaka — every day is a new world. You'll soak in ryokan hot springs, taste the freshest bluefin tuna at Toyosu Market, ride the bullet train through countryside blanketed in sakura, hike volcanic trails, and end with two full days of Tokyo shopping. All on public transit, no Japanese required.",
  duration: '12 nights',
  dates: 'Mar 31 – Apr 12, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Couples · Foodies · Adventure Seekers',
  highlights: [
    'Cherry blossoms in full bloom across Tokyo & Kyoto',
    'Two nights at a traditional ryokan with private onsen in Hakone',
    'Bluefin tuna breakfast at Toyosu Fish Market',
    'Sake, whiskey & craft beer tastings in Kyoto\'s Fushimi district',
    'Bullet train (shinkansen) through sakura-lined countryside',
    'Mt. Kintoki day hike with views of Mt. Fuji',
    'Osaka street food crawl through Dotonbori',
    'Head spa & scalp massage in Shibuya',
    'Two full days of Tokyo shopping in Harajuku, Shibuya & Akihabara'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Season', text: 'You\'re arriving at peak sakura time! Tokyo\'s blossoms typically reach full bloom around March 26 and the petals linger into early April. Kyoto blooms a few days later. Expect stunning hanami (flower viewing) everywhere — parks, temples, rivers, and even convenience store parking lots.' },
    { title: '🚄 Getting Around', text: 'Get a 14-day Japan Rail Pass (¥50,000/~$330) — it covers all shinkansen (bullet trains), JR local trains, and many buses. In cities, use a Suica or Pasmo IC card (tap-and-go) for subway, buses, and even convenience stores. Google Maps works perfectly for transit directions in Japan.' },
    { title: '🏯 Language Tips', text: 'English signage is common in major stations and tourist areas. Google Translate\'s camera mode reads Japanese signs instantly. Most restaurants have picture menus or plastic food displays. Learn three phrases: "Sumimasen" (excuse me), "Arigatou" (thanks), and "Oishi" (delicious) — you\'ll use them constantly.' },
    { title: '💴 Money & Tipping', text: 'Japan is still partly cash-based — carry ¥10,000-20,000 ($65-130) for small restaurants, shrines, and markets. 7-Eleven ATMs accept foreign cards. Tipping is NOT customary and can actually cause confusion. Tax-free shopping is available at most department stores (bring your passport).' },
    { title: '♨️ Onsen Etiquette', text: 'Wash thoroughly before entering the bath. No swimsuits — onsen are enjoyed nude. Small towels stay out of the water (fold on your head). Tattoos: some onsen restrict them, but private baths (kashikiri) have no rules. Your ryokan will have yukata robes to wear around the property.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-31',
      neighborhoods: 'Narita/Haneda · Shinjuku · Shibuya',
      title: 'Welcome to Tokyo — Neon, Ramen & Cherry Blossoms',
      description: "Touch down in Tokyo and immediately feel the energy. Check into your hotel in Shinjuku — the city\'s vibrant heart — grab your first bowl of ramen, and witness the famous Shibuya Crossing at night. The cherry trees are in bloom and Tokyo is glowing.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle into Shinjuku',
              description: 'After landing at Narita or Haneda, take the Narita Express or Airport Limousine Bus to Shinjuku. Drop your bags, activate your Japan Rail Pass at the JR ticket office, and pick up Suica IC cards from any station machine.',
              details: [
                '✈️ Narita Express to Shinjuku: ~80 min (covered by JR Pass)',
                '🏨 Stay in Shinjuku for walkable nightlife, food, and transit access',
                '💳 Get Suica cards from any JR station — load ¥3,000 each to start'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Late Lunch',
              name: 'Fuunji (風雲児)',
              description: 'One of Tokyo\'s best tsukemen (dipping ramen) shops, right near Shinjuku station. Rich, creamy fish-pork broth with thick chewy noodles. The line moves fast.',
              meta: '💰 $ · 📍 Shinjuku 3-chome, 2 min from south exit · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Nightlife Walk',
              description: 'Take the JR line one stop to Shibuya and witness the world\'s busiest pedestrian crossing. Stand on the Shibuya Sky observation deck or the Starbucks above the crossing for the full effect. Then explore the backstreets of Nonbei Yokocho (Drunkard\'s Alley).',
              details: [
                '📸 Best photo spot: Shibuya Sky rooftop (¥2,000, book online)',
                '🍺 Nonbei Yokocho — tiny alley of 40+ cramped bars, very atmospheric',
                '🌸 Sakura illuminations at nearby Meguro River (10 min walk)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Uobei Shibuya (魚べい)',
              description: 'High-tech conveyor belt sushi where you order on a tablet and plates zoom to your seat on a mini bullet train. Fun, fresh, and absurdly cheap for the quality.',
              meta: '💰 $ · 📍 Shibuya Dogenzaka · Great for jet-lagged first night'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'attraction', desc: 'World\'s busiest station — your home base' },
        { lat: 35.6897, lng: 139.7005, label: 'Fuunji', num: 2, cat: 'food', desc: 'Top-tier tsukemen near Shinjuku south exit' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 3, cat: 'attraction', desc: 'The iconic scramble crossing' },
        { lat: 35.6580, lng: 139.6985, label: 'Nonbei Yokocho', num: 4, cat: 'food', desc: 'Tiny atmospheric bar alley in Shibuya' },
        { lat: 35.6536, lng: 139.7038, label: 'Meguro River Sakura', num: 5, cat: 'attraction', desc: 'Cherry blossom-lined river, stunning at night' }
      ]
    },
    {
      num: 2,
      date: '2026-04-01',
      neighborhoods: 'Toyosu · Asakusa · Ueno · Akihabara',
      title: 'Bluefin Tuna, Temples & Electric Town',
      description: "Start with the freshest fish on earth at Toyosu Market, then explore Tokyo\'s traditional side in Asakusa before diving into the otaku wonderland of Akihabara. End with cherry blossoms in Ueno Park — Tokyo\'s most beloved hanami spot.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Toyosu Fish Market — Bluefin Tuna Breakfast',
              description: 'Head to Toyosu Market early for the freshest sushi breakfast of your life. The tuna auction viewing gallery opens at 5:45am, but the restaurant floor is worth it even without the auction. Order the honmaguro (bluefin tuna) set — otoro, chutoro, and akami.',
              details: [
                '🐟 Sushi Dai and Daiwa Sushi are the most famous — lines start at 5am',
                '🍣 For shorter waits, try Sushi Yoshitake or any stall on the restaurant floor',
                '🚇 Yurikamome line to Shijo-mae station, direct from Shimbashi'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Breakfast',
              name: 'Sushi Dai (寿司大)',
              description: 'Legendary Toyosu sushi counter — the omakase set includes multiple cuts of bluefin tuna, uni, and whatever\'s freshest that morning. Worth every minute of the wait.',
              meta: '💰 $$ · 📍 Toyosu Market Building 6, 3F · Cash preferred · Opens 5:30am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Senso-ji Temple & Asakusa',
              description: 'Tokyo\'s oldest and most visited temple is a sensory overload — incense smoke, the massive red Kaminarimon gate, and Nakamise shopping street lined with traditional snacks and souvenirs. Try fresh ningyo-yaki (custard-filled cakes) and melon pan.',
              details: [
                '⛩️ Free entry · The main hall and five-story pagoda are stunning',
                '🛍️ Nakamise Street — 200m of traditional souvenir shops',
                '📸 Best photos early morning or late afternoon when crowds thin'
              ]
            },
            {
              title: 'Ueno Park Cherry Blossoms',
              description: 'Walk from Asakusa to Ueno Park (20 min) for Tokyo\'s most famous hanami spot. Over 1,000 cherry trees line the central pathway. Grab a bento and a beer from a convenience store and picnic under the blossoms like a local.',
              details: [
                '🌸 1,000+ cherry trees — peak bloom likely early April',
                '🍱 Konbini (7-Eleven/Lawson) bento boxes make perfect picnic food',
                '🍺 Drinking in parks is totally normal and encouraged during hanami!'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Akihabara Electric Town',
              description: 'Explore Tokyo\'s anime, gaming, and electronics mecca. Multi-story arcades, retro game shops, manga stores, and gachapon (capsule toy) machines everywhere. Even if you\'re not into anime, the sensory overload is unforgettable.',
              details: [
                '🕹️ Super Potato — retro gaming paradise across 5 floors',
                '🎮 Sega and Taito arcades — try UFO catchers and rhythm games',
                '📍 5 min walk from JR Akihabara station'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kanda Matsuya (神田まつや)',
              description: 'A 130-year-old soba noodle shop near Akihabara. Hand-cut buckwheat noodles served cold with dipping sauce or hot in broth. Simple, perfect, historic.',
              meta: '💰 $ · 📍 Kanda Sudacho · 10 min walk from Akihabara'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6421, lng: 139.7812, label: 'Toyosu Fish Market', num: 1, cat: 'food', desc: 'World\'s largest fish market — bluefin tuna heaven' },
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 2, cat: 'attraction', desc: 'Tokyo\'s oldest temple with iconic thunder gate' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 3, cat: 'attraction', desc: '1,000+ cherry trees — Tokyo\'s top hanami spot' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 4, cat: 'attraction', desc: 'Electric Town — anime, games, and electronics' },
        { lat: 35.6957, lng: 139.7710, label: 'Kanda Matsuya', num: 5, cat: 'food', desc: '130-year-old soba noodle shop' }
      ]
    },
    {
      num: 3,
      date: '2026-04-02',
      neighborhoods: 'Kyoto Station · Higashiyama · Gion',
      title: 'Bullet Train to Kyoto — Temples & Geisha District',
      description: "Board the shinkansen and watch the Japanese countryside blur past at 300km/h. In just over two hours, you\'re in Kyoto — Japan\'s cultural soul. Spend the afternoon wandering ancient temples draped in cherry blossoms and the evening in the atmospheric geisha district of Gion.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Kyoto',
              description: 'Take the Tokaido Shinkansen from Tokyo Station to Kyoto — one of the world\'s great train journeys. Sit on the right side (seats D/E) for views of Mt. Fuji on a clear day. The Nozomi takes 2h15m, but your JR Pass covers the Hikari (2h40m).',
              details: [
                '🚄 Hikari shinkansen: ~2h 40min (JR Pass covered)',
                '🗻 Mt. Fuji visible on the right side about 45 min in',
                '🍱 Buy an ekiben (station bento) for the ride — Tokyo Station has 200+ varieties'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kiyomizu-dera Temple',
              description: 'One of Kyoto\'s most spectacular temples, perched on a hillside with a massive wooden terrace overlooking the city. In early April, the surrounding cherry trees create a pink cloud effect. The approach streets (Sannen-zaka and Ninen-zaka) are lined with traditional shops.',
              details: [
                '⛩️ ¥400 entry · Open 6am-6pm (extended hours during sakura)',
                '🌸 Evening illumination during cherry blossom season is magical',
                '🛍️ Sannen-zaka and Ninen-zaka — charming preserved streets below the temple'
              ]
            },
            {
              title: 'Philosopher\'s Path (Tetsugaku no Michi)',
              description: 'A 2km canal-side path lined with hundreds of cherry trees — one of Kyoto\'s most iconic sakura spots. Walk slowly, stop for matcha at a canal-side café, and let the petals drift onto your shoulders.',
              details: [
                '🌸 Hundreds of cherry trees create a pink tunnel over the canal',
                '🍵 Stop at Yojiya Café for matcha with a garden view',
                '📍 Runs between Ginkaku-ji and Nanzen-ji temples'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion District Evening Walk',
              description: 'As dusk falls, walk through Gion — Kyoto\'s famous geisha (geiko) district. The wooden machiya townhouses, soft lantern light, and the possibility of spotting a geiko or maiko in full regalia make this one of Japan\'s most atmospheric experiences.',
              details: [
                '🏮 Hanamikoji Street — the main geisha street, stunning at dusk',
                '📸 Be respectful — don\'t chase or block geiko/maiko for photos',
                '🌸 Shirakawa canal area has weeping cherry trees lit up at night'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa Restaurant',
              description: 'Intimate kaiseki-style restaurant in the heart of Gion. Multi-course traditional Kyoto cuisine using seasonal ingredients — spring means bamboo shoots, sakura mochi, and cherry blossom-themed presentation.',
              meta: '💰 $$$ · 📍 Gion, Higashiyama-ku · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0028, lng: 135.7686, label: 'Kyoto Station', num: 1, cat: 'attraction', desc: 'Arrive via shinkansen — impressive modern architecture' },
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 2, cat: 'attraction', desc: 'Hilltop temple with iconic wooden terrace' },
        { lat: 35.0272, lng: 135.7947, label: 'Philosopher\'s Path', num: 3, cat: 'attraction', desc: 'Cherry blossom-lined canal walk' },
        { lat: 35.0037, lng: 135.7748, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Historic geisha district — atmospheric at night' },
        { lat: 35.0043, lng: 135.7757, label: 'Gion Kappa', num: 5, cat: 'food', desc: 'Seasonal kaiseki in the heart of Gion' }
      ]
    },
    {
      num: 4,
      date: '2026-04-03',
      neighborhoods: 'Fushimi · Arashiyama · Nishiki Market',
      title: 'Sake District, Bamboo Forest & Market Grazing',
      description: "Today you explore Kyoto\'s best flavors. Start in Fushimi — Japan\'s premier sake-brewing district — for morning tastings. Then head to the ethereal bamboo groves of Arashiyama, and end with a street food crawl through the legendary Nishiki Market.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Sake District — Brewery Tastings',
              description: 'Fushimi is to sake what Bordeaux is to wine. This historic brewing district has been producing Japan\'s finest sake for over 600 years. Visit Gekkeikan Okura Sake Museum and the Kizakura Kappa Country brewery for tastings, tours, and history.',
              details: [
                '🍶 Gekkeikan Okura Museum: ¥600, includes 3 tastings',
                '🍶 Kizakura Kappa Country: free museum, sake + beer tastings ¥300-500',
                '🚃 Keihan line to Chushojima station, 30 min from central Kyoto',
                '🥃 Also try Torisei restaurant for sake flights paired with yakitori'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'Walk through the towering bamboo forest of Arashiyama — one of the most photographed places in Japan. The bamboo stalks creak and sway overhead, creating an otherworldly atmosphere. Arrive early or late to avoid peak crowds.',
              details: [
                '🎋 Free entry · Best light in early morning or late afternoon',
                '🐒 Iwatayama Monkey Park is nearby — wild monkeys with city views (¥550)',
                '🌉 Togetsukyo Bridge with cherry trees along the Katsura River'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Arashiyama Yoshimura',
              description: 'Handmade soba noodles with a view of Togetsukyo Bridge and the cherry blossom-lined Katsura River. The tempura soba set is perfect.',
              meta: '💰 $$ · 📍 Overlooking Togetsukyo Bridge'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nishiki Market — Kyoto\'s Kitchen',
              description: 'Five blocks of covered market stalls selling everything from fresh tofu to grilled octopus on a stick. Graze your way through — this is dinner, snack by snack. Don\'t miss the tamagoyaki (sweet rolled omelette), yuba (tofu skin), and matcha everything.',
              details: [
                '🦑 Grilled octopus balls, fresh mochi, pickles, and wagashi',
                '🍵 Matcha soft serve from Nishiki Sato',
                '🔪 Some stalls offer knife-sharpening for the cooks in your life',
                '📍 Nishiki-koji, between Teramachi and Takakura streets'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Evening',
              name: 'Yoramu Bar (Sake Bar)',
              description: 'Tiny, legendary sake bar in Gion run by an Israeli sake sommelier who speaks English. Incredible curated flights with expert explanations. Perfect way to deepen your sake education.',
              meta: '💰 $$ · 📍 Gion, near Yasaka Shrine · Seats 8, walk-in only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9278, lng: 135.7594, label: 'Fushimi Sake District', num: 1, cat: 'attraction', desc: 'Historic sake brewing district — 600+ years of craft' },
        { lat: 34.9290, lng: 135.7600, label: 'Gekkeikan Okura Museum', num: 2, cat: 'attraction', desc: 'Sake museum with tastings included' },
        { lat: 35.0173, lng: 135.6714, label: 'Arashiyama Bamboo Grove', num: 3, cat: 'attraction', desc: 'Ethereal bamboo forest — iconic Kyoto' },
        { lat: 35.0045, lng: 135.7651, label: 'Nishiki Market', num: 4, cat: 'food', desc: 'Kyoto\'s kitchen — 5 blocks of food stalls' },
        { lat: 35.0040, lng: 135.7760, label: 'Yoramu Sake Bar', num: 5, cat: 'food', desc: 'Legendary English-friendly sake bar' }
      ]
    },
    {
      num: 5,
      date: '2026-04-04',
      neighborhoods: 'Fushimi Inari · Northern Higashiyama · Pontocho',
      title: 'Thousand Torii Gates, Golden Pavilion & Whiskey Night',
      description: "Hike through the mesmerizing tunnel of 10,000 vermillion torii gates at Fushimi Inari, visit the golden Kinkaku-ji pavilion reflected in its mirror lake, and end with a whiskey tasting in Kyoto\'s atmospheric Pontocho alley.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Shrine — 10,000 Torii Gates',
              description: 'The iconic tunnel of thousands of vermillion torii gates winding up Mt. Inari is Kyoto\'s most visited site. Go early (before 8am) for a nearly empty trail. The full loop to the summit takes about 2-3 hours and offers incredible city views.',
              details: [
                '⛩️ Free entry · Open 24 hours',
                '🥾 Full circuit to summit: ~2-3 hours, 4km',
                '🦊 The fox statues are messengers of the deity Inari',
                '📸 Early morning = empty gates = magical photos'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: 'The gold-leaf covered pavilion reflected perfectly in its mirror pond is one of the most arresting sights in Japan. Cherry trees in the surrounding garden add pink accents to the gold. Even if you\'ve seen a thousand photos, the real thing is breathtaking.',
              details: [
                '🏯 ¥500 entry · Your ticket is a beautiful calligraphy charm',
                '📸 The reflection in the pond is the classic shot — morning light is best',
                '🚌 Bus 205 from Kyoto Station, or bus 12 from Fushimi Inari area'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Ippudo Ramen Kyoto',
              description: 'Kyoto outpost of Japan\'s most famous tonkotsu ramen chain. Rich, creamy pork broth with thin noodles — the perfect recharge after a morning of shrine hiking.',
              meta: '💰 $ · 📍 Nishiki-koji area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley & Whiskey Tasting',
              description: 'Pontocho is a narrow, atmospheric alley running parallel to the Kamo River, lined with restaurants and bars. Many places have riverside terraces (kawadoko) that open in warmer months. End the night at a Japanese whiskey bar.',
              details: [
                '🏮 One of Kyoto\'s most photogenic streets — lantern-lit at dusk',
                '🥃 Bar K6 — legendary Kyoto cocktail bar since 1946',
                '🥃 Nokishita 711 — excellent Japanese whiskey selection'
              ]
            }
          ],
          meals: [
            {
              type: '🥃 Dinner & Drinks',
              name: 'Nokishita 711',
              description: 'An intimate whiskey bar tucked away near Pontocho with an extraordinary collection of Japanese whiskeys — Yamazaki, Hakushu, Nikka, and rare small-batch bottles. The bartender crafts perfect highballs and old fashioneds.',
              meta: '💰 $$$ · 📍 Near Pontocho, Nakagyo-ku · Open from 6pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Shrine', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates on Mt. Inari' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 2, cat: 'attraction', desc: 'Gold-leaf pavilion with mirror pond' },
        { lat: 35.0050, lng: 135.7705, label: 'Pontocho Alley', num: 3, cat: 'attraction', desc: 'Atmospheric riverside restaurant alley' },
        { lat: 35.0048, lng: 135.7700, label: 'Nokishita 711', num: 4, cat: 'food', desc: 'Japanese whiskey bar with rare bottles' }
      ]
    },
    {
      num: 6,
      date: '2026-04-05',
      neighborhoods: 'Hakone-Yumoto · Gora · Owakudani',
      title: 'To Hakone — Volcanic Valleys & Your First Onsen Soak',
      description: "Leave Kyoto and head to Hakone — Japan\'s premier hot spring resort town nestled in the mountains near Mt. Fuji. Check into your ryokan, explore volcanic landscapes, and end the day soaking in a steaming outdoor onsen as the sun sets over the mountains.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Odawara, then Hakone',
              description: 'Take the shinkansen from Kyoto to Odawara (about 2 hours), then switch to the charming Hakone Tozan Railway — a switchback mountain train that climbs through forests and over bridges. Get the Hakone Free Pass for unlimited transport in the Hakone area.',
              details: [
                '🚄 Hikari shinkansen Kyoto → Odawara: ~2 hours (JR Pass)',
                '🚃 Hakone Tozan Railway: Odawara → Gora, 40 min',
                '🎫 Hakone Free Pass: ¥5,000 for 2 days — covers all Hakone transport',
                '🧳 Send luggage ahead via takkyubin (hotel can arrange) to travel light'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Owakudani Volcanic Valley',
              description: 'Take the Hakone Ropeway up to Owakudani — an active volcanic zone with steaming sulphur vents and bubbling hot springs. On clear days, Mt. Fuji dominates the horizon. Eat the famous black eggs (kuro-tamago) boiled in volcanic hot springs — each one adds 7 years to your life!',
              details: [
                '🥚 Black eggs: ¥500 for 5 — boiled in 80°C sulphur springs',
                '🗻 Mt. Fuji views on clear days are absolutely stunning',
                '🚡 Hakone Ropeway from Gora station, covered by Free Pass'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ryokan Check-in & Onsen',
              description: 'Check into your ryokan in Hakone-Yumoto or Gora. Change into yukata robes, explore the property, and then head to the onsen. Most ryokans have both indoor and outdoor (rotenburo) baths. The outdoor bath at sunset, surrounded by mountains, is pure bliss.',
              details: [
                '♨️ Recommended: Senkyoro (private onsen available) or Hoeiso (river views)',
                '👘 Yukata and slippers provided — wear them everywhere on the property',
                '🍽️ Kaiseki dinner included — multi-course seasonal feast in your room'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ryokan Kaiseki Dinner',
              description: 'Your ryokan will serve an exquisite multi-course kaiseki dinner — often 10-12 small dishes featuring seasonal ingredients, beautifully presented. Expect spring bamboo shoots, sashimi, grilled fish, hot pot, and sakura-themed desserts.',
              meta: '💰 Included with stay · 📍 Served in your room or private dining area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2329, lng: 139.1060, label: 'Hakone-Yumoto Station', num: 1, cat: 'attraction', desc: 'Gateway to Hakone — hot spring town' },
        { lat: 35.2471, lng: 139.0641, label: 'Owakudani', num: 2, cat: 'attraction', desc: 'Volcanic valley with black eggs and Fuji views' },
        { lat: 35.2440, lng: 139.0716, label: 'Gora', num: 3, cat: 'attraction', desc: 'Hakone\'s cultural center with art museums' },
        { lat: 35.2329, lng: 139.1060, label: 'Ryokan Area', num: 4, cat: 'attraction', desc: 'Traditional Japanese inns with hot springs' }
      ]
    },
    {
      num: 7,
      date: '2026-04-06',
      neighborhoods: 'Mt. Kintoki · Lake Ashi · Hakone Shrine',
      title: 'Mountain Hiking, Lake Cruise & Torii in the Water',
      description: "Your hiking day! Summit Mt. Kintoki for panoramic Mt. Fuji views, then descend to Lake Ashi for a pirate ship cruise and visit the iconic lakeside torii gate of Hakone Shrine. Return to the ryokan for one more glorious onsen evening.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Mt. Kintoki (Kintokiyama) Day Hike',
              description: 'Mt. Kintoki (1,212m) is Hakone\'s best hike — a moderate 3-4 hour round trip with one of the most spectacular Mt. Fuji views in Japan. The trail winds through forest before opening up to a dramatic summit panorama. Bring water and snacks.',
              details: [
                '🥾 Round trip: 3-4 hours, moderate difficulty',
                '🗻 The Fuji view from the summit is jaw-dropping on clear days',
                '🚌 Bus from Hakone-Yumoto to Kintoki trailhead (Kintoki Tozanguchi), 30 min',
                '👟 Trail is well-marked but steep in sections — proper shoes recommended'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Ashi Pirate Ship Cruise',
              description: 'Board one of Hakone\'s quirky pirate ship replicas for a scenic cruise across Lake Ashi. On clear days, Mt. Fuji towers above the lake\'s far shore. The cruise connects Togendai to Hakone-machi/Moto-Hakone.',
              details: [
                '🚢 Covered by Hakone Free Pass · ~30 min cruise',
                '🗻 Fuji views from the deck (weather permitting)',
                '📸 The pirate ships look ridiculous and that\'s part of the fun'
              ]
            },
            {
              title: 'Hakone Shrine & Lakeside Torii',
              description: 'The vermillion torii gate standing in the waters of Lake Ashi is one of Japan\'s most photographed scenes. The shrine itself is set in ancient cedar forest. Walk down to the lakeside for the iconic gate-and-Fuji shot.',
              details: [
                '⛩️ Free entry · The lakeside torii is a 5 min walk from the main shrine',
                '🌲 Ancient cedar-lined approach path is incredibly atmospheric',
                '📸 Best light for the lakeside torii: morning or late afternoon'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Amazake-chaya',
              description: 'A 400-year-old teahouse on the old Tokaido highway serving amazake (sweet rice drink) and mochi by a wood fire. One of the most atmospheric stops in Hakone.',
              meta: '💰 $ · 📍 Old Tokaido Road between Moto-Hakone and Hatajuku'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Ryokan Onsen & Kaiseki',
              description: 'Your last night in the ryokan — make the most of it. Soak in the outdoor bath under the stars, savor another kaiseki dinner, and sleep on your futon to the sound of the mountain stream.',
              details: [
                '♨️ Evening onsen under the stars is the ultimate Japan experience',
                '🍶 Ask for local jizake (regional sake) with dinner',
                '😴 Futon sleeping on tatami — surprisingly comfortable'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ryokan Kaiseki (Night 2)',
              description: 'Second night kaiseki — the chef will prepare completely different dishes. Spring specialties may include sakura shrimp, mountain vegetables, and Hakone-sourced tofu.',
              meta: '💰 Included · 📍 Your ryokan'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2751, lng: 138.9992, label: 'Mt. Kintoki Summit', num: 1, cat: 'attraction', desc: 'Best Fuji views in Hakone — moderate 3-4hr hike' },
        { lat: 35.2050, lng: 139.0220, label: 'Lake Ashi', num: 2, cat: 'attraction', desc: 'Scenic lake with pirate ship cruises' },
        { lat: 35.2083, lng: 139.0328, label: 'Hakone Shrine', num: 3, cat: 'attraction', desc: 'Famous torii gate standing in the lake' },
        { lat: 35.2130, lng: 139.0380, label: 'Amazake-chaya', num: 4, cat: 'food', desc: '400-year-old teahouse on the old Tokaido road' }
      ]
    },
    {
      num: 8,
      date: '2026-04-07',
      neighborhoods: 'Osaka · Dotonbori · Shinsekai · Namba',
      title: 'Osaka — Japan\'s Kitchen & Street Food Paradise',
      description: "Leave Hakone and head to Osaka — Japan\'s most food-obsessed city. The local motto is \'kuidaore\' (eat until you drop), and today you\'ll understand why. From takoyaki to okonomiyaki, Osaka\'s street food scene is legendary.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hakone to Osaka',
              description: 'Take the Hakone Tozan Railway back to Odawara, then shinkansen to Shin-Osaka. Drop bags at your hotel near Namba/Dotonbori — the heart of Osaka\'s food and entertainment district.',
              details: [
                '🚄 Odawara → Shin-Osaka: ~2.5 hours by Hikari shinkansen',
                '🚇 Midosuji line from Shin-Osaka to Namba: 15 min',
                '🏨 Stay near Namba/Dotonbori for walkable food access'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dotonbori Street Food Crawl',
              description: 'Osaka\'s most famous street — a neon-lit canal-side strip of restaurants, food stalls, and giant mechanical signs (the Glico Running Man!). Eat your way through: takoyaki, okonomiyaki, gyoza, kushikatsu, and more.',
              details: [
                '🐙 Takoyaki (octopus balls): Try Kukuru or Wanaka — crispy outside, molten inside',
                '🥞 Okonomiyaki (savory pancake): Mizuno or Fukutaro for the best',
                '🍢 Kushikatsu (deep-fried skewers): Daruma — never double-dip!',
                '📸 The Glico Running Man sign is Osaka\'s Times Square'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai — Retro Osaka',
              description: 'Explore Osaka\'s wonderfully retro Shinsekai district, dominated by the Tsutenkaku Tower. The area is famous for kushikatsu (deep-fried skewers) and has a nostalgic, slightly rough-around-the-edges charm. Grab craft beers at a local standing bar.',
              details: [
                '🗼 Tsutenkaku Tower observation deck: ¥900',
                '🍺 Craft beer: Marca Brewing or Craft Beer Base in nearby Tennoji',
                '🎮 Retro game centers and jan-ken (rock-paper-scissors) machines everywhere'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Toyo (トヨ) — Shinsekai Seafood Stand',
              description: 'A legendary open-air seafood stall in Shinsekai where the chef slices sashimi with theatrical flair. Famous for insanely fresh tuna, uni, and scallops at street-food prices.',
              meta: '💰 $$ · 📍 Shinsekai, near Tsutenkaku · Cash only · Standing only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori', num: 1, cat: 'food', desc: 'Osaka\'s neon-lit street food paradise' },
        { lat: 34.6523, lng: 135.5063, label: 'Shinsekai', num: 2, cat: 'attraction', desc: 'Retro district with kushikatsu and Tsutenkaku Tower' },
        { lat: 34.6686, lng: 135.5015, label: 'Namba Area', num: 3, cat: 'attraction', desc: 'Osaka\'s buzzing entertainment hub' },
        { lat: 34.6525, lng: 135.5064, label: 'Toyo Seafood Stand', num: 4, cat: 'food', desc: 'Legendary street sashimi in Shinsekai' }
      ]
    },
    {
      num: 9,
      date: '2026-04-08',
      neighborhoods: 'Osaka Castle · Kuromon Market · Amerikamura',
      title: 'Osaka Castle, Market Feasting & Craft Beer',
      description: "Explore Osaka\'s magnificent castle surrounded by cherry blossoms, feast through the \'Kitchen of Osaka\' at Kuromon Market, and discover the city\'s creative side in Amerikamura — Japan\'s answer to Brooklyn.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: 'Osaka Castle is stunning year-round, but during cherry blossom season it\'s extraordinary. The Nishinomaru Garden (¥350) has 300 cherry trees with the castle tower as a backdrop. Climb the castle for panoramic city views.',
              details: [
                '🏯 Castle tower entry: ¥600 · Open 9am-5pm',
                '🌸 Nishinomaru Garden: 300 cherry trees framing the castle — peak photo spot',
                '🚇 Tanimachi 4-chome station, 10 min walk'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kuromon Market',
              description: 'Known as \'Osaka\'s Kitchen\', this 600m covered market has been feeding the city for over 170 years. Sample fresh sashimi, grilled seafood, tamagoyaki, and seasonal fruits. It\'s less touristy than Nishiki and more focused on quality.',
              details: [
                '🦀 Giant grilled crab legs, fresh uni, and otoro sashimi',
                '🍓 Japanese strawberries in spring are absurdly sweet',
                '🔪 Great for Japanese kitchen knives — several specialty shops'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Kuromon Market Grazing',
              description: 'Don\'t sit down for lunch — graze your way through the market. Budget ¥2,000-3,000 per person for a stomach-busting tour of Japan\'s best seafood, grilled meats, and seasonal treats.',
              meta: '💰 $$ · 📍 Kuromon Market, Chuo-ku · Most stalls cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Amerikamura & Craft Beer',
              description: 'Osaka\'s creative youth district — think vintage shops, street art, and independent bars. It\'s the perfect place for craft beer hopping. End at a standing bar (tachinomiya) for the quintessential Osaka drinking experience.',
              details: [
                '🍺 Craft Beer Base — excellent local and Japanese craft brews',
                '🍺 Beer Belly — tiny taproom with rotating Japanese craft beers',
                '🛍️ Vintage clothing stores rival Tokyo\'s Shimokitazawa'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ajinoya (味乃家)',
              description: 'One of Osaka\'s finest okonomiyaki restaurants. Watch the chef build your savory pancake on the teppan grill right in front of you. The pork-shrimp-squid mix with extra cheese is legendary.',
              meta: '💰 $$ · 📍 Namba, near Dotonbori · Often a short wait'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle spectacular during cherry blossom season' },
        { lat: 34.6688, lng: 135.5073, label: 'Kuromon Market', num: 2, cat: 'food', desc: 'Osaka\'s Kitchen — 170-year-old food market' },
        { lat: 34.6724, lng: 135.4976, label: 'Amerikamura', num: 3, cat: 'attraction', desc: 'Creative youth district with craft beer bars' },
        { lat: 34.6680, lng: 135.5010, label: 'Ajinoya', num: 4, cat: 'food', desc: 'Top-tier okonomiyaki in Namba' }
      ]
    },
    {
      num: 10,
      date: '2026-04-09',
      neighborhoods: 'Nara · Todai-ji · Nara Park',
      title: 'Day Trip to Nara — Deer, Giant Buddha & Ancient Capital',
      description: "Take a short train ride to Nara — Japan\'s first permanent capital, where over 1,000 wild deer roam freely through the city. Bow to them (they bow back!), visit the world\'s largest wooden building housing a colossal Buddha, and stroll through ancient shrine forests.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park',
              description: 'Nara is just 45 minutes from Osaka by train. As you walk from the station, you\'ll encounter the first of Nara\'s 1,000+ wild deer — considered sacred messengers of the gods. Buy ¥200 deer crackers (shika-senbei) and watch them bow politely for a treat.',
              details: [
                '🚃 JR or Kintetsu line from Namba: ~45 min',
                '🦌 The deer are wild but very tame — they literally bow for crackers',
                '⚠️ Hide your maps and bags — the deer will try to eat anything paper!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Todai-ji Temple — Great Buddha Hall',
              description: 'The Daibutsuden (Great Buddha Hall) is the world\'s largest wooden building, housing a 15-meter bronze Buddha cast in 752 AD. The scale is genuinely awe-inspiring — you won\'t believe it until you stand in front of it.',
              details: [
                '🏛️ ¥600 entry · The building is 48m tall — massive even by modern standards',
                '📸 Try to squeeze through the pillar hole — legend says it grants enlightenment',
                '🌸 Cherry trees in Todai-ji\'s grounds add spring color'
              ]
            },
            {
              title: 'Kasuga Grand Shrine',
              description: 'Walk through the thousands of stone lanterns leading to Kasuga Grand Shrine, set in a primeval forest. The bronze lanterns inside the shrine are lit during festivals, creating an ethereal atmosphere.',
              details: [
                '🏮 3,000 stone and bronze lanterns line the approach',
                '🌿 The primeval forest behind the shrine is a UNESCO site',
                '⛩️ ¥500 for the inner sanctuary'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Kakinoha Sushi (柿の葉寿司)',
              description: 'Nara\'s signature dish — sushi wrapped in persimmon leaves. The leaf imparts a subtle fragrance to the vinegared rice and fish. Try it at Tanaka or Hiraso near Nara Park.',
              meta: '💰 $ · 📍 Multiple shops near Nara Park'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka — Final Night',
              description: 'Head back to Osaka for your last night. Hit up any food spots you missed, or return to a favorite from the past two days. Dotonbori at night is electric.',
              details: [
                '🚃 Last trains to Osaka run until ~11pm',
                '🌃 Dotonbori canal reflections at night are gorgeous'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Ichiran Ramen Dotonbori',
              description: 'End your Osaka food tour at Ichiran — famous for its solo booth ramen experience. Customize your noodle firmness, broth richness, and spice level on a paper form. Deeply personal, perfectly crafted tonkotsu.',
              meta: '💰 $ · 📍 Dotonbori, Chuo-ku · Open 24 hours'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ wild deer roaming freely — they bow!' },
        { lat: 34.6890, lng: 135.8399, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building with giant Buddha' },
        { lat: 34.6812, lng: 135.8499, label: 'Kasuga Grand Shrine', num: 3, cat: 'attraction', desc: 'Ancient shrine with 3,000 stone lanterns' },
        { lat: 34.6851, lng: 135.8100, label: 'Kakinoha Sushi', num: 4, cat: 'food', desc: 'Nara\'s signature persimmon leaf sushi' }
      ]
    },
    {
      num: 11,
      date: '2026-04-10',
      neighborhoods: 'Harajuku · Omotesando · Shimokitazawa · Shinjuku',
      title: 'Back to Tokyo — Shopping Day One: Fashion & Vintage',
      description: "Shinkansen back to Tokyo for two full days of shopping! Today is fashion-focused: Harajuku\'s wild street style, Omotesando\'s luxury boutiques, and Shimokitazawa\'s legendary vintage scene. Plus your well-deserved head spa experience.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Tokyo & Head Spa',
              description: 'Take an early shinkansen from Shin-Osaka to Tokyo. Drop your bags at your hotel, then head to Shibuya for a luxurious Japanese head spa — the scalp massage you\'ve been dreaming of. Book The Head Spa Tokyo or Head Spa Kuu in Omotesando.',
              details: [
                '🚄 Shin-Osaka → Tokyo: ~2h 30min by Hikari',
                '💆 The Head Spa Tokyo (Shibuya): ¥8,000-15,000 for 60-90 min',
                '💆 Head Spa Kuu (Omotesando): ¥12,000 for 120 min — highly rated by tourists',
                '📱 Book online in advance — these places fill up'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Tokyo\'s fashion epicenter. Takeshita Street is a chaotic, colorful pedestrian lane of youth fashion, crepe shops, and kawaii culture. Beyond the street, Cat Street and the backstreets have independent boutiques and streetwear.',
              details: [
                '👗 Takeshita Street — wild youth fashion, cotton candy, purikura photo booths',
                '🛍️ Cat Street — curated boutiques, streetwear, and concept stores',
                '🍦 Marion Crepes — Harajuku institution since 1976'
              ]
            },
            {
              title: 'Omotesando — Tokyo\'s Champs-Élysées',
              description: 'A tree-lined boulevard of flagship luxury stores housed in architect-designed buildings. Even if you\'re not shopping luxury, the architecture alone is worth the walk — Tadao Ando\'s Omotesando Hills, the Prada crystal, and the Dior building.',
              details: [
                '🏛️ Architecture: Prada, Dior, Tod\'s — each building is a statement piece',
                '🛍️ Omotesando Hills — multi-level shopping complex by Tadao Ando',
                '📍 Walk from Harajuku to Omotesando — they connect naturally'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shimokitazawa — Vintage & Live Music',
              description: 'Tokyo\'s bohemian neighborhood is a maze of vintage clothing stores, tiny live music venues, and cozy cafés. It feels like a different city — slow, creative, and full of character. Perfect for vintage finds and a relaxed evening.',
              details: [
                '👕 New York Joe Exchange — huge vintage warehouse',
                '🎵 Live music at Bear Pond or Shelter',
                '☕ Bear Pond Espresso — famously grumpy barista, incredible coffee'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shirube (しるべ)',
              description: 'A beloved Shimokitazawa izakaya with an open kitchen, great sake selection, and inventive small plates. The grilled miso-marinated fish and dashimaki tamago are standouts.',
              meta: '💰 $$ · 📍 Shimokitazawa · Cozy and lively atmosphere'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6604, lng: 139.7024, label: 'The Head Spa Tokyo', num: 1, cat: 'attraction', desc: 'Japanese head spa & scalp massage in Shibuya' },
        { lat: 35.6702, lng: 139.7027, label: 'Harajuku / Takeshita Street', num: 2, cat: 'attraction', desc: 'Tokyo\'s colorful fashion epicenter' },
        { lat: 35.6653, lng: 139.7121, label: 'Omotesando', num: 3, cat: 'attraction', desc: 'Luxury boulevard with stunning architecture' },
        { lat: 35.6613, lng: 139.6680, label: 'Shimokitazawa', num: 4, cat: 'attraction', desc: 'Bohemian vintage shopping and live music' },
        { lat: 35.6610, lng: 139.6685, label: 'Shirube Izakaya', num: 5, cat: 'food', desc: 'Loved izakaya with sake and small plates' }
      ]
    },
    {
      num: 12,
      date: '2026-04-11',
      neighborhoods: 'Akihabara · Nakamise · Ginza · Shibuya',
      title: 'Shopping Day Two — Electronics, Department Stores & Souvenirs',
      description: "Day two of shopping covers everything else: Akihabara for electronics and anime merch, Ginza for department stores and tax-free luxury, and a final evening in Shibuya. Load up on souvenirs — Japanese Kit-Kats, chopsticks, ceramics, and those perfect little things you can only find here.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Akihabara — Electronics & Anime',
              description: 'Return to Akihabara with shopping intent. Yodobashi Camera is an 8-floor electronics megastore (tax-free with passport). Mandarake and Animate are paradise for manga and anime. Don\'t forget the gachapon (capsule toy) alleys — addictive souvenir machines.',
              details: [
                '📱 Yodobashi Camera — tax-free electronics, cameras, appliances',
                '📚 Mandarake Complex — 8 floors of manga, figures, vintage games',
                '🎰 Gachapon machines — ¥200-500 per capsule, perfect small souvenirs',
                '💳 Most large stores offer tax-free shopping (bring passport)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza — Department Stores & Luxury',
              description: 'Tokyo\'s upscale shopping district. Mitsukoshi and Ginza Six are massive department stores with incredible basement food halls (depachika). Even if you don\'t buy luxury goods, the depachika alone are worth the trip — beautifully wrapped sweets, bento, and wagashi.',
              details: [
                '🏬 Ginza Six — modern luxury mall with rooftop garden',
                '🏬 Mitsukoshi — Japan\'s oldest department store, incredible depachika',
                '🍫 Depachika food halls — buy beautiful boxed sweets as gifts',
                '🗾 Uniqlo Ginza flagship — 12 floors, Japan-exclusive items'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Mitsukoshi Depachika',
              description: 'Grab a bento box from the legendary Mitsukoshi basement food hall. The variety is staggering — wagyu bento, sushi rolls, tempura sets — all beautifully packaged.',
              meta: '💰 $$ · 📍 Ginza Mitsukoshi B1-B2 · Food heaven'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Last Night in Tokyo — Golden Gai',
              description: 'Spend your final evening in Shinjuku\'s Golden Gai — a maze of over 200 tiny bars, each seating 6-10 people, crammed into six narrow alleys. Each bar has its own personality — music bars, movie bars, art bars. It\'s the most Tokyo experience possible.',
              details: [
                '🍺 Most bars have a ¥500-1000 cover charge — totally normal',
                '🎵 Find a bar that matches your vibe — ask to peek before sitting',
                '📸 The narrow alleys are incredibly photogenic',
                '🌃 Best after 9pm when things really come alive'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Omoide Yokocho (Memory Lane)',
              description: 'Just outside Shinjuku Station\'s west exit, this narrow alley of tiny yakitori stalls has been serving smoky, charcoal-grilled skewers since the 1940s. Squeeze onto a stool, order assorted yakitori and a cold beer, and soak in the atmosphere of old Tokyo.',
              meta: '💰 $ · 📍 Shinjuku West Exit · Cash only · The smoke is part of the charm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 1, cat: 'attraction', desc: 'Electronics, anime, and gachapon paradise' },
        { lat: 35.6717, lng: 139.7649, label: 'Ginza', num: 2, cat: 'attraction', desc: 'Upscale shopping and incredible depachika food halls' },
        { lat: 35.6933, lng: 139.7035, label: 'Golden Gai', num: 3, cat: 'food', desc: '200+ tiny bars in narrow alleys — quintessential Tokyo' },
        { lat: 35.6934, lng: 139.6988, label: 'Omoide Yokocho', num: 4, cat: 'food', desc: 'Smoky yakitori alley since the 1940s' }
      ]
    },
    {
      num: 13,
      date: '2026-04-12',
      neighborhoods: 'Shinjuku · Narita/Haneda',
      title: 'Sayonara, Japan — Last Bites & Departure',
      description: "Your final morning in Tokyo. Squeeze in one last experience — a konbini (convenience store) breakfast that\'s shockingly good, grab final souvenirs at the airport, and say goodbye to a country that will stay with you forever.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Morning Rituals',
              description: 'Start your last day with a Japanese convenience store breakfast — sounds ordinary, but Japan\'s konbini are on another level. Onigiri (rice balls), egg sandwiches, and canned coffee from 7-Eleven or Lawson. Then pack up and check out.',
              details: [
                '🍙 Onigiri: ¥120-180 each — tuna mayo, salmon, or umeboshi',
                '🥪 7-Eleven egg sandwiches are genuinely famous',
                '☕ Boss or Georgia canned coffee from the hotel vending machine'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Airport & Last Shopping',
              description: 'Head to the airport with plenty of time. Both Narita and Haneda have excellent shopping — this is your last chance for Japanese Kit-Kats (matcha, sake, strawberry), Tokyo Banana, and other omiyage (souvenir snacks).',
              details: [
                '✈️ Narita Express from Shinjuku: ~80 min (JR Pass)',
                '🍫 Don\'t forget: Japanese Kit-Kats, Tokyo Banana, roasted green tea',
                '💰 Claim tax refund at the airport if you have tax-free purchases'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku', num: 1, cat: 'attraction', desc: 'Your Tokyo home base — final morning' },
        { lat: 35.7647, lng: 140.3864, label: 'Narita Airport', num: 2, cat: 'attraction', desc: 'International departure — last Kit-Kat shopping!' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (non-ryokan)', budget: '¥8,000-12,000/night', midrange: '¥15,000-25,000/night', luxury: '¥30,000-60,000/night' },
    { category: 'Ryokan (2 nights, per person)', budget: '¥15,000-25,000/night', midrange: '¥30,000-50,000/night', luxury: '¥50,000-100,000/night' },
    { category: 'Meals (per couple)', budget: '¥4,000-8,000/day', midrange: '¥8,000-15,000/day', luxury: '¥20,000-40,000/day' },
    { category: 'Transport (JR Pass + local)', budget: '¥60,000 total', midrange: '¥70,000 total', luxury: '¥90,000+ total' },
    { category: 'Activities & Entry Fees', budget: '¥3,000-5,000 total', midrange: '¥10,000-15,000 total', luxury: '¥20,000-40,000 total' },
    { category: '12-Night Total (couple)', budget: '$2,500-4,000', midrange: '$5,000-8,000', luxury: '$10,000-20,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita (NRT) or Haneda (HND) — Haneda is closer to the city center', 'Narita Express to Shinjuku/Tokyo: ~60-80 min (JR Pass covered)', 'Haneda monorail or Keikyu line to the city: ~20-30 min', 'Activate your JR Pass at the airport JR ticket office'] },
    { title: '🚄 Japan Rail Pass', items: ['14-day JR Pass: ~¥50,000 ($330) — covers all shinkansen (except Nozomi/Mizuho) + JR locals', 'Buy online before your trip and activate at the airport', 'Covers: Tokyo↔Kyoto, Kyoto↔Odawara, Odawara↔Osaka, Osaka↔Tokyo shinkansen', 'Also covers JR city trains, Narita Express, and some buses'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku (transit hub), Shibuya (nightlife), Asakusa (traditional)', 'Kyoto: Near Kyoto Station (convenient) or Gion (atmospheric)', 'Hakone: Hakone-Yumoto or Gora ryokans', 'Osaka: Namba/Dotonbori (food central)'] },
    { title: '🌡️ Weather (Late March – Early April)', items: ['Temperatures: 10-18°C (50-64°F) — pleasant but bring layers', 'Cherry blossoms peak late March – early April', 'Occasional spring rain — pack a compact umbrella', 'Light jacket for evenings, comfortable walking shoes essential'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at the airport (~¥1,000/day) or get an eSIM before departure', 'Ubigi, Airalo, or Japan Wireless are popular eSIM providers', 'Google Maps works perfectly for all transit navigation in Japan', 'Google Translate camera mode reads Japanese signs instantly'] },
    { title: '🎌 Cultural Tips', items: ['Remove shoes when entering homes, ryokans, and some restaurants (look for a genkan)', 'Don\'t tip — it\'s not customary and can cause confusion', 'Don\'t eat while walking (standing at a stall is fine)', 'Carry a small towel — many restrooms don\'t have hand dryers', 'Trash cans are rare — carry a small bag for your garbage'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
