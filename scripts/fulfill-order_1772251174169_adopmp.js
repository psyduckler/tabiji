const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772251174169_adopmp',
  email: 'shreya.nalla@gmail.com',
  destination: 'Boston, MA, USA',
  startDate: '2026-04-27',
  endDate: '2026-05-28',
  groupSize: 5,
  requests: 'Multi-city road trip: Boston → NYC → New Haven → Las Vegas → Grand Canyon → Salt Lake City → Yellowstone → Chicago. Cousins grad ceremonies Apr 29 & May 1 at Northeastern. Brothers grad May 8 in New Haven. Cultural & foodie focus, casual dining, group of 5+.'
};

const itineraryData = {
  destination: 'Boston to Chicago',
  countryEmoji: '🇺🇸',
  title: 'The Great American Road Trip: Coast to Canyon to City',
  subtitle: '31 days across 8 cities — graduations, national parks & the best food in America',
  description: "This epic cross-country journey begins with family celebrations in Boston and ends with deep-dish in Chicago. Along the way, you'll explore the cultural riches of NYC, taste legendary New Haven pizza, hit the neon lights of Vegas, stand on the rim of the Grand Canyon, watch geysers erupt in Yellowstone, and eat your way through Chicago's incredible food scene. It's a trip that covers the full spectrum of America — ivy-league campuses, towering skyscrapers, red-rock canyons, and wild geothermal landscapes — all tied together by family milestones and unforgettable meals.",
  duration: '31 nights',
  dates: 'Apr 27 – May 28, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups & Families',
  highlights: [
    'Two Northeastern University graduation ceremonies in Boston',
    'Walking the Freedom Trail & eating lobster rolls',
    'NYC food crawl — pizza, bagels, dim sum, and everything between',
    'Legendary New Haven apizza at Frank Pepe\'s & Sally\'s',
    'Las Vegas Strip by night & Fremont Street experience',
    'Sunrise over the Grand Canyon South Rim',
    'Old Faithful & the Grand Prismatic Spring in Yellowstone',
    'Chicago deep-dish, architecture boat tour & Millennium Park'
  ],

  essentials: [
    { title: '🎓 Graduation Schedule', text: 'April 29 and May 1 — Northeastern University ceremonies in Boston. May 8 — graduation ceremony in New Haven. Plan outfits and arrive early to secure good seats.' },
    { title: '🚗 Road Trip Segments', text: 'NYC to New Haven is ~90 min by car. Vegas to Grand Canyon South Rim is ~4.5 hours. Grand Canyon to SLC is ~6.5 hours. SLC to Yellowstone (West Entrance) is ~5 hours. Budget for gas, snacks, and scenic stops.' },
    { title: '🏔️ Yellowstone in May', text: 'Mid-May in Yellowstone means some roads may still be opening for the season. Expect cool temps (30-55°F), possible snow, and fewer crowds. Pack layers, waterproof jackets, and sturdy hiking boots.' },
    { title: '💰 Budget Tips', text: 'Book flights early (Boston→Vegas, SLC→Chicago). Share Airbnbs for the group. Casual dining keeps costs down — this itinerary focuses on local gems over fine dining. National park passes are $35/vehicle.' }
  ],

  days: [
    // ===== BOSTON: Apr 27-30 =====
    {
      num: 1,
      date: '2026-04-27',
      neighborhoods: 'Back Bay · Beacon Hill · Boston Common',
      title: 'Arrival in Boston — Lobster & the Common',
      description: "Touch down in Boston and get your bearings in one of America's most walkable cities. Stroll through the Public Garden, explore Beacon Hill's gas-lit streets, and kick off the trip with New England's finest lobster roll.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Boston Common & Public Garden',
              description: "America's oldest public park is the perfect first stop. Walk through the Public Garden, see the famous Swan Boats (if running), and cross into Beacon Hill — one of the most photogenic neighborhoods in the country with its brick row houses and gas lanterns.",
              details: [
                '🌳 Boston Common dates to 1634 — oldest city park in the US',
                '🦢 Swan Boats in the Public Garden run late April through September',
                '📸 Acorn Street in Beacon Hill — the most photographed street in America'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Late Lunch',
              name: 'Neptune Oyster',
              description: 'Tiny North End spot famous for the best lobster roll in Boston — warm, buttered, overflowing. Worth the wait.',
              meta: '💰 $$ · 📍 63 Salem St, North End · Cash only, expect a line'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'North End Food Walk',
              description: "Boston's Little Italy is packed with incredible Italian restaurants, bakeries, and cafés. Walk Hanover Street, grab cannoli from Mike's Pastry or Modern Pastry, and soak in the old-world atmosphere.",
              details: [
                '🍝 Carmelina\'s for hearty Italian — no reservations, casual vibe',
                '🍰 Mike\'s Pastry vs. Modern Pastry — the eternal Boston debate',
                '🍷 Stroll Hanover Street and people-watch'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Carmelina\'s',
              description: 'Beloved North End Italian spot — massive portions, lively atmosphere, and the garlic bread is legendary. Perfect for a big group.',
              meta: '💰 $$ · 📍 307 Hanover St, North End'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3551, lng: -71.0656, label: 'Boston Common', num: 1, cat: 'attraction', desc: "America's oldest public park" },
        { lat: 42.3541, lng: -71.0707, label: 'Public Garden', num: 2, cat: 'attraction', desc: 'Swan Boats and beautiful gardens' },
        { lat: 42.3588, lng: -71.0707, label: 'Beacon Hill', num: 3, cat: 'attraction', desc: 'Gas-lit streets and brick row houses' },
        { lat: 42.3636, lng: -71.0553, label: 'Neptune Oyster', num: 4, cat: 'food', desc: "Boston's best lobster roll" },
        { lat: 42.3634, lng: -71.0533, label: "Carmelina's", num: 5, cat: 'food', desc: 'Hearty North End Italian' }
      ]
    },
    {
      num: 2,
      date: '2026-04-28',
      neighborhoods: 'Freedom Trail · Faneuil Hall · Seaport',
      title: 'Freedom Trail & Faneuil Hall',
      description: "Walk the 2.5-mile Freedom Trail through 16 historic sites spanning the American Revolution, feast at Faneuil Hall Marketplace, and explore Boston's buzzy Seaport District.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Freedom Trail Walk',
              description: "Follow the red-brick line from Boston Common through 16 of America's most important Revolutionary War sites. Pass the Massachusetts State House, Park Street Church, the Old North Church, and Paul Revere's House.",
              details: [
                '🧱 2.5 miles, about 2-3 hours at a leisurely pace',
                '⛪ Old North Church — where the "one if by land, two if by sea" lanterns hung',
                '🏠 Paul Revere House — oldest remaining structure in downtown Boston (1680)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Faneuil Hall & Quincy Market',
              description: "Historic marketplace turned food hall. Grab lunch from the dozens of food stalls inside Quincy Market — clam chowder in a bread bowl is the move. Street performers and local vendors make it a lively scene.",
              details: [
                '🥣 Boston Chowda Co. inside Quincy Market — award-winning chowder',
                '🎭 Street performers on the cobblestone plaza',
                '🛍️ Browse local artisan shops in the surrounding buildings'
              ]
            }
          ],
          meals: [
            {
              type: '🥣 Lunch',
              name: 'Boston Chowda Co.',
              description: 'Award-winning New England clam chowder in a bread bowl at Quincy Market. Thick, creamy, and full of clams.',
              meta: '💰 $ · 📍 Quincy Market, Faneuil Hall'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Seaport District',
              description: "Boston's trendiest neighborhood — waterfront restaurants, the ICA museum, and great cocktail bars. Walk along the Harborwalk as the sun sets over the harbor.",
              details: [
                '🎨 Institute of Contemporary Art — stunning waterfront architecture',
                '🍸 Envoy Hotel rooftop bar — harbor views and cocktails',
                '🚶 Harborwalk for a scenic evening stroll'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Row 34',
              description: 'Stylish Seaport oyster bar and seafood restaurant. Excellent raw bar, craft beers, and a fun, lively atmosphere perfect for groups.',
              meta: '💰 $$$ · 📍 383 Congress St, Seaport'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3554, lng: -71.0640, label: 'Freedom Trail Start', num: 1, cat: 'attraction', desc: '2.5-mile historic walk through Revolutionary Boston' },
        { lat: 42.3601, lng: -71.0569, label: 'Faneuil Hall', num: 2, cat: 'attraction', desc: 'Historic marketplace and food hall' },
        { lat: 42.3633, lng: -71.0544, label: "Old North Church", num: 3, cat: 'attraction', desc: 'Where the lantern signal was hung for Paul Revere' },
        { lat: 42.3491, lng: -71.0424, label: 'Seaport District', num: 4, cat: 'attraction', desc: "Boston's trendiest waterfront neighborhood" },
        { lat: 42.3506, lng: -71.0449, label: 'Row 34', num: 5, cat: 'food', desc: 'Stylish oyster bar in the Seaport' }
      ]
    },
    {
      num: 3,
      date: '2026-04-29',
      neighborhoods: 'Northeastern University · Fenway · South End',
      title: '🎓 Graduation Day #1 — Northeastern University',
      description: "The first big celebration! Attend your cousin's graduation ceremony at Northeastern, then explore the Fenway neighborhood and celebrate with a special dinner in the South End.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: '🎓 Northeastern University Graduation Ceremony',
              description: "Arrive early to secure good seats for the commencement ceremony. Northeastern's campus is beautiful in late April with spring blooms. Bring tissues — it's going to be emotional!",
              details: [
                '🎓 Arrive at least 1 hour early for seating',
                '📸 Photo ops around campus — Centennial Common is great',
                '👔 Dress semi-formal — spring weather can be unpredictable in Boston',
                '📍 Check Northeastern website for exact ceremony location and time'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Post-Ceremony Celebration',
              description: "After the ceremony, take a walk through the Fens — a beautiful Frederick Law Olmsted-designed green space adjacent to campus. The Rose Garden is beginning to bloom in late April.",
              details: [
                '🌹 Kelleher Rose Garden in the Back Bay Fens',
                '🏟️ Walk past Fenway Park — even from outside, it\'s iconic',
                '📸 Group photos at the Northeastern sign and around campus'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'El Jefe\'s Taqueria',
              description: 'Casual, delicious burritos and tacos right near Northeastern\'s campus. Perfect post-ceremony fuel — big portions, affordable, and fun.',
              meta: '💰 $ · 📍 83 Gainsborough St, Fenway'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Celebration Dinner',
              name: 'The Salty Pig',
              description: 'Charcuterie boards, artisan pizzas, and an incredible craft beer list. Casual-upscale vibe perfect for a graduation celebration with a big group.',
              meta: '💰 $$ · 📍 130 Dartmouth St, Back Bay'
            }
          ],
          tips: [
            { type: 'tip', text: 'Make a reservation for dinner — graduation weekends are busy across the city. Book at least a week in advance.' }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3398, lng: -71.0892, label: 'Northeastern University', num: 1, cat: 'attraction', desc: 'Graduation ceremony venue' },
        { lat: 42.3425, lng: -71.0963, label: 'Kelleher Rose Garden', num: 2, cat: 'attraction', desc: 'Beautiful garden in the Back Bay Fens' },
        { lat: 42.3467, lng: -71.0972, label: 'Fenway Park', num: 3, cat: 'attraction', desc: 'Iconic baseball stadium' },
        { lat: 42.3400, lng: -71.0900, label: "El Jefe's Taqueria", num: 4, cat: 'food', desc: 'Casual burritos near Northeastern' },
        { lat: 42.3474, lng: -71.0762, label: 'The Salty Pig', num: 5, cat: 'food', desc: 'Charcuterie and craft beer in Back Bay' }
      ]
    },
    {
      num: 4,
      date: '2026-04-30',
      neighborhoods: 'Cambridge · Harvard · MIT',
      title: 'Cambridge Day — Harvard, MIT & Brunch',
      description: "Cross the Charles River to Cambridge and explore two of the world's most famous universities. Wander Harvard Yard, geek out at MIT, and discover the incredible food scene along Massachusetts Avenue.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Harvard Yard & Harvard Square',
              description: "Walk through the hallowed gates of Harvard Yard, rub the foot of the John Harvard statue for luck, and explore Harvard Square's bookshops, buskers, and cafés.",
              details: [
                '📸 Touch the John Harvard statue\'s foot — it\'s tradition (and always shiny)',
                '📚 Harvard Book Store — incredible indie bookshop',
                '🏛️ Harvard Art Museums — world-class collection, free with student ID'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'The Friendly Toast',
              description: 'Funky, eclectic brunch spot with creative dishes, big portions, and a fun vibe. Think pumpkin pancakes, breakfast burritos, and craft cocktails.',
              meta: '💰 $$ · 📍 1 Kendall Square, Cambridge'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'MIT Campus & The Infinite Corridor',
              description: "Walk through MIT's campus along the Charles River. See the iconic Great Dome, the Stata Center (Frank Gehry's wildest building), and the Media Lab. The campus is an architectural playground.",
              details: [
                '🏗️ Stata Center — looks like it\'s melting, Frank Gehry masterpiece',
                '🔬 MIT Museum — quirky exhibits on robots, holograms, and kinetic art',
                '🌊 Memorial Drive along the Charles — great for a group walk'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Charles River Esplanade',
              description: 'Walk along the Boston side of the Charles River as the sun sets. The Esplanade is beautiful in spring — sailboats, joggers, and the Boston skyline reflecting on the water.',
              details: [
                '🌅 Best sunset views from the Longfellow Bridge',
                '⛵ Community Boating offers sunset sailing (seasonal)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shy Bird',
              description: 'Farm-to-table casual dining in Cambridge with an incredible rotisserie chicken and seasonal menu. Warm, welcoming atmosphere great for groups.',
              meta: '💰 $$ · 📍 1 Kendall Square, Cambridge'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3744, lng: -71.1169, label: 'Harvard Yard', num: 1, cat: 'attraction', desc: 'Walk through one of the most famous campuses in the world' },
        { lat: 42.3736, lng: -71.1189, label: 'Harvard Square', num: 2, cat: 'attraction', desc: 'Bookshops, buskers, and café culture' },
        { lat: 42.3601, lng: -71.0942, label: 'MIT Campus', num: 3, cat: 'attraction', desc: 'Iconic campus with stunning architecture' },
        { lat: 42.3625, lng: -71.0855, label: 'The Friendly Toast', num: 4, cat: 'food', desc: 'Eclectic brunch spot in Kendall Square' },
        { lat: 42.3625, lng: -71.0855, label: 'Shy Bird', num: 5, cat: 'food', desc: 'Farm-to-table casual dining' }
      ]
    },
    {
      num: 5,
      date: '2026-05-01',
      neighborhoods: 'Northeastern University · Fenway · Newbury Street',
      title: '🎓 Graduation Day #2 — Northeastern University',
      description: "Round two! Attend the second graduation ceremony at Northeastern, then celebrate on iconic Newbury Street with shopping and a festive group dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: '🎓 Northeastern University Graduation Ceremony #2',
              description: "Second cousin's big day! Same drill — arrive early, dress well, bring the energy. You know the campus now, so navigate like a pro.",
              details: [
                '🎓 Same tips as Day 3 — arrive early, check the website for exact time/location',
                '📸 Get the family group photo you missed last time',
                '🎉 This calls for an extra-special celebration tonight'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Newbury Street Shopping & Strolling',
              description: "Boston's premier shopping street — eight blocks of boutiques, galleries, cafés, and brownstones. Great for a post-ceremony wind-down. The street gets more eclectic (and affordable) as you walk from Arlington toward Mass Ave.",
              details: [
                '🛍️ Boutiques, vintage shops, and galleries line both sides',
                '☕ Trident Booksellers & Café — beloved bookshop-café combo',
                '🎨 Galleries on the upper blocks toward Mass Ave'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Trident Booksellers & Café',
              description: 'Iconic Newbury Street bookshop and café. Browse books while waiting for your avocado toast and house-roasted coffee.',
              meta: '💰 $$ · 📍 338 Newbury St, Back Bay'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Celebration Dinner',
              name: 'Buttermilk & Bourbon',
              description: 'Southern-inspired comfort food in Back Bay — fried chicken, biscuits, shrimp & grits, and a killer bourbon cocktail list. Fun, festive, and perfect for celebrating.',
              meta: '💰 $$ · 📍 160 Commonwealth Ave, Back Bay'
            }
          ],
          tips: [
            { type: 'tip', text: 'Last night in Boston! Pack tonight so you can leave for NYC first thing tomorrow morning.' }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3398, lng: -71.0892, label: 'Northeastern University', num: 1, cat: 'attraction', desc: 'Graduation ceremony #2' },
        { lat: 42.3501, lng: -71.0837, label: 'Newbury Street', num: 2, cat: 'attraction', desc: 'Premier shopping and dining street' },
        { lat: 42.3492, lng: -71.0858, label: 'Trident Booksellers', num: 3, cat: 'food', desc: 'Bookshop-café on Newbury Street' },
        { lat: 42.3517, lng: -71.0743, label: 'Buttermilk & Bourbon', num: 4, cat: 'food', desc: 'Southern comfort food celebration dinner' }
      ]
    },

    // ===== NYC: May 2-7 =====
    {
      num: 6,
      date: '2026-05-02',
      neighborhoods: 'Lower Manhattan · SoHo · Chinatown',
      title: 'NYC Arrival — Downtown Manhattan',
      description: "Take the train or drive from Boston to NYC (~4 hours). Dive straight into Lower Manhattan's incredible energy — walk the Brooklyn Bridge, explore SoHo, and feast in Chinatown.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Travel: Boston → New York City',
              description: 'Drive or take Amtrak from Boston to NYC. The Amtrak Acela takes ~3.5 hours and drops you at Penn Station in Midtown. If driving, budget 4-5 hours with traffic.',
              details: [
                '🚂 Amtrak Acela: Boston South Station → NYC Penn Station (~3.5 hrs)',
                '🚗 Driving: I-90 W to I-84 to I-95 S, about 4-5 hours',
                '💡 Book Amtrak early for best prices — group of 5+ should compare cost vs. rental car'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Brooklyn Bridge Walk',
              description: 'Walk across the Brooklyn Bridge from the Manhattan side for stunning views of the skyline and the Statue of Liberty in the distance. End in DUMBO for the famous Manhattan Bridge photo from Washington Street.',
              details: [
                '🌉 Walk takes about 30 minutes — go slowly and enjoy the views',
                '📸 DUMBO — Washington Street for the iconic Manhattan Bridge frame photo',
                '🍦 Brooklyn Ice Cream Factory on the waterfront'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chinatown Food Crawl',
              description: "NYC's Chinatown is one of the best food neighborhoods in the world. Walk Mott Street and Canal Street, popping into noodle shops, dumpling houses, and bakeries.",
              details: [
                '🥟 Joe\'s Shanghai — legendary soup dumplings (xiao long bao)',
                '🍜 Xi\'an Famous Foods — hand-pulled noodles and cumin lamb',
                '🧋 Bubble tea from Tiger Sugar or Boba Guys'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Dinner',
              name: 'Joe\'s Shanghai',
              description: 'The soup dumpling institution. Order the crab & pork xiao long bao and prepare for flavor explosion. Cash only, no frills, incredible food.',
              meta: '💰 $$ · 📍 46 Bowery, Chinatown'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7061, lng: -73.9969, label: 'Brooklyn Bridge', num: 1, cat: 'attraction', desc: 'Walk across for iconic NYC skyline views' },
        { lat: 40.7033, lng: -73.9894, label: 'DUMBO', num: 2, cat: 'attraction', desc: 'Manhattan Bridge photo spot and waterfront' },
        { lat: 40.7148, lng: -73.9970, label: 'Chinatown', num: 3, cat: 'attraction', desc: 'Incredible food neighborhood' },
        { lat: 40.7148, lng: -73.9981, label: "Joe's Shanghai", num: 4, cat: 'food', desc: 'Legendary soup dumplings' }
      ]
    },
    {
      num: 7,
      date: '2026-05-03',
      neighborhoods: 'Midtown · Times Square · Central Park',
      title: 'Iconic Manhattan — Central Park to Times Square',
      description: "Hit the big-ticket Manhattan landmarks: Central Park in the morning, the Met or MoMA in the afternoon, and the sensory overload of Times Square at night.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Central Park',
              description: "Enter from the south and walk through the Mall, past Bethesda Fountain, and up to the Bow Bridge. In early May, the cherry blossoms may still be lingering and the park is lush and green.",
              details: [
                '🌸 Bethesda Fountain — the heart of the park',
                '🌉 Bow Bridge — most romantic spot in Central Park',
                '🚣 Rent a rowboat on the Lake (seasonal, weather permitting)',
                '🏰 Belvedere Castle for panoramic park views'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Sarabeth\'s Central Park South',
              description: 'Classic NYC brunch institution. Famous for their lemon ricotta pancakes, jams, and eggs benedict. Right at the park entrance.',
              meta: '💰 $$$ · 📍 40 Central Park S'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Metropolitan Museum of Art',
              description: "One of the world's greatest museums. You could spend days here — focus on the Egyptian Temple of Dendur, the American Wing, and the rooftop garden (open May-October) with stunning Central Park views.",
              details: [
                '🏛️ Suggested donation for NY residents, $30 for visitors',
                '🌿 Rooftop Garden opens in May — cocktails with skyline views',
                '⏱️ Budget 2-3 hours minimum'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Times Square & Broadway',
              description: "Love it or hate it, Times Square is a must-see. Walk through the neon canyon, then catch a Broadway show if you're up for it. Even just people-watching is entertainment.",
              details: [
                '🎭 TKTS booth in Times Square — discounted same-day Broadway tickets',
                '💡 Most spectacular after dark — the lights are overwhelming',
                '📸 Red Steps viewing platform at the TKTS booth'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Joe\'s Pizza',
              description: 'The quintessential NYC slice. No-frills, cash-only, perfect thin-crust pizza. A New York rite of passage.',
              meta: '💰 $ · 📍 7 Carmine St, Greenwich Village (original location)'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7736, lng: -73.9712, label: 'Central Park - Bethesda Fountain', num: 1, cat: 'attraction', desc: 'Iconic fountain in the heart of the park' },
        { lat: 40.7794, lng: -73.9632, label: 'Metropolitan Museum of Art', num: 2, cat: 'attraction', desc: "One of the world's greatest art museums" },
        { lat: 40.7580, lng: -73.9855, label: 'Times Square', num: 3, cat: 'attraction', desc: 'The neon heart of Manhattan' },
        { lat: 40.7641, lng: -73.9858, label: 'TKTS Booth', num: 4, cat: 'attraction', desc: 'Discounted same-day Broadway tickets' },
        { lat: 40.7306, lng: -74.0021, label: "Joe's Pizza", num: 5, cat: 'food', desc: 'NYC pizza institution' }
      ]
    },
    {
      num: 8,
      date: '2026-05-04',
      neighborhoods: 'Chelsea · Meatpacking · West Village',
      title: 'The High Line, Chelsea Market & West Village',
      description: "Explore NYC's trendiest neighborhoods. Walk the High Line elevated park, eat through Chelsea Market, and get lost in the charming streets of the West Village.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The High Line',
              description: "Walk this elevated park built on a former railway line from the Meatpacking District up through Chelsea. Art installations, gardens, and incredible views of the Hudson River and the city. Best experienced before the crowds.",
              details: [
                '🌿 1.45 miles, about 45 min to walk the full length',
                '🎨 Rotating art installations along the way',
                '📸 Great views of the Hudson and the Whitney Museum'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Chelsea Market',
              description: "Incredible food hall in a former Nabisco factory. Browse artisan vendors, grab tacos from Los Tacos No. 1, fresh lobster from The Lobster Place, or dumplings from Very Fresh Noodles.",
              details: [
                '🌮 Los Tacos No. 1 — arguably the best tacos in NYC',
                '🦞 The Lobster Place — fresh seafood market and restaurant',
                '🍩 Doughnuttery — mini doughnuts, freshly made'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Lunch',
              name: 'Los Tacos No. 1',
              description: 'Small stand inside Chelsea Market with incredible al pastor, carne asada, and chicken tacos. Always a line, always worth it.',
              meta: '💰 $ · 📍 Chelsea Market, 75 9th Ave'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'West Village Stroll',
              description: "The West Village is NYC at its most charming — tree-lined streets, brownstones, jazz clubs, and some of the city's best restaurants. Wander Bleecker Street and Perry Street for the quintessential New York vibe.",
              details: [
                '🎵 Village Vanguard — legendary jazz club (if you can get tickets)',
                '🏡 Perry Street — the Carrie Bradshaw stoop from Sex and the City',
                '📚 Three Lives & Company — beautiful independent bookshop'
              ]
            }
          ],
          meals: [
            {
              type: '🍝 Dinner',
              name: 'L\'Artusi',
              description: 'Upscale-casual Italian in the West Village. Seasonal pasta, incredible wine list, and a sophisticated but relaxed atmosphere. Great for a group dinner.',
              meta: '💰 $$$ · 📍 228 W 10th St, West Village · Reserve ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7480, lng: -74.0048, label: 'The High Line', num: 1, cat: 'attraction', desc: 'Elevated park on a former railway' },
        { lat: 40.7425, lng: -74.0060, label: 'Chelsea Market', num: 2, cat: 'food', desc: 'Incredible food hall in a former factory' },
        { lat: 40.7339, lng: -74.0025, label: 'West Village', num: 3, cat: 'attraction', desc: 'Charming streets, brownstones, and jazz' },
        { lat: 40.7425, lng: -74.0060, label: 'Los Tacos No. 1', num: 4, cat: 'food', desc: 'Best tacos in NYC' },
        { lat: 40.7334, lng: -74.0023, label: "L'Artusi", num: 5, cat: 'food', desc: 'Seasonal Italian in the West Village' }
      ]
    },
    {
      num: 9,
      date: '2026-05-05',
      neighborhoods: 'Williamsburg · Bushwick · East Village',
      title: 'Brooklyn Cool — Williamsburg & the East Village',
      description: "Cross into Brooklyn for vintage shopping, street art, and incredible food in Williamsburg and Bushwick. Return to the East Village for one of NYC's best dinner neighborhoods.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Williamsburg, Brooklyn',
              description: "Brooklyn's creative epicenter — vintage shops, street art, waterfront parks with Manhattan skyline views, and some of the best brunch spots in the city. Start at the Bedford Avenue L stop and wander.",
              details: [
                '🎨 Street art murals throughout Williamsburg and neighboring Bushwick',
                '🛍️ Vintage shops on Bedford Avenue — Buffalo Exchange, Beacon\'s Closet',
                '🌊 Domino Park — waterfront views of the Manhattan skyline'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Sunday in Brooklyn',
              description: 'Famous for their malted pancakes with hazelnut maple praline. One of NYC\'s best brunch spots with a beautiful open kitchen.',
              meta: '💰 $$$ · 📍 348 Wythe Ave, Williamsburg'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Smorgasburg or Brooklyn Brewery',
              description: "If it's a Saturday, hit Smorgasburg — the famous outdoor food market with 100+ vendors. Otherwise, tour the Brooklyn Brewery, browse the Artists & Fleas market, or walk to Bushwick for street art.",
              details: [
                '🍔 Smorgasburg — Saturdays at Williamsburg waterfront (April-October)',
                '🍺 Brooklyn Brewery — tours and tastings',
                '🖌️ Bushwick Collective — outdoor street art gallery'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'East Village Bar Hop & Dinner',
              description: "Head back to Manhattan's East Village — NYC's most eclectic nightlife neighborhood. Dive bars, izakayas, and incredible cheap eats.",
              details: [
                '🍶 Decibel — underground sake bar',
                '🍛 Curry Row (E 6th St) for cheap, fun Indian food',
                '🍺 McSorley\'s Old Ale House — NYC\'s oldest bar (1854)'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Veselka',
              description: 'Iconic 24-hour Ukrainian diner in the East Village. Pierogies, borscht, and kielbasa in a bustling, colorful setting. A New York institution since 1954.',
              meta: '💰 $$ · 📍 144 2nd Ave, East Village'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7142, lng: -73.9614, label: 'Williamsburg', num: 1, cat: 'attraction', desc: 'Brooklyn\'s creative epicenter' },
        { lat: 40.7114, lng: -73.9662, label: 'Domino Park', num: 2, cat: 'attraction', desc: 'Waterfront park with Manhattan skyline views' },
        { lat: 40.7218, lng: -73.9579, label: 'Sunday in Brooklyn', num: 3, cat: 'food', desc: 'Famous brunch with malted pancakes' },
        { lat: 40.7291, lng: -73.9876, label: 'East Village', num: 4, cat: 'attraction', desc: 'Eclectic nightlife and cheap eats' },
        { lat: 40.7290, lng: -73.9870, label: 'Veselka', num: 5, cat: 'food', desc: 'Iconic Ukrainian diner since 1954' }
      ]
    },
    {
      num: 10,
      date: '2026-05-06',
      neighborhoods: 'Statue of Liberty · Ellis Island · Financial District',
      title: 'Lady Liberty, Wall Street & Little Italy',
      description: "Visit the Statue of Liberty and Ellis Island — essential Americana. Then walk through the Financial District, past the 9/11 Memorial, and end with dinner in Little Italy.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Statue of Liberty & Ellis Island',
              description: "Take the first ferry from Battery Park to Liberty Island. Walk around the base of the statue (pedestal access requires advance booking), then hop to Ellis Island to explore the Immigration Museum — incredibly moving if your family has an immigration story.",
              details: [
                '🗽 Book ferry tickets in advance at statuecruises.com',
                '🏛️ Ellis Island Immigration Museum — free with ferry ticket',
                '⏰ First ferry is 8:30am — go early to avoid crowds',
                '⏱️ Budget 3-4 hours for both islands'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '9/11 Memorial & Museum',
              description: "The reflecting pools where the Twin Towers stood are deeply moving. The memorial is free and open-air. The museum beneath tells the full story — allow 2 hours and bring tissues.",
              details: [
                '💧 The reflecting pools are free to visit anytime',
                '🏛️ Museum tickets: ~$26/adult, book online',
                '🌳 The Survivor Tree — a pear tree that survived the attacks'
              ]
            }
          ],
          meals: [
            {
              type: '🥯 Lunch',
              name: 'Russ & Daughters Cafe',
              description: 'Classic NYC Jewish deli — bagels, lox, smoked fish, and egg creams. An institution since 1914, now with a sit-down café on the Lower East Side.',
              meta: '💰 $$ · 📍 127 Orchard St, Lower East Side'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍝 Dinner',
              name: 'Rubirosa',
              description: 'Thin-crust pizza and homemade pasta on Mulberry Street. The tie-dye vodka pizza is legendary. Casual, fun, and always packed — a true NYC Italian gem.',
              meta: '💰 $$ · 📍 235 Mulberry St, Nolita'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.6892, lng: -74.0445, label: 'Statue of Liberty', num: 1, cat: 'attraction', desc: 'Iconic symbol of freedom and immigration' },
        { lat: 40.6995, lng: -74.0399, label: 'Ellis Island', num: 2, cat: 'attraction', desc: 'Immigration museum — deeply moving history' },
        { lat: 40.7115, lng: -74.0134, label: '9/11 Memorial', num: 3, cat: 'attraction', desc: 'Reflecting pools and museum at Ground Zero' },
        { lat: 40.7188, lng: -73.9882, label: 'Russ & Daughters', num: 4, cat: 'food', desc: 'Classic NYC Jewish deli since 1914' },
        { lat: 40.7233, lng: -73.9960, label: 'Rubirosa', num: 5, cat: 'food', desc: 'Legendary tie-dye vodka pizza' }
      ]
    },
    {
      num: 11,
      date: '2026-05-07',
      neighborhoods: 'Upper West Side · Harlem · Washington Heights',
      title: 'Uptown Culture — Harlem, Gospel & Tacos',
      description: "Explore upper Manhattan — the cultural richness of Harlem, soul food, and if it's Sunday, a gospel brunch. End the NYC chapter with an incredible meal before heading to New Haven tomorrow.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Harlem Cultural Walk',
              description: "Harlem is the heart of African American culture. Walk along 125th Street past the Apollo Theater, stop by the Studio Museum, and soak in the neighborhood's vibrant energy and history.",
              details: [
                '🎤 Apollo Theater — where legends from Ella Fitzgerald to Lauryn Hill were discovered',
                '🎨 Studio Museum in Harlem — Black art and culture',
                '📸 Sylvia\'s Restaurant — Harlem institution since 1962'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Brunch',
              name: 'Red Rooster Harlem',
              description: 'Chef Marcus Samuelsson\'s acclaimed restaurant. Southern comfort food meets global flavors — fried chicken, cornbread, and a lively brunch scene with live music.',
              meta: '💰 $$$ · 📍 310 Lenox Ave, Harlem'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'American Museum of Natural History',
              description: "One of the world's great museums — the dinosaur halls, the whale room, and the Rose Center for Earth and Space are awe-inspiring. Great for the whole group.",
              details: [
                '🦕 4th floor dinosaur halls are the highlights',
                '🐋 Blue whale room is breathtaking',
                '🌌 Rose Center Planetarium — Hayden Sphere show'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Last Night in NYC',
              description: "Make your last NYC dinner count. Head to a neighborhood you haven't explored yet, or revisit a favorite. Tomorrow you're New Haven-bound.",
              details: [
                '📦 Pack up tonight — New Haven is a quick trip tomorrow',
                '🗽 One last walk through your favorite NYC neighborhood'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ippudo',
              description: 'World-famous Japanese ramen chain — the Shiromaru Classic (tonkotsu) is silky, rich, and perfect. Always busy, always worth it.',
              meta: '💰 $$ · 📍 65 4th Ave, East Village'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.8101, lng: -73.9504, label: 'Apollo Theater', num: 1, cat: 'attraction', desc: 'Legendary Harlem performance venue' },
        { lat: 40.8051, lng: -73.9543, label: 'Red Rooster Harlem', num: 2, cat: 'food', desc: 'Marcus Samuelsson\'s acclaimed restaurant' },
        { lat: 40.7813, lng: -73.9740, label: 'Natural History Museum', num: 3, cat: 'attraction', desc: 'Dinosaurs, whales, and the planetarium' },
        { lat: 40.7311, lng: -73.9897, label: 'Ippudo', num: 4, cat: 'food', desc: 'World-famous tonkotsu ramen' }
      ]
    },

    // ===== NEW HAVEN: May 8 =====
    {
      num: 12,
      date: '2026-05-08',
      neighborhoods: 'New Haven Green · Yale · Wooster Square',
      title: '🎓 New Haven — Brother\'s Graduation & Legendary Pizza',
      description: "Drive to New Haven for your brother's graduation, explore the beautiful Yale campus, and eat what many consider the best pizza in America.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive NYC → New Haven',
              description: 'Quick 90-minute drive from NYC to New Haven via I-95. Arrive in time to settle in and prep for the ceremony.',
              details: [
                '🚗 ~90 minutes via I-95 N',
                '💡 Park near the university — check ceremony parking instructions',
                '👔 Dress semi-formal for the graduation'
              ]
            },
            {
              title: '🎓 Brother\'s Graduation Ceremony',
              description: "The big one! Your brother's graduation day. Arrive early, find great seats, and celebrate this incredible milestone.",
              details: [
                '🎓 Check the university website for exact ceremony time and location',
                '📸 Plan group photos at iconic campus spots afterwards',
                '🎉 This deserves a major celebration dinner'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yale University Campus Walk',
              description: "After the ceremony, explore Yale's stunning Gothic campus. The Beinecke Rare Book Library (with its translucent marble walls) and the Yale University Art Gallery are both free and extraordinary.",
              details: [
                '📚 Beinecke Library — the marble walls glow with natural light',
                '🎨 Yale University Art Gallery — free, world-class collection',
                '🏛️ Gothic architecture everywhere — feels like Hogwarts'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'New Haven Pizza Pilgrimage',
              description: "New Haven-style pizza (apizza) is coal-fired, thin, charred, and legendary. Frank Pepe's and Sally's Apizza have been battling for the crown since the 1930s. You must try both.",
              details: [
                '🍕 Frank Pepe\'s — the Original Tomato Pie and White Clam pie are iconic',
                '🍕 Sally\'s Apizza — same street, equally legendary',
                '🔥 Both are on Wooster Street — walk between them',
                '⏰ Lines can be long — go early or be patient'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Celebration Dinner',
              name: 'Frank Pepe Pizzeria Napoletana',
              description: 'The birthplace of New Haven-style apizza (since 1925). The White Clam pizza is a national treasure — fresh littleneck clams, garlic, olive oil, no mozzarella. Life-changing.',
              meta: '💰 $$ · 📍 157 Wooster St, New Haven'
            }
          ],
          tips: [
            { type: 'tip', text: 'If you can handle two pizza stops, walk next door to Sally\'s Apizza for a second pie. The rivalry is real and both are extraordinary.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3083, lng: -72.9279, label: 'New Haven Green', num: 1, cat: 'attraction', desc: 'Historic center of New Haven' },
        { lat: 41.3111, lng: -72.9267, label: 'Yale University', num: 2, cat: 'attraction', desc: 'Stunning Gothic campus' },
        { lat: 41.3117, lng: -72.9300, label: 'Beinecke Library', num: 3, cat: 'attraction', desc: 'Rare book library with translucent marble walls' },
        { lat: 41.3025, lng: -72.9198, label: "Frank Pepe's", num: 4, cat: 'food', desc: 'Legendary coal-fired pizza since 1925' },
        { lat: 41.3023, lng: -72.9194, label: "Sally's Apizza", num: 5, cat: 'food', desc: 'Rival legendary apizza — equally iconic' }
      ]
    },

    // ===== LAS VEGAS: May 9-10 =====
    {
      num: 13,
      date: '2026-05-09',
      neighborhoods: 'The Strip · Fremont Street · Arts District',
      title: 'Fly to Las Vegas — Neon Nights',
      description: "Catch a flight to Las Vegas and arrive in the desert. Check in, walk the Strip, and experience the sensory overload of Vegas at night. This isn't about gambling — it's about the spectacle.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Flight: New Haven Area → Las Vegas',
              description: 'Fly from a nearby airport (JFK, Newark, or Hartford) to Las Vegas McCarran International. Budget for 5-6 hours of travel including flight time.',
              details: [
                '✈️ Fly from JFK/EWR/BDL → Las Vegas (LAS), ~5 hours',
                '🚗 You\'ll need a rental car in Vegas for the Grand Canyon drive',
                '💡 Pick up the rental car at the airport'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Las Vegas Strip Walk',
              description: "Walk the Strip from the Bellagio fountains to the Venetian. Even if you don't gamble, the hotels are insane — the Bellagio conservatory, the Venetian canals, and the Cosmopolitan's chandelier bar are all free to explore.",
              details: [
                '⛲ Bellagio Fountains — free show every 15-30 min',
                '🌸 Bellagio Conservatory — incredible seasonal botanical display (free)',
                '🏛️ The Venetian — indoor canals and gondola rides',
                '🍸 Chandelier Bar at The Cosmopolitan — three-story cocktail bar'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Fremont Street Experience',
              description: "Old Vegas! The Fremont Street Experience is a covered pedestrian mall with a massive LED canopy, live music, street performers, and vintage casinos. It's grittier and more fun than the Strip.",
              details: [
                '💡 The Viva Vision LED canopy is 1,500 feet long',
                '🎰 Vintage casinos — Golden Nugget, Binion\'s, El Cortez',
                '🍺 More affordable drinks and food than the Strip'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tacos El Gordo',
              description: 'Tijuana-style street tacos on the Strip. The adobada (al pastor) is carved from a massive spit and loaded into fresh tortillas. The best cheap eat in Vegas.',
              meta: '💰 $ · 📍 3049 Las Vegas Blvd S'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1126, lng: -115.1767, label: 'Bellagio Fountains', num: 1, cat: 'attraction', desc: 'Iconic water show on the Strip' },
        { lat: 36.1211, lng: -115.1690, label: 'The Venetian', num: 2, cat: 'attraction', desc: 'Indoor canals and gondolas' },
        { lat: 36.1699, lng: -115.1398, label: 'Fremont Street', num: 3, cat: 'attraction', desc: 'Old Vegas — LED canopy and vintage casinos' },
        { lat: 36.1214, lng: -115.1689, label: 'Tacos El Gordo', num: 4, cat: 'food', desc: 'Best Tijuana-style street tacos in Vegas' }
      ]
    },
    {
      num: 14,
      date: '2026-05-10',
      neighborhoods: 'Las Vegas · Route 66 · Grand Canyon approach',
      title: 'Vegas Morning → Drive to the Grand Canyon',
      description: "One more Vegas morning, then hit the road toward one of the world's great natural wonders. The drive through the desert is stunning — red rocks, Joshua trees, and wide-open sky.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Vegas Brunch & Departure',
              description: "Fuel up with a big Vegas brunch before the road trip. The Arts District (18b) has great casual spots if you want to skip the Strip tourist traps.",
              details: [
                '🎨 18b Arts District — murals, galleries, and coffee shops',
                '☕ PublicUs — excellent specialty coffee and brunch in the Arts District'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Mon Ami Gabi',
              description: 'French bistro with a patio right on the Strip, looking out at the Bellagio fountains. Classic eggs benedict, steak frites, and people-watching.',
              meta: '💰 $$$ · 📍 Paris Las Vegas, 3655 Las Vegas Blvd S'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Drive: Las Vegas → Grand Canyon South Rim',
              description: 'Hit the road for the ~4.5-hour drive to the Grand Canyon South Rim. The desert scenery is gorgeous — consider a stop in Kingman or Williams along old Route 66.',
              details: [
                '🚗 ~275 miles via US-93 S and I-40 E, about 4-4.5 hours',
                '🛣️ Williams, AZ — "Gateway to the Grand Canyon" has Route 66 charm',
                '⛽ Fill up in Williams — limited services closer to the canyon',
                '🌄 Arrive by late afternoon for your first rim views'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'First Sunset at the Grand Canyon',
              description: "Check into your lodging near the South Rim and head straight to Mather Point or Yavapai Point for sunset. The canyon transforms minute by minute as the light changes — this first view will stop you in your tracks.",
              details: [
                '🌅 Mather Point — most accessible sunset viewpoint',
                '📸 The canyon is 277 miles long, 18 miles wide, and a mile deep',
                '🏨 Stay at Tusayan (just outside the park) or in-park lodges (book far ahead)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'El Tovar Dining Room',
              description: 'Historic dining room right on the South Rim inside the iconic El Tovar Hotel. The views are extraordinary and the food is surprisingly good for a national park.',
              meta: '💰 $$$ · 📍 El Tovar Hotel, Grand Canyon South Rim · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1162, lng: -115.1745, label: 'Mon Ami Gabi', num: 1, cat: 'food', desc: 'French bistro with Bellagio fountain views' },
        { lat: 35.2494, lng: -113.1944, label: 'Kingman, AZ', num: 2, cat: 'attraction', desc: 'Route 66 pit stop' },
        { lat: 36.0544, lng: -112.1401, label: 'Grand Canyon South Rim', num: 3, cat: 'attraction', desc: 'One of the seven natural wonders' },
        { lat: 36.0580, lng: -112.1071, label: 'Mather Point', num: 4, cat: 'attraction', desc: 'Classic Grand Canyon viewpoint' },
        { lat: 36.0545, lng: -112.1170, label: 'El Tovar', num: 5, cat: 'food', desc: 'Historic dining on the canyon rim' }
      ]
    },
    {
      num: 15,
      date: '2026-05-11',
      neighborhoods: 'Grand Canyon South Rim · Bright Angel Trail',
      title: 'Grand Canyon — Rim Trail & Bright Angel',
      description: "A full day at the Grand Canyon. Hike a portion of the Bright Angel Trail, walk the Rim Trail, ride the free shuttle to viewpoints, and watch the canyon change colors throughout the day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise at Yavapai Point',
              description: "Set your alarm for early — Grand Canyon sunrise is one of the most spectacular things you'll ever see. Yavapai Point offers panoramic views with interpretive displays about the canyon's geology.",
              details: [
                '🌅 Sunrise around 5:30am in mid-May — arrive 20 min early',
                '📸 Yavapai Geology Museum explains the billion-year-old rock layers',
                '☕ Grab coffee and snacks before — services open early in the park'
              ]
            },
            {
              title: 'Bright Angel Trail Hike',
              description: "Hike down the Bright Angel Trail — the most popular trail into the canyon. Go as far as you're comfortable: the 1.5-mile Resthouse (3 miles round trip) is a great turnaround for most groups. The trail is steep but well-maintained.",
              details: [
                '🥾 1.5-Mile Resthouse: 3 miles RT, ~1,100 ft elevation change',
                '💧 Bring LOTS of water — at least 1 liter per person per hour',
                '⚠️ Do NOT attempt to hike to the river and back in one day',
                '🌡️ Canyon is significantly hotter below the rim — start early'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rim Trail & Shuttle Viewpoints',
              description: "The Rim Trail is a mostly flat, paved path along the canyon edge — perfect for a leisurely post-hike walk. Take the free Hermit Road shuttle to viewpoints like Hopi Point, Mohave Point, and Hermit's Rest (designed by Mary Colter).",
              details: [
                '🚌 Free Hermit Road shuttle operates March-November',
                '📸 Hopi Point — best panoramic views on the South Rim',
                '🏛️ Hermit\'s Rest — stone rest house designed by architect Mary Colter (1914)',
                '🦅 Watch for California condors soaring over the canyon'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Bright Angel Lodge Café',
              description: 'Casual counter-service spot right on the rim. Burgers, sandwiches, and soup — nothing fancy, but the view makes everything taste better.',
              meta: '💰 $ · 📍 Bright Angel Lodge, South Rim'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Canyon Sunset & Stargazing',
              description: "The Grand Canyon is a certified International Dark Sky Park. After sunset, stay for stargazing — on a clear night, the Milky Way stretches across the sky in stunning detail. The park sometimes offers ranger-led star programs.",
              details: [
                '🌌 The Grand Canyon has some of the darkest skies in the country',
                '🔭 Check for ranger-led astronomy programs at the visitor center',
                '🌅 Hopi Point is the #1 sunset spot — arrive 30 min early'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Arizona Room',
              description: 'Casual steakhouse at Bright Angel Lodge with rim views through picture windows. Steaks, ribs, and local trout. No reservations — first come, first served.',
              meta: '💰 $$ · 📍 Bright Angel Lodge, South Rim'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.0585, lng: -112.1146, label: 'Yavapai Point', num: 1, cat: 'attraction', desc: 'Panoramic sunrise viewpoint' },
        { lat: 36.0573, lng: -112.1435, label: 'Bright Angel Trailhead', num: 2, cat: 'attraction', desc: 'Most popular trail into the canyon' },
        { lat: 36.0626, lng: -112.1552, label: 'Hopi Point', num: 3, cat: 'attraction', desc: 'Best panoramic views on the South Rim' },
        { lat: 36.0624, lng: -112.2143, label: "Hermit's Rest", num: 4, cat: 'attraction', desc: 'Historic Mary Colter rest house' },
        { lat: 36.0567, lng: -112.1405, label: 'Bright Angel Lodge', num: 5, cat: 'food', desc: 'Casual dining with canyon views' }
      ]
    },
    {
      num: 16,
      date: '2026-05-12',
      neighborhoods: 'Grand Canyon East Rim · Desert View',
      title: 'Grand Canyon East Rim & Desert View',
      description: "Explore the eastern section of the South Rim via Desert View Drive — less crowded, equally stunning. Visit the Watchtower at Desert View for 360° panoramas before departing.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Desert View Drive',
              description: "Drive the 25-mile Desert View Drive east along the rim, stopping at viewpoints along the way. Each offers a different perspective — you'll see the canyon widen, the Colorado River appear, and the Painted Desert in the distance.",
              details: [
                '🚗 25 miles, about 1-2 hours with stops',
                '📸 Grandview Point — one of the most dramatic viewpoints',
                '🏜️ Lipan Point — see the Colorado River far below'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Desert View Watchtower',
              description: "Mary Colter's masterpiece — a 70-foot stone tower inspired by Ancestral Puebloan watchtowers. Climb to the top for 360° views spanning the canyon, the Painted Desert, and on clear days, the Navajo Nation. The interior murals by Hopi artist Fred Kabotie are beautiful.",
              details: [
                '🏛️ Built in 1932, inspired by ancestral Puebloan architecture',
                '🎨 Interior murals by Hopi artist Fred Kabotie',
                '📸 360° views from the top — bring a wide-angle lens'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Desert View Trading Post',
              description: 'Simple snacks and sandwiches at the Desert View area. Stock up on water and snacks for the afternoon drive.',
              meta: '💰 $ · 📍 Desert View, Grand Canyon'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Last Evening at the Canyon',
              description: "Enjoy one more sunset from the rim before departing tomorrow. Reflect on the scale of this place — it's been carved over 6 million years and reveals 2 billion years of Earth's history.",
              details: [
                '🌅 Pick a new sunset spot — Yavapai or Mather for variety',
                '📝 Tomorrow: long drive to Salt Lake City'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'El Tovar Dining Room',
              description: 'One more dinner at this historic spot. Try something different from the menu — the elk or bison options are uniquely southwestern.',
              meta: '💰 $$$ · 📍 El Tovar Hotel, South Rim'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.0004, lng: -111.8259, label: 'Desert View Watchtower', num: 1, cat: 'attraction', desc: 'Mary Colter\'s 70-foot stone watchtower' },
        { lat: 36.0004, lng: -112.0478, label: 'Grandview Point', num: 2, cat: 'attraction', desc: 'Dramatic canyon viewpoint' },
        { lat: 36.0233, lng: -111.8538, label: 'Lipan Point', num: 3, cat: 'attraction', desc: 'See the Colorado River far below' },
        { lat: 36.0545, lng: -112.1170, label: 'El Tovar', num: 4, cat: 'food', desc: 'Historic canyon-rim dining' }
      ]
    },
    {
      num: 17,
      date: '2026-05-13',
      neighborhoods: 'Northern Arizona · Page · Lake Powell area',
      title: 'Grand Canyon → Northward — Road Trip Day',
      description: "Begin the long drive northward toward Salt Lake City. Break up the journey with stops at scenic spots in northern Arizona and southern Utah. This is a driving day, but the scenery is world-class.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive North: Grand Canyon → Page, AZ',
              description: 'Head north from the Grand Canyon through the Navajo Nation toward Page, Arizona (~2.5 hours). The landscape shifts from pine forests to red desert.',
              details: [
                '🚗 ~140 miles, about 2.5 hours to Page',
                '🏜️ Drive through the Navajo Nation — stunning red mesas',
                '⛽ Fill up at Cameron Trading Post — a good rest stop'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Horseshoe Bend (Optional Stop)',
              description: "If time allows, stop at Horseshoe Bend — one of the most photographed spots in the American Southwest. A short 1.5-mile round trip walk from the parking lot leads to a jaw-dropping 1,000-foot drop overlooking the Colorado River's iconic horseshoe curve.",
              details: [
                '📸 1.5 miles round trip, easy walk',
                '⚠️ No guardrails at the edge — be careful!',
                '💰 $10 parking fee'
              ]
            },
            {
              title: 'Continue to Kanab or Cedar City',
              description: 'Continue north through southern Utah. The drive through Vermilion Cliffs and across the Colorado Plateau is stunning. Stop in Kanab for a late lunch — it\'s a charming little town known as "Little Hollywood."',
              details: [
                '🚗 Page to Kanab: ~75 miles, ~1.5 hours',
                '🎬 Kanab was used as a filming location for many westerns',
                '🚗 Kanab to Cedar City: ~125 miles, ~2 hours'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Rocking V Cafe',
              description: 'Surprisingly great café in tiny Kanab, UT. Eclectic menu with fresh, creative dishes — a welcome oasis on this desert drive.',
              meta: '💰 $$ · 📍 97 W Center St, Kanab, UT'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Overnight in Cedar City or St. George',
              description: 'Stop for the night in Cedar City or St. George, Utah. Both are comfortable mid-size towns with good food options. You\'ll continue to Salt Lake City tomorrow.',
              details: [
                '🏨 Cedar City or St. George — both have good hotel options',
                '🚗 About 3-4 hours remaining to SLC tomorrow',
                '🌄 The red rock scenery continues into southern Utah'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Centro Woodfired Pizzeria',
              description: 'Excellent wood-fired pizza in Cedar City. Surprising quality for a small town — great way to end a long driving day.',
              meta: '💰 $$ · 📍 50 W University Blvd, Cedar City, UT'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.8791, lng: -111.5104, label: 'Horseshoe Bend', num: 1, cat: 'attraction', desc: 'Iconic Colorado River overlook' },
        { lat: 37.0475, lng: -111.5326, label: 'Page, AZ', num: 2, cat: 'attraction', desc: 'Gateway to Lake Powell and Horseshoe Bend' },
        { lat: 37.0476, lng: -112.5263, label: 'Kanab, UT', num: 3, cat: 'attraction', desc: '"Little Hollywood" — charming desert town' },
        { lat: 37.6775, lng: -113.0619, label: 'Cedar City, UT', num: 4, cat: 'attraction', desc: 'Overnight stop in southern Utah' }
      ]
    },
    {
      num: 18,
      date: '2026-05-14',
      neighborhoods: 'Salt Lake City · Temple Square · Downtown',
      title: 'Arrive Salt Lake City — Mountain Views & Local Eats',
      description: "Complete the drive to Salt Lake City, nestled against the stunning Wasatch Mountains. Explore Temple Square, walk through downtown, and discover SLC's surprisingly vibrant food scene.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Salt Lake City',
              description: 'Finish the drive from Cedar City/St. George to Salt Lake City (~3-4 hours). The I-15 corridor through Utah is scenic, passing through Provo and along Utah Lake.',
              details: [
                '🚗 ~250 miles from Cedar City, about 3.5 hours',
                '🏔️ The Wasatch Mountains come into view as you approach SLC',
                '🌿 May weather in SLC is pleasant — 60-70°F'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Temple Square & Downtown SLC',
              description: 'Visit the iconic Temple Square — the spiritual center of The Church of Jesus Christ of Latter-day Saints. Even if you\'re not religious, the architecture and gardens are beautiful. The surrounding downtown has great restaurants and craft breweries.',
              details: [
                '🏛️ Salt Lake Temple — recently renovated, stunning architecture',
                '🌸 Temple Square gardens — beautifully maintained',
                '🍺 SLC has a surprisingly good craft beer scene'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Red Iguana',
              description: 'Legendary Mexican restaurant in SLC — the mole sauces are extraordinary (they have 7 different moles!). Always busy, always worth the wait.',
              meta: '💰 $$ · 📍 736 W North Temple, SLC'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Relax & Prep for Yellowstone',
              description: 'Take it easy tonight — you\'ve been driving for two days. Rest up for the Yellowstone adventure starting tomorrow. Check the park\'s road status online (some roads may still be opening in mid-May).',
              details: [
                '🗺️ Check nps.gov/yell for road status and closures',
                '🧥 Pack warm layers — Yellowstone will be cold!',
                '📱 Download the NPS Yellowstone app for offline maps'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Copper Onion',
              description: 'Farm-to-table New American restaurant in downtown SLC. Excellent seasonal dishes, craft cocktails, and a warm, buzzy atmosphere.',
              meta: '💰 $$$ · 📍 111 E Broadway, SLC'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7608, lng: -111.8910, label: 'Temple Square', num: 1, cat: 'attraction', desc: 'Iconic LDS temple and gardens' },
        { lat: 40.7721, lng: -111.9103, label: 'Red Iguana', num: 2, cat: 'food', desc: 'Legendary mole — 7 different varieties' },
        { lat: 40.7592, lng: -111.8833, label: 'Copper Onion', num: 3, cat: 'food', desc: 'Farm-to-table New American' }
      ]
    },

    // ===== YELLOWSTONE: May 15-18 =====
    {
      num: 19,
      date: '2026-05-15',
      neighborhoods: 'West Yellowstone · Old Faithful · Upper Geyser Basin',
      title: 'Yellowstone Day 1 — Old Faithful & Geyser Basin',
      description: "Drive from SLC to Yellowstone's west entrance (~5 hours) and head straight to Old Faithful. Watch the world's most famous geyser erupt, then explore the Upper Geyser Basin — the densest concentration of geysers on Earth.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive: SLC → West Yellowstone',
              description: 'Head north from Salt Lake City to West Yellowstone, Montana (~5 hours). The drive goes through Idaho and along the Snake River — beautiful terrain.',
              details: [
                '🚗 ~320 miles, about 5 hours via I-15 N and US-20 E',
                '⛽ Fill up before entering the park — gas is limited and expensive inside',
                '🏔️ You\'ll drive through Island Park, ID — stunning volcanic plateau'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Old Faithful',
              description: "The world's most famous geyser erupts roughly every 90 minutes, shooting 130-180 feet into the air. Check the predicted eruption times at the visitor center and claim a seat on the viewing boardwalk. It never gets old.",
              details: [
                '💨 Erupts every ~90 minutes — check the prediction board',
                '📸 Sit on the side where the wind is blowing AWAY from you',
                '🏛️ Old Faithful Inn — the world\'s largest log structure, worth exploring'
              ]
            },
            {
              title: 'Upper Geyser Basin Boardwalk',
              description: 'Walk the boardwalks around the Upper Geyser Basin — home to the highest concentration of geysers in the world. Morning Glory Pool, Chromatic Pool, and dozens of smaller geysers surround you.',
              details: [
                '🌈 Morning Glory Pool — stunning blue and orange hot spring',
                '♨️ Castle Geyser, Grand Geyser, and Riverside Geyser are all spectacular',
                '🚶 The full loop is about 3 miles on boardwalks'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Old Faithful Inn Dining Room',
              description: 'Dine inside the historic Old Faithful Inn — massive log-and-stone architecture with a soaring lobby. Casual and group-friendly.',
              meta: '💰 $$ · 📍 Old Faithful Village · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'Mid-May is still early season in Yellowstone. Some roads and facilities may be closed. Check nps.gov/yell for the latest updates. Expect wildlife on the roads — bison jams are real!' }
          ]
        }
      ],
      mapPins: [
        { lat: 44.4605, lng: -110.8281, label: 'Old Faithful', num: 1, cat: 'attraction', desc: "World's most famous geyser" },
        { lat: 44.4684, lng: -110.8442, label: 'Morning Glory Pool', num: 2, cat: 'attraction', desc: 'Stunning hot spring in the Upper Geyser Basin' },
        { lat: 44.4600, lng: -110.8310, label: 'Old Faithful Inn', num: 3, cat: 'food', desc: "World's largest log structure and historic dining" }
      ]
    },
    {
      num: 20,
      date: '2026-05-16',
      neighborhoods: 'Grand Prismatic · Midway Geyser Basin · Firehole River',
      title: 'Yellowstone Day 2 — Grand Prismatic & Midway Basin',
      description: "Today is all about color. The Grand Prismatic Spring is Yellowstone's most jaw-dropping feature — a 370-foot-wide rainbow of turquoise, orange, and yellow. Pair it with the Midway Geyser Basin and a scenic drive along the Firehole River.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grand Prismatic Spring',
              description: "The largest hot spring in the US and the third largest in the world. The colors are caused by heat-loving bacteria — the center is too hot for life (sterile blue), while the edges bloom in orange, yellow, and green. Absolutely unreal.",
              details: [
                '🌈 370 feet across — the size of a football field',
                '📸 For the best overhead view, hike the Fairy Falls Trail to the Grand Prismatic Overlook (~1.6 miles round trip)',
                '♨️ The steam can obscure views — early morning or clear days are best',
                '🌡️ Water temperature: ~160°F in the center'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Midway Geyser Basin',
              description: 'The boardwalk loop through Midway Geyser Basin passes Excelsior Geyser Crater (which pumps 4,000 gallons of boiling water per minute into the Firehole River) and of course Grand Prismatic itself.',
              details: [
                '💧 Excelsior Geyser Crater — massive boiling crater',
                '🌊 Watch the turquoise water cascade into the Firehole River',
                '🚶 Short boardwalk loop — about 0.6 miles'
              ]
            },
            {
              title: 'Firehole River Swim',
              description: "One of the only places you can legally swim in Yellowstone! The Firehole Swimming Area is a stretch of the Firehole River warmed by geothermal activity. It's chilly but exhilarating — a truly unique experience.",
              details: [
                '🏊 Firehole Swimming Area — south of Madison Junction',
                '🌡️ Water is warmed by hot springs but still cold — think 70°F',
                '📍 Open seasonally, usually late May (check if open during your visit)'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Canyon Lodge Eatery',
              description: 'Casual cafeteria-style dining with surprisingly good options — bison burgers, BBQ, and salads. Fill up for the afternoon adventures.',
              meta: '💰 $$ · 📍 Canyon Village'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Wildlife Watching at Dusk',
              description: "Yellowstone comes alive at dusk. Drive slowly along the roads near Hayden Valley or Lamar Valley — you might spot bison herds, elk, coyotes, and if you're incredibly lucky, wolves or bears.",
              details: [
                '🦬 Bison are EVERYWHERE — keep your distance (25 yards minimum)',
                '🐺 Lamar Valley is known as the "Serengeti of North America"',
                '🔭 Bring binoculars for wildlife spotting'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'West Yellowstone Restaurants',
              description: 'Head to West Yellowstone town for dinner. Wild West Pizzeria or the Buffalo Bar & Grill are solid casual options after a big day in the park.',
              meta: '💰 $$ · 📍 West Yellowstone, MT'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 44.5251, lng: -110.8381, label: 'Grand Prismatic Spring', num: 1, cat: 'attraction', desc: "Yellowstone's most colorful feature" },
        { lat: 44.5258, lng: -110.8369, label: 'Midway Geyser Basin', num: 2, cat: 'attraction', desc: 'Boardwalk with Excelsior Geyser and Grand Prismatic' },
        { lat: 44.6329, lng: -110.8563, label: 'Firehole Swimming Area', num: 3, cat: 'attraction', desc: 'Geothermally-warmed river swimming' },
        { lat: 44.7336, lng: -110.4967, label: 'Hayden Valley', num: 4, cat: 'attraction', desc: 'Prime wildlife viewing area' }
      ]
    },
    {
      num: 21,
      date: '2026-05-17',
      neighborhoods: 'Yellowstone Lake · Canyon Village · Grand Canyon of the Yellowstone',
      title: 'Yellowstone Day 3 — Canyon, Waterfalls & Yellowstone Lake',
      description: "Explore the Grand Canyon of the Yellowstone — not to be confused with Arizona's! The Lower Falls waterfall is twice the height of Niagara, plunging into a golden-walled canyon. Then visit Yellowstone Lake, the largest high-altitude lake in North America.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grand Canyon of the Yellowstone',
              description: "The Yellowstone River carved this magnificent canyon with yellow, orange, and red walls stretching 20 miles. The Lower Falls — at 308 feet — is the star. View it from Artist Point (south rim) or the more dramatic Uncle Tom's Trail.",
              details: [
                '💧 Lower Falls: 308 feet — twice the height of Niagara Falls',
                '📸 Artist Point — the classic viewpoint, easy walk from parking',
                '🪜 Uncle Tom\'s Trail — 328 steel steps down for a closer view (strenuous!)',
                '🎨 The canyon walls are colored by iron compounds — hence "Yellowstone"'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yellowstone Lake',
              description: "The largest high-altitude lake in North America (7,733 ft). The shore at West Thumb Geyser Basin is surreal — hot springs and geysers right on the lake's edge. In May, the lake may still have ice chunks floating on it.",
              details: [
                '🌊 136 square miles of pristine alpine lake',
                '♨️ West Thumb Geyser Basin — geysers right at the lake\'s edge',
                '❄️ Lake may still have ice in mid-May — hauntingly beautiful',
                '🎣 Cutthroat trout fishing is legendary (catch-and-release)'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Lake Hotel Deli',
              description: 'Casual deli at the historic Lake Hotel. Sandwiches and snacks with views of Yellowstone Lake.',
              meta: '💰 $ · 📍 Lake Village'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Fishing Bridge or Lake',
              description: 'Watch the sun set over Yellowstone Lake. The sky reflects off the water and the mountains glow pink. This is Yellowstone at its most peaceful.',
              details: [
                '🌅 Fishing Bridge area — great sunset views',
                '🦌 Watch for elk and bison near the lake at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Lake Yellowstone Hotel Dining Room',
              description: 'Elegant dining room in the 1891 Lake Yellowstone Hotel. Views over the lake, a varied menu, and historic charm.',
              meta: '💰 $$$ · 📍 Lake Village · Reservations required'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 44.7198, lng: -110.4862, label: 'Artist Point', num: 1, cat: 'attraction', desc: 'Classic viewpoint of the Lower Falls' },
        { lat: 44.7175, lng: -110.5006, label: 'Lower Falls', num: 2, cat: 'attraction', desc: '308-foot waterfall — twice Niagara\'s height' },
        { lat: 44.4164, lng: -110.5718, label: 'West Thumb Geyser Basin', num: 3, cat: 'attraction', desc: 'Geysers right at the edge of Yellowstone Lake' },
        { lat: 44.5528, lng: -110.3968, label: 'Yellowstone Lake', num: 4, cat: 'attraction', desc: 'Largest high-altitude lake in North America' },
        { lat: 44.5528, lng: -110.3950, label: 'Lake Yellowstone Hotel', num: 5, cat: 'food', desc: 'Historic 1891 hotel and elegant dining' }
      ]
    },
    {
      num: 22,
      date: '2026-05-18',
      neighborhoods: 'Mammoth Hot Springs · Lamar Valley',
      title: 'Yellowstone Day 4 — Mammoth, Wildlife & Farewell',
      description: "Last day in Yellowstone! Explore the terraced travertine formations at Mammoth Hot Springs, drive through Lamar Valley for world-class wildlife viewing, then begin heading south toward Salt Lake City.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Mammoth Hot Springs',
              description: 'Unlike the geysers, Mammoth Hot Springs are terraced limestone formations — cascading white and orange travertine that looks like another planet. Walk the boardwalks around the upper and lower terraces.',
              details: [
                '🏔️ Minerva Terrace — the most photogenic formation',
                '🦌 Elk often graze right on the Mammoth village lawn',
                '🏛️ Historic Fort Yellowstone buildings surround the area',
                '📸 The terraces change constantly — what\'s flowing today may be dry tomorrow'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lamar Valley Wildlife Drive',
              description: "Drive through the Lamar Valley — the \"Serengeti of North America.\" This broad, open valley is the best place in the lower 48 to see wolves, bison herds, grizzly bears, and pronghorn. Move slowly, stop at pullouts, and scan with binoculars.",
              details: [
                '🐺 Best wolf-watching spot in the US — dawn and dusk are prime times',
                '🦬 Bison herds can number in the hundreds here',
                '🐻 Grizzly bears are active in May — scan hillsides and meadows',
                '🔭 Bring binoculars or rent a spotting scope'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Mammoth Hot Springs Hotel Dining Room',
              description: 'Casual dining at the Mammoth Hotel. Burgers, salads, and local dishes in a historic setting.',
              meta: '💰 $$ · 📍 Mammoth Hot Springs Village'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Depart Yellowstone → Overnight Stop',
              description: 'Head south out of Yellowstone through Grand Teton National Park (stunning mountain views!) toward Jackson, WY or further south. You\'ll finish the drive to SLC tomorrow.',
              details: [
                '🏔️ Grand Teton views as you exit south — absolutely spectacular',
                '🏘️ Jackson, WY — charming western town, good food and lodging',
                '🚗 Jackson to SLC is about 5 hours — you can split the drive'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Persephone Bakery',
              description: 'Charming French-inspired bakery and café in Jackson, WY. Fresh pastries, seasonal dishes, and excellent coffee. A lovely end to your Yellowstone chapter.',
              meta: '💰 $$ · 📍 145 E Broadway, Jackson, WY'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 44.9685, lng: -110.7043, label: 'Mammoth Hot Springs', num: 1, cat: 'attraction', desc: 'Terraced travertine formations' },
        { lat: 44.8982, lng: -110.2286, label: 'Lamar Valley', num: 2, cat: 'attraction', desc: 'Best wildlife viewing in Yellowstone' },
        { lat: 43.8231, lng: -110.6777, label: 'Grand Teton View', num: 3, cat: 'attraction', desc: 'Spectacular mountain views on the drive south' },
        { lat: 43.4799, lng: -110.7624, label: 'Jackson, WY', num: 4, cat: 'food', desc: 'Charming western town — Persephone Bakery' }
      ]
    },

    // ===== BACK TO SLC: May 19 =====
    {
      num: 23,
      date: '2026-05-19',
      neighborhoods: 'Salt Lake City · Sugar House · 9th & 9th',
      title: 'Back to Salt Lake City — Rest & Recharge',
      description: "Return to Salt Lake City, return the rental car, and enjoy a relaxed day exploring SLC's hip neighborhoods. Sugar House and 9th & 9th have great local shops, cafés, and a chill vibe.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive: Jackson/Teton area → SLC',
              description: 'Complete the drive back to Salt Lake City (~5 hours from Jackson). Drop off the rental car — you won\'t need it in Chicago.',
              details: [
                '🚗 ~280 miles from Jackson, about 5 hours',
                '🚙 Return the rental car at SLC airport or downtown',
                '🛬 Tomorrow: flight to Chicago'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '9th & 9th Neighborhood',
              description: 'One of SLC\'s most walkable, charming neighborhoods. Browse local boutiques, get coffee at The Rose Establishment, and enjoy a slower pace after days of hiking and driving.',
              details: [
                '☕ The Rose Establishment — excellent specialty coffee',
                '🛍️ Local boutiques and vintage shops',
                '🎭 Tower Theatre — beautiful indie cinema'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Stoneground Kitchen',
              description: 'Italian-inspired café in Sugar House. Fresh pastas, paninis, and excellent espresso. Casual and neighborhood-y.',
              meta: '💰 $$ · 📍 2114 S Highland Dr, SLC'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Liberty Park & Dinner',
              description: 'Walk through Liberty Park — SLC\'s favorite green space. Locals jog, picnic, and play here. It\'s a great way to wind down before your flight tomorrow.',
              details: [
                '🌳 80-acre park with a pond, playground, and the Tracy Aviary',
                '🏞️ Beautiful in May with spring flowers'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Takashi',
              description: 'Widely considered the best sushi in Utah — fresh, creative, and packed nightly. A perfect change of pace from the Western fare of the past week.',
              meta: '💰 $$$ · 📍 18 W Market St, SLC'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7225, lng: -111.8619, label: '9th & 9th', num: 1, cat: 'attraction', desc: 'Charming walkable neighborhood' },
        { lat: 40.7156, lng: -111.8649, label: 'Liberty Park', num: 2, cat: 'attraction', desc: "SLC's favorite green space" },
        { lat: 40.7335, lng: -111.8573, label: 'Stoneground Kitchen', num: 3, cat: 'food', desc: 'Italian-inspired café in Sugar House' },
        { lat: 40.7640, lng: -111.8949, label: 'Takashi', num: 4, cat: 'food', desc: 'Best sushi in Utah' }
      ]
    },

    // ===== CHICAGO: May 20-28 =====
    {
      num: 24,
      date: '2026-05-20',
      neighborhoods: 'The Loop · Millennium Park · Michigan Avenue',
      title: 'Arrive Chicago — The Bean & Deep Dish',
      description: "Fly from SLC to Chicago and arrive in one of America's greatest food cities. Head straight to Millennium Park, see The Bean, walk the Magnificent Mile, and eat the deep-dish pizza you've been dreaming about.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Flight: SLC → Chicago O\'Hare',
              description: 'Fly from Salt Lake City to Chicago (~3.5 hours). Take the Blue Line from O\'Hare into downtown — it\'s the cheapest and fastest way into the city.',
              details: [
                '✈️ SLC → ORD, ~3.5 hours',
                '🚇 Blue Line from O\'Hare to the Loop — $5, about 45 min',
                '🏙️ Welcome to the Third City!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Millennium Park & The Bean',
              description: "Cloud Gate (aka \"The Bean\") is Chicago's most iconic sculpture — a massive reflective bean that mirrors the skyline. Millennium Park also has the Crown Fountain (kids love it), the Lurie Garden, and in summer, free concerts at the Pritzker Pavilion.",
              details: [
                '📸 Cloud Gate — best photos early morning or at sunset',
                '⛲ Crown Fountain — two 50-foot video towers that \"spit\" water',
                '🌸 Lurie Garden — peaceful escape within the park',
                '🎵 Jay Pritzker Pavilion — Frank Gehry\'s outdoor concert venue'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Lou Malnati\'s Pizzeria',
              description: 'The deep-dish institution. The Malnati Chicago Classic — sausage patty, crushed tomatoes, mozzarella in a buttery crust — is perfection. Get here early or expect a wait.',
              meta: '💰 $$ · 📍 Multiple locations · Original: 439 N Wells St, River North'
            }
          ],
          tips: [
            { type: 'tip', text: 'Deep-dish pizza takes 30-45 minutes to bake. Order appetizers and enjoy the anticipation.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8827, lng: -87.6233, label: 'Cloud Gate (The Bean)', num: 1, cat: 'attraction', desc: 'Chicago\'s most iconic sculpture' },
        { lat: 41.8826, lng: -87.6226, label: 'Millennium Park', num: 2, cat: 'attraction', desc: 'World-class public park and cultural hub' },
        { lat: 41.8901, lng: -87.6341, label: 'Lou Malnati\'s', num: 3, cat: 'food', desc: 'Legendary Chicago deep-dish pizza' }
      ]
    },
    {
      num: 25,
      date: '2026-05-21',
      neighborhoods: 'Chicago River · Loop Architecture · River North',
      title: 'Architecture Boat Tour & River North',
      description: "Chicago's architecture is world-famous, and the best way to see it is from the river. Take the acclaimed architecture boat tour, then explore River North's restaurants and galleries.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Chicago Architecture Foundation Boat Tour',
              description: "The #1 rated tour in Chicago — a 90-minute cruise down the Chicago River with expert docents explaining the evolution of the skyline. You'll learn about Louis Sullivan, Frank Lloyd Wright, Mies van der Rohe, and the buildings that made Chicago the birthplace of the skyscraper.",
              details: [
                '🚢 Book the Chicago Architecture Center river cruise (operated by Chicago\'s First Lady)',
                '⏰ Morning tours have better light — book the 10am or 11am',
                '💰 ~$50/person — worth every penny',
                '📸 Sit on the right side for the best views heading south'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Wildberry Pancakes & Café',
              description: 'Massive, creative pancakes and breakfast dishes. The Berry Bliss pancakes are legendary. Portions are huge — share with the group.',
              meta: '💰 $$ · 📍 130 E Randolph St, the Loop'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'River North Galleries & Shopping',
              description: "River North is Chicago's gallery district — dozens of contemporary art galleries in converted warehouses. Also great for shopping, with boutiques and the massive Merchandise Mart.",
              details: [
                '🎨 River North Gallery District — dozens of galleries, free to browse',
                '🏛️ Merchandise Mart — one of the largest buildings in the world',
                '🛍️ Mix of independent boutiques and major brands'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Girl & the Goat',
              description: 'Stephanie Izard\'s flagship restaurant — bold, creative, globally-inspired dishes meant for sharing. The wood-oven roasted pig face is a legend. Fun, loud, and unforgettable.',
              meta: '💰 $$$ · 📍 809 W Randolph St, West Loop · Reserve far ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8882, lng: -87.6218, label: 'Architecture Boat Tour', num: 1, cat: 'attraction', desc: '#1 rated tour in Chicago' },
        { lat: 41.8854, lng: -87.6243, label: 'Wildberry Pancakes', num: 2, cat: 'food', desc: 'Legendary creative pancakes' },
        { lat: 41.8908, lng: -87.6340, label: 'River North', num: 3, cat: 'attraction', desc: 'Gallery district and dining' },
        { lat: 41.8841, lng: -87.6488, label: 'Girl & the Goat', num: 4, cat: 'food', desc: 'Stephanie Izard\'s bold, creative restaurant' }
      ]
    },
    {
      num: 26,
      date: '2026-05-22',
      neighborhoods: 'West Loop · Fulton Market · Greektown',
      title: 'West Loop Food Crawl — Chicago\'s Restaurant Row',
      description: "The West Loop / Fulton Market district is where Chicago's food scene lives. Former meatpacking warehouses are now home to some of the city's best restaurants. Today is a food day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fulton Market District Walk',
              description: "Explore the Fulton Market neighborhood — once the city's meatpacking district, now its culinary epicenter. The architecture is a mix of industrial heritage and sleek new construction.",
              details: [
                '🏗️ Former meatpacking warehouses turned restaurant row',
                '📸 Great murals and street art in the area',
                '🛍️ Boutiques and design shops along Randolph Street'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Au Cheval',
              description: 'The burger that put Chicago on the food map. A thick, decadent cheeseburger with a fried egg that\'s been called the best in America. The wait is long — put your name in early.',
              meta: '💰 $$$ · 📍 800 W Randolph St, West Loop · No reservations, expect a wait'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Greektown',
              description: "Walk over to Greektown on Halsted Street — Chicago has one of the largest Greek communities in the US. The restaurants here have been serving up flaming saganaki (\"Opa!\") for decades.",
              details: [
                '🇬🇷 The National Hellenic Museum — Greek American history',
                '🧀 Saganaki (flaming cheese) was invented in Chicago\'s Greektown',
                '🍢 Greek Islands — classic Greektown restaurant'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ema',
              description: 'Mediterranean restaurant in River North — hummus flights, wood-fired meats, and creative small plates. Perfect for sharing with a big group in a lively, modern space.',
              meta: '💰 $$ · 📍 74 W Illinois St, River North'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8866, lng: -87.6492, label: 'Fulton Market', num: 1, cat: 'attraction', desc: 'Chicago\'s culinary epicenter' },
        { lat: 41.8844, lng: -87.6495, label: 'Au Cheval', num: 2, cat: 'food', desc: 'Best burger in America' },
        { lat: 41.8778, lng: -87.6468, label: 'Greektown', num: 3, cat: 'attraction', desc: 'Flaming saganaki and Greek culture' },
        { lat: 41.8909, lng: -87.6319, label: 'Ema', num: 4, cat: 'food', desc: 'Mediterranean small plates and hummus flights' }
      ]
    },
    {
      num: 27,
      date: '2026-05-23',
      neighborhoods: 'Art Institute · Grant Park · Museum Campus',
      title: 'Art, Science & Lakefront',
      description: "Chicago's museum game is elite. Spend the morning at the world-class Art Institute, afternoon at the Museum of Science and Industry or Field Museum, and evening on the lakefront.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Art Institute of Chicago',
              description: "One of the greatest art museums in the world. The Impressionist collection rivals the Musée d'Orsay. Don't miss Seurat's A Sunday Afternoon, Grant Wood's American Gothic, and Hopper's Nighthawks.",
              details: [
                '🖼️ #1 rated museum in the world by TripAdvisor multiple times',
                '🎨 Impressionist gallery — Monet, Renoir, Seurat, Caillebotte',
                '📸 The lion statues out front are iconic Chicago',
                '⏱️ Budget at least 2-3 hours'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Field Museum or Museum of Science & Industry',
              description: 'Choose your adventure: the Field Museum of Natural History (Sue the T-Rex!) on Museum Campus, or the Museum of Science & Industry (a real captured U-505 submarine!) in Hyde Park.',
              details: [
                '🦖 Field Museum — Sue the T-Rex, the largest and most complete ever found',
                '🔬 Museum of Science & Industry — captured WWII German submarine',
                '📍 Field Museum is closer (Museum Campus), MSI is in Hyde Park (~20 min drive)'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Portillo\'s',
              description: 'Chicago institution — the Italian beef (dipped, with hot giardiniera) is a religious experience. Also famous for their Chicago-style hot dogs and chocolate cake shake.',
              meta: '💰 $ · 📍 100 W Ontario St, River North (or multiple locations)'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lakefront Trail at Sunset',
              description: "Walk or bike along the Chicago Lakefront Trail — 18 miles of uninterrupted path along Lake Michigan. The stretch from Museum Campus to Navy Pier at sunset is magical, with the skyline glowing golden behind you.",
              details: [
                '🚲 Divvy bike share — cheap and easy way to cruise the lakefront',
                '🌅 Sunset views from Adler Planetarium are spectacular',
                '🏖️ North Avenue Beach — watch the skyline from the sand'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Frontera Grill',
              description: 'Rick Bayless\'s acclaimed Mexican restaurant. Regional Mexican cuisine with incredible moles, ceviches, and seasonal dishes. Casual and beloved.',
              meta: '💰 $$$ · 📍 445 N Clark St, River North'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8796, lng: -87.6237, label: 'Art Institute of Chicago', num: 1, cat: 'attraction', desc: '#1 rated art museum in the world' },
        { lat: 41.8663, lng: -87.6170, label: 'Field Museum', num: 2, cat: 'attraction', desc: 'Sue the T-Rex and natural history' },
        { lat: 41.8826, lng: -87.6100, label: 'Lakefront Trail', num: 3, cat: 'attraction', desc: '18 miles of scenic lakefront path' },
        { lat: 41.8929, lng: -87.6316, label: 'Portillo\'s', num: 4, cat: 'food', desc: 'Chicago Italian beef institution' },
        { lat: 41.8911, lng: -87.6307, label: 'Frontera Grill', num: 5, cat: 'food', desc: 'Rick Bayless\'s celebrated Mexican restaurant' }
      ]
    },
    {
      num: 28,
      date: '2026-05-24',
      neighborhoods: 'Lincoln Park · Wrigleyville · Old Town',
      title: 'Lincoln Park, Wrigley Field & Chicago Comedy',
      description: "Explore Chicago's North Side — the green spaces of Lincoln Park, the legendary Wrigley Field neighborhood, and a night at Second City or an improv show.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Lincoln Park & Zoo',
              description: 'Lincoln Park is one of Chicago\'s most beautiful neighborhoods, anchored by the free Lincoln Park Zoo — one of the oldest zoos in the US. Walk through the conservatory, see the nature boardwalk, and enjoy spring in the city.',
              details: [
                '🦁 Lincoln Park Zoo — free admission, always!',
                '🌿 Lincoln Park Conservatory — tropical plants in glass houses',
                '🌊 North Pond — scenic spot in the middle of the park'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Batter & Berries',
              description: 'Lincoln Park brunch legend — the caramel french toast is life-changing. Expect a line but it moves fast.',
              meta: '💰 $$ · 📍 2748 N Lincoln Ave, Lincoln Park'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wrigleyville & Wrigley Field',
              description: "Even if there's no game, walking around Wrigley Field is a Chicago essential. The marquee, the ivy walls, and the surrounding bars and restaurants create an atmosphere like nowhere else in baseball.",
              details: [
                '⚾ Check if the Cubs have a home game — catching a game at Wrigley is unforgettable',
                '🍺 Murphy\'s Bleachers — legendary sports bar across from Wrigley',
                '📸 The Wrigley Field marquee is the most photographed sign in sports'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Second City or Improv Show',
              description: "Chicago is the birthplace of improv comedy. Second City launched the careers of Tina Fey, Steve Carell, Amy Poehler, and dozens more. Catch a show — the mainstage revues are world-class.",
              details: [
                '🎭 The Second City — mainstage and e.t.c. shows',
                '😂 iO Theater — another legendary improv venue',
                '🎫 Book tickets in advance — shows sell out'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Big Star',
              description: 'Tacos, whiskey, and honky-tonk music in Wicker Park. The al pastor tacos and margaritas are incredible. Outdoor patio is perfect in May.',
              meta: '💰 $$ · 📍 1531 N Damen Ave, Wicker Park'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.9211, lng: -87.6340, label: 'Lincoln Park Zoo', num: 1, cat: 'attraction', desc: 'Free zoo in beautiful Lincoln Park' },
        { lat: 41.9484, lng: -87.6553, label: 'Wrigley Field', num: 2, cat: 'attraction', desc: 'Legendary baseball stadium' },
        { lat: 41.9163, lng: -87.6361, label: 'Second City', num: 3, cat: 'attraction', desc: 'Birthplace of improv comedy' },
        { lat: 41.9280, lng: -87.6405, label: 'Batter & Berries', num: 4, cat: 'food', desc: 'Legendary caramel french toast' },
        { lat: 41.9095, lng: -87.6777, label: 'Big Star', num: 5, cat: 'food', desc: 'Tacos and whiskey in Wicker Park' }
      ]
    },
    {
      num: 29,
      date: '2026-05-25',
      neighborhoods: 'Hyde Park · Pilsen · Chinatown',
      title: 'South Side Soul — Hyde Park, Pilsen & Chinatown',
      description: "Explore Chicago's South Side — the intellectual hub of Hyde Park (Obama's neighborhood), the vibrant murals and Mexican culture of Pilsen, and the excellent food of Chinatown.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hyde Park & the University of Chicago',
              description: "The Obamas' neighborhood. Walk through the beautiful University of Chicago campus (Gothic architecture that rivals Yale), visit the Robie House (Frank Lloyd Wright masterpiece), and see the Obama Presidential Center (under construction).",
              details: [
                '🏛️ University of Chicago campus — stunning Gothic quads',
                '🏠 Robie House — Frank Lloyd Wright\'s Prairie Style masterpiece',
                '📚 Seminary Co-op Bookstores — one of the best bookshops in the US',
                '🏗️ Obama Presidential Center — under construction, exterior is impressive'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Valois Restaurant',
              description: 'Obama\'s favorite cafeteria — \"See Your Food\" is the motto. Honest, cheap, no-frills breakfast. The man ate here regularly as a senator.',
              meta: '💰 $ · 📍 1518 E 53rd St, Hyde Park'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pilsen — Murals & Mexican Culture',
              description: "Pilsen is Chicago's vibrant Mexican American neighborhood — every block is covered in incredible murals. The National Museum of Mexican Art (free!) is one of the best cultural museums in the city.",
              details: [
                '🎨 16th Street murals — outdoor gallery of Mexican American art',
                '🏛️ National Museum of Mexican Art — free admission, world-class',
                '🌮 18th Street — the main commercial strip with taquerias and bakeries'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Lunch',
              name: 'Mi Tocaya Antojería',
              description: 'Modern Mexican restaurant in Pilsen — creative takes on classic antojitos. The mushroom barbacoa and mezcal cocktails are outstanding.',
              meta: '💰 $$ · 📍 2800 W Chicago Ave, Humboldt Park'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chinatown',
              description: "Chicago's Chinatown is vibrant and authentic. Walk under the ornate gate, browse the shops on Wentworth Avenue, and feast on dim sum or hot pot.",
              details: [
                '🏮 Chinatown Gate — ornate entrance on Wentworth Ave',
                '🛍️ Wentworth Avenue shops — Chinese bakeries, tea shops, herbalists',
                '🥟 Some of the best dim sum outside of the coasts'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Dinner',
              name: 'MingHin Cuisine',
              description: 'Excellent dim sum in Chicago Chinatown. The har gow, siu mai, and BBQ pork buns are authentic and delicious. Big, bright dining room great for groups.',
              meta: '💰 $$ · 📍 2168 S Archer Ave, Chinatown'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.7886, lng: -87.5987, label: 'University of Chicago', num: 1, cat: 'attraction', desc: 'Gothic campus — Obama\'s neighborhood' },
        { lat: 41.8563, lng: -87.6712, label: 'Pilsen Murals', num: 2, cat: 'attraction', desc: 'Vibrant Mexican American street art' },
        { lat: 41.8540, lng: -87.6723, label: 'National Museum of Mexican Art', num: 3, cat: 'attraction', desc: 'Free, world-class Mexican art museum' },
        { lat: 41.8516, lng: -87.6335, label: 'Chinatown', num: 4, cat: 'attraction', desc: 'Authentic dim sum and Chinese culture' },
        { lat: 41.7917, lng: -87.5969, label: 'Valois', num: 5, cat: 'food', desc: 'Obama\'s favorite cafeteria' },
        { lat: 41.8516, lng: -87.6335, label: 'MingHin Cuisine', num: 6, cat: 'food', desc: 'Best dim sum in Chicago' }
      ]
    },
    {
      num: 30,
      date: '2026-05-26',
      neighborhoods: 'Wicker Park · Bucktown · Logan Square',
      title: 'Wicker Park & Logan Square — Indie Chicago',
      description: "Explore Chicago's coolest neighborhoods — vintage shops, street art, indie music venues, and some of the city's most creative restaurants. This is the non-touristy Chicago that locals love.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Wicker Park & Bucktown',
              description: 'Hip, tree-lined neighborhoods full of vintage shops, record stores, and excellent coffee. The six-way intersection at Damen/Milwaukee/North is the heart of it all.',
              details: [
                '🛍️ Vintage shops — Kokorokoko, Ragstock, and dozens more',
                '💿 Reckless Records — iconic Chicago record store',
                '☕ Wormhole Coffee — vintage décor and excellent espresso'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Dove\'s Luncheonette',
              description: 'Tex-Mex diner vibes with a vinyl jukebox and incredible chilaquiles. Cozy counter seating and a vintage atmosphere. A Wicker Park gem.',
              meta: '💰 $$ · 📍 1545 N Damen Ave, Wicker Park'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Logan Square',
              description: 'Walk or bike up Milwaukee Avenue to Logan Square — a beautiful neighborhood centered around a grand boulevard with a historic monument. The food scene here rivals the West Loop at lower prices.',
              details: [
                '🏛️ Illinois Centennial Monument in the square',
                '🌳 Logan Boulevard — gorgeous tree-lined street with mansions',
                '🍺 Revolution Brewing taproom — Chicago\'s largest craft brewery'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Lula Cafe',
              description: 'Farm-to-table pioneer in Logan Square. Creative, seasonal dishes in a warm, neighborhood setting. The Monday night prix fixe is legendary.',
              meta: '💰 $$$ · 📍 2537 N Kedzie Ave, Logan Square'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 41.9088, lng: -87.6772, label: 'Wicker Park', num: 1, cat: 'attraction', desc: 'Hip vintage shops and street art' },
        { lat: 41.9093, lng: -87.6780, label: 'Dove\'s Luncheonette', num: 2, cat: 'food', desc: 'Tex-Mex diner with vinyl jukebox' },
        { lat: 41.9233, lng: -87.6990, label: 'Logan Square', num: 3, cat: 'attraction', desc: 'Grand boulevard and indie food scene' },
        { lat: 41.9240, lng: -87.6988, label: 'Lula Cafe', num: 4, cat: 'food', desc: 'Farm-to-table pioneer' }
      ]
    },
    {
      num: 31,
      date: '2026-05-27',
      neighborhoods: 'Navy Pier · Magnificent Mile · Chicago Riverwalk',
      title: 'Navy Pier, Shopping & Riverwalk',
      description: "Soak up the last full day with Chicago's waterfront attractions. Ride the Centennial Wheel at Navy Pier, shop the Magnificent Mile, and walk the beautiful Chicago Riverwalk.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Navy Pier',
              description: 'Chicago\'s most-visited attraction — a 3,300-foot pier on Lake Michigan with the Centennial Wheel, gardens, and great lake views.',
              details: [
                '🎡 Centennial Wheel — 196 feet high, incredible lake and skyline views',
                '🌊 Walk to the end of the pier for open lake panoramas',
                '🎭 Chicago Shakespeare Theater is here if you want a matinee'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Magnificent Mile',
              description: 'Michigan Avenue\'s famous shopping stretch — 13 blocks of flagship stores and the Historic Water Tower, one of the few buildings to survive the Great Fire of 1871.',
              details: [
                '🛍️ Water Tower Place, 900 North Michigan, flagship stores',
                '🏛️ Historic Water Tower — survived the Great Chicago Fire',
                '📸 Tribune Tower — stones from famous buildings in its walls'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Al\'s #1 Italian Beef',
              description: 'The original Chicago Italian beef since 1938. Get it dipped with hot giardiniera.',
              meta: '💰 $ · 📍 1079 W Taylor St, Little Italy'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chicago Riverwalk Sunset',
              description: 'Walk the Riverwalk — a pedestrian path with restaurants, bars, and kayak rentals. Watch the sunset paint the buildings gold.',
              details: [
                '🍷 City Winery on the Riverwalk — wine and sunset views',
                '🛶 Kayak rentals for a river perspective on the architecture',
                '🌅 The river reflects the buildings at sunset — magical'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Pequod\'s Pizza',
              description: 'The other Chicago deep-dish legend. Famous for the caramelized cheese crust. Many locals prefer it over Lou Malnati\'s.',
              meta: '💰 $$ · 📍 2207 N Clybourn Ave, Lincoln Park'
            }
          ],
          tips: [
            { type: 'tip', text: 'Last night! Raise a glass to an incredible 31-day journey across America. 🎓🗽🍕🏜️🦬🏙️' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8919, lng: -87.6051, label: 'Navy Pier', num: 1, cat: 'attraction', desc: 'Centennial Wheel and lakefront' },
        { lat: 41.8944, lng: -87.6246, label: 'Magnificent Mile', num: 2, cat: 'attraction', desc: 'Chicago\'s premier shopping street' },
        { lat: 41.8873, lng: -87.6240, label: 'Chicago Riverwalk', num: 3, cat: 'attraction', desc: 'Scenic riverside path' },
        { lat: 41.8694, lng: -87.6560, label: 'Al\'s Italian Beef', num: 4, cat: 'food', desc: 'Original Italian beef since 1938' },
        { lat: 41.9196, lng: -87.6644, label: 'Pequod\'s Pizza', num: 5, cat: 'food', desc: 'Caramelized crust deep-dish' }
      ]
    },
    {
      num: 32,
      date: '2026-05-28',
      neighborhoods: 'Departure Day',
      title: 'Farewell Chicago — End of an Epic Journey',
      description: "Last morning of this incredible 31-day journey. Grab one final breakfast and head to the airport with memories that will last a lifetime.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Last Chicago Morning',
              description: 'Take a final stroll, grab coffee, and reflect on 31 days and 8 cities of unforgettable experiences.',
              details: [
                '☕ One last Chicago coffee — Intelligentsia, Metric, or Dark Matter',
                '📸 Final photos at the Bean or your favorite spot',
                '✈️ Head to O\'Hare or Midway for your flight home'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Do-Rite Donuts',
              description: 'Best donuts in Chicago — the pistachio old fashioned is incredible. A sweet ending to an epic trip.',
              meta: '💰 $ · 📍 50 W Randolph St, the Loop'
            }
          ],
          tips: [
            { type: 'tip', text: '31 days, 8+ cities, 3 graduations, 2 national parks, and countless incredible meals. What a trip! 🎓🗽🍕🏜️🦬🏙️' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8845, lng: -87.6295, label: 'Do-Rite Donuts', num: 1, cat: 'food', desc: 'Best donuts in Chicago' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Flights (per person)', budget: '$300–500', midrange: '$500–800', luxury: '$800–1,500' },
    { category: 'Accommodation', budget: '$100–150/night', midrange: '$150–300/night', luxury: '$300–600/night' },
    { category: 'Meals (per person)', budget: '$40–60/day', midrange: '$60–100/day', luxury: '$100–200/day' },
    { category: 'Rental Car (road trip)', budget: '$50–80/day', midrange: '$80–120/day', luxury: '$120–200/day' },
    { category: 'Activities & Admissions', budget: '$20–40/day', midrange: '$40–80/day', luxury: '$80–150/day' },
    { category: 'National Park Passes', budget: '$35/vehicle', midrange: '$35/vehicle', luxury: '$80 (Annual)' },
    { category: '31-Day Total (per person)', budget: '$3,000–5,000', midrange: '$5,000–9,000', luxury: '$9,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Flights to Book', items: ['Boston Logan (BOS) — arrive Apr 27', 'JFK/EWR/BDL → Las Vegas (LAS) — May 9', 'Salt Lake City (SLC) → Chicago O\'Hare (ORD) — May 20', 'Chicago O\'Hare (ORD) or Midway (MDW) — depart May 28'] },
    { title: '🚗 Rental Car', items: ['Pick up in Las Vegas on May 9, drop off in Salt Lake City around May 19-20', 'Needed for: Vegas → Grand Canyon → SLC → Yellowstone → SLC', 'One-way drop-off fee may apply — compare prices', 'Book early for national park season rates'] },
    { title: '🏨 Where to Stay', items: ['Boston (4 nights): Airbnb in Back Bay or Fenway', 'NYC (6 nights): Airbnb in Manhattan or Brooklyn', 'New Haven (1 night): Hotel near Yale', 'Vegas (1 night): Budget hotel off-Strip', 'Grand Canyon (2-3 nights): Tusayan or in-park lodges — book months ahead', 'Yellowstone (3-4 nights): West Yellowstone motels — book NOW', 'SLC (2 nights): Downtown hotel', 'Chicago (8 nights): Airbnb in River North, West Loop, or Lincoln Park'] },
    { title: '🌡️ Weather', items: ['Boston (late Apr): 50-65°F, spring layers', 'NYC (early May): 55-70°F, pleasant spring', 'Las Vegas (May): 80-95°F, hot and dry', 'Grand Canyon rim (May): 55-75°F, cooler at elevation', 'Yellowstone (mid-May): 30-55°F, possible snow — pack warm!', 'Chicago (late May): 60-75°F, beautiful late spring'] },
    { title: '💳 Budget Tips', items: ['Share Airbnbs for the group — much cheaper than hotels', 'National park entry: $35/vehicle or $80 annual pass', 'Tip 18-20% at sit-down restaurants', 'Book Amtrak and flights 3-6 weeks ahead', 'This itinerary focuses on casual dining — budget $40-80/person/day for food'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}