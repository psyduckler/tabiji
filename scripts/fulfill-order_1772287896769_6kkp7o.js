const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: "order_1772287896769_6kkp7o",
  email: "argirard@aol.com",
  destination: "London, UK",
  start_date: "2026-05-15",
  end_date: "2026-05-21",
  group_size: "2",
  travel_style: "Adventure, Foodie, Nightlife",
  dining: "Casual throughout",
  budget: "",
  requests: "Small pubs restaurant\nWalking",
  amount: "0.00",
  timestamp: "2026-02-28T14:11:36.769Z",
  status: "in-progress"
};

const itineraryData = {
  destination: "London, UK",
  countryEmoji: "🇬🇧",
  title: "London in 7 Days: Pubs, Walking & Hidden Nightlife",
  subtitle: "South Bank → Soho → Shoreditch → Notting Hill → Greenwich → Camden → The City",
  description: "A London adventure built for two who love walking, great pubs, and staying out late. Seven days to explore London's most rewarding neighborhoods on foot — iconic sights by day, legendary pubs and vibrant bars by night. From centuries-old taverns to craft beer railway arches, this is London for people who actually want to feel the city.",
  duration: "7 days",
  dates: "May 15 – 21, 2026",
  budget: "Moderate",
  pace: "Active walkers — 8-12km per day with plenty of pub stops",
  bestFor: "Couples who love walking, craft beer, street food & late nights",
  highlights: [
    "Borough Market — London's legendary food market (open Friday & Saturday)",
    "Ye Olde Cheshire Cheese — a pub Samuel Johnson drank at since 1538",
    "Brixton Market — vibrant, multicultural food and nightlife hub",
    "Brick Lane & Shoreditch street art — London's coolest 2km walk",
    "The Mayflower — the pub that launched the Pilgrim voyage to America",
    "Camden Market & the canal — indie food, music venues, chaos",
    "Sky Garden — free 360° rooftop views over London",
    "Greenwich Royal Observatory — stand on the Prime Meridian",
    "Columbia Road Flower Market (Sunday morning — iconic)",
    "Thames Path — walk the river from Westminster to Tower Bridge"
  ],
  essentials: [
    { title: "🚇 Getting Around", text: "Use contactless bank cards on the Tube — no need for Oyster. Daily cap is ~£8.10 for Zones 1-2. But this itinerary is designed for WALKING — many of the best pub crawls connect naturally on foot. Download Citymapper and follow the walking routes between neighborhoods." },
    { title: "🍺 Pub Etiquette", text: "Order at the bar — there's no table service in traditional British pubs. Pay when you order. 'Round' culture means each person buys a round for the group. A pint of ale/lager is typically £5-7 in central London, £4-5 in outer areas. 'Lock-ins' (after-hours drinking with door closed) occasionally happen at proper local pubs." },
    { title: "🌤️ May Weather", text: "May is London at its best — 14-19°C, long evenings (sunset ~8:45pm), parks in full bloom. Light rain is always possible. Pack a small packable rain jacket and comfortable walking shoes. Evenings can cool down — bring a light layer." },
    { title: "🏨 Where to Stay", text: "Southwark or London Bridge: perfect central location, close to Borough Market and South Bank. Shoreditch: great for nightlife access. Brixton: local vibes, excellent food and bar scene, cheaper. Avoid Zone 2+ hotels that aren't on a Tube line — London is big." },
    { title: "📱 Essential Apps", text: "Citymapper (best navigation app for London — includes walking), Untappd (find craft beer spots), OpenTable/Resy (restaurant booking), What's On Stage (theatre), Time Out London (events). Google Maps walking directions are excellent for the walking pub crawl routes." },
    { title: "🦶 Walking Tips", text: "The distances between London's best neighborhoods are very walkable: Borough Market → Tate Modern → Southbank = 1km. London Bridge → Shoreditch = 3km via Spitalfields. Westminster → Covent Garden = 20 min walk. Invest in good shoes — you'll easily do 15,000+ steps a day." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival — South Bank, Westminster & First London Pints",
      neighborhoods: "Westminster · South Bank · Waterloo",
      date: "May 15",
      mapPins: [
        { lat: 51.5014, lng: -0.1419, label: "Westminster & Big Ben", num: 1, cat: "activity", desc: "Iconic Parliament and Elizabeth Tower" },
        { lat: 51.5033, lng: -0.1195, label: "London Eye", num: 2, cat: "activity", desc: "30-minute panoramic ride" },
        { lat: 51.5076, lng: -0.0994, label: "Tate Modern / South Bank", num: 3, cat: "activity", desc: "World-class modern art + riverside walk" },
        { lat: 51.5074, lng: -0.0901, label: "Borough Market", num: 4, cat: "food", desc: "London's legendary food market" },
        { lat: 51.5043, lng: -0.0858, label: "The Anchor Bankside", num: 5, cat: "food", desc: "Historic pub — Samuel Pepys watched the Great Fire from here" },
        { lat: 51.5079, lng: -0.0877, label: "The George Inn", num: 6, cat: "food", desc: "London's only surviving galleried coaching inn, 1677" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Westminster & Big Ben", description: "Get oriented — start at Westminster Tube and do the classic London arrival moment. Big Ben, Parliament, Westminster Bridge. Cross the bridge for a full river view with the London Eye ahead of you.", details: ["📍 Westminster Tube (Jubilee/District/Circle lines)"] },
            { title: "South Bank Walk to Tate Modern", description: "Walk along the Thames from Westminster Bridge to Tate Modern — about 1.5km of London's finest riverside path. Pass the London Eye, Southbank Centre, National Theatre, and Globe Theatre on the way.", details: ["💡 Pop into Tate Modern (free) for 30-60 min — the Turbine Hall alone is worth it."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Flat White (any South Bank café)", description: "Grab a flat white and pastry from one of the Southbank kiosks and eat it watching the river. That's the London move.", meta: "£4-7 · Various spots along the Southbank" }
          ],
          tips: [{ type: "tip", text: "May in London means sunset around 8:45pm — you have long days. Don't rush the morning. The city reveals itself slowly." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Borough Market", description: "London's greatest food market. Friday and Saturday it's fully open — all the legendary stalls. Padella pasta (queue moves fast), Kappacasein raclette, Bread Ahead doughnuts. Graze your way around rather than sitting down.", details: ["📍 London Bridge Tube/rail · Open Mon-Sat", "💡 Friday and Saturday are the biggest days. If you're here on a weekday, it's quieter but still open."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Borough Market Grazing", description: "Padella for fresh pasta (pici cacio e pepe is famous), Monmouth Coffee, Bar Tozino for Ibérico ham, Bread Ahead doughnuts. Budget £15-20 for two grazing properly.", meta: "£15-20 for two · Open Mon-Sat" }
          ],
          tips: [{ type: "reddit", text: "Padella at Borough Market is legitimately the best pasta in London. Queue looks long but moves in 15-20 minutes. The pici cacio e pepe is perfect.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Historic Pub Crawl: Bermondsey & Bankside", description: "Start your London pub education with two of the oldest and most atmospheric pubs in the city — both within a 5-minute walk of Borough Market.", details: [] }
          ],
          meals: [
            { type: "🍺 First Pub", name: "The Anchor Bankside", description: "Dating to the 1600s, right on the Thames. Samuel Pepys watched the Great Fire of London from this spot in 1666. Stone floors, low beams, river views from the terrace. Order a pint of London Pride.", meta: "34 Park St, SE1 · Order at bar · Cash or card" },
            { type: "🍺 Second Pub", name: "The George Inn", description: "London's only surviving galleried coaching inn — a National Trust property still serving proper beer since 1677. Drink in the courtyard under the medieval gallery. Get a Young's bitter.", meta: "75-77 Borough High St · Worth the detour · Incredible atmosphere" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Dinner in Bermondsey", description: "Settle in for dinner after your pub warm-up. Bermondsey has quietly become one of London's best dining streets.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Tozino or José Tapas Bar", description: "José Pizarro's tiny Bermondsey tapas bar — one of the best in London. Standing room, brilliant Ibérico ham, croquetas, and sherries. Or Tozino next door for full sit-down Iberian dinner.", meta: "104 Bermondsey St · Walk-in only · Small and buzzing" }
          ],
          tips: [{ type: "tip", text: "José has no reservations and fills up fast. Arrive at 6pm or 8:30pm for the best chance of space. Worth the wait." }]
        }
      ]
    },
    {
      num: 2,
      title: "The City, Fleet Street Pubs & Soho Night Out",
      neighborhoods: "City of London · Fleet Street · Covent Garden · Soho",
      date: "May 16",
      mapPins: [
        { lat: 51.5141, lng: -0.0985, label: "St Paul's Cathedral", num: 1, cat: "activity", desc: "Wren's masterpiece — 365 steps to the dome" },
        { lat: 51.5147, lng: -0.1059, label: "Ye Olde Cheshire Cheese", num: 2, cat: "food", desc: "London's most historic pub — rebuilt 1667" },
        { lat: 51.5159, lng: -0.1150, label: "Temple & Inns of Court", num: 3, cat: "activity", desc: "Medieval legal quarter — free to walk" },
        { lat: 51.5117, lng: -0.1240, label: "Covent Garden", num: 4, cat: "activity", desc: "Street performers and market" },
        { lat: 51.5131, lng: -0.1370, label: "Soho", num: 5, cat: "nightlife", desc: "London's dining and bar capital" },
        { lat: 51.5121, lng: -0.1319, label: "The French House", num: 6, cat: "food", desc: "Soho's most legendary boozer — De Gaulle drank here" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "St Paul's Cathedral Walk", description: "The exterior of Wren's masterpiece is free to admire and photograph from everywhere. For the dome climb (365 steps, incredible city views), entry is £22pp. Walk around the cathedral and through the churchyard.", details: ["💡 The Whispering Gallery inside the dome is remarkable. Budget 1.5-2 hours if going inside."] },
            { title: "Temple & Inns of Court", description: "Walk west from St Paul's through the medieval Inns of Court — the Temple (Middle and Inner Temple), Gray's Inn Gardens. These legal chambers have barely changed in 400 years. Free to walk through on weekdays.", details: ["💡 It feels like a time warp. The gardens at Middle Temple are open and beautiful in May."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Look Mum No Hands! or any local café", description: "Grab breakfast near St Paul's before starting. Gail's Bakery on Fleet Street is reliable, or any of the classic City bakeries that open early for the office crowd.", meta: "£8-12pp" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Fleet Street Historic Pub Walk", description: "Fleet Street — London's old newspaper row — has several of the city's most ancient pubs. Walk the short stretch between Chancery Lane and Blackfriars Tube, stopping in at the greats.", details: [] },
            { title: "Covent Garden Wander", description: "Walk west to Covent Garden for the street performers in the piazza, the Apple Market, and window shopping. The Royal Opera House lobby is free to walk through.", details: [] }
          ],
          meals: [
            { type: "🍺 Pub Lunch", name: "Ye Olde Cheshire Cheese", description: "Built right after the Great Fire of 1667, this labyrinthine pub off Fleet Street is extraordinary. Multiple bars on different levels, sawdust on the floor, roaring fireplaces, and properly cheap traditional pub food (pies, etc.). Samuel Johnson was a regular. Order house ale and a pie.", meta: "Wine Office Court, off 145 Fleet Street · Cash preferred · No sign on the door — look for the tiny alley" },
            { type: "🍺 Also visit", name: "The Blackfriar", description: "The most art nouveau pub in London — built in 1905 with extraordinary marble, bronze, and mosaic decorations inside. Even if just for one drink, it's unmissable.", meta: "174 Queen Victoria St · Open daily" }
          ],
          tips: [{ type: "reddit", text: "Ye Olde Cheshire Cheese feels like you've walked into the 17th century. Go down into the basement bar — it's the most atmospheric pub room in London. The Cheshire Cheese 'Polly' parrot stuffed in a glass case has been there since the 1920s.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Soho Dinner & Bar Hop", description: "Head to Soho for London's best dinner and bar scene — dense, walkable, and endlessly entertaining. Wander Dean Street, Frith Street, and Old Compton Street.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Bao Soho or Kiln", description: "Bao: Taiwanese bao buns, casual and brilliant (53 Lexington St, no reservations, queue worth it). OR Kiln: open-fire Thai-British cooking on Brewer Street, buzzy, book ahead.", meta: "£20-35 for two · Soho · Both excellent" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Soho Pub Crawl", description: "Three legendary Soho pubs in a 10-minute walk.", details: ["The French House, 49 Dean Street — half pints only (house rule), incredible Soho history, De Gaulle and Dylan Thomas drank here. A London institution.", "The Dog and Duck, 18 Bateman Street — beautiful Victorian pub, Orwell allegedly drank here.", "Bar Termini, 7 Old Compton Street — tiny Italian bar with some of London's best negronis."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The French House serves only half pints — the landlord's rule since forever. They also have natural wines and genuinely good cheese. The whole pub is about 30 people max. It's a treasure." }]
        }
      ]
    },
    {
      num: 3,
      title: "East End & Shoreditch — Street Art, Spitalfields & Late Nights",
      neighborhoods: "Spitalfields · Brick Lane · Shoreditch · Bethnal Green",
      date: "May 17",
      mapPins: [
        { lat: 51.5201, lng: -0.0750, label: "Spitalfields Market", num: 1, cat: "food", desc: "Covered market — great Sunday but good daily" },
        { lat: 51.5246, lng: -0.0790, label: "Brick Lane", num: 2, cat: "activity", desc: "Street art, bagels & curry mile" },
        { lat: 51.5265, lng: -0.0837, label: "Shoreditch Street Art", num: 3, cat: "activity", desc: "Boxpark, Rivington Street, Hanbury Street murals" },
        { lat: 51.5226, lng: -0.0750, label: "Beigel Bake", num: 4, cat: "food", desc: "24-hour bagel shop — iconic salt beef bagel" },
        { lat: 51.5267, lng: -0.0806, label: "Boxpark Shoreditch", num: 5, cat: "food", desc: "Street food container park" },
        { lat: 51.5270, lng: -0.0790, label: "Nightlife — Shoreditch", num: 6, cat: "nightlife", desc: "Happiness Forgets, Discount Suit Company, XOYO" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Spitalfields Market", description: "Start at this covered Victorian market. Sundays are the big day, but weekdays have food stalls, vintage shops, and good coffee. Great for browsing before heading deeper into the East End.", details: ["📍 Commercial Street, E1 · Liverpool Street Tube"] },
            { title: "Brick Lane Street Art Walk", description: "Walk north up Brick Lane — the entire area is an open-air street art gallery. Turn onto Hanbury Street, Princelet Street, and the Shoreditch Triangle for the best murals. Artists like Banksy, ROA, and Stik have worked here.", details: ["💡 Download the Shoreditch Street Art map from Google 'Shoreditch street art tour' — it's well-documented."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Beigel Bake (Brick Lane)", description: "Open 24 hours, this legendary bagel shop sells the salt beef beigel for £4-5. Queue moves fast. Non-negotiable on Brick Lane.", meta: "159 Brick Lane · Cash only · Life-changing salt beef bagel" }
          ],
          tips: [{ type: "reddit", text: "Skip the Brick Lane curry touts who stand outside calling you in — they're tourist traps. The real Brick Lane food is Beigel Bake and the weekend food market stalls inside Spitalfields and Boxpark.", cite: "r/london" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sky Garden", description: "The 'Walkie Talkie' building's free rooftop garden gives 360° views over London. Must book free tickets online (skygarden.london) — they release 3 weeks ahead and go fast. 2-3pm is a great slot.", details: ["💡 Free tickets at skygarden.london. If full, the Rooftop Bar at Montcalm Royal London House (nearby) has similar views for the cost of a drink."] },
            { title: "Shoreditch Street Art & Boxpark", description: "Walk the Shoreditch Triangle: Rivington Street, Charlotte Road, Old Street. Street art walls everywhere. Boxpark has food from all over the world in converted shipping containers.", details: [] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Boxpark Shoreditch or Mercato Metropolitano", description: "Boxpark: casual street food containers — pick your cuisine. Mercato Metropolitano (south): Italian market hall with incredible pasta, pizza, and natural wine.", meta: "£10-18pp · Casual and excellent" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Craft Beer: Bethnal Green & Shoreditch", description: "London has an incredible craft beer scene concentrated in East London railway arches. Walk the Bethnal Green arches for some of the best.", details: ["Redchurch Brewery Taproom — local Shoreditch brewery, excellent pale ales", "Beavertown Tottenham (nearby) — one of London's most famous craft breweries", "EBF (East Beverley Follick) — tiny local, worth finding"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Smokestak", description: "Low-and-slow BBQ in a railway arch. The beef brisket is the best in London — smoky, tender, extraordinary. Order the smoked ox cheek and the burnt ends too. Industrial setting, great atmosphere.", meta: "35 Sclater St, E1 · Book on Resy · £30-40 for two" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Shoreditch Bar Crawl", description: "London's best nightlife concentration for adventurous drinkers.", details: ["Happiness Forgets, Holywell Lane — basement speakeasy with exceptional cocktails. Book a table or arrive before 8pm. London's best cocktail bar many years running.", "Discount Suit Company, Middlesex St — bar hidden inside what looks like a suit shop entrance. Creative cocktails, cool crowd.", "XOYO, Cowper St — if you want a proper club night, this is Shoreditch's best. Check listings for the night."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "End the night at Beigel Bake (open 24 hours) — a salt beef bagel at 2am on Brick Lane is a London rite of passage." }]
        }
      ]
    },
    {
      num: 4,
      title: "Tower of London, Bermondsey Beer Mile & Thames Path Walk",
      neighborhoods: "Tower Hill · Bermondsey · London Bridge",
      date: "May 18",
      mapPins: [
        { lat: 51.5081, lng: -0.0759, label: "Tower of London", num: 1, cat: "activity", desc: "1,000-year-old fortress — Crown Jewels & Beefeaters" },
        { lat: 51.5055, lng: -0.0754, label: "Tower Bridge", num: 2, cat: "activity", desc: "Victorian icon with glass floor walkway" },
        { lat: 51.4972, lng: -0.0784, label: "Bermondsey Beer Mile", num: 3, cat: "food", desc: "London's craft brewery corridor under railway arches" },
        { lat: 51.5015, lng: -0.0822, label: "Maltby Street Market", num: 4, cat: "food", desc: "Locals' alternative to Borough Market" },
        { lat: 51.5043, lng: -0.0858, label: "The Mayflower Pub", num: 5, cat: "food", desc: "The pub that launched the Pilgrim Fathers' voyage" },
        { lat: 51.5008, lng: -0.0754, label: "Shad Thames Walk", num: 6, cat: "activity", desc: "Victorian warehouse district — gorgeous riverside walk" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tower of London", description: "Arrive at opening (10am) to beat crowds. Join a free Yeoman Warder (Beefeater) tour — they're dark, funny, and brilliantly knowledgeable. See the Crown Jewels (allow 30-45 min queue), the White Tower, and the spot where Anne Boleyn was executed.", details: ["💡 £33pp — prebook on the HRP website for timed entry. Allow 2.5-3 hours.", "📍 Tower Hill Tube (Circle/District lines)"] },
            { title: "Tower Bridge Walk", description: "Cross Tower Bridge — it's free and the views are superb. The glass floor walkway costs £12pp if you want the vertigo experience. Walk over and back.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The Beefeater tours are the highlight of the Tower. They're hilarious, dark, and completely compelling. Don't skip it — join the first tour of the day." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Bermondsey Beer Mile Walk", description: "Walk south from Tower Bridge into Bermondsey — London's craft brewery district, crammed into Victorian railway arches. A 1km stretch with 10+ craft breweries, all open on weekends and most on weekday afternoons.", details: ["Fourpure Brewing — great session IPAs and pilsners", "Brew By Numbers — some of London's most experimental beers", "Anspach & Hobday — the Smoked Porter alone is worth the trip", "Partizan Brewing — excellent seasonals"] },
            { title: "Maltby Street Market", description: "Just a short walk from the Beer Mile — this is the locals' answer to Borough Market. Food stalls under railway arches, less touristy, equally delicious. Perfect late lunch while drinking.", details: [] }
          ],
          meals: [
            { type: "🍺 Afternoon", name: "Bermondsey Beer Mile", description: "Walk in, sample a third/half pint at each arch, move on. The breweries are friendly and most have tasting paddles. Budget £15-20 each for a solid afternoon of craft beer.", meta: "Saturdays and Sundays are peak. Weekday afternoons from 12-6pm, most open" }
          ],
          tips: [{ type: "reddit", text: "The Bermondsey Beer Mile is legitimately one of the best things in London. Go on a Saturday afternoon and just walk from arch to arch. Anspach & Hobday's Smoked Porter is one of the best beers made in London.", cite: "r/CasualUK" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Thames Path: Shad Thames to Southwark", description: "Walk the Shad Thames riverside path — Victorian warehouse conversions with external walkways, mooring bollards, and stunning river views. One of London's most beautiful walks at golden hour.", details: [] }
          ],
          meals: [
            { type: "🍺 Pint", name: "The Mayflower Pub", description: "The pub from which the Pilgrim Fathers set sail for America in 1620. Still standing, still serving. Dark, creaking, timber-framed. Order a pint and sit in the river-facing seats.", meta: "117 Rotherhithe St · Historic gem off the tourist trail" },
            { type: "🍽️ Dinner", name: "Aqua Shard or Flat Iron (London Bridge)", description: "Flat Iron: exceptional steaks at £13-18 — London's best value steak. Walk-in only, queue is worth it. OR treat yourselves to Aqua Shard for the views.", meta: "Flat Iron · 84 Bermondsey St · £25-35 for two" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Borough Market Late Drinks", description: "Head back to Borough Market area — a cluster of excellent bars within a five-minute walk.", details: ["Rake Bar — tiny, legendary craft beer bar right in Borough Market. Excellent selection.", "Brew Dog London Bridge — larger, reliably good craft beer selection.", "Hide Bar — cocktails on Bermondsey Street, elegant and affordable."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Notting Hill Walk & Camden Nightlife",
      neighborhoods: "Notting Hill · Hyde Park · Camden Town",
      date: "May 19",
      mapPins: [
        { lat: 51.5157, lng: -0.2009, label: "Portobello Road Market", num: 1, cat: "activity", desc: "Antiques, vintage, food — best on Saturdays" },
        { lat: 51.5125, lng: -0.2060, label: "Notting Hill Streets", num: 2, cat: "activity", desc: "Pastel houses, bookshops, community feel" },
        { lat: 51.5098, lng: -0.1949, label: "Churchill Arms Pub", num: 3, cat: "food", desc: "Most photographed pub in London — draped in flowers" },
        { lat: 51.5073, lng: -0.1657, label: "Hyde Park", num: 4, cat: "activity", desc: "350 acres — Serpentine, Diana Fountain, Speaker's Corner" },
        { lat: 51.5394, lng: -0.1427, label: "Camden Market", num: 5, cat: "food", desc: "Chaotic, brilliant market with world food" },
        { lat: 51.5375, lng: -0.1424, label: "Camden Nightlife", num: 6, cat: "nightlife", desc: "Electric Ballroom, Jazz Café, Proud Camden" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Notting Hill Walk", description: "Explore London's most photogenic neighborhood at a leisurely pace. The pastel-painted terraces on Portobello Road, Elgin Crescent, and Lancaster Road are at their best in May morning light.", details: ["📍 Notting Hill Gate Tube (Central/Circle/District lines)"] },
            { title: "Portobello Road Market", description: "One of the world's great markets — antiques, vintage clothing, food stalls, and jewelry. Saturday is biggest, but Tuesday-Friday still has most shops open and is much less crowded.", details: ["💡 Best for: vintage clothing (the covered section at Golborne Road end), antique silver and maps, and artisan food at the top end."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Coffee Affair or The Grain Store", description: "Notting Hill has excellent independent cafés. Grab breakfast on Portobello Road before the market gets busy.", meta: "£10-15pp · Notting Hill area" }
          ],
          tips: [{ type: "tip", text: "The best Notting Hill photo streets: the blue houses on Portobello Road, the pastel terrace on St Luke's Mews (tiny, easy to miss), and the view down Ladbroke Grove from Holland Park Tube." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Churchill Arms Pub Stop", description: "The most photographed pub in London — absolutely draped in flower baskets and plants, especially in May bloom. Even if just for one pint in the flower-covered facade, it's unmissable. The Thai restaurant in the back is also genuinely good.", details: ["📍 119 Kensington Church St · Walk from Notting Hill"] },
            { title: "Hyde Park Walk", description: "Walk southeast through Hyde Park — 350 acres of London's finest parkland. In May it's spectacular. See the Serpentine lake, the Diana Memorial Fountain, and cut through to Marble Arch.", details: ["💡 The whole Notting Hill → Hyde Park → Camden route is about 8km but completely walkable through leafy streets."] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "The Lido Café (Hyde Park Serpentine)", description: "Café at the edge of the Serpentine lido, with outdoor seating and views over the water. Great salads, sandwiches, and the best park-lunch setting in London.", meta: "£12-18pp · Hyde Park · Open daily in summer months" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Camden Town", description: "Take the Tube to Camden Town — London's most chaotic, creative, and uniquely irreverent neighborhood. The Lock Market, the Canal, and the entire strip is unlike anywhere else.", details: ["📍 Camden Town Tube (Northern line)"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Camden Market Street Food", description: "Hawker-style international street food across Kerb Camden in the market. Korean fried chicken, Venezuelan arepas, Ethiopian, Japanese okonomiyaki. One of London's best casual food experiences.", meta: "£10-15pp · Camden Market · Open evenings" }
          ],
          tips: [{ type: "reddit", text: "Camden Market food is way better than its reputation suggests. The Korean fried chicken and the Japanese stalls in the basement area of the Lock Market are legit. Avoid the tourist-trap places at street level.", cite: "r/london" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Camden Music Venues & Bars", description: "Camden is London's live music heartland. Legendary venues within 200 metres of each other.", details: ["Jazz Café — world music, soul, funk. Great intimate venue.", "Electric Ballroom — classic rock, indie, club nights. Been going since 1938.", "Proud Camden — converted horse hospital with a rooftop bar and live acts.", "The World's End — enormous Wetherspoon's pub right by the Tube. Cheap pints, no-frills, always packed."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Check Dice FM or Resident Advisor for what's on at Camden venues. The Jazz Café often has excellent acts and an electric atmosphere. Book ahead if there's someone good on." }]
        }
      ]
    },
    {
      num: 6,
      title: "Greenwich & Brixton — History, Food & Late-Night Vibes",
      neighborhoods: "Greenwich · Deptford · Brixton",
      date: "May 20",
      mapPins: [
        { lat: 51.4769, lng: -0.0005, label: "Royal Observatory Greenwich", num: 1, cat: "activity", desc: "Prime Meridian — 0° longitude" },
        { lat: 51.4826, lng: -0.0096, label: "Cutty Sark", num: 2, cat: "activity", desc: "Famous tea clipper ship, beautifully restored" },
        { lat: 51.4813, lng: -0.0066, label: "Greenwich Market", num: 3, cat: "food", desc: "Covered market with excellent street food" },
        { lat: 51.4614, lng: -0.1148, label: "Brixton Market", num: 4, cat: "food", desc: "Caribbean food, independent traders, incredible energy" },
        { lat: 51.4622, lng: -0.1148, label: "Brixton Village", num: 5, cat: "food", desc: "Covered market with brilliant restaurants" },
        { lat: 51.4620, lng: -0.1140, label: "Brixton Nightlife", num: 6, cat: "nightlife", desc: "Dogstar, Electric Brixton, NMT, Phonox" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Thames Clipper to Greenwich", description: "Take the river bus from Embankment or London Bridge pier — sit on the top deck for the best views of London from the water. 30-40 minutes of Thames scenery.", details: ["💡 Oyster cards and contactless work on Thames Clippers. Get a return or a day pass."] },
            { title: "Cutty Sark & Greenwich Market", description: "Start with the beautifully restored Cutty Sark — the legendary tea clipper. Then walk through Greenwich Market (covered, great food stalls) for breakfast.", details: ["📍 Cutty Sark DLR station"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Greenwich Market Stalls", description: "Ethiopian coffee, wood-fired sourdough, arepas, or a full English from the market. Great casual options.", meta: "£8-12pp · Greenwich Market · Open daily" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Royal Observatory & Prime Meridian", description: "Climb the steep hill through Greenwich Park to the Royal Observatory. Stand on the Prime Meridian — 0° longitude — with one foot in each hemisphere. The views from the hilltop over the Cutty Sark, Queen's House, and Canary Wharf are iconic.", details: ["💡 The park and Prime Meridian photo (outside the Observatory) are free. £18pp to go inside. The view from the hill is magnificent either way."] },
            { title: "Greenwich Park Walk", description: "Spread out in the park — in May the wildflower meadows and rose garden are in bloom. One of London's most peaceful places on a sunny afternoon.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "The Old Brewery (Greenwich)", description: "Craft beer and seasonal British food in the stunning old Meantime brewery building at the Royal Naval College. Excellent burgers and pies.", meta: "£18-28pp · Pepys Building, Old Royal Naval College" }
          ],
          tips: [{ type: "reddit", text: "The Greenwich Observatory hill view is one of the best in London. Most tourists don't make it up here. The view of Canary Wharf reflected in the Thames with the Cutty Sark in the foreground — stunning.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Brixton — London's Most Vibrant Neighborhood", description: "Take the Overground or Tube to Brixton — London's most electric neighborhood for food and nightlife. The market, the restaurants, and the bar scene are all exceptional.", details: ["📍 Brixton Tube (Victoria line) · 20 min from central London"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Brixton Village Market", description: "The covered market has brilliant restaurants — Franco Manca (the original Franco Manca pizza is here), Elephant (tapas), Fish, Wings & Tings (Caribbean), and many more. Share plates around the market.", meta: "Coldharbour Lane · From £8-15pp · Very casual" }
          ],
          tips: [{ type: "tip", text: "Franco Manca original site in Brixton Village makes the best sourdough pizza in London. The queue is always worth it. Get the No. 2 with buffalo mozzarella." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Brixton Nightlife", description: "Brixton has London's best nightlife concentration outside of central London — and a better atmosphere than most of Zone 1.", details: ["Dogstar — legendary Brixton pub-turned-club, great drinks and later a DJ. Always busy.", "NMT (Never Mind the Bollocks) — Brixton's best pub for music and local crowd.", "Electric Brixton — 1,500-cap venue with the best sound system in south London.", "Phonox — intimate techno and house club. One of London's finest small clubs."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Brixton feels like the real London that tourists don't usually reach. The music at Phonox or Electric Brixton is world-class. Book tickets in advance." }]
        }
      ]
    },
    {
      num: 7,
      title: "Columbia Road Market, Canals & Farewell London Pints",
      neighborhoods: "Bethnal Green · Islington · Angel · King's Cross",
      date: "May 21",
      mapPins: [
        { lat: 51.5287, lng: -0.0723, label: "Columbia Road Flower Market", num: 1, cat: "activity", desc: "Sunday flower market — one of London's most beautiful" },
        { lat: 51.5362, lng: -0.1040, label: "Regent's Canal Walk", num: 2, cat: "activity", desc: "Walk the canal from Islington to Little Venice" },
        { lat: 51.5353, lng: -0.1034, label: "Angel & Islington", num: 3, cat: "food", desc: "Village atmosphere with great pubs and restaurants" },
        { lat: 51.5310, lng: -0.1233, label: "Exmouth Market", num: 4, cat: "food", desc: "Foodie street in Clerkenwell" },
        { lat: 51.5308, lng: -0.1238, label: "The Peasant Pub", num: 5, cat: "food", desc: "Excellent gastropub in Clerkenwell" },
        { lat: 51.5362, lng: -0.1024, label: "The Compton Arms", num: 6, cat: "food", desc: "Orwell's local — unchanged since he described it in 1946" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Columbia Road Flower Market", description: "One of London's most extraordinary experiences — Sunday only, 8am-2pm. A narrow East End street transforms into a riot of flowers and color. Traders call out in Cockney rhyming slang, everyone carries armfuls of blooms. Go between 9-11am before it gets packed.", details: ["📍 Columbia Road E2 · Bus or Overground to Hoxton/Bethnal Green", "💡 Sunday ONLY. Arrive by 9am for the best experience. Extremely photogenic."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Jones Dairy Café or Market Stalls", description: "Jones Dairy on Columbia Road has been here since the 1890s — brilliant coffee and pastries. Or grab a coffee and brownie from the market stalls themselves.", meta: "£6-10pp · Columbia Road E2 · Sunday morning only" }
          ],
          tips: [{ type: "reddit", text: "Columbia Road Flower Market on a Sunday morning is one of London's most genuinely joyful experiences. The vendors are characters, the flowers are cheap, the atmosphere is pure old East End.", cite: "r/london" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Regent's Canal Walk", description: "Walk along the Regent's Canal from Islington west toward King's Cross. One of London's most pleasant walking routes — narrowboats, towpaths, and a completely different pace of city. About 3km to King's Cross.", details: ["💡 Pick up the canal at Angel (City Road Basin) and walk west. You'll pass through the tunnel at Islington (boats go through, walkers climb over the hill) and emerge at King's Cross Basin."] },
            { title: "Exmouth Market & Clerkenwell", description: "A detour through Clerkenwell — one of London's most underrated neighborhoods. Exmouth Market is a pedestrianized street with excellent lunch spots. The area has brilliant gastropubs.", details: [] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Exmouth Market Food Stalls or The Peasant", description: "Exmouth Market stalls for casual eats (tacos, Ethiopian, gyros). Or The Peasant gastropub at the end of the market for proper sit-down British food.", meta: "£12-20pp · Exmouth Market EC1 · Both excellent" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Pub Crawl: Islington to Angel", description: "Islington has a brilliant cluster of old pubs for your final London evening.", details: [] }
          ],
          meals: [
            { type: "🍺 Farewell Pub 1", name: "The Compton Arms", description: "George Orwell's local — he described the ideal English pub in his famous 1946 essay 'The Moon Under Water' and this is widely believed to be the pub. Tiny, perfect, completely unchanged. One of the best pubs in London.", meta: "4 Compton Ave, N1 · Hidden backstreet gem" },
            { type: "🍺 Farewell Pub 2", name: "The Islington Tap or The Angelic", description: "Walk from The Compton Arms to Upper Street — a dense strip of pubs and restaurants. The Islington Tap has excellent craft beer; The Angelic has a great atmosphere for final evening drinks.", meta: "Upper Street, N1 · Multiple options on the strip" },
            { type: "🍽️ Farewell Dinner", name: "Ottolenghi Islington (Original)", description: "The original Ottolenghi on Upper Street — Yotam Ottolenghi's Israeli-Mediterranean café that changed London food. Beautiful mezze plates, excellent wine, perfect farewell dinner energy.", meta: "287 Upper Street, N1 · £30-45 for two · Book ahead" }
          ],
          tips: [{ type: "tip", text: "The Compton Arms is easy to miss — look for the tiny sign on Compton Avenue off Canonbury Road. It's one of those pubs that makes you understand why people love London." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Last London Walk", description: "Walk or Tube back to your hotel area. If you have time, take one last Thames walk — the South Bank at night, with St Paul's lit across the water and the Shard glowing, is London at its most beautiful.", details: ["💡 London is never really finished. But if seven days of walking, great pubs, brilliant food, and late nights haven't made you want to move here — nothing will."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Look out your last London train or Tube window as you head to the airport. The city is extraordinary. Come back." }]
        }
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
