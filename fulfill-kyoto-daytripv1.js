const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1772626588256_1210pp',
  email: 'galaxycats510@gmail.com',
  destination: 'Kyoto, Japan',
  startDate: '2026-03-13',
  endDate: '2026-03-13',
  groupSize: '3-4',
  travelStyle: ['Cultural', 'Relaxation'],
  dining: 'Casual throughout',
  budget: 'Surprise me',
  requests: 'Day trip to Kyoto from Osaka. Arashiyama (NO bamboo grove). Include Uji if time permits.'
};

const itineraryData = {
  destination: "Kyoto, Japan",
  countryEmoji: "🇯🇵",
  title: "Kyoto in a Day: Arashiyama & Uji",
  subtitle: "A perfect day trip from Osaka — zen gardens, riverside temples, mountain monkeys, and the world's best matcha",
  description: "One day, two of Kyoto's most beautiful corners. Start in Arashiyama — stroll Togetsukyo Bridge, wander the Tenryū-ji zen garden, walk the quiet Saga-Toriimoto preserved street, and hike up to meet the monkeys with their panoramic Kyoto views. Then catch the afternoon train to Uji, a small riverside town that's home to the stunning Byōdō-in Temple and Japan's finest matcha. Back in Osaka before dinner. No crowds, no rush — just the best of Kyoto.",
  duration: "1 day",
  dates: "March 13, 2026",
  budget: "¥5,000–8,000 per person (excluding transport)",
  pace: "Relaxed — plenty of time at each stop",
  bestFor: "Groups of 3-4 · Cultural travelers · First-time Kyoto visitors",
  highlights: [
    "Tenryū-ji Zen Garden — UNESCO World Heritage zen landscape",
    "Togetsukyo 'Moon Crossing' Bridge at dawn",
    "Saga-Toriimoto — Kyoto's best-preserved Meiji-era townscape",
    "Iwatayama Monkey Park — 170 Japanese macaques + panoramic Kyoto views",
    "Byōdō-in Phoenix Hall — the temple on Japan's 10-yen coin",
    "Matcha everything in Uji — birthplace of Japanese green tea culture"
  ],

  essentials: [
    { title: "🚆 Getting from Osaka", text: "Take Hankyu from Osaka Umeda → Katsura → change to Hankyu Arashiyama Line → Arashiyama Station (~45-50 min, ~¥410 each way). Or JR Osaka → Kyoto → JR San-in Line to Saga-Arashiyama (~55 min, ~¥990). Hankyu is cheaper and drops you closest to Togetsukyo." },
    { title: "🎫 Buy Tickets In Advance", text: "Tenryū-ji garden entry is ¥500 (garden only) or ¥1,000 (temple buildings). Monkey Park entry is ¥600/person. Byōdō-in is ¥700/person. All walk-in but budget for all three." },
    { title: "⏰ Timing Matters", text: "Arrive at Arashiyama by 9am before tour groups flood in. Tenryū-ji opens at 8:30am. Monkey Park hike takes 20-30 min each way — wear comfortable shoes." },
    { title: "🍵 Matcha in Uji", text: "Uji is the matcha capital of Japan. The street leading to Byōdō-in (Byōdō-in Omotesandō) is lined with tea shops. Budget ¥500-1,500 for matcha sweets and a bowl of tea." },
    { title: "🦌 Skip the Bamboo Grove (By Choice!)", text: "The famous Arashiyama Bamboo Grove is extremely crowded and honestly overrated. You're not missing much — and Saga-Toriimoto, Tenryū-ji, and the Monkey Park give you a far better, more peaceful Arashiyama experience." },
    { title: "💴 Cash Is King", text: "Many smaller temples, tea shops, and food stalls in Arashiyama and Uji are cash-only. Bring ¥10,000-15,000 per person." }
  ],

  days: [
    {
      num: 1,
      date: "2026-03-13",
      neighborhoods: "Arashiyama · Saga-Toriimoto · Uji",
      title: "Arashiyama Zen & Uji Matcha — A Perfect Day",
      description: "Early start from Osaka, a serene morning in Arashiyama, monkeys with a view, then the short train hop to Uji for temples and the best matcha of your life.",
      timeBlocks: [
        {
          label: "Morning (7:30–8:00am)",
          activities: [
            {
              title: "Depart Osaka",
              description: "Catch an early train from Osaka Umeda (Hankyu) toward Arashiyama. The early morning crowds are manageable and the light on the Oi River is beautiful.",
              details: [
                "🚆 Hankyu Osaka Umeda → Katsura (change) → Arashiyama: ~45 min, ¥410",
                "💡 Aim to arrive in Arashiyama by 9am before the tour buses arrive",
                "📍 If coming from southern Osaka, JR Osaka → Kyoto → Saga-Arashiyama works too"
              ]
            }
          ]
        },
        {
          label: "Morning (9:00–9:30am)",
          activities: [
            {
              title: "Togetsukyo Bridge — The Icon",
              description: "This graceful wooden bridge over the Oi River is the symbol of Arashiyama. Walk across at your own pace, take in the forested hillside that frames it, and breathe in the quiet before the day picks up. In mid-March the first cherry blossoms sometimes appear on the banks.",
              details: [
                "📍 5 min walk from Hankyu Arashiyama Station",
                "🌸 Mid-March: early plum blossoms are likely; cherry may just be budding",
                "📸 Best photo angle: from the riverbank looking west toward Arashiyama mountain"
              ]
            }
          ],
          meals: [
            {
              type: "Breakfast",
              name: "Walden Woods Kyoto (or riverside konbini)",
              description: "Cozy café near the bridge serving Japanese-style breakfast sets. Alternatively, grab an onigiri and canned coffee from 7-Eleven before the train — Arashiyama's café options get crowded fast.",
              meta: "¥600-1,200/person · Opens at 8am"
            }
          ]
        },
        {
          label: "Mid-Morning (9:30–11:00am)",
          activities: [
            {
              title: "Tenryū-ji Garden — Zen Masterpiece",
              description: "One of Japan's greatest zen gardens, with a raked gravel garden and perfectly composed pond landscape framed by borrowed scenery of Arashiyama's forested hills. The garden was designed in 1339 by renowned monk Musō Soseki and hasn't changed much since. Walk slowly. Sit on a bench. Let it sink in.",
              details: [
                "🎫 ¥500 garden only / ¥1,000 for temple buildings too — garden is plenty",
                "⏰ Opens 8:30am — go early for peaceful photos",
                "🌿 The moss garden after rain is especially beautiful",
                "📍 2 min from Togetsukyo Bridge via Tenryūji Mae bus stop"
              ]
            },
            {
              title: "Saga-Toriimoto — Kyoto's Best-Kept Street",
              description: "A 15-minute walk (or short rickshaw) north of Tenryū-ji brings you to Saga-Toriimoto, a remarkably preserved Meiji-era townscape. Thatched-roof farmhouses turned into tofu restaurants and tea houses line both sides of the road. Almost no tourists. Feels like stepping back 150 years.",
              details: [
                "📍 ~15 min walk north from Tenryū-ji main gate",
                "🍵 Hiranoya — traditional tofu kaiseki in a 400-year-old building (book ahead for lunch)",
                "💡 Pass under the orange torii gates of Nonomiya Shrine on the way — worth a 10-min peek",
                "📸 Street is most photogenic in the morning light"
              ]
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "Saga-Toriimoto was my favorite part of Arashiyama. Zero crowds, gorgeous old houses, and you can just walk and absorb the atmosphere. Everyone is at the bamboo grove which is 5 minutes away. Go the other direction.",
              cite: "r/JapanTravel"
            }
          ]
        },
        {
          label: "Late Morning (11:00am–12:30pm)",
          activities: [
            {
              title: "Iwatayama Monkey Park — Worth the Hike",
              description: "From near Togetsukyo Bridge, a 20-30 minute uphill trail takes you to Iwatayama Monkey Park, home to around 170 wild Japanese macaques who roam completely free. At the top, you can feed them through a wire fence and take in sweeping views over Arashiyama and the Kyoto basin. Genuinely one of Kyoto's best hidden gems.",
              details: [
                "🎫 ¥600 adults",
                "⏰ Opens 9am — trails close 4:30pm",
                "👟 20-30 min uphill hike — wear comfortable shoes",
                "🐒 Don't make direct eye contact with the monkeys or show food in the open air",
                "📸 View from the top is stunning — the Oi River, Togetsukyo, and mountains in one frame",
                "📍 Entrance near Togetsukyo Bridge on the south bank of the river"
              ]
            }
          ],
          tips: [
            {
              type: "tip",
              text: "The monkey park is only worth doing if you're okay with a moderate hike. The trail is paved but steep. Reward: one of the best panoramic views in all of Kyoto."
            }
          ]
        },
        {
          label: "Lunch (12:30–1:30pm)",
          activities: [
            {
              title: "Lunch in Arashiyama",
              description: "Several excellent casual options near the bridge. Tofu is the local specialty — try yudofu (simmered tofu) which is both light and filling. The riverside restaurants have great views.",
              details: []
            }
          ],
          meals: [
            {
              type: "Lunch",
              name: "Yoshida-ya (or Arashiyama Yoshimura)",
              description: "Yoshida-ya: cozy soba/udon spot tucked a block from the bridge. Yoshimura: handmade soba with river views — excellent tempura soba set. Both casual and no reservations needed.",
              meta: "¥900-1,500/person · Cash preferred"
            }
          ]
        },
        {
          label: "Afternoon (2:00–5:00pm)",
          activities: [
            {
              title: "Train to Uji — Temple & Tea Town",
              description: "From Arashiyama, take the JR Sagano Line back toward Kyoto Station, then JR Nara Line to Uji (~55-65 min total, ¥340 from Saga-Arashiyama). This riverside town has been Japan's finest tea-growing region for over 800 years and contains one of Japan's most breathtaking temples.",
              details: [
                "🚆 Saga-Arashiyama → Kyoto (JR Sagano) → Uji (JR Nara Line): ~55 min, ¥340",
                "💡 Uji is a short detour back toward Osaka — you can head directly to Osaka from Uji Station",
                "🕑 Arrive Uji by 2:30pm to have comfortable time before closing"
              ]
            },
            {
              title: "Byōdō-in Phoenix Hall — Japan's Most Beautiful Temple",
              description: "Built in 1053 as a nobleman's villa, Byōdō-in's Phoenix Hall is one of Japan's architectural masterpieces — an elegant pavilion that appears to float above its reflecting pond. You've seen it before: it's on the Japanese 10-yen coin. Up close, it's even more extraordinary. Mid-March often brings early plum blossoms on the grounds.",
              details: [
                "🎫 ¥700 garden; ¥300 extra to enter Phoenix Hall (limited timed entry — book at ticket window on arrival)",
                "⏰ Last garden admission 5:15pm — arrive by 2:30-3:00pm for comfortable visit",
                "📍 10 min walk from JR Uji Station or 3 min from Keihan Uji Station",
                "📸 Best photo: from the far garden path reflecting the hall in the pond"
              ]
            },
            {
              title: "Uji Matcha Street (Byōdō-in Omotesandō)",
              description: "The stone-paved street leading to Byōdō-in is lined with tea shops selling everything matcha: soft serve, mochi, thick whisked tea ceremonies, parfaits. Multiple generations of tea families here — Nakamura Tokichi has been making tea since 1854. Take your time and sample freely.",
              details: [
                "🍵 Must-try: matcha soft serve (~¥400), ceremonial matcha + wagashi set (~¥1,200)",
                "🏪 Nakamura Tokichi (1854) — most famous, beautiful traditional shop",
                "🏪 Tsuen Tea — oldest tea shop in Japan (since 1160!)",
                "💡 Buy some loose matcha to bring home — quality far exceeds anything you'll find at airports"
              ]
            }
          ],
          tips: [
            {
              type: "reddit",
              text: "Uji is absolutely worth it if you have time. Byōdō-in is one of the top 5 temples I saw in all of Japan. The walk from the station through the matcha shops to the temple is really pleasant too.",
              cite: "r/JapanTravel"
            },
            {
              type: "tip",
              text: "Uji timing note: Byōdō-in's garden closes at 5:30pm (last admission 5:15pm). Aim to arrive by 3pm at the latest for a relaxed visit."
            }
          ]
        },
        {
          label: "Evening (5:30pm–)",
          activities: [
            {
              title: "Return to Osaka",
              description: "Head back to Osaka from Uji Station — it's actually closer to Osaka than to Arashiyama. Two options: JR Nara Line to Kyoto then JR toward Osaka (~55 min), or Kintetsu Kyoto Line from Kintetsu Uji Station to Kintetsu Namba (~45 min, very convenient for Namba area).",
              details: [
                "🚆 Kintetsu option: Kintetsu Uji → Namba (~45 min, ¥570) — drops you right in Namba",
                "🚆 JR option: JR Uji → Kyoto → Osaka (~55 min, ¥990)",
                "🍜 Back in Osaka by 6:30-7pm — perfect for Dotonbori dinner (takoyaki, ramen, kushikatsu)"
              ]
            }
          ],
          meals: [
            {
              type: "Dinner (back in Osaka)",
              name: "Dotonbori — Osaka's Street Food Capital",
              description: "After a day in Kyoto's temples, let Osaka remind you it's the food capital. Hit Dotonbori for takoyaki at Gindaco, kushikatsu at Daruma, or a bowl of ramen at Ichiran (Namba branch).",
              meta: "¥800-2,000/person · Cash widely accepted"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0095, lng: 135.6776, label: "Togetsukyo Bridge", num: 1, cat: "attraction", desc: "Iconic 'Moon Crossing' bridge over the Oi River" },
        { lat: 35.0168, lng: 135.6730, label: "Tenryū-ji Garden", num: 2, cat: "attraction", desc: "UNESCO Zen garden — one of Japan's greatest" },
        { lat: 35.0213, lng: 135.6712, label: "Saga-Toriimoto", num: 3, cat: "attraction", desc: "Preserved Meiji-era townscape, almost no tourists" },
        { lat: 35.0069, lng: 135.6781, label: "Iwatayama Monkey Park", num: 4, cat: "activity", desc: "170 wild Japanese macaques + panoramic Kyoto views" },
        { lat: 34.8936, lng: 135.8072, label: "Byōdō-in Temple", num: 5, cat: "attraction", desc: "UNESCO Phoenix Hall — on Japan's 10-yen coin" },
        { lat: 34.8956, lng: 135.8033, label: "Uji Matcha Street", num: 6, cat: "food", desc: "Tea shops serving Uji matcha since the 1100s" }
      ]
    }
  ],

  budgetTable: [
    { category: "Transport (Osaka ↔ Arashiyama + Uji return)", perPerson: "¥1,500–2,000", notes: "Hankyu + JR Sagano + JR Nara + Kintetsu return" },
    { category: "Tenryū-ji Garden", perPerson: "¥500–1,000", notes: "Garden only vs garden + buildings" },
    { category: "Monkey Park", perPerson: "¥600", notes: "Fixed entry fee" },
    { category: "Byōdō-in", perPerson: "¥700–1,000", notes: "¥700 garden + ¥300 for Phoenix Hall interior" },
    { category: "Meals (breakfast + lunch + matcha)", perPerson: "¥2,500–4,000", notes: "Casual options throughout" },
    { category: "Matcha sweets & souvenirs", perPerson: "¥1,000–2,000", notes: "Highly recommended — Uji matcha is world-class" },
    { category: "Total (excluding Osaka dinner)", perPerson: "¥6,800–10,000", notes: "~$45–65 USD per person" }
  ],

  practicalInfo: [
    { title: "When to Arrive in Arashiyama", text: "9am or earlier. Tour groups arrive from 10am onward. The morning hour makes an enormous difference." },
    { title: "Bamboo Grove Note", text: "You've wisely skipped it — the bamboo grove is the most photographed and most crowded spot in all of Kyoto. You're getting the better parts of Arashiyama with Tenryū-ji, Saga-Toriimoto, and the Monkey Park." },
    { title: "March Weather", text: "Mid-March in Kyoto is cool (8-15°C / 46-59°F). Bring layers. Comfortable walking shoes are essential — you're doing the Monkey Park hike." },
    { title: "Cherry Blossoms", text: "March 13 is likely too early for full cherry blossom bloom (peak is typically late March in Kyoto), but you may see early bloomers along the Oi River. Check bloom forecasts closer to your trip at japan-guide.com." },
    { title: "IC Card (Suica/ICOCA)", text: "Load an ICOCA or Suica card at any major station — works on all trains, buses, and many shops. Makes transfers faster and avoids ticket-machine confusion." },
    { title: "Uji Is Optional But Recommended", text: "If the group is tired after Arashiyama, you can skip Uji and head back to Osaka. But Byōdō-in is a genuine once-in-a-lifetime temple, and Uji is only 55 minutes away." }
  ]
};

// Run the fulfillment (synchronous)
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ ORDER FULFILLED!');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
