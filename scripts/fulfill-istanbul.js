const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771301199198_dds92g',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Istanbul, İstanbul, Türkiye',
};

const itineraryData = {
  destination: 'Istanbul, Türkiye',
  countryEmoji: '🇹🇷',
  title: 'Istanbul: Where East Meets West',
  subtitle: 'Four days of Byzantine wonders, Ottoman grandeur, Bosphorus sunsets, and the world\'s greatest street food — solo and at your own pace',
  description: 'Istanbul is a city that straddles two continents and twenty centuries. This solo itinerary weaves through the ancient Sultanahmet quarter, colorful Balat streets, bustling bazaars, and serene Bosphorus shores. You\'ll start mornings with lavish Turkish breakfasts, wander Byzantine and Ottoman masterpieces, unwind in a centuries-old hammam, and end evenings watching the sun set over the strait with a glass of çay in hand. May is Istanbul at its finest — warm, blooming, and buzzing.',
  duration: '4 nights',
  dates: 'May 8 – May 12, 2026',
  budget: '$800 – $1,500',
  pace: 'Relaxed',
  bestFor: 'Solo travelers, Culture lovers, Relaxation seekers',
  highlights: ['Hagia Sophia & Blue Mosque', 'Bosphorus sunset cruise', 'Traditional hammam experience', 'Grand Bazaar & Spice Bazaar', 'Colorful Balat neighborhood', 'Kadıköy Asian side exploration', 'Turkish breakfast spreads', 'Fish sandwich at Eminönü'],

  essentials: [
    { title: '🛬 Getting Around', text: 'Get an Istanbulkart at the airport (works on metro, tram, ferries, buses). Tram T1 connects the airport shuttle to Sultanahmet. Ferries are the best way to cross the Bosphorus. Taxis use meters — insist on it, or use BiTaksi app.' },
    { title: '💵 Money', text: 'Turkish Lira (TRY). Cards widely accepted in tourist areas, but carry cash for bazaars, street food, and small shops. ATMs (Garanti, İş Bankası) everywhere. Budget ₺1,500-3,000/day comfortably.' },
    { title: '🗣️ Language', text: 'Turkish. English spoken in tourist areas and hotels. Learn a few phrases: Merhaba (hello), Teşekkürler (thanks), Lütfen (please). Shopkeepers in bazaars often speak multiple languages.' },
    { title: '🌦️ Weather in May', text: 'Perfect season — 15-24°C (59-75°F), mostly sunny with occasional showers. Light layers, comfortable walking shoes, and a light jacket for evening Bosphorus breezes.' },
    { title: '🕌 Mosque Etiquette', text: 'Remove shoes, cover shoulders and knees. Women should bring a headscarf (loaners available at Blue Mosque). Avoid prayer times for tourist visits. Photography generally okay outside prayer.' },
    { title: '🔒 Safety', text: 'Istanbul is very safe for solo travelers. Standard big-city awareness applies. Avoid unlicensed taxis. The tourist police (Turizm Polisi) are helpful. Solo dining is completely normal.' },
  ],

  days: [
    // DAY 1 — Sultanahmet: The Imperial Core
    {
      num: 1,
      title: 'Sultanahmet: Byzantine & Ottoman Treasures',
      description: 'Dive into Istanbul\'s ancient heart — Hagia Sophia, the Blue Mosque, and the sprawling Topkapi Palace, followed by a hammam to melt away travel fatigue.',
      neighborhoods: 'Sultanahmet · Fatih',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hagia Sophia (Ayasofya)',
              description: 'Begin at the building that changed architecture forever. Built in 537 AD as a Byzantine cathedral, converted to a mosque, then a museum, and now a mosque again — its massive dome and golden mosaics remain breathtaking after 1,500 years.',
              details: ['📍 Sultanahmet Mh., Ayasofya Meydanı, Fatih', '🕐 Open daily, free admission (mosque) · Closed briefly during prayer times', '💡 Arrive by 8:30am to beat tour groups. The upper gallery mosaics are extraordinary.']
            },
            {
              title: 'Blue Mosque (Sultan Ahmed Camii)',
              description: 'Just across the square from Hagia Sophia, the Blue Mosque (1616) gets its name from 20,000+ hand-painted İznik tiles lining the interior. Six minarets punctuate the skyline — a bold statement of Ottoman ambition.',
              details: ['📍 Sultanahmet Mh., Atmeydanı Cd., Fatih', '🕐 Open outside prayer times · Free admission', '💡 Visit between prayers. The interior is most atmospheric in morning light.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Sultanahmet Köftecisi',
              description: 'A no-frills Istanbul institution since 1920. Famous for its grilled köfte (meatballs) served with white beans, bread, and sharp pickled peppers. Simple, perfect, and beloved by locals.',
              meta: '📍 Divanyolu Cd. No:12, Sultanahmet · 💰 ₺150-200 · 🕐 Opens 8am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Sultanahmet tram stop puts you right between Hagia Sophia and Blue Mosque. Start your day here.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Topkapi Palace (Topkapı Sarayı)',
              description: 'The nerve center of the Ottoman Empire for 400 years. Explore the Imperial Treasury (the 86-carat Spoonmaker\'s Diamond), the Harem\'s tiled labyrinth, and the terrace overlooking the Golden Horn and Bosphorus.',
              details: ['📍 Cankurtaran Mh., Fatih', '🕐 9am-6pm (closed Tuesdays) · ₺750 + ₺400 for Harem', '💡 Buy combined ticket. The Harem is the highlight — don\'t skip it.']
            },
            {
              title: 'Basilica Cistern (Yerebatan Sarnıcı)',
              description: 'Descend into the atmospheric 6th-century underground cistern — 336 marble columns rising from still water, dramatically lit. Look for the two Medusa head column bases.',
              details: ['📍 Yerebatan Cd. 1/3, Sultanahmet', '🕐 9am-7pm · ₺450', '💡 Beautifully renovated. The lighting and music create an almost otherworldly atmosphere.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Matbah Restaurant',
              description: 'Ottoman palace cuisine reimagined — located inside the Ottoman Hotel Imperial near Hagia Sophia. Try the lamb tandir, stuffed quince, or Ottoman meze platter. A fitting lunch after Topkapi.',
              meta: '📍 Caferiye Sk. No:6/1, Sultanahmet · 💰 ₺400-600 · ⭐ Ottoman fine dining'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Çemberlitaş Hamamı',
              description: 'Built in 1584 by the great architect Mimar Sinan, this is one of Istanbul\'s most beautiful and authentic hammams. Lie on the heated marble göbektaşı (belly stone), get scrubbed and massaged, and let the travel tension dissolve under the domed ceiling.',
              details: ['📍 Vezirhan Cd. No:8, Çemberlitaş, Fatih', '💰 ₺1,200-2,000 for traditional bath + scrub + massage', '💡 Book the full traditional package. Solo-friendly — very used to international visitors.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tarihi Sultanahmet Meze & Kebap',
              description: 'A terrace dinner with views of the Blue Mosque\'s illuminated minarets. Classic Turkish meze spread — hummus, ezme, sigara böreği — followed by Adana kebab or mixed grill.',
              meta: '📍 Sultanahmet area · 💰 ₺300-500 · 🌙 Mosque views at night'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After the hammam, you\'ll feel reborn. Walk back through the illuminated Sultanahmet square — the Blue Mosque glows blue at night.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.0086, lng: 28.9802, label: 'Hagia Sophia', num: 1, cat: 'attraction', desc: '6th-century architectural masterpiece, now a mosque' },
        { lat: 41.0054, lng: 28.9768, label: 'Blue Mosque', num: 2, cat: 'attraction', desc: 'Iconic 17th-century mosque with 20,000 İznik tiles' },
        { lat: 41.0070, lng: 28.9772, label: 'Sultanahmet Köftecisi', num: 3, cat: 'restaurant', desc: 'Legendary köfte since 1920' },
        { lat: 41.0115, lng: 28.9834, label: 'Topkapi Palace', num: 4, cat: 'attraction', desc: 'Ottoman imperial residence with Treasury & Harem' },
        { lat: 41.0084, lng: 28.9779, label: 'Basilica Cistern', num: 5, cat: 'attraction', desc: 'Atmospheric underground Byzantine cistern' },
        { lat: 41.0080, lng: 28.9715, label: 'Çemberlitaş Hamamı', num: 6, cat: 'wellness', desc: 'Historic 1584 hammam by Mimar Sinan' },
        { lat: 41.0092, lng: 28.9790, label: 'Matbah Restaurant', num: 7, cat: 'restaurant', desc: 'Ottoman palace cuisine near Hagia Sophia' }
      ]
    },

    // DAY 2 — Bazaars, Balat & Golden Horn
    {
      num: 2,
      title: 'Bazaars, Balat & the Golden Horn',
      description: 'Explore Istanbul\'s legendary bazaars, then wander the colorful streets of Balat — the city\'s most photogenic and soulful neighborhood.',
      neighborhoods: 'Beyazıt · Eminönü · Balat · Fener',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Grand Bazaar (Kapalıçarşı)',
              description: 'One of the world\'s oldest and largest covered markets — 4,000+ shops across 61 streets. Don\'t try to see it all. Focus on the central jewelry lanes, ceramic shops, leather artisans, and the historic Kalpakçılar Caddesi (main street). Haggling is expected.',
              details: ['📍 Beyazıt, Fatih', '🕐 9am-7pm (closed Sundays)', '💡 Go early to beat the crowds. Get lost on purpose — the side alleys are where the magic is.']
            },
            {
              title: 'Spice Bazaar (Mısır Çarşısı)',
              description: 'The aromatic L-shaped bazaar at Eminönü, built in 1664. Towers of colorful spices, Turkish delight, dried fruits, teas, and saffron. More focused and less overwhelming than the Grand Bazaar.',
              details: ['📍 Rüstem Paşa Mh., Eminönü, Fatih', '🕐 8am-7:30pm daily', '💡 Buy Turkish delight here (try pomegranate or pistachio), lokum, and baharat spice mixes to take home.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Van Kahvaltı Evi',
              description: 'A legendary Turkish breakfast spot in Cihangir. Massive spread of cheeses, honey with kaymak (clotted cream), sucuk (spicy sausage), eggs, jams, olives, fresh bread, and endless çay. This is what Turkish breakfast dreams are made of.',
              meta: '📍 Kılıçali Paşa Mh., Defterdar Ykş. 52/A, Beyoğlu · 💰 ₺250-400 · 🕐 Opens 8am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 From the Spice Bazaar, walk outside to the Eminönü waterfront for a balık ekmek (fish sandwich) from the iconic boats — ₺80-100 for Istanbul\'s most famous street food.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Fish Sandwich at Eminönü',
              description: 'Step outside the Spice Bazaar to the Galata Bridge waterfront where rocking boats grill fresh fish and stuff it into crusty bread with onions and lettuce. Eat it on the bridge watching ferries crisscross the Golden Horn. Pure Istanbul.',
              details: ['📍 Eminönü waterfront, near Galata Bridge', '💰 ₺80-100', '💡 Squeeze lemon, add salt, eat immediately. That\'s the ritual.']
            },
            {
              title: 'Rüstem Pasha Mosque',
              description: 'A hidden Sinan gem tucked above the Eminönü shops. The interior İznik tile work is arguably finer than the Blue Mosque — thousands of tulip-patterned tiles in deep red and blue. Most tourists miss this one.',
              details: ['📍 Hasırcılar Cd., Eminönü, Fatih', '🕐 Open daily, free · Closed during prayer', '💡 Look for the entrance up a narrow staircase from the street level shops.']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Balat & Fener Neighborhoods',
              description: 'Istanbul\'s most colorful and atmospheric quarter. Walk the steep streets lined with candy-colored Ottoman houses, antique shops, and local cafes. This old Greek, Jewish, and Armenian quarter is Instagram-famous but still genuinely lived-in.',
              details: ['📍 Balat & Fener, Fatih (bus 99A from Eminönü or walk 20 min)', '💡 Key streets: Merdivenli Yokuş (the famous colorful stairs), Vodina Caddesi, and the streets around the red-brick Phanar Greek Orthodox College.']
            },
            {
              title: 'Tea at Fener Café or Naftalin K',
              description: 'Settle into one of Balat\'s charming cafes with a Turkish tea or coffee. Naftalin K is an art-filled local favorite in a restored building. Watch the neighborhood life unfold from a window seat.',
              details: ['📍 Balat, Fatih', '💰 ₺50-100 for drinks and a snack', '💡 Balat is best in late afternoon golden light.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Asitane',
              description: 'One of Istanbul\'s most unique restaurants — serving recreated Ottoman palace recipes from 15th-17th century archives. Dishes like stuffed melon, almond soup, and mutancana (lamb with dried fruits). A culinary time machine.',
              meta: '📍 Kariye Camii Sk. No:6, Edirnekapı, Fatih · 💰 ₺500-800 · ⭐ Ottoman palace cuisine'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Asitane is near the Chora Church (Kariye Mosque) — if it\'s open for visitors, the Byzantine mosaics inside rival those in Hagia Sophia.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.0106, lng: 28.9680, label: 'Grand Bazaar', num: 1, cat: 'shopping', desc: '4,000+ shops in the world\'s oldest covered market' },
        { lat: 41.0163, lng: 28.9705, label: 'Spice Bazaar', num: 2, cat: 'shopping', desc: 'Aromatic spice market since 1664' },
        { lat: 41.0264, lng: 28.9740, label: 'Van Kahvaltı Evi', num: 3, cat: 'restaurant', desc: 'Legendary Turkish breakfast spread' },
        { lat: 41.0175, lng: 28.9693, label: 'Eminönü Fish Boats', num: 4, cat: 'restaurant', desc: 'Iconic fish sandwich from rocking boats' },
        { lat: 41.0165, lng: 28.9678, label: 'Rüstem Pasha Mosque', num: 5, cat: 'attraction', desc: 'Hidden Sinan masterpiece with incredible İznik tiles' },
        { lat: 41.0303, lng: 28.9485, label: 'Balat Neighborhood', num: 6, cat: 'neighborhood', desc: 'Colorful Ottoman streets, antique shops & cafes' },
        { lat: 41.0325, lng: 28.9390, label: 'Asitane', num: 7, cat: 'restaurant', desc: 'Ottoman palace recipes from 15th-century archives' }
      ]
    },

    // DAY 3 — Bosphorus & Asian Side
    {
      num: 3,
      title: 'Bosphorus Cruise & the Asian Side',
      description: 'Cross to another continent. A morning Bosphorus cruise reveals Ottoman waterfront palaces, then explore the vibrant Kadıköy market and Moda\'s seaside promenade.',
      neighborhoods: 'Eminönü · Bosphorus · Kadıköy · Moda',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bosphorus Cruise',
              description: 'Take the official Şehir Hatları ferry from Eminönü for the full Bosphorus cruise (or the shorter 2-hour version). Glide past Dolmabahçe Palace, Ortaköy Mosque, the Bosphorus bridges, Rumeli Hisarı fortress, and elegant yalı (waterfront mansions). The short cruise turns around at Anadolu Kavağı.',
              details: ['📍 Şehir Hatları dock, Eminönü (near Galata Bridge)', '🕐 Short cruise: 10:35am departure, ~2 hours round trip · ₺150 with Istanbulkart', '💡 Sit on the right (European) side going up, left side coming back. Morning light is best.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Simit & Çay at the Eminönü Waterfront',
              description: 'Istanbul\'s quintessential grab-and-go breakfast: a sesame-crusted simit (Turkish bagel) with a tulip glass of black çay from a waterfront vendor. Eat on the Galata Bridge watching the morning ferry traffic.',
              meta: '📍 Eminönü waterfront · 💰 ₺30-50 · 🕐 Any time from dawn'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The short Bosphorus cruise (2h) gives you all the highlights and leaves afternoon free. The full cruise (6h) goes further but eats the whole day.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ferry to Kadıköy (Asian Side)',
              description: 'Take the ferry from Eminönü to Kadıköy (20 min, ₺15 with Istanbulkart). The crossing itself is magical — skyline views of the Old City, Galata Tower, and the minarets. Kadıköy is Istanbul\'s most vibrant, local neighborhood.',
              details: ['📍 Kadıköy ferry terminal', '💡 Ferries run frequently. The ride is one of Istanbul\'s best experiences — cheap and beautiful.']
            },
            {
              title: 'Kadıköy Market & Streets',
              description: 'Wander the bustling Kadıköy produce market (Kadıköy Çarşı) — fishmongers, olive vendors, cheese shops, pickle stalls, and fresh-squeezed pomegranate juice. Then explore the surrounding streets full of record shops, bookstores, street art, and local bars.',
              details: ['📍 Kadıköy Çarşı, Kadıköy', '💡 Try a midye dolma (stuffed mussels) from a street vendor — ₺10-15 each. Squeeze lemon, pop it in.']
            },
            {
              title: 'Moda Seaside Walk',
              description: 'Walk the Moda coastal promenade — a peaceful waterfront path with stunning views back toward the European side, the Maiden\'s Tower, and the Sea of Marmara. Locals jog, read, and drink çay here. Find a bench and soak it in.',
              details: ['📍 Moda, Kadıköy', '💡 Walk from Kadıköy center to Moda neighborhood (15 min). The coastal path loops around the peninsula.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Çiya Sofrası',
              description: 'Istanbul\'s most celebrated lokanta (home-style restaurant). Chef Musa Dağdeviren is a culinary anthropologist who rescues forgotten regional Turkish dishes. The kebab and stew buffet changes daily. Anthony Bourdain called it one of his favorites.',
              meta: '📍 Güneşlibahçe Sk. No:43, Kadıköy · 💰 ₺200-350 · ⭐ Featured in Chef\'s Table'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Kadıköy is where Istanbullus actually eat. Less tourist pricing, more authentic energy. Spend a real afternoon here.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from Üsküdar Waterfront',
              description: 'Take the ferry from Kadıköy to Üsküdar for Istanbul\'s most famous sunset. Sit at the Kuzguncuk or Üsküdar waterfront with a çay and watch the sun drop behind the European skyline — the silhouettes of Sultanahmet\'s mosques and minarets against orange sky.',
              details: ['📍 Üsküdar İskelesi (ferry terminal) waterfront', '💡 Sunset in May is around 8pm. Grab çay from the waterfront vendors. This is THE Istanbul sunset experience.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kanaat Lokantası',
              description: 'A beloved Üsküdar institution since 1933. Traditional Turkish home cooking — try the lamb güveç (clay pot stew), İskender kebab, or quince dessert with kaymak. Locals have been eating here for generations.',
              meta: '📍 Selmanipak Cd. No:9, Üsküdar · 💰 ₺200-350 · 🕐 Open until 11pm'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, take the ferry back to Eminönü at night — the illuminated mosques and Galata Tower from the water are unforgettable.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.0175, lng: 28.9693, label: 'Eminönü Ferry Dock', num: 1, cat: 'transport', desc: 'Bosphorus cruise departure point' },
        { lat: 41.0891, lng: 29.0570, label: 'Anadolu Kavağı', num: 2, cat: 'attraction', desc: 'Bosphorus cruise turnaround — hilltop fortress views' },
        { lat: 40.9901, lng: 29.0234, label: 'Kadıköy Market', num: 3, cat: 'shopping', desc: 'Vibrant local produce market on the Asian side' },
        { lat: 40.9871, lng: 29.0278, label: 'Çiya Sofrası', num: 4, cat: 'restaurant', desc: 'Legendary regional Turkish cuisine — Chef\'s Table fame' },
        { lat: 40.9833, lng: 29.0310, label: 'Moda Promenade', num: 5, cat: 'attraction', desc: 'Seaside walk with European skyline views' },
        { lat: 41.0250, lng: 29.0156, label: 'Üsküdar Sunset Point', num: 6, cat: 'attraction', desc: 'Best sunset view of Istanbul\'s mosque skyline' },
        { lat: 41.0242, lng: 29.0172, label: 'Kanaat Lokantası', num: 7, cat: 'restaurant', desc: 'Üsküdar classic since 1933 — traditional home cooking' }
      ]
    },

    // DAY 4 — Beyoğlu, Galata & Farewell
    {
      num: 4,
      title: 'Beyoğlu, Galata Tower & İstiklal Farewell',
      description: 'Explore the vibrant European \'new city\' — climb Galata Tower, stroll İstiklal Avenue, discover hidden passages, and say goodbye over rooftop meze with Bosphorus views.',
      neighborhoods: 'Karaköy · Galata · Beyoğlu · Cihangir',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Galata Tower (Galata Kulesi)',
              description: 'The 14th-century Genoese watchtower is one of Istanbul\'s most iconic landmarks. Climb to the top for 360° panoramic views — the Old City, the Bosphorus, the Golden Horn, and the Asian shore all visible at once.',
              details: ['📍 Bereketzade Mh., Galata Kulesi Sk., Beyoğlu', '🕐 8:30am-11pm · ₺650', '💡 Go at opening (8:30am) to avoid lines. The views are worth the climb.']
            },
            {
              title: 'Galata & Karaköy Streets',
              description: 'Wander downhill from the tower through Galata\'s cobblestone streets — independent coffee shops, vinyl stores, vintage boutiques, and art galleries fill this once-Genoese quarter. Karaköy below has become Istanbul\'s café and street art hub.',
              details: ['📍 Galata & Karaköy, Beyoğlu', '💡 Stop at Karabatak or Kronotrop for excellent Turkish specialty coffee.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Karaköy Güllüoğlu',
              description: 'Turkey\'s most famous baklava house — the Güllüoğlu family has been making baklava since 1820. Start your final day with pistachio baklava and a glass of çay. Yes, baklava for breakfast. You\'re in Istanbul.',
              meta: '📍 Kemankeş Karamustafa Paşa Mh., Mumhane Cd., Karaköy · 💰 ₺100-180 · 🕐 Opens 7am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The walk from Galata Tower down to Karaköy through winding streets is one of Istanbul\'s most charming routes.' }
          ]
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'İstiklal Avenue (İstiklal Caddesi)',
              description: 'Istanbul\'s grand pedestrian boulevard — nearly 1.5km of shops, cafes, bookstores, churches, consulates, and the nostalgic red tram. Duck into the historic passages (pasajlar) — Çiçek Pasajı (Flower Passage) and the surrounding Balık Pazarı (Fish Market) for meze and raki.',
              details: ['📍 İstiklal Cd., Beyoğlu (from Tünel to Taksim)', '💡 The side streets and passages are more interesting than the main drag. Explore Nevizade Sokak for the liveliest meyhane (tavern) street.']
            },
            {
              title: 'Çiçek Pasajı & Nevizade Sokak',
              description: 'Duck into the ornate 19th-century Çiçek Pasajı (Flower Passage) for the atmosphere, then continue to adjacent Nevizade Sokak — a narrow lane packed with meyhane tables spilling into the street. This is where Istanbul comes to drink raki and eat meze.',
              details: ['📍 Hüseyinağa Mh., İstiklal Cd., Beyoğlu', '💡 Perfect for a long, leisurely meze lunch with raki.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nevizade Sokak Meyhane',
              description: 'Pick any bustling meyhane on Nevizade Street for a long meze lunch. Order a raki, then let the meze flow: haydari (yogurt dip), acılı ezme, octopus salad, sigara böreği, fried calamari. This is the Istanbul lunch experience.',
              meta: '📍 Nevizade Sk., Beyoğlu · 💰 ₺300-500 with raki · 🍸 Lion\'s milk (raki) flows'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Raki tip: sip it slowly with cold water, always with meze. Never on an empty stomach. Turks call it \'lion\'s milk\' because it turns milky white when mixed.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at a Rooftop Bar',
              description: 'End your Istanbul journey at a rooftop bar overlooking the Bosphorus and the Old City. Mikla (at the Marmara Pera hotel) offers Scandinavian-Turkish fusion cuisine with jaw-dropping views. Or try 360 İstanbul on İstiklal for a cocktail with panoramic views.',
              details: ['📍 Mikla: The Marmara Pera, Meşrutiyet Cd. No:15, Beyoğlu', '📍 360 İstanbul: İstiklal Cd. No:163, Beyoğlu', '💡 Book ahead for Mikla dinner. 360 is more casual for drinks.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mikla',
              description: 'Chef Mehmet Gürs\' rooftop restaurant at the Marmara Pera hotel — Turkish-Scandinavian tasting menu with stunning views over the Golden Horn and Bosphorus. One of Istanbul\'s most acclaimed fine dining experiences. A fitting farewell dinner.',
              meta: '📍 Meşrutiyet Cd. No:15, Beyoğlu · 💰 ₺1,500-2,500 · ⭐ Regularly on World\'s 50 Best list'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Final night tradition: walk down to Galata Bridge after dinner. The bridge comes alive at night with fishermen, tea sellers, and the illuminated city on both sides.' }
          ]
        }
      ],
      mapPins: [
        { lat: 41.0256, lng: 28.9741, label: 'Galata Tower', num: 1, cat: 'attraction', desc: '14th-century tower with 360° panoramic views' },
        { lat: 41.0220, lng: 28.9770, label: 'Karaköy Güllüoğlu', num: 2, cat: 'restaurant', desc: 'Turkey\'s most famous baklava since 1820' },
        { lat: 41.0235, lng: 28.9755, label: 'Karaköy & Galata Streets', num: 3, cat: 'neighborhood', desc: 'Coffee shops, art galleries, vintage boutiques' },
        { lat: 41.0340, lng: 28.9770, label: 'İstiklal Avenue', num: 4, cat: 'attraction', desc: 'Grand pedestrian boulevard with historic passages' },
        { lat: 41.0340, lng: 28.9760, label: 'Nevizade Sokak', num: 5, cat: 'restaurant', desc: 'Lively meyhane street — meze & raki paradise' },
        { lat: 41.0313, lng: 28.9725, label: 'Mikla Restaurant', num: 6, cat: 'restaurant', desc: 'Rooftop fine dining — Turkish-Scandinavian fusion with views' },
        { lat: 41.0202, lng: 28.9732, label: 'Galata Bridge', num: 7, cat: 'attraction', desc: 'Iconic bridge — fishermen, tea, illuminated city views' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (4 nights)', budget: '$300 – $600', notes: 'Boutique hotel in Sultanahmet or Beyoğlu' },
    { category: 'Food & Drink', budget: '$200 – $400', notes: 'Mix of street food, lokanta, and fine dining' },
    { category: 'Transportation', budget: '$30 – $50', notes: 'Istanbulkart covers tram, metro, ferries' },
    { category: 'Attractions', budget: '$80 – $120', notes: 'Topkapi, Basilica Cistern, Galata Tower' },
    { category: 'Hammam', budget: '$40 – $70', notes: 'Full traditional bath + scrub + massage' },
    { category: 'Bosphorus Cruise', budget: '$10 – $15', notes: 'Public ferry short cruise' },
    { category: 'Shopping & Souvenirs', budget: '$50 – $200', notes: 'Ceramics, spices, Turkish delight, textiles' },
  ],

  practicalInfo: [
    { title: '✈️ Airport Transfer', items: ['Istanbul Airport (IST) is 35km from the city center', 'Havaist bus to Taksim (₺140, ~90 min) or taxi (₺400-600, ~45 min)', 'Metro M11 connects to Gayrettepe station'] },
    { title: '📱 Connectivity', items: ['Buy a local SIM at the airport (Turkcell or Vodafone, ~₺500 for tourist package with data)', 'Free Wi-Fi in most cafes and hotels'] },
    { title: '💡 Istanbulkart', items: ['Essential — load at kiosks in metro stations', 'Works on all public transport including ferries', 'Tap to enter, tap to exit — much cheaper than single tickets'] },
    { title: '🕌 Friday Prayers', items: ['Major mosques close to tourists during Friday midday prayers (~12:30-2pm)', 'Plan mosque visits around this schedule'] },
    { title: '🧖 Hammam Tips', items: ['Bring your own flip-flops — you\'ll be given a peştamal (wrap cloth)', 'Men and women bathe separately in traditional hammams', 'Tip your tellak (scrubber) 15-20%'] },
    { title: '💧 Water & Drinks', items: ['Tap water is safe but tastes of chlorine — bottled water ₺10-15', 'Ayran (salted yogurt drink) is the local refresher — try it with kebabs'] },
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
