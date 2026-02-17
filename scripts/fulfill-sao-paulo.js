const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771276879137_kryzuw',
  email: 'bernard.j.huang@gmail.com',
  destination: 'São Paulo, Brazil',
};

const itineraryData = {
  destination: 'São Paulo, Brazil',
  countryEmoji: '🇧🇷',
  title: 'São Paulo: A Culinary & Cultural Odyssey',
  subtitle: "Seven days exploring Brazil's vibrant mega-city — world-class food, street art, museums & hidden neighborhoods",
  description: "São Paulo is South America's largest city and one of the world's great food capitals. This 7-day itinerary blends iconic museums (MASP, Pinacoteca), vibrant neighborhoods (Vila Madalena, Liberdade, Jardins), legendary street food, and fine dining — all at a mid-range budget that lets you experience SP like a local.",
  duration: '7 nights',
  dates: 'Mar 14 – Mar 21, 2026',
  budget: '$2,000 – $5,000',
  pace: 'Moderate',
  bestFor: 'Groups of 3-4, Food lovers, Culture seekers',
  highlights: ['MASP & Pinacoteca museums', 'Mercado Municipal', 'Beco do Batman street art', 'Ibirapuera Park', 'Liberdade Japanese quarter', 'World-class dining scene'],

  essentials: [
    { title: '🛬 Getting Around', text: 'Use the Metrô (clean, fast) and ride-hailing apps (99, Uber). Avoid driving — traffic is legendary. A BILHETE ÚNICO card works on buses and metro.' },
    { title: '💵 Money', text: 'Brazilian Real (BRL). Credit cards widely accepted. Budget ~R$150-300/person/day for food. ATMs at Bradesco/Itaú work with international cards.' },
    { title: '🗣️ Language', text: 'Portuguese is the language. English is limited outside tourist areas. Google Translate helps; locals appreciate any attempt at Portuguese.' },
    { title: '🌦️ Weather in March', text: 'Late summer — warm and humid, 22-30°C (72-86°F). Afternoon rain showers are common. Bring an umbrella and light layers.' },
    { title: '🔒 Safety', text: 'Normal big-city precautions. Avoid flashing expensive items. Stick to well-lit areas at night. Uber/99 after dark is safest.' },
    { title: '🍽️ Dining Culture', text: "Paulistanos eat late — lunch 12-2pm, dinner 8-10pm. Many restaurants are closed Mondays. 'Rodízio' means all-you-can-eat. Tips: 10% is standard (often included)." },
  ],

  days: [
    // DAY 1 — Arrival + Centro Histórico
    {
      num: 1,
      title: 'Arrival & Centro Histórico',
      neighborhoods: 'Centro · República · Luz',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle In',
              description: 'Check into your hotel. Rest up after the flight, then head out to explore.',
              details: ['Recommended area to stay: Jardins or Pinheiros — central, safe, walkable']
            },
            {
              title: 'Edifício Itália Observation Deck',
              description: 'Head to the top of one of SP\'s tallest buildings for panoramic city views. The Terraço Itália restaurant on the 41st floor offers drinks with a stunning sunset vista.',
              details: ['📍 Av. Ipiranga, 344 — Centro', '💰 Minimum consumption ~R$80/person for the view']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'A Casa do Porco',
              description: 'Ranked among the world\'s best restaurants. Famous for creative pork dishes — the porco san zé tasting menu is unforgettable.',
              meta: '📍 Rua Araújo, 124 — República · 💰 R$120-200/person · ⚠️ Book weeks ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book A Casa do Porco ASAP — it fills up fast. Check their Instagram for reservation openings.' }
          ]
        }
      ],
      mapPins: [
        { lat: -23.5445, lng: -46.6507, label: 'Edifício Itália', num: 1, cat: 'attraction', desc: 'Panoramic city views from the 41st floor' },
        { lat: -23.5432, lng: -46.6459, label: 'A Casa do Porco', num: 2, cat: 'food', desc: 'World-famous pork restaurant' }
      ]
    },

    // DAY 2 — Pinacoteca, Luz & Mercado Municipal
    {
      num: 2,
      title: 'Art, History & the Great Market',
      neighborhoods: 'Luz · Centro · Sé',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Pinacoteca do Estado',
              description: "São Paulo's oldest art museum (1905) houses an exceptional collection of Brazilian art from the 19th century to contemporary works. The building itself — a stunning brick structure by Ramos de Azevedo — is worth the visit.",
              details: ['📍 Praça da Luz, 2 — Luz', '🕐 Wed-Mon 10am-5:30pm · 💰 R$30 (free on Saturdays)']
            },
            {
              title: 'Jardim da Luz',
              description: 'Stroll through SP\'s oldest public park, right next to the Pinacoteca. Beautiful gardens and sculptures.',
              details: ['📍 Adjacent to Pinacoteca — free entry']
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'Padaria Santa Tereza',
              description: 'Classic São Paulo bakery experience. Try pão de queijo (cheese bread) and a strong cafezinho.',
              meta: '📍 Rua Santa Tereza — Luz · 💰 R$15-25/person'
            }
          ],
          tips: []
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Mercado Municipal (Mercadão)',
              description: "SP's legendary 1933 market. Stunning stained-glass windows and an overwhelming selection of tropical fruits, spices, dried meats, and cheeses. The famous mortadella sandwich and pastel de bacalhau are must-tries.",
              details: ['📍 Rua da Cantareira, 306 — Centro', '🕐 Mon-Sat 6am-6pm, Sun 6am-4pm', '💰 Mortadella sandwich ~R$35, Pastel de bacalhau ~R$40']
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Hocca Bar (inside Mercadão)',
              description: 'The original home of SP\'s iconic mortadella sandwich — piled high with thinly sliced mortadella, melted cheese, and a tangy sauce.',
              meta: '📍 Inside Mercado Municipal · 💰 R$30-45/person'
            }
          ],
          tips: [
            { type: 'tip', text: 'Go to Mercadão early (before 10am) to avoid the biggest crowds. Upstairs vendors tend to be pricier — shop ground floor for better deals.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Catedral da Sé',
              description: "One of the world's largest neo-Gothic churches. The cathedral's crypt contains the remains of indigenous chief Tibiriçá. Praça da Sé in front is the symbolic center of São Paulo.",
              details: ['📍 Praça da Sé — Centro · Free entry']
            },
            {
              title: 'Pátio do Colégio',
              description: 'The literal birthplace of São Paulo — where Jesuit priests founded the city in 1554. Small museum inside.',
              details: ['📍 Praça Pátio do Colégio, 2 — Centro · 💰 R$15']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bar da Dona Onça',
              description: 'Chef Janaína Torres\' beloved boteco serving elevated Brazilian comfort food — try the bolinho de arroz and picanha.',
              meta: '📍 Edifício Copan, Av. Ipiranga, 200 — Centro · 💰 R$70-120/person'
            }
          ],
          tips: [
            { type: 'tip', text: 'While at Copan, admire the iconic Oscar Niemeyer-designed building — it\'s the largest residential building in the world.' }
          ]
        }
      ],
      mapPins: [
        { lat: -23.5342, lng: -46.6343, label: 'Pinacoteca do Estado', num: 1, cat: 'attraction', desc: "SP's oldest art museum with Brazilian masterpieces" },
        { lat: -23.5352, lng: -46.6340, label: 'Jardim da Luz', num: 2, cat: 'attraction', desc: 'Oldest public park in São Paulo' },
        { lat: -23.5416, lng: -46.6296, label: 'Mercado Municipal', num: 3, cat: 'food', desc: 'Legendary 1933 market — mortadella sandwiches & tropical fruit' },
        { lat: -23.5503, lng: -46.6345, label: 'Catedral da Sé', num: 4, cat: 'attraction', desc: 'Massive neo-Gothic cathedral at the heart of SP' },
        { lat: -23.5484, lng: -46.6340, label: 'Pátio do Colégio', num: 5, cat: 'attraction', desc: 'Birthplace of São Paulo (1554)' },
        { lat: -23.5465, lng: -46.6502, label: 'Bar da Dona Onça', num: 6, cat: 'food', desc: 'Elevated Brazilian comfort food inside Edifício Copan' }
      ]
    },

    // DAY 3 — Paulista Avenue & MASP
    {
      num: 3,
      title: 'Avenida Paulista & MASP',
      neighborhoods: 'Paulista · Bela Vista · Jardins',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'MASP — Museu de Arte de São Paulo',
              description: "South America's most important art museum. The brutalist building by Lina Bo Bardi is iconic — paintings displayed on glass easels create a unique 'crystal gallery' experience. Collection includes Renoir, Van Gogh, Picasso, and major Brazilian artists.",
              details: ['📍 Av. Paulista, 1578 — Bela Vista', '🕐 Tue-Sun 10am-6pm (Thu until 8pm) · 💰 R$50 (free Tuesdays)']
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Café Girondino',
              description: 'Traditional SP café since 1997 — excellent coffee, fresh-baked pastries, and a classic paulistano atmosphere.',
              meta: '📍 Rua Boa Vista, 365 — Centro · 💰 R$20-35/person'
            }
          ],
          tips: [
            { type: 'tip', text: 'Visit MASP on a Tuesday for free entry, or Thursday for extended evening hours.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Walk Avenida Paulista',
              description: "SP's most iconic boulevard. Walk from MASP toward Consolação — pass cultural centers (Japan House, Instituto Moreira Salles, SESC Paulista), street performers, and people-watching galore.",
              details: ['📍 Av. Paulista stretches ~2.8km', '🎨 Japan House (free) is a gem — rotating exhibits on Japanese design and culture']
            },
            {
              title: 'Rua Augusta & Jardins',
              description: 'Cross from Paulista down Rua Augusta into Jardins — SP\'s upscale neighborhood. Browse designer boutiques on Rua Oscar Freire, or explore the funkier Baixo Augusta strip.',
              details: ['📍 Rua Oscar Freire — Jardins · Great for shopping and café-hopping']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Bráz Pizzaria',
              description: 'São Paulo is the pizza capital of Latin America. Bráz serves Neapolitan-style pies with Brazilian flair — the margherita with buffalo mozzarella is perfect.',
              meta: '📍 Rua Graúna, 125 — Moema (or other locations) · 💰 R$50-80/person'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mocotó',
              description: 'Chef Rodrigo Oliveira\'s celebration of Northeastern Brazilian cuisine. Famous for the mocotó (cow-foot soup), dadinhos de tapioca, and baião de dois. Consistently ranked among Latin America\'s best.',
              meta: '📍 Av. Nossa Sra. do Loreto, 1100 — Vila Medeiros · 💰 R$80-140/person · 🚗 Worth the Uber ride'
            }
          ],
          tips: [
            { type: 'tip', text: 'Mocotó is in the north zone — 30min by Uber from Jardins. Go hungry, order family-style, and share everything.' }
          ]
        }
      ],
      mapPins: [
        { lat: -23.5614, lng: -46.6558, label: 'MASP', num: 1, cat: 'attraction', desc: "South America's premier art museum" },
        { lat: -23.5629, lng: -46.6554, label: 'Avenida Paulista', num: 2, cat: 'attraction', desc: "SP's iconic boulevard — cultural centers and street life" },
        { lat: -23.5638, lng: -46.6721, label: 'Japan House', num: 3, cat: 'attraction', desc: 'Free exhibits on Japanese design and culture' },
        { lat: -23.5636, lng: -46.6690, label: 'Rua Oscar Freire', num: 4, cat: 'shopping', desc: 'Upscale shopping street in Jardins' },
        { lat: -23.4867, lng: -46.5799, label: 'Mocotó', num: 5, cat: 'food', desc: 'Legendary Northeastern Brazilian cuisine' }
      ]
    },

    // DAY 4 — Vila Madalena & Pinheiros
    {
      num: 4,
      title: 'Street Art, Vinyl & Craft Beer',
      neighborhoods: 'Vila Madalena · Pinheiros',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Beco do Batman (Batman Alley)',
              description: "Vila Madalena's famous open-air street art gallery. This narrow alleyway and surrounding streets are completely covered in vibrant, ever-changing murals and graffiti by local and international artists.",
              details: ['📍 Rua Gonçalo Afonso — Vila Madalena', '🎨 Free, open 24/7 — best light for photos in the morning']
            },
            {
              title: 'Wander Vila Madalena',
              description: "SP's bohemian neighborhood. Browse indie art galleries, vintage shops, and vinyl record stores. Rua Aspicuelta and Rua Harmonia are the main drags.",
              details: ['📍 Start at Beco do Batman and wander south toward Rua Aspicuelta']
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Coffee Lab',
              description: 'Award-winning specialty coffee roaster. Try their pour-over single-origin Brazilian beans — considered some of the best coffee in the city.',
              meta: '📍 Rua Fradique Coutinho, 1340 — Vila Madalena · 💰 R$20-40/person'
            }
          ],
          tips: [
            { type: 'tip', text: 'Vila Madalena is where SP\'s art scene lives. Check if there\'s a gallery opening or street fair happening — especially vibrant on weekends.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pinheiros Neighborhood & Feira de Antiguidades',
              description: 'Walk south into Pinheiros — more polished but equally creative. Browse the antique shops along Rua Cardeal Arcoverde. On Saturdays, the Praça Benedito Calixto antique fair is a highlight.',
              details: ['📍 Praça Benedito Calixto — Pinheiros', '🕐 Antique fair: Saturdays 9am-5pm']
            },
            {
              title: 'Instituto Tomie Ohtake',
              description: "Striking contemporary art museum with free rotating exhibitions in a colorful building. Named after the renowned Japanese-Brazilian artist.",
              details: ['📍 Av. Faria Lima, 201 — Pinheiros', '🕐 Tue-Sun 11am-8pm · Free']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Banana Verde',
              description: 'Creative vegetarian restaurant using Brazilian ingredients — banana is the star. The moqueca de banana da terra is a tropical twist on the Bahian classic.',
              meta: '📍 Rua Cônego Eugênio Leite, 324 — Pinheiros · 💰 R$40-65/person'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Craft Beer Crawl — Vila Madalena',
              description: "SP has an exploding craft beer scene. Vila Madalena's bars pour excellent local brews. Hit a few spots along Rua Aspicuelta.",
              details: ['🍺 Try: Cervejaria Nacional, O Torto, BrewDog SP', '💰 Craft pints ~R$20-35']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Maní',
              description: "Chef Helena Rizzo's refined Brazilian cuisine in a chic Jardins setting. Creative tasting menus that reimagine Brazilian ingredients — consistently on Latin America's 50 Best.",
              meta: '📍 Rua Joaquim Antunes, 210 — Jardins · 💰 R$180-280/person · ⚠️ Reserve in advance'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: -23.5567, lng: -46.6867, label: 'Beco do Batman', num: 1, cat: 'attraction', desc: 'Famous open-air street art gallery' },
        { lat: -23.5553, lng: -46.6893, label: 'Coffee Lab', num: 2, cat: 'food', desc: 'Award-winning specialty coffee' },
        { lat: -23.5599, lng: -46.6866, label: 'Praça Benedito Calixto', num: 3, cat: 'attraction', desc: 'Charming square with Saturday antique fair' },
        { lat: -23.5679, lng: -46.6934, label: 'Instituto Tomie Ohtake', num: 4, cat: 'attraction', desc: 'Contemporary art museum — free entry' },
        { lat: -23.5617, lng: -46.6827, label: 'Vila Madalena Bars', num: 5, cat: 'nightlife', desc: 'Craft beer crawl along Rua Aspicuelta' },
        { lat: -23.5672, lng: -46.6750, label: 'Maní', num: 6, cat: 'food', desc: "Chef Helena Rizzo's refined Brazilian cuisine" }
      ]
    },

    // DAY 5 — Ibirapuera Park & Moema
    {
      num: 5,
      title: 'Ibirapuera Park & Southern Neighborhoods',
      neighborhoods: 'Ibirapuera · Moema · Vila Olímpia',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Parque Ibirapuera',
              description: "SP's Central Park — a massive green oasis designed by Oscar Niemeyer and Roberto Burle Marx. Jog the paths, rent a bike, or just soak in the scene. Home to several museums and cultural spaces.",
              details: ['📍 Av. Pedro Álvares Cabral — Ibirapuera', '🕐 5am-midnight · Free entry']
            },
            {
              title: 'MAM — Museu de Arte Moderna',
              description: 'Inside Ibirapuera, MAM houses an excellent modern art collection in a Lina Bo Bardi-designed space. The sculpture garden is serene.',
              details: ['📍 Inside Parque Ibirapuera · 🕐 Tue-Sun 10am-5:30pm · 💰 R$25 (free Sundays)']
            },
            {
              title: 'OCA & Afro Brasil Museum',
              description: 'The dome-shaped OCA pavilion hosts rotating exhibitions. Nearby, the Afro Brasil Museum celebrates the African diaspora\'s profound influence on Brazilian culture.',
              details: ['📍 Inside Parque Ibirapuera · 💰 R$15-25']
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Padoca do Maní',
              description: 'Helena Rizzo\'s casual bakery — artisan breads, pastries, and excellent coffee in a relaxed setting.',
              meta: '📍 Rua Joaquim Antunes, 210 — Jardins · 💰 R$20-35/person'
            }
          ],
          tips: [
            { type: 'tip', text: 'Sunday mornings at Ibirapuera are magical — the park fills with joggers, families, and musicians. Bike rentals available at multiple entrances.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Moema Neighborhood Stroll',
              description: 'Walk south from the park into Moema — a leafy, upscale residential area with excellent restaurants and a village-like feel.',
              details: ['📍 Around Av. Ibirapuera and Alameda dos Arapanés']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Aoyama Sushi',
              description: 'São Paulo has the largest Japanese population outside Japan — and the sushi scene is world-class. Aoyama serves pristine omakase.',
              meta: '📍 Rua Augusta, 1327 — Consolação · 💰 R$100-180/person for omakase'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Vila Olímpia Nightlife',
              description: 'SP\'s upscale entertainment district comes alive after dark. Cocktail lounges, rooftop bars, and clubs line the streets.',
              details: ['🍸 Try: Seen Bar (rooftop at Hotel Tivoli) for sunset cocktails', '📍 Rua Olimpíadas area']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'D.O.M.',
              description: "Alex Atala's flagship — once #4 in the world. Amazonian ingredients meet fine dining: ants with pineapple, hearts of palm fettuccine. A bucket-list meal.",
              meta: '📍 Rua Barão de Capanema, 549 — Jardins · 💰 R$350-500/person (tasting menu) · ⚠️ Reserve well in advance'
            }
          ],
          tips: [
            { type: 'tip', text: "D.O.M. is a splurge, but it's one of the most famous restaurants in Latin America. Worth it for a special night." }
          ]
        }
      ],
      mapPins: [
        { lat: -23.5874, lng: -46.6576, label: 'Parque Ibirapuera', num: 1, cat: 'attraction', desc: "SP's iconic urban park — museums, paths, and green space" },
        { lat: -23.5867, lng: -46.6554, label: 'MAM — Museu de Arte Moderna', num: 2, cat: 'attraction', desc: 'Modern art inside Ibirapuera' },
        { lat: -23.5843, lng: -46.6553, label: 'Afro Brasil Museum', num: 3, cat: 'attraction', desc: "African diaspora's influence on Brazil" },
        { lat: -23.5940, lng: -46.6600, label: 'Moema', num: 4, cat: 'neighborhood', desc: 'Leafy upscale neighborhood south of Ibirapuera' },
        { lat: -23.5652, lng: -46.6565, label: 'D.O.M.', num: 5, cat: 'food', desc: "Alex Atala's iconic fine dining" },
        { lat: -23.5940, lng: -46.6790, label: 'Vila Olímpia', num: 6, cat: 'nightlife', desc: 'Upscale nightlife district' }
      ]
    },

    // DAY 6 — Liberdade & Japanese-Brazilian Culture
    {
      num: 6,
      title: 'Liberdade & East Side Flavors',
      neighborhoods: 'Liberdade · Aclimação · Cambuci',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Liberdade — Japanese Quarter',
              description: "Home to the largest Japanese community outside Japan. Walk under the distinctive red torii gates, browse Asian markets, and soak in the unique blend of Japanese-Brazilian culture. The Sunday street fair (Feira da Liberdade) is a must.",
              details: ['📍 Start at Metrô Liberdade station', '🎌 Torii gates mark the neighborhood entrances']
            },
            {
              title: 'Museu Histórico da Imigração Japonesa',
              description: 'Fascinating museum documenting Japanese immigration to Brazil since 1908. Seven floors of artifacts, photos, and stories.',
              details: ['📍 Rua São Joaquim, 381 — Liberdade', '🕐 Tue-Sun 1:30-5:30pm · 💰 R$16']
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bolo Japonês on the street',
              description: 'Start with Japanese-Brazilian street food — imagawayaki (stuffed sweet pancakes) and taiyaki from vendors along Rua Galvão Bueno.',
              meta: '📍 Rua Galvão Bueno — Liberdade · 💰 R$5-15'
            }
          ],
          tips: [
            { type: 'tip', text: 'Sunday is the best day for Liberdade — the Feira da Liberdade street fair runs along Rua Galvão Bueno with food stalls, crafts, and performances.' }
          ]
        },
        {
          label: 'Midday',
          activities: [],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Aska Lamen',
              description: 'Legendary ramen shop in Liberdade — queue up for rich tonkotsu ramen and gyoza. A paulistano institution.',
              meta: '📍 Rua Galvão Bueno, 466 — Liberdade · 💰 R$35-55/person'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Templo Busshinji',
              description: "The main Buddhist temple in São Paulo. A serene escape in the middle of the city, with beautiful Japanese-style architecture and peaceful gardens.",
              details: ['📍 Rua São Joaquim, 285 — Liberdade · Free entry']
            },
            {
              title: 'Casa Amarela — Casa do Saber',
              description: 'Explore the concept stores and creative spaces popping up in the Liberdade-Aclimação border area. Great for unique souvenirs.',
              details: ['📍 Wander Rua Conde de Sarzedas and surroundings']
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Samba Night',
              description: "Experience live samba — SP has an incredible live music scene. Bar Samba in Vila Madalena or Traço de União in Itaim have authentic roda de samba sessions.",
              details: ['🎵 Traço de União: Rua Clodomiro Amazonas, 1136 — Itaim Bibi', '💰 Cover ~R$30-50']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kinoshita',
              description: 'Japanese-Brazilian fusion at its finest. Chef Tsuyoshi Murakami creates stunning omakase combining São Paulo ingredients with Japanese technique.',
              meta: '📍 Rua Jacques Félix, 405 — Vila Nova Conceição · 💰 R$200-350/person'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: -23.5567, lng: -46.6326, label: 'Liberdade Gate', num: 1, cat: 'attraction', desc: "SP's Japanese quarter — torii gates and Asian markets" },
        { lat: -23.5584, lng: -46.6321, label: 'Museu da Imigração Japonesa', num: 2, cat: 'attraction', desc: 'Japanese immigration history in Brazil' },
        { lat: -23.5576, lng: -46.6335, label: 'Aska Lamen', num: 3, cat: 'food', desc: 'Legendary ramen in Liberdade' },
        { lat: -23.5589, lng: -46.6316, label: 'Templo Busshinji', num: 4, cat: 'attraction', desc: 'Serene Buddhist temple' },
        { lat: -23.5864, lng: -46.6710, label: 'Traço de União', num: 5, cat: 'nightlife', desc: 'Authentic samba roda sessions' },
        { lat: -23.5865, lng: -46.6668, label: 'Kinoshita', num: 6, cat: 'food', desc: 'Exquisite Japanese-Brazilian omakase' }
      ]
    },

    // DAY 7 — Day Trip or Chill Day + Farewell Dinner
    {
      num: 7,
      title: 'Final Day — Hidden Gems & Farewell',
      neighborhoods: 'Bom Retiro · Santa Cecília · Higienópolis',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Bom Retiro — Immigrant Quarter',
              description: "One of SP's most diverse neighborhoods — historically Jewish, now Korean, Bolivian, and more. Browse fabric shops, Korean BBQ spots, and street markets.",
              details: ['📍 Start at Metrô Tiradentes', '🛍️ Great for cheap clothing and textiles']
            },
            {
              title: 'Museu da Língua Portuguesa',
              description: 'Beautifully restored after a 2015 fire, this interactive museum celebrates the Portuguese language through immersive exhibits inside the gorgeous Estação da Luz building.',
              details: ['📍 Praça da Luz, 1 — Luz', '🕐 Tue-Sun 9am-5pm · 💰 R$20']
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Padaria Bella Paulista',
              description: 'Open 24/7 — a classic São Paulo institution. Perfect for a final leisurely breakfast with pão na chapa and fresh juices.',
              meta: '📍 Rua Haddock Lobo, 354 — Cerqueira César · 💰 R$20-30/person'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Higienópolis & FAAP',
              description: 'Stroll through this elegant, tree-lined neighborhood. Beautiful Art Deco and modernist architecture. Stop by Shopping Pátio Higienópolis for last-minute gifts.',
              details: ['📍 Rua Maranhão / Av. Angélica area']
            },
            {
              title: 'Edifício Copan — Ground Floor',
              description: "Return to Niemeyer's masterpiece to explore the ground-floor galleries, shops, and cafés. A fitting architectural farewell to São Paulo.",
              details: ['📍 Av. Ipiranga, 200 — República']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Lamen Kazu',
              description: 'Another top ramen spot — thick, rich broth and handmade noodles. Perfect casual lunch.',
              meta: '📍 Rua Thomaz Gonzaga, 62 — Liberdade · 💰 R$35-50/person'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Fasano',
              description: "São Paulo's most storied restaurant. Classic Italian-Brazilian cuisine in an impossibly elegant Art Deco dining room. The risotto and ossobuco are legendary. A perfect finale.",
              meta: '📍 Rua Vittorio Fasano, 88 — Jardins · 💰 R$250-400/person · ⚠️ Dress code: smart casual minimum'
            }
          ],
          tips: [
            { type: 'tip', text: 'End the trip at Baretto (the bar below Fasano) for a last cocktail — one of the best bars in South America.' }
          ]
        }
      ],
      mapPins: [
        { lat: -23.5282, lng: -46.6375, label: 'Bom Retiro', num: 1, cat: 'neighborhood', desc: 'Diverse immigrant quarter — Korean, Bolivian, Jewish' },
        { lat: -23.5348, lng: -46.6344, label: 'Museu da Língua Portuguesa', num: 2, cat: 'attraction', desc: 'Interactive museum of the Portuguese language' },
        { lat: -23.5499, lng: -46.6578, label: 'Higienópolis', num: 3, cat: 'neighborhood', desc: 'Elegant Art Deco and modernist architecture' },
        { lat: -23.5465, lng: -46.6502, label: 'Edifício Copan', num: 4, cat: 'attraction', desc: "Oscar Niemeyer's iconic residential building" },
        { lat: -23.5624, lng: -46.6685, label: 'Fasano', num: 5, cat: 'food', desc: "SP's most storied Italian-Brazilian restaurant" },
        { lat: -23.5627, lng: -46.6687, label: 'Baretto at Fasano', num: 6, cat: 'nightlife', desc: 'World-class cocktail bar' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (7 nights)', mid: 'R$4,200–6,300', notes: 'Mid-range hotel in Jardins/Pinheiros' },
    { category: 'Food & Dining', mid: 'R$3,500–7,000', notes: '~R$150-300/person/day × 3-4 people' },
    { category: 'Transport (Uber/Metro)', mid: 'R$700–1,200', notes: 'Metro + Uber for farther spots' },
    { category: 'Museums & Attractions', mid: 'R$400–700', notes: 'Several have free days' },
    { category: 'Nightlife & Entertainment', mid: 'R$500–1,000', notes: 'Covers, drinks, samba nights' },
    { category: 'Shopping & Souvenirs', mid: 'R$300–800', notes: 'Markets, antiques, gifts' },
    { category: 'TOTAL (group of 3-4)', mid: 'R$9,600–17,000', notes: '~$1,900–$3,400 USD at current rates' }
  ],

  practicalInfo: [
    {
      title: '🛬 Getting There',
      items: [
        'GRU Airport (Guarulhos) is the main international airport — 25-40km from city center',
        'Uber/99 from GRU to Jardins costs ~R$80-150 depending on traffic',
        'Airport Express bus (Airport Bus Service) runs to Paulista/Congonhas — R$60',
        'CGH (Congonhas) is the domestic airport, much closer to the center'
      ]
    },
    {
      title: '🚇 Getting Around',
      items: [
        'Metrô is clean, safe, and efficient — covers most tourist areas',
        'BILHETE ÚNICO card: load credit and tap — works on metro and buses',
        'Uber and 99 are cheap and widely available — always use these at night',
        'Avoid rush hour metro (7-9am, 5-7pm) — it gets extremely crowded'
      ]
    },
    {
      title: '🔒 Safety Tips',
      items: [
        "Don't flash phones or jewelry on the street — keep valuables in front pockets",
        'Stick to well-known neighborhoods (Jardins, Pinheiros, Vila Madalena, Itaim)',
        'Uber everywhere after dark — avoid walking alone at night in Centro',
        'Leave passport copies at hotel, carry a photocopy'
      ]
    },
    {
      title: '📱 Connectivity',
      items: [
        'Buy a local SIM at the airport (Claro or Vivo) — ~R$50 for 10GB',
        'Most restaurants and cafés have good Wi-Fi',
        'Download offline maps of SP in Google Maps before arriving',
        'WhatsApp is the primary communication app in Brazil — everyone uses it'
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Itinerary deployed!');
console.log('URL:', result.url);
console.log('Slug:', result.slug);
console.log('Email sent:', result.emailSent);
