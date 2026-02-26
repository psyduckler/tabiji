const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772045774521_lnbojz',
  email: 'psyduckler@gmail.com',
  destination: 'Loch Ness, Scotland',
};

const itineraryData = {
  destination: 'Loch Ness, Scotland',
  countryEmoji: '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
  title: 'Loch Ness: Into the Highland Mist',
  subtitle: 'Five days of ancient castles, whisky distilleries, wild hikes, and Nessie-hunting in the heart of the Scottish Highlands',
  description: 'Loch Ness is more than its famous monster — it\'s the gateway to Scotland\'s wildest, most atmospheric landscape. This solo itinerary takes you from the charming capital of the Highlands, Inverness, deep into the Great Glen. Explore ruined castles perched above dark waters, hike through ancient Caledonian pine forests, taste single malt whisky at family-run distilleries, and wander villages where time moves at the pace of the river. By day five, you\'ll understand why people come here looking for a monster and leave enchanted by everything else.',
  duration: '5 nights',
  dates: 'Apr 21 – Apr 26, 2026',
  budget: 'Moderate',
  pace: 'Relaxed',
  bestFor: 'Solo travelers, Nature lovers, History & whisky enthusiasts',
  highlights: ['Urquhart Castle ruins overlooking Loch Ness', 'Whisky tasting at Highland distilleries', 'The Loch Ness Centre & monster-hunting boat cruise', 'Hiking in Cairngorms National Park', 'Culloden Battlefield & Clava Cairns', 'Fort Augustus & the Caledonian Canal locks'],

  essentials: [
    { title: '🛬 Getting There', text: 'Fly into Inverness Airport (INV) — direct flights from London, Edinburgh, Dublin, and Amsterdam. Alternatively, take the scenic train from Edinburgh (~3.5 hours) or Glasgow (~3 hours). A rental car is highly recommended for exploring the loch and Highlands.' },
    { title: '💵 Money', text: 'British Pound Sterling (£). Cards accepted almost everywhere, even remote pubs. Budget £80-150/day for a comfortable solo trip with casual dining. ATMs available in Inverness and larger villages.' },
    { title: '🗣️ Language', text: 'English with a wonderful Highland accent. You\'ll hear some Scots Gaelic on signs (Loch Nis = Loch Ness). Locals are famously friendly and love to chat — don\'t be surprised if a pub conversation turns into a history lesson.' },
    { title: '🌦️ Weather in April', text: 'Spring in the Highlands — expect everything. Temperatures 5-13°C (41-55°F), mix of sunshine, rain, and wind, sometimes all in one hour. Layer up: waterproof jacket is non-negotiable. Days are long — sunrise around 6am, sunset after 8:30pm.' },
    { title: '🚗 Getting Around', text: 'Rent a car — essential for the loch\'s south shore and Glen Affric. Roads are single-track with passing places outside Inverness. Drive on the LEFT. Stagecoach buses run Inverness to Fort Augustus but are infrequent. Loch Ness boat cruises depart from multiple points.' },
    { title: '🔒 Safety', text: 'Extremely safe area. Main hazards are weather exposure on hikes and single-track road driving. Midges aren\'t usually bad in April (they peak June-August). Mobile signal is patchy in remote glens — download offline maps.' },
  ],

  days: [
    // DAY 1 — Arrival in Inverness & Loch Ness Introduction
    {
      num: 1,
      title: 'Arrival & First Glimpse of the Loch',
      description: 'Arrive in the Highland capital, explore Inverness, then drive south for your first magical encounter with Loch Ness at Urquhart Castle.',
      neighborhoods: 'Inverness · Drumnadrochit · Urquhart Castle',
      timeBlocks: [
        {
          label: 'Morning / Early Afternoon',
          activities: [
            {
              title: 'Arrive in Inverness',
              description: 'Fly into Inverness Airport or arrive by train. Pick up your rental car and drive into the city centre (15 minutes from airport). Drop bags at your accommodation and take a short stroll along the River Ness — the pink-sandstone Inverness Castle overlooks the water.',
              details: ['Recommended stays: Rocpool Reserve (boutique), Ness Walk (luxury), or a cozy B&B in the Crown area', '💡 If arriving by train, the station is right in the city centre — car hire desks nearby']
            },
            {
              title: 'Inverness City Walk',
              description: 'Wander the compact Highland capital. Cross the Ness Islands — a series of wooded islands connected by Victorian footbridges in the middle of the river. Pop into Leakey\'s Bookshop, Scotland\'s largest secondhand bookshop housed in a converted church.',
              details: ['📍 Leakey\'s: Church St, Inverness IV1 1EY', '💡 The Victorian Market on Academy Street has local crafts and a good café']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Mustard Seed',
              description: 'A beloved Inverness restaurant in a converted church overlooking the River Ness. Scottish comfort food — think cullen skink (smoked haddock soup), Highland venison, and locally sourced seafood. Excellent value lunch menu.',
              meta: '📍 16 Fraser St, Inverness IV1 1DW · 💰 £12-20/main · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pick up supplies at Inverness before heading to the loch — shops are sparse once you leave the city.' }
          ]
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Drive to Urquhart Castle',
              description: 'Head southwest on the A82 along the north shore of Loch Ness. The drive itself is stunning — dark water stretching endlessly to the south, ancient woodland on both sides. After 25 minutes, you\'ll reach the iconic ruins of Urquhart Castle.',
              details: ['📍 A82, Drumnadrochit IV63 6XJ', '💰 £14 adult admission (Historic Scotland)', '🕐 Open 9:30am-6pm in April', '💡 The castle\'s Grant Tower has the best viewpoint — look out over the loch and imagine the centuries of clan warfare']
            },
            {
              title: 'Urquhart Castle',
              description: 'One of Scotland\'s most iconic ruins, dramatically perched on a headland jutting into Loch Ness. The castle dates to the 13th century and was fought over by Scots and English for centuries before being blown up in 1692 to prevent Jacobite use. The visitor centre film is surprisingly good.',
              details: ['💡 This is the #1 spot for Nessie sightings — keep your camera ready', '💡 Late afternoon light is magical on the ruins']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Dores Inn',
              description: 'A cozy lochside pub in the tiny village of Dores, at the northeastern tip of Loch Ness. Famous for its beer garden right on the pebbly beach — watch the sunset over the loch with a pint of local ale and hearty pub food (fish & chips, venison burger, sticky toffee pudding).',
              meta: '📍 Dores, Inverness IV2 6TR · 💰 £12-18/main · 🍺 Great local ale selection'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The sunset from Dores Beach is legendary — arrive by 7:30pm for the best light over the loch.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.4778, lng: -4.2247, label: 'Inverness', num: 1, cat: 'transport', desc: 'Arrive in the Highland capital' },
        { lat: 57.4617, lng: -4.2400, label: 'Ness Islands', num: 2, cat: 'attraction', desc: 'Wooded islands with Victorian footbridges' },
        { lat: 57.4650, lng: -4.2290, label: 'The Mustard Seed', num: 3, cat: 'restaurant', desc: 'Riverside Scottish lunch' },
        { lat: 57.3242, lng: -4.4428, label: 'Urquhart Castle', num: 4, cat: 'attraction', desc: 'Iconic 13th-century ruins on Loch Ness' },
        { lat: 57.3858, lng: -4.3308, label: 'The Dores Inn', num: 5, cat: 'restaurant', desc: 'Lochside pub with sunset views' }
      ]
    },

    // DAY 2 — South Loch Ness & Fort Augustus
    {
      num: 2,
      title: 'The Deep Loch & Fort Augustus',
      description: 'Explore the quieter south shore of Loch Ness, visit the Loch Ness Centre, cruise the dark waters, and end in the charming canal village of Fort Augustus.',
      neighborhoods: 'Drumnadrochit · South Loch Ness · Fort Augustus',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Loch Ness Centre',
              description: 'Recently renovated and genuinely fascinating — not a cheesy tourist trap. The exhibition traces the geological history of the loch, the science of sonar surveys, and the cultural phenomenon of the monster. Interactive displays and original research equipment from decades of expeditions.',
              details: ['📍 Drumnadrochit IV63 6TU', '💰 £10.95 adult', '🕐 Open 10am-5pm', '💡 The 1987 Operation Deepscan sonar sweep section is riveting']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Fiddler\'s Coffee House',
              description: 'A cheerful wee café in Drumnadrochit. Strong coffee, fresh-baked scones with clotted cream and jam, and full Scottish breakfasts (square sausage, tattie scone, black pudding).',
              meta: '📍 Drumnadrochit · 💰 £8-12'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Loch Ness Centre is far better than the old "exhibition" — they did a complete redesign in 2023.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Loch Ness Boat Cruise',
              description: 'Take a cruise from Drumnadrochit or Fort Augustus out onto the loch. The water is over 230 meters deep — deeper than the North Sea — and holds more fresh water than all the lakes of England and Wales combined. Onboard sonar lets you watch the loch bed in real time.',
              details: ['Cruise Loch Ness or Jacobite Cruises both run from multiple departure points', '💰 £15-25 for a 1-hour cruise', '💡 The loch never freezes — the peat-stained water absorbs heat. It\'s eerily dark below the surface.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Lock Inn',
              description: 'Friendly canal-side pub in Fort Augustus with outdoor seating overlooking the Caledonian Canal locks. Watch boats navigate the lock staircase while enjoying a venison pie or fish & chips with a local craft beer.',
              meta: '📍 Fort Augustus PH32 4AU · 💰 £10-16/main'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Fort Augustus & the Caledonian Canal',
              description: 'This picturesque village sits at the southwestern tip of Loch Ness where the Caledonian Canal enters through a dramatic flight of five locks. Watch boats being raised and lowered through the lock staircase — pure engineering theatre. Walk along the canal towpath for gorgeous views.',
              details: ['💡 The canal was built by Thomas Telford (1803-1822) to connect the east and west coasts of Scotland', '💡 Fort Augustus Abbey ruins (now flats) are worth a look from outside']
            },
            {
              title: 'South Loch Ness Drive',
              description: 'Take the B862 along the quieter south shore back toward Inverness. This single-track road through Foyers and Whitebridge offers the most atmospheric views of the loch — fewer tourists, wilder scenery, and the stunning Falls of Foyers waterfall.',
              details: ['📍 Falls of Foyers — short walk from the road, dramatic 140ft drop', '💡 This road is narrow and winding — take your time and enjoy the remoteness']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Whitebridge Hotel',
              description: 'A proper Highland inn on the quiet south shore road. Home-cooked food with local ingredients — haggis, neeps & tatties, Highland beef, and a good selection of single malts at the bar. The kind of place where locals and travelers mix.',
              meta: '📍 Whitebridge, Inverness-shire IV2 6UN · 💰 £12-20/main'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Stop at the Falls of Foyers viewpoint — Robert Burns visited in 1787 and was so moved he wrote a poem about them.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.3340, lng: -4.4790, label: 'Loch Ness Centre', num: 1, cat: 'attraction', desc: 'Renovated monster & loch science exhibition' },
        { lat: 57.3340, lng: -4.4790, label: 'Drumnadrochit', num: 2, cat: 'restaurant', desc: 'Breakfast at Fiddler\'s Coffee House' },
        { lat: 57.3300, lng: -4.4500, label: 'Loch Ness Cruise', num: 3, cat: 'attraction', desc: 'Boat cruise on the deep dark loch' },
        { lat: 57.1448, lng: -4.6800, label: 'Fort Augustus', num: 4, cat: 'attraction', desc: 'Canal locks & charming Highland village' },
        { lat: 57.1448, lng: -4.6800, label: 'The Lock Inn', num: 5, cat: 'restaurant', desc: 'Canal-side pub lunch' },
        { lat: 57.2520, lng: -4.4880, label: 'Falls of Foyers', num: 6, cat: 'attraction', desc: '140ft waterfall on the south shore' },
        { lat: 57.2450, lng: -4.5200, label: 'The Whitebridge Hotel', num: 7, cat: 'restaurant', desc: 'Highland inn dinner on the south shore' }
      ]
    },

    // DAY 3 — Culloden, Clava Cairns & Whisky
    {
      num: 3,
      title: 'Battlefields, Standing Stones & Whisky',
      description: 'A day of Highland history and whisky. Walk the haunting Culloden Battlefield, explore 4,000-year-old burial cairns, and taste single malt at a classic Speyside-edge distillery.',
      neighborhoods: 'Culloden · Clava · Tomatin · Inverness',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Culloden Battlefield',
              description: 'The site of the last pitched battle on British soil (1746), where Bonnie Prince Charlie\'s Jacobite army was destroyed in under an hour by government forces. The visitor centre is outstanding — immersive film, battlefield artefacts, and audio guides for the outdoor walk among the clan grave markers. Deeply moving even on a drizzly day.',
              details: ['📍 Culloden Moor, Inverness IV2 5EU', '💰 £15 adult (NTS)', '🕐 Open 10am-5pm', '💡 The roof-top viewpoint shows the whole battlefield — you\'ll understand the terrain advantage the government had']
            },
            {
              title: 'Clava Cairns',
              description: 'Just a mile from Culloden — a prehistoric cemetery of passage graves and ring cairns dating to around 2000 BC. Stone circles surround the cairns, and the alignment captures midwinter sunset through the passage. Atmospheric, free, and usually deserted. This site inspired the standing stones in Outlander.',
              details: ['📍 Near Culloden, off B9006', '💰 Free · Open all hours', '💡 The Bronze Age cup marks on some stones are still visible after 4,000 years']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Velocity Café',
              description: 'A cyclist-friendly café in Inverness with excellent coffee, thick-cut toast with local honey, porridge with cream, and freshly baked pastries. Relaxed vibe, good people-watching.',
              meta: '📍 1 Crown Ave, Inverness IV2 3NF · 💰 £6-10'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Visit Culloden first thing — it\'s most powerful when quiet. The audio guide for the battlefield walk is essential.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tomatin Distillery',
              description: 'A friendly, unpretentious distillery 25 minutes south of Inverness in the Monadhliath Mountains. The standard tour covers the full whisky-making process with tastings of their 12-year and 14-year-old single malts. The setting in a Highland village at the edge of the Cairngorms is gorgeous.',
              details: ['📍 Tomatin, Inverness-shire IV13 7YT', '💰 £10-25 depending on tour level', '🕐 Tours at 10am, 12pm, 2pm — book ahead', '💡 The Cù Bòcan peated expression is excellent if you like smoky whisky']
            },
            {
              title: 'Glen Ord Distillery (optional alternative)',
              description: 'If you prefer a west-side drive, Glen Ord near Muir of Ord is the only remaining single malt distillery in the Black Isle. Known as "The Singleton" — rich, fruity Highland style. More intimate experience than bigger Speyside distilleries.',
              details: ['📍 Muir of Ord, Ross-shire IV6 7UJ', '💰 £10-20 per tour', '💡 The Black Isle itself is beautiful — rolling farmland, dolphins in the Moray Firth']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Café 1',
              description: 'One of Inverness\'s best restaurants — modern Scottish bistro using Highland ingredients. Excellent seafood (Loch Duart salmon, west coast mussels), local steaks, and a well-curated wine list. Relaxed but polished.',
              meta: '📍 75 Castle St, Inverness IV2 3EA · 💰 £14-22/main'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Whisky Tasting at The Malt Room',
              description: 'End the day with a guided whisky flight at Inverness\'s finest whisky bar. Over 300 single malts behind the bar, knowledgeable staff, and a cozy atmosphere. Try a flight of Highland malts to compare what you tasted at the distillery.',
              details: ['📍 34 Church St, Inverness IV1 1EH', '💰 £15-40 for a flight of 3-5 drams', '💡 Ask for their recommendation based on what you tasted at the distillery — they love helping people explore']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Kitchen Brasserie',
              description: 'River Ness-side restaurant by acclaimed chef, focusing on seasonal Highland produce. Think pan-seared sea bass, Highland lamb, and Scottish cheese boards. Beautiful riverside terrace if the evening is mild.',
              meta: '📍 15 Huntly St, Inverness IV3 5PR · 💰 £16-25/main'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, walk along the River Ness at dusk — the castle and church spires are beautifully lit.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.4773, lng: -4.0943, label: 'Culloden Battlefield', num: 1, cat: 'attraction', desc: 'Site of the 1746 Jacobite defeat' },
        { lat: 57.4730, lng: -4.0740, label: 'Clava Cairns', num: 2, cat: 'attraction', desc: '4,000-year-old prehistoric burial cairns' },
        { lat: 57.4650, lng: -4.2290, label: 'Velocity Café', num: 3, cat: 'restaurant', desc: 'Great coffee & breakfast in Inverness' },
        { lat: 57.3400, lng: -4.0200, label: 'Tomatin Distillery', num: 4, cat: 'attraction', desc: 'Highland single malt whisky tour & tasting' },
        { lat: 57.4660, lng: -4.2260, label: 'Café 1', num: 5, cat: 'restaurant', desc: 'Modern Scottish bistro lunch' },
        { lat: 57.4660, lng: -4.2280, label: 'The Malt Room', num: 6, cat: 'attraction', desc: '300+ single malts — whisky tasting' },
        { lat: 57.4640, lng: -4.2340, label: 'The Kitchen Brasserie', num: 7, cat: 'restaurant', desc: 'Riverside Highland dinner' }
      ]
    },

    // DAY 4 — Glen Affric & Highland Wilderness
    {
      num: 4,
      title: 'Glen Affric — Scotland\'s Most Beautiful Glen',
      description: 'A day in the wilderness. Hike through ancient Caledonian pine forest in Glen Affric, one of Scotland\'s most stunning and remote valleys. Waterfalls, lochs, and red deer.',
      neighborhoods: 'Cannich · Glen Affric · Beauly',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Glen Affric',
              description: 'Head west from Inverness through Beauly and Struy to the village of Cannich — gateway to Glen Affric. The drive takes about 45 minutes and the scenery builds dramatically as you enter the glen. This is Scotland\'s most beautiful valley — remnant Caledonian pine forest, pristine lochs, and mountains on all sides.',
              details: ['📍 Glen Affric, near Cannich, Inverness-shire', '💡 Fill up petrol in Inverness — no stations in the glen', '💡 Pack a picnic lunch, water, and layers — weather changes fast']
            },
            {
              title: 'Dog Falls Walk',
              description: 'An easy 1.5-mile circular walk through ancient Scots pine and birch woodland to a series of beautiful waterfalls on the River Affric. The trees here are 300+ years old — gnarled, windswept survivors of the original Caledonian Forest that once covered all of Scotland.',
              details: ['📍 Dog Falls car park, Glen Affric', '🕐 45 min – 1 hour loop', '💰 Free (parking £3)', '💡 Look for red squirrels in the pines and dippers bobbing in the river']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Hotel breakfast or packed provisions',
              description: 'Have a hearty breakfast at your accommodation before the drive. Pack trail snacks — there are no cafés in Glen Affric.',
              meta: '💡 Pick up sandwiches from a deli in Inverness the night before'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Glen Affric is a nature reserve — you might see red deer, golden eagles, pine martens, and red squirrels. Binoculars recommended.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Loch Affric Circuit',
              description: 'The signature Glen Affric hike — a 9-mile circular walk around Loch Affric through some of the finest scenery in Scotland. Ancient pines reflected in mirror-still water, mountain ridges on the horizon, and a profound sense of wilderness. This is the Scotland of the imagination.',
              details: ['📍 Start from the River Affric car park at the end of the road', '🕐 4-5 hours at a relaxed pace', '💡 The north shore trail is slightly higher and offers better views', '⚠️ Sturdy waterproof boots essential — boggy sections even in dry weather']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Picnic at Loch Affric',
              description: 'Find a flat rock by the loch shore and enjoy your packed lunch with one of the greatest views in Scotland. Just you, the ancient pines, and the water.',
              meta: '📍 Anywhere along the loch shore · 💰 Free (the best things are)'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If 9 miles feels too much, the shorter 3-mile loch viewpoint trail from the same car park is equally beautiful.' }
          ]
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Beauly Priory',
              description: 'On the drive back, stop at the ruins of Beauly Priory (1230) in the pretty town of Beauly. Mary Queen of Scots visited in 1564 and reportedly said "Ah, qu\'el beau lieu!" (what a beautiful place) — giving the town its name.',
              details: ['📍 Beauly, Inverness-shire IV4 7DX', '💰 Free · Open daylight hours', '💡 The town square has a nice butcher and deli for provisions']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Riva Italian Restaurant',
              description: 'After a big hiking day, casual Italian comfort food in Inverness hits the spot. Wood-fired pizzas, fresh pasta, and Scottish seafood with an Italian twist. Unpretentious and satisfying.',
              meta: '📍 4-6 Ness Walk, Inverness IV3 5NE · 💰 £12-18/main'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 You\'ll be pleasantly tired after Glen Affric — it\'s a proper day in the hills. Treat yourself to a hot bath and an early night.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.2800, lng: -4.9600, label: 'Glen Affric', num: 1, cat: 'attraction', desc: 'Scotland\'s most beautiful glen' },
        { lat: 57.2900, lng: -4.9400, label: 'Dog Falls', num: 2, cat: 'attraction', desc: 'Waterfalls in ancient Caledonian forest' },
        { lat: 57.2650, lng: -5.0500, label: 'Loch Affric', num: 3, cat: 'attraction', desc: '9-mile circuit through pristine Highlands' },
        { lat: 57.4750, lng: -4.4700, label: 'Beauly Priory', num: 4, cat: 'attraction', desc: '13th-century priory ruins' },
        { lat: 57.4650, lng: -4.2310, label: 'Riva', num: 5, cat: 'restaurant', desc: 'Casual Italian dinner in Inverness' }
      ]
    },

    // DAY 5 — Black Isle, Dolphins & Departure
    {
      num: 5,
      title: 'Black Isle, Dolphins & Farewell',
      description: 'Your final Highland morning. Cross to the Black Isle for bottlenose dolphins, a medieval cathedral, and a farewell dram before departing.',
      neighborhoods: 'Black Isle · Chanonry Point · Fortrose · Inverness',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Chanonry Point — Dolphin Watching',
              description: 'Drive 30 minutes northeast to Chanonry Point on the Black Isle — the best place in Europe to see bottlenose dolphins from shore. The Moray Firth pod (about 200 dolphins) regularly feeds close to the point, especially around the incoming tide. Stand on the shingle beach and watch them leap and roll just meters away.',
              details: ['📍 Chanonry Point, Fortrose IV10 8SD', '💰 Free', '💡 Check tide times — dolphins feed on the incoming tide. Arrive 1-2 hours before high tide', '💡 April is great for sightings — calves born in summer are still young and playful']
            },
            {
              title: 'Fortrose Cathedral',
              description: 'The beautiful red sandstone ruins of a 13th-century cathedral in the quiet town of Fortrose. Peaceful grounds with views across the Moray Firth. A hidden gem most tourists miss.',
              details: ['📍 Fortrose, Black Isle IV10 8TD', '💰 Free', '💡 The chapter house and south aisle are remarkably well preserved']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'The Anderson',
              description: 'Boutique restaurant and bar in Fortrose with an excellent breakfast — locally smoked salmon and scrambled eggs, proper porridge with Highland honey, and strong coffee. A lovely start to the last day.',
              meta: '📍 Union St, Fortrose IV10 8TD · 💰 £8-14'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Even if you don\'t see dolphins (unusual but possible), Chanonry Point is beautiful — the views across to Fort George and the mountains are stunning.' }
          ]
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Farewell Walk — Ness Islands & River',
              description: 'Back in Inverness for a final stroll. Walk the Ness Islands loop one more time, or wander along the river to the cathedral and Eden Court Theatre gardens. Soak in the Highland capital one last time.',
              details: ['💡 If you have time, the Inverness Museum & Art Gallery (free) has excellent Highland history displays']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Black Isle Bar & Rooms',
              description: 'Organic craft beer brewery taproom right in Inverness city centre. Excellent burgers, fish tacos, and sharing plates paired with their own award-winning organic ales. A fitting farewell meal.',
              meta: '📍 68 Church St, Inverness IV1 1EN · 💰 £10-16/main · 🍺 Try the Hibernator Oatmeal Stout'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pick up a bottle of single malt at The Whisky Shop on Bridge Street as a souvenir — they\'ll help you choose based on what you liked at the distillery.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Depart Inverness',
              description: 'Head to Inverness Airport (15 min drive) or the train station for your onward journey. If flying, the airport is small and efficient — arrive 90 minutes before your flight. If taking the evening train to Edinburgh, enjoy 3.5 hours of stunning Highland scenery through the Cairngorms.',
              details: ['💡 Return your rental car at the airport or in-town drop-off', '💡 The Inverness-Edinburgh train via Aviemore and Pitlochry is one of Britain\'s great rail journeys']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 Slàinte mhath! (Gaelic for "good health") — you\'ve earned it. The Highlands have a way of staying with you long after you leave.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.5745, lng: -4.0945, label: 'Chanonry Point', num: 1, cat: 'attraction', desc: 'Best shore-based dolphin watching in Europe' },
        { lat: 57.5810, lng: -4.1300, label: 'Fortrose Cathedral', num: 2, cat: 'attraction', desc: 'Red sandstone 13th-century ruins' },
        { lat: 57.5810, lng: -4.1300, label: 'The Anderson', num: 3, cat: 'restaurant', desc: 'Boutique breakfast in Fortrose' },
        { lat: 57.4660, lng: -4.2280, label: 'Black Isle Bar', num: 4, cat: 'restaurant', desc: 'Organic craft beer & farewell lunch' },
        { lat: 57.4778, lng: -4.2247, label: 'Inverness Departure', num: 5, cat: 'transport', desc: 'Airport or train station' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (5 nights, mid-range B&B/hotel)', cost: '£400 – £750' },
    { category: 'Car Rental (5 days + fuel)', cost: '£200 – £350' },
    { category: 'Dining (casual, 5 days)', cost: '£200 – £350' },
    { category: 'Attractions & Admission Fees', cost: '£50 – £80' },
    { category: 'Whisky Distillery Tours & Tastings', cost: '£30 – £60' },
    { category: 'Loch Ness Boat Cruise', cost: '£15 – £25' },
    { category: 'Drinks & Pubs', cost: '£60 – £100' },
    { category: 'Souvenirs & Misc', cost: '£50 – £100' },
    { category: 'Total Estimated', cost: '£1,005 – £1,815' },
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: [
      'Inverness Airport (INV): Direct flights from London (Heathrow, Gatwick, Luton), Edinburgh, Dublin, Amsterdam',
      'Train from Edinburgh: ~3.5 hours via ScotRail (book at scotrail.co.uk for best fares)',
      'Train from London: ~8 hours via LNER Caledonian Sleeper (overnight — wake up in the Highlands)',
      'Car rental at Inverness Airport or city centre — essential for exploring the loch and glens'
    ]},
    { title: '📱 Connectivity', items: [
      'Mobile signal good in Inverness and main A-roads, patchy to nonexistent in glens (Glen Affric, south shore)',
      'Download Google Maps offline for the Highlands region before you go',
      'Most hotels and B&Bs have Wi-Fi — connection quality varies',
      'Essential apps: Google Maps (offline), Met Office Weather (accurate Highland forecasts), WalkHighlands.co.uk (route guides)'
    ]},
    { title: '🥾 Hiking Preparation', items: [
      'Waterproof hiking boots essential — even "dry" trails have boggy sections',
      'Waterproof jacket and layers — Highland weather changes rapidly',
      'Pack snacks and water for Glen Affric — no facilities in the glen',
      'Walking poles useful for Loch Affric circuit (undulating terrain)',
      'Midges not usually a problem in April (peak season is June-August)'
    ]},
    { title: '🚗 Driving Tips', items: [
      'Drive on the LEFT — take extra care at roundabouts and after stopping',
      'Many roads are single-track with passing places — pull into them to let oncoming traffic pass',
      'Watch for sheep, deer, and Highland cows on rural roads',
      'Fuel up in Inverness — petrol stations rare in remote areas',
      'Speed limit: 60mph on single carriageways, 30mph in villages'
    ]},
    { title: '🧳 Departure', items: [
      'Apr 26 checkout — Inverness Airport is 15 minutes east of city centre',
      'Drop rental car at airport or in-town',
      'For train journeys, Inverness station is central — easy walk from most accommodation',
      'Inverness Airport is small — 90 minutes before flight is plenty',
      'Pick up whisky and Scottish shortbread at the airport shop for souvenirs'
    ]},
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled!', result);
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
