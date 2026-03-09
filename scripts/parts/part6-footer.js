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
