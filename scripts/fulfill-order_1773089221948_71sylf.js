const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773089221948_71sylf',
  email: 'speak@kaeko.us',
  destination: 'Tokyo, Japan',
  startDate: '2026-04-27',
  endDate: '2026-05-02',
  groupSize: 2,
  requests: 'Two vegetarian travelers arriving from Europe, gentle jetlag recovery pace, Haneda landing 13:55 Apr 27, departing 19:40 May 2. Both techy, appreciate history/architecture/culture. Explore beyond Tokyo towards Mt Fuji 1-2 days. Walking and nature. Bookmarked: teamLab Borderless, Kamakura, Ashikaga Flower Park, Ghibli Museum, Shinjuku Gyoen, Rikugien, Meiji Shrine, Yoyogi Park, Skytree, Edo-Tokyo Open Air Museum, private onsen, Imperial Palace.'
};

const itineraryData = {
  destination: 'Tokyo & Hakone, Japan',
  countryEmoji: '🇯🇵',
  title: 'Wisteria, Fuji & the Vegetarian Path Through Tokyo',
  subtitle: '6 days of zen gardens, temple cuisine & mountain escapes for two — timed for Golden Week and peak wisteria bloom',
  description: "This itinerary is designed for two vegetarian travelers arriving from Europe with a gentle first-day pace, then gradually building into Tokyo's most spectacular cultural highlights — timed to coincide with peak wisteria season at Ashikaga Flower Park and the energy of Golden Week. You'll experience shojin ryori (Zen Buddhist cuisine), immerse yourselves in teamLab's digital art, explore Kamakura's ancient temples, and escape to Hakone for private onsen with Mt Fuji views. Every meal recommendation is vegetarian-friendly, and the pace leaves room for spontaneous detours.",
  duration: '5 nights',
  dates: 'Apr 27 – May 2, 2026',
  budget: '$',
  pace: 'Gentle',
  bestFor: 'Couples · Vegetarians · Culture Lovers',
  highlights: [
    'Peak wisteria bloom at Ashikaga Flower Park — cascading purple tunnels',
    'Shojin ryori tasting menus — centuries-old Zen Buddhist vegetarian cuisine',
    'teamLab Borderless at Azabudai Hills — immersive digital art without boundaries',
    'Private onsen with Mount Fuji views in Hakone',
    'Kamakura\'s Great Buddha, bamboo grove & seaside temple town',
    'Golden Week atmosphere — Japan at its most festive and alive'
  ],
  essentials: [
    { title: '🥬 Vegetarian Dining in Japan', text: "Japan can be tricky for vegetarians — dashi (fish stock) is in almost everything. Key phrases: \"Watashi wa bejitarian desu\" (I am vegetarian). Shojin ryori (Buddhist temple cuisine) is your best friend — entirely plant-based. Konbini have umeboshi onigiri, inari-zushi, and edamame. Download HappyCow app." },
    { title: '🎌 Golden Week Alert', text: "Your trip overlaps with Golden Week (Apr 29–May 5). Expect HUGE crowds, fully booked hotels, packed trains. We've scheduled early-morning visits to beat the rush. Book all tickets (teamLab, Ghibli Museum, Hakone trains) well in advance." },
    { title: '🚃 Getting Around', text: "Get a Suica IC card at Haneda — works on all trains, buses, and konbini. For Hakone, buy the Hakone Free Pass (about 6,100 yen, 2-day validity) covering Romancecar, cable car, ropeway, pirate ship, and buses. Consider a 72-hour Tokyo Subway Ticket (1,500 yen)." },
    { title: '🌸 Weather & Packing', text: "Late April averages 15-22°C. Pack layers, comfortable walking shoes, a light rain jacket, and quick-dry layers for onsen days." },
    { title: '♨️ Onsen Etiquette', text: "Wash thoroughly before entering. Small towel on your head, not in water. Private onsen (kashikiri) bypasses tattoo restrictions and is perfect for couples." }
  ],
  days: [
    {
      num: 1, date: '2026-04-27',
      neighborhoods: 'Haneda · Shinagawa · Meguro',
      title: 'Gentle Arrival — Touchdown & First Steps',
      description: "Land at Haneda at 1:55pm, clear customs by ~3pm, ease into Tokyo. Today is about arriving, settling in, and your first taste of Japanese vegetarian food.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            { title: 'Arrive at Haneda & Transit to Hotel', description: "Clear immigration (45-60 min), take Keikyu Line to Shinagawa (18 min). Drop bags and take a breather.", details: ['Haneda Terminal 3 → Keikyu Line to Shinagawa (18 min, 300 yen)', 'Buy Suica card at airport or use Apple Pay Suica', 'Budget: Shinagawa/Meguro hostels from 3,500 yen/night pp'] },
            { title: 'Meguro River Walk & Daienji Temple', description: "Gentle 30-min stroll along the Meguro River — green tree tunnel in late April. Stop at Daienji Temple with 500 stone arhat statues on its hillside.", details: ['Flat, shaded walk — perfect for jet-lagged legs', 'Daienji Temple is 400 years old with 500 carved statues', 'Uncrowded on weekday afternoons'] }
          ],
          meals: [
            { type: 'Dinner', name: 'Afuri Ramen — Meguro', description: "Famous yuzu shio ramen with a fully vegan version. Light, fragrant, perfect jet-lag recovery meal.", meta: '1,100-1,400 yen · Meguro Station · Vegan option available' }
          ],
          tips: [
            { type: 'tip', text: "Jet-lag strategy: Stay awake until 9pm, drink water, walk outside for daylight. Don't nap longer than 20 min." },
            { type: 'tip', text: "Konbini veggie picks: umeboshi onigiri, inari-zushi, edamame, anpan (sweet red bean bread)." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.5494, lng: 139.7798, label: 'Haneda Airport', num: 1, cat: 'transport', desc: 'International arrival Terminal 3' },
        { lat: 35.6284, lng: 139.7388, label: 'Shinagawa Station', num: 2, cat: 'transport', desc: '18 min from Haneda on Keikyu Line' },
        { lat: 35.6339, lng: 139.7157, label: 'Meguro River Walk', num: 3, cat: 'attraction', desc: 'Peaceful canal walk with green tree tunnel' },
        { lat: 35.6330, lng: 139.7116, label: 'Daienji Temple', num: 4, cat: 'attraction', desc: '400-year-old temple with 500 arhat statues' },
        { lat: 35.6332, lng: 139.7155, label: 'Afuri Ramen', num: 5, cat: 'food', desc: 'Yuzu shio ramen with vegan option' }
      ]
    },
    {
      num: 2, date: '2026-04-28',
      neighborhoods: 'Ashikaga · Shinjuku · Azabudai Hills',
      title: 'Wisteria Wonderland & Digital Art Immersion',
      description: "Early start for Ashikaga Flower Park at peak wisteria bloom — one of Japan's most magical sights. Return for teamLab Borderless at Azabudai Hills. Two unforgettable visual experiences in one day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Ashikaga Flower Park — Peak Wisteria', description: "Take early train from Tokyo (about 2 hours via JR). The Great Wisteria Trellis — a 150-year-old tree covering 1,000 sqm — is a natural monument. Walk through tunnels of purple, white, pink, and yellow wisteria.", details: ['Great Wisteria Festival: Apr 11–May 20, 2026', 'Gates open 7am in peak season — arrive EARLY', 'Train: Tokyo → Oyama (Shinkansen 45 min) → Ashikaga Flower Park (local 30 min)', 'Admission 1,200-2,300 yen depending on bloom', 'Best photos: 80m wisteria tunnel and reflection pool', 'Allow 2-3 hours — park is 9.4 hectares'] }
          ],
          meals: [
            { type: 'Breakfast', name: 'Konbini Grab & Go', description: "Station konbini onigiri, bento, and canned coffee. Umeboshi onigiri and inari-zushi are reliably vegetarian.", meta: '400-600 yen · Any station store' },
            { type: 'Lunch', name: 'Ashikaga Park Stalls', description: "Yaki-dango, wisteria soft serve, vegetable tempura. Ask about dashi — some stalls use kombu-only broth.", meta: '500-1,000 yen · Inside park' }
          ],
          tips: [
            { type: 'tip', text: "Apr 28 is a regular Tuesday — much better than the following Golden Week weekend. 7am opening is your window for peaceful photos." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Shinjuku Gyoen National Garden', description: "Back in Tokyo by 2pm, visit this 58-hectare garden combining Japanese, English, and French styles. Late April: last yaezakura cherry blossoms and first azaleas.", details: ['Open 9am-6pm, 500 yen · Closed Mon (Apr 28 = Tue, open)', 'Japanese Garden teahouse and koi pond are the most serene', 'Greenhouse with tropical plants — a quiet escape'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'teamLab Borderless — Azabudai Hills', description: "Immersive digital art museum. Artworks flow between rooms and respond to your presence. Infinity Mirror Room, digital waterfalls, Crystal Universe. Book 5-6pm slot.", details: ['Azabudai Hills Garden Plaza B, B1F — 2 min from Kamiyacho Station', '3,800 yen/adult — book online weeks ahead (Golden Week sellouts)', 'Allow 2-3 hours · Wear dark clothes and flat shoes', 'Bring portable charger — phone drains fast'] }
          ],
          meals: [
            { type: 'Dinner', name: "T's TanTan — Tokyo Station", description: "100% vegan restaurant inside Tokyo Station. Incredible tantanmen (spicy sesame noodles), vegan gyoza, soy-meat karaage.", meta: '900-1,300 yen · Tokyo Station Keiyo Street · Fully vegan' }
          ]
        }
      ],
      mapPins: [
        { lat: 36.3147, lng: 139.5197, label: 'Ashikaga Flower Park', num: 1, cat: 'attraction', desc: 'Peak wisteria — 150-year-old Great Wisteria Trellis' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 2, cat: 'attraction', desc: '58-hectare national garden' },
        { lat: 35.6574, lng: 139.7384, label: 'teamLab Borderless', num: 3, cat: 'attraction', desc: 'Immersive digital art at Azabudai Hills' },
        { lat: 35.6812, lng: 139.7671, label: "T's TanTan", num: 4, cat: 'food', desc: 'Vegan tantanmen inside Tokyo Station' }
      ]
    },
    {
      num: 3, date: '2026-04-29',
      neighborhoods: 'Harajuku · Meiji Shrine · Rikugien · Asakusa',
      title: 'Showa Day — Shrines, Gardens & the Skyline',
      description: "Showa Day (national holiday) kicks off Golden Week. Meiji Shrine's forest, Yoyogi Park's festive atmosphere, Rikugien's exquisite garden, and Tokyo Skytree at sunset.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Meiji Shrine & Yoyogi Park', description: "Walk through 70 hectares of dense forest to the spiritual heart of Tokyo. The shrine is stunning in simplicity. Yoyogi Park will have cosplayers, performers, and festival stalls for Showa Day.", details: ['Arrive by 8am to beat Golden Week crowds', 'Forest planted 1920 with 100,000 trees from across Japan', 'Write a wish on ema (wooden plaque) — 500 yen', 'Yoyogi Park lawns perfect for resting with konbini snacks'] }
          ],
          meals: [
            { type: 'Brunch', name: 'Ain Soph Journey — Shinjuku', description: "Tokyo's most beloved vegan chain. Fluffy vegan pancakes, burgers, pasta, curries. 100% plant-based.", meta: '1,200-1,800 yen · 5 min from Shinjuku Stn · Fully vegan' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Rikugien Garden', description: "Tokyo's most beautiful traditional garden (1702). 88 scenes from Japanese/Chinese poetry recreated in miniature landscapes. Azaleas blooming in late April.", details: ['Open 9am-5pm, 300 yen · Komagome Station 5 min', 'Matcha and wagashi at Fukiage Chaya teahouse', 'Fujishiro-toge hill has the finest view', 'Allow 1-1.5 hours'] },
            { title: 'Imperial Palace East Gardens', description: "Free Edo Castle grounds with ancient stone walls, moats, and the Ninomaru Garden. Architecture lovers will appreciate the layered history.", details: ['Free · Open 9am-4:30pm · Closed Mon & Fri', 'Otemachi or Tokyo Station — 10 min walk', 'Ninomaru Garden: 260 tree varieties from Edo period', 'Climb to Honmaru foundation for panoramic views'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Tokyo Skytree at Sunset', description: "World's tallest tower (634m). Tembo Deck at 350m and Galleria at 450m. On clear days, Mt Fuji is visible. Arrive 30 min before sunset.", details: ['2,100 yen (deck) or 3,100 yen (both) — timed tickets online', 'Sunset ~6:15pm late April — arrive 5:45pm', 'Southwest windows for Fuji + sunset combo'] }
          ],
          meals: [
            { type: 'Dinner', name: 'Soranoiro Nippon — Skytree Solamachi', description: "Celebrated vegan ramen with soy broth and colourful vegetable toppings. Photogenic green veggie-soba noodles.", meta: '1,000-1,400 yen · Skytree complex · Vegan ramen' }
          ],
          tips: [
            { type: 'tip', text: "Showa Day crowds: shrines peaceful before 9am, gardens thin after 3pm, Skytree best with pre-booked evening tickets." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Shinto shrine in 70-hectare forest' },
        { lat: 35.6717, lng: 139.6949, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Festival atmosphere on Showa Day' },
        { lat: 35.6888, lng: 139.7053, label: 'Ain Soph Journey', num: 3, cat: 'food', desc: 'Vegan pancakes and curries' },
        { lat: 35.7329, lng: 139.7455, label: 'Rikugien Garden', num: 4, cat: 'attraction', desc: 'Finest Edo-period stroll garden' },
        { lat: 35.6874, lng: 139.7603, label: 'Imperial Palace East Gardens', num: 5, cat: 'attraction', desc: 'Edo Castle ruins — free entry' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 6, cat: 'attraction', desc: 'Sunset views from 350m' },
        { lat: 35.7101, lng: 139.8085, label: 'Soranoiro Nippon', num: 7, cat: 'food', desc: 'Vegan ramen at Solamachi' }
      ]
    },
    {
      num: 4, date: '2026-04-30',
      neighborhoods: 'Kamakura · Kita-Kamakura · Hase',
      title: 'Ancient Kamakura — Great Buddha, Bamboo & the Sea',
      description: "Escape to Kamakura — ancient seaside capital with 65+ temples, bamboo groves, and the iconic Great Buddha. Start at quiet Kita-Kamakura Zen temples, then the main sights. Relaxed energy and good vegetarian dining.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Kita-Kamakura — Engaku-ji & Kencho-ji', description: "JR Yokosuka Line from Tokyo (55 min). Engaku-ji: moss-covered steps through ancient Zen gates. Walk to Kencho-ji (Japan's oldest Zen monastery, 1253) and climb the hillside trail for ocean views.", details: ['Tokyo → Kita-Kamakura 55 min, 940 yen', 'Engaku-ji: 500 yen · Founded 1282', 'Kencho-ji: 500 yen · Hillside trail 20 min climb', 'Arrive 9am for near-solitude'] }
          ],
          meals: [
            { type: 'Lunch', name: 'Bowls Kamakura', description: "Vegetarian-friendly cafe with acai bowls, smoothie bowls, plant-based plates. Or try Onari Yokocho for vegan sushi/curry.", meta: '1,000-1,500 yen · Near Kamakura Station · Vegan options' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Great Buddha (Kotoku-in)', description: "13.35m bronze Buddha in open air since a 1498 tsunami destroyed its hall. Step inside for 50 yen extra to see centuries-old casting technique.", details: ['300 yen + 50 yen interior · Open 8am-5:30pm', 'Enoden train to Hase or 20 min walk from Kamakura Stn', 'Best angle: left side pathway approaching'] },
            { title: 'Hase-dera Temple', description: "Hillside temple overlooking the ocean. Bamboo-lined paths, carved cave statues, sweeping Sagami Bay views from observation deck.", details: ['400 yen · Open 8am-5pm', 'Bamboo path less crowded than Kyoto\'s famous grove', 'Benten-kutsu cave with carved goddess statues', 'Ocean view from upper terrace is stunning'] },
            { title: 'Komachi-dori Street', description: "Kamakura's lively shopping street with pottery, crafts, matcha sweets. Veggie snacks: warabi mochi, yaki-dango, matcha soft serve, senbei.", details: ['360m street ending at Tsurugaoka Hachimangu shrine', 'Golden Week afternoons = packed'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Return & Shojin Ryori Dinner', description: "Direct JR from Kamakura to Tokyo (55 min). Tonight, experience the pinnacle of Japanese vegetarian cuisine.", details: ['Pack bags tonight — Hakone tomorrow'] }
          ],
          meals: [
            { type: 'Dinner', name: 'Daigo — Shiba Park', description: "Two-Michelin-star shojin ryori (Zen Buddhist cuisine) for over 70 years. Multi-course kaiseki with seasonal vegetables, tofu, yuba, mountain herbs. A once-in-a-lifetime vegetarian dining experience. Or try Bon in Taito-ku for 4,000-6,000 yen.", meta: '8,000-15,000 yen pp · Shiba Park near Tokyo Tower · Reservation essential' }
          ],
          tips: [
            { type: 'tip', text: "Apr 30 is a regular weekday — smaller crowds than surrounding holidays. Perfect for temple hopping." },
            { type: 'tip', text: "If Daigo feels too splurgy, Bon in Taito-ku serves excellent fucha ryori at 4,000-6,000 yen — still fully vegetarian and unforgettable." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3388, lng: 139.5454, label: 'Engaku-ji Temple', num: 1, cat: 'attraction', desc: 'Great Zen temple founded 1282' },
        { lat: 35.3351, lng: 139.5515, label: 'Kencho-ji', num: 2, cat: 'attraction', desc: 'Oldest Zen monastery in Japan' },
        { lat: 35.3167, lng: 139.5356, label: 'Great Buddha', num: 3, cat: 'attraction', desc: '13m bronze Buddha in open air since 1498' },
        { lat: 35.3125, lng: 139.5328, label: 'Hase-dera', num: 4, cat: 'attraction', desc: 'Hillside temple with ocean views' },
        { lat: 35.3248, lng: 139.5528, label: 'Komachi-dori', num: 5, cat: 'attraction', desc: 'Lively shopping street with veggie snacks' },
        { lat: 35.6562, lng: 139.7465, label: 'Daigo Restaurant', num: 6, cat: 'food', desc: '2-Michelin-star shojin ryori' }
      ]
    },
    {
      num: 5, date: '2026-05-01',
      neighborhoods: 'Hakone · Owakudani · Lake Ashi · Gora',
      title: 'Hakone Escape — Mt Fuji, Hot Springs & Mountain Air',
      description: "Leave Tokyo behind for the mountains and hot springs of Hakone. Ride the Romancecar, take cable cars over volcanic valleys, cruise Lake Ashi with Mt Fuji towering behind, and soak in a private onsen at a ryokan. This is the mountain-and-nature experience you've been dreaming of.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Romancecar to Hakone-Yumoto', description: "Board the Odakyu Romancecar from Shinjuku — a panoramic observation train that winds through mountains to Hakone (85 min). At Hakone-Yumoto, take the Hakone Tozan Railway switchback train up the mountain to Gora.", details: ['Romancecar: Shinjuku → Hakone-Yumoto 85 min (covered by Hakone Free Pass + 1,200 yen surcharge)', 'Buy Hakone Free Pass at Shinjuku (6,100 yen, 2-day) — covers all transport in Hakone', 'Hakone Tozan Railway: switchback mountain train to Gora (40 min)', 'Store luggage at Hakone-Yumoto station lockers'] },
            { title: 'Hakone Open-Air Museum', description: "Japan's first open-air museum set against a mountain backdrop. Over 120 sculptures by Picasso, Henry Moore, and Japanese artists scattered across rolling lawns. The Picasso Pavilion alone is worth the visit. The hot-spring foot bath in the garden is a bonus.", details: ['1,600 yen · 5 min walk from Chokoku-no-Mori Station', 'Hot spring foot bath inside the sculpture garden — free with admission', 'Allow 1.5-2 hours · Partly outdoors so dress for weather', 'The stained glass tower is stunning on a sunny day'] }
          ],
          meals: [
            { type: 'Lunch', name: 'Gora Brewery & Grill', description: "Craft beer brewery in Gora with excellent vegetarian options including veggie pizza, salads, and seasonal plates. Great mountain views from the terrace.", meta: '1,500-2,500 yen · Gora, Hakone · Vegetarian options' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Owakudani Volcanic Valley', description: "Take the Hakone Ropeway from Gora over Owakudani — an active volcanic valley with sulphurous steam vents, bubbling pools, and dramatic views. On clear days, Mt Fuji looms perfectly behind the valley. The famous kuro-tamago (black eggs boiled in sulphur springs) are said to add 7 years to your life.", details: ['Ropeway: Gora → Owakudani → Togendai (30 min total, included in Free Pass)', 'Black eggs: 500 yen for 5 — vegetarian! Cooked in natural hot springs', 'Mt Fuji visibility is best on clear mornings — fingers crossed', 'Volcanic fumes: follow staff guidance on restricted areas'] },
            { title: 'Lake Ashi Pirate Ship Cruise', description: "Board the Hakone Sightseeing Cruise (yes, it's a pirate ship) from Togendai Port across Lake Ashi to Hakone-machi or Moto-Hakone. Mt Fuji reflected in the lake with the vermillion torii gate of Hakone Shrine in the foreground is one of Japan's most iconic views.", details: ['30 min cruise (included in Free Pass)', 'Best views of Fuji from the upper deck — sit on the right side', 'Hakone Shrine\'s lakeside torii gate is a 10 min walk from the port', 'Return to Gora area by bus for evening'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Private Onsen at Ryokan', description: "Check into a ryokan (traditional inn) in the Gora or Hakone-Yumoto area and soak in a private onsen. Several budget-friendly options offer rooms with private outdoor baths. Tenzan Onsen in Hakone is an excellent day-onsen alternative if your accommodation doesn't have private baths.", details: ['Budget ryokan: 8,000-15,000 yen pp including dinner and breakfast', 'Wakakusa no Yado Maruei (Kawaguchiko area) has private Fuji-view onsen from 12,000 yen', 'Tenzan Onsen: 1,300 yen day pass, tattoo-friendly, outdoor rock baths', 'Request vegetarian meals when booking — most ryokan accommodate with advance notice', 'Evening onsen under the stars is pure magic'] }
          ],
          meals: [
            { type: 'Dinner', name: 'Ryokan Kaiseki (Vegetarian)', description: "Many Hakone ryokan serve kaiseki (multi-course dinner). Request vegetarian when booking — you'll receive beautifully presented seasonal vegetables, tofu, mountain vegetables, and rice. Alternatively, Gora has several restaurants.", meta: 'Included with ryokan stay · Request vegetarian in advance' }
          ],
          tips: [
            { type: 'tip', text: "Golden Week in Hakone: Book ryokan months ahead. The Romancecar sells out — reserve seats online. Ropeway may have 30+ min waits; go early." },
            { type: 'tip', text: "The Hakone Free Pass is incredible value — 6,100 yen covers round-trip from Shinjuku plus ALL Hakone transport for 2 days." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2328, lng: 139.1059, label: 'Hakone-Yumoto Station', num: 1, cat: 'transport', desc: 'Hakone gateway — Romancecar terminus' },
        { lat: 35.2453, lng: 139.0644, label: 'Hakone Open-Air Museum', num: 2, cat: 'attraction', desc: '120+ sculptures with mountain backdrop' },
        { lat: 35.2468, lng: 139.0219, label: 'Owakudani', num: 3, cat: 'attraction', desc: 'Volcanic valley with sulphur vents and black eggs' },
        { lat: 35.2069, lng: 139.0222, label: 'Lake Ashi', num: 4, cat: 'attraction', desc: 'Pirate ship cruise with Mt Fuji views' },
        { lat: 35.2050, lng: 139.0280, label: 'Hakone Shrine', num: 5, cat: 'attraction', desc: 'Lakeside torii gate — iconic Fuji photo spot' },
        { lat: 35.2379, lng: 139.0651, label: 'Gora Area', num: 6, cat: 'attraction', desc: 'Mountain town with ryokan and onsen' }
      ]
    },
