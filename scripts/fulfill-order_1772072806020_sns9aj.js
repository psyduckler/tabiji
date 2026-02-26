const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772072806020_sns9aj',
  email: 'psyduckler@gmail.com',
  destination: 'Osaka, Japan',
  startDate: '2026-02-27',
  endDate: '2026-03-02',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Solo Through the Kitchen of Japan',
  subtitle: '3 nights of neon-lit street food, ancient castles & neighbourhood charm in Osaka',
  description: "Osaka is Japan's most unapologetically fun city — a place where eating is a sport, strangers become friends over counter seats, and every neighbourhood has its own personality. This itinerary takes you from the neon chaos of Dotonbori to the retro soul of Shinsekai, through the peaceful grounds of Osaka Castle in late-winter light, and into hidden standing bars where solo travelers are welcomed like regulars. Late February means fewer crowds, crisp air, and the first hints of plum blossoms — the perfect time to have Osaka almost to yourself.",
  duration: '3 nights',
  dates: 'Feb 27 – Mar 2, 2026',
  budget: '$–$$',
  pace: 'Moderate',
  bestFor: 'Solo Travelers · Foodies',
  highlights: [
    'Dotonbori neon walk & street food crawl',
    'Osaka Castle & Nishinomaru Garden plum blossoms',
    'Shinsekai retro neighbourhood & Tsutenkaku Tower',
    'Kuromon Market morning tasting tour',
    'Standing bars & izakaya hopping in Ura-Namba'
  ],

  essentials: [
    { title: '🌸 Late Winter Weather', text: 'Late February in Osaka averages 5–10°C (41–50°F). Bring layers — a warm jacket for mornings, lighter layers for afternoon sun. Plum blossoms (ume) start blooming at Osaka Castle around this time.' },
    { title: '🚇 Getting Around', text: 'Get an ICOCA card at the airport for seamless subway, train, and bus travel. The Osaka Metro covers everywhere you need. A 1-day pass (¥820) is worth it for heavy exploration days.' },
    { title: '🍜 Solo Dining Culture', text: "Osaka is paradise for solo eaters. Counter seats at ramen shops, takoyaki stands, and standing bars (tachinomi) are designed for one. No awkward solo dining here — it's the norm and often preferred." },
    { title: '💴 Cash & Cards', text: 'Many small restaurants and street food stalls are cash-only. Withdraw yen at 7-Eleven ATMs (no fee, English interface). Larger restaurants accept IC cards and credit cards.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-27',
      neighborhoods: 'Namba · Dotonbori · Shinsaibashi',
      title: 'Neon Lights & Street Food Baptism',
      description: "Arrive in Osaka and dive straight into its beating heart — the canal-side madness of Dotonbori. Tonight is about sensory overload: giant mechanical crabs, glowing signs reflected in the water, and eating your way through Japan's street food capital.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check Into Namba',
              description: 'Fly into Kansai International Airport and take the Nankai Rapi:t express train (34 min) straight to Namba Station. Drop your bags and step outside — you\'re already in the middle of everything.',
              details: [
                '🚂 Nankai Rapi:t — ¥1,450, retro-futuristic design, direct to Namba',
                '🏨 Stay near Namba or Shinsaibashi for walkable access to everything',
                '💡 Arrive by mid-afternoon to maximize your first evening'
              ]
            },
            {
              title: 'Shinsaibashi-suji Shopping Arcade',
              description: 'Stroll through this 600-metre covered shopping arcade stretching from Shinsaibashi to Namba. A mix of international brands, local boutiques, drugstores, and vintage shops — perfect for an afternoon wander.',
              details: [
                '🛍️ Covered arcade means weather-proof browsing',
                '💊 Stock up on Japanese skincare at matsumoto kiyoshi',
                '📸 Side streets hide vintage shops and quirky cafés'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Pick up a pocket WiFi or activate your eSIM at KIX airport. Osaka\'s free WiFi is patchy outside stations and malls.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Street Food Crawl',
              description: 'The main event. Walk along the Dotonbori canal and eat everything. Takoyaki (octopus balls) from Wanaka, kushikatsu (deep-fried skewers) from Daruma, gyoza from Chao Chao — Osaka\'s motto is kuidaore (eat until you drop), and tonight you honour it.',
              details: [
                '🐙 Takoyaki Wanaka — crispy outside, molten inside, the city\'s best',
                '🍢 Kushikatsu Daruma — the original since 1929. Rule: no double-dipping!',
                '📸 The Glico Running Man sign — Osaka\'s most iconic photo spot',
                '🌊 Walk the canal boardwalk for the full neon reflection experience'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Late Dinner',
              name: 'Ichiran Ramen Dotonbori',
              description: 'The ultimate solo ramen experience — individual booths with a bamboo curtain, a paper order form to customize your bowl, and rich Hakata-style tonkotsu broth. Designed for solo diners.',
              meta: '💰 $ · 📍 Dotonbori · Open late'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6658, lng: 135.5013, label: 'Namba Station', num: 1, cat: 'transport', desc: 'Main arrival hub — Nankai line from KIX airport' },
        { lat: 34.6715, lng: 135.5017, label: 'Shinsaibashi-suji Arcade', num: 2, cat: 'attraction', desc: '600m covered shopping arcade' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori', num: 3, cat: 'attraction', desc: 'Neon-lit canal street — Osaka\'s street food epicenter' },
        { lat: 34.6685, lng: 135.5010, label: 'Takoyaki Wanaka', num: 4, cat: 'food', desc: 'Osaka\'s best takoyaki — crispy and molten' },
        { lat: 34.6682, lng: 135.5022, label: 'Kushikatsu Daruma', num: 5, cat: 'food', desc: 'Legendary kushikatsu since 1929' },
        { lat: 34.6686, lng: 135.5027, label: 'Ichiran Ramen', num: 6, cat: 'food', desc: 'Solo-booth tonkotsu ramen experience' }
      ]
    },
    {
      num: 2,
      date: '2026-02-28',
      neighborhoods: 'Osaka Castle · Tenmabashi · Nakazakicho · Umeda',
      title: 'Castle Grounds, Plum Blossoms & Hidden Cafés',
      description: "Today you explore Osaka's cultural and creative side. Morning at the majestic Osaka Castle surrounded by early plum blossoms, afternoon in the bohemian backstreets of Nakazakicho with its quirky cafés, and evening high above the city in Umeda's sky gardens.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: 'Walk through the vast castle grounds to Japan\'s most visited castle. The main tower houses a museum of Toyotomi Hideyoshi\'s legacy with panoramic views from the 8th floor. Nishinomaru Garden, on the western side, is where Osaka\'s earliest plum blossoms appear in late February — pale pink and white against the castle backdrop.',
              details: [
                '🏯 Main tower: ¥600 · Open 9am–5pm',
                '🌸 Nishinomaru Garden: ¥200 — plum trees bloom late Feb/early March',
                '📸 Best castle photo: from the southwest across the inner moat',
                '🏃 The castle park is massive — allow 2+ hours to explore properly'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Café & Meal MUJI (Grand Front Osaka or Namba)',
              description: 'Clean, minimalist café serving Japanese breakfast sets — grilled fish, miso soup, rice, pickles. The MUJI way: simple, excellent ingredients, no fuss.',
              meta: '💰 $ · 📍 Multiple locations'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakazakicho Backstreet Exploration',
              description: 'This former residential neighbourhood near Umeda has been quietly transformed into Osaka\'s coolest creative district. Wander narrow lanes past converted wooden houses now home to independent cafés, record shops, vintage clothing stores, and tiny galleries. It feels like a different city entirely.',
              details: [
                '☕ Salon de AManTo — café in a 100-year-old townhouse with a rooftop garden',
                '📚 Blackbird Books — tiny independent bookshop with curated Japanese lit',
                '🎨 Street art and hand-painted signs on every corner',
                '🚶 No map needed — just wander and discover'
              ]
            }
          ],
          meals: [
            {
              type: '🍛 Lunch',
              name: 'Salon de AManTo',
              description: 'A café, gallery, and cultural space in a century-old machiya townhouse. Vegetarian-friendly lunch sets, excellent coffee, and a rooftop where you can see across the neighbourhood rooftops.',
              meta: '💰 $ · 📍 Nakazakicho · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Umeda Sky Building & Floating Garden Observatory',
              description: 'Take the dramatic escalator ride to the Floating Garden Observatory on the 40th floor of the futuristic Umeda Sky Building. The 360° open-air rooftop gives you all of Osaka — from the mountains to the bay — glittering below at sunset.',
              details: [
                '🌆 Admission: ¥1,500 · Best at sunset (around 5:45pm in late Feb)',
                '🏙️ The building itself is an architectural landmark — two towers connected by a sky bridge',
                '🍻 Basement floor: Takimi-Koji — a retro Showa-era food alley'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Takimi-Koji Alley (Umeda Sky Building B1)',
              description: 'A reconstructed 1920s Osaka street in the basement of the Sky Building. Tiny restaurants serve okonomiyaki, udon, sushi, and yakitori in atmospheric retro surroundings.',
              meta: '💰 $–$$ · 📍 Umeda Sky Building basement'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle with museum and panoramic views' },
        { lat: 34.6855, lng: 135.5220, label: 'Nishinomaru Garden', num: 2, cat: 'attraction', desc: 'Castle garden with early plum blossoms' },
        { lat: 34.7075, lng: 135.4995, label: 'Nakazakicho', num: 3, cat: 'attraction', desc: 'Bohemian backstreet neighbourhood with indie cafés' },
        { lat: 34.7078, lng: 135.4992, label: 'Salon de AManTo', num: 4, cat: 'food', desc: '100-year-old townhouse café with rooftop' },
        { lat: 34.7052, lng: 135.4901, label: 'Umeda Sky Building', num: 5, cat: 'attraction', desc: 'Futuristic tower with 360° floating garden observatory' },
        { lat: 34.7052, lng: 135.4901, label: 'Takimi-Koji Alley', num: 6, cat: 'food', desc: 'Retro 1920s food alley in the Sky Building basement' }
      ]
    },
    {
      num: 3,
      date: '2026-03-01',
      neighborhoods: 'Kuromon Market · Shinsekai · Tennoji · Ura-Namba',
      title: 'Market Mornings, Retro Towers & Izakaya Nights',
      description: "Today is pure Osaka soul. Morning grazing through Kuromon Market, afternoon in the wonderfully weird retro district of Shinsekai, evening izakaya hopping in the hidden bars of Ura-Namba. This is the day you fall in love with the city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Market Tasting Tour',
              description: "Osaka's Kitchen has been feeding the city for over 190 years. Walk through narrow aisles past 170+ stalls selling the freshest sashimi, grilled seafood, tamagoyaki, mochi, and seasonal fruits. Eat as you go — this is breakfast and a cultural experience in one.",
              details: [
                '🦀 Fresh king crab legs grilled to order — worth the splurge',
                '🍣 Sashimi stands with uni, toro, and seasonal fish',
                '🍡 Tamagoyaki (Japanese rolled omelette) from the corner stall',
                '🍓 Japanese strawberries in winter — sweet and perfect',
                '⏰ Go by 9am for the best selection; market winds down by 4pm'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai & Tsutenkaku Tower',
              description: "Step into Osaka's most retro neighbourhood — Shinsekai (New World) was built in 1912 as a futuristic district modelled on Paris and New York. Today it's a glorious time warp of neon signs, shogi parlours, and kushikatsu joints. Climb Tsutenkaku Tower for views and rub Billiken's feet for good luck.",
              details: [
                '🗼 Tsutenkaku Tower: ¥900 · Rub Billiken\'s feet for luck',
                '🎮 Retro game arcades and shogi (Japanese chess) parlours everywhere',
                '📸 The tower framed by neon kushikatsu signs is quintessential Osaka',
                '🍢 Jan Jan Yokocho — narrow alley of old-school kushikatsu shops'
              ]
            },
            {
              title: 'Tennoji Park & Chausuyama',
              description: 'Walk through Tennoji Park to the small Chausuyama hill — a quiet green space perfect for a breather. The nearby Tennoji Zoo and Abeno Harukas (Japan\'s tallest skyscraper) are bonus options.',
              details: [
                '🏙️ Abeno Harukas observation deck (300m) — optional ¥1,500 for incredible views',
                '🌳 Tennoji Park is a peaceful contrast to Shinsekai\'s chaos'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Lunch',
              name: 'Yaekatsu (Shinsekai)',
              description: 'One of Shinsekai\'s most beloved kushikatsu shops. Battered and fried skewers of everything — shrimp, lotus root, cheese, pumpkin — with a communal dipping sauce. Solo counter seats available.',
              meta: '💰 $ · 📍 Shinsekai · Counter seating'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ura-Namba Izakaya & Standing Bar Crawl',
              description: "Ura-Namba (Back Namba) is the locals' secret — a tight grid of alleyways south of Namba packed with tiny izakayas, standing bars (tachinomi), and hole-in-the-wall restaurants. This is where Osaka goes to drink and eat after work. As a solo traveler, you'll fit right in at the counter.",
              details: [
                '🍶 Tachinomi (standing bars) charge ¥200-500 per drink — cheapest night out in Japan',
                '🏮 Look for the red lanterns and follow the smoke and laughter',
                '🍺 Try highball (whisky soda) — Osaka\'s signature drink',
                '🗣️ Basic Japanese phrases go a long way: kanpai! (cheers), oishii! (delicious)'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Toyo (Ura-Namba)',
              description: 'Legendary outdoor standing sashimi bar where the charismatic chef slices tuna with theatrical flair. Cash only, no seats, incredible fish. A quintessential Osaka experience.',
              meta: '💰 $ · 📍 Ura-Namba · Standing only · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6689, lng: 135.5072, label: 'Kuromon Market', num: 1, cat: 'food', desc: 'Osaka\'s Kitchen — 190+ year old market with 170 stalls' },
        { lat: 34.6523, lng: 135.5063, label: 'Shinsekai', num: 2, cat: 'attraction', desc: 'Retro 1912 neighbourhood with neon and kushikatsu' },
        { lat: 34.6516, lng: 135.5064, label: 'Tsutenkaku Tower', num: 3, cat: 'attraction', desc: 'Iconic tower — rub Billiken\'s feet for luck' },
        { lat: 34.6523, lng: 135.5070, label: 'Yaekatsu', num: 4, cat: 'food', desc: 'Beloved kushikatsu counter in Shinsekai' },
        { lat: 34.6492, lng: 135.5133, label: 'Abeno Harukas', num: 5, cat: 'attraction', desc: 'Japan\'s tallest skyscraper — 300m observation deck' },
        { lat: 34.6625, lng: 135.5005, label: 'Ura-Namba', num: 6, cat: 'attraction', desc: 'Hidden alley district of izakayas and standing bars' },
        { lat: 34.6627, lng: 135.5000, label: 'Toyo Sashimi Bar', num: 7, cat: 'food', desc: 'Legendary standing sashimi bar — theatrical chef' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥4,000–8,000/night', midrange: '¥10,000–20,000/night', luxury: '¥30,000–60,000/night' },
    { category: 'Meals', budget: '¥2,000–4,000/day', midrange: '¥5,000–10,000/day', luxury: '¥15,000–30,000/day' },
    { category: 'Transport', budget: '¥500–1,000/day', midrange: '¥1,000–2,000/day', luxury: '¥3,000–5,000/day (taxi)' },
    { category: 'Activities', budget: '¥0–1,000/day', midrange: '¥1,000–3,000/day', luxury: '¥5,000–10,000/day' },
    { category: '3-Night Total', budget: '¥25,000–50,000 ($170–340)', midrange: '¥60,000–120,000 ($400–800)', luxury: '¥180,000–350,000 ($1,200–2,300)' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) — main international gateway', 'Nankai Rapi:t express to Namba: 34 min, ¥1,450', 'JR Haruka express to Tennoji/Shin-Osaka also available', 'Itami Airport (ITM) for domestic flights — closer to city centre'] },
    { title: '🏨 Where to Stay', items: ['Namba/Dotonbori — walkable to everything, neon energy all night', 'Shinsaibashi — slightly quieter, great shopping and food', 'Tennoji — near Shinsekai, good value, local vibe', 'Capsule hotels and hostels are excellent for solo travelers (try Nine Hours or The Dorm)'] },
    { title: '🌡️ Weather', items: ['Late Feb averages 5–10°C (41–50°F)', 'Crisp and dry — layers are essential', 'Plum blossoms (ume) start blooming in late February', 'Early cherry blossoms unlikely until late March'] },
    { title: '💳 Money', items: ['Many small restaurants and street stalls are cash-only', '7-Eleven ATMs accept international cards (no fee, English available)', 'IC cards (ICOCA/Suica) work for trains and many konbini purchases', 'Budget ¥5,000–10,000/day for comfortable solo travel'] },
    { title: '📱 Connectivity', items: ['Activate eSIM before arrival or buy SIM at KIX airport', 'Free WiFi at stations, konbini, and most hotels', 'Download Google Maps offline — essential for backstreet navigation', 'Google Translate camera mode reads Japanese menus instantly'] }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
