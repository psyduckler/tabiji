const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773098135999_bxymdk',
  email: 'hello@scanmyplan.com',
  destination: 'Dallas, TX, USA',
  startDate: '2026-03-13',
  endDate: '2026-03-15',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Dallas, Texas',
  countryEmoji: '🇺🇸',
  title: 'Solo in Big D: Dallas in 3 Days',
  subtitle: 'BBQ smoke, street murals, world-class museums & Texas-sized nightlife',
  description: "Dallas rewards the solo traveler who shows up curious. It's a city that's reinvented itself — think world-class art museums steps from a deck park, legendary brisket joints tucked into neon-lit warehouse districts, and neighborhoods where every wall is a mural. This 3-day itinerary covers the Arts District, Klyde Warren Park, the JFK Memorial, Deep Ellum's live music scene, Bishop Arts District's indie charm, and enough Texas BBQ to last a lifetime. No rental car needed — Dallas's DART rail and rideshares cover it all.",
  duration: '3 days',
  dates: 'Mar 13 – Mar 15, 2026',
  budget: '$–$$',
  pace: 'Active',
  bestFor: 'Solo Travelers',

  highlights: [
    'Legendary Texas BBQ at Pecan Lodge in Deep Ellum',
    'World-class art and dinosaurs at the Dallas Arts District & Perot Museum',
    'Live music crawl through Deep Ellum\'s neon-lit venues',
    'The JFK Sixth Floor Museum at Dealey Plaza',
    'Indie cafés, boutiques & brunches in Bishop Arts District'
  ],

  essentials: [
    {
      title: '🌤️ March Weather',
      text: 'March in Dallas is mild and pleasant — highs around 65–72°F (18–22°C), occasional rain showers. Pack a light layer for evenings. Perfect weather for walking neighborhoods.'
    },
    {
      title: '🚊 Getting Around',
      text: 'DART light rail connects downtown, Uptown, and Deep Ellum. Day passes are $6. For Bishop Arts and other spots, Uber/Lyft are cheap and fast. Much of central Dallas is walkable within neighborhoods.'
    },
    {
      title: '🤠 Texas Tips',
      text: 'Texans are famously friendly — strike up conversations at BBQ joints and bars. Portions are enormous; come hungry. Most BBQ spots sell out by early afternoon, so go by noon.'
    },
    {
      title: '🎵 Deep Ellum',
      text: 'Dallas\'s live music and art hub comes alive after 9pm. Venues like Trees, Club Dada, and Deep Ellum Art Co. host local and touring acts most nights. Check do214.com for the weekly lineup.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-13',
      neighborhoods: 'Arts District · Victory Park · Klyde Warren Park · Uptown',
      title: 'Art, Culture & the World\'s Largest Urban Deck Park',
      description: "Kick off in Dallas's cultural core — a walkable stretch connecting world-class museums, a stunning deck park over a freeway, and one of the city's buzziest dining neighborhoods. This is Big D at its most polished.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dallas Museum of Art',
              description: 'Start your Dallas trip at the DMA — one of the largest art museums in the country with over 24,000 works. Free general admission makes this a no-brainer. The ancient art collection, African art galleries, and the Impressionist wing are standouts.',
              details: [
                '🎨 Free general admission — always',
                '📍 1717 N Harwood St, Dallas TX 75201',
                '🕐 Open Tue–Sun, 11am–5pm (Fri until 9pm)',
                '📸 The modern sculpture on the lawn outside is Instagram gold'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Commissary',
              description: 'Beloved downtown Dallas breakfast and lunch spot known for excellent coffee, pastries, and avocado toast. Just a few blocks from the DMA.',
              meta: '💰 $ · 📍 1522 Main St, Dallas TX 75201'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Klyde Warren Park',
              description: 'Dallas\'s crown jewel — a 5.2-acre deck park built over a recessed freeway that bridges Uptown to the Arts District. Grab lunch from the rotating food truck lineup, walk the lawn, and people-watch. The park hosts free events and yoga classes most weekends.',
              details: [
                '🌿 2012 Woodall Rodgers Frwy, Dallas TX 75201',
                '🚚 Food trucks rotate daily — options from tacos to BBQ to gourmet grilled cheese',
                '🐶 Huge dog park and kids play area — great solo vibe',
                '📅 Check klydewarrenpark.org for weekend events'
              ]
            },
            {
              title: 'Nasher Sculpture Center',
              description: 'One of the world\'s finest private sculpture collections in a stunning Renzo Piano-designed building. The garden alone — with works by Rodin, Matisse, and Serra — is worth the price of admission.',
              details: [
                '🗿 2001 Flora St, Dallas TX 75201',
                '🕐 Tue–Sun, 11am–5pm',
                '💰 $10 admission · Free on the first Saturday of each month',
                '🌿 The outdoor sculpture garden is a peaceful retreat'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Uptown Dinner & Nightcap',
              description: 'Uptown is Dallas\'s most walkable dining and bar district. McKinney Avenue runs through the heart of it with restaurant patios, cocktail bars, and the vintage McKinney Avenue Trolley running for free.',
              details: [
                '🚃 McKinney Avenue Trolley is free and runs until 10pm on weekends',
                '🍸 Old Monk on Henderson is the OG Uptown bar — fantastic beer selection',
                '🌆 Rooftop bars along McKinney Ave have skyline views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Knife Dallas',
              description: 'Dallas\'s premier steakhouse in the Highland Dallas hotel. Chef John Tesar\'s Texas Wagyu steaks and dry-aged beef are legendary. The bar scene alone is worth a visit.',
              meta: '💰 $$$ · 📍 5300 E Mockingbird Ln, Dallas TX 75206'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'The Uptown Arts District stretch between the DMA and Klyde Warren Park is walkable in 10 minutes. Spend the day on foot — rideshare back to your hotel when you\'re done.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 32.7878, lng: -96.7999, label: 'Dallas Museum of Art', num: 1, cat: 'attraction', desc: 'Free world-class art museum — 24,000+ works' },
        { lat: 32.7894, lng: -96.8022, label: 'Klyde Warren Park', num: 2, cat: 'attraction', desc: 'Iconic deck park with food trucks and free events' },
        { lat: 32.7882, lng: -96.7988, label: 'Nasher Sculpture Center', num: 3, cat: 'attraction', desc: 'Renzo Piano garden full of Rodin and Matisse' },
        { lat: 32.7941, lng: -96.8085, label: 'Uptown / McKinney Ave', num: 4, cat: 'attraction', desc: 'Prime dining and bar district with free trolley' },
        { lat: 32.7928, lng: -96.7956, label: 'Commissary', num: 5, cat: 'food', desc: 'Top downtown breakfast spot near DMA' },
        { lat: 32.8234, lng: -96.7804, label: 'Knife Dallas', num: 6, cat: 'food', desc: 'Premier Texas steakhouse — Wagyu and dry-aged beef' }
      ]
    },
    {
      num: 2,
      date: '2026-03-14',
      neighborhoods: 'Downtown · West End · Deep Ellum · Bishop Arts District',
      title: 'History, BBQ & the Best Nightlife in Texas',
      description: "Dallas's most storied day: start at the Sixth Floor Museum where history stands still, grab legendary brisket in Deep Ellum, and spend the afternoon in Bishop Arts — the coolest neighborhood in the city. Then it's back to Deep Ellum for the best live music scene in Texas.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Sixth Floor Museum at Dealey Plaza',
              description: "One of the most powerful museum experiences in America. The Sixth Floor Museum occupies the very floor from which Lee Harvey Oswald fired on President Kennedy in 1963. The exhibits are meticulously curated and deeply moving. Dealey Plaza outside is surprisingly small — the tragedy hits differently in person.",
              details: [
                '📍 411 Elm St, Dallas TX 75202',
                '🕐 Open daily, 10am–6pm',
                '💰 $18 admission · Audio guide included',
                '🎧 The audio tour is essential — narrated by Dallas journalists and historians',
                '📸 The grassy knoll and X-mark on Elm St are right outside'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Ellen\'s',
              description: 'Classic Southern-style breakfast and brunch spot in the West End, blocks from Dealey Plaza. Famous for chicken and waffles and the bottomless mimosa brunch.',
              meta: '💰 $$ · 📍 1718 N Market St, Dallas TX 75202'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pecan Lodge — Legendary Texas BBQ',
              description: 'Deep Ellum\'s most beloved BBQ institution. Pecan Lodge is Texas Monthly-approved, perpetually lined up, and absolutely worth the wait. The beef brisket, pulled pork, and jalapeño cheddar sausage are all extraordinary. Go by noon before they sell out.',
              details: [
                '📍 2702 Main St, Dallas TX 75226 (Deep Ellum)',
                '🕐 Thu–Sun 11am–whenever they sell out (usually 2–3pm)',
                '💰 $$ · Cash and card accepted',
                '🔥 Order the "Trifecta": brisket + ribs + pulled pork',
                '⏰ Arrive before noon on weekends — lines form fast'
              ]
            },
            {
              title: 'Deep Ellum Street Art & Murals Walk',
              description: 'After lunch, walk off that BBQ by exploring Deep Ellum\'s legendary street art. Every block has massive murals — from portraits to geometric abstracts to cultural commentary. The area around Commerce Street and Malcolm X Blvd is especially dense with art.',
              details: [
                '🎨 Self-guided mural walk — no tickets needed',
                '📍 Center around Commerce St and Elm St in Deep Ellum',
                '📸 The "I Love You So Much" style murals are a Dallas tradition',
                '🏛️ Deep Ellum Art Co. hosts rotating gallery exhibitions'
              ]
            },
            {
              title: 'Bishop Arts District Afternoon',
              description: 'Uber 15 minutes southwest to Bishop Arts — Dallas\'s most charming neighborhood. Independent boutiques, vintage shops, galleries, and excellent cafés line Bishop Ave and Davis St. This is where Dallas locals actually hang out.',
              details: [
                '📍 Bishop Ave & Davis St, Dallas TX 75208 (Oak Cliff)',
                '☕ Houndstooth Coffee on Bishop — the city\'s best specialty coffee',
                '🛍️ Small boutiques, vintage finds, and local art galleries',
                '🌮 Get a taco at Vera\'s Backyard Bar-B-Que if you still have room'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Deep Ellum Live Music Crawl',
              description: "Head back to Deep Ellum after dinner for the best live music scene in Texas. On any given Friday or Saturday night, dozens of venues have live acts from 9pm onwards. Club Dada, Trees, Deep Ellum Art Co., Ruins, and the Prophet Bar are all within walking distance of each other.",
              details: [
                '🎸 Check do214.com for tonight\'s lineup across all venues',
                '🍺 Club Dada (2720 Elm St) — iconic indie/alternative venue since 1990',
                '🎵 Trees (2709 Elm St) — mid-size venue with national touring acts',
                '🍹 The Double Wide on Commerce — dive bar with great patio vibes',
                '🎨 Deep Ellum Art Co. (3200 Commerce St) — art gallery + live music'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Buli',
              description: 'Bishop Arts neighborhood gem serving Texas-meets-global cuisine. The wood-fired menu changes seasonally and the cocktail program is excellent. Lively solo-friendly bar seating available.',
              meta: '💰 $$ · 📍 408 W 8th St, Dallas TX 75208 (Bishop Arts)'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Deep Ellum is safest and most vibrant between 8pm and 2am on weekends. Stick to the main strips on Elm, Main, and Commerce. Everything is walkable within the neighborhood — save rideshare for getting home.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 32.7768, lng: -96.8089, label: 'Sixth Floor Museum at Dealey Plaza', num: 1, cat: 'attraction', desc: 'Powerful JFK assassination museum — a must-see' },
        { lat: 32.7849, lng: -96.7846, label: 'Pecan Lodge', num: 2, cat: 'food', desc: 'Texas Monthly\'s top Dallas BBQ — brisket and ribs' },
        { lat: 32.7836, lng: -96.7840, label: 'Deep Ellum Mural Walk', num: 3, cat: 'attraction', desc: 'Block after block of massive street art murals' },
        { lat: 32.7481, lng: -96.8296, label: 'Bishop Arts District', num: 4, cat: 'attraction', desc: 'Dallas\'s coolest indie neighborhood — cafés, boutiques, galleries' },
        { lat: 32.7848, lng: -96.7843, label: 'Club Dada / Trees', num: 5, cat: 'attraction', desc: 'Deep Ellum\'s iconic live music venues on Elm St' },
        { lat: 32.7767, lng: -96.8089, label: 'Ellen\'s', num: 6, cat: 'food', desc: 'Southern-style brunch spot near Dealey Plaza' },
        { lat: 32.7483, lng: -96.8290, label: 'Buli', num: 7, cat: 'food', desc: 'Wood-fired global cuisine in Bishop Arts' }
      ]
    },
    {
      num: 3,
      date: '2026-03-15',
      neighborhoods: 'Victory Park · Reunion Tower · Design District · Uptown',
      title: 'Dinosaurs, Skyline Views & a Texas Farewell',
      description: "Your final morning belongs to the Perot Museum — one of the best natural history museums in the country. Then it's a skyline moment at Reunion Tower before exploring the Design District's galleries and galleries. A Texas-worthy sendoff.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Perot Museum of Nature and Science',
              description: 'One of America\'s finest science museums, designed by Thom Mayne in a jaw-dropping angular building. The paleontology hall has a stunning T. rex specimen and full dinosaur skeletons. The energy hall, space hall, and children\'s exhibits are all world-class. Budget 2–3 hours.',
              details: [
                '📍 2201 N Field St, Dallas TX 75201',
                '🕐 Open Mon–Sat 10am–5pm, Sun noon–5pm',
                '💰 $25 adults · Buy tickets online to skip the line',
                '🦕 The Paleontology Hall is the crown jewel — the T. rex exhibit is stunning',
                '🏗️ The building itself is a work of architecture — photo from all angles'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast / Brunch',
              name: 'Klyde Warren Park Food Trucks',
              description: 'The park right across from the Perot Museum has rotating food trucks serving excellent breakfast items and coffee from around 8am on weekends. Grab something and eat on the lawn.',
              meta: '💰 $ · 📍 2012 Woodall Rodgers Frwy (across from Perot Museum)'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Reunion Tower GeO-Deck',
              description: "Dallas's iconic observation deck 470 feet up in the ball-shaped Reunion Tower. The GeO-Deck gives 360° views of the Dallas skyline and on a clear day you can see for 30 miles. Go in the afternoon for beautiful directional light before golden hour.",
              details: [
                '📍 300 Reunion Blvd E, Dallas TX 75207',
                '🕐 Daily 10am–9pm (Fri–Sat until 10pm)',
                '💰 $26 adults · Book online',
                '📸 The sweeping skyline panoramas are genuinely impressive',
                '🍸 Wolfgang Puck\'s Five Sixty restaurant is at the top if you want a splurge lunch'
              ]
            },
            {
              title: 'Design District Gallery Walk',
              description: "Dallas's Design District has transformed into a cultural hub with art galleries, concept stores, and great restaurants all within a few walkable blocks. Oak Street and Slocum Street are the core — pick up an afternoon coffee and browse.",
              details: [
                '📍 Design District centered around Oak St and Slocum St, Dallas TX 75207',
                '🎨 Dozens of contemporary art galleries — most are free to browse',
                '☕ Cultivar Coffee on Oak St — excellent single-origin pour-overs',
                '🛍️ Mix of high-design furniture showrooms and street-level boutiques'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Golden Hour at the Margaret Hunt Hill Bridge',
              description: "Before you leave, walk or Uber to the Margaret Hunt Hill Bridge at golden hour. Santiago Calatrava's stunning white arch bridge over the Trinity River turns golden in the late afternoon sun, with the downtown skyline as the backdrop. One of the most photogenic spots in Texas.",
              details: [
                '📍 Margaret Hunt Hill Bridge, Dallas TX 75212',
                '🌅 Best photographed from the west bank of the Trinity River',
                '🚶 Walk across the pedestrian path on the bridge itself',
                '📸 The Calatrava bridge + downtown skyline = peak Dallas shot'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Terry Black\'s Barbecue',
              description: "If you missed Pecan Lodge on Day 2, Terry Black's is your second-chance Texas BBQ redemption — and many argue it's even better. The beef ribs are the size of a fist and the margaritas are dangerously good.",
              meta: '💰 $$ · 📍 3025 Main St, Dallas TX 75226 (Deep Ellum)'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'If your flight is evening, you can easily add the Dallas Arboretum (a stunning 66-acre garden on White Rock Lake) as a morning detour before the Perot Museum. It\'s at its best in spring when the tulips and azaleas bloom.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 32.7872, lng: -96.8063, label: 'Perot Museum of Nature and Science', num: 1, cat: 'attraction', desc: 'World-class science museum with T. rex hall and space exhibits' },
        { lat: 32.7757, lng: -96.8098, label: 'Reunion Tower GeO-Deck', num: 2, cat: 'attraction', desc: '470-foot observation deck with 360° Dallas skyline views' },
        { lat: 32.7833, lng: -96.8152, label: 'Design District', num: 3, cat: 'attraction', desc: 'Art galleries, concept stores, and excellent coffee' },
        { lat: 32.7826, lng: -96.8296, label: 'Margaret Hunt Hill Bridge', num: 4, cat: 'attraction', desc: 'Calatrava\'s iconic white arch bridge — golden hour must' },
        { lat: 32.7849, lng: -96.7799, label: 'Terry Black\'s Barbecue', num: 5, cat: 'food', desc: 'Outstanding Texas BBQ — beef ribs and margaritas' },
        { lat: 32.7894, lng: -96.8022, label: 'Klyde Warren Park Food Trucks', num: 6, cat: 'food', desc: 'Rotating trucks serving breakfast near the Perot Museum' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–130/night', midrange: '$130–200/night', luxury: '$200–400/night' },
    { category: 'Meals (per day)', budget: '$30–50/day', midrange: '$50–90/day', luxury: '$100–200/day' },
    { category: 'Transport (DART + rideshare)', budget: '$10–20/day', midrange: '$20–40/day', luxury: '$40–80/day' },
    { category: 'Activities', budget: '$0–30/day', midrange: '$30–70/day', luxury: '$70–150/day' },
    { category: '3-Day Total (solo)', budget: '$350–600', midrange: '$600–1,000', luxury: '$1,000–2,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Dallas Love Field (DAL) — 10 min from downtown, served by Southwest', 'Dallas/Fort Worth Int\'l (DFW) — 30 min, major hub with all carriers', 'DART Orange Line from DFW to downtown: $2.50 flat', 'Uber/Lyft from Love Field to downtown: $15–20'] },
    { title: '🏨 Where to Stay', items: ['Downtown / Arts District — walkable to most Day 1 sights', 'Uptown — best dining and bar access, safe and walkable', 'Deep Ellum — ideal if you\'re there for the music scene', 'Budget: SpringHill Suites Downtown, Hilton Garden Inn', 'Mid-range: Adolphus Hotel (historic gem), Lorenzo Hotel (Design District)'] },
    { title: '🌡️ March Weather', items: ['Highs: 65–72°F (18–22°C)', 'Occasional rain — pack a light packable jacket', 'Evenings can cool to 50°F — bring a layer for outdoor patios', 'Wildflower season begins in late March — beautiful'] },
    { title: '💳 Money', items: ['Dallas is very card/tap-friendly', 'BBQ joints: some are cash-only or prefer it — carry $40 in cash', 'Tipping: 18–20% at sit-down restaurants, $1–2/drink at bars'] },
    { title: '📱 Getting Around', items: ['DART Day Pass ($6) for light rail and buses', 'GoPass app for DART tickets on your phone', 'Uber/Lyft: very affordable and abundant in Dallas', 'Lime and Bird scooters available in most neighborhoods'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
