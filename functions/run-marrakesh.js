const fulfillOrder = require('./fulfill-order');

const order = {
  orderId: "order_1771454341285_jiyti3",
  email: "psyduckler@gmail.com",
  destination: "Marrakesh, Morocco",
  start_date: "2026-06-19",
  end_date: "2026-06-22",
  group_size: "3-4",
  travel_style: "Adventure",
  dining: "Casual throughout",
  budget: "$5,000-10,000",
  requests: "",
  status: "pending"
};

const itineraryData = {
  destination: "Marrakesh, Morocco",
  countryEmoji: "🇲🇦",
  title: "Marrakesh: 4 Days of Adventure in the Red City",
  subtitle: "Medina → Atlas Mountains → Desert Edge → Souks & Rooftops",
  description: "An adventure-packed group trip through Marrakesh and beyond. From getting lost in the labyrinthine medina to quad biking in the Agafay Desert and hiking the Atlas Mountains, this itinerary balances adrenaline with the sensory overload of Morocco's most electrifying city.",
  duration: "4 days",
  dates: "Jun 19 – 22, 2026",
  budget: "$5,000–10,000 for 3–4 travelers",
  pace: "Active & adventurous",
  bestFor: "Friend groups seeking adventure & culture",
  highlights: [
    "Sunrise hot air balloon over the Agafay Desert",
    "Atlas Mountains day trek to Berber villages",
    "Quad biking through palm groves and desert terrain",
    "Getting lost in the souks of the ancient medina",
    "Rooftop dinner overlooking Jemaa el-Fnaa",
    "Traditional hammam spa experience",
    "Camel ride at sunset near the Agafay stone desert",
    "Cooking class with a local Moroccan family"
  ],
  essentials: [
    { title: "🚕 Getting Around", text: "Use petit taxis (beige/cream) within the medina area — always agree on a price before getting in (20-40 MAD for most rides). For day trips, book a private driver through your riad or use a reputable tour operator. Walking is the only way inside the medina." },
    { title: "💰 Money", text: "Moroccan Dirham (MAD). ~10 MAD = $1 USD. ATMs are plentiful in Gueliz (new city). Cash is king in the medina and souks. Cards accepted at upscale restaurants and hotels. Bring small bills for tips and haggling." },
    { title: "🌡️ June Heat", text: "Expect 35-42°C during the day. Start outdoor activities early (7-8am). Long midday breaks at your riad are essential. Evenings cool down to a pleasant 22-25°C. Carry water everywhere." },
    { title: "🏨 Where to Stay", text: "A riad in the medina is the quintessential Marrakesh experience — traditional houses with interior courtyards. Look for riads near Jemaa el-Fnaa or in the Mouassine/Bab Doukkala neighborhoods for easy access." },
    { title: "👗 What to Wear", text: "Morocco is Muslim — dress modestly (shoulders and knees covered, especially women). Loose, breathable fabrics are ideal for the heat. Comfortable walking shoes with grip for cobblestone streets." },
    { title: "🗣️ Language & Haggling", text: "French and Arabic are primary. Many in tourism speak English. Haggling is expected in souks — start at 30-40% of asking price and work up. It's a cultural exchange, not a confrontation. Smile and enjoy it." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & Medina Immersion",
      neighborhoods: "Jemaa el-Fnaa · Medina · Mouassine",
      date: "Jun 19",
      mapPins: [
        { lat: 31.6069, lng: -8.0363, label: "Marrakesh Menara Airport (RAK)", num: 1, cat: "transport", desc: "Arrive and transfer to medina riad" },
        { lat: 31.6258, lng: -7.9891, label: "Jemaa el-Fnaa", num: 2, cat: "activity", desc: "Legendary main square — snake charmers, food stalls, storytellers" },
        { lat: 31.6310, lng: -7.9870, label: "Mouassine Quarter", num: 3, cat: "activity", desc: "Beautiful riad neighborhood with hidden fountains and galleries" },
        { lat: 31.6275, lng: -7.9836, label: "Souk Semmarine", num: 4, cat: "activity", desc: "Main covered souk — textiles, leather, spices, ceramics" },
        { lat: 31.6240, lng: -7.9889, label: "Koutoubia Mosque", num: 5, cat: "activity", desc: "12th-century mosque with iconic 77m minaret — Marrakesh's skyline landmark" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive at Menara Airport → Riad Check-in", description: "Grab a taxi to your riad in the medina. Most riads send a porter to meet you at the nearest car-accessible point — the medina streets are too narrow for vehicles.", details: ["💡 Airport taxi to medina: fixed rate 70-100 MAD. Ignore anyone who says the meter is broken."] },
            { title: "Koutoubia Mosque & Gardens", description: "Walk to the iconic Koutoubia — you can't enter as a non-Muslim, but the exterior and surrounding gardens are stunning. The minaret is visible from all over the city and serves as your compass.", details: ["📍 Just west of Jemaa el-Fnaa"] }
          ],
          meals: [
            { type: "🥗 Late Lunch", name: "Café des Épices", description: "Three-story terrace café overlooking Rahba Kedima spice square. Fresh salads, avocado toast, and mint tea with medina rooftop views.", meta: "60-120 MAD/person · Rahba Kedima" }
          ],
          tips: [{ type: "tip", text: "Don't stress about getting lost in the medina — it's part of the experience. Keep Koutoubia's minaret as your reference point. When truly stuck, any local kid will guide you back to Jemaa el-Fnaa for 10-20 MAD." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Souk Exploration — Mouassine & Semmarine", description: "Dive into the souks as the heat fades. The main covered souks branch off Jemaa el-Fnaa — Souk Semmarine for textiles, Souk des Teinturiers for dyed fabrics, Souk Haddadine for metalwork. Don't buy on the first pass — scout, then return.", details: ["💡 Shops start closing around 8pm. Best browsing is 5-7pm."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Nomad", description: "Modern Moroccan cuisine on a rooftop terrace with Jemaa el-Fnaa views. Try the lamb tangia (slow-cooked in charcoal) and the harissa calamari. Book ahead.", meta: "150-250 MAD/person · 1 Derb Aarjane, Medina" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Jemaa el-Fnaa After Dark", description: "The square transforms at night — dozens of food stalls fire up, Gnaoua musicians play, henna artists work by lamplight, and storytellers draw crowds. It's sensory overload in the best way. Try a fresh-squeezed orange juice (4 MAD) from the famous juice stalls.", details: ["💡 Stall #1 and #14 are local favorites for harira (chickpea soup) and grilled meats. Follow the crowds."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Watch your pockets in the square at night — it's safe but pickpockets are skilled. Keep phones in front pockets." }]
        }
      ]
    },
    {
      num: 2,
      title: "Atlas Mountains Adventure",
      neighborhoods: "Imlil · Asni · Ourika Valley",
      date: "Jun 20",
      mapPins: [
        { lat: 31.1362, lng: -7.9196, label: "Imlil Village", num: 1, cat: "activity", desc: "Gateway to Toubkal — Berber mountain village at 1,740m" },
        { lat: 31.1685, lng: -7.9807, label: "Asni", num: 2, cat: "activity", desc: "Market town at the foot of the High Atlas" },
        { lat: 31.1450, lng: -7.9100, label: "Armed Village Trail", num: 3, cat: "activity", desc: "Scenic trek through walnut groves and Berber terraces" },
        { lat: 31.3642, lng: -7.8428, label: "Ourika Valley Viewpoint", num: 4, cat: "activity", desc: "Lush valley with waterfalls — dramatic contrast to the desert" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Imlil (1.5 hours)", description: "Your driver picks you up at 7am. The road climbs through argan tree forests and Berber villages clinging to mountainsides. Stop at the Tizi n'Test overlook for photos.", details: ["💡 Book a 4x4 with driver through your riad — ~600-800 MAD round trip for the group. Way better than a bus."] },
            { title: "Imlil to Armed Village Trek", description: "A local Berber guide leads you through walnut groves, irrigation channels, and terraced fields to the village of Armed. The views of Toubkal (4,167m — North Africa's highest peak) are incredible. Moderate difficulty, 2-3 hours round trip.", details: ["📍 Guides available in Imlil center — ~300 MAD/group for a half-day", "⚠️ Bring 2L water per person and sun protection. Trail is exposed."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Riad breakfast (included)", description: "Most riads serve a spectacular Moroccan breakfast — msemen (flatbread), amlou (almond-argan dip), fresh fruit, eggs, and endless mint tea.", meta: "Included with riad stay" }
          ],
          tips: [{ type: "tip", text: "June in the Atlas is warm but much cooler than Marrakesh — bring a light layer for the early morning drive. Temperature at Imlil hovers around 25°C." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Berber Lunch in Imlil", description: "Eat with a Berber family or at a village café — expect tagine cooked over charcoal, fresh bread baked in a communal oven, and the best mint tea you've ever had.", details: [] },
            { title: "Ourika Valley Waterfalls (optional stop on return)", description: "If the group has energy, detour to Setti Fatma in the Ourika Valley for a short hike to the seven waterfalls. The first two are easy to reach.", details: ["💡 Entry: 10 MAD. Local guides will offer to show you the upper falls — worth it for ~50 MAD."] }
          ],
          meals: [
            { type: "🍲 Lunch", name: "Village Tagine in Imlil", description: "Home-cooked chicken or lamb tagine with preserved lemons and olives, served on a rooftop with mountain views. Simple, unforgettable.", meta: "80-120 MAD/person · Imlil village" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Return to Marrakesh & Hammam", description: "Back in Marrakesh by 5pm. Head to a traditional hammam (Moroccan bathhouse) to soak out the trek. Heritage Spa or Hammam de la Rose offer the full experience: steam room, black soap scrub, and massage.", details: ["💡 Heritage Spa: ~400 MAD for full hammam + massage (1.5 hours). Book ahead."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Al Fassia Aguedal", description: "Run entirely by women — one of the best traditional Moroccan restaurants in the city. The pastilla (pigeon or chicken in crispy filo with cinnamon and almonds) is legendary.", meta: "200-350 MAD/person · Aguedal, outside medina" }
          ],
          tips: [{ type: "tip", text: "A hammam after a mountain trek is peak Morocco. Don't skip it — your muscles will thank you." }]
        }
      ]
    },
    {
      num: 3,
      title: "Agafay Desert & Adrenaline Day",
      neighborhoods: "Agafay Desert · Palmeraie",
      date: "Jun 21",
      mapPins: [
        { lat: 31.4700, lng: -8.2200, label: "Agafay Desert", num: 1, cat: "activity", desc: "Rocky lunar desert 40 min from Marrakesh — Morocco's 'desert lite'" },
        { lat: 31.4650, lng: -8.2100, label: "Quad Biking Base", num: 2, cat: "activity", desc: "Quad/ATV adventure through desert terrain and dry riverbeds" },
        { lat: 31.4500, lng: -8.2300, label: "Camel Ride Sunset Point", num: 3, cat: "activity", desc: "Sunset camel trek through the stone desert" },
        { lat: 31.6600, lng: -8.0250, label: "Palmeraie", num: 4, cat: "activity", desc: "Palm grove oasis north of the medina — camel rides and gardens" }
      ],
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            { title: "Hot Air Balloon over Agafay", description: "5am pickup for a sunrise hot air balloon ride over the Agafay Desert and Atlas Mountain foothills. Floating above the barren lunar landscape as the sun paints the Atlas peaks pink is genuinely one of the most surreal experiences in Morocco.", details: ["💡 Book with Ciel d'Afrique — most established operator. ~€180/person including transfers and breakfast.", "⚠️ Flights are weather-dependent. Book for this morning with a backup slot."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Post-balloon Berber Breakfast", description: "Most balloon operators include a ground breakfast after landing — fresh bread, jams, pastries, and mint tea in the desert. Surreal vibes.", meta: "Included with balloon ride" }
          ],
          tips: [{ type: "tip", text: "This is a 4:30-5am wake-up call. Worth every second of lost sleep. Dress in layers — mornings in the desert are cool." }]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "Quad Biking in Agafay", description: "After the balloon, switch gears to quad biking through the rocky desert terrain. Most tours are 2 hours through dry riverbeds, Berber villages, and palm groves. Dusty, loud, and an absolute blast.", details: ["💡 ~€50-70/person for a 2-hour guided quad tour. Helmet and goggles provided.", "⚠️ Wear clothes you don't mind getting dirty. Dust gets everywhere."] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Moroccan Cooking Class", description: "Back in Marrakesh, join a hands-on cooking class. Visit a local market to buy ingredients, then learn to make tagine, couscous, and Moroccan salads from scratch. You eat everything you cook.", details: ["💡 La Maison Arabe and Café Clock both run excellent classes — ~€40-60/person including market visit and meal."] }
          ],
          meals: [
            { type: "🍲 Lunch", name: "Your Own Cooking!", description: "The best meal is the one you make yourself — tagine, couscous, zaalouk (smoky eggplant dip), and khobz (Moroccan bread) fresh from the oven.", meta: "Included in cooking class" }
          ],
          tips: [{ type: "tip", text: "Ask to learn how to make Moroccan mint tea properly — it's an art form involving pouring from height. Great party trick back home." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset Camel Ride in the Palmeraie", description: "A mellow sunset camel ride through the palm groves on the edge of the city. It's touristy, but riding a camel through palms as the sun goes down over the Atlas Mountains is undeniably magical.", details: ["💡 ~200-300 MAD/person for 1 hour. Book through your riad for best rates."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Le Jardin", description: "Hidden garden restaurant in the medina — lush greenery, fairy lights, and modern Moroccan-Mediterranean fusion. Try the lamb mrouzia (sweet-savory tagine with raisins and almonds).", meta: "150-250 MAD/person · 32 Souk Sidi Abdelaziz, Medina" }
          ],
          tips: [{ type: "tip", text: "Tonight's your last big night — hit the rooftop bars in Gueliz (new city) for cocktails. Baromètre and 68 Bar à Vin are popular." }]
        }
      ]
    },
    {
      num: 4,
      title: "Final Souk Run & Departure",
      neighborhoods: "Medina · Mellah · Gueliz",
      date: "Jun 22",
      mapPins: [
        { lat: 31.6223, lng: -7.9837, label: "Bahia Palace", num: 1, cat: "activity", desc: "Stunning 19th-century palace with intricate zellige tilework" },
        { lat: 31.6200, lng: -7.9820, label: "Mellah (Jewish Quarter)", num: 2, cat: "activity", desc: "Historic quarter with spice market and Lazama Synagogue" },
        { lat: 31.6290, lng: -7.9850, label: "Ensemble Artisanal", num: 3, cat: "activity", desc: "Government fixed-price craft center — good for comparison shopping" },
        { lat: 31.6355, lng: -8.0100, label: "Gueliz (New City)", num: 4, cat: "activity", desc: "Modern Marrakesh — cafés, galleries, and boutiques" },
        { lat: 31.6069, lng: -8.0363, label: "Marrakesh Menara Airport (RAK)", num: 5, cat: "transport", desc: "Departure" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bahia Palace", description: "A masterpiece of Moroccan architecture — acres of zellige tilework, carved cedar ceilings, and tranquil courtyards. Built in the 1860s for a grand vizier's harem. Go early to beat the tour buses.", details: ["💡 70 MAD entry. Opens at 9am. Allow 45 min-1 hour.", "📍 Near Place des Ferblantiers"] },
            { title: "Mellah & Spice Market", description: "Wander through the old Jewish Quarter — the Lazama Synagogue is worth a peek. The nearby spice souk (Rahba Kedima) is where you find saffron, ras el hanout, and argan oil for gifts.", details: ["💡 Real saffron is ~30-50 MAD/gram. If it's cheap, it's fake."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Riad Breakfast", description: "Final Moroccan breakfast spread at the riad. Savor every bite of msemen and amlou — you'll miss it.", meta: "Included" }
          ],
          tips: [{ type: "tip", text: "For souvenir shopping, visit Ensemble Artisanal first (fixed prices) to calibrate your haggling expectations in the souks." }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Final Souk Shopping Sprint", description: "Last chance to grab those leather babouches (slippers), hand-painted ceramics, woven baskets, or brass lanterns. Armed with prices from Ensemble Artisanal, you'll haggle like a pro.", details: ["💡 Best buys: leather goods, argan oil, ceramic tagines, Berber rugs (if you want to ship), spices"] }
          ],
          meals: [
            { type: "🥗 Brunch", name: "KAOWA", description: "Trendy café in Gueliz with avocado toasts, acai bowls, and specialty coffee. A modern contrast to your medina mornings.", meta: "80-150 MAD/person · Rue de la Liberté, Gueliz" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Departure", description: "Taxi to Menara Airport (~30 min from medina). Allow extra time — airport security lines can be long during peak season.", details: ["💡 Airport taxi: 70-100 MAD fixed rate. Have your riad call one."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Morocco has a saying: 'You leave Marrakesh, but Marrakesh never leaves you.' You'll be back. 🇲🇦" }]
        }
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
