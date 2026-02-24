const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771949868597_8vjkpb',
  email: 'miao-cc@hotmail.com',
  destination: 'Shanghai, China',
  startDate: '2026-02-27',
  endDate: '2026-02-28',
  groupSize: '3-4',
  travelStyle: 'Foodie, Family-friendly',
  budget: 'Under $1,000'
};

const itineraryData = {
  destination: 'Shanghai, China',
  countryEmoji: '🇨🇳',
  title: 'Shanghai in Two Days — A Family Foodie Adventure',
  subtitle: 'Soup dumplings, lantern-lit gardens, neon Bund nights & street food for 3–4',
  description: "Shanghai is China's most electric city — a place where ancient teahouses sit steps from glass-and-steel skyscrapers, and where the world's finest soup dumplings cost less than a dollar each. This two-day itinerary is built for a hungry family: morning xiaolongbao at a 100-year-old dumpling house, kids running across the Nine-Bend Bridge over lotus-filled ponds, the famous Bund waterfront glittering at night, and a leisurely stroll through the plane-tree-shaded lanes of the French Concession. Budget-friendly, genuinely delicious, endlessly memorable.",
  duration: '2 days',
  dates: 'Feb 27 – Feb 28, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Families, Foodies',

  highlights: [
    'Steaming xiaolongbao fresh from the bamboo basket at Nanxiang Mantou Dian',
    'The iconic Nine-Bend Bridge and lotus-filled ponds of Yu Garden',
    'The Bund waterfront promenade — Pudong skyline glittering across the river',
    'Shengjian bao (pan-fried pork buns) — Shanghai\'s crunchiest street food',
    'The French Concession\'s tree-lined lanes and café culture on Wukang Road',
    'Scallion pancakes (cong you bing) hot from a street-side iron griddle'
  ],

  essentials: [
    {
      title: '🥟 The Dumpling Rules',
      text: "Xiaolongbao (soup dumplings) are delicate — bite a small hole in the side, let steam escape, sip the broth, THEN eat. Never bite straight in — boiling soup will burn you. Serve with black vinegar and shredded ginger. Kids love the ritual."
    },
    {
      title: '💴 Cash & WeChat Pay',
      text: "Most street vendors and markets are cash-only (RMB/yuan). Bring ¥500–800 in cash. WeChat Pay and Alipay dominate — if you have a Chinese phone number, link a foreign card to WeChat Pay. Many modern shops also accept Visa/Mastercard. ATMs at banks are reliable."
    },
    {
      title: '🚇 Getting Around',
      text: "Shanghai's metro (地铁) is world-class — clean, cheap (~¥4–7 per ride), and covers all the main sights. Buy a Shanghai Public Transport Card at any metro station for easy tap-on. Taxis and DiDi (China's Uber) are affordable for families with bags."
    },
    {
      title: '🌡️ February Weather',
      text: "Late February in Shanghai is cool and crisp — typically 5–12°C (41–54°F). Layers are key: a warm base layer, mid-layer, and a wind-proof jacket. The dry, clear skies make this a beautiful time to visit — fewer crowds than summer, and the Bund is misty and atmospheric."
    },
    {
      title: '📱 Connectivity',
      text: "Download offline Google Maps or Amap (高德地图) before arrival. A local SIM card is ~¥50–100 for 10 days of data. Note: Google, WhatsApp, and Instagram are blocked in China — use a VPN if needed, or switch to WeChat, Baidu Maps, and local apps for the trip."
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-27',
      neighborhoods: 'Yu Garden · Old Town · The Bund',
      title: 'Dumplings, Dragon Walls & the Glittering Bund',
      description: "Start your Shanghai adventure where locals have been eating for centuries — the Old Town. Weave through the nine-bend bridge over lotus ponds, eat steaming xiaolongbao, explore the classical Yu Garden, then walk north along the Bund waterfront as the Pudong skyline blazes into life after dark.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive at Yu Garden Bazaar — Breakfast Dumpling Hunt',
              description: "Head to the Yuyuan Bazaar area first thing — the streets are at their quietest in the morning and the dumpling shops are just firing up their steamers. This is Shanghai's most atmospheric old quarter: Ming-dynasty architecture, red lanterns overhead, the smell of frying dough and sizzling pork.",
              details: [
                '📍 Nearest metro: Yu Garden Station (Line 10)',
                '🏮 The Nine-Bend Bridge (Jiuqu Qiao) over Lotus Pond is free to walk across — gorgeous morning light',
                '📸 Get your family photo in front of the white-wall dragon-topped garden walls',
                '⏰ Arrive by 8:30am to beat the tour groups — mornings are magical here'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Breakfast/Brunch',
              name: 'Nanxiang Mantou Dian (南翔馒头店)',
              description: "Shanghai's most famous xiaolongbao shop, founded in 1900. A pilgrimage site for dumpling lovers. Order from the ground-floor takeaway counter for the best price — ¥18–22 for a basket of 8. The crab-and-pork (蟹粉小笼) version is spectacular if budget allows.",
              meta: '💰 ¥18–35 per basket · 📍 Yu Yuan Bazaar, Old Town · Queue expected, moves fast'
            },
            {
              type: '🥘 Street Snack',
              name: 'Shengjian Bao — Pan-Fried Pork Buns',
              description: "After xiaolongbao, grab a portion of shengjian bao from any of the small stalls dotting the bazaar lanes. Golden and crispy on the bottom, pillowy on top, with a juicy pork filling. Order by pointing — ¥10–15 for 4 buns. Kids absolutely love these.",
              meta: '💰 ¥10–15 · 📍 Yu Yuan Bazaar street stalls · Cash only'
            }
          ],
          tips: [
            { type: 'tip', text: "The queue at Nanxiang can be 20–30 minutes on weekends. Weekday mornings are faster. Use the wait time to explore the bridge and ponds — they're right next door." },
            { type: 'tip', text: "Eating in the bazaar: prices are slightly higher than side streets, but the atmosphere is worth it for your first meal in Shanghai." }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Yu Garden (豫园) — Classical Chinese Garden',
              description: "Built in 1559 for the Pan family, Yu Garden is a masterpiece of Ming-dynasty garden design: rockery mountains, koi-filled ponds, zigzag corridors, and pavilions draped in wisteria. Kids love climbing around the artificial stone mountains and spotting fish. The garden is compact (2 hectares) but feels like a different world.",
              details: [
                '🎫 Entry: ¥30 adults, ¥15 children (off-season Feb–Mar discount)',
                '⏱️ Allow 1–1.5 hours to explore at a relaxed pace',
                '🐟 Spot the huge koi in the central pond near the Yuhua Hall',
                '🏛️ The Hall of Heralding Spring (点春堂) has gorgeous carved wooden screens',
                '📸 Best photo: stand at the zigzag bridge and shoot back toward the teahouse'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Skip the souvenir shops inside the bazaar — prices are tourist-inflated. Better souvenirs at lower prices can be found later on Nanjing Road or at the City God Temple market." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Walk or Metro to The Bund (外滩)',
              description: "The Bund is Shanghai's most iconic promenade — 1.5km of colonial-era European buildings facing the futuristic Pudong skyline across the Huangpu River. Walking north from Old Town (about 20 minutes on foot) takes you past the old French Quarter streets and gives you a feel for the city's European-meets-Chinese character.",
              details: [
                '🚶 Walk: 20 minutes north through Old Town lanes',
                '🚇 Metro: Line 2 to East Nanjing Road station (1 stop)',
                '🌆 The Pudong skyline across the river: Oriental Pearl Tower, Shanghai Tower (world\'s 2nd tallest), Jin Mao Tower',
                '📸 The best Bund photo: shoot from the promenade toward Pudong at the No. 3 Bund, looking north'
              ]
            },
            {
              title: 'East Nanjing Road (南京东路) — Pedestrian Street Stroll',
              description: "Shanghai's famous pedestrian shopping boulevard runs 1.5km from People's Square to the Bund. Lined with department stores, snack shops, and street performers, it's great for the kids. Duck into Shen Dacheng (沈大成) bakery for traditional Shanghai pastries: red bean cakes, sesame puffs, and osmanthus rice cakes.",
              details: [
                '🧁 Shen Dacheng — a 130-year-old Shanghai pastry institution',
                '🛍️ Window shopping is free; budget ¥50–100 for snacks and treats',
                '🎪 Street performances and live music most afternoons',
                '⏱️ Allow 30–45 minutes'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Jia Jia Tang Bao (佳家汤包)',
              description: "Locals\' favourite for xiaolongbao — no tourist fuss, just perfect dumplings. A small, no-frills shop near People's Square that gets packed with office workers at lunch. Order the pork xiaolongbao (¥14 for 6) and the crab roe version if you're feeling spendy. This is the real deal.",
              meta: '💰 ¥14–28 per basket · 📍 90 Huanghe Road, near People\'s Square · Cash only, lines move quickly'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'The Bund at Night — When Shanghai Truly Dazzles',
              description: "Return to the Bund as the sun sets (around 6pm in February). The Pudong skyline lights up tower by tower — the Oriental Pearl glows pink, Shanghai Tower shimmers, and the colonial facades behind you warm in golden light. Grab a spot along the railing and let the spectacle wash over you. This is one of the world's great city views.",
              details: [
                '🌆 Head to the Bund around 5:30pm to catch the last light',
                '💡 The light show intensifies from 6:30pm onward',
                '🎠 The Bund is at its best from the Waibaidu Bridge end (north)',
                '🧊 February evenings are cold — bring that extra layer!'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Lost Heaven (花马天堂)',
              description: "Yunnan cuisine in a beautifully atmospheric space on the Bund — think aromatic mushroom broths, mint-heavy salads, fragrant rice dishes, and mellow spice. Great for families: the flavours are interesting without being too fiery, portions are generous, and the design (Yunnan ethnic art) is visually stunning for kids and adults alike.",
              meta: '💰 ¥60–100pp · 📍 17 Yan\'an East Road, near The Bund · Book ahead or arrive early'
            }
          ],
          tips: [
            { type: 'tip', text: "For the Bund at night: the free ferry across to Pudong (¥2 each way) gives you the iconic reverse view — the Bund lit up from the water. Kids love the ferry crossing and it's much cheaper than a river cruise." }
          ]
        }
      ],
      mapPins: [
        { lat: 31.2263, lng: 121.4888, label: 'Nine-Bend Bridge & Lotus Pond', num: 1, cat: 'attraction', desc: 'Iconic zigzag bridge over lotus ponds at Yu Yuan Bazaar' },
        { lat: 31.2272, lng: 121.4923, label: 'Nanxiang Mantou Dian', num: 2, cat: 'food', desc: '100-year-old xiaolongbao institution — order from ground-floor counter' },
        { lat: 31.2278, lng: 121.4926, label: 'Yu Garden (豫园)', num: 3, cat: 'attraction', desc: 'Ming-dynasty classical garden with rockeries, koi ponds, and pavilions' },
        { lat: 31.2358, lng: 121.4762, label: 'Jia Jia Tang Bao', num: 4, cat: 'food', desc: 'Locals\' favourite xiaolongbao near People\'s Square — no frills, perfect dumplings' },
        { lat: 31.2354, lng: 121.4701, label: 'East Nanjing Road', num: 5, cat: 'attraction', desc: 'Famous pedestrian boulevard with Shen Dacheng pastries and street performers' },
        { lat: 31.2397, lng: 121.4904, label: 'The Bund (外滩)', num: 6, cat: 'attraction', desc: 'Iconic waterfront promenade — Pudong skyline views, dazzling at night' },
        { lat: 31.2346, lng: 121.4871, label: 'Lost Heaven Restaurant', num: 7, cat: 'food', desc: 'Yunnan cuisine — aromatic, family-friendly, beautifully designed' }
      ]
    },
    {
      num: 2,
      date: '2026-02-28',
      neighborhoods: 'French Concession · Tianzifang · Xintiandi',
      title: 'Plane Trees, Street Art & the French Concession Food Crawl',
      description: "Day two explores Shanghai's most charming neighbourhood — the Former French Concession. Leafy boulevards, art deco villas, boutique cafés, and the hidden alleyways of Tianzifang packed with artisan stalls and excellent dumplings. End with the lively lane-house complex of Xintiandi and a final family feast.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Scallion Pancake Breakfast on the Street',
              description: "Start the day the way Shanghai locals do: queuing at a street-side cong you bing (葱油饼) cart. These scallion-and-sesame flatbreads are made fresh on a seasoned iron griddle, layered with shallots, sesame seeds, and a drizzle of chilli sauce. Cost: ¥6–8 each. Find them on any residential street in the French Concession — just follow your nose.",
              details: [
                '🥞 Look for small carts with iron griddles near metro station exits in the morning',
                '🧅 Can add egg (加鸡蛋) for ¥2 extra — highly recommended',
                '⏰ Best between 7–9am before they sell out',
                '💰 ¥6–10 per pancake — one of Shanghai\'s best budget breakfasts'
              ]
            },
            {
              title: 'Wukang Road (武康路) — Shanghai\'s Most Beautiful Street',
              description: "Walk along Wukang Road — often called Shanghai's most photogenic street. Lined with French plane trees (platanes) that form a cathedral canopy overhead, flanked by Art Deco and French Renaissance villas housing cafés, boutiques, and hidden courtyards. The Wukang Building at the north end is the city's most-photographed building.",
              details: [
                '🌳 The plane trees are bare in February — a different but equally beautiful look, with misty skies',
                '📸 Wukang Building (at the fork): iconic red-brick Art Deco building from 1924',
                '☕ Stop at any of the dozen-odd independent cafés — Shanghai has incredible coffee culture',
                '🚶 Stroll at leisure — the whole road is only 1.1km'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Street Scallion Pancakes + Coffee from a Concession Café',
              description: "Grab your pancakes from a street cart, then stop at one of the independent specialty cafés along Yongkang Road or Anfu Road for a flat white. Shanghai's café scene is world-class — better quality than most western cities, and prices are similar.",
              meta: '💰 ¥20–40 total for breakfast · 📍 Wukang Road area, French Concession'
            }
          ],
          tips: [
            { type: 'tip', text: "Yongkang Road is nicknamed 'Bar Street' but in the daytime it's a quiet, locals-only café strip. The coffee shops here serve the city's best brews at ¥25–40 a cup." }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Tianzifang (田子坊) — The Maze of Art & Street Food',
              description: "Tianzifang is a labyrinth of 1920s shikumen (stone-gate) lane houses converted into galleries, artisan boutiques, café terraces, and street food stalls. It's Shanghai's most fun neighbourhood to explore with kids — the alleys twist and fork, dead ends open into hidden courtyards, and every corner has something to smell, taste, or buy. Budget an hour or two.",
              details: [
                '🗺️ Enter from Taikang Road — the main entrance has the most stalls',
                '🎨 Dozens of tiny art and craft shops: paper cuts, ceramics, painted silk, calligraphy',
                '🧆 Street food inside: egg waffles (鸡蛋仔), stinky tofu, shrimp rolls, mango smoothies',
                '📸 Climb to the top-floor terraces for aerial alley views',
                '💡 Free entry, but budget ¥50–100 per person for snacks and souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🥙 Snack Stop',
              name: 'Tianzifang Street Food — Egg Waffles & Shrimp Rolls',
              description: "Pick your way through the stalls: Hong Kong-style egg waffles (QQ, crispy, slightly sweet) from the little waffle cart, and fresh shrimp spring rolls from the counter at the back of lane 210. These are great snacks to carry while exploring.",
              meta: '💰 ¥10–20 per snack · 📍 Inside Tianzifang lanes, Taikang Road'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Xintiandi (新天地) — Lane Houses & City History',
              description: "A short walk from Tianzifang, Xintiandi is a chic complex of restored 1920s shikumen (stone-gate) lane houses — now boutique restaurants, galleries, and the Shanghai History Museum of the 1st National Congress of the CPC. The North Block has a lovely open square good for kids to run around; the South Block has excellent dining options.",
              details: [
                '🏛️ Shikumen Open House Museum: small, fascinating look inside a 1920s family home — ¥20',
                '🌍 The 1st National Congress Site is historically significant and very accessible with kids',
                '☀️ The open plaza in the North Block is a great spot to rest tired feet in the afternoon sun',
                '🛍️ Designer shops here — good for window shopping, not budget buying'
              ]
            },
            {
              title: 'People\'s Square & Shanghai Museum',
              description: "If time and energy allow, metro one stop to People's Square and visit the free Shanghai Museum (上海博物馆) — one of Asia's finest. The ancient bronzes, ceramics, and calligraphy galleries are world-class. The museum is designed around a bronze ding (ancient cooking vessel) — fitting for a foodie trip.",
              details: [
                '🏛️ Free entry with timed ticket booking (book online the day before)',
                '⏱️ Allow 1–1.5 hours — the bronzes and ceramics galleries are the highlights',
                '👶 Family-friendly: the museum has clear signage in English and engaging exhibits',
                '📍 People\'s Square, Line 1/2/8'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Crystal Jade (翡翠酒家) at Xintiandi',
              description: "A Singapore-born dim sum chain that has earned a loyal Shanghai following — excellent quality xiaolongbao, har gow (shrimp dumplings), char siu bao (BBQ pork buns), and congee. Perfect for families: the service is attentive, the menu has pictures, and kids love the variety of small dishes. Reasonably priced for the quality.",
              meta: '💰 ¥80–120 for 3–4 people · 📍 Xintiandi South Block, Lane 123 Xingye Road'
            }
          ],
          tips: [
            { type: 'tip', text: "At dim sum, ordering tip: point at the trolley or tick boxes on the paper menu. For families: har gow (🦐), siu mai (🥟), cheung fun (rice noodle rolls), and egg tarts (蛋挞) are universal crowd-pleasers." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Bund Sunset Walk & Huangpu Ferry',
              description: "For your last evening, walk back to the Bund for one more look — this time at sunset. Take the ¥2 Huangpu River ferry from Jinling Road to Dongchang Road on the Pudong side. The 5-minute crossing gives you the iconic reverse view: the entire Bund facade glowing golden. Cross back and stroll north for one last family photo in front of the colonial skyline.",
              details: [
                '⛴️ Jinling Road Ferry Pier → Dongchang Road Pudong — ¥2 each way',
                '📸 From the Pudong side, the full Bund panorama is unobstructed',
                '🌅 February sunsets: around 5:50pm — the golden hour is brief but beautiful',
                '🌃 Stay for the lights: by 6:30pm, the colonial buildings are lit warm amber'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Din Tai Fung (鼎泰丰) — The Classic Farewell',
              description: "End your Shanghai food adventure at Din Tai Fung — the Taiwanese xiaolongbao institution that perfectd the soup dumpling for the modern world. Open kitchen where you can watch the chefs hand-pleat each dumpling. Order the signature pork xiaolongbao (黄金蛋炒饭), the shrimp and pork wontons in chilli oil, and the taro dumplings for dessert. A joyful, loud, family-friendly feast.",
              meta: '💰 ¥100–160 for 3–4 people · 📍 Multiple locations; IAPM Mall (Huaihai Road) branch is convenient · Reserve online or arrive early'
            }
          ],
          tips: [
            { type: 'tip', text: "Shanghai food farewell rule: you'll spend the flight home thinking about the soup dumplings. Buy a frozen pack from a supermarket (City Shop or Carrefour) to take home — they travel surprisingly well." }
          ]
        }
      ],
      mapPins: [
        { lat: 31.2181, lng: 121.4400, label: 'Wukang Road (武康路)', num: 1, cat: 'attraction', desc: 'Shanghai\'s most beautiful street — Art Deco villas, plane trees, cafés' },
        { lat: 31.2153, lng: 121.4422, label: 'Wukang Building', num: 2, cat: 'attraction', desc: 'Iconic 1924 Art Deco landmark — the city\'s most-photographed building' },
        { lat: 31.2103, lng: 121.4641, label: 'Tianzifang (田子坊)', num: 3, cat: 'attraction', desc: '1920s lane house maze of art, crafts, street food — Taikang Road entrance' },
        { lat: 31.2186, lng: 121.4731, label: 'Xintiandi (新天地)', num: 4, cat: 'attraction', desc: 'Restored shikumen complex — history museum, plaza, and great dim sum' },
        { lat: 31.2186, lng: 121.4731, label: 'Crystal Jade Restaurant', num: 5, cat: 'food', desc: 'Excellent dim sum in Xintiandi — family-friendly with English menu' },
        { lat: 31.2304, lng: 121.4762, label: 'Shanghai Museum', num: 6, cat: 'attraction', desc: 'Free world-class museum — bronzes, ceramics, calligraphy (book tickets ahead)' },
        { lat: 31.2397, lng: 121.4904, label: 'Bund Jinling Ferry Pier', num: 7, cat: 'attraction', desc: '¥2 ferry to Pudong — the best Bund view money can\'t buy' },
        { lat: 31.2168, lng: 121.4540, label: 'Din Tai Fung (IAPM Mall)', num: 8, cat: 'food', desc: 'Farewell dinner — world-famous xiaolongbao, open kitchen, perfect for families' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (3-4 people)', budget: '¥300–500/night', midrange: '¥500–900/night', luxury: '¥1,200–3,000/night' },
    { category: 'Meals (per person)', budget: '¥80–150/day', midrange: '¥150–300/day', luxury: '¥400+/day' },
    { category: 'Metro & Transport', budget: '¥20–40/day', midrange: '¥50–100/day (DiDi mix)', luxury: '¥200+/day (private car)' },
    { category: 'Yu Garden Entry', budget: '¥30 adults, ¥15 kids', midrange: '¥30 adults, ¥15 kids', luxury: '¥30 adults, ¥15 kids' },
    { category: 'Street Food & Snacks', budget: '¥50–100/day', midrange: '¥80–150/day', luxury: '¥150+/day' },
    { category: '2-Day Total (family of 4)', budget: '¥1,500–2,500 (~$200–350 USD)', midrange: '¥2,500–4,500 (~$350–620 USD)', luxury: '¥6,000+ (~$800+ USD)' }
  ],

  practicalInfo: [
    {
      title: '✈️ Getting There & Around',
      items: [
        'Shanghai has two airports: Pudong (PVG, international) and Hongqiao (SHA, domestic)',
        'Pudong to city: Maglev to Longyang Road (¥50, 8 mins!) then metro, or metro Line 2 direct (~50 mins, ¥7)',
        'Metro is clean, safe, and has English signage — perfect for families',
        'DiDi app (Chinese Uber) works for families with more luggage — most drivers accept in-app translation'
      ]
    },
    {
      title: '🏨 Where to Stay',
      items: [
        'French Concession area: best for families — walkable, charming, quiet at night',
        'Budget option: Ji Hotel or Hanting near Xintiandi (~¥250–400/night)',
        'Mid-range: The Capella Shanghai, Jian Ye Li (boutique shikumen) (~¥600–900/night)',
        'Avoid Pudong unless you\'re specifically there for business — it\'s less atmospheric'
      ]
    },
    {
      title: '🥢 Food Tips for Families',
      items: [
        'Kids menu isn\'t common, but most dishes are shareable and mild unless you ask for spice',
        'Allergen note: soy sauce and sesame oil are universal in Shanghai cuisine',
        'Vegetarian options are limited in traditional spots — look for Buddha cuisine (素食) restaurants if needed',
        'Eating out is cheap: a full meal for 4 at a local restaurant = ¥80–150 total'
      ]
    },
    {
      title: '📱 App Essentials',
      items: [
        'Amap (高德地图) — better than Google Maps for China; works offline',
        'Dianping — China\'s Yelp for restaurant reviews (use translation)',
        'DiDi — ride hailing, add your destination in English and show the driver',
        'WeChat — essential for payments and messaging once you\'re in China'
      ]
    },
    {
      title: '👶 Family Tips',
      items: [
        'Yu Garden is stroller-accessible but crowded — a carrier is easier',
        'Tianzifang lanes are narrow — fold strollers and let kids explore on foot',
        'Shanghai is very safe for families — streets are lively and well-lit at night',
        'Most major attractions have Western-style toilets alongside squat toilets'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
