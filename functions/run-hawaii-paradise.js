const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771516426743_i28iob",
  email: "bernard.j.huang@gmail.com",
  destination: "Hawaiian Paradise Park, HI, USA",
  start_date: "2026-04-23",
  end_date: "2026-04-26",
  group_size: "1",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-19T15:53:46.743Z",
  status: "pending"
};

const itineraryData = {
  destination: "Big Island, Hawaiʻi",
  countryEmoji: "🇺🇸",
  title: "Big Island in 3 Nights: Volcanoes, Black Sand & Tropical Solitude",
  subtitle: "Puna District → Hawaiʻi Volcanoes NP → Hilo → Kalapana Coast",
  description: "A solo explorer's guide to the Big Island's wild east side — based out of Hawaiian Paradise Park in the lush Puna district. This is the untouristy Hawaiʻi: active volcanoes, black sand beaches, steaming jungle vents, and a fiercely independent local community. April means warm trade winds, occasional tropical showers that make everything impossibly green, and the kind of solitude that rewires your brain.",
  duration: "3 nights / 4 days",
  dates: "Apr 23 – 26, 2026",
  budget: "Budget-Moderate",
  pace: "Relaxed — morning nature, afternoon exploration, evening unwinding",
  bestFor: "Solo travelers, nature lovers & volcano chasers",
  highlights: [
    "Hawaiʻi Volcanoes National Park — Kīlauea crater, Thurston Lava Tube & Chain of Craters Road",
    "Black sand beaches at Kehena & Pohoiki",
    "Pahoa Town — the Big Island's funky, off-grid heart",
    "Hilo — farmers market, Rainbow Falls & old-school Hawaiian town charm",
    "Lava Tree State Monument — eerie tree molds from a 1790 eruption",
    "Kapoho tide pools & geothermal coastline",
    "Star gazing in one of the darkest skies in the US",
    "Ahalanui Hot Pond (if reopened) & natural thermal pools",
    "Local fruit stands — lilikoi, rambutan, breadfruit, starfruit",
    "Uncle Robert's Wednesday Night Market in Kalapana"
  ],
  essentials: [
    { title: "🚗 Getting Around", text: "A rental car is absolutely essential. Hawaiian Paradise Park is about 30 min south of Hilo airport (ITO). Roads in Puna are mostly two-lane through jungle. Highway 11 south to Volcanoes NP is a stunning 45-min drive. 4WD not needed but a car is non-negotiable — there's zero public transit out here." },
    { title: "💵 Budget Tips", text: "Puna is the most affordable part of Hawaiʻi. Plate lunches run $10-14. Hilo restaurants are $15-30pp. Hawaiʻi Volcanoes NP is $30/car (valid 7 days). Fruit stands along Red Road sell papayas for $1. Grocery at KTA Super Stores in Keaʻau. Cook at your rental — most have kitchens." },
    { title: "🌴 April Weather", text: "Expect 75-82°F (24-28°C) with trade winds keeping it comfortable. Puna is the wet side — brief tropical showers are daily, usually clearing fast. Mornings are often sunny. Pack a light rain jacket and embrace the lush green that comes from all that rain. Volcanoes NP at 4,000ft elevation is noticeably cooler (60-70°F)." },
    { title: "🏨 Where to Stay", text: "Hawaiian Paradise Park puts you in the heart of Puna — jungle properties with coqui frog choruses at night. Expect a vacation rental or Airbnb, not a resort. This is real Hawaiʻi: off-grid vibes, fruit trees in the yard, maybe chickens. Pahoa town is 10 min away for supplies." },
    { title: "🌋 Volcano Safety", text: "Kīlauea is an active volcano. Check the USGS Hawaiian Volcano Observatory site before visiting. Stay on marked trails, don't enter closed areas, and be mindful of volcanic fog (vog) which can irritate lungs. The current eruption status changes — check nps.gov/havo for real-time updates." },
    { title: "📱 Useful Apps", text: "AllTrails (hiking in Volcanoes NP), USGS Volcanoes app (eruption status), Google Maps (offline maps essential — cell service is spotty in Puna), Yelp (Hilo restaurants)." }
  ],
  days: [
    {
      num: 1,
      title: "Puna Coast, Black Sand & Pahoa Town",
      neighborhoods: "Hawaiian Paradise Park · Pahoa · Kehena · Red Road",
      date: "Apr 23",
      mapPins: [
        { lat: 19.5837, lng: -154.9657, label: "Hawaiian Paradise Park", num: 1, cat: "activity", desc: "Home base in the lush Puna jungle" },
        { lat: 19.4924, lng: -154.9440, label: "Kehena Black Sand Beach", num: 2, cat: "activity", desc: "Secluded black sand cove with dolphins" },
        { lat: 19.4671, lng: -154.8565, label: "Pahoa Town", num: 3, cat: "food", desc: "Funky main street, restaurants & shops" },
        { lat: 19.4810, lng: -154.9100, label: "Lava Tree State Monument", num: 4, cat: "activity", desc: "Eerie lava molds of trees from 1790" },
        { lat: 19.4575, lng: -154.8350, label: "Pohoiki Black Sand Beach", num: 5, cat: "activity", desc: "New black sand beach created by 2018 lava" },
        { lat: 19.5200, lng: -154.9500, label: "Red Road (Hwy 137)", num: 6, cat: "activity", desc: "Scenic coastal drive through jungle" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Settle In & Red Road Drive", description: "Pick up your rental car at Hilo airport and drive 30 minutes south to Hawaiian Paradise Park through increasingly tropical scenery. Drop your bags, then head to the Red Road (Highway 137) — a winding, single-lane coastal road through dense jungle canopy that opens up to dramatic ocean views. This is the Big Island's wildest, least-developed coastline.", details: ["📍 Highway 137 runs from Kalapana to Pohoiki — about 12 miles of pure magic", "💡 Drive slowly. The road is narrow with blind curves, and locals drive it daily. Pull over at any ocean viewpoint."] },
            { title: "Lava Tree State Monument", description: "Stop at Lava Tree State Monument — a surreal park where a 1790 lava flow encased ōhiʻa trees, leaving standing lava molds after the wood burned away. A short loop trail winds through the ghostly formations in a dense rainforest setting. It's quiet, strange, and beautiful.", details: ["📍 Pahoa-Pohoiki Rd · Free · 15-30 min walk", "💡 The mosquitoes here are legendary. Bring bug spray."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Grab & Go from Keaʻau", description: "Stop at KTA Super Stores in Keaʻau on your way from the airport. Grab a poke bowl, musubi, and tropical fruit for a DIY first meal. This is how locals eat — plate lunch counters and supermarket deli.", meta: "$8-12 · Keaʻau Town Center · On the route from Hilo airport" }
          ],
          tips: [{ type: "tip", text: "Cell service in Puna is unreliable. Download offline Google Maps for the whole Big Island before leaving the airport." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Kehena Black Sand Beach", description: "Drive the Red Road to Kehena Beach — a hidden black sand cove at the bottom of a short but steep trail. The sand is jet black volcanic glass, the water is deep blue, and spinner dolphins often play in the bay. This is clothing-optional and very chill. The energy is pure old Hawaiʻi — hippies, locals, and no one in a hurry.", details: ["📍 Mile marker 19 on Hwy 137 · Free · Steep 5-min trail down", "💡 Swim with caution — no lifeguard, strong currents. Best on calm days. The dolphins usually show up mid-morning to early afternoon."] },
            { title: "Pohoiki Black Sand Beach", description: "Continue to Pohoiki — a brand new black sand beach literally created by the 2018 Kīlauea eruption. Lava flowed here and created fresh coastline. The beach is still forming and evolving. There's a boat ramp and natural warm springs nearby where geothermally heated water meets the ocean.", details: ["📍 End of Pohoiki Rd · Free parking", "💡 The warm springs at Pohoiki are where warm freshwater seeps through the new lava rock. Locals soak here."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Kaleo's Bar & Grill", description: "Pahoa's most popular restaurant — American comfort food with Hawaiian touches in a laid-back open-air setting. The fish tacos and kalua pork are excellent. Good craft beer selection. This is where Puna locals actually eat.", meta: "$15-28pp · 15-2969 Pahoa Village Rd · Walk-in usually fine" }
          ],
          tips: [{ type: "reddit", text: "Kehena is the real deal. No tourists. Just black sand, dolphins, and vibes. The hike down is steep but short. Don't leave valuables in your car.", cite: "r/BigIsland" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Pahoa Town Stroll", description: "Explore Pahoa — Puna's funky main street town with a Wild West boardwalk vibe. Eclectic shops, crystal stores, organic cafés, and a community that survived the 2018 lava crisis together. The town has real character — part hippie commune, part old Hawaiʻi, entirely itself.", details: ["📍 Pahoa Village Rd — the main drag is about 3 blocks", "💡 Check if Akebono Theater (a 1917 building) has anything going on. Pahoa is tiny but mighty."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Ning's Thai Cuisine", description: "A Pahoa institution — authentic Thai food that has no business being this good in a tiny jungle town. The green curry and pad see ew are outstanding. Tiny restaurant, big flavors, very affordable. BYOB is common at small Pahoa restaurants.", meta: "$12-20pp · Pahoa Village Rd · Cash preferred" }
          ],
          tips: [{ type: "tip", text: "The coqui frogs will serenade you all night. They're tiny but LOUD. Earplugs if you're a light sleeper — or just surrender to the jungle symphony." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Stargazing from Your Rental", description: "Step outside your rental and look up. Puna has some of the darkest skies in the US — minimal light pollution from the surrounding jungle. On a clear night, the Milky Way is vivid. April means good visibility of the Southern Cross low on the horizon. Bring a blanket, lie on the grass, and let the coqui frogs be your soundtrack.", details: ["💡 If you have binoculars, bring them. The star clusters visible from Hawaiʻi at this latitude are extraordinary."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Hawaiʻi Volcanoes National Park",
      neighborhoods: "Kīlauea · Chain of Craters Road · Volcano Village",
      date: "Apr 24",
      mapPins: [
        { lat: 19.4194, lng: -155.2885, label: "Kīlauea Visitor Center", num: 1, cat: "activity", desc: "Park HQ with eruption updates & exhibits" },
        { lat: 19.4120, lng: -155.2362, label: "Kīlauea Overlook / Halemaʻumaʻu", num: 2, cat: "activity", desc: "Massive summit caldera — may be erupting" },
        { lat: 19.4133, lng: -155.2380, label: "Thurston Lava Tube", num: 3, cat: "activity", desc: "Walk-through 500-year-old lava tube" },
        { lat: 19.3095, lng: -155.0972, label: "Hōlei Sea Arch", num: 4, cat: "activity", desc: "End of Chain of Craters Road — dramatic coast" },
        { lat: 19.4400, lng: -155.2500, label: "Volcano Village", num: 5, cat: "food", desc: "Charming misty village at 4,000ft elevation" },
        { lat: 19.4000, lng: -155.2600, label: "Devastation Trail", num: 6, cat: "activity", desc: "Boardwalk through 1959 eruption fallout zone" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Volcanoes National Park", description: "Take Highway 11 south from HPP — a 45-minute drive through macadamia nut orchards and elevation gain from sea level to 4,000 feet. The temperature drops noticeably and the vegetation shifts from tropical to native ōhiʻa forest. Stop at the Kīlauea Visitor Center for current eruption status and trail conditions.", details: ["📍 Hawaii Volcanoes NP · $30/vehicle (valid 7 days)", "💡 Arrive by 9am to beat tour bus crowds. Check nps.gov/havo for real-time eruption status before driving up."] },
            { title: "Thurston Lava Tube (Nāhuku)", description: "Walk through a 500-year-old lava tube — a massive underground tunnel carved by flowing lava. The entrance trail descends through a lush tree fern forest (it feels like Jurassic Park). The tube itself is lit and walkable — about 600 feet of raw volcanic geology. An extended, unlit section continues for the adventurous.", details: ["📍 Crater Rim Drive · Free with park entry · 20-30 min", "💡 Bring a flashlight for the extended unlit portion — it's 4x longer than the main tube and far more atmospheric."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Cafe Ono", description: "A beloved breakfast spot in Volcano Village just outside the park. Fresh-baked pastries, excellent coffee, and a misty rainforest garden setting. The banana bread is legendary. Run by a local couple who pour real aloha into every cup.", meta: "$8-14pp · Volcano Village · Cash and card accepted" }
          ],
          tips: [{ type: "reddit", text: "Get to the park EARLY. By 10am the tour buses arrive and Thurston Lava Tube gets a line. At 8:30am you'll have it to yourself. The extended unlit section is 100x better than the main tube.", cite: "r/VisitingHawaii" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Chain of Craters Road", description: "Drive the spectacular Chain of Craters Road — 19 miles of descent from the summit to the coast, passing ancient craters, lava fields, and petroglyphs. The landscape shifts from rainforest to barren moonscape as you drop 3,700 feet to sea level. At the end: the Hōlei Sea Arch, where hardened lava meets crashing Pacific waves.", details: ["📍 Starts near Devastation Trail, ends at coast · 2-3 hours round trip with stops", "💡 Stop at the Puʻu Loa Petroglyphs — a short hike to see over 23,000 Hawaiian petroglyphs carved into pahoehoe lava. Bring water — no services on this road."] },
            { title: "Kīlauea Overlook & Halemaʻumaʻu Crater", description: "Return to the summit and walk to the Kīlauea Overlook for views into Halemaʻumaʻu Crater — the home of Pele, goddess of fire. If Kīlauea is actively erupting, the glow is visible even in daylight. The scale of the caldera is staggering — over 2 miles across. Steam vents along the rim trail add to the otherworldly atmosphere.", details: ["📍 Crater Rim Trail between overlooks · Multiple viewpoints", "💡 Come back at sunset or after dark if there's active eruption — the lava glow against the night sky is a once-in-a-lifetime sight."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Volcano House Restaurant", description: "The only restaurant inside the national park — perched right on the rim of Kīlauea Caldera. The views are insane. The food is solid (not exceptional) but you're eating lunch while looking into an active volcano. Try the local fish or kalua pork plate. Worth it for the setting alone.", meta: "$18-30pp · Inside the park on Crater Rim · Reservations helpful" }
          ],
          tips: [{ type: "tip", text: "Pack snacks and a full water bottle for Chain of Craters Road. There are zero services for the entire 19-mile drive. The return drive uphill takes longer than going down." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Volcano Village Exploration", description: "Before heading back to Puna, spend time in Volcano Village — a misty, cool hamlet at 4,000 feet with art galleries, a general store, and a bohemian vibe. The contrast with coastal Puna is striking: here it's ferns, fog, and fleece jackets. The village has a tight-knit artist community.", details: ["📍 Old Volcano Road, just outside the park's west entrance", "💡 Volcano Garden Arts has beautiful gardens and a gallery worth browsing."] },
            { title: "Return for Sunset / Night Glow", description: "If Kīlauea is erupting: return to the park after dinner for the night glow. The lava lake in Halemaʻumaʻu casts an orange-red glow visible from the overlooks — it's transcendent. Even without eruption, the steam vents glow eerily in the dark and the stars above the caldera are spectacular.", details: ["💡 The park is open 24 hours. Night visits during active eruptions are some of the most memorable experiences in all of Hawaiʻi."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Thai Thai Bistro & Bar", description: "Volcano Village's go-to dinner spot. Excellent Thai food in a warm, wood-paneled space. The curries are rich and aromatic, portions generous. A popular locals' spot — the owner moved from Bangkok and cooks with serious skill. Perfect warming food after a day at elevation.", meta: "$14-24pp · 19-4084 Old Volcano Rd · Reservations recommended on weekends" }
          ],
          tips: [{ type: "reddit", text: "If the volcano is actively erupting when you visit, GO BACK AT NIGHT. The lava glow from Halemaʻumaʻu after dark is genuinely life-changing. We sat on the rim for two hours just watching.", cite: "r/BigIsland" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Drive Back Through the Dark", description: "The 45-minute drive back to HPP through the dark jungle is atmospheric — keep an eye out for mongoose and listen to the coqui frogs intensify as you descend back to sea level. The temperature shift from 65°F at the summit to 78°F at the coast is palpable.", details: ["💡 The drive is safe but dark. Go slowly — unlit roads with occasional pedestrians."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Hilo Town, Waterfalls & Farmers Market",
      neighborhoods: "Hilo · Pepeʻekeo · Wainaku · Boiling Pots",
      date: "Apr 25",
      mapPins: [
        { lat: 19.7241, lng: -155.0868, label: "Hilo Farmers Market", num: 1, cat: "food", desc: "Hawaiʻi's best farmers market — Wed & Sat" },
        { lat: 19.7310, lng: -155.1063, label: "Rainbow Falls", num: 2, cat: "activity", desc: "80-foot waterfall with morning rainbows" },
        { lat: 19.7360, lng: -155.1150, label: "Boiling Pots (Peʻepeʻe Falls)", num: 3, cat: "activity", desc: "Cascading pools in volcanic rock" },
        { lat: 19.7280, lng: -155.0900, label: "Downtown Hilo", num: 4, cat: "activity", desc: "Historic bayfront town with retro charm" },
        { lat: 19.7750, lng: -155.0920, label: "Pepeʻekeo Scenic Route", num: 5, cat: "activity", desc: "4-mile detour through jungle & bridges" },
        { lat: 19.7235, lng: -155.0750, label: "Hilo Bay", num: 6, cat: "activity", desc: "Calm bay with Mauna Kea backdrop" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Hilo Farmers Market", description: "The Hilo Farmers Market is the best in Hawaiʻi — maybe the best in the US. Over 200 vendors on Wednesdays and Saturdays sell tropical fruit you've never seen (rambutan, longan, soursop, dragonfruit, lilikoi), fresh flower leis, macadamia nut products, local honey, and hot food. The colors, smells, and energy are electric. Go hungry.", details: ["📍 Mamo St & Kamehameha Ave, Downtown Hilo · Wed & Sat 6am-4pm are the big days", "💡 Wednesday market is great but Saturday is the main event. Either way, arrive before 9am for the best selection and fewer crowds."] },
            { title: "Rainbow Falls (Waiānuenue)", description: "A 5-minute drive from downtown Hilo brings you to Rainbow Falls — an 80-foot waterfall that cascades into a lush gorge. In the morning sun, rainbows form in the mist (hence the name). The viewing area is right at the parking lot — no hiking required. A quick but stunning stop.", details: ["📍 Waiānuenue Ave · Free · 5 minutes from downtown", "💡 Go between 9-10am for the best rainbow formation. The falls are in a cave sacred to Hina, mother of Maui in Hawaiian mythology."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hilo Farmers Market Grazing", description: "Skip a sit-down breakfast and graze the market. Fresh lilikoi juice, hot malasadas (Portuguese donuts), musubi, poke, tropical smoothies, and whatever exotic fruit catches your eye. Budget $10-15 and eat like a king. This IS the breakfast.", meta: "$10-15 · Multiple vendors · Cash preferred, some take cards" }
          ],
          tips: [{ type: "reddit", text: "The Hilo farmers market is NOT the sanitized mainland type. This is farmers and aunties who've been selling here for decades. Buy the white pineapple — it's the sweetest thing you'll ever eat. And the $1 apple bananas.", cite: "r/BigIsland" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Boiling Pots & Peʻepeʻe Falls", description: "Continue upriver to Boiling Pots — a series of natural pools connected by underground lava tubes that make the water appear to boil when the river is flowing strong. Peʻepeʻe Falls cascades into the top pool. The pools are surrounded by lush tropical vegetation. Swimming is prohibited (dangerous currents) but the views are spectacular.", details: ["📍 Pepeʻekeo Falls Dr · Free · Just upstream from Rainbow Falls", "💡 Despite the 'no swimming' signs, locals do swim here on calm days. As a visitor, enjoy the view — flash flooding is real and deadly."] },
            { title: "Downtown Hilo Walking Tour", description: "Hilo's downtown is frozen in mid-century Hawaiʻi — vintage storefronts, mom-and-pop shops, and zero chain restaurants. Walk along Kamehameha Avenue and the bayfront. Visit the Pacific Tsunami Museum (fascinating and sobering), browse Big Island Book Buyers, and check out the old movie theaters. Hilo is what Hawaiʻi looked like before resorts.", details: ["📍 Kamehameha Ave — the main bayfront strip · Most shops open 10am-5pm", "💡 Hilo gets more rain than almost anywhere in the US. If a shower rolls in, duck into a café — it'll pass in 15 minutes."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Café Pesto", description: "A Hilo institution in the historic S. Hata Building on the bayfront. Wood-fired pizzas, fresh fish, and creative pastas using local ingredients. The calzone with local goat cheese and the fresh catch are standouts. Beautiful high-ceiling space with views of Hilo Bay.", meta: "$16-28pp · 308 Kamehameha Ave · Walk-in or call ahead" }
          ],
          tips: [{ type: "tip", text: "Hilo is the antidote to resort Hawaiʻi. No high-rises, no chain stores, no pretense. Just a real working Hawaiian town with incredible natural beauty. Give it time — it grows on you fast." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Pepeʻekeo Scenic Route", description: "On the drive back toward HPP, take the 4-mile Pepeʻekeo Scenic Route — an old highway that winds through tropical jungle, one-lane bridges, and ocean viewpoints. It's a beautiful golden-hour drive with the lush vegetation glowing in the late sun. Reconnects to Highway 19 after a few magical miles.", details: ["📍 Old Māmalahoa Highway — turnoff is just north of Hilo", "💡 This is a real shortcut that doubles as scenery. The single-lane bridges are a throwback to old Hawaiʻi."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Hilo Bay Café", description: "Hilo's finest dining — sophisticated farm-to-table cuisine using Big Island ingredients in a warm, contemporary space. The menu changes daily based on what local farmers and fishermen bring in. The macadamia-crusted fish and Hamakua mushroom dishes are exceptional. A proper farewell dinner.", meta: "$30-50pp · 315 Makaala St · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Hilo Bay Café is legitimately one of the best restaurants on the island, any coast. The chef sources everything locally and the quality shows. Make a reservation.", cite: "r/BigIsland" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Final Night in the Jungle", description: "Back at your HPP rental, take in one last jungle evening. Sit on the lānai with a local beer (Mehana Brewing or Big Island Brewhaus), listen to the coqui frogs, and feel the trade winds. Tomorrow you leave this wild, untamed corner of Hawaiʻi. Let it soak in.", details: ["💡 If it's a Wednesday: Uncle Robert's Night Market in Kalapana (5-9pm) has live music, food vendors, and a very local Puna vibe. Worth the 20-min drive."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Morning Swim, Fruit Stands & Departure",
      neighborhoods: "Puna Coast · Keaʻau · Hilo Airport",
      date: "Apr 26",
      mapPins: [
        { lat: 19.4924, lng: -154.9440, label: "Kehena Beach (Sunrise)", num: 1, cat: "activity", desc: "One last dip in black sand paradise" },
        { lat: 19.5500, lng: -154.9600, label: "Puna Fruit Stands", num: 2, cat: "food", desc: "Roadside tropical fruit on Hwy 130" },
        { lat: 19.6400, lng: -155.0300, label: "Keaʻau Town", num: 3, cat: "food", desc: "Last stop for coffee & plate lunch" },
        { lat: 19.7200, lng: -155.0480, label: "Hilo International Airport", num: 4, cat: "activity", desc: "ITO — small, easy airport" },
        { lat: 19.4810, lng: -154.9100, label: "Lava Tree (revisit)", num: 5, cat: "activity", desc: "Quick morning stop if time allows" },
        { lat: 19.5837, lng: -154.9657, label: "Hawaiian Paradise Park", num: 6, cat: "activity", desc: "Pack up & say goodbye to the jungle" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sunrise at Kehena or Pohoiki", description: "If you're an early riser, drive down to Kehena or Pohoiki for a sunrise swim. The east-facing coastline means the sun rises directly over the ocean. At Kehena, the black sand catches the golden light beautifully. Even if you just sit on the sand with coffee and watch the sun come up, it's a perfect final morning.", details: ["📍 20-25 min drive from HPP · Sunrise around 6:00am in April", "💡 Bring a thermos of coffee and a towel. You'll have the beach largely to yourself at sunrise."] },
            { title: "Fruit Stand Tour on Highway 130", description: "Drive back via Highway 130 and stop at the roadside fruit stands that dot the road between Pahoa and Keaʻau. Fresh-picked papayas, lilikoi, starfruit, rambutan, and apple bananas — often on the honor system. Load up a bag of tropical fruit for the journey home. This is peak Puna.", details: ["💡 The best stands are between mile markers 10-15 on Hwy 130. Look for hand-painted signs. Prices are absurdly cheap compared to mainland grocery stores."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Vibe Café (Keaʻau)", description: "A solid café in Keaʻau for a last proper meal before the airport. Good coffee, açaí bowls, and breakfast burritos. Chill vibe (living up to its name) with a local crowd. Alternatively, grab one last poke bowl from KTA.", meta: "$10-16pp · Keaʻau Town Center · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Hilo airport (ITO) is tiny and low-stress. You can arrive 60-75 minutes before an interisland flight. TSA lines are usually under 10 minutes." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Departure from Hilo", description: "Return your rental car and fly out of Hilo International Airport. ITO is one of the most relaxed airports in the US — open-air walkways, no jetways, and views of Mauna Kea from the terminal. A fitting low-key goodbye to this low-key island.", details: ["📍 Hilo International Airport (ITO) · 30 min from HPP", "💡 If flying to Honolulu to connect: the interisland flight gives you aerial views of the entire Big Island coastline. Window seat on the left side."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Pack your tropical fruit in your checked bag if flying interisland to Honolulu (allowed). If flying to the mainland: most fresh fruit is prohibited due to agriculture inspection. Eat it before security!" }]
        }
      ]
    }
  ]
};

// Run fulfillment
(async () => {
  try {
    const result = fulfillOrder(order, itineraryData);
    console.log('\n🎉 Fulfillment complete!');
    console.log('Slug:', result.slug);
    console.log('URL:', result.url);
    console.log('Email sent:', result.emailSent);
  } catch (err) {
    console.error('❌ Fulfillment failed:', err.message);
    process.exit(1);
  }
})();
