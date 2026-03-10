const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773128916505_s8eles',
  email: 'galaxycats510@gmail.com',
  destination: 'Sapporo, Hokkaido, Japan',
  startDate: '2026-03-21',
  endDate: '2026-03-23',
  groupSize: '3-4',
  requests: 'I want to see makomanai takino cementry, fushimi inari, shiroi kobito theme park, shirahige waterfall, Jozankei Onsen. Make sure to add timings. im staying in sapporo'
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '\u{1F1EF}\u{1F1F5}',
  title: 'Snow, Shrines & Soaking \u2014 A Sapporo Winter Escape',
  subtitle: '3 days of hidden Buddhas, torii gates, chocolate factories & hot springs for your crew',
  description: "Late March in Sapporo is a world between seasons \u2014 the last breath of Hokkaido winter, snow still dusting the mountains while the city starts to stir toward spring. This itinerary hits every spot on your wishlist: the surreal Hill of the Buddha at Makomanai Takino Cemetery, Sapporo's own Fushimi Inari Shrine with its tunnel of vermillion torii, the whimsical Shiroi Koibito chocolate theme park, and a soul-warming soak at Jozankei Onsen in the snowy valley. We've packed in real timings, transit details from central Sapporo, and the best casual eats near every stop \u2014 from steaming bowls of miso ramen to fresh seafood at Nijo Market. Bundle up, bring your sense of wonder, and let Hokkaido work its quiet magic.",
  duration: '3 days',
  dates: 'Mar 21 \u2013 Mar 23, 2026',
  budget: '$$',
  pace: 'Moderate',
  bestFor: 'Friends \u00B7 Small Groups',
  highlights: [
    'The surreal Hill of the Buddha at Makomanai Takino Cemetery \u2014 a giant Buddha hidden inside a hill, designed by Tadao Ando',
    "Sapporo Fushimi Inari Shrine \u2014 27 vermillion torii gates on a forested hillside, Hokkaido's only Inari shrine",
    "Shiroi Koibito Park \u2014 Sapporo's beloved chocolate theme park with factory tours & cookie-making workshops",
    'Jozankei Onsen \u2014 a snowy mountain hot spring valley just 1 hour from central Sapporo',
    "Sapporo's legendary miso ramen, fresh seafood at Nijo Market & Genghis Khan grilled lamb"
  ],
  essentials: [
    { title: '\u{1F976} Late March = Still Winter', text: 'Sapporo in late March averages -2\u00B0C to 5\u00B0C (28-41\u00B0F). Snow is still on the ground, especially at higher elevations like Jozankei and Takino Cemetery. Pack warm layers, a waterproof jacket, insulated boots with good grip, gloves, and a hat. Roads and paths can be icy.' },
    { title: '\u{1F687} Getting Around', text: "Sapporo has an efficient subway (3 lines), buses, and a streetcar. Get a Kitaca IC card at any station for tap-and-go on all transit. For Jozankei, take the Jotetsu 'Kappa Liner' bus from Sapporo Station (~75 min, \u00A5800 one-way). For Makomanai Takino Cemetery, take the Namboku Line to Makomanai Station then bus #106 (~25 min)." },
    { title: '\u{1F35C} Dining Style', text: "Sapporo is a casual food city \u2014 think ramen alleys, izakayas, and market stalls. No reservations needed for most places. Sapporo miso ramen is a must (rich, buttery, topped with corn and butter). Susukino comes alive at night with hundreds of small eateries." },
    { title: '\u2668\uFE0F Onsen Etiquette', text: "At Jozankei (and any Japanese onsen): wash thoroughly before entering the bath, no swimsuits, tie long hair up, and don't submerge towels. Tattoos may be restricted at some facilities \u2014 we've recommended tattoo-friendly options. Bring a small towel or rent one on-site." },
    { title: '\u{1F4B4} Budget Tips', text: 'Japan is still a cash-friendly country. Convenience stores (7-Eleven, Lawson, Seicomart) have ATMs that accept foreign cards. Most attractions accept IC cards or cash. Budget \u00A53,000-5,000/person per day for meals at casual spots.' }
  ],
  days: [
    {
      num: 1,
      date: '2026-03-21',
      neighborhoods: 'Minami Ward \u00B7 Chuo-ku \u00B7 Fushimi',
      title: 'Hidden Buddhas & Torii Gates',
      description: "Start your Sapporo adventure with two of the city's most photogenic spiritual sites. Morning at the otherworldly Makomanai Takino Cemetery to see the Hill of the Buddha \u2014 a 13.5-metre statue concealed inside a hill, designed by Tadao Ando. Then Sapporo's own Fushimi Inari Shrine with 27 vermillion torii gates. End with Genghis Khan grilled lamb in Susukino.",
      timeBlocks: [
        {
          label: 'Morning (9:00 AM \u2013 12:30 PM)',
          activities: [
            {
              title: 'Makomanai Takino Cemetery \u2014 Hill of the Buddha',
              description: "One of the most extraordinary sights in Hokkaido. A 13.5-metre seated Buddha statue is enclosed within a hill, with only the top of its head peeking out. You approach through a long, serene concrete tunnel designed by Tadao Ando that opens dramatically to reveal the massive Buddha. The grounds also have full-sized Moai replicas and a Stonehenge reproduction \u2014 wonderfully surreal.",
              details: [
                '\u23F0 Winter hours (Nov\u2013Mar): 10:00 AM \u2013 3:00 PM \u2014 arrive by 10:00 to have plenty of time',
                '\u{1F687} From Sapporo Station: Namboku Line subway to Makomanai Station (~20 min, \u00A5290)',
                '\u{1F68C} At Makomanai Station: bus #106 from the bus stop in front (~25 min, \u00A5210). Get off at Takino Reien stop',
                '\u{1F3AB} Free admission to the grounds and Great Buddha Hall',
                '\u{1F4F8} The tunnel approach is the money shot \u2014 walk slowly and enjoy the reveal',
                '\u23F1\uFE0F Allow 60-90 minutes to explore the Buddha, Moai statues, and grounds',
                '\u{1F9E4} The grounds are exposed and cold/windy in March \u2014 dress warmly'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Bus #106 runs roughly every 30 minutes. Check the return schedule when you arrive so you don't get stranded. Last return bus from Takino Cemetery in winter is around 2:30 PM." }
          ]
        },
        {
          label: 'Afternoon (1:30 PM \u2013 4:30 PM)',
          activities: [
            {
              title: 'Lunch near Makomanai Station',
              description: 'After returning by bus, grab lunch near the station before heading to the shrine.',
              details: [
                '\u{1F35C} Ramen Shingen (\u4FE1\u7384) near Makomanai \u2014 excellent miso ramen, often ranked top in Sapporo',
                '\u23F0 Budget 30-40 minutes for lunch'
              ]
            },
            {
              title: 'Sapporo Fushimi Inari Shrine (\u672D\u5E4C\u4F0F\u898B\u7A32\u8377\u795E\u793E)',
              description: "Sapporo's branch of Kyoto's famous Fushimi Inari Taisha \u2014 and the only Inari shrine in all of Hokkaido. While smaller than its Kyoto namesake, the 27 vermillion torii gates ascending a forested hillside are stunning, especially with snow clinging to the trees. The shrine is known for blessings related to good relationships and safe travel.",
              details: [
                '\u{1F695} Taxi from Makomanai directly (~15 min, \u00A51,500-2,000) \u2014 easiest option for a group',
                '\u{1F687} Or: Namboku Line north to Nakanoshima, transfer Tozai Line to Maruyama Koen, then taxi/bus 10 min',
                '\u{1F4CD} Address: 2 Chome Fushimi, Chuo Ward, Sapporo',
                '\u23F0 Open 24 hours (outdoor shrine) \u2014 visit during daylight for photos',
                '\u{1F3AB} Free',
                '\u23F1\uFE0F Allow 30-45 minutes for the torii gate path and grounds',
                '\u{1F4F8} Best photos from the bottom looking up through the torii tunnel'
              ]
            }
          ],
          meals: [
            {
              type: '\u{1F35C} Lunch',
              name: 'Ramen Shingen (\u4FE1\u7384) Minami 6-jo Branch',
              description: "One of Sapporo's most beloved miso ramen shops. Rich, deeply flavoured pork-based miso broth topped with corn, bean sprouts, and butter.",
              meta: '\u{1F4B0} \u00A5900-1,100 \u00B7 \u{1F4CD} Near Makomanai Station \u00B7 Expect a short queue'
            }
          ]
        },
        {
          label: 'Evening (5:30 PM \u2013 9:00 PM)',
          activities: [
            {
              title: 'Nijo Market (\u4E8C\u6761\u5E02\u5834)',
              description: "Sapporo's historic seafood market, operating since the Meiji era. Browse stalls of glistening Hokkaido seafood \u2014 giant crab legs, fresh uni, ikura, and scallops the size of your palm. Several stalls offer eat-in donburi (seafood rice bowls).",
              details: [
                '\u{1F4CD} Chuo-ku, just south of Odori Park \u2014 5 min walk from Odori Station',
                '\u23F0 Most stalls open until 6:00 PM, some restaurants stay open later',
                '\u{1F980} Try a seafood donburi (kaisen-don) for \u00A51,500-3,000'
              ]
            },
            {
              title: 'Susukino Evening Stroll',
              description: "Sapporo's vibrant entertainment district. Neon lights reflect off the snow, and hundreds of small izakayas, ramen joints, and bars line the streets.",
              details: [
                '\u{1F4CD} Susukino Station on the Namboku Line \u2014 one stop south of Odori',
                '\u{1F37A} Try a Sapporo Classic beer \u2014 the local-only brew you can\'t get outside Hokkaido'
              ]
            }
          ],
          meals: [
            {
              type: '\u{1F356} Dinner',
              name: 'Daruma Genghis Khan (\u3060\u308B\u307E)',
              description: "A Sapporo institution for Genghis Khan \u2014 Hokkaido's signature grilled lamb dish. You cook tender slices on a dome-shaped grill at your table. The original shop in Susukino has been running since 1954.",
              meta: '\u{1F4B0} \u00A51,500-2,500/person \u00B7 \u{1F4CD} Susukino, Crystal Bldg 4-jo \u00B7 Opens 5:00 PM \u00B7 Expect 15-30 min wait'
            }
          ],
          tips: [
            { type: 'tip', text: "Daruma has multiple branches in Susukino within a block of each other. If the main shop (4-jo) has a huge queue, check the 5-jo or 6-jo branches \u2014 same food, shorter wait." }
          ]
        }
      ],
      mapPins: [
        { lat: 42.9545, lng: 141.3614, label: 'Makomanai Takino Cemetery', num: 1, cat: 'attraction', desc: 'Hill of the Buddha \u2014 13.5m statue by Tadao Ando' },
        { lat: 42.9918, lng: 141.3235, label: 'Makomanai Station', num: 2, cat: 'transport', desc: 'Namboku Line subway \u2014 transfer point for bus #106' },
        { lat: 43.0392, lng: 141.3308, label: 'Sapporo Fushimi Inari Shrine', num: 3, cat: 'attraction', desc: "27 vermillion torii gates \u2014 Hokkaido's only Inari shrine" },
        { lat: 43.0585, lng: 141.3551, label: 'Nijo Market', num: 4, cat: 'food', desc: 'Historic seafood market with eat-in donburi stalls' },
        { lat: 43.0545, lng: 141.3534, label: 'Susukino', num: 5, cat: 'attraction', desc: "Sapporo's neon-lit entertainment & dining district" },
        { lat: 43.0534, lng: 141.3523, label: 'Daruma Genghis Khan', num: 6, cat: 'food', desc: 'Legendary grilled lamb since 1954' }
      ]
    },
    {
      num: 2,
      date: '2026-03-22',
      neighborhoods: 'Nishi Ward \u00B7 Odori \u00B7 Tanukikoji',
      title: 'Chocolate Factory & City Flavours',
      description: "Spend the morning at Shiroi Koibito Park \u2014 Sapporo's beloved chocolate theme park \u2014 with factory tours, cookie-making workshops, and fairy-tale gardens dusted with snow. Afternoon in central Sapporo for Odori Park, Tanukikoji arcade, and JR Tower sunset views. Evening at the famous Sapporo Ramen Alley.",
      timeBlocks: [
        {
          label: 'Morning (9:30 AM \u2013 1:00 PM)',
          activities: [
            {
              title: 'Shiroi Koibito Park (\u767D\u3044\u604B\u4EBA\u30D1\u30FC\u30AF)',
              description: "Sapporo's most popular attraction \u2014 a chocolate theme park built by ISHIYA, makers of Hokkaido's famous Shiroi Koibito cookies. The European-style buildings, clock tower, and rose garden (snow-covered in March) feel like a fairy tale. Tour the chocolate factory, learn chocolate history, and try the cookie-making workshop where you decorate your own heart-shaped Shiroi Koibito cookie.",
              details: [
                '\u23F0 Open 10:00 AM \u2013 5:00 PM (last entry 4:00 PM)',
                '\u{1F687} From Sapporo Station: Tozai Line to Miyanosawa Station (~20 min, \u00A5290), then 7-minute walk',
                '\u{1F3AB} Admission: \u00A5800/adult (factory tour area). Free area includes shop, caf\u00E9, garden',
                '\u{1F36A} Cookie-making workshop: \u00A51,200/person \u2014 sign up at the counter on arrival (first come, ~40 min)',
                '\u23F1\uFE0F Allow 2-3 hours for factory tour + workshop + garden + shopping',
                '\u{1F6CD}\uFE0F The shop has exclusive flavors and Sapporo-only editions \u2014 perfect souvenirs',
                '\u{1F4F8} The clock tower performs every hour with a parade of chocolate figurines'
              ]
            }
          ],
          meals: [
            {
              type: '\u2615 Lunch',
              name: 'Shiroi Koibito Park Caf\u00E9',
              description: "The park's caf\u00E9 serves excellent soft-serve, chocolate drinks, and light meals. The Shiroi Koibito Soft Cream is their signature \u2014 rich white chocolate soft-serve that tastes like the cookie in frozen form.",
              meta: '\u{1F4B0} \u00A5600-1,200 \u00B7 \u{1F4CD} Inside the park \u00B7 Casual, no reservations'
            }
          ],
          tips: [
            { type: 'tip', text: 'Arrive right at 10:00 AM to beat tour groups. Cookie workshop spots fill up fast on weekends \u2014 sign up first, then explore while you wait for your time slot.' }
          ]
        },
        {
          label: 'Afternoon (2:00 PM \u2013 5:30 PM)',
          activities: [
            {
              title: 'Odori Park & Sapporo TV Tower',
              description: "Stroll through Odori Park \u2014 the green belt dividing the city. In late March, it's still wintry but starting to thaw. Climb the Sapporo TV Tower at the east end for a 360\u00B0 view of the city grid stretching to the mountains.",
              details: [
                '\u{1F4CD} Odori Park runs east-west for 1.5 km through the city center',
                '\u{1F5FC} TV Tower observation deck: \u00A51,000/adult, open 9:00 AM \u2013 10:00 PM',
                '\u{1F4F8} Best views at golden hour \u2014 sunset is around 5:50 PM in late March'
              ]
            },
            {
              title: 'Tanukikoji Shopping Arcade (\u72F8\u5C0F\u8DEF)',
              description: "Japan's oldest covered shopping arcade (since 1873), stretching 7 blocks through central Sapporo. Souvenir shops, drug stores, caf\u00E9s, game arcades, and local boutiques \u2014 all under a covered roof so you stay warm.",
              details: [
                '\u{1F4CD} One block south of Odori Park, from Nishi 1 to Nishi 7',
                '\u23F0 Most shops open 10:00 AM \u2013 8:00 PM',
                '\u{1F6CD}\uFE0F Look for Royce\' chocolate, Rokkatei sweets, and Hokkaido melon products'
              ]
            }
          ]
        },
        {
          label: 'Evening (6:00 PM \u2013 9:00 PM)',
          activities: [
            {
              title: 'JR Tower Observation Deck T38',
              description: "Head to the 38th floor of JR Tower (above Sapporo Station) for panoramic views. On a clear evening, city lights stretch to the horizon with snow-capped mountains beyond. The dimmed interior lighting makes it feel intimate.",
              details: [
                '\u{1F4CD} JR Tower, directly above Sapporo Station',
                '\u23F0 Open 10:00 AM \u2013 10:00 PM (last entry 9:30 PM)',
                '\u{1F3AB} \u00A5740/adult',
                '\u{1F306} Arrive by 5:30 PM for golden hour \u2014 sunset around 5:50 PM'
              ]
            }
          ],
          meals: [
            {
              type: '\u{1F35C} Dinner',
              name: 'Ganso Sapporo Ramen Yokocho (\u5143\u7956\u3055\u3063\u307D\u308D\u30E9\u30FC\u30E1\u30F3\u6A2A\u4E01)',
              description: "The original Sapporo Ramen Alley \u2014 a narrow lane in Susukino with 17 tiny ramen shops shoulder-to-shoulder, each serving their own take on Sapporo miso ramen. Operating since 1951, this is where Sapporo miso ramen was born.",
              meta: '\u{1F4B0} \u00A5800-1,200 \u00B7 \u{1F4CD} Minami 5-jo, Nishi 3 (Susukino) \u00B7 Most shops open 11:00 AM \u2013 2:00 AM'
            }
          ],
          tips: [
            { type: 'tip', text: "Can't decide which ramen shop? Favorites include Shirakaba Sansou (\u767D\u6A3A\u5C71\u8358) for classic miso and Ichiryuan (\u4E00\u7C92\u5EB5) for rich garlic miso. Just follow your nose." }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0815, lng: 141.2762, label: 'Shiroi Koibito Park', num: 1, cat: 'attraction', desc: 'Chocolate theme park with factory tours & cookie workshops' },
        { lat: 43.0600, lng: 141.3565, label: 'Sapporo TV Tower', num: 2, cat: 'attraction', desc: '360\u00B0 city views from the observation deck' },
        { lat: 43.0580, lng: 141.3500, label: 'Odori Park', num: 3, cat: 'attraction', desc: "Sapporo's central green belt dividing north and south" },
        { lat: 43.0565, lng: 141.3500, label: 'Tanukikoji Shopping Arcade', num: 4, cat: 'attraction', desc: "Japan's oldest covered shopping arcade \u2014 7 blocks of shops" },
        { lat: 43.0689, lng: 141.3509, label: 'JR Tower T38', num: 5, cat: 'attraction', desc: '38th floor observation deck above Sapporo Station' },
        { lat: 43.0541, lng: 141.3519, label: 'Ramen Yokocho', num: 6, cat: 'food', desc: 'Original Sapporo Ramen Alley \u2014 17 shops since 1951' }
      ]
    },
    {
      num: 3,
      date: '2026-03-23',
      neighborhoods: 'Jozankei \u00B7 Minami-ku \u00B7 Sapporo Station',
      title: 'Hot Springs in the Snowy Valley',
      description: "Your final day is pure relaxation \u2014 a journey to Jozankei Onsen, Sapporo's mountain hot spring retreat in a forested valley about an hour south. Soak in outdoor rotenburo baths surrounded by snow-dusted trees, stroll along the Toyohira River, and warm up from the inside out. Return for a farewell feast at the iconic Sapporo Beer Garden.",
      timeBlocks: [
        {
          label: 'Morning (8:30 AM \u2013 12:00 PM)',
          activities: [
            {
              title: 'Bus to Jozankei Onsen (\u5B9A\u5C71\u6E13\u6E29\u6CC9)',
              description: "Catch the Jotetsu Kappa Liner direct bus from Sapporo Station to Jozankei Onsen. The 75-minute ride takes you through increasingly mountainous terrain into a quiet valley where steam rises from the river and snow blankets the peaks. Jozankei has been a hot spring retreat for over 150 years.",
              details: [
                '\u{1F68C} Kappa Liner bus from Sapporo Station Bus Terminal (Platform 12)',
                '\u23F0 First bus around 8:30 AM, runs every 30-60 min. \u00A5800 one-way (~75 min)',
                '\u{1F4CD} Get off at Jozankei Onsen (\u5B9A\u5C71\u6E13\u6E29\u6CC9) stop',
                '\u{1F3AB} Some hotels sell round-trip + day-use onsen packages at Sapporo Station'
              ]
            },
            {
              title: 'Jozankei Onsen \u2014 Outdoor Hot Spring Soak',
              description: "The main event: soak in a steaming outdoor rotenburo bath while snow drifts down around you. Several ryokan offer day-use bathing (higaeri nyuyoku). Mori no Uta is our top pick for groups: beautiful facilities, forest views, and tattoo-friendly private baths available.",
              details: [
                '\u2668\uFE0F Top pick: Mori no Uta (\u68EE\u306E\u8B0C) \u2014 day-use \u00A51,500/person, 12:00-15:00, forest-view baths',
                '\u2668\uFE0F Budget pick: Jozankei View Hotel \u2014 day-use \u00A51,200/person, large indoor/outdoor pools, 12:00-15:00',
                '\u2668\uFE0F Free foot baths (ashiyu) along the river \u2014 no reservation, look for the Kappa statues',
                '\u{1F9D6} Most day-use slots are 12:00-15:00 \u2014 arrive by 11:30 to check in',
                '\u{1F3F7}\uFE0F Rent a towel set (\u00A5300-500) if you didn\'t bring one'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Look for the Kappa statues throughout Jozankei \u2014 the town's legendary water spirit. There are 23 hidden Kappa statues around town \u2014 a fun scavenger hunt while walking to the onsen." }
          ]
        },
        {
          label: 'Afternoon (12:00 PM \u2013 3:30 PM)',
          activities: [
            {
              title: 'Jozankei River Walk & Futami Suspension Bridge',
              description: "After your soak, walk along the Toyohira River. The Futami Suspension Bridge (\u4E8C\u898B\u540A\u6A4B) offers stunning views of the river gorge. In late March you may see the last of winter's ice formations on the rocks below.",
              details: [
                '\u{1F4CD} Futami Suspension Bridge is a 10-minute walk from the main onsen area',
                '\u{1F4F8} The red bridge against the snowy gorge is incredibly photogenic',
                '\u23F1\uFE0F Allow 30-45 minutes for the walk and bridge'
              ]
            }
          ],
          meals: [
            {
              type: '\u{1F35C} Lunch',
              name: 'Onsen Hotel Buffet or Jozankei Restaurants',
              description: "Many day-use packages include lunch. Mori no Uta has an excellent natural buffet using Hokkaido ingredients. The small restaurants on the main street serve udon, soba, and local dishes.",
              meta: '\u{1F4B0} \u00A51,500-2,500/person \u00B7 \u{1F4CD} Jozankei main street area'
            }
          ],
          tips: [
            { type: 'tip', text: "\u{1F4A7} About Shirahige Waterfall (\u767D\u3072\u3052\u306E\u6EDD): This beautiful blue waterfall is located in Biei \u2014 about 2.5 hours from Sapporo by car. It's wonderful but hard to fit in a 3-day Sapporo trip. If you have extra time on a future visit, it's worth the day trip. Jozankei's Futami Gorge offers similar natural beauty much closer." }
          ]
        },
        {
          label: 'Evening (4:30 PM \u2013 8:30 PM)',
          activities: [
            {
              title: 'Return to Sapporo & Sapporo Beer Museum',
              description: "Take the Kappa Liner bus back to Sapporo. If time allows, stop at the Sapporo Beer Museum in Sapporo Garden Park. Free self-guided tours, and the tasting salon offers three-glass tasting sets.",
              details: [
                '\u{1F68C} Kappa Liner back to Sapporo Station: catch the 3:30 or 4:00 PM bus',
                '\u{1F37A} Sapporo Beer Museum: open until 6:00 PM, free entry, tasting set \u00A5800',
                '\u{1F4CD} 10-minute walk from Sapporo Station or Toho Line to Higashi-Kuyakusho-mae'
              ]
            }
          ],
          meals: [
            {
              type: '\u{1F37B} Farewell Dinner',
              name: 'Sapporo Beer Garden \u2014 Genghis Khan Hall (\u30B5\u30C3\u30DD\u30ED\u30D3\u30FC\u30EB\u5712)',
              description: "End your trip at the iconic Sapporo Beer Garden in a gorgeous red-brick building from 1890. All-you-can-eat lamb grilled on dome-shaped hotplates, paired with fresh-from-the-brewery Sapporo beer. Festive, delicious, unforgettable.",
              meta: '\u{1F4B0} All-you-can-eat + drink: \u00A54,500-5,500/person (100 min) \u00B7 \u{1F4CD} Sapporo Garden Park \u00B7 Reservations recommended \u00B7 11:30 AM \u2013