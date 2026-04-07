const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1773495735772_i3e3ij',
  email: 'bdavis72@gmail.com',
  destination: 'Switzerland',
  start_date: '2026-04-26',
  end_date: '2026-05-14',
  group_size: '2',
  travel_style: 'Adventure, Foodie, Relaxation, Family-friendly',
  dining: 'Mix of everything',
  budget: '$10,000+',
  requests: 'Focus on photography spots. Provide locations for best pictures and places not to miss. Zurich 3 days → Lucerne 3 days → Wengen 5 days → Zermatt 3 days → Montreux 3 days → depart via Geneva 2 days.'
};

const itineraryData = {
  destination: 'Switzerland',
  countryEmoji: '🇨🇭',
  title: 'Switzerland Photography Odyssey',
  subtitle: '19 Days Through Zurich, Lucerne, Wengen, Zermatt & Montreux',
  description: 'A masterfully routed 19-day journey through Switzerland\'s most photogenic landscapes — from Zurich\'s reflective lakeshores and Lucerne\'s medieval bridges to the Jungfrau\'s icy spires, the Matterhorn\'s mirror-lake reflections, and Montreux\'s vineyard-draped shores. Built for two adventurous foodies chasing golden-hour alpenglow, hidden mountain hamlets, and Michelin-starred fondue.',
  duration: '19 days',
  dates: 'April 26 – May 14, 2026',
  budget: '$10,000+',
  pace: 'Moderate-Active',
  bestFor: 'Couples, photography enthusiasts, adventure foodies',
  highlights: [
    'Matterhorn mirror reflections at Stellisee & Riffelsee (Zermatt)',
    'Jungfraujoch Top of Europe at 3,454m with Aletsch Glacier views',
    'Kapellbrücke golden hour reflections in Lucerne',
    'Männlichen ridge walk with panoramic Jungfrau views',
    'Château de Chillon on Lake Geneva',
    'Lavaux UNESCO vineyards above Lake Geneva',
    'Mt. Pilatus cogwheel railway — steepest in the world',
    'Car-free Wengen with unobstructed Jungfrau panoramas'
  ],

  essentials: [
    { title: '🎫 Swiss Travel Pass', text: 'Get the 15-day Swiss Travel Pass (around CHF 580/person) — covers all trains, most cable cars/cogwheels, and many museums. Buy before leaving home for the best rate. The Grand Train Tour of Switzerland connects all your stops perfectly.' },
    { title: '📷 Camera Essentials', text: 'Bring a polarizing filter for Alpine lake reflections — essential for Stellisee and Riffelsee. A telephoto lens (200mm+) brings Matterhorn details to life. Arrive at viewpoints 30-45 min before sunrise for golden hour alpenglow. Spring (April-May) means wildflowers and snow-capped peaks — best of both worlds.' },
    { title: '🏔️ Altitude & Weather', text: 'May in the Alps means rapid weather changes. Layer up: base layer, fleece, waterproof shell. Jungfraujoch can be -10°C and windy even in May. At lower elevations, temperatures are 12-18°C. Check cable car/cogwheel status the day before — they close in bad weather.' },
    { title: '🚆 Train Logistics', text: 'Swiss trains are punctual to the minute. Book Jungfraujoch tickets in advance (CHF 190/person with Swiss Travel Pass discount). The Glacier Express and GoldenPass Line are scenic train journeys worth taking. Wengen and Zermatt are car-free — park at Grindelwald or Täsch respectively.' },
    { title: '💰 Money & Budget', text: 'Switzerland is expensive — budget CHF 150-250/day per person for mid-range dining. Most places accept credit cards. Tipping isn\'t mandatory but 5-10% is appreciated. The biggest costs are mountain excursions (Jungfraujoch CHF 190+, Gornergrat CHF 90+). Lunch at mountain restaurants saves vs. dinner.' },
    { title: '🍽️ Food Culture', text: 'Fondue and raclette are at their absolute best in mountain villages. Try Rösti (Swiss potato cake), Birchermüesli (invented in Zurich), and Zürcher Geschnetzeltes (creamy veal in Zurich). Each region has its own wine — Chasselas whites around Montreux/Lavaux are world-class.' }
  ],

  days: [
    // ===================== ZURICH: DAYS 1-3 =====================
    {
      num: 1,
      neighborhoods: 'Zurich · Kloten Airport · Altstadt',
      title: 'Arrival in Zurich — First Impressions',
      description: 'Touch down in one of the world\'s most liveable cities. After checking in, golden-hour light on Lake Zurich rewards the jetlagged with some of the most beautiful urban photography in Europe.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            { title: 'Arrive at Zurich Airport (ZRH)', description: 'Zurich Airport is efficient and beautiful — the train station is directly below Terminal 1. Take the 10-minute train to Zurich Hauptbahnhof (main station). Your Swiss Travel Pass activates from today.', details: ['🚆 Airport → HB: CHF 6.80 or free with Swiss Travel Pass', '💡 Buy a local SIM or activate roaming — Swiss coverage is excellent', '📸 The airport itself has nice architectural lines worth a shot'] },
            { title: 'Check In & Explore Niederdorf', description: 'The medieval Old Town\'s Niederdorf quarter is your orientation walk — cobblestone lanes, guild houses, and the Limmat river. Cross the Münsterbrücke for your first views of Grossmünster\'s twin towers.', details: ['📸 Photo spot: Münsterbrücke with Grossmünster reflection in the Limmat river', '📍 Niederdorf is car-free and endlessly photogenic', '🕐 Allow 1-1.5 hours for wandering'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Sunset at Bürkliplatz & Lake Zurich', description: 'Walk to Bürkliplatz where the Limmat meets Lake Zurich. On clear days you can see the snow-capped Alps reflected in the lake. The Pavilion and the lakeside Quai are prime spots for long-exposure photography as the city lights come on.', details: ['📸 Best shot: Looking south from Quaibrücke toward the Alps', '🕐 Golden hour typically 7:30-8:30pm in late April', '💡 The "foehn" wind from the Alps sometimes clears the air for crystal mountain views'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Haus Hiltl', description: 'The world\'s oldest vegetarian restaurant (est. 1898) — a Zurich institution with a legendary buffet. Don\'t let "vegetarian" fool you: this is some of the most creative, satisfying food in the city.', meta: '€€ · Sihlstrasse 28 · Vegetarian · Open late' },
            { type: '☕ Nightcap', name: 'Kronenhalle Bar', description: 'Legendary art-filled bar with original Picassos and Mirós on the walls. Order a Spritz and soak in 100 years of Zurich bohemian history.', meta: '€€€ · Rämistrasse 4 · Historic bar' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.4582, lng: 8.5555, label: 'Zurich Airport (ZRH)', num: 1, cat: 'transport', desc: 'Arrival — train directly below terminal to city center' },
        { lat: 47.3778, lng: 8.5402, label: 'Zurich Hauptbahnhof', num: 2, cat: 'transport', desc: 'Main train station — Swiss Travel Pass hub' },
        { lat: 47.3764, lng: 8.5446, label: 'Niederdorf Quarter', num: 3, cat: 'attraction', desc: 'Medieval cobblestone quarter for evening stroll' },
        { lat: 47.3697, lng: 8.5437, label: 'Grossmünster', num: 4, cat: 'attraction', desc: 'Twin-towered Romanesque cathedral — iconic Zurich' },
        { lat: 47.3665, lng: 8.5416, label: 'Bürkliplatz & Lake Zurich', num: 5, cat: 'photo', desc: 'Golden hour shot: Alps reflected in the lake' },
        { lat: 47.3706, lng: 8.5397, label: 'Haus Hiltl', num: 6, cat: 'food', desc: 'World\'s oldest vegetarian restaurant, legendary buffet' }
      ]
    },
    {
      num: 2,
      neighborhoods: 'Zurich · Altstadt · Zürich West',
      title: 'Old Town Splendor & Urban Photography',
      description: 'Zurich\'s photogenic Old Town in the morning light, world-class museums in the afternoon, and the edgy Zürich West district after dark — one city, three completely different personalities.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Grossmünster & Fraumünster Golden Hour', description: 'Be at the Münsterbrücke by 7am. The low morning light hits the twin spires of Grossmünster while the Fraumünster\'s Chagall windows glow from within. The Limmat river perfectly mirrors the façades on a still morning.', details: ['📸 Best angle: From the east bank of the Limmat looking west at Fraumünster', '📸 Wide angle for the bridge + both towers in one frame', 'Fraumünster interior (Chagall windows) opens at 10am'] },
            { title: 'Fraumünster Chagall Windows', description: 'Five stained-glass windows by Marc Chagall (1970) and a rose window by Alberto Giacometti. When morning light streams through, the colors are extraordinary. One of the most underrated photo subjects in Switzerland.', details: ['🎟️ CHF 5 entry', '📸 Bring a tripod — interior is dim', '💡 Cloudy days diffuse the light beautifully for windows'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: 'Bahnhofstrasse & Confiserie Sprüngli', description: 'Switzerland\'s most famous shopping street is beautiful before the crowds arrive. Stop at Sprüngli at Paradeplatz for their legendary Luxemburgerli macarons — a Swiss institution since 1836. The flagship store is architecturally beautiful.', details: ['📸 Photo spot: Bahnhofstrasse from Paradeplatz toward the lake on a clear day', '☕ Order a coffee and Luxemburgerli at the Sprüngli café', '💡 The street is car-free and surprisingly photogenic before 10am'] },
            { title: 'Swiss National Museum (Landesmuseum)', description: 'In a castle-like building right next to HB, this museum covers Swiss history and culture. The medieval armory and reconstructed guild rooms are extraordinary. Budget 1.5-2 hours.', details: ['🎟️ Free with Swiss Travel Pass', '📸 The castle exterior and courtyard are photogenic', '🕐 Opens at 10am'] }
          ],
          meals: [
            { type: '☕ Breakfast', name: 'Café Schwarzenbach', description: 'A 130-year-old specialty grocery and café in Niederdorf. Incredible coffee and traditional Swiss pastries. The interior is a photographer\'s dream.', meta: '€ · Münstergasse 19 · Historic café' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Kunsthaus Zürich', description: 'Switzerland\'s largest art museum houses Giacometti, Monet, and an outstanding modern art extension. Recently expanded (2021) with a stunning new wing by David Chipperfield. Allow 2 hours.', details: ['🎟️ CHF 26 (not covered by Swiss Pass)', '📸 The new wing\'s massive skylights are architectural art', 'Tip: Tuesday evenings are free after 5pm'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 Zürich West (Industriequartier)', description: 'Zurich\'s coolest neighborhood occupies former industrial buildings. The Viadukt arches house boutique shops; Frau Gerolds Garten is an urban garden bar. Prime for street photography — gritty murals, converted warehouses, creative energy.', details: ['📸 Best spot: Under the railway viaduct arches at dusk', '📸 Frau Gerolds Garten for urban garden atmosphere', '💡 Most interesting after 6pm when the bars and restaurants fill up'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Zeughauskeller', description: 'Massive historic armory (1487) converted into a beer hall. Zürich\'s most atmospheric dinner — long communal tables, enormous portions of Zürcher Geschnetzeltes, and Swiss beer on tap.', meta: '€€ · Bahnhofstrasse 28a · Swiss beer hall · Very popular' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.3714, lng: 8.5404, label: 'Fraumünster', num: 1, cat: 'photo', desc: 'Chagall stained-glass windows — morning light essential' },
        { lat: 47.3697, lng: 8.5443, label: 'Grossmünster', num: 2, cat: 'photo', desc: 'Twin towers — Limmat river reflection at dawn' },
        { lat: 47.3706, lng: 8.5397, label: 'Paradeplatz & Sprüngli', num: 3, cat: 'food', desc: 'Legendary macarons and Bahnhofstrasse photography' },
        { lat: 47.3793, lng: 8.5395, label: 'Swiss National Museum', num: 4, cat: 'attraction', desc: 'Castle-like museum of Swiss history — free with Swiss Pass' },
        { lat: 47.3705, lng: 8.5485, label: 'Kunsthaus Zürich', num: 5, cat: 'attraction', desc: 'Switzerland\'s largest art museum, Chipperfield extension' },
        { lat: 47.3847, lng: 8.5127, label: 'Zürich West / Viadukt', num: 6, cat: 'photo', desc: 'Industrial-chic district, murals, arched viaduct' },
        { lat: 47.3770, lng: 8.5388, label: 'Zeughauskeller', num: 7, cat: 'food', desc: '1487 armory beer hall — authentic Zürich dinner' }
      ]
    },
    {
      num: 3,
      neighborhoods: 'Zurich · Uetliberg · Seefeld',
      title: 'Uetliberg Summit & Alpine Panorama',
      description: 'Zurich\'s local mountain delivers the city\'s best panoramic photography — Alps to one side, the city and its lake to the other. Spring wildflowers bloom along the ridge. Afternoon rewards with the beautiful Seefeld lakeside.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Uetliberg Mountain at Sunrise', description: 'Take the S10 train from HB directly to Uetliberg (30 min). Arrive before sunrise to watch the Alps glow pink with alpenglow while the city wakes below. The TV tower observation deck (130m climb) gives a 360° view stretching to the Black Forest on clear days.', details: ['🚆 S10 from HB: every 30min, covered by Swiss Travel Pass', '📸 Best angle: From the ridge trail heading south — city + lake + Alps', '🌅 Sunrise April 26: approximately 6:20am CST', '💡 The 10km Planet Trail along the ridge is moderate and beautiful'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: 'Uetliberg Ridge Walk (Planet Trail)', description: 'Follow the ridge south toward Felsenegg (about 5km, 2 hours). The trail passes through beech forests with occasional openings revealing the whole Alpine arc from the Säntis to the Bernese Alps. Take the gondola down from Felsenegg to Adliswil, then train back.', details: ['📸 Best photo stop: Km 3 lookout over the Zürichsee', '🥾 Trail is well-maintained but can be muddy in spring', 'Return to Zurich by 1pm for afternoon activities'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Restaurant Uto Kulm (summit)', description: 'Restaurant right at the Uetliberg summit with panoramic terrace. Classic Swiss lunch: Rösti with fried egg, local sausages, and a cold Feldschlösschen beer.', meta: '€€ · Uetliberg summit · Swiss classics' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Seefeld District & Quaibrücke', description: 'Zurich\'s most upscale lakeside neighborhood. The Quaibrücke offers your best shot of the city skyline with the Grossmünster towers. Walk the full Seequai south to Zürichhorn — boats, swans, and manicured gardens.', details: ['📸 Best angle: From Quaibrücke looking toward Fraumünster', '📸 The Chinese Garden (free) reflects in the lake beautifully', '💡 On clear spring days you can see Säntis mountain from the far shore'] },
            { title: '📸 Lindenhügel Viewpoint at Golden Hour', description: 'This small hill in the Altstadt above the river is Zurich\'s best-kept photo secret. At golden hour, the warm light cascades over the Grossmünster towers and down across the red-roofed Old Town. Locals come here to watch the sunset.', details: ['📍 Access from Lindenhügel steps off Schipfe', '📸 Bring a medium telephoto to compress the towers against the skyline', '🕐 Best 30 minutes before sunset'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Clouds Restaurant (Prime Tower)', description: 'On the 35th floor of Zurich\'s tallest building, Clouds delivers the city\'s most spectacular evening view. The menu is contemporary Swiss-international — excellent Zürichsee perch (Egli) and refined Swiss beef.', meta: '€€€ · Prime Tower, Maagplatz · View restaurant · Reserve ahead' }
          ],
          tips: [{ type: 'tip', text: '🎒 Pack tonight for Lucerne tomorrow. It\'s only 50 minutes by train, but you\'ll want your photography gear ready at the Chapel Bridge for golden-hour arrival.' }]
        }
      ],
      mapPins: [
        { lat: 47.3507, lng: 8.4916, label: 'Uetliberg Summit', num: 1, cat: 'photo', desc: '360° Alpine panorama — arrive before sunrise' },
        { lat: 47.3290, lng: 8.4794, label: 'Felsenegg (Planet Trail end)', num: 2, cat: 'attraction', desc: 'Gondola down after the ridge walk' },
        { lat: 47.3686, lng: 8.5436, label: 'Quaibrücke', num: 3, cat: 'photo', desc: 'Zurich skyline + Grossmünster towers from the lake bridge' },
        { lat: 47.3786, lng: 8.5416, label: 'Lindenhügel Viewpoint', num: 4, cat: 'photo', desc: 'Secret hilltop golden-hour view over Old Town rooftops' },
        { lat: 47.3720, lng: 8.5419, label: 'Schipfe (Limmat riverside)', num: 5, cat: 'attraction', desc: 'Charming riverside lane below the Old Town' },
        { lat: 47.3847, lng: 8.5199, label: 'Prime Tower / Clouds Restaurant', num: 6, cat: 'food', desc: '35th-floor view restaurant — book well ahead' }
      ]
    },

    // ===================== LUCERNE: DAYS 4-6 =====================
    {
      num: 4,
      neighborhoods: 'Zurich → Lucerne · Kapellbrücke · Old Town',
      title: 'Arrive Lucerne — The Painted Bridge',
      description: 'Fifty minutes south of Zurich, Lucerne feels like another century. The 14th-century Chapel Bridge (world\'s oldest covered wooden bridge) glows amber in the afternoon sun. Settle in, shoot the bridge at golden hour and blue hour, and discover why this is Switzerland\'s most-photographed city.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Last Zurich Morning — Limmat River Walk', description: 'Before leaving for Lucerne, walk the Limmat riverbanks from HB south to the lake. The morning light on the guild houses is gorgeous and the crowds haven\'t arrived yet. A perfect farewell photography session.', details: ['📸 Best angle: From Rathausbrücke looking toward Grossmünster', '🕐 Keep it to 1 hour — aim for the 10:05am IC5 to Lucerne'] }
          ],
          meals: [
            { type: '☕ Breakfast', name: 'Bircher Benner (Zurich HB)', description: 'Grab the quintessential Swiss breakfast at the main station — Birchermüesli was literally invented in Zurich by Dr. Bircher-Benner. The station has several excellent café options.', meta: '€ · Zurich HB · Swiss breakfast classics' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 Kapellbrücke (Chapel Bridge)', description: 'The 1333 covered wooden bridge with its octagonal water tower and 112 painted panels depicting Swiss history is the symbol of Lucerne — and one of the most photographed spots in all of Switzerland. Late afternoon light from the south illuminates the paintings beautifully.', details: ['📸 Best angle: From the Spreuerbrücke looking north at full bridge span', '📸 Water tower reflection: upstream side of the bridge at low angle', '📸 Bridge interior: panels are backlit beautifully in late afternoon', '💡 Arrive before 3pm for best light on the bridge paintings'] },
            { title: 'Lucerne Old Town Wander', description: 'Cross the bridge into the medieval Old Town. The Hirschenplatz and Weinmarkt squares are lined with painted facades. Seek out the "painted houses" on Weinmarkt — their frescoed walls date to the 16th century.', details: ['📸 Weinmarkt is the Instagram spot — colorful guild house facades', '📍 Rathaus (Town Hall) right on the river — great architecture', '🕐 Allow 1 hour for the square and lanes'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 KKL Building Reflection & Blue Hour', description: 'Jean Nouvel\'s concert hall (KKL Luzern) extends over the lake on a massive steel roof. At blue hour, the illuminated roof reflects perfectly in the water alongside the Kapellbrücke glow. This two-in-one shot is legendary among photographers.', details: ['📸 Stand on the station pier looking south-southwest at blue hour', '📸 Use a wide angle to capture both KKL and Chapel Bridge', '🕐 Blue hour approximately 8:30-9pm in late April'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Zunfthaus zu Pfistern', description: 'Lucerne\'s most historic guild restaurant (1341), right on the Reuss river with a terrace over the water. The Nidwalden lamb, lake fish, and Älpler Macaroni are the stars. Dine with a view of the lit Chapel Bridge.', meta: '€€€ · Kornmarkt 4 · Historic guild house · Reserve ahead' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.0508, lng: 8.3067, label: 'Kapellbrücke (Chapel Bridge)', num: 1, cat: 'photo', desc: '14th-century painted bridge — golden hour essential' },
        { lat: 47.0507, lng: 8.3050, label: 'Spreuerbrücke', num: 2, cat: 'photo', desc: 'Older covered bridge — best angle to shoot Kapellbrücke' },
        { lat: 47.0520, lng: 8.3068, label: 'Wasserturm (Water Tower)', num: 3, cat: 'photo', desc: 'Octagonal tower mid-bridge — reflection shots from upstream' },
        { lat: 47.0525, lng: 8.3090, label: 'Weinmarkt / Old Town', num: 4, cat: 'photo', desc: 'Painted guild house facades — Lucerne\'s colorful heart' },
        { lat: 47.0504, lng: 8.3099, label: 'KKL Luzern', num: 5, cat: 'photo', desc: 'Nouvel\'s steel roof reflects in the lake at blue hour' },
        { lat: 47.0512, lng: 8.3080, label: 'Zunfthaus zu Pfistern', num: 6, cat: 'food', desc: 'Historic 1341 guild restaurant on the Reuss river' }
      ]
    },
    {
      num: 5,
      neighborhoods: 'Lucerne · Mount Pilatus · Alpnachstad',
      title: 'Mount Pilatus — Dragon\'s Domain',
      description: 'Pilatus is the mythical mountain that lords over Lucerne — named for Pontius Pilate and home (according to legend) to dragons. Take the world\'s steepest cogwheel railway from Alpnachstad and spend the day above the clouds for photography that rivals Jungfraujoch at a fraction of the cost.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚢 Lake Cruise to Alpnachstad', description: 'Start with the classic "Golden Round Trip": take the lake cruise (CGN ferry) from Lucerne station pier to Alpnachstad (45 min). The lake views of Pilatus growing larger as you approach are magnificent and unmissable.', details: ['🎫 Covered by Swiss Travel Pass', '📸 Shoot Pilatus from the bow of the ferry as you approach', '🕐 First ferry 8:50am — arrive at Alpnachstad by 9:35am'] },
            { title: '🚞 World\'s Steepest Cogwheel Railway (48% gradient)', description: 'From Alpnachstad, take the cogwheel train that defies gravity up to Pilatus Kulm (2,132m). The 30-minute ascent passes through wildflower meadows and limestone cliffs with dizzying views back down to the lake. Only runs May-November.', details: ['🎫 ~CHF 72 up/down, discounted with Swiss Travel Pass', '📸 Right-side seats for best downward lake views', '💡 Check weather at pilatus.ch the morning before'] }
          ]
        },
        {
          label: 'Late Morning — Afternoon',
          activities: [
            { title: '📸 Pilatus Kulm Summit Photography', description: 'The twin summits (Esel at 2,119m and Oberhaupt at 2,132m) give 360° views of 73 Alpine peaks. On a clear day you see Lake Lucerne below, the Jura mountains to the north, and the Bernese Alps to the south. Spring often produces a "sea of clouds" below with peaks emerging — magical.', details: ['📸 Best: Sea of clouds shots if low cloud cover over the lake', '📸 Esel summit cross for classic shot with Alps behind', '📸 Dragon\'s Path trail (easy, 45 min) passes photo viewpoints', '⛏️ Pilatus also has two via ferrata routes for the adventurous'] },
            { title: 'Pilatus Palace Hotel & Dragon Rides', description: 'Even if not staying, the historic Pilatus Palace (built 1890) is a photo subject. The "Dragon Ride" gondola back down to Kriens has panoramic glass cabins perfect for aerial photography.', details: ['🎫 Dragon Ride gondola to Kriens included in Swiss Pass round trip', '📸 Gondola glass gives unobstructed aerial photos of the lake'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Restaurant Pilatus Kulm', description: 'Alpine classics at 2,100m with a terrace overlooking Lake Lucerne. The Älpler-Macaroni with applesauce is the quintessential Swiss mountain lunch. Hot chocolate required.', meta: '€€ · Pilatus summit · Alpine classics · Terrace views' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 Lion Monument at Dusk', description: 'Back in Lucerne, the Löwendenkmal (Lion Monument, 1821) carved into a cliff face is one of the most moving sculptures in Europe — Mark Twain called it "the saddest and most moving piece of rock in the world." The illuminated lion at dusk is a powerful long-exposure photo.', details: ['📍 Free, Denkmalstrasse 4', '📸 Shoot from the far end of the pond for full reflection', '🕐 Best 30 min after sunset'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Wirtshaus Galliker', description: 'Lucerne\'s most beloved old-school restaurant (est. 1856). Kalbskopf (calf\'s head), veal liver with Rösti, and a wood-paneled atmosphere that hasn\'t changed in decades. The kind of place locals eat every week.', meta: '€€ · Schützenstrasse 1 · Traditional Swiss · Cash only' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.0502, lng: 8.3089, label: 'Lucerne Station Pier', num: 1, cat: 'transport', desc: 'Lake cruise to Alpnachstad — Golden Round Trip start' },
        { lat: 46.9950, lng: 8.2787, label: 'Alpnachstad Cogwheel Station', num: 2, cat: 'transport', desc: 'World\'s steepest cogwheel railway departs here' },
        { lat: 46.9794, lng: 8.2521, label: 'Pilatus Kulm (2,132m)', num: 3, cat: 'photo', desc: '360° Alpine panorama, sea of clouds photography' },
        { lat: 47.0131, lng: 8.2644, label: 'Kriens Gondola (Dragon Ride)', num: 4, cat: 'transport', desc: 'Glass gondola return with aerial lake photography' },
        { lat: 47.0583, lng: 8.3091, label: 'Lion Monument (Löwendenkmal)', num: 5, cat: 'photo', desc: 'Mark Twain\'s "saddest piece of rock" — dusk reflection' },
        { lat: 47.0584, lng: 8.3094, label: 'Bourbaki Panorama', num: 6, cat: 'attraction', desc: 'Near the Lion Monument — impressive 1881 circular painting' }
      ]
    },
    {
      num: 6,
      neighborhoods: 'Lucerne · Mount Rigi · Musegg Wall',
      title: 'Queen of the Mountains — Rigi Sunrise',
      description: 'Rigi is the oldest mountain railway in Europe and arguably the most rewarding: stand above the cloud layer at sunrise surrounded by a sea of mist with 14 lakes visible below. Afternoon brings Lucerne\'s hidden medieval walls and a farewell lakeside golden hour.',
      timeBlocks: [
        {
          label: 'Very Early Morning',
          activities: [
            { title: '📸 Rigi Sunrise (Pre-Booked)', description: 'Take the early morning ferry to Vitznau (6:10am from Lucerne) then the cogwheel railway to Rigi Kulm (1,798m). Arrive before sunrise for the famous spectacle: 14 lakes visible simultaneously, Alps to the south, Black Forest to the north. In late April, morning mist often creates a "cloud inversion" — one of photography\'s most sought-after conditions.', details: ['🚢 Ferry Lucerne → Vitznau: 6:10am (Swiss Travel Pass)', '🚞 Cogwheel Vitznau → Rigi Kulm: 35 min (Swiss Travel Pass)', '📸 Bring telephoto for distant Alpine peaks (Jungfrau visible on clear days)', '🌅 Sunrise April 26: ~6:20am — arrive by 6:15am', '💡 Book via rigi.ch for the "Sunrise Package" with breakfast included'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: 'Rigi Kulm & Trails', description: 'After sunrise, walk the easy circular trail around the summit (45 min) and then take the Rigi-Scheidegg branch railway down halfway, then walk the "Rigi Classic" trail through flower meadows back to Vitznau. The lake views are postcard perfect.', details: ['📸 Best mid-morning shot: Vitznaustock trail looking back at Rigi Kulm with Lake Lucerne', '🥾 Trail from Rigi-Scheidegg to Vitznau: 2 hours, moderate', '🚢 Return ferry Vitznau → Lucerne at your leisure'] }
          ],
          meals: [
            { type: '🍽️ Breakfast', name: 'Rigi Kulm Hotel Restaurant', description: 'Breakfast above the clouds — fresh bread, Swiss cheese, local yogurt and jam. The terrace overlooks Lake Lucerne and the sunrise panorama. Worth every franc.', meta: '€€ · Rigi Kulm summit · Sunrise breakfast package' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 Musegg Wall — Lucerne\'s Secret Viewpoint', description: 'The 870m-long medieval town wall (1386) is one of the most photogenic and overlooked spots in Lucerne. Climb the Zyt Tower (Zeitturm) for a free elevated view of the whole city — the bridge, lake, and mountains framed perfectly.', details: ['📍 Free entry, open April-November', '📸 Zyt Tower gives the best overhead Kapellbrücke angle', '🕐 Allow 1 hour along the full wall walk'] },
            { title: 'Spreuerbrücke & Death Dance Paintings', description: 'The older of Lucerne\'s two covered bridges (1408) contains macabre yet beautiful 17th-century "Dance of Death" (Totentanz) paintings. Photographically stunning with its floral boxes and water wheel.', details: ['📍 Free, western end of the old town', '📸 Shoot from downstream to capture both bridge and water wheel', '💡 Much less crowded than Kapellbrücke'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 Lake Lucerne Golden Hour & Farewell', description: 'Your last Lucerne evening — walk the lakeside promenade from the Schweizerhofquai all the way to the National Quay. The Kapellbrücke glows warmly at golden hour while swans drift past the KKL\'s steel canopy. One of the great European urban photography moments.', details: ['📸 Wide-angle from Schweizerhofquai at sunset for lake panorama', '💡 Spring evenings are warm — perfect terrace dining'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Old Swiss House', description: 'A Lucerne classic since 1931. The Wiener Schnitzel here is prepared tableside and is perhaps the best in Switzerland. Wood-paneled rooms hung with antiques and original Dali sculptures. Reserve well ahead.', meta: '€€€ · Löwenplatz 4 · Swiss classics · Tableside preparation' }
          ],
          tips: [{ type: 'tip', text: '📦 Pack for mountain life tomorrow — Wengen is car-free at 1,274m. You\'ll leave your luggage lighter. Consider storing the non-essentials at Interlaken if needed.' }]
        }
      ],
      mapPins: [
        { lat: 47.0461, lng: 8.3170, label: 'Lucerne Ferry Pier (Rigi)', num: 1, cat: 'transport', desc: 'Early ferry 6:10am → Vitznau for sunrise' },
        { lat: 47.0561, lng: 8.4922, label: 'Rigi Kulm (1,798m)', num: 2, cat: 'photo', desc: 'Queen of the Alps — 14 lakes visible, cloud inversion photography' },
        { lat: 47.0554, lng: 8.3082, label: 'Musegg Wall & Zyt Tower', num: 3, cat: 'photo', desc: 'Elevated medieval wall — best aerial view of Chapel Bridge' },
        { lat: 47.0502, lng: 8.3055, label: 'Spreuerbrücke', num: 4, cat: 'photo', desc: 'Death Dance paintings, water wheel, less crowded than Kapellbrücke' },
        { lat: 47.0480, lng: 8.3130, label: 'Schweizerhofquai Promenade', num: 5, cat: 'photo', desc: 'Lakeside golden hour walk — swans, KKL, Chapel Bridge glow' }
      ]
    },

    // ===================== WENGEN: DAYS 7-11 =====================
    {
      num: 7,
      neighborhoods: 'Lucerne → Interlaken → Lauterbrunnen · Wengen',
      title: 'Into the Jungfrau Region — Lauterbrunnen Valley',
      description: 'The train journey from Lucerne to Wengen passes through Interlaken and then descends into the most dramatic valley in the Alps: Lauterbrunnen, with 72 waterfalls cascading from 300m cliffs. Then the rack railway climbs up to Wengen — your car-free mountain home for five days.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Train to Interlaken via Bern', description: 'The morning IC8 train from Lucerne reaches Interlaken Ost via Bern (approximately 2 hours). The Lake Brienz section of the route is phenomenally scenic — sit on the right side.', details: ['🚆 Lucerne → Bern → Interlaken Ost: ~2h, every hour', '📸 Right-side seat on the final stretch for Lake Brienz', '🎫 Swiss Travel Pass covers the whole journey'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Taverne Restaurant, Lauterbrunnen', description: 'Refuel after arriving in the valley. Classic Swiss lunch — Rösti, bratwurst, or a hearty soup before the afternoon\'s photography mission.', meta: '€ · Lauterbrunnen village · Swiss comfort food' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 Lauterbrunnen Valley — 72 Waterfalls', description: 'The Lauterbrunnen Valley is UNESCO-protected and arguably the most dramatic landscape in Switzerland. Sheer 300m cliff walls on both sides, with 72 waterfalls spilling over the edges. The Staubbach Falls (297m, Europe\'s tallest free-falling waterfall) is directly in the village — photogenic from every angle.', details: ['📸 Walk to the Staubbach viewpoint platform (5 min from village)', '📸 Shoot the valley from the main road with telephoto for full cliff scale', '📸 Hike up behind Staubbach Falls into the grotto (10 min) for a unique angle', '💡 Spring runoff means the falls are at their most powerful'] },
            { title: 'Trümmelbach Falls Preview', description: 'The Trümmelbach Falls are 10 glacier waterfalls inside the mountain — accessible by tunnel elevator. Save the full visit for Day 11, but stop at the entrance to see the exterior cascades in the evening light.', details: ['📍 3km from Lauterbrunnen village, regular bus service', '💡 Visit inside on Day 11 for the full experience'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '🚞 Rack Railway to Wengen + First Jungfrau Views', description: 'Board the BOB rack railway from Lauterbrunnen to Wengen (16 min, 400m vertical climb). Wengen is car-free — all transport is on foot or by electric vehicle. As you emerge from the forest, the Jungfrau (4,158m) suddenly fills the entire southern horizon. Your first look will stop you in your tracks.', details: ['🚆 Trains every 30 minutes, last train 10:30pm', '📸 Shoot immediately from the station platform — the view is extraordinary', '🎫 Swiss Travel Pass covers this rack railway'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Hirschen, Wengen', description: 'Traditional Bernese Oberland cuisine in a cozy chalet-style restaurant. Try the cheese fondue with local Appenzeller and Gruyère — mandatory on your first mountain evening. The view of the Jungfrau from the terrace is priceless.', meta: '€€ · Wengen village center · Fondue & raclette' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.6831, lng: 7.8632, label: 'Interlaken Ost Station', num: 1, cat: 'transport', desc: 'Hub for Jungfrau region trains — connect to BOB railway' },
        { lat: 46.5931, lng: 7.9089, label: 'Lauterbrunnen', num: 2, cat: 'photo', desc: 'Valley of 72 waterfalls — UNESCO, 300m cliff walls' },
        { lat: 46.5930, lng: 7.9094, label: 'Staubbach Falls (297m)', num: 3, cat: 'photo', desc: 'Europe\'s tallest free-falling waterfall — viewpoint + grotto walk' },
        { lat: 46.5666, lng: 7.9119, label: 'Trümmelbach Falls (exterior)', num: 4, cat: 'attraction', desc: 'Preview spot — full visit on Day 11' },
        { lat: 46.6082, lng: 7.9228, label: 'Wengen Village', num: 5, cat: 'photo', desc: 'Car-free alpine village at 1,274m — Jungfrau views from station' },
        { lat: 46.6072, lng: 7.9224, label: 'Restaurant Hirschen', num: 6, cat: 'food', desc: 'Best fondue in Wengen with Jungfrau terrace view' }
      ]
    },
    {
      num: 8,
      neighborhoods: 'Wengen · Männlichen · Kleine Scheidegg',
      title: 'The Greatest Ridge Walk in Europe',
      description: 'The Männlichen ridge walk to Kleine Scheidegg (2.5 hours, gentle gradient) is Switzerland\'s most spectacular moderate hike — the entire Jungfrau massif on one side, the Grindelwald valley on the other, with the Eiger North Face glowering above you the whole way.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Wengen Dawn Photography', description: 'Before the cable car opens, the village comes alive in the early morning light. The Jungfrau, Mönch and Eiger glow with alpenglow (pink/red light before sunrise hits the valleys). Shoot from the main street looking south — no crowds, perfect light.', details: ['📸 Alpenglow hits the Jungfrau ~15 min before sunrise', '📸 Walk down toward Wengernalp for the iconic three-peaks framing', '🕐 Best window: 5:45-6:30am in late April'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: '🚡 Cable Car to Männlichen (2,343m)', description: 'The Wengen-Männlichen gondola rises 1,000m in 30 minutes. Exit at the top station and immediately you\'re hit with views in every direction: Jungfrau massif to the south, Grindelwald valley and glacier below, Wetterhorn to the east. The Royal Station at Männlichen is worth exploring.', details: ['🎫 CHF 48 return, partially covered by Swiss Pass', '📸 From the top station: wide angle south for the full massif', '💡 Arrive by 9am before any afternoon haze builds'] },
            { title: '🥾 📸 Männlichen → Kleine Scheidegg Ridge Walk (2.5h)', description: 'The flagship hike of the Jungfrau region. Follow the ridge south, keeping the Jungfrau, Mönch, and Eiger to your left. The Eiger North Face (1,800m of vertical rock) is your constant companion. Multiple rest/photo stops. Arrive at Kleine Scheidegg for lunch with the greatest mountain view in Switzerland.', details: ['🥾 5km, 340m descent, 2-2.5 hours, easy-moderate', '📸 Best photo stops: Km 1 (Männlichen summit cross), Km 2.5 (Eiger North Face close-up), Km 4 (Scheidegg panorama)', '💡 The trail is snow-free from mid-April in most years'] }
          ]
        },
        {
          label: 'Midday',
          activities: [
            { title: '📸 Kleine Scheidegg (2,061m) — Photography Central', description: 'The mountain pass between Grindelwald and Lauterbrunnen has the most iconic Alpine views in the world — the complete Eiger-Mönch-Jungfrau trio. The railway station itself is historical (in many films). Spend time exploring the viewpoints in every direction.', details: ['📸 THE shot: From Scheidegg station platform with all three peaks', '📸 Use telephoto for Eiger North Face detail shots', '⏰ If time permits, take the cogwheel up to Eigergletscher for even better views'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Restaurant Bellevue des Alpes, Kleine Scheidegg', description: 'Historic hotel (1840) right at the pass. The terrace faces the Eiger North Face directly. Order the Bernese plate (meats, sauerkraut, Rösti) and eat with the greatest view in the Alps.', meta: '€€€ · Kleine Scheidegg · Historic mountain hotel · Reserve if possible' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '🚞 Cogwheel to Wengen via Wengernalp', description: 'Take the historic Wengernalp Railway back down to Wengen (25 min). The route passes through the Wengernalp meadows with wildflowers and a unique perspective back up at the three peaks. Slower than the gondola, more scenic.', details: ['🎫 Included in Swiss Travel Pass', '📸 Left-side seats for best Jungfrau angle on the descent'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Hotel Silberhorn Restaurant', description: 'Wengen\'s grande dame hotel with panoramic dining room. Outstanding raclette — Bernese Oberland cheese melted tableside onto potatoes, pickles and onions. The fondue chinoise is also spectacular.', meta: '€€ · Wengen · Raclette & fondue · Terrace view of Jungfrau' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.6082, lng: 7.9228, label: 'Wengen Dawn Photo Spot', num: 1, cat: 'photo', desc: 'Alpenglow on Jungfrau 15 min before sunrise — shoot from village center' },
        { lat: 46.6164, lng: 7.9312, label: 'Männlichen (2,343m)', num: 2, cat: 'photo', desc: '360° views — gondola top station, ridge walk start' },
        { lat: 46.5845, lng: 7.9612, label: 'Kleine Scheidegg (2,061m)', num: 3, cat: 'photo', desc: 'Iconic Eiger-Mönch-Jungfrau trio — most famous Alpine view' },
        { lat: 46.5810, lng: 7.9580, label: 'Eigergletscher Station', num: 4, cat: 'photo', desc: 'Even closer Eiger views — optional extension from Scheidegg' },
        { lat: 46.5924, lng: 7.9344, label: 'Wengernalp', num: 5, cat: 'attraction', desc: 'Wildflower meadows, unique three-peaks angle on cogwheel descent' },
        { lat: 46.6082, lng: 7.9228, label: 'Hotel Silberhorn', num: 6, cat: 'food', desc: 'Classic raclette with Jungfrau view' }
      ]
    },
    {
      num: 9,
      neighborhoods: 'Wengen · Jungfraujoch · Top of Europe',
      title: 'Jungfraujoch — Top of Europe (3,454m)',
      description: 'The highest railway station in Europe, built in 1912 through 7km of tunnel inside the Eiger and Mönch. Emerge at 3,454m onto a world of eternal snow, the 23km Aletsch Glacier, and an altitude that will make your heart pound. Clear May mornings often mean ice-crystal clarity.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚞 Journey to Jungfraujoch (reserve tickets!)', description: 'Board the cogwheel railway from Wengen to Kleine Scheidegg (25 min), then the Jungfrau Railway inside the mountain (45 min) to the summit station. The tunnel has two stops (Eigerwand and Eismeer) with window views into the sheer Eiger face and the glacier.', details: ['🎫 ~CHF 190/person from Wengen (discounted with Swiss Travel Pass)', 'BOOK IN ADVANCE at jungfrau.ch — sells out weeks ahead in May', '📸 Stop at Eigerwand window station — shoot straight down the North Face', '💡 Take the first train (7:35am from Wengen) to beat afternoon clouds'] },
            { title: '📸 Jungfraujoch Summit Photography', description: 'At the top, you have the Sphinx Observatory (free access), the Aletsch Glacier viewpoint, the Plateau (snowfield), and the Ice Palace (carved inside the glacier). Clear mornings give unrestricted views to the Matterhorn, Monte Rosa, and even Mont Blanc.', details: ['📸 Sphinx terrace: shoot Aletsch Glacier curving away into infinity', '📸 Sunrise alpenglow on the Silberhorn peak if you\'re there early', '📸 Plateau snowfield for "Ice Age" landscape shots', '❄️ Dress warmly — it\'s -5°C to -15°C and windy at the top', '🌅 First train gets you there for 9am golden light on the glacier'] }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            { title: 'Ice Palace & Glacier Experience', description: 'The Ice Palace is carved 30m inside the Aletsch Glacier. Sculptures, ice tunnels, and the eerie blue light of the glacier interior make for extraordinary photos. Bring a wide-angle lens.', details: ['🎟️ Included with Jungfraujoch ticket', '📸 Use long exposure to capture the blue ice glow', '🥾 The "Great Aletsch Glacier" trail from here (summer only) is one of the world\'s great hikes'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Crystal Restaurant, Jungfraujoch', description: 'Dining at 3,454m with panoramic windows onto the glacier. Self-service but with spectacular views. Try the Swiss cheese soup and the warm bread — you\'ll need the calories at altitude.', meta: '€€ · Top of Europe station · Buffet restaurant' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Return & Rest in Wengen', description: 'Return to Wengen by early afternoon and rest — altitude (even 1,300m) will tire you more than expected after 3,454m. Take a gentle afternoon walk through Wengen\'s flower-filled lanes toward the Männlichen viewpoint area.', details: ['💡 Altitude sickness is rare at 1,300m but rest is good after Jungfraujoch', '📸 Wengen village lanes with the Jungfrau behind — classic Switzerland'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Arvenstube (Hotel Beausite)', description: 'Intimate arven-paneled dining room with creative Bernese cuisine. The local lamb with mountain herbs and the handmade pasta are exceptional. One of Wengen\'s finest tables.', meta: '€€€ · Wengen · Contemporary Alpine cuisine · Reserve ahead' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.5845, lng: 7.9612, label: 'Kleine Scheidegg (Jungfraujoch departure)', num: 1, cat: 'transport', desc: 'Switch to Jungfrau Railway here for the summit' },
        { lat: 46.5537, lng: 7.9764, label: 'Eigerwand (tunnel window)', num: 2, cat: 'photo', desc: 'Window into the Eiger North Face — vertigo-inducing photo' },
        { lat: 46.5473, lng: 7.9854, label: 'Jungfraujoch (3,454m)', num: 3, cat: 'photo', desc: 'Top of Europe — Aletsch Glacier, Sphinx Observatory, Ice Palace' },
        { lat: 46.5456, lng: 7.9836, label: 'Sphinx Observatory Terrace', num: 4, cat: 'photo', desc: 'Best glacier panorama photo point — get here early' },
        { lat: 46.5468, lng: 7.9847, label: 'Ice Palace', num: 5, cat: 'attraction', desc: 'Carved 30m inside the Aletsch Glacier — blue ice photography' },
        { lat: 46.6082, lng: 7.9228, label: 'Wengen Village', num: 6, cat: 'attraction', desc: 'Return and rest — wildflower lane walks in afternoon' }
      ]
    },
    {
      num: 10,
      neighborhoods: 'Wengen · Grindelwald · First · Bachalpsee',
      title: 'Grindelwald First & the Bachalpsee Mirror',
      description: 'The other side of the Scheidegg pass is Grindelwald — a larger, livelier resort with the Grindelwald First cable car reaching 2,168m. The 45-minute walk to Bachalpsee (2,265m) offers some of the most extraordinary Alpine lake reflections in Europe, rivaling anything in Switzerland.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚞 Train from Wengen to Grindelwald', description: 'Take the cogwheel railway over Kleine Scheidegg to Grindelwald (45 min). The journey over the pass gives glorious reverse views back at the Eiger. Grindelwald village has more shops, cafés, and a livelier energy than Wengen.', details: ['🚆 Via Kleine Scheidegg — Swiss Travel Pass', '📸 Look back at the Eiger from Scheidegg for a different angle', '🕐 Aim for the 8:45am train to be at First by 10am'] },
            { title: '🚡 📸 Grindelwald First (2,168m)', description: 'The 25-minute gondola from Grindelwald to First passes through larch forests and emerges into open Alpine meadows with the Wetterhorn and Schreckhorn dominating the view. The First Cliff Walk by Tissot is an optional 45-min via ferrata-style walkway along the cliff edge.', details: ['🎫 ~CHF 72 return (partial Swiss Pass discount)', '📸 From the terrace: panorama of Grindelwald valley, Eiger, and Wetterhorn', '🥾 First Cliff Walk: moderate, some exposed sections, stunning views'] }
          ]
        },
        {
          label: 'Late Morning — Afternoon',
          activities: [
            { title: '🥾 📸 Hike to Bachalpsee (2,265m)', description: 'The 45-minute walk from First to Bachalpsee is the most rewarding easy hike in the Jungfrau region. The two alpine lakes perfectly reflect the Schreckhorn (4,078m) and Finsteraarhorn (4,274m) on calm mornings. This is one of the most photographed spots in all of Switzerland — and the reflection shots are extraordinary.', details: ['📸 THE reflection shot: east shore of Bachalpsee, morning light', '📸 Use a polarizing filter to eliminate surface glare', '🥾 3km round trip, 100m ascent, very manageable', '💡 Arrive by 10am for best calm-water reflections before afternoon winds'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'First Mountain Restaurant', description: 'Mountain lunch with valley and glacier views. The Bündnerfleisch (air-dried beef) with Alpkäse (alpine cheese) platter is perfect for fueling the afternoon. Great outdoor terrace.', meta: '€€ · Grindelwald First · Mountain classics' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '🛷 First Flyer & Fun Rides (Optional)', description: 'If you\'re up for adventure, the First Flyer zipline reaches 84km/h over the valley. The Trottibike (mountain scooter) ride back down to Grindelwald is exhilarating and fast.', details: ['🎫 First Flyer: ~CHF 29/person', '🎫 Trottibike: ~CHF 18/person', '📸 Shoot the valley from the zipline launch point'] },
            { title: 'Glacier Canyon (Gletscherschlucht)', description: 'On the walk back through Grindelwald, the Gletscherschlucht is a narrow gorge carved by the meltwater of the Upper Grindelwald Glacier — dramatic rock formations and turquoise water. Great photographs.', details: ['🎫 ~CHF 9 adult', '📸 Narrow canyon with layered rock strata — fascinating geology shots'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Return to Wengen', description: 'Take the cogwheel back over Scheidegg to Wengen. Evening in Wengen is peaceful — the day-trippers have gone and the village belongs to the mountain again.', details: ['📸 Wengen at dusk: shoot the village with the lit Jungfrau behind'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Jungfrau, Wengen', description: 'Reliably excellent Alpine bistro — the fondue bourguignonne (hot oil fondue with beef) for two is the signature dish. Lively atmosphere with hikers and ski season survivors.', meta: '€€ · Wengen village · Fondue & grills' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.6241, lng: 8.0413, label: 'Grindelwald Village', num: 1, cat: 'attraction', desc: 'Larger resort village — more shops, cafés, livelier energy' },
        { lat: 46.6382, lng: 8.0476, label: 'Grindelwald First (2,168m)', num: 2, cat: 'photo', desc: 'Cable car top — Wetterhorn panorama, Cliff Walk' },
        { lat: 46.6462, lng: 8.0584, label: 'Bachalpsee (2,265m)', num: 3, cat: 'photo', desc: 'THE reflection shot — Schreckhorn mirrored in alpine lakes' },
        { lat: 46.6158, lng: 8.0363, label: 'Gletscherschlucht', num: 4, cat: 'attraction', desc: 'Glacier gorge with turquoise water and layered rock' },
        { lat: 46.6153, lng: 8.0341, label: 'First Flyer Launch Point', num: 5, cat: 'attraction', desc: 'Zipline 84km/h over the valley — optional adventure' }
      ]
    },
    {
      num: 11,
      neighborhoods: 'Wengen · Trümmelbach Falls · Mürren · Lauterbrunnen',
      title: 'Waterfalls Inside the Mountain & Mürren',
      description: 'Your final Wengen day explores two unmissable spots: Trümmelbach Falls (ten glacier waterfalls thundering inside a mountain, accessible by tunnel elevator) and Mürren (another car-free village clinging to cliffs opposite Wengen with arguably even more dramatic Jungfrau views).',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Final Wengen Sunrise & Village Farewell', description: 'One last dawn photography session in Wengen. Walk the path toward Wengernalp for the classic "three peaks + meadow" composition that has appeared on more Swiss calendars than any other image. Wildflowers bloom in the meadows from mid-May.', details: ['📸 Walk 15 min south of village toward Wengernalp for meadow foreground', '📸 Golden alpenglow hits the peaks before sunrise in the valley', '🕐 5:45-7am for best light'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: '📸 Trümmelbach Falls — Waterfalls Inside a Mountain', description: 'Ten UNESCO-listed glacier waterfalls that carry the meltwater of the Jungfrau, Mönch, and Eiger — up to 20,000 liters per second at peak flow. The tunnel elevator takes you inside the mountain where the roar is deafening and the light is extraordinary. One of Switzerland\'s most unique photography locations.', details: ['🎫 ~CHF 14 adult (Swiss Pass partial discount)', '📸 Long exposures of the rushing water in the tunnel', '📸 External cascade shots from the valley floor', '💡 Take the full walk up through all 10 levels — allow 45-60 min'] }
          ]
        },
        {
          label: 'Midday',
          activities: [
            { title: '🚡 Cable Car to Grütschalp → Train to Mürren', description: 'From Lauterbrunnen, take the cable car to Grütschalp then the cliff railway to Mürren (total 30 min). Mürren at 1,650m is car-free and has one of the most dramatic mountain settings in the Alps — the Eiger, Mönch, and Jungfrau face you at eye level across the valley.', details: ['🎫 Swiss Travel Pass', '📸 The Mürren platform when you arrive gives an immediate jaw-dropping view across the valley', '💡 Mürren is less visited than Wengen — noticeably quieter'] },
            { title: '📸 Mürren Photography & Allmendhubel', description: 'The Allmendhubel funicular from Mürren rises another 200m to a wildflower meadow with an even closer view of the Eiger. The "Flower Trail" (2 hours, marked) through summer wildflowers with the Jungfrau behind is extraordinary. Mürren village itself is beautifully unspoiled.', details: ['🎫 Allmendhubel funicular: ~CHF 10', '📸 From Allmendhubel: the three peaks are almost at eye level', '📸 Mürren village lanes with geranium boxes — classic Swiss postcard'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Eiger Guesthouse Restaurant, Mürren', description: 'The classic British skiers\' haunt (the Eiger Guesthouse has been here since the Mürren pioneer days). Great burgers, soup, and hot chocolate on the terrace with a perfect Eiger North Face view.', meta: '€€ · Mürren · International & Swiss' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Return to Wengen, Pack for Zermatt', description: 'Return to Wengen for final packing. The train to Zermatt tomorrow is a 3-hour journey via Interlaken and Visp — one of Switzerland\'s most scenic rail routes.', details: ['📸 Last Jungfrau photos from your hotel window or terrace', '💡 Store non-essential luggage if needed — Zermatt also has luggage storage'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Berghaus Männlichen', description: 'For a special farewell, take the evening gondola up to Männlichen for dinner at the summit restaurant. Watch the Jungfrau turn pink with alpenglow from 2,343m with a glass of Valais wine.', meta: '€€€ · Männlichen summit · Reserve for evening gondola time' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.5738, lng: 7.9248, label: 'Trümmelbach Falls', num: 1, cat: 'photo', desc: '10 glacier waterfalls inside mountain — tunnel elevator, UNESCO' },
        { lat: 46.5564, lng: 7.8934, label: 'Mürren Village (1,650m)', num: 2, cat: 'photo', desc: 'Car-free cliff village — eye-level Eiger, Mönch, Jungfrau' },
        { lat: 46.5601, lng: 7.8911, label: 'Allmendhubel (1,907m)', num: 3, cat: 'photo', desc: 'Wildflower meadows + three peaks at eye level' },
        { lat: 46.5920, lng: 7.9070, label: 'Lauterbrunnen Cable Car', num: 4, cat: 'transport', desc: 'To Grütschalp for Mürren connection' },
        { lat: 46.6164, lng: 7.9312, label: 'Männlichen (evening gondola)', num: 5, cat: 'food', desc: 'Summit dinner with alpenglow on Jungfrau' }
      ]
    },

    // ===================== ZERMATT: DAYS 12-14 =====================
    {
      num: 12,
      neighborhoods: 'Wengen → Interlaken → Visp → Zermatt',
      title: 'Arrival in Zermatt — First Matterhorn',
      description: 'The train journey to Zermatt is a journey into legend. The final approach up the Matter Valley, as the Matterhorn gradually reveals itself above the forest, is one of the most emotional arrivals in travel. Zermatt is car-free — electric taxis only — and the Matterhorn dominates every view.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚆 Train to Zermatt (3 hours scenic)', description: 'Wengen → Interlaken Ost → Brig/Visp → Zermatt. The Lötschberg section through the Valais (Rhône valley) is dramatic. As you enter Täsch (last car-accessible town), leave all vehicles behind. Transfer to the Matterhorn Gotthard Railway for the final 12km to Zermatt.', details: ['🚆 Full journey ~3h with one change at Visp', '🎫 Swiss Travel Pass covers everything', '📸 Right-side seat from Visp to Zermatt for Matter Valley views'] }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 First Matterhorn Views — Arrival Photography', description: 'As the train pulls into Zermatt station, step out and look south. The Matterhorn\'s perfect pyramid fills the sky. Walk through the village immediately toward the church — the classic "church spire in foreground, Matterhorn behind" shot is your first trophy.', details: ['📸 Churchyard angle: Zermatt cemetery chapel + Matterhorn', '📸 Main street (Bahnhofstrasse) looking south', '💡 The "golden age" for early afternoon: 2-4pm light hits the west face'] },
            { title: '📸 Hike to Stellisee (One Hour Above Village)', description: 'Don\'t wait — get to Stellisee this afternoon if you arrive by 2pm. This small alpine lake at 2,537m is one of the world\'s most photographed photography spots: the Matterhorn reflected perfectly in a still pool. The hour-long hike from the village passes through larch forests.', details: ['📸 THE shot: Matterhorn south face reflected in Stellisee', '📸 Shoot from both the east and north shores for different compositions', '🥾 Trail from Zermatt: 1 hour, 600m elevation gain via Sunnegga', '💡 Afternoon reflections: still water most likely before 4pm'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Explore Zermatt Village', description: 'Wander the vehicle-free village. The traditional Heustation (hay barns on stilts with stone bases) are architecturally unique to the Valais. The small Matterhorn Museum (Zermatlantis) tells the story of the first ascent and the famous 1865 tragedy.', details: ['🎟️ Matterhorn Museum: CHF 12', '📸 The raised hay barns are unique photo subjects', '💡 The village is most atmospheric after the day-trippers leave (after 5pm)'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Zum See', description: 'Hidden in the woods 30 minutes walk from the village (or take a taxi), Zum See is one of Switzerland\'s great restaurants — a converted Alpine hut serving local trout, wild game, and the region\'s finest raclette. Book weeks ahead. Magical in every season.', meta: '€€€ · 15 min walk from village · Reserve weeks ahead · One of Switzerland\'s best' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.0201, lng: 7.7491, label: 'Zermatt Station', num: 1, cat: 'transport', desc: 'Arrive by MGBahn — Matterhorn immediately visible' },
        { lat: 46.0197, lng: 7.7487, label: 'Zermatt Church & Matterhorn View', num: 2, cat: 'photo', desc: 'Classic: church spire + Matterhorn — first arrival shot' },
        { lat: 46.0012, lng: 7.7534, label: 'Stellisee (2,537m)', num: 3, cat: 'photo', desc: 'World-famous Matterhorn reflection — arrive afternoon for calm water' },
        { lat: 46.0205, lng: 7.7497, label: 'Matterhorn Museum (Zermatlantis)', num: 4, cat: 'attraction', desc: '1865 first ascent story and the tragedy — fascinating exhibits' },
        { lat: 46.0060, lng: 7.7230, label: 'Restaurant Zum See', num: 5, cat: 'food', desc: 'Alpine hut fine dining — one of Switzerland\'s great restaurants' }
      ]
    },
    {
      num: 13,
      neighborhoods: 'Zermatt · Gornergrat · Riffelsee · Riffelberg',
      title: 'Gornergrat — The Grand Alpine Observatory',
      description: 'The Gornergrat Bahn (1898) is one of Switzerland\'s oldest mountain railways, climbing to 3,089m. From the summit, you overlook the Monte Rosa massif (Switzerland\'s highest), the Gorner Glacier, 29 of the Alps\' highest peaks — and most importantly, a Matterhorn view that rivals Jungfraujoch.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Sunrise at Gornergrat (Reserve!)', description: 'Take the first Gornergrat Bahn from Zermatt (6:48am) to reach the 3,089m summit before 8am. The Matterhorn\'s east face glows spectacular orange-red in the morning alpenglow — considered by many the best single Alpine photography moment in Switzerland.', details: ['🎫 ~CHF 50 one way, discounted with Swiss Pass', '📸 From the Kulmhotel Gornergrat terrace: Matterhorn alpenglow + Monte Rosa panorama', '🌅 Alpenglow hits the Matterhorn approximately 15-20 min before sunrise hits the valley', '💡 The Kulmhotel restaurant serves early breakfast — book the night before'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: '📸 Gornergrat Observatory Terrace', description: 'The observatory sits on the summit ridge above the Gorner Glacier — the second-largest glacier in the Alps. On clear days, you can see Monte Rosa (4,634m), Dom (4,545m), Lyskamm, and Castor & Pollux. The Matterhorn stands slightly apart, pyramid-perfect.', details: ['📸 Full panorama from the observatory roof (ask permission)', '📸 Gorner Glacier wide-angle — a river of ice 14km long', '📸 Telephoto the Matterhorn — at this distance and angle it looks impossibly sculptural', '🔭 The Swiss telescope is sometimes open to the public'] },
            { title: 'Walk from Gornergrat to Riffelsee', description: 'The trail from Gornergrat down toward Riffelalp passes the famous Riffelsee and Riffelboden lakes (2,757m) — where the Matterhorn reflects in two small glacial lakes surrounded by snowfields. Different from Stellisee — here the reflection includes Monte Rosa too.', details: ['🥾 Gornergrat → Riffelsee: 1.5 hours, 300m descent, spectacular', '📸 Riffelsee: The Matterhorn reflection is more dramatic here — steeper mountain angle', '📸 Shoot in early morning when the water is still'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Restaurant Riffelberg', description: 'Lunch at 2,582m after the trail down. The terrace faces the Matterhorn directly and the lamb from local Valais flocks is exceptional. The Valais wine selection includes wines from vineyards at 1,000m — unique in Europe.', meta: '€€€ · Riffelberg station · Valais lamb & mountain cuisine' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '🚞 Return via Cogwheel & Afternoon Recovery', description: 'Take the cogwheel back to Zermatt. Spend the afternoon exploring the village\'s quieter streets: the old Zmutt quarter (pre-tourist hamlet), the Bahnhofstrasse shops, and the excellent Biner Sport/Bayard for alpine gear browsing.', details: ['📸 Zmutt quarter: ancient stone houses, chapel, no tourists', '📸 Village photography is best 4-6pm when light falls golden on the streets'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Chez Vrony, Findeln', description: 'Take the Sunnegga cableway up to Findeln hamlet (2,000m) for Zermatt\'s most celebrated restaurant. Chez Vrony is a converted 17th-century barn serving local lamb, house-cured meats, and the finest fondue in the region — with a direct Matterhorn terrace view. The descent back to Zermatt is by foot (45 min, marked trail) or last gondola.', meta: '€€€ · Findeln hamlet · Reserve weeks ahead · Matterhorn terrace view' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.0201, lng: 7.7491, label: 'Zermatt (Gornergrat Bahn)', num: 1, cat: 'transport', desc: 'First train 6:48am — reach summit before 8am for alpenglow' },
        { lat: 45.9833, lng: 7.7857, label: 'Gornergrat (3,089m)', num: 2, cat: 'photo', desc: 'Matterhorn alpenglow + Monte Rosa panorama — summit observatory' },
        { lat: 45.9870, lng: 7.7578, label: 'Gorner Glacier viewpoint', num: 3, cat: 'photo', desc: 'Second-largest glacier in Alps — wide-angle shots' },
        { lat: 45.9788, lng: 7.7347, label: 'Riffelsee (2,757m)', num: 4, cat: 'photo', desc: 'Matterhorn + Monte Rosa reflection — different from Stellisee angle' },
        { lat: 46.0059, lng: 7.7624, label: 'Restaurant Riffelberg', num: 5, cat: 'food', desc: 'Valais lamb lunch at 2,582m with Matterhorn terrace' },
        { lat: 46.0109, lng: 7.7618, label: 'Findeln / Chez Vrony', num: 6, cat: 'food', desc: '17th-century barn restaurant — Zermatt\'s most celebrated table' }
      ]
    },
    {
      num: 14,
      neighborhoods: 'Zermatt · Matterhorn Glacier Paradise · Schwarzsee · Stellisee',
      title: 'Matterhorn Glacier Paradise & Sunset Reflections',
      description: 'Your final Zermatt day goes highest — the cable car to Matterhorn Glacier Paradise (3,883m, highest cable car station in the Alps) for a perspective of the Matterhorn you\'ve never imagined. Afternoon returns to the village and the beloved Stellisee for the ultimate golden-hour reflection.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Dawn Matterhorn from Zermatt Village', description: 'Your last dawn in Zermatt. Walk to the bridge over the Matter Vispa river at the south end of the village — the classic "Matterhorn behind the bridge" shot in blue predawn light, with a long exposure of the rushing meltwater below.', details: ['📸 Long exposure: 30-60 seconds for silky water + lit Matterhorn', '📸 Also shoot from the cemetery chapel for the spire-and-peak composition in first light', '🕐 Best 5:30-7am'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: '🚡 Cable Car to Matterhorn Glacier Paradise (3,883m)', description: 'The four-stage cable car from Zermatt via Furi, Trockener Steg, and Klein Matterhorn reaches the highest point accessible by cable car in the Alps. You are literally at the same altitude as Everest Base Camp. The Matterhorn towers above you from a completely unexpected angle — you\'re looking UP at it.', details: ['🎫 ~CHF 100 return (significant Swiss Pass discount)', '📸 At this altitude, you shoot DOWN onto the glacier — the angle is psychedelic', '📸 From the summit terrace: 14 countries visible on clear days', '❄️ Always -10°C to -20°C — full winter gear required', '💡 Book first gondola of the day for clearest skies'] },
            { title: '📸 Glacier Ice Palace at 3,883m', description: 'Unlike Jungfraujoch, this ice palace is carved much higher and in a different glacier system. The blue ice here has been compressed for centuries. The tunnel exit on the Italian side looks down on Cervinia — the Italian Matterhorn resort.', details: ['📸 Shoot through the tunnel opening to Italy for an unexpected "portal" composition', '📸 Wide angle in the ice tunnels with natural blue light'] }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 Schwarzsee — Matterhorn Up Close', description: 'Descend via cable car to Schwarzsee (2,583m) — a small black lake with the Matterhorn reflected at its closest photographable proximity. The little Schwarzsee chapel (1787) adds a human element. You\'re directly below the south face.', details: ['📸 Schwarzsee reflection: the Matterhorn fills the entire frame', '📸 Chapel in foreground, pyramid above — perfect composition', '🥾 Hike from Schwarzsee down to Zermatt via Staffel (2 hours, moderate)'] },
            { title: '📸 Stellisee Golden Hour — The Greatest Shot', description: 'Return to Stellisee for the last time. Late afternoon and golden hour produce the most saturated reflection colors of the entire trip. In late April/early May, the peaks may still have heavy snow giving the reflection an extra punch. Stay until the lake turns lavender in the dusk.', details: ['📸 Arrive 5pm for afternoon gold; stay for blue-hour purple reflections', '📸 Shoot with wide-angle for sky + peaks + reflection in one frame', '💡 This is your final great photography window — don\'t rush it'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Schwarzsee Mountain Restaurant', description: 'Lunch with the Matterhorn at its most imposing directly above. The Walliser Teller (Valais plate) with rye bread, dried meats, Raclette cheese, and pickles is the essential mountain lunch.', meta: '€€ · Schwarzsee (2,583m) · Alpine classics' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant Schäferstube (Hotel Alex)', description: 'Zermatt\'s finest wine cellar with one of Switzerland\'s most impressive Valais wine selections. The raclette is made with 8 different mountain cheeses. An appropriately grand farewell dinner for your Matterhorn days.', meta: '€€€ · Hotel Alex · Exceptional wine list · Reserve ahead' }
          ],
          tips: [{ type: 'tip', text: '📦 Pack tonight for Montreux. The train via Visp to Montreux takes about 2h30m — a scenic journey through the Rhône Valley with vineyard views on both sides.' }]
        }
      ],
      mapPins: [
        { lat: 45.9764, lng: 7.6586, label: 'Klein Matterhorn / Glacier Paradise (3,883m)', num: 1, cat: 'photo', desc: 'Highest cable car in Alps — shoot DOWN onto glacier, see Italy' },
        { lat: 45.9741, lng: 7.6840, label: 'Trockener Steg (cable car mid-station)', num: 2, cat: 'photo', desc: 'Best mid-station photography — Matterhorn from side angle' },
        { lat: 45.9914, lng: 7.7189, label: 'Schwarzsee (2,583m)', num: 3, cat: 'photo', desc: 'Matterhorn up close — chapel reflection in black lake' },
        { lat: 46.0012, lng: 7.7534, label: 'Stellisee (golden hour)', num: 4, cat: 'photo', desc: 'Final golden-hour reflection — stay until blue dusk' },
        { lat: 46.0022, lng: 7.7156, label: 'Zmutt Ancient Quarter', num: 5, cat: 'photo', desc: 'Pre-tourist hamlet — stone houses, chapel, no crowds' },
        { lat: 46.0201, lng: 7.7491, label: 'Hotel Alex / Schäferstube', num: 6, cat: 'food', desc: 'Zermatt\'s finest wine cellar — farewell Valais raclette dinner' }
      ]
    },

    // ===================== MONTREUX: DAYS 15-17 =====================
    {
      num: 15,
      neighborhoods: 'Zermatt → Montreux · Château de Chillon · Lakeside',
      title: 'Arrive Montreux — Riviera & the Castle',
      description: 'The train from Zermatt descends through the Rhône Valley into the Vaud canton and the legendary Swiss Riviera. Montreux sits between the Alps and Lake Geneva in a sheltered microclimate where palms grow beside the lake and vineyards cascade to the water\'s edge.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚆 Train Zermatt → Montreux (2h30m)', description: 'A spectacular journey through the Rhône Valley, passing vineyards and the Sion medieval hilltop castles. From Visp, the track follows the Rhône with the Alps reflected in its fast-moving waters.', details: ['🚆 Via Visp → Lausanne → Montreux (Swiss Travel Pass)', '📸 Left-side seat from Visp for vineyard-valley views', '💡 Consider the Glacier Express for this section — more scenic, needs reservation'] }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '📸 Château de Chillon', description: 'Situated on a rock island in Lake Geneva, Château de Chillon is Switzerland\'s most visited historic monument — and one of Europe\'s most beautifully sited castles. Lord Byron carved his name into a pillar in 1816 and wrote "The Prisoner of Chillon" here. The lakeside walk from Montreux to the castle (2km) is gorgeous, with the Alps reflected in the lake.', details: ['🎫 CHF 14.50 adult', '📸 Best exterior shot: From the lakeside 200m east of the castle', '📸 Internal courtyard with lake views through the arched windows', '📸 Reflection of castle in the lake from the access bridge', '🕐 Allow 1.5-2 hours inside'] },
            { title: 'Montreux Lakeside Promenade', description: 'The 3km flower-lined promenade from Château de Chillon back to Montreux passes statues, sculptures, and manicured gardens. The famous Freddie Mercury statue (6 months lived in Montreux) stands by the casino with his fist raised toward the Alps.', details: ['📸 Freddie Mercury statue with lakeside Alps behind', '📸 The long promenade with mountains reflected in the lake', '🌸 April-May blooms: tulips, cherry blossoms, and roses in the lakeside gardens'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 Montreux Jazz Murals & Golden Hour Lake', description: 'Montreux is famous for its Jazz Festival (July). The murals throughout the town feature legends from Miles Davis to BB King. At golden hour, the lake turns to gold with the Dents du Midi peaks reflected. The casino terrace is the best vantage point.', details: ['📸 Casino terrace: lake at golden hour', '📸 Jazz murals add urban color to city photography'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Le Palais Oriental, Montreux', description: 'Elegant lakeside Moroccan restaurant in a villa with terrace tables overlooking Lake Geneva. A surprisingly excellent restaurant in unexpected setting — the tajines and couscous are outstanding.', meta: '€€€ · Quai de Rive · Lakeside terrace · North African cuisine' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.4140, lng: 6.9277, label: 'Château de Chillon', num: 1, cat: 'photo', desc: 'Switzerland\'s most visited castle on a lake island — Byron connection' },
        { lat: 46.4328, lng: 6.9139, label: 'Freddie Mercury Statue', num: 2, cat: 'photo', desc: 'Fist raised toward the Alps — iconic Montreux photo' },
        { lat: 46.4333, lng: 6.9151, label: 'Montreux Lakeside Promenade', num: 3, cat: 'photo', desc: '3km flower-lined walk, mountains reflected in Lake Geneva' },
        { lat: 46.4339, lng: 6.9148, label: 'Montreux Casino Terrace', num: 4, cat: 'photo', desc: 'Golden hour lake reflection — best in town' },
        { lat: 46.4329, lng: 6.9151, label: 'Le Palais Oriental', num: 5, cat: 'food', desc: 'Lakeside Moroccan villa restaurant — excellent tajines' }
      ]
    },
    {
      num: 16,
      neighborhoods: 'Montreux · Lavaux Vineyards · Epesses · Rivaz',
      title: 'Lavaux — UNESCO Vineyards Above the Lake',
      description: 'The Lavaux wine region stretches 30km along Lake Geneva\'s north shore — a UNESCO World Heritage landscape of stone-terraced vineyards cascading from 800m altitude down to the water. Walking the trail through Epesses and Rivaz villages in late April is extraordinary: vines just leafing out, lake views, Alps reflected in the water below.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Morning: Château de Chillon Interior (if missed Day 15)', description: 'If you haven\'t done the full interior visit, morning hours are quieter. Otherwise, take a leisurely lakeside coffee and pastry morning in Montreux.', details: ['☕ Café du Marché in old Montreux for excellent croissants', '📸 Early morning: mist on the lake with Alps behind'] }
          ]
        },
        {
          label: 'Late Morning — Afternoon',
          activities: [
            { title: '🚆 Train to Cully → 📸 Lavaux Terraces Walk', description: 'Take the train to Cully (12 min) and walk the famous "Lavaux Wine Route" eastward through Epesses, Riex, and Rivaz back toward Lausanne. The Lavaux wine route winds through the vineyards with constant lake and Alps views. In spring, the new vine leaves are a luminous green against the blue lake.', details: ['🚆 Montreux → Cully: 12 min, Swiss Travel Pass', '📸 Best shot: Terraced vineyards falling to lake + Alps beyond', '📸 Villages like Riex and Épesses are immaculately preserved — shoot the stone lanes', '🍷 Stop at Domaine Croix-Duplex for a tasting (CHF 10-20) with lake view', '🥾 Full walk Cully → Rivaz → Lutry: ~12km, 4 hours, moderate climbs', '💡 The "LeNovice" cru at Riex is the most photogenic vine plot'] },
            { title: 'Rivaz Village & Wine Terrace', description: 'The tiny village of Rivaz sits at the most photogenic point of the Lavaux — directly at water level with vineyards rising steeply behind and the Dents du Midi reflected in the lake. The cooperative winery here offers excellent Chasselas wine for CHF 8-15/bottle to take home.', details: ['📸 From the Rivaz pier: terraced vineyards + Alps + lake', '🍷 Chasselas is the Lavaux signature grape — crisp, mineral, unique', '📸 Rivaz church bell tower in vineyard context'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Auberge du Raisin, Cully', description: 'A legendary address in the Swiss wine world — this inn in the heart of Lavaux has been feeding winemakers and travelers since 1829. Exceptional local fish (perch from Lake Geneva), lake wine pairings, and terrace tables with vineyard views.', meta: '€€€ · Place de l\'Hôtel-de-Ville, Cully · Reserve ahead · Lavaux institution' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: '📸 Montreux Golden Hour Return', description: 'Return to Montreux for the golden hour lake photography. The Casino promenade, the rose garden near the theater, and the lake reflections are at their most beautiful in the May evening light.', details: ['📸 Panorama from the casino terrace: lake + mountains + town lights at dusk', '📸 Long exposure of the lake at blue hour with Chillon castle lit in the distance'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurant du Grand-Chêne, Lausanne (optional detour)', description: 'If feeling adventurous, take the 25-min train to Lausanne for dinner — the city has a much more vibrant food scene. Return to Montreux by 10pm. Alternatively, Le Pont de Brent above Montreux is a Michelin-starred option.', meta: '€€€ · Various · Lausanne food scene or Montreux Michelin option' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.4843, lng: 6.7613, label: 'Cully (Lavaux start)', num: 1, cat: 'attraction', desc: 'Start of the Lavaux wine route walk — 12 min from Montreux' },
        { lat: 46.4843, lng: 6.7800, label: 'Epesses Village', num: 2, cat: 'photo', desc: 'Preserved village in UNESCO vineyard landscape' },
        { lat: 46.4808, lng: 6.7980, label: 'Riex (LeNovice cru)', num: 3, cat: 'photo', desc: 'Most photogenic vine plot — terraced rows + lake + Alps' },
        { lat: 46.4743, lng: 6.8121, label: 'Rivaz Village & Pier', num: 4, cat: 'photo', desc: 'Water-level village — best Lavaux composition' },
        { lat: 46.4843, lng: 6.7618, label: 'Auberge du Raisin', num: 5, cat: 'food', desc: '1829 Lavaux institution — local perch, Chasselas wine' },
        { lat: 46.4333, lng: 6.9151, label: 'Montreux Casino Promenade (golden hour)', num: 6, cat: 'photo', desc: 'Return for blue-hour lake + Chillon distant glow' }
      ]
    },
    {
      num: 17,
      neighborhoods: 'Montreux · Rochers-de-Naye · Vevey',
      title: 'Rochers-de-Naye Summit & Chaplin\'s World',
      description: 'The cogwheel railway from Montreux to Rochers-de-Naye (2,042m) climbs through forest and emerges at a summit with one of the finest panoramas in the Western Alps — looking over Lake Geneva, the Rhône valley, and the entire arc of the Bernese Alps you\'ve spent a week exploring.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '🚞 📸 Rochers-de-Naye Sunrise (Optional Early Start)', description: 'For the serious photographers: the first cogwheel from Montreux leaves at 6:30am to reach the summit at 8:10am for sunrise. The view stretches from Mont Blanc to the Matterhorn — arguably the most complete panorama available from a single Swiss summit.', details: ['🚞 MVR cogwheel from Montreux station', '📸 Panorama arc: Mont Blanc (NW) → Dents du Midi → Alps → Matterhorn (E)', '📸 Lake Geneva spreads 72km below — photograph with telephoto layers', '🎫 CHF 57 return (Swiss Pass discount)'] }
          ]
        },
        {
          label: 'Morning — Midday',
          activities: [
            { title: 'Rochers-de-Naye Gardens & Summit Walk', description: 'The Alpine garden at Rochers-de-Naye (1,700+ species) is one of the highest in Switzerland. In May, early blooms include primroses, gentians, and Alpine crocuses. The resident marmots are not shy. The summit ridge walk toward the Naye peak (30 min) gives the best views north over the lake.', details: ['🎫 CHF 57 return on the cogwheel (Swiss Pass discount)', '📸 Alpine flowers in early season — macro photography', '📸 Naye ridge: Lake Geneva 2km below you — dramatic depth of field', '💡 The "Caux-Palace" below the summit was a famous Belle Époque hotel'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Restaurant Rochers-de-Naye', description: 'Summit lunch with lake panorama. Simple but satisfying Swiss mountain standards — soup, sandwiches, hot chocolate. The view is the star.', meta: '€€ · 2,042m summit · Terrace lake views' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: '🚆 Train to Vevey — Charlie Chaplin\'s World', description: 'Descend to Montreux and take the 8-minute train to Vevey. Charlie Chaplin spent the last 25 years of his life here ("the most beautiful place in the world"). His estate is now a world-class museum (Chaplin\'s World) with a full recreation of his study, props, and films.', details: ['🎟️ CHF 21 (not covered by Swiss Pass)', '📸 The Chaplin statue on the Vevey lakefront (bronze, 3.5m) is the Montreux Jazz Festival equivalent for photographers', '🕐 Allow 2 hours for the full Chaplin experience'] },
            { title: '📸 Vevey Lakeside & Quai Perdonnet', description: 'Vevey has a quieter, more authentic waterfront than Montreux — locals swim here in summer, and the market square (Grande-Place) looks exactly as it did when Chaplin walked it. The fork sculpture in the lake (Alimentarium art installation) is surreally photogenic.', details: ['📸 Giant fork in the lake: shoot from the lakeside east of the pier', '📸 Chaplin statue + Alps behind + lake = perfect composition', '📸 The covered market hall (Halle de Fête) is architecturally interesting'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Denis Martin, Vevey', description: 'Montreux-Vevey\'s single Michelin star and arguably the most creative restaurant between Geneva and Zurich. Denis Martin was the pioneer of molecular gastronomy in Switzerland — 17-course surprise menu with wines from the Lavaux below. A truly special farewell to the Riviera.', meta: '€€€€ · Vevey · Michelin star · 17 courses · Book months ahead' }
          ],
          tips: [{ type: 'tip', text: '📦 Last night in Montreux — pack carefully for Geneva tomorrow. The train takes 50 minutes and you\'ll want your cameras accessible for the Jet d\'Eau and Old Town photography.' }]
        }
      ],
      mapPins: [
        { lat: 46.4280, lng: 6.9763, label: 'Rochers-de-Naye (2,042m)', num: 1, cat: 'photo', desc: 'Mont Blanc → Matterhorn panorama — supreme western Alps view' },
        { lat: 46.4292, lng: 6.9421, label: 'Caux Viewpoint (en route)', num: 2, cat: 'photo', desc: 'Mid-mountain stop with lake panorama below' },
        { lat: 46.4677, lng: 6.8442, label: 'Vevey Lakefront', num: 3, cat: 'photo', desc: 'Quieter than Montreux — fork sculpture, Chaplin statue' },
        { lat: 46.4628, lng: 6.8405, label: 'Chaplin\'s World Museum', num: 4, cat: 'attraction', desc: 'Charlie Chaplin\'s last home — world-class museum on his estate' },
        { lat: 46.4639, lng: 6.8423, label: 'Giant Fork in Lake (Alimentarium)', num: 5, cat: 'photo', desc: '8m steel fork in the lake — absurdist Swiss surrealism' },
        { lat: 46.4627, lng: 6.8408, label: 'Denis Martin Restaurant', num: 6, cat: 'food', desc: 'Michelin-starred molecular gastronomy — book months ahead' }
      ]
    },

    // ===================== GENEVA: DAYS 18-19 =====================
    {
      num: 18,
      neighborhoods: 'Montreux → Geneva · Old Town · Jet d\'Eau',
      title: 'Geneva — City of Diplomacy & the World\'s Most Famous Fountain',
      description: 'The train from Montreux to Geneva is 50 minutes along the full length of Lake Geneva — the Alps reflected in the water the entire way. Geneva is the most international city in Switzerland: UN, ICRC, Red Cross, and more watches per square meter than any city on Earth.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: '🚆 Train Montreux → Geneva (50 min)', description: 'The GoldenPass line follows Lake Geneva\'s north shore for much of the journey — look right for continuous mountain reflections. Arrive at Geneva Cornavin (main station) around 9am.', details: ['🚆 Montreux → Geneva: every 30 min, Swiss Travel Pass', '📸 Right-side seat for the lake the whole way', '💡 Geneva Cornavin is central — everything walkable from here'] },
            { title: '📸 Jet d\'Eau — Geneva\'s Icon', description: 'The Jet d\'Eau shoots 140m of water at 200km/h from a pier in Lake Geneva. Walk the Jetée des Eaux-Vives to get as close as possible — getting misted is part of the experience. Photography tip: shoot in the morning with the sun behind you (east) for best light on the water column.', details: ['📍 Free, visible from everywhere in Geneva', '📸 Morning: sun illuminates the water spray from behind you', '📸 Wide angle from the Quai Gustave-Ador for full fountain + Alps behind', '💡 The fountain operates April-October, 9am-11pm'] }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            { title: '📸 Old Town (Vieille-Ville) & Cathédrale Saint-Pierre', description: 'Geneva\'s Old Town rises on a hill above the lake. The Cathédrale Saint-Pierre (where Calvin preached) has a tower climb giving the finest rooftop view of the city — lake, mountains, and the Jet d\'Eau all visible.', details: ['🎟️ Tower climb: CHF 5', '📸 From the tower: the full lake + Alps panorama', '📸 Place du Bourg-de-Four — Geneva\'s oldest square, terraced cafés', '📸 Grand-Rue for medieval Geneva street photography'] }
          ],
          meals: [
            { type: '☕ Coffee', name: 'Café des Négociants (Old Town)', description: 'Traditional Geneva café in the old town quarter. Excellent coffee and croissants in a setting that hasn\'t changed since the Calvinist era.', meta: '€ · Old Town · Traditional café' },
            { type: '🍽️ Lunch', name: 'L\'Adresse, Geneva', description: 'Geneva\'s best brasserie for local classics — Longeole (Geneva pork sausage), perch fillets from Lake Geneva, and the classic "Filets de perche" which is Geneva\'s signature dish.', meta: '€€ · Rue de Rive 4 · Genevois classics' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Palais des Nations (UN Geneva) & Broken Chair', description: 'The European headquarters of the United Nations is open for guided tours. Outside the entrance, the giant Broken Chair sculpture (11m, 1997) symbolizes opposition to landmines. The Broken Chair + UN + Alps view behind is one of Geneva\'s great photographs.', details: ['🎟️ Guided tour: CHF 15 (ID required)', '📸 Broken Chair foreground + Palais des Nations + Mont Blanc on clear days', '🕐 Allow 1.5 hours for the tour'] },
            { title: '📸 Horloge Fleurie (Flower Clock) & Jardin Anglais', description: 'The Flower Clock (1955) is Geneva\'s most-photographed object after the Jet d\'Eau — 6,500 plants make up the clock face. In late April/May, the spring planting is spectacular. The English Garden surrounds it with lake views.', details: ['📍 Free, Quai du Général-Guisan', '📸 Elevated angle from the promenade wall for best clock composition', '📸 Include lake + Alps in background for the full Geneva postcard'] },
            { title: '📸 Bains des Pâquis Pier', description: 'Geneva\'s beloved bathing piers extend into the lake with views of Mont Blanc on clear days. The sunbathing culture here is very Genevois — locals come year-round. The pier and changing huts date from 1872 and are architecturally charming.', details: ['📍 Rue des Pâquis 30 · Free entry to pier area', '📸 From the end of the pier: Mt. Blanc framed between the Jet d\'Eau and the Old Town', '💡 Mt. Blanc is visible from Geneva on ~25% of days'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Café du Soleil, Grand-Saconnex', description: 'For a true Genevois experience: this canteen near the UN has served fondue to diplomats and locals since 1840. The fondue moitié-moitié (half Gruyère, half Vacherin) is definitive. Take a taxi; it\'s 10 min north.', meta: '€€ · Near the UN · Fondue institution since 1840' }
          ]
        }
      ],
      mapPins: [
        { lat: 46.2062, lng: 6.1551, label: 'Jet d\'Eau', num: 1, cat: 'photo', desc: '140m water fountain — shoot from east with morning sun behind you' },
        { lat: 46.2008, lng: 6.1476, label: 'Cathédrale Saint-Pierre', num: 2, cat: 'photo', desc: 'Tower climb for rooftop panorama — lake + Alps + fountain' },
        { lat: 46.2001, lng: 6.1484, label: 'Place du Bourg-de-Four', num: 3, cat: 'photo', desc: 'Geneva\'s oldest square — terraced cafés, medieval atmosphere' },
        { lat: 46.2261, lng: 6.1406, label: 'Broken Chair / Palais des Nations', num: 4, cat: 'photo', desc: 'UN HQ + 11m anti-landmine sculpture — with Alps on clear days' },
        { lat: 46.2022, lng: 6.1534, label: 'Horloge Fleurie (Flower Clock)', num: 5, cat: 'photo', desc: '6,500 plants make the clock face — spring planting spectacular' },
        { lat: 46.2103, lng: 6.1595, label: 'Bains des Pâquis Pier', num: 6, cat: 'photo', desc: 'Historic bathing pier — Mt. Blanc framed between Jet d\'Eau and Old Town' }
      ]
    },
    {
      num: 19,
      neighborhoods: 'Geneva · Patek Philippe Museum · Airport Departure',
      title: 'Final Geneva Morning & Departure',
      description: 'Your last morning in Switzerland. Geneva rewards the early riser: the Old Town is empty at 7am, the Jet d\'Eau glows in the morning light, and the lake is glassy and still. End 19 extraordinary days with coffee on a terrace above the lake before heading to Geneva Airport.',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            { title: '📸 Dawn Geneva — Empty City Photography', description: 'Wake early for Geneva\'s most magical photography window. The Old Town at 6-7am is completely empty. The Jet d\'Eau glows against the pink dawn sky. The Quai Wilson is deserted with perfect lake reflections.', details: ['📸 Jet d\'Eau at dawn: pink sky + water spray + still lake', '📸 Old Town lanes: Grand-Rue with morning mist', '📸 Cathédrale towers silhouetted against sunrise', '💡 The fountain starts at 9am (Apr-Oct) but the lake itself and the pier are photogenic before'] }
          ]
        },
        {
          label: 'Morning',
          activities: [
            { title: 'Patek Philippe Museum (If Time Permits)', description: 'The finest watch museum in the world occupies a restored 19th-century building near Plainpalais. Even non-horologists are amazed: enamel miniatures, pocket watches from 1530, and the full story of Swiss watchmaking. Allow 1.5 hours.', details: ['🎟️ CHF 10 adult', 'Opens at 10am Tuesday-Saturday', '📸 The historic timepieces are extraordinary macro subjects'] },
            { title: 'Final Lake Walk & Coffee', description: 'A last stroll along the Quai du Mont-Blanc. On clear days, Mont Blanc is visible from here — at 4,808m, Europe\'s highest peak floating above the lake. Order a final café au lait at a lakeside terrace.', details: ['📸 Mont Blanc from the Quai du Mont-Blanc on clear mornings', '☕ Grand Café de Rive or Café du Lac for a final lake terrace coffee'] }
          ],
          meals: [
            { type: '🍽️ Breakfast', name: 'Boulangerie Poilâne Geneva', description: 'The Parisian bakery\'s Geneva outpost. Outstanding butter croissants, pain au chocolat, and the best bread in the city. Perfect final Swiss morning fuel.', meta: '€ · Rue du Marché · Finest French-Swiss baking' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            { title: '✈️ Geneva Airport (GVA) — Departure', description: 'Geneva Airport is compact and efficient. Uniquely, the airport has a dedicated Swiss customs exit (Sector F) that allows direct boarding into Switzerland — meaning you don\'t queue for Swiss customs when you return. The Unique Art program fills the terminal with rotating modern art exhibitions.', details: ['🚆 Geneva Cornavin → Airport: 7 min, every 10 min, Swiss Travel Pass', '✈️ Arrive 2.5-3 hours before international departure', '💡 You can buy last-minute Swiss chocolate, watches, and cheese at the duty-free — all genuine', '🎁 Lindt, Läderach, and Laderach pralines are excellent gifts from GVA'] }
          ],
          tips: [{ type: 'reddit', text: '"Swiss milk chocolate really is better in Switzerland — the cows eat the grass, the chocolate tastes different. Buy Läderach at the airport, not Toblerone — locals don\'t eat Toblerone." — r/Switzerland', cite: 'r/Switzerland' }]
        }
      ],
      mapPins: [
        { lat: 46.2062, lng: 6.1551, label: 'Jet d\'Eau (dawn)', num: 1, cat: 'photo', desc: 'First light on the fountain — empty promenade photography' },
        { lat: 46.2001, lng: 6.1484, label: 'Old Town at dawn', num: 2, cat: 'photo', desc: 'Empty Grand-Rue at 6-7am — no tourists, perfect light' },
        { lat: 46.1983, lng: 6.1440, label: 'Patek Philippe Museum', num: 3, cat: 'attraction', desc: 'World\'s finest watch museum — opens 10am, CHF 10' },
        { lat: 46.2100, lng: 6.1500, label: 'Quai du Mont-Blanc', num: 4, cat: 'photo', desc: 'Final lake walk — Mont Blanc visible on clear mornings' },
        { lat: 46.2310, lng: 6.1085, label: 'Geneva Airport (GVA)', num: 5, cat: 'transport', desc: '7 min by train from Cornavin — Sector F for Swiss customs exit' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Flights (international, round trip for 2)', budget: '$2,400–3,400', notes: 'Business class or premium economy from US; book 3+ months ahead' },
    { category: 'Swiss Travel Pass (15-day, 2 people)', budget: '$1,200–1,400', notes: 'Covers virtually all trains, boats, mountain transport discounts' },
    { category: 'Accommodation (19 nights, 2 people)', budget: '$3,500–5,000', notes: 'Mix: Zurich/Geneva (4-star hotels), Alpine villages (mountain hotels)' },
    { category: 'Mountain Excursions (Jungfraujoch, Glacier Paradise, etc.)', budget: '$600–800', notes: 'Top-ups beyond Swiss Pass: Jungfraujoch, Glacier Paradise, etc.' },
    { category: 'Meals & Dining', budget: '$1,500–2,000', notes: 'Mix of mountain huts, brasseries, one Michelin dinner' },
    { category: 'Activities (museums, cable cars, Château de Chillon)', budget: '$300–400', notes: 'Some covered by Swiss Pass; CHF 100 buffer for misc' },
    { category: 'Shopping & Souvenirs', budget: '$500–1,000', notes: 'Swiss watches, chocolate, Lavaux wine to bring home' },
    { category: 'TOTAL ESTIMATE (2 people)', budget: '$10,000–13,600', notes: 'Upper estimate includes premium hotel upgrades and Michelin meals' }
  ],

  practicalInfo: [
    {
      title: '📷 Photography Essentials for Switzerland',
      items: [
        'Polarizing filter: Non-negotiable for Stellisee and Bachalpsee reflections. Eliminates glare and saturates the blue.',
        'Telephoto 200-400mm: Compresses distance to Matterhorn and Alpine peaks. Brings distant details to life.',
        'Wide angle 16-24mm: Essential for Jungfraujoch glacier, mountain panoramas, and old-town architecture.',
        'Golden hour times in late April: Sunrise ~6:20am, Sunset ~8:30pm — plan summit arrivals accordingly.',
        'Tripod for: long-exposure water (Lauterbrunnen, Trümmelbach), blue-hour cityscapes (Lucerne), and reflection photography at still water.',
        'Camera rain cover: Swiss mountain weather changes without warning — protect your gear.'
      ]
    },
    {
      title: '🎫 Swiss Travel Pass Tips',
      items: [
        'Buy the 15-day consecutive pass BEFORE leaving home — discounts up to 15% from Swiss travel offices abroad.',
        'The pass covers: all SBB trains, most postal buses, lake steamers (including Lucerne and Montreux/Geneva), and 50% off most mountain railways.',
        'NOT covered by the pass: Jungfraujoch top section (~CHF 100 surcharge), Matterhorn Glacier Paradise (~CHF 50 surcharge), Rochers-de-Naye.',
        'Free days at 500+ museums including Swiss National Museum, Matterhorn Museum, and KKL Luzern.',
        'Seat reservations required for Glacier Express (CHF 49) — not included in pass price.',
        'The Half Fare Card (CHF 130) is an alternative if you prefer flexibility over unlimited travel.'
      ]
    },
    {
      title: '🏔️ Mountain Safety & Preparation',
      items: [
        'Check the forecast at meteoswiss.ch every morning — cable cars close for wind and visibility. Have backup plans.',
        'Altitude: At Jungfraujoch (3,454m) you may feel light-headed. Drink water, move slowly, eat something. Altitude sickness is uncommon but take the first symptoms seriously.',
        'Layers: Mountain temperatures can be 15°C warmer or colder than the valley within one hour. Always carry: waterproof shell, fleece, sun protection.',
        'Trail conditions in late April: Snow is common on higher trails (Bachalpsee, Riffelsee area). Trekking poles are useful. Check jungfrau.ch and zermatt.ch for current conditions.',
        'Boots: Waterproof hiking boots are essential. The trails are well-maintained but rocky and sometimes muddy.',
        'Sun protection: Alpine UV is intense even through cloud. SPF 50, sunglasses (UV400), and a hat are non-negotiable above 2,000m.'
      ]
    },
    {
      title: '🚆 Getting Around',
      items: [
        'Swiss trains run every 30 minutes on all main routes and are precise to the minute. Missed connections are extremely rare.',
        'Wengen to Zermatt: Train via Interlaken and Visp (~3 hours). The Lötschberg section is spectacular.',
        'Zermatt to Montreux: Via Visp and Lausanne (or direct BLS Lötschberger trains). ~2h30min.',
        'Montreux to Geneva: 50 minutes on the GoldenPass or direct IC trains. Frequent service.',
        'Car-free zones: Wengen (park at Lauterbrunnen) and Zermatt (park at Täsch, CHF 16/day). The rail connections are seamless.',
        'Download the SBB Mobile app — real-time timetables, platform information, and digital ticket options.'
      ]
    },
    {
      title: '🍽️ Dining Culture',
      items: [
        'Reservations: Always book dinner ahead at mountain restaurants (Zum See, Chez Vrony, Denis Martin). These fill weeks out.',
        'Lunch is often better value than dinner — many restaurants offer a "Tagesmenü" (daily menu) for CHF 18-28 with two courses.',
        'Fondue etiquette: If you lose your bread in the pot, Swiss tradition says you buy a round of drinks. Different regions use different cheeses — Appenzeller in the East, Gruyère/Vacherin in the West.',
        'Tipping: Not obligatory — service is included in Swiss prices. Round up 5-10% for excellent service.',
        'Dietary needs: Vegetarian options are excellent at all major restaurants. Vegan requires advance notice at traditional Swiss places. Gluten-free Rösti (naturally GF) is a go-to option.',
        'Wine pairing: In Valais (Zermatt area), drink Fendant (Chasselas) white and Pinot Noir red. In Vaud (Montreux/Lavaux), focus on Chasselas whites from the terraced vineyards.'
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Switzerland 19-day itinerary fulfilled!');
console.log('URL:', result.url);
console.log('Slug:', result.slug);
console.log('Email sent:', result.emailSent);
