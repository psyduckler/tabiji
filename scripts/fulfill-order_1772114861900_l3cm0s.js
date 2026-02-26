const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772114861900_l3cm0s',
  email: 'sophieslot@hotmail.com',
  destination: 'Bangkok & Luang Prabang',
  startDate: '2026-05-08',
  endDate: '2026-05-17',
  groupSize: 2,
  requests: 'A 2 days one night boat trip over Mekong from northern Thailand to Luang Prabang. Some time for chill reading.'
};

const itineraryData = {
  destination: 'Bangkok & Luang Prabang',
  countryEmoji: '🇹🇭🇱🇦',
  title: 'Bangkok to Luang Prabang: Markets, Temples & the Mekong Slow Boat',
  subtitle: '10 days of street food, sacred temples, a legendary river crossing, and blissful downtime for two',
  description: "Begin in Bangkok — Asia's most electrifying city — where ancient temples glow gold beside neon-lit streets, and every corner hides a world-class bowl of noodles. Then head north to Chiang Rai before crossing into Laos for one of Southeast Asia's great adventures: the two-day Mekong slow boat from Huay Xai to Luang Prabang. Drift through jungle-clad mountains, village riverbanks, and golden light to arrive in Luang Prabang — a UNESCO World Heritage town of saffron-robed monks, waterfall pools, and the kind of deep calm that makes you forget what day it is. The perfect blend of adventure, culture, food, and soul-restoring stillness.",
  duration: '9 nights',
  dates: 'May 8 – May 17, 2026',
  budget: '$$',
  pace: 'Balanced',
  bestFor: 'Couples, Adventurers, Foodies, Culture Seekers',

  highlights: [
    'Two-day Mekong slow boat from Huay Xai to Luang Prabang',
    'Grand Palace and Wat Pho in Bangkok',
    'Street food feasting in Yaowarat Chinatown and Or Tor Kor Market',
    "Chiang Rai's surreal White Temple (Wat Rong Khun)",
    'Kuang Si turquoise waterfall with lazy afternoon swimming',
    'Watching monks collect alms at dawn in Luang Prabang',
    'Hammock and book time on the Mekong riverbanks'
  ],

  essentials: [
    {
      title: '🛂 Visas',
      text: 'Thailand: visa-free on arrival for most nationalities (30 days). Laos: e-visa available online ($30–50 USD) or visa on arrival at Huay Xai border (~$35–50 USD). Apply for the e-visa before leaving Bangkok to save time at the border.'
    },
    {
      title: '🌧️ May Weather',
      text: "May is the start of the rainy season in both countries — expect warm temperatures (28–35°C), high humidity, and afternoon rain showers. Bangkok can be sticky; Luang Prabang is lush and green. Pack light, breathable clothes, a packable rain jacket, and sturdy sandals. The Mekong is high and fast in May — the slow boat runs smoothly."
    },
    {
      title: '💵 Money & Budget',
      text: 'Budget $100–150 USD/day for two (mid-range). Bangkok: ATMs everywhere, Kasikorn and Bangkok Bank have low fees. Laos: bring USD cash — ATMs are scarce and often out of service on the slow boat route. Exchange at official booths, not street money changers. The slow boat operators prefer cash for onboard food and drinks.'
    },
    {
      title: '🛥️ Slow Boat Essentials',
      text: "Book the Luang Say slow boat or the Shompoo Cruise for a more comfortable experience (cushioned seats, snacks, guide). The basic public slow boat is also fine — many travellers love the social atmosphere. Pack: a good book (or two!), snacks, a pillow or neck cushion, headphones, sunscreen, and cash for the Pakbeng overnight stop. You'll want a Lao SIM for connectivity."
    },
    {
      title: '🕌 Temple Etiquette',
      text: 'Cover shoulders and knees in temples — both Bangkok and Luang Prabang. Remove shoes before entering. In Luang Prabang, be respectful during the alms-giving ceremony (tak bat): stand back, be quiet, and do not touch the monks or offer food unless you know how. The ceremony is sacred, not a tourist spectacle.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-08',
      neighborhoods: 'Riverside · Rattanakosin · Chinatown',
      title: 'Bangkok Arrival — River, Temples & Chinatown Nights',
      description: "Land in Bangkok and ease into the city's intoxicating rhythm. A leisurely afternoon in the Riverside area, a golden hour moment at Wat Pho, and dinner deep in the fiery chaos of Yaowarat — Bangkok's legendary Chinatown.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Riverside Walk',
              description: "Settle into your hotel near the Chao Phraya River and take a slow stroll along the riverside promenade. The afternoon light on the golden spires is stunning. Grab a river taxi (15 baht) to hop between piers.",
              details: [
                '🏨 Stay near Tha Tien pier for easy temple access — Praya Palazzo, Sala Rattanakosin, or Chakrabongse Villas (splurge)',
                '⛵ Grab a Chao Phraya Express Boat from any pier — easiest way to navigate',
                '📸 Wang Lang (Siriraj) pier has great views back towards the Grand Palace'
              ]
            },
            {
              title: 'Wat Pho — Temple of the Reclining Buddha',
              description: "Visit Wat Pho in the golden afternoon light. The 46-metre gilded Reclining Buddha is breathtaking in scale and serenity. Wat Pho is also the birthplace of traditional Thai massage — book a 30-minute session in the courtyard (300 THB).",
              details: [
                '⏰ Open 8am–6pm · Admission 200 THB',
                '👗 Sarongs available at the entrance if needed',
                '💆 Onsite massage school — traditional Thai massage 30 min for 300 THB',
                '🕐 Allow 1.5–2 hours to explore the temple compound'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Grand Palace is next door — save it for Day 2 when you have a full morning. Trying to do both on arrival day is exhausting.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yaowarat Chinatown Street Food Crawl',
              description: "Take a tuk-tuk or Grab to Yaowarat Road — Bangkok's Chinatown and one of Asia's greatest street food destinations. The street comes alive after dark with crab stalls, roast duck vendors, seafood on ice, and legendary pad thai joints.",
              details: [
                '🦀 T&K Seafood — legendary crab and prawn, always a queue',
                '🍜 Thipsamai Pad Thai — the most famous pad thai in Bangkok (queue early)',
                '🍢 Wander Yaowarat Soi 11 for oyster omelettes and grilled skewers',
                '🫘 Lek & Rut Seafood has been serving since 1952',
                '⚠️ Street food is your best bet — avoid tourist restaurants near temples'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Yaowarat Street Food Crawl',
              description: 'Graze through the world-famous Chinatown street stalls. Order pad thai at Thipsamai, crab at T&K, and finish with a fresh mango sticky rice from a cart.',
              meta: '💰 $ · 📍 Yaowarat Road, Bangkok · Best after 7pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 13.7465, lng: 100.4931, label: 'Wat Pho', num: 1, cat: 'attraction', desc: 'Temple of the Reclining Buddha — must-see on arrival afternoon' },
        { lat: 13.7436, lng: 100.4855, label: 'Wat Arun', num: 2, cat: 'attraction', desc: 'Temple of Dawn — stunning from across the river at sunset' },
        { lat: 13.7408, lng: 100.5107, label: 'Yaowarat Chinatown', num: 3, cat: 'food', desc: 'Bangkok\'s legendary street food district — come hungry after dark' },
        { lat: 13.7455, lng: 100.4963, label: 'Chao Phraya Riverside', num: 4, cat: 'attraction', desc: 'River taxis, golden temples, and evening breezes' },
        { lat: 13.7447, lng: 100.5113, label: 'Thipsamai Pad Thai', num: 5, cat: 'food', desc: 'Bangkok\'s most famous pad thai — queue worth it' }
      ]
    },
    {
      num: 2,
      date: '2026-05-09',
      neighborhoods: 'Rattanakosin · Dusit · Bang Rak',
      title: 'Grand Palace, Sacred Temples & Rooftop Sundowners',
      description: "An iconic Bangkok day — the glittering Grand Palace complex, Wat Phra Kaew's Emerald Buddha, and Wat Arun at sunset. Cool down with a riverside cocktail from a rooftop bar as the city lights up below.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grand Palace & Wat Phra Kaew',
              description: "Arrive early (8am) to beat both the heat and the crowds at one of the world's most dazzling royal complexes. The Temple of the Emerald Buddha sits within the palace walls — the gilded architecture, mosaic spires, and mythological murals are staggering in their detail.",
              details: [
                '⏰ Open 8:30am–3:30pm · Admission 500 THB (includes Wat Phra Kaew)',
                '👗 Strict dress code — cover shoulders and knees. Sarongs for rent at gate',
                '⚠️ Tuk-tuk drivers outside may say it\'s closed — it\'s almost never closed, this is a scam',
                '🗺️ Allow 2–3 hours to do it justice',
                '☀️ Bring water and sunscreen — the courtyards are exposed and blazing'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Khao Tom at a local shophouse',
              description: 'Start with rice porridge (khao tom) or jok (congee) from a street shophouse near your hotel. Classic Thai breakfast — light, warming, and about 50 THB.',
              meta: '💰 $ · 📍 Any local shophouse near the riverside'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wat Arun — Temple of Dawn',
              description: "Cross the river by ferry (3–5 baht) to reach Wat Arun — arguably Bangkok's most photogenic temple. Climb the steep central prang for sweeping river views. The tower is encrusted with thousands of colourful porcelain fragments.",
              details: [
                '⛵ Ferry from Tha Tien pier (opposite Wat Pho) — 3 THB',
                '⏰ Open 8am–6pm · Admission 100 THB',
                '📸 Best photos from the Wat Pho side of the river at sunset',
                '🪜 Steep stairs to climb — wear shoes with grip'
              ]
            },
            {
              title: 'Jim Thompson House',
              description: "Take a Grab to the Jim Thompson House — an atmospheric cluster of traditional Thai silk merchant houses turned museum. The story of its owner's mysterious disappearance adds intrigue to beautiful antiques and textiles.",
              details: [
                '⏰ Open daily 10am–6pm · Admission 200 THB',
                '🧵 Buy Thai silk at the adjacent shop — excellent quality',
                '🌿 The garden is lush and cool — perfect midday escape'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Err Urban Rustic Thai',
              description: 'Hip restaurant near the Grand Palace specialising in smoky, fermented, and aged Thai flavours. A modern lens on ancient recipes — excellent sharing plates.',
              meta: '💰 $$ · 📍 394/35 Maharaj Rd, Phra Nakhon'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Cocktails at a Rooftop Bar',
              description: "Bangkok's rooftop bar scene is legendary. Head to Lebua Sky Bar (immortalised in The Hangover Part II) or the more local-favourite Octave Rooftop Lounge at Bangkok Marriott for 360° city views and expert cocktails at golden hour.",
              details: [
                '🍸 Lebua Sky Bar — iconic, pricier, worth it for the view (State Tower, Silom)',
                '🍸 Octave Rooftop — Sukhumvit, 360° panorama, more relaxed',
                '👔 Smart casual dress required at most rooftop bars',
                '🌅 Arrive 45 minutes before sunset for a table'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nahm Restaurant',
              description: 'One of Bangkok\'s finest Thai restaurants — serious, research-driven cooking rooted in royal Thai cuisine. David Thompson\'s menu is a master class in the complexity of Thai flavour.',
              meta: '💰 $$$ · 📍 COMO Metropolitan Hotel, Sathorn'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 13.7500, lng: 100.4913, label: 'Grand Palace', num: 1, cat: 'attraction', desc: 'The dazzling royal complex — arrive at 8am to beat crowds' },
        { lat: 13.7500, lng: 100.4913, label: 'Wat Phra Kaew', num: 2, cat: 'attraction', desc: 'Temple of the Emerald Buddha within the Grand Palace walls' },
        { lat: 13.7436, lng: 100.4855, label: 'Wat Arun', num: 3, cat: 'attraction', desc: 'Temple of Dawn — climb the central prang for river views' },
        { lat: 13.7457, lng: 100.5285, label: 'Jim Thompson House', num: 4, cat: 'attraction', desc: 'Thai silk merchant museum in atmospheric traditional houses' },
        { lat: 13.7215, lng: 100.5133, label: 'Lebua Sky Bar', num: 5, cat: 'attraction', desc: 'Iconic rooftop bar — panoramic Bangkok skyline views' },
        { lat: 13.7216, lng: 100.5172, label: 'Nahm Restaurant', num: 6, cat: 'food', desc: 'Royal Thai cuisine masterclass — book ahead' }
      ]
    },
    {
      num: 3,
      date: '2026-05-10',
      neighborhoods: 'Chatuchak · Or Tor Kor · Ekkamai · Thonglor',
      title: "Markets, Massages & Bangkok's Foodie Side Streets",
      description: "A market day with a difference — browse Chatuchak's 15,000-stall weekend market, graze through Or Tor Kor's upscale food hall, and wind down in the hip Ekkamai and Thonglor neighbourhood with craft beer and modern Thai cooking.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Chatuchak Weekend Market',
              description: "One of the world's largest weekend markets — 15,000 stalls across 35 acres of plants, vintage clothing, ceramics, street food, antiques, and oddities. Go early (9am) before the heat peaks. Get purposefully lost in the grid of covered alleyways.",
              details: [
                '⏰ Open Sat–Sun 9am–6pm · Free entry',
                '🗺️ Grab a section map at the entrance — Section 2 for art, 18–19 for food',
                '💧 Buy fresh coconut water from every second stall — you\'ll need it',
                '💳 Some stalls cash only — bring Thai baht',
                '🚇 Take the MRT to Chatuchak Park station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Or Tor Kor Market Food Hall',
              description: "Bangkok's finest covered fresh market — upscale produce, prepared foods, and some of the city's best khao man gai (poached chicken rice) stalls. A short walk from Chatuchak.",
              meta: '💰 $ · 📍 Kamphaeng Phet Rd, opposite Chatuchak Park'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Traditional Thai Massage',
              description: "Treat yourselves to a proper Thai massage at a reputable parlour. Ruen-Nuad Massage Studio in Silom is a beautiful traditional wooden house set in a quiet garden — the best mid-range option in the city.",
              details: [
                '💆 Ruen-Nuad Massage Studio, Silom — 2hr oil or Thai massage ~600 THB',
                '💆 Health Land Spa — multiple locations, excellent value',
                '⏰ Book ahead online or arrive early to avoid waits on weekends'
              ]
            },
            {
              title: 'Afternoon Reading & Coffee Break',
              description: "Bangkok has a thriving café culture. Find a beautiful air-conditioned spot and settle in with your book. Souvenir is a beautiful bookshop-café near the river. Paper Butter & the Burger in Ari is beloved by locals.",
              details: [
                '📚 Souvenir Bookshop & Café — a love letter to reading',
                '☕ Roots Coffee Roaster — among the best specialty coffee in Bangkok',
                '🏡 Grab an iced Americano, find a quiet corner, let Bangkok disappear for an hour'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ekkamai & Thonglor — Bangkok\'s Hip Local Scene',
              description: "Head to Ekkamai/Thonglor — where Bangkok's cool kids eat and drink. Tree-lined streets, independent restaurants, jazz bars, and craft beer taprooms. A world away from tourist Bangkok.",
              details: [
                '🍺 Hair of the Dog — Bangkok\'s best craft beer bar',
                '🎵 WTF Gallery Café — weird, wonderful, eclectic bar with revolving art shows',
                '🌃 The Ekkamai street food lanes — local vendors, cheap and delicious'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Samlor',
              description: 'Modern Thai bistro in Thonglor — exceptional curries, salads, and larb using heirloom ingredients. One of Bangkok\'s most exciting younger restaurants.',
              meta: '💰 $$ · 📍 Thonglor Soi 10, Bangkok · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 13.7999, lng: 100.5500, label: 'Chatuchak Weekend Market', num: 1, cat: 'attraction', desc: 'One of the world\'s largest markets — arrive early' },
        { lat: 13.8030, lng: 100.5490, label: 'Or Tor Kor Market', num: 2, cat: 'food', desc: 'Bangkok\'s finest fresh produce and food hall' },
        { lat: 13.7245, lng: 100.5312, label: 'Ruen-Nuad Massage Studio', num: 3, cat: 'attraction', desc: 'Traditional Thai massage in a beautiful garden house' },
        { lat: 13.7255, lng: 100.5860, label: 'Ekkamai / Thonglor', num: 4, cat: 'attraction', desc: 'Bangkok\'s hippest neighbourhood for food, bars, and cafés' },
        { lat: 13.7267, lng: 100.5848, label: 'Hair of the Dog', num: 5, cat: 'food', desc: 'Bangkok\'s best craft beer bar' },
        { lat: 13.7280, lng: 100.5862, label: 'Samlor Restaurant', num: 6, cat: 'food', desc: 'Modern Thai bistro — one of Bangkok\'s most exciting restaurants' }
      ]
    },
    {
      num: 4,
      date: '2026-05-11',
      neighborhoods: 'Bangkok → Chiang Rai',
      title: 'Bangkok to Chiang Rai — Gateway to the Golden Triangle',
      description: "Your last Bangkok morning — a slow coffee at a canal-side café before a flight north to Chiang Rai. Explore the surreal White Temple in the afternoon, then ease into the city's night bazaar for dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Last Bangkok Morning — Canal Walk & Coffee',
              description: "Take a final Bangkok stroll along the Khlong (canal) near Banglamphu — local longboat taxis zip past, vendors sell grilled corn and fresh fruit, and you might stumble on a floating market. A slice of old Bangkok that tourists rarely see.",
              details: [
                '⛵ Longboat taxi on Khlong Saen Saep — 20–50 THB across the city',
                '☕ Grab coffee at Roots or a local shophouse',
                '🕙 Check out by 10am — flight to Chiang Rai in early afternoon'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Canal-side coffee and pastries',
              description: 'Any of the local café-bakeries near Banglamphu or your hotel. Or go classic — iced Thai tea and fresh-grilled toast with pandan jam from a street cart.',
              meta: '💰 $ · 📍 Near your hotel or any canal-side café'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Flight to Chiang Rai + White Temple (Wat Rong Khun)',
              description: "Fly Bangkok → Chiang Rai (~1.5 hrs, Air Asia or Nok Air ~$30-60 USD). Pick up a rental car or take a songthaew (shared taxi) and head straight to Wat Rong Khun — the astonishing White Temple. Built by local artist Chalermchai Kositpipat, it's one of the most striking temples in Asia — blindingly white, covered in mirror fragments, with a bridge over a sea of hands.",
              details: [
                '✈️ DMK → CEI (Don Mueang → Chiang Rai) — book in advance',
                '🚗 Rental cars from Chiang Rai airport are easy and cheap (~$25/day)',
                '⏰ Wat Rong Khun open 6:30am–6pm · Admission 100 THB',
                '📸 Best photos: morning light (or late afternoon if you arrive by 3pm)',
                '⚠️ Extremely popular — weekday afternoons slightly quieter'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chiang Rai Night Bazaar',
              description: "Chiang Rai's night market is small, charming, and unpretentious — local crafts, Hilltribe textiles, silver jewellery, and street food. A world away from Bangkok's commercialised tourist bazaars.",
              details: [
                '🕗 Open from 6pm–11pm nightly',
                '🎨 Hill Tribe Textiles are excellent quality here',
                '🎵 Night Bazaar stage hosts local music most evenings'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Khao Soi Mae Sai',
              description: "Chiang Rai's most-loved khao soi (Northern Thai curry noodle soup) restaurant. Order the rich, coconut curry egg noodle soup with crispy noodles on top — a Northern Thailand speciality you must eat here.",
              meta: '💰 $ · 📍 Chiang Rai city centre · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 13.7597, lng: 100.4969, label: 'Khao San Road / Banglamphu Canal', num: 1, cat: 'attraction', desc: 'Final Bangkok morning stroll along the canal' },
        { lat: 13.9169, lng: 100.6064, label: 'Don Mueang Airport (DMK)', num: 2, cat: 'attraction', desc: 'Bangkok\'s domestic airport — flights to Chiang Rai from here' },
        { lat: 19.8244, lng: 99.7632, label: 'Wat Rong Khun (White Temple)', num: 3, cat: 'attraction', desc: 'Surreal, mirror-encrusted white temple — one of Thailand\'s most striking' },
        { lat: 19.9073, lng: 99.8334, label: 'Chiang Rai Night Bazaar', num: 4, cat: 'attraction', desc: 'Charming night market with Hilltribe crafts and street food' },
        { lat: 19.9082, lng: 99.8341, label: 'Khao Soi Mae Sai', num: 5, cat: 'food', desc: 'Legendary Northern Thai curry noodle soup restaurant' }
      ]
    },
    {
      num: 5,
      date: '2026-05-12',
      neighborhoods: 'Chiang Rai · Chiang Khong · Huay Xai Border',
      title: 'Golden Triangle & The Border Crossing to Laos',
      description: "A morning at the enigmatic Golden Triangle — where Thailand, Laos, and Myanmar converge at the Mekong — then cross into Laos at the Chiang Khong/Huay Xai border. Tonight is your last night before the river; sleep early, the boat departs at 8am.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Golden Triangle & Opium Museum',
              description: "Drive to the Golden Triangle — the storied meeting point of three countries at the Mekong River. The Hall of Opium (funded by the Mae Fah Luang Foundation) is a sobering and excellent museum on the history of the opium trade in the region.",
              details: [
                '📍 About 60km north of Chiang Rai — 1 hour drive',
                '⏰ Hall of Opium open Tue–Sun, 8:30am–4pm · Admission 200 THB',
                '⛵ Take a short boat trip to see the exact confluence (50 THB)',
                '🇱🇦 You can see the Laos riverbank and Casinos from here'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cross to Huay Xai — Laos Border',
              description: "Head south to Chiang Khong (about 30 mins from the Golden Triangle) and cross the 4th Thai–Lao Friendship Bridge into Huay Xai, Laos. Get your Lao visa on arrival or use your pre-obtained e-visa. Exchange money to Lao Kip and USD here.",
              details: [
                '🛂 Visa on arrival at Huay Xai: ~$35–50 USD, passport photo required',
                '🏦 Exchange money at the border — better rates than guesthouses',
                '⏰ Border crossing hours: 6am–10pm (allow 1–2 hours)',
                '📝 Book slow boat tickets in Huay Xai (Luang Say Cruise or Shompoo)',
                '💡 Book the Luang Say Cruise for cushioned seats, guide, and meals included'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Last Thai Meal in Chiang Khong',
              description: 'Eat well in Chiang Khong before crossing. Try the riverside restaurants on the Thai side for a final Thai-style fish curry or larb before entering Laos.',
              meta: '💰 $ · 📍 Chiang Khong riverside'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Settle Into Huay Xai — Early Night',
              description: "Huay Xai is a small, relaxed border town. Walk the riverside promenade, buy snacks and supplies for the boat (the boat has cold drinks but pack your own snacks), and get an early night — the slow boat departs at 8am sharp.",
              details: [
                '🛒 Buy snacks, books, and sunscreen for the boat journey',
                '🍺 Daofa Restaurant by the river is pleasant for a sunset beer',
                '🛏️ Stay at: Huay Xai Riverside Hotel or Ban Khily Guesthouse',
                '⏰ Set your alarm — boat departs 8am from the Huay Xai pier'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Daofa Restaurant',
              description: 'Reliable riverfront restaurant in Huay Xai — Lao and Thai dishes, cold Beerlao, and a view of the Mekong at dusk. Simple and satisfying.',
              meta: '💰 $ · 📍 Huay Xai riverside'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.3489, lng: 100.0854, label: 'Golden Triangle', num: 1, cat: 'attraction', desc: 'Where Thailand, Laos & Myanmar meet at the Mekong' },
        { lat: 20.3544, lng: 100.0861, label: 'Hall of Opium Museum', num: 2, cat: 'attraction', desc: 'Excellent museum on the history of the opium trade' },
        { lat: 20.1667, lng: 100.4000, label: 'Chiang Khong / Friendship Bridge', num: 3, cat: 'attraction', desc: 'Thai–Lao border crossing into Huay Xai' },
        { lat: 20.2692, lng: 100.4111, label: 'Huay Xai Pier', num: 4, cat: 'attraction', desc: 'Slow boat departure point — arrive before 8am' },
        { lat: 20.2685, lng: 100.4118, label: 'Daofa Restaurant', num: 5, cat: 'food', desc: 'Riverfront dinner with Mekong views before the boat' }
      ]
    },
    {
      num: 6,
      date: '2026-05-13',
      neighborhoods: 'Mekong River · Huay Xai to Pakbeng',
      title: 'Slow Boat Day 1 — Into the Mekong Jungle',
      description: "The slow boat journey begins. Eight hours drifting southeast through the heart of Laos: towering jungle-clad mountains, tiny villages appearing on the riverbanks, fishermen in long-tail boats, and absolute, meditative stillness. This is the highlight of the trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Departure from Huay Xai Pier',
              description: "Board the slow boat at the Huay Xai pier by 8am. The boat is a long, narrow wooden vessel — if you booked Luang Say, expect cushioned seats and a guide. Public slow boats have wooden benches — bring a cushion or your sleeping bag liner for comfort. Find seats at the back where you can spread out and watch the river.",
              details: [
                '⏰ Depart 8am sharp — arrive 30 mins early to secure good seats',
                '🪑 Luang Say Cruise: cushioned seats, meals included, English guide (~$200/person, 2 days)',
                '🪑 Public slow boat: 230,000 Kip (~$11) each way, basic wooden benches',
                '📦 Store luggage in the hold — take a day bag with essentials onto the boat',
                '💧 Bottled water and cold Beerlao available onboard'
              ]
            },
            {
              title: 'Morning on the River',
              description: "The Mekong in May is high and powerful — the boat cuts through brownish-gold water flanked by hills cloaked in tropical forest. There is nothing to do but look, read, talk, and breathe. This is exactly the point. Settle in with your book and let the river do its thing.",
              details: [
                '📚 This is prime reading time — bring at least one great novel',
                '📷 The light is beautiful in the first morning hours',
                '🐦 Watch for fishing birds, monitor lizards on rocks, and village smoke rising through the trees',
                '🌧️ May showers are brief — duck under the canvas canopy'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "The slow boat is about the journey, not the destination. Resist the urge to do things. Let yourself be bored in the best possible way — the river will reward you." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Village Stops & Afternoon Reading',
              description: "The boat makes occasional stops at small riverside villages to drop off supplies and passengers. If yours stops at Ban Pakha or similar, hop ashore briefly for a look. Otherwise: more reading, more river.",
              details: [
                '🏘️ River villages are wonderfully unhurried — children wave from the banks',
                '🌄 The light in the afternoon makes the green hills glow',
                '☕ Pack instant coffee or tea bags for an afternoon brew'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch on the Boat',
              name: 'Packed lunch (Luang Say includes meals)',
              description: 'Luang Say guests get a packed lunch included. Public boat passengers should bring their own food — stock up on sticky rice parcels, fruit, and snacks in Huay Xai before departure.',
              meta: '💰 Included with Luang Say · $ bring your own on public boat'
            },
            {
              type: '🍺 Drinks',
              name: 'Beerlao on the Mekong',
              description: 'The best beer in Southeast Asia, served cold on a slow wooden boat on the Mekong. One of life\'s great simple pleasures.',
              meta: '💰 $ · 📍 Onboard'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Arrive Pakbeng — Overnight Stop',
              description: "The boat docks at Pakbeng around 5–6pm. This tiny hilltop village exists almost entirely to host slow boat travellers for one night. Walk up the main street, watch the sunset over the Mekong, have dinner, and sleep early — Day 2 departs at 8am.",
              details: [
                '🛏️ Luang Say Mekong Lodge — excellent (included with Luang Say Cruise)',
                '🛏️ Santi Guesthouse or Monsavanh Guesthouse — good budget options',
                '🌅 Walk to the hill above town for Mekong sunset views',
                '⚠️ Electricity may cut out after midnight — not unusual in Pakbeng'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pakbeng riverside restaurants',
              description: 'Simple Lao food — grilled fish from the Mekong, sticky rice, green papaya salad, and cold Beerlao. Nothing fancy, everything satisfying.',
              meta: '💰 $ · 📍 Pakbeng main street'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2692, lng: 100.4111, label: 'Huay Xai Pier — Boat Departs', num: 1, cat: 'attraction', desc: 'Slow boat departure point — 8am sharp' },
        { lat: 20.1500, lng: 100.7000, label: 'Mekong River — Morning Section', num: 2, cat: 'attraction', desc: 'Deep jungle hills, fishing villages, golden river' },
        { lat: 19.8500, lng: 101.1334, label: 'Pakbeng', num: 3, cat: 'attraction', desc: 'Overnight village stop on the Mekong slow boat route' },
        { lat: 19.8498, lng: 101.1337, label: 'Luang Say Mekong Lodge', num: 4, cat: 'attraction', desc: 'Best accommodation in Pakbeng — included with Luang Say Cruise' },
        { lat: 20.0000, lng: 100.9000, label: 'Riverside Village Stop', num: 5, cat: 'attraction', desc: 'Typical Mekong riverside village — wave back to the kids' }
      ]
    },
    {
      num: 7,
      date: '2026-05-14',
      neighborhoods: 'Pakbeng to Luang Prabang via Mekong',
      title: 'Slow Boat Day 2 — Arrival in the Ancient Capital',
      description: "The second day on the river is shorter and arguably more beautiful. The Mekong narrows, the forest presses closer, and excitement builds as you approach Luang Prabang — one of Southeast Asia's most remarkable cities. Arrive in the late afternoon to ancient golden temples and the scent of frangipani.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Day 2 Departure from Pakbeng',
              description: "Up early, onto the boat by 8am. Today is a shorter ride — about 6 hours. The scenery in the lower Mekong section is arguably more dramatic: the river bends through steep limestone cliffs and the banks grow more populated as you approach Luang Prabang.",
              details: [
                '⏰ Depart 8am from Pakbeng pier',
                '📚 Another perfect reading morning — settle in with your book',
                '🦅 Bird life is more abundant in this section — look for kingfishers and egrets',
                '🌿 The vegetation changes subtly as you move south'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Breakfast in Pakbeng before departure',
              description: 'Simple noodle soup or baguette (the French colonial legacy is everywhere in Laos, even this far north) at a Pakbeng café before boarding.',
              meta: '💰 $ · 📍 Pakbeng main street — any open café at 7am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pak Ou Caves — Sacred River Caves',
              description: "One to two hours before Luang Prabang, the boat passes the Pak Ou Caves — sacred limestone grottoes set into a cliff at the confluence of the Ou and Mekong rivers. Thousands of Buddha statues have been placed here over centuries. The Luang Say Cruise includes a stop; on the public boat, arrange a local boat from Luang Prabang later.",
              details: [
                '⛵ Luang Say stops here — free with the cruise',
                '📿 Over 4,000 Buddha images in two main caves',
                '☀️ The afternoon light through the cave entrance is gorgeous'
              ]
            },
            {
              title: 'Arrival at Luang Prabang — The Ancient Capital',
              description: "The boat docks at Ban Don pier on the outskirts of Luang Prabang around 2–3pm. The UNESCO World Heritage city reveals itself in layers: golden temple spires, frangipani trees, French colonial architecture, and a sleepiness that seems almost protective of its own peace. Grab a tuk-tuk to your guesthouse.",
              details: [
                '🏨 Stay in the old town UNESCO core — Sayo River Guesthouse, La Maison Dalabua, or Villa Santi',
                '🛺 Tuk-tuk from Ban Don pier to town: ~50,000 Kip (negotiate)',
                '🌳 Walk the Sisavangvong Road and just breathe in the atmosphere'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Night Market & First Luang Prabang Evening',
              description: "Luang Prabang's famous night market stretches along Sisavangvong Road every evening — hand-woven textiles, silver jewellery, silk scarves, and Hmong and Khmu handicrafts. Browse slowly. Then find a restaurant with a candlelit balcony for a proper Lao welcome dinner.",
              details: [
                '🛍️ Night market open 5pm–11pm daily',
                '🧣 Buy hand-woven silk scarves direct from village weavers',
                '🌙 The old town at night is magical — lanterns, temple bells, frangipani scent'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tamarind Restaurant',
              description: 'The definitive introduction to Lao cuisine — set in a garden on the Nam Khan river, Tamarind has been teaching travellers about Lao food for 20 years. Try the tasting menu for a full flavour tour.',
              meta: '💰 $$ · 📍 Ban Vat Sene, Luang Prabang · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8500, lng: 101.1334, label: 'Pakbeng Pier — Day 2 Departs', num: 1, cat: 'attraction', desc: 'Second day on the Mekong begins here at 8am' },
        { lat: 20.0563, lng: 102.2200, label: 'Pak Ou Caves', num: 2, cat: 'attraction', desc: 'Sacred river caves with 4,000+ Buddha statues in cliff limestone' },
        { lat: 19.8900, lng: 102.1366, label: 'Ban Don Pier — Luang Prabang Arrival', num: 3, cat: 'attraction', desc: 'Slow boat arrival pier for Luang Prabang' },
        { lat: 19.8940, lng: 102.1323, label: 'Luang Prabang Night Market', num: 4, cat: 'attraction', desc: 'Nightly handicraft and textile market on Sisavangvong Road' },
        { lat: 19.8870, lng: 102.1380, label: 'Tamarind Restaurant', num: 5, cat: 'food', desc: 'The best introduction to Lao cuisine — garden dining by the river' }
      ]
    },
    {
      num: 8,
      date: '2026-05-15',
      neighborhoods: 'Luang Prabang Old Town · Mount Phousi · Nam Khan River',
      title: 'Monks at Dawn, Ancient Temples & the Art of Doing Nothing',
      description: "Luang Prabang reveals itself best to those who move slowly. Wake before sunrise for the alms-giving ceremony, then explore the old town's ancient wats, climb Mount Phousi for panoramic views, and spend the afternoon exactly as planned: in a hammock with a book.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Tak Bat — Alms Giving at Dawn',
              description: "At sunrise, saffron-robed monks process silently through the old town streets collecting alms (sticky rice and food) from devout locals. It is one of the most beautiful and humbling sights in Southeast Asia. Stand at respectful distance — this is a living religious practice, not a performance.",
              details: [
                '⏰ Begins around 5:30–6am, earlier in May (shorter nights)',
                '🙏 Stand back at least 5 metres — observe quietly, no flash photography',
                '🙏 Do NOT touch the monks or join the line unless you are Buddhist and know the protocol',
                '📍 Best viewing: Sisavangvong Road near Wat Mai',
                '💡 Buy sticky rice from a local vendor to observe locals offering — but respectfully only'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Set your alarm. The alms ceremony is only on dawn. Missing it is one of the most common regrets of visitors to Luang Prabang.' }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Wat Xieng Thong — The Temple of the Golden City',
              description: "The finest temple in Laos — Wat Xieng Thong dates to 1560 and represents the pinnacle of Luang Prabang architecture. Steeply tiered roofs sweeping almost to the ground, intricate mosaic rear walls, and a serene atmosphere even with visitors present.",
              details: [
                '⏰ Open 8am–5pm · Admission 20,000 Kip (~$1)',
                '🏛️ Don\'t miss the "Tree of Life" mosaic on the rear chapel wall',
                '🛶 The temple sits at the confluence of the Mekong and Nam Khan rivers — gorgeous setting'
              ]
            },
            {
              title: 'Climb Mount Phousi',
              description: "328 steps to the summit of the sacred hill at the heart of the old town. From the top, That Chomsi stupa crowns the hill above a panorama of Luang Prabang, the Mekong, and the surrounding mountains. The view at sunrise or sunset is unforgettable.",
              details: [
                '⏰ Open from 6am · Admission 20,000 Kip',
                '👣 328 steps — takes about 20 minutes, comfortable pace',
                '📸 360° views: Mekong, Nam Khan, old town, jungle mountains in all directions'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Le Café Ban Vat Sene',
              description: 'Excellent French-Lao café in the old town — fresh baguettes, good coffee, eggs, and pastries in a colonial courtyard. The baguette sandwiches (khaow jii) are a Luang Prabang staple.',
              meta: '💰 $ · 📍 Sakkarine Road, Old Town'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hammock Time & Riverside Reading',
              description: "This is the planned downtime. Find a guesthouse hammock by the Nam Khan River, order an iced coffee, open your book, and stay there for as long as you want. Luang Prabang is the rare place where doing nothing feels like doing exactly the right thing.",
              details: [
                '🏝️ The L\'Elephant Blanc guesthouse has beautiful riverside hammocks',
                '☕ The Nam Khan coffee shops (near the bamboo bridge) are perfect',
                '📚 Don\'t feel guilty. This is the whole point of Luang Prabang.',
                '💧 Stay hydrated — May is warm and humid even in the shade'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Royal Palace Museum & Sunset on Mount Phousi',
              description: "Visit the former Royal Palace (now National Museum) for a glimpse into Lao royalty, then climb Phousi again for a spectacular sunset — the sky turns gold over the mountains and the Mekong bends around the town like a moat.",
              details: [
                '⏰ Royal Palace Museum open 8am–11:30am, 1pm–4pm · Closed Tuesdays',
                '📸 Mount Phousi at sunset is even better than sunrise — dozens of monks chant below'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Manda de Laos',
              description: 'The most atmospheric restaurant in Luang Prabang — set in a lotus pond-filled heritage villa. Exquisite Lao cuisine in an almost impossibly beautiful setting.',
              meta: '💰 $$$ · 📍 Off Sakkarine Rd, near Nam Khan river · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8945, lng: 102.1335, label: 'Tak Bat — Alms Ceremony', num: 1, cat: 'attraction', desc: 'Monks collect alms at dawn on Sisavangvong Road — observe with respect' },
        { lat: 19.9000, lng: 102.1348, label: 'Wat Xieng Thong', num: 2, cat: 'attraction', desc: 'The finest temple in Laos — 1560 AD, mosaic masterpieces' },
        { lat: 19.8924, lng: 102.1353, label: 'Mount Phousi', num: 3, cat: 'attraction', desc: '328 steps to panoramic views over Luang Prabang and the Mekong' },
        { lat: 19.8955, lng: 102.1360, label: 'Royal Palace Museum', num: 4, cat: 'attraction', desc: 'Former royal residence — now museum of Lao royal history' },
        { lat: 19.8870, lng: 102.1377, label: 'Nam Khan Riverside (Hammock Time)', num: 5, cat: 'attraction', desc: 'Perfect spot for reading, hammocks, and watching the river go by' },
        { lat: 19.8860, lng: 102.1382, label: 'Manda de Laos', num: 6, cat: 'food', desc: 'Exquisite Lao dining in a lotus pond heritage villa' }
      ]
    },
    {
      num: 9,
      date: '2026-05-16',
      neighborhoods: 'Luang Prabang · Kuang Si Falls · Ock Pop Tok',
      title: 'Kuang Si Waterfalls & Silk Weaving by the River',
      description: "A perfect final full day — morning at the turquoise pools of Kuang Si Falls (the most beautiful waterfall in Southeast Asia), afternoon at the Ock Pop Tok weaving centre, and one last Luang Prabang evening with silk scarves and sunset cocktails.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuang Si Waterfall',
              description: "Leave early for Kuang Si — 30km south of Luang Prabang, the most spectacular waterfall in Laos. The Mekong's tributary tumbles through limestone terraces into a series of crystalline turquoise pools that look too perfect to be real. Swim in the lower pools, walk the trail to the top falls, and don't forget the sun bear rescue centre at the entrance.",
              details: [
                '🚕 Tuk-tuk from town: ~120,000–150,000 Kip return (negotiate)',
                '⏰ Go early (8am) — the pools are crowded by midday',
                '🏊 Swimming is allowed in the lower pools — the colour is astonishing',
                '🐻 Free the Bears — sun bear rescue centre at the entrance (visit on the way in)',
                '💧 Bring water shoes — the rocks are slippery',
                '⏰ Open 8am–5:30pm · Admission 20,000 Kip'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Kuang Si Waterfall Picnic or Café',
              description: 'There are simple food stalls at the falls entrance. Pack a picnic baguette from town (buy in the morning before departing) to eat by the pools — sublime.',
              meta: '💰 $ · 📍 Kuang Si entrance stalls or bring a picnic'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ock Pop Tok Living Crafts Centre',
              description: "Return to Luang Prabang for a visit to Ock Pop Tok — a fair-trade silk weaving centre run by local women on the banks of the Mekong. Watch weavers at work on traditional looms, see natural dye demonstrations, and browse the beautiful silk and linen collections.",
              details: [
                '🧵 "East Meets West" — the name means where the Mekong meets the world',
                '⏰ Open daily 8am–5pm · Free to enter, tours available',
                '🛍️ Buy directly here — the quality is exceptional and the money goes to weavers',
                '📸 The setting on the Mekong riverbank is itself worth the visit'
              ]
            },
            {
              title: 'Afternoon Reading by the Mekong',
              description: "One more afternoon of deliberate, unscheduled peace. The Mekong café strip near Ock Pop Tok has riverside terraces perfect for a long, slow afternoon of reading, watching the boats, and listening to nothing in particular.",
              details: [
                '☕ Khaiphaen or Utopia Bar for riverside coffee or cocktails',
                '📚 This is your last Luang Prabang reading session — savour it',
                '🌸 Frangipani trees line the riverbank — collect a fallen flower'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Last Night in Luang Prabang — Slow Walk & Farewell Dinner',
              description: "Walk the old town slowly for the last time. Stop at every temple you haven't entered, buy one final thing from the night market, and end with a long dinner. Tomorrow this extraordinary city will be a memory.",
              details: [
                '🌙 Wat Mai by moonlight — hauntingly beautiful',
                '🛍️ Final night market shopping — silk scarves, hand-made paper products, silver rings',
                '🕯️ Candlelit restaurants along Sakkarine Road glow warm and inviting'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'L\'Elephant Restaurant',
              description: 'The grand dame of Luang Prabang dining — a French colonial mansion serving refined Franco-Lao cuisine for over 25 years. Order the laap salad, the Mekong river fish, and the coconut crème brûlée. A worthy farewell.',
              meta: '💰 $$$ · 📍 Ban Vat Nong, Old Town · Reservations strongly recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.7715, lng: 102.0148, label: 'Kuang Si Waterfall', num: 1, cat: 'attraction', desc: 'Turquoise tiered pools and jungle waterfall — swim here' },
        { lat: 19.7720, lng: 102.0150, label: 'Free the Bears — Sun Bear Rescue', num: 2, cat: 'attraction', desc: 'Sun bear rescue sanctuary at Kuang Si entrance' },
        { lat: 19.8852, lng: 102.1374, label: 'Ock Pop Tok Weaving Centre', num: 3, cat: 'attraction', desc: 'Fair-trade silk weaving on the Mekong — buy direct from weavers' },
        { lat: 19.8870, lng: 102.1369, label: 'Utopia Bar — Mekong Terrace', num: 4, cat: 'food', desc: 'Riverside terrace perfect for reading and sunset drinks' },
        { lat: 19.8928, lng: 102.1344, label: 'Luang Prabang Night Market (Final)', num: 5, cat: 'attraction', desc: 'Last night of shopping — silk, silver, and hand-made crafts' },
        { lat: 19.8908, lng: 102.1360, label: "L'Elephant Restaurant", num: 6, cat: 'food', desc: 'Farewell dinner in a French colonial mansion — 25 years of Franco-Lao excellence' }
      ]
    },
    {
      num: 10,
      date: '2026-05-17',
      neighborhoods: 'Luang Prabang · Departure',
      title: 'Last Morning in Luang Prabang — A Final Slow Breakfast',
      description: "A slow, unhurried final morning. One last coffee with a view of the Mekong, a walk through the frangipani-scented streets, and a farewell to one of the world's most quietly perfect places.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Dawn Walk & Morning Meditation',
              description: "Wake with the monks one last time. Walk to the Nam Khan riverside as the mist lifts off the water — it's one of the most peaceful sights in Southeast Asia. If your flight allows, sit by the river for an hour and do nothing but be present.",
              details: [
                '🌅 The bamboo footbridge over the Nam Khan is open in the morning (closed in floods)',
                '🧘 There is nowhere better to sit quietly and reflect',
                '📦 Pack the night before — leave the morning free'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Farewell Breakfast',
              name: 'Croissant d\'Or Boulangerie',
              description: "Luang Prabang's best patisserie — flaky croissants, proper espresso, and pain au chocolat in a beautiful old town townhouse. The perfect final meal.",
              meta: '💰 $ · 📍 Sisavangvong Road, Old Town'
            }
          ]
        },
        {
          label: 'Departure',
          activities: [
            {
              title: 'Transfer to Luang Prabang Airport',
              description: "Luang Prabang International Airport (LPQ) is just 4km from the old town — a short tuk-tuk or taxi ride. Fly direct to Bangkok for onward connections, or take the overnight train to Vientiane if continuing south.",
              details: [
                '✈️ LPQ to BKK: ~1.5 hrs with Lao Airlines or Bangkok Airways',
                '🕐 Allow extra time at the airport — Lao border procedures are slow',
                '🎁 Last chance for duty-free Beerlao and Lao coffee at the airport'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8870, lng: 102.1377, label: 'Nam Khan Riverside — Final Morning', num: 1, cat: 'attraction', desc: 'Misty morning river walk — the most peaceful send-off imaginable' },
        { lat: 19.8880, lng: 102.1360, label: "Croissant d'Or Boulangerie", num: 2, cat: 'food', desc: 'Best patisserie in Luang Prabang — farewell breakfast' },
        { lat: 19.8973, lng: 102.1616, label: 'Luang Prabang Airport (LPQ)', num: 3, cat: 'attraction', desc: 'Departure airport — 4km from old town, 20-min tuk-tuk' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$30–60/night', midrange: '$60–120/night', luxury: '$150–350/night' },
    { category: 'Meals (per couple)', budget: '$15–30/day', midrange: '$40–80/day', luxury: '$100–200/day' },
    { category: 'Transport (per couple)', budget: '$10–20/day', midrange: '$20–50/day', luxury: '$80–150/day (private driver)' },
    { category: 'Activities', budget: '$5–15/day', midrange: '$20–60/day', luxury: '$80–200/day' },
    { category: 'Slow Boat (2 days)', budget: '$22/person (public)', midrange: '$200/person (Luang Say)', luxury: '$400+/person (Luang Say superior)' },
    { category: 'Flights (BKK-CNX or BKK-CEI)', budget: '$30–60/person', midrange: '$60–120/person', luxury: '$200+/person' },
    { category: '10-Day Total (couple)', budget: '$700–1,000', midrange: '$1,200–2,000', luxury: '$3,000–6,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Bangkok: Suvarnabhumi (BKK) is the main international hub', 'Fly Bangkok → Chiang Rai (CEI) ~1.5 hrs, from $30–80 USD (Air Asia, Nok Air)', 'Slow boat: Huay Xai → Pakbeng → Luang Prabang (2 days)', 'Return: Fly Luang Prabang (LPQ) → Bangkok from ~$80 USD'] },
    { title: '🏨 Where to Stay', items: ['Bangkok: Sala Rattanakosin (riverside, near temples), Marriott Sukhumvit (mid-range), Lub d Hostel (budget)', 'Chiang Rai: Wangcome Hotel or Le Méridien Chiang Rai', 'Pakbeng: Luang Say Mekong Lodge (included with cruise) or Santi Guesthouse', 'Luang Prabang: Villa Santi, La Maison Dalabua, or Sayo River Guesthouse'] },
    { title: '🌡️ May Weather', items: ['Bangkok: 32–36°C, very humid, afternoon showers', 'Chiang Rai: 28–33°C, greener and cooler than Bangkok', 'Mekong Slow Boat: 28–32°C, occasional rain, river is high and fast', 'Luang Prabang: 28–32°C, lush and green from early rains, very pleasant evenings'] },
    { title: '💊 Health', items: ['Take malaria prophylaxis — recommended for the slow boat route and Luang Prabang jungle areas', 'Bring travellers diarrhoea medicine — stick to cooked food in rural areas', 'Sunscreen is essential — the Mekong boat has no shade on the sides', 'Hepatitis A and Typhoid vaccinations recommended if not already done'] },
    { title: '📱 Connectivity', items: ['Thailand: AIS or DTAC prepaid SIM — excellent 4G coverage everywhere', 'Laos: Unitel or LTC SIM from the border or Luang Prabang town', 'The slow boat has no wifi — download books, podcasts, and offline maps beforehand', 'Luang Prabang has good wifi at most guesthouses and cafés'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  if (err.stack) console.error(err.stack);
  process.exit(1);
}
