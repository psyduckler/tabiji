const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1774236064376_gigmpd',
  email: 'maxy76566@gmail.com',
  customerName: null,
  startDate: '2026-09-30'
};

const days1to7 = require('./toyokoro-days-1-7.json');
const days8to11 = require('./toyokoro-days-8-11.json');

const itineraryData = {
  destination: 'Toyokoro & the Tokachi Region, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokachi Autumn: Foliage, Farms & Wild Hokkaido',
  subtitle: '11 days through eastern Hokkaido — foliage peaks, wild coast, volcanic lakes & hidden onsen',
  description: 'An 11-day journey through the Tokachi region and eastern Hokkaido, timed for peak autumn foliage. From Obihiro\'s butadon and sweets culture to Toyokoro\'s wild Pacific coast, hidden onsen towns, morning-mist canoeing on Lake Akan, and the fiery reds and golds of Daisetsuzan — this is Hokkaido at its most raw and beautiful.',
  duration: '11 days, 10 nights',
  dates: 'September 30 – October 10, 2026',
  budget: 'USD $2,000–5,000 for 2 people',
  pace: 'Relaxed to moderate — long scenic drives balanced with onsen soaks and leisurely meals',
  bestFor: 'Adventure · Cultural · Foodie · Relaxation',
  highlights: [
    'Peak autumn foliage at Daisetsuzan and Lake Shikaribetsu',
    'Tokachi butadon — Obihiro\'s iconic grilled pork bowl',
    'Morning mist canoeing on volcanic Lake Akan',
    'Toyokoro\'s wild Pacific coast — birthplace of Jewel Ice',
    'Tokachi wine, farm-to-table cheese, and Rokkatei sweets',
    'Hidden onsen: Nukabira, Tokachigawa, Kawayu',
    'Red-crowned cranes at Tsurui near Kushiro',
    'Biei\'s rolling hills and Shirogane Blue Pond'
  ],
  essentials: [
    {
      title: '🍂 Weather & Foliage',
      text: 'Late September to early October is peak autumn in inland Hokkaido. Expect 5–18°C, cooler at elevation (near freezing at Daisetsuzan). Colors peak at high elevations in late September, moving to lower areas by early October. Pack layers: light down jacket, fleece, rain shell. Mornings are crisp — perfect for onsen.'
    },
    {
      title: '🚗 Getting Around',
      text: 'A rental car is essential for this itinerary. Pick up at Tokachi-Obihiro Airport (OBO). Expect ¥5,000–8,000/day for a compact car. Roads are excellent but distances are large — budget 1–3 hours between major stops. Fill up at every gas station in rural areas. Download offline Google Maps before leaving cities.'
    },
    {
      title: '💴 Budget Overview',
      text: 'Accommodation: ¥8,000–20,000/night for ryokan/hotels. Meals: ¥800–2,500/person. Many activities are free (hiking, scenic drives). Canoeing: ~¥5,000–8,000/person. Car rental: ~¥50,000–80,000 for 11 days. Total for 2 people: roughly USD $2,500–4,500 depending on accommodation.'
    },
    {
      title: '🏨 Accommodation Strategy',
      text: 'Mix of business hotels in cities (Obihiro, Kushiro) and onsen ryokan in hot spring towns (Tokachigawa, Nukabira, Kawayu). Book ryokan with dinner included — the kaiseki meals alone are worth it. In cities, stay near stations for easy restaurant access.'
    },
    {
      title: '📱 Useful Tips',
      text: 'Seicomart is Hokkaido\'s local convenience store chain — better than 7-Eleven, with excellent hot food. Carry cash — rural Hokkaido is cash-heavy. Many rural restaurants close by 7 PM, so eat early or plan ahead. Deer cross roads at dawn and dusk — drive carefully in forested areas.'
    }
  ],
  days: [...days1to7, ...days8to11],
  budgetTable: [
    { category: 'Car Rental (11 days)', perDay: '¥6,500', total: '¥71,500', notes: 'Compact car, shared by 2' },
    { category: 'Accommodation', perDay: '¥8,000–18,000/person', total: '¥160,000–360,000', notes: 'Mix of hotels and ryokan' },
    { category: 'Meals', perDay: '¥3,000–6,000/person', total: '¥66,000–132,000', notes: 'Ryokan dinners included on onsen nights' },
    { category: 'Activities', perDay: '¥0–3,000', total: '¥0–30,000', notes: 'Canoeing, ropeway, museum admissions' },
    { category: 'Fuel & Tolls', perDay: '¥1,500', total: '¥16,500', notes: 'Hokkaido distances are long' },
    { category: 'Total for 2 people', perDay: '', total: 'USD $2,800–5,500', notes: 'Mid-range estimate' }
  ],
  practicalInfo: [
    {
      title: '✈️ Getting There',
      text: 'Fly to Tokachi-Obihiro Airport (OBO) from Tokyo Haneda — about 1 hour 45 minutes. ANA and JAL operate multiple daily flights. Alternatively fly to New Chitose (Sapporo) and drive or take the JR Tokachi limited express (~2.5 hours).'
    },
    {
      title: '📡 Connectivity',
      text: 'Get a Japan SIM card or pocket WiFi at the airport. Rakuten Mobile and IIJmio offer good coverage even in rural Hokkaido. Offline Google Maps downloaded before leaving cities is essential — some mountain areas have no signal.'
    },
    {
      title: '🦌 Wildlife Notes',
      text: 'Hokkaido has deer, foxes, and occasional bears. Do not feed wildlife. Ezo deer (a large subspecies) frequently cross roads at dawn and dusk — drive carefully in forested areas, especially around Daisetsuzan and the wetlands.'
    },
    {
      title: '🏥 Health & Safety',
      text: 'Japan is extremely safe. Travel insurance is recommended. Bring any prescription medications — rural pharmacies may not stock specialty drugs. Hot spring etiquette: some onsen restrict visible tattoos. Shower before entering any communal bath.'
    }
  ]
};

fulfillOrder(order, itineraryData);
