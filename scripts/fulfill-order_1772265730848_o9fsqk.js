const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772265730848_o9fsqk',
  email: 'doughobbs@hotmail.com',
  destination: 'Ipoh, Perak, Malaysia',
  startDate: '2026-03-20',
  endDate: '2026-03-24',
  groupSize: 2,
  requests: ''
};

const itineraryData = {
  destination: 'Ipoh, Malaysia',
  countryEmoji: '🇲🇾',
  title: 'The Foodie & Adventure Guide to Ipoh',
  subtitle: '4 nights of cave temples, colonial charm, legendary street food & jungle adventures for two',
  description: "Ipoh is Malaysia's best-kept secret — a laid-back city where colonial shophouses drip with bougainvillea, cave temples glow with incense, and every meal is a revelation. Famous for its white coffee, silky-smooth hor fun, and the most tender bean sprout chicken you'll ever taste, Ipoh rewards slow travellers who linger over kopi and wander down mural-lined alleyways. This itinerary blends cultural depth, outdoor adventure, and serious food exploration — all on a budget that won't break the bank.",
  duration: '4 nights',
  dates: 'Mar 20 – Mar 24, 2026',
  budget: '$',
  pace: 'Relaxed–Moderate',
  bestFor: 'Couples',
  highlights: [
    'Cave temples: Sam Poh Tong, Kek Lok Tong & Perak Tong',
    'Legendary Ipoh white coffee & Old Town dim sum breakfasts',
    'Bean sprout chicken — the dish Ipoh is famous for',
    "Kellie's Castle ruins & jungle adventures at Lost World of Tambun",
    'Street art & mural trails through colonial Ipoh Old Town'
  ],

  essentials: [
    { title: '☀️ March Weather', text: 'March is warm and humid — expect 30–34°C days with occasional afternoon showers. Light, breathable clothing is essential. Pack a small umbrella for brief tropical downpours that clear quickly.' },
    { title: '🚗 Getting Around', text: 'Ipoh is best explored by Grab (Southeast Asia\'s Uber). It\'s cheap and reliable — most rides in the city cost RM5–15 ($1–3 USD). Walking is great for Old Town. Rent a car for day trips to Kellie\'s Castle and Lost World of Tambun.' },
    { title: '🍜 Food Culture', text: "Ipoh's food scene is its biggest draw. Eat breakfast early (7–9am) at the old kopitiam coffee shops before they run out of the best dishes. Dim sum restaurants fill up by 8am on weekends. Go where the locals go — if there's a queue, it's worth the wait." },
    { title: '💰 Budget Tips', text: 'Ipoh is incredibly affordable. Street food meals cost RM8–15 ($2–4 USD) per person. Hotel rooms in Old Town start from RM80–150/night ($18–35 USD). Total budget for 2 people over 4 nights is very achievable under $1,000 USD.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-20',
      neighborhoods: 'Ipoh Old Town · Concubine Lane · Padang',
      title: 'Arrival & Old Town Immersion',
      description: "Arrive in Ipoh and dive straight into the colonial heart of the city. Wander Concubine Lane, get your first Ipoh white coffee, and explore the atmospheric shophouse streets as the golden afternoon light makes everything glow.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Ipoh Old Town Walk',
              description: "Settle into your hotel near Old Town, then head out to explore on foot. Ipoh's colonial core is compact and walkable — the grand Moorish-style railway station (nicknamed the 'Taj Mahal of Ipoh'), the Padang (town square), Town Hall, and heritage shophouses are all within a short stroll.",
              details: [
                '🏨 Stay in Old Town: M Boutique Hotel, Majestic Station Hotel, or Mango Tree Boutique',
                '🏛️ Ipoh Railway Station — stunning Moorish colonial architecture, built 1935',
                '🌳 Ipoh Padang (Town Hall Green) — colonial square ringed by heritage buildings',
                '📸 Best photo: FMS Bar & Restaurant opposite the station — classic Ipoh street scene'
              ]
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Concubine Lane & Mural Art Trail',
              description: "Concubine Lane (Lorong Panglima) is Ipoh's most famous alleyway — a narrow, vibrant lane of heritage shophouses selling local snacks, crafts, and quirky souvenirs. Nearby, the Mural Art's Lane (Lorong Belakang Greentown) features stunning street art murals. Follow the trail through the old town to discover local life and colonial architecture.",
              details: [
                '🛍️ Concubine Lane: try the local pomelo candy, dried fruits, and white coffee sachets',
                '🎨 Street art trail: murals along the back lanes of Old Town — free walking tour',
                '📸 The "Children Playing" murals capture Ipoh\'s nostalgic charm beautifully',
                '⏰ Best light for photos: late afternoon golden hour (5–6pm)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee & Snack',
              name: 'Ipoh White Coffee (Sin Yoon Loong or Nam Heong)',
              description: "Your first Ipoh white coffee experience — these legendary old kopitiam (coffee shops) have been roasting beans with palm oil margarine for decades, creating a uniquely smooth, aromatic brew. Order kaya toast on the side.",
              meta: '💰 $ · 📍 Sin Yoon Loong: 15 Jalan Bandar Timah · RM3–5 per coffee'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kinta River Walk & Night Atmosphere',
              description: "Stroll along the Kinta River waterfront as Ipoh comes alive in the cool of the evening. The Heritage Walk trail passes illuminated colonial buildings and leads to the Birch Memorial Clock Tower — a beautiful Victorian-era landmark.",
              details: [
                '🌊 Kinta River Walk: a pleasant riverside promenade with views of the hills',
                '🕰️ Birch Memorial Clock Tower — Ipoh\'s most photogenic landmark at night',
                '🌙 The old town streets are lovely after dark — much quieter than daytime'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restoran Yong Suan (Bean Sprout Chicken)',
              description: "Your introduction to Ipoh's most famous dish — bean sprout chicken. Poached chicken served over silky smooth rice with bean sprouts that are uniquely crunchy due to Ipoh's limestone-filtered water. This is the dish that defines the city.",
              meta: '💰 $ · 📍 Near Old Town · RM12–18 per person · Order the half chicken + bean sprouts'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 4.5975, lng: 101.0901, label: 'Ipoh Railway Station', num: 1, cat: 'attraction', desc: 'Iconic Moorish colonial station — the Taj Mahal of Ipoh' },
        { lat: 4.5968, lng: 101.0862, label: 'Concubine Lane', num: 2, cat: 'attraction', desc: 'Famous heritage alleyway with snacks and souvenirs' },
        { lat: 4.5971, lng: 101.0871, label: 'Sin Yoon Loong Kopitiam', num: 3, cat: 'food', desc: 'Legendary Ipoh white coffee since the 1950s' },
        { lat: 4.5960, lng: 101.0890, label: 'Kinta River Walk', num: 4, cat: 'attraction', desc: 'Riverside promenade with colonial architecture views' },
        { lat: 4.5965, lng: 101.0878, label: 'Birch Memorial Clock Tower', num: 5, cat: 'attraction', desc: 'Victorian landmark — beautiful lit up at night' }
      ]
    },
    {
      num: 2,
      date: '2026-03-21',
      neighborhoods: 'Cave Temples · South Ipoh · Gunung Lang',
      title: 'Sacred Caves & Limestone Wonders',
      description: "Ipoh sits in a valley ringed by dramatic limestone karst hills, many of which hide extraordinary cave temples. Today is dedicated to exploring these spiritual wonders — ancient Buddhist shrines carved into living rock, serene gardens, and a hidden lake that reflects the world in perfect mirror image.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sam Poh Tong Cave Temple',
              description: "The most atmospheric cave temple in Ipoh — a working Buddhist shrine built into a massive limestone cavern. Wander through chambers filled with golden Buddhas and incense smoke, then emerge into a serene garden courtyard with a reflecting pool and resident tortoises. The turtle pond is a symbol of longevity.",
              details: [
                '🕌 Free entry · Open daily from 8am–5pm',
                '🐢 Turtle pond: hundreds of terrapins in the garden courtyard',
                '📿 Active place of worship — dress respectfully (shoulders + knees covered)',
                '📍 Gunung Rapat, South Ipoh — 10 min Grab from Old Town'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Breakfast',
              name: 'Foh San Dim Sum Restaurant',
              description: "Go early! Foh San is Ipoh's most famous dim sum restaurant — a cavernous, bustling hall serving dozens of dim sum varieties. The har gow (shrimp dumplings), char siu bao (BBQ pork buns), and egg tarts are exceptional. Go before 9am to avoid the queue.",
              meta: '💰 $ · 📍 51 Jalan Leong Sin Nam · Open 6am–1pm · RM15–25pp'
            }
          ]
        },
        {
          label: 'Mid-Morning',
          activities: [
            {
              title: 'Kek Lok Tong Cave Temple & Garden',
              description: "A short distance from Sam Poh Tong, Kek Lok Tong is arguably even more beautiful. The cave opens into an extraordinary natural garden — an open-air limestone valley with manicured gardens, Tai Chi practitioners at dawn, and a tranquil koi pond. The contrast between the dark cave interior and the lush garden beyond is breathtaking.",
              details: [
                '🌿 Free entry · Open 8am–6pm',
                '🧘 Locals practice Tai Chi in the garden every morning',
                '🐟 Beautiful koi pond in the natural limestone garden',
                '📸 The cave exit into the garden is one of the most photogenic spots in Ipoh'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Perak Tong Cave Temple',
              description: "The tallest cave temple in Ipoh — climb 385 steps through the limestone hill to reach a summit with panoramic views over the city and surrounding karst landscape. The cave itself houses a 12-metre-tall golden Buddha and thousands of murals and inscriptions left by Chinese scholars and artists over the decades.",
              details: [
                '🧗 385 steps to the summit — worth every one for the views',
                '🏔️ Panoramic view over Ipoh and the Kinta Valley from the top',
                '🎨 Ancient Chinese paintings and calligraphy throughout the cave',
                '📍 Jalan Kuala Kangsar, 6km north of Old Town — RM15 Grab ride'
              ]
            },
            {
              title: 'Gunung Lang Recreational Park',
              description: "Take a short boat ride across a lake surrounded by limestone cliffs to this peaceful park. Paddle around the karst formations, enjoy the lush gardens, and find a quiet bench to take in the dramatic scenery.",
              details: [
                '🚤 Boat ride: RM1 per person · Open Tue–Sun, 9am–5pm',
                '🦆 Deer park and animal enclosures inside',
                '🌊 The lake reflecting the limestone peaks is stunning on calm days'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Restoran Onn Kee (Bean Sprout Chicken)',
              description: "One of the most celebrated bean sprout chicken restaurants in all of Malaysia. The chicken is poached to perfection — silky, tender, and served over fragrant rice with a side of Ipoh bean sprouts that crunch like nowhere else.",
              meta: '💰 $ · 📍 Taman Canning · Best at lunch · RM12–18 per person'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gerbang Malam Night Market',
              description: "Ipoh's lively night market is a feast of hawker food — satay, grilled seafood, popiah (fresh spring rolls), rojak (fruit salad), and countless local snacks. Grab a plastic table under the stars and eat your way through the stalls.",
              meta: '💰 $ · 📍 Near Jalan Sultan Iskandar · Evenings only · RM20–30 total for two'
            }
          ],
          tips: [
            { type: 'tip', text: "Don't miss the cendol (shaved ice with pandan jelly and palm sugar) and the rojak (spicy fruit salad with shrimp paste) at the night market — iconic Malaysian desserts." }
          ]
        }
      ],
      mapPins: [
        { lat: 4.5522, lng: 101.0980, label: 'Sam Poh Tong', num: 1, cat: 'attraction', desc: 'Famous cave temple with turtle pond and garden' },
        { lat: 4.5543, lng: 101.0990, label: 'Kek Lok Tong', num: 2, cat: 'attraction', desc: 'Cave temple with stunning natural garden' },
        { lat: 4.6267, lng: 101.0928, label: 'Perak Tong', num: 3, cat: 'attraction', desc: '385 steps to panoramic karst views' },
        { lat: 4.6350, lng: 101.0880, label: 'Gunung Lang Park', num: 4, cat: 'attraction', desc: 'Limestone lake park with boat rides' },
        { lat: 4.5733, lng: 101.0827, label: 'Foh San Dim Sum', num: 5, cat: 'food', desc: "Ipoh's most famous dim sum restaurant" },
        { lat: 4.5870, lng: 101.0981, label: 'Restoran Onn Kee', num: 6, cat: 'food', desc: 'Legendary bean sprout chicken' }
      ]
    },
    {
      num: 3,
      date: '2026-03-22',
      neighborhoods: "Kellie's Castle · Lost World of Tambun · Tambun",
      title: "Adventure Day — Kellie's Castle & Lost World of Tambun",
      description: "An action-packed day of adventure and history. Begin with the haunting ruins of Kellie's Castle — a Scottish rubber planter's unfinished dream in the Perak jungle — then spend the afternoon splashing around at Lost World of Tambun, a natural hot spring theme park nestled among dramatic limestone cliffs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: "Kellie's Castle",
              description: "One of Malaysia's most atmospheric ruins — a five-storey Moorish-style mansion begun in 1915 by Scottish rubber baron William Kellie Smith, never completed after his death in 1926. The roofless ruin, draped in jungle vegetation, sits beside a Hindu shrine Smith built for his Tamil workers. Wander through the empty rooms and staircases imagining the colonial-era excess that never was.",
              details: [
                '🏰 Entry: RM5 per person · Open daily 9am–5pm',
                '👻 Known locally as haunted — ghost stories abound',
                '🕌 The Hindu temple Smith built for workers is still active and beautifully maintained',
                '📍 Batu Gajah, 20km south of Ipoh — RM35 Grab or rent a car'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Ipoh Hor Fun (Morning Kopitiam)',
              description: "Start your day with Ipoh's other culinary legend — hor fun. These flat rice noodles in a clear, delicate prawn or chicken broth are uniquely smooth thanks to the soft limestone water. Try it at any old kopitiam near your hotel.",
              meta: '💰 $ · 📍 Old Town kopitiam · RM8–12 per bowl · Best before 10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lost World of Tambun',
              description: "A full afternoon of fun at this unique theme park built around natural hot springs and limestone cliffs. Swim in the natural hot springs, ride the rapids, float down the lazy river, and explore the tiger valley and petting zoo. The backdrop of jungle and karst peaks makes this far more beautiful than your average water park.",
              details: [
                '🎢 Day admission: RM100–130 per person · Open 11am–6pm',
                '♨️ Natural hot spring pools (open until 11pm for evening visitors)',
                '🐯 Tiger Valley: rare Indochinese tigers on display',
                '🏊 Wave pool, lazy river, rapid ride — bring aqua shoes',
                '📍 Sunway City Ipoh, Tambun — 10km from Old Town'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hot Spring Soak (Night Session)',
              description: "After the water park action, upgrade to the evening hot spring session. The natural hot springs at Tambun are even more atmospheric at night — steam rising among the limestone formations under a sky full of stars. A perfect way to relax tired legs.",
              details: [
                '♨️ Evening hot spring admission: RM30–40 per person',
                '🌙 Open until 11pm — much quieter after 8pm',
                '🧖 Various mineral pools at different temperatures'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tambun Food Village / Ipoh Town Hawkers',
              description: "Head back to Ipoh for dinner at a hawker centre. Try nasi lemak (coconut rice with sambal), char kway teow (stir-fried flat noodles), or satay with peanut sauce — classic Malaysian hawker fare at honest prices.",
              meta: '💰 $ · 📍 Old Town hawker stalls · RM15–25 per person'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 4.4286, lng: 101.0581, label: "Kellie's Castle", num: 1, cat: 'attraction', desc: 'Haunting colonial ruins in the Perak jungle' },
        { lat: 4.5733, lng: 101.1281, label: 'Lost World of Tambun', num: 2, cat: 'attraction', desc: 'Hot spring theme park among limestone cliffs' },
        { lat: 4.5733, lng: 101.1281, label: 'Tambun Hot Springs', num: 3, cat: 'attraction', desc: 'Natural mineral hot springs — evening sessions available' },
        { lat: 4.5968, lng: 101.0862, label: 'Old Town Hawker Centre', num: 4, cat: 'food', desc: 'Ipoh hawker stalls — nasi lemak, char kway teow, satay' }
      ]
    },
    {
      num: 4,
      date: '2026-03-23',
      neighborhoods: 'Mirror Lake · Old Town · Little India · Market Lane',
      title: 'Hidden Lake, Street Art & Slow Farewell',
      description: "Your penultimate day is for savoring Ipoh at its most beautiful and unhurried. Visit the mysterious Mirror Lake hidden in a limestone cave, explore the street art scene, browse Market Lane, and end with a long, indulgent farewell dinner at one of Ipoh's best restaurants.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tasik Cermin (Mirror Lake)',
              description: "One of Ipoh's most magical hidden spots — a crystal-clear lake tucked inside a limestone cave system. The perfectly still water creates a mirror reflection of the cave ceiling and surrounding cliffs. Accessible only through a narrow limestone passage (bring a torch). It's a genuine wow moment.",
              details: [
                '🌊 Free entry · Open daily 9am–5pm',
                '🔦 Bring a torch/phone light — the passage is dark',
                '📸 The mirror reflection effect is best on calm, clear mornings',
                '📍 Gunung Rapat area — RM10–15 Grab from Old Town',
                '⚠️ Wear non-slip shoes — the rocks can be slippery'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Brunch',
              name: 'Canning Dim Sum (Weekend) or Kopitiam Breakfast',
              description: "If it's a weekend, Canning Garden's dim sum scene is legendary — bamboo steamers stacked high, strong Chinese tea, and a convivial weekend-morning atmosphere. On weekdays, seek out a traditional kopitiam for white coffee, half-boiled eggs, and kaya toast.",
              meta: '💰 $ · 📍 Canning Garden (weekend) or any Old Town kopitiam (weekday) · RM15–20pp'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Han Chin Pet Soo Museum',
              description: "Ipoh's most fascinating museum — the restored clubhouse of the Hakka miners' guild (the Kwong Siew Association), dating to the early 1900s. The tin mining era made Ipoh wealthy, and this beautifully curated museum tells that story through artifacts, opium paraphernalia, and period photographs.",
              details: [
                '🏛️ Admission: RM16pp · Open Tue–Sun, guided tours every hour',
                '📜 Fascinating history of Hakka Chinese tin miners and their secret societies',
                '🎭 One of the best small museums in Malaysia'
              ]
            },
            {
              title: 'Market Lane & Little India',
              description: "Browse Market Lane — a restored heritage market of old shophouses selling local produce, dried goods, and street food. Then wander through Ipoh's Little India, where the air is thick with incense, jasmine garlands, and the smell of freshly baked roti canai.",
              details: [
                '🛒 Market Lane: local produce, dried fruits, tofu, and traditional sweets',
                '🌺 Little India: Jalan Sultan Idris Shah — sari shops, banana leaf rice, flower stalls',
                '🍛 Stop for a banana leaf rice lunch if you\'re still hungry'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Restoran Lou Wong (Bean Sprout Chicken — the Original)',
              description: "The restaurant that made bean sprout chicken famous. Lou Wong (originally called Tauge Ayam) has been serving the city's most celebrated dish since the 1960s. A must-do final bean sprout chicken before you leave.",
              meta: '💰 $ · 📍 49 Jalan Yau Tet Shin · Open 10am–8pm · RM12–18 per person'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kong Heng Square & Rooftop Drinks',
              description: "Kong Heng is a beautifully restored heritage building in Old Town — think exposed brick, high ceilings, and a curated collection of shops and a courtyard bar. Have sundowners here before heading to Above Gastro Bar for Ipoh's best elevated cocktail experience.",
              details: [
                '🏚️ Kong Heng Square: heritage courtyard with boutiques and a craft beer bar',
                '🍹 Above Gastro Bar: rooftop views over Old Town, craft cocktails, and sharing plates',
                '🌆 Best time: arrive as the sun sets over the shophouse rooftops'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Burps & Giggles (Western-Asian fusion) or Restoran Yik Foong',
              description: "For a special farewell dinner, Burps & Giggles is Ipoh's most beloved independent restaurant — creative Western-Asian fusion in a charming heritage space. For something more local, Restoran Yik Foong serves excellent Cantonese seafood that the locals adore.",
              meta: '💰 $$–$$$ · 📍 Old Town area · Book ahead at Burps & Giggles · RM60–100 for two'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 4.5544, lng: 101.0989, label: 'Tasik Cermin (Mirror Lake)', num: 1, cat: 'attraction', desc: 'Hidden lake with stunning mirror reflections in a limestone cave' },
        { lat: 4.5965, lng: 101.0878, label: 'Han Chin Pet Soo Museum', num: 2, cat: 'attraction', desc: 'Fascinating Hakka miners museum in a restored clubhouse' },
        { lat: 4.5972, lng: 101.0850, label: 'Market Lane', num: 3, cat: 'attraction', desc: 'Heritage market with local produce and traditional food' },
        { lat: 4.5967, lng: 101.0858, label: 'Little India', num: 4, cat: 'attraction', desc: 'Vibrant Indian quarter with roti canai and banana leaf rice' },
        { lat: 4.5960, lng: 101.0862, label: "Lou Wong (Original Bean Sprout Chicken)", num: 5, cat: 'food', desc: 'The restaurant that invented Ipoh bean sprout chicken' },
        { lat: 4.5968, lng: 101.0855, label: 'Kong Heng Square', num: 6, cat: 'attraction', desc: 'Restored heritage courtyard with bars and boutiques' }
      ]
    },
    {
      num: 5,
      date: '2026-03-24',
      neighborhoods: 'Old Town · Ipoh Railway Station',
      title: 'Last Morning — Farewell Coffee & Departure',
      description: "A slow, lingering last morning in Ipoh. One final white coffee, a last stroll through the Old Town before it gets too hot, and a departure that will leave you already planning your return.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Old Town Wander & Souvenir Shopping',
              description: "Rise early for a final stroll through Ipoh Old Town before the heat sets in. The morning light on the colonial shophouses is magical. Pop into Concubine Lane for last-minute souvenirs — white coffee sachets, pomelo candy, and Ipoh-branded ceramics make perfect gifts.",
              details: [
                '☕ Last white coffee: try Nam Heong if you haven\'t been — a rival to Sin Yoon Loong',
                '🛍️ Souvenir picks: Old Town white coffee sachets, Tambun pomelo products, Ipoh ceramics',
                '🚂 Ipoh to KL by ETS train: 2–2.5hrs, trains every hour from ~RM35–55 per person',
                '🚌 Bus to KL TBS: 3hrs, from ~RM20 per person'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Farewell Breakfast',
              name: 'Nam Heong Ipoh White Coffee',
              description: "Ipoh's other legendary kopitiam — Nam Heong claims to have invented white coffee. Order a kopi-O (black), kopi (with condensed milk), or the famous white coffee, with crispy toast and half-boiled eggs. A perfect farewell.",
              meta: '💰 $ · 📍 2 Jalan Bandar Timah · Open from 7am · RM8–12 per person'
            }
          ],
          tips: [
            { type: 'tip', text: "Book your ETS train ticket in advance at ktmb.com.my — the popular departure times fill up, especially on weekends. The 10am and 12pm trains to KL Sentral are most convenient." }
          ]
        }
      ],
      mapPins: [
        { lat: 4.5972, lng: 101.0871, label: 'Nam Heong Kopitiam', num: 1, cat: 'food', desc: 'The original Ipoh white coffee — perfect farewell breakfast' },
        { lat: 4.5975, lng: 101.0901, label: 'Ipoh Railway Station', num: 2, cat: 'attraction', desc: 'Depart by ETS train to Kuala Lumpur (2–2.5 hrs)' },
        { lat: 4.5968, lng: 101.0862, label: 'Concubine Lane', num: 3, cat: 'attraction', desc: 'Last-minute souvenirs — coffee sachets and pomelo candy' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (2 people)', budget: 'RM80–150/night ($19–35)', midrange: 'RM150–300/night ($35–70)', luxury: 'RM300–600/night ($70–140)' },
    { category: 'Meals (per couple/day)', budget: 'RM40–80/day ($10–19)', midrange: 'RM80–150/day ($19–35)', luxury: 'RM150–300/day ($35–70)' },
    { category: 'Transport (Grab/day)', budget: 'RM20–50/day ($5–12)', midrange: 'RM50–120/day ($12–28)', luxury: 'RM150–300/day (private car)' },
    { category: 'Cave Temples', budget: 'Free–RM5pp', midrange: 'Free–RM5pp', luxury: 'Free–RM5pp' },
    { category: "Kellie's Castle", budget: 'RM5pp', midrange: 'RM5pp', luxury: 'RM5pp' },
    { category: 'Lost World of Tambun', budget: 'RM100–130pp', midrange: 'RM100–130pp', luxury: 'RM150 (VIP)' },
    { category: '4-Night Total (couple)', budget: '$350–550 USD', midrange: '$550–800 USD', luxury: '$800–1,200 USD' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Ipoh has a small airport (IPH) with flights from KL and Singapore', 'Best option: ETS train from KL Sentral — 2–2.5 hours, from RM35pp', 'Book at ktmb.com.my — popular trains sell out on weekends', 'Bus from KL TBS is cheapest (RM20) — 3 hours to Amanjaya Bus Station'] },
    { title: '🏨 Where to Stay', items: ['Stay in or near Old Town for walkability to food and attractions', 'M Boutique Hotel — quirky colonial-style boutique, great value', 'Majestic Station Hotel — grand heritage hotel inside the railway station', 'Mango Tree Boutique — budget-friendly Old Town option', 'WEIL Hotel — modern 5-star if you want to splurge'] },
    { title: '🌡️ March Weather', items: ['Temperatures: 30–34°C (86–93°F) days, around 25°C nights', 'High humidity — lightweight, breathable clothing only', 'Afternoon showers are common but brief — carry a compact umbrella', 'The limestone hills create shade pockets — plan cave visits for midday'] },
    { title: '💰 Money & Payments', items: ['Currency: Malaysian Ringgit (MYR) — RM4.3 ≈ $1 USD (check current rate)', 'Cash is king at hawker stalls and old kopitiam — ATMs widely available', 'Most hotels and newer restaurants accept cards', 'Grab (taxi app) works everywhere — set up before arrival'] },
    { title: '🍜 Food Tips', items: ['Eat where locals eat — long queues mean quality', 'Must-tries: white coffee, bean sprout chicken, hor fun, dim sum, cendol', "Ipoh's bean sprouts are uniquely crunchy because of the limestone-filtered water", 'Early breakfast (7–9am) is the best food time — many places close by noon', 'Download Grab Food for delivery to your hotel if you want a rest day'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
