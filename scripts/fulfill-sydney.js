const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771305592929_vg1awg',
  email: 'bernardjhuang@gmail.com',
  destination: 'Sydney NSW, Australia',
  startDate: '2026-12-23',
  endDate: '2026-12-29',
  groupSize: 2,
  requests: 'romantic holiday'
};

const itineraryData = {
  destination: 'Sydney, Australia',
  countryEmoji: '🇦🇺',
  title: 'A Romantic Summer Christmas in Sydney',
  subtitle: '6 days of harbour sunsets, beach picnics & festive magic for two',
  description: "Sydney at Christmas is pure summer magic — golden beaches, sparkling harbour views, and long balmy evenings made for romance. This itinerary weaves iconic landmarks with intimate experiences: sunrise walks along coastal cliffs, candlelit dinners overlooking the Opera House, a Christmas Day beach picnic, and a sunset harbour cruise for two. It's the Southern Hemisphere's most romantic holiday.",
  duration: '6 nights',
  dates: 'Dec 23 – Dec 29, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Couples',
  highlights: [
    'Sunset harbour cruise past the Opera House',
    'Christmas Day beach picnic at Bondi',
    'Bondi to Coogee coastal walk',
    'Fine dining at Quay with harbour views',
    'Blue Mountains day trip to romantic lookouts'
  ],

  essentials: [
    { title: '☀️ Summer Christmas', text: 'December is peak summer in Sydney — expect 25-30°C, long daylight hours, and beach weather. Pack sunscreen, swimwear, and light layers for breezy evenings.' },
    { title: '🚇 Getting Around', text: 'Tap-on with a contactless card or phone on buses, trains, ferries & light rail. The Opal system covers everything. Ferries are the most scenic way to travel.' },
    { title: '🎄 Christmas Hours', text: "Dec 25 is very quiet — most shops and restaurants close. Book Christmas Day dining well in advance. Boxing Day (Dec 26) sees major sales and Sydney to Hobart yacht race festivities." },
    { title: '💑 Romance Tips', text: "Book harbour-view restaurants early (Quay, Bennelong, The Boathouse). Sunset is around 8pm — perfect for late golden-hour strolls. Many beaches have secluded spots at their southern ends." }
  ],

  days: [
    {
      num: 1,
      date: '2026-12-23',
      neighborhoods: 'Circular Quay · The Rocks · Harbour',
      title: 'Harbour Icons & First Impressions',
      description: "Arrive in Sydney and fall in love with the harbour. Stroll through The Rocks' cobblestone lanes, catch your first glimpse of the Opera House at golden hour, and toast to the trip with cocktails overlooking the bridge.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & The Rocks Discovery Walk',
              description: 'After settling into your hotel, wander through The Rocks — Sydney\'s oldest neighbourhood. Explore the cobblestone laneways, artisan markets, and heritage pubs.',
              details: [
                '🏨 Stay near Circular Quay for walkable harbour access',
                '🛍️ The Rocks Markets run Sat–Sun, but the lanes are charming any day',
                '📸 Cadman\'s Cottage — Sydney\'s oldest surviving residential building'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet-lagged? The harbour breeze and golden light will wake you right up. Walk along the foreshore from The Rocks to the Opera House.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Opera House & Harbour Bridge at Sunset',
              description: 'Walk to the Opera House forecourt and watch the sunset paint the Harbour Bridge gold. The eastern side of Circular Quay gives you both icons in one frame.',
              details: [
                '🌅 Sunset is around 8:00pm — the light is magical from 7pm',
                '📸 Best couple photo spot: Mrs Macquarie\'s Chair for the classic framing'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Bennelong Restaurant',
              description: 'Fine dining inside the Opera House sails — Australian contemporary cuisine in one of the world\'s most iconic settings.',
              meta: '💰 $$$$ · 📍 Inside Sydney Opera House · Book well ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.8599, lng: 151.2090, label: 'The Rocks', num: 1, cat: 'attraction', desc: 'Historic cobblestone neighbourhood with markets and pubs' },
        { lat: -33.8568, lng: 151.2153, label: 'Sydney Opera House', num: 2, cat: 'attraction', desc: 'Iconic performing arts venue on Bennelong Point' },
        { lat: -33.8523, lng: 151.2108, label: 'Sydney Harbour Bridge', num: 3, cat: 'attraction', desc: 'The famous Coathanger — walk or climb for views' },
        { lat: -33.8601, lng: 151.2225, label: "Mrs Macquarie's Chair", num: 4, cat: 'attraction', desc: 'Sandstone bench with the best Opera House + Bridge panorama' },
        { lat: -33.8567, lng: 151.2149, label: 'Bennelong Restaurant', num: 5, cat: 'food', desc: 'Fine dining inside the Opera House' }
      ]
    },
    {
      num: 2,
      date: '2026-12-24',
      neighborhoods: 'Royal Botanic Garden · Farm Cove · Darling Harbour',
      title: 'Christmas Eve — Gardens, Galleries & Harbour Lights',
      description: "Spend Christmas Eve immersed in Sydney's natural beauty and culture. Morning in the Royal Botanic Garden, afternoon art at the AGNSW, and a magical Christmas Eve harbour dinner cruise as the city twinkles.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Royal Botanic Garden Stroll',
              description: "Wander through 30 hectares of lush gardens right on the harbour. The rose garden is in full summer bloom, and the rainforest walk feels like a secret world. Find a shady bench for two near the harbour edge.",
              details: [
                '🌹 The Palace Rose Garden — peak bloom in December',
                '🌿 Rainforest Gully walk for cool shade',
                '☕ Botanic House café for flat whites with harbour views'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Art Gallery of NSW',
              description: 'Visit the recently expanded Art Gallery of NSW, including the stunning new Sydney Modern building. Free entry to most galleries, with Aboriginal and Torres Strait Islander art collections that are world-class.',
              details: [
                '🖼️ Free admission · Open Christmas Eve until 5pm',
                '🏛️ The new Sydney Modern building has a rooftop with harbour views'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Chiswick at the Gallery',
              description: 'Garden-to-table dining in a beautiful setting within the Art Gallery grounds. Perfect for a leisurely Christmas Eve lunch.',
              meta: '💰 $$$ · 📍 Art Gallery of NSW'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Christmas Eve Harbour Dinner Cruise',
              description: "Board a Christmas Eve dinner cruise and glide past the Opera House and Harbour Bridge as they light up for the festive season. Many cruises offer a 3-course meal with champagne — utterly romantic.",
              details: [
                '🚢 Captain Cook Cruises or Sydney Harbour Tall Ships offer Christmas Eve specials',
                '🥂 Book the sunset departure (around 6:30pm) for golden hour on the water',
                '🎄 The harbour foreshore homes are decorated with Christmas lights'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.8642, lng: 151.2166, label: 'Royal Botanic Garden', num: 1, cat: 'attraction', desc: 'Lush harbourside gardens with roses in full bloom' },
        { lat: -33.8688, lng: 151.2173, label: 'Art Gallery of NSW', num: 2, cat: 'attraction', desc: 'World-class art including Sydney Modern expansion' },
        { lat: -33.8688, lng: 151.2173, label: 'Chiswick at the Gallery', num: 3, cat: 'food', desc: 'Garden-to-table lunch in the gallery grounds' },
        { lat: -33.8610, lng: 151.2030, label: 'Darling Harbour', num: 4, cat: 'attraction', desc: 'Waterfront precinct — departure point for dinner cruises' },
        { lat: -33.8555, lng: 151.2094, label: 'Harbour Cruise Route', num: 5, cat: 'attraction', desc: 'Christmas Eve dinner cruise past illuminated icons' }
      ]
    },
    {
      num: 3,
      date: '2026-12-25',
      neighborhoods: 'Bondi Beach · Tamarama · Bronte',
      title: 'Christmas Day — Beach, Bubbles & Summer Sun',
      description: "This is the quintessential Aussie Christmas — wake up slow, head to Bondi Beach with a picnic hamper, swim in the ocean, and celebrate the most magical Christmas you've ever had under a blazing summer sun.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Christmas Morning at Bondi Beach',
              description: "Arrive at Bondi early for a Christmas morning swim. The beach fills up as the day goes on, so claim a spot near the south end for more privacy. Thousands of people celebrate Christmas at Bondi — it's a uniquely joyful tradition.",
              details: [
                '🏖️ South Bondi is quieter and more romantic',
                '🎄 Backpackers and locals alike celebrate Christmas on the sand',
                '🏊 The ocean is around 22°C — perfect for a Christmas dip'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Beach Picnic for Two',
              description: "Spread out a picnic blanket and enjoy a gourmet Christmas hamper — think prawns, oysters, champagne, pavlova. Many Sydney delis offer pre-made Christmas picnic hampers (order ahead). Tamarama Beach, just south of Bondi, is a hidden gem that's less crowded.",
              details: [
                '🦐 Order a hamper from Jones the Grocer or The Picnic Co.',
                '🍾 BYO champagne — Tamarama is a gorgeous, intimate cove',
                '🧴 SPF 50+ and a hat — the Christmas sun is intense'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Almost everything is closed on Christmas Day in Sydney. Prepare your picnic the day before or pre-order a hamper. Your hotel may offer a Christmas Day package too." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Christmas Sunset at Bronte',
              description: "Walk south along the coastal path to Bronte Beach and watch the sun set from the cliffside park. The Bronte Baths ocean pool glows golden at sunset. A magical end to a perfect Christmas Day.",
              details: [
                '🌅 Bronte Park has BBQ facilities and shady Norfolk pines',
                '🏊 Bronte Baths ocean pool — swim with a view'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hotel Christmas Dinner',
              description: "Most upscale hotels offer special Christmas dinner seatings. Book at your hotel or a nearby luxury property — it's the most reliable option for Christmas night dining.",
              meta: '💰 $$$$ · 📍 Book well in advance — Christmas dinner sells out'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.8915, lng: 151.2767, label: 'Bondi Beach', num: 1, cat: 'attraction', desc: 'Sydney\'s most famous beach — Christmas Day tradition' },
        { lat: -33.8980, lng: 151.2730, label: 'Tamarama Beach', num: 2, cat: 'attraction', desc: 'Intimate cove beach perfect for a couple\'s picnic' },
        { lat: -33.9036, lng: 151.2680, label: 'Bronte Beach', num: 3, cat: 'attraction', desc: 'Beautiful beach with ocean pool and sunset views' },
        { lat: -33.8930, lng: 151.2745, label: 'Bondi to Bronte Walk', num: 4, cat: 'attraction', desc: 'Spectacular coastal path linking the eastern beaches' },
        { lat: -33.8932, lng: 151.2782, label: 'Bondi Icebergs', num: 5, cat: 'attraction', desc: 'Iconic ocean pool and dining club on the cliffs' }
      ]
    },
    {
      num: 4,
      date: '2026-12-26',
      neighborhoods: 'Sydney Harbour · Rushcutters Bay · Watsons Bay',
      title: 'Boxing Day — Yacht Race, Harbour & Watsons Bay',
      description: "It's Boxing Day and the start of the legendary Sydney to Hobart yacht race! Watch the fleet pour through the harbour heads, then escape to Watsons Bay for fish & chips, cliff walks, and sunset drinks at a harbourside pub.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sydney to Hobart Yacht Race Start',
              description: "The Boxing Day start of the Sydney to Hobart race is one of Australia's great sporting spectacles. Over 100 yachts sail out through the harbour heads. The best free views are from the shoreline — head to Bradleys Head, Nielsen Park, or take a ferry to watch from the water.",
              details: [
                '⛵ Race starts at 1pm from Sydney Harbour',
                '📍 Bradleys Head in Mosman gives front-row harbour views',
                '🚢 Special spectator ferries run — book early',
                '📸 The fleet passing the Opera House is a bucket-list photo'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'The Boathouse, Balmoral Beach',
              description: 'Beautiful waterside café on Balmoral Beach — one of the most romantic brunch spots in Sydney. Fresh pastries, smashed avo, and harbour views.',
              meta: '💰 $$ · 📍 Balmoral Beach, Mosman'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Watsons Bay & South Head Walk',
              description: "Catch a ferry to Watsons Bay — one of Sydney's most charming harbour villages. Walk the South Head Heritage Trail along dramatic sandstone cliffs with sweeping ocean views. The Gap lookout is breathtaking.",
              details: [
                '🚢 Ferry from Circular Quay to Watsons Bay — 25 mins of pure harbour scenery',
                '🥾 South Head walk is about 1.5km — easy and stunning',
                '🏖️ Camp Cove — tiny, perfect harbour beach for a swim'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Doyles on the Beach',
              description: "Sydney's legendary seafood restaurant right on Watsons Bay. Fresh fish and chips with your feet practically in the sand, watching the sun set over the city skyline. Unbeatable.",
              meta: '💰 $$$ · 📍 Watsons Bay · Outdoor waterfront seating'
            }
          ],
          tips: [
            { type: 'tip', text: "Catch the ferry back to Circular Quay after dinner — the city lights reflecting on the harbour at night are incredibly romantic." }
          ]
        }
      ],
      mapPins: [
        { lat: -33.8433, lng: 151.2567, label: 'Bradleys Head', num: 1, cat: 'attraction', desc: 'Best vantage point for the yacht race start' },
        { lat: -33.8314, lng: 151.2519, label: 'Balmoral Beach', num: 2, cat: 'food', desc: 'The Boathouse café — romantic waterside brunch' },
        { lat: -33.8437, lng: 151.2833, label: 'Watsons Bay', num: 3, cat: 'attraction', desc: 'Charming harbour village with ferries and seafood' },
        { lat: -33.8358, lng: 151.2862, label: 'South Head Walk', num: 4, cat: 'attraction', desc: 'Dramatic clifftop walk with ocean panoramas' },
        { lat: -33.8430, lng: 151.2775, label: 'Camp Cove Beach', num: 5, cat: 'attraction', desc: 'Tiny hidden harbour beach for a couple\'s swim' },
        { lat: -33.8437, lng: 151.2833, label: 'Doyles on the Beach', num: 6, cat: 'food', desc: 'Legendary seafood with sunset harbour views' }
      ]
    },
    {
      num: 5,
      date: '2026-12-27',
      neighborhoods: 'Blue Mountains · Katoomba · Leura',
      title: 'Blue Mountains — Misty Valleys & Village Romance',
      description: "Escape the city for a day trip to the Blue Mountains. Dramatic cliff faces, eucalyptus-scented valleys, and the charming village of Leura with its cafés, antique shops, and gardens. It's like stepping into another world.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to the Blue Mountains',
              description: "Hire a car or book a private tour and head west to the Blue Mountains — about 90 minutes from Sydney. The winding road up through the mountains builds anticipation, and the first viewpoint will take your breath away.",
              details: [
                '🚗 Hire a car from the city or book a private couples tour',
                '⏰ Leave by 8am to beat the crowds at lookouts',
                '🗺️ Take the Great Western Highway — scenic and straightforward'
              ]
            },
            {
              title: 'Three Sisters & Echo Point',
              description: "The Three Sisters rock formation at Echo Point is the Blue Mountains' most famous view. Arrive early and you may have the lookout almost to yourselves. Descend the Giant Stairway (800+ steps) for a closer look — or just admire from above.",
              details: [
                '📸 The Three Sisters against blue eucalyptus haze — iconic',
                '🥾 Giant Stairway descent is optional — great workout though!',
                '🌿 The valley floor has beautiful rainforest walks'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Scenic World & Rainforest Walk',
              description: "Ride the Scenic Railway — the world's steepest — down into the ancient Jurassic rainforest. Walk the boardwalk through towering tree ferns and listen for lyrebirds. Take the Skyway cable car back for panoramic valley views.",
              details: [
                '🚂 Scenic Railway is thrilling — 52° incline!',
                '🌳 The Jurassic-era rainforest is 300+ million years old',
                '🚡 Skyway gives you a bird\'s-eye view of Katoomba Falls'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Leura Garage',
              description: 'Mediterranean-inspired bistro in a converted Art Deco garage in charming Leura village. Excellent wine list and a garden courtyard.',
              meta: '💰 $$$ · 📍 84 Railway Parade, Leura'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Leura Village & Return',
              description: "Stroll through Leura's tree-lined streets, browse antique shops and galleries, and pick up handmade chocolates from Josophan's Fine Chocolates. Then head back to Sydney as the sun sets over the mountains.",
              details: [
                '🍫 Josophan\'s Fine Chocolates — pick up a box for the hotel room',
                '🏘️ Leura is adorable — think English village meets Australian bush'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Quay Restaurant',
              description: "Back in Sydney, celebrate your mountain adventure at Quay — one of Australia's finest restaurants. Peter Gilmore's tasting menu is extraordinary, and the Opera House views from your table are unmatched.",
              meta: '💰 $$$$ · 📍 Overseas Passenger Terminal, The Rocks · Book months ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.7324, lng: 150.3115, label: 'Three Sisters / Echo Point', num: 1, cat: 'attraction', desc: 'Iconic rock formation with panoramic valley views' },
        { lat: -33.7273, lng: 150.3010, label: 'Scenic World', num: 2, cat: 'attraction', desc: 'Railway, Skyway, and rainforest walks' },
        { lat: -33.7137, lng: 150.3364, label: 'Leura Village', num: 3, cat: 'attraction', desc: 'Charming mountain village with cafés and antiques' },
        { lat: -33.7137, lng: 150.3364, label: 'Leura Garage', num: 4, cat: 'food', desc: 'Mediterranean bistro in a converted Art Deco garage' },
        { lat: -33.8600, lng: 151.2093, label: 'Quay Restaurant', num: 5, cat: 'food', desc: "Australia's top restaurant — harbour views and tasting menus" }
      ]
    },
    {
      num: 6,
      date: '2026-12-28',
      neighborhoods: 'Manly · Bondi to Coogee · Circular Quay',
      title: 'Coastal Walks, Manly Ferry & Farewell Sunset',
      description: "Your last full day is all about Sydney's coastal magic. Morning ferry to Manly Beach, the legendary Bondi to Coogee walk in the afternoon, and a farewell sunset from the harbour with the one you love.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ferry to Manly Beach',
              description: "The Manly Ferry from Circular Quay is one of the world's great commuter rides — 30 minutes across the sparkling harbour. Manly Beach is a gorgeous stretch of golden sand backed by Norfolk pines. Swim, stroll, or just sit together and watch the waves.",
              details: [
                '🚢 Ferry from Circular Quay Wharf 3 — sit on the left for Opera House views',
                '🏖️ Manly Beach is long and beautiful — walk to the quieter north end',
                '🦈 Shelly Beach (short walk from Manly) has excellent snorkelling'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'The Pantry Manly',
              description: 'Beloved beachside café right on Manly Beach. Excellent coffee, ricotta hotcakes, and ocean views from the terrace.',
              meta: '💰 $$ · 📍 Ocean Promenade, Manly'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bondi to Coogee Coastal Walk',
              description: "Sydney's most famous walk — 6km of stunning coastal scenery from Bondi to Coogee. Dramatic sandstone cliffs, hidden beaches, ocean pools, and Aboriginal rock carvings. Take your time, swim at Bronte or Clovelly, and savour every view.",
              details: [
                '🥾 6km, about 2 hours (or longer with beach stops)',
                '🏖️ Swim stops: Tamarama, Bronte, Clovelly, Coogee',
                '🌊 Gordon\'s Bay — tiny hidden cove, perfect for snorkelling',
                '📸 The cliffs between Bondi and Tamarama are jaw-dropping'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Sunset at Opera Bar',
              description: "End your trip where it began — at the harbour. Opera Bar, nestled under the Opera House sails, is the ultimate spot for sunset drinks. Watch the sky turn pink over the Harbour Bridge and raise a glass to Sydney, summer, and love.",
              details: [
                '🍸 Opera Bar — no reservations, first come first served',
                '🌅 Grab a spot by 6:30pm for prime sunset viewing',
                '🎵 Live music most evenings — relaxed harbour vibes'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Aria Restaurant',
              description: "Matt Moran's Aria overlooks the harbour with the Bridge lit up at night. Modern Australian cuisine with impeccable service — the perfect farewell dinner.",
              meta: '💰 $$$$ · 📍 1 Macquarie St, Circular Quay'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.7970, lng: 151.2878, label: 'Manly Beach', num: 1, cat: 'attraction', desc: 'Gorgeous surf beach reached by iconic harbour ferry' },
        { lat: -33.8008, lng: 151.2990, label: 'Shelly Beach', num: 2, cat: 'attraction', desc: 'Sheltered cove near Manly, great for snorkelling' },
        { lat: -33.8915, lng: 151.2767, label: 'Bondi Beach', num: 3, cat: 'attraction', desc: 'Start of the Bondi to Coogee coastal walk' },
        { lat: -33.9200, lng: 151.2578, label: 'Coogee Beach', num: 4, cat: 'attraction', desc: 'End point of the famous coastal walk' },
        { lat: -33.8571, lng: 151.2151, label: 'Opera Bar', num: 5, cat: 'food', desc: 'Harbourside bar under the Opera House sails' },
        { lat: -33.8610, lng: 151.2127, label: 'Aria Restaurant', num: 6, cat: 'food', desc: 'Fine dining with harbour bridge views — farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$200–350/night', midrange: '$350–600/night', luxury: '$600–1200/night' },
    { category: 'Meals (per couple)', budget: '$80–120/day', midrange: '$150–250/day', luxury: '$300–500/day' },
    { category: 'Transport', budget: '$20–40/day', midrange: '$40–80/day', luxury: '$100–200/day (private)' },
    { category: 'Activities', budget: '$0–50/day', midrange: '$50–150/day', luxury: '$150–400/day' },
    { category: 'Harbour Cruise', budget: '$80–120pp', midrange: '$150–250pp', luxury: '$300–500pp' },
    { category: '6-Day Total (couple)', budget: '$2,500–4,500', midrange: '$5,000–9,000', luxury: '$10,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Sydney Kingsford Smith Airport (SYD) is 8km from the CBD', 'Train to Central or Circular Quay takes 15–20 mins', 'Uber/taxi from airport is about $40–60 AUD'] },
    { title: '🏨 Where to Stay', items: ['Park Hyatt — harbour views, next to Opera House (luxury)', 'Pier One — The Rocks, waterfront boutique hotel', 'Potts Point — charming neighbourhood with boutique stays', 'Bondi area — for beach lovers who want sand on their doorstep'] },
    { title: '🌡️ Weather', items: ['Late December averages 25–30°C (77–86°F)', 'UV index is extreme — wear SPF 50+, hat, and sunglasses', 'Occasional summer thunderstorms pass quickly', 'Sunset around 8pm — long, warm evenings'] },
    { title: '💳 Money', items: ['Tap-and-go payments are universal', 'Many places are cashless — card/phone is all you need', 'Tipping appreciated but not expected (10% for great service)'] },
    { title: '📱 Connectivity', items: ['Buy an eSIM or prepaid Optus/Telstra SIM at the airport', 'Coverage is excellent across Sydney and Blue Mountains towns', 'Free WiFi at most cafés, hotels, and public spaces'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
