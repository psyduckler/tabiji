const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772103227800_3cpfnc',
  email: 'galaxycats510@gmail.com',
  destination: 'Osaka, Japan',
  startDate: '2026-03-11',
  endDate: '2026-03-14',
  groupSize: '3-4',
  requests: 'NICHE scenic spots, can be day trip from Osaka but has to be convenient. Not too touristy. Nature and old Japan.'
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Hidden Osaka — Nature, Shrines & Old Japan',
  subtitle: '4 days of secret waterfalls, ancient trails & traditional villages near Osaka',
  description: "Forget Dotonbori crowds and castle selfies — this Osaka trip goes deep into the side of Kansai most visitors never see. Hike through primeval forests to hidden waterfalls, wander centuries-old shrine paths, explore a traditional merchant town frozen in time, and find serenity at mountain temples. Every stop is convenient from Osaka, but feels a world away. This is old Japan at its most atmospheric — nature, quiet, and soul.",
  duration: '3 nights',
  dates: 'Mar 11 – Mar 14, 2026',
  budget: '$$',
  pace: 'Moderate',
  bestFor: 'Small Groups · Nature Lovers · Culture Seekers',
  highlights: [
    'Minoo Falls forest hike through towering cedars',
    'Sumiyoshi Taisha — Osaka\'s oldest shrine with iconic arched bridge',
    'Akame 48 Waterfalls nature trail through ninja territory',
    'Yamanobe-no-michi — Japan\'s oldest recorded road through rural Nara',
    'Hidden teahouses and local izakayas away from the tourist trail'
  ],

  essentials: [
    { title: '🌸 Early March Weather', text: 'Early-to-mid March in Osaka averages 8-14°C. Plum blossoms are in bloom and early cherry blossoms may appear. Layers are essential — mornings can be chilly, afternoons pleasant. Rain is possible, so pack a light waterproof.' },
    { title: '🚃 Getting Around', text: 'An ICOCA or Suica card works on all trains, subways, and buses. For day trips, consider the Kintetsu Rail Pass or Kansai Thru Pass for unlimited rides on private railways. Most niche spots are 30-90 minutes from central Osaka by train.' },
    { title: '🥾 Trail Tips', text: 'Several days involve forest trails. Bring comfortable walking shoes with grip — paths can be damp. Trails are well-maintained but not paved. Walking poles are overkill; good sneakers or light hikers are perfect.' },
    { title: '🍜 Casual Dining', text: 'Osaka is Japan\'s kitchen (tenka no daidokoro). Skip the tourist spots — look for tiny counter-only joints with plastic curtain doorways and Japanese-only menus. Point-and-order works great. Lunch sets (teishoku) are the best value anywhere.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-11',
      neighborhoods: 'Minoo · Shin-Osaka · Nakazakicho',
      title: 'Minoo Falls & Osaka\'s Hidden Retro District',
      description: "Start with one of Osaka's best-kept secrets: the Minoo Park forest trail leading to a stunning waterfall, all just 30 minutes from the city center. Afternoon, explore Nakazakicho — a tucked-away neighborhood of converted old houses turned into tiny cafés, bookshops, and galleries.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Minoo Park & Minoo Falls',
              description: 'Take the Hankyu line to Minoo Station and walk the 2.7km riverside trail through towering cedars and maples to Minoo Falls (Minoo-no-taki) — a stunning 33-meter waterfall cascading into an emerald pool. The path follows the Minoo River through a forested valley that feels impossibly far from the city. In March, you may catch early plum blossoms along the trail.',
              details: [
                '🚃 Hankyu Takarazuka Line to Minoo — 30 min from Umeda',
                '🥾 Trail is 2.7km one way, mostly flat paved path along the river',
                '⏱️ Allow 2-3 hours round trip with time to enjoy the waterfall',
                '🍁 Try momiji tempura (deep-fried maple leaves) from trailside vendors — a Minoo specialty'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Start by 9am to have the trail mostly to yourselves. Weekday mornings are especially quiet — you might only see a few local hikers and the occasional monkey.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakazakicho — Retro Hidden Village in the City',
              description: 'This tiny neighborhood near Umeda is a maze of pre-war wooden houses converted into indie cafés, vintage shops, and art galleries. It feels like a secret village hiding in plain sight between skyscrapers. Wander without a map — getting lost is the point.',
              details: [
                '📍 5-minute walk from Nakazakicho Station (Tanimachi Line)',
                '☕ Salon de AManTo — café in a 100-year-old townhouse with a rooftop garden',
                '📚 Tiny bookshops and record stores tucked into old machiya houses',
                '🎨 Street art and hand-painted signs on every corner'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Minoo Tofu Restaurant (Minoo area)',
              description: 'Simple, traditional tofu cuisine near the base of the Minoo trail. Handmade tofu in a quiet tatami room — the kind of place only locals know.',
              meta: '💰 $ · 📍 Near Minoo Station'
            },
            {
              type: '🍺 Dinner',
              name: 'Ura-Namba Izakaya Crawl',
              description: 'Skip Dotonbori entirely. Ura-Namba (the backstreets behind Namba) is where Osaka locals actually eat. Tiny standing bars, yakitori counters with 6 seats, and kushikatsu joints with handwritten menus. Just follow the smoke and the laughter.',
              meta: '💰 $–$$ · 📍 Ura-Namba backstreets, south of Namba Station'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.8389, lng: 135.4708, label: 'Minoo Falls', num: 1, cat: 'attraction', desc: '33-meter waterfall at the end of a beautiful forest trail' },
        { lat: 34.8352, lng: 135.4697, label: 'Minoo Park Trailhead', num: 2, cat: 'attraction', desc: 'Start of the riverside cedar forest walk' },
        { lat: 34.7093, lng: 135.5072, label: 'Nakazakicho', num: 3, cat: 'attraction', desc: 'Hidden retro neighborhood of converted old houses' },
        { lat: 34.6632, lng: 135.5010, label: 'Ura-Namba', num: 4, cat: 'food', desc: 'Local backstreet izakaya district — the real Osaka' }
      ]
    },
    {
      num: 2,
      date: '2026-03-12',
      neighborhoods: 'Sumiyoshi · Sakai · Daisen Park',
      title: 'Ancient Shrines & the Merchant City of Sakai',
      description: "Dive into old Japan without leaving the Osaka metro area. Morning at Sumiyoshi Taisha — one of Japan's oldest and most beautiful shrines, free of tourist crowds. Then head south to Sakai, a wealthy merchant city with samurai history, ancient burial mounds, and traditional knife-making workshops.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sumiyoshi Taisha Shrine',
              description: 'One of Japan\'s oldest Shinto shrines (founded in the 3rd century), Sumiyoshi Taisha is a world away from the tourist-packed shrines of Kyoto. The distinctive sumiyoshi-zukuri architecture is found nowhere else — clean cypress wood, straight lines, no Chinese influence. Cross the iconic Sorihashi arched bridge, walk through hundreds of stone lanterns, and enjoy the serene grounds. In early March, plum blossoms frame the main hall beautifully.',
              details: [
                '⛩️ Free entry · Open 6am-5pm',
                '🚃 Nankai Main Line to Sumiyoshi Taisha Station — 10 min from Namba',
                '🌺 Plum blossom garden is stunning in March',
                '📸 The Sorihashi (drum bridge) reflected in the pond is one of Japan\'s most iconic shrine images'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sakai — Japan\'s Medieval Merchant City',
              description: 'Just south of Osaka, Sakai was once the wealthiest city in Japan — a free, self-governing port that rivalled Venice. Today it\'s known for its knife-making tradition (supplying 90% of Japan\'s professional kitchen knives), tea ceremony heritage (Sen no Rikyū was born here), and the massive Daisen Kofun burial mound — the largest tomb in the world by area.',
              details: [
                '🚃 Nankai Line from Namba — 15 min to Sakai',
                '🔪 Sakai Traditional Crafts Museum — watch master knife-makers at work (free)',
                '☕ Rikyū\'s birthplace memorial — the father of the Japanese tea ceremony was from Sakai',
                '🏛️ Daisen Kofun — 5th century keyhole-shaped tomb, larger than the Egyptian pyramids by footprint'
              ]
            },
            {
              title: 'Daisen Park & Kofun Cluster',
              description: 'Walk through peaceful Daisen Park surrounding the ancient burial mound. The park has a Japanese garden, a tea house where you can experience matcha service, and views over the moat of the great kofun. The UNESCO World Heritage burial mound cluster here predates most of Japan\'s famous castles by a millennium.',
              details: [
                '🌳 Daisen Park Japanese Garden — ¥200 entry, beautifully maintained',
                '🍵 Matcha and wagashi at the park teahouse — peaceful experience',
                '📐 The kofun is so large you can only see its keyhole shape from the air'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Chitose Sushi (Sakai)',
              description: 'Sakai has a fishing heritage, and this local sushi shop near the old harbor serves incredibly fresh anago (conger eel) — a Sakai specialty. No tourists, just fishermen and locals at the counter.',
              meta: '💰 $$ · 📍 Sakai Old Town area'
            },
            {
              type: '🍷 Dinner',
              name: 'Shinsekai Kushikatsu',
              description: 'Head to Shinsekai — Osaka\'s retro entertainment district with its neon Tsutenkaku Tower. Skip the main drag and find a tiny kushikatsu (deep-fried skewer) joint in the back alleys. Rule #1: never double-dip in the communal sauce.',
              meta: '💰 $ · 📍 Shinsekai backstreets · Cash preferred'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6128, lng: 135.4929, label: 'Sumiyoshi Taisha', num: 1, cat: 'attraction', desc: 'One of Japan\'s oldest shrines with iconic arched bridge' },
        { lat: 34.5640, lng: 135.4870, label: 'Sakai Traditional Crafts Museum', num: 2, cat: 'attraction', desc: 'Watch master knife-makers — Sakai supplies 90% of Japan\'s pro knives' },
        { lat: 34.5585, lng: 135.4880, label: 'Daisen Kofun', num: 3, cat: 'attraction', desc: 'World\'s largest tomb by area — UNESCO World Heritage' },
        { lat: 34.5560, lng: 135.4920, label: 'Daisen Park', num: 4, cat: 'attraction', desc: 'Japanese garden and teahouse beside the ancient kofun' },
        { lat: 34.6520, lng: 135.5063, label: 'Shinsekai', num: 5, cat: 'food', desc: 'Retro neon district — kushikatsu back-alley joints' }
      ]
    },
    {
      num: 3,
      date: '2026-03-13',
      neighborhoods: 'Yamanobe-no-michi · Tenri · Nara countryside',
      title: 'Japan\'s Oldest Road — Rural Nara Countryside Walk',
      description: "Leave the cities behind entirely for a day on the Yamanobe-no-michi — Japan's oldest recorded road, mentioned in the 8th-century Kojiki. This ancient trail winds through persimmon orchards, past tiny village shrines, along rice paddy edges, and through groves of cedar and bamboo in the rural Nara countryside. This is old Japan as it's been for centuries.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Tenri & Start of the Yamanobe-no-michi',
              description: 'Take the Kintetsu line from Osaka-Namba to Tenri (about 50 minutes). From Tenri, the Yamanobe-no-michi trail heads south through one of the most untouched rural landscapes in the Kansai region. The first section passes Isonokami Shrine — one of Japan\'s oldest Shinto shrines, with free-roaming sacred chickens and an atmosphere of deep antiquity.',
              details: [
                '🚃 Kintetsu Line from Osaka-Namba to Tenri — ~50 min, ¥760',
                '⛩️ Isonokami Shrine — possibly Japan\'s oldest shrine, with sacred roosters roaming free',
                '🗾 The trail is well-marked with signs in English and Japanese',
                '🥾 Flat to gently rolling terrain — very walkable'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Walk Through Ancient Villages & Orchards',
              description: 'Continue south on the trail past farming villages, ancient kofun (burial mounds), roadside jizo statues, and persimmon orchards. Stop at tiny unmanned fruit stands to buy local oranges. Visit Omiwa Shrine at the trail\'s southern end — where the mountain itself is the deity. No main hall — you worship the mountain directly through a torii gate. It\'s one of the most spiritually powerful places in Japan.',
              details: [
                '🏘️ Villages along the trail have barely changed in centuries',
                '🍊 Unmanned fruit stands operate on an honor system — leave coins in the box',
                '⛩️ Omiwa Shrine — Japan\'s oldest style of worship: the mountain IS the god',
                '🗻 Mt. Miwa\'s perfect conical shape behind the shrine is stunning'
              ]
            },
            {
              title: 'Return via Sakurai',
              description: 'End the walk at JR Miwa or Sakurai Station and take the train back to Osaka. The whole walk from Tenri to Sakurai is about 16km, but you can shorten it by starting or ending at intermediate stations.',
              details: [
                '📏 Full trail: ~16km (4-5 hours walking). Can shorten to 8-10km easily',
                '🚃 JR Sakurai to Tennoji (Osaka) — ~45 min'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Trailside Village Café or Bento',
              description: 'Pack an onigiri bento from a conbini before the hike, or stop at one of the tiny cafés in the villages along the trail. There\'s a lovely soba noodle shop near Omiwa Shrine that\'s been serving hikers for decades.',
              meta: '💰 $ · 📍 Along the Yamanobe-no-michi trail'
            },
            {
              type: '🍶 Dinner',
              name: 'Hozenji Yokocho Alley',
              description: 'Back in Osaka, find dinner in Hozenji Yokocho — a narrow stone-paved alley behind Dotonbori that most tourists walk right past. Tiny kappo (chef\'s counter) restaurants, the moss-covered Hozenji Temple, and an atmosphere straight out of a Tanizaki novel. Get the chef\'s omakase at whichever place has an open seat.',
              meta: '💰 $$–$$$ · 📍 Hozenji Yokocho, behind Dotonbori · Reservations help but not always needed'
            }
          ],
          tips: [
            { type: 'tip', text: 'Bring a reusable water bottle — there are no convenience stores for long stretches of the trail, but there are occasional vending machines (Japan always delivers). The trail is mostly flat so it\'s not strenuous, just long and beautiful.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.5967, lng: 135.8378, label: 'Tenri (Trail Start)', num: 1, cat: 'attraction', desc: 'Starting point for Japan\'s oldest road' },
        { lat: 34.5950, lng: 135.8510, label: 'Isonokami Shrine', num: 2, cat: 'attraction', desc: 'Ancient shrine with sacred free-roaming roosters' },
        { lat: 34.5279, lng: 135.8531, label: 'Omiwa Shrine', num: 3, cat: 'attraction', desc: 'Mountain-worship shrine — the mountain is the deity' },
        { lat: 34.5130, lng: 135.8440, label: 'Sakurai Station', num: 4, cat: 'attraction', desc: 'Trail end point — trains back to Osaka' },
        { lat: 34.6690, lng: 135.5058, label: 'Hozenji Yokocho', num: 5, cat: 'food', desc: 'Hidden stone alley with tiny kappo restaurants' }
      ]
    },
    {
      num: 4,
      date: '2026-03-14',
      neighborhoods: 'Katsuoji · Expo Park · Departure',
      title: 'Daruma Temple, Morning Forest & Farewell',
      description: "Your final morning takes you to one of Kansai's quirkiest and most scenic temples — Katsuoji, the 'Temple of Winners,' carpeted with thousands of daruma dolls nestled among forested hills. A peaceful, surreal farewell to your hidden Japan adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Katsuoji Temple — The Daruma Temple',
              description: 'Hidden in the forested hills north of Osaka, Katsuoji is covered with thousands of daruma dolls placed by visitors praying for success. The temple grounds span a mountainside garden with pagodas, ponds, and forest trails — all eerily quiet on weekday mornings. The combination of ancient architecture, dense forest, and thousands of little red daruma faces is unlike anything else in Japan.',
              details: [
                '🚃 Kita-Osaka Kyuko Line to Senri-Chuo, then bus #29 (~30 min total from Umeda)',
                '🎯 ¥400 entry · Open 8am-5pm',
                '🔴 Buy a daruma, make a wish, paint in one eye — return to paint the other when it comes true',
                '📸 The stairways covered in daruma among autumn leaves are surreal (equally beautiful in early spring)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast/Brunch',
              name: 'Brooklyn Roasting Company Kitahama',
              description: 'Excellent specialty coffee in a beautifully renovated historic building along the Tosabori River. A calm, non-touristy start to the morning before heading to the temple.',
              meta: '💰 $ · 📍 Kitahama, Chuo-ku'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Stroll & Departure',
              description: 'If time allows before your departure, take a final walk through Osaka. The Nakanoshima area between the two rivers has beautiful rose gardens (early blooms in March), the elegant Central Public Hall building, and quiet riverside paths. Or simply grab one last bowl of udon and head to the station with a full heart.',
              details: [
                '🌹 Nakanoshima Rose Garden — free, peaceful riverside walk',
                '🏛️ Osaka Central Public Hall — gorgeous 1918 neo-Renaissance building',
                '🚅 Shin-Osaka for shinkansen or Kansai Airport for flights'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Imai Honten Udon (Dotombori)',
              description: 'If you only eat one thing on your way out, make it the kitsune udon at Imai — serving Osaka\'s signature dish since 1946. The broth is kelp-forward, the fried tofu is sweet and plump, and the handmade noodles are silky. It\'s a 2-minute walk from Dotonbori but feels like a different world inside.',
              meta: '💰 $ · 📍 Dotombori · Cash only · Open since 1946'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pick up omiyage (souvenirs) at Shin-Osaka Station before departing — the depachika (underground food hall) has beautifully packaged local sweets. 551 Horai\'s butaman (pork buns) are the iconic Osaka omiyage.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.8619, lng: 135.5047, label: 'Katsuoji Temple', num: 1, cat: 'attraction', desc: 'Forest temple covered in thousands of daruma dolls' },
        { lat: 34.6920, lng: 135.5060, label: 'Nakanoshima', num: 2, cat: 'attraction', desc: 'River island with rose garden and historic architecture' },
        { lat: 34.6937, lng: 135.5022, label: 'Central Public Hall', num: 3, cat: 'attraction', desc: 'Gorgeous 1918 neo-Renaissance building' },
        { lat: 34.6666, lng: 135.5015, label: 'Imai Honten Udon', num: 4, cat: 'food', desc: 'Osaka\'s signature kitsune udon since 1946' },
        { lat: 34.7334, lng: 135.5001, label: 'Shin-Osaka Station', num: 5, cat: 'attraction', desc: 'Departure point — shinkansen hub' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥5,000–8,000/night', midrange: '¥10,000–20,000/night', luxury: '¥25,000–50,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000–3,500/day', midrange: '¥4,000–8,000/day', luxury: '¥10,000–20,000/day' },
    { category: 'Transport', budget: '¥1,000–2,000/day', midrange: '¥2,000–3,500/day', luxury: '¥5,000–10,000/day (taxi)' },
    { category: 'Activities', budget: '¥0–500/day', midrange: '¥500–2,000/day', luxury: '¥3,000–8,000/day' },
    { category: '4-Day Total (per person)', budget: '¥35,000–55,000', midrange: '¥65,000–130,000', luxury: '¥170,000–350,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) — Nankai Rapi:t express to Namba in 38 min (¥1,450)', 'Itami/Osaka Airport (ITM) — monorail + subway to Umeda in 40 min (domestic flights)', 'From Tokyo: Shinkansen Nozomi to Shin-Osaka, 2h30m (¥13,870)'] },
    { title: '🏨 Where to Stay', items: ['Shinsaibashi/Namba — central, walkable to food and nightlife', 'Kitahama/Nakanoshima — quieter, riverside, more local feel', 'Budget: Guest houses in Shinsekai or Tennoji from ¥3,000/night', 'Splurge: Conrad Osaka or The Ritz-Carlton for river views'] },
    { title: '🌡️ March Weather', items: ['Average highs 12-15°C (54-59°F), lows 4-7°C (39-45°F)', 'Plum blossoms peak in early-mid March', 'Cherry blossoms usually begin late March (luck-dependent)', 'Occasional rain — pack a compact umbrella'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless but many small restaurants and temples are cash-only', 'ATMs at 7-Eleven and Japan Post accept international cards', 'Budget roughly ¥10,000-15,000/day per person for comfortable travel', 'No tipping in Japan — it can actually be considered rude'] },
    { title: '📱 Useful Tips', items: ['Get a Suica/ICOCA IC card at any station — tap-on/tap-off for all transit', 'Google Maps works perfectly for train routing in Japan', 'Download Google Translate with Japanese offline pack', 'Konbini (convenience stores) are your best friend — 7-Eleven, Lawson, FamilyMart have great food, ATMs, and essentials 24/7'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
