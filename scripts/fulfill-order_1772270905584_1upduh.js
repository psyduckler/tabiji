const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772270905584_1upduh',
  email: 'monisavant9999@gmail.com',
  destination: 'Edinburgh, Scotland, UK',
};

const itineraryData = {
  destination: 'Edinburgh & Scotland',
  countryEmoji: '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
  title: 'Scotland: Castles, Highlands & the Outer Isles',
  subtitle: '16 days of Edinburgh\'s medieval wynds, Stirling\'s battlefields, Glencoe\'s dramatic glens, Loch Ness\'s shores, and the wild magic of the Isle of Lewis — solo, adventurous, and on a budget',
  description: 'This is Scotland at full stretch. You\'ll begin in Edinburgh — one of Europe\'s most atmospheric cities — wandering cobblestone closes, climbing Arthur\'s Seat at dawn, and exploring the world-class National Museum. From there, a day in Stirling unlocks the story of Scottish independence at its castle and the Wallace Monument. The journey north through the Highlands takes you past the haunting valley of Glencoe, up Ben Nevis\'s lower slopes, and along the Great Glen to Loch Ness. A ferry crossing from Ullapool lands you on the Isle of Lewis — the edge of Europe — where Callanish Standing Stones predate Stonehenge and Harris\'s beaches rival the Caribbean. The return south via Eilean Donan Castle and Inverness completes a loop through the soul of Scotland. Late May to early June is perhaps the finest time to visit: long daylight hours, wildflowers, and the first flush of green on every hillside. Budget-friendly throughout — hostels, self-catering, and Scotland\'s brilliant free-to-roam outdoor culture make this very achievable under $1,000.',
  duration: '16 days',
  dates: 'May 25 – June 9, 2026',
  budget: 'Under $1,000',
  pace: 'Active',
  bestFor: 'Solo adventurers, History lovers, Hikers, Budget travelers',
  highlights: [
    'Edinburgh Castle & the Royal Mile',
    'Sunrise on Arthur\'s Seat',
    'Stirling Castle & the Wallace Monument',
    'Glencoe — Scotland\'s most dramatic glen',
    'Glenfinnan Viaduct & the Jacobite Steam Train',
    'Eilean Donan Castle',
    'Ferry to the Isle of Lewis',
    'Callanish Standing Stones at dusk',
    'Luskentyre Beach on Harris — Scotland\'s finest',
    'Loch Ness & Urquhart Castle',
    'Culloden Battlefield',
    'Pitlochry & the Highlands homeward',
  ],

  essentials: [
    { title: '🚌 Getting Around', text: 'Scotland\'s budget secret: Citylink coaches and ScotRail trains connect Edinburgh, Stirling, Inverness, and Fort William cheaply. For the Highlands and Isle of Lewis, rent a car (from ~£25/day) or use the Haggis Adventures / Rabbie\'s budget tour hop-ons. Ferry to Stornoway (Isle of Lewis) departs Ullapool — CalMac £30-40 return. Book ahead for summer dates.' },
    { title: '💵 Money', text: 'GBP (£). Budget roughly £40-55/day: hostel dorm £20-30/night, meals £8-15, transport varies. Scotland\'s Right to Roam law means hiking, wild camping, and most nature is FREE. Many museums (National Museum of Scotland, National Galleries) are also free. ATMs everywhere.' },
    { title: '🌦️ Weather in Late May / June', text: 'Scotland\'s finest season — long daylight (sunset around 10pm in late May!), wildflowers, and lush green glens. Expect 12-18°C (54-64°F), some rain showers, and the occasional perfect sunny day. Layer up — waterproof jacket is essential. The famous midges appear by June in the Highlands; bring repellent.' },
    { title: '🥾 What to Pack', text: 'Waterproof jacket (non-negotiable), good walking boots, layers, midges repellent (DEET-based), portable charger, and a reusable water bottle (tap water is excellent). A lightweight daypack for hikes. HiViz for remote hikes is sensible.' },
    { title: '🏕️ Right to Roam', text: 'Scotland has the world\'s most generous public access rights — you can hike, camp, and walk almost anywhere (within the Land Reform Act guidelines). Wild camping is legal and stunning. Bring a tent for the Highlands to slash accommodation costs to near zero.' },
    { title: '🔒 Safety', text: 'Scotland is very safe for solo travelers. The Highlands can have rapidly changing weather — always check forecasts (mwis.org.uk for mountain weather) and tell someone your plans before remote hikes. The Mountain Rescue services are excellent but prevention is better. Mobile signal is patchy in the Outer Hebrides.' },
  ],

  days: [
    // DAY 1 — Arrival in Edinburgh
    {
      num: 1,
      date: '2026-05-25',
      title: 'Arrival in Edinburgh: Old Town First Impressions',
      description: 'Arrive in Edinburgh and orient yourself in one of Europe\'s most dramatic cities. Settle in, stroll the Royal Mile as evening light hits the Castle, and soak in the medieval atmosphere of the Old Town.',
      neighborhoods: 'Old Town · Grassmarket · Cowgate',
      timeBlocks: [
        {
          label: 'Arrival & Afternoon',
          activities: [
            {
              title: 'Check In & First Walk: Royal Mile',
              description: 'Drop your bags at your hostel (Grassmarket or Old Town area is ideal) and head straight to the Royal Mile — the spine of Edinburgh\'s Old Town, running from Edinburgh Castle down to the Palace of Holyroodhouse. Walk from top to bottom, duck into the narrow closes (alleyways) branching off each side — Advocates Close has the best city view, Mary King\'s Close is a buried medieval street beneath your feet.',
              details: ['📍 Royal Mile, Edinburgh Old Town', '🕐 Walk takes 1-2 hours leisurely', '💡 Warm Feelings hostel in Grassmarket or St Christophers Inn are well-placed budget options (~£20-28/night)']
            },
            {
              title: 'Grassmarket & Victoria Street',
              description: 'Head down to the Grassmarket — a lively square below the Castle Rock that was once Edinburgh\'s public execution site and cattle market. Grab a pint at one of the pubs. Then climb Victoria Street, the curved cobblestone lane said to have inspired Diagon Alley in Harry Potter, lined with colourful shops.',
              details: ['📍 Grassmarket, Edinburgh EH1', '💡 The Last Drop pub in Grassmarket is a fun historic stop — named in dark Edinburgh humor for the gallows that once stood here.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mums Great Comfort Food',
              description: 'Edinburgh\'s beloved comfort food institution. Classic Scottish and British dishes with a twist — haggis, neeps and tatties; hearty pies; massive breakfasts. Affordable, filling, and genuinely delicious. Solo-diner-friendly with counter seating.',
              meta: '📍 4A Forrest Rd, Edinburgh · 💰 £8-14 · 🕐 Open until 10pm'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pick up a Lothian Buses day ticket (£4.50) — it covers all city buses including airport. Much cheaper than taxis.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Edinburgh Castle Ramparts at Dusk (Exterior)',
              description: 'Even from outside, Edinburgh Castle sitting atop its volcanic plug is extraordinary. In late May the sun sets around 9:30pm — the castle glows gold in the evening light. Walk up the esplanade for the view, then head to the Outlook Tower / Camera Obscura area for views over the city rooftops.',
              details: ['📍 Castle Esplanade, Castlehill, Edinburgh', '💡 The castle is expensive inside (£20+) — save that for Day 2. Tonight just take in the exterior drama.']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 Late May in Edinburgh means incredible long evenings — golden light until 10pm. Use this for walks and views, not sitting indoors.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9500, lng: -3.1890, label: 'Royal Mile', num: 1, cat: 'attraction', desc: 'Medieval spine of Edinburgh Old Town' },
        { lat: 55.9472, lng: -3.1947, label: 'Grassmarket', num: 2, cat: 'neighborhood', desc: 'Historic market square below Castle Rock' },
        { lat: 55.9481, lng: -3.1923, label: 'Victoria Street', num: 3, cat: 'attraction', desc: 'Curved cobblestone lane — said to inspire Diagon Alley' },
        { lat: 55.9474, lng: -3.1912, label: 'Mums Great Comfort Food', num: 4, cat: 'restaurant', desc: 'Beloved Edinburgh comfort food' },
        { lat: 55.9486, lng: -3.2001, label: 'Edinburgh Castle', num: 5, cat: 'attraction', desc: 'Volcanic rock fortress dominating the Old Town skyline' }
      ]
    },

    // DAY 2 — Edinburgh Castle, Old Town Depth
    {
      num: 2,
      date: '2026-05-26',
      title: 'Edinburgh Castle, Closes & the National Museum',
      description: 'Spend the morning inside Edinburgh Castle exploring the Scottish Crown Jewels and Mons Meg cannon, then dive deep into the medieval Old Town\'s hidden closes and the free National Museum of Scotland.',
      neighborhoods: 'Old Town · South Bridge · Chambers Street',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Edinburgh Castle',
              description: 'Scotland\'s most visited attraction and worth every penny. The volcanic rock has been fortified since the Iron Age. Don\'t miss the Scottish Crown Jewels (Honours of Scotland — older than the English Crown Jewels), the Stone of Destiny (returned from Westminster in 1996), the Great Hall, and the One O\'Clock Gun fired daily. The views from the battlements over the city and to the Firth of Forth are spectacular.',
              details: ['📍 Castlehill, Edinburgh EH1 2NG', '🕐 9:30am-6pm · £20 adults (book online for slight discount)', '💡 Book online and arrive at opening. Audio guide included — use it. Spend 2-2.5 hours inside.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'The Elephant House',
              description: 'The "birthplace of Harry Potter" — J.K. Rowling famously wrote early chapters of Harry Potter here, looking out at Edinburgh Castle and Greyfriars Kirkyard. Great coffee, cakes, and Scottish breakfasts. Now a pilgrimage site with notes and messages covering the bathroom walls.',
              meta: '📍 21 George IV Bridge, Edinburgh · 💰 £5-10 · 🕐 Opens 8am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After the castle, walk next door to the Scotch Whisky Experience for a free amber dram tasting if you sign up for their introductory tour (£18 but includes whisky).' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Old Town Closes & Greyfriars Kirkyard',
              description: 'Spend an hour exploring the closes — narrow medieval alleyways running off the Royal Mile. Try Advocates Close (55.9509,-3.1909) for the postcard Edinburgh view, Riddle\'s Court for a hidden courtyard, and White Horse Close at the Canongate for a step back in time. Then visit Greyfriars Kirkyard — Edinburgh\'s most atmospheric graveyard, where Greyfriars Bobby\'s statue stands guard and the Covenanters\' Prison still gives historians chills.',
              details: ['📍 Royal Mile closes, Edinburgh Old Town', '💡 Greyfriars Kirkyard is free and genuinely atmospheric. Many Harry Potter character names were taken from the gravestones here.']
            },
            {
              title: 'National Museum of Scotland',
              description: 'One of Britain\'s best museums and completely FREE. The Grand Gallery is a stunning Victorian atrium. Highlights: Dolly the Sheep (first cloned mammal, stuffed), Lewis Chessmen, Jacobite artefacts, Scotland\'s natural history, and the Kerr\'s Miniatures collection. Could spend a full day here — allow at least 2 hours.',
              details: ['📍 Chambers Street, Edinburgh EH1 1JF', '🕐 10am-5pm daily · FREE', '💡 The rooftop terrace restaurant has excellent views over the Old Town. Grab coffee up top.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Hendersons',
              description: 'Edinburgh\'s oldest vegetarian restaurant, a local institution since 1962. Excellent value salad bar, hot dishes, and Scottish soups. Huge portions, friendly vibe, great for a budget solo lunch. The haggis samosas are surprisingly good.',
              meta: '📍 94 Hanover Street, Edinburgh · 💰 £7-12 · ⭐ Edinburgh institution'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Real Mary King\'s Close (Optional)',
              description: 'An underground tour of the real buried medieval street beneath the Royal Mile — preserved since the 17th century. Fascinating and slightly spooky — ghost stories and real history in equal measure. Book in advance.',
              details: ['📍 2 Warriston\'s Close, Royal Mile, Edinburgh', '🕐 Tours hourly · £19.50', '💡 Highly recommended for history fans. Book at least a day ahead online.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mosque Kitchen',
              description: 'Edinburgh\'s legendary budget institution. Enormous portions of curry, rice, and naan for £6-8. An Edinburgh student staple that draws everyone from backpackers to professors. Cash only, outdoor benches.',
              meta: '📍 31 Nicolson Square, Edinburgh · 💰 £6-8 · 🕐 Open until 11pm · CASH ONLY'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Mosque Kitchen is one of Edinburgh\'s great secrets — £7 gets you a huge, delicious curry that\'ll fill you up for the evening.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9486, lng: -3.2001, label: 'Edinburgh Castle', num: 1, cat: 'attraction', desc: 'Crown Jewels, Stone of Destiny, One O\'Clock Gun' },
        { lat: 55.9477, lng: -3.1920, label: 'The Elephant House', num: 2, cat: 'restaurant', desc: 'Birthplace of Harry Potter — great breakfast & coffee' },
        { lat: 55.9469, lng: -3.1915, label: 'Greyfriars Kirkyard', num: 3, cat: 'attraction', desc: 'Atmospheric old graveyard — Greyfriars Bobby, Covenanters\' Prison' },
        { lat: 55.9474, lng: -3.1907, label: 'National Museum of Scotland', num: 4, cat: 'attraction', desc: 'World-class free museum — Dolly, Lewis Chessmen, Jacobite artefacts' },
        { lat: 55.9490, lng: -3.1888, label: 'Real Mary King\'s Close', num: 5, cat: 'attraction', desc: 'Buried medieval street beneath the Royal Mile' },
        { lat: 55.9460, lng: -3.1885, label: 'Mosque Kitchen', num: 6, cat: 'restaurant', desc: 'Edinburgh\'s best budget curry — £6-8 for massive portions' }
      ]
    },

    // DAY 3 — Arthur's Seat & New Town
    {
      num: 3,
      date: '2026-05-27',
      title: 'Arthur\'s Seat at Dawn & Edinburgh New Town',
      description: 'Climb Arthur\'s Seat for a sunrise view over the city, then cross to Edinburgh\'s Georgian New Town for the Scottish National Gallery and Stockbridge village charm.',
      neighborhoods: 'Holyrood · Southside · New Town · Stockbridge',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Sunrise on Arthur\'s Seat',
              description: 'The ancient volcanic peak rising 251m above Holyrood Park is the finest viewpoint in Edinburgh — and arguably one of the best urban hikes in the world. Set your alarm for 5am. The summit route via Salisbury Crags and the Radical Road (or the gentler Dunsapie Loch path) takes 45-60 minutes. At the top: Edinburgh, the Firth of Forth, the Pentland Hills, and in clear weather, the Highlands — all glowing in the early light. You\'ll likely have it almost to yourself before 7am.',
              details: ['📍 Holyrood Park, Queen\'s Drive, Edinburgh', '🕐 Aim for summit by 5:30-6am in late May — sunrise is before 5am!', '💡 FREE. Take the path from Holyrood Palace car park. Bring a jacket — it\'s cold at the top even in May. The view is life-changing.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Breakfast back in the city post-hike',
              description: 'Descend by 7:30am and head to the Southside or Grassmarket for breakfast. Urban Angel on Hanover Street serves excellent full Scottish breakfasts from 8am. Or grab pastries from a local bakery.',
              meta: '📍 Various · 💰 £5-10'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Late May sunrise in Edinburgh is before 5am. You can climb Arthur\'s Seat and be back in time for a normal breakfast — the ultimate morning plan.' }
          ]
        },
        {
          label: 'Mid-Morning',
          activities: [
            {
              title: 'Palace of Holyroodhouse (Optional)',
              description: 'The official Scottish residence of the King, at the base of Arthur\'s Seat. Mary Queen of Scots lived here; her secretary Rizzio was murdered here. The State Apartments and Queen\'s Gallery are fascinating for history lovers. Skip if budget is tight.',
              details: ['📍 Canongate, Edinburgh EH8 8DX', '🕐 9:30am-6pm · £18.50', '💡 The ruins of Holyrood Abbey in the grounds are free to view from outside.']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Scottish National Gallery',
              description: 'Edinburgh\'s finest art museum, sitting in its Greek Revival building on the Mound between Old and New Town. FREE. Highlights: Botticelli\'s Virgin Adoring the Sleeping Christ Child, Velázquez, Rembrandt, Titian, and an excellent Scottish collection including the Raeburn portraits. The Impressionist room has Monet, Gauguin, and Van Gogh.',
              details: ['📍 The Mound, Edinburgh EH2 2EL', '🕐 10am-5pm · FREE', '💡 Don\'t skip the lower floor Scottish collection — Ramsay, Raeburn, and McTaggart tell Scottish history through portraiture.']
            },
            {
              title: 'Stockbridge Village Stroll',
              description: 'Walk down from New Town to Stockbridge — Edinburgh\'s most charming village-in-a-city. Independent bookshops, delis, coffee shops, and the Sunday Farmers Market (skip if a weekday). The Water of Leith Walkway follows the river through Stockbridge to the Gallery of Modern Art.',
              details: ['📍 Stockbridge, Edinburgh', '💡 The Royal Botanic Garden is free and a 10-min walk from Stockbridge — beautiful in late May with the rhodododendrons still in bloom.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Scran & Scallie',
              description: 'Tom Kitchin\'s Stockbridge gastropub — a more affordable cousin of his Michelin-starred restaurant. Scottish ingredients prepared with real skill: venison burger, cullen skink (smoked haddock soup), fish and chips made properly. Great spot for a leisurely solo lunch.',
              meta: '📍 1 Comely Bank Road, Stockbridge · 💰 £12-18 · ⭐ Tom Kitchin group'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Princes Street Gardens & Calton Hill Sunset',
              description: 'Take a late-evening walk through Princes Street Gardens (free, lovely in May) with the castle above, then climb Calton Hill for the 360° panorama at sunset. The collection of monuments — National Monument (Scotland\'s "Disgrace"), Nelson Monument, Old Observatory — makes for a dramatic skyline. This is the classic Edinburgh photo spot.',
              details: ['📍 Calton Hill, Edinburgh', '🕐 Open 24 hours · FREE', '💡 Sunset is around 9:30pm in late May. Pack a beer from a corner shop and watch it from the hill.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Howies Edinburgh',
              description: 'Honest Scottish cooking at fair prices. Haggis in filo pastry, Aberdeen Angus steak, Scottish salmon. Set menus offer the best value — 2 courses for around £17-20. A step up from pub grub without breaking the budget.',
              meta: '📍 10-14 Victoria Street, Edinburgh · 💰 £15-22 · 🕐 Open until 10pm'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you can do only one Edinburgh evening activity, Calton Hill at sunset is it.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9441, lng: -3.1615, label: 'Arthur\'s Seat Summit', num: 1, cat: 'attraction', desc: '251m volcanic peak — best view in Edinburgh, completely free' },
        { lat: 55.9524, lng: -3.1724, label: 'Palace of Holyroodhouse', num: 2, cat: 'attraction', desc: 'King\'s official Scottish residence — Mary Queen of Scots lived here' },
        { lat: 55.9500, lng: -3.1960, label: 'Scottish National Gallery', num: 3, cat: 'attraction', desc: 'Free world-class art museum on the Mound' },
        { lat: 55.9567, lng: -3.2068, label: 'Stockbridge', num: 4, cat: 'neighborhood', desc: 'Edinburgh\'s most charming village — independents, delis, Water of Leith' },
        { lat: 55.9564, lng: -3.2080, label: 'The Scran & Scallie', num: 5, cat: 'restaurant', desc: 'Tom Kitchin gastropub — excellent Scottish produce' },
        { lat: 55.9556, lng: -3.1809, label: 'Calton Hill', num: 6, cat: 'attraction', desc: 'Hilltop monuments & best 360° Edinburgh panorama' }
      ]
    },

    // DAY 4 — Leith & Rosslyn Chapel
    {
      num: 4,
      date: '2026-05-28',
      title: 'Leith Waterfront & Rosslyn Chapel',
      description: 'Explore Leith — Edinburgh\'s rejuvenated port district with the Royal Yacht Britannia — then make the afternoon pilgrimage to Rosslyn Chapel, the mysterious medieval masterpiece south of the city.',
      neighborhoods: 'Leith · Roslin · Midlothian',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Leith Waterfront Walk',
              description: 'Take bus 22 or 36 from the city centre to Leith (20 min). Walk along the Shore — Leith\'s rejuvenated waterfront lined with restaurants and converted warehouses. The Water of Leith meets the Firth of Forth here. Leith has gone from Edinburgh\'s gritty industrial port to its most exciting food and arts district.',
              details: ['📍 The Shore, Leith, Edinburgh', '💡 The Shore has excellent independent coffee shops. Try Artisan Roast or Fortitude Coffee on the way.']
            },
            {
              title: 'Royal Yacht Britannia',
              description: 'The Queen\'s former floating palace, now permanently moored at Leith. Five decks of royal history — State Apartments, the Sun Lounge where royals relaxed, engine room, crew quarters. Audio guide tells the stories of 254 official visits and the Queen\'s honeymoon. Fascinating even for non-royalists.',
              details: ['📍 Ocean Terminal, Leith, Edinburgh EH6 6JJ', '🕐 9:30am-6pm (last entry 4:30pm) · £18', '💡 Allow 2 hours. The contrast between the opulent State Rooms and the spartan sailors\' quarters is striking.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast / Brunch',
              name: 'The Kitchin (Bar Lunch) or Shore Bars',
              description: 'The Shore area in Leith has excellent cafes and brunch spots. Bross Bagels on Constitution Street does exceptional Montreal-style bagels. Or grab a flat white and pastry at one of the waterfront cafes.',
              meta: '📍 The Shore, Leith · 💰 £5-10'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rosslyn Chapel',
              description: 'Take the X62 Lothian Bus from Princes Street south to Roslin village (45 min, £2.80). Rosslyn Chapel (1446) is the most ornately carved church in Scotland — every surface covered in stone carvings of biblical scenes, plants, animals, and the famous Apprentice Pillar. Made famous globally by The Da Vinci Code (filmed here), but long revered by Freemasons, Templars enthusiasts, and architectural historians. The carvings allegedly include depictions of corn and aloe vera — centuries before Columbus reached America.',
              details: ['📍 Chapel Loan, Roslin, Midlothian EH25 9PU', '🕐 9:30am-5pm Mon-Sat, 12pm-4:45pm Sun · £10', '💡 Budget 1.5 hours minimum. Guided tours run regularly and are worth attending. The graveyard outside has incredible carved stones.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Original Rosslyn Inn',
              description: 'The pub right next to Rosslyn Chapel, serving traditional Scottish pub food. Soup and a roll, fish and chips, steak pie. Unpretentious, warm, and exactly right after the chapel visit.',
              meta: '📍 4 Main Street, Roslin · 💰 £8-14'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After Rosslyn Chapel, walk down to Roslin Glen — a beautiful wooded gorge following the North Esk river, with Roslin Castle ruins above. Free and stunning.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Edinburgh Evening — Pub Crawl the Grassmarket',
              description: 'Return to Edinburgh for your last city evening. The Grassmarket has a cluster of excellent pubs: The Last Drop, The White Hart Inn (Edinburgh\'s oldest pub, 1516), and The Bow Bar on Victoria Street — a brilliant real ale pub with no music, no TV, just excellent Scottish cask ales.',
              details: ['📍 Grassmarket & Victoria Street, Edinburgh', '💡 The Bow Bar has an incredible whisky selection. Ask the bartender to recommend a Highlands dram in preparation for your journey north.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Outsider',
              description: 'A local favourite on George IV Bridge with views of the castle. Modern Scottish cooking with global influences — chargrilled meats, seasonal vegetables, great cocktails. Affordable pre-theatre set menu available. Popular, so book ahead.',
              meta: '📍 15-16 George IV Bridge, Edinburgh · 💰 £15-22 · 🕐 Open until 11pm'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Pack tonight for tomorrow\'s early departure to Stirling and the Highlands. Exciting days ahead.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9756, lng: -3.1718, label: 'Leith Shore', num: 1, cat: 'neighborhood', desc: 'Rejuvenated port district — best food & coffee scene outside Old Town' },
        { lat: 55.9780, lng: -3.1780, label: 'Royal Yacht Britannia', num: 2, cat: 'attraction', desc: 'Queen\'s former floating palace — 5 decks of royal history' },
        { lat: 55.8560, lng: -3.1598, label: 'Rosslyn Chapel', num: 3, cat: 'attraction', desc: 'Intricately carved 15th-century chapel — Da Vinci Code fame, genuine mystery' },
        { lat: 55.8562, lng: -3.1605, label: 'Original Rosslyn Inn', num: 4, cat: 'restaurant', desc: 'Traditional pub next to the chapel' },
        { lat: 55.9472, lng: -3.1947, label: 'Grassmarket Pubs', num: 5, cat: 'attraction', desc: 'The Bow Bar, White Hart Inn, The Last Drop — Edinburgh pub heritage' }
      ]
    },

    // DAY 5 — Stirling
    {
      num: 5,
      date: '2026-05-29',
      title: 'Stirling: The Heart of Scotland\'s Independence Story',
      description: 'Take the train to Stirling — Scotland\'s most historically significant city. Stirling Castle, the Wallace Monument, and Bannockburn battlefield tell the story of Scotland\'s fight for independence in one extraordinary day.',
      neighborhoods: 'Stirling Old Town · Causewayhead · Bannockburn',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Stirling Castle',
              description: 'Scotland\'s most important castle — arguably more significant than Edinburgh Castle historically. This is where Mary Queen of Scots was crowned aged nine months, where James VI grew up, and where Scotland\'s medieval monarchs held court. The Great Hall (1503) and the Royal Palace with its extraordinary Stirling Heads roundels are masterpieces of Renaissance architecture in Scotland. The view from the battlements over the Forth valley and to Ben Lomond is extraordinary.',
              details: ['📍 Castle Wynd, Stirling FK8 1EJ', '🕐 9:30am-6pm · £17 (book online)', '💡 Arrive at opening. Spend 2 hours minimum. The Stirling Heads replicas in the Royal Palace are stunning — carved oak portrait medallions of Renaissance figures.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Grab breakfast in Edinburgh before 8am train, or Stirling cafes',
              description: 'TrainLine: Edinburgh to Stirling is 50 minutes, £7-12. Aim to arrive at the castle by 9:30am opening. Grab coffee and a pastry at Stirling station or along Stirling\'s upper town.',
              meta: '📍 Stirling train station 10 min walk to castle · 💰 £7-12 train'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Historic Environment Scotland Explorer Pass (from £43 for 3 days) covers both Stirling Castle and Edinburgh Castle — good value if you haven\'t already paid for Edinburgh Castle.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Old Town Stirling & Church of the Holy Rude',
              description: 'Walk down the cobblestone streets of Stirling\'s Old Town — Mar\'s Wark (a ruined Renaissance palace), Argyll\'s Lodging (Scotland\'s most complete Renaissance townhouse), and the Church of the Holy Rude where the infant James VI was crowned in 1567. The Old Town graveyard has incredible carved stones and a view of the castle.',
              details: ['📍 Castle Wynd / St John Street, Stirling', '🕐 Church of the Holy Rude: free to enter · Open daily', '💡 This whole area is free — wander slowly and read the history plaques.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nicky Tams Bar & Bothy',
              description: 'A proper Stirling pub — named after the old Scottish boots tied with straps (tams). Real ales, excellent haggis pakoras, and hearty soup with crusty bread. The kind of pub the locals love and tourists miss.',
              meta: '📍 29 Baker Street, Stirling · 💰 £8-13 · 🕐 Open from 11am'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'National Wallace Monument',
              description: 'A 15-minute bus ride from Stirling centre brings you to the 67m Victorian tower built to honour William Wallace — the hero of Braveheart, and Scotland\'s most iconic freedom fighter. Climb 246 steps to the crown-shaped top for staggering views over the Forth valley, the castle, and beyond. Inside: Wallace\'s actual two-handed broadsword (enormous), and displays on the 1297 Battle of Stirling Bridge.',
              details: ['📍 Abbey Craig, Hillfoots Road, Stirling FK9 5LF', '🕐 10am-5pm · £12.50 (shuttle bus from visitor centre)', '💡 The view from the top on a clear day stretches to Edinburgh and the Highlands — remarkable.']
            },
            {
              title: 'Bannockburn Battlefield',
              description: 'A short bus ride south brings you to Bannockburn — where in June 1314, Robert the Bruce\'s outnumbered Scottish army defeated Edward II\'s English force in the decisive battle of the Wars of Independence. The Bannockburn Visitor Centre has an excellent immersive 3D battle experience.',
              details: ['📍 Glasgow Road, Stirling FK7 0LJ', '🕐 10am-5:30pm · £12 (NTS members free)', '💡 The bronze equestrian statue of Robert the Bruce is free to view — striking at any time of day.']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 You can see both Wallace Monument and Bannockburn in an afternoon if you plan the buses well. Or skip Bannockburn if you want more time at the castle — it\'s the highlight.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Edinburgh or Press On to Fort William',
              description: 'Decision point: return to Edinburgh to collect your bag and then take the 5pm+ bus/train toward Fort William (overnight hostel stop en route to Glencoe), or if you\'re already packed, go direct from Stirling. Citylink coach from Stirling to Fort William is 2.5 hours.',
              details: ['📍 Stirling Bus Station', '💡 Check Citylink.co.uk for timetables. Evening coaches to Fort William are limited — plan ahead.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pub dinner in Stirling before onward journey, or hostel meal in Fort William',
              description: '',
              meta: '💰 £8-15'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 56.1241, lng: -3.9470, label: 'Stirling Castle', num: 1, cat: 'attraction', desc: 'Scotland\'s most historically significant castle — Mary QoS, James VI' },
        { lat: 56.1213, lng: -3.9380, label: 'Church of the Holy Rude', num: 2, cat: 'attraction', desc: 'Medieval church where James VI was crowned in 1567' },
        { lat: 56.1235, lng: -3.9340, label: 'Nicky Tams Bar', num: 3, cat: 'restaurant', desc: 'Stirling local pub — haggis pakoras, real ales' },
        { lat: 56.1444, lng: -3.9184, label: 'National Wallace Monument', num: 4, cat: 'attraction', desc: '67m Victorian tower — Wallace\'s broadsword, stunning Forth valley views' },
        { lat: 56.0971, lng: -3.9334, label: 'Bannockburn Battlefield', num: 5, cat: 'attraction', desc: '1314 battle that secured Scottish independence — immersive visitor centre' }
      ]
    },

    // DAY 6 — Glencoe
    {
      num: 6,
      date: '2026-05-30',
      title: 'Glencoe: Scotland\'s Most Dramatic Glen',
      description: 'Drive or bus through Glencoe — the most hauntingly beautiful valley in Scotland. Hike the Lost Valley, visit the Glencoe Folk Museum, and soak in the scale of the Three Sisters.',
      neighborhoods: 'Glencoe Village · Glen Coe · Loch Achtriochtan',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive or Bus into Glencoe',
              description: 'From Fort William (45 min south), the A82 enters Glencoe — Scotland\'s most dramatic glen. Sheer quartzite ridges rise 900m from the valley floor. The Three Sisters — Beinn Fhada, Gearr Aonach, and Aonach Dubh — form a cathedral of rock. The valley carries the shadow of the 1692 Glencoe Massacre, when Campbells killed MacDonalds in their sleep. Stop at the Glencoe Visitor Centre first.',
              details: ['📍 Glencoe Visitor Centre, Ballachulish, PH49 4LA', '🕐 Visitor Centre 9am-5pm · Free access to glen 24/7', '💡 Citylink coaches from Glasgow and Fort William stop at Glencoe Visitor Centre. The glen itself is always free to enter.']
            },
            {
              title: 'The Lost Valley (Coire Gabhail) Hike',
              description: 'The finest half-day hike in Glencoe. A steep, dramatic path climbs between two of the Three Sisters into a hidden flat valley invisible from the glen below. This is where the MacDonalds hid their cattle before the massacre. The scrambling approach through the gorge is thrilling, and the valley is a revelation — completely hidden and utterly wild.',
              details: ['📍 Trailhead at Allt Lairig Eilde car park, A82, Glencoe', '⏱️ 4-5 hours round trip · 400m elevation gain · Moderate-challenging', '💡 Bring proper footwear and waterproofs. The gorge crossing is slippery after rain. Absolutely worth every step.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Hostel or Fort William cafe before departure',
              description: 'Stock up on sandwiches, snacks, and water in Fort William before heading to Glencoe — there are few food options in the glen itself.',
              meta: '📍 Fort William town centre · 💰 £5-8'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The light in Glencoe is theatrical — low cloud, patches of sunlight, and long shadows make every photo look cinematic. Embrace the drama even on a grey day.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Glencoe Village & Folk Museum',
              description: 'The small village of Glencoe sits at the western end of the glen where it meets Loch Leven. The Glencoe Folk Museum in thatched cottages tells the story of Highland life and the massacre with personal artefacts. The walk along Loch Leven\'s shore from the village is beautiful and gentle.',
              details: ['📍 Glencoe Village, PH49 4HS', '🕐 Folk Museum: 10am-4:30pm Tue-Sat · £4', '💡 The views back up the glen from Loch Leven shore at the village are spectacular.']
            },
            {
              title: 'Loch Achtriochtan & Signal Rock',
              description: 'The small loch in the floor of Glencoe perfectly reflects the Three Sisters. Signal Rock — the flat topped knoll where the Campbells allegedly lit the signal to begin the massacre — is a short easy walk from the car park near the Study (viewpoint).',
              details: ['📍 Loch Achtriochtan, Glencoe (along the A82)', '💡 Stop at "The Study" viewpoint on the A82 for the classic Glencoe panorama photograph.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Glencoe Café',
              description: 'The Glencoe Café in the village is the main food stop — excellent homemade soup, sandwiches, and scones. Post-hike calories sorted.',
              meta: '📍 Glencoe Village · 💰 £6-10'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Onward to Fort William for the Night',
              description: 'Return to Fort William for the night. Ben Nevis Inn at the foot of Ben Nevis does excellent hearty food and has a great atmosphere for walkers and climbers. Fort William\'s High Street has the usual chip shops and pubs for a budget dinner.',
              details: ['📍 Fort William, PH33', '💡 Fort William Backpackers hostel is friendly and central — £20-25/night.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ben Nevis Bar & Restaurant',
              description: 'Lively Fort William pub popular with climbers, walkers, and outdoor types. Good Scottish pub food — steak pie, fish supper, venison burger. Great atmosphere.',
              meta: '📍 103 High Street, Fort William · 💰 £10-16'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Tomorrow you\'ll want an early start for the Glenfinnan Viaduct and the drive north — a big, exciting day.' }
          ]
        }
      ],
      mapPins: [
        { lat: 56.6786, lng: -5.1034, label: 'Glencoe Visitor Centre', num: 1, cat: 'attraction', desc: 'NTS centre — start here for maps and trail info' },
        { lat: 56.6638, lng: -5.0270, label: 'Lost Valley Trailhead', num: 2, cat: 'attraction', desc: 'Hidden valley hike — 4-5 hours, Glencoe\'s finest walk' },
        { lat: 56.6720, lng: -5.0980, label: 'Glencoe Village', num: 3, cat: 'neighborhood', desc: 'Small village at the foot of the glen — Folk Museum, cafes' },
        { lat: 56.6690, lng: -5.0580, label: 'Loch Achtriochtan', num: 4, cat: 'attraction', desc: 'Mirror-flat loch reflecting the Three Sisters' },
        { lat: 56.8198, lng: -5.1053, label: 'Fort William', num: 5, cat: 'neighborhood', desc: 'Gateway to Ben Nevis — hostels, pubs, supplies' }
      ]
    },

    // DAY 7 — Glenfinnan & Journey North
    {
      num: 7,
      date: '2026-05-31',
      title: 'Glenfinnan Viaduct & the Road to Eilean Donan',
      description: 'An iconic Highland day: the Glenfinnan Viaduct (and maybe the Jacobite Steam Train), Eilean Donan Castle reflecting in the loch, and an evening arrival near Ullapool.',
      neighborhoods: 'Glenfinnan · Loch Eil · Kyle of Lochalsh · Loch Duich',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Glenfinnan Viaduct & Monument',
              description: 'Head west from Fort William 25 minutes to Glenfinnan at the head of Loch Shiel. The Glenfinnan Viaduct — 21 arches of curved stone bridge over the valley — is one of Scotland\'s most photographed spots, made famous as the bridge Harry Potter\'s train crosses in the films. The viewpoint above gives the perfect angle. Below, the Glenfinnan Monument marks where Bonnie Prince Charlie raised his standard in 1745 to begin the Jacobite Rising.',
              details: ['📍 Glenfinnan, Inverness-shire PH37 4LT', '🕐 Monument/NTS Visitor Centre: 9am-5pm · Monument free · NTS parking £3', '💡 The Jacobite Steam Train (The Hogwarts Express) crosses the viaduct at 10:43am heading west. Time your viaduct viewpoint visit for just before this for the photo of photos. Book train tickets at steam-train.co.uk if you want to ride it — £40+ but magical.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Grab breakfast before leaving Fort William',
              description: '',
              meta: '📍 Fort William · 💰 £5-8'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The viaduct viewpoint hike takes 20-30 minutes up. Get there by 10:15am for the steam train crossing at 10:43am westbound.' }
          ]
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Eilean Donan Castle',
              description: 'Drive northwest along the A87 to Eilean Donan — Scotland\'s most photographed castle, sitting on a tiny island where three sea lochs meet, connected to the mainland by an arched stone bridge. Built in the 13th century, blown up by the English in 1719 during the Jacobite Rising, and romantically restored between 1919-1932. The interior has Jacobite artefacts, Spanish cannon, and clan history.',
              details: ['📍 Dornie, Kyle of Lochalsh IV40 8DX', '🕐 9am-6pm · £15', '💡 The famous photo is from the roadside viewing area — free. Visit inside for the story. Time your arrival for when tour buses have left (after 4pm is quietest).']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Dornie Cafe or Eilean Donan café',
              description: 'The Eilean Donan Castle café does good soups and sandwiches. Alternatively, the small village of Dornie has a couple of spots for a bite.',
              meta: '📍 Dornie, near Eilean Donan · 💰 £7-12'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Drive North to Ullapool',
              description: 'Drive north on the A835 through dramatic Wester Ross scenery to Ullapool — roughly 2 hours from Eilean Donan. Ullapool is the ferry port for Stornoway on the Isle of Lewis. Check in to your hostel — Broomfield Holiday Park or West House are solid budget options. The evening drive through Wester Ross is spectacular: Loch Maree, Beinn Eighe, and the wild northwest coast.',
              details: ['📍 Ullapool, Ross-shire IV26 2XB', '💡 Book your Ullapool accommodation and the CalMac ferry to Stornoway IN ADVANCE. The ferry books up in summer — CalMac.co.uk · Ferry departs 10:00am and 2:30pm daily, ~2.5 hours crossing.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Arch Inn, Ullapool',
              description: 'Ullapool\'s best pub — real ales, excellent fish and chips, and a warm atmosphere. On the waterfront looking out to Loch Broom. A proper Highland pub evening.',
              meta: '📍 10-11 West Shore Street, Ullapool · 💰 £10-16'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Book the Stornoway ferry NOW if you haven\'t already — CalMac summer ferries fill up weeks in advance. calmacc.co.uk' }
          ]
        }
      ],
      mapPins: [
        { lat: 56.8742, lng: -5.4306, label: 'Glenfinnan Viaduct', num: 1, cat: 'attraction', desc: '21-arch curved viaduct — Jacobite steam train crosses at 10:43am' },
        { lat: 56.8726, lng: -5.4400, label: 'Glenfinnan Monument', num: 2, cat: 'attraction', desc: 'Bonnie Prince Charlie\'s 1745 Jacobite Rising launch point' },
        { lat: 57.2742, lng: -5.5161, label: 'Eilean Donan Castle', num: 3, cat: 'attraction', desc: 'Scotland\'s most iconic castle on its island in Loch Duich' },
        { lat: 57.8989, lng: -5.1614, label: 'Ullapool', num: 4, cat: 'neighborhood', desc: 'Ferry port for Isle of Lewis — Highland fishing village' },
        { lat: 57.8974, lng: -5.1625, label: 'The Arch Inn', num: 5, cat: 'restaurant', desc: 'Ullapool\'s finest pub — waterfront, real ales, great fish' }
      ]
    },

    // DAY 8 — Ferry to Isle of Lewis
    {
      num: 8,
      date: '2026-06-01',
      title: 'Ferry Crossing to the Isle of Lewis',
      description: 'Sail the Minch from Ullapool to Stornoway on the Isle of Lewis. Arrive on Scotland\'s most remote and atmospheric island — explore Stornoway and witness the Hebridean light.',
      neighborhoods: 'Ullapool · Stornoway · Lews Castle Grounds',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'CalMac Ferry: Ullapool to Stornoway',
              description: 'Board the MV Loch Seaforth at Ullapool for the 2.5-hour crossing of the Minch — the strait separating mainland Scotland from the Outer Hebrides. On a clear day, the approach to Stornoway with Lewis\'s peat moorlands opening up ahead is unforgettable. Keep an eye out for dolphins, porpoises, and minke whales which are common on this crossing.',
              details: ['📍 Ullapool Ferry Terminal', '🕐 Departures 10:00am and 2:30pm · £17.70 single passenger (no vehicle) or £34 return', '💡 Arrive 45 minutes before departure. The crossing can be rough in bad weather — take seasickness tablets if you\'re sensitive. The café onboard is reasonable.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Early breakfast in Ullapool before ferry',
              description: 'The Ceilidh Place in Ullapool does good breakfasts — or grab supplies at the Co-op for the crossing.',
              meta: '📍 Ullapool · 💰 £5-10'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Stornoway is conservative — the Outer Hebrides observe Sunday traditions more strictly than mainland Scotland. Many shops and attractions close on Sunday. Plan accordingly.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Stornoway & Lews Castle Grounds',
              description: 'Stornoway is a proper working town — the only real town in the Outer Hebrides. Explore the harbour waterfront, visit the Lews Castle Museum (An Lanntair) to understand Hebridean history and see the Lewis Chessmen replica (the originals are split between the British Museum and the National Museum of Scotland). Lews Castle grounds — once a Victorian baronial estate — are now public parkland with great views over the bay.',
              details: ['📍 Lews Castle, Stornoway HS2 0XY', '🕐 Castle Museum: Mon-Sat 10am-5pm · Free', '💡 An Lanntair arts centre on the waterfront has good exhibitions, a great café, and the pulse of local Hebridean culture.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'An Lanntair Café',
              description: 'The café at the An Lanntair arts centre on Stornoway\'s waterfront serves excellent homemade soups, Hebridean seafood, and cakes. Locally sourced and unpretentious.',
              meta: '📍 Kenneth Street, Stornoway · 💰 £7-12'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Stornoway Waterfront Evening',
              description: 'Walk the Stornoway waterfront as the long Hebridean evening light floods the harbour. The fishing boats, the castle across the bay, and the sheer remoteness of this place — furthest-flung capital in Britain — creates a distinctive atmosphere. Buy some smoked salmon or Stornoway Black Pudding from a local deli to take away.',
              details: ['📍 Stornoway Harbour, HS1 2DF', '💡 Stornoway Black Pudding is a Protected Geographic Indication product — the real thing is extraordinary. Pick some up at Charles MacLeod Butchers.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Thai Café Stornoway',
              description: 'This sounds absurd but Stornoway\'s Thai Café is genuinely beloved by locals — delicious, fresh Thai food on the edge of Europe. A quirky and wonderful choice. Alternatively, the Digby Chick does excellent local seafood.',
              meta: '📍 27 Church Street, Stornoway · 💰 £10-15'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 On the Isle of Lewis, in June, it barely gets dark at all. At midnight, the sky is still light. Embrace this extraordinary phenomenon.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.8989, lng: -5.1614, label: 'Ullapool Ferry Terminal', num: 1, cat: 'transport', desc: 'CalMac ferry to Stornoway — 2.5 hour crossing' },
        { lat: 58.2096, lng: -6.3779, label: 'Stornoway Harbour', num: 2, cat: 'neighborhood', desc: 'Capital of the Outer Hebrides — fishing port, castle, arts' },
        { lat: 58.2133, lng: -6.3956, label: 'Lews Castle Museum', num: 3, cat: 'attraction', desc: 'Hebridean history — Lewis Chessmen replicas, local culture' },
        { lat: 58.2073, lng: -6.3769, label: 'An Lanntair Arts Centre', num: 4, cat: 'attraction', desc: 'Hebridean arts, culture, and the best café in Stornoway' },
        { lat: 58.2088, lng: -6.3800, label: 'Thai Café Stornoway', num: 5, cat: 'restaurant', desc: 'Beloved local spot — surprisingly excellent Thai food on the edge of Europe' }
      ]
    },

    // DAY 9 — Callanish Standing Stones & West Lewis
    {
      num: 9,
      date: '2026-06-02',
      title: 'Callanish Standing Stones & the Wild West Coast',
      description: 'The ancient stone circle at Callanish predates Stonehenge and sits in a landscape that feels genuinely otherworldly. Then explore Lewis\'s wild Atlantic coastline and the Carloway Broch.',
      neighborhoods: 'Callanish · Carloway · Gearrannan · Great Bernera',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Callanish Standing Stones at Sunrise',
              description: 'Drive 25km west from Stornoway to Callanish (30 min). The Callanish Stones — 50 standing stones arranged in a cross pattern around a central circle with a burial cairn — were erected around 2900 BC, predating Stonehenge by several centuries. The setting is extraordinary: the stones rise from the peat moorland above Loch Roag, backed by the hills of Harris. Arrive early (before the visitor centre opens at 10am) to have them to yourself in the Hebridean morning light. The experience is genuinely moving.',
              details: ['📍 Calanais, Isle of Lewis HS2 9DY', '🕐 Stones: Free and accessible 24/7 · Visitor Centre: 10am-5:30pm (free)', '💡 These are Scotland\'s finest prehistoric monument and arguably more atmospheric than Stonehenge — on a clear morning with low light and total quiet, they\'re unforgettable.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Callanish Visitor Centre Café',
              description: 'Opens at 10am and serves excellent breakfast and Hebridean soups. Worth waiting for after your early stone circle visit.',
              meta: '📍 Callanish Visitor Centre · 💰 £5-9'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 There are actually three Callanish stone sites (Callanish I, II, and III) in the same area — all free, all fascinating. Callanish I is the main one but the others add context.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Carloway Broch (Dun Carloway)',
              description: 'A perfectly preserved Iron Age broch tower — a 2,000-year-old drystone fortification still standing to 9 metres high. You can walk right up to it and peer inside. Free. The view from the broch over Loch Carloway and the surrounding moorland is spectacular.',
              details: ['📍 Carloway, Isle of Lewis HS2 9AZ', '🕐 Open 24/7 · FREE', '💡 A short, steep path leads up to the broch from the road. 15 minutes from Callanish.']
            },
            {
              title: 'Gearrannan Blackhouse Village',
              description: 'A restored village of traditional Hebridean blackhouses — the long, low thatched stone cottages that were home to Lewis crofters until the 1970s. Set dramatically on the clifftop above the Atlantic. Some are available as holiday lets; others are open as a museum. The setting — old stone buildings against crashing Atlantic waves — is unforgettable.',
              details: ['📍 Gearrannan, Carloway, Lewis HS2 9AL', '🕐 Village always accessible · Museum: April-Sep 9am-5pm · £3.50', '💡 Walk down to the shore below the village for Atlantic views and the smell of the sea.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Picnic supplies from Stornoway',
              description: 'Stock up on supplies the night before from the Co-op or deli in Stornoway — Lewis\'s west coast has few food stops. A picnic among the blackhouses or above Loch Roag is perfect.',
              meta: '📍 Various Stornoway shops · 💰 £5-8'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at the Butt of Lewis (or Beach Walk)',
              description: 'Drive to the Butt of Lewis — the northernmost tip of the Outer Hebrides, where the Atlantic crashes against towering red sandstone cliffs. The lighthouse here marks the true edge of Europe. In June the sunset here (around 10:30pm) with the pinkish Arctic light is extraordinary. Alternatively, find one of Lewis\'s west coast beaches — Dalbeg, Dalmore, or Bhaltos — for a sunset dip if you\'re brave.',
              details: ['📍 Butt of Lewis, Ness, Lewis HS2 0XN', '💡 The cliff walk at the Butt of Lewis is free. Seabirds, seals, and complete wildness.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Back in Stornoway for the evening',
              description: 'Return to Stornoway for dinner. The Digby Chick does excellent local seafood — Hebridean langoustines, scallops, and Lewis crab when available.',
              meta: '📍 5 Bank Street, Stornoway · 💰 £15-22'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Wild swimming on Lewis is exhilarating — the Atlantic is cold but incredibly clear. Dalbeg Beach is sheltered and relatively accessible.' }
          ]
        }
      ],
      mapPins: [
        { lat: 58.1979, lng: -6.7441, label: 'Callanish Standing Stones', num: 1, cat: 'attraction', desc: '5,000-year-old stone circle — predates Stonehenge, free access 24/7' },
        { lat: 58.2832, lng: -6.7892, label: 'Carloway Broch', num: 2, cat: 'attraction', desc: '2,000-year-old Iron Age tower — still standing 9m high, free' },
        { lat: 58.3147, lng: -6.8202, label: 'Gearrannan Blackhouse Village', num: 3, cat: 'attraction', desc: 'Restored Hebridean crofting village on Atlantic clifftop' },
        { lat: 58.5146, lng: -6.2609, label: 'Butt of Lewis', num: 4, cat: 'attraction', desc: 'Northernmost tip of the Outer Hebrides — lighthouse, dramatic cliffs' },
        { lat: 58.2073, lng: -6.3769, label: 'Digby Chick', num: 5, cat: 'restaurant', desc: 'Stornoway seafood — langoustines, scallops, Lewis crab' }
      ]
    },

    // DAY 10 — Harris & the Beaches
    {
      num: 10,
      date: '2026-06-03',
      title: 'Harris: The Most Beautiful Beaches in Britain',
      description: 'Drive south into the Isle of Harris — the southern half of the same island as Lewis — for jaw-dropping white sand beaches that look like the Caribbean (just colder), Harris Tweed, and the dramatic Bays of Harris.',
      neighborhoods: 'Tarbert · Luskentyre · Seilebost · Scarista · Leverburgh',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive South to Tarbert (Harris)',
              description: 'The boundary between Lewis and Harris is one of the most dramatic landscape changes in Britain — you cross from the flat peat moorland of Lewis into the bare Lewisian gneiss mountains of Harris. Tarbert is the "capital" of Harris — a small settlement with a café, post office, and the Harris Tweed shop.',
              details: ['📍 Tarbert, Isle of Harris HS3 3DJ', '🕐 55km from Stornoway, about 1 hour', '💡 Stop at the Golden Road viewpoint en route for the classic Harris mountain-sea panorama.']
            },
            {
              title: 'Luskentyre Beach',
              description: 'Often voted Britain\'s most beautiful beach — and the claim is not exaggerated. Luskentyre is a vast expanse of white shell sand backed by machair grasslands and turquoise shallow water, framed by the mountains of North Harris. In June the sea is an impossible Caribbean blue-green. Walk out as far as the tidal sandbanks allow.',
              details: ['📍 Luskentyre, Isle of Harris HS3 3HL', '🕐 Always open · FREE', '💡 The beach faces west — afternoon and evening light is the most spectacular. There\'s a small car park but the beach itself is completely free and usually uncrowded.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast / Lunch',
              name: 'Harris Distillery Café, Tarbert',
              description: 'The Isle of Harris Distillery (makers of the beautiful Harris Gin) has an excellent café in Tarbert. Great coffee, local produce, and the chance to taste their gin. Stop here on the way to the beaches.',
              meta: '📍 Tarbert, Isle of Harris · 💰 £6-12 · ⭐ Harris Gin distillery'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Luskentyre is stunning in any weather. Rain adds drama. Sun makes it look like Maldives. Wind makes it feel alive. Just go.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Scarista Beach & Seilebost',
              description: 'Continue south along the west coast of Harris. Seilebost beach sits opposite Luskentyre across the tidal estuary — equally beautiful with a different angle. Scarista further south is wilder and usually even emptier — the Old Scarista burial ground at the beach edge adds a poignant edge to the view.',
              details: ['📍 Scarista, Isle of Harris HS3 3HX', '💡 Wild swim at Scarista if you\'re brave — the Atlantic is cold but crystal clear.']
            },
            {
              title: 'Harris Tweed Discovery',
              description: 'Harris Tweed — the protected handwoven fabric made only in the Outer Hebrides — is one of Scotland\'s great craft traditions. Visit a local weaver (several welcome visitors; ask at the Tarbert visitor centre) to see the looms in action. The cloth is woven in domestic outbuildings across the islands.',
              details: ['📍 Various crofts, Harris', '💡 Look for the Orb trademark on any Harris Tweed you buy — it guarantees authenticity. A small piece makes a perfect souvenir.']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 The Bays of Harris on the east side — reached via the "Golden Road" (so called because it cost a fortune to build) — is a completely different landscape: rocky, rugged, dotted with tiny lochs.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Leverburgh & Return Journey Plan',
              description: 'Leverburgh in the south of Harris is the departure point for the CalMac ferry to North Uist (if you wanted to explore further south) or just a contemplative end point before driving back to Stornoway. The Am Bothan bunkhouse in Leverburgh is a great budget sleep option in the south.',
              details: ['📍 Leverburgh, Harris HS5 3UA', '💡 From Leverburgh, return north through the Golden Road (east coast) for the most dramatic drive back to Stornoway — completely different landscape from the morning.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Anchorage, Leverburgh or return to Stornoway',
              description: 'The Anchorage in Leverburgh does excellent fresh seafood. Or take the Golden Road back to Stornoway for a final Hebridean dinner.',
              meta: '📍 Leverburgh, Harris · 💰 £10-18'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 57.9001, lng: -6.8083, label: 'Tarbert, Harris', num: 1, cat: 'neighborhood', desc: 'Harris "capital" — Harris Gin distillery café' },
        { lat: 57.9167, lng: -6.9167, label: 'Luskentyre Beach', num: 2, cat: 'attraction', desc: 'Britain\'s most beautiful beach — white sand, turquoise water, free' },
        { lat: 57.9000, lng: -6.9010, label: 'Seilebost Beach', num: 3, cat: 'attraction', desc: 'Opposite Luskentyre across the tidal estuary' },
        { lat: 57.8500, lng: -7.0000, label: 'Scarista Beach', num: 4, cat: 'attraction', desc: 'Wild Atlantic beach with ancient burial ground' },
        { lat: 57.7744, lng: -7.0214, label: 'Leverburgh', num: 5, cat: 'neighborhood', desc: 'Southern Harris — ferry to North Uist, seafood at The Anchorage' }
      ]
    },

    // DAY 11 — Ferry Back & Inverness
    {
      num: 11,
      date: '2026-06-04',
      title: 'Farewell to Lewis, Drive to Inverness',
      description: 'Take the morning ferry back to Ullapool, then drive south through Wester Ross to Inverness — the capital of the Highlands. Evening arrival in the most northerly city in Britain.',
      neighborhoods: 'Stornoway · Ullapool · Wester Ross · Inverness',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Ferry: Stornoway to Ullapool',
              description: 'Take the 10:00am CalMac ferry back to Ullapool. Enjoy the crossing — you may have seen more wildlife by now (dolphins are common). The approach to Ullapool\'s white buildings against the hillside is beautiful from the sea.',
              details: ['📍 Stornoway Ferry Terminal', '🕐 10:00am departure, arrives Ullapool 12:30pm', '💡 Or take the afternoon ferry if you want one more morning on Lewis — check CalMac timetables.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Ferry café or pre-packed breakfast in Stornoway',
              description: '',
              meta: '💰 £5-8'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Corrieshalloch Gorge (En Route)',
              description: 'Just 20km south of Ullapool, Corrieshalloch Gorge is a dramatic slot canyon where the Falls of Measach plunge 45m into a narrow gorge. A Victorian suspension bridge spans the gorge at eye level with the falls. Free, accessible, and genuinely spectacular for 30 minutes.',
              details: ['📍 Corrieshalloch Gorge, IV23 2PJ (A835, near Braemore)', '🕐 Open 24/7 · FREE (NTS property)', '💡 The suspension bridge sways. The spray reaches you. The views down into the gorge are vertiginous.']
            },
            {
              title: 'Drive to Inverness',
              description: 'Continue south on the A835 then A9 to Inverness — about 1.5 hours from Corrieshalloch Gorge. Pass through the Dingwall area and into the Great Glen. Inverness city centre hostels are affordable — Inverness Student Hotel or Black Isle Bar & Rooms are good options.',
              details: ['📍 Inverness, Highlands IV1', '💡 Inverness is small and very walkable — the castle, old town, and riverside are all compact.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Ceilidh Place, Ullapool (before departing)',
              description: 'Ullapool\'s cultural hub — excellent bookshop, arts space, and café-restaurant. Great soups and sandwiches before the road south.',
              meta: '📍 14 West Argyle Street, Ullapool · 💰 £8-14'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Inverness Old Town & River Walk',
              description: 'Settle in to Inverness with an evening walk along the River Ness — the short, fast river that drains Loch Ness into the Moray Firth. Inverness Castle sits above the river on a red sandstone bluff. The old town has good pubs along Academy Street and Church Street.',
              details: ['📍 River Ness, Inverness', '💡 Inverness is a great base — compact, friendly, and full of Highland character.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Number 27',
              description: 'A Inverness favourite for solid Scottish cooking — steaks, venison, seafood. Fair prices and a comfortable atmosphere. Popular with locals.',
              meta: '📍 27 Castle Street, Inverness · 💰 £13-20'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Tomorrow is Loch Ness and Culloden — two of Scotland\'s most powerful places.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.8989, lng: -5.1614, label: 'Ullapool Ferry Terminal', num: 1, cat: 'transport', desc: 'CalMac arrives 12:30pm from Stornoway' },
        { lat: 57.7342, lng: -5.0717, label: 'Corrieshalloch Gorge', num: 2, cat: 'attraction', desc: 'Dramatic slot canyon — Falls of Measach, Victorian suspension bridge, free' },
        { lat: 57.4778, lng: -4.2247, label: 'Inverness', num: 3, cat: 'neighborhood', desc: 'Capital of the Highlands — riverside, castle, great base' },
        { lat: 57.4801, lng: -4.2249, label: 'Inverness Castle', num: 4, cat: 'attraction', desc: 'Victorian red sandstone castle above the River Ness' },
        { lat: 57.4799, lng: -4.2267, label: 'Number 27', num: 5, cat: 'restaurant', desc: 'Reliable Inverness restaurant — venison, steaks, local seafood' }
      ]
    },

    // DAY 12 — Loch Ness & Culloden
    {
      num: 12,
      date: '2026-06-05',
      title: 'Loch Ness & Culloden Battlefield',
      description: 'The Great Glen\'s jewels: cruise Loch Ness and explore the ruins of Urquhart Castle, then visit Culloden — the haunting moor where Scottish Highland culture was effectively destroyed in 1746.',
      neighborhoods: 'Drumnadrochit · Loch Ness · Culloden Moor',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Loch Ness & Urquhart Castle',
              description: 'Drive or bus 25km southwest from Inverness to Drumnadrochit on the shores of Loch Ness. The loch is 37km long, up to 240m deep, and holds more fresh water than all of England and Wales combined. The monster is probably not real, but the loch is genuinely impressive. Urquhart Castle — ruined on a promontory jutting into the loch — was one of Scotland\'s largest castles. The views up and down the loch from the castle are classic Loch Ness. Grant Tower still stands with its trebuchet.',
              details: ['📍 Urquhart Castle, Drumnadrochit IV63 6XJ', '🕐 9:30am-6pm · £15', '💡 Boat tours of Loch Ness from Drumnadrochit are £15-20 for an hour — worth it for the scale of the loch from water level.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Fiddler\'s Coffee Shop, Drumnadrochit',
              description: 'Cosy local café in Drumnadrochit for breakfast and coffee before the castle.',
              meta: '📍 Drumnadrochit · 💰 £5-9'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The best free Loch Ness view is from the B862 road along the south shore — quieter, higher, and more dramatic than the main A82.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Culloden Battlefield',
              description: 'Return to Inverness and drive 8km east to Culloden Moor — the site of the last pitched battle fought on British soil (April 16, 1746). In 40 minutes, the Duke of Cumberland\'s government forces destroyed Bonnie Prince Charlie\'s Jacobite Highland army. The aftermath was brutal — a deliberate campaign to eradicate Highland culture, the clan system, and the Gaelic way of life. Walking among the clan grave markers on the open moor is genuinely moving. The NTS visitor centre with its immersive 360° battle experience is one of Scotland\'s best.',
              details: ['📍 Culloden, Inverness IV2 5EU', '🕐 9am-5:30pm · £14 (or free if NTS member)', '💡 Allow 2 hours. The battlefield audio guide is excellent — you walk the actual ground where it happened. The clan stones are simple and heartbreaking.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Culloden Visitor Centre Café',
              description: 'Good café at the NTS visitor centre — soups, sandwiches, and cakes. Open during visitor centre hours.',
              meta: '📍 Culloden Visitor Centre · 💰 £7-11'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Inverness Pubs & Whisky',
              description: 'End the emotional day with a Highland malt at one of Inverness\'s excellent whisky pubs. The Hootananny on Church Street has live Highland music most evenings. The Gellions on Bridge Street is Inverness\'s oldest pub (1841). Ask for a recommended Speyside or Highlands single malt.',
              details: ['📍 Church Street / Bridge Street, Inverness', '💡 Hootananny has free live folk and Highland music most evenings — a proper Scottish experience.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Contrast Brasserie',
              description: 'Good quality modern Scottish food in Inverness at reasonable prices. Three-course set menu is good value at around £22. Or grab fish and chips from a chippie for a £6-8 dinner.',
              meta: '📍 Glenmoriston Hotel, Ness Bank, Inverness · 💰 £13-22'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you have a car, the Cairngorms and Speyside whisky trail are to the south and southeast — both worth a morning detour.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.3230, lng: -4.4384, label: 'Urquhart Castle', num: 1, cat: 'attraction', desc: 'Ruined Highland castle on Loch Ness — tower, trebuchet, magnificent views' },
        { lat: 57.3229, lng: -4.4244, label: 'Loch Ness', num: 2, cat: 'attraction', desc: '37km loch, 240m deep — more fresh water than England and Wales combined' },
        { lat: 57.4768, lng: -4.0959, label: 'Culloden Battlefield', num: 3, cat: 'attraction', desc: 'Last battle on British soil (1746) — clan grave stones, immersive NTS visitor centre' },
        { lat: 57.4778, lng: -4.2247, label: 'Inverness Hootananny', num: 4, cat: 'attraction', desc: 'Live Highland folk music most evenings — best Inverness pub experience' }
      ]
    },

    // DAY 13 — Cairngorms Day or Speyside
    {
      num: 13,
      date: '2026-06-06',
      title: 'Cairngorms National Park & the Road South',
      description: 'A scenic day through the Cairngorms — Britain\'s largest national park — stopping at Aviemore, the Highland Folk Museum, and beginning the journey back toward Edinburgh.',
      neighborhoods: 'Aviemore · Kingussie · Newtonmore · Pitlochry',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Aviemore & Cairngorms',
              description: 'Drive south from Inverness on the A9 into the Cairngorms — a high plateau national park with ancient Caledonian pinewoods, red squirrels, ospreys, and red deer. Aviemore is the outdoor activity hub — walking, cycling, skiing in winter. The CairnGorm Mountain funicular railway (when operating) takes you to 1085m for panoramic views.',
              details: ['📍 Aviemore, PH22 1PP', '💡 Short walks from Aviemore: Loch Morlich (beautiful circular walk, 1.5 hours), the Rothiemurchus Forest for ancient pines and red squirrels.']
            },
            {
              title: 'Highland Folk Museum, Newtonmore',
              description: 'An extraordinary open-air museum spread across 80 acres — a reconstructed Highland township showing how people lived from the 1700s to the 1960s. Working crofts, mills, a 1930s school where lessons are still "taught," a salmon smoker, and costumed interpreters. FREE. One of Scotland\'s most underrated attractions.',
              details: ['📍 Aultlarie Croft, Newtonmore PH20 1AY', '🕐 April-Oct 10am-5pm · FREE', '💡 This is genuinely superb and most tourists miss it. Allow 2 hours minimum.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Aviemore cafes or hostel',
              description: '',
              meta: '📍 Aviemore · 💰 £5-9'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pitlochry — The Perfect Highland Town',
              description: 'Continue south to Pitlochry — a Victorian resort town in the Tummel valley, surrounded by forested hills. Walk the Pitlochry Dam fish ladder (free — watch salmon jumping upstream through the glass-walled viewing chamber), stroll along the River Tummel to the dam, and explore the attractive main street. The Edradour Distillery — Scotland\'s smallest traditional distillery — is 3km away and offers free tours.',
              details: ['📍 Pitlochry, Perthshire PH16 5BX', '🕐 Salmon ladder: free, open all day', '💡 Edradour Distillery tour is excellent and ends with a free dram. Walk or taxi from town (3km).']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Moulin Hotel Pub, Pitlochry',
              description: 'The Moulin Hotel is a 17th-century coaching inn slightly above the town. The pub does excellent real ales brewed on site and proper pub food — stovies, Scotch broth, game pie.',
              meta: '📍 11 Kirkmichael Road, Pitlochry · 💰 £9-15'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Soldier Loch / Loch Faskally Walk & Evening in Pitlochry',
              description: 'An evening walk along Loch Faskally (the reservoir above Pitlochry Dam) through the mixed woodland is beautiful in June. The Pitlochry Festival Theatre does nightly productions through summer — check pitlochryfestivaltheatre.com for what\'s on during your visit.',
              details: ['📍 Pitlochry · 💡 The evening light on the Tummel valley is gorgeous in early June.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Old Mill Inn, Pitlochry',
              description: 'Solid pub food in a converted mill building. Steak pie, haggis nachos, and good local ales. Affordable and filling.',
              meta: '📍 Mill Lane, Pitlochry · 💰 £10-16'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Sleep in Pitlochry tonight — it\'s ideally placed for tomorrow\'s drive south via Dunkeld, and only 90 minutes from Edinburgh.' }
          ]
        }
      ],
      mapPins: [
        { lat: 57.1942, lng: -3.8306, label: 'Aviemore', num: 1, cat: 'neighborhood', desc: 'Cairngorms activity hub — Loch Morlich, Rothiemurchus Forest' },
        { lat: 56.9884, lng: -4.1188, label: 'Highland Folk Museum', num: 2, cat: 'attraction', desc: 'Free open-air museum — 300 years of Highland life, 80 acres' },
        { lat: 56.7042, lng: -3.7350, label: 'Pitlochry', num: 3, cat: 'neighborhood', desc: 'Victorian Perthshire resort — salmon ladder, Edradour Distillery' },
        { lat: 56.7050, lng: -3.7420, label: 'Moulin Hotel', num: 4, cat: 'restaurant', desc: '17th-century coaching inn with own brewery and excellent pub food' },
        { lat: 56.7219, lng: -3.7997, label: 'Edradour Distillery', num: 5, cat: 'attraction', desc: 'Scotland\'s smallest traditional distillery — free tours, free dram' }
      ]
    },

    // DAY 14 — Dunkeld, Aberfeldy & Perthshire
    {
      num: 14,
      date: '2026-06-07',
      title: 'Perthshire\'s Gentle Heartland: Dunkeld & Aberfeldy',
      description: 'Explore the cathedral town of Dunkeld on the River Tay, walk the Hermitage with the Black Linn Falls, and wander Aberfeldy before a final afternoon back in Edinburgh.',
      neighborhoods: 'Dunkeld · Birnam · Aberfeldy · Perth',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'The Hermitage, Dunkeld',
              description: 'Ossian\'s Hall — the Hermitage is a National Trust for Scotland woodland walk following the River Braan through towering Douglas firs (some of the tallest trees in Britain) to Ossian\'s Hall perched above the thundering Black Linn waterfall. The falls plunge through a narrow gorge into a deep dark pool. About 2 km walk round trip. One of Perthshire\'s finest natural sites. FREE.',
              details: ['📍 The Hermitage, Dunkeld PH8 0HX (off A9, 2km from Dunkeld)', '🕐 Open 24/7 · Free parking £3', '💡 The Douglas Firs here are extraordinary — some over 60m tall. The combination of waterfall, giant trees, and 18th-century folly is uniquely magical.']
            },
            {
              title: 'Dunkeld Cathedral & Little Houses',
              description: 'Dunkeld Cathedral sits half-ruined, half-intact on the banks of the River Tay — built from 1318, the nave is still roofless but the choir functions as the parish church. The town\'s Little Houses — a row of perfectly restored 17th-century whitewashed cottages along Cathedral Street — are charming. Birnam across the river is where Shakespeare\'s Macbeth forest marched from.',
              details: ['📍 Dunkeld Cathedral, PH8 0AW', '🕐 Cathedral: always accessible · FREE', '💡 Walk the suspension bridge to Birnam for the Macbeth connection and the Birnam Oak — one of Scotland\'s oldest trees, possibly referenced in Macbeth.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Dunkeld Hostel café or Dunkeld town cafes',
              description: '',
              meta: '📍 Dunkeld · 💰 £5-9'
            }
          ],
          tips: []
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Aberfeldy & Wade\'s Bridge',
              description: 'Drive west to Aberfeldy — a picturesque Perthshire town on the River Tay. General Wade\'s Bridge (1733) — built to subjugate the Highlands after the Jacobite Rising — is a masterpiece of military engineering. The Aberfeldy Distillery does excellent whisky tours. The town itself is a good coffee and browse stop.',
              details: ['📍 Aberfeldy, PH15 2BD', '🕐 Aberfeldy Distillery: 10am-5pm Mon-Sat · Tour £10', '💡 The water of life actually begins here: Glen Lyon — the longest enclosed glen in Scotland — starts just west of Aberfeldy.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'The Watermill, Aberfeldy',
              description: 'A beautifully converted working watermill housing an excellent bookshop and café. Great soups, toasties, and cakes. A genuinely lovely lunch stop before the drive back to Edinburgh.',
              meta: '📍 Mill Street, Aberfeldy · 💰 £7-12'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Return to Edinburgh',
              description: 'Drive south through Perthshire and back to Edinburgh — about 90 minutes via the A9 and M90 from Aberfeldy. Return your hire car (if applicable) and check into a final night in Edinburgh. The city will feel different now — richer with context after all you\'ve seen.',
              details: ['📍 Edinburgh', '💡 If you have time, stop at Kinross and Loch Leven — where Mary Queen of Scots was imprisoned in the castle on the island — for a final historical resonance.']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Edinburgh Evening',
              description: 'Back in Edinburgh for a final night. Treat yourself to dinner somewhere you haven\'t been. Head to the Old Town for a final evening walk — the illuminated castle, the cobblestones, the smell of hops and old stone.',
              details: ['📍 Edinburgh Old Town']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Witchery by the Castle',
              description: 'A splurge for the final night — Edinburgh\'s most theatrical restaurant, inside a 16th-century building at the top of the Royal Mile. Dramatic gothic interiors, candles, red velvet, and excellent Scottish produce. Order the venison or the langoustines. Unforgettable.',
              meta: '📍 Castlehill, Royal Mile, Edinburgh · 💰 £30-50 · ⭐ Book well ahead'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After 14 days of Scotland, The Witchery\'s theatrical excess feels entirely appropriate. Book a table by the window if available.' }
          ]
        }
      ],
      mapPins: [
        { lat: 56.5620, lng: -3.6137, label: 'The Hermitage & Black Linn Falls', num: 1, cat: 'attraction', desc: 'Stunning woodland walk — giant Douglas firs, thundering waterfall, free' },
        { lat: 56.5635, lng: -3.5879, label: 'Dunkeld Cathedral', num: 2, cat: 'attraction', desc: 'Half-ruined 14th-century cathedral on the banks of the Tay, free' },
        { lat: 56.6218, lng: -3.8602, label: 'Aberfeldy', num: 3, cat: 'neighborhood', desc: 'Perthshire town — Wade\'s Bridge, distillery, watermill café' },
        { lat: 56.6224, lng: -3.8571, label: 'The Watermill Aberfeldy', num: 4, cat: 'restaurant', desc: 'Bookshop café in a working watermill — excellent lunch' },
        { lat: 55.9500, lng: -3.1890, label: 'Return to Edinburgh', num: 5, cat: 'neighborhood', desc: 'Final night in the capital' }
      ]
    },

    // DAY 15 — Edinburgh Final Day
    {
      num: 15,
      date: '2026-06-08',
      title: 'Edinburgh Farewell: Portobello & Hidden Gems',
      description: 'A relaxed final full day in Edinburgh — explore Portobello Beach, the Scottish Parliament, and any remaining Old Town spots. Pick up souvenirs, and enjoy a proper Scottish farewell dinner.',
      neighborhoods: 'Portobello · Canongate · Scottish Parliament · Old Town',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Portobello Beach',
              description: 'Edinburgh\'s seaside — a long sandy beach just 4km from the city centre, accessible by bus 26 or 42 (15 min). In June the promenade is lively with locals, ice cream vans, and dogs. Wild swimming in the Firth of Forth is popular (and invigorating). The Victorian era seafront architecture is charming.',
              details: ['📍 Portobello, Edinburgh EH15', '🕐 Always open · Free · Bus 26 or 42 from city centre', '💡 A morning swim at Portobello is a proper Edinburgh rite of passage. The water is cold. The feeling after is wonderful.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Harry\'s Café, Portobello',
              description: 'A Portobello institution right on the High Street — excellent full Scottish breakfast with Lorne sausage (square sausage), black pudding, tattie scones, and proper fried eggs.',
              meta: '📍 95 Portobello High Street, Edinburgh · 💰 £8-12'
            }
          ],
          tips: []
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Scottish Parliament Building (Holyrood)',
              description: 'Return via Holyrood and visit the Scottish Parliament building — the controversial but fascinating Enric Miralles-designed building that opened in 2004. Free public access to the public areas; free guided tours when parliament isn\'t sitting. The architectural symbolism (upturned boats referencing Scottish fishing villages, Raeburn paintings embedded in MSP offices) is worth exploring.',
              details: ['📍 Horse Wynd, Edinburgh EH99 1SP', '🕐 Mon-Fri 10am-5pm · FREE', '💡 Guided tours are free and excellent — book at the reception desk. The Debating Chamber is extraordinary.']
            },
            {
              title: 'Canongate Kirkyard & Final Royal Mile',
              description: 'Walk the lower end of the Royal Mile — the Canongate section — past John Knox\'s House (Edinburgh\'s oldest inhabited building), the Museum of Edinburgh (free local history), and into Canongate Kirkyard where the graves include Adam Smith (economist), Robert Fergusson (Burns\'s hero-poet), and Dugald Stewart.',
              details: ['📍 Canongate, Edinburgh', '💡 Canongate Kirkyard is free and quieter than Greyfriars. The economic history buried in the Adam Smith grave alone is remarkable.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Cannonball Restaurant & Bar, Edinburgh Castle',
              description: 'Just steps below the Castle Esplanade, Cannonball serves excellent Scottish dishes in a historic 1630s building. Cullen skink, haggis bon bons, Scottish salmon. A perfect final lunch with castle views.',
              meta: '📍 356 Castlehill, Edinburgh EH1 2NE · 💰 £14-22'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Souvenir Shopping & Final Wanders',
              description: 'Spend the afternoon picking up any final souvenirs. Edinburgh has excellent options: Ragamuffin on the Royal Mile for quality Scottish textiles; Valvona & Crolla (the legendary Italian deli near Broughton Street) for edible gifts; the Tartan Blanket Co. for beautiful woven pieces. Walk Princes Street Gardens one last time in the afternoon light.',
              details: ['📍 Royal Mile & surrounding areas', '💡 Best value whisky is at Cadenhead\'s on Canongate — an independent bottler with no-nonsense prices and incredible selection.']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Edinburgh Finale: Old Town by Night',
              description: 'Walk the Royal Mile one last time as Edinburgh\'s evening golden light hits the stone. The closes, the Castle, Greyfriars Bobby — all feel different after two weeks of Scotland. End at a traditional pub for a final Scottish dram.',
              details: ['📍 Edinburgh Old Town', '💡 The Bow Bar on Victoria Street remains the ideal farewell pub — excellent whisky, no music, just conversation and good ale.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ondine',
              description: 'Edinburgh\'s finest sustainable seafood restaurant — Hebridean langoustines, Orkney crab, and native oysters. A fitting farewell that brings the journey full circle from the Outer Isles. Set pre-theatre menu is good value at around £35-40 for two courses.',
              meta: '📍 2 George IV Bridge, Edinburgh · 💰 £25-40 · ⭐ Book ahead'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Order the langoustines at Ondine — if they have Isle of Lewis langoustines, they\'ll taste even better knowing you\'ve been there.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9530, lng: -3.1105, label: 'Portobello Beach', num: 1, cat: 'attraction', desc: 'Edinburgh\'s seaside — sandy beach, promenade, wild swimming in the Forth' },
        { lat: 55.9503, lng: -3.1746, label: 'Scottish Parliament', num: 2, cat: 'attraction', desc: 'Controversial Miralles masterpiece — free tours, remarkable architecture' },
        { lat: 55.9496, lng: -3.1893, label: 'Cannonball Restaurant', num: 3, cat: 'restaurant', desc: '1630s building below Castle — great Scottish lunch' },
        { lat: 55.9477, lng: -3.1923, label: 'Bow Bar, Victoria Street', num: 4, cat: 'attraction', desc: 'Edinburgh\'s finest whisky pub — excellent cask ales, no music' },
        { lat: 55.9471, lng: -3.1918, label: 'Ondine Restaurant', num: 5, cat: 'restaurant', desc: 'Sustainable Scottish seafood — langoustines, crab, oysters' }
      ]
    },

    // DAY 16 — Departure
    {
      num: 16,
      date: '2026-06-09',
      title: 'Departure Day: A Final Edinburgh Morning',
      description: 'A relaxed final morning in Edinburgh before departing. Sunrise walk, a great breakfast, and the airport — leaving Scotland with memories that will last years.',
      neighborhoods: 'Old Town · Edinburgh Airport',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dawn Walk: Arthur\'s Seat or Calton Hill',
              description: 'Rise early for one last Edinburgh dawn walk. Arthur\'s Seat rewards early risers with the city still sleeping below; Calton Hill is quicker and still spectacular. Either way, Edinburgh in the morning light on your last day — knowing what you know now about Scotland — will feel different and deeply meaningful.',
              details: ['📍 Arthur\'s Seat or Calton Hill, Edinburgh', '🕐 Sunrise is before 5am in June — but even a 6am walk catches the golden hour', '💡 Take your time. Breathe it in. Scotland will still be here.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Café Andaluz or The Edinburgh Larder',
              description: 'The Edinburgh Larder on Blackfriars Street does a brilliant final breakfast — Scottish smoked salmon and scrambled eggs, Stornoway black pudding on toast. A perfect final taste of Scotland.',
              meta: '📍 15 Blackfriars Street, Edinburgh · 💰 £8-14 · 🕐 Opens 8am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Edinburgh Airport is 30 minutes from the city centre by tram (from St Andrew\'s Square, £8.50). Allow 2 hours before your flight.' }
          ]
        },
        {
          label: 'Departure',
          activities: [
            {
              title: 'Airport Transfer',
              description: 'Take the Edinburgh Tram from York Place (near St Andrew\'s Square) directly to Edinburgh Airport — 35 minutes, £8.50 one way. The tram runs every 7-12 minutes. Clean, reliable, and the best budget transfer option.',
              details: ['📍 York Place tram stop, Edinburgh City Centre', '🕐 Trams run 6am-midnight, every 7-12 minutes · £8.50 one way', '💡 Check in online and get to the airport at least 2 hours before departure.']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 Scotland has a way of getting under your skin. You\'ll be back.' }
          ]
        }
      ],
      mapPins: [
        { lat: 55.9441, lng: -3.1615, label: 'Arthur\'s Seat — Final Dawn', num: 1, cat: 'attraction', desc: 'One last sunrise over the city' },
        { lat: 55.9500, lng: -3.1849, label: 'The Edinburgh Larder', num: 2, cat: 'restaurant', desc: 'Perfect final Scottish breakfast — salmon, Stornoway black pudding' },
        { lat: 55.9557, lng: -3.1875, label: 'York Place Tram Stop', num: 3, cat: 'transport', desc: 'Edinburgh Tram to Airport — 35 min, £8.50' },
        { lat: 55.9508, lng: -3.3615, label: 'Edinburgh Airport', num: 4, cat: 'transport', desc: 'Edinburgh International Airport (EDI)' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (15 nights)', budget: '$330 – $480', notes: 'Hostel dorms £18-28/night avg. Wild camping some nights saves money.' },
    { category: 'Food & Drink', budget: '$280 – $380', notes: 'Mix of self-catering, pubs, budget cafes (£15-25/day avg)' },
    { category: 'Transport', budget: '$180 – $250', notes: 'Trains + buses + CalMac ferry. Car rental adds cost but enables Hebrides & Highlands.' },
    { category: 'Attractions', budget: '$80 – $130', notes: 'Edinburgh Castle £20, Stirling £17, Rosslyn £10. Many are free (NMS, Callanish, Arthur\'s Seat, Culloden walk-ins).' },
    { category: 'CalMac Ferry (Lewis)', budget: '$45 – $55', notes: 'Ullapool–Stornoway return (passenger only, no car)' },
    { category: 'Food shopping / picnics', budget: '$40 – $60', notes: 'Co-ops and Lidls for Highlands picnic supplies' },
    { category: 'Miscellaneous', budget: '$25 – $50', notes: 'Midges repellent, postcard, the odd dram of whisky' },
  ],

  practicalInfo: [
    { title: '✈️ Getting to Edinburgh', items: ['Edinburgh Airport (EDI) is well connected. Tram from city centre: 35 min, £8.50. Bus 100 Airlink: 25-40 min, £5.50.', 'Budget airlines (Ryanair, easyJet) serve Edinburgh from most European cities.', 'No visa required for most nationalities for UK visits under 6 months.'] },
    { title: '🚂 Rail & Bus Passes', items: ['ScotRail Spirit of Scotland Rover pass: 4 days travel in 8 days (from £135) — good for Edinburgh-Inverness-Pitlochry circuit.', 'Citylink buses: book ahead online at citylink.co.uk for cheapest fares.', 'Megabus Scotland routes: very cheap if booked weeks ahead.'] },
    { title: '🏕️ Wild Camping', items: ['Scotland\'s Land Reform (Scotland) Act 2003 gives the right to camp almost anywhere.', 'Wild camping in the Highlands and Islands is free and legal — invest in a lightweight tent.', 'Leave No Trace principles apply: carry out all waste, use a trowel, leave sites pristine.'] },
    { title: '🧴 Midges Warning', items: ['Highland midges (tiny biting insects) appear from late May and peak in July-August.', 'Worst in still, humid conditions, especially near water and in sheltered glens.', 'DEET-based repellent (Smidge or Avon Skin So Soft) is essential for Glencoe, Loch Ness, and Isle of Lewis evenings.', 'Wind and sun significantly reduce midge activity.'] },
    { title: '📱 Mobile Coverage', items: ['EE has the best coverage in Scotland including the Highlands.', 'Isle of Lewis has patchy coverage — download offline maps on OS Maps or Maps.me before you leave Stornoway.', 'Callanish, Carloway, and the west coast may have no signal — plan accordingly.'] },
    { title: '⏰ June Daylight', items: ['Late May to early June: sunset around 10pm in Edinburgh, later still further north.', 'Isle of Lewis in June barely gets dark — the sky is luminous until midnight.', 'This is Scotland\'s finest gift to summer visitors. Use every minute of light.'] },
  ]
};

fulfillOrder(order, itineraryData);
