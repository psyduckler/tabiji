const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772717416075_8bzhi2',
  email: 'galaxycats510@gmail.com',
  destination: 'Nikko, Tochigi, Japan',
  startDate: '2026-03-18',
  endDate: '2026-03-18',
  groupSize: '3-4',
  requests: 'Day trip to Nikko FROM Tokyo. So far I have Shinkyo Bridge, Kegon Waterfalls, and Lake Chuzenji that I wish to see. Help add timings too.'
};

const itineraryData = {
  destination: 'Nikko, Japan',
  countryEmoji: '🇯🇵',
  title: 'A Perfect Day in Nikko — Shrines, Waterfalls & Mountain Lakes',
  subtitle: 'A full day trip from Tokyo through Nikko\'s UNESCO heritage, thundering falls, and serene alpine scenery',
  description: "Nikko is where nature and history collide in the most dramatic way — towering cedar forests guard a UNESCO World Heritage shrine complex, a 97-metre waterfall plunges into a misty gorge, and a volcanic lake sits cradled by mountains at 1,269 metres elevation. This day trip from Tokyo packs in all four of Nikko's crown jewels — Shinkyo Bridge, Toshogu Shrine, Kegon Falls, and Lake Chuzenji — with realistic timing so you see everything without rushing. March means fewer crowds, crisp mountain air, and the first hints of spring.",
  duration: '1 day',
  dates: 'Mar 18, 2026',
  budget: '$$',
  pace: 'Active',
  bestFor: 'Small Groups · Adventure · Culture',
  highlights: [
    'Toshogu Shrine — Japan\'s most lavishly decorated shrine, home of the famous three wise monkeys',
    'Kegon Falls — one of Japan\'s top three waterfalls, 97m drop into a misty gorge',
    'Lake Chuzenji — serene volcanic lake at 1,269m elevation ringed by mountains',
    'Shinkyo Bridge — sacred vermilion bridge spanning the Daiya River gorge',
    'Irohazaka Winding Road — 48 hairpin curves climbing 400m through the mountains'
  ],

  essentials: [
    { title: '🚃 Getting There', text: 'Take the Tobu Railway Limited Express "Revaty Kegon" from Tobu Asakusa Station — direct to Tobu-Nikko in about 1 hour 50 minutes. Costs around ¥2,800 one-way (reserved seat). Alternatively, JR runs via Shinjuku to JR Nikko with a transfer at Utsunomiya. The Tobu line is more direct and frequent.' },
    { title: '🎫 Passes & Tickets', text: 'The Tobu "All Nikko Pass" (¥4,780 from Asakusa) covers round-trip train + unlimited bus in Nikko including the route to Lake Chuzenji. Highly recommended — it saves money and hassle. Buy it at Tobu Asakusa Station the morning of your trip.' },
    { title: '🌡️ March Weather', text: 'Nikko sits at 600m elevation (town) to 1,270m (Lake Chuzenji). Expect 5-10°C in town, near freezing at the lake. Dress in warm layers, bring a windproof jacket, and wear comfortable walking shoes. Snow is possible at higher elevations.' },
    { title: '🍜 Dining in Nikko', text: 'Nikko is famous for yuba (tofu skin) — try it in soba, as sashimi, or in a bento. The area around Toshogu has several casual restaurants. Lunch near the shrine area before heading up to the lake keeps the timing smooth.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-18',
      neighborhoods: 'Asakusa · Nikko Town · Oku-Nikko',
      title: 'Tokyo → Nikko: Shrines, Falls & Mountain Lake',
      description: "An early start from Tokyo gets you to Nikko by mid-morning. You'll walk the sacred bridge, explore Japan's most ornate shrine, ride the famous winding mountain road, stand at the base of a 97-metre waterfall, and relax by a volcanic lake — all before heading back to Tokyo for dinner.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Tobu Asakusa Station → Tobu-Nikko',
              description: 'Catch the 7:30 AM Limited Express "Revaty Kegon" from Tobu Asakusa Station. The train is comfortable with reserved seating and takes about 1 hour 50 minutes direct to Tobu-Nikko. Watch Tokyo\'s sprawl give way to rice paddies and cedar forests as you head north into Tochigi Prefecture.',
              details: [
                '🕖 Depart Tobu Asakusa at 7:30 AM — arrive Tobu-Nikko ~9:20 AM',
                '🎫 Buy the All Nikko Pass at the Tobu ticket counter before boarding',
                '💺 Reserved seats recommended — the train can fill up',
                '📍 Tobu Asakusa Station is right next to Sensoji Temple — not the same as Tokyo Metro Asakusa'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Grab onigiri or a bento from the konbini at Asakusa Station for a breakfast-on-the-go. The train has no food car, but eating on trains in Japan is perfectly normal.' }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkyo Bridge',
              description: 'Start your Nikko exploration at this iconic sacred bridge spanning the Daiya River gorge. The vermilion-lacquered bridge against the forested ravine is one of Nikko\'s most photographed scenes. You can walk across for a small fee or admire it from the road for free — both views are stunning.',
              details: [
                '🌉 ¥300 to walk across, or free views from the road and riverbank',
                '📸 Best photo angle: from the modern bridge just downstream',
                '⏱️ Allow 15-20 minutes here',
                '🚶 10-minute walk from Tobu-Nikko Station, or one bus stop'
              ]
            },
            {
              title: 'Toshogu Shrine',
              description: 'The crown jewel of Nikko — a UNESCO World Heritage Site and the final resting place of Tokugawa Ieyasu, the founder of the Tokugawa shogunate. Unlike Japan\'s typically minimalist shrines, Toshogu is an explosion of gold leaf, intricate carvings, and vivid colours. Don\'t miss the famous "see no evil, speak no evil, hear no evil" three wise monkeys carving and the Sleeping Cat (Nemuri-neko).',
              details: [
                '⛩️ Admission: ¥1,300 adults · Open 9:00 AM – 4:00 PM (April–Oct until 5 PM)',
                '🐒 Three Wise Monkeys carving is on the Sacred Stable building',
                '😴 Nemuri-neko (Sleeping Cat) guards the path to Ieyasu\'s tomb — don\'t miss the 207-step climb',
                '🌲 The approach through 600-year-old cedar trees is magical',
                '⏱️ Allow 1.5–2 hours to explore properly'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Toshogu is massive — pick up the English-language map at the entrance. The tomb climb (207 stone steps) is worth it for the peaceful forest atmosphere, even if the tomb itself is modest.' }
          ]
        },
        {
          label: 'Lunch',
          activities: [
            {
              title: 'Lunch in Nikko Town',
              description: 'Refuel near the shrine area before heading up the mountain. The streets around Toshogu have several casual restaurants serving Nikko\'s famous yuba (tofu skin) dishes, hearty soba noodles, and Japanese comfort food.',
              details: [
                '🍜 Try yuba soba — Nikko\'s signature dish combining local specialties',
                '🏠 Restaurants along the main road between the station and shrine area',
                '⏱️ Keep lunch to about 45 minutes to stay on schedule'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Nikko Yuba Cuisine (various restaurants)',
              description: 'The shrine area has several excellent casual restaurants. Komekichi Kozushi and Yuba Zen are local favourites for yuba set meals. Hippari Dako is great for casual gyoza and ramen.',
              meta: '💰 ¥1,000–1,800 · 📍 Along the main road near Toshogu entrance'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bus to Lake Chuzenji via Irohazaka',
              description: 'Catch the bus from Nikko town up to Chuzenji Onsen. The 40-minute ride climbs the famous Irohazaka Winding Road — 48 hairpin curves that gain 400 metres of elevation through dense forest. Each curve is named after a character from the Japanese alphabet. It\'s an adventure in itself.',
              details: [
                '🚌 Bus from Tobu-Nikko or JR Nikko Station to Chuzenji Onsen (~40 min)',
                '🎫 Covered by the All Nikko Pass',
                '🔄 The uphill road (Second Irohazaka) has 20 curves; downhill (First) has 28',
                '📍 Get off at Chuzenji Onsen bus stop for Kegon Falls'
              ]
            },
            {
              title: 'Kegon Falls',
              description: 'One of Japan\'s three most beautiful waterfalls. The Daiya River plunges 97 metres from Lake Chuzenji\'s outlet into a dramatic gorge. Take the elevator down to the observation platform at the base for the most powerful view — the thundering water, rising mist, and surrounding cliffs are awe-inspiring.',
              details: [
                '🛗 Elevator to base platform: ¥570 adults · Highly recommended',
                '💧 97-metre drop — most impressive during spring snowmelt',
                '🌫️ In March, you may see frozen sections alongside flowing water — spectacular',
                '⏱️ Allow 30–45 minutes including elevator wait',
                '📍 3-minute walk from Chuzenji Onsen bus stop'
              ]
            },
            {
              title: 'Lake Chuzenji Lakeside Walk',
              description: 'After the falls, walk to the shore of Lake Chuzenji — a stunning volcanic lake formed 20,000 years ago when Mt. Nantai erupted and dammed the valley. At 1,269 metres elevation, the air is crisp and the mountain reflections on the water are breathtaking. Stroll the lakeside promenade and soak in the tranquility.',
              details: [
                '🏔️ Mt. Nantai (2,486m) towers over the lake — sacred mountain of Nikko',
                '🚢 Sightseeing boats run on the lake (seasonal — check March availability)',
                '📸 The view from the eastern shore looking west toward Mt. Nantai is iconic',
                '⏱️ Allow 45–60 minutes for a relaxed lakeside walk',
                '🍵 Warm up with matcha or coffee at one of the lakeside cafés'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'March at Lake Chuzenji can be significantly colder than Nikko town — bring an extra layer. The elevation difference means it can be 5-8°C cooler up here.' }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Chuzenji Temple (Tachiki Kannon)',
              description: 'If time permits, visit Chuzenji Temple on the lakeside — a sub-temple of Rinnoji with a beautiful wooden Kannon statue carved directly from a standing tree. The temple grounds offer peaceful lake views and a moment of reflection before heading back.',
              details: [
                '⛩️ ¥500 admission · Small but beautiful',
                '📍 Short walk along the lakeshore from the bus stop',
                '⏱️ Allow 20 minutes'
              ]
            },
            {
              title: 'Bus Back to Tobu-Nikko Station',
              description: 'Catch the bus back down the mountain via the First Irohazaka (28 curves on the descent — different route than the way up). Aim for the 4:00–4:30 PM bus to have comfortable time for the return train.',
              details: [
                '🚌 Bus from Chuzenji Onsen back to Tobu-Nikko (~40 min)',
                '🎫 Covered by the All Nikko Pass',
                '🔄 The descent route is different from the ascent — enjoy new scenery'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return Train to Tokyo',
              description: 'Board the Limited Express back to Asakusa. You\'ll arrive in Tokyo around 7:00–7:30 PM with the whole evening ahead for dinner in the city.',
              details: [
                '🚃 Tobu Limited Express departs roughly every 30 min — last express around 5:30-6:00 PM',
                '🕖 Arrive Tobu Asakusa ~7:00–7:30 PM',
                '💤 The train ride is a perfect time to rest after a big day of walking'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dinner in Tokyo (Asakusa or your neighbourhood)',
              description: 'You\'ll arrive back in Asakusa — one of Tokyo\'s best areas for casual evening dining. Try Hoppy Street (Hoppy-dori) for lively izakaya atmosphere with yakitori and beer, or head to Sometaro for DIY okonomiyaki in a charming old house.',
              meta: '💰 ¥1,500–3,000/person · 📍 Asakusa area · Casual & lively'
            }
          ],
          tips: [
            { type: 'tip', text: 'Asakusa at night is magical — Sensoji Temple lit up with almost no crowds is one of Tokyo\'s best-kept secrets. Walk through the Kaminarimon gate and Nakamise-dori after dinner.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7500, lng: 139.5981, label: 'Tobu-Nikko Station', num: 1, cat: 'transport', desc: 'Main station — starting point for Nikko exploration' },
        { lat: 36.7577, lng: 139.6005, label: 'Shinkyo Bridge', num: 2, cat: 'attraction', desc: 'Sacred vermilion bridge over the Daiya River gorge' },
        { lat: 36.7581, lng: 139.5999, label: 'Toshogu Shrine', num: 3, cat: 'attraction', desc: 'UNESCO World Heritage shrine — Japan\'s most ornate' },
        { lat: 36.7383, lng: 139.4997, label: 'Kegon Falls', num: 4, cat: 'attraction', desc: '97m waterfall — one of Japan\'s top three falls' },
        { lat: 36.7401, lng: 139.4820, label: 'Lake Chuzenji', num: 5, cat: 'attraction', desc: 'Volcanic lake at 1,269m surrounded by mountains' },
        { lat: 36.7394, lng: 139.4890, label: 'Chuzenji Temple', num: 6, cat: 'attraction', desc: 'Lakeside temple with Kannon carved from a standing tree' },
        { lat: 35.7101, lng: 139.8107, label: 'Tobu Asakusa Station', num: 7, cat: 'transport', desc: 'Departure/return point in Tokyo' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Train (round trip)', budget: '¥2,800 (local trains)', midrange: '¥4,780 (All Nikko Pass)', luxury: '¥5,600 (Limited Express reserved)' },
    { category: 'Shrine Admission', budget: '¥1,300', midrange: '¥1,300', luxury: '¥1,300' },
    { category: 'Kegon Falls Elevator', budget: '—', midrange: '¥570', luxury: '¥570' },
    { category: 'Meals', budget: '¥2,000', midrange: '¥3,500', luxury: '¥6,000' },
    { category: 'Day Total (per person)', budget: '¥6,100 (~$41)', midrange: '¥10,150 (~$68)', luxury: '¥13,470 (~$90)' }
  ],

  practicalInfo: [
    { title: '🚃 Train Options', items: ['Tobu Limited Express "Revaty Kegon" from Asakusa — 1h50m, direct, ~¥2,800 one-way', 'JR from Shinjuku via Utsunomiya — 2h+, requires transfer, covered by JR Pass', 'Tobu "All Nikko Pass" (¥4,780) — best value: round-trip train + unlimited Nikko buses'] },
    { title: '🚌 Getting Around Nikko', items: ['Local buses connect the station, shrines, and Lake Chuzenji area', 'Chuzenji Onsen bus: ~40 min from station, runs every 20-30 min', 'All covered by the All Nikko Pass — just show it to the driver', 'Walking between Shinkyo Bridge and Toshogu is easy (~10 min)'] },
    { title: '🌡️ Weather & Packing', items: ['March in Nikko town: 5-12°C — cool and crisp', 'Lake Chuzenji area: 0-7°C — significantly colder at elevation', 'Dress in warm layers, bring a windproof jacket', 'Comfortable walking shoes essential — shrine paths are uneven stone', 'Possible snow at higher elevations — check forecast day-of'] },
    { title: '💡 Tips for Groups', items: ['Buy All Nikko Passes together at the counter — faster', 'Coin lockers at Tobu-Nikko Station for bags (¥400-600)', 'Shrine paths are uneven — watch footing on wet stone', 'ATMs at 7-Eleven in Nikko town accept international cards', 'Cash is king for small shops and temple admissions'] }
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
