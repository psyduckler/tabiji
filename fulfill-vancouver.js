const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771453980237_v1kanq',
  email: 'psyduckler@gmail.com',
  destination: 'Vancouver, BC, Canada',
  startDate: '2026-02-26',
  endDate: '2026-03-01',
  groupSize: 1,
  requests: 'asian food'
};

const itineraryData = {
  destination: 'Vancouver, BC, Canada',
  countryEmoji: '🇨🇦',
  title: 'Asian Flavours & Cultural Gems of Vancouver',
  subtitle: '3 days of world-class Asian cuisine, vibrant neighbourhoods & Pacific Northwest beauty for one',
  description: "Vancouver is North America's gateway to Asia — a city where dim sum rivals Hong Kong, ramen shops line entire blocks, and night markets sizzle with wok-fried everything. This solo itinerary threads through Chinatown's heritage, Richmond's legendary food scene, and the cultural pulse of a city shaped by generations of Asian immigration. Between meals, explore stunning coastal scenery, world-class museums, and neighbourhoods that feel like stepping between continents.",
  duration: '3 nights',
  dates: 'Feb 26 – Mar 1, 2026',
  budget: '$$',
  pace: 'Moderate',
  bestFor: 'Solo travellers · Foodies',
  highlights: [
    'Dim sum at one of North America\'s best Chinese restaurants',
    'Richmond\'s Golden Village — Asia outside of Asia',
    'Chinatown heritage walking tour & night market vibes',
    'Japanese ramen & izakaya crawl on Robson Street',
    'Granville Island Public Market for Pacific Northwest flavours'
  ],

  essentials: [
    { title: '🌧️ Late February Weather', text: 'Expect 4–9°C with frequent rain. Pack layers, a waterproof jacket, and an umbrella. The rain is light but persistent — Vancouverites don\'t let it stop them.' },
    { title: '🚇 Getting Around', text: 'The Canada Line SkyTrain connects downtown to Richmond in 25 minutes. Use a Compass Card for buses, SkyTrain, and SeaBus. Ride-sharing (Uber/Lyft) is widely available.' },
    { title: '🍜 Asian Food Scene', text: 'Vancouver has the best Asian food in North America, full stop. Richmond alone has 800+ Asian restaurants. No reservations needed for most dim sum — just arrive before 11am to avoid queues.' },
    { title: '🎒 Solo Travel Tips', text: 'Vancouver is extremely safe and walkable. Counter dining is king for solo eaters — sit at ramen bars, sushi counters, and dim sum tea houses without feeling out of place.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-26',
      neighborhoods: 'Downtown · Chinatown · Gastown',
      title: 'Chinatown Heritage & Evening Ramen',
      description: 'Arrive in Vancouver and dive straight into the cultural heart of the city. Explore North America\'s third-largest Chinatown, taste historic Chinese-Canadian cuisine, and end the night with a steaming bowl of ramen.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Chinatown Heritage Walk',
              description: 'Explore Vancouver\'s historic Chinatown, one of the largest in North America. Wander through the Millennium Gate, visit the Dr. Sun Yat-Sen Classical Chinese Garden — the first full-scale Chinese garden built outside China — and browse the herbal shops and bakeries along Pender Street.',
              details: [
                '🏯 Dr. Sun Yat-Sen Garden — $14 admission, a tranquil masterpiece of Ming Dynasty design',
                '🥮 Pick up egg tarts and pineapple buns from New Town Bakery',
                '📸 The Millennium Gate on Pender St is the classic Chinatown photo'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Late Lunch',
              name: 'Bao Bei Chinese Brasserie',
              description: 'A modern Chinese brasserie in a heritage Chinatown building. Creative small plates — mantou with braised pork, shao bing flatbreads, and excellent cocktails. Perfect for solo counter dining.',
              meta: '💰 $$ · 📍 163 Keefer St, Chinatown · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'The Dr. Sun Yat-Sen Garden is especially beautiful in the rain — the sound of droplets on the pond and the misty atmosphere create an almost meditative experience.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gastown Stroll & Steam Clock',
              description: 'Walk north to Gastown, Vancouver\'s oldest neighbourhood. The cobblestone streets, heritage buildings, and the iconic steam clock (whistling every 15 minutes) are atmospheric in the evening light. Browse independent boutiques and galleries along Water Street.',
              details: [
                '⏰ The Gastown Steam Clock — one of only a few steam-powered clocks in the world',
                '🏛️ Heritage buildings date back to the 1880s',
                '🛍️ Water Street has great independent shops and galleries'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Marutama Ra-men',
              description: 'Rich, creamy chicken paitan ramen — a Vancouver institution. The tonkotsu-style chicken broth is silky and deeply flavoured. Solo counter seating is the norm. Add a tamago egg and extra noodles.',
              meta: '💰 $ · 📍 270 Robson St · No reservations, expect a short queue'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 49.2796, lng: -123.1004, label: 'Millennium Gate', num: 1, cat: 'attraction', desc: 'Grand entrance to Vancouver\'s historic Chinatown' },
        { lat: 49.2793, lng: -123.1030, label: 'Dr. Sun Yat-Sen Garden', num: 2, cat: 'attraction', desc: 'Ming Dynasty classical Chinese garden' },
        { lat: 49.2791, lng: -123.0992, label: 'New Town Bakery', num: 3, cat: 'food', desc: 'Classic Chinese bakery — egg tarts and buns' },
        { lat: 49.2797, lng: -123.1002, label: 'Bao Bei Chinese Brasserie', num: 4, cat: 'food', desc: 'Modern Chinese small plates in heritage Chinatown' },
        { lat: 49.2843, lng: -123.1089, label: 'Gastown Steam Clock', num: 5, cat: 'attraction', desc: 'Iconic steam-powered clock in Vancouver\'s oldest neighbourhood' },
        { lat: 49.2815, lng: -123.1220, label: 'Marutama Ra-men', num: 6, cat: 'food', desc: 'Beloved chicken paitan ramen on Robson St' }
      ]
    },
    {
      num: 2,
      date: '2026-02-27',
      neighborhoods: 'Richmond · Golden Village · Steveston',
      title: 'Richmond — Asia Outside of Asia',
      description: 'Take the Canada Line south to Richmond, a suburban city that\'s become one of the greatest concentrations of authentic Asian cuisine outside of Asia. Dim sum for breakfast, bubble tea alleys, a sprawling Asian mall food court, and a sunset visit to the fishing village of Steveston.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dim Sum at Chef Tony',
              description: 'Start the day with world-class Cantonese dim sum. Chef Tony is a local favourite for its delicate har gow, crispy BBQ pork buns, and silky cheung fun. Arrive by 10am to avoid the queue. Solo diners can sit at communal tables.',
              details: [
                '🥟 Must-order: Har gow (crystal shrimp dumplings), char siu bao, and egg tarts',
                '🍵 Unlimited tea service — jasmine or pu-erh are classic choices',
                '⏰ Peak hours: 10:30am–12:30pm. Go early or late.'
              ]
            }
          ],
          meals: [
            {
              type: '🥟 Breakfast/Brunch',
              name: 'Chef Tony Seafood Restaurant',
              description: 'One of Richmond\'s top dim sum spots, known for pristine Cantonese dumplings, roast meats, and congee. The cart service is authentic and bustling.',
              meta: '💰 $$ · 📍 4600 No. 3 Rd, Richmond · Cash preferred for carts'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Golden Village & Aberdeen Centre',
              description: 'Explore Richmond\'s Golden Village — a cluster of Asian malls, bakeries, and shops that feels like stepping into Hong Kong or Taipei. Aberdeen Centre is the crown jewel: a massive Asian mall with a legendary food court featuring stalls from every corner of Asia.',
              details: [
                '🏬 Aberdeen Centre — Hong Kong-style mall with Asian grocery, fashion, and food court',
                '🧋 Hit up a bubble tea shop (CoCo, Tiger Sugar, or The Alley)',
                '🍡 Try Taiwanese fried chicken, takoyaki, or Korean corn dogs from food court stalls'
              ]
            },
            {
              title: 'Steveston Village',
              description: 'Take a bus to Steveston, a charming fishing village at the southwest tip of Richmond. Stroll the boardwalk, watch fishing boats unload their catch, and visit the Gulf of Georgia Cannery — a national historic site telling the story of BC\'s fishing industry and its deep ties to Japanese-Canadian heritage.',
              details: [
                '🎣 Fisherman\'s Wharf — buy fresh spot prawns and salmon straight off the boats (seasonal)',
                '🏛️ Gulf of Georgia Cannery — the Japanese-Canadian fishing story is deeply moving',
                '📸 The boardwalk and harbour are photogenic even on overcast days'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Japanese-Canadian community in Steveston has roots going back to the 1880s. The area was once called "Japanese-town" and the cannery history is a powerful story of immigration, internment, and resilience.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Korean BBQ Dinner',
              description: 'Head back to Richmond or downtown for Korean BBQ. Sura Korean Royal Cuisine in Richmond offers an elevated take, while Kook in downtown Vancouver is a buzzy, modern option with premium cuts of galbi and samgyeopsal.',
              details: [
                '🥩 Solo BBQ is totally normal — many spots have single-diner setups',
                '🍶 Pair with soju or Korean beer'
              ]
            }
          ],
          meals: [
            {
              type: '🔥 Dinner',
              name: 'Sura Korean Royal Cuisine',
              description: 'Upscale Korean dining in Richmond with beautifully presented royal court-style dishes. The banchan spread alone is worth the trip. Bulgogi, japchae, and seafood pancakes are standouts.',
              meta: '💰 $$–$$$ · 📍 4151 Hazelbridge Way, Richmond'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 49.1810, lng: -123.1360, label: 'Chef Tony Seafood Restaurant', num: 1, cat: 'food', desc: 'Top-tier Cantonese dim sum in Richmond' },
        { lat: 49.1820, lng: -123.1365, label: 'Aberdeen Centre', num: 2, cat: 'attraction', desc: 'Massive Asian mall with legendary food court' },
        { lat: 49.1240, lng: -123.1830, label: 'Steveston Village', num: 3, cat: 'attraction', desc: 'Historic fishing village with Japanese-Canadian heritage' },
        { lat: 49.1242, lng: -123.1875, label: 'Gulf of Georgia Cannery', num: 4, cat: 'attraction', desc: 'National historic site — BC fishing and immigration history' },
        { lat: 49.1815, lng: -123.1350, label: 'Sura Korean Royal Cuisine', num: 5, cat: 'food', desc: 'Upscale Korean royal court cuisine in Richmond' }
      ]
    },
    {
      num: 3,
      date: '2026-02-28',
      neighborhoods: 'Granville Island · Kitsilano · West End',
      title: 'Pacific Northwest Culture & Japanese Izakaya Night',
      description: 'Explore Vancouver\'s creative and culinary soul — Granville Island\'s public market, the Museum of Anthropology\'s Indigenous art, and Kitsilano\'s laid-back beach vibes. End with a Japanese izakaya crawl through the West End.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Granville Island Public Market',
              description: 'Ferry across to Granville Island and spend the morning browsing the public market. It\'s a feast for the senses — fresh Pacific salmon, local cheeses, artisan breads, and incredible Asian-fusion food stalls. Grab a window seat at the market and watch the boats.',
              details: [
                '🚢 Take the Aquabus mini-ferry from downtown — $3.50, scenic, and fun',
                '🐟 Try the smoked salmon sampler or a fresh oyster plate',
                '🎨 Studios and galleries throughout the island showcase local artists'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'A Bread Affair + Market Stalls',
              description: 'Graze through the market — pastries from A Bread Affair, a Thai iced tea from one of the Asian stalls, and a sit-down oyster plate from the seafood counter. The best brunch in Vancouver is the one you assemble yourself.',
              meta: '💰 $–$$ · 📍 Granville Island Public Market'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Museum of Anthropology at UBC',
              description: 'Take a bus to UBC and visit the Museum of Anthropology — one of the world\'s great museums of Indigenous art and culture. The Great Hall, filled with towering totem poles and carved figures against floor-to-ceiling glass overlooking the mountains, is breathtaking. The Asian art collection is also world-class.',
              details: [
                '🏛️ Admission $18 · The Great Hall alone is worth the trip',
                '🎭 Bill Reid\'s "The Raven and the First Men" — an iconic Canadian artwork',
                '🌏 Significant collection of Asian ceramics and textiles'
              ]
            },
            {
              title: 'Kitsilano Beach & Views',
              description: 'After the museum, walk or bus down to Kitsilano Beach. Even in late February, the views across English Bay to the North Shore mountains are stunning. Grab a coffee and enjoy the Pacific Northwest scenery.',
              details: [
                '⛰️ Views of the North Shore mountains, often snow-capped in February',
                '☕ 49th Parallel Coffee on West 4th is a local favourite'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Japanese Izakaya Crawl — Robson & Denman',
              description: 'Vancouver\'s West End, especially along Robson and Denman Streets, is packed with authentic Japanese izakayas, sushi bars, and ramen shops. Do a mini crawl: start with sashimi at one spot, yakitori at another, and finish with a nightcap at a whisky bar.',
              details: [
                '🍶 Guu with Garlic — lively izakaya with incredible tapas-style dishes',
                '🍣 Miku — if you splurge on one sushi meal, make it this. Aburi (flame-seared) sushi is their signature',
                '🥃 Zakkushi — charcoal-grilled yakitori skewers with Japanese beer'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Guu with Garlic',
              description: 'Vancouver\'s most beloved izakaya. The staff shout "irasshaimase!" when you enter, the energy is electric, and the kabocha korokke and saba shioyaki are legendary. Solo counter seats are the best in the house.',
              meta: '💰 $$ · 📍 1698 Robson St · No reservations — queue is part of the fun'
            },
            {
              type: '🍣 Late Night',
              name: 'Zakkushi on Denman',
              description: 'Charcoal-grilled yakitori skewers in a cozy, intimate setting. Every part of the chicken is celebrated. Pair with a cold Asahi and watch the grill master work.',
              meta: '💰 $$ · 📍 823 Denman St'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 49.2713, lng: -123.1340, label: 'Granville Island Public Market', num: 1, cat: 'food', desc: 'Iconic public market with seafood, produce, and Asian food stalls' },
        { lat: 49.2695, lng: -123.1350, label: 'Aquabus Ferry Terminal', num: 2, cat: 'attraction', desc: 'Mini-ferry to Granville Island from downtown' },
        { lat: 49.2695, lng: -123.2594, label: 'Museum of Anthropology (UBC)', num: 3, cat: 'attraction', desc: 'World-class Indigenous art and Asian ceramics collection' },
        { lat: 49.2743, lng: -123.1536, label: 'Kitsilano Beach', num: 4, cat: 'attraction', desc: 'Beach with stunning mountain views across English Bay' },
        { lat: 49.2875, lng: -123.1275, label: 'Guu with Garlic', num: 5, cat: 'food', desc: 'Vancouver\'s most beloved Japanese izakaya' },
        { lat: 49.2875, lng: -123.1360, label: 'Zakkushi on Denman', num: 6, cat: 'food', desc: 'Charcoal-grilled yakitori skewers' }
      ]
    }
  ]
};

fulfillOrder(order, itineraryData);
