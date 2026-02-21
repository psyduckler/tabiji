const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771698979560_q1hdud',
  email: 'psyduckler@gmail.com',
  destination: 'Amazon Rainforest',
  start_date: '2026-02-28',
  end_date: '2026-03-04',
  startDate: '2026-02-28',
  endDate: '2026-03-04',
  groupSize: 2,
  group_size: '2',
  amount: '0.00',
  requests: ''
};

const itineraryData = {
  destination: 'Amazon Rainforest, Brazil',
  countryEmoji: '🇧🇷',
  title: 'Into the Lungs of the Earth',
  subtitle: '5 days deep in the Brazilian Amazon — jungle lodges, pink dolphins, flooded forests & caiman nights for two',
  description: "The Amazon in late February is alive in a way that defies description. The rainy season has flooded the forest floor, turning the jungle into a labyrinth of black-water channels where you paddle your canoe beneath a cathedral of ancient trees. Pink river dolphins (botos) materialize from the depths. Spider monkeys swing overhead. Three-toed sloths peer down from cecropia branches. At night, a guide sweeps a flashlight across the water and dozens of caiman eyes glow orange from the darkness. This is Earth's greatest wilderness — rawer, louder, and more overwhelming than anything you've imagined. This itinerary begins in Manaus — the Amazon's improbable jungle city — then takes you deep into the rainforest by boat, settling into a riverside jungle lodge as your base for four days of expedition. You'll witness the famous Meeting of the Waters, fish for piranha, swim with pink dolphins, visit indigenous communities, and fall asleep to the symphony of the jungle. Return changed.",
  duration: '5 days',
  dates: 'Feb 28 – Mar 4, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Couples · Nature Lovers · Adventure Seekers',

  highlights: [
    'Meeting of the Waters — watch the black Rio Negro meet the tawny Solimões and refuse to mix for miles',
    'Flooded forest canoe tour — paddling silently through submerged jungle at water level',
    'Swimming with wild pink river dolphins (botos) in a black-water lake',
    'Night caiman safari — spotting glowing orange eyes from a motorized canoe',
    'Piranha fishing on the Amazon River — catch and release (or cook for lunch)',
    'Dawn chorus bird walk — over 1,000 species call the Amazon home',
    'Indigenous Sateré-Mawé village visit — learn about forest medicine and traditional life',
    'Giant Amazonian water lily pads (Victoria amazonica) in a flooded igapó',
    'Sleeping to the relentless, overwhelming symphony of the jungle at night',
    'Hammock under the stars at a remote Amazon wilderness camp'
  ],

  essentials: [
    {
      title: '🌧️ Rainy Season Realities',
      text: 'Late February is peak rainy season — expect daily afternoon downpours lasting 1-2 hours. This is actually GOOD: the flooded forest (igapó) is accessible only when water levels are high, enabling canoe exploration deep into the jungle. Pack dry bags, quick-dry clothes, and embrace the mud. The rain cools everything down beautifully.'
    },
    {
      title: '🦟 Insects & Health',
      text: 'Start malaria prophylactics 1-2 weeks before departure (consult a travel clinic). Use DEET 50%+ repellent on all exposed skin. Wear long sleeves and pants after sunset. Yellow fever vaccination required for entry into Amazonas state — get it at least 10 days before. The lodge will provide basic first aid; Manaus has hospitals for emergencies.'
    },
    {
      title: '✈️ Getting to Manaus',
      text: 'Fly into Eduardo Gomes International Airport (MAO), Manaus — gateway to the Brazilian Amazon. Direct flights from São Paulo (4h), Rio de Janeiro (4h30), and Miami. Most lodges include airport pickup as part of their packages. Book your lodge transfer in advance and confirm your arrival time.'
    },
    {
      title: '🏡 Choosing Your Lodge',
      text: 'Your lodge is your world for 4 nights. We recommend Amazon Ecopark Jungle Lodge or Juma Lodge for first-timers — both are within 2-3 hours of Manaus by boat, offer all-inclusive packages (meals + guided excursions), have comfortable bungalows with nets, and have expert English-speaking naturalist guides. Book the all-inclusive program — it\'s worth every real.'
    },
    {
      title: '💰 Money & Budget',
      text: 'Most jungle lodges are all-inclusive (transfers, meals, excursions). Budget separately for: airport meals in Manaus (~R$80-150/meal), souvenirs at the city market, tips for guides (R$50-100/day per guide is generous and appreciated — these guides are extraordinary people). Exchange USD/EUR to BRL in Manaus or use Wise/Revolut cards. ATMs widely available in Manaus, but bring cash to the lodge.'
    },
    {
      title: '🎒 What to Pack',
      text: 'Quick-dry clothing (2-3 sets), rain jacket, rubber boots (usually provided by lodge), dry bags for electronics, strong insect repellent, sunscreen, headlamp + spare batteries, binoculars (game-changer for wildlife), waterproof camera or phone case, hand sanitizer. Pack light — you\'ll wear the same 3 outfits in the jungle and nobody cares.'
    }
  ],

  days: [
    // ========== DAY 1 ==========
    {
      num: 1,
      date: '2026-02-28',
      neighborhoods: 'Manaus · Meeting of the Waters · Rio Negro',
      title: 'Arrival in Manaus — Meeting of the Waters',
      description: "Land in Manaus — a city of 2 million that somehow exists in the middle of the world's greatest jungle. After checking in and a quick city orientation, take an afternoon boat tour to witness one of nature's most extraordinary phenomena: the Meeting of the Waters, where the dark Rio Negro flows alongside the tawny Solimões River for 6 kilometers without mixing. Then celebrate your Amazon arrival with a riverside dinner watching the sun bleed into the jungle horizon.",
      timeBlocks: [
        {
          label: 'Morning & Arrival',
          activities: [
            {
              title: 'Arrive at Manaus Airport (MAO) & Transfer',
              description: "Touch down at Eduardo Gomes International Airport and feel the wall of heat and humidity the moment you step outside — welcome to the equatorial rainforest. Your lodge transfer driver will be waiting. If arriving early, drop bags at your hotel and walk around the historic center.",
              details: [
                '✈️ Most connecting flights arrive via São Paulo (GRU) or Brasília (BSB)',
                '🌡️ Temperature ~30-32°C (86-90°F) year-round with high humidity',
                '🏨 Stay at Hotel Amazonas or similar in the city center for night 1 before heading to the lodge tomorrow',
                '💵 Exchange cash at the airport — better rates than the city center banks'
              ]
            },
            {
              title: 'Manaus Historic Center Walk',
              description: "Manaus is a surprisingly elegant city built on rubber boom wealth. The centerpiece is the opulent Teatro Amazonas opera house — an improbable pink-domed masterpiece completed in 1896, furnished with European crystal chandeliers and Venetian glass. Wander the neoclassical streets, visit the bustling Mercado Adolpho Lisboa (a cast-iron market modeled on Les Halles in Paris), and get your first taste of Amazonian fruit juices — cupuaçu, açaí, camu camu.",
              details: [
                '🎭 Teatro Amazonas: guided tour R$40 · Mon-Sat 10am-4pm',
                '🏛️ Mercado Adolpho Lisboa: open Mon-Sat 6am-5pm — excellent açaí, fruits, and dried fish',
                '🍹 Try fresh cupuaçu juice — rich, tangy, unique to the Amazon. Nothing else tastes like it.',
                '📸 The market\'s cast-iron architecture is stunning — modeled on Les Halles, Paris'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Choupana Flutuante',
              description: "A floating restaurant on the Rio Negro serving fresh Amazonian fish. Order tucunaré (peacock bass) grilled with manioc and herbs, or tambaqui ribs — the \"rib-eye of the Amazon,\" grilled over charcoal with lime and tucupi sauce. This is the freshest river fish you'll ever eat.",
              meta: '💰 $$ · 📍 Ponta Negra Beach, Manaus · Best at lunch'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Meeting of the Waters (Encontro das Águas) Boat Tour',
              description: "This is one of the great natural wonders of the world. The dark, acidic, slow-moving Rio Negro (deep black as black tea, 28°C/82°F) collides with the sandy-beige, fast-moving, sediment-rich Solimões River (lighter brown, 22°C/72°F) — and for 6 kilometers, they refuse to mix. Different temperatures, different speeds, different densities. The boundary line between the two rivers is razor-sharp: lean over the boat and you can touch black water with one hand and brown with the other. Tour boats head out daily and the sight never gets old.",
              details: [
                '🚢 Tours depart from Porto de Manaus · Approx 3-4 hours · R$80-120pp',
                '🐬 Pink river dolphins (botos) frequently surface at the confluence',
                '📸 Bring a polarized lens filter if you can — the color contrast is extraordinary',
                '🌊 The two rivers flow side by side for 6km before fully mixing — visible from the air on Google Maps'
              ]
            },
            {
              title: 'MUSA — Museu da Amazônia (Amazon Forest Tower)',
              description: "If time allows before your boat tour, visit MUSA's extraordinary forest canopy walkway: a 42-meter steel tower rising above the jungle canopy, with spiral walkways that put you eye-level with toucans, parrots, and tree frogs. From the top, you see nothing but unbroken jungle to every horizon — the scale of the Amazon finally hits home.",
              details: [
                '🌿 MUSA Tower: R$45 · Open Tue-Sun 9am-4pm',
                '🦜 Canopy level: best birdwatching in the Manaus area',
                '📍 15 min from city center'
              ]
            }
          ],
          meals: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ponta Negra Beach Sunset & Farewell to the City',
              description: "Manaus's urban beach on the Rio Negro is a gathering place at sunset — local families, vendors selling tapioca and grilled meats, fishermen hauling in nets. Sit on the sand and watch the jungle-green horizon swallow the sun in a blaze of orange and violet. Tomorrow you leave the city behind entirely.",
              details: [
                '🌅 The Rio Negro is so dark it reflects sunsets like a mirror',
                '🎵 Live forró or pagode music often at the beachside bars on weekends'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Banzeiro Restaurant',
              description: "Manaus's finest Amazonian cuisine, run by chef Felipe Schaedler. Try moqueca de pirarucu (the Amazon's giant fish in coconut-tucupi stew), tacacá soup (traditional fermented tucupi broth with jambu leaves — the slight numbness in your lips is normal and wonderful), and bolo de macaxeira. An essential last night of civilization.",
              meta: '💰 $$$ · 📍 Manaus city center · Book ahead on weekends'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Prepare your bags tonight for the lodge tomorrow. Leave non-essentials in hotel storage. You need: quick-dry clothes, swimwear, insect repellent, sunscreen, binoculars, headlamp, dry bag, camera. Everything else is unnecessary in the jungle.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -3.1190, lng: -60.0217, label: 'Manaus Airport (MAO)', num: 1, cat: 'transport', desc: 'Gateway to the Brazilian Amazon — Eduardo Gomes Int\'l Airport' },
        { lat: -3.1450, lng: -60.0217, label: 'Teatro Amazonas', num: 2, cat: 'attraction', desc: 'Opulent 1896 opera house — symbol of the rubber boom' },
        { lat: -3.1368, lng: -60.0222, label: 'Mercado Adolpho Lisboa', num: 3, cat: 'food', desc: 'Cast-iron market with fresh Amazonian fruits and fish' },
        { lat: -3.1630, lng: -59.8985, label: 'Meeting of the Waters', num: 4, cat: 'attraction', desc: 'Rio Negro meets Solimões — and refuses to mix for 6km' },
        { lat: -3.0820, lng: -60.0760, label: 'Ponta Negra Beach', num: 5, cat: 'attraction', desc: 'Rio Negro urban beach — sunset drinks and local life' },
        { lat: -3.1080, lng: -60.0330, label: 'Banzeiro Restaurant', num: 6, cat: 'food', desc: 'Finest Amazonian cuisine — tacacá, pirarucu, tucupi' }
      ]
    },

    // ========== DAY 2 ==========
    {
      num: 2,
      date: '2026-03-01',
      neighborhoods: 'Rio Negro · Jungle Lodge · Flooded Forest',
      title: 'Into the Jungle — Flooded Forest by Canoe',
      description: "Leave Manaus behind by boat. A 2-3 hour motorized canoe ride up the Rio Negro takes you deep into the rainforest, the city dissolving into unbroken jungle on all sides. Settle into your lodge bungalow — a stilted cabin over the water, nets, wooden floors, the sounds of the jungle constant. In the afternoon, take your first flooded forest canoe tour: paddling silently through the igapó, the submerged forest, where the treetops become islands and the jungle floor is 8 meters underwater. Wildlife surrounds you.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Boat Transfer to Jungle Lodge',
              description: "Your lodge boat picks you up from the Manaus harbor. As the city skyline shrinks behind you, the Rio Negro opens up — impossibly wide, dark as strong tea, the jungle a solid wall of green on both banks. In the rainy season, the river has swallowed its banks entirely; the trees stand with their feet in the water. Watch for pink dolphins surfacing alongside the boat. This journey is itself part of the experience.",
              details: [
                '🚤 Transfer time: ~2-3 hours by fast boat from Manaus',
                '🐬 Pink dolphins (botos) often follow motorized boats on the Rio Negro',
                '🦅 Watch overhead for black vultures, kingfishers, and osprey hunting the river',
                '📷 Keep camera accessible — wildlife sightings start immediately on the river'
              ]
            },
            {
              title: 'Lodge Arrival & Orientation',
              description: "Arrive at your stilted lodge bungalow over the water. Unpack, get oriented, meet your naturalist guide. Lunch is always fresh and abundant at Amazonian lodges — river fish, manioc, açaí, tropical fruits. After lunch, a mandatory rest in your hammock while the afternoon downpour hammers the metal roof.",
              details: [
                '🏡 Lodges provide: mosquito-netted beds, ceiling fans, outdoor decks over the water',
                '🌧️ The afternoon rain (1-2 hours) is your built-in siesta time — embrace it',
                '🦟 Apply repellent immediately and keep netting in place — especially at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Lodge Kitchen — Amazon River Fish',
              description: "Your first jungle lodge lunch: freshly caught tambaqui or tucunaré grilled over wood coals, served with manioc farinha, hearts of palm salad, and fresh-squeezed cupuaçu juice. River fish in the Amazon tastes completely different — cleaner, more mineral, sweeter — than anything you get anywhere else.",
              meta: '💰 Included · 📍 Lodge dining room'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Flooded Forest (Igapó) Canoe Tour',
              description: "This is the defining Amazon experience during the rainy season and it's available nowhere else. Your guide paddles you in a small wooden canoe into the igapó — the flooded forest. The trees stand in 5-8 meters of black water, their roots hidden below, their canopies meeting above. You're gliding through the interior of the forest at treetop level. Look left: a pair of howler monkeys watching you with suspicion. Look right: a giant otter slides off a branch. A sloth hangs motionless from a cecropia, regarding you with ancient indifference. Silence, broken only by paddles and birds.",
              details: [
                '🐒 Howler monkeys often heard before seen — a roar that sounds like a large predator',
                '🦦 Giant otters: the apex predator of the Amazon rivers — incredibly playful to watch',
                '🦥 Three-toed sloths move about 1 body length per minute — patience pays off',
                '🐊 Caiman may be visible sunning on logs above the waterline',
                '🌺 Orchids and bromeliads sprout directly from tree branches 10 meters above the water'
              ]
            }
          ],
          meals: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Boat Ride & Night Sounds',
              description: "As the sky turns red over the jungle, drift out on the river and watch the show. Scarlet macaws fly in pairs toward their roosts, their calls bouncing off the water. Herons stand like statues in the branches. At dusk, the first bats emerge — hundreds of them — sweeping across the river surface for insects. Then darkness arrives fast, as it does in the tropics, and the jungle night chorus begins: frogs, insects, nightbirds, the occasional distant roar of a howler monkey. There is nothing quite like an Amazon night.",
              details: [
                '🌅 Sunsets on the Rio Negro are extraordinary — the dark water reflects everything',
                '🦇 Hundreds of bats emerge at dusk to hunt insects over the water',
                '🐸 The night cacophony is overwhelming and beautiful — record it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Lodge Kitchen — Jungle Dinner by Lantern',
              description: "Dinner at the lodge: manioc soup, freshwater fish stew with local herbs (especially jambu — the leaf that numbs your lips), cassava bread, and tropical fruit. By lantern light, with the jungle noises surrounding you. Your guide will identify what you're hearing.",
              meta: '💰 Included · 📍 Open-air lodge dining room'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Your first night in the jungle is sensory overload. The noise is relentless and magnificent — insects, frogs, nightjars, and possibly howler monkeys at 3am. Earplugs are there if you need them; most people find they sleep extraordinarily well by night 2.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -3.1400, lng: -60.0150, label: 'Manaus Harbor — Departure Point', num: 1, cat: 'transport', desc: 'Board the lodge boat here' },
        { lat: -3.3400, lng: -60.5800, label: 'Amazon Jungle Lodge', num: 2, cat: 'attraction', desc: 'Stilted bungalows over the Rio Negro — your home in the jungle' },
        { lat: -3.2800, lng: -60.5200, label: 'Igapó Flooded Forest', num: 3, cat: 'attraction', desc: 'Submerged forest — canoe at treetop level through the flood' },
        { lat: -3.3200, lng: -60.6100, label: 'River Wildlife Corridor', num: 4, cat: 'attraction', desc: 'Pink dolphins, giant otters, and macaws along the river' },
        { lat: -3.2500, lng: -60.4800, label: 'Sunset Viewpoint', num: 5, cat: 'attraction', desc: 'Open river stretch — watch the sun sink into the jungle' }
      ]
    },

    // ========== DAY 3 ==========
    {
      num: 3,
      date: '2026-03-02',
      neighborhoods: 'Jungle Lodge · Deep Forest · River Channels',
      title: 'Deep Jungle — Piranhas, Caimans & Night Safari',
      description: "Your deepest day in the Amazon. Wake before dawn for the bird symphony, then venture on a serious jungle walk through primary rainforest — your guide identifies plants, insects, tracks, and the invisible architecture of the ecosystem. In the afternoon, fish for piranha from the riverside. After dinner, the night comes alive in ways daylight never reveals: headlamps sweep across the water and a caiman night safari shows you the Amazon's apex predators in their element.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dawn Bird Walk (5:30 AM)',
              description: "Rise at 5am and step out onto your deck. The Amazon dawn is extraordinary: as the jungle shifts from black to grey to green, the bird chorus builds into something almost unbearable in its intensity. Over 1,000 species of birds call the Amazon home. Your guide will identify calls: the prehistoric scream of the hoatzin, the territorial display of the scarlet macaw, the hammering of a woodpecker on a giant Brazil nut tree. This is one of the great wildlife experiences on Earth.",
              details: [
                '🦜 Species to listen for: hoatzin, harpy eagle (rare), blue-and-yellow macaw, toucans',
                '🔭 Binoculars essential — bring 8x42 minimum for canopy birds',
                '⏰ 5:30am departure when the light is low and birds are most active',
                '📍 Walk along the elevated forest paths above the flood line'
              ]
            },
            {
              title: 'Primary Rainforest Walk & Survival Skills',
              description: "After breakfast, a 2-3 hour guided walk through primary forest along raised paths and ridges above the flood level. Your guide transforms the jungle from overwhelming noise into readable text: which palms have edible hearts, which vines collect drinking water, what animal made these claw marks on the Brazil nut tree (an ocelot), why those leaves are perfectly arranged in a helix (a bromeliad collecting rainwater for tree frogs). You'll handle tarantulas if brave, taste forest fruits, and understand why indigenous communities can survive here indefinitely.",
              details: [
                '🕷️ Tarantulas are docile in expert hands — handling is optional but memorable',
                '💧 Your guide will cut a vine and let you drink the fresh water inside',
                '🌿 Medicinal plants: the forest pharmacy — learn which bark reduces fever, which leaf treats infection',
                '🐜 Leaf-cutter ant colonies: underground fungus farms up to 30 million strong',
                '🌳 A single Brazil nut tree can live 500 years and feeds dozens of species'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Lodge Kitchen — Açaí & Jungle Breakfast',
              description: "Freshly made açaí bowl (actual Amazonian açaí, not the imported stuff — it's earthier and more intense), tapioca pancakes with local honey, fresh papaya, and strong Brazilian coffee. Fuel up — it's a long morning.",
              meta: '💰 Included · 📍 Lodge'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Piranha Fishing on the Amazon',
              description: "Grab a hand line and a piece of raw meat and join the locals at their favorite riverbank. Red-bellied piranha are everywhere in the Amazon — and surprisingly easy to catch on a hand line if you keep the bait moving. They're aggressive, prehistoric-looking creatures with eyes full of ancient intelligence. Your guide will show you how to handle them safely (those teeth are no joke). Many lodges cook your catch for dinner — a genuine eat-what-you-catch experience.",
              details: [
                '🎣 Hand-line fishing only — keeps it sporting and traditional',
                '🦷 Piranha teeth are razor-sharp and can bite through fishing line — your guide shows safe handling',
                '🍳 Catch gets pan-fried at the lodge — piranha actually tastes quite good',
                '🌊 Fish in channels and tributary inlets — the main river has too much current'
              ]
            },
            {
              title: 'Giant Water Lily Pond & Wildlife Spotting',
              description: "Navigate to a quiet black-water lake covered with Victoria amazonica — the giant Amazonian water lily. The pads can reach 3 meters in diameter and support the weight of a child. They're covered in sharp spines on their undersides (to deter manatees from eating them) and bloom pure white at night, turning pink by morning. While floating among them, your guide spots a pygmy marmoset (the world's smallest monkey, 15cm tall) in the branches above, and a pair of squirrel monkeys watching from across the water.",
              details: [
                '🌺 Victoria amazonica pads: up to 3m diameter, hold 40kg if weight is distributed',
                '🐒 Pygmy marmoset: world\'s smallest monkey, hidden in cecropia leaves near the waterline',
                '🦜 Hoatzin birds often nest in overhanging branches at these quiet lakes',
                '📸 The lily pad lake at golden hour is one of the Amazon\'s most photogenic settings'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Riverside Jungle Picnic',
              description: "Eat lunch at a river beach or on a sandy bank that emerges above the flood line — manioc bread, smoked fish, fresh mango and watermelon, cold coconut water. The simplest food tastes extraordinary out here.",
              meta: '💰 Included · 📍 Riverside'
            }
          ]
        },
        {
          label: 'Night',
          activities: [
            {
              title: 'Caiman Night Safari',
              description: "After dinner, headlamps on and into the dark river. Your guide sweeps a powerful flashlight across the water's surface — and the darkness erupts with orange points of light. Caiman eyes. Black caiman (one of the largest predatory reptiles in the Americas, up to 4 meters) and the smaller spectacled caiman lie motionless at the water's surface. Your guide maneuvers the boat alongside, reaches into the water, and with practiced hands lifts a young spectacled caiman from the dark — lets you hold it — then slips it back. A primordial, unforgettable experience.",
              details: [
                '🐊 Black caiman: up to 4 meters — kept at a respectful distance from the boat',
                '🐊 Spectacled caiman: smaller (1-1.5m), young ones handled by experienced guides only',
                '🔦 Their eyes glow orange-red in flashlight — dozens visible on any given channel',
                '🌙 The river at night sounds completely different — more intense, more dense with life'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Lodge Kitchen — Piranha Soup & Tambaqui',
              description: "Tonight's dinner features piranha soup — a local tradition, thin and peppery with herbs, the little monsters repurposed into something delicious. The main: tambaqui (Amazon's best eating fish) baked in banana leaves with herbs and lime. Your guide eats with you and tells stories.",
              meta: '💰 Included · 📍 Lodge'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'For the night safari, bring your waterproof camera and a headlamp. Wear full-length clothing and use repellent heavily. Move slowly and follow your guide\'s directions exactly — the Amazon at night is safe with an expert guide and potentially not-safe without one.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -3.3600, lng: -60.6200, label: 'Dawn Bird Walk Trail', num: 1, cat: 'attraction', desc: 'Primary forest trail — over 1,000 bird species recorded here' },
        { lat: -3.3500, lng: -60.5900, label: 'Piranha Fishing Channel', num: 2, cat: 'attraction', desc: 'River channel for hand-line piranha fishing' },
        { lat: -3.3800, lng: -60.6400, label: 'Giant Water Lily Lake', num: 3, cat: 'attraction', desc: 'Victoria amazonica — pads up to 3m diameter' },
        { lat: -3.3700, lng: -60.6300, label: 'Caiman Safari Zone', num: 4, cat: 'attraction', desc: 'Black-water channel — dozens of caiman eyes at night' },
        { lat: -3.3450, lng: -60.5750, label: 'Jungle Walk Base', num: 5, cat: 'attraction', desc: 'Starting point for primary forest survival skills walk' }
      ]
    },

    // ========== DAY 4 ==========
    {
      num: 4,
      date: '2026-03-03',
      neighborhoods: 'Rio Negro · Indigenous Village · Black-Water Lake',
      title: 'Pink Dolphins & Indigenous Culture',
      description: "The most joyful day in the Amazon. Motor out to a black-water lake known for boto (pink river dolphin) encounters — these extraordinary creatures, unique to South America's rivers, surface around the boat, sometimes close enough to touch. In the afternoon, visit a Sateré-Mawé indigenous community for a genuine cultural exchange — traditional ceremony, plant medicine knowledge, handicrafts, and a perspective on the forest that can only come from 10,000 years of living inside it. A day of wonder and humility.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Swimming with Pink River Dolphins (Botos)',
              description: "One of the most extraordinary wildlife experiences on Earth. The boto (Amazon river dolphin) is the world's largest freshwater dolphin — up to 2.5 meters, pale grey when young, turning progressively pinker as they age. In certain black-water lakes near Manaus, wild botos have learned to associate boats with fish. They approach, surface, bump the boat, roll onto their sides to look at you with small intelligent eyes. Your guide enters the water holding small fish as an offering — the dolphins feed from hand, then dart away. Getting into the water with them is a once-in-a-lifetime moment.",
              details: [
                '🐬 Amazon river dolphins (botos) are pink — more vivid in adult males',
                '🌊 Water temperature: ~28-30°C (82-86°F) — warm and inviting',
                '🏊 Wear quick-dry shorts for swimming — bring a waterproof camera',
                '🐟 Your guide carries small fish to attract and reward the dolphins',
                '⚠️ Botos are wild animals — follow guide instructions, no grabbing or chasing'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Lodge Kitchen — Tropical Fruit & Tapioca',
              description: "Early breakfast before the dolphin trip: fresh papaya, pineapple, and starfruit, tapioca with coconut cream, and coffee. Light enough to swim on.",
              meta: '💰 Included · 📍 Lodge'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sateré-Mawé Indigenous Village Visit',
              description: "A river journey to a Sateré-Mawé community — one of the Amazon's 400+ surviving indigenous nations. This is not a staged tourist show: the guide introduces you to community members who share aspects of their lives genuinely and on their terms. You'll see how guaraná (the plant the energy drink was named after) is cultivated and ground, learn which plants treat which ailments from the community's knowledge-keeper, and see how handmade hammocks, baskets, and body decorations are made. Children will likely show you around with enormous curiosity about you.",
              details: [
                '🌿 Guaraná: originated with the Sateré-Mawé — it grows wild here and they\'ve cultivated it for centuries',
                '💊 Forest medicine: over 80% of the Amazon\'s plants have been identified by indigenous medicine',
                '🎨 Traditional body painting uses jenipapo fruit — the blue-black stain lasts 2 weeks',
                '🤝 Ask your guide how to greet people respectfully — it matters',
                '🛒 Buy handmade bracelets and baskets directly from the artisans — money stays in the community'
              ]
            },
            {
              title: 'Anaconda Territory — Searching for the Giant',
              description: "The world's heaviest snake lives in the Amazon — the green anaconda, which can reach 7 meters and 250kg. They're shy and increasingly rare near lodges, but your guide knows where to look: the shallows of quiet channels, submerged root systems, the margins of lakes. Even if you don't find one (you might), the search takes you into channels so overgrown they feel like tunnels, the canoe pushing through lotus pads and floating grass islands while kingfishers flash ahead.",
              details: [
                '🐍 Green anaconda: can reach 7m/250kg — docile unless provoked, prefers water',
                '🦅 These channels are excellent for kingfisher and heron spotting even if no anaconda',
                '🌿 The boat pushes through floating meadows of water hyacinth — otherworldly'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Community Meal at Indigenous Village',
              description: "Eat with the community: beiju (fermented manioc flatbread), tucupi broth with regional spices, pirarucu (the Amazon's giant fish, dried and cooked in a clay pot), and fresh guaraná drink prepared from dried powder scraped on fish teeth — the traditional way. A meal unlike any other.",
              meta: '💰 Included with lodge package · 📍 Indigenous village'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hammock Sunset & Stargazing',
              description: "Return to the lodge for your last proper evening. Swing in your hammock on the deck as the sun sets across the river. The Amazon sky after dark — far from any city lights — is the Milky Way in full resolution, the Southern Cross wheeling overhead, satellite tracks crossing silent. Bring a glass of cachacinha (local sugarcane spirit) and a blanket if it rains.",
              details: [
                '🌟 The Amazon has one of the darkest night skies accessible from civilization',
                '🌌 Milky Way visible to the naked eye in both rainy and dry season',
                '🔭 Scorpius and Centaurus are directly overhead — utterly different sky from the Northern Hemisphere'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Lodge Farewell Dinner — Pirarucu & Caipirinha',
              description: "The lodge's best dinner: pirarucu in tucupi sauce — the giant Amazonian fish (can reach 3 meters, 200kg) prepared as a generous fillet, slow-cooked with regional herbs, served with jaraqui fritter and cassava purée. Caipirinha cocktails made with fresh maracujá (passion fruit). A celebration of the Amazon table.",
              meta: '💰 Included · 📍 Lodge'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Tip your guides generously tonight. These naturalists are extraordinary humans — fluent in the language of the forest, genuinely passionate, often from families who have lived in the Amazon for generations. R$100 per guide per day is a meaningful gift.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -3.4200, lng: -60.7000, label: 'Pink Dolphin Lake (Boto Lake)', num: 1, cat: 'attraction', desc: 'Black-water lake — wild boto feeding and swimming encounters' },
        { lat: -3.5000, lng: -60.7500, label: 'Sateré-Mawé Village', num: 2, cat: 'attraction', desc: 'Indigenous community — guaraná, forest medicine, traditional culture' },
        { lat: -3.4600, lng: -60.7200, label: 'Anaconda Channel', num: 3, cat: 'attraction', desc: 'Narrow channels through water hyacinth meadows — anaconda territory' },
        { lat: -3.3300, lng: -60.5500, label: 'Lodge Stargazing Deck', num: 4, cat: 'attraction', desc: 'Over-water deck — Milky Way and Southern Cross visible' },
        { lat: -3.4000, lng: -60.6800, label: 'Rio Negro Wildlife Zone', num: 5, cat: 'attraction', desc: 'Prime river corridor for macaws, kingfishers, and giant otters' }
      ]
    },

    // ========== DAY 5 ==========
    {
      num: 5,
      date: '2026-03-04',
      neighborhoods: 'Jungle Lodge · Rio Negro · Manaus Departure',
      title: 'Last Dawn in the Jungle — Farewell to the Amazon',
      description: "Your final morning in the Amazon is not wasted on packing. Rise at 5am one last time: the forest is silver and alive with sound. A short morning canoe through the flooded trees, listening, looking, saying goodbye. Then back to the lodge for a final breakfast, pack up, and board the boat for the return journey to Manaus. The city will feel overwhelming after days in the jungle — use the transit time to process, and carry the Amazon back with you.",
      timeBlocks: [
        {
          label: 'Dawn',
          activities: [
            {
              title: 'Final Dawn Canoe — The Amazon Goodbye',
              description: "At 5am, push out from the dock in silence. The jungle is waking up: the dawn chorus is reaching its daily crescendo, pink light filtering through the canopy, mist rising off the black water. Paddle slowly through the flooded forest one last time — no rushing, no schedule, just the forest and its sounds. Your guide points out a family of howler monkeys crossing above you through the canopy. A giant kingfisher watches from a dead branch, perfectly still, then departs in a streak of electric blue. You will want to stay.",
              details: [
                '⏰ 5:00am departure — the most magical hour in the Amazon',
                '🐒 Howler monkey family crossings are common in the canopy at dawn',
                '🦚 Horned screamers and egrets often visible in the waterside trees',
                '📸 Last chance for flooded forest photography in beautiful early light'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Final Breakfast',
              name: 'Lodge Kitchen — Last Jungle Morning',
              description: "A generous final breakfast: tucumã fruit on tapioca (Manaus's most beloved street food), fresh açaí, scrambled eggs with herbs, strong coffee, and fresh coconut. Eat slowly — this is your last meal in the jungle.",
              meta: '💰 Included · 📍 Lodge'
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Lodge Departure & River Journey Back',
              description: "Check out, settle tip with your guides, and board the boat for the return to Manaus. The 2-3 hour river journey back is its own experience — you've changed since you came the other way. The river looks different: you can name the birds now, you recognize the trees, you know what lives in that dark water. The city appears on the horizon looking strange and loud.",
              details: [
                '🚤 Return journey: 2-3 hours · Depart lodge by 8-9am to make afternoon flight',
                '🦅 The Meeting of the Waters is visible from the river on the approach back to Manaus',
                '📸 Final river photos — the Rio Negro is beautiful in morning light'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Manaus Souvenir Market & Departure',
              description: "If you have time before your flight, the Mercado Municipal (Adolpho Lisboa) is the best place for authentic Amazon souvenirs: artisanal açaí soaps, local guaraná powder and candy, handmade indigenous crafts, and fine hardwood bowls. Avoid anything made from animal parts (illegal, unethical, often seized at customs). Buy the food items — they're allowed and delicious.",
              details: [
                '🛒 Best souvenirs: guaraná powder, tucupi paste, Amazonian spice sets, cotton hammocks',
                '⚠️ DO NOT buy: anything made from animal parts, corals, or rare woods — illegal in Brazil and at customs',
                '🏪 The market is open Mon-Sat — check timing based on your flight'
              ]
            },
            {
              title: 'Airport Departure — Carry the Amazon Home',
              description: "At the airport, take a quiet moment before boarding. You've been inside the world's greatest wilderness. You've heard the jungle's heartbeat and seen its creatures at close range. The Amazon occupies 40% of South America and produces 20% of the world's fresh water. It's under pressure. Your visit, done responsibly through locally-owned lodges and indigenous-led tours, is part of the argument for its survival.",
              details: [
                '✈️ Eduardo Gomes Airport (MAO) — allow 2 hours before departure',
                '🌿 The smell of the Amazon — wet earth, river, vegetation — stays with you for days'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Restaurante do Largo — Manaus Last Meal',
              description: "If time permits, a final Amazon meal in Manaus: caldeirada de tucunaré (peacock bass fish stew in a tomato and herb broth), served with rice, manioc, and a caipirinha made with regional cachaça. Simple, perfect, Amazonian.",
              meta: '💰 $$ · 📍 Manaus Centro'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'The Amazon changes people. Most visitors say they return home seeing their own environment differently — more attentive to trees, birds, the complexity of living systems. Take that change seriously. Support organizations like WWF Brazil, Instituto Socioambiental, or IMAZON that are working to protect the Amazon. What you\'ve just experienced is worth protecting.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -3.3400, lng: -60.5800, label: 'Lodge — Final Canoe Departure', num: 1, cat: 'transport', desc: 'Final dawn canoe — 5am on your last morning in the jungle' },
        { lat: -3.2000, lng: -60.3000, label: 'Rio Negro — Return Journey', num: 2, cat: 'transport', desc: 'River journey back to Manaus — 2-3 hours through the jungle' },
        { lat: -3.1630, lng: -59.8985, label: 'Meeting of the Waters (Return View)', num: 3, cat: 'attraction', desc: 'Visible from the river on approach to Manaus' },
        { lat: -3.1368, lng: -60.0222, label: 'Mercado Adolpho Lisboa', num: 4, cat: 'food', desc: 'Final souvenirs — guaraná, spices, Amazonian crafts' },
        { lat: -3.0380, lng: -59.9863, label: 'Manaus Airport (MAO)', num: 5, cat: 'transport', desc: 'Departure — carry the Amazon with you' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Jungle Lodge (4 nights, all-inclusive)', budget: 'R$800-1,200pp/night', midrange: 'R$1,200-2,000pp/night', luxury: 'R$2,500-5,000pp/night' },
    { category: 'Manaus Hotel (1 night)', budget: 'R$200-350', midrange: 'R$350-600', luxury: 'R$600-1,500' },
    { category: 'Flights to/from Manaus', budget: 'R$600-1,000pp', midrange: 'R$1,000-2,000pp', luxury: 'R$3,000+ (business class)' },
    { category: 'Manaus meals & activities', budget: 'R$150-300/day', midrange: 'R$300-600/day', luxury: 'R$600+/day' },
    { category: 'Guide tips (recommended)', budget: 'R$50/guide/day', midrange: 'R$100/guide/day', luxury: 'R$200+/guide/day' },
    { category: '5-Day Total (couple, all-inclusive lodge)', budget: 'R$8,000-12,000 (~$1,500-2,300 USD)', midrange: 'R$14,000-20,000 (~$2,700-3,800 USD)', luxury: 'R$25,000-50,000 (~$5,000-10,000 USD)' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Manaus (MAO) — Eduardo Gomes International Airport', 'Direct flights from: São Paulo (4h), Rio de Janeiro (4.5h), Miami (6h)', 'Most lodges include airport pickup — confirm in advance', 'No visa required for US, EU, UK, Canada citizens (as of 2025)'] },
    { title: '🌡️ Weather (Late Feb–Mar)', items: ['Peak rainy season — daily afternoon showers 1-3 hours', 'Temperature: 28-32°C (82-90°F) year-round', 'Humidity: very high (~85-90%)', 'The rain actually brings advantages: flooded forest canoe access, cooler afternoons, beautiful dramatic skies'] },
    { title: '💉 Health & Safety', items: ['Yellow fever vaccine required — get it 10+ days before travel', 'Malaria prophylaxis recommended — consult travel clinic 2-4 weeks before', 'DEET 50%+ insect repellent — non-negotiable', 'The jungle is safe with a guide; don\'t wander alone. Follow guide instructions exactly.'] },
    { title: '🛂 Entry Requirements', items: ['No visa for US/EU/UK/Canadian citizens as of 2025', 'Yellow fever vaccination certificate often checked on arrival in Amazonas state', 'Valid passport required (6+ months validity recommended)'] },
    { title: '💰 Currency & Payments', items: ['Brazilian Real (BRL) — ~R$5-6 per USD (check current rate)', 'ATMs widely available in Manaus. Lodges are almost all cash or pre-paid packages.', 'Wise or Revolut cards highly recommended for favorable exchange rates', 'Bring cash to the lodge — no ATMs in the jungle'] },
    { title: '📱 Connectivity', items: ['No cell signal at jungle lodges — this is a feature, not a bug. Embrace the disconnect.', 'Most lodges have emergency satellite communication for safety', 'Download offline maps of Manaus, and any books/podcasts for travel days', 'WhatsApp works in Manaus — useful for communicating with lodge staff'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
