const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772393016214_7fw1b7',
  email: 'heathervandeest@gmail.com',
  destination: 'London, UK',
  startDate: '2026-06-03',
  endDate: '2026-06-07',
  groupSize: '3-4',
  requests: 'Include Tower of London, St Paul\'s Cathedral, Churchill War Rooms, quick stop at Buckingham Palace. Also Camden Locks/market and a couple hours at the British Museum. Staying in Covent Garden.'
};

const itineraryData = {
  destination: 'London, UK',
  countryEmoji: '🇬🇧',
  title: 'Crown Jewels & Camden Locks: A London Family Adventure',
  subtitle: '4 days of history, culture & market magic for the whole family — based in Covent Garden',
  description: "London is a city where 2,000 years of history meets world-class culture at every turn. This family-friendly itinerary hits the landmarks you've been dreaming about — the Tower of London, St Paul's Cathedral, Churchill War Rooms, Buckingham Palace — while weaving in the vibrant chaos of Camden Market and the treasures of the British Museum. Based in Covent Garden, you're perfectly placed to walk to most attractions, hop on the Tube for the rest, and end each day surrounded by great casual dining and street performers. Early June brings long daylight, pleasant weather, and London at its best.",
  duration: '4 nights',
  dates: 'Jun 3 – Jun 7, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Families · Culture Lovers · History Buffs',
  highlights: [
    'See the Crown Jewels and 1,000 years of history at the Tower of London',
    'Climb to the Whispering Gallery inside St Paul\'s Cathedral dome',
    'Step into Churchill\'s secret underground bunker at the War Rooms',
    'Watch the Changing of the Guard at Buckingham Palace',
    'Explore the eclectic food stalls and vintage shops of Camden Market',
    'Marvel at the Rosetta Stone and Egyptian mummies at the British Museum'
  ],

  essentials: [
    { title: '☀️ Early June Weather', text: 'Expect 15–22°C (59–72°F) with long daylight until 9:15pm. Rain is always possible — pack a compact umbrella and layers. Mornings can be cool; afternoons are lovely for walking.' },
    { title: '🚇 Getting Around', text: 'Get Oyster cards or use contactless bank cards on the Tube and buses. Kids under 11 travel free on all TfL services with a paying adult. The Tube is the fastest way between zones; buses offer better views.' },
    { title: '🎫 Advance Booking', text: 'Book Tower of London, Churchill War Rooms, and St Paul\'s tickets online in advance — you\'ll save money and skip queues. The British Museum and Buckingham Palace exterior are free.' },
    { title: '💷 Budget Tips', text: 'London can be pricey, but this itinerary keeps costs down: free museums, casual dining, Tube travel. Budget roughly £60–80/day for a family of 4 on food, or eat at markets and grab-and-go spots to save more.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-03',
      neighborhoods: 'Tower Hill · City of London · Southbank',
      title: 'The Tower, the Bridge & the Thames',
      description: "Hit the ground running with London's most iconic fortress. The Tower of London is a must for families — Crown Jewels, Beefeaters, ravens, and medieval armour. Then cross Tower Bridge and stroll the South Bank back toward your Covent Garden base.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tower of London',
              description: 'Arrive early to beat the crowds at this 1,000-year-old fortress. Join a free Yeoman Warder (Beefeater) tour — they\'re hilarious storytellers who bring the Tower\'s grisly history alive for all ages. See the Crown Jewels, the White Tower\'s medieval armour collection, and count the famous ravens.',
              details: [
                '🏰 Book online: Adults ~£33, Children (5-15) ~£16, Under 5 free',
                '⏰ Open 9am – allow 2.5-3 hours for a thorough visit',
                '👑 Crown Jewels queue moves fast — go here first or save for last',
                '🐦 Look for the 7 ravens — legend says the kingdom falls if they leave'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Take the Tube from Covent Garden (Piccadilly line) to Tower Hill — about 15 minutes door to door. The Tower is a 3-minute walk from the station.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tower Bridge & South Bank Walk',
              description: 'Cross the iconic Tower Bridge (free to walk across, £12 for the Exhibition with glass floor walkway — kids love it). Then stroll west along the South Bank past City Hall, the Tate Modern exterior, and Shakespeare\'s Globe toward Waterloo.',
              details: [
                '🌉 The glass floor walkway is 42 metres above the Thames — thrilling for brave kids',
                '📸 Great family photo ops from the north bank looking at the bridge',
                '🚶 South Bank walk to Waterloo is about 30 minutes — flat and scenic'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Borough Market (quick detour)',
              description: 'Just a 10-minute walk from Tower Bridge, Borough Market is London\'s oldest food market. Grab gourmet grilled cheese from Kappacasein, fresh pad thai, or a classic pie from Pieminister. Something for every taste and budget.',
              meta: '💰 $ · 📍 8 Southwark St, SE1 · Open Wed–Sat, limited Mon–Tue'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Flat Iron Covent Garden',
              description: 'Hugely popular casual steak restaurant — just one cut of flat iron steak, perfectly cooked, for about £14. Free ice cream cone for dessert. Kids love the simplicity and the mini cleavers that hold the bill. No reservations; queue moves fast.',
              meta: '💰 $ · 📍 17 Henrietta St, WC2E · Walk-in only'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, catch the street performers in the Covent Garden Piazza — there are jugglers, magicians, and musicians every evening until late. Free entertainment right on your doorstep.' }
          ]
        }
      ],
      mapPins: [
        { lat: 51.5081, lng: -0.0759, label: 'Tower of London', num: 1, cat: 'attraction', desc: '1,000-year-old fortress — Crown Jewels, Beefeaters & ravens' },
        { lat: 51.5055, lng: -0.0754, label: 'Tower Bridge', num: 2, cat: 'attraction', desc: 'Iconic bridge with glass floor walkway' },
        { lat: 51.5055, lng: -0.0910, label: 'Borough Market', num: 3, cat: 'food', desc: 'London\'s oldest food market — gourmet street food' },
        { lat: 51.5118, lng: -0.1246, label: 'Flat Iron Covent Garden', num: 4, cat: 'food', desc: 'Casual steak restaurant with free ice cream' },
        { lat: 51.5117, lng: -0.1240, label: 'Covent Garden Piazza', num: 5, cat: 'attraction', desc: 'Street performers and evening entertainment' }
      ]
    },
    {
      num: 2,
      date: '2026-06-04',
      neighborhoods: 'Westminster · St James\'s · Whitehall',
      title: 'Palaces, Parliament & the War Rooms',
      description: "A day in the heart of royal and political London. Start with the Changing of the Guard at Buckingham Palace, dive underground into Churchill's wartime bunker, and take in the magnificent St Paul's Cathedral. History comes alive today.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Buckingham Palace — Changing of the Guard',
              description: 'Arrive by 10:15am to secure a good viewing spot along the Palace fence or on the Victoria Memorial steps. The ceremony starts at 11am and lasts about 45 minutes — the pageantry of the Guards in their bearskin hats and red tunics is unmissable.',
              details: [
                '💂 Ceremony runs Mon, Wed, Fri, Sun in June (check schedule day-of)',
                '📍 Best spots: Victoria Memorial steps or the fence along Spur Road',
                '⏱️ Quick stop — 30-45 minutes is plenty, then move on',
                '🆓 Completely free to watch'
              ]
            },
            {
              title: 'St James\'s Park Stroll',
              description: 'Walk through gorgeous St James\'s Park from the Palace toward Whitehall. Feed the pelicans on the lake (they\'ve been here since 1664!), enjoy the views of Buckingham Palace from the Blue Bridge, and let the kids run on the grass.',
              details: [
                '🦆 Pelican feeding is daily at 2:30pm near Duck Island — but they\'re around all morning',
                '📸 The view from the Blue Bridge with Buckingham Palace behind is iconic'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Churchill War Rooms',
              description: 'Descend into the secret underground complex where Churchill directed WWII. The cramped Map Room, his bedroom, the transatlantic telephone room — everything preserved exactly as it was left in 1945. The interactive Churchill Museum is excellent for older kids and history-loving adults.',
              details: [
                '🎫 Book online: Adults ~£28, Children (5-15) free with paying adult',
                '⏰ Allow 1.5–2 hours — the audio guide is fantastic',
                '📍 Clive Steps, King Charles St — 5 min walk from St James\'s Park',
                '🎧 Free audio guide included with entry — essential for full experience'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Café in the Park (St James\'s Park)',
              description: 'Relaxed lakeside café in the heart of St James\'s Park with views of the pelicans. Sandwiches, salads, and cakes — perfect casual refuel between Buckingham Palace and the War Rooms.',
              meta: '💰 $ · 📍 St James\'s Park, Horse Guards Rd'
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'St Paul\'s Cathedral',
              description: 'Christopher Wren\'s masterpiece dominates the City skyline. Climb 257 steps to the Whispering Gallery inside the dome — whisper against the wall and hear it on the opposite side 30 metres away. Kids are mesmerized. Continue to the Stone and Golden Galleries for panoramic London views.',
              details: [
                '⛪ Book online: Adults ~£23, Children (6-17) ~£10',
                '🔊 Whispering Gallery: 257 steps, Stone Gallery: 376, Golden Gallery: 528',
                '⏰ Last entry 4pm — arrive by 3pm to enjoy fully',
                '📸 The view from the Golden Gallery is one of London\'s best'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dishoom Covent Garden',
              description: 'Bombay-inspired café that\'s become a London institution. The black daal is legendary, the lamb biryani feeds two, and the atmosphere is pure 1960s Bombay glamour. Family-friendly with a kids\' menu. Expect a queue at peak times — worth it.',
              meta: '💰 $$ · 📍 12 Upper St Martin\'s Ln, WC2H · Book ahead or queue from 5pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.5014, lng: -0.1419, label: 'Buckingham Palace', num: 1, cat: 'attraction', desc: 'Changing of the Guard ceremony' },
        { lat: 51.5025, lng: -0.1350, label: 'St James\'s Park', num: 2, cat: 'attraction', desc: 'Royal park with pelicans and Palace views' },
        { lat: 51.5022, lng: -0.1293, label: 'Churchill War Rooms', num: 3, cat: 'attraction', desc: 'WWII underground bunker museum' },
        { lat: 51.5138, lng: -0.0984, label: 'St Paul\'s Cathedral', num: 4, cat: 'attraction', desc: 'Wren\'s masterpiece — Whispering Gallery & dome views' },
        { lat: 51.5130, lng: -0.1265, label: 'Dishoom Covent Garden', num: 5, cat: 'food', desc: 'Bombay-inspired café — legendary black daal' }
      ]
    },
    {
      num: 3,
      date: '2026-06-05',
      neighborhoods: 'Camden Town · Bloomsbury · Covent Garden',
      title: 'Camden Market & the British Museum',
      description: "A change of pace — start with the vibrant energy of Camden Market, where vintage fashion meets global street food by the canal. Then head south to Bloomsbury for a couple of hours with the world's treasures at the British Museum. Two very different London vibes, one brilliant day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Camden Market & Camden Lock',
              description: 'Take the Northern line to Camden Town and dive into London\'s most eclectic market. Wander through the Stables Market (vintage and alternative fashion), browse Hawley Wharf\'s food hall, and explore the canalside Lock Market. It\'s sensory overload in the best way — kids love the quirky shops and giant food court.',
              details: [
                '🛍️ Markets open 10am–6pm daily — arrive by 10:30 to beat crowds',
                '🍜 Best food stalls: The cheese toastie at The Cheese Bar, gyoza at Kukuruza, and fresh Thai at Yum Bun',
                '🎨 Hawley Wharf has family entertainment — arcade games, creative workshops',
                '📸 Don\'t miss the giant sculptures and colourful shopfronts along Camden High Street'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch/Lunch',
              name: 'Camden Market Street Food',
              description: 'Skip a sit-down meal — the market IS the meal. Each person picks what they want from dozens of stalls. Budget about £8–12 per person for a generous portion. The food court areas have covered seating.',
              meta: '💰 $ · 📍 Camden Lock Place, NW1 · Come hungry'
            }
          ],
          tips: [
            { type: 'tip', text: 'Walk along the Regent\'s Canal towpath from Camden Lock toward Regent\'s Park for 10 minutes — it\'s a lovely, peaceful contrast to the market bustle. You\'ll pass colorful narrow boats and street art.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The British Museum',
              description: 'One of the world\'s greatest museums — and completely free. With limited time, focus on the greatest hits: the Rosetta Stone (Room 4), Egyptian mummies (Rooms 62–63), the Parthenon Marbles (Room 18), and the stunning Great Court atrium. Pick up a family trail map at the info desk to keep kids engaged.',
              details: [
                '🆓 Free entry — suggested donation £5',
                '⏰ Open 10am–5pm (Fridays until 8:30pm)',
                '🗺️ Grab the free family trail — different themes for different ages',
                '📍 15-minute walk south from Camden, or one Tube stop to Tottenham Court Road',
                '⏱️ 2–2.5 hours is perfect for a focused visit with kids'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Covent Garden Evening',
              description: 'Back in your neighborhood — browse the boutique shops in the Apple Market, catch the evening street performers in the Piazza, and settle into dinner. Covent Garden is at its most magical in the early evening light.',
              details: [
                '🎭 Check what\'s on at nearby theatres — family-friendly West End shows are walkable',
                '🛍️ The Apple Market has handmade crafts and jewellery'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Crust Bros',
              description: 'Authentic Neapolitan pizza right in Covent Garden — hand-stretched dough, San Marzano tomatoes, and proper mozzarella. Simple, delicious, and very family-friendly. Kids can watch the pizza chefs at work.',
              meta: '💰 $ · 📍 17-18 Henrietta St, WC2E'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.5413, lng: -0.1466, label: 'Camden Market', num: 1, cat: 'attraction', desc: 'Eclectic market — vintage fashion, street food & canal' },
        { lat: 51.5410, lng: -0.1455, label: 'Camden Lock', num: 2, cat: 'attraction', desc: 'Canalside market with food stalls and craft shops' },
        { lat: 51.5194, lng: -0.1270, label: 'British Museum', num: 3, cat: 'attraction', desc: 'World-class museum — Rosetta Stone, mummies & more (free)' },
        { lat: 51.5117, lng: -0.1240, label: 'Covent Garden Piazza', num: 4, cat: 'attraction', desc: 'Street performers and evening shopping' },
        { lat: 51.5115, lng: -0.1245, label: 'Crust Bros', num: 5, cat: 'food', desc: 'Authentic Neapolitan pizza in Covent Garden' }
      ]
    },
    {
      num: 4,
      date: '2026-06-06',
      neighborhoods: 'South Kensington · Hyde Park · Soho',
      title: 'Museums, Parks & a West End Farewell',
      description: "Your final full day mixes world-class free museums with London's most beloved green space. Start at the Natural History Museum (a guaranteed family hit), enjoy a leisurely afternoon in Hyde Park, and wrap up your trip with a buzzing Soho dinner near the theatres.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Natural History Museum',
              description: 'The cathedral of nature — the grand Hintze Hall with its blue whale skeleton is jaw-dropping from the moment you walk in. Kids will lose their minds at the animatronic T-Rex, the earthquake simulator, and the insect gallery. One of London\'s best free attractions.',
              details: [
                '🆓 Free entry — arrive at 10am opening for shortest queues',
                '🦕 Highlights: Hintze Hall (blue whale), Dinosaur Gallery, Earth Hall earthquake sim',
                '⏰ Allow 2–2.5 hours for a family visit',
                '📍 Tube to South Kensington, 5-minute walk through the tunnel'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The V&A and Science Museum are right next door if anyone wants more. The Science Museum has excellent interactive galleries for kids (also free).' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hyde Park & Kensington Gardens',
              description: 'Decompress in London\'s most famous park. Rent a pedalo on the Serpentine lake, visit the Diana Memorial Playground (a massive pirate ship adventure playground — kids\' paradise), and stroll through Kensington Gardens past the Albert Memorial.',
              details: [
                '⛵ Serpentine pedalos: ~£14/30 min for a family boat',
                '🏴‍☠️ Diana Memorial Playground: free, open 10am–5:45pm, ages 0–12',
                '🌳 The Italian Gardens at the north end of the Serpentine are beautiful and quiet'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'The Serpentine Bar & Kitchen',
              description: 'Lakeside restaurant in Hyde Park with outdoor terrace overlooking the water. Casual menu of salads, burgers, and seasonal dishes. Perfect spot to relax while kids play nearby.',
              meta: '💰 $$ · 📍 Serpentine Road, Hyde Park'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Stroll Through Soho & Covent Garden',
              description: 'Your last evening — wander through the buzzing streets of Soho, peek at the neon lights of Piccadilly Circus, and loop back to Covent Garden for one last look at the Piazza performers. London is best explored on foot, and this walk captures its energy perfectly.',
              details: [
                '📸 Piccadilly Circus lights + Eros statue — classic London photo',
                '🎭 If you fancy a show, Leicester Square TKTS booth sells same-day discounted West End tickets',
                '🛍️ Neal\'s Yard in Covent Garden is a hidden, Instagram-worthy colourful courtyard'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hoppers Soho',
              description: 'Sri Lankan and South Indian street food — the egg hoppers (crispy bowl-shaped pancakes) are addictive, the bone marrow varuval is unforgettable, and the kothu roti is family-sharing perfection. Casual, affordable, and deeply delicious.',
              meta: '💰 $ · 📍 49 Frith St, Soho, W1D · No reservations — queue from 5:30pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 51.4967, lng: -0.1764, label: 'Natural History Museum', num: 1, cat: 'attraction', desc: 'Free museum — dinosaurs, blue whale & earthquake simulator' },
        { lat: 51.5053, lng: -0.1657, label: 'Hyde Park — Serpentine', num: 2, cat: 'attraction', desc: 'Pedalos on the lake and lakeside relaxation' },
        { lat: 51.5097, lng: -0.1878, label: 'Diana Memorial Playground', num: 3, cat: 'attraction', desc: 'Pirate ship adventure playground for kids' },
        { lat: 51.5100, lng: -0.1347, label: 'Piccadilly Circus', num: 4, cat: 'attraction', desc: 'Iconic neon lights and Eros statue' },
        { lat: 51.5133, lng: -0.1312, label: 'Hoppers Soho', num: 5, cat: 'food', desc: 'Sri Lankan hoppers and street food' }
      ]
    },
    {
      num: 5,
      date: '2026-06-07',
      neighborhoods: 'Covent Garden · The Strand',
      title: 'Morning Coffee & Goodbye London',
      description: "A relaxed departure morning. Enjoy a final breakfast in Covent Garden, pick up last-minute souvenirs, and soak in the neighborhood that's been your home base for four wonderful days.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Covent Garden Morning',
              description: 'No rush today. Wander the morning market stalls, grab souvenirs from the quirky shops along Neal Street, and enjoy one last coffee overlooking the Piazza. If you haven\'t visited Neal\'s Yard yet, duck into the tiny colourful courtyard — it\'s magical.',
              details: [
                '🛍️ Stanfords on Long Acre is the world\'s largest travel bookshop — great for map prints',
                '🌈 Neal\'s Yard: look for the hidden entrance off Shorts Gardens',
                '☕ If time allows, pop into the London Transport Museum (kid-friendly, £20/adult, under 18 free)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Notes Coffee Roasters',
              description: 'Excellent specialty coffee and pastries in a charming space right in Covent Garden. Great flat whites, fresh croissants, and a calm start to your travel day.',
              meta: '💰 $ · 📍 31 St Martin\'s Ln, WC2N'
            }
          ],
          tips: [
            { type: 'tip', text: 'Heading to Heathrow? The Piccadilly line runs direct from Covent Garden — about 50 minutes. For Gatwick, take the Thameslink from Farringdon or St Pancras. Allow 2.5 hours before your flight.' }
          ]
        }
      ],
      mapPins: [
        { lat: 51.5117, lng: -0.1240, label: 'Covent Garden Piazza', num: 1, cat: 'attraction', desc: 'Final morning at your home base' },
        { lat: 51.5139, lng: -0.1264, label: 'Neal\'s Yard', num: 2, cat: 'attraction', desc: 'Colourful hidden courtyard' },
        { lat: 51.5120, lng: -0.1258, label: 'Notes Coffee Roasters', num: 3, cat: 'food', desc: 'Specialty coffee and pastries' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '£80–120/night (budget hotel)', midrange: '£150–250/night', luxury: '£300–600/night' },
    { category: 'Meals (family of 4)', budget: '£50–70/day', midrange: '£80–120/day', luxury: '£150–300/day' },
    { category: 'Transport (Oyster/contactless)', budget: '£15–25/day', midrange: '£25–40/day', luxury: '£60–150/day (private)' },
    { category: 'Activities', budget: '£30–60/day', midrange: '£60–100/day', luxury: '£100–200/day' },
    { category: '4-Day Total (family of 4)', budget: '£700–1,100', midrange: '£1,200–2,000', luxury: '£2,500–5,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Heathrow (LHR): Piccadilly line direct to Covent Garden — ~50 min, £5.50/adult', 'Gatwick (LGW): Thameslink train to Farringdon or St Pancras — ~40 min, £10–15', 'Stansted (STN): Stansted Express to Liverpool St — ~50 min, then Tube', 'Black cabs from Heathrow: ~£60–80 — consider Uber for families with luggage'] },
    { title: '🏨 Staying in Covent Garden', items: ['Central location — walkable to most Day 1-2 attractions', 'Tube stations: Covent Garden (Piccadilly), Leicester Square (Northern/Piccadilly), Holborn (Central/Piccadilly)', 'Supermarkets: Tesco Express on The Strand, Sainsbury\'s Local on Kingsway', 'Plenty of pharmacies, ATMs, and late-night shops in the area'] },
    { title: '🌡️ Weather', items: ['Early June averages 15–22°C (59–72°F)', 'Sunset around 9:15pm — long, light evenings', 'Rain is always possible — pack a compact umbrella and light layers', 'Sunscreen for park days — UV can be moderate even under clouds'] },
    { title: '💳 Money & Tips', items: ['British Pound (£) — contactless accepted almost everywhere', 'Tipping: 10–12.5% at restaurants (check if service charge is included)', 'Kids under 11 ride free on Tube and buses with paying adult', 'Many museums are free — take advantage of this!'] },
    { title: '👨‍👩‍👧‍👦 Family Tips', items: ['Most attractions have baby-changing facilities', 'Pushchairs are fine on buses but awkward on the Tube (lots of stairs)', 'Pack snacks — London attraction cafés are pricey', 'The Tube can be hot in summer — carry water bottles'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
