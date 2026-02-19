const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771459341095_71r41l",
  email: "bernard.j.huang@gmail.com",
  destination: "Boston, MA, USA",
  start_date: "2026-07-22",
  end_date: "2026-07-26",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "$1,000-2,000",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-19T00:02:21.095Z",
  status: "pending"
};

const itineraryData = {
  destination: "Boston, MA, USA",
  countryEmoji: "🇺🇸",
  title: "Boston in 4 Nights: History, Seafood & Harbor Sunsets",
  subtitle: "Freedom Trail → North End → Cambridge → Seaport → Back Bay",
  description: "A couple's guide to Boston in peak summer — America's most walkable city where cobblestone history meets world-class seafood, craft cocktails in converted warehouses, and golden-hour harbor walks. July means warm evenings on waterfront patios, free outdoor concerts, and sailboats on the Charles.",
  duration: "4 nights / 5 days",
  dates: "Jul 22 – 26, 2026",
  budget: "$1,000–2,000",
  pace: "Balanced — mornings exploring, afternoons flexible, evenings out",
  bestFor: "Couples, history buffs & seafood lovers",
  highlights: [
    "Freedom Trail — 2.5 miles of American Revolution history",
    "North End — Boston's Little Italy, the best cannoli debate",
    "Boston Harbor sunset from the Seaport District",
    "Harvard & MIT campus strolls in Cambridge",
    "Fresh lobster rolls on the waterfront",
    "Boston Common & Public Garden — swan boats in summer",
    "Fenway Park — catch a Red Sox game",
    "Charles River Esplanade — kayaking & sunset walks",
    "Isabella Stewart Gardner Museum — art in a Venetian palace",
    "Craft cocktails in speakeasy-style bars"
  ],
  essentials: [
    { title: "🚇 Getting Around", text: "The T (MBTA subway) covers most areas — get a CharlieCard at any station. Boston is incredibly walkable: most attractions are within 20-30 minutes on foot. For Cambridge, take the Red Line. Water taxis are fun and practical for Seaport ↔ North End. Skip rental cars — parking is expensive and stressful." },
    { title: "💵 Budget Tips", text: "Expect $15-25 for casual lunches, $40-70pp for nice dinners. Happy hours (4-6pm) are excellent — especially in the Seaport. Lobster rolls run $22-35. Many museums have discount days. Street parking is nearly impossible; if driving, budget $30-50/day for garages." },
    { title: "☀️ July Weather", text: "Warm and humid — expect 80-90°F (27-32°C) with occasional heat waves. Evenings cool to mid-70s, perfect for outdoor dining. Afternoon thunderstorms are possible but brief. Pack sunscreen, sunglasses, and comfortable walking shoes. Light layers for over-air-conditioned restaurants." },
    { title: "🏨 Where to Stay", text: "Back Bay for classic Boston (Newbury Street shopping, Public Garden walks). Seaport for modern waterfront vibes. North End for being steps from the best food. Cambridge for a quieter, college-town feel. Budget pick: look at hotels near South Station or the Waterfront." },
    { title: "🦞 Seafood Rules", text: "Boston takes seafood seriously. Lobster rolls come two ways: Connecticut-style (warm, buttered) and Maine-style (cold, mayo). Try both and pick a side. Clam chowder should be creamy, never thin. Oyster happy hours are everywhere in summer. Don't sleep on the fried clams." },
    { title: "📱 Useful Apps", text: "MBTA (subway/bus tracker), Resy & OpenTable (restaurant reservations — book ahead for popular spots), AllTrails (harbor walks), Uber/Lyft (for Cambridge trips at night)." }
  ],
  days: [
    {
      num: 1,
      title: "Freedom Trail, North End & Italian Feast",
      neighborhoods: "Downtown · Beacon Hill · North End",
      date: "Jul 22",
      mapPins: [
        { lat: 42.3541, lng: -71.0655, label: "Boston Common", num: 1, cat: "activity", desc: "America's oldest public park — start here" },
        { lat: 42.3588, lng: -71.0636, label: "Public Garden & Swan Boats", num: 2, cat: "activity", desc: "Victorian garden with iconic swan boat rides" },
        { lat: 42.3581, lng: -71.0636, label: "Beacon Hill", num: 3, cat: "activity", desc: "Cobblestone streets and gas-lit lamps" },
        { lat: 42.3601, lng: -71.0549, label: "Faneuil Hall & Quincy Market", num: 4, cat: "food", desc: "Historic marketplace and food hall" },
        { lat: 42.3641, lng: -71.0542, label: "Paul Revere House", num: 5, cat: "activity", desc: "Oldest remaining structure in downtown Boston" },
        { lat: 42.3647, lng: -71.0542, label: "North End", num: 6, cat: "food", desc: "Boston's Little Italy — legendary restaurants" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Boston Common & Public Garden", description: "Start at America's oldest public park. Walk through Boston Common to the adjacent Public Garden — in summer, the gardens are in full bloom and the famous Swan Boats glide across the lagoon. A perfect, romantic start to the trip.", details: ["📍 Swan Boat rides: $4.50pp, open 10am-4pm in summer", "💡 The Make Way for Ducklings statues in the Public Garden are iconic — find them near the pond."] },
            { title: "Beacon Hill Stroll", description: "Walk up to Beacon Hill — Boston's most photogenic neighborhood. Acorn Street (the most photographed street in America) has cobblestones and Federal-era brick row houses. Gas-lit Louisburg Square is where old money lives. Every corner is a photo op.", details: ["📍 Acorn Street is tiny — off Cedar Street between Willow and West Cedar"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Tatte Bakery & Café (Charles Street)", description: "Israeli-inspired bakery on Beacon Hill's charming Charles Street. Flaky shakshuka pastries, perfect lattes, and the halva cruffin is unforgettable. Sunny patio seating in summer.", meta: "$14-22pp · 70 Charles St · Walk-in, arrive by 9am on weekdays" }
          ],
          tips: [{ type: "tip", text: "Charles Street in Beacon Hill is lined with antique shops, independent bookstores, and cute cafés. Worth a slow browse — it's one of the most charming streets in America." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Freedom Trail (Northern Half)", description: "Pick up the red-brick Freedom Trail line at Boston Common and follow it through downtown. Hit the key stops: Old South Meeting House, Old State House (site of the Boston Massacre), Faneuil Hall. You don't need to do all 16 stops — cherry-pick the ones that interest you.", details: ["📍 The trail is a red line painted/bricked into the sidewalk — just follow it", "💡 Skip the guided tours and go at your own pace. Download the free Freedom Trail app for audio at each stop."] },
            { title: "Paul Revere House & Old North Church", description: "Continue the trail into the North End. Paul Revere's House (c. 1680) is the oldest remaining structure in downtown Boston. A few blocks away, Old North Church is where the 'one if by land, two if by sea' lanterns were hung. Both are quick visits with huge historical weight.", details: ["📍 Paul Revere House: $6 adults · Old North Church: $5 suggested donation"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Quincy Market / Faneuil Hall", description: "The historic Quincy Market food hall is touristy but fun for a quick bite — grab a lobster roll from one of the stands, New England clam chowder in a bread bowl, or just browse. Good for a casual first taste of Boston seafood.", meta: "$15-25pp · Faneuil Hall Marketplace · No reservations needed" }
          ],
          tips: [{ type: "reddit", text: "Quincy Market is overpriced but worth walking through once. For actual good food, save your appetite for the North End — it's a 10-minute walk away and 10x better.", cite: "r/boston" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "North End Stroll & Dinner", description: "The North End is Boston's Little Italy and the city's best food neighborhood. Hanover Street is the main drag — lined with Italian restaurants, bakeries, and cafés with sidewalk seating. In summer, the neighborhood comes alive with street festivals and outdoor dining. Just wander and soak it in.", details: ["💡 Make dinner reservations — the best spots fill up on summer evenings."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Giacomo's Ristorante", description: "Cash-only, no-reservations legend that's been packing people in for decades. Tiny space, huge portions of incredible Italian. The lobster fra diavolo and pumpkin ravioli are legendary. Come early or expect a line — it's worth the wait.", meta: "$30-45pp · 355 Hanover St · Cash only, no reservations, line starts by 5pm" }
          ],
          tips: [{ type: "reddit", text: "The great North End cannoli debate: Mike's Pastry (bigger, more famous, tourist line) vs Modern Pastry (locals' choice, better cannoli, no line). Get one from each and decide for yourselves. This is a required couples activity in Boston.", cite: "r/boston" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Cannoli Walk & Harbor Night Stroll", description: "Grab cannoli from Mike's Pastry AND Modern Pastry (they're across the street from each other — you must try both). Walk down to the waterfront with your cannoli. The harbor at night is peaceful, with city lights reflecting off the water. End the night at the North End park along the Greenway.", details: ["💡 Mike's: the ricotta cannoli is classic. Modern: try the pistachio. Both are excellent."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Cambridge, Harvard, MIT & Charles River",
      neighborhoods: "Cambridge · Harvard Square · Kendall Square · Charles River",
      date: "Jul 23",
      mapPins: [
        { lat: 42.3736, lng: -71.1189, label: "Harvard Yard", num: 1, cat: "activity", desc: "Walk the historic campus and rub the Statue of Three Lies" },
        { lat: 42.3727, lng: -71.1209, label: "Harvard Square", num: 2, cat: "food", desc: "Bookshops, buskers, and college-town energy" },
        { lat: 42.3601, lng: -71.0942, label: "MIT Campus", num: 3, cat: "activity", desc: "Starchitect buildings and the infinite corridor" },
        { lat: 42.3571, lng: -71.0870, label: "Charles River Esplanade", num: 4, cat: "activity", desc: "Kayaking, sailing, and sunset views" },
        { lat: 42.3516, lng: -71.0740, label: "Hatch Shell", num: 5, cat: "activity", desc: "Free outdoor concerts in summer" },
        { lat: 42.3625, lng: -71.0812, label: "Kendall Square", num: 6, cat: "food", desc: "Boston's tech hub — great restaurants" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Harvard Yard & Campus", description: "Take the Red Line to Harvard Square and walk through Harvard Yard. The campus is stunning — 400 years of American history in ivy-covered brick. Rub the foot of the John Harvard statue for good luck (everyone does, the foot is shiny gold). Peek into Widener Library and wander the old dormitories.", details: ["📍 Harvard T stop (Red Line) — campus is right there", "💡 Free student-led campus tours run daily — check the admissions office schedule. They're entertaining and full of Harvard lore."] },
            { title: "Harvard Square Browsing", description: "Harvard Square is one of America's great college-town neighborhoods. Browse Harvard Book Store (new, used, and remainders — excellent curated selection), check out The Coop, and people-watch from a café. Buskers and street performers are everywhere in summer.", details: ["💡 Harvard Book Store has a book-printing machine that prints any of millions of titles on demand. Nerdy and cool."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Mamaleh's Delicatessen", description: "Modern Jewish deli in Cambridge that's been getting national attention. The smoked salmon bagel is perfect, the babka is outrageous, and the egg creams are the real deal. Bright, fun space.", meta: "$16-24pp · Cambridge (Kendall Sq area) · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Harvard Square has an overwhelming number of bookshops. If you love books, budget extra time — Harvard Book Store, Grolier Poetry Book Shop (oldest poetry-only bookshop in the US), and Raven Used Books are all within walking distance." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "MIT Campus Walk", description: "Walk (or take 1 stop on the Red Line) from Harvard to MIT. The campus is a showcase of modern architecture — Frank Gehry's Stata Center looks like crumpled metal, the MIT Chapel by Saarinen is beautiful, and the Great Dome anchors it all. Very different vibe from Harvard's ivy-covered tradition.", details: ["📍 Kendall/MIT T stop (Red Line)", "💡 The 'Infinite Corridor' inside Building 7 is a 251m hallway that aligns with the sunset twice a year (MIThenge). The lobby is open to visitors."] },
            { title: "Charles River Kayaking", description: "Rent kayaks or stand-up paddleboards on the Charles River. Paddle between Boston and Cambridge with the skyline on one side and the campus on the other. In July, the river is calm and warm. It's one of the most romantic things you can do in Boston.", details: ["📍 Community Boating (Boston side) or Paddle Boston (Cambridge side)", "💡 Paddle Boston at Kendall Square: single kayak ~$25/hr, tandem ~$30/hr. Late afternoon light is magical."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Mr. Bartley's Burger Cottage", description: "Harvard Square institution since 1960. Famous for creative burgers named after celebrities and politicians. Cash only, packed, loud, and full of character. The burgers are enormous and excellent.", meta: "$18-25pp · Harvard Square · Cash only, walk-in" }
          ],
          tips: [{ type: "reddit", text: "Charles River kayaking on a summer evening is one of the most underrated Boston experiences. The skyline at sunset from the water is incredible. Go between 5-7pm for the best light.", cite: "r/boston" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Charles River Esplanade Sunset", description: "Walk along the Esplanade on the Boston side of the Charles. In summer, there are often free concerts at the Hatch Shell, and the pathway is full of runners, cyclists, and couples enjoying the warm evening. Watch the sunset over the river with the Cambridge skyline beyond.", details: ["📍 Access from Back Bay — walk across the Arthur Fiedler Footbridge"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Giulia", description: "Intimate, candlelit Italian restaurant in Harvard Square. Hand-made pasta that rivals the North End — the tagliatelle bolognese is extraordinary. Small, romantic, and beloved by locals. Book ahead.", meta: "$45-65pp · Harvard Square · Reservations essential on Resy" }
          ],
          tips: [{ type: "tip", text: "If Giulia is booked, try Alden & Harlow (creative American, great cocktails) or Pammy's (Italian-American, also romantic) — both in Harvard Square and both excellent for date night." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Drinks in Cambridge", description: "The Hourly Oyster House has a great bar scene and late-night oyster specials. Brick & Mortar is a cozy cocktail bar with dim lighting and creative drinks. Cambridge nightlife is more low-key than downtown Boston — perfect for couples.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Seaport, Museums & Fenway Night",
      neighborhoods: "Seaport · Fort Point · Back Bay · Fenway",
      date: "Jul 24",
      mapPins: [
        { lat: 42.3519, lng: -71.0451, label: "Seaport District", num: 1, cat: "activity", desc: "Boston's newest waterfront neighborhood" },
        { lat: 42.3518, lng: -71.0496, label: "Institute of Contemporary Art", num: 2, cat: "activity", desc: "Stunning harbor-front museum with free Thursdays" },
        { lat: 42.3384, lng: -71.0962, label: "Isabella Stewart Gardner Museum", num: 3, cat: "activity", desc: "Art collection in a Venetian-style palazzo" },
        { lat: 42.3467, lng: -71.0972, label: "Fenway Park", num: 4, cat: "activity", desc: "America's oldest ballpark — catch a Red Sox game" },
        { lat: 42.3502, lng: -71.0770, label: "Newbury Street", num: 5, cat: "food", desc: "Boston's premier shopping and dining street" },
        { lat: 42.3497, lng: -71.0466, label: "Row 34", num: 6, cat: "food", desc: "Exceptional oyster bar in the Seaport" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Seaport District & ICA", description: "Walk through the Seaport — Boston's most modern neighborhood, all glass and steel on the waterfront. The Institute of Contemporary Art (ICA) is architecturally stunning, cantilevered over the harbor. The collection is excellent and the harbor views from inside are worth the visit alone.", details: ["📍 ICA: $20 adults, free Thursdays 5-9pm · The mediatheque (free viewing room with harbor views) is open to all", "💡 The ICA's outdoor terrace overlooking the harbor is one of the best views in Boston. Bring coffee and sit."] },
            { title: "Fort Point Channel Walk", description: "Walk along Fort Point Channel — the old industrial waterfront converted into artist studios and restaurants. The painted buildings, working artists, and waterfront path have a great vibe. Boston Tea Party Ships & Museum is here too if you want a fun, interactive history experience.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Flour Bakery + Cafe (Fort Point)", description: "Joanne Chang's beloved Boston bakery chain started here. The sticky buns are legendary (they beat Bobby Flay's on Throwdown), the egg sandwiches are perfect, and the coffee is excellent. Bright, welcoming space.", meta: "$12-18pp · Fort Point · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Flour Bakery's sticky bun is genuinely one of the best things you'll eat in Boston. Get there before 10am — they sell out. The Fort Point location is the original and has the best vibe.", cite: "r/boston" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Isabella Stewart Gardner Museum", description: "One of the most unique museums in the world. Isabella Gardner built a Venetian palazzo in Boston and filled it with her personal art collection — Rembrandts, Sargents, Titians — arranged exactly as she specified, forever. The central courtyard is filled with flowers and light. Deeply romantic.", details: ["📍 25 Evans Way · $20 adults · Anyone named 'Isabella' gets in free (forever, per her will)", "💡 The empty frames from the 1990 art heist (largest in history, $500M+ in stolen art) are still on the walls. Haunting and fascinating."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Row 34", description: "The Seaport's best restaurant — an industrial-chic oyster bar and craft beer hall in a converted warehouse. The raw bar is exceptional: get a dozen oysters, littleneck clams, and a crisp white wine. The lobster roll (warm, buttered) is one of the city's best.", meta: "$35-50pp · Fort Point · Reservations recommended on Resy" }
          ],
          tips: [{ type: "tip", text: "The Gardner Museum courtyard is genuinely breathtaking. Even if you're not a museum person, the building itself — a Venetian palace transplanted to Boston — is worth the visit." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Fenway Park — Red Sox Game", description: "Catch the Red Sox at Fenway Park, America's oldest ballpark (1912). The Green Monster, Pesky's Pole, hand-operated scoreboard — it's baseball the way it was meant to be. A summer night game at Fenway is pure magic. Even if you don't follow baseball, the atmosphere is electric.", details: ["📍 Check Red Sox schedule for Jul 24 game times — buy tickets on MLB.com or StubHub", "💡 Bleacher seats are cheapest ($20-40) and have the best atmosphere. Grandstand along the 3rd base line gives great views. Fenway Franks are mandatory."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Eastern Standard (pre-game)", description: "Classic Boston brasserie near Fenway. Great cocktails, raw bar, and French-American bistro food. Perfect pre-game dinner — it's a 5-minute walk to the park. The burger and oyster platter are both excellent.", meta: "$40-55pp · Kenmore Square · Reservations recommended for game nights" }
          ],
          tips: [{ type: "reddit", text: "Go to Fenway early. Gates open 90 minutes before first pitch. Walk around the entire park, check out the retired numbers on the facade, stand behind the Green Monster. Get a Fenway Frank and a beer. Baseball doesn't get better than this.", cite: "r/redsox" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Kenmore Square & Fenway Bars", description: "Post-game Kenmore Square is lively. The Hawthorne (craft cocktails in a beautiful space) is nearby. Bleacher Bar (literally built into the center field wall of Fenway, with a window looking onto the field) is an iconic post-game spot.", details: ["💡 Bleacher Bar has a view INTO Fenway through a garage door behind center field. Wild. It gets packed after games — go early or wait it out."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Back Bay, Waterfront & Sunset Sail",
      neighborhoods: "Back Bay · South End · Waterfront",
      date: "Jul 25",
      mapPins: [
        { lat: 42.3493, lng: -71.0783, label: "Newbury Street", num: 1, cat: "activity", desc: "Eight blocks of shopping, galleries, and sidewalk cafés" },
        { lat: 42.3496, lng: -71.0823, label: "Copley Square", num: 2, cat: "activity", desc: "Boston Public Library and Trinity Church" },
        { lat: 42.3468, lng: -71.0818, label: "South End", num: 3, cat: "food", desc: "Boston's best restaurant neighborhood" },
        { lat: 42.3559, lng: -71.0486, label: "Boston Harbor", num: 4, cat: "activity", desc: "Sunset sailing on the harbor" },
        { lat: 42.3567, lng: -71.0545, label: "Long Wharf", num: 5, cat: "activity", desc: "Harbor walks and whale watch boats" },
        { lat: 42.3478, lng: -71.0778, label: "SoWa Open Market", num: 6, cat: "activity", desc: "Sunday artisan market in the South End" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Newbury Street & Copley Square", description: "Walk Newbury Street — Boston's premier shopping street, eight blocks of boutiques, galleries, and sidewalk cafés. The brownstones are beautiful, and the energy on a summer morning is perfect. End at Copley Square for the stunning Boston Public Library (McKim Building — Renaissance Revival masterpiece, free to enter) and Trinity Church.", details: ["📍 Start at Mass Ave end (more indie shops) and walk toward the Public Garden end (more luxury)", "💡 Boston Public Library's courtyard is a hidden oasis — grab a coffee and sit in the Italian-style cloister. Free."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Thinking Cup", description: "Cozy café on Newbury Street with exceptional coffee (they pour Stumptown). Perfect spot to fuel up before exploring. The avocado toast and pastries are solid.", meta: "$10-16pp · Newbury Street · Walk-in" }
          ],
          tips: [{ type: "tip", text: "The BPL courtyard is one of Boston's great secrets. Modeled after an Italian palazzo, it's peaceful, beautiful, and completely free. Perfect mid-morning escape." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "South End Exploration", description: "Walk south to the South End — Boston's most vibrant dining and arts neighborhood. Victorian brownstones line tree-shaded streets, and the restaurant density is incredible. In summer, outdoor patios are everywhere. Tremont Street and Washington Street are the main drags for restaurants and boutiques.", details: ["💡 If visiting on a Sunday, SoWa Open Market (artists, vintage, food trucks) runs 10am-4pm on Harrison Avenue. Great for unique finds."] },
            { title: "Boston Harbor Walk", description: "Walk the Harbor Walk from Long Wharf through the waterfront parks. In summer, the harbor is alive with sailboats, ferries, and harbor islands shuttle boats. The breeze off the water is refreshing on hot days. Consider a quick ferry to the Boston Harbor Islands (Georges Island has a Civil War fort to explore).", details: ["📍 Harbor Islands ferry from Long Wharf: ~$20 round trip, 30-min ride"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Myers + Chang", description: "Joanne Chang's other restaurant — a vibrant, colorful Chinese-Southeast Asian spot in the South End. The dumplings, wok-charred udon, and tea-smoked chicken are outstanding. Fun, shareable plates perfect for two.", meta: "$30-45pp · South End · Walk-in or Resy" }
          ],
          tips: [{ type: "reddit", text: "The South End is the most underrated neighborhood for visitors. Skip the tourist-heavy areas and eat here — it's where Boston chefs actually go on their nights off. Tremont Street alone has like 20 excellent restaurants.", cite: "r/boston" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset Sail on Boston Harbor", description: "Book a sunset sail on Boston Harbor — classic schooners and sailboats depart from Long Wharf and Rowes Wharf. Two hours on the water as the sun sets over the skyline is pure magic. Many include a BYOB option or serve drinks on board. One of the most romantic things to do in Boston.", details: ["📍 Boston Sail (classic schooner) from Long Wharf or Liberty Fleet from Long Wharf", "💡 Book in advance — summer sunset sails sell out. Bring a light layer; it's cooler on the water."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Neptune Oyster", description: "Tiny North End gem that serves arguably the best lobster roll in Boston (hot buttered, overflowing). The raw bar is impeccable. Lines can be long, but the food is transcendent. Worth planning your evening around. Arrive early or try for bar seats.", meta: "$50-70pp · North End · No reservations, line starts by 5pm, worth every minute" }
          ],
          tips: [{ type: "reddit", text: "Neptune Oyster's lobster roll is the benchmark. Hot butter, huge portion, perfect bread. Go at 4:30pm when they open — the line at 6pm can be an hour+. Totally, completely worth it.", cite: "r/boston" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Cocktails at Drink", description: "No menu, no signs — just tell the bartender what you're in the mood for and they'll craft something perfect. Drink is one of the best cocktail bars in America, hidden in Fort Point. Moody, intimate, and endlessly impressive. The perfect end to a Boston evening.", details: ["📍 348 Congress St, Fort Point · No sign outside — look for the brick building with people going downstairs", "💡 Sit at the bar for the full experience. Trust the bartenders completely — they're among the best in the country."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Drink is a destination bar. Seriously — cocktail nerds travel to Boston for this place. Don't order a specific drink; tell them a spirit you like and a flavor profile. They'll blow your mind." }]
        }
      ]
    },
    {
      num: 5,
      title: "Morning Markets & Departure",
      neighborhoods: "Back Bay · Beacon Hill · Downtown",
      date: "Jul 26",
      mapPins: [
        { lat: 42.3600, lng: -71.0570, label: "Faneuil Hall area", num: 1, cat: "food", desc: "Final Boston brunch" },
        { lat: 42.3541, lng: -71.0655, label: "Boston Common", num: 2, cat: "activity", desc: "One last stroll through the park" },
        { lat: 42.3591, lng: -71.0593, label: "Downtown Crossing", num: 3, cat: "activity", desc: "Shopping and city energy" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Boston Morning", description: "Take a last walk through Boston Common and the Public Garden. In summer, the gardens are lush and the swan boats are already gliding. Walk through Beacon Hill one more time — the morning light on the brick and cobblestones is beautiful. Boston rewards the slow goodbye.", details: [] },
            { title: "Last-Minute Picks", description: "Grab souvenirs on Charles Street (Beacon Hill) or Newbury Street (Back Bay). Pick up cannoli from Modern Pastry for the road. If you have time, the Boston Public Market near Faneuil Hall has local foods and gifts.", details: ["📍 Boston Public Market: 100 Hanover St · Local producers, great for food gifts"] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Paramount", description: "Beacon Hill breakfast institution. Old-school cafeteria-style (order at the counter, sit wherever). The banana french toast, eggs benedict, and home fries are famous. Locals have been coming here for decades. Cash and card. A proper Boston farewell.", meta: "$14-22pp · Charles Street, Beacon Hill · Walk-in, line moves fast" }
          ],
          tips: [{ type: "tip", text: "Logan Airport is just a short ride from downtown — the Blue Line goes direct from Aquarium or Government Center to the airport. Or grab a rideshare ($15-25 from most areas). Leave 2 hours before your flight." }]
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
