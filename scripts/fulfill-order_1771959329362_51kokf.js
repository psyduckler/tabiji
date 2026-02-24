const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771959329362_51kokf',
  email: 'james.cadena@gmail.com',
  destination: 'Amsterdam, Netherlands',
  start_date: '2026-03-27',
  end_date: '2026-03-29',
  group_size: '2',
  style: 'Cultural, Foodie, Nightlife',
};

const itineraryData = {
  destination: 'Amsterdam, Netherlands',
  countryEmoji: '🇳🇱',
  title: 'Amsterdam in 3 Days: Canals, Culture & Late Nights',
  subtitle: 'A perfectly curated long weekend for two — world-class museums by day, market feasts at noon, and the Netherlands\' greatest nightlife after dark',
  description: 'Amsterdam rewards those who wander. In three days you\'ll cover the city\'s greatest cultural icons — the Rijksmuseum\'s Dutch Masters, Van Gogh\'s electric canvases, the heartbreaking quiet of Anne Frank\'s hiding place — while eating your way through De Pijp\'s market stalls, dining in elegant Jordaan canal houses, and staying out until 4am at legendary venues like Paradiso. The city in late March is stirring from winter: canal-side terraces are cracking open their first heaters, the crowds at peak summer are still weeks away, and the light over the Prinsengracht has that cool silver quality that drove 17th-century painters into their studios. Two people who love culture, food, and nightlife will find Amsterdam close to perfect.',
  duration: '3 days',
  dates: 'Mar 27 – Mar 29, 2026',
  budget: '€150 – €250 per person/day (mid-range to splurge)',
  pace: 'Active',
  bestFor: 'Couples, Culture lovers, Foodies, Night owls',

  highlights: [
    'The Rijksmuseum\'s Night Watch — Rembrandt\'s masterpiece in a cathedral-like hall',
    'Van Gogh Museum: 200+ paintings tracing his life from dark Dutch fields to Arles sun',
    'Anne Frank House — the most moving two hours in Amsterdam, book weeks in advance',
    'Albert Cuyp Market in De Pijp — stroopwafels, raw herring, Dutch cheese, Indonesian snacks',
    'Brouwerij \'t IJ — craft beer in a working windmill; the quintessential Amsterdam afternoon',
    'Late night at Paradiso — a consecrated 19th-century church turned pop and electronic temple',
    'Jordaan canal strolls past 17th-century merchant houses hung with ivy and fairy lights',
    'Indonesian rijsttafel — 20+ dishes descended from Dutch colonial trade, a true Amsterdam ritual',
  ],

  essentials: [
    {
      title: '🛬 Getting There',
      text: 'Amsterdam Schiphol (AMS) is one of Europe\'s best-connected airports. From the airport, the direct train (Intercity Direct) reaches Amsterdam Centraal in just 17 minutes — buy your ticket at the NS yellow machines. A taxi or Uber is 30–45 min and costs €40–€60. If you\'re arriving by Eurostar or Thalys from London, Brussels, or Paris, you arrive directly at Centraal Station in the heart of the city.'
    },
    {
      title: '🚲 Getting Around',
      text: 'Amsterdam is a bike city. Renting bicycles (€12–€20/day at MacBike or Starbikes) is the single best decision you\'ll make — it\'s how locals move and you\'ll cover 3x the ground with 10x the fun. Trams are excellent for longer hops (OV-chipkaart or GVB day passes from €8). Walking works for the canal belt — the Jordaan to De Pijp is 20 minutes on foot. Avoid the central canal ring by car at all costs.'
    },
    {
      title: '🗓️ Book Before You Arrive',
      text: 'Three bookings are mandatory before you land: (1) Anne Frank House tickets — these sell out 4–8 weeks ahead, only sold online at annefrank.org; (2) Rijksmuseum — buy timed-entry tickets online to skip the queues; (3) Van Gogh Museum — timed entry required, book at vangoghmuseum.nl. All three have no same-day walk-up option in practice. For nightlife, check Paradiso\'s event calendar (paradiso.nl) — big Saturday night acts sell out fast.'
    },
    {
      title: '🌦️ Late March Weather',
      text: 'Amsterdam in late March is cool and variable — expect 7–14°C (45–57°F). The sun appears, disappears, and reappears without warning. Rain is possible any day. Pack a waterproof layer, comfortable walking shoes (cobblestones are hard on thin soles), and mid-weight layers. The canal terraces will have outdoor heating but you\'ll want a coat. By day\'s end, evenings drop to 5–7°C — bring a proper jacket if you\'re club-hopping.'
    },
    {
      title: '🏨 Where to Stay',
      text: 'The best locations for this trip: Jordaan (romantic, walkable, canal-facing) or De Pijp (young, foodie, close to Albert Cuyp Market). Avoid the immediate Red Light District area if you want quiet — it\'s great to visit but loud at night. Recommended: Hotel V Nesplein (boutique, central, excellent design), The Dylan Amsterdam (luxury canal-house hotel in the Jordaan), or Hotel Dwars (intimate, Jordaan, perfect location). Book early — March weekends fill quickly.'
    },
    {
      title: '💶 Money & Costs',
      text: 'The Netherlands is cashless — nearly everywhere accepts contactless card payment (Mastercard/Visa). Amsterdam is not cheap: expect €15–22 for a main at a casual restaurant, €25–40 at a nicer dinner spot, €8–10 for a craft beer, €15–20 club entry. Museum tickets: Rijksmuseum €22.50, Van Gogh €22, Anne Frank €16. The biggest savings come from booking museum tickets online (no queue) and eating lunch at markets rather than tourist restaurants. Budget roughly €150–250/person/day all-in.'
    }
  ],

  days: [
    // ====================================================
    // DAY 1 — Jordaan + Rijksmuseum + First Night Out
    // ====================================================
    {
      num: 1,
      date: 'Friday, Mar 27',
      neighborhoods: 'Jordaan · Nine Streets · Museumplein · Leidseplein',
      title: 'Canals, Dutch Masters & First Night Out',
      description: 'Arrive, get oriented in the magical Jordaan neighborhood, visit the Rijksmuseum\'s crown jewels, and end with a serious dinner followed by drinks around Leidseplein — Amsterdam\'s most vibrant after-dark square.',
      timeBlocks: [
        {
          label: 'Morning / Arrival',
          activities: [
            {
              title: 'Arrive & Check In — Jordaan',
              description: 'Drop your bags and immediately step outside. The Jordaan is Amsterdam\'s most beautiful neighborhood: a 17th-century grid of narrow canals lined with gabled merchant houses, independent galleries, cheese shops, and brown cafés. Wander with no agenda — the Bloemgracht, Brouwersgracht, and Egelantiersgracht canals are some of the loveliest in the city. Get hopelessly lost. It\'s fine.',
              details: [
                '📍 Jordaan neighborhood — between Prinsengracht and Lijnbaansgracht',
                '💡 The Jordaan was working-class in the 17th century; now it\'s the most sought-after address in Amsterdam',
                '💡 Walk the Brouwersgracht canal — voted one of the most beautiful streets in the world',
                '🚲 Rent bikes right away from MacBike near Centraal — you\'ll use them all day'
              ]
            },
            {
              title: 'Nine Streets (De 9 Straatjes)',
              description: 'A grid of nine charming cross-streets between the Jordaan and the main canal ring, lined with independent boutiques, vintage shops, specialty food stores, and design studios. Browse at leisure — it\'s one of the best shopping strips in Europe, full of locals rather than tourists. Stop in any cheese shop for samples; the aged Gouda here bears no resemblance to what you\'ve had at home.',
              details: [
                '📍 De 9 Straatjes — Reestraat, Hartenstraat, Wolvenstraat etc. between Prinsengracht and Singel',
                '🧀 Must-stop: De Kaaskamer (Runstraat 7) — outstanding Dutch cheese selection, tasting plates available',
                '💡 Vintage shop: Laura Dols for Dutch vintage fashion (Wolvenstraat)',
                '🕐 Allow 60–90 minutes to properly wander'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Morning Coffee & Brunch',
              name: 'Café Winkel 43',
              description: 'A Jordaan institution, famous across Amsterdam for one thing: apple pie. The appeltaart here is warm, thick, served with a mountain of fresh cream and has a serious cult following among locals. Sit inside the brown café interior or grab a spot on the Noordermarkt terrace and watch Amsterdam wake up. Outstanding coffee too.',
              meta: '📍 Noordermarkt 43, Jordaan · ⏰ Opens 8am · 💰 €4-8 · 💡 The apple pie comes in a wedge the size of a paperback novel'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Friday morning in the Jordaan is pleasantly quiet — the tourists sleep in and the locals have already cycled to work. This is the best window to walk the smaller canals undisturbed. By afternoon it picks up considerably.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rijksmuseum 🎨',
              description: 'The greatest collection of Dutch Golden Age art on Earth. The Rijksmuseum\'s 2013 renovation turned it into one of the world\'s most beautiful museum buildings — and inside, Rembrandt\'s enormous Night Watch stops people cold in the Gallery of Honour. Budget 2–2.5 hours minimum: see the Night Watch, Vermeer\'s The Milkmaid, the collection of Delftware, and Jan Steen\'s chaotic household scenes. Avoid the audio guide and instead use the Rijksmuseum app (free, excellent) — it maps the highlights and shows you context for each work.',
              details: [
                '📍 Museumstraat 1, Amsterdam-South',
                '⏰ Open daily 9am–5pm · Allow 2–2.5 hours',
                '💰 €22.50/person — pre-book timed entry online at rijksmuseum.nl (mandatory)',
                '💡 Arrive 15 min early — even with a ticket there\'s a small security line',
                '💡 The Night Watch is in the central Gallery of Honour — you\'ll hear the gasps before you see it',
                '📷 Photography is allowed everywhere without flash — but respect other visitors near the Night Watch',
                '💡 The library (accessible from the main hall) is one of Amsterdam\'s most beautiful rooms — don\'t miss it'
              ]
            },
            {
              title: 'Museumplein & Iamsterdam Area',
              description: 'After the Rijksmuseum, the Museumplein is right outside — a large park with the Van Gogh Museum and Stedelijk Museum of modern art also flanking it. Even if you\'re saving Van Gogh for tomorrow, walk around the square. In late March, the skating rink is gone but the terrace cafés are warming up. The Vondelpark is a 5-minute walk west — Amsterdam\'s main green space, popular with locals year-round.',
              details: [
                '📍 Museumplein, Amsterdam-South',
                '🌿 Vondelpark: Stadhouderskade entrance, 5 min walk from Rijksmuseum',
                '💡 The iAmsterdam sign (famous letter sculptures) was removed from Museumplein but smaller versions exist throughout the city'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Foodhallen',
              description: 'Amsterdam\'s best food hall, set inside a converted tram depot in the Oud-West neighborhood near Museumplein. Twenty-plus vendors under one roof: Dutch bitterballen, Venezuelan arepas, Japanese ramen, wood-fired pizza, fresh oysters, and excellent natural wines. The atmosphere is industrial-cool with long communal tables, neon signs, and a serious craft beer bar. This is where Amsterdam\'s food culture lives.',
              meta: '📍 Bellamyplein 51, Oud-West · ⏰ Open daily 11am-11:30pm · 💰 €12-22/person for a meal · 🚲 5 min bike from Museumplein'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Rijksmuseum basement café is excellent but expensive. If you\'re hungry inside the museum, get a coffee and pastry at the café — the museum restaurant Rijks has Michelin-quality food but costs accordingly.' }
          ]
        },
        {
          label: 'Evening & Night',
          activities: [
            {
              title: 'After-Dinner Drinks at Leidseplein',
              description: 'Leidseplein is Amsterdam\'s busiest nightlife square — surrounded by bars, clubs, and the iconic Paradiso and Melkweg venues. For a sophisticated pre-club drink, Bar Beton (Marnixstraat 426) has an excellent cocktail menu in a stylish industrial space — a local favorite far from the tourist crush of the square itself. Alternatively, Proeflokaal de Ooievaar in the Jordaan is a classic jenever (Dutch gin) tasting house — an only-in-Amsterdam experience with dozens of local gins served in tiny tulip glasses.',
              details: [
                '📍 Leidseplein and surrounding streets',
                '🍸 Bar Beton: Marnixstraat 426 — crafted cocktails, no tourists, cool crowd',
                '🥃 Proeflokaal Wynand Fockink: Pijlsteeg 31 (near Dam Square) — 300-year-old jenever tasting house, a true Amsterdam original',
                '💡 Dutch genever (jenever) is the ancestor of gin — the aged varieties taste more like whiskey than modern gin'
              ]
            },
            {
              title: 'Night at Paradiso 🎵',
              description: 'Paradiso is Amsterdam\'s most legendary live music and club venue — a 19th-century church turned concert hall turned nightclub that has hosted everyone from The Rolling Stones to Daft Punk. On Friday nights, the programming mixes live bands with late-night DJ sets across two floors. Check the calendar at paradiso.nl before you travel — book tickets if there\'s an act you like. Even the building alone is extraordinary: soaring ceilings, Gothic windows, balconies, and one of the best sound systems in Europe.',
              details: [
                '📍 Weteringschans 6-8, near Leidseplein',
                '⏰ Doors typically 11pm–4am (varies by event)',
                '💰 €15–35/person depending on the act',
                '💡 Check paradiso.nl for Friday March 27 lineup and book tickets ahead',
                '💡 Melkweg (Lijnbaansgracht 234a) is right next door — an equally legendary former milk factory turned club. Both on the same night is possible.',
                '💡 Dress code is relaxed — Amsterdam club culture is less fashion-strict than Berlin or London'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Brasserie Van Baerle',
              description: 'An Amsterdam classic in the Museum District — Van Baerle has been serving impeccably executed French-Dutch brasserie cuisine since 1987. The crowd is a mix of after-museum diners and Oud-Zuid regulars. The menu centers on exceptional steaks, fresh North Sea fish, and seasonal dishes. The wine list is exceptional. Book the corner table by the window if you can.',
              meta: '📍 Van Baerlestraat 158, Museum District · ⏰ Dinner from 5:30pm · 💰 €35-50/person · 📞 Reserve at brasserievanbaerle.nl — popular Friday nights'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Paradiso is unmissable. Even if you don\'t care about the act, the building and the vibe are incredible. Get there around midnight when it really starts going. I\'ve been to clubs all over Europe and nothing else has that energy.', cite: 'r/Amsterdam' }
          ]
        }
      ],
      mapPins: [
        { lat: 52.3745, lng: 4.8837, label: 'Jordaan — Brouwersgracht', num: 1, cat: 'attraction', desc: 'Most beautiful canal in Amsterdam — start your walk here' },
        { lat: 52.3752, lng: 4.8872, label: 'Café Winkel 43 — Best Apple Pie', num: 2, cat: 'restaurant', desc: 'Jordaan institution — legendary appeltaart on Noordermarkt' },
        { lat: 52.3740, lng: 4.8900, label: 'De 9 Straatjes (Nine Streets)', num: 3, cat: 'attraction', desc: 'Nine charming cross-streets: cheese, vintage, boutiques, coffee' },
        { lat: 52.3600, lng: 4.8852, label: 'Rijksmuseum', num: 4, cat: 'attraction', desc: 'Dutch Golden Age art — the Night Watch, Vermeer, Delftware' },
        { lat: 52.3637, lng: 4.8787, label: 'Foodhallen', num: 5, cat: 'restaurant', desc: 'Best food hall in Amsterdam — tram depot with 20+ vendors' },
        { lat: 52.3625, lng: 4.8808, label: 'Brasserie Van Baerle', num: 6, cat: 'restaurant', desc: 'French-Dutch brasserie excellence near Museumplein' },
        { lat: 52.3625, lng: 4.8810, label: 'Bar Beton', num: 7, cat: 'nightlife', desc: 'Craft cocktails in cool industrial space — pre-Paradiso drinks' },
        { lat: 52.3624, lng: 4.8815, label: 'Paradiso', num: 8, cat: 'nightlife', desc: 'Legendary 19th-century church turned club — Amsterdam\'s greatest night out' }
      ]
    },

    // ====================================================
    // DAY 2 — Van Gogh + Albert Cuyp + Windmill Brewery + Big Night
    // ====================================================
    {
      num: 2,
      date: 'Saturday, Mar 28',
      neighborhoods: 'Museumplein · De Pijp · Oost · Rembrandtplein',
      title: 'Van Gogh, Market Feasts & Amsterdam After Dark',
      description: 'Begin with Van Gogh\'s electric canvases at the finest single-artist museum in the world, then dive into De Pijp\'s Albert Cuyp Market for the best food crawl in the city. Afternoon: craft beers in a windmill. Night: Amsterdam\'s most iconic after-dark square.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Van Gogh Museum 🌻',
              description: 'The Van Gogh Museum holds the largest collection of Van Gogh\'s work in the world — over 200 paintings and 500 drawings, arranged chronologically so you follow his life from the dark potato-eaters of the Dutch countryside to the blazing Sunflowers and Starry Night to the tragic last canvases before his death at 37. The building is beautiful, the curation is superb, and even if you think you know his work, you\'ll leave having seen it completely differently. Book timed entry for 9am — it\'s substantially quieter in the first hour.',
              details: [
                '📍 Museumplein 6, Amsterdam-South',
                '⏰ Open daily 9am–5pm (Fri/Sat until 9pm) · Allow 2–2.5 hours',
                '💰 €22/person — book timed entry at vangoghmuseum.nl (mandatory)',
                '💡 The audioguide is worth it here — Van Gogh\'s own letters are quoted throughout and they\'re extraordinary',
                '💡 Don\'t miss Room 2.3 — the Sunflowers, The Bedroom, and Almond Blossom are all here',
                '💡 The temporary exhibition changes seasonally — check what\'s on when you visit',
                '📷 Photography allowed only in selected rooms — check the floor map'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Lot Sixty One Coffee Roasters',
              description: 'Amsterdam\'s best specialty coffee shop, in the Kinkerbuurt neighborhood west of Museumplein. This is serious coffee — filter brews, meticulous pourovers, excellent pastries — in a minimal-beautiful space that coffee obsessives will recognize immediately. Go before the Van Gogh Museum to fuel up properly.',
              meta: '📍 Kinkerstraat 112, Oud-West · ⏰ Opens 8am · 💰 €4-8 · 🚲 5 min bike from Van Gogh Museum · 💡 Their natural process Ethiopian is remarkable'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you haven\'t pre-booked Van Gogh Museum tickets, do so the moment you land. Same-day tickets are theoretically available but disappear fast. The museum also has a brilliant shop with serious art books and prints — budget time for it.' }
          ]
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Albert Cuyp Market — De Pijp 🧆',
              description: 'The Albert Cuyp Market is one of Europe\'s largest outdoor markets — running 300 meters down Albert Cuypstraat in the heart of De Pijp, with 260+ stalls selling fresh herring, stroopwafels, Indonesian snacks, Dutch cheeses, flowers, clothes, and street food from dozens of cultures. Open daily except Sunday, it\'s at its Saturday best: packed, loud, delicious, and utterly alive. This is where you eat lunch — grab a raw herring (haring) from a fishmonger, fresh stroopwafels, Surinamese roti, or bitterballen. Budget about €15 for a full market crawl.',
              details: [
                '📍 Albert Cuypstraat, De Pijp · ⏰ Mon–Sat 9am–5pm',
                '🐟 Herring: order "haring met uitjes" (herring with raw onions and pickles) — eat it the Dutch way, head tilted back',
                '🍪 Stroopwafels: get them freshly made, not the packaged ones. The vendor with the longest line is the right one.',
                '🧆 Surinamese food stalls: the roti and pom here are authentic and extraordinary',
                '💡 De Pijp means "the pipe" — a 19th-century working-class neighborhood now one of Amsterdam\'s most multicultural and food-forward areas'
              ]
            },
            {
              title: 'Brouwerij \'t IJ — Windmill Craft Brewery 🍺',
              description: 'One of Amsterdam\'s most iconic experiences: a craft brewery built inside a working 18th-century windmill. Brouwerij \'t IJ has been producing excellent beers since 1985 and the tasting room at the base of the De Gooyer windmill is a genuinely remarkable space. Order a flight of their signature brews — Zatte (tripel), Natte (dubbel), Columbus (strong IPA), and Struis (barleywine) — and settle in for a proper Dutch afternoon. The terrace outside the windmill is stunning.',
              details: [
                '📍 Funenkade 7, Amsterdam-Oost · ⏰ Tasting room open daily 2pm–8pm (closed Mon/Tue) — check hours',
                '💰 Beer flights ~€12–16/person',
                '🚲 20 min bike from Albert Cuyp Market through the Oost neighborhood',
                '💡 The windmill itself (De Gooyer) is one of the last surviving windmills within Amsterdam proper',
                '💡 Arrive early on Saturdays — it gets very busy by 4pm'
              ]
            },
            {
              title: 'Explore De Pijp',
              description: 'Spend an hour wandering De Pijp after the market — Amsterdam\'s most culturally diverse and vibrant neighborhood. Sarphatipark is a small elegant park in the center, surrounded by beautiful 19th-century terraces. Browse Gerard Douplein square (known as "the square" to locals) for café terraces in the afternoon sun. The neighborhood has an unassuming, everyday Amsterdam energy that the tourist-heavy Centrum entirely lacks.',
              details: [
                '📍 De Pijp — centered around Albert Cuypstraat and Gerard Douplein',
                '💡 Look for the street art on Eerste van der Helststraat — rotating murals change monthly',
                '☕ Coffee stop: Coffee & Coconuts (Ceintuurbaan 282) — a former cinema converted into a spectacular tri-level café'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Albert Cuyp Market Crawl',
              description: 'No single restaurant — eat your way through the market. Must-tries: raw herring (€3.50), fresh stroopwafel (€2), bitterballen cone (€4), Surinamese roti or pom (€6–9), Indonesian satay stick (€3). The combination of Dutch, Indonesian, Surinamese, and Moroccan food stalls reflects Amsterdam\'s remarkable multicultural history. Budget €15–20 for a proper fill.',
              meta: '📍 Albert Cuypstraat market · 💰 €15-20 for a full market lunch · 🧆 Surinamese pom is the sleeper hit of the whole market'
            }
          ],
          tips: [
            { type: 'reddit', text: 'The Albert Cuyp Market is criminally underrated in travel guides. Skip any tourist restaurant for lunch on Saturday and eat at the market instead. The raw herring stall with the longest line is De Blauwe Viskar — it\'s worth it. And the fresh stroopwafels near the Ceintuurbaan end are life-changing.', cite: 'r/Amsterdam' }
          ]
        },
        {
          label: 'Evening & Night',
          activities: [
            {
              title: 'Pre-Dinner Cocktails — Rembrandtplein Area',
              description: 'Rembrandtplein is Amsterdam\'s other great nightlife square — slightly more local than Leidseplein, ringed by bars and cafés with terraces under heat lamps in March. Bar Oldenhof (Elandsgracht 84 in the Jordaan) is a beautifully preserved Art Deco cocktail bar with one of Amsterdam\'s most respected bar programs — a perfect pre-dinner destination. The atmosphere alone (low light, leather, dark wood) makes it worth the detour.',
              details: [
                '📍 Bar Oldenhof: Elandsgracht 84, Jordaan',
                '⏰ Opens 6pm',
                '🍸 The house Negroni and seasonal botanical cocktails are the highlights',
                '💡 This is the bar where Amsterdam professionals and food-world people go — not a tourist bar'
              ]
            },
            {
              title: 'Late Night: Melkweg or Shelter ADE',
              description: 'Saturday night in Amsterdam should be celebrated properly. Melkweg ("Milky Way") is right next to Paradiso — a former dairy factory turned legendary multi-venue arts complex with two concert halls, a cinema, gallery, and café. The Saturday night club programming runs until 5am and covers everything from house to techno to bass. If you want harder techno, Shelter Amsterdam (in the ADAM Tower north of Centraal) is a serious underground venue with top international DJs. Both require advance ticket booking on busy Saturdays.',
              details: [
                '📍 Melkweg: Lijnbaansgracht 234a, Leidseplein area',
                '📍 Shelter ADE: Overhoeksplein 3, Amsterdam-Noord (ferry from Centraal, 5 min)',
                '⏰ Doors from 11pm–5am',
                '💰 €18–30/person',
                '💡 Check melkweg.nl for Saturday March 28 programming — their Paradiso-adjacent location means a great bar crawl between both venues',
                '💡 Shelter has the best sound system in Amsterdam if you like harder electronic music'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tempo Doeloe — Indonesian Rijsttafel',
              description: 'The rijsttafel ("rice table") is Amsterdam\'s most unique dining ritual — descended from the Dutch colonial trade with Indonesia, it\'s a feast of 20+ small dishes: rendang, satay, gado gado, sambal-stacked curries, tempeh, and more, all arriving around a central bowl of steamed rice. Tempo Doeloe on Utrechtsestraat is one of Amsterdam\'s most celebrated Indonesian restaurants — the spice levels are serious (ask for "medium" if you\'re uncertain) and the experience takes 2 hours. Utterly memorable.',
              meta: '📍 Utrechtsestraat 75, near Rembrandtplein · ⏰ Dinner from 6pm · 💰 Rijsttafel €40-55/person · 📞 Reserve well in advance at tempodoeloe.nl — one of Amsterdam\'s most sought-after Saturday tables'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The rijsttafel at Tempo Doeloe is a full 2-hour experience — don\'t rush it. Order the medium sambal level unless you genuinely love extreme heat. The "Tempo Doeloe Rijsttafel" includes the best selection (about 22 dishes). Bring your appetite.' }
          ]
        }
      ],
      mapPins: [
        { lat: 52.3584, lng: 4.8811, label: 'Van Gogh Museum', num: 1, cat: 'attraction', desc: '200+ paintings — the best single-artist museum on Earth' },
        { lat: 52.3562, lng: 4.8942, label: 'Albert Cuyp Market', num: 2, cat: 'attraction', desc: '300m market — herring, stroopwafels, Indonesian food, Dutch cheese' },
        { lat: 52.3612, lng: 4.9004, label: 'Brouwerij \'t IJ — Windmill Brewery', num: 3, cat: 'activity', desc: 'Craft beers in a working 18th-century windmill — unmissable' },
        { lat: 52.3593, lng: 4.8952, label: 'Coffee & Coconuts', num: 4, cat: 'restaurant', desc: 'Stunning converted cinema café in De Pijp' },
        { lat: 52.3660, lng: 4.8963, label: 'Bar Oldenhof', num: 5, cat: 'nightlife', desc: 'Art Deco cocktail bar — Amsterdam\'s best pre-dinner drinks' },
        { lat: 52.3643, lng: 4.8975, label: 'Tempo Doeloe', num: 6, cat: 'restaurant', desc: 'Indonesian rijsttafel — 20+ dishes, a true Amsterdam tradition' },
        { lat: 52.3624, lng: 4.8814, label: 'Melkweg', num: 7, cat: 'nightlife', desc: 'Legendary multi-venue arts complex — until 5am on Saturdays' },
        { lat: 52.3978, lng: 4.9001, label: 'Shelter Amsterdam', num: 8, cat: 'nightlife', desc: 'Serious underground techno club in ADAM Tower (ferry from Centraal)' }
      ]
    },

    // ====================================================
    // DAY 3 — Anne Frank House + Canal Cruise + Jordaan Farewell
    // ====================================================
    {
      num: 3,
      date: 'Sunday, Mar 29',
      neighborhoods: 'Anne Frank House · Jordaan · Canal Ring · Centrum',
      title: 'Anne Frank, Canal Cruise & Farewell to the Jordaan',
      description: 'The most moving morning in Amsterdam at Anne Frank House, followed by a classic canal boat cruise, a long lazy Jordaan lunch, and a perfect farewell evening with Dutch jenever and canal-side reflection.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Anne Frank House 🕯️',
              description: 'One of the most profound and important experiences in all of Europe. The Anne Frank House is the hidden annex where Anne Frank, her family, and four other Jewish people hid from the Nazis for over two years, from 1942 to 1944. Walking through the actual rooms — the swinging bookcase, the tiny annex, the wall where Anne marked her growth in pencil — is deeply, undeniably moving. Allow 1.5–2 hours. The newer wing has excellent historical context on the war and Anne\'s legacy. Even if you\'ve read the diary, this is different.',
              details: [
                '📍 Westermarkt 20, Jordaan · ⏰ Open daily 9am–10pm',
                '💰 €16/person — tickets ONLY available online at annefrank.org (no walk-up entry)',
                '💡 Book tickets 4–8 weeks in advance — this is Amsterdam\'s most visited attraction and sell-out most days',
                '💡 Visit early (first session of the morning) — the space is small and emotionally intense; fewer people makes it more powerful',
                '⚠️ The house is very compact and requires climbing steep Dutch stairs — not suitable for those with mobility issues',
                '💡 Westerkerk (church next door) has a beautiful tower with views — Anne could hear its bells from the annex'
              ]
            },
            {
              title: 'Westerkerk Tower (optional)',
              description: 'Directly next to Anne Frank House, the Westerkerk is Amsterdam\'s most beautiful Protestant church, completed in 1631. Rembrandt is buried here. The tower (Westertoren) can be climbed for panoramic views over the canal ring and Jordaan — 85 meters high. Anne Frank wrote that she could see the tower from her hiding place and found comfort in its bells.',
              details: [
                '📍 Prinsengracht 281, Jordaan',
                '⏰ Tower tours: Apr–Sep (check availability in late March)',
                '💰 €8 for tower climb',
                '💡 Even if the tower isn\'t open, the church interior is free to enter and quietly beautiful'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Morning Coffee Before Anne Frank',
              name: 'Café \'t Smalle',
              description: 'One of Amsterdam\'s most charming brown cafés (bruine kroeg) — an actual 18th-century proeflokaal (tasting house) on the Egelantiersgracht in the Jordaan. The canal-side terrace has tiny wooden chairs overlooking a perfect little canal. Have a coffee and appeltaart before heading to Anne Frank House — it\'s a two-minute walk away and will set the Jordaan mood perfectly.',
              meta: '📍 Egelantiersgracht 12, Jordaan · ⏰ Opens 10am (Sun) · 💰 €4-8 · 💡 The canal terrace is worth waiting for, even in March'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Allow time after Anne Frank House to simply sit by the Prinsengracht canal and decompress. The experience is often heavier than people expect — the small scale of the hiding place makes history immediate in a way that larger memorials don\'t.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Canal Boat Cruise 🛶',
              description: 'Amsterdam has over 100 kilometers of canals — a UNESCO World Heritage Site — and seeing them from the water is completely different from the bridges. Take a 1-hour hop-on/hop-off canal boat or book a small private canal boat tour for just the two of you. The canal ring at the Herengracht, Keizersgracht, and Prinsengracht looks completely different from water level: the 17th-century gabled facades, the leaning houses, the bikes locked to every bridge. March light on the canals is cool and silver and beautiful.',
              details: [
                '📍 Multiple departure points: Centraal Station pier, Leidseplein, Rembrandtplein',
                '💰 Hop-on/hop-off: €20–25/person | Private 1hr canal boat (pedal or electric): €35–50/person',
                '💡 For a more romantic option, rent a self-drive electric boat (Sloepdelen): €50–80/hour for a 6-person boat',
                '💡 Lovers Canal Cruises and Blue Boat Company both run excellent routes',
                '💡 The Herengracht ("Gentlemen\'s Canal") is the grandest — particularly the Golden Bend section near Vijzelstraat'
              ]
            },
            {
              title: 'Spui Square & Begijnhof',
              description: 'Spui is a beautiful tree-lined square in the center of Amsterdam — on Sundays it hosts a wonderful book market (Boekenmarkt). More importantly, just off the square is the Begijnhof: a hidden medieval courtyard of houses and two chapels, one of the oldest surviving residential complexes in Amsterdam (14th century). You enter through an unremarkable door in the street and find yourself in a completely still, green courtyard. Free to enter, surprisingly unknown. One of Amsterdam\'s greatest hidden gems.',
              details: [
                '📍 Begijnhof: enter from Gedempte Begijnensloot, just off Spui · ⏰ Open daily 9am–5pm',
                '💡 Completely free — one of Amsterdam\'s best hidden places',
                '📚 Spui book market: Sundays 10am–6pm (March–November)',
                '💡 The Het Houten Huys inside the Begijnhof is one of only two remaining wooden houses in Amsterdam — from 1528'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'CT Coffee & Coconuts (or Café Caron)',
              description: 'Café Caron in De Pijp (Ferdinand Bolstraat 27) is one of Amsterdam\'s most beloved neighborhood French restaurants — steak frites, croque monsieurs, and excellent wines at honest prices. Or return to Coffee & Coconuts for a gorgeous Sunday brunch (eggs Benedict, Bircher muesli, smoothie bowls) under the spectacular cinema ceiling. Either works for a lazy post-canal Sunday lunch.',
              meta: '📍 Café Caron: Ferdinand Bolstraat 27, De Pijp · ⏰ From 12pm · 💰 €18-28/person · 💡 Very popular Sunday lunch spot — arrive when it opens'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Begijnhof is genuinely one of Amsterdam\'s best secrets. Most tourists walk right past the unassuming wooden door in the street. Inside is a perfectly preserved medieval courtyard that feels like it\'s from another century — 5 minutes of complete peace in the middle of the city.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Drinks: Dutch Jenever at Wynand Fockink',
              description: 'End your Amsterdam trip the way the locals have been ending their evenings for three centuries: at Proeflokaal Wynand Fockink, a tasting house in operation since 1679, hidden in an alley just behind Dam Square. Tiny space, wooden barrels, dozens of Dutch gins and liqueurs served in small tulip glasses so full you have to bend down to sip the first taste without spilling. This is Amsterdam in a glass — old, precise, deeply Dutch, and completely wonderful.',
              details: [
                '📍 Pijlsteeg 31, just behind Dam Square · ⏰ Open daily 3pm–9pm',
                '💰 €5-8 per glass · 💡 Order the "Korenwijn" (aged corn whiskey-style jenever) — it\'s exceptional',
                '💡 The bartenders will explain every spirit if you ask — they\'re proud of the history',
                '💡 Try the house special "Bruidstranen" (tears of the bride) — a classic Dutch liqueur from 1679'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Café de Reiger',
              description: 'A Jordaan landmark since 1929 — Café de Reiger is the platonic ideal of a Dutch eetcafé (eating café): dark wood panelling, tiled floors, beautiful old bar, and daily-changing seasonal Dutch and French-inflected food. Regulars have been coming for decades. The menu changes with what\'s local and seasonal — expect confit duck, fresh fish from the North Sea, excellent Dutch cheeses. This is the perfect final dinner in Amsterdam: intimate, local, no fuss, and genuinely great.',
              meta: '📍 Nieuwe Leliestraat 34, Jordaan · ⏰ Dinner from 5:30pm (kitchen closes 10pm) · 💰 €28-40/person · 💡 One of Amsterdam\'s most beloved old-guard restaurants — reserve ahead at cafedereiger.nl'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, walk the Jordaan one last time at night. The small canals lit from below, the lights in the canal houses, the old bridges — it\'s one of the most beautiful urban walks in Europe. The Egelantiersgracht at 10pm in late March, with the reflection of the gabled houses in the still canal, is an image that will stay with you.' }
          ]
        }
      ],
      mapPins: [
        { lat: 52.3752, lng: 4.8840, label: 'Anne Frank House', num: 1, cat: 'attraction', desc: 'The hidden annex — book tickets 4-8 weeks ahead at annefrank.org' },
        { lat: 52.3744, lng: 4.8836, label: 'Café \'t Smalle', num: 2, cat: 'restaurant', desc: '18th-century canal-side brown café — perfect pre-visit coffee' },
        { lat: 52.3747, lng: 4.8874, label: 'Westerkerk', num: 3, cat: 'attraction', desc: '1631 church where Rembrandt is buried — Anne Frank could hear its bells' },
        { lat: 52.3698, lng: 4.8903, label: 'Canal Cruise Departure — Leidseplein', num: 4, cat: 'activity', desc: 'Hop-on/hop-off or private electric canal boat — see Amsterdam from water level' },
        { lat: 52.3700, lng: 4.8941, label: 'Begijnhof — Hidden Medieval Courtyard', num: 5, cat: 'attraction', desc: '14th-century hidden courtyard off Spui — one of Amsterdam\'s best secrets' },
        { lat: 52.3711, lng: 4.8898, label: 'Spui Book Market (Sunday)', num: 6, cat: 'attraction', desc: 'Outdoor book market on Sundays — local and antiquarian books' },
        { lat: 52.3726, lng: 4.8964, label: 'Wynand Fockink — Jenever Tasting', num: 7, cat: 'nightlife', desc: 'Proeflokaal since 1679 — Dutch jenever in tulip glasses, just off Dam Square' },
        { lat: 52.3761, lng: 4.8820, label: 'Café de Reiger', num: 8, cat: 'restaurant', desc: 'Jordaan eetcafé since 1929 — the perfect final dinner in Amsterdam' }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('\n✅ Fulfilled Amsterdam order!');
    console.log('Slug:', result.slug);
    console.log('URL:', result.url);
    console.log('Email sent:', result.emailSent);
  })
  .catch(err => {
    console.error('\n❌ Fulfillment failed:', err.message);
    process.exit(1);
  });
