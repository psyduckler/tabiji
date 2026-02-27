const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772186413979_4xisql',
  email: 'taloool@msn.com',
  destination: 'Europe',
  startDate: '2026-07-14',
  endDate: '2026-07-30',
  groupSize: 5,
  requests: ''
};

const itineraryData = {
  destination: 'Europe',
  countryEmoji: '🇪🇺',
  title: 'A Grand European Summer for the Family',
  subtitle: '16 days through Barcelona, Provence, Florence, Rome & the Amalfi Coast',
  description: "This is the European summer trip your family will talk about for decades. Start in Barcelona with Gaudí's whimsical architecture and tapas crawls, drift through lavender-scented Provence and the sparkling French Riviera, then cross into Italy for Renaissance art in Florence, ancient wonders in Rome, and sun-drenched coastal magic on the Amalfi Coast. Every day blends culture, incredible food, and moments the whole family — from kids to grandparents — will treasure.",
  duration: '16 nights',
  dates: 'Jul 14 – Jul 30, 2026',
  budget: '$$–$$$$',
  pace: 'Moderate',
  bestFor: 'Families · Foodies · Culture Lovers',
  highlights: [
    'Gaudí\'s Sagrada Família in Barcelona',
    'Lavender fields of Provence',
    'Gelato and the Duomo in Florence',
    'The Colosseum and Roman Forum',
    'Boat day along the Amalfi Coast',
    'Family pasta-making class in Tuscany'
  ],

  essentials: [
    { title: '☀️ Summer in Southern Europe', text: 'July means 30-38°C across all stops. Pack light layers, sun hats, sunscreen, and comfortable walking shoes. Sightseeing is best early morning or late afternoon — embrace the siesta.' },
    { title: '🚄 Getting Between Cities', text: 'High-speed trains connect Barcelona → Provence (TGV), Nice → Italy. Book Trenitalia/Italo for Florence → Rome. Amalfi is best reached by car or SITA bus from Naples/Salerno.' },
    { title: '👨‍👩‍👧‍👦 Family Tips', text: 'Kids eat free or cheap at most Italian restaurants. Skip the line tickets are essential everywhere in July. Bring refillable water bottles — public fountains (nasoni) are everywhere in Rome.' },
    { title: '💳 Money & Language', text: 'Euro everywhere. Card widely accepted but carry some cash for markets and small towns. English is spoken in tourist areas; locals appreciate even basic \"bonjour\" or \"grazie.\"' }
  ],

  days: [
    {
      num: 1,
      date: '2026-07-14',
      neighborhoods: 'Gothic Quarter · Las Ramblas · El Born',
      title: 'Hola Barcelona! — Gothic Quarter & First Tapas',
      description: "Arrive in Barcelona and dive straight into the electric energy of the Gothic Quarter. Wander medieval lanes, stumble upon hidden plazas, and end the night with your first round of patatas bravas and jamón ibérico.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gothic Quarter Walking Tour',
              description: "Drop your bags and explore the Barri Gòtic — Barcelona's ancient heart. The labyrinthine streets are full of surprises: Roman ruins, tiny churches, street musicians, and the grand Barcelona Cathedral.",
              details: [
                '⛪ Barcelona Cathedral — free entry, stunning Gothic cloister with geese',
                '📸 Plaça del Rei — medieval royal palace square',
                '🎵 Street musicians on Carrer del Bisbe — the bridge is magical'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "It's Bastille Day in France but you're in Spain! Barcelona will be buzzing with summer energy. Settle in and save energy — you've got 16 incredible days ahead." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Las Ramblas & El Born Tapas Crawl',
              description: "Stroll down Las Ramblas to soak up the atmosphere, then duck into El Born for better tapas and fewer tourists. Hit 2-3 spots: one for jamón and croquetas, one for seafood, one for vermouth.",
              details: [
                '🦐 Cal Pep — legendary tapas bar (arrive early or queue)',
                '🍷 El Xampanyet — tiny cava bar with anchovies and atmosphere',
                '🧀 La Boqueria market closes at 8pm but peek in for tomorrow'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Cal Pep',
              description: 'Iconic tapas counter where the chef serves you directly. Fresh seafood, razor clams, crispy artichokes — a Barcelona institution.',
              meta: '💰 $$$ · 📍 Plaça de les Olles, 8 · No reservations at the bar'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3840, lng: 2.1761, label: 'Gothic Quarter', num: 1, cat: 'attraction', desc: 'Medieval heart of Barcelona with Roman ruins' },
        { lat: 41.3839, lng: 2.1764, label: 'Barcelona Cathedral', num: 2, cat: 'attraction', desc: 'Gothic cathedral with cloister of 13 geese' },
        { lat: 41.3809, lng: 2.1748, label: 'Las Ramblas', num: 3, cat: 'attraction', desc: 'Famous tree-lined pedestrian boulevard' },
        { lat: 41.3842, lng: 2.1861, label: 'El Born', num: 4, cat: 'attraction', desc: 'Trendy neighbourhood with great tapas bars' },
        { lat: 41.3834, lng: 2.1856, label: 'Cal Pep', num: 5, cat: 'food', desc: 'Legendary tapas counter — fresh seafood' }
      ]
    },
    {
      num: 2,
      date: '2026-07-15',
      neighborhoods: 'Eixample · Park Güell · Gràcia',
      title: 'Gaudí Day — Sagrada Família & Park Güell',
      description: "Today belongs to Antoni Gaudí — Barcelona's visionary architect. The Sagrada Família will leave adults speechless and kids wide-eyed, and Park Güell is a mosaic-covered playground with city views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sagrada Família',
              description: "Gaudí's unfinished masterpiece is unlike anything your family has ever seen. The interior is a forest of light — columns branch like trees, and stained glass paints everything in rainbows. Book the tower elevator for vertiginous city views.",
              details: [
                '🎫 Book timed-entry tickets months ahead — July sells out',
                '🗼 Tower access (Nativity facade) is best for families with older kids',
                '⏰ 9am entry is quietest — arrive 15 min early',
                '📸 The light inside is best in the morning (east-facing windows)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Park Güell',
              description: "Gaudí's mosaic wonderland overlooking the city. The colourful dragon fountain (El Drac), the serpentine bench with panoramic views, and the gingerbread gatehouses are pure magic for all ages. The free zone has great paths through Mediterranean gardens.",
              details: [
                '🎫 Timed entry for the Monumental Zone — book ahead',
                '🦎 The mosaic dragon is THE photo spot',
                '🌳 Free areas have lovely shaded walks'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'La Pepita',
              description: 'Casual Gràcia neighbourhood spot beloved by locals. Creative bocadillos (sandwiches), patatas bravas, and craft vermouth. Kid-friendly vibe.',
              meta: '💰 $$ · 📍 Carrer de Còrsega, 343, Gràcia'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gràcia Neighbourhood Wander',
              description: "The Gràcia neighbourhood around Park Güell is a village within the city — quiet plazas with playing children, family-run restaurants, and zero tourist tat. Plaça del Sol is perfect for an evening drink while kids run around.",
              details: [
                '🏘️ Plaça de la Vila de Gràcia — local families gather here at sunset',
                '🍦 Gelaaati di Marco — excellent gelato on Carrer de Verdi'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.4036, lng: 2.1744, label: 'Sagrada Família', num: 1, cat: 'attraction', desc: "Gaudí's breathtaking unfinished basilica" },
        { lat: 41.4145, lng: 2.1527, label: 'Park Güell', num: 2, cat: 'attraction', desc: 'Mosaic wonderland with city panorama views' },
        { lat: 41.4025, lng: 2.1571, label: 'Gràcia', num: 3, cat: 'attraction', desc: 'Charming village-like neighbourhood' },
        { lat: 41.4010, lng: 2.1563, label: 'La Pepita', num: 4, cat: 'food', desc: 'Creative bocadillos and vermouth in Gràcia' }
      ]
    },
    {
      num: 3,
      date: '2026-07-16',
      neighborhoods: 'Barceloneta · La Boqueria · Montjuïc',
      title: 'Beach, Market & Montjuïc Magic',
      description: "A perfect Barcelona day: morning at the legendary Boqueria market, beach time at Barceloneta, and sunset from Montjuïc hill with the Magic Fountain show — a highlight kids will never forget.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'La Boqueria Market',
              description: "Barcelona's most famous food market is a feast for the senses. Fresh tropical fruit cups, jamón ibérico carved to order, seafood paella, and the best fresh-squeezed juices. Let the kids pick their own breakfast from the stalls.",
              details: [
                '🍓 Fresh fruit cups — mango, papaya, coconut — from €2',
                '🦐 Pinotxo Bar — legendary counter inside the market',
                '⏰ Go before 10am to avoid the biggest crowds'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Barceloneta Beach',
              description: "Hit the beach! Barceloneta is Barcelona's liveliest stretch of sand — golden beach, warm Mediterranean water, and chiringuitos (beach bars) serving cold drinks and paella. Perfect for the whole family.",
              details: [
                '🏖️ The water is warm (24-25°C) in July',
                '🍹 W Hotel end is less crowded than the main strip',
                '⚽ Beach volleyball, paddleboarding, sandcastles — something for everyone'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'La Mar Salada',
              description: 'Excellent seafood restaurant near the beach. Fresh catch of the day, fideuà (Catalan noodle paella), and a great kids menu.',
              meta: '💰 $$$ · 📍 Passeig de Joan de Borbó, 58'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Montjuïc & Magic Fountain Show',
              description: "Take the cable car up Montjuïc hill for panoramic views, then catch the Magic Fountain show — a spectacular display of water, light, and music that runs on summer evenings. Kids absolutely love it.",
              details: [
                '🚡 Telefèric de Montjuïc cable car — fun ride with amazing views',
                '⛲ Magic Fountain shows run Thu-Sun in summer, starting at 9:30pm',
                '🏰 Montjuïc Castle has great views too (and a moat!)'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3816, lng: 2.1719, label: 'La Boqueria Market', num: 1, cat: 'food', desc: "Barcelona's legendary food market" },
        { lat: 41.3790, lng: 2.1892, label: 'Barceloneta Beach', num: 2, cat: 'attraction', desc: 'City beach with golden sand and warm water' },
        { lat: 41.3714, lng: 2.1519, label: 'Montjuïc', num: 3, cat: 'attraction', desc: 'Hill with castle, gardens, and panoramic views' },
        { lat: 41.3714, lng: 2.1528, label: 'Magic Fountain', num: 4, cat: 'attraction', desc: 'Spectacular water-light-music show' },
        { lat: 41.3795, lng: 2.1880, label: 'La Mar Salada', num: 5, cat: 'food', desc: 'Fresh seafood and fideuà near the beach' }
      ]
    },
    {
      num: 4,
      date: '2026-07-17',
      neighborhoods: 'Casa Batlló · Passeig de Gràcia · El Raval',
      title: 'Modernisme, Chocolate & Farewell to Barcelona',
      description: "Your last Barcelona morning: explore Gaudí's Casa Batlló, shop along elegant Passeig de Gràcia, and squeeze in a chocolate museum visit before catching the afternoon train to Provence.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Casa Batlló',
              description: "Gaudí's most playful building — the facade looks like dragon scales, the interior is an underwater dreamworld. The augmented reality guide is incredible for kids (and adults). The rooftop with its dragon-spine chimney pots is unforgettable.",
              details: [
                '🎫 Book \"Blue\" timed entry online — includes AR experience',
                '🐉 The rooftop is designed as a dragon\'s back',
                '⏰ First entry (9am) is least crowded'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train to Provence (Barcelona → Avignon TGV)',
              description: "Board the high-speed TGV from Barcelona Sants to Avignon — about 4.5 hours through gorgeous scenery. Watch Spain turn into France through the window. Book a family compartment if available.",
              details: [
                '🚄 Barcelona Sants → Avignon TGV · ~4.5 hours',
                '🎫 Book on SNCF or Renfe — family fares available',
                '🥖 Grab bocadillos and drinks at the station for the ride'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Cervecería Catalana',
              description: 'Perfect farewell lunch — one of Barcelona\'s best tapas bars. Montaditos (small toasts), grilled prawns, and sangría. Always buzzing, always delicious.',
              meta: '💰 $$$ · 📍 Carrer de Mallorca, 236 · Arrive by 1pm or queue'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pack some Boqueria snacks for the train. Settle into your seats, put on a movie for the kids, and watch the landscape shift from Catalan coast to French countryside.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Arrive in Avignon — Settle In',
              description: "Arrive in Avignon and check into your accommodation. If there's energy left, walk to the Place de l'Horloge for a glass of rosé and people-watching. The Palais des Papes is magnificent even just lit up at night.",
              details: [
                '🏰 The Palais des Papes is stunning when illuminated after dark',
                '🍷 Place de l\'Horloge — main square with cafés and carousel for kids'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3916, lng: 2.1650, label: 'Casa Batlló', num: 1, cat: 'attraction', desc: "Gaudí's dragon-scale masterpiece" },
        { lat: 41.3927, lng: 2.1649, label: 'Passeig de Gràcia', num: 2, cat: 'attraction', desc: 'Elegant boulevard with Modernista architecture' },
        { lat: 41.3793, lng: 2.1402, label: 'Barcelona Sants Station', num: 3, cat: 'transport', desc: 'TGV departure to Avignon' },
        { lat: 41.3930, lng: 2.1648, label: 'Cervecería Catalana', num: 4, cat: 'food', desc: 'Top-tier tapas — farewell Barcelona lunch' },
        { lat: 43.9493, lng: 4.8055, label: 'Avignon', num: 5, cat: 'attraction', desc: 'Medieval walled city in Provence' }
      ]
    },
    {
      num: 5,
      date: '2026-07-18',
      neighborhoods: 'Avignon · Palais des Papes · Pont d\'Avignon',
      title: 'Papal Palace, Lavender & Provençal Markets',
      description: "Explore Avignon's magnificent Papal Palace — the largest Gothic palace in the world — then drive through the lavender fields of the Luberon. July is peak lavender season and the purple fields are breathtaking.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Palais des Papes',
              description: "The largest Gothic palace ever built — where popes ruled Christendom from 1309-1377. The immense halls, chapels, and frescoed chambers are awe-inspiring. The tablet guide brings it alive for kids with interactive elements.",
              details: [
                '🏰 Book online for timed entry — the tablet guide is excellent',
                '📸 The Grand Chapel is enormous — built to impress ambassadors',
                '⏰ Open 9am — go first thing to beat the heat'
              ]
            },
            {
              title: 'Pont d\'Avignon (Pont Saint-Bénézet)',
              description: "The famous half-bridge from the children's song \"Sur le Pont d'Avignon.\" Walk out over the Rhône — the views upstream and the story of why it's only half a bridge captivate kids.",
              details: [
                '🎵 Every French child knows the song — teach it to your kids!',
                '🌊 Only 4 of the original 22 arches remain'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lavender Fields & Luberon Villages',
              description: "July is peak lavender season in Provence. Drive through the Luberon to see rolling purple fields stretching to the horizon. Stop at Sénanque Abbey (iconic lavender + stone abbey photo) and the perched village of Gordes — one of the most beautiful villages in France.",
              details: [
                '💜 Sénanque Abbey — the most photographed lavender field in the world',
                '🏘️ Gordes — hilltop village with honey-stone houses and valley views',
                '🚗 Rent a car or book a half-day tour from Avignon',
                '🍦 Lavender ice cream in Gordes — the kids will love it'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Le Jardin du Quai, L\'Isle-sur-la-Sorgue',
              description: "Charming restaurant in the antiques capital of Provence. Dine in a garden courtyard beside the River Sorgue. Fresh Provençal cuisine — ratatouille, grilled lamb, tarts.",
              meta: '💰 $$$ · 📍 L\'Isle-sur-la-Sorgue · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'La Mirande',
              description: "Elegant dining in a 14th-century cardinal's palace right beside the Palais des Papes. The garden terrace on summer evenings is pure Provence. Excellent tasting menu.",
              meta: '💰 $$$$ · 📍 4 Place de la Mirande, Avignon'
            }
          ],
          tips: [
            { type: 'tip', text: "If you're visiting in mid-July, check if the Festival d'Avignon (theatre festival) is on — the whole city becomes a stage with street performers everywhere." }
          ]
        }
      ],
      mapPins: [
        { lat: 43.9508, lng: 4.8075, label: 'Palais des Papes', num: 1, cat: 'attraction', desc: 'Largest Gothic palace in the world' },
        { lat: 43.9536, lng: 4.8037, label: "Pont d'Avignon", num: 2, cat: 'attraction', desc: 'Famous half-bridge over the Rhône' },
        { lat: 43.9276, lng: 5.1866, label: 'Sénanque Abbey', num: 3, cat: 'attraction', desc: 'Iconic abbey surrounded by lavender fields' },
        { lat: 43.9119, lng: 5.2003, label: 'Gordes', num: 4, cat: 'attraction', desc: 'One of the most beautiful villages in France' },
        { lat: 43.9199, lng: 5.0523, label: "L'Isle-sur-la-Sorgue", num: 5, cat: 'food', desc: 'Antiques village with riverside dining' },
        { lat: 43.9504, lng: 4.8063, label: 'La Mirande', num: 6, cat: 'food', desc: "Fine dining in a cardinal's palace garden" }
      ]
    },
    {
      num: 6,
      date: '2026-07-19',
      neighborhoods: 'Provence · Roussillon · Apt · Nice',
      title: 'Ochre Cliffs, Provençal Markets & On to Nice',
      description: "Explore the rust-red ochre cliffs of Roussillon, browse a Provençal market day, then drive to the glamorous French Riviera. Arrive in Nice for your first evening on the Côte d'Azur.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Roussillon Ochre Trail',
              description: "Walk through the Sentier des Ocres — a surreal landscape of red, orange, and yellow cliffs carved by centuries of ochre mining. It feels like walking on Mars. Kids love the colours and the adventure of the trail.",
              details: [
                '🟠 Wear shoes you don\'t mind getting stained — the ochre is everywhere',
                '🥾 Two trails: short (30 min) and long (50 min) — both family-friendly',
                '📸 The colours are most vivid in morning light'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Drive to Nice via the Route Napoléon',
              description: "Hit the road toward the Côte d'Azur. The drive through the Provençal hills is gorgeous — olive groves, vineyards, and the scent of wild herbs. Stop in a village for a crêpe. Arrive in Nice by late afternoon.",
              details: [
                '🚗 ~3.5 hours from Roussillon to Nice',
                '🛣️ The Route Napoléon (N85) is scenic but winding — take the autoroute if kids get carsick',
                '☕ Stop in Grasse (perfume capital) if you have time'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Le Piquebaure, Roussillon',
              description: 'Simple, charming restaurant on the main square of Roussillon. Classic Provençal fare with views over the ochre village rooftops.',
              meta: '💰 $$ · 📍 Place de la Mairie, Roussillon'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'First Evening on the Promenade des Anglais',
              description: "Arrive in Nice and take your first walk along the legendary Promenade des Anglais. The Baie des Anges glows turquoise in the evening light. Grab socca (chickpea pancake) from a street vendor in Old Nice.",
              details: [
                '🏖️ The pebbly beach is beautiful at sunset',
                '🥞 Chez Pipo or Chez René Socca — essential Nice street food',
                '🌅 Walk from the Promenade up to Castle Hill for a 360° sunset view'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.9019, lng: 5.2928, label: 'Roussillon', num: 1, cat: 'attraction', desc: 'Village perched on red ochre cliffs' },
        { lat: 43.9019, lng: 5.2928, label: 'Sentier des Ocres', num: 2, cat: 'attraction', desc: 'Surreal ochre cliff walking trail' },
        { lat: 43.6590, lng: 6.9063, label: 'Grasse', num: 3, cat: 'attraction', desc: 'World perfume capital — optional stop' },
        { lat: 43.6947, lng: 7.2651, label: 'Promenade des Anglais', num: 4, cat: 'attraction', desc: "Nice's iconic seafront promenade" },
        { lat: 43.6961, lng: 7.2760, label: 'Old Nice (Vieux Nice)', num: 5, cat: 'attraction', desc: 'Colourful old town with narrow lanes and markets' }
      ]
    },
    {
      num: 7,
      date: '2026-07-20',
      neighborhoods: 'Nice · Old Town · Cours Saleya · Castle Hill',
      title: 'Nice — Flower Market, Old Town & Azure Waters',
      description: "A full day in Nice: browse the famous Cours Saleya market, explore the colourful old town, swim in the impossibly blue Mediterranean, and hike up Castle Hill for panoramic views of the entire Riviera.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cours Saleya Market',
              description: "Nice's famous outdoor market is a sensory explosion — flowers, fresh produce, olives, lavender sachets, socca, and local cheese. It's the best market in the South of France and perfect for families. Let the kids pick out pastries.",
              details: [
                '🌺 Flower market runs Tue-Sun mornings',
                '🧀 Try Banon — goat cheese wrapped in chestnut leaves',
                '🫒 Olive tapenade samples everywhere',
                '⏰ Get there by 8:30am for the best experience'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Beach Time & Castle Hill',
              description: "Spend the afternoon at one of Nice's beach clubs (or the free public beaches) before climbing Castle Hill — the view from the top is iconic: the sweep of the Baie des Anges, terracotta rooftops, and the deep blue sea.",
              details: [
                '🏖️ Blue Beach or Castel Plage for loungers/umbrellas',
                '🏔️ Castle Hill — take the elevator or stairs (free)',
                '⛲ A waterfall cascades down the hill — very picturesque',
                '👟 The walk up is about 15 minutes — manageable for kids'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Chez Pipo',
              description: "Nice's most famous socca (chickpea pancake) spot since 1923. Crispy, golden, served piping hot on paper. Simple, cheap, unforgettable. Cash only.",
              meta: '💰 $ · 📍 13 Rue Bavastro · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dinner in Vieux Nice',
              description: "The narrow streets of Old Nice come alive at night — tiny restaurants with tables spilling onto cobblestones, gelato shops, and the hum of conversation. Pick a spot on a quiet square and settle in for a long Niçoise dinner.",
              details: [
                '🍝 Salade Niçoise — eat it where it was invented',
                '🍦 Fenocchio — 100+ gelato flavours including lavender, olive, and tomato-basil'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Le Safari',
              description: 'Classic Niçoise restaurant on Cours Saleya. Pissaladière, stuffed vegetables, fresh pasta — all the regional specialties done right. Outdoor terrace.',
              meta: '💰 $$$ · 📍 1 Cours Saleya'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.6955, lng: 7.2755, label: 'Cours Saleya Market', num: 1, cat: 'food', desc: "Nice's famous flower and food market" },
        { lat: 43.6949, lng: 7.2811, label: 'Castle Hill', num: 2, cat: 'attraction', desc: 'Panoramic views of the Baie des Anges' },
        { lat: 43.6961, lng: 7.2760, label: 'Vieux Nice', num: 3, cat: 'attraction', desc: 'Colourful old town streets' },
        { lat: 43.6933, lng: 7.2621, label: 'Chez Pipo', num: 4, cat: 'food', desc: 'Famous socca since 1923' },
        { lat: 43.6952, lng: 7.2758, label: 'Le Safari', num: 5, cat: 'food', desc: 'Classic Niçoise cuisine on Cours Saleya' }
      ]
    },
    {
      num: 8,
      date: '2026-07-21',
      neighborhoods: 'Nice · Èze · Monaco',
      title: 'Riviera Day Trip — Hilltop Èze & Monaco',
      description: "Explore the medieval hilltop village of Èze with its exotic garden perched above the sea, then descend to Monaco for the Casino, the Oceanographic Museum, and a taste of royal glamour.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Èze Village & Exotic Garden',
              description: "Perched 427 metres above the sea, Èze is a medieval eagle's nest village. Climb through stone archways and tiny passages to the Jardin Exotique at the summit — the views down to Cap Ferrat and the Mediterranean are staggering.",
              details: [
                '🌵 Jardin Exotique — cacti, succulents, and 360° views',
                '🏘️ The village is car-free — explore on foot',
                '🚌 Bus 82/112 from Nice or drive and park below',
                '🧴 Fragonard perfume factory in Èze — free tour, great for families'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Monaco & Monte Carlo',
              description: "Continue along the coast to the tiny principality of Monaco. The Oceanographic Museum (Jacques Cousteau's legacy) is world-class for families, and kids love watching the changing of the guard at the Prince's Palace. Walk through the Casino gardens for the full Monte Carlo experience.",
              details: [
                '🐠 Oceanographic Museum — touch pool, shark lagoon, rooftop terrace',
                '👑 Prince\'s Palace guard change at 11:55am',
                '🎰 Casino Square — just for the photos (kids can\'t enter)',
                '🚗 Drive the F1 circuit route — point out the tunnel and hairpin!'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Café de Paris, Monte Carlo',
              description: "Belle Époque brasserie on Casino Square. Classic French fare — croque monsieur, salade Niçoise, steak frites. The people-watching of Ferraris and superyachts is the real show.",
              meta: '💰 $$$$ · 📍 Place du Casino, Monte Carlo'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Nice',
              description: "Drive back along the Basse Corniche (Lower Coast Road) for dramatic sunset views over the Mediterranean. Stop at Villefranche-sur-Mer for a quick stroll — it's one of the prettiest small harbours on the Riviera.",
              details: [
                '🌅 The Basse Corniche at sunset is unforgettable',
                '⛵ Villefranche-sur-Mer — pastel houses and a tiny perfect harbour'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.7276, lng: 7.3612, label: 'Èze Village', num: 1, cat: 'attraction', desc: 'Medieval hilltop village with exotic garden' },
        { lat: 43.7311, lng: 7.4263, label: 'Oceanographic Museum', num: 2, cat: 'attraction', desc: "Cousteau's world-class marine museum" },
        { lat: 43.7325, lng: 7.4200, label: "Prince's Palace", num: 3, cat: 'attraction', desc: 'Monaco royal palace with guard changing' },
        { lat: 43.7396, lng: 7.4269, label: 'Casino de Monte-Carlo', num: 4, cat: 'attraction', desc: 'Iconic Belle Époque casino' },
        { lat: 43.7396, lng: 7.4269, label: 'Café de Paris', num: 5, cat: 'food', desc: 'Classic brasserie on Casino Square' },
        { lat: 43.7059, lng: 7.3116, label: 'Villefranche-sur-Mer', num: 6, cat: 'attraction', desc: 'Charming pastel harbour town' }
      ]
    },
    {
      num: 9,
      date: '2026-07-22',
      neighborhoods: 'Nice → Florence · Santa Maria Novella · Duomo',
      title: 'Buongiorno Firenze! — Arrival & the Duomo',
      description: "Fly or train from Nice to Florence and step into the Renaissance. The Duomo's terracotta dome dominates the skyline, and your first gelato in Italy will be a moment of pure family joy.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Travel to Florence',
              description: "Take an early flight from Nice to Florence (1.5 hours) or the scenic train via Genoa (5-6 hours). Arrive by midday and check into your accommodation in the centro storico.",
              details: [
                '✈️ Nice → Florence direct flight ~1.5 hours (easyJet, Vueling)',
                '🚄 Train via Genoa/Pisa is scenic but longer — save for a non-travel day',
                '🏠 Stay near Santa Maria Novella or Santo Spirito for walkability'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Florence Duomo & Baptistery',
              description: "Your first sight of the Florence Cathedral is a gasp-out-loud moment. Brunelleschi's dome — the largest masonry dome ever built — towers over the city. Walk around the exterior first, admiring the green-and-white marble, then visit the Baptistery with Ghiberti's Gates of Paradise.",
              details: [
                '⛪ Climb the dome — 463 steps but the views are incredible (book ahead!)',
                '🚪 Gates of Paradise — Ghiberti\'s gilded bronze doors on the Baptistery',
                '🔔 Giotto\'s Bell Tower — 414 steps, slightly easier than the dome',
                '⏰ Book dome climb online — timed entry required'
              ]
            }
          ],
          meals: [
            {
              type: '🍦 Gelato Break',
              name: 'Vivoli',
              description: "Florence's oldest gelateria, serving since 1930. The crema, pistachio, and dark chocolate are legendary. No cones — cups only, like a true Florentine.",
              meta: '💰 $ · 📍 Via dell\'Isola delle Stinche, 7r'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Piazza della Signoria & First Florentine Dinner',
              description: "Wander to Piazza della Signoria — Florence's open-air sculpture gallery. The copy of Michelangelo's David stands here, alongside Cellini's Perseus and the Loggia dei Lanzi. Then find a family trattoria for your first Florentine steak.",
              details: [
                '🗿 Neptune Fountain, copy of David, and the Loggia sculptures — all free',
                '🏛️ Palazzo Vecchio — Florence\'s medieval town hall, lit up at night'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Trattoria Mario',
              description: "Family-run since 1953, shared tables, no reservations. The bistecca, ribollita (Tuscan bread soup), and house Chianti are everything Florentine dining should be. Cash only.",
              meta: '💰 $$ · 📍 Via Rosina, 2 · Cash only · Shared tables · Lunch is better (closes early)'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.7731, lng: 11.2560, label: 'Florence Duomo', num: 1, cat: 'attraction', desc: "Brunelleschi's iconic dome — climb for city views" },
        { lat: 43.7733, lng: 11.2550, label: 'Baptistery', num: 2, cat: 'attraction', desc: "Ghiberti's Gates of Paradise" },
        { lat: 43.7694, lng: 11.2553, label: 'Piazza della Signoria', num: 3, cat: 'attraction', desc: 'Open-air sculpture gallery and civic heart' },
        { lat: 43.7768, lng: 11.2530, label: 'Vivoli', num: 4, cat: 'food', desc: "Florence's oldest gelateria since 1930" },
        { lat: 43.7767, lng: 11.2533, label: 'Trattoria Mario', num: 5, cat: 'food', desc: 'No-frills Florentine cooking since 1953' }
      ]
    },
    {
      num: 10,
      date: '2026-07-23',
      neighborhoods: 'Uffizi · Ponte Vecchio · Oltrarno',
      title: 'Renaissance Masterpieces & Oltrarno Artisans',
      description: "Spend the morning face-to-face with Botticelli's Venus and da Vinci's Annunciation at the Uffizi, then cross the Ponte Vecchio into the Oltrarno — Florence's artisan quarter where leather-workers and goldsmiths still ply ancient crafts.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Uffizi Gallery',
              description: "One of the world's greatest art museums. The Uffizi holds Botticelli's Birth of Venus and Primavera, works by Leonardo, Raphael, Caravaggio, and Michelangelo. With kids, focus on highlights rather than trying to see everything.",
              details: [
                '🎫 Book timed entry online — essential in July',
                '🖼️ Must-sees: Botticelli Room, Leonardo\'s Annunciation, Caravaggio\'s Medusa',
                '👨‍👩‍👧‍👦 Keep it to 2 hours max with kids — hit the highlights',
                '📸 The corridor windows have stunning Arno River views'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ponte Vecchio & Oltrarno',
              description: "Cross the Ponte Vecchio — the medieval bridge lined with goldsmith shops — into the Oltrarno. This is the real, lived-in Florence: artisan workshops, family trattorias, and neighbourhood piazzas where kids play football. Visit a leather workshop or watch a goldsmith at work.",
              details: [
                '💍 The bridge goldsmiths have been here since 1593',
                '🔨 Scuola del Cuoio (leather school) — watch artisans work, buy quality leather',
                '🏘️ Santo Spirito plaza — local neighbourhood square with church flea market'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'All\'Antico Vinaio',
              description: "Florence's most famous sandwich shop — legendary schiacciata (flatbread) stuffed with cured meats, truffle cream, artichokes, and more. The queue is long but moves fast. Worth every second.",
              meta: '💰 $ · 📍 Via dei Neri, 74r · Expect a queue'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Piazzale Michelangelo Sunset',
              description: "Walk or drive up to Piazzale Michelangelo for THE Florence sunset. The entire city spreads below you — the Duomo, Palazzo Vecchio, the Arno, and the Tuscan hills beyond. Bring a bottle of wine and watch the sky turn gold.",
              details: [
                '🌅 Arrive by 7:30pm to claim a spot on the steps',
                '🍷 Buy wine and snacks from the van — sit on the wall and soak it in',
                '📸 This is the postcard view of Florence'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Il Latini',
              description: "Boisterous, family-style Tuscan restaurant. Prosciutto hangs from the ceiling, pasta is handmade, and the bistecca alla fiorentina is massive. Perfect for a big family dinner.",
              meta: '💰 $$$ · 📍 Via dei Palchetti, 6r'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.7677, lng: 11.2553, label: 'Uffizi Gallery', num: 1, cat: 'attraction', desc: "World's greatest Renaissance art collection" },
        { lat: 43.7680, lng: 11.2531, label: 'Ponte Vecchio', num: 2, cat: 'attraction', desc: 'Medieval bridge with goldsmith shops' },
        { lat: 43.7654, lng: 11.2474, label: 'Oltrarno', num: 3, cat: 'attraction', desc: "Florence's artisan quarter" },
        { lat: 43.7629, lng: 11.2650, label: 'Piazzale Michelangelo', num: 4, cat: 'attraction', desc: 'Panoramic sunset viewpoint over Florence' },
        { lat: 43.7710, lng: 11.2561, label: "All'Antico Vinaio", num: 5, cat: 'food', desc: "Florence's most famous sandwich shop" },
        { lat: 43.7715, lng: 11.2490, label: 'Il Latini', num: 6, cat: 'food', desc: 'Boisterous family-style Tuscan feast' }
      ]
    },
    {
      num: 11,
      date: '2026-07-24',
      neighborhoods: 'Tuscan Countryside · Chianti · San Gimignano',
      title: 'Tuscan Day Trip — Cooking Class, Chianti & Towers',
      description: "Escape into the Tuscan countryside for a hands-on pasta-making class at a family farm, taste Chianti wines amid rolling vineyards, and visit the medieval tower-town of San Gimignano.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Family Pasta-Making Class',
              description: "Drive into the Chianti hills to a family farm for a hands-on cooking class. Learn to make fresh pasta (pici, ravioli, or tagliatelle), bruschetta, and tiramisù. Kids love getting their hands in the dough, and you eat everything you make for lunch.",
              details: [
                '👨‍🍳 Many farms offer family classes — book on Airbnb Experiences or directly',
                '🍝 You\'ll make 3-4 dishes including pasta from scratch',
                '🍷 Adults get Chianti wine pairings during the meal',
                '🐔 Farm animals, olive groves, and vineyard views — pure Tuscany'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'San Gimignano — Medieval Manhattan',
              description: "Drive to San Gimignano, the \"Medieval Manhattan\" famous for its 14 surviving tower houses. The skyline is straight out of a fairy tale. Climb the Torre Grossa for panoramic views, then wander the tiny streets eating the world's best gelato.",
              details: [
                '🗼 14 medieval towers survive (originally 72!) — climb Torre Grossa',
                '🍦 Gelateria Dondoli — 2x Gelato World Champion, in the main piazza',
                '🍷 Vernaccia di San Gimignano — the local white wine, crisp and perfect for summer',
                '📸 The tower skyline against rolling Tuscan hills is magical'
              ]
            }
          ],
          meals: [
            {
              type: '🍦 Afternoon Treat',
              name: 'Gelateria Dondoli',
              description: '2-time World Gelato Champion. The Crema di Santa Fina (saffron cream) and Vernaccia sorbet are unique to San Gimignano. Queue around the piazza but worth it.',
              meta: '💰 $ · 📍 Piazza della Cisterna, 4'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Florence',
              description: "Drive back through the golden Tuscan landscape as the sun sets. Stop at a roadside viewpoint for one last photo of the cypress-lined hills.",
              details: [
                '🚗 ~1.5 hours back to Florence',
                '🌅 The drive through Chianti at golden hour is reason enough for this day trip'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Buca Mario',
              description: "One of Florence's oldest restaurants (since 1886), set in a vaulted cellar. Classic Tuscan fare — pappardelle al cinghiale (wild boar), lampredotto, and tiramisu.",
              meta: '💰 $$$ · 📍 Piazza degli Ottaviani, 16r'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.5287, lng: 11.2163, label: 'Chianti Cooking Farm', num: 1, cat: 'attraction', desc: 'Hands-on pasta making at a Tuscan family farm' },
        { lat: 43.4677, lng: 11.0440, label: 'San Gimignano', num: 2, cat: 'attraction', desc: 'Medieval Manhattan — tower town skyline' },
        { lat: 43.4677, lng: 11.0436, label: 'Gelateria Dondoli', num: 3, cat: 'food', desc: 'World Champion gelato in the main piazza' },
        { lat: 43.4682, lng: 11.0433, label: 'Torre Grossa', num: 4, cat: 'attraction', desc: 'Tallest tower with panoramic views' },
        { lat: 43.7723, lng: 11.2490, label: 'Buca Mario', num: 5, cat: 'food', desc: 'Historic vaulted-cellar Tuscan restaurant' }
      ]
    },
    {
      num: 12,
      date: '2026-07-25',
      neighborhoods: 'Florence → Rome · Trastevere · Centro Storico',
      title: 'The Eternal City — Arrival in Rome',
      description: "High-speed train from Florence to Rome in just 90 minutes. Arrive in the Eternal City and spend the afternoon exploring Trastevere — Rome's most charming neighbourhood, full of ivy-draped trattorias and cobblestone lanes.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Accademia Gallery — Michelangelo\'s David',
              description: "Before leaving Florence, see THE David — Michelangelo's 17-foot marble masterpiece. The moment you turn the corner and see it in person is one of art's greatest experiences. The museum also has Michelangelo's unfinished \"Prisoners\" — fascinating for all ages.",
              details: [
                '🎫 Book timed entry — 8:15am slot is best',
                '🗿 The David is 5.17 metres (17 ft) tall — truly awe-inspiring',
                '📸 No flash photography but photos are allowed',
                '⏰ 45-60 min is enough for most families'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train to Rome & Trastevere Exploration',
              description: "Board the Frecciarossa from Florence Santa Maria Novella to Roma Termini — just 90 minutes. Check into your hotel, then head to Trastevere: Rome's most atmospheric neighbourhood with winding streets, ivy-covered buildings, and the best casual dining in the city.",
              details: [
                '🚄 Frecciarossa — Italy\'s fastest train, 300 km/h, WiFi onboard',
                '🎫 Book on Trenitalia — Super Economy fares from €19',
                '🏘️ Trastevere = \"across the Tiber\" — feels like a village in the city',
                '⛲ Piazza di Santa Maria in Trastevere — one of Rome\'s loveliest squares'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Da Enzo al 29',
              description: "Tiny, beloved Trastevere trattoria serving classic Roman dishes. Cacio e pepe, amatriciana, and fried artichokes that will ruin all other artichokes forever. No reservations — queue early.",
              meta: '💰 $$ · 📍 Via dei Vascellari, 29 · No reservations · Arrive by 7pm'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening Passeggiata in Trastevere',
              description: "Join the Romans for their evening passeggiata (stroll) through Trastevere. Street musicians play on corners, gelato shops glow, and the neighbourhood buzzes with that unmistakable Roman energy. End with gelato at Fior di Luna.",
              details: [
                '🍦 Fior di Luna — small-batch artisan gelato in Trastevere',
                '🎵 Live music drifts from restaurants and buskers on warm evenings'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.7768, lng: 11.2589, label: 'Accademia Gallery', num: 1, cat: 'attraction', desc: "Home of Michelangelo's David" },
        { lat: 41.8819, lng: 12.4700, label: 'Trastevere', num: 2, cat: 'attraction', desc: "Rome's most charming neighbourhood" },
        { lat: 41.8895, lng: 12.4838, label: 'Piazza di Santa Maria in Trastevere', num: 3, cat: 'attraction', desc: 'Beautiful medieval square with golden mosaics' },
        { lat: 41.8853, lng: 12.4740, label: 'Da Enzo al 29', num: 4, cat: 'food', desc: 'Beloved Roman trattoria — cacio e pepe perfection' },
        { lat: 41.8864, lng: 12.4714, label: 'Fior di Luna', num: 5, cat: 'food', desc: 'Artisan gelato in Trastevere' }
      ]
    },
    {
      num: 13,
      date: '2026-07-26',
      neighborhoods: 'Colosseum · Roman Forum · Palatine Hill · Monti',
      title: 'Ancient Rome — Gladiators, Forums & Emperors',
      description: "Step 2,000 years back in time. The Colosseum, Roman Forum, and Palatine Hill are the epic heart of Ancient Rome — and kids who've seen any gladiator movie or read Percy Jackson will be spellbound.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Colosseum',
              description: "The greatest amphitheatre ever built — where 50,000 Romans watched gladiators fight. Walk through the entrance arches, stand in the arena floor area, and imagine the roar of the crowd. The underground level (hypogeum) shows where animals and fighters waited.",
              details: [
                '🎫 Book \"Full Experience\" ticket — includes arena floor + underground',
                '⏰ First entry (8:30am) is cooler and less crowded',
                '👨‍👩‍👧‍👦 The underground tour is incredible for kids — lion cages, trap doors',
                '📸 Best exterior photo: from the Via dei Fori Imperiali side'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Roman Forum & Palatine Hill',
              description: "Walk through the ruins of ancient Rome's political and social centre. The Forum was the beating heart of the Republic — temples, courts, and triumphal arches line the Sacred Way. Climb Palatine Hill for shade, emperor's palace ruins, and views over the Forum and Circus Maximus.",
              details: [
                '🏛️ Must-see: Arch of Titus, Temple of Saturn, House of the Vestals',
                '🌳 Palatine Hill has shade and gardens — welcome relief in July heat',
                '🎫 Included with Colosseum ticket — enter from Via di San Gregorio',
                '💧 Bring water! Nasoni (drinking fountains) are scattered around'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Ai Tre Scalini',
              description: 'No-frills wine bar in the Monti neighbourhood, steps from the Forum. Excellent cold cuts, cheese plates, and house wine. Shady terrace for a cool midday break.',
              meta: '💰 $$ · 📍 Via Panisperna, 251, Monti'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Monti Neighbourhood & Aperitivo',
              description: "Monti is Rome's hippest neighbourhood — just uphill from the Forum. Wander the boutique-lined streets, browse vintage shops, and settle into a bar on Via del Boschetto for aperitivo (drinks + free snacks from 6-8pm).",
              details: [
                '🍹 Aperitivo culture — order a spritz and get free snacks',
                '🛍️ Vintage shops and indie boutiques on Via del Boschetto',
                '🏘️ Quieter and more local than the tourist centre'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Felice a Testaccio',
              description: "The temple of cacio e pepe. This Testaccio institution has been perfecting Rome's signature pasta since 1936. The tonnarelli cacio e pepe is prepared tableside. Book well ahead.",
              meta: '💰 $$$ · 📍 Via Mastro Giorgio, 29, Testaccio · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8902, lng: 12.4922, label: 'Colosseum', num: 1, cat: 'attraction', desc: 'Ancient amphitheatre — gladiator arena for 50,000' },
        { lat: 41.8925, lng: 12.4853, label: 'Roman Forum', num: 2, cat: 'attraction', desc: 'Ruins of ancient Rome\'s civic heart' },
        { lat: 41.8891, lng: 12.4875, label: 'Palatine Hill', num: 3, cat: 'attraction', desc: 'Emperor\'s hill with gardens and views' },
        { lat: 41.8945, lng: 12.4932, label: 'Monti', num: 4, cat: 'attraction', desc: 'Hip neighbourhood with boutiques and aperitivo bars' },
        { lat: 41.8945, lng: 12.4942, label: 'Ai Tre Scalini', num: 5, cat: 'food', desc: 'Charming wine bar in Monti' },
        { lat: 41.8766, lng: 12.4768, label: 'Felice a Testaccio', num: 6, cat: 'food', desc: 'Temple of cacio e pepe since 1936' }
      ]
    },
    {
      num: 14,
      date: '2026-07-27',
      neighborhoods: 'Vatican City · Pantheon · Piazza Navona · Trevi',
      title: 'Vatican, Pantheon & Fountains of Rome',
      description: "The Vatican Museums and Sistine Chapel in the morning, then an afternoon hitting Rome's greatest hits: the Pantheon, Piazza Navona, and the Trevi Fountain — throw a coin and make a wish.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Vatican Museums & Sistine Chapel',
              description: "Enter the Vatican Museums early and work your way through one of the world's greatest art collections to the Sistine Chapel — Michelangelo's ceiling is a moment that transcends words. Then visit St. Peter's Basilica, the largest church on Earth.",
              details: [
                '🎫 Book skip-the-line tickets or a guided tour — non-negotiable in July',
                '⏰ 7:30am entry (if available) or 8am — the Sistine Chapel gets mobbed by 10am',
                '🖼️ Gallery of Maps, Raphael Rooms, then Sistine Chapel — follow the route',
                '⛪ St. Peter\'s is free — enter from the right side of the square after the museums',
                '👗 Dress code enforced: knees and shoulders covered for everyone'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pantheon',
              description: "The best-preserved ancient Roman building — 2,000 years old and still awe-inspiring. The oculus (open hole in the dome) lets in a perfect cylinder of light. Stand underneath and look up — it's a spiritual experience.",
              details: [
                '🎫 Free entry but timed tickets now required — book online',
                '🕳️ The oculus is 9 metres wide — rain falls straight through',
                '⚱️ Raphael is buried here'
              ]
            },
            {
              title: 'Piazza Navona & Trevi Fountain',
              description: "Walk to Piazza Navona — Bernini's Fountain of the Four Rivers is a baroque masterpiece. Then weave through the lanes to the Trevi Fountain — toss a coin with your right hand over your left shoulder to ensure you'll return to Rome.",
              details: [
                '⛲ Trevi Fountain — visit at 8am or 10pm to avoid massive crowds',
                '🪙 Legend: one coin = return to Rome, two = find love, three = marriage',
                '🎨 Street artists in Piazza Navona — get a family caricature!'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Armando al Pantheon',
              description: "Family-run since 1961, steps from the Pantheon. Classic Roman dishes — gricia, supplì, saltimbocca. Incredibly good for a tourist-area restaurant.",
              meta: '💰 $$$ · 📍 Salita dei Crescenzi, 31 · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Spanish Steps & Evening Stroll',
              description: "Walk to the Spanish Steps and Piazza di Spagna, then stroll Via del Corso for shopping. End at Piazza del Popolo with its twin churches and Egyptian obelisk — beautiful at night.",
              details: [
                '🛍️ Via Condotti — luxury shopping (Gucci, Prada, etc.)',
                '⛲ Piazza del Popolo — grand square with Bernini churches'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Roscioli',
              description: "Part restaurant, part deli, part wine bar — Roscioli is a Roman food temple. The carbonara is legendary, the wine list is biblical, and the cheese counter will make you weep with joy.",
              meta: '💰 $$$$ · 📍 Via dei Giubbonari, 21 · Book well ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.9065, lng: 12.4536, label: 'Vatican Museums', num: 1, cat: 'attraction', desc: "World's greatest art collection + Sistine Chapel" },
        { lat: 41.9022, lng: 12.4539, label: "St. Peter's Basilica", num: 2, cat: 'attraction', desc: 'Largest church in the world' },
        { lat: 41.8986, lng: 12.4769, label: 'Pantheon', num: 3, cat: 'attraction', desc: '2,000-year-old temple with oculus' },
        { lat: 41.8992, lng: 12.4731, label: 'Piazza Navona', num: 4, cat: 'attraction', desc: "Bernini's baroque fountain masterpiece" },
        { lat: 41.9009, lng: 12.4833, label: 'Trevi Fountain', num: 5, cat: 'attraction', desc: 'Throw a coin to return to Rome' },
        { lat: 41.8986, lng: 12.4769, label: 'Armando al Pantheon', num: 6, cat: 'food', desc: 'Classic Roman trattoria since 1961' },
        { lat: 41.8964, lng: 12.4761, label: 'Roscioli', num: 7, cat: 'food', desc: 'Roman food temple — legendary carbonara' }
      ]
    },
    {
      num: 15,
      date: '2026-07-28',
      neighborhoods: 'Rome → Amalfi Coast · Positano · Amalfi',
      title: 'Amalfi Coast — Cliffs, Colour & Limoncello',
      description: "Leave Rome behind and head south to the Amalfi Coast — one of the most dramatic coastlines on Earth. Pastel villages cling to impossible cliffs above turquoise water. Check into Positano and feel like you've entered a dream.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Travel to the Amalfi Coast',
              description: "Take the high-speed train from Rome to Naples (70 min), then a private transfer or SITA bus to the coast. The winding road down to Positano — with its first reveal of coloured houses tumbling to the sea — is one of travel's great moments.",
              details: [
                '🚄 Roma Termini → Napoli Centrale — Frecciarossa, 70 min',
                '🚐 Private transfer from Naples to Positano (~90 min) — worth it with 5+ people and luggage',
                '🚌 SITA bus from Sorrento is cheaper but winding — sit front for views, take motion sickness pills',
                '⚠️ The coast road is narrow and winding — not for the faint-hearted!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Positano — First Wander',
              description: "Drop your bags and explore Positano on foot. The village cascades down the cliff in layers of pink, yellow, and white — connected by steep stepped pathways. Every turn reveals a new view. Walk down to Spiaggia Grande (the main beach) and stick your feet in the Tyrrhenian Sea.",
              details: [
                '🏖️ Spiaggia Grande — rent umbrellas and chairs, or use the free section',
                '👗 Positano is famous for linen and resort wear — browse the boutiques',
                '🍋 Try granita al limone — the lemons here are the size of your head',
                '📸 Best photo of Positano: from the coast road above, or from the beach looking up'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Da Vincenzo',
              description: 'Family-run restaurant up the steps in Positano. Fresh seafood, homemade pasta with Amalfi lemons, and a vine-covered terrace with sea views.',
              meta: '💰 $$$ · 📍 Viale Pasitea, 172, Positano'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from the Cliff Path',
              description: "Walk the Sentiero degli Dei trailhead path above Positano for a sunset you'll never forget — the entire coastline glows gold and pink as the sun drops into the sea. Or simply watch from your terrace with a glass of local Falanghina wine.",
              details: [
                '🌅 Sunset views from Franco\'s Bar terrace — cocktails + coast panorama',
                '🍷 Falanghina and Greco di Tufo — local white wines perfect for summer'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'La Tagliata',
              description: "A family farm restaurant perched high above Positano with vertigo-inducing sea views. They serve a set multi-course feast — antipasti, pasta, meat, dessert — all from their farm. The drive up is an adventure in itself.",
              meta: '💰 $$$ · 📍 Via Tagliata, 22 · They pick you up from Positano · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.6281, lng: 14.4849, label: 'Positano', num: 1, cat: 'attraction', desc: 'Iconic pastel village cascading down cliffs to the sea' },
        { lat: 40.6282, lng: 14.4867, label: 'Spiaggia Grande', num: 2, cat: 'attraction', desc: "Positano's main beach" },
        { lat: 40.6285, lng: 14.4855, label: 'Da Vincenzo', num: 3, cat: 'food', desc: 'Family-run seafood with sea-view terrace' },
        { lat: 40.6390, lng: 14.4800, label: 'La Tagliata', num: 4, cat: 'food', desc: 'Farm restaurant with vertiginous coast views' },
        { lat: 40.6340, lng: 14.6023, label: 'Amalfi', num: 5, cat: 'attraction', desc: 'Historic maritime republic on the coast' }
      ]
    },
    {
      num: 16,
      date: '2026-07-29',
      neighborhoods: 'Amalfi · Ravello · Capri (optional)',
      title: 'Amalfi, Ravello & Final Mediterranean Magic',
      description: "Your grand finale: explore the town of Amalfi with its Arab-Norman cathedral, then climb to Ravello — the \"City of Music\" — for gardens with views that Wagner and Gore Vidal called the most beautiful in the world. A perfect final day in paradise.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Amalfi Town',
              description: "Take the ferry or bus along the coast to Amalfi town. The Cathedral of St. Andrew with its striped Arab-Norman facade dominates the piazza. Explore the tiny lanes behind the cathedral — the old paper mills and lemon groves hidden in the ravine are magical.",
              details: [
                '⛪ Cathedral of St. Andrew — climb the 57 steps, visit the Cloister of Paradise',
                '📜 Museo della Carta — ancient paper mill still powered by water',
                '🚢 Ferry from Positano to Amalfi — 25 min, gorgeous coastal views',
                '🍋 Paper and lemon products are Amalfi\'s signature souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Trattoria Il Mulino',
              description: 'Hidden in the lanes behind Amalfi\'s cathedral. Family cooking, fresh catch of the day, homemade lemon pasta (scialatielli ai frutti di mare). Covered terrace among lemon trees.',
              meta: '💰 $$ · 📍 Via delle Cartiere, Amalfi'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ravello — Gardens in the Sky',
              description: "Bus or drive up the winding road to Ravello, perched 350 metres above the sea. Visit Villa Rufolo — its gardens inspired Wagner's Parsifal — and Villa Cimbrone, whose Terrace of Infinity is one of the most photographed viewpoints in Italy. This is the exclamation point on your European summer.",
              details: [
                '🌺 Villa Rufolo — Moorish gardens and summer concert stage',
                '♾️ Villa Cimbrone — the Terrace of Infinity will literally take your breath away',
                '🎵 Ravello Festival — summer concerts at Villa Rufolo (check schedule)',
                '🚌 Bus from Amalfi to Ravello — 25 min of hairpin turns with incredible views'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Sunset & Farewell Dinner',
              description: "Return to Positano for one last golden sunset over the Mediterranean. Toast to 16 days of unforgettable family memories — from Barcelona's tapas bars to Rome's ancient ruins to this glittering coast. This is the trip of a lifetime.",
              details: [
                '🌅 Watch the sunset from your terrace or Franco\'s Bar',
                '🥂 Raise a limoncello to the journey — you\'ve earned it',
                '📸 Final family photo with Positano\'s lights twinkling below'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Il Ritrovo',
              description: "Chef Salvatore's mountain restaurant above Positano. Fresh pasta with foraged herbs, wood-fired pizza, and the most honest, soulful cooking on the coast. A perfect farewell dinner for a perfect trip.",
              meta: '💰 $$$ · 📍 Via Montepertuso, 77, Positano · Free shuttle from town'
            }
          ],
          tips: [
            { type: 'tip', text: "For departure on July 30: arrange a morning transfer from Positano to Naples airport (NAP) or train station. The coast road is slow — allow 2+ hours. Or take the SITA bus to Sorrento and Circumvesuviana train to Naples." }
          ]
        }
      ],
      mapPins: [
        { lat: 40.6340, lng: 14.6023, label: 'Amalfi Cathedral', num: 1, cat: 'attraction', desc: 'Stunning Arab-Norman cathedral on the piazza' },
        { lat: 40.6345, lng: 14.6030, label: 'Trattoria Il Mulino', num: 2, cat: 'food', desc: 'Hidden gem with lemon pasta among lemon trees' },
        { lat: 40.6492, lng: 14.6115, label: 'Villa Rufolo, Ravello', num: 3, cat: 'attraction', desc: 'Moorish gardens that inspired Wagner' },
        { lat: 40.6460, lng: 14.6130, label: 'Villa Cimbrone, Ravello', num: 4, cat: 'attraction', desc: 'Terrace of Infinity — most beautiful viewpoint in Italy' },
        { lat: 40.6281, lng: 14.4849, label: 'Positano', num: 5, cat: 'attraction', desc: 'Final sunset in paradise' },
        { lat: 40.6350, lng: 14.4750, label: 'Il Ritrovo', num: 6, cat: 'food', desc: 'Mountain restaurant — soulful farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$120–200/night', midrange: '$250–450/night', luxury: '$500–1500/night' },
    { category: 'Meals (family of 5)', budget: '$100–180/day', midrange: '$200–350/day', luxury: '$400–800/day' },
    { category: 'Transport (inter-city)', budget: '$50–100/day', midrange: '$100–200/day', luxury: '$200–400/day (private)' },
    { category: 'Activities & Entry', budget: '$30–60/day', midrange: '$60–150/day', luxury: '$150–400/day (private guides)' },
    { category: 'Day Trips', budget: '$50–100/trip', midrange: '$100–250/trip', luxury: '$300–600/trip (private)' },
    { category: '16-Day Total (family of 5)', budget: '$6,000–10,000', midrange: '$12,000–22,000', luxury: '$25,000–50,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There & Away', items: ['Fly into Barcelona El Prat (BCN)', 'Fly home from Naples (NAP) or Rome Fiumicino (FCO)', 'Open-jaw ticket (into BCN, out of NAP) saves backtracking', 'Book inter-city trains on SNCF, Trenitalia, or Italo'] },
    { title: '🏨 Where to Stay', items: ['Barcelona: Gothic Quarter or Eixample for walkability', 'Avignon: Inside the walled city, near Palais des Papes', 'Nice: Vieux Nice or Promenade des Anglais', 'Florence: Centro Storico or Santo Spirito (Oltrarno)', 'Rome: Trastevere, Monti, or Centro Storico', 'Amalfi Coast: Positano for views, Amalfi town for access'] },
    { title: '🌡️ July Weather', items: ['Barcelona: 28-32°C, sunny, beach weather', 'Provence: 30-35°C, dry heat, lavender in peak bloom', 'Nice: 27-30°C, warm Mediterranean, calm seas', 'Florence: 32-38°C, very hot — sightsee early and late, siesta midday', 'Rome: 30-36°C, hot but manageable with breaks and gelato', 'Amalfi: 28-32°C, coastal breeze helps, warm swimming water'] },
    { title: '💳 Money & Tipping', items: ['Euro used everywhere (Spain, France, Italy)', 'Cards widely accepted but carry €50-100 cash for markets and small towns', 'Tipping: not mandatory in Europe. Round up or leave 5-10% for great service', 'Service charge (coperto) in Italy is normal — not a tip'] },
    { title: '👨‍👩‍👧‍👦 Family Travel Tips', items: ['Skip-the-line tickets are essential everywhere in July — book 2+ weeks ahead', 'Siesta time (2-5pm): rest at the hotel, swim, or do gelato runs', 'Kids under 18 are free at many Italian state museums', 'Pack a universal EU power adapter (Type C/F)', 'Travel insurance with medical coverage is highly recommended'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
