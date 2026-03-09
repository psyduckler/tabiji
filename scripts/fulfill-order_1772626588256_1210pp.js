const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772626588256_1210pp',
  email: 'galaxycats510@gmail.com',
  destination: 'Kyoto, Japan',
  startDate: '2026-03-13',
  endDate: '2026-03-13',
  groupSize: '3-4',
  requests: 'Day trip to Kyoto from Osaka. Explore Arashiyama but NO bamboo grove. Include Uji if time allows (not mandatory).'
};

const itineraryData = {
  destination: 'Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Arashiyama & Uji — A Quiet Side of Kyoto',
  subtitle: 'One unhurried day for 3-4 friends: temple gardens, river views, monkeys, and the best matcha of your life',
  description: "Kyoto in March is quietly magical — before the crowds of cherry blossom season descend, the city breathes easy. This day trip from Osaka skips the bamboo grove (smart move) and leans into Arashiyama's gentler charms: the UNESCO-listed temple garden at Tenryu-ji, the gentle arc of Togetsukyo Bridge over a misty river, and 120 snow-macaque monkeys with panoramic mountain views. If your legs still have something left, Uji pulls you south for matcha tea culture and the gilded Phoenix Hall of Byodoin — one of Japan's most breathtaking temples. Come home to Osaka with tired feet and a full heart.",
  duration: '1 Day',
  dates: 'March 13, 2026',
  budget: '$–$$',
  pace: 'Relaxed',
  bestFor: 'Friends',

  highlights: [
    'Tenryu-ji garden — UNESCO World Heritage zen masterpiece without the bamboo rush',
    'Togetsukyo Bridge at its most tranquil (pre-cherry-blossom season)',
    'Iwatayama Monkey Park — 120 wild macaques and panoramic Kyoto views',
    'Kimono Forest light installation near the riverside Randen tram stop',
    'Byodoin Temple in Uji — the Phoenix Hall on the 10-yen coin, in real life'
  ],

  essentials: [
    {
      title: '🚆 Getting There from Osaka',
      text: 'Take the JR Sagano line from Osaka Station (via Kyoto) to Saga-Arashiyama — about 60-75 minutes total, under ¥1,000. Or take the Hankyu line to Katsura, transfer to Arashiyama line. IC cards (Suica/ICOCA) work everywhere — tap in, tap out, no fuss.'
    },
    {
      title: '🌸 March Conditions',
      text: 'Mid-March in Kyoto is crisp and cool — expect 8–15°C. Layers are your friend. Early plum blossoms may be around Arashiyama; sakura usually peaks late March to early April, so you might catch the very first hints. The upside: fewer tourists than peak bloom season.'
    },
    {
      title: '🐒 Monkey Park Heads Up',
      text: 'Iwatayama Monkey Park requires a 20-minute uphill hike. Sturdy shoes recommended. Entry is ¥550 per person. Inside the enclosed feeding area, YOU are the one inside the cage — the monkeys roam free outside. It\'s as funny as it sounds.'
    },
    {
      title: '🍵 Uji Is Worth It',
      text: 'If you\'re running low on time or energy after Arashiyama, Uji is optional — but it\'s genuinely special. The matcha here is the real deal (Uji is Japan\'s matcha capital), and Byodoin is stunning. Budget about 2 hours. Train from Arashiyama to Uji takes about 50-60 min via Kyoto Station.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-13',
      neighborhoods: 'Arashiyama · Sagano · Uji',
      title: 'Arashiyama at Its Finest — Then Uji\'s Matcha Magic',
      description: "A perfectly paced day through two of Kyoto's most beloved neighborhoods, intentionally skipping the bamboo grove crowds for the quieter, deeper experiences Arashiyama has to offer — then south to Uji for tea, temples, and a memorable close.",
      timeBlocks: [
        {
          label: 'Morning (9:00–11:30am)',
          activities: [
            {
              title: 'Kimono Forest — The Gentle Opening Act',
              description: 'Start at the Randen Arashiyama terminus, where 600 illuminated cylinders wrapped in traditional kimono fabric line the path. It\'s free, open all day, and genuinely lovely — especially in the cool morning light. Sets the mood perfectly without requiring any tickets or planning.',
              details: [
                '📍 Adjacent to Randen Arashiyama Station — impossible to miss',
                '🎨 600 kimono cylinders, each a different pattern — take your time wandering',
                '🆓 Free and open all hours — no crowds at 9am',
                '📸 Great group photo spot before the day gets going'
              ]
            },
            {
              title: 'Tenryu-ji Garden — A UNESCO Masterpiece',
              description: 'This is the crown jewel of Arashiyama. Tenryu-ji\'s garden was designed in the 14th century and is considered one of the finest in Japan — a serene composition of pond, raked gravel, and borrowed mountain scenery. Walk slowly. Sit by the water. Let the quiet settle in. The temple buildings are beautiful too, though the garden is the real draw.',
              details: [
                '⏰ Opens at 8:30am — arrive early before groups arrive',
                '💴 Garden only: ¥500/person; with buildings: ¥800/person',
                '🌿 The pond garden is designed to frame the mountains behind as part of the composition (shakkei — borrowed scenery)',
                '🌸 Early plum blossoms possible in mid-March; very first sakura buds may appear',
                '⏱️ Budget 60–90 minutes — it rewards slow wandering'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Don\'t exit Tenryu-ji the way you came in. The back exit opens directly onto the bamboo grove path (which you\'re skipping) — instead, keep to the garden and exit toward the main gate for the river.' }
          ]
        },
        {
          label: 'Late Morning (11:30am–12:30pm)',
          activities: [
            {
              title: 'Togetsukyo Bridge & Riverside Walk',
              description: 'The "Moon Crossing Bridge" spans the Oi River with Arashiyama\'s forested mountains as the backdrop. March light is soft and clear — this is a beautiful walk. Cross the bridge, then wander the southern bank. The riverside is calm and unhurried, with mountain views in every direction.',
              details: [
                '🌉 The bridge is about 150 meters long — short enough to cross twice',
                '🏔️ The mountains change color by season; in March, they\'re a deep, restful green',
                '📸 Classic photo: midpoint of the bridge looking upstream toward the mountains',
                '🦅 Keep an eye out for cormorant fishermen on the river in cooler months'
              ]
            }
          ]
        },
        {
          label: 'Lunch (12:30–1:30pm)',
          activities: [],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hiranoya Honke (or riverside tofu spot)',
              description: 'Arashiyama has excellent tofu cuisine — a Kyoto specialty. Hiranoya Honke has been serving kaiseki and tofu dishes since 1727, with riverside garden seating. For something more casual, grab yudofu (simmered tofu) from one of the small restaurants along Saga-Toriimoto street — warming and perfect for a cool March day.',
              meta: '💰 $–$$ · 📍 Along the riverside near Togetsukyo · No reservations needed for casual spots'
            }
          ],
          tips: [
            { type: 'tip', text: 'Arashiyama has lots of small shops selling matcha soft serve, mochi, and sesame snacks. Perfect for a walk-and-eat moment between lunch and the monkey park.' }
          ]
        },
        {
          label: 'Early Afternoon (1:30–3:00pm)',
          activities: [
            {
              title: 'Iwatayama Monkey Park — Best Surprise of the Day',
              description: 'This is the hidden gem of Arashiyama. A 20-minute uphill hike through forest brings you to a hilltop where 120 wild Japanese macaques roam freely. At the top, there\'s a small enclosed hut where you can feed them through the bars (you\'re inside; monkeys are outside — the twist is brilliant). The views over Kyoto from up here are genuinely stunning.',
              details: [
                '💴 Entry: ¥550/person',
                '🥾 Uphill hike takes 20-25 min each way — wear comfortable shoes',
                '🐒 These are wild macaques — don\'t try to touch them outside the feeding hut',
                '🏙️ Views from the top stretch all the way to downtown Kyoto',
                '⏱️ Allow 90 minutes total (hike up + time with monkeys + hike down)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon → Uji (3:00–6:30pm)',
          activities: [
            {
              title: 'Train to Uji — Japan\'s Matcha Capital',
              description: 'Head to Uji via JR from Saga-Arashiyama: take the JR Sagano line east to Kyoto Station, then the JR Nara line south to Uji. About 50-60 minutes total. A perfect time to sit, decompress, and compare monkey park notes.',
              details: [
                '🚆 Saga-Arashiyama → Kyoto → Uji (JR all the way, IC card fine)',
                '⏱️ About 50-60 minutes; trains run frequently',
                '☕ Grab a canned coffee from the station vending machine for the ride'
              ]
            },
            {
              title: 'Byodoin Temple — The Phoenix Hall',
              description: 'You\'ve seen it on the 10-yen coin — now stand in front of it. Byodoin\'s Phoenix Hall sits reflected in a mirror pond, looking impossibly perfect. Built in 1053, it somehow still feels otherworldly. The symmetry, the gilded phoenix statues on the roof, the reflection in the water — arrive late afternoon when the light goes golden and you\'ll understand why people come just for this.',
              details: [
                '💴 Garden entry: ¥700; Phoenix Hall interior tour: ¥300 extra (worth it, book at the gate)',
                '⏰ Last entry is 5:15pm — plan to arrive by 4:00-4:30pm to not feel rushed',
                '📸 The reflection shot requires the afternoon sun — perfect timing for your arrival',
                '🏛️ The interior has original Heian-period paintings on the wooden walls — rare surviving examples'
              ]
            },
            {
              title: 'Uji Bridge & Matcha Shopping',
              description: 'Uji Bridge is one of Japan\'s oldest bridges and a lovely walk over the Uji River. The streets around it are lined with matcha tea shops — this is the real source of Kyoto\'s famous matcha. Pick up loose-leaf tea, matcha KitKats, and whatever matcha dessert catches your eye. Tsujiri and Nakamuratsuen are the legacy names; Itohkyuemon has excellent sweets.',
              details: [
                '🍵 Uji matcha is a protected designation — what\'s sold here is the benchmark',
                '🛍️ Great souvenir shopping: tea tins, matcha powder, matcha sweets',
                '🌉 Uji Bridge itself is lovely — nice walk before the shops close',
                '⏰ Most tea shops close around 5:30–6pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha Treat',
              name: 'Itohkyuemon or Tsujiri Uji',
              description: 'Order a matcha parfait or matcha soft serve at one of Uji\'s famous tea houses. Itohkyuemon has beautiful matcha desserts and a lovely sit-down atmosphere. Tsujiri is the classic — their matcha soft serve is legendary. The perfect sweet close to the trip.',
              meta: '💰 $ · 📍 Uji bridge-side streets · No reservations needed'
            }
          ]
        },
        {
          label: 'Evening — Return to Osaka (6:30pm+)',
          activities: [
            {
              title: 'Train Back to Osaka',
              description: 'From Uji Station, JR Nara line north to Kyoto Station, then Shinkansen or JR Kyoto–Osaka line back to Osaka. You\'ll be back in time for a relaxed dinner in Namba or Shinsaibashi — possibly the best ramen of your lives after a day well spent.',
              details: [
                '🚆 Uji → Kyoto → Osaka: about 60 minutes total',
                '🍜 Osaka dinner options are endless — Dotonbori for takoyaki and ramen is a classic homecoming',
                '💤 You earned it — early night or late izakaya, your call'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0127, lng: 135.6774, label: 'Kimono Forest', num: 1, cat: 'attraction', desc: '600 illuminated kimono cylinders near Randen station — free, magical' },
        { lat: 35.0170, lng: 135.6726, label: 'Tenryu-ji Garden', num: 2, cat: 'attraction', desc: 'UNESCO garden masterpiece — zen pond, raked gravel, mountain views' },
        { lat: 35.0100, lng: 135.6778, label: 'Togetsukyo Bridge', num: 3, cat: 'attraction', desc: 'The Moon Crossing Bridge — iconic Arashiyama landmark over the Oi River' },
        { lat: 35.0054, lng: 135.6726, label: 'Iwatayama Monkey Park', num: 4, cat: 'attraction', desc: '120 wild macaques + stunning panoramic views of Kyoto (20min hike up)' },
        { lat: 35.0130, lng: 135.6750, label: 'Arashiyama Lunch District', num: 5, cat: 'food', desc: 'Tofu restaurants and riverside casual dining along Saga-Toriimoto' },
        { lat: 34.8894, lng: 135.8071, label: 'Byodoin Temple', num: 6, cat: 'attraction', desc: 'The Phoenix Hall — the 10-yen coin temple, reflected in a perfect mirror pond' },
        { lat: 34.8892, lng: 135.8052, label: 'Uji Bridge & Tea Shops', num: 7, cat: 'attraction', desc: 'One of Japan\'s oldest bridges + Uji matcha shopping (Tsujiri, Itohkyuemon)' }
      ]
    }
  ],

  practicalInfo: [
    {
      title: '🚆 Getting Around',
      items: [
        'From Osaka to Arashiyama: JR Sagano line via Kyoto Station (60-75 min, ~¥990)',
        'IC cards (ICOCA / Suica) work on all trains and buses — no need for individual tickets',
        'Arashiyama is very walkable — most sights are within 20 minutes on foot',
        'Uji from Arashiyama: JR Sagano east to Kyoto, then JR Nara line south (50-60 min)',
        'Back to Osaka from Uji: JR Nara line north to Kyoto, then Shinkansen or JR Kyoto Line (~60 min)'
      ]
    },
    {
      title: '🌸 March in Kyoto',
      items: [
        'Average temperatures: 8–15°C — bring a light jacket and layers',
        'Plum blossoms (ume) may be finishing up; very first sakura buds possible late March',
        'March is before peak cherry blossom season — fewer tourists than April',
        'Rain gear is handy — March can be unpredictable, but rarely heavy'
      ]
    },
    {
      title: '💴 Costs & Budget',
      items: [
        'Tenryu-ji garden: ¥500/person',
        'Iwatayama Monkey Park: ¥550/person',
        'Byodoin Temple: ¥700/person (+¥300 for interior tour)',
        'Train (Osaka ↔ Arashiyama ↔ Uji ↔ Osaka): ~¥2,500/person total',
        'Lunch + matcha treats: ¥2,000–4,000/person',
        'Full day total per person: roughly ¥7,000–12,000 (~$45–80 USD)'
      ]
    },
    {
      title: '📱 Tips',
      items: [
        'Arashiyama is cash-friendly but most major spots accept IC cards or credit cards',
        'Google Maps works great for train navigation in Japan — just type the destination',
        'Uji Bridge area shops close around 5:30–6pm — arrive at Uji by 3:30pm at the latest',
        'The monkey park requires energy — save it by not rushing lunch beforehand'
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Order fulfilled!');
    console.log('Slug:', result.slug);
    console.log('URL:', result.url);
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
