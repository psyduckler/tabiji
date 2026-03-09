const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772895983046_mfyeua',
  email: 'bernardjhuang@gmail.com',
  destination: 'Milos, Greece',
  start_date: '2026-03-23',
};

const itineraryData = {
  destination: 'Milos, Greece',
  countryEmoji: '🇬🇷',
  title: 'Milos: Moonscapes, Sea Caves & the Real Greece',
  subtitle: 'Five days of volcanic coastlines, lunar beaches, ancient catacombs, and fishing village tavernas — solo adventure on the Cyclades\' hidden gem',
  description: 'Milos is the Greek island that Santorini wishes it still was — raw, volcanic, uncrowded, and hauntingly beautiful. With over 70 beaches carved from sulfur cliffs and obsidian shores, early Christian catacombs hidden beneath olive groves, and fishing villages where boats still nestle into carved-rock garages called syrmata, this is Greece at its most authentic. Late March means you\'ll have the lunar landscape of Sarakiniko almost entirely to yourself, the wildflowers are erupting across the hills, and the tavernas that stay open year-round will treat you like family. This itinerary is built for a solo explorer who wants adventure without crowds — hiking volcanic trails, scrambling down to secret beaches, watching sunsets from a medieval kastro, and eating the freshest seafood of your life in tiny harbor-front tavernas.',
  duration: '5 nights',
  dates: 'Mar 23 – Mar 28, 2026',
  budget: 'Moderate',
  pace: 'Moderate-Active',
  bestFor: 'Solo travelers, Adventure seekers, Culture lovers',
  highlights: [
    'Sarakiniko — walk across the lunar white volcanic landscape, completely alone in March',
    'Full-day boat tour to Kleftiko sea caves and pirate hideouts',
    'Plaka sunset from the kastro — the best free show in the Cyclades',
    'Ancient Catacombs of Milos — one of only three in the world',
    'Fishing village hopping: Klima, Mandrakia, Firopotamos and their colorful syrmata',
    'Hike the volcanic south coast from Fyriplaka to Tsigrado',
    'O! Hamos! — the legendary taverna that defines Milos dining',
    'Paleochori beach with volcanic hot springs warming the sand',
  ],

  essentials: [
    { title: '🛬 Getting There', text: 'Milos has a small airport (MLO) with seasonal flights from Athens on Olympic Air (~45 min). Year-round ferries run from Piraeus (Athens) — high-speed ~3.5 hours, conventional ~7 hours. SeaJets and Blue Star Ferries are the main operators. In March, ferry schedules are reduced — book ahead via ferryhopper.com.' },
    { title: '🚗 Getting Around', text: 'Rent a car or ATV — essential on Milos, especially in March when buses run a skeleton schedule. The island is small (about 30 min end-to-end) but roads to beaches are often unpaved. A small 4x4 or sturdy ATV handles everything. Rental agencies cluster around Adamas port. Budget €30-40/day for a car in March (off-season rates).' },
    { title: '💵 Money', text: 'Euros (€). ATMs in Adamas and Plaka. Many tavernas accept cards but bring cash for small beach cantinas and village shops. March prices are significantly lower than summer — expect 30-50% off accommodation and dining is more relaxed.' },
    { title: '🌡️ March Weather', text: 'Daytime 14-18°C, nights 10-13°C. Mix of sunny days and occasional rain. Perfect for hiking and exploring — not peak swimming weather, though brave souls do swim at Sarakiniko on calm days. Pack layers, a light rain jacket, and good walking shoes. Wind can be strong — the meltemi hasn\'t started yet but northerlies occur.' },
    { title: '⚠️ Early Season Note', text: 'March is shoulder season on Milos. Some seasonal restaurants and tour operators won\'t open until April/May. The upside is enormous: zero crowds at beaches, lower prices, and a more authentic experience. Adamas, Plaka, and Pollonia have year-round restaurants. Boat tours to Kleftiko typically start operating in late March (weather-dependent) — book through your accommodation.' },
    { title: '🔒 Safety', text: 'Milos is extremely safe for solo travelers. The island has a small, close-knit community of ~5,000 residents. Beach access can involve scrambling over rocks or down steep paths (Tsigrado especially) — wear proper shoes and don\'t attempt difficult access in wet conditions. Cell service covers most of the island.' },
  ],

  days: [
    // DAY 1 — Arrival, Adamas & Plaka Sunset
    {
      num: 1,
      date: '2026-03-23',
      title: 'Arrival, Harbor Town & Kastro Sunset',
      description: 'Settle into Milos with a gentle first day exploring Adamas harbor, getting oriented, and climbing to Plaka\'s medieval kastro for one of the most spectacular sunsets in all of Greece.',
      neighborhoods: 'Adamas · Plaka · Trypiti',
      timeBlocks: [
        {
          label: 'Morning / Afternoon',
          activities: [
            {
              title: 'Arrive & Explore Adamas',
              description: 'Whether you arrive by ferry or flight, Adamas is your base. This cheerful port town wraps around a natural harbor — one of the largest in the Mediterranean, formed by the island\'s volcanic caldera. Pick up your rental car, drop bags at your accommodation, then stroll the waterfront. The Milos Mining Museum here is surprisingly excellent — Milos has been mined for obsidian since 10,000 BC, and the exhibits trace the island\'s geological story from volcanic birth to modern-day bentonite extraction.',
              details: ['📍 Adamas port, central Milos', '🕐 Mining Museum: 9am-2pm, 5pm-9pm (check winter hours) · €4', '💡 The museum explains why Milos looks so otherworldly — volcanic activity created the bizarre rock formations and 70+ unique beaches']
            },
            {
              title: 'Lunch at Adamas Waterfront',
              description: 'Walk the harbor promenade and find a waterfront taverna for your first proper Greek meal. Mikros Apoplous is a solid year-round choice right on the water — try the fresh catch of the day, local cheese pitarakia (fried cheese pies), and a glass of Assyrtiko wine.',
              details: ['📍 Mikros Apoplous, Adamas waterfront', '💰 €15-25/person', '💡 Ask what fish came in today — in March, the fishermen supply directly to restaurants']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mikros Apoplous',
              description: 'Waterfront restaurant-bar in Adamas with fresh seafood, creative Greek dishes, and a relaxed vibe. Great for a solo meal at the bar watching boats come and go.',
              meta: '📍 Adamas waterfront · 💰 €15-25 · Open year-round'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pick up a local map from the port shops — phone signal can be spotty on remote beaches and the map marks unpaved road conditions.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Plaka & Kastro Sunset 🌅',
              description: 'Drive 4km up to Plaka, the island\'s tiny capital perched on a hilltop. Wander the narrow whitewashed streets and climb to the ruins of the Venetian kastro (castle) at the very top. The 360° panoramic view is staggering — you can see neighboring islands Kimolos, Sifnos, and Serifos. At sunset, the sky ignites over the caldera and the entire town turns golden. In March, you might be the only person up here.',
              details: ['📍 Kastro (castle ruins), top of Plaka · Free', '🕐 Arrive 30 min before sunset for the best spot', '💡 The kastro has a small church, Panagia Thalassitra, with an icon said to protect sailors']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Archontoula',
              description: 'Traditional taverna in the heart of Plaka\'s pedestrian lanes. Hearty, no-nonsense Greek cooking — moussaka, stuffed tomatoes (gemista), grilled lamb chops. The outdoor tables in the lane are atmospheric even in March.',
              meta: '📍 Plaka village center · 💰 €12-20 · Check hours in March (may close some weeknights)'
            }
          ],
          tips: [
            { type: 'tip', text: '🌅 Plaka sunset rivals Santorini\'s Oia — without the 500 other people. Bring a jacket, it gets windy at the kastro.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7267, lng: 24.4464, label: 'Adamas Port', num: 1, cat: 'transport', desc: 'Main port town — ferries, car rental, waterfront dining' },
        { lat: 36.7282, lng: 24.4430, label: 'Milos Mining Museum', num: 2, cat: 'attraction', desc: 'Volcanic geology and 10,000 years of mining history' },
        { lat: 36.7275, lng: 24.4472, label: 'Mikros Apoplous', num: 3, cat: 'restaurant', desc: 'Waterfront restaurant-bar with fresh seafood' },
        { lat: 36.7408, lng: 24.4267, label: 'Plaka Kastro', num: 4, cat: 'attraction', desc: 'Venetian castle ruins — best sunset viewpoint on Milos' },
        { lat: 36.7395, lng: 24.4275, label: 'Archontoula', num: 5, cat: 'restaurant', desc: 'Traditional taverna in Plaka\'s pedestrian lanes' }
      ]
    },

    // DAY 2 — Sarakiniko, Papafragas & North Coast
    {
      num: 2,
      date: '2026-03-24',
      title: 'Lunar Landscapes & Sea Cave Cathedrals',
      description: 'The day you came to Milos for. Explore the surreal white volcanic moonscape of Sarakiniko, peer into the collapsed sea caves of Papafragas, and discover the colorful fishing villages of the north coast.',
      neighborhoods: 'Sarakiniko · Papafragas · Mandrakia · Firopotamos',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sarakiniko Beach 🌙',
              description: 'This is the image that put Milos on the map — smooth white volcanic rock sculpted by wind and waves into something that looks like a lunar landscape dropped onto the Aegean Sea. In March, you\'ll likely have this alien world entirely to yourself. Explore the rock formations, find the old shipwreck rusting in a cove, and climb to the top of the cliffs for vertiginous views down to the turquoise water. The morning light is best for photography — the white rock practically glows.',
              details: ['📍 Sarakiniko, north coast of Milos', '🕐 Arrive by 9am for the best light and solitude', '💡 The rocks are smooth but can be slippery when wet. Wear shoes with grip, not flip-flops', '📸 Walk past the main cove to the eastern cliffs for the most dramatic photos — the arch and the rusted shipwreck are Instagram gold']
            },
            {
              title: 'Papafragas Caves',
              description: 'A 5-minute drive east of Sarakiniko, Papafragas is a collapsed sea cave that formed a narrow inlet of impossibly turquoise water between towering rock walls. Steep stairs lead down to a tiny hidden beach. Even if the water is too cold for swimming in March, the view from above is jaw-dropping — like looking into a natural cathedral.',
              details: ['📍 Papafragas, north coast · Free', '💡 The steep access path is rocky — take your time. In wet conditions, admire from the top', '📸 Stand at the cliff edge and shoot straight down into the narrow canyon — the water color is unreal']
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pick up pastries in Adamas',
              description: 'Grab a tyropita (cheese pie) and Greek coffee from a bakery in Adamas before heading out. Fournos tou Kosta is a solid local bakery.',
              meta: '📍 Adamas center · 💰 €3-5'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Sarakiniko faces north — mornings have the best light. The afternoon sun creates harsh shadows on the white rock. Visit before 11am for photos.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mandrakia Fishing Village',
              description: 'One of Milos\' most picturesque fishing hamlets. Colorful wooden doors line the rock-cut boat garages (syrmata) where fishermen still store their traditional boats. The tiny harbor has maybe 20 houses, a small church, and crystal-clear water. It feels like stepping into a postcard from 1950s Greece.',
              details: ['📍 Mandrakia, north coast', '💡 Walk along the coast path east from Mandrakia for views of dramatic rock formations and small hidden coves']
            },
            {
              title: 'Firopotamos Beach & Village',
              description: 'Another gem of a fishing village with syrmata boat houses, a small whitewashed church sitting right on the beach, and calm turquoise water in a sheltered cove. Less visited than Mandrakia and even more photogenic. The small beach here is one of the most sheltered on the north coast.',
              details: ['📍 Firopotamos, northwest coast', '💡 The drive down is on a winding unpaved road — take it slow', '📸 The church on the beach with fishing boats is the quintessential Milos photo']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Medusa (Mandrakia)',
              description: 'Famous seafood restaurant right on the tiny harbor of Mandrakia. Tables sit inches from the water and the fishing boats. Known for grilled octopus, shrimp saganaki, and the freshest fish on the island. In March, call ahead to confirm they\'re open — if so, this is a bucket-list meal.',
              meta: '📍 Mandrakia harbor · 💰 €20-35 · Cash preferred · Call ahead in March: +30 22870 28404'
            }
          ],
          tips: [
            { type: 'tip', text: '📱 If Medusa is closed for the season, head to Adamas for lunch at O! Hamos! instead — it\'s open year-round and equally legendary.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Plaka Evening Stroll',
              description: 'Return to Plaka for an evening walk through the quiet lanes. Visit the Archaeological Museum of Milos (home to a replica of the Venus de Milo — the original is in the Louvre) and the Folk Museum. Browse the small shops and pick up local ceramics or volcanic stone jewelry.',
              details: ['📍 Archaeological Museum, Plaka · €3', '🕐 Check winter hours — typically closes by 3pm, may have evening hours in shoulder season', '💡 The original Venus de Milo was discovered on the island in 1820 by a farmer plowing his field']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Avli (Plaka)',
              description: 'Set in a beautiful courtyard garden in the backstreets of Plaka. Traditional Cycladic cuisine with a modern touch — slow-cooked lamb, local cheeses, excellent wine list. Perfect for a solo dinner with a book.',
              meta: '📍 Plaka backstreets · 💰 €18-30 · Reservations recommended even in March'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 36.7453, lng: 24.3972, label: 'Sarakiniko Beach', num: 1, cat: 'attraction', desc: 'Iconic lunar white volcanic landscape — Milos\' most famous sight' },
        { lat: 36.7445, lng: 24.4089, label: 'Papafragas Caves', num: 2, cat: 'attraction', desc: 'Collapsed sea cave with hidden turquoise beach between rock walls' },
        { lat: 36.7477, lng: 24.3861, label: 'Mandrakia Village', num: 3, cat: 'attraction', desc: 'Tiny fishing village with colorful syrmata boat garages' },
        { lat: 36.7477, lng: 24.3861, label: 'Medusa Restaurant', num: 4, cat: 'restaurant', desc: 'Famous harbor-front seafood — grilled octopus and shrimp saganaki' },
        { lat: 36.7530, lng: 24.3730, label: 'Firopotamos', num: 5, cat: 'attraction', desc: 'Picturesque fishing village with beach-side church' },
        { lat: 36.7395, lng: 24.4275, label: 'Avli Restaurant', num: 6, cat: 'restaurant', desc: 'Courtyard dining in Plaka — traditional Cycladic cuisine' }
      ]
    },

    // DAY 3 — Kleftiko Boat Tour
    {
      num: 3,
      date: '2026-03-25',
      title: 'Kleftiko Sea Caves & Pirate History',
      description: 'The absolute must-do on Milos — a full-day boat tour around the dramatic southwestern coast to Kleftiko, a formation of towering white sea stacks and hidden caves once used as a pirate hideout. Only accessible by sea.',
      neighborhoods: 'Adamas · Southwest Coast · Kleftiko',
      timeBlocks: [
        {
          label: 'Full Day',
          activities: [
            {
              title: 'Full-Day Boat Tour to Kleftiko ⛵',
              description: 'This is the highlight of any Milos trip. Board a traditional sailing boat or catamaran from Adamas and cruise along the southwestern coast — a jaw-dropping progression of volcanic cliffs, sea caves, and hidden coves in every color from blinding white to rusty red to obsidian black. The destination is Kleftiko: massive white rock formations rising from the sea, riddled with caves and natural arches. The name means "thieves" — pirates used these caves as hideouts because the labyrinthine rocks made pursuit impossible. You\'ll anchor in the sheltered bay, explore caves by swimming or dinghy, and the crew serves fresh Greek lunch on board with local wine.',
              details: [
                '📍 Departs from Adamas harbor, typically 9am-10am',
                '🕐 Full-day tour, 6-8 hours · Returns late afternoon',
                '💰 €60-90/person in March (off-season rates) — includes lunch, drinks, snorkeling gear',
                '💡 Book through your accommodation or Milos Adventures (milosadventures.gr) — they\'re one of the few operators who start early season',
                '⚠️ Weather-dependent! March can be windy. If seas are rough, the captain may adjust the route or reschedule. Have a backup plan (Day 5 activities work as alternatives)',
                '📸 The moment the boat rounds the cape and Kleftiko appears is genuinely awe-inspiring — keep your camera ready'
              ]
            },
            {
              title: 'Stops Along the Way',
              description: 'Most tours stop at several points along the coast: Sykia Cave (a collapsed cave with a "skylight" opening to the sky and emerald water inside), the volcanic hot springs at Paleochori or Agia Kyriaki, and the dramatic sulfur-stained cliffs near Thiorichia (the abandoned sulfur mines). Each stop is more surreal than the last.',
              details: [
                '💡 Sykia Cave is accessible only by sea — the entrance is a narrow arch that opens into a massive cavern',
                '🌊 If brave enough, the water in March is around 16-17°C — refreshing but swimmable with a quick dip mentality',
                '📸 The sulfur cliffs near Thiorichia are streaked yellow, orange, and white — utterly alien'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Onboard the Boat',
              description: 'Most boat tours include a freshly prepared Greek lunch — grilled fish or chicken, Greek salad, bread, local wine and beer. Eaten anchored in a turquoise cove with volcanic cliffs towering above.',
              meta: 'Included in tour price'
            },
            {
              type: '🍽️ Dinner',
              name: 'O! Hamos!',
              description: 'THE legendary Milos taverna. Rustic, lively, unapologetically Greek. Massive portions of pitarakia (fried cheese pies unique to Milos), grilled octopus, lamb chops, local sausage, and handmade pasta. The owner is a character — expect boisterous hospitality. This is a top-5 meal on any Greek island, full stop.',
              meta: '📍 Adamas · 💰 €15-25 · Open year-round · Arrive by 7:30pm or prepare to wait'
            }
          ],
          tips: [
            { type: 'tip', text: '⛵ If the Kleftiko tour is cancelled due to weather, rebook for Day 5 and swap today with Day 5\'s plan. Flexibility is key in March.' },
            { type: 'tip', text: '🧴 Even in March, the sun reflecting off the sea and white rocks can burn. Wear sunscreen and bring sunglasses.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7267, lng: 24.4464, label: 'Adamas Harbor (Boat Departure)', num: 1, cat: 'transport', desc: 'Boat tours depart from the main harbor' },
        { lat: 36.6667, lng: 24.3167, label: 'Kleftiko', num: 2, cat: 'attraction', desc: 'Towering white sea stacks and pirate cave network — only accessible by boat' },
        { lat: 36.6750, lng: 24.3400, label: 'Sykia Cave', num: 3, cat: 'attraction', desc: 'Collapsed sea cave with skylight opening and emerald water' },
        { lat: 36.6689, lng: 24.3750, label: 'Thiorichia Sulfur Mines', num: 4, cat: 'attraction', desc: 'Abandoned sulfur mines with dramatic yellow-orange cliffs' },
        { lat: 36.7255, lng: 24.4480, label: 'O! Hamos!', num: 5, cat: 'restaurant', desc: 'Legendary taverna — pitarakia, grilled octopus, massive portions' }
      ]
    },

    // DAY 4 — South Coast Adventure & Catacombs
    {
      num: 4,
      date: '2026-03-26',
      title: 'Ancient Catacombs, Volcanic South & Hidden Beaches',
      description: 'Explore the island\'s ancient history in the Christian catacombs and Roman theater, then head to the wild south coast for volcanic hot springs, dramatic beach scrambles, and the colorful syrmata of Klima.',
      neighborhoods: 'Trypiti · Klima · Fyriplaka · Paleochori',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Catacombs of Milos',
              description: 'One of only three early Christian catacombs in the world (alongside Rome and the Holy Land). Carved into the hillside near Trypiti village in the 1st-5th century AD, these underground corridors contain burial niches for over 2,000 people. The guided tour takes you through dim, narrow passageways lined with carved arcosolium tombs. It\'s atmospheric, slightly eerie, and deeply moving — a tangible connection to the earliest days of Christianity in Greece.',
              details: [
                '📍 Trypiti, south of Plaka · Signposted from the main road',
                '🕐 8:30am-3pm (check winter schedule) · Closed Mondays',
                '💰 €4 · Guided tours only, ~20 minutes',
                '💡 Photography may be restricted inside. The entrance area has information boards with historical context'
              ]
            },
            {
              title: 'Ancient Theater & Venus de Milo Site',
              description: 'A short walk from the catacombs, the ancient Roman theater sits on a hillside with sweeping views over the bay. Originally built in the Hellenistic period and rebuilt by the Romans, it seated 7,000 spectators. Nearby, a simple marker shows where a farmer discovered the Venus de Milo statue in 1820 — arguably the most famous sculpture in the world, now in the Louvre.',
              details: [
                '📍 Between Trypiti and Klima · Free',
                '💡 Sit in the theater seats and look out toward the sea — the ancient Greeks knew how to pick a location',
                '📸 The theater with the sea behind it makes a beautiful photo'
              ]
            },
            {
              title: 'Klima Fishing Village 🎨',
              description: 'The most photogenic village on Milos — and possibly all of Greece. A single row of syrmata (boat houses carved into the rock face) line the waterfront, each painted in a different vivid color: electric blue, sunflower yellow, burnt orange, deep red. The fishermen\'s living quarters sit directly above the boat garages, accessed by steep outdoor stairs. Walk the narrow concrete path along the water\'s edge and peek into the open garages where traditional boats are stored.',
              details: [
                '📍 Klima, below Trypiti · Free',
                '💡 The morning light hitting the colored doors is spectacular — visit before 11am for the best photos',
                '📸 Walk to the far end of the path for the classic shot looking back along the row of colorful doors with the sea beyond'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Utopia Café (Plaka)',
              description: 'Perched at the edge of Plaka with a terrace overlooking the sea and countryside. Great coffee, fresh juice, and simple breakfast. In the evening it\'s famous for sunset cocktails, but mornings are peaceful.',
              meta: '📍 Edge of Plaka village · 💰 €5-10 · Check March hours'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Visit Klima, catacombs, and theater in one loop — they\'re all within walking distance of each other near Trypiti.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fyriplaka Beach',
              description: 'One of Milos\' most striking south coast beaches — a long crescent of sand backed by dramatic multicolored volcanic cliffs streaked in white, red, orange, and grey. Even in March when swimming isn\'t ideal, the geological drama of these cliffs makes it worth the visit. Walk along the beach and examine the rock layers — each one tells a chapter of Milos\' volcanic story.',
              details: [
                '📍 Fyriplaka, south coast · Free',
                '💡 Decent paved road access and a short walk down. One of the easier beaches to reach',
                '📸 The cliff colors are most vivid in afternoon light'
              ]
            },
            {
              title: 'Paleochori Beach & Volcanic Hot Springs ♨️',
              description: 'This south coast beach sits on top of active volcanic vents. Dig into the sand in certain spots and you\'ll feel hot water seeping up — natural geothermal springs right on the beach. The sulfurous streaks of yellow and orange in the cliffs add to the alien atmosphere. Some areas of shallow water are noticeably warmer. A restaurant right on the beach (Sirocco) sometimes cooks food using the geothermal heat buried in the sand.',
              details: [
                '📍 Paleochori, southeast coast',
                '💡 The hot spots are near the eastern end of the beach — look for yellowish sand and sulfur smell',
                '⚠️ Don\'t dig too deep or stay too long in the hottest spots — the geothermal water can be scalding below the surface',
                '🌋 This is a reminder that Milos is a still-active volcanic system — the same geology that creates the incredible beaches'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sirocco (Paleochori Beach)',
              description: 'Right on Paleochori beach with tables in the sand. Famous for cooking food using the geothermal heat from volcanic vents beneath the beach. Fresh fish, grilled meats, and Greek salads with your feet in warm sand.',
              meta: '📍 Paleochori Beach · 💰 €15-25 · Check March availability — may open weekends only'
            },
            {
              type: '🍽️ Dinner',
              name: 'Barriello (Trypiti)',
              description: 'The closest thing Milos has to fine dining — a creative Mediterranean menu with local ingredients, excellent wine pairings, and a romantic candlelit atmosphere in a restored village house. Perfect for treating yourself on a solo trip.',
              meta: '📍 Trypiti village · 💰 €25-40 · Reservations essential'
            }
          ],
          tips: [
            { type: 'tip', text: '🌋 Milos is one of the few places in Greece where you can directly experience volcanic activity — the hot springs at Paleochori are genuinely warm even in March.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7308, lng: 24.4192, label: 'Catacombs of Milos', num: 1, cat: 'attraction', desc: 'Early Christian catacombs — one of only three in the world' },
        { lat: 36.7320, lng: 24.4150, label: 'Ancient Roman Theater', num: 2, cat: 'attraction', desc: 'Hellenistic theater with sea views — near the Venus de Milo discovery site' },
        { lat: 36.7280, lng: 24.4100, label: 'Klima Village', num: 3, cat: 'attraction', desc: 'Most photogenic village in Greece — colorful syrmata boat houses' },
        { lat: 36.6850, lng: 24.3850, label: 'Fyriplaka Beach', num: 4, cat: 'attraction', desc: 'Crescent beach with dramatic multicolored volcanic cliffs' },
        { lat: 36.6858, lng: 24.4100, label: 'Paleochori Beach', num: 5, cat: 'attraction', desc: 'Beach with volcanic hot springs warming the sand' },
        { lat: 36.6858, lng: 24.4100, label: 'Sirocco Restaurant', num: 6, cat: 'restaurant', desc: 'Beach restaurant that cooks with geothermal heat' },
        { lat: 36.7310, lng: 24.4175, label: 'Barriello', num: 7, cat: 'restaurant', desc: 'Creative Mediterranean fine dining in a village house' }
      ]
    },

    // DAY 5 — Pollonia, East Coast & Farewell
    {
      num: 5,
      date: '2026-03-27',
      title: 'Pollonia, Eastern Shores & Island Farewell',
      description: 'Spend your final full day exploring the charming resort village of Pollonia, hiking coastal trails on the east side of the island, and soaking in the last views of this volcanic paradise.',
      neighborhoods: 'Pollonia · Phylakopi · Agia Kiriaki · Adamas',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Pollonia Village',
              description: 'Drive to the northeast corner of Milos to Pollonia, a small whitewashed village facing the neighboring island of Kimolos across a narrow strait. It\'s the most resort-like settlement on the island but retains its fishing village charm. Walk along the tamarisk-shaded beach, browse the small shops, and watch the Kimolos ferry come and go from the tiny pier.',
              details: [
                '📍 Pollonia, northeast Milos · ~20 min drive from Adamas',
                '💡 If you have time and the weather is calm, the ferry to Kimolos takes just 20 minutes for an optional day-trip to an even quieter island'
              ]
            },
            {
              title: 'Phylakopi Archaeological Site',
              description: 'On the way to or from Pollonia, stop at the ruins of Phylakopi — one of the most important Bronze Age settlements in the Cyclades. Inhabited from 3000 BC to 1100 BC, this ancient Minoan-era city was a major center of obsidian trade. The site is partially fenced but you can walk around the perimeter and see the ancient walls and foundations overlooking the sea.',
              details: [
                '📍 North coast road between Adamas and Pollonia',
                '💡 Not heavily signed — look for the archaeological site marker. The setting on the cliff edge is dramatic',
                '🕐 Exterior viewable anytime · Free'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'Gialos tis Pollonias',
              description: 'Relaxed taverna right on Pollonia beach with tables under tamarisk trees. Fresh seafood, excellent dakos (Cretan barley rusk salad), and strong Greek coffee. Watch fishing boats while you eat.',
              meta: '📍 Pollonia beachfront · 💰 €12-20 · Check March hours'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pollonia is the quietest corner of an already quiet island in March. Perfect for a contemplative morning if you\'re solo.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tsigrado Beach Scramble 🧗',
              description: 'The most adventurous beach access on Milos. Tsigrado is reached by climbing down through a narrow crack in the cliff using ropes and a rickety ladder — it feels like descending into a secret world. At the bottom: a tiny white sand beach with crystal-clear turquoise water surrounded by towering rock walls. Even if you just peer over the edge in March, the view down is vertigo-inducing and magnificent.',
              details: [
                '📍 Tsigrado, south coast (near Fyriplaka)',
                '⚠️ The descent requires some agility and confidence. Don\'t attempt in wet/windy conditions or with heavy bags',
                '💡 There\'s also a steep but less extreme path to the right — ask locals which is passable',
                '📸 The view from the top looking down through the narrow cliff gap to the turquoise water below is spectacular'
              ]
            },
            {
              title: 'Agia Kiriaki Beach',
              description: 'A sheltered south-coast beach with dramatic dark volcanic sand and crystal water. Protected from north winds, it\'s often swimmable even in shoulder season. Much easier to access than Tsigrado — a proper road and gentle path down. A good beach to simply sit, read, and appreciate the volcanic landscape one last time.',
              details: [
                '📍 Agia Kiriaki, south coast',
                '💡 One of the more sheltered beaches — if any beach is swimmable in late March, it\'s this one'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bakaliko tou Galani (Adamas)',
              description: 'Your farewell dinner at this beloved local wine bar and mezze spot in Adamas. Excellent selection of Greek wines paired with platters of local cheeses, cured meats, Milos pitarakia, and creative small plates. The owner curates the wine list personally and loves recommending bottles. A perfect solo farewell meal at the bar.',
              meta: '📍 Adamas · 💰 €20-30 · Open year-round · Great for solo dining at the bar'
            }
          ],
          tips: [
            { type: 'tip', text: '🌅 For your last sunset, drive up to the windmill viewpoint above Trypiti — less known than the Plaka kastro but equally stunning views over the whole island.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7618, lng: 24.5155, label: 'Pollonia Village', num: 1, cat: 'attraction', desc: 'Charming whitewashed village facing Kimolos island' },
        { lat: 36.7575, lng: 24.4650, label: 'Phylakopi', num: 2, cat: 'attraction', desc: 'Bronze Age archaeological site — 5,000 years of history' },
        { lat: 36.7618, lng: 24.5155, label: 'Gialos tis Pollonias', num: 3, cat: 'restaurant', desc: 'Beachfront taverna under tamarisk trees' },
        { lat: 36.6830, lng: 24.3870, label: 'Tsigrado Beach', num: 4, cat: 'attraction', desc: 'Secret beach accessed by climbing through a cliff crack' },
        { lat: 36.6780, lng: 24.4050, label: 'Agia Kiriaki Beach', num: 5, cat: 'attraction', desc: 'Sheltered dark-sand beach — best for swimming in March' },
        { lat: 36.7262, lng: 24.4460, label: 'Bakaliko tou Galani', num: 6, cat: 'restaurant', desc: 'Wine bar and mezze — curated Greek wines with local plates' }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData);
