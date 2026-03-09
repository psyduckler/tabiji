const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772417061858_ll0dbb",
  email: "cdpartner@gmail.com",
  destination: "Disneyland, Anaheim, CA",
  start_date: "2026-04-10",
  end_date: "2026-04-13",
  group_size: "3-4",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-03-02T02:04:21.858Z",
  status: "pending"
};

const itineraryData = {
  destination: "Disneyland, Anaheim, CA",
  countryEmoji: "🏰",
  title: "Disneyland in 3 Days: The Magic Kingdom Playbook",
  subtitle: "Disneyland Park · Disney California Adventure · Downtown Disney",
  description: "Three days at Disneyland Anaheim for a group of 3-4 in spring — timed for April when the weather is perfect, the flowers are blooming, and spring break crowds are thinning. This is the insider strategy guide: when to hit which rides, where to eat, how to avoid the lines, and how to make every moment magical. No fairy tale fluff — just real park strategy that maximizes fun and minimizes waiting.",
  duration: "3 nights / 4 days (arrive Apr 10, depart Apr 13)",
  dates: "Apr 10 – 13, 2026",
  budget: "$3,000–5,000 (park tickets, hotel, food, Genie+)",
  pace: "High-energy mornings → leisurely afternoons → magical evenings",
  bestFor: "Groups of 3-4, families, first-timers and returnees alike",
  highlights: [
    "Rope drop Disneyland at 8am — hit Star Wars: Galaxy's Edge before the crowds",
    "Indiana Jones Adventure — walk-on in the first hour, 60-min wait by noon",
    "Radiator Springs Racers at DCA — must-do, get Lightning Lane early",
    "Mickey's Toontown — newly reimagined in 2023, perfect for the group",
    "World of Color at DCA — spectacular nighttime water show",
    "Main Street at night — castle lit up, fireworks above Sleeping Beauty Castle",
    "Club 33 may be off the table, but Carthay Circle Restaurant is the elegant upgrade",
    "April weather: 68–75°F, low humidity, evening breezes — peak Disneyland conditions",
    "Dole Whip at the Tiki Juice Bar — the original, not the franchise versions",
    "Monte Cristo sandwich at Blue Bayou — bucket list Disney dining"
  ],
  essentials: [
    {
      title: "🎢 Genie+ & Lightning Lane Strategy",
      text: "Buy Genie+ ($35-45/person/day) — it's worth every penny. At 7am sharp (before park opening), book your first Lightning Lane on the Disneyland app. Priority order: Radiator Springs Racers (DCA), Indiana Jones (DL), Matterhorn (DL). Individual Lightning Lane (ILL) costs extra ($18-25/person) for premium rides: Rise of the Resistance and Radiator Springs Racers. Buy ILL as soon as the park app opens — they sell out before rope drop. Stack your Genie+ selections throughout the day as each is used."
    },
    {
      title: "📱 Disneyland App — Download Before You Go",
      text: "The Disneyland app is non-negotiable. Use it for: real-time wait times for every attraction, Lightning Lane bookings, mobile food ordering (skip the counter line), Genie+ management, and show/parade schedules. Set up your group's account linking before you arrive. Turn on notifications for Genie+ availability. Mobile Order from the app and pick up at the window — saves 20-30 minutes per meal."
    },
    {
      title: "🌸 April at Disneyland",
      text: "April is one of the best months to visit. Spring break peaks in late March/early week of April — by April 10, crowds are tapering. Weather is ideal: 68-75°F, sunny, low humidity. Disneyland is in full spring bloom with flowers throughout the park. Easter weekend (if applicable) can spike — check the calendar. Weekdays (Mon-Thu) are meaningfully less crowded than weekends."
    },
    {
      title: "🏨 Where to Stay",
      text: "Disney Hotels (Grand Californian, Disneyland Hotel, Paradise Pier) give you Early Entry (30 min before general public) — worth the premium for a 3-day trip. Grand Californian is IN the park (DCA entrance is right there) — the nicest option. Alternative: off-property hotels on Harbor Blvd run $150-250/night vs $400-600 for Disney hotels. With Early Entry, the Disney hotels pay for themselves in avoided wait times. Book the Disneyland Hotel for a classic experience at a slightly lower price point."
    },
    {
      title: "💵 Budget Reality Check",
      text: "Two parks, 3 days: park tickets ~$150-200pp/day (3-day Park Hopper ~$420-500pp). Genie+ adds ~$35-45/person/day. Food runs $15-25pp for counter service, $45-80pp for table service. Parking is $30/day (free if staying at a Disney hotel). Budget ~$500-700/day for a group of 4, all-in. Pro tip: breakfast at the hotel saves $20/person vs in-park breakfast. Pack snacks — bringing food is allowed."
    },
    {
      title: "🎭 Must-Know Park Tips",
      text: "Rope drop (first hour) is when you conquer the big rides — do 2-3 major attractions before most guests have had coffee. Single Rider lines (Radiator Springs Racers, Matterhorn, Indiana Jones) can cut wait times by 50-70% for groups willing to split up. Character meet-and-greets book up fast — check the app on arrival. Parades close walkways and spike nearby attraction waits — use parade time to hit rides in other lands. Rider Switch lets adults swap between riding and waiting with non-riders."
    }
  ],
  days: [
    {
      num: 1,
      title: "Rope Drop Disneyland — Classic Park Day",
      neighborhoods: "Main Street · Adventureland · Fantasyland · Tomorrowland",
      date: "Apr 10",
      mapPins: [
        { lat: 33.8121, lng: -117.9190, label: "Main Street USA", num: 1, cat: "activity", desc: "The iconic entry to the Magic Kingdom" },
        { lat: 33.8115, lng: -117.9211, label: "Indiana Jones Adventure", num: 2, cat: "activity", desc: "Best ride in Adventureland — walk-on at rope drop" },
        { lat: 33.8109, lng: -117.9219, label: "Jungle Cruise", num: 3, cat: "activity", desc: "Skipper puns and animatronic animals" },
        { lat: 33.8130, lng: -117.9185, label: "Matterhorn Bobsleds", num: 4, cat: "activity", desc: "Classic alpine roller coaster" },
        { lat: 33.8128, lng: -117.9192, label: "Space Mountain", num: 5, cat: "activity", desc: "Iconic dark roller coaster in the dark" },
        { lat: 33.8112, lng: -117.9190, label: "Blue Bayou Restaurant", num: 6, cat: "food", desc: "Dinner inside the Pirates of the Caribbean queue" }
      ],
      timeBlocks: [
        {
          label: "Morning — Rope Drop Strategy",
          activities: [
            {
              title: "7am App Alarm — Lock Lightning Lanes",
              description: "Before you even get out of bed, open the Disneyland app at 7:00am sharp. Book your Individual Lightning Lanes for the day's priorities. This is non-negotiable — Rise of the Resistance and Radiator Springs Racers sell out within minutes of 7am. If staying at a Disney hotel, you get 30 minutes of Early Entry — use it.",
              details: [
                "📱 Priority ILL: Rise of the Resistance (if visiting DCA tomorrow), Radiator Springs Racers",
                "⚡ First Genie+ selection: Indiana Jones (do this at 7am — you can book once you're in the park)",
                "💡 Set three alarms: 6:58am, 7:00am, 7:01am. Seriously."
              ]
            },
            {
              title: "Rope Drop — Indiana Jones to Jungle Cruise",
              description: "Get to the park entrance 20-30 minutes before opening. When the gates open, move with purpose (not run) to Adventureland. Indiana Jones Adventure at rope drop is a walk-on — by 9:30am it's 45 minutes, by noon it's 60+. Ride it twice if you can. Then immediately hit Jungle Cruise — the skippers are freshest in the morning and the puns hit harder before you're tired.",
              details: [
                "📍 Indiana Jones: Adventureland, towards the back — follow the signs",
                "💡 The queue for Indiana Jones is one of the best-designed queues in any park — take it slow on your second ride to see all the details",
                "🎟️ Jungle Cruise: typically 15-25 min wait in first hour"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Carnation Café (Main Street) or hotel breakfast",
              description: "Carnation Café opens at park open on Main Street — Mickey waffle, eggs, and fresh pastries in a classic setting overlooking the hub. Or save money and grab breakfast at your hotel before heading in. Mobile Order if eating in-park.",
              meta: "$18-28pp · Main Street USA · Mobile Order via Disneyland app"
            }
          ],
          tips: [
            { type: "tip", text: "The first 90 minutes after park open are golden. The rides you wait 60 minutes for at 11am are walk-ons at 8am. Protect this window — save the shows and shopping for afternoons." }
          ]
        },
        {
          label: "Mid-Morning — Fantasyland & New Orleans Square",
          activities: [
            {
              title: "Haunted Mansion",
              description: "One of Disney's all-time classics. The Haunted Mansion queue itself is a masterpiece of themed design — a Victorian estate full of tombstones and gags. The ride is fun and atmospheric, appropriate for all ages. Watch for the hitchhiking ghosts in your Doom Buggy at the end.",
              details: [
                "📍 New Orleans Square — next door to Pirates of the Caribbean",
                "💡 'Stretching room' at the start is a classic Disney storytelling moment — pay attention",
                "⚡ Use Genie+ if wait is over 30 min"
              ]
            },
            {
              title: "Pirates of the Caribbean",
              description: "The original — Johnny Depp's Jack Sparrow was based on THIS ride, not the other way around. Glide through a dark bayou into a swashbuckling pirate town. Genuinely atmospheric and fun. Kids love it, adults get hit with nostalgia.",
              details: [
                "📍 New Orleans Square, right next to Blue Bayou restaurant",
                "💡 Sit on the right side for the best views of the battle scene"
              ]
            },
            {
              title: "Space Mountain & Tomorrowland",
              description: "Head to Tomorrowland mid-morning before lunch rush. Space Mountain is a classic indoor roller coaster in total darkness — the 'roller coaster in the dark' experience is timeless. Buzz Lightyear Astro Blasters is fun for groups (it's competitive — everyone gets a score). Star Wars: Hyperspace Mountain runs seasonal overlays.",
              details: [
                "📍 Tomorrowland — left from the castle hub",
                "💡 Buzz Lightyear is low-wait and highly competitive — compare scores after",
                "⚡ Space Mountain: use Genie+ if wait exceeds 25 min"
              ]
            }
          ],
          meals: [],
          tips: [
            { type: "reddit", text: "Space Mountain in the morning is a walk-on or near walk-on. By 11am it's 40 minutes. Tomorrowland is almost always less crowded in the first two hours than Adventureland or Fantasyland.", cite: "r/Disneyland" }
          ]
        },
        {
          label: "Afternoon — Fantasyland & Mickey's Toontown",
          activities: [
            {
              title: "Mickey's Toontown",
              description: "The completely reimagined Toontown (reopened 2023) is one of the best additions to Disneyland in decades. Designed for all ages — it's not just a kids area anymore. Wandering through Mickey's house, Minnie's house, and the interactive outdoor areas is genuinely fun. CenTOONial Park is perfect for groups to hang out and recharge.",
              details: [
                "📍 Between Fantasyland and Tomorrowland, separate gated land",
                "💡 Mickey and Minnie Mouse character meets are here — check the app for meet times",
                "🎢 Chip 'n' Dale's GADGETcoaster: fun quick ride, low wait"
              ]
            },
            {
              title: "Big Thunder Mountain Railroad",
              description: "The 'wildest ride in the wilderness!' — a fantastic family roller coaster through a haunted gold mine. Smooth, fun, and intense enough to be thrilling without being scary. One of Disneyland's best rides and often overlooked for the headliners. Do this in the afternoon with a Genie+ reservation.",
              details: [
                "📍 Frontierland",
                "💡 Boarding at the back of the mine train gives a wilder ride",
                "⚡ Use Genie+ — waits hit 45-60 min in the afternoon"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Rancho del Zocalo Restaurante (Frontierland)",
              description: "One of the best counter-service options in the park. Mexican-inspired plates — enchiladas, burritos, carne asada. Fast-casual, generous portions, and the outdoor seating near Big Thunder Mountain is genuinely scenic. Mobile Order ahead to skip the counter line.",
              meta: "$18-26pp · Frontierland · Mobile Order via app"
            }
          ],
          tips: [
            { type: "tip", text: "Afternoon (1-4pm) is when crowds peak everywhere. This is the perfect time to: grab a Dole Whip at the Tiki Juice Bar in Adventureland, explore Club Buzz / Tomorrowland shops, or simply sit on a bench and people-watch. The park is beautiful; you don't have to be on a ride every minute." }
          ]
        },
        {
          label: "Evening — Main Street Magic & Fireworks",
          activities: [
            {
              title: "Main Street Electrical Parade / Fireworks",
              description: "Check the evening entertainment schedule in the app. Disneyland's nighttime shows are worth staying for — 'Wondrous Journeys' fireworks over Sleeping Beauty Castle is genuinely spectacular. The castle lit up at night against fireworks is the quintessential Disneyland image. Get a spot on the hub (in front of the castle) 30-45 minutes early.",
              details: [
                "📍 Stake out a spot in the castle hub for fireworks — the raised viewing area on either side is best",
                "💡 The fireworks are short (~20 min) but incredible — it's worth the wait",
                "⚠️ Check the app for specific show times on your date — schedules vary"
              ]
            },
            {
              title: "Late Night Ride — Haunted Mansion or Space Mountain",
              description: "After the fireworks, the crowds leave or scatter. Head to your favorite ride for one final go — waits often drop to near-zero in the last 30 minutes before close. End the night on a high note.",
              details: [
                "💡 The park clears 15-20 min after fireworks — this is prime late-night ride time"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Blue Bayou Restaurant",
              description: "The crown jewel of Disneyland dining. You eat inside the Pirates of the Caribbean — literally in the bayou, watching boats drift by in the dim, blue-lit darkness with fireflies overhead. Cajun-inspired menu: Monte Cristo sandwich (worth the hype), gumbo, prime rib, fantastic cocktails. This is a bucket list Disney experience. Reserve weeks in advance.",
              meta: "$60-90pp · New Orleans Square (inside Pirates queue) · OpenTable reservation required — book 30-60 days ahead"
            }
          ],
          tips: [
            { type: "reddit", text: "Blue Bayou is overpriced but you're paying for the experience, not just the food. The Monte Cristo sandwich is legendary and correct. The atmosphere of eating 'inside' the Pirates ride at night is something you can't get anywhere else on earth. Do it once.", cite: "r/Disneyland" }
          ]
        }
      ]
    },
    {
      num: 2,
      title: "Disney California Adventure — Cars, Avengers & World of Color",
      neighborhoods: "Buena Vista Street · Cars Land · Avengers Campus · Pixar Pier",
      date: "Apr 11",
      mapPins: [
        { lat: 33.8058, lng: -117.9218, label: "Radiator Springs Racers", num: 1, cat: "activity", desc: "The crown jewel of DCA — Cars Land's centerpiece" },
        { lat: 33.8052, lng: -117.9192, label: "Avengers Campus", num: 2, cat: "activity", desc: "WEB SLINGERS and Doctor Strange's Sanctum Sanctorum" },
        { lat: 33.8068, lng: -117.9197, label: "Guardians of the Galaxy", num: 3, cat: "activity", desc: "Massive drop tower with a classic rock soundtrack" },
        { lat: 33.8055, lng: -117.9175, label: "Pixar Pier", num: 4, cat: "activity", desc: "Incredicoaster, Toy Story, and waterfront fun" },
        { lat: 33.8073, lng: -117.9229, label: "Carthay Circle Restaurant", num: 5, cat: "food", desc: "Iconic 1930s movie palace — upscale DCA dining" },
        { lat: 33.8060, lng: -117.9203, label: "World of Color", num: 6, cat: "activity", desc: "Spectacular nighttime water and light show" }
      ],
      timeBlocks: [
        {
          label: "Morning — Cars Land Before the Crowds",
          activities: [
            {
              title: "Radiator Springs Racers — The Crown Jewel",
              description: "DCA's best ride and consistently rated one of the top theme park attractions in the world. You board a little car and cruise through the world of Cars before being launched into a racing finale. At rope drop, waits are 20-30 minutes (vs 90-120 min at noon). If you bought Individual Lightning Lane at 7am, use it wisely — even better, hit it at rope drop AND use ILL later for a second ride.",
              details: [
                "📍 Cars Land — follow Radiator Springs signs as soon as DCA opens",
                "⚡ ILL costs ~$20/person — worth it for a group of 4 if the line is long",
                "💡 The ride through Ornament Valley at sunset (artificial, but beautiful) changes with time of day — dusk setting is magic"
              ]
            },
            {
              title: "Luigi's Rollickin' Roadsters & Mater's Junkyard Jamboree",
              description: "While in Cars Land, hit both the secondary rides — they're fun, low-wait, and the Cars Land theming is breathtaking. Route 66 gas stations, Flo's V8 Café, the Cozy Cone Motel — it's one of the most immersive themed environments Disney has ever created.",
              details: [
                "💡 Cars Land at night (later this evening or tomorrow morning) is stunning — neon lights everywhere"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Flo's V8 Café (Cars Land)",
              description: "Classic American diner-style breakfast inside Cars Land, themed as a 1950s roadside café. Pancakes, biscuits and gravy, breakfast burritos. The theming is excellent and it feels very much like you're in Radiator Springs.",
              meta: "$16-24pp · Cars Land · Mobile Order via Disneyland app"
            }
          ],
          tips: [
            { type: "reddit", text: "Cars Land at night is one of Disney's finest design achievements. The entire land transforms after dark — neon signs, Route 66 vibes, Radiator Springs Racers glowing. If you're in DCA in the evening, walk through Cars Land regardless of whether you're riding.", cite: "r/Disneyland" }
          ]
        },
        {
          label: "Mid-Morning — Avengers Campus",
          activities: [
            {
              title: "WEB SLINGERS: A Spider-Man Adventure",
              description: "The most innovative attraction in Avengers Campus — you use hand gestures (literally shooting webs like Spidey) to capture Spider-Bots on screens around you. Interactive, competitive between your group, and surprisingly physical. Kids and adults both love it. Check wait times — often lower than Guardians.",
              details: [
                "📍 Avengers Campus — west side of DCA",
                "💡 The ride scores your web-slinging — it's a competitive group experience"
              ]
            },
            {
              title: "Guardians of the Galaxy — Mission: BREAKOUT!",
              description: "A massive drop tower set to a killer classic rock soundtrack. You're 'breaking out' the Guardians from The Collector's collection. The random music rotation means every ride is different — you might get Immigrant Song, you might get Fisher's Shakedown. Thrilling, loud, and enormous fun. One of the best rides in either park.",
              details: [
                "📍 Near the entrance of DCA — the big tower you can see from Harbor Blvd",
                "⚡ Use Genie+ for this one — waits hit 60-90 min by midday",
                "💡 The music changes randomly each ride — try to ride twice for different songs"
              ]
            }
          ],
          meals: [],
          tips: [
            { type: "tip", text: "Avengers Campus has character meets with actual Marvel heroes — Black Panther, Spider-Man, Thor, Black Widow. They do meet-and-greet 'moments' throughout the day, not traditional queued meets. Keep an eye on the app for appearances." }
          ]
        },
        {
          label: "Afternoon — Pixar Pier & Downtown Disney",
          activities: [
            {
              title: "Incredicoaster (Pixar Pier)",
              description: "DCA's major roller coaster — a fun, classic coaster along the waterfront with Incredibles theming. Good for all thrill-seekers in the group. The views of Paradise Bay from the top are great.",
              details: [
                "📍 Pixar Pier — the colorful pier along Paradise Bay",
                "⚡ Single Rider line often available and much shorter"
              ]
            },
            {
              title: "Toy Story Midway Mania!",
              description: "A must-do interactive ride — you 'throw' virtual rings, darts, and balls at carnival game targets. Incredibly fun for groups (competitive scoring), smooth ride, great for all ages. One of the most rerideable attractions in either park.",
              details: [
                "💡 This is a great one to hit during afternoon peak hours when outdoor rides are crowded",
                "⚡ Use Genie+ — this ride gets backed up quickly"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Shawarma Palace (Avengers Campus)",
              description: "Exactly what it sounds like — a shawarma spot in Avengers Campus (reference to the post-credits scene in The Avengers). The Mediterranean bowls, pita wraps, and falafel are all good and genuinely filling. Great theming, outdoor seating, reasonably priced for Disney.",
              meta: "$18-25pp · Avengers Campus · Mobile Order via app"
            }
          ],
          tips: [
            { type: "tip", text: "Afternoon is perfect for Downtown Disney — right outside the parks, free to access, tons of dining and shopping options. Great for the group to split up: half shop while half continue in the park." }
          ]
        },
        {
          label: "Evening — World of Color",
          activities: [
            {
              title: "World of Color Nighttime Show",
              description: "DCA's signature nighttime spectacular — a 22-minute show of water, light, fire, and lasers projected on a massive mist screen over Paradise Bay, synchronized to iconic Disney music. One of the most impressive theme park nighttime shows ever created. Get World of Color Viewing Area access via the Disneyland app (free with park admission, but you must secure a spot). Arrive 30 minutes early for a good viewing position.",
              details: [
                "📍 Paradise Bay, DCA — main viewing area in front of the water",
                "⚡ Book World of Color Viewing experience in the app same day as visit — it's free but fills up",
                "💡 Arrive 30 min early for center viewing. Bring a light jacket — the mist travels"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Carthay Circle Restaurant",
              description: "DCA's finest dining — inside a recreation of the Carthay Circle Theatre where Snow White premiered in 1937. Table-service with California cuisine: fresh pasta, beautiful steaks, excellent cocktails. The ambiance is as good as anything in either park. Perfect for a special group dinner. Reserve in advance.",
              meta: "$65-95pp · Buena Vista Street, DCA · Reserve on Disneyland app or OpenTable — book 30-60 days ahead"
            }
          ],
          tips: [
            { type: "reddit", text: "Grab a cocktail at the Carthay Circle Lounge even if you can't get a dinner reservation — it's a beautiful bar with a view of Buena Vista Street, and you can mobile-order appetizers. Far superior to most DCA dining.", cite: "r/Disneyland" }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Galaxy's Edge, Matterhorn & The Grand Finale",
      neighborhoods: "Star Wars: Galaxy's Edge · Frontierland · New Orleans Square · Main Street",
      date: "Apr 12",
      mapPins: [
        { lat: 33.8145, lng: -117.9224, label: "Star Wars: Galaxy's Edge", num: 1, cat: "activity", desc: "Batuu — immersive Star Wars land" },
        { lat: 33.8155, lng: -117.9218, label: "Rise of the Resistance", num: 2, cat: "activity", desc: "The most technologically complex theme park ride ever built" },
        { lat: 33.8153, lng: -117.9226, label: "Millennium Falcon: Smugglers Run", num: 3, cat: "activity", desc: "Fly the Falcon — you're the crew" },
        { lat: 33.8131, lng: -117.9178, label: "Matterhorn Bobsleds", num: 4, cat: "activity", desc: "Classic Alpine coaster — the OG Disney thrill ride" },
        { lat: 33.8112, lng: -117.9186, label: "Pirates of the Caribbean", num: 5, cat: "activity", desc: "Farewell lap through the bayou" },
        { lat: 33.8105, lng: -117.9186, label: "Main Street USA", num: 6, cat: "activity", desc: "Final walk down Main Street before departure" }
      ],
      timeBlocks: [
        {
          label: "Morning — Star Wars: Galaxy's Edge",
          activities: [
            {
              title: "Rise of the Resistance — Do Not Skip This",
              description: "The most ambitious, technologically complex theme park ride ever built. You're captured by the First Order and must escape — the scale, the immersion, the sheer number of Audio-Animatronics and practical effects is staggering. Multiple ride systems, enormous sets, real AT-AT walkers above you. This is what $200 million and ten years of Imagineering looks like. The ILL is worth every penny. Buy it at 7am.",
              details: [
                "📍 Star Wars: Galaxy's Edge, back corner — follow the trail through Batuu",
                "⚡ Individual Lightning Lane: ~$20/person — absolutely required. It sells out before the park opens.",
                "💡 The pre-show areas before the main ride are part of the experience — don't rush"
              ]
            },
            {
              title: "Millennium Falcon: Smugglers Run",
              description: "You sit in the cockpit of the ACTUAL Millennium Falcon (1:1 scale) and fly her on a smuggling mission. Three roles: pilots (you actually fly it), gunners, and engineers. Pilots get the most immersive experience — try to be seated as a pilot. The Falcon is enormous and breathtaking in person.",
              details: [
                "📍 Galaxy's Edge — you can't miss the Falcon in the center of the land",
                "💡 Walk up to Dok-Ondar's Den of Antiquities to see amazing Star Wars collectibles — a working lightsaber costs $200+ but is iconic",
                "🎟️ Build your own lightsaber at Savi's Workshop: $250/person — worth it if any group member is a Star Wars superfan (reserve in advance)"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Docking Bay 7 Food and Cargo (Galaxy's Edge)",
              description: "The main restaurant in Batuu — themed as a salvage yard/food stall with inventive Star Wars menu items. The Endorian Fried Chicken Tip-Yip with roasted grain and mashed peas is genuinely excellent. Ronto Roasters outside has ronto wraps (a must-try from the outdoor cart). Blue or green milk is a Galaxy's Edge pilgrimage.",
              meta: "$18-28pp · Galaxy's Edge · Mobile Order highly recommended"
            }
          ],
          tips: [
            { type: "reddit", text: "Galaxy's Edge is the most impressive themed land Disney has ever built, full stop. Even if you're not a Star Wars fan, walk through it and look up. The level of detail — the alien script on every surface, the droids wandering around, the starships overhead — is unreal. Take your time.", cite: "r/Disneyland" }
          ]
        },
        {
          label: "Afternoon — Matterhorn & Favorites Lap",
          activities: [
            {
              title: "Matterhorn Bobsleds",
              description: "The original Disney thrill ride — opened in 1959, still amazing. Two bobsled tracks weave through the Swiss Alps (complete with a Yeti) in an outdoor roller coaster that was groundbreaking for its era. The roughness is part of the charm — it's a classic. Take it as a nod to Disney history.",
              details: [
                "📍 Fantasyland/Tomorrowland border — the big mountain you can see from everywhere",
                "💡 Left track is slightly different from right track — both worth riding",
                "⚡ Use Genie+ to avoid waits"
              ]
            },
            {
              title: "Any Missed Rides — Rider's Choice",
              description: "Use this time to hit anything you didn't get to in the first two days. Top candidates: Star Tours (Tomorrowland), Finding Nemo Submarine Voyage, Alice in Wonderland (Fantasyland), or just revisit your group favorites. Check wait times on the app and target anything under 20 minutes.",
              details: [
                "💡 Star Tours is underrated — 50+ different route combinations with hyper-specific Star Wars references. No wait in the afternoon sometimes."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Dole Whip at the Tiki Juice Bar + Relaxed Counter Service",
              description: "First, get your Dole Whip — the original pineapple soft-serve from the Tiki Juice Bar near the Tiki Room in Adventureland. This is sacred. Then grab a casual lunch at Bengal Barbecue (Adventureland) — chicken skewers and tiger tail breadsticks, perfect for walking. Mobile Order both.",
              meta: "$10-20pp · Adventureland · The Dole Whip float (pineapple juice + whip) is the move"
            }
          ],
          tips: [
            { type: "reddit", text: "The Bengal Barbecue tiger tail breadstick is criminally underrated Disneyland food. It's a grilled breadstick with garlic and cheese. It costs $5 and is better than 90% of the restaurant food in the park. Get one for everyone.", cite: "r/Disneyland" }
          ]
        },
        {
          label: "Evening — Main Street Last Night & Fantasmic!",
          activities: [
            {
              title: "Fantasmic! Nighttime Show",
              description: "Mickey Mouse's dreamscape battle against Disney villains — live performers, water screens, fire, lasers, and a massive finale with a steamboat full of Disney characters. One of Disney's all-time greatest nighttime shows. The River Theatre in Frontierland holds thousands, but still fills up — arrive 30-40 minutes early. Check if it runs on your date (schedules vary).",
              details: [
                "📍 Frontierland River Theatre — seats 9,000 but still fills up",
                "💡 Fantasmic! Dining Package secures reserved seating — worth it if you want front-center views (book in advance)",
                "⚠️ Confirm Fantasmic! is running on your date via the app — it's seasonal"
              ]
            },
            {
              title: "Final Main Street Walk & Souvenirs",
              description: "End your last night with a slow walk down Main Street. The Emporium has the best souvenir selection. Crystal Arts has personalized items. Pick up the iconic Mickey ears, pressed pennies, or Disney pins. Main Street at night, castle glowing, music playing softly — this is the image you carry home.",
              details: [
                "💡 The Disneyland pin trading community is massive — starter pin sets are $10-15 and trading with Cast Members is free",
                "📍 Emporium: right on Main Street at the start — you passed it on day one"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Café Orleans (New Orleans Square)",
              description: "The casual sibling to Blue Bayou — same New Orleans-inspired menu, outdoor courtyard seating in the most beautiful part of the park. The pommes frites with three dipping sauces are legendary, the Monte Cristo sandwich rivals Blue Bayou's, and the mint julep (non-alcoholic) is classic. Walkup or Mobile Order.",
              meta: "$30-50pp · New Orleans Square · Mobile Order available — no reservation needed"
            }
          ],
          tips: [
            { type: "reddit", text: "Café Orleans' Monte Cristo and pommes frites are legitimately some of the best food in Disneyland. The non-alcoholic mint julep is a park staple. If you couldn't get Blue Bayou, this is the local's choice — same New Orleans vibes for $25 less.", cite: "r/Disneyland" }
          ]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "Park Tickets (3-Day Park Hopper × 4 people)", low: "$1,400", mid: "$1,700", high: "$2,000" },
    { category: "Genie+ (3 days × 4 people)", low: "$360", mid: "$450", high: "$540" },
    { category: "Individual Lightning Lanes (key rides)", low: "$80", mid: "$150", high: "$240" },
    { category: "Hotel (3 nights)", low: "$450", mid: "$900", high: "$1,800" },
    { category: "Meals (in-park + Downtown Disney)", low: "$600", mid: "$900", high: "$1,400" },
    { category: "Merchandise & Extras", low: "$100", mid: "$200", high: "$400" },
    { category: "Transportation (parking or rideshare)", low: "$90", mid: "$120", high: "$150" },
    { category: "TOTAL (group of 4)", low: "~$3,080", mid: "~$4,420", high: "~$6,530" }
  ],
  practicalInfo: [
    {
      title: "🚗 Getting There",
      items: [
        "From LAX: ~40 miles, 45-75 min (traffic-dependent). Rideshare ~$50-80 each way. Rental car parking is $30/day on-site.",
        "Harbor Blvd offramp from I-5 — direct to Disneyland parking structure. The Mickey & Friends parking structure is steps from the main entrance.",
        "Anaheim Resort Transit (ART) shuttles run between many Harbor Blvd hotels and the park entrance. If staying off-property, this saves $30/day parking.",
        "Flying into John Wayne Airport (SNA) is closer — 15 miles, ~20 minutes. Often cheaper than LAX for Anaheim trips."
      ]
    },
    {
      title: "📅 April Crowd Levels",
      items: [
        "April 10-13 is post-spring-break — generally Tier 3 out of 5 crowds. Still busy on weekends but manageable on weekdays.",
        "Avoid going on Easter Sunday/weekend (falls around Apr 5, 2026) — the week after is much calmer.",
        "Best days: Monday-Wednesday. Avoid Saturday at all costs.",
        "Park hours in April: typically 8am-12am on weekdays, 8am-1am on weekends. Check the calendar closer to your trip."
      ]
    },
    {
      title: "🎢 Ride Height Requirements",
      items: [
        "If any group members have height restrictions, check in advance. Big Thunder Mountain: 40\". Matterhorn: 35\". Space Mountain: 40\". Rise of the Resistance: 40\". Incredicoaster: 48\". Guardians: 40\".",
        "Rider Swap is available at all height-restricted rides — adults can wait with a non-rider while the rest of the group rides, then swap without waiting in line again."
      ]
    },
    {
      title: "🎒 What to Pack",
      items: [
        "Comfortable walking shoes — you'll walk 8-12 miles per day. Broken-in sneakers are essential.",
        "Light layers — April days are warm (68-75°F) but evenings cool to 55-60°F. A light jacket for after 7pm.",
        "Portable phone charger — the Disneyland app kills your battery.",
        "Sunscreen — California sun is strong even in April.",
        "Refillable water bottle — there are water bottle refill stations throughout the park (free water at any counter service).",
        "Snacks from outside — outside food is allowed (no glass containers, no alcohol). Granola bars and trail mix save $15-20/day."
      ]
    },
    {
      title: "📞 Key Contacts",
      items: [
        "Disneyland Reservations: 714-781-4565",
        "Blue Bayou Restaurant: reserve at disneyland.disney.go.com or OpenTable",
        "Medical: First Aid at Main Street and DCA entrance. Cast Members are trained for all scenarios.",
        "Lost & Found: Central Services on Main Street or call 714-817-2166"
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
