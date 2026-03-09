const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772481601812_ul6yqi",
  email: "paulhblasjr@gmail.com",
  destination: "Tokyo, Osaka, Kyoto",
  start_date: "2026-05-15",
  end_date: "2026-05-24",
  group_size: "5+",
  travel_style: "Adventure, Cultural, Foodie, Family-friendly",
  dining: "Mix of everything",
  budget: "Surprise me",
  requests: "",
  amount: "0.00",
  timestamp: "2026-03-02T20:00:01.812Z",
  status: "pending"
};

const itineraryData = {
  destination: "Tokyo, Osaka & Kyoto, Japan",
  countryEmoji: "🇯🇵",
  title: "Japan with Kids: Tokyo, Osaka & Kyoto in 10 Days",
  subtitle: "Tokyo 4 Nights → Osaka Base Camp 5 Nights (with Kyoto & Nara Day Trips)",
  description: "A family adventure through Japan's greatest hits — designed for 3 adults and 2 toddlers (ages 2 and 3). This itinerary packs in anime stores, temples, incredible food (no pork!), and kid-friendly parks while keeping the pace toddler-friendly with built-in rest time, stroller-accessible routes, and shorter walking days. May in Japan means pleasant weather, fewer crowds than cherry blossom season, and lush green everywhere.",
  duration: "9 nights / 10 days",
  dates: "May 15 – 24, 2026",
  budget: "Flexible — mix of splurge meals and convenience stores",
  pace: "Family-friendly — built-in rest blocks, stroller-friendly routes",
  bestFor: "Families with toddlers, anime fans, foodies (no pork)",
  highlights: [
    "teamLab Planets — immersive digital art (toddler-friendly!)",
    "Sensō-ji Temple — Tokyo's oldest, stunning Thunder Gate",
    "Pokémon Centers & Kirby Café — anime heaven for kids",
    "Fushimi Inari Taisha — iconic thousand red torii gates",
    "Nara Park — friendly bowing deer, toddler paradise",
    "Arashiyama Bamboo Forest — magical walk through towering bamboo",
    "Osaka Aquarium Kaiyukan — one of the world's best",
    "Dotonbori — Osaka's neon-lit food street (Glico sign!)",
    "Shinjuku Gyoen — peaceful garden oasis for family picnics",
    "Tokyo Skytree — panoramic views from Japan's tallest tower"
  ],
  essentials: [
    { title: "👶 Traveling with Toddlers", text: "Japan is incredibly family-friendly. Most train stations have elevators (look for ♿ signs). Department stores have clean nursing rooms (授乳室) and diaper-changing stations on every floor. Strollers are welcome everywhere — many temples have paved paths. Convenience stores (konbini) are lifesavers for snacks, milk, and baby supplies 24/7." },
    { title: "🚅 Getting Around", text: "Get a 7-day Japan Rail Pass (activate on Day 1 in Tokyo for ¥50,000/adult — covers the Tokyo→Osaka shinkansen worth ¥14,000 alone). Kids under 6 ride FREE on all trains. In Tokyo, use Suica/PASMO IC cards (tap-and-go). Buy at any station kiosk. Strollers fold for crowded trains — baby carriers are great for rush hour." },
    { title: "🍜 No-Pork Dining", text: "Japan's cuisine is pork-heavy, but doable without it! Key phrases: 豚肉なし (butaniku nashi = no pork). Watch for hidden pork in: ramen broth (ask for 鶏 tori/chicken or 魚介 gyokai/fish-based), gyoza filling, curry, and dashi. We've curated restaurants verified for no-pork options. Halal/chicken ramen shops are increasingly common in tourist areas." },
    { title: "🌤️ May Weather", text: "May is ideal — warm (18-25°C), low humidity, pre-rainy season. Light layers for mornings/evenings, t-shirts for afternoon. Pack a light rain jacket just in case. Sunscreen for the kids — UV can be strong even on cloudy days." },
    { title: "🏨 Where to Stay", text: "Tokyo (4 nights): Shinjuku area — central hub for trains, food, and walking to many attractions. Osaka (5 nights): Namba/Shinsaibashi area — walking distance to Dotonbori, great train access for day trips. Book family rooms or connecting rooms — many hotels offer cribs for free on request." },
    { title: "📱 Useful Apps", text: "Google Maps (train navigation is perfect in Japan), Suica app (IC card on iPhone), Google Translate (camera mode for menus), Tabelog (restaurant reviews — trust the 3.5+ ratings), NAVITIME for Japan transit." },
    { title: "💴 Money Tips", text: "Japan is increasingly cashless but still keep some yen. 7-Eleven ATMs accept all foreign cards. Tax-free shopping available at most stores over ¥5,000 — bring your passport! No tipping in Japan — it's considered rude." },
    { title: "🧳 Packing for Toddlers", text: "Bring a lightweight umbrella stroller (or rent one from hotels). Pack small snack containers — Japanese konbini have great kid snacks (onigiri, milk, fruit). Baby formula and diapers (Merries, Moony) are available at every drugstore and are excellent quality." }
  ],
  days: [
    // ========== DAY 1 — MAY 15 — ARRIVAL + SHINJUKU ==========
    {
      num: 1,
      title: "Arrival & Shinjuku Exploration",
      neighborhoods: "Shinjuku",
      date: "May 15",
      mapPins: [
        { lat: 35.6896, lng: 139.6921, label: "Shinjuku Station East Exit", num: 1, cat: "activity", desc: "JJK reference — the famous east exit" },
        { lat: 35.6938, lng: 139.7034, label: "Shinjuku Gyoen", num: 2, cat: "activity", desc: "Sprawling garden — perfect for toddlers to run" },
        { lat: 35.6936, lng: 139.7004, label: "Omoide Yokocho", num: 3, cat: "food", desc: "Memory Lane — atmospheric alley dining" },
        { lat: 35.6940, lng: 139.7030, label: "Don Quijote Shinjuku", num: 4, cat: "activity", desc: "Massive discount store — everything you need" },
        { lat: 35.6945, lng: 139.7035, label: "Shinjuku Golden Gai", num: 5, cat: "activity", desc: "Tiny bars district — walk through for photos" },
        { lat: 35.6895, lng: 139.7004, label: "3D Cat Billboard", num: 6, cat: "activity", desc: "Giant 3D calico cat on Cross Shinjuku Vision screen" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            { title: "Arrive & Settle In", description: "Land at Narita or Haneda, activate your JR Pass at the airport JR counter, and take the train to Shinjuku. Drop bags at hotel, freshen up. Let the toddlers decompress — the flight was long! Grab drinks and snacks from the nearest konbini (FamilyMart or 7-Eleven) to fuel up.", details: ["JR Pass activation: bring your exchange order + passports", "Airport → Shinjuku: ~90 min from Narita (N'EX), ~40 min from Haneda (monorail + JR)", "IC cards (Suica/PASMO): grab them at the airport station too"] },
            { title: "Shinjuku Station East Exit", description: "Snap a photo at the famous east exit — if you're a JJK fan, you know why. The iconic Shinjuku Station is the world's busiest, and the east exit area is a great introduction to Tokyo's energy.", details: ["JJK fans: this is the Shibuya Incident location inspiration", "Look for the 3D cat billboard on the Cross Shinjuku Vision screen nearby"] },
            { title: "3D Cat Billboard (Cross Shinjuku Vision)", description: "Walk to the Cross Shinjuku Vision building on the north side of Shinjuku — the giant 3D calico cat is mesmerizing for kids and adults alike. It plays on the hour and is best seen from the street level.", details: ["Free — just look up!", "Plays regularly throughout the day, best visibility in the late afternoon"] }
          ],
          meals: [
            { type: "🍜 Dinner", name: "Omoide Yokocho (Memory Lane)", description: "Atmospheric alley of tiny restaurants near Shinjuku Station west exit. Narrow, smoky, magical at night. Many stalls serve yakitori (chicken skewers), seafood, and ramen — easy to find no-pork options. Kids will love the energy. Strollers are tight here — baby carriers recommended.", meta: "¥800-1,500pp · Shinjuku · Cash preferred · Open until late" }
          ],
          tips: [
            { type: "tip", text: "Don Quijote (Donki) Shinjuku is open 24 hours — grab baby supplies, snacks, souvenirs, and random fun stuff. Kids love the toy floors." },
            { type: "tip", text: "SURUGA-YA Shinjuku Marui Annex is great for anime figures and collectibles. Seria (100-yen shop) in the same building for cheap souvenirs." }
          ]
        }
      ]
    },

    // ========== DAY 2 — MAY 16 — ASAKUSA + SKYTREE + IKEBUKURO ==========
    {
      num: 2,
      title: "Asakusa, Skytree & Ikebukuro Anime District",
      neighborhoods: "Asakusa · Sumida · Ikebukuro",
      date: "May 16",
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: "Sensō-ji Temple", num: 1, cat: "activity", desc: "Tokyo's oldest temple — stunning Thunder Gate" },
        { lat: 35.7100, lng: 139.8107, label: "Tokyo Skytree", num: 2, cat: "activity", desc: "634m tower with panoramic views" },
        { lat: 35.7131, lng: 139.7982, label: "Nakamise-dori", num: 3, cat: "food", desc: "Shopping street to Sensō-ji — ichigo daifuku!" },
        { lat: 35.7290, lng: 139.7190, label: "Sunshine City", num: 4, cat: "activity", desc: "Mega mall with Pokémon Center & KIDDY LAND" },
        { lat: 35.7290, lng: 139.7190, label: "Pokémon Center Mega Tokyo", num: 5, cat: "activity", desc: "Massive Pokémon store + Pikachu Sweets" },
        { lat: 35.7284, lng: 139.7193, label: "Donguri Kyowakoku", num: 6, cat: "activity", desc: "Official Studio Ghibli merchandise store" },
        { lat: 35.7120, lng: 139.7950, label: "UNIQLO Asakusa", num: 7, cat: "activity", desc: "Great for Japanese-exclusive UNIQLO items" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sensō-ji Temple & Nakamise-dori", description: "Start early (by 8am) to beat crowds at Tokyo's oldest and most iconic temple. Walk through the magnificent Kaminarimon (Thunder Gate) with its giant red lantern, then stroll Nakamise-dori — the 250m shopping street lined with traditional snacks and souvenirs. Get ichigo daifuku (strawberry mochi) from Asakusa Ichigo-za or Ginkado along the way. The temple grounds are stroller-friendly with paved paths.", details: ["Arrive before 9am for peaceful photos at the gate", "Ichigo daifuku vendors: look for Asakusa Ichigo-za and Ginkado on Nakamise-dori", "Free to enter — incense burning area is optional", "Pick up omamori (charms) as souvenirs — different ones for different blessings"] },
            { title: "UNIQLO Asakusa", description: "The Asakusa UNIQLO store has Japan-exclusive designs, character collabs, and great kids' clothes at amazing prices. Quick stop on the way out of Asakusa.", details: ["Look for Japanese-exclusive UT graphic tees", "Kids' section has great anime collaboration items"] }
          ],
          meals: [
            { type: "🍳 Breakfast", name: "Wagyu Ichinoya (Asakusa)", description: "Start the day with a wagyu beef breakfast set — yes, wagyu for breakfast is a thing in Asakusa. Tender beef over rice with miso soup. No pork on the menu. Kids love the simple rice + meat combo.", meta: "¥1,500-2,500pp · Asakusa · 5 min from Sensō-ji" }
          ],
          tips: [
            { type: "tip", text: "Sensō-ji is most magical at dawn or after 5pm when the lanterns glow. Morning visit = less crowded and cooler for kids." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "Tokyo Skytree", description: "Japan's tallest structure at 634m. The Tembo Deck (350m) has incredible panoramic views — on clear days you can see Mt. Fuji. The observation deck is fully stroller-accessible via elevator. Toddlers love watching the tiny cars below. Solamachi mall at the base has great food and shops.", details: ["Book tickets online to skip the line (skytree.jp)", "Tembo Deck: ¥2,100/adult, ¥950/child (4-11), FREE under 4", "Stroller-friendly — elevators to all levels", "Skip Tembo Gallery (450m) with toddlers — Deck is impressive enough"] },
            { title: "Oyokogawa Shinsui Park", description: "If the kids need to burn energy after Skytree, this charming waterside park is a 10-minute walk away. Shaded paths along the old canal with small playgrounds. Perfect toddler break.", details: ["Free · Open 24h · Stroller-friendly paths", "Nice spot for a konbini picnic lunch"] }
          ],
          meals: [
            { type: "🍱 Lunch", name: "Solamachi (Skytree Base)", description: "The Solamachi mall under Skytree has dozens of restaurants — sushi, udon, curry, and more. Easy to find no-pork options. Kid-friendly with high chairs available at most spots.", meta: "¥1,000-2,000pp · Sumida · Multiple options" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rest Break", description: "Head back to the hotel or find a family café for a 1-2 hour rest. Toddlers (and adults!) need recharge time. Japanese hotels often have great lobby lounges. Or grab treats from a konbini and relax in the room.", details: ["Konbini rest hack: onigiri, fruit cups, milk boxes = easy toddler snacks", "Many Shinjuku hotels have coin laundry — great time to do a load"] },
            { title: "Sunshine City (Ikebukuro)", description: "This massive entertainment complex is anime heaven. Home to Pokémon Center Mega Tokyo & Pikachu Sweets, KIDDY LAND (toy paradise), the Ghibli Store (Donguri Kyowakoku), and more. Fully stroller-accessible. Plan at least 2 hours here — you won't want to leave.", details: ["Pokémon Center Mega Tokyo: Japan's biggest — exclusive plushies and merch", "Pikachu Sweets: café with Pikachu-shaped desserts — book online!", "Donguri Kyowakoku: official Ghibli store — Totoro everything", "KIDDY LAND: multi-floor toy store — Sanrio, Disney, anime, crafts"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "The Front Room Deli Restaurant (Marunouchi)", description: "Upscale-casual deli restaurant in the Marunouchi area near Tokyo Station. Great international menu with clear allergen labeling — easy to navigate no-pork. Good kids' portions. The area around Tokyo Station is beautiful at night.", meta: "¥2,000-4,000pp · Marunouchi · Reservations recommended" }
          ],
          tips: [
            { type: "tip", text: "Ikebukuro is an anime district — Sunshine City alone could fill an entire day. Prioritize Pokémon Center + Ghibli store if time is short." }
          ]
        }
      ]
    },

    // ========== DAY 3 — MAY 17 — HARAJUKU + SHIBUYA ==========
    {
      num: 3,
      title: "Harajuku, Meiji Shrine & Shibuya",
      neighborhoods: "Harajuku · Omotesando · Shibuya",
      date: "May 17",
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: "Meiji Jingu", num: 1, cat: "activity", desc: "Serene shrine in a forest — peaceful morning" },
        { lat: 35.6702, lng: 139.7026, label: "Yoyogi Park", num: 2, cat: "activity", desc: "Huge park — toddler heaven for running" },
        { lat: 35.6704, lng: 139.7027, label: "Takeshita Street", num: 3, cat: "activity", desc: "Harajuku's famous colorful shopping street" },
        { lat: 35.6595, lng: 139.7004, label: "Shibuya Crossing", num: 4, cat: "activity", desc: "World's busiest pedestrian crossing" },
        { lat: 35.6584, lng: 139.7022, label: "Shibuya Sky", num: 5, cat: "activity", desc: "360° rooftop observation — stunning views" },
        { lat: 35.6611, lng: 139.6984, label: "Pokémon Center Shibuya", num: 6, cat: "activity", desc: "Shibuya-exclusive Pokémon merchandise" },
        { lat: 35.6617, lng: 139.6977, label: "MAGNET by SHIBUYA109", num: 7, cat: "activity", desc: "Iconic Shibuya mall — rooftop Shibuya X photo" },
        { lat: 35.6685, lng: 139.7029, label: "A Happy Pancake", num: 8, cat: "food", desc: "Famous fluffy soufflé pancakes" },
        { lat: 35.6640, lng: 139.6978, label: "CAFE REISSUE", num: 9, cat: "food", desc: "Latte art café — adorable character foam art" },
        { lat: 35.6675, lng: 139.7048, label: "ONE PIECE Mugiwara Store", num: 10, cat: "activity", desc: "Official One Piece merchandise store" },
        { lat: 35.6686, lng: 139.7036, label: "Brandy Melville Japan", num: 11, cat: "activity", desc: "Popular fashion store" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Meiji Jingu Shrine", description: "Walk through the towering torii gate into the peaceful forested grounds of Meiji Jingu — Tokyo's most important Shinto shrine, dedicated to Emperor Meiji. The gravel paths through the forest feel like another world. Strollers work on the main path (packed gravel). Write a wish on an ema (wooden plaque) — kids love it.", details: ["Free entry · Open sunrise to sunset", "The walk from the entrance to the main shrine is ~10 min through beautiful forest", "Stroller-friendly on main path — some gravel sections", "Morning is quieter and cooler for toddlers"] },
            { title: "Yoyogi Park", description: "Right next to Meiji Jingu, this massive park is perfect for toddlers to run free. Wide open lawns, shaded areas, and usually street performers on weekends. Bring a blanket for a picnic. In May the roses are in bloom.", details: ["Free · Open 24h · Huge lawns for kids", "Restrooms with changing tables available", "Great konbini picnic spot"] }
          ],
          meals: [
            { type: "🥞 Breakfast", name: "A Happy Pancake (Omotesando)", description: "Famous Japanese soufflé pancakes — impossibly fluffy, jiggly, cloud-like. Kids are mesmerized watching them wobble. The Omotesando location has a calm atmosphere. No pork on the menu.", meta: "¥1,200-1,800pp · Omotesando · Arrive at opening (10am) to avoid wait" }
          ],
          tips: [
            { type: "tip", text: "Meiji Jingu → Yoyogi Park → Takeshita Street are all connected. Do them in this order for a natural flow from peaceful to chaotic." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "Takeshita Street", description: "Harajuku's iconic pedestrian shopping street — a candy-colored sensory overload of fashion, crêpes, cotton candy, and kawaii everything. Kids will love the rainbow cotton candy and character-themed treats. It gets PACKED — strollers work but baby carriers are easier.", details: ["Immo Pipi — get the roasted sweet potato treats here!", "Cotton candy shops — Instagram-worthy rainbow creations", "100-yen shops for cheap fun souvenirs", "⚠️ Very crowded by noon — go early or use carriers for toddlers"] },
            { title: "ONE PIECE Mugiwara Store (Harajuku)", description: "Official One Piece merchandise store — even if you're not a huge fan, the store is impressive with exclusive items and fun photo spots.", details: ["Harajuku location · Near Takeshita Street"] },
            { title: "Brandy Melville Japan", description: "Quick stop for fans of the brand — the Japan store has some exclusive items.", details: [] }
          ],
          meals: [
            { type: "🍦 Snack", name: "Immo Pipi Sweet Potato", description: "Harajuku sweet potato dessert shop — crispy on the outside, sweet and creamy inside. A unique Japanese street food that toddlers love. Naturally pork-free!", meta: "¥500-800 · Harajuku · Near Takeshita Street" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rest Break + CAFE REISSUE", description: "After the Harajuku sensory overload, take a family breather at CAFE REISSUE — famous for incredible latte art. They draw characters, animals, and custom designs in the foam. Kids are absolutely enchanted. Great for a mid-day rest.", details: ["Near Shibuya · Character latte art ¥700-1,000", "Can request custom designs!", "Chill atmosphere — good for toddler nap time in stroller"] },
            { title: "Shibuya Crossing & Station Area", description: "Walk to the world's busiest pedestrian crossing — up to 3,000 people cross at once during peak times. It's a spectacle even for toddlers (the sheer movement is mesmerizing). Visit the Hachikō statue outside the station — Japan's most loyal dog. Shibuya Station is another JJK reference spot!", details: ["Best viewed from the Starbucks above (2F Tsutaya building) or Shibuya Sky", "Hachikō statue: meet at the famous bronze dog — quick photo op", "JJK fans: Shibuya Station itself is significant"] },
            { title: "Shibuya Sky", description: "The 360° open-air observation deck on the rooftop of Shibuya Scramble Square (230m). Stunning views of the crossing below, Tokyo skyline, and Mt. Fuji on clear days. There's a glass floor section and a net art installation. Stroller parking available at ground level.", details: ["Book online: ¥2,000/adult, ¥900/child 6-12, FREE under 6!", "Sunset timing is magical — golden hour over the city", "Stroller parking at entrance — carry toddlers up top", "The open-air rooftop has high barriers — safe for kids"] },
            { title: "Pokémon Center Shibuya & MAGNET by SHIBUYA109", description: "The Shibuya Pokémon Center has exclusive Shibuya-themed merchandise (Mewtwo in a suit!). MAGNET by SHIBUYA109 is the iconic Shibuya mall — head to the rooftop for an awesome photo with the Shibuya X sign overlooking the crossing.", details: ["Pokémon Center: inside Shibuya PARCO 6F", "MAGNET rooftop: free viewing area of Shibuya Crossing", "109 has trendy Japanese fashion across multiple floors"] }
          ],
          meals: [
            { type: "🥩 Dinner", name: "Wagyu Halal Steak & Ramen 5W-Tokyo 1962 (Harajuku/Shibuya)", description: "This restaurant specifically caters to halal/no-pork diners — wagyu steak, chicken ramen, and Japanese fusion without any pork. Perfect for your dietary needs and a treat after a big day. Kid-friendly with smaller portions available.", meta: "¥2,500-5,000pp · Harajuku/Shibuya · Reservations recommended" }
          ],
          tips: [
            { type: "tip", text: "Shibuya Sky at sunset is one of Tokyo's best experiences. Book the 5:30-6pm slot for golden hour." }
          ]
        }
      ]
    },

    // ========== DAY 4 — MAY 18 — TEMPLES, GINZA & teamLab ==========
    {
      num: 4,
      title: "Temples, Ginza & teamLab Planets",
      neighborhoods: "Akasaka · Minato · Ginza · Toyosu",
      date: "May 18",
      mapPins: [
        { lat: 35.6576, lng: 139.7398, label: "Hie Shrine", num: 1, cat: "activity", desc: "Beautiful shrine with tunnel of red torii gates" },
        { lat: 35.6586, lng: 139.7455, label: "Prince Shiba Park", num: 2, cat: "activity", desc: "Park with Tokyo Tower views" },
        { lat: 35.6586, lng: 139.7454, label: "Tokyo Tower", num: 3, cat: "activity", desc: "Iconic 333m red-and-white tower" },
        { lat: 35.6706, lng: 139.7640, label: "Ginza Matcha Wabisabi", num: 4, cat: "food", desc: "Beautiful matcha desserts" },
        { lat: 35.6710, lng: 139.7650, label: "Art Aquarium Museum", num: 5, cat: "activity", desc: "Mesmerizing goldfish art installations" },
        { lat: 35.6686, lng: 139.7636, label: "Godaime Hanayama Udon", num: 6, cat: "food", desc: "Famous thick Ginza udon" },
        { lat: 35.6507, lng: 139.7833, label: "teamLab Planets", num: 7, cat: "activity", desc: "Immersive barefoot digital art — incredible" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Hie Shrine", description: "A hidden gem — this beautiful shrine has a tunnel of vermillion torii gates (similar to Fushimi Inari but without crowds). The escalator access makes it stroller-friendly! Peaceful morning atmosphere. The shrine's messenger is a monkey — kids love the monkey statues.", details: ["Free · Escalator from street level to the shrine!", "The torii gate tunnel is on the west side — follow signs", "Stroller-friendly via escalator route", "Less crowded than major shrines — authentic local feel"] },
            { title: "Prince Shiba Park & Tokyo Tower", description: "Walk through the pleasant Shiba Park with great views of Tokyo Tower. The iconic red-and-white tower is 333m tall and beautifully retro. You can go up (observation decks at 150m and 250m) or just enjoy it from the park — which is honestly the better photo. Kids love running around in the park with the tower looming above.", details: ["Tokyo Tower: ¥1,200/adult, ¥700/child 4-6, FREE under 4", "Park is free, stroller-friendly, with benches and shade", "The park view of the tower is better than the view FROM the tower"] }
          ],
          meals: [
            { type: "🍵 Breakfast/Brunch", name: "Matcha Café Wabisabi (Higashi-Ginza)", description: "Gorgeous matcha-themed café with stunning desserts — matcha tiramisu, parfaits, and lattes. The aesthetic is beautiful (great photos), flavors are authentic, and it's naturally pork-free. Kids love the green treats.", meta: "¥1,000-1,800pp · Ginza · Opens 11am" }
          ],
          tips: [
            { type: "tip", text: "Hie Shrine is near Akasaka — combine with Prince Shiba Park (15 min walk) for a peaceful morning before the Ginza bustle." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ginza Exploration", description: "Tokyo's upscale shopping district — wide boulevards, luxury brands, and great food. On weekends, the main Chūō-dōri street is car-free (hokōsha tengoku — pedestrian paradise), making it perfect for strollers. Visit the Onitsuka Tiger flagship for embroidery customization.", details: ["Onitsuka Tiger Ginza: custom embroidery on shoes — takes ~30 min", "Department store basements (depachika) have incredible food halls", "Weekend pedestrian zone: 12pm-5pm on Chūō-dōri"] },
            { title: "Art Aquarium Museum (Ginza)", description: "Mesmerizing fusion of art and aquarium — thousands of goldfish in beautifully illuminated installations. Dark, atmospheric, and genuinely stunning. Toddlers are captivated by the glowing fish and changing colors. Stroller-accessible.", details: ["¥2,400/adult, free under 3, ¥1,200 ages 3-12", "Takes ~45-60 min · Stroller-friendly (elevators)", "Dark environment — may be slightly scary for very sensitive toddlers", "Located in Ginza Mitsukoshi building"] },
            { title: "Godaime Hanayama Udon", description: "Famous Ginza udon shop — thick, chewy, handmade noodles. The signature cold udon with dipping sauce is incredible. Completely pork-free, with chicken and vegetable tempura options. Simple, satisfying, and kid-friendly.", details: ["¥1,000-1,500pp · Ginza", "Handmade udon — thick and chewy, kids love the texture", "No pork on the menu — chicken tempura udon is the star"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Godaime Hanayama Udon Ginza", description: "See activity above — this IS your lunch. Famous thick udon in Ginza, completely pork-free.", meta: "¥1,000-1,500pp · Ginza · Expect a short line" }
          ],
          tips: [
            { type: "tip", text: "Tokyo Metropolitan Government Building has FREE observation decks — but we've placed it on Day 1's neighborhood (Shinjuku). If you missed it, today is flexible enough to add it." }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "teamLab Planets TOKYO DMM", description: "One of Tokyo's must-do experiences — a barefoot walk through immersive digital art installations. You wade through water, walk on mirrors, and get surrounded by infinite digital flowers and koi. Toddlers are MESMERIZED. It's safe for kids (shallow water, soft floors). You'll need to carry the 2-year-old in some areas. Bring a change of clothes — you will get wet up to mid-calf.", details: ["Book online in advance — sells out! (planets.teamlab.art)", "¥3,800/adult, FREE for ages 0-3, ¥1,500 ages 4-12", "Go in the evening for fewer crowds and magical lighting", "Barefoot experience — bring towel and change of clothes for wet areas", "Lockers provided for bags and shoes", "Allow 60-90 min · Fully accessible paths (but no strollers inside)"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Toyosu Manyo Club Area / Toyosu Food Court", description: "After teamLab (which is in Toyosu), grab dinner at the nearby Toyosu food court or restaurants. The Toyosu Manyo Club is a 24-hour onsen/spa resort — you could even do a foot bath with the kids after dinner for ultimate relaxation.", meta: "¥2,000-3,000pp for dinner · Toyosu Manyo Club: ¥2,900/adult entry (kids extra)" }
          ],
          tips: [
            { type: "tip", text: "teamLab Planets has a Garden area that's outdoors — beautiful in May with real flowers + digital art. Don't miss it!" },
            { type: "tip", text: "Toyosu Manyo Club: if the kids are exhausted, a family onsen soak is the perfect way to end the day. Private family baths available." }
          ]
        }
      ]
    },

    // ========== DAY 5 — MAY 19 — TSUKIJI + GŌTOKUJI + TRAVEL TO OSAKA ==========
    {
      num: 5,
      title: "Tsukiji, Cat Temple & Shinkansen to Osaka",
      neighborhoods: "Tsukiji · Setagaya · Osaka (Namba)",
      date: "May 19",
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: "Tsukiji Outer Market", num: 1, cat: "food", desc: "Tokyo's famous food market — incredible street food" },
        { lat: 35.6590, lng: 139.7747, label: "Tokyo Metropolitan Govt Building", num: 2, cat: "activity", desc: "FREE observation deck — 202m panoramic views" },
        { lat: 35.6455, lng: 139.6421, label: "Gōtokuji Temple", num: 3, cat: "activity", desc: "The lucky cat temple — thousands of maneki-neko" },
        { lat: 34.6687, lng: 135.5013, label: "Osaka Namba", num: 4, cat: "activity", desc: "Arrive at your Osaka base camp!" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tsukiji Outer Market", description: "The original Tokyo fish market's outer market is still thriving — a maze of food stalls and small restaurants. This is a must for foodies. Try fresh sushi, tamagoyaki (egg omelette on a stick — kids love it!), grilled seafood, and fruit. Street food format makes it easy with toddlers. No pork needed — it's all about seafood here!", details: ["Go early (8-9am) for the best experience and fewer crowds", "Must-try: tamagoyaki (sweet egg), fresh uni (sea urchin), grilled scallops", "Stroller-navigable but tight in spots — carriers also work", "Most stalls are cash only · ¥300-500 per snack item", "Ichigo daifuku available here too!"] },
            { title: "Tokyo Metropolitan Government Building", description: "Quick stop for free panoramic views from the 45th floor (202m). Two observation decks — North and South. North deck is usually less crowded. On clear May mornings, Mt. Fuji is visible. Free and fast — elevator takes 55 seconds.", details: ["FREE · North Observation Deck open 9:30am-11pm", "45th floor · 202m high · Elevator takes 55 seconds", "Stroller-friendly · In Shinjuku — near your hotel"] }
          ],
          meals: [
            { type: "🍣 Breakfast", name: "Tsukiji Outer Market (Street Food)", description: "Graze your way through Tsukiji — this IS breakfast. Fresh sushi, tamagoyaki sticks, grilled scallops, fruit cups, and more. Budget about ¥2,000-3,000 per person for a full breakfast of snacking.", meta: "¥2,000-3,000pp · Tsukiji · Cash preferred · Go by 8am" }
          ],
          tips: [
            { type: "tip", text: "Tsukiji vs Toyosu: Toyosu is the new wholesale market (requires early morning auction reservations). Tsukiji Outer Market is easier, more fun with kids, and better for street food." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "Gōtokuji Temple (Cat Temple)", description: "The birthplace of the maneki-neko (lucky beckoning cat)! This serene temple is filled with THOUSANDS of small white lucky cat figurines left as offerings. It's absolutely magical and unique — kids are fascinated by the sea of cats. Buy a small maneki-neko to leave (or take home). The temple is in a quiet residential area — very peaceful.", details: ["Free · Buy maneki-neko figurines at the temple office (¥300-3,000)", "Setagaya area — take the Odakyu line to Gōtoku-ji station, 5 min walk", "Plan 30-45 min · Stroller-friendly on main paths", "Photo opportunity is incredible — the wall of thousands of cats"] }
          ],
          meals: [
            { type: "🍱 Lunch", name: "Ekiben (Train Station Bento)", description: "Grab beautiful ekiben (train station bento boxes) at Tokyo Station before your shinkansen. Tokyo Station has an incredible selection — the bento are works of art. Chicken, seafood, and vegetable options galore. This is a quintessential Japanese experience!", meta: "¥1,000-1,800 per bento · Tokyo Station · Ekiben shops on basement floor and near platforms" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Shinkansen to Osaka!", description: "Take the Tokaido Shinkansen (bullet train) from Tokyo Station to Shin-Osaka — one of the most iconic train rides in the world. The journey is ~2.5 hours and incredibly smooth. Reserve seats in advance (Green Car = first class is worth it with kids). Watch for Mt. Fuji on the right side about 45 min in! Kids love the speed and watching Japan blur past.", details: ["Covered by JR Pass! · Reserve seats at any JR ticket counter", "Tokyo → Shin-Osaka: ~2h30 on Nozomi (or ~2h45 on Hikari if using JR Pass)", "⚠️ JR Pass only covers Hikari and Kodama (NOT Nozomi) — plan accordingly", "Sit on the right side (seats D/E) for Mt. Fuji views", "Strollers: fold and store in overhead rack or last-row space", "Each car has a toilet — many have a larger accessible one with changing table"] },
            { title: "Check Into Osaka Hotel", description: "Arrive at Shin-Osaka, take the Midosuji subway line to Namba/Shinsaibashi area (your base for 5 nights). Check in, drop bags, and head out for your first taste of Osaka!", details: ["Shin-Osaka → Namba: ~15 min on Midosuji line", "Namba/Shinsaibashi = perfect central location for Osaka exploring"] }
          ],
          meals: [
            { type: "🌮 Dinner", name: "Dotonbori Street Food Tour", description: "Welcome to Osaka — Japan's kitchen! Walk along the neon-lit Dotonbori canal and eat your way through: takoyaki (octopus balls), kushikatsu (deep-fried skewers — get chicken/shrimp, skip pork), and okonomiyaki (savory pancake — request no pork, sub seafood). See the famous Glico Running Man sign. Dotonbori at night is ELECTRIC.", meta: "¥2,000-3,000pp for a full street food dinner · Namba · Evening is best for the neon atmosphere" }
          ],
          tips: [
            { type: "tip", text: "Osaka is known as 'Japan's Kitchen' (天下の台所). The food here is heartier, bolder, and cheaper than Tokyo. You're going to eat so well." },
            { type: "tip", text: "Glico Running Man sign — the iconic Dotonbori photo spot. Cross the Ebisubashi Bridge for the classic angle. Best lit after dark." }
          ]
        }
      ]
    },

    // ========== DAY 6 — MAY 20 — OSAKA DAY — AQUARIUM + DOTONBORI ==========
    {
      num: 6,
      title: "Osaka Aquarium & Pokémon Café",
      neighborhoods: "Tempozan · Shinsaibashi · Namba",
      date: "May 20",
      mapPins: [
        { lat: 34.6545, lng: 135.4290, label: "Osaka Aquarium Kaiyukan", num: 1, cat: "activity", desc: "One of the world's best aquariums" },
        { lat: 34.6720, lng: 135.5019, label: "Pokémon Café", num: 2, cat: "food", desc: "Pokémon-themed food and drinks" },
        { lat: 34.6687, lng: 135.5013, label: "Glico Sign", num: 3, cat: "activity", desc: "Dotonbori's iconic running man" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Osaka Aquarium Kaiyukan", description: "One of the world's largest and best aquariums — the central Pacific Ocean tank (9m deep, 5,400 tons of water) is home to whale sharks, manta rays, and thousands of fish. The design spirals down around the central tank — toddlers are mesmerized at every level. Touch pools, penguin exhibits, and jellyfish galleries. Plan 2-3 hours. Fully stroller-accessible.", details: ["¥2,700/adult, FREE under 3, ¥1,200 ages 3-6", "Open 10am-8pm · Go at opening for fewer crowds", "Stroller-friendly — elevators between all levels", "Touch pools: kids can touch sharks and rays!", "Gift shop has adorable whale shark plushies", "The jellyfish room is magical — don't skip it"] }
          ],
          meals: [
            { type: "🍳 Breakfast", name: "Hotel Breakfast or Konbini", description: "Fuel up at the hotel or grab a quick konbini breakfast before heading to the aquarium. FamilyMart and 7-Eleven have surprisingly great options — onigiri, sandwiches, fruit, yogurt, and good coffee.", meta: "¥500-800pp · Any konbini" }
          ],
          tips: [
            { type: "tip", text: "Buy Kaiyukan tickets online to skip the ticket line. The aquarium is in the Tempozan area — take the Chuo Line to Osakako Station (15 min from Namba)." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rest Break + Explore Tempozan", description: "After the aquarium, grab lunch in the Tempozan Harbor Village area. There's a giant Ferris wheel (¥800, great bay views), shopping mall, and LEGOLAND Discovery Center if the kids have energy. Or just head back to the hotel for nap time.", details: ["Tempozan Ferris Wheel: ¥800 · One of the world's largest", "LEGOLAND Discovery Center: ¥2,400 — good for ages 3-10", "Or head back for afternoon nap — no shame in it!"] },
            { title: "Pokémon Café Osaka (Shinsaibashi)", description: "Book well in advance — this themed café serves Pokémon-shaped food (Pikachu curry, Eevee pancakes, Poké Ball desserts). Interactive experience with a dancing Pokémon show. The kids will lose their minds. Reservations open monthly — book the moment they open.", details: ["¥1,650 reservation fee per person (includes place setting)", "Food ordered separately: ¥1,000-2,000 per item", "Book at pokemoncafe-reservation.jp — opens 1 month ahead", "Shows happen hourly — check schedule", "No pork items available — plenty of alternatives"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Tempozan Harbor Village Food Court", description: "Multiple options near the aquarium — family-friendly with kids' menus. Udon, curry, and seafood options all pork-free.", meta: "¥1,000-1,500pp · Tempozan" },
            { type: "🎉 Snack/Dinner", name: "Pokémon Café", description: "This doubles as your late afternoon snack or early dinner — the portions are decent and the experience is the main event.", meta: "¥3,000-5,000pp total · Shinsaibashi · Reservations required" }
          ],
          tips: [
            { type: "tip", text: "Pokémon Café reservations are HARD to get — book exactly when they open (usually the 1st of the month for the following month). Have someone try at midnight JST." }
          ]
        }
      ]
    },

    // ========== DAY 7 — MAY 21 — KYOTO DAY TRIP 1 — FUSHIMI INARI + ARASHIYAMA ==========
    {
      num: 7,
      title: "Kyoto Day Trip: Fushimi Inari & Arashiyama",
      neighborhoods: "Fushimi · Arashiyama · Sagano",
      date: "May 21",
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Taisha", num: 1, cat: "activity", desc: "Thousands of vermillion torii gates — ICONIC" },
        { lat: 35.0094, lng: 135.6722, label: "Arashiyama Bamboo Forest", num: 2, cat: "activity", desc: "Walk through towering bamboo groves" },
        { lat: 35.0065, lng: 135.6668, label: "Kimono Forest", num: 3, cat: "activity", desc: "LED pillars with kimono fabric — beautiful" },
        { lat: 35.0282, lng: 135.6656, label: "Otagi Nenbutsu-ji", num: 4, cat: "activity", desc: "1,200 whimsical stone figures — enchanting" },
        { lat: 35.0104, lng: 135.6732, label: "Arashiyama Monkey Park", num: 5, cat: "activity", desc: "Monkeys on a mountain! Kids love it" },
        { lat: 35.0125, lng: 135.6740, label: "Miffy Sakura Kitchen", num: 6, cat: "food", desc: "Adorable Miffy-themed bakery and café" }
      ],
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            { title: "Fushimi Inari Taisha", description: "Japan's most iconic shrine — the endless tunnel of 10,000+ vermillion torii gates winding up Mt. Inari. GO EARLY (before 8am) to have the gates nearly to yourself for photos. You don't need to climb the full mountain (2-3 hours) — the first 20 minutes of the torii trail gives you the best photos and is stroller-navigable. The atmosphere is magical in the morning mist.", details: ["FREE · Open 24 hours · JR Inari Station (2 min walk)", "Osaka → Fushimi Inari: ~45 min by JR train (covered by JR Pass)", "First 20 min of the trail = best photo spots + stroller-doable", "The full mountain hike is 2-3 hours — skip with toddlers", "Fox statues everywhere — Inari's messenger. Kids love them!", "⚠️ Steps begin about 10 min up — turn around here with strollers"] }
          ],
          meals: [
            { type: "🍡 Breakfast/Snack", name: "Street Food at Fushimi Inari", description: "The approach street has great snacks — try kitsune senbei (fox-shaped rice crackers), inari sushi (sweet tofu pouches — no pork!), and matcha soft serve.", meta: "¥200-500 per item · Cash preferred" }
          ],
          tips: [
            { type: "tip", text: "Fushimi Inari → Arashiyama: take JR Inari → JR Saga-Arashiyama (~30 min with transfer at Kyoto Station). Covered by JR Pass." }
          ]
        },
        {
          label: "Late Morning / Afternoon",
          activities: [
            { title: "Arashiyama Bamboo Forest", description: "Walk through the soaring bamboo groves — one of Japan's most otherworldly experiences. The sound of wind through bamboo is unforgettable. The main path is flat and stroller-friendly. Go early or during lunch for fewer crowds. In May, the bamboo is lush and green.", details: ["FREE · Always open · 5 min walk from JR Saga-Arashiyama", "The main path is ~500m — takes 15-20 min", "Stroller-friendly — paved path", "Continue to Tenryu-ji Temple garden (¥500) for a peaceful add-on"] },
            { title: "Kimono Forest", description: "At Randen Arashiyama Station — 600 LED pillars wrapped in Kyoto kimono fabrics. Beautiful during the day, magical lit up at dusk. Free to walk through, great for toddler wandering.", details: ["FREE · At Randen Arashiyama Station", "Best lit up in the evening, but beautiful anytime"] },
            { title: "Arashiyama Miffy Sakura Kitchen", description: "The cutest bakery in Arashiyama! Miffy-shaped buns, sakura-flavored treats, and character-themed drinks. Toddler paradise. On the main shopping street near the bamboo forest.", details: ["Main shopping street · ¥300-600 per item", "Miffy bread buns are too cute to eat (but do eat them)"] },
            { title: "Arashiyama Monkey Park Iwatayama", description: "Climb the short trail (~20 min uphill) to the monkey park where 120+ Japanese macaques roam free. You can feed them from inside an enclosed shelter (they're outside — you're in the cage!). Kids love it. ⚠️ The trail is steep with stairs — you'll need to carry toddlers or use carriers (no strollers).", details: ["¥550/adult, ¥250/child 4-15 · Opens 9am", "⚠️ 20-min uphill climb — NO strollers, carriers only", "Feeding pellets: ¥100 per bag", "Amazing Kyoto panoramic views from the top!", "Monkeys are wild but used to humans — follow rules (no eye contact, don't touch)"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Men-ya Inoichi Ramen (Kyoto)", description: "Kyoto chicken-broth ramen — rich, flavorful, and 100% pork-free. Their chicken paitan (creamy chicken broth) is legendary. Request no pork toppings to be safe. Easy walk from the Arashiyama area.", meta: "¥900-1,200pp · Arashiyama area · Popular — expect a short wait" }
          ],
          tips: [
            { type: "tip", text: "Otagi Nenbutsu-ji is a 20-min walk north of the bamboo forest — 1,200 stone statues each with unique expressions. If the family has energy, it's incredibly charming and almost empty of tourists." }
          ]
        },
        {
          label: "Late Afternoon",
          activities: [
            { title: "Otagi Nenbutsu-ji (Optional — if energy allows)", description: "A hidden gem temple with 1,200 stone rakan (Buddhist disciple) statues — each carved by amateur sculptors with completely unique, often humorous expressions. Some are laughing, some meditating, some playing instruments. Kids love finding funny faces. It's a 20-minute walk past the bamboo forest, and usually nearly empty.", details: ["¥300 entrance · Usually very few tourists", "1,200 unique stone figures — each face is different", "Great for kids — like a stone figure treasure hunt"] },
            { title: "Kimono Rental Experience", description: "Rent kimonos/yukatas in Arashiyama and walk around the bamboo forest area in traditional dress. Many shops rent tiny kids' kimonos too — the cutest family photo opportunity. Rentals include hair styling. This is one of Kyoto's most memorable experiences.", details: ["¥3,000-5,000pp for full-day rental · Kids' sizes available", "Includes kimono, obi, accessories, and basic hair styling", "Return by closing time (usually 5-6pm)", "Book in advance during busy season — many shops on the main road"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Osaka Namba Dinner (Back at Base)", description: "Head back to Osaka (~50 min from Arashiyama) and grab dinner near the hotel. Try okonomiyaki (savory pancake — ask for seafood/no pork version) at a local spot. Osaka-style okonomiyaki is mixed together, Hiroshima-style is layered.", meta: "¥1,000-1,500pp · Namba area" }
          ],
          tips: [
            { type: "tip", text: "Kyoto day trips from Osaka: JR Osaka → JR Kyoto is ~30 min by special rapid (free with JR Pass). Budget ~1 hour each way including station walking." }
          ]
        }
      ]
    },

    // ========== DAY 8 — MAY 22 — NARA DAY TRIP ==========
    {
      num: 8,
      title: "Nara Day Trip: Deer, Temples & Tea",
      neighborhoods: "Nara Park · Naramachi · Fushimi (if missed)",
      date: "May 22",
      mapPins: [
        { lat: 34.6851, lng: 135.8430, label: "Nara Park", num: 1, cat: "activity", desc: "Friendly bowing deer — toddler paradise!" },
        { lat: 34.6821, lng: 135.8399, label: "Manyo Botanical Gardens", num: 2, cat: "activity", desc: "Japan's oldest botanical garden" },
        { lat: 34.6810, lng: 135.8380, label: "Boksburg Market", num: 3, cat: "food", desc: "Ice cream bouquet and local treats" },
        { lat: 34.6890, lng: 135.8398, label: "Todai-ji Temple", num: 4, cat: "activity", desc: "World's largest wooden building + giant Buddha" },
        { lat: 34.6805, lng: 135.8300, label: "Rokujuan Teahouse", num: 5, cat: "food", desc: "Traditional tea ceremony experience" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Nara Park & Deer", description: "Over 1,000 sacred deer roam freely in this beautiful park — and they BOW to you when you offer them deer crackers! This is absolute toddler paradise. The deer are gentle (mostly!) and incredibly photogenic. Buy shika senbei (deer crackers, ¥200) and watch the kids' faces light up. The park is massive, flat, and stroller-friendly.", details: ["FREE park entry · Deer crackers ¥200", "Deer are most gentle in the morning — less hangry", "⚠️ Some deer can be pushy about crackers — hold food high and break into pieces", "Stroller-friendly paths throughout the park", "The deer are a protected national treasure — don't chase or ride them", "Osaka → Nara: ~45 min by Kintetsu railway from Namba"] },
            { title: "Todai-ji Temple", description: "Inside Nara Park — this massive wooden structure houses a 15m-tall bronze Buddha. It's the world's largest wooden building. Kids are awed by the sheer scale. There's a pillar with a hole the same size as the Buddha's nostril — tradition says crawling through brings enlightenment. Kids love trying!", details: ["¥600/adult, ¥300/child · Inside Nara Park", "The nostril pillar hole: kids can crawl through!", "World's largest wooden building — genuinely awe-inspiring", "Stroller-friendly to the entrance — leave stroller at the steps"] }
          ],
          meals: [
            { type: "🍳 Breakfast", name: "Hotel breakfast then early start", description: "Eat at the hotel and head out early to Nara — the deer are calmer in the morning and the park is less crowded.", meta: "Leave by 8:30am for best experience" }
          ],
          tips: [
            { type: "tip", text: "Namba → Nara: Kintetsu Limited Express is the fastest (~35 min). Regular Kintetsu Nara Line is ~45 min and cheaper. JR also goes to Nara but the Kintetsu station is closer to the deer park." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Manyo Botanical Gardens", description: "Japan's oldest botanical garden, featuring plants mentioned in the ancient Manyōshū poetry collection. Peaceful, beautiful, and a welcome break from the deer chaos. Winding paths through curated gardens — stroller-friendly on main routes.", details: ["Inside Nara Park area · ¥500", "Peaceful alternative to the busy deer areas", "Beautiful in May — irises and peonies in bloom"] },
            { title: "Boksburg Market & Ice Cream Bouquet", description: "A charming local market area where you can get the famous ice cream bouquet — scoops of ice cream arranged like a flower bouquet. Ridiculously photogenic and delicious. Various local snacks and treats available too.", details: ["Near Nara Park · ¥500-800 for ice cream bouquet", "Multiple flavors — matcha, strawberry, sweet potato are popular"] },
            { title: "Rokujuan Teahouse", description: "Experience a casual Japanese tea ceremony in a traditional setting. Some teahouses offer family-friendly sessions where kids can try matcha and wagashi (traditional sweets). The structured ritual is fascinating for adults, and kids love the colorful sweets.", details: ["¥800-1,500pp for tea + sweet", "Casual atmosphere — not a formal ceremony", "Tatami seating — toddlers can sit on cushions or laps"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Naramachi Area Restaurant", description: "The charming Naramachi district near the park has great lunch options — try kakinoha sushi (sushi wrapped in persimmon leaves — Nara's specialty, no pork!) or curry udon.", meta: "¥1,000-1,500pp · Naramachi" }
          ],
          tips: [
            { type: "tip", text: "Nishiki robe + photoshoot: if you'd like traditional kimono photos, many rental shops in Nara offer this near the park. Book in advance for family sets." }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Return to Osaka & Evening Walk", description: "Head back to Osaka (45 min from Nara). If the family still has energy, walk along the Dotonbori canal at night — it's a completely different vibe after dark with all the neon signs reflected in the water. Or just grab dinner and rest — you've earned it.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Kushikatsu in Namba", description: "Try Osaka's famous kushikatsu — deep-fried skewers on sticks. Choose chicken, shrimp, vegetables, cheese — skip the pork skewers. The batter is light and crispy. Rule: NO double-dipping in the communal sauce!", meta: "¥1,500-2,500pp · Namba/Shinsekai area · Fun interactive dining" }
          ],
          tips: [
            { type: "tip", text: "If you haven't done kimono rental yet, Nara is a beautiful (and less crowded) place to do it. The deer + kimono photos are incredible." }
          ]
        }
      ]
    },

    // ========== DAY 9 — MAY 23 — KYOTO DAY TRIP 2 — GION + OKAZAKI + SHOPPING ==========
    {
      num: 9,
      title: "Kyoto Day Trip: Gion, Okazaki & Higashiyama",
      neighborhoods: "Gion · Okazaki · Higashiyama · Shinsaibashi",
      date: "May 23",
      mapPins: [
        { lat: 35.0037, lng: 135.7785, label: "Gion District", num: 1, cat: "activity", desc: "Kyoto's famous geisha district" },
        { lat: 35.0146, lng: 135.7841, label: "Okazaki Sakura Corridor", num: 2, cat: "activity", desc: "Beautiful canal-side walking area" },
        { lat: 34.6720, lng: 135.5019, label: "Shinsaibashi Shopping", num: 3, cat: "activity", desc: "Osaka's premier shopping street" },
        { lat: 34.6700, lng: 135.5060, label: "Onitsuka Tiger Osaka", num: 4, cat: "activity", desc: "Custom embroidery available" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Gion District Walk", description: "Kyoto's most atmospheric neighborhood — traditional wooden machiya houses, stone-paved streets, and if you're lucky, a glimpse of a geiko or maiko heading to an appointment. Walk along Hanamikoji-dori, the main street of Gion. Early morning is peaceful and tourist-free. The architecture alone is worth the visit — this is the Kyoto of your imagination.", details: ["Free to walk · Best in early morning or evening", "Hanamikoji-dori is the main geisha district street", "Be respectful — don't chase or block geiko/maiko", "Stroller-friendly on main streets", "Many beautiful tea houses and traditional shops"] },
            { title: "Okazaki Sakura Corridor", description: "A beautiful canal-side walk in the Okazaki area — lined with cherry trees (beautiful even without blossoms in May — lush green canopy). The area connects several major temples and the Kyoto Municipal Museum of Art. Peaceful, shaded, and stroller-perfect.", details: ["Free · Beautiful year-round (green canopy in May)", "Near Heian Shrine — worth a quick look (massive red torii gate)", "Flat canal-side paths — easy stroller pushing"] }
          ],
          meals: [
            { type: "🍵 Breakfast", name: "Traditional Kyoto Cafe in Gion", description: "Find a small café on the Gion side streets for a Japanese-style morning — matcha, hojicha, and simple breakfast sets. The atmosphere in Gion's back streets is uniquely Kyoto.", meta: "¥800-1,500pp · Gion" }
          ],
          tips: [
            { type: "tip", text: "Gion tip: Hanamikoji-dori has photography restrictions in parts — respect the signs. Side streets are equally beautiful and less restricted." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Return to Osaka — Shopping & Rest", description: "Head back to Osaka by early afternoon. Use this time for shopping, souvenirs, and any missed experiences. This is your last full day — soak it in!", details: [] },
            { title: "Shinsaibashi Shopping Street", description: "Osaka's premier covered shopping arcade — nearly 600m of shops, from international brands to local boutiques. The covered arcade means rain-proof shopping and stroller-friendly flat surfaces. Don Quijote (Donki) is here too for last-minute souvenirs.", details: ["Covered arcade — weather-proof shopping", "Connected to Dotonbori at the south end", "Great for souvenirs, clothes, and snacks"] },
            { title: "Onitsuka Tiger Store", description: "If you haven't hit the Ginza location, the Osaka Shinsaibashi store also offers custom embroidery on shoes — a unique Japan-only souvenir. Takes about 30 minutes.", details: ["Shinsaibashi area · Custom embroidery service", "Japan-exclusive colorways available", "~30 min for embroidery customization"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Ichiran Ramen (Chicken Broth)", description: "Ichiran is famous for their individual booth ramen experience — you customize your order on a form. Their Osaka locations offer chicken-based tonkotsu alternatives. The booth system is actually great with toddlers (contained!). Confirm no pork with staff.", meta: "¥1,000-1,500pp · Multiple Osaka locations" },
            { type: "🍽️ Farewell Dinner", name: "Dotonbori Last Night Feast", description: "Last night in Osaka — go all out! Hit your favorite spots from the trip or try new ones. Must-try if you haven't: takoyaki, chicken kushikatsu, seafood okonomiyaki. Walk the Dotonbori strip one more time and soak in the neon.", meta: "¥3,000-5,000pp · Dotonbori/Namba" }
          ],
          tips: [
            { type: "tip", text: "Pack souvenirs in your suitcase tonight — tomorrow is departure day! Buy a Japan Post shipping box from any post office to ship extras home (¥2,000-5,000 to US, takes 1-2 weeks by surface)." }
          ]
        }
      ]
    },

    // ========== DAY 10 — MAY 24 — DEPARTURE ==========
    {
      num: 10,
      title: "Departure Day — Sayonara Japan!",
      neighborhoods: "Osaka · Kansai International Airport",
      date: "May 24",
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: "Namba Station", num: 1, cat: "activity", desc: "Train to airport" },
        { lat: 34.4320, lng: 135.2304, label: "Kansai International Airport", num: 2, cat: "activity", desc: "Fly home from KIX" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Last Morning in Japan", description: "Depending on your flight time, enjoy a final konbini breakfast or hotel meal. Take a last walk around the Namba area. Visit FamilyMart or 7-Eleven one final time for snacks, kit-kats (Japan-exclusive flavors make great gifts!), and treats for the flight.", details: ["FamilyMart & 7-Eleven: grab Japan-exclusive Kit-Kats, Pocky, and snacks as gifts", "Japanese convenience store onigiri one last time — you'll miss them", "Check out of hotel — most have luggage storage if your flight is later"] },
            { title: "Travel to Kansai International Airport", description: "Take the Nankai Rapi:t express from Namba Station to KIX — a cool retro-futuristic blue train that kids will love. The journey is ~38 minutes. Or take the JR Haruka from Tennoji (covered by JR Pass if still valid). Arrive at the airport 3 hours before international flights.", details: ["Nankai Rapi:t: ¥1,450/adult · 38 min to KIX · NOT covered by JR Pass", "JR Haruka: ~50 min from Tennoji · Covered by JR Pass", "KIX has excellent duty-free shopping — matcha, snacks, sake", "KIX Terminal 1 has a kids' play area near Gate 25"] }
          ],
          meals: [
            { type: "🍱 Breakfast/Lunch", name: "Airport Dining at KIX", description: "Kansai Airport has great restaurants — grab one last Japanese meal before flying. Udon, curry, sushi — many options. The pre-security food court is solid, and there are options after security too.", meta: "¥1,000-2,000pp · KIX" }
          ],
          tips: [
            { type: "tip", text: "Tax-free shopping at KIX duty free: Japanese whisky, matcha, cosmetics, and Kit-Kats are popular last-minute gifts." },
            { type: "tip", text: "You did it — 10 days in Japan with toddlers! That's an achievement. The kids won't remember everything, but the photos (and the joy on their faces with the Nara deer) will last forever. お疲れ様でした! (Otsukaresama deshita — You worked hard, well done!)" }
          ]
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
