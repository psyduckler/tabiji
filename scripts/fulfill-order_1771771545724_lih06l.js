const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771771545724_lih06l',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Kathmandu Valley, Nepal',
  startDate: '2026-02-25',
  endDate: '2026-02-28',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Kathmandu Valley, Nepal',
  countryEmoji: '🇳🇵',
  title: 'Gods, Stupas & Ancient Cities — Kathmandu Valley',
  subtitle: '3 days across Kathmandu, Patan & Bhaktapur: sacred temples, UNESCO old towns, and the food capital of the Himalayas',
  description: "The Kathmandu Valley is one of the most extraordinary places on Earth — a cradle of civilization tucked into the Himalayas at 1,400 metres, where three medieval cities (Kathmandu, Patan, and Bhaktapur) have coexisted for over a thousand years in creative, spiritual, and architectural rivalry. Seven UNESCO World Heritage Sites are packed into an area you can cross by taxi in 30 minutes. Buddhist stupas rise from rice paddies. Hindu temples release incense smoke that curls past gilded rooftops. Sadhus with ash-painted faces meditate on ghats where sacred fires have burned for centuries. And in the alleyways of Bhaktapur's old town, potters still shape clay on wheels unchanged since the 12th century. In late February, the valley is crisp and clear — the best mountain views of the year, thin-season crowds, and Holi just around the corner painting everything in colour.",
  duration: '3 nights',
  dates: 'Feb 25 – Feb 28, 2026',
  budget: '$',
  pace: 'Active',
  bestFor: 'Solo Travelers',

  highlights: [
    'Boudhanath Stupa — one of the largest Buddhist stupas in the world, ringed by monasteries and prayer flags',
    'Pashupatinath Temple — Nepal\'s holiest Hindu shrine, with sacred ghats and cremation ceremonies on the Bagmati River',
    'Swayambhunath ("Monkey Temple") — ancient hilltop stupa with panoramic valley views and mischievous rhesus macaques',
    'Bhaktapur Durbar Square — the best-preserved medieval city in South Asia, with the towering 5-storey Nyatapola Temple',
    'Patan Durbar Square & Museum — the finest example of Newar architecture, with a museum that will make you rethink everything you know about Himalayan art',
    'Newari cuisine — chatamari (rice crepes), bara (lentil patties), choila (spiced buff), and yomari dumplings in centuries-old courtyards'
  ],

  essentials: [
    { title: '🌤️ February Weather', text: 'Late February is one of the best times to visit the valley. Expect cool, clear days (10–18°C) and chilly nights (2–5°C). The air is clean after winter, and mountain views are exceptional — on a clear morning you can see the entire Himalayan arc from Kathmandu\'s hilltops. Bring a warm jacket for mornings and evenings, light layers for the afternoon sun.' },
    { title: '✈️ Getting There', text: 'Fly into Tribhuvan International Airport (KTM) — Nepal\'s only international airport, 5km from Thamel. Taxi to Thamel costs NPR 700–900 (~$5–7 USD) with a prepaid voucher from the airport taxi desk (avoid the touts). Many Asian hubs connect directly: Delhi (1.5hr), Doha (5hr), Kuala Lumpur (5hr). Book accommodation in Thamel for the best central location.' },
    { title: '💰 Budget Tips', text: 'Nepal is extraordinarily good value. A clean guesthouse in Thamel runs $10–25/night, dal bhat (the national dish — unlimited refills) costs $2–4 at local spots. A three-course dinner at the best Newari restaurant in Patan is $8–12. The Nepali Rupee (NPR) trades at roughly 133:1 USD. Major sites charge entrance fees ($3–15 USD range) — budget about $30/day total including meals and transport.' },
    { title: '🗺️ Getting Around', text: 'The valley is compact but chaotic. Taxis are cheap and metered (or negotiate upfront — NPR 200–400 for most trips). Ride-hailing via Pathao or InDrive is even cheaper. For Bhaktapur and Nagarkot, hire a taxi for the day (NPR 2,500–4,000). Walking is the only way to explore the old towns properly — the alleys of Bhaktapur are too narrow for cars.' },
    { title: '🙏 Temple Etiquette', text: 'Remove shoes before entering temples and stupas (carry a small bag for them). Non-Hindus cannot enter the inner sanctum of Pashupatinath Temple — observe respectfully from across the river. Dress modestly: cover shoulders and knees. Photography is usually fine outside, restricted inside. Clockwise circumambulation of stupas is the tradition. Accept tika (red powder on the forehead) graciously if offered — it\'s a blessing.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-25',
      neighborhoods: 'Thamel · Swayambhunath · Kathmandu Durbar Square · Asan Bazaar',
      title: 'Arrival in the City of Gods',
      description: "Your first day in Kathmandu is an immersion in living antiquity. Start above the city at Swayambhunath — the Monkey Temple — where the all-seeing eyes of the Buddha gaze across the valley from a hilltop stupa that predates written history. Then descend into the medieval heart of old Kathmandu: Durbar Square, where 55 courtyards and dozens of temples crowd around the ancient royal palace. End the evening lost in the colour and chaos of Asan Bazaar, where Kathmandu has traded spices, thangkas, and marigolds for 2,000 years.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Swayambhunath Stupa (Monkey Temple)',
              description: "Climb the 365 stone steps to Swayambhunath — one of the most recognisable images in all of Asia. The great white dome topped by a golden spire, painted with the all-seeing eyes of the Buddha, sits atop a hill with panoramic views of the entire Kathmandu Valley. Rhesus macaques patrol the complex like gatekeepers. Prayer flags flutter in every direction. Buddhist monks spin prayer wheels in the early morning mist. This is a living temple — arrive before 8am to see devotees doing kora (circumambulation) as the light comes in golden over the valley.",
              details: [
                '🕌 Entry fee: NPR 200 (~$1.50) for foreigners · Opens at dawn',
                '⏰ Best before 8:30am — fewer crowds, morning light, monkeys most active',
                '📸 Sunrise views of the valley are extraordinary — bring your camera',
                '🐒 Don\'t carry food openly — the monkeys are bold and will grab it',
                '📍 2.5km west of Thamel · 10min taxi or 30min walk'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Himalayan Java Coffee (Thamel)',
              description: "Nepal's best coffee chain — proper espresso, fresh croissants, and a warm escape from the morning chill. The Thamel branch is a reliable first-morning ritual before heading out to the temple circuit.",
              meta: '💰 $ · 📍 Thamel, multiple locations'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kathmandu Durbar Square',
              description: "The ancient royal palace complex at the heart of old Kathmandu — a UNESCO World Heritage Site. Hanuman Dhoka (the old royal palace) anchors a square packed with temples, courtyards, and stone sculptures. The Taleju Temple (off-limits to non-Hindus) towers above everything. Look for the living goddess — the Kumari, a young girl worshipped as a divine incarnation of Durga — who occasionally appears in a carved window of the Kumari Chowk. The 2015 earthquake damaged parts of the square; reconstruction is ongoing, but the atmosphere remains electric.",
              details: [
                '🎟️ Entry: NPR 1,000 (~$7.50) for foreigners — valid all day, keep your ticket',
                '🛕 Highlight: Kumari Chowk — wait quietly for the Kumari to appear at the window',
                '🏛️ Hanuman Dhoka Museum inside the palace is worth 45 minutes',
                '📸 The square is best light in late afternoon — golden on the pagoda rooftops',
                '⚠️ Aggressive touts and "student guides" at the entrance — a polite firm "no" works'
              ]
            },
            {
              title: 'Asan Bazaar & Indra Chowk',
              description: "Walk north from Durbar Square through the ancient trading network of old Kathmandu. Asan Chowk is a six-way intersection that has been a spice market since the days of the trans-Himalayan caravan trade. Marigold garlands, turmeric piles, dried chillies, and incense fill the air. Indra Chowk hosts the Akash Bhairav temple behind a screen of peacock feathers — the blue-faced deity of the sky. These alleys are one of Asia's great street-photography corridors.",
              details: [
                '🌼 Marigolds everywhere — used for temple offerings, perfect for photos',
                '🌶️ Buy Nepali spice mixes, Himalayan salt, and timur pepper as souvenirs',
                '🕌 Look up — the upper floors of Asan\'s old trading houses are extraordinary',
                '🆓 Free to wander · Most atmospheric late afternoon when market is busiest'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Hire a registered local guide for Durbar Square (NPR 500–800 for 2 hours) — the stories behind the deities, the history of the Rana regime, and the earthquake damage context make the square three times more meaningful.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Garden of Dreams — Sunset Drink',
              description: "Just behind Thamel\'s chaos, the Garden of Dreams is an extraordinary Edwardian-era neo-classical garden built in the 1920s by Kaiser Shumsher Rana. Six pavilions surround manicured lawns, lily ponds, and bougainvillea-draped pergolas. It\'s the most tranquil spot in Kathmandu — a genuine escape from the city noise. The bar in the pavilion serves excellent cocktails at sunset.",
              details: [
                '💰 Entry: NPR 400 (~$3) · Open until 9pm',
                '🍸 The Kaiser Cafe inside does cocktails, wine, and light meals — treat yourself',
                '📍 Kaiser Mahal, Tridevi Marg — a 2-min walk from Thamel'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Thamel House Restaurant',
              description: "The gold standard for Newari cuisine in a tourist-friendly setting. A beautifully restored Rana-era building in Thamel houses a set-menu Newari feast: chatamari (rice crepe \"pizza\" topped with egg and spiced buff), bara (crispy lentil patties), choila (flame-charred buffalo meat with mustard oil and spices), and aalu tama (potato and bamboo shoot curry). Live Nepali folk music most evenings.",
              meta: '💰 $$ · 📍 Thamel House, Thamel · Book ahead if possible'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.7149, lng: 85.2903, label: 'Swayambhunath Stupa', num: 1, cat: 'attraction', desc: 'The Monkey Temple — hilltop stupa with all-seeing eyes and valley panoramas' },
        { lat: 27.7044, lng: 85.3067, label: 'Kathmandu Durbar Square', num: 2, cat: 'attraction', desc: 'Ancient royal palace complex — UNESCO World Heritage Site' },
        { lat: 27.7071, lng: 85.3099, label: 'Asan Bazaar', num: 3, cat: 'attraction', desc: 'Ancient spice market crossroads — marigolds, turmeric, incense chaos' },
        { lat: 27.7152, lng: 85.3127, label: 'Garden of Dreams', num: 4, cat: 'attraction', desc: 'Edwardian garden oasis — cocktails at sunset, total tranquility' },
        { lat: 27.7159, lng: 85.3123, label: 'Himalayan Java Coffee', num: 5, cat: 'food', desc: 'Best coffee in Thamel — proper espresso and croissants' },
        { lat: 27.7147, lng: 85.3129, label: 'Thamel House Restaurant', num: 6, cat: 'food', desc: 'Gold-standard Newari set menu — chatamari, bara, choila, live music' }
      ]
    },
    {
      num: 2,
      date: '2026-02-26',
      neighborhoods: 'Boudhanath · Pashupatinath · Patan (Lalitpur)',
      title: 'Spiritual Circuit — Stupas, Sadhus & Patan\'s Renaissance',
      description: "The valley's most powerful day. Morning at Boudhanath — the giant stupa that is the beating heart of Tibetan Buddhism outside Tibet itself. Then to Pashupatinath, Nepal's holiest Hindu temple complex, where sacred fires have burned on the Bagmati River ghats for centuries. In the afternoon, cross to Patan — the city of artists — and its magnificent Durbar Square and world-class museum. By evening you'll have moved through two great world religions and three centuries of architecture, all within six kilometres.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Boudhanath Stupa — Circumambulation at Dawn',
              description: "Boudhanath is one of the largest Buddhist stupas in the world — a 36-metre dome of pure whitewash rising from a mandala-shaped base, ringed by 147 recessed niches containing prayer wheels. The all-seeing eyes of the Buddha look out in four directions. At dawn, hundreds of Tibetan Buddhist pilgrims perform kora (circumambulation), spinning prayer wheels and chanting mantras as butter lamps flicker in the monastery windows. Walk the circuit clockwise, then climb to one of the rooftop cafes for a coffee with a stupa view that will rearrange your priorities.",
              details: [
                '🎟️ Entry: NPR 400 (~$3) · Opens at dawn',
                '⏰ Arrive by 7am — monks do morning puja, maximum atmosphere',
                '🙏 Walk clockwise — always. Spin every prayer wheel as you pass',
                '☕ Stupa View Rooftop Cafe (northwest corner) — best coffee with the view',
                '🛍️ The lanes around the stupa have excellent Tibetan thangka paintings, singing bowls, and meditation supplies — best quality in Nepal here'
              ]
            },
            {
              title: 'Pashupatinath Temple & Ghats',
              description: "Nepal's most sacred Hindu temple — a UNESCO World Heritage Site on the banks of the Bagmati River. The main temple, with its golden roof and silver doors, is off-limits to non-Hindus, but the ghats (stone steps to the river) are fully accessible and far more compelling. Watch cremation ceremonies conducted openly on the riverside platforms — a profound and humbling window into Hindu philosophy about life, death, and rebirth. Sadhus (wandering holy men) with matted hair, ash-painted bodies, and orange robes gather near the temple for alms and contemplation.",
              details: [
                '🎟️ Entry: NPR 1,000 (~$7.50) for foreigners · The ghats themselves are free to approach from the eastern bank',
                '⛔ Inner temple: Hindus only. Observe respectfully from the opposite bank — actually a better vantage point',
                '🔥 Cremation ceremonies: respectful observation from a distance is accepted. No close photography of the pyres — deeply inappropriate',
                '🕉️ Sadhus will offer to pose for photos — a NPR 100–200 tip is expected and fair',
                '⏰ Most active in the early morning and around sunset'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Café de Patan (Patan Durbar Square)',
              description: "Inside the Patan Museum complex — Nepali dal bhat, buff momos, and filter coffee in a 17th-century Rana courtyard. Probably the most beautiful lunch setting in the valley.",
              meta: '💰 $$ · 📍 Patan Durbar Square, inside museum complex'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Patan Durbar Square & Patan Museum',
              description: "Patan (officially Lalitpur — 'City of Beauty') has long been the valley's artistic heart, home to the finest metalworkers, woodcarvers, and stone sculptors in Nepal. Patan Durbar Square is a UNESCO World Heritage Site that rivals anything in South or Southeast Asia — three main temples (Krishna Mandir, Bhimsen Temple, Vishwanath), the old royal bath (Manga Hiti), and the extraordinary Patan Museum, which houses the finest collection of Himalayan bronze sculpture in the world, displayed in the beautifully restored 17th-century royal palace itself.",
              details: [
                '🎟️ Patan Durbar Square: NPR 1,000 (~$7.50) — includes museum entry',
                '🏛️ Patan Museum: allow 90 minutes minimum — the bronze galleries alone are worth the trip to Nepal',
                '🛕 Krishna Mandir (1637 AD) — a rare example of the shikhara (North Indian) style in Nepal, each floor carved with scenes from the Mahabharata and Ramayana',
                '🔔 Manga Hiti — a 500-year-old stone water spout that still flows continuously, used for ritual bathing',
                '📸 Afternoon light is perfect on the square from 2–4pm'
              ]
            },
            {
              title: 'Kumbheshwar Temple & Golden Temple (Hiranyavarna Mahavihara)',
              description: "Walk five minutes from Durbar Square to these two extraordinary sites. Kumbheshwar is one of only two 5-tiered pagoda temples in the valley (the other is Nyatapola in Bhaktapur) — a soaring Shiva temple with a sacred pond believed connected to Gosaikunda lake high in the Himalayas. The Golden Temple is a Newari Buddhist monastery with a golden facade encrusted with peacock feathers, miniature shrines, and hammered metal dragons — one of the most ornate religious buildings in all of Nepal.",
              details: [
                '🕌 Golden Temple (Hiranyavarna Mahavihara): small donation requested',
                '⛔ No leather allowed inside the Golden Temple compound',
                '📸 The Golden Temple courtyard is one of the valley\'s great photography subjects — afternoon light on the gold facade is extraordinary'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Patan\'s old town streets south of Durbar Square are worth exploring — you\'ll find traditional metalworkers\' ateliers, woodcarving workshops, and thangka painting studios. These aren\'t tourist traps — they\'re working artisans whose families have practiced the same crafts for generations.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Junction Restaurant (Patan)',
              description: "One of the valley's best contemporary Nepali restaurants, just south of Patan Durbar Square. Their set Newari thali includes 12–15 small dishes showcasing the full spectrum of Newari cuisine — tama ko tarkari (bamboo shoot curry), kachila (minced raw buff with mustard oil), yomari (sweet rice dumplings), and chhyang (Newari rice beer). Exceptional value and atmosphere in a traditional Newar house.",
              meta: '💰 $$ · 📍 Near Patan Durbar Square, Lalitpur'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.7215, lng: 85.3620, label: 'Boudhanath Stupa', num: 1, cat: 'attraction', desc: 'Giant Buddhist stupa — dawn circumambulation with Tibetan pilgrims' },
        { lat: 27.7104, lng: 85.3486, label: 'Pashupatinath Temple', num: 2, cat: 'attraction', desc: 'Nepal\'s holiest Hindu shrine — sacred ghats, sadhus, cremation ceremonies' },
        { lat: 27.6727, lng: 85.3246, label: 'Patan Durbar Square', num: 3, cat: 'attraction', desc: 'UNESCO old town square — finest Newari architecture and Patan Museum' },
        { lat: 27.6760, lng: 85.3215, label: 'Kumbheshwar Temple', num: 4, cat: 'attraction', desc: 'One of only two 5-tiered pagoda temples in the valley' },
        { lat: 27.6748, lng: 85.3225, label: 'Golden Temple (Hiranyavarna Mahavihara)', num: 5, cat: 'attraction', desc: 'Golden Buddhist monastery with peacock-feather facade — no leather allowed' },
        { lat: 27.6725, lng: 85.3245, label: 'Café de Patan', num: 6, cat: 'food', desc: 'Dal bhat and buff momos in a 17th-century Rana palace courtyard' },
        { lat: 27.6720, lng: 85.3238, label: 'Junction Restaurant', num: 7, cat: 'food', desc: 'Best Newari thali in the valley — 12+ dishes, exceptional value' }
      ]
    },
    {
      num: 3,
      date: '2026-02-27',
      neighborhoods: 'Bhaktapur · Changu Narayan · Nagarkot',
      title: 'Bhaktapur: Nepal\'s Living Medieval City',
      description: "Bhaktapur is the valley's crown jewel — a UNESCO World Heritage city where the medieval past is not preserved behind velvet ropes but genuinely lived. The old town's 900-year-old brick streets have no cars; potters still turn wheels in Pottery Square; farmers thresh grain in the courtyards of 15th-century temples. The 5-storey Nyatapola Temple (the tallest temple in Nepal) rises like a rocket from Taumadhi Square. After the old town, continue to Changu Narayan — the valley's oldest temple on a hilltop — then drive up to Nagarkot for an extraordinary sunset over the Himalayan arc: Langtang, Ganesh Himal, Manaslu, Annapurna, and on a clear February day, Everest on the far horizon.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bhaktapur Durbar Square & Taumadhi Square',
              description: "The most complete and best-preserved medieval city square in South Asia. Bhaktapur Durbar Square holds the 55-Window Palace (1427 AD), the Golden Gate (gilded copper and brass, considered Nepal's finest piece of art), and the Vatsala Temple with its gilded bell. A five-minute walk brings you to Taumadhi Square and the Nyatapola Temple — 30 metres tall, five stories, built in 1702 in just seven months. Each successive platform is flanked by stone guardians of decreasing size as you ascend — wrestlers, elephants, lions, griffins, and goddesses.",
              details: [
                '🎟️ Entry: NPR 1,800 (~$13.50) — covers the entire old city for the day. Keep your ticket.',
                '🏛️ Golden Gate (Sun Dhoka): arguably the most beautiful single object in Nepal — gilded copper-gilt, every surface carved with deities',
                '🕌 Nyatapola Temple: the tallest pagoda in Nepal — perfectly proportioned, never been damaged by earthquake. Climb if open.',
                '📸 Morning light hits Taumadhi from the east — Nyatapola at 7–9am is sublime',
                '🚌 Bhaktapur: 13km east of Kathmandu · NPR 40 local bus from Old Bus Park or NPR 800–1,000 taxi'
              ]
            },
            {
              title: 'Pottery Square & Dattatreya Square',
              description: "Walk east from Taumadhi to Pottery Square (Chakhu Dhoka) — where Bhaktapur's potters work in open courtyards, shaping clay on traditional wheels before setting pots out to dry in rows across the square. It's been a pottery market for at least 700 years and you can buy directly from the makers. Continue to Dattatreya Square, the oldest part of Bhaktapur, anchored by a temple older than the Durbar Square itself and the famous Peacock Window — a carved wooden latticework window of such intricate beauty that it's on the old NPR 10 note.",
              details: [
                '🏺 Pottery Square: free to enter and watch. Pots sell for NPR 100–500 — wonderful and packable souvenirs.',
                '🪟 Peacock Window (Tachupal Tole): now in a small museum — NPR 50 entry. One of the finest pieces of woodcarving in Asia.',
                '📍 15-minute walk from Taumadhi Square through the old town\'s brick alleys'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Café Nyatapola (Taumadhi Square)',
              description: "A Bhaktapur institution — a traditional stepped-terrace tea house right on Taumadhi Square, with the Nyatapola Temple filling your entire field of vision. Order the local specialty: juju dhau ('king curd') — Bhaktapur's famous thick, slightly sweet clay-pot yogurt, eaten here for breakfast with beaten rice (chiura). There is no better start to a morning in the valley.",
              meta: '💰 $ · 📍 Taumadhi Square, Bhaktapur'
            },
            {
              type: '🍽️ Lunch',
              name: 'Sunny Restaurant (Bhaktapur)',
              description: "The reliable choice on Durbar Square — roof terrace with temple views, serving fresh momos (steamed and fried), thukpa (noodle soup), and a decent dal bhat. Sit outside if the sun is warm.",
              meta: '💰 $ · 📍 Bhaktapur Durbar Square area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Changu Narayan Temple',
              description: "Nepal's oldest temple (4th century AD, rebuilt multiple times) sits on a forested hilltop ridge 6km north of Bhaktapur — a 20-minute taxi from the old town. The Changu Narayan complex is one of the finest examples of Licchavi-era architecture in Nepal, with extraordinary stone inscriptions from the 5th century, gilded copper roofs, and exquisitely detailed carvings of Vishnu in his ten avatar forms. It's less visited than the other heritage sites — you'll often have it nearly to yourself.",
              details: [
                '🎟️ Entry: NPR 300 (~$2.25)',
                '📜 The stone inscription (464 AD) is one of the oldest texts in Nepal — look for it near the main temple',
                '🦅 Changu Narayan is dedicated to Vishnu — look for Garuda statues throughout the complex',
                '📍 Hilltop above Changu village · 20-min taxi from Bhaktapur (NPR 600–800 round trip with wait)',
                '🌄 Views from the ridge looking north toward the Himalayan foothills are excellent on clear afternoons'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nagarkot — Himalayan Sunset',
              description: "Drive 10km further into the hills from Changu Narayan to Nagarkot (2,175m) — the closest viewpoint from Kathmandu for panoramic Himalayan views. In late February, the air is at its clearest, and on a good day the panorama stretches from Dhaulagiri in the west to Kanchenjunga in the east — including Everest visible as a distant pyramid on the horizon to the northeast. Sunset on the Himalayan arc from Nagarkot is one of those views that changes your sense of scale permanently.",
              details: [
                '🏔️ February is one of the best months for Himalayan visibility — pre-monsoon haze hasn\'t set in yet',
                '🌄 Sunset typically 5:30–6pm in late February',
                '🚗 Nagarkot: 32km from Kathmandu city centre, 10km from Changu Narayan · Hire a taxi for the afternoon (NPR 3,000–4,000 Bhaktapur → Changu → Nagarkot → Kathmandu)',
                '🏨 Option: Stay overnight in Nagarkot for the even more spectacular sunrise — then head back to Kathmandu in the morning',
                '❄️ Bring your warmest layer — at 2,175m it drops to near freezing at sunset, even in February'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner / Snack at Sunset',
              name: 'Club Himalaya or Nagarkot Farmhouse',
              description: "Several lodges at Nagarkot serve hot tea, butter chicken, and thukpa on view-facing decks. Club Himalaya has the best infrastructure; Nagarkot Farmhouse has better food and atmosphere. Either works for a warm post-sunset meal before the drive down.",
              meta: '💰 $$ · 📍 Nagarkot hilltop'
            }
          ],
          tips: [
            { type: 'tip', text: 'Hire a single taxi driver for the entire day: Kathmandu → Bhaktapur → Changu Narayan → Nagarkot → Kathmandu. Negotiate a full-day rate (NPR 4,000–5,500 including fuel and waiting time). Your hotel/guesthouse can arrange a trusted driver the night before.' },
            { type: 'tip', text: 'The drive down from Nagarkot to Kathmandu at night is winding and takes about 1.5 hours. Your driver will know it well — trust them. Arrive back in Thamel by 8:30–9pm for a final dinner.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.6715, lng: 85.4298, label: 'Bhaktapur Durbar Square', num: 1, cat: 'attraction', desc: 'UNESCO medieval city — Golden Gate, 55-Window Palace, stone temples' },
        { lat: 27.6710, lng: 85.4320, label: 'Nyatapola Temple (Taumadhi Square)', num: 2, cat: 'attraction', desc: 'Nepal\'s tallest pagoda — 5 stories, perfect proportions, 1702 AD' },
        { lat: 27.6700, lng: 85.4350, label: 'Pottery Square (Chakhu Dhoka)', num: 3, cat: 'attraction', desc: 'Working pottery market — buy direct from makers shaping clay on wheel' },
        { lat: 27.6695, lng: 85.4370, label: 'Peacock Window (Dattatreya Square)', num: 4, cat: 'attraction', desc: 'Finest woodcarving in Asia — intricate latticework on the NPR 10 note' },
        { lat: 27.6933, lng: 85.4516, label: 'Changu Narayan Temple', num: 5, cat: 'attraction', desc: 'Nepal\'s oldest temple (4th century) — Licchavi art, hilltop serenity' },
        { lat: 27.7167, lng: 85.5166, label: 'Nagarkot Viewpoint', num: 6, cat: 'attraction', desc: 'Best Himalayan panorama near Kathmandu — Everest visible on clear days' },
        { lat: 27.6710, lng: 85.4315, label: 'Café Nyatapola', num: 7, cat: 'food', desc: 'Juju dhau and chiura breakfast with Nyatapola Temple filling the view' },
        { lat: 27.7167, lng: 85.5166, label: 'Club Himalaya / Nagarkot Farmhouse', num: 8, cat: 'food', desc: 'Hot thukpa and butter chicken at sunset, 2,175m altitude' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (Thamel guesthouse)', budget: '$10–20/night', midrange: '$25–60/night', luxury: '$80–200/night' },
    { category: 'Meals (solo)', budget: '$5–10/day', midrange: '$15–30/day', luxury: '$40–70/day' },
    { category: 'Entry fees (all UNESCO sites)', budget: '~$35 total', midrange: '~$35 total', luxury: '~$35 total' },
    { category: 'Transport (taxis, day hire)', budget: '$10–20/day', midrange: '$25–40/day', luxury: '$50–80/day' },
    { category: 'Bhaktapur/Nagarkot full-day taxi', budget: 'NPR 4,000 (~$30)', midrange: 'NPR 5,000 (~$38)', luxury: 'Private car $60–80' },
    { category: '3-Day Total (solo)', budget: '$80–120', midrange: '$150–220', luxury: '$300–500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tribhuvan International Airport (KTM) — 5km from Thamel', 'Prepaid taxi to Thamel: NPR 700–900 from the airport desk (~$5–7)', 'Direct flights from Delhi, Doha, Kuala Lumpur, Bangkok, Singapore', 'Nepal Visa: available on arrival at KTM ($30 for 15 days, $50 for 30 days) — bring 1 passport photo and USD cash'] },
    { title: '🏨 Where to Stay', items: ['Hotel Encounter Nepal — clean, central Thamel, great rooftop ($15–25)', 'Hotel Manaslu — established guesthouse, garden courtyard ($25–40)', 'Dwarika\'s Hotel — Kathmandu\'s finest, traditional Newar architecture ($150–300/night)', 'Stay in Thamel: noisy but centrally located — everything within walking distance or short taxi'] },
    { title: '🌡️ February Weather', items: ['Daytime: 10–18°C (warm in the sun, cool in shade)', 'Nights: 2–5°C — bring a real warm jacket', 'Mountain views: excellent clarity in late February — one of the best months', 'Air quality: improved in winter, but still variable — AQI app useful'] },
    { title: '💳 Money & Logistics', items: ['Currency: Nepali Rupee (NPR) — roughly 133:1 USD', 'ATMs: widely available in Thamel — Nabil Bank and Standard Chartered most reliable', 'Cash is king outside central Kathmandu — carry small bills', 'Bargaining: expected at markets and souvenir shops, not restaurants'] },
    { title: '📱 SIM & Connectivity', items: ['Buy an Ncell or Nepal Telecom SIM at the airport — NPR 200 starter, data is cheap', '2GB data: NPR 200 (~$1.50) — speeds are decent in the valley', 'Wi-Fi at all Thamel guesthouses and most cafes', 'Download offline Google Maps before arriving — essential for old town navigation'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
