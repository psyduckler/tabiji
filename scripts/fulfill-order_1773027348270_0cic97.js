const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773027348270_0cic97',
  email: 'amyalil1909@gmail.com',
  destination: 'Japan',
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'Japan in 12 Days: Tokyo, Hakone, Kyoto, Nara, Osaka & Hiroshima',
  subtitle: 'Cherry blossoms, ancient temples, mountain onsen, deer parks, and the world\'s best street food — all packed into one unforgettable adventure for 3-4 people',
  description: 'Mid-to-late March is one of the best times to visit Japan — cherry blossoms bloom across the country in a rolling wave, transforming shrine gates, canal banks, and mountain paths into pink-and-white wonderlands. This 12-day itinerary covers Japan\'s greatest hits plus some hidden gems: four days in Tokyo with a Hakone detour for Mt. Fuji views and hot springs, three days in Kyoto exploring ancient temples and bamboo forests, a half-day feeding deer in Nara, two days of Osaka street food and nightlife, and a day trip to Hiroshima and Miyajima island that will stay with you forever. With a 7-day JR Pass and careful routing, you\'ll cover serious ground while keeping costs well within budget.',
  duration: '12 days',
  dates: 'Mar 16 – Mar 28, 2026',
  budget: '$1,000–2,000 per person',
  pace: 'Active',
  bestFor: 'Families, Adventurers, Culture lovers',

  highlights: [
    'Cherry blossoms at Ueno Park, Philosopher\'s Path & Maruyama Park',
    'Mt. Fuji views and outdoor onsen in Hakone',
    'Thousands of torii gates at Fushimi Inari at sunrise',
    'Arashiyama bamboo grove and monkey mountain',
    'Hand-feeding free-roaming deer in Nara\'s ancient park',
    'Hiroshima Peace Memorial and Miyajima\'s floating torii gate',
    'Osaka street food crawl — takoyaki, kushikatsu, and okonomiyaki',
    'Shibuya Crossing, Senso-ji Temple, and Dotonbori neon chaos',
    '7-day JR Pass covering all shinkansen between cities',
    'Local ryokan breakfast, sake vending machines, and 7-Eleven onigiri at midnight',
  ],

  essentials: [
    {
      title: '🚅 Getting Around — JR Pass',
      text: 'Buy a 7-day JR Pass before you leave home (must be purchased outside Japan). Activate it on Day 4 or 5 when you take your first shinkansen. It covers all JR shinkansen between Tokyo→Kyoto→Osaka→Hiroshima, plus JR local trains. For Tokyo\'s subway, top up a Suica/Pasmo IC card at any station.',
    },
    {
      title: '💵 Money — Cash Is King',
      text: 'Japan is still heavily cash-reliant. Bring or withdraw yen at 7-Eleven ATMs (international cards accepted). Budget ¥5,000-8,000/person/day for food, transport, and activities. Convenience stores (konbini) — 7-Eleven, Lawson, FamilyMart — are your best friend for cheap, amazing food available 24/7.',
    },
    {
      title: '🌸 Cherry Blossom Season (Mid-March)',
      text: 'Mid-to-late March is prime sakura season. Tokyo typically peaks around March 25-31; Kyoto slightly earlier. You may catch the very beginning of bloom in Tokyo (Days 1-4) and full peak in Kyoto (Days 5-7). Check sakura.weathermap.jp for real-time forecasts. Bring a picnic blanket for hanami (flower viewing) sessions!',
    },
    {
      title: '🗣️ Language Tips',
      text: 'Japanese. Major train stations and tourist areas have excellent English signage. Google Translate camera mode is essential for menus. Learn: sumimasen (excuse me), arigatou gozaimasu (thank you very much), ikura desu ka (how much is it?), eigo wo hanasemasu ka (do you speak English?). Japanese people are incredibly helpful even with no shared language.',
    },
    {
      title: '🏨 Where to Stay',
      text: 'Budget-savvy picks: Tokyo — Khaosan Tokyo Origami (Asakusa) or Unplan Shinjuku; Kyoto — Piece Hostel Sanjo or First Cabin Tenjin; Osaka — Cross Hotel Osaka or Dormy Inn Shinsaibashi. Mix in one ryokan night in Hakone for the full Japanese experience — worth every yen.',
    },
    {
      title: '🎌 Etiquette Essentials',
      text: 'No tipping — it\'s considered rude. Be quiet on trains, no phone calls. Remove shoes when indicated (look for genkan step). Queue politely — always. Don\'t eat while walking (except at festivals/markets). Tattoos may restrict onsen access — ask ahead. Bow slightly when thanking someone.',
    },
    {
      title: '📱 Connectivity',
      text: 'Rent a pocket Wi-Fi at the airport or buy a data SIM/eSIM before departure (Airalo or Ubigi, ~$5-15 for the trip). Japan has excellent free Wi-Fi at most train stations, konbini, and many restaurants. Download Google Maps offline for each city before you arrive.',
    },
  ],

  days: [
    // DAY 1 — Arrive Tokyo, Shinjuku, first wander
    {
      num: 1,
      date: 'Mar 16',
      title: 'Touchdown in Tokyo — Shinjuku First Night',
      description: 'After landing, get your bearings in Shinjuku — Tokyo\'s electric heart. Recover from the flight, get your Suica card, and dive into the neon-lit streets and izakayas of this endlessly entertaining neighborhood.',
      neighborhoods: 'Shinjuku · Kabukicho',
      timeBlocks: [
        {
          label: 'Arrival',
          activities: [
            {
              title: 'Airport → City (Narita or Haneda)',
              description: 'From Narita: Take the Keisei Skyliner to Ueno Station (36 min, ¥2,520) or the Airport Access Express (55 min, ¥1,290). From Haneda: Tokyo Monorail to Hamamatsucho or Keikyu Line (25-30 min, ¥650). Both routes drop you into the JR/subway network. Get a Suica or Pasmo IC card at any station machine — tap it for every train, bus, and many convenience stores.',
              details: [
                '💡 Luggage delivery (takuhaibin) service available at the airport — send bags to your hotel for ¥2,000-3,000 and explore light',
                '💡 7-Eleven ATMs at the airport accept most foreign cards',
              ],
            },
            {
              title: 'Check In & Rest',
              description: 'Check in, freshen up, and give yourself an hour to recover from the flight before heading out. Jet lag is real — a short rest now will serve you for 12 days.',
              details: [
                '💡 Shinjuku is the ideal base for Day 1 — everything is walkable or one train stop away',
              ],
            },
          ],
          meals: [],
          tips: [],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Exploration — East & West',
              description: 'Walk east through the neon chaos of Kabukicho — Tokyo\'s famous entertainment district. Wander the Memory Lane (Omoide Yokocho) alley lined with tiny yakitori stalls, smoke-filled and magical. Cross to the west side for the soaring Metropolitan Government Building observation deck (free, open until 10:30pm) and views of the city grid.',
              details: [
                '📍 Omoide Yokocho: 1-2-11 Nishishinjuku, Shinjuku-ku (west of Shinjuku Station)',
                '📍 Tokyo Metropolitan Government Building: 2-8-1 Nishishinjuku (free, North Tower open until 10:30pm)',
                '💡 Omoide Yokocho is best after dark — each tiny stall has maybe 8 seats and serves yakitori and beer',
              ],
            },
            {
              title: 'Golden Gai or Shinjuku 3-chome Bar Hopping',
              description: 'Golden Gai is a labyrinth of ~200 tiny bars, each with its own personality, theme, and ~10 seats. Pick a door, pay the cover (¥500-1,000), order a drink, and meet locals and travelers alike. One of the world\'s truly unique bar experiences — don\'t skip it.',
              details: [
                '📍 Golden Gai: 1-1-6 Kabukicho, Shinjuku-ku',
                '💡 Most bars have a 1-2 drink minimum. Don\'t be shy — bartenders are welcoming even to newcomers',
                '🍺 Shinjuku 3-chome (three stops on the subway) has excellent LGBTQ+ bars and is welcoming to all',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ichiran Ramen (Shinjuku)',
              description: 'The famous solo-booth ramen experience where you customize your own tonkotsu ramen via a paper form — richness level, firmness of noodles, garlic amount. A legendary first meal in Japan, open 24 hours. Perfect for jet-lagged solo diners or groups.',
              meta: '📍 Multiple Shinjuku locations · 💰 ¥900-1,200/person · Open 24hr',
            },
          ],
          tips: [
            { type: 'tip', text: '💡 Pick up tomorrow\'s breakfast from a 7-Eleven tonight — try an onigiri (rice ball), tamagoyaki (egg roll), and a canned coffee. Your first konbini experience awaits.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.6892, lng: 139.6917, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'World\'s busiest station — your Tokyo hub' },
        { lat: 35.6938, lng: 139.7034, label: 'Kabukicho', num: 2, cat: 'attraction', desc: 'Tokyo\'s neon entertainment district' },
        { lat: 35.6917, lng: 139.6925, label: 'Omoide Yokocho', num: 3, cat: 'restaurant', desc: 'Memory Lane — tiny yakitori stalls, smoke and magic' },
        { lat: 35.6896, lng: 139.6923, label: 'Golden Gai', num: 4, cat: 'attraction', desc: '200 tiny bars in a labyrinth — unmissable' },
        { lat: 35.6917, lng: 139.6953, label: 'Ichiran Ramen Shinjuku', num: 5, cat: 'restaurant', desc: 'Famous solo-booth tonkotsu ramen, customized to your taste' },
        { lat: 35.6896, lng: 139.6916, label: 'Tokyo Metropolitan Govt Building', num: 6, cat: 'attraction', desc: 'Free observation deck with panoramic city views until 10:30pm' },
      ],
    },

    // DAY 2 — Asakusa, Ueno, Akihabara
    {
      num: 2,
      date: 'Mar 17',
      title: 'Ancient Temples, Cherry Blossoms & Electric Town',
      description: 'Start with Tokyo\'s most iconic temple at dawn, spend the afternoon under cherry blossoms at Ueno\'s famous hanami park, and finish in the sensory overload of Akihabara.',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise-dori',
              description: 'Tokyo\'s oldest temple (628 AD) is stunning in early morning light, especially with cherry trees beginning to bloom across the grounds. Walk through the iconic Kaminarimon (Thunder Gate), browse the traditional craft stalls on Nakamise-dori, and explore the five-story pagoda and inner temple. The surrounding Asakusa neighborhood is beautifully preserved with rickshaws, kimono rentals, and old Tokyo vibes.',
              details: [
                '📍 2-3-1 Asakusa, Taito-ku',
                '🕐 Temple grounds always open · Main hall 6am-5pm · Free',
                '💡 Arrive by 7am — before the tour groups — for peaceful photos with early blossoms and morning mist',
                '🎋 Try your fortune with an omikuji slip (¥100) — if it\'s bad luck, tie it to the rack near the temple',
                '🍡 Try ningyo-yaki (sweet custard cakes) and age-manju (fried buns) on Nakamise-dori — ¥100-300',
              ],
            },
            {
              title: 'Asakusa Culture & Sumida River Walk',
              description: 'Walk west toward the Sumida River for stunning views of Tokyo Skytree reflected in the water. Explore the Sumida Park — one of Tokyo\'s oldest cherry blossom spots — then wander back through the charming shotengai (shopping streets) of Asakusa.',
              details: [
                '📍 Sumida Park, Taito-ku',
                '🌸 Sumida Park has ~400 cherry trees along the river — first of many hanami moments on this trip',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café (ペリカンカフェ)',
              description: 'A legendary Asakusa bakery that\'s been making bread since 1942. Their thick-cut toast with butter and jam, served with coffee, is a simple and perfect Tokyo morning meal. Gets crowded by 9am.',
              meta: '📍 1-4-16 Kotobuki, Taito-ku · 💰 ¥400-800/person · Opens 8am',
            },
          ],
          tips: [
            { type: 'tip', text: '🎎 Kimono rental in Asakusa (¥3,000-5,000) is worth doing for photos at Senso-ji — you\'ll walk the temple grounds feeling fully immersed. Book ahead.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park Cherry Blossom Hanami 🌸',
              description: 'One of Tokyo\'s most famous hanami spots with over 1,000 Somei Yoshino cherry trees. Spread a picnic blanket, buy bento boxes and drinks from nearby konbini, and join thousands of locals celebrating the blossoms. The main central path becomes a tunnel of pale pink blossoms. In the evenings, trees are lit up for magical yozakura (night blossom viewing).',
              details: [
                '📍 Uenokoen, Taito-ku · Free',
                '💡 Buy blue tarps (¥100 at Daiso nearby), bento boxes and drinks from the Lawson just outside the park',
                '🌸 The path between Keisei Ueno Station and the National Museum is the prime sakura corridor',
              ],
            },
            {
              title: 'Tokyo National Museum (if rainy or too crowded)',
              description: 'The world\'s largest collection of Japanese art right inside Ueno Park. Samurai swords, ancient pottery, Noh masks, woodblock prints. Perfect rainy-day fallback.',
              details: [
                '📍 13-9 Uenokoen, Taito-ku · 💰 ¥1,000/person · Closed Mon',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Ueno Ameyoko Street Food',
              description: 'Just outside Ueno Park, Ameyoko market street is packed with seafood stalls, yakitori, fresh fruit, and cheap izakayas. A chaotic, delicious lunch among locals doing their daily shopping.',
              meta: '📍 Ameyoko, Ueno, Taito-ku · 💰 ¥1,000-1,800/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Akihabara — Electric Town',
              description: 'The world capital of anime, manga, retro gaming, and electronics. Multi-floor arcades where you can play crane games and retro classics. Anime merchandise shops piled floor-to-ceiling. If anyone in your group is remotely into gaming or anime, this is heaven. Even if not, the sensory overload is worth 30 minutes just to experience.',
              details: [
                '📍 Akihabara, Chiyoda-ku (5 min from Ueno by JR Yamanote line)',
                '💡 Best stores: Yodobashi Camera (top floor has incredible views + everything electronic), Super Potato (retro games), Animate (anime merch)',
                '🕹️ Try a round at Taito Station arcade — UFO catcher machines are addictive',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kanda Yabu Soba',
              description: 'One of Tokyo\'s most storied soba restaurants, operating since 1880. Light, elegant handmade buckwheat noodles in dashi broth — the opposite of ramen\'s richness. A Tokyo dining institution.',
              meta: '📍 2-10 Kanda Awajicho, Chiyoda-ku · 💰 ¥1,500-2,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🌸 After dinner, return to Ueno Park for yozakura — the illuminated cherry blossoms along the main path are lit until 8pm during peak season.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — iconic Thunder Gate and Nakamise-dori' },
        { lat: 35.7107, lng: 139.8013, label: 'Sumida Park', num: 2, cat: 'attraction', desc: '400 cherry trees along Sumida River with Skytree views' },
        { lat: 35.7059, lng: 139.7743, label: 'Pelican Café', num: 3, cat: 'restaurant', desc: 'Legendary 1942 bakery — thick-cut toast and coffee' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 4, cat: 'attraction', desc: 'Prime hanami with 1,000+ cherry trees — yozakura at night' },
        { lat: 35.7085, lng: 139.7745, label: 'Ameyoko Market', num: 5, cat: 'restaurant', desc: 'Bustling market street — seafood, yakitori, cheap beer' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 6, cat: 'attraction', desc: 'Anime, gaming, electronics — Tokyo\'s electric wonderland' },
        { lat: 35.6956, lng: 139.7741, label: 'Kanda Yabu Soba', num: 7, cat: 'restaurant', desc: 'Historic soba restaurant operating since 1880' },
      ],
    },

    // DAY 3 — Meiji Shrine, Harajuku, Shibuya, Shinjuku Gyoen
    {
      num: 3,
      date: 'Mar 18',
      title: 'Sacred Forests, Street Style & Tokyo\'s Best Garden',
      description: 'From the ancient Meiji Shrine forest to Harajuku\'s kawaii chaos, the zen of Shinjuku Gyoen\'s cherry blossoms, and Shibuya\'s famous scramble crossing — a perfect Tokyo day.',
      neighborhoods: 'Harajuku · Shibuya · Shinjuku',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'Walk through the towering torii gate into a 170-acre forested sanctuary dedicated to Emperor Meiji and Empress Shoken. The path through ancient trees is meditative and completely removed from the city\'s buzz — despite being surrounded by Harajuku and Shibuya. Write a wish on an ema wooden prayer tablet, or watch shrine priests in white robes conduct morning rituals.',
              details: [
                '📍 1-1 Yoyogikamizonocho, Shibuya-ku · Free',
                '🕐 Sunrise to sunset',
                '💡 Buy an ema tablet (¥500) at the inner shrine and write your wish — a meaningful ritual',
                '💡 Arrive by 8am on weekdays for the quietest, most atmospheric visit',
              ],
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Step from ancient forest into Tokyo\'s most colorful, chaotic youth culture zone. Takeshita Street is packed with crepe shops, kawaii fashion, and cosplay teens. Wander the backstreets of Ura-Harajuku (behind Omotesando Hills) for more grown-up vintage boutiques and international designer shops.',
              details: [
                '📍 Takeshita-dori, Jingumae, Shibuya-ku',
                '💡 Best Harajuku crepes: Marion Crepes (strawberry and cream, ¥500) or Totti Candy Factory (rainbow cotton candy)',
                '🛍️ Omotesando Blvd is Tokyo\'s Champs-Élysées — beautiful tree-lined avenue with high-end shops',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Genki Sushi (Harajuku)',
              description: 'Modern conveyor belt sushi where you order via tablet and dishes arrive by mini shinkansen train. Fresh, fast, family-friendly, and affordable. Perfect for the pickiest eaters in your group.',
              meta: '📍 6-7-18 Jingumae, Shibuya-ku · 💰 ¥1,200-2,000/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden 🌸',
              description: 'Tokyo\'s most beautiful park — 1,000+ cherry trees across Japanese formal, English landscape, and French formal gardens. Alcohol is banned, making it a calmer, more family-friendly alternative to Ueno. The Japanese Garden section has weeping sakura that bloom slightly later than the Somei Yoshino. Bring a picnic and spend 2 hours here.',
              details: [
                '📍 11 Naitomachi, Shinjuku-ku · 💰 ¥500/person',
                '🕐 9am-5:30pm · Closed Mondays',
                '🌸 Enter from the Shinjuku Gate — the main lawn\'s sakura are the star, but walk to the Japanese Garden for weeping cherry magic',
                '📸 The reflection pond in the Japanese Garden at golden hour is the money shot',
              ],
            },
            {
              title: 'Shibuya Crossing & Surroundings',
              description: 'The world\'s busiest pedestrian crossing — a genuine Tokyo spectacle. Watch from the Starbucks or Mag\'s Park balcony above the crossing, then plunge into it yourself. Nearby: Shibuya Sky rooftop observation deck for an aerial view of the city, and the Hachiko statue (loyal dog memorial) outside the station.',
              details: [
                '📍 Shibuya Crossing, Shibuya-ku',
                '💡 Observe first from Starbucks 2F (arrive 15 min early to grab a window seat), then cross yourself',
                '🛗 Shibuya Sky (rooftop): ¥2,000/person, stunning 360° views from 230m',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Fuunji Tsukemen',
              description: 'One of Tokyo\'s most acclaimed tsukemen (dipping ramen) restaurants — thick, rich fish-and-pork broth that you dip fat, chewy noodles into. A revelatory ramen experience, just 5 minutes from Shinjuku Station.',
              meta: '📍 2-14-3 Yoyogi, Shibuya-ku · 💰 ¥900-1,200/person · Cash only · Expect short queue',
            },
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, explore Shinjuku\'s Kabukicho one more time — or rest up. Day 4 is Hakone and you want energy for the mountain air.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Ancient shrine in 170-acre forest — peaceful morning ritual' },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Harajuku\'s iconic kawaii youth fashion street' },
        { lat: 35.6590, lng: 139.7016, label: 'Genki Sushi Harajuku', num: 3, cat: 'restaurant', desc: 'Conveyor belt sushi with tablet ordering and mini-train delivery' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 4, cat: 'attraction', desc: '1,000+ cherry trees in Tokyo\'s most beautiful garden' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 5, cat: 'attraction', desc: 'World\'s busiest pedestrian scramble — Tokyo\'s ultimate spectacle' },
        { lat: 35.6580, lng: 139.7016, label: 'Hachiko Statue', num: 6, cat: 'attraction', desc: 'Famous loyal dog memorial at Shibuya Station' },
        { lat: 35.6836, lng: 139.7020, label: 'Fuunji Tsukemen', num: 7, cat: 'restaurant', desc: 'Top-ranked tsukemen dipping ramen near Shinjuku' },
      ],
    },

    // DAY 4 — Hakone Day Trip (Mt Fuji views + Onsen)
    {
      num: 4,
      date: 'Mar 19',
      title: 'Hakone: Mt. Fuji, Volcanic Valleys & Hot Springs',
      description: 'A day trip from Tokyo into the mountains for jaw-dropping Mt. Fuji views (weather permitting), volcanic steam vents, black eggs, and a real outdoor onsen — the perfect adventure-meets-relaxation day.',
      neighborhoods: 'Hakone · Odawara',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Romancecar to Hakone',
              description: 'Take the Romancecar express train from Shinjuku to Hakone-Yumoto (85 min, ¥2,470 one-way). Unlike shinkansen, the Romancecar has a panoramic front window — sit in the first car for views of the mountains as you approach. The Hakone Free Pass (¥5,000-6,100 from Shinjuku) covers the round-trip Romancecar plus all transport in Hakone (ropeway, bus, boat, train).',
              details: [
                '🚆 Odakyu Romancecar from Shinjuku Station · ¥2,470 one-way or included in Hakone Free Pass',
                '💡 The Hakone Free Pass is worth it — covers ropeway, lake boat, and local buses all day',
                '📅 Book Romancecar seats online 1-2 days in advance, especially on weekends',
              ],
            },
            {
              title: 'Owakudani Volcanic Valley',
              description: 'Take the ropeway up to Owakudani — an active volcanic zone with sulfurous steam vents, boiling mud pools, and the famous kuro-tamago (black eggs hard-boiled in hot spring water, said to add 7 years to your life). On clear mornings, Mt. Fuji towers beyond the steam — a genuinely surreal landscape.',
              details: [
                '📍 Owakudani, Hakone-machi, Ashigarashimo District',
                '💰 Included in Hakone Free Pass',
                '🥚 Black eggs: ¥500 for 5 eggs — eat one at the summit for the longevity bonus',
                '⚠️ Ropeway occasionally closes due to volcanic activity — check the day before',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Konbini or Hakone-Yumoto Station',
              description: 'Grab breakfast from a 7-Eleven near your hotel before the early train, or from the station shops at Hakone-Yumoto upon arrival.',
              meta: '💰 ¥500-800/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🗻 Mt. Fuji is visible only about 30% of the year. Morning is your best chance — clouds build up by afternoon. If you see Fuji, drop everything and stare for a while. It\'s earned.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Ashi Boat Cruise',
              description: 'From Togendai (bottom of the ropeway), board the Hakone Sightseeing Cruise across Lake Ashi — a volcanic caldera lake with Fuji looming on the far side on clear days. Pirate-ship-themed boats add a fun twist. Cross to Hakone-machi for views of the historic torii gate rising from the lake\'s surface.',
              details: [
                '⛵ Togendai → Hakone-machi (25 min) or → Moto-Hakone (30 min)',
                '💰 Included in Hakone Free Pass',
                '📍 Hakone Shrine Torii: 80-1 Motohakone, Hakone-machi — walk 5 min from Moto-Hakone pier',
              ],
            },
            {
              title: 'Hakone Open Air Museum (Optional)',
              description: 'Japan\'s first outdoor art museum, set in a stunning mountain valley with Picasso pavilion, Henry Moore sculptures, and a foot-bath hot spring path. Excellent for families. Allow 2 hours.',
              details: [
                '📍 1121 Ninotaira, Hakone-machi · 💰 ¥1,800/person',
                '🕐 9am-5pm',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Naraya Café',
              description: 'A charming café built around an old bathhouse near Hakone-Yumoto, with foot-baths you can soak your feet in while eating. Try the hakone-mochi sweet and local black sesame ice cream.',
              meta: '📍 2-397 Yumoto, Hakone-machi · 💰 ¥800-1,200/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Onsen at Tenzan Tojikyō (天山湯治郷)',
              description: 'One of Hakone\'s best outdoor onsen (rotenburo) experiences — set in a forested riverside location with several open-air baths at different temperatures, plus steam rooms and indoor pools. The crisp mountain air and sound of the river make it magical. Note: no tattoo policy at this onsen.',
              details: [
                '📍 208 Yumoto-chaya, Hakone-machi · 💰 ¥1,400/person',
                '🕐 9am-10pm · No tattoos',
                '♨️ Bring or rent a towel. Nude bathing, separate areas for men and women.',
                '💡 A sake vending machine is on site — sip hot sake while sitting in the outdoor bath. Peak Japan moment.',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ramen at Hakone-Yumoto Station',
              description: 'Hakone-Yumoto station has great ramen stalls and casual restaurants. Refuel before the return Romancecar to Shinjuku.',
              meta: '💰 ¥900-1,200/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🚆 Return Romancecar from Hakone-Yumoto to Shinjuku runs until around 9:30pm. Book the return seat when you book the morning departure.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.2324, lng: 139.0573, label: 'Owakudani', num: 1, cat: 'attraction', desc: 'Active volcanic valley — black eggs, sulfur steam, Mt. Fuji views' },
        { lat: 35.2002, lng: 139.0183, label: 'Lake Ashi Boat Cruise', num: 2, cat: 'attraction', desc: 'Pirate-ship cruise across volcanic caldera lake' },
        { lat: 35.1967, lng: 139.0256, label: 'Hakone Shrine Torii', num: 3, cat: 'attraction', desc: 'Iconic torii gate rising from Lake Ashi' },
        { lat: 35.2509, lng: 139.0467, label: 'Hakone Open Air Museum', num: 4, cat: 'attraction', desc: 'Mountain-valley outdoor art museum with Picasso pavilion' },
        { lat: 35.2334, lng: 139.1011, label: 'Naraya Café', num: 5, cat: 'restaurant', desc: 'Foot-bath café with black sesame ice cream' },
        { lat: 35.2301, lng: 139.1018, label: 'Tenzan Onsen', num: 6, cat: 'attraction', desc: 'Riverside outdoor hot springs — sake vending, mountain air' },
      ],
    },

    // DAY 5 — Tokyo → Kyoto, Gion evening
    {
      num: 5,
      date: 'Mar 20',
      title: 'Shinkansen South: Tokyo to Kyoto — Ancient Capital Arrival',
      description: 'Activate your JR Pass and board the bullet train south. Arrive in Japan\'s ancient capital as the cherry blossoms hit peak bloom, and ease into Kyoto\'s atmosphere with an evening walk through Gion.',
      neighborhoods: 'Kyoto Station · Gion · Pontocho',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Check Out & Shinkansen to Kyoto',
              description: 'Activate your 7-day JR Pass at Tokyo Station\'s JR ticket window. Board the Nozomi or Hikari shinkansen to Kyoto (2 hr 15 min, covered by JR Pass). On clear days, Mt. Fuji is visible from the right side of the train around Shizuoka — sit on the right (window seats D or E) for the best views.',
              details: [
                '🚅 Tokyo → Kyoto: ~2h15m on Nozomi, 2h40m on Hikari (both JR Pass eligible)',
                '💡 Sit on the right side of the train (seats D/E) for Mt. Fuji views around 40-50 minutes into the journey',
                '💡 Luggage forward service: send your big bags to Kyoto accommodation the previous day (¥2,500-3,500)',
              ],
            },
            {
              title: 'Check In & Orientation',
              description: 'Drop bags at your Kyoto accommodation. Kyoto\'s best neighborhoods to stay: Gion (most atmospheric), Shimogyo-ku near the station (convenient), or Kawaramachi (central for nightlife). Walk around the block to orient yourself.',
              details: [
                '💡 Pick up a day bus pass (¥700) from Kyoto Station bus terminal for unlimited city bus travel',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Lunch (on the train)',
              name: 'Shinkansen Ekiben',
              description: 'Buy an ekiben (station bento box) from the Gransta market at Tokyo Station before boarding — this is a Japanese tradition. Look for the makunouchi bento with assorted pickles, tamagoyaki, salmon, rice, and soba. Best train meal you\'ll ever have.',
              meta: '📍 Tokyo Station Gransta · 💰 ¥900-1,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🚅 The Nozomi shinkansen is fastest (Tokyo → Kyoto in 2h15m) but note: regular JR Pass holders cannot book Nozomi seats. Use the Hikari instead (2h40m) — nearly as fast, and fully covered.' },
          ],
        },
        {
          label: 'Afternoon & Evening',
          activities: [
            {
              title: 'Gion District Evening Walk',
              description: 'Kyoto\'s most famous district is best experienced in the early evening, when the lanterns glow, geisha (geiko) and apprentices (maiko) move silently between teahouses, and the wooden machiya townhouses cast long shadows. Walk down Hanamikoji-dori — the main Gion street — and explore the quieter lanes like Shinmonzen-dori and Shimbashi-dori.',
              details: [
                '📍 Gion, Higashiyama, Kyoto',
                '💡 Best times: 5:30-8pm when maiko begin their evening rounds',
                '📸 Shimbashi area (near Tatsumi Bridge) is the most photogenic — old tea houses with cherry blossoms and canal reflections',
                '⚠️ Do not chase or grab geisha/maiko for photos. Watch respectfully from a distance.',
              ],
            },
            {
              title: 'Nishiki Market "Kyoto\'s Kitchen"',
              description: 'A narrow, 400-meter covered arcade market lined with over 100 vendors selling Kyoto\'s distinctive foods: pickled vegetables (tsukemono), handmade tofu, fresh yuba, matcha-covered sweets, and grilled skewers. The perfect introduction to Kyoto cuisine.',
              details: [
                '📍 Nishiki-koji, Nakagyo-ku · Most shops open 9am-6pm',
                '🥢 Try: yudofu (hot tofu), matcha daifuku mochi, tako tamago (octopus with quail egg on a stick)',
              ],
            },
            {
              title: 'Pontocho Alley Dinner',
              description: 'A narrow lantern-lit alleyway between the Kamogawa River and Kawaramachi that\'s lined with some of Kyoto\'s best restaurants — from casual izakayas to high-end kaiseki. In warm months, restaurants extend tatami platforms (yuka) out over the river — a unique Kyoto dining experience.',
              details: [
                '📍 Pontocho, Nakagyo-ku (runs parallel to the Kamogawa River)',
                '💡 Walk the full length first to see all options before choosing — plenty of spots welcome walk-ins',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kichi Kichi Omurice (きちきち)',
              description: 'Kyoto\'s most famous omurice restaurant, run by the flamboyant and talented Chef Motokichi Yukimura. He slices open a perfectly oval egg omelette tableside in a dramatic showmanship performance. The meal becomes pure theater. Book weeks in advance (or queue before opening).',
              meta: '📍 Rokkaku-dori, Nakagyo-ku · 💰 ¥2,800/person · Reservations essential',
            },
          ],
          tips: [
            { type: 'tip', text: '🌸 Walk along the Kamogawa River banks at dusk — the cherry trees along the riverside promenade are illuminated at night, and locals sit out drinking convenience store beers under the blossoms. Pure Kyoto magic.' },
          ],
        },
      ],
      mapPins: [
        { lat: 34.9860, lng: 135.7584, label: 'Kyoto Station', num: 1, cat: 'transport', desc: 'Your gateway to ancient Kyoto — activate JR Pass here' },
        { lat: 35.0034, lng: 135.7762, label: 'Hanamikoji-dori (Gion)', num: 2, cat: 'attraction', desc: 'Kyoto\'s most famous street — maiko, lanterns, machiya teahouses' },
        { lat: 35.0052, lng: 135.7693, label: 'Nishiki Market', num: 3, cat: 'restaurant', desc: 'Kyoto\'s Kitchen — 400m of local foods, pickles, tofu, and sweets' },
        { lat: 35.0075, lng: 135.7691, label: 'Pontocho Alley', num: 4, cat: 'restaurant', desc: 'Lantern-lit alley with riverside kaiseki and izakayas' },
        { lat: 35.0060, lng: 135.7756, label: 'Tatsumi Bridge / Shimbashi', num: 5, cat: 'attraction', desc: 'Most photogenic Gion canal scene — cherry blossoms + lanterns' },
        { lat: 35.0050, lng: 135.7681, label: 'Kichi Kichi Omurice', num: 6, cat: 'restaurant', desc: 'Famous theatrical omurice — egg sliced tableside by Chef Motokichi' },
      ],
    },

    // DAY 6 — Fushimi Inari, Philosopher's Path
    {
      num: 6,
      date: 'Mar 21',
      title: 'Thousand Torii Gates & the Philosopher\'s Path in Bloom',
      description: 'An early rise earns you nearly empty torii gates at one of Japan\'s most iconic shrines. Afternoon brings the cherry blossom-lined Philosopher\'s Path and the Higashiyama heritage walking district.',
      neighborhoods: 'Fushimi · Higashiyama · Okazaki',
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Fushimi Inari-Taisha at Sunrise',
              description: 'Kyoto\'s most iconic sight — thousands of vermillion torii gates winding up a mountain for 4km, forming tunnels of red. The lower gates are photographed by millions; the upper mountain sees almost no one, especially at dawn. Hike all the way to the top summit for panoramic views of Kyoto below. Allow 2-3 hours for the full loop.',
              details: [
                '📍 68 Fukakusa Yabunouchicho, Fushimi-ku',
                '🕐 Always open · Free',
                '🚃 Take JR Nara Line from Kyoto Station to Inari Station (5 min) — covered by JR Pass',
                '💡 Arrive at 6am to be ahead of tour groups — the lower gates are empty at dawn and filled by 8am',
                '🦊 Foxes (kitsune) are the shrine messengers — spot their stone statues throughout the grounds',
                '⛰️ The full hike to the top and back: 2h30m to 3h. Even half-way up Yotsutsuji intersection has great views and takes 45 min.',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Early Breakfast',
              name: 'Konbini before departure',
              description: 'Grab onigiri, a coffee, and a triangle sandwich from a convenience store before the 6am train — you\'ll want food before the mountain hike.',
              meta: '💰 ¥400-600/person',
            },
          ],
          tips: [
            { type: 'tip', text: '📸 The classic torii gate photo: crouch low and shoot toward the light. The reflection of red gates on the worn stone path is the real magic.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Philosopher\'s Path (Tetsugaku-no-michi) 🌸',
              description: 'Kyoto\'s most beloved cherry blossom walk — a 2km stone path running alongside the Shishigatani canal, lined with 400+ Somei Yoshino cherry trees. Philosopher Nishida Kitaro walked this path daily in contemplation. In late March, the trees form a pink tunnel overhead and petals drift into the canal below. Walk from Nanzenji (south) to Ginkaku-ji (north).',
              details: [
                '📍 Start at Nanzenji Temple, walk north to Ginkaku-ji (Silver Pavilion)',
                '🌸 Best section is the middle stretch near Otoyo Shrine — the canal reflections with petals are stunning',
                '🐱 Small cat cafés and craft shops dot the path — peek inside',
                '⏱️ Allow 1-1.5 hours for the full walk including photo stops',
              ],
            },
            {
              title: 'Nanzenji Temple Complex',
              description: 'At the southern end of the Philosopher\'s Path, Nanzenji is one of Japan\'s most important Zen temples, set against the forested Higashiyama mountains. Walk through the towering Sanmon Gate (¥600 to climb), and don\'t miss the bizarre aqueduct — a Roman-style brick arch right in the middle of the temple grounds, built in 1890 to channel water from Lake Biwa.',
              details: [
                '📍 86 Fukuchicho, Nanzenji, Sakyo-ku',
                '💰 Grounds free · Sub-temples ¥500-600 each',
                '🌸 The temple garden has early-blooming cherry varieties in late March',
              ],
            },
            {
              title: 'Ginkaku-ji Silver Pavilion',
              description: 'The northern terminus of the Philosopher\'s Path. Despite the name, this "Silver Pavilion" was never actually covered in silver — but the Zen garden with its meticulously raked sand cone (kogetsudai) and the surrounding cedar forest make it one of Kyoto\'s most beautiful temple grounds.',
              details: [
                '📍 2 Ginkakujicho, Sakyo-ku · 💰 ¥500/person',
                '🕐 8:30am-5pm (until 5:30 in spring)',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Omen Noodles (おめん)',
              description: 'A beloved Kyoto institution since 1969, specializing in thick udon noodles served with a seasonal array of toppings — sesame, green onion, mushrooms — in a light dashi broth. Located right on the Philosopher\'s Path. Warm, comforting, unpretentious.',
              meta: '📍 74 Ishibashicho, Okazaki, Sakyo-ku · 💰 ¥1,000-1,400/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Higashiyama Heritage District Walk',
              description: 'Stroll south from Gion through the preserved machiya townhouse streets of Higashiyama — some of Kyoto\'s most evocative scenery. Key stops: Yasaka Shrine (lit up at dusk), Maruyama Park (Kyoto\'s most famous hanami park with a weeping cherry tree illuminated at night), the cobblestone lanes of Sannenzaka and Ninenzaka, and finally the wooden stage of Kiyomizu-dera temple.',
              details: [
                '📍 Higashiyama, Kyoto (walk from Maruyama Park south to Kiyomizudera)',
                '🌸 Maruyama Park\'s lone weeping cherry tree (illuminated 6-9pm) is one of Kyoto\'s most iconic images',
                '🕐 Kiyomizudera closes at 6pm (later during spring season) — check website',
                '💡 The Sannenzaka and Ninenzaka lanes are lined with traditional shops selling Kyoto ceramics, matcha sweets, and lacquerware',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Misoka-An Kawamichiya (みそか庵 川道屋)',
              description: 'A 300-year-old Kyoto soba restaurant near Nijo Castle, serving buckwheat noodles in the refined Kyoto style. The soba seiro with soba-yu (hot cooking water mixed with remaining dip sauce) is a ritual. One of the most authentic traditional dining experiences in Japan.',
              meta: '📍 Fuyacho-dori, Nakagyo-ku · 💰 ¥1,500-2,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🌸 Maruyama Park at night during cherry blossom season is essential Kyoto. The great weeping sakura (shidarezakura) is illuminated 6-9pm — one of Japan\'s most famous images. Stalls sell sake and beer — join the hanami party.' },
          ],
        },
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari-Taisha', num: 1, cat: 'attraction', desc: 'Thousands of torii gates winding up a mountain — go at sunrise' },
        { lat: 35.0116, lng: 135.7984, label: 'Nanzenji Temple', num: 2, cat: 'attraction', desc: 'Zen temple with towering gate and Roman-style aqueduct' },
        { lat: 35.0148, lng: 135.7964, label: 'Philosopher\'s Path', num: 3, cat: 'attraction', desc: '2km canal walk under 400 cherry trees — peak hanami' },
        { lat: 35.0166, lng: 135.7986, label: 'Omen Noodles', num: 4, cat: 'restaurant', desc: 'Beloved 1969 udon spot on the Philosopher\'s Path' },
        { lat: 35.0168, lng: 135.7994, label: 'Ginkaku-ji Silver Pavilion', num: 5, cat: 'attraction', desc: 'Zen garden with sand cone — forest-framed northern Kyoto' },
        { lat: 35.0034, lng: 135.7842, label: 'Maruyama Park', num: 6, cat: 'attraction', desc: 'Kyoto\'s #1 hanami park — weeping cherry illuminated at night' },
        { lat: 34.9948, lng: 135.7850, label: 'Kiyomizudera Temple', num: 7, cat: 'attraction', desc: 'Iconic wooden stage jutting from the mountainside' },
        { lat: 35.0002, lng: 135.7830, label: 'Sannenzaka & Ninenzaka', num: 8, cat: 'attraction', desc: 'Cobblestone heritage lanes with traditional Kyoto shops' },
      ],
    },

    // DAY 7 — Arashiyama + Bamboo Grove
    {
      num: 7,
      date: 'Mar 22',
      title: 'Arashiyama: Bamboo Groves, Monkey Mountains & River Temples',
      description: 'Kyoto\'s western mountains hold some of Japan\'s most beautiful landscapes — a towering bamboo grove, a hillside monkey park, floating temples, and the bamboo-surrounded Jojakko-ji that feels like another world.',
      neighborhoods: 'Arashiyama · Sagano',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'One of Japan\'s most otherworldly sights — a forest of towering green bamboo soaring 20+ meters overhead, swaying in the wind with an eerie, hollow sound. The light filtering through the bamboo creates constantly shifting patterns. The main grove is a 5-minute walk; the side paths extend much further into quieter forest.',
              details: [
                '📍 Ukyo-ku, Kyoto (walk 5 min north from Arashiyama Station)',
                '🕐 Always open · Free',
                '💡 Arrive by 7am for near-empty bamboo paths — crowds arrive by 9am',
                '🚃 Arashiyama: Take the JR Sagano Line from Kyoto Station to Saga-Arashiyama Station (15 min, JR Pass)',
              ],
            },
            {
              title: 'Tenryu-ji Temple & Garden',
              description: 'A UNESCO World Heritage temple right at the edge of the bamboo grove. Its 14th-century garden — considered one of Japan\'s finest — uses "borrowed scenery" (shakkei) to incorporate the Arashiyama mountains into the composition. Cherry trees bloom within the garden, reflected in the mirror-still pond.',
              details: [
                '📍 68 Sagatenryuji Susukinobabacho, Ukyo-ku · 💰 ¥500/person (garden)',
                '🕐 8:30am-5:30pm',
                '🌸 In-garden cherry trees bloom mid-to-late March — stunning against the white-wall backdrop',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Arabica Kyoto (% Arabica)',
              description: 'One of Japan\'s most Instagram-famous coffee shops, with a location in Arashiyama. A minimalist glass-and-steel café with views of the mountains. Their espresso is outstanding. Arrive early to beat the line.',
              meta: '📍 3-47 Sagatenryuji Susukinobabacho, Ukyo-ku · 💰 ¥600-900/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Mid-Morning',
          activities: [
            {
              title: 'Arashiyama Monkey Park (Iwatayama)',
              description: 'Hike 15 minutes up a steep trail to a mountain summit where 120+ wild Japanese macaques roam freely around you. Surreal experience — you\'re in the cage (to protect the monkeys), while the monkeys roam outside. Panoramic views of Kyoto spread below the monkey mountain.',
              details: [
                '📍 1 Genrokuzancho, Arashiyama, Nishikyo-ku · 💰 ¥600/person',
                '🕐 9am-5pm (4:30pm entry cutoff)',
                '🐒 Buy monkey food inside (¥100) and feed them through the wire mesh. Do NOT bring food in your bag — they will steal it.',
              ],
            },
            {
              title: 'Jojakko-ji Temple (常寂光寺)',
              description: 'An off-the-beaten-path temple hidden up stone steps behind the bamboo grove. Moss-covered stone walls, thatched gate, a multi-story pagoda peeking above maple trees. Utterly peaceful and beautiful in cherry blossom season when blossoms frame the pagoda.',
              details: [
                '📍 3 Oguracho, Sagano, Ukyo-ku · 💰 ¥500/person',
                '💡 Far fewer tourists than the main bamboo grove — take your time here',
              ],
            },
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '🎋 The bamboo grove in Arashiyama extends far beyond the famous 5-minute main stretch. Walk deeper on the side paths toward Jojakko-ji and Nonomiya Shrine for complete solitude.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Togetsukyo Bridge & Riverside Walk',
              description: 'Arashiyama\'s iconic "Moon Crossing Bridge" has been photographed with cherry blossoms for centuries. Walk across, then stroll the riverside past cherry trees, boat rental docks, and the Oi River. Rent a rowboat (¥600-1,500/30 min) and drift under the blossoms.',
              details: [
                '📍 Togetsukyo Bridge, Arashiyama',
                '💡 The classic shot: bridge framed by cherry blossoms with mountains behind — best from the south riverbank looking northwest',
                '🚣 Rowboat rental: near Togetsukyo Bridge, ¥600 for 30 minutes',
              ],
            },
            {
              title: 'Sagano Romantic Train (Sagano Torokko)',
              description: 'A scenic open-air railway running through the Hozugawa river gorge — steep canyon walls, rushing river, and forest. A 25-minute ride on the retro Torokko train with mountain scenery. Then continue by boat down the Hozugawa River (Hozugawa Kudari) to Arashiyama — an epic canyon descent.',
              details: [
                '🚂 Torokko train: ¥880/person one-way · Book at Torokko Saga Station',
                '🚣 Hozugawa River descent (boat): ¥4,100/person · March season · 2 hours',
                '💡 If time is tight, just take the Torokko train one-way and return by bus',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Yoshida-ya Tofu Cuisine',
              description: 'Kyoto is famous for its tofu cuisine (kyo-ryori), and Arashiyama\'s riverside restaurants specialize in seasonal tofu set meals (tofu kaiseki). Try the silken yudofu (tofu simmered in dashi) with yuba, pickles, and rice — a surprisingly satisfying and elegant meal.',
              meta: '📍 Arashiyama riverside area · 💰 ¥1,500-2,500/person',
            },
            {
              type: '🍽️ Dinner',
              name: 'Izuju Sushi (いづ重)',
              description: 'A Kyoto institution since 1781 specializing in saba-zushi (mackerel pressed sushi) — Kyoto\'s distinctive style of sushi, pressed into a wooden mold. Beautifully presented, mild and vinegary. Order the take-out box and enjoy near Gion.',
              meta: '📍 292-1 Gionmachi Kitagawa, Higashiyama-ku · 💰 ¥1,500-2,500',
            },
          ],
          tips: [
            { type: 'tip', text: '⏰ Arashiyama is easily a full day. Prioritize: bamboo at sunrise (must), Monkey Park (morning energy), Togetsukyo Bridge + rowboat (afternoon). Drop Sagano train if time runs short.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.0173, lng: 135.6716, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering green bamboo — go at 7am before the crowds arrive' },
        { lat: 35.0158, lng: 135.6737, label: 'Tenryu-ji Temple', num: 2, cat: 'attraction', desc: 'UNESCO garden with cherry trees and mountain borrowed scenery' },
        { lat: 35.0157, lng: 135.6734, label: '% Arabica Arashiyama', num: 3, cat: 'restaurant', desc: 'Famous minimalist coffee with mountain views' },
        { lat: 35.0092, lng: 135.6755, label: 'Arashiyama Monkey Park', num: 4, cat: 'attraction', desc: '120+ wild macaques with panoramic Kyoto views from the summit' },
        { lat: 35.0183, lng: 135.6705, label: 'Jojakko-ji Temple', num: 5, cat: 'attraction', desc: 'Hidden moss-covered temple with pagoda — blossoms in March' },
        { lat: 35.0129, lng: 135.6771, label: 'Togetsukyo Bridge', num: 6, cat: 'attraction', desc: 'Iconic Moon Crossing Bridge framed by cherry blossoms' },
        { lat: 35.0168, lng: 135.6742, label: 'Torokko Saga Station', num: 7, cat: 'transport', desc: 'Board the scenic canyon railway here' },
      ],
    },

    // DAY 8 — Nara Day Trip
    {
      num: 8,
      date: 'Mar 23',
      title: 'Nara: Ancient Deer, Giant Buddhas & Sacred Forest',
      description: 'A day trip to Japan\'s first ancient capital — where over 1,200 wild sika deer roam freely through the park as divine messengers, a colossal bronze Buddha sits in the world\'s largest wooden hall, and cherry blossoms carpet the surrounding hills.',
      neighborhoods: 'Nara Park · Naramachi',
      timeBlocks: [
        {
          label: 'Getting There',
          activities: [
            {
              title: 'Kyoto → Nara (JR Nara Line)',
              description: 'Take the JR Nara Line from Kyoto Station to JR Nara Station (45 min on Rapid, covered by JR Pass). Nara is a compact, walkable city — most major sights are within 30 minutes\' walk from the station.',
              details: [
                '🚃 JR Nara Line: Kyoto → Nara, 45 min on Rapid (JR Pass)',
                '💡 Alternatively, the Kintetsu-Nara Limited Express is faster (35 min) but NOT covered by JR Pass',
                '🗺️ Get the Nara Park map at the Tourist Info Center just outside Kintetsu Nara Station',
              ],
            },
          ],
          meals: [],
          tips: [],
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nara Deer Park',
              description: 'Over 1,200 wild sika deer roam freely through Nara Park, protected as divine messengers of the Kasuga Taisha shrine for 1,300 years. Buy shika-senbei deer crackers (¥200/bundle) from roaming vendors and feed them directly — the deer will bow (actually just their way of demanding more crackers), follow you, and occasionally be pushy. It\'s chaotic, hilarious, and utterly magical.',
              details: [
                '📍 Nara Park, Nara City · Always open · Free',
                '🦌 Buy deer crackers from the orange-vested vendors in the park (¥200)',
                '💡 The deer are wild — they may headbutt you for crackers. Keep crackers hidden until ready to feed. Never tease them.',
                '🌸 Late March: cherry trees blooming throughout the park turn it into a pink deer wonderland',
              ],
            },
            {
              title: 'Todai-ji Temple — Great Buddha',
              description: 'The world\'s largest wooden building houses Daibutsu — a 15-meter-tall bronze Buddha weighing 500 tons, cast in 749 AD. You\'ll feel small standing before it. Look for the pillar with a hole at its base — locals believe squeezing through it (same size as the Buddha\'s nostril) grants enlightenment. The temple deer congregate at the entrance.',
              details: [
                '📍 406-1 Zoshicho, Nara · 💰 ¥600/person',
                '🕐 7:30am-5:30pm (Mar-Oct)',
                '💡 The pillar hole: children easily fit, adults can try — it\'s about 37cm x 37cm. Worth attempting.',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mizuya Chaya (水谷茶屋)',
              description: 'A thatched-roof tea house sitting beside a stream in Nara Park, serving simple but delicious traditional Japanese sweets, matcha, and light meals. One of Nara\'s most atmospheric spots — deer wander past the windows.',
              meta: '📍 Kasugano-cho, Nara Park · 💰 ¥800-1,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🦌 The "bowing" deer are not actually being polite — they\'ve learned it gets them food faster. Bow back. It feels right.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Grand Shrine',
              description: 'One of Japan\'s most ancient and important Shinto shrines, founded in 768 AD and rebuilt every 20 years in the traditional style. Over 3,000 bronze and stone lanterns line the approaches and hang in the corridors — when all are lit at the Setsubun and Obon festivals, it\'s extraordinary. The surrounding primeval forest of Kasugayama is a World Heritage Site.',
              details: [
                '📍 160 Kasuganocho, Nara · 💰 Grounds free · Inner shrine ¥500',
                '🌿 The Kasugayama Primeval Forest behind the shrine is 130+ hectares of old-growth forest — dramatic hiking trails',
              ],
            },
            {
              title: 'Naramachi Historic District',
              description: 'A preserved merchant quarter with traditional machiya townhouses converted into cafés, craft shops, and small museums. Stroll the quiet lanes, visit the Naramachi Koshi-no-ie (a restored merchant house from the Meiji period), and browse the craft shops for Nara souvenirs — ink sticks, deer-shaped everything, and kakinoha sushi.',
              details: [
                '📍 Naramachi, Nara City (south of Sarusawa Pond)',
                '💡 Try kakinoha-zushi (sushi wrapped in persimmon leaves, pressed overnight) — Nara\'s most distinctive food',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Late Lunch / Snacks',
              name: 'Naramachi Café Crawl',
              description: 'Naramachi has excellent small cafés and craft beer spots. Stop in at any of the converted machiya cafés for matcha soft serve, kakigori (shaved ice), or coffee before returning to Kyoto.',
              meta: '💰 ¥400-900/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🌸 Return from Nara via Kyoto in the late afternoon. If you\'re near Gion or the Kamogawa, the evening cherry blossoms and riverside lanterns make the perfect end to a perfect day.' },
          ],
        },
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8386, label: 'Nara Deer Park', num: 1, cat: 'attraction', desc: '1,200+ wild divine deer — buy crackers and feed them' },
        { lat: 34.6890, lng: 135.8398, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden hall housing a 15m bronze Buddha' },
        { lat: 34.6868, lng: 135.8432, label: 'Mizuya Chaya', num: 3, cat: 'restaurant', desc: 'Thatched tea house in the park — deer wander past the windows' },
        { lat: 34.6815, lng: 135.8479, label: 'Kasuga Taisha Shrine', num: 4, cat: 'attraction', desc: 'Ancient shrine with 3,000 lanterns and primeval forest' },
        { lat: 34.6790, lng: 135.8361, label: 'Naramachi District', num: 5, cat: 'attraction', desc: 'Preserved merchant quarter — machiya cafés and craft shops' },
        { lat: 34.6849, lng: 135.8327, label: 'JR Nara Station', num: 6, cat: 'transport', desc: 'JR Nara Line — 45 min direct to/from Kyoto' },
      ],
    },

    // DAY 9 — Kyoto → Osaka
    {
      num: 9,
      date: 'Mar 24',
      title: 'Osaka: Street Food Capital — Dotonbori & Kuromon Market',
      description: 'Transfer to Osaka (30 min by shinkansen), Japan\'s most ebullient and food-obsessed city. Osaka\'s motto is kuidaore — "eat until you drop" — and this city takes that seriously. Dotonbori neon, Kuromon\'s fresh seafood, and takoyaki on every corner.',
      neighborhoods: 'Dotonbori · Namba · Shinsaibashi',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kyoto → Osaka (Shinkansen)',
              description: 'Short hop from Kyoto Station to Shin-Osaka (15 min by Hikari shinkansen, JR Pass). From Shin-Osaka, take the Midosuji subway line to Namba or Shinsaibashi. Check into your Osaka accommodation and store your bags.',
              details: [
                '🚅 Kyoto → Shin-Osaka: 15 min on Hikari/Sakura shinkansen (JR Pass)',
                '🚃 Shin-Osaka → Namba: Midosuji subway (15 min, ¥280 on Suica)',
                '💡 The Osaka Amazing Pass (¥2,800/day) covers all subway + entry to Osaka Castle and other attractions',
              ],
            },
            {
              title: 'Kuromon Ichiba Market (黒門市場)',
              description: 'Osaka\'s "kitchen" — a covered 580-meter market with 170+ stalls selling premium seafood, Wagyu beef skewers, fresh oysters, giant prawns, fugu (puffer fish), and Kobe beef sushi. The vendors cook and serve fresh — walk and eat your way through. This is the real Osaka food experience.',
              details: [
                '📍 Kuromon Ichiba, Namba, Osaka',
                '🕐 Most stalls 9am-6pm · Busiest 10am-1pm',
                '💡 Budget ¥2,000-3,000 for a market breakfast/lunch. Try: fresh oysters (¥200 each), tamagoyaki (sweet egg roll, ¥150), giant scallop skewer, wagyu beef nigiri',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Breakfast / Early Lunch',
              name: 'Kuromon Market Crawl',
              description: 'Eat your way through Kuromon — fresh oysters, Wagyu skewers, seafood sashimi, and sweet tamagoyaki. One of the best food experiences in all of Japan.',
              meta: '📍 Kuromon Ichiba, Namba · 💰 ¥2,000-3,000/person',
            },
          ],
          tips: [],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dotonbori & Namba',
              description: 'The heart of Osaka — a canal flanked by towering neon signs, mechanical crabs, and the iconic Glico Running Man. It\'s Japan\'s most photographed urban streetscape. Walk the length of Dotonbori Canal, cross the Ebisu bridge (famous selfie spot), and explore the side streets packed with everything from 500-yen ramen to michelin-starred sushi.',
              details: [
                '📍 Dotonbori, Namba, Osaka',
                '💡 The Glico Running Man sign is best photographed from Ebisubashi Bridge at dusk when the neon is competing with the fading sky',
                '🦀 Don Quijote (discount store) in Dotonbori is 5 floors of everything imaginable — great for gifts',
              ],
            },
            {
              title: 'Shinsaibashi Shopping & Amemura',
              description: 'Osaka\'s main shopping street — Shinsaibashi-suji — is a covered arcade stretching 600 meters with everything from luxury brands to 100-yen shops. A few blocks west, Amerika-mura (Amemura) is Osaka\'s answer to Harajuku — vintage shops, skateboard culture, and American pop culture references.',
              details: [
                '📍 Shinsaibashi-suji, Chuo-ku, Osaka',
                '🛍️ Best Amemura vintage: Flamingo vintage, New Vintage Collection',
              ],
            },
          ],
          meals: [
            {
              type: '🍡 Snack',
              name: 'Takoyaki at Wanaka (わなか)',
              description: 'Osaka invented takoyaki (octopus balls) and Wanaka is one of the city\'s most beloved spots. Eight crispy-outside, molten-inside balls of batter filled with tender octopus, topped with okonomiyaki sauce, mayo, bonito flakes, and green onion. ¥600 for a box of 8.',
              meta: '📍 Shinsaibashi-suji, Chuo-ku · 💰 ¥600 for 8 pieces',
            },
          ],
          tips: [],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori After Dark',
              description: 'Dotonbori transforms at night — the neon reflections on the canal create a cyberpunk dreamscape. The restaurants come fully alive: massive queues at Kani Doraku (mechanical crab), Ichiran ramen, and the legendary Ikinari Steak. Walk the canal walkway (Tombori River Walk) for the best reflections.',
              details: [
                '📍 Tombori River Walk, along Dotonbori Canal',
                '💡 Take the glass-bottom boat cruise (¥900) for canal-level neon views',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Okonomiyaki at Mizuno (美津の)',
              description: 'Osaka-style okonomiyaki (savory pancake) is different from Hiroshima-style — the ingredients are mixed INTO the batter rather than layered. Mizuno has been making Osaka\'s best okonomiyaki since 1945. Order the modanyaki (with yakisoba noodles inside) and mountain potato (yamaimo) version.',
              meta: '📍 1-4-15 Dotonbori, Chuo-ku · 💰 ¥1,500-2,500/person · Expect queue',
            },
          ],
          tips: [
            { type: 'tip', text: '🎰 Osaka has the world\'s highest concentration of pachinko parlors, retro arcades, and UFO catcher machines. Throw a few coins into a retro arcade — it\'s peak Osaka culture.' },
          ],
        },
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5052, label: 'Kuromon Ichiba Market', num: 1, cat: 'restaurant', desc: 'Osaka\'s kitchen — fresh oysters, Wagyu skewers, 170+ stalls' },
        { lat: 34.6687, lng: 135.5003, label: 'Dotonbori Canal', num: 2, cat: 'attraction', desc: 'Neon-lit canal — Glico Man, mechanical crabs, night reflections' },
        { lat: 34.6705, lng: 135.5016, label: 'Ebisubashi Bridge', num: 3, cat: 'attraction', desc: 'The selfie bridge — Glico Man sign framed perfectly' },
        { lat: 34.6729, lng: 135.5005, label: 'Shinsaibashi-suji', num: 4, cat: 'attraction', desc: '600m covered shopping arcade + Amemura vintage district' },
        { lat: 34.6688, lng: 135.5010, label: 'Wanaka Takoyaki', num: 5, cat: 'restaurant', desc: 'Beloved takoyaki spot — crispy outside, molten inside' },
        { lat: 34.6687, lng: 135.5028, label: 'Okonomiyaki Mizuno', num: 6, cat: 'restaurant', desc: 'Osaka\'s best okonomiyaki since 1945 — mixed-style savory pancake' },
      ],
    },

    // DAY 10 — Hiroshima + Miyajima
    {
      num: 10,
      date: 'Mar 25',
      title: 'Hiroshima & Miyajima: Peace, History & the Floating Torii',
      description: 'Japan\'s most sobering and ultimately hopeful destination, followed by one of the country\'s most beautiful sights — a vermillion torii gate rising from the sea at Miyajima island. A day that will move you.',
      neighborhoods: 'Hiroshima · Miyajima Island',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka → Hiroshima (Shinkansen)',
              description: 'Take the Nozomi or Hikari shinkansen from Shin-Osaka to Hiroshima (1h10m, covered by JR Pass). Hiroshima Station is connected to the city\'s tram system.',
              details: [
                '🚅 Shin-Osaka → Hiroshima: 1h10m on Nozomi / 1h30m on Hikari (JR Pass)',
                '💡 Leave Osaka by 7:30-8am to maximize time in Hiroshima',
              ],
            },
            {
              title: 'Peace Memorial Park & Museum',
              description: 'The A-Bomb Dome — the skeletal ruins of the former Industrial Promotion Hall, preserved as it stood after the atomic bombing of August 6, 1945 — is one of the world\'s most powerful memorials. The Peace Memorial Museum tells the human story of that day and its aftermath in unflinching detail. Required human experience.',
              details: [
                '📍 Peace Memorial Museum: 1-2 Nakajima-cho, Naka-ku · 💰 ¥200/person',
                '🕐 8:30am-6pm (until 8pm Jul-Nov)',
                '📍 A-Bomb Dome: Otemachi, Naka-ku · Always open · Free',
                '🕊️ The Children\'s Peace Monument is surrounded by thousands of paper cranes — a powerful sight',
                '💡 Allow 2-3 hours in the museum. It is emotionally heavy. Take time to sit quietly between galleries.',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Okonomimura (お好み村)',
              description: 'A multi-floor building housing dozens of okonomiyaki stalls — all making the Hiroshima-style version (layered with noodles, cabbage, and egg). Pick any stall on the upper floors and watch the chef build your pancake layer by layer on the iron griddle in front of you. Different from Osaka\'s mixed style — both are excellent.',
              meta: '📍 5-13 Shintenchi, Naka-ku, Hiroshima · 💰 ¥1,000-1,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🕊️ At the Peace Memorial Museum, fold a paper crane at the origami station inside. It\'s a small act of remembrance and solidarity.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Miyajima Island — Itsukushima Shrine',
              description: 'Take the JR ferry (7 min, covered by JR Pass) from Miyajimaguchi to Miyajima island. Itsukushima Shrine — built over the water on stilts — and its iconic floating torii gate are one of Japan\'s Three Views (Nihon Sankei). At high tide, the gate appears to float on the sea. At low tide, you can walk to it across the tidal flats and see the barnacles and scale up close.',
              details: [
                '⛴️ JR Ferry: Miyajimaguchi → Miyajima, 7 min (JR Pass covers this ferry!)',
                '💰 Itsukushima Shrine: ¥300/person',
                '🌊 Check tide times before going — high tide (floating gate) is photogenic; low tide (walk-to gate) is experiential. Both are worth experiencing.',
                '🦌 Miyajima also has free-roaming deer — feed them carefully',
              ],
            },
            {
              title: 'Mt. Misen Hike or Ropeway',
              description: 'The island\'s sacred mountain offers the best panoramic views of the Seto Inland Sea, dotted with hundreds of islands. Hike up via the Daisho-in trail (1.5h, moderately challenging, passes waterfalls and stone lanterns) or take the ropeway up (¥1,840 round trip) and hike the final 30 minutes to the summit.',
              details: [
                '⛰️ Full hike: 1h30m-2h up via Daisho-in trail · Free',
                '🚡 Ropeway: ¥1,840 round trip + 30 min hike to summit',
                '🌅 Summit views: 360° of the Seto Inland Sea — extraordinary on a clear day',
              ],
            },
            {
              title: 'Daisho-in Temple',
              description: 'One of Japan\'s most important Shingon Buddhist temples, at the base of Mt. Misen. Stone steps lined with 500 stone disciples (rakan) — each with a unique expression. Spin the prayer wheels, ring the enormous bell, and visit the cave shrine with sacred flame that has burned continuously for 1,200 years.',
              details: [
                '📍 Daisho-in Temple, Miyajima island · Free',
                '💡 Don\'t miss the fire cave inside the main hall — the eternal flame brought from the sacred lantern on Koya-san',
              ],
            },
          ],
          meals: [
            {
              type: '🦪 Snack on Miyajima',
              name: 'Miyajima Oysters & Momiji Manju',
              description: 'Miyajima is famous for its giant flame-grilled oysters (fresh from the Hiroshima bay, best in Japan). Buy them hot from the stalls along the ferry pier street. Also try momiji manju — maple-leaf-shaped sweet cakes in matcha, red bean, or cream flavors. Miyajima\'s most beloved souvenir.',
              meta: '💰 Oysters: ¥400-600 each · Momiji manju: ¥100-150 each',
            },
          ],
          tips: [
            { type: 'tip', text: '🌅 If timing works, watch the sun set behind the torii gate from the ferry dock as you leave Miyajima. The torii silhouetted against an orange sky is an image you\'ll carry forever.' },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: 'Take the JR ferry back to Miyajimaguchi, then JR to Hiroshima Station, then shinkansen back to Osaka (1h10m). Arrive in time for a late dinner in Namba.',
              details: [
                '💡 Last sensible shinkansen back: aim for 6-7pm from Hiroshima to be in Osaka by 8pm',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Late Dinner',
              name: 'Kuidaore Taro Street Food',
              description: 'Back in Dotonbori, pick up a late-night street food dinner — takoyaki, kushikatsu (deep-fried skewers), taiyaki (fish-shaped waffle), or just konbini snacks if exhausted. Today was big.',
              meta: '💰 ¥500-1,500/person',
            },
          ],
          tips: [],
        },
      ],
      mapPins: [
        { lat: 34.3955, lng: 132.4531, label: 'Peace Memorial Park', num: 1, cat: 'attraction', desc: 'A-Bomb Dome and Peace Museum — required human experience' },
        { lat: 34.3958, lng: 132.4530, label: 'A-Bomb Dome', num: 2, cat: 'attraction', desc: 'UNESCO ruins of the dome that survived — preserved as-is' },
        { lat: 34.3946, lng: 132.4548, label: 'Okonomimura', num: 3, cat: 'restaurant', desc: 'Multi-floor building of Hiroshima-style okonomiyaki stalls' },
        { lat: 34.2963, lng: 132.3194, label: 'Itsukushima Shrine', num: 4, cat: 'attraction', desc: 'Floating shrine and iconic torii gate — Japan\'s Three Views' },
        { lat: 34.2948, lng: 132.3208, label: 'Miyajima Torii Gate', num: 5, cat: 'attraction', desc: 'Walk to it at low tide, photograph at high tide' },
        { lat: 34.2883, lng: 132.3222, label: 'Mt. Misen Summit', num: 6, cat: 'attraction', desc: 'Sacred mountain — 360° views of the Seto Inland Sea' },
        { lat: 34.2974, lng: 132.3182, label: 'Daisho-in Temple', num: 7, cat: 'attraction', desc: '1,200-year-old eternal flame in a sacred cave temple' },
      ],
    },

    // DAY 11 — Osaka: Castle + Shinsekai + Nightlife
    {
      num: 11,
      date: 'Mar 26',
      title: 'Osaka: Castle, Kushikatsu & the Retro Streets of Shinsekai',
      description: 'A slower Osaka day — explore the great castle\'s cherry-lined moats, dive into the retro working-class neighborhood of Shinsekai, and spend a final evening shopping in Shinsaibashi before the next day\'s shinkansen north.',
      neighborhoods: 'Osaka Castle · Shinsekai · Namba',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Cherry Blossom Park 🌸',
              description: 'Osaka Castle is surrounded by one of Japan\'s finest castle parks, with 600+ cherry trees lining the moats and inner grounds. Walk the outer moat circuit in full bloom, then climb to the castle\'s observation deck for panoramic views of the city. The castle itself has an excellent free museum covering Toyotomi Hideyoshi\'s era.',
              details: [
                '📍 1-1 Osakajo, Chuo-ku, Osaka',
                '💰 Castle tower: ¥600/person · Park: free',
                '🕐 9am-5pm',
                '🌸 The cherry trees along the outer moat are some of Osaka\'s finest — arrive by 8:30am for moat reflections',
                '💡 The castle interior museum is excellent and free with tower entry — covers the Sengoku period',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Osaka morning pastry from konbini',
              description: 'Pick up melon pan, coffee, and a yogurt from the 7-Eleven near Osaka Castle for a classic Japanese morning.',
              meta: '💰 ¥400-700/person',
            },
          ],
          tips: [
            { type: 'tip', text: '📸 Best castle-and-cherry-blossoms shot: stand on the stone bridge over the inner moat looking up at the castle tower with blossoms framing both sides.' },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai — Old Osaka Retro District',
              description: 'A fascinatingly preserved 1950s working-class neighborhood dominated by the Tsutenkaku Tower and its Billiken god statue (rub his feet for good luck). The streets are lined with kushikatsu (deep-fried skewer) restaurants, retro game parlors, and old-school sento bathhouses. Completely different vibe from touristy Namba — this is old Osaka, unapologetically itself.',
              details: [
                '📍 Shinsekai, Naniwa-ku, Osaka',
                '🏯 Tsutenkaku Tower: ¥800 (observation deck) — the view is secondary to the vibe',
                '🍢 Kushikatsu: deep-fried skewers of everything (Wagyu beef, asparagus, shrimp, mochi) in a light panko batter, dipped in a shared sweet-savory sauce. NEVER double-dip.',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kushikatsu Daruma (串カツだるま)',
              description: 'The most famous kushikatsu restaurant in Shinsekai, with the iconic "No double-dipping!" sign. Order a mix platter and work through the skewers with cold Asahi beer. Budget and fun.',
              meta: '📍 Shinsekai area, Naniwa-ku · 💰 ¥1,500-2,500/person with drinks',
            },
          ],
          tips: [],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Evening in Osaka — Namba & Dotonbori',
              description: 'A final wander through Dotonbori and Namba at night — by now you know the streets. Pick up souvenirs from Don Quijote, try any food you haven\'t tasted yet, and soak in the neon atmosphere one last time.',
              details: [
                '🛍️ Best souvenirs: Kit Kat flavors (Japan-exclusive), Pocky, matcha chocolates, Glico candy sets, Osaka specialty: Baton d\'Or cookies',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sushiro Conveyor Belt Sushi (スシロー)',
              description: 'Japan\'s most popular kaiten-zushi (conveyor belt sushi) chain is excellent quality at ¥110-330 per plate. Order from the tablet, watch your plates arrive by conveyor — fresh tuna, salmon, prawn, uni, and seasonal specials. A perfect casual farewell dinner.',
              meta: '📍 Multiple Namba/Shinsaibashi locations · 💰 ¥1,500-2,500/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🛒 Stock up at Don Quijote tonight for gifts — Japan-exclusive Kit Kat flavors (matcha, sake, wasabi), Pocky gift boxes, and Beauty products from local brands are perfect omiyage.' },
          ],
        },
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5259, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Historic castle with 600+ cherry trees along the moat' },
        { lat: 34.6526, lng: 135.5064, label: 'Shinsekai', num: 2, cat: 'attraction', desc: 'Retro 1950s district — Tsutenkaku tower and old Osaka character' },
        { lat: 34.6528, lng: 135.5059, label: 'Tsutenkaku Tower', num: 3, cat: 'attraction', desc: 'Osaka\'s retro landmark — rub Billiken\'s feet for luck' },
        { lat: 34.6524, lng: 135.5050, label: 'Kushikatsu Daruma', num: 4, cat: 'restaurant', desc: 'The original kushikatsu spot — "No double-dipping!"' },
        { lat: 34.6687, lng: 135.5003, label: 'Dotonbori (Final Night)', num: 5, cat: 'attraction', desc: 'Last walk through the neon canal — soak it all in' },
        { lat: 34.6672, lng: 135.5014, label: 'Don Quijote Namba', num: 6, cat: 'attraction', desc: 'Multi-floor discount store — best omiyage shopping' },
        { lat: 34.6695, lng: 135.5005, label: 'Sushiro Namba', num: 7, cat: 'restaurant', desc: 'Japan\'s best conveyor belt sushi — perfect farewell dinner' },
      ],
    },

    // DAY 12 — Osaka → Tokyo, Shinjuku final day
    {
      num: 12,
      date: 'Mar 27',
      title: 'Return to Tokyo — Shinjuku, Shibuya & Farewell Ramen',
      description: 'The final full day — an easy morning shinkansen back to Tokyo, a few hours to revisit favorites or explore anything missed, and a proper farewell dinner in the city that started it all.',
      neighborhoods: 'Shinjuku · Shibuya · Harajuku',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka → Tokyo (Shinkansen)',
              description: 'Morning Hikari shinkansen from Shin-Osaka to Tokyo (2h40m, JR Pass). Use the journey to rest, review photos, and plan your last day. Arrive in Tokyo by lunchtime.',
              details: [
                '🚅 Shin-Osaka → Tokyo: 2h40m on Hikari (JR Pass)',
                '💡 Book early morning departure — 7am or 8am trains get you back to Tokyo by 10-11am',
                '💡 Remember to return your JR Pass today if the 7-day period ends — no need to return it, it simply becomes inactive',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Breakfast',
              name: 'Shinkansen Ekiben (last one!)',
              description: 'One final ekiben from Osaka Station before boarding — try the Hana-zushi (Osaka pressed sushi set) or the wagyu beef bento from the Shin-Osaka platform shops.',
              meta: '💰 ¥1,000-1,800',
            },
          ],
          tips: [],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Meguro River Cherry Blossoms (if still in bloom) 🌸',
              description: 'The Meguro River is Tokyo\'s most romantic cherry blossom spot — 800+ trees lining the canal for 4 km, illuminated at night. By March 27, Tokyo blossoms should be at or near peak (they typically peak March 25-31). Walk from Naka-Meguro to Ikejiri-Ohashi and back along both banks.',
              details: [
                '📍 Naka-Meguro Station, Meguro-ku',
                '🌸 Illuminated 5pm-9pm during peak bloom',
                '💡 Grab canned sake from a convenience store and join the locals sitting along the riverbank under the blossoms',
              ],
            },
            {
              title: 'Harajuku Omotesando & Last Shopping',
              description: 'A final walk down Omotesando Avenue for any last-minute shopping — from Uniqlo to international luxury brands. Pick up any remaining Japan-specific items: Loewe Shinjuku exclusive bags, Muji stationery, handmade Japanese ceramics, and limited Tokyo Kit Kats.',
              details: [
                '💡 Tokyu Hands department store in Shibuya or Shinjuku is the best place for Japan design goods and stationery',
                '💡 The Muji flagship (Aoyama or Ginza) has Japan-only products not available overseas',
              ],
            },
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Katsu Midori Sushi (Shibuya)',
              description: 'One of Tokyo\'s most popular budget sushi spots, using premium fish at half the price of Tsukiji restaurants. Queues move fast. Fresh tuna, fatty toro, scallop — all excellent.',
              meta: '📍 Shibuya Hikarie, Shibuya-ku · 💰 ¥1,500-2,500/person · Expect 20-30 min queue',
            },
          ],
          tips: [],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chidorigafuchi Final Walk 🌸',
              description: 'If the cherry blossoms are at peak, a final walk at Chidorigafuchi — the Imperial Palace moat lined with weeping cherry trees, illuminated at night — is an unmissable farewell to Japan. The trees arch over the water, and petal rain fills the air as petals begin to fall.',
              details: [
                '📍 Chidorigafuchi, Chiyoda-ku',
                '🕐 Night illumination: 6pm-10pm during peak bloom',
                '💡 Even if blossoms have passed, the moat reflection and palace walls make it beautiful',
              ],
            },
          ],
          meals: [
            {
              type: '🍜 Farewell Dinner',
              name: 'Menya Musashi Ramen (麺屋武蔵)',
              description: 'One of Tokyo\'s most beloved ramen chains, specializing in tsukemen and rich pork-based ramen. The thick broth is intensely savory — a proper final meal before heading home. Multiple Shinjuku-area locations.',
              meta: '📍 Shinjuku area · 💰 ¥950-1,300/person',
            },
          ],
          tips: [
            { type: 'tip', text: '🛫 Departure day checklist: Arrange luggage forwarding to airport (¥2,000-3,000, book via hotel), plan train route to Narita or Haneda (~90 min from Shinjuku), arrive at airport 2h30m before international flight.' },
          ],
        },
      ],
      mapPins: [
        { lat: 35.6440, lng: 139.6988, label: 'Meguro River Blossoms', num: 1, cat: 'attraction', desc: '800 cherry trees illuminated along 4km of canal — peak yozakura' },
        { lat: 35.6652, lng: 139.7063, label: 'Omotesando Avenue', num: 2, cat: 'attraction', desc: 'Tree-lined luxury shopping avenue — last Japan shopping' },
        { lat: 35.6595, lng: 139.7016, label: 'Shibuya Hikarie (Katsu Midori)', num: 3, cat: 'restaurant', desc: 'Premium budget sushi — Tokyo\'s best value fresh fish' },
        { lat: 35.6938, lng: 139.7500, label: 'Chidorigafuchi', num: 4, cat: 'attraction', desc: 'Imperial moat with illuminated weeping cherry trees' },
        { lat: 35.6892, lng: 139.6917, label: 'Shinjuku (Farewell Base)', num: 5, cat: 'attraction', desc: 'Return to where it all began — final night in Tokyo' },
        { lat: 35.6854, lng: 139.6980, label: 'Menya Musashi Ramen', num: 6, cat: 'restaurant', desc: 'Farewell ramen — rich tsukemen to close out 12 incredible days' },
      ],
    },
  ],

  budgetTable: [
    { category: 'Accommodation (12 nights, per person)', low: '$480', mid: '$720', high: '$1,200', notes: 'Hostel/budget hotel vs. boutique ryokan mix' },
    { category: '7-Day JR Pass', low: '$280', mid: '$280', high: '$280', notes: 'Fixed cost — buy before departure' },
    { category: 'Local transport (subway, buses)', low: '$60', mid: '$80', high: '$100', notes: 'Suica/Pasmo IC card top-ups' },
    { category: 'Food (12 days)', low: '$360', mid: '$540', high: '$840', notes: 'Konbini + street food + izakayas + one nice dinner' },
    { category: 'Activities & Entrance Fees', low: '$80', mid: '$140', high: '$220', notes: 'Temples, museums, onsen, owl café, monkey park' },
    { category: 'Souvenirs & Shopping', low: '$50', mid: '$150', high: '$400', notes: 'Gifts, Kit Kats, ceramics, clothing' },
    { category: 'TOTAL (per person)', low: '$1,310', mid: '$1,910', high: '$3,040', notes: 'Comfortably within your $1,000-2,000 budget at mid level' },
  ],

  practicalInfo: [
    {
      title: '🛬 Arriving in Japan',
      items: [
        '<strong>Narita Airport:</strong> Keisei Skyliner to Ueno (36 min, ¥2,520) or Access Express (55 min, ¥1,290)',
        '<strong>Haneda Airport:</strong> Tokyo Monorail or Keikyu Line to city center (25-30 min, ¥500-650)',
        'Arrange JR Pass activation at airport or at Narita/Haneda station — bring your exchange order voucher',
        'Luggage forwarding (takuhaibin) at the airport sends bags to your hotel for ¥2,000-3,000 each',
      ],
    },
    {
      title: '🚅 JR Pass Strategy',
      items: [
        '<strong>Buy before departure</strong> (not available in Japan except at premium prices)',
        '<strong>7-day pass: ~$280/person</strong> — activate on Day 5 (Kyoto departure) for 7 days: Tokyo→Kyoto→Osaka→Hiroshima→back to Tokyo',
        'Covers: Hikari/Sakura shinkansen, JR Nara Line, JR Ferry to Miyajima, local JR trains',
        '<strong>Does NOT cover:</strong> Nozomi shinkansen (use Hikari), Kyoto subway, Osaka subway',
        'Reserve shinkansen seats at the JR ticket window (free for JR Pass holders) — recommended for travel during cherry blossom season',
      ],
    },
    {
      title: '🌸 Cherry Blossom Timing (Late March)',
      items: [
        '<strong>Tokyo:</strong> Typically peaks March 25-31 — you\'ll catch it in the second half of your trip',
        '<strong>Kyoto:</strong> Peaks slightly earlier, often March 20-28 — prime timing for your Days 5-8',
        '<strong>Osaka:</strong> Similar to Kyoto — mid-to-late March',
        'Check real-time forecasts: <strong>sakura.weathermap.jp</strong> (Japanese) or <strong>jnto.go.jp/sakura</strong>',
        'If blossoms peak early or late, adjust your schedule — go to best-bloom cities first',
      ],
    },
    {
      title: '🏨 Accommodation Tips',
      items: [
        '<strong>Tokyo (Days 1-4, 12):</strong> Khaosan Tokyo Origami (Asakusa, ~$45/night), Unplan Shinjuku (~$55/night), Book and Bed (sleep in a bookshelf!)',
        '<strong>Hakone (Day 4):</strong> Consider one night in a basic ryokan in Hakone-Yumoto (¥8,000-15,000/person with dinner + breakfast) — the full Japanese inn experience',
        '<strong>Kyoto (Days 5-8):</strong> Piece Hostel Sanjo (~$35/person), First Cabin Tenjin (~$50/person)',
        '<strong>Osaka (Days 9-11):</strong> Cross Hotel Osaka (~$80/night), Dormy Inn Shinsaibashi (~$90/night)',
        '⚠️ Book early — late March cherry blossom season = Japan\'s peak tourist season',
      ],
    },
    {
      title: '🍜 Must-Eat Japan',
      items: [
        '<strong>Tokyo:</strong> Ramen (Ichiran/Fuunji tsukemen), soba (Kanda Yabu), sushi (Katsu Midori), tamagoyaki, konbini onigiri at 2am',
        '<strong>Kyoto:</strong> Kaiseki (one splurge meal), tofu yudofu, Nishiki market snacks, matcha everything, Omurice at Kichi Kichi',
        '<strong>Osaka:</strong> Takoyaki, okonomiyaki (Osaka-style mixed), kushikatsu (Shinsekai), fresh oysters (Kuromon), conveyor sushi (Sushiro)',
        '<strong>Nara:</strong> Kakinoha-zushi (persimmon leaf sushi), mochi from park vendors',
        '<strong>Hiroshima:</strong> Hiroshima-style okonomiyaki (layered, not mixed), oysters from the bay',
        '<strong>Everywhere:</strong> 7-Eleven/Lawson onigiri, melon pan, taiyaki, matcha soft serve, corn dogs at FamilyMart',
      ],
    },
  ],
};

fulfillOrder(order, itineraryData);
