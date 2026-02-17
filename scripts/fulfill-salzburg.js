const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771295494107_qxbclp',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Salzburg, Austria',
};

const itineraryData = {
  destination: 'Salzburg, Austria',
  countryEmoji: '🇦🇹',
  title: 'Salzburg: Mozart, Mountains & the Sound of Music',
  subtitle: '6 nights exploring Austria\'s baroque jewel — fortress views, Alpine lakes, underground ice caves, and Salzburg Festival magic',
  description: 'Salzburg sits where the Alps meet baroque elegance — a city of domes and spires framed by dramatic mountain scenery. This July itinerary takes a group of 3-4 through Mozart\'s birthplace, Sound of Music filming locations, the mighty Hohensalzburg Fortress, and out into the surrounding Alps for day trips to Hallstatt, the Eisriesenwelt ice caves, and the lakes of the Salzkammergut. July means the legendary Salzburg Festival is in full swing — expect the city humming with music, theater, and cultural energy.',
  duration: '6 nights',
  dates: 'Jul 4 – Jul 10, 2026',
  budget: '€150 – €250 per person/day',
  pace: 'Moderate',
  bestFor: 'Small groups, Culture lovers, Alpine adventurers',
  highlights: ['Hohensalzburg Fortress panoramic views', 'Mozart\'s Birthplace & Getreidegasse', 'Sound of Music filming locations', 'Salzburg Festival performances', 'Day trip to Hallstatt', 'Eisriesenwelt Ice Caves', 'Alpine lake swimming in Salzkammergut'],

  essentials: [
    { title: '🛬 Getting Around', text: 'Salzburg\'s Altstadt (Old Town) is compact and walkable. Buses cover the wider city (24hr ticket ~€6). For day trips, rent a car or use ÖBB trains — the Salzburg Card (€30-42) covers public transport, fortress funicular, and museum entry.' },
    { title: '💵 Money', text: 'Euro (€). Cards widely accepted, but carry some cash for smaller cafés and market stalls. ATMs are plentiful. Budget €50-80/person for meals, €20-40 for attractions per day.' },
    { title: '🗣️ Language', text: 'German (Austrian dialect). English is widely spoken in tourist areas, hotels, and restaurants. A "Grüß Gott" (hello) and "Danke" (thanks) go a long way.' },
    { title: '🌦️ July Weather', text: 'Warm and sunny, 18-28°C (64-82°F). Afternoon thunderstorms are common in the Alps — pack a light rain jacket. Sunscreen essential for mountain hikes. Lake water is refreshing at 20-24°C.' },
    { title: '🎵 Salzburg Festival', text: 'The Salzburger Festspiele runs mid-July through August — world-class opera, concerts, and theater. Book tickets well ahead at salzburgerfestspiele.at. Even without tickets, the city buzzes with free open-air screenings and street performances.' },
    { title: '🔒 Safety', text: 'Salzburg is extremely safe. Tap water is pristine Alpine spring water — drink it everywhere. Pharmacies (Apotheke) are well-stocked. EU health cards accepted; travel insurance recommended for mountain activities.' },
  ],

  days: [
    // DAY 1 — Arrival & Old Town
    {
      num: 1,
      title: 'Arrival & Baroque Old Town',
      description: 'Settle into Salzburg and explore the UNESCO-listed Altstadt — Getreidegasse, Mozart\'s Birthplace, and the Residenzplatz fountains.',
      neighborhoods: 'Altstadt · Getreidegasse · Residenzplatz',
      timeBlocks: [
        {
          label: 'Morning / Afternoon',
          activities: [
            {
              title: 'Arrive in Salzburg',
              description: 'Fly into Salzburg Airport (SZG) or arrive by train from Munich (1.5h) or Vienna (2.5h). The Hauptbahnhof is a 20-minute walk or quick bus ride to the Old Town.',
              details: ['Recommended hotels: Hotel Sacher Salzburg, Hotel Goldener Hirsch, or Arthotel Blaue Gans in the Altstadt', '💡 Pick up a Salzburg Card at the tourist office — it pays for itself in one day']
            },
            {
              title: 'Mozart\'s Birthplace (Mozarts Geburtshaus)',
              description: 'Wolfgang Amadeus Mozart was born in this bright yellow townhouse on Getreidegasse in 1756. Three floors of exhibits display his childhood violin, portraits, and original scores. A pilgrimage for any music lover.',
              details: ['📍 Getreidegasse 9', '🕐 9am-5:30pm daily · €14 (included in Salzburg Card)', '💡 Less crowded after 3pm']
            },
            {
              title: 'Getreidegasse & Residenzplatz',
              description: 'Salzburg\'s most famous shopping street — look up at the ornate wrought-iron guild signs. Continue to Residenzplatz, the grand square with its baroque fountain, flanked by the Salzburg Cathedral (Dom) and the Residenz palace.',
              details: ['📍 Heart of the Altstadt', '💡 Step into the side passages (Durchhäuser) connecting Getreidegasse to Universitätsplatz — hidden courtyards and local shops']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Stiftsbäckerei St. Peter',
              description: 'One of Salzburg\'s oldest bakeries, right next to St. Peter\'s Abbey. Grab fresh bread, pastries, and a simple lunch in the courtyard — the perfect casual introduction to Salzburg.',
              meta: '📍 Kapitelplatz 8 · 💰 €8-15/person'
            },
            {
              type: '🍽️ Dinner',
              name: 'Stiftskeller St. Peter',
              description: 'Possibly Europe\'s oldest restaurant (803 AD). Dine in vaulted baroque rooms or the candlelit rock-carved chambers. Classic Austrian cuisine — Tafelspitz, Wiener Schnitzel, and Salzburger Nockerl for dessert.',
              meta: '📍 St. Peter Bezirk 1/4 · 💰 €30-50/person · ⚠️ Reserve ahead in July'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Salzburg Card (24/48/72hr) includes all major museums, fortress funicular, river cruise, and public transport. Essential for a group of 3-4.' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.7953, lng: 13.0044, label: 'Salzburg Hauptbahnhof', num: 1, cat: 'transport', desc: 'Main train station — 20 min walk to Old Town' },
        { lat: 47.8001, lng: 13.0438, label: 'Mozart\'s Birthplace', num: 2, cat: 'attraction', desc: 'Getreidegasse 9 — where Mozart was born in 1756' },
        { lat: 47.7986, lng: 13.0455, label: 'Getreidegasse', num: 3, cat: 'attraction', desc: 'Famous shopping street with wrought-iron signs' },
        { lat: 47.7982, lng: 13.0467, label: 'Residenzplatz', num: 4, cat: 'attraction', desc: 'Grand baroque square with fountain and cathedral' },
        { lat: 47.7974, lng: 13.0453, label: 'Stiftskeller St. Peter', num: 5, cat: 'restaurant', desc: 'Europe\'s oldest restaurant — Austrian classics since 803 AD' }
      ]
    },

    // DAY 2 — Fortress & Mirabell
    {
      num: 2,
      title: 'Fortress, Mirabell & Mozart\'s Music',
      description: 'Ride the funicular up to Hohensalzburg Fortress for panoramic Alpine views, then stroll through Mirabell Gardens — the iconic Sound of Music "Do-Re-Mi" location.',
      neighborhoods: 'Festungsberg · Mirabell · Kapuzinerberg',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hohensalzburg Fortress',
              description: 'Towering above the city at 506m, this 1077 fortress is one of the largest medieval castles in Europe. Take the funicular up (or walk 20 min) and explore the state rooms, torture chamber museum, and the stunning Rainer Regiment Museum. The terrace views over the city, river, and Alps are breathtaking.',
              details: ['📍 Mönchsberg 34', '🕐 9am-7pm (July) · €16.30 incl. funicular (Salzburg Card)', '💡 Go early for fewer crowds and clearer mountain views']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Panorama Restaurant at the Fortress',
              description: 'Dine with arguably the best view in Salzburg — floor-to-ceiling windows overlooking the city and Alps. Austrian comfort food elevated: kasnocken (cheese dumplings), local trout, and cold Austrian white wine.',
              meta: '📍 Inside Hohensalzburg Fortress · 💰 €20-35/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The fortress funicular is included in the Salzburg Card. Without it, the uphill walk takes ~20 minutes through lovely wooded paths.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mirabell Palace & Gardens',
              description: 'The baroque Mirabell Gardens are Salzburg\'s most photographed spot — and where Julie Andrews and the von Trapp children danced around the Pegasus Fountain singing "Do-Re-Mi." The Marble Hall inside is one of the world\'s most beautiful concert venues.',
              details: ['📍 Mirabellplatz 4', '🕐 Gardens open 6am-dusk · Free', '💡 Marble Hall concerts run almost nightly in summer — €30-40 for an hour of Mozart/Baroque in an extraordinary setting']
            },
            {
              title: 'Kapuzinerberg Walk',
              description: 'Cross the Salzach River and climb the forested Kapuzinerberg hill for a quieter, locals-favorite viewpoint. The Stefan Zweig memorial path winds through woods to the Capuchin Monastery at the top. Wonderful late-afternoon light.',
              details: ['📍 Linzer Gasse trailhead', '🕐 30-45 min round trip · Free', '💡 Bring water — it\'s a proper uphill walk in July heat']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Triangel',
              description: 'Beloved by locals and tucked behind the Festspielhaus. Known for excellent Wiener Schnitzel the size of a dinner plate, seasonal salads, and Austrian wines. Casual, bustling, and unpretentious.',
              meta: '📍 Wiener-Philharmoniker-Gasse 7 · 💰 €18-30/person'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Mirabell Gardens at golden hour is magical. Go around 7pm in July — fewer tour groups, gorgeous light.', cite: 'r/austria' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.7952, lng: 13.0475, label: 'Hohensalzburg Fortress', num: 1, cat: 'attraction', desc: '1077 medieval fortress with panoramic views' },
        { lat: 47.8053, lng: 13.0421, label: 'Mirabell Gardens', num: 2, cat: 'attraction', desc: 'Baroque gardens — "Do-Re-Mi" filming location' },
        { lat: 47.8029, lng: 13.0509, label: 'Kapuzinerberg', num: 3, cat: 'attraction', desc: 'Forested hill with panoramic viewpoint' },
        { lat: 47.7987, lng: 13.0407, label: 'Triangel', num: 4, cat: 'restaurant', desc: 'Local favorite for oversized Wiener Schnitzel' }
      ]
    },

    // DAY 3 — Sound of Music & Hellbrunn
    {
      num: 3,
      title: 'Sound of Music Trail & Hellbrunn Palace',
      description: 'Follow in the footsteps of the von Trapp family — Leopoldskron Palace, Nonnberg Abbey, and the trick fountains of Hellbrunn Palace.',
      neighborhoods: 'Leopoldskron · Nonnberg · Hellbrunn',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nonnberg Abbey',
              description: 'The real Maria von Trapp was a novice at this Benedictine convent, the oldest continuously operating nunnery north of the Alps (founded 714 AD). The church is open to visitors — you can\'t enter the cloister, but the Gothic church and views over the city are wonderful.',
              details: ['📍 Nonnberggasse 2', '🕐 7am-dusk · Free', '💡 The walk up from Kaigasse is steep but atmospheric']
            },
            {
              title: 'Schloss Leopoldskron',
              description: 'This lakeside rococo palace served as the exterior of the von Trapp family home in the film. Now a hotel, you can\'t tour inside, but walk around the lake for the iconic view of the palace with the fortress behind it. Gorgeous on a summer morning.',
              details: ['📍 Leopoldskronstraße 56-58', '💡 Walk the full loop around Leopoldskroner Weiher (lake) — about 30 minutes, flat and scenic']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Café Tomaselli',
              description: 'Austria\'s oldest coffee house (1700). Sit on the terrace overlooking Alter Markt square, order a Melange (Viennese-style coffee), and choose from the pastry tray wheeled to your table. Pure old-world charm.',
              meta: '📍 Alter Markt 9 · 💰 €10-18/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Original Sound of Music Tour (€55, 4 hours) covers all major film locations with a fun guide. Book at panoramatours.com if you want the full experience.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hellbrunn Palace & Trick Fountains',
              description: 'This 1615 pleasure palace was built by a prince-archbishop with a wicked sense of humor. The trick fountains (Wasserspiele) are the highlight — hidden water jets soak unsuspecting visitors from stone seats, table settings, and garden paths. Hilarious for groups. The "Sixteen Going on Seventeen" gazebo from Sound of Music is in the gardens.',
              details: ['📍 Fürstenweg 37, 5020 Salzburg', '🕐 9am-6pm (July) · €16.50 (Salzburg Card)', '💡 You WILL get wet at the trick fountains — welcome on a hot July day']
            },
            {
              title: 'Swim at Freibad Leopoldskron or Salzach River',
              description: 'Cool off at the Leopoldskron outdoor swimming pool with mountain views, or join the locals at the Salzach River beaches. July in Salzburg means outdoor swimming is a way of life.',
              details: ['📍 Leopoldskronstraße · 💰 €5-7 entry', '💡 River swimming is popular but check current conditions — the Salzach can be swift']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gasthof Schloss Aigen',
              description: 'A hidden beer garden gem at the foot of the Gaisberg mountain. Locals pack this place on summer evenings for massive Schnitzels, grilled fish, and cold Stiegl beer under chestnut trees. The Sound of Music\'s "Edelweiss" scene was inspired by places like this.',
              meta: '📍 Schwarzenbergpromenade 37 · 💰 €15-28/person'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Hellbrunn trick fountains are genuinely funny — even adults crack up. Best experience on a hot day when getting soaked is a feature, not a bug.', cite: 'r/travel' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.7943, lng: 13.0499, label: 'Nonnberg Abbey', num: 1, cat: 'attraction', desc: 'Where the real Maria was a novice — oldest nunnery north of Alps' },
        { lat: 47.7868, lng: 13.0379, label: 'Schloss Leopoldskron', num: 2, cat: 'attraction', desc: 'Von Trapp family home exterior in the film' },
        { lat: 47.7988, lng: 13.0461, label: 'Café Tomaselli', num: 3, cat: 'restaurant', desc: 'Austria\'s oldest coffee house since 1700' },
        { lat: 47.7627, lng: 13.0601, label: 'Hellbrunn Palace', num: 4, cat: 'attraction', desc: 'Trick fountains and Sound of Music gazebo' },
        { lat: 47.7862, lng: 13.0390, label: 'Freibad Leopoldskron', num: 5, cat: 'attraction', desc: 'Outdoor pool with mountain views' },
        { lat: 47.7910, lng: 13.0780, label: 'Gasthof Schloss Aigen', num: 6, cat: 'restaurant', desc: 'Beer garden at foot of Gaisberg mountain' }
      ]
    },

    // DAY 4 — Hallstatt Day Trip
    {
      num: 4,
      title: 'Day Trip: Hallstatt & the Salzkammergut',
      description: 'Drive or take the train to the fairy-tale lakeside village of Hallstatt — a UNESCO World Heritage site with salt mines, Alpine swimming, and the famous Skywalk viewpoint.',
      neighborhoods: 'Hallstatt · Salzkammergut · Dachstein',
      timeBlocks: [
        {
          label: 'Full Day',
          activities: [
            {
              title: 'Drive to Hallstatt',
              description: 'Hallstatt is about 75 minutes from Salzburg by car (or 2.5h by train + ferry). Leave early to beat the crowds — this tiny village gets packed by midday in summer. Park at P1 (the tunnel parking garage) and take the 2-minute walk into the village.',
              details: ['📍 75 min drive via A10 motorway', '💡 By train: Salzburg Hbf → Attnang-Puchheim → Hallstatt station, then a scenic 7-minute ferry across the lake', '💡 Arrive before 9:30am for the best experience']
            },
            {
              title: 'Hallstatt Skywalk (Salzwelten)',
              description: 'Take the funicular up to the world\'s oldest salt mine (3,000+ years). The Skywalk viewing platform juts out 350m above the lake — the panorama of Hallstatt, the lake, and the Dachstein mountains is one of Austria\'s most iconic views.',
              details: ['📍 Salzbergstraße 21', '🕐 9:30am-4:30pm · €40 combo ticket (mine + funicular)', '💡 The salt mine tour (1.5h) includes underground slides and a subterranean salt lake — great fun for groups']
            },
            {
              title: 'Hallstatt Village & Lake Swimming',
              description: 'Wander the pastel-colored houses clinging to the mountainside, visit the Beinhaus (bone house) in St. Michael\'s Chapel with its painted skulls, and then cool off with a swim in the crystal-clear lake. Water temperature reaches 20-24°C in July.',
              details: ['📍 Hallstatt village center', '💡 The lakeside Badestrand (beach area) near the Lahn car park is the best spot for swimming', '💡 Grab a Langos (fried dough) or fish from a lakeside vendor']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Bräugasthof Hallstatt',
              description: 'Lakeside restaurant with a terrace hanging over the water. Local lake fish (Reinanke), Kaiserschmarrn (torn pancake), and house-brewed beer. The view alone is worth the trip.',
              meta: '📍 Seestraße 120, Hallstatt · 💰 €18-30/person'
            },
            {
              type: '🍽️ Dinner',
              name: 'Bärenwirt',
              description: 'Back in Salzburg, this is one of the city\'s best traditional restaurants. Organic, locally-sourced Austrian cuisine — the Styrian beef and seasonal game dishes are outstanding. Great beer selection.',
              meta: '📍 Müllner Hauptstraße 8, Salzburg · 💰 €20-35/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Hallstatt is tiny — 2-3 hours is enough to see the village. Spend the extra time at the salt mine or swimming in the lake.' },
            { type: 'reddit', text: 'Go to Hallstatt early or late. Between 10am-3pm it\'s a zoo. The morning light on the lake is insanely beautiful.', cite: 'r/austria' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.5622, lng: 13.6493, label: 'Hallstatt Village', num: 1, cat: 'attraction', desc: 'UNESCO fairy-tale lakeside village' },
        { lat: 47.5576, lng: 13.6421, label: 'Salzwelten & Skywalk', num: 2, cat: 'attraction', desc: 'World\'s oldest salt mine + 350m viewing platform' },
        { lat: 47.5620, lng: 13.6500, label: 'Hallstatt Lake Beach', num: 3, cat: 'attraction', desc: 'Crystal-clear Alpine lake swimming spot' },
        { lat: 47.5618, lng: 13.6485, label: 'Bräugasthof Hallstatt', num: 4, cat: 'restaurant', desc: 'Lakeside terrace with local fish and house-brewed beer' },
        { lat: 47.8065, lng: 13.0361, label: 'Bärenwirt', num: 5, cat: 'restaurant', desc: 'Organic Austrian cuisine back in Salzburg' }
      ]
    },

    // DAY 5 — Eisriesenwelt & Werfen
    {
      num: 5,
      title: 'Eisriesenwelt Ice Caves & Hohenwerfen Castle',
      description: 'Venture south into the Salzach Valley for the world\'s largest ice cave and a dramatic medieval fortress perched on a cliff — with a live falconry show.',
      neighborhoods: 'Werfen · Tennengebirge · Salzach Valley',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Eisriesenwelt Ice Caves',
              description: 'The world\'s largest accessible ice cave stretches 42km into the Tennengebirge mountains. A guided tour (1.5h) takes you through glittering ice formations, frozen waterfalls, and vast chambers lit by magnesium flares. Even in July, it\'s 0°C inside — bring warm layers.',
              details: ['📍 Eishöhlenstraße 30, Werfen (40 min from Salzburg)', '🕐 First tour 9:30am, last tour 3:30pm · €29/person', '💡 The approach involves a cable car + 20-min uphill walk. Wear sturdy shoes.', '⚠️ Temperature inside is 0°C year-round — bring a jacket, gloves, and warm layer even in July']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Dr. Oedl-Haus Mountain Hut',
              description: 'Rustic mountain hut near the ice cave entrance. Hearty Austrian mountain food — Gulaschsuppe, Kaiserschmarrn, and hot drinks to warm up after the caves. Stunning valley views.',
              meta: '📍 Near Eisriesenwelt cable car station · 💰 €10-18/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Book the first tour of the day (9:30am) at Eisriesenwelt — smaller groups and you\'ll have time for Hohenwerfen Castle in the afternoon.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hohenwerfen Castle & Falconry Show',
              description: 'This dramatic 11th-century cliff-top fortress starred as the "SS headquarters" in Where Eagles Dare. The live falconry show features eagles, hawks, and falcons diving from the castle ramparts against an Alpine backdrop. The views down the Salzach Valley are extraordinary.',
              details: ['📍 Burgstraße 2, Werfen', '🕐 9am-6pm (July) · €16.50 · Falconry shows at 11:15am & 3:15pm', '💡 Take the lift up (included in ticket) or walk the fortress trail (15 min)']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'K+K Restaurant am Waagplatz',
              description: 'Elegant but unfussy restaurant on one of Salzburg\'s prettiest squares. Creative Austrian-Mediterranean cuisine with seasonal ingredients. The outdoor terrace on Waagplatz is perfect for warm summer evenings.',
              meta: '📍 Waagplatz 2, Salzburg · 💰 €30-45/person'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Eisriesenwelt is a real adventure — not a tourist trap. The magnesium flare lighting makes the ice glow. Absolutely worth the trek up.', cite: 'r/travel' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.5039, lng: 13.1914, label: 'Eisriesenwelt Ice Caves', num: 1, cat: 'attraction', desc: 'World\'s largest ice cave — 0°C underground adventure' },
        { lat: 47.4828, lng: 13.1880, label: 'Hohenwerfen Castle', num: 2, cat: 'attraction', desc: '11th-century cliff fortress with live falconry shows' },
        { lat: 47.4980, lng: 13.1890, label: 'Dr. Oedl-Haus', num: 3, cat: 'restaurant', desc: 'Mountain hut with hearty Austrian food near ice caves' },
        { lat: 47.7993, lng: 13.0467, label: 'K+K am Waagplatz', num: 4, cat: 'restaurant', desc: 'Austrian-Mediterranean on a pretty Old Town square' }
      ]
    },

    // DAY 6 — Untersberg, Festival & Farewell
    {
      num: 6,
      title: 'Untersberg Summit, Festival & Farewell',
      description: 'Ride the cable car up the Untersberg for breathtaking Alpine panoramas, spend a final afternoon soaking in Salzburg Festival atmosphere, and toast the trip with a farewell dinner.',
      neighborhoods: 'Untersberg · Festspielhaus · Altstadt',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Untersberg Cable Car & Summit',
              description: 'The Untersbergbahn whisks you from the city fringe to 1,853m in just 8 minutes. At the top, a network of hiking trails leads to panoramic viewpoints across the Berchtesgaden Alps, Salzburg, and as far as the Czech border on clear days. The short trail to the Geiereck summit (15 min) is essential.',
              details: ['📍 Dr.-Friedrich-Oedl-Weg 2, Grödig (15 min from Salzburg)', '🕐 8:30am-5:30pm (July) · €29 round trip (Salzburg Card)', '💡 Temperature at the top is 10-15°C cooler than the city — bring layers', '💡 For serious hikers: the ridge walk to Salzburger Hochthron (1h) is spectacular']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Augustiner Bräustübl',
              description: 'Salzburg\'s legendary beer hall — a working monastery brewery since 1621. Grab a stone mug, fill it from the wooden barrels, and choose from food stalls selling roast pork, pretzels, and radishes. Sit in the enormous chestnut tree beer garden. A quintessential Salzburg experience.',
              meta: '📍 Lindhofstraße 7 · 💰 €10-18/person · 🍺 Self-service beer from wooden barrels'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Augustiner Bräustübl is cash-only for the beer. Grab euros before you go. The garden fits 1,400 people but fills up on summer evenings.' }
          ]
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Salzburg Festival Atmosphere',
              description: 'Stroll the Festival District around the Festspielhaus and Domplatz. In early July, the festival is gearing up or just beginning — check the program for open-air screenings, Jedermann performances on Domplatz, and Siemens Fest>Spiel>Nächte (free open-air opera screenings in Kapitelplatz).',
              details: ['📍 Hofstallgasse / Domplatz', '💡 Free open-air screenings of festival performances on the big screen in Kapitelplatz most evenings', '💡 Even without tickets, the energy around the Festspielhaus is electric']
            },
            {
              title: 'Final Stroll Along the Salzach',
              description: 'Walk along the Salzach River as the evening light paints the fortress and Old Town in gold. Cross the Makartsteg bridge (covered in love locks) for a final panoramic photo op.',
              details: ['📍 Makartsteg footbridge', '💡 Golden hour in July is around 8:30pm — perfect timing before dinner']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Esszimmer',
              description: 'Salzburg\'s two-Michelin-star restaurant for a memorable farewell dinner. Chef Andreas Kaiblinger creates extraordinary multi-course menus with Austrian ingredients and global technique. The rooftop views over the Old Town are the cherry on top.',
              meta: '📍 Müllner Hauptstraße 33 · 💰 €120-180/person · ⭐⭐ 2 Michelin stars · ⚠️ Book well in advance'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If Esszimmer is fully booked, Ikarus at Hangar-7 (Red Bull\'s aviation museum) is another world-class option — guest chefs rotate monthly.' },
            { type: 'reddit', text: 'Augustiner Bräustübl is the real deal. Stone mugs, monastery beer, massive beer garden. Don\'t leave Salzburg without going here.', cite: 'r/austria' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.7310, lng: 13.0050, label: 'Untersberg Cable Car', num: 1, cat: 'attraction', desc: 'Cable car to 1,853m — Alpine panoramas in 8 minutes' },
        { lat: 47.8057, lng: 13.0338, label: 'Augustiner Bräustübl', num: 2, cat: 'restaurant', desc: 'Monastery beer hall since 1621 — stone mugs, beer garden' },
        { lat: 47.7978, lng: 13.0432, label: 'Festspielhaus', num: 3, cat: 'attraction', desc: 'Salzburg Festival main venue — open-air screenings nearby' },
        { lat: 47.8004, lng: 13.0446, label: 'Makartsteg Bridge', num: 4, cat: 'attraction', desc: 'Love-lock bridge with panoramic Old Town views' },
        { lat: 47.8068, lng: 13.0355, label: 'Restaurant Esszimmer', num: 5, cat: 'restaurant', desc: '2 Michelin stars — rooftop farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (mid-range hotel)', perDay: '€120-180', total6Nights: '€720-1,080' },
    { category: 'Food & Drink', perDay: '€50-80', total6Nights: '€300-480' },
    { category: 'Attractions & Tours', perDay: '€20-40', total6Nights: '€120-240' },
    { category: 'Transport (Salzburg Card + car rental)', perDay: '€25-40', total6Nights: '€150-240' },
    { category: 'Total per person', perDay: '€215-340', total6Nights: '€1,290-2,040' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: [
      'Salzburg Airport (SZG) is 4km from the city center — buses 2 and 10 reach the Altstadt in 20 minutes',
      'Alternative: Fly into Munich (MUC) and take the 1.5h train to Salzburg Hauptbahnhof',
      'Vienna is 2.5h by ÖBB Railjet train — scenic ride through the Alps'
    ]},
    { title: '🚗 Car Rental & Transport', items: [
      'Car rental essential for day trips to Hallstatt and Werfen — book at airport or Hauptbahnhof',
      'Austrian motorways require a vignette toll sticker (€9.90 for 10 days, buy at gas stations)',
      'Parking in the Altstadt is limited — use Mönchsberggarage (€18/day)',
      'Within Salzburg, walk or use the excellent bus network (included in Salzburg Card)'
    ]},
    { title: '🎫 Salzburg Card', items: [
      '24h (€30), 48h (€39), 72h (€45) — buy at the tourist office or online',
      'Covers all museums, fortress funicular, Hellbrunn, Untersberg cable car, river cruise, and public transport',
      'Pays for itself easily in one full sightseeing day'
    ]},
    { title: '💶 Tipping & Payments', items: [
      'Round up or add 5-10% at restaurants',
      'Say the total you want to pay when handing cash: "Stimmt so" (keep the change) or state the rounded amount',
      'Cards accepted most places but carry cash for beer gardens and market stalls'
    ]},
    { title: '🎵 Salzburg Festival', items: [
      'Runs mid-July through August — world-class opera, concerts, theater',
      'Major opera tickets sell out months ahead, but smaller concerts and Jedermann on Domplatz are easier to get',
      'Free open-air screenings most evenings in Kapitelplatz — check salzburgerfestspiele.at'
    ]},
    { title: '🏥 Emergency & Health', items: [
      'EU emergency number: 112',
      'Nearest hospital: Universitätsklinikum Salzburg (Müllner Hauptstraße 48)',
      'Pharmacies (Apotheke) rotate for night/weekend duty — check apothekenindex.at',
      'Tap water is pristine Alpine spring water — drink it everywhere'
    ]}
  ]
};

// Execute
const result = fulfillOrder(order, itineraryData);
console.log('✅ Itinerary fulfilled!');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('File:', result.filePath);
