const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771529362699_gpk7tc",
  email: "bernard.j.huang@gmail.com",
  destination: "Lisbon, Portugal",
  start_date: "2026-07-01",
  end_date: "2026-07-07",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "nature",
  amount: "0.00",
  timestamp: "2026-02-19T19:29:22.699Z",
  status: "pending"
};

const itineraryData = {
  destination: "Lisbon, Portugal",
  countryEmoji: "🇵🇹",
  title: "Lisbon in 6 Nights: Atlantic Cliffs, Secret Gardens & Golden Light",
  subtitle: "Alfama → Sintra → Arrábida → Comporta → Belém → Bairro Alto",
  description: "A couple's guide to Lisbon and its wild Atlantic surroundings in early July — golden hour that lasts forever, cliff-top trails above crashing waves, cork oak forests, hidden beaches, and the kind of light that makes everything look like a painting. This itinerary leans hard into nature: Sintra's enchanted forests, Arrábida's turquoise coves, Comporta's rice paddies and dunes, plus Lisbon's own secret gardens and miradouros.",
  duration: "6 nights / 7 days",
  dates: "Jul 1 – 7, 2026",
  budget: "Moderate",
  pace: "Relaxed — mornings in nature, afternoons exploring, golden hour everything",
  bestFor: "Couples, nature lovers & sunset chasers",
  highlights: [
    "Sintra — enchanted palaces hidden in misty mountain forests",
    "Arrábida Natural Park — turquoise coves and cliff-top trails",
    "Comporta — pristine dunes, rice fields & barefoot beach restaurants",
    "Alfama — labyrinthine medieval streets and fado at sunset",
    "Miradouros — Lisbon's rooftop viewpoints over terracotta and the Tagus",
    "Monsanto Forest Park — 900-hectare urban forest overlooking the city",
    "Belém — Jerónimos Monastery, Torre de Belém & pastel de nata",
    "Jardim Botânico — lush 150-year-old botanical garden",
    "Costa da Caparica — endless Atlantic beach south of the city",
    "Bairro Alto — cobblestone nightlife and rooftop cocktails"
  ],
  essentials: [
    { title: "🚗 Getting Around", text: "Lisbon's center is walkable but hilly — wear good shoes. Tram 28 is iconic but packed; take it early morning or skip for Uber (cheap, €5-8 across town). For Sintra, Arrábida, and Comporta day trips, rent a car — public transit works for Sintra (40-min train from Rossio) but a car gives you freedom for coastal stops. Bolt and Uber are everywhere." },
    { title: "☀️ July Weather", text: "Expect 28-33°C (82-91°F) with zero rain and intense sunshine. Coastal areas are 3-5°C cooler with Atlantic breezes. Evenings cool to 20°C — perfect for outdoor dining. Sunset around 9pm means epic golden hours. Sunscreen, hat, and water bottle are essential. The UV at Lisbon's latitude is serious." },
    { title: "💵 Budget Tips", text: "Lisbon is one of Western Europe's best-value capitals. Expect €8-15 for casual lunches, €25-45pp for nice dinners. Wine is absurdly cheap — €3-5 for excellent glasses, €8-15 for great bottles at restaurants. Ginjinha (cherry liqueur) shots are €1-2 at street windows. Many miradouros and parks are free." },
    { title: "🏨 Where to Stay", text: "Alfama for old-world charm and proximity to miradouros. Príncipe Real for upscale boutique vibes and the botanical garden. Chiado for central location between Bairro Alto nightlife and Baixa. Santos/Cais do Sodré for riverside energy. Avoid Baixa — it's the most touristic and least charming." },
    { title: "🍷 Food & Wine", text: "Portuguese cuisine is underrated. Must-tries: pastel de nata (custard tart), bacalhau (salt cod — hundreds of preparations), arroz de marisco (seafood rice), bifana (pork sandwich), and fresh grilled fish. Vinho verde (green wine) is perfect for summer. Lisbon's food scene has exploded — Time Out Market is great for variety, but seek out local tascas (taverns) for the real experience." },
    { title: "📱 Useful Apps", text: "Bolt (rideshare, cheaper than Uber), Google Maps (works great for transit), Resy/TheFork (restaurant reservations), Zomato (local restaurant reviews), CP (train schedules for Sintra/Cascais lines)." }
  ],
  days: [
    {
      num: 1,
      title: "Alfama, Miradouros & Secret Gardens",
      neighborhoods: "Alfama · Graça · Mouraria",
      date: "Jul 1",
      mapPins: [
        { lat: 38.7139, lng: -9.1334, label: "Miradouro da Graça", num: 1, cat: "activity", desc: "Panoramic terrace over the city and Tagus" },
        { lat: 38.7119, lng: -9.1300, label: "Castelo de São Jorge", num: 2, cat: "activity", desc: "Moorish castle with peacocks and panoramic views" },
        { lat: 38.7103, lng: -9.1289, label: "Alfama", num: 3, cat: "activity", desc: "Medieval labyrinth of cobblestone streets" },
        { lat: 38.7146, lng: -9.1327, label: "Miradouro da Senhora do Monte", num: 4, cat: "activity", desc: "Highest viewpoint — locals' secret sunset spot" },
        { lat: 38.7069, lng: -9.1367, label: "Jardim Botânico", num: 5, cat: "activity", desc: "150-year-old botanical garden, shaded paths" },
        { lat: 38.7098, lng: -9.1364, label: "Portas do Sol", num: 6, cat: "activity", desc: "Classic Alfama viewpoint with terrace bar" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Miradouro da Graça & Senhora do Monte", description: "Start at Miradouro da Graça — a pine-shaded terrace with sweeping views over the castle, the river, and the bridge. Then walk five minutes uphill to Miradouro da Senhora do Monte — Lisbon's highest viewpoint. Fewer tourists, wider panorama, and a quiet garden feel. In July, the morning light turns the terracotta rooftops amber.", details: ["📍 Largo da Graça → Rua da Senhora do Monte · Both free, always open", "💡 Senhora do Monte is where locals go for sunset — come back in the evening if you want the full golden-hour experience."] },
            { title: "Alfama Wander", description: "Descend into Alfama — Lisbon's oldest neighborhood, a medieval labyrinth of narrow alleys, tiled facades, and hidden courtyards. Get deliberately lost. Every turn reveals a new doorway, laundry line, or tiny square with a gnarled tree. Listen for fado drifting from open windows. This is the soul of Lisbon.", details: ["💡 Alfama is best explored without a map. Start high (at the castle) and drift downhill — you'll always end up at the river."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Dear Breakfast", description: "Light-filled café near Graça with a terrace overlooking the city. Excellent eggs, açaí bowls, and some of the best coffee in Lisbon. A calm, beautiful start before the heat kicks in.", meta: "€10-16pp · Rua Gomes Freire 1 · Walk-in or reserve" }
          ],
          tips: [{ type: "tip", text: "July mornings in Lisbon are perfect — warm but not yet hot, with soft golden light. Do your outdoor exploring before 1pm, then find shade or air conditioning for the hottest hours." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Castelo de São Jorge", description: "Explore the Castelo de São Jorge — a Moorish castle perched above Alfama with massive stone walls, wandering peacocks, and 360° views over Lisbon. The archaeological site beneath the castle reveals layers of Phoenician, Roman, and Islamic history. The castle gardens are shaded by ancient pines — a cool retreat on a July afternoon.", details: ["📍 Rua de Santa Cruz do Castelo · €15 adults · Book timed-entry online to skip lines", "💡 The best views are from the outer ramparts on the north side — you can see all the way to Sintra on a clear day."] },
            { title: "Jardim Botânico", description: "Walk downhill to the Jardim Botânico — a lush 150-year-old botanical garden hidden behind the university. Massive fig trees, tropical palms, butterfly garden, and winding shaded paths. It feels like a secret forest in the middle of the city. One of Lisbon's most underrated nature escapes.", details: ["📍 Rua da Escola Politécnica 56 · €3 · Open daily", "💡 The garden is terraced — enter from the top (Príncipe Real side) and walk down through layers of greenery. The butterfly house is magical."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Taberna da Rua das Flores", description: "Tiny, award-winning tasca on one of Lisbon's prettiest streets. No menu — the chef tells you what's fresh. Cured meats, tinned fish (elevated to art form), seasonal plates, and incredible Portuguese wines by the glass. Authentic, unpretentious, and unforgettable.", meta: "€20-30pp · Rua das Flores 103 · No reservations, arrive by 12:30 or wait" }
          ],
          tips: [{ type: "reddit", text: "Taberna da Rua das Flores is the meal people remember from Lisbon. No menu, just trust. The tinned fish is not what you think — these are €8-15 artisan conservas that are genuinely mind-blowing.", cite: "r/lisbon" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset at Portas do Sol", description: "Catch sunset from Miradouro das Portas do Sol — a classic Alfama viewpoint with a terrace bar. The Tagus turns gold, the ferries glow, and the São Vicente church towers catch the last light. Order a glass of vinho verde and watch the city shift from day to night.", details: ["💡 For a less crowded sunset, try Miradouro de Santa Luzia next door — bougainvillea-draped terrace with azulejo tile panels."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Belcanto", description: "José Avillez's two-Michelin-star restaurant in Chiado. Modern Portuguese tasting menu that tells the story of the country through food. The 'Garden of the Goose that Laid the Golden Eggs' dessert is legendary. Splurge-worthy for a first night in Lisbon.", meta: "€120-160pp · Rua Serpa Pinto 10A · Reserve weeks ahead" }
          ],
          tips: [{ type: "reddit", text: "If Belcanto is too pricey or booked, Avillez's Bairro do Avillez next door has multiple concepts at different price points — all excellent.", cite: "r/lisbon" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Fado in Alfama", description: "End the night with fado — Portugal's soulful, melancholic music. In Alfama, fado isn't a performance; it's a way of life. Tasca do Chico (tiny, standing room, amateur fado nights) or Mesa de Frades (more refined, in a former chapel) for the real thing. The music will give you chills.", details: ["💡 Tasca do Chico Alfama: arrive by 8pm for a seat. No cover but order food/drinks. Amateur nights (Mon/Wed) are the most raw and beautiful."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Sintra: Enchanted Forests & Mountain Palaces",
      neighborhoods: "Sintra · Cabo da Roca · Colares",
      date: "Jul 2",
      mapPins: [
        { lat: 38.7876, lng: -9.3907, label: "Quinta da Regaleira", num: 1, cat: "activity", desc: "Gothic palace with underground tunnels and initiation well" },
        { lat: 38.7876, lng: -9.3907, label: "Pena Palace", num: 2, cat: "activity", desc: "Colorful Romanticist palace in the clouds" },
        { lat: 38.7953, lng: -9.4255, label: "Park of Pena", num: 3, cat: "activity", desc: "500-acre forest with exotic trees and hidden trails" },
        { lat: 38.7810, lng: -9.4994, label: "Cabo da Roca", num: 4, cat: "activity", desc: "Westernmost point of mainland Europe — dramatic cliffs" },
        { lat: 38.7974, lng: -9.4621, label: "Praia da Ursa", num: 5, cat: "activity", desc: "Wild, hidden beach with sea stacks" },
        { lat: 38.8002, lng: -9.4472, label: "Colares", num: 6, cat: "food", desc: "Wine village at Sintra's edge" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Quinta da Regaleira", description: "Arrive early at Quinta da Regaleira — a Gothic-meets-mystical estate with underground tunnels, an initiation well that spirals 27 meters into the earth, grottoes behind waterfalls, and gardens that feel like a fairy tale. The initiation well is the icon, but the surrounding gardens — dense, mossy, dripping with ferns — are where the magic really lives. In July, the canopy keeps it cool.", details: ["📍 Rua Barbosa du Bocage · €10 · Open 9:30am · ARRIVE AT OPENING — it gets mobbed by 11am", "💡 Explore the tunnels that connect the well to the lake grotto. Bring a small flashlight. The tunnels are damp and atmospheric."] },
            { title: "Park of Pena", description: "Drive up to the Park of Pena — a 500-acre enchanted forest surrounding Pena Palace. Sequoias, tree ferns from Australia, camellias, and 500+ plant species from every Portuguese colony. The trails wind through dense forest with occasional breaks revealing sweeping Atlantic views. Skip the palace interior (crowded) — the park and exterior views are the real prize.", details: ["📍 Estrada da Pena · €14 park only, €20 park + palace · Car park fills by 10am — arrive early", "💡 The Cruz Alta viewpoint in the park is 528m above sea level — on a clear day, you can see Lisbon and the Atlantic simultaneously."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Fabrica das Verdadeiras Queijadas da Sapa", description: "Sintra's legendary pastry shop since 1756. The queijadas (tiny cheese tarts) and travesseiros (almond pastry pillows) are the reason to come. Grab a box, sit on the bench outside, and fuel up before exploring.", meta: "€3-6 · Volta do Duche 12, Sintra · Cash" }
          ],
          tips: [{ type: "tip", text: "Sintra is 10-15°F cooler than Lisbon — the mountain forests create a microclimate. Bring a light layer. The mist that rolls through the trees is part of the magic." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Cabo da Roca", description: "Drive west to Cabo da Roca — the westernmost point of mainland Europe. Dramatic sea cliffs plunge into the Atlantic, a lonely lighthouse stands at the edge, and the wind is fierce and wild. The poet Camões called it 'where the land ends and the sea begins.' Stand at the cliff edge and feel the scale of the Atlantic stretching toward America.", details: ["📍 Estrada do Cabo da Roca · Free · 20 min drive from Sintra", "💡 Walk south along the cliff path (away from the crowds at the lighthouse) for wilder, emptier views. Wildflowers bloom along the cliffs in July."] },
            { title: "Praia da Ursa (optional hike)", description: "For the adventurous: Praia da Ursa is a wild, hidden beach accessible only by a steep 20-minute scramble down a cliff trail. Massive sea stacks, no facilities, no crowds — just raw Atlantic coastline. The formations look like something from another planet. Only attempt in good conditions; the trail is steep and sandy.", details: ["📍 Park at the trailhead on N247, between Cabo da Roca and Praia da Adraga · Free", "💡 Bring water, wear sturdy shoes. The climb back up is the hard part. Start before 3pm to avoid the worst heat."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Restaurante Colares Velho", description: "Traditional Portuguese restaurant in the wine village of Colares, nestled in Sintra's foothills. Grilled fish, homestyle cataplana (copper-pot seafood stew), and local Colares wine — one of the rarest wine regions in the world (ungrafted vines from pre-phylloxera rootstock). Shaded garden terrace.", meta: "€18-28pp · Colares · Walk-in, relaxed" }
          ],
          tips: [{ type: "reddit", text: "Praia da Ursa is one of the most beautiful beaches in Europe and almost nobody goes because of the sketchy trail down. If you're reasonably fit, do it. The sea stacks at sunset are insane.", cite: "r/portugal" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset Drive Along the Coast", description: "Drive the N247 coastal road from Cabo da Roca south through Guincho and Cascais. The road hugs Atlantic cliffs with constant ocean views. Stop at Praia do Guincho — a windswept beach where surfers ride powerful waves and the sun sets directly into the ocean. In July, the sunset light along this stretch is extraordinary.", details: ["💡 Guincho is famous for its wind — stunning to watch but bring a windbreaker if you walk on the beach."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Furnas do Guincho", description: "Dramatic cliffside restaurant built into natural sea caves on the Guincho coast. Fresh grilled seafood, ocean views from every table, and waves crashing against the rocks below. The arroz de marisco (seafood rice) feeds two and is spectacular. One of the most memorable dinner settings near Lisbon.", meta: "€35-50pp · Estrada do Guincho · Reserve ahead in summer" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Return to Lisbon", description: "Drive back to Lisbon along the coast (40 minutes). The city lights reflecting on the Tagus as you cross the bridge are a beautiful welcome home.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Arrábida: Turquoise Coves & Cliff Trails",
      neighborhoods: "Serra da Arrábida · Setúbal · Sesimbra",
      date: "Jul 3",
      mapPins: [
        { lat: 38.4784, lng: -8.9750, label: "Praia de Galapinhos", num: 1, cat: "activity", desc: "Hidden turquoise cove — one of Europe's best beaches" },
        { lat: 38.4820, lng: -9.0010, label: "Praia de Creiros", num: 2, cat: "activity", desc: "Secluded beach backed by aromatic scrubland" },
        { lat: 38.4953, lng: -8.9275, label: "Setúbal", num: 3, cat: "food", desc: "Fishing town famous for fresh grilled fish" },
        { lat: 38.4850, lng: -8.9600, label: "Serra da Arrábida Trail", num: 4, cat: "activity", desc: "Cliff-top trail with Atlantic panoramas" },
        { lat: 38.4737, lng: -9.0247, label: "Portinho da Arrábida", num: 5, cat: "activity", desc: "Tiny harbor with crystalline water" },
        { lat: 38.4440, lng: -9.1040, label: "Sesimbra", num: 6, cat: "food", desc: "Charming fishing village with castle above" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Arrábida", description: "Drive 40 minutes south across the Vasco da Gama Bridge to the Serra da Arrábida — a limestone mountain range that plunges into the Atlantic, creating turquoise coves that look like the Mediterranean but with Atlantic power. The Arrábida Natural Park protects 10,800 hectares of Mediterranean scrubland, aromatic herbs, and hidden beaches. In July, the water is warm enough to swim and the air smells of rosemary and pine.", details: ["📍 Take the A2 south, exit toward Azeitão, then follow signs to Arrábida. 40-50 min from Lisbon.", "💡 In July, beach roads close to cars on weekends. Go on a weekday, or arrive before 9am on weekends. Park at the upper lots and walk down."] },
            { title: "Praia de Galapinhos", description: "Hike down to Praia de Galapinhos — voted one of Europe's best beaches. A crescent of white sand between limestone cliffs, with water so turquoise it looks photoshopped. The 15-minute trail down through aromatic scrubland is part of the experience. Bring snorkeling gear — the water clarity is exceptional and the rocky edges harbor sea life.", details: ["📍 Park at the upper car park on the Arrábida road · 15-min downhill walk", "💡 No facilities, no shade (except cliff shadows in afternoon). Bring water, umbrella, snacks. The beach is small and fills by noon in summer."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Pick up pastries in Azeitão", description: "Stop in the village of Azeitão on the way to Arrábida. Grab tortas de Azeitão (rolled pastry with egg cream) from any bakery — they're a regional specialty you won't find elsewhere. Excellent coffee too.", meta: "€4-8 · Various bakeries on the main road · Quick stop" }
          ],
          tips: [{ type: "reddit", text: "Galapinhos is worth the hype. The water color is unreal. But go EARLY — by noon it's packed and there's no shade. Bring everything you need because there's zero infrastructure.", cite: "r/portugal" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Arrábida Cliff Trail", description: "Hike a section of the Trilho da Arrábida — a cliff-top trail with vertiginous views over the coves and the Atlantic. The trail runs along the ridge through Mediterranean scrubland — rosemary, wild lavender, and cistus release their scents in the July heat. Views of the Troia peninsula and the open ocean are constant. Pick a 2-3 hour section based on energy.", details: ["📍 Multiple trailheads along the Arrábida road · AllTrails has the best mapped routes", "💡 Start from Portinho da Arrábida and hike west for the best cliff views. Bring 2L of water per person — no shade on the ridge. Morning or late afternoon for comfort."] },
            { title: "Portinho da Arrábida", description: "Cool off at Portinho da Arrábida — a tiny harbor with crystalline water, a few fishing boats, and a small fort above. The water here is sheltered and calm — perfect for a post-hike swim. A tiny beach bar serves cold beer and snacks.", details: ["💡 The Forte de Santa Maria above the harbor sometimes hosts exhibitions. The views from the fort walls are gorgeous."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Restaurante Gaivota, Portinho", description: "Simple seafood restaurant overlooking the harbor at Portinho. Grilled fresh fish, fried squid, and salad — nothing fancy, everything fresh. The view and the simplicity are the point. Cold Sagres beer, sun on your face, feet still sandy.", meta: "€15-25pp · Portinho da Arrábida · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Arrábida's water is dramatically warmer than Lisbon's Atlantic coast — the south-facing coves are sheltered from cold northern currents. July water temps hit 20-22°C, which feels glorious after the trail." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Setúbal Waterfront", description: "Drive east to Setúbal — a working fishing town with a gorgeous waterfront, lively mercado (market), and Portugal's freshest grilled fish. The town is real, not touristy, and the energy is warm and local. Walk along the Avenida Luísa Todi waterfront as the fishing boats come in.", details: ["💡 Setúbal is famous for choco frito — fried cuttlefish. It's the town's signature dish and you'll find it at every restaurant."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Casa Santiago", description: "The most famous choco frito in Portugal. This no-frills Setúbal institution serves battered, fried cuttlefish that is crispy, tender, and utterly addictive. Paired with local Moscatel wine (sweet, fortified) and a simple salad. There will be a line. It's worth it.", meta: "€12-20pp · Av. Luísa Todi 594, Setúbal · No reservations, expect a queue" }
          ],
          tips: [{ type: "reddit", text: "Casa Santiago choco frito is a religious experience. Get the large plate to share plus bread with butter. The Moscatel de Setúbal dessert wine is incredible and costs like €3 a glass.", cite: "r/portugal" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Return via the Bridge", description: "Drive back to Lisbon over the Vasco da Gama Bridge — at 17km, the longest bridge in Europe. At night, the bridge lights reflect on the Tagus estuary. A beautiful end to a nature-filled day.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Comporta: Dunes, Rice Fields & Barefoot Luxury",
      neighborhoods: "Comporta · Carvalhal · Troia Peninsula",
      date: "Jul 4",
      mapPins: [
        { lat: 38.3780, lng: -8.7850, label: "Comporta Beach", num: 1, cat: "activity", desc: "Endless white sand backed by rice paddies and pine forests" },
        { lat: 38.3640, lng: -8.7760, label: "Carvalhal Beach", num: 2, cat: "activity", desc: "Wilder beach with dune trails" },
        { lat: 38.3900, lng: -8.7600, label: "Rice Paddies", num: 3, cat: "activity", desc: "Stork-filled wetlands and emerald green fields" },
        { lat: 38.3720, lng: -8.7950, label: "Comporta Village", num: 4, cat: "food", desc: "Tiny village with design shops and cafés" },
        { lat: 38.4900, lng: -8.9000, label: "Troia Peninsula", num: 5, cat: "activity", desc: "Wild sand spit with dolphins in the estuary" },
        { lat: 38.3550, lng: -8.7680, label: "Pego Beach", num: 6, cat: "activity", desc: "Remote, pristine — nature at its purest" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Comporta", description: "Drive 90 minutes south to Comporta — Portugal's answer to the Hamptons, but wilder and less developed. The landscape shifts dramatically: rice paddies stretching to the horizon, white storks nesting on power lines, umbrella pines, and then — endless white-sand beach backed by dunes. Comporta has become a discreet retreat for European creatives and celebrities, but it still feels beautifully untouched.", details: ["📍 Take A2 south, then N253 toward Comporta. 80-90 min from Lisbon.", "💡 The drive through the rice paddies is stunning — stop to photograph the storks and the vast green-and-water landscape."] },
            { title: "Comporta Beach Morning", description: "Set up on Comporta Beach — a vast, pristine stretch of white sand with gentle Atlantic waves. The beach is backed by dunes and pine forest, and you can walk for miles without seeing another person. In July, the water is refreshing (19-21°C) and the sand is warm. Beach restaurants (chiringuitos) dot the dunes — barefoot, sand-floor, amazing fresh seafood.", details: ["💡 Beach parking is along sandy tracks through the dunes. Follow signs to 'Praia da Comporta.' Arrive before 11am for easy parking."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Café da Praia, Comporta", description: "Laid-back beach café with sand-floor terrace under pine trees. Fresh juices, tostas, and strong espresso. The vibe is barefoot and unhurried — exactly the Comporta energy.", meta: "€8-12pp · Near the beach entrance · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Comporta is Portugal's 'secret' coastal retreat — fashion editors, architects, and artists come for the simplicity. The aesthetic is 'rich but wearing flip-flops.' Don't overdress; do bring good sunscreen." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rice Paddy Walk & Birdwatching", description: "Walk or drive through the Herdade da Comporta rice paddies. In July, the fields are vivid emerald green, reflecting the sky like mirrors. White storks nest everywhere, and you may spot herons, egrets, and harriers. The landscape is flat, vast, and hypnotic — a complete contrast to Lisbon's urban hills.", details: ["💡 The rice paddies are private land but the roads through them are public. Drive slowly, stop at pull-offs, and bring binoculars for the birdlife."] },
            { title: "Carvalhal & Pego Beaches", description: "Explore south to the wilder beaches — Carvalhal and Pego. Less developed, more dunes, bigger sky. Carvalhal has a legendary beach restaurant; Pego is raw and pristine. Walk the dune trails connecting the beaches through maritime pine forest. The scent of warm pine resin and salt air is intoxicating.", details: ["💡 Pego Beach is the most remote — a 10-minute walk through dunes from parking. Almost always uncrowded, even in peak July."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Sal, Comporta", description: "The iconic Comporta beach restaurant. Sand floor, driftwood furniture, fish grilling over open flames. The catch of the day, grilled simply with olive oil, sea salt, and lemon, is perfect. Pair with vinho verde and listen to the waves. This is the Comporta experience distilled.", meta: "€25-40pp · Praia da Comporta · Reserve in summer" }
          ],
          tips: [{ type: "reddit", text: "Sal in Comporta is one of the best meals you'll have in Portugal — not because it's fancy, but because it's the freshest grilled fish, on the beach, with your feet in the sand. Book ahead in July.", cite: "r/portugal" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Comporta Sunset & Drive Back", description: "Stay for sunset on the beach — Comporta faces west, so the sun drops directly into the Atlantic. The sky turns pink, orange, and purple over the empty dunes. It's one of Portugal's most beautiful sunsets. Then drive back to Lisbon under the stars.", details: ["💡 Stop in Alcácer do Sal on the way back — a hilltop town over the Sado river, beautiful at dusk."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Cavalariça, Comporta", description: "Upscale but relaxed restaurant in a converted horse stable. Wood-fired meats, seasonal vegetables from local farms, and an excellent Portuguese wine list. Candlelit garden terrace under cork oaks. The perfect Comporta farewell dinner.", meta: "€35-50pp · Comporta village · Reserve ahead" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Stargazing on the Drive", description: "The drive back through the Alentejo countryside is pitch-dark — stop at a pull-off and look up. With minimal light pollution, the Milky Way is visible on clear July nights. A perfect natural end to a nature day.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Belém, Monsanto Forest & River Gardens",
      neighborhoods: "Belém · Monsanto · Ajuda",
      date: "Jul 5",
      mapPins: [
        { lat: 38.6916, lng: -9.2159, label: "Torre de Belém", num: 1, cat: "activity", desc: "Iconic Manueline tower on the Tagus" },
        { lat: 38.6970, lng: -9.2064, label: "Jerónimos Monastery", num: 2, cat: "activity", desc: "Masterpiece of Manueline architecture" },
        { lat: 38.6975, lng: -9.2034, label: "Pastéis de Belém", num: 3, cat: "food", desc: "The original pastel de nata since 1837" },
        { lat: 38.7500, lng: -9.1900, label: "Monsanto Forest Park", num: 4, cat: "activity", desc: "900-hectare urban forest — Lisbon's green lung" },
        { lat: 38.6950, lng: -9.1950, label: "Jardim Botânico Tropical", num: 5, cat: "activity", desc: "Tropical garden with colonial-era plantings" },
        { lat: 38.7070, lng: -9.1870, label: "Tapada da Ajuda", num: 6, cat: "activity", desc: "Former royal hunting ground, now a nature reserve" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Monsanto Forest Park", description: "Start with nature: Monsanto Forest Park is Lisbon's 900-hectare urban forest — a wild, hilly expanse of eucalyptus, pine, and cork oak overlooking the entire city and the Tagus. Trails wind through the forest with viewpoints over Lisbon, the bridge, and the river. In July, the shade and the breeze through the canopy are heavenly. It feels remote but it's 15 minutes from downtown.", details: ["📍 Multiple entrances — Parque do Alvito is a good starting point. Free, always open.", "💡 The Panorâmico de Monsanto is an abandoned hilltop restaurant covered in street art — it's been fenced off but you can see it from the road. The viewpoints near it are spectacular."] },
            { title: "Tapada da Ajuda", description: "Walk through the Tapada da Ajuda — a 100-hectare former royal hunting ground, now a nature reserve and agricultural campus. Deer, peacocks, and hundreds of bird species live among centuries-old trees. Far fewer visitors than any Lisbon park. A genuinely wild green space.", details: ["📍 Calçada da Tapada · Small entry fee · Open weekdays + Saturday mornings", "💡 The botanical collection includes trees planted by Portuguese kings — some are over 300 years old."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Landeau Chocolate", description: "Famous for having Lisbon's best chocolate cake — a dense, fudgy, single-layer slab of pure chocolate. Paired with excellent coffee, it's an indulgent morning start. Multiple locations; the Belém one has a terrace.", meta: "€8-12pp · Multiple locations · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Monsanto is where Lisbon runners, cyclists, and nature lovers go. You'll barely see tourists. The forest trails are well-marked and range from easy walks to serious trail runs." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Belém Waterfront", description: "Head to Belém — Lisbon's monumental riverfront district. The Torre de Belém stands alone in the river, a Manueline jewel from 1519 when explorers departed for unknown worlds. The Jerónimos Monastery is one of Europe's most stunning buildings — intricate carved stone that looks like lace. Walk the waterfront promenade and feel the scale of Portugal's Age of Discovery.", details: ["📍 Torre de Belém: €10 · Jerónimos: €10 · Combined tickets available · Book timed-entry online", "💡 The Jerónimos cloisters are the highlight — two levels of carved columns, each unique. The light in the upper cloisters in afternoon is magical."] },
            { title: "Jardim Botânico Tropical", description: "Next to the monastery, the Jardim Botânico Tropical is a peaceful escape — tropical plants from former Portuguese colonies, shaded paths, and a serene lake. Dragon trees from Madeira, palms from Goa, and giant bamboo groves. A living museum of Portugal's global connections.", details: ["📍 Largo dos Jerónimos · €3 · Shaded and cool even in July heat"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Pastéis de Belém", description: "The original pastel de nata, made here since 1837 using a secret recipe from the monastery monks. The warm, just-from-the-oven tarts with a sprinkle of cinnamon and powdered sugar are transcendent. Yes, there's a line. Yes, it moves fast. Yes, it's worth it. Order at least 4.", meta: "€1.40 each · Rua de Belém 84-92 · Walk-in, eat at the counter for speed" },
            { type: "🍽️ Lunch", name: "Ponto Final", description: "Take the ferry across the Tagus to Cacilhas and walk to Ponto Final — a legendary waterfront restaurant with the best view of Lisbon across the river. Fresh grilled fish, massive portions, reasonable prices, and a view that makes you want to weep. Locals queue for this.", meta: "€15-25pp · Rua do Ginjal 72, Almada · No reservations, arrive early or wait" }
          ],
          tips: [{ type: "reddit", text: "Ponto Final across the river is the view that every Lisbon Instagram photo is shot from. But the food actually matches the view — the grilled dourada is incredible. Take the ferry from Cais do Sodré to Cacilhas.", cite: "r/lisbon" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "LX Factory & Sunset", description: "Walk to LX Factory — a creative complex in a converted textile factory under the 25 de Abril Bridge. Design shops, bookstores (Ler Devagar, one of the world's most beautiful bookshops), food stalls, and rooftop bars. The bridge towers overhead dramatically. Catch sunset from the rooftop of Rio Maravilha bar — one of Lisbon's best sunset views.", details: ["📍 Rua Rodrigues de Faria 103 · Free to enter · Open daily", "💡 Sunday brunch at LX Factory is a local institution. But the weeknight vibe is cooler and less crowded."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Prado", description: "Farm-to-table restaurant in Chiado sourcing from small Portuguese producers. Chef António Galapito's menu changes daily — expect stunning vegetable dishes, heritage breed meats, and creative use of every part. The sourdough alone is worth the visit. A wine list deep in natural and small-production Portuguese bottles.", meta: "€35-50pp · Travessa das Pedras Negras 2 · Reserve on TheFork" }
          ],
          tips: [{ type: "reddit", text: "Prado is the most exciting restaurant in Lisbon right now. António Galapito trained at Noma and it shows — but the food is deeply Portuguese. The vegetables are the star. Don't skip the bread.", cite: "r/lisbon" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Príncipe Real Gardens", description: "End with a walk through Jardim do Príncipe Real — a beautiful garden with a massive 150-year-old cedar tree whose branches form a natural canopy. In summer, the garden hosts evening markets and events. Nearby bars on Rua da Escola Politécnica are intimate and local.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 6,
      title: "Costa da Caparica & River Beach Day",
      neighborhoods: "Costa da Caparica · Fonte da Telha · Almada",
      date: "Jul 6",
      mapPins: [
        { lat: 38.6400, lng: -9.2350, label: "Costa da Caparica", num: 1, cat: "activity", desc: "30km of Atlantic beach south of the city" },
        { lat: 38.5900, lng: -9.2200, label: "Fonte da Telha", num: 2, cat: "activity", desc: "Pine-backed wild beach, local surfers" },
        { lat: 38.6350, lng: -9.2380, label: "Praia da Morena", num: 3, cat: "activity", desc: "Chill beach with great chiringuito" },
        { lat: 38.6775, lng: -9.1730, label: "Cristo Rei", num: 4, cat: "activity", desc: "Christ statue with city panorama" },
        { lat: 38.6500, lng: -9.2300, label: "Beach Train (Transpraia)", num: 5, cat: "activity", desc: "Mini-train connecting 20+ beach stops" },
        { lat: 38.6440, lng: -9.2280, label: "Praia da Saúde", num: 6, cat: "food", desc: "Lively beach with restaurant strip" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Costa da Caparica", description: "Cross the bridge to Costa da Caparica — 30 kilometers of unbroken Atlantic beach stretching south from the city. A mini-train (Transpraia) runs along the dunes, stopping at 20+ beaches — each with its own personality. The northern beaches are more lively; head south for wilder, emptier stretches. In July, the water is refreshing and the surf is rideable for beginners.", details: ["📍 Drive across the 25 de Abril Bridge or take the ferry + bus. 30-40 min from Lisbon.", "💡 The Transpraia mini-train is a delightful way to explore — hop on at the north end and ride south until you find your perfect beach. €4 round trip."] },
            { title: "Surf or Swim", description: "Caparica is Lisbon's surf coast. If you've never surfed, book a lesson — the beach breaks here are gentle and perfect for beginners. Surf schools are everywhere along the main stretch. If you prefer swimming, head to a sheltered section near one of the beach restaurants. The water in July is around 19-20°C — cold at first, then exhilarating.", details: ["💡 Surf lesson: ~€30-40/person for a 2-hour group lesson including board and wetsuit. Book at the beach — no need to reserve ahead."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Waikiki Beach Bar", description: "Right on the sand with a surf-shack vibe. Açaí bowls, fresh juices, toast with local honey. The kind of place where you eat barefoot and watch surfers while planning nothing.", meta: "€8-14pp · Praia da Caparica · Walk-in" }
          ],
          tips: [{ type: "tip", text: "The further south you go on the Caparica coast, the wilder and emptier it gets. Beaches 14-19 on the Transpraia are nudist-friendly and very uncrowded. Fonte da Telha (past the train) is a local favorite." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Fonte da Telha", description: "Walk or drive south to Fonte da Telha — a pine-forest-backed beach with a local, uncommercial feel. Fishermen still pull boats up on the sand. Small restaurants serve fried fish and cold beer. The dune trails connecting the beaches are beautiful — maritime pine forest, sandy paths, and the constant sound of waves.", details: ["💡 The pine forests behind the beaches are popular for trail running and mountain biking — bring shoes if you want to explore."] },
            { title: "Cristo Rei Viewpoint", description: "On the way back, stop at Cristo Rei — the Christ the King statue overlooking Lisbon from the south bank. The viewing platform at the base has an extraordinary panorama: the 25 de Abril Bridge, the Tagus, downtown Lisbon, the castle, Belém. In late afternoon light, it's one of the best viewpoints in the region.", details: ["📍 Av. Cristo Rei, Almada · €8 for elevator to viewing platform", "💡 The perspective from here — seeing all of Lisbon across the river at once — really shows you how the city works with its seven hills and the water."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "O Barbas", description: "Legendary beach restaurant on Caparica. The name means 'the bearded one' — named for the original owner. Massive platters of grilled fish, seafood açorda (bread-based stew), and ice-cold beer served on a terrace overlooking the waves. No pretension, just perfect beach food.", meta: "€18-30pp · Praia da Caparica · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "O Barbas is the GOAT Caparica beach restaurant. Get the mixed grilled fish platter for two — they grill whatever came in that morning. Bring cash as backup.", cite: "r/lisbon" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Bairro Alto & Final Night Out", description: "Last full night — head to Bairro Alto, Lisbon's nightlife heart. Start with a ginjinha (sour cherry liqueur) at one of the tiny street windows near Rossio. Then climb into Bairro Alto where every narrow street has a bar. The neighborhood has a block-party energy in summer — people spill out of bars onto the cobblestones, drinks in hand. End at a rooftop bar with river views.", details: ["💡 Bairro Alto bars close at 2am, then everyone migrates to Cais do Sodré (Pink Street) for clubs until dawn. But the early evening in Bairro Alto (9-midnight) is the sweet spot."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Cervejaria Ramiro", description: "Lisbon's most famous seafood restaurant — and it lives up to the hype. Tiger prawns, percebes (goose barnacles — a Portuguese obsession), garlic clams, and the legendary prego (steak sandwich) to finish. Loud, bustling, and utterly delicious. A proper Lisbon farewell feast.", meta: "€40-60pp · Av. Almirante Reis 1-H · No reservations, expect 30-60 min wait in summer — worth it" }
          ],
          tips: [{ type: "reddit", text: "Ramiro rule: start with clams and percebes, then prawns and crab. ALWAYS finish with the prego steak sandwich — it's the secret best thing on the menu. Skip dessert. Bring cash for tip.", cite: "r/lisbon" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Rooftop Farewell", description: "End on a rooftop. PARK Bar (at the top of a parking garage in Bairro Alto) has 360° views over the castle, the river, and the bridge. Order a gin and tonic (Portugal is obsessed with elaborate G&Ts) and say goodbye to Lisbon's terracotta skyline under the stars.", details: ["📍 PARK Bar: Calçada do Combro 58 (enter through the parking garage, ride elevator to top). Open 1pm-2am.", "💡 Other great rooftop options: Noobai (at Miradouro de Santa Catarina), Topo Chiado, or Sky Bar at Tivoli."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 7,
      title: "Morning Light & Departure",
      neighborhoods: "Chiado · Baixa · Príncipe Real",
      date: "Jul 7",
      mapPins: [
        { lat: 38.7103, lng: -9.1427, label: "Príncipe Real", num: 1, cat: "food", desc: "Final morning coffee under the cedar tree" },
        { lat: 38.7070, lng: -9.1400, label: "Chiado", num: 2, cat: "activity", desc: "Last stroll through Lisbon's literary quarter" },
        { lat: 38.7139, lng: -9.1394, label: "Miradouro de São Pedro de Alcântara", num: 3, cat: "activity", desc: "Final panoramic view" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Last Morning Walk", description: "Take a final morning walk through Príncipe Real and Chiado. The July morning light in Lisbon is legendary — soft, golden, and warm. Sit under the giant cedar tree in Jardim do Príncipe Real, sip one last espresso, and watch Lisbon wake up. Walk to Miradouro de São Pedro de Alcântara for a final panoramic view of the castle and the city. Breathe it in.", details: ["💡 The airport is 20 minutes from central Lisbon by Uber/Bolt. The metro also connects directly (Red line to Aeroporto). Leave 2 hours before your flight."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Copenhagen Coffee Lab", description: "Scandinavian-Portuguese hybrid café with some of Lisbon's best specialty coffee. Light pastries, clean aesthetic, and a sunny terrace on Príncipe Real. A calm, beautiful final morning.", meta: "€8-12pp · Rua Nova da Piedade 10 · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Before you leave: pick up pastel de nata from Manteigaria (they box them for travel), a bottle of Moscatel de Setúbal from any wine shop, and a tin of artisan sardines. Portuguese souvenirs that people actually love." }]
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
