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
