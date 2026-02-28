const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772235277165_iuj295',
  email: 'rodde13@gail.com',
  destination: 'vietnam',
  startDate: '2026-06-08',
  endDate: '2026-06-29',
  groupSize: 2,
  requests: 'Cultural, Foodie, Relaxation, Family-friendly — Mix of everything dining — $2,000–5,000 budget'
};

const itineraryData = {
  destination: 'Vietnam',
  countryEmoji: '🇻🇳',
  title: 'The Full Vietnam Experience',
  subtitle: '21 days of street food, ancient temples, limestone bays & mountain cool for two',
  description: "Vietnam is one of the world's great travel adventures — a country that rewards the curious with extraordinary food, stunning landscapes, and layers of history that span millennia. This south-to-north journey begins in the electric chaos of Ho Chi Minh City, drifts through the misty highlands of Da Lat, lingers in lantern-lit Hoi An, explores imperial Hue, sails the emerald waters of Ha Long Bay, and ends in Hanoi's timeless Old Quarter. For a couple seeking culture, great food, and genuine relaxation, Vietnam delivers everything.",
  duration: '21 nights',
  dates: 'Jun 8 – Jun 29, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Couples · Foodies · Culture Lovers',
  highlights: [
    'Street food tour of Ho Chi Minh City\'s Ben Thanh Market area',
    'Overnight Ha Long Bay cruise through limestone karsts',
    'Lantern-lit evenings in Hoi An Ancient Town',
    'Hue Imperial Citadel and royal tomb cycle tour',
    'Ninh Binh boat tour through rice paddies and caves',
    'Hanoi Old Quarter pho and bia hoi culture',
    'Da Lat highlands: waterfalls, strawberry farms & French colonial villas'
  ],

  essentials: [
    { title: '🌧️ June Weather', text: 'June is the shoulder/rainy season — expect warm temps (28–35°C in south, 25–32°C in Hanoi) with afternoon showers. The north is often clearer; the south is wetter. Pack a light rain jacket. Ha Long Bay is beautiful even with some mist.' },
    { title: '🛵 Getting Around', text: 'Domestic flights connect cities quickly and cheaply (Vietjet, Bamboo, Vietnam Airlines). Book 2–4 weeks ahead. Within cities, Grab (the SE Asian Uber) is essential — safe, metered, and dirt cheap. Motorbike taxis (xe ôm) are fun for short hops.' },
    { title: '💰 Money', text: 'Vietnamese Dong (VND). ATMs are plentiful; withdraw large amounts to avoid fees. Many restaurants and hotels now accept cards. Budget around 500,000–1,000,000 VND (~$20–40 USD) per day per person for food at a mix of street stalls and mid-range restaurants.' },
    { title: '🍜 Food Rules', text: 'Embrace the street food — it\'s often the best and safest. Look for busy stalls with high turnover. Always say "không đá" (no ice) if water safety concerns you, though most tourist ice is purified. Each city has its own noodle dish — pho (Hanoi), bún bò Huế (Hue), cao lầu (Hoi An), bánh mì (everywhere).' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-08',
      neighborhoods: 'Ho Chi Minh City · District 1 · Ben Thanh',
      title: 'Arrive in Saigon — City of Motorbikes & Magic',
      description: 'Touch down in Ho Chi Minh City — the city that never really stops. Check in, get your bearings, and let the energy of Saigon wash over you with a gentle evening stroll and your first bowl of pho.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle In',
              description: 'Tan Son Nhat International Airport (SGN) is 7km from the city center. Grab a Grab car to your hotel in District 1 — the central tourist hub. Rest, freshen up, and gear up for the sensory overload ahead.',
              details: [
                '🚗 Grab car from airport to District 1: ~120,000–180,000 VND (~$5–7)',
                '🏨 Stay in District 1 for walkable access to major sights',
                '💡 Buy a local SIM at the airport (Viettel or Mobifone — ~$5 for 5GB)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Crossing the street in HCMC is an art — walk slowly and steadily, let the motorbikes flow around you. Never stop suddenly. You\'ll have it mastered by day two.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ben Thanh Market & First Wander',
              description: 'Head to Ben Thanh Market at dusk when the night market springs up around it. Browse street food stalls, pick up snacks, and soak up the chaos. Then walk along Nguyen Hue Boulevard — the city\'s pedestrianized "walking street" with light displays.',
              details: [
                '🌆 Nguyen Hue Walking Street is beautiful at night — great first impression',
                '📸 Ho Chi Minh City Hall is lit up beautifully after dark',
                '🛍️ Ben Thanh Night Market runs until midnight'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Pho Hoa Pasteur',
              description: 'A HCMC institution since 1960 — the gold standard for Saigon-style pho. Rich, clear broth, silky rice noodles, and a mountain of fresh herbs. Simple perfection for your first meal.',
              meta: '💰 $ · 📍 260C Pasteur, District 3 · Open until late'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.7769, lng: 106.6980, label: 'Ben Thanh Market', num: 1, cat: 'attraction', desc: 'Iconic Saigon market — night market surrounds it from dusk' },
        { lat: 10.7764, lng: 106.7009, label: 'Nguyen Hue Walking Street', num: 2, cat: 'attraction', desc: 'Pedestrian boulevard with light displays and city hall' },
        { lat: 10.7752, lng: 106.6977, label: 'Pho Hoa Pasteur', num: 3, cat: 'food', desc: 'HCMC pho institution since 1960' }
      ]
    },
    {
      num: 2,
      date: '2026-06-09',
      neighborhoods: 'Ho Chi Minh City · District 1 · District 3',
      title: 'Saigon\'s Soul — War History, Colonial Streets & Street Food',
      description: 'Dive deep into Saigon\'s layered history — from French colonial architecture to the Vietnam War\'s haunting legacy — then lose yourself in the city\'s legendary street food scene.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'War Remnants Museum',
              description: 'One of the most powerful museums in Southeast Asia. Unflinching in its portrayal of the Vietnam War — photographs, military equipment, and exhibits that stay with you. Allow 2 hours. Emotionally heavy but essential viewing.',
              details: [
                '🏛️ 28 Vo Van Tan, District 3 · Open daily 7:30am–6pm',
                '💰 Entry: 40,000 VND (~$1.60)',
                '📸 The rooftop displays military aircraft and tanks',
                '⚠️ Some exhibits are graphic — emotionally prepare'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bánh Mì Huỳnh Hoa',
              description: 'Widely considered Saigon\'s best bánh mì. Loaded with multiple meats, pâté, pickled vegetables, and chili. Queue is worth it — locals line up from early morning.',
              meta: '💰 $ · 📍 26 Le Thi Rieng, District 1 · Opens 6am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Reunification Palace & Notre-Dame Cathedral',
              description: 'Walk through the Reunification Palace — the former South Vietnamese presidential palace, frozen in time since the tanks rolled through its gates on April 30, 1975. Then stroll to the French-built Notre-Dame Cathedral and the Central Post Office — a gorgeous colonial relic designed by Gustave Eiffel\'s team.',
              details: [
                '🏛️ Reunification Palace: 135 Nam Ky Khoi Nghia · Entry 40,000 VND',
                '⛪ Notre-Dame Cathedral closed for renovation — beautiful exterior still worth seeing',
                '📮 Central Post Office: still operational, beautiful interior, great postcards'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Street Food Walking Tour',
              description: 'Join a local street food walking tour around Bui Vien Street and the backpacker district, or explore independently. Sample bún thịt nướng (grilled pork noodles), bánh xèo (sizzling crepes), gỏi cuốn (fresh spring rolls), and wash it down with a 5,000 VND bia hơi (fresh draught beer).',
              details: [
                '🍺 Bui Vien "Walking Street" is HCMC\'s neon-lit party street',
                '🥗 Gỏi cuốn from street carts: 15,000 VND each',
                '🍺 Bia hơi (draft beer) from 5,000 VND (~20 cents) — the world\'s cheapest beer'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cục Gạch Quán',
              description: 'A beloved Saigon restaurant in a converted colonial home with a lush garden. Serves traditional Vietnamese comfort food — broken rice, caramelized fish in clay pots, morning glory stir-fry. The kind of place that feels like eating at a Vietnamese grandmother\'s house.',
              meta: '💰 $$ · 📍 10 Dang Tat, District 1 · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.7793, lng: 106.6926, label: 'War Remnants Museum', num: 1, cat: 'attraction', desc: 'Powerful museum documenting the Vietnam War' },
        { lat: 10.7797, lng: 106.6959, label: 'Reunification Palace', num: 2, cat: 'attraction', desc: 'Historic presidential palace, frozen since 1975' },
        { lat: 10.7799, lng: 106.6990, label: 'Notre-Dame Cathedral', num: 3, cat: 'attraction', desc: 'French colonial cathedral in the city center' },
        { lat: 10.7762, lng: 106.6975, label: 'Bánh Mì Huỳnh Hoa', num: 4, cat: 'food', desc: 'Saigon\'s most famous bánh mì — long queue, worth it' },
        { lat: 10.7697, lng: 106.6975, label: 'Bui Vien Street', num: 5, cat: 'attraction', desc: 'Neon backpacker street — bia hơi and street food' },
        { lat: 10.7841, lng: 106.6893, label: 'Cục Gạch Quán', num: 6, cat: 'food', desc: 'Colonial home restaurant with Vietnamese comfort food' }
      ]
    },
    {
      num: 3,
      date: '2026-06-10',
      neighborhoods: 'Cu Chi · Ho Chi Minh City outskirts',
      title: 'Cu Chi Tunnels & Rooftop Saigon',
      description: 'Venture outside the city to the remarkable Cu Chi Tunnel network, then return for rooftop cocktails and fine Vietnamese dining to close out your Saigon chapter.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cu Chi Tunnels',
              description: 'The Cu Chi tunnel network is one of the most astonishing feats of wartime engineering — 250km of tunnels used by Viet Cong fighters during the Vietnam War. Crawl through narrow passages, see trap doors, and understand the extraordinary resilience of the people who lived underground for years.',
              details: [
                '🚌 Join a half-day tour from HCMC (~$15–20 including transport)',
                '⏰ Leave by 8am to avoid the midday heat',
                '🦟 Wear long sleeves and bring insect repellent',
                '💡 Ben Dinh tunnels are less touristy than Ben Duoc — ask for Ben Dinh'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Return to Saigon & Rest',
              description: 'Back in the city by early afternoon. Rest at the hotel, or explore the colourful Chinatown district (Cholon) — the largest Chinatown in Vietnam, centred around Binh Tay Market and the elaborate Thien Hau Temple.',
              details: [
                '🏯 Thien Hau Temple: 710 Nguyen Trai, District 5 — incense-filled, stunning',
                '🛒 Binh Tay Market: HCMC\'s largest wholesale market, more local than Ben Thanh'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hu Tieu Nam Vang (Phnom Penh Noodle Soup)',
              description: 'In Chinatown, try hu tiếu — the Cambodian-influenced noodle soup that\'s deeply loved in southern Vietnam. Clear pork broth, rice noodles, shrimp, and fresh herbs. Simple, sublime.',
              meta: '💰 $ · 📍 Available at street stalls throughout Cholon'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Saigon Rooftop Farewell',
              description: 'Head up to one of Saigon\'s spectacular rooftop bars for golden hour drinks. Chill Skybar on the 26th floor of the AB Tower offers 360° panoramas over the city. Watch the motorbike rivers below and the city shimmer into evening.',
              details: [
                '🍹 Chill Skybar: Level 26, AB Tower, 76A Le Lai — spectacular views',
                '🌅 Golden hour in HCMC: around 5:30–6pm',
                '📸 The view of the city at sunset is unforgettable'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Deck Saigon',
              description: 'Elegant riverside restaurant on the Saigon River in District 2. Beautiful terrace setting, fusion Vietnamese cuisine, excellent cocktails. A romantic farewell to Saigon.',
              meta: '💰 $$$ · 📍 38 Nguyen U Di, Thao Dien, District 2'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 11.1437, lng: 106.4611, label: 'Cu Chi Tunnels', num: 1, cat: 'attraction', desc: '250km of wartime tunnels — a feat of human endurance' },
        { lat: 10.7567, lng: 106.6548, label: 'Thien Hau Temple', num: 2, cat: 'attraction', desc: 'Beautiful Cantonese temple in Cholon Chinatown' },
        { lat: 10.7559, lng: 106.6538, label: 'Binh Tay Market', num: 3, cat: 'attraction', desc: 'HCMC\'s largest wholesale market in Cholon' },
        { lat: 10.7725, lng: 106.7014, label: 'Chill Skybar', num: 4, cat: 'attraction', desc: '360° rooftop bar — best sunset views in Saigon' },
        { lat: 10.8024, lng: 106.7327, label: 'The Deck Saigon', num: 5, cat: 'food', desc: 'Riverside fusion restaurant with beautiful terrace' }
      ]
    },
    {
      num: 4,
      date: '2026-06-11',
      neighborhoods: 'Mekong Delta · Ben Tre · Can Tho',
      title: 'Mekong Delta — Life on the River',
      description: 'A full-day journey into the Mekong Delta — the "rice bowl" of Vietnam. Glide through canals lined with coconut palms, visit floating markets, sample local sweets, and see a completely different Vietnam.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to the Mekong & Boat Journey Begins',
              description: 'Depart HCMC at 7am on a guided day trip to Ben Tre or My Tho. Board a wooden sampan boat and navigate the narrow canals, stopping at coconut candy workshops, honey bee farms, and a traditional music performance.',
              details: [
                '⏰ Book a guided day tour from HCMC (~$30–50 per person)',
                '🥥 Ben Tre is the "coconut capital" — coconut candy, coconut wine, coconut everything',
                '🎵 Traditional đờn ca tài tử music performance at a local home',
                '🚣 The canals are lush and quiet — poles, not motors, on the smaller waterways'
              ]
            }
          ],
          meals: [
            {
              type: '🍌 Tropical Fruit Tasting',
              name: 'Mekong Orchard Stop',
              description: 'Local orchards along the delta route offer seasonal fruit platters — rambutan, longan, pomelo, jackfruit, and dragon fruit, all grown on-site. Often included in tour packages.',
              meta: '💰 Included in tour · 📍 Ben Tre province orchards'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cai Be Floating Market (optional extension)',
              description: 'If doing a Can Tho extension, the morning floating market at Cai Rang is the largest in the delta. Wholesale boats laden with pineapples, watermelons, and greens. Come by small boat at dawn — it\'s most active 6–9am.',
              details: [
                '🛶 The floating market boats hang samples of their goods from long poles',
                '☕ Buy a coffee from a floating café boat',
                '📸 The colours and chaos of floating trade are extraordinary to photograph'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hủ tiếu mực (Squid noodle soup)',
              description: 'A Mekong Delta speciality — squid-broth noodle soup, lighter and more delicate than Saigon pho. Often eaten from tiny plastic stools at canal-side stalls.',
              meta: '💰 $ · 📍 Ben Tre town eateries along the canal'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to HCMC & Fly to Da Lat',
              description: 'Return to HCMC by late afternoon. If taking an evening flight to Da Lat (Lien Khuong Airport), transfer directly to the airport. The mountain city awaits — pack a light layer, temperatures drop to a refreshing 17–22°C.',
              details: [
                '✈️ HCMC to Da Lat: ~50 min flight (Vietjet, Bamboo)',
                '🌙 Alternatively, take a scenic overnight bus (~7 hours) through the highlands',
                '🏨 Stay in Da Lat city center near Xuan Huong Lake'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.2417, lng: 106.3756, label: 'Ben Tre Province', num: 1, cat: 'attraction', desc: 'Coconut capital of Vietnam — canal boat tours depart here' },
        { lat: 10.0522, lng: 105.7869, label: 'Cai Rang Floating Market', num: 2, cat: 'attraction', desc: 'Vietnam\'s largest floating market — best at dawn' },
        { lat: 10.2600, lng: 106.3800, label: 'Mekong Canal Network', num: 3, cat: 'attraction', desc: 'Narrow palm-lined waterways with traditional life' },
        { lat: 11.9484, lng: 108.4416, label: 'Da Lat City', num: 4, cat: 'attraction', desc: 'Highland city — destination for next 2 days' }
      ]
    },
    {
      num: 5,
      date: '2026-06-12',
      neighborhoods: 'Da Lat · Xuan Huong Lake · French Quarter',
      title: 'Da Lat — The City of Eternal Spring',
      description: 'Da Lat is Vietnam\'s highland escape — a French colonial hill station surrounded by pine forests, flower farms, and misty waterfalls. The cool air and European-flavored architecture make it feel like a completely different country.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Xuan Huong Lake Morning Walk',
              description: 'Start the day with a serene walk around Xuan Huong Lake at the heart of Da Lat. The cool morning air, pine forests, and French-era buildings reflected in the water make it one of Vietnam\'s most romantic settings.',
              details: [
                '🦢 The lake is 5km in circumference — full circle takes about 1 hour',
                '📸 Best reflections in the early morning mist',
                '🌸 The hillsides are covered in flower farms — Da Lat supplies 70% of Vietnam\'s cut flowers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Da Lat Train Café',
              description: 'Breakfast at a cosy café inside or near the old Da Lat train station — a gorgeous French-era building with tiled platforms and vintage locomotives. Weasel coffee (cà phê chồn) is a Da Lat speciality.',
              meta: '💰 $ · 📍 1 Quang Trung, Da Lat'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Crazy House & Da Lat Palace',
              description: 'Visit Hang Nga Guesthouse, nicknamed "Crazy House" — a surrealist architectural fantasia of twisted staircases, cave tunnels, and tree-trunk rooms designed by a Vietnamese architect trained in Moscow. Then walk past the golden Da Lat Palace Hotel, a perfectly preserved French colonial palace.',
              details: [
                '🏠 Crazy House: 3 Huynh Thuc Khang — Entry 60,000 VND',
                '🏨 Da Lat Palace Hotel (Sofitel) is open to walk-ins for afternoon tea',
                '🌲 The pine-tree setting around the Palace is stunning in the mist'
              ]
            },
            {
              title: 'Datanla Waterfall',
              description: 'Take a scenic cable car and Alpine coaster down to Datanla Falls — a lovely multi-tiered waterfall in a cool forest valley. The Alpine coaster (bobsled track) back up is thrillingly fun for couples.',
              details: [
                '⛷️ Alpine coaster: 70,000 VND per ride — genuinely fun',
                '🌊 The falls are surrounded by cool, mossy forest',
                '📍 10 minutes from Da Lat center by motorbike taxi'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Artichoke Hotpot (Lẩu Atiso)',
              description: 'Da Lat\'s signature dish — hotpot made with locally-grown artichoke broth, incredibly healthy and deeply comforting on a cool highland evening. Add mushrooms, tofu, vegetables, and pork.',
              meta: '💰 $$ · 📍 Available at multiple Da Lat Night Market stalls and Da Lat restaurants'
            }
          ],
          activities: [
            {
              title: 'Da Lat Night Market',
              description: 'The Da Lat Night Market along Nguyen Thi Minh Khai Street buzzes every evening from around 5pm. Try stuffed rice cakes (bánh tráng nướng, called "Vietnamese pizza"), strawberry wine, and artichoke tea.',
              details: [
                '🍓 Strawberries grow everywhere in Da Lat — fresh strawberry juice, jam, and wine',
                '🍕 Bánh tráng nướng (grilled rice paper with toppings) is a Da Lat street specialty',
                '🫖 Artichoke tea is earthy and wonderful on a cool evening'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 11.9417, lng: 108.4386, label: 'Xuan Huong Lake', num: 1, cat: 'attraction', desc: 'Heart of Da Lat — morning walk with misty pine reflections' },
        { lat: 11.9335, lng: 108.4254, label: 'Crazy House (Hang Nga)', num: 2, cat: 'attraction', desc: 'Surrealist guesthouse — one of Vietnam\'s most unique buildings' },
        { lat: 11.9494, lng: 108.4330, label: 'Da Lat Palace Hotel', num: 3, cat: 'attraction', desc: 'Perfectly preserved French colonial palace hotel' },
        { lat: 11.9067, lng: 108.4396, label: 'Datanla Waterfall', num: 4, cat: 'attraction', desc: 'Tiered waterfall with Alpine coaster — fun for couples' },
        { lat: 11.9391, lng: 108.4426, label: 'Da Lat Night Market', num: 5, cat: 'food', desc: 'Evening market — strawberry wine, artichoke tea, bánh tráng nướng' }
      ]
    },
    {
      num: 6,
      date: '2026-06-13',
      neighborhoods: 'Da Lat surrounds · Flower Farms · Valley of Love',
      title: 'Da Lat Highlands — Flower Farms, Pine Valleys & French Villas',
      description: 'A lazy day exploring Da Lat\'s romantic countryside — strawberry farms you can pick from, the whimsical Valley of Love, and a cycle or motorbike tour through flower-lined roads to a French Cistercian monastery.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Strawberry Farm Pick-Your-Own',
              description: 'Da Lat\'s strawberry farms let you wander the rows and pick berries straight from the vine. The highland climate makes them intensely sweet — nothing like store-bought. Several farms on Nguyen Thi Nghia street offer this experience.',
              details: [
                '🍓 Most farms open from 7am — early morning light is lovely',
                '💰 Pay per 500g of picked strawberries — very cheap',
                '🌸 Many farms also grow hydrangeas, roses, and lily of the valley'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Peace Café Da Lat',
              description: 'Cosy highland café with excellent Vietnamese egg coffee, avocado smoothies, and bánh cuốn (steamed rice rolls). Warm, wood-panelled atmosphere.',
              meta: '💰 $ · 📍 Da Lat city center'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Valley of Love & Truc Lam Monastery',
              description: 'The Valley of Love (Thung Lũng Tình Yêu) is a pine forest with a lake and gardens north of the city — touristy but genuinely pretty. Then take a cable car to Truc Lam Zen Monastery, serenely situated on a hill above a lake, with beautiful views and gardens.',
              details: [
                '🌺 Valley of Love: expect flower arches, pedalboats, and picnic spots',
                '🛕 Truc Lam Monastery: peaceful Zen Buddhist temple — dress modestly',
                '🚡 Cable car to the monastery: 50,000 VND return'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Bún Bò Huế at a Da Lat Market Stall',
              description: 'Even in Da Lat, the spicy Hue-style beef noodle soup (bún bò Huế) is everywhere. Richer and spicier than Hanoi pho — a perfect midday comfort food.',
              meta: '💰 $ · 📍 Da Lat central market food stalls'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Fly to Hoi An (via Da Nang)',
              description: 'Early evening flight from Da Lat (LKE) to Da Nang (DAD), then a 30-minute taxi south to Hoi An. Arrive in the lantern city just in time for a first magical evening stroll.',
              details: [
                '✈️ Da Lat to Da Nang: ~1 hour flight',
                '🚕 Da Nang airport to Hoi An: ~30–40 min taxi (~250,000 VND)',
                '🏨 Stay in or very near Hoi An Ancient Town'
              ]
            }
          ],
          meals: [
            {
              type: '🏮 Late Dinner',
              name: 'White Rose Dumplings (Bánh Bao Vạc)',
              description: 'Arrive in Hoi An and head straight for a plate of White Rose dumplings — shrimp-filled translucent dumplings unique to Hoi An. Available only from a single family who supplies all restaurants in town.',
              meta: '💰 $ · 📍 Any restaurant in Hoi An Ancient Town'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 11.9667, lng: 108.4350, label: 'Strawberry Farms', num: 1, cat: 'attraction', desc: 'Pick-your-own strawberry farms in the Da Lat highlands' },
        { lat: 11.9694, lng: 108.4299, label: 'Valley of Love', num: 2, cat: 'attraction', desc: 'Pine forest valley with lake and gardens' },
        { lat: 11.8975, lng: 108.3900, label: 'Truc Lam Monastery', num: 3, cat: 'attraction', desc: 'Zen Buddhist monastery above Tuyen Lam Lake' },
        { lat: 15.9000, lng: 108.3200, label: 'Hoi An Ancient Town', num: 4, cat: 'attraction', desc: 'Tonight\'s destination — lantern-lit ancient trading port' }
      ]
    },
    {
      num: 7,
      date: '2026-06-14',
      neighborhoods: 'Hoi An Ancient Town · Japanese Bridge · Thu Bon River',
      title: 'Hoi An — Lanterns, Ancient Streets & Morning Markets',
      description: 'Hoi An is one of Southeast Asia\'s most beautiful towns — a UNESCO World Heritage site of yellow-walled merchant houses, silk lanterns, and a river that glows with colour at night. Morning is the best time to explore.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ancient Town Early Morning Walk',
              description: 'Wake before 7am and walk the Ancient Town streets while they\'re quiet — just locals setting up stalls, monks walking to temple, and the golden morning light on those famous yellow walls. Visit the Japanese Covered Bridge (the symbol of Hoi An) and the Assembly Halls of the Chinese trading clans.',
              details: [
                '🌅 6–8am is magical — before the tourists and the heat arrive',
                '🌉 Japanese Covered Bridge: cross into the Japanese quarter — lovely wooden arch',
                '🏛️ Phuc Kien Assembly Hall: ornate Chinese Fujian merchant hall, gorgeous interior',
                '💰 Ancient Town entry ticket: 120,000 VND — valid for multiple sites'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Cao Lầu at Trung Bắc',
              description: 'Cao lầu is the noodle dish unique to Hoi An — thick, chewy noodles made with water from a specific local well, topped with char siu pork, crispy rice crackers, and herbs. Unmissable.',
              meta: '💰 $ · 📍 87 Tran Phu, Ancient Town'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hoi An Central Market & Cooking Class',
              description: 'Visit Hoi An\'s riverside market to see the incredible produce — river herbs, morning glory, galangal, lemongrass — then join a half-day cooking class. Learn to make White Rose dumplings, cao lầu, and fresh spring rolls. Most classes include a market tour and are fantastic fun as a couple.',
              details: [
                '👨‍🍳 Recommended: Red Bridge Cooking School or Morning Glory Cooking Class',
                '💰 Cooking class: ~$30–40 per person including market tour',
                '🌿 The market herb section alone is worth a visit — extraordinary variety'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lantern Release on the Thu Bon River',
              description: 'At dusk, the Thu Bon River transforms into a river of light as hundreds of coloured lanterns float downstream. Buy a paper lotus lantern (20,000 VND), make a wish, and set it afloat. The reflections of the ancient buildings in the lantern-lit river are extraordinarily beautiful.',
              details: [
                '🏮 Lanterns are sold at the riverbank — best spot is opposite the Japanese Bridge',
                '🌙 Full moon nights (around the 14th of each lunar month) are especially magical',
                '📸 This is one of the most photogenic moments in all of Vietnam'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Morning Glory Restaurant',
              description: 'The most celebrated restaurant in Hoi An — run by celebrity chef Ms. Vy. Beautifully presented Vietnamese dishes from across the country, in a gorgeous old-house setting on Tran Phu.',
              meta: '💰 $$ · 📍 106 Nguyen Thai Hoc, Ancient Town · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8773, lng: 108.3261, label: 'Japanese Covered Bridge', num: 1, cat: 'attraction', desc: 'Symbol of Hoi An — 18th century wooden bridge' },
        { lat: 15.8761, lng: 108.3270, label: 'Phuc Kien Assembly Hall', num: 2, cat: 'attraction', desc: 'Ornate Chinese Fujian merchants\' assembly hall' },
        { lat: 15.8769, lng: 108.3282, label: 'Hoi An Market', num: 3, cat: 'food', desc: 'Riverside market with incredible herbs and produce' },
        { lat: 15.8769, lng: 108.3243, label: 'Thu Bon River', num: 4, cat: 'attraction', desc: 'River of lanterns at dusk — release paper lotus lanterns' },
        { lat: 15.8777, lng: 108.3262, label: 'Morning Glory Restaurant', num: 5, cat: 'food', desc: 'Hoi An\'s most celebrated restaurant — Ms. Vy\'s kitchen' }
      ]
    },
    {
      num: 8,
      date: '2026-06-15',
      neighborhoods: 'Hoi An · An Bang Beach · Cam Kim Island',
      title: 'Hoi An Beach Day & Island Escape',
      description: 'Balance the cultural intensity with a perfect beach day at An Bang — a quiet stretch of sand just 3km from the Ancient Town. Then island-hop to Cam Kim for a bicycle tour through rice paddies and a family-run craft workshop.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'An Bang Beach',
              description: 'Bicycle or grab a scooter taxi to An Bang Beach — the most laid-back stretch of coast near Hoi An. Gentle waves, beach bars with sunbeds, fresh seafood shacks, and a local fishing village atmosphere. A beautiful morning of doing absolutely nothing.',
              details: [
                '🚲 Bicycle rentals from Hoi An: ~40,000 VND/day — the road is pleasant',
                '🏖️ An Bang is calmer and more local than Cua Dai Beach',
                '☀️ June mornings are bright — arrive early before the midday heat'
              ]
            }
          ],
          meals: [
            {
              type: '🦐 Brunch',
              name: 'Soul Kitchen An Bang Beach',
              description: 'Beloved beachside restaurant with creative Vietnamese dishes, fresh seafood, and excellent smoothies. Sunbeds and a relaxed vibe — a great place to linger for hours.',
              meta: '💰 $$ · 📍 An Bang Beach, Hoi An'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cam Kim Island Bicycle Tour',
              description: 'Cross to Cam Kim Island by small ferry and rent bicycles to explore. The island has virtually no cars — just rice paddies, vegetable gardens, and traditional craft workshops making Hoi An\'s famous wooden boats and furniture. A wonderfully peaceful escape.',
              details: [
                '⛵ Small ferry from Bach Dang pier: 20,000 VND each way',
                '🚲 Bicycle around the island takes about 2 hours at a leisurely pace',
                '🛶 Watch local craftsmen building traditional wooden fishing boats'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tailor Shop Experience',
              description: 'Hoi An is famous for bespoke tailoring — 24-hour made-to-measure clothing at remarkable prices. Visit a reputable tailor on Tran Phu (A Dong Silk or Yaly Couture) and commission shirts, dresses, or suits. Measurements today, fitting tomorrow morning.',
              details: [
                '👗 Yaly Couture: 358 Nguyen Duy Hieu — highest quality, slightly pricier',
                '👔 A shirt tailored in 24 hours: ~$25–40 USD in excellent fabric',
                '🎁 Tailored linen clothing makes excellent trip souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Field Restaurant',
              description: 'Farm-to-table Vietnamese dining in a gorgeous rice paddy setting just outside Hoi An. You eat surrounded by actual paddy fields with fairy lights — extraordinarily romantic.',
              meta: '💰 $$$ · 📍 3km from Ancient Town — take a Grab'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.9033, lng: 108.3567, label: 'An Bang Beach', num: 1, cat: 'attraction', desc: 'Quiet local beach 3km from the Ancient Town' },
        { lat: 15.8742, lng: 108.3141, label: 'Cam Kim Island', num: 2, cat: 'attraction', desc: 'Car-free island with boat builders and rice paddies' },
        { lat: 15.8764, lng: 108.3279, label: 'Tailor Row (Tran Phu)', num: 3, cat: 'attraction', desc: '24-hour bespoke tailoring — Hoi An\'s famous craft' },
        { lat: 15.8637, lng: 108.3015, label: 'The Field Restaurant', num: 4, cat: 'food', desc: 'Romantic farm-to-table dining in actual rice paddies' }
      ]
    },
    {
      num: 9,
      date: '2026-06-16',
      neighborhoods: 'Hoi An · My Son Sanctuary',
      title: 'My Son Hindu Sanctuary & Farewell to Hoi An',
      description: 'Take a morning excursion to My Son — the ancient Cham Hindu temple complex hidden in a jungle valley. Return to Hoi An for a final afternoon of shopping and silk lanterns before heading north to Hue.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'My Son Cham Sanctuary',
              description: 'My Son is one of Southeast Asia\'s most important archaeological sites — a collection of 4th–13th century Hindu temples built by the Cham kingdom. Set in a mysterious, forested valley 70km from Hoi An. The brick towers draped in jungle vegetation rival Angkor Wat in atmosphere.',
              details: [
                '🏛️ UNESCO World Heritage Site — Cham civilisation at its peak',
                '⏰ Go early (7am departure) to beat the heat and tour groups',
                '🚌 Half-day tours from Hoi An: ~$10–15 per person',
                '🎭 Optional: Cham dance performance at the site (45 min, atmospheric)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Hoi An Afternoon — Lantern Shopping & Fitting',
              description: 'Back in Hoi An by early afternoon. Pick up your tailored clothing, browse the silk lantern shops (many sell beautiful handmade lanterns to pack flat), and have one last wander through the Ancient Town streets.',
              details: [
                '🏮 Silk lanterns: buy flat-packed styles for easy transport',
                '🧵 Collect your tailored items — final fitting and adjustments',
                '🍵 One last Vietnamese iced coffee at a riverside café — bánh mì on the side'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Bánh Mì Phương',
              description: 'Anthony Bourdain called it "the best bánh mì in Vietnam." Queue for 20 minutes, receive the most perfect bánh mì of your life. Crispy baguette, pâté, multiple meats, pickled carrot, and house sauce.',
              meta: '💰 $ · 📍 2B Phan Chau Trinh, Ancient Town · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Train to Hue on the Reunification Express',
              description: 'Board the Reunification Express train from Da Nang station (30min taxi from Hoi An) for the scenic 2.5-hour journey to Hue. The coastal section past Lang Co lagoon is one of the most spectacular train rides in Vietnam.',
              details: [
                '🚂 Book soft-seat tickets: ~$8–12 per person on the Reunification Express',
                '🌊 The train hugs the coast through Hai Van Pass — bring a camera',
                '🏨 Arrive in Hue by evening — stay near the Imperial Citadel'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.7717, lng: 108.1234, label: 'My Son Sanctuary', num: 1, cat: 'attraction', desc: 'Ancient Cham Hindu temples in a jungle valley — UNESCO site' },
        { lat: 15.8804, lng: 108.3265, label: 'Bánh Mì Phương', num: 2, cat: 'food', desc: 'Bourdain\'s "best bánh mì in Vietnam"' },
        { lat: 16.0471, lng: 108.2062, label: 'Da Nang Train Station', num: 3, cat: 'attraction', desc: 'Departure point for the scenic Reunification Express to Hue' },
        { lat: 16.4637, lng: 107.5909, label: 'Hue City', num: 4, cat: 'attraction', desc: 'Imperial capital — tonight\'s destination' }
      ]
    },
    {
      num: 10,
      date: '2026-06-17',
      neighborhoods: 'Hue · Imperial Citadel · Perfume River',
      title: 'Hue — Imperial Grandeur on the Perfume River',
      description: 'Hue was the seat of Vietnam\'s last imperial dynasty. The walled Citadel, the Forbidden Purple City within it, and the royal tombs scattered across the hills around the Perfume River make this one of Vietnam\'s most culturally rich cities.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hue Imperial Citadel & Forbidden City',
              description: 'Explore the massive Imperial Citadel — a 10km walled compound modelled on Beijing\'s Forbidden City. Inside, the Dai Noi (Inner Imperial City) contains the Forbidden Purple City, throne rooms, temples, and royal gardens. Allow 3–4 hours.',
              details: [
                '🏯 Citadel entry: 200,000 VND (covers the Citadel and most inner buildings)',
                '👑 Thai Hoa Palace — the throne hall is magnificent',
                '🌺 The royal gardens (Truong Du) are especially beautiful in early morning',
                '📸 The Ngo Mon Gate (Noon Gate) is the most iconic shot in Hue'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Bún Bò Huế — The Original',
              description: 'In Hue, bún bò Huế — the city\'s signature spicy beef noodle soup — is a completely different experience from the watered-down versions elsewhere. Rich, lemongrass-scented, complex, and fiery. Start the morning right.',
              meta: '💰 $ · 📍 Quán Bún Bò Huế, 17 Ly Thuong Kiet'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dragon Boat on the Perfume River',
              description: 'Board a traditional dragon boat for a leisurely cruise along the Perfume River. Stop at Thien Mu Pagoda — a seven-tiered tower that is Hue\'s most iconic landmark. The view from the pagoda grounds looking down at the river bend is spectacular.',
              details: [
                '⛵ Dragon boat cruise: ~$8–15 per boat (share with others or take private)',
                '🛕 Thien Mu Pagoda: free to enter, serene grounds, river views',
                '🌿 The river is lined with lotus flowers and fishing boats in June'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hue Royal Cuisine at Tinh Gia Vien',
              description: 'Experience royal Hue cuisine — dishes that were once served to emperors. Beautifully presented small plates, often vegetarian or with delicate flavours. Served in a traditional house with live nhã nhạc (imperial court music).',
              meta: '💰 $$$ · 📍 7 Le Thanh Ton, Hue'
            }
          ],
          tips: [
            { type: 'tip', text: 'Hue cuisine is considered the most sophisticated in Vietnam — more complex and refined than southern or northern food. Look for dishes like banh loc (tapioca dumplings), banh khoai (Hue crispy crepe), and che hue (sweet dessert soups).' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.4698, lng: 107.5796, label: 'Imperial Citadel', num: 1, cat: 'attraction', desc: 'Massive walled imperial compound — Vietnam\'s Forbidden City' },
        { lat: 16.4631, lng: 107.5783, label: 'Ngo Mon Gate', num: 2, cat: 'attraction', desc: 'Iconic Noon Gate — most photographed in Hue' },
        { lat: 16.4524, lng: 107.5443, label: 'Thien Mu Pagoda', num: 3, cat: 'attraction', desc: 'Seven-tiered tower on the Perfume River — Hue\'s symbol' },
        { lat: 16.4700, lng: 107.5800, label: 'Tinh Gia Vien Restaurant', num: 4, cat: 'food', desc: 'Royal Hue cuisine with imperial court music' }
      ]
    },
    {
      num: 11,
      date: '2026-06-18',
      neighborhoods: 'Hue · Royal Tombs · Tu Duc · Minh Mang',
      title: 'Hue Royal Tombs by Bicycle',
      description: 'Hue\'s royal tombs are scattered in the hills south of the city along the Perfume River — each one a unique architectural masterpiece. Cycling through the countryside between them is a perfect day.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tu Duc Royal Tomb',
              description: 'The largest and most elaborate of the Nguyen dynasty tombs — a complex of pavilions, lakes, and pine forests. Emperor Tu Duc spent years here writing poetry and contemplating his reign. The lotus-covered lake and forest paths are extraordinarily peaceful.',
              details: [
                '🌿 155,000 VND entry — largest of the royal tombs',
                '🦢 The lake is covered in lotus flowers in June',
                '📸 The Xung Khiem Pavilion over the water is endlessly photogenic',
                '🚲 Rent bicycles in Hue (~50,000 VND/day) — the route is flat and pleasant'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bánh Cuốn at a Local Hue Stall',
              description: 'Steamed rice rolls with minced pork and wood-ear mushrooms, served with a clear dipping broth. The Hue version is slightly different from Hanoi — lighter and more delicate.',
              meta: '💰 $ · 📍 Local stalls near the citadel'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Minh Mang Tomb & Country Road Cycle',
              description: 'Cycle through rice paddies and rural villages to Emperor Minh Mang\'s tomb — more formal and grand than Tu Duc, with a processional approach through three honour courtyards. The lakeside setting with stone bridges and ancient pines is magnificent.',
              details: [
                '🌾 The cycle route through the countryside takes you past local farms and villages',
                '🏯 Minh Mang tomb: 155,000 VND — the most geometrically perfect of the tombs',
                '🌊 The tomb is set on a peninsula surrounded by lakes — very photogenic'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dong Ba Market & Hue Night Life',
              description: 'Explore Hue\'s largest market — Dong Ba — for evening street food browsing. Then head to Pham Ngu Lao Street for craft beer and live music at one of Hue\'s small bars. The city has a slower, more refined energy than Saigon.',
              details: [
                '🛒 Dong Ba Market: Tran Hung Dao — street food on the river bank',
                '🍺 DMZ Bar: 60 Le Loi — popular spot with live music and local craft beers',
                '🌊 The Perfume River at night is beautifully lit from the Trang Tien Bridge'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Lac Thien Restaurant',
              description: 'A Hue institution run by a deaf family — the warmest, most charming dining experience in the city. Order banh khoai (crispy sizzling crepes with shrimp and pork) and wash it down with the famous local Huda beer.',
              meta: '💰 $ · 📍 6 Dinh Tien Hoang, Hue'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.4050, lng: 107.5525, label: 'Tu Duc Royal Tomb', num: 1, cat: 'attraction', desc: 'Most elaborate royal tomb — lakes, lotus, pavilions' },
        { lat: 16.3858, lng: 107.5487, label: 'Minh Mang Tomb', num: 2, cat: 'attraction', desc: 'Grand processional tomb on a peninsula surrounded by lakes' },
        { lat: 16.4765, lng: 107.5985, label: 'Dong Ba Market', num: 3, cat: 'food', desc: 'Hue\'s largest market with riverside street food' },
        { lat: 16.4727, lng: 107.5895, label: 'Trang Tien Bridge', num: 4, cat: 'attraction', desc: 'Beautiful lit bridge over the Perfume River at night' },
        { lat: 16.4742, lng: 107.5862, label: 'Lac Thien Restaurant', num: 5, cat: 'food', desc: 'Family-run institution — best banh khoai in Hue' }
      ]
    },
    {
      num: 12,
      date: '2026-06-19',
      neighborhoods: 'Hue · Hai Van Pass · Da Nang · Marble Mountains',
      title: 'The Hai Van Pass & Marble Mountains',
      description: 'One of Vietnam\'s great drives — over the spectacular Hai Van Pass (Cloud Pass) by motorbike or car, then down to Da Nang\'s coast. Stop at the extraordinary Marble Mountains before settling into the beach city.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive the Hai Van Pass',
              description: 'The Hai Van Pass (496m) is one of the most spectacular coastal mountain roads in Vietnam — the peninsula divides the climate zones of north and south. Drive or ride over the pass for panoramic views of Lang Co lagoon below and the Da Nang coastline ahead.',
              details: [
                '🏍️ Hire a motorbike guide or private car with driver for the pass (~$40–60)',
                '📸 Multiple viewpoints along the pass — Lang Co lagoon is stunning',
                '⚠️ June can bring mist on the pass — still atmospheric, sometimes clearer by midday',
                '🚂 Note: The train passes through a tunnel, missing the view — take road transport'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Marble Mountains (Ngũ Hành Sơn)',
              description: 'Five marble and limestone hills rising dramatically from the coastal plain south of Da Nang. Climb Thuy Son (the tallest) for panoramic views, explore the Huyen Khong cave with its natural skylight, and visit ancient Buddhist and Hindu shrines carved into the rock face.',
              details: [
                '🗻 Entry: 40,000 VND — worth it, very atmospheric',
                '🔦 The cave shrines inside the mountain are extraordinary — bring a small torch',
                '⛩️ Am Phu Cave is an elaborate Buddhist depiction of heaven and hell',
                '🎨 The surrounding village specializes in marble carving — workshop visits possible'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Mì Quảng (Da Nang Turmeric Noodles)',
              description: 'Da Nang\'s signature dish — turmeric-yellow noodles in a small amount of rich broth with shrimp, pork, quail egg, crushed peanuts, and fresh herbs. Lighter than pho but wonderfully complex.',
              meta: '💰 $ · 📍 Local restaurants in Da Nang city'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'My Khe Beach Sunset & Dragon Bridge',
              description: 'Settle in Da Nang and head to My Khe Beach for a sunset walk. Then cross the Han River to see the famous Dragon Bridge — a fire-breathing dragon sculpture spanning the river that breathes actual fire and water on weekend evenings.',
              details: [
                '🐉 Dragon Bridge fire show: Saturdays and Sundays, 9pm',
                '🏖️ My Khe Beach stretches for 30km — clean, wide, and beautiful',
                '🌉 The Han River bridges are beautifully lit at night'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Dinner',
              name: 'Seafood on My Khe Beach',
              description: 'My Khe Beach is lined with open-air seafood restaurants where you choose your catch from tanks. Tiger prawns, clams, crab, and sea bass, grilled at your table. Extraordinarily fresh and affordable.',
              meta: '💰 $$ · 📍 Restaurant row along My Khe Beach, Da Nang'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.2046, lng: 108.0667, label: 'Hai Van Pass Summit', num: 1, cat: 'attraction', desc: 'Spectacular Cloud Pass with views over Lang Co lagoon' },
        { lat: 15.9736, lng: 108.2634, label: 'Marble Mountains', num: 2, cat: 'attraction', desc: 'Five limestone hills with ancient caves and Buddhist shrines' },
        { lat: 16.0543, lng: 108.2475, label: 'My Khe Beach', num: 3, cat: 'attraction', desc: '30km of pristine beach — Da Nang\'s main coastline' },
        { lat: 16.0612, lng: 108.2275, label: 'Dragon Bridge', num: 4, cat: 'attraction', desc: 'Fire-breathing dragon bridge — spectacular on weekend nights' }
      ]
    },
    {
      num: 13,
      date: '2026-06-20',
      neighborhoods: 'Da Nang · Ba Na Hills',
      title: 'Da Nang Rest Day & Ba Na Hills',
      description: 'A lighter day — morning beach relaxation, then an afternoon ascent to Ba Na Hills via the world\'s longest non-stop single-track cable car, visiting the famous Golden Bridge held aloft by giant stone hands.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'My Khe Beach Morning',
              description: 'A slow morning on one of Vietnam\'s most beautiful urban beaches. Swim, rent a sunbed, or simply walk the long stretch of sand. The water is warm and gentle in June — perfect for a relaxed swim.',
              details: [
                '🏄 Surf rentals available — the waves are gentle and good for beginners',
                '🏊 The beach is very long — walk north toward the quieter sections',
                '☕ Beachside cafés serve excellent Vietnamese iced coffee from 6am'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Cà Phê Trứng (Egg Coffee)',
              description: 'Vietnamese egg coffee — whipped egg yolk foam over strong Vietnamese coffee. Rich, sweet, and completely unique. Originated in Hanoi but beloved across the country.',
              meta: '💰 $ · 📍 Any good Da Nang café'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ba Na Hills & The Golden Bridge',
              description: 'Take the world\'s longest (and most spectacular) non-stop cable car — 5,801 metres — up to Ba Na Hills, a French colonial hill station at 1,487m altitude. The centrepiece is the Golden Bridge, an Instagram-famous footbridge held aloft by giant stone hands. The hilltop is consistently misty and dramatically beautiful.',
              details: [
                '🚡 Cable car includes return — round trip takes about 1.5 hours with the ride',
                '🌉 Golden Bridge is about 150m long — the views on a clear day are extraordinary',
                '🌡️ Temperature at the top is 10°C cooler than the coast — bring a layer',
                '💰 Full day ticket (cable car + all attractions): ~750,000 VND per person'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Madame Lân Restaurant',
              description: 'Da Nang\'s most beloved traditional Vietnamese restaurant, in a gorgeous French colonial building. Extensive menu of Vietnamese classics — bánh xèo, white rose, grilled pork vermicelli. The setting is beautiful.',
              meta: '💰 $$ · 📍 4 Bach Dang, Da Nang'
            }
          ],
          tips: [
            { type: 'tip', text: 'From Da Nang, fly to Hanoi (1h15min) the following morning to begin the northern section. Book your domestic flight ahead — Vietjet and Bamboo connect Da Nang to Hanoi directly.' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0543, lng: 108.2475, label: 'My Khe Beach', num: 1, cat: 'attraction', desc: 'Morning beach time — swim, sunbed, and iced coffee' },
        { lat: 15.9972, lng: 107.9891, label: 'Ba Na Hills', num: 2, cat: 'attraction', desc: 'Mountain resort with world\'s longest cable car and Golden Bridge' },
        { lat: 15.9990, lng: 107.9917, label: 'Golden Bridge', num: 3, cat: 'attraction', desc: 'Instagram-famous bridge held by giant stone hands' },
        { lat: 16.0600, lng: 108.2250, label: 'Madame Lân Restaurant', num: 4, cat: 'food', desc: 'Da Nang\'s best traditional Vietnamese restaurant' }
      ]
    },
    {
      num: 14,
      date: '2026-06-21',
      neighborhoods: 'Hanoi · Hoan Kiem Lake · Old Quarter',
      title: 'Arrive in Hanoi — The Ancient Capital',
      description: 'Fly to Hanoi and discover a city utterly different from Saigon — slower, cooler, more French, more traditional. The Old Quarter\'s 36 guild streets are a UNESCO-recognised time capsule, and Hoan Kiem Lake at its heart is the soul of the city.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Morning Flight Da Nang to Hanoi',
              description: 'Early morning domestic flight (1h15min) from Da Nang to Noi Bai International Airport, Hanoi. The capital awaits — cooler, more French, deeply historical.',
              details: [
                '✈️ Noi Bai Airport is 35km north of the city center',
                '🚌 Airport bus 86: 45 min to Old Quarter, 35,000 VND — very efficient',
                '🚕 Grab car: ~250,000 VND, about 45 minutes to 1 hour depending on traffic'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hoan Kiem Lake & Ngoc Son Temple',
              description: 'The spiritual heart of Hanoi — a jade-green lake in the center of the Old Quarter, said to be where a magical turtle returned a sacred sword to the gods. Walk the shaded promenade, cross the red wooden Huc Bridge to Ngoc Son Temple on its tiny island.',
              details: [
                '🐢 The lake is home to a rare giant softshell turtle — a living legend of Hanoi',
                '⛩️ Ngoc Son Temple: 30,000 VND — serene island setting',
                '📸 The Huc Bridge (red lacquer arch) is one of Hanoi\'s most recognisable sights'
              ]
            },
            {
              title: 'Old Quarter Walking Tour',
              description: 'Wander the 36 guild streets of the Old Quarter — each originally dedicated to a specific trade. Hang Gai (silk), Hang Ma (paper offerings), Hang Bac (silver), Hang Dao (dye). Medieval guild system, ancient shop-houses, and streetlife everywhere.',
              details: [
                '🗺️ Each "Hang" street translates to its guild — Hang means "goods"',
                '🏛️ Bach Ma Temple: 76 Hang Buom — one of Hanoi\'s four sacred guardian temples',
                '☕ Take a break at a pavement coffee stall — tiny stools, brilliant views'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Bun Cha Huong Lien — "Obama\'s Bún Chả"',
              description: 'The exact restaurant where Anthony Bourdain and Barack Obama ate bún chả in 2016 — chargrilled pork patties in dipping broth with cold vermicelli noodles. One of Hanoi\'s great dishes in its most famous setting.',
              meta: '💰 $ · 📍 24 Le Van Huu — they preserved the table where Bourdain and Obama sat'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Bia Hơi Corner & Old Quarter Night',
              description: 'Join the legend of Bia Hơi Junction — the intersection of Hang Gai and Luong Ngoc Quyen where locals and travellers crowd plastic stools for 5,000 VND fresh draft beer every evening. The Old Quarter at night, lit by street lamps and motorbike headlights, is pure Hanoi magic.',
              details: [
                '🍺 Bia hơi (fresh draught beer) brewed daily and sold out by midnight',
                '🌙 The Old Quarter streets close to traffic after dark on weekends',
                '🎶 Traditional ca trù music sometimes performed in the Old Quarter squares'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Chả Cá Lã Vọng',
              description: 'Hanoi\'s most iconic restaurant — serving only one dish for 150+ years. Chả cá: turmeric-marinated catfish, sizzling in butter with dill and spring onions at your table. Serve over noodles with peanuts and shrimp paste. Utterly memorable.',
              meta: '💰 $$$ · 📍 14 Cha Ca, Hoan Kiem · Only one dish on the menu — chả cá'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0285, lng: 105.8542, label: 'Hoan Kiem Lake', num: 1, cat: 'attraction', desc: 'Sacred turtle lake — heart of Hanoi' },
        { lat: 21.0291, lng: 105.8567, label: 'Ngoc Son Temple', num: 2, cat: 'attraction', desc: 'Island temple on Hoan Kiem Lake — cross the red Huc Bridge' },
        { lat: 21.0333, lng: 105.8484, label: 'Hanoi Old Quarter', num: 3, cat: 'attraction', desc: '36 ancient guild streets — medieval trading city' },
        { lat: 21.0226, lng: 105.8498, label: 'Bun Cha Huong Lien', num: 4, cat: 'food', desc: 'Obama & Bourdain\'s bún chả restaurant' },
        { lat: 21.0354, lng: 105.8488, label: 'Bia Hơi Junction', num: 5, cat: 'food', desc: '5,000 VND fresh beer at plastic stools — Hanoi institution' },
        { lat: 21.0300, lng: 105.8498, label: 'Chả Cá Lã Vọng', num: 6, cat: 'food', desc: '150-year-old restaurant serving only one dish' }
      ]
    },
    {
      num: 15,
      date: '2026-06-22',
      neighborhoods: 'Hanoi · Ba Dinh · Tay Ho (West Lake)',
      title: 'Hanoi Deep Dive — Ho Chi Minh Mausoleum, Temples & Temple of Literature',
      description: 'A day of Hanoi\'s grand historical sights — the somber Ho Chi Minh Mausoleum complex, the ancient one-pillar pagoda, the 1,000-year-old Temple of Literature, and the serene lakeside village of Tay Ho.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ho Chi Minh Mausoleum Complex',
              description: 'Visit the grand mausoleum where Ho Chi Minh\'s embalmed body lies in state. The square has a solemn military atmosphere, and queues move quietly past in reverence. The Presidential Palace gardens and Ho Chi Minh\'s simple stilt house within the compound are also open to visitors.',
              details: [
                '⏰ Opens 8am, closed Mon & Fri, and for parts of autumn for maintenance',
                '👗 Strict dress code — no shorts or bare shoulders',
                '🏡 Ho Chi Minh\'s stilt house: a surprisingly modest wooden home',
                '🏛️ The One Pillar Pagoda (Chua Mot Cot) is nearby — a lotus flower rising from a lake'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Pho Thin',
              description: 'The most famous pho in Hanoi — Pho Thin on Lo Duc Street, famous for its beef pho where the noodles and broth are subtly different from every other bowl you\'ll have. Clear, clean broth and no herbs — pure Hanoi style.',
              meta: '💰 $ · 📍 13 Lo Duc — queue from 6am, opens early'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Temple of Literature (Van Mieu)',
              description: 'Vietnam\'s first national university, founded in 1070 — a beautiful complex of traditional Vietnamese architecture set around landscaped courtyards and turtle stelae bearing the names of doctoral graduates. Peaceful, beautiful, and one of Hanoi\'s most loved sites.',
              details: [
                '🏛️ Entry: 30,000 VND — absolutely worth it',
                '📚 The stone turtles in the third courtyard bear doctoral graduates\' names from the 15th century onwards',
                '🌺 The third courtyard is especially lovely — traditional architecture at its finest'
              ]
            },
            {
              title: 'Tay Ho (West Lake) & Tran Quoc Pagoda',
              description: 'Head to Tay Ho — Hanoi\'s largest lake in the northwest. Walk the western shoreline to Tran Quoc Pagoda, the oldest Buddhist temple in Hanoi (6th century), built on a small island in the lake. The lakeside road is lined with shrimp paste and lotus rice cafés.',
              details: [
                '🌸 Tran Quoc Pagoda is reached by a causeway — serene and beautiful',
                '🦐 Banh tom (shrimp fritters) are a Tay Ho speciality — buy from lakeside vendors',
                '🌅 Tay Ho is also the hub of Hanoi\'s expat café scene'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '☕ Afternoon Tea',
              name: 'Egg Coffee at Café Giang',
              description: 'The original egg coffee — Café Giang invented cà phê trứng in 1946 when milk was scarce and the owner substituted whipped egg yolk. A tiny café down an alley off Hang Gai, serving the most famous cup in Vietnam.',
              meta: '💰 $ · 📍 39 Nguyen Huu Huan, alley on the right'
            },
            {
              type: '🍽️ Dinner',
              name: 'La Badiane',
              description: 'Hanoi\'s finest French-Vietnamese restaurant, in a beautifully restored colonial villa with garden seating. The tasting menu blends French technique with Vietnamese flavours — an elegant and romantic evening.',
              meta: '💰 $$$$ · 📍 10 Nam Ngu, Hoan Kiem · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0367, lng: 105.8344, label: 'Ho Chi Minh Mausoleum', num: 1, cat: 'attraction', desc: 'Solemn mausoleum where Ho Chi Minh lies in state' },
        { lat: 21.0354, lng: 105.8357, label: 'One Pillar Pagoda', num: 2, cat: 'attraction', desc: 'Lotus pagoda rising from a small lake — Hanoi icon' },
        { lat: 21.0233, lng: 105.8354, label: 'Temple of Literature', num: 3, cat: 'attraction', desc: 'Vietnam\'s 1,000-year-old first university' },
        { lat: 21.0524, lng: 105.8291, label: 'Tran Quoc Pagoda', num: 4, cat: 'attraction', desc: '6th-century pagoda on an island in West Lake' },
        { lat: 21.0335, lng: 105.8521, label: 'Café Giang', num: 5, cat: 'food', desc: 'Inventor of egg coffee — tiny alley café since 1946' }
      ]
    },
    {
      num: 16,
      date: '2026-06-23',
      neighborhoods: 'Hanoi · Train Street · Hoan Kiem',
      title: 'Hanoi Free Day — Markets, Train Street & Water Puppets',
      description: 'A free-ranging Hanoi day — browse Dong Xuan Market, catch the train roll through the narrow alley of Train Street, and end the evening with a traditional water puppet performance.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dong Xuan Market',
              description: 'Hanoi\'s largest covered market — a three-storey warren of stalls selling everything from silk fabric and ao dai to dried mushrooms, live animals, and street food. The ground floor food section is particularly good for breakfast browsing.',
              details: [
                '🛒 Dong Xuan is where locals shop — more authentic than tourist-focused markets',
                '🥘 Upstairs food stalls: bún ốc (snail noodle soup) is a Hanoi speciality',
                '🧵 Fabric section: beautiful silks and cottons by the metre, very cheap'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Bún Ốc (Snail Noodle Soup)',
              description: 'A very Hanoi breakfast — rice vermicelli in tomato-tinged broth with freshwater snails and rice paddy herb. Unfamiliar but delicious — a local favourite that rarely appears outside northern Vietnam.',
              meta: '💰 $ · 📍 35 Hang Dieu — or at Dong Xuan market stalls'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train Street',
              description: 'One of Hanoi\'s most extraordinary urban curiosities — a narrow lane where residential houses line both sides of a working railway track, with barely 50cm to spare. Residents sit on their doorsteps and drink coffee while the train rolls past. Visit the cafés on the upper floors for the best view.',
              details: [
                '🚂 Train passes 1–2 times each afternoon — check schedule online',
                '☕ Cafés above the street level have the best viewpoint',
                '⚠️ Stay behind the white safety line when the train approaches'
              ]
            },
            {
              title: 'Hang Ma (Paper Offerings Street)',
              description: 'One of the most visually extraordinary streets in the Old Quarter — Hang Ma is entirely dedicated to brightly coloured paper offerings for the dead: paper houses, cars, phones, money. Even if not buying, the visual spectacle is stunning.',
              details: [
                '🏮 The street is also famous for seasonal decorations — beautiful at any time',
                '📸 The colours and textures are extraordinary for photography'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Thang Long Water Puppet Theatre',
              description: 'Water puppetry originated in the Red River Delta over 1,000 years ago — performers stand waist-deep in water, controlling wooden puppets on bamboo rods. The Thang Long theatre on Hoan Kiem Lake does the best performances in Vietnam, with live traditional music.',
              details: [
                '🎭 Book tickets in advance: 100,000 VND — 50-minute show',
                '🎵 Live orchestra plays traditional instruments including dan bau and trong drums',
                '🐉 Dragon, phoenix, and agricultural scenes from Vietnamese village life'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Quan An Ngon Hanoi',
              description: 'A beautiful colonial courtyard restaurant where different stalls cook specialties from around Vietnam — you walk the courtyard and point at what you want, then eat at communal tables. An excellent way to sample 5–6 different Vietnamese dishes in one sitting.',
              meta: '💰 $$ · 📍 18 Phan Boi Chau, Hoan Kiem'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0419, lng: 105.8498, label: 'Dong Xuan Market', num: 1, cat: 'food', desc: 'Hanoi\'s largest covered market — fabric, food, everything' },
        { lat: 21.0348, lng: 105.8469, label: 'Train Street', num: 2, cat: 'attraction', desc: 'Working railway through residential alley — uniquely Hanoi' },
        { lat: 21.0346, lng: 105.8485, label: 'Hang Ma Street', num: 3, cat: 'attraction', desc: 'Paper offerings street — extraordinary colours and craft' },
        { lat: 21.0284, lng: 105.8559, label: 'Thang Long Water Puppet Theatre', num: 4, cat: 'attraction', desc: '1,000-year-old water puppetry tradition — best theatre in Vietnam' }
      ]
    },
    {
      num: 17,
      date: '2026-06-24',
      neighborhoods: 'Ninh Binh · Trang An · Tam Coc',
      title: 'Ninh Binh — The Inland Ha Long Bay',
      description: 'Ninh Binh is called "Ha Long Bay on land" — an extraordinary landscape of towering limestone karsts rising from rice paddies and rivers. A day trip from Hanoi that is one of Vietnam\'s most visually spectacular experiences.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Ninh Binh & Trang An Boat Tour',
              description: 'Depart Hanoi early by car (2 hours south). Begin at Trang An — a UNESCO-listed geopark where small wooden row boats navigate through a labyrinth of karst formations, rice paddies, and river caves. The scenery is breathtaking and the caves are theatrical.',
              details: [
                '🚗 Hire a driver for the day from Hanoi: ~$40–60 for the full tour',
                '⛵ Trang An boat tour: 200,000 VND per person — about 2 hours',
                '🦅 Eagles and cormorants nest in the karsts — frequently spotted',
                '🕳️ Pass through 9 caves during the tour — some are enormous and cathedral-like'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'En Route Roadside Café',
              description: 'Stop at a traditional Vietnamese roadside café between Hanoi and Ninh Binh for pho, bánh mì, or sticky rice wrapped in banana leaves (xôi) — authentic morning fuel before the day\'s adventure.',
              meta: '💰 $ · 📍 Roadside cafés on National Highway 1 between Hanoi and Ninh Binh'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tam Coc Boat Tour & Mua Cave',
              description: 'Tam Coc — "Three Caves" — is a classic Ninh Binh scene: rice paddies leading to three natural caves, all explored by rowing boat with local women using their feet to paddle. Then climb Mua Cave (500 steps) for the panoramic view over the entire valley — one of Vietnam\'s most iconic viewpoints.',
              details: [
                '⛵ Tam Coc boat: 150,000 VND — takes 2 hours',
                '🧗 Mua Cave climb: 100,000 VND entry — the view at the top is extraordinary',
                '📸 The dragon statue at the top of Mua Cave overlooks the entire karst valley',
                '🌾 June means rice is in the fields — vivid green against grey limestone'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Bich Dong Pagoda & Return to Hanoi',
              description: 'A final stop at Bich Dong — a three-level pagoda carved into the face of a karst cliff, with caves leading up through the mountain to a summit view. Then head back to Hanoi by car, arriving in time for a late dinner.',
              details: [
                '🛕 Bich Dong Pagoda: free entry — three levels carved into the cliff',
                '🌿 The path up through the pagoda levels is wonderfully atmospheric',
                '🕕 Allow 2 hours return drive to Hanoi from Ninh Binh'
              ]
            }
          ],
          meals: [
            {
              type: '🍖 Dinner',
              name: 'Dê Núi (Mountain Goat) in Ninh Binh',
              description: 'Ninh Binh\'s speciality meat is mountain goat — roasted, stir-fried with lemongrass, or served in hotpot. Try it at a local restaurant before the drive back.',
              meta: '💰 $$ · 📍 Restaurants near Tam Coc village'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2614, lng: 105.8694, label: 'Trang An Geopark', num: 1, cat: 'attraction', desc: 'UNESCO boat tour through karst caves and rice paddies' },
        { lat: 20.2244, lng: 105.9095, label: 'Tam Coc', num: 2, cat: 'attraction', desc: 'Three caves by rowing boat through paddy fields' },
        { lat: 20.2185, lng: 105.9014, label: 'Mua Cave Viewpoint', num: 3, cat: 'attraction', desc: '500-step climb to Vietnam\'s most dramatic valley panorama' },
        { lat: 20.2235, lng: 105.9081, label: 'Bich Dong Pagoda', num: 4, cat: 'attraction', desc: 'Three-level pagoda carved into a limestone cliff' }
      ]
    },
    {
      num: 18,
      date: '2026-06-25',
      neighborhoods: 'Hanoi · Transfer to Ha Long Bay',
      title: 'Ha Long Bay — Embark on the Overnight Cruise',
      description: 'Board a luxury overnight cruise into Ha Long Bay — 1,969 islands of limestone rising from jade-green water, one of the world\'s great natural wonders. This is the journey, the journey, the journey.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Transfer to Ha Long Bay',
              description: 'A cruise shuttle picks you up from your Hanoi hotel and drives 3.5 hours to Ha Long City. Board the junk boat at noon and sail into the bay as lunch is served. The first hour of sailing — watching the karsts rise from the water all around you — is genuinely awe-inspiring.',
              details: [
                '🚌 Transfer included in most cruise packages',
                '⏰ Morning pickup ~7:30–8am from Old Quarter hotels',
                '⛵ Recommend booking a mid-range or luxury cruise ($120–200 per person/night)',
                '🌊 Bhaya Cruises, Paradise Cruises, or Indochina Junk are top-tier options'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Lunch',
              name: 'On Board Welcome Lunch',
              description: 'Most Ha Long cruises serve a fresh seafood lunch as you first sail into the bay. Steamed squid, clams, steamed fish, and spring rolls, with the karsts rising around you outside the window.',
              meta: '💰 Included in cruise · 📍 On board the junk boat'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kayaking Through Karst Tunnels',
              description: 'The afternoon stop — a kayaking excursion through sea caves and around the limestone islands. Paddle into hidden lagoons, discover secluded beaches, and see the bay from water level. Genuinely spectacular.',
              details: [
                '🚣 Kayaking included in most cruise packages',
                '🦑 The water is warm (28°C in June) — swimming off the kayak is wonderful',
                '🦅 Look for monkeys on the island cliffs and eagles overhead',
                '🌊 Luon Cave kayak route is a highlight — paddling into a completely enclosed lagoon'
              ]
            },
            {
              title: 'Floating Village Visit',
              description: 'A small boat tour to visit one of Ha Long Bay\'s last floating fishing villages — communities that live entirely on the water, raising fish in submerged cages beneath their floating homes. A completely unique way of life.',
              details: [
                '🐟 The fish farms raise grouper, squid, and various shellfish',
                '⛵ The villages are accessible only by small boat — usually a stop on cruise itineraries',
                '📸 The stilted houses and coloured boats against the karsts are extraordinary'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Drinks on the Sundeck',
              description: 'As the sun descends behind the limestone islands, join other passengers on the sundeck for cocktails and the most spectacular sunset you\'ve ever seen. The silhouettes of thousands of karsts stretching to the horizon, the water turning copper and gold.',
              details: [
                '🌅 Ha Long Bay sunsets are extraordinary — have your camera ready from 5:30pm',
                '🍹 Most cruises offer a sunset cocktail hour included or at bar prices',
                '⭐ After dark, the bay is utterly silent and the stars are unobstructed'
              ]
            }
          ],
          meals: [
            {
              type: '🦐 Dinner',
              name: 'Sunset Seafood Feast on Board',
              description: 'A multi-course seafood dinner on the junk boat as night falls over the bay. Fresh grilled prawns, steamed clams with lemongrass, soft-shell crab, and Vietnamese-style whole fish. Wine, candles, and karsts outside every window.',
              meta: '💰 Included in cruise · On board the junk boat'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.9101, lng: 107.1839, label: 'Ha Long Bay', num: 1, cat: 'attraction', desc: '1,969 limestone islands — one of the world\'s great wonders' },
        { lat: 20.9000, lng: 107.1200, label: 'Luon Cave Kayak Route', num: 2, cat: 'attraction', desc: 'Kayaking through karst tunnels into hidden lagoons' },
        { lat: 20.9244, lng: 107.1580, label: 'Vung Vieng Fishing Village', num: 3, cat: 'attraction', desc: 'Traditional floating fishing village on the bay' },
        { lat: 20.9350, lng: 107.0550, label: 'Ha Long City', num: 4, cat: 'attraction', desc: 'Departure point for bay cruises' }
      ]
    },
    {
      num: 19,
      date: '2026-06-26',
      neighborhoods: 'Ha Long Bay · Bai Tu Long Bay',
      title: 'Ha Long Bay — Caves, Beaches & Silent Morning',
      description: 'Your second day on the water. Explore the Sung Sot cave at dawn, swim off a deserted island beach, and sail deeper into the bay before heading back to Hanoi by evening.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise Tai Chi on the Sundeck',
              description: 'Wake at 6am for sunrise over the bay. Most cruises offer a tai chi session on the sundeck as the mist lifts from the karsts — one of the most peaceful, surreal experiences imaginable. The quiet of the bay in early morning is profound.',
              details: [
                '🌅 Sunrise is around 5:30am in late June — worth the early rise',
                '🧘 Tai chi is gentle and welcoming — no experience needed',
                '🌫️ Morning mist over the karsts creates an otherworldly, ink-painting landscape'
              ]
            },
            {
              title: 'Sung Sot (Amazing) Cave',
              description: 'The largest cave in Ha Long Bay — a cathedral-like cavern of stalactites and stalagmites with dramatic lighting. Two chambers, the second enormous enough to hold thousands of people. Walk up to the entrance for views back over the bay.',
              details: [
                '🕳️ Sung Sot is the most impressive cave in Ha Long — genuinely breathtaking',
                '💡 The cave is lit theatrically — some formations are 500 million years old',
                '📸 The view from the cave entrance over the bay is spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'On Board Breakfast',
              description: 'A leisurely breakfast on the boat — fresh fruit, banh mi, fried eggs, and Vietnamese coffee as the bay wakes up around you.',
              meta: '💰 Included in cruise · On board'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Swimming at Ti Top Island',
              description: 'Ti Top Island has a small but beautiful beach — swim in clear water with karsts all around, then climb the 427 steps to the island\'s summit for the most spectacular panoramic view of Ha Long Bay. On a clear June day, you can see hundreds of islands spreading to every horizon.',
              details: [
                '🏊 The beach is small but the water is clear and warm',
                '📸 The summit view at Ti Top is the iconic Ha Long Bay panorama',
                '⛵ Small boats take you from the junk to the island'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Hanoi',
              description: 'The cruise ends at noon with a final lunch on board, before the shuttle returns to Hanoi (arriving around 5–6pm). Rest and a slow evening — you\'ve earned it after two days on the water.',
              details: [
                '🚌 Shuttle drops at Old Quarter hotels',
                '😴 A quiet evening is well-earned after the boat — consider room service or a nearby pho bowl'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Pho 10 Ly Quoc Su',
              description: 'After returning to Hanoi, a simple and perfect bowl of pho at this famous Old Quarter spot — rich bone broth, rice noodles, thin beef slices. The perfect return-to-earth meal after Ha Long Bay.',
              meta: '💰 $ · 📍 10 Ly Quoc Su, Hoan Kiem'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.9101, lng: 107.1839, label: 'Ha Long Bay (Day 2)', num: 1, cat: 'attraction', desc: 'Second day on the water — caves, beaches, sunrise' },
        { lat: 20.9069, lng: 107.1306, label: 'Sung Sot Cave', num: 2, cat: 'attraction', desc: 'Ha Long\'s largest cave — cathedral-like stalactite chambers' },
        { lat: 20.9236, lng: 107.1447, label: 'Ti Top Island', num: 3, cat: 'attraction', desc: 'Beach swim + 427-step climb to the panoramic summit' }
      ]
    },
    {
      num: 20,
      date: '2026-06-27',
      neighborhoods: 'Hanoi · Hoan Kiem · Long Bien',
      title: 'Hanoi Final Day — Hidden Cafés, Galleries & Long Bien Bridge',
      description: 'A gentle final Hanoi day for everything you haven\'t done yet — the hidden courtyard cafés, the Long Bien Bridge at golden hour, and Hanoi\'s contemporary art scene before a farewell dinner.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hanoi Slow Morning — Hidden Café Alley',
              description: 'Hanoi\'s café culture is extraordinary — hundreds of tiny coffee shops hidden in alleys, on rooftops, and behind ancient wooden doors. Spend the morning café-hopping through the Old Quarter: Café Dinh (run from a family\'s front room), Café Nhan (ground floor of a colonial building), or the rooftop cafés on Hang Gai.',
              details: [
                '☕ Cà phê sữa đá (iced milk coffee): 25,000 VND — the perfect slow-sip morning drink',
                '🏠 Café Dinh: 13 Dinh Tien Hoang — tiny, atmospheric, original',
                '🌿 The Old Quarter rooftop cafés look over a sea of ancient orange tile roofs'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Bánh Cuốn Bà Hoành',
              description: 'The most famous bánh cuốn (steamed rice crepe) stall in Hanoi — silky, translucent rice sheets filled with minced pork and mushroom, served with fish sauce and crispy shallots. A gentle, perfect breakfast.',
              meta: '💰 $ · 📍 66 To Hien Thanh — opens 6am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Vietnam Museum of Ethnology',
              description: 'One of the best museums in Southeast Asia — a beautifully curated collection showcasing the culture, clothing, tools, and traditions of all 54 of Vietnam\'s ethnic groups. The outdoor section has full-size traditional houses from various highland communities. Fascinating and moving.',
              details: [
                '🏛️ Entry: 40,000 VND · Open 8am–5:30pm, closed Mon',
                '🌿 The outdoor section is magnificent — full-scale stilted longhouses and communal halls',
                '📸 The textile collection is extraordinary — hundreds of traditional costumes'
              ]
            },
            {
              title: 'Long Bien Bridge Walk',
              description: 'Hanoi\'s oldest iron bridge, built by Gustave Eiffel\'s company in 1902 — a long, creaking span across the Red River still used by motorbikes and pedestrians. Walk it in the afternoon for views over the vast river, the vegetable gardens on the flood plain, and the city skyline.',
              details: [
                '🌉 The bridge still carries trains, motorbikes, and pedestrians on separate sections',
                '📸 The view from the center of the bridge at sunset is one of Hanoi\'s great photographs',
                '🥬 The flood plain below grows most of Hanoi\'s fresh vegetables and herbs'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Nha Hang Ngon (Villa Dining)',
              description: 'A beautiful colonial villa transformed into a Vietnamese dining destination — 30+ different dishes from across the country, each cooked by specialists at open-air kitchen stalls around the garden courtyard. An ideal last supper in Vietnam.',
              meta: '💰 $$ · 📍 18 Phan Boi Chau, Hoan Kiem'
            }
          ],
          activities: [
            {
              title: 'Final Night at Hoan Kiem Lake',
              description: 'End your Vietnam journey at Hoan Kiem Lake. The lake is especially beautiful at night, lit from below, with locals doing tai chi, dancing, and playing badminton around its shores. A perfect, peaceful goodbye to Vietnam.',
              details: [
                '🌙 Weekend nights: the Old Quarter roads around the lake close to traffic',
                '🎵 Street musicians and dancers perform around the lake on weekends',
                '🏮 The red Huc Bridge and Ngoc Son Temple glowing at night — unforgettable last image'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0335, lng: 105.8498, label: 'Old Quarter Café Alleys', num: 1, cat: 'food', desc: 'Hidden courtyard cafés — Hanoi\'s slow morning ritual' },
        { lat: 21.0435, lng: 105.8300, label: 'Vietnam Museum of Ethnology', num: 2, cat: 'attraction', desc: 'Best museum in Vietnam — 54 ethnic groups showcased' },
        { lat: 21.0443, lng: 105.8524, label: 'Long Bien Bridge', num: 3, cat: 'attraction', desc: '1902 Eiffel-built bridge over the Red River' },
        { lat: 21.0285, lng: 105.8542, label: 'Hoan Kiem Lake at Night', num: 4, cat: 'attraction', desc: 'Final farewell — the lake glows beautifully at night' }
      ]
    },
    {
      num: 21,
      date: '2026-06-28',
      neighborhoods: 'Hanoi · Noi Bai Airport',
      title: 'Last Morning in Vietnam & Departure',
      description: 'A final slow morning in Hanoi before heading to the airport. One last bowl of pho, a walk by the lake, and the quiet satisfaction of having experienced one of the world\'s great travel destinations.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Hoan Kiem Lake Sunrise',
              description: 'Wake early for one last walk around Hoan Kiem Lake as the city wakes up. This is when Hanoi is at its most beautiful — locals doing tai chi on the lakeside paths, vendors setting up, the lake perfectly still and reflecting the morning light.',
              details: [
                '🌅 Sunrise is around 5:30am — worth setting the alarm one last time',
                '🧘 Join the tai chi groups on the lakeside — beginners always welcome to watch and try',
                '🐢 The famous giant turtle occasionally surfaces in the early morning'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Final Breakfast',
              name: 'One Last Bowl of Pho',
              description: 'Your final meal in Vietnam should be exactly what you had on your first morning — a perfect bowl of Hanoi pho. Clear beef broth, silky noodles, fresh herbs, a squeeze of lime. Vietnam in a bowl.',
              meta: '💰 $ · 📍 Pho Thin, 13 Lo Duc — or the nearest street stall to your hotel'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Transfer to Noi Bai International Airport',
              description: 'Allow plenty of time for the journey to Noi Bai Airport — 35–45km north of the city. Traffic can be significant, especially midday. Vietnam Airlines, Vietjet, and Bamboo connect Hanoi to major international hubs.',
              details: [
                '🚗 Grab to airport: ~$12–18 USD depending on traffic',
                '⏰ Allow 2–2.5 hours before your international departure',
                '🛍️ Last-minute shopping at the airport: Vietnamese coffee (Trung Nguyen), pho spice packets, lacquerware',
                '🎁 Don\'t forget: take home bánh phồng tôm (prawn crackers) as snacks for the flight'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Vietnam will almost certainly get under your skin. It\'s a country with a gift for making first-time visitors plan a return trip before they\'ve even left. One journey is rarely enough.' }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0285, lng: 105.8542, label: 'Hoan Kiem Lake — Final Morning', num: 1, cat: 'attraction', desc: 'Last sunrise walk by the sacred turtle lake' },
        { lat: 21.2212, lng: 105.8072, label: 'Noi Bai International Airport', num: 2, cat: 'attraction', desc: 'Departure — Hanoi\'s international airport, 35km north' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$25–50/night', midrange: '$60–120/night', luxury: '$150–300/night' },
    { category: 'Meals (per couple)', budget: '$15–30/day', midrange: '$40–80/day', luxury: '$100–200/day' },
    { category: 'Domestic Flights (3)', budget: '$80–150 total', midrange: '$150–280 total', luxury: '$300–500 (flex tickets)' },
    { category: 'Ha Long Bay Cruise (2 nights)', budget: '$150–250pp', midrange: '$280–450pp', luxury: '$500–900pp' },
    { category: 'Day Tours & Activities', budget: '$5–20/day', midrange: '$30–60/day', luxury: '$80–150/day' },
    { category: '21-Day Total (couple)', budget: '$2,000–3,500', midrange: '$4,000–7,000', luxury: '$10,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Ho Chi Minh City (SGN) and out of Hanoi (HAN) for the most efficient route', 'Direct flights from many US cities via Tokyo, Seoul, or Hong Kong (15–20 hours total)', 'Vietnam Airlines, EVA Air, and Korean Air are popular options from North America'] },
    { title: '📋 Visas', items: ['Most nationalities now get 90-day visa-free entry to Vietnam', 'Check Vietnam e-visa system at evisa.xuatnhapcanh.gov.vn for your nationality', 'The e-visa ($25 USD) is valid for 90 days single or multiple entry'] },
    { title: '🏨 Where to Stay', items: ['HCMC: The Reverie Saigon (luxury), Caravelle Hotel (classic), or boutique hotels in District 1', 'Hoi An: La Siesta Resort & Spa, Anantara Hoi An, or a riverside guesthouse in the Ancient Town', 'Hue: Pilgrimage Village Boutique Resort, La Residence Hotel (French colonial)', 'Hanoi: Sofitel Legend Metropole (historic), Pan Pacific Hanoi, or Old Quarter boutique hotels'] },
    { title: '🌡️ June Weather', items: ['South Vietnam (HCMC, Mekong): hot and humid, 30–35°C, afternoon showers', 'Central Vietnam (Hoi An, Hue): warm and drier, 28–32°C', 'North Vietnam (Hanoi, Ha Long, Ninh Binh): warm and humid, 28–33°C, occasional rain', 'Da Lat is 10°C cooler than everywhere else — a welcome break at 17–22°C'] },
    { title: '🛵 Transport Between Cities', items: ['Domestic flights: Vietjet, Bamboo, Vietnam Airlines — book 2–4 weeks ahead for best prices', 'HCMC→Da Lat: 1 hour flight or 7-hour bus through highlands', 'Da Nang→Hanoi: 1h15min flight — skip the long overland journey', 'Within cities: Grab app is essential — safe, metered, English-speaking'] },
    { title: '💊 Health', items: ['No mandatory vaccinations for Vietnam, but hepatitis A & B, typhoid, and tetanus are recommended', 'Mosquito repellent is essential — apply morning and evening', 'Tap water is not drinkable — buy bottled or use a filtered water bottle', 'Travel insurance is strongly recommended — quality hospitals available in HCMC and Hanoi'] }
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
