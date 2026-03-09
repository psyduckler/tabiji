const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773032068878_y7gz3o',
  email: 'c13.bako@gmail.com',
  destination: 'Tbilisi, Georgia',
  startDate: '2026-03-27',
  endDate: '2026-04-03',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Tbilisi, Georgia',
  countryEmoji: '🇬🇪',
  title: 'Solo Through the Cradle of Wine & Hospitality',
  subtitle: '8 days of ancient fortresses, sulfur baths, khinkali feasts & Caucasus adventures',
  description: "Georgia is one of those places that rewires your understanding of hospitality, food, and wine. Tbilisi — a city draped over hills and carved by the Mtkvari River — is chaotic, beautiful, and absurdly affordable. This itinerary is built for a solo adventurer who wants to eat khinkali until they lose count, soak in sulfur baths under brick domes, hike to churches perched on impossible ridges, and drink qvevri wine in candlelit cellars. From the cobblestone lanes of Old Town to the snow-dusted peaks of Kazbegi, this is 8 days of the real Georgia — no tour bus required.",
  duration: '8 Days',
  dates: 'Mar 27 – Apr 3, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Solo Adventurers · Foodies · Culture Seekers',
  highlights: [
    'Soak in centuries-old sulfur baths in Abanotubani',
    'Hike to Gergeti Trinity Church with Mt. Kazbegi as backdrop',
    'Feast on khinkali at legendary local joints like Pasanauri & Zakhar Zakharich',
    'Explore 8,000 years of winemaking at natural wine bars & qvevri cellars',
    'Wander the cobblestone lanes of Old Town & Narikala Fortress',
    'Day trip to Mtskheta — Georgia\'s ancient capital & UNESCO World Heritage Site',
    'Browse Soviet relics at the Dry Bridge Flea Market',
    'Discover Tbilisi\'s creative scene at Fabrika & the Stamba district',
    'Taste churchkhela, fresh bread from tone ovens & street-side mtsvadi',
    'Cross the futuristic Bridge of Peace at golden hour'
  ],

  essentials: [
    { title: '💰 Budget Paradise', text: 'Georgia is extraordinarily affordable. Expect $30-50 USD/day covering hostel dorms ($5-12), full meals ($3-8), metro rides ($0.20), and wine by the glass ($2-4). Your $1,000 budget gives you 8 days of luxury by Georgian standards — private rooms, sit-down restaurants, day trips included.' },
    { title: '🍷 Wine Country', text: 'Georgia has 8,000 years of winemaking history — the oldest in the world. Qvevri (clay vessel) wines are UNESCO-recognized. Key grapes: Saperavi (bold red), Rkatsiteli (amber/white), Kisi, Mtsvane. Natural wine is the norm here, not the exception. Many bars offer tastings for $5-10.' },
    { title: '🚇 Getting Around', text: 'Tbilisi metro is fast, clean, and costs 1 GEL ($0.35). Two lines cover the city center. Bolt/Yandex taxis are dirt cheap ($1-3 for most rides). Marshrutkas (minibuses) go everywhere including day trips. The city center is very walkable but hilly — wear good shoes.' },
    { title: '🗣️ Language & Safety', text: 'Georgian script looks alien but younger locals speak English well, especially in the tourist areas. Learn "gamarjoba" (hello) and "madloba" (thank you). Tbilisi is extremely safe for solo travelers — even walking alone at night. Georgians are famously hospitable and will invite you to eat with them.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-27',
      neighborhoods: 'Old Town · Abanotubani · Narikala',
      title: 'Arrival — Old Town, Sulfur Baths & First Khinkali',
      description: "Land in Tbilisi and dive straight into the soul of the city. The Old Town is a maze of leaning wooden balconies, crumbling churches, and winding lanes that feel like they haven't changed in centuries. End the day with a sulfur bath soak — Tbilisi was literally founded because a king's hawk fell into a hot spring.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Old Town Wander',
              description: "Drop your bags at Fabrika Hostel (the social hub for solo travelers) or a guesthouse in Sololaki, then head straight to Old Town. Walk from Freedom Square down into the narrow streets — every turn reveals painted balconies, hidden courtyards, and tone ovens baking fresh shotis puri (bread).",
              details: [
                '🏨 Fabrika Hostel — converted Soviet sewing factory, incredible courtyard, $8-12/dorm',
                '🗺️ Freedom Square is the starting point for Old Town exploration',
                '🍞 Buy hot shotis puri straight from a tone oven for 1 GEL ($0.35)'
              ]
            },
            {
              title: 'Legvtakhevi Waterfall & Canyon',
              description: "Yes, there's a waterfall in the middle of the city. Walk down through the sulfur bath district to find Legvtakhevi — a hidden gorge with a small waterfall tucked behind the bath houses. It's surreal and beautiful.",
              details: [
                '💧 Free to visit — follow the path behind the sulfur baths',
                '📸 The canyon is narrow and photogenic, especially in afternoon light',
                '🌿 Small café at the top of the gorge for a breather'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Dinner',
              name: 'Pasanauri',
              description: "Your first khinkali experience should be here. Pasanauri is a beloved chain that does one thing perfectly — Georgian dumplings. Order beef-and-pork khinkali (the classic), some khachapuri, and a cold Natakhtari beer. Eat with your hands — twist the top knob, bite, slurp the broth, eat the dumpling, leave the knob on the plate.",
              meta: '💰 $ · 📍 Multiple locations · ~₾8-12 for a feast'
            }
          ],
          tips: [
            { type: 'tip', text: "Don't eat the top knob of the khinkali — it's just a handle. Leave them on your plate so the server can count how many you ate. Locals consider eating the knob a rookie move." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sulfur Baths in Abanotubani',
              description: "The sulfur baths are Tbilisi's founding legend and an essential experience. Book a private room at Bathhouse No. 5 or Royal Bath House — you get a domed brick room with a hot sulfur pool and an optional kisi scrub (exfoliation massage). The water is 40-45°C and smells of sulfur — you'll come out feeling reborn.",
              details: [
                '♨️ Private room: 50-80 GEL ($18-30) for 1 hour — worth every lari',
                '🧖 Kisi scrub: 20-30 GEL extra — they scrub layers of dead skin off you',
                '🕐 Evening is the best time — fewer crowds, atmospheric lighting',
                '🏛️ The brick domed roofs of the bath houses are a Tbilisi icon'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.6934, lng: 44.8015, label: 'Freedom Square', num: 1, cat: 'attraction', desc: 'Central square and gateway to Old Town' },
        { lat: 41.6886, lng: 44.8093, label: 'Old Town (Kala)', num: 2, cat: 'attraction', desc: 'Historic heart of Tbilisi — wooden balconies and winding lanes' },
        { lat: 41.6871, lng: 44.8107, label: 'Legvtakhevi Waterfall', num: 3, cat: 'attraction', desc: 'Hidden waterfall and canyon in the city center' },
        { lat: 41.6860, lng: 44.8098, label: 'Abanotubani Sulfur Baths', num: 4, cat: 'attraction', desc: 'Historic sulfur bath district with brick-domed bathhouses' },
        { lat: 41.6862, lng: 44.8105, label: 'Bathhouse No. 5', num: 5, cat: 'attraction', desc: 'Best-value sulfur bath — private rooms with kisi scrub' },
        { lat: 41.6920, lng: 44.8050, label: 'Pasanauri', num: 6, cat: 'food', desc: 'Legendary khinkali restaurant — the essential first meal' },
        { lat: 41.6952, lng: 44.7898, label: 'Fabrika Hostel', num: 7, cat: 'hotel', desc: 'Converted Soviet factory — best social hostel in Tbilisi' }
      ]
    },
    {
      num: 2,
      date: '2026-03-28',
      neighborhoods: 'Narikala · Sololaki · Botanical Garden · Rustaveli',
      title: 'Fortress Views, Art & Rustaveli Avenue',
      description: "Today is all about Tbilisi's layers — climb ancient fortress walls for panoramic views, wander through the National Botanical Garden's hidden trails, then walk the grand Rustaveli Avenue like a local. The contrast between medieval ruins and buzzing modern life is what makes this city magic.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cable Car to Narikala Fortress',
              description: "Take the cable car from Rike Park over the river to Narikala Fortress — the ancient citadel that's watched over Tbilisi since the 4th century. Scramble along the crumbling walls for 360° views of the city, the river, and the mountains beyond. The Mother of Georgia statue stands nearby, sword and wine cup in hand.",
              details: [
                '🚡 Cable car: 2.5 GEL ($0.90) each way — pay with metro card',
                '🏰 The fortress ruins are free to explore — wear sturdy shoes',
                '📸 Best photo spots: the eastern wall for Old Town views, the western wall for river views',
                '⛪ St. Nicholas Church inside the fortress — restored with vivid frescoes'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tone Bakery (street-side)',
              description: "Start like a local — grab a fresh shotis puri or lobiani (bean-filled bread) from any tone oven bakery in Old Town. Pair with a strong Turkish-style coffee from a nearby café. Total cost: under $2.",
              meta: '💰 $ · 📍 Throughout Old Town · Grab-and-go'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'National Botanical Garden',
              description: "Enter from the fortress side and descend into the surprisingly lush Botanical Garden — 128 hectares of trails, bridges, and a waterfall. It feels like escaping the city entirely. The paths wind through bamboo groves, rose gardens, and ancient tree canopies.",
              details: [
                '🌿 Entry: 4 GEL ($1.50) — open daily',
                '💧 The garden waterfall is worth the walk to the lower levels',
                '🗺️ Allow 1.5-2 hours for a proper wander'
              ]
            },
            {
              title: 'Sololaki Neighborhood Walk',
              description: "Descend back into the city through Sololaki — Tbilisi's most photogenic residential neighborhood. Look for the famous Kaleidoscope House (a building covered in colorful tiles), leaning wooden balconies draped in vines, and hidden courtyards.",
              details: [
                '🏘️ Sololaki streets between Narikala and Freedom Square are pure gold',
                '📸 The Kaleidoscope House is on Besiki Street',
                '🐈 Tbilisi is full of friendly cats — Sololaki especially'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Keto & Kote',
              description: "A local favorite in Sololaki serving excellent traditional Georgian food in a cozy setting. Try the adjarian khachapuri (boat-shaped with egg and butter), badrijani nigvzit (eggplant with walnut paste), and a glass of house wine.",
              meta: '💰 $$ · 📍 3 Zandukeli St, Sololaki · Book ahead on weekends'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Rustaveli Avenue & National Museum',
              description: "Walk the full length of Rustaveli Avenue — Tbilisi's grand boulevard lined with plane trees, theaters, and Soviet-era buildings. Stop at the Georgian National Museum (Rustaveli Ave 3) for the Gold Treasury — Colchian gold jewelry from 3,000+ years ago. Finish at the Opera House.",
              details: [
                '🏛️ National Museum: 15 GEL ($5.50) — the Gold Treasury is mesmerizing',
                '🎭 Rustaveli Theatre and Opera House are architectural landmarks',
                '🛍️ Book shops and wine stores line the avenue'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Vino Underground',
              description: "Tbilisi's original natural wine bar, located in a basement near Freedom Square. They represent a collective of small Georgian winemakers producing qvevri wines. Order a four-wine tasting flight and a cheese plate. This is where you fall in love with Georgian wine.",
              meta: '💰 $$ · 📍 15 Galaktion Tabidze St · Tasting flights ~₾15-20'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.6907, lng: 44.8089, label: 'Rike Park (Cable Car)', num: 1, cat: 'attraction', desc: 'Riverside park — catch the cable car to Narikala' },
        { lat: 41.6876, lng: 44.8082, label: 'Narikala Fortress', num: 2, cat: 'attraction', desc: '4th-century fortress with panoramic city views' },
        { lat: 41.6869, lng: 44.8069, label: 'Mother of Georgia (Kartlis Deda)', num: 3, cat: 'attraction', desc: '20m aluminum statue — sword for enemies, wine for friends' },
        { lat: 41.6838, lng: 44.8065, label: 'National Botanical Garden', num: 4, cat: 'attraction', desc: '128 hectares of trails, bridges and a waterfall' },
        { lat: 41.6905, lng: 44.8035, label: 'Sololaki / Kaleidoscope House', num: 5, cat: 'attraction', desc: 'Photogenic neighborhood with the famous tiled building' },
        { lat: 41.6906, lng: 44.8048, label: 'Keto & Kote', num: 6, cat: 'food', desc: 'Beloved local Georgian restaurant in Sololaki' },
        { lat: 41.6973, lng: 44.7990, label: 'Rustaveli Avenue', num: 7, cat: 'attraction', desc: 'Grand boulevard — museums, theaters, tree-lined walks' },
        { lat: 41.6970, lng: 44.7988, label: 'Georgian National Museum', num: 8, cat: 'attraction', desc: 'Ancient Colchian gold and Georgian history' },
        { lat: 41.6940, lng: 44.8020, label: 'Vino Underground', num: 9, cat: 'food', desc: 'Original natural wine bar — qvevri wine collective' }
      ]
    },
    {
      num: 3,
      date: '2026-03-29',
      neighborhoods: 'Mtskheta (Day Trip) · Dry Bridge',
      title: "Mtskheta — Georgia's Sacred Ancient Capital",
      description: "A half-day trip to Mtskheta — Georgia's ancient capital and a UNESCO World Heritage Site just 30 minutes from Tbilisi. Two of the country's most important churches sit here: the hilltop Jvari Monastery (with jaw-dropping river confluence views) and the massive Svetitskhoveli Cathedral. Back in Tbilisi by afternoon for markets and street food.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Marshrutka to Mtskheta',
              description: "Catch a marshrutka (minibus) from Didube station to Mtskheta — they leave every 15-20 minutes and cost 1.5 GEL ($0.55). The ride is 20-30 minutes. Or take a Bolt taxi for about 15-20 GEL ($6).",
              details: [
                '🚐 Marshrutkas from Didube Bus Station — frequent and cheap',
                '⏰ Leave by 9am to beat tour groups at Jvari',
                '🗺️ Mtskheta is tiny — walkable in an afternoon'
              ]
            },
            {
              title: 'Jvari Monastery',
              description: "Perched on a cliff above the confluence of the Mtkvari and Aragvi rivers, Jvari Monastery is one of the most photographed places in Georgia. The 6th-century church is austere and powerful, and the views of the two rivers meeting below are stunning. Getting there requires a taxi from Mtskheta town (10-15 GEL round trip) as it's on a hilltop with no public transport.",
              details: [
                '⛪ 6th-century Georgian Orthodox monastery — UNESCO World Heritage',
                '📸 The river confluence view is Georgia\'s most iconic panorama',
                '🚕 Share a taxi from Mtskheta center — negotiate round trip with 20 min wait'
              ]
            },
            {
              title: 'Svetitskhoveli Cathedral',
              description: "Back in Mtskheta town, visit Svetitskhoveli — the largest historical church in Georgia and the spiritual heart of Georgian Christianity. Built in the 11th century, it's said to house Christ's robe. The interior frescoes and towering stone columns are breathtaking.",
              details: [
                '⛪ Free entry — dress modestly (headscarves for women at the door)',
                '🏛️ The cathedral courtyard has excellent views of the surrounding mountains',
                '📜 Georgia adopted Christianity in 337 AD — one of the first nations to do so'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Restaurant in Mtskheta Old Town',
              description: "Mtskheta's cobblestone main street has several excellent family-run restaurants. Try mtsvadi (grilled pork skewers) fresh off the mangal, paired with tkemali (sour plum sauce) and a cold Kazbegi beer. Sit in a garden courtyard with mountain views.",
              meta: '💰 $ · 📍 Mtskheta main street · ₾10-15 for a full meal'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dry Bridge Flea Market',
              description: "Back in Tbilisi, head to the Dry Bridge Market — a sprawling open-air flea market where vendors sell Soviet-era memorabilia, antique daggers, old paintings, vinyl records, and all manner of curious treasures. It's a treasure hunt and a history lesson in one.",
              details: [
                '🕰️ Open daily but best on weekends — busiest 11am-3pm',
                '🎖️ Soviet medals, Georgian drinking horns, old cameras, vintage jewelry',
                '💬 Haggle respectfully — prices are already low but there\'s always room'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shavi Lomi',
              description: "One of Tbilisi's most acclaimed restaurants — modern Georgian cuisine in a quirky, art-filled space. Chef-driven dishes that riff on traditional flavors. Try the walnut-crusted trout, smoked sulguni cheese, and whatever seasonal special they're running. Great wine list too.",
              meta: '💰 $$ · 📍 28 Zubalashvili St · Book ahead — popular with locals'
            }
          ],
          tips: [
            { type: 'tip', text: "At Mtskheta, both Jvari and Svetitskhoveli are active religious sites. Dress respectfully — no shorts, cover shoulders. Women should cover their heads inside churches (scarves available at entrance)." }
          ]
        }
      ],
      mapPins: [
        { lat: 41.7073, lng: 44.8150, label: 'Didube Bus Station', num: 1, cat: 'transport', desc: 'Marshrutka departure point for Mtskheta' },
        { lat: 41.8381, lng: 44.7263, label: 'Jvari Monastery', num: 2, cat: 'attraction', desc: '6th-century hilltop monastery — iconic river confluence views' },
        { lat: 41.8426, lng: 44.7206, label: 'Svetitskhoveli Cathedral', num: 3, cat: 'attraction', desc: "Georgia's largest historic church — houses Christ's robe" },
        { lat: 41.8430, lng: 44.7200, label: 'Mtskheta Old Town', num: 4, cat: 'attraction', desc: 'UNESCO ancient capital with cobblestone streets' },
        { lat: 41.6988, lng: 44.8025, label: 'Dry Bridge Flea Market', num: 5, cat: 'attraction', desc: 'Open-air market with Soviet relics and antiques' },
        { lat: 41.6980, lng: 44.8128, label: 'Shavi Lomi', num: 6, cat: 'food', desc: 'Modern Georgian cuisine in an arty, eclectic space' }
      ]
    },
    {
      num: 4,
      date: '2026-03-30',
      neighborhoods: 'Kazbegi · Georgian Military Highway',
      title: 'Kazbegi — Gergeti Trinity Church & the Great Caucasus',
      description: "The adventure day. Drive the Georgian Military Highway — one of the world's most dramatic roads — through river gorges, past the medieval Ananuri fortress, up through ski-resort Gudauri, and into the shadow of Mt. Kazbegi (5,047m). Then hike to Gergeti Trinity Church, floating above the clouds on its ridge. This is the Georgia you see in dreams.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Georgian Military Highway Drive',
              description: "Book a shared tour ($25-35) or hire a private driver ($60-80 for the day) and head north on the Georgian Military Highway. The road itself is the attraction — it climbs through the Aragvi valley past the stunning Ananuri fortress complex (stop for photos), the Gudauri viewpoint, and over the Jvari Pass at 2,395m.",
              details: [
                '🚗 Leave Tbilisi by 7-8am — the drive to Stepantsminda is ~3 hours',
                '🏰 Ananuri Fortress stop — medieval castle on a reservoir, incredibly photogenic',
                '🏔️ Gudauri Friendship Monument — Soviet-era panoramic viewpoint mosaic',
                '⚠️ Late March may have some snow on the pass — roads are usually clear'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hike to Gergeti Trinity Church',
              description: "From Stepantsminda (Kazbegi town), hike up to Gergeti Trinity Church — a 14th-century stone church perched at 2,170m with Mt. Kazbegi towering behind it. The hike is steep but straightforward (3-4km, ~1.5 hours up). Or take a 4x4 jeep up for 50-60 GEL round trip.",
              details: [
                '🥾 Hike: ~1.5 hours up, 1 hour down — moderate difficulty',
                '🚙 4x4 jeep from town square: 50-60 GEL round trip (common option)',
                '📸 If the weather is clear, Mt. Kazbegi fills the entire background',
                '🧥 It\'s significantly colder up here — bring layers even if Tbilisi is warm'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Café in Stepantsminda',
              description: "Warm up with khinkali and a bowl of kharcho (spicy beef soup with walnuts and rice) at one of the small restaurants in town. The mountain air makes everything taste better.",
              meta: '💰 $ · 📍 Stepantsminda main square · ₾8-12'
            }
          ],
          tips: [
            { type: 'tip', text: "Check weather before committing — if clouds are low, Kazbegi won't reward you visually. Most drivers/tours will let you reschedule. Clear mornings are best. Late March is shoulder season — fewer tourists but unpredictable weather." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Tbilisi & Wine',
              description: "Drive back to Tbilisi (arrive ~7-8pm) and decompress with wine. Head to 8000 Vintages — a wine bar and shop named after Georgia's 8,000 years of winemaking history. They have the largest selection of Georgian wines in one place.",
              details: [
                '🍷 8000 Vintages has 800+ wines — ask for a guided tasting',
                '📍 Located on Chardin Street near Meidan Square',
                '💰 Tastings from ₾15 — bottles from ₾12 to take home'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.1625, lng: 44.7028, label: 'Ananuri Fortress', num: 1, cat: 'attraction', desc: 'Medieval castle complex on Aragvi reservoir' },
        { lat: 42.4582, lng: 44.4735, label: 'Gudauri Friendship Monument', num: 2, cat: 'attraction', desc: 'Soviet panoramic viewpoint mosaic at 2,300m' },
        { lat: 42.6567, lng: 44.6381, label: 'Stepantsminda (Kazbegi)', num: 3, cat: 'attraction', desc: 'Mountain town at the foot of Mt. Kazbegi' },
        { lat: 42.6624, lng: 44.6199, label: 'Gergeti Trinity Church', num: 4, cat: 'attraction', desc: "14th-century church at 2,170m — Georgia's most iconic view" },
        { lat: 42.6901, lng: 44.5174, label: 'Mt. Kazbegi (5,047m)', num: 5, cat: 'attraction', desc: 'Third-highest peak in Georgia — dramatic Caucasus backdrop' },
        { lat: 41.6912, lng: 44.8080, label: '8000 Vintages', num: 6, cat: 'food', desc: '800+ Georgian wines — the ultimate tasting room' }
      ]
    },
    {
      num: 5,
      date: '2026-03-31',
      neighborhoods: 'Marjanishvili · Agmashenebeli · Dezerter Bazaar',
      title: 'Markets, Street Food & the Left Bank',
      description: "Rest day after yesterday's Kazbegi adventure. Explore Tbilisi's left bank — the less-touristy side of the river where locals shop, eat, and hang out. Hit the massive Dezerter Bazaar for sensory overload, stroll the renovated Agmashenebeli Avenue, and dive into the food scene.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dezerter Bazaar',
              description: "Tbilisi's biggest and most chaotic market — a covered bazaar where locals buy everything from spices and cheese to churchkhela and fresh herbs. Vendors will offer you samples of sulguni cheese, spice blends, dried fruits, and homemade tkemali sauce.",
              details: [
                '🧀 Try sulguni (stretchy Georgian cheese) — buy from vendors who let you taste first',
                '🍬 Churchkhela — candle-shaped walnut-and-grape snacks — the original Georgian energy bar',
                '🌶️ Buy a bag of khmeli suneli (Georgian spice blend) — essential souvenir',
                '⏰ Go early (9-11am) for the best energy and selection'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Entrée Café',
              description: "Popular brunch spot near Marjanishvili Square. Great coffee, eggs, and pastries in a modern space.",
              meta: '💰 $ · 📍 Marjanishvili area · Coffee + pastry from ₾8'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Agmashenebeli Avenue Stroll',
              description: "The left bank's grand avenue — recently renovated with beautiful neo-classical facades, wine bars, and local restaurants. Less touristy than Rustaveli, more authentic.",
              details: [
                '🏛️ Beautiful 19th-century architecture — recently restored',
                '🍷 Several wine bars line the avenue — Amber Bar is a standout for qvevri wines',
                '🚇 Marjanishvili metro station is the hub for this area'
              ]
            },
            {
              title: 'Cooking Class or Food Tour',
              description: "Join a Georgian cooking class — learn to make khinkali from scratch, fold khachapuri, and prepare pkhali (walnut-herb paste). Several operators run half-day classes for $25-40 including a feast of everything you cook. Best solo activity — eat with other travelers.",
              details: [
                '👨‍🍳 Gastronaut offers popular small-group classes in English',
                '🥟 You will make and eat 20+ khinkali — come hungry',
                '🍷 Most classes include wine pairing',
                '📱 Book via GetYourGuide or direct — fills up fast'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Zakhar Zakharich',
              description: "A hidden gem for khinkali purists. Hand-mixed dough, meat khinkali bursting with broth. Hard to find — down a nondescript alley — but that's part of the charm. Order 10 khinkali and a beer. Total damage: under $5.",
              meta: '💰 $ · 📍 Near Marjanishvili · Ask locals for directions'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Bridge of Peace at Golden Hour',
              description: "Walk across the Bridge of Peace — Tbilisi's futuristic glass-and-steel pedestrian bridge designed by Michele De Lucchi. It connects the Old Town to Rike Park and looks stunning at sunset when the LED lights begin to pulse.",
              details: [
                '🌉 The bridge lights up with changing LED patterns after dark',
                '📸 Best photographed from Metekhi Church hill or from the Old Town side',
                '🚶 Connect this with an evening walk through Rike Park'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Poliphonia Natural Wine Bar',
              description: "A cozy wine bar focused purely on natural Georgian wines. Intimate space, knowledgeable staff, and a carefully curated list of small-producer wines. Pair with a cheese and charcuterie board. Great solo bar — you'll chat with the staff and other wine lovers.",
              meta: '💰 $$ · 📍 Leselidze St, Old Town · Open evenings'
            }
          ],
          tips: [
            { type: 'tip', text: "Late March in Tbilisi is spring — expect 10-18°C, occasional rain, and trees starting to blossom. Layer up in the morning, shed layers by afternoon. Perfect walking weather." }
          ]
        }
      ],
      mapPins: [
        { lat: 41.7155, lng: 44.7985, label: 'Dezerter Bazaar', num: 1, cat: 'attraction', desc: "Tbilisi's biggest local market — spices, cheese, churchkhela" },
        { lat: 41.7092, lng: 44.7973, label: 'Marjanishvili Square', num: 2, cat: 'attraction', desc: 'Left bank hub — metro, cafes, local restaurants' },
        { lat: 41.7068, lng: 44.7958, label: 'Agmashenebeli Avenue', num: 3, cat: 'attraction', desc: 'Grand renovated avenue with wine bars and architecture' },
        { lat: 41.7060, lng: 44.7950, label: 'Amber Bar', num: 4, cat: 'food', desc: 'Qvevri wine bar on Agmashenebeli Avenue' },
        { lat: 41.7100, lng: 44.7965, label: 'Zakhar Zakharich', num: 5, cat: 'food', desc: 'Hidden gem for hand-mixed khinkali' },
        { lat: 41.6924, lng: 44.8088, label: 'Bridge of Peace', num: 6, cat: 'attraction', desc: 'Futuristic glass pedestrian bridge — stunning at sunset' },
        { lat: 41.6920, lng: 44.8055, label: 'Poliphonia Natural Wine', num: 7, cat: 'food', desc: 'Intimate natural wine bar in Old Town' }
      ]
    },
    {
      num: 6,
      date: '2026-04-01',
      neighborhoods: 'Stamba · Vera · Vake',
      title: 'Creative Tbilisi — Art, Coffee & Hidden Neighborhoods',
      description: "Discover the Tbilisi that locals love — the creative quarter around Stamba and Rooms Hotels, the leafy residential streets of Vera, and the upscale parks of Vake. This is where you see the city's future alongside its past — coworking cafes, gallery spaces, and the best third-wave coffee in the Caucasus.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Stamba District & Rooms Hotel',
              description: "The area around Stamba Hotel (a converted Soviet-era printing house) and Rooms Hotel has become Tbilisi's creative district. Walk through the lobbies, browse the shops, and soak up the design-forward atmosphere. The Stamba lobby is a stunning industrial-chic space open to all.",
              details: [
                '🏨 Stamba Hotel lobby — industrial-chic with a massive atrium and bookshop',
                '📚 Rooms Hotel bar — the place to be seen in Tbilisi',
                '🎨 Several galleries and design shops in the surrounding blocks'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Stamba Cafe',
              description: "Excellent third-wave coffee in the Stamba Hotel space. Soaring ceilings, industrial beams, creative types on laptops. Good pastries and brunch options.",
              meta: '💰 $$ · 📍 14 Merab Kostava St · Great for solo working'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Vera Neighborhood Walk',
              description: "Vera is Tbilisi's bohemian residential neighborhood — quiet, leafy streets, art nouveau buildings, independent cafes, and local wine bars. It's where young Tbilisians live and hang out. Walk from Stamba through Vera's winding streets to Vake Park.",
              details: [
                '🏘️ Look for the colorful balconies and ivy-covered buildings',
                '☕ Independent cafes dot the area — coffee is excellent everywhere in Tbilisi',
                '🎵 Vera has a live music scene — check for evening events'
              ]
            },
            {
              title: 'Vake Park & Chronicle of Georgia',
              description: "Tbilisi's biggest urban park — a hillside green space where locals jog, picnic, and escape the city. Walk up to the Chronicle of Georgia — a massive monument of 16 stone pillars (35m tall) depicting Georgian history. Incredible hilltop views.",
              details: [
                '🏛️ Chronicle of Georgia — free to visit, always open',
                '🌳 The park is big — allow 1-2 hours for a full walk',
                '🚡 Cable car from Vake Park entrance goes to Turtle Lake'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Barbarestan',
              description: "A special restaurant based on a 19th-century Georgian cookbook by Barbare Jorjadze — Georgia's first female cookbook author. Every dish is a historical recipe, beautifully presented. Georgian food as art and history. Try the walnut chicken satsivi and herb-crusted lamb.",
              meta: '💰 $$$ · 📍 132 Davit Aghmashenebeli Ave · Book ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Wine Bar Crawl in Old Town',
              description: "Self-guided wine bar crawl through Old Town. Start at G.Vino on Erekle II Street (500+ Georgian wines with modern food), move to Wine Gallery (hidden courtyard vibes), and finish at Karalashvili Wine Cellar — a family winery making qvevri wine since 1396.",
              details: [
                '🍷 G.Vino — upscale wine bar with 500+ Georgian wines',
                '🏠 Wine Gallery — courtyard wine bar, casual and local',
                '🏺 Karalashvili Wine Cellar — family winery since 1396',
                '💰 Budget ₾40-60 for the whole crawl including food'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.7052, lng: 44.7915, label: 'Stamba Hotel & Cafe', num: 1, cat: 'attraction', desc: 'Converted printing house — creative district hub' },
        { lat: 41.7040, lng: 44.7900, label: 'Rooms Hotel', num: 2, cat: 'attraction', desc: 'Design hotel with famous lobby bar' },
        { lat: 41.7020, lng: 44.7870, label: 'Vera Neighborhood', num: 3, cat: 'attraction', desc: 'Bohemian residential area — leafy, local, artistic' },
        { lat: 41.7110, lng: 44.7670, label: 'Vake Park', num: 4, cat: 'attraction', desc: "Tbilisi's biggest urban park — trails and viewpoints" },
        { lat: 41.7280, lng: 44.7540, label: 'Chronicle of Georgia', num: 5, cat: 'attraction', desc: 'Massive stone pillar monument with panoramic views' },
        { lat: 41.7068, lng: 44.7958, label: 'Barbarestan', num: 6, cat: 'food', desc: '19th-century cookbook restaurant — Georgian food as history' },
        { lat: 41.6910, lng: 44.8070, label: 'G.Vino Wine Bar', num: 7, cat: 'food', desc: 'Upscale wine bar with 500+ Georgian wines' },
        { lat: 41.6900, lng: 44.8060, label: 'Karalashvili Wine Cellar', num: 8, cat: 'food', desc: 'Family winery since 1396 — qvevri wines in a historic cellar' }
      ]
    },
    {
      num: 7,
      date: '2026-04-02',
      neighborhoods: 'Metekhi · Avlabari · Sameba',
      title: 'Metekhi, Avlabari & the Georgian Feast (Supra)',
      description: "Cross the river to the Metekhi district — home to one of Tbilisi's oldest churches, the massive Holy Trinity Cathedral (Sameba), and the Armenian-influenced Avlabari quarter. Today is about slowing down and ideally joining a supra — the legendary Georgian feast with endless toasts.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Metekhi Church & Viewpoint',
              description: "Start at Metekhi Church — perched on a cliff overlooking the Mtkvari River. Built in the 13th century, it's one of Tbilisi's most recognizable landmarks. The viewpoint in front offers the best panoramic view of Old Town, with the sulfur baths, Narikala Fortress, and the river canyon laid out before you.",
              details: [
                '⛪ 13th-century church — free entry, still active',
                '📸 THE classic Tbilisi photo spot — Old Town panorama',
                '🗡️ Statue of King Vakhtang Gorgasali on horseback nearby — the city founder'
              ]
            },
            {
              title: 'Avlabari Quarter Walk',
              description: "Walk through Avlabari — historically an Armenian neighborhood with its own distinct character. Quieter than Old Town, with colorful houses, small churches, and a local vibe. Look for the Blue Monastery and the remains of old Armenian architecture.",
              details: [
                '🏘️ More residential and local than Old Town — fewer tourists',
                '📸 Colorful buildings and quiet courtyards',
                '🚇 Avlabari metro station connects you easily to the rest of the city'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Puris Sakhli (Bread House)',
              description: "Watch women bake traditional Georgian bread in clay tone ovens while you eat. Fresh lobiani, khachapuri, and shotis puri with cheese, all baked to order. One of the most authentic breakfast experiences in the city.",
              meta: '💰 $ · 📍 Avlabari area · Opens early'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Holy Trinity Cathedral (Sameba)',
              description: "Visit the Sameba Cathedral — the largest religious building in the South Caucasus. Completed in 2004, it towers over the Avlabari skyline with its golden dome. The interior is vast, filled with modern frescoes and icons.",
              details: [
                '⛪ Free entry — dress modestly, no photography during services',
                '🏛️ The cathedral complex includes gardens and a viewpoint terrace',
                '📸 Best exterior photo from across the river in Rike Park'
              ]
            },
            {
              title: 'Free Walking Tour',
              description: "Join one of Tbilisi's excellent tip-based free walking tours — they run daily and are great for meeting fellow solo travelers. Covers Old Town, Abanotubani, Sololaki, and hidden gems in about 2.5 hours.",
              details: [
                '🚶 Tbilisi Free Walking Tour — daily at 11am and 3pm from Freedom Square',
                '💰 Tip-based — ₾20-30 is fair and appreciated',
                '🗺️ Great way to fill gaps and get insider tips from a local guide'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Georgian Supra Experience',
              description: "Tonight is your supra night — the legendary Georgian feast. Led by a tamada (toastmaster) who delivers elaborate toasts to God, family, the dead, love, and Georgia itself. The food keeps coming and the wine flows freely. Book a hosted supra through Eat This Tours or a similar operator for $30-50.",
              details: [
                '🍷 Each toast requires draining your glass — pace yourself with chacha (grape brandy)',
                '🥘 Expect 15-20 dishes: pkhali, satsivi, mtsvadi, khinkali, khachapuri, lobio...',
                '🎵 Traditional polyphonic singing may break out — UNESCO-listed vocal tradition',
                '💡 Book via Eat This Tours or similar — authentic multi-course supra with locals'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "During a supra, the tamada leads toasts and everyone drinks together. It's deeply ritualistic and emotional — Georgians toast to ancestors, love, and their country. Don't be surprised if you get emotional. It's that kind of experience." }
          ]
        }
      ],
      mapPins: [
        { lat: 41.6910, lng: 44.8120, label: 'Metekhi Church', num: 1, cat: 'attraction', desc: '13th-century church on a cliff — best Old Town panorama' },
        { lat: 41.6900, lng: 44.8135, label: 'King Vakhtang Gorgasali Statue', num: 2, cat: 'attraction', desc: 'Equestrian statue of the Tbilisi founder' },
        { lat: 41.6940, lng: 44.8150, label: 'Avlabari Quarter', num: 3, cat: 'attraction', desc: 'Historic Armenian neighborhood — quiet and colorful' },
        { lat: 41.6975, lng: 44.8172, label: 'Holy Trinity Cathedral (Sameba)', num: 4, cat: 'attraction', desc: 'Largest cathedral in the South Caucasus — golden dome' },
        { lat: 41.6935, lng: 44.8140, label: 'Puris Sakhli (Bread House)', num: 5, cat: 'food', desc: 'Watch bread baked in clay ovens — fresh lobiani and khachapuri' },
        { lat: 41.6934, lng: 44.8015, label: 'Freedom Square (Walking Tour)', num: 6, cat: 'attraction', desc: 'Meeting point for free daily walking tours' }
      ]
    },
    {
      num: 8,
      date: '2026-04-03',
      neighborhoods: 'Old Town · Chardin Street · Meidan',
      title: 'Last Morning — Souvenirs, One More Khinkali & Farewell',
      description: "Your final day in Georgia. Slow morning, last-chance shopping for spices and wine, one more plate of khachapuri, and a farewell walk through streets that have become familiar. Tbilisi has a way of making you not want to leave — you'll understand why so many travelers extend their trips.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Chardin Street & Last Wander',
              description: "Stroll down Chardin Street (Shardeni) — the lively cafe-lined pedestrian street in the heart of Old Town. Perfect for a final leisurely breakfast. Walk through Meidan Square, where ancient caravans once arrived from Persia. Take your last look at the bath domes, the fortress walls, the impossible balconies.",
              details: [
                '☕ Chardin Street has the highest concentration of cafes in Old Town',
                '📸 Take one more photo from the Metekhi viewpoint — you earned it',
                '🛍️ Wine shops on Chardin have curated bottles perfect for gifts'
              ]
            },
            {
              title: 'Souvenir Shopping',
              description: "Pick up last-minute Georgian souvenirs: a bottle of Saperavi or amber wine, churchkhela, dried spices (khmeli suneli, adjika), a drinking horn (kantsi), or cloisonné enamel jewelry. The shops around Meidan Square and Leselidze Street have the best selection.",
              details: [
                '🍷 Wine bottles are safe to fly — wrap well or buy padded wine bags',
                '🧵 Cloisonné enamel jewelry — a Georgian craft tradition',
                '🍬 Churchkhela lasts weeks — perfect travel snack and gift',
                '🏺 Small qvevri clay vessel replicas make unique decorative souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: "Sofia Melnikova's Fantastic Douqan",
              description: "End where it matters — with one last plate of perfect khinkali at this beloved Old Town institution. The Pasanauri-style mountain khinkali here are legendary. Order a dozen, sit in the cozy underground space, and say goodbye to Georgian food (for now).",
              meta: '💰 $ · 📍 Old Town · The perfect farewell meal'
            }
          ],
          tips: [
            { type: 'tip', text: "Tbilisi Airport (TBS) is only 20 minutes from the center by Bolt taxi (~₾15-20). The airport is small and efficient — arrive 2 hours before international flights. Buy one last churchkhela at the airport shop before boarding." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Departure from Tbilisi',
              description: "Head to Shota Rustaveli Tbilisi International Airport (TBS). The city will have left its mark — the warmth, the wine, the food, the mountains, the impossibly generous people. Georgia has a saying: 'A guest is a gift from God.' You've been that gift, and Tbilisi has given you everything in return.",
              details: [
                '🚕 Bolt taxi to airport: ₾15-20 (~$6) from city center',
                '✈️ TBS airport is small — arrive 2 hours before international flights',
                '🍷 Duty-free has excellent Georgian wine at reasonable prices',
                '🇬🇪 Once is never enough — you will be back'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.6912, lng: 44.8080, label: 'Chardin Street (Shardeni)', num: 1, cat: 'attraction', desc: 'Cafe-lined pedestrian street — Old Town heart' },
        { lat: 41.6900, lng: 44.8090, label: 'Meidan Square', num: 2, cat: 'attraction', desc: 'Historic caravan square — shops and restaurants' },
        { lat: 41.6895, lng: 44.8075, label: 'Leselidze Street Shopping', num: 3, cat: 'attraction', desc: 'Best souvenirs — wine, spices, churchkhela, enamel' },
        { lat: 41.6888, lng: 44.8085, label: "Sofia Melnikova's Fantastic Douqan", num: 4, cat: 'food', desc: 'Legendary khinkali spot — the perfect farewell meal' },
        { lat: 41.6692, lng: 44.9546, label: 'Tbilisi International Airport (TBS)', num: 5, cat: 'transport', desc: '20 minutes from center — small and efficient' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$5-12/night (dorm)', midrange: '$30-60/night (private)', luxury: '$80-150/night (boutique)' },
    { category: 'Meals (per day)', budget: '$8-15/day', midrange: '$20-40/day', luxury: '$50-80/day' },
    { category: 'Transport', budget: '$1-3/day (metro+Bolt)', midrange: '$5-10/day', luxury: '$20-40/day (private)' },
    { category: 'Activities', budget: '$0-10/day', midrange: '$10-30/day', luxury: '$30-60/day' },
    { category: 'Day Trips', budget: '$15-25 (marshrutka)', midrange: '$30-50 (shared tour)', luxury: '$80-120 (private driver)' },
    { category: '8-Day Total (solo)', budget: '$250-350', midrange: '$400-600', luxury: '$700-900' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Tbilisi International Airport (TBS) is 20km from center', 'Bolt taxi to center: ~₾15-20 ($6-7)', 'Bus #37 runs to Avlabari metro station for 1 GEL'] },
    { title: '🏨 Where to Stay', items: ['Fabrika Hostel — best social hostel, converted Soviet factory', 'Envoy Hostel — rooftop terrace, panoramic views, great vibe', 'Sololaki guesthouses — private rooms $25-40/night, charming location', 'Old Town Tbilisi Hotel — boutique, wooden balconies, central'] },
    { title: '🌡️ Weather in Late March', items: ['Average 10-18°C (50-64°F) — spring weather', 'Occasional rain showers — pack a light rain jacket', 'Mountain areas (Kazbegi) can be 0-5°C — bring warm layers', 'Trees are blossoming — beautiful time to visit'] },
    { title: '💳 Money', items: ['Currency: Georgian Lari (GEL) — ~2.7 GEL = $1 USD', 'ATMs are everywhere — use local ATMs for best rates', 'Most restaurants and shops are cash-preferred', 'Tipping: 10% is generous and appreciated but not expected'] },
    { title: '📱 Connectivity', items: ['Buy a Magti or Geocell SIM at the airport — $5 for 10GB', 'Free WiFi at most cafes, hostels, and restaurants', 'Bolt taxi app works great for cheap, reliable rides'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
