const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773148297467_uv1pmb',
  email: 'galaxycats510@gmail.com',
  destination: 'Osaka',
  startDate: '2026-03-12',
  endDate: '2026-03-12',
  groupSize: '2',
  requests: 'Plan one day in Osaka for my parents. Their plan is to start their day at minoo park'
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '\u{1F1EF}\u{1F1F5}',
  title: 'Waterfalls, Street Food & Neon Lights — One Perfect Day in Osaka',
  subtitle: 'A morning forest hike, afternoon retro district, and evening food feast for two',
  description: "Your parents asked to start at Minoo Park, and what a way to begin — a gentle riverside trail through ancient forest leading to a 33-metre waterfall, with a centuries-old mountain temple halfway up. After the morning hike, we bring them back into the city for Osaka's signature experiences: the retro wonderland of Shinsekai with its iconic tower and legendary kushikatsu, then an evening stroll through the neon-drenched canals of Dotonbori for takoyaki, okonomiyaki, and the most photogenic street in Japan. It's one day, but it captures the full range of what makes Osaka unforgettable — nature, culture, and some of the best street food on earth.",
  duration: '1 day',
  dates: 'Mar 12, 2026',
  budget: '$$',
  pace: 'Relaxed',
  bestFor: 'Parents · Couples',
  highlights: [
    'Morning hike to Minoo Falls — a stunning 33-metre waterfall through ancient forest, just 30 minutes from central Osaka',
    'Ryuanji Temple — a centuries-old mountain temple nestled along the trail, part of the Shugendo mountain worship tradition',
    'Shinsekai — Osaka\'s beloved retro district with the iconic Tsutenkaku Tower and the birthplace of kushikatsu',
    'Dotonbori Canal at dusk — glowing neon signs, the famous Glico Running Man, and Osaka\'s greatest street food strip',
    'Osaka\'s legendary street food: takoyaki, okonomiyaki, kushikatsu, and fresh taiyaki'
  ],
  essentials: [
    { title: '\u{1F338} Mid-March Weather', text: 'Osaka in mid-March averages 7–15°C (45–59°F). Spring is arriving — you may catch early cherry blossoms. Pack layers: a light jacket for morning, something you can peel off by afternoon. Comfortable walking shoes are essential for the Minoo Park trail.' },
    { title: '\u{1F687} Getting Around', text: 'Osaka has an excellent subway and rail network. Get an ICOCA IC card at any station for tap-and-go on all trains and buses. For Minoo Park, take the Hankyu Takarazuka Line from Umeda to Ishibashi-Handai-Mae, then transfer to the Hankyu Minoo Line to Minoo Station (~30 min total). The afternoon and evening spots are all on the Osaka Metro.' },
    { title: '\u{1F35C} Dining Style', text: "Osaka is the \"Kitchen of Japan\" (天下の台所). Street food is the star — most of the best eating happens standing at counters or perched on tiny stools. No reservations needed anywhere on this itinerary. Cash is king at street stalls, though more restaurants now accept IC cards." },
    { title: '\u{1F6B6} Walking Expectations', text: "The Minoo Park trail is 2.7 km each way on a paved, gently sloping riverside path — very manageable for parents. The afternoon and evening areas are flat urban walking. Total for the day: roughly 10-12 km of easy walking." },
    { title: '\u{1F4B4} Budget Tips', text: 'Street food items run ¥400-800 each. A full sit-down meal is ¥1,000-2,000 per person. Tsutenkaku Tower observation deck is ¥900. Convenience stores (Lawson, 7-Eleven, FamilyMart) have excellent onigiri, sandwiches, and drinks for trail snacks.' }
  ],
  days: [
    {
      num: 1,
      date: '2026-03-12',
      neighborhoods: 'Minoo · Shinsekai · Dotonbori · Namba',
      title: 'Forest Trail to Neon Lights',
      description: "Start the morning surrounded by nature at Minoo Park — a gentle riverside hike to a stunning waterfall with a mountain temple along the way. After lunch near the park, head south to Osaka's retro Shinsekai district for kushikatsu and city views from Tsutenkaku Tower. End the day in the electric glow of Dotonbori, grazing on Osaka's legendary street food along the famous canal.",
      timeBlocks: [
        {
          label: 'Morning (8:30 AM – 12:00 PM)',
          activities: [
            {
              title: 'Minoo Park (箕面公園) — Hike to Minoo Falls',
              description: "A gentle 2.7 km riverside trail through an ancient forest leading to Minoo Falls (箕面大滝), a beautiful 33-metre waterfall cascading over a mossy rock face. The paved path follows a stream uphill, passing through towering cedar and maple trees. In March, the forest is coming alive with early spring greenery, and you may spot wild monkeys in the trees. Along the way, small stalls sell momiji tempura — maple leaves deep-fried in sweet batter, a Minoo specialty for over 1,300 years.",
              details: [
                '🚃 From Umeda/Osaka Station: Hankyu Takarazuka Line to Ishibashi-Handai-Mae, transfer to Hankyu Minoo Line → Minoo Station (~30 min, ¥280)',
                '🚶 From Minoo Station: follow the main road north — trail entrance is a 5-minute walk',
                '⏱️ Trail to waterfall: 40-50 minutes each way at a relaxed pace (paved, gentle slope)',
                '🍁 Try momiji tempura from the stalls along the path — sweet, crunchy, unique to Minoo',
                '📸 The waterfall is most photogenic in morning light with fewer crowds',
                '🐒 Wild Japanese macaques live in the park — don\'t feed them or make eye contact',
                '🎫 Free — no admission fee'
              ]
            },
            {
              title: 'Ryuanji Temple (瀧安寺)',
              description: "Halfway up the trail to the waterfall, you'll pass Ryuanji Temple — one of Japan's oldest lottery shrines, founded over 1,400 years ago. It's part of the Shugendo mountain worship tradition and has a serene, timeless atmosphere. The main hall and surrounding stone gardens are a peaceful place to rest before continuing to the falls.",
              details: [
                '📍 Located about 15 minutes up the trail from the park entrance',
                '⏱️ Allow 10-15 minutes to explore the temple grounds',
                '🎫 Free to enter',
                '🙏 Said to be the birthplace of the Japanese lottery (takarakuji)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Start early (8:30-9:00 AM) to have the trail mostly to yourselves. The path gets busy after 10:30 AM, especially on weekends. Bring water and a small snack — there are vending machines at the station but limited options on the trail itself." }
          ]
        },
        {
          label: 'Lunch (12:00 PM – 1:30 PM)',
          activities: [
            {
              title: 'Lunch in Minoo — Local Favorites',
              description: "Head back down the trail to the Minoo Station area for a well-earned lunch. The streets around the station have charming local restaurants serving udon, soba, and set meals.",
              details: [
                '🍜 Minoo Beer Warehouse (箕面ビール ウエアハウス) — craft beer brewed in Minoo + excellent wood-fired pizza. A beloved local hangout',
                '🍛 Hashimoto Shokudō (はしもと食堂) — classic Japanese teishoku (set meals) with miso soup, rice, pickles, and grilled fish',
                '⏱️ Budget 45-60 minutes for a relaxed lunch',
                '📍 Both within a 5-minute walk of Minoo Station'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Lunch',
              name: 'Minoo Beer Warehouse (箕面ビール ウエアハウス)',
              description: "Minoo's own craft brewery taproom with rotating beers brewed locally (their Stout won a World Beer Award). Wood-fired pizzas, salads, and bar snacks in a casual warehouse setting. A hidden gem that locals love.",
              meta: '💰 ¥1,200-2,000/person · 📍 5 min walk from Minoo Station · Casual, no reservations needed'
            }
          ]
        },
        {
          label: 'Afternoon (2:00 PM – 5:00 PM)',
          activities: [
            {
              title: 'Transit to Shinsekai',
              description: "Take the train back to central Osaka and head to Shinsekai, Osaka's retro entertainment district. The journey takes about 45 minutes.",
              details: [
                '🚃 Hankyu Minoo Line → Ishibashi-Handai-Mae → Hankyu to Umeda → Osaka Metro Midosuji Line to Dobutsuen-mae Station',
                '⏱️ Total transit: ~45 minutes',
                '💡 Or take the JR Loop Line from Osaka Station to Shin-Imamiya Station (~20 min)'
              ]
            },
            {
              title: 'Shinsekai (新世界) District',
              description: "Step into Osaka's most characterful neighborhood — a retro wonderland of neon signs, towering Billiken statues, and narrow lanes packed with kushikatsu restaurants. Built in 1912 as Osaka's \"New World\" (modeled on New York and Paris), Shinsekai has kept its old-school charm while the rest of the city modernized. It's colorful, loud, a little chaotic, and completely loveable.",
              details: [
                '📍 Exit Dobutsuen-mae Station (Exit 1) and you\'re right in Shinsekai',
                '🗼 Tsutenkaku Tower dominates the skyline — the symbol of the district since 1956',
                '🎰 Jan Jan Yokocho alley — retro game arcades, shogi parlors, and tiny izakayas',
                '📸 The streets are incredibly photogenic, especially as the afternoon light hits the neon signs',
                '⏱️ Allow 1-2 hours to wander, snack, and soak up the atmosphere'
              ]
            },
            {
              title: 'Tsutenkaku Tower (通天閣)',
              description: "Osaka's beloved landmark tower, standing 108 metres tall. Take the elevator to the observation deck for panoramic views across southern Osaka. At the top, rub the feet of Billiken — the \"God of Things as They Ought to Be\" — for good luck. The tower is especially beautiful at golden hour when the city starts to glow.",
              details: [
                '🎫 Observation deck: ¥900/adult (general), ¥1,300 for special outdoor deck',
                '⏰ Open 10:00 AM – 8:00 PM (last entry 7:30 PM)',
                '📸 Best views: look north toward Umeda skyline or south to Tennoji Park',
                '⏱️ Allow 30-40 minutes for the visit'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Afternoon Snack',
              name: 'Daruma Kushikatsu (串カツだるま) — Shinsekai Main Branch',
              description: "The birthplace of kushikatsu — Osaka's signature deep-fried skewered street food. Daruma has been serving crispy, golden kushikatsu in Shinsekai since 1929. Pick from dozens of options: pork, shrimp, lotus root, mochi, asparagus, quail egg. Dip once in the communal sauce — never double-dip!",
              meta: '💰 ¥100-200 per skewer (most people eat 8-15 sticks) · 📍 Shinsekai, right near Tsutenkaku · Opens 11:00 AM'
            }
          ],
          tips: [
            { type: 'tip', text: "The golden rule of kushikatsu: NEVER double-dip in the communal sauce. Use the cabbage leaves on your table to scoop extra sauce onto your skewer if needed. The staff will remind you too — it's serious business in Osaka!" }
          ]
        },
        {
          label: 'Evening (5:30 PM – 9:00 PM)',
          activities: [
            {
              title: 'Dotonbori Canal Walk (道頓堀)',
              description: "Osaka's most iconic street — a sensory explosion of towering neon signs, animatronic crabs, and the glow of a thousand food stalls reflecting off the canal. The famous Glico Running Man sign has been the symbol of Osaka since 1935. Walk along the Dotonbori Riverwalk, cross the Ebisubashi Bridge, and take in the electric atmosphere. This is Osaka at its most alive.",
              details: [
                '🚃 From Shinsekai: Osaka Metro Sakaisuji Line from Ebisucho → Nippombashi, then walk 5 min. Or take a taxi (~¥800, 10 min)',
                '📍 Dotonbori runs along the canal between Dotonboribashi and Nipponbashi',
                '📸 Best Glico Running Man photo: stand on Ebisubashi Bridge facing south',
                '🌙 The neon signs light up from dusk — arrive around 5:30-6:00 PM for the transition'
              ]
            },
            {
              title: 'Dotonbori Street Food Crawl',
              description: "Graze your way through Osaka's greatest hits. This is what the city is famous for — standing at tiny counters, eating incredible food, moving to the next spot. No reservations, no formality, just pure delicious chaos.",
              details: [
                '🐙 Takoyaki (たこ焼き): Crispy-outside, molten-inside octopus balls. Try Wanaka (わなか) or Kukuru (くくる) along Dotonbori',
                '🥞 Okonomiyaki (お好み焼き): Osaka\'s savory pancake griddled before your eyes. Mizuno (美津の) is legendary — expect a 20-30 min wait but worth it',
                '🍢 Kushi-age at Yaekatsu — sit-down kushikatsu with a refined touch if you want more after Shinsekai',
                '🍜 Kinryu Ramen (金龍ラーメン) — the dragon-adorned ramen stand open 24 hours, a Dotonbori institution',
                '🍡 Taiyaki (鯛焼き) — fish-shaped pastry filled with sweet red bean paste or custard, perfect dessert'
              ]
            },
            {
              title: 'Shinsaibashi-suji Shopping Arcade (心斎橋筋)',
              description: "If your parents have energy for a stroll after dinner, the covered Shinsaibashi-suji arcade stretches 600 metres north from Dotonbori. Department stores, boutiques, drug stores (great for Japanese skincare and snack souvenirs), and everything in between — all under a covered roof.",
              details: [
                '📍 Entrance right at the north end of Dotonbori, across Ebisubashi Bridge',
                '⏰ Most shops open until 8:00-9:00 PM',
                '🛍️ Good for: Japanese cosmetics, Kit Kat flavors, matcha sweets, and unique souvenirs',
                '💡 Don Quijote (ドン・キホーテ) at Dotonbori is open 24 hours — the ultimate souvenir hunting ground'
              ]
            }
          ],
          meals: [
            {
              type: '🐙 Dinner (Street Food Crawl)',
              name: 'Dotonbori Street Food — Multiple Stops',
              description: "Rather than one big sit-down dinner, do what Osaka locals call kuidaore (食い倒れ) — \"eat until you drop.\" Start with takoyaki from Wanaka, grab okonomiyaki at Mizuno or Fukutaro, try a stick of kushikatsu, and finish with taiyaki for dessert. The whole canal strip is your restaurant.",
              meta: '💰 ¥2,000-4,000/person for a full crawl · 📍 Dotonbori canal strip · No reservations needed'
            }
          ],
          tips: [
            { type: 'tip', text: "Mizuno okonomiyaki is worth the wait — they've been making it since 1945. Order the yamaimoyaki (山芋焼き) — their signature fluffy pancake made with grated mountain yam. It's lighter and creamier than regular okonomiyaki." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.8367, lng: 135.4703, label: 'Minoo Station', num: 1, cat: 'transport', desc: 'Hankyu Minoo Line — trailhead starting point' },
        { lat: 34.8429, lng: 135.4695, label: 'Ryuanji Temple (瀧安寺)', num: 2, cat: 'attraction', desc: '1,400-year-old mountain temple — birthplace of the Japanese lottery' },
        { lat: 34.8519, lng: 135.4710, label: 'Minoo Falls (箕面大滝)', num: 3, cat: 'attraction', desc: '33-metre waterfall at the end of the forest trail' },
        { lat: 34.8354, lng: 135.4698, label: 'Minoo Beer Warehouse', num: 4, cat: 'food', desc: 'Award-winning craft brewery taproom with wood-fired pizza' },
        { lat: 34.6523, lng: 135.5063, label: 'Shinsekai (新世界)', num: 5, cat: 'attraction', desc: 'Retro entertainment district — neon signs, kushikatsu & Billiken' },
        { lat: 34.6528, lng: 135.5064, label: 'Tsutenkaku Tower', num: 6, cat: 'attraction', desc: '108m tower with panoramic views — rub Billiken for luck' },
        { lat: 34.6520, lng: 135.5058, label: 'Daruma Kushikatsu', num: 7, cat: 'food', desc: 'Legendary kushikatsu since 1929 — never double-dip!' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori Canal', num: 8, cat: 'attraction', desc: 'Neon-lit canal strip — Glico Running Man, street food paradise' },
        { lat: 34.6690, lng: 135.5020, label: 'Ebisubashi Bridge', num: 9, cat: 'attraction', desc: 'Best spot for the iconic Glico Running Man photo' },
        { lat: 34.6692, lng: 135.5027, label: 'Wanaka Takoyaki', num: 10, cat: 'food', desc: 'Crispy, molten takoyaki — Osaka\'s signature street food' },
        { lat: 34.6695, lng: 135.5008, label: 'Mizuno Okonomiyaki (美津の)', num: 11, cat: 'food', desc: 'Since 1945 — try the yamaimoyaki, fluffy with mountain yam' },
        { lat: 34.6714, lng: 135.5013, label: 'Shinsaibashi-suji Arcade', num: 12, cat: 'attraction', desc: '600m covered shopping arcade — souvenirs, cosmetics, snacks' }
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('\n✅ FULFILLMENT COMPLETE');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('Email sent:', result.emailSent);
