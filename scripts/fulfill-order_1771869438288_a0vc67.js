const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771869438288_a0vc67',
  email: 'gianni.gulletta@gmail.com',
  destination: 'Sirmione, BS, Italia',
  startDate: '2026-06-27',
  endDate: '2026-07-04',
  groupSize: '3-4',
  travelStyle: 'Relaxation, Family-friendly',
  dining: 'Fine dining dinners only',
  budget: 'Under $1,000',
  requests: ''
};

const itineraryData = {
  destination: 'Sirmione, Italy',
  countryEmoji: '🇮🇹',
  title: 'Sirmione & Lake Garda: A Family Escape',
  subtitle: '7 nights of thermal waters, medieval magic & fine lakeside dining for the whole family',
  description: "Rising from the turquoise waters of Lake Garda like a fairy-tale, Sirmione is one of Italy's most enchanting destinations. This compact peninsula offers an extraordinary blend of medieval history, natural healing waters, crystalline beaches, and world-class cuisine — all within easy walking distance. Whether you're soaking in ancient thermal pools, climbing the towers of a 14th-century castle, or watching the sun melt into the Dolomite-framed lake from a candlelit restaurant terrace, Sirmione delivers pure Italian magic at a relaxed family pace.",
  duration: '7 nights',
  dates: 'Jun 27 – Jul 4, 2026',
  budget: '€–€€',
  pace: 'Relaxed',
  bestFor: 'Families · 3–4 people',
  highlights: [
    'Explore the perfectly preserved 14th-century Scaligero Castle and its moat',
    'Soak in the famous sulphurous thermal waters at Aquaria Spa & Thermal Garden',
    'Walk to Jamaica Beach and the Roman ruins of Grotte di Catullo',
    'Sunset boat cruise around the Sirmio peninsula',
    'Fine dining at La Rucola 2.0 and La Speranzina (both Michelin-starred)',
    'Ferry day trip to Bardolino, Lazise, and the eastern shore of Lake Garda',
    'Day trip to Verona — Romeo & Juliet, the Roman amphitheatre, and gelato'
  ],

  essentials: [
    { title: '☀️ Summer in Sirmione', text: 'Late June–early July brings warm, sunny weather (26–32°C). Mornings are perfect for sightseeing before midday heat. Pack sunscreen SPF 50+, hats, and swimwear. Lake water temperature reaches 22–24°C — ideal for swimming.' },
    { title: '🚗 Getting There & Around', text: 'Sirmione is 30 min from Verona Airport (VRN) and 1.5 hrs from Milan. Park at one of the official car parks at the town entrance (Parcheggio Colombare or Parcheggio Nord) — the historic centre is pedestrian-only. The entire old town is walkable.' },
    { title: '👨‍👩‍👧 Family Tips', text: 'Sirmione is highly family-friendly. The pedestrian centre is safe and stroller-accessible on wider lanes. Beaches have shallow entry points great for children. Gardaland theme park is a 25-min drive and a guaranteed crowd-pleaser.' },
    { title: '🍽️ Dining Reservations', text: 'Book fine dining restaurants (especially Michelin-starred La Rucola 2.0 and La Speranzina) at least 2–4 weeks in advance for summer. Dinner reservations in Italy are typically from 7:30–8:00pm. Lunch is noon–2:30pm.' },
    { title: '⛴️ Ferry & Boats', text: 'Navigazione Laghi (NLG) operates regular ferries from Sirmione port to Desenzano, Lazise, Bardolino, and beyond. Schedules and tickets at the port kiosk. Private boat tours depart from the same harbour — book directly on the dock or online.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-27',
      neighborhoods: 'Sirmione Old Town · Scaligero Castle · Piazza Carducci',
      title: 'Arrival — First Steps into the Pearl of Lake Garda',
      description: 'Arrive in Sirmione and let the magic take hold immediately. Cross the ancient moat, wander the medieval lanes, and climb Scaligero Castle for your first sweeping views of the lake. Tonight, a classic Italian lakeside dinner eases you into holiday mode.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive, Check In & First Walk on the Peninsula',
              description: 'Park at the entrance car parks and walk across the iconic bridge into Sirmione\'s medieval heart. Your first glimpse of the turquoise lake shimmering beyond the castle walls is unforgettable. Settle into your accommodation and take a relaxed orientation stroll through the town.',
              details: [
                '🅿️ Parcheggio Nord or Colombare — €2–3/hr, long-stay available',
                '🏨 Recommend Hotel Catullo, Villa Rosa, or Hotel Sirmione for central locations',
                '🌊 The peninsula is only 3.5km long — everything is walkable',
                '📸 First photo op: the castle reflected in the lake from the drawbridge'
              ]
            },
            {
              title: 'Scaligero Castle (Castello Scaligero)',
              description: 'One of Italy\'s best-preserved medieval fortresses, dating to the 14th century. Climb the towering keep for panoramic views over the entire peninsula and lake. The castle\'s fortified harbour — where wooden boats once sheltered — is a highlight for kids and adults alike.',
              details: [
                '🏰 Open Tue–Sun, 8:30am–7:30pm (summer). Closed Mondays',
                '🎟️ Entry ~€6 adults, €3 EU citizens 18–25, free under 18',
                '👧 Kids love climbing the battlements and looking out the arrow-slit windows',
                '⏱️ Allow 45–60 minutes inside'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Visit the castle in the late afternoon when the light is golden and crowds begin to thin. The views from the tower at sunset hour are outstanding.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening Passeggiata Through the Old Town',
              description: 'Join the Italian tradition of the evening stroll. The narrow lanes of Sirmione come alive at dusk — artisan shops, gelaterias, and the lively Piazza Carducci are perfect for people-watching and stretching your legs before dinner.',
              details: [
                '🍦 Stop at Gelateria Pontile or Bar Fioreria for artisan gelato',
                '🛍️ Browse local olive oil, limoncello, and Garda wine shops',
                '🌅 Piazza Carducci overlooks the lake — excellent sunset spot'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ristorante Risorgimento',
              description: 'A Sirmione institution since 1918, located on Piazza Carducci with beautiful lake views. Their signature semolina pasta from Benedetto Cavalieri and freshly caught lake fish make for an elegant, authentic first dinner. Ask for a terrace table.',
              meta: '💰 $$$ · 📍 Piazza Carducci, Sirmione · Reservations recommended in summer'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4930, lng: 10.6097, label: 'Scaligero Castle', num: 1, cat: 'attraction', desc: '14th-century fortress with tower views over Lake Garda' },
        { lat: 45.4932, lng: 10.6106, label: 'Sirmione Old Town', num: 2, cat: 'attraction', desc: 'Medieval pedestrian centre with narrow lanes and shops' },
        { lat: 45.4928, lng: 10.6115, label: 'Piazza Carducci', num: 3, cat: 'attraction', desc: 'Central square overlooking the lake — perfect for passeggiata' },
        { lat: 45.4929, lng: 10.6112, label: 'Ristorante Risorgimento', num: 4, cat: 'food', desc: 'Century-old lakeside restaurant — Day 1 dinner' }
      ]
    },
    {
      num: 2,
      date: '2026-06-28',
      neighborhoods: 'Aquaria Thermal Spa · Lido delle Bionde · Santa Maria della Neve',
      title: 'Thermal Waters & Beach Day — Pure Relaxation',
      description: 'Today is for pure indulgence. Sirmione\'s famous sulphurous thermal waters have been healing visitors since Roman times. Spend the morning in the Aquaria Thermal Garden, then cool off at the lovely Lido delle Bionde beach. Tonight, a Michelin-starred dinner caps off the perfect Italian day.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Aquaria Thermal Spa & Thermal Garden',
              description: 'The crown jewel of Sirmione — 10,000 sq metres of thermal pools, waterfalls, hydromassage jets, and lake-view terraces. The natural sulphurous salso-bromo-iodine water springs directly from the lake bed at 69°C and is cooled to a perfect soaking temperature. Children love the outdoor pools, while adults can try the full spa treatments.',
              details: [
                '🏊 Open daily 9:00am–10:00pm in summer',
                '🎟️ Day entry ~€35–45 adults, reduced rates for children',
                '📍 Piazza Don A. Piatti 1, just 2 min walk from Scaligero Castle',
                '💆 Book spa treatments (massages, facials) in advance at termedisirmione.com',
                '🌊 Outdoor thermal pools face directly onto Lake Garda — stunning views',
                '👙 Bring towels, swimwear, and water shoes or sandals'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Arrive when it opens at 9am for the calmest experience. By midday in July it gets busy. You can leave and return same-day with your wristband.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lido delle Bionde Beach',
              description: 'A short walk from the old town, Lido delle Bionde is one of Sirmione\'s most popular beaches with a beautiful promenade lined with olive and cypress trees. The clear, shallow water is perfect for families. Rent sun loungers and umbrellas for a proper Italian beach afternoon.',
              details: [
                '🏖️ Mixed sand and pebble beach with gentle lake entry — great for kids',
                '⛱️ Lounger + umbrella hire ~€10–15 per set',
                '🍹 Beach bars serve aperitivo, granita, and snacks',
                '📍 Via Antiche Mure — 5 min walk from town centre'
              ]
            },
            {
              title: 'Church of Santa Maria della Neve',
              description: 'A quick cultural stop on your way back to town — this 15th-century church in the historic centre holds beautiful Renaissance frescoes and a Roman milestone in the portico. Takes just 15 minutes but adds depth to your Sirmione experience.',
              details: [
                '⛪ Free entry, usually open mornings and late afternoons',
                '🖼️ Look for the carved wooden Madonna and the faded frescoes',
                '📍 Via Santa Maria Maggiore, historic centre'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Rucola 2.0 ⭐ Michelin',
              description: 'Tucked into a charming alley beside the Scaligero Castle, La Rucola 2.0 is Sirmione\'s most celebrated fine dining destination. The one Michelin-starred kitchen focuses on creative fish dishes — carpaccio of lake carp, risotto with perch and saffron, and exquisite desserts. Elegant yet welcoming for families.',
              meta: '💰 $$$$ · 📍 Vicolo Strentelle 7, Sirmione · Book weeks ahead for summer'
            }
          ],
          tips: [
            { type: 'tip', text: 'La Rucola 2.0 is small — just a handful of tables. If you can\'t get a reservation, their sister restaurant La Rucola (same street) offers similar quality at slightly lower prices.' }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4926, lng: 10.6101, label: 'Aquaria Thermal Spa', num: 1, cat: 'attraction', desc: '10,000 sqm thermal wellness complex overlooking Lake Garda' },
        { lat: 45.4942, lng: 10.6141, label: 'Lido delle Bionde', num: 2, cat: 'attraction', desc: 'Family-friendly beach with clear lake water and lounger hire' },
        { lat: 45.4933, lng: 10.6108, label: 'Santa Maria della Neve', num: 3, cat: 'attraction', desc: '15th-century church with Renaissance frescoes' },
        { lat: 45.4931, lng: 10.6095, label: 'La Rucola 2.0', num: 4, cat: 'food', desc: 'Michelin-starred fine dining beside the castle — Day 2 dinner' }
      ]
    },
    {
      num: 3,
      date: '2026-06-29',
      neighborhoods: 'Grotte di Catullo · Jamaica Beach · Peninsula Boat Cruise',
      title: 'Roman Ruins, Wild Beach & Sunset on the Water',
      description: 'Explore the far end of the peninsula where ancient Rome meets pristine nature. Visit the remarkable ruins of a 1st-century Roman villa, swim at the wild rocky beach at the peninsula\'s tip, then glide around Sirmione by boat as the sun sets. Fine dining closes a perfect day.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grotte di Catullo — Roman Villa & Museum',
              description: 'A 20-minute walk along the olive-tree-lined path to the northern tip of the peninsula brings you to one of the largest and best-preserved Roman private residences in Northern Italy. Built in the 1st century BC, the ruins sprawl across 2 hectares with terraces overlooking the lake. The onsite museum displays Roman artefacts found during excavations.',
              details: [
                '🏛️ Open Tue–Sun 8:30am–7:30pm (summer); closed Mondays',
                '🎟️ Entry ~€6 adults, free under 18 with EU citizenship',
                '⏱️ Allow 1–1.5 hours to explore properly',
                '🌿 The walk through the olive grove to get here is beautiful in itself',
                '📍 Via Catullo — 20 min walk from town centre'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Jamaica Beach',
              description: 'Just beyond the Grotte di Catullo, Jamaica Beach is the wild, rocky tip of the Sirmio peninsula. Unlike typical sandy beaches, this is smooth flat rocks — beloved by locals for sunbathing and diving directly into the brilliantly clear lake. There\'s also a small sandy area under the trees with sun loungers and a casual bar.',
              details: [
                '🪨 Rocky flat stones perfect for sunbathing — bring a mat',
                '🤿 Excellent snorkelling directly off the rocks — water is very clear',
                '🌳 Sandy shaded area behind with loungers and a snack bar',
                '📍 15-min walk north from Grotte di Catullo',
                '👧 Kids love jumping off the flat rocks — water is usually calm in summer'
              ]
            },
            {
              title: 'Peninsula Boat Cruise',
              description: 'Board a private or shared boat from Sirmione harbour for a guided cruise around the entire Sirmio peninsula. Seeing Sirmione from the water — the castle, the thermal springs (visible as bubbles rising from the lake bed), the Roman ruins, and the villa-dotted hillsides — is a completely different perspective. The sunset cruise is highly recommended.',
              details: [
                '⛵ We Float Sirmione, Beeboatservice, or harbour operators — book at the port',
                '🕐 Peninsula circuit: 30–45 min. Extended Lake Garda tours: 2–4 hours',
                '🌅 Sunset cruise (around 7pm in late June): ~€30–40pp for shared tour',
                '🚢 For the family, a private boat hire is ~€80–120/hr',
                '📍 Departs from Sirmione Port (Porto di Sirmione)'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Casual lunch at Jamaica Beach Bar',
              description: 'The small beach bar at Jamaica Beach serves excellent bruschetta, panini, and cold drinks. Nothing fancy — but eating with your feet in the sand overlooking the crystal-clear lake is the perfect Italian lunch.',
              meta: '💰 $ · 📍 Jamaica Beach, tip of peninsula · Cash friendly'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Speranzina ⭐ Michelin',
              description: 'The other Michelin-starred gem of Sirmione, La Speranzina sits above the lake with a breathtaking terrace view. Chef Fabrizio Lanzini\'s cuisine celebrates local ingredients — Lake Garda fish, seasonal vegetables, and Lugana wines — in sophisticated, beautifully plated dishes. An unmissable evening.',
              meta: '💰 $$$$ · 📍 Via Dante 16, Sirmione · Book 2–4 weeks ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.5014, lng: 10.6112, label: 'Grotte di Catullo', num: 1, cat: 'attraction', desc: '1st-century BC Roman villa ruins with museum and lake views' },
        { lat: 45.5032, lng: 10.6107, label: 'Jamaica Beach', num: 2, cat: 'attraction', desc: 'Wild rocky beach at the peninsula tip — clear water, local favourite' },
        { lat: 45.4925, lng: 10.6089, label: 'Sirmione Port', num: 3, cat: 'attraction', desc: 'Departure point for peninsula boat cruises and lake ferries' },
        { lat: 45.4940, lng: 10.6130, label: 'La Speranzina', num: 4, cat: 'food', desc: 'Michelin-starred lakeside fine dining — Day 3 dinner' }
      ]
    },
    {
      num: 4,
      date: '2026-06-30',
      neighborhoods: 'Desenzano del Garda · Lazise · Eastern Shore',
      title: 'Lake Garda by Ferry — Charming Towns of the Eastern Shore',
      description: 'Take the ferry across Lake Garda for a day exploring the colourful medieval towns of the eastern shore. Desenzano\'s Roman mosaics, Lazise\'s Venetian customs house, and Bardolino\'s wine culture give you a taste of Garda\'s remarkable diversity. Back to Sirmione for fine dining.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ferry to Desenzano del Garda',
              description: 'Board the Navigazione Laghi ferry from Sirmione port — a scenic 20-minute crossing to Desenzano, the largest town on Lake Garda. Visit the remarkable Roman Villa (Villa Romana di Desenzano) with its extraordinary 3rd-century floor mosaics, one of the finest in Northern Italy.',
              details: [
                '⛴️ Navigazione Laghi ferries run hourly — buy tickets at the port kiosk',
                '🎟️ Ferry return ~€8–12 per person; day passes available',
                '🏛️ Villa Romana: open Tue–Sun, entry ~€4. Mosaics are stunning',
                '🛍️ Desenzano\'s old port and Piazza Malvezzi are great for morning coffee',
                '📍 20-minute ferry from Sirmione'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Morning Coffee',
              name: 'Bar in Piazza Malvezzi, Desenzano',
              description: 'Grab an espresso and cornetto at any bar on Desenzano\'s beautiful central square. Italians do breakfast standing at the bar — it\'s faster and half the price.',
              meta: '💰 $ · 📍 Piazza Malvezzi, Desenzano del Garda'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lazise — The Venetian Jewel',
              description: 'Hop back on the ferry north to Lazise — one of Lake Garda\'s most picturesque medieval villages. The Venetian customs house (Dogana Veneta), the perfectly preserved Visconti castle, and the ancient town walls make it feel like a film set. Stroll the promenade and browse the artisan boutiques.',
              details: [
                '🏰 Lazise Castle and Venetian Customs House — free to see from outside',
                '🛍️ Excellent artisan shops along the lakefront promenade',
                '🍦 Try the local gelato — Lazise has several excellent gelaterias',
                '📍 Lazise: ferry north from Desenzano (~45 min)'
              ]
            }
          ],
          meals: [
            {
              type: '🍝 Lunch',
              name: 'Osteria Al Portichetto, Lazise',
              description: 'A charming osteria on Lazise\'s waterfront serving honest Veronese cucina — bigoli with duck ragù, lake fish, and the local Custoza white wine. Perfect lakefront lunch setting.',
              meta: '💰 $$ · 📍 Lazise waterfront · Book ahead for terrace table'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return Ferry to Sirmione',
              description: 'Take the late-afternoon ferry back to Sirmione — the lake in the golden evening light is extraordinary. The silhouette of the castle growing larger as you approach is one of the trip\'s most memorable moments.',
              details: [
                '⛴️ Last ferry from Lazise to Sirmione usually around 7–8pm in summer',
                '🌅 Try to get the 6:30pm departure for the best light',
                '📸 The view of Sirmione\'s peninsula from the lake is iconic'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ristorante Tancredi',
              description: 'Back in Sirmione, Tancredi overlooks Lake Garda from a beautiful terrace. The menu blends Mediterranean tradition with modern creativity — fresh pasta, lake fish, and seasonal vegetables, paired with an excellent Lugana white wine selection.',
              meta: '💰 $$$ · 📍 Via Catullo, Sirmione · Terrace dining with lake views'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4665, lng: 10.5361, label: 'Desenzano del Garda', num: 1, cat: 'attraction', desc: 'Largest Lake Garda town — Roman villa with extraordinary mosaics' },
        { lat: 45.5048, lng: 10.7321, label: 'Lazise', num: 2, cat: 'attraction', desc: 'Perfectly preserved medieval village with Venetian customs house' },
        { lat: 45.4925, lng: 10.6089, label: 'Sirmione Ferry Port', num: 3, cat: 'attraction', desc: 'Navigazione Laghi departures — tickets at port kiosk' },
        { lat: 45.4929, lng: 10.6112, label: 'Ristorante Tancredi', num: 4, cat: 'food', desc: 'Lakeside fine dining with terrace views — Day 4 dinner' }
      ]
    },
    {
      num: 5,
      date: '2026-07-01',
      neighborhoods: 'Gardaland · Peschiera del Garda · Sirmione Old Town',
      title: 'Gardaland Day — Italy\'s Best Theme Park',
      description: 'A guaranteed highlight for the kids: Gardaland, Italy\'s most visited theme park and one of Europe\'s best, is just 25 minutes by car from Sirmione. Spend the day on rides, shows, and family adventures. Return to Sirmione in the evening for a well-earned fine dinner.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gardaland Theme Park',
              description: 'Home to over 40 rides and attractions across themed worlds, Gardaland is an all-ages adventure. Highlights include the Oblivion ride, Raptor roller coaster, the magical Magic Mountain, and the Peppa Pig Land for younger children. The park opens at 10am — arrive early to beat the queues.',
              details: [
                '🎢 Park opens 10:00am daily in summer; closes 10–11pm',
                '🎟️ Online tickets: ~€40–50 adults, €35–45 children (under 100cm free)',
                '🚗 Drive from Sirmione: 25 min via SS249 towards Peschiera',
                '🅿️ On-site parking ~€8–10. Arrive by 9:30am for first rides',
                '📍 Via Derna 4, Castelnuovo del Garda, Verona',
                '💡 Buy tickets online in advance to skip the box office queue'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Gardaland is very busy in July. Rent a Q-Rapid Fast Pass for the biggest rides to skip the longest queues — worth it with kids.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Continue at Gardaland — Shows & Sea Life',
              description: 'Gardaland SEA LIFE Aquarium is right next to the main park — a separate ticket but wonderful for younger children with shark tanks, jellyfish, and a coral reef tunnel. The park also has a water park section (Legoland Water Park) perfect for hot July afternoons.',
              details: [
                '🦈 SEA LIFE Aquarium: ~€18 adults, €14 children (combo tickets available)',
                '💦 Legoland Water Park: included with main Gardaland ticket',
                '🎭 Live shows throughout the day at the main theatre — check the schedule',
                '🍕 Eat inside the park or picnic in the designated areas'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tavernetta Maria Callas',
              description: 'Back in Sirmione, this refined restaurant sits within the walls of the castle area — named in honour of Maria Callas who lived on the peninsula. The kitchen respects seasonal cycles, delivering beautifully balanced dishes and an excellent wine list in a welcoming, historic atmosphere.',
              meta: '💰 $$$ · 📍 Via Piana 25, Sirmione · Book ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'After Gardaland, freshen up at your hotel before dinner — a quick swim in the pool or a shower does wonders. Italians dress well for dinner even in summer.' }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4619, lng: 10.7139, label: 'Gardaland Theme Park', num: 1, cat: 'attraction', desc: 'Italy\'s best theme park — 40+ rides, shows, and family fun' },
        { lat: 45.4319, lng: 10.6983, label: 'Gardaland SEA LIFE Aquarium', num: 2, cat: 'attraction', desc: 'Underwater tunnels, sharks, and coral reefs next to Gardaland' },
        { lat: 45.4928, lng: 10.6113, label: 'Tavernetta Maria Callas', num: 3, cat: 'food', desc: 'Refined seasonal restaurant near the castle walls — Day 5 dinner' }
      ]
    },
    {
      num: 6,
      date: '2026-07-02',
      neighborhoods: 'Sirmione Spa · San Pietro in Mavino · Old Town · Harbour Sunset',
      title: 'Slow Day — Spa, Church & Sunset Aperitivo',
      description: 'A gentler day to recharge. Morning wellness at the thermal spa, a visit to the oldest church on the peninsula, and a long lazy afternoon at the beach. As the sun dips toward the mountains, enjoy a sunset aperitivo on the castle terrace — then fine dining by the lake.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Return to Aquaria Spa — Treatments & Relaxation',
              description: 'If yesterday was action-packed, today is for restoration. Book in advance for a thermal massage, hydro-massage session, or a facial treatment at Aquaria. The outdoor pools facing the lake are extraordinary — lie in warm sulphurous water and watch boats drift across Lake Garda.',
              details: [
                '💆 Book treatments online at termedisirmione.com',
                '🏊 Morning is calmer — the spa fills up by midday',
                '🌡️ Pool temperature ~35–38°C year-round',
                '☕ The spa café serves light breakfast and healthy snacks'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Church of San Pietro in Mavino',
              description: 'One of the oldest churches in the entire Lake Garda region, San Pietro in Mavino was founded in the 8th century. Tucked among olive trees near the tip of the peninsula, it offers an evocative visit and an extraordinary elevated view over the peninsula and surrounding lake.',
              details: [
                '⛪ Usually open afternoons, donations welcome',
                '🫒 The olive grove surrounding the church is centuries old',
                '👀 Views from the churchyard extend to both sides of Lake Garda',
                '📍 Via San Pietro, Sirmione — 15 min walk from old town'
              ]
            },
            {
              title: 'Beach & Swim at Punta Staffalo',
              description: 'Sirmione has smaller, quieter beach spots away from the main Lido. Punta Staffalo on the western side of the peninsula offers clear water and a more local atmosphere — perfect for a quiet family swim.',
              details: [
                '🏊 Bring your own towels and snorkelling gear',
                '💧 Lake water in July is 22–24°C — perfectly swimmable',
                '📍 Western side of the peninsula, near the spa complex'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Osteria Al Torcol',
              description: 'A beautiful osteria in the heart of Sirmione\'s old town, Al Torcol crafts dishes with premium ingredients and creative pairings. Their pasta and lake fish are exceptional — matched by an extensive selection of local and national wines.',
              meta: '💰 $$ · 📍 Via San Salvatore 30, Sirmione · Lovely courtyard setting'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Aperitivo at the Castle Moat',
              description: 'Pull up a chair at one of the bars along the castle moat and watch the sun sink behind the Western Alps while sipping a Campari Spritz or the local Lugana Bianco. In Italy, aperitivo (6–8pm) is practically a religion — it\'s how the evening should begin.',
              details: [
                '🍹 Spritz Campari or Aperol Spritz: €5–8',
                '🧀 Most bars include small nibbles (olives, chips) with aperitivo',
                '📍 Anywhere along Via Dante or Piazza Carducci has views',
                '🌄 Sunset in late June/early July is around 9:00pm — plan accordingly'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Villa Pioppi',
              description: 'A stunning early 1900s Art Nouveau villa on the shores of Lake Garda, Villa Pioppi serves contemporary Mediterranean cuisine that highlights local products. The setting — candlelit tables in an historic lakeside villa — is genuinely magical.',
              meta: '💰 $$$ · 📍 Via Pioppi, Sirmione · Reserve for lakeside terrace'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4926, lng: 10.6101, label: 'Aquaria Thermal Spa', num: 1, cat: 'attraction', desc: 'Morning wellness — thermal pools and treatments' },
        { lat: 45.4987, lng: 10.6109, label: 'Church of San Pietro in Mavino', num: 2, cat: 'attraction', desc: '8th-century church with views over both sides of the lake' },
        { lat: 45.4933, lng: 10.6083, label: 'Punta Staffalo Beach', num: 3, cat: 'attraction', desc: 'Quiet local beach on the western side of the peninsula' },
        { lat: 45.4931, lng: 10.6109, label: 'Osteria Al Torcol', num: 4, cat: 'food', desc: 'Artisan osteria with creative pairings and local wine — lunch' },
        { lat: 45.4942, lng: 10.6125, label: 'Villa Pioppi', num: 5, cat: 'food', desc: 'Art Nouveau lakeside villa restaurant — Day 6 dinner' }
      ]
    },
    {
      num: 7,
      date: '2026-07-03',
      neighborhoods: 'Verona — Arena · Juliet\'s House · Piazza Bra',
      title: 'Day Trip to Verona — Romeo, Juliet & the Roman Arena',
      description: 'Verona, UNESCO World Heritage City and eternal stage for Shakespeare\'s greatest love story, is just 35 minutes from Sirmione. Spend the day exploring the Roman arena, the medieval old town, and Juliet\'s famous courtyard. Return to Sirmione for a farewell fine dinner.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Verona & Piazza Bra',
              description: 'Leave by 9am and arrive in Verona before the crowds build. Park at Parking Piazza Cittadella or Porta Nuova and walk to the stunning Piazza Bra, dominated by the ancient Roman amphitheatre. The Arena di Verona is the third-largest Roman amphitheatre still standing — it seats 15,000 and still hosts summer opera.',
              details: [
                '🚗 Sirmione to Verona: 35–40 min via A22/SS12',
                '🅿️ Parcheggio Piazza Cittadella: central and well-priced',
                '🏛️ Arena di Verona: open daily, entry ~€10. Opera season runs June–Sept',
                '📍 Piazza Bra, Verona — the heart of the city'
              ]
            },
            {
              title: "Casa di Giulietta — Juliet's House",
              description: "The legendary balcony where Juliet supposedly stood waiting for Romeo. Whether you believe the story or not, the medieval courtyard and balcony are genuinely atmospheric. Touch the bronze Juliet statue (said to bring luck in love), and read the thousands of love letters plastered on the entrance wall.",
              details: [
                '❤️ Free to enter the courtyard; balcony and museum ~€6',
                '📸 Arrive early — the courtyard gets very crowded by 11am',
                '📍 Via Cappello 23, Verona — 5-min walk from the Arena'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Explore Verona\'s Medieval Old Town',
              description: 'Wander through Piazza delle Erbe — the ancient Roman forum, now a colourful market square — and into Piazza dei Signori. Climb Torre dei Lamberti (84m) for the best views over the city\'s rooftops and the river Adige snaking through it. Verona\'s palaces, fountains, and frescoed facades are breathtaking.',
              details: [
                '🗼 Torre dei Lamberti: entry ~€6, great city panorama',
                '🛒 Piazza delle Erbe: daily market with local produce and souvenirs',
                '🏛️ Arco dei Gavi and Castelvecchio (medieval castle) are nearby',
                '🍦 Best gelato in Verona: Gelateria Savoia near Piazza Bra'
              ]
            }
          ],
          meals: [
            {
              type: '🍝 Lunch',
              name: 'Trattoria al Pompiere, Verona',
              description: 'A Veronese institution since 1972, Al Pompiere serves the finest traditional Veronese cuisine: pasta e fasoi (pasta and beans), risotto all\'Amarone, and braised horse (a local speciality, if adventurous). Excellent wine cellar with Amarone and Valpolicella.',
              meta: '💰 $$$ · 📍 Vicolo Regina d\'Ungheria 5, Verona · Book ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Sirmione',
              description: 'Drive back to Sirmione by late afternoon. The sight of the castle rising from the lake as you approach the peninsula never gets old — it\'s been seven days and it still takes your breath away.',
              details: [
                '🚗 Return journey: 35–40 min',
                '🌅 Arrive in time for a quick sunset walk before dinner'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Casa dei Pescatori',
              description: 'A farewell dinner at this beautiful lakeside restaurant celebrating local, sustainable ingredients. The kitchen blends Mediterranean tradition with modern flair — organic lake fish, seasonal vegetables, and refined pairings. Simple elegance for your penultimate evening.',
              meta: '💰 $$$ · 📍 Via Piana 22, Sirmione · Lakefront terrace'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4386, lng: 10.9939, label: 'Arena di Verona', num: 1, cat: 'attraction', desc: 'Ancient Roman amphitheatre — third largest in the world' },
        { lat: 45.4416, lng: 10.9980, label: "Juliet's House (Casa di Giulietta)", num: 2, cat: 'attraction', desc: 'The legendary balcony — medieval courtyard and bronze statue' },
        { lat: 45.4424, lng: 10.9974, label: 'Piazza delle Erbe', num: 3, cat: 'attraction', desc: 'Ancient Roman forum — daily market and stunning architecture' },
        { lat: 45.4413, lng: 10.9954, label: 'Trattoria al Pompiere', num: 4, cat: 'food', desc: 'Veronese institution since 1972 — traditional cuisine and Amarone' },
        { lat: 45.4929, lng: 10.6112, label: 'Casa dei Pescatori', num: 5, cat: 'food', desc: 'Sustainable lakeside fine dining — Day 7 farewell dinner' }
      ]
    },
    {
      num: 8,
      date: '2026-07-04',
      neighborhoods: 'Sirmione Old Town · Castle Moat · Departure',
      title: 'Final Morning — Last Gelato & Arrivederci',
      description: 'Your last morning in paradise. A slow breakfast, a final walk past the castle, one last gelato by the moat, and a bittersweet drive away from the most beautiful peninsula in Italy. Sirmione doesn\'t let go easily.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Slow Breakfast & Last Old Town Walk',
              description: 'Linger over a proper Italian breakfast — cornetto caldo and cappuccino at a bar on Piazza Carducci. Take a final slow walk through the old town. Buy a bottle of local Lugana Bianco wine, some limoncello, or a jar of Garda olive oil as the perfect souvenir.',
              details: [
                '☕ Bar Centrale or any bar on Piazza Carducci for breakfast',
                '🛒 Best souvenir shops are on Via Vittorio Emanuele',
                '🍋 Local products: Garda olive oil, Lugana white wine, limoncello del Garda',
                '🏰 Last photo from the castle drawbridge before checking out'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bar Centrale, Piazza Carducci',
              description: 'Stand at the bar like a local. Cornetto (croissant) and a perfect cappuccino — don\'t order a cappuccino after 11am in Italy, it\'s a cardinal sin. Enjoy the morning buzz of the square one last time.',
              meta: '💰 $ · 📍 Piazza Carducci, Sirmione · Cash or card'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Last Gelato & Departure',
              description: 'Pick up one final artisan gelato from Gelateria Pontile — try the fig and honey or the Lake Garda lemon. Walk to the castle moat for a last look at the turquoise water and the medieval walls. Then load the car, breathe in the lake air one last time, and drive away.',
              details: [
                '🍦 Gelateria Pontile or Gelateria Bardolino — both excellent',
                '📸 Final photo opportunity at the entrance drawbridge',
                '🚗 Check-out times usually noon — ask hotel for late check-out if needed',
                '✈️ Verona Airport: 35 min. Milan Malpensa: 1.5 hrs. Milan Linate: 1.5 hrs'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Already planning your return? Summer is magical but September–October brings quieter crowds, warm weather, and spectacular autumn light on the lake. Sirmione in the off-season is a different kind of perfect.' }
          ]
        }
      ],
      mapPins: [
        { lat: 45.4928, lng: 10.6115, label: 'Piazza Carducci', num: 1, cat: 'attraction', desc: 'Final breakfast spot — cornetto and cappuccino by the lake' },
        { lat: 45.4930, lng: 10.6097, label: 'Scaligero Castle Drawbridge', num: 2, cat: 'attraction', desc: 'Last photo opportunity — the iconic castle entrance' },
        { lat: 45.4927, lng: 10.6108, label: 'Gelateria Pontile', num: 3, cat: 'food', desc: 'Artisan gelato — final taste of Sirmione' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per night)', budget: '€80–120/night', midrange: '€120–200/night', luxury: '€200–400/night' },
    { category: 'Meals (fine dining dinner, 3–4 people)', budget: '€80–100', midrange: '€100–180', luxury: '€180–300' },
    { category: 'Thermal Spa (Aquaria, per person)', budget: '€35/day', midrange: '€50 with treatment', luxury: '€80+ full spa day' },
    { category: 'Gardaland (per person)', budget: '€40 online', midrange: '€50 at gate', luxury: '€60 + fast pass' },
    { category: 'Boat tours & ferries', budget: '€10–20/day', midrange: '€30–50/day', luxury: '€80–120/hr private boat' },
    { category: 'Activities & entry fees', budget: '€15–30/day', midrange: '€30–60/day', luxury: '€60–100/day' },
    { category: '7-Night Total (family of 4)', budget: '€2,500–4,000', midrange: '€4,000–7,000', luxury: '€7,000–12,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Verona Villafranca Airport (VRN): 30 min drive to Sirmione', 'Milan Malpensa (MXP): 1 hr 30 min drive', 'Milan Linate (LIN): 1 hr 20 min drive', 'Train to Desenzano station + taxi/bus to Sirmione (20 min)'] },
    { title: '🏨 Where to Stay', items: ['Hotel Catullo — central, pool, family rooms (mid-range)', 'Hotel Sirmione e Promessi Sposi — lakeview, thermal access (mid-luxury)', 'Grand Hotel Terme — historic lakeside hotel with spa (luxury)', 'Villa Rosa — boutique guesthouse, excellent value (budget-mid)', 'Book early for summer — Sirmione fills up by March for July'] },
    { title: '🌡️ Weather in Late June / Early July', items: ['Average high 28–32°C (82–90°F); overnight lows 18–20°C', 'Lake Garda water temperature: 22–24°C — perfect swimming', 'Very occasional afternoon thunderstorms that pass quickly', 'Strong UV — SPF 50+, hats, and sunglasses essential', 'Long daylight hours: sunrise ~5:40am, sunset ~9:00pm'] },
    { title: '💳 Money & Tips', items: ['Italy uses Euros (€). ATMs widely available', 'Cards accepted everywhere in Sirmione, but carry €20–30 cash for beach bars and small shops', 'Tipping: 5–10% at fine dining restaurants is appreciated but not obligatory', 'Avoid tourist-trap restaurants near the main entrance — walk 5 min deeper into town for better value'] },
    { title: '📱 Connectivity & Transport', items: ['Italian SIMs available at newsagents (Vodafone, TIM, WindTre)', 'Free WiFi in most hotels, bars, and cafés', 'Sirmione centre is pedestrian-only — park outside and walk in', 'Taxis available outside the town gate; Uber doesn\'t operate on the lake'] },
    { title: '🇮🇹 Local Tips', items: ['Lunch is sacred: 12:30–2:30pm. Many shops close for riposo (siesta)', 'Dinner starts late: locals eat 8:00–9:30pm. Reserve for 8pm', 'Dress neatly for fine dining — smart casual is the standard', 'Learning a few Italian words goes a long way: "grazie," "per favore," "il conto, per favore" (the bill, please)'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
