const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1773073630484_lczlvy',
  orderId: 'order_1773073630484_lczlvy',
  email: 'kialogy@gmail.com',
  destination: 'Kualapuu, HI, USA',
  startDate: '2026-05-11',
  endDate: '2026-05-17',
  customerName: null
};

const itineraryData = {
  destination: "Molokai, Hawaii",
  countryEmoji: "🇺🇸",
  title: "Molokai, Hawaii",
  subtitle: "6 Days on the Friendly Isle — Surf, Sand & Slow Living with Baby",
  description: "A family-friendly adventure across Hawaii's most untouched island. Six days of uncrowded beaches, world-class snorkeling, local flavors, and the kind of quiet magic that only Molokai delivers — all at a pace that works with a baby in tow.",
  duration: "6 days",
  dates: "May 11 – May 17, 2026",
  budget: "$5,000–10,000",
  pace: "Relaxed with adventure sprinkled in",
  bestFor: "Couples with baby · Beach lovers · Foodies · Adventure seekers",
  highlights: [
    "Three-mile-long Papohaku Beach almost entirely to yourselves",
    "Snorkeling Hawaii's only barrier reef at Murphy's Beach",
    "Late-night hot bread ritual at legendary Kanemitsu Bakery",
    "Kayaking the calm south shore with Molokai Outdoors",
    "Mailing a hand-painted coconut home from Post-A-Nut",
    "Ancient Hawaiian fishponds and sacred Halawa Valley"
  ],

  essentials: [
    {
      title: "🏠 Where to Stay",
      text: "Book a vacation rental (VRBO/Airbnb) in Kaunakakai or the west side near Kepuhi Beach. Molokai has one hotel (Hotel Molokai) and a handful of condo resorts (Molokai Shores, Wavecrest, Ke Nani Kai). For families with a baby, a 2-bedroom rental with kitchen is ideal — grocery stores are limited, so stock up at Friendly Market in Kaunakakai on Day 1."
    },
    {
      title: "🚗 Getting Around",
      text: "Rent a car — absolutely essential on Molokai. The island is 38 miles long but has no public transit, no rideshare, and no traffic lights. Alamo at Molokai Airport (MKK) is the main option. Book well in advance — inventory is tiny. A 4WD SUV is recommended for unpaved roads to the west end and Halawa Valley."
    },
    {
      title: "👶 Baby Logistics",
      text: "Bring your own car seat, stroller, and baby carrier (hiking-style carriers are gold here). Pack extra supplies — there's one small grocery store and one pharmacy on the entire island. The nearest hospital is Molokai General (Kaunakakai), but for serious emergencies you'd be airlifted to Maui. Sunscreen, shade tents, and reef-safe baby sunscreen are must-haves."
    },
    {
      title: "🍽️ Dining Reality Check",
      text: "Molokai has roughly 8-10 restaurants total, mostly in Kaunakakai. Some close early or on random days. Check hours before driving across the island. Cook at your rental 2-3 meals a day and treat restaurant meals as special outings. Stock up at Friendly Market on arrival."
    },
    {
      title: "🌊 Ocean Safety",
      text: "No lifeguards anywhere on Molokai. The south shore is calm and protected by the reef (great for baby wading). The west end (Papohaku) has powerful shore break — beautiful for walks but swim with extreme caution. Always check conditions before entering the water."
    },
    {
      title: "📱 Connectivity",
      text: "Cell service is spotty outside Kaunakakai. The west end and Halawa Valley have little to no signal. Download offline maps before you go. Wi-Fi is available at Hotel Molokai and most vacation rentals. Embrace the disconnect — it's part of the magic."
    }
  ],

  days: [
    {
      num: 1,
      title: "Arrive & Settle Into Island Time",
      neighborhoods: "Molokai Airport · Kaunakakai · South Shore",
      description: "Arrive on Molokai, pick up your rental car, stock up on supplies, and ease into the island's famously slow pace. Today is about orienting yourselves and soaking in the first sunset.",
      timeBlocks: [
        {
          label: "Morning / Arrival",
          activities: [
            {
              title: "Arrive at Molokai Airport (MKK)",
              description: "Fly in from Honolulu (25 min) or Maui (15 min) via Mokulele Airlines or Southern Airways Express. The airport is a single open-air terminal — the most laid-back arrival in Hawaii.",
              details: [
                "📍 Molokai Airport, 3980 Airport Loop, Hoolehua",
                "🚗 Pick up rental car at Alamo counter (book months ahead — limited inventory)",
                "👶 Install car seat immediately — you'll need it for every drive"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Pro tip: Flights from Honolulu on Mokulele are in tiny prop planes with incredible views. Window seats on the left side offer the best Molokai approach." }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Stock Up at Friendly Market",
              description: "Molokai's main grocery store and your lifeline for the week. Grab breakfast staples, snacks, baby food, water, and dinner ingredients. Selection is decent but prices are higher than mainland — don't expect Whole Foods.",
              details: [
                "📍 90 Ala Malama Ave, Kaunakakai",
                "⏰ Mon–Fri 8:30am–8:30pm, Sat 8:30am–6:30pm"
              ]
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "Paddlers Restaurant & Bar",
              description: "Welcome yourself to Molokai with lunch at the island's best restaurant. Chef Kainoa Turner trained at Le Cordon Bleu and brings serious chops to island classics. Try the chili garlic wings with inamona or the carne asada tacos.",
              meta: "📍 10 Mohala St, Kaunakakai · $$"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Check In & Explore Kaunakakai",
              description: "Settle into your vacation rental, set up baby's space, then stroll through Kaunakakai — Molokai's only real town. Three blocks of low-rise buildings with genuine Hawaiian charm. Walk the Kaunakakai Wharf at sunset — it's the longest wharf in Hawaii, stretching half a mile into the ocean.",
              details: [
                "📍 Kaunakakai Wharf — extends 1/2 mile into the ocean",
                "👶 Flat, paved wharf walk is stroller-friendly",
                "🌅 Faces south — great sunset views toward Lanai"
              ]
            }
          ],
          tips: [
            { type: "reddit", text: "Molokai isn't broken — it's on purpose. Don't come expecting Maui amenities. Come expecting the Hawaii that existed 50 years ago.", cite: "r/HawaiiVisitors" }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Cook at Your Rental",
              description: "First night — make a simple dinner with groceries, put baby down early, and sit outside under more stars than you've ever seen. No light pollution out here.",
              meta: "🏠 Your vacation rental"
            }
          ],
          tips: [
            { type: "tip", text: "Late-night ritual: After baby's asleep, one parent can sneak to Kanemitsu Bakery's back alley for hot bread (after 10:30pm). Warm loaves stuffed with cream cheese, cinnamon, and strawberry jam. 79 Ala Malama Ave — follow the locals." }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1528, lng: -157.0956, label: "Molokai Airport (MKK)", num: 1, cat: "transport", desc: "Open-air terminal — most Hawaiian airport arrival ever" },
        { lat: 21.0816, lng: -157.0143, label: "Friendly Market", num: 2, cat: "shopping", desc: "Stock up on arrival — only real grocery store" },
        { lat: 21.0833, lng: -157.0241, label: "Paddlers Restaurant & Bar", num: 3, cat: "food", desc: "Best restaurant on Molokai — Le Cordon Bleu trained chef" },
        { lat: 21.0806, lng: -157.0098, label: "Kaunakakai Wharf", num: 4, cat: "attraction", desc: "Hawaii's longest wharf — stunning sunset stroll" },
        { lat: 21.0820, lng: -157.0139, label: "Kanemitsu Bakery", num: 5, cat: "food", desc: "Legendary late-night hot bread from the back alley" }
      ]
    },
    {
      num: 2,
      title: "West End Beaches & Sunset Paradise",
      neighborhoods: "Papohaku Beach · Kepuhi Beach · Moomomi",
      description: "Head to Molokai's stunning west end for miles of deserted white sand, gentle tide pool exploration, and some of the most dramatic sunsets in Hawaii. A perfect beach day for the whole family.",
      timeBlocks: [
        {
          label: "Morning",
          meals: [
            {
              type: "Breakfast",
              name: "Kualapuu Cookhouse",
              description: "Fuel up at this beloved local diner. Known for hearty plate breakfasts, pancakes, and local-style eggs with rice. Cash-friendly, family-run, zero pretense.",
              meta: "📍 Farrington Hwy, Kualapuu · $ · Check hours — they close when food runs out"
            }
          ]
        },
        {
          label: "Mid-Morning",
          activities: [
            {
              title: "Papohaku Beach Park",
              description: "Three miles of pristine white sand — one of Hawaii's longest beaches — and you might have it entirely to yourselves. The sand is soft and wide, perfect for baby to crawl and play. Set up a shade tent and spend the morning here.",
              details: [
                "📍 Kaluakoi Rd, west end of Molokai",
                "🅿️ Free parking at multiple beach access points",
                "👶 Wide flat sand, shade trees at the pavilion — excellent for baby",
                "⚠️ Strong shore break — wade only, don't swim in deep water",
                "🚿 Restrooms and outdoor showers available"
              ]
            }
          ],
          tips: [
            { type: "reddit", text: "Papohaku is magical. We spent 3 hours there and saw exactly 4 other people. On Maui that same beach would have 400.", cite: "r/HawaiiVisitors" }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Kepuhi Beach & Tide Pools",
              description: "Short drive from Papohaku. The north end has rocky tide pools at low tide — small pools trapping little fish, crabs, and sea urchins. Baby will be mesmerized watching the mini marine world.",
              details: [
                "📍 Kepuhi Beach, near Ke Nani Kai condos",
                "👶 Shallow tide pools at low tide — great for baby's feet in the water",
                "⚠️ Check tide charts — visit at low tide for best pool access"
              ]
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "Packed Picnic on the Beach",
              description: "No restaurants on the west end — pack a cooler from Friendly Market. Sandwiches, fruit, and cold drinks on the sand. Peak Molokai living.",
              meta: "🧊 Pack a cooler — there's nothing to buy out here"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Moomomi Dunes (Drive-By)",
              description: "If baby is napping in the car, detour to the Moomomi dunes — a windswept coastal preserve with rare native plants and Hawaiian green sea turtle nesting grounds. The road is rough (4WD recommended) but the landscape is otherworldly.",
              details: [
                "📍 Moomomi Beach, northwest coast",
                "🚗 Unpaved road — 4WD recommended, go slow",
                "🐢 Sea turtle nesting area — keep your distance from any turtles"
              ]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Sunset at Papohaku Beach",
              description: "Return for what might be the most spectacular sunset of your trip. The west-facing beach gets a full unobstructed view of the sun dropping into the Pacific. Bring a blanket and let baby play in the warm sand.",
              details: [
                "🌅 Sunset around 7:00pm in May",
                "📸 Wide-open beach — incredible family photo opportunity"
              ]
            }
          ],
          meals: [
            {
              type: "Dinner",
              name: "Hiro's Ohana Grill at Hotel Molokai",
              description: "Oceanfront dining with live Hawaiian music most evenings. Chef Woody Hiro brings Oahu training to Molokai classics — try the ahi katsu with wasabi aioli or the Angus steak with kiawe smoked sea salt.",
              meta: "📍 1300 Kamehameha V Hwy, Kaunakakai · $$ · 🎶 Live music"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.1569, lng: -157.0638, label: "Kualapuu Cookhouse", num: 1, cat: "food", desc: "Local diner — hearty Hawaiian breakfasts" },
        { lat: 21.1764, lng: -157.2483, label: "Papohaku Beach Park", num: 2, cat: "beach", desc: "3 miles of white sand — one of Hawaii's longest beaches" },
        { lat: 21.1895, lng: -157.2525, label: "Kepuhi Beach & Tide Pools", num: 3, cat: "beach", desc: "Rocky tide pools for exploring at low tide" },
        { lat: 21.1950, lng: -157.1700, label: "Moomomi Dunes Preserve", num: 4, cat: "nature", desc: "Windswept coastal dunes and turtle nesting grounds" },
        { lat: 21.0772, lng: -156.9984, label: "Hiro's Ohana Grill", num: 5, cat: "food", desc: "Oceanfront dining with live music at Hotel Molokai" }
      ]
    },
    {
      num: 3,
      title: "South Shore Kayak & Ancient Fishponds",
      neighborhoods: "Kaunakakai · South Shore · Kamalo",
      description: "Explore Molokai's protected south shore by kayak, discover 700-year-old Hawaiian fishponds, and enjoy calm waters that the fringing reef creates. Adventure meets history today.",
      timeBlocks: [
        {
          label: "Morning",
          meals: [
            {
              type: "Breakfast",
              name: "Kanemitsu Bakery & Coffee Shop",
              description: "Start the day at Molokai's most famous bakery. By day it's a cozy coffee shop with fresh pastries, bread, and simple breakfast plates. The Molokai sweet bread is legendary — James Beard nominated.",
              meta: "📍 79 Ala Malama Ave, Kaunakakai · $ · Opens 5:30am"
            }
          ],
          activities: [
            {
              title: "Kayak the South Shore with Molokai Outdoors",
              description: "Guided kayak or SUP tour along the protected south shore from Kamalo Harbor. The fringing reef keeps waters calm and flat. Paddle past ancient fishponds, spot sea turtles, and see the coastline from the water. One parent paddles while the other watches baby, then switch.",
              details: [
                "📍 Molokai Outdoors — molokai-outdoors.com or (808) 553-4477",
                "💰 ~$75/person for guided kayak tour",
                "⏰ Morning tours for calmest water",
                "👶 Take turns — one paddles, one watches baby on shore",
                "🏄 SUP rentals also available (~$45/half day)"
              ]
            }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Ancient Fishponds of the South Shore",
              description: "Molokai's south coast has the most intact ancient Hawaiian fishponds in the state — stone-walled aquaculture enclosures built 700+ years ago. Drive along Kamehameha V Highway and stop to see Keawanui Fishpond, the largest fully enclosed and functioning fishpond in Hawaii.",
              details: [
                "📍 Along Kamehameha V Hwy (Hwy 450), east of Kaunakakai",
                "🏛️ Keawanui Fishpond visible from road at ~mile marker 14",
                "👶 Easy — viewable from the car or short roadside walks"
              ]
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "A Taste of Molokai Food Truck",
              description: "Molokai's best poke bowls from a food truck in Kaunakakai. Fresh, generous, surprisingly restaurant-quality. The ahi poke bowl is the move.",
              meta: "📍 Near Molokai Fish & Dive, Kaunakakai · $"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Post-A-Nut at Hoolehua Post Office",
              description: "One of Molokai's quirkiest traditions — paint and mail a real coconut to friends or family. No box needed; the coconut IS the package. The post office provides coconuts and markers. Over 3,000 coconuts shipped annually.",
              details: [
                "📍 Hoolehua Post Office, Puupeelua Ave, Hoolehua",
                "💰 Free (just pay postage: $12–$20 per coconut)",
                "⏰ Mon–Fri, 8:30am–12pm and 1pm–4pm",
                "👶 Baby's handprint on a coconut = perfect keepsake"
              ]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Beach Time at One Alii Park",
              description: "Calm, shallow beach park in Kaunakakai — ideal for baby's evening splash. Calm water protected by the reef, picnic tables, shade trees, and restrooms.",
              details: [
                "📍 One Alii Park, Kamehameha V Hwy, Kaunakakai",
                "👶 Calm shallow water — ideal for baby wading"
              ]
            }
          ],
          meals: [
            {
              type: "Dinner",
              name: "Paddlers Restaurant & Bar",
              description: "Return for dinner — the Thai coconut curry shrimp and gourmet burgers on brioche buns are standouts. Check if they have live music tonight.",
              meta: "📍 10 Mohala St, Kaunakakai · $$ · 🎶 Live music some nights"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0820, lng: -157.0139, label: "Kanemitsu Bakery", num: 1, cat: "food", desc: "James Beard nominated — legendary hot bread" },
        { lat: 21.0625, lng: -156.9025, label: "Kamalo Harbor (Kayak Launch)", num: 2, cat: "adventure", desc: "South shore kayak and SUP tour launch" },
        { lat: 21.0600, lng: -156.8900, label: "Keawanui Fishpond", num: 3, cat: "cultural", desc: "Largest functioning ancient Hawaiian fishpond" },
        { lat: 21.0815, lng: -157.0150, label: "A Taste of Molokai", num: 4, cat: "food", desc: "Best poke bowls on the island" },
        { lat: 21.1528, lng: -157.0956, label: "Hoolehua Post Office", num: 5, cat: "attraction", desc: "Post-A-Nut — mail a hand-painted coconut" },
        { lat: 21.0750, lng: -156.9980, label: "One Alii Beach Park", num: 6, cat: "beach", desc: "Calm shallow water for baby's beach time" },
        { lat: 21.0833, lng: -157.0241, label: "Paddlers Restaurant", num: 7, cat: "food", desc: "Thai coconut curry shrimp and gourmet burgers" }
      ]
    },
    {
      num: 4,
      title: "Halawa Valley & the Wild East End",
      neighborhoods: "East Molokai · Murphy's Beach · Halawa Valley",
      description: "Drive the spectacular east coast highway to Halawa Valley — Molokai's most sacred and dramatic landscape. Snorkel at Murphy's Beach and discover why locals call this the real Hawaii.",
      timeBlocks: [
        {
          label: "Morning",
          meals: [
            {
              type: "Breakfast",
              name: "Cook at Rental + Pack a Full Cooler",
              description: "Fuel up early. Pack snacks, lunch, water, and all baby supplies — there are zero services on the east end past mile marker 15.",
              meta: "🏠 Your vacation rental · 🧊 Pack everything"
            }
          ],
          activities: [
            {
              title: "Murphy's Beach (Kumimi Beach) — Snorkeling",
              description: "The best shore snorkeling on Molokai. Crystal-clear calm water, colorful coral gardens, and abundant marine life just a short swim from shore. Arrive early for clearest conditions. Take turns snorkeling while one parent watches baby on the sandy beach.",
              details: [
                "📍 Kumimi Beach, mile marker 20 on Kamehameha V Hwy",
                "🐠 Parrotfish, butterflyfish, tangs, green sea turtles",
                "👶 Sandy beach with shade trees — baby plays on shore",
                "🤿 Bring your own gear or rent from Molokai Fish & Dive",
                "⏰ Best before 10am for calmest, clearest water"
              ]
            }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Scenic Drive to Halawa Valley",
              description: "Continue east on one of Hawaii's most spectacular coastal drives. The road hugs sea cliffs, passes tiny historic churches, and reveals hidden coves at every turn. Stop at St. Joseph's Church (built by Father Damien, 1876) and Iliiliopae Heiau — one of Hawaii's largest ancient temple platforms.",
              details: [
                "📍 Kamehameha V Hwy (Hwy 450), miles 20–27",
                "📸 Pull over at marked viewpoints — each one is incredible",
                "👶 Baby will likely nap — the winding road is a natural sleep inducer",
                "⚠️ Road narrows past mile 20 — drive slowly, share the road"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "The drive from Kaunakakai to Halawa is 27 miles but takes 90+ minutes. The road is narrow, winding, and stunningly beautiful. Don't rush — the drive IS the experience." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Halawa Valley Overlook",
              description: "At the end of the road — one of Hawaii's most breathtaking views. The emerald Halawa Valley with twin waterfalls (Moaula Falls and Hipuapua Falls) cascading into the lush valley floor. This valley was one of the first places settled by Hawaiians over 1,000 years ago.",
              details: [
                "📍 End of Kamehameha V Hwy — road ends at Halawa Valley",
                "📸 Overlook is accessible from the road — stunning photo op",
                "⚠️ Hiking into the valley requires a local guide and advance reservation. With baby, the overlook is best — the hike is 4+ miles with stream crossings.",
                "📞 Guided hikes (without baby): (808) 542-1855"
              ]
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "Packed Picnic at Halawa Beach Park",
              description: "Small beach at the base of the valley — a beautiful picnic spot. Protected bay with calm water for wading, valley walls towering above.",
              meta: "📍 Halawa Beach Park · 🧊 Bring everything — no services"
            }
          ],
          tips: [
            { type: "reddit", text: "Halawa Valley is sacred to Hawaiians. If you can't do the guided hike, the overlook alone is worth the drive. Better than the Road to Hana IMO.", cite: "r/travel" }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Hiro's Ohana Grill at Hotel Molokai",
              description: "Oceanfront dinner with live music. After a long adventure day, this is the perfect reward — fresh ahi, cold drinks, and the sound of ukulele drifting over the water.",
              meta: "📍 1300 Kamehameha V Hwy, Kaunakakai · $$ · 🎶 Live music"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 21.0580, lng: -156.8540, label: "Murphy's (Kumimi) Beach", num: 1, cat: "beach", desc: "Best shore snorkeling on Molokai" },
        { lat: 21.0735, lng: -156.8280, label: "St. Joseph's Church", num: 2, cat: "cultural", desc: "Built by Father Damien in 1876" },
        { lat: 21.0700, lng: -156.7800, label: "Iliiliopae Heiau", num: 3, cat: "cultural", desc: "One of the largest ancient temples in Hawaii" },
        { lat: 21.1570, lng: -156.7335, label: "Halawa Valley Overlook", num: 4, cat: "nature", desc: "Twin waterfalls and emerald valley" },
        { lat: 21.1560, lng: -156.7350, label: "Halawa Beach Park", num: 5, cat: "beach", desc: "Protected bay at the base of Halawa Valley" },
        { lat: 21.0772, lng: -156.9984, label: "Hiro's Ohana Grill", num: 6, cat: "food", desc: "Oceanfront dining with live Hawaiian music" }
      ]
    },
    {
      num: 5,
      title: "Surf, Culture & the Heart of Molokai",
      neighborhoods: "Kaunakakai · Kalae · Central Molokai",
      description: "Catch some waves, explore Molokai's cultural heritage at the museum, and enjoy a slower-paced day that balances adventure and rest. This is your flex day — adjust based on baby's mood and your energy.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Surf or SUP at the South Shore",
              description: "Molokai's south shore has mellow breaks near Kaunakakai perfect for longboarding or stand-up paddleboarding. Check with Molokai Fish & Dive or Molokai Outdoors for current conditions and board rentals. Take turns — one parent surfs while the other does baby beach time.",
              details: [
                "📍 Molokai Fish & Dive — 53 Ala Malama Ave, (808) 553-5926",
                "🏄 Board rentals: ~$25–40/day (surfboard or SUP)",
                "🌊 May south shore is typically small and mellow — good for intermediate surfers",
                "👶 One surfs, the other hangs with baby at One Alii Park",
                "💡 For bigger waves, a Maui day trip is possible but logistically tough with baby"
              ]
            }
          ],
          meals: [
            {
              type: "Breakfast",
              name: "Kanemitsu Bakery",
              description: "Return for another round of fresh pastries and coffee. Grab extra Molokai sweet bread to bring home — it freezes well and makes an incredible souvenir.",
              meta: "📍 79 Ala Malama Ave, Kaunakakai · $ · Opens 5:30am"
            }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Molokai Museum & Cultural Center (R.W. Meyer Sugar Mill)",
              description: "Housed in a beautifully restored 1878 sugar mill in Kalae, this small museum tells Molokai's history from early Hawaiian settlement through the plantation era. Original machinery, artifacts, and cultural exhibits. A nice air-conditioned break if it's hot.",
              details: [
                "📍 1 Meyers St, Kalae (central Molokai highlands)",
                "💰 ~$5 adults, free for young children",
                "⏰ Mon–Sat 10am–2pm",
                "👶 Small museum — quick 30-45 min visit, baby-friendly",
                "📸 The restored sugar mill building is photogenic"
              ]
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "Ono Fish and Shrimp Truck",
              description: "Parked outside Molokai Fish & Dive, this food truck serves tacos made from locally caught ono and mahimahi — some caught that very morning from their own fishing charters. Fresh doesn't get fresher.",
              meta: "📍 53 Ala Malama Ave, Kaunakakai · $ · Cash preferred"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: