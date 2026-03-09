const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772668506136_0ijwwa',
  email: 'psyduckler@gmail.com',
  destination: 'Lake Annecy, France',
  startDate: '2026-03-11',
  endDate: '2026-03-15',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Lake Annecy, France',
  countryEmoji: '🇫🇷',
  title: 'Alpine Serenity at Lake Annecy',
  subtitle: '5 days of turquoise waters, medieval charm & mountain escapes for one',
  description: "Lake Annecy in early spring is a secret the French keep to themselves — the turquoise waters are impossibly clear, the snow-capped peaks frame every view, and the medieval old town empties of summer crowds. This solo itinerary mixes lakeside wandering with Savoyard comfort food, fairy-tale castles, and a mountain day trip where you can still find snow. It's slow travel at its finest, in one of the most beautiful corners of the Alps.",
  duration: '4 nights',
  dates: 'Mar 11 – Mar 15, 2026',
  budget: '$$',
  pace: 'Relaxed',
  bestFor: 'Solo Travelers',
  highlights: [
    'Wander Annecy\'s canal-laced Vieille Ville, the "Venice of the Alps"',
    'Savoyard fondue and tartiflette at Le Freti',
    'Château de Menthon-Saint-Bernard — the castle that inspired Sleeping Beauty',
    'Mountain day trip to Le Semnoz with panoramic Alpine views',
    'Lakeside sunrise walk along the Jardins de l\'Europe and Pont des Amours'
  ],

  essentials: [
    { title: '🌤️ March Weather', text: 'Expect 5–12°C with a mix of sun and clouds. Mornings are crisp; afternoons can be surprisingly mild. Pack layers, a warm jacket, and waterproof shoes — spring showers are possible and trails may be muddy.' },
    { title: '🚶 Getting Around', text: 'Annecy\'s old town is entirely walkable. The SIBRA bus network covers lakeside villages (Line 51 to Menthon/Talloires, Line 2 to Semnoz base). For flexibility, rent a car for day trips. Vélo bikes are available for lakeside cycling.' },
    { title: '🧀 Savoyard Cuisine', text: 'This is cheese country. Fondue savoyarde, raclette, tartiflette (potato/reblochon gratin), and croziflette are winter staples still served in March. Local Reblochon and Tomme de Savoie are must-tries. Pair with a crisp Savoie white wine (Apremont or Chignin).' },
    { title: '🗣️ Language & Solo Tips', text: 'English is spoken at hotels and tourist spots, but a few French phrases go far. Annecy is extremely safe for solo travelers. Cafés welcome lingerers — grab a window seat with a book and watch the canals flow by.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-11',
      neighborhoods: 'Vieille Ville · Canal du Thiou · Château d\'Annecy',
      title: 'Arrival — Medieval Canals & Alpine First Light',
      description: 'Arrive in Annecy and lose yourself in one of France\'s most photogenic old towns. Cobblestone arcades, turquoise canals, and the iconic Palais de l\'Isle — all framed by snow-dusted mountains.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Explore the Vieille Ville',
              description: 'After settling in, walk straight into the medieval old town. Cross the Pont Perrière, follow the Canal du Thiou past pastel-painted houses, and discover the Palais de l\'Isle — the 12th-century island prison that\'s become Annecy\'s most photographed landmark.',
              details: [
                '📸 The classic Palais de l\'Isle photo is from the Pont Perrière bridge',
                '🏘️ Rue Sainte-Claire — main arcaded street with shops and cafés',
                '⛪ Église Saint-François de Sales — pale sandstone church along the canal'
              ]
            },
            {
              title: 'Château d\'Annecy',
              description: 'Climb up to the castle perched above the old town. This 12th–16th century fortress houses a regional museum with Alpine art and natural history. The real draw is the panoramic view — red rooftops, the lake, and the Massif des Bauges beyond.',
              details: [
                '🏰 Museum hours: 10am–12pm, 2–5pm (closed Tuesdays)',
                '💰 Entry: ~€5.50',
                '📸 Best viewpoint is from the castle terrace — bring your camera'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The old town is small — you can walk the whole thing in 90 minutes. But slow down. Sit by the canal. Watch the swans. This is the pace for the whole trip.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Pont des Amours',
              description: 'Walk through the Jardins de l\'Europe to the Pont des Amours (Lovers\' Bridge), an iron footbridge spanning the canal where it meets the lake. The sunset view across Lake Annecy from here is legendary — mountains turning pink, water like glass.',
              details: [
                '🌅 Sunset in mid-March is around 6:30pm',
                '🌳 The Jardins de l\'Europe are beautiful for a pre-dinner stroll'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Le Freti',
              description: 'The locals\' pick for Savoyard classics. Le Freti serves what many consider the best fondue and raclette in Annecy — generous portions of melted cheese, charcuterie, and a warm, rustic atmosphere. Perfect first-night solo comfort food.',
              meta: '💰 $$ · 📍 12 Rue Sainte-Claire, Vieille Ville · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.8992, lng: 6.1263, label: 'Palais de l\'Isle', num: 1, cat: 'attraction', desc: '12th-century island prison — Annecy\'s iconic landmark' },
        { lat: 45.8970, lng: 6.1240, label: 'Rue Sainte-Claire', num: 2, cat: 'attraction', desc: 'Medieval arcaded street in the heart of the old town' },
        { lat: 45.9008, lng: 6.1282, label: 'Château d\'Annecy', num: 3, cat: 'attraction', desc: 'Hilltop castle with museum and panoramic views' },
        { lat: 45.9010, lng: 6.1360, label: 'Pont des Amours', num: 4, cat: 'attraction', desc: 'Lovers\' Bridge with sunset lake views' },
        { lat: 45.9005, lng: 6.1340, label: 'Jardins de l\'Europe', num: 5, cat: 'attraction', desc: 'Lakeside gardens with mountain backdrop' },
        { lat: 45.8987, lng: 6.1264, label: 'Le Freti', num: 6, cat: 'food', desc: 'Best fondue and raclette in Annecy' }
      ]
    },
    {
      num: 2,
      date: '2026-03-12',
      neighborhoods: 'Lac d\'Annecy · Menthon-Saint-Bernard · Talloires',
      title: 'Fairy-Tale Castles & Lakeside Villages',
      description: 'Head east along the lake to discover the charming villages that dot its shores. Visit a real fairy-tale castle, walk through a medieval hamlet, and enjoy a lakeside lunch with views that belong on a postcard.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Lakeside Walk & Morning Coffee',
              description: 'Start with a walk along the Pâquier esplanade — a wide grassy lakefront stretching from the Jardins de l\'Europe. In March, the lake is mirror-still and the mountains are reflected perfectly. Grab a coffee at one of the cafés along the Quai Napoléon III.',
              details: [
                '☕ Café des Arts on Place Sainte-Claire for excellent espresso',
                '🏔️ La Tournette (2,351m) dominates the eastern skyline',
                '🦢 Swans and ducks patrol the lakefront year-round'
              ]
            },
            {
              title: 'Château de Menthon-Saint-Bernard',
              description: 'Take the bus or drive 10km south to this breathtaking medieval castle perched 200m above the lake. Said to have inspired Walt Disney\'s Sleeping Beauty castle, it\'s been home to the same family for over 1,000 years. The turrets, towers, and lake panorama are unforgettable.',
              details: [
                '🏰 Open for guided tours — check seasonal schedule (limited in March)',
                '🚌 Bus 51 from Annecy gare routière, ~20 min',
                '📸 The approach from below, looking up at the castle against the Alps, is magical'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Talloires Village & Lakeside Stroll',
              description: 'Continue along the eastern shore to Talloires, a tiny lakeside village nestled in a bay below sheer cliffs. The Abbaye de Talloires (now a luxury hotel) and the quiet waterfront promenade make this feel like stepping into a painting.',
              details: [
                '🏔️ Talloires sits at the foot of the Roc de Chère nature reserve',
                '🚶 Walk the Sentier du Roc de Chère — a 1-hour forest loop with lake views',
                '📍 Population: ~1,700 — it\'s delightfully quiet in March'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Auberge du Père Bise',
              description: 'A legendary lakeside restaurant in Talloires with a Michelin-starred pedigree. Even the bistro menu is superb — fresh lake fish (féra, omble chevalier), local produce, and those views. Treat yourself.',
              meta: '💰 $$$ · 📍 Route du Port, Talloires · Book ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening in the Old Town',
              description: 'Return to Annecy and wander the old town as the evening lights reflect in the canals. The arcaded streets glow warmly, and the café terraces are cozy with outdoor heaters even in March.',
              details: [
                '🌙 The canals lit up at night are stunning — different character than daytime',
                '🍷 Try a glass of Mondeuse (local Savoie red) at a wine bar'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'L\'Esquisse',
              description: 'Modern French bistro near the old town with creative seasonal dishes. The chef sources locally and the menu changes frequently. Excellent wine pairings and a warm, intimate atmosphere perfect for solo dining at the bar.',
              meta: '💰 $$$ · 📍 21 Rue Royale · Closed Sundays'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.9020, lng: 6.1350, label: 'Le Pâquier Esplanade', num: 1, cat: 'attraction', desc: 'Wide lakefront promenade with mountain views' },
        { lat: 45.8630, lng: 6.1960, label: 'Château de Menthon-Saint-Bernard', num: 2, cat: 'attraction', desc: '1,000-year-old fairy-tale castle above the lake' },
        { lat: 45.8420, lng: 6.2140, label: 'Talloires', num: 3, cat: 'attraction', desc: 'Charming lakeside village in a sheltered bay' },
        { lat: 45.8430, lng: 6.2120, label: 'Auberge du Père Bise', num: 4, cat: 'food', desc: 'Legendary lakeside restaurant with lake fish' },
        { lat: 45.8480, lng: 6.2050, label: 'Roc de Chère', num: 5, cat: 'attraction', desc: 'Nature reserve with forest trails and lake views' },
        { lat: 45.8988, lng: 6.1270, label: 'L\'Esquisse', num: 6, cat: 'food', desc: 'Modern French bistro with seasonal cuisine' }
      ]
    },
    {
      num: 3,
      date: '2026-03-13',
      neighborhoods: 'Le Semnoz · Forêt du Semnoz · Mountain Panoramas',
      title: 'Mountain Day — Snow, Forest & Alpine Views',
      description: 'Escape to the mountains just 20 minutes from Annecy. Le Semnoz is the city\'s backyard mountain — at 1,700m you\'ll find snow, cross-country ski trails, snowshoe paths, and a 360° panorama from Mont Blanc to the Chartreuse.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive Up to Le Semnoz',
              description: 'The winding D41 road climbs from Annecy through dense fir forests to the summit plateau of Le Semnoz (1,704m). In March, there\'s usually still snow at the top. The road itself is an experience — each hairpin turn reveals a broader panorama.',
              details: [
                '🚗 20km from Annecy center, ~30 min drive',
                '🏔️ Summit: Crêt de Chatillon (1,699m) — 360° views',
                '❄️ Snow likely still present in March — check conditions'
              ]
            },
            {
              title: 'Snowshoeing or Winter Walking',
              description: 'At the Semnoz plateau, you can rent snowshoes or simply walk the groomed trails through the snow-covered forest. The silence up here is profound — just wind, birds, and crunching snow. The cross-country ski trails are also open if you want to try.',
              details: [
                '🥾 Snowshoe rental available at the station',
                '⛷️ 30km of cross-country tracks if conditions allow',
                '🌲 The fir forests are magical with snow — total solitude'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Summit Panorama at Crêt de Chatillon',
              description: 'Hike to the summit marker at Crêt de Chatillon for one of the finest viewpoints in the Haute-Savoie. On a clear day, you can see Mont Blanc, the Aravis range, the Bauges massif, and Lake Annecy far below — a shimmering turquoise sliver.',
              details: [
                '📸 Mont Blanc is visible to the east on clear days',
                '🗺️ Orientation tables at the summit identify all visible peaks',
                '🌤️ Best visibility is usually in the morning — arrive early if possible'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Chalet du Semnoz',
              description: 'Mountain refuge restaurant at the Semnoz station. Hearty mountain fare — croûtes savoyardes (open-faced cheese toasts), soups, and tartiflette. Eat on the terrace if the sun is out — nothing beats mountain food at altitude.',
              meta: '💰 $ · 📍 Station du Semnoz · Cash helpful'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return & Old Town Market Browse',
              description: 'Head back down to Annecy. If it\'s a Tuesday or Friday, catch the tail end of the famous Annecy market — one of the biggest in the Haute-Savoie. Even on other days, the fromageries and charcuteries along Rue Sainte-Claire are worth browsing for Reblochon, Tomme, and dried sausages.',
              details: [
                '🧀 Fromagerie La Ferme des Aravis — incredible cheese selection',
                '🛒 Market days: Tuesday, Friday, and Sunday mornings',
                '🍯 Pick up local honey, lavender, or Alpine herb teas as souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Le Lilas Rose',
              description: 'Another beloved local spot for raclette — voted best in Annecy by many regulars. All-you-can-eat raclette with top-quality cheese, charcuterie, and potatoes. The warm, convivial vibe is wonderful for a solo traveler on a cold March evening.',
              meta: '💰 $$ · 📍 14 Faubourg Sainte-Claire · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.8230, lng: 6.1060, label: 'Le Semnoz Station', num: 1, cat: 'attraction', desc: 'Mountain resort with snowshoe trails and cross-country skiing' },
        { lat: 45.8200, lng: 6.1080, label: 'Crêt de Chatillon', num: 2, cat: 'attraction', desc: '1,699m summit with 360° Alpine panorama' },
        { lat: 45.8220, lng: 6.1070, label: 'Chalet du Semnoz', num: 3, cat: 'food', desc: 'Mountain chalet restaurant with Savoyard fare' },
        { lat: 45.8987, lng: 6.1264, label: 'Rue Sainte-Claire Market', num: 4, cat: 'attraction', desc: 'Famous market street with cheese and charcuterie shops' },
        { lat: 45.8980, lng: 6.1250, label: 'Le Lilas Rose', num: 5, cat: 'food', desc: 'Top-rated all-you-can-eat raclette spot' }
      ]
    },
    {
      num: 4,
      date: '2026-03-14',
      neighborhoods: 'West Shore · Duingt · Col de la Forclaz · Annecy-le-Vieux',
      title: 'The Western Shore & Hidden Viewpoints',
      description: 'Explore the quieter western side of the lake. Drive to the charming village of Duingt with its lakeside castle, climb to the Col de la Forclaz for the most dramatic viewpoint over the lake, and finish in the laid-back neighbourhood of Annecy-le-Vieux.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive the Western Lakeshore to Duingt',
              description: 'Take the D1508 along the western shore — the road hugs the lake with mountains rising on both sides. Stop at Duingt, a tiny village dominated by the Château de Duingt on its own peninsula. The castle is private, but the views from the village shore are magical.',
              details: [
                '🏰 Château de Duingt sits on a narrow peninsula — visible from the shore path',
                '📍 Duingt marks the narrowest point of the lake',
                '📸 The view back toward Annecy with the mountains is spectacular'
              ]
            },
            {
              title: 'Col de la Forclaz Viewpoint',
              description: 'Continue south and wind up to the Col de la Forclaz (1,150m) — the most famous viewpoint over Lake Annecy. The lake stretches below in its full glory, divided by the Roc de Chère promontory, with snow-capped peaks in every direction. This is a famous paragliding launch site in summer.',
              details: [
                '🏔️ 1,150m altitude — the view is breathtaking',
                '📸 This is THE postcard viewpoint of Lake Annecy',
                '🅿️ Parking at the col, short walk to viewpoints',
                '🪂 Paragliders launch from here in warmer months — you may see early-season flyers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Restaurant du Col de la Forclaz',
              description: 'Mountain restaurant at the pass with a sun-drenched terrace overlooking the lake far below. Simple, hearty dishes — omelettes, salads, and Savoyard plates. The setting is the star.',
              meta: '💰 $$ · 📍 Col de la Forclaz · Seasonal hours — check before going'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Annecy-le-Vieux & Lakeside Path',
              description: 'Return to Annecy and explore the neighbouring commune of Annecy-le-Vieux. Walk the lakeside path from the Impérial Palace park northward — it\'s quieter than the main town promenade and offers different perspectives on the lake and the distant Semnoz.',
              details: [
                '🏛️ Annecy-le-Vieux has a charming old village core with a Romanesque bell tower',
                '🚶 The lakeside path continues north toward Veyrier — peaceful and scenic',
                '🦆 Great birdwatching along this stretch in early spring'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Night — Aperitif & Farewell Dinner',
              description: 'Your last evening in Annecy. Take a final stroll through the old town, perhaps stopping for a kir savoyard (white wine with blackcurrant) at a canal-side terrace. Then settle in for a memorable farewell dinner.',
              details: [
                '🥂 Kir savoyard or a glass of Roussette de Savoie as aperitif',
                '🌙 The old town is magical at night — reflections in the canals'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Le Clos des Sens',
              description: 'For a special farewell, treat yourself to Laurent Petit\'s renowned restaurant in Annecy-le-Vieux. Creative, modern Alpine cuisine using hyper-local ingredients — lake fish, mountain herbs, Alpine dairy. A culinary experience that captures everything beautiful about this region.',
              meta: '💰 $$$$ · 📍 13 Rue Jean Mermoz, Annecy-le-Vieux · Book well ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.8330, lng: 6.1680, label: 'Duingt', num: 1, cat: 'attraction', desc: 'Charming village with lakeside castle on a peninsula' },
        { lat: 45.8130, lng: 6.2210, label: 'Col de la Forclaz', num: 2, cat: 'attraction', desc: 'Famous viewpoint — the best panorama of Lake Annecy' },
        { lat: 45.8130, lng: 6.2210, label: 'Restaurant du Col de la Forclaz', num: 3, cat: 'food', desc: 'Mountain restaurant with terrace overlooking the lake' },
        { lat: 45.9120, lng: 6.1450, label: 'Annecy-le-Vieux', num: 4, cat: 'attraction', desc: 'Quiet lakeside commune with Romanesque village core' },
        { lat: 45.9100, lng: 6.1410, label: 'Le Clos des Sens', num: 5, cat: 'food', desc: 'Laurent Petit\'s celebrated Alpine cuisine' }
      ]
    },
    {
      num: 5,
      date: '2026-03-15',
      neighborhoods: 'Vieille Ville · Lac d\'Annecy · Departure',
      title: 'Departure — One Last Lakeside Morning',
      description: 'A slow final morning to soak in the Alpine air. Sunrise by the lake, a last wander through the old town, and a proper French breakfast before heading home with your head full of mountains, cheese, and turquoise water.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise Walk Along the Lake',
              description: 'Wake early for one last lakeside walk. The Pâquier esplanade at sunrise, with the mountains emerging from mist and the lake catching the first light, is something you\'ll remember forever. The air is cold and clean. The Alps are quiet.',
              details: [
                '🌅 Sunrise in mid-March is around 7:00am',
                '📸 The reflection of La Tournette in the still morning water is extraordinary',
                '🦢 The swans are usually out at dawn'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Patisserie Fidèle',
              description: 'One of Annecy\'s best bakeries for a proper last morning. Flaky croissants, pain au chocolat, and excellent coffee. Sit at the tiny tables inside and watch the old town wake up.',
              meta: '💰 $ · 📍 Rue Royale, Vieille Ville'
            }
          ],
          tips: [
            { type: 'tip', text: 'If you have time before your departure, stop at the Sunday market (if it\'s Sunday) or pick up a wheel of Reblochon from a fromagerie — it travels surprisingly well and makes the best souvenir.' }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Final Old Town Stroll & Departure',
              description: 'Take one last loop through the canals, past the Palais de l\'Isle, along Rue Sainte-Claire. Annecy has a way of feeling like home very quickly — and leaving is always harder than arriving. Head to Geneva Airport (45 min) or Lyon (1h45) for your flight.',
              details: [
                '✈️ Geneva Airport (GVA): 45 min drive — closest international airport',
                '✈️ Lyon-Saint Exupéry (LYS): 1h45 — more flight options',
                '🚂 Annecy SNCF station: direct trains to Paris Gare de Lyon (3h40 TGV)'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 45.9020, lng: 6.1350, label: 'Le Pâquier (Sunrise Walk)', num: 1, cat: 'attraction', desc: 'Lakefront esplanade — sunrise with mountain reflections' },
        { lat: 45.8995, lng: 6.1275, label: 'Patisserie Fidèle', num: 2, cat: 'food', desc: 'Top bakery for croissants and coffee' },
        { lat: 45.8992, lng: 6.1263, label: 'Palais de l\'Isle (Farewell)', num: 3, cat: 'attraction', desc: 'One last look at Annecy\'s most iconic view' },
        { lat: 45.9020, lng: 6.1210, label: 'Annecy SNCF Station', num: 4, cat: 'attraction', desc: 'Train station — TGV to Paris, regional connections' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '€50–80/night', midrange: '€100–180/night', luxury: '€200–400/night' },
    { category: 'Meals (solo)', budget: '€25–40/day', midrange: '€50–90/day', luxury: '€100–200/day' },
    { category: 'Transport', budget: '€5–15/day (bus)', midrange: '€40–60/day (car rental)', luxury: '€80–150/day (private)' },
    { category: 'Activities', budget: '€0–15/day', midrange: '€15–40/day', luxury: '€50–120/day' },
    { category: '5-Day Total (solo)', budget: '€400–700', midrange: '€900–1,600', luxury: '€2,000–3,800' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Geneva Airport (GVA) is 45 min by car — closest international hub', 'Lyon-Saint Exupéry (LYS) is 1h45 — more European connections', 'TGV from Paris Gare de Lyon: 3h40 direct to Annecy', 'FlixBus and BlaBlaCar also serve Annecy'] },
    { title: '🏨 Where to Stay', items: ['Hôtel du Palais de l\'Isle — right on the canal, can\'t beat the location', 'Les Trésoms — lakeside with pool and panoramic views', 'Airbnb in Vieille Ville — character + kitchen for solo flexibility', 'Annecy-le-Vieux — quieter, local feel, still walkable to old town'] },
    { title: '🌡️ Weather', items: ['March averages 5–12°C (41–54°F) — warming toward spring', 'Expect a mix of sun and overcast days', 'Mountains still have snow above 1,500m', 'Layer up — mornings are cold, afternoons can be mild in the sun'] },
    { title: '💳 Money', items: ['Euros (€) — France is in the eurozone', 'Cards accepted almost everywhere — some mountain restaurants prefer cash', 'Tipping: round up or leave 5–10% for good service (not obligatory)', 'ATMs in the old town and at the train station'] },
    { title: '📱 Connectivity', items: ['French SIM or eSIM from Free Mobile (€2/month) at a Free shop', 'WiFi at virtually all hotels and cafés', 'Cell coverage good in town, spotty on mountain roads and Semnoz summit', 'Download offline maps for driving days'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
