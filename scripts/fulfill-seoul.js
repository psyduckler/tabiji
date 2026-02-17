const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771286409625_oulrnn',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Seoul, South Korea',
};

const itineraryData = {
  destination: 'Seoul, South Korea',
  countryEmoji: '🇰🇷',
  title: 'Seoul: A Fine Dining Odyssey',
  subtitle: 'Four days of Michelin-starred Korean cuisine, hidden omakase bars, and cultural immersion in one of Asia\'s greatest food cities',
  description: 'Seoul is a city where ancient palaces sit alongside Michelin-starred temples of gastronomy. This luxury solo itinerary is built around Korea\'s finest dining — from innovative Korean haute cuisine at Jungsik and Mingles to the refined elegance of La Yeon\'s traditional Korean course meals. Between extraordinary meals, explore Joseon-era palaces, wander through Bukchon\'s hanok village, sip tea in centuries-old tea houses, and unwind in a traditional jjimjilbang.',
  duration: '4 nights',
  dates: 'Jun 4 – Jun 8, 2026',
  budget: '$5,000 – $10,000',
  pace: 'Relaxed',
  bestFor: 'Solo travelers, Fine dining enthusiasts, Food connoisseurs',
  highlights: ['Michelin-starred Korean haute cuisine', 'Traditional Korean tea ceremony', 'Gyeongbokgung Palace & Bukchon Hanok Village', 'World-class omakase experiences', 'Jjimjilbang spa culture', 'Gangnam & Itaewon dining scenes'],

  essentials: [
    { title: '🛬 Getting Around', text: 'Seoul\'s metro is world-class — clean, fast, and English-friendly. Get a T-money card at the airport. Taxis are affordable and metered. Kakao T app works like Uber.' },
    { title: '💵 Money', text: 'Korean Won (KRW). Cards accepted nearly everywhere. Budget ₩300,000-600,000/day for fine dining. ATMs in convenience stores (CU, GS25) accept international cards.' },
    { title: '🗣️ Language', text: 'Korean is the language. English menus available at upscale restaurants. Papago (Naver) translates better than Google for Korean. Staff at fine dining spots often speak English.' },
    { title: '🌦️ Weather in June', text: 'Early summer — warm and humid, 20-28°C (68-82°F). Late June brings monsoon season. Pack light layers, an umbrella, and comfortable walking shoes.' },
    { title: '🍽️ Fine Dining Culture', text: 'Reservations essential for starred restaurants — book 2-4 weeks ahead. Lunch courses are often cheaper than dinner. Tipping is not customary in Korea. Many top restaurants close Sundays or Mondays.' },
    { title: '🔒 Safety', text: 'Seoul is exceptionally safe, even late at night. Solo dining is completely normal — many restaurants have solo counter seating. Convenience stores (편의점) are 24/7 lifelines.' },
  ],

  days: [
    // DAY 1 — Arrival + Gangnam Fine Dining
    {
      num: 1,
      title: 'Arrival & Gangnam Gastronomy',
      description: 'Touch down in Seoul and dive straight into Gangnam\'s Michelin-starred dining scene after a peaceful temple visit.',
      neighborhoods: 'Gangnam · Sinsa · Cheongdam',
      timeBlocks: [
        {
          label: 'Morning / Afternoon',
          activities: [
            {
              title: 'Arrive at Incheon International Airport',
              description: 'Take the AREX express train (43 min, ₩9,500) to Seoul Station, then taxi or metro to your hotel. Settle into your accommodation in the Gangnam or Jongno area.',
              details: ['Recommended hotels: Josun Palace (Gangnam), Park Hyatt Seoul, or The Shilla Seoul', '💡 Pick up a T-money card and pocket Wi-Fi at the airport']
            },
            {
              title: 'Bongeunsa Temple',
              description: 'A serene 8th-century Buddhist temple tucked between Gangnam\'s skyscrapers. Walk the grounds, admire the 23-meter Maitreya Buddha statue, and find calm before your culinary journey begins.',
              details: ['📍 531 Bongeunsa-ro, Gangnam-gu', '🕐 Open daily 5am-9pm · Free admission', '💡 Temple stay programs available if you want deeper immersion']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Dosa',
              description: 'Chef Jeong Jiyeon\'s intimate Korean fine dining in Cheongdam — a single-course menu featuring reinterpreted Korean dishes with impeccable seasonal ingredients. One Michelin star.',
              meta: '📍 Cheongdam-dong, Gangnam-gu · 💰 ₩80,000-120,000/person · ⭐ 1 Michelin star'
            },
            {
              type: '🍽️ Dinner',
              name: 'Jungsik',
              description: 'Korea\'s most internationally acclaimed restaurant. Chef Yim Jungsik reimagines Korean cuisine with modern techniques — expect dishes like bibimbap deconstructed into art. Two Michelin stars.',
              meta: '📍 11 Seolleung-ro 158-gil, Gangnam-gu · 💰 ₩200,000-300,000/person · ⭐⭐ 2 Michelin stars · ⚠️ Book well in advance'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Jet lag strategy: power through to dinner. Jungsik\'s tasting menu is worth staying awake for.' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.5140, lng: 126.4419, label: 'Incheon Airport', num: 1, cat: 'transport', desc: 'Arrival — AREX express to Seoul Station' },
        { lat: 37.5153, lng: 127.0574, label: 'Bongeunsa Temple', num: 2, cat: 'attraction', desc: '8th-century Buddhist temple in Gangnam' },
        { lat: 37.5244, lng: 127.0467, label: 'Dosa', num: 3, cat: 'restaurant', desc: '1-star Michelin Korean fine dining lunch' },
        { lat: 37.5240, lng: 127.0390, label: 'Jungsik', num: 4, cat: 'restaurant', desc: '2-star Michelin modern Korean dinner' }
      ]
    },

    // DAY 2 — Jongno Palaces & Traditional Korean Haute Cuisine
    {
      num: 2,
      title: 'Palaces, Hanok & Korean Haute Cuisine',
      description: 'A full day of Joseon-era grandeur, traditional tea culture, and Seoul\'s most celebrated fine dining — from 2-star Mingles to 3-star La Yeon.',
      neighborhoods: 'Jongno · Bukchon · Samcheong-dong',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gyeongbokgung Palace',
              description: 'Seoul\'s grandest Joseon-era palace (1395). Arrive early for the Royal Guard Changing Ceremony at 10am. Explore the throne hall, Gyeonghoeru Pavilion floating on its lotus pond, and the National Folk Museum inside the grounds.',
              details: ['📍 161 Sajik-ro, Jongno-gu', '🕐 9am-6pm (closed Tuesdays) · ₩3,000 admission', '💡 Wearing hanbok (Korean traditional dress) gets you free admission']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Tosokchon Samgyetang',
              description: 'Legendary ginseng chicken soup restaurant near Gyeongbokgung. The whole young chicken stuffed with ginseng, jujube, and glutinous rice is Seoul\'s most iconic breakfast. Always a queue — worth it.',
              meta: '📍 5 Jahamun-ro 5-gil, Jongno-gu · 💰 ₩18,000-22,000 · 🕐 Opens 10am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Arrive at Gyeongbokgung right at 9am to beat crowds and catch soft morning light for photos.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Bukchon Hanok Village',
              description: 'Wander through narrow alleys lined with 600-year-old traditional Korean houses (hanok). The area between Gyeongbokgung and Changdeokgung is one of Seoul\'s most photogenic neighborhoods.',
              details: ['📍 Between Jongno-gu 3-ga and Anguk stations', '💡 Be respectful — people live here. Keep voices low, especially on Gahoe-dong streets']
            },
            {
              title: 'Traditional Tea at Suyeonsanbang',
              description: 'A hidden gem — this 1930s wooden hanok was once the home of novelist Lee Tae-jun. Now a traditional tea house serving omija-cha (five-flavor berry tea), daechu-cha (jujube tea), and homemade rice cakes in a magical garden setting.',
              details: ['📍 8 Seongbuk-ro 26-gil, Seongbuk-gu', '💰 ₩8,000-15,000 per tea set', '💡 One of Seoul\'s most atmospheric experiences — don\'t skip this']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mingles',
              description: 'Chef Kang Min-goo\'s creative "Hansik" cuisine — Korean traditions reimagined through global techniques. The tasting menu moves through fermented, aged, and seasonal Korean ingredients in surprising ways. Two Michelin stars.',
              meta: '📍 19 Dosan-daero 67-gil, Gangnam-gu · 💰 ₩150,000-200,000/person · ⭐⭐ 2 Michelin stars · ⚠️ Reservations essential'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Changdeokgung Palace Moonlight Tour',
              description: 'If available (seasonal, limited tickets), this guided nighttime tour through Changdeokgung\'s Secret Garden is magical — lantern-lit paths through ancient pavilions and 300-year-old trees.',
              details: ['📍 99 Yulgok-ro, Jongno-gu', '💰 ₩30,000 · ⚠️ Tickets sell out instantly — book on interpark.com weeks ahead', '💡 Regular daytime tours also excellent if moonlight tour unavailable']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Yeon',
              description: 'The pinnacle of traditional Korean fine dining. Located atop The Shilla hotel, La Yeon serves exquisite royal court-inspired Korean cuisine. The multi-course dinner is a journey through Korean culinary heritage — each dish a masterpiece of balance and presentation. Three Michelin stars.',
              meta: '📍 The Shilla Seoul, 249 Dongho-ro, Jung-gu · 💰 ₩300,000-400,000/person · ⭐⭐⭐ 3 Michelin stars · ⚠️ Book 3-4 weeks ahead'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 La Yeon has Seoul\'s best city views at sunset. Request a window table when booking.' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.5796, lng: 126.9770, label: 'Gyeongbokgung Palace', num: 1, cat: 'attraction', desc: 'Grand Joseon-era palace with guard ceremony' },
        { lat: 37.5790, lng: 126.9735, label: 'Tosokchon Samgyetang', num: 2, cat: 'restaurant', desc: 'Legendary ginseng chicken soup' },
        { lat: 37.5824, lng: 126.9854, label: 'Bukchon Hanok Village', num: 3, cat: 'attraction', desc: 'Traditional Korean house neighborhood' },
        { lat: 37.5930, lng: 127.0050, label: 'Suyeonsanbang', num: 4, cat: 'attraction', desc: '1930s hanok tea house' },
        { lat: 37.5241, lng: 127.0382, label: 'Mingles', num: 5, cat: 'restaurant', desc: '2-star Michelin modern Korean lunch' },
        { lat: 37.5794, lng: 126.9910, label: 'Changdeokgung Palace', num: 6, cat: 'attraction', desc: 'UNESCO palace — moonlight tour' },
        { lat: 37.5571, lng: 127.0050, label: 'La Yeon', num: 7, cat: 'restaurant', desc: '3-star Michelin Korean fine dining dinner' }
      ]
    },

    // DAY 3 — Itaewon, Yongsan & Omakase
    {
      num: 3,
      title: 'Itaewon, Markets & Omakase',
      description: 'From Seoul\'s oldest market to world-class contemporary art, then sunset at N Seoul Tower and an intimate omakase dinner.',
      neighborhoods: 'Itaewon · Hannam · Yongsan · Namdaemun',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Namdaemun Market',
              description: 'Seoul\'s oldest and largest traditional market (est. 1414). Wander through the maze of 10,000+ vendors selling everything from ginseng to handmade knives. The food alley (kalguksu — knife-cut noodle soup) is a must.',
              details: ['📍 21 Namdaemunno 4-ga, Jung-gu', '🕐 Open early morning, many stalls from 5am', '💡 Galchi jorim (braised hairtail fish) alley is a hidden breakfast gem']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Namdaemun Market Kalguksu Alley',
              description: 'Join the ahjummas at communal tables for hand-cut knife noodles in rich anchovy broth — Seoul\'s most authentic market breakfast. No English menu, no frills, just perfect noodles.',
              meta: '📍 Namdaemun Market, Kalguksu Alley · 💰 ₩8,000-10,000'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Namdaemun is a great contrast to fine dining — experience the full spectrum of Korean food culture.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Leeum Museum of Art',
              description: 'Samsung\'s world-class private art museum in Hannam-dong. Three buildings by Mario Botta, Jean Nouvel, and Rem Koolhaas house Korean national treasures alongside contemporary art. Stunning architecture.',
              details: ['📍 60-16 Itaewon-ro 55-gil, Yongsan-gu', '💰 Free admission · 🕐 10am-6pm (closed Mondays)']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mosu',
              description: 'Chef Ahn Sung-jae\'s boundary-pushing cuisine — Korean ingredients through a European lens, with technique honed at Copenhagen\'s Noma. The tasting menu is an intellectual and sensory journey. Two Michelin stars.',
              meta: '📍 Hannam-dong, Yongsan-gu · 💰 ₩200,000-280,000/person · ⭐⭐ 2 Michelin stars'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hannam-dong & Itaewon Exploration',
              description: 'Stroll through Seoul\'s most cosmopolitan neighborhood. Browse independent boutiques, specialty coffee shops (try Felt Coffee or Center Coffee), and the vibrant Gyeongnidan-gil street.',
              details: ['💡 Antique furniture row on "Itaewon Antique Street" is fascinating', '☕ Seoul has an incredible specialty coffee scene — indulge between meals']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'N Seoul Tower at Sunset',
              description: 'Take the Namsan cable car up to Seoul Tower for panoramic views of the city at golden hour. The observation deck offers 360° views across the entire Seoul basin.',
              details: ['📍 105 Namsangongwon-gil, Yongsan-gu', '💰 Cable car ₩11,000 round trip + observation deck ₩16,000', '🕐 Best at sunset — arrive 30 min before']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kojima',
              description: 'Seoul\'s finest omakase experience. Chef Kojima serves an intimate 20+ course Edomae-style sushi omakase using the best fish flown in from Tsukiji and Korean coastal waters. A counter-only, hushed temple of sushi.',
              meta: '📍 Cheongdam-dong, Gangnam-gu · 💰 ₩250,000-350,000/person · ⭐ 1 Michelin star · ⚠️ Extremely limited seating — book far ahead'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, the Cheongdam-dong area has excellent cocktail bars. Try Le Chamber for a speakeasy experience.' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.5592, lng: 126.9778, label: 'Namdaemun Market', num: 1, cat: 'attraction', desc: 'Seoul\'s oldest market — kalguksu breakfast' },
        { lat: 37.5346, lng: 126.9980, label: 'Leeum Museum of Art', num: 2, cat: 'attraction', desc: 'Samsung\'s world-class art museum' },
        { lat: 37.5340, lng: 127.0000, label: 'Mosu', num: 3, cat: 'restaurant', desc: '2-star Michelin Korean-European lunch' },
        { lat: 37.5345, lng: 126.9940, label: 'Hannam-dong', num: 4, cat: 'attraction', desc: 'Cosmopolitan neighborhood stroll' },
        { lat: 37.5512, lng: 126.9882, label: 'N Seoul Tower', num: 5, cat: 'attraction', desc: 'Panoramic city views at sunset' },
        { lat: 37.5237, lng: 127.0480, label: 'Kojima', num: 6, cat: 'restaurant', desc: 'Top omakase sushi dinner' }
      ]
    },

    // DAY 4 — Hongdae, Jjimjilbang & Farewell Dinner
    {
      num: 4,
      title: 'Hongdae, Spa & Grand Finale',
      description: 'Korean spa culture, indie street art, a 3-star Michelin lunch at Gaon, and a farewell dinner to remember.',
      neighborhoods: 'Hongdae · Mapo · Jung-gu',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dragon Hill Spa (Jjimjilbang)',
              description: 'Experience Korea\'s iconic bathhouse culture at one of Seoul\'s largest jjimjilbangs. Multiple saunas (charcoal, salt, ice), hot pools, outdoor baths, and a rooftop garden. The quintessential Korean wellness experience.',
              details: ['📍 40 Hangang-daero 21na-gil, Yongsan-gu', '💰 ₩15,000-20,000 · 🕐 Open 24 hours', '💡 Go early morning for a serene, uncrowded experience. Spend 2-3 hours.']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Jjimjilbang Eggs & Sikhye',
              description: 'The classic jjimjilbang snack: brown-shelled baked eggs (maekbanseok gyeran) and cold sweet rice drink (sikhye) from the spa\'s snack bar. Authentic Korean comfort.',
              meta: '📍 Inside Dragon Hill Spa · 💰 ₩5,000'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Jjimjilbang etiquette: shower thoroughly before entering pools. Bathing areas are nude and gender-separated. Common areas (saunas, sleeping rooms) are clothed.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Hongdae Creative District',
              description: 'Seoul\'s indie arts and youth culture hub. Street performers, murals, vinyl shops, and independent designers. Walk through the "Picasso Street" and the Hongdae Free Market (weekends) for handmade goods.',
              details: ['📍 Around Hongik University Station exits 8 & 9', '💡 Great for picking up unique souvenirs — handmade ceramics, K-indie vinyl, art prints']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Gaon',
              description: 'Refined traditional Korean cuisine elevated to the highest level. Chef Kim Byoung-jin presents a hansang (full Korean table) course with rare seasonal ingredients — wild herbs, aged kimchi, heirloom grains. Three Michelin stars.',
              meta: '📍 317 Dosan-daero, Gangnam-gu · 💰 ₩250,000-350,000/person · ⭐⭐⭐ 3 Michelin stars · ⚠️ Jacket suggested'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Jogyesa Temple',
              description: 'Seoul\'s chief Buddhist temple and headquarters of the Jogye Order. Beautiful in June with lotus lanterns. A moment of zen before your final evening in Seoul.',
              details: ['📍 55 Ujeongguk-ro, Jongno-gu', '🕐 Open 24 hours · Free admission', '💡 If visiting in early June, the Lotus Lantern Festival decorations may still be up']
            },
            {
              title: 'Insadong Art & Tea Street',
              description: 'Browse galleries, antique shops, and traditional craft stores. Pick up last-minute souvenirs — Korean celadon ceramics, hanji paper goods, or premium teas.',
              details: ['📍 Insadong-gil, Jongno-gu', '💡 Ssamziegil is a fun spiraling open-air mall with artisan shops']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Cocktails at Charles H.',
              description: 'One of Asia\'s best bars, located in the Four Seasons Seoul. Named after diplomat Charles H. Head, it serves impeccable cocktails in a 1920s-inspired speakeasy setting. The perfect pre-dinner aperitif.',
              details: ['📍 Four Seasons Hotel, 97 Saemunan-ro, Jongno-gu', '💰 ₩25,000-35,000 per cocktail', '💡 Named one of Asia\'s 50 Best Bars']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Alla Prima',
              description: 'Chef Kim Tae-yoon\'s French-Korean fine dining — a farewell dinner to remember. The degustation menu marries French technique with Korean ferments and seasonal produce. Intimate 20-seat space. One Michelin star.',
              meta: '📍 Hannam-dong, Yongsan-gu · 💰 ₩180,000-250,000/person · ⭐ 1 Michelin star'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, walk along the Cheonggyecheon Stream — the illuminated urban waterway is beautiful at night and a peaceful end to your Seoul journey.' }
          ]
        }
      ],
      mapPins: [
        { lat: 37.5348, lng: 126.9650, label: 'Dragon Hill Spa', num: 1, cat: 'attraction', desc: 'Iconic jjimjilbang — Korean spa culture' },
        { lat: 37.5568, lng: 126.9234, label: 'Hongdae', num: 2, cat: 'attraction', desc: 'Indie arts & youth culture district' },
        { lat: 37.5245, lng: 127.0400, label: 'Gaon', num: 3, cat: 'restaurant', desc: '3-star Michelin traditional Korean lunch' },
        { lat: 37.5728, lng: 126.9837, label: 'Jogyesa Temple', num: 4, cat: 'attraction', desc: 'Seoul\'s chief Buddhist temple' },
        { lat: 37.5730, lng: 126.9857, label: 'Insadong', num: 5, cat: 'attraction', desc: 'Art galleries & traditional crafts' },
        { lat: 37.5725, lng: 126.9756, label: 'Charles H.', num: 6, cat: 'restaurant', desc: 'Asia\'s 50 Best Bars — cocktails' },
        { lat: 37.5340, lng: 127.0000, label: 'Alla Prima', num: 7, cat: 'restaurant', desc: '1-star Michelin farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (4 nights, luxury hotel)', cost: '$1,200 – $2,400' },
    { category: 'Fine Dining (8 meals at starred restaurants)', cost: '$1,800 – $3,200' },
    { category: 'Casual Meals & Market Food', cost: '$100 – $200' },
    { category: 'Cocktails & Drinks', cost: '$150 – $300' },
    { category: 'Attractions & Admission Fees', cost: '$50 – $100' },
    { category: 'Transportation (AREX, metro, taxis)', cost: '$80 – $150' },
    { category: 'Jjimjilbang & Wellness', cost: '$20 – $40' },
    { category: 'Shopping & Souvenirs', cost: '$200 – $500' },
    { category: 'Total Estimated', cost: '$3,600 – $6,900' },
  ],

  practicalInfo: [
    { title: '✈️ Airport Transfer', items: [
      'AREX express train from Incheon to Seoul Station: 43 min, ₩9,500',
      'KAL Limousine Bus to major hotels: ~₩17,000, 70-90 min',
      'Taxi from airport: ₩65,000-80,000 (international taxi available)'
    ]},
    { title: '📱 Connectivity', items: [
      'Rent a pocket Wi-Fi at Incheon Airport (₩3,000-5,000/day) or buy an eSIM',
      'Korea has blazing fast internet everywhere — even in subway tunnels',
      'Essential apps: KakaoMap (navigation), Kakao T (taxi), Naver Papago (translation), Catch Table (restaurant reservations)'
    ]},
    { title: '🍷 Drinking Culture', items: [
      'Wine lists at fine dining spots are world-class — sommeliers are knowledgeable',
      'Makgeolli (rice wine) pairs beautifully with Korean food',
      'Korean craft beer scene is booming — try local IPAs at taprooms',
      'Soju is ubiquitous at casual spots; premium soju brands worth trying'
    ]},
    { title: '🎌 Reservations Strategy', items: [
      'Book Michelin-starred restaurants 2-4 weeks ahead',
      'La Yeon and Gaon: book via phone or their websites',
      'Jungsik and Mingles: accept online reservations',
      'Some restaurants use Catch Table app (Korean, but navigable with Papago)',
      'Lunch courses are often ₩50,000-100,000 cheaper than dinner — strategic savings'
    ]},
    { title: '🧳 Departure', items: [
      'Jun 8 checkout — AREX back to Incheon Airport',
      'Duty-free shopping at Incheon is excellent (Korean cosmetics, ginseng, soju)',
      'Allow 3 hours before international flights',
      'Tax-free refund counters available at the airport for purchases over ₩30,000'
    ]},
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled!', result);
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
