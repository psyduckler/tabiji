const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772665927229_9antum',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Rio de Janeiro, State of Rio de Janeiro, Brazil',
  startDate: '2026-03-25',
  endDate: '2026-03-28',
  groupSize: 1,
  travelStyle: 'Adventure, Foodie',
  dining: '',
  budget: '',
  requests: ''
};

const itineraryData = {
  destination: 'Rio de Janeiro, Brazil',
  countryEmoji: '🇧🇷',
  title: 'A Wild & Flavorful Solo Adventure in Rio',
  subtitle: '4 days of hang gliding, iconic landmarks, samba nights & serious eating',
  description: "Rio de Janeiro is where the mountains meet the sea and every meal is a celebration. This solo itinerary packs in the city's greatest adventures — soaring over Ipanema on a hang glider, hiking the world's largest urban forest, ascending Christ the Redeemer at sunrise, and watching the sun melt into the ocean from Sugarloaf. At night, the botecos, samba bars, and street food stalls around Lapa's colonial arches call. Four days of pure Carioca magic.",
  duration: '4 days',
  dates: 'Mar 25 – Mar 28, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Solo Adventure & Foodie',
  highlights: [
    'Hang gliding over Ipanema Beach from Pedra Bonita',
    'Sunrise at Christ the Redeemer before the crowds',
    'Sugarloaf Mountain sunset with caipirinha in hand',
    'Samba and street food in Lapa under the colonial arches',
    'Hiking Tijuca National Forest — the world\'s largest urban rainforest'
  ],

  essentials: [
    { title: '🌡️ March Weather', text: 'March is late summer in Rio — expect warm temperatures around 28–32°C with afternoon rain showers. The city is post-Carnival and buzzing. Pack light, breathable clothing, a rain jacket, and SPF 50+.' },
    { title: '🚕 Getting Around', text: 'Uber is safe, reliable, and cheap — use it exclusively over taxis. The Metro covers Copacabana, Ipanema, and central Rio. For Santa Teresa, catch a vintage tram (bonde) from downtown.' },
    { title: '🔒 Safety Tips', text: 'Rio is vibrant but requires street smarts. Leave valuables at your hotel, use Uber over street taxis, avoid empty streets at night, and never display phones or cameras conspicuously. Stick to tourist-friendly zones.' },
    { title: '💰 Cash & Payments', text: 'Carry some Brazilian reais (BRL) for street food, markets, and smaller botecos. Cards are widely accepted in restaurants and shops. ATMs at large banks (Bradesco, Itaú) are the safest option.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-25',
      neighborhoods: 'Copacabana · Ipanema · Santa Teresa',
      title: 'Beach Vibes, Mosaic Steps & Hilltop Bohemia',
      description: "Hit the ground running with Rio's most iconic neighborhoods. Walk the crescent of Copacabana, feel the pulse of Ipanema, climb the dazzling Selarón Steps, and end the day in Santa Teresa — the city's bohemian arts quarter perched in the hills, with dinner and views to match.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Copacabana Beach Morning Walk',
              description: "Start your first morning with the quintessential Carioca experience — a walk along the legendary Copacabana beachfront. The black-and-white mosaic promenade stretches 4km, framed by mountains. Watch early-morning volleyball, surfers, and beach vendors setting up.",
              details: [
                '🏖️ The beachfront promenade (calçadão) is one of the world\'s most recognizable boardwalks',
                '🏐 Beach volleyball and futevolei (foot-volleyball) happen all morning at the sand courts',
                '☕ Stop at a beach kiosk for a fresh coconut water (R$5–8) — the Carioca way to start the day'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Padaria Boulangerie',
              description: 'Classic Brazilian padaria (bakery) on Copacabana — grab a pão de queijo (cheese bread), coxinha, and strong espresso. The Brazilian breakfast staples.',
              meta: '💰 $ · 📍 Copacabana · Open from 7am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ipanema Beach & The Famous Posto 9',
              description: "Walk from Copacabana over to Ipanema — Rio's more stylish, tree-lined beach neighborhood. Posto 9 (Lifeguard Post 9) near Rua Vinícius de Moraes is where the cool crowd gathers. Swim in the clear green water, or just sit and absorb the Carioca lifestyle.",
              details: [
                '🌊 Ipanema has strong shore break — swim parallel to shore if currents feel strong',
                '🛍️ Ipanema\'s side streets have great boutiques, açaí shops, and local designers',
                '🎵 This is literally the beach that inspired "The Girl from Ipanema"'
              ]
            },
            {
              title: 'Escadaria Selarón (Selarón Steps)',
              description: "From Ipanema, head to Santa Teresa and discover the Selarón Steps — 215 steps covered in 2,000 tiles from 60+ countries, the obsessive life\'s work of Chilean artist Jorge Selarón. An explosion of color and one of Rio\'s most photographed spots.",
              details: [
                '🎨 The tiles include scenes of Rio life, Brazilian flags, and abstract patterns',
                '📸 Go mid-afternoon when the light hits the tiles perfectly',
                '📍 Located between Lapa and Santa Teresa at Rua Joaquim Silva'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Garota de Ipanema',
              description: 'The legendary boteco where the Girl from Ipanema was first composed. Classic Brazilian lunch — try the grilled fish (peixe grelhado) or moqueca (seafood stew). Cold chopp (draft beer) is mandatory.',
              meta: '💰 $$ · 📍 Rua Vinícius de Moraes 49, Ipanema'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Santa Teresa Neighborhood Wander',
              description: "Take the historic bonde (tram) or a short Uber up to Santa Teresa — Rio\'s hillside bohemian quarter, packed with artists\' studios, quirky bars, and sweeping city views. Wander Rua Almirante Alexandrino, peek into art galleries, and soak in the vibe.",
              details: [
                '🚃 The bonde tram runs from downtown (Carioca metro station) — R$25, vintage and fun',
                '🎨 The neighborhood hosts galleries, studios, and artisan shops',
                '🌆 Belvedere do Morro dos Prazeres offers sweeping views of the city below'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Aprazível',
              description: "Rio\'s most celebrated hilltop restaurant, set in a lush tropical garden in Santa Teresa. Chef Ana Castilho\'s Brazilian cuisine showcases regional ingredients — try the carne seca (sun-dried beef) with pirão, or the catch of the day. The views over the city are extraordinary.",
              meta: '💰 $$$ · 📍 Rua Aprazível 62, Santa Teresa · Reserve ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, Santa Teresa\'s boteco bars come alive. Bar do Mineiro on Rua Paschoal Carlos Magno is a beloved local institution — cold beer, petiscos, and great people-watching.' }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9711, lng: -43.1822, label: 'Copacabana Beach', num: 1, cat: 'attraction', desc: 'Iconic 4km crescent beach with the famous mosaic promenade' },
        { lat: -22.9838, lng: -43.2096, label: 'Ipanema Beach (Posto 9)', num: 2, cat: 'attraction', desc: "Rio's coolest beach stretch — the Girl from Ipanema's hometown" },
        { lat: -22.9868, lng: -43.2039, label: 'Garota de Ipanema', num: 3, cat: 'food', desc: 'Legendary boteco where The Girl from Ipanema was composed' },
        { lat: -22.9146, lng: -43.1787, label: 'Selarón Steps', num: 4, cat: 'attraction', desc: '215 steps covered in 2,000 hand-painted tiles from 60 countries' },
        { lat: -22.9190, lng: -43.1793, label: 'Santa Teresa', num: 5, cat: 'attraction', desc: "Bohemian hilltop neighborhood with art galleries and city views" },
        { lat: -22.9208, lng: -43.1817, label: 'Aprazível Restaurant', num: 6, cat: 'food', desc: 'Hilltop garden restaurant with stunning views and refined Brazilian cuisine' }
      ]
    },
    {
      num: 2,
      date: '2026-03-26',
      neighborhoods: 'Pedra Bonita · Tijuca Forest · Leblon',
      title: 'Hang Gliding, Jungle Hiking & Açaí',
      description: "Pure adventure day. Launch off a mountain on a tandem hang glider and soar over Ipanema Beach, then hike deep into the Tijuca — the world's largest urban rainforest, a green lung in the heart of Rio. Reward yourself with the city's best açaí in Leblon and a memorable seafood dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tandem Hang Gliding from Pedra Bonita',
              description: "One of the most thrilling experiences in South America. You launch off Pedra Bonita (a 510m granite peak) strapped to an experienced pilot and glide silently over Rio, watching Ipanema and Leblon beaches grow larger below. The landing is right on São Conrado beach. Pure adrenaline.",
              details: [
                '🪂 Depart early (8–9am) for best thermals and lighter winds',
                '✈️ Flight lasts 10–20 minutes — an unforgettable perspective on Rio',
                '📸 Your pilot will wear a GoPro and give you footage — ask in advance',
                '💰 Around R$600–800 (approx $100–130 USD) for a tandem flight',
                '🔗 Book with Just Fly (Superfly) or Delta Fly Rio — the two most reputable operators'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Café near São Conrado',
              description: 'After landing on São Conrado beach, grab a quick açaí bowl and coffee from a nearby kiosk to fuel up before the forest hike.',
              meta: '💰 $ · 📍 São Conrado beachfront kiosks'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tijuca National Forest Hike',
              description: "Tijuca is astonishing — a 32km² Atlantic rainforest that was almost entirely replanted in the 1800s after coffee farms stripped the hillsides. Today it hides waterfalls, rare orchids, toucans, and monkeys. The hike to Pico da Tijuca (1,021m, Rio\'s highest peak) rewards with views over the entire city.",
              details: [
                '🌿 Trail options: Pico da Tijuca (4–5 hours, challenging) or Cascatinha Waterfall (1 hour, easy)',
                '🐒 Watch for golden-headed lion tamarins — tiny monkeys native to this forest',
                '🌊 Cascatinha Taunay waterfall is a beautiful, manageable detour',
                '🥤 Bring 2L of water — the forest is humid and the trails can be steep',
                '🦟 Wear long pants and insect repellent — the understory has biting insects'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Os Esquilos Restaurant',
              description: 'Charming rustic restaurant inside Tijuca Forest, near the Cascatinha waterfall. Open since 1945 — try the Brazilian bacalhau (salted cod) or picanha (top sirloin). An institution beloved by cariocas.',
              meta: '💰 $$ · 📍 Inside Tijuca Forest, near Cascatinha · Lunch only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Leblon Beachfront & Açaí Culture',
              description: "Head to Leblon — Rio\'s most upscale neighborhood and the quieter, more residential cousin of Ipanema. Leblon beach is less crowded and beautiful at golden hour. Stop at one of the famous açaí kiosks for a thick, frozen açaí bowl topped with granola and banana. It\'s Rio\'s obsession.",
              details: [
                '🫐 Açaí in Rio is thick and unsweetened — NOT the watery purple juice you get elsewhere',
                '🏖️ Leblon beach (Posto 12) is calmer and preferred by locals with kids and dogs',
                '🌅 The view from Leblon toward the Two Brothers mountain is stunning at sunset'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Zuka Restaurant',
              description: "Leblon's beloved wood-fire kitchen by chef Ludmila Soeiro. Acclaimed for grilled fish, the signature duck confit, and beautiful desserts. Warm, elegant atmosphere — a perfect solo dinner at the bar counter.",
              meta: '💰 $$$ · 📍 Rua Dias Ferreira 233, Leblon · Reserve ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, Rua Dias Ferreira in Leblon is lined with excellent bars and dessert spots. Jobi bar (open since 1956) is legendary for its chopp (draft beer) and petiscos.' }
          ]
        }
      ],
      mapPins: [
        { lat: -23.0002, lng: -43.2880, label: 'Pedra Bonita (Launch Site)', num: 1, cat: 'attraction', desc: 'Granite peak — takeoff point for hang gliding over Rio' },
        { lat: -23.0104, lng: -43.3031, label: 'São Conrado Beach (Landing)', num: 2, cat: 'attraction', desc: 'Hang gliding landing strip on São Conrado beach' },
        { lat: -22.9351, lng: -43.2814, label: 'Tijuca Forest / Cascatinha', num: 3, cat: 'attraction', desc: "World's largest urban rainforest — waterfalls, monkeys, rare birds" },
        { lat: -22.9423, lng: -43.2795, label: 'Os Esquilos Restaurant', num: 4, cat: 'food', desc: 'Classic Brazilian lunch spot inside Tijuca Forest' },
        { lat: -22.9875, lng: -43.2269, label: 'Leblon Beach (Posto 12)', num: 5, cat: 'attraction', desc: "Rio's most upscale beach neighborhood — quieter and beautiful" },
        { lat: -22.9862, lng: -43.2269, label: 'Zuka Restaurant', num: 6, cat: 'food', desc: 'Wood-fire kitchen in Leblon — acclaimed fish and duck' }
      ]
    },
    {
      num: 3,
      date: '2026-03-27',
      neighborhoods: 'Corcovado · Centro · Lapa',
      title: 'Christ the Redeemer, Sugarloaf & Samba in Lapa',
      description: "The big icons day — but done right, early and without the crowds. Sunrise at Christ the Redeemer before the tour buses arrive, colonial Rio in Centro, and then the climax: watching the sun dissolve into the Atlantic from the summit of Sugarloaf Mountain. The night belongs to Lapa — Rio's wild, beautiful, samba-soaked entertainment district.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Christ the Redeemer at Sunrise',
              description: "Cristo Redentor is one of the world's great landmarks — a 38m Art Deco statue of Jesus perched 710m above Rio, arms open to the city. The secret is timing: book the 8am shuttle from Cosme Velho to beat the tour groups. The view from the platform extends from the ocean to the mountains, with the city spread below like a map.",
              details: [
                '⏰ Book the earliest train/van (departs ~8am from Cosme Velho station)',
                '🌅 Morning light gives the statue a warm golden glow — best photography',
                '🎫 Buy tickets online in advance at cristoredentor.com.br (R$90 incl. train)',
                '☁️ Check the forecast — clouds can obscure the view. Clear mornings are magic',
                '📍 Cosme Velho station is the departure point for the rack railway (trem do Corcovado)'
              ]
            }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Centro Histórico Walk — Confeitaria Colombo & Arcos da Lapa',
              description: "Descend to Rio\'s Centro and step into the city\'s Belle Époque past. Confeitaria Colombo (1894) is a jaw-dropping cafe with floor-to-ceiling mirrors, stained glass, and marble — one of Brazil\'s most beautiful interiors. Then walk to the Arcos da Lapa (18th-century aqueduct) that dominates Lapa\'s skyline.",
              details: [
                '☕ Confeitaria Colombo: try the bolo Colombo (cream cake) or quindim (coconut custard)',
                '📸 The interior mirrors and balconies at Colombo are extraordinary — go before lunch rush',
                '🏛️ The Arcos da Lapa aqueduct now carries the Santa Teresa tram over it',
                '📍 Centro is also home to the Museu Histórico Nacional and Praça XV'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast / Morning Coffee',
              name: 'Confeitaria Colombo',
              description: "Rio\'s most beautiful café, open since 1894. Belle Époque interior with mirrored walls, stained glass, and ornate azulejo tiles. Order the café com leite and a selection of traditional Brazilian sweets.",
              meta: '💰 $$ · 📍 Rua Gonçalves Dias 32, Centro'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sugarloaf Mountain (Pão de Açúcar) at Sunset',
              description: "The two-stage cable car ascent of Sugarloaf (396m) is Rio\'s other iconic vantage point. But unlike Corcovado, this is best at sunset — timed right, you\'ll watch the sun sink into the Atlantic behind the Two Brothers peaks while the city below begins to twinkle. Get the last cable car up (~sunset) for the full effect.",
              details: [
                '🚡 Two cable car stages: Praia Vermelha → Morro da Urca → Pão de Açúcar summit',
                '🌅 Check sunset time (~6:15pm in March) and aim to be on top 30 mins before',
                '🎫 Buy tickets at bondinho.com.br (R$120 roundtrip)',
                '🦅 You can also rock climb the peak with a guide for a different perspective',
                '🍹 There\'s a bar and restaurant on the Urca level — ideal for a caipirinha with the view'
              ]
            }
          ],
          meals: [
            {
              type: '🥩 Lunch',
              name: 'Churrascaria Palace',
              description: 'The best rodízio churrasco experience in Rio. A parade of cuts — picanha, fraldinha, costela, garlic beef — brought to your table by gaucho-style servers. The salad bar is legendary. A true Brazilian feast.',
              meta: '💰 $$$ · 📍 Rua Rodolfo Dantas 16, Copacabana · Worth every real'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lapa Nightlife — Street Food & Live Samba',
              description: "After dark, Lapa transforms into Rio\'s electric entertainment district. The streets around the colonial Arcos da Lapa fill with vendors selling espetinhos (grilled skewers), tapioca crepes, and pastéis. Dozens of samba clubs come alive — Rio Scenarium (three floors, live samba, antique decor) and Lapa 40 Graus are the best. Expect samba dancing, cold Brahma beer, and pure Carioca chaos.",
              details: [
                '🎶 Rio Scenarium: arrives from 10pm, live samba. Book a table on the website',
                '🥩 Espetinhos (R$5–10 each) from street vendors are the authentic Lapa experience',
                '🍺 Brahma chopp (draft beer, R$8–12) flows freely from street kiosks',
                '⏰ Lapa gets going late — don\'t arrive before 10pm. Stays hot until 3-4am',
                '🚕 Uber back to Ipanema/Copacabana — R$25–35, very easy'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bar do Mineiro',
              description: 'An authentic Santa Teresa/Lapa institution with no-frills carioca cooking — feijão tropeiro (pork & bean stew), pork ribs, farofa, and cold Antarctica beer. Beloved by locals and in the neighborhood since forever.',
              meta: '💰 $ · 📍 Rua Paschoal Carlos Magno 99, Santa Teresa'
            }
          ],
          tips: [
            { type: 'tip', text: 'Lapa on a Friday night is one of South America\'s great street parties. Leave your phone well-secured and carry only cash you\'re comfortable losing — the energy is electric but pickpockets work the crowd.' }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9519, lng: -43.2105, label: 'Christ the Redeemer', num: 1, cat: 'attraction', desc: 'Iconic 38m Art Deco statue at 710m — panoramic views over all of Rio' },
        { lat: -22.9098, lng: -43.1729, label: 'Confeitaria Colombo', num: 2, cat: 'food', desc: "Rio's most beautiful café — Belle Époque mirrors, tiles, and Brazilian sweets" },
        { lat: -22.9140, lng: -43.1795, label: 'Arcos da Lapa', num: 3, cat: 'attraction', desc: '18th-century aqueduct arches — iconic symbol of Lapa' },
        { lat: -22.9486, lng: -43.1726, label: 'Churrascaria Palace', num: 4, cat: 'food', desc: 'Classic rodízio churrascaria — the full Brazilian meat feast' },
        { lat: -22.9494, lng: -43.1645, label: 'Sugarloaf Mountain', num: 5, cat: 'attraction', desc: '396m granite peak — cable car to the summit, sunset views' },
        { lat: -22.9143, lng: -43.1795, label: 'Rio Scenarium / Lapa Samba', num: 6, cat: 'attraction', desc: 'Three-floor samba club in a stunning antique warehouse — Rio\'s best nightlife' },
        { lat: -22.9208, lng: -43.1817, label: 'Bar do Mineiro', num: 7, cat: 'food', desc: 'Beloved carioca boteco in Santa Teresa — feijoada and cold beer' }
      ]
    },
    {
      num: 4,
      date: '2026-03-28',
      neighborhoods: 'Jardim Botânico · Lagoa · Ipanema',
      title: 'Botanical Garden, Lagoon & A Proper Farewell',
      description: "End Rio the carioca way — slow mornings, beautiful spaces, and a long goodbye. The Jardim Botânico is one of the world\'s great botanical gardens, especially alive in the morning humidity. Walk or bike the Lagoa Rodrigo de Freitas, grab the city\'s best pastéis at the hippy fair, and close the trip with a caipirinha as the sun sets over Ipanema.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Jardim Botânico (Rio Botanical Garden)',
              description: "One of the world\'s great botanical gardens — 137 hectares of Atlantic rainforest, with a famous imperial palm avenue that dates to 1809. Morning is magical: the humidity makes the orchid houses steam, toucans hop through the canopy, and you\'ll often have whole sections to yourself. The 750+ species of trees include Victoria amazonica water lilies.",
              details: [
                '🌺 The Imperial Palm Avenue was planted by Dom João VI in 1809',
                '🦜 Spot toucans, parrots, and marmosets in the canopy',
                '🌸 Orchid greenhouse has over 5,000 orchid specimens',
                '⏰ Opens at 8am — mornings are quieter and cooler',
                '💰 Entry R$30 (adults) · 📍 Rua Jardim Botânico 1008'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Couve-Flor Café (inside Jardim Botânico)',
              description: 'A charming café inside the botanical garden. Tropical fruit salads, granola, tapioca, and good coffee — the perfect fuel before you explore.',
              meta: '💰 $ · 📍 Inside Jardim Botânico'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lagoa Rodrigo de Freitas & Hippy Fair',
              description: "The Lagoa is Rio\'s beautiful urban lagoon, ringed by mountains and favelas. Rent a bike or pedalinho (paddleboat) and circle the lake while Christ the Redeemer watches from the Corcovado ridge. On Saturday (today!), the Ipanema Hippy Fair (Feira Hippie da Praça General Osório) is in full swing — 500+ vendors of art, jewelry, crafts, and food.",
              details: [
                '🚲 Bike rentals along the lagoon perimeter (R$15–20/hour)',
                '🛶 Pedalinho paddleboats are fun for solo riders too',
                '🛍️ Hippy Fair at Praça General Osório, Ipanema — Saturdays 9am–6pm',
                '🧃 Try a fresh sugarcane juice (garapa) from a vendor at the lagoon — R$5'
              ]
            },
            {
              title: 'Favela Vidigal Hike to Dois Irmãos Summit',
              description: "For one final adventure, hike through the Vidigal favela community to the summit of Dois Irmãos (Two Brothers) — two granite peaks that form Rio\'s most recognizable skyline feature. From the top, you get arguably the best panoramic view in all of Rio: Ipanema, Leblon, Lagoa, and the Atlantic all at once.",
              details: [
                '🥾 The hike is about 45 minutes up through the favela — moderate difficulty',
                '📸 Views from the top stretch over Ipanema, Leblon, and the entire Southern Zone',
                '👥 Locals and tourists both make this hike regularly — it\'s well-traveled',
                '💡 Go in the afternoon for the best light on Ipanema beach below'
              ]
            }
          ],
          meals: [
            {
              type: '🥘 Lunch',
              name: 'Gula Gula',
              description: 'Ipanema classic known for its enormous, creative salads and sandwiches. Great for a light, delicious lunch before the afternoon hike. A Rio institution since the 1980s.',
              meta: '💰 $$ · 📍 Rua Aníbal de Mendonça 132, Ipanema'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ipanema Sunset & Final Caipirinha',
              description: "Ipanema beach at sunset is a Rio ritual. Locals gather at Arpoador — the rocky promontory between Copacabana and Ipanema — and collectively watch the sun dip behind Dois Irmãos. When it disappears, the crowd spontaneously applauds. It\'s one of travel\'s small, unforgettable moments. Then it\'s time for a caipirinha at a beachfront bar.",
              details: [
                '🌅 Pedra do Arpoador is the classic sunset-watching spot — arrive 20 mins early',
                '👏 Wait for it: the crowd applause when the sun disappears behind the mountains',
                '🍹 Post-sunset caipirinhas at Barraca do Uruguay beach bar (Posto 8/9)',
                '📸 Golden hour light on Dois Irmãos is extraordinary'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Oro Restaurant',
              description: "Chef Felipe Bronze\'s Leblon restaurant — one of Rio\'s most celebrated. The tasting menu blends Brazilian biodiversity (Amazonian herbs, cerrado fruits, Atlantic seafood) with technique. A proper farewell to Rio's extraordinary flavors.",
              meta: '💰 $$$$ · 📍 Rua General San Martín 889, Leblon · Reserve well ahead'
            }
          ],
          tips: [
            { type: 'tip', text: "Can't get into Oro? Roberta Sudbrack (contemporary Brazilian) and CT Boucherie (creative churrasco by Claude Troisgros) are both excellent alternatives in the same neighborhood." }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9669, lng: -43.2229, label: 'Jardim Botânico', num: 1, cat: 'attraction', desc: '137-hectare botanical garden with imperial palms and toucans' },
        { lat: -22.9734, lng: -43.2109, label: 'Lagoa Rodrigo de Freitas', num: 2, cat: 'attraction', desc: 'Beautiful urban lagoon ringed by mountains — bike or pedal-boat' },
        { lat: -22.9870, lng: -43.1980, label: 'Feira Hippie (Praça Osório)', num: 3, cat: 'attraction', desc: 'Saturday artisan market — crafts, jewelry, street food' },
        { lat: -22.9840, lng: -43.2207, label: 'Dois Irmãos / Vidigal', num: 4, cat: 'attraction', desc: 'Hike through Vidigal favela to the summit — best panoramic view in Rio' },
        { lat: -22.9874, lng: -43.2020, label: 'Gula Gula', num: 5, cat: 'food', desc: 'Classic Ipanema lunch spot — creative salads and sandwiches' },
        { lat: -22.9886, lng: -43.1952, label: 'Arpoador (Sunset Spot)', num: 6, cat: 'attraction', desc: 'Rocky promontory — sunset crowd applauds as sun sets behind Dois Irmãos' },
        { lat: -22.9882, lng: -43.2260, label: 'Oro Restaurant', num: 7, cat: 'food', desc: "Chef Felipe Bronze's celebrated restaurant — Brazilian fine dining farewell" }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: 'R$200–350/night', midrange: 'R$400–700/night', luxury: 'R$800–2,000/night' },
    { category: 'Meals (per person)', budget: 'R$60–100/day', midrange: 'R$150–280/day', luxury: 'R$350–600/day' },
    { category: 'Transport (Uber)', budget: 'R$30–60/day', midrange: 'R$60–120/day', luxury: 'R$150–300/day' },
    { category: 'Activities', budget: 'R$50–150/day', midrange: 'R$200–400/day', luxury: 'R$500–1,000/day' },
    { category: 'Hang Gliding', budget: 'R$600–800', midrange: 'R$600–800', luxury: 'R$600–800' },
    { category: '4-Day Total (solo)', budget: 'R$2,500–4,000', midrange: 'R$5,000–8,000', luxury: 'R$10,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Rio has two airports: Galeão International (GIG) for long-haul flights, and Santos Dumont (SDU) for domestic', 'GIG to Ipanema by Uber: ~45 mins, R$80–120', 'BRT express bus from GIG: R$22, takes 1.5 hours (budget option)'] },
    { title: '🏨 Where to Stay', items: ['Ipanema: best location for beaches, restaurants, and nightlife access', 'Copacabana: more affordable, great beach, lively — ideal for solo travelers', 'Santa Teresa: boutique guesthouses, bohemian vibe, hillside views', 'Leblon: quietest, most upscale, excellent restaurant scene'] },
    { title: '🌡️ Weather in March', items: ['Late summer: average 28–32°C (82–90°F)', 'Afternoon rain showers are common — pass quickly, usually 30–60 mins', 'Humidity is high — light, breathable clothing is essential', 'UV index very high — SPF 50+, hat, and sunglasses mandatory'] },
    { title: '💳 Money', items: ['Currency: Brazilian Real (BRL). $1 USD ≈ R$5–6', 'Cards accepted everywhere modern — carry cash for street food and markets', 'ATMs at Bradesco and Itaú banks are safest', 'Tipping: 10% service charge usually added to restaurant bills'] },
    { title: '🔒 Safety', items: ['Use Uber exclusively — avoid street taxis', 'Don\'t display phone, camera, or jewelry in the street', 'Stick to established tourist areas, especially at night', 'Keep hotel cards in your shoe or money belt when out at night', 'Ipanema, Leblon, and Santa Teresa are generally safe for tourists'] }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
