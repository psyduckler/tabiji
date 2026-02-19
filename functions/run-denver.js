const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771476709360_100dhv",
  email: "bernard.j.huang@gmail.com",
  destination: "Denver, CO, USA",
  start_date: "2026-02-19",
  end_date: "2026-02-22",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-19T04:51:49.360Z",
  status: "pending"
};

const itineraryData = {
  destination: "Denver, CO, USA",
  countryEmoji: "🇺🇸",
  title: "Denver in 3 Nights: Mountains, Breweries & Mile-High Sunsets",
  subtitle: "RiNo → LoDo → Red Rocks → Golden → Capitol Hill",
  description: "A couple's guide to Denver in late February — crisp mountain air, 300 days of sunshine, world-class craft beer, and that electric blue-sky energy that makes everything feel possible. Winter means fewer crowds, cozy brewery taprooms, stunning snow-capped mountain views, and the chance to hit the slopes for a day trip.",
  duration: "3 nights / 4 days",
  dates: "Feb 19 – 22, 2026",
  budget: "Moderate",
  pace: "Relaxed — morning adventures, afternoon exploration, evening food & drinks",
  bestFor: "Couples, beer lovers & mountain enthusiasts",
  highlights: [
    "RiNo Art District — street art, breweries & creative restaurants",
    "Red Rocks Amphitheatre — iconic venue with stunning geology",
    "Union Station — beautifully restored Beaux-Arts train station",
    "200+ craft breweries in the metro area",
    "Larimer Square — Denver's oldest and most charming block",
    "Mile High views of the Rocky Mountain Front Range",
    "Denver Art Museum — Hamilton Building by Daniel Libeskind",
    "Cherry Creek — upscale shopping and dining",
    "Golden day trip — Coors Brewery, Clear Creek trail",
    "Capitol Hill — vibrant nightlife and diverse dining"
  ],
  essentials: [
    { title: "🚗 Getting Around", text: "Denver is spread out but manageable. RTD light rail connects the airport to Union Station ($10.50). Uber/Lyft are plentiful and cheap. RiNo, LoDo, and Capitol Hill are walkable clusters. Rent a car for Red Rocks and Golden day trips — or use rideshare ($25-35 each way to Red Rocks)." },
    { title: "💵 Budget Tips", text: "Expect $12-20 for casual lunches, $35-60pp for nice dinners. Brewery taprooms are great value ($6-8 pints). Happy hours are a Denver institution — most restaurants run 3-6pm with significant discounts. Red Rocks is free to visit during the day (no concert needed)." },
    { title: "❄️ February Weather", text: "Expect 40-50°F (4-10°C) during the day with intense sunshine, dropping to 15-25°F (-9 to -4°C) at night. Denver gets 300 days of sunshine — even winter days are often bright and blue. Snow is possible but usually melts fast at city altitude. Layer up: sunny mornings can turn cold quickly. Sunscreen is essential at 5,280 feet." },
    { title: "🏨 Where to Stay", text: "LoDo (Lower Downtown) for walkability to Union Station, restaurants, and nightlife. RiNo for the hipster-creative scene and brewery crawls. Capitol Hill for a more local, neighborhood feel. Cherry Creek for upscale quiet. All are 10-15 min from each other by car." },
    { title: "🍺 Beer Culture", text: "Denver takes craft beer seriously — over 200 breweries in metro area. Must-visits: Great Divide, Ratio Beerworks, Our Mutual Friend (all in RiNo). Most taprooms are dog-friendly and have food trucks. Brewery crawls in RiNo are a legitimate Denver activity — they're all walkable from each other." },
    { title: "📱 Useful Apps", text: "RTD (transit), Resy & OpenTable (restaurant reservations), AllTrails (hiking trails around Red Rocks and Golden), Uber/Lyft, Colorado DOT (road conditions for mountain drives)." }
  ],
  days: [
    {
      num: 1,
      title: "LoDo, Union Station & Larimer Square",
      neighborhoods: "LoDo · Union Station · Larimer Square",
      date: "Feb 19",
      mapPins: [
        { lat: 39.7530, lng: -104.9996, label: "Union Station", num: 1, cat: "activity", desc: "Beautifully restored 1914 Beaux-Arts hub" },
        { lat: 39.7475, lng: -104.9994, label: "Larimer Square", num: 2, cat: "food", desc: "Denver's oldest and most charming block" },
        { lat: 39.7486, lng: -105.0002, label: "Dairy Block", num: 3, cat: "food", desc: "Alley of boutiques, bars & restaurants" },
        { lat: 39.7392, lng: -104.9903, label: "Denver Art Museum", num: 4, cat: "activity", desc: "Libeskind's angular masterpiece" },
        { lat: 39.7395, lng: -104.9848, label: "Capitol Building", num: 5, cat: "activity", desc: "Stand exactly one mile high on the 13th step" },
        { lat: 39.7502, lng: -104.9953, label: "Coors Field Area", num: 6, cat: "food", desc: "Sports bars and pre-game restaurants" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Union Station", description: "Start at Denver's stunning Union Station — a 1914 Beaux-Arts train station beautifully restored into a food hall, cocktail bars, and boutique hotel. The Great Hall has massive chandeliers, leather couches, and a gorgeous shuffleboard area. Grab coffee and soak in the energy. Even in February, the morning light flooding through the windows is magical.", details: ["📍 1701 Wynkoop St · Free to explore, always open", "💡 The Terminal Bar inside Union Station makes excellent cocktails and has a great people-watching perch."] },
            { title: "Dairy Block & LoDo Stroll", description: "Walk through the Dairy Block — a European-style alley packed with boutiques, a bookstore, and restaurants. Then explore LoDo (Lower Downtown), Denver's historic warehouse district converted into restaurants, galleries, and lofts. The brick buildings and mountain views down every east-west street are quintessential Denver.", details: ["💡 The Dairy Block alley is covered and heated — perfect for a February morning browse."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Mercantile Dining & Provision (Union Station)", description: "Farm-to-table café inside Union Station from chef Alex Seidel. The pastry case is stunning — flaky croissants, seasonal danishes, and house-made granola. Excellent coffee. A refined but relaxed start.", meta: "$14-22pp · Inside Union Station · Walk-in for café side" }
          ],
          tips: [{ type: "tip", text: "Union Station is Denver's living room. Locals hang out here — it's not just a tourist spot. Come back in the evening for cocktails at the Terminal Bar or Cooper Lounge (upstairs, speakeasy vibes)." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Denver Art Museum", description: "The Denver Art Museum's Hamilton Building by Daniel Libeskind is an angular, titanium-clad masterpiece — stunning from outside and inside. The Western American art collection is world-class, and the Indigenous arts wing is exceptional. The building itself is worth the visit — every angle reveals a new geometric surprise.", details: ["📍 100 W 14th Ave Pkwy · $15 adults · Free first Saturday of each month", "💡 The rooftop terrace has incredible mountain views. Even in winter, pop up for photos."] },
            { title: "Colorado State Capitol", description: "Walk to the Colorado State Capitol. The 13th step on the west side is exactly one mile above sea level (5,280 feet) — marked with a brass medallion. On a clear February day, the Front Range views from the Capitol steps are jaw-dropping: 200 miles of snow-capped Rocky Mountains.", details: ["📍 200 E Colfax Ave · Free tours on weekdays", "💡 Stand on the 13th step and look west — the entire Front Range of the Rockies stretches across the horizon. One of Denver's best photo ops."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Rioja", description: "Jennifer Jasinski's Mediterranean gem on Larimer Square. The artisan cheese plate and house-made pastas are outstanding. Beautiful dining room, warm service. One of Denver's most consistently excellent restaurants.", meta: "$30-45pp · Larimer Square · Reservations on Resy" }
          ],
          tips: [{ type: "reddit", text: "Larimer Square is the one block in Denver that actually feels like a real city. String lights, historic buildings, great restaurants all in a row. It's especially beautiful in winter with the lights.", cite: "r/denver" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Larimer Square Evening", description: "Larimer Square at night is Denver at its most charming — a full block of Victorian buildings strung with thousands of lights. In winter, the glow against the dark sky is magical. Browse the boutiques, peek into galleries, and settle in for dinner. This is Denver's best date-night block.", details: ["💡 The string lights on Larimer Square are up year-round but hit different in winter — the contrast against fresh snow is gorgeous."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Guard and Grace", description: "Sleek, modern steakhouse in LoDo. Dry-aged steaks, incredible seafood tower, and a cocktail program that rivals standalone bars. The space is dramatic — soaring ceilings, open kitchen, buzzing energy. Perfect for a first-night splurge.", meta: "$55-80pp · 1801 California St · Reservations essential on Resy" }
          ],
          tips: [{ type: "reddit", text: "Guard and Grace is the steakhouse locals actually go to. Skip the chains. The cocktails are almost better than the steaks — almost. Get the old fashioned and the bone-in ribeye.", cite: "r/denver" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Cooper Lounge & Union Station", description: "End the night at Cooper Lounge — a hidden speakeasy-style bar on Union Station's mezzanine level. Craft cocktails, velvet couches, and a sophisticated crowd. Or head to Williams & Graham in RiNo — enter through a fake bookshelf into one of America's best cocktail bars.", details: ["💡 Williams & Graham: book ahead on Resy. The entrance is through a working bookshop — pull the right book and the shelf opens. Not kidding."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "RiNo Art District & Brewery Crawl",
      neighborhoods: "RiNo · Five Points · River North",
      date: "Feb 20",
      mapPins: [
        { lat: 39.7654, lng: -104.9812, label: "RiNo Art District", num: 1, cat: "activity", desc: "Street murals, galleries & creative energy" },
        { lat: 39.7716, lng: -104.9798, label: "Great Divide Brewing", num: 2, cat: "food", desc: "Denver craft beer pioneer" },
        { lat: 39.7680, lng: -104.9785, label: "Ratio Beerworks", num: 3, cat: "food", desc: "Industrial-chic taproom with great vibes" },
        { lat: 39.7640, lng: -104.9770, label: "Our Mutual Friend", num: 4, cat: "food", desc: "Neighborhood brewery with a cult following" },
        { lat: 39.7622, lng: -104.9805, label: "The Source", num: 5, cat: "food", desc: "Artisan food hall in a 1880s ironworks building" },
        { lat: 39.7630, lng: -104.9790, label: "Denver Central Market", num: 6, cat: "food", desc: "Indoor market with local vendors" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "RiNo Street Art Walk", description: "RiNo (River North) Art District is Denver's creative heart — a former industrial zone now covered in massive, vibrant murals. Every alley, warehouse wall, and loading dock has been transformed into public art. Walk along Larimer Street between 25th and 38th — the density of murals is incredible. February means clear skies and perfect light for photos.", details: ["📍 Start at Larimer & 25th, walk north. The best murals cluster between 30th-36th on Larimer and Walnut.", "💡 The CRUSH Walls festival adds new murals every September — the collection keeps growing. Look for work by Pat Milbery, Jaime Molina, and Detour."] },
            { title: "Denver Central Market", description: "Browse the Denver Central Market — a curated food hall in a RiNo warehouse. Local vendors sell artisan chocolate (Temper), craft coffee (Crema), wood-fired bagels, and more. Great for grazing and getting a feel for Denver's food scene.", details: ["📍 2669 Larimer St · Open daily 8am-8pm"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Rosenberg's Bagels & Delicatessen", description: "New York-style bagels that actually live up to the claim — the owner shipped in NYC water to perfect them. Hand-rolled, kettle-boiled, the real deal. The lox bagel is outstanding. A RiNo essential.", meta: "$12-18pp · 725 E 26th Ave · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Rosenberg's is legit the best bagels outside New York. The guy literally imports NYC water. Get the everything bagel with lox — don't overthink it.", cite: "r/denver" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "RiNo Brewery Crawl", description: "Time for a Denver rite of passage: the RiNo brewery crawl. All walkable within 15 minutes of each other. Start at Ratio Beerworks (industrial-chic taproom, excellent IPAs, great music). Walk to Our Mutual Friend (neighborhood gem, Belgian-inspired, cozy). Then Great Divide Barrel Bar (their barrel-aged collection is legendary). Pace yourselves — this is a marathon, not a sprint.", details: ["📍 Ratio → OMF → Great Divide is a natural walking route, all within 10-15 min of each other", "💡 Most RiNo breweries have food trucks parked outside or allow delivery. Taprooms are dog-friendly and have board games."] },
            { title: "The Source", description: "Visit The Source — an artisan food market in an 1880s ironworks building. Acorn (wood-fired everything) is the anchor restaurant. Browse RiNo Made (local crafts), grab provisions, and soak in the industrial-meets-artisan vibe.", details: ["📍 3350 Brighton Blvd · Acorn is excellent for a sit-down lunch or early dinner"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Work & Class", description: "RiNo's best restaurant — a butcher-shop-meets-dining-room serving incredible smoked meats, empanadas, and South American-inspired plates. The brisket is legendary. Loud, fun, communal energy. Cash-conscious and delicious.", meta: "$25-40pp · 2500 Larimer St · Reservations recommended" }
          ],
          tips: [{ type: "tip", text: "Brewery taproom etiquette in Denver: tip $1/beer at the bar, don't be loud on the phone, bring your own food or order from food trucks outside, and always try the seasonal/experimental taps first." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Five Points & Welton Street", description: "Walk south into Five Points — Denver's historic Black neighborhood, now a hub for jazz, soul food, and some of the city's best restaurants. Welton Street is the main artery. In February, the cozy restaurants and dim cocktail bars feel especially inviting.", details: ["💡 Five Points has deep jazz history — it was once called 'The Harlem of the West.' The spirit lives on in spots like Nocturne."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Tavernetta", description: "Stunning Italian restaurant near Union Station by the Frasca team. House-made pasta, wood-fired dishes, and an Italian wine list that goes deep. The space is gorgeous — warm woods, open kitchen, soft lighting. One of the best meals in Denver, period.", meta: "$50-70pp · 1889 16th St · Reservations essential on Resy" }
          ],
          tips: [{ type: "reddit", text: "Tavernetta is the best Italian in Denver and it's not close. The cacio e pepe and the lamb are life-changing. Book at least a week ahead — it fills up.", cite: "r/denver" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Nocturne Jazz Club", description: "End the night at Nocturne — a gorgeous jazz supper club in RiNo. Live jazz every night, excellent cocktails, and a vibe that feels like stepping into a 1950s Manhattan club. Intimate, romantic, and uniquely Denver. Reserve a table for the best experience.", details: ["📍 1330 27th St · Reservations recommended · Shows at 7pm and 9pm typically", "💡 The 9pm set is usually more intimate and relaxed. Order the Old Fashioned — they make it perfectly."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Red Rocks, Golden & Mountain Views",
      neighborhoods: "Red Rocks · Golden · Morrison",
      date: "Feb 21",
      mapPins: [
        { lat: 39.6654, lng: -105.2057, label: "Red Rocks Amphitheatre", num: 1, cat: "activity", desc: "Iconic natural amphitheatre — free to visit" },
        { lat: 39.6634, lng: -105.2047, label: "Red Rocks Trading Post Trail", num: 2, cat: "activity", desc: "Easy 1.4-mile loop through red rock formations" },
        { lat: 39.7555, lng: -105.2211, label: "Golden", num: 3, cat: "activity", desc: "Charming mountain town at the foot of the Rockies" },
        { lat: 39.7586, lng: -105.2173, label: "Coors Brewery", num: 4, cat: "food", desc: "World's largest single-site brewery — free tours" },
        { lat: 39.7536, lng: -105.2230, label: "Clear Creek Trail", num: 5, cat: "activity", desc: "Walk along the creek through downtown Golden" },
        { lat: 39.7393, lng: -105.1780, label: "Lookout Mountain", num: 6, cat: "activity", desc: "Buffalo Bill's grave and panoramic Denver views" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Red Rocks Amphitheatre", description: "Drive 30 minutes west to Red Rocks — one of the most stunning natural formations in America. The amphitheatre is carved between two 300-foot red sandstone monoliths, and it's free to visit when there's no show. Walk the rows, take in the acoustics, and stare at the mountain views. In February, morning light paints the rocks gold and orange. If you're lucky, there'll be fresh snow on the formations.", details: ["📍 18300 W Alameda Pkwy, Morrison · Free parking and entry during the day", "💡 The Performers Hall of Fame museum inside is free and fascinating — see the history of every legendary show held here."] },
            { title: "Trading Post Trail", description: "Hike the Trading Post Trail — an easy 1.4-mile loop through the red rock formations. Stunning geological layers, mountain views, and in winter, the contrast of red rock against blue sky (and possibly snow) is breathtaking. The trail is well-maintained and accessible.", details: ["📍 Trailhead is at the Trading Post, south end of the park", "💡 Bring layers — it can be windy and 10-15°F cooler up in the rocks than in the city. Sunglasses essential."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Snooze, an A.M. Eatery", description: "Denver-born breakfast chain that's become a cult favorite. Creative pancake flights (pineapple upside-down, sweet potato), incredible eggs benedict variations, and a build-your-own bloody mary bar. Fun, colorful, and always buzzing.", meta: "$16-24pp · Multiple Denver locations · Expect a wait on weekends, put your name in on Yelp Waitlist" }
          ],
          tips: [{ type: "reddit", text: "Red Rocks during the day (no concert) is completely free and genuinely one of the coolest things in Colorado. Run the stairs for a workout, or just sit and absorb the view. Go in the morning for the best light and fewer people.", cite: "r/denver" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Golden", description: "Drive 15 minutes north to Golden — a charming mountain town at the mouth of Clear Creek Canyon. The main street feels like a Western movie set, with the Rockies rising dramatically behind it. A huge arch over Washington Ave reads 'Howdy Folks! Welcome to Golden, Where the West Lives.' In February, Clear Creek may have ice formations and the mountains are snow-covered.", details: ["📍 Take I-70 west from Red Rocks, about 15-20 minutes", "💡 Golden is home to Colorado School of Mines and has a surprising number of great restaurants for its size."] },
            { title: "Coors Brewery Tour", description: "Tour the Coors Brewery — the world's largest single-site brewery. The free tour walks through the brewing process in a massive facility nestled in a mountain valley. Three free beers at the end. Love it or not, it's an impressive operation and a Colorado institution.", details: ["📍 13th & Ford St, Golden · Free tours, first-come-first-served · Thursday-Sunday in winter", "💡 Tours fill up fast even in winter. Arrive by 11am to guarantee a spot. Photo ID required for beer tasting."] },
            { title: "Clear Creek Trail", description: "Walk along Clear Creek through downtown Golden. The trail follows the creek with mountain views, kayak features (in summer), and connects downtown to the canyon. In February, the creek runs cold and clear, and the surrounding peaks may have fresh snow. Peaceful and beautiful.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bob's Atomic Burgers", description: "Tiny, retro burger joint in Golden. Smashed burgers, hand-cut fries, and milkshakes in a space-age themed shack. Unpretentious, delicious, and perfect fuel for a day of exploring. Cash only.", meta: "$12-18pp · Golden · Cash only, walk-in" }
          ],
          tips: [{ type: "tip", text: "Lookout Mountain is a quick detour from Golden — drive up for panoramic views of Denver and the plains. Buffalo Bill is buried at the top (Buffalo Bill Museum & Grave). The lookout is free and the views are incredible on a clear winter day." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Cherry Creek Evening", description: "Head back to Denver and explore Cherry Creek — Denver's upscale neighborhood with tree-lined streets, art galleries, and excellent restaurants. It's quieter and more refined than LoDo or RiNo. In February, the neighborhood feels cozy and intimate — perfect for a last full evening.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Matsuhisa Denver", description: "Nobu Matsuhisa's original concept — elevated Japanese with Peruvian influences. The black cod miso is legendary for a reason. Sushi is pristine, the rock shrimp tempura is addictive. Intimate, warm, and impeccable. A special-occasion dinner that delivers.", meta: "$60-85pp · 303 Josephine St (Cherry Creek) · Reservations essential" }
          ],
          tips: [{ type: "reddit", text: "If Matsuhisa is too spendy or booked, Sushi Den in South Denver is the locals' GOAT for sushi. Fish flown in daily from their family's fish market in Japan. Also: Uchi (South Broadway) is incredible if you like Austin-style omakase.", cite: "r/denver" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Capitol Hill Nightcap", description: "Finish the night on Capitol Hill — Denver's most eclectic neighborhood for nightlife. Adrift (tiki bar with over-the-top cocktails), Thin Man (craft cocktails in a moody lounge), or just bar-hop down Broadway. In winter, the cozy dive bars and cocktail spots feel especially welcoming.", details: ["💡 Broadway between Ellsworth and Alameda is the densest strip of bars in Denver. You'll find everything from dives to craft cocktail spots within a few blocks."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Morning Coffee, Last Looks & Departure",
      neighborhoods: "Capitol Hill · Congress Park · Downtown",
      date: "Feb 22",
      mapPins: [
        { lat: 39.7401, lng: -104.9658, label: "Capitol Hill", num: 1, cat: "food", desc: "Final Denver brunch" },
        { lat: 39.7325, lng: -104.9615, label: "Congress Park", num: 2, cat: "activity", desc: "Charming residential streets" },
        { lat: 39.7530, lng: -104.9996, label: "Union Station", num: 3, cat: "activity", desc: "One last look before heading out" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Capitol Hill Brunch", description: "Cap Hill is Denver's brunch capital. Take a slow morning — walk the residential streets with their beautiful old homes and mountain views. February mornings in Denver are often crisp, clear, and bright. Grab coffee, sit on a sunny patio (yes, even in February — Denverites patio in all weather), and soak in your last hours.", details: [] },
            { title: "Last-Minute Picks", description: "Grab Denver souvenirs at Tattered Cover Book Store (independent bookshop, a Denver institution) or pick up local hot sauce, craft chocolate, or Colorado coffee beans. If you have time, swing by City Park for one last look at the mountain panorama from the east side.", details: ["📍 Tattered Cover: 2526 E Colfax Ave · Denver's beloved independent bookstore since 1971", "💡 City Park's eastern edge has the classic 'Denver skyline with mountains behind' photo angle."] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Steuben's", description: "Retro American comfort food diner that takes brunch seriously. Green chile smothered everything (a Colorado staple), biscuits and gravy, chicken and waffles. Big portions, strong cocktails, cheerful energy. A proper Denver farewell.", meta: "$18-28pp · 523 E 17th Ave (Uptown) · Walk-in or OpenTable, expect a wait weekends" }
          ],
          tips: [{ type: "tip", text: "Denver International Airport (DEN) is 30-40 minutes from downtown. The A Line train from Union Station is $10.50 and runs every 15 minutes — easy and stress-free. Leave 2.5 hours before your flight; DEN is huge." }]
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
