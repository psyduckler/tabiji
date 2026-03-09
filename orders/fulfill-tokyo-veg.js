const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773089221948_71sylf',
  orderId: 'order_1773089221948_71sylf',
  email: 'speak@kaeko.us',
  destination: 'Tokyo, Japan',
  startDate: '2026-04-27',
  start_date: '2026-04-27',
  endDate: '2026-05-02',
  end_date: '2026-05-02',
  groupSize: '2',
  travelStyle: 'Adventure, Cultural, Foodie, Relaxation',
  dining: 'Mix of everything (VEGETARIAN)',
  budget: 'Under $1,000',
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '\u{1F1EF}\u{1F1F5}',
  title: 'Tokyo & Beyond',
  subtitle: 'Wisteria, Fuji Views & Vegetarian Feasts During Golden Week',
  description: 'A 5-day adventure for two vegetarian travelers arriving from Europe \u2014 gentle jetlag recovery, iconic Tokyo culture, a day trip to the Great Buddha in Kamakura, overnight near Mt Fuji with private onsen, and the legendary Ashikaga Flower Park at peak wisteria season. All during Golden Week, with budget-smart tips throughout.',
  duration: '5 Days \u00b7 April 27 \u2013 May 2, 2026',
  dates: 'April 27 \u2013 May 2, 2026',
  budget: 'Under $1,000 for two',
  pace: 'Gentle to moderate (jetlag-adjusted)',
  bestFor: 'Vegetarian foodies, nature lovers, culture & architecture enthusiasts',
  highlights: [
    'teamLab Borderless at Azabudai Hills',
    'Ashikaga Flower Park at peak wisteria',
    'Kamakura Great Buddha & coastal trails',
    'Private onsen near Mt Fuji',
    'Shinjuku Gyoen gardens',
    'Ghibli Museum in Mitaka',
    'Meiji Shrine & Harajuku',
    '100% vegetarian dining guide'
  ],

  essentials: [
    {
      title: '\u26a0\ufe0f Golden Week Alert',
      text: "Your trip overlaps with Golden Week (Apr 29\u2013May 5) \u2014 Japan's biggest holiday period. Expect larger crowds at popular attractions, packed trains, and higher accommodation prices. Book teamLab Borderless, Ghibli Museum, and onsen/ryokan NOW. The upside? Festive atmosphere, special events, and wisteria at peak bloom."
    },
    {
      title: '\ud83e\udd66 Vegetarian Survival Guide',
      text: 'Japan can be tricky for vegetarians \u2014 dashi (fish stock) hides in many dishes. Your secret weapons: say "watashi wa bejitarian desu" (I am vegetarian) and "niku, sakana, dashi nashi de onegaishimasu" (no meat, fish, or dashi please). Konbini (convenience stores) are lifesavers: umeboshi/kombu onigiri, inari sushi, edamame, and salads are always veggie-safe. We have curated 100% vegetarian-verified restaurants for every meal.'
    },
    {
      title: '\ud83d\ude83 Getting Around',
      text: 'Get a 72-hour Tokyo Metro pass (\u00a51,500/person) for Days 1-3. For day trips (Kamakura, Ashikaga, Kawaguchiko), buy individual tickets or use a Suica/Pasmo IC card loaded with \u00a55,000 each. Haneda to central Tokyo is ~30 min via Keikyu Line or Tokyo Monorail (\u00a5500).'
    },
    {
      title: '\ud83d\udcb4 Budget Tips',
      text: 'Under \u00a570,000 per person for 5 days is tight during Golden Week but doable. Stay in hostels or budget hotels (\u00a55,000-8,000/night). Eat at konbini for breakfast (\u00a5300-500), casual lunch (\u00a5800-1,200), and splurge on one nice dinner daily (\u00a52,000-3,000). Use free attractions: Meiji Shrine, Imperial Palace gardens, Yoyogi Park, temple grounds. Your biggest expenses will be the Kawaguchiko overnight and day trip trains.'
    },
    {
      title: '\ud83d\udcf1 Stay Connected',
      text: 'Grab a prepaid eSIM before you fly (Ubigi, Airalo, or Sakura Mobile \u2014 \u00a52,000-3,000 for 5 days unlimited data). Free Wi-Fi exists at stations and konbini but is unreliable. Google Maps works perfectly for train navigation \u2014 set it to transit mode.'
    },
    {
      title: '\u2708\ufe0f Airport Logistics',
      text: "Arrive Haneda Mon Apr 27 at 13:55. Immigration + baggage takes ~45-60 min (Golden Week = busier). You'll be at your hotel by ~16:00. Departure May 2 at 19:40 \u2014 leave your hotel by 16:30, aim to be at Haneda by 17:30 for international check-in."
    }
  ],

  days: [
    // === DAY 1: Mon Apr 27 \u2014 Arrival & Gentle Shinjuku ===
    {
      num: 1,
      neighborhoods: 'Shinjuku \u00b7 Shinjuku Gyoen',
      title: 'Gentle Landing & Garden Therapy',
      description: "You land at 13:55 \u2014 by the time you clear customs and reach your hotel, it'll be late afternoon. Today is all about gentle acclimatization: check in, stretch your legs with a stroll through one of Tokyo's most beautiful gardens, and end with a comforting vegetarian dinner. No rushing, no pressure.",
      timeBlocks: [
        {
          label: '\ud83d\udecf Afternoon \u2014 Arrival',
          activities: [
            {
              title: 'Haneda Airport \u2192 Shinjuku',
              description: 'Take the Keikyu Line to Shinagawa, then JR Yamanote Line to Shinjuku (total ~50 min, \u00a5600). Alternatively, the Limousine Bus goes direct to Shinjuku (\u00a51,400, 50-75 min but no transfers with luggage).',
              details: [
                '\ud83d\udcb0 Keikyu + JR: ~\u00a5600/person | Bus: \u00a51,400/person',
                '\ud83e\uddf3 Pick up a Suica/Pasmo card at the airport station (\u00a5500 deposit + load \u00a53,000-5,000)',
                '\ud83d\udca1 Tip: If exhausted, grab an ekiben (station bento) at Haneda \u2014 look for inari sushi or vegetable tempura boxes'
              ]
            },
            {
              title: 'Check In & Freshen Up',
              description: 'Drop your bags at your accommodation in the Shinjuku area. Budget options: Imano Tokyo Hostel Shinjuku (\u00a54,000-6,000/night, private rooms available), Unplan Shinjuku (stylish capsule/private), or Citadines Shinjuku (apartment-style, kitchen for self-catering).',
              details: [
                '\ud83c\udfe8 Budget: \u00a55,000-8,000/night for two',
                '\ud83d\udca1 Having a kitchen or fridge helps with vegetarian meal prep and konbini snacks'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "\ud83d\udd50 Don't fight the jetlag too hard \u2014 just stay awake until 20:00-21:00 and you'll reset faster. Walk slowly, drink water, and avoid napping." }
          ]
        },
        {
          label: '\ud83c\udf3f Late Afternoon \u2014 Shinjuku Gyoen',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "A 10-minute walk from Shinjuku Station, this 144-acre garden is the perfect jetlag antidote. Wander through the Japanese landscape garden (zen ponds and bridges), the English landscape garden (wide lawns), and the French formal garden (rose beds). In late April, the last cherry blossoms may still be lingering and wisteria begins blooming in the pergolas.",
              details: [
                '\ud83d\udcb0 \u00a5500/person entry',
                '\u23f0 Open until 18:00 (last entry 17:30) \u2014 plenty of time even arriving at 16:00',
                '\ud83d\udcf7 The Taiwan Pavilion and greenhouse are hidden gems most tourists skip',
                '\ud83d\udeab No alcohol allowed (unusual for Japan parks!) \u2014 peaceful atmosphere guaranteed'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f DINNER',
              name: 'Ain Soph. Journey \u2014 Shinjuku',
              description: "Tokyo's most beloved vegan restaurant chain. The fluffy vegan pancakes are Instagram-famous, but dinner is the real star: try the Heavenly Vegan Burger or the seasonal set meal with tofu steak. Everything is clearly labeled, staff speaks English, and the cozy interior feels like a warm hug after a long flight.",
              meta: '\ud83d\udccd Shinjuku 3-chome, 5 min walk from station \u00b7 \ud83d\udcb0 \u00a51,500-2,500/person \u00b7 \u23f0 11:30-22:00'
            }
          ],
          tips: [
            { type: 'reddit', text: "Ain Soph Journey is genuinely one of the best vegan spots in Tokyo \u2014 the burger and pancakes are not to be missed. Even my non-vegan Japanese friends love it.", cite: 'r/JapanTravel' },
            { type: 'tip', text: "\ud83c\udf19 After dinner, take a slow walk through Shinjuku's neon streets for your first taste of Tokyo's electric energy \u2014 Kabukicho's Godzilla Head is just minutes away." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6921, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Main transit hub \u2014 arrival point from Haneda' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 2, cat: 'attraction', desc: '144-acre garden \u2014 jetlag recovery in nature' },
        { lat: 35.6931, lng: 139.7028, label: 'Ain Soph. Journey', num: 3, cat: 'food', desc: 'Top-rated vegan restaurant \u2014 heavenly burger & pancakes' },
        { lat: 35.6945, lng: 139.7036, label: 'Kabukicho Godzilla Head', num: 4, cat: 'attraction', desc: "Iconic Godzilla towering over Shinjuku's neon streets" }
      ]
    },

    // === DAY 2: Tue Apr 28 \u2014 Central Tokyo Culture Day ===
    {
      num: 2,
      neighborhoods: 'Chiyoda \u00b7 Azabudai \u00b7 Oshiage',
      title: 'Imperial Gardens, teamLab & SkyTree',
      description: "A full day exploring central Tokyo's cultural highlights \u2014 morning serenity at the Imperial Palace gardens, afternoon immersion in teamLab Borderless's digital art universe, and evening views from Tokyo SkyTree. Today hits three of your bookmarked spots while keeping a manageable pace.",
      timeBlocks: [
        {
          label: '\ud83c\udf05 Morning \u2014 Imperial Palace',
          activities: [
            {
              title: 'Imperial Palace East Gardens',
              description: "The only freely accessible part of the Imperial Palace grounds. Walk through the Ote-mon gate into the former Edo Castle's innermost circle \u2014 stone walls, moats, and meticulously maintained gardens. The ninomaru garden is especially beautiful, and the foundation stones of the old castle keep offer panoramic views. Architecture lovers will appreciate the contrast between Edo-era fortifications and modern Tokyo.",
              details: [
                '\ud83d\udcb0 FREE entry',
                '\u23f0 Open 9:00-16:30 (closed Mon & Fri \u2014 but Apr 28 is Tuesday!)',
                '\ud83d\udcf7 The Suwano-chaya tea house reflected in the pond is the money shot',
                '\ud83c\udff0 Allow 60-90 min for a thorough walk around the gardens'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f BREAKFAST',
              name: 'Konbini Breakfast',
              description: "Start the day with a classic konbini run. 7-Eleven and FamilyMart are your vegetarian allies: grab onigiri (umeboshi/plum or kombu/seaweed filling \u2014 these are always veg), a salad, and hot canned coffee or matcha latte.",
              meta: '\ud83d\udccd Any 7-Eleven, FamilyMart, or Lawson \u00b7 \ud83d\udcb0 \u00a5300-500/person'
            }
          ],
          tips: [
            { type: 'tip', text: "\ud83d\udca1 The Imperial Palace outer grounds (Kokyo Gaien) with the famous double bridge are always open \u2014 great for early morning photos before the East Gardens open at 9:00." }
          ]
        },
        {
          label: '\ud83c\udfa8 Afternoon \u2014 teamLab Borderless',
          activities: [
            {
              title: 'teamLab Borderless \u2014 Azabudai Hills',
              description: "The world's first museum without maps or boundaries. Art flows from room to room, projections respond to your touch and movement, and no two visits are ever the same. Now located at Azabudai Hills (moved from Odaiba in 2024), the new venue is even more immersive. Highlights: the Crystal Universe, the infinite flower room, and the En Tea House where your tea blooms with digital flowers.",
              details: [
                '\ud83d\udcb0 \u00a54,000/person (advance tickets ESSENTIAL \u2014 book at teamlab.art)',
                '\u23f0 Allow 2-3 hours to fully explore',
                '\ud83d\udccd Azabudai Hills Garden Plaza B, B1F \u2014 2 min from Kamiyacho Station (Hibiya Line)',
                '\ud83d\udc57 Wear comfortable shoes and avoid white clothing (projections wash out)',
                '\u26a0\ufe0f GOLDEN WEEK: Book your time slot ASAP \u2014 sells out weeks in advance'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f LUNCH',
              name: "T's TanTan \u2014 Tokyo Station",
              description: "Legendary vegan ramen shop inside Tokyo Station's Keiyo Street (basement level). All-plant-based tantanmen (sesame ramen) that's so rich and creamy, you'd never guess it's vegan. The white sesame tantan is the crowd favorite. Fast, affordable, and right in your transit path.",
              meta: '\ud83d\udccd Tokyo Station Keiyo Street B1F \u00b7 \ud83d\udcb0 \u00a5900-1,200/person \u00b7 \u23f0 7:00-23:00'
            }
          ],
          tips: [
            { type: 'reddit', text: "T's TanTan in Tokyo Station is the GOAT vegan ramen. I went three times in a week. The sesame broth is insanely good and it's cheap.", cite: 'r/veganinjapan' },
            { type: 'tip', text: '\ud83c\udfab Book your teamLab time slot for 14:00-15:00 \u2014 usually less crowded than morning slots during Golden Week.' }
          ]
        },
        {
          label: '\ud83c\udf03 Evening \u2014 Tokyo SkyTree',
          activities: [
            {
              title: 'Tokyo SkyTree',
              description: "Japan's tallest structure at 634 meters. The Tembo Deck at 350m gives you a 360-degree panorama of greater Tokyo \u2014 on clear evenings, you might spot Mt Fuji silhouetted against the sunset. The Tembo Galleria at 450m has a sloping glass corridor that feels like walking through the sky.",
              details: [
                '\ud83d\udcb0 Tembo Deck: \u00a52,100/person \u00b7 Combo: \u00a53,100/person',
                '\u23f0 Open until 21:00 (last entry 20:00) \u2014 go at sunset for magic hour',
                '\ud83d\udccd Oshiage Station (direct access)',
                '\ud83d\udca1 The Solamachi complex at the base has food courts with veggie options'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f DINNER',
              name: 'Afuri \u2014 Oshiage/Roppongi',
              description: "Famous for their yuzu shio (citrus salt) ramen \u2014 the vegan version uses a rich kelp and mushroom broth. Light, fragrant, and utterly addictive. Multiple locations across Tokyo; the Roppongi or Oshiage branch works perfectly with today's route.",
              meta: '\ud83d\udccd Multiple locations \u00b7 \ud83d\udcb0 \u00a51,000-1,500/person \u00b7 \u23f0 11:00-23:00'
            }
          ],
          tips: [
            { type: 'tip', text: '\ud83d\udcf8 For the best SkyTree photos FROM outside, head to the Jikken bridge on the Kitajikken River \u2014 the reflection shot is iconic.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7528, label: 'Imperial Palace East Gardens', num: 1, cat: 'attraction', desc: 'Free Edo Castle gardens \u2014 history & architecture' },
        { lat: 35.6812, lng: 139.7671, label: "T's TanTan", num: 2, cat: 'food', desc: 'Legendary vegan ramen inside Tokyo Station' },
        { lat: 35.6585, lng: 139.7385, label: 'teamLab Borderless', num: 3, cat: 'attraction', desc: 'Immersive digital art museum at Azabudai Hills' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo SkyTree', num: 4, cat: 'attraction', desc: '634m tower \u2014 sunset panorama over Tokyo' },
        { lat: 35.7095, lng: 139.8085, label: 'Afuri Ramen', num: 5, cat: 'food', desc: 'Vegan yuzu shio ramen \u2014 light & citrusy' }
      ]
    },

    // === DAY 3: Wed Apr 29 \u2014 Kamakura Day Trip (Showa Day) ===
    {
      num: 3,
      neighborhoods: 'Kamakura \u00b7 Hase \u00b7 Enoshima',
      title: 'Great Buddha, Bamboo Groves & Coastal Walks',
      description: "Escape Tokyo for the ancient capital of Kamakura \u2014 home to the iconic Great Buddha, zen temples hidden in bamboo groves, and a stunning coastal walk. April 29 is Showa Day (Golden Week starts), so leave early to beat crowds. The sea breeze and temple serenity are a perfect counterpoint to Tokyo's intensity.",
      timeBlocks: [
        {
          label: '\ud83c\udf05 Morning \u2014 Temples & Great Buddha',
          activities: [
            {
              title: 'Train to Kamakura + Hokokuji Temple',
              description: "Take the JR Yokosuka Line from Shinjuku/Tokyo to Kamakura (60-75 min, \u00a5950). Start at Hokokuji Temple, known as the Bamboo Temple \u2014 a serene grove of over 2,000 moso bamboo stalks with a matcha tea house hidden inside. Less crowded than Kyoto's Arashiyama and arguably more atmospheric.",
              details: [
                '\ud83d\udcb0 \u00a5300 entry + \u00a5600 for matcha tea in the bamboo garden',
                '\u23f0 Open 9:00-16:00 \u00b7 Bus #24 from Kamakura Station (10 min)',
                '\ud83d\udcf7 Morning light filtering through bamboo is magical \u2014 arrive by 9:30'
              ]
            },
            {
              title: 'K\u014dtoku-in \u2014 The Great Buddha',
              description: "Kamakura's 13.35-meter bronze Amida Buddha has sat in the open air since a tsunami destroyed its temple hall in 1498. You can go inside the hollow statue for \u00a550 extra. One of Japan's most iconic sights.",
              details: [
                '\ud83d\udcb0 \u00a5300/person + \u00a550 to enter interior',
                '\u23f0 8:00-17:30 \u00b7 Enoden Line to Hase Station (3 min walk)',
                '\ud83c\udfdb\ufe0f Over 750 years old \u2014 the patina of centuries gives it incredible presence'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f BREAKFAST',
              name: 'Early Konbini Grab-and-Go',
              description: "Fuel up before the train \u2014 get onigiri, a banana, and a hot coffee from the station konbini. Aim for the 8:00-8:30 train to beat Showa Day crowds.",
              meta: '\ud83d\udccd Shinjuku Station konbini \u00b7 \ud83d\udcb0 \u00a5400/person'
            }
          ],
          tips: [
            { type: 'tip', text: '\u26a1 April 29 is Showa Day (first day of Golden Week). Kamakura gets PACKED by midday \u2014 catch the 8:00-8:30 train to enjoy temples in relative peace.' }
          ]
        },
        {
          label: '\ud83d\udeb6 Afternoon \u2014 Hase & Seaside',
          activities: [
            {
              title: 'Hase-dera Temple',
              description: "Just 5 minutes from the Great Buddha, this hillside temple offers panoramic views of Sagami Bay. The main hall houses a magnificent 9.18m gilt Kannon, and the cave system underneath (Benten-kutsu) is an eerie tunnel lined with candles and small statues.",
              details: [
                '\ud83d\udcb0 \u00a5400/person',
                '\ud83d\udcf7 The observation deck view of the coast is stunning',
                '\ud83c\udf3a April greenery is beautiful even before the famous June hydrangeas'
              ]
            },
            {
              title: 'Komachi-d\u014dri & Yuigahama Beach',
              description: "Walk back to Kamakura Station via Komachi-d\u014dri shopping street for snacks and souvenirs, then head to Yuigahama Beach for a coastal stroll. The Enoden Line from Hase is a charming single-track train that runs between houses \u2014 worth riding just for the experience.",
              details: [
                '\ud83d\udeb6 Komachi-d\u014dri: 5 min walk from Kamakura Station',
                '\ud83d\ude82 Enoden Line: \u00a5260-310 per ride \u2014 a scenic ride itself',
                '\ud83c\udf0a Yuigahama Beach is a pleasant 15-min walk from Hase Station'
              ]
            }
          ],
          meals: [
            {
              type: '\ud83c\udf3f LUNCH',
              name: 'Vegetable Tempura Set \u2014 Komachi-d\u014dri',
              description: "Kamakura's main shopping street has several tempura shops. Order yasai tempura (vegetable tempura) \u2014 sweet potato, lotus root, shiso leaf, eggplant, and shishito peppers deep-fried in a light batter. Specify no dashi in the dipping sauce and use salt instead.",
              meta: '\ud83d\udccd Komachi-d\u014dri, 1 min from Kamakura Station \u00b7 \ud83d\udcb0 \u00a51,000-1,500/person'
            },
            {
              type: '\ud83c\udf3f DINNER',
              name: 'Nagi Shokudo \u2014 Shibuya',
              description: "Back in Tokyo, end the day at Nagi Shokudo, a beloved 100% vegan caf\u00e9 in Shibuya. The daily set meal changes with the seasons \u2014 brown rice, simmered vegetables, miso soup, and pickles. Cozy, homey, soul food.",
              meta: '\ud83d\udccd Shibuya, Udagawacho \u00b7 \ud83d\udcb0 \u00a51,200-1,800/person \u00b7 \u23f0 11:30-21:30 \u00b7 Cash-only'
            }
          ],
          tips: [
            { type: 'reddit', text: "Nagi Shokudo is the soul food of Tokyo vegan dining. The set meal feels like eating at a Japanese grandmother's house \u2014 simple, perfect, nourishing.", cite: 'r/veganinjapan' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3195, lng: 139.5500, label: 'Hokokuji Bamboo Temple', num: 1, cat: 'attraction', desc: '2,000 bamboo stalks + hidden matcha tea house' },
        { lat: 35.3168, lng: 139.5360, label: 'Great Buddha (K\u014dtoku-in)', num: 2, cat: 'attraction', desc: "13.35m bronze Buddha \u2014 Kamakura's icon" },
        { lat: 35.3148, lng: 139.5349, label: 'Hase-dera Temple', num: 3, cat: 'attraction', desc: 'Hillside temple with ocean panorama & cave system' },
        { lat: 35.3069, lng: 139.5505, label: 'Komachi-d\u014dri Street', num: 4, cat: 'food', desc: "Kamakura's main shopping & food street" },
        { lat: 35.3123, lng: 139.5404, label: 'Yuigahama Beach', num: 5, cat: 'attraction', desc: 'Sandy beach with Enoshima island views' },
        { lat: 35.6624, lng: 139.6979, label: 'Nagi Shokudo', num: 6, cat: 'food', desc: '100% vegan caf\u00e9 \u2014 seasonal soul food set meals' }
      ]
    },

    // === DAY 4: Thu Apr 30 \u2014 Mt Fuji & Onsen ===
    {
      num: 4,
      neighborhoods: 'Kawaguchiko \u00b7 Mt Fuji \u00b7 Oshino Hakkai',
      title: 'Mt Fuji, Lakeside Walks & Private Onsen',
      description: "Leave Tokyo for the Fuji Five Lakes region \u2014 Japan's most iconic mountain looming over mirror-still lakes. This overnight in Kawaguchiko combines your Mt Fuji views and private onsen wishes while saving money compared to central Tokyo hotels. The pace is relaxed: nature walks, hot springs, and jaw-dropping scenery.",
      timeBlocks: [
        {
          label: '\ud83c\udf05 Morning \u2014 Journey to Fuji',
          activities: [
            {
              title: 'Shinjuku \u2192 Kawaguchiko (Highway Bus)',
              description: "The Fuji Kyuko highway bus departs from Busta Shinjuku (4F) and goes direct to Kawaguchiko Station in about 2 hours. Book via highway-buses.jp or Willer Express \u2014 Golden Week buses fill up fast! Alternative: JR to Otsuki + Fuji Kyuko Railway (~2.5 hours, more scenic).",
              details: [
                '\ud83d\udcb0 Highway bus: \u00a52,200/person one-way \u00b7 Train: ~\u00a53,500/person',
                '\u23f0 Catch the 8:00 or 8:30 bus to arrive by ~10:30',
                '\ud83c\udfab Book at highway-buses.jp at least 3-4 days ahead for Golden Week',
                '\ud83d\udca1 Sit on the LEFT side of the bus for your first Fuji glimpse'
              ]
            },
            {
              title: 'Kawaguchiko North Shore Walk',
              description: "Drop your bags at your ryokan (most accept luggage from morning) and walk the north shore of Lake Kawaguchi. The Kawaguchiko Ohashi bridge frames Fuji perfectly on clear mornings. Follow the lakeside promenade for the most photogenic angles.",
              details: [
                '\ud83d\udcf7 Best Fuji reflection photos: early morning or late afternoon when the lake is calm',
                '\ud83d\udeb6 North shore promenade: ~3 km easy walk',
                '\ud83c\udf41 The lakeside path has benches everywhere \u2014 perfect for absorbing the view'
              ]
