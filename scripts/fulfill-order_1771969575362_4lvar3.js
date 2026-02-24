const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771969575362_4lvar3',
  email: 'psyduckler@gmail.com',
  destination: 'Alberta, Canada',
  startDate: '2026-07-01',
  endDate: '2026-07-05',
  groupSize: '2',
  requests: ''
};

const itineraryData = {
  destination: 'Alberta, Canada',
  countryEmoji: '🇨🇦',
  title: 'Wild Heart of the Rockies',
  subtitle: '4 nights of turquoise lakes, glacier walks & mountain town magic for two',
  description: "Alberta in July is the Canadian Rockies at their absolute peak — wildflowers carpeting alpine meadows, glacial lakes glowing impossible shades of blue, and daylight stretching past 10pm. This itinerary takes you from the cosmopolitan energy of Calgary through the jaw-dropping landscapes of Banff and Jasper National Parks. You'll hike to hidden lakes, walk on ancient glaciers, spot elk and bears from the road, and eat surprisingly well in mountain towns that have evolved far beyond pub grub. Canada Day on July 1st means you'll arrive to fireworks, red-and-white celebrations, and a country in full summer mode.",
  duration: '4 nights',
  dates: 'Jul 1 – Jul 5, 2026',
  budget: 'Free',
  pace: 'Moderate–Active',
  bestFor: 'Couples · Nature · Adventure',
  highlights: [
    'Lake Louise — the most photographed lake in Canada, and it earns every shot',
    'Icefields Parkway — 230km of the most scenic driving on Earth',
    'Columbia Icefield Skywalk & Athabasca Glacier — walk on ancient ice',
    'Moraine Lake — the turquoise gem that launched a thousand desktop wallpapers',
    'Johnston Canyon — a slot canyon hike through waterfalls and catwalks'
  ],

  essentials: [
    { title: '🏔️ July Weather', text: 'July in the Rockies averages 15-25°C (59-77°F) in valleys, but can drop to 5°C at higher elevations and glaciers. Pack layers — mornings are cool, afternoons warm, and weather changes fast. Afternoon thunderstorms are common. Sunscreen is essential at altitude.' },
    { title: '🚗 Getting Around', text: 'A rental car is essential. Pick up at Calgary Airport (YYC). The drive to Banff is 90 minutes on the Trans-Canada Highway. Roads are excellent but watch for wildlife — elk and bears regularly cross. Gas stations exist in Banff, Lake Louise, and Saskatchewan River Crossing (fill up here on the Icefields Parkway — no gas for 150km).' },
    { title: '🐻 Wildlife Safety', text: 'You will likely see bears, elk, mountain goats, and bighorn sheep. Carry bear spray on all hikes (rent from Wilson Mountain Sports in Banff). Make noise on trails. Never approach wildlife. Store food in bear-proof containers. Parks Canada posts trail advisories — check before hiking.' },
    { title: '🎫 Park Passes', text: 'You need a Parks Canada Discovery Pass — $72.25 CAD per person for an annual pass or $10.50/day. Buy online or at park gates. Required for Banff and Jasper National Parks. Parking at Lake Louise and Moraine Lake requires a separate reservation via Parks Canada in peak season — book weeks ahead.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-07-01',
      neighborhoods: 'Calgary · Banff · Banff Avenue',
      title: 'Canada Day in the Rockies',
      description: "Arrive in Calgary on Canada Day and drive straight into the mountains. The Trans-Canada Highway west of Calgary is one of those drives where the Rockies appear on the horizon and just keep getting bigger until they surround you completely. Settle into Banff — a genuine mountain town that happens to sit inside a national park — and celebrate Canada's birthday with the locals.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Calgary to Banff Drive',
              description: "Pick up your rental car at YYC and head west on the Trans-Canada (Highway 1). The 130km drive takes about 90 minutes, and the scenery transitions from prairie to foothills to full-blown Rocky Mountain grandeur. Stop at the Banff park gate to buy your Parks Canada pass.",
              details: [
                '🚗 Calgary Airport to Banff — 130km, ~90 mins via Hwy 1',
                '🎫 Buy Parks Canada pass at the east gate — $10.50/person/day or $72.25 annual',
                '⛽ Fill up in Canmore (last cheap gas before Banff)',
                '🇨🇦 Canada Day — expect festive vibes everywhere'
              ]
            },
            {
              title: 'Explore Banff Avenue & Town',
              description: "Banff's main strip is walkable and charming — independent shops, outdoor gear stores, cafés, and restaurants with mountain views in every direction. Stroll the Bow River boardwalk, check out the Banff Park Museum (a wooden Victorian-era natural history collection), and soak in the mountain town atmosphere.",
              details: [
                '🏔️ Cascade Mountain looms at the end of Banff Ave — iconic view',
                '🦌 Elk wander through town regularly — keep your distance',
                '🛍️ Wild Mountain for local art, Patagonia for gear, Rocky Mountain Soap for gifts',
                '🎆 Canada Day fireworks usually launch from the recreation grounds around 11pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Park Distillery',
              description: 'Farm-to-table restaurant and craft distillery right on Banff Ave. They make their own vodka, gin, and whisky using glacial water from the Rockies. The campfire-grilled meats and wood-fired dishes are excellent. Buzzy Canada Day atmosphere guaranteed.',
              meta: '💰 $30-50 CAD pp · 📍 219 Banff Ave · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'If you arrive early enough, drive up to the Mount Norquay lookout (10 mins from town) for a panoramic view of Banff and the Bow Valley. Free, and the late afternoon light is gorgeous.' }
          ]
        }
      ],
      mapPins: [
        { lat: 51.1784, lng: -115.5708, label: 'Banff Town', num: 1, cat: 'attraction', desc: 'Mountain town inside a national park' },
        { lat: 51.1780, lng: -115.5700, label: 'Banff Avenue', num: 2, cat: 'attraction', desc: 'Main street with Cascade Mountain views' },
        { lat: 51.1785, lng: -115.5690, label: 'Park Distillery', num: 3, cat: 'food', desc: 'Craft distillery and farm-to-table dining' },
        { lat: 51.2050, lng: -115.5960, label: 'Mt Norquay Lookout', num: 4, cat: 'attraction', desc: 'Panoramic views over Banff and the Bow Valley' }
      ]
    },
    {
      num: 2,
      date: '2026-07-02',
      neighborhoods: 'Johnston Canyon · Lake Louise · Moraine Lake',
      title: 'Turquoise Lakes & Waterfall Canyons',
      description: "Today is the day that ruins you for every other landscape. Johnston Canyon's catwalks hang over thundering waterfalls, Lake Louise sits like a pool of liquid turquoise beneath Victoria Glacier, and Moraine Lake — tucked in the Valley of the Ten Peaks — might be the most beautiful place in North America. Get up early. The early light and smaller crowds are worth every lost minute of sleep.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Johnston Canyon Hike',
              description: "Start early (by 7:30am) to beat the crowds at this slot canyon hike along the Bow Valley Parkway. Steel catwalks bolted into canyon walls take you past two stunning waterfalls — the Lower Falls (1.1km, 30 mins) and the Upper Falls (2.7km, 1 hour). The turquoise pools and limestone walls are mesmerizing. In July, the water volume is at its peak.",
              details: [
                '🥾 Lower Falls: 1.1km, easy — wheelchair accessible to the first viewpoint',
                '💦 Upper Falls: 2.7km total, moderate — the payoff is enormous',
                '⏰ Start by 7:30am — by 10am the trail is a conga line',
                '🐻 Bear country — carry bear spray and make noise'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tooloulou\'s',
              description: 'Banff\'s beloved breakfast spot — Cajun-inspired brunch with a mountain twist. The beignets are legendary, and the breakfast poutine is absurd in the best way. Fuel up before a big hiking day.',
              meta: '💰 $15-22 CAD · 📍 Banff Ave · Opens 8am · Expect a weekend wait'
            }
          ],
          tips: [
            { type: 'tip', text: 'Drive the Bow Valley Parkway (1A) instead of the Trans-Canada to Johnston Canyon — it\'s slower, quieter, and you\'re much more likely to spot wildlife. Watch for bears in meadows.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Louise',
              description: "Park at the Lake Louise lot (arrive before 9:30am or after 5pm to guarantee a spot, or take the Parks Canada shuttle). The first view of the lake stops everyone mid-step — the color is not edited, not exaggerated, it really is that shade of impossible turquoise. Walk the flat, easy lakeshore trail (2km) to the far end for the best glacier-reflecting views.",
              details: [
                '🏔️ Free to visit — parking lot fills by 9:30am in July',
                '🚌 Parks Canada shuttle from Lake Louise village — reserve online',
                '🚶 Lakeshore trail: 2km each way, flat, easy, stunning',
                '📸 The most photogenic spot is from the far end, looking back with the Chateau in frame'
              ]
            },
            {
              title: 'Moraine Lake',
              description: "If Lake Louise is famous, Moraine Lake is legendary. Accessible only by Parks Canada shuttle (private cars banned in peak season), this lake sits in the Valley of the Ten Peaks and is so photogenic it was on the Canadian $20 bill. Climb the short Rockpile Trail (15 mins) for THE viewpoint — ten peaks reflected in blue-green water.",
              details: [
                '🚌 Shuttle only in summer — book at reservation.pc.gc.ca weeks ahead',
                '📸 Rockpile Trail — the classic viewpoint. 15 mins, worth every step',
                '🛶 Canoe rentals available — $135 CAD/hour but unforgettable',
                '🧊 The color comes from glacial rock flour — finest in July when meltwater peaks'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Bison',
              description: 'Banff\'s best restaurant for regional Canadian cuisine. Elk tartare, Alberta beef, bison short ribs, and foraged mushrooms in a rustic-chic space. The wine list focuses on BC and Alberta producers. A proper celebration dinner after an epic day.',
              meta: '💰 $45-70 CAD pp · 📍 Bear Street, Banff · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.2455, lng: -115.8410, label: 'Johnston Canyon', num: 1, cat: 'attraction', desc: 'Slot canyon with catwalk trails past waterfalls' },
        { lat: 51.4167, lng: -116.1767, label: 'Lake Louise', num: 2, cat: 'attraction', desc: 'Iconic turquoise glacial lake' },
        { lat: 51.3217, lng: -116.1860, label: 'Moraine Lake', num: 3, cat: 'attraction', desc: 'Valley of the Ten Peaks — former $20 bill' },
        { lat: 51.1760, lng: -115.5695, label: 'The Bison', num: 4, cat: 'food', desc: 'Regional Canadian cuisine — elk, bison, foraged mushrooms' }
      ]
    },
    {
      num: 3,
      date: '2026-07-03',
      neighborhoods: 'Icefields Parkway · Columbia Icefield · Peyto Lake',
      title: 'The Greatest Road Trip on Earth',
      description: "The Icefields Parkway (Highway 93N) from Lake Louise to the Columbia Icefield is 130km of the most jaw-dropping mountain scenery on the planet. Glacier-capped peaks, waterfalls tumbling from cliffs, turquoise rivers, and wildlife around every bend. Today you drive it, stop everywhere, walk on a glacier, and stand on a glass-floored skywalk above a valley that makes you feel very small and very alive.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Icefields Parkway Drive — Southern Section',
              description: "Leave Banff early and head north on Highway 93. Every 10 minutes brings another stop-worthy viewpoint. Bow Lake appears first — a vast turquoise sheet beneath Bow Glacier. Then Peyto Lake — hike the short trail to the lookout for one of Canada's most iconic views: a wolf-head-shaped lake in preposterous blue. Mistaya Canyon is a quick, easy detour with churning emerald water.",
              details: [
                '⛽ FILL UP in Lake Louise — no gas until Saskatchewan River Crossing (77km)',
                '📸 Peyto Lake lookout: 15-min walk from parking lot — go early for no crowds',
                '🌊 Mistaya Canyon: 15-min walk — thundering water through carved limestone',
                '🐐 Watch for mountain goats on road shoulders — they lick road salt'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Columbia Icefield — Athabasca Glacier',
              description: "The Columbia Icefield is the largest ice field in the Rockies — feeding rivers that flow to three oceans. The Athabasca Glacier tongue descends to roadside. Book the Ice Explorer tour (massive all-terrain buses drive onto the glacier) and the Glacier Skywalk — a glass-floored platform 280 meters above the Sunwapta Valley. Standing on ancient ice with mountains in every direction is genuinely humbling.",
              details: [
                '🧊 Ice Explorer + Skywalk combo: ~$115 CAD pp — book at icefieldsadventure.com',
                '⏰ Tours run every 15-30 mins, 10am-5pm — afternoon has shorter lines',
                '🧤 Temperature on the glacier: around 0-5°C even in July — bring warm layers',
                '🏔️ The Skywalk is incredible — 280m above the valley floor on glass'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'The Crossing Resort',
              description: 'The only food and gas stop between Lake Louise and the Icefield. Not gourmet, but the cafeteria-style meals are decent and the location can\'t be beat — surrounded by peaks. Fill your tank here too.',
              meta: '💰 $12-20 CAD · 📍 Saskatchewan River Crossing · Cash & card'
            },
            {
              type: '🍽️ Dinner',
              name: 'Juniper Hotel Bistro',
              description: 'Back in Banff, this bistro at the Juniper Hotel has one of the best deck views in town — overlooking Mount Rundle and the Bow Valley. Creative mountain cuisine, excellent cocktails, and a sunset that paints the mountains pink.',
              meta: '💰 $35-55 CAD pp · 📍 Juniper Hotel, Banff · Deck seating is magical at sunset'
            }
          ],
          tips: [
            { type: 'tip', text: 'The Icefields Parkway is a full day. Leave by 7:30am, drive slowly, stop often. The road itself is the destination. Keep your eyes peeled — bears, elk, and mountain goats are common along the route.' }
          ]
        }
      ],
      mapPins: [
        { lat: 51.6723, lng: -116.4585, label: 'Bow Lake', num: 1, cat: 'attraction', desc: 'Vast turquoise lake beneath Bow Glacier' },
        { lat: 51.7253, lng: -116.5103, label: 'Peyto Lake Lookout', num: 2, cat: 'attraction', desc: 'Wolf-head-shaped lake — Canada\'s most iconic viewpoint' },
        { lat: 51.8860, lng: -116.5300, label: 'Mistaya Canyon', num: 3, cat: 'attraction', desc: 'Emerald water churning through carved limestone' },
        { lat: 52.2194, lng: -117.2240, label: 'Columbia Icefield', num: 4, cat: 'attraction', desc: 'Walk on ancient ice and glass-floored Skywalk' },
        { lat: 51.8500, lng: -116.5050, label: 'The Crossing Resort', num: 5, cat: 'food', desc: 'Only gas and food stop on the Parkway' }
      ]
    },
    {
      num: 4,
      date: '2026-07-04',
      neighborhoods: 'Banff · Sulphur Mountain · Bow River · Vermilion Lakes',
      title: 'Gondolas, Hot Springs & Golden Hour',
      description: "Your last full day is about savoring Banff itself. Ride the gondola to the top of Sulphur Mountain for 360° views of six mountain ranges, soak in the historic Banff Upper Hot Springs (the reason this national park exists), paddle the Bow River, and catch sunset at Vermilion Lakes — where the mountains glow pink and orange reflected in still water.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Banff Gondola — Sulphur Mountain',
              description: "The 8-minute gondola ride to the summit of Sulphur Mountain (2,281m) delivers 360° panoramic views of the Bow Valley, Banff town, and six mountain ranges stretching to the horizon. At the top, the Banff Skywalk is a 1km boardwalk along the ridge with interpretive exhibits. On a clear July morning, the views are limitless.",
              details: [
                '🚡 Opens 8am in summer · $72 CAD pp — book online for guaranteed time',
                '🏔️ Clear mornings give the best views — go first thing',
                '📸 The rooftop observation deck is the highest point — full 360° panorama',
                '🥾 Option: hike up (5.5km, 2h) and gondola down for free descent'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Banff Upper Hot Springs',
              description: "These natural hot springs at 1,585m elevation are the reason Banff National Park was created in 1885. The outdoor pool is fed by mineral-rich water at 37-40°C, with views of Mount Rundle. After three days of hiking and driving, this is exactly what your muscles need.",
              details: [
                '♨️ Open 10am-10pm · $8.48 CAD · Swimsuit rental available',
                '🏔️ The view of Rundle from the pool is peak Canadian Rockies',
                '⏰ Weekday afternoons are quietest — go between 2-4pm',
                '💆 The minerals actually help sore muscles — not just marketing'
              ]
            },
            {
              title: 'Bow River & Bow Falls Walk',
              description: "A gentle walk along the Bow River takes you past the iconic Bow Falls — a wide, powerful cascade that you might recognize from Marilyn Monroe's 'River of No Return.' The riverside trail is flat, shaded, and perfect for a relaxed afternoon stroll.",
              details: [
                '🚶 Bow Falls trail: 1.5km from downtown, flat and easy',
                '🎬 Bow Falls appeared in the 1954 Marilyn Monroe film',
                '🦌 Elk frequently graze along the riverbanks — keep 30m distance'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Whitebark Café',
              description: 'Cozy café in the Aspen Lodge with excellent espresso, fresh pastries, and mountain views. Great for a leisurely start before the gondola.',
              meta: '💰 $10-18 CAD · 📍 Banff Aspen Lodge · Opens 6:30am'
            },
            {
              type: '🍽️ Farewell Dinner',
              name: 'Chuck\'s Steakhouse',
              description: 'Alberta is beef country, and Chuck\'s is where Banff goes for the best of it. AAA Alberta beef, house-made sauces, and a warm, unpretentious vibe. The ribeye is the move. Perfect farewell dinner for your last night in the Rockies.',
              meta: '💰 $50-75 CAD pp · 📍 Banff Ave · Reservations essential in July'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Vermilion Lakes Sunset',
              description: "Drive 5 minutes from Banff to the three Vermilion Lakes for the most spectacular sunset in the park. Mount Rundle and Sulphur Mountain reflected in glassy water, sky turning every shade of orange and pink. Bring a beverage. This is the way to end an Alberta trip.",
              details: [
                '🌅 Sunset in early July is around 9:45pm — arrive by 9:15pm',
                '📸 Third Vermilion Lake has the best Rundle reflections',
                '🦟 Mosquitoes come out at dusk — bring repellent',
                '🐻 Stay aware — bears frequent this area at dusk'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.1485, lng: -115.5588, label: 'Banff Gondola', num: 1, cat: 'attraction', desc: 'Summit views of six mountain ranges' },
        { lat: 51.1505, lng: -115.5580, label: 'Banff Upper Hot Springs', num: 2, cat: 'attraction', desc: 'Historic hot springs with mountain views' },
        { lat: 51.1695, lng: -115.5600, label: 'Bow Falls', num: 3, cat: 'attraction', desc: 'Powerful cascade on the Bow River' },
        { lat: 51.1830, lng: -115.6050, label: 'Vermilion Lakes', num: 4, cat: 'attraction', desc: 'Sunset reflections of Mount Rundle' },
        { lat: 51.1762, lng: -115.5710, label: 'Chuck\'s Steakhouse', num: 5, cat: 'food', desc: 'AAA Alberta beef — Banff\'s best steakhouse' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$100-150 CAD/night', midrange: '$200-350 CAD/night', luxury: '$500-1,000+ CAD/night' },
    { category: 'Meals (per person)', budget: '$30-50 CAD/day', midrange: '$60-100 CAD/day', luxury: '$150-250 CAD/day' },
    { category: 'Car Rental', budget: '$50-80 CAD/day', midrange: '$80-120 CAD/day', luxury: '$150-250 CAD/day' },
    { category: 'Activities', budget: '$20-40 CAD/day', midrange: '$50-100 CAD/day', luxury: '$150-300 CAD/day' },
    { category: 'Columbia Icefield Tour', budget: '$115 CAD pp', midrange: '$115 CAD pp', luxury: '$250 CAD pp (private)' },
    { category: '4-Night Total (per person)', budget: '$800-1,200 CAD', midrange: '$1,500-2,500 CAD', luxury: '$3,500-6,000 CAD' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Calgary International Airport (YYC) — direct flights from most major North American cities', 'Banff is 130km (90 mins) west of Calgary on the Trans-Canada Highway', 'Rent a car at YYC — essential for the entire trip', 'No commercial flights to Banff — Calgary is the gateway'] },
    { title: '🏨 Where to Stay', items: ['Banff Town: Fairmont Banff Springs (splurge), Moose Hotel & Suites (midrange), HI Banff (budget)', 'Book months ahead for July — this is absolute peak season', 'Canmore (20 mins east) is a great alternative — cheaper, less touristy, excellent restaurants', 'Airbnb/VRBO options are limited inside the park but plentiful in Canmore'] },
    { title: '🌡️ Weather', items: ['July averages 15-25°C (59-77°F) in valleys, 0-10°C at glaciers and summits', 'Afternoon thunderstorms are common — pack a rain shell', 'UV is intense at altitude — wear sunscreen and a hat', 'Evenings cool down quickly — always carry a warm layer'] },
    { title: '💳 Money', items: ['Canadian dollars (CAD). $1 USD ≈ $1.36 CAD', 'Canada is nearly cashless — tap-to-pay works everywhere, even trailhead parking', 'Tipping: 15-20% at restaurants, standard in Canada', 'National park passes: buy at the gate or online at pc.gc.ca'] },
    { title: '📱 Connectivity', items: ['Cell coverage is good in Banff and Lake Louise, spotty on the Icefields Parkway', 'Download offline maps (Google Maps or maps.me) before heading north', 'Most hotels and cafés have WiFi', 'Parks Canada app is useful for trail conditions and closures'] }
  ]
};

fulfillOrder(order, itineraryData);
