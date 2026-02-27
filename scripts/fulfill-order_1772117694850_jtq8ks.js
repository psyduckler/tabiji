const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772117694850_jtq8ks',
  email: 'speak@kaeko.us',
  destination: 'Tokyo, Japan',
  start_date: '2026-04-27',
  end_date: '2026-05-02',
  startDate: '2026-04-27',
  endDate: '2026-05-02',
  groupSize: 2,
  group_size: '2',
  amount: '0.00',
  requests: 'Vegetarian, want to see gardens, open air architectural museum, tech-savvy couple, not big shoppers but might want some clothing items as continuing on to Australia for 6 weeks'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Gardens, Grids & Golden Light',
  subtitle: '6 days in Tokyo for two — ancient gardens, open-air architecture, vegetarian feasts & quiet wonder before Australia',
  description: "Late April in Tokyo is a miracle of timing. The last cherry blossoms cling to branches in Shinjuku Gyoen while fresh green leaves push through everywhere else — the city exists in that brief, luminous gap between spring's peak and summer's approach. Golden Week begins during your stay, filling the streets with a festive energy that's distinctly Japanese: orderly chaos, families in their best clothes, food stalls appearing on every corner. This itinerary is built for a tech-savvy couple who'd rather wander a 300-year-old garden than a department store, who want to eat extraordinary vegetarian food in a city that takes vegetables as seriously as it takes everything else, and who are curious about the strange, beautiful intersection of tradition and technology that makes Tokyo unlike anywhere on Earth. You'll explore the Edo-Tokyo Open Air Architectural Museum (relocated historic buildings you can walk through), lose yourselves in teamLab's digital dreamscapes, eat shōjin ryōri (Buddhist temple cuisine) that will permanently change your understanding of what vegetables can do, and find moments of absolute stillness in gardens that have been cultivated for centuries — all within a city of 14 million people moving at full speed around you.",
  duration: '6 days',
  dates: 'Apr 27 – May 2, 2026',
  budget: '$–$$',
  pace: 'Relaxed–Moderate',
  bestFor: 'Couples · Garden Lovers · Vegetarians · Culture Seekers',

  highlights: [
    'Shinjuku Gyoen National Garden — 144 acres of French, English & Japanese gardens in the heart of Tokyo',
    'Edo-Tokyo Open Air Architectural Museum — 30 relocated historic buildings from Edo to Shōwa era, walkable',
    'Shōjin ryōri (Buddhist temple cuisine) — multi-course vegetarian art at Daigo near Tokyo Tower',
    'teamLab Borderless at Azabudai Hills — immersive digital art that responds to your presence',
    'Meiji Jingū inner garden & iris fields — 170,000 trees donated from across Japan, hidden forest in Shibuya',
    'Yanaka & Nezu — Tokyo\'s most atmospheric old neighborhood, untouched by war, full of temples and cats',
    'Koishikawa Kōrakuen — Edo-period strolling garden with miniature landscapes of famous Chinese and Japanese scenes',
    'Shimokitazawa vintage shops — curated secondhand clothing perfect for pre-Australia wardrobe building',
    'Akihabara electric town — for the tech-curious: retro gaming, electronics, maker culture',
    'Golden Week atmosphere — Japan\'s biggest holiday week, festivals and energy everywhere'
  ],

  essentials: [
    {
      title: '🌸 Golden Week (Apr 29 – May 5)',
      text: 'Your trip overlaps with Golden Week — Japan\'s biggest holiday stretch. Apr 29 (Shōwa Day), May 3 (Constitution Day), May 4 (Greenery Day), May 5 (Children\'s Day). Museums and gardens will be busier than usual, but the festive atmosphere is wonderful. Arrive early at popular spots (before 10am). Some smaller restaurants may close — book dinner reservations in advance. Trains run on holiday schedules. The upside: street festivals, special events, and a joyful national mood.'
    },
    {
      title: '🥬 Vegetarian Eating in Tokyo',
      text: 'Tokyo is more vegetarian-friendly than its reputation suggests — you just need to know where to look. Shōjin ryōri (Buddhist temple cuisine) is entirely plant-based and exquisite. Many ramen shops offer vegetable broth options. Indian and Nepali restaurants are everywhere and reliably vegetarian. Use the HappyCow app to find dedicated veggie spots. Key phrase: "Niku nashi, sakana nashi, dashi mo yasai dake de onegaishimasu" (no meat, no fish, vegetable broth only please). Convenience stores (7-Eleven, Lawson) carry onigiri with seaweed/plum fillings, edamame, and salads. Be aware that standard dashi (soup stock) contains bonito — always ask.'
    },
    {
      title: '🚃 Getting Around',
      text: 'Get a 72-hour Tokyo Subway Ticket (¥1,500) for your first 3 days, then use a Suica/Pasmo IC card (tap-and-go, works on all trains, buses, and convenience stores). Tokyo Metro + JR Yamanote Line covers 95% of what you need. For the Edo-Tokyo Open Air Architectural Museum in Koganei, take the JR Chūō Line from Shinjuku (~25 min to Musashi-Koganei station, then bus). Google Maps transit directions are flawless in Tokyo.'
    },
    {
      title: '🏨 Where to Stay',
      text: 'For garden lovers on a budget: stay in Shinjuku (walking distance to Gyoen, great transit hub) or Yanaka/Nippori area (atmospheric, affordable, old Tokyo charm). A well-reviewed business hotel or ryokan-style guesthouse runs ¥8,000-15,000/night ($55-100). Booking.com and Agoda have the best Tokyo hotel inventory. Consider one night at a traditional ryokan with onsen — Sadachiyo in Asakusa is affordable and authentic.'
    },
    {
      title: '💰 Budget Tips',
      text: 'Tokyo is surprisingly affordable if you eat like locals do. Convenience store meals: ¥300-600 ($2-4). Ramen/udon: ¥800-1,200 ($5-8). Department store basement (depachika) food halls: incredible quality at ¥500-1,500. Train fares: ¥170-400 per ride. Museum entry: ¥400-1,600. Your biggest expenses will be the shōjin ryōri dinner (~¥5,000-8,000pp) and teamLab (~¥3,800pp). A couple can absolutely do Tokyo well on $150/day including accommodation.'
    },
    {
      title: '🧳 Packing for Tokyo → Australia',
      text: 'Late April Tokyo: 15-22°C (60-72°F), occasional rain. Light layers, a rain jacket, comfortable walking shoes (you\'ll walk 15,000+ steps/day). Since you\'re continuing to Australia for 6 weeks, pack light and use Shimokitazawa\'s vintage shops to pick up unique pieces. Japan Post will ship a box home for you cheaply if you overbuy. Coin laundry (コインランドリー) is everywhere and cheap (¥300-500/load).'
    }
  ],

  days: [
    // ========== DAY 1 ==========
    {
      num: 1,
      date: '2026-04-27',
      neighborhoods: 'Shinjuku · Shinjuku Gyoen',
      title: 'Arrival & Shinjuku Gyoen at Golden Hour',
      description: "Land in Tokyo and ease into the city gently. After settling into your hotel in Shinjuku, walk straight to Shinjuku Gyoen — one of the world's great urban gardens. In late April, the cherry blossoms may still linger on late-blooming varieties while wisteria begins to drape its purple curtains. The garden is 144 acres of perfection: a formal French section, a rolling English landscape, and a contemplative Japanese strolling garden with tea houses over ponds. End the day in Shinjuku's neon glow with a vegetarian ramen that will make you question everything you thought about soup.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive at Narita or Haneda & Transfer to Shinjuku',
              description: "Touch down and grab your Suica/Pasmo IC card at the airport station — you'll use it for everything. Narita Express to Shinjuku takes ~80 minutes; from Haneda, the Keikyu Line or monorail gets you there in ~40 minutes. Drop bags at your hotel and resist the urge to nap. The best cure for jet lag is sunlight and walking.",
              details: [
                '✈️ Narita: Narita Express (N\'EX) ¥3,250 to Shinjuku · 80 min',
                '✈️ Haneda: Keikyu Line ¥300 to Shinagawa, then JR to Shinjuku · 40 min total',
                '💳 Buy Suica card at any JR station ticket machine — load ¥3,000 to start',
                '📱 Pocket WiFi or eSIM recommended — order before departure for airport pickup'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "Walk from your hotel to one of Tokyo's most beautiful spaces. Shinjuku Gyoen is 144 acres of meticulously maintained gardens — three distinct styles in one park. The Japanese Traditional Garden has a large pond with islands, winding paths, and tea houses. The French Formal Garden features symmetrical plane trees and roses. The English Landscape Garden is open lawns bordered by enormous trees. In late April, late-blooming cherry varieties (Kanzan, Ichiyō) may still be in flower, and the wisteria trellises are starting to bloom. The greenhouse holds tropical plants from Okinawa. Take your time — this is a place for slow wandering.",
              details: [
                '🌿 Open 9am-6pm (last entry 5:30pm) · ¥500 entry · Closed Mondays',
                '🌸 Late April: late cherry varieties + early wisteria — a beautiful overlap',
                '🍵 Rakuutei Tea House: matcha and wagashi (traditional sweet) for ¥700 — overlooking the pond',
                '📸 The Japanese garden pond with the NTT Docomo Tower behind it is the iconic shot',
                '🚫 No alcohol allowed — this keeps the atmosphere peaceful and family-friendly'
              ]
            }
          ],
          meals: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Neon Walk — Omoide Yokochō & Kabukichō',
              description: "As night falls, Shinjuku transforms. Walk through Omoide Yokochō (Memory Lane) — a narrow alley of tiny yakitori stalls unchanged since the post-war era, smoke and lanterns and shouting cooks. Then cross to Kabukichō for Tokyo's most overwhelming neon spectacle. The new Kabukichō Tower and the Godzilla head on the Hotel Gracery are pure cyberpunk. This is the Tokyo of your imagination, and it's real.",
              details: [
                '🏮 Omoide Yokochō: free to walk through · Most stalls seat 6-8 people',
                '🦖 Godzilla Head: visible from the street on Hotel Gracery, Kabukichō',
                '📸 Best neon photography: the narrow alleys between Kabukichō 1-chōme buildings',
                '🌃 The pedestrian crossing at Shinjuku Station south exit is its own spectacle'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Afuri Ramen — Shinjuku',
              description: "Afuri serves a yuzu shio (citrus salt) ramen with a light, fragrant broth that works beautifully in their vegan version. The vegan ramen uses kelp and vegetable dashi with the same bright yuzu finish. It's clean, elegant, and deeply satisfying — the opposite of heavy tonkotsu. Perfect first meal in Tokyo.",
              meta: '💰 $ · 📍 Shinjuku · Vegan ramen ¥1,100 · No reservations — join the queue'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Jet lag strategy: stay awake until at least 9pm local time on arrival day. The garden walk and evening exploration will help. If you absolutely must nap, set an alarm for 30 minutes max. Drink water constantly — flights and Tokyo walking dehydrate you fast.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7103, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'World\'s busiest station — your home base' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 2, cat: 'attraction', desc: '144 acres — French, English & Japanese gardens' },
        { lat: 35.6936, lng: 139.7034, label: 'Omoide Yokochō', num: 3, cat: 'food', desc: 'Memory Lane — post-war yakitori alleys' },
        { lat: 35.6951, lng: 139.7029, label: 'Kabukichō', num: 4, cat: 'attraction', desc: 'Neon heart of Shinjuku — Godzilla head & nightlife' },
        { lat: 35.6930, lng: 139.7044, label: 'Afuri Ramen', num: 5, cat: 'food', desc: 'Yuzu shio vegan ramen — light, bright, perfect' }
      ]
    },

    // ========== DAY 2 ==========
    {
      num: 2,
      date: '2026-04-28',
      neighborhoods: 'Koganei · Kichijōji · Inokashira Park',
      title: 'Edo-Tokyo Open Air Architectural Museum & Kichijōji',
      description: "Today is built around the place you specifically asked for: the Edo-Tokyo Open Air Architectural Museum in Koganei. This extraordinary outdoor museum has 30 relocated historic buildings — Edo-period farmhouses, Meiji-era shops, a Taishō bathhouse, a Shōwa-era stationery store — that you walk through freely. Hayao Miyazaki used it as reference for Spirited Away. Afterward, explore nearby Kichijōji and Inokashira Park — one of Tokyo's most charming neighborhoods.",
      timeBlocks: [
        {
          label: 'Morning & Afternoon',
          activities: [
            {
              title: 'Edo-Tokyo Open Air Architectural Museum (江戸東京たてもの園)',
              description: "Take the JR Chūō Line from Shinjuku to Musashi-Koganei station (~25 min), then a short bus ride to Koganei Park. The museum sits inside the park — 30 historic buildings relocated here and meticulously restored. The eastern zone recreates a commercial street from the Meiji-Taishō era: a soy sauce shop, a flower shop, a hardware store, a stationery shop with original inventory still on shelves. The western zone has grand residences and rural farmhouses with thatched roofs. The centerpiece is the Kodakara-yu bathhouse — a Shōwa-era sentō with original tilework, vaulted ceilings, and painted Mt. Fuji murals. Miyazaki fans: the bathhouse and the commercial street directly inspired settings in Spirited Away. Plan 2-3 hours minimum.",
              details: [
                '🏛️ Open 9:30am-5:30pm (Apr-Sep) · ¥400 entry · Closed Mondays',
                '🚃 JR Chūō Line: Shinjuku → Musashi-Koganei (25 min, ¥390) · Bus 5 min to park',
                '🎬 Spirited Away connections: Kodakara-yu bathhouse → Yubaba\'s bathhouse; Shitamachi street → spirit town',
                '📸 The commercial street at golden hour is magical — arrive early, stay late',
                '🏡 Enter the buildings — sit on tatami, look through windows, imagine the lives lived here',
                '🍵 The museum tea room serves matcha in a restored Meiji-era building'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Museum Tea Room or Koganei Park Bento',
              description: "The museum has a small café in a restored building serving udon and light meals. Alternatively, grab a bento from the convenience store near Musashi-Koganei station and eat in Koganei Park under the trees — the park itself is beautiful, especially in late April with fresh green leaves.",
              meta: '💰 $ · 📍 Inside museum or Koganei Park'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Inokashira Park & Kichijōji',
              description: "From Koganei, take the bus or train to Kichijōji — consistently voted Tokyo's most desirable neighborhood. Inokashira Park is its heart: a wooded park around a large pond, pedal boats shaped like swans, buskers performing on the bridge, couples and families everywhere. The surrounding streets are full of independent cafés, vintage shops, and small galleries. Kichijōji has a village-within-a-city feeling that's irresistible.",
              details: [
                '🌿 Inokashira Park: free entry · The pond is beautiful with spring foliage',
                '🦢 Swan pedal boats: ¥700/30min — touristy but genuinely fun',
                '🛍️ Kichijōji Sun Road & Daiya Street: covered shopping arcades with unique small shops',
                '🎨 The Ghibli Museum is nearby (Mitaka) but requires advance tickets — check availability'
              ]
            }
          ],
          meals: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kichijōji Harmonica Yokochō & Dinner',
              description: "Kichijōji's Harmonica Yokochō is a tangle of narrow alleys packed with tiny bars and restaurants — named because the buildings look like harmonica reeds from above. It's less touristy than Golden Gai and feels more genuinely local. Find a small izakaya and order what looks interesting.",
              details: [
                '🏮 Harmonica Yokochō: north side of Kichijōji Station · Free to wander',
                '🍶 Most bars seat 8-12 people — that\'s the charm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Monk\'s Foods (モンクスフーズ) or Nagi Shokudō',
              description: "Nagi Shokudō in Shibuya is one of Tokyo's best all-vegetarian restaurants — a cozy upstairs space serving a daily-changing set meal (teishoku) of brown rice, miso soup, tofu dish, vegetable sides, and pickles. Simple, beautiful, nourishing. If you stay in Kichijōji, several vegetarian-friendly izakayas line Harmonica Yokochō.",
              meta: '💰 $ · 📍 Shibuya (Nagi) or Kichijōji · Nagi set meal ~¥1,200'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'The Edo-Tokyo Open Air Architectural Museum is genuinely one of Tokyo\'s best-kept secrets. Most tourists never make it out to Koganei. Go on a weekday if possible — even during Golden Week, it\'s less crowded than central Tokyo attractions.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7155, lng: 139.5150, label: 'Edo-Tokyo Open Air Architectural Museum', num: 1, cat: 'attraction', desc: '30 relocated historic buildings — Spirited Away inspiration' },
        { lat: 35.7032, lng: 139.5794, label: 'Kichijōji Station', num: 2, cat: 'transport', desc: 'Tokyo\'s most-loved neighborhood' },
        { lat: 35.6992, lng: 139.5770, label: 'Inokashira Park', num: 3, cat: 'attraction', desc: 'Wooded park with pond, swan boats & buskers' },
        { lat: 35.7040, lng: 139.5790, label: 'Harmonica Yokochō', num: 4, cat: 'food', desc: 'Tiny alley bars and restaurants — local atmosphere' },
        { lat: 35.7100, lng: 139.5200, label: 'Koganei Park', num: 5, cat: 'attraction', desc: 'Spacious green park surrounding the museum' }
      ]
    },

    // ========== DAY 3 ==========
    {
      num: 3,
      date: '2026-04-29',
      neighborhoods: 'Harajuku · Meiji Jingū · Omotesandō · Shibuya',
      title: 'Meiji Shrine Gardens, Harajuku & Shibuya',
      description: "Shōwa Day (national holiday) — Golden Week officially begins. Start in the ancient forest of Meiji Jingū, where 170,000 trees donated from across Japan create a sacred woodland in the middle of Shibuya. The inner garden has iris fields and a serene spring-fed pond. Then contrast ancient with ultra-modern: Harajuku's Takeshita Street, Omotesandō's architectural masterpieces, and Shibuya Crossing — the world's most famous intersection.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingū Shrine & Inner Garden',
              description: "Enter through the massive torii gate on Omotesandō and walk the gravel path through the forest. Meiji Jingū was built in 1920 to honor Emperor Meiji, and its 170-acre forest was planted from scratch with 100,000 trees donated from across Japan — now a mature, old-growth forest harboring species you'd never expect in central Tokyo. The shrine itself is simple, powerful Shintō architecture. Pay ¥500 to enter the Inner Garden (Gyoen) — a secluded strolling garden with iris fields that bloom in June, but in late April the fresh greenery and the spring-fed Kiyomasa's Well are beautiful. This is Tokyo's deepest breath of green.",
              details: [
                '⛩️ Free entry to shrine grounds · Inner Garden ¥500 · Opens at sunrise',
                '🌲 The forest is 170 acres — larger than many national parks in other countries',
                '💒 You may see a traditional Shintō wedding procession — gorgeous and moving',
                '🌿 Inner Garden: koi pond, iris fields (peak June), Kiyomasa\'s Well, wisteria',
                '🙏 At the main hall: toss a coin, bow twice, clap twice, bow once — Shintō prayer etiquette'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Bills Omotesandō',
              description: "The famous Australian-Japanese ricotta pancakes at Bills — fluffy, cloud-like, served with honeycomb butter and banana. A beautiful start to the day, and fitting given you're heading to Australia next. The Omotesandō location has a terrace with tree views.",
              meta: '💰 $$ · 📍 Omotesandō · Pancakes ¥1,800 · Arrive by 9am to avoid queues'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku & Takeshita Street',
              description: "Step out of the shrine forest and into Harajuku — the contrast is the point. Takeshita Street is a narrow, heaving pedestrian alley of youth fashion, crêpe stands, and sensory overload. It's loud, colorful, and pure Tokyo. Beyond Takeshita, explore Cat Street (a quieter, more curated fashion strip) and the backstreets of Ura-Harajuku where independent designers and vintage shops hide.",
              details: [
                '🛍️ Takeshita Street: free to walk · Peak crowded 12-4pm on holidays',
                '🐱 Cat Street: parallel to Takeshita, calmer · Vintage, streetwear, independent brands',
                '🍦 Marion Crêpes: Harajuku institution since 1976 · The strawberry banana is the classic',
                '👗 For pre-Australia clothing: check vintage shops on Cat Street — unique pieces at ¥1,000-5,000'
              ]
            },
            {
              title: 'Omotesandō Architecture Walk',
              description: "Omotesandō is Tokyo's most architecturally stunning boulevard. Every major fashion brand hired a different starchitect: Tadao Ando's concrete meditation for Omotesandō Hills, Toyo Ito's crystalline grid for Tod's, Herzog & de Meuron's glass stack for Prada, SANAA's bubbling glass for Dior. You don't need to buy anything — just walk and look up.",
              details: [
                '🏛️ Prada: Herzog & de Meuron\'s diamond-pane glass — stunning at any angle',
                '🏗️ Tod\'s: Toyo Ito\'s concrete tree branches wrapping the building',
                '🔲 Omotesandō Hills: Tadao Ando — sloping spiral walkway inside',
                '📸 Best architecture photos: mid-afternoon when shadows define the geometries'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Ain Soph Journey — Shinjuku',
              description: "Ain Soph is Tokyo's most beloved vegan restaurant chain. The Shinjuku location serves an extraordinary vegan burger, fluffy vegan pancakes, and seasonal set meals. Everything is beautifully plated and genuinely delicious — not sad substitutes but joyful plant food. Reservations recommended on holidays.",
              meta: '💰 $$ · 📍 Shinjuku 3-chōme · Vegan burger ¥1,650 · Book on Golden Week'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: "Walk from Omotesandō to Shibuya and witness the crossing — up to 3,000 people crossing simultaneously when the light changes, a beautiful organized chaos. Then go up to Shibuya Sky (Shibuya Scramble Square rooftop, 47th floor) for a 360° open-air view of Tokyo at sunset. On clear days, Mt. Fuji appears on the western horizon.",
              details: [
                '🚶 Shibuya Crossing: best viewed from Starbucks 2F (get a window seat) or Shibuya Sky above',
                '🌆 Shibuya Sky: ¥2,000 · Book online in advance · Sunset slot is best',
                '🗻 On clear days, Mt. Fuji visible to the west from the rooftop — stunning at sunset',
                '🐕 Hachikō statue: in front of Shibuya Station — the loyal dog who waited'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'T\'s TanTan — Tokyo Station (or Shibuya branch)',
              description: "T's TanTan serves entirely vegan ramen that's so good most customers don't realize it's vegan. The tantanmen (sesame-chili ramen) is rich, spicy, and deeply savory — made with soy meat and sesame broth. There are branches in Tokyo Station and near Shibuya. It's affordable, fast, and genuinely excellent.",
              meta: '💰 $ · 📍 Tokyo Station Keiyo Street or Jiyūgaoka · Tantanmen ¥980'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Golden Week Day 1 (Shōwa Day) — expect crowds at Meiji Jingū. Arrive before 9am for relative peace. The inner garden is always quieter than the main shrine approach. Shibuya Sky should be booked online in advance — walk-up sells out on holidays.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingū Shrine', num: 1, cat: 'attraction', desc: '170-acre sacred forest & shrine in central Tokyo' },
        { lat: 35.6715, lng: 139.7030, label: 'Harajuku / Takeshita Street', num: 2, cat: 'attraction', desc: 'Youth fashion, crêpes & sensory overload' },
        { lat: 35.6654, lng: 139.7121, label: 'Omotesandō', num: 3, cat: 'attraction', desc: 'Starchitect boulevard — Ando, Ito, Herzog & de Meuron' },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Crossing', num: 4, cat: 'attraction', desc: 'World\'s most famous intersection — 3,000 people per crossing' },
        { lat: 35.6584, lng: 139.7022, label: 'Shibuya Sky', num: 5, cat: 'attraction', desc: '47F rooftop — 360° views, Mt. Fuji at sunset' }
      ]
    },

    // ========== DAY 4 ==========
    {
      num: 4,
      date: '2026-04-30',
      neighborhoods: 'Azabudai Hills · Roppongi · Tōkyō Tower · Zōjō-ji',
      title: 'teamLab Borderless & Shōjin Ryōri Temple Cuisine',
      description: "A day of contrasts: begin in the digital infinity of teamLab Borderless at Azabudai Hills — one of the most extraordinary art experiences on Earth — then slow down completely with shōjin ryōri (Buddhist vegetarian temple cuisine) at Daigo, a two-Michelin-starred restaurant near Tokyo Tower. Between them, explore the temple grounds of Zōjō-ji with Tokyo Tower framed behind it. This is the day that will stay with you longest.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Borderless — Azabudai Hills',
              description: "teamLab Borderless is not a museum — it's a world. 10,000 square meters of dark, labyrinthine space filled with digital art installations that move between rooms, respond to your presence, and merge with each other. Flowers bloom and scatter at your feet. Waterfalls cascade across walls and over your body. Butterflies emerge from your phone screen and fly into the wall projections. The Crystal Universe room is a room of infinite LED lights that you walk through. There is no map and no set path — you wander, get lost, find things, and never see the same artwork twice. For a tech-savvy couple, this is pure magic. Arrive when it opens to avoid peak crowds.",
              details: [
                '🎨 ¥3,800pp · Open 10am-9pm · Book timed entry online in advance',
                '📍 Azabudai Hills Garden Plaza B, Minato-ku',
                '⏱️ Plan 2-3 hours minimum — you\'ll lose track of time',
                '📸 Wear white or light colors — the projections show up on your clothes beautifully',
                '👟 Wear flat shoes — the floor is uneven in places by design',
                '🚫 No tripods or flash photography — phone cameras are fine and encouraged'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Konbini Breakfast (7-Eleven or Lawson)',
              description: "Embrace the konbini (convenience store) experience. Japanese 7-Eleven is nothing like its American counterpart — the onigiri are fresh, the egg sandwiches are impossibly fluffy, and the coffee is excellent. Grab a vegetarian onigiri (ume/plum or kombu/seaweed), a tamago sando (egg sandwich), and a hot coffee. Total: ¥500 ($3.50).",
              meta: '💰 $ · 📍 Any 7-Eleven or Lawson · Open 24/7'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Zōjō-ji Temple & Tokyo Tower',
              description: "Walk from Azabudai to Zōjō-ji, one of Tokyo's most important Buddhist temples — the funerary temple of the Tokugawa shoguns. The main gate (Sangedatsu-mon, 1622) is the oldest wooden structure in Tokyo. Behind the temple, Tokyo Tower rises in its orange-and-white Eiffel-inspired glory — the most photographed composition in the city. The temple grounds are peaceful, with rows of small Jizō statues (protectors of children) wearing red knitted caps and holding toy pinwheels.",
              details: [
                '⛩️ Zōjō-ji: free entry · Open 6am-5pm',
                '🗼 Tokyo Tower: observation deck ¥1,200 · Open 9am-11pm',
                '📸 The view of Tokyo Tower framed through Sangedatsu-mon gate is iconic',
                '👶 Jizō statues: deeply moving — each one placed by parents remembering a lost child'
              ]
            },
            {
              title: 'Roppongi Art Walk',
              description: "Roppongi has evolved from nightlife district to art hub. The Mori Art Museum (52F of Mori Tower) has rotating contemporary exhibitions with stunning city views. The National Art Center Tokyo (Kurokawa Kishō's undulating glass wave building) is architecturally stunning even from outside. If you have energy, both are excellent.",
              details: [
                '🎨 Mori Art Museum: ¥2,000 · Open 10am-10pm · Includes Tokyo City View observation',
                '🏛️ National Art Center: ¥0-1,600 (depends on exhibition) · The café inside is gorgeous',
                '📍 Both within walking distance of Roppongi Station'
              ]
            }
          ],
          meals: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shōjin Ryōri at Daigo — Temple Cuisine Perfection',
              description: "This is the meal of the trip. Daigo has served shōjin ryōri (Buddhist vegetarian temple cuisine) for over 70 years, earning two Michelin stars for food that uses absolutely no animal products. A multi-course kaiseki meal arrives in a sequence of tiny, exquisite dishes: seasonal vegetables prepared dozens of ways, tofu in forms you didn't know existed, simmered yuba (tofu skin), mountain vegetables, pickles, rice, and miso. Each course is a meditation on a single ingredient. The dining rooms overlook a small garden. Book weeks in advance.",
              details: [
                '🍽️ Courses start at ¥5,500 (lunch) / ¥8,800 (dinner) · Dinner 5pm-9pm',
                '📍 Near Akabanebashi Station, Minato-ku · Walk from Tokyo Tower area',
                '📞 Reserve well in advance — especially during Golden Week',
                '🥢 Entirely plant-based — no meat, fish, eggs, dairy, or animal-derived dashi',
                '🧘 Shōjin ryōri originated in Zen Buddhist monasteries — cooking as spiritual practice',
                '👔 Smart casual dress — this is a special occasion restaurant'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Azabudai Hills Food Court — Vegetable-Forward Options',
              description: "Azabudai Hills (where teamLab is) has an excellent food hall. Look for Sougo — a vegetable-forward Japanese restaurant — or grab soba noodles (ask for vegetable broth). The complex is new (opened 2023) and beautifully designed.",
              meta: '💰 $$ · 📍 Azabudai Hills · Various options ¥1,000-2,000'
            },
            {
              type: '🍷 Dinner',
              name: 'Daigo — Shōjin Ryōri',
              description: "Two-Michelin-starred Buddhist temple cuisine — multi-course vegetarian kaiseki that will permanently change your understanding of vegetables. 70+ years of tradition. A spiritual and culinary experience.",
              meta: '💰 $$$ · 📍 Akabanebashi · Dinner courses from ¥8,800 · Reserve in advance'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Book teamLab online at least a week in advance — Golden Week slots sell out. Arrive right at opening (10am) for the most peaceful experience. The installations are best with fewer people. For Daigo, reserve as far ahead as possible — their English website accepts bookings.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7380, label: 'teamLab Borderless — Azabudai Hills', num: 1, cat: 'attraction', desc: 'Immersive digital art — 10,000sqm of wonder' },
        { lat: 35.6586, lng: 139.7516, label: 'Zōjō-ji Temple', num: 2, cat: 'attraction', desc: 'Tokugawa funerary temple — Tokyo Tower framed behind' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 3, cat: 'attraction', desc: 'Orange-and-white icon — 333m observation tower' },
        { lat: 35.6604, lng: 139.7292, label: 'Mori Art Museum', num: 4, cat: 'attraction', desc: '52F contemporary art + Tokyo City View' },
        { lat: 35.6555, lng: 139.7449, label: 'Daigo — Shōjin Ryōri', num: 5, cat: 'food', desc: 'Two Michelin stars — Buddhist vegetarian kaiseki' }
      ]
    },

    // ========== DAY 5 ==========
    {
      num: 5,
      date: '2026-05-01',
      neighborhoods: 'Yanaka · Nezu · Koishikawa Kōrakuen · Akihabara',
      title: 'Old Tokyo Gardens, Temples & Electric Town',
      description: "Explore the Tokyo that survived — Yanaka and Nezu, neighborhoods that escaped the 1945 firebombing and retain their Edo-era street patterns, wooden houses, and unhurried pace. Visit one of Tokyo's finest Edo-period strolling gardens at Koishikawa Kōrakuen, then switch gears entirely with an evening in Akihabara — Tokyo's electric town of retro gaming, anime, and electronics culture. The contrast between morning and evening is the point.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Yanaka & Nezu — Old Tokyo Walking Tour',
              description: "Yanaka is Tokyo's most atmospheric old neighborhood — narrow lanes lined with wooden houses, tiny temples around every corner, cats sunning on stone walls, and an unhurried pace that feels impossible in a 14-million-person city. Start at Nippori Station and walk down Yanaka Ginza — a charming shopping street with family-run businesses: a senbei (rice cracker) maker, a traditional candy shop, a tiny art gallery in someone's living room. Continue to Yanaka Cemetery (surprisingly beautiful — cherry trees line the paths), past dozens of small temples, and down to Nezu Shrine.",
              details: [
                '🚶 Walking route: Nippori Station → Yanaka Ginza → Yanaka Cemetery → Nezu Shrine (~2.5 km)',
                '🐱 Yanaka is famous for cats — they\'re everywhere and thoroughly worshipped',
                '🍘 Try fresh-grilled senbei on Yanaka Ginza — ¥150 from the corner cracker shop',
                '⛩️ There are over 70 temples in the Yanaka area alone — just wander and discover'
              ]
            },
            {
              title: 'Nezu Shrine & Azalea Garden',
              description: "Nezu Shrine is one of Tokyo's oldest (1706) and most beautiful — vermillion torii gates line a path through an azalea garden that blooms spectacularly in late April. The Tsutsuji Matsuri (Azalea Festival) runs mid-April through early May, with 3,000 azalea bushes in 100 varieties covering the hillside in waves of pink, red, white, and purple. The shrine's tunneled torii path is reminiscent of Fushimi Inari in Kyoto but far less crowded.",
              details: [
                '⛩️ Nezu Shrine: free entry · Azalea garden ¥300 during festival · Open 6am-5pm',
                '🌺 Azalea Festival: mid-Apr to early May — timing should be perfect for your visit',
                '⛩️ Torii tunnel: miniature vermillion gates climbing the hillside — beautiful',
                '📸 The azalea hillside with the shrine gate in the background is the shot'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'Kayaba Coffee — Yanaka',
              description: "A century-old wooden house converted into a café, serving thick Japanese-style toast (shokupan) with butter and jam, hand-dripped coffee, and egg sandwiches. The building itself is the attraction — tatami seating upstairs, the scent of old wood, sunlight through paper screens.",
              meta: '💰 $ · 📍 Yanaka, near Nezu Station · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Koishikawa Kōrakuen Garden',
              description: "One of Tokyo's two surviving Edo-period great gardens (built 1629). Koishikawa Kōrakuen is a masterpiece of miniature landscape design — it recreates famous scenic spots from China and Japan in a single strolling circuit. A miniature version of Kyoto's Arashiyama bamboo grove, a recreation of West Lake in Hangzhou, plum groves, iris marshes, and a full moon bridge reflected in the central pond. Unlike Shinjuku Gyoen (which is grand and open), this garden is intimate and poetic — designed for contemplation, not spectacle.",
              details: [
                '🌿 Open 9am-5pm · ¥300 entry · Closed some Mondays',
                '📍 Adjacent to Tokyo Dome — Iidabashi or Kōrakuen Station',
                '🌉 Engetsu-kyō (Full Moon Bridge): stone arch that forms a perfect circle with its reflection',
                '🍁 Created by the Mito branch of the Tokugawa family — for scholars and poets',
                '📸 The central pond with Hōrai-jima island is the classic composition'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sasanoyuki — Nezu (est. 1691)',
              description: "Sasanoyuki has served tofu cuisine for over 330 years — the oldest tofu restaurant in Tokyo. The tofu tasting course includes silken tofu, grilled tofu, tofu dengaku (miso-glazed), yuba (tofu skin), and tofu in broth. Entirely vegetarian if you skip the dashi (ask for kombu dashi). A profound experience of a single ingredient.",
              meta: '💰 $$ · 📍 Negishi, near Uguisudani Station · Tofu course ¥3,300-5,500 · Lunch from 11:30am'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Akihabara — Electric Town',
              description: "From centuries-old gardens to the bleeding edge: Akihabara is Tokyo's electronics and geek culture district. For a tech-savvy couple, this is playground time. Yodobashi Camera Akiba is 9 floors of every gadget imaginable. Super Potato is a retro gaming museum-shop with playable consoles from the 1980s onward. Mandarake sells vintage manga, anime cels, and collectibles. The Radio Kaikan building has floors of specialized electronics and hobby shops. Don't buy anything expensive — just absorb the energy.",
              details: [
                '🎮 Super Potato: 5 floors of retro gaming · 3F has playable arcade machines from the 80s-90s',
                '📱 Yodobashi Camera Akiba: 9 floors · Tax-free for tourists with passport',
                '📚 Mandarake: vintage manga, anime cels, figurines — a collector\'s paradise',
                '🏢 Radio Kaikan: hobby electronics, gashapon machines, specialized tech',
                '🕹️ SEGA arcade: multiple floors of crane games, rhythm games, retro arcade cabinets'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'CoCo Ichibanya Curry — Vegetarian Menu',
              description: "CoCo Curry is Japan's biggest curry chain and they have a full vegetarian menu at select locations (Akihabara has one). Japanese curry is comfort food perfection — thick, sweet, mildly spicy, served over rice with vegetables. Customize your spice level (1-10) and toppings. It's cheap, filling, and exactly what you want after hours of walking.",
              meta: '💰 $ · 📍 Akihabara · Veggie curry ¥750-1,000'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Yanaka is best in the morning when shops are opening and the light is soft. Akihabara is best at night when the neon signs blaze. Plan accordingly. If you want to buy electronics, bring your passport for tax-free shopping at Yodobashi (purchases over ¥5,000).'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7282, lng: 139.7677, label: 'Yanaka Ginza', num: 1, cat: 'attraction', desc: 'Old Tokyo shopping street — family shops, cats, charm' },
        { lat: 35.7220, lng: 139.7620, label: 'Nezu Shrine', num: 2, cat: 'attraction', desc: '1706 shrine — azalea festival, torii tunnel' },
        { lat: 35.7080, lng: 139.7520, label: 'Koishikawa Kōrakuen', num: 3, cat: 'attraction', desc: 'Edo-period strolling garden — miniature landscapes since 1629' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 4, cat: 'attraction', desc: 'Electric Town — retro gaming, electronics, geek culture' },
        { lat: 35.7260, lng: 139.7700, label: 'Kayaba Coffee', num: 5, cat: 'food', desc: 'Century-old wooden café — thick toast & hand-dripped coffee' },
        { lat: 35.7210, lng: 139.7750, label: 'Sasanoyuki', num: 6, cat: 'food', desc: '330-year-old tofu restaurant — vegetarian tasting course' }
      ]
    },

    // ========== DAY 6 ==========
    {
      num: 6,
      date: '2026-05-02',
      neighborhoods: 'Shimokitazawa · Rikugien · Departure',
      title: 'Shimokitazawa Vintage, Rikugien Garden & Farewell',
      description: "Your final day weaves together two last experiences: Shimokitazawa — Tokyo's bohemian village of vintage clothing, independent cafés, and small live music venues — and Rikugien, one of the city's most beautiful and peaceful Edo-period gardens. Since you're heading to Australia for six weeks, Shimokitazawa's vintage shops are perfect for picking up unique pieces. End with a last walk through Rikugien's landscaped poetry, then head to the airport carrying Tokyo with you.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shimokitazawa — Vintage Shopping & Café Culture',
              description: "Shimokitazawa is Tokyo's answer to Brooklyn or Shoreditch — a tangle of narrow streets filled with vintage clothing shops, record stores, independent cafés, and small theaters. For pre-Australia wardrobe building, this is the place. Shops like New York Joe Exchange, Flamingo, and Stick Out sell curated vintage at ¥1,000-5,000 per piece — everything from 90s streetwear to classic denim to unique Japanese brands you won't find anywhere else. The neighborhood runs on creativity and caffeine.",
              details: [
                '🛍️ New York Joe Exchange: huge vintage warehouse — ¥1,000-5,000 per piece',
                '👗 Flamingo: curated vintage — 90s streetwear, denim, one-of-a-kind finds',
                '☕ Bear Pond Espresso: legendary single-shot espresso — no photos, no WiFi, just coffee',
                '🎵 Flash Disc Ranch: vinyl record store — jazz, city pop, ambient',
                '📍 Shimokitazawa Station: Keio Inokashira Line from Shibuya (3 min) or Odakyu from Shinjuku'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Breakfast',
              name: 'City Country City — Shimokitazawa',
              description: "A café above a vintage clothing store, serving hand-dripped coffee and thick toast with seasonal jam. The vibe is records on the turntable, mismatched furniture, and morning light through big windows. Peak Shimokitazawa.",
              meta: '💰 $ · 📍 Shimokitazawa · Opens 11am (brunch timing)'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rikugien Garden — Tokyo\'s Most Poetic Garden',
              description: "Your final garden: Rikugien (Six Poems Garden), built in 1702 by the fifth Tokugawa shogun's advisor. Named after the six principles of Japanese poetry, the garden is designed to be 'read' like a poem as you walk its circular path. Every hill, bridge, stone arrangement, and tree placement references a specific waka poem or scene from The Tale of Genji. The weeping cherry at the entrance is Tokyo's most famous single tree (spring peak is March, but the fresh green canopy in late April is equally moving). The central pond with its islands and miniature mountains is mesmerizing.",
              details: [
                '🌿 Open 9am-5pm · ¥300 entry · Komagome Station (JR Yamanote or Namboku Line)',
                '🌸 The weeping shidare-zakura at the entrance — Tokyo\'s most famous tree',
                '📖 The garden represents 88 scenes from classical Japanese poetry',
                '🍵 Fukiage Tea House: matcha and seasonal wagashi for ¥510 — overlooking the pond',
                '📸 Tsutsuji-chaya viewpoint: the classic composition across the central pond'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Falafel Brothers — Roppongi or Shibuya',
              description: "When you want a break from Japanese food: Falafel Brothers serves the best falafel in Tokyo — crispy outside, green and herby inside, stuffed into warm pita with tahini, pickled vegetables, and harissa. Fully vegan-friendly. Quick, delicious, and a flavor reset before departure.",
              meta: '💰 $ · 📍 Roppongi or Shibuya · Falafel plate ¥1,200'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Tokyo Moments & Airport Departure',
              description: "Pack up and head to the airport, but leave time for one last ritual: a final konbini stop. Stock up on Japanese snacks for Australia — Kit Kat flavors (matcha, strawberry cheesecake), rice crackers, instant miso soup packets, and matcha powder. Japan's convenience stores are world-class and the snacks make perfect gifts. Then board your flight carrying Tokyo with you — the gardens, the neon, the quiet temples, and the memory of vegetables treated like miracles.",
              details: [
                '✈️ Narita: N\'EX from Shinjuku/Shibuya (80 min) · Allow 3 hours before int\'l flight',
                '✈️ Haneda: Keikyu/Monorail from central Tokyo (30-50 min) · Allow 2.5 hours',
                '🍫 Airport Kit Kat shop at Narita has exclusive flavors — last chance!',
                '📦 If you overbought in Shimokitazawa: Japan Post at the airport ships boxes home affordably'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Farewell Dinner',
              name: 'Sougo — Vegetable Kaiseki',
              description: "If you have time before departure, Sougo in Roppongi serves entirely plant-based kaiseki — seasonal vegetables in beautiful multi-course progression. A perfect farewell to Tokyo's vegetarian excellence. If time is tight, the airport has surprisingly good ramen and soba shops.",
              meta: '💰 $$$ · 📍 Roppongi · Course from ¥6,600 · Reserve ahead'
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'If flying to Australia, check your visa (ETA/eVisitor) is sorted. Pack any Japanese snacks in checked luggage — Australia has strict biosecurity. Fresh food, seeds, and wooden items may be confiscated. Processed/sealed snacks are generally fine. Declare everything on the arrival card to avoid fines.'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6613, lng: 139.6680, label: 'Shimokitazawa', num: 1, cat: 'attraction', desc: 'Bohemian village — vintage shops, cafés, live music' },
        { lat: 35.7326, lng: 139.7462, label: 'Rikugien Garden', num: 2, cat: 'attraction', desc: 'Edo-period poetry garden — weeping cherry & classical landscapes' },
        { lat: 35.6613, lng: 139.6690, label: 'New York Joe Exchange', num: 3, cat: 'attraction', desc: 'Vintage warehouse — curated secondhand ¥1,000-5,000' },
        { lat: 35.6615, lng: 139.6675, label: 'Bear Pond Espresso', num: 4, cat: 'food', desc: 'Legendary single-shot espresso — no photos, no WiFi' },
        { lat: 35.7720, lng: 140.3929, label: 'Narita Airport (NRT)', num: 5, cat: 'transport', desc: 'International departure — Kit Kat shop inside' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (5 nights)', budget: '¥7,000-10,000/night ($48-70)', midrange: '¥15,000-25,000/night ($100-170)', luxury: '¥40,000-80,000/night ($275-550)' },
    { category: 'Meals (per day, couple)', budget: '¥3,000-5,000 ($20-35)', midrange: '¥8,000-15,000 ($55-100)', luxury: '¥20,000-40,000 ($135-275)' },
    { category: 'Transport (per day)', budget: '¥1,000-1,500 ($7-10)', midrange: '¥1,500-2,500 ($10-17)', luxury: '¥5,000+ (taxis)' },
    { category: 'Attractions (total)', budget: '¥5,000-8,000 ($35-55)', midrange: '¥10,000-15,000 ($70-100)', luxury: '¥20,000+ ($135+)' },
    { category: 'Shopping (Shimokitazawa vintage)', budget: '¥3,000-8,000 ($20-55)', midrange: '¥10,000-20,000 ($70-135)', luxury: '¥30,000+ ($200+)' },
    { category: '6-Day Total (couple)', budget: '¥80,000-120,000 ($550-825)', midrange: '¥180,000-300,000 ($1,200-2,000)', luxury: '¥400,000+ ($2,750+)' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita (NRT): 60-90 min from central Tokyo · Narita Express or Skyliner', 'Haneda (HND): 30-50 min · Keikyu Line or Tokyo Monorail', 'Haneda is closer and increasingly serves international routes — check first', 'No visa required for US, EU, UK, Australia, Canada citizens (90 days)'] },
    { title: '🌡️ Weather (Late Apr–Early May)', items: ['Temperature: 15-22°C (60-72°F) — perfect walking weather', 'Occasional rain — pack a light rain jacket or buy a ¥500 clear umbrella at any konbini', 'Late cherry blossoms possible on late-blooming varieties', 'Fresh spring green everywhere — Tokyo is lush in late April'] },
    { title: '🥬 Vegetarian Essentials', items: ['HappyCow app: essential for finding veggie restaurants in Tokyo', 'Key phrase: "Watashi wa bejitarian desu" (I am vegetarian)', 'Watch for hidden dashi (bonito stock) — ask "Katsuo dashi nashi de" (without bonito dashi)', 'Shōjin ryōri restaurants are always 100% plant-based — safest bet', 'Konbini: onigiri (ume, kombu), edamame, salads are reliably vegetarian'] },
    { title: '💰 Money & Budget', items: ['Japan is increasingly cashless but carry ¥10,000-20,000 for small shops and temples', 'Suica/Pasmo IC card: tap-and-go for trains, buses, vending machines, konbini', 'Tax-free shopping: spend ¥5,000+ at participating stores, show passport', 'Tipping is not practiced and can cause confusion — don\'t tip'] },
    { title: '📱 Connectivity', items: ['eSIM recommended (Ubigi, Airalo) — activate before departure', 'Pocket WiFi rental: available at airport · ¥500-1,000/day', 'Free WiFi at stations, konbini, and cafés (spotty quality)', 'Google Maps transit directions are flawless in Tokyo — use them constantly'] },
    { title: '🇦🇺 Onward to Australia', items: ['Check ETA/eVisitor visa for Australia before leaving home', 'Australia biosecurity is strict: declare ALL food, wooden items, plant material on arrival card', 'Processed/sealed Japanese snacks are generally fine — fresh food will be confiscated', 'Japan Post at Narita can ship excess luggage/purchases home or forward to Australia'] }
  ]
};

fulfillOrder(order, itineraryData);
