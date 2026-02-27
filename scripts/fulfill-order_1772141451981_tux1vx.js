const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772141451981_tux1vx',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Lake Winnibigoshish, Minnesota',
  startDate: '2026-06-23',
  endDate: '2026-06-28',
  groupSize: 2,
  requests: ''
};

const itineraryData = {
  destination: 'Lake Winnibigoshish, Minnesota',
  countryEmoji: '🇺🇸',
  title: 'A Northwoods Escape on Big Winnie',
  subtitle: '5 nights of walleye fishing, forest trails & lakeside sunsets for two',
  description: "Lake Winnibigoshish — 'Big Winnie' — is one of Minnesota's legendary walleye lakes, ringed by the vast Chippewa National Forest. This itinerary pairs world-class fishing with quiet northwoods adventures: paddle through hidden bays, hike towering red pines, walk across the headwaters of the Mississippi at Itasca State Park, and end every day watching the sun sink into 67,000 acres of pristine water. It's the kind of trip where your phone stays in the cabin and you remember what stillness sounds like.",
  duration: '5 nights',
  dates: 'Jun 23 – Jun 28, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Couples · Outdoor Enthusiasts',
  highlights: [
    'Walleye fishing on one of Minnesota\'s top lakes',
    'Walk across the Mississippi headwaters at Itasca State Park',
    'Hike the Lost Forty — ancient pines untouched for 300+ years',
    'Sunset kayaking through Chippewa National Forest bays',
    'Stargazing from the dock with zero light pollution'
  ],

  essentials: [
    { title: '🎣 Fishing', text: 'Late June is prime walleye season on Big Winnie. A Minnesota fishing license is required — buy one online at mndnr.gov before your trip. The lake is famous for walleye, northern pike, and perch. Local resorts can arrange guided trips.' },
    { title: '🦟 Bug Prep', text: 'June in northern Minnesota means mosquitoes and deer flies. Bring DEET-based repellent, long sleeves for dusk, and consider a Thermacell for the dock and boat. The tradeoff is absolutely worth it.' },
    { title: '🚗 Getting Around', text: 'You\'ll need a car — there\'s no public transit up here. The nearest airports are Bemidji (BJI, 50 min) and Grand Rapids (GPZ, 35 min). Most resorts have boat rentals and docks on-site.' },
    { title: '🌡️ Weather', text: 'Late June averages 75–85°F days and 55–60°F nights. Afternoon thunderstorms pop up fast — keep an eye on the sky when you\'re on the water. Pack layers for cool mornings on the boat.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-23',
      neighborhoods: 'Lake Winnibigoshish · Bena',
      title: 'Arrive & Settle Into the Northwoods',
      description: 'Drive up through pine forests and rolling farmland to reach Big Winnie. Check into your lakeside cabin, unpack the cooler, and spend your first evening on the dock watching the sun melt into the lake.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In at Your Resort',
              description: 'Arrive at your lakeside cabin and settle in. Most resorts on Winnie sit right on the water with private docks, fire pits, and boat slips. Take a walk around the grounds, grab your fishing license if you haven\'t already, and breathe in that pine air.',
              details: [
                '🏡 High Banks Resort or Bowen Lodge are top picks — full-service with restaurant, bar, and boat rentals',
                '🎣 Grab bait and tackle at the resort shop or stop in Bena on the way in',
                '🛶 Most resorts include a canoe or kayak with your cabin rental'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Stop at the Bena gas station/convenience store for snacks, firewood, and ice on your way in. Selection is limited up here — bring anything specific you want from Grand Rapids.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'First Sunset on the Dock',
              description: 'Big Winnie faces west, which means sunsets are extraordinary. Grab a couple of beers, sit on the dock, and watch the sky turn orange over miles of open water. You might spot a bald eagle making its last pass of the day.',
              details: [
                '🌅 Sunset is around 9:15pm in late June — long golden evenings',
                '🦅 Chippewa National Forest has the highest density of bald eagles in the lower 48'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'High Banks Lodge Restaurant',
              description: 'The lodge restaurant at High Banks serves hearty northwoods fare — walleye, burgers, steaks — with a full bar and a screened porch overlooking the forest.',
              meta: '💰 $$ · 📍 On-site at High Banks Resort'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.4336, lng: -94.0519, label: 'Lake Winnibigoshish', num: 1, cat: 'attraction', desc: 'Minnesota\'s 5th largest lake — 67,000 acres of walleye water' },
        { lat: 47.3505, lng: -94.2023, label: 'Bena', num: 2, cat: 'attraction', desc: 'Small town on the south shore — supplies and bait' },
        { lat: 47.4478, lng: -94.0100, label: 'High Banks Resort', num: 3, cat: 'food', desc: 'Full-service resort with lodge restaurant and bar' }
      ]
    },
    {
      num: 2,
      date: '2026-06-24',
      neighborhoods: 'Lake Winnibigoshish · Cut Foot Sioux Lake',
      title: 'Walleye Day — Fish Big Winnie',
      description: 'Today is all about fishing. Head out early when the walleye are biting, explore the legendary fishing grounds of Big Winnie and connected Cut Foot Sioux Lake, and cook your catch for a shore lunch you\'ll never forget.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Morning Walleye Run',
              description: 'Hit the water at dawn for prime walleye fishing. The south shore reefs and Tamarack Point are legendary spots. If you\'re new to Winnie, book a local guide — they know exactly where the fish are stacked in late June.',
              details: [
                '🎣 Northern Drift Outfitters offers half and full-day guided trips',
                '🐟 Jig and minnow or live bait rigs work best for June walleye',
                '📍 Tamarack Point, Sugar Point, and the dam area are hotspots',
                '⏰ Best bite is early morning (5–9am) and again at dusk'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Minnesota regulations: walleye slot limit on Winnie is typically 4 fish, with one over 20 inches allowed. Check current DNR regs before you go.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shore Lunch & Cut Foot Sioux',
              description: 'Clean your morning catch and have a classic shore lunch — battered walleye fried over an open fire on a rocky point. Then motor through the channel into Cut Foot Sioux Lake, a gorgeous connected lake with quieter water and excellent crappie fishing.',
              details: [
                '🍳 Many guides do shore lunch as part of the trip — fresh walleye, beans, and fried potatoes',
                '🛶 Cut Foot Sioux is shallower and more intimate — great for kayaking too',
                '🦅 Look for osprey and eagles along the channel between the lakes'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Campfire & Stargazing',
              description: 'Build a campfire at your cabin and watch the stars come out. With minimal light pollution this far north, the Milky Way is vivid. June nights are cool and perfect for sitting by the fire.',
              details: [
                '🔥 Most cabins have fire pits with wood provided or available for purchase',
                '⭐ The Big Dipper is practically overhead — bring a star chart or app',
                '🍺 Pick up some craft beer from a Grand Rapids brewery for the cooler'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cook Your Catch',
              description: 'Fry up the walleye you caught this morning — breaded and pan-fried with butter is the classic Minnesota preparation. Pair with corn on the cob and a cold beer on the cabin porch.',
              meta: '💰 $ · 📍 Your cabin kitchen'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.4550, lng: -94.0400, label: 'Tamarack Point', num: 1, cat: 'attraction', desc: 'Prime walleye fishing spot on Big Winnie\'s south shore' },
        { lat: 47.4900, lng: -94.1100, label: 'Sugar Point', num: 2, cat: 'attraction', desc: 'Historic point with excellent fishing and eagle nesting' },
        { lat: 47.4700, lng: -94.0700, label: 'Cut Foot Sioux Lake', num: 3, cat: 'attraction', desc: 'Connected lake — quieter water, great crappie and scenery' },
        { lat: 47.4336, lng: -94.0519, label: 'Winnibigoshish Dam', num: 4, cat: 'attraction', desc: 'Historic dam at the lake\'s northeast outlet' }
      ]
    },
    {
      num: 3,
      date: '2026-06-25',
      neighborhoods: 'Chippewa National Forest · Lost Forty',
      title: 'Ancient Pines & Forest Trails',
      description: 'Trade the boat for hiking boots. Explore the Chippewa National Forest\'s crown jewel — the Lost Forty, where 300-year-old red and white pines were spared from logging by a surveyor\'s mapping error. Then paddle the calm waters of a forest lake at golden hour.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Lost Forty Hike',
              description: 'Drive north to one of Minnesota\'s most awe-inspiring natural sites. The Lost Forty is a stand of virgin old-growth pine trees — some over 300 years old and 120 feet tall — that survived the logging era because a surveyor accidentally mapped the area as a lake. The 1-mile interpretive loop is flat, easy, and humbling.',
              details: [
                '🌲 Some pines are 4+ feet in diameter and 300+ years old',
                '📍 About 45 minutes north of the lake — take County Road 26',
                '🦌 Watch for deer, porcupines, and woodpeckers in the old growth',
                '📸 The morning light filtering through the canopy is stunning'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Chippewa National Forest Scenic Drive & Hike',
              description: 'Wind through the Chippewa National Forest on the Edge of the Wilderness Scenic Byway. Stop at overlooks, hike a section of the North Country Trail, and soak in the deep quiet of the boreal forest.',
              details: [
                '🛣️ The scenic byway runs along Highway 38 — gorgeous route',
                '🥾 North Country Trail has accessible sections near Marcell',
                '🐻 Black bears live here — make noise on the trail and store food properly'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Forest Lake Restaurant',
              description: 'A local favorite near the lake — casual dining with solid burgers, walleye sandwiches, and homemade pie.',
              meta: '💰 $ · 📍 Near Deer River'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Kayak Paddle',
              description: 'Launch kayaks from your resort dock and paddle along the shoreline as the sun drops. The water goes glass-calm in the evening, and loons start their haunting calls across the lake. This is peak northwoods magic.',
              details: [
                '🛶 Hug the shoreline for calmer water and wildlife sightings',
                '🦆 Loon calls at dusk are unforgettable — listen for the tremolo and yodel',
                '🌅 Paddle west toward the open lake for the full sunset show'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'The Gosh Dam Place',
              description: 'The best restaurant on Lake Winnie — a quirky, beloved spot near the Winnibigoshish Dam with excellent food, cold drinks, and a fun northwoods vibe. The name says it all.',
              meta: '💰 $$ · 📍 Highway 46, near Deer River · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.6700, lng: -93.9900, label: 'The Lost Forty', num: 1, cat: 'attraction', desc: '300-year-old virgin pine forest saved by a mapping error' },
        { lat: 47.5300, lng: -93.7700, label: 'Edge of the Wilderness Byway', num: 2, cat: 'attraction', desc: 'Scenic drive through the Chippewa National Forest' },
        { lat: 47.4400, lng: -94.0300, label: 'Sunset Kayak Launch', num: 3, cat: 'attraction', desc: 'Evening paddle along the lakeshore' },
        { lat: 47.4389, lng: -94.0147, label: 'The Gosh Dam Place', num: 4, cat: 'food', desc: 'Best restaurant on the lake — near the dam' }
      ]
    },
    {
      num: 4,
      date: '2026-06-26',
      neighborhoods: 'Itasca State Park · Lake Itasca',
      title: 'Mississippi Headwaters & Itasca State Park',
      description: 'Take a day trip to Itasca State Park and stand at the very spot where the Mississippi River begins — a tiny stream you can wade across. Hike through old-growth forest, cruise on Lake Itasca, and explore one of Minnesota\'s most iconic parks.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Itasca State Park',
              description: 'Head west to Itasca State Park — about 75 minutes from Lake Winnie. This is where the mighty Mississippi begins its 2,340-mile journey to the Gulf of Mexico, trickling out of Lake Itasca as a stream you can walk across on stepping stones.',
              details: [
                '📍 About 75 minutes west via Highway 2 and 71',
                '🚗 Minnesota State Park vehicle permit required ($7/day or $35/year)',
                '⏰ Arrive by 9am to beat the summer crowds at the headwaters'
              ]
            },
            {
              title: 'Walk Across the Mississippi Headwaters',
              description: 'The most iconic moment of the trip — wade across the infant Mississippi River where it flows out of Lake Itasca. The water is ankle-deep and crystal clear. It\'s hard to believe this tiny stream becomes one of the world\'s greatest rivers.',
              details: [
                '👣 The stepping stones are right at the headwaters — wear sandals you can get wet',
                '📸 Everyone takes the classic photo straddling the baby Mississippi',
                '🏛️ The Mary Gibbs Mississippi Headwaters Center has exhibits on the river\'s history'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wilderness Drive & Old-Growth Pines',
              description: 'Take the one-way Wilderness Drive through Itasca\'s Preacher\'s Grove — a stand of towering red pines over 250 years old. The 11-mile drive winds through pristine forest with pull-offs for short hikes and wildlife viewing.',
              details: [
                '🌲 Preacher\'s Grove pines are 250+ years old',
                '🚴 The drive is also popular for biking — consider renting bikes at the park',
                '🦌 Moose sightings are rare but possible in the boggy areas'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Douglas Lodge',
              description: 'Historic 1905 lodge inside Itasca State Park with a dining room overlooking Lake Itasca. Classic Minnesota fare — wild rice soup, walleye, and blueberry pie.',
              meta: '💰 $$ · 📍 Inside Itasca State Park'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return & Evening Fishing',
              description: 'Head back to Lake Winnie in time for the evening walleye bite. The golden hour fishing on Big Winnie in late June is magic — calm water, warm air, and active fish.',
              details: [
                '🎣 Evening bite typically picks up around 7pm and runs until dark',
                '🌅 The drive back is gorgeous through rolling forest and farmland'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Resort Restaurant or Cabin Cookout',
              description: 'Keep it simple tonight — grill steaks at your cabin or eat at the resort lodge. After a full day of exploring, a quiet dinner on the porch hits different.',
              meta: '💰 $–$$ · 📍 Your cabin or resort lodge'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.2388, lng: -95.2081, label: 'Mississippi Headwaters', num: 1, cat: 'attraction', desc: 'Where the Mississippi River begins — wade across it' },
        { lat: 47.2300, lng: -95.1900, label: 'Itasca State Park', num: 2, cat: 'attraction', desc: 'Minnesota\'s oldest state park — 32,000 acres of wilderness' },
        { lat: 47.2400, lng: -95.1850, label: 'Preacher\'s Grove', num: 3, cat: 'attraction', desc: '250-year-old red pine grove on Wilderness Drive' },
        { lat: 47.2355, lng: -95.1940, label: 'Douglas Lodge', num: 4, cat: 'food', desc: 'Historic 1905 lodge dining room on Lake Itasca' }
      ]
    },
    {
      num: 5,
      date: '2026-06-27',
      neighborhoods: 'Grand Rapids · Chippewa National Forest',
      title: 'Grand Rapids, Golf & Last Lakeside Evening',
      description: 'Explore the charming town of Grand Rapids — birthplace of Judy Garland — play a round of golf, pick up blueberries at a local farm, and spend your last evening savoring every minute on the lake.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grand Rapids Town Exploration',
              description: 'Drive 35 minutes south to Grand Rapids, the largest town near the lake. Visit the Judy Garland Museum (yes, Dorothy from Wizard of Oz was born here), browse the shops on Pokegama Avenue, and pick up local specialties to bring home.',
              details: [
                '🏠 The Judy Garland Museum has the actual house she was born in',
                '☕ Balsam Coffee Co. for excellent morning coffee',
                '🛍️ Pokegama Avenue has unique shops, galleries, and a co-op grocery',
                '🫐 Ask about local blueberry u-pick farms — late June is early season'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'The Sawmill Inn',
              description: 'Classic northern Minnesota breakfast spot in Grand Rapids. Big portions, strong coffee, and friendly service.',
              meta: '💰 $ · 📍 2301 S Pokegama Ave, Grand Rapids'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Golf or Berry Picking',
              description: 'Tee off at one of the area\'s scenic courses — Pokegama Golf Course in Grand Rapids winds through pines with lake views. Or if golf isn\'t your thing, hunt for wild blueberries in the national forest (they\'re just starting to ripen in late June).',
              details: [
                '⛳ Pokegama Golf Course — 18 holes, affordable, beautiful setting',
                '🫐 Wild blueberries grow along forest roads and clearings',
                '🌲 The national forest trails are quiet on weekday afternoons'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Sunset & Loon Serenade',
              description: 'Your last night on Big Winnie. Paddle out one more time, build one last fire, and listen to the loons say goodbye. The long June twilight stretches past 10pm — milk every minute of it.',
              details: [
                '🛶 Glass-calm evenings on Winnie are otherworldly',
                '🔥 Roast marshmallows and watch the northern sky for the last traces of light',
                '🦆 Count how many different loon calls you can identify — wail, tremolo, yodel, hoot'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Bowen Lodge Dining',
              description: 'End your trip with a special dinner at Bowen Lodge — lakeside dining in the heart of Chippewa National Forest. Fresh walleye, wild rice, and a sunset view you won\'t forget.',
              meta: '💰 $$–$$$ · 📍 Bowen Lodge, Cut Foot Sioux Lake'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.2372, lng: -93.5302, label: 'Grand Rapids', num: 1, cat: 'attraction', desc: 'Judy Garland\'s hometown — shops, restaurants, and culture' },
        { lat: 47.2380, lng: -93.5310, label: 'Judy Garland Museum', num: 2, cat: 'attraction', desc: 'Birthplace of Dorothy — museum and historic house' },
        { lat: 47.2200, lng: -93.5200, label: 'Pokegama Golf Course', num: 3, cat: 'attraction', desc: '18-hole course through pines and lake views' },
        { lat: 47.4700, lng: -94.0700, label: 'Bowen Lodge', num: 4, cat: 'food', desc: 'Lakeside dining on Cut Foot Sioux Lake' }
      ]
    },
    {
      num: 6,
      date: '2026-06-28',
      neighborhoods: 'Lake Winnibigoshish · Departure',
      title: 'One Last Cast & Heading Home',
      description: 'Wake up early for one final sunrise fishing session on Big Winnie, pack up the cabin, and head home with a cooler full of walleye and a head full of memories.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise Fishing — One Last Cast',
              description: 'Set your alarm for 5am and get on the water one more time. Early morning on Winnie in June is absolute magic — mist rising off the lake, loons calling, and walleye hitting hard. This is the memory that\'ll carry you through winter.',
              details: [
                '🌅 Sunrise is around 5:30am — the mist on the lake is ethereal',
                '🎣 Focus on the shallow reefs near shore — walleye feed aggressively at dawn',
                '📦 Clean and pack your fish in the resort\'s fish cleaning house'
              ]
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Pack Up & Depart',
              description: 'Check out of your cabin, load up the car, and take one long last look at the lake. Stop in Deer River or Grand Rapids for gas and a final cup of coffee before the drive home.',
              details: [
                '☕ Stop at a Grand Rapids café for the road',
                '🧊 Pack your fish in a quality cooler with plenty of ice — they\'ll be fine for the drive',
                '📸 Take a final dock photo before you leave'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Resort Breakfast or Deer River Café',
              description: 'Fuel up with a hearty northwoods breakfast before hitting the road — pancakes, eggs, bacon, and strong coffee.',
              meta: '💰 $ · 📍 Resort or Deer River'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.4336, lng: -94.0519, label: 'Lake Winnibigoshish', num: 1, cat: 'attraction', desc: 'One last sunrise on Big Winnie' },
        { lat: 47.3310, lng: -93.7110, label: 'Deer River', num: 2, cat: 'attraction', desc: 'Small town for a coffee stop on the way out' },
        { lat: 47.2372, lng: -93.5302, label: 'Grand Rapids', num: 3, cat: 'attraction', desc: 'Last stop for supplies before the drive home' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (cabin)', budget: '$100–150/night', midrange: '$150–250/night', luxury: '$250–400/night' },
    { category: 'Meals (per couple)', budget: '$40–70/day', midrange: '$70–120/day', luxury: '$120–200/day' },
    { category: 'Fishing Guide (half day)', budget: 'DIY ($0)', midrange: '$250–350', luxury: '$400–500 (full day)' },
    { category: 'Boat Rental', budget: '$80–120/day', midrange: '$120–180/day', luxury: '$200–300/day (pontoon)' },
    { category: 'Activities', budget: '$0–30/day', midrange: '$30–60/day', luxury: '$60–150/day' },
    { category: '5-Night Total (couple)', budget: '$1,200–2,200', midrange: '$2,200–4,000', luxury: '$4,000–7,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Grand Rapids airport (GPZ) is 35 min south — limited commercial flights', 'Bemidji airport (BJI) is 50 min west — seasonal service', 'Most visitors drive — about 4 hours from Minneapolis/St. Paul', 'Duluth is about 3 hours east'] },
    { title: '🏨 Where to Stay', items: ['High Banks Resort — full-service lodge with restaurant, cabins, and boat rentals', 'Bowen Lodge — family-run resort on Cut Foot Sioux Lake', 'Denny\'s Resort — south shore, established 1932, great fishing access', 'VRBO/Airbnb cabins — plenty of private options on the lake'] },
    { title: '🌡️ Weather', items: ['Late June: 75–85°F days, 55–60°F nights', 'Afternoon thunderstorms are common — check radar before going on the water', 'UV can be strong on the lake — bring sunscreen and a hat', 'Sunset around 9:15pm — incredibly long evenings'] },
    { title: '🛒 Supplies', items: ['Stock up in Grand Rapids (Walmart, grocery stores, liquor store) before heading to the lake', 'Bena and Deer River have basic supplies but limited selection', 'Bring your own specialty items — this is remote Minnesota', 'Don\'t forget: fishing license, bug spray, sunscreen, layers'] },
    { title: '📱 Connectivity', items: ['Cell service is spotty on the lake — Verizon has the best coverage', 'Most resorts have WiFi in the lodge area', 'Embrace the disconnect — that\'s half the point of being up here'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
