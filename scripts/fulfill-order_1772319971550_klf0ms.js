const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772319971550_klf0ms',
  email: 'bernardjhuang@gmail.com',
  destination: 'Telluride, CO, USA',
};

const itineraryData = {
  destination: 'Telluride, CO, USA',
  countryEmoji: '🇺🇸',
  title: 'Telluride: Powder, Peaks & Alpine Charm',
  subtitle: '4 nights of world-class skiing, stunning box canyon views, and a historic mountain town that punches way above its weight',
  description: 'Telluride is the most beautiful ski town in America — and it\'s not close. A Victorian mining town wedged into a dramatic box canyon, surrounded by 13,000-foot peaks on three sides, connected to Mountain Village by a free gondola that floats over the valley. Early March means deep snowpack, smaller crowds than February, and spring-like sunshine on the slopes. This itinerary balances big ski days with Telluride\'s surprisingly excellent dining scene, après-ski culture, and jaw-dropping scenery. Two people, four nights, pure mountain magic.',
  duration: '4 nights',
  dates: 'Mar 1 – Mar 5, 2026',
  budget: '$150 – $300 per person/day',
  pace: 'Moderate',
  bestFor: 'Couples, Ski enthusiasts, Mountain lovers',
  highlights: [
    'World-class skiing & snowboarding at Telluride Ski Resort',
    'Free gondola ride between Telluride and Mountain Village',
    'Historic Main Street with Victorian architecture',
    'Bridal Veil Falls — tallest free-falling waterfall in Colorado',
    'Incredible dining scene for a town of 2,500 people',
    'Stunning box canyon scenery from every angle',
    'Relaxed, uncrowded vibe compared to Vail/Aspen'
  ],

  essentials: [
    { title: '🛬 Getting There', text: 'Fly into Montrose Regional Airport (MTJ) — about 65 miles / 1.5 hours from Telluride. Telluride Regional Airport (TEX) has limited flights but is only 6 miles out. Mountain Limo and Telluride Express run shared shuttles from Montrose ($50-60/person). A rental car is helpful but not essential — town is very walkable and the gondola connects to Mountain Village for free.' },
    { title: '💵 Money', text: 'USD. Cards accepted everywhere. Telluride is an expensive ski town, but less absurd than Aspen. Lift tickets run $180-220/day — buy multi-day passes online in advance for 10-15% savings. Groceries at Clark\'s Market for breakfast/lunch supplies will save significant money on food.' },
    { title: '🌦️ March Weather', text: 'Daytime highs around 35-45°F (2-7°C) at town level, colder up top. Sunny days are common in early March but storms can roll in fast. Pack layers, goggles, sunscreen (the UV at 8,750-12,570ft is brutal), and lip balm. March snowpack is typically the deepest of the season.' },
    { title: '🎿 Ski Terrain', text: 'Telluride Ski Resort: 2,000+ acres, 148 trails, 4,425ft vertical drop (highest in North America). Terrain splits roughly 23% beginner, 36% intermediate, 41% advanced/expert. The Revelation Bowl and Gold Hill areas offer serious expert terrain. Prospect Bowl is a hidden gem for intermediates. Lifts open 9am-4pm.' },
    { title: '🏠 Where to Stay', text: 'Telluride town (walk to Lift 8 + nightlife) or Mountain Village (ski-in/ski-out, quieter). The Hotel Telluride and Victorian Inn are mid-range in town. Airbnb condos in Mountain Village offer ski-in/ski-out for $200-400/night. Budget tip: stay in town and ride the free gondola to Mountain Village slopes.' },
    { title: '🚡 The Gondola', text: 'The free gondola connecting Telluride to Mountain Village runs 7am-midnight daily (winter). It\'s 13 minutes each way and the views are spectacular. This is your primary transportation between the two villages and it\'s completely free — one of the best perks of Telluride.' }
  ],

  days: [
    // DAY 1 — Arrival & Town Exploration
    {
      num: 1,
      title: 'Arrival & Main Street Stroll',
      description: 'Arrive in Telluride, get settled, explore the charming historic Main Street, and ease into altitude with a mellow afternoon and a great dinner.',
      neighborhoods: 'Telluride Main Street · Colorado Avenue · Mountain Village',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check In',
              description: 'Fly into Montrose (MTJ) and shuttle or drive to Telluride. The drive through the San Juan Mountains is gorgeous — winding through red rock canyons before the valley opens up to reveal Telluride\'s box canyon. Check into your hotel or condo and take a moment to absorb the scenery — the town is literally surrounded by peaks on three sides.',
              details: [
                '💡 Pick up groceries at Clark\'s Market on Colorado Ave — breakfast supplies and snacks save $$$ over restaurant meals',
                '💡 Drink extra water today — you\'re at 8,750ft elevation and probably coming from sea level'
              ]
            },
            {
              title: 'Explore Historic Main Street',
              description: 'Telluride\'s Main Street (Colorado Avenue) is a National Historic Landmark District lined with colorful Victorian buildings from the 1880s mining era. Browse the shops, galleries, and outfitters. Pop into Telluride Sports or Bootdoctors if you need rental gear. Walk east toward the end of the canyon for views of Bridal Veil Falls in the distance — Colorado\'s tallest free-falling waterfall at 365 feet.',
              details: [
                '📍 Colorado Avenue, downtown Telluride',
                '💡 The town is only 8 blocks long and 12 blocks wide — you can walk the whole thing in 30 minutes',
                '💡 Look up at the end of the valley — Bridal Veil Falls and the old Smuggler-Union hydroelectric plant are stunning even from town'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Brown Dog Pizza',
              description: 'A Telluride institution — wood-fired pizzas with creative toppings, craft beer, and a lively atmosphere. The Sausage & Pepper and the Margherita are both excellent. Casual, affordable (by Telluride standards), and perfect for a first-night meal while adjusting to altitude.',
              meta: '📍 110 E Colorado Ave · 💰 $18-28/person · 🍕 Wood-fired pizza + great local beer selection'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Don\'t go hard on day 1 — altitude sickness is real at 8,750ft. Hydrate aggressively, skip the heavy drinking, and get to bed early for your first ski day.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ride the Free Gondola at Night 🚡',
              description: 'Take the free gondola from Telluride up to Mountain Village after dinner. The 13-minute ride offers incredible views of the valley lights below and stars above. Grab a drink at one of the Mountain Village bars or just enjoy the ride and head back. The gondola runs until midnight.',
              details: [
                '📍 Station St. Sophia, south end of San Juan Ave',
                '🕐 Runs until midnight in winter',
                '💡 The ride itself is the attraction — the views at night are magical'
              ]
            }
          ],
          meals: [],
          tips: []
        }
      ],
      mapPins: [
        { lat: 37.9375, lng: -107.8123, label: 'Telluride Main Street', num: 1, cat: 'attraction', desc: 'Historic Victorian mining town — 8 blocks of charm' },
        { lat: 37.9275, lng: -107.7702, label: 'Bridal Veil Falls (viewpoint)', num: 2, cat: 'attraction', desc: 'Colorado\'s tallest free-falling waterfall — 365ft' },
        { lat: 37.9358, lng: -107.8094, label: 'Brown Dog Pizza', num: 3, cat: 'restaurant', desc: 'Wood-fired pizza — Telluride institution' },
        { lat: 37.9366, lng: -107.8126, label: 'Gondola Station (Telluride)', num: 4, cat: 'transport', desc: 'Free gondola to Mountain Village — runs until midnight' }
      ]
    },

    // DAY 2 — First Big Ski Day
    {
      num: 2,
      title: 'First Tracks on the Mountain',
      description: 'A full day on the slopes exploring Telluride Ski Resort\'s incredible terrain — from groomed cruisers to Prospect Bowl\'s wide-open intermediate runs. Après-ski on the mountain, dinner in town.',
      neighborhoods: 'Telluride Ski Resort · Mountain Village · Telluride Town',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ski Day — Telluride Ski Resort ⛷️',
              description: 'Grab the gondola to Mountain Village and hit the slopes. Start with warm-up runs on the groomed blue cruisers off Lift 4 (Meadows) and Lift 9 (Village Express) to get your legs and lungs adjusted to the altitude. Then work your way over to Prospect Bowl — an entire mountain face of intermediate terrain with some of the best views on the mountain. The snow in early March is typically deep and well-groomed.',
              details: [
                '📍 Lifts open 9am, gondola from town starts at 7am',
                '💰 Lift tickets $180-220/day — buy multi-day online for savings',
                '💡 Start on Lift 4 (Meadows) for mellow warm-up laps',
                '💡 Prospect Bowl opens at 9:30am — get there early before it gets tracked out',
                '⚠️ Altitude matters! Take breaks, drink water, don\'t push too hard on day 1'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Alpino Vino',
              description: 'The highest altitude dining in North America at 12,000ft — a European-style wine bar and restaurant accessible only by skiing. Incredible views, fondue, charcuterie, and an excellent wine list. It\'s a splurge but an unforgettable experience. Book a reservation.',
              meta: '📍 Ski to Lift 14 (See Forever) · 💰 $40-60/person · 🍷 Reservation strongly recommended — book online'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Alpino Vino is worth every penny. Ski up to 12,000 feet, have fondue and wine with panoramic views, then ski back down. There\'s nothing else like it.', cite: 'r/skiing' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Afternoon Skiing & Après',
              description: 'After lunch, explore the front side — Plunge and Spiral Stairs are classic Telluride runs, steep but manageable for strong intermediates. If you\'re expert-level, hike the short bootpack to Palmyra Peak for the most insane views in Colorado skiing. Wrap up by 3:30pm and head to après-ski.',
              details: [
                '💡 Tomboy Road and Plunge are iconic Telluride runs — steep, sustained, and fun',
                '💡 Last chair is 4pm on most lifts'
              ]
            },
            {
              title: 'Après-Ski at Tomboy Tavern 🍺',
              description: 'Right at the base of the gondola in Mountain Village — grab a seat on the sunny deck, order a local craft beer or hot toddy, and watch skiers come down the last runs. The deck gets golden afternoon sun and the views of the ski area are perfect.',
              details: [
                '📍 Mountain Village, Heritage Plaza',
                '💰 $8-14/drink',
                '💡 Sit outside on the deck — afternoon sun makes it feel way warmer than it is'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Marmotte',
              description: 'An intimate French bistro that\'s been a Telluride favorite for decades. Classic French dishes — duck confit, steak frites, bouillabaisse — in a cozy, romantic setting. Perfect for a couple\'s dinner. The wine list is excellent.',
              meta: '📍 150 W San Juan Ave · 💰 $50-75/person · 🍷 One of Telluride\'s most beloved restaurants'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 37.9366, lng: -107.8126, label: 'Gondola to Mountain Village', num: 1, cat: 'transport', desc: 'Free ride to the slopes — 13 minutes' },
        { lat: 37.9425, lng: -107.8475, label: 'Prospect Bowl', num: 2, cat: 'activity', desc: 'Wide-open intermediate terrain with stunning views' },
        { lat: 37.9505, lng: -107.8385, label: 'Alpino Vino', num: 3, cat: 'restaurant', desc: 'Highest altitude restaurant in North America — 12,000ft' },
        { lat: 37.9317, lng: -107.8561, label: 'Tomboy Tavern', num: 4, cat: 'restaurant', desc: 'Après-ski deck with mountain views' },
        { lat: 37.9378, lng: -107.8133, label: 'La Marmotte', num: 5, cat: 'restaurant', desc: 'French bistro — duck confit and great wine' }
      ]
    },

    // DAY 3 — Adventure Day
    {
      num: 3,
      title: 'Expert Terrain & Hot Springs Day Trip',
      description: 'Morning on the mountain exploring expert terrain or tree skiing, then drive to Orvis Hot Springs for a soak in natural hot springs surrounded by mountains.',
      neighborhoods: 'Telluride Ski Resort · Gold Hill · Ridgway / Orvis Hot Springs',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Morning Ski — Gold Hill & Revelation Bowl',
              description: 'Today, push your limits. Gold Hill (Lift 14 area) offers expert chutes, bumps, and wide-open steeps with views that stretch to Utah. If you\'re not expert-level, the See Forever trail from Lift 14 is a stunning blue cruiser that traverses the entire mountain with panoramic views. Revelation Bowl offers hike-to expert terrain in a spectacular alpine cirque.',
              details: [
                '📍 Access via Lift 14 (Prospect Express) then Lift 12',
                '💡 See Forever is the best scenic run on the mountain — intermediate-friendly and jaw-dropping views',
                '💡 Gold Hill chutes: Bald Mountain, Gold Hill Chutes 1-10 — steep and exposed',
                '⚠️ Check avalanche conditions at Telluride Ski Patrol before venturing into Revelation Bowl'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Baked in Telluride',
              description: 'A beloved local bakery and café on Main Street. Massive breakfast burritos, fresh-baked pastries, sandwiches, and excellent coffee. Grab-and-go or sit in the cozy café. Great spot for a quick lunch before heading to the hot springs.',
              meta: '📍 127 S Fir St · 💰 $10-16/person · ☕ The breakfast burrito is legendary'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Orvis Hot Springs Soak ♨️',
              description: 'Drive 45 minutes north to Orvis Hot Springs near Ridgway — natural hot springs pools of varying temperatures (98-112°F) set against a stunning mountain backdrop. This is the perfect recovery after two days of skiing. The outdoor pools are clothing-optional with a peaceful, chill vibe. There\'s also an indoor pool if you prefer privacy.',
              details: [
                '📍 1585 County Rd 3, Ridgway, CO (45 min drive north)',
                '🕐 Open 9am-10pm daily',
                '💰 $22/person',
                '💡 Bring your own towel to save the $2 rental fee',
                '💡 The drive through the San Juan Mountains to Ridgway is stunning — stop at Dallas Divide viewpoint for Mt. Sneffels photos'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: '221 South Oak',
              description: 'Telluride\'s upscale farm-to-table gem — creative American cuisine with seasonal ingredients in an elegant but unpretentious setting. The tasting menu is exceptional, or go à la carte. Elk tenderloin, Colorado lamb, and inventive vegetable dishes. One of the best meals you\'ll have in any ski town.',
              meta: '📍 221 S Oak St · 💰 $60-90/person · 🌟 Arguably the best restaurant in Telluride — reserve ahead'
            }
          ],
          tips: [
            { type: 'reddit', text: '221 South Oak is a must for a nice dinner in Telluride. The food is genuinely world-class and the vibe is perfect — upscale without being stuffy.', cite: 'r/Telluride' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.9505, lng: -107.8385, label: 'Gold Hill / Revelation Bowl', num: 1, cat: 'activity', desc: 'Expert terrain with alpine cirque and panoramic views' },
        { lat: 37.9336, lng: -107.8108, label: 'Baked in Telluride', num: 2, cat: 'restaurant', desc: 'Bakery & café — legendary breakfast burritos' },
        { lat: 38.1367, lng: -107.7517, label: 'Orvis Hot Springs', num: 3, cat: 'activity', desc: 'Natural hot springs pools — perfect post-ski recovery' },
        { lat: 37.9370, lng: -107.8125, label: '221 South Oak', num: 4, cat: 'restaurant', desc: 'Farm-to-table fine dining — best restaurant in Telluride' }
      ]
    },

    // DAY 4 — Last Ski Day & Farewell
    {
      num: 4,
      title: 'Last Runs & Farewell Dinner',
      description: 'Soak up every last turn on the mountain, explore any terrain you missed, then close out with a celebration dinner and one final gondola ride under the stars.',
      neighborhoods: 'Telluride Ski Resort · Mountain Village · Telluride Town',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Ski Day — Greatest Hits 🎿',
              description: 'Last day on the mountain — revisit your favorite runs and check off anything you missed. Take a few laps on Plunge for the classic Telluride experience, cruise See Forever one more time for the views, or venture into the Prospect Bowl glades for some tree skiing. March snow is often soft and forgiving — perfect for pushing your limits a little.',
              details: [
                '📍 Start early — lifts open 9am',
                '💡 Ski the Bear Creek area for quiet, uncrowded runs on the Telluride side',
                '💡 Take photos from Lift 14 — the 360° views of the San Juans are absurd',
                '💡 Wrap up by 2-3pm to enjoy the afternoon in town'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Bon Vivant',
              description: 'A cozy mountain-lodge restaurant on the slopes — accessible by skiing or the gondola. Elevated comfort food: burgers, salads, and daily specials with a great deck for sunny March lunches. Less crowded and more interesting than the standard lodge cafeteria.',
              meta: '📍 Mountain Village, near Gondola station · 💰 $20-30/person'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Explore Town & Last Shopping',
              description: 'After skiing, stroll through town one last time. Browse Between the Covers Bookstore for a good read, check out the galleries along Colorado Avenue, or grab a coffee at Ghost Town Coffee Roasters. Pick up souvenirs — Telluride trucker hats, local hot sauce, or turquoise jewelry.',
              details: [
                '📍 Colorado Avenue, downtown Telluride',
                '💡 Ghost Town Coffee Roasters on Main Street has excellent espresso',
                '💡 Between the Covers is one of the best independent bookstores in Colorado'
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
              title: 'Farewell Dinner & Night Gondola',
              description: 'End the trip right. After dinner, take one final gondola ride — the night views of Telluride\'s lights nestled in the box canyon are unforgettable. Toast to a perfect trip and soak in the silence and the stars at 10,500 feet.',
              details: [
                '💡 The gondola ride at night is even more magical than during the day',
                '💡 Dress warm — it gets cold after dark at this altitude'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Allred\'s Restaurant',
              description: 'The crown jewel of Telluride dining — located at the top of the gondola at 10,551 feet in Mountain Village. Floor-to-ceiling windows with panoramic views of the San Juan Mountains. The menu is refined American with Colorado influences — bison, elk, fresh seafood, and an award-winning wine list. Perfect farewell dinner.',
              meta: '📍 Top of gondola, Station St. Sophia · 💰 $70-100/person · 🌟 Reservations essential — book well in advance'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Allred\'s at the top of the gondola is one of the best restaurant experiences in Colorado. The views alone are worth it, and the food actually matches the setting.', cite: 'r/Telluride' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.9366, lng: -107.8126, label: 'Telluride Ski Resort', num: 1, cat: 'activity', desc: 'Final day — greatest hits on 2,000+ acres' },
        { lat: 37.9375, lng: -107.8123, label: 'Colorado Avenue', num: 2, cat: 'shopping', desc: 'Last shopping — bookstore, galleries, souvenirs' },
        { lat: 37.9366, lng: -107.8126, label: 'Ghost Town Coffee', num: 3, cat: 'restaurant', desc: 'Excellent local roaster on Main Street' },
        { lat: 37.9317, lng: -107.8561, label: 'Allred\'s Restaurant', num: 4, cat: 'restaurant', desc: 'Fine dining at 10,551ft — top of the gondola' }
      ]
    },

    // DAY 5 — Departure
    {
      num: 5,
      title: 'Departure Day',
      description: 'A relaxed morning in Telluride before heading to the airport. Grab breakfast, take one last look at the mountains, and drive out through the stunning San Juan valley.',
      neighborhoods: 'Telluride Town · Montrose',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Breakfast & Departure',
              description: 'Sleep in, grab a final breakfast, and take a last walk down Colorado Avenue. The morning light on the box canyon walls is beautiful — soak it in. Then drive back to Montrose Airport through the San Juan Mountains. The drive out is just as stunning as the drive in.',
              details: [
                '💡 Montrose Airport (MTJ) is 1.5 hours — leave 3 hours before your flight',
                '💡 Stop at the Dallas Divide viewpoint on Hwy 62 for one last mountain panorama'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'The Butcher & The Baker',
              description: 'A charming café with excellent coffee, pastries, and breakfast sandwiches. The egg sandwich on house-baked bread is simple perfection. Quick, delicious, and a great send-off.',
              meta: '📍 217 E Colorado Ave · 💰 $10-16/person · ☕ Perfect last breakfast'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If your flight is late, consider one last half-day on the slopes — many hotels will hold bags. March mornings often have the best snow conditions.' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.9375, lng: -107.8100, label: 'The Butcher & The Baker', num: 1, cat: 'restaurant', desc: 'Charming café — perfect last breakfast' },
        { lat: 38.1417, lng: -107.8939, label: 'Dallas Divide Viewpoint', num: 2, cat: 'attraction', desc: 'Iconic Mt. Sneffels panorama — last photo op' },
        { lat: 38.5098, lng: -107.8943, label: 'Montrose Airport (MTJ)', num: 3, cat: 'transport', desc: '1.5 hours from Telluride — your way home' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (split 2 ways)', perDay: '$100-200', total: '$400-800' },
    { category: 'Lift Tickets (multi-day)', perDay: '$160-200', total: '$480-600' },
    { category: 'Meals & Drinks', perDay: '$50-80', total: '$200-320' },
    { category: 'Equipment Rental (if needed)', perDay: '$50-70', total: '$150-210' },
    { category: 'Orvis Hot Springs', perDay: '—', total: '$22' },
    { category: 'Montrose Shuttle (round trip)', perDay: '—', total: '$100-120' },
    { category: 'TOTAL (per person)', perDay: '', total: '$1,350-2,070' }
  ],

  practicalInfo: [
    { title: '🚗 Getting Around', items: ['The free gondola connects Telluride and Mountain Village — runs 7am to midnight', 'Telluride town is tiny and entirely walkable — 8 blocks long', 'Galloping Goose free bus runs within town', 'Rental car helpful for Orvis Hot Springs day trip and airport transfer', 'Uber/Lyft essentially don\'t exist here'] },
    { title: '🏔️ Altitude', items: ['Telluride sits at 8,750ft — Mountain Village at 9,545ft — ski area tops at 13,150ft', 'Drink LOTS of water, especially the first two days', 'Go easy on alcohol the first night — it hits harder at altitude', 'If you feel headaches or nausea, rest and hydrate — it usually passes in 24 hours'] },
    { title: '📱 Cell Service', items: ['Decent in town and Mountain Village', 'Spotty to none on some ski runs and the drive to/from Montrose', 'Download offline maps before arriving'] },
    { title: '🎿 Rental Gear', items: ['Bootdoctors and Telluride Sports on Main Street are the top shops', 'Book online in advance for 10-15% off', 'Demo packages let you try different skis each day'] }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
