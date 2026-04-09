const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771254018189_tr59kf',
  email: 'casabeccaescapes@gmail.com',
  destination: 'Lanzarote, Spain',
  dates: 'Jan 6 – Jan 13, 2027',
  groupSize: '3-4',
  travelStyle: 'Family-friendly',
  dining: 'Casual',
  budget: 'Under $1,000',
  specialRequests: 'none'
};

const itineraryData = {
  destination: 'Lanzarote, Spain',
  countryEmoji: '🇪🇸',
  title: 'Lanzarote Family Escape',
  subtitle: '7 Days of Volcanic Wonders & Beach Bliss',
  description: 'A week-long family adventure through Lanzarote\'s surreal volcanic landscapes, golden beaches, and César Manrique\'s artistic legacy — all on a budget.',
  duration: '7 nights',
  dates: 'Jan 6 – Jan 13, 2027',
  budget: 'Under $1,000',
  pace: 'Relaxed',
  bestFor: 'Families with kids',
  highlights: [
    'Timanfaya National Park camel rides',
    'Jameos del Agua underground lagoon',
    'Papagayo beach coves',
    'César Manrique Foundation',
    'Cueva de los Verdes lava tube'
  ],

  essentials: [
    { title: '🌋 Volcanic Island', text: 'Lanzarote is a UNESCO Biosphere Reserve with otherworldly lava fields, over 300 volcanic cones, and year-round mild weather (18-22°C in January).' },
    { title: '🎨 César Manrique', text: 'The island\'s beloved artist-architect shaped Lanzarote\'s identity. His sites blend art with nature and are must-visits. Buy a multi-attraction pass (CACT) to save money.' },
    { title: '🚗 Getting Around', text: 'Rent a car — it\'s the cheapest and most flexible way to explore. Budget ~€15-20/day. The island is small (60km long) so nowhere is far.' },
    { title: '💶 Budget Tips', text: 'Eat "menú del día" lunches (€8-12 for 3 courses). Buy groceries at HiperDino supermarkets. CACT pass covers 6 attractions for ~€35/adult.' },
    { title: '🏖️ Beach Gear', text: 'Bring reef shoes for rocky entries, sun cream (UV is strong even in winter), and snorkel gear for Papagayo and Playa Chica.' },
    { title: '👨‍👩‍👧‍👦 Family Friendly', text: 'Lanzarote is very family-oriented. Most beaches are calm, restaurants welcome kids, and attractions have child pricing. January is low season — fewer crowds.' }
  ],

  days: [
    {
      num: 1,
      neighborhoods: 'Arrecife · Costa Teguise',
      title: 'Arrival & Coastal Stroll',
      description: 'Settle in, stretch your legs along the coast, and enjoy your first Canarian sunset.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            { title: 'Arrive at César Manrique Airport (ACE)', description: 'Pick up your rental car and drive to your accommodation. Costa Teguise and Puerto del Carmen are the best family bases.', details: ['💡 Book car rental in advance — from €15/day with AutoReisen or Cicar'] },
            { title: 'Explore Arrecife Waterfront', description: 'Stroll along the Charco de San Ginés, a picturesque tidal lagoon in the capital lined with white houses and bobbing fishing boats.', details: ['🕐 Allow 30-45 minutes', '📍 Free to explore'] }
          ],
          tips: [{ type: 'tip', text: 'Pick up groceries and snacks at HiperDino near your accommodation to save on meals throughout the trip.' }]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Lilium Restaurant & Bar', description: 'Casual waterfront dining in Arrecife with fresh fish and Canarian tapas. Kid-friendly atmosphere.', meta: '€€ · Arrecife · Seafood & Tapas' }
          ]
        }
      ],
      mapPins: [
        { lat: 28.9507, lng: -13.6056, label: 'César Manrique Airport', num: 1, cat: 'transport', desc: 'Lanzarote airport — pick up rental car' },
        { lat: 28.9630, lng: -13.5480, label: 'Charco de San Ginés', num: 2, cat: 'attraction', desc: 'Picturesque tidal lagoon in Arrecife' },
        { lat: 28.9640, lng: -13.5470, label: 'Lilium Restaurant', num: 3, cat: 'food', desc: 'Casual waterfront seafood and tapas' }
      ]
    },
    {
      num: 2,
      neighborhoods: 'Timanfaya · Yaiza',
      title: 'Fire Mountains & Volcanic Drama',
      description: 'Experience Lanzarote\'s most iconic landscape — the surreal lava fields and fire mountains of Timanfaya National Park.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Timanfaya National Park', description: 'Take the guided coach tour through the Montañas del Fuego (Fire Mountains). Watch geothermal demonstrations where water turns to steam and straw ignites from underground heat. Kids love it.', details: ['🎟️ €12 adult / €6 child (included in CACT pass)', '🕐 Allow 2-3 hours including queue', '💡 Arrive by 10am to beat crowds'] },
            { title: 'Camel Rides at Echadero de los Camellos', description: 'Just outside Timanfaya, take a short camel ride across the volcanic terrain. A highlight for kids and adults alike.', details: ['🎟️ ~€6 per person for a 20-minute ride', '📍 Right at the park entrance'] }
          ]
        },
        {
          label: 'Afternoon',
          meals: [
            { type: '🍽️ Lunch', name: 'La Era Restaurant, Yaiza', description: 'Traditional Canarian cuisine in a charming old farmhouse. Try the grilled goat cheese with mojo sauce.', meta: '€€ · Yaiza · Canarian · Menú del día ~€12' }
          ],
          activities: [
            { title: 'Explore Yaiza Village', description: 'One of Spain\'s prettiest villages — whitewashed houses, bougainvillea, and a peaceful central square. Perfect for a post-lunch wander.', details: ['📍 Free to explore', '🕐 30-45 minutes'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'El Golfo & Lago Verde', description: 'Drive to the coast to see the stunning green lagoon (Charco de los Cliclos) inside a half-submerged volcanic crater. Spectacular at sunset.', details: ['📍 Free — short walk from car park', '💡 The green color comes from algae — totally natural'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Casa Roja, El Golfo', description: 'Fresh-off-the-boat seafood right on the waterfront. Famous for limpets (lapas) and grilled fish.', meta: '€€ · El Golfo · Seafood' }
          ]
        }
      ],
      mapPins: [
        { lat: 29.0136, lng: -13.7507, label: 'Timanfaya National Park', num: 1, cat: 'attraction', desc: 'Fire Mountains coach tour and geothermal demos' },
        { lat: 29.0060, lng: -13.7560, label: 'Echadero de los Camellos', num: 2, cat: 'attraction', desc: 'Camel rides across volcanic terrain' },
        { lat: 28.9526, lng: -13.7640, label: 'La Era Restaurant', num: 3, cat: 'food', desc: 'Traditional Canarian farmhouse dining' },
        { lat: 28.9510, lng: -13.7650, label: 'Yaiza Village', num: 4, cat: 'attraction', desc: 'One of Spain\'s prettiest whitewashed villages' },
        { lat: 28.9720, lng: -13.8230, label: 'El Golfo & Lago Verde', num: 5, cat: 'attraction', desc: 'Green lagoon in a volcanic crater' },
        { lat: 28.9715, lng: -13.8210, label: 'Casa Roja', num: 6, cat: 'food', desc: 'Fresh seafood by the waterfront' }
      ]
    },
    {
      num: 3,
      neighborhoods: 'Haría · Northern Lanzarote',
      title: 'Underground Wonders & the Valley of 1000 Palms',
      description: 'Dive into Lanzarote\'s volcanic underworld with two spectacular lava tube experiences, then explore the lush north.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Jameos del Agua', description: 'César Manrique transformed this lava tube into a jaw-dropping cultural space with an underground lagoon home to blind albino crabs found nowhere else on Earth. The tropical garden, pool, and auditorium are magical.', details: ['🎟️ €10 adult / €5 child (CACT pass)', '🕐 Allow 1-1.5 hours', '💡 Kids love spotting the tiny white crabs'] },
            { title: 'Cueva de los Verdes', description: 'A guided walk through 1km of a massive lava tube formed 3,000 years ago. Dramatic lighting and a surprise ending that delights everyone.', details: ['🎟️ €10 adult / €5 child (CACT pass)', '🕐 50-minute guided tour', '💡 Just 5 min drive from Jameos del Agua — do both!'] }
          ]
        },
        {
          label: 'Afternoon',
          meals: [
            { type: '🍽️ Lunch', name: 'El Mirador de Haría', description: 'Casual restaurant with panoramic views over the Valley of a Thousand Palms. Great grilled meats and salads.', meta: '€€ · Haría · Canarian' }
          ],
          activities: [
            { title: 'Haría Saturday Market (or town stroll)', description: 'If it\'s Saturday, catch the artisan market. Otherwise, wander the charming streets of this palm-filled village, the greenest spot on the island.', details: ['📍 Free to explore', '🌿 César Manrique lived here — his home is now a museum'] }
          ]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Mirador del Río', description: 'Manrique-designed viewpoint perched on 475m cliffs with breathtaking views over La Graciosa island and the strait. The café inside is built into the cliff.', details: ['🎟️ €5 adult / €2.50 child (CACT pass)', '🕐 30-45 minutes', '📸 One of the most photogenic spots in all of Spain'] }
          ],
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurante El Risco', description: 'Hidden gem in Famara cliff area. Fresh fish, stunning views, and very reasonable prices.', meta: '€-€€ · Famara · Seafood' }
          ]
        }
      ],
      mapPins: [
        { lat: 29.1570, lng: -13.4320, label: 'Jameos del Agua', num: 1, cat: 'attraction', desc: 'Manrique\'s underground lagoon with blind crabs' },
        { lat: 29.1590, lng: -13.4350, label: 'Cueva de los Verdes', num: 2, cat: 'attraction', desc: '1km lava tube guided tour' },
        { lat: 29.1450, lng: -13.4980, label: 'Haría Village', num: 3, cat: 'attraction', desc: 'Valley of a Thousand Palms' },
        { lat: 29.1460, lng: -13.4970, label: 'El Mirador de Haría', num: 4, cat: 'food', desc: 'Panoramic views and Canarian cuisine' },
        { lat: 29.2140, lng: -13.4810, label: 'Mirador del Río', num: 5, cat: 'attraction', desc: 'Cliff-top viewpoint over La Graciosa' },
        { lat: 29.1110, lng: -13.5590, label: 'Restaurante El Risco', num: 6, cat: 'food', desc: 'Fresh fish with cliff views' }
      ]
    },
    {
      num: 4,
      neighborhoods: 'Teguise · Fundación César Manrique',
      title: 'Art, History & Manrique\'s Masterpiece',
      description: 'Explore the island\'s cultural heart — the old capital of Teguise and the incredible César Manrique Foundation built inside volcanic bubbles.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Fundación César Manrique', description: 'Manrique\'s former home, built over five volcanic bubbles (jameos). Each bubble is a unique living space — a pool in one, a garden in another. His art collection and the architecture itself are unforgettable.', details: ['🎟️ €10 adult / €1 child (CACT pass)', '🕐 Allow 1.5-2 hours', '⭐ The absolute #1 must-see on Lanzarote'] }
          ]
        },
        {
          label: 'Midday',
          activities: [
            { title: 'Teguise Old Town', description: 'The former capital of Lanzarote, with beautiful colonial architecture, churches, and craft shops. If visiting on Sunday, the famous Teguise Market fills the streets with 400+ stalls.', details: ['📍 Free to wander', '🛍️ Sunday market 9am-2pm is the island\'s biggest'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'La Cantina, Teguise', description: 'Relaxed courtyard café in a historic building. Tapas, wrinkled potatoes (papas arrugadas) with mojo, and fresh juices.', meta: '€ · Teguise · Tapas & Light Bites' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Castillo de Santa Bárbara & Piracy Museum', description: 'Hilltop castle with panoramic views and a quirky museum about the island\'s history of pirate attacks. Kids find it fascinating.', details: ['🎟️ €3 adult', '🕐 45 minutes', '📍 Short drive up from Teguise'] }
          ],
          tips: [{ type: 'tip', text: 'Head back to your accommodation for pool time. January water temp is ~19°C — refreshing but swimmable for brave kids!' }]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurante Hespérides, Costa Teguise', description: 'Family-friendly restaurant near the beach with pizzas, pasta, and local fish. Great value menú del día.', meta: '€-€€ · Costa Teguise · International & Canarian' }
          ]
        }
      ],
      mapPins: [
        { lat: 29.0050, lng: -13.5580, label: 'Fundación César Manrique', num: 1, cat: 'attraction', desc: 'Artist\'s home built in volcanic bubbles' },
        { lat: 29.0610, lng: -13.5620, label: 'Teguise Old Town', num: 2, cat: 'attraction', desc: 'Historic former capital with Sunday market' },
        { lat: 29.0615, lng: -13.5615, label: 'La Cantina', num: 3, cat: 'food', desc: 'Courtyard café with tapas and papas arrugadas' },
        { lat: 29.0680, lng: -13.5560, label: 'Castillo de Santa Bárbara', num: 4, cat: 'attraction', desc: 'Hilltop castle and piracy museum' },
        { lat: 29.0670, lng: -13.4950, label: 'Costa Teguise', num: 5, cat: 'area', desc: 'Family resort area with beaches and restaurants' }
      ]
    },
    {
      num: 5,
      neighborhoods: 'Papagayo · Playa Blanca',
      title: 'Paradise Beaches',
      description: 'A full beach day at Lanzarote\'s most stunning coves — the golden Papagayo beaches on the southern tip.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Playas de Papagayo', description: 'A string of pristine golden sand coves with crystal-clear turquoise water, sheltered from the wind. Playa de Papagayo and Playa Mujeres are the standouts. The water is calm and shallow — perfect for kids.', details: ['🚗 €3 car entry to the natural park', '🕐 Spend the whole morning here', '💡 Bring food and water — there\'s one basic chiringuito but it\'s pricey', '🤿 Great snorkeling off the rocks between coves'] }
          ]
        },
        {
          label: 'Afternoon',
          meals: [
            { type: '🍽️ Lunch', name: 'Chiringuito Papagayo', description: 'The only beach bar at Papagayo. Simple but you can\'t beat the setting. Alternatively, pack a picnic from HiperDino.', meta: '€€ · Papagayo Beach · Snacks & Drinks' }
          ],
          activities: [
            { title: 'Playa Blanca Promenade', description: 'Head into Playa Blanca town for ice cream and a stroll along the seafront promenade. Browse the shops and enjoy the relaxed southern vibe.', details: ['📍 Free', '🍦 Several gelato shops along the promenade'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'La Ola Restaurant, Playa Blanca', description: 'Beachfront dining with gorgeous sunset views. Fresh grilled fish, paella, and a solid kids\' menu.', meta: '€€ · Playa Blanca · Seafood & Mediterranean' }
          ]
        }
      ],
      mapPins: [
        { lat: 28.8440, lng: -13.7830, label: 'Playa de Papagayo', num: 1, cat: 'beach', desc: 'Stunning golden sand cove with calm turquoise water' },
        { lat: 28.8470, lng: -13.7900, label: 'Playa Mujeres', num: 2, cat: 'beach', desc: 'Sheltered family-friendly cove' },
        { lat: 28.8600, lng: -13.8200, label: 'Playa Blanca Promenade', num: 3, cat: 'attraction', desc: 'Seaside stroll with shops and ice cream' },
        { lat: 28.8610, lng: -13.8220, label: 'La Ola Restaurant', num: 4, cat: 'food', desc: 'Beachfront seafood with sunset views' }
      ]
    },
    {
      num: 6,
      neighborhoods: 'La Geria · Puerto del Carmen',
      title: 'Wine Country & Surf Town Vibes',
      description: 'Discover Lanzarote\'s unique wine-growing region where vines grow in volcanic craters, then enjoy the island\'s liveliest beach town.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'La Geria Wine Region', description: 'Lanzarote\'s surreal wine valley where each vine is sheltered in a hand-dug pit (hoyo) with a semicircular stone wall. Visit a bodega for a tasting — Malvasía white wine is the local star. Kids can have grape juice and explore the lunar landscape.', details: ['🍷 Bodega La Geria: tastings from €5', '🕐 Allow 1-1.5 hours', '📍 The drive through La Geria is scenic — stop for photos'] }
          ]
        },
        {
          label: 'Midday',
          activities: [
            { title: 'Monumento al Campesino', description: 'Another Manrique creation — a striking white sculpture and a small museum/restaurant celebrating Lanzarote\'s farming heritage. The restaurant serves traditional food cooked over a wood fire.', details: ['📍 Free to visit the monument', '🎟️ Museum: €6 (CACT pass)'] }
          ],
          meals: [
            { type: '🍽️ Lunch', name: 'Monumento al Campesino Restaurant', description: 'Eat in the traditional farmhouse setting. Excellent papas arrugadas, grilled meats, and local cheeses. Very affordable.', meta: '€ · San Bartolomé · Canarian' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Puerto del Carmen Beaches', description: 'Hit Playa Grande or Playa Chica for a relaxed afternoon. Playa Chica is a sheltered cove that\'s great for snorkeling. Puerto del Carmen has the best variety of casual restaurants on the island.', details: ['🏖️ Playa Grande: wide sandy beach, calm water', '🤿 Playa Chica: top snorkeling spot'] }
          ]
        },
        {
          label: 'Evening',
          meals: [
            { type: '🍽️ Dinner', name: 'Restaurante El Tomate, Puerto del Carmen', description: 'Popular family restaurant with a huge menu — burgers, fresh fish, pasta, steaks. Big portions and very reasonable prices.', meta: '€-€€ · Puerto del Carmen · International' }
          ]
        }
      ],
      mapPins: [
        { lat: 29.0090, lng: -13.6830, label: 'Bodega La Geria', num: 1, cat: 'attraction', desc: 'Wine tasting in volcanic vine pits' },
        { lat: 29.0180, lng: -13.6280, label: 'Monumento al Campesino', num: 2, cat: 'attraction', desc: 'Manrique sculpture and traditional restaurant' },
        { lat: 28.9230, lng: -13.6430, label: 'Playa Grande', num: 3, cat: 'beach', desc: 'Main beach in Puerto del Carmen' },
        { lat: 28.9200, lng: -13.6340, label: 'Playa Chica', num: 4, cat: 'beach', desc: 'Sheltered cove — great snorkeling' },
        { lat: 28.9220, lng: -13.6400, label: 'Restaurante El Tomate', num: 5, cat: 'food', desc: 'Casual family restaurant with big portions' }
      ]
    },
    {
      num: 7,
      neighborhoods: 'Famara · Caleta de Famara',
      title: 'Surf, Cliffs & Farewell',
      description: 'End the trip at Lanzarote\'s most dramatic beach — the wild, windswept Famara with its towering cliffs — before heading to the airport.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            { title: 'Playa de Famara', description: 'A 6km stretch of golden sand backed by 600m cliffs — the most dramatic beach in the Canary Islands. Popular with surfers but the wide sands are perfect for building sandcastles and running around. The views of La Graciosa island are incredible.', details: ['⚠️ Currents can be strong — stay in the shallows with kids', '🏄 Surf lessons available for older kids (~€35/person)', '📍 Free'] }
          ],
          meals: [
            { type: '🍽️ Brunch', name: 'El Risco Café, Caleta de Famara', description: 'Laid-back surf café with great coffee, açaí bowls, and pancakes. The chilled Famara vibe at its best.', meta: '€ · Famara · Café & Brunch' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            { title: 'Jardín de Cactus', description: 'Manrique\'s last major work — a beautiful cactus garden built in an old quarry with over 4,500 cacti from around the world. The windmill on top and the café inside are lovely.', details: ['🎟️ €6.50 adult / €3.25 child (CACT pass)', '🕐 Allow 45 minutes-1 hour', '🌵 Kids love the weird and wonderful cacti shapes'] }
          ],
          tips: [{ type: 'tip', text: 'If your flight is later, this is a perfect last stop — it\'s between Famara and the airport.' }]
        },
        {
          label: 'Evening',
          activities: [
            { title: 'Departure', description: 'Return your rental car and head to the airport. ¡Hasta luego, Lanzarote!', details: ['✈️ ACE airport is compact — arrive 2 hours before your flight'] }
          ]
        }
      ],
      mapPins: [
        { lat: 29.1110, lng: -13.5560, label: 'Playa de Famara', num: 1, cat: 'beach', desc: '6km dramatic beach with towering cliffs' },
        { lat: 29.1080, lng: -13.5530, label: 'El Risco Café', num: 2, cat: 'food', desc: 'Surf café with açaí bowls and pancakes' },
        { lat: 29.0760, lng: -13.4570, label: 'Jardín de Cactus', num: 3, cat: 'attraction', desc: 'Manrique\'s cactus garden with 4,500+ cacti' },
        { lat: 28.9507, lng: -13.6056, label: 'César Manrique Airport', num: 4, cat: 'transport', desc: 'Departure — return rental car' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (7 nights)', budget: '€350-450', notes: 'Apartment/Airbnb with kitchen' },
    { category: 'Rental Car (7 days)', budget: '€105-140', notes: '€15-20/day with basic insurance' },
    { category: 'Fuel', budget: '€30-40', notes: 'Island is small — one tank is enough' },
    { category: 'CACT Pass (2 adults)', budget: '€70', notes: 'Covers 6 Manrique attractions' },
    { category: 'Other Attractions', budget: '€30-40', notes: 'Camel ride, Papagayo parking, etc.' },
    { category: 'Food & Dining', budget: '€250-300', notes: 'Mix of restaurants, grocery cooking, and picnics' },
    { category: 'TOTAL', budget: '€835-990', notes: 'Well under $1,000 at current rates' }
  ],

  practicalInfo: [
    {
      title: '🛫 Getting There',
      items: [
        'Fly to César Manrique-Lanzarote Airport (ACE). Budget airlines like Ryanair and easyJet serve it from most European cities.',
        'Airport is 5km from Arrecife. Rental car desks are in the terminal.',
        'No public transport worth relying on — rent a car.'
      ]
    },
    {
      title: '💡 Money-Saving Tips',
      items: [
        'Buy the CACT 6-centre pass (~€35/adult) — covers Timanfaya, Jameos del Agua, Cueva de los Verdes, Mirador del Río, Jardín de Cactus, and MIAC.',
        'Kids under 7 are free at most attractions; 7-12 get ~50% off.',
        'Cook breakfast and some dinners in your apartment kitchen — HiperDino supermarkets are everywhere.',
        'Menú del día (lunch set menu) at local restaurants: €8-12 for starter, main, dessert, and a drink.',
        'January is low season — accommodation is 30-50% cheaper than summer.'
      ]
    },
    {
      title: '🌤️ Weather in January',
      items: [
        'Daytime: 18-22°C (64-72°F) — pleasant but bring a light jacket for evenings.',
        'Sea temperature: ~19°C (66°F) — swimmable but refreshing.',
        'Occasional rain but mostly sunny. UV is strong — wear sunscreen.',
        'Wind can be brisk, especially on northern/western beaches.'
      ]
    },
    {
      title: '👨‍👩‍👧‍👦 Family Tips',
      items: [
        'Papagayo and Playa Dorada (Playa Blanca) are the calmest beaches for young kids.',
        'Most restaurants are very welcoming to families — eating out with kids is normal in Spain.',
        'Bring reef shoes for volcanic rock beaches.',
        'Rent snorkel gear in Puerto del Carmen or Playa Blanca (€5-8/day).',
        'Car seats: book with your rental car or bring your own.'
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Itinerary fulfilled!');
console.log('URL:', result.url);
console.log('Slug:', result.slug);
console.log('Email sent:', result.emailSent);
