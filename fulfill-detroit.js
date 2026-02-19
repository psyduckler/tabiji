const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771454412814_g80naz',
  email: 'psyduckler@gmail.com',
  destination: 'Detroit, MI, USA',
  startDate: '2026-02-25',
  endDate: '2026-03-01',
  groupSize: '5+',
  requests: 'boys get together trip'
};

const itineraryData = {
  destination: 'Detroit, MI, USA',
  countryEmoji: '🇺🇸',
  title: 'Motor City Reunion: A Detroit Bros Trip',
  subtitle: '4 nights of craft beer, live music, muscle cars & legendary eats with the boys',
  description: "Detroit is having its moment — and it's the perfect city for a crew of guys looking to eat big, drink well, and have stories to tell. From the birthplace of Motown and techno to a revitalized downtown packed with breweries, speakeasies, and some of the best Middle Eastern food outside Beirut, the Motor City delivers. This itinerary balances daytime culture (car museums, street art, sports) with epic group dinners, dive bars, and late-night adventures across Detroit's distinct neighbourhoods.",
  duration: '4 nights',
  dates: 'Feb 25 – Mar 1, 2026',
  budget: '$$',
  pace: 'Moderate',
  bestFor: 'Groups · Friends · Guys trips',
  highlights: [
    'The Henry Ford Museum — jaw-dropping automotive history',
    'Dearborn\'s legendary Middle Eastern food strip',
    'Craft brewery crawl through Eastern Market & Corktown',
    'Live music at iconic Detroit venues',
    'Greektown casino night with the crew'
  ],

  essentials: [
    { title: '🥶 Late February Weather', text: 'Expect 0–5°C (32–41°F) with possible snow. Pack warm layers, a solid winter coat, and boots with grip. Indoor activities are plentiful so you won\'t freeze.' },
    { title: '🚗 Getting Around', text: 'Rent a car or use Uber/Lyft. Detroit is spread out and public transit is limited. The QLine streetcar covers Woodward Ave downtown. Parking is cheap and abundant compared to most cities.' },
    { title: '🍺 Drinking Scene', text: 'Detroit\'s craft beer scene is elite — Atwater, Batch, Jolly Pumpkin, and dozens more. Corktown and Midtown are the brewery hotspots. Bars stay open until 2am.' },
    { title: '👥 Group Tips', text: 'Most restaurants accommodate big groups with a heads-up call. Eastern Market on Saturday is a must for the group energy. Book a large Airbnb in Corktown or Midtown for the best location.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-25',
      neighborhoods: 'Downtown · Greektown',
      title: 'Arrive & Hit the Ground Running',
      description: 'Roll into Detroit, get settled, and kick off the trip with downtown exploration, a group dinner in Greektown, and a casino night to set the tone.',
      mapPins: [
        { lat: 42.3314, lng: -83.0458, label: 'Detroit Marriott Renaissance Center', num: 1, cat: 'hotel', desc: 'Downtown hotel with river views' },
        { lat: 42.3358, lng: -83.0404, label: 'Spirit of Detroit', num: 2, cat: 'activity', desc: 'Iconic Detroit sculpture photo op' },
        { lat: 42.3348, lng: -83.0394, label: 'Campus Martius Park', num: 3, cat: 'activity', desc: 'Downtown gathering spot with ice rink' },
        { lat: 42.3365, lng: -83.0383, label: 'Pegasus Taverna', num: 4, cat: 'food', desc: 'Greektown staple for group dinner' },
        { lat: 42.3361, lng: -83.0367, label: 'MGM Grand Detroit', num: 5, cat: 'nightlife', desc: 'Casino night with the crew' }
      ],
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Downtown Detroit Walk',
              description: 'Drop your bags and explore downtown on foot. Hit the Spirit of Detroit statue for the obligatory group photo, stroll along the Detroit Riverwalk with views of Windsor, Canada, and check out Campus Martius Park where you can ice skate in winter.',
              details: [
                '📸 Spirit of Detroit — the group photo spot, right on Woodward Ave',
                '🏙️ Detroit Riverwalk — 5.5 miles along the river, stunning even in winter',
                '⛸️ Campus Martius ice rink — $10 with skate rental'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Late Lunch',
              name: 'Buddy\'s Pizza',
              description: 'The birthplace of Detroit-style pizza — thick, square, crispy-edged, cheese-to-the-crust perfection. Order the Detroiter (pepperoni, tomato basil sauce on top). Essential eating for first-timers.',
              meta: '💰 $ · 📍 1565 Broadway St, Downtown · No reservations needed'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Greektown Exploration',
              description: 'Detroit\'s Greektown is a compact, neon-lit strip of restaurants, bars, and the MGM Grand casino. It\'s loud, lively, and perfect for a group\'s first night out. Wander Monroe Street, pop into bars, and soak up the energy.',
              details: [
                '🎰 MGM Grand, MotorCity Casino, and Greektown Casino are all within reach',
                '🍸 Greektown bars are casual and group-friendly',
                '📍 Everything is walkable within a few blocks'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pegasus Taverna',
              description: 'A Greektown institution. Flaming saganaki (they yell "Opa!"), lamb chops, and gyro platters — perfect for sharing with the crew. Loud, festive, and exactly the vibe for night one.',
              meta: '💰 $$ · 📍 558 Monroe St, Greektown · Call ahead for large group'
            }
          ],
          tips: [
            { type: 'tip', text: 'Set a casino budget before you walk in — $50-100 per person keeps it fun without the regret. The table games (blackjack, craps) are more fun as a group than slots.' }
          ]
        }
      ]
    },
    {
      num: 2,
      date: '2026-02-26',
      neighborhoods: 'Dearborn · Corktown',
      title: 'Cars, Coney Dogs & Corktown Brews',
      description: 'Spend the morning geeking out at the Henry Ford Museum, feast on legendary Dearborn Middle Eastern food, then bar-hop through Corktown\'s brewery scene.',
      mapPins: [
        { lat: 42.3040, lng: -83.2341, label: 'The Henry Ford Museum', num: 1, cat: 'activity', desc: 'World-class automotive & American history museum' },
        { lat: 42.3022, lng: -83.2497, label: 'Al-Ameer Restaurant', num: 2, cat: 'food', desc: 'Best Lebanese food in Metro Detroit' },
        { lat: 42.3319, lng: -83.0636, label: 'Batch Brewing Company', num: 3, cat: 'nightlife', desc: 'Corktown craft brewery' },
        { lat: 42.3311, lng: -83.0601, label: 'Mercury Bar', num: 4, cat: 'nightlife', desc: 'Iconic Corktown dive bar' },
        { lat: 42.3325, lng: -83.0566, label: 'Slows Bar BQ', num: 5, cat: 'food', desc: 'Famous Corktown BBQ joint' }
      ],
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Henry Ford Museum of American Innovation',
              description: 'This is not your average museum. The Henry Ford houses the bus Rosa Parks sat on, the chair Lincoln was assassinated in, JFK\'s presidential limo, and acres of vintage cars. Even non-car guys will be impressed. Plan 3+ hours.',
              details: [
                '🚗 Don\'t miss the "Driving America" exhibit — a century of auto evolution',
                '🎫 $28 adult admission — buy online to skip the line',
                '📸 The Presidential Limousine collection is unreal'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: 'Greenfield Village (outdoor portion) is closed in winter, but the indoor museum alone is worth the trip. Budget at least 3 hours.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dearborn Middle Eastern Food Crawl',
              description: 'Dearborn has the highest concentration of Arab Americans in the US, and the food is extraordinary. Warren Avenue and Michigan Avenue are lined with Lebanese, Yemeni, and Iraqi restaurants that blow away anything you\'ve had back home.',
              details: [
                '🧆 Al-Ameer — award-winning hummus, shawarma, and lamb',
                '🫓 Shatila Bakery — Middle Eastern pastries that\'ll change your life',
                '🥙 Bucharest Grill for late-night shawarma (bookmark for later)'
              ]
            }
          ],
          meals: [
            {
              type: '🥙 Lunch',
              name: 'Al-Ameer Restaurant',
              description: 'The gold standard of Dearborn Lebanese cuisine. Massive platters of hummus, tabbouleh, grilled kebabs, and shawarma. Order the mixed grill for the table and let everyone share. Unbeatable value.',
              meta: '💰 $ · 📍 12710 W Warren Ave, Dearborn · Large groups welcome'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Corktown Brewery Crawl',
              description: 'Corktown is Detroit\'s oldest neighborhood and its hottest. Hit Batch Brewing for creative small-batch beers, then Mercury Bar (a legendary dive), and end at Motor City Brewing Works for pizza and pints.',
              details: [
                '🍺 Batch Brewing — try the rotating IPAs and stouts',
                '🥃 Mercury Bar — cash only, cheap drinks, perfect dive bar energy',
                '🍕 Motor City Brewing Works — craft beer + brick oven pizza combo'
              ]
            }
          ],
          meals: [
            {
              type: '🍖 Dinner',
              name: 'Slows Bar BQ',
              description: 'The BBQ spot that helped put Corktown on the map. Brisket, pulled pork, mac & cheese — the works. It gets packed, so call ahead or go slightly early (5:30pm). Great bourbon list too.',
              meta: '💰 $$ · 📍 2138 Michigan Ave, Corktown · Reservations recommended for groups'
            }
          ],
          tips: [
            { type: 'tip', text: 'Corktown bars are close together — you can hit 4-5 spots on foot. The neighborhood is safe and walkable. Uber back to downtown when you\'re done.' }
          ]
        }
      ]
    },
    {
      num: 3,
      date: '2026-02-27',
      neighborhoods: 'Eastern Market · Midtown',
      title: 'Eastern Market, Street Art & Live Music',
      description: 'Explore Detroit\'s massive Eastern Market, check out world-class street art murals, hit the Motown Museum, and catch live music in Midtown.',
      mapPins: [
        { lat: 42.3490, lng: -83.0400, label: 'Eastern Market', num: 1, cat: 'activity', desc: 'Historic public market — Saturday is the big day' },
        { lat: 42.3500, lng: -83.0420, label: 'Eastern Market Murals', num: 2, cat: 'activity', desc: 'World-famous street art' },
        { lat: 42.3641, lng: -83.0886, label: 'Motown Museum (Hitsville USA)', num: 3, cat: 'activity', desc: 'Where Motown Records started' },
        { lat: 42.3560, lng: -83.0660, label: 'Hopcat', num: 4, cat: 'food', desc: 'Craft beer bar with 100+ taps' },
        { lat: 42.3530, lng: -83.0680, label: 'Majestic Theatre', num: 5, cat: 'nightlife', desc: 'Iconic live music venue' }
      ],
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Eastern Market Saturday Market',
              description: 'If it\'s Saturday (Feb 27 is a Friday — hit the Friday market or just explore the permanent murals and shops). Eastern Market is Detroit\'s beating heart — six massive sheds full of vendors, plus world-famous murals painted on every surface. Even on non-Saturday days, the murals and surrounding shops are worth the trip.',
              details: [
                '🎨 The Murals in the Market festival has turned every wall into gallery-grade street art',
                '🥩 Gratiot Central Market is open daily for meats, cheeses, and snacks',
                '📸 The colorful murals are some of the best street art in America'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Supino Pizzeria (Eastern Market)',
              description: 'Yes, pizza for breakfast. Supino\'s thin-crust, wood-fired slices are legendary. Grab a few pies for the group — the margherita and soppressata are perfect. Cash only.',
              meta: '💰 $ · 📍 2457 Russell St, Eastern Market · Cash only'
            }
          ],
          tips: [
            { type: 'tip', text: 'Friday is actually a great day for Eastern Market — fewer crowds, same murals, and the surrounding businesses (Vivio\'s, Russell Street Deli) are all open.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Motown Museum (Hitsville USA)',
              description: 'Stand in Studio A where the Supremes, Stevie Wonder, Marvin Gaye, and the Temptations recorded their hits. The guided tour is genuinely moving — even if you\'re not a huge Motown fan, the history and the tiny studio will give you chills.',
              details: [
                '🎵 Guided tours only — book online in advance ($17)',
                '🎤 You\'ll stand on the exact spot where "My Girl" was recorded',
                '📸 The blue Hitsville USA house is an iconic Detroit photo'
              ]
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: 'Tours sell out, especially weekends. Book at least a few days ahead. The tour is about 1 hour and worth every minute.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Midtown Bar Hop & Live Music',
              description: 'Midtown is Detroit\'s cultural corridor — DIA, Wayne State, and a strip of excellent bars and venues. Start at Hopcat (130+ beers on tap), grab dinner, then catch a show at the Majestic Theatre or Garden Bowl (America\'s oldest bowling alley, with live music upstairs).',
              details: [
                '🍺 Hopcat — 130+ craft beers on tap, legendary Crack Fries',
                '🎶 Majestic Theatre / Magic Stick — check listings for live shows',
                '🎳 Garden Bowl — bowling + live bands + cheap drinks = perfect group night'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Selden Standard',
              description: 'The best restaurant in Midtown — seasonal, ingredient-driven small plates meant for sharing. Order a spread for the table: roasted bone marrow, wood-fired vegetables, house-made pasta. Excellent cocktails. This is the "nice dinner" of the trip.',
              meta: '💰 $$$ · 📍 3921 Second Ave, Midtown · Reservations essential for groups'
            }
          ],
          tips: [
            { type: 'tip', text: 'Garden Bowl (bowling alley above the Majestic) is a perfect group activity — cheap lanes, live music some nights, and a full bar. Great way to end the evening.' }
          ]
        }
      ]
    },
    {
      num: 4,
      date: '2026-02-28',
      neighborhoods: 'Belle Isle · Mexican Town · Downtown',
      title: 'Belle Isle, Tacos & Final Night Out',
      description: 'Drive out to Belle Isle for winter scenery and the aquarium, hit Mexican Town for tacos, then send it on the final big night downtown.',
      mapPins: [
        { lat: 42.3449, lng: -82.9726, label: 'Belle Isle Aquarium', num: 1, cat: 'activity', desc: 'Free historic aquarium on the island' },
        { lat: 42.3422, lng: -82.9815, label: 'Belle Isle Conservatory', num: 2, cat: 'activity', desc: 'Tropical plants in a glass dome — free' },
        { lat: 42.3225, lng: -83.0775, label: 'Mexicantown', num: 3, cat: 'food', desc: 'Authentic Mexican food strip' },
        { lat: 42.3256, lng: -83.0791, label: 'El Asador Steakhouse', num: 4, cat: 'food', desc: 'Mexican steakhouse for the final dinner' },
        { lat: 42.3341, lng: -83.0497, label: 'Cliff Bell\'s', num: 5, cat: 'nightlife', desc: 'Art deco jazz club — Detroit classic' }
      ],
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Belle Isle State Park',
              description: 'A 982-acre island park in the Detroit River with skyline views, a free aquarium (the oldest in the US), a botanical conservatory, and the Dossin Great Lakes Museum. Even in winter, the drive around the island and indoor attractions make it worth the visit.',
              details: [
                '🐠 Belle Isle Aquarium — free admission, gorgeous historic building',
                '🌴 Anna Scripps Whitcomb Conservatory — tropical escape from the cold, also free',
                '🚗 Michigan Recreation Passport required ($17/day or $32/year)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Rose\'s Fine Food',
              description: 'A beloved Detroit diner with a cult following. House-made everything — biscuits, sausage, hash. The kind of no-frills, perfect breakfast that\'s worth a wait. Gets crowded on weekends.',
              meta: '💰 $ · 📍 10551 E Jefferson Ave · Cash only, no reservations'
            }
          ],
          tips: [
            { type: 'tip', text: 'Belle Isle is gorgeous even in winter — the frozen river views and empty paths make for great photos. The aquarium and conservatory are both free and heated.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mexican Town Food Crawl',
              description: 'Detroit\'s Mexicantown (around Vernor Highway and Bagley) is packed with authentic taquerias, bakeries, and markets. Walk the strip, grab tacos from multiple spots, and pick up pastries from a Mexican bakery.',
              details: [
                '🌮 Taqueria Nuestra Familia — street-style tacos, cash only',
                '🍰 Mexicantown Bakery — conchas and tres leches',
                '🛒 Honey Bee Market — browse the aisles for hot sauce and snacks to bring home'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Lunch',
              name: 'Taqueria El Rey',
              description: 'No-frills, fluorescent-lit, and absolutely delicious. Tacos al pastor, barbacoa, and lengua that rival anything in a border town. The salsa bar is serious. Order at the counter and grab a table.',
              meta: '💰 $ · 📍 4730 Vernor Hwy, Mexicantown · Order at counter'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Night: Cliff Bell\'s & Downtown',
              description: 'Make the last night count. Start at Cliff Bell\'s — a stunning 1935 art deco jazz club with live music nightly and craft cocktails. Then hit the downtown bars for a final send-off. Sugar House (speakeasy) and The Apparatus Room (Shinola Hotel bar) are both excellent options.',
              details: [
                '🎷 Cliff Bell\'s — live jazz Wed-Sat, no cover most nights',
                '🥃 The Sugar House — Detroit\'s best speakeasy-style cocktail bar',
                '🏨 The Apparatus Room at Shinola Hotel — upscale nightcap spot'
              ]
            }
          ],
          meals: [
            {
              type: '🥩 Dinner',
              name: 'El Asador Steakhouse',
              description: 'A Mexican steakhouse in Mexicantown — thick ribeyes, carne asada, chorizo appetizers, and strong margaritas. Perfect for a group\'s final dinner. The vibe is celebratory and loud, exactly what you want for the last night.',
              meta: '💰 $$ · 📍 1312 Springwells St, Mexicantown · Reservations strongly recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'Cliff Bell\'s gets busy on weekends — arrive by 8pm for a good table. The cocktails are excellent. Dress a notch above casual but don\'t overthink it.' }
          ]
        }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData);
