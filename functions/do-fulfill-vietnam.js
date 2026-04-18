#!/usr/bin/env node
/**
 * Fulfill order_1776071489380_w8jtoh
 * Vietnam trip, May 26 - Jun 6, 2026
 * Group: 3-4, Style: Adventure/Cultural/Foodie/Relaxation/Family-friendly
 * Budget: Under $1,000
 */

const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1776071489380_w8jtoh",
  email: "raghu2192@gmail.com",
  destination: "Vietnam",
  start_date: "2026-05-26",
  end_date: "2026-06-06",
  group_size: "3-4",
  travel_style: "Adventure, Cultural, Foodie, Relaxation, Family-friendly",
  dining: "Mix of everything",
  budget: "Under $1,000"
};

const itineraryData = {
  destination: "Vietnam",
  countryEmoji: "🇻🇳",
  title: "11 Nights in Vietnam: From Hanoi Street Food to Saigon Nights",
  subtitle: "A family-friendly adventure through ancient towns, emerald bays, and the world's best street food — without breaking the bank",
  description: "Vietnam is the ultimate budget travel destination, and this 12-day route covers the absolute best of the country. You'll slurp pho at dawn in Hanoi, cruise through limestone karsts in Ha Long Bay, pedal through rice paddies in Ninh Binh, lantern-gaze in Hoi An, walk the imperial halls of Hue, and eat your way through Ho Chi Minh City — all for under $1,000 per person.",
  duration: "12 days",
  dates: "May 26 – Jun 6, 2026",
  budget: "Under $1,000 per person",
  pace: "Moderate",
  bestFor: "Adventure seekers, culture lovers, foodies, families, budget travelers",

  essentials: [
    { title: "✈️ Flights", text: "Fly into Hanoi (HAN), out of Ho Chi Minh City (SGN). Book 2-3 months ahead for best fares. Budget airlines: VietJet, Bamboo Airways." },
    { title: "💴 Money", text: "Vietnamese Dong (VND). ~24,000 VND = $1 USD. ATMs everywhere. Bring USD as backup. Budget: $60-80/day per person covers everything." },
    { title: "📱 SIM Card", text: "Buy at Hanoi airport: Viettel or Vinaphile. ~$10 for 30 days unlimited data. Essential for Grab (ride-hailing app)." },
    { title: "🌡️ Weather", text: "Late May is hot (85-95°F / 29-35°C) with occasional rain. Pack light, breathable clothes, sunscreen, and a compact umbrella." },
    { title: "🛂 Visa", text: "E-visa available online for $25 (90 days single entry). Apply at least 2 weeks before travel at evisa.xuatnhapcanh.gov.vn." },
    { title: "🏥 Health", text: "No required vaccinations. Recommended: Hepatitis A & B, Typhoid. Drink only bottled or filtered water. Mosquito repellent essential." },
    { title: "🚗 Getting Around", text: "Grab (Uber of SE Asia) for city rides. Overnight buses between cities ($10-15). Domestic flights Hanoi→Da Nang ($30-50), Hue→HCMC ($30-50)." },
    { title: "👨‍👩‍👧‍👦 Family Tips", text: "Vietnam is very kid-friendly. Children are welcomed everywhere. Street food is safe at busy stalls. Bring hand sanitizer and a carrier/stroller for younger kids." }
  ],

  days: [
    // ===== DAY 1: ARRIVE HANOI =====
    {
      num: 1,
      neighborhoods: "Hanoi · Old Quarter",
      title: "Welcome to Hanoi — Street Food Capital of the World",
      description: "Land in Hanoi, drop your bags, and dive straight into the sensory overload of the Old Quarter. The streets are the attraction here.",
      timeBlocks: [
        {
          label: "Morning / Arrival",
          activities: [
            {
              title: "Arrive at Noi Bai International Airport (HAN)",
              description: "Take Grab to Old Quarter (~45 min, $8-10). Check into your hotel or hostel. Budget pick: Hanoi Banana Hostel ($8/night). Mid-range: La Siesta Premium ($35/night).",
              details: ["Grab from airport: download the app, set pickup at Terminal 2 arrivals", "Most Old Quarter hotels offer early check-in if you email ahead"]
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Explore the Old Quarter (36 Ancient Streets)",
              description: "Wander the maze of narrow streets, each traditionally dedicated to a different craft. Hàng Gai (silk), Hàng Bạc (silver), Hàng Mã (paper offerings).",
              details: ["Start at Hoàn Kiếm Lake and work your way north", "Don't plan too much — getting lost IS the plan", "Great for families: kids love the chaos and street vendors"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Phở Gia Truyền", description: "Legendary phở bò since 1955. Simple, perfect, cash only. A bowl costs ~$2.", meta: "49 Bát Đàn, open 6am-12pm" }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Hoàn Kiếm Lake & Night Market",
              description: "Walk around the spiritual heart of Hanoi. On weekends, the surrounding streets become a walking zone with food stalls, live music, and games.",
              details: ["Ngọc Sơn Temple on the lake island is beautifully lit at night", "Weekend night market runs Friday-Sunday, 6-11pm"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Bún Chả Hương Liên", description: "The 'Obama bún chả' spot — grilled pork patties in a sweet-savory broth with rice noodles and fresh herbs. ~$3.", meta: "24 Lê Văn Hữu, open 11am-9pm" }
          ],
          tips: [
            { type: "reddit", text: "Don't over-plan Hanoi. The best experiences happen when you just walk and eat. Every corner has something incredible.", cite: "r/VietNam" }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0345, lng: 105.85, label: "Phở Gia Truyền", num: 1, cat: "food", desc: "Legendary phở bò since 1955 — simple, perfect, cash only" },
        { lat: 21.0288, lng: 105.8525, label: "Hoàn Kiếm Lake", num: 2, cat: "sight", desc: "The spiritual heart of Hanoi — morning tai chi, Turtle Tower, Ngọc Sơn Temple" },
        { lat: 21.0335, lng: 105.849, label: "Old Quarter Walking", num: 3, cat: "explore", desc: "Wander the 36 ancient streets — silk, silver, paper, and street food at every turn" },
        { lat: 21.031, lng: 105.853, label: "Bún Chả Hương Liên", num: 4, cat: "food", desc: "The 'Obama bún chả' spot — grilled pork, herbs, dipping broth perfection" },
        { lat: 21.033, lng: 105.851, label: "Night Market / Tạ Hiện", num: 5, cat: "nightlife", desc: "Weekend walking streets with food stalls, live music, and the famous bia hơi corner" }
      ]
    },

    // ===== DAY 2: HANOI CULTURAL DEEP DIVE =====
    {
      num: 2,
      neighborhoods: "Hanoi · Ba Đình · West Lake",
      title: "Temples, Prisons & Egg Coffee — Hanoi Deep Dive",
      description: "Today goes deeper into Hanoi's complex history and vibrant cafe culture. Start early to beat the heat and the crowds.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Hồ Chí Minh Mausoleum & One Pillar Pagoda",
              description: "Vietnam's most solemn monument. The preserved body of Uncle Hồ lies in a grand Soviet-style building. Dress modestly, no photos inside.",
              details: ["Open 7:30-10:30am (closed Mon & Fri). Get there by 8am", "One Pillar Pagoda is right next door — iconic 11th-century lotus-shaped temple", "Kids find the pagoda fascinating — it literally sits on one pillar"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Bánh Cuốn Bà Hoành", description: "Steamed rice rolls filled with minced pork and wood ear mushroom — ethereal texture. ~$1.50.", meta: "Steet-side on Hàng Bạc, arrive before 9am" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Hỏa Lò Prison Museum ('Hanoi Hilton')",
              description: "A French colonial prison later used during the Vietnam War. Powerful and sobering. Allow 1-1.5 hours.",
              details: ["Entrance: ~$1.25 (30,000 VND)", "Audio guide available and highly recommended", "Older kids can handle it — it's educational, not gory"]
            },
            {
              title: "Temple of Literature (Văn Miếu)",
              description: "Vietnam's first university, founded in 1070. Beautiful Confucian temple with stone stelae of doctoral graduates.",
              details: ["Entrance: ~$1.25", "Peaceful gardens perfect for a midday rest", "Kids love the tortoise stelae — each one names a scholar from centuries ago"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Chả Cá Thăng Long", description: "Hanoi's signature dish: turmeric-marinated fish cooked tableside with heaps of dill and spring onion. ~$4.", meta: "21 Đường Thanh, open 11am-10pm" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "West Lake (Hồ Tây) & Trấn Quốc Pagoda",
              description: "Hanoi's largest lake. Rent bicycles or take a Grab around the perimeter. Stop at Vietnam's oldest Buddhist temple (6th century).",
              details: ["Bike rental: ~$2/day", "Trấn Quốc Pagoda is stunning at sunset", "Lotus flowers bloom in the lake during summer months"]
            }
          ],
          meals: [
            { type: "Snack", name: "Café Giảng (Egg Coffee)", description: "The birthplace of egg coffee — a Hanoi invention. Whisked egg yolk over strong Vietnamese coffee. ~$1.", meta: "Hidden upstairs at 39 Nguyễn Hữu Huân" }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Thăng Long Water Puppet Theatre",
              description: "Traditional Vietnamese water puppetry — a uniquely Hanoian art form dating back 1,000 years. Great for kids.",
              details: ["Show at 5pm or 8pm, ~$3-5 per ticket", "Book ahead online or through your hotel", "The live traditional music is half the experience"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Bia Hơi Corner (Tạ Hiện Street)", description: "Fresh draft beer for 5,000 VND (~$0.20) per glass. Sit on tiny plastic stools, order peanuts and dried squid, and soak in the atmosphere.", meta: "Corner of Tạ Hiện & Lương Ngọc Quyến" }
          ],
          tips: [
            { type: "reddit", text: "Hanoi is cheap but the mausoleum has strict dress code — cover shoulders and knees. They'll turn you away otherwise.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0369, lng: 105.8345, label: "Hồ Chí Minh Mausoleum", num: 1, cat: "sight", desc: "Vietnam's most solemn monument — arrive by 8am, dress modestly" },
        { lat: 21.0363, lng: 105.834, label: "One Pillar Pagoda", num: 2, cat: "sight", desc: "Iconic lotus-shaped pagoda from the 11th century" },
        { lat: 21.0285, lng: 105.8472, label: "Hỏa Lò Prison Museum", num: 3, cat: "culture", desc: "'Hanoi Hilton' — French colonial prison turned powerful war museum" },
        { lat: 21.0295, lng: 105.8485, label: "Temple of Literature", num: 4, cat: "culture", desc: "Vietnam's first university (1070) — stone stelae of ancient scholars" },
        { lat: 21.0475, lng: 105.8365, label: "Trấn Quốc Pagoda", num: 5, cat: "sight", desc: "Vietnam's oldest Buddhist temple (6th century) — stunning on West Lake" },
        { lat: 21.031, lng: 105.85, label: "Café Giảng", num: 6, cat: "coffee", desc: "Birthplace of egg coffee — hidden upstairs, uniquely Hanoian" },
        { lat: 21.033, lng: 105.851, label: "Bia Hơi Corner", num: 7, cat: "nightlife", desc: "Fresh draft beer for $0.20 — plastic stools, street-side, perfection" }
      ]
    },

    // ===== DAY 3: HANOI → HA LONG BAY =====
    {
      num: 3,
      neighborhoods: "Hanoi → Ha Long Bay",
      title: "Into the Emerald Dragon — Ha Long Bay Cruise",
      description: "Leave Hanoi early and head to one of the most spectacular natural wonders on Earth. Nearly 2,000 limestone islands rising from emerald waters.",
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            {
              title: "Depart Hanoi for Ha Long Bay",
              description: "Most cruise operators provide shuttle bus from Hanoi Old Quarter (included in cruise price). 2.5-3 hour drive. Leave by 8am.",
              details: ["Cruise pickup typically 7:30-8:30am from your hotel", "Book a 2-day/1-night cruise: $40-70/person all-inclusive", "Recommended: Swan Cruises, Stellar of the Seas, or Renea Cruises for budget-friendly options"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Grab Banh Mi To-Go", description: "Grab a banh mi from a street stall near your hotel (~$1) before the shuttle picks you up.", meta: "Any Banh Mi stand in Old Quarter — look for the crowds" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Board Cruise & Sail into Ha Long Bay",
              description: "Board your junk boat at Tuan Chau Marina. Lunch on board as you sail into the bay's dramatic limestone karst landscape.",
              details: ["Safety briefing and cabin assignment", "Upper deck has the best views — claim a lounge chair", "Kids love exploring the boat — many have sundecks and kayaks"]
            }
          ],
          meals: [
            { type: "Lunch", name: "On-Board Seafood Lunch", description: "Included in cruise package. Fresh seafood, spring rolls, and Vietnamese dishes. Usually excellent quality.", meta: "Included in cruise price" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Kayaking or Bamboo Boat through Lagoons",
              description: "Paddle through hidden lagoons and caves. The water is calm and warm. Suitable for beginners and families with older kids.",
              details: ["Double kayaks available — perfect for parent + child", "Life jackets provided for all sizes", "Alternative: take a bamboo rowboat guided by locals"]
            },
            {
              title: "Visit Surprise Cave (Sung Sot)",
              description: "One of Ha Long Bay's largest and most spectacular caves. Walk through enormous chambers with stalactites and stalagmites.",
              details: ["About 200 steps to reach the cave entrance", "Well-lit with walkways — manageable for kids 5+", "The second chamber is the size of a cathedral"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Sunset on Deck & Squid Fishing",
              description: "Watch the sunset paint the limestone towers gold and pink. Many cruises offer night-time squid fishing off the boat — fun for the whole family.",
              details: ["Squid fishing gear provided by crew", "If you catch one, the kitchen will cook it for breakfast", "Stargazing is incredible here — zero light pollution"]
            }
          ],
          meals: [
            { type: "Dinner", name: "On-Board Dinner", description: "Multi-course Vietnamese dinner on the cruise. Usually includes grilled seafood, hot pot, and fruit platters.", meta: "Included in cruise price" }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0345, lng: 105.85, label: "Hanoi Old Quarter Pickup", num: 1, cat: "transport", desc: "Cruise shuttle picks up from Old Quarter hotels around 8am" },
        { lat: 20.9101, lng: 107.1839, label: "Tuan Chau Marina", num: 2, cat: "transport", desc: "Board your cruise boat here — 2.5hr drive from Hanoi" },
        { lat: 20.9232, lng: 107.1437, label: "Ha Long Bay Limestone Karsts", num: 3, cat: "sight", desc: "Nearly 2,000 limestone islands — UNESCO World Heritage Site" },
        { lat: 20.9169, lng: 107.1044, label: "Surprise Cave (Sung Sot)", num: 4, cat: "explore", desc: "Enormous cathedral-like cave chambers with stalactites" },
        { lat: 20.9025, lng: 107.1458, label: "Kayaking Lagoon", num: 5, cat: "adventure", desc: "Paddle through hidden lagoons between limestone karsts" }
      ]
    },

    // ===== DAY 4: HA LONG BAY → NINH BINH =====
    {
      num: 4,
      neighborhoods: "Ha Long Bay → Ninh Binh",
      title: "Dawn on the Bay & Journey to Inland Ha Long",
      description: "Wake up on the bay, do sunrise Tai Chi, then head south to Ninh Binh — the 'inland Ha Long Bay' with limestone peaks rising from rice paddies.",
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            {
              title: "Sunrise Tai Chi on the Sundeck",
              description: "Most cruises offer a 6am Tai Chi session on the upper deck. The bay is magical at dawn — mist rising between the karsts.",
              details: ["Worth waking up for — the light at 5:30-6:30am is extraordinary", "Coffee and tea available from 5:30am"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "On-Board Breakfast", description: "Full buffet breakfast on the cruise. Pho, eggs, fresh fruit, and Vietnamese coffee.", meta: "Included in cruise price" }
          ]
        },
        {
          label: "Morning",
          activities: [
            {
              title: "Morning Activity & Cruise Disembarkation",
              description: "Final cruise activity (usually a cooking class or visit to a floating fishing village), then disembark by 11:30am.",
              details: ["Cooking class: learn to make spring rolls — fun for the whole family", "Floating village: see how local fishing families live on the water"]
            }
          ],
          meals: [
            { type: "Lunch", name: "On-Board Brunch", description: "Early lunch on board before disembarking. Usually a lighter meal of noodles and spring rolls.", meta: "Included in cruise price" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Transfer to Ninh Binh (2 hours)",
              description: "Arrange a private car from Ha Long to Ninh Binh (~$30-40 for the group, 2 hours). Alternatively, return to Hanoi first and take a train or bus south.",
              details: ["Private car is most convenient with a group", "Scenic drive through rural northern Vietnam", "Check into Ninh Binh hotel: Tam Coc Riverside Homestay ($15/night) or Chezbeo Homestay ($20/night)"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Relax at Homestay & Explore Tam Coc Town",
              description: "Ninh Binh is rural and peaceful. Take a sunset walk through the rice paddies, or rent bicycles from your homestay.",
              details: ["Tam Coc town is small and walkable", "Most homestays have hammocks and gardens — pure relaxation", "Kids can run around freely in the countryside"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Goat Meat at Local Restaurant", description: "Ninh Bình's specialty — grilled mountain goat (thịt dê) with herbs, rice paper wraps, and dipping sauce. A unique regional dish. ~$3-5.", meta: "Any 'Thịt Dê' restaurant in town — your host will point you to the best one" }
          ],
          tips: [
            { type: "reddit", text: "Ninh Binh is the underrated gem of Vietnam. Most tourists rush through but spending 2 nights here is the move. The scenery is jaw-dropping and it's way less crowded than Ha Long Bay.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 20.9075, lng: 107.1387, label: "Ha Long Bay Dawn", num: 1, cat: "sight", desc: "Sunrise Tai Chi on the sundeck — mist rising between limestone karsts" },
        { lat: 20.2512, lng: 105.9745, label: "Ninh Binh Town", num: 2, cat: "transport", desc: "Scenic 2-hour drive from Ha Long to the 'inland Ha Long Bay'" },
        { lat: 20.2476, lng: 105.9587, label: "Tam Coc Rice Paddies", num: 3, cat: "explore", desc: "Peaceful countryside walks and cycling through rice paddies at golden hour" },
        { lat: 20.25, lng: 105.96, label: "Local Goat Meat Restaurant", num: 4, cat: "food", desc: "Ninh Bình's famous grilled mountain goat with herbs and rice paper" }
      ]
    },

    // ===== DAY 5: NINH BINH ADVENTURE =====
    {
      num: 5,
      neighborhoods: "Ninh Binh · Tam Cốc · Mùa Caves",
      title: "Rivers, Caves & Dragon Peaks — Ninh Bình Adventure Day",
      description: "Today is pure adventure: rowboat through limestone caves, climb 500 steps to a dragon viewpoint, and cycle through timeless villages.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Tràng An Boat Ride (UNESCO Site)",
              description: "A 2-hour rowboat journey through a network of rivers, caves, and temples nestled between towering limestone peaks. Better than Tam Coc and less touristy.",
              details: ["Entrance: ~$9 (250,000 VND) per boat — fits 2 adults + 1 child", "Rower does all the work — you sit back and take photos", "Passes through 9 caves — some you have to duck!", "Kids absolutely love this — it's like a real-life theme park ride"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Homestay Breakfast", description: "Most homestays include a simple breakfast of pho, eggs, and fruit.", meta: "Included with accommodation" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Climb Mùa Caves Viewpoint",
              description: "500 stone steps to a summit crowned with a dragon statue. The panoramic view of the Tam Coc valley is one of Vietnam's most iconic sights.",
              details: ["Entrance: ~$2 (50,000 VND)", "Go early or late to avoid midday heat", "The climb is steep but manageable — take breaks", "Kids 6+ can handle it with encouragement and snacks at the top"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Tam Coc Riverside Lunch", description: "Com tam (broken rice) with grilled pork, or bun cha at a riverside restaurant. ~$2.", meta: "Restaurants along the Tam Coc boat dock area" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Bicycle Tour through Local Villages",
              description: "Rent bikes from your homestay (~$1/day) and pedal through rice paddies, past water buffalo, and through tiny villages where life hasn't changed in centuries.",
              details: ["Flat terrain — easy cycling for the whole family", "Stop at Bich Dong Pagoda (ancient cave temple)", "Cross wooden bridges and ride along river paths", "Great photography opportunities everywhere"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Sunset at Tam Coc Pier & Dinner",
              description: "Watch the sun set behind the limestone karsts from the Tam Coc viewing platform. Then enjoy a relaxed dinner at your homestay.",
              details: ["Many homestays offer family-style dinner for ~$3-5/person", "Great way to meet other travelers and share stories"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Homestay Family Dinner", description: "Home-cooked Vietnamese family meal — multiple dishes shared around a table. Spring rolls, stir-fried morning glory, grilled fish, and rice. ~$3-5.", meta: "Ask your host to prepare dinner — they're often the best meals of the trip" }
          ],
          tips: [
            { type: "reddit", text: "Trang An > Tam Coc for the boat ride. More caves, less crowded, UNESCO listed. Do Mua Caves in the morning before it gets hot — the view is insane.", cite: "r/VietNam" }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2578, lng: 105.8948, label: "Tràng An Boat Dock", num: 1, cat: "adventure", desc: "2-hour rowboat through caves, rivers, and temples between limestone peaks" },
        { lat: 20.251, lng: 105.874, label: "Mùa Caves Viewpoint", num: 2, cat: "adventure", desc: "500 steps to dragon statue summit — panoramic views of Tam Coc valley" },
        { lat: 20.245, lng: 105.885, label: "Bicycle Route through Villages", num: 3, cat: "explore", desc: "Ride through rice paddies, past water buffalo, and ancient villages" },
        { lat: 20.2476, lng: 105.9587, label: "Tam Coc Sunset View", num: 4, cat: "sight", desc: "Watch the sun set behind limestone karsts from the viewing platform" }
      ]
    },

    // ===== DAY 6: NINH BINH → HOI AN =====
    {
      num: 6,
      neighborhoods: "Ninh Binh → Flight to Da Nang → Hoi An",
      title: "Southward Bound — Landing in Lantern Town",
      description: "Travel day: transfer from Ninh Binh to Hanoi airport (2 hours), fly to Da Nang, then a short drive to the magical lantern-lit town of Hoi An.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Transfer to Hanoi Airport",
              description: "Private car from Ninh Binh to Noi Bai Airport (2 hours). Book through your homestay (~$25-35 for the group).",
              details: ["Leave by 7am for a 10-11am flight", "Pack snacks for the ride"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Homestay Breakfast", description: "Quick breakfast before the drive. Most hosts will prepare something early if you ask the night before.", meta: "Included with accommodation" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Fly Hanoi (HAN) → Da Nang (DAD)",
              description: "1.5-hour flight. Budget airlines: VietJet ($25-40), Bamboo Airways ($30-50). Book 2+ weeks ahead for best prices.",
              details: ["VietJet is cheapest but strict on baggage — pre-pay for checked bags", "Da Nang airport is small and efficient — out in 15 minutes", "Grab from Da Nang airport to Hoi An: ~$12, 45 minutes"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Airport or In-Flight", description: "Grab a banh mi at Hanoi airport or buy a snack on board.", meta: "~$3-5" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Arrive in Hoi An & Check In",
              description: "Hoi An's Ancient Town is one of the most beautiful places in Vietnam. Check into your hotel and start exploring.",
              details: ["Budget: Hoi An Historic Hotel ($20/night)", "Mid-range: La An Central Villa ($40/night)", "The town is flat and walkable — great for families with kids"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Hoi An Ancient Town at Night",
              description: "The old town glows with thousands of silk lanterns at night. Walk along the Thu Bon River, release a paper lantern on the water, and browse the artisan shops.",
              details: ["Ancient Town ticket: ~$3 (one-time pass valid for your entire stay)", "Lantern boats on the river: ~$1-2 per person", "Kids love the lantern-making workshops — ~$3-5 per person", "Tailor shops everywhere — get measured for custom clothes (24hr turnaround!)"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Cao Lầu at Morning Glory", description: "Hoi An's signature dish: thick noodles in a small amount of broth with herbs, pork, and crispy croutons. Unique to this town. ~$3.", meta: "Morning Glory Restaurant, 106 Nguyễn Thái Học" }
          ],
          tips: [
            { type: "reddit", text: "Hoi An is the most beautiful town in Vietnam. At night with all the lanterns lit up, it looks like a fairy tale. Go with zero expectations and you'll be blown away.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2512, lng: 105.9745, label: "Ninh Binh Departure", num: 1, cat: "transport", desc: "Transfer to Hanoi airport — 2 hour scenic drive" },
        { lat: 21.2212, lng: 105.808, label: "Noi Bai Airport (HAN)", num: 2, cat: "transport", desc: "Fly to Da Nang — 1.5 hours, $25-50" },
        { lat: 16.0439, lng: 108.1995, label: "Da Nang Airport (DAD)", num: 3, cat: "transport", desc: "Land here — 45 min Grab to Hoi An (~$12)" },
        { lat: 15.8801, lng: 108.338, label: "Hoi An Ancient Town", num: 4, cat: "sight", desc: "Lantern-lit UNESCO old town — magical at night" },
        { lat: 15.8783, lng: 108.3358, label: "Thu Bon River Lantern Boats", num: 5, cat: "sight", desc: "Release paper lanterns on the river — $1-2 per person" }
      ]
    },

    // ===== DAY 7: HOI AN =====
    {
      num: 7,
      neighborhoods: "Hoi An · Ancient Town · Cam Thanh",
      title: "Cooking Classes, Tailors & Rice Paddies — Hoi An Immersion",
      description: "Hoi An is designed for wandering. Today: learn to cook Vietnamese food, visit a water coconut village, and explore the famous tailor shops.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Hoi An Cooking Class",
              description: "Start with a market tour to buy ingredients, then learn to cook 3-4 Vietnamese dishes. Most classes include a visit to the herb gardens.",
              details: ["Recommended: Green Bamboo Cooking Class (~$20/person)", "Market tour is fascinating — kids love seeing the exotic fruits and live seafood", "You'll eat everything you cook for lunch", "Vegetarian options available"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Bánh Mì Phượng", description: "Anthony Bourdain's favorite banh mi in Vietnam. Crispy baguette, pâté, herbs, and your choice of protein. ~$1.", meta: "2B Phan Châu Trinh, open 6:30am-9pm" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Eat Your Cooking Class Creations",
              description: "Enjoy the meal you just prepared. Most classes cover spring rolls, papaya salad, and a main dish like lemongrass chicken or fish in banana leaf.",
              details: ["Classes usually end around 1-2pm", "Take photos of the recipes — you'll want to recreate these at home"]
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Cam Thanh Water Coconut Village",
              description: "Take a round bamboo boat (thuyền thúng) through the water coconut palm forest. The boat spins and twirls — kids think it's a ride.",
              details: ["Bamboo boat ride: ~$5-8 per person", "The boat drivers are entertainers — they'll spin you around", "About 20 minutes from Hoi An center by Grab (~$3)"]
            },
            {
              title: "Explore Tailor Shops",
              description: "Hoi An is famous for custom tailoring. Get measured for a suit, dress, or áo dài (traditional Vietnamese outfit) — ready in 24-48 hours.",
              details: ["Custom suits from $60-100, dresses from $30-50", "Recommended: BeBe Tailor, Yaly Couture, Bao Khanh Silk", "Bring a photo of what you want — they can copy anything"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Ancient Town Walking & Japanese Bridge",
              description: "Visit the iconic Japanese Covered Bridge (built in the 1590s), the colorful Chinese assembly halls, and the preserved merchant houses.",
              details: ["The bridge is lit up beautifully at night", "Assembly halls have intricate carvings and incense-filled rooms", "Street musicians often play near the central market"]
            }
          ],
          meals: [
            { type: "Dinner", name: "White Rose Dumplings", description: "Another Hoi An exclusive — delicate translucent shrimp dumplings shaped like roses. Only one family makes them in the whole town. ~$2.", meta: "Restaurant on Nha Truong Street — look for the 'White Rose' sign" }
          ],
          tips: [
            { type: "reddit", text: "Get clothes tailored in Hoi An. It's absurdly cheap and the quality is legit. I got a full suit, 3 shirts, and a coat for under $200.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8765, lng: 108.3357, label: "Hoi An Central Market", num: 1, cat: "food", desc: "Start your cooking class market tour here — exotic fruits, live seafood, fresh herbs" },
        { lat: 15.8801, lng: 108.338, label: "Japanese Covered Bridge", num: 2, cat: "sight", desc: "Iconic 1590s bridge — the symbol of Hoi An, lit up at night" },
        { lat: 15.8712, lng: 108.3538, label: "Cam Thanh Coconut Village", num: 3, cat: "adventure", desc: "Spin in round bamboo boats through water coconut palms" },
        { lat: 15.8793, lng: 108.3362, label: "Tailor Shops", num: 4, cat: "shopping", desc: "Custom clothing in 24-48 hours — suits from $60, dresses from $30" },
        { lat: 15.8785, lng: 108.3368, label: "White Rose Dumplings", num: 5, cat: "food", desc: "Hoi An exclusive — translucent shrimp dumplings shaped like roses" }
      ]
    },

    // ===== DAY 8: HOI AN BEACH DAY =====
    {
      num: 8,
      neighborhoods: "Hoi An · An Bàng Beach",
      title: "Beach Day & Countryside Cycling — Hoi An Relaxation",
      description: "A well-deserved rest day. Bike to the beach, swim in the warm South China Sea, eat fresh seafood, and watch the sunset.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Cycle to An Bàng Beach",
              description: "Rent bicycles from your hotel (~$1/day) and ride 4km through rice paddies and villages to An Bàng Beach — one of Vietnam's best.",
              details: ["Flat, easy ride — about 20 minutes", "Park at any beachside restaurant (they'll watch your bike for free)", "The beach is clean, wide, and has gentle waves — perfect for kids", "Beach chairs and umbrellas: free if you order food/drinks"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Hotel Breakfast", description: "Most Hoi An hotels include breakfast. Enjoy it in the garden courtyard.", meta: "Included with accommodation" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Swim, Sun & Relax at An Bàng Beach",
              description: "Spend the morning swimming in warm, calm waters. The beach is lined with restaurants serving cold coconuts and fresh seafood.",
              details: ["Water temperature: warm bath (~28°C/82°F)", "Lifeguards on duty at main sections", "Order a fresh coconut ($0.50) and claim your lounge chair"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Beachfront Seafood Feast", description: "Fresh grilled squid, shrimp, and fish straight from the boats. With rice, salad, and beer. ~$5-8 per person.", meta: "Any beachside restaurant — look for the ones with the freshest catch displayed" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Beach Time or Tra Que Herb Village",
              description: "Continue relaxing at the beach, or cycle to nearby Tra Que — a traditional herb-farming village where you can plant vegetables and learn about organic farming.",
              details: ["Tra Que is 3km from An Bàng Beach", "Free to wander the gardens", "Kids love getting their hands dirty planting seeds", "Many farms offer foot massages using herbs from the garden ($5)"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Return to Ancient Town for Final Hoi An Night",
              description: "One more night in the lantern-lit old town. Pick up your custom clothes if you got measured, and do any last shopping.",
              details: ["Most tailor shops do final fittings tonight", "Buy lanterns as souvenirs — they fold flat for packing", "Handmade leather goods are also a great deal here"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Bánh Xèo (Sizzling Crepes)", description: "Crispy turmeric rice flour crepes filled with shrimp, pork, bean sprouts. Wrap in rice paper with herbs and dip. ~$2.", meta: "Bánh Xèo  direction Hoi An — look for the sizzling sounds" }
          ],
          tips: [
            { type: "reddit", text: "An Bang beach is seriously underrated. Clean water, cheap seafood, barely any tourists compared to other Asian beaches. Spend a full day here.", cite: "r/VietNam" }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8801, lng: 108.338, label: "Hoi An Ancient Town", num: 1, cat: "sight", desc: "Start point — rent bikes and head to the beach" },
        { lat: 15.8708, lng: 108.3065, label: "An Bàng Beach", num: 2, cat: "beach", desc: "4km bike ride through rice paddies — wide, clean, calm waters" },
        { lat: 15.863, lng: 108.325, label: "Tra Que Herb Village", num: 3, cat: "culture", desc: "Traditional organic herb farming — plant vegetables, herb foot massage" },
        { lat: 15.8793, lng: 108.3362, label: "Ancient Town Night Market", num: 4, cat: "shopping", desc: "Final night shopping — lanterns, leather goods, custom clothes pickup" }
      ]
    },

    // ===== DAY 9: HOI AN → HUE =====
    {
      num: 9,
      neighborhoods: "Hoi An → Hai Van Pass → Hue",
      title: "Over the Clouds — Hai Van Pass to the Imperial City",
      description: "One of the most scenic drives in Southeast Asia: the Hai Van Pass. Then arrive in Hue, the ancient imperial capital of Vietnam.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Drive the Hai Van Pass",
              description: "Hire a private car or join a guided motorbike tour from Hoi An to Hue via the Hai Van Pass — the dramatic mountain road featured on Top Gear. 3-4 hours total.",
              details: ["Private car with driver: ~$35-45 for the group", "Motorbike tour (passenger): ~$25-30 per person", "Stop at the top for panoramic views of both coastlines", "Kids should go in the car — the pass has steep drops"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Hotel Breakfast", description: "Quick breakfast before departure.", meta: "Included with accommodation" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Stop at Lang Co Beach & Lap An Lagoon",
              description: "A stunning stretch of white sand beach and a turquoise lagoon famous for oyster farming. Great photo stop.",
              details: ["Fresh oysters for $1-2 per dozen", "Pristine beach with barely any tourists", "20-minute stop is enough — you're on your way to Hue"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Bún Bò Huế (at a roadside stop)", description: "You're entering Hue's territory — time for its namesake dish: a spicy, lemongrass-scented beef noodle soup with pork knuckle and blood pudding. ~$1.50.", meta: "Any roadside restaurant after the Hai Van Pass" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Arrive in Hue & Visit the Imperial City",
              description: "Hue was the capital of Vietnam for 143 years (1802-1945). The Imperial City is a vast complex of palaces, temples, and gardens surrounded by a moat.",
              details: ["Entrance: ~$6 (150,000 VND)", "Allow 2-3 hours to explore", "Rent an audio guide — the history is fascinating", "Kids enjoy running through the empty palace courtyards", "Much of it was destroyed in the war but restoration is ongoing"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Perfume River Night Walk",
              description: "Walk along the Perfume River (Sông Hương) at dusk. The bridges are lit up and families stroll along the promenade.",
              details: ["Truong Tien Bridge is beautifully illuminated", "Dragon boats offer evening cruises for ~$3-5", "The pace of Hue is noticeably slower than Hanoi or HCMC"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Bánh Khoái & Nem Lụi", description: "Hue street food at its best: crispy pancakes with pork and shrimp, plus grilled pork sausage on lemongrass sticks wrapped in rice paper with peanuts. ~$2.", meta: "Street vendors along Pham Ngu Lao street — follow the smoke" }
          ],
          tips: [
            { type: "reddit", text: "The Hai Van Pass is one of the best drives in the world. Do it by car if you have kids, but it's worth every minute either way. Stop at Lang Co Beach.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8801, lng: 108.338, label: "Depart Hoi An", num: 1, cat: "transport", desc: "Begin the scenic drive to Hue via Hai Van Pass" },
        { lat: 16.2425, lng: 108.1858, label: "Hai Van Pass Summit", num: 2, cat: "sight", desc: "Panoramic views of both coastlines — Top Gear's favorite road" },
        { lat: 16.1588, lng: 108.1162, label: "Lang Co Beach", num: 3, cat: "beach", desc: "Pristine white sand beach with fresh oysters" },
        { lat: 16.4689, lng: 107.5886, label: "Hue Imperial City", num: 4, cat: "culture", desc: "Vast 19th-century palace complex — capital of Vietnam for 143 years" },
        { lat: 16.463, lng: 107.582, label: "Perfume River & Truong Tien Bridge", num: 5, cat: "sight", desc: "Night stroll along the river — dragon boats and illuminated bridges" }
      ]
    },

    // ===== DAY 10: HUE → HO CHI MINH CITY =====
    {
      num: 10,
      neighborhoods: "Hue → Flight to Ho Chi Minh City",
      title: "Imperial Tombs & The Big City — Hue to Saigon",
      description: "Morning exploring Hue's royal tombs, then fly to Ho Chi Minh City — Vietnam's largest, loudest, most energetic city.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Emperor Tu Duc's Tomb",
              description: "The most beautiful of Hue's royal tombs. Set among pine forests and lotus ponds, it's where Emperor Tu Duc wrote poetry and retreated from court life.",
              details: ["Entrance: ~$3 (80,000 VND)", "8km from Hue center — Grab or bicycle", "Arrive by 8am to beat the heat and crowds", "Kids can explore the grounds freely — it's like a garden maze"]
            },
            {
              title: "Thien Mu Pagoda",
              description: "Hue's most iconic pagoda, perched on the Perfume River. The 7-story tower is the tallest religious building in Vietnam.",
              details: ["Free entry", "Beautiful river views from the grounds", "Contains the Austin car driven by monk Thich Quang Duc to his self-immolation in 1963"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Bánh Ép (Hue Pressed Cake)", description: "A Hue breakfast specialty — thin rice flour cakes pressed with egg, pork, and herbs on a charcoal grill. ~$0.50.", meta: "Street vendors around the Imperial City — morning only" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Fly Hue (HUI) → Ho Chi Minh City (SGN)",
              description: "1.5-hour flight. VietJet ($30-45). Book ahead. Hue airport is small — arrive 1.5 hours early.",
              details: ["Phu Bai Airport (HUI) is 30 min from Hue center", "Grab to airport: ~$5", "Fly to Tan Son Nhat (SGN) — HCMC's main airport"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Airport / In-Flight Snack", description: "Grab something quick at Hue airport or on the flight.", meta: "~$3-5" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Arrive in Ho Chi Minh City & Check In",
              description: "Vietnam's biggest city hits different — it's louder, faster, and more chaotic than anywhere else in the country. Embrace it.",
              details: ["Grab from airport to District 1: ~$5-7, 30 min", "Budget: Common Room Hostel ($8/night)", "Mid-range: La Siesta Premium Saigon ($40/night)", "Stay in District 1 — walkable to everything"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Bui Vien Walking Street & Ben Thanh Market",
              description: "HCMC's backpacker street is loud, colorful, and fun. Then walk to Ben Thanh Market for souvenirs and street food.",
              details: ["Bui Vien comes alive after 7pm — live music, cheap beer, street performers", "Ben Thanh Market stays open until midnight", "Bargain hard at Ben Thanh — start at 50% of their first offer", "Kids will be wide-eyed at the energy"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Cơm Tấm (Broken Rice) at Ba Giao", description: "HCMC's signature dish: broken rice with grilled pork chop, egg meatloaf, and fish sauce. Simple, perfect, ~$2.", meta: "Street stalls everywhere in District 1" }
          ],
          tips: [
            { type: "reddit", text: "HCMC traffic looks insane but it's actually organized chaos. Just walk slowly and steadily across the street — the scooters will flow around you like water. Don't stop or run.", cite: "r/VietNam" }
          ]
        }
      ],
      mapPins: [
        { lat: 16.4458, lng: 107.5633, label: "Tu Duc Tomb", num: 1, cat: "culture", desc: "Most beautiful royal tomb — poetry pavilions among pine forests and lotus ponds" },
        { lat: 16.4553, lng: 107.5493, label: "Thien Mu Pagoda", num: 2, cat: "sight", desc: "Hue's iconic 7-story pagoda on the Perfume River" },
        { lat: 16.4057, lng: 107.7034, label: "Phu Bai Airport (HUI)", num: 3, cat: "transport", desc: "Fly to HCMC — 1.5 hours" },
        { lat: 10.7869, lng: 106.7004, label: "HCMC District 1", num: 4, cat: "transport", desc: "Stay here — walkable to everything in Saigon" },
        { lat: 10.7723, lng: 106.6981, label: "Ben Thanh Market", num: 5, cat: "shopping", desc: "Iconic market — souvenirs, street food, and bargaining practice" }
      ]
    },

    // ===== DAY 11: HO CHI MINH CITY =====
    {
      num: 11,
      neighborhoods: "Ho Chi Minh City · Cu Chi · District 1",
      title: "Tunnels, War History & Saigon Street Food Tour",
      description: "A powerful day: explore the Cu Chi Tunnels in the morning, then dive into Saigon's wartime history and legendary food scene.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Cu Chi Tunnels",
              description: "An immense network of underground tunnels used during the Vietnam War. Crawl through sections, see booby traps, and learn about life underground.",
              details: ["1.5 hours from HCMC center — book a half-day tour ($10-15/person)", "Includes hotel pickup and drop-off", "You can crawl through widened tunnel sections (optional)", "Firing range on-site (M16, AK47) — ~$1.50 per bullet", "Better for kids 8+ — younger ones may find it intense"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Bánh Mì Huỳnh Hoa", description: "Saigon's most famous banh mi — overstuffed with cold cuts, pâté, and pickled vegetables. Huge portion. ~$2.", meta: "26 Lê Thị Riêng, open 6:30am-10pm" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "War Remnants Museum",
              description: "A powerful and sobering museum documenting the Vietnam War from the Vietnamese perspective. Not for young children, but essential for older kids and adults.",
              details: ["Entrance: ~$0.60 (15,000 VND)", "Allow 1.5-2 hours", "The Agent Orange section is heavy — pace yourself", "Powerful photography exhibits"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Bún Thit Nuong (Grilled Pork Noodles)", description: "Cold vermicelli with grilled lemongrass pork, fresh herbs, spring rolls, and fish sauce. The perfect HCMC lunch. ~$2.", meta: "Street food stalls in District 1" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Independence Palace & Notre-Dame Cathedral",
              description: "The Reunification Palace is where the war ended (tank crashing through the gates on April 30, 1975). Nearby, the Notre-Dame Cathedral and Central Post Office showcase beautiful French colonial architecture.",
              details: ["Palace entrance: ~$2.50", "Central Post Office is free — still a working post office", "Notre-Dame Cathedral exterior is under renovation but still impressive", "All three are within walking distance of each other"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Saigon Street Food Tour",
              description: "Join an evening food tour by motorbike (or walking) to hit 5-6 different street food spots. A perfect way to experience HCMC's incredible food scene.",
              details: ["Motorbike food tour: ~$20-25/person (XO Tours is popular)", "Walking food tour: ~$15-20/person", "Sample: bahn xeo, goi cuon, che (sweet soup), and more", "The motorbike tour at night is an adventure in itself"]
            }
          ],
          meals: [
            { type: "Dinner", name: "Street Food Tour", description: "Multiple dishes across multiple stops — part of the food tour experience.", meta: "Included in tour price" }
          ],
          tips: [
            { type: "reddit", text: "The Cu Chi tunnels are worth it but don't do the shooting range if you have young kids — the sound of gunfire in a war zone setting can be intense. The tunnels themselves are fascinating though.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 11.0643, lng: 106.5192, label: "Cu Chi Tunnels", num: 1, cat: "culture", desc: "Underground tunnel network — crawl through sections, see wartime history" },
        { lat: 10.7802, lng: 106.703, label: "War Remnants Museum", num: 2, cat: "culture", desc: "Powerful museum documenting the Vietnam War from Vietnamese perspective" },
        { lat: 10.7769, lng: 106.6957, label: "Independence Palace", num: 3, cat: "sight", desc: "Where the war ended — tank through the gates, April 30, 1975" },
        { lat: 10.7799, lng: 106.6983, label: "Notre-Dame Cathedral & Post Office", num: 4, cat: "sight", desc: "Beautiful French colonial architecture — working post office with vaulted ceilings" },
        { lat: 10.7723, lng: 106.6981, label: "District 1 Street Food", num: 5, cat: "food", desc: "Evening food tour — sample 5-6 dishes across the best street food spots" }
      ]
    },

    // ===== DAY 12: HO CHI MINH CITY & DEPARTURE =====
    {
      num: 12,
      neighborhoods: "Ho Chi Minh City · Chợ Lớn",
      title: "Last Day — Chinatown, Coffee & Goodbye Vietnam",
      description: "Your final day. Explore HCMC's vibrant Chinatown (Chợ Lớn), grab one last incredible coffee, and reflect on an unforgettable 12 days.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Chợ Lớn (Chinatown) & Binh Tay Market",
              description: "HCMC's Chinatown is the largest in Vietnam. Wander through lantern-lined streets, visit ornate Chinese temples, and browse the bustling Binh Tay Market.",
              details: ["5km from District 1 — Grab for ~$3", "Binh Tay Market is less touristy than Ben Thanh — better prices", "Visit Thien Hau Temple (dedicated to the sea goddess)", "Try Chinese-Vietnamese breakfast items you won't find elsewhere"]
            }
          ],
          meals: [
            { type: "Breakfast", name: "Hủ Tiếu Nam Vang (Phnom Penh Noodles)", description: "A Chinese-Vietnamese hybrid: pork and seafood noodle soup with a clear, sweet broth. HCMC does it best. ~$1.50.", meta: "Street stalls in Chợ Lớn — look for the crowded ones" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Last Vietnamese Coffee & Souvenir Shopping",
              description: "Sit at a sidewalk cafe with a cà phê sữa đá (Vietnamese iced coffee with condensed milk) and watch Saigon's incredible street life one last time.",
              details: ["Buy: Vietnamese coffee beans ($3-5/bag), fish sauce ($2), dried fruit ($3)", "Pack souvenirs carefully — the airlines are strict on liquid fish sauce", "Cong Caphe or The Workshop for a great final coffee experience"]
            }
          ],
          meals: [
            { type: "Lunch", name: "Gỏi Cuốn (Fresh Spring Rolls) & Phở", description: "One last round of Vietnam's greatest hits. Fresh spring rolls with peanut sauce and a final bowl of phở. ~$3.", meta: "Any street food stall or Phở Hòa Pasteur" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Head to Tan Son Nhat Airport (SGN)",
              description: "Leave for the airport 3 hours before your flight. Grab from District 1 to airport: ~$5, 30 minutes. Say goodbye to Vietnam.",
              details: ["Allow extra time — HCMC traffic can be unpredictable", "Airport has decent food options and souvenir shops", "International terminal has a decent lounge ($15 entry)"]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Fly Home",
              description: "Reflect on 12 incredible days: Hanoi's street food, Ha Long Bay's limestone towers, Ninh Binh's caves and peaks, Hoi An's lanterns, Hue's imperial history, and Saigon's electric energy.",
              details: ["You did it all for under $1,000 per person", "Vietnam will stay with you forever — most travelers come back"]
            }
          ],
          tips: [
            { type: "reddit", text: "Vietnam changes you. I went for 2 weeks and I've been back 3 times. The food alone is worth the trip. Don't try to pack too much into each day — the best moments happen when you slow down.", cite: "r/travel" }
          ]
        }
      ],
      mapPins: [
        { lat: 10.7509, lng: 106.6603, label: "Chợ Lớn Chinatown", num: 1, cat: "culture", desc: "Vietnam's largest Chinatown — ornate temples, lantern streets, Binh Tay Market" },
        { lat: 10.7482, lng: 106.6532, label: "Thien Hau Temple", num: 2, cat: "sight", desc: "Beautiful Chinese temple dedicated to the sea goddess" },
        { lat: 10.7833, lng: 106.6967, label: "District 1 Coffee & Shopping", num: 3, cat: "food", desc: "Final Vietnamese iced coffee and souvenir shopping" },
        { lat: 10.8188, lng: 106.658, label: "Tan Son Nhat Airport (SGN)", num: 4, cat: "transport", desc: "Fly home — 3 hours early for international flights" }
      ]
    }
  ],

  budgetTable: [
    { category: "🏨 Accommodation", item: "Hostels/budget hotels (11 nights)", perPerson: "$80-120", total: "$240-360" },
    { category: "🚗 Transport", item: "Grab, buses, 2 domestic flights", perPerson: "$120-160", total: "$360-480" },
    { category: "🍜 Food", item: "Street food & restaurants (12 days)", perPerson: "$80-120", total: "$240-360" },
    { category: "🎭 Activities", item: "Ha Long Bay cruise, Cu Chi tour, cooking class, attractions", perPerson: "$80-120", total: "$240-360" },
    { category: "🎫 Visas & Insurance", item: "E-visa + travel insurance", perPerson: "$45-60", total: "$135-180" },
    { category: "📱 SIM & Misc", item: "SIM card, souvenirs, laundry", perPerson: "$25-35", total: "$75-105" },
    { category: "✈️ International Flights", item: "Varies by origin (excluded from budget)", perPerson: "—", total: "—" },
    { category: "📊 TOTAL (excl. flights)", item: "Per person for the group", perPerson: "$430-615", total: "$1,290-1,845" }
  ],

  practicalInfo: [
    { title: "💰 Tipping", items: ["Not expected or required in Vietnam", "Rounding up the bill or leaving small change is appreciated", "Never mandatory — don't feel pressured"] },
    { title: "🚕 Getting Around", items: ["Download Grab (Southeast Asia's Uber) — works everywhere", "Shows price before booking — no negotiation needed", "Cheaper and safer than street taxis", "Motorbike taxis on Grab are even cheaper for solo riders"] },
    { title: "🥡 Street Food Safety", items: ["Eat at busy stalls with high turnover", "If locals are eating there, it's safe", "Avoid pre-cut fruit that's been sitting out", "Bring hand sanitizer — not always available at stalls"] },
    { title: "💧 Water", items: ["Never drink tap water", "Bottled water is cheap (~$0.25/liter)", "Most hotels provide free water daily", "Ice in restaurants is generally safe (factory-made)"] },
    { title: "👕 Dress Code", items: ["Casual everywhere in daily life", "Temples & mausoleum: cover shoulders and knees", "Light, breathable fabrics essential in May heat", "Bring a light scarf — works as cover-up and sun protection"] },
    { title: "💳 Payment", items: ["Cash (VND) is king — always carry small bills", "Cards accepted at hotels and upscale restaurants", "ATM max withdrawal: usually 2,000,000 VND (~$80)", "Withdraw enough for a few days at a time"] },
    { title: "📱 Useful Apps", items: ["Grab — rides + food delivery", "Google Translate — camera mode translates menus instantly", "XE Currency — quick VND conversion", "Maps.me — offline maps for remote areas"] },
    { title: "🧳 Packing Essentials", items: ["Lightweight breathable clothes", "Sunscreen SPF 50+ and insect repellent", "Compact umbrella (sudden rain showers)", "Comfortable walking shoes + flip flops", "US-style power adapter (Type A/C)", "Small daypack for daily excursions"] },
    { title: "👨‍👩‍👧‍👦 With Kids", items: ["Vietnam is extremely child-friendly — kids welcomed everywhere", "Many restaurants have child portions or kids eat free", "Bring a carrier for toddlers (strollers struggle on narrow sidewalks)", "Most attractions have discounted child tickets", "Pharmacies stock children's medicine and are very helpful"] },
    { title: "🛂 Visa & Entry", items: ["E-visa is the easiest option — apply online at evisa.xuatnhapcanh.gov.vn", "Cost: $25 for 90-day single entry", "Print a copy + bring a passport photo", "Have your hotel address ready for the arrival card"] }
  ],

  highlights: [
    "Street food crawl through Hanoi's Old Quarter",
    "Overnight cruise through Ha Long Bay's limestone karsts",
    "Rowboat adventure through Tràng An caves",
    "500-step climb to the dragon viewpoint at Mùa Caves",
    "Lantern-lit nights in Hoi An Ancient Town",
    "Cooking class with market tour",
    "Scenic drive over the Hai Van Pass",
    "Imperial City of Hue — 143 years of history",
    "Cu Chi Tunnels — underground war history",
    "Saigon street food tour by motorbike"
  ]
};

// Run fulfillment
const result = fulfillOrder(order, itineraryData);
console.log('\n=== FULFILLMENT COMPLETE ===');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('Email sent:', result.emailSent);
