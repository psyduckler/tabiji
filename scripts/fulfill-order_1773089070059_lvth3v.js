const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: "order_1773089070059_lvth3v",
  email: "hello@scanmyplan.com",
  destination: "San Antonio, TX, USA",
  start_date: "2026-03-12",
  end_date: "2026-03-15",
  group_size: "1",
  travel_style: "",
  dining: "",
  budget: "$1,000-2,000",
  requests: "",
  amount: "0.00",
  timestamp: "2026-03-09T20:44:30.059Z",
  status: "pending"
};

const itineraryData = {
  destination: "San Antonio, TX, USA",
  countryEmoji: "🇺🇸",
  title: "San Antonio in 3 Days: The Alamo, UNESCO Missions & Authentic Tex-Mex",
  subtitle: "River Walk · Historic Missions · Pearl District · King William · Southtown",
  description: "Three days in Texas' most historically rich city — where 18th-century Spanish missions rise above the cottonwood trees, the River Walk winds through a limestone canyon lined with restaurants and live music, and the Tex-Mex is the real deal (not the watered-down chain version). San Antonio for solo travelers is a dream: walkable downtown, an extraordinary UNESCO World Heritage Site hiding in plain sight, and a food scene that goes from old-school puffy tacos at dawn to craft cocktails in the Pearl District at midnight. March is perfect — wildflowers are blooming across the Hill Country, temperatures are warm without being brutal, and the city is alive without peak summer crowds.",
  duration: "3 nights / 3 days",
  dates: "March 12–15, 2026",
  budget: "Mid-Range ($1,000–2,000 total)",
  pace: "Active — history-packed mornings, relaxed afternoons, lively evenings",
  bestFor: "Solo history lovers, Tex-Mex fanatics, architecture enthusiasts & first-time San Antonio visitors",
  highlights: [
    "The Alamo — Texas' most iconic landmark, the 'Shrine of Texas Liberty,' in the heart of downtown",
    "San Antonio Missions National Historical Park — the only UNESCO World Heritage Site in Texas, spanning four 18th-century Spanish colonial missions",
    "The River Walk (Paseo del Río) — a 15-mile riverside promenade lined with restaurants, bars, and live music beneath ancient cypress trees",
    "Pearl District — a stunning converted Pearl Brewery complex that's now San Antonio's hippest food and culture hub",
    "King William Historic District — a Victorian neighborhood of mansions and art galleries along the San Antonio River",
    "Natural Bridge Caverns — the largest caverns in Texas, just 30 minutes from downtown, with jaw-dropping stalactite formations",
    "Mi Tierra Café y Panadería — 24-hour Tex-Mex institution in Market Square, open since 1941, a San Antonio rite of passage",
    "Southtown Arts District & Blue Star Arts Complex — local galleries, studios, and restaurants in a converted warehouse complex",
    "San Fernando Cathedral — the oldest cathedral in the US, built in 1731, standing guard over the city's historic main plaza",
    "2M Smokehouse BBQ — a Texas Monthly Top 50 BBQ pit run by a veteran and his wife, putting San Antonio on the BBQ map"
  ],
  essentials: [
    { title: "✈️ Getting There & Around", text: "San Antonio International Airport (SAT) is 8 miles from downtown. Uber/Lyft runs about $15-20 to the River Walk area. Downtown San Antonio is surprisingly walkable — the Alamo, River Walk, Market Square, La Villita, and King William District are all connected on foot or via the free VIA streetcar. For the Missions Trail (Day 2), rent a bike from San Antonio B-cycle ($3/ride, multiple docking stations) or use Uber/Lyft between missions. For Natural Bridge Caverns (Day 3), you'll need a rental car or rideshare (~$25-30 each way) — it's 30 minutes north on I-35." },
    { title: "💵 Budget Reality", text: "San Antonio is one of the most affordable major cities in Texas. Mid-range hotels near the River Walk: $120-200/night. Budget picks in Southtown or Pearl area: $80-130/night. Tex-Mex at legendary spots: $12-22 for a full plate. BBQ: $20-35 for a serious spread. River Walk tourist restaurants: pricier ($25-45 entrees) — worth it for ambiance on one evening, but eat like a local the rest. Daily budget for food + activities: $80-150/day comfortably. Total 3-day trip: $600-900 (excluding flights) leaves room in the $1-2K budget for splurging on a good hotel or day trip." },
    { title: "🌸 March Weather", text: "Mid-March in San Antonio is glorious: highs of 22-27°C (72-80°F), low humidity, blue skies. This is arguably the best time to visit — spring wildflowers are blooming across the Hill Country, the River Walk cypress trees are leafing out, and the famous San Antonio Stock Show & Rodeo has just wrapped up. Light layers for morning and evening (can drop to 12-15°C at night). Comfortable walking shoes are essential — you'll be covering miles of limestone paths and river trails." },
    { title: "🏨 Where to Stay", text: "For the full experience, stay in the River Walk/Downtown zone (zip 78205) or Southtown. Best mid-range picks: Hotel Emma at Pearl ($300-450/night, stunning converted brewhouse, a splurge worth considering), Hotel Havana on the River ($180-250/night, boutique Cuban-inspired), or the Menger Hotel adjacent to the Alamo ($150-220/night, historical significance — Teddy Roosevelt recruited his Rough Riders here). Budget-minded: La Quinta Inn River Walk or Hampton Inn and Suites Downtown ($120-160/night). Book ahead — March sees strong weekend demand." },
    { title: "🌮 Tex-Mex & BBQ Culture", text: "San Antonio is the birthplace of Tex-Mex cuisine — this is where chili queens sold fiery stews from pushcarts in the 1800s, where puffy tacos were invented (at Henry's Puffy Tacos), and where generations of Mexican-American families have refined enchiladas, fajitas, and breakfast tacos to an art form. The rules: avoid chain restaurants anywhere near the River Walk tourist corridor, seek out family-owned spots in neighborhoods, and order the puffy taco at least once. For BBQ: San Antonio's scene is up-and-coming — 2M Smokehouse is the city's breakout star, run by a veteran who smokes everything over post oak. No sauce needed." },
    { title: "🏛️ History & Culture Tips", text: "The Alamo is free but the museum exhibit requires a timed entry ticket ($21) — book online at thealamo.org to skip long queues. The four UNESCO Missions are all free National Park Service sites. San Fernando Cathedral on Main Plaza is free to visit and stunning — look for the 'Light Up the Night' sound and light show projected on its facade in the evenings (free, usually 9-10pm). The McNay Art Museum (free on Sundays) has one of the finest modern art collections in Texas. The Briscoe Western Art Museum on the River Walk is excellent for understanding the region's ranching heritage ($15)." },
    { title: "📱 Apps & Getting Connected", text: "Download the VIA Metropolitan Transit app for bus routes (rarely needed downtown, but useful). Google Maps works well for navigation. Download the NPS app for audio guides at the Missions — it works offline and is genuinely excellent. San Antonio B-cycle app for bike rentals. OpenTable or Resy for restaurant reservations — book Pearl District and Southtown restaurants at least a day ahead, especially Friday/Saturday. The SATX app has event listings. Good cell coverage throughout downtown on all major carriers." }
  ],
  days: [
    {
      num: 1,
      title: "The Alamo, River Walk & Market Square",
      neighborhoods: "Downtown · Alamo Plaza · River Walk · Market Square · La Villita",
      date: "March 12",
      mapPins: [
        { lat: 29.4260, lng: -98.4861, label: "The Alamo", num: 1, cat: "activity", desc: "Texas' most iconic landmark — the 1718 Spanish mission turned battlefield" },
        { lat: 29.4217, lng: -98.4895, label: "River Walk (Paseo del Río)", num: 2, cat: "activity", desc: "15-mile riverside promenade — heart of San Antonio" },
        { lat: 29.4257, lng: -98.4941, label: "San Fernando Cathedral", num: 3, cat: "activity", desc: "Oldest cathedral in the US, built 1731 — stunning interior" },
        { lat: 29.4261, lng: -98.4962, label: "Mi Tierra Café y Panadería", num: 4, cat: "food", desc: "24-hour Tex-Mex legend in Market Square, open since 1941" },
        { lat: 29.4209, lng: -98.4883, label: "La Villita Historic Arts Village", num: 5, cat: "activity", desc: "San Antonio's original settlement — craft galleries & plazas" },
        { lat: 29.4218, lng: -98.4843, label: "Tower of the Americas", num: 6, cat: "activity", desc: "750-ft observation tower with panoramic city views" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "The Alamo",
              description: "Start where Texas history begins. The Alamo — originally Mission San Antonio de Valero, founded in 1718 — was the site of the famous 1836 battle where 189 Texan defenders held out for 13 days against Santa Anna's 1,800-strong Mexican army before falling. 'Remember the Alamo' became the battle cry that won Texas independence six weeks later. The restored chapel is free; the Long Barrack Museum and the new Alamo museum experience require a timed ticket ($21) and are absolutely worth it for the immersive exhibits on the siege, its defenders, and the complex politics of Texas independence.",
              details: [
                "📍 300 Alamo Plaza, San Antonio · Free chapel entry; museum tickets $21 (book at thealamo.org)",
                "💡 Book timed entry tickets online in advance — walk-up queues can stretch 45-60 minutes in March.",
                "💡 The Long Barrack (the original convento of the mission) has the most powerful exhibits — artifacts from the battle, Bowie's knife, and personal effects of the defenders.",
                "⚠️ No photography inside the Shrine (chapel). The courtyard and grounds are fully photogenic — morning light on the limestone facade is beautiful."
              ]
            },
            {
              title: "Alamo Plaza & San Fernando Cathedral",
              description: "After the Alamo, walk west through Alamo Plaza to San Fernando Cathedral — the oldest cathedral sanctuary in the United States, built 1731-1750 by Canary Island settlers. Santa Anna famously flew a red 'no quarter' flag from its bell tower during the siege of the Alamo in 1836. The interior is breathtakingly ornate — gilded altars, painted ceilings, and a profound sense of historical weight. The Main Plaza outside is the original heart of colonial San Antonio.",
              details: [
                "📍 115 Main Plaza · Free entry · Open daily 6am-7pm",
                "💡 Come back at night (9-10pm) for the 'Light Up the Night' sound and light show projected on the cathedral facade — free and genuinely spectacular."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Bakery Lorraine",
              description: "San Antonio's beloved French-inspired bakery, with multiple locations including one in the Pearl District and Alamo Heights. The butter croissants, kouign-amann, and pastries are exceptional. Line up early on weekdays for the freshest selection. A proper start to the day.",
              meta: "$10-16pp · Multiple locations · Opens 7am weekdays"
            }
          ],
          tips: [
            {
              type: "tip",
              text: "The Alamo is genuinely moving if you go in understanding the history. It's small — the chapel is surprisingly intimate for a site of such enormous significance. Take time in the Long Barrack museum and read the defenders' stories. The politics of the Texas Revolution are complex, but the courage of those 189 people is undeniable."
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "River Walk Exploration",
              description: "Descend to the River Walk — the Paseo del Río — San Antonio's extraordinary below-street-level promenade that winds for 15 miles along the San Antonio River. Lined with ancient bald cypress trees, limestone pathways, arched bridges, and hundreds of restaurants and bars, the River Walk is one of the great urban public spaces in America. Walk south from the Alamo toward La Villita — the 'little village,' San Antonio's original colonial settlement, now full of craft galleries and artisan studios.",
              details: [
                "📍 Multiple River Walk access stairs along Commerce St and Commerce to Losoya area",
                "💡 The River Walk is famous for tourist-priced restaurants — walk past the first dozen and find spots where locals actually eat. Or use it purely as a walking/atmosphere experience and eat elsewhere.",
                "💡 Rent a bike from a B-cycle station to cover more ground on the Mission Reach section south of downtown."
              ]
            },
            {
              title: "La Villita Historic Arts Village & Tower of the Americas",
              description: "La Villita is San Antonio's original neighborhood — established in the early 1700s before the rest of the city existed. Today it's a charming collection of historic adobe and limestone buildings housing local artisan galleries, craft studios, and small restaurants. Across the street, the 750-foot Tower of the Americas (built for the 1968 World's Fair) offers breathtaking 360-degree views of the city and the Hill Country beyond from its observation deck.",
              details: [
                "📍 La Villita: between South Alamo St and the River Walk · Free to wander",
                "📍 Tower of the Americas: 739 E César Chávez Blvd · Observation deck $14 · Opens 10am",
                "💡 The Tower is best at sunset — the golden light across the limestone city and the Hill Country ridgeline to the northwest is extraordinary."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Schilo's Delicatessen",
              description: "A San Antonio institution since 1917 — a German-Texan deli a block from the Alamo that serves everything from split pea soup to enchiladas. It's cheap, fast, beloved by locals and travel writers alike, and the root beer is homemade. The lunch crowd is a cross-section of downtown San Antonio: tourists, city workers, and third-generation regulars.",
              meta: "$10-18pp · 424 E Commerce St · No reservations, walk-in"
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "Skip the River Walk restaurants for actual meals — they're overpriced and mediocre. Use the River Walk as your walking corridor and eat at spots one block off in either direction. Schilo's for lunch, Mi Tierra for late dinner, and anything in the Pearl for elevated. The vibe on the River Walk is genuinely great, just don't eat there.",
              cite: "r/sanantonio"
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Market Square & Mi Tierra",
              description: "Walk or ride to Market Square (El Mercado) — the largest Mexican market in the United States outside of Mexico, a block of covered stalls selling jewelry, leather goods, pottery, clothing, and every kind of artisanal Mexican craft. The adjacent Mi Tierra Café y Panadería is the cultural anchor: open 24 hours since 1941, covered in Christmas lights year-round, with enormous murals of Mexican-American history on the walls. Order the cheese enchiladas, the barbacoa, or the puffy tacos. Finish with a pan dulce from the attached bakery.",
              details: [
                "📍 Market Square: 514 W Commerce St · Open daily 10am-8pm (shops vary)",
                "📍 Mi Tierra: 218 Produce Row · Open 24 hours · No reservations",
                "💡 Mi Tierra's Christmas light ceiling is legendary — on since the restaurant opened in 1941. The murals are worth studying: they document 200 years of San Antonio Mexican-American life.",
                "💡 The attached bakery sells conchas, churros, and pan dulce for around $1-2 each — grab a bag for tomorrow's breakfast."
              ]
            },
            {
              title: "San Fernando Cathedral Night Show",
              description: "At 9pm, San Fernando Cathedral hosts 'En Luz de Historia' — a stunning sound and light show projected on the 1738 facade, telling the 300-year history of San Antonio with dramatic visual storytelling. The entire Main Plaza fills with locals and visitors watching together. Completely free.",
              details: [
                "📍 115 Main Plaza · Free · Runs nightly at 9pm and 9:30pm (check schedule)",
                "💡 Arrive 10-15 minutes early for a good viewing position on the Plaza."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Mi Tierra Café y Panadería",
              description: "You've already been in the market — now eat. Mi Tierra is open 24 hours and serves classic San Antonio Tex-Mex: cheese enchiladas with chili gravy, carne guisada, puffy tacos, and the house margaritas made with fresh lime. Loud, festive, covered in lights. Order the Mexican breakfast plate if you arrive early or late — eggs with nopalitos and refried beans is outstanding any hour.",
              meta: "$18-30pp · 218 Produce Row · Open 24 hours"
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "Mi Tierra is touristy AND a genuine institution — both things are true. Go once. The murals, the Christmas lights, the 24-hour chaos, the margaritas — it's authentically San Antonio in a way few places are. Just don't go on a Saturday night expecting a quiet dinner.",
              cite: "r/sanantonio"
            }
          ]
        }
      ]
    },
    {
      num: 2,
      title: "UNESCO Missions Trail & King William District",
      neighborhoods: "Mission Trail · King William · Southtown · Pearl District",
      date: "March 13",
      mapPins: [
        { lat: 29.3954, lng: -98.4682, label: "Mission Concepción", num: 1, cat: "activity", desc: "Best-preserved Spanish colonial church in the US, built 1731" },
        { lat: 29.3641, lng: -98.4665, label: "Mission San José", num: 2, cat: "activity", desc: "The 'Queen of the Missions' — largest and most ornate UNESCO mission" },
        { lat: 29.3356, lng: -98.4710, label: "Mission San Juan", num: 3, cat: "activity", desc: "Remote mission with wetlands trail along the river" },
        { lat: 29.3127, lng: -98.4745, label: "Mission Espada", num: 4, cat: "activity", desc: "Southernmost mission, oldest acequia (irrigation) system in the US" },
        { lat: 29.4140, lng: -98.4880, label: "King William Historic District", num: 5, cat: "activity", desc: "Victorian mansions & art galleries along the San Antonio River" },
        { lat: 29.4401, lng: -98.4784, label: "Pearl District", num: 6, cat: "food", desc: "Converted Pearl Brewery — SA's best food, drink & culture hub" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Mission Concepción",
              description: "Start the UNESCO Missions Trail at Mission Concepción — the oldest unrestored stone church in the United States, built in 1731. The twin bell towers and the limestone exterior are beautiful, but what stops you cold is the interior: geometric polychrome frescoes in reds, oranges, and yellows, painted by the Franciscan friars and their indigenous converts, still vivid after 300 years. The 'Eye of God' fresco in the sacristy is the most striking. Active Catholic parish — you may hear mass in progress.",
              details: [
                "📍 807 Mission Rd · Free (NPS site) · Open daily 9am-5pm",
                "💡 Download the NPS app for the Missions before you go — the audio guides are excellent and work offline.",
                "💡 The painted geometric diamonds on the exterior (now mostly faded) were originally blazing with color to help indigenous converts recognize the mission from far away."
              ]
            },
            {
              title: "Mission San José — Queen of the Missions",
              description: "Mission San José is the crown jewel of the San Antonio Missions — the largest, most ornate, and most beautiful of the four. Founded in 1720, it housed over 300 Coahuiltecan indigenous converts at its peak and was a self-sufficient agricultural and manufacturing community. The intricate 'Rosa's Window' (La Ventana de Rosa) carved in limestone is considered one of the finest examples of Baroque architecture in North America. The granary, the soldier quarters, the acequia (irrigation channel), and the enormous convento complex are all intact and fascinatingly detailed.",
              details: [
                "📍 6701 San José Dr · Free (NPS site) · Open daily 9am-5pm",
                "💡 The mariachi mass every Sunday at noon at Mission San José is legendary — hundreds of people attend and it's completely free. If you're here on a Sunday, plan your day around it.",
                "💡 Walk the full perimeter of the mission walls — the scale of the complex (it was a small city) only becomes apparent when you see the entire wall circuit."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast / Coffee",
              name: "South Alamo Street Cafés",
              description: "Grab breakfast from a café on South Alamo Street in Southtown before heading to the missions. Halcyon (a 24-hour hangout with board games and good coffee) or Lulu's Bakery are both good options for a quick, quality start before hitting the trail.",
              meta: "$8-14pp · South Alamo St corridor · Opens 7am"
            }
          ],
          tips: [
            {
              type: "tip",
              text: "The four UNESCO Missions are all National Park Service sites and completely free. They're strung along the San Antonio River about 8 miles from downtown to Espada. The Mission Reach trail connects them by bike path — rent a B-cycle for $3 and ride the whole stretch in 2-3 hours. It's a genuinely beautiful ride along the river through cottonwood groves and open fields."
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Mission San Juan & Mission Espada",
              description: "Continue south to Mission San Juan (founded 1731) — the most remote and serene of the four missions, with a short wetlands trail along the river that's excellent for birds in March. Then to Mission Espada — the southernmost mission, founded as San Francisco de los Tejas in East Texas in 1690 and moved here in 1731. The Espada Acequia (irrigation aqueduct) just north of the mission is remarkable: built in the 1730s, it still carries water today and is the oldest functioning irrigation system in the United States.",
              details: [
                "📍 Mission San Juan: 9101 Graf Rd · Free · Open daily 9am-5pm",
                "📍 Mission Espada: 10040 Espada Rd · Free · Open daily 9am-5pm",
                "💡 The wetlands trail at Mission San Juan is excellent for spring birding — March brings migrating warblers and shorebirds. Bring binoculars if you have them.",
                "💡 If biking, the Mission Reach trail is well-marked from mission to mission. Add 30-40 minutes between each mission for the scenic river path."
              ]
            },
            {
              title: "King William Historic District",
              description: "Return north to the King William Historic District — San Antonio's grandest 19th-century neighborhood, where wealthy German merchants built elaborate Victorian mansions along the tree-lined streets above the San Antonio River. Today it's a mix of historic homes (several open as B&Bs), art galleries, and some of SA's most interesting restaurants. Walk the main streets: King William, Madison, and Turner. The Guenther House (1860s Victorian manse turned restaurant) is the anchor attraction.",
              details: [
                "📍 South of downtown along King William St · Free to wander",
                "💡 The King William Association offers a walking tour map downloadable from their website — excellent architectural detail on the major homes.",
                "💡 The Blue Star Arts Complex, just at the north edge of King William, has galleries, studios, and the Blue Star Brewing Company inside a converted historic warehouse."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "The Guenther House",
              description: "A San Antonio landmark since 1859 — the historic home of the Pioneer Flour Mills founder, now a restaurant serving brunch and lunch daily. Order the waffles, the migas, or the freshly baked biscuits with Pioneer flour gravy. The Victorian dining rooms and the sunny garden patio are beautiful. A genuine piece of San Antonio history you can eat inside.",
              meta: "$14-22pp · 205 E Guenther St, King William · No reservations"
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "The UNESCO Missions are severely underrated — most tourists see only the Alamo and miss the other four. Mission San José alone is one of the most beautiful buildings in Texas. The whole mission trail by bike along the river is a world-class experience. I'd argue it's more impressive than the Alamo itself. Tell no one.",
              cite: "r/sanantonio"
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Pearl District Exploration",
              description: "The Pearl District is San Antonio's most exciting neighborhood — the 22-acre site of the historic Pearl Brewery (1883-2001) transformed into a world-class food and culture campus. The old brewhouse is now Hotel Emma (one of America's best boutique hotels). The farmers market runs every Saturday and Sunday morning. The restaurant lineup includes some of SA's very best: Cured, Restaurant Claudine, Supper, and the excellent weekend market stalls. Walk the complex, have a drink at the outdoor bars, and take in the stunning industrial-heritage architecture.",
              details: [
                "📍 312 Pearl Pkwy · Free to explore",
                "💡 Hotel Emma's lobby bar (Sternewirth) is worth a drink even if you're not staying — inside the original brewhouse with vaulted brick ceilings, 30-foot windows, and a genuinely spectacular space.",
                "💡 The Saturday morning farmers market at Pearl is one of the best in Texas — produce, artisan foods, pastries, local vendors. If your timing aligns, it's a 9am-1pm must."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Cured at Pearl",
              description: "Chef Steve McHugh's award-winning restaurant in a restored 1894 brewhouse building — the best fine dining in San Antonio. The menu centers on charcuterie (McHugh cured meats are exceptional) and seasonal Texas ingredients: Gulf Coast seafood, Hill Country venison, locally grown vegetables. The wine list is excellent. Dinner here is a genuine splurge ($60-90pp) but this is where San Antonio's food scene earns national recognition.",
              meta: "$60-90pp · 306 Pearl Pkwy · Reservations essential (resy.com)"
            }
          ],
          tips: [
            {
              type: "tip",
              text: "For a more budget-friendly Pearl District dinner, try Carnitas Lonja (excellent casual Mexican) or NAO (Latin street food-inspired) — both in or near the Pearl complex and excellent quality at half the price of Cured."
            }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Natural Bridge Caverns, Southtown Arts & Farewell Tex-Mex",
      neighborhoods: "Natural Bridge Caverns · Southtown · Blue Star Arts · Downtown",
      date: "March 14",
      mapPins: [
        { lat: 29.6927, lng: -98.3430, label: "Natural Bridge Caverns", num: 1, cat: "activity", desc: "Largest caverns in Texas — 180-ft stalactite formations, 30 min north" },
        { lat: 29.4118, lng: -98.4882, label: "Blue Star Arts Complex", num: 2, cat: "activity", desc: "Converted warehouse with galleries, studios & Blue Star Brewing" },
        { lat: 29.4572, lng: -98.4628, label: "San Antonio Botanical Garden", num: 3, cat: "activity", desc: "38-acre garden with Hill Country landscapes & spring wildflowers" },
        { lat: 29.4138, lng: -98.4493, label: "2M Smokehouse BBQ", num: 4, cat: "food", desc: "Texas Monthly Top 50 BBQ — post oak smoked brisket, East Side SA" },
        { lat: 29.4252, lng: -98.4954, label: "Briscoe Western Art Museum", num: 5, cat: "activity", desc: "World-class collection of Western American art on the River Walk" },
        { lat: 29.4403, lng: -98.4796, label: "Southtown Arts District", num: 6, cat: "activity", desc: "South Alamo St galleries, bars & local restaurants" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Natural Bridge Caverns",
              description: "Drive 30 minutes north on I-35 to Natural Bridge Caverns — the largest natural caverns in Texas, named for the 60-foot limestone natural bridge above the entrance. The 'Hidden Wonders' tour descends 180 feet underground into a cathedral of stalactites and stalagmites, some over 100 million years old. The formations are extraordinary: massive columns, translucent 'soda straw' stalactites, flowstone curtains in orange and cream. The cave maintains a constant 70°F/21°C — bring a light layer. The Discovery Tour (75 minutes) is the main cave experience; the more adventurous Hidden Wonders tour is worth the upgrade.",
              details: [
                "📍 26495 Natural Bridge Caverns Rd · Adult tickets ~$27-35 (book at naturalbridgecaverns.com) · Open daily 9am",
                "🚗 30 min north on I-35 from downtown — Uber/Lyft ~$25-30 each way, or rent a car for the day",
                "💡 Book tickets in advance online — March spring break period can see heavy crowds. The first tours of the day (9-10am) are the least crowded.",
                "💡 The cave tour also passes through the famous 'Hall of Giants' — 40-foot stalactite/stalagmite columns that took hundreds of thousands of years to form. Genuinely awe-inspiring."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Grab food en route",
              description: "Pick up breakfast from your hotel or a drive-through before heading north. Natural Bridge Caverns has a decent café on-site for snacks, but save your appetite for the legendary BBQ lunch at 2M Smokehouse back in the city.",
              meta: "$6-12pp"
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "Natural Bridge Caverns is legitimately world-class. I've been to Carlsbad Caverns and Mammoth Cave — this holds its own. The formations are incredibly dense and well-lit. Go on the main Discovery Tour at minimum; if you're not claustrophobic the 'Wild Cave Tour' is extraordinary. Wear closed-toe shoes.",
              cite: "r/texas"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "2M Smokehouse BBQ",
              description: "This is the pilgrimage. 2M Smokehouse on the East Side of San Antonio was named to Texas Monthly's Top 50 BBQ list — a massive honor in a state that takes barbecue with religious seriousness. Owner Esaul Ramos (a US Army veteran) and his wife Sylvia smoke everything over post oak: brisket with a perfect bark, jalapeño-cheese sausage, pork spare ribs that fall from the bone, and cabrito (goat) on weekends. Get the two-meat plate with brisket and ribs, add the house-made potato salad, and plan to spend an hour in blissful silence.",
              details: [
                "📍 2731 S WW White Rd, San Antonio · Opens 11am until sold out (usually 3-4pm) · Cash preferred",
                "💡 Arrive by 11:30am — the brisket and ribs sell out early, especially on weekends. The line moves fast.",
                "💡 The brisket point (the fatty end) is the correct order. Don't let anyone tell you otherwise.",
                "⚠️ 2M is not on the River Walk and not fancy. It's a proper East Side pitmaster operation. Take an Uber/Lyft (~$12-15 from downtown). Worth every mile."
              ]
            },
            {
              title: "Blue Star Arts Complex & Southtown Gallery Walk",
              description: "Spend the afternoon in San Antonio's arts district. The Blue Star Arts Complex in King William is a 90,000-square-foot converted 1917 warehouse with studios, galleries, and the Blue Star Brewing Company taproom. First Friday art walks happen the first Friday of each month (March 6 was the last one, but galleries are open regardless). Walk north on South Alamo Street through Southtown — the stretch from Blue Star to Hemisfair Park has independent galleries, vintage shops, and the kind of neighborhood life that doesn't show up in tourist guides.",
              details: [
                "📍 Blue Star Arts: 1400 S Alamo St · Galleries open Tue-Sat noon-6pm · Free",
                "💡 Blue Star Brewing Company is one of San Antonio's oldest craft breweries — grab a pint of their Texican Lager or a seasonal beer in the taproom after gallery-browsing.",
                "💡 The Southtown stretch of South Alamo Street has the best independent shops in San Antonio — Folklore Vintage, friendly local bookstores, and art studios you can walk into and talk to the artists."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "2M Smokehouse BBQ",
              description: "Post oak-smoked brisket with jalapeño-cheese sausage and house-made sides — the best BBQ in San Antonio and one of the best in Texas. Get the two-meat plate, add the potato salad and a jalapeño for completeness. This is a legendary Texas BBQ experience at a local East Side institution with zero pretension.",
              meta: "$20-32pp · 2731 S WW White Rd · Cash preferred · Opens 11am"
            }
          ],
          tips: [
            {
              type: "tip",
              text: "San Antonio's barbecue scene is less famous than Austin's but catching up fast. 2M is the flagship, but also check out Reese Bros BBQ (excellent ribs, near the Alamodome) if you want a second opinion. San Antonio BBQ has more Mexican-American influence — look for barbacoa alongside brisket."
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "San Antonio Botanical Garden (Optional Sunset Visit)",
              description: "If you have energy before dinner, the 38-acre San Antonio Botanical Garden in the Mahncke Park neighborhood is stunning in mid-March — Texas Hill Country wildflowers are at their peak, the succulent and cactus gardens are in bloom, and the evening light through the glass conservatory is beautiful. The Kumamoto En Japanese garden is a hidden gem.",
              details: [
                "📍 555 Funston Pl · $15 adult · Open daily 9am-5pm (last entry 4pm)",
                "💡 Check if they have their spring 'Garden After Dark' evening events — sometimes run on weekends in March."
              ]
            },
            {
              title: "Final River Walk Evening",
              description: "For your last evening, walk the River Walk south from downtown toward the Museum Reach at twilight. The limestone canyon, the ancient cypress trees reflected in the water, the arched bridges lit from below, and the distant sound of live music drifting from the restaurants — this is San Antonio at its most atmospheric. Cross every bridge. Take the slow route.",
              details: [
                "💡 The Museum Reach north of downtown is quieter and more scenic than the commercial strip — it passes under historic bridges and through a serene canyon.",
                "💡 Riverboat tours run until 9pm and cost $15 — an easy, relaxed way to see the River Walk from water level with good narration."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Farewell Dinner",
              name: "La Fonda on Main",
              description: "For your final San Antonio dinner, go to La Fonda on Main — a beloved San Antonio institution since 1932, serving slightly elevated Tex-Mex in a beautiful hacienda-style building. The oak-grilled fajitas sizzle tableside, the queso flameado (flaming queso with chorizo) is theatrical and delicious, and the margaritas with fresh-squeezed lime are the ideal farewell toast. This is the San Antonio experience that locals actually send visitors to.",
              meta: "$28-45pp · 2415 N Main Ave · Reservations recommended (opentable.com)"
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "San Antonio is one of those cities that surprises people. Most expect theme parks and tourist traps. They get a legitimately beautiful River Walk, the most underrated UNESCO site in North America, genuine world-class Tex-Mex, and a neighborhood scene that's still affordable. Come for 3 days; plan your return trip by day 2.",
              cite: "r/solotravel"
            }
          ]
        }
      ]
    }
  ]
};

// Run fulfillment
(async () => {
  try {
    const result = await fulfillOrder(order, itineraryData);
    console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('❌ Fulfillment failed:', err.message);
    process.exit(1);
  }
})();
