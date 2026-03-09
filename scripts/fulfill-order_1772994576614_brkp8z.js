const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772994576614_brkp8z',
  email: 'meg.bogatko@gmail.com',
  destination: 'Zürich, Switzerland',
  startDate: '2026-03-14',
  endDate: '2026-03-15',
  groupSize: 2,
  requests: 'I love design, interior design, minimalist style and eco slow life, recommend me restaurants and coffee shops and shops in this style'
};

const itineraryData = {
  destination: 'Zürich, Switzerland',
  countryEmoji: '🇨🇭',
  title: 'Design, Coffee & Slow Living in Zürich',
  subtitle: '2 days of minimalist design, specialty coffee & eco-conscious culture for two',
  description: "Zürich is a quiet powerhouse of design culture — home to the world's leading design museum, iconic sustainable brands like Freitag and QWSTION, award-winning specialty coffee roasters, and a creative district where converted industrial spaces house concept stores and farm-to-table restaurants. This itinerary is curated for a design lover who values thoughtful aesthetics, slow mornings, and the kind of places where every detail has been considered. Think Japanese-inspired coffee bars, eco-fashion boutiques, and minimalist interiors that feel like they belong in a magazine.",
  duration: '1 night',
  dates: 'Mar 14 – Mar 15, 2026',
  budget: '$–$$',
  pace: 'Relaxed',
  bestFor: 'Design Lovers · Couples',
  highlights: [
    'Museum für Gestaltung at Toni-Areal — Switzerland\'s leading design museum',
    'FREITAG Tower — iconic shipping container flagship store with rooftop views',
    'MAME Coffee — award-winning Japanese-Swiss specialty roaster in Kreis 5',
    'Kunsthaus Zürich — world-class art in David Chipperfield\'s stunning expansion',
    'QWSTION Store — sustainable bags & curated design goods on Limmatstrasse'
  ],

  essentials: [
    { title: '🌡️ March Weather', text: 'Mid-March in Zürich is early spring — expect 3–11°C (37–52°F) with a mix of sun and clouds. Layer up with a warm coat, scarf, and comfortable walking shoes. Rain is possible, so bring a compact umbrella.' },
    { title: '🚋 Getting Around', text: 'Zürich\'s tram and bus network is excellent. Buy a 24-hour ZVV pass (CHF 8.80 for Zone 110) — it covers all trams, buses, and local trains. Most design spots are walkable from each other in Kreis 4/5 and the Old Town.' },
    { title: '💳 Money & Tipping', text: 'Switzerland uses Swiss Francs (CHF). Cards accepted almost everywhere. Tipping isn\'t expected but rounding up is appreciated. Budget tip: lunch menus (Tagesmenu) at restaurants are significantly cheaper than dinner.' },
    { title: '🎨 Design Culture', text: 'Zürich is the birthplace of Dada, home to the Swiss Style of graphic design, and headquarters of some of Europe\'s most innovative sustainable brands. The Kreis 5 (Zürich West) district is the creative heart — former industrial buildings now house studios, galleries, and concept stores.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-14',
      neighborhoods: 'Zürich West · Kreis 5 · Viadukt',
      title: 'Design District — Sustainable Brands, Specialty Coffee & Creative Spaces',
      description: "Start your Zürich design immersion in Kreis 5, the city's creative heartbeat. Former factories and railway arches now house Switzerland's most exciting concept stores, sustainable fashion brands, and specialty coffee roasters. This is where minimalist aesthetics meet eco-conscious innovation.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'MAME Coffee — Josefstrasse',
              description: 'Begin your day at MAME, founded by World Brewers Cup champion Emi Fukahori and Mathieu Theis. This Japanese-Swiss specialty roaster serves impeccable pour-overs and espresso in a beautifully minimal space. The attention to detail — from the ceramic cups to the brewing ritual — is pure design thinking in action.',
              details: [
                '📍 Josefstrasse 160, 8005 Zürich — in the heart of Kreis 5',
                '☕ Try the hand-brewed filter coffee — the quality is world-class',
                '🎨 Minimalist interior with Japanese-inspired precision — your kind of place'
              ]
            },
            {
              title: 'Museum für Gestaltung — Toni-Areal',
              description: 'Switzerland\'s leading museum of design and visual communication. The Toni-Areal location is inside a massive converted dairy factory, now home to the Zürich University of the Arts (ZHdK). The museum\'s four collections — decorative arts, design, graphics, and posters — are united under one roof with rotating exhibitions on architecture, industrial design, fashion, and photography.',
              details: [
                '📍 Pfingstweidstrasse 96, 8005 Zürich — inside the Toni-Areal campus',
                '🖼️ Exhibition running through April 2026 — check museum-gestaltung.ch for current shows',
                '💡 The building itself is a design statement — explore the campus architecture',
                '⏰ Open Tue–Sun 10am–5pm, Wed until 8pm'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Toni-Areal building is worth exploring beyond the museum — the ZHdK campus has public areas, a rooftop terrace, and often student exhibitions. It\'s a living design lab.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'FREITAG Flagship Store & Tower',
              description: 'No design trip to Zürich is complete without visiting the FREITAG Tower — a 26-metre structure made from 19 stacked shipping containers. Browse their iconic upcycled bags made from recycled truck tarpaulins, then climb to the rooftop viewing platform for panoramic views over the train tracks, the Alps, and Zürich West\'s ever-evolving skyline.',
              details: [
                '📍 Geroldstrasse 17, 8005 Zürich — right next to Hardbrücke station',
                '♻️ Each bag is one-of-a-kind, cut from used truck tarps — circular design at its best',
                '🔭 The rooftop terrace is free and offers incredible views',
                '🛠️ Check out the Repair Kiosk next door — they fix old Freitag bags'
              ]
            },
            {
              title: 'Im Viadukt — Shops Under the Railway Arches',
              description: 'A beautifully restored viaduct from 1894, its stone arches now house curated independent shops, design studios, and a covered Markthalle (market hall). Wander through eco-fashion boutiques, homeware stores, and artisan food shops — all with a focus on Swiss-made, sustainable, and beautifully designed products.',
              details: [
                '📍 Viaduktstrasse 21–99, 8005 Zürich',
                '🛍️ Look for Kitchener — lifestyle store with curated homeware and stationery',
                '🥬 Markthalle — covered market with organic produce, cheese, bread, and wine',
                '🧶 Several arches house sustainable fashion and handcraft studios'
              ]
            },
            {
              title: 'QWSTION Store — Limmatstrasse',
              description: 'This Zürich-born brand creates bags and everyday objects designed for circularity, made from Bananatex® — the world\'s first technical fabric made entirely from banana plants. Their flagship store is part shop, part design gallery, showcasing sustainable Swiss design at its most innovative.',
              details: [
                '📍 Limmatstrasse 202, 8005 Zürich',
                '🌿 Everything is plant-based and designed for end-of-life composting',
                '🎨 The store itself is beautifully minimal — clean lines, natural materials'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Restaurant Josef',
              description: 'A Kreis 5 institution with a distinctive wood-panelled interior and a sharing-plate concept that lets you build your own meal from seasonal, locally-sourced dishes. Clean design, honest food, and a creative neighbourhood atmosphere.',
              meta: '💰 $$ · 📍 Gasometerstrasse 24, 8005 Zürich'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'RRRevolve — Eco Fashion & Design Store',
              description: 'If you want to browse sustainable fashion before dinner, stop by RRRevolve near Helvetiaplatz. This carefully curated store stocks conscious brands like Veja, Armedangels, Colorful Standard, and QWSTION — plus eco-design homeware and accessories.',
              details: [
                '📍 Ankerstrasse 112, 8004 Zürich (Kreis 4)',
                '👗 Fair fashion for women and men — from sneakers to jackets',
                '🌱 Everything meets strict sustainability and fair-trade criteria'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Marktküche',
              description: 'A farm-to-table gem in Zürich West where the menu changes daily based on what\'s fresh and seasonal from local producers. The interior is warm minimalism — exposed brick, natural wood, soft lighting. Exactly the kind of place where design-conscious eating meets sustainable philosophy.',
              meta: '💰 $$–$$$ · 📍 Feldstrasse 98, 8004 Zürich · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'For an after-dinner drink, try Frau Gerolds Garten (seasonal rooftop bar near the Freitag Tower) — if weather allows, the urban garden atmosphere with views over the train tracks is magical. Check if it\'s open in mid-March.' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.3872, lng: 8.5198, label: 'MAME Coffee', num: 1, cat: 'food', desc: 'Award-winning Japanese-Swiss specialty coffee roaster' },
        { lat: 47.3906, lng: 8.5098, label: 'Museum für Gestaltung (Toni-Areal)', num: 2, cat: 'attraction', desc: 'Switzerland\'s leading design museum in a converted dairy factory' },
        { lat: 47.3856, lng: 8.5192, label: 'FREITAG Flagship Store', num: 3, cat: 'attraction', desc: 'Shipping container tower with upcycled bags and rooftop views' },
        { lat: 47.3867, lng: 8.5234, label: 'Im Viadukt', num: 4, cat: 'attraction', desc: 'Railway arches with design shops, eco-boutiques, and Markthalle' },
        { lat: 47.3835, lng: 8.5281, label: 'QWSTION Store', num: 5, cat: 'attraction', desc: 'Plant-based bags and sustainable Swiss design goods' },
        { lat: 47.3875, lng: 8.5180, label: 'Restaurant Josef', num: 6, cat: 'food', desc: 'Sharing plates from seasonal, local ingredients in Kreis 5' },
        { lat: 47.3774, lng: 8.5252, label: 'RRRevolve', num: 7, cat: 'attraction', desc: 'Curated eco-fashion and sustainable design store' },
        { lat: 47.3816, lng: 8.5230, label: 'Marktküche', num: 8, cat: 'food', desc: 'Daily-changing farm-to-table menu with minimalist interior' }
      ]
    },
    {
      num: 2,
      date: '2026-03-15',
      neighborhoods: 'Old Town · Niederdorf · Seefeld · Lake Zürich',
      title: 'Art, Old Town & Lakeside — Kunsthaus, Hidden Cafés & A Slow Farewell',
      description: "Day two takes you from the world-class Kunsthaus art museum through Zürich\'s charming Old Town, with stops at hidden design gems, an iconic interior store in Seefeld, and a peaceful lakeside walk. End your trip the way a slow-life believer should — with a beautiful coffee and a view of the Alps across the water.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kunsthaus Zürich',
              description: 'One of Switzerland\'s most important art museums, recently expanded with David Chipperfield\'s stunning minimalist extension. The collection spans from medieval to contemporary — Monet, Picasso, Giacometti, and major Swiss artists. The Chipperfield wing itself is a masterclass in restrained modern architecture — clean concrete, natural light, and perfectly proportioned galleries.',
              details: [
                '📍 Heimplatz 1, 8001 Zürich',
                '🏛️ The Chipperfield extension (2021) is a must-see for architecture lovers',
                '🖼️ "The Histories" exhibition running through Aug 2026',
                '⏰ Open Tue/Fri–Sun 10am–6pm, Wed–Thu 10am–8pm · Closed Mondays'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee',
              name: 'Café Kunst — Kunsthaus Café',
              description: 'Have a morning coffee in the Kunsthaus café before or after your visit. The space reflects the museum\'s design ethos — minimal, light-filled, and elegant. Perfect for a slow start before diving into the galleries.',
              meta: '💰 $ · 📍 Inside Kunsthaus Zürich'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Old Town Wander — Niederdorf & Augustinergasse',
              description: 'Stroll through Zürich\'s atmospheric Old Town. Niederdorf is a tangle of medieval lanes with independent bookshops, galleries, and hidden courtyards. Augustinergasse is one of the most photogenic streets in Switzerland — pastel guild houses with ornate bay windows and painted facades.',
              details: [
                '📍 Start at Heimplatz and walk downhill toward the Limmat river',
                '📸 Augustinergasse — the bay-windowed street is pure architectural beauty',
                '🛍️ Look for small galleries and design bookshops in the alleys',
                '⛪ Grossmünster — the iconic twin-tower Romanesque church'
              ]
            },
            {
              title: 'FROHSINN — Interior Design Store in Seefeld',
              description: 'Founded by renowned interior architect Claudia Silberschmidt, FROHSINN is a beautifully curated lifestyle and interior design store in the elegant Seefeld district. Think handcrafted ceramics, designer candles, minimalist homeware, and objects that blur the line between art and function.',
              details: [
                '📍 Seefeldstrasse 102, 8008 Zürich — in the Seefeld quarter',
                '🕯️ Curated selection of designer candles, ceramics, and matchstick holders',
                '🏠 Interior design consultations available — the founder is a practicing architect'
              ]
            },
            {
              title: 'Seefeld Quarter — Specialty Coffee & Design Walk',
              description: 'The Seefeld district is Zürich\'s version of a design-conscious residential neighbourhood — leafy streets, independent boutiques, and some of the city\'s best specialty coffee. MAME has a second location here (MAME Seefeld), and the area rewards slow, aimless wandering.',
              details: [
                '☕ MAME Seefeld — their second outpost, equally beautiful',
                '🛍️ Browse independent boutiques along Seefeldstrasse',
                '🌳 Quiet, residential, very "slow life" energy'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'HILTL',
              description: 'The world\'s oldest vegetarian restaurant (est. 1898), HILTL is a Zürich institution. The design-forward interior was renovated in a clean, modern style, and their extensive buffet offers global plant-based cuisine — Indian curries, Mediterranean mezze, Asian noodles, and Swiss specialties. Perfect for eco-minded food lovers.',
              meta: '💰 $$ · 📍 Sihlstrasse 28, 8001 Zürich (near Paradeplatz)'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lake Zürich Promenade — Sunset Walk',
              description: 'End your trip with a peaceful walk along the Lake Zürich promenade. In mid-March, the light is soft and the Alps begin to emerge from winter haze across the water. Walk from Bürkliplatz along the eastern shore toward the Zürichhorn — benches, swans, and the quiet beauty of Swiss lakeside life.',
              details: [
                '📍 Start at Bürkliplatz, walk east along the Utoquai promenade',
                '🏔️ On clear days, you can see the snow-capped Alps across the lake',
                '🦢 The swans on the lake are iconic Zürich',
                '🌅 Sunset around 6:30pm in mid-March — beautiful golden light'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Maison Blunt',
              description: 'A hidden gem in the Old Town — Moroccan-Mediterranean cuisine served in a gorgeously designed space with mosaic tiles, warm textures, and candlelight. The tagines are excellent, the atmosphere is intimate, and the interior is the kind of maximalist-meets-minimalist beauty that a design lover will appreciate.',
              meta: '💰 $$–$$$ · 📍 Pfingstweidstrasse 2, 8005 Zürich · Book ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'If you want a final specialty coffee moment, Commercial – The Project on Bahnhofstrasse serves several local roasters in a clean, Japanese-omakase-inspired setting. A beautiful last stop before heading home.' }
          ]
        }
      ],
      mapPins: [
        { lat: 47.3703, lng: 8.5481, label: 'Kunsthaus Zürich', num: 1, cat: 'attraction', desc: 'World-class art museum with David Chipperfield\'s minimalist extension' },
        { lat: 47.3714, lng: 8.5418, label: 'Old Town (Niederdorf)', num: 2, cat: 'attraction', desc: 'Medieval lanes with bookshops, galleries, and hidden courtyards' },
        { lat: 47.3725, lng: 8.5397, label: 'Augustinergasse', num: 3, cat: 'attraction', desc: 'Zürich\'s most photogenic street — pastel guild houses with bay windows' },
        { lat: 47.3555, lng: 8.5540, label: 'FROHSINN', num: 4, cat: 'attraction', desc: 'Curated interior design store by architect Claudia Silberschmidt' },
        { lat: 47.3580, lng: 8.5520, label: 'MAME Seefeld', num: 5, cat: 'food', desc: 'Second outpost of Zürich\'s best specialty coffee roaster' },
        { lat: 47.3727, lng: 8.5315, label: 'HILTL', num: 6, cat: 'food', desc: 'World\'s oldest vegetarian restaurant — design-forward interior' },
        { lat: 47.3667, lng: 8.5450, label: 'Lake Zürich Promenade', num: 7, cat: 'attraction', desc: 'Peaceful lakeside walk with Alpine views and swans' },
        { lat: 47.3733, lng: 8.5380, label: 'Maison Blunt', num: 8, cat: 'food', desc: 'Moroccan-Mediterranean gem with beautiful mosaic interior' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: 'CHF 80–150/night', midrange: 'CHF 150–300/night', luxury: 'CHF 300–600/night' },
    { category: 'Meals (per couple)', budget: 'CHF 50–80/day', midrange: 'CHF 80–150/day', luxury: 'CHF 150–300/day' },
    { category: 'Transport (ZVV pass)', budget: 'CHF 9–18/day', midrange: 'CHF 9–18/day', luxury: 'CHF 30–50/day (taxi)' },
    { category: 'Museums & Activities', budget: 'CHF 0–30/day', midrange: 'CHF 30–60/day', luxury: 'CHF 60–100/day' },
    { category: '2-Day Total (couple)', budget: 'CHF 300–550', midrange: 'CHF 550–1,050', luxury: 'CHF 1,100–2,100' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Zürich Airport (ZRH) is 10km from the city centre', 'Direct train from airport to Zürich HB (main station) takes 12 minutes', 'A taxi costs about CHF 50–70, but the train is faster and cheaper'] },
    { title: '🏨 Where to Stay', items: ['25hours Hotel Langstrasse — design hotel in the creative Kreis 4 district', 'Hotel Marktgasse — minimalist boutique hotel in the Old Town', 'Greulich Design & Lifestyle Hotel — architect-designed in Kreis 4', 'Placid Hotel — modern and minimal near Zürich West'] },
    { title: '🌡️ Weather', items: ['Mid-March averages 3–11°C (37–52°F) — dress in warm layers', 'Mix of sunny and overcast days, occasional rain', 'Snow is rare but possible in early March', 'Spring bulbs start appearing in parks and along the lake'] },
    { title: '💡 Design Lover Tips', items: ['Museum für Gestaltung Ausstellungsstrasse is closed until April 17, 2026 — visit the Toni-Areal location instead', 'Pavillon Le Corbusier (also run by Museum für Gestaltung) is seasonal — typically closed in March', 'Zürich has a strong typography heritage — look for Swiss Style posters in bookshops and the museum store', 'Many shops close on Sundays — Saturday is your best shopping day (March 14 is a Saturday!)'] },
    { title: '📱 Connectivity', items: ['Buy an eSIM or prepaid SIM at the airport (Swisscom or Sunrise)', 'Free WiFi available at most cafés and hotels', 'Google Maps works well for tram/bus navigation', 'Download the ZVV app for real-time public transport info'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
