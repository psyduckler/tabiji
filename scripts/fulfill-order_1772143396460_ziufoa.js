const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772143396460_ziufoa',
  email: 'spralex@gmail.com',
  destination: 'Rio de Janeiro, Brazil',
  startDate: '2026-10-20',
  endDate: '2026-10-24',
  groupSize: 4,
  requests: '2 couples going (4 people total). 2 out of 4 people are vegetarian.'
};

const itineraryData = {
  destination: 'Rio de Janeiro, Brazil',
  countryEmoji: '🇧🇷',
  title: 'Rio de Janeiro: Adventure, Culture & Flavor',
  subtitle: '4 nights of beaches, jungle hikes, samba nights & world-class food for two couples',
  description: "Rio de Janeiro is one of the world's most dramatic cities — a place where jungle mountains plunge into golden beaches, colonial neighborhoods pulse with samba, and every sunset over Guanabara Bay looks like a painting. This itinerary blends adrenaline-fueled adventure (hang gliding, jungle hiking, rock climbing) with deep cultural immersion (Santa Teresa art scenes, samba schools, Afro-Brazilian heritage), exceptional food for both meat-lovers and vegetarians, and blissful relaxation on Ipanema and Copacabana. October is ideal: the rainy season hasn't arrived, crowds are thin, and the lush Tijuca forest is vivid green.",
  duration: '4 nights',
  dates: 'Oct 20 – Oct 24, 2026',
  budget: '$$$',
  pace: 'Active',
  bestFor: 'Two Couples · Adventure + Culture + Food',
  highlights: [
    'Hang gliding over Ipanema Beach from Pedra Bonita',
    'Sunrise hike to Dois Irmãos peak for panoramic views',
    'Christ the Redeemer and Corcovado by sunrise train',
    'Street food and samba in Santa Teresa and Lapa',
    'Sunset caipirinhas at Aprazível with bay views'
  ],

  essentials: [
    { title: '🌤️ October Weather', text: 'October is spring in Rio — warm (25–30°C), mostly sunny with occasional afternoon showers. Perfect for beaches, hikes, and outdoor dining. Jungle trails are lush and green.' },
    { title: '🥦 Vegetarian in Rio', text: 'Rio has excellent vegetarian options. Brazilian cuisine features abundant rice, beans, tropical fruit, and fresh salads. Many restaurants offer a veggie prato feito (daily plate). Seek out por kilo buffet restaurants where you pay by weight — always has incredible veggie selection.' },
    { title: '🚌 Getting Around', text: 'Use 99 or Uber for safety and convenience. The metro connects Ipanema/Copacabana to Centro. Avoid buses at night. Santa Teresa is best by Uber — the historic tram is scenic but limited.' },
    { title: '💰 Budget Tips', text: 'Por kilo restaurants are great value ($5–10pp). Street food (acarajé, tapioca, açaí) is cheap and delicious. Beaches are free. Most cultural sites cost under $10. Top dining for four runs $80–150 with drinks.' },
    { title: '🔒 Safety', text: 'Rio is safe in tourist zones — Ipanema, Copacabana, Santa Teresa, Urca, Barra. Stay in well-lit areas at night, avoid displays of expensive jewelry/cameras on the beach, and use hotel safes. Stick with Uber over hailing cabs.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-10-20',
      neighborhoods: 'Ipanema · Leblon · Vidigal',
      title: 'Arrival: Beaches, Sunset & South Zone Vibes',
      description: "Touch down in Rio, settle into the sun-soaked South Zone, and let the city cast its spell. Afternoon on Ipanema's famous sands, a sunset hike with jaw-dropping views, and dinner in Leblon — the most elegant neighborhood in Rio.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ipanema Beach & Farme de Amoedo',
              description: "Drop your bags and head straight to Ipanema Beach — one of the most beautiful urban beaches in the world. Set up near Posto 9 (the hip central section) and soak in the iconic view: twin peaks of Dois Irmãos rising from the sea. The beach culture here is unlike anywhere else.",
              details: [
                '🏖️ Posto 9 is the bohemian heart of Ipanema — artists, musicians, and locals',
                '🌊 October water temp is ~23°C — perfect for swimming',
                '🥤 Order água de coco from beach vendors — the real thing in a fresh coconut',
                '🎒 Leave valuables at the hotel. Use a waterproof pouch for your phone'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Snack',
              name: 'Bibi Sucos',
              description: 'Legendary juice bar on Ipanema — try the açaí bowl or a fresh tropical juice blend. 100% vegetarian-friendly.',
              meta: '💰 $ · 📍 Rua Teixeira de Melo, Ipanema · Vegetarian ✅'
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Dois Irmãos Viewpoint (Vidigal Trail)',
              description: "Hike up from Vidigal favela to the summit of Dois Irmãos — one of Rio's most rewarding short hikes. The twin peaks rise above Ipanema and São Conrado beaches, and from the top you get a 360° panorama that puts everything in perspective: beach, mountains, city, sea.",
              details: [
                '🥾 45-60 minute hike each way — moderate difficulty, well-marked trail',
                '🌅 Aim to arrive at the top by 5pm for golden hour',
                '🦁 Look for squirrel monkeys on the trail — they\'re cheeky and used to people',
                '📍 Trailhead: Take Uber to "Trilha dos Dois Irmãos, Vidigal"'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Wear trail shoes and bring water. The view from the top — looking down on Ipanema from above — is among the best in the world. Go before sunset and watch the light change over the bay.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Zaza Bistrô Tropical',
              description: "Creative Brazilian fusion in a beautifully decorated space in Ipanema. Half the menu is vegetarian — think coconut curry with tropical vegetables, stuffed chayote, and vibrant salads alongside grilled fish and meats. Perfect for a mixed group.",
              meta: '💰 $$$ · 📍 Rua Joana Angélica 40, Ipanema · Vegetarian-friendly ✅'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9868, lng: -43.2044, label: 'Ipanema Beach (Posto 9)', num: 1, cat: 'attraction', desc: 'Famous bohemian stretch of Ipanema — the heart of beach culture' },
        { lat: -23.0128, lng: -43.2211, label: 'Dois Irmãos Trailhead (Vidigal)', num: 2, cat: 'attraction', desc: 'Start of the twin peaks hike — squirrel monkeys and panoramic views' },
        { lat: -23.0083, lng: -43.2201, label: 'Dois Irmãos Summit', num: 3, cat: 'attraction', desc: '360° panorama over Ipanema, São Conrado and Guanabara Bay' },
        { lat: -22.9845, lng: -43.2032, label: 'Bibi Sucos', num: 4, cat: 'food', desc: 'Legendary açaí and fresh juice bar in Ipanema' },
        { lat: -22.9850, lng: -43.2001, label: 'Zaza Bistrô Tropical', num: 5, cat: 'food', desc: 'Creative fusion dining — excellent vegetarian options' }
      ]
    },
    {
      num: 2,
      date: '2026-10-21',
      neighborhoods: 'Corcovado · Cosme Velho · Santa Teresa · Lapa',
      title: 'Christ the Redeemer, Bohemian Santa Teresa & Samba Night',
      description: "The most iconic day in Rio: sunrise at Christ the Redeemer, a lazy afternoon in the bohemian hilltop neighborhood of Santa Teresa with street art and colonial mansions, then diving into Lapa's legendary Friday night samba scene.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Christ the Redeemer at Sunrise',
              description: "Take the first Corcovado train (6:30am) to beat the crowds and catch the sunrise from the feet of Christ the Redeemer. On a clear morning you'll see the entire city laid out below: Sugarloaf, Guanabara Bay, Maracanã, the Atlantic — all at once. October skies are usually crystal clear.",
              details: [
                '🚂 Trem do Corcovado departs from Cosme Velho — book tickets online in advance',
                '⏰ First train is 6:30am — arrive at station by 6am',
                '🎟️ Buy timed tickets at trenmdocorcovado.rio — sells out on weekends',
                '📸 The statue is 30m tall — go wide and shoot from the lower viewing platform',
                '☁️ Check weather forecast the night before — clear days are magic, cloudy ones are mystical'
              ]
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Santa Teresa Neighborhood Walk',
              description: "Take the charming yellow tram (or Uber) up to Santa Teresa — Rio's bohemian hilltop neighborhood of crumbling mansions, street art, artist studios, and spectacular bay views. Wander the steep cobblestone streets, discover the Parque das Ruínas (a beautiful ruin with a terrace overlooking the city), and explore the local galleries.",
              details: [
                '🎨 Parque das Ruínas — free entry, stunning views from the terrace',
                '🏛️ Museu Chácara do Céu — private collection of Picasso, Dalí, and Brazilian modernists',
                '🖼️ The steep streets are an open-air gallery of murals and sculptures',
                '🛍️ Browse artisan shops on Largo do Guimarães — handmade jewelry and ceramics'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Aprazível',
              description: "Set in a tropical garden spilling down a hillside in Santa Teresa, Aprazível is one of Rio's most magical restaurants. The garden terrace overlooks Guanabara Bay. Brazilian-inspired cuisine with exceptional vegetarian options — try the tapioca with smoked palm hearts, the tropical fruit plates, and the slow-cooked beans.",
              meta: '💰 $$$ · 📍 Rua Aprazível 62, Santa Teresa · Vegetarian-friendly ✅'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Selarón Staircase & Lapa Arches',
              description: "Walk down from Santa Teresa to the famous Selarón Steps — a kaleidoscopic mosaic staircase created by Chilean artist Jorge Selarón over 20 years. Continue to the Lapa Arches (Arcos da Lapa), the dramatic 18th-century aqueduct that's become the symbol of Rio's bohemian nightlife district.",
              details: [
                '🎨 Selarón Steps: 250 mosaic steps featuring tiles from 60+ countries',
                '📸 Best photos: morning light or late afternoon — midday gets crowded',
                '🏛️ Arcos da Lapa: originally a Roman-style aqueduct, now carries the Santa Teresa tram',
                '🍦 Grab a mate leão or sugar cane juice from street vendors nearby'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "The Selarón Steps are busiest midday — visit in the late afternoon for better photos and cooler temps. The surrounding Lapa neighborhood comes alive after dark, so returning in the evening is the real experience." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lapa Samba Night',
              description: "Tuesday through Saturday, Lapa transforms into one of the world's great street party scenes. Live samba and pagode spill out of bars and clubs onto the street. Cariocas (Rio locals) of all ages dance under the arches. Join the swirling mass at Rio Scenarium or Circo Voador, or just street dance under the arches.",
              details: [
                '🎵 Rio Scenarium — 3 floors of live music in a converted antique shop',
                '🎺 Circo Voador — legendary outdoor venue under a big top',
                '💃 Street samba kicks off around 10pm and goes until 3am',
                '🍺 Brahma beer and caipirinhas flow freely — cheap and cheerful'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bar do Mineiro',
              description: "Santa Teresa institution since 1948 — beloved for classic Minas Gerais comfort food. Incredible feijoada (black bean stew) and coxinha, with excellent vegetarian options including tutu à mineira (creamy mashed beans), fried plantains, and seasonal vegetable dishes.",
              meta: '💰 $$ · 📍 Rua Paschoal Carlos Magno 99, Santa Teresa · Vegetarian options ✅'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9519, lng: -43.2105, label: 'Christ the Redeemer', num: 1, cat: 'attraction', desc: 'The iconic statue — take the first train for sunrise views' },
        { lat: -22.9183, lng: -43.1790, label: 'Santa Teresa', num: 2, cat: 'attraction', desc: 'Bohemian hilltop neighborhood — art, views, colonial mansions' },
        { lat: -22.9221, lng: -43.1790, label: 'Parque das Ruínas', num: 3, cat: 'attraction', desc: 'Crumbling mansion turned art space with bay overlook terrace' },
        { lat: -22.9263, lng: -43.1803, label: 'Selarón Steps', num: 4, cat: 'attraction', desc: 'Colorful mosaic staircase — one of Rio\'s most photogenic spots' },
        { lat: -22.9291, lng: -43.1788, label: 'Arcos da Lapa', num: 5, cat: 'attraction', desc: '18th-century aqueduct arches — heart of the samba nightlife district' },
        { lat: -22.9213, lng: -43.1820, label: 'Aprazível', num: 6, cat: 'food', desc: 'Garden restaurant in Santa Teresa with bay views — excellent veggie menu' },
        { lat: -22.9220, lng: -43.1843, label: 'Bar do Mineiro', num: 7, cat: 'food', desc: 'Classic Santa Teresa eatery — try the feijoada or tutu à mineira' },
        { lat: -22.9284, lng: -43.1819, label: 'Rio Scenarium', num: 8, cat: 'attraction', desc: 'Legendary 3-floor samba venue in Lapa' }
      ]
    },
    {
      num: 3,
      date: '2026-10-22',
      neighborhoods: 'Urca · Sugarloaf · Flamengo · Centro',
      title: 'Sugarloaf, History & Guanabara Bay at Sunset',
      description: "One of Rio's great adventure days: cable car up Sugarloaf Mountain at sunset, a morning in the charming Urca neighborhood with its military village atmosphere, and a deep dive into Rio's fascinating colonial history in the historic center.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Urca Village & Praia Vermelha',
              description: "Urca is one of Rio's most peaceful and charming neighborhoods — a walled military village on a peninsula between Sugarloaf and the bay. Stroll along the waterfront promenade, swim at Praia Vermelha (Red Beach — sheltered and calm), and watch the fishing boats come in.",
              details: [
                '🏖️ Praia Vermelha is one of Rio\'s most beautiful small beaches — calm water, mountain backdrop',
                '🦐 The waterfront kiosks serve cold beer and fresh shrimp — great for people watching',
                '🐟 Early morning fishermen bring in their catch along Urca\'s promenade',
                '🏛️ The neighborhood feels like a village frozen in the 1950s — genuinely tranquil'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Cafe Urca',
              description: 'Iconic waterfront café right on the Urca promenade overlooking the bay. Famous for their pastéis, tapioca, and açaí bowls. One of Rio\'s best breakfast spots with spectacular views.',
              meta: '💰 $ · 📍 Rua Cândido Gaffrée 205, Urca · Vegetarian ✅'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Rock Climbing at Morro da Urca (Optional Adventure)',
              description: "Urca Hill and the surrounding granite faces are world-class climbing routes — from beginner to expert. Local guides offer 3-hour climbing sessions on the same rock formations the cable car ascends. Non-climbers can hike the trail up Morro da Urca for city views.",
              details: [
                '🧗 Rio Trekking and Jungle Me offer guided climbing sessions from ~$60pp',
                '⏱️ 2-3 hours for a beginner session',
                '🥾 Non-climbers: hike to Morro da Urca via the Claudio Coutinho trail (~45 min)',
                '🌊 The Claudio Coutinho coastal trail is flat, shaded, and runs along the base of Sugarloaf'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Historic Centro & Cinelândia',
              description: "Head to Rio's historic center — a fascinating layer cake of Portuguese colonial architecture, Art Nouveau buildings, and vibrant street life. The Theatro Municipal is breathtaking, Paço Imperial (former royal palace) is free, and the Centro Cultural Banco do Brasil hosts world-class free exhibitions.",
              details: [
                '🏛️ Theatro Municipal — guided tours available, stunning Beaux-Arts interior',
                '🎨 CCBB (Centro Cultural Banco do Brasil) — free world-class art exhibitions',
                '⛪ Real Gabinete Português de Leitura — the most beautiful library in Brazil',
                '🚶 The pedestrianized Rua do Ouvidor has great street food stalls'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Confeitaria Colombo',
              description: "A Rio landmark since 1894 — a Belle Époque café with 18-meter mirrors, stained glass, and gilded balconies. Elegant lunch options include quiches, fresh salads, and Brazilian classics. The vegetarian spread at their buffet is excellent.",
              meta: '💰 $$ · 📍 Rua Gonçalves Dias 32, Centro · Vegetarian-friendly ✅'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sugarloaf Cable Car at Sunset',
              description: "The classic Rio experience — two cable car rides to the top of Sugarloaf (Pão de Açúcar), arriving just before sunset. From 396 meters up, you have a 360° panorama: Corcovado with Christ looking down, the Atlantic coast, Guanabara Bay shimmering gold. Book the last cable car of the day for the sunset-to-nighttime transition.",
              details: [
                '🚡 Book tickets at bondinho.com.br — last car is 8:55pm',
                '🌅 Arrive at the base by 5pm to ensure sunset timing',
                '📸 First cable car stop (Morro da Urca) has great Sugarloaf composition shots',
                '🌃 Stay after sunset — the city lights at night from the summit are equally magical',
                '🥂 There\'s a kiosk at the top — caipirinhas at sunset is peak Rio'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Botequim da Esquina (Flamengo)',
              description: "A traditional Rio boteco (corner bar) in charming Flamengo — classic Brazilian comfort food, cold draft beer, and a lively local crowd. Try the moqueca de legumes (vegetable coconut curry) and the arroz com feijão. Local and unpretentious.",
              meta: '💰 $$ · 📍 Flamengo neighborhood · Vegetarian options ✅'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9517, lng: -43.1664, label: 'Praia Vermelha', num: 1, cat: 'attraction', desc: 'Beautiful sheltered beach at the foot of Sugarloaf' },
        { lat: -22.9512, lng: -43.1654, label: 'Cafe Urca', num: 2, cat: 'food', desc: 'Iconic waterfront café — açaí bowls and bay views' },
        { lat: -22.9492, lng: -43.1558, label: 'Claudio Coutinho Trail', num: 3, cat: 'attraction', desc: 'Flat coastal trail around the base of Sugarloaf — birds and monkeys' },
        { lat: -22.9489, lng: -43.1565, label: 'Sugarloaf Mountain', num: 4, cat: 'attraction', desc: 'Cable car to 396m summit — sunset views over all of Rio' },
        { lat: -22.9035, lng: -43.1759, label: 'Real Gabinete Português de Leitura', num: 5, cat: 'attraction', desc: 'The most beautiful library in Brazil — free to visit' },
        { lat: -22.9075, lng: -43.1754, label: 'Confeitaria Colombo', num: 6, cat: 'food', desc: 'Belle Époque landmark café since 1894' },
        { lat: -22.9341, lng: -43.1772, label: 'Flamengo', num: 7, cat: 'attraction', desc: 'Traditional neighborhood — boteco dinner and local Rio vibe' }
      ]
    },
    {
      num: 4,
      date: '2026-10-23',
      neighborhoods: 'Tijuca Forest · São Conrado · Barra da Tijuca',
      title: 'Jungle Adventure: Hang Gliding & Tijuca Forest',
      description: "The most exhilarating day in Rio: soar over Ipanema Beach on a tandem hang glider, then plunge into the world's largest urban rainforest for waterfall hikes and wildlife spotting. Tonight, celebrate with a feast at a top Rio restaurant.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Hang Gliding from Pedra Bonita',
              description: "The single most spectacular thing you can do in Rio — tandem hang gliding from the 520m Pedra Bonita launch ramp. You run off the mountain, soar over the Atlantic forest, and land on São Conrado beach 10 minutes later. No experience needed — you're harnessed to a licensed pilot.",
              details: [
                '🪂 Book with Just Fly or Delta Flight Rio — both ABVL-certified (Brazil\'s aviation authority)',
                '⏰ First flights depart 8am — go early for calmer winds and better visibility',
                '💰 ~$120-140pp for a 10-15 minute flight',
                '📱 They video and photograph the entire flight — buy the footage!',
                '❓ Weight limit: 100kg per person. Minimum age: 6. No prior experience needed'
              ]
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tijuca National Park — Cascatinha Taunay & Pico da Tijuca',
              description: "The world's largest urban rainforest covers 32 square kilometers and sits right inside Rio. Hike through dense Atlantic rainforest to Cascatinha Taunay waterfall (15-meter cascade) and continue to the Pico da Tijuca summit (1,021m) for extraordinary views over the city.",
              details: [
                '🌿 Tijuca forest has 100+ endemic species — toucans, monkeys, bromeliads',
                '💧 Cascatinha Taunay is a 15-minute easy walk from the main entrance',
                '⛰️ Pico da Tijuca summit: 3-4 hour round trip, moderate-strenuous',
                '🕊️ Vista Chinesa: Chinese pavilion lookout — stunning city panorama',
                '👟 Wear trail shoes and bring bug spray, water, and sunscreen'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Picnic Lunch',
              name: 'Tijuca Forest Picnic',
              description: "Pack a picnic from the local market or your hotel — the park has beautiful picnic areas near the waterfall. Or grab açaí bowls and wraps from the park entrance vendors.",
              meta: '💰 $ · Bring supplies from the city · Vegetarian ✅'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Barra da Tijuca Beach',
              description: "After the forest, cool off at Barra da Tijuca — Rio's longest and least crowded beach, backed by lagoons and mountains. The water is crystal-clear and the waves are excellent for surfing. Rent boards from the beach kiosks and try to surf, or just collapse on the sand.",
              details: [
                '🏄 Surf lessons available from beach instructors — $40/hour',
                '🌊 Barra is 18km long — walk to quieter sections away from the kiosks',
                '🦅 The lagoon side of Barra has kayaking and stand-up paddleboarding'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Pedra do Arpoador',
              description: "Back in Ipanema, join the Rio tradition of watching the sunset from Arpoador Rock — a granite promontory that juts into the sea between Ipanema and Copacabana. The whole beach applauds when the sun drops below the horizon. A completely free, completely Rio experience.",
              details: [
                '🌅 The sunset applause is a genuine Rio tradition — everyone claps',
                '🚶 Walk from Ipanema to Arpoador — it\'s the southern tip of the beach',
                '🎸 Street musicians often set up nearby — catch free live music'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'CT Boucherie (Leblon)',
              description: "Claude Troisgros's Rio landmark — modern French-Brazilian cuisine in a stunning Leblon space. The menu balances exceptional meat dishes (beef, suckling pig) with outstanding vegetarian options including seasonal vegetable risottos, roasted beet compositions, and fresh pasta. A perfect celebratory dinner for all four.",
              meta: '💰 $$$$ · 📍 Rua Dias Ferreira 636, Leblon · Vegetarian-friendly ✅'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -23.0028, lng: -43.2878, label: 'Pedra Bonita Hang Glide Launch', num: 1, cat: 'attraction', desc: 'Tandem hang gliding launch ramp — 520m above Ipanema' },
        { lat: -22.9717, lng: -43.2463, label: 'Tijuca National Park', num: 2, cat: 'attraction', desc: 'World\'s largest urban rainforest — waterfalls and wildlife' },
        { lat: -22.9638, lng: -43.2569, label: 'Cascatinha Taunay', num: 3, cat: 'attraction', desc: '15-meter waterfall deep in the Atlantic forest' },
        { lat: -22.9588, lng: -43.2763, label: 'Pico da Tijuca', num: 4, cat: 'attraction', desc: 'Highest point in Rio — 360° panorama from the summit' },
        { lat: -23.0094, lng: -43.3156, label: 'Barra da Tijuca Beach', num: 5, cat: 'attraction', desc: "Rio's longest beach — great waves, surf lessons, crystal water" },
        { lat: -22.9897, lng: -43.1970, label: 'Pedra do Arpoador', num: 6, cat: 'attraction', desc: 'Granite rock jutting into the sea — Rio\'s sunset applause tradition' },
        { lat: -22.9900, lng: -43.2261, label: 'CT Boucherie', num: 7, cat: 'food', desc: 'Claude Troisgros\'s French-Brazilian masterpiece in Leblon' }
      ]
    },
    {
      num: 5,
      date: '2026-10-24',
      neighborhoods: 'Copacabana · Ipanema · Jardim Botânico',
      title: 'Last Morning: Botanical Garden, Copacabana & Farewell',
      description: "A slow, beautiful final morning in Rio. The extraordinary Jardim Botânico under the shadow of Corcovado, a final swim on Copacabana, and a long farewell lunch before departure. One last caipirinha for the road.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rio Botanical Garden (Jardim Botânico)',
              description: "Founded by Dom João VI in 1808, Rio's Botanical Garden is one of the most beautiful in the world — 140 hectares of Atlantic forest flora, with a stunning avenue of imperial palms, orchid greenhouses, Japanese garden, and the famous bromeliads collection. Christ the Redeemer watches over everything from the hill above.",
              details: [
                '🌿 Avenue of Royal Palms: 134 planted in 1809 — impossibly majestic',
                '🌸 Orchid greenhouse has 600+ species',
                '🦜 Free-roaming parrots, toucans, and sloths in the canopy',
                '🧘 The Japanese garden section is serene — perfect for slow morning reflection',
                '🎟️ Entry ~R$30 per person (~$6) — opens 8am'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Cine Café (inside Jardim Botânico)',
              description: "Beautiful open-air café inside the botanical garden with fresh fruit plates, tapioca, granola bowls, and excellent coffee. Eat surrounded by 200-year-old trees.",
              meta: '💰 $ · 📍 Inside Jardim Botânico · Vegetarian ✅'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Copacabana Beach & Boardwalk',
              description: "A final dip at Copacabana — the world's most famous beach. Walk the wave-pattern black and white mosaic boardwalk (inspired by Lisbon's Avenida), rent beach chairs and umbrellas, and take a last long swim in the Atlantic.",
              details: [
                '🏖️ Copacabana stretches 4km — go early, it fills up by 11am on weekends',
                '🍹 Beach kiosks serve fresh coconuts, caipirinhas, and mate leão',
                '📸 The Copacabana Palace hotel (white neoclassical facade) makes a beautiful backdrop',
                '🌊 Posto 2 area near the Forte de Copacabana is less crowded'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          meals: [
            {
              type: '🍽️ Farewell Lunch',
              name: 'Miam Miam',
              description: "A legendary Botafogo brunch and lunch spot — innovative Brazilian comfort food in a beautiful restored house. The brunch menu has stunning vegetarian options: açaí waffles, tropical fruit bowls, shakshuka with Brazilian herbs, and fresh-pressed juices alongside eggs and charcuterie for meat-eaters. A perfect farewell meal.",
              meta: '💰 $$$ · 📍 Rua General Goes Monteiro 34, Botafogo · Vegetarian-friendly ✅'
            }
          ],
          tips: [
            { type: 'tip', text: "Allow 3 hours before your flight departure to reach GIG (Galeão airport) — it's on the other side of the bay via the bridge, 45-60 minutes from the South Zone. Use Uber/99 and always have a buffer." }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9669, lng: -43.2224, label: 'Jardim Botânico', num: 1, cat: 'attraction', desc: 'World-class botanical garden — royal palms, orchids, sloths' },
        { lat: -22.9711, lng: -43.1858, label: 'Copacabana Beach', num: 2, cat: 'attraction', desc: "The world's most famous beach — final swim in the Atlantic" },
        { lat: -22.9871, lng: -43.1891, label: 'Forte de Copacabana', num: 3, cat: 'attraction', desc: 'Historic fort at the southern tip of Copacabana — great views' },
        { lat: -22.9550, lng: -43.1899, label: 'Miam Miam', num: 4, cat: 'food', desc: 'Farewell brunch in Botafogo — excellent vegetarian options' },
        { lat: -22.9028, lng: -43.1759, label: 'Confeitaria Colombo', num: 5, cat: 'food', desc: 'Optional final coffee at the Belle Époque landmark' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–150/night', midrange: '$150–300/night', luxury: '$300–600/night' },
    { category: 'Meals (per person)', budget: '$15–30/day', midrange: '$30–60/day', luxury: '$60–120/day' },
    { category: 'Transport', budget: '$15–25/day', midrange: '$25–50/day', luxury: '$60–120/day (private)' },
    { category: 'Activities', budget: '$0–40/day', midrange: '$40–100/day', luxury: '$100–250/day' },
    { category: 'Hang Gliding', budget: '$120pp', midrange: '$140pp', luxury: '$180pp (private)' },
    { category: '4-Night Total (4 people)', budget: '$1,000–1,500', midrange: '$1,500–2,500', luxury: '$3,000–5,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Galeão International Airport (GIG) — main international hub, north side of the bay', 'Santos Dumont Airport (SDU) — domestic flights, right in Centro', 'Uber from Galeão to Ipanema: ~45-60 min, ~R$80-120 ($15-25)', 'Avoid taxis at the airport — use Uber/99 for safety and transparency'] },
    { title: '🏨 Where to Stay', items: ['Ipanema: best location — beach, restaurants, nightlife (Pestana, Fasano, boutiques)', 'Leblon: quieter, upscale, great restaurant scene', 'Santa Teresa: bohemian charm, amazing views, slightly removed', 'Copacabana: central, famous beach, wide range of prices'] },
    { title: '🥦 Vegetarian Guide', items: ['Por kilo restaurants are everywhere — pay by weight, always has salads/beans/cooked veg', 'Tapioca (gluten-free crepe) is a staple street food — can be filled with cheese, vegetables, fruit', 'Acai bowls are ubiquitous — genuinely Brazilian and delicious', 'Moqueca de legumes (vegetable coconut curry) is a classic Brazilian vegetarian dish', 'Caldo verde (potato kale soup) and feijoada de legumes at traditional spots'] },
    { title: '🌡️ October Weather', items: ['Average 26-30°C (79-86°F)', 'Spring — mostly sunny, occasional afternoon showers (15-30 min)', 'Low season shoulder period — fewer tourists, better prices', 'Jungle trails are beautifully green', 'Pack light cotton, swimwear, and one light layer for evenings'] },
    { title: '💳 Money & Budget', items: ['Credit cards widely accepted in tourist areas', 'Always carry some Brazilian reais (R$) for street food, small vendors', 'ATMs are widely available — use Banco do Brasil or Bradesco to avoid high fees', 'Current rate: ~R$5 per $1 USD — Rio is very affordable for USD/EUR visitors', 'Tipping: 10% service charge added to most restaurant bills; not mandatory'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
