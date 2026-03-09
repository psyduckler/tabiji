const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772321838777_0jnfqh',
  email: 'mailannez@gmail.com',
  destination: 'Netherlands',
  startDate: '2026-03-01',
  endDate: '2026-03-01',
  groupSize: 2,
  requests: 'I want to spend a day in the Netherlands with my grandfather. He can not walk for hours and needs to visit the toilet regularly.'
};

const itineraryData = {
  destination: 'Amsterdam, Netherlands',
  countryEmoji: '🇳🇱',
  title: 'A Gentle Day in Amsterdam with Grandpa',
  subtitle: 'Canal boats, cozy cafés & Dutch masterpieces — at your own pace',
  description: "Amsterdam is the perfect city for a gentle day out with your grandfather. With its flat terrain, excellent public transport, and world-class accessible venues, you can enjoy the very best of Dutch culture without rushing. This itinerary focuses on seated experiences, canal boat tours with onboard toilets, accessible museums, and cozy cafés with frequent rest stops. Every venue is chosen for comfort, accessibility, and easy access to facilities.",
  duration: '1 day',
  dates: 'Mar 1, 2026',
  budget: '$',
  pace: 'Very Relaxed',
  bestFor: 'Family · Accessibility',
  highlights: [
    'Private canal boat cruise with onboard toilet',
    'Rijksmuseum highlights tour (wheelchair accessible)',
    'Traditional Dutch pancakes at a cozy café',
    'Scenic tram ride through the historic centre',
    'Warm apple pie at a classic brown café'
  ],

  essentials: [
    { title: '♿ Accessibility', text: "Amsterdam is flat and well-adapted for limited mobility. The Rijksmuseum and canal boats are fully accessible. Trams have low-floor boarding. Public toilets are available at Centraal Station, all major museums, and most cafés. We've chosen venues with good toilet facilities throughout." },
    { title: '🚋 Getting Around', text: "Use the GVB tram network — it's smooth, frequent, and has priority seating. Buy an anonymous OV-chipkaart or tap your contactless card. Tram lines 2, 5, and 12 connect Centraal Station to the Museum Quarter. Taxis are also easy to find." },
    { title: '🌧️ March Weather', text: "Early March in Amsterdam averages 5-9°C. Dress in warm layers, bring a waterproof jacket, and wear comfortable non-slip shoes. The canal boat and museum are indoor activities — perfect for unpredictable weather." },
    { title: '🚻 Toilet Access', text: "Every stop on this itinerary has accessible toilets. Museums have multiple restrooms on each floor. The canal boat has an onboard toilet. Cafés and restaurants all have facilities. Centraal Station has a large, clean toilet facility (€0.70)." }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-01',
      neighborhoods: 'Centraal · Canal Ring · Museum Quarter',
      title: 'Amsterdam — Canals, Art & Dutch Warmth',
      description: "A gentle day exploring Amsterdam's finest highlights with plenty of seated experiences, warm indoor stops, and easy access to facilities. Start with a canal cruise, visit the Rijksmuseum at a leisurely pace, and end with a cozy Dutch dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive & Coffee at Centraal Station',
              description: "Start your day at Amsterdam Centraal Station. Grab a coffee and a fresh stroopwafel at the station's grand café while you settle in. The station has excellent toilet facilities and is the hub for all tram routes.",
              details: [
                '☕ Starbucks or Grand Café 1e Klas (beautiful Art Nouveau interior) inside the station',
                '🚻 Clean, accessible toilets in the main hall (€0.70)',
                '🚋 All tram lines depart from right outside the station'
              ]
            },
            {
              title: 'Canal Cruise — Blue Boat Company',
              description: "Board a 75-minute canal cruise from right near Centraal Station. Glide through Amsterdam's UNESCO-listed canal ring while sitting comfortably with a warm drink. The boat has an onboard toilet, heating, and a glass roof for panoramic views even on grey days. Your grandfather can sit back and enjoy the narrated tour of gabled merchant houses, bridges, and hidden gardens.",
              details: [
                '🚢 Blue Boat Company or Lovers Canal Cruises — both depart near Centraal',
                '🚻 Onboard toilet available throughout the cruise',
                '♿ Wheelchair-accessible boarding via ramp',
                '🎧 Multi-language audio guide with headphones provided',
                '💰 ~€18 per person · Book online for a guaranteed departure time'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee',
              name: 'Grand Café 1e Klas',
              description: "A stunning Art Nouveau café inside Centraal Station — once the first-class waiting room. Beautiful interior, good coffee, and easy to reach before your canal cruise.",
              meta: '💰 $ · 📍 Amsterdam Centraal Station · 🚻 Toilets nearby'
            }
          ],
          tips: [
            { type: 'tip', text: "Book the canal cruise for around 10:30am — the boats are less crowded on weekday mornings. The Blue Boat Company's covered boats are warm and comfortable, perfect for March weather." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dutch Pancakes at The Pancake Bakery',
              description: "After the cruise, take tram 2 or 5 to the Jordaan area for a classic Dutch lunch. The Pancake Bakery serves enormous, delicious Dutch pancakes in a cozy 17th-century warehouse. Sweet or savoury — the bacon and apple pancake is legendary. A warm, seated, indoor experience perfect for refuelling.",
              details: [
                '🥞 Try the bacon & apple pancake or the classic sugar & butter',
                '🚻 Toilets available in the restaurant',
                '📍 Prinsengracht 191 — right on the canal',
                '💰 ~€12-15 per pancake · Cash and card accepted'
              ]
            },
            {
              title: 'Rijksmuseum — Highlights Tour',
              description: "The Rijksmuseum is fully wheelchair-accessible and has excellent facilities. Rather than trying to see everything, focus on the highlights: Rembrandt's Night Watch, Vermeer's Milkmaid, and the stunning Gallery of Honour. Free wheelchairs are available at the entrance. Take your time — there are benches in every gallery and toilets on each floor.",
              details: [
                '🖼️ Must-see: The Night Watch (Rembrandt), The Milkmaid (Vermeer), Gallery of Honour',
                '♿ Free wheelchair loan at cloakroom · Lifts to all floors',
                '🚻 Accessible toilets on every floor',
                '🪑 Benches in most galleries — rest whenever you need',
                '💰 €22.50 per person · Free for under-18s · Book timed entry online',
                '⏰ Allow 1.5–2 hours for a relaxed highlights visit'
              ]
            }
          ],
          meals: [
            {
              type: '🥞 Lunch',
              name: 'The Pancake Bakery',
              description: 'Classic Dutch pancake house in a 17th-century canal warehouse. Enormous, fluffy Dutch pancakes in sweet and savoury varieties.',
              meta: '💰 $$ · 📍 Prinsengracht 191, Jordaan · 🚻 Toilets on-site'
            }
          ],
          tips: [
            { type: 'tip', text: "At the Rijksmuseum, ask for the free museum map and head straight to Room 2.08 (Night Watch) and the Gallery of Honour. Skip the Asian Pavilion and library wing to save energy for the masterpieces." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Apple Pie at Café Winkel 43',
              description: "Before dinner, stop at Café Winkel 43 in the Jordaan for the best apple pie in Amsterdam. Thick, buttery, loaded with cinnamon apples, and served with a mountain of whipped cream. It's a beloved local tradition. Sit by the window and watch the Noordermarkt square.",
              details: [
                '🍰 Their apple pie is legendary — order it warm with slagroom (whipped cream)',
                '📍 Noordermarkt 43, Jordaan',
                '🚻 Toilets available',
                '💰 ~€5 per slice'
              ]
            },
            {
              title: 'Leisurely Tram Ride Back',
              description: "Take tram 13 or 17 from the Jordaan area back towards the centre. Riding the tram through Amsterdam's illuminated streets at dusk is a lovely experience — watch the canal houses light up and the bridges twinkle.",
              details: [
                '🚋 Trams run every 5-10 minutes',
                '🪑 Priority seating at the front of every tram',
                '📸 The Prinsengracht and Westerkerk are beautiful at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Moeders (Mothers)',
              description: "A warm, homestyle Dutch restaurant where the walls are covered in photos of guests' mothers. Traditional Dutch comfort food — stamppot, erwtensoep, and bitterballen. The perfect cozy end to a day with your grandfather. Accessible ground-floor seating.",
              meta: '💰 $$ · 📍 Rozengracht 251, Jordaan · 🚻 Toilets on-site · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: "Moeders ('Mothers') is a beloved Amsterdam institution — bring a photo of your grandmother or mother to add to their wall collection! The stamppot (mashed potatoes with vegetables and sausage) is classic Dutch comfort food." }
          ]
        }
      ],
      mapPins: [
        { lat: 52.3791, lng: 4.9003, label: 'Amsterdam Centraal Station', num: 1, cat: 'transport', desc: 'Main station — starting point, coffee, toilet facilities' },
        { lat: 52.3775, lng: 4.8948, label: 'Canal Cruise Departure', num: 2, cat: 'attraction', desc: 'Blue Boat Company — 75-min canal cruise with onboard toilet' },
        { lat: 52.3812, lng: 4.9003, label: 'Grand Café 1e Klas', num: 3, cat: 'food', desc: 'Art Nouveau café inside Centraal Station' },
        { lat: 52.3757, lng: 4.8826, label: 'The Pancake Bakery', num: 4, cat: 'food', desc: 'Classic Dutch pancakes in a canal warehouse' },
        { lat: 52.3600, lng: 4.8852, label: 'Rijksmuseum', num: 5, cat: 'attraction', desc: 'World-class art museum — fully accessible, Rembrandt & Vermeer' },
        { lat: 52.3814, lng: 4.8840, label: 'Café Winkel 43', num: 6, cat: 'food', desc: "Amsterdam's best apple pie — warm with whipped cream" },
        { lat: 52.3759, lng: 4.8811, label: 'Moeders Restaurant', num: 7, cat: 'food', desc: 'Homestyle Dutch comfort food — the perfect cozy dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Canal Cruise (2 persons)', budget: '€36', midrange: '€36', luxury: '€70 (private boat)' },
    { category: 'Rijksmuseum (2 persons)', budget: '€45', midrange: '€45', luxury: '€45 + private guide €150' },
    { category: 'Meals (2 persons)', budget: '€50–70', midrange: '€70–100', luxury: '€100–150' },
    { category: 'Transport (tram/taxi)', budget: '€10–15', midrange: '€15–25', luxury: '€40–60 (taxi)' },
    { category: 'Apple Pie & Coffee', budget: '€15', midrange: '€15', luxury: '€15' },
    { category: '1-Day Total (2 persons)', budget: '€150–180', midrange: '€180–220', luxury: '€320–490' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Amsterdam Schiphol Airport (AMS) is 20 minutes from the city centre by train', 'Direct train from Schiphol to Centraal Station every 10 minutes (€4.60)', 'If arriving by car, park at a P+R location and take the tram in — city centre parking is expensive'] },
    { title: '♿ Accessibility Tips', items: ['Request a wheelchair at the Rijksmuseum cloakroom (free)', 'All GVB trams have low-floor boarding and priority seating', 'Canal boats have step-free boarding via ramp — call ahead to confirm', 'Most restaurants in the Jordaan have ground-floor seating'] },
    { title: '🚻 Toilet Locations', items: ['Centraal Station — main hall (€0.70, accessible)', 'Rijksmuseum — every floor (free with entry, accessible)', 'All restaurants and cafés on this itinerary have on-site toilets', 'Public toilet at Museumplein near the Rijksmuseum'] },
    { title: '🌡️ March Weather', items: ['Average temperature: 5–9°C (41–48°F)', 'Rain is likely — bring a compact umbrella and waterproof jacket', 'Wind can be brisk near the canals — a warm scarf helps', 'Indoor activities (museum, cafés, boat) keep you warm throughout'] },
    { title: '💳 Money', items: ['The euro (€) — contactless/card payments accepted almost everywhere', 'Some toilets and small vendors prefer coins — carry a few euros', 'Tipping is not expected but rounding up is appreciated', 'Budget for the day: approximately €150–200 for two people'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
