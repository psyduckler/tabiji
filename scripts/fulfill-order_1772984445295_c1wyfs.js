const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772984445295_c1wyfs',
  email: 'hidenseeksonu@gmail.com',
  destination: 'Ubud, Gianyar Regency, Bali, Indonesia',
  startDate: '2026-06-25',
  endDate: '2026-07-04',
  groupSize: '3-4',
  requests: ''
};

const itineraryData = {
  destination: 'Ubud, Bali, Indonesia',
  countryEmoji: '🇮🇩',
  title: 'The Heart of Bali — Rice Terraces, Temples & Tropical Magic',
  subtitle: '10 days of sacred water temples, emerald rice paddies, hidden waterfalls & Balinese soul for 3–4 travellers',
  description: "Ubud is where Bali drops the beach-bar mask and shows you its real face — ancient temples draped in moss, rice terraces that cascade like green staircases to the sky, and a creative energy that hums through every laneway. This 10-day itinerary takes you deep into Bali's cultural heartland: sunrise treks on a volcanic crater, purification rituals at thousand-year-old springs, hands-on cooking classes in jungle kitchens, white-water rafting through rainforest gorges, and long evenings watching fire dances under the stars. With 10 days, you'll have time to explore far beyond Ubud — day trips to the sacred east coast, dramatic northern waterfalls, and the otherworldly Gate of Heaven. This is Bali as it was meant to be experienced.",
  duration: '9 nights',
  dates: 'Jun 25 – Jul 4, 2026',
  budget: '$–$$',
  pace: 'Moderate',
  bestFor: 'Friends / Small Groups',
  highlights: [
    'Sunrise trek to the rim of Mount Batur volcano',
    'Purification ceremony at Tirta Empul holy spring temple',
    'Tegallalang Rice Terraces at golden hour',
    'Balinese cooking class with market visit',
    'Kecak fire dance at Ubud Palace',
    'White-water rafting the Ayung River through jungle',
    'Hidden waterfalls — Tukad Cepung, Tibumana & Kanto Lampo',
    'Gate of Heaven at Lempuyang Temple',
    'Sacred Monkey Forest Sanctuary',
    'Traditional Balinese spa & yoga at The Yoga Barn'
  ],

  essentials: [
    { title: '🌧️ Dry Season Bliss', text: 'Late June through early July is peak dry season — expect warm days (27–30°C), low humidity, and clear skies. Perfect for trekking and outdoor temples. Mornings can be cool in the highlands, so bring a light layer.' },
    { title: '🛵 Getting Around', text: 'Hire a private driver for day trips (IDR 500–700K/day, ~$30–45 USD for the car). For around town, rent scooters if comfortable (IDR 70K/day) or use Grab/GoJek. Roads are narrow and traffic can be chaotic — a driver is the stress-free choice.' },
    { title: '🙏 Temple Etiquette', text: 'Sarongs are required at all temples — most provide rentals at the entrance (IDR 10–20K). Cover shoulders and knees. Women who are menstruating are traditionally asked not to enter temples. Remove shoes before entering inner courtyards.' },
    { title: '💰 Budget Tips', text: 'Eat at local warungs for IDR 30–50K ($2–3) per meal — the food is incredible. Save splurges for sunset fine dining. ATMs are everywhere but often charge fees; bring a no-foreign-transaction-fee card. Tipping 10% at restaurants is appreciated but not required.' },
    { title: '🏥 Health & Safety', text: 'Drink only bottled or filtered water. Mosquito repellent is essential at dawn/dusk. Travel insurance is a must — Bali\'s hospitals are decent but evacuation to Singapore is the standard for serious issues. The monkeys at Monkey Forest WILL grab loose items.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-25',
      neighborhoods: 'Ubud Centre · Campuhan · Jalan Raya',
      title: 'Arrival & First Taste of Ubud',
      description: "Land in Bali, wind through the rice-paddy roads to Ubud, and get your first dose of the town's magic. An afternoon walk along the Campuhan Ridge at golden hour, followed by your first Balinese feast, sets the tone for the entire trip.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle In',
              description: 'Fly into Ngurah Rai International Airport (DPS) and transfer to Ubud — about 90 minutes by private car. The drive itself is an introduction to Bali: stone-carved temples, offering-laden streets, and the sudden lush green as you climb into the highlands.',
              details: [
                '🚗 Pre-book airport pickup through your hotel (IDR 350–450K)',
                '🏨 Check into your villa — Ubud has incredible value on private pool villas',
                '💡 Stay in Penestanan or Sayan for quieter rice-field views, or central Ubud for walkability'
              ]
            },
            {
              title: 'Campuhan Ridge Walk at Golden Hour',
              description: 'This narrow ridge between two river valleys is Ubud\'s most magical walk. Tall grass sways in the breeze, coconut palms line the path, and the light at 4–5pm is pure gold. About 2km one way — easy and beautiful.',
              details: [
                '🌾 Start from the bridge near Warwick Ibah hotel',
                '📸 The grass is greener and taller during dry season — stunning photos',
                '⏰ Go between 4–5:30pm to avoid heat and catch golden light'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Locavore NXT',
              description: 'Ubud\'s most celebrated restaurant reimagines Indonesian ingredients through a modern lens. Inventive tasting menus using hyper-local produce. An unforgettable first-night statement.',
              meta: '💰 $$$$ · 📍 Jl. Dewi Sita · Book well in advance'
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag from long-haul flights? The Campuhan walk is gentle enough for tired legs but scenic enough to reset your brain. Don\'t nap too long — push to local dinner time.' }
          ]
        }
      ],
      mapPins: [
        { lat: -8.5069, lng: 115.2625, label: 'Ubud Centre', num: 1, cat: 'attraction', desc: 'Heart of Ubud — palace, market, restaurants' },
        { lat: -8.5048, lng: 115.2469, label: 'Campuhan Ridge Walk', num: 2, cat: 'attraction', desc: 'Scenic ridge walk between two river valleys' },
        { lat: -8.5075, lng: 115.2590, label: 'Locavore NXT', num: 3, cat: 'food', desc: 'Award-winning modern Indonesian tasting menu' }
      ]
    },
    {
      num: 2,
      date: '2026-06-26',
      neighborhoods: 'Tegallalang · Tampaksiring · Gunung Kawi',
      title: 'Rice Terraces & Sacred Springs',
      description: "Your first full day dives straight into Bali's most iconic landscape — the cascading emerald steps of Tegallalang — then descends into the ancient river valley of Gunung Kawi temple before a purification ritual at the thousand-year-old Tirta Empul springs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tegallalang Rice Terraces',
              description: 'The most photographed rice terraces in Bali — and they earn it. Arrive early (before 9am) to beat the crowds and see the morning light paint the paddies. Walk the paths between the subak irrigation channels that UNESCO recognises as cultural heritage.',
              details: [
                '🌾 Arrive by 8:30am for soft light and thin crowds',
                '📸 The mid-level viewing platform gives the best panoramic shots',
                '💰 Entrance IDR 25K + small donations along the walking paths',
                '☕ D\'Tukad coffee shop has terraces right over the rice paddies'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tis Café Tegallalang',
              description: 'Perched on the edge of the rice terraces with an infinity pool overlooking the paddies. The nasi goreng here comes with a million-dollar view.',
              meta: '💰 $$ · 📍 Tegallalang · Get a terrace seat'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gunung Kawi Temple',
              description: 'Descend 300 steps through a lush river valley to reach this 11th-century royal tomb complex — 10 carved rock shrines (candi) cut directly into the cliff face. One of Bali\'s oldest and most atmospheric monuments. The walk down through rice paddies is half the experience.',
              details: [
                '🏛️ Built in the 11th century for King Anak Wungsu and his queens',
                '🥾 300 steps down (and back up!) — wear comfortable shoes',
                '🌿 The moss-covered shrines in the river gorge feel like Indiana Jones'
              ]
            },
            {
              title: 'Tirta Empul Holy Spring Temple',
              description: 'One of Bali\'s most sacred sites — a water temple where Balinese Hindus come for ritual purification. You can participate: enter the pools in a sarong and move through 13 fountain spouts, each with a different blessing. A genuinely moving spiritual experience.',
              details: [
                '🙏 Wear a sarong (provided) and respectfully follow the ritual sequence left to right',
                '💧 Skip fountains 11 and 12 — those are reserved for funeral purification rites',
                '📸 The courtyard with emerald pools and ancient stone carvings is extraordinary',
                '💰 Entrance IDR 50K per person'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Bring a waterproof bag for your phone and a change of dry clothes for after the Tirta Empul purification. The experience is deeply meaningful — approach it with genuine respect.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Swept Away at The Samaya',
              description: 'Romantic riverside dining surrounded by rice paddies and torches. Balinese and Indonesian fine dining with a tasting menu option. The setting — tables right beside the Ayung River — is pure magic after dark.',
              meta: '💰 $$$ · 📍 Sayan · Reservation recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.4312, lng: 115.2792, label: 'Tegallalang Rice Terraces', num: 1, cat: 'attraction', desc: 'Iconic cascading rice paddies — UNESCO subak system' },
        { lat: -8.4225, lng: 115.3117, label: 'Gunung Kawi Temple', num: 2, cat: 'attraction', desc: '11th-century royal tombs carved into cliff faces' },
        { lat: -8.4153, lng: 115.3155, label: 'Tirta Empul Temple', num: 3, cat: 'attraction', desc: 'Sacred spring temple for water purification rituals' },
        { lat: -8.4316, lng: 115.2800, label: 'Tis Café', num: 4, cat: 'food', desc: 'Rice terrace views with infinity pool' },
        { lat: -8.5020, lng: 115.2380, label: 'Swept Away at The Samaya', num: 5, cat: 'food', desc: 'Riverside fine dining in the Ayung valley' }
      ]
    },
    {
      num: 3,
      date: '2026-06-27',
      neighborhoods: 'Monkey Forest · Ubud Centre · Peliatan',
      title: 'Monkeys, Markets & Fire Dance',
      description: "A day for Ubud's greatest hits: the Sacred Monkey Forest at dawn, bargain-hunting at the famous art market, the royal palace grounds, and an evening Kecak fire dance that will give you chills. This is the Ubud that everyone falls in love with.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sacred Monkey Forest Sanctuary',
              description: 'Over 1,200 long-tailed macaques live in this ancient 12.5-hectare forest in the heart of Ubud. Moss-covered temples, banyan trees with massive roots, a dragon-guarded bridge — it\'s like walking through a Studio Ghibli film. Arrive early when the monkeys are calmer.',
              details: [
                '🐒 Open 9am–5pm · IDR 80K entrance',
                '⚠️ Secure everything — glasses, water bottles, phones. Monkeys are expert thieves',
                '🌳 Three ancient temples inside the forest, including Pura Dalem Agung (temple of the dead)',
                '📸 The moss-covered stone statues and banyan roots are incredibly photogenic'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Milk & Madu',
              description: 'Trendy brunch spot in central Ubud with excellent avocado toast, smoothie bowls, and strong Bali coffee. Great people-watching from the upstairs terrace.',
              meta: '💰 $$ · 📍 Jl. Dewi Sita'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ubud Art Market (Pasar Seni Ubud)',
              description: 'Across from the palace, this bustling market sells handmade crafts, batik textiles, woven baskets, silver jewellery, paintings, and woodcarvings. Come ready to bargain — start at about 40% of the asking price and negotiate with a smile.',
              details: [
                '🛍️ Best in the morning when locals also shop (before tour buses arrive)',
                '🎨 Look for hand-painted Balinese fans, silver rings, and rattan bags',
                '💰 Bargain hard but fair — most items are handmade by local artisans'
              ]
            },
            {
              title: 'Ubud Royal Palace (Puri Saren Agung)',
              description: 'The historical seat of Ubud\'s royal family, with ornate Balinese architecture and manicured gardens. The front courtyard is open to visitors during the day. The palace still hosts the royal family and is the venue for nightly dance performances.',
              details: [
                '🏛️ Free to walk the outer courtyards',
                '📸 The split gate (candi bentar) and ornate stone carvings are stunning',
                '🌺 The lotus pond across the street (Pura Taman Saraswati) is gorgeous'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kecak Fire Dance Performance',
              description: 'Bali\'s most dramatic traditional performance: 50+ men chanting "cak-cak-cak" in concentric circles while dancers enact the Ramayana epic, climaxing with a fire-walking finale. Performed at dusk in the palace courtyard or at Pura Dalem Taman Kaja. An absolute must.',
              details: [
                '🔥 Shows at 7:30pm most evenings · IDR 100K per person',
                '📍 Ubud Palace or Pura Dalem Taman Kaja — check schedules locally',
                '🎭 The chanting alone — no instruments, just human voices — is hypnotic',
                '📸 Arrive 20 minutes early for front-row seats'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Warung Biah Biah',
              description: 'Authentic Balinese warung tucked down a side street. Try the babi guling (suckling pig) or lawar (spiced minced meat with coconut). This is real Balinese food at local prices.',
              meta: '💰 $ · 📍 Jl. Suweta · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.5186, lng: 115.2588, label: 'Sacred Monkey Forest', num: 1, cat: 'attraction', desc: '1,200 macaques in an ancient temple forest' },
        { lat: -8.5069, lng: 115.2633, label: 'Ubud Art Market', num: 2, cat: 'shopping', desc: 'Handicrafts, batik, silver and woodcarvings' },
        { lat: -8.5065, lng: 115.2628, label: 'Ubud Royal Palace', num: 3, cat: 'attraction', desc: 'Historic royal residence and dance venue' },
        { lat: -8.5077, lng: 115.2621, label: 'Pura Taman Saraswati', num: 4, cat: 'attraction', desc: 'Beautiful lotus pond temple' },
        { lat: -8.5066, lng: 115.2617, label: 'Milk & Madu', num: 5, cat: 'food', desc: 'Popular brunch café on Jl. Dewi Sita' },
        { lat: -8.5045, lng: 115.2645, label: 'Warung Biah Biah', num: 6, cat: 'food', desc: 'Authentic Balinese warung — babi guling & lawar' }
      ]
    },
    {
      num: 4,
      date: '2026-06-28',
      neighborhoods: 'Ubud · Laplapan · Tegenungan',
      title: 'Cooking Class & Waterfall Chase',
      description: "Morning at a Balinese cooking school — start at the local market picking fresh ingredients, then learn to make nasi goreng, satay, and lawar in an open-air jungle kitchen. Afternoon, cool off at the thundering Tegenungan Waterfall.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Balinese Cooking Class with Market Tour',
              description: 'Join a hands-on cooking class that starts at the traditional morning market (pasar pagi), where your chef-guide teaches you to identify galangal, lemongrass, palm sugar, and fresh turmeric. Then head to the cooking school — usually an open-air kitchen surrounded by rice paddies — and prepare 5–7 dishes from scratch.',
              details: [
                '👨‍🍳 Paon Bali or Pemulan Farm Cooking School are top-rated',
                '🛒 Market tour starts around 8am — the earlier the better for the freshest produce',
                '🍛 You\'ll make: nasi goreng, chicken satay, lawar, sate lilit, black rice pudding, and more',
                '💰 ~IDR 350–450K per person including all food and transport'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tegenungan Waterfall',
              description: 'The most accessible big waterfall near Ubud — a thundering curtain of water plunging into a natural swimming pool surrounded by lush jungle. The walk down is steep but short (about 15 minutes). Swim in the pool at the base and feel the mist on your face.',
              details: [
                '💧 Bring swimwear and water shoes (rocks are slippery)',
                '💰 Entrance IDR 20K',
                '📸 Morning light is best for photos, but afternoons are less crowded',
                '🌿 There are multiple viewpoints on the walk down — don\'t rush'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'After the waterfall, you\'ll be wet and possibly muddy. Bring a dry bag for your electronics and a change of clothes. The parking area has simple warungs for cold drinks.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Room4Dessert',
              description: 'World-class dessert-focused tasting restaurant by pastry legend Will Goldfarb (featured on Chef\'s Table). A wildly creative 10-course dinner where dessert IS the meal. Unlike anything you\'ve ever eaten.',
              meta: '💰 $$$$ · 📍 Jl. Raya Sanggingan · Book well ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.5100, lng: 115.2600, label: 'Morning Market (Pasar Ubud)', num: 1, cat: 'attraction', desc: 'Traditional morning market for cooking class ingredients' },
        { lat: -8.4850, lng: 115.2650, label: 'Cooking School', num: 2, cat: 'attraction', desc: 'Hands-on Balinese cooking in an open-air jungle kitchen' },
        { lat: -8.5725, lng: 115.2886, label: 'Tegenungan Waterfall', num: 3, cat: 'attraction', desc: 'Thundering waterfall with a natural swimming pool' },
        { lat: -8.5028, lng: 115.2500, label: 'Room4Dessert', num: 4, cat: 'food', desc: 'Chef\'s Table-featured dessert tasting experience' }
      ]
    },
    {
      num: 5,
      date: '2026-06-29',
      neighborhoods: 'Mount Batur · Kintamani · Trunyan',
      title: 'Mount Batur Sunrise Trek',
      description: "The alarm rings at 2am — worth every lost minute of sleep. Climb an active volcano in the dark, reach the crater rim at dawn, and watch the sun rise over the entire island while steam vents hiss beneath your feet. Breakfast is eggs cooked in volcanic steam. One of the best sunrises on Earth.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Mount Batur Sunrise Trek',
              description: 'Depart Ubud at 2am, drive to the trailhead at Toya Bungkah village, and begin the 2-hour ascent of Mount Batur (1,717m) in the dark with headlamps. The trail is steep but non-technical. At the summit, watch the sky shift from deep blue to orange to gold as the sun rises over Mount Agung and Lake Batur. Your guide will cook breakfast on the volcanic steam vents.',
              details: [
                '🌋 Active volcano — last erupted in 2000, but the trek is perfectly safe',
                '⏰ Pickup from hotel at 2am, summit around 5:30am for sunrise',
                '🥚 Breakfast at the top: eggs and banana sandwiches cooked on volcanic steam',
                '🥾 Moderate difficulty — good shoes, warm layers, headlamp (provided by guide)',
                '💰 ~IDR 500–700K per person with guide, transport, breakfast',
                '🏔️ On a clear day, you can see all the way to Lombok\'s Mount Rinjani'
              ]
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Kintamani Caldera Views & Hot Springs',
              description: 'After descending, take in the panoramic views of Mount Batur\'s caldera and the crescent-shaped Lake Batur from the Kintamani ridgeline. Then soak your aching legs in the natural hot springs at Toya Devasya on the lake shore.',
              details: [
                '♨️ Toya Devasya Hot Springs: IDR 150K entry, open-air pools overlooking the lake',
                '🌋 The caldera view from Kintamani village is one of Bali\'s most dramatic panoramas',
                '☕ Roadside cafés along the rim have incredible views'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rest & Recovery at Your Villa',
              description: 'After a 2am wake-up and a volcano trek, you\'ve earned an afternoon off. Return to Ubud and spend the afternoon at your villa pool, book a Balinese massage, or simply nap in a hammock surrounded by rice paddies.',
              details: [
                '💆 Book an in-villa massage (IDR 150–300K for 60–90 mins)',
                '🏊 Most Ubud villas have private pools — perfect for post-trek recovery'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The trek is manageable for anyone with reasonable fitness, but it is steep and dusty. Wear proper shoes (not sandals), bring a jacket (it\'s cold at 1,700m before dawn), and carry plenty of water.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hujan Locale',
              description: 'Chef Will Meyrick\'s Indonesian archipelago restaurant — dishes from across the 17,000 islands, beautifully plated. The rendang and slow-cooked lamb are exceptional. A gorgeous colonial-era building with lush gardens.',
              meta: '💰 $$$ · 📍 Jl. Sri Wedari, Ubud'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.2421, lng: 115.3754, label: 'Mount Batur Summit', num: 1, cat: 'attraction', desc: 'Active volcano — 1,717m sunrise trek' },
        { lat: -8.2880, lng: 115.3700, label: 'Kintamani Viewpoint', num: 2, cat: 'attraction', desc: 'Panoramic caldera and Lake Batur views' },
        { lat: -8.2577, lng: 115.3975, label: 'Toya Devasya Hot Springs', num: 3, cat: 'attraction', desc: 'Lakeside hot springs for post-trek recovery' },
        { lat: -8.5052, lng: 115.2575, label: 'Hujan Locale', num: 4, cat: 'food', desc: 'Indonesian archipelago cuisine by Will Meyrick' }
      ]
    },
    {
      num: 6,
      date: '2026-06-30',
      neighborhoods: 'Ubud · Penestanan · Sayan',
      title: 'Yoga, Wellness & Art',
      description: "A restorative day for body and soul. Morning yoga at Bali's most famous studio, a long rejuvenating spa session, and an afternoon exploring Ubud's world-class art museums. End with sunset drinks over rice paddies.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Morning Yoga at The Yoga Barn',
              description: 'The Yoga Barn is Ubud\'s legendary wellness hub — a bamboo open-air studio complex surrounded by gardens. Drop in for a 90-minute morning flow, vinyasa, or hatha class. All levels welcome. The energy of practicing yoga in the heart of Bali is something special.',
              details: [
                '🧘 Drop-in classes from IDR 130K · Schedule on their website',
                '📍 Jl. Hanoman, Pengosekan — 10-min walk from central Ubud',
                '🥗 Garden Kafe on-site serves excellent plant-based meals',
                '🔔 Sound healing and meditation sessions also available'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Sayuri Healing Food',
              description: 'Raw vegan café known for vibrant rainbow bowls, kombucha, and raw chocolate cakes. Even non-vegans rave about it. One of Ubud\'s most Instagrammable spots.',
              meta: '💰 $$ · 📍 Jl. Sukma'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Spa Day — Traditional Balinese Treatment',
              description: 'Book a 2–3 hour spa package: Balinese massage, body scrub with local herbs and coconut, flower bath, and facial. Bali is one of the world\'s best spa destinations, and Ubud\'s hillside spas overlooking the river gorge elevate it to another level.',
              details: [
                '💆 Karsa Spa (in the rice fields) or Fivelements (luxury riverside)',
                '🌺 Traditional Balinese massage uses long strokes, acupressure, and aromatherapy',
                '💰 High-end: IDR 500K–1.5M ($30–100) for a 2-hour package — incredible value'
              ]
            },
            {
              title: 'ARMA Museum (Agung Rai Museum of Art)',
              description: 'A beautiful museum and cultural centre showcasing Balinese and Indonesian fine art from the 17th century to today. Paintings by Walter Spies, Rudolf Bonnet, and I Gusti Nyoman Lempad — the artists who put Ubud on the cultural map. Set in gorgeous tropical gardens.',
              details: [
                '🎨 IDR 80K entrance · Open 9am–5pm',
                '🏛️ Also hosts traditional dance rehearsals and gamelan performances',
                '🌴 The garden setting is as impressive as the art — wander slowly'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Bridges Bali',
              description: 'Elegant dining overlooking the Campuhan river gorge. The terrace at sunset, with the jungle canopy below, is breathtaking. Contemporary Asian and Western menu with excellent cocktails.',
              meta: '💰 $$$ · 📍 Jl. Raya Campuhan · Sunset terrace seating'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.5148, lng: 115.2620, label: 'The Yoga Barn', num: 1, cat: 'attraction', desc: 'Bali\'s most famous yoga and wellness centre' },
        { lat: -8.5100, lng: 115.2580, label: 'Sayuri Healing Food', num: 2, cat: 'food', desc: 'Raw vegan café with rainbow bowls' },
        { lat: -8.5200, lng: 115.2520, label: 'Karsa Spa', num: 3, cat: 'attraction', desc: 'Rice-field spa with traditional Balinese treatments' },
        { lat: -8.5130, lng: 115.2550, label: 'ARMA Museum', num: 4, cat: 'attraction', desc: 'Balinese and Indonesian fine art museum' },
        { lat: -8.5043, lng: 115.2488, label: 'Bridges Bali', num: 5, cat: 'food', desc: 'River gorge dining at sunset' }
      ]
    },
    {
      num: 7,
      date: '2026-07-01',
      neighborhoods: 'East Bali · Tirta Gangga · Lempuyang',
      title: 'East Bali — Water Palace & Gate of Heaven',
      description: "A full day trip to Bali's dramatic east coast. Start at the serene Tirta Gangga water palace with its fountains and koi ponds, then climb to the ancient Lempuyang Temple for the legendary 'Gate of Heaven' view framing Mount Agung. This is bucket-list Bali.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to East Bali & Tirta Gangga',
              description: 'Depart early (7am) for the 2-hour drive east through increasingly dramatic volcanic landscapes. Tirta Gangga is a former royal water palace — ornamental pools, fountains, and stepping stones across koi-filled ponds, all set against the backdrop of Mount Agung.',
              details: [
                '🏛️ Built in 1946 by the last king of Karangasem',
                '💧 You can swim in the upper spring-fed pool (IDR 10K extra)',
                '🐟 Walk the stepping stones across the koi pond — surprisingly fun',
                '💰 Entrance IDR 50K'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lempuyang Temple (Gate of Heaven)',
              description: 'The most Instagram-famous view in Bali — the split gate of Pura Penataran Agung Lempuyang perfectly framing Mount Agung in the distance. The temple complex has 7 temples on the mountainside, but most visitors focus on the iconic gateway. Come prepared for a potential queue.',
              details: [
                '⛩️ The split gate (candi bentar) with Agung behind it is the money shot',
                '⏰ Arrive by 11am–12pm to avoid the worst queues (morning is busiest)',
                '🙏 Full sarong and sash required — free rentals available',
                '📸 Temple attendants help position you for the perfect photo',
                '🏔️ On clear days, Mount Agung is perfectly centred in the gate'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Mahagiri Panoramic Resort Restaurant',
              description: 'Stunning buffet restaurant perched on a hillside with panoramic views of rice terraces and Mount Agung. The Indonesian buffet is solid, but you\'re really here for the view.',
              meta: '💰 $$ · 📍 Rendang, Karangasem · On the route between Tirta Gangga and Lempuyang'
            }
          ],
          tips: [
            { type: 'tip', text: 'The Lempuyang queue for photos can be 1–2 hours at peak times. Going midday (11am–1pm) or on a weekday helps. The actual temple complex beyond the gate is peaceful and uncrowded — don\'t skip it.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Naughty Nuri\'s Warung',
              description: 'The legendary Ubud institution — famous for its grilled pork ribs and dirty martinis. No-frills roadside warung with massive flavour. Anthony Bourdain approved. Arrive hungry.',
              meta: '💰 $$ · 📍 Jl. Raya Sanggingan · Cash preferred'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.4123, lng: 115.5877, label: 'Tirta Gangga Water Palace', num: 1, cat: 'attraction', desc: 'Former royal water palace with koi ponds and fountains' },
        { lat: -8.3909, lng: 115.6305, label: 'Lempuyang Temple', num: 2, cat: 'attraction', desc: 'Iconic Gate of Heaven framing Mount Agung' },
        { lat: -8.4432, lng: 115.4591, label: 'Mahagiri Restaurant', num: 3, cat: 'food', desc: 'Panoramic rice terrace and volcano views' },
        { lat: -8.5026, lng: 115.2496, label: 'Naughty Nuri\'s', num: 4, cat: 'food', desc: 'Legendary ribs and dirty martinis' }
      ]
    },
    {
      num: 8,
      date: '2026-07-02',
      neighborhoods: 'Ayung River · Goa Gajah · Yeh Pulu',
      title: 'River Rafting & Ancient Caves',
      description: "Adrenaline in the morning, ancient mystery in the afternoon. Start with white-water rafting through a jungle gorge on the Ayung River, then explore the enigmatic Elephant Cave temple and the hidden Yeh Pulu rock carvings that few tourists ever see.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'White-Water Rafting on the Ayung River',
              description: 'Bali\'s best rafting experience — 10km of Class II–III rapids through a deep jungle gorge with towering cliff walls, waterfalls cascading into the river, and stone carvings on the canyon walls. Thrilling but safe for beginners. A highlight of any Bali trip.',
              details: [
                '🚣 About 2 hours on the river · Class II–III rapids (fun, not scary)',
                '🌿 The gorge is 15–20 metres deep with jungle overhead — feels like Jurassic Park',
                '💦 You WILL get soaked — wear swimwear under light clothes',
                '💰 ~IDR 350–500K per person with Sobek or Mason Adventures',
                '📸 Waterproof camera recommended — stone carvings on the canyon walls are amazing'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Goa Gajah (Elephant Cave)',
              description: 'A mysterious 9th-century cave temple with a gaping demon-face entrance carved into the rock. Inside, the T-shaped cave contains lingam and yoni shrines. Outside, bathing fountains hold water nymphs. One of Bali\'s most atmospheric archaeological sites.',
              details: [
                '🏛️ Dating from the 9th century — predates most Ubud temples',
                '👹 The demon mouth entrance (Bhoma) is meant to ward off evil spirits',
                '💧 The bathing fountains were only rediscovered in 1954',
                '💰 Entrance IDR 50K · Sarong provided'
              ]
            },
            {
              title: 'Yeh Pulu Rock Reliefs',
              description: 'A hidden gem just 1km from Goa Gajah — a 25-metre long rock carving from the 14th century depicting daily life scenes. Almost no tourists come here. Walk through rice paddies to reach the carved cliff face. One of Bali\'s best-kept secrets.',
              details: [
                '🗿 14th-century carvings showing hunting, daily life, and spiritual scenes',
                '🌾 Beautiful walk through rice fields to reach the site',
                '💰 Small donation at the entrance (IDR 15K)',
                '🤫 Barely visited — you may have it entirely to yourselves'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mozaic Restaurant Gastronomique',
              description: 'Chef Chris Salans\' flagship — French haute cuisine meets Balinese ingredients. A 7-course tasting menu in a romantic tropical garden setting. One of Bali\'s finest restaurants and a fitting splurge for a big night out.',
              meta: '💰 $$$$ · 📍 Jl. Raya Sanggingan · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.4950, lng: 115.2400, label: 'Ayung River Rafting', num: 1, cat: 'attraction', desc: '10km of jungle gorge white-water rafting' },
        { lat: -8.5243, lng: 115.2872, label: 'Goa Gajah (Elephant Cave)', num: 2, cat: 'attraction', desc: '9th-century cave temple with demon-face entrance' },
        { lat: -8.5260, lng: 115.2930, label: 'Yeh Pulu Rock Reliefs', num: 3, cat: 'attraction', desc: 'Hidden 14th-century rock carvings in rice fields' },
        { lat: -8.5026, lng: 115.2498, label: 'Mozaic Restaurant', num: 4, cat: 'food', desc: 'French-Balinese haute cuisine — 7-course tasting' }
      ]
    },
    {
      num: 9,
      date: '2026-07-03',
      neighborhoods: 'Bangli · Tembuku · Kemenuh',
      title: 'Hidden Waterfall Safari',
      description: "Bali's waterfalls are best experienced in sequence — each one completely different. Today is a three-waterfall day: the cathedral-like Tukad Cepung (sunbeams through a cave), the jungle paradise Tibumana, and the dramatic curtain of Kanto Lampo. Bring swimsuits and a spirit of adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tukad Cepung Waterfall',
              description: 'The most otherworldly waterfall in Bali — you walk through a narrow canyon and into a cave where water pours from cracks in the ceiling while shafts of sunlight pierce through like spotlights. It feels like entering a cathedral made by nature. Best between 9–11am when the sun angle creates the light beams.',
              details: [
                '✨ The sunbeam effect between 9–11am is breathtaking',
                '🥾 15-minute walk down steep steps and through a shallow river',
                '💧 You\'ll wade through knee-deep water to reach the falls — wear sandals you can get wet',
                '💰 Entrance IDR 20K'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Tibumana Waterfall',
              description: 'A jungle gem — a tall, thin waterfall pouring into a crystal-clear plunge pool surrounded by tropical vegetation. Less touristy than Tegenungan, more intimate, and the swimming pool at the base is perfect for a refreshing dip.',
              details: [
                '🌿 Short 10-minute walk through jungle to reach the falls',
                '🏊 The plunge pool is deep enough for swimming and cliff-adjacent lounging',
                '💰 Entrance IDR 20K',
                '📸 The bamboo bridge near the falls is great for photos'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Warung near Tibumana',
              description: 'Simple local warung near the waterfall parking area. Fresh nasi campur, fried tempeh, and cold Bintang beer. The best kind of Bali lunch.',
              meta: '💰 $ · 📍 Tibumana parking area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kanto Lampo Waterfall',
              description: 'A dramatic stepped waterfall where water cascades over layered rock formations like a giant staircase. The most photogenic of the three — the rock formations create a unique layered curtain effect. Popular for photos but the pool at the base is refreshing.',
              details: [
                '💧 Water flows over stepped rock slabs — you can sit on the rocks in the cascade',
                '📸 Stand on the lower rocks with the waterfall fanning behind you — incredible shots',
                '⏰ Best in afternoon light · IDR 15K entrance',
                '🚗 Only 15 minutes from central Ubud'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Night Celebration',
              description: 'Your last evening in Ubud — make it special. Watch the sunset from the rice terraces, freshen up, and head to a memorable farewell dinner.',
              details: [
                '🌅 Sari Organik walk through the rice fields catches beautiful late-afternoon light',
                '📸 Perfect golden-hour photo walk for group shots'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Apéritif Restaurant & Bar',
              description: 'A grand 1920s colonial supper club in the hills above Ubud. Theatrical cocktails, a stunning 6-course tasting menu, and an atmosphere that feels like stepping into a Baz Luhrmann film. The ultimate Ubud farewell.',
              meta: '💰 $$$$ · 📍 Jl. Lanyahan, Banjar Nagi · Reservations required'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.4800, lng: 115.3800, label: 'Tukad Cepung Waterfall', num: 1, cat: 'attraction', desc: 'Cave waterfall with cathedral sunbeams' },
        { lat: -8.5150, lng: 115.3200, label: 'Tibumana Waterfall', num: 2, cat: 'attraction', desc: 'Jungle waterfall with crystal swimming pool' },
        { lat: -8.5197, lng: 115.2960, label: 'Kanto Lampo Waterfall', num: 3, cat: 'attraction', desc: 'Stepped rock waterfall — dramatic photo spot' },
        { lat: -8.4988, lng: 115.2444, label: 'Apéritif Restaurant', num: 4, cat: 'food', desc: '1920s supper club with theatrical tasting menu' }
      ]
    },
    {
      num: 10,
      date: '2026-07-04',
      neighborhoods: 'Ubud Centre · Petulu · Airport',
      title: 'Last Morning & Farewell to Bali',
      description: "A gentle final morning — catch the famous Petulu heron colony at dawn, wander through Ubud one last time, pick up souvenirs, and have a lingering brunch before the drive to the airport. Bali will stay with you long after you leave.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Petulu Heron Village (Optional Early Bird)',
              description: 'Just 5 minutes north of Ubud, the village of Petulu is home to thousands of white herons and egrets that return to roost at dawn and dusk. The sight of thousands of birds against the misty morning rice paddies is magical — and almost no tourists know about it.',
              details: [
                '🐦 Best at dawn (6–7am) or dusk (5:30–6:30pm)',
                '📸 The birds fill the trees like white blossoms — surreal',
                '🌾 Combine with a final rice-field walk'
              ]
            },
            {
              title: 'Final Ubud Stroll & Souvenir Shopping',
              description: 'One last wander through the streets you\'ve come to love. Pick up final gifts at the art market, browse the silver workshops of Celuk village on the way to the airport, or just sit at your favourite café and watch Ubud wake up one more time.',
              details: [
                '🛍️ Ganesha Bookshop (Jl. Raya Ubud) — great for Indonesian literature and maps',
                '💍 Celuk silver village (on the airport road) — handmade Balinese silver jewellery',
                '🎨 Threads of Life gallery — traditional Indonesian textiles (Jl. Kajeng)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Farewell Brunch',
              name: 'Café Pomegranate',
              description: 'A serene garden café with creative brunch dishes — smoked salmon eggs benedict, chia pudding, and excellent pour-over coffee. Peaceful and pretty — the perfect last Ubud meal.',
              meta: '💰 $$ · 📍 Jl. Sukma'
            }
          ],
          tips: [
            { type: 'tip', text: 'The drive to Ngurah Rai airport takes 90 minutes in good traffic, 2+ hours if it\'s busy. Allow at least 3 hours before your flight. Your hotel can arrange transport, or use Grab for a lower price.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Transfer to Airport',
              description: 'Say goodbye to the rice paddies, the temple incense, and the gamelan music drifting through the evening air. The drive south from Ubud to Ngurah Rai takes you back through the bustling Bali lowlands — a reminder of how special Ubud\'s highland calm truly is.',
              details: [
                '🚗 Pre-arrange airport transfer through your hotel or Grab',
                '⏰ Budget 2–2.5 hours to be safe',
                '✈️ Ngurah Rai Airport (DPS) — international departures in Terminal I'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: -8.4936, lng: 115.2647, label: 'Petulu Heron Village', num: 1, cat: 'attraction', desc: 'Thousands of white herons roosting at dawn' },
        { lat: -8.5069, lng: 115.2625, label: 'Ubud Centre', num: 2, cat: 'attraction', desc: 'Final morning stroll through town' },
        { lat: -8.5080, lng: 115.2610, label: 'Café Pomegranate', num: 3, cat: 'food', desc: 'Garden café for a farewell brunch' },
        { lat: -8.7467, lng: 115.1667, label: 'Ngurah Rai Airport (DPS)', num: 4, cat: 'transport', desc: 'International airport — 90 min from Ubud' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$20–50/night', midrange: '$80–200/night', luxury: '$300–800/night' },
    { category: 'Meals (per person)', budget: '$5–10/day', midrange: '$20–50/day', luxury: '$80–200/day' },
    { category: 'Transport', budget: '$10–20/day', midrange: '$30–45/day (driver)', luxury: '$60–100/day (private)' },
    { category: 'Activities', budget: '$5–15/day', midrange: '$30–60/day', luxury: '$80–150/day' },
    { category: 'Spa/Wellness', budget: '$10–20/session', midrange: '$30–60/session', luxury: '$100–300/session' },
    { category: '10-Day Total (per person)', budget: '$400–800', midrange: '$1,200–3,000', luxury: '$4,000–10,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Ngurah Rai International Airport (DPS) in South Bali', 'Transfer to Ubud takes 90 minutes by car (IDR 350–450K one-way)', 'Many hotels offer free or discounted airport pickups — ask when booking', 'Grab and GoJek are cheaper than hotel transfers (~IDR 200–300K)'] },
    { title: '🏨 Where to Stay', items: ['Central Ubud (Jl. Raya / Jl. Hanoman) — walkable to everything, lively', 'Penestanan — quieter artist village, rice-field views, 10 min from centre', 'Sayan — river gorge luxury (where Mandapa and Four Seasons are)', 'Tegallalang area — closer to rice terraces, very rural and peaceful', 'Budget: $20–50/night gets incredible private pool villas by Bali standards'] },
    { title: '🌡️ Weather', items: ['Late June is peak dry season — expect sunny skies and 27–30°C daily', 'Humidity is moderate (60–70%), much more comfortable than the wet season', 'Mountain areas (Kintamani, Batur) are noticeably cooler', 'UV is strong year-round — wear SPF 50+ even on cloudy days'] },
    { title: '💳 Money', items: ['Indonesian Rupiah (IDR) — roughly 15,500 IDR = $1 USD', 'ATMs everywhere in Ubud — BCA and Mandiri are most reliable', 'Many restaurants accept cards, but carry cash for temples, markets, warungs', 'Tipping is appreciated: round up bills, IDR 10–20K for guides/drivers'] },
    { title: '📱 Connectivity', items: ['Buy a local SIM at the airport — Telkomsel has the best coverage', 'eSIM providers (Airalo, Holafly) work well if your phone supports them', 'WiFi is reliable in most hotels and cafés', 'Rural areas and mountain treks may have spotty signal'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
