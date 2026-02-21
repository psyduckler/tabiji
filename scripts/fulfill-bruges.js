const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771633962141_3ntibd',
  email: 'psyduckler@gmail.com',
  destination: 'Bruges, Belgium',
  startDate: '2026-06-24',
  endDate: '2026-06-28',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Bruges, Belgium',
  countryEmoji: '🇧🇪',
  title: 'Medieval Magic: Solo in Bruges',
  subtitle: '5 days of Flemish masters, canal wandering & Belgian indulgence for one',
  description: "Bruges is a fairy-tale city frozen in medieval amber — winding canals, cobblestone lanes, soaring belfries, and world-class art behind every corner. This solo cultural itinerary immerses you in Flemish painting, Gothic architecture, Belgian beer culture, and artisan chocolate. Late June brings long golden evenings, outdoor café culture, and the city at its most enchanting. Travel at your own pace, linger in museums, and lose yourself in one of Europe's most perfectly preserved cities.",
  duration: '4 nights',
  dates: 'Jun 24 – Jun 28, 2026',
  budget: '$$',
  pace: 'Relaxed',
  bestFor: 'Solo Travelers · Culture Lovers',
  highlights: [
    'Climb the 366 steps of the iconic Belfry of Bruges for panoramic views',
    'See Van Eyck and the Flemish Primitives at the Groeningemuseum',
    'Canal boat cruise through medieval waterways',
    'Tour De Halve Maan — Bruges\' last active city brewery',
    'Discover Michelangelo\'s Madonna at the Church of Our Lady',
    'Chocolate tasting at artisan shops along Katelijnestraat'
  ],

  essentials: [
    { title: '☀️ Late June Weather', text: 'Expect 18–23°C with long daylight until 10pm. Occasional rain showers — pack a light rain jacket and layers for cool evenings. Perfect walking weather.' },
    { title: '🚶 Getting Around', text: 'Bruges\' historic centre is compact and entirely walkable — about 2km across. No car or transit needed. Rent a bike for day trips to Damme along the canal path.' },
    { title: '🎫 Musea Brugge Card', text: 'The Musea Brugge Card (€30) covers 16 museums including Groeningemuseum, Belfry, and Gruuthusemuseum. Pays for itself in 2–3 visits — essential for culture lovers.' },
    { title: '🍺 Beer Culture', text: 'Belgium has over 1,500 beers. In Bruges, try local brews at De Halve Maan (Brugse Zot), \'t Brugs Beertje for rare bottles, and Brewery Bourgogne des Flandres on the canal.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-24',
      neighborhoods: 'Markt · Burg · Historic Centre',
      title: 'Arrival & the Heart of Medieval Bruges',
      description: "Arrive in Bruges and step straight into the Middle Ages. The Markt and Burg squares are the city's beating heart — towering belfry, ornate town hall, and the mysterious Basilica of the Holy Blood. Get oriented with an afternoon of iconic landmarks.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Markt Square & the Belfry',
              description: 'Drop your bags and head to the Markt, Bruges\' central square ringed by colourful guild houses and horse-drawn carriages. Climb the Belfry\'s 366 narrow steps for a breathtaking 360° panorama over the medieval rooftops.',
              details: [
                '🏰 Belfry: €15 entry, last admission 5pm — go early to avoid queues',
                '📸 The view from the top is the single best photo op in Bruges',
                '🔔 Listen for the 47-bell carillon — it plays every 15 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Arriving by train? Bruges station is a 15-minute walk to the Markt, or take any bus to Centrum. The walk along \'t Zand square is lovely.' }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Burg Square & Basilica of the Holy Blood',
              description: 'Just steps from the Markt, Burg Square is more intimate and arguably more beautiful. Visit the Basilica of the Holy Blood, a 12th-century chapel housing a relic believed to contain Christ\'s blood. The upper chapel is a riot of Gothic colour.',
              details: [
                '⛪ Free entry to the basilica, €5 for the treasury museum',
                '🏛️ Admire the Bruges City Hall — the oldest in the Low Countries (1376)',
                '📍 The Gothic Hall inside City Hall has spectacular vaulted ceilings'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Den Dyver',
              description: 'Acclaimed restaurant specializing in beer-paired cuisine — each dish is matched with a specific Belgian beer. Perfect introduction to Bruges\' food culture for a solo diner at the bar.',
              meta: '💰 $$$ · 📍 Dijver 5 · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2093, lng: 3.2247, label: 'Markt Square', num: 1, cat: 'attraction', desc: 'Grand central square with Belfry and guild houses' },
        { lat: 51.2087, lng: 3.2268, label: 'Belfry of Bruges', num: 2, cat: 'attraction', desc: '83m medieval bell tower — 366 steps to panoramic views' },
        { lat: 51.2082, lng: 3.2273, label: 'Burg Square', num: 3, cat: 'attraction', desc: 'Elegant square with City Hall and Basilica' },
        { lat: 51.2083, lng: 3.2280, label: 'Basilica of the Holy Blood', num: 4, cat: 'attraction', desc: '12th-century chapel with sacred relic' },
        { lat: 51.2060, lng: 3.2270, label: 'Den Dyver', num: 5, cat: 'food', desc: 'Beer-paired fine dining on the Dijver canal' }
      ]
    },
    {
      num: 2,
      date: '2026-06-25',
      neighborhoods: 'Dijver · Groeninge · Minnewater',
      title: 'Flemish Masters & Canal Dreams',
      description: "A deep dive into Bruges' artistic soul. Morning with the Flemish Primitives at the Groeningemuseum, afternoon floating through the canals by boat, and a peaceful evening stroll to the Lake of Love.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Groeningemuseum',
              description: 'Home to one of the world\'s finest collections of Flemish Primitive painting. Van Eyck\'s luminous works, Memling\'s portraits, and Bosch\'s fantastical visions — all in an intimate, uncrowded setting. Take your time; this is why you came.',
              details: [
                '🖼️ Don\'t miss: Jan van Eyck\'s "Madonna with Canon van der Paele"',
                '🎨 Covers 600 years of Flemish art from medieval to modern',
                '⏰ Open 9:30am–5pm, closed Mondays — arrive at opening for solitude'
              ]
            },
            {
              title: 'Gruuthusemuseum',
              description: 'Right next door, this palatial 15th-century mansion tells the story of Bruges through decorative arts, tapestries, and a stunning chapel bridge to the Church of Our Lady.',
              details: [
                '🏠 The building itself is as impressive as the collection',
                '🌉 Walk across the private prayer chapel connecting to the church'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Books & Brunch',
              description: 'Cozy café on a quiet side street with excellent salads, quiches, and coffee. Solo-traveler-friendly with books to browse and a peaceful courtyard garden.',
              meta: '💰 $ · 📍 Garenmarkt 30'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Canal Boat Cruise',
              description: 'Board one of the open-top boats at the Dijver landing and glide through Bruges\' medieval waterways. In 30 minutes you\'ll pass under ancient stone bridges, past trailing willows, and see the city from its most magical angle.',
              details: [
                '🚣 €14 per person, boats depart every few minutes from 5 departure points',
                '📸 The view approaching the Bonifacius Bridge is unforgettable',
                '⏰ Runs March–November, 10am–6pm'
              ]
            },
            {
              title: 'Minnewater — Lake of Love',
              description: 'End the afternoon at this tranquil lake surrounded by weeping willows and gliding swans. Legend says couples who cross the bridge will love forever — but it\'s equally magical for a solo moment of reflection.',
              details: [
                '🦢 The swans are here because of a 500-year-old decree by Maximilian of Austria',
                '🌿 The adjacent Begijnhof (Beguinage) is a serene 13th-century courtyard'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Begijnhof closes at 6:30pm. Visit before the canal cruise or right after — the white-washed houses around the garden are hauntingly peaceful.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'De Stoepa',
              description: 'Relaxed world-kitchen restaurant with a sprawling terrace overlooking the Minnewater park. Great for solo dining — order a Belgian beer and watch the swans as the sun sets at 10pm.',
              meta: '💰 $$ · 📍 Oostmeers 124 · Terrace seating in summer'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2050, lng: 3.2265, label: 'Groeningemuseum', num: 1, cat: 'attraction', desc: 'World-class Flemish Primitive paintings including Van Eyck' },
        { lat: 51.2045, lng: 3.2260, label: 'Gruuthusemuseum', num: 2, cat: 'attraction', desc: '15th-century palace museum of Bruges history' },
        { lat: 51.2055, lng: 3.2245, label: 'Canal Boat Landing (Dijver)', num: 3, cat: 'attraction', desc: 'Departure point for canal boat cruises' },
        { lat: 51.1995, lng: 3.2240, label: 'Minnewater (Lake of Love)', num: 4, cat: 'attraction', desc: 'Romantic swan lake with medieval legend' },
        { lat: 51.2005, lng: 3.2242, label: 'Begijnhof', num: 5, cat: 'attraction', desc: 'Serene 13th-century Beguinage courtyard' },
        { lat: 51.1997, lng: 3.2230, label: 'De Stoepa', num: 6, cat: 'food', desc: 'World-kitchen terrace dining by Minnewater park' }
      ]
    },
    {
      num: 3,
      date: '2026-06-26',
      neighborhoods: 'Sint-Anna · Damme · Eastern Bruges',
      title: 'Hidden Bruges & a Bicycle to Damme',
      description: "Leave the tourist centre behind and discover Bruges' quieter, equally charming eastern quarter. Visit lace-makers, windmills on the ramparts, and cycle the tree-lined canal path to the storybook village of Damme.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sint-Anna Quarter & Windmills',
              description: 'Cross the canal east into the Sint-Anna neighbourhood — local, residential, and wonderfully authentic. Walk the old city ramparts where four historic windmills still stand against the sky. Visit the Kantcentrum (Lace Centre) to watch artisans demonstrate Bruges\' famous bobbin lace.',
              details: [
                '🌀 Sint-Janshuismolen windmill is still operational — visit inside (€5)',
                '🧵 Kantcentrum: €8 entry, fascinating live lace demonstrations',
                '📸 The rampart walk from Kruispoort to Dampoort is gorgeous and crowd-free'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cycle to Damme',
              description: 'Rent a bike and ride 7km along the ruler-straight Damme Canal, lined with tall poplars — one of Belgium\'s most scenic cycling routes. Damme is a tiny medieval book village with second-hand bookshops, a ruined church tower, and excellent flemish stew.',
              details: [
                '🚲 Rent from Fietspunt at the train station (~€15/day)',
                '📚 Damme is Belgium\'s official "book village" — browse the outdoor book stalls',
                '🏰 Climb the Damme Town Hall steps for views of the surrounding polders',
                '⏱️ 25 minutes each way — flat and easy cycling'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Tante Marie',
              description: 'Charming Damme restaurant in a historic building serving classic Flemish dishes — try the waterzooi (creamy chicken stew) or stoofvlees (beer-braised beef).',
              meta: '💰 $$ · 📍 Kerkstraat 38, Damme'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Belgian Beer Tasting at \'t Brugs Beertje',
              description: 'Back in Bruges, end the day at this legendary beer bar — tiny, wood-panelled, and stocking over 300 Belgian beers. The owner is a walking encyclopedia. Ask for a Trappist flight or a sour lambic you can\'t find anywhere else.',
              details: [
                '🍺 300+ beers — the menu is a book. Ask the staff for guidance.',
                '📍 Kemelstraat 5 — easy to miss, look for the small sign',
                '🕕 Opens at 4pm, gets busy after 8pm — go early for a good seat'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cambrinus',
              description: 'Brasserie with 400+ beers and hearty Flemish cuisine — perfect for pairing carbonade flamande with a dark abbey ale. Lively atmosphere, great for solo travelers sitting at the long tables.',
              meta: '💰 $$ · 📍 Philipstockstraat 19'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2138, lng: 3.2380, label: 'Sint-Janshuismolen Windmill', num: 1, cat: 'attraction', desc: 'Working windmill on the medieval ramparts' },
        { lat: 51.2125, lng: 3.2350, label: 'Kantcentrum (Lace Centre)', num: 2, cat: 'attraction', desc: 'Live bobbin lace-making demonstrations' },
        { lat: 51.2490, lng: 3.2870, label: 'Damme Village', num: 3, cat: 'attraction', desc: 'Medieval book village at the end of a scenic canal ride' },
        { lat: 51.2090, lng: 3.2260, label: '\'t Brugs Beertje', num: 4, cat: 'food', desc: 'Legendary beer bar with 300+ Belgian beers' },
        { lat: 51.2085, lng: 3.2240, label: 'Cambrinus', num: 5, cat: 'food', desc: 'Brasserie with 400+ beers and Flemish classics' }
      ]
    },
    {
      num: 4,
      date: '2026-06-27',
      neighborhoods: 'Walplein · Katelijnestraat · South Bruges',
      title: 'Beer, Chocolate & Sacred Art',
      description: "Today is pure Belgian indulgence — a morning brewery tour, afternoon chocolate crawl, and a masterpiece by Michelangelo. This is the day where Bruges' sensory pleasures come together.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'De Halve Maan Brewery Tour',
              description: 'Tour Bruges\' last active city-centre brewery, family-run since 1856. Learn about their famous Brugse Zot and Straffe Hendrik beers, climb to the rooftop for stunning views, and end with a tasting. They even built an underground beer pipeline across the city!',
              details: [
                '🍺 Tours run hourly from 11am — €18 includes tasting',
                '📸 The rooftop terrace has one of the best views in Bruges',
                '🔧 The 3km underground beer pipeline (2016) is a modern marvel',
                '🪑 The brewery restaurant XO serves excellent lunch too'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'De Halve Maan Brasserie',
              description: 'Eat right at the brewery — stoofvlees braised in Brugse Zot, paired with a fresh glass of Straffe Hendrik. The courtyard is sunny and relaxed.',
              meta: '💰 $$ · 📍 Walplein 26'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Church of Our Lady & Michelangelo\'s Madonna',
              description: 'Visit this 115-metre brick Gothic church — the second tallest brick tower in the world. Inside, Michelangelo\'s Madonna and Child (1504) sits in quiet majesty. It\'s the only Michelangelo sculpture to leave Italy during his lifetime.',
              details: [
                '⛪ Free entry to the church, €7 for the museum area with the Michelangelo',
                '🗿 The marble Madonna is smaller than expected — but utterly captivating',
                '🪦 Also houses the ornate tombs of Charles the Bold and Mary of Burgundy'
              ]
            },
            {
              title: 'Chocolate Crawl on Katelijnestraat',
              description: 'Bruges has over 50 chocolate shops. Walk down Katelijnestraat and taste your way through the best: The Chocolate Line for avant-garde flavours, Dumon for pure tradition, and Choco-Story museum for the full cocoa-to-praline journey.',
              details: [
                '🍫 The Chocolate Line (Dominique Persoone) — wasabi, bacon, and other wild pralines',
                '🍫 Dumon — family chocolatier since 1992, classic and exceptional',
                '🏛️ Choco-Story Museum: €11 entry, includes tasting — learn 4,000 years of chocolate history',
                '🛍️ Budget ~€20–30 for tasting and gifts'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Golden Hour on the Rozenhoedkaai',
              description: 'The most photographed spot in Bruges: the Rozenhoedkaai (Rosary Quay). Canal boats drift past, medieval buildings reflect in the water, and the Belfry rises behind. In late June, golden hour hits around 9pm — find a bench and savour it.',
              details: [
                '📸 The classic Bruges postcard shot — canals, Belfry, and medieval rooflines',
                '🌅 Golden hour in late June: ~9:00–9:45pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Sans Cravate',
              description: 'Michelin-starred restaurant in a medieval townhouse. Chef Henk Van Oudenhove serves creative Franco-Belgian cuisine. A splurge-worthy solo dinner to remember — request the bar seating for a convivial experience.',
              meta: '💰 $$$$ · 📍 Langestraat 159 · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2035, lng: 3.2250, label: 'De Halve Maan Brewery', num: 1, cat: 'attraction', desc: 'Bruges\' last active brewery — tours, tastings & rooftop views' },
        { lat: 51.2038, lng: 3.2268, label: 'Church of Our Lady', num: 2, cat: 'attraction', desc: 'Gothic church with Michelangelo\'s Madonna & Child' },
        { lat: 51.2020, lng: 3.2255, label: 'The Chocolate Line', num: 3, cat: 'food', desc: 'Avant-garde chocolate by Dominique Persoone' },
        { lat: 51.2032, lng: 3.2248, label: 'Choco-Story Museum', num: 4, cat: 'attraction', desc: '4,000 years of chocolate history with tastings' },
        { lat: 51.2068, lng: 3.2270, label: 'Rozenhoedkaai', num: 5, cat: 'attraction', desc: 'Most photographed canal viewpoint in Bruges' },
        { lat: 51.2115, lng: 3.2225, label: 'Sans Cravate', num: 6, cat: 'food', desc: 'Michelin-starred Franco-Belgian cuisine' }
      ]
    },
    {
      num: 5,
      date: '2026-06-28',
      neighborhoods: 'Markt · Jan van Eyckplein · North Bruges',
      title: 'Morning Markets & Farewell Bruges',
      description: "A final morning to soak in what makes Bruges special. Wander the northern quarter's quieter canals, visit the Jan van Eyck statue, pick up last gifts, and say goodbye to this enchanted city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Jan van Eyckplein & Northern Canals',
              description: 'The handsome square where Jan van Eyck once lived, now marked by his statue gazing over the canal. The surrounding streets — Spinolarei, Spiegelrei — are some of the most beautiful and least crowded in Bruges. Pure medieval atmosphere without the tour groups.',
              details: [
                '📸 Spiegelrei canal with the Poortersloge (Merchants\' Lodge) in frame',
                '🏛️ The nearby Sint-Walburgakerk has a stunning Baroque interior (free)',
                '🚶 This quarter was Bruges\' medieval merchant hub — look for old trading house facades'
              ]
            },
            {
              title: 'Last Waffle & Souvenir Shopping',
              description: 'Grab a final Liège waffle from a street vendor — the caramelized pearl sugar version, warm and crispy. Pick up lace, chocolate, or beer to bring home from the shops along Steenstraat and Breidelstraat.',
              details: [
                '🧇 Liège waffles > Brussels waffles — fight me. Get one plain, no toppings needed.',
                '🍫 Last-minute chocolate: Leonidas for affordable gifts, Dumon for the real stuff',
                '🍺 Bottle shops near the Markt sell packaged Belgian beer gift sets'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'That\'s Toast',
              description: 'Popular brunch spot near the Markt with creative toast combinations, excellent coffee, and a bright modern interior. Solo-friendly with counter seating.',
              meta: '💰 $ · 📍 Hallestraat 8'
            }
          ],
          tips: [
            { type: 'tip', text: 'If departing by train, Bruges station has luggage lockers (€4–6). Store your bags and enjoy the last morning hands-free.' }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2120, lng: 3.2280, label: 'Jan van Eyckplein', num: 1, cat: 'attraction', desc: 'Historic square with Van Eyck statue and canal views' },
        { lat: 51.2130, lng: 3.2290, label: 'Spiegelrei Canal', num: 2, cat: 'attraction', desc: 'One of Bruges\' most beautiful and quiet canal streets' },
        { lat: 51.2093, lng: 3.2247, label: 'Markt Square', num: 3, cat: 'attraction', desc: 'Central square — starting point for final morning walk' },
        { lat: 51.2090, lng: 3.2250, label: 'That\'s Toast', num: 4, cat: 'food', desc: 'Creative brunch spot near the Markt' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '€30–60/night (hostel)', midrange: '€90–150/night', luxury: '€200–400/night' },
    { category: 'Meals (solo)', budget: '€25–40/day', midrange: '€50–80/day', luxury: '€100–200/day' },
    { category: 'Transport', budget: '€0–10/day (walking)', midrange: '€10–20/day', luxury: '€30–60/day (private)' },
    { category: 'Activities', budget: '€0–15/day', midrange: '€15–35/day', luxury: '€40–80/day' },
    { category: 'Beer & Chocolate', budget: '€10–15/day', midrange: '€20–35/day', luxury: '€40–60/day' },
    { category: '5-Day Total (solo)', budget: '€400–700', midrange: '€800–1,500', luxury: '€2,000–3,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Brussels Airport (BRU) — direct train to Bruges in ~60 mins (€18)', 'Brussels South Charleroi (CRL) — budget airlines, shuttle + train ~90 mins', 'Bruges station is a 15-min walk or short bus to the historic centre', 'Consider a Eurail pass if combining with other Belgian/Dutch cities'] },
    { title: '🏨 Where to Stay', items: ['Hotel Heritage — boutique luxury in a UNESCO building on the Markt', 'Hotel Jan Brito — charming 16th-century mansion near the canals', 'Sint-Anna area — quieter, more local, walking distance to everything', 'St Christopher\'s Inn — social hostel near the station for solo travelers'] },
    { title: '🌡️ Weather', items: ['Late June averages 18–23°C (64–73°F)', 'Daylight until ~10pm — glorious long evenings', 'Rain is always possible — pack a compact rain jacket', 'UV is moderate — sunscreen for outdoor café days'] },
    { title: '💳 Money', items: ['Euro (€) — card/contactless accepted almost everywhere', 'Some small beer bars and market stalls are cash-only — keep €50 handy', 'Tipping: round up or 5–10% at restaurants, not obligatory', 'Belgium is moderately priced — cheaper than Paris, pricier than Prague'] },
    { title: '📱 Connectivity', items: ['EU roaming included for European SIM holders', 'Buy an eSIM (Airalo, Holafly) for non-EU travelers', 'Free WiFi in most hotels, cafés, and the central library', 'Download offline maps — the winding streets will get you happily lost'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
