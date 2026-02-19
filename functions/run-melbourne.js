const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771456417689_mzcldc",
  email: "bernard.j.huang@gmail.com",
  destination: "Melbourne VIC, Australia",
  start_date: "2026-02-18",
  end_date: "2026-02-21",
  group_size: "1",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-18T23:13:37.689Z",
  status: "pending"
};

const itineraryData = {
  destination: "Melbourne, Australia",
  countryEmoji: "🇦🇺",
  title: "Melbourne in 3 Nights: Laneways, Coffee & Culture",
  subtitle: "CBD Laneways → Fitzroy → South Melbourne → St Kilda",
  description: "A solo explorer's guide to Melbourne — Australia's cultural capital. Dive into world-class coffee culture, street art-covered laneways, incredible food from every continent, and neighborhoods bursting with character. February means summer in Melbourne: long evenings, rooftop bars, and beach sunsets.",
  duration: "3 nights / 4 days",
  dates: "Feb 18 – 21, 2026",
  budget: "Moderate",
  pace: "Relaxed — deep dives over checklists",
  bestFor: "Solo travelers, coffee lovers & foodies",
  highlights: [
    "Hosier Lane & AC/DC Lane — Melbourne's iconic street art",
    "World-class coffee in every laneway",
    "Queen Victoria Market — fresh food, crafts & atmosphere",
    "Fitzroy & Collingwood — Melbourne's creative heartbeat",
    "Rooftop bars with skyline views",
    "Royal Botanic Gardens — peaceful green escape",
    "South Melbourne Market — locals' favorite",
    "St Kilda Beach sunset & Luna Park",
    "NGV (National Gallery of Victoria) — free collection",
    "Hidden bars behind unmarked doors"
  ],
  essentials: [
    { title: "🚊 Getting Around", text: "Get a Myki card at any station or 7-Eleven. Trams are free within the CBD Free Tram Zone. Beyond that, trams + trains cover everywhere. The city is very walkable — most CBD attractions are within 20 minutes on foot." },
    { title: "💵 Money Tips", text: "Cards accepted everywhere — many places are cashless. Tipping is not expected in Australia (staff earn good wages) but 10% for great service is appreciated. No tax is added at checkout — the listed price is what you pay." },
    { title: "☀️ February Weather", text: "Summer! Expect 20-30°C with occasional hot days (35°C+). Melbourne is famous for 'four seasons in one day' — carry a light layer and sunscreen. UV is extreme in Australian summer — wear SPF 50+." },
    { title: "🏨 Where to Stay", text: "CBD (Flinders Lane area) for walkability to everything. Fitzroy or Collingwood for hipster vibes. Southbank for river views. Solo travelers: CBD hostels are social; boutique hotels on Flinders Lane are perfectly located." },
    { title: "☕ Coffee Culture", text: "Melbourne takes coffee seriously — it's arguably the world's best coffee city. Order a 'flat white' (invented here). Avoid chains. Every laneway has an excellent café. If the barista looks judgmental, you're in the right place." },
    { title: "📱 Useful Apps", text: "PTV (public transport), Google Maps (walking), Beanhunter (coffee), Broadsheet Melbourne (restaurants/bars), Zomato (reviews)." }
  ],
  days: [
    {
      num: 1,
      title: "CBD Laneways, Street Art & Rooftop Bars",
      neighborhoods: "CBD · Flinders Lane · Chinatown · Southbank",
      date: "Feb 18",
      mapPins: [
        { lat: -37.8162, lng: 144.9671, label: "Flinders Street Station", num: 1, cat: "activity", desc: "Melbourne's iconic yellow railway station" },
        { lat: -37.8165, lng: 144.9693, label: "Hosier Lane", num: 2, cat: "activity", desc: "Melbourne's most famous street art laneway" },
        { lat: -37.8170, lng: 144.9669, label: "Centre Place & Degraves St", num: 3, cat: "food", desc: "Laneway cafés and European-style dining" },
        { lat: -37.8116, lng: 144.9693, label: "Chinatown", num: 4, cat: "food", desc: "Australia's oldest Chinatown — incredible dumplings" },
        { lat: -37.8208, lng: 144.9672, label: "NGV International", num: 5, cat: "activity", desc: "Australia's oldest and largest art gallery — free" },
        { lat: -37.8100, lng: 144.9700, label: "Rooftop Bar", num: 6, cat: "nightlife", desc: "Open-air rooftop cinema and bar" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Flinders Street Station & Federation Square", description: "Start at Melbourne's heart — the iconic yellow Flinders Street Station. Cross to Federation Square and get your bearings. The visitor center here has free maps and tips.", details: ["📍 Flinders Street Station — catch a tram here if needed"] },
            { title: "Laneway Coffee Crawl", description: "Melbourne's laneways hide the world's best coffee. Start at Degraves Street (European-style laneway cafés), then weave through Centre Place to Flinders Lane. Order a flat white — it was born here.", details: ["💡 Try Patricia Coffee Brewers (standing room only, incredible coffee) or Dukes Coffee Roasters on Flinders Lane."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hardware Société", description: "French-influenced brunch in a tiny laneway spot. The baked eggs with chorizo and the crème brûlée french toast are legendary. Come early — it's popular.", meta: "$18-28pp · Hardware Lane · Walk-in, arrive by 9am" }
          ],
          tips: [{ type: "tip", text: "Melbourne mornings are for coffee. Don't rush this. Find a laneway café, sit down, people-watch. This IS the Melbourne experience." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hosier Lane & Street Art Walk", description: "Melbourne's most famous laneway is covered floor-to-ceiling in street art — and it changes constantly. Walk through Hosier Lane, then explore AC/DC Lane, Croft Alley, and Blender Lane for more. Every visit reveals new pieces.", details: ["📍 Off Flinders Street, near Federation Square", "💡 The art changes weekly. What you see won't be there next month."] },
            { title: "NGV International", description: "The National Gallery of Victoria's international collection is free and world-class. The building itself is stunning — the stained glass ceiling and water wall entrance are iconic. Don't miss the photography and contemporary galleries.", details: ["📍 180 St Kilda Road · Free permanent collection · Open 10-5"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Chin Chin", description: "Melbourne's most hyped Asian restaurant lives up to it. Bold Southeast Asian flavors, vibrant space, always buzzing. The pad see ew and crispy bug tail are musts. Solo diners can often snag a bar seat quickly.", meta: "$25-40pp · Flinders Lane · Walk-in (bar seats fastest)" }
          ],
          tips: [{ type: "reddit", text: "Chin Chin has a no-reservations policy but the queue moves fast. Go at 11:30am or after 2pm to skip the wait. Bar seats are perfect for solo.", cite: "r/melbourne" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Rooftop Bar Season", description: "February is peak rooftop season in Melbourne. Hit Rooftop Bar (Curtin House, Level 6) for open-air drinks with CBD views, or Naked in the Sky above Fitzroy for a different vibe. Summer evenings are long and warm.", details: ["💡 Rooftop Bar sometimes has outdoor cinema screenings — check their site."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Supernormal", description: "Andrew McConnell's modern Asian restaurant on Flinders Lane. The New England lobster roll and the raw kingfish are exceptional. Sleek, buzzy, and perfect for solo dining at the bar.", meta: "$35-50pp · Flinders Lane · Book on their site" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Hidden Bar Hop", description: "Melbourne pioneered the hidden bar scene. Try Eau de Vie (speakeasy behind a heavy door on Malthouse Lane), Bar Americano (6-seat standing bar in a laneway), or Manchuria (cocktail bar above a Chinese restaurant). Each has personality to spare.", details: ["💡 Bar Americano fits 6 people. Seriously. If there's a spot, take it — the martinis are Melbourne's best."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Melbourne's bar scene rewards the curious. Look for unmarked doors and narrow staircases. If it looks like you shouldn't go in, you probably should." }]
        }
      ]
    },
    {
      num: 2,
      title: "Fitzroy, Markets & Melbourne's Creative Side",
      neighborhoods: "Fitzroy · Collingwood · Carlton · Queen Victoria Market",
      date: "Feb 19",
      mapPins: [
        { lat: -37.8075, lng: 144.9564, label: "Queen Victoria Market", num: 1, cat: "food", desc: "Melbourne's legendary open-air market since 1878" },
        { lat: -37.7984, lng: 144.9783, label: "Brunswick Street, Fitzroy", num: 2, cat: "activity", desc: "Melbourne's bohemian heart — cafés, vintage, street art" },
        { lat: -37.7998, lng: 144.9861, label: "Smith Street, Collingwood", num: 3, cat: "food", desc: "Trendy restaurants and craft beer" },
        { lat: -37.8000, lng: 144.9660, label: "Carlton Gardens", num: 4, cat: "activity", desc: "UNESCO-listed Royal Exhibition Building" },
        { lat: -37.7960, lng: 144.9660, label: "Lygon Street, Carlton", num: 5, cat: "food", desc: "Melbourne's 'Little Italy' — pasta and gelato" },
        { lat: -37.8020, lng: 144.9840, label: "Gertrude Street", num: 6, cat: "activity", desc: "Galleries, boutiques, and excellent wine bars" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Queen Victoria Market", description: "Melbourne's sprawling open-air market has been running since 1878. Wander the produce halls, deli section (grab cheese and charcuterie), and the merchandise section. The atmosphere on a summer morning is electric.", details: ["📍 Queen St · Open Tue, Thu, Fri, Sat, Sun · Arrive by 9am for best energy", "💡 The deli hall is the highlight — free tastings everywhere. Try the bratwurst stand near the food court."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Market Lane Coffee (QVM)", description: "Excellent single-origin coffee right at the market. Grab a flat white and a pastry, then explore with coffee in hand.", meta: "$5-8 · Queen Victoria Market" }
          ],
          tips: [{ type: "reddit", text: "The American Doughnut Kitchen van at QVM has been there since 1950. Hot jam doughnuts, $1 each. There's always a line. It's always worth it.", cite: "r/melbourne" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Fitzroy: Brunswick & Gertrude Streets", description: "Catch a tram to Fitzroy — Melbourne's most creative neighborhood. Brunswick Street has vintage shops, independent bookstores, record stores, and street art everywhere. Gertrude Street is more curated — galleries, wine bars, and boutique design shops.", details: ["📍 Tram 11 from CBD to Brunswick Street", "💡 Polyester Records and Fitzroy Books are great browsing stops. Rose Street Artists' Market (weekends) is worth checking."] },
            { title: "Collingwood Brewery Lane", description: "Walk east to Collingwood for Melbourne's craft beer scene. Stomping Ground Brewery has a great beer garden. Nearby, Moon Dog World is an over-the-top brewery theme park with a pool (yes, really).", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Lune Croissanterie", description: "Widely considered the best croissants in the world. The original Fitzroy location has a glass-walled lab where you watch them being made. The twice-baked almond croissant is transcendent.", meta: "$8-15 · Fitzroy · Open early, sells out by afternoon" }
          ],
          tips: [{ type: "tip", text: "Lune croissants sell out. Go before 11am or miss out. The cruffin (croissant-muffin hybrid) is their rotating special — always incredible." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Carlton & Lygon Street", description: "Walk through Carlton Gardens (UNESCO-listed Royal Exhibition Building is stunning at sunset) to Lygon Street — Melbourne's Little Italy. It's touristy in parts but the Italian heritage is real. Great for a leisurely pasta dinner.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Tipo 00", description: "Modern Italian pasta bar on Lygon Street that's rewritten the rules. Hand-made pasta, creative seasonal fillings, excellent wine list. The malfaldine with duck ragù is phenomenal. Solo dining at the bar is perfect here.", meta: "$35-50pp · Lygon Street, Carlton · Book ahead" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Fitzroy Bar Crawl", description: "Head back to Fitzroy for nightlife. The Everleigh (upstairs cocktail bar on Gertrude Street — old-world glamour), Black Pearl (legendary cocktail bar on Brunswick Street), or Naked for Satan (rooftop pintxos bar with city views). Fitzroy after dark is Melbourne at its best.", details: ["💡 Naked for Satan has free pintxos (small bites) at the downstairs bar. The rooftop upstairs (Naked in the Sky) has views but charges for food."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Black Pearl on Brunswick Street is consistently rated one of the best bars in the world. The cocktails are next level. Go late — it gets better after 10pm.", cite: "r/melbourne" }]
        }
      ]
    },
    {
      num: 3,
      title: "South Melbourne, Botanic Gardens & Beach Sunset",
      neighborhoods: "South Melbourne · Royal Botanic Gardens · St Kilda",
      date: "Feb 20",
      mapPins: [
        { lat: -37.8316, lng: 144.9570, label: "South Melbourne Market", num: 1, cat: "food", desc: "Locals' market — dim sims, organic produce, great coffee" },
        { lat: -37.8304, lng: 144.9796, label: "Royal Botanic Gardens", num: 2, cat: "activity", desc: "38 hectares of stunning gardens by the Yarra" },
        { lat: -37.8300, lng: 144.9830, label: "Shrine of Remembrance", num: 3, cat: "activity", desc: "War memorial with panoramic city views from the balcony" },
        { lat: -37.8580, lng: 144.9740, label: "St Kilda Beach", num: 4, cat: "activity", desc: "Melbourne's beloved beach strip" },
        { lat: -37.8568, lng: 144.9766, label: "Luna Park", num: 5, cat: "activity", desc: "Heritage amusement park with iconic face entrance" },
        { lat: -37.8615, lng: 144.9740, label: "St Kilda Pier", num: 6, cat: "activity", desc: "Sunset views and little penguins at dusk" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "South Melbourne Market", description: "Skip the tourist markets — this is where locals shop. Running since 1867, it's smaller and more authentic than QVM. The dim sim (invented in Melbourne!) from the original South Melbourne Dim Sim stall is a must.", details: ["📍 Tram 96 from CBD · Open Wed, Fri, Sat, Sun", "💡 The dim sim here is different from what you've had anywhere else. Get it fried."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Chez Dré", description: "French-style bakery and café near South Melbourne Market. Exceptional pastries, strong coffee, and a relaxed neighborhood feel. The pain au chocolat is perfect.", meta: "$15-22pp · South Melbourne · Walk-in" }
          ],
          tips: [{ type: "tip", text: "South Melbourne Market on a Wednesday morning is blissfully uncrowded. Grab coffee, a dim sim, and wander. This is local Melbourne." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Royal Botanic Gardens", description: "38 hectares of stunning gardens along the Yarra River. In February, everything is in full bloom. Walk the Tan Track (3.8km loop popular with joggers), find the ornamental lake, and spot black swans. Bring a book — the lawns are perfect for lying in the grass.", details: ["📍 Free entry · Open sunrise to sunset · Enter from Birdwood Avenue or Domain Road"] },
            { title: "Shrine of Remembrance", description: "Walk up to the Shrine for the best panoramic view of Melbourne's skyline. The balcony terrace gives a 360° view — the CBD, the Gardens, the bay. Powerful memorial and stunning architecture.", details: ["📍 Free entry · The balcony is accessed from inside — ask at the entrance."] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Jardin Tan (Botanic Gardens)", description: "Shannon Bennett's restaurant right inside the gardens. Modern Australian menu using produce from the gardens' own kitchen garden. Beautiful setting among the trees.", meta: "$30-45pp · Royal Botanic Gardens · Book on their site" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "St Kilda Beach & Sunset", description: "Catch a tram to St Kilda — Melbourne's beachside neighborhood. Walk along the Esplanade, past Luna Park's iconic face, and out along St Kilda Pier. February sunsets here are stunning — the sky goes pink and orange over the bay.", details: ["📍 Tram 96 from CBD — about 30 min", "💡 Wait at the end of St Kilda Pier at dusk to see the little penguins come home to their burrow. Free and magical."] },
            { title: "Little Penguins at Dusk", description: "At the end of St Kilda Pier breakwater, a colony of little penguins (the world's smallest) returns each evening at dusk. Stand quietly, watch them waddle in from the sea. It's free and unforgettable.", details: ["💡 Arrive 15-20 min before sunset. No flash photography. Be quiet — they're tiny and easily startled."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Stokehouse", description: "Right on St Kilda Beach with floor-to-ceiling ocean views. Upstairs is fine dining; downstairs (Stokebar) is casual with the same view. Fresh seafood, great wine list, sunset dinner is magical.", meta: "$40-60pp (upstairs) or $25-35 (Stokebar) · St Kilda Beach · Book upstairs" }
          ],
          tips: [{ type: "reddit", text: "The little penguins at St Kilda pier are amazing but PLEASE don't use flash or torches. Red lights only. The volunteers there will guide you. Best wildlife experience in Melbourne and it's free.", cite: "r/melbourne" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Acland Street & St Kilda Nightlife", description: "Acland Street has classic cake shops (European-style since the 1930s — the area has a strong Jewish heritage). For drinks, try Hotel Esplanade (The Espy) — a legendary live music venue recently restored to glory. There's usually a band playing.", details: ["💡 The Espy has free live music most nights. The rooftop has bay views. It's a Melbourne institution."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "End the night with a cake from one of Acland Street's cake shops — Monarch Cakes has been here since 1934. The kugelhopf is legendary." }]
        }
      ]
    },
    {
      num: 4,
      title: "Morning Vibes & Departure",
      neighborhoods: "CBD · Southbank",
      date: "Feb 21",
      mapPins: [
        { lat: -37.8180, lng: 144.9580, label: "Flinders Lane Cafés", num: 1, cat: "food", desc: "Final Melbourne coffee ritual" },
        { lat: -37.8206, lng: 144.9540, label: "Arts Centre Melbourne", num: 2, cat: "activity", desc: "Iconic spire and riverside arts precinct" },
        { lat: -37.8200, lng: 144.9580, label: "Yarra River Walk", num: 3, cat: "activity", desc: "Peaceful riverside stroll through Southbank" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Melbourne Coffee", description: "One last flat white in a laneway café. Take your time — Melbourne mornings are meant to be savored. Sit, sip, watch the city wake up. You've earned it.", details: [] },
            { title: "Yarra River Morning Walk", description: "Stroll along the Yarra through Southbank. The river is peaceful in the morning — rowers glide past, the Arts Centre spire catches the light. A perfect quiet goodbye to Melbourne.", details: [] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Higher Ground", description: "Stunning café in a converted power station — soaring ceilings, beautiful fit-out, exceptional food. The ricotta hotcakes are Melbourne-famous. A proper farewell brunch.", meta: "$20-30pp · CBD · Arrive early or book" }
          ],
          tips: [{ type: "tip", text: "Melbourne to the airport: SkyBus from Southern Cross Station ($20, runs every 10 min, takes ~30 min). Way easier than a taxi in traffic." }]
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
