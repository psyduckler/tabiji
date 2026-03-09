const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1773032068878_y7gz3o",
  email: "c13.bako@gmail.com",
  destination: "Tbilisi, Georgia",
  start_date: "2026-03-27",
  end_date: "2026-04-03",
  group_size: "1",
  travel_style: "Adventure, Cultural, Foodie",
  dining: "Mix of everything",
  budget: "Under $1,000",
  requests: "",
  amount: "0.00",
  timestamp: "2026-03-09T04:54:28.878Z",
  status: "pending"
};

const itineraryData = {
  destination: "Tbilisi, Georgia",
  countryEmoji: "🇬🇪",
  title: "Tbilisi in 8 Days: Sulfur Baths, Ancient Fortresses & Georgian Wine",
  subtitle: "Old Town · Narikala · Mtskheta · Kazbegi · Kakheti",
  description: "Eight days in one of the Caucasus' most captivating cities — where medieval churches share cobblestone alleys with natural wine bars, steaming sulfur baths bubble beneath fairy-tale balconies, and snow-capped mountains loom just hours away. Tbilisi for solo adventurers is pure magic: the city is absurdly affordable, effortlessly walkable, and utterly alive with culture, food, and warm Georgian hospitality (known as 'tamada' spirit). Spring means mild weather, blossoming apricot trees, and the Caucasus' dramatic landscapes at their most photogenic.",
  duration: "7 nights / 8 days",
  dates: "March 27 – April 3, 2026",
  budget: "Budget-Friendly (Under $1,000 total)",
  pace: "Active — early mornings, big day trips, late Georgian feasts",
  bestFor: "Solo adventurers, foodies, culture seekers & natural wine lovers",
  highlights: [
    "Abanotubani — Tbilisi's legendary sulfur bath district, soaking in thermal waters under domed rooftops",
    "Narikala Fortress — 4th-century hilltop ruins with sweeping panoramas over the Old Town",
    "Mtskheta day trip — ancient Georgian capital with UNESCO World Heritage churches",
    "Kazbegi adventure — the iconic Gergeti Trinity Church perched at 2,170m above the Caucasus",
    "Sighnaghi & Kakheti wine country — the cradle of wine, 8,000-year-old tradition",
    "Fabrika — a Soviet-era factory reborn as Tbilisi's hippest creative hub",
    "Georgian feast (supra) — khinkali dumplings, churchkhela, mtsvadi, and endless natural wine",
    "Dry Bridge Flea Market — Tbilisi's open-air treasure trove of Soviet antiques and local crafts",
    "Shardeni Street — intimate wine bars and candlelit restaurants in the Old Town",
    "Mtkvari River walks — the city from both banks at golden hour"
  ],
  essentials: [
    { title: "✈️ Getting There & Around", text: "Tbilisi International Airport (TBS) is 18km from the center. Take the metro (Line 2, Isani station) for ₾1 (~$0.37), or grab a Bolt/Yango taxi for ~₾25-30 (~$9-11). The city is walkable for the Old Town, Rustaveli, and Fabrika areas. For Mtskheta and Kakheti, use shared marshrutkas (minibuses) from Didube or Samgori bus stations — cheap, reliable, and the local way. For Kazbegi, book a shared jeep tour (~$25-30pp) or marshrutka from Didube station (~₾15)." },
    { title: "💵 Budget Reality", text: "Georgia is incredibly affordable. Guesthouses and boutique hostels: $15-40/night. Georgian meals: $5-10 for a full feast at local spots, $15-25 at nicer restaurants. Natural wine bars: $2-4 per glass. Beer: $1-2. Daily budget including accommodation, 3 meals, wine, and activities: $50-80/day easily. Total 8-day trip: $400-640 including everything — well under $1,000 even with day trips." },
    { title: "🌸 March/April Weather", text: "Late March / early April is ideal for Tbilisi. Expect 12-18°C (54-65°F) during the day, dropping to 5-10°C at night. Spring blooms are arriving — apricot and cherry trees blossom around the city. The Caucasus mountains are still snow-capped. Occasional rain is possible; pack a light rain jacket. The mountains (Kazbegi) will be colder — bring warm layers for that day trip." },
    { title: "🏨 Where to Stay", text: "Old Town (Kala) — best location for first-timers; cobblestones, sulfur baths, Narikala right outside your door. Stay on or just off Shardeni Street for the full atmosphere. Budget picks: Fabrika Hostel ($15-20/night for private room, excellent social scene). Mid-range boutique: Old Town guesthouses ($35-55/night) on Bambi Street or Tabukashvili. Book ahead for spring — Tbilisi tourism peaks from April onward." },
    { title: "🍷 Georgian Wine & Food Culture", text: "Georgia invented wine — 8,000 years of winemaking in clay qvevri vessels buried in the earth. Amber/orange wines (skin-contact whites) are the specialty. Don't miss: Rkatsiteli (white), Saperavi (red), Chinuri. Natural wine bars cluster on Shardeni Street and in Fabrika. Must-eat: khinkali (soup dumplings — never cut them, bite and slurp), khachapuri (cheese bread, especially Adjarian boat-shaped version), badrijani nigvzit (eggplant with walnut), mtsvadi (grilled skewers). A full Georgian supra (feast) with endless small plates and flowing wine for $10-15pp." },
    { title: "🗣️ Language & Tips", text: "Georgian script (mkhedruli) looks completely unique — you won't recognize a single letter. But English is widely spoken in tourist areas, hotels, and restaurants. Google Translate's camera mode is invaluable for menus and street signs. GEL (Georgian Lari) is the currency; ₾1 ≈ $0.37 USD. Tbilisipass for free/discounted museum entry ($15 for 3 days) is worth it. Tipping: 10% at restaurants is appreciated but not obligatory." },
    { title: "📱 Apps & Getting Connected", text: "Bolt and Yango for taxis (much cheaper and safer than hailing on street). Google Maps works well for navigating Tbilisi. Get a Georgian SIM at the airport (Magti or Geocell, ~$5 for a week of data). Download offline maps for Kazbegi — cell signal up the mountain is spotty. Currency exchange: use exchange kiosks in the city (much better rates than airport), or ATMs with your travel card (Wise/Revolut)." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival, Old Town & First Sulfur Bath",
      neighborhoods: "Old Town (Kala) · Abanotubani · Rustaveli",
      date: "March 27",
      mapPins: [
        { lat: 41.6939, lng: 44.8017, label: "Freedom Square", num: 1, cat: "activity", desc: "Central landmark & orientation point" },
        { lat: 41.6924, lng: 44.8072, label: "Sioni Cathedral", num: 2, cat: "activity", desc: "6th-century mother church of Tbilisi" },
        { lat: 41.6930, lng: 44.8058, label: "Anchiskhati Basilica", num: 3, cat: "activity", desc: "Tbilisi's oldest surviving church, 6th century" },
        { lat: 41.6927, lng: 44.8063, label: "Shardeni Street", num: 4, cat: "food", desc: "Cobblestone alley of wine bars & restaurants" },
        { lat: 41.6853, lng: 44.8104, label: "Abanotubani (Sulfur Baths)", num: 5, cat: "activity", desc: "Famous domed sulfur bath district" },
        { lat: 41.6898, lng: 44.8112, label: "Metekhi Church", num: 6, cat: "activity", desc: "13th-century church on a cliff above the river" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            { title: "Arrive & Settle In", description: "Land at Tbilisi International Airport and take the metro or Bolt taxi to the Old Town. Drop your bags, breathe in the jasmine-scented spring air, and prepare to fall in love with this city. Check in to your guesthouse on or near Shardeni Street — you want to be in the heart of the Old Town from day one.", details: ["🚇 Metro from airport: Line 2 to Isani, then walk (15 min). ₾1 flat fare — buy a Metromoney card at the airport station.", "🚗 Bolt taxi from airport: ~₾25-30 ($9-11). Reliable and metered.", "💡 If you arrive early afternoon, drop bags and start exploring immediately — Tbilisi's Old Town rewards unhurried wandering."] },
            { title: "Old Town First Wander", description: "Lose yourself in the Old Town. Start at Freedom Square and walk south down Kote Afkhazi Street toward the river. The Old Town is a dizzying mix of ancient churches, crumbling balconied homes draped in wisteria, Persian-style archways, and hip wine bars wedged between medieval walls. Every alley reveals something unexpected.", details: ["📍 Start at Freedom Square and walk south-southeast toward the Mtkvari River.", "💡 Look up constantly — the wooden carved balconies (archways with flower carvings) are Tbilisi's architectural signature. Many are hundreds of years old.", "💡 Anchiskhati Basilica (6th century) is the oldest church in Tbilisi — the dark interior with flickering candles is deeply atmospheric."] }
          ],
          meals: [
            { type: "🍽️ Late Lunch / First Georgian Meal", name: "Shavi Lomi", description: "Your first khinkali at a legendary local spot. Order a round of the classic meat soup dumplings and figure out the technique: hold the knob, bite the side, drink the soup inside, then eat down — never cut them! The walnut-stuffed eggplant (badrijani nigvzit) and mushroom khinkali are exceptional. Cheap, loud, and absolutely Georgian.", meta: "₾20-30pp ($7-11) · 8 Mingreli St · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Khinkali eating technique: hold by the doughy knob (the 'kudi'), bite a small hole in the side, drink the soup broth inside, then eat the rest. The knob is left on the plate — counting how many you eat. Never use a fork. This is the rule." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Abanotubani Sulfur Bath District", description: "Welcome yourself to Tbilisi the right way: with a sulfur bath. The domed bathhouses of Abanotubani have been the city's communal ritual since the 4th century — Alexander Dumas called it 'the best bath in my life.' Book a private room (₾50-100/hour for 2-4 people, so solo it's just you) and soak in the naturally hot sulfurous waters that smell faintly of eggs. The water is said to cure everything. You'll emerge feeling absolutely reborn.", details: ["📍 The main bath district is below Narikala Fortress on the right bank of the Baratashvili Bridge.", "💡 Recommended: Chreli Abano or Sulphur Baths No. 5. Private rooms with natural stone pools run ₾50-80/hour solo. Book ahead or walk in on weekday afternoons.", "💡 The sulfur smell is intense at first but you stop noticing it. The water is genuinely hot (~37-42°C) and silky-soft. Bring a bathing suit and a towel (or rent for ₾5)."] },
            { title: "Metekhi Church at Sunset", description: "After your bath, cross the Metekhi Bridge and look back at the city. The view of Narikala Fortress lit up above the Old Town, the river glinting below, and Metekhi Church perched on its rocky spur is one of the most beautiful urban panoramas in the Caucasus. The equestrian statue of King Vakhtang Gorgasali (Tbilisi's founder) stands guard against the golden sky.", details: ["📍 Metekhi Bridge, right bank of Mtkvari River", "💡 Best photo angle: stand on the Metekhi Bridge and face west for the Narikala/Old Town vista."] }
          ],
          meals: [
            { type: "🍷 Dinner", name: "Azarpesha Wine Bar", description: "A candlelit wine bar tucked into a Shardeni Street alley. The focus is Georgian natural wine — amber/orange skin-contact whites, funky Saperavi reds, skin-contact Rkatsiteli. The owner will walk you through a tasting. Pair with cheese boards and local cold cuts. This is why people come to Tbilisi.", meta: "₾30-50pp ($11-18) · Shardeni St area · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "The sulfur baths are a Tbilisi must. Yes, they smell like eggs. Yes, it's incredible. Go private — ₾80 for an hour solo sounds like a lot but it's $29. You'll have a stone-tiled room with a thermal pool entirely to yourself. Life-changing nap afterwards.", cite: "r/solotravel" }]
        }
      ]
    },
    {
      num: 2,
      title: "Narikala Fortress, Cable Car & Old Town Deep Dive",
      neighborhoods: "Old Town · Narikala · Rike Park · Sameba",
      date: "March 28",
      mapPins: [
        { lat: 41.6885, lng: 44.8097, label: "Narikala Fortress", num: 1, cat: "activity", desc: "4th-century fortress with panoramic city views" },
        { lat: 41.6892, lng: 44.8035, label: "Rike Park Cable Car Station", num: 2, cat: "activity", desc: "Cable car up to Narikala — incredible views" },
        { lat: 41.7024, lng: 44.8095, label: "Sameba Cathedral", num: 3, cat: "activity", desc: "Georgia's largest cathedral, completed 2004" },
        { lat: 41.6940, lng: 44.7880, label: "Fabrika", num: 4, cat: "activity", desc: "Soviet-era sewing factory turned creative hub" },
        { lat: 41.6951, lng: 44.7987, label: "Dry Bridge Flea Market", num: 5, cat: "activity", desc: "Open-air antiques market — Soviet treasures" },
        { lat: 41.6957, lng: 44.7981, label: "National Museum of Georgia", num: 6, cat: "activity", desc: "Georgian gold treasury & ancient artifacts" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Cable Car to Narikala Fortress", description: "Take the cable car from Rike Park (near the river, free/₾1 token) up to Narikala Fortress — a 4th-century fortification expanded by Arab invaders and Mongols. The fortress ruins are dramatic: crumbling walls, hidden gardens, and views that stretch across the entire city. On a clear March morning, you can see the snow-capped Caucasus above the Tbilisi skyline.", details: ["📍 Cable car departs from Rike Park, river level. Runs daily 10am-10pm. ₾2.50 roundtrip.", "💡 Walk the fortress walls early (before 10am) for crowds-free exploration. The upper terrace has 360° views: Old Town, the river, Sameba Cathedral, and the Caucasus mountains.", "⚠️ Some fortress sections are unstable — stay on marked paths and be careful near edge walls."] },
            { title: "St. Nicholas Church & Botanical Garden", description: "Below Narikala, a small church rebuilt in 1996 glows white against the ancient walls. From there, wind down through the Upper Botanical Garden — 128 hectares of greenery in a hidden gorge. In late March, the first spring flowers are blooming: snowdrops, early crocuses, blossoming trees.", details: ["📍 Tbilisi Botanical Garden entrance is ₾3. Open 10am-8pm.", "💡 The garden's waterfall trail leads to a hidden canyon — easy 30-minute walk, completely different world from the city above."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Fabrika Courtyard Cafés", description: "Head to Fabrika for breakfast in the most interesting courtyard in Tbilisi. A dozen cafés and eateries ring the old factory space — grab fresh-baked Georgian bread (puri) with butter and honey at the simple stalls, or a specialty coffee at one of the hipster cafés. This is where Tbilisi's creative class starts their mornings.", meta: "₾8-15pp ($3-5) · 8 Ninoshvili St · Opens 9am" }
          ],
          tips: [{ type: "tip", text: "Narikala is free to enter. The cable car is ₾2.50 roundtrip — take it up, walk down through the Old Town for a better experience of the descent through the Kala neighborhood."}]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Dry Bridge Flea Market", description: "One of the most fascinating markets in the Caucasus: hundreds of vendors sprawl under the Dry Bridge, selling Soviet-era medals, Georgian Orthodox icons, antique samovars, old cameras, handmade silver jewelry, and dusty oil paintings. Sunday is the biggest day but it runs daily. Bring ₾50 cash and be prepared to spend it.", details: ["📍 Baratashvili Bridge, right bank. Open daily from ~10am, peaks on weekends.", "💡 Bargaining is expected — start at 50-60% of asking price and meet in the middle. Vendors are friendly and the vibe is relaxed."] },
            { title: "Sameba Cathedral", description: "A 20-minute walk up to Sameba Cathedral (Holy Trinity) — Georgia's largest church, completed in 2004 but built in the Byzantine style with spectacular frescoes, gilded iconostasis, and a sense of soaring grandeur. Surprisingly moving for a modern building. The cathedral complex has gardens and views toward the old town.", details: ["📍 Avlabari district. Free entry. Modest dress required (scarves available at door for women).", "💡 Attend if there's a choral service — Georgian Orthodox polyphonic chanting is UNESCO-listed and genuinely otherworldly."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Samikitno (Organique)", description: "Classic Georgian restaurant near the National Museum with excellent value. The Adjarian khachapuri here (boat-shaped bread filled with melted cheese, a raw egg yolk and butter) is the standard against which all others are measured. Order it and nothing else — stir the yolk into the cheese and tear the bread sides to dip.", meta: "₾15-25pp ($5-9) · 26 Rustaveli Ave · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Adjarian khachapuri is the iconic one — the boat with the egg. But honestly every region has its own version. Imeruli is the round stuffed bread; megruli has cheese inside AND on top. Try all of them. You cannot overeat khachapuri in Georgia, it is physically impossible.", cite: "r/georgia" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "National Museum of Georgia", description: "If it's open late, the National Museum on Rustaveli is essential for context. The Gold Treasury (requires guided tour, ₾15 extra) has 5,000-year-old gold jewelry, Achaemenid-era artifacts, and the famous Kolkhian Gold — stunning even for non-museum people.", details: ["📍 3 Shota Rustaveli Ave · ₾15 entry · Open Tue-Sun 10am-6pm", "💡 The National Treasury on the top floor has the most impressive pieces. Book the guided tour — otherwise the context is lost."] }
          ],
          meals: [
            { type: "🍷 Dinner", name: "Vino Underground", description: "Tbilisi's most famous natural wine bar — a basement cave below the Old Town that hosts Georgia's natural winemakers. The list changes constantly; the staff are evangelical about their wines and will guide you expertly. Cheese, meats, and simple Georgian plates. This is where you'll spend three hours when you planned for one.", meta: "₾40-60pp ($15-22) · 14 Galaktion Tabidze St · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Vino Underground is a pilgrimage spot for natural wine lovers. Come with an open mind about amber wines — they're tannic, complex, and made in clay vessels buried in the earth. The owner has personally tasted every bottle. Ask for the 'unexpected orange' flight.", cite: "r/wine" }]
        }
      ]
    },
    {
      num: 3,
      title: "Mtskheta Day Trip — Georgia's Ancient Soul",
      neighborhoods: "Mtskheta · Jvari · Svetitskhoveli",
      date: "March 29",
      mapPins: [
        { lat: 41.8442, lng: 44.7278, label: "Jvari Monastery", num: 1, cat: "activity", desc: "6th-century hilltop monastery — 2 rivers converge below" },
        { lat: 41.8428, lng: 44.7185, label: "Svetitskhoveli Cathedral", num: 2, cat: "activity", desc: "UNESCO — Georgia's spiritual heart since 4th century" },
        { lat: 41.8441, lng: 44.7214, label: "Mtskheta Old Town", num: 3, cat: "activity", desc: "Ancient capital's charming streets & wine shops" },
        { lat: 41.8390, lng: 44.7153, label: "Samtavro Church", num: 4, cat: "activity", desc: "4th-century church where Queen Nino converted Georgia" },
        { lat: 41.7009, lng: 44.7928, label: "Didube Bus Station (Tbilisi)", num: 5, cat: "activity", desc: "Marshrutka to Mtskheta departs here — ₾1" },
        { lat: 41.6945, lng: 44.7998, label: "Rustaveli Avenue", num: 6, cat: "activity", desc: "Return to Tbilisi's main boulevard" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Marshrutka to Mtskheta", description: "Catch a marshrutka (shared minibus) from Didube station in Tbilisi to Mtskheta — the ancient capital of Georgia, only 20km north of Tbilisi but a world apart. The ride takes 20-30 minutes and costs ₾1. Mtskheta is where Christianity came to Georgia in 327 AD, and the entire town is UNESCO World Heritage listed. On a clear spring morning, with the mountains rising behind the cathedral spires, it feels like stepping into the Old Testament.", details: ["🚌 Marshrutka: Tbilisi Metro Line 1, Didube station. Find the marshrutkas labeled 'Mtskheta' in the lot. Departs when full, runs every 15-20 min from 8am. ₾1 cash.", "💡 Go on a weekday to avoid weekend crowds. Early morning is best for photos — the Jvari light is golden before 10am."] },
            { title: "Jvari Monastery", description: "Taxi from Mtskheta town up the dramatic hill to Jvari Monastery (₾5-8 for the taxi). Built in the 6th century at the exact spot where St. Nino planted a cross to convert Georgia, Jvari sits at the confluence of the Mtkvari and Aragvi rivers. The view of the two rivers meeting below, with Mtskheta's rooftops and the Caucasus beyond, is the image that defines Georgia. Lermontov wrote his famous poem 'Mtsyri' about this exact view.", details: ["📍 Hilltop above Mtskheta, 2km drive. Taxi up ₾5-8; walk down (steep, 30-40 min).", "💡 The monastery interior has remarkable early frescoes and a simply carved stone iconostasis. The cross at the center (a replica of St. Nino's) is Georgia's most sacred object."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Home-style in Tbilisi Before Departing", description: "Grab a quick breakfast at your guesthouse or grab a fresh Georgian bread (puri) and churchkhela (walnut-stuffed grape candy) from a street vendor near Didube station. You'll eat a big lunch in Mtskheta.", meta: "₾5-8 ($2-3)" }
          ],
          tips: [{ type: "tip", text: "Walk DOWN from Jvari to Mtskheta town — the path descends through vineyards and orchards, takes about 40 minutes, and gives you the best views of the river confluence. Much better than another taxi ride." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Svetitskhoveli Cathedral", description: "The Cathedral of the Living Pillar — Georgia's spiritual heart since the 4th century. A UNESCO site and the second-largest cathedral in the Caucasus. The name refers to a legendary cedar pillar that miraculously descended from the sky; it's buried beneath the cathedral floor, said to flow with miraculous ointment. The 11th-century cathedral has extraordinary scale and beautiful frescoes. This is where Georgian kings were crowned and buried for 15 centuries.", details: ["📍 Center of Mtskheta old town. Free entry. ₾5 with audio guide (recommended).", "💡 Look for the small chapel replica of the Holy Sepulchre inside — brought to Georgia in the 5th century. The entire complex is full of extraordinary detail."] },
            { title: "Samtavro Church & Mtskheta Wander", description: "Walk 15 minutes to Samtavro Church (4th century) — allegedly built over the hut where St. Nino lived when she converted the Georgians. The site contains the tombs of Georgia's first Christian king and queen. The adjacent nunnery is still active — you may see nuns in black going about their day. Atmospheric, intimate, and deeply moving.", details: ["📍 North end of Mtskheta, 10-min walk from Svetitskhoveli", "💡 The frescoes inside Samtavro are among the oldest surviving Georgian church paintings — heavily damaged but haunting in their faded glory."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Mtskheta's Local Restaurants", description: "Mtskheta's main street has excellent tourist restaurants with panoramic patios. Order the local specialty: grilled trout from the nearby rivers, mtsvadi (pork skewers), and fresh salads with walnuts. Everything is cheaper than Tbilisi. Sit on a terrace with a glass of local wine and the cathedral towers visible above the rooftops.", meta: "₾20-35pp ($7-13) · Main street restaurants · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Mtskheta is a 30-minute marshrutka ride for ₾1 and people often skip it because 'it's just a church'. Those people are wrong. This is where Georgia became Georgia. Standing at Jvari looking down at the rivers and then walking through Svetitskhoveli puts everything else in context.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Return to Tbilisi & Mtatsminda Evening", description: "Marshrutka back to Tbilisi by late afternoon. If you have energy, take the funicular up Mtatsminda Mountain for sunset views over the whole city. The panorama from the top extends across Tbilisi's terracotta rooftops to the Caucasus foothills. The funicular station is on Chonkadze Street.", details: ["🎡 Funicular: Chonkadze St station. ₾2.50 roundtrip. Runs 11am-11pm.", "📸 Sunset from Mtatsminda with the city spread below is one of the best views in the Caucasus."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Poliphonia", description: "A small, intimate Old Town restaurant with an excellent Georgian-European menu. The khinkali with cheese and herbs are outstanding, as is the roasted lamb with tkemali (sour plum sauce). Great natural wine list. Candles everywhere, the walls close in warmly — perfect after a day in ancient churches.", meta: "₾40-55pp ($15-20) · Old Town · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Modern Tbilisi: Fabrika, Street Art & Tbilisi Sea",
      neighborhoods: "Fabrika · Marjanishvili · Vake · Avlabari",
      date: "March 30",
      mapPins: [
        { lat: 41.6940, lng: 44.7880, label: "Fabrika", num: 1, cat: "activity", desc: "Soviet sewing factory — now Tbilisi's coolest hub" },
        { lat: 41.6938, lng: 44.7869, label: "Marjanishvili Square", num: 2, cat: "activity", desc: "Neighborhood square with local cafés & bars" },
        { lat: 41.7070, lng: 44.7800, label: "Vake Park", num: 3, cat: "activity", desc: "Tbilisi's Central Park — Georgian families, tennis, cafés" },
        { lat: 41.7476, lng: 44.8892, label: "Tbilisi Sea (Tbilisi Reservoir)", num: 4, cat: "activity", desc: "Artificial lake with mountain views — local escape" },
        { lat: 41.7009, lng: 44.7928, label: "Dezerter Bazaar", num: 5, cat: "food", desc: "Tbilisi's main food market — chaotic and wonderful" },
        { lat: 41.6945, lng: 44.8011, label: "Rustaveli Avenue", num: 6, cat: "activity", desc: "Grand boulevard — opera house, galleries, parks" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Dezerter Bazaar", description: "Start the day at Dezerter Bazaar — Tbilisi's sprawling central food market, chaotic, colorful, and completely alive. Vendors sell cones of spices, braids of churchkhela (walnut-stuffed grape-juice candy), 100 varieties of cheese, freshly baked Georgian breads still warm from the tone oven, dried fruits, and seasonal produce. Walk every aisle, try everything offered, buy churchkhela for the week. This is where Tbilisi cooks shop.", details: ["📍 Near Tbilisi Central Railway Station, Avlabari metro stop", "💡 Get there before 10am for peak produce activity. Bring cash ₾30-50 for snacks and provisions.", "💡 Look for churchkhela — walnut strings dipped in grape juice concentrate, dried in the sun. The best souvenir and an excellent trail snack. ₾2-3 for a large string."] },
            { title: "Rustaveli Avenue Walk", description: "Walk the full length of Rustaveli Avenue — Tbilisi's grand 19th-century boulevard named after the national poet. Pass the National Opera House (beautiful restored neoclassical), the Parliament building, the Kashveti Church, and a string of bookshops and galleries. The street feels European and distinctly Georgian simultaneously.", details: ["📍 Runs from Freedom Square to Marjanishvili, about 1.5km", "💡 The Rustaveli Theatre is one of the most celebrated theatrical companies in the former Soviet Union. Check their schedule — a performance (even without Georgian language) can be extraordinary."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Stamba Hotel Coffee", description: "The Stamba Hotel in Fabrika/Vera is Tbilisi's best design hotel and its ground-floor café is a local favorite. Industrial chic, great espresso, and excellent pastries. Even if you're not staying here, it's worth coming for the coffee and the gorgeous restored typography workshop space.", meta: "₾10-18pp ($4-6) · 14 Merab Kostava St" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Fabrika Deep Dive", description: "Spend a proper afternoon at Fabrika — a 1930s Soviet sewing factory with 19 shipping containers converted into bars, cafés, artisan shops, a surf shop (!), a hostel, a yoga studio, and a barber. The courtyard has outdoor ping pong, street art, dogs lounging everywhere, and a genuinely cool crowd from 20 nationalities. This is Tbilisi's creative soul.", details: ["📍 8 Ninoshvili St · Free entry · Open all day, peaks 2pm-midnight", "💡 The hostel upstairs has a great communal vibe — even non-guests can grab a drink at the rooftop bar with city views.", "💡 Check the events board — there are often free concerts, art openings, or market days in the courtyard."] },
            { title: "Vake Park & Sunday Stroll", description: "Walk uphill to Vake Park — Tbilisi's Central Park equivalent. Georgian families play chess in the sun, vendors sell fried fish (a Sunday tradition), couples walk the tree-lined alleys, and the city spreads below. The 'Eternal Flame' monument to WWII soldiers stands at the main entrance. Peaceful, local, and lovely.", details: ["📍 Vake district, accessible by marshrutka from Freedom Square", "💡 Vake's residential streets behind the park have some of Tbilisi's best restaurants — quieter and more local than Old Town."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Mapshalia", description: "A tiny restaurant in Fabrika courtyard serving Svan cuisine — from the Svaneti mountain region. The Svan salt (a spice blend with chili, garlic, fenugreek, marigold) flavors everything. The kubdari (Svan meat pie) is outstanding — denser and spicier than regular Georgian bread. Unusual and excellent.", meta: "₾20-30pp ($7-11) · Fabrika courtyard · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Fabrika gets dismissed as 'too touristy' by some people. They're wrong. It's tourist-friendly, yes, but the shops are genuinely local, the bars are cheap, and you'll meet more interesting people in one afternoon there than a week of only doing the traditional tourist route.", cite: "r/tbilisi" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset Walk: River & Avlabari", description: "Catch the sunset from the Baratashvili Bridge — arguably Tbilisi's best view. The Old Town with its wooden balconies and Narikala Fortress stacked above, the bridge lit in evening gold, the river below. Then cross to Avlabari for a walk through the Armenian quarter, with its small churches and neighborhood cafés.", details: ["💡 The Metekhi Bridge has the more iconic angle for photos; Baratashvili Bridge has the better 'city feeling.'"] }
          ],
          meals: [
            { type: "🍷 Dinner", name: "Wine Factory No. 1", description: "A massive restored wine factory turned restaurant-bar complex near the city center. The space is stunning — industrial architecture, wine tanks turned into private dining rooms, vaulted brick ceilings. The food is excellent modern Georgian, and the wine selection (Kakhetian qvevri wines mostly) is vast. A great place to try multiple wines by the glass.", meta: "₾45-65pp ($16-24) · 1 Akhvlediani St · Reservations for dinner" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Georgian Food Deep Dive & Peaceful Old Town",
      neighborhoods: "Old Town · Shardeni · Kala",
      date: "March 31",
      mapPins: [
        { lat: 41.6920, lng: 44.8068, label: "Sioni Cathedral", num: 1, cat: "activity", desc: "Morning service in Tbilisi's oldest cathedral" },
        { lat: 41.6927, lng: 44.8063, label: "Shardeni Wine Street", num: 2, cat: "food", desc: "Old Town's wine bar and restaurant strip" },
        { lat: 41.6936, lng: 44.8050, label: "Georgian Cooking Class", num: 3, cat: "food", desc: "Learn to make khinkali & khachapuri" },
        { lat: 41.6906, lng: 44.7987, label: "Gabriadze Theatre & Clock Tower", num: 4, cat: "activity", desc: "Quirky marionette theatre with famous animated clock" },
        { lat: 41.6892, lng: 44.8035, label: "Rike Park", num: 5, cat: "activity", desc: "Riverside park with amphitheatre & cable car base" },
        { lat: 41.6930, lng: 44.8058, label: "Anchiskhati Basilica", num: 6, cat: "activity", desc: "6th-century church with polyphonic chanting on Sundays" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Morning in Kala (Old Town)", description: "Take a slow morning to explore the oldest part of the Old Town — the Kala neighborhood. Wind through the tiny alleys behind Sioni Cathedral, where old ladies sell flowers and herbs, cats nap on ancient walls, and children play in courtyards visible through iron gates. The morning light through Tbilisi's famous balconies is extraordinary. This is the real neighborhood life of the city.", details: ["💡 The area between Sioni Cathedral and the Anchiskhati Basilica is the most atmospheric part of the Old Town — residential, non-touristy, and beautiful.", "💡 Visit Anchiskhati Basilica (Tbilisi's oldest church) early — if you're lucky, you'll hear the Georgian Orthodox liturgy sung in polyphonic harmony. Chills."] },
            { title: "Gabriadze Theatre & Clock Tower", description: "Walk to the Gabriadze Puppet Theatre — a whimsical building topped by a clock tower that comes alive every hour: a tiny angel emerges, rings the bell, and returns. The theatre itself stages extraordinary marionette productions (book ahead if you want to catch a show in the evening). Even the café attached has a magical fairy-tale atmosphere.", details: ["📍 13 Shavteli St · Clock tower strikes every hour with mechanical theater", "💡 The Gabriadze marionette shows are beloved — the evening shows sell out. Book at gabriadzetheatre.com if interested."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Paul's Coffee House (Shardeni)", description: "A cozy café on Shardeni Street with excellent Georgian coffee (filter and espresso) and fresh pastries. The tables spill onto the cobblestones. The ideal spot for a slow morning with a book before a cooking lesson.", meta: "₾8-15pp ($3-5) · Shardeni St · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Georgian Cooking Class", description: "Join a hands-on Georgian cooking class — a highlight of any Tbilisi stay. You'll learn to make khinkali from scratch (the dough, the folding technique, the precise amount of broth trapped inside) and Imeruli khachapuri. Most classes include a Georgian supra feast at the end with natural wine. Cooking with locals and eating what you made is an irreplaceable cultural experience.", details: ["📍 Multiple operators: Caucasian Cooking Class (₾80pp), My Georgian Kitchen (₾90pp) — most include 3-hour class + meal + wine.", "💡 Book 2-3 days ahead online. Groups are small (4-8 people) — a great way to meet other travelers.", "💡 The khinkali folding is genuinely hard — 19 folds is the traditional target. Most tourists manage 12. The dumplings taste great regardless."] }
          ],
          meals: [
            { type: "🍽️ Lunch (in class)", name: "Your Own Georgian Feast", description: "The cooking class lunch IS the meal — you'll eat what you made: fresh khinkali, khachapuri, badrijani nigvzit (walnut eggplant rolls), Georgian salad, and as much natural wine as you can manage on an afternoon. The communal table with new friends is one of the best parts of solo travel.", meta: "₾80-90pp ($29-33) including class + feast" }
          ],
          tips: [{ type: "reddit", text: "Do a cooking class in Tbilisi. I know it sounds touristy. But folding your own khinkali and then eating them with qvevri wine while a Georgian grandmother corrects your technique is genuinely one of the best travel experiences I've had. And you actually learn something useful.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Rike Park & Night Walk", description: "Rest in Rike Park — a riverside green space with an open-air amphitheatre and great people-watching. As the sun sets, Tbilisi comes alive: groups gather on the riverbank, music drifts from open restaurants, the bridges light up. Take the evening to wander without a plan — Tbilisi at night is safe and vibrant for solo travelers.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Barbarestan", description: "One of the most beloved restaurants in Tbilisi — recipes from a 19th-century Georgian cookbook, executed with modern precision. The menu changes seasonally; the walnut dishes, the Kakhuri roast, and the pomegranate-dressed salads are exceptional. Booked out constantly for a reason. Reserve well ahead.", meta: "₾60-80pp ($22-29) · 132 Davit Aghmashenebeli Ave · Reservations essential" }
          ],
          tips: [{ type: "tip", text: "Barbarestan takes reservations very seriously — they'll give your table away after 15 minutes. Be on time or call ahead. But if it's full, Cafe Littera (in a beautiful garden) or Keto & Kote (near Old Town) are excellent alternatives."}]
        }
      ]
    },
    {
      num: 6,
      title: "Kazbegi Adventure — Gergeti Trinity Church",
      neighborhoods: "Kazbegi (Stepantsminda) · Georgian Military Highway",
      date: "April 1",
      mapPins: [
        { lat: 41.7009, lng: 44.7928, label: "Didube Bus Station (Tbilisi)", num: 1, cat: "activity", desc: "Depart: marshrutka to Kazbegi, 3hrs, ₾15" },
        { lat: 42.5040, lng: 44.4720, label: "Gudauri Viewpoint", num: 2, cat: "activity", desc: "Hairpin turns & mountain views — halfway point" },
        { lat: 42.5285, lng: 44.4867, label: "Zhinvali Reservoir", num: 3, cat: "activity", desc: "Turquoise reservoir visible from the highway" },
        { lat: 42.6587, lng: 44.6363, label: "Stepantsminda (Kazbegi Town)", num: 4, cat: "activity", desc: "Base village — local guesthouses, mountain air" },
        { lat: 42.6629, lng: 44.6378, label: "Gergeti Trinity Church", num: 5, cat: "activity", desc: "14th-century church perched at 2,170m — icon of Georgia" },
        { lat: 42.6622, lng: 44.6335, label: "Kazbek Mountain Viewpoint", num: 6, cat: "activity", desc: "5,047m peak looming above the church" }
      ],
      timeBlocks: [
        {
          label: "Early Morning (Departure)",
          activities: [
            { title: "Marshrutka to Kazbegi", description: "Wake up early and get to Didube bus station by 7:30-8am. Catch the marshrutka to Kazbegi/Stepantsminda — a 3-hour journey through the Georgian Military Highway, one of the most dramatic roads in the Caucasus. The route ascends through the Greater Caucasus mountains, past the turquoise Zhinvali Reservoir, through the Cross Pass at 2,395m, and emerges in the valley below Mt. Kazbek (5,047m). Every turn is more spectacular than the last.", details: ["🚌 Marshrutka from Didube to Stepantsminda: ₾15, departs when full from 8am onward. Journey ~3 hours.", "💡 Sit on the RIGHT side of the marshrutka going north — you'll get the better mountain views.", "💡 Bring warm layers even in April — Kazbegi is significantly colder than Tbilisi (often 0-8°C). Snow is common."] }
          ],
          meals: [
            { type: "☕ Pre-dawn Snack", name: "Grab Provisions at a Tbilisi Deli/Market", description: "Pick up Georgian bread, churchkhela, and a bottle of water before departing. The journey has no reliable stops. Eat your breakfast in the marshrutka while watching the mountains grow.", meta: "₾5-8 ($2-3)" }
          ],
          tips: []
        },
        {
          label: "Full Day in Kazbegi",
          activities: [
            { title: "Gergeti Trinity Church Hike", description: "The crown jewel of Georgia: Gergeti Trinity Church (Tsminda Sameba) perched on a rocky spur at 2,170m, with the ice-capped 5,047m Mt. Kazbek directly behind it. The hike up from Stepantsminda village is 2-3 hours roundtrip (6km, 1,000m elevation gain). The trail winds through shepherd pastures and forests. On a clear April day, the views are apocalyptically beautiful: the church spire against the white Caucasus summit, the valley falling away below.", details: ["⛰️ Hike: ~3km each way, +1,000m elevation. Moderate difficulty — fit hikers do it in 1.5 hours up, 1 hour down.", "💡 Start early (10am) to get the morning light and beat any afternoon clouds. The mountain often clouds over by 2-3pm.", "🚗 Alternatively, hire a 4WD taxi from Stepantsminda (₾30-40 roundtrip) for the drive if conditions are snowy. The road is rough but passable April onward.", "⚠️ Cold, wind, and possible snow even in April. Bring warm layers, waterproof jacket, and good footwear."] },
            { title: "Explore Stepantsminda Village", description: "The village of Stepantsminda (Kazbegi) is tiny and enchanting — wooden guesthouses, a small market, dogs everywhere, and the Terek River rushing through. Locals are from the Khevsur and Tushetian mountain cultures. After the hike, wander the village, have tea with a guesthouse family, and absorb the extraordinary mountain setting.", details: ["💡 The small Kazbegi Museum on the main street has fascinating exhibits on local mountain culture, Khevsur armor and chain mail, and the region's history."] }
          ],
          meals: [
            { type: "🍽️ Lunch in Kazbegi", name: "Guesthouse Lunch", description: "Have lunch at one of Stepantsminda's family-run guesthouses — traditional Caucasian mountain food: grilled meats, thick bean soups, fresh bread, and Georgian cheese. Simple, hearty, and exactly what you need after a mountain hike. Many guesthouses serve food even to non-guests for ₾15-25.", meta: "₾15-25pp ($5-9) · Any guesthouse in Stepantsminda" }
          ],
          tips: [{ type: "reddit", text: "Kazbegi in early April can still have snow at the church level. Check conditions beforehand and bring layers you'd normally take skiing. The hike is absolutely worth it — Gergeti in snow is even more dramatic than without. But the 4WD taxi is a legitimate option if the trail is icy.", cite: "r/Georgiahiking" }]
        },
        {
          label: "Evening (Return)",
          activities: [
            { title: "Return Marshrutka to Tbilisi", description: "Catch the return marshrutka from Stepantsminda at 4-5pm (departs when full — the driver waits at the main square). Back in Tbilisi by 7:30-8:30pm. You'll be exhausted in the best possible way.", details: ["💡 The marshrutka back fills up fast — be at the square by 3:30pm to be sure of a seat.", "💡 Alternatively, pre-book a shared taxi back with other travelers you meet at the church hike."] }
          ],
          meals: [
            { type: "🍽️ Late Dinner", name: "Rigi Guesthouse Restaurant (simple dinner)", description: "You'll be back in Tbilisi late and tired. Get something simple and satisfying near your guesthouse — lobiani (bean bread), a bowl of thick Georgian bean soup (lobio) with mchadi (corn bread), and a glass of red wine. Every neighborhood restaurant does this well for ₾15-20.", meta: "₾15-20pp ($5-7) · Any Old Town neighborhood restaurant" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 7,
      title: "Kakheti Wine Country & Sighnaghi",
      neighborhoods: "Sighnaghi · Kakheti · Bodbe",
      date: "April 2",
      mapPins: [
        { lat: 41.8060, lng: 44.7300, label: "Tbilisi → Sighnaghi Road", num: 1, cat: "activity", desc: "2-hour drive east through Alazani Valley" },
        { lat: 41.6161, lng: 45.9218, label: "Sighnaghi", num: 2, cat: "activity", desc: "City of Love — fortified hilltop wine town" },
        { lat: 41.6021, lng: 45.9247, label: "Bodbe Monastery", num: 3, cat: "activity", desc: "Tomb of St. Nino who converted Georgia to Christianity" },
        { lat: 41.6100, lng: 45.9100, label: "Alazani Valley Vineyards", num: 4, cat: "food", desc: "8,000-year-old wine tradition in the Kakheti valley" },
        { lat: 41.6200, lng: 45.9300, label: "Pheasant's Tears Winery", num: 5, cat: "food", desc: "Famous natural winery — qvevri wines & restaurant" },
        { lat: 41.6900, lng: 44.8000, label: "Tbilisi (Return)", num: 6, cat: "activity", desc: "Back to Tbilisi for final evening" }
      ],
      timeBlocks: [
        {
          label: "Morning (Departure to Kakheti)",
          activities: [
            { title: "Travel to Sighnaghi via Marshrutka or Tour", description: "Head to Isani/Samgori metro station and catch a marshrutka to Sighnaghi — a 2-hour journey east through the stunning Alazani Valley, which is Georgia's wine heartland. The road passes through vine-covered landscapes and small villages making wine in backyard qvevri vessels. Alternatively, join a small-group wine day tour from Tbilisi (~$35-50pp including transport, tastings, and lunch) — worth it for the included winery visits.", details: ["🚌 Marshrutka from Tbilisi Samgori station to Sighnaghi: ₾10, roughly every 1-2 hours. 2-hr journey.", "💡 A guided tour adds real value here — the guides know which family wineries to visit and explain qvevri winemaking in context. Look for GetYourGuide or local operators offering Kakheti wine tours.", "🍷 Georgia is the birthplace of wine — qvevri (clay vessels buried in earth) winemaking dates back 8,000 years. Kakheti produces ~70% of Georgian wine."] }
          ],
          meals: [
            { type: "☕ Early Breakfast", name: "Quick breakfast before departure", description: "Eat before you leave Tbilisi — grab fresh bread and cheese from a local shop near your guesthouse. You'll eat a big wine country lunch.", meta: "₾8-12 ($3-4)" }
          ],
          tips: []
        },
        {
          label: "Full Day in Kakheti",
          activities: [
            { title: "Sighnaghi — City of Love", description: "Sighnaghi (also spelled Signagi) sits on a hilltop overlooking the Alazani Valley and the Caucasus mountains of Azerbaijan beyond. The entire town is enclosed by a remarkably intact medieval wall with 23 watchtowers — you can walk the full perimeter. The town is charming, small, and full of wine bars, craft shops, and guesthouses. Spring flowers are blooming on the slopes below.", details: ["📍 Sighnaghi is 3km by foot from the bus stop. Walk up or take a taxi (₾3).", "💡 Sighnaghi is known as Georgia's 'City of Love' because the 24-hour registry office allows immediate marriage — couples come from all over. The town decorated its streets for romance as a result."] },
            { title: "Pheasant's Tears Winery & Restaurant", description: "Pheasant's Tears is Georgia's most famous natural winery — founded by American artist John Wurdeman and Georgian winemaker Gela Patalishvili. They use only traditional qvevri methods with indigenous Georgian grapes. Visit the winery, taste their extraordinary amber wines and natural reds, and have lunch at the restaurant (one of the best in the region).", details: ["📍 18 Baratashvili St, Sighnaghi. Open daily. ₾20-30 for a tasting flight.", "💡 The Rkatsiteli amber wine here is the reference point — tannins from skin contact, apricot and dried fruit, completely different from Western white wine. Life-changing for wine lovers."] },
            { title: "Bodbe Monastery", description: "A short taxi ride (₾5) from Sighnaghi brings you to Bodbe Monastery — a 9th-century convent on a forested hillside, where St. Nino (who brought Christianity to Georgia) is buried. The tiny church interior is dark and fragrant with incense, the tomb glowing with candles left by pilgrims. A holy spring at the base of the hill is said to cure illness — Georgians travel from across the country to drink from it.", details: ["📍 3km from Sighnaghi by taxi (₾5-7)", "💡 The spring is at the bottom of a long staircase descent through the forest. Beautiful, quiet, and moving."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Pheasant's Tears Restaurant", description: "The best meal of the trip may happen here. John Wurdeman's restaurant serves traditional Kakhetian dishes: slow-cooked meats from the wood fire, bean dishes with Svan salt, fresh herbs from the garden, and exceptional wines by the glass or bottle. The space is intimate and beautiful. Spring menu features asparagus, fresh herbs, and young wine.", meta: "₾50-70pp ($18-25) including wine · Book ahead if possible" }
          ],
          tips: [{ type: "reddit", text: "Pheasant's Tears in Sighnaghi is legitimately one of the best lunches I've had in Europe. Sit outside if weather permits. Order the amber Rkatsiteli, the bean stew, and whatever meat is on the fire. Stay for two hours. You'll try to leave and fail. Embrace it.", cite: "r/travel" }]
        },
        {
          label: "Evening (Return to Tbilisi)",
          activities: [
            { title: "Return & Final Tbilisi Evening", description: "Marshrutka back to Tbilisi, arriving early evening. Tonight is your last night in the city. Wander the Old Town slowly — you know it now. The familiar alleys, the smell of sulfur drifting up from the baths, the wine bars' glow through carved wooden screens. Have a glass of wine on Shardeni Street and say goodbye to the city properly.", details: [] }
          ],
          meals: [
            { type: "🍷 Farewell Dinner", name: "Shavi Lomi (Return Visit)", description: "Go back to where you started — Shavi Lomi for a final Georgian feast. Order everything you loved plus one thing you haven't tried yet: the mushroom khinkali, the walnut soup, the adjapsandali (Georgian vegetable stew). Toast to the trip with a bottle of Saperavi.", meta: "₾30-50pp ($11-18) · 8 Mingreli St" }
          ],
          tips: [{ type: "tip", text: "Tbilisi grows on you. Many people plan 3 days and stay for 2 weeks. If you feel the pull to extend — listen to it. The city is endlessly explorable and extraordinarily cheap for good quality of life."}]
        }
      ]
    },
    {
      num: 8,
      title: "Final Morning & Departure",
      neighborhoods: "Old Town · Rustaveli · Airport",
      date: "April 3",
      mapPins: [
        { lat: 41.6927, lng: 44.8063, label: "Shardeni Street Morning Walk", num: 1, cat: "activity", desc: "Final Old Town wander before departure" },
        { lat: 41.6930, lng: 44.8058, label: "Anchiskhati Basilica", num: 2, cat: "activity", desc: "Last morning light through the ancient windows" },
        { lat: 41.6853, lng: 44.8104, label: "Abanotubani Farewell", num: 3, cat: "activity", desc: "One last walk past the sulfur bath domes" },
        { lat: 41.6892, lng: 44.8035, label: "Rike Park", num: 4, cat: "activity", desc: "Riverside farewell walk" },
        { lat: 41.6695, lng: 44.9547, label: "Tbilisi International Airport (TBS)", num: 5, cat: "activity", desc: "Depart — leave a piece of your heart in Tbilisi" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Old Town Walk", description: "Wake up early for one last walk through the Old Town before the city fully wakes. Tbilisi at 7am is magical — the alleys empty, morning light filtering through the carved wooden balconies, the first bakeries opening with warm bread, cats everywhere. Walk from your guesthouse to Abanotubani, up past the sulfur bath domes, along the river, through Rike Park, and back. It takes less than an hour and you'll be glad you did it.", details: ["💡 Bring a notebook or just walk without your phone for once. The Old Town morning light deserves full attention.", "📸 Best light for photos: 7-9am, when the golden hour light hits the wooden balconies and the city is quiet."] },
            { title: "Last-Minute Georgian Provisions", description: "Stop at a spice shop or Dezerter Bazaar for churchkhela, dried chacha fruit, Georgian tea, tklapi (dried fruit leather), and Svan salt to take home. These are authentic and excellent gifts/souvenirs that fit in a carry-on. Georgian chocolate (with hazelnut paste) is also excellent.", details: ["💡 Churchkhela survives well in a bag for weeks. Svan salt is unique to Georgia — you won't find it easily elsewhere.", "⚠️ Chacha (Georgian grape spirit) is allowed in carry-on up to 100ml — or pack a bottle in checked luggage."] }
          ],
          meals: [
            { type: "☕ Last Breakfast", name: "Entrée (Near Shardeni)", description: "A lovely modern café near the Old Town that does an excellent Georgian breakfast set: fried eggs with fresh herbs, mchadi cornbread, fresh cheese, honey and tkemali, and excellent coffee. A perfect farewell to Georgian mornings.", meta: "₾15-22pp ($5-8) · Near Shardeni St · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Airport transfer: Metro Line 2 from Isani station to the airport takes about 15 minutes and costs ₾1. Add extra time for the walk from Old Town to Isani station. Leave 2.5-3 hours before your flight — TBS is small but can get backed up at security." }]
        },
        {
          label: "Departure",
          activities: [
            { title: "Tbilisi → Airport", description: "Metro or Bolt taxi to Tbilisi International Airport (TBS). The metro is ₾1, fast, and direct. Bolt taxi is ~₾25. Give yourself 2.5 hours before departure. The duty-free at TBS has Georgian wine, chacha, and churchkhela if you need last-minute gifts.", details: ["🚇 Metro Line 2 from Isani station directly to airport — ₾1, ~20 min.", "🚗 Bolt/Yango taxi: ₾25-30, 20-30 min depending on traffic.", "💡 TBS duty-free has good Georgian wine prices — grab a bottle of Pheasant's Tears or Iago's Wine if you can."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "I've been to 60+ countries and Tbilisi is legitimately one of the most underrated destinations on the planet. The food, the wine, the history, the mountains, the people — all world-class. And it costs basically nothing. Tell everyone. Or don't, so it stays like this.", cite: "r/travel" }]
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
