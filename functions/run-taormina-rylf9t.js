const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771625755795_rylf9t",
  email: "psyduckler@gmail.com",
  destination: "Taormina, Metropolitan City of Messina, Italy",
  start_date: "2026-06-17",
  end_date: "2026-06-21",
  group_size: "2",
  travel_style: "Adventure, Foodie, Relaxation",
  dining: "",
  budget: "",
  requests: "Romantic couply things",
  amount: "0.00",
  status: "pending"
};

const itineraryData = {
  destination: "Taormina, Sicily, Italy",
  countryEmoji: "🇮🇹",
  title: "Taormina: 5 Days of Amore on Sicily's Coast",
  subtitle: "Ancient Theatre · Mount Etna · Isola Bella · Sicilian Cuisine · Sunset Aperitivo",
  description: "Taormina is the kind of place that makes you forget the rest of the world exists. Perched on a cliff 200 meters above the Ionian Sea with Mount Etna smoking in the background, it's been seducing travelers since the ancient Greeks. This 5-day escape for two weaves together adventure (Etna crater hike, kayaking Isola Bella), world-class Sicilian food, and pure romantic downtime — rooftop sunsets, hidden beaches, and long dinners where nobody rushes you. Sicily at its most intoxicating.",
  duration: "5 days",
  dates: "Jun 17 – 21, 2026",
  budget: "Mid-range ($2,500–4,500 for two)",
  pace: "Relaxed mornings, active afternoons, romantic evenings",
  bestFor: "Couples seeking romance + adventure",
  highlights: [
    "Watching sunset from the Ancient Greek Theatre with Etna as backdrop",
    "Hiking Mount Etna's summit craters with a vulcanologist guide",
    "Kayaking the crystal-clear waters around Isola Bella",
    "Hands-on Sicilian cooking class in a hillside farmhouse",
    "Aperitivo on a rooftop terrace overlooking the Bay of Naxos",
    "Swimming at the hidden Mazzarò Beach via cable car descent",
    "Strolling Corso Umberto at golden hour — gelato in hand",
    "Seafood dinner at a candlelit terrace in Castelmola"
  ],
  essentials: [
    {
      title: "✈️ Getting There",
      text: "Fly into Catania–Fontanarossa Airport (CTA), ~1 hour from Taormina. Pre-book a private transfer (~€60-80) or take the Interbus shuttle. Driving yourself is fine but Taormina's historic center is pedestrian-only — your hotel may have parking or use the Lumbi or Porta Catania garages (~€15/day). Train from Catania takes ~50 min to Taormina-Giardini station, then a quick bus up the hill."
    },
    {
      title: "💶 Money",
      text: "Euro (€). Cards accepted at restaurants and hotels but carry some cash for small shops, beach vendors, and tips. A nice dinner for two: €60-120. Granita + brioche breakfast: €5-7. Gelato: €2.50-4. Sicily is significantly cheaper than northern Italy — your money stretches further here."
    },
    {
      title: "☀️ June Weather",
      text: "Expect 25–32°C (77–90°F) with abundant sunshine. The sea is warm enough for swimming (~22°C). Evenings are perfect — warm enough for a dress or linen shirt, cool enough for lingering dinners outdoors. Bring sunscreen, a hat, and comfortable sandals. Rain is very rare in June."
    },
    {
      title: "🏨 Where to Stay",
      text: "For romance, stay in or near the historic center on Corso Umberto. Belmond Grand Hotel Timeo (splurge — directly next to the Greek Theatre with Etna views), Hotel Villa Carlotta (elegant mid-range with pool), or a boutique B&B on Via Bagnoli Croce for charm on a budget. Book a room with a sea or Etna view — it's worth every euro."
    },
    {
      title: "🍝 Eating Well",
      text: "Sicily's food is legendary. Must-try: pasta alla Norma (eggplant + ricotta salata), arancini (fried rice balls), fresh pesce spada (swordfish), cannoli, and granita con brioche for breakfast. Wine: Etna Rosso (volcanic red) and Nero d'Avola are the stars. Don't skip the aperitivo ritual — Aperol Spritz with a sea view is a religious experience here."
    },
    {
      title: "📋 Book Ahead",
      text: "Etna summit tours sell out in summer — book 2-3 weeks ahead. Restaurant reservations for dinner (especially La Capinera, Otto Geleng, and Vicolo Stretto) should be made 1-2 weeks in advance. Isola Bella beach gets crowded — arrive before 10am or do a kayak tour to avoid the masses."
    }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & Falling for Taormina",
      neighborhoods: "Catania Airport → Taormina · Corso Umberto · Piazza IX Aprile",
      date: "Jun 17",
      mapPins: [
        { lat: 37.4668, lng: 15.0664, label: "Catania Airport (CTA)", num: 1, cat: "transport", desc: "Fly into Sicily's eastern hub — 1 hour from Taormina" },
        { lat: 37.8523, lng: 15.2884, label: "Corso Umberto I", num: 2, cat: "activity", desc: "Taormina's elegant main street — pedestrian-only, lined with cafés and boutiques" },
        { lat: 37.8516, lng: 15.2853, label: "Piazza IX Aprile", num: 3, cat: "activity", desc: "The most photogenic piazza in Sicily — terrace views over the bay and Etna" },
        { lat: 37.8529, lng: 15.2920, label: "Teatro Antico di Taormina", num: 4, cat: "activity", desc: "3rd-century BC Greek theatre with Etna and sea panorama — magical at sunset" },
        { lat: 37.8555, lng: 15.2815, label: "Porta Messina", num: 5, cat: "activity", desc: "Northern gate to the old town — start your Corso Umberto stroll here" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          items: [
            { icon: "✈️", title: "Arrive at Catania Airport", text: "Private transfer to Taormina (~€70, 1 hour). Watch the coastline unfold as you climb toward the hilltop town. Check into your hotel and let the views sink in." },
            { icon: "🚶", title: "First Stroll on Corso Umberto", text: "Walk the entire length of Taormina's main drag from Porta Messina to Porta Catania. Stop at Piazza IX Aprile — the terrace with the checkerboard floor overlooking the bay is jaw-dropping. Get your first gelato at Bam Bar (their granita is famous)." },
            { icon: "🏛️", title: "Greek Theatre at Golden Hour", text: "Time your visit to the Teatro Antico for late afternoon. The light on Etna turns golden and the ancient stone glows. This 2,300-year-old theatre has the most dramatic backdrop in the Mediterranean. €10 entry, worth every cent." }
          ]
        },
        {
          label: "Evening",
          items: [
            { icon: "🍹", title: "Aperitivo at Piazza IX Aprile", text: "Grab a table at Mocambo Bar or Wunderbar Caffè (where Elizabeth Taylor once held court). Aperol Spritz, olives, and that view. This is your daily ritual now." },
            { icon: "🍽️", title: "Dinner: Vicolo Stretto", text: "Intimate alley restaurant with creative Sicilian cuisine. Try the tuna tartare, pasta with sea urchin, and anything with pistachio. Reserve a table outside — the narrow lane draped in vines is impossibly romantic. Budget ~€80-100 for two with wine." }
          ]
        }
      ]
    },
    {
      num: 2,
      title: "Mount Etna: Europe's Mightiest Volcano",
      neighborhoods: "Etna South · Rifugio Sapienza · Summit Craters · Taormina",
      date: "Jun 18",
      mapPins: [
        { lat: 37.7000, lng: 14.9927, label: "Rifugio Sapienza (Etna South)", num: 1, cat: "activity", desc: "Base camp at 1,900m — cable car and 4x4s depart for the summit from here" },
        { lat: 37.7510, lng: 14.9934, label: "Etna Summit Craters (~3,300m)", num: 2, cat: "activity", desc: "Active volcanic craters with smoking fumaroles — guided access only above 2,920m" },
        { lat: 37.6414, lng: 15.0280, label: "Etna DOC Winery (Gambino)", num: 3, cat: "food", desc: "Volcanic-soil vineyards producing Etna Rosso and Bianco — tasting with Etna views" },
        { lat: 37.8516, lng: 15.2853, label: "Piazza IX Aprile (return)", num: 4, cat: "activity", desc: "Back to Taormina for a well-earned sunset" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          items: [
            { icon: "🌋", title: "Etna Summit Hike (Guided)", text: "Depart Taormina ~8am. Your guide picks you up and drives to Rifugio Sapienza (1,900m). Take the cable car + 4x4 to 2,900m, then hike to the summit craters (~3,300m). You'll walk on still-warm lava flows, peer into steaming vents, and see all of Sicily spread below. The scale is humbling. Dress in layers — it's 15-20°C cooler up top. Tour runs ~5-6 hours. Book with Etna People or Gruppo Guide Alpine Etna (~€80-100/person including cable car + 4x4)." }
          ]
        },
        {
          label: "Afternoon",
          items: [
            { icon: "🍷", title: "Wine Tasting on Etna's Slopes", text: "On the drive back, stop at a winery on Etna's northern or eastern slopes. Gambino Vini or Tenuta delle Terre Nere produce stunning Etna Rosso from Nerello Mascalese grapes grown in volcanic soil. Tasting + light lunch with views of the vines and the volcano above. ~€25-35/person." },
            { icon: "🛁", title: "Hotel Pool Time", text: "Back in Taormina by late afternoon. Decompress at the hotel pool or book a couples' massage. You earned it after 3,300 meters of altitude." }
          ]
        },
        {
          label: "Evening",
          items: [
            { icon: "🍽️", title: "Dinner: La Capinera", text: "One-Michelin-star seafood right on the coast below Taormina. Chef Pietro D'Agostino does exquisite things with local fish — the crudo tasting and lobster pasta are phenomenal. Terrace tables overlook the moonlit sea. Book well in advance. ~€120-160 for two with wine pairing. This is your big splurge dinner." }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Isola Bella & Beach Romance",
      neighborhoods: "Mazzarò · Isola Bella · Lido · Spisone Beach",
      date: "Jun 19",
      mapPins: [
        { lat: 37.8485, lng: 15.2920, label: "Funivia (Cable Car) to Mazzarò", num: 1, cat: "transport", desc: "Scenic 3-minute cable car ride from Taormina center down to the beach — €3 each way" },
        { lat: 37.8478, lng: 15.2935, label: "Isola Bella", num: 2, cat: "activity", desc: "The 'Pearl of the Ionian' — a tiny island connected by a sandbar, now a nature reserve" },
        { lat: 37.8470, lng: 15.2945, label: "Mazzarò Beach", num: 3, cat: "activity", desc: "Taormina's main beach cove — crystal-clear water, pebbly shore, beach clubs" },
        { lat: 37.8420, lng: 15.3010, label: "Spisone Beach", num: 4, cat: "activity", desc: "Quieter beach south of Mazzarò — fewer tourists, more local vibe" },
        { lat: 37.8578, lng: 15.2757, label: "Castelmola", num: 5, cat: "activity", desc: "Tiny medieval village perched above Taormina — panoramic views and almond wine" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          items: [
            { icon: "☕", title: "Granita e Brioche Breakfast", text: "Start the Sicilian way: almond or pistachio granita stuffed in a warm brioche bun at Bam Bar. It sounds weird, it's life-changing. This is THE Taormina breakfast." },
            { icon: "🚡", title: "Cable Car to Mazzarò Beach", text: "Take the funivia down the cliff to Mazzarò. The 3-minute ride has views worth the €3 fare alone." },
            { icon: "🛶", title: "Kayak Tour Around Isola Bella", text: "Guided kayak tour (~2 hours, €35/person) around Isola Bella and the grottos. Paddle through sea caves, snorkel in crystal-clear coves, and see the coastline from the water. Way better than fighting for towel space on the crowded beach. Book with Taormina Outdoor." }
          ]
        },
        {
          label: "Afternoon",
          items: [
            { icon: "🏖️", title: "Beach Club Relaxation", text: "Claim two sunbeds at one of the lido beach clubs on Mazzarò (€15-25/person for beds + umbrella). Swim, read, nap, order fresh seafood and cold Moretti beer delivered to your lounger. This is the dolce far niente — the sweetness of doing nothing." },
            { icon: "🏔️", title: "Castelmola Side Trip", text: "Late afternoon, take a taxi or hike up to Castelmola (~20 min drive, 45 min walk). This tiny medieval village above Taormina has even more dramatic views. Bar Turrisi is famous for its... phallic décor (trust us, it's hilarious and charming). Try the vino alla mandorla (almond wine)." }
          ]
        },
        {
          label: "Evening",
          items: [
            { icon: "🍽️", title: "Dinner: Osteria Nero D'Avola", text: "Named after Sicily's famous red grape, this cozy osteria on a side street off Corso Umberto does honest, soulful Sicilian cooking. Caponata, swordfish involtini, and the pasta alla Norma is textbook perfect. Great wine list, warm service, ~€70-90 for two." }
          ]
        }
      ]
    },
    {
      num: 4,
      title: "Sicilian Cooking, Gorge Walk & Giardini Naxos",
      neighborhoods: "Alcantara Gorge · Hillside Farm · Giardini Naxos · Taormina",
      date: "Jun 20",
      mapPins: [
        { lat: 37.8779, lng: 15.1764, label: "Gole dell'Alcantara (Alcantara Gorge)", num: 1, cat: "activity", desc: "Dramatic basalt canyon carved by river and volcanic lava — wade through the gorge" },
        { lat: 37.8200, lng: 15.2500, label: "Cooking Class (Hillside Farm)", num: 2, cat: "food", desc: "Hands-on Sicilian cooking with local ingredients — pasta, caponata, cannoli" },
        { lat: 37.8353, lng: 15.2750, label: "Giardini Naxos", num: 3, cat: "activity", desc: "Seaside town below Taormina — long sandy beach and the first Greek colony in Sicily" },
        { lat: 37.8523, lng: 15.2884, label: "Taormina Centro", num: 4, cat: "activity", desc: "Return to the hilltop for your final evening" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          items: [
            { icon: "🏞️", title: "Alcantara Gorge Adventure", text: "Drive 30 min to the Gole dell'Alcantara — a volcanic basalt canyon where you wade through waist-deep river water between towering hexagonal rock columns. It's dramatic, refreshing, and unlike anything else in Sicily. €13 entry + elevator down. Bring water shoes or rent them (€5). Go early before tour buses arrive." }
          ]
        },
        {
          label: "Afternoon",
          items: [
            { icon: "👨‍🍳", title: "Sicilian Cooking Class", text: "Hands-on class at a hillside farm between Taormina and Etna. You'll visit the garden, pick herbs and vegetables, then cook a full Sicilian meal together: handmade busiate pasta, caponata, and cannoli. Then eat everything you made with local wine on a terrace overlooking the valley. ~€80-100/person, 3-4 hours. Book via Cooking with the Duchess or a similar local outfit. This is a highlight — learning to cook together is peak romance." }
          ]
        },
        {
          label: "Evening",
          items: [
            { icon: "🌅", title: "Sunset Walk in Giardini Naxos", text: "The long sandy beach below Taormina has a completely different vibe — more local, more relaxed. Walk the lungomare (seafront promenade) as the sun sets behind Taormina's cliffs above you." },
            { icon: "🍽️", title: "Dinner: Trattoria da Nino", text: "No-frills, incredible-food trattoria in Giardini Naxos. Family-run, paper tablecloths, the freshest seafood in town. Fritto misto, grilled catch of the day, and the house white. ~€50-70 for two. The kind of meal you'll talk about for years." }
          ]
        }
      ]
    },
    {
      num: 5,
      title: "Last Morning & Arrivederci",
      neighborhoods: "Taormina · Villa Comunale · Catania",
      date: "Jun 21",
      mapPins: [
        { lat: 37.8506, lng: 15.2877, label: "Villa Comunale (Public Garden)", num: 1, cat: "activity", desc: "Victorian-era garden with exotic plants, folly towers, and Etna views — serene morning spot" },
        { lat: 37.8523, lng: 15.2850, label: "Via Bagnoli Croce", num: 2, cat: "activity", desc: "Quiet residential street with art galleries and one last espresso" },
        { lat: 37.8530, lng: 15.2870, label: "Porta Catania", num: 3, cat: "activity", desc: "Southern gate — last photo spot with Etna framed in the archway" },
        { lat: 37.4668, lng: 15.0664, label: "Catania Airport (CTA)", num: 4, cat: "transport", desc: "Departure — 1 hour from Taormina" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          items: [
            { icon: "☕", title: "Last Granita Ritual", text: "One more almond granita e brioche. You know the drill. This time try pistachio if you haven't — the Bronte pistachio granita is electric green and insanely good." },
            { icon: "🌿", title: "Villa Comunale Gardens", text: "Taormina's public garden is a hidden gem — lush Victorian-era plantings, whimsical stone follies, and peaceful benches overlooking the sea. It's quiet in the morning and perfect for a romantic last stroll." },
            { icon: "🛍️", title: "Last Stroll & Shopping", text: "Pick up ceramics, limoncello, pistachio cream, or Sicilian olive oil on Corso Umberto. The hand-painted Teste di Moro (Moor's head planters) make stunning souvenirs if you can fit them in your luggage." }
          ]
        },
        {
          label: "Afternoon",
          items: [
            { icon: "✈️", title: "Transfer to Catania Airport", text: "Pre-booked transfer back to CTA (~€70, 1 hour). One last look at the coast as you descend from Taormina. Arrivederci, Sicily — you'll be back." }
          ]
        }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData);
