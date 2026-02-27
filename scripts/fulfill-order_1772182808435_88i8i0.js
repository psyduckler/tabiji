const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772182808435_88i8i0',
  email: 'wathenconnor09@gmail.com',
  destination: 'Switzerland',
  startDate: '2026-07-15',
  endDate: '2026-07-29',
  groupSize: '3-4',
  travelStyle: 'Adventure, Family-friendly',
  dining: 'Casual throughout',
  budget: '$2,000-5,000',
  requests: ''
};

const itineraryData = {
  destination: 'Switzerland',
  countryEmoji: '🇨🇭',
  title: 'Switzerland: Alpine Adventure for the Family',
  subtitle: '14 days of mountain peaks, turquoise lakes & unforgettable adventures',
  description: 'Switzerland in summer is a playground unlike any other — snow-capped peaks reflected in emerald lakes, cable cars soaring above wildflower meadows, and postcard-perfect villages where cowbells echo through crisp mountain air. This itinerary takes a group of 3-4 on an adventure-packed journey through Zurich, Lucerne, Interlaken, the Jungfrau region, Zermatt, and Bern. From riding the world\'s highest railway to Jungfraujoch and hiking past Trümmelbach Falls, to spotting the iconic Matterhorn and swimming in glacier-fed lakes — every day delivers wonder. It\'s Switzerland at its most thrilling, accessible, and family-friendly.',
  duration: '14 days',
  dates: 'Jul 15 – Jul 29, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Families & Adventure Seekers',
  highlights: [
    'Jungfraujoch — Top of Europe at 3,454m',
    'Matterhorn views from Gornergrat railway',
    'Paragliding over Interlaken\'s green valley',
    'First Cliff Walk above Grindelwald',
    'Trümmelbach Falls inside a living glacier',
    'Swimming in Lake Lucerne and Lake Thun',
    'Bern\'s medieval Old Town & Bear Park'
  ],

  essentials: [
    { title: '🏔️ Summer in the Alps', text: 'July is peak season with warm valley temps (20-28°C) and mountain highs of 5-15°C. Pack layers — mornings and evenings are cool even at lower altitudes. Sunscreen is essential at altitude.' },
    { title: '🚂 Swiss Travel Pass', text: 'A Swiss Travel Pass covers trains, buses, boats, and most mountain railways. For 14 days, a Family Card means children under 16 travel free with parents. Buy before arrival for the best price.' },
    { title: '💰 Budget Tips', text: 'Switzerland is expensive but manageable. Save on meals with supermarket lunches (Migros & Coop are excellent), picnic by lakes, and use the Swiss Travel Pass to avoid individual ticket costs. Book mountain attractions early — Jungfraujoch sells out.' },
    { title: '🎒 What to Pack', text: 'Sturdy walking shoes or light hiking boots are essential. Pack a waterproof jacket, sunglasses, sunscreen SPF50+, and a reusable water bottle (tap water is pristine everywhere). Children will want a daypack for summit snacks.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-07-15',
      neighborhoods: 'Zurich · Old Town (Altstadt) · Lake Zurich',
      title: 'Arrival in Zurich — City, Spires & Lake',
      description: 'Touch down in Switzerland and ease into the trip with a stroll through Zurich\'s beautifully preserved medieval Old Town, a glimpse of the shimmering Limmat River, and a first taste of Swiss culture.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Explore Zurich Altstadt',
              description: 'Check into your hotel and head straight to the Old Town. Cross the Münsterbrücke bridge, wander the cobblestone lanes of Niederdorf, and visit the Grossmünster cathedral with its twin towers overlooking the river.',
              details: [
                '🏨 Stay near the main station (Hauptbahnhof) for easy onward travel',
                '⛪ Grossmünster — climb the tower for panoramic city views (small fee)',
                '🛍️ Niederdorf is the charming pedestrian heart of Zurich'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Zurich\'s tap water is some of the best in the world — use the free public fountains throughout the city. Fill up your water bottles here.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lakeside Stroll at Lake Zurich',
              description: 'Walk along the Zürichsee promenade for stunning views of the lake and distant Alps. In summer, the lake is open for swimming at the Seebad Enge or Strandbad Mythenquai — perfect for kids.',
              details: [
                '🏊 Public lidos (Badis) are a Swiss institution — entry is a few francs',
                '🌅 The lake promenade glows beautifully at golden hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Zeughauskeller',
              description: 'A beloved Zurich institution in a 15th-century armoury. Giant portions of rösti, sausages, and Swiss classics at reasonable prices. Perfect for a hungry group just off the plane.',
              meta: '💰 $$ · 📍 Bahnhofstrasse 28a, Zurich · No reservations — just show up'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.3769, lng: 8.5417, label: 'Zurich Hauptbahnhof', num: 1, cat: 'attraction', desc: 'Central station — gateway to all of Switzerland' },
        { lat: 47.3700, lng: 8.5440, label: 'Grossmünster', num: 2, cat: 'attraction', desc: 'Twin-towered cathedral with city views' },
        { lat: 47.3650, lng: 8.5434, label: 'Lake Zurich Promenade', num: 3, cat: 'attraction', desc: 'Scenic lakeside walk with mountain backdrop' },
        { lat: 47.3725, lng: 8.5391, label: 'Zeughauskeller', num: 4, cat: 'food', desc: 'Classic Swiss fare in a historic armoury' }
      ]
    },
    {
      num: 2,
      date: '2026-07-16',
      neighborhoods: 'Zurich · Rhine Falls · Stein am Rhein',
      title: 'Rhine Falls — Europe\'s Most Powerful Waterfall',
      description: 'A day trip to the thundering Rhine Falls at Schaffhausen, one of Europe\'s most spectacular natural wonders. Kids will love the boat ride right up to the crashing falls — then explore the perfectly preserved medieval town of Stein am Rhein.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rhine Falls by Boat',
              description: 'Train to Schaffhausen and then to Neuhausen. Board a small boat that takes you right up to the central rock in the middle of the falls — the roar and spray are unforgettable, and there\'s a flag at the top to claim.',
              details: [
                '🚂 45-min train from Zurich — included with Swiss Travel Pass',
                '⛵ Boat rides run frequently — get there early to avoid queues',
                '📸 Best photo: from the Schloss Laufen lookout platform above the falls'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Bring a rain poncho or accept getting wet — the boats get close enough that spray is inevitable. The kids will love it.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Stein am Rhein Medieval Town',
              description: 'A short train ride brings you to Stein am Rhein, one of Switzerland\'s best-preserved medieval towns. The main square (Rathausplatz) is lined with elaborately painted half-timbered buildings — it looks almost too perfect to be real.',
              details: [
                '🏘️ The frescoed buildings of Rathausplatz are extraordinary',
                '🏰 Hohenklingen Castle above town has sweeping Rhine views',
                '🍦 Stop for ice cream on the square — a ritual for all Swiss towns'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Restaurant zum Rebstock',
              description: 'Traditional Swiss restaurant in Stein am Rhein with Rhine views and hearty lunch menus. Great for refuelling after the falls.',
              meta: '💰 $$ · 📍 Rathausplatz, Stein am Rhein'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Zurich',
              description: 'Head back to Zurich for an early dinner and rest. Tomorrow is a travel day to Lucerne.',
              details: ['🚂 Direct trains back to Zurich Hauptbahnhof every 30 minutes']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tibits Zurich',
              description: 'Popular Swiss vegetarian buffet restaurant — pay by weight, eat as much as you want. Excellent for families with varied tastes.',
              meta: '💰 $ · 📍 Seefeldstrasse 2, Zurich'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.6773, lng: 8.6152, label: 'Rhine Falls', num: 1, cat: 'attraction', desc: 'Europe\'s most powerful waterfall — boat rides to the central rock' },
        { lat: 47.6579, lng: 8.8613, label: 'Stein am Rhein', num: 2, cat: 'attraction', desc: 'Perfectly preserved medieval town with frescoed buildings' },
        { lat: 47.6579, lng: 8.8600, label: 'Rathausplatz', num: 3, cat: 'attraction', desc: 'Stunning medieval square with painted half-timbered houses' }
      ]
    },
    {
      num: 3,
      date: '2026-07-17',
      neighborhoods: 'Lucerne · Old Town · Chapel Bridge',
      title: 'Lucerne — Chapel Bridge & Lakeside Magic',
      description: 'Travel to Lucerne, consistently rated one of Switzerland\'s most beautiful cities. The medieval Chapel Bridge, the dramatic Lion Monument, and the shimmering Lake Lucerne make this a highlight of any Swiss trip.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Lucerne & Chapel Bridge',
              description: 'A scenic 1-hour train from Zurich brings you to Lucerne. Drop your bags and head straight to the famous Chapel Bridge (Kapellbrücke) — a 14th-century covered wooden bridge with painted panels depicting Swiss history.',
              details: [
                '🚂 Direct train Zurich → Lucerne, 50 minutes, included with pass',
                '🌉 Chapel Bridge is the most-photographed bridge in Switzerland',
                '📸 Best view: from the opposite bank in the morning light'
              ]
            },
            {
              title: 'Lucerne Old Town Walk',
              description: 'Wander the car-free medieval Old Town with its painted buildings, guild fountains, and medieval walls. Climb the Musegg Wall — a 900-year-old fortification with nine towers — for views over the city and lake.',
              details: [
                '🏰 Musegg Wall — free to walk, open in summer',
                '⛪ Jesuit Church — the ornate baroque interior is stunning and free',
                '🛒 Weekly markets on the Weinmarkt square'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Wirtshaus Galliker',
              description: 'Beloved local institution serving classic Lucerne specialties since 1856. Try the Luzerner Chügelipastete (a pastry shell filled with meat and mushroom ragout) — a local delicacy.',
              meta: '💰 $$ · 📍 Schützenstrasse 1, Lucerne · Closed weekends'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lion Monument & Swiss Museum of Transport',
              description: 'The Lion Monument (Löwendenkmal) is a powerful 19th-century sculpture carved into a cliff face, commemorating the Swiss Guards who died in 1792. Then visit the brilliant Swiss Museum of Transport — interactive, great for kids with flight simulators and real trains.',
              details: [
                '🦁 The Lion Monument — Mark Twain called it "the most mournful piece of stone in the world"',
                '🚂 Swiss Museum of Transport — allow 2+ hours, kids love it',
                '🚢 Museum is lakeside — nice for a post-visit walk'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lake Lucerne Sunset Cruise',
              description: 'Board an evening paddle steamer for a sunset cruise on Lake Lucerne. The surrounding Pilatus and Rigi mountains reflected on the water are simply magical. Several historic Belle Époque steamers operate on the lake.',
              details: [
                '🚢 Swiss Travel Pass covers SGV lake boats — no extra cost',
                '🌅 Evening departures from 5-7pm offer the best light',
                '⛰️ Spot Mt. Pilatus and Mt. Rigi from the water'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Schiff',
              description: 'Right on the river Reuss in the Old Town, with outdoor terrace seating and classic Swiss-German cuisine. Relaxed, family-friendly atmosphere.',
              meta: '💰 $$ · 📍 Unter der Egg 8, Lucerne'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.0520, lng: 8.3071, label: 'Chapel Bridge (Kapellbrücke)', num: 1, cat: 'attraction', desc: '14th-century covered wooden bridge — most iconic in Switzerland' },
        { lat: 47.0543, lng: 8.3108, label: 'Musegg Wall', num: 2, cat: 'attraction', desc: '900-year-old medieval fortification with tower climbs' },
        { lat: 47.0583, lng: 8.3076, label: 'Lion Monument', num: 3, cat: 'attraction', desc: 'Majestic carved lion in a natural cliff face — deeply moving' },
        { lat: 47.0510, lng: 8.3257, label: 'Swiss Museum of Transport', num: 4, cat: 'attraction', desc: 'Interactive transport museum — great for kids' },
        { lat: 47.0523, lng: 8.3085, label: 'Wirtshaus Galliker', num: 5, cat: 'food', desc: 'Lucerne institution since 1856 — try the Kügeli Pastete' }
      ]
    },
    {
      num: 4,
      date: '2026-07-18',
      neighborhoods: 'Lucerne · Mt. Pilatus · Lake Lucerne',
      title: 'Mt. Pilatus — Dragon Country Above the Clouds',
      description: 'Take the world\'s steepest cogwheel railway up to Mt. Pilatus at 2,132m. Above the clouds, walk the summit ridge trails for jaw-dropping views over Lake Lucerne and dozens of Alpine peaks.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Pilatus Cogwheel Railway Ascent',
              description: 'From Alpnachstad (boat from Lucerne), board the world\'s steepest cogwheel railway (48° gradient!) to the Pilatus summit. The journey up through forests, meadows, and rocky cliffs is an adventure in itself.',
              details: [
                '🚢 Boat from Lucerne to Alpnachstad — scenic, included with pass',
                '🚂 Cogwheel railway — 30 minutes up through dramatic scenery',
                '🎟️ Pilatus railway NOT included in Swiss Travel Pass — budget ~CHF 75/person for round trip'
              ]
            },
            {
              title: 'Pilatus Summit Walk',
              description: 'At the top, walk the 30-minute Esel-Tomlishorn summit trail along the ridge between the two peaks. Below you, Lake Lucerne shimmers and on clear days you can see the Bernese Alps, Black Forest, and Vosges mountains.',
              details: [
                '⛰️ Summit is at 2,132m — bring layers, it\'s cooler than the valley',
                '🦅 Paragliders launch from here — watch (or join!) the pros',
                '🐉 Legend says dragons lived on Pilatus — the area is called Dragon Country'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Restaurant Pilatus-Kulm',
              description: 'Lunch with a view at 2,000m. The terrace restaurant offers hot meals and stunning panoramas. Nothing beats a warm soup when you\'re above the clouds.',
              meta: '💰 $$$ · 📍 Pilatus Summit · Part of the Pilatus complex'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gondola & Cable Car Descent to Kriens',
              description: 'Descend by aerial cable car and gondola to Kriens — a completely different descent route with new perspectives. Then bus back to Lucerne for the afternoon.',
              details: [
                '🚡 The gondola section is open and thrilling — amazing views',
                '⏰ Allow 2 hours for the full descent experience',
                '🚌 Bus 1 from Kriens back to Lucerne city centre'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lake Lucerne Swimming',
              description: 'After a big mountain day, cool off with a swim at Lido Lucerne on the lake. The grassy lawns, diving platform, and clear water make it perfect for kids and adults alike.',
              details: [
                '🏊 Lido Lucerne — outdoor pool and lake swimming, small entry fee',
                '🌅 Evening light on the lake is beautiful after 6pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bellini',
              description: 'Great Italian on the lakefront — pizza, pasta, and salads in a relaxed setting. Popular with families and very reasonably priced by Swiss standards.',
              meta: '💰 $$ · 📍 Haldenstrasse 4, Lucerne'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.9792, lng: 8.2534, label: 'Alpnachstad (Pilatus Railway Base)', num: 1, cat: 'attraction', desc: 'Departure point for the world\'s steepest cogwheel railway' },
        { lat: 46.9786, lng: 8.2527, label: 'Mt. Pilatus Summit (2,132m)', num: 2, cat: 'attraction', desc: 'Dragon Country summit with panoramic Alpine views' },
        { lat: 47.0230, lng: 8.2889, label: 'Kriens Gondola Base', num: 3, cat: 'attraction', desc: 'Lower terminus for the cable car descent' },
        { lat: 47.0434, lng: 8.3363, label: 'Lido Lucerne', num: 4, cat: 'attraction', desc: 'Lakeside lido for a refreshing swim after the mountain' }
      ]
    },
    {
      num: 5,
      date: '2026-07-19',
      neighborhoods: 'Interlaken · Lake Thun · Lake Brienz',
      title: 'Interlaken — Between Two Lakes, at the Foot of Giants',
      description: 'Travel to Interlaken, the adventure capital of Switzerland, dramatically positioned between Lake Thun and Lake Brienz with the Eiger, Mönch, and Jungfrau towering above. Settle in, swim in the lakes, and explore the town.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Scenic Train from Lucerne to Interlaken',
              description: 'The Brünig Pass route from Lucerne to Interlaken is one of Switzerland\'s most scenic train journeys — passing through forests, mountain villages, and along lake shores.',
              details: [
                '🚂 Lucerne → Interlaken Ost, 2 hours via Brünig Pass — sit on the right side',
                '📸 Lake Brienz appears suddenly in all its turquoise glory',
                '✅ Fully covered by Swiss Travel Pass'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Thun Boat Trip & Spiez Castle',
              description: 'Jump on a lake boat from Interlaken West to Spiez, where a 14th-century castle sits dramatically on a vineyard peninsula jutting into Lake Thun. The lake\'s turquoise water is perfect for a swim off the boat dock.',
              details: [
                '🚢 Lake Thun boats included with Swiss Travel Pass',
                '🏰 Spiez Castle (Schloss Spiez) — walk the vineyard to the castle',
                '🏊 Swim from the castle docks — the water is crystal clear and cold!'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Restaurant Schloss Spiez',
              description: 'Lunch at the castle restaurant with stunning lake and mountain views. Local lake fish (Felchen) and seasonal salads.',
              meta: '💰 $$$ · 📍 Schlossstrasse 16, Spiez'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Höhematte Park & Jungfrau Views',
              description: 'Return to Interlaken and stroll the famous Höhematte park — a large green meadow in the town centre with perfect framed views of the Jungfrau massif. Watch paragliders land here all afternoon.',
              details: [
                '🪂 Paragliders land on Höhematte — a wonderful free spectacle',
                '⛰️ On a clear evening, the Jungfrau turns pink at alpenglow',
                '🛒 Interlaken\'s main street has Swiss souvenirs and sports shops'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'El Azteca',
              description: 'Beloved casual Mexican restaurant in Interlaken — generous portions, great for groups. Reliably good and very popular with travellers.',
              meta: '💰 $ · 📍 Jungfraustrasse 30, Interlaken · Cash preferred'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.6863, lng: 7.8632, label: 'Interlaken Ost Station', num: 1, cat: 'attraction', desc: 'Gateway to the Jungfrau region — adventure capital of Switzerland' },
        { lat: 46.6865, lng: 7.6618, label: 'Spiez Castle', num: 2, cat: 'attraction', desc: '14th-century castle on a vineyard peninsula over Lake Thun' },
        { lat: 46.6864, lng: 7.8510, label: 'Höhematte Park', num: 3, cat: 'attraction', desc: 'Green meadow with paraglider landing and Jungfrau views' },
        { lat: 46.6876, lng: 7.8524, label: 'El Azteca', num: 4, cat: 'food', desc: 'Casual Mexican — great for groups, very popular' }
      ]
    },
    {
      num: 6,
      date: '2026-07-20',
      neighborhoods: 'Jungfraujoch · Grindelwald · First',
      title: 'Top of Europe — Jungfraujoch at 3,454m',
      description: 'The crown jewel of any Switzerland trip — the Jungfraujoch railway climbs to the highest train station in Europe. Snow, glaciers, and views stretching to France and Germany await at the "Top of Europe."',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Jungfraujoch Summit Experience',
              description: 'Take the early morning train from Interlaken to Grindelwald, then the Eiger Express gondola and Jungfrau railway to the top. At 3,454m, you can walk on the Aletsch Glacier, explore ice tunnels, and see views that will stay with you forever.',
              details: [
                '🚂 Leave Interlaken by 8am for the best snow conditions and views',
                '🎟️ Budget ~CHF 145/adult — book online early (Swiss Travel Pass discount available)',
                '🥶 It\'s below freezing at the top — bring proper warm layers even in July',
                '❄️ Aletsch Glacier — Europe\'s longest glacier at 23km',
                '🐕 Sphinx Observatory — 360° views from an outdoor terrace at the summit'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Altitude can cause mild headaches at 3,454m, especially for children. Take it slow at the top, drink water, and eat something warm. Most people feel fine after 20-30 minutes.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'First Cliff Walk, Grindelwald',
              description: 'Descend to Grindelwald and take the First gondola up to the First Cliff Walk — a series of steel walkways bolted onto the cliff face at 2,168m. The views of Grindelwald and the Eiger are extraordinary. Brave souls can try the First Flyer zip line.',
              details: [
                '🚡 First gondola from Grindelwald village — 25 minutes to the top',
                '🪂 First Flyer zip line — 84 km/h over the valley (minimum age 6, weight limits apply)',
                '🛷 First Glider and Mountain Cart also available for adrenaline-seekers',
                '🎟️ Cliff Walk is free; Flyer and other rides extra'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Restaurant First Mountain',
              description: 'Casual self-service mountain restaurant at First with panoramic Eiger views. Warm soups, pasta, and Swiss classics.',
              meta: '💰 $$ · 📍 First Mountain, Grindelwald'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Grindelwald Village Evening Walk',
              description: 'Wander through Grindelwald village with its classic Swiss chalets, flower-draped balconies, and the imposing Eiger North Face looming above. A beautiful, peaceful evening after a big day at altitude.',
              details: [
                '⛰️ The Eiger North Face right above the village is awe-inspiring',
                '🌸 July meadows are thick with wildflowers and grazing cows',
                '🚂 Trains back to Interlaken run until late evening'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Alte Post',
              description: 'Cozy mountain restaurant in a historic chalet in Grindelwald. Great fondue, rösti, and local specialties after a big mountain day.',
              meta: '💰 $$ · 📍 Dorfstrasse 10, Grindelwald'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.5474, lng: 7.9854, label: 'Jungfraujoch (3,454m)', num: 1, cat: 'attraction', desc: 'Top of Europe — highest railway station in Europe, glacier walks' },
        { lat: 46.6240, lng: 8.0413, label: 'Grindelwald Village', num: 2, cat: 'attraction', desc: 'Classic Alpine village beneath the imposing Eiger' },
        { lat: 46.6493, lng: 8.0427, label: 'First Cliff Walk (2,168m)', num: 3, cat: 'attraction', desc: 'Clifftop walkways and zip line with Eiger panoramas' },
        { lat: 46.6240, lng: 8.0500, label: 'Eiger Express Gondola Base', num: 4, cat: 'attraction', desc: 'Fast gondola connection to the Jungfraujoch railway' }
      ]
    },
    {
      num: 7,
      date: '2026-07-21',
      neighborhoods: 'Interlaken · Lauterbrunnen Valley · Trümmelbach',
      title: 'Lauterbrunnen — Valley of 72 Waterfalls',
      description: 'Descend into the Lauterbrunnen valley — the inspiration for Tolkien\'s Rivendell. Seventy-two waterfalls cascade off sheer cliffs, and inside a mountain, the roaring Trümmelbach Falls drain the entire Jungfrau glacier.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Lauterbrunnen Village & Staubbach Falls',
              description: 'Take the train into the Lauterbrunnen valley and prepare to be overwhelmed. The Staubbach Falls plunge 297m off the cliff directly above the village — one of Europe\'s highest free-falling waterfalls. Walk behind the falls for a magical perspective.',
              details: [
                '🚂 Train from Interlaken Ost to Lauterbrunnen — 20 minutes',
                '💧 Staubbach Falls: walkable path leads behind the curtain of water',
                '📸 The valley walls rise 1,000m on both sides — utterly dramatic'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Trümmelbach Falls Inside the Mountain',
              description: 'A short bus or walk leads to Trümmelbach Falls — ten glacier waterfalls inside a living mountain, draining 20,000 litres of water per second from the Jungfrau glacier. You take a tunnel lift inside the cliff and walk through the thundering caverns.',
              details: [
                '🚌 Bus 141 from Lauterbrunnen to Trümmelbach — 10 minutes',
                '🎟️ Entry ~CHF 14/adult, CHF 7/child — absolutely worth every franc',
                '💧 The sound and power of the water inside the rock is unforgettable',
                '🧥 Wear a jacket — it\'s cool and misty inside the gorge tunnels'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Hotel Restaurant Staubbach',
              description: 'Classic Swiss lunch in Lauterbrunnen village — great rösti, soups, and the falls as a backdrop.',
              meta: '💰 $$ · 📍 Lauterbrunnen village centre'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening in Lauterbrunnen & Return',
              description: 'As the day-trippers leave, the valley takes on an ethereal quality in the evening light. Watch BASE jumpers launch from the cliffs, listen to the roar of the falls, and soak it all in.',
              details: [
                '🪂 Lauterbrunnen is a world-famous BASE jumping destination — watch from the valley',
                '🌙 The valley glows gold in the evening — magical photography',
                '🚂 Last trains to Interlaken run until 11pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Airtime Bar & Grill',
              description: 'Lively spot in Lauterbrunnen popular with adventurers and families. Burgers, wraps, and Swiss dishes — great atmosphere after a full day.',
              meta: '💰 $ · 📍 Lauterbrunnen village'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.5936, lng: 7.9084, label: 'Lauterbrunnen Village', num: 1, cat: 'attraction', desc: 'Valley of 72 waterfalls — Tolkien\'s Rivendell inspiration' },
        { lat: 46.5948, lng: 7.9073, label: 'Staubbach Falls', num: 2, cat: 'attraction', desc: '297m free-falling waterfall — walk behind the curtain' },
        { lat: 46.5735, lng: 7.9196, label: 'Trümmelbach Falls', num: 3, cat: 'attraction', desc: 'Ten glacier waterfalls inside a living mountain — unmissable' }
      ]
    },
    {
      num: 8,
      date: '2026-07-22',
      neighborhoods: 'Interlaken · Paragliding · Lake Brienz',
      title: 'Fly Over the Alps — Paragliding & Lake Brienz',
      description: 'An adrenaline morning soaring over Interlaken on a tandem paraglide, then a relaxing afternoon on the turquoise shores of Lake Brienz — one of the most beautiful lakes in Europe.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tandem Paragliding over Interlaken',
              description: 'Launch from Beatenberg (1,100m) with an experienced pilot and glide over the Interlaken valley with the Eiger, Mönch, and Jungfrau spread before you. The 15-20 minute flight is smooth, scenic, and safe for all ages (6+).',
              details: [
                '🪂 Paragliding Interlaken or Alpin Air are reputable operators',
                '💰 ~CHF 175/person for a tandem flight — worth every franc',
                '📸 Pilots carry cameras and will photograph/film your flight',
                '👶 Minimum age typically 6 years; no experience needed'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book your paragliding the day before and confirm the weather forecast. July usually has excellent flying conditions. Morning flights have the calmest air.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Brienz — Swimming & Paddle Boats',
              description: 'Take the train to Brienz and spend the afternoon at this stunning turquoise lake. Rent paddle boats or kayaks, swim in the impossibly clear water, and relax on the wooden docks.',
              details: [
                '🚂 Train from Interlaken Ost to Brienz — 20 minutes',
                '🏊 Strandbad Brienz — public lido with clear lake swimming',
                '🚣 Kayak and paddle boat rentals available at the boat dock',
                '📸 The village reflection in the turquoise water is like a painting'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Restaurant Strandhotel Belvedere',
              description: 'Right on the lake in Brienz with an outdoor terrace over the water. Fresh fish, salads, and ice cold drinks in paradise.',
              meta: '💰 $$$ · 📍 Hauptstrasse 110, Brienz'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ballenberg Open-Air Museum',
              description: 'Just outside Brienz, the Ballenberg Open-Air Museum preserves over 100 original Swiss farmhouses, barns, and mills from across the country. Watch traditional crafts like cheese-making, wood-carving, and weaving.',
              details: [
                '🏘️ 66 hectares of authentic Swiss rural heritage — great for kids',
                '🧀 Watch live cheese-making and bread baking demonstrations',
                '⏰ Allow 2-3 hours — there\'s a lot to see'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pizzeria San Marco',
              description: 'Reliable Italian back in Interlaken with wood-fired pizzas and pasta. A casual, filling dinner after an adventure-packed day.',
              meta: '💰 $ · 📍 Interlaken town centre'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.7058, lng: 7.8025, label: 'Paragliding Launch (Beatenberg)', num: 1, cat: 'attraction', desc: 'Tandem paragliding launch with Jungfrau panorama' },
        { lat: 46.6700, lng: 7.8050, label: 'Paragliding Landing (Höhematte)', num: 2, cat: 'attraction', desc: 'Landing zone in Interlaken\'s central park' },
        { lat: 46.7468, lng: 7.9895, label: 'Lake Brienz', num: 3, cat: 'attraction', desc: 'Turquoise glacial lake — kayaking, swimming, and paddle boats' },
        { lat: 46.7530, lng: 8.0300, label: 'Ballenberg Open-Air Museum', num: 4, cat: 'attraction', desc: 'Historic Swiss farmhouses and traditional crafts demonstrations' }
      ]
    },
    {
      num: 9,
      date: '2026-07-23',
      neighborhoods: 'Zermatt · Matterhorn · Gornergrat',
      title: 'Zermatt — Face to Face with the Matterhorn',
      description: 'Travel to Zermatt, the car-free mountain town at the foot of the iconic Matterhorn (4,478m). Take the Gornergrat railway for astonishing 360° views of 29 peaks over 4,000m.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Scenic Train to Zermatt',
              description: 'An unforgettable 3.5-hour journey from Interlaken through Brig and up to Zermatt. The final approach through the Mattertal valley is electric — the Matterhorn suddenly appears as you round a bend.',
              details: [
                '🚂 Interlaken Ost → Zermatt, ~2.5-3h via Brig — seat reservations recommended',
                '🚫 Zermatt is car-free — electric taxis only. Park at Täsch and take a shuttle',
                '⛰️ Your first view of the Matterhorn from the station will stop you in your tracks'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gornergrat Railway — 29 Peaks Over 4,000m',
              description: 'Board Europe\'s highest open-air cog railway up to Gornergrat (3,089m). The panorama is extraordinary: the Matterhorn directly ahead, the Monte Rosa massif, Lyskamm, and the vast Gorner Glacier below. This is arguably the finest mountain view in Switzerland.',
              details: [
                '🎟️ ~CHF 94/adult round trip — Swiss Travel Pass gives 50% discount',
                '🚂 8 stops on the way up — each reveals a new angle on the Matterhorn',
                '⛰️ Gorner Glacier visible from the summit — the second largest glacier in the Alps',
                '🔭 Telescopes at the summit for close-up Matterhorn views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kulmhotel Gornergrat',
              description: 'Lunch at the summit hotel at 3,089m with direct Matterhorn views from every seat. The mountain view while eating is surreal.',
              meta: '💰 $$$ · 📍 Gornergrat Summit, 3,089m'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Zermatt Village & Matterhorn Alpenglow',
              description: 'Explore Zermatt\'s charming traffic-free village, browse the mountain sports shops, and find a terrace facing the Matterhorn for the magical alpenglow — when the peak turns fiery red at sunset.',
              details: [
                '🌅 Alpenglow on the Matterhorn peak is one of the world\'s great natural shows',
                '🏘️ The old village (Hinterdorf) has beautiful preserved wooden chalets',
                '🍫 Pick up Zermatt-branded Swiss chocolate as a souvenir'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Whymper-Stube',
              description: 'Named after the first man to summit the Matterhorn, this cozy restaurant serves excellent fondue and raclette in a warm, atmospheric setting.',
              meta: '💰 $$ · 📍 Bahnhofstrasse 80, Zermatt'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.0207, lng: 7.7491, label: 'Zermatt Village', num: 1, cat: 'attraction', desc: 'Car-free Alpine village at the foot of the Matterhorn' },
        { lat: 45.9836, lng: 7.7423, label: 'Matterhorn (4,478m)', num: 2, cat: 'attraction', desc: 'The most iconic mountain in the world' },
        { lat: 45.9832, lng: 7.7854, label: 'Gornergrat (3,089m)', num: 3, cat: 'attraction', desc: 'Panorama of 29 peaks including the Matterhorn and Monte Rosa' },
        { lat: 46.0207, lng: 7.7491, label: 'Restaurant Whymper-Stube', num: 4, cat: 'food', desc: 'Atmospheric fondue and raclette — Matterhorn history on the walls' }
      ]
    },
    {
      num: 10,
      date: '2026-07-24',
      neighborhoods: 'Zermatt · Schwarzsee · Matterhorn Glacier Paradise',
      title: 'Zermatt Adventures — Glacier Paradise & Alpine Hikes',
      description: 'A full day in the Zermatt area with access to the highest cable car in the Alps — the Matterhorn Glacier Paradise at 3,883m — plus a beautiful hike through wildflower meadows to the Schwarzsee lake at the base of the Matterhorn.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matterhorn Glacier Paradise (3,883m)',
              description: 'The highest cable car station in the Alps brings you to a glacier viewing platform at 3,883m. Look down at the 14 glaciers and across borders into Italy and France. The Ice Palace carved inside the glacier is a favourite with kids.',
              details: [
                '🚡 Cable car from Zermatt — multiple stages, about 45 minutes total',
                '🎟️ ~CHF 110/adult — Swiss Travel Pass gives 50% discount',
                '🧊 Ice Palace inside the glacier — sculptures carved from ice',
                '🥶 At 3,883m it can be very cold even in July — bring serious layers'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Schwarzsee Hike & Matterhorn Views',
              description: 'Descend to Schwarzsee (2,583m) and hike the 2-hour Schwarzsee loop trail around the lake with a permanent reflection of the Matterhorn in the water. The closest you can safely get to the base of the mountain on foot.',
              details: [
                '🏔️ Schwarzsee — "Black Lake" sitting directly below the Matterhorn',
                '🥾 2-hour moderate hike suitable for families with older children',
                '📸 The Matterhorn reflection in the lake is breathtaking',
                '🌸 July wildflowers at this altitude are spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Hotel Schwarzsee Restaurant',
              description: 'Simple mountain restaurant right at the lake with unbeatable Matterhorn views. Hot food, snacks, and the best view in the Alps.',
              meta: '💰 $$ · 📍 Schwarzsee, 2,583m'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Zermatt Spa & Mountain Museum',
              description: 'After two big mountain days, unwind at the Matterhorn Museum — a fascinating underground exhibition about Zermatt\'s history and the first Matterhorn ascent in 1865. Then a soak at the RIFFELALP Alpine Wellness if your budget allows.',
              details: [
                '🏛️ Matterhorn Museum (Zermatlantis) — atmospheric underground exhibits',
                '🏔️ The 1865 first ascent story is genuinely gripping — four men died on descent',
                '♨️ Baths in Zermatt area: La Vache Leisure Centre has pool and sauna'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Papperia Pub',
              description: 'Casual and lively Zermatt classic — great pizza, beer, and a fun atmosphere. Popular with mountain guides, locals, and adventurers.',
              meta: '💰 $ · 📍 Steinmattstrasse 34, Zermatt'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.9352, lng: 7.7354, label: 'Matterhorn Glacier Paradise (3,883m)', num: 1, cat: 'attraction', desc: 'Highest cable car in the Alps — ice palace and glacier views' },
        { lat: 45.9830, lng: 7.7171, label: 'Schwarzsee (2,583m)', num: 2, cat: 'attraction', desc: 'Mountain lake with Matterhorn reflection — gentle hike loop' },
        { lat: 46.0207, lng: 7.7491, label: 'Matterhorn Museum', num: 3, cat: 'attraction', desc: 'Fascinating underground museum about the first Matterhorn ascent' }
      ]
    },
    {
      num: 11,
      date: '2026-07-25',
      neighborhoods: 'Bern · Old Town · Bear Park',
      title: 'Bern — Medieval Capital & Bears on the Aare',
      description: 'Travel to Bern, Switzerland\'s charming federal capital and a UNESCO World Heritage Old Town. Explore 6km of medieval arcades, Einstein\'s apartment, the famous Rose Garden, and the Bear Park on the banks of the Aare River.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train from Zermatt to Bern',
              description: 'A beautiful 3-hour journey from Zermatt to Bern via Visp and the Lötschberg tunnel. Arrive in Bern\'s stunning art nouveau station and walk down to the medieval old town.',
              details: [
                '🚂 Zermatt → Bern, ~2.5h via Visp — fully covered by Swiss Travel Pass',
                '🏙️ Bern\'s old town is compact and very walkable — no car needed'
              ]
            },
            {
              title: 'Medieval Arcade Walk & Zytglogge',
              description: 'Bern has 6km of covered arcades (Lauben) lining its medieval streets — the most extensive in the world. Walk from the station to the Zytglogge clock tower, where an animated astronomical clock puts on a show every hour.',
              details: [
                '🕐 Zytglogge astronomical clock — show happens at :58 past the hour',
                '🛍️ The arcades shelter dozens of independent shops, cafés, and bakeries',
                '⛲ Bern\'s colourful 16th-century fountains line the main streets'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kornhauskeller',
              description: 'Magnificent restaurant in a restored 18th-century granary with ornate frescoed ceilings. Mediterranean cuisine in one of the most beautiful dining rooms in Switzerland.',
              meta: '💰 $$$ · 📍 Kornhausplatz 18, Bern'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bear Park & Rose Garden Views',
              description: 'The BernBear Park is home to Bern\'s famous bears (the city symbol since 1191) in a natural riverside habitat. Climb up to the Rosengarten (Rose Garden) — 200 varieties of roses plus a panoramic view over the red-roofed Old Town below.',
              details: [
                '🐻 Bears in a natural setting with the Aare River running below',
                '🌹 Rosengarten — 220 varieties of roses, peak bloom through July',
                '📸 The view from the Rose Garden terrace is the classic Bern postcard shot'
              ]
            },
            {
              title: 'Einstein Museum & Old Town',
              description: 'Albert Einstein lived and worked in Bern, developing his Theory of Relativity here. Visit the Einstein Museum (Historisches Museum) or simply see his apartment at Kramgasse 49 from the street.',
              details: [
                '🔬 Einstein developed special relativity while working at the Bern patent office',
                '🏠 Einstein House at Kramgasse 49 — apartment preserved from 1903-1905',
                '📚 Historisches Museum has a superb Einstein exhibition on the lower level'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Aare River Walk at Sunset',
              description: 'The Aare makes a dramatic oxbow bend around the Old Town. Walk the riverside promenade at sunset and watch the river glow emerald in the evening light. In summer, locals float the Aare in inner tubes — a Bern tradition.',
              details: [
                '🌊 The Aare is glacier-fed and ice cold (15-18°C in summer) — refreshing if brave!',
                '🛶 Locals tube the Aare — you can rent tubes and float the bend',
                '🌅 Sunset views from the Nydeggbrücke bridge are spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Lötschberg',
              description: 'Warm, popular Bernese restaurant known for excellent Swiss specialties and an extensive wine list. Try the Bernese Platter — a lavish spread of cured meats and sauerkraut.',
              meta: '💰 $$ · 📍 Zeughausgasse 16, Bern'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.9480, lng: 7.4474, label: 'Zytglogge Clock Tower', num: 1, cat: 'attraction', desc: 'Medieval astronomical clock — animated show at :58 past the hour' },
        { lat: 46.9465, lng: 7.4598, label: 'BernBear Park', num: 2, cat: 'attraction', desc: 'Bern\'s famous bears in a natural riverside habitat' },
        { lat: 46.9499, lng: 7.4602, label: 'Rose Garden (Rosengarten)', num: 3, cat: 'attraction', desc: '200 rose varieties with panoramic Old Town views' },
        { lat: 46.9482, lng: 7.4514, label: 'Einstein House', num: 4, cat: 'attraction', desc: 'Where Einstein developed the Theory of Relativity' },
        { lat: 46.9481, lng: 7.4484, label: 'Kornhauskeller', num: 5, cat: 'food', desc: 'Stunning 18th-century granary restaurant' }
      ]
    },
    {
      num: 12,
      date: '2026-07-26',
      neighborhoods: 'Bern · Gurten · Emmental',
      title: 'Bern Day Two — Gurten Hill & Swiss Cheese Country',
      description: 'A funicular ride up Gurten hill for bird\'s-eye Bern views, then an afternoon adventure into the rolling Emmental hills — the homeland of Swiss cheese — for a dairy farm visit and a taste of the real Switzerland.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gurten — Bern\'s Local Mountain',
              description: 'Take the Gurtenbahn funicular from Wabern up to the Gurten hill (858m) — Bern\'s own mini mountain. The 360° panorama includes the Old Town below, Lake Thun in the distance, and the full Bernese Alps on clear days.',
              details: [
                '🚡 Gurten funicular from Wabern — 5 minutes up, included with Swiss Travel Pass',
                '⛰️ On clear days, see the Eiger, Mönch, and Jungfrau from the top',
                '🎢 Amusement rides and a toy train on the summit — great for kids',
                '🌳 Beautiful woodland walks and picnic spots on the plateau'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Gurten Pavilion Restaurant',
              description: 'Casual hilltop restaurant with a large sunny terrace and Bernese Alps views. Great for a relaxed lunch with kids.',
              meta: '💰 $$ · 📍 Gurten Summit, Bern'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Emmental Valley & Cheese Dairy',
              description: 'Drive or take a regional train 45 minutes to the Emmental — the rolling green valley that gave Emmentaler cheese to the world. Visit the Emmentaler Schaukäserei (show dairy) in Affoltern to watch cheese being made in traditional copper vats.',
              details: [
                '🧀 Emmentaler Schaukäserei in Affoltern — live cheese-making demonstrations',
                '🚗 40 minutes by car, or train to Burgdorf then bus',
                '🌿 The rolling green hills of Emmental look like a children\'s picture book',
                '🛒 Buy fresh Emmentaler cheese direct from the dairy — exceptional quality'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Bern Federal Palace & Evening Walk',
              description: 'Back in Bern, visit the impressive neo-baroque Federal Palace (Bundeshaus) — free guided tours are available. Then a final evening stroll along the arcaded streets, picking up last-minute Swiss chocolate.',
              details: [
                '🏛️ Federal Parliament building — free tours available (book ahead)',
                '🍫 Confiserie Tschirren on Kramgasse has outstanding Swiss chocolate since 1919',
                '🌙 Bern\'s old town at night, lit by lanterns, is incredibly atmospheric'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Brasserie Bern',
              description: 'Classic Swiss brasserie in the heart of Bern with excellent fondue, local craft beers, and a lively atmosphere. Great way to end your Bern stay.',
              meta: '💰 $$ · 📍 Bahnhofplatz 10, Bern'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.9230, lng: 7.4367, label: 'Gurten Funicular (Wabern)', num: 1, cat: 'attraction', desc: 'Base of the Gurten funicular — Bern\'s local mountain' },
        { lat: 46.9155, lng: 7.4323, label: 'Gurten Summit (858m)', num: 2, cat: 'attraction', desc: '360° views of Bern, Lake Thun, and the Bernese Alps' },
        { lat: 46.9940, lng: 7.7770, label: 'Emmentaler Schaukäserei', num: 3, cat: 'attraction', desc: 'Live cheese-making demonstrations in the homeland of Emmentaler' },
        { lat: 46.9466, lng: 7.4396, label: 'Federal Palace (Bundeshaus)', num: 4, cat: 'attraction', desc: 'Switzerland\'s neo-baroque parliament — free guided tours' }
      ]
    },
    {
      num: 13,
      date: '2026-07-27',
      neighborhoods: 'Lake Geneva · Lausanne · Montreux',
      title: 'Lake Geneva — Château de Chillon & Terraced Vineyards',
      description: 'A scenic day along the shores of Lake Geneva, visiting the fairy-tale Château de Chillon and the UNESCO-listed Lavaux vineyard terraces. The combination of lake, Alps, and ancient castle is pure magic.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Montreux via Lausanne',
              description: 'A beautiful 2-hour train journey from Bern along Lake Geneva. Stop in Lausanne for a quick walk up to the Gothic cathedral, then continue to Montreux — the Riviera of Switzerland.',
              details: [
                '🚂 Bern → Lausanne → Montreux, ~2 hours total — Swiss Travel Pass covers all',
                '⛪ Lausanne Cathedral — free, and the city views from the terrace are spectacular',
                '🌊 The approach to Montreux along the lake with Alps behind is stunning'
              ]
            },
            {
              title: 'Château de Chillon',
              description: 'One of Europe\'s best-preserved medieval castles, sitting on a rocky island jutting into Lake Geneva. Explore the dungeons, battlements, and great halls — the castle inspired Byron\'s poem "The Prisoner of Chillon" in 1816.',
              details: [
                '🏰 Château de Chillon — ~CHF 14/adult, ~CHF 7 for children 6-15, under 6 free',
                '⛵ Best arrival: walk 25 minutes along the lake from Montreux, or take a boat',
                '🗡️ The medieval dungeons where Bonivard was chained are genuinely atmospheric',
                '📖 Lord Byron carved his name on a pillar in 1816 — you can see it'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Restaurant Bon Port, Montreux',
              description: 'Waterfront restaurant in Montreux with Lake Geneva views and local fish (perch, trout). Perfect setting for a leisurely lunch.',
              meta: '💰 $$$ · 📍 Rue du Lac 2, Montreux'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lavaux Vineyard Terraces',
              description: 'The Lavaux is a UNESCO World Heritage Site — 830 hectares of terraced vineyards carved into steep hillsides above Lake Geneva since the 11th century. Walk the Lavaux Vineyard Trail between Chexbres and Rivaz for extraordinary lake and mountain views.',
              details: [
                '🍇 UNESCO-listed since 2007 — some of the world\'s most dramatically sited vineyards',
                '🚂 Train to Chexbres or Grandvaux — walk or take the scenic Lavaux Express (mini-train)',
                '🍷 Small wineries along the trail offer tastings — try Chasselas wine, the local white',
                '📸 The panorama of lake, vineyards, and Alps together is extraordinary'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Montreux Lakefront & Return to Bern',
              description: 'A final golden-hour stroll along the famous Montreux lakefront promenade, past the Freddie Mercury statue (Montreux was his favourite place and home of the legendary Mountain Studios). Then train back to Bern.',
              details: [
                '🎸 Freddie Mercury Statue on the lakefront — a great photo stop',
                '🌅 The sunset over the lake from the Montreux promenade is beautiful',
                '🚂 Direct trains Montreux → Bern every hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant du Marché',
              description: 'Back in Bern for a final dinner at this relaxed market-side restaurant. Great Swiss dishes and local wines in a casual setting.',
              meta: '💰 $$ · 📍 Bern Old Town'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 46.5218, lng: 6.6323, label: 'Lausanne Cathedral', num: 1, cat: 'attraction', desc: 'Gothic cathedral on the hill with lake views' },
        { lat: 46.4142, lng: 6.9278, label: 'Château de Chillon', num: 2, cat: 'attraction', desc: 'Medieval castle on a lake island — inspired Byron\'s Prisoner of Chillon' },
        { lat: 46.4711, lng: 6.7693, label: 'Lavaux Vineyard Terraces', num: 3, cat: 'attraction', desc: 'UNESCO vineyard terraces with panoramic lake views' },
        { lat: 46.4312, lng: 6.9123, label: 'Freddie Mercury Statue', num: 4, cat: 'attraction', desc: 'Iconic lakefront tribute to the Queen frontman who loved Montreux' }
      ]
    },
    {
      num: 14,
      date: '2026-07-28',
      neighborhoods: 'Zurich · Old Town · Farewell',
      title: 'Farewell Zurich — Uetliberg & Last Swiss Moments',
      description: 'Return to Zurich for a final day. Ride up to Uetliberg — Zurich\'s own mountain with a 360° city, lake, and Alps panorama — before a leisurely afternoon of last-minute Swiss chocolate shopping and a celebratory farewell dinner.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Zurich & Uetliberg Summit',
              description: 'Morning train from Bern to Zurich, drop bags at the hotel, and immediately head up Uetliberg (871m) on the S10 train from Zurich HB. A 10-minute forest walk from the station leads to the viewing tower with all of Zurich, the lake, and the Alps spread below.',
              details: [
                '🚂 Bern → Zurich, 60 minutes — covered by Swiss Travel Pass',
                '🚂 Zurich HB → Uetliberg on S10, 23 minutes — also covered!',
                '🏔️ On clear days, you can see Alpine peaks from Säntis to the Jungfrau',
                '📸 The view of Zurich and the lake with Alps behind is exceptional'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Zurich Old Town & Shopping',
              description: 'A relaxed final afternoon in Zurich — browse Bahnhofstrasse for high-end Swiss watches and chocolate, or explore the indie boutiques of Langstrasse. Pick up last-minute souvenirs (Swiss Army knives, Lindt, cow bells) on Niederdorfstrasse.',
              details: [
                '🍫 Sprüngli on Paradeplatz — the finest Zurich chocolate since 1836',
                '🔪 Victorinox Swiss Army knives — iconic souvenirs for everyone',
                '🛍️ Niederdorfstrasse is charming and full of independent shops'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Sternen Grill',
              description: 'Zurich institution serving bratwurst from an outdoor grill since 1963. The best fast casual lunch in the city — locals queue here daily. Have it with rösti and a cold beer.',
              meta: '💰 $ · 📍 Theaterstrasse 22, Zurich · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Lake Zurich Sunset',
              description: 'Take a final stroll along Lake Zurich, swim at Seebad Enge if the weather is warm, and find a lakeside bench to reflect on an extraordinary two weeks in Switzerland. Toast to the mountains, the waterfalls, and the adventure.',
              details: [
                '🏊 Seebad Enge — lovely lido right on the lake, open until 8pm',
                '🌅 Sunset over the lake from General-Guisan-Quai — beautiful',
                '🥂 Grab a lakeside drink at Bar Bederstrasse or Rimini Bar'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Restaurant Haus zum Rüden',
              description: 'Celebrating your last night in a 13th-century guild hall on the Limmat River. Outstanding Swiss cuisine — rack of lamb, lake fish, seasonal game — in a room dripping with history.',
              meta: '💰 $$$$ · 📍 Limmatquai 42, Zurich · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 47.3499, lng: 8.4922, label: 'Uetliberg Summit (871m)', num: 1, cat: 'attraction', desc: 'Zurich\'s local mountain — panorama of the city, lake, and Alps' },
        { lat: 47.3769, lng: 8.5417, label: 'Zurich Hauptbahnhof', num: 2, cat: 'attraction', desc: 'Main station and Bahnhofstrasse shopping start' },
        { lat: 47.3644, lng: 8.5416, label: 'Sprüngli (Paradeplatz)', num: 3, cat: 'food', desc: 'Finest Zurich chocolates and confections since 1836' },
        { lat: 47.3595, lng: 8.5401, label: 'Lake Zurich Lido (Seebad Enge)', num: 4, cat: 'attraction', desc: 'Lovely lakeside lido for a final farewell swim' },
        { lat: 47.3712, lng: 8.5440, label: 'Restaurant Haus zum Rüden', num: 5, cat: 'food', desc: 'Farewell dinner in a 13th-century guild hall on the Limmat' }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
