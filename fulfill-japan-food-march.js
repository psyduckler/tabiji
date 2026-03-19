const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1773640104252_xih28b',
  orderId: 'order_1773640104252_xih28b',
  email: 'paudcll4@gmail.com',
  destination: 'Japan',
  start_date: '2026-03-17',
  end_date: '2026-03-25',
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'Sakura Trail: Hakuba to Kyoto & the Heart of Cherry Blossom Season',
  subtitle: 'Nine days through Japan\'s most beautiful spring landscapes — from alpine Takayama to ancient Kyoto, Yoshino\'s legendary cherry mountains, Nara\'s deer parks, and Osaka\'s vibrant food scene',
  description: 'Late March in Japan is the moment the entire country has been waiting for: cherry blossom season arrives in the Kansai region. This itinerary takes you from the mountains of Hakuba south through Takayama\'s Edo-period streets, then deep into the heart of sakura country — Kyoto\'s temple gardens bursting with pink, Yoshino\'s mountainside covered in 30,000 cherry trees (Japan\'s most famous blossom site), Nara\'s friendly deer wandering beneath flowering canopies, and Osaka\'s castle park lit up at night. Every day is built around what makes late March magical: specific temples at peak bloom, seasonal foods you can only eat now, and festivals that celebrate spring\'s arrival. You\'ll end by heading to your new home in Naka-Meguro, Tokyo — just in time for the Meguro River sakura to bloom.',
  duration: '9 days / 8 nights',
  dates: 'Mar 17 – Mar 25, 2026',
  budget: 'Moderate',
  pace: 'Moderate',
  bestFor: 'Solo travelers, Cherry blossom chasers, Culture & food lovers',

  highlights: [
    'Takayama\'s preserved Edo-era streets and morning markets with seasonal mountain cuisine',
    'Kyoto at peak cherry blossom — Philosopher\'s Path, Maruyama Park, Kiyomizu-dera at sunset',
    'Mount Yoshino: Japan\'s #1 cherry blossom spot with 30,000 trees cascading down the mountain',
    'Nara\'s 1,200 free-roaming deer under cherry blossoms at Nara Park',
    'Osaka Castle Park sakura and Dōtonbori street food — takoyaki, okonomiyaki, kushikatsu',
    'Fushimi Inari\'s 10,000 vermillion torii gates at golden hour'
  ],

  essentials: [
    { title: '🚄 Getting Around', text: 'A 7-day JR Pass (¥50,000/~$330) activated on Day 1 covers the Hakuba→Nagoya→Takayama and Takayama→Kyoto segments, plus Kyoto→Nara, Kyoto→Osaka, and Osaka→Tokyo. Within Kyoto, use city buses (¥230/ride) or rent a bicycle. IC card (Suica/Pasmo) works for local trains and buses everywhere.' },
    { title: '💵 Budget', text: 'Moderate budget: ¥8,000-12,000/day covers food, transport top-ups, and admissions. Accommodation: ¥4,000-7,000/night for business hotels and hostels, plus one ryokan night in Takayama (¥10,000-15,000). Japan is very cash-friendly — ATMs at 7-Eleven and post offices accept international cards.' },
    { title: '🌸 Cherry Blossom Intel', text: 'Late March 2026 forecast: Kyoto first bloom ~March 23, full bloom ~March 30. Yoshino first bloom ~March 25. Osaka first bloom ~March 22. You\'ll catch the exciting early blooms opening — the most photogenic moment. Some early-blooming varieties (shidare-zakura, kawazu-zakura) will already be full.' },
    { title: '🏨 Accommodation', text: 'Mix of business hotels (Toyoko Inn, APA Hotel: ¥5,000-7,000), one capsule hotel in Osaka for the experience (¥3,000-4,000), and a traditional ryokan in Takayama. Book Kyoto accommodation early — cherry blossom season is peak and prices surge.' },
    { title: '🗣️ Language Tips', text: 'Kyoto and Osaka are tourist-friendly with good English signage. Takayama and Yoshino less so — Google Translate camera mode is essential. Key phrases: sumimasen (excuse me), oishii (delicious), ikura desu ka (how much?), kore kudasai (this one please).' },
    { title: '🎒 Packing', text: 'Mid-late March: 10-18°C in Kansai, cooler in Takayama (5-12°C). Layers are key. Bring a compact umbrella (spring showers), comfortable walking shoes (you\'ll walk 15,000-20,000 steps/day), and a small towel for onsen. Use takkyubin luggage forwarding (¥2,000) to ship bags ahead.' }
  ],

  days: [
    // ===================== DAY 1 — March 17: Hakuba → Takayama =====================
    {
      num: 1,
      date: 'March 17',
      neighborhoods: 'Hakuba · Matsumoto · Takayama',
      title: 'Mountain to Mountain: Hakuba to Takayama\'s Edo Streets',
      description: 'Leave Hakuba and travel south through Matsumoto (quick stop if time allows), then onward to Takayama — a beautifully preserved Edo-period town in the Japanese Alps known for its morning markets, Hida beef, and sake breweries.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hakuba → Matsumoto → Takayama by Train',
              description: 'Take the JR Oito Line from Hakuba to Matsumoto (~2 hours through scenic alpine valleys). From Matsumoto, transfer to the JR Wide View Hida limited express to Takayama (~2 hours through the dramatic Hida mountain gorge). This is one of Japan\'s most beautiful train rides — the train winds along river gorges with snow-capped peaks.',
              details: [
                '🚂 Hakuba → Matsumoto: JR Oito Line (~2h, ¥1,170)',
                '🚂 Matsumoto → Takayama: JR Wide View Hida (~2h, ¥4,510) — covered by JR Pass',
                '💡 Sit on the right side for the best gorge views after Matsumoto',
                '⏰ Aim to depart Hakuba by 8am to arrive Takayama by ~1pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch (Matsumoto Station or on the train)',
              name: 'Shinshu Soba Eki-ben',
              description: 'Nagano prefecture is famous for buckwheat soba. Grab a cold soba bento at Matsumoto Station or eat at the standing soba shop on the platform — fresh, fast, and delicious.',
              meta: '💰 ¥600-900 · Matsumoto Station platform or bento shop'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you have a JR Pass, activate it today. The Wide View Hida is fully covered and seat reservations are free.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sanmachi Suji (三町筋) — Old Town Walking',
              description: 'Takayama\'s heart is this preserved district of dark-wood merchant houses from the Edo period (1600s-1800s). The three parallel streets are lined with sake breweries (look for sugidama cedar balls hanging outside), craft shops, and small museums. It feels like stepping back 300 years.',
              details: [
                '📍 Sanmachi Suji, Takayama — 10-minute walk from station',
                '🕐 Shops open until ~5pm, streets are beautiful anytime',
                '🍶 Look for sake breweries with blue noren curtains — many offer free tastings',
                '🆓 Free to walk around'
              ]
            },
            {
              title: 'Sake Brewery Tastings',
              description: 'Takayama has 6 sake breweries within walking distance in the old town. In late March, many are finishing their winter brewing season and offer special new sake (shinshu). Funasaka Sake Brewery and Harada Sake Brewery are excellent — try the nama (unpasteurized) sake, only available fresh.',
              details: [
                '📍 Funasaka Brewery: 6-8 Kamininomachi — free tasting of 5+ varieties',
                '📍 Harada Brewery: 10 Kaminannomachi — try their daiginjo',
                '💰 Free tastings at most breweries, bottles ¥800-3,000'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hida Beef Dinner',
              description: 'Hida beef (飛騨牛) is Takayama\'s claim to fame — a wagyu variety rivaling Kobe beef at half the price. Try it as steak, yakiniku (grilled), or on sushi (yes, raw beef sushi). Maruaki is a local favorite with counter seating where you grill your own premium cuts.',
              details: [
                '📍 Maruaki: 1-42 Tenmanmachi — reservations recommended',
                '💰 ¥2,500-4,000 for a Hida beef set',
                '🥩 Try the Hida beef nigiri sushi from street stalls too (~¥600 for 2 pieces)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Maruaki (丸明) or Ajikura Tengoku',
              description: 'Premium Hida beef yakiniku at prices that would be double in Tokyo. The A5-grade sirloin melts on the grill. Pair with local Takayama sake.',
              meta: '💰 ¥2,500-4,000 · Takayama Old Town · Hida Beef Yakiniku'
            }
          ],
          tips: [
            { type: 'tip', text: '🏨 Stay at a traditional ryokan like Sumiyoshi Ryokan (¥8,000-12,000 with breakfast) for the full Takayama experience, or Takayama Ouan hostel (¥3,500) for budget.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.6980, lng: 137.8600, label: 'Hakuba Station', num: 1, cat: 'transport', desc: 'Departure point — JR Oito Line' },
        { lat: 36.2305, lng: 137.9721, label: 'Matsumoto Station', num: 2, cat: 'transport', desc: 'Transfer to Wide View Hida' },
        { lat: 36.1412, lng: 137.2526, label: 'Sanmachi Suji', num: 3, cat: 'culture', desc: 'Edo-period preserved merchant streets' },
        { lat: 36.1398, lng: 137.2540, label: 'Funasaka Sake Brewery', num: 4, cat: 'food', desc: 'Free sake tastings — try the shinshu' },
        { lat: 36.1405, lng: 137.2535, label: 'Maruaki', num: 5, cat: 'food', desc: 'Famous Hida beef yakiniku restaurant' }
      ]
    },

    // ===================== DAY 2 — March 18: Takayama Full Day =====================
    {
      num: 2,
      date: 'March 18',
      neighborhoods: 'Takayama · Higashiyama',
      title: 'Morning Markets, Mountain Temples & Hida Folk Village',
      description: 'A full day in Takayama exploring the famous morning markets, the hilltop Higashiyama temple walk, and the open-air folk village that showcases traditional thatched-roof farmhouses of the Hida region.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Miyagawa Morning Market (宮川朝市)',
              description: 'One of Japan\'s oldest and most charming morning markets, running along the Miyagawa River since the Edo period. Local grandmothers sell pickles, miso paste, handmade crafts, and seasonal mountain vegetables. In March, look for fukinotō (butterbur sprouts) and sansai (mountain wild vegetables) — harbingers of spring.',
              details: [
                '📍 Along Miyagawa River, central Takayama',
                '🕐 7am-12pm daily',
                '🆓 Free to browse',
                '💡 Try the mitarashi dango (sweet soy-glazed rice balls) — Takayama\'s version is uniquely savory, not sweet'
              ]
            },
            {
              title: 'Takayama Jinya (高山陣屋) — Historic Government House',
              description: 'The only surviving Edo-era government office in Japan. This beautifully restored complex shows how Tokugawa-era officials administered the region. The rice storehouses, torture room, and beautiful gardens give a vivid picture of feudal governance.',
              details: [
                '📍 1-5 Hachikenmachi, Takayama',
                '🕐 8:45am-5pm',
                '🎟️ ¥440',
                '💡 The morning market at Jinya-mae (in front of Jinya) is the second morning market — smaller but equally charming'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Morning Market Street Food',
              description: 'Graze through the morning market: mitarashi dango, gohei mochi (walnut-miso rice cake), hot amazake (sweet rice drink), and fresh apple juice from Hida orchards.',
              meta: '💰 ¥500-800 for a full market breakfast'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hida Folk Village (飛騨の里)',
              description: 'An open-air museum showcasing 30+ traditional thatched-roof farmhouses (gassho-zukuri style, similar to Shirakawa-go which you\'ve already seen, but here you can go inside each one and see craft demonstrations). In late March, the last snow may still dust the roofs while spring flowers emerge — a magical transitional moment.',
              details: [
                '📍 1-590 Kamiokamotocho, Takayama — 10-min bus from station',
                '🕐 8:30am-5pm',
                '🎟️ ¥700',
                '🚌 Sarubobo Bus from Takayama Station (¥210, every 20 min)'
              ]
            },
            {
              title: 'Higashiyama Walking Course (東山遊歩道)',
              description: 'A peaceful 3.5km hillside path connecting 13 temples and 5 shrines on Takayama\'s eastern edge. The trail winds through forest and past moss-covered stone walls. In late March, early plum blossoms line the path. It\'s meditative, quiet, and locals-only.',
              details: [
                '📍 Starts near Takayama Station east side',
                '🕐 Allow 1.5-2 hours for the full walk',
                '🆓 Free',
                '💡 Best done in the afternoon light — the temples face west and glow golden'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kyōya (京や) — Hida Soba & Tofu',
              description: 'A cozy soba restaurant near the old town serving handmade buckwheat noodles and Hida-style tofu (grilled with miso). The cold soba with mountain vegetable tempura is perfect.',
              meta: '💰 ¥900-1,400 · Takayama Old Town · Soba & Tofu'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Takayama Night Walk & Izakaya',
              description: 'The old town is magical after dark — lanterns illuminate the wooden buildings and the river reflects the lights. End the night at a local izakaya for Hida pork skewers, mountain vegetable tempura, and one last round of Takayama sake.',
              details: [
                '📍 Sanmachi Suji area after dark',
                '💡 Ebisu Honten izakaya near the station is local and lively'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ebisu Honten (ゑびす本店)',
              description: 'Local izakaya with a lively atmosphere. Try the hoba miso — a Takayama specialty where miso paste, green onions, mushrooms, and Hida beef are grilled on a magnolia leaf over a charcoal flame at your table.',
              meta: '💰 ¥1,500-2,500 · Near Takayama Station · Izakaya'
            }
          ],
          tips: [
            { type: 'tip', text: '♨️ Many ryokan have their own onsen — soak before bed. If staying at a hotel, try Hida Takayama Onsen (public bath near the station, ¥600).' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1430, lng: 137.2550, label: 'Miyagawa Morning Market', num: 1, cat: 'food', desc: 'Edo-period riverside morning market' },
        { lat: 36.1395, lng: 137.2560, label: 'Takayama Jinya', num: 2, cat: 'culture', desc: 'Only surviving Edo-era government office' },
        { lat: 36.1540, lng: 137.2380, label: 'Hida Folk Village', num: 3, cat: 'culture', desc: 'Open-air museum with thatched-roof houses' },
        { lat: 36.1460, lng: 137.2640, label: 'Higashiyama Walk Start', num: 4, cat: 'nature', desc: '3.5km temple and shrine hillside path' },
        { lat: 36.1415, lng: 137.2525, label: 'Ebisu Honten', num: 5, cat: 'food', desc: 'Local izakaya — try the hoba miso' }
      ]
    },

    // ===================== DAY 3 — March 19: Takayama → Kyoto =====================
    {
      num: 3,
      date: 'March 19',
      neighborhoods: 'Takayama · Kyoto · Higashiyama',
      title: 'Into the Ancient Capital: Takayama to Kyoto',
      description: 'Travel from the mountains to Japan\'s cultural heart. Arrive in Kyoto and spend the afternoon exploring the atmospheric Higashiyama district — Kyoto\'s most beautiful neighborhood of temples, tea houses, and geisha streets.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Takayama → Kyoto by Train',
              description: 'Take the JR Wide View Hida from Takayama to Nagoya (~2.5 hours), then transfer to the Tokaido Shinkansen to Kyoto (~35 minutes). Use takkyubin luggage forwarding to send your big bag directly to your Kyoto hotel (arrange at hotel front desk or 7-Eleven the night before, ¥2,000) so you travel light.',
              details: [
                '🚂 Takayama → Nagoya: JR Wide View Hida (~2.5h) — covered by JR Pass',
                '🚂 Nagoya → Kyoto: Tokaido Shinkansen Hikari (~35min) — covered by JR Pass',
                '⏰ Depart Takayama ~8:30am, arrive Kyoto ~12pm',
                '💡 Forward your luggage via takkyubin — travel with just a daypack'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nishiki Market (錦市場)',
              description: 'Kyoto\'s 400-year-old "Kitchen of Kyoto." A narrow 5-block covered arcade with 130+ vendors selling Kyoto specialties: dashimaki tamago (rolled omelet), tsukemono (pickled vegetables), yuba (tofu skin), and fresh matcha treats. This is your introduction to Kyoto cuisine.',
              meta: '💰 ¥1,000-2,000 grazing · Nishiki-dori, Nakagyō-ku'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Buy an IC card at Kyoto Station for buses. Kyoto buses are the main way to get around — ¥230 flat fare. Consider a bus day pass (¥700) if you\'ll take 4+ rides.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kiyomizu-dera (清水寺) at Golden Hour',
              description: 'One of Kyoto\'s most iconic temples, perched on a hillside with a massive wooden stage jutting out over the valley. In late March, the cherry trees around the temple begin to bloom — the combination of the wooden stage, city panorama, and pink blossoms is unforgettable. Come in late afternoon for golden light and fewer crowds.',
              details: [
                '📍 1-294 Kiyomizu, Higashiyama-ku',
                '🕐 6am-6pm (extended hours during cherry blossom season, often until 9pm with illumination)',
                '🎟️ ¥400',
                '🌸 Check if nighttime illumination has started — Kiyomizu-dera\'s cherry blossom night viewing is magical'
              ]
            },
            {
              title: 'Ninenzaka & Sannenzaka (二年坂・三年坂)',
              description: 'The photogenic stone-paved lanes leading down from Kiyomizu-dera are lined with traditional wooden machiya houses converted into tea shops, pottery stores, and sweet shops. Walk slowly — there\'s a beautiful detail around every corner. Look for the hidden Starbucks inside a 100-year-old machiya.',
              details: [
                '📍 Between Kiyomizu-dera and Yasaka Pagoda',
                '🆓 Free to walk',
                '💡 Late afternoon is less crowded than morning. The Starbucks at Ninenzaka is in a tatami-mat machiya — worth peeking in even if you don\'t buy coffee'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion District Evening Walk',
              description: 'Kyoto\'s famous geisha district comes alive at dusk. Walk along Hanamikoji-dori and the canal-lined Shirakawa area to see beautifully preserved ochaya (tea houses) with their distinctive bamboo screens and paper lanterns. If you\'re lucky, you may spot a maiko (apprentice geisha) heading to an evening engagement.',
              details: [
                '📍 Hanamikoji-dori, Gion, Higashiyama-ku',
                '🕐 Best at dusk (5:30-7pm)',
                '🆓 Free to walk',
                '⚠️ Do not photograph geiko/maiko without permission — it\'s considered very rude'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pontocho Alley (先斗町)',
              description: 'A narrow alley along the Kamo River packed with restaurants. In spring, many have yuka (outdoor terraces) over the river. Try obanzai — Kyoto\'s style of home cooking with many small seasonal dishes. Mame-hana or Kappa Sushi are good affordable options.',
              meta: '💰 ¥1,500-3,000 · Pontocho, Nakagyō-ku · Kyoto obanzai & kaiseki'
            }
          ],
          tips: [
            { type: 'tip', text: '🏨 Stay in the Higashiyama or Gion area for the most atmospheric experience. Piece Hostel Kyoto (¥3,500) or Hotel Mystays Shijo (¥6,000) are good moderate options.' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1412, lng: 137.2526, label: 'Takayama Station', num: 1, cat: 'transport', desc: 'Departure — JR Wide View Hida to Nagoya' },
        { lat: 35.0050, lng: 135.7631, label: 'Nishiki Market', num: 2, cat: 'food', desc: 'Kyoto\'s 400-year-old covered food market' },
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 3, cat: 'sight', desc: 'Iconic hillside temple with wooden stage' },
        { lat: 34.9980, lng: 135.7800, label: 'Ninenzaka & Sannenzaka', num: 4, cat: 'culture', desc: 'Stone-paved lanes with traditional shops' },
        { lat: 35.0037, lng: 135.7750, label: 'Gion District', num: 5, cat: 'culture', desc: 'Geisha district — evening walk' },
        { lat: 35.0060, lng: 135.7700, label: 'Pontocho Alley', num: 6, cat: 'food', desc: 'Narrow riverside restaurant alley' }
      ]
    },

    // ===================== DAY 4 — March 20: Kyoto Full Day =====================
    {
      num: 4,
      date: 'March 20',
      neighborhoods: 'Arashiyama · Kinugasa · Fushimi',
      title: 'Bamboo, Gold & Ten Thousand Torii Gates',
      description: 'Today covers Kyoto\'s western and southern highlights: the ethereal Arashiyama bamboo grove, the iconic Golden Pavilion, and the mesmerizing tunnel of vermillion torii gates at Fushimi Inari. March 20 is also Shunbun no Hi (Spring Equinox Day) — a national holiday celebrating the arrival of spring.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove (嵐山竹林)',
              description: 'Arrive early (before 8am) to experience the famous bamboo forest in relative solitude. The towering stalks create a natural cathedral, with light filtering through in shafts. In late March, the bamboo is lush green against the first cherry blossoms along the Katsura River — a stunning contrast.',
              details: [
                '📍 Arashiyama, Ukyō-ku — JR Saga-Arashiyama Station (15 min from Kyoto Station)',
                '🕐 Always open · Best before 8:30am',
                '🆓 Free',
                '💡 Continue through the grove to Ōkōchi Sansō Villa (¥1,000, includes matcha) — stunning hilltop garden with views of Kyoto'
              ]
            },
            {
              title: 'Tenryū-ji Temple & Garden (天龍寺)',
              description: 'A UNESCO World Heritage Zen temple at the base of the bamboo grove. The garden is one of Japan\'s finest — designed in the 14th century with Mt. Arashiyama as borrowed scenery. Early cherry blossoms frame the pond garden beautifully.',
              details: [
                '📍 68 Susukinobabachō, Saga Tenryūji, Ukyō-ku',
                '🕐 8:30am-5pm',
                '🎟️ ¥500 garden, +¥300 for the main hall'
              ]
            },
            {
              title: 'Togetsukyo Bridge & River Walk',
              description: 'The iconic "Moon Crossing Bridge" over the Katsura River is Arashiyama\'s symbol. Walk along the riverside where cherry trees line both banks. In late March, you\'ll see the first blooms opening against the mountain backdrop.',
              details: [
                '📍 Togetsukyo Bridge, Arashiyama',
                '🆓 Free',
                '🌸 The riverside cherry trees are some of Kyoto\'s earliest to bloom'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast/Brunch',
              name: '% Arabica Arashiyama',
              description: 'World-famous specialty coffee roaster with a tiny shop right on the Katsura River. Perfect espresso with a mountain view. Grab a coffee before hitting the bamboo grove.',
              meta: '💰 ¥400-600 · Arashiyama riverside'
            }
          ],
          tips: [
            { type: 'tip', text: '🎌 March 20 is Shunbun no Hi (Spring Equinox) — a national holiday. Temples may be busier than usual, but the festive atmosphere adds energy. Arrive at Arashiyama by 8am to beat holiday crowds.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kinkaku-ji — The Golden Pavilion (金閣寺)',
              description: 'Kyoto\'s most famous image: a three-story pavilion covered in real gold leaf, reflected perfectly in the mirror pond. The garden is designed so that the approach gradually reveals the pavilion. In late March, scattered cherry blossoms add pink accents to the gold — a uniquely spring scene.',
              details: [
                '📍 1 Kinkakujichō, Kita-ku',
                '🕐 9am-5pm',
                '🎟️ ¥500 (the ticket is a beautiful calligraphy charm — keep it!)',
                '🚌 Bus 205 from Arashiyama area'
              ]
            },
            {
              title: 'Ryōan-ji — Zen Rock Garden (龍安寺)',
              description: 'Just a 15-minute walk from Kinkaku-ji, this temple houses Japan\'s most famous Zen garden — 15 rocks on raked white gravel, positioned so that you can never see all 15 from any single angle. Sit on the wooden veranda and let the garden\'s mystery wash over you.',
              details: [
                '📍 13 Ryōanji Goryōnoshitachō, Ukyō-ku',
                '🕐 8am-5pm',
                '🎟️ ¥500',
                '💡 The temple grounds also have a beautiful pond garden with early cherry blossoms'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Tofu Cuisine at Yudofu Sagano (嵯峨野)',
              description: 'Arashiyama is famous for yudofu — silky tofu simmered in kombu broth, a Kyoto specialty. Sagano serves it in a traditional setting with garden views. Light, seasonal, and very Kyoto.',
              meta: '💰 ¥1,200-2,000 · Arashiyama · Tofu kaiseki'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Fushimi Inari Taisha (伏見稲荷大社) at Sunset',
              description: 'Japan\'s most visited shrine, famous for its seemingly endless tunnel of 10,000+ vermillion torii gates winding up Mt. Inari. Coming at sunset means the gates glow in golden-red light and the crowds thin dramatically after dark. The full hike to the summit takes 2-3 hours, but even walking 30 minutes up gives you the iconic gate-tunnel photos.',
              details: [
                '📍 68 Fukakusa Yabunouchichō, Fushimi-ku — JR Inari Station (5 min from Kyoto Station)',
                '🕐 24 hours (the shrine never closes!)',
                '🆓 Free',
                '🌸 The approach has cherry trees that may be opening — torii + sakura is an incredible combo',
                '💡 Walk at least to the Yotsutsuji intersection (halfway up) for panoramic Kyoto sunset views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Vermillion Café (near Fushimi Inari) or Kyoto Station Ramen Street',
              description: 'Vermillion is a charming café/restaurant right at Fushimi Inari\'s entrance with good rice bowls and matcha. Or head back to Kyoto Station where the underground Ramen Koji has 9 regional ramen shops — try a rich tonkotsu or Kyoto-style light shoyu ramen.',
              meta: '💰 ¥800-1,200 · Fushimi or Kyoto Station'
            }
          ],
          tips: [
            { type: 'tip', text: '⛩️ The Fushimi Inari experience transforms after dark — fewer people, more mystical atmosphere, and some gates are subtly lit. Bring a phone flashlight for the upper trails.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0094, lng: 135.6761, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'nature', desc: 'Towering bamboo forest — arrive before 8am' },
        { lat: 35.0158, lng: 135.6748, label: 'Tenryū-ji Temple', num: 2, cat: 'culture', desc: 'UNESCO Zen temple with stunning garden' },
        { lat: 35.0114, lng: 135.6779, label: 'Togetsukyo Bridge', num: 3, cat: 'sight', desc: 'Iconic Moon Crossing Bridge over Katsura River' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 4, cat: 'sight', desc: 'Gold-leaf pavilion on mirror pond' },
        { lat: 35.0345, lng: 135.7184, label: 'Ryōan-ji', num: 5, cat: 'culture', desc: 'Japan\'s most famous Zen rock garden' },
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 6, cat: 'sight', desc: '10,000 vermillion torii gates up the mountain' }
      ]
    },

    // ===================== DAY 5 — March 21: Kyoto Cherry Blossom Day =====================
    {
      num: 5,
      date: 'March 21',
      neighborhoods: 'Philosopher\'s Path · Maruyama · Higashiyama',
      title: 'Sakura Kyoto: Philosopher\'s Path, Maruyama Park & Temple Gardens',
      description: 'Today is dedicated to Kyoto\'s most famous cherry blossom spots. The first blooms should be appearing now — you\'re here at the magical moment when the buds open. This is also the time of Hanatōro, Kyoto\'s spring illumination festival with lantern-lit paths.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Philosopher\'s Path (哲学の道)',
              description: 'A 2km canal-side path lined with hundreds of cherry trees, connecting Ginkaku-ji to Nanzen-ji. Named after philosopher Nishida Kitaro who walked here daily in meditation. In late March, the first sakura blossoms appear along the canal — scattered petals floating on the water. Early morning is magical and uncrowded.',
              details: [
                '📍 Starts near Ginkaku-ji, ends near Nanzen-ji, Sakyō-ku',
                '🕐 Always open · Best before 9am',
                '🆓 Free',
                '🌸 Even before full bloom, the early blossoms over the canal are enchanting',
                '💡 Walk south (Ginkaku-ji → Nanzen-ji) to end at Nanzen-ji\'s spectacular aqueduct'
              ]
            },
            {
              title: 'Nanzen-ji Temple & Suirokaku Aqueduct (南禅寺)',
              description: 'A grand Zen temple complex with a dramatic Meiji-era brick aqueduct running through it — one of Kyoto\'s most photogenic spots. The cherry trees around the aqueduct arches create a surreal blend of old and older. The temple\'s rock garden and hilltop viewpoint are also worth exploring.',
              details: [
                '📍 Nanzenji Fukuchichō, Sakyō-ku',
                '🕐 8:40am-5pm',
                '🎟️ ¥600 for the main hall, aqueduct is free',
                '📸 The brick aqueduct with cherry blossoms is one of Kyoto\'s most Instagrammed spots'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Yojiya Café (Ginkaku-ji branch)',
              description: 'Famous Kyoto cosmetics brand that runs charming cafés. Their matcha latte comes with a latte-art face drawn in the foam — Kyoto\'s most photogenic breakfast. Pair with a warabi mochi set.',
              meta: '💰 ¥800-1,200 · Near Ginkaku-ji · Matcha & sweets'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Maruyama Park (円山公園) — Kyoto\'s Sakura Gathering Place',
              description: 'Kyoto\'s most famous hanami (cherry blossom viewing) park, centered around a magnificent weeping cherry tree (shidarezakura) that is lit up at night. Even in early bloom, locals gather here with picnic blankets and sake. The atmosphere is festive and joyful — this is where Kyoto celebrates spring.',
              details: [
                '📍 Maruyama Park, Higashiyama-ku — adjacent to Yasaka Shrine',
                '🕐 24 hours · Illumination at night during bloom season',
                '🆓 Free',
                '🌸 The famous shidarezakura (weeping cherry) is an early bloomer — it may already be showing color!',
                '💡 Grab drinks from the yatai (food stalls) that pop up during sakura season'
              ]
            },
            {
              title: 'Yasaka Shrine & Chion-in Temple',
              description: 'Yasaka Shrine sits at the entrance to Maruyama Park — walk through its iconic vermillion gate. Then continue to Chion-in, one of Kyoto\'s most powerful temples with the largest temple gate in Japan (sanmon, 24m tall). The temple grounds have beautiful cherry trees and a peaceful back garden.',
              details: [
                '📍 Yasaka Shrine: 625 Gionmachi, Higashiyama-ku',
                '📍 Chion-in: 400 Rinkachō, Higashiyama-ku',
                '🆓 Yasaka Shrine free · Chion-in garden ¥500',
                '💡 Chion-in\'s massive sanmon gate is lit up during cherry blossom season'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Omen (おめん) — Udon Noodles',
              description: 'A beloved Kyoto udon institution near the Philosopher\'s Path. Their signature dish is cold udon served with a basket of fresh seasonal vegetables and a rich dipping broth. Simple, seasonal, perfect.',
              meta: '💰 ¥1,000-1,500 · Near Ginkaku-ji · Kyoto udon'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Higashiyama Hanatōro (東山花灯路) — Spring Lantern Festival',
              description: 'If the timing aligns (check dates — it\'s usually mid-March), thousands of lanterns illuminate the stone paths of Higashiyama from Shōren-in to Kiyomizu-dera. The combination of lantern light, emerging cherry blossoms, and ancient temples is pure magic. Even if the official festival has ended, many temples offer their own nighttime illuminations during sakura season.',
              details: [
                '📍 Higashiyama area — Shōren-in to Kiyomizu-dera',
                '🕐 6pm-9:30pm',
                '🆓 Free (individual temple illuminations may charge separately)',
                '💡 If Hanatōro has ended, check for individual temple nighttime specials — Kiyomizu-dera and Kodai-ji often have their own sakura illuminations'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa Restaurant (祇園キャッパ)',
              description: 'A hidden gem in Gion serving creative Kyoto-Italian fusion with seasonal Japanese ingredients. The prix fixe dinner uses Kyoto vegetables, Kyoto beef, and spring ingredients like bamboo shoots (takenoko) that are just coming into season.',
              meta: '💰 ¥2,000-3,500 · Gion · Kyoto-Italian fusion'
            }
          ],
          tips: [
            { type: 'tip', text: '🌸 Download the "Sakura Navi" app or check sakura.weathermap.jp for real-time bloom updates across Kyoto. Different spots bloom at different times — early sites to check: Tō-ji Temple, Maruyama Park weeping cherry, and the Imperial Palace grounds.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0270, lng: 135.7983, label: 'Philosopher\'s Path (north end)', num: 1, cat: 'nature', desc: 'Cherry-lined canal walk — 2km of sakura' },
        { lat: 35.0112, lng: 135.7931, label: 'Nanzen-ji Temple', num: 2, cat: 'culture', desc: 'Zen temple with Meiji-era brick aqueduct' },
        { lat: 35.0035, lng: 135.7812, label: 'Maruyama Park', num: 3, cat: 'nature', desc: 'Kyoto\'s #1 hanami spot — weeping cherry tree' },
        { lat: 35.0036, lng: 135.7786, label: 'Yasaka Shrine', num: 4, cat: 'culture', desc: 'Iconic vermillion shrine at Gion entrance' },
        { lat: 35.0072, lng: 135.7830, label: 'Chion-in Temple', num: 5, cat: 'culture', desc: 'Largest temple gate in Japan' },
        { lat: 34.9997, lng: 135.7799, label: 'Gion Kappa', num: 6, cat: 'food', desc: 'Kyoto-Italian fusion dinner' }
      ]
    },

    // ===================== DAY 6 — March 22: Day Trip to Nara =====================
    {
      num: 6,
      date: 'March 22',
      neighborhoods: 'Nara Park · Naramachi · Kasuga Taisha',
      title: 'Deer, Giant Buddhas & Spring Blossoms: Nara Day Trip',
      description: 'A day trip to Nara — Japan\'s first permanent capital (710 AD) and home to 1,200 free-roaming deer, the world\'s largest bronze Buddha, and ancient shrine forests. In late March, the park\'s cherry trees are beginning to bloom, and the deer wandering beneath pink petals is one of Japan\'s most iconic spring images.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kyoto → Nara (35 minutes by train)',
              description: 'Take the JR Nara Line from Kyoto Station to JR Nara Station (45 min, covered by JR Pass) or the faster Kintetsu Limited Express from Kintetsu Kyoto Station (35 min, ¥640). The Kintetsu drops you closer to Nara Park.',
              details: [
                '🚂 JR Nara Line: 45 min, covered by JR Pass',
                '🚂 Kintetsu: 35 min, ¥640, closer to sights',
                '⏰ Depart by 8:30am to maximize your day'
              ]
            },
            {
              title: 'Nara Park & the Friendly Deer (奈良公園)',
              description: 'As soon as you enter the park, you\'ll be greeted by hundreds of Sika deer who bow for shika senbei (deer crackers, ¥200). These deer are considered divine messengers of the Kasuga Shrine and have roamed freely for over 1,000 years. In late March, cherry blossoms frame the meadows where deer rest — pure postcard Japan.',
              details: [
                '📍 Nara Park — 15-minute walk from either station',
                '🕐 24 hours · Best in morning light',
                '🆓 Free (deer crackers ¥200)',
                '📸 Pro tip: bow to the deer and they\'ll bow back before you offer a cracker',
                '⚠️ They can be pushy! Hold crackers behind your back and distribute slowly'
              ]
            },
            {
              title: 'Tōdai-ji Temple & the Great Buddha (東大寺)',
              description: 'The world\'s largest wooden building houses a 15-meter-tall bronze Buddha (Daibutsu) cast in 752 AD. The scale is overwhelming — the Buddha\'s hand alone is 2.5 meters long. The temple\'s Nandaimon gate features two fierce 8-meter guardian statues carved by the master sculptor Unkei.',
              details: [
                '📍 406-1 Zōshichō, Nara',
                '🕐 8am-5pm (March)',
                '🎟️ ¥600',
                '💡 Try squeezing through the pillar hole in the Great Buddha Hall — it\'s said to be the same size as the Buddha\'s nostril and grants enlightenment!'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Café at Kyoto Station or on the train',
              description: 'Grab a quick breakfast at one of Kyoto Station\'s many bakeries (Sizuya is a Kyoto institution with their famous karashi-mentai France bread) before heading to Nara.',
              meta: '💰 ¥300-600 · Kyoto Station'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine (春日大社)',
              description: 'An ancient Shinto shrine famous for its 3,000 stone and bronze lanterns, many covered in moss and hundreds of years old. The approach through a primeval forest with deer appearing between ancient trees is magical. In February and August, all 3,000 lanterns are lit — but even now, the atmosphere is mystical.',
              details: [
                '📍 160 Kasuganocho, Nara',
                '🕐 7:30am-5:30pm',
                '🎟️ ¥500 for inner sanctuary',
                '🌸 The wisteria garden (fuji-no-sono) is not yet in bloom, but the cherry trees along the approach are'
              ]
            },
            {
              title: 'Naramachi (ならまち) — Old Merchant Quarter',
              description: 'The traditional merchant district with narrow streets of converted machiya (wooden townhouses) now housing craft shops, cafés, and small museums. It\'s quieter and more authentic than Kyoto\'s tourist streets. Look for the red monkey charms (migawari-zaru) hanging from houses — protective talismans.',
              details: [
                '📍 Naramachi district, south of Sarusawa Pond',
                '🕐 Most shops 10am-5pm',
                '🆓 Free to walk, small museum entries ¥200-300',
                '☕ Café Kotodama serves excellent pour-over coffee in a renovated machiya'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kakinoha Sushi at Tanaka (柿の葉すし)',
              description: 'Nara\'s signature dish: pressed sushi wrapped in persimmon leaves, which impart a subtle fragrance. Tanaka near Kintetsu Nara Station has been making them for decades. Try the mackerel and salmon varieties.',
              meta: '💰 ¥800-1,200 · Near Kintetsu Nara Station · Nara specialty'
            }
          ],
          tips: [
            { type: 'tip', text: '🍡 Try Nakatanidou\'s famous mochi pounding show near Kintetsu Nara Station — the mochi master pounds at incredible speed, and the fresh yomogi (mugwort) mochi is ¥130 each and unforgettable.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto & Kyoto Tower Night View',
              description: 'Head back to Kyoto and catch the city from above at Kyoto Tower\'s observation deck. At night, you can see the city\'s temple-studded landscape stretching to the mountains. Or simply stroll through the illuminated Kamo River area.',
              details: [
                '🚂 Nara → Kyoto: JR or Kintetsu, 35-45 min',
                '📍 Kyoto Tower: Karasuma-dori, right at Kyoto Station',
                '🎟️ ¥900 observation deck',
                '🕐 Until 9pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kyoto Station Underground — Ramen Koji or Eat Paradise',
              description: 'Kyoto Station has two excellent food floors. Ramen Koji on the 10th floor has branches of Japan\'s best ramen chains. For variety, Eat Paradise in the Cube building has everything from tonkatsu to tempura to Kyoto-style sushi.',
              meta: '💰 ¥800-1,500 · Kyoto Station · Various'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you\'re not tired, the Kamo River banks between Shijō and Sanjō are beautiful for an evening walk — many locals jog or sit along the river at sunset.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'nature', desc: '1,200 free-roaming sacred deer' },
        { lat: 34.6890, lng: 135.8398, label: 'Tōdai-ji Temple', num: 2, cat: 'sight', desc: 'World\'s largest wooden building & Great Buddha' },
        { lat: 34.6811, lng: 135.8498, label: 'Kasuga Taisha', num: 3, cat: 'culture', desc: '3,000 stone and bronze lanterns in ancient forest' },
        { lat: 34.6788, lng: 135.8272, label: 'Naramachi', num: 4, cat: 'culture', desc: 'Traditional merchant quarter with craft shops' },
        { lat: 34.6818, lng: 135.8200, label: 'Tanaka Kakinoha Sushi', num: 5, cat: 'food', desc: 'Nara\'s signature persimmon-leaf pressed sushi' },
        { lat: 34.6878, lng: 135.8118, label: 'Nakatanidou Mochi', num: 6, cat: 'food', desc: 'Famous high-speed mochi pounding show' }
      ]
    },

    // ===================== DAY 7 — March 23: Yoshino — Japan's Best Cherry Blossoms =====================
    {
      num: 7,
      date: 'March 23',
      neighborhoods: 'Yoshino · Shimosenbon · Nakasenbon',
      title: 'Mount Yoshino: Japan\'s Most Sacred Cherry Blossom Mountain',
      description: 'Today you visit Japan\'s single most famous cherry blossom destination — Mount Yoshino in Nara Prefecture, where 30,000 cherry trees cover an entire mountainside in waves of pink and white. The trees bloom in stages from bottom to top over several weeks. In late March, the lower groves (Shimosenbon) should be in early bloom. This is a UNESCO World Heritage site and a sacred mountain for over 1,300 years.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kyoto → Yoshino by Train',
              description: 'Take the Kintetsu Limited Express from Kyoto to Yoshino (~1 hour 45 minutes, with a transfer at Kashiharajingū-mae). The train winds through the Nara countryside, passing ancient burial mounds and rice paddies. Yoshino Station sits at the base of the mountain.',
              details: [
                '🚂 Kintetsu from Kyoto → Kashiharajingū-mae → Yoshino (~1h45, ¥1,600)',
                '⏰ Depart Kyoto by 7:30am to arrive ~9:15am',
                '💡 This route is NOT covered by JR Pass — buy Kintetsu tickets separately',
                '🚡 From Yoshino Station, a ropeway/cable car goes up to Shimosenbon (¥450 one-way, 3 min) — or walk up (20 min)'
              ]
            },
            {
              title: 'Shimosenbon (下千本) — Lower Cherry Groves',
              description: 'The lowest of Yoshino\'s four cherry blossom zones, and the first to bloom. "Senbon" means "1,000 trees" and there are literally thousands of Yoshino cherry trees (shirayama-zakura, the mountain cherry variety) covering the slopes. These are the trees that gave the "Yoshino cherry" its name — this is where sakura culture began.',
              details: [
                '📍 Shimosenbon area, lower Mt. Yoshino',
                '🆓 Free',
                '🌸 Late March = early bloom here. You may see 1-3 bud (ichirin-sanrin) stage — the exciting moment of first opening',
                '💡 The Shimosenbon viewpoint near the ropeway station offers panoramic views of the cherry groves below'
              ]
            },
            {
              title: 'Kinpusen-ji Temple (金峯山寺) — Zaōdō Hall',
              description: 'The spiritual heart of Yoshino and one of Japan\'s most important mountain temples. The massive Zaōdō Hall (National Treasure, second-largest wooden building in Japan after Tōdai-ji) houses three fierce blue-skinned Zaō Gongen statues — secret Buddhist images rarely shown to the public. During cherry blossom season, a special viewing (hibutsu gokaicho) is held.',
              details: [
                '📍 Yoshinoyama, Yoshino — central Nakasenbon area',
                '🕐 8:30am-4:30pm',
                '🎟️ ¥800 (¥1,600 during special hibutsu viewing)',
                '🌸 The cherry blossom season special viewing of the secret Zaō Gongen statues runs March 28-May 7 — you might just miss it, but the temple is magnificent regardless'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Early breakfast at hotel/konbini before departure',
              description: 'Grab onigiri and coffee from a konbini near Kyoto Station. You\'ll want to be on an early train.',
              meta: '💰 ¥300-500 · Konbini'
            }
          ],
          tips: [
            { type: 'tip', text: '🥾 Yoshino involves uphill walking. Wear comfortable shoes with good grip. The mountain path from Shimosenbon to Nakasenbon is about 2km uphill — steep in places but well-paved.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakasenbon (中千本) — Middle Cherry Groves & Viewpoints',
              description: 'Continue uphill to the middle zone, where even more cherry trees spread across the mountainside. The famous "Yoshimizu Shrine Viewpoint" here is where Toyotomi Hideyoshi (Japan\'s great unifier) held a legendary cherry blossom viewing party in 1594 with 5,000 guests. The same view is there for you today — the entire mountainside cascading with cherry trees.',
              details: [
                '📍 Nakasenbon area — 20-min walk uphill from Kinpusen-ji',
                '📸 Yoshimizu Shrine viewpoint (¥200) for the famous panoramic shot',
                '💡 If you have energy, continue to Kamisenbon (upper groves) — less crowded, wilder, more sacred',
                '🌸 Nakasenbon blooms about a week after Shimosenbon — you may see buds just ready to pop'
              ]
            },
            {
              title: 'Yoshino Mountain Street Food & Tea Houses',
              description: 'The walking path along Yoshino\'s ridge is lined with shops selling seasonal treats: sakura mochi (pink rice cake wrapped in cherry leaf), kuzukiri (kuzu starch noodles — a Yoshino specialty), roasted chestnut mochi, and sakura soft serve ice cream. Stop at a tea house for matcha with a mountain view.',
              details: [
                '🍡 Try kuzu sweets — Yoshino is Japan\'s most famous source of kuzu (arrowroot starch)',
                '🍵 Hana Yagura tea house has panoramic views with matcha service',
                '💰 Snacks ¥200-500, matcha set ¥600-800'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Yoshino Mountain Restaurant — Shimizuya or Hōrinden',
              description: 'Simple mountain food at its best. Try the kaki-no-ha sushi (persimmon leaf sushi, same as Nara\'s but this is where it originated), mountain vegetable tempura, and warm udon with wild mushrooms.',
              meta: '💰 ¥1,000-1,500 · Nakasenbon area · Mountain cuisine'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto or Continue to Osaka',
              description: 'Take the Kintetsu back from Yoshino. If continuing to Osaka tomorrow, you could head there tonight (~1h45 via Kintetsu with transfer at Kashiharajingū-mae to Osaka-Abenobashi). Or return to Kyoto (same route, ~1h45) for one more night.',
              details: [
                '🚂 Yoshino → Kyoto: Kintetsu ~1h45, ¥1,600',
                '🚂 Yoshino → Osaka-Abenobashi: Kintetsu ~1h45, ¥1,000',
                '💡 If moving to Osaka tonight, your first Osaka hotel should be in Namba or Shinsaibashi area for tomorrow\'s food crawl'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'If arriving in Osaka: Dōtonbori First Night',
              description: 'If you\'ve moved to Osaka, head straight to Dōtonbori for your first hit of Osaka street food: takoyaki (octopus balls) from Wanaka, kushikatsu (deep-fried skewers) from Daruma, and the neon-lit canal atmosphere. If staying in Kyoto, revisit your favorite Pontocho spot.',
              meta: '💰 ¥1,000-2,000 · Dōtonbori or Kyoto'
            }
          ],
          tips: [
            { type: 'tip', text: '🌸 Yoshino\'s cherry blossoms bloom in 4 stages: Shimosenbon (late March) → Nakasenbon (early April) → Kamisenbon (mid-April) → Okusenbon (late April). You\'re catching the exciting first act!' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.3772, lng: 135.8578, label: 'Yoshino Station', num: 1, cat: 'transport', desc: 'Base of Mt. Yoshino — ropeway to Shimosenbon' },
        { lat: 34.3700, lng: 135.8560, label: 'Shimosenbon', num: 2, cat: 'nature', desc: 'Lower cherry groves — first to bloom' },
        { lat: 34.3685, lng: 135.8523, label: 'Kinpusen-ji Temple', num: 3, cat: 'culture', desc: 'Sacred mountain temple with massive Zaōdō Hall' },
        { lat: 34.3648, lng: 135.8494, label: 'Nakasenbon Viewpoint', num: 4, cat: 'nature', desc: 'Hideyoshi\'s famous cherry blossom view' },
        { lat: 34.3640, lng: 135.8480, label: 'Yoshimizu Shrine', num: 5, cat: 'sight', desc: 'Panoramic viewpoint over cherry-covered mountain' },
        { lat: 34.3660, lng: 135.8510, label: 'Hana Yagura Tea House', num: 6, cat: 'food', desc: 'Matcha with mountain panorama views' }
      ]
    },

    // ===================== DAY 8 — March 24: Osaka =====================
    {
      num: 8,
      date: 'March 24',
      neighborhoods: 'Osaka Castle · Shinsekai · Dōtonbori · Namba',
      title: 'Osaka: Castle Sakura, Street Food & Neon Nights',
      description: 'A full day in Japan\'s "Kitchen" — Osaka is the country\'s street food capital and has a brash, friendly energy that\'s the perfect counterpoint to refined Kyoto. Osaka Castle Park is one of the best cherry blossom spots in the Kansai region, and the food scene is legendary.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle Park Cherry Blossoms (大阪城公園)',
              description: 'Osaka Castle Park has over 3,000 cherry trees across a vast park surrounding the castle. The Nishinomaru Garden (¥350) is the premium sakura viewing spot — cherry trees framing the castle tower with the city skyline behind. In late March, the earliest varieties will be blooming and the park buzzes with hanami anticipation.',
              details: [
                '📍 1-1 Ōsakajō, Chūō-ku — Ōsakajōkōen Station or Tanimachi 4-chome Station',
                '🕐 Castle 9am-5pm · Park 24 hours',
                '🎟️ Castle tower ¥600 · Nishinomaru Garden ¥350',
                '🌸 Even before full bloom, the early buds and festive atmosphere make this worthwhile',
                '💡 The park is enormous — allow 2-3 hours to explore the moat, garden, and castle tower'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'Morning at Kuromon Market (黒門市場)',
              description: 'Osaka\'s "Kitchen" — a covered market with 170+ stalls. Eat your way through: fresh sashimi, grilled seafood on sticks, tamago (egg) on a stick, and seasonal fruits. It\'s touristy but the quality is genuine.',
              meta: '💰 ¥1,500-2,500 for a full graze · Nipponbashi area'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Osaka has a different vibe from Kyoto — it\'s louder, funnier, and food-obsessed. The saying goes: Kyoto people spend on clothes, Osaka people spend on food (京の着倒れ、大阪の食い倒れ / Kyo no kidaore, Osaka no kuidaore).' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai (新世界) — Retro Osaka',
              description: 'A delightfully retro neighborhood built in 1912 as "New World" — meant to combine Paris and New York. It\'s now a wonderfully kitschy area of neon signs, Tsūtenkaku Tower, and the best kushikatsu (deep-fried skewers) in Osaka. The street life here feels like stepping into a 1960s Japanese film.',
              details: [
                '📍 Shinsekai, Naniwa-ku — Dobutsuen-mae Station',
                '🗼 Tsūtenkaku Tower: ¥900 for observation deck',
                '💡 Rub the feet of Billiken (the "God of Things as They Ought to Be") at Tsūtenkaku for good luck'
              ]
            },
            {
              title: 'Kushikatsu Lunch at Daruma (串カツだるま)',
              description: 'Osaka\'s most famous kushikatsu chain, but the Shinsekai original is special. Choose from dozens of skewers: lotus root, quail egg, shrimp, asparagus, pork — all battered and deep-fried to golden perfection. The cardinal rule: NEVER double-dip in the communal sauce!',
              details: [
                '📍 2-3-9 Ebisuhigashi, Naniwa-ku',
                '💰 ¥100-200 per skewer, a full meal runs ¥1,000-1,800',
                '⚠️ Sosu nidozuke kinshi! (No double dipping!) — use the cabbage leaf to scoop extra sauce instead'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kushikatsu Daruma — Shinsekai Original',
              description: 'The original location of Osaka\'s most iconic kushikatsu. Sit at the counter and order skewer by skewer. Don\'t miss the renkon (lotus root) and the mochi.',
              meta: '💰 ¥1,000-1,800 · Shinsekai · Deep-fried skewers'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dōtonbori (道頓堀) — Osaka\'s Neon Food Paradise',
              description: 'The beating heart of Osaka nightlife and street food. Walk along the canal under massive neon signs (the Glico Running Man, the giant crab, the mechanized gyōza), then eat your way through Japan\'s most famous food street. This is where you understand why Osaka\'s motto is kuidaore — "eat till you drop."',
              details: [
                '📍 Dōtonbori, Chūō-ku — Namba Station',
                '🕐 Best from 5pm onward when the neon is blazing',
                '🆓 Free to walk and gawk'
              ]
            },
            {
              title: 'Osaka Street Food Grand Tour',
              description: 'Hit the greatest hits: takoyaki (octopus balls) from Wanaka or Creo-Ru, okonomiyaki (savory pancake) from Mizuno or Fukutaro, gyōza from Chao Chao, and finish with a cheesecake from Rikuro Ojisan (watch it jiggle!). Each is a few hundred yen — this is how Osaka eats.',
              details: [
                '🐙 Takoyaki at Wanaka: crispy outside, molten inside — ¥500',
                '🥞 Okonomiyaki at Mizuno: Osaka-style with layers of cabbage and pork — ¥1,000',
                '🥟 Gyōza at Chao Chao: crispy pan-fried — ¥400',
                '🧀 Rikuro Ojisan cheesecake: iconic jiggly cheesecake — ¥965 whole cake!',
                '💡 Pace yourself — it\'s easy to over-order when everything smells incredible'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dōtonbori Street Food Crawl',
              description: 'Not a single restaurant — a crawl through Osaka\'s greatest hits. Takoyaki → okonomiyaki → kushikatsu → gyōza → cheesecake. Budget ¥2,000-3,000 total for an unforgettable feast.',
              meta: '💰 ¥2,000-3,000 total · Dōtonbori · Street food crawl'
            }
          ],
          tips: [
            { type: 'tip', text: '🏨 Stay in Namba/Shinsaibashi area to be walking distance from Dōtonbori. Nine Hours Namba is an excellent capsule hotel (¥3,500) for the experience. Or Vessel Inn Shinsaibashi (¥5,500) for a regular room with great location.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle Park', num: 1, cat: 'sight', desc: '3,000 cherry trees surrounding the castle' },
        { lat: 34.6630, lng: 135.5065, label: 'Kuromon Market', num: 2, cat: 'food', desc: 'Osaka\'s Kitchen — 170+ food stalls' },
        { lat: 34.6524, lng: 135.5063, label: 'Shinsekai', num: 3, cat: 'culture', desc: 'Retro neighborhood with Tsūtenkaku Tower' },
        { lat: 34.6520, lng: 135.5058, label: 'Kushikatsu Daruma', num: 4, cat: 'food', desc: 'Iconic deep-fried skewer original location' },
        { lat: 34.6687, lng: 135.5018, label: 'Dōtonbori', num: 5, cat: 'sight', desc: 'Neon-lit canal and street food paradise' },
        { lat: 34.6690, lng: 135.5012, label: 'Takoyaki Wanaka', num: 6, cat: 'food', desc: 'Osaka\'s best octopus balls' }
      ]
    },

    // ===================== DAY 9 — March 25: Osaka → Tokyo (Naka-Meguro) =====================
    {
      num: 9,
      date: 'March 25',
      neighborhoods: 'Osaka · Shinkansen · Naka-Meguro',
      title: 'Homecoming: Osaka to Your New Life in Naka-Meguro',
      description: 'Your final travel day — but also the first day of your new chapter. Take the Shinkansen from Osaka to Tokyo and settle into Naka-Meguro, one of Tokyo\'s most charming neighborhoods. The Meguro River cherry blossoms should be just starting to bloom — a perfect welcome to your new home.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Last Morning in Osaka — Breakfast at Shin-Osaka',
              description: 'If time allows, explore the excellent food halls inside Shin-Osaka Station before your train. The Ekimarché has a wonderful selection of Osaka souvenirs and fresh food. Or grab a final batch of takoyaki from the station stalls.',
              details: [
                '📍 Shin-Osaka Station Ekimarché',
                '💡 Buy omiyage (souvenirs) here: 551 HORAI pork buns are Osaka\'s most popular gift (but eat them fresh — they\'re famous on the Shinkansen)',
                '🎁 Pick up a box of baton d\'or (fancy Pocky, Osaka-exclusive) for your new neighbors in Naka-Meguro'
              ]
            },
            {
              title: 'Shinkansen: Shin-Osaka → Shinagawa/Tokyo',
              description: 'Take the Tokaido Shinkansen Nozomi or Hikari from Shin-Osaka to Tokyo or Shinagawa (~2.5 hours). The Hikari is covered by JR Pass; the Nozomi is faster but not covered. On a clear day, watch for Mt. Fuji on the right side between Shizuoka and Shin-Yokohama.',
              details: [
                '🚂 Hikari: 2h50, covered by JR Pass',
                '🚂 Nozomi: 2h25, NOT covered by JR Pass (¥13,870)',
                '💡 Sit on the right side (E seat) for the Mt. Fuji view around Shin-Fuji Station',
                '🏔️ Clear-sky probability in late March: ~40%. If you see Fuji, it\'s a good omen for your new life!'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast/Brunch',
              name: '551 HORAI Pork Buns (on the Shinkansen)',
              description: 'Osaka\'s famous 551 HORAI butaman (steamed pork buns) are a Shinkansen tradition. Buy a box at Shin-Osaka Station and eat them warm on the train. The entire car will smell amazing.',
              meta: '💰 ¥510 for 2 pieces · Shin-Osaka Station'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If your JR Pass is still valid, take the Hikari. If it expired, the Nozomi is ¥13,870 but 25 min faster. Either way, it\'s your last Shinkansen — enjoy the ride.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive in Naka-Meguro & Settle In',
              description: 'Welcome home! Naka-Meguro is one of Tokyo\'s most desirable neighborhoods — a perfect blend of hip cafés, independent boutiques, and quiet residential streets along the Meguro River. Drop your bags and take a first walk along the river to get your bearings.',
              details: [
                '🚂 From Shinagawa/Tokyo: take the Yamanote Line to Ebisu, then Hibiya Line one stop to Naka-Meguro. Or Tōkyū Tōyoko Line from Shibuya (one stop)',
                '📍 Naka-Meguro Station, Meguro-ku, Tokyo',
                '💡 Your neighborhood: the area between the station and the Meguro River is the main commercial strip. South of the river is quieter and residential.'
              ]
            },
            {
              title: 'Meguro River Cherry Blossom Preview Walk (目黒川の桜)',
              description: 'The Meguro River cherry blossoms are Tokyo\'s most beloved — 800 trees lining both banks for almost 4km. By March 25, the first buds should be opening. In a few days, when full bloom arrives, this will be one of the most spectacular sakura tunnels in Japan — and it\'s your daily walk now. Lanterns are strung between the trees and light up at night during peak bloom.',
              details: [
                '📍 Meguro River, from Ikejiri-Ōhashi to Meguro Station',
                '🕐 Best section: Naka-Meguro Station to Meguro Station (~30 min walk)',
                '🆓 Free',
                '🌸 Full bloom usually hits Meguro River March 28-April 2 — you\'ll be here for it!',
                '💡 Walk it now to see the buds, then come back in 3-4 days for the full spectacle. You live here now — best sakura season upgrade possible.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Onigiri Asakusa Yadoroku',
              description: 'No — your first Tokyo lunch should be something simple and perfect. Walk to the nearest konbini or find a local onigiri shop. You\'ll eat here every day — start discovering your daily spots.',
              meta: '💰 ¥300-800 · Naka-Meguro neighborhood'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Naka-Meguro Neighborhood Dinner — Your New Local',
              description: 'For your first evening at home, explore the streets around Naka-Meguro Station. The area is packed with excellent small restaurants, craft coffee shops, and cozy izakayas. Try Afuri (yuzu shio ramen, originally from Kanagawa) or Yakitori Hachibei for charcoal-grilled chicken skewers with locals at the counter.',
              details: [
                '📍 Afuri Naka-Meguro: 1-1-7 Kamimeguro — famous yuzu ramen',
                '📍 Yakitori Hachibei: near the station — counter seats, great atmosphere',
                '💡 Walk south of the river on the small residential streets — you\'ll discover hidden izakayas that will become your regular spots',
                '🍺 Blue Bottle Coffee\'s Naka-Meguro location is in a beautiful converted warehouse — perfect afternoon coffee tomorrow'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Afuri (阿夫利) Ramen — Naka-Meguro',
              description: 'Celebrate arriving home with a bowl of Afuri\'s signature yuzu shio ramen — light, citrusy, and completely different from heavy tonkotsu. The handmade noodles and yuzu-infused broth are addictive. This is your neighborhood ramen shop now.',
              meta: '💰 ¥1,000-1,400 · Naka-Meguro · Yuzu ramen'
            }
          ],
          tips: [
            { type: 'tip', text: '🏡 Welcome to Naka-Meguro! You have the rest of the year to explore Tokyo, Kyoto deep cuts, Hiroshima, Hokkaido, and everything else on your list. But first — enjoy the Meguro River sakura from your new home. It doesn\'t get better than this. 🌸' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7335, lng: 135.5001, label: 'Shin-Osaka Station', num: 1, cat: 'transport', desc: 'Shinkansen departure to Tokyo' },
        { lat: 35.6440, lng: 139.6988, label: 'Naka-Meguro Station', num: 2, cat: 'transport', desc: 'Your new home base' },
        { lat: 35.6445, lng: 139.6970, label: 'Meguro River Cherry Trees', num: 3, cat: 'nature', desc: '800 cherry trees along 4km — Tokyo\'s best sakura' },
        { lat: 35.6437, lng: 139.6985, label: 'Afuri Ramen', num: 4, cat: 'food', desc: 'Famous yuzu shio ramen — your new local' },
        { lat: 35.6450, lng: 139.6975, label: 'Blue Bottle Coffee', num: 5, cat: 'food', desc: 'Converted warehouse café on the river' }
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete!');
  console.log('URL:', result.url);
  console.log('Slug:', result.slug);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
