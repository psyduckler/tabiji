const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771870935819_8l5h2k',
  email: 'kissin.pat@gmail.com',
  destination: 'Yellowstone National Park, WY, USA',
  start_date: '2026-03-21',
  end_date: '2026-03-28',
  group_size: '3-4',
};

const itineraryData = {
  destination: 'Yellowstone National Park, WY, USA',
  countryEmoji: '🇺🇸',
  title: 'Yellowstone in Late March: Wolves, Steam & Winter\'s Last Magic',
  subtitle: '8 days of elk bugling, wolf sightings, steaming hot springs, and crowd-free geysers in the world\'s first national park — before the summer masses arrive',
  description: 'Late March at Yellowstone is one of America\'s best-kept travel secrets. While summer tourists endlessly circle jam-packed parking lots, you\'ll have Lamar Valley nearly to yourselves — spotting wolves, bison, and elk against snow-covered peaks in golden morning light. This is the "in-between" season: the interior snowcoach roads have closed but the summer crowds haven\'t arrived, leaving the park\'s accessible northern loop gloriously uncrowded. Mammoth Hot Springs glows with steam and color. The Lamar Valley wolf packs are at their most visible. And every steaming geyser and hot spring looks 10x more dramatic against the cold, snowy landscape. Base yourself in Gardiner, Montana — the only year-round gateway to Yellowstone — and work outward each day into the park. This is Yellowstone as it was meant to be experienced: wild, quiet, and utterly spectacular.',
  duration: '7 nights',
  dates: 'Mar 21 – Mar 28, 2026',
  budget: '$150 – $250 per person/day',
  pace: 'Relaxed-Moderate',
  bestFor: 'Wildlife lovers, Photographers, Small groups, Nature seekers',
  highlights: [
    'Wolf watching at dawn in Lamar Valley — the best in the world',
    'Mammoth Hot Springs terraces glowing with steam in cold air',
    'Bison herds thundering through snow-covered valleys',
    'Soak in the Boiling River natural hot spring (free)',
    'Tower Fall and the Petrified Tree in winter stillness',
    'Elk herds gathered on the Mammoth Hot Springs terraces',
    'Virtually zero crowds — less than 3% of annual visitors come in winter',
    'Guided wolf watching tour with Yellowstone Forever naturalists',
  ],

  essentials: [
    {
      title: '🛬 Getting There',
      text: 'Fly into Bozeman Yellowstone International Airport (BZN) — the closest and most convenient option, about 90 minutes from Gardiner. Alternatively, fly into Jackson Hole (JAC) but note the South Entrance is closed in late March, so you\'d still need to drive 3+ hours around to Gardiner. Rent a 4WD vehicle — road conditions can be icy in late March. From Bozeman, take I-90 east to Livingston, then US-89 south through Paradise Valley straight into Gardiner.'
    },
    {
      title: '⚠️ Late March Road Access',
      text: 'This is critical: in late March, the ONLY roads open to regular vehicles are from the North Entrance (Gardiner, MT) through Mammoth Hot Springs, Tower-Roosevelt, and Lamar Valley to the Northeast Entrance. The West, South, and East Entrances are all closed to vehicles until mid-April or later. Old Faithful, Grand Prismatic Spring, and the Grand Canyon of Yellowstone are NOT accessible by car. The snowcoach season has already ended (~March 15). Plan your trip around Mammoth, Tower, and Lamar — these areas are spectacular and completely worth it.'
    },
    {
      title: '🌡️ March Weather',
      text: 'Expect serious winter conditions. Daytime temps in Mammoth: 30–45°F (0–7°C). Lamar Valley: often colder, 15–35°F (-9–2°C). Nights can drop to -10°F (-23°C) with wind chill. Snow is common — sometimes dramatic storms roll through. Pack serious winter layers: base layers, insulating mid-layer, waterproof outer shell, insulated pants, warm hat, gloves, balaclava, and waterproof winter boots with traction (or YakTrax). This is NOT a casual spring jacket situation.'
    },
    {
      title: '🐺 Wildlife Safety',
      text: 'Yellowstone has grizzly bears, black bears, wolves, bison, moose, and elk. Bears are typically not very active in late March (still in dens or just emerging), but bison and elk are very active and can be dangerous — never approach within 25 yards of bison or 100 yards of wolves and bears. Stay in or near your vehicle while viewing wildlife in Lamar Valley. Bison can appear docile but are unpredictable and have injured many visitors. Let them cross roads on their timeline, not yours.'
    },
    {
      title: '🏨 Where to Stay',
      text: 'Gardiner, MT is your base camp — the only town at the North Entrance, open year-round. Options: Absaroka Lodge (great views of Yellowstone River, ~$120-160/night), Comfort Inn by Yellowstone (solid mid-range), Yellowstone Village Inn. Mammoth Hot Springs Hotel inside the park closes for the season in late February, so you\'ll be staying in Gardiner. Book early — limited options in this tiny town. Alternatively, stay in Livingston, MT (45 min north) for more choices at lower prices.'
    },
    {
      title: '🎿 Gear to Rent / Buy',
      text: 'If you want to snowshoe (highly recommended for Mammoth area trails), rent gear in Gardiner at Park\'s Fly Shop or Yellowstone Association outfitters. Binoculars are absolutely essential for wolf watching — 8x42 or 10x42 recommended. A spotting scope dramatically improves wolf viewing (rent or bring). Hand warmers (disposable) are a life-saver — buy in bulk at Walmart in Bozeman before heading down. Traction devices for boots (YakTrax or Microspikes) are essential on icy boardwalks.'
    }
  ],

  days: [
    // DAY 1 — Arrival in Bozeman/Gardiner + Paradise Valley
    {
      num: 1,
      date: 'Saturday, Mar 21',
      neighborhoods: 'Bozeman · Paradise Valley · Gardiner',
      title: 'Arrival: Bozeman → Paradise Valley → Gardiner',
      description: 'Fly into Bozeman, pick up your 4WD rental, and make the gorgeous drive south through Paradise Valley — one of Montana\'s most scenic corridors — arriving in Gardiner at the doorstep of Yellowstone.',
      timeBlocks: [
        {
          label: 'Morning / Afternoon',
          activities: [
            {
              title: 'Arrive at Bozeman Yellowstone International Airport (BZN)',
              description: 'Pick up your rental car — request or insist on 4WD/AWD. The roads can be icy in late March. Stock up on snacks, water, hand warmers, and supplies at the Walmart Supercenter in Bozeman before you leave town — Gardiner\'s grocery options are very limited.',
              details: [
                '💡 Walmart Supercenter: 3120 E Valley Center Rd, Bozeman — stock up before leaving',
                '💡 Get a 4WD vehicle — non-negotiable for icy March park roads',
                '⛽ Fill up on gas in Bozeman or Livingston — Gardiner has gas but it\'s pricier'
              ]
            },
            {
              title: 'Scenic Drive: Paradise Valley (US-89 South)',
              description: 'The 53-mile drive south from Livingston to Gardiner through Paradise Valley is jaw-dropping — the Yellowstone River roars alongside the highway while the Absaroka Range towers to the east. Stop at any pullout to stretch your legs and take in the scenery. Wildlife is often visible right from the road here. Welcome to Big Sky country.',
              details: [
                '📍 Livingston, MT → US-89 South → Gardiner (~53 miles, ~1 hour)',
                '💡 Stop at the Yellowstone River Trout Hatchery overlook near Pine Creek',
                '👀 Watch for bighorn sheep on rocky hillsides near Yankee Jim Canyon'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Murray Bar (Livingston)',
              description: 'A classic Montana saloon in downtown Livingston — burgers, cold beers, and serious Western character. Grab a late lunch here before the final leg to Gardiner. The elk burger is excellent and Livingston has way more options than tiny Gardiner.',
              meta: '📍 201 W Park St, Livingston, MT · 💰 $12-18/person · 🍺 Montana craft beers on tap'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Livingston is a surprisingly cool little town — check out the Murray Hotel where Sam Peckinpah used to drink, and Dan Bailey\'s Fly Shop if you\'re into that. But don\'t dawdle — you want to arrive in Gardiner before dark.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Check In & Explore Gardiner',
              description: 'Check into your Gardiner lodging and take a short walk to see the Roosevelt Arch — the historic entrance arch built in 1903 that President Theodore Roosevelt himself laid the cornerstone for. It\'s lit up at night and makes for a great first photo. The Yellowstone River roars right through the middle of town.',
              details: [
                '📍 Roosevelt Arch: North Entrance to Yellowstone, Gardiner',
                '💡 Park entrance is free if you\'re just seeing the arch — it\'s right at the gate',
                '💡 Pick up your America the Beautiful annual pass ($80) here to save money — covers all 7 days'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Wonderland Cafe & Lodge',
              description: 'Gardiner\'s best farm-to-table restaurant and the obvious choice for your first night. Chef-inspired cuisine with locally sourced Montana ingredients — bison dishes, fresh walleye, seasonal soups. Cozy atmosphere with a wood-burning fireplace, local art on the walls, and craft cocktails. The huckleberry scones alone are worth the trip.',
              meta: '📍 206 Main St, Gardiner · ⏰ Dinner 4:30-9pm · 💰 $20-35/person · 🔥 Reserve ahead — popular in the off-season'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Plan for an early wake-up tomorrow — wolf watching in Lamar Valley means pre-dawn starts. Set that alarm for 5:30am and prepare your cold weather gear tonight.' }
          ]
        }
      ],
      mapPins: [
        { lat: 45.7775, lng: -108.5007, label: 'Bozeman Airport (BZN)', num: 1, cat: 'transport', desc: 'Fly in here — closest airport to Yellowstone North Entrance' },
        { lat: 45.6613, lng: -110.5611, label: 'Livingston, MT', num: 2, cat: 'waypoint', desc: 'Stop for lunch and supplies before heading to Gardiner' },
        { lat: 45.0310, lng: -110.7038, label: 'Roosevelt Arch — North Entrance', num: 3, cat: 'attraction', desc: 'Historic 1903 entrance arch — iconic first photo op' },
        { lat: 45.0306, lng: -110.7059, label: 'Wonderland Cafe & Lodge', num: 4, cat: 'restaurant', desc: 'Gardiner\'s best farm-to-table dinner — fireplace and bison dishes' }
      ]
    },

    // DAY 2 — Lamar Valley Wolf Watch
    {
      num: 2,
      date: 'Sunday, Mar 22',
      neighborhoods: 'Lamar Valley · Tower-Roosevelt · Yellowstone River',
      title: 'Dawn Wolf Watch in Lamar Valley',
      description: 'The crown jewel of winter Yellowstone — an early morning wolf watch in Lamar Valley with one of the world\'s highest concentrations of wild wolves. Then explore Tower Fall and the Petrified Tree in the afternoon.',
      timeBlocks: [
        {
          label: 'Pre-Dawn / Morning',
          activities: [
            {
              title: 'Lamar Valley Wolf Watch at Sunrise 🐺',
              description: 'This is the reason to visit Yellowstone in late March. Lamar Valley is arguably the best place on Earth to see wild wolves in their natural habitat. Multiple packs roam this valley — in late winter, they\'re concentrated in the valley bottom and frequently visible from the road. Drive east from Gardiner through Mammoth, past Tower-Roosevelt, and into the Lamar Valley. Pull over at any widened shoulder when you see scopes set up — those are the wolf watchers, and they\'ll know exactly where the packs are. Dawn and dusk are the magic windows.',
              details: [
                '📍 Lamar Valley, Yellowstone NE — Slough Creek, Lamar River corridor',
                '⏰ Leave Gardiner by 6am to reach Lamar Valley by sunrise (~7:15am in late March)',
                '🔭 Bring binoculars — a spotting scope is even better. Wolves are often across the valley',
                '💡 Join the Yellowstone Forever "Wildlife in Winter" guided watch ($75-120) — guides know the pack locations',
                '💡 Look for coyotes and ravens first — where they congregate means a wolf kill nearby',
                '🚗 Drive slowly through the valley, stop often, and scan the hills with binoculars'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pack Your Own',
              description: 'There are NO services open in Lamar Valley in late March. Pack a thermos of hot coffee, hot chocolate, and a hearty breakfast from your cooler or Gardiner the night before. You do NOT want to be hungry and cold at 7am with no food options.',
              meta: '💡 Pick up bakery items from Wonderland Cafe the night before · 🥤 Thermos is essential'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The pull-off at Slough Creek is where wolf watchers often gather. Look for the scopes — these are experienced wolf watchers who have been there for hours and know the pack positions. They\'re almost always happy to let you look through their scope and will tell you where to look.' },
            { type: 'tip', text: '🐺 Wolves tend to be most active in the morning (right after first light) and evening (hour before dark). Midday is less productive. Plan your time accordingly.' }
          ]
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Tower Fall',
              description: 'After wolf watching, drive back west through the valley and stop at Tower Fall — a spectacular 132-foot waterfall partially frozen in the canyon walls. The overlook provides a beautiful view of the plunge pool far below with steam rising from the Yellowstone River. In late March it\'s often partially iced over, which makes it even more dramatic.',
              details: [
                '📍 Tower Fall Trailhead, Tower-Roosevelt Junction',
                '💡 The viewing platform trail (0.25 miles) is accessible but can be icy — use traction devices',
                '📷 Golden light on the canyon walls in late afternoon is spectacular'
              ]
            },
            {
              title: 'Petrified Tree',
              description: 'A short drive from Tower-Roosevelt is one of Yellowstone\'s most unusual features — a 50-million-year-old redwood tree petrified in place, still standing upright. It\'s fenced off to protect it and the whole area is empty in late March. A quick, fascinating stop that most visitors walk right past.',
              details: [
                '📍 Roosevelt Lodge, Tower-Roosevelt area (short paved path)',
                '⏰ 5-minute detour from Tower Fall — worth it',
                '💡 The surrounding landscape of rolling hills and elk is beautiful even to get here'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Picnic at Lamar Valley Overlook',
              description: 'Pack a proper lunch — sandwiches, hot soup in a thermos, snacks. There are no services or restaurants open in the park interior in late March. Find a pullout in Lamar Valley, bundle up in your winter gear, and eat while watching for bison and birds. This is the wildest picnic you\'ll ever have.',
              meta: '💡 Prep lunch in Gardiner the morning before · 🦬 Bison may wander past while you eat'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Bison Watch in Lamar Valley',
              description: 'Return to Lamar Valley as the light turns golden. Bison herds are massive in late March — sometimes thousands of them. They\'ll be moving, grazing, and occasionally sparring in the low golden light. The valley turns amber and pink as the sun sets behind the western ridgeline. This is some of the best wildlife photography in North America.',
              details: [
                '📍 Any pull-out in Lamar Valley',
                '⏰ Arrive 1 hour before sunset (~6:30pm in late March)',
                '📷 Set up facing east for the best light on the bison'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Iron Horse Bar & Grill',
              description: 'Back in Gardiner, the Iron Horse Bar & Grill sits right on the Yellowstone River with Montana\'s best outdoor-dining view (weather permitting). Western comfort food — bison burgers, elk nachos, bison meatloaf, fresh salmon. A full bar with local craft beers and a mulberry margarita that\'s become a Gardiner institution.',
              meta: '📍 212 Spring St, Gardiner · ⏰ Open from 12pm (call to confirm winter hours) · 💰 $16-28/person'
            }
          ],
          tips: [
            { type: 'reddit', text: 'I\'ve been to Yellowstone 8 times and the best experience was always a winter/early spring Lamar Valley wolf watch at dawn. The wolves were maybe 300 yards away and I watched them for 2 hours. Zero other tourists.', cite: 'r/Yellowstone' }
          ]
        }
      ],
      mapPins: [
        { lat: 44.9035, lng: -110.2397, label: 'Lamar Valley — Wolf Watch Pullouts', num: 1, cat: 'attraction', desc: 'Best wolf watching on Earth — scan hillsides with binoculars at dawn' },
        { lat: 44.8951, lng: -110.3736, label: 'Slough Creek Area', num: 2, cat: 'attraction', desc: 'Prime wolf watching spot — look for spotting scopes set up here' },
        { lat: 44.8915, lng: -110.4051, label: 'Tower Fall', num: 3, cat: 'attraction', desc: '132-foot waterfall, often partially frozen in March' },
        { lat: 44.9033, lng: -110.3984, label: 'Petrified Tree', num: 4, cat: 'attraction', desc: '50 million year old petrified redwood, still standing upright' },
        { lat: 45.0306, lng: -110.7059, label: 'Iron Horse Bar & Grill', num: 5, cat: 'restaurant', desc: 'Riverside dinner — bison burgers and Montana craft beers' }
      ]
    },

    // DAY 3 — Mammoth Hot Springs
    {
      num: 3,
      date: 'Monday, Mar 23',
      neighborhoods: 'Mammoth Hot Springs · Albright Visitor Center · Boiling River',
      title: 'Mammoth Hot Springs & the Boiling River',
      description: 'Explore the otherworldly calcium carbonate terraces of Mammoth Hot Springs — one of Yellowstone\'s year-round jewels — then soak in the magical Boiling River natural hot spring where a geothermal tributary meets the icy Gardner River.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Mammoth Hot Springs Terraces 🌋',
              description: 'The Mammoth Hot Springs terraces are among the most alien landscapes in North America — thousands of years of mineral-rich geothermal water have built towering calcium carbonate formations, cascading terraces, and vivid orange and yellow bacterial mats. In winter cold, the steam rising off the active terraces is intense and beautiful. Walk the Upper and Lower Terrace boardwalks — both are generally accessible in late March (wear traction devices for icy spots).',
              details: [
                '📍 Mammoth Hot Springs, northern Yellowstone',
                '⏰ Open year-round — arrive early for soft morning light and fewer people',
                '🦶 Wear traction devices — boardwalks can be icy',
                '💡 Liberty Cap (the conical 37-foot dormant hot spring cone) is the first thing you\'ll see',
                '💡 Palette Springs and Canary Spring are the most colorful active terraces — check which are flowing',
                '📷 Steam rises most dramatically on cold mornings — shoot early for misty terrace photos'
              ]
            },
            {
              title: 'Albright Visitor Center',
              description: 'Right at Mammoth, the Albright Visitor Center is open year-round and has excellent exhibits on Yellowstone\'s geology, wildlife, and history. The staff and rangers here are knowledgeable and will give you the day\'s wildlife report — ask specifically about wolf and bear activity. There\'s a great bookstore for maps and nature guides.',
              details: [
                '📍 Albright Visitor Center, Mammoth Hot Springs',
                '⏰ Open daily 9am-5pm (reduced winter hours — call to confirm)',
                '💡 Ask rangers for the current wolf pack locations — they track them daily'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast / Coffee',
              name: 'Yellowstone Grill (Gardiner)',
              description: 'Early breakfast before heading into the park. Yellowstone Grill on Scott Street is a Gardiner institution — big portions, homemade biscuits, and the best breakfast in town. Popular with park rangers and wolf watchers. Early opening makes it perfect for a pre-dawn fueling stop.',
              meta: '📍 404 Scott St, Gardiner · ⏰ Opens early (check winter hours) · 💰 $10-16/person'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The elk herd at Mammoth is legendary. In late March, dozens (sometimes hundreds) of elk literally walk through the townsite at Mammoth. They are NOT afraid of people — you can be 30 feet from a huge bull elk. This is one of the most surreal wildlife encounters in the park.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Boiling River Natural Hot Spring 🌡️',
              description: 'One of the most unique and free experiences in all of Yellowstone — a natural hot spring where a thermal geothermal tributary flows into the icy Gardner River, creating a stretch of warm-to-hot water you can actually soak in. The contrast of the cold air and snowy banks against the warm water is magical. This is a 0.5-mile walk from the parking area on the road between Gardiner and Mammoth.',
              details: [
                '📍 Boiling River Trailhead, 2.5 miles south of Gardiner on North Entrance Rd',
                '⏰ Dawn to dusk only (no nighttime soaking)',
                '⚠️ Check current status before going — it occasionally closes for high water conditions or maintenance. Call the Mammoth Visitor Center.',
                '💡 Wear your swimsuit under your clothes for an easy change',
                '💡 Water temp varies — find your spot where hot spring water mixes with cold river',
                '🧻 There are no changing rooms — change in your car. Bring a dry towel and dry clothes.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Pack a Trail Lunch',
              description: 'No services between Gardiner and Mammoth Hot Springs except at Mammoth itself (which has limited winter hours). Pack lunch from Gardiner — sandwiches, hot soup in a thermos, and snacks. Eat at the Mammoth terraces or after your Boiling River soak.',
              meta: '💡 Pick up supplies at Food Farm in Gardiner (small but has basics)'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 The Boiling River is technically at the Montana-Wyoming border. Soaking in a geothermal hot spring in Yellowstone with snow on the ground and elk potentially wandering by is as surreal and wonderful as it sounds.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Mammoth Elk Herd at Dusk',
              description: 'Return to Mammoth just before sunset — the elk herd that lives here year-round comes out of the surrounding hills to graze on the lawn of the historic Mammoth townsite. It\'s completely surreal to watch 50+ elk casually graze around old government buildings while steam rises from the terraces in the background. Stay until dark.',
              details: [
                '📍 Mammoth Hot Springs townsite (historic cavalry fort)',
                '⏰ 1 hour before sunset for best light',
                '📷 Shoot the elk with the terraces steaming in the background'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Corral',
              description: 'Gardiner\'s legendary burger joint since 1961. Winner of "Best Elk Burger in Montana" from USA Today. They grind their bison and elk burgers fresh daily from locally raised animals. Hand-cut fries, incredible huckleberry milkshakes, casual outdoor patio (heated in winter). Budget-friendly and beloved.',
              meta: '📍 711 Scott St W, Gardiner · ⏰ Open 12pm-9pm (call to confirm winter hours) · 💰 $8-17/person · 🦌 The elk burger is mandatory'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 44.9769, lng: -110.7007, label: 'Mammoth Hot Springs Terraces', num: 1, cat: 'attraction', desc: 'Otherworldly calcium carbonate terraces — most dramatic in cold steam' },
        { lat: 44.9767, lng: -110.6997, label: 'Liberty Cap', num: 2, cat: 'attraction', desc: '37-foot dormant hot spring cone — first thing you see at Mammoth' },
        { lat: 44.9789, lng: -110.6985, label: 'Albright Visitor Center', num: 3, cat: 'attraction', desc: 'Get daily wolf pack locations from rangers — open year-round' },
        { lat: 45.0107, lng: -110.7031, label: 'Boiling River', num: 4, cat: 'activity', desc: 'Free natural hot spring soak — geothermal meets icy Gardner River' },
        { lat: 45.0260, lng: -110.7034, label: 'The Corral', num: 5, cat: 'restaurant', desc: 'Best elk burgers in Montana since 1961 — huckleberry milkshake required' }
      ]
    },

    // DAY 4 — Guided Wolf Watch Tour
    {
      num: 4,
      date: 'Tuesday, Mar 24',
      neighborhoods: 'Lamar Valley · Little America · Yellowstone River Picnic Area',
      title: 'Professional Wolf Watch & Winter Wildlife Photography',
      description: 'Book a professional guided wolf watching tour with Yellowstone Forever naturalists for the best chance at close wolf encounters. Then explore the vast wildlife-rich landscape of the northern range in the afternoon.',
      timeBlocks: [
        {
          label: 'Pre-Dawn / Full Day',
          activities: [
            {
              title: 'Yellowstone Forever Guided Wildlife Safari 🐺',
              description: 'Yellowstone Forever (the official nonprofit partner of Yellowstone NP) runs professional wolf watching tours led by certified naturalists who know exactly which packs are active and where. In late winter, the Lamar Canyon pack, Junction Butte pack, and other packs are almost always visible to those who know where to look. Guides have spotting scopes, radios, and inside knowledge from the research teams. This is the single best investment you can make for your Yellowstone trip.',
              details: [
                '📍 Departs from Yellowstone Forever Headquarters, Gardiner',
                '💰 Approx $75-120/person for a half-day tour · Group rates available',
                '⏰ Typically depart at dawn (~6-6:30am) and last 4-6 hours',
                '📞 Book at yellowstone.org/programs — reserve 2-4 weeks in advance',
                '💡 Tell them your group size and they\'ll customize accordingly',
                '🔭 Guides bring 80mm spotting scopes — you\'ll see wolves you\'d never find alone',
                '💡 Ask specifically about the Junction Butte pack — largest in the park, often 20+ animals'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Early Breakfast',
              name: 'Pack from Gardiner',
              description: 'You\'ll be leaving before most restaurants open. Prep a thermos of hot coffee and breakfast items the night before. Your guide will likely have a coffee/snack break planned — bring extra snacks for the cold.',
              meta: '💡 Stop at Park\'s Fly Shop or the gas station the night before for a morning coffee setup'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Went in February with Yellowstone Forever guides and saw 14 wolves including pups from the Junction Butte pack. The guides set up scopes right at the side of the road in Lamar Valley. Best $100 I\'ve ever spent. They also spotted 3 grizzlies just waking up from hibernation.', cite: 'r/nationalparks' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yellowstone River Picnic Area & Little America',
              description: 'After your morning guide tour, spend the afternoon exploring the "Little America" flat between Tower-Roosevelt and Lamar Valley — a wide open basin where wolf packs frequently rest midday after a kill. The Yellowstone River Picnic Area (open year-round) is a beautiful spot for lunch with dramatic river canyon views. Look for golden eagles, osprey (sometimes), and coyotes working the riverside terrain.',
              details: [
                '📍 Yellowstone River Picnic Area: between Mammoth and Tower on North Entrance Road',
                '💡 Scan cliffs above the river for bighorn sheep — this is prime bighorn territory in March',
                '👀 Look for golden eagles riding thermals over the canyon walls'
              ]
            },
            {
              title: 'Lamar Buffalo Ranch Historic Site',
              description: 'The Lamar Buffalo Ranch is where Yellowstone\'s bison herd was saved from extinction in the early 1900s — they were brought back from a population of just 23 animals. Now over 5,000 bison roam the park. The historic cabins here are open year-round and are often used by Yellowstone Forever for educational programs. A humble but significant place.',
              details: [
                '📍 Lamar Buffalo Ranch, Lamar Valley',
                '💡 Stop here to learn the bison conservation story — it\'s one of America\'s great conservation victories'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Packed Lunch in Lamar Valley',
              description: 'Eat your packed lunch at a pullout in Lamar Valley after the guided tour. Look for wildlife while you eat — this is entirely normal here. Bison may walk by within 50 feet. Don\'t leave food out — ravens will steal it instantly.',
              meta: '🦅 Ravens are alarmingly bold and will grab unattended food'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dusk Return Drive Through Lamar Valley',
              description: 'The light in Lamar Valley as the sun drops behind the western ridge is magical — the snowy hillsides turn orange and pink, the steam from the Yellowstone River glows. Drive slowly back through the valley one more time, watching for the evening wolf activity. This late-March evening light is a photographer\'s dream.',
              details: [
                '⏰ Sunset around 7:30pm in late March',
                '📷 Use a long lens if you have one — the light on wolves and bison is spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Wonderland Cafe & Lodge',
              description: 'Back to Gardiner\'s best. The rotating seasonal menu often features game meats and local Montana produce. Ask about the daily specials — often features local elk or bison in late winter. The craft cocktails and Montana beer selection make it a perfect wind-down after a full day in the cold.',
              meta: '📍 206 Main St, Gardiner · 💰 $20-35/person · 🔥 Reserve: (406) 223-1914'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 45.0278, lng: -110.7024, label: 'Yellowstone Forever HQ (Gardiner)', num: 1, cat: 'activity', desc: 'Book guided wolf tours here — official park partner with naturalist guides' },
        { lat: 44.9035, lng: -110.2397, label: 'Lamar Valley — Full Valley Drive', num: 2, cat: 'attraction', desc: 'Wolf, bison, elk, coyote and eagle country — scan constantly' },
        { lat: 44.8969, lng: -110.2143, label: 'Lamar Buffalo Ranch', num: 3, cat: 'attraction', desc: 'Historic site where Yellowstone bison were saved from extinction' },
        { lat: 44.9401, lng: -110.4567, label: 'Yellowstone River Picnic Area', num: 4, cat: 'activity', desc: 'Picnic lunch with river canyon views — bighorn sheep on cliffs' },
        { lat: 44.9239, lng: -110.3799, label: 'Little America Flats', num: 5, cat: 'attraction', desc: 'Open basin where wolf packs rest midday — scan with binoculars' }
      ]
    },

    // DAY 5 — Norris & Interior (if accessible) / Cooke City
    {
      num: 5,
      date: 'Wednesday, Mar 25',
      neighborhoods: 'Cooke City · Soda Butte Valley · Northeast Entrance',
      title: 'Northeast Corridor: Cooke City & Soda Butte Valley',
      description: 'Explore the dramatic corridor east of Lamar Valley toward Cooke City — the Soda Butte Valley is one of the most wildlife-rich stretches in the park, home to pronghorn, elk, and sometimes wolves. Cooke City is a tiny mountain town with serious character.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Soda Butte Valley Wildlife Drive',
              description: 'Drive east from Lamar Valley through the Soda Butte Valley — a beautiful glacially-carved corridor flanked by the Beartooth Mountains. The Soda Butte Creek runs through meadows where pronghorn, elk, and sometimes wolves hunt. Stop at the Soda Butte thermal feature — a small cone of calcium carbonate formed by a former hot spring, now dormant but historically significant.',
              details: [
                '📍 Northeast entrance road, east of Lamar Valley',
                '👀 Watch for pronghorn in the meadows — they stay in the valley through winter',
                '💡 The Soda Butte cone is right next to the road — easy stop',
                '⚠️ Roads can be very icy in this section in late March — drive carefully'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast / Coffee',
              name: 'Range Rider Motel Café (Cooke City) or Pack Your Own',
              description: 'Cooke City is tiny (population ~100) but has a few diners and cafés that are open in winter, serving basic hearty mountain food to snowmobilers and locals. A cup of hot coffee and a breakfast plate before exploring the Soda Butte Valley.',
              meta: '📍 Cooke City, MT — call ahead to confirm winter hours as some places have limited schedules'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Cooke City and Silver Gate are at the dead end of the Beartooth Highway — the road east (toward Red Lodge) is closed until May/June due to snow. But the NE Entrance road from the park into town IS open year-round for vehicles.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cooke City Exploration',
              description: 'Cooke City is one of those remote mountain towns that\'s charmingly stuck in time — a handful of buildings, a few shops, snowmobiles everywhere in winter. It\'s accessed primarily by snowmobile in winter and has a surprisingly feisty little community. Browse the small shops, grab a beer at the local bar, and chat with the permanent residents who "stay in all winter." Very different from any tourist town you\'ve seen.',
              details: [
                '📍 Cooke City, MT — end of the road until Beartooth Hwy opens',
                '💡 The Miner\'s Saloon is the local gathering spot — warm, friendly, and full of character',
                '💡 Check out the Cooke City Store for souvenirs and local snacks'
              ]
            },
            {
              title: 'Drive Back: Late Afternoon Lamar Valley',
              description: 'Head back west through Soda Butte Valley and Lamar Valley in the late afternoon. The golden light is at its best in this 3-4pm window. Stop at every pullout. This is your fourth day in the area and you\'re now getting to know the terrain intimately — you\'ll notice things you missed before.',
              details: [
                '⏰ Leave Cooke City by 3pm to catch the golden afternoon light in Lamar Valley',
                '💡 By now you know the good pullouts — use them'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Packed Lunch in Soda Butte Valley',
              description: 'Eat at one of the pull-outs in the Soda Butte Valley. Look for wolf tracks in the snow along the creek bank — this area is frequently traveled by wolves between Lamar Valley and the Absaroka Range.',
              meta: '🐾 Scan riverbanks and snow-covered meadows for wolf and coyote tracks'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at the Roosevelt Arch',
              description: 'The Roosevelt Arch at the North Entrance to Yellowstone is beautiful at sunset. Walk through the arch into the park and look south — the Yellowstone River canyon and the snow-covered peaks are beautiful in evening light. This is one of those quiet moments where you realize you\'ve been in one of the world\'s great wilderness areas for several days.',
              details: [
                '📍 Roosevelt Arch, North Entrance to Yellowstone, Gardiner',
                '📷 The arch frames perfectly against the canyon and peaks to the south'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Iron Horse Bar & Grill',
              description: 'Riverside dinner on the Yellowstone River. Try the bison meatloaf tonight if you haven\'t — it\'s the best thing on the menu and deeply Montana. A whiskey flight from Montana distilleries is a worthy evening sipper after a full day in the cold.',
              meta: '📍 212 Spring St, Gardiner · 💰 $16-28/person · 🥃 Ask about the Montana whiskey selection'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 44.8896, lng: -110.0940, label: 'Soda Butte Thermal Feature', num: 1, cat: 'attraction', desc: 'Dormant hot spring cone in the Soda Butte Valley — historic geothermal remnant' },
        { lat: 45.0167, lng: -109.9285, label: 'Cooke City, MT', num: 2, cat: 'waypoint', desc: 'Remote mountain town at the end of the Beartooth Highway — snowmobiles and locals' },
        { lat: 44.8969, lng: -110.0830, label: 'Soda Butte Valley Meadows', num: 3, cat: 'attraction', desc: 'Pronghorn and elk in valley meadows — scan for wolf tracks on riverbanks' },
        { lat: 44.9035, lng: -110.2397, label: 'Lamar Valley Late Afternoon', num: 4, cat: 'attraction', desc: 'Golden hour light on bison and snowy peaks — the money shot' },
        { lat: 45.0310, lng: -110.7038, label: 'Roosevelt Arch (Sunset)', num: 5, cat: 'attraction', desc: 'Historic entrance arch at sunset — beautiful framing of the canyon behind' }
      ]
    },

    // DAY 6 — Paradise Valley Day Trip
    {
      num: 6,
      date: 'Thursday, Mar 26',
      neighborhoods: 'Paradise Valley · Livingston · Chico Hot Springs',
      title: 'Chico Hot Springs & Paradise Valley',
      description: 'Take a day trip out of Yellowstone country and explore Montana\'s stunning Paradise Valley — soak in the historic Chico Hot Springs resort, explore the Yellowstone River corridor, and visit charming Livingston.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive: Paradise Valley Morning',
              description: 'The 53-mile corridor between Gardiner and Livingston along the Yellowstone River is called Paradise Valley for good reason. In late March, the river runs high and fast from snowmelt, bighorn sheep cling to roadside cliffs, and bald eagles perch in cottonwoods along the riverbank. Drive slowly north, stopping at pullouts.',
              details: [
                '📍 US-89 North from Gardiner to Livingston',
                '👀 Bighorn sheep on rocky cliffs near Yankee Jim Canyon — early morning is best',
                '🦅 Bald eagles perch in cottonwoods along the Yellowstone River — look for white heads'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Chico Hot Springs Resort Dining Room',
              description: 'Chico Hot Springs has a charming dining room that serves breakfast and is open to day visitors. Great food in a beautiful old resort setting. Worth arriving for a hot breakfast before your soak. The French toast and eggs Benedict are both excellent.',
              meta: '📍 163 Chico Rd, Pray, MT (25 miles north of Gardiner) · 💰 $12-18/person · ⏰ Breakfast hours — call ahead'
            }
          ],
          tips: []
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Chico Hot Springs 🛁',
              description: 'Chico Hot Springs is one of Montana\'s most beloved institutions — a historic resort that\'s been operating since 1900, with natural geothermal hot spring pools open to day visitors. Two outdoor pools (main pool ~96°F, soaking pool ~104°F) surrounded by snowy mountains. The setting is spectacular in late March — steam rising off the pools against snow-covered Absaroka peaks. This is different from the Boiling River — this is a developed resort but the hot springs are completely authentic.',
              details: [
                '📍 163 Chico Rd, Pray, MT',
                '💰 Day pass for pools: ~$10-15/person (very reasonable)',
                '⏰ Pools open daily (check current hours)',
                '💡 Weekday visits are quieter — this is a local favorite, busier on weekends',
                '💡 Rent a room for a few hours if the group wants a nicer changing area',
                '🏊 Bring swimsuits and a dry bag for your valuables'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Poolside Snacks or Chico Saloon',
              description: 'The Chico Saloon next to the pools serves food and cold Montana beers. Perfect post-soak lunch — burgers, sandwiches, and local brews while the steam rises from the pools 20 feet away. Classic Montana afternoon.',
              meta: '📍 Chico Hot Springs Saloon · 💰 $12-18/person · 🍺 Cold Montana beers and good burgers'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Chico Hot Springs is an absolute must for anyone in the Yellowstone/Paradise Valley area. Day pass for the pools is cheap and the setting (Montana mountains, geothermal water) is incredible. Go on a weekday.', cite: 'r/Montana' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Livingston Downtown Exploration',
              description: 'Livingston, MT is a refreshingly cool small city with a real art scene, fly fishing culture, and the best restaurant options near Yellowstone. The historic downtown on Park Street is lined with galleries, bookstores, and bars. This is where wealthy ranchers and artists meet working cowboys — the mix is fascinating. Browse the galleries and stop for a drink at the legendary Murray Bar.',
              details: [
                '📍 Downtown Livingston, MT · ~45 min north of Gardiner',
                '💡 The Murray Bar in the Murray Hotel has serious history — it\'s been going since the 1900s',
                '🎨 Browse the galleries on Park Street — there\'s a surprisingly vibrant Montana arts scene here'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gil\'s Goods or 2nd Street Bistro',
              description: 'Livingston has significantly better dining than tiny Gardiner. 2nd Street Bistro is the best restaurant in town — seasonal contemporary cuisine in a cozy setting. Gil\'s Goods is a more casual gastropub with excellent craft beers and a fun Montana menu. Either is a major upgrade from Gardiner dining and worth the 45-minute drive.',
              meta: '📍 2nd Street Bistro: 123 N 2nd St, Livingston · 💰 $20-35/person · 💡 Reserve on weeknights in winter'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Livingston is 45 minutes from Gardiner but the extra drive is worth it for a special dinner. The road back at night is beautiful — watch for deer and elk on US-89.' }
          ]
        }
      ],
      mapPins: [
        { lat: 45.2789, lng: -110.6812, label: 'Yankee Jim Canyon', num: 1, cat: 'attraction', desc: 'Dramatic river canyon with bighorn sheep on the cliffs' },
        { lat: 45.3502, lng: -110.6785, label: 'Chico Hot Springs Resort', num: 2, cat: 'activity', desc: 'Historic hot springs resort — day pass pools against mountain backdrop' },
        { lat: 45.6613, lng: -110.5611, label: 'Downtown Livingston', num: 3, cat: 'waypoint', desc: 'Arts, galleries, Murray Bar — the coolest town near Yellowstone' },
        { lat: 45.6618, lng: -110.5586, label: '2nd Street Bistro', num: 4, cat: 'restaurant', desc: 'Best restaurant near Yellowstone — seasonal contemporary cuisine' },
        { lat: 45.6571, lng: -110.5538, label: 'Murray Bar', num: 5, cat: 'nightlife', desc: 'Historic Montana saloon in the Murray Hotel — cold beers and history' }
      ]
    },

    // DAY 7 — Final Lamar Valley Dawn + Mammoth Snowshoeing
    {
      num: 7,
      date: 'Friday, Mar 27',
      neighborhoods: 'Lamar Valley · Mammoth · Tower Area',
      title: 'Last Dawn in Lamar & Mammoth Snowshoe',
      description: 'One final pre-dawn wolf watch in Lamar Valley, then snowshoe the Mammoth Hot Springs Upper Terrace Loop for a completely different perspective on the park\'s most iconic thermal feature.',
      timeBlocks: [
        {
          label: 'Pre-Dawn / Morning',
          activities: [
            {
              title: 'Final Dawn Wolf Watch — Lamar Valley 🐺',
              description: 'This is your last morning in Lamar Valley — make it count. Be in position before sunrise. By now you know the best pullouts and scanning spots. The Junction Butte pack\'s territory overlaps much of the eastern valley, and the Lamar Canyon pack works the western portion. Position yourself and wait. Dawn light on the Yellowstone plateau is something you won\'t forget.',
              details: [
                '⏰ Leave Gardiner by 5:45am for pre-dawn arrival in Lamar Valley',
                '💡 If you didn\'t see wolves earlier in the trip, this is your last chance — be patient',
                '📷 Use the lowest ISO your camera allows in the dark conditions — wolves are often in dim light'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Pre-Dawn Coffee',
              name: 'Thermos from Gardiner',
              description: 'Pack the thermos the night before. No time for restaurants at this hour — you need to be in position before the wolves start moving at first light.',
              meta: '💡 Prep everything the night before — pack the car, set out cold weather gear, fill the thermos'
            }
          ],
          tips: []
        },
        {
          label: 'Midday / Afternoon',
          activities: [
            {
              title: 'Mammoth Upper Terrace Snowshoe Loop 🎿',
              description: 'Rent snowshoes in Gardiner and hike the Upper Terrace Loop above Mammoth Hot Springs — a 1.5-mile loop trail that gets you to viewpoints looking DOWN on the lower terraces, with panoramic views of the Gallatin Range to the north and the park\'s volcanic landscape in every direction. In late March, this trail is usually snow-covered and absolutely beautiful. You might share the trail with a handful of others — maybe no one.',
              details: [
                '📍 Upper Terrace Loop trailhead, Mammoth Hot Springs',
                '📏 1.5 miles round trip, relatively flat',
                '💡 Rent snowshoes at Park\'s Fly Shop in Gardiner (~$20/day)',
                '⚠️ Check with rangers — trail conditions vary. May be icy in spots.',
                '📷 The view from the upper loop looking down on the terraces with steam is one of Yellowstone\'s best photos'
              ]
            },
            {
              title: 'Beaver Ponds Loop Snowshoe',
              description: 'If you have energy left, the Beaver Ponds Loop starts right from the Mammoth townsite and winds through lodgepole forest to a series of beaver ponds with views of the electric peak. In late March, look for beaver activity at the ponds (they\'re active year-round) and watch for moose in the willows.',
              details: [
                '📍 Trailhead near the Mammoth Hot Springs Terraces',
                '📏 5 miles loop, rolling terrain',
                '⏰ Allow 2.5-3 hours · Do this only if you have time after the Upper Terrace'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Yellowstone Grill (Gardiner)',
              description: 'A hot lunch at the Yellowstone Grill back in Gardiner between the wolf watch and the snowshoe. Warm up, refuel, and grab your rental snowshoes before heading back to Mammoth.',
              meta: '📍 404 Scott St, Gardiner · 💰 $10-16/person · ⏰ Good lunch hours'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Hot Spring Soak at Boiling River',
              description: 'One final soak in the Boiling River at dusk. The thermal water glows against the darkening sky, stars start to appear, and you\'ll hear the Gardner River rushing past. If the weather cooperated during your trip, this is the perfect final Yellowstone moment — your feet in geothermal water, snow on the banks, and the Roosevelt Arch just visible upstream.',
              details: [
                '📍 Boiling River Trailhead, 2.5 miles south of Gardiner',
                '⏰ Dawn-to-dusk access only — time it to finish before full dark',
                '🌟 Stars appear early in late March — incredible if you can stay until blue hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Special Group Dinner — Wonderland or Iron Horse',
              description: 'Your last dinner in Yellowstone country. Choose your favorite from the week — Wonderland Cafe for a special farm-to-table splurge, or Iron Horse for that one last bison burger with the Yellowstone River roaring outside. Either way, toast to the wolves you saw, the bison traffic jams, and the steam rising off ancient geothermal vents.',
              meta: '🥂 This trip deserves a proper toast — get a bottle of Montana-made wine or whiskey'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you can, stay out for a sunset hour drive through the north part of Mammoth and toward Tower after dinner — late March skies above Yellowstone are extraordinary, with no light pollution and the silhouettes of elk against the blue dusk.' }
          ]
        }
      ],
      mapPins: [
        { lat: 44.9035, lng: -110.2397, label: 'Lamar Valley — Final Dawn', num: 1, cat: 'attraction', desc: 'Last pre-dawn wolf watch — be in position by sunrise' },
        { lat: 44.9800, lng: -110.7005, label: 'Upper Terrace Loop Trailhead', num: 2, cat: 'activity', desc: 'Snowshoe above the terraces with panoramic park views' },
        { lat: 44.9830, lng: -110.6992, label: 'Beaver Ponds Loop Trailhead', num: 3, cat: 'activity', desc: 'Optional: 5-mile snowshoe through forest to beaver ponds' },
        { lat: 45.0107, lng: -110.7031, label: 'Boiling River — Farewell Soak', num: 4, cat: 'activity', desc: 'Final sunset soak in geothermal spring — stars appear overhead' },
        { lat: 45.0306, lng: -110.7059, label: 'Wonderland Cafe (Farewell Dinner)', num: 5, cat: 'restaurant', desc: 'Final dinner in Yellowstone country — make it special' }
      ]
    },

    // DAY 8 — Departure
    {
      num: 8,
      date: 'Saturday, Mar 28',
      neighborhoods: 'Gardiner · Paradise Valley · Bozeman',
      title: 'Departure: Last Bison Jam & Paradise Valley Drive',
      description: 'One last early morning drive through Mammoth for wildlife, then the scenic Paradise Valley drive back to Bozeman Airport for departure.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Mammoth Drive — Elk Herd Farewell',
              description: 'You don\'t need to rush out. Make one last slow morning drive through Mammoth Hot Springs and say goodbye to the elk herd. They\'ll be there — they always are. Stop at the terraces one more time in the morning light. The steam, the elk, the empty boardwalks. Pack this image away carefully — it\'s worth keeping.',
              details: [
                '📍 Mammoth Hot Springs townsite + terraces',
                '⏰ Early morning — elk are most active in the first hours of daylight',
                '💡 Check out of your Gardiner lodging first and load the car — then do one final drive'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Breakfast',
              name: 'The Corral (Open from noon) or Yellowstone Grill',
              description: 'One last Gardiner breakfast before the drive to Bozeman. The Yellowstone Grill opens early enough for a pre-departure meal. Alternatively, pack breakfast for the road and make the drive a leisurely picnic stop in Paradise Valley.',
              meta: '📍 Yellowstone Grill: 404 Scott St, Gardiner · 💰 $10-16/person'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon / Departure',
          activities: [
            {
              title: 'Paradise Valley Drive to Bozeman',
              description: 'The 90-minute drive from Gardiner to Bozeman takes you back through Paradise Valley — the same road you drove in on, but now you see it differently. You\'ve spent a week in the wilderness and your eyes have been trained to spot wildlife. Scan the cliff faces for bighorn sheep one more time. Watch the Yellowstone River reflect the Absaroka peaks. This is what Montana looks like. Remember it.',
              details: [
                '📍 US-89 North from Gardiner → Livingston → I-90 → Bozeman',
                '⏰ Allow 2 hours including any stops',
                '💡 Stop in Livingston for one last coffee or pie slice if time allows'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch (if time allows)',
              name: 'MAP Brewing (Bozeman)',
              description: 'If you have time before your flight, MAP Brewing in Bozeman has excellent food and outstanding craft beers made in-house. A great final meal with a taste of Bozeman\'s impressive craft beer scene. Look back at your wolf photos over a cold IPA.',
              meta: '📍 510 Manley Rd, Bozeman · 💰 $14-20/person · 🍺 Incredible craft beers — don\'t miss the stout'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Bozeman Airport (BZN) is small but can get busy. Arrive 1.5-2 hours before departure. Return your rental car early if you can — rental centers are a short shuttle from the terminal.' }
          ]
        }
      ],
      mapPins: [
        { lat: 44.9769, lng: -110.7007, label: 'Mammoth Hot Springs — Final Visit', num: 1, cat: 'attraction', desc: 'Say goodbye to the elk herd and the steaming terraces' },
        { lat: 45.0310, lng: -110.7038, label: 'Roosevelt Arch — Last Look', num: 2, cat: 'attraction', desc: 'Last photo at the historic entrance before departing' },
        { lat: 45.2789, lng: -110.6812, label: 'Paradise Valley Scenic Drive', num: 3, cat: 'waypoint', desc: 'One final bighorn sheep scan on the cliff faces' },
        { lat: 45.6613, lng: -110.5611, label: 'Livingston Coffee Stop', num: 4, cat: 'waypoint', desc: 'Optional: last stop in Livingston before Bozeman' },
        { lat: 45.7775, lng: -108.5007, label: 'Bozeman Airport (BZN)', num: 5, cat: 'transport', desc: 'Depart — 1.5-2 hours before flight, small but can be busy' }
      ]
    }
  ],

  practicalInfo: [
    {
      title: '🚗 Getting Around',
      items: [
        'A 4WD/AWD rental car is essential — icy roads are common in late March',
        'Only the North Entrance corridor is open to vehicles: Gardiner → Mammoth → Tower → Lamar Valley → Cooke City',
        'Fill up gas in Gardiner before entering the park — no services inside in late March',
        'Keep traction devices (YakTrax or Microspikes) in the car for boardwalks and trails',
        'Cell service is spotty to non-existent inside the park — download offline Google Maps'
      ]
    },
    {
      title: '⚠️ What\'s Closed in Late March',
      items: [
        'West Entrance and Old Faithful area — closed until ~April 17',
        'South Entrance (from Jackson) — closed until ~May 8',
        'East Entrance (from Cody) — closed until ~May 1',
        'Grand Canyon of Yellowstone — not accessible',
        'Hayden Valley — not accessible by car',
        'Snowcoach season ends ~March 15 — no snowcoach to Old Faithful',
        'Most park lodges and facilities are closed until April/May'
      ]
    },
    {
      title: '🐺 Wildlife Viewing Tips',
      items: [
        'Dawn and dusk are the prime windows for wolf activity',
        'Look for spotting scopes set up at roadside pullouts — wolf watchers know pack locations',
        'Bison have right-of-way on roads — do not honk or rush them',
        'Keep 100 yards distance from wolves and bears, 25 yards from bison and elk',
        'Stay in or near your vehicle when viewing large animals',
        'Ravens circling low often indicates a wolf kill nearby — worth investigating with binoculars'
      ]
    },
    {
      title: '📸 Photography Tips',
      items: [
        'Cold morning air makes thermal features 10x more dramatic — shoot geysers and hot springs early',
        'Dark-coated animals (wolves, bison) contrast beautifully against snow — ideal conditions',
        'Bring extra batteries — cold drains them fast. Keep spares in an inner pocket',
        'A telephoto lens (200-400mm) dramatically improves wildlife shots',
        'Spotting scope + phone adapter = wolf photos from hundreds of yards away',
        'Magic hour in late March is golden — sunset around 7:30pm with long warm light'
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('\n✅ Fulfilled Yellowstone order!');
    console.log('Slug:', result.slug);
    console.log('URL:', result.url);
    console.log('Email sent:', result.emailSent);
  })
  .catch(err => {
    console.error('\n❌ Fulfillment failed:', err.message);
    process.exit(1);
  });
