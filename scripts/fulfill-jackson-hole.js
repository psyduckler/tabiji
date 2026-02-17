const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771296505593_b21nb2',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Jackson Hole, WY, USA',
};

const itineraryData = {
  destination: 'Jackson Hole, WY, USA',
  countryEmoji: '🇺🇸',
  title: 'Jackson Hole Bachelorette: Tetons, Trails & Tequila',
  subtitle: '5 nights of mountain magic — whitewater rapids, cowboy bars, scenic hikes, spa days, and Grand Teton sunsets on a budget',
  description: 'Jackson Hole is the ultimate mountain-town bachelorette. Forget overpriced Vegas — this is where your crew trades bottle service for whitewater rapids, club lines for cowboy boot-stomping at the Million Dollar Cowboy Bar, and spa robes with a backdrop of the most dramatic peaks in North America. June means long golden days, wildflower meadows, and the Snake River running high. This itinerary packs adventure, relaxation, and celebration into five unforgettable days — all without breaking the bank.',
  duration: '5 nights',
  dates: 'Jun 18 – Jun 23, 2026',
  budget: '$80 – $150 per person/day',
  pace: 'Moderate-Active',
  bestFor: 'Bachelorette parties, Friend groups, Outdoor lovers',
  highlights: [
    'Whitewater rafting on the Snake River',
    'Grand Teton National Park hiking',
    'Million Dollar Cowboy Bar line dancing',
    'Scenic Snake River float trip',
    'Spa day with mountain views',
    'Town Square nightlife & cocktails',
    'Sunset at Schwabacher Landing'
  ],

  essentials: [
    { title: '🛬 Getting There', text: 'Fly into Jackson Hole Airport (JAC) — the only commercial airport inside a National Park. It\'s 15 minutes from town. Alternatively fly into Idaho Falls (IDA, ~2hr drive) or Salt Lake City (SLC, ~5hr drive) for cheaper fares. A rental car is recommended for park day trips, or split rideshares — START Bus runs free within Jackson.' },
    { title: '💵 Money', text: 'USD. Cards accepted everywhere. Jackson Hole isn\'t cheap, but you can save: pack picnic lunches for hike days, share vacation rentals instead of hotels, and hit happy hours. Budget $80-150/person/day for a fun but affordable trip.' },
    { title: '🌦️ June Weather', text: 'Warm days (65-80°F / 18-27°C), cool nights (35-45°F / 2-7°C). Afternoon thunderstorms are common — pack layers and a rain jacket. Sunscreen and sunglasses are essential at 6,200ft elevation. River water is COLD (snowmelt) — wetsuits provided for rafting.' },
    { title: '🐻 Wildlife Safety', text: 'You\'re in grizzly and black bear country. Carry bear spray on hikes ($8-10 rental at adventure shops). Keep food in bear boxes at trailheads. Moose are common and can be aggressive — give them 25+ yards. You WILL see wildlife; that\'s part of the magic.' },
    { title: '👢 What to Pack', text: 'Hiking boots or sturdy trail shoes, swimsuit (hot tub + river), cowboy boots or western wear for going out (borrow or buy at the Boot Barn in town!), layers for cool mountain evenings, and a fun sash/tiara for the bride-to-be.' },
    { title: '🏠 Where to Stay', text: 'Split an Airbnb or VRBO with the group — condos near Snow King or in Teton Village sleep 6-8 for $200-350/night total. The Hostel in Teton Village is surprisingly nice ($50-80/person). Anvil Hotel and The Lexington at Jackson Hole are affordable boutique options in town.' }
  ],

  days: [
    // DAY 1 — Arrival & Town Square
    {
      num: 1,
      title: 'Arrival & Cowboy Welcome',
      description: 'Fly in, settle into your rental, explore Jackson\'s iconic Town Square, shop for matching cowboy hats, and kick off the bachelorette at the legendary Million Dollar Cowboy Bar.',
      neighborhoods: 'Jackson Town Square · Cache Street · Million Dollar Cowboy Bar',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check In',
              description: 'Land at Jackson Hole Airport (JAC) with the Tetons literally right outside the terminal — the most scenic airport arrival in America. Pick up your rental car or arrange a shuttle to your Airbnb. Get the group settled and pop the first bottle of champagne on the deck.',
              details: [
                '💡 Stock up on groceries at Albertsons or Smith\'s — pack lunches for hike days save serious $$$',
                '💡 Rent bear spray at Teton Mountaineering or Adventure Sports — $8-10/day'
              ]
            },
            {
              title: 'Jackson Town Square & Shopping',
              description: 'Stroll through Jackson\'s famous Town Square with its four elk-antler arches. Browse the western boutiques along Cache Street and the Boardwalk — this is where you buy matching cowboy hats, "Bride" and "Bridal Posse" gear, and turquoise jewelry. Hit up JW Boot for affordable cowboy boots.',
              details: [
                '📍 Town Square, downtown Jackson',
                '💡 Photo op under the elk-antler arches — essential bachelorette content'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Thai Me Up',
              description: 'Affordable, fun, and delicious — this local-favorite Thai restaurant doubles as a brewery. Pad thai, curries, and craft beer on tap. Casual group-friendly vibe, and the price is right for a mountain town.',
              meta: '📍 75 E Pearl Ave · 💰 $15-22/person · 🍺 Try the Melvin Brewing beers on tap'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Million Dollar Cowboy Bar 🤠',
              description: 'THE iconic Jackson Hole bar — saddle-up at the bar stools (literally, they\'re saddles), dance to live country music, and soak in the Western atmosphere. This is non-negotiable for a Jackson bachelorette. Free entry, and drinks are surprisingly reasonable.',
              details: [
                '📍 25 N Cache St, Town Square',
                '🕐 Live music most nights starting 9pm',
                '💡 No cover charge! Go early to snag saddle barstools for the group',
                '💡 Wear your cowboy hats and bachelorette sashes — the bartenders love it'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'reddit', text: 'Million Dollar Cowboy Bar is a must. Sit at the saddle bar stools, grab a whiskey, and enjoy the live music. No cover, and it\'s genuinely fun — not just a tourist trap.', cite: 'r/JacksonHole' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.4799, lng: -110.7624, label: 'Jackson Hole Airport', num: 1, cat: 'transport', desc: 'America\'s most scenic airport — inside Grand Teton NP' },
        { lat: 43.4799, lng: -110.7624, label: 'Town Square', num: 2, cat: 'attraction', desc: 'Elk-antler arches and western shopping' },
        { lat: 43.4804, lng: -110.7624, label: 'Million Dollar Cowboy Bar', num: 3, cat: 'nightlife', desc: 'Iconic saddle barstools and live country music' },
        { lat: 43.4789, lng: -110.7614, label: 'Thai Me Up', num: 4, cat: 'restaurant', desc: 'Affordable Thai food + craft brewery' }
      ]
    },

    // DAY 2 — Whitewater Rafting & River Fun
    {
      num: 2,
      title: 'Whitewater Rafting the Snake River',
      description: 'Get your adrenaline pumping on a half-day whitewater rafting trip through Snake River Canyon — class II-III rapids with stunning canyon walls. Afternoon at the pool or exploring, then cocktails on the town square.',
      neighborhoods: 'Snake River Canyon · Alpine · Jackson Town',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Whitewater Rafting — Snake River Canyon 🌊',
              description: 'The highlight for any adventure bachelorette! Half-day whitewater trip through Snake River Canyon with class II-III rapids — exciting but no experience needed. Your guide handles the hard part while your crew screams, laughs, and gets soaked. June snowmelt means the rapids are pumping. Most outfitters include wetsuits and splash jackets.',
              details: [
                '📍 Snake River Canyon, south of Jackson (outfitters provide shuttle)',
                '🕐 8-9am pickup, ~3-4 hours on the water',
                '💰 $75-95/person with Mad River Boat Trips or Dave Hansen Whitewater',
                '💡 Book Mad River or Dave Hansen — both offer group rates for 5+',
                '💡 Bring a waterproof phone case or GoPro — these photos are GOLD'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Picnic at the River',
              description: 'Most rafting outfitters drop you back around 12-1pm. Grab deli sandwiches from Creekside Market & Deli in town for a budget-friendly post-rafting refuel. Eat on the Jackson Town Square lawn.',
              meta: '📍 145 E Broadway · 💰 $10-14/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Ask about group rates when booking rafting — most outfitters give 10-15% off for groups of 5+. Book 2-3 weeks ahead for June dates.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'R&R at Your Rental / Snow King Pool',
              description: 'After a morning in cold river water, recharge. Lounge at your rental\'s hot tub, or head to Snow King Resort\'s pool area. Paint nails, play games, do a champagne toast on the deck with the Tetons as your backdrop.',
              details: [
                '💡 Pick up wine and snacks at Jackson Whole Grocer for an affordable afternoon hang'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pinky G\'s Pizzeria',
              description: 'New York-style pizza in the heart of Jackson. Huge slices, cold beer, and a lively atmosphere. Perfect for a big group — share a few pies and keep it affordable. The pepperoni and the white pizza are both excellent.',
              meta: '📍 50 W Broadway · 💰 $12-18/person · 🍕 Cash-friendly prices'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Cocktails at The Rose',
              description: 'Jackson\'s chicest cocktail bar — craft cocktails in a cozy, stylish setting above the Pink Garter Theatre. The perfect elevated-but-chill bachelorette evening spot. Try the Huckleberry Mule (local huckleberry vodka + ginger beer).',
              details: [
                '📍 50 W Broadway (upstairs)',
                '💰 $12-16/cocktail',
                '💡 Go during happy hour (5-6pm) for discounted drinks'
              ]
            }
          ],
          meals: [],
          tips: []
        }
      ],
      mapPins: [
        { lat: 43.3722, lng: -110.8667, label: 'Snake River Canyon Rafting', num: 1, cat: 'activity', desc: 'Class II-III whitewater — half-day adventure' },
        { lat: 43.4785, lng: -110.7607, label: 'Creekside Market & Deli', num: 2, cat: 'restaurant', desc: 'Affordable deli sandwiches for post-rafting lunch' },
        { lat: 43.4773, lng: -110.7565, label: 'Snow King Resort', num: 3, cat: 'activity', desc: 'Pool, alpine slide, and mountain coaster' },
        { lat: 43.4806, lng: -110.7633, label: 'Pinky G\'s Pizzeria', num: 4, cat: 'restaurant', desc: 'NY-style pizza — affordable group dinner' },
        { lat: 43.4802, lng: -110.7633, label: 'The Rose', num: 5, cat: 'nightlife', desc: 'Craft cocktails — Huckleberry Mule is a must' }
      ]
    },

    // DAY 3 — Grand Teton National Park
    {
      num: 3,
      title: 'Grand Teton National Park Adventure',
      description: 'A full day in one of America\'s most stunning national parks — hike to stunning alpine lakes, spot moose and bald eagles, and catch an unforgettable Teton sunset at Schwabacher Landing.',
      neighborhoods: 'Grand Teton NP · Jenny Lake · Schwabacher Landing',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive into Grand Teton National Park',
              description: 'The Tetons are RIGHT THERE — just 15 minutes north of Jackson. Enter via Moose Junction and drive the Teton Park Road. Stop at the iconic Moulton Barn on Mormon Row for photos with the Tetons towering behind — one of the most photographed barns in America.',
              details: [
                '📍 Moose Junction entrance, Teton Park Rd',
                '💰 $35/vehicle park entrance (valid 7 days) — split 5 ways = $7/person!',
                '💡 Pack a full picnic lunch, tons of water, sunscreen, and bear spray'
              ]
            },
            {
              title: 'Cascade Canyon Trail via Jenny Lake ⛰️',
              description: 'Take the shuttle boat across Jenny Lake ($18 round trip) and hike into Cascade Canyon — one of the most spectacular trails in the Rockies. The trail follows a creek through a glacial canyon with 1,000ft granite walls on either side. Hike as far as you want — even 2 miles in is incredible. Wildflowers are peak in mid-June.',
              details: [
                '📍 Jenny Lake Visitor Center',
                '🕐 Boat shuttle runs 7am-7pm (June) · $18 round trip',
                '📏 5.8 miles round trip to Inspiration Point + Cascade Canyon overlook',
                '💡 Take the first boat (7am) to beat crowds — Jenny Lake is the park\'s most popular area',
                '⚠️ Carry bear spray! Grizzlies frequent this canyon in summer'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Picnic at String Lake',
              description: 'After the hike, drive 2 minutes to String Lake for a picnic lunch on the shore. The water is actually swimmable in late June (by Teton standards — it\'s refreshing!). Spread out blankets, wade in, and refuel with your packed sandwiches and snacks.',
              meta: '📍 String Lake Picnic Area · 💰 Free (bring your own food) · 🏊 Swimmable!'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Cascade Canyon is the best bang-for-your-buck hike in the Tetons. Take the boat across, hike to the fork, and you\'ll see some of the most insane scenery in the lower 48.', cite: 'r/GrandTetonNatlPark' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wildlife Spotting on the Drive Back',
              description: 'Drive the Teton Park Road south slowly — moose love the willow flats near Oxbow Bend and along the Snake River. Bison herds graze in the sagebrush flats. Stop at pullouts when you see cars gathered — that usually means something cool is nearby. Binoculars help.',
              details: [
                '📍 Oxbow Bend, Willow Flats, Snake River Overlook',
                '💡 The Snake River Overlook is where Ansel Adams took his famous photo — stop for the crew photo'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hatch Taqueria',
              description: 'Tacos and margaritas after a day in the Tetons — what more could you want? Fresh, affordable, with excellent fish tacos, elote, and a tequila-heavy drink menu. Perfect budget pick for a hungry hiking crew.',
              meta: '📍 10 E Broadway, Jackson · 💰 $14-20/person · 🌮 Fish tacos are legendary'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Schwabacher Landing 🌅',
              description: 'Drive 10 minutes from town to Schwabacher Landing on the Snake River — the most magical sunset spot in Jackson Hole. The Tetons reflect perfectly in the still beaver ponds, turning gold and pink. Bring champagne and toast the bride-to-be as the sky lights up. This will be the most liked photo from the whole trip.',
              details: [
                '📍 Schwabacher Landing Rd, off Hwy 89',
                '🕐 Arrive 45 min before sunset (~9pm in late June)',
                '💡 Bring bug spray, blankets, and bubbly — mosquitoes are real but the views are worth it'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 June sunset in Jackson Hole is around 9:15pm — you have LONG golden evening light. Schwabacher is free and the most Instagrammable spot in the valley.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.6643, lng: -110.6649, label: 'Mormon Row / Moulton Barn', num: 1, cat: 'attraction', desc: 'Iconic barn with Teton backdrop — ultimate photo op' },
        { lat: 43.7533, lng: -110.7228, label: 'Jenny Lake', num: 2, cat: 'attraction', desc: 'Shuttle boat + Cascade Canyon trailhead' },
        { lat: 43.7695, lng: -110.7320, label: 'String Lake', num: 3, cat: 'activity', desc: 'Swimmable lake + picnic area — post-hike hang' },
        { lat: 43.8567, lng: -110.5535, label: 'Oxbow Bend', num: 4, cat: 'attraction', desc: 'Premier wildlife viewing — moose, eagles, otters' },
        { lat: 43.4789, lng: -110.7614, label: 'Hatch Taqueria', num: 5, cat: 'restaurant', desc: 'Tacos, margs, and good vibes — budget-friendly' },
        { lat: 43.6425, lng: -110.6760, label: 'Schwabacher Landing', num: 6, cat: 'attraction', desc: 'Teton reflections at sunset — bring champagne' }
      ]
    },

    // DAY 4 — Spa Day & Scenic Float
    {
      num: 4,
      title: 'Spa Morning & Scenic Float Trip',
      description: 'Pamper the crew with a spa morning, then float the Snake River on a gentle scenic raft trip — spotting bald eagles and beavers with the Tetons as your backdrop. End with wine and a farewell dinner.',
      neighborhoods: 'Jackson · Snake River · Teton Village',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Spa Morning at Solitude Spa 💆‍♀️',
              description: 'Treat the bride (and yourselves). Solitude Spa at the Rustic Inn offers affordable group packages — massages, facials, and soaking pools with mountain views. Or go ultra-budget: DIY spa morning at your rental with face masks, mimosas, and matching robes from Target.',
              details: [
                '📍 Rustic Inn Creekside Resort, 475 N Cache St',
                '💰 $80-120 for a 60-min massage · Group packages available',
                '💡 Budget option: Body Sage Spa at The Lodge at JH also has group rates',
                '💡 Ultra-budget: grab face masks and nail polish from Smith\'s, mimosa bar at the rental'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'Persephone Bakery',
              description: 'Jackson\'s beloved French-inspired bakery and café. Flaky croissants, avocado toast, breakfast pastries, and excellent coffee. The line is part of the experience — and it moves fast. Perfect bachelorette brunch spot.',
              meta: '📍 145 E Broadway · 💰 $12-18/person · ☕ Get there before 9am to avoid the rush'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Scenic Snake River Float Trip 🛶',
              description: 'A totally different river experience from day 2 — this is a peaceful, scenic float through Grand Teton National Park on calm water. Your guide rows while you spot bald eagles, ospreys, beavers, and moose along the riverbanks. The Tetons tower above. Bring champagne in a tumbler for the ultimate chill bachelorette afternoon.',
              details: [
                '📍 Various put-ins along Snake River in GTNP',
                '🕐 ~3 hours on the water, afternoon departure',
                '💰 $85-100/person with Barker-Ewing Scenic Float Trips or Solitude Float Trips',
                '💡 This is calm water — no rapids. Great for anyone who skipped whitewater day',
                '💡 Bring layers — it\'s cooler on the water, even in June'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Café Genevieve',
              description: 'A Jackson institution in a charming 1910 log cabin on the Town Square. Southern-meets-Western comfort food — the Pig Candy (candied bacon) is famous. Great cocktails and a warm, celebratory atmosphere perfect for a bachelorette dinner. Share appetizers to keep costs down.',
              meta: '📍 135 E Broadway · 💰 $22-35/person · 🥓 The Pig Candy appetizer is NON-NEGOTIABLE'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Float trips run $85-100/person but the experience is magical — you\'re silently drifting through one of America\'s most beautiful landscapes. Worth every penny.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Last Night Out — Town Square Bar Hop 🍻',
              description: 'It\'s the last night — go all out. Start at The Silver Dollar Bar (bar top embedded with 2,032 silver dollars), move to the Roadhouse Brewing Company for craft beers, and end back at the Cowboy Bar for one last dance. Wear your cowboy hats and sashes — Jackson loves a bachelorette party.',
              details: [
                '📍 Silver Dollar Bar: 50 N Glenwood St (inside The Wort Hotel)',
                '📍 Roadhouse Brewing: 20 S Hwy 89',
                '💡 Silver Dollar has live music many nights — check the schedule',
                '💡 Most bars are walkable within a 3-block radius of Town Square'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'reddit', text: 'Silver Dollar Bar in The Wort Hotel is a Jackson classic — beautiful old bar with real silver dollars in the bartop. Get a Wyoming Whiskey cocktail.', cite: 'r/JacksonHole' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.4830, lng: -110.7630, label: 'Solitude Spa (Rustic Inn)', num: 1, cat: 'activity', desc: 'Spa morning — massages and mountain views' },
        { lat: 43.4785, lng: -110.7607, label: 'Persephone Bakery', num: 2, cat: 'restaurant', desc: 'French bakery — croissants and coffee' },
        { lat: 43.7200, lng: -110.6700, label: 'Snake River Scenic Float', num: 3, cat: 'activity', desc: 'Peaceful float trip through Grand Teton NP' },
        { lat: 43.4795, lng: -110.7618, label: 'Café Genevieve', num: 4, cat: 'restaurant', desc: '1910 log cabin — famous Pig Candy' },
        { lat: 43.4807, lng: -110.7644, label: 'Silver Dollar Bar', num: 5, cat: 'nightlife', desc: '2,032 silver dollars embedded in the bartop' },
        { lat: 43.4771, lng: -110.7621, label: 'Roadhouse Brewing', num: 6, cat: 'nightlife', desc: 'Local craft brewery — great beers and pizza' }
      ]
    },

    // DAY 5 — Adventure & Farewell
    {
      num: 5,
      title: 'Alpine Adventure & Farewell Brunch',
      description: 'One last morning of mountain fun — ride the Snow King Mountain alpine slide or hike the Josie\'s Ridge trail for a final Teton panorama. Farewell brunch and departure.',
      neighborhoods: 'Snow King · Jackson · Teton Views',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Snow King Mountain — Alpine Slide & Cowboy Coaster 🎢',
              description: 'Right in town and an absolute blast for groups. The Alpine Slide is a 2,500ft luge-style ride down the mountain. The Cowboy Coaster is a mountain roller coaster with Teton views. Buy combo tickets for the best deal. Arrive at opening for shorter lines.',
              details: [
                '📍 400 E Snow King Ave (base of Snow King Mountain)',
                '🕐 Opens 10am in summer',
                '💰 $20-30/person for combo tickets (slide + coaster)',
                '💡 Ride the scenic chairlift up for panoramic views, then slide/coast down'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'The Bunnery Bakery & Restaurant',
              description: 'A Jackson landmark since 1975. Famous for their O.S.M. (oat, sunflower, millet) bread and massive breakfast platters. The line wraps around the building but moves fast. The perfect final group meal — hearty, delicious, and not fancy-expensive.',
              meta: '📍 130 N Cache St · 💰 $14-20/person · 🍞 Try the O.S.M. French toast'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Snow King is the budget-friendly alternative to the Jackson Hole Mountain Resort tram ($40+). Same fun, way cheaper, and you can walk there from town.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last-Minute Shopping & Departure',
              description: 'Grab matching souvenirs on the Town Square — turquoise earrings, Wyoming-made hot sauce, huckleberry everything, or a "Jackson Hole" trucker hat. Pick up huckleberry fudge at Mountain Dandy for the flight home. Then it\'s hugs, happy tears, and promises to come back.',
              details: [
                '📍 Town Square shops & galleries',
                '💡 Jackson Hole Airport is 15 min from town — it\'s tiny and relaxed, no need for 2hr early arrival',
                '💡 Mountain Dandy on the square has the best candy and gifts'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 JAC airport is delightfully small. TSA takes 10 minutes. Arrive 1 hour before your flight and you\'re golden.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.4773, lng: -110.7565, label: 'Snow King Mountain', num: 1, cat: 'activity', desc: 'Alpine slide, cowboy coaster, and chairlift' },
        { lat: 43.4808, lng: -110.7625, label: 'The Bunnery', num: 2, cat: 'restaurant', desc: 'Famous O.S.M. bread and massive breakfasts since 1975' },
        { lat: 43.4799, lng: -110.7624, label: 'Town Square Shopping', num: 3, cat: 'shopping', desc: 'Last-minute souvenirs — huckleberry everything' },
        { lat: 43.6073, lng: -110.7378, label: 'Jackson Hole Airport', num: 4, cat: 'transport', desc: 'Tiny, relaxed airport inside Grand Teton NP' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (Airbnb split 5 ways)', perDay: '$40-70', total: '$200-350' },
    { category: 'Meals & Drinks', perDay: '$30-50', total: '$150-250' },
    { category: 'Whitewater Rafting', perDay: '—', total: '$75-95' },
    { category: 'Scenic Float Trip', perDay: '—', total: '$85-100' },
    { category: 'Grand Teton NP Entry (split)', perDay: '—', total: '$7' },
    { category: 'Jenny Lake Boat Shuttle', perDay: '—', total: '$18' },
    { category: 'Snow King Combo Ticket', perDay: '—', total: '$20-30' },
    { category: 'Spa Treatment', perDay: '—', total: '$80-120' },
    { category: 'Nightlife & Bars', perDay: '$15-25', total: '$75-125' },
    { category: 'TOTAL (per person)', perDay: '', total: '$710-1,095' }
  ],

  practicalInfo: [
    { title: '🚗 Getting Around', items: ['Rent one or two cars and split gas — you need wheels for the park and rafting trips', 'The free START Bus runs through town and to Teton Village', 'Uber/Lyft exist but are limited and expensive', 'Most downtown spots are walkable'] },
    { title: '🍺 Drinking Age & Laws', items: ['Wyoming drinking age is 21', 'Open container laws apply in vehicles but Jackson is very walkable between bars', 'Many bars don\'t charge cover — happy hours run 4-6pm'] },
    { title: '🏔️ Altitude', items: ['Jackson sits at 6,237 feet — you\'ll feel it if coming from sea level', 'Drink extra water, especially with alcohol', 'Take it easy on day 1 — hydrate, hydrate, hydrate'] },
    { title: '📱 Cell Service', items: ['Good in Jackson town, spotty to nonexistent in Grand Teton NP and on the river', 'Download offline maps (Google Maps or AllTrails) before heading out', 'Let someone know your plans on park/river days'] },
    { title: '📸 Photo Tips', items: ['Golden hour in June lasts forever (8-9:30pm)', 'Schwabacher Landing, Mormon Row, and Jenny Lake are the money shots', 'Bring a portable charger and waterproof phone case for rafting'] }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
