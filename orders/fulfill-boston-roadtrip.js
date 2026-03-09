const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772251174169_adopmp',
  email: 'shreya.nalla@gmail.com',
  destination: 'Boston, MA, USA',
  start_date: '2026-04-27',
  end_date: '2026-05-28',
  group_size: '5+',
  travel_style: 'Cultural, Foodie',
  dining: 'Casual throughout',
  budget: '$2,000-5,000',
  requests: 'Boston first. Cousins grad ceremonies on 29th April and 1st May. Brothers grad ceremony on 8th in New Haven.',
  amount: '0.00',
  timestamp: '2026-02-28T03:59:34.169Z',
  status: 'pending'
};

const itineraryData = {
  destination: "Boston → NYC → New Haven → Las Vegas → Grand Canyon → Salt Lake City → Yellowstone → Chicago",
  countryEmoji: "🇺🇸",
  title: "The Great American Journey",
  subtitle: "Boston to Chicago — A 31-Day Cultural & Foodie Road Trip",
  description: "An epic cross-country adventure spanning 8 cities over 31 days. From Ivy League graduations in New England to the wild grandeur of the American West, this itinerary blends family celebrations, world-class food scenes, and jaw-dropping national parks into one unforgettable trip.",
  duration: "31 days",
  dates: "April 27 – May 28, 2026",
  budget: "$2,000–5,000 per person",
  pace: "Moderate — with built-in rest days",
  bestFor: "Cultural explorers, foodies, families celebrating milestones",
  essentials: [
    { title: "✈️ Flights", text: "Book: arrival into Boston (Apr 27), Vegas one-way (May 9), SLC → Chicago (May 21), departure from Chicago (May 28). Southwest/JetBlue for domestic legs." },
    { title: "🚗 Rental Car", text: "Rent a car in Las Vegas (May 9) and return in Salt Lake City (May 21). You'll need it for Grand Canyon, SLC, and Yellowstone. Book SUV for 5+ people." },
    { title: "🏨 Accommodations", text: "Mix of hotels and Airbnbs. Book Yellowstone lodging EARLY — Old Faithful Inn or cabins in West Yellowstone fill up fast." },
    { title: "🎓 Graduations", text: "Northeastern University: Apr 29 & May 1. New Haven (Yale area): May 8. Plan outfits and gifts ahead!" },
    { title: "🌡️ Weather", text: "Boston/NYC in late April–early May: 55-70°F. Vegas/Grand Canyon mid-May: 85-100°F. Yellowstone: 40-60°F (bring layers!). Chicago late May: 65-75°F." }
  ],
  days: [
    // ============ BOSTON: Days 1-5 (Apr 27 – May 1) ============
    {
      num: 1,
      date: "April 27",
      neighborhoods: "Boston · Back Bay · Beacon Hill",
      title: "Arrival & Boston Orientation",
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive in Boston", description: "Check into your hotel/Airbnb in Back Bay or Cambridge. Settle in and get oriented." },
            { title: "Stroll Through Beacon Hill", description: "Walk the cobblestone streets of one of America's most charming neighborhoods. Browse the antique shops on Charles Street." }
          ],
          meals: [
            { type: "Dinner", name: "Neptune Oyster", description: "Iconic North End seafood spot — the lobster roll is legendary. Expect a wait but it's worth every minute.", meta: "$$$ · North End · Cash-friendly" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3563, lng: -71.0686, label: "Back Bay", num: 1, cat: "neighborhood", desc: "Home base area" },
        { lat: 42.3588, lng: -71.0707, label: "Beacon Hill", num: 2, cat: "neighborhood", desc: "Historic cobblestone streets" },
        { lat: 42.3636, lng: -71.0531, label: "Neptune Oyster", num: 3, cat: "food", desc: "Famous lobster rolls" }
      ]
    },
    {
      num: 2,
      date: "April 28",
      neighborhoods: "Boston · Freedom Trail · North End",
      title: "Freedom Trail & Italian Feasting",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Walk the Freedom Trail", description: "Follow the 2.5-mile red-brick path through 16 historic sites — from Boston Common to Paul Revere's House to the Old North Church. A crash course in American history." }
          ],
          meals: [
            { type: "Lunch", name: "Giacomo's Ristorante", description: "Tiny North End institution with massive portions of Italian comfort food. No reservations — line up early.", meta: "$$ · North End · Cash only" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Faneuil Hall & Quincy Market", description: "Browse the historic marketplace, grab snacks, watch street performers. Great for the whole group." }
          ],
          meals: [
            { type: "Dinner", name: "Regina Pizzeria", description: "The original since 1926. Thin-crust brick-oven pizza in the heart of the North End. A Boston rite of passage.", meta: "$$ · North End" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3554, lng: -71.0640, label: "Boston Common (Freedom Trail Start)", num: 1, cat: "attraction", desc: "Start of the Freedom Trail" },
        { lat: 42.3637, lng: -71.0546, label: "Paul Revere's House", num: 2, cat: "attraction", desc: "Historic landmark" },
        { lat: 42.3601, lng: -71.0549, label: "Faneuil Hall", num: 3, cat: "attraction", desc: "Historic marketplace" },
        { lat: 42.3649, lng: -71.0563, label: "Regina Pizzeria", num: 4, cat: "food", desc: "Legendary brick-oven pizza since 1926" }
      ]
    },
    {
      num: 3,
      date: "April 29",
      neighborhoods: "Boston · Northeastern University · Fenway",
      title: "🎓 Graduation Day — Northeastern University",
      timeBlocks: [
        {
          label: "Morning & Afternoon",
          activities: [
            { title: "🎓 Cousin's Graduation Ceremony", description: "Graduation day at Northeastern University! Arrive early for good seats. The ceremony is at Matthews Arena or the main campus quad. Dress smart and bring your camera." }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Celebration Dinner", description: "After the ceremony, celebrate with the family at a great Boston restaurant." }
          ],
          meals: [
            { type: "Dinner", name: "Legal Sea Foods", description: "Classic Boston seafood chain that's actually excellent. Great for large groups — clam chowder is a must.", meta: "$$ · Multiple locations · Reservations recommended" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3398, lng: -71.0892, label: "Northeastern University", num: 1, cat: "attraction", desc: "Graduation ceremony" },
        { lat: 42.3467, lng: -71.0972, label: "Fenway Park Area", num: 2, cat: "neighborhood", desc: "Nearby dining options" }
      ]
    },
    {
      num: 4,
      date: "April 30",
      neighborhoods: "Cambridge · Harvard · MIT",
      title: "Cambridge Intellectuals & Craft Beer",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Harvard Yard & Harvard Square", description: "Walk through the iconic campus, browse the bookshops on Mass Ave, and soak in the collegiate atmosphere. Touch the John Harvard statue's foot for luck." },
            { title: "MIT Campus Walk", description: "Cross the river to see MIT's stunning mix of classical and avant-garde architecture — the Stata Center is wild." }
          ],
          meals: [
            { type: "Lunch", name: "Mr. Bartley's Burger Cottage", description: "Harvard Square legend. Creative burgers named after celebrities, thick frappes, and a truly chaotic vibe.", meta: "$$ · Harvard Square · Cash only" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Museum of Fine Arts or Isabella Stewart Gardner Museum", description: "Pick one: the encyclopedic MFA or the intimate, courtyard-centered Gardner. Both are world-class." }
          ],
          meals: [
            { type: "Dinner", name: "Giulia", description: "Upscale handmade pasta in Cambridge. One of the best Italian restaurants in the Boston area. Book ahead.", meta: "$$$ · Cambridge" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3770, lng: -71.1167, label: "Harvard Yard", num: 1, cat: "attraction", desc: "Iconic university campus" },
        { lat: 42.3601, lng: -71.0942, label: "MIT Campus", num: 2, cat: "attraction", desc: "Avant-garde architecture" },
        { lat: 42.3394, lng: -71.0940, label: "Museum of Fine Arts", num: 3, cat: "attraction", desc: "World-class art collection" },
        { lat: 42.3753, lng: -71.1190, label: "Mr. Bartley's", num: 4, cat: "food", desc: "Legendary burger spot" }
      ]
    },
    {
      num: 5,
      date: "May 1",
      neighborhoods: "Boston · Northeastern University · Seaport",
      title: "🎓 Second Graduation & Seaport District",
      timeBlocks: [
        {
          label: "Morning & Afternoon",
          activities: [
            { title: "🎓 Cousin's Second Graduation Ceremony", description: "Back to Northeastern for the second graduation event. Same drill — arrive early, celebrate big!" }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Explore the Seaport District", description: "Boston's trendiest neighborhood. Walk along the waterfront, check out the ICA (Institute of Contemporary Art), and enjoy the buzzy restaurant scene." }
          ],
          meals: [
            { type: "Dinner", name: "Row 34", description: "Sleek Seaport oyster bar and craft brewery. Excellent raw bar, creative seafood dishes, and a great beer list.", meta: "$$ · Seaport District" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3398, lng: -71.0892, label: "Northeastern University", num: 1, cat: "attraction", desc: "Second graduation ceremony" },
        { lat: 42.3519, lng: -71.0447, label: "Seaport District", num: 2, cat: "neighborhood", desc: "Trendy waterfront neighborhood" },
        { lat: 42.3521, lng: -71.0432, label: "Row 34", num: 3, cat: "food", desc: "Oyster bar & craft brewery" }
      ]
    },
    // ============ NYC: Days 6-10 (May 2-6) ============
    {
      num: 6,
      date: "May 2",
      neighborhoods: "Transit · Boston → New York City",
      title: "Boston to NYC — The Northeast Corridor",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to NYC", description: "Take the Amtrak Acela or Northeast Regional from Boston South Station to Penn Station (~4 hours). Scenic ride through Connecticut and along the coast." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Check In & Times Square Area", description: "Drop bags at your hotel/Airbnb (Midtown or Lower Manhattan recommended for 5+ people). Walk through Times Square to get it out of your system." }
          ],
          meals: [
            { type: "Dinner", name: "Joe's Pizza", description: "The quintessential NYC slice. Grab a cheese slice and fold it in half like a real New Yorker. Greenwich Village location is the original.", meta: "$ · Greenwich Village" }
          ]
        }
      ],
      mapPins: [
        { lat: 42.3519, lng: -71.0552, label: "Boston South Station", num: 1, cat: "transport", desc: "Amtrak departure" },
        { lat: 40.7506, lng: -73.9935, label: "Penn Station NYC", num: 2, cat: "transport", desc: "Arrival in NYC" },
        { lat: 40.7580, lng: -73.9855, label: "Times Square", num: 3, cat: "attraction", desc: "The iconic neon crossroads" },
        { lat: 40.7308, lng: -74.0020, label: "Joe's Pizza", num: 4, cat: "food", desc: "NYC's quintessential slice" }
      ]
    },
    {
      num: 7,
      date: "May 3",
      neighborhoods: "Manhattan · Lower East Side · SoHo · Chinatown",
      title: "Downtown Manhattan Food Crawl",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Lower East Side Walking Tour", description: "Explore the immigrant history of the LES. Visit the Tenement Museum (book ahead!), browse vintage shops on Orchard Street." }
          ],
          meals: [
            { type: "Brunch", name: "Russ & Daughters Cafe", description: "Jewish appetizing since 1914. Smoked fish platters, bagels with lox, and egg creams in a beautiful sit-down space.", meta: "$$ · Lower East Side" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "SoHo & Chinatown", description: "Browse SoHo's cast-iron architecture and boutiques, then duck into Chinatown for some of the best and cheapest food in the city." }
          ],
          meals: [
            { type: "Snack", name: "Joe's Shanghai", description: "Soup dumplings (xiaolongbao) that are genuinely among the best in New York. Don't miss them.", meta: "$$ · Chinatown" },
            { type: "Dinner", name: "Prince Street Pizza", description: "The pepperoni square slice is an NYC legend — crispy, cupped pepperoni, spicy. Worth any line.", meta: "$ · Nolita" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7185, lng: -73.9880, label: "Russ & Daughters", num: 1, cat: "food", desc: "Legendary Jewish deli" },
        { lat: 40.7187, lng: -73.9901, label: "Tenement Museum", num: 2, cat: "attraction", desc: "Immigration history" },
        { lat: 40.7234, lng: -73.9985, label: "SoHo", num: 3, cat: "neighborhood", desc: "Shopping & architecture" },
        { lat: 40.7159, lng: -73.9972, label: "Chinatown", num: 4, cat: "neighborhood", desc: "Incredible food scene" },
        { lat: 40.7231, lng: -73.9946, label: "Prince Street Pizza", num: 5, cat: "food", desc: "Famous pepperoni square" }
      ]
    },
    {
      num: 8,
      date: "May 4",
      neighborhoods: "Manhattan · Central Park · Upper West Side · Harlem",
      title: "Central Park to Harlem",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Central Park", description: "Rent bikes or walk through the park — Bethesda Fountain, Bow Bridge, the Ramble, Strawberry Fields. It's enormous and endlessly beautiful." }
          ],
          meals: [
            { type: "Brunch", name: "Jacob's Pickles", description: "Southern comfort food on the Upper West Side. Massive biscuits, fried chicken, and creative pickle-forward dishes.", meta: "$$ · Upper West Side" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Harlem Food & Culture", description: "Head uptown for soul food, gospel brunch vibes, and the Apollo Theater exterior. Visit the Studio Museum or Malcolm Shabazz Harlem Market." }
          ],
          meals: [
            { type: "Dinner", name: "Sylvia's Restaurant", description: "The Queen of Soul Food since 1962. Fried chicken, mac and cheese, collard greens — the real deal in the heart of Harlem.", meta: "$$ · Harlem" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7736, lng: -73.9712, label: "Bethesda Fountain", num: 1, cat: "attraction", desc: "Central Park landmark" },
        { lat: 40.7812, lng: -73.9814, label: "Jacob's Pickles", num: 2, cat: "food", desc: "Southern comfort brunch" },
        { lat: 40.8100, lng: -73.9500, label: "Apollo Theater", num: 3, cat: "attraction", desc: "Legendary Harlem venue" },
        { lat: 40.8087, lng: -73.9443, label: "Sylvia's Restaurant", num: 4, cat: "food", desc: "Soul food institution" }
      ]
    },
    {
      num: 9,
      date: "May 5",
      neighborhoods: "Manhattan · Brooklyn · Williamsburg · DUMBO",
      title: "Brooklyn Bridge & Williamsburg Eats",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Walk the Brooklyn Bridge", description: "Start from the Manhattan side and walk across for incredible skyline views. Arrive in DUMBO for the iconic Manhattan Bridge photo spot on Washington Street." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Williamsburg", description: "Brooklyn's hippest neighborhood. Browse vintage shops, street art, and the Smorgasburg food market (weekends). The food scene rivals Manhattan." }
          ],
          meals: [
            { type: "Lunch", name: "L'Industrie Pizzeria", description: "Possibly NYC's best pizza right now — burrata slice is transcendent. Tiny shop, huge flavors.", meta: "$$ · Williamsburg" },
            { type: "Dinner", name: "Peter Luger Steak House", description: "NYC's most famous steakhouse since 1887. Porterhouse for the table, cash only, no-nonsense service. A bucket-list meal.", meta: "$$$$ · Williamsburg · Cash only" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7061, lng: -73.9969, label: "Brooklyn Bridge (Manhattan Side)", num: 1, cat: "attraction", desc: "Iconic bridge walk" },
        { lat: 40.7033, lng: -73.9894, label: "DUMBO", num: 2, cat: "neighborhood", desc: "Waterfront views & photo spots" },
        { lat: 40.7141, lng: -73.9613, label: "Williamsburg", num: 3, cat: "neighborhood", desc: "Hipster food & shopping" },
        { lat: 40.7098, lng: -73.9624, label: "Peter Luger", num: 4, cat: "food", desc: "Legendary steakhouse since 1887" }
      ]
    },
    {
      num: 10,
      date: "May 6",
      neighborhoods: "Manhattan · Statue of Liberty · Chelsea · West Village",
      title: "Lady Liberty & Village Vibes",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Statue of Liberty & Ellis Island", description: "Take the ferry from Battery Park. Book pedestal access tickets in advance. Ellis Island's immigration museum is genuinely moving." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Chelsea Market & High Line", description: "Browse Chelsea Market's food stalls (Los Tacos No. 1!), then walk the High Line elevated park up to Hudson Yards." }
          ],
          meals: [
            { type: "Lunch", name: "Los Tacos No. 1", description: "The best tacos in Manhattan, hands down. Adobada and nopal tacos are perfection. Inside Chelsea Market.", meta: "$ · Chelsea Market" },
            { type: "Dinner", name: "Via Carota", description: "The West Village Italian spot everyone's obsessed with. Seasonal, rustic, perfect. No reservations — arrive early or late.", meta: "$$$ · West Village" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.6892, lng: -74.0445, label: "Statue of Liberty", num: 1, cat: "attraction", desc: "America's iconic landmark" },
        { lat: 40.7425, lng: -74.0061, label: "Chelsea Market", num: 2, cat: "food", desc: "Indoor food hall" },
        { lat: 40.7480, lng: -74.0048, label: "The High Line", num: 3, cat: "attraction", desc: "Elevated park" },
        { lat: 40.7337, lng: -74.0036, label: "Via Carota", num: 4, cat: "food", desc: "Beloved West Village Italian" }
      ]
    },
    // ============ NEW HAVEN: Days 11-12 (May 7-8) ============
    {
      num: 11,
      date: "May 7",
      neighborhoods: "Transit · NYC → New Haven · Yale University",
      title: "NYC to New Haven — Pizza Pilgrimage",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to New Haven", description: "Take Metro-North from Grand Central to New Haven (~2 hours). Easy, scenic, and drops you right downtown." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Yale University Campus Tour", description: "Walk the gorgeous Gothic campus — the Harkness Tower, Sterling Memorial Library, and the beautiful residential colleges. Free self-guided tours available." },
            { title: "Yale University Art Gallery", description: "Free! One of the oldest university art museums in the Western hemisphere with works spanning ancient to contemporary." }
          ],
          meals: [
            { type: "Lunch", name: "Frank Pepe Pizzeria Napoletana", description: "The holy grail of New Haven-style apizza since 1925. The white clam pie is one of America's greatest pizzas. Period.", meta: "$$ · Wooster Street" },
            { type: "Dinner", name: "Sally's Apizza", description: "Pepe's fierce rival across the street. Charred, thin, and perfect. Get the tomato pie. The pizza wars are real and both sides win.", meta: "$$ · Wooster Street" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3083, lng: -72.9279, label: "New Haven Union Station", num: 1, cat: "transport", desc: "Metro-North arrival" },
        { lat: 41.3111, lng: -72.9267, label: "Yale Campus", num: 2, cat: "attraction", desc: "Gothic university campus" },
        { lat: 41.3025, lng: -72.9173, label: "Frank Pepe's", num: 3, cat: "food", desc: "Legendary New Haven pizza" },
        { lat: 41.3021, lng: -72.9176, label: "Sally's Apizza", num: 4, cat: "food", desc: "Pepe's iconic rival" }
      ]
    },
    {
      num: 12,
      date: "May 8",
      neighborhoods: "New Haven · Graduation",
      title: "🎓 Brother's Graduation Day",
      timeBlocks: [
        {
          label: "Morning & Afternoon",
          activities: [
            { title: "🎓 Brother's Graduation Ceremony", description: "The big day in New Haven! Arrive early for seating. Soak in the pomp and circumstance — this is what the trip is all about." }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Graduation Celebration", description: "Celebrate the graduate! New Haven has a surprisingly excellent restaurant scene beyond pizza." }
          ],
          meals: [
            { type: "Dinner", name: "Union League Cafe", description: "Elegant French-American brasserie right on the Green. Perfect for a special celebration dinner with the whole family.", meta: "$$$ · New Haven Green" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.3111, lng: -72.9267, label: "Graduation Venue", num: 1, cat: "attraction", desc: "Brother's graduation ceremony" },
        { lat: 41.3077, lng: -72.9285, label: "New Haven Green", num: 2, cat: "attraction", desc: "Historic town green" },
        { lat: 41.3080, lng: -72.9290, label: "Union League Cafe", num: 3, cat: "food", desc: "Celebration dinner" }
      ]
    },
    // ============ LAS VEGAS: Days 13-14 (May 9-10) ============
    {
      num: 13,
      date: "May 9",
      neighborhoods: "Transit · New Haven → Las Vegas · The Strip",
      title: "Fly to Vegas — Let the Road Trip Begin",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Fly to Las Vegas", description: "Early flight from New Haven/Hartford (BDL) or NYC area (JFK/EWR) to Las Vegas. ~5 hours. Pick up your rental car (SUV recommended for 5+) at Harry Reid International." }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "The Strip at Night", description: "Check into your hotel and experience the Strip after dark. The Bellagio fountains, neon lights, and people-watching are peak Vegas." }
          ],
          meals: [
            { type: "Dinner", name: "Secret Pizza at The Cosmopolitan", description: "Hidden pizza joint on the 3rd floor of the Cosmo — no signage, just follow the music. Surprisingly excellent late-night slices.", meta: "$ · The Cosmopolitan" }
          ]
        }
      ],
      mapPins: [
        { lat: 36.0840, lng: -115.1537, label: "Harry Reid International Airport", num: 1, cat: "transport", desc: "Arrive & pick up rental car" },
        { lat: 36.1126, lng: -115.1767, label: "The Strip", num: 2, cat: "attraction", desc: "Vegas neon wonderland" },
        { lat: 36.1098, lng: -115.1743, label: "Bellagio Fountains", num: 3, cat: "attraction", desc: "Iconic water show" }
      ]
    },
    {
      num: 14,
      date: "May 10",
      neighborhoods: "Las Vegas · Fremont Street · Arts District",
      title: "Vegas Beyond the Strip",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Fremont Street Experience", description: "Old Vegas! The original strip before the Strip. Vintage casinos, the Viva Vision LED canopy, and a grittier, more authentic Vegas vibe." }
          ],
          meals: [
            { type: "Brunch", name: "Eggslut", description: "LA's famous egg sandwich shop with a Vegas outpost at The Venetian. The Fairfax sandwich is life-changing.", meta: "$$ · The Venetian" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Arts District", description: "Vegas's creative heart — murals, galleries, breweries, and great coffee shops. A world away from the casinos." },
            { title: "Red Rock Canyon (Optional)", description: "If you want nature before the road trip begins, Red Rock Canyon is only 30 minutes west. Stunning desert landscapes and easy scenic drives." }
          ],
          meals: [
            { type: "Dinner", name: "Lotus of Siam", description: "Widely considered the best Thai restaurant in America. The northern Thai dishes are extraordinary. Book ahead!", meta: "$$$ · Off-Strip" }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1700, lng: -115.1422, label: "Fremont Street", num: 1, cat: "attraction", desc: "Old Vegas experience" },
        { lat: 36.1612, lng: -115.1537, label: "Arts District", num: 2, cat: "neighborhood", desc: "Murals & breweries" },
        { lat: 36.1353, lng: -115.4275, label: "Red Rock Canyon", num: 3, cat: "attraction", desc: "Desert scenic drive" },
        { lat: 36.1290, lng: -115.1350, label: "Lotus of Siam", num: 4, cat: "food", desc: "America's best Thai restaurant" }
      ]
    },
    // ============ GRAND CANYON: Days 15-16 (May 11-12) ============
    {
      num: 15,
      date: "May 11",
      neighborhoods: "Road Trip · Las Vegas → Grand Canyon South Rim",
      title: "Vegas to Grand Canyon — Road Trip Begins",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Grand Canyon South Rim", description: "~4.5 hour drive via I-40 through the Arizona desert. Stop in Kingman or Seligman on Route 66 for photos and nostalgia. Arrive at Grand Canyon Village by afternoon." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Mather Point & Rim Trail", description: "Your first view of the Grand Canyon will take your breath away. Mather Point is the classic overlook. Walk the Rim Trail east toward Yavapai Geology Museum." }
          ],
          meals: [
            { type: "Dinner", name: "El Tovar Dining Room", description: "Historic lodge dining room right on the rim. Southwest-inspired cuisine with a view you can't beat. Reservations essential.", meta: "$$$ · Grand Canyon Village" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2570, lng: -113.9874, label: "Kingman / Route 66", num: 1, cat: "attraction", desc: "Route 66 photo stop" },
        { lat: 36.0544, lng: -112.1074, label: "Mather Point", num: 2, cat: "attraction", desc: "Iconic Grand Canyon overlook" },
        { lat: 36.0544, lng: -112.1170, label: "El Tovar", num: 3, cat: "food", desc: "Historic rim-side dining" }
      ]
    },
    {
      num: 16,
      date: "May 12",
      neighborhoods: "Grand Canyon · South Rim",
      title: "Grand Canyon Deep Dive",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bright Angel Trail Hike", description: "Hike partway down the Bright Angel Trail — even 1.5 miles to the first rest house gives incredible perspective on the canyon's depth. Bring plenty of water!" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Desert View Watchtower", description: "Drive the East Rim to Desert View — the Mary Colter-designed watchtower offers 360° views. One of the best vistas in the park." },
            { title: "Sunset at Hopi Point", description: "End the day watching the canyon light up in reds and golds at Hopi Point. Arrive 45 min early for a good spot." }
          ],
          meals: [
            { type: "Lunch", name: "Arizona Room", description: "Casual rim-side restaurant with solid steaks and burgers. Sit by the window for canyon views while you eat.", meta: "$$ · Bright Angel Lodge" },
            { type: "Dinner", name: "Picnic at Sunset", description: "Grab supplies from the general store and have a sunset picnic at Hopi Point. Sometimes the best meals are the simplest.", meta: "$ · Self-catered" }
          ]
        }
      ],
      mapPins: [
        { lat: 36.0573, lng: -112.1432, label: "Bright Angel Trailhead", num: 1, cat: "attraction", desc: "Famous canyon hike" },
        { lat: 36.0429, lng: -111.8261, label: "Desert View Watchtower", num: 2, cat: "attraction", desc: "Panoramic viewpoint" },
        { lat: 36.0711, lng: -112.1548, label: "Hopi Point", num: 3, cat: "attraction", desc: "Best sunset viewpoint" }
      ]
    },
    // ============ ROAD TRIP TO SLC: Days 17-18 (May 13-14) ============
    {
      num: 17,
      date: "May 13",
      neighborhoods: "Road Trip · Grand Canyon → Page → Kanab",
      title: "Grand Canyon to Page — Monument Valley Vibes",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive Grand Canyon → Page, AZ", description: "~2.5 hour drive north to Page. Stop at the Cameron Trading Post for Navajo crafts and fry bread." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Horseshoe Bend", description: "The Instagram-famous 1,000-foot drop to the Colorado River. Short 1.5-mile round-trip walk from the parking lot. Vertigo-inducing and spectacular." },
            { title: "Lake Powell Overlook", description: "Crystal blue water in red desert — surreal. If time allows, consider a kayak rental at Antelope Point Marina." }
          ],
          meals: [
            { type: "Lunch", name: "Big John's Texas BBQ", description: "Surprisingly great barbecue in the middle of the Arizona desert. Brisket and pulled pork with desert views.", meta: "$$ · Page, AZ" },
            { type: "Dinner", name: "Rocking V Cafe", description: "Artsy café in Kanab (the gateway to Zion and Bryce). Farm-to-table in cowboy country.", meta: "$$ · Kanab, UT" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.8600, lng: -111.4225, label: "Cameron Trading Post", num: 1, cat: "attraction", desc: "Navajo crafts & fry bread" },
        { lat: 36.8791, lng: -111.5104, label: "Horseshoe Bend", num: 2, cat: "attraction", desc: "Iconic Colorado River viewpoint" },
        { lat: 36.9375, lng: -111.4859, label: "Lake Powell", num: 3, cat: "attraction", desc: "Desert reservoir" },
        { lat: 37.0475, lng: -112.5263, label: "Kanab", num: 4, cat: "neighborhood", desc: "Gateway town" }
      ]
    },
    {
      num: 18,
      date: "May 14",
      neighborhoods: "Road Trip · Kanab → Bryce Canyon → Salt Lake City",
      title: "Bryce Canyon & Push to Salt Lake City",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bryce Canyon National Park", description: "Quick detour (~1.5 hours from Kanab) to see the otherworldly hoodoo formations. Sunrise Point and the Navajo Loop Trail are must-dos. Budget 2-3 hours." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Drive to Salt Lake City", description: "~4 hour drive north on I-15 from Bryce Canyon to Salt Lake City. Stunning desert-to-mountain scenery the whole way." }
          ],
          meals: [
            { type: "Lunch", name: "Bryce Canyon Lodge", description: "Quick lunch at the historic lodge before hitting the road. Solid comfort food in a stunning setting.", meta: "$$ · Bryce Canyon" },
            { type: "Dinner", name: "Red Iguana", description: "Salt Lake City's most beloved Mexican restaurant. Seven different mole sauces and massive portions. Worth any wait.", meta: "$$ · Salt Lake City" }
          ]
        }
      ],
      mapPins: [
        { lat: 37.6283, lng: -112.1671, label: "Bryce Canyon", num: 1, cat: "attraction", desc: "Hoodoo wonderland" },
        { lat: 37.6321, lng: -112.1668, label: "Navajo Loop Trail", num: 2, cat: "attraction", desc: "Classic Bryce hike" },
        { lat: 40.7608, lng: -111.8910, label: "Salt Lake City", num: 3, cat: "neighborhood", desc: "Overnight stopover" },
        { lat: 40.7769, lng: -111.9130, label: "Red Iguana", num: 4, cat: "food", desc: "Famous mole restaurant" }
      ]
    },
    // ============ SLC STOPOVER: Day 19 (May 15) ============
    {
      num: 19,
      date: "May 15",
      neighborhoods: "Salt Lake City · Temple Square · Natural History",
      title: "Salt Lake City — Quick But Worthwhile",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Temple Square", description: "The heart of Salt Lake City. Even if you're not LDS, the architecture and gardens are beautiful, and the visitor center is interesting." },
            { title: "Natural History Museum of Utah", description: "Stunning modern building up in the foothills with world-class dinosaur and Native American exhibits. Great for all ages." }
          ],
          meals: [
            { type: "Lunch", name: "The Copper Onion", description: "One of SLC's best restaurants — seasonal American cuisine, great cocktails, lively atmosphere in the heart of downtown.", meta: "$$ · Downtown SLC" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Drive to West Yellowstone", description: "~5 hour drive north on I-15 to West Yellowstone, Montana — the western gateway to Yellowstone. Beautiful drive through Idaho." }
          ],
          meals: [
            { type: "Dinner", name: "Madison Crossing Lounge", description: "West Yellowstone's best restaurant. Montana elk burger, local trout, and craft cocktails in a cozy lodge atmosphere.", meta: "$$ · West Yellowstone, MT" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7706, lng: -111.8920, label: "Temple Square", num: 1, cat: "attraction", desc: "SLC landmark" },
        { lat: 40.7665, lng: -111.8231, label: "Natural History Museum", num: 2, cat: "attraction", desc: "Dinosaurs & Utah history" },
        { lat: 44.6621, lng: -111.1041, label: "West Yellowstone", num: 3, cat: "neighborhood", desc: "Gateway to Yellowstone" }
      ]
    },
    // ============ YELLOWSTONE: Days 20-23 (May 16-19) ============
    {
      num: 20,
      date: "May 16",
      neighborhoods: "Yellowstone · West Entrance · Upper Geyser Basin",
      title: "Yellowstone Day 1 — Old Faithful & Geysers",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Enter Yellowstone (West Entrance)", description: "Drive into the park via the West Entrance from West Yellowstone. The Madison River valley is gorgeous first thing in the morning — watch for elk and bison." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Old Faithful & Upper Geyser Basin", description: "Watch Old Faithful erupt (~every 90 minutes), then walk the boardwalk trail past Morning Glory Pool, Grand Geyser, and dozens of other thermal features. Budget 3-4 hours." },
            { title: "Grand Prismatic Spring Overlook", description: "The park's most photographed feature — a massive rainbow-colored hot spring. Take the Fairy Falls trailhead overlook for the best aerial view." }
          ],
          meals: [
            { type: "Lunch", name: "Old Faithful Inn Dining Room", description: "Eat inside the world's largest log structure. The building itself is as impressive as the food. Bison burgers recommended.", meta: "$$ · Old Faithful" },
            { type: "Dinner", name: "Cook at Your Cabin", description: "If staying in a cabin with a kitchen in West Yellowstone, cook a hearty meal after a long day. Stock up at the Food Roundup grocery store.", meta: "$ · Self-catered" }
          ]
        }
      ],
      mapPins: [
        { lat: 44.6510, lng: -110.8668, label: "West Entrance", num: 1, cat: "transport", desc: "Park entry" },
        { lat: 44.4605, lng: -110.8281, label: "Old Faithful", num: 2, cat: "attraction", desc: "World's most famous geyser" },
        { lat: 44.5251, lng: -110.8382, label: "Grand Prismatic Spring", num: 3, cat: "attraction", desc: "Rainbow hot spring" }
      ]
    },
    {
      num: 21,
      date: "May 17",
      neighborhoods: "Yellowstone · Lamar Valley · Tower-Roosevelt",
      title: "Yellowstone Day 2 — Wildlife Safari",
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            { title: "Lamar Valley Sunrise Safari", description: "Wake up EARLY (5am) and drive to Lamar Valley — the Serengeti of North America. Wolves, bison herds, grizzly bears, pronghorn. Bring binoculars and patience. Dawn is the magic hour." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Tower Fall & Petrified Tree", description: "Stop at Tower Fall for a quick hike to the waterfall viewpoint, then see the petrified tree — an ancient redwood turned to stone." },
            { title: "Mammoth Hot Springs", description: "Drive north to the terraced limestone formations at Mammoth. The mineral deposits create an ever-changing landscape of white and orange terraces." }
          ],
          meals: [
            { type: "Lunch", name: "Mammoth Hot Springs Hotel Dining Room", description: "Classic park lodge dining. Solid sandwiches and soups after a morning in the wild.", meta: "$$ · Mammoth" },
            { type: "Dinner", name: "Wild West Pizzeria", description: "Back in West Yellowstone for hand-tossed pizza and local microbrews. Great for refueling after a long wildlife day.", meta: "$$ · West Yellowstone" }
          ]
        }
      ],
      mapPins: [
        { lat: 44.8985, lng: -110.2281, label: "Lamar Valley", num: 1, cat: "attraction", desc: "Premier wildlife viewing" },
        { lat: 44.8925, lng: -110.3874, label: "Tower Fall", num: 2, cat: "attraction", desc: "Scenic waterfall" },
        { lat: 44.9735, lng: -110.7004, label: "Mammoth Hot Springs", num: 3, cat: "attraction", desc: "Terraced limestone formations" }
      ]
    },
    {
      num: 22,
      date: "May 18",
      neighborhoods: "Yellowstone · Canyon Village · Yellowstone Lake",
      title: "Yellowstone Day 3 — Grand Canyon of Yellowstone",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Grand Canyon of the Yellowstone", description: "The park's most dramatic scenery. Start at Artist Point for the classic view of Lower Falls — a 308-foot waterfall into a golden-walled canyon. Walk both the North and South Rim trails." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hayden Valley", description: "Drive through Hayden Valley between Canyon and the Lake — prime bison and grizzly territory. Drive slow and scan the meadows." },
            { title: "Yellowstone Lake & West Thumb", description: "The largest high-altitude lake in North America. Walk the West Thumb Geyser Basin where geysers bubble right into the lake." }
          ],
          meals: [
            { type: "Lunch", name: "Canyon Lodge Eatery", description: "Modern cafeteria-style dining with surprisingly good food — local trout, rotisserie chicken, and regional ingredients.", meta: "$$ · Canyon Village" },
            { type: "Dinner", name: "Lake Yellowstone Hotel Dining Room", description: "Elegant lakeside dining in a 1920s hotel. White tablecloths, sunset views, and fresh fish. The fanciest dinner in the park.", meta: "$$$ · Lake Village" }
          ]
        }
      ],
      mapPins: [
        { lat: 44.7198, lng: -110.4876, label: "Artist Point / Lower Falls", num: 1, cat: "attraction", desc: "Iconic canyon viewpoint" },
        { lat: 44.6500, lng: -110.4500, label: "Hayden Valley", num: 2, cat: "attraction", desc: "Wildlife watching" },
        { lat: 44.4154, lng: -110.5727, label: "West Thumb Geyser Basin", num: 3, cat: "attraction", desc: "Geysers meet the lake" },
        { lat: 44.5524, lng: -110.3973, label: "Lake Yellowstone Hotel", num: 4, cat: "food", desc: "Elegant lakeside dining" }
      ]
    },
    {
      num: 23,
      date: "May 19",
      neighborhoods: "Yellowstone · Norris · Firehole River",
      title: "Yellowstone Day 4 — Hidden Gems & Farewell",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Norris Geyser Basin", description: "The hottest and most dynamic thermal area in the park. Steamboat Geyser (world's tallest active geyser) lives here. The Back Basin loop is otherworldly." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Firehole River Swimming Area", description: "One of Yellowstone's best-kept secrets — a natural warm swimming hole where hot springs heat the river. Perfect on a warm May afternoon." },
            { title: "Last Look at Old Faithful", description: "Circle back for one more eruption. Say goodbye to the park the way you arrived — in awe." }
          ],
          meals: [
            { type: "Lunch", name: "Geyser Grill", description: "Quick-service spot near Old Faithful. Grab burgers and milkshakes before hitting the road.", meta: "$ · Old Faithful" },
            { type: "Dinner", name: "Firehole Bar & Grill", description: "Last dinner in West Yellowstone. Montana steaks, local beers, and stories from the road.", meta: "$$ · West Yellowstone" }
          ]
        }
      ],
      mapPins: [
        { lat: 44.7262, lng: -110.7036, label: "Norris Geyser Basin", num: 1, cat: "attraction", desc: "Hottest thermal area" },
        { lat: 44.6329, lng: -110.8564, label: "Firehole Swimming Area", num: 2, cat: "attraction", desc: "Warm river swimming" },
        { lat: 44.4605, lng: -110.8281, label: "Old Faithful (Farewell)", num: 3, cat: "attraction", desc: "One last eruption" }
      ]
    },
    // ============ RETURN TO SLC & FLY TO CHICAGO: Days 24-25 (May 20-21) ============
    {
      num: 24,
      date: "May 20",
      neighborhoods: "Road Trip · Yellowstone → Salt Lake City",
      title: "Yellowstone to Salt Lake City",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Salt Lake City", description: "~5 hour drive south back to SLC through Idaho. Enjoy the open road and reflect on an incredible few days in the wild." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Return Rental Car & Relax", description: "Return the rental car near the airport or downtown. Take the afternoon to rest, do laundry, and repack for the final leg of the trip." }
          ],
          meals: [
            { type: "Lunch", name: "Lucky 13 Bar & Grill", description: "SLC's best burgers — seriously. The Celestial Burger is legendary. Casual, fun, great patio.", meta: "$$ · Downtown SLC" },
            { type: "Dinner", name: "Takashi", description: "Surprisingly outstanding sushi in landlocked Utah. Fresh fish flown in daily, creative rolls, and excellent sake selection.", meta: "$$$ · Downtown SLC" }
          ]
        }
      ],
      mapPins: [
        { lat: 40.7608, lng: -111.8910, label: "Salt Lake City", num: 1, cat: "neighborhood", desc: "Return to SLC" },
        { lat: 40.7543, lng: -111.8997, label: "Lucky 13", num: 2, cat: "food", desc: "Best burgers in SLC" },
        { lat: 40.7608, lng: -111.8870, label: "Takashi", num: 3, cat: "food", desc: "Outstanding sushi" }
      ]
    },
    {
      num: 25,
      date: "May 21",
      neighborhoods: "Transit · Salt Lake City → Chicago",
      title: "Fly to the Windy City",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Fly SLC → Chicago", description: "Catch a morning flight from SLC to Chicago O'Hare or Midway (~3.5 hours). Check into your hotel/Airbnb — downtown or Wicker Park areas recommended for food access." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Millennium Park & The Bean", description: "Start your Chicago adventure at the iconic Cloud Gate ('The Bean'). Walk through the beautiful park, check out the Crown Fountain, and enjoy the skyline views." }
          ],
          meals: [
            { type: "Lunch", name: "Portillo's", description: "Chicago institution. Italian beef (dipped, with hot giardiniera) is mandatory. This is Chicago in sandwich form.", meta: "$ · Multiple locations" },
            { type: "Dinner", name: "Girl & The Goat", description: "Stephanie Izard's flagship and one of Chicago's most exciting restaurants. Creative, bold, shareable plates. Reservations essential.", meta: "$$$ · West Loop" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8827, lng: -87.6233, label: "Millennium Park / The Bean", num: 1, cat: "attraction", desc: "Chicago's iconic sculpture" },
        { lat: 41.8841, lng: -87.6507, label: "Girl & The Goat", num: 2, cat: "food", desc: "Award-winning restaurant" },
        { lat: 41.8796, lng: -87.6341, label: "Portillo's", num: 3, cat: "food", desc: "Chicago Italian beef" }
      ]
    },
    // ============ CHICAGO: Days 26-31 (May 22-27) ============
    {
      num: 26,
      date: "May 22",
      neighborhoods: "Chicago · Architecture · River North",
      title: "Chicago Architecture & Deep Dish",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Chicago Architecture Boat Tour", description: "THE must-do Chicago experience. A 90-minute cruise down the Chicago River learning about the world's most impressive skyline. Book Chicago Architecture Center's tour." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Art Institute of Chicago", description: "One of the world's great art museums. Grant Wood's 'American Gothic', Seurat's 'Sunday Afternoon', Hopper's 'Nighthawks' — they're all here. Budget 3+ hours." }
          ],
          meals: [
            { type: "Lunch", name: "Lou Malnati's", description: "The deep-dish debate is eternal, but Lou Malnati's buttery crust wins many hearts. Get the Malnati Chicago Classic.", meta: "$$ · Multiple locations" },
            { type: "Dinner", name: "Frontera Grill", description: "Rick Bayless's Mexican masterpiece. Authentic, seasonal, and endlessly creative. The moles alone are worth the trip.", meta: "$$$ · River North" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8882, lng: -87.6218, label: "Chicago Riverwalk", num: 1, cat: "attraction", desc: "Architecture boat tour departure" },
        { lat: 41.8796, lng: -87.6237, label: "Art Institute of Chicago", num: 2, cat: "attraction", desc: "World-class art museum" },
        { lat: 41.8901, lng: -87.6338, label: "Lou Malnati's", num: 3, cat: "food", desc: "Chicago deep-dish legend" },
        { lat: 41.8906, lng: -87.6310, label: "Frontera Grill", num: 4, cat: "food", desc: "Rick Bayless Mexican" }
      ]
    },
    {
      num: 27,
      date: "May 23",
      neighborhoods: "Chicago · West Loop · Pilsen",
      title: "West Loop Food Tour & Pilsen Murals",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "West Loop / Randolph Street", description: "Chicago's restaurant row. Even just walking Randolph Street in the morning, the aromas and energy are incredible. This is where Chicago's food revolution lives." }
          ],
          meals: [
            { type: "Brunch", name: "Au Cheval", description: "The double cheeseburger here is regularly called the best burger in America. Also serve a perfect egg-topped single. Expect a serious wait.", meta: "$$$ · West Loop" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Pilsen", description: "Chicago's vibrant Mexican-American neighborhood. Incredible murals everywhere, the National Museum of Mexican Art (free!), and some of the city's best tacos." }
          ],
          meals: [
            { type: "Lunch", name: "Birriería Zaragoza", description: "James Beard Award-winning birria. Rich, complex, soul-warming goat stew that's worth traveling across the city for.", meta: "$$ · Pilsen" },
            { type: "Dinner", name: "Alinea", description: "If budget allows, this is a once-in-a-lifetime 3-Michelin-star experience. Multi-course tasting menu that redefines what food can be. Reserve weeks ahead.", meta: "$$$$ · Lincoln Park" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8841, lng: -87.6485, label: "Au Cheval", num: 1, cat: "food", desc: "Best burger in America" },
        { lat: 41.8565, lng: -87.6722, label: "Pilsen", num: 2, cat: "neighborhood", desc: "Murals & Mexican culture" },
        { lat: 41.8555, lng: -87.6717, label: "National Museum of Mexican Art", num: 3, cat: "attraction", desc: "Free museum" },
        { lat: 41.9133, lng: -87.6535, label: "Alinea", num: 4, cat: "food", desc: "3 Michelin stars" }
      ]
    },
    {
      num: 28,
      date: "May 24",
      neighborhoods: "Chicago · Lincoln Park · Wrigleyville",
      title: "Lincoln Park, Zoo & Cubs Game",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Lincoln Park Zoo", description: "Free! One of the last free zoos in America. Walk the beautiful grounds, see the big cats, and enjoy the Lincoln Park Conservatory next door." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Wrigley Field", description: "Even if there's no game, walk the neighborhood — Wrigleyville is quintessential Chicago. If the Cubs are playing, grab cheap bleacher seats for the full experience." }
          ],
          meals: [
            { type: "Lunch", name: "Wieners Circle", description: "Famous (infamous?) hot dog stand in Lincoln Park. Great Chicago-style dogs, and the staff will roast you for free. A true Chicago experience.", meta: "$ · Lincoln Park" },
            { type: "Dinner", name: "Smoque BBQ", description: "Best BBQ in Chicago, no contest. Texas-style brisket, ribs, and pulled pork. The brisket is next level.", meta: "$$ · Irving Park" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.9211, lng: -87.6340, label: "Lincoln Park Zoo", num: 1, cat: "attraction", desc: "Free zoo" },
        { lat: 41.9484, lng: -87.6553, label: "Wrigley Field", num: 2, cat: "attraction", desc: "Iconic baseball stadium" },
        { lat: 41.9210, lng: -87.6363, label: "Wieners Circle", num: 3, cat: "food", desc: "Infamous hot dog stand" },
        { lat: 41.9535, lng: -87.6793, label: "Smoque BBQ", num: 4, cat: "food", desc: "Best BBQ in Chicago" }
      ]
    },
    {
      num: 29,
      date: "May 25",
      neighborhoods: "Chicago · Hyde Park · South Side",
      title: "Hyde Park & Obama's Chicago",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Museum of Science and Industry", description: "The largest science museum in the Western Hemisphere. The U-505 submarine exhibit, the Coal Mine, and the Mirror Maze are highlights. Budget half a day." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "University of Chicago Campus", description: "Beautiful Gothic campus rivaling Yale. Walk the main quad, see Rockefeller Chapel, and browse Seminary Co-op Bookstore." },
            { title: "Obama Presidential Center (Under Construction)", description: "Drive by the site of the future Obama Presidential Center in Jackson Park. The neighborhood is buzzing with anticipation." }
          ],
          meals: [
            { type: "Lunch", name: "Valois", description: "Hyde Park's iconic cafeteria — 'See Your Food.' Obama's regular breakfast spot. Classic diner food, real community.", meta: "$ · Hyde Park" },
            { type: "Dinner", name: "Virtue Restaurant", description: "Southern-inspired fine dining in Hyde Park. Cornbread, smothered pork chops, and bourbon cocktails in a gorgeous space.", meta: "$$$ · Hyde Park" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.7906, lng: -87.5831, label: "Museum of Science & Industry", num: 1, cat: "attraction", desc: "Massive science museum" },
        { lat: 41.7886, lng: -87.5988, label: "University of Chicago", num: 2, cat: "attraction", desc: "Gothic campus" },
        { lat: 41.7870, lng: -87.6005, label: "Valois", num: 3, cat: "food", desc: "Obama's breakfast spot" },
        { lat: 41.7935, lng: -87.5970, label: "Virtue Restaurant", num: 4, cat: "food", desc: "Southern fine dining" }
      ]
    },
    {
      num: 30,
      date: "May 26",
      neighborhoods: "Chicago · Navy Pier · Magnificent Mile",
      title: "Lakefront & Shopping Spree",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Lakefront Trail & Navy Pier", description: "Walk or bike the gorgeous Lakefront Trail. Stop at Navy Pier for the Centennial Wheel and lake views. Skip the tourist traps inside — the outdoor views are the attraction." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Magnificent Mile Shopping", description: "Michigan Avenue's legendary shopping strip. Nike, Nordstrom, Apple, and plenty of unique boutiques. Great for souvenirs and gifts." }
          ],
          meals: [
            { type: "Lunch", name: "Eataly Chicago", description: "Mario Batali's Italian marketplace. Browse, graze, sit down — there are multiple restaurants inside plus incredible grocery shopping.", meta: "$$ · River North" },
            { type: "Dinner", name: "RPM Italian", description: "Celebrity-backed Italian with a scene. Great pasta, great steaks, great people-watching. Reserve ahead.", meta: "$$$ · River North" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.8917, lng: -87.6063, label: "Navy Pier", num: 1, cat: "attraction", desc: "Lakefront landmark" },
        { lat: 41.8952, lng: -87.6244, label: "Magnificent Mile", num: 2, cat: "attraction", desc: "Premier shopping" },
        { lat: 41.8897, lng: -87.6175, label: "Eataly Chicago", num: 3, cat: "food", desc: "Italian food marketplace" },
        { lat: 41.8907, lng: -87.6292, label: "RPM Italian", num: 4, cat: "food", desc: "Upscale Italian dining" }
      ]
    },
    {
      num: 31,
      date: "May 27",
      neighborhoods: "Chicago · Wicker Park · Logan Square",
      title: "Last Day — Neighborhood Hopping",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Wicker Park & Bucktown", description: "Chicago's indie-cool neighborhoods. Vintage shopping, record stores, local boutiques, and excellent coffee. The Six Corners intersection is the heart of it." }
          ],
          meals: [
            { type: "Brunch", name: "Big Star", description: "Rick Bayless protégé's taco joint. Incredible tacos al pastor on the patio with a whiskey cocktail. Weekend brunch is a Chicago institution.", meta: "$$ · Wicker Park" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Logan Square", description: "The neighborhood that's been 'up and coming' for 10 years and is now fully arrived. Great bars, restaurants, and the beautiful Logan Square boulevard." }
          ],
          meals: [
            { type: "Lunch", name: "Fat Rice", description: "Macanese-inspired cuisine that's unlike anything else in Chicago. The arroz gordo (fat rice) is a must. Unique and unforgettable.", meta: "$$ · Logan Square" }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Dinner", description: "Last night of an epic 31-day journey across America. Pick your favorite spot from the trip, or try somewhere new — Chicago's got endless options." }
          ],
          meals: [
            { type: "Dinner", name: "Joe's Seafood, Prime Steak & Stone Crab", description: "Perfect farewell dinner. Elegant but not stuffy, with incredible stone crab claws and prime steaks. A celebration-worthy finale.", meta: "$$$$ · River North" }
          ]
        }
      ],
      mapPins: [
        { lat: 41.9088, lng: -87.6776, label: "Wicker Park", num: 1, cat: "neighborhood", desc: "Indie shopping & dining" },
        { lat: 41.9088, lng: -87.6776, label: "Big Star", num: 2, cat: "food", desc: "Legendary taco joint" },
        { lat: 41.9234, lng: -87.7013, label: "Logan Square", num: 3, cat: "neighborhood", desc: "Trendy neighborhood" },
        { lat: 41.8916, lng: -87.6266, label: "Joe's Seafood", num: 4, cat: "food", desc: "Farewell celebration dinner" }
      ]
    }
  ],
  budgetTable: [
    { item: "Flights (per person)", low: "$400", high: "$800", notes: "Boston in, Chicago out, + Vegas/SLC legs" },
    { item: "Rental Car (12 days)", low: "$600", high: "$1,000", notes: "SUV for 5+ people, Vegas→SLC" },
    { item: "Gas", low: "$150", high: "$250", notes: "~1,800 miles of driving" },
    { item: "Hotels/Airbnb (30 nights)", low: "$2,000", high: "$4,500", notes: "Split among 5+ people" },
    { item: "National Park Passes", low: "$35", high: "$80", notes: "America the Beautiful pass = $80 for all parks" },
    { item: "Food & Drink (per person)", low: "$1,500", high: "$3,000", notes: "Mix of casual & splurge meals" },
    { item: "Activities & Attractions", low: "$200", high: "$500", notes: "Museums, tours, boat rides" },
    { item: "TOTAL per person", low: "$2,400", high: "$5,000", notes: "Varies by accommodation choices" }
  ],
  practicalInfo: [
    { title: "Transportation Strategy", items: ["Fly into Boston, train Boston→NYC, train NYC→New Haven, fly New Haven→Vegas, rent car Vegas→SLC (return SLC), fly SLC→Chicago, fly out of Chicago.", "The rental car is only needed for the Western road trip leg (12 days)."] },
    { title: "Packing", items: ["Light layers for the East Coast (55-70°F)", "Sun protection and shorts for the Southwest (85-100°F)", "Warm layers and rain gear for Yellowstone (40-60°F)", "Comfortable walking shoes — you'll average 10,000+ steps daily"] },
    { title: "Reservations to Book ASAP", items: ["Yellowstone lodging (Old Faithful Inn or West Yellowstone cabins)", "El Tovar Dining Room (Grand Canyon)", "Alinea (Chicago) — weeks ahead", "Girl & The Goat (Chicago)", "Peter Luger (NYC) — cash only"] },
    { title: "National Parks", items: ["Buy an America the Beautiful Annual Pass ($80) — covers Grand Canyon, Bryce Canyon, and Yellowstone entrance fees", "One pass covers a whole carload of people"] },
    { title: "Graduation Tips", items: ["Arrive 60-90 minutes early for good seating at all three ceremonies", "Bring a portable charger for photos/video", "Have a restaurant reservation ready for the celebration dinner"] }
  ]
};

// Run fulfillment
fulfillOrder(order, itineraryData);
