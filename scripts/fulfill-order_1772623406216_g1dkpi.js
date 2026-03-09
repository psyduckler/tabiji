const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772623406216_g1dkpi',
  email: 'galaxycats510@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-14',
  endDate: '2026-03-19',
  groupSize: '3-4',
  requests: "Im going with my best friend, fun things pls! don't mind day trips as well. Want to just enjoy and shop a bit and take good pictures"
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo with Your Best Friend',
  subtitle: '6 days of iconic photo spots, street food, shopping & neon-lit nights',
  description: "Tokyo is the world's most electrifying city — and it hits different with your best friend by your side. This itinerary is built for fun: Instagrammable food and fashion in Harajuku, mind-bending digital art at teamLab, karaoke until midnight in Shinjuku, izakaya-hopping through Golden Gai, and a scenic day trip to ancient Kamakura. Mid-March brings the first shy cherry blossoms — a bonus if timing aligns. You'll come back with a thousand photos and twice as many memories.",
  duration: '5 nights',
  dates: 'Mar 14 – Mar 19, 2026',
  budget: '$$–$$$',
  pace: 'Energetic',
  bestFor: 'Best friends, shopping lovers, foodies, night owls',
  highlights: [
    'Shibuya Crossing & Shibuya Sky observation deck',
    'Takeshita Street shopping spree in Harajuku',
    'teamLab Planets — immersive digital art',
    'Golden Gai bar-hopping & karaoke in Shinjuku',
    'Kamakura day trip — Giant Buddha & ocean views',
    'Senso-ji Temple at dawn in Asakusa',
    'Shimokitazawa vintage shopping & live music'
  ],

  essentials: [
    { title: '🌸 Cherry Blossoms', text: 'Mid-March is just before peak bloom in Tokyo (usually late March). You may catch the very first blossoms — especially in warm years. Check real-time forecasts on Japan Meteorological Corporation. Ueno Park and Yoyogi Park are top spots.' },
    { title: '🚇 IC Card = Everything', text: 'Get a Suica or Pasmo card at the airport and tap it on every train, bus, and even many convenience stores and vending machines. Recharge at any station. JR Pass is NOT needed for Tokyo city travel.' },
    { title: '📱 Pocket WiFi or eSIM', text: 'Pick up a pocket WiFi at the airport or activate an eSIM before landing. Google Maps works perfectly for Tokyo navigation. Download Hyperdia or Google Maps offline for subway routing.' },
    { title: '🏨 Where to Stay', text: 'Shinjuku is the best home base — central, lively, and steps from Golden Gai. Shibuya is great for nightlife. Asakusa is more traditional. Budget: ¥8,000–15,000/night per room. Mid-range: ¥15,000–35,000.' },
    { title: '💴 Cash & Cards', text: "Japan is still largely cash-based. Withdraw yen from 7-Eleven ATMs (most reliable for foreign cards). Budget ¥5,000–10,000/person/day for food, transport, and incidentals. Credit cards work at bigger shops and restaurants." },
    { title: '🍜 Eating Like Locals', text: "Convenience stores (7-Eleven, Lawson, FamilyMart) sell genuinely excellent food — perfect for breakfast. For meals, look for spots with plastic food displays or picture menus. Many high-end ramen shops have vending machine ordering — pay first, hand the ticket to the chef." }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-14',
      neighborhoods: 'Shinjuku · Kabukicho · Golden Gai',
      title: 'Welcome to Tokyo — Neon City, First Night',
      description: "Land in Tokyo and let the city hit you. Check in, grab a convenience store snack, and head straight to Shinjuku for your first taste of Tokyo's electric nightlife. Omoide Yokocho (Memory Lane) sets the mood with smoky yakitori and lantern light — then Golden Gai seals it.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Shinjuku Orientation',
              description: "Get your IC card at the airport and hop the Narita Express or Skyliner into the city. Check into your hotel, stash your bags, and take a first lap around Shinjuku — the most dense, dazzling square kilometre on earth.",
              details: [
                '✈️ Narita → Shinjuku via N\'EX: ~1hr 20min (¥3,070 with IC card)',
                '🛍️ Takashimaya Times Square right next to Shinjuku Station for any essentials',
                '📍 East Exit leads to Kabukicho and the neon action'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Snack',
              name: '7-Eleven or Lawson Convenience Store',
              description: 'Japanese convenience store food is genuinely great — onigiri, egg salad sandwiches, hot noodles, and strawberry daifuku. Stock up on snacks for the trip.',
              meta: '💰 ¥ · 📍 Everywhere in Japan'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kabukicho & Godzilla Head',
              description: "Walk through Kabukicho — Tokyo's entertainment district — and look up for the giant Godzilla head roaring from the Shinjuku Kabukicho Tower Hotel. Snap the obligatory photo, then soak in the neon chaos.",
              details: [
                '🦖 Godzilla Head: Shinjuku Kabukicho Tower, 1-29-1 Kabukicho',
                '📸 Best angle: from the street below looking up at night',
                '🎮 Toho Cinemas building — where the kaiju lives'
              ]
            },
            {
              title: 'Golden Gai Bar Hop',
              description: "Six narrow alleyways, 200+ tiny bars — Golden Gai is Tokyo's most unique nightlife experience. Each bar fits 5–10 people max, has its own vibe (jazz, anime, horror, vintage film), and you're forced to talk to strangers. Pick three bars and do a proper crawl.",
              details: [
                '🍺 Most bars have a cover charge of ¥500–1,000 — totally worth it',
                '🎵 Look for themes that match your vibe — there\'s something for everyone',
                '🌙 Gets busy from 9pm — perfect for a first night out',
                '📍 Golden Gai is directly behind Kabukicho, near Hanazono Shrine'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Dinner',
              name: 'Omoide Yokocho (Memory Lane)',
              description: "The narrow alley of smoky yakitori stalls under the train tracks — one of Tokyo's most atmospheric dining spots. Pull up a stool, order chicken skewers and cold Sapporo, and let the smoke and chatter wash over you.",
              meta: '💰 ¥¥ · 📍 1-2 Nishishinjuku, next to Shinjuku Station West Exit · Opens from 5pm'
            }
          ],
          tips: [
            { type: 'tip', text: "Don't skip Golden Gai on night one — it's the perfect Tokyo initiation. Dress down. Make friends. Some bars have English menus, many don't — just point and smile." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Main hub — East Exit for Kabukicho, West Exit for Memory Lane' },
        { lat: 35.6912, lng: 139.6997, label: 'Omoide Yokocho (Memory Lane)', num: 2, cat: 'food', desc: 'Iconic smoky yakitori alley under the train tracks' },
        { lat: 35.6946, lng: 139.7031, label: 'Kabukicho & Godzilla Head', num: 3, cat: 'attraction', desc: 'Entertainment district with giant Godzilla on the rooftop' },
        { lat: 35.6937, lng: 139.7017, label: 'Golden Gai', num: 4, cat: 'attraction', desc: '200+ tiny themed bars in six narrow alleyways' },
        { lat: 35.6944, lng: 139.7024, label: 'Hanazono Shrine', num: 5, cat: 'attraction', desc: 'Atmospheric shrine next to Golden Gai — beautiful at night' }
      ]
    },
    {
      num: 2,
      date: '2026-03-15',
      neighborhoods: 'Harajuku · Omotesando · Shibuya',
      title: 'Harajuku Shop-Til-You-Drop & Shibuya Sky',
      description: "Day two is the ultimate Tokyo photo and shopping day. Takeshita Street in Harajuku for wild fashion and crepes, Omotesando for high-end browsing and the best people-watching in Tokyo, then Shibuya Crossing at rush hour and the famous Shibuya Sky rooftop for city views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Takeshita Street — Harajuku\'s Wild Side',
              description: "The legendary pedestrian street of Harajuku is packed with avant-garde fashion, rainbow cotton candy, crepe shops, and costume stores. It's chaotic, colourful, and completely photogenic. Go in the morning before the weekend crowds go insane.",
              details: [
                '🍦 Marion Crepes — the OG Harajuku crepe spot since 1976',
                '🛍️ Bubbles, spinns, and local indie brands for unique pieces',
                '📸 Street fashion is the real attraction — portraits everywhere',
                '⏰ Go before 11am if you want elbow room'
              ]
            }
          ],
          meals: [
            {
              type: '🥞 Breakfast',
              name: 'Marion Crepes, Takeshita Street',
              description: 'Freshly made crepes stuffed with strawberries, whipped cream, and custard — the quintessential Harajuku experience. Queue moves fast.',
              meta: '💰 ¥ · 📍 1-6-15 Jingumae, Shibuya · Open from 10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Omotesando & Cat Street',
              description: "Walk from Harajuku down Omotesando — Tokyo's most beautiful boulevard, lined with zelkova trees and flagship stores from every major brand. Then duck into the backstreets of Cat Street (Ura-Harajuku) for indie boutiques, vintage shops, and hidden cafés.",
              details: [
                '🏛️ Omotesando Hills — stunning spiral shopping complex by Tadao Ando',
                '🐱 Cat Street: Jingumae, Shibuya — small brands and unique finds',
                '☕ Streamer Coffee Company on Cat Street is exceptional',
                '📸 The zelkova tree boulevard is gorgeous — especially if blossoms are out'
              ]
            },
            {
              title: 'Shibuya Crossing & Scramble Square',
              description: "Make your way to Shibuya and stand in the middle of the world's busiest crossing — up to 3,000 people crossing at once. Then head up to Shibuya Sky (109m rooftop) for a 360-degree view of Tokyo — the best city view anywhere, and incredible for photos.",
              details: [
                '🚦 Best time to photograph the crossing: from Starbucks or L\'Occitane 2F window',
                '🏙️ Shibuya Sky: book tickets online in advance (¥2,000pp)',
                '📸 The rooftop is fully open-air — breathtaking at golden hour',
                '⏰ Book Shibuya Sky for around 4-5pm for sunset views'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Ichiran Ramen, Shibuya',
              description: 'The iconic solo-booth ramen shop where you customize your broth intensity, richness, and spice level on a paper form. Each stall is partitioned — hyper-focused ramen eating. The tonkotsu is transcendent.',
              meta: '💰 ¥¥ · 📍 1-22-7 Jinnan, Shibuya · No reservations needed'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nonbei Yokocho (Shibuya\'s Hidden Bar Alley)',
              description: "Just a few blocks from Shibuya Crossing, Nonbei Yokocho ('Drunkard's Alley') is a cluster of tiny bars and izakayas under low wooden eaves — feels like a tiny Kyoto village tucked inside the megacity. Grab a table at one of the izakayas and order unlimited edamame, karaage, and highballs.",
              details: [
                '🏮 Charming alleyway just north of Shibuya Station',
                '🥃 Highball (whisky + soda) is the classic order: ¥600-900',
                '🍗 Karaage (Japanese fried chicken) is the essential bar snack'
              ]
            }
          ],
          meals: [
            {
              type: '🍻 Dinner',
              name: 'Izakaya at Nonbei Yokocho',
              description: 'Pick any izakaya with an open door and an English menu. Order a selection of small plates — yakitori, edamame, gyoza, octopus skewers — and a round of frozen draft beers.',
              meta: '💰 ¥¥ · 📍 1-25 Shibuya, Shibuya · From 6pm'
            }
          ],
          tips: [
            { type: 'tip', text: "Book Shibuya Sky tickets online in advance — they sell out, especially weekends. The golden hour and blue hour (after sunset) shots are magical." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6702, lng: 139.7027, label: 'Takeshita Street, Harajuku', num: 1, cat: 'attraction', desc: 'Wild fashion street with crepes, costumes, and candy' },
        { lat: 35.6680, lng: 139.7060, label: 'Cat Street (Ura-Harajuku)', num: 2, cat: 'attraction', desc: 'Indie boutiques and vintage shops in backstreet Harajuku' },
        { lat: 35.6653, lng: 139.7125, label: 'Omotesando Boulevard', num: 3, cat: 'attraction', desc: 'Tree-lined luxury shopping avenue with Tadao Ando buildings' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Scramble Crossing', num: 4, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing — iconic Tokyo photo' },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Sky', num: 5, cat: 'attraction', desc: 'Open-air rooftop observation deck — best 360° Tokyo view' },
        { lat: 35.6575, lng: 139.7049, label: 'Ichiran Ramen Shibuya', num: 6, cat: 'food', desc: 'Solo-booth tonkotsu ramen perfection' },
        { lat: 35.6613, lng: 139.7061, label: 'Nonbei Yokocho', num: 7, cat: 'food', desc: 'Hidden izakaya alley — tiny bars under wooden eaves' }
      ]
    },
    {
      num: 3,
      date: '2026-03-16',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Ancient Temples, Neon Markets & Electric Town',
      description: "Go old-school Tokyo today. Dawn at Senso-ji when the incense hangs in the quiet air, yakitori and craft beer at Hoppy Street, then a deep dive into Akihabara's anime and retro gaming wonderland. End the night with an onsen soak at a public sento.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple at Sunrise',
              description: "Tokyo's oldest temple looks magical in the early morning — the crowds are thin, the incense smoke catches the light, and the five-storey pagoda glows. Walk through the giant Kaminarimon (Thunder Gate) and down Nakamise-dori shopping street for souvenir browsing.",
              details: [
                '⛩️ Temple grounds open 24/7 — best before 8am',
                '🌅 The Kaminarimon lantern and Nakamise-dori at dawn — stunning photos',
                '🪔 Shake an omikuji fortune slip — it\'s a Tokyo rite of passage',
                '🛍️ Nakamise-dori: yukata, ninja goods, sembei rice crackers, matcha everything'
              ]
            }
          ],
          meals: [
            {
              type: '🍡 Breakfast',
              name: 'Nakamise-dori Street Food',
              description: 'Grab freshly grilled ningyo-yaki (red bean cakes) from the stalls along Nakamise shopping street. Small, hot, and perfect with green tea.',
              meta: '💰 ¥ · 📍 Nakamise-dori, Asakusa'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park Cherry Blossom Stroll',
              description: "Walk through Ueno Park — in mid-March the blossoms are just starting on the earliest trees (usually late March for full bloom, but some years are early). Even if it's pre-bloom, the park and Shinobazu Pond are beautiful. The Tokyo National Museum here is world-class if you want culture.",
              details: [
                '🌸 Check real-time bloom forecast at sakura.weathermap.jp',
                '🦆 Shinobazu Pond has lotus flowers and temple on the water',
                '🏛️ Tokyo National Museum: Japan\'s finest art collection — free on special days'
              ]
            },
            {
              title: 'Akihabara Electric Town',
              description: "Tokyo's legendary electronics and anime district is an assault on the senses in the best way. Multi-storey arcades, floors of manga and figures, retro game shops (Super Potato), maid cafés, and gadget stores with things you've never seen before.",
              details: [
                '🎮 Super Potato: retro game paradise — Famicom, SNES, PCE, Dreamcast',
                '🏬 Yodobashi Camera: 8 floors of tech for the best prices',
                '🗼 Radio Kaikan building: figures, models, and anime merch',
                '☕ Try a maid café for the full Akihabara experience'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Lunch',
              name: 'Hoppy Street, Asakusa',
              description: 'Retro outdoor food street near Senso-ji where locals have sipped Hoppy (barley beer mixer) and eaten motsu (offal) stew since the 1940s. Cheap, delicious, and completely authentic.',
              meta: '💰 ¥ · 📍 2 Asakusa, Taito · From 11am'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Public Onsen (Sento) Soak',
              description: "After a big walking day, find a neighbourhood public bath (sento) near your hotel. No tattoo restrictions at most sentō — just bring a small towel and toiletries. An hour soaking in hot mineral water will reset your legs completely.",
              details: [
                '♨️ Thermae-yu in Shinjuku accepts foreigners and is tattoo-friendly',
                '🧴 Entry around ¥1,000–2,500 including towel rental',
                '⚠️ No phones or cameras inside the bathing area — phones in lockers'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Conveyor Belt Sushi (Kaitenzushi)',
              description: 'Hit a kaitenzushi spot like Genki Sushi or Sushiro for a fun, affordable dinner — plates arrive by conveyor belt or mini Shinkansen bullet train. Order off a tablet, grab what looks good, stack your plates. ¥100–200 per plate.',
              meta: '💰 ¥ · 📍 Genki Sushi Akihabara or Sushiro Ueno'
            }
          ],
          tips: [
            { type: 'tip', text: "Akihabara UFO catcher (crane game) arcades are seriously addictive. Budget 30 extra minutes and ¥1,000 in 100-yen coins — winning a giant plush is a peak Tokyo memory." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s most iconic temple — best at dawn' },
        { lat: 35.7133, lng: 139.7966, label: 'Nakamise-dori Shopping Street', num: 2, cat: 'attraction', desc: 'Souvenir and street food lane leading to Senso-ji' },
        { lat: 35.7133, lng: 139.7930, label: 'Hoppy Street', num: 3, cat: 'food', desc: 'Retro outdoor beer and motsu stew street in Asakusa' },
        { lat: 35.7163, lng: 139.7741, label: 'Ueno Park', num: 4, cat: 'attraction', desc: 'Large park with early cherry blossoms and Tokyo National Museum' },
        { lat: 35.7021, lng: 139.7741, label: 'Akihabara Electric Town', num: 5, cat: 'attraction', desc: 'Anime, electronics, retro games, and maid cafés' },
        { lat: 35.7012, lng: 139.7726, label: 'Super Potato Akihabara', num: 6, cat: 'attraction', desc: 'Multi-floor retro video game shop' },
        { lat: 35.6920, lng: 139.7034, label: 'Thermae-yu Onsen Shinjuku', num: 7, cat: 'attraction', desc: 'Public onsen/sento — tattoo-friendly, no cover charge' }
      ]
    },
    {
      num: 4,
      date: '2026-03-17',
      neighborhoods: 'Toyosu · Shimokitazawa · Shinjuku',
      title: 'teamLab, Vintage Hunting & Karaoke Night',
      description: "Today hits three completely different vibes: the digital art wonderland of teamLab Planets in the morning, vintage shopping and live music in the indie neighbourhood of Shimokitazawa in the afternoon, and a legendary karaoke night in Shinjuku to close it out.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Planets, Toyosu',
              description: "One of the most photographed art experiences on earth — walk through rooms of infinite mirrors, wade barefoot through water reflecting a thousand flowers, and disappear into pulsing LED universes. Book tickets well in advance. Wear shorts or clothes you don't mind getting slightly wet.",
              details: [
                '🎨 Book tickets at planets.teamlab.art — sell out weeks ahead',
                '👣 Goes barefoot — lockers provided for shoes and bags',
                '📸 The waterscape rooms and infinity rooms are otherworldly',
                '⏰ Allow 90 minutes to 2 hours minimum',
                '🌸 The flower universe installations include sakura motifs'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shimokitazawa — Tokyo\'s Coolest Neighbourhood',
              description: "Head to Shimokitazawa — a maze of narrow lanes packed with vintage clothing shops, indie record stores, live music venues, and tiny cafés. It's the antithesis of Shibuya — slow, creative, and deeply local. Budget 3 hours here minimum.",
              details: [
                '🛍️ Flamingo Shimokitazawa — curated vintage from ¥1,000',
                '🛍️ New York Joe Exchange — iconic thrift and swap shop',
                '🎵 Shimokitazawa has more live music venues per block than anywhere',
                '☕ Bear Pond Espresso — legendary tiny coffee shop (only 20 cups/day)',
                '📍 20 min from Shinjuku on the Odakyu Line'
              ]
            }
          ],
          meals: [
            {
              type: '🍛 Lunch',
              name: 'Shimokitazawa Curry or Ramen',
              description: 'Shimokitazawa is full of great independent curry spots — Japanese curry is thick, sweet, and deeply comforting. Look for the spots with handwritten signs and a queue.',
              meta: '💰 ¥¥ · 📍 Around Shimokitazawa Station, Setagaya'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Karaoke in Shinjuku',
              description: "Tokyo karaoke is an experience unlike anywhere else in the world — you get your own private room, unlimited song selection (English songs galore), microphones with echo effects, and unlimited drinks packages. Go to Big Echo or Karaoke-kan in Shinjuku and book 2–3 hours.",
              details: [
                '🎤 Big Echo Shinjuku: multiple English song options, fun party rooms',
                '🍹 Most karaoke venues offer all-you-can-drink packages (nomihodai)',
                '⏰ Book a 2–3 hour session starting around 9pm',
                '💰 Expect ¥2,000–4,000pp with drinks package',
                '🎵 The songbook has every English pop/hip-hop/K-pop song you know'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Izakaya in Shinjuku before karaoke',
              description: 'Fuel up at a Shinjuku izakaya before karaoke. Torikizoku is a brilliant budget chain — every item is ¥360, the yakitori is excellent, and it\'s always packed and loud.',
              meta: '💰 ¥ · 📍 Torikizoku multiple locations around Shinjuku'
            }
          ],
          tips: [
            { type: 'tip', text: "teamLab tickets sell out weeks in advance. If you can't get Planets, teamLab Borderless in Azabudai Hills is also spectacular. Book whichever you can get." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6472, lng: 139.7949, label: 'teamLab Planets, Toyosu', num: 1, cat: 'attraction', desc: 'Immersive digital art — barefoot through water and light' },
        { lat: 35.6617, lng: 139.6680, label: 'Shimokitazawa', num: 2, cat: 'attraction', desc: 'Indie neighbourhood: vintage shops, cafes, live music' },
        { lat: 35.6625, lng: 139.6693, label: 'Flamingo Vintage Shimokitazawa', num: 3, cat: 'attraction', desc: 'Curated vintage fashion from ¥1,000' },
        { lat: 35.6621, lng: 139.6686, label: 'New York Joe Exchange', num: 4, cat: 'attraction', desc: 'Iconic thrift and clothing swap shop' },
        { lat: 35.6937, lng: 139.7017, label: 'Shinjuku Karaoke District', num: 5, cat: 'attraction', desc: 'Big Echo, Karaoke-kan — private room karaoke central' },
        { lat: 35.6896, lng: 139.7006, label: 'Torikizoku Shinjuku', num: 6, cat: 'food', desc: 'Budget izakaya — every item ¥360, great yakitori' }
      ]
    },
    {
      num: 5,
      date: '2026-03-18',
      neighborhoods: 'Kamakura · Hase · Yuigahama',
      title: 'Kamakura Day Trip — Giant Buddha & Ocean Views',
      description: "Escape Tokyo for the day and head south to Kamakura — a coastal city of ancient temples, the iconic Giant Buddha, bamboo groves, and one of the most photogenic train rides in Japan. The ocean view from Inamuragasaki Point is jaw-dropping, and Komachi-dori is a perfect shopping street for souvenirs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Kamakura — Scenic Ride',
              description: "Take the JR Yokosuka Line from Shinjuku or Tokyo Station to Kamakura (about 1 hour). Once in Kamakura, switch to the Enoden tram line — one of the most charming train journeys in Japan, running along the coastline and through residential streets.",
              details: [
                '🚆 Shinjuku → Kamakura: ~1h via JR (IC card, about ¥940)',
                '🚋 Enoden tram: Kamakura → Hase → Enoshima along the coast',
                '🌊 Ride the Enoden on the left side for ocean views',
                '⏰ Leave by 8am to beat the crowds at the Buddha'
              ]
            },
            {
              title: 'Kotoku-in Great Buddha (Kamakura Daibutsu)',
              description: "Stand before the 13.35-metre bronze Buddha that's been sitting in open air since 1252. You can go inside the hollow bronze statue for ¥20 extra. In the morning light with mountains behind, it's one of Japan's most powerful images.",
              details: [
                '⛩️ Kotoku-in Temple, Hase — admission ¥300',
                '📸 Best photo: from the main approach facing north',
                '🏛️ You can enter the statue: ¥20 extra, see the internal structure',
                '⏰ Opens at 8am — arrive early for low crowds'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Convenience store on train',
              description: 'Pick up onigiri and canned coffee at Shinjuku Station before boarding — eating on the train is perfectly acceptable in Japan.',
              meta: '💰 ¥ · 📍 Any JR station convenience store'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hase-dera Temple & Hydrangea Garden',
              description: "A short walk from the Buddha, Hase-dera is one of Kamakura's most beautiful temples — featuring a massive gilded wooden Kannon statue, an ocean overlook, and a terrace carved from the hillside. In March you might catch some early spring flowers.",
              details: [
                '⛩️ Admission ¥400 · 3-11-2 Hase, Kamakura',
                '🌺 The ocean view terrace is spectacular — best photo in Kamakura',
                '🙏 The cave with small Jizo statues for unborn children is deeply moving'
              ]
            },
            {
              title: 'Komachi-dori Shopping Street & Yuigahama Beach',
              description: "Walk the main shopping street of Kamakura for local crafts, matcha everything (ice cream, soft serve, Kit-Kats), and quality pottery. Then stroll down to Yuigahama Beach — in mid-March the water is cold but the ocean views and surfers are a great photo backdrop.",
              details: [
                '🛍️ Komachi-dori: pickles, ceramics, wagashi sweets, matcha soft serve',
                '🏄 Yuigahama Beach is a beautiful Pacific coast beach',
                '📸 The beach with mountains in the background = incredible shot'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Kamakura Shirasu Bowl',
              description: 'Kamakura is famous for shirasu (whitebait) — tiny fish eaten fresh or semi-dried. Order a shirasu rice bowl (shirasu-don) at one of the beachside restaurants near Yuigahama. Wildly fresh and delicious.',
              meta: '💰 ¥¥ · 📍 Beachside restaurants near Yuigahama Beach'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tsurugaoka Hachimangu Shrine at Dusk',
              description: "Walk up the main approach (Wakamiya-oji) to Kamakura's most important shrine as the light turns golden. The approach lined with cherry trees is usually in bloom in late March — in mid-March you may catch some early blossoms.",
              details: [
                '⛩️ Free entry · 2-1-31 Yukinoshita, Kamakura',
                '🌸 The approach cherry trees are some of Japan\'s most photogenic',
                '📸 Shoot from the stairs looking back down for the best composition'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Early dinner / drinks',
              name: 'Back in Shinjuku — Soba and Sake',
              description: 'Head back to Tokyo around 6-7pm and grab simple soba noodles and Japanese sake at a standing bar near Shinjuku Station. Kamonan or any standing soba bar is perfect after a long day walking.',
              meta: '💰 ¥¥ · 📍 Shinjuku Station area'
            }
          ],
          tips: [
            { type: 'tip', text: "The Enoden tram is the real charm of Kamakura — buy a day pass (¥700) and ride it all day between stops. The stretch between Kamakura and Hase where it runs along the coast is a classic Japan photo." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3167, lng: 139.5356, label: 'Kotoku-in Great Buddha', num: 1, cat: 'attraction', desc: '13m bronze Buddha dating from 1252 — one of Japan\'s icons' },
        { lat: 35.3156, lng: 139.5337, label: 'Hase-dera Temple', num: 2, cat: 'attraction', desc: 'Beautiful hillside temple with ocean panorama' },
        { lat: 35.3192, lng: 139.5467, label: 'Kamakura Station', num: 3, cat: 'transport', desc: 'Main train hub — JR and Enoden tram interchange' },
        { lat: 35.3232, lng: 139.5561, label: 'Komachi-dori Shopping Street', num: 4, cat: 'attraction', desc: 'Main souvenir street — matcha ice cream, crafts, pottery' },
        { lat: 35.3026, lng: 139.5509, label: 'Yuigahama Beach', num: 5, cat: 'attraction', desc: 'Pacific coast beach with mountain backdrop — great photos' },
        { lat: 35.3258, lng: 139.5562, label: 'Tsurugaoka Hachimangu Shrine', num: 6, cat: 'attraction', desc: 'Kamakura\'s most important shrine with cherry-lined approach' }
      ]
    },
    {
      num: 6,
      date: '2026-03-19',
      neighborhoods: 'Harajuku · Yoyogi Park · Omotesando',
      title: 'Meiji Shrine, Park Picnic & Final Wanders',
      description: "Your last morning in Tokyo. Start with the serene Meiji Shrine forest, then lay out in Yoyogi Park for a slow morning — watch the city wake up, maybe catch some street performers. Last-minute shopping on Omotesando before heading to the airport with a heart full of Tokyo magic.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine — Sacred Forest Walk',
              description: "Walk through 70 hectares of old-growth forest to reach the grand shrine dedicated to Emperor Meiji. The towering wooden torii gate, the forested approach, and the inner garden are all stunning — a completely different energy from Tokyo's neon chaos.",
              details: [
                '⛩️ Free entry · 1-1 Yoyogikamizonocho, Shibuya',
                '📸 The torii gate is one of Japan\'s most photographed structures',
                '🌿 The walk through the forest is deeply calming — allow 1 hour',
                '⏰ Opens at sunrise — gorgeous in early morning mist'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yoyogi Park — People Watching & Picnic',
              description: "The park attached to Meiji Shrine is Tokyo's biggest and best. On weekends it fills with outdoor musicians, rockabilly dancers, cosplayers, dog walkers, and friend groups having picnics. In mid-March the earliest plum blossoms may be out. Buy snacks from 7-Eleven and find a patch of grass.",
              details: [
                '🌸 Check if any early sakura or plum trees are in bloom',
                '🎸 On Sundays, rockabilly groups dance near the south entrance — iconic',
                '🛒 Pick up picnic supplies from the FamilyMart near the park entrance',
                '📍 Most lively on weekends — Sundays especially'
              ]
            },
            {
              title: 'Final Omotesando Wander & Last Souvenirs',
              description: "One final walk down Omotesando to pick up any last gifts — Kiddyland for toys and anime merch, Japan Gallery for quality crafts, and the underground market of Omotesando Hills for gourmet Japanese food gifts.",
              details: [
                '🧸 Kiddyland: 6 floors of toys, anime, and Sanrio everything',
                '🍫 Look for regional Kit-Kat flavors (sakura, matcha, rum raisin)',
                '🛍️ Omotesando Hills basement: premium Japanese pantry items as gifts'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Last Lunch',
              name: 'Omotesando Hills or Eggs\'n Things',
              description: 'For a proper last meal, head to the restaurants inside Omotesando Hills for Japanese dining with style. Or Eggs\'n Things on Omotesando does massive pancakes with whipped cream — a fun last Tokyo breakfast-lunch.',
              meta: '💰 ¥¥ · 📍 Omotesando Hills, 4-12-10 Jingumae, Shibuya'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Airport Transfer — Narita or Haneda',
              description: "Head to the airport with plenty of time. Narita: take the N'EX (Narita Express) from Shinjuku — about 1h 20min. Haneda: take the Keikyu or Tokyo Monorail — about 30-40min from the city.",
              details: [
                '✈️ Allow 3 hours before departure for international check-in',
                '🛍️ Last chance duty-free shopping at the airport — great for whisky, sake, and cosmetics',
                '🤳 Use the airport lounge if you have Priority Pass or a qualifying card'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Before leaving Japan, stop at a 7-Eleven and grab one last convenience store snack — a strawberry milk or melon pan. You'll be craving it on the plane home." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6763, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Grand Shinto shrine in a 70-hectare old-growth forest' },
        { lat: 35.6718, lng: 139.6947, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Tokyo\'s biggest park — picnics, performers, early blossoms' },
        { lat: 35.6657, lng: 139.7121, label: 'Omotesando Hills', num: 3, cat: 'attraction', desc: 'Spiral shopping complex by Tadao Ando — cafes and boutiques' },
        { lat: 35.6692, lng: 139.7076, label: 'Kiddyland Omotesando', num: 4, cat: 'attraction', desc: '6-floor toy and anime merch store' },
        { lat: 35.6895, lng: 139.6997, label: 'Shinjuku Station (Airport Departure)', num: 5, cat: 'transport', desc: 'Board N\'EX to Narita Airport from here' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per room)', budget: '¥8,000–15,000/night', midrange: '¥15,000–35,000/night', luxury: '¥35,000–80,000/night' },
    { category: 'Meals (per person/day)', budget: '¥2,000–3,500', midrange: '¥3,500–7,000', luxury: '¥7,000–20,000' },
    { category: 'Transport (IC card, per day)', budget: '¥500–1,000', midrange: '¥1,000–2,000', luxury: '¥2,000+ (taxis)' },
    { category: 'Activities', budget: '¥1,000–3,000/day', midrange: '¥3,000–8,000/day', luxury: '¥8,000+/day' },
    { category: 'teamLab Planets ticket', budget: '¥3,200pp', midrange: '¥3,200pp', luxury: '¥3,200pp' },
    { category: 'Kamakura day trip', budget: '¥3,000–5,000pp', midrange: '¥5,000–8,000pp', luxury: '¥8,000+pp' },
    { category: '6-Day Total (per person)', budget: '¥60,000–90,000', midrange: '¥90,000–150,000', luxury: '¥150,000+' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT) — 60km from central Tokyo, ~1hr 20min by N\'EX train', 'Haneda Airport (HND) — 20km from center, much closer and more convenient', 'N\'EX (Narita Express): ¥3,070 to Shinjuku with IC card', 'Limousine Bus: slower but cheaper — about ¥3,200 to major hotels'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku: best base for nightlife access (Golden Gai steps away)', 'Shibuya: trendy, close to shopping and bar scene', 'Asakusa: traditional feel, close to Senso-ji and Kamakura trains', 'Budget picks: Grids hostels, Book And Bed (sleep in a bookshelf!)', 'Mid-range: Keio Presso Inn, Dormy Inn, Richmond Hotel'] },
    { title: '🌸 Cherry Blossoms', items: ['Mid-March is just before peak bloom in Tokyo (peak usually late March)', 'Check real-time forecasts at sakura.weathermap.jp', 'Best spots: Ueno Park, Yoyogi Park, Shinjuku Gyoen, Meguro River', 'Some early-blooming varieties may be open — a surprise bonus!'] },
    { title: '📱 Apps to Download', items: ['Google Maps — best for Tokyo navigation', 'Hyperdia or Jorudan — train route planning', 'Google Translate — camera mode reads Japanese menus instantly', 'Tabelog — find the best local restaurants with ratings'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
