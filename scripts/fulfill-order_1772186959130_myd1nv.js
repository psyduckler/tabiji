const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772186959130_myd1nv',
  email: 'vibanez@ticketgotourism.com',
  destination: 'Barcelona, España',
  startDate: '2026-03-16',
  endDate: '2026-03-20',
  groupSize: '2',
  travelStyle: 'Cultural',
  dining: 'Fine dining all meals',
  budget: 'Under $1,000',
  requests: 'We don\'t want crowded places'
};

const itineraryData = {
  destination: 'Barcelona, España',
  countryEmoji: '🇪🇸',
  title: 'Barcelona: Cultural Depths & Hidden Elegance',
  subtitle: '4 nights of art, architecture & fine dining away from the crowds',
  description: 'This is Barcelona for those who know that the city\'s most extraordinary moments happen in doorways tourists walk past, in wine bars with no signage, and in narrow Gothic lanes that dead-end into a perfect medieval square. For 4 nights you\'ll move through El Born, Gràcia, Poble Sec, and the quieter corners of the Eixample — discovering Modernista masterpieces beyond the postcard, eating at some of the most inventive tables in Europe, and experiencing a city that rewards curiosity over itinerary. March is ideal: warm enough to sit outside, light enough in the evenings, and blissfully free of summer crowds.',
  duration: '4 nights / 5 days',
  dates: 'Mar 16 – Mar 20, 2026',
  budget: '$$$',
  pace: 'Leisurely',
  bestFor: 'Culturally-minded couples',
  highlights: [
    'Recinte Modernista de Sant Pau — Domènech\'s masterpiece, quieter than the Sagrada Família',
    'Basílica de Santa Maria del Mar — Gothic perfection built by the people of the Ribera',
    'Palau de la Música Catalana — Modernista explosion of stained glass and sculpture',
    'El Born\'s labyrinthine medieval lanes and independent galleries',
    'Bunkers del Carmel at dusk — the best city panorama with almost no one around',
    'Gràcia\'s village squares and neighbourhood Modernista gems',
    'Poble Sec and Paral·lel — Barcelona\'s most authentic hillside neighbourhood'
  ],

  essentials: [
    { title: '🌤️ March in Barcelona', text: 'March is shoulder season — temperatures of 14-18°C, roughly 6 hours of sunshine per day, and the city largely to yourselves. Some outdoor terraces are already open. Bring a light jacket for evenings, especially near the waterfront.' },
    { title: '🚇 Getting Around', text: 'A T-Casual card (10 trips, ~€12.15) covers all metro, bus, and FGC trains. Barcelona is very walkable between El Born, Gothic Quarter, and Eixample. For Gràcia and Poble Sec, the metro is faster. Avoid taxis for short distances — walk instead.' },
    { title: '🍽️ Fine Dining Reservations', text: 'Barcelona\'s best restaurants book out weeks in advance. Reserve all dinners before you land — use each restaurant\'s website or Resy. Disfrutar and Alkimia especially require advance planning. Lunch menus (menú del día) at fine dining spots offer extraordinary value: €30-50 for multi-course meals that cost €100+ at dinner.' },
    { title: '🏛️ Museum Tips', text: 'The Palau de la Música requires a guided tour — book online. Recinte Modernista de Sant Pau is best visited at opening time (10am) before tour groups arrive. Museu Picasso offers free entry on Thursday evenings (6-9:30pm). A BCN Card (€50) covers many museums if you plan to visit several.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-16',
      neighborhoods: 'El Born · Gothic Quarter side streets · Sant Pere',
      title: 'Arrival in El Born — Medieval Lanes & Modernista Splendour',
      description: 'Touch down and ease into Barcelona\'s oldest neighbourhoods. El Born and the side streets of the Gothic Quarter reward slow walking — every arch, courtyard, and tiled façade has a story. Tonight, dinner at one of Spain\'s most celebrated creative tables.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'El Born Arrival Walk',
              description: 'Check into your hotel — ideally in El Born or the Eixample for the best access. Head straight into the Barri de la Ribera: the narrow lanes radiating from Santa Maria del Mar are among the most atmospheric in Europe. Look up — the Gothic arches, iron balconies, and carved stone details are extraordinary.',
              details: [
                '🏨 Stay in El Born (Hotel Mercer, Yurbban Trafalgar) or Eixample for the best base',
                '🚶 Carrer del Rec, Carrer dels Mirallers, Carrer de la Cirera — wander freely',
                '⚠️ Avoid La Barceloneta waterfront strip — tourist traps and poor food'
              ]
            },
            {
              title: 'Basílica de Santa Maria del Mar',
              description: 'One of the great Gothic churches of Europe — and Barcelona\'s most soulful. Built between 1329 and 1383 by the merchants and porters of the Ribera neighbourhood, its soaring interior has a purity that the Catedral lacks. Visit late afternoon when light filters through the rose window.',
              details: [
                '⛪ Entry: €10 (includes rooftop access) — book online to skip any queue',
                '📸 The three-nave interior is strikingly elegant — less ornate, more powerful',
                '🕯️ Locals still light candles here — it remains a living place of worship',
                '🏛️ The Fossar de les Moreres memorial square outside is historically significant'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'El Born\'s best streets have almost no signage directing tourists. Put the phone away and just walk — you\'ll find better things than any map shows.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Palau de la Música Catalana — Evening Concert',
              description: 'Book tickets for an evening concert at Domènech i Montaner\'s extraordinary 1908 concert hall — a Modernista explosion of stained glass, sculpted columns, and flowing mosaics. Even a chamber music evening here is a full sensory experience.',
              details: [
                '🎼 Check schedule at palaumusica.cat — chamber concerts from €18-35',
                '🎟️ Book online; popular concerts sell out weeks ahead',
                '📸 The interior can only be seen on a guided tour (€22) or at a concert — the concert is far more magical',
                '🕐 Tours run 9am-6pm daily; evening concerts usually start at 7:30-8pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'El Xampanyet',
              description: 'A legendary El Born cava bar that has been pouring house cava and piling plates of house-made anchovies, jamón, and Catalan tapas since 1929. It\'s tiny, always buzzing, and one of the most authentic spots in the city — arrive early (7pm) or expect a short wait.',
              meta: '💰 $$ · 📍 Carrer de la Montcada 22, El Born · Closed Mon'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3842, lng: 2.1808, label: 'Basílica de Santa Maria del Mar', num: 1, cat: 'attraction', desc: 'Gothic masterpiece built by the people of the Ribera — sublime interior' },
        { lat: 41.3873, lng: 2.1753, label: 'Palau de la Música Catalana', num: 2, cat: 'attraction', desc: 'Modernista concert hall — attend an evening concert' },
        { lat: 41.3843, lng: 2.1813, label: 'El Xampanyet', num: 3, cat: 'food', desc: 'Legendary cava bar on Carrer de la Montcada — anchovies and house cava since 1929' },
        { lat: 41.3851, lng: 2.1800, label: 'El Born neighbourhood', num: 4, cat: 'attraction', desc: 'Medieval lane network — best walked without a map' }
      ]
    },
    {
      num: 2,
      date: '2026-03-17',
      neighborhoods: 'Eixample · Recinte Modernista · Gràcia',
      title: 'Modernisme Beyond the Postcard — Sant Pau & Gràcia',
      description: 'Escape the Sagrada Família queues and discover Domènech i Montaner\'s Recinte Modernista de Sant Pau — a hospital so beautiful it became a UNESCO World Heritage Site. Then lose an afternoon in Gràcia, Barcelona\'s proudest neighbourhood.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Recinte Modernista de Sant Pau',
              description: 'Built between 1901 and 1930 as a working hospital, the Recinte Modernista is arguably the most spectacular Modernista complex in Barcelona — and far less crowded than the Sagrada Família directly opposite. Twelve pavilions of Catalan stonework, glazed tile domes, and sculptural gardens.',
              details: [
                '🎟️ Entry: €19 — book online at recintemodernistadesantpau.com',
                '⏰ Open from 10am — arrive at opening to have the gardens to yourself',
                '🏛️ Built simultaneously with the Sagrada Família on the same axis — architect rivalry made manifest',
                '📸 The view from inside the grounds toward the Sagrada Família towers is remarkable'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Federal Café',
              description: 'Beloved Eixample breakfast spot with excellent flat whites, avocado toast, and seasonal pastries. Light-filled and calm — a great start before a museum morning.',
              meta: '💰 $ · 📍 Carrer del Parlament 39 (Eixample Esquerra) · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gràcia Neighbourhood & Plaça del Sol',
              description: 'Walk north into Gràcia — technically a separate village until 1897, and it still feels like one. The neighbourhood\'s five main squares (Plaça del Sol, Plaça de la Vila de Gràcia, Plaça de la Virreina) are where locals actually live: café terraces, neighbourhood dogs, and zero tourist infrastructure.',
              details: [
                '🏡 Gràcia has its own Modernista gems: Casa Vicens (Gaudí\'s first major work, €16)',
                '🛍️ Carrer de Verdi and Carrer de Torrijos have independent bookshops, ceramics studios',
                '☕ The squares have good local café terraces — ideal for a coffee break',
                '🎭 Check for gallery openings in the side streets off Carrer Gran de Gràcia'
              ]
            },
            {
              title: 'Casa Vicens — Gaudí\'s First Major Work',
              description: 'Far fewer visitors than Casa Batlló or Casa Milà, but arguably more interesting — this is where Gaudí\'s imagination first found full expression in 1883. The Moorish and Oriental influences, the ceramic tiles, the iron palm fronds — it\'s unlike anything else he built.',
              details: [
                '🏠 Entry: €16 — book at casavicens.org; rarely sells out',
                '📍 Carrer de les Carolines 20, Gràcia — a 5-minute walk from Fontana metro',
                '🎨 The interior restoration is beautifully done with excellent contextual information',
                '⏰ Allow 60-90 minutes to explore properly'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Bunkers del Carmel at Dusk',
              description: 'The old Republican anti-aircraft bunkers above the Carmel neighbourhood offer the finest 360° panorama of Barcelona — and almost no one knows about them compared to the Tibidabo crowds. Bring a bottle of cava and watch the city light up as the sun sets over the Mediterranean.',
              details: [
                '📍 Turó de la Rovira — take bus V17 from Passeig de Gràcia or walk up from Carmel',
                '🌅 Arrive 45 minutes before sunset — the light on the Eixample grid is extraordinary',
                '🍾 Pick up cava at Vinissimus or any Gràcia bodega before going up',
                '⚠️ No facilities at the top — bring everything you need'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bodega 1900',
              description: 'Albert Adrià\'s (brother of Ferran Adrià of elBulli) love letter to the old Barcelona vermouth bar — reinvented with brilliant technique. The format is traditional vermouth and small plates, but the execution is world-class. Unmissable and far less famous than Tickets next door.',
              meta: '💰 $$$ · 📍 Carrer de Tamarit 91, Eixample · Book at bodega1900.com · Closed Sun/Mon'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.4145, lng: 2.1735, label: 'Recinte Modernista de Sant Pau', num: 1, cat: 'attraction', desc: 'UNESCO Modernista hospital complex — far less crowded than Sagrada Família' },
        { lat: 41.4030, lng: 2.1537, label: 'Casa Vicens', num: 2, cat: 'attraction', desc: 'Gaudí\'s 1883 debut masterpiece in Gràcia — Moorish and Oriental style' },
        { lat: 41.4185, lng: 2.1536, label: 'Bunkers del Carmel', num: 3, cat: 'attraction', desc: 'Old Republican bunkers — finest 360° panorama of Barcelona at dusk' },
        { lat: 41.3791, lng: 2.1618, label: 'Bodega 1900', num: 4, cat: 'food', desc: 'Albert Adrià\'s reinvented vermouth bar — creative small plates, excellent wine' },
        { lat: 41.4032, lng: 2.1594, label: 'Plaça del Sol, Gràcia', num: 5, cat: 'attraction', desc: 'Gràcia\'s beating heart — terrace cafés and zero tourist infrastructure' }
      ]
    },
    {
      num: 3,
      date: '2026-03-18',
      neighborhoods: 'Gothic Quarter (off-route) · El Born · Sant Pere',
      title: 'Gothic Depths — Hidden Courtyards & Living History',
      description: 'A full day in Barcelona\'s oldest quarter — but off the tourist circuit. The Roman ruins, medieval courtyards, and Renaissance palaces that most visitors walk past are yours today. An afternoon gallery trail through El Born\'s independent art spaces, then one of the city\'s finest creative dinners.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Temple d\'August & Roman Barcelona',
              description: 'In the courtyard of the medieval Centre Excursionista de Catalunya, four enormous Roman columns from the Temple of Augustus (1st century BC) stand perfectly preserved inside a Gothic building. Free to enter, almost always empty. This is time travel at its best.',
              details: [
                '📍 Carrer del Paradís 10 — look for a small sign on the Gothic Quarter lane',
                '🏛️ Free entry; the hidden courtyard is typically calm even in peak season',
                '🗺️ From here, explore: Plaça de Sant Felip Neri (bullet holes from the Civil War), Carrer de Sant Sever',
                '⛪ The Catedral del Bisbat is nearby — the Gothic cloister with geese is free'
              ]
            },
            {
              title: 'El Call — Barcelona\'s Medieval Jewish Quarter',
              description: 'One of the best-preserved medieval Jewish quarters in Europe, and almost entirely overlooked by tourists. The narrow lanes of El Call (from the Hebrew "kahal") contain a tiny museum, a 13th-century synagogue, and layers of layered urban history invisible from the main streets.',
              details: [
                '🕍 Antiga Sinagoga Major — one of Europe\'s oldest synagogues (€2.50 entry)',
                '📍 Carrer de Marlet, Carrer de Sant Domènec del Call — impossibly narrow',
                '🏛️ The Institut de Cultura hosts temporary exhibitions in the area — check what\'s on',
                '🔍 Look for the Hebrew inscription stones embedded in walls throughout'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bar del Pla',
              description: 'A true neighbourhood bar in El Born — proper café amb llet, freshly squeezed orange juice, and pa amb tomàquet (bread rubbed with tomato). Locals at the bar, marble counter, tiled floor. Exactly right.',
              meta: '💰 $ · 📍 Carrer de la Montcada 2, El Born · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Museu Picasso — Formative Years',
              description: 'The Museu Picasso holds the most important collection of Picasso\'s early work anywhere — his Barcelona years (1895-1904) when he painted his first masterpieces in studios just steps from the museum. Housed in five interconnected medieval palaces on Carrer de Montcada.',
              details: [
                '🎟️ Entry: €12 — book online. Free Thursday evenings 6-9:30pm (arrive early)',
                '⏰ Allow 1.5-2 hours; the Blue Period rooms are extraordinary',
                '🏛️ The Gothic palaces themselves — 15th-century merchant homes — are as interesting as the art',
                '📍 Carrer de Montcada 15-23 — the street itself is a medieval masterpiece'
              ]
            },
            {
              title: 'El Born Independent Gallery Trail',
              description: 'El Born has Barcelona\'s highest concentration of independent galleries and artist studios. An afternoon of gallery-hopping reveals what\'s actually happening in contemporary Catalan art — and most galleries are free. Galeria Senda, Galeria Toni Tapies, and Espai Mescladís are worth a look.',
              details: [
                '🎨 Most galleries open Tue-Sat 11am-2pm and 4-8pm — free entry',
                '🗺️ The area around Carrer del Rec and Carrer del Comerç is densest',
                '☕ Stop at El Xampanyet or Bar Marsella for a break between galleries',
                '📖 Pick up a free cultural map at any gallery reception'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Vermouth Hour at Bar Marsella',
              description: 'Barcelona\'s oldest bar (1820) hidden on a small lane near the Rambla. The bottles on the shelves have been there for decades; the dust is genuine; the absinthe is poured by hand. A mandatory stop for anyone serious about Barcelona\'s cultural history.',
              details: [
                '📍 Carrer de Sant Pau 65, Raval — a 5-minute walk from El Born',
                '🍸 Order the house vermouth or an absinthe — the cocktail menu is limited by design',
                '⏰ Opens around 6pm — arrive early as it\'s tiny and fills up quickly',
                '📸 The interior hasn\'t changed in 200 years — photograph respectfully'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Alkimia',
              description: 'Chef Jordi Vilà\'s intimate restaurant in the Eixample — one of the most intelligent interpretations of modern Catalan cuisine in the city. The Clàssics menu (traditional Catalan dishes, playfully reinvented) is exceptional. Quiet, beautifully lit, and a world away from the tourist strip.',
              meta: '💰 $$$$ · 📍 Ronda de Sant Antoni 41, Eixample · Book at alkimia.cat · Tasting menu from €90'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3838, lng: 2.1762, label: 'Temple d\'August (Roman Columns)', num: 1, cat: 'attraction', desc: '1st-century Roman temple columns hidden in a Gothic courtyard — free entry' },
        { lat: 41.3835, lng: 2.1753, label: 'El Call (Jewish Quarter)', num: 2, cat: 'attraction', desc: 'Medieval Jewish quarter with 13th-century synagogue — largely unvisited' },
        { lat: 41.3851, lng: 2.1805, label: 'Museu Picasso', num: 3, cat: 'attraction', desc: 'Picasso\'s early masterpieces in five interconnected Gothic palaces' },
        { lat: 41.3793, lng: 2.1682, label: 'Bar Marsella', num: 4, cat: 'food', desc: 'Barcelona\'s oldest bar (1820) — absinthe and vermouth in a time capsule interior' },
        { lat: 41.3818, lng: 2.1631, label: 'Alkimia', num: 5, cat: 'food', desc: 'Modern Catalan cuisine by Jordi Vilà — one of Barcelona\'s finest quiet tables' }
      ]
    },
    {
      num: 4,
      date: '2026-03-19',
      neighborhoods: 'Poble Sec · Montjuïc · Paral·lel',
      title: 'Poble Sec & Montjuïc — Barcelona\'s Authentic Hillside',
      description: 'Cross to the south side of the city and discover Poble Sec — Barcelona\'s most authentically neighbourhood neighbourhood, tucked between Montjuïc hill and the Paral·lel avenue. Then ascend Montjuïc for Romanesque art, Mediterranean gardens, and panoramic views that rival anywhere in Europe.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Museu Nacional d\'Art de Catalunya (MNAC)',
              description: 'The MNAC\'s Romanesque collection is among the finest in the world — 1,000-year-old frescoes rescued from Pyrenean churches and installed in purpose-built apses that recreate their original setting with eerie precision. The Gothic collection and the Modernisme galleries round out an extraordinary morning.',
              details: [
                '🎟️ Entry: €12, free first Sunday of the month and every Saturday after 3pm',
                '🏛️ The Romanesque rooms are the reason to come — plan 90 minutes minimum',
                '📍 Accessible by metro to Espanya, then walk up Avinguda de la Reina Maria Cristina',
                '☕ The terrace café has spectacular city views — stop here for coffee after the Romanesque rooms'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bar Calders',
              description: 'Poble Sec\'s beloved neighbourhood café — outdoor terrace on Carrer del Parlament, excellent coffee, and simple Catalan breakfast dishes. Often full of locals on their way to work.',
              meta: '💰 $ · 📍 Carrer del Parlament 25, Poble Sec · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fundació Joan Miró',
              description: 'Sert\'s 1975 building — all white walls, natural light, and Mediterranean air — is perfectly calibrated for Miró\'s exuberant primary colours and biomorphic forms. The foundation holds the most comprehensive Miró collection in the world, with almost no crowds in March.',
              details: [
                '🎟️ Entry: €14 — book at fmirobcn.org',
                '⏰ Allow 2 hours; the sculpture terraces are beautiful in afternoon light',
                '🎨 The Espai 13 gallery shows cutting-edge contemporary artists — always surprising',
                '🌿 The walk from MNAC to Fundació Miró through Montjuïc gardens is lovely (15 mins)'
              ]
            },
            {
              title: 'Jardins de Laribal & Montjuïc Viewpoints',
              description: 'The terraced gardens of Montjuïc are one of Barcelona\'s best-kept secrets — fountains, pergolas, and Mediterranean plantings designed in the 1920s, largely unknown to tourists. In March the mimosa and early spring blossom are extraordinary.',
              details: [
                '🌿 Jardins de Laribal — free entry, usually completely empty',
                '🌸 March brings early spring: almond blossom, mimosa, cyclamen',
                '📸 The views from the castle ramparts down to the port and Barceloneta',
                '🏰 Castell de Montjuïc (€5) has the best 360° panorama on this side of the city'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Poble Sec Aperitivo Hour',
              description: 'Descend from Montjuïc into Poble Sec for the neighbourhood aperitivo ritual. The stretch of Carrer de Blai is famous for pintxos bars — smaller and more local than anything in El Born — while Carrer del Parlament and Carrer de Tamarit have excellent wine bars.',
              details: [
                '🍷 Quimet i Quimet (Carrer del Poeta Cabanyes 25) — legendary standing bar, incredible montaditos and conservas',
                '🍸 Bar Olimpia (Carrer de Lleida) — natural wines by the glass, local crowd',
                '⏰ Quimet i Quimet opens at noon, closes at 4pm and reopens at 7pm — plan around it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tickets',
              description: 'Albert Adrià\'s theatrical tapas bar — the most playful and technically brilliant small-plates experience in Barcelona. Dishes are inspired by circus and carnival; the execution is as precise as any Michelin table. Book the first available sitting (7:15pm) for the quietest experience.',
              meta: '💰 $$$$ · 📍 Avinguda del Paral·lel 164, Poble Sec · Book at elbarriadria.com · Opens Tue-Sat'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3683, lng: 2.1534, label: 'MNAC (Museu Nacional d\'Art de Catalunya)', num: 1, cat: 'attraction', desc: 'World\'s finest Romanesque art collection — 1,000-year-old Pyrenean frescoes' },
        { lat: 41.3681, lng: 2.1601, label: 'Fundació Joan Miró', num: 2, cat: 'attraction', desc: 'Comprehensive Miró collection in Sert\'s luminous 1975 building' },
        { lat: 41.3631, lng: 2.1580, label: 'Jardins de Laribal', num: 3, cat: 'attraction', desc: '1920s terraced gardens on Montjuïc — almost always empty, beautiful in March' },
        { lat: 41.3747, lng: 2.1581, label: 'Quimet i Quimet', num: 4, cat: 'food', desc: 'Legendary standing bar — tinned fish, montaditos, and vermouth since 1914' },
        { lat: 41.3769, lng: 2.1603, label: 'Tickets', num: 5, cat: 'food', desc: 'Albert Adrià\'s theatrical tapas bar — the most creative small-plates in Barcelona' }
      ]
    },
    {
      num: 5,
      date: '2026-03-20',
      neighborhoods: 'Eixample · Passeig de Gràcia · Departure',
      title: 'Final Morning — Modernisme on Foot & A Last Perfect Meal',
      description: 'A morning of Modernista architecture at walking pace along Barcelona\'s grandest boulevard, a long lunch worth lingering over, and a final taste of the city before departure. End as you began — on foot, curious, looking up.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Manzana de la Discordia — Three Modernista Masters',
              description: 'The "Block of Discord" on Passeig de Gràcia puts Domènech i Montaner\'s Casa Lleó Morera, Puig i Cadafalch\'s Casa Amatller, and Gaudí\'s Casa Batlló on the same city block — architectural rivalry made beautiful. Walk slowly and look at every façade detail before going inside.',
              details: [
                '🏠 Casa Batlló exterior is free to appreciate — interior entry (€35) is worth it if time allows',
                '🏠 Casa Amatller (€17) is less visited and equally extraordinary inside — book at casaamatller.org',
                '🍫 Amatller chocolates are sold at the Casa Amatller shop — an excellent Barcelona souvenir',
                '📸 Best time: 9-10am before the tour group coaches arrive'
              ]
            },
            {
              title: 'Fundació Antoni Tàpies',
              description: 'Tàpies is Barcelona\'s greatest postwar artist — and his foundation occupies a beautiful 1880 Modernista publishing house just off Passeig de Gràcia. The permanent collection of his large-format works (earth, clay, burnt canvas, torn paper) is haunting and powerful. Almost never crowded.',
              details: [
                '🎟️ Entry: €8 — fundaciotapies.org',
                '🏛️ The building itself (Domènech i Montaner, 1880) is as interesting as the collection',
                '🎨 Look up at the roof terrace from the street — Tàpies\' wire sculpture sits above the building',
                '⏰ Allow 1 hour — the permanent collection is compact but intense'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Forn de Sant Jaume',
              description: 'Classic Eixample pastisseria — buttery croissants, xuixos (Catalan fried custard pastries), and strong café amb llet. The kind of breakfast that makes you wish you\'d booked another night.',
              meta: '💰 $ · 📍 Rambla de Catalunya 50, Eixample · Opens 8am'
            },
            {
              type: '🍽️ Lunch (Farewell)',
              name: 'Disfrutar',
              description: 'Three-Michelin-star Disfrutar (by three former elBulli chefs) regularly appears in the World\'s 50 Best Restaurants list. The lunch tasting menu is the finest creative dining experience Barcelona offers — technique, wit, surprise, and extraordinary produce in a bright, modernist dining room. This is the meal to remember the trip by. Reserve months ahead.',
              meta: '💰 $$$$ · 📍 Carrer de Villarroel 163, Eixample · disfrutarbarcelona.com · Lunch tasting menu from €220/person'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Walk & Departure',
              description: 'After a long, memorable lunch, a slow walk back through the Eixample grid. Stop at Escribà pastisseria for a box of chocolate to take home. Then head to the airport or your onward connection — Barcelona recedes but it never quite leaves you.',
              details: [
                '🍫 Escribà (Gran Via de les Corts Catalanes 546) — extraordinary chocolates and pastries since 1906',
                '🚇 Metro L3 (Tarragona) or L5 (Hospital Clínic) to Aerobús stop at Plaça d\'Espanya',
                '✈️ Allow 90 minutes from city centre to airport for an international flight'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3915, lng: 2.1649, label: 'Casa Batlló', num: 1, cat: 'attraction', desc: 'Gaudí\'s masterwork on Passeig de Gràcia — the Block of Discord' },
        { lat: 41.3916, lng: 2.1653, label: 'Casa Amatller', num: 2, cat: 'attraction', desc: 'Puig i Cadafalch\'s Gothic-Flemish fantasy — less visited, equally beautiful' },
        { lat: 41.3925, lng: 2.1655, label: 'Fundació Antoni Tàpies', num: 3, cat: 'attraction', desc: 'Barcelona\'s greatest postwar artist in a beautiful Modernista building — rarely crowded' },
        { lat: 41.3867, lng: 2.1558, label: 'Disfrutar', num: 4, cat: 'food', desc: 'World\'s 50 Best restaurant — farewell tasting lunch by three ex-elBulli chefs' },
        { lat: 41.3785, lng: 2.1519, label: 'Escribà Gran Via', num: 5, cat: 'food', desc: 'Extraordinary chocolates and pastries since 1906 — perfect Barcelona souvenir' }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
