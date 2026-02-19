const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771452311536_q9m7dn",
  email: "psyduckler@gmail.com",
  destination: "Santorini, Greece",
  start_date: "2026-08-18",
  end_date: "2026-08-23",
  group_size: "1",
  travel_style: "Cultural, Nightlife",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-18T22:05:11.536Z",
  status: "pending"
};

const itineraryData = {
  destination: "Santorini, Greece",
  countryEmoji: "🇬🇷",
  title: "Santorini: 6 Days of Culture, Sunsets & After-Dark Magic",
  subtitle: "Fira → Oia → Akrotiri → Pyrgos → Perissa → Fira",
  description: "A solo adventure through Santorini's volcanic landscapes, ancient ruins, and legendary nightlife. From cliff-side wine tastings at sunset to late-night cocktails in Fira's caldera bars, this itinerary blends deep cultural exploration with the island's vibrant after-dark scene.",
  duration: "6 days",
  dates: "Aug 18 – 23, 2026",
  budget: "Moderate",
  pace: "Relaxed with late nights",
  bestFor: "Solo travelers, culture lovers & night owls",
  highlights: [
    "Iconic Oia sunset from the castle ruins",
    "Ancient Akrotiri — the 'Pompeii of the Aegean'",
    "Wine tasting on volcanic terroir in Megalochori",
    "Fira's buzzing caldera-view cocktail bars",
    "Black sand beaches of Perissa and Kamari",
    "Pyrgos village — medieval alleys and panoramic views",
    "Late-night bar crawls through Fira's Gold Street",
    "Catamaran sunset cruise with dinner"
  ],
  essentials: [
    { title: "🚗 Getting Around", text: "Rent an ATV or scooter (€20-35/day) — it's the easiest way to get around the island solo. Buses run between major towns but stop around 11pm. Taxis are scarce in peak season." },
    { title: "💶 Cash & Cards", text: "Most restaurants and bars accept cards, but keep €50-100 cash for small shops, beach chairs, and bus fare. ATMs are in Fira and Oia." },
    { title: "🌡️ August Heat", text: "Expect 30-35°C daily. Carry water, wear sunscreen, and plan indoor activities (museums, wine caves) for midday. Evenings cool down beautifully." },
    { title: "🏨 Where to Stay", text: "Base yourself in Fira for nightlife access and central bus connections. Caldera-view hotels book out months ahead — book early or consider Firostefani for a quieter alternative with the same views." },
    { title: "👟 Footwear", text: "Cobblestone streets and volcanic paths are uneven. Bring sturdy sandals for day and comfortable shoes for cliffside walks. Skip the heels." },
    { title: "🌅 Sunset Strategy", text: "Oia gets packed 2 hours before sunset. Arrive early or watch from a restaurant with a reservation. Fira and Imerovigli offer equally stunning views with fewer crowds." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & Fira First Impressions",
      neighborhoods: "Fira · Firostefani",
      date: "Aug 18",
      mapPins: [
        { lat: 36.3932, lng: 25.4615, label: "Santorini Airport (JTR)", num: 1, cat: "transport", desc: "Arrive and transfer to Fira" },
        { lat: 36.4167, lng: 25.4314, label: "Fira Town Center", num: 2, cat: "lodging", desc: "Check into hotel in the heart of Fira" },
        { lat: 36.4186, lng: 25.4280, label: "Caldera Walkway", num: 3, cat: "activity", desc: "Stunning cliffside promenade with volcano views" },
        { lat: 36.4237, lng: 25.4285, label: "Firostefani", num: 4, cat: "activity", desc: "Quieter village with iconic blue dome photo spot" },
        { lat: 36.4170, lng: 25.4320, label: "Tropical Bar", num: 5, cat: "nightlife", desc: "Legendary caldera-view cocktail bar" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive at Santorini Airport → Fira", description: "Take a bus (€1.80) or taxi (€20) to Fira. Drop your bags and get oriented.", details: ["💡 Airport bus runs every 30 min in summer"] },
            { title: "Caldera Walkway Stroll", description: "Walk along the cliff edge from Fira toward Firostefani. The views of the caldera, volcano, and Thirassia island are jaw-dropping.", details: ["📍 Starts near the cable car station in Fira"] }
          ],
          meals: [
            { type: "🥗 Late Lunch", name: "Argo Restaurant", description: "Caldera-view taverna with classic Greek dishes. Try the fava (yellow split pea purée) — it's Santorini's signature.", meta: "€15-25 · Fira caldera path" }
          ],
          tips: [{ type: "tip", text: "Don't rush to do everything Day 1. Santorini rewards slow afternoons and long evenings." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Firostefani Blue Dome Photo Spot", description: "The most photographed spot in Santorini — three blue domes with the caldera behind. Best light is late afternoon.", details: ["📍 Near Agios Theodori church, Firostefani"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Naoussa Tavern", description: "Family-run spot with grilled octopus and local wine. Unpretentious and delicious.", meta: "€20-30 · Central Fira" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Tropical Bar & Fira Bar Scene", description: "Start at Tropical — the most iconic bar in Fira with caldera views and strong cocktails. Then drift down Gold Street (Erithrou Stavrou) where the clubs and bars line up.", details: ["💡 Things don't get going until 11pm-midnight in summer"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Solo tip: sit at the bar. Santorini attracts travelers from everywhere — you'll make friends fast." }]
        }
      ]
    },
    {
      num: 2,
      title: "Akrotiri Ruins & South Coast Beaches",
      neighborhoods: "Akrotiri · Red Beach · Perissa",
      date: "Aug 19",
      mapPins: [
        { lat: 36.3516, lng: 25.4036, label: "Akrotiri Archaeological Site", num: 1, cat: "activity", desc: "Bronze Age Minoan city preserved in volcanic ash" },
        { lat: 36.3473, lng: 25.3940, label: "Red Beach", num: 2, cat: "activity", desc: "Dramatic red volcanic cliffs meeting turquoise water" },
        { lat: 36.3553, lng: 25.4734, label: "Perissa Beach", num: 3, cat: "activity", desc: "Black sand beach with beach bars and loungers" },
        { lat: 36.3560, lng: 25.4740, label: "Wet Stories Beach Bar", num: 4, cat: "nightlife", desc: "Beach bar that turns into a party after dark" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Akrotiri Archaeological Site", description: "A Bronze Age city frozen in time by the volcanic eruption of 1600 BC. Incredibly well-preserved frescoes, streets, and multi-story buildings. Often called the 'Pompeii of the Aegean.'", details: ["💡 €12 entry. Go early (8am) to beat tour groups. Allow 1.5-2 hours.", "📍 Southwest tip of the island"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The audio guide is worth it — brings the ruins to life. The site is covered and shaded, so it's comfortable even in August heat." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Red Beach", description: "A short walk from Akrotiri, this beach is famous for its towering red volcanic cliffs. Swim in the crystal-clear water and snap photos.", details: ["⚠️ Check if the path is open — rockfalls sometimes close it. Boat access from Akrotiri port is an alternative."] },
            { title: "Perissa Black Sand Beach", description: "Head to the other coast for the long stretch of black sand. Grab a sunbed, swim, and relax. The water is deep blue against the dark sand.", details: [] }
          ],
          meals: [
            { type: "🐟 Lunch", name: "God's Garden (Perissa)", description: "Right on the beach — fresh grilled fish, Greek salad, cold Mythos beer. Perfect beach lunch.", meta: "€15-25 · Beachfront Perissa" }
          ],
          tips: []
        },
        {
          label: "Evening & Night",
          activities: [
            { title: "Perissa Beach Bar Scene", description: "Perissa transforms after dark. Wet Stories and Chilli Bar pump music on the beach. It's more casual and young than Fira's scene — board shorts and cocktails.", details: ["💡 Thursdays and Saturdays tend to be the biggest nights"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Tranquilo Perissa", description: "Mediterranean-Greek fusion right on the sand. Great cocktails and chill atmosphere before the party starts.", meta: "€20-35 · Perissa beachfront" }
          ],
          tips: [{ type: "reddit", text: "Perissa is underrated for nightlife. Way more relaxed than Fira and you can literally go from dancing to swimming at 2am.", cite: "r/solotravel" }]
        }
      ]
    },
    {
      num: 3,
      title: "Oia: Castles, Art & the Legendary Sunset",
      neighborhoods: "Oia · Ammoudi Bay",
      date: "Aug 20",
      mapPins: [
        { lat: 36.4613, lng: 25.3756, label: "Oia Village", num: 1, cat: "activity", desc: "Iconic whitewashed village on the northern tip" },
        { lat: 36.4630, lng: 25.3720, label: "Oia Castle (Sunset Point)", num: 2, cat: "activity", desc: "The famous sunset viewing spot" },
        { lat: 36.4580, lng: 25.3760, label: "Naval Maritime Museum", num: 3, cat: "activity", desc: "Santorini's seafaring history in a beautiful mansion" },
        { lat: 36.4652, lng: 25.3712, label: "Ammoudi Bay", num: 4, cat: "food", desc: "Tiny fishing port with seafood tavernas at the base of the cliff" },
        { lat: 36.4590, lng: 25.3750, label: "Karma Cocktail Bar", num: 5, cat: "nightlife", desc: "Oia's best after-sunset cocktails" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Explore Oia Village", description: "Wander the marble lanes, cave houses, and blue-domed churches. Visit the small art galleries — Oia has a thriving art scene. The Naval Maritime Museum tells the story of Santorini's merchant sailors.", details: ["💡 Take the bus from Fira (30 min, €1.80) or ride your ATV. Arrive by 10am before day-trippers flood in."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The back streets of Oia away from the main path are where the real charm is. Get lost." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ammoudi Bay", description: "Descend 300 steps (or take a donkey, but walking is better for the donkeys) to the tiny port below Oia. Swim off the rocks, then have the freshest seafood lunch of your life.", details: ["📍 Steps start near the castle"] }
          ],
          meals: [
            { type: "🦑 Lunch", name: "Ammoudi Fish Taverna", description: "Tables on the rocks by the water. Grilled octopus hung to dry on the line. Order whatever's fresh — the sea urchin and fried calamari are legendary.", meta: "€25-40 · Ammoudi Bay port" }
          ],
          tips: [{ type: "reddit", text: "Jump off the rocks at Ammoudi Bay — locals do it all day. The water is incredibly clear and deep enough.", cite: "r/greece" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Oia Sunset at the Castle", description: "Claim your spot at least 90 minutes before sunset. The castle ruins fill up fast but the atmosphere is electric — hundreds of people, applause when the sun dips below the horizon. It's a whole event.", details: ["🌅 August sunset is around 8:15-8:20pm"] }
          ],
          meals: [
            { type: "🍷 Dinner", name: "Pelekanos Restaurant", description: "Book a sunset table — caldera view dining with creative Greek cuisine. The lamb kleftiko and Santorini cherry tomato dishes are standouts.", meta: "€35-50 · Reserve 2-3 days ahead" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Karma Cocktail Bar & Oia After Dark", description: "Oia is quieter than Fira at night, but Karma has excellent cocktails with caldera views under the stars. Perfect for a chill solo nightcap before heading back.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Last bus to Fira leaves around 11:30pm. After that it's taxi (€25-30) or a beautiful but long walk." }]
        }
      ]
    },
    {
      num: 4,
      title: "Wine, Villages & Volcano",
      neighborhoods: "Pyrgos · Megalochori · Nea Kameni",
      date: "Aug 21",
      mapPins: [
        { lat: 36.3791, lng: 25.4452, label: "Pyrgos Village", num: 1, cat: "activity", desc: "Medieval hilltop village with 360° views" },
        { lat: 36.3860, lng: 25.4380, label: "Santo Wines", num: 2, cat: "food", desc: "Famous winery with caldera views and tastings" },
        { lat: 36.3720, lng: 25.4280, label: "Venetsanos Winery", num: 3, cat: "food", desc: "Cliffside winery — arguably the best sunset view" },
        { lat: 36.4060, lng: 25.3960, label: "Nea Kameni (Volcano)", num: 4, cat: "activity", desc: "Hike the active volcano crater in the caldera" },
        { lat: 36.4170, lng: 25.4330, label: "Koo Club", num: 5, cat: "nightlife", desc: "Fira's premier nightclub" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Nea Kameni Volcano Hike", description: "Take a boat from Fira's old port to the volcanic island in the middle of the caldera. Hike to the crater (20 min), see steam vents, and take in 360° views of the caldera from the center.", details: ["💡 €15-20 for the boat + €5 crater entry. Tours run from 10am. Bring water and a hat — there's zero shade.", "📍 Boats leave from the old port at the bottom of Fira (cable car or donkey down)"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Some tours include hot springs after the volcano — you swim in warm sulfur water. Fun but it'll stain light swimwear yellow." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Pyrgos Village", description: "The highest village on the island, built around a Venetian castle. Quieter and more authentic than Oia. Climb to the top of Kasteli for the best panoramic view on the island.", details: [] },
            { title: "Wine Tasting at Santo Wines", description: "Santorini's volcanic soil produces unique Assyrtiko wine. Santo Wines' terrace overlooks the caldera — pair flights with local cheese and cherry tomato preserves.", details: ["💡 €15-25 for a tasting flight. No reservation needed but go before 5pm to avoid crowds."] }
          ],
          meals: [
            { type: "🍷 Lunch", name: "Franco's Café (Pyrgos)", description: "Hidden gem in the castle village. Simple Greek plates, local wine, and a peaceful terrace with views stretching to the sea.", meta: "€15-20 · Pyrgos hilltop" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Venetsanos Winery Sunset", description: "Skip the Oia crowds and watch sunset from this cliffside winery. Industrial-chic design, outstanding Vinsanto (sweet wine), and a view that rivals any on the island.", details: ["💡 Arrive by 7pm for a good spot. No reservation needed for tastings."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Metaxy Mas", description: "Widely considered the best restaurant on Santorini. Creative Cretan-Greek cuisine — book days ahead. The lamb chops and stuffed zucchini flowers are unforgettable.", meta: "€30-45 · Exo Gonia village · Reserve ahead" }
          ],
          tips: [{ type: "reddit", text: "Metaxy Mas is the one restaurant everyone agrees on. It's inland with no view — and nobody cares because the food is that good.", cite: "r/santorini" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Koo Club & Fira Gold Street", description: "Back in Fira for the big night out. Koo Club is the main nightclub — open-air with international DJs in summer. Start at Two Brothers or Tango Bar for warmup cocktails on Gold Street.", details: ["💡 Koo gets busy after 1am. No cover most nights. Drinks €10-15."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Saturday night is the biggest in Fira. The whole street comes alive." }]
        }
      ]
    },
    {
      num: 5,
      title: "Catamaran Cruise & Final Fira Night",
      neighborhoods: "Caldera · Thirassia · Fira",
      date: "Aug 22",
      mapPins: [
        { lat: 36.4100, lng: 25.4000, label: "Caldera Catamaran Cruise", num: 1, cat: "activity", desc: "Sailing the caldera with stops for swimming and dinner" },
        { lat: 36.4400, lng: 25.3500, label: "Thirassia Island", num: 2, cat: "activity", desc: "Quiet island across the caldera — untouched by tourism" },
        { lat: 36.4170, lng: 25.4310, label: "PK Cocktail Bar", num: 3, cat: "nightlife", desc: "Rooftop cocktails with volcano view" },
        { lat: 36.4165, lng: 25.4325, label: "Enigma Club", num: 4, cat: "nightlife", desc: "Outdoor club in a converted mansion courtyard" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sleep In & Brunch", description: "After last night's adventures, take it slow. Wander to a café for a long Greek breakfast — thick yogurt, honey, fresh orange juice, and a freddo cappuccino.", details: [] }
          ],
          meals: [
            { type: "🥐 Brunch", name: "Mama Thira", description: "Cozy brunch spot in central Fira with excellent coffee and homemade pastries. The bougatsa (custard pie) is perfect.", meta: "€10-15 · Fira center" }
          ],
          tips: []
        },
        {
          label: "Afternoon → Sunset",
          activities: [
            { title: "Sunset Catamaran Cruise", description: "The quintessential Santorini experience. Board a catamaran for 5 hours of sailing the caldera. Stops at the volcano hot springs, Red Beach, White Beach, and Thirassia. BBQ dinner on board as the sun sets over the Aegean.", details: ["💡 €120-180 per person. Book with Sunset Oia or Santorini Sailing. They include food, drinks, and snorkel gear.", "📍 Departs from Vlychada port, usually around 2-3pm"] }
          ],
          meals: [
            { type: "🍖 Dinner", name: "BBQ on the Catamaran", description: "Fresh fish, grilled chicken, Greek salad, and unlimited wine/beer as you watch the sunset from the water. Surreal.", meta: "Included in cruise price" }
          ],
          tips: [{ type: "tip", text: "Solo travelers: catamaran cruises are very social. You'll share the boat with 15-20 people and everyone mingles. Great way to meet people for your last night out." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Final Night: PK Cocktail Bar → Enigma Club", description: "Start at PK Cocktail Bar for rooftop drinks, then head to Enigma — an open-air club in a mansion courtyard. It's your last night, make it count.", details: ["💡 Enigma is more upscale. €15 cocktails but the setting is worth it."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Get gyros from Lucky's Souvlaki at 3am on the walk home. Best drunk food on the island." }]
        }
      ]
    },
    {
      num: 6,
      title: "Morning Farewell",
      neighborhoods: "Fira · Santorini Airport",
      date: "Aug 23",
      mapPins: [
        { lat: 36.4167, lng: 25.4314, label: "Fira", num: 1, cat: "activity", desc: "Final morning in town" },
        { lat: 36.3932, lng: 25.4615, label: "Santorini Airport (JTR)", num: 2, cat: "transport", desc: "Departure" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Last Morning Walk", description: "Wake up early for one final stroll along the caldera path. The morning light on the white buildings is magical — and you'll have it almost to yourself.", details: [] },
            { title: "Depart Santorini", description: "Head to the airport or port for your onward journey. Yiá sou, Santorini!", details: ["💡 Airport is 15 min from Fira. Leave 2 hours before flight in peak August."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Corner Café (Fira)", description: "One last freddo espresso and tiropita (cheese pie) with a caldera view. A perfect goodbye.", meta: "€8-12 · Fira walkway" }
          ],
          tips: [{ type: "tip", text: "If flying out later, leave your bags at the hotel and squeeze in a morning swim at Kamari beach (20 min by bus)." }]
        }
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
