const fulfillOrder = require('../../functions/fulfill-order');

const order = {
  id: 'order_1773066100350_f1t1mr',
  email: 'kialogy@gmail.com',
  destination: 'Bangkok, Thailand',
  startDate: '2026-06-15',
  endDate: '2026-06-30',
  groupSize: 2,
  requests: 'Try to fit in a Muay Thai experience where I train at great facilities, watch live fights, attend seminars, and get other aspects of Muay Thai, even if I have to visit other cities in Thailand.'
};

const itineraryData = {
  destination: 'Bangkok & Chiang Mai, Thailand',
  countryEmoji: '\u{1F1F9}\u{1F1ED}',
  title: 'The Art of Eight Limbs \u2014 A Muay Thai Odyssey Through Thailand',
  subtitle: '15 days of training, live fights, street food crawls & temple runs across Bangkok and Chiang Mai',
  description: "This isn't a beach holiday with a kickboxing class tacked on. This is a full immersion into Muay Thai \u2014 the ancient Art of Eight Limbs \u2014 woven through Thailand's two greatest cities. You'll train at legendary Bangkok gyms where world champions sharpen their craft, watch warriors clash under the lights at Rajadamnern and Lumpinee stadiums, learn the history and rituals that make this martial art a spiritual discipline, and escape to Chiang Mai's mountain camps for focused training with smaller class sizes. Between sessions, you'll eat your way through Yaowarat's smoky alleys, explore golden temples at dawn, and discover why Thailand's food and fighting culture are two sides of the same coin.",
  duration: '15 days',
  dates: 'Jun 15 \u2013 Jun 30, 2026',
  budget: '$$\u2013$$$',
  pace: 'Active',
  bestFor: 'Couples \u00b7 Adventure Seekers \u00b7 Martial Arts Enthusiasts',
  highlights: [
    "Train at Yokkao Training Center with Saenchai's team in Bangkok",
    "Ringside seats at Rajadamnern Stadium \u2014 the world's oldest Muay Thai venue",
    "Watch elite fights at Lumpinee Stadium on a Saturday night",
    "Deep training immersion at Santai Muay Thai in Chiang Mai",
    "Yaowarat Chinatown midnight street food crawl",
    "Muay Thai history seminar and Wai Kru ceremony lesson",
    "Ayutthaya ancient ruins day trip \u2014 birthplace of Nai Khanomtom legend",
    "Chiang Mai night fights at Thapae Boxing Stadium",
    "Dawn alms offering and Doi Suthep temple visit",
    "Amphawa floating market sunset boat cruise"
  ],
  essentials: [
    {title: '\u{1F94A} Training Essentials', text: 'Bring hand wraps, a mouthguard, and shin guards if you have your own \u2014 otherwise every gym rents or sells quality gear. Wear lightweight shorts and a breathable top. Most sessions are 1.5-2 hours with pad work, bag work, clinching, and sparring (optional). Hydrate aggressively \u2014 Bangkok heat is brutal.'},
    {title: '\u{1F327}\u{FE0F} Monsoon Season', text: "June is early rainy season in Thailand. Expect short, intense afternoon downpours that clear within an hour. Mornings are usually sunny and hot (30-34\u00b0C). Carry a light rain jacket and embrace the drama \u2014 fewer tourists, greener landscapes, and the gyms are less crowded."},
    {title: '\u{1F35C} Street Food Rules', text: "Follow the crowds \u2014 long lines mean fresh, high-turnover food. Point and order \u2014 English menus are rare at the best stalls. Carry cash (20-80 THB per dish). Chinatown (Yaowarat) is the undisputed king of Bangkok street food."},
    {title: '\u{1F687} Getting Around Bangkok', text: "BTS Skytrain and MRT subway cover most tourist areas. Grab (Thai Uber) is cheap and reliable. Tuk-tuks are fun but negotiate first \u2014 100-150 THB for short trips. River boats are fastest for Wat Arun and Grand Palace."},
    {title: '\u2708\u{FE0F} Bangkok to Chiang Mai', text: "Fly AirAsia, Nok Air, or Thai Lion Air \u2014 1 hour, often under 1,500 THB one-way. Trains take 12-14 hours. Fly to maximize training time."},
    {title: '\u{1F4B0} Budget Tips', text: "Muay Thai drop-in: 300-500 THB ($9-15). Weekly: 2,500-5,000 THB. Fight tickets: 1,500-3,000 THB ringside. Street food: 50-150 THB. Mid-range restaurants: 300-800 THB for two."}
  ],
  days: [
    // DAY 1
    {
      num: 1, date: '2026-06-15', neighborhoods: 'Sukhumvit \u00b7 Asoke \u00b7 Nana',
      title: 'Arrival & Bangkok Orientation',
      description: "Land in Bangkok, settle into the Sukhumvit area \u2014 the nerve center for Muay Thai gyms and street food. Get your bearings, grab your first pad thai, and soak in the electrifying chaos of Thailand's capital.",
      timeBlocks: [
        { label: 'Afternoon', activities: [
          { title: 'Arrive at Suvarnabhumi Airport & Transfer to Sukhumvit', description: "Take the Airport Rail Link to Makkasan, then MRT or Grab to your Sukhumvit hotel. This neighbourhood puts you near Yokkao Training Center and Bangkok's best food streets.", details: ['\u2708\uFE0F Airport Rail Link: 45 THB, 30 min to Makkasan', '\uD83C\uDFE8 Stay near BTS Asoke or Phrom Phong', '\uD83D\uDCB1 Exchange at SuperRich (better rates)'] },
          { title: 'Sukhumvit Soi 38 Food Walk', description: "Walk to the famous Soi 38 food stalls and surrounding Thonglor-Ekkamai scene. Mango sticky rice, grilled pork skewers, and boat noodles.", details: ['\uD83C\uDF56 Kor moo yang (grilled pork neck) \u2014 perfect welcome snack', '\uD83E\uDD6D Mango sticky rice season peaks Apr-Jun', '\uD83C\uDF5C Boat noodles \u2014 tiny bowls, huge flavour'] }
        ], tips: [{ type: 'tip', text: 'Jet lag strategy: stay active until 9pm local. The heat keeps you awake.' }] },
        { label: 'Evening', activities: [
          { title: 'Thonglor Neighbourhood Dinner', description: "Thonglor (Soi 55) is Bangkok's trendiest neighbourhood \u2014 craft cocktail bars, izakayas, and incredible Thai restaurants.", details: ['\uD83C\uDF5C Phed Phed \u2014 fiery Isaan food', '\uD83C\uDF7A Craft beer at Hair of the Dog', '\uD83C\uDF19 Comes alive after 8pm'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Supanniga Eating Room (Thonglor)', description: 'Refined Thai-Isaan cuisine in a heritage house. River prawn chu chee and crab fried rice are legendary.', meta: '\uD83D\uDCB0 $$$ \u00b7 \uD83D\uDCCD Soi 55 \u00b7 Reservations recommended' }
        ] }
      ],
      mapPins: [
        { lat: 13.7380, lng: 100.5601, label: 'BTS Asoke Station', num: 1, cat: 'transport', desc: 'BTS/MRT interchange near hotels' },
        { lat: 13.7264, lng: 100.5850, label: 'Sukhumvit Soi 38', num: 2, cat: 'food', desc: 'Famous street food strip' },
        { lat: 13.7318, lng: 100.5791, label: 'Supanniga Eating Room', num: 3, cat: 'food', desc: 'Thai-Isaan cuisine in heritage house' },
        { lat: 13.7304, lng: 100.5820, label: 'Thonglor', num: 4, cat: 'attraction', desc: 'Trendiest neighbourhood' }
      ]
    },
    // DAY 2
    {
      num: 2, date: '2026-06-16', neighborhoods: 'Sukhumvit Soi 16 \u00b7 Phra Nakhon \u00b7 Yaowarat',
      title: 'First Training Session at Yokkao',
      description: "Your Muay Thai journey begins at Yokkao Training Center \u2014 home to legendary fighter Saenchai. Morning pad work and technique drills. Afternoon recovery with Thai massage at Wat Pho. Evening Chinatown food crawl.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Yokkao Training Center \u2014 Session 1', description: "Your first real session. World-class facility. Fundamentals: stance, jab-cross combos, roundhouse kicks, basic clinch work. Trainers are incredibly patient with beginners.", details: ['\uD83E\uDD4A Session: 7:30-9:30am (arrive 15 min early)', '\uD83D\uDCB0 Drop-in: ~400 THB, weekly: ~3,500 THB', '\uD83C\uDFCB\uFE0F Gear rental available', '\uD83D\uDCCD Sukhumvit Soi 16, 5 min from BTS Asoke'] }
        ], meals: [
          { type: '\u2615 Breakfast', name: 'Roast Coffee & Eatery', description: "Strong coffee and pad krapao (basil pork rice) \u2014 the fighter's breakfast.", meta: '\uD83D\uDCB0 $ \u00b7 Near BTS Asoke' }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Thai Massage Recovery at Wat Pho', description: "Home of the reclining Buddha AND Thailand's most famous massage school. Proper Thai massage from traditionally trained practitioners.", details: ['\uD83D\uDC86 Thai massage: 260 THB/30 min, 420 THB/60 min', '\uD83D\uDE4F Reclining Buddha: 46m long, gold leaf', '\uD83C\uDFDB\uFE0F Temple entry: 200 THB'] }
        ], tips: [{ type: 'tip', text: "Thai massage after training is a fighter tradition \u2014 speeds recovery and loosens tight hips. Don't skip it." }] },
        { label: 'Evening', activities: [
          { title: 'Yaowarat (Chinatown) Street Food Crawl', description: "Yaowarat Road transforms into Bangkok's greatest open-air food hall at sunset. Follow neon signs and charcoal smoke through the sois.", details: ['\uD83E\uDDAA Nai Ek Roll Noodle \u2014 legendary', '\uD83D\uDD25 Grilled seafood on Soi Texas', '\uD83C\uDF5C Jek Pui curry rice \u2014 70 years old'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'T&K Seafood (Yaowarat)', description: "Orange-plastic-chair institution. Grilled river prawns, crab omelets, tom yum. Cash only, always packed.", meta: '\uD83D\uDCB0 $$ \u00b7 Yaowarat Rd \u00b7 Open from 5pm' }
        ] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao Training Center', num: 1, cat: 'muaythai', desc: 'World-class Muay Thai gym' },
        { lat: 13.7462, lng: 100.4928, label: 'Wat Pho', num: 2, cat: 'attraction', desc: 'Reclining Buddha & massage school' },
        { lat: 13.7403, lng: 100.5073, label: 'Yaowarat Road', num: 3, cat: 'food', desc: 'Chinatown street food strip' },
        { lat: 13.7392, lng: 100.5082, label: 'T&K Seafood', num: 4, cat: 'food', desc: 'Legendary Chinatown seafood' },
        { lat: 13.7385, lng: 100.5065, label: 'Nai Ek Roll Noodle', num: 5, cat: 'food', desc: 'Famous rolled noodle soup' }
      ]
    },
    // DAY 3
    {
      num: 3, date: '2026-06-17', neighborhoods: 'Ratchadamnoen \u00b7 Banglamphu \u00b7 Phra Nakhon',
      title: 'Rajadamnern Stadium Fight Night',
      description: "Morning training, afternoon exploring Bangkok's royal district with Grand Palace and Wat Arun. Tonight \u2014 live Muay Thai at Rajadamnern Stadium, the world's oldest venue, operating since 1945.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Yokkao \u2014 Session 2', description: "Kick technique day: teep (push kick), devastating roundhouse, and first clinch work \u2014 the grueling close-range battle that separates Muay Thai from all other striking arts.", details: ['\uD83E\uDD4A Focus: teep, roundhouse, basic clinch', '\uD83C\uDFCB\uFE0F Conditioning: jump rope, planks, sprints', '\uD83D\uDCA6 Bring 2 litres of water'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Grand Palace & Wat Phra Kaew', description: "Thailand's most sacred landmark. Emerald Buddha, ornate throne halls, and centuries of royal history.", details: ['\uD83C\uDFDB\uFE0F Entry: 500 THB', '\uD83D\uDC54 Dress code: cover shoulders and knees', '\uD83D\uDCF8 Murals are extraordinary'] },
          { title: 'Wat Arun & Riverside', description: "Cross the Chao Phraya by ferry to the Temple of Dawn. Climb the central prang for panoramic river views.", details: ['\uD83D\uDEA5 Cross-river ferry: 4 THB', '\uD83C\uDFDB\uFE0F Entry: 100 THB'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Jay Fai', description: "World's only Michelin-starred street food. Crab omelets and drunken noodles over charcoal fire. Book weeks ahead.", meta: '\uD83D\uDCB0 $$$$ \u00b7 327 Maha Chai Rd' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Rajadamnern Stadium \u2014 Live Muay Thai', description: "The cathedral of Muay Thai since 1945. Dome projection, live orchestra (pi Java, drums, cymbals), and Wai Kru ritual dance before each fight create an atmosphere unlike anything in sports.", details: ['\uD83C\uDF9F\uFE0F Tickets: 1,500-3,000 THB (rajadamnern.com)', '\u23F0 Wed fights: 6pm-9pm, ~8 bouts', '\uD83C\uDFB5 Orchestra speeds up as fights intensify', '\uD83D\uDCF8 Photography allowed \u2014 cinematic lighting'] }
        ], tips: [{ type: 'tip', text: "Book ringside seats online a week ahead. Wednesday card features competition-level fighters, not tourist shows." }] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao Training Center', num: 1, cat: 'muaythai', desc: 'Morning training' },
        { lat: 13.7516, lng: 100.4910, label: 'Grand Palace', num: 2, cat: 'attraction', desc: 'Most sacred royal compound' },
        { lat: 13.7437, lng: 100.4888, label: 'Wat Arun', num: 3, cat: 'attraction', desc: 'Temple of Dawn' },
        { lat: 13.7528, lng: 100.5058, label: 'Jay Fai', num: 4, cat: 'food', desc: 'Michelin-starred street food' },
        { lat: 13.7630, lng: 100.5108, label: 'Rajadamnern Stadium', num: 5, cat: 'muaythai', desc: 'World\'s oldest Muay Thai stadium' }
      ]
    },
    // DAY 4
    {
      num: 4, date: '2026-06-18', neighborhoods: 'On Nut \u00b7 Phra Khanong \u00b7 Bang Krachao',
      title: "Attachai Gym & Bangkok's Green Lung",
      description: "Train at Attachai Muay Thai, run by a 3x Lumpinee champion with 200 fights and 180 wins. Intimate, technical, beloved by serious practitioners. Afternoon cycling through Bang Krachao, Bangkok's hidden jungle.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Attachai Muay Thai Gym', description: "Attachai Fairtex is a former Lumpinee champion. Smaller and more personal \u2014 serious one-on-one attention and detailed technique corrections. A genuine fighter's atmosphere.", details: ['\uD83E\uDD4A Morning: 7:00-9:00am', '\uD83D\uDCB0 Drop-in: ~350 THB', '\uD83D\uDCCD On Nut Soi 36 \u2014 BTS On Nut', '\uD83C\uDFC6 Record: 200 fights, 180 wins'] }
        ], meals: [
          { type: '\u2615 Breakfast', name: 'Joke Prince', description: "Thai rice congee with pork, century egg, and crispy garlic \u2014 the classic fighter breakfast.", meta: '\uD83D\uDCB0 $ \u00b7 On Nut area' }
        ] },
        { label: 'Afternoon', activities: [
          { title: "Bang Krachao \u2014 Bangkok's Green Lung", description: "Hire bikes and explore a massive jungle-covered peninsula in the Chao Phraya. Elevated boardwalks through mangroves, hidden temples, family-run gardens.", details: ['\uD83D\uDEB2 Bike rental: 100 THB/day', '\uD83D\uDEA5 Long-tail boat from Khlong Toei: 10 THB', '\uD83C\uDF3F Bangkok Tree House \u2014 eco caf\u00e9 in jungle canopy'] }
        ] },
        { label: 'Evening', activities: [
          { title: 'Victory Monument Street Food', description: "Where locals eat after work \u2014 boat noodles, pad thai, and Isaan food in a dizzying ring of stalls.", details: ['\uD83C\uDF5C Boat noodles: 15 THB/bowl, order 5-10', '\uD83D\uDC14 Gai yang (grilled chicken)', '\uD83C\uDF61 Moo ping (pork skewers) \u2014 10 THB each'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Boat Noodle Alley', description: "Tiny bowls of intensely flavoured pork blood broth noodles. Stack bowls as you go \u2014 it's tradition.", meta: '\uD83D\uDCB0 $ \u00b7 Victory Monument BTS' }
        ] }
      ],
      mapPins: [
        { lat: 13.7095, lng: 100.6012, label: 'Attachai Muay Thai', num: 1, cat: 'muaythai', desc: '3x Lumpinee champion gym' },
        { lat: 13.6920, lng: 100.5730, label: 'Bang Krachao', num: 2, cat: 'attraction', desc: 'Green Lung \u2014 jungle cycling' },
        { lat: 13.7649, lng: 100.5381, label: 'Victory Monument', num: 3, cat: 'food', desc: 'Street food hub' },
        { lat: 13.7100, lng: 100.5990, label: 'Joke Prince', num: 4, cat: 'food', desc: 'Fighter breakfast congee' }
      ]
    },
    // DAY 5
    {
      num: 5, date: '2026-06-19', neighborhoods: 'Siam \u00b7 Silom \u00b7 Sathorn',
      title: 'Training, Gear Shopping & Silom Nightlife',
      description: "Morning session at Yokkao, then Bangkok's Muay Thai retail scene \u2014 fight shorts and gloves at MBK. Jim Thompson House for culture. Evening at Silom's rooftop bars.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Yokkao \u2014 Session 3', description: "Mid-week session. Your body is adapting \u2014 roundhouse feels natural, teep has snap. Today: combination work, counter techniques, and longer clinch rounds.", details: ['\uD83E\uDD4A Focus: combos, counters, extended clinch', '\uD83C\uDFCB\uFE0F Ice your shins after every session', '\uD83D\uDCAA Ask about the Superman punch'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Muay Thai Gear Shopping \u2014 MBK Center', description: "Budget Muay Thai gear at MBK, premium at Yokkao Store. Thai-made fight gear is far cheaper here.", details: ['\uD83D\uDECD\uFE0F MBK: shorts from 200 THB, gloves from 800 THB', '\uD83E\uDD4A Yokkao Store: premium shorts 1,500-2,500 THB', '\uD83C\uDDF9\uD83C\uDDED Also: Fairtex, Twins Special, Top King'] },
          { title: 'Jim Thompson House', description: "Teak house museum of the American spy-turned-silk-king. Lush tropical garden and traditional Thai architecture.", details: ['\uD83C\uDFE0 Entry: 200 THB \u00b7 Guided tours every 20 min', '\uD83D\uDCCD Near BTS National Stadium'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Som Tam Nua', description: "Legendary papaya salad. Crispy soft-shell crab salad and larb. Always has a queue.", meta: '\uD83D\uDCB0 $$ \u00b7 Siam Square Soi 5' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Rooftop Drinks & Silom Night', description: "Bangkok's rooftop bar scene from 60 stories high. Patpong Night Market for souvenirs.", details: ['\uD83C\uDF78 Sky Bar at Lebua \u2014 The Hangover II location', '\uD83C\uDF03 Vertigo & Moon Bar \u2014 360\u00b0 views', '\uD83D\uDECD\uFE0F Patpong Night Market'] }
        ], meals: [
          { type: '\uD83C\uDF77 Dinner', name: 'Nahm (COMO Metropolitan)', description: "One of Bangkok's finest. Exquisite royal Thai cuisine you won't find at street stalls.", meta: '\uD83D\uDCB0 $$$$ \u00b7 Sathorn \u00b7 Reservations essential' }
        ] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao Training Center', num: 1, cat: 'muaythai', desc: 'Morning combos and counters' },
        { lat: 13.7446, lng: 100.5300, label: 'MBK Center', num: 2, cat: 'shopping', desc: 'Muay Thai gear shopping' },
        { lat: 13.7500, lng: 100.5277, label: 'Jim Thompson House', num: 3, cat: 'attraction', desc: 'Silk king museum' },
        { lat: 13.7455, lng: 100.5340, label: 'Som Tam Nua', num: 4, cat: 'food', desc: 'Legendary papaya salad' },
        { lat: 13.7218, lng: 100.5254, label: 'Sky Bar (Lebua)', num: 5, cat: 'food', desc: 'Iconic rooftop bar' },
        { lat: 13.7242, lng: 100.5412, label: 'Nahm', num: 6, cat: 'food', desc: 'Royal Thai fine dining' }
      ]
    },
    // DAY 6
    {
      num: 6, date: '2026-06-20', neighborhoods: 'Lumphini \u00b7 Ratchada \u00b7 Ram Intra',
      title: 'Lumpinee Stadium Saturday Night',
      description: "Light training morning, Lumphini Park and Jodd Fairs. Tonight \u2014 Saturday night fights at Lumpinee Boxing Stadium, the other great cathedral of Muay Thai where champions are crowned.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Yokkao \u2014 Light Recovery Session', description: "Recovery-focused: technique review, shadow boxing, light pad work. Trainers know you have a big night ahead.", details: ['\uD83E\uDD4A Technique refinement, shadow boxing', '\uD83E\uDDD8 Stretch and mobility work', '\uD83D\uDC86 Optional ice bath'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Lumphini Park', description: "Bangkok's Central Park. Paddle boats on the lake, monitor lizards on the banks, tai chi under shady trees.", details: ['\uD83C\uDF3F Free entry \u00b7 Open 5am-9pm', '\uD83E\uDD8E Giant monitor lizards \u2014 harmless', '\uD83D\uDEA3 Paddle boats: 40 THB/30 min'] },
          { title: 'Jodd Fairs Night Market', description: "Bangkok's trendiest night market. 700+ stalls of street food, vintage clothing, craft cocktails. The seafood section alone is worth it.", details: ['\uD83D\uDCCD MRT Thailand Cultural Centre', '\uD83E\uDD91 Giant grilled squid and rainbow crepes', '\uD83C\uDF7A Craft beer bars throughout'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Baan Somtum', description: "Upscale Isaan dining with inventive som tam variations. Try crab version with salted egg.", meta: '\uD83D\uDCB0 $$ \u00b7 Silom area' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Lumpinee Stadium \u2014 Saturday Night Fights', description: "Lumpinee is the other crown jewel. A Lumpinee belt is the most coveted prize in the sport. Saturday nights feature headline bouts with Thailand's top-ranked fighters.", details: ['\uD83C\uDF9F\uFE0F Tickets: 1,500-3,000 THB', '\u23F0 Fights from ~6pm', '\uD83C\uDFC6 Look for title fights', '\uD83D\uDCCD Ram Intra Rd \u2014 30 min Grab from Sukhumvit'] }
        ], tips: [{ type: 'tip', text: "Lumpinee is further from central Bangkok. Book a Grab both ways. The rawer, more authentic atmosphere is worth the trip." }] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao Training Center', num: 1, cat: 'muaythai', desc: 'Light recovery session' },
        { lat: 13.7310, lng: 100.5415, label: 'Lumphini Park', num: 2, cat: 'attraction', desc: 'Paddle boats and lizards' },
        { lat: 13.7580, lng: 100.5670, label: 'Jodd Fairs', num: 3, cat: 'food', desc: 'Trendiest night market' },
        { lat: 13.8745, lng: 100.6280, label: 'Lumpinee Stadium', num: 4, cat: 'muaythai', desc: 'Crown jewel of Muay Thai' }
      ]
    },
    // DAY 7
    {
      num: 7, date: '2026-06-21', neighborhoods: 'Ayutthaya \u00b7 Bang Pa-In',
      title: 'Ayutthaya \u2014 Birthplace of Muay Thai Legend',
      description: "Day trip to the ancient capital of Siam \u2014 where Nai Khanomtom, the father of Muay Thai, was captured by the Burmese in 1767. Explore UNESCO ruins and learn the martial art's origin story.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Train to Ayutthaya', description: "Scenic 90-minute ride through Thai countryside from Hua Lamphong. The ancient capital was once the largest city in the world.", details: ['\uD83D\uDE82 Train: 20 THB, ~6:30am from Hua Lamphong', '\uD83D\uDEFA Hire tuk-tuk at station: 200-300 THB half-day'] },
          { title: 'Wat Mahathat \u2014 Buddha Head in Tree', description: "The most photographed image in Ayutthaya \u2014 a stone Buddha head entwined in banyan roots. The temple was the seat of the Supreme Patriarch.", details: ['\uD83D\uDCF8 Iconic tree-root Buddha head', '\uD83C\uDFDB\uFE0F Entry: 50 THB', '\u23F0 Go early for fewer crowds'] }
        ], meals: [
          { type: '\u2615 Brunch', name: 'Baan Kao Nhom', description: "Traditional Thai dessert house in a century-old wooden building. Try roti sai mai \u2014 Ayutthaya's signature hand-pulled cotton candy crepes.", meta: '\uD83D\uDCB0 $ \u00b7 Riverside' }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Wat Phra Si Sanphet & Royal Ruins', description: "The most important temple in the royal palace complex. Three magnificent chedis contain the ashes of Ayutthaya's kings.", details: ['\uD83C\uDFDB\uFE0F Entry: 50 THB', '\uD83D\uDCF8 Three chedis are the iconic silhouette'] },
          { title: 'Nai Khanomtom & Muay Thai Origins', description: "Learn the legend of Nai Khanomtom \u2014 the Thai prisoner who defeated 10 Burmese warriors in unarmed combat in 1774 and won his freedom. This is the origin story of Muay Thai. March 17 is National Muay Thai Day in his honour.", details: ['\uD83E\uDD4A Father of Muay Thai', '\uD83D\uDCDC Captured during fall of Ayutthaya 1767', '\uD83C\uDFDB\uFE0F His legacy shaped Muay Thai into a national art'] }
        ] },
        { label: 'Evening', activities: [
          { title: 'Sunset at Wat Chai Watthanaram & Return', description: "End at the most photogenic temple \u2014 Khmer-style on the riverbank. Sunset light on the prangs is breathtaking. Evening train back to Bangkok.", details: ['\uD83C\uDF05 Entry: 50 THB \u00b7 Best at golden hour', '\uD83D\uDE82 Return trains until ~8pm'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Raan Khun Phor', description: "Riverside restaurant famous for giant river prawn dishes and tom yum. Perfect end to a historic day.", meta: '\uD83D\uDCB0 $$ \u00b7 Ayutthaya riverside' }
        ] }
      ],
      mapPins: [
        { lat: 14.3577, lng: 100.5684, label: 'Wat Mahathat', num: 1, cat: 'attraction', desc: 'Buddha head in banyan roots' },
        { lat: 14.3543, lng: 100.5554, label: 'Wat Phra Si Sanphet', num: 2, cat: 'attraction', desc: 'Three royal chedis' },
        { lat: 14.3428, lng: 100.5479, label: 'Wat Chai Watthanaram', num: 3, cat: 'attraction', desc: 'Khmer-style sunset temple' },
        { lat: 14.3560, lng: 100.5600, label: 'Ayutthaya Historical Park', num: 4, cat: 'attraction', desc: 'UNESCO World Heritage ruins' },
        { lat: 14.3550, lng: 100.5620, label: 'Raan Khun Phor', num: 5, cat: 'food', desc: 'Riverside river prawn restaurant' }
      ]
    },
    // DAY 8
    {
      num: 8, date: '2026-06-22', neighborhoods: 'Amphawa \u00b7 Mae Klong \u00b7 Samut Songkhram',
      title: 'Floating Markets & Rest Day',
      description: "Active recovery day. Visit the famous Amphawa Floating Market and the Instagram-famous Mae Klong Railway Market where trains pass through the vendor stalls. Evening back in Bangkok for Wai Kru ceremony class.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Mae Klong Railway Market (Talad Rom Hup)', description: "The famous market where vendors pull back their awnings seconds before a train passes through. The train literally squeezes through the market stalls \u2014 it's surreal.", details: ['\uD83D\uDE82 Trains pass ~8:30am, 11:10am, 2:30pm, 5:30pm', '\uD83D\uDCCD 80km southwest of Bangkok \u2014 1.5h by car', '\uD83D\uDCF8 Arrive 30 min before train for best spot'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Amphawa Floating Market', description: "The most authentic floating market near Bangkok. Wooden boats sell pad thai, grilled seafood, and coconut ice cream on the canal. Less touristy than Damnoen Saduak and far more charming.", details: ['\uD83D\uDEA3 Open Fri-Sun, 12pm-8pm', '\uD83E\uDD90 Grilled river prawns from the boats', '\uD83E\uDD65 Coconut ice cream in coconut shells', '\uD83D\uDEF6 Firefly boat tours at dusk (seasonal)'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Amphawa Canal Boat Food', description: "Eat directly from the boats. Point at what looks good \u2014 grilled seafood, noodles, mango sticky rice. Sit on the canal edge with your feet dangling.", meta: '\uD83D\uDCB0 $ \u00b7 Pay each boat vendor directly' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Wai Kru Ceremony & Muay Thai Culture Class', description: "Back in Bangkok, attend a special Wai Kru ceremony class \u2014 learn the pre-fight ritual dance that every Muay Thai fighter performs. The Wai Kru pays respect to teachers, family, and the art itself. It's a spiritual practice, not just choreography.", details: ['\uD83D\uDE4F Wai Kru: the ritual dance before every fight', '\uD83C\uDFB5 Performed to the live orchestra music', '\uD83E\uDD4A Most gyms offer cultural sessions on request', '\uD83D\uDCB0 Usually included in training package or ~300 THB extra'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Krua Apsorn (Samsen)', description: "Legendary shophouse restaurant near Khao San. Famous for crab curry and stir-fried morning glory. A favourite of Thai royalty.", meta: '\uD83D\uDCB0 $$ \u00b7 Samsen Rd \u00b7 Closes at 8pm' }
        ] }
      ],
      mapPins: [
        { lat: 13.4098, lng: 99.9999, label: 'Mae Klong Railway Market', num: 1, cat: 'attraction', desc: 'Train passes through market stalls' },
        { lat: 13.4263, lng: 99.9527, label: 'Amphawa Floating Market', num: 2, cat: 'food', desc: 'Most authentic floating market' },
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao (Wai Kru class)', num: 3, cat: 'muaythai', desc: 'Wai Kru ceremony lesson' },
        { lat: 13.7605, lng: 100.5027, label: 'Krua Apsorn', num: 4, cat: 'food', desc: 'Royal-favourite crab curry' }
      ]
    },
    // DAY 9
    {
      num: 9, date: '2026-06-23', neighborhoods: 'Sukhumvit \u00b7 Khlong Toei \u00b7 Bang Rak',
      title: 'Muay Thai Seminar & Bang Rak Food Tour',
      description: "A special day: morning Muay Thai seminar or masterclass with a former champion covering advanced techniques, fight strategy, and the philosophy behind the art. Afternoon exploring Bang Rak \u2014 Bangkok's oldest neighbourhood and food paradise.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Muay Thai Technique Seminar', description: "Many Bangkok gyms host weekly seminars or masterclasses with visiting champions. Today's focus: fight strategy, reading opponents, and the mental game. Learn what separates a fighter from someone who just trains.", details: ['\uD83E\uDD4A Seminars cover strategy, not just technique', '\uD83E\uDDE0 Mental game: reading feints, controlling distance', '\uD83D\uDCB0 Usually 500-1,000 THB for special sessions', '\uD83D\uDCCD Check Yokkao or Evolve MMA schedules'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Bang Rak Food Walking Tour', description: "Bangkok's oldest neighbourhood is a food goldmine. Walk through narrow sois past century-old shophouses, Chinese temples, and some of the city's most revered food stalls.", details: ['\uD83C\uDF5C Muslim Restaurant (halal Thai food since 1947)', '\uD83E\uDD6B Nai Mong Hoi Tod \u2014 crispy oyster omelets', '\uD83C\uDF75 Old-school coffee shops with kopi', '\uD83D\uDCCD Start at BTS Saphan Taksin and walk north'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Nai Mong Hoi Tod', description: "Bangkok's best crispy oyster and mussel omelets. A 70-year institution near the river. Massive portions.", meta: '\uD83D\uDCB0 $ \u00b7 Charoen Krung Rd' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Riverside Dinner at Asiatique', description: "The night bazaar by the river. Ferris wheel, riverside dining, and a free shuttle boat from Saphan Taksin. More upscale than street markets but great atmosphere.", details: ['\uD83D\uDEA2 Free shuttle boat from BTS Saphan Taksin', '\uD83C\uDFA1 Giant Ferris wheel with river views', '\uD83C\uDF5C Viva 8 for Thai seafood by the river'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Viva 8 (Asiatique)', description: "Thai-Chinese seafood right on the river. The steamed sea bass in lime and the pepper crab are outstanding. Great view of Wat Arun lit up at night.", meta: '\uD83D\uDCB0 $$$ \u00b7 Asiatique riverfront' }
        ] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao (Seminar)', num: 1, cat: 'muaythai', desc: 'Technique seminar with champion' },
        { lat: 13.7278, lng: 100.5138, label: 'Bang Rak', num: 2, cat: 'food', desc: "Bangkok's oldest food neighbourhood" },
        { lat: 13.7270, lng: 100.5130, label: 'Nai Mong Hoi Tod', num: 3, cat: 'food', desc: 'Best oyster omelets in Bangkok' },
        { lat: 13.7073, lng: 100.5014, label: 'Asiatique', num: 4, cat: 'attraction', desc: 'Riverside night bazaar' }
      ]
    },
    // DAY 10 - Fly to Chiang Mai
    {
      num: 10, date: '2026-06-24', neighborhoods: 'Chiang Mai Old City \u00b7 Tha Phae',
      title: 'Fly to Chiang Mai \u2014 Mountain Camp Begins',
      description: "Leave Bangkok's heat for Chiang Mai's mountain cool. Settle into the Old City, explore ancient temples within the moat walls, and prep for three days of immersive Muay Thai training at Santai Gym.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Fly Bangkok to Chiang Mai', description: "1-hour flight from Don Mueang or Suvarnabhumi to Chiang Mai. Arrive by late morning and transfer to your Old City guesthouse. The pace shift from Bangkok is immediate \u2014 quieter, cooler, greener.", details: ['\u2708\uFE0F AirAsia/Nok Air: 1,000-1,500 THB one-way', '\uD83D\uDE95 Airport to Old City: 150 THB by songthaew', '\uD83C\uDFE8 Stay inside or near the Old City moat'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Chiang Mai Old City Temple Walk', description: "Explore the ancient walled city. Within the moat are over 30 temples dating back to the Lanna Kingdom. Walk between golden stupas, discover hidden monk chats, and feel the spiritual calm.", details: ['\uD83C\uDFDB\uFE0F Wat Chedi Luang \u2014 massive 15th-century chedi', '\uD83C\uDFDB\uFE0F Wat Phra Singh \u2014 most revered in the city', '\uD83D\uDE4F Monk Chat programs at several temples', '\uD83D\uDEB6 The entire Old City is walkable'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Khao Soi Mae Sai', description: "Your first bowl of Chiang Mai's signature dish \u2014 khao soi. Coconut curry broth with egg noodles, crispy noodles on top, and your choice of chicken or beef. Absolutely life-changing.", meta: '\uD83D\uDCB0 $ \u00b7 Near Tha Phae Gate' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Tha Phae Gate Area & Night Bazaar', description: "The eastern gate of the Old City is the social hub of Chiang Mai. Street performers, food vendors, and the famous Night Bazaar stretching along Chang Khlan Road.", details: ['\uD83C\uDFEA Night Bazaar: handicrafts, hill tribe textiles', '\uD83C\uDF5C Street food stalls line the road', '\uD83D\uDCCD Walking distance from most Old City hotels'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Huen Phen', description: "Classic northern Thai restaurant in a beautiful old teak house. Try the nam prik ong (chili dip), sai oua (northern sausage), and khao soi.", meta: '\uD83D\uDCB0 $$ \u00b7 Rachamankha Rd, Old City' }
        ] }
      ],
      mapPins: [
        { lat: 18.7883, lng: 98.9853, label: 'Tha Phae Gate', num: 1, cat: 'attraction', desc: 'Eastern gate of Old City' },
        { lat: 18.7883, lng: 98.9867, label: 'Wat Chedi Luang', num: 2, cat: 'attraction', desc: 'Massive 15th-century chedi' },
        { lat: 18.7893, lng: 98.9817, label: 'Wat Phra Singh', num: 3, cat: 'attraction', desc: 'Most revered Chiang Mai temple' },
        { lat: 18.7870, lng: 98.9930, label: 'Khao Soi Mae Sai', num: 4, cat: 'food', desc: 'Life-changing khao soi' },
        { lat: 18.7870, lng: 98.9850, label: 'Huen Phen', num: 5, cat: 'food', desc: 'Classic northern Thai teak house' }
      ]
    },
    // DAY 11
    {
      num: 11, date: '2026-06-25', neighborhoods: 'Chiang Mai \u00b7 Santai Muay Thai',
      title: 'Santai Muay Thai \u2014 Mountain Training Day 1',
      description: "Full immersion begins. Two-a-day training at Santai Muay Thai Gym in Chiang Mai \u2014 morning and afternoon sessions. Santai is known for smaller classes, personal attention, and authentic training methods. Between sessions, explore Chiang Mai's coffee culture.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Santai Muay Thai \u2014 Morning Session', description: "Santai is a respected Chiang Mai gym with experienced trainers who teach all levels. The mountain air and smaller class sizes make for a completely different training experience compared to Bangkok. Morning: shadow boxing, heavy bag, pad work, clinch.", details: ['\uD83E\uDD4A Session: 7:30-9:30am', '\uD83D\uDCB0 Drop-in: ~350 THB, weekly: ~2,500 THB', '\uD83D\uDCCD Near Old City \u2014 easy to reach', '\uD83C\uDF21\uFE0F Cooler than Bangkok \u2014 24-30\u00b0C'] }
        ], meals: [
          { type: '\u2615 Breakfast', name: 'Ristr8to Lab', description: "World-class specialty coffee. Ristr8to's latte art won global championships. Pair with a Thai-style toast set. Perfect post-training fuel.", meta: '\uD83D\uDCB0 $$ \u00b7 Nimman area' }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Santai \u2014 Afternoon Session', description: "Second session: technique drilling, sparring (optional), and focused clinch work. The afternoon heat in Chiang Mai is more manageable than Bangkok. Push yourself \u2014 this is what you came for.", details: ['\uD83E\uDD4A Session: 3:30-5:30pm', '\uD83E\uDD3C Optional light sparring', '\uD83D\uDCA7 Stay hydrated between sessions', '\uD83D\uDC86 Recovery massage available nearby'] }
        ] },
        { label: 'Evening', activities: [
          { title: 'Nimman Road (Nimmanhaemin)', description: "Chiang Mai's hipster neighbourhood. Trendy caf\u00e9s, boutique shops, art galleries, and excellent restaurants line this tree-shaded road. Less chaotic than Bangkok \u2014 more walkable and relaxed.", details: ['\u2615 Some of Thailand\u2019s best coffee shops', '\uD83C\uDFA8 Art galleries and design shops', '\uD83C\uDF7A Craft beer at Brewery and Let The Boy Die'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Cherng Doi Roast Chicken', description: "No-frills institution. Perfectly charcoal-roasted chicken with sticky rice, som tam, and Isaan-style dipping sauces. The best simple Thai meal you'll have.", meta: '\uD83D\uDCB0 $ \u00b7 Multiple locations \u00b7 Cash only' }
        ] }
      ],
      mapPins: [
        { lat: 18.7920, lng: 98.9760, label: 'Santai Muay Thai', num: 1, cat: 'muaythai', desc: 'Mountain Muay Thai gym' },
        { lat: 18.7975, lng: 98.9674, label: 'Ristr8to Lab', num: 2, cat: 'food', desc: 'World-champion latte art coffee' },
        { lat: 18.7980, lng: 98.9680, label: 'Nimman Road', num: 3, cat: 'attraction', desc: 'Hipster neighbourhood' },
        { lat: 18.7930, lng: 98.9730, label: 'Cherng Doi', num: 4, cat: 'food', desc: 'Perfect charcoal roast chicken' }
      ]
    },
    // DAY 12
    {
      num: 12, date: '2026-06-26', neighborhoods: 'Chiang Mai \u00b7 Doi Suthep',
      title: 'Training Day 2 & Doi Suthep Temple',
      description: "Morning training at Santai, then ascend Doi Suthep \u2014 the sacred mountain temple that watches over Chiang Mai. 309 steps flanked by naga serpents lead to a golden chedi with panoramic views of the city below.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Santai Muay Thai \u2014 Session 2', description: "Day 2 at Santai. Your technique is sharper, your conditioning is building. Today the trainers push you on timing and distance management \u2014 the subtle art of controlling the space between you and your opponent.", details: ['\uD83E\uDD4A Focus: timing, distance, footwork', '\uD83C\uDFCB\uFE0F Clinch drills with partner', '\uD83D\uDCAA You\'re noticeably better than day 1'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Doi Suthep Temple', description: "Chiang Mai's most sacred site. Climb 309 steps flanked by naga serpent balustrades to a glittering golden chedi at 1,000m elevation. The panoramic view of the city and the spiritual atmosphere are unforgettable.", details: ['\uD83C\uDFDB\uFE0F Entry: 30 THB', '\uD83E\uDD7E 309 steps or take the funicular', '\uD83D\uDE4F Walk clockwise around the golden chedi', '\uD83C\uDF05 Best views on clear mornings or late afternoon'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Khao Soi Khun Yai', description: "Arguably the best khao soi in Chiang Mai. This humble shop near the Old City has been serving the coconut curry noodle masterpiece for decades.", meta: '\uD83D\uDCB0 $ \u00b7 Sri Poom Rd' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Thapae Boxing Stadium \u2014 Chiang Mai Fights', description: "Chiang Mai's most accessible fight venue. Nightly fights (except Sunday) from 9pm. The atmosphere is intimate and raw \u2014 closer to how Muay Thai has always been watched in Thailand.", details: ['\uD83C\uDF9F\uFE0F Tickets: 400-600 THB', '\u23F0 Fights: 9pm-midnight, 5-6 bouts', '\uD83D\uDCCD Near the Night Bazaar', '\uD83C\uDF7A Beer available \u2014 casual atmosphere'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'SP Chicken (Samoe Jai)', description: "The most famous grilled chicken in Chiang Mai. Fall-off-the-bone tender with a sweet chili glaze. Get the sticky rice and som tam combo.", meta: '\uD83D\uDCB0 $ \u00b7 Samoe Jai intersection \u00b7 Queue expected' }
        ] }
      ],
      mapPins: [
        { lat: 18.7920, lng: 98.9760, label: 'Santai Muay Thai', num: 1, cat: 'muaythai', desc: 'Morning training \u2014 timing and distance' },
        { lat: 18.8048, lng: 98.9217, label: 'Doi Suthep Temple', num: 2, cat: 'attraction', desc: 'Sacred mountain temple with 309 steps' },
        { lat: 18.7930, lng: 98.9850, label: 'Khao Soi Khun Yai', num: 3, cat: 'food', desc: "Best khao soi in Chiang Mai" },
        { lat: 18.7870, lng: 98.9920, label: 'Thapae Boxing Stadium', num: 4, cat: 'muaythai', desc: 'Nightly Chiang Mai fights' },
        { lat: 18.7910, lng: 98.9870, label: 'SP Chicken', num: 5, cat: 'food', desc: 'Famous grilled chicken' }
      ]
    },
    // DAY 13
    {
      num: 13, date: '2026-06-27', neighborhoods: 'Chiang Mai \u00b7 Chiang Dao \u00b7 Mae Rim',
      title: 'Final Training & Chiang Mai Adventure',
      description: "Last training session at Santai \u2014 give everything you've got. Afternoon adventure: choose between the Chiang Dao Cave, a Thai cooking class, or Bua Tong sticky waterfall (unique in the world). Evening celebrating at a Chiang Mai craft beer spot.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Santai Muay Thai \u2014 Final Session', description: "Your last training session in Thailand. The trainers give you a proper send-off: full technique review, hard pad rounds, and if you're ready, light sparring. Savour every moment \u2014 you've earned this.", details: ['\uD83E\uDD4A Full session: everything you\'ve learned', '\uD83E\uDD3C Optional light sparring to test yourself', '\uD83D\uDCF8 Photo with your trainers \u2014 they love it', '\uD83E\uDD4A Consider buying your trainer a gift (500-1,000 THB)'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Bua Tong Sticky Waterfall', description: "A natural wonder you won't find anywhere else: a limestone waterfall you can walk UP because the rock is naturally sticky. It feels like defying gravity. Surrounded by jungle in the Nam Phu Chet Si National Park.", details: ['\uD83E\uDDD7 You can literally walk up the waterfall', '\uD83D\uDCCD 60km north of Chiang Mai \u2014 ~1.5h drive', '\uD83C\uDF3F Jungle setting with natural pools at the base', '\uD83D\uDCA7 Bring swimwear and water shoes'] },
          { title: 'Thai Cooking Class (Alternative)', description: "If you prefer a culinary adventure, join an afternoon cooking class. Visit a local market to pick ingredients, then learn to make pad thai, green curry, tom yum, and mango sticky rice from scratch.", details: ['\uD83D\uDC69\u200D\uD83C\uDF73 Farm-to-table classes: Mama Noi, Pantawan', '\uD83D\uDCB0 800-1,500 THB including market visit', '\uD83D\uDCCD Several near Old City'] }
        ] },
        { label: 'Evening', activities: [
          { title: 'Chiang Mai Craft Beer & Celebration', description: "You've completed your Muay Thai immersion training. Celebrate at one of Chiang Mai's excellent craft beer spots, reflect on what you've accomplished, and toast to the Art of Eight Limbs.", details: ['\uD83C\uDF7A Brewery \u2014 Chiang Mai\'s best craft beer bar', '\uD83C\uDF7A Let The Boy Die \u2014 quirky name, excellent beer', '\uD83C\uDF1F You trained at 3 different gyms across 2 cities'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Dash! Teak House', description: "Northern Thai fine dining in a stunning century-old teak house. The khao soi is elevated, the sai oua (sausage) is house-made, and the ambience is pure Lanna magic.", meta: '\uD83D\uDCB0 $$$ \u00b7 Old City \u00b7 Reserve ahead' }
        ] }
      ],
      mapPins: [
        { lat: 18.7920, lng: 98.9760, label: 'Santai Muay Thai', num: 1, cat: 'muaythai', desc: 'Final training session' },
        { lat: 19.1300, lng: 99.0170, label: 'Bua Tong Sticky Waterfall', num: 2, cat: 'attraction', desc: 'Walk up a waterfall' },
        { lat: 18.7950, lng: 98.9740, label: 'Mama Noi Cooking', num: 3, cat: 'attraction', desc: 'Thai cooking class' },
        { lat: 18.7980, lng: 98.9690, label: 'Brewery Craft Beer', num: 4, cat: 'food', desc: 'Best craft beer in Chiang Mai' },
        { lat: 18.7890, lng: 98.9830, label: 'Dash! Teak House', num: 5, cat: 'food', desc: 'Northern Thai fine dining' }
      ]
    },
    // DAY 14
    {
      num: 14, date: '2026-06-28', neighborhoods: 'Chiang Mai \u00b7 Old City \u00b7 Warorot',
      title: 'Chiang Mai Markets, Temples & Return to Bangkok',
      description: "Morning dawn alms offering, then explore Warorot Market \u2014 Chiang Mai's biggest traditional market. Afternoon visit the Silver Temple and Chiang Mai's art scene. Evening flight back to Bangkok for your final two nights.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Dawn Alms Offering', description: "Wake early and witness (or participate in) the Buddhist alms offering. Monks walk barefoot through the Old City streets collecting food from kneeling devotees. It's a profound, humbling experience. Ask your guesthouse about participating respectfully.", details: ['\u23F0 Around 6:00am \u2014 set an alarm', '\uD83D\uDE4F Dress modestly, kneel to offer', '\uD83D\uDCCD Best near Wat Phra Singh or Tha Phae area', '\uD83D\uDCF8 Photography from a respectful distance'] },
          { title: 'Warorot Market (Kad Luang)', description: "Chiang Mai's largest and oldest market. Three floors of northern Thai snacks, hill tribe crafts, dried flowers, and local ingredients. This is where locals shop \u2014 authentic and overwhelming in the best way.", details: ['\uD83D\uDED2 Northern sausages, dried fruits, chili pastes', '\uD83C\uDFA8 Hill tribe textiles and handicrafts', '\uD83D\uDCCD Riverside near Nawarat Bridge'] }
        ], meals: [
          { type: '\u2615 Brunch', name: 'Warorot Market Food Hall', description: "Eat at the market. Khao kha moo (braised pork leg on rice), kuay jap (rolled noodle soup), and fresh tropical smoothies. The food hall is chaotic and delicious.", meta: '\uD83D\uDCB0 $ \u00b7 Ground floor of Warorot Market' }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Wat Sri Suphan (Silver Temple)', description: "An entire temple made of hammered silver \u2014 the most unique wat in Thailand. Local silversmiths from the Wualai area created every surface. The detail is absolutely extraordinary.", details: ['\uD83C\uDFDB\uFE0F Entry: free \u00b7 Women cannot enter the main ordination hall', '\uD83E\uDD47 The silver gleams especially at night', '\uD83D\uDCCD Wualai Road, south of Old City'] }
        ] },
        { label: 'Evening', activities: [
          { title: 'Fly Back to Bangkok', description: "Evening flight from Chiang Mai back to Bangkok. 1 hour in the air, then transfer to your Sukhumvit hotel. You're returning to Bangkok as a different person \u2014 trained, tested, and deeply connected to Thai culture.", details: ['\u2708\uFE0F Evening flights: 5-7pm options', '\uD83D\uDE95 Chiang Mai airport is 15 min from Old City'] }
        ], meals: [
          { type: '\uD83C\uDF7D\uFE0F Dinner', name: 'Nana Jungle (Bangkok)', description: "Back in Bangkok. This Chinatown-edge cocktail bar and restaurant blends Thai flavours with creative cocktails in a jungle-themed space. Perfect re-arrival vibes.", meta: '\uD83D\uDCB0 $$$ \u00b7 Charoen Krung \u00b7 Trendy crowd' }
        ] }
      ],
      mapPins: [
        { lat: 18.7893, lng: 98.9817, label: 'Wat Phra Singh (Alms)', num: 1, cat: 'attraction', desc: 'Dawn alms offering route' },
        { lat: 18.7912, lng: 98.9957, label: 'Warorot Market', num: 2, cat: 'food', desc: "Chiang Mai's biggest market" },
        { lat: 18.7810, lng: 98.9867, label: 'Wat Sri Suphan', num: 3, cat: 'attraction', desc: 'Silver Temple \u2014 unique in Thailand' },
        { lat: 18.7669, lng: 98.9625, label: 'Chiang Mai Airport', num: 4, cat: 'transport', desc: 'Evening flight to Bangkok' }
      ]
    },
    // DAY 15
    {
      num: 15, date: '2026-06-29', neighborhoods: 'Sukhumvit \u00b7 Khao San \u00b7 Chatuchak',
      title: 'Final Bangkok Day \u2014 Farewell to the Ring',
      description: "Your last full day. Morning farewell session at Yokkao with your favourite trainers. Afternoon for final shopping at Chatuchak Weekend Market \u2014 the world's largest outdoor market. Evening farewell dinner and one last Bangkok night.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Yokkao \u2014 Farewell Training Session', description: "One last session at the gym that started your journey. The trainers remember you now. They push harder because they know you can take it. Shadow boxing, pads, clinch, and a proper send-off. You're leaving Bangkok as a Muay Thai practitioner, not just a tourist.", details: ['\uD83E\uDD4A Full session: everything you\'ve learned', '\uD83D\uDCF8 Photo with trainers and gym', '\uD83C\uDF81 Tip your favourite trainer (500-1,000 THB)', '\uD83E\uDD4A Buy a pair of Yokkao gloves as your souvenir'] }
        ] },
        { label: 'Afternoon', activities: [
          { title: 'Chatuchak Weekend Market', description: "The world's largest outdoor market: 15,000+ stalls across 35 acres. Vintage clothing, Thai handicrafts, home decor, art, and incredible food courts. This is your last shopping opportunity \u2014 go wild.", details: ['\uD83D\uDCCD BTS Mo Chit or MRT Chatuchak Park', '\uD83D\uDED2 15,000+ stalls \u2014 bring a map (available at entrances)', '\uD83E\uDD65 Coconut ice cream and Thai iced tea everywhere', '\u23F0 Open Sat-Sun 9am-6pm \u2014 go early to beat heat'] }
        ], meals: [
          { type: '\u2615 Lunch', name: 'Chatuchak Food Section', description: "The market's food section is a destination itself. Pad thai, mango sticky rice, grilled seafood, northern sausages, and fresh fruit smoothies from dozens of stalls.", meta: '\uD83D\uDCB0 $ \u00b7 Sections 2, 3, 4 and edges of market' }
        ] },
        { label: 'Evening', activities: [
          { title: 'Farewell Dinner & Bangkok Night', description: "Your last night in Thailand. Dress up for a special dinner, then walk through the streets one more time. Take in the smells, the sounds, the energy. You'll be back \u2014 everyone comes back to Thailand.", details: ['\uD83C\uDF19 Walk Sukhumvit one last time', '\uD83D\uDE4F Thank Thailand for the experience', '\uD83E\uDD4A You arrived as a tourist. You leave as a fighter.'] }
        ], meals: [
          { type: '\uD83C\uDF77 Dinner', name: 'Bo.lan', description: "Sustainably-minded Thai fine dining. Chef Bo and Dylan serve a set menu of rare Thai recipes rescued from disappearing traditions. A Michelin-starred farewell to the cuisine that fuelled your journey.", meta: '\uD83D\uDCB0 $$$$ \u00b7 Sukhumvit Soi 53 \u00b7 Reserve well ahead' }
        ] }
      ],
      mapPins: [
        { lat: 13.7364, lng: 100.5600, label: 'Yokkao Training Center', num: 1, cat: 'muaythai', desc: 'Farewell training session' },
        { lat: 13.7999, lng: 100.5504, label: 'Chatuchak Market', num: 2, cat: 'shopping', desc: "World's largest outdoor market" },
        { lat: 13.7280, lng: 100.5790, label: 'Bo.lan', num: 3, cat: 'food', desc: 'Michelin Thai fine dining farewell' }
      ]
    },
    // DAY 16 (Departure day - June 30)
    {
      num: 16, date: '2026-06-30', neighborhoods: 'Sukhumvit \u00b7 Suvarnabhumi',
      title: 'Departure \u2014 Carry the Spirit Home',
      description: "Pack your bruised shins and full heart. Grab one last street breakfast, and head to the airport. You arrived knowing nothing about Muay Thai. You leave with technique, stories, and a deep respect for the Art of Eight Limbs.",
      timeBlocks: [
        { label: 'Morning', activities: [
          { title: 'Final Bangkok Breakfast & Departure', description: "One last pad krapao at your favourite stall, one last Thai iced coffee. Head to Suvarnabhumi Airport via Airport Rail Link or Grab. Check in early and browse the duty-free for last-minute Thai snacks and Muay Thai gear.", details: ['\uD83C\uDF5C Last pad krapao \u2014 make it count', '\u2615 Thai iced coffee for the road', '\u2708\uFE0F Airport Rail Link from Makkasan: 45 THB', '\uD83D\uDECD\uFE0F Duty-free: dried mango, Tom Yum instant noodles, Thai tea'] }
        ], tips: [{ type: 'tip', text: "You trained at 3 gyms, watched fights at 3 stadiums, ate at 30+ food spots, visited 2 cities, and learned the Art of Eight Limbs. Not bad for 15 days. \uD83E\uDD4A\uD83C\uDDF9\uD83C\uDDED" }] }
      ],
      mapPins: [
        { lat: 13.7380, lng: 100.5601, label: 'Sukhumvit (Start)', num: 1, cat: 'transport', desc: 'Last morning in Bangkok' },
        { lat: 13.6900, lng: 100.7501, label: 'Suvarnabhumi Airport', num: 2, cat: 'transport', desc: 'Departure airport' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '800–1,500 THB/night', midrange: '2,000–4,000 THB/night', luxury: '5,000–12,000 THB/night' },
    { category: 'Muay Thai Training', budget: '300–500 THB/session', midrange: '2,500–5,000 THB/week', luxury: 'Private coaching 1,500–3,000 THB/hr' },
    { category: 'Fight Tickets', budget: '400–800 THB (Chiang Mai)', midrange: '1,500–2,000 THB (Bangkok ringside)', luxury: '2,500–3,000 THB (VIP ringside)' },
    { category: 'Meals (per couple)', budget: '200–400 THB/day (street food)', midrange: '800–1,500 THB/day', luxury: '2,000–5,000 THB/day' },
    { category: 'Transport', budget: '100–200 THB/day (BTS/MRT)', midrange: '300–600 THB/day (Grab + BTS)', luxury: '800–2,000 THB/day (private car)' },
    { category: 'Bangkok→Chiang Mai Flights', budget: '1,000–1,500 THB each way', midrange: '1,500–2,500 THB each way', luxury: '3,000+ THB business class' },
    { category: '15-Day Total (couple)', budget: '$2,000–3,000', midrange: '$3,500–5,000', luxury: '$7,000–12,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Bangkok Suvarnabhumi (BTS) is the main international hub', 'Airport Rail Link to city center: 45 THB, 30 min', 'Grab from airport: 300-500 THB to Sukhumvit'] },
    { title: '🏨 Where to Stay in Bangkok', items: ['Near BTS Asoke (Sukhumvit) for gym access', 'Grafton Sukhumvit or Grande Centre Point — comfortable mid-range', 'Sukhumvit Soi 11 area — lively, central, tons of food'] },
    { title: '🏨 Where to Stay in Chiang Mai', items: ['Inside the Old City moat for walkable temple access', 'Nimman area for coffee shops and nightlife', 'Tamarind Village or 99 The Gallery — beautiful Old City hotels'] },
    { title: '🌡️ Weather in June', items: ['Bangkok: 30-35°C, humid, afternoon rain showers', 'Chiang Mai: 25-32°C, cooler at altitude, also rainy season', 'Train early morning to avoid peak heat', 'Monsoon means green landscapes and fewer tourists'] },
    { title: '💳 Money', items: ['ATMs widely available — Kasikorn Bank has lowest fees', 'Most gyms and markets are cash only', 'Tell your bank before traveling — international ATM use can trigger fraud holds'] },
    { title: '📱 Connectivity', items: ['Buy a True Move H or DTAC SIM at the airport: 299-599 THB for 30 days unlimited data', 'Coverage excellent across Bangkok and Chiang Mai', 'Grab app essential — download before you land'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
