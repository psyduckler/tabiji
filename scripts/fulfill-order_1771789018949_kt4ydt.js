const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771789018949_kt4ydt',
  email: 'klabianco+testingtravel@gmail.com',
  destination: 'irvine, ca',
  startDate: '2026-02-22',
  endDate: '2026-02-28',
  groupSize: '3-4',
  requests: ''
};

const itineraryData = {
  destination: 'Irvine, CA',
  countryEmoji: '🇺🇸',
  title: 'Orange County\'s Finest: Sun, Sand & Sophistication',
  subtitle: '6 days of coastal hikes, beach towns & world-class dining for 3–4',
  description: "Irvine is Orange County's most livable city — spotlessly clean, endlessly walkable, and surrounded by some of Southern California's most spectacular coastline. This itinerary takes you from the city's giant-wheel Spectrum to tide-pooling at Crystal Cove, art-hopping in Laguna Beach, kayaking in Newport Harbor, and whale-watching in Dana Point. February brings mild weather, whale migration season, and uncrowded beaches — a rare sweet spot before spring break hits.",
  duration: '6 nights',
  dates: 'Feb 22 – Feb 28, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups',
  highlights: [
    'Crystal Cove State Park tide pools and coastal hiking',
    'Laguna Beach art galleries and seaside village charm',
    'Whale watching in Dana Point during peak migration season',
    'Newport Beach Balboa Island ferry and frozen banana tradition',
    'Irvine Spectrum Center — dining, shopping & giant Ferris wheel',
    'Diamond Jamboree Asian food hall deep dive'
  ],

  essentials: [
    { title: '☀️ February Weather', text: 'Expect mild temperatures of 60–68°F (15–20°C) with occasional light rain. Pack a light jacket for evenings and coastal breezes. February is peak gray whale migration — perfect for whale watching at Dana Point.' },
    { title: '🚗 Getting Around', text: 'A car is highly recommended in Orange County. Irvine is well-planned with wide roads and ample parking. Lyft/Uber are readily available. For beach days, weekday visits avoid weekend parking headaches.' },
    { title: '🌊 Beach Tips', text: "February waters are around 58–62°F — too cold for most swimming but perfect for hiking coastal trails, tide pooling, and watching surfers. Crystal Cove and Laguna Beach are best explored at low tide for maximum tide pool access." },
    { title: '🍜 Food Scene', text: 'Irvine has one of the most diverse food scenes in California, with exceptional Asian restaurants at Diamond Jamboree and Irvine Spectrum, plus excellent farm-to-table and coastal California cuisine throughout Orange County.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-22',
      neighborhoods: 'Irvine Spectrum · Great Park · Woodbury',
      title: 'Arrival — Spectrum Vibes & the Great Park',
      description: "Touch down in Orange County and ease into Irvine's California rhythm. The afternoon is for exploring the open-air Irvine Spectrum Center, and sunset over the Great Park's famous tethered balloon gives you your first sweeping view of the region.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Irvine Spectrum Center',
              description: "After settling in, head to Irvine Spectrum Center — an enormous open-air shopping, dining, and entertainment hub. Stroll the palm-lined promenade, ride the 108-foot Giant Wheel for panoramic OC views, and browse the mix of boutiques and restaurants.",
              details: [
                '🎡 Giant Wheel rides are a must for the group — views stretch to the coast on clear days',
                '🛍️ Over 130 shops and 30+ restaurants — great first-night browsing',
                '📍 Free parking structure on-site'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee Stop',
              name: 'Philz Coffee (Irvine Spectrum)',
              description: 'California\'s beloved pour-over coffee chain. The Tesora blend is legendary — great fuel for the afternoon.',
              meta: '💰 $ · 📍 Irvine Spectrum Center'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Great Park Irvine & Tethered Balloon',
              description: "Drive over to Great Park Irvine — a 1,300-acre public park built on a former Marine base. Ride the famous free tethered orange balloon for aerial views of Irvine, the Santa Ana Mountains, and on a clear evening, the Pacific Ocean shimmer.",
              details: [
                '🎈 Balloon rides are FREE — check launch times online (weather dependent)',
                '🌅 Golden hour from the balloon is spectacular',
                '🏞️ The Bosque meadow and farm areas are lovely for a sunset stroll'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cucina Enoteca',
              description: "Cal-Italian cuisine that evokes a coastal farmhouse — house-made pastas, wood-fired dishes, and a stellar wine list. The outdoor patio with fire pits is perfect for a group first-night dinner.",
              meta: '💰 $$$ · 📍 Irvine Spectrum Center · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: "Irvine Spectrum has a fantastic happy hour scene (4–6pm at most restaurants). Grab drinks and apps on one of the patios before dinner — great way to people-watch and soak in the California vibe." }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6508, lng: -117.7401, label: 'Irvine Spectrum Center', num: 1, cat: 'attraction', desc: 'Open-air shopping/dining hub with 108-ft Giant Wheel' },
        { lat: 33.6510, lng: -117.7418, label: 'Giant Wheel', num: 2, cat: 'attraction', desc: 'Panoramic Ferris wheel ride with OC views' },
        { lat: 33.6780, lng: -117.7394, label: 'Great Park Irvine', num: 3, cat: 'attraction', desc: '1,300-acre public park with free tethered balloon rides' },
        { lat: 33.6500, lng: -117.7395, label: 'Cucina Enoteca', num: 4, cat: 'food', desc: 'Cal-Italian dining with fire pit patios' },
        { lat: 33.6510, lng: -117.7406, label: 'Philz Coffee', num: 5, cat: 'food', desc: 'California pour-over coffee institution' }
      ]
    },
    {
      num: 2,
      date: '2026-02-23',
      neighborhoods: 'Newport Beach · Balboa Island · Corona del Mar',
      title: 'Newport Beach — Harbor Life & Balboa Island',
      description: "Newport Beach is Orange County's quintessential beach town — a sparkling harbor packed with yachts, a charming island village, and dramatic cliffs at Corona del Mar. Today you'll do it all: ferry rides, frozen bananas, tidepooling, and a sunset dinner on the bluff.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Balboa Island Ferry & Village',
              description: "Take the tiny three-car Balboa Ferry — one of the most charming ferry rides in California — across to Balboa Island. Stroll Marine Avenue, browse boutique shops, and pick up the famous Balboa Bar (a chocolate-dipped frozen banana) at Dad's Donut & Bakery Shop.",
              details: [
                '⛴️ Balboa Ferry runs continuously — $1–2 per person, cash only',
                '🍌 The frozen Balboa Bar is a 100-year-old OC tradition — don\'t skip it',
                '🏡 Marine Avenue has cute boutiques, coffee shops, and brunch spots',
                '📸 Views of Newport Harbor and the Pavilion are gorgeous from the ferry'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'The Crab Cooker',
              description: 'An OC institution since 1951 — casual, no-frills seafood on the Balboa Peninsula. Fresh clam chowder, fish & chips, and grilled catch of the day.',
              meta: '💰 $$ · 📍 2200 Newport Blvd, Newport Beach'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Corona del Mar State Beach & Tidal Pools',
              description: "Drive south on PCH to Corona del Mar — a small, affluent beach community with some of the most beautiful tidal pools in Orange County. The Little Corona del Mar Beach has outstanding tidal pool exploration during low tide, and the main beach has dramatic bluffs.",
              details: [
                '🐙 Bring water shoes for tide pooling — sea anemones, urchins, and small fish abound',
                '🌊 Check tide charts — low tide reveals the best pools',
                '📸 The bluff above Corona del Mar Main Beach gives classic OC sunset photography'
              ]
            },
            {
              title: 'Ocean Blvd Walk & Inspiration Point',
              description: "Walk along Ocean Blvd above the cliffs at Corona del Mar. Inspiration Point overlook gives sweeping views of the coastline, Catalina Island (on clear days), and the Pacific. The neighborhood\'s gardens and architecture are stunning.",
              details: [
                '🏔️ Catalina Island is often visible on clear February days',
                '🌺 The CDM flower gardens and estates along Ocean Blvd are beautiful',
                '📍 Inspiration Point is at Ocean Blvd & Orchid Ave'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Bandera Restaurant',
              description: "Upscale American comfort cuisine in a warm, lodge-like setting in Newport Beach. The rotisserie chicken and wood-fired dishes are outstanding. A great group dinner spot with a lively bar scene.",
              meta: '💰 $$$ · 📍 3201 E Coast Hwy, Corona del Mar · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: "After dinner, walk down to the CDM beach for the last of the sunset light — the bluff walk back up to the car is a gorgeous way to end the evening." }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6054, lng: -117.8982, label: 'Balboa Island', num: 1, cat: 'attraction', desc: 'Charming harbor island with ferry, boutiques, and Balboa Bars' },
        { lat: 33.6048, lng: -117.9058, label: 'Balboa Ferry', num: 2, cat: 'attraction', desc: 'Three-car ferry across Newport Harbor — $1-2 each' },
        { lat: 33.6059, lng: -117.9247, label: 'The Crab Cooker', num: 3, cat: 'food', desc: 'OC seafood institution since 1951 — clam chowder & fish' },
        { lat: 33.5930, lng: -117.8770, label: 'Little Corona del Mar Beach', num: 4, cat: 'attraction', desc: 'Outstanding tidal pools and rocky cove' },
        { lat: 33.5968, lng: -117.8764, label: 'Inspiration Point', num: 5, cat: 'attraction', desc: 'Ocean Blvd overlook with sweeping coastal views' },
        { lat: 33.5972, lng: -117.8717, label: 'Bandera Restaurant', num: 6, cat: 'food', desc: 'Upscale American comfort dining on PCH' }
      ]
    },
    {
      num: 3,
      date: '2026-02-24',
      neighborhoods: 'Crystal Cove State Park · Laguna Beach Village · Arts District',
      title: 'Crystal Cove, Tide Pools & Laguna Beach',
      description: "One of the best days in Orange County: morning in the magical Crystal Cove State Park for hiking and tide pooling, then an afternoon in Laguna Beach — the artsy beach town where galleries, boutiques, and sea-view terraces line every corner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Crystal Cove State Park — Beach & Tide Pools',
              description: "Crystal Cove is one of California's most stunning state parks — 3.5 miles of undeveloped coastline backed by 2,400 acres of backcountry. The historic cottages and wild beach feel like stepping back to 1930s California. Explore the tide pools, sea caves, and snorkel in the crystal-clear coves.",
              details: [
                '🅿️ Arrive by 8am — lots fill up quickly, even in February',
                '🌊 The tide pools at the south end of the beach are exceptional',
                '🏊 El Moro Cove is sheltered and good for snorkeling in dry suits',
                '📸 The historic cottages are a designated National Historic Landmark'
              ]
            },
            {
              title: 'Moro Canyon Trail Hike',
              description: "For the active members of your group — hike the Moro Canyon Loop Trail (5 miles, moderate). The trail climbs through coastal sage scrub to a ridgeline with 360° views of the ocean and Santa Ana Mountains. Worth every step.",
              details: [
                '🥾 5-mile loop, approximately 2.5 hours, ~900ft elevation gain',
                '🌿 Native wildflowers begin to bloom in late February',
                '👁️ The ocean panorama from the ridgeline is extraordinary'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Crystal Cove Shake Shack',
              description: "Not the burger chain — this 1940s beachside shack is an OC legend. Milkshakes, breakfast burritos, and coffee with your feet in the sand. The ultimate beach morning.",
              meta: '💰 $ · 📍 Crystal Cove State Park historic beach · Cash preferred'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Laguna Beach Village & Heisler Park',
              description: "Drive 10 minutes south on PCH to Laguna Beach — a bohemian coastal art town that's been attracting painters and sculptors since the 1920s. Walk through the village, browse the galleries on PCH, and stroll Heisler Park's cliffside gardens with sweeping ocean views.",
              details: [
                '🎨 Laguna Art Museum is worth a quick visit — strong California plein air collection',
                '🌺 Heisler Park has gorgeous planted gardens above dramatic sea stacks',
                '🛍️ Browse Forest Ave for local art, jewelry, and ceramics',
                '🏖️ Main Beach Laguna has a lifeguard tower and volleyball courts — iconic'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Lunch',
              name: 'Taco Loco',
              description: "A beloved Laguna Beach institution since 1987. Best fish tacos in Orange County, served on a second-floor deck overlooking PCH and the Pacific. Cash only but absolutely worth it.",
              meta: '💰 $ · 📍 640 S Coast Hwy, Laguna Beach · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Thousand Steps Beach',
              description: "Hike down the famous (and very steep) Thousand Steps Beach in South Laguna — actually about 220 steps, but it feels like more. This hidden gem is less crowded, surrounded by cliffs, and offers some of the most stunning sunset colors in the county.",
              details: [
                '⚠️ The stairs are steep — wear good shoes and watch your step',
                '🌅 Sunset faces west from the beach — arrive 30 min before for best light',
                '🏖️ The beach is dramatic and rocky — perfect for photography'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mozambique',
              description: "South African-inspired beachside restaurant with a rooftop deck in Laguna Beach. The peri-peri dishes, seafood, and cocktails are excellent — and the ocean views are spectacular at sunset.",
              meta: '💰 $$$ · 📍 1740 S Coast Hwy, Laguna Beach · Rooftop recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.5665, lng: -117.8380, label: 'Crystal Cove State Park', num: 1, cat: 'attraction', desc: '3.5 miles of wild coastline, historic cottages, and tide pools' },
        { lat: 33.5641, lng: -117.8342, label: 'Crystal Cove Shake Shack', num: 2, cat: 'food', desc: '1940s beachside shack — milkshakes and breakfast burritos' },
        { lat: 33.5720, lng: -117.8400, label: 'Moro Canyon Trailhead', num: 3, cat: 'attraction', desc: '5-mile ridge loop with 360° coastal views' },
        { lat: 33.5428, lng: -117.7854, label: 'Laguna Beach Main Beach', num: 4, cat: 'attraction', desc: 'Iconic village beach with boardwalk and volleyball courts' },
        { lat: 33.5448, lng: -117.7870, label: 'Heisler Park', num: 5, cat: 'attraction', desc: 'Cliffside gardens with sweeping Pacific views' },
        { lat: 33.5355, lng: -117.7817, label: 'Thousand Steps Beach', num: 6, cat: 'attraction', desc: 'Hidden cliffside beach — stunning sunset spot' },
        { lat: 33.5418, lng: -117.7862, label: 'Taco Loco', num: 7, cat: 'food', desc: 'Best fish tacos in OC since 1987' },
        { lat: 33.5214, lng: -117.7749, label: 'Mozambique Restaurant', num: 8, cat: 'food', desc: 'South African rooftop dining with ocean views' }
      ]
    },
    {
      num: 4,
      date: '2026-02-25',
      neighborhoods: 'UCI Campus · Diamond Jamboree · Quail Hill',
      title: 'Campus Culture, Asian Eats & Sunset Hike',
      description: "Explore Irvine's own backyard today — the beautiful UC Irvine campus and arboretum, a deep dive into the incredible Diamond Jamboree Asian food hall, and a golden-hour hike on the Quail Hill Loop Trail with views of the city and mountains.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'UCI Campus & Aldrich Park',
              description: "The UC Irvine campus is built around a remarkable circular central park — Aldrich Park — ringed by a stunning ring road and faculty buildings. Walk through the park, stop at the modernist architecture, and visit the newly built OCMA (Orange County Museum of Art) on campus.",
              details: [
                '🏛️ OCMA opened 2022 — bold contemporary art in a striking Morphosis-designed building',
                '🌲 Aldrich Park has a magnificent fig tree grove and peaceful paths',
                '🔭 The ALP Anteater Recreation Center has impressive views of the ring road',
                '📸 The circular campus layout is unique in American academia'
              ]
            },
            {
              title: 'UCI Arboretum',
              description: "A hidden gem on the western edge of campus — 12 acres of plants from around the world, including a renowned South African collection that blooms in late winter. The king proteas are spectacular in February.",
              details: [
                '🌺 Late February brings the best South African protea blooms',
                '🆓 Free admission most days',
                '🌿 The California native section and succulent garden are highlights'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee',
              name: 'Peet\'s Coffee (UCI)',
              description: 'Campus café fuel before the food hall adventure.',
              meta: '💰 $ · 📍 UC Irvine Student Center'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Diamond Jamboree Food Hall Crawl',
              description: "Diamond Jamboree is a must-visit — an Asian-American food and retail center that's become one of Orange County's best dining destinations. A stunning lineup of authentic Taiwanese, Korean, Japanese, and Chinese restaurants cluster here. Do a group crawl — order multiple dishes and share.",
              details: [
                '🍜 85°C Bakery Cafe — Taiwanese-style breads and pastries',
                '🍣 Ichiya Ramen — rich tonkotsu ramen',
                '🧋 Yi Fang Taiwan Fruit Tea — fresh fruit bubble tea',
                '🥟 Huynh Garden — Vietnamese soups and banh mi',
                '🍡 Popular: Din Tai Fung nearby at South Coast Plaza for XLB dumplings'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Quail Hill Loop Trail at Golden Hour',
              description: "The Quail Hill Loop Trail is Irvine's favorite local hike — 2.8 miles through coastal sage scrub and grassland with panoramic views of Irvine, the Saddleback Mountains, and (on clear days) the ocean. The golden hour light on this trail is magnificent.",
              details: [
                '🥾 2.8 miles, easy-moderate, about 1 hour',
                '🌅 Sunset faces west — perfect timing from November through April',
                '🦅 Red-tailed hawks and coyotes are commonly spotted',
                '🐕 Dog-friendly trail'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Bistango',
              description: "One of Irvine's most celebrated restaurants — an art-filled supper club with rotating gallery walls, live jazz, and inventive California cuisine. The perfect group dinner with atmosphere. Make reservations.",
              meta: '💰 $$$ · 📍 19100 Von Karman Ave, Irvine · Live music most evenings'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6461, lng: -117.8427, label: 'UCI Aldrich Park', num: 1, cat: 'attraction', desc: 'Circular central park at the heart of UC Irvine campus' },
        { lat: 33.6456, lng: -117.8497, label: 'OCMA at UCI', num: 2, cat: 'attraction', desc: 'Orange County Museum of Art — bold Morphosis building (2022)' },
        { lat: 33.6460, lng: -117.8430, label: 'UCI Arboretum', num: 3, cat: 'attraction', desc: '12-acre botanical garden with stunning South African proteas' },
        { lat: 33.6850, lng: -117.8236, label: 'Diamond Jamboree', num: 4, cat: 'food', desc: 'Asian-American food hall — Irvine\'s best culinary adventure' },
        { lat: 33.6297, lng: -117.7888, label: 'Quail Hill Loop Trail', num: 5, cat: 'attraction', desc: '2.8-mile golden-hour hike with mountain and city views' },
        { lat: 33.6670, lng: -117.8190, label: 'Bistango', num: 6, cat: 'food', desc: 'Art-filled supper club with live jazz and California cuisine' }
      ]
    },
    {
      num: 5,
      date: '2026-02-26',
      neighborhoods: 'Dana Point · San Juan Capistrano · South OC Coast',
      title: 'Whale Watching, Dana Point Harbor & Old Town',
      description: "February is peak gray whale migration season along the California coast, and Dana Point is the best place in OC to catch them. After a thrilling whale watch, explore Dana Point Harbor's waterfront, then drive to charming Old Town San Juan Capistrano for mission history and a legendary burger.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dana Point Whale Watching Cruise',
              description: "Book a 2.5-hour whale watching cruise from Dana Point Harbor — February is the peak of gray whale southbound migration, and you'll likely see dozens of gray whales passing close to shore. The harbor also teems with Pacific white-sided dolphins, sea lions, and occasionally blue whales.",
              details: [
                '🐋 Dana Wharf Sportfishing & Whale Watching runs multiple daily departures',
                '📅 Feb–Mar is best for gray whales — 90%+ sighting rates',
                '🐬 Common bottlenose and Pacific white-sided dolphins often escort the boat',
                '⚠️ Book in advance — morning trips sell out on weekends',
                '🧥 Bring a warm jacket — it\'s cool on the open water'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Pre-Cruise Breakfast',
              name: 'Proud Mary\'s',
              description: "Dana Point Harbor's beloved breakfast spot — hearty portions, great coffee, and a nautical atmosphere steps from the whale watch check-in.",
              meta: '💰 $$ · 📍 34689 Golden Lantern, Dana Point'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dana Point Harbor & Bluff Top Trail',
              description: "After the cruise, stroll Dana Point Harbor — one of Southern California's prettiest marinas. The Bluff Top Trail runs along the cliff edge above the harbor and beach, with excellent vantage points for spotting the ocean and Catalina Island.",
              details: [
                '🚢 The harbor has a replica of the brig Pilgrim from Dana\'s 1830s voyage',
                '🌊 Baby Beach is a sheltered cove perfect for a peaceful picnic',
                '📸 The headland bluffs above the harbor offer beautiful coastal panoramas'
              ]
            },
            {
              title: 'Old Town San Juan Capistrano',
              description: "Drive 10 minutes inland to San Juan Capistrano — one of the oldest towns in California. The Mission San Juan Capistrano (founded 1776) has stunning gardens, resident swallows, and remarkable ruins. The surrounding Old Town has a walkable mix of antiques, wine bars, and boutiques.",
              details: [
                '🕊️ The swallows traditionally return to the mission every March — February you may catch early arrivals',
                '🌿 The mission gardens are serene and beautifully maintained',
                '🏛️ The Great Stone Church ruins are hauntingly beautiful',
                '🍷 Los Rios Historic District — wine tasting rooms and art galleries'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍔 Dinner',
              name: 'The Ramos House Café',
              description: "Tucked into San Juan Capistrano's historic Los Rios District — one of the most charming and celebrated brunch/dinner spots in all of Orange County. Seasonal farm-to-table Southern California cuisine in a 19th-century cottage.",
              meta: '💰 $$$ · 📍 31752 Los Rios St, San Juan Capistrano · Reservations essential'
            }
          ],
          tips: [
            { type: 'tip', text: "After dinner, walk the quiet gas-lamp lit streets of the Los Rios Historic District — it's genuinely one of the most atmospheric spots in Southern California. Worth lingering for." }
          ]
        }
      ],
      mapPins: [
        { lat: 33.4693, lng: -117.6980, label: 'Dana Point Harbor', num: 1, cat: 'attraction', desc: 'Whale watching departures, marinas, and bluff trail' },
        { lat: 33.4701, lng: -117.6969, label: 'Dana Wharf Whale Watching', num: 2, cat: 'attraction', desc: 'Best whale watching in OC — Feb peak gray whale season' },
        { lat: 33.4654, lng: -117.7017, label: 'Baby Beach', num: 3, cat: 'attraction', desc: 'Sheltered cove and picnic area in the harbor' },
        { lat: 33.4685, lng: -117.6963, label: 'Bluff Top Trail', num: 4, cat: 'attraction', desc: 'Clifftop walk above Dana Point with harbor and ocean views' },
        { lat: 33.4982, lng: -117.6622, label: 'Mission San Juan Capistrano', num: 5, cat: 'attraction', desc: 'Historic 1776 mission with stunning gardens and ruins' },
        { lat: 33.4981, lng: -117.6636, label: 'Ramos House Café', num: 6, cat: 'food', desc: 'Farm-to-table dining in a 19th-century Los Rios cottage' },
        { lat: 33.4690, lng: -117.6975, label: "Proud Mary's", num: 7, cat: 'food', desc: 'Harbor breakfast spot before the whale watch cruise' }
      ]
    },
    {
      num: 6,
      date: '2026-02-27',
      neighborhoods: 'Bommer Canyon · William Mason Park · Irvine Spectrum',
      title: 'Canyon Hike, Local Brunch & Farewell Night Out',
      description: "Your last full day in Irvine — morning hike through the wild oak canyons of Bommer Canyon, a lazy local brunch, an afternoon at William Mason Regional Park, and a proper farewell group dinner at one of Irvine's best.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bommer Canyon Cattle Camp Trail',
              description: "Bommer Canyon is one of Irvine's hidden natural treasures — a 2,500-acre open space reserve with ancient oak and sycamore groves, boulder-strewn hills, and a seasonal creek. The Cattle Camp Trail (3.5 miles, moderate) winds through the canyon past old ranching remnants.",
              details: [
                '🌳 200-year-old oak trees line the canyon — look for acorn woodpeckers',
                '🦊 Coyotes, deer, and red-tailed hawks are common',
                '💧 The creek can flow in February after rain — nice to see',
                '🥾 3.5 miles, moderate, approximately 1.5 hours',
                '📍 Trailhead at Bommer Canyon Trailhead off Shady Canyon Dr'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Post-Hike Brunch',
              name: 'HiroNori Craft Ramen',
              description: "Irvine's beloved craft ramen spot — housemade noodles in deeply complex broths. The tonkotsu ramen with chashu pork is extraordinary. Perfect post-hike fuel.",
              meta: '💰 $$ · 📍 2222 Michelson Dr, Irvine · Opens 11am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'William R. Mason Regional Park',
              description: "A peaceful 346-acre park with a beautiful lake, shaded picnic areas, and easy walking paths. Rent a paddleboat on the lake, feed the ducks, or just decompress under the eucalyptus trees. A lovely low-key afternoon for a group.",
              details: [
                '🚣 Paddleboat rentals available on the lake',
                '🦆 The waterfowl around the lake are abundant in February',
                '🌳 The tree canopy here is one of the best in Irvine',
                '🏓 Ping-pong tables and picnic facilities throughout'
              ]
            },
            {
              title: 'Irvine Spectrum Last-Minute Shopping & Treats',
              description: "Return to the Spectrum for any last-minute shopping, souvenir hunting, or dessert. The Giant Wheel at night is a different experience — colorful LED lights spinning above the palm trees.",
              details: [
                '🍦 Jamba Juice, Sugar+Plum, or Milk Jar Cookies for dessert',
                '🎡 Night ride on the Giant Wheel — the illuminated Spectrum from above is pretty',
                '🛍️ Anthropologie, H&M, REI, and dozens more for any last gifts'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Puesto Los Olivos',
              description: "The crown jewel of Irvine dining — upscale Mexican cuisine with an artistic twist from 'tacoteur' Eric Adler. The tortillas are handmade, the cocktails are serious, and the crispy cheese-skirt tacos are life-changing. Perfect farewell group dinner.",
              meta: '💰 $$$ · 📍 Irvine Spectrum Center · Reservations a must'
            }
          ],
          tips: [
            { type: 'tip', text: "Order a round of the house margaritas and the full taco spread for the table. The crispy cheese-skirt carne asada taco is the one everyone talks about. End the trip right." }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6350, lng: -117.7800, label: 'Bommer Canyon Trailhead', num: 1, cat: 'attraction', desc: '2,500-acre reserve with ancient oak canyons and wildlife' },
        { lat: 33.6510, lng: -117.8200, label: 'William R. Mason Regional Park', num: 2, cat: 'attraction', desc: '346-acre park with lake, paddleboats, and eucalyptus groves' },
        { lat: 33.6570, lng: -117.8231, label: 'HiroNori Craft Ramen', num: 3, cat: 'food', desc: 'Housemade noodles in complex broths — Irvine\'s best ramen' },
        { lat: 33.6508, lng: -117.7401, label: 'Irvine Spectrum Center (night)', num: 4, cat: 'attraction', desc: 'Giant Wheel at night with LED lights — great send-off views' },
        { lat: 33.6502, lng: -117.7415, label: 'Puesto Los Olivos', num: 5, cat: 'food', desc: 'Upscale Mexican with cheese-skirt tacos — farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$120–180/night', midrange: '$180–300/night', luxury: '$300–550/night' },
    { category: 'Meals (per person/day)', budget: '$30–50/day', midrange: '$60–100/day', luxury: '$120–200/day' },
    { category: 'Transport (car rental)', budget: '$40–60/day', midrange: '$60–100/day', luxury: '$100–200/day' },
    { category: 'Activities', budget: '$10–30/day', midrange: '$40–80/day', luxury: '$100–200/day' },
    { category: 'Whale Watching', budget: '$45pp', midrange: '$65pp', luxury: '$120pp (private)' },
    { category: '6-Day Total (group of 4)', budget: '$1,800–2,800', midrange: '$3,200–5,500', luxury: '$6,000–10,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Closest airport: John Wayne Airport (SNA) — 10 min from Irvine', 'LAX is 45–60 min away (add time for traffic)', 'Lyft/Uber from SNA to Irvine hotels: $20–35'] },
    { title: '🏨 Where to Stay', items: ['Irvine Marriott — central location near Spectrum, good group rooms', 'Hotel Irvine — rooftop pool, walkable to Jamboree dining corridor', 'AC Hotel Irvine — stylish, modern, near UCI', 'For beach access: Hotels in Newport Beach or Laguna Beach add 15-20 min drive'] },
    { title: '🌡️ February Weather', items: ['Average highs: 65–68°F (18–20°C), lows: 48–52°F (9–11°C)', 'February is officially rainy season — pack a light rain jacket', 'Pacific coastal fog common in mornings — burns off by 10–11am', 'Whale watching: Gray whale peak migration passes February–March'] },
    { title: '🚗 Driving Tips', items: ['All parking at major attractions is free or low-cost ($2–10)', 'PCH (Pacific Coast Highway) is the scenic coastal route — take it whenever possible', 'Rush hour (7–9am, 4–7pm) on I-5 and 405 can be brutal — plan accordingly', 'Many Irvine attractions have ample free parking'] },
    { title: '📱 Local Tips', items: ['Irvine is one of the safest cities in America — very relaxed, walkable feel', 'Download the OC Parks app for trail maps and tide charts', 'The OC Streetcar (Newport) and local OCTA buses supplement driving', 'Yelp and Google Maps are reliable for navigation and restaurant wait times'] }
  ]
};

fulfillOrder(order, itineraryData);
