const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772993384125_hbmuod',
  email: 'rotopin377@pckage.com',
  destination: 'Vietnam',
  startDate: '2026-03-12',
  endDate: '2026-03-21',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Vietnam',
  countryEmoji: '🇻🇳',
  title: 'Vietnam: Noodles, Temples & Lantern-Lit Nights',
  subtitle: '9 days of ancient citadels, street food obsessions & breezy Hoi An for the solo explorer',
  description: "Vietnam is the kind of destination that rewires you. This 9-day solo journey threads together the best of the country's cultural heart — egg coffee in Hanoi's crumbling French quarter, the imperial grandeur of Hue's walled citadel, the Hai Van Pass with the South China Sea shimmering below, and Hoi An at dusk when a thousand paper lanterns turn the Thu Bon River gold. Under $1,000 total. Not a typo. Vietnam is incredibly generous to the curious traveler: a bowl of pho costs less than a coffee back home, a heritage hotel room goes for $25/night, and the experiences — a dawn motorbike through the Old Quarter, a cooking class in a 300-year-old shophouse — are priceless. Three cities. Three moods. One unforgettable solo trip.",
  duration: '9 nights',
  dates: 'Mar 12 – Mar 21, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Solo Travelers',
  highlights: [
    'Egg coffee ritual at Cà Phê Trứng in Hanoi\'s Old Quarter',
    'Pho at dawn from a sidewalk plastic stool',
    'Hue\'s Imperial Citadel and the royal tomb of Tu Duc',
    'Riding the Hai Van Pass with ocean views to infinity',
    'Hoi An Old Town glowing under a thousand paper lanterns',
    'Banh mi at Banh Mi Phuong — the sandwich that changed the world',
    'A traditional cooking class in a 300-year-old Hoi An home',
    'Sunset beers at An Bang Beach with sand between your toes'
  ],

  essentials: [
    { title: '🌤️ March Weather', text: 'March is ideal in Hanoi (cool, 20-25°C) and gorgeous in Hue and Hoi An (warm, 25-28°C, low rain). Central Vietnam\'s dry season runs Feb–July. Pack light layers for Hanoi nights and pure linen for the south.' },
    { title: '🛵 Getting Around', text: 'Within cities: Grab (Southeast Asia\'s Uber) is cheap and reliable. Between cities: budget airlines (VietJet, Bamboo) connect Hanoi→Hue for ~$20-40. Hue→Hoi An: hire a car or motorbike taxi over the Hai Van Pass ($15-25pp) — the most beautiful road in Vietnam. Do not miss it.' },
    { title: '💵 Money & Budget', text: 'Vietnam runs on cash (Vietnamese Dong). ATMs are everywhere — withdraw 2-3 million VND at a time. Under $1,000 for 9 days is very achievable: hostel dorms ~$8-12/night, budget private rooms ~$20-30/night, street meals ~$1-3, restaurant meals ~$5-10. Daily spend: ~$40-60.' },
    { title: '🍜 Street Food Rules', text: 'The best food is on the street. Look for plastic stools, long lines of locals, and vats of broth that have been simmering since 4am. Bun Bo Hue at 7am, Banh Mi at noon, Bun Cha at lunch, Cao Lau at dinner. Say yes to everything. Your stomach will be fine.' },
    { title: '📱 SIM Card', text: 'Buy a local SIM at the airport (Viettel or Vinaphone) for ~$3-5. Unlimited data for 30 days. Grab app uses data for navigation and rides — essential for solo travel. Download it before you land.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-12',
      neighborhoods: 'Old Quarter · Hoàn Kiếm · French Quarter',
      title: 'Hanoi Arrival — Into the Beautiful Chaos',
      description: "Land in Hanoi and let the city hit you like a warm, slightly chaotic wave. The Old Quarter is 36 streets of motorbike madness, French colonial peeling plaster, and street food sizzling on every corner. Tonight: your first bowl of pho, your first bia hoi, and a walk around Hoan Kiem Lake as it lights up for the evening.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Old Quarter First Walk',
              description: 'Drop your bags and dive straight into the Old Quarter — a dense 1km² maze of streets each historically named after the goods sold there (Silk Street, Paper Street, Tin Street). Walk without a plan. Get lost. Find your way back by smell.',
              details: [
                '🏨 Stay in the Old Quarter — Hang Be, Hang Bac, or Luong Ngoc Quyen streets have great budget guesthouses ($15-30/night)',
                '🛺 From the airport: take a Grab car (~$10) or the bus 86 ($2) to the Old Quarter',
                '🚶 Walk Hang Gai (Silk Street) → Hang Bac (Silver Street) → Hang Be Market to soak in the vibe'
              ]
            }
          ],
          meals: [
            {
              type: '☕ First Coffee',
              name: 'Cà Phê Trứng (Café Giang)',
              description: 'Hanoi\'s legendary egg coffee. A thick, sweet egg yolk foam floats atop dark Vietnamese robusta. Served in a cup nested in hot water to keep it warm. Life-changing. Non-negotiable on day one.',
              meta: '💰 $ · 📍 39 Nguyễn Hữu Huân St, Hoàn Kiếm · Upstairs balcony has Old Quarter views'
            }
          ],
          tips: [
            { type: 'tip', text: 'Crossing the street in Hanoi: don\'t stop, don\'t run. Walk slowly and steadily. The motorbikes will flow around you like water around a stone. Trust the process.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hoan Kiem Lake at Dusk',
              description: 'The heart of Hanoi softens at sunset. Walk the loop around the lake (3km), cross the red bridge to Ngoc Son Temple, and watch locals doing evening tai chi, badminton, and couples strolling. On weekends, the area around the lake becomes a pedestrian zone.',
              details: [
                '🏯 Ngoc Son Temple sits on a small island — open until 6pm',
                '🌉 The red Huc Bridge (The Rising Sun Bridge) is the money shot at golden hour',
                '📸 The Turtle Tower in the middle of the lake is best photographed from the south shore'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner (First Pho)',
              name: 'Phở Gia Truyền (Bát Đàn)',
              description: 'The most famous pho in Hanoi. Queue up before 7:30am for the best bowls — but they also do dinner. This is pho bac: clear broth, simple toppings, depth you can\'t explain. Locals have been eating here for generations.',
              meta: '💰 $ · 📍 49 Bát Đàn St, Hoàn Kiếm · Cash only · Arrives fast, eat fast, leave — that\'s the drill'
            },
            {
              type: '🍺 Nightcap',
              name: 'Bia Hơi Corner (Tạ Hiện Street)',
              description: 'The most famous street drinking corner in Vietnam. Fresh beer brewed daily, plastic stools on the sidewalk, 10,000 VND (~$0.40) per glass. Order a plate of fried tofu with shrimp paste and join the beautiful mess.',
              meta: '💰 $ · 📍 Tạ Hiện / Lương Ngọc Quyến corner, Old Quarter · Best 8-10pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0342, lng: 105.8490, label: 'Old Quarter', num: 1, cat: 'attraction', desc: '36 ancient trade streets — the chaotic heart of Hanoi' },
        { lat: 21.0287, lng: 105.8526, label: 'Hoan Kiem Lake', num: 2, cat: 'attraction', desc: 'The spiritual center of Hanoi — beautiful at dusk' },
        { lat: 21.0302, lng: 105.8524, label: 'Ngoc Son Temple', num: 3, cat: 'attraction', desc: 'Temple on an island accessed via red wooden bridge' },
        { lat: 21.0353, lng: 105.8494, label: 'Café Giang (Egg Coffee)', num: 4, cat: 'food', desc: 'Hanoi\'s legendary egg coffee — a must on day one' },
        { lat: 21.0376, lng: 105.8478, label: 'Phở Gia Truyền', num: 5, cat: 'food', desc: 'Hanoi\'s most iconic pho spot since 1955' },
        { lat: 21.0357, lng: 105.8512, label: 'Tạ Hiện Bia Hơi Corner', num: 6, cat: 'food', desc: 'Fresh draft beer for $0.40 — classic Hanoi sidewalk drinking' }
      ]
    },
    {
      num: 2,
      date: '2026-03-13',
      neighborhoods: 'Hoàn Kiếm · Ba Đình · West Lake',
      title: 'Hanoi Deep Dive — Temples, Tombs & Uncle Ho',
      description: "Go deeper into Hanoi. Visit the Temple of Literature — Vietnam's first university built in 1070 — then pay respects at the Ho Chi Minh Mausoleum complex. Lunch is bun cha. Afternoon is for the city's most spiritual corners. Evening: Train Street and street food like a local.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ho Chi Minh Mausoleum Complex',
              description: "Vietnam's most solemn site. The granite mausoleum holds Ho Chi Minh's embalmed body (closed Mondays and for annual maintenance Sept-Oct). The surrounding complex includes the Presidential Palace gardens, One Pillar Pagoda, and the Ho Chi Minh Museum — all walkable.",
              details: [
                '⏰ Opens 7:30am–10:30am (closed Mon & Fri). Arrive by 8am to avoid queues',
                '👕 Dress respectfully: no shorts, no sleeveless. Shoulders and knees covered',
                '📸 No photography inside the mausoleum. Silence and no hands in pockets',
                '🌸 One Pillar Pagoda is right next door — a lotus rising from a pond, built 1049'
              ]
            }
          ],
          meals: [
            {
              type: '🌅 Breakfast',
              name: 'Xôi Yến (Sticky Rice)',
              description: 'Grab a paper parcel of xoi (sticky rice) topped with egg, fried shallots, and shredded pork from a street cart near your hotel. The quintessential Hanoi breakfast for under $1.',
              meta: '💰 $ · 📍 35B Nguyễn Hữu Huân or any morning street cart · ~5,000-15,000 VND'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Temple of Literature (Văn Miếu)',
              description: "Founded in 1070, Vietnam's first national university and best-preserved example of traditional Vietnamese architecture. Five courtyards of stone stelae bearing the names of 1,307 doctoral graduates. In spring, the gardens are peaceful — a welcome contrast to the city's energy.",
              details: [
                '🏛️ Open daily 8am–5pm. Entrance: ~30,000 VND (~$1.20)',
                '📚 The Doctors\' Steles (1442-1779) are UNESCO Memory of the World inscriptions',
                '🌿 Quietest in the late morning — the coach tours arrive at noon'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'West Lake & Tran Quoc Pagoda',
              description: "Hanoi's largest lake, ringed by upscale cafés, flower vendors, and quiet residential streets. Tran Quoc Pagoda, Vietnam's oldest Buddhist temple (6th century), sits on a tiny peninsula jutting into the lake — an island of calm amid the city. The lotus flowers bloom in spring.",
              details: [
                '🕌 Tran Quoc Pagoda: free entry, open daily. Most photogenic from across the water',
                '☕ Café DUY TRI on West Lake: famous for ca phe trung (egg coffee) with lake views — a different atmosphere to the Old Quarter version',
                '🚲 Rent a bicycle (~$2/hr) and ride the 17km lake circuit at your own pace'
              ]
            }
          ],
          meals: [
            {
              type: '🍖 Lunch',
              name: 'Bún Chả Hương Liên',
              description: 'The most famous bun cha in Hanoi — the exact restaurant where Anthony Bourdain and Barack Obama ate in 2016. Grilled pork patties in sweet-sour dipping broth with cold rice vermicelli. The Obama Combo (bun cha + spring rolls + bia Hanoi) is still on the menu.',
              meta: '💰 $ · 📍 24 Lê Văn Hưu St, Hai Bà Trưng · ~45,000 VND/person · Queue at noon, go at 11am'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hanoi Train Street',
              description: "A narrow alley where twice daily a full-size train squeezes between residential houses just centimetres from the doorways. Locals sit in tiny cafés literally inside the train's path, retreating seconds before it passes. Surreal, humbling, uniquely Hanoian.",
              details: [
                '🚂 Train times vary — ask your hotel or check that day. Usually 3:30pm and 7:30pm',
                '📍 Enter via 28 Trần Phú — look for the narrow alley on your map app',
                '⚠️ Stand back against the wall when the train comes through'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Dinner Street Crawl',
              name: 'Old Quarter Night Market',
              description: 'Friday–Sunday evenings, Đồng Xuân Night Market takes over the Old Quarter. Graze through: nem cua be (crab spring rolls), bánh cuốn (steamed rice rolls), chả cá (turmeric fish with dill), and bún bò (spicy beef noodles). Eat where the locals are three-deep.',
              meta: '💰 $ · 📍 Đồng Xuân Market area + Hàng Đào pedestrian street · Fri-Sun only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0365, lng: 105.8354, label: 'Ho Chi Minh Mausoleum', num: 1, cat: 'attraction', desc: "Vietnam's most solemn monument — arrive early" },
        { lat: 21.0357, lng: 105.8346, label: 'One Pillar Pagoda', num: 2, cat: 'attraction', desc: 'Iconic lotus-shaped pagoda built in 1049' },
        { lat: 21.0282, lng: 105.8353, label: 'Temple of Literature', num: 3, cat: 'attraction', desc: "Vietnam's first university, founded 1070 — stunning architecture" },
        { lat: 21.0461, lng: 105.8270, label: 'Tran Quoc Pagoda', num: 4, cat: 'attraction', desc: "Vietnam's oldest Buddhist temple on West Lake peninsula" },
        { lat: 21.0503, lng: 105.8228, label: 'West Lake', num: 5, cat: 'attraction', desc: "Hanoi's largest lake — great for cycling and lakeside cafés" },
        { lat: 21.0199, lng: 105.8416, label: 'Bún Chả Hương Liên', num: 6, cat: 'food', desc: 'The Obama-Bourdain bun cha spot — legendary' },
        { lat: 21.0224, lng: 105.8449, label: 'Hanoi Train Street', num: 7, cat: 'attraction', desc: 'Train squeezes through a residential alley twice daily' }
      ]
    },
    {
      num: 3,
      date: '2026-03-14',
      neighborhoods: 'French Quarter · Old Quarter · Dong Xuan Market',
      title: 'Hanoi Last Morning — Markets, Cha Ca & Night Bus South',
      description: "Squeeze the last drops from Hanoi. Morning market run at Dong Xuan, a final street food breakfast, and lunch of Hanoi's most unique dish — cha ca la vong. Catch an afternoon flight or evening bus to Hue for a new chapter.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dong Xuan Market at Opening',
              description: "Hanoi's largest covered market, operating since 1889. Three floors of everything: fresh produce on the ground floor where vendors have been setting up since 3am, fabric and garments above, household goods and souvenirs beyond. Go before 9am when it's lively and local.",
              details: [
                '🕌 Open 6am–7pm · 📍 Đồng Xuân, Hoàn Kiếm',
                '🛍️ Great for Vietnamese coffee beans, dried goods, conical hats, silk fabric',
                '🌅 The surrounding streets (Hàng Chiếu, Hàng Mã) are active at dawn with vendors'
              ]
            },
            {
              title: 'St Joseph\'s Cathedral & French Quarter Walk',
              description: "Hanoi's Gothic neo-Romanesque cathedral sits at the edge of the Old Quarter like a piece of Paris dropped into Southeast Asia. Built 1886. The surrounding streets have excellent coffee shops and French bakeries — Hanoi's colonial café culture at its finest.",
              details: [
                '⛪ Cathedral opens for Mass early morning and periodically — check times',
                '📸 The square in front is beautiful in the morning light',
                '☕ Nearby: Tranquil Books & Coffee (Nguyễn Quang Bích) for good pour-overs'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Head to Hanoi Airport / Bus Station',
              description: "Catch an afternoon flight to Huế (VietJet/Bamboo/Vietnam Airlines: ~$20-40, 1hr) or take an overnight sleeper bus (~$12-18, 12 hrs). The flight is the better option for maximizing time. Noi Bai Airport is 45 minutes north of the Old Quarter.",
              details: [
                '✈️ VietJet HAN→HUI: 1 hour, from $20-40 — book ahead',
                '🚌 Sleeper bus: departs Giáp Bát station ~9pm, arrives Hue ~7am. Budget option.',
                '🚗 Grab to airport: ~$10-12 from Old Quarter, 40-50 minutes'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Bánh Mì Street Cart',
              description: 'One last Hanoi breakfast — grab a bánh mì from the lady with the cart. Pâté, butter, pickled daikon, herbs, and chilli in a crisp baguette. 15,000-25,000 VND. The bread is better in Hanoi than almost anywhere else.',
              meta: '💰 $ · 📍 Any Old Quarter street cart · Look for the ones with the longest queues of locals'
            },
            {
              type: '🐟 Lunch',
              name: 'Chả Cá Lã Vọng',
              description: "Hanoi's most distinctive dish: turmeric-marinated catfish, pan-fried tableside with dill and spring onions, served over vermicelli with peanuts, shrimp paste, and herbs. The original restaurant has operated since the 1800s. Order the set and follow the ritual.",
              meta: '💰 $$ · 📍 14 Chả Cá St, Hoàn Kiếm · ~120,000-150,000 VND · The street is literally named after this dish'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0383, lng: 105.8503, label: 'Dong Xuan Market', num: 1, cat: 'attraction', desc: "Hanoi's largest covered market — best at dawn" },
        { lat: 21.0283, lng: 105.8485, label: "St Joseph's Cathedral", num: 2, cat: 'attraction', desc: 'Gothic cathedral from 1886 — a slice of Paris in Hanoi' },
        { lat: 21.0363, lng: 105.8490, label: 'Chả Cá Lã Vọng', num: 3, cat: 'food', desc: 'Tableside turmeric catfish — Hanoi\'s most iconic dish' },
        { lat: 21.0327, lng: 105.8019, label: 'Noi Bai International Airport', num: 4, cat: 'attraction', desc: 'Hanoi Airport — depart for Hue' }
      ]
    },
    {
      num: 4,
      date: '2026-03-15',
      neighborhoods: 'Hue Citadel · Thuan Thanh · Phuong Duc',
      title: 'Hue — Arrive in the Imperial City',
      description: "Welcome to Hue — Vietnam's former imperial capital, a city of emperors, poets, and the most complex regional cuisine in the country. Check in, cross the Perfume River, and spend the afternoon inside one of Southeast Asia's greatest walled cities. This evening: your first bowl of bun bo Hue.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Imperial Citadel of Hue (Đại Nội)',
              description: "Built between 1804-1833 during the Nguyen Dynasty, the Hue Citadel is a 6km walled complex containing the Forbidden Purple City at its center. Only partially restored after wartime damage — the ruins give it a haunted grandeur. Allow 2-3 hours minimum.",
              details: [
                '🏯 Entrance: 200,000 VND (~$8) — includes main citadel and Forbidden City ruins',
                '⏰ Open daily 7am–5:30pm. Afternoon light is golden and beautiful',
                '🚩 Ngo Mon Gate (Noon Gate): the ceremonial southern entrance — climb the walls for panoramic views',
                '📸 The Thai Hoa Palace (Palace of Supreme Harmony) interior is stunning — lacquer pillars, imperial thrones'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Arrival Coffee',
              name: 'La Carambole Café',
              description: 'Cross the Trang Tien Bridge and settle into a French colonial café on the south bank. Hue has a refined café culture — lemon iced tea (trà chanh) and bánh khoái (Hue crispy pancake) while you plan your citadel visit.',
              meta: '💰 $ · 📍 South bank of Perfume River near Trang Tien Bridge'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Walk Dong Ba Market at Dusk',
              description: "Hue's main market sprawls along the north bank of the Perfume River — best at golden hour when the vendors are in full swing and the river light is magic. The market is famous for Hue specialties: mè xửng (sesame candy), bánh khoái kits, and local shrimp paste (mắm tôm).",
              details: [
                '🌅 The bridge (Truong Tien Bridge) at sunset: one of Vietnam\'s most beautiful bridge views',
                '🛍️ Buy: mè xửng sesame candy (great gifts), conical hats (nón lá)',
                '📍 Open until ~8pm daily · North bank of Perfume River'
              ]
            }
          ],
          meals: [
            {
              type: '🌶️ Dinner',
              name: 'Bún Bò Huế (local shop)',
              description: "Hue's great gift to the world: a fiery, lemongrass-perfumed beef noodle soup with thick round noodles, sliced beef shank, and pork knuckle. It\'s spicier and more complex than Hanoi pho. Eat where locals go at 6pm — look for the yellow sign and plastic stools.",
              meta: '💰 $ · 📍 Bún Bò Huế O Hoa: 11 Lý Thường Kiệt or any local spot with a queue · ~35,000-50,000 VND'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.4698, lng: 107.5769, label: 'Imperial Citadel of Hue', num: 1, cat: 'attraction', desc: 'Walled imperial complex — seat of the Nguyen Dynasty' },
        { lat: 16.4662, lng: 107.5774, label: 'Noon Gate (Ngo Mon)', num: 2, cat: 'attraction', desc: 'Main ceremonial gate — climb for panoramic views' },
        { lat: 16.4631, lng: 107.5797, label: 'Thai Hoa Palace', num: 3, cat: 'attraction', desc: 'Palace of Supreme Harmony — imperial lacquerwork interior' },
        { lat: 16.4719, lng: 107.5834, label: 'Dong Ba Market', num: 4, cat: 'attraction', desc: 'Hue\'s main market on the river — best at dusk' },
        { lat: 16.4738, lng: 107.5814, label: 'Truong Tien Bridge', num: 5, cat: 'attraction', desc: 'Elegant six-arch bridge over the Perfume River — sunset views' },
        { lat: 16.4633, lng: 107.5926, label: 'Bún Bò Huế O Hoa', num: 6, cat: 'food', desc: 'Best bun bo Hue in the city — spicy, rich, unmissable' }
      ]
    },
    {
      num: 5,
      date: '2026-03-16',
      neighborhoods: 'Tu Duc Royal Tomb · Thien Mu · Perfume River',
      title: 'Hue — Royal Tombs, Pagodas & the Perfume River',
      description: "Spend the day exploring Hue's extraordinary legacy scattered along the banks of the Perfume River: the philosopher-emperor Tu Duc's romantic lakeside tomb, the 21-metre Thien Mu Pagoda rising from the riverbank, and a boat journey downstream that feels timeless.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Thien Mu Pagoda by Boat',
              description: "The Pagoda of the Celestial Lady, built 1601, stands on a hill above the Perfume River — the unofficial symbol of Hue. Take a dragon boat from Dong Ba wharf (negotiate: ~$10-15 for a half-day boat with driver) and arrive by water as pilgrims have for centuries.",
              details: [
                '⛵ Dragon boat from Dong Ba Wharf: negotiate ~150,000-200,000 VND for the trip',
                '🕌 Thien Mu Pagoda: free entry. The 7-storey Phuoc Duyen tower was built 1844',
                '🚗 Also inside: the preserved Austin car driven by monk Thich Quang Duc to his protest self-immolation in 1963 — a pivotal moment in history',
                '⏰ Go early (7-8am) for morning prayers and quiet'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Bánh Canh Cua (Crab Noodle Soup)',
              description: "A Hue breakfast specialty: thick tapioca noodles in a rich crab broth, topped with crab meat and fried shallots. Eaten for breakfast at tiny sidewalk shops near the citadel. Deeply satisfying and utterly local.",
              meta: '💰 $ · 📍 Near Dong Ba Market area · Any early-morning spot with the yellow bánh canh cua sign'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tomb of Emperor Tu Duc',
              description: "The most beautiful and romantic of Hue's eight royal tombs. Tu Duc designed it himself as a retreat during his lifetime (1849-1883) — a lakeside pavilion for writing poetry, surrounded by pine forests, artificial lakes, and gardens. He ruled for 35 years, had 104 wives, and never had children. The melancholy is built into the architecture.",
              details: [
                '🏛️ Entrance: 150,000 VND (~$6) · Open daily 7am-5:30pm',
                '📍 7km south of Hue center — hire a motorbike taxi (~$5) or bicycle',
                '🌲 The tomb complex is the size of a small palace. Allow 1.5 hours',
                '🎭 Du Khiem Pavilion on Luu Khiem Lake is the most photogenic spot'
              ]
            },
            {
              title: 'Tomb of Emperor Khai Dinh',
              description: "The most ornate of the Hue tombs — a fusion of Vietnamese and European architecture, completed 1931. The interior is covered floor-to-ceiling in an extraordinary mosaic of porcelain and glass fragments. Strange, spectacular, and unlike anything else in Vietnam.",
              details: [
                '🏛️ Entrance: 150,000 VND (~$6) — or buy a Hue combo ticket for all tombs',
                '📍 12km from Hue center — on the way back from Tu Duc',
                '📸 The stairway with carved dragons is the iconic shot — best in late afternoon light'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Perfume River Sunset',
              description: "Watch the sun set from the riverside promenade near Le Loi street. The Perfume River (Sông Hương) lives up to its name at dusk — named for the fallen flowers that scent the water each autumn. Join locals on the riverside benches and watch the dragon boats drift past.",
              details: [
                '🌅 Best viewpoint: the grassy bank opposite the citadel walls',
                '🎵 Street musicians sometimes play traditional Hue court music (Nhã nhạc) near the riverbank'
              ]
            }
          ],
          meals: [
            {
              type: '🥘 Dinner',
              name: 'Hue Royal Cuisine — Cơm Hến',
              description: "Try Hue's most unique rice dish: com hen — cold rice mixed with baby mussels, shrimp crackers, banana blossom, star fruit, and a spicy shrimp paste. It\'s a sensory collision and a Hue morning/evening tradition. Odd, complex, unforgettable.",
              meta: '💰 $ · 📍 Hàng Me Island (Cồn Hến): take a motorcycle taxi to the island for the most authentic version · ~20,000-30,000 VND'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.4541, lng: 107.5497, label: 'Thien Mu Pagoda', num: 1, cat: 'attraction', desc: '7-storey pagoda from 1601 — symbol of Hue' },
        { lat: 16.4719, lng: 107.5834, label: 'Dong Ba Wharf (Dragon Boats)', num: 2, cat: 'attraction', desc: 'Departure point for dragon boat to Thien Mu' },
        { lat: 16.4518, lng: 107.5528, label: "Tomb of Emperor Tu Duc", num: 3, cat: 'attraction', desc: 'Most romantic royal tomb — lakeside pavilions and pine forests' },
        { lat: 16.4409, lng: 107.5773, label: 'Tomb of Emperor Khai Dinh', num: 4, cat: 'attraction', desc: 'Ornate fusion tomb covered in porcelain mosaic' },
        { lat: 16.4640, lng: 107.5780, label: 'Perfume River Promenade', num: 5, cat: 'attraction', desc: 'Riverside walkway — best at sunset' },
        { lat: 16.4667, lng: 107.5967, label: "Con Hen Island (Cơm Hến)", num: 6, cat: 'food', desc: "Island famous for Hue's unique cold mussel rice dish" }
      ]
    },
    {
      num: 6,
      date: '2026-03-17',
      neighborhoods: 'Hai Van Pass · Lang Co · Hoi An Old Town',
      title: 'The Most Beautiful Road in Vietnam — Hue to Hoi An',
      description: "Today is a journey, not just a transfer. The Hai Van Pass — the 'Ocean Cloud Pass' — is a 21km mountain road where the Truong Son mountain range plunges into the South China Sea. On one side: the East Sea stretching to the horizon. On the other: a thousand shades of green. Anthony Bourdain called this road the most beautiful he'd ever ridden. Arrive in Hoi An by evening — check in, find your street, eat your first banh mi.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hai Van Pass by Motorbike or Car',
              description: "Hire a motorbike taxi (xe om), Easy Rider guide, or a private car ($25-40) for the Hue→Hoi An journey via the Hai Van Pass. Do NOT take the expressway tunnel — it bypasses the entire reason for the journey. The pass summit is at 496m elevation. Pull over at the top — French and American military fortifications remain, and the view is staggering in both directions.",
              details: [
                '🏍️ Easy Rider with driver: ~$25-30 for the full Hue-Hoi An journey (~4-5 hours with stops)',
                '🚗 Private car (split with other travelers): ~$35-40/car',
                '⛽ The pass summit has a small café and snack stalls',
                '📍 Lang Cô Beach: a stunning lagoon halfway — worth a 20-minute beach stop',
                '⛰️ The pass is fog-free and clear in March — you got lucky with the month'
              ]
            }
          ],
          meals: [
            {
              type: '🌊 Beach Stop',
              name: 'Lăng Cô Beach Break',
              description: 'Stop at Lang Co, a spit of land between a lagoon and the sea. If time allows, have a coconut on the beach and swim in the crystal water. This is one of Vietnam\'s most underrated beaches.',
              meta: '💰 $ · 📍 Lang Co, halfway between Hue and Da Nang · ~30,000 VND for beach chair + coconut'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive Hoi An & Check In',
              description: "Drop your bags and breathe it in. Hoi An Ancient Town is a UNESCO World Heritage site — a perfectly preserved 15th-century trading port where Japanese, Chinese, and Dutch merchants once lived. The cars stop at the edge of the old town. Inside: yellow walls, bicycles, jasmine, and the silence of 500 years.",
              details: [
                '🏨 Stay inside or adjacent to the Ancient Town — Tran Phu St area or the riverside',
                '📍 Central Reservations Area: arrive before 5pm to explore in daylight first',
                '🚲 Rent a bicycle ($2/day) immediately — it\'s the ideal speed for Hoi An'
              ]
            },
            {
              title: 'First Walk: Ancient Town Orientation',
              description: "Stroll the main drag — Tran Phu St, then down to the river. Find the Japanese Covered Bridge, peek into the merchant houses (Tan Ky Old House is excellent), and pick your tailor for tomorrow's fitting.",
              details: [
                '🌉 Japanese Covered Bridge (Chùa Cầu): built 1593, still standing, still charming. Entrance ~30,000 VND',
                '🏠 Tan Ky Old House: one of Hoi An\'s best-preserved 200-year-old merchant houses',
                '✂️ Hoi An tailors can make custom clothing in 24-48hrs for $20-80 — pick a shop tonight, bring a reference photo'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hoi An Lantern Night',
              description: "At dusk, the Ancient Town transforms. Paper lanterns glow from every shopfront and float on the river. Wander Nguyen Thai Hoc Street, find a riverside seat, and watch the town become a painting. On the 14th of each lunar month, the town goes completely dark except for lanterns — if the dates align, this is one of the most magical things in Southeast Asia.",
              details: [
                '🏮 Lantern vendors sell floating lotus lanterns for ~10,000 VND — release yours from the river bridge',
                '🌉 Bach Dang Street riverside: best spot for lantern reflections on the Thu Bon River',
                '📸 Golden hour → lantern hour is a continuous magic window 5:30pm–8pm'
              ]
            }
          ],
          meals: [
            {
              type: '🥖 First Banh Mi',
              name: 'Bánh Mì Phượng',
              description: "The most famous banh mi in the world. Anthony Bourdain called it 'a symphony in a sandwich'. Crisp baguette, housemade pâté, char siu pork, cold cuts, pickled daikon and carrot, fresh chilli, and secret sauces. Queue, unwrap, stand on the street, eat. This is why you came.",
              meta: '💰 $ · 📍 2B Phan Châu Trinh St, Hoi An · Open 6:30am–late · ~25,000-35,000 VND · Always a queue, always worth it'
            },
            {
              type: '🍺 Evening Drinks',
              name: 'Riverside Bar on Bach Dang',
              description: "Pull up a riverside chair at any of the open-front bars on Bach Dang Street. Order a Larue (local beer) or a lychee smoothie, watch the lanterns drift, and toast yourself for making it here.",
              meta: '💰 $ · 📍 Bach Dang riverside, Hoi An Old Town · ~20,000-40,000 VND per drink'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.1971, lng: 108.1139, label: 'Hai Van Pass Summit', num: 1, cat: 'attraction', desc: "Vietnam's most spectacular mountain pass — views to infinity" },
        { lat: 16.2195, lng: 108.0780, label: 'Lang Co Beach', num: 2, cat: 'attraction', desc: 'Pristine lagoon beach — stop for a swim on the way south' },
        { lat: 15.8773, lng: 108.3266, label: 'Japanese Covered Bridge', num: 3, cat: 'attraction', desc: '1593 bridge-temple — Hoi An\'s most iconic landmark' },
        { lat: 15.8773, lng: 108.3280, label: 'Tan Ky Old House', num: 4, cat: 'attraction', desc: '200-year-old merchant house — perfectly preserved' },
        { lat: 15.8783, lng: 108.3339, label: 'Hoi An Old Town', num: 5, cat: 'attraction', desc: 'UNESCO Ancient Town — yellow walls, lanterns, bicycles' },
        { lat: 15.8773, lng: 108.3312, label: 'Bánh Mì Phượng', num: 6, cat: 'food', desc: "World's most famous banh mi — Bourdain-approved" },
        { lat: 15.8769, lng: 108.3358, label: 'Bach Dang Riverside', num: 7, cat: 'food', desc: 'Riverside bars with lantern views over Thu Bon River' }
      ]
    },
    {
      num: 7,
      date: '2026-03-18',
      neighborhoods: 'Hoi An Old Town · Central Market · An Hoi Peninsula',
      title: 'Hoi An — Deep in the Ancient Town',
      description: "A full day in the Ancient Town. Morning at the Central Market where Hoi An's food culture begins at 6am. Lunch at a proper restaurant for Cao Lau and White Rose dumplings. Afternoon: tailor fitting and bicycle wander. Evening: cooking class in a lantern-lit kitchen.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hoi An Central Market at Dawn',
              description: "The Hoi An Central Market is best experienced at 6-8am when the vendors are at their most vibrant. A covered market right on the river: freshly caught fish, tropical fruit piled in pyramids, herb sellers arranging their bundles, bánh mì vendors with mobile carts, and the smell of pho stock starting its day.",
              details: [
                '🐟 The fish market section (north end) is busiest at dawn',
                '🌿 Look for rau muống (water spinach), coriander, and Vietnamese basil by the kilo',
                '🍵 Cao lau noodles are only made from water from Hoi An\'s Ba Le Well — you\'ll see them being cut at the market',
                '📍 Nguyễn Hoàng St / Central Market entrance'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast',
              name: 'Mì Quảng at the Market',
              description: "Hoi An's own noodle dish: turmeric-stained flat noodles in a small amount of rich broth (not soup), topped with shrimp, pork, quail eggs, and a handful of sesame rice crackers. Served at market stalls with fresh herbs. Extraordinary for $1.",
              meta: '💰 $ · 📍 Market food stalls, Hoi An Central Market · ~20,000-30,000 VND'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'White Rose Dumplings & Cao Lau',
              description: "Two dishes that exist only in Hoi An — made with local ingredients that supposedly can't be replicated elsewhere. White Rose: shrimp dumplings shaped like white roses, steamed in rice wrappers, topped with crispy shallots. Cao Lau: thick Udon-like noodles (made with ash water from Cham ruins) with char siu pork and bean sprouts. Eat both. No excuses.",
              details: [
                '🌹 White Rose (Banh Bao Banh Vac): the recipe is controlled by one family who supplies all Hoi An restaurants',
                '🍜 Best Cao Lau: Cao Lầu Thanh (corner of Trần Phú and Hội An street)',
                '💡 Cao Lau restaurants only use water from the Ba Le Well — you can visit the well (free, in the old town)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tailor Visit & Bicycle Wander',
              description: "Pick up your custom pieces from the tailor (if you ordered yesterday) or browse the fabric shops on Le Loi Street. Then get on your bicycle and escape the tourist center: cross the bridge to the An Hoi Peninsula for local restaurants and quieter streets, or head north toward the rice paddies.",
              details: [
                '✂️ Reputable tailors: Yaly Couture, Bebe Tailor — prices $20-80 for custom shirts/dresses',
                '🚲 Cross Thu Bon River to An Hoi Island — less touristy, great local lunch spots',
                '🌾 Cycle north on Cua Dai Road through rice paddies — beautiful and flat'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Cooking Class at Hoi An Eco Cooking',
              description: "The best cultural experience in Hoi An. Most classes start with a bicycle ride to the morning market to source ingredients, then move to a traditional kitchen. You\'ll make: white rose dumplings, cao lau, banh xeo (sizzling crêpe), and fresh spring rolls. Then eat what you cooked on a riverside terrace.",
              details: [
                '🍳 Book: Red Bridge Cooking School or Hoi An Eco Cooking ($25-35pp) — book same-day if available',
                '⏰ Evening classes typically start 4-5pm, finish 7-8pm with dinner',
                '🌉 Red Bridge School is set in a garden across the river — boat trip included'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Late Night',
              name: 'The Alley Bar (An Hoi)',
              description: 'After your cooking class dinner, walk across to An Hoi Island\'s bar street for one final drink. The bars here are local and lively without being overwhelming — less backpacker, more neighborhood.',
              meta: '💰 $ · 📍 An Hoi Peninsula bar strip, across the footbridge from Old Town'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8783, lng: 108.3339, label: 'Hoi An Central Market', num: 1, cat: 'attraction', desc: 'The living heart of Hoi An — best at 6-8am' },
        { lat: 15.8787, lng: 108.3367, label: 'Cao Lau Thanh', num: 2, cat: 'food', desc: 'The best Cao Lau in Hoi An — Udon-like noodles unique to this town' },
        { lat: 15.8777, lng: 108.3330, label: 'White Rose Restaurant', num: 3, cat: 'food', desc: 'Only place to try White Rose dumplings at their source' },
        { lat: 15.8793, lng: 108.3345, label: 'Ba Le Well', num: 4, cat: 'attraction', desc: 'Ancient Cham well — water used to make Cao Lau noodles' },
        { lat: 15.8763, lng: 108.3394, label: 'An Hoi Peninsula', num: 5, cat: 'attraction', desc: 'Quiet local island across the river — bikes and local restaurants' },
        { lat: 15.8722, lng: 108.3438, label: 'Red Bridge Cooking School', num: 6, cat: 'attraction', desc: 'Garden cooking school across the river — evening classes' }
      ]
    },
    {
      num: 8,
      date: '2026-03-19',
      neighborhoods: 'My Son Sanctuary · An Bang Beach · Hoi An',
      title: 'My Son Ruins & An Bang Beach — Ancient & Easy',
      description: "Split your day between two millennia: morning at the Cham temple ruins of My Son (a UNESCO site from the 4th century), afternoon at An Bang Beach with the South China Sea lapping at your feet. The perfect blend of culture and relaxation.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'My Son Sanctuary (4th-Century Cham Temples)',
              description: "A hidden valley 40km from Hoi An, ringed by mountains, containing the ruins of the greatest Cham civilization. The Hindu temples were built between the 4th and 14th centuries and dedicated to Shiva. Most were destroyed by US bombing in 1969 — the ruins speak of that loss and of what came before. Eerie, overgrown, beautiful.",
              details: [
                '🏛️ Entrance: 150,000 VND (~$6). Open 6am–5pm',
                '🚌 Day tour from Hoi An: ~$10-15 (including boat ride back on the Thu Bon River)',
                '⏰ Leave by 7:30am to arrive before 9am tour groups — early light is magical',
                '🌿 Wear long trousers (temple etiquette) and bring insect repellent — the jungle presses close',
                '🚤 Book the return boat trip option — you float back down the Thu Bon River past rural Vietnam'
              ]
            }
          ],
          meals: [
            {
              type: '🌅 Early Breakfast',
              name: 'Roadside Pho on the Way',
              description: "Stop at a roadside pho shop on the way to My Son — the further from the tourist center, the better the pho. Point, smile, receive a bowl of something wonderful for 25,000 VND.",
              meta: '💰 $ · 📍 Any roadside shop on the road to My Son · Follow the motorbike traffic'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'An Bang Beach Afternoon',
              description: "5km from the Old Town, An Bang is Hoi An's best beach — long, calm, and still relatively local compared to Cua Dai Beach to the south. March brings warm water (25°C), light wind, and the best swimming conditions of the year.",
              details: [
                '🏖️ Rent a sun lounger: ~50,000-80,000 VND at beach bars (often free with a drink order)',
                '🚲 Bike there from Old Town: 20 minutes through rice paddies',
                '🌊 Water is calm and clear in March — bring goggles for snorkelling around the rocks at the north end',
                '🍺 Eat lunch at Salt Pub (great fish tacos and Vietnamese sharing plates, beach-view terrace)'
              ]
            }
          ],
          meals: [
            {
              type: '🍹 Beach Lunch',
              name: 'Salt Pub, An Bang Beach',
              description: 'The best beach lunch in Hoi An. A relaxed terrace right on the sand with fresh fish, crispy spring rolls, and excellent cocktails. The chargrilled squid is famous.',
              meta: '💰 $$ · 📍 An Bang Beach, Hoi An · Beachfront terrace · Open all day'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset & Night Walk Through the Old Town',
              description: "Walk back into the Ancient Town as the lanterns come on. Browse the fabric shops, pick up hand-embroidered postcards, try the coconut ice cream cart on Tran Phu Street, and soak up the last evening light.",
              details: [
                '🍦 Coconut ice cream cart: corner of Tran Phu and Nguyen Hue — try the pandan or coconut flavors',
                '🌙 By 7pm, the Ancient Town is at its most photogenic — every corner glows',
                '🛍️ Best last-minute shopping: Reaching Out (fair trade handmade goods), 103 Nguyen Thai Hoc'
              ]
            }
          ],
          meals: [
            {
              type: '🐟 Dinner',
              name: 'Morning Glory Restaurant',
              description: "Chef Trinh Diem Vy's flagship restaurant — the gold standard for Hoi An cuisine. Order the white rose dumplings, cao lau, fried wontons, and the mixed herb salad. The presentation is as beautiful as the flavors are precise.",
              meta: '💰 $$ · 📍 106 Nguyễn Thái Học St, Hoi An · Book ahead for evening · ~200,000-350,000 VND pp'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.7707, lng: 108.1269, label: 'My Son Sanctuary', num: 1, cat: 'attraction', desc: 'UNESCO Cham temple ruins from the 4th century — haunting and beautiful' },
        { lat: 15.9023, lng: 108.3620, label: 'An Bang Beach', num: 2, cat: 'attraction', desc: "Hoi An's best beach — calm, warm, and relatively local" },
        { lat: 15.9035, lng: 108.3612, label: 'Salt Pub, An Bang', num: 3, cat: 'food', desc: 'Beachfront terrace — fresh fish, squid, cocktails' },
        { lat: 15.8783, lng: 108.3303, label: 'Morning Glory Restaurant', num: 4, cat: 'food', desc: 'Gold standard Hoi An cuisine by Chef Trinh Diem Vy' },
        { lat: 15.8801, lng: 108.3380, label: 'Hoi An Old Town Lantern Walk', num: 5, cat: 'attraction', desc: 'Ancient Town at its most magical after sunset' }
      ]
    },
    {
      num: 9,
      date: '2026-03-20',
      neighborhoods: 'Hoi An Old Town · Tra Que · An Bang',
      title: 'Last Day in Hoi An — Slow Morning, Herb Village & Farewell',
      description: "Don't rush. Vietnam rewards the slow. Visit Tra Que Herb Village for a sunrise bicycle ride through vegetable gardens. A final bowl of whatever you've loved most. One last walk through the Ancient Town. Then pack your lantern memories and head to the airport.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tra Que Herb Village Bicycle Ride',
              description: "3km north of the Old Town, Tra Que is a tiny farming village that has supplied Hoi An's restaurants with organic herbs and vegetables for generations. Cycle there at sunrise, watch the farmers working by hand in the dawn light, and do a 45-minute 'farmer for a day' session — raking, watering, planting.",
              details: [
                '🌿 Farmer experience: ~100,000-150,000 VND pp, includes breakfast at the village',
                '⏰ Arrive at 6:30-7am for the most beautiful light and the working farmers',
                '🚲 15-minute bicycle ride from the Old Town center',
                '🌱 The herbs grown here: mint, basil, dill, coriander, perilla — you\'ll recognize them from every meal you\'ve had'
              ]
            }
          ],
          meals: [
            {
              type: '🌅 Village Breakfast',
              name: 'Breakfast at Tra Que',
              description: 'After the farming session, eat breakfast at the village — typically banh xeo (sizzling crêpe), fresh rice paper rolls, and herb tea. Grown 10 meters away, cooked while you watch.',
              meta: '💰 $ · 📍 Tra Que Village restaurant (included with farm experience) · ~30,000-50,000 VND'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Final Wander: Ancient Town & the River',
              description: "Take one final, unhurried walk through the Ancient Town. Find the corners you missed. Sit by the river. Visit the Assembly Hall of the Fujian Chinese Congregation if you haven't — the most ornate interior in Hoi An, free to enter. Buy a paper lantern to take home.",
              details: [
                '🏛️ Fujian Assembly Hall (Phước Kiến): 17 Trần Phú — stunning painted altar, dragon courtyard, free',
                '🏮 Paper lanterns from the shops on Le Loi Street: ~50,000-100,000 VND — they pack flat',
                '☕ Final coffee: Café 43 (43 Nguyen Phuc Tan) — rooftop, river views, excellent Vietnamese iced coffee'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Depart for Da Nang Airport',
              description: "Da Nang Airport (DAD) is 30km from Hoi An — about 45 minutes by Grab ($8-12). Allow extra time for Hoi An's bicycle congestion at the exit roads. The closest international hub for your flight home.",
              details: [
                '🚗 Grab or hotel transfer: ~150,000-200,000 VND (~$6-8)',
                '✈️ Allow 2 hours before departure for check-in and security',
                '📱 Da Nang has direct flights to many Asian hubs: Singapore, Bangkok, Seoul, Tokyo'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Final Lunch',
              name: 'One Last Bowl — Your Choice',
              description: "Go back to the dish that hit hardest. Pho? Bun Bo Hue? Cao Lau? White Rose? One final bowl before the airport. Make it count.",
              meta: '💰 $ · 📍 Wherever your instincts take you · ~30,000-60,000 VND · You earned it'
            }
          ],
          tips: [
            { type: 'tip', text: "Take Phuong Dong Road south from Hoi An to Da Nang — it's a scenic coastal road with ocean on your right. A beautiful final view of Vietnam before you fly." }
          ]
        }
      ],
      mapPins: [
        { lat: 15.9085, lng: 108.3255, label: 'Tra Que Herb Village', num: 1, cat: 'attraction', desc: 'Organic herb farming village — sunrise bicycle ride and farmer experience' },
        { lat: 15.8779, lng: 108.3280, label: 'Fujian Assembly Hall', num: 2, cat: 'attraction', desc: 'Most ornate interior in Hoi An — painted altars and dragon courtyard' },
        { lat: 15.8780, lng: 108.3358, label: 'Cafe 43 Rooftop', num: 3, cat: 'food', desc: 'Rooftop coffee with river views — perfect final morning' },
        { lat: 15.8769, lng: 108.3358, label: 'Thu Bon Riverside', num: 4, cat: 'attraction', desc: 'Final walk along the river before departing Hoi An' },
        { lat: 16.0439, lng: 108.1992, label: 'Da Nang International Airport', num: 5, cat: 'attraction', desc: 'Departure airport — 45 minutes from Hoi An' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$8–15/night (dorm)', midrange: '$20–40/night (private)', luxury: '$60–120/night (boutique)' },
    { category: 'Meals', budget: '$5–10/day (street food)', midrange: '$15–25/day (mix)', luxury: '$40–70/day (restaurants)' },
    { category: 'Transport', budget: '$3–8/day (Grab + local)', midrange: '$10–20/day', luxury: '$25–50/day (private)' },
    { category: 'Activities & Entry', budget: '$5–10/day', midrange: '$10–20/day', luxury: '$20–40/day' },
    { category: 'Hue→Hoi An Transfer', budget: '$12–15 (sleeper bus)', midrange: '$25–35 (Easy Rider)', luxury: '$40–60 (private car)' },
    { category: '9-Day Total (Solo)', budget: '$300–450', midrange: '$500–750', luxury: '$800–1,200' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Hanoi Noi Bai (HAN) — most major hubs connect via Doha, Singapore, or Taipei', 'Depart from Da Nang (DAD) — 30km from Hoi An via Grab', 'Domestic flight Hanoi→Hue: $20-40 on VietJet/Bamboo (book 1-2 weeks ahead)'] },
    { title: '🏨 Where to Stay', items: ['Hanoi: Old Quarter guesthouses ($15-25/night) — Hang Be or Hang Bac St area', 'Hue: Riverside guesthouses near Truong Tien Bridge ($15-25/night)', 'Hoi An: Stay inside or adjacent to the Ancient Town ($20-40/night) — the UNESCO area is car-free'] },
    { title: '🌡️ March Weather', items: ['Hanoi: Cool and clear, 18-24°C. Pack a light jacket for evenings.', 'Hue: Warm and dry, 24-28°C. The best month to visit.', 'Hoi An: Perfect beach weather, 26-29°C. Very low rainfall.'] },
    { title: '💰 Money', items: ['Vietnamese Dong (VND): ~25,000 VND = $1 USD', 'Withdraw 2-3M VND at ATMs ($80-120). Fee: ~$2-3 per withdrawal.', 'Street food is cash-only. Cards accepted at most restaurants and hotels.', 'Bargain gently at markets — a friendly smile goes further than hard negotiating'] },
    { title: '📱 Apps & Connectivity', items: ['Grab: Essential for city transport (motorbike or car)', 'Google Maps: Works offline — download Vietnam before you land', 'XE Currency: Instant VND conversions', 'Airport SIM (Viettel): ~$3-5 for 30 days unlimited data'] }
  ]
};

fulfillOrder(order, itineraryData);
