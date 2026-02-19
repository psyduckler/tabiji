const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771468222901_hu3wz4",
  email: "bernard.j.huang@gmail.com",
  destination: "Kaohsiung, Gushan District, Kaohsiung City, Taiwan",
  start_date: "2026-02-26",
  end_date: "2026-02-28",
  group_size: "1",
  travel_style: "Cultural, Relaxation",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-19T02:30:22.901Z",
  status: "pending"
};

const itineraryData = {
  destination: "Kaohsiung, Taiwan",
  countryEmoji: "🇹🇼",
  title: "Kaohsiung in 2 Nights: Harbor Art, Temple Calm & Island Sunsets",
  subtitle: "Pier 2 Arts → Cijin Island → Lotus Pond → Gushan Trails",
  description: "A solo cultural and relaxation guide to Kaohsiung — Taiwan's harbor city reinvented. Wander open-air art warehouses along the waterfront, ferry to a tiny island for seafood and sunsets, hike through old Japanese-era tunnels, and find quiet in lotus-filled temple ponds. February means perfect weather: warm days, cool evenings, no crowds.",
  duration: "2 nights / 3 days",
  dates: "Feb 26 – 28, 2026",
  budget: "Budget-friendly",
  pace: "Relaxed — mornings exploring, afternoons slow, evenings unwinding",
  bestFor: "Solo travelers, culture seekers & those who need to slow down",
  highlights: [
    "Pier 2 Art Center — massive waterfront warehouse art district",
    "Cijin Island — 5-minute ferry, seafood alley, lighthouse, black-sand beach",
    "Former British Consulate at Takow — hilltop colonial history with harbor views",
    "Lotus Pond — Dragon & Tiger Pagodas, temples reflected in still water",
    "Dome of Light at Formosa Boulevard — world's largest glass art installation",
    "Shoushan (Monkey Mountain) — coastal trail with city panoramas",
    "Love River evening walk — lit bridges, café boats, quiet reflections",
    "Night markets — Liuhe and Ruifeng for street food grazing",
    "Sizihwan Beach — sunset spot tucked below the mountain",
    "Hot springs nearby — Baolai for a day trip soak"
  ],
  essentials: [
    { title: "🚇 Getting Around", text: "Kaohsiung's KMRT (metro) has two lines — Red and Orange — that cover most tourist areas. The Orange Line runs to Gushan and the waterfront. Get an iPass or EasyCard at any convenience store for metro, buses, ferries, and YouBike rentals. The Circular Light Rail connects Pier 2 to the Seaport area. Most attractions in Gushan are walkable. The ferry to Cijin Island is a 5-minute ride from Gushan Ferry Pier (NT$25 with EasyCard)." },
    { title: "💵 Budget Tips", text: "Kaohsiung is very affordable. Night market meals run NT$50-150 ($1.50-5 USD). Sit-down restaurants are NT$150-400 ($5-13). Most temples and parks are free. The KMRT is NT$20-65 per ride. YouBike is NT$10 per 30 min. Budget NT$1,500-2,500/day ($50-80) for food, transport, and activities. Accommodation runs $30-80/night for good options." },
    { title: "☀️ February Weather", text: "February in Kaohsiung is ideal — 18-24°C (64-75°F), dry, low humidity, and sunny. Perfect walking weather. Evenings can dip to 15°C so bring a light jacket. Rain is unlikely. This is southern Taiwan's best season." },
    { title: "🏨 Where to Stay", text: "Stay near Pier 2 / Yancheng for the best location — walking distance to the art district, ferry pier, Love River, and Gushan attractions. The area around MRT Yanchengpu or Salt Yancheng stations is ideal. Alternatively, near Formosa Boulevard for central access to both metro lines." },
    { title: "🍜 Food Culture", text: "Kaohsiung is a street food city. Don't miss: grilled squid and seafood on Cijin Island, papaya milk (invented here), danzai noodles, braised pork rice (lu rou fan), and shaved ice with fresh mango (still available in Feb from greenhouses). Liuhe Night Market is the classic tourist market; Ruifeng is where locals go." },
    { title: "📱 Useful Apps", text: "Google Maps works perfectly for transit. 7-ELEVEN and FamilyMart are everywhere for snacks, cash withdrawal, and EasyCard top-ups. Download 'Taiwan eBus' for real-time bus tracking. LINE is the local messaging app if connecting with anyone." }
  ],
  days: [
    {
      num: 1,
      title: "Pier 2 Art District, British Consulate & Cijin Island",
      neighborhoods: "Gushan · Yancheng · Cijin Island",
      date: "Feb 26",
      mapPins: [
        { lat: 22.6196, lng: 120.2815, label: "Pier 2 Art Center", num: 1, cat: "activity", desc: "Massive waterfront warehouse art district" },
        { lat: 22.6148, lng: 120.2716, label: "Hamasen Railway Cultural Park", num: 2, cat: "activity", desc: "Old railway tracks turned into art installation park" },
        { lat: 22.6241, lng: 120.2657, label: "Former British Consulate at Takow", num: 3, cat: "activity", desc: "Hilltop colonial building with harbor panorama" },
        { lat: 22.6213, lng: 120.2635, label: "Gushan Ferry Pier", num: 4, cat: "activity", desc: "5-min ferry to Cijin Island" },
        { lat: 22.6290, lng: 120.2591, label: "Cijin Island Seafood Street", num: 5, cat: "food", desc: "Fresh seafood alley right off the ferry" },
        { lat: 22.6343, lng: 120.2600, label: "Cijin Lighthouse", num: 6, cat: "activity", desc: "Historic lighthouse with ocean views" },
        { lat: 22.6112, lng: 120.2868, label: "Love River", num: 7, cat: "activity", desc: "Evening waterfront walk" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Pier 2 Art Center", description: "Start your trip at Kaohsiung's crown jewel — a sprawling complex of repurposed harbor warehouses filled with contemporary art, street murals, sculptures, indie shops, and craft studios. The outdoor areas between warehouses are lined with installations and old railway tracks. Rent a YouBike and cruise along the waterfront promenade. In the morning, it's quiet and meditative — just you and the art.", details: ["📍 Take the Orange Line to Yanchengpu Station, exit 1 — Pier 2 is a 5-min walk", "💡 The outdoor murals and sculptures are free and best in morning light. Indoor galleries vary — most are free or NT$50-100."] },
            { title: "Hamasen Railway Cultural Park", description: "Adjacent to Pier 2, this park preserves old Japanese-era railway tracks and switches. The miniature trains, old signal equipment, and the elevated Sky Balcony walkway give sweeping harbor views. Peaceful and photogenic.", details: ["📍 Connected to Pier 2 — just keep walking along the tracks"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Pier 2 Coffee Shops", description: "Several indie coffee shops and bakeries are scattered through the Pier 2 warehouses. Grab a flat white and a pastry at one of the artsy cafés inside the converted warehouses. In-Blossom and Cest si Bon are popular picks.", meta: "NT$120-200 · Pier 2 area · Walk-in" }
          ],
          tips: [{ type: "tip", text: "YouBike stations are everywhere around Pier 2. The dedicated waterfront bike path runs from Pier 2 all the way to Sizihwan Beach — it's one of the best urban bike rides in Taiwan." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Former British Consulate at Takow", description: "Walk up the hill to this beautifully restored 1879 British consulate — the oldest surviving consulate building in Taiwan. The hilltop location offers a stunning 270° panorama of Kaohsiung Harbor, Cijin Island, and the open sea. There's a small museum inside about the port's trading history, and a café on the terrace where you can sit with a tea and watch ships pass.", details: ["📍 At the top of the hill near Gushan Ferry Pier — about a 10-min uphill walk", "💡 Admission is NT$99 (includes a drink voucher for the terrace café). Worth it for the view alone."] },
            { title: "Ferry to Cijin Island", description: "Walk down to Gushan Ferry Pier and catch the 5-minute ferry to Cijin Island — a narrow barrier island that guards the harbor entrance. It's a completely different world: seafood restaurants, narrow lanes with temple incense, a lighthouse, and a long black-sand beach on the ocean side.", details: ["📍 Gushan Ferry Pier — swipe EasyCard, NT$25 each way", "💡 Ferries run every 5-10 minutes. You can bring a YouBike on the ferry for free."] },
            { title: "Cijin Island Exploring", description: "Wander Cijin's main lane — lined with grilled seafood stalls, dried fish shops, and the ornate Tianhou Temple (one of the oldest in Kaohsiung). Walk or bike to the Cijin Lighthouse at the northern tip for stunning views. Then cross to the ocean side for the black-sand beach and the surreal Rainbow Church art installation.", details: ["📍 The island is small — easily walkable in 2-3 hours", "💡 The Cihou Starlight Tunnel cuts through the hill to the lighthouse — it's dark, atmospheric, and beautiful."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cijin Seafood Street", description: "The alley right off the Cijin ferry terminal is packed with seafood restaurants and stalls. Grab grilled squid on a stick, fried fish cakes, and fresh sashimi. Small shops with plastic stools and ice-cold Taiwan Beer — unpretentious and delicious. Point-and-choose at the display counters.", meta: "NT$200-400 · Cijin Ferry Terminal area · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Cijin Island is best visited on a weekday — weekends it gets packed with local tourists. The grilled squid near the ferry terminal is legitimately some of the best street food in Kaohsiung.", cite: "r/taiwan" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sizihwan Beach Sunset", description: "Head to Sizihwan Beach, tucked below Shoushan mountain on the mainland side. It's Kaohsiung's best sunset spot — watch the sun drop into the Taiwan Strait while sitting on the seawall. The beach is small and calm, with a few cafés nearby. Pure relaxation.", details: ["📍 A short walk from Sizihwan MRT station (Orange Line) or from the British Consulate area"] },
            { title: "Love River Evening Walk", description: "After sunset, walk along the Love River — Kaohsiung's revitalized urban waterway. The bridges are lit with colorful lights, café boats line the banks, and the evening breeze is perfect. Start near the river mouth and walk upstream past the illuminated pedestrian bridges. Quiet, reflective, perfect for solo wandering.", details: ["📍 Start near Yanchengpu MRT and walk north along the east bank"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Liuhe Night Market", description: "Kaohsiung's most famous night market — two blocks of food stalls specializing in seafood. Must-tries: papaya milk (Kaohsiung's signature drink), salt-crusted shrimp, oyster omelets, and stinky tofu. It's a solo traveler's paradise — order small portions, try everything, keep moving.", meta: "NT$150-300 total · MRT Formosa Boulevard, exit 11 · Open 5pm-midnight" }
          ],
          tips: [{ type: "tip", text: "Liuhe is touristy but the food is genuinely good. For a more local experience, Ruifeng Night Market (near Kaohsiung Arena MRT) has more variety and lower prices — save it for tomorrow night." }]
        }
      ]
    },
    {
      num: 2,
      title: "Lotus Pond Temples, Dome of Light & Night Market",
      neighborhoods: "Zuoying · Formosa Boulevard · Kaohsiung Arena",
      date: "Feb 27",
      mapPins: [
        { lat: 22.6814, lng: 120.2945, label: "Lotus Pond", num: 1, cat: "activity", desc: "Temple-lined lake with pagodas and pavilions" },
        { lat: 22.6830, lng: 120.2956, label: "Dragon & Tiger Pagodas", num: 2, cat: "activity", desc: "Iconic twin pagodas — enter dragon, exit tiger" },
        { lat: 22.6800, lng: 120.2940, label: "Spring & Autumn Pavilions", num: 3, cat: "activity", desc: "Lakeside temple with Guanyin riding a dragon" },
        { lat: 22.6838, lng: 120.2975, label: "Confucius Temple", num: 4, cat: "activity", desc: "Largest Confucius temple in Taiwan" },
        { lat: 22.6316, lng: 120.3015, label: "Dome of Light", num: 5, cat: "activity", desc: "World's largest glass art installation in a metro station" },
        { lat: 22.6654, lng: 120.3024, label: "Kaohsiung Museum of Fine Arts", num: 6, cat: "activity", desc: "Major art museum in a lakeside park" },
        { lat: 22.6557, lng: 120.3070, label: "Ruifeng Night Market", num: 7, cat: "food", desc: "Local favorite night market" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Lotus Pond (Lianchi Tan)", description: "Take the Red Line to Zuoying and walk to Lotus Pond — a serene lake ringed with ornate temples, pagodas, and pavilions. In the morning light, the reflections are magical. Walk the full loop: enter the Dragon & Tiger Pagodas (enter through the dragon's mouth, exit the tiger's — it's tradition and brings good luck), visit the Spring & Autumn Pavilions with Guanyin riding a dragon over the water, and the towering Beiji Xuantian Shang Di temple.", details: ["📍 MRT Zuoying (Red Line) or Ecological District Station — 10-min walk to the pond", "💡 All temples are free. The full loop around the pond takes about 90 minutes at a relaxed pace. Morning is quieter and cooler."] },
            { title: "Zuoying Confucius Temple", description: "On the north end of Lotus Pond, Taiwan's largest Confucius Temple is a beautiful complex of traditional architecture. The grounds are peaceful, with koi ponds and centuries-old trees. It's an active place of worship — you might see students praying before exams.", details: ["📍 Adjacent to Lotus Pond's north shore · Free admission"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Traditional Taiwanese Breakfast Shop", description: "Find a local breakfast shop (早餐店) near your hotel — they're everywhere and quintessentially Taiwanese. Order dan bing (egg crepe), fan tuan (sticky rice roll), and warm soy milk. It'll cost you about NT$60-80 for a full breakfast. This is how Taiwan starts every morning.", meta: "NT$60-80 · Any neighborhood · Walk-in, most close by 11am" }
          ],
          tips: [{ type: "tip", text: "Lotus Pond is Kaohsiung's most Instagrammable spot. The Dragon & Tiger Pagodas reflected in the still morning water are iconic. Go before 9am for the best light and fewest people." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Kaohsiung Museum of Fine Arts", description: "Head to KMFA — one of Taiwan's premier art museums, set in the beautiful Neiwei Cultural Park in Gushan District. The permanent collection covers Taiwanese modern and contemporary art, and rotating exhibitions are consistently excellent. The surrounding park has lakes, walking paths, and sculptures. Perfect for a slow afternoon.", details: ["📍 Take the Red Line to Aozihdi Station, walk 10 min through the park", "💡 Admission is NT$90 for special exhibitions, permanent collection often free. Closed Mondays — but Feb 27 is Friday, you're good."] },
            { title: "Dome of Light at Formosa Boulevard", description: "Stop at Formosa Boulevard MRT station (where the Red and Orange lines cross) to see the Dome of Light — the largest glass art installation in the world. Italian artist Narcissus Quagliata created 4,500 glass panels telling the story of human life. Stand in the center and look up. It's breathtaking.", details: ["📍 Formosa Boulevard MRT Station — it's literally inside the station, free", "💡 The light changes throughout the day. There are brief light shows at set times — check the schedule posted in the station."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Simon Salary Stew with Rice (賽門薪傳)", description: "A beloved local spot in Gushan District near Aozihdi MRT. Hearty Taiwanese stew rice bowls — braised pork, stewed beef, and traditional sides. Small, bustling, authentic. The kind of place only locals know about.", meta: "NT$100-180 · Gushan District · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "The Dome of Light is genuinely impressive in person — photos don't do it justice. Visit during a light show time if you can. It's free and takes 10 minutes. No reason not to stop.", cite: "r/taiwan" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Relaxation Time", description: "Take the afternoon slow. Head back to your hotel for a rest, or find a quiet café in the Yancheng area. Kaohsiung's café culture is underrated — many converted old buildings into beautiful coffee shops. Try BOOKING (a café in a bookshop) or Café de Rio along the Love River for waterfront coffee and a book.", details: [] },
            { title: "Ruifeng Night Market", description: "For tonight, skip the tourist markets and go where locals go: Ruifeng Night Market near Kaohsiung Arena MRT. It's huge, chaotic, and incredible. Hundreds of stalls selling everything from Japanese-style takoyaki to pepper buns to grilled corn to fresh fruit juices. No tourists, just pure Kaohsiung street food energy.", details: ["📍 MRT Kaohsiung Arena (Red Line), exit 1 — market is right there", "💡 Open Tuesday, Thursday, Friday, Saturday, Sunday nights. Closed Mon & Wed. Feb 27 is Friday — you're in luck."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Ruifeng Night Market Crawl", description: "Graze your way through. Must-tries: pepper buns (胡椒餅), flame-grilled steak on a hot plate (NT$100!), shaved ice with condensed milk, Taiwanese fried chicken (鹹酥雞), and fresh squeezed juices. Eat small portions from many stalls — that's the move.", meta: "NT$200-400 total · Open ~6pm-midnight · Near Kaohsiung Arena MRT" }
          ],
          tips: [{ type: "reddit", text: "Ruifeng > Liuhe for food quality and price. Liuhe is fine for tourists but Ruifeng is where Kaohsiung people actually eat. Go hungry.", cite: "r/taiwan" }]
        }
      ]
    },
    {
      num: 3,
      title: "Shoushan Morning Hike & Departure",
      neighborhoods: "Gushan · Sizihwan",
      date: "Feb 28",
      mapPins: [
        { lat: 22.6300, lng: 120.2650, label: "Shoushan (Monkey Mountain)", num: 1, cat: "activity", desc: "Coastal mountain trail with monkeys and views" },
        { lat: 22.6260, lng: 120.2630, label: "Sizihwan Beach", num: 2, cat: "activity", desc: "Quiet beach below the mountain" },
        { lat: 22.6196, lng: 120.2815, label: "Pier 2 (return visit)", num: 3, cat: "food", desc: "Final waterfront coffee and browsing" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Shoushan (Monkey Mountain) Hike", description: "Start your last day with a morning hike up Shoushan — the mountain that rises right behind Gushan District. The trails wind through tropical forest with Formosan macaques (they're everywhere — friendly but don't feed them). Several viewpoints offer panoramic views of the harbor, Cijin Island, and the city stretching south. The main trail takes about 60-90 minutes round trip and is well-maintained.", details: ["📍 Main trailhead near Shoushan Yuanheng Temple — walkable from Sizihwan MRT", "💡 Go early (before 8am) for cooler temperatures and active monkeys. Bring water. The trail is shaded but can be humid."] },
            { title: "Sizihwan Tunnel & Beach", description: "On the way down, pass through the atmospheric Sizihwan Old Tunnel (formerly a Japanese WWII air-raid shelter, now an art installation) and emerge at Sizihwan Beach. Sit on the seawall, breathe in the ocean air, and watch the fishing boats. A perfectly calm end to the trip.", details: ["📍 The tunnel entrance is near the Sizihwan MRT station area"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Local Breakfast + Coffee at Pier 2", description: "Grab a quick dan bing or fan tuan from a breakfast shop, then walk to Pier 2 for a proper coffee at one of the warehouse cafés. The morning light on the harbor warehouses is beautiful. Browse any galleries you missed on day one.", meta: "NT$60-80 breakfast + NT$120-180 coffee" }
          ],
          tips: [{ type: "tip", text: "Don't bring food or plastic bags on Shoushan — the macaques will grab them. Keep a respectful distance. They're wild animals, just very accustomed to people." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Final Wandering & Departure", description: "If you have time before your departure, revisit Pier 2 for any shops or galleries you missed, or simply sit at a waterfront café and soak in Kaohsiung's harbor energy one last time. The city rewards slow, quiet moments. Pick up pineapple cakes or sun cakes from a bakery as souvenirs.", details: ["📍 THSR Zuoying Station (Red Line north terminus) for high-speed rail, or Kaohsiung International Airport (Red Line south) for flights"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Duck Meat Rice at a Local Shop", description: "For your last Kaohsiung meal, find a duck rice (鴨肉飯) shop — a southern Taiwan specialty. Tender sliced duck over rice with a side of blanched vegetables and a bowl of clear soup. Simple, comforting, and uniquely Kaohsiung. Many shops are near the Yancheng area.", meta: "NT$80-120 · Yancheng area · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Kaohsiung International Airport is on the Red MRT Line — only 15 minutes from city center. THSR to Taipei takes 90 minutes from Zuoying Station. Allow 30 min to get to either from the Pier 2 area." }]
        }
      ]
    }
  ]
};

// Run fulfillment
(async () => {
  try {
    const result = fulfillOrder(order, itineraryData);
    console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('❌ Fulfillment failed:', err.message);
    process.exit(1);
  }
})();
