const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771626938544_x95f7v",
  email: "psyduckler@gmail.com",
  destination: "Zermatt, Switzerland",
  start_date: "2026-12-27",
  end_date: "2026-12-31",
  group_size: "1",
  travel_style: "Adventure, Nightlife",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-20T22:35:38.544Z",
  status: "pending"
};

const itineraryData = {
  destination: "Zermatt, Switzerland",
  countryEmoji: "🇨🇭",
  title: "Zermatt in 4 Nights: Matterhorn, Powder & Après-Ski",
  subtitle: "Skiing → Mountain Huts → Fondue → Après-Ski Bars → New Year's Eve",
  description: "A solo adventure trip to one of the Alps' most iconic villages — car-free Zermatt sits at the foot of the Matterhorn with 360km of pistes, Europe's highest cable car, and an après-ski scene that runs until the early hours. Late December means fresh powder, holiday magic, and ringing in the New Year with fireworks against the Matterhorn silhouette.",
  duration: "4 nights / 5 days",
  dates: "Dec 27 – 31, 2026",
  budget: "Flexible",
  pace: "Active — ski hard, party harder",
  bestFor: "Solo adventurers, ski lovers & nightlife seekers",
  highlights: [
    "Matterhorn Glacier Paradise — Europe's highest cable car at 3,883m",
    "360km of ski runs across Zermatt-Cervinia",
    "Iglu-Dorf — overnight in an igloo village on the mountain",
    "Chez Vrony — legendary mountain hut lunch with Matterhorn views",
    "Hennu Stall — the wildest après-ski bar on the slopes",
    "Papperla Pub — Zermatt's most notorious nightlife spot",
    "Gornergrat Railway — panoramic train to 3,100m viewpoint",
    "New Year's Eve fireworks over the Matterhorn",
    "Swiss fondue in a cozy chalet restaurant",
    "Car-free village charm — electric taxis and horse-drawn carriages"
  ],
  essentials: [
    { title: "🚂 Getting There", text: "Zermatt is car-free. Take the train from Zürich (3.5h), Geneva (3.5h), or fly into Zürich/Geneva and train in. The last stretch on the Matterhorn Gotthard Bahn from Visp is scenic and stunning. No cars allowed in town — you'll walk, take electric shuttles, or ride horse-drawn carriages." },
    { title: "⛷️ Ski Pass", text: "Get the Zermatt-Cervinia International ski pass for full access to 360km of runs across Switzerland and Italy. Multi-day passes are cheaper per day — a 4-day pass is ~CHF 320. Buy online at matterhornparadise.ch for discounts. The pass covers all lifts including Matterhorn Glacier Paradise." },
    { title: "💵 Budget Reality", text: "Zermatt is expensive. Mountain lunches: CHF 25-45. Dinner in town: CHF 50-90. Beer at après-ski: CHF 8-12. Ski rental: CHF 50-80/day. Budget CHF 200-300/day beyond accommodation and ski pass. Tip: eat a big mountain lunch and go lighter for dinner." },
    { title: "🏔️ Weather & Conditions", text: "Late December averages -5 to -10°C in town, colder on the mountain. Snow is usually excellent — Zermatt's glacier means guaranteed snow. Pack serious layers: base layer, mid layer, ski jacket, goggles, sunscreen (the reflection at altitude burns fast). Days are short — sunrise ~8:15, sunset ~4:45." },
    { title: "🏨 Where to Stay", text: "Book early for holiday week — Zermatt fills up. Bahnhofstrasse area puts you near the train station and main nightlife. For quieter vibes, stay near the church in old Zermatt. Hostels and budget spots: Zermatt Youth Hostel or Hotel Bahnhof. Mid-range: Hotel Pollux or Backstage Hotel (boutique, right in town)." },
    { title: "📱 Useful Apps", text: "Zermatt App (lift status, piste map, GPS tracking), SBB Mobile (Swiss trains), Skiguide Zermatt (run recommendations), Meteo Swiss (accurate mountain weather). Download offline maps — cell signal can be spotty on the mountain." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival, Village Vibes & First Night Out",
      neighborhoods: "Zermatt Village · Bahnhofstrasse · Old Town",
      date: "Dec 27",
      mapPins: [
        { lat: 46.0207, lng: 7.7491, label: "Zermatt Bahnhof", num: 1, cat: "activity", desc: "Train station — your arrival point" },
        { lat: 46.0197, lng: 7.7486, label: "Bahnhofstrasse", num: 2, cat: "food", desc: "Main street — shops, restaurants, bars" },
        { lat: 46.0192, lng: 7.7478, label: "Old Town Zermatt", num: 3, cat: "activity", desc: "Traditional wooden chalets and the old church" },
        { lat: 46.0185, lng: 7.7477, label: "Kirchbrücke viewpoint", num: 4, cat: "activity", desc: "Classic Matterhorn photo spot from the bridge" },
        { lat: 46.0201, lng: 7.7489, label: "Papperla Pub", num: 5, cat: "food", desc: "Zermatt's legendary party bar" },
        { lat: 46.0195, lng: 7.7485, label: "Whymper Stube", num: 6, cat: "food", desc: "Best fondue in Zermatt" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Explore the Village", description: "Step off the train into car-free Zermatt — immediately magical. The air is crisp, electric taxis hum by, and the Matterhorn looms at the end of every street. Walk Bahnhofstrasse (main street) to get your bearings — it's lined with luxury watch shops, outdoor gear stores, and restaurants. The village is small enough to walk end-to-end in 15 minutes.", details: ["📍 If you need a ski pass, grab it at the ticket office near the Gornergrat railway station", "💡 The Matterhorn is often hidden by afternoon clouds. Best views are early morning — don't panic if you can't see it on arrival."] },
            { title: "Old Town & Kirchbrücke", description: "Wander into old Zermatt — dark wooden chalets on stone foundations, some hundreds of years old. Cross the Kirchbrücke (church bridge) over the Vispa river for the classic postcard Matterhorn view. The old church cemetery has graves of mountaineers who died on the Matterhorn — sobering and fascinating.", details: ["💡 The Matterhorn Museum (Zermatlantis) is underground near the church — covers the first ascent and the tragedy. Worth 45 minutes if you're into mountain history."] }
          ],
          meals: [
            { type: "☕ Arrival Snack", name: "Fuchs Bakery", description: "Right near the station — grab a fresh pretzel, Nussgipfel (nut croissant), or slice of Engadiner Nusstorte (walnut tart) to fuel your first exploration. The hot chocolate is thick and proper Swiss.", meta: "CHF 6-12 · Bahnhofstrasse · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Zermatt is at 1,620m elevation. If you're coming from sea level, take it easy on day one — hydrate, skip intense exercise, and don't overdo the alcohol. You'll feel the altitude more than you expect." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Fondue Dinner", description: "Your first night demands fondue. Whymper Stube (named after the first Matterhorn summiteer) does the definitive Zermatt version — moitié-moitié (half Gruyère, half Vacherin) in a cozy wood-paneled room. Pair with a crisp Fendant white wine. This is Switzerland at its most essential.", details: ["📍 On Bahnhofstrasse · Reservations recommended during holiday week", "💡 Fondue etiquette: if your bread falls off the fork into the pot, you buy the next round of drinks."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Whymper Stube", description: "The most atmospheric fondue spot in Zermatt. Wood-paneled walls covered in mountaineering memorabilia, the cheese is perfectly made, and the Fendant (local Valais white wine) is the ideal pairing. It's touristy but genuinely excellent. Come hungry — fondue is heavier than you think.", meta: "CHF 35-55pp · Bahnhofstrasse · Reserve ahead for Dec 27" }
          ],
          tips: [{ type: "reddit", text: "Whymper Stube fondue is the real deal. Don't bother with the cheaper tourist traps. Also: eat the boiled potatoes and cornichons between fondue dips — it helps your stomach handle the cheese. Trust me.", cite: "r/switzerland" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Papperla Pub", description: "Zermatt's most legendary nightlife spot. It starts civilized with drinks and dancing on tables by 10pm — by midnight it's absolute chaos in the best way. Live music, international crowd, people in ski boots on the bar. Solo travelers thrive here because everyone's in party mode. This is where you'll meet people.", details: ["📍 Steinmattstrasse · Gets going around 10pm, peaks at midnight", "💡 It's a small space that gets HOT. Dress in layers you can shed. Also — drinks are expensive (CHF 12+ for a beer). Pre-game a little at dinner."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Papperla Pub is chaos incarnate and I mean that in the best way. Go solo, you'll leave with a crew. Just pace yourself — Zermatt altitude + alcohol hits different.", cite: "r/skiing" }]
        }
      ]
    },
    {
      num: 2,
      title: "Matterhorn Glacier Paradise & Après-Ski",
      neighborhoods: "Klein Matterhorn · Trockener Steg · Furi · Village",
      date: "Dec 28",
      mapPins: [
        { lat: 45.9375, lng: 7.7283, label: "Matterhorn Glacier Paradise", num: 1, cat: "activity", desc: "3,883m — Europe's highest cable car station" },
        { lat: 45.9809, lng: 7.7467, label: "Trockener Steg", num: 2, cat: "activity", desc: "Mid-station — access to glacier skiing" },
        { lat: 46.0038, lng: 7.7543, label: "Furi", num: 3, cat: "food", desc: "Mid-mountain station and restaurant stop" },
        { lat: 46.0041, lng: 7.7540, label: "Hennu Stall", num: 4, cat: "food", desc: "The wildest après-ski bar on the mountain" },
        { lat: 45.9700, lng: 7.7400, label: "Italian Border", num: 5, cat: "activity", desc: "Ski into Cervinia, Italy for lunch" },
        { lat: 46.0196, lng: 7.7490, label: "Elsie Bar", num: 6, cat: "food", desc: "Zermatt institution — oysters and champagne" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Matterhorn Glacier Paradise", description: "Take the first cable car up to 3,883m — the highest cable car station in Europe. The viewing platform offers a jaw-dropping 360° panorama of 38 four-thousanders including Monte Rosa, the Matterhorn's east face, and on clear days, all the way to the Jura and Black Forest. There's an ice palace carved into the glacier with ice sculptures. It's surreal — you're standing on a glacier in December.", details: ["📍 First cable car around 8:30am from Zermatt → Furi → Trockener Steg → Klein Matterhorn", "💡 Bring sunglasses and sunscreen even in December — the UV at this altitude is brutal. The viewing platform is outdoors and can be -20°C with wind chill."] },
            { title: "Glacier Skiing", description: "The glacier runs from Klein Matterhorn are wide, groomed, and stunning. You're skiing at 3,800m with views that don't exist anywhere else. The runs down to Trockener Steg are long and satisfying — mostly red (intermediate) with some blue (easy) options. Snow is guaranteed on the glacier year-round.", details: ["💡 The glacier runs are above the treeline — visibility can change fast. If clouds roll in, head down to lower areas where you have reference points."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hotel grab-and-go", description: "Eat at your hotel or grab pastries from Fuchs Bakery before the first lift. You want to be on that first cable car — the mountain is emptiest before 9:30am and the light on the Matterhorn at sunrise is unforgettable.", meta: "CHF 8-15 · Eat quick, ski early" }
          ],
          tips: [{ type: "tip", text: "The Klein Matterhorn cable car can have long lines during holiday week. Be at the valley station by 8:15am. The first cabin up is worth the early wake-up — empty slopes and the best light of the day." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ski to Italy (Optional)", description: "From Trockener Steg, you can ski over the border into Cervinia, Italy. The Italian side has wider, sunnier runs and significantly cheaper food and drinks. Grab a pizza and espresso at one of the Italian mountain huts — it's a different world from the Swiss side. Just watch the time — the last lift back to Switzerland closes around 4pm.", details: ["📍 Your Zermatt-Cervinia pass covers the Italian side", "💡 Italian mountain food is half the price of Swiss. A full pasta lunch with wine can be €20 vs CHF 45 on the Swiss side."] },
            { title: "Afternoon Laps", description: "Head back to the Swiss side for afternoon runs. The Rothorn and Sunnegga areas get the best afternoon sun. The runs through the larch forests above Furi are gorgeous — dappled light through snow-covered trees. Start heading toward Furi around 3:30pm for après-ski.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Chez Vrony (Findeln)", description: "The most famous mountain restaurant in Zermatt — perched above the hamlet of Findeln with an unobstructed Matterhorn view that will stop you mid-bite. The lamb shoulder and Valais wine are exceptional. Reservations essential during holiday week. Ski in, ski out — it's on the Sunnegga side.", meta: "CHF 40-65pp · Above Findeln · Reserve on their website — this fills up days in advance" }
          ],
          tips: [{ type: "reddit", text: "Chez Vrony is not overhyped. The Matterhorn view from the terrace is insane. Book ahead or show up right at 11:30 when they open. The rösti with egg is incredible if you want something lighter than the lamb.", cite: "r/zermatt" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Hennu Stall Après-Ski", description: "THE après-ski bar in Zermatt. Located on the slopes above Furi, you ski right up to it around 3:30-4pm and the party is already raging. DJs, dancing in ski boots, glühwein flowing, everyone's sunburned and happy. It's the best après-ski in the Alps — frenetic, joyful energy. You'll make friends instantly.", details: ["📍 On the piste between Furi and Zermatt — you can't miss it (you'll hear it)", "💡 Get there by 3:30pm for the best vibes. By 4:30pm people start skiing the last run down to town. The descent after Hennu Stall après-ski is... adventurous. Ski carefully."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Elsie Bar", description: "A Zermatt institution since 1961. Tiny, wood-paneled bar famous for oysters and champagne — an unexpected combination at 1,620m in the Alps. The oysters are flown in fresh, the champagne list is serious, and the atmosphere is old-school glamorous. It's the most Zermatt thing possible.", meta: "CHF 45-70pp · Near the church · Walk-in, but get there by 7pm for a seat" }
          ],
          tips: [{ type: "tip", text: "Zermatt's dining scene is split: mountain huts for lunch, village restaurants for dinner. Budget your big meal for lunch on the mountain — it's often better food, better views, and comparable prices." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Vernissage Club", description: "Zermatt's most stylish nightclub — part art gallery, part cinema, part club, all underground. The Heinz Julen-designed space is visually stunning with exposed rock walls and modern art. DJs spin house and electronic music. It draws a more sophisticated crowd than Papperla — dress smart-casual, not ski gear.", details: ["📍 Hofmattstrasse · Opens late (~11pm), gets going after midnight", "💡 Cover charge varies but usually CHF 10-20. Drinks are pricey (CHF 15+ cocktails). Worth one night for the atmosphere alone."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Gornergrat Railway & Rothorn Skiing",
      neighborhoods: "Gornergrat · Rothorn · Sunnegga · Village",
      date: "Dec 29",
      mapPins: [
        { lat: 45.9836, lng: 7.7853, label: "Gornergrat", num: 1, cat: "activity", desc: "3,100m — panoramic railway viewpoint" },
        { lat: 46.0083, lng: 7.7640, label: "Sunnegga", num: 2, cat: "activity", desc: "Sunny slopes and family-friendly runs" },
        { lat: 46.0130, lng: 7.7750, label: "Rothorn", num: 3, cat: "activity", desc: "3,103m — challenging runs and stunning views" },
        { lat: 45.9920, lng: 7.7750, label: "Findeln", num: 4, cat: "food", desc: "Charming hamlet with multiple mountain restaurants" },
        { lat: 46.0200, lng: 7.7488, label: "GramPi's Pub", num: 5, cat: "food", desc: "Cozy pub for evening drinks" },
        { lat: 46.0190, lng: 7.7480, label: "Restaurant Schäferstube", num: 6, cat: "food", desc: "Walliser Teller — the local cheese platter" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Gornergrat Railway", description: "Take the Gornergrat Bahn — a 33-minute cogwheel train ride from Zermatt village to 3,100m. It's one of the most scenic train rides in the world. The panorama from the top is staggering — Monte Rosa (Switzerland's highest peak), the Gorner Glacier, and an unobstructed Matterhorn view. In December, the early morning light turns everything gold and pink.", details: ["📍 Train departs from next to Zermatt Bahnhof · Included in most ski passes or ~CHF 50 return", "💡 Sit on the right side going up for the best Matterhorn views. The first train (~7am) catches sunrise — absolutely worth the early alarm."] },
            { title: "Ski the Gornergrat", description: "From the top, ski down through some of Zermatt's most spectacular terrain. The runs are long (1,500m+ vertical) and varied — from wide groomers to off-piste powder stashes in the trees. The Kelle run is a famous steep pitch. For something gentler, the runs through Riffelalp offer gorgeous scenery with manageable gradient.", details: ["💡 The Gornergrat side gets morning sun, so snow can get heavy by afternoon. Ski it in the morning and switch to Rothorn/Sunnegga for afternoon shade."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Café du Pont", description: "Local breakfast spot near the train station. Strong coffee, fresh bread with Swiss butter and jam, and Birchermüesli (the original — Zermatt is in the canton where it was invented). Fuel up properly for a big ski day.", meta: "CHF 12-18 · Near Bahnhof · Walk-in, opens early" }
          ],
          tips: [{ type: "reddit", text: "Sunrise Gornergrat is a bucket-list experience. The Matterhorn goes from blue to pink to gold in about 20 minutes. Bundle up — it's brutally cold at 3,100m before the sun hits. Totally worth it.", cite: "r/switzerland" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rothorn & Sunnegga Skiing", description: "Transfer to the Rothorn side via Sunnegga. The underground funicular from the village shoots you to Sunnegga in 3 minutes — fastest access to any ski area. The Rothorn sector has some of the most challenging skiing in Zermatt — steep blacks, mogul fields, and incredible off-piste. Sunnegga itself is sunnier and more mellow — great for cruising.", details: ["📍 Sunnegga funicular entrance is a 5-min walk from the village center", "💡 The Trifji area near Rothorn has excellent off-piste if you're comfortable in steep terrain. Ask ski patrol about conditions."] },
            { title: "Findeln Hamlet", description: "Ski down to Findeln — a tiny, car-free hamlet of dark wooden chalets that's home to several mountain restaurants. It's the most photogenic lunch stop in the Alps. Each restaurant has a sun terrace with Matterhorn views. It feels like stepping back 200 years.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Findlerhof", description: "An alternative to Chez Vrony in the same hamlet — equally stunning views, slightly less famous, which means easier reservations. The raclette is outstanding and the wine list focuses on Valais producers. Sit on the terrace and watch skiers carve past while you eat.", meta: "CHF 35-55pp · Findeln · Reserve recommended but easier than Chez Vrony" }
          ],
          tips: [{ type: "tip", text: "Findeln has 4-5 restaurants in a cluster. If your first choice is full, just walk to the next one. They're all good and they all have the view. Adler Hitta and Enzian are also excellent." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Village Stroll & Shopping", description: "After skiing, shower and walk through the village as it transforms for the evening. Zermatt is magical after dark — the chalets glow with warm light, the Matterhorn disappears into stars, and the streets fill with people in that post-ski glow. Browse the shops on Bahnhofstrasse or sit in a hotel lobby bar with a Glühwein and people-watch.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Restaurant Schäferstube", description: "For an authentic Valais dinner experience. The Walliser Teller (local cheese and dried meat platter) is a revelation — paper-thin Viande des Grisons, local alpine cheeses, rye bread, and pickles. Raclette is also done perfectly here. Cozy, traditional, unpretentious.", meta: "CHF 35-55pp · Hotel Julen · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Schäferstube has its own sheep herd in the basement (seriously, you can visit them). The Walliser Teller is the most underrated dish in Zermatt — get it as an appetizer even if you're getting raclette.", cite: "r/zermatt" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "GramPi's Pub & Bar Crawl", description: "Start at GramPi's — a cozy, friendly pub that's less chaotic than Papperla but still lively. Good beer selection, reasonable prices by Zermatt standards, and a mixed crowd of locals and visitors. From there, bar-hop down Bahnhofstrasse. The Brown Cow is a chill whiskey bar, Schneewittchen is cocktail-forward, and if you end up at Papperla again at midnight — you're doing Zermatt right.", details: ["💡 Most bars close around 1:30-2am. Vernissage is the only real late-night option (until 3:30am). Pace accordingly."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Last Ski Day & New Year's Eve",
      neighborhoods: "Schwarzsee · Village · Bahnhofstrasse",
      date: "Dec 30",
      mapPins: [
        { lat: 45.9922, lng: 7.7275, label: "Schwarzsee", num: 1, cat: "activity", desc: "Closest ski area to the Matterhorn" },
        { lat: 45.9850, lng: 7.7300, label: "Hirli", num: 2, cat: "activity", desc: "Panoramic skiing with Matterhorn backdrop" },
        { lat: 46.0190, lng: 7.7483, label: "Kirchplatz", num: 3, cat: "activity", desc: "Main square for NYE celebrations" },
        { lat: 46.0195, lng: 7.7487, label: "Bahnhofstrasse", num: 4, cat: "food", desc: "New Year's Eve buzz" },
        { lat: 46.0188, lng: 7.7475, label: "The Omnia", num: 5, cat: "food", desc: "Dramatic hotel bar with panoramic views" },
        { lat: 46.0200, lng: 7.7492, label: "Hotel Post Bar", num: 6, cat: "food", desc: "Lively NYE party" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Schwarzsee Skiing", description: "Save the Schwarzsee area for your last ski day — it's the closest you can get to the Matterhorn on skis. The cable car to Schwarzsee passes directly beneath the Matterhorn's north face, which towers above you at an impossible angle. The skiing here is mostly intermediate with some genuinely challenging off-piste options. The connection to Furi makes it easy to ski laps.", details: ["📍 Take the Zermatt → Furi → Schwarzsee lift sequence", "💡 The small chapel at Schwarzsee (Kapelle Maria zum Schnee) at 2,583m is one of the most photographed spots in the Alps. Worth a 5-minute stop."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bäckerei Fuchs (again)", description: "Quick fuel-up. Grab a Gipfeli (Swiss croissant) and a double espresso. Today is about maximizing ski time in the morning and saving energy for tonight.", meta: "CHF 8-12 · Quick and efficient" }
          ],
          tips: [{ type: "tip", text: "Last day of skiing — take a moment at the top of each lift to look around. The Matterhorn, Monte Rosa, the Gorner Glacier, the Weisshorn. This is one of the most dramatic mountain environments on Earth. Soak it in." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Final Runs & Mountain Goodbye", description: "Do your favorite runs one more time. The long cruise from Rothorn all the way to the village (if conditions allow the Triftji descent) is about 1,500m of vertical — one of the longest runs in the Alps. Finish by 3pm to rest before New Year's Eve.", details: [] },
            { title: "Rest & Prep for NYE", description: "Take a proper break. Shower, nap, charge up. New Year's Eve in Zermatt goes very late and starts with dinner around 7-8pm. Some hotels have spa access — a hot tub or sauna after 4 days of skiing is heaven.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Restaurant Stafelalp", description: "Mountain restaurant on the Schwarzsee side with a perfect sun terrace. The Älplermagronen (Swiss alpine mac and cheese with potatoes, cream, and applesauce on the side) is the ultimate ski fuel. Simple, hearty, exactly right.", meta: "CHF 25-40pp · On the piste above Furi · Walk-in usually fine for lunch" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "New Year's Eve Dinner", description: "Most Zermatt restaurants do special NYE menus — book well in advance. The village buzzes with anticipation. Bahnhofstrasse fills with people strolling between restaurants and bars. Get dinner early (7-8pm) so you're done and mobile by 11pm for the countdown.", details: ["💡 Many restaurants require NYE prix fixe bookings weeks in advance. If you haven't booked: Elsie Bar, GramPi's, and some hotel restaurants may still have space for à la carte or bar seating."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "After Seven (The Omnia Hotel)", description: "For a special NYE dinner: dramatic cliff-side hotel with a restaurant that serves creative Swiss cuisine with Matterhorn views through floor-to-ceiling windows. The tasting menu is pricey but memorable. Even if you skip dinner, visit the bar — the view at night is extraordinary.", meta: "CHF 100-150pp for NYE menu · Reserve weeks ahead · Dress: smart casual" }
          ],
          tips: [{ type: "reddit", text: "The Omnia bar alone is worth visiting — built into the cliff with a glass wall overlooking the Matterhorn. Get there before midnight for a drink and watch the fireworks from the terrace. One of the most dramatic NYE settings on Earth.", cite: "r/travel" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "New Year's Eve Countdown & Fireworks", description: "At midnight, Zermatt erupts. Fireworks launch from the village and the mountain — the explosions echo off the valley walls and the Matterhorn is silhouetted against the pyrotechnics. People flood Kirchplatz and Bahnhofstrasse with champagne and cheers. The entire village is the party. Solo or not, you'll be hugging strangers. This is one of the most spectacular NYE celebrations in Europe.", details: ["📍 Best spots: Kirchplatz (main square), the bridge near the church, or The Omnia terrace (if you can get in)", "💡 Bring your own champagne/prosecco to the streets — everyone does. Buy a bottle earlier in the day from a shop."] },
            { title: "NYE After-Parties", description: "After the fireworks, the party moves indoors. Papperla Pub goes absolutely nuclear — expect the most chaotic night of the year. Vernissage Club runs until dawn. Hotel Post has a lively party. Or just drift between bars — the whole village is alive until 4am. This is the night to push the limits.", details: ["💡 Pace yourself with water. Altitude + champagne + 4 days of skiing = rough morning if you're not careful."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "NYE in Zermatt is genuinely world-class. The fireworks with the Matterhorn as a backdrop is surreal. Papperla on NYE is the most chaotic bar experience I've ever had — in the absolute best way. Solo travelers: this is YOUR night. Everyone talks to everyone.", cite: "r/skiing" }]
        }
      ]
    },
    {
      num: 5,
      title: "Recovery Brunch & Departure",
      neighborhoods: "Zermatt Village",
      date: "Dec 31",
      mapPins: [
        { lat: 46.0197, lng: 7.7486, label: "Bahnhofstrasse", num: 1, cat: "food", desc: "Late morning brunch" },
        { lat: 46.0207, lng: 7.7491, label: "Zermatt Bahnhof", num: 2, cat: "activity", desc: "Train departure" },
        { lat: 46.0192, lng: 7.7478, label: "Old Town", num: 3, cat: "activity", desc: "One last walk" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Late Wake-Up & Village Farewell", description: "Sleep in. You've earned it. When you finally surface, take one last walk through Zermatt. The village on New Year's Day morning is quiet and peaceful — a stark contrast to last night. The Matterhorn doesn't care about your hangover; it's sitting there as perfect as ever. Breathe the mountain air one final time.", details: [] },
            { title: "Departure", description: "The train from Zermatt to Visp runs frequently — from there you can connect to Zürich, Geneva, or anywhere in Switzerland. The ride down the valley is beautiful even if you're half-asleep. Say goodbye to the Matterhorn from the train window.", details: ["📍 Trains to Visp depart roughly every 30 min · Connect to intercity trains from there", "💡 Buy train tickets on the SBB app. Supersaver tickets (booked in advance) can save 30-50% vs walk-up prices."] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Café du Pont or Hotel Breakfast", description: "Wherever is closest and open. Coffee, bread, cheese — keep it simple. A proper Swiss breakfast is the gentlest way to recover. If your hotel does breakfast, use it. If not, Café du Pont is reliable and opens early.", meta: "CHF 15-22 · Gentle recovery food" }
          ],
          tips: [{ type: "tip", text: "If you're not in a rush to leave, take one more Gornergrat train ride on New Year's Day morning. The mountain will be quiet, the light will be beautiful, and you'll have the best possible farewell to Zermatt." }]
        }
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
