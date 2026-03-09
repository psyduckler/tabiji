const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772393016214_7fw1b7",
  email: "heathervandeest@gmail.com",
  destination: "London, UK",
  start_date: "2026-06-03",
  end_date: "2026-06-07",
  group_size: "3-4",
  travel_style: "Cultural, Family-friendly",
  dining: "Casual throughout",
  budget: "Under $1,000",
  requests: "Include tower of london, st paul's cathedral, church hill war rooms, and a quick stop by Buckingham palace. Also please work in a visit to the Camden Locks and market and a couple of hours for the British Museum. We're staying in Covent Garden.",
  amount: "0.00",
  timestamp: "2026-03-01T19:23:36.214Z",
  status: "pending"
};

const itineraryData = {
  destination: "London, UK",
  countryEmoji: "🇬🇧",
  title: "London Family Adventure: Icons, Markets & Hidden Gems",
  subtitle: "Covent Garden → Royal London → Tower of London → British Museum → Camden",
  description: "A perfectly paced 5-day London itinerary for families — hitting every must-see landmark while leaving room for spontaneous wanders and affordable casual meals. Buckingham Palace, Churchill War Rooms, Tower of London, St Paul's Cathedral, British Museum, Camden Market, and the charm of your Covent Garden home base. June is the perfect time: long evenings, warm days, and London in full bloom.",
  duration: "5 days",
  dates: "Jun 3 – 7, 2026",
  budget: "Budget-friendly",
  pace: "Balanced — full days with breathing room, family-friendly pacing",
  bestFor: "Families, culture lovers & first-timers",
  highlights: [
    "Tower of London — Crown Jewels, Beefeater tours & 1,000 years of history",
    "Churchill War Rooms — Winston Churchill's secret WWII underground bunker",
    "St Paul's Cathedral — climb the dome for panoramic London views",
    "Buckingham Palace & Changing of the Guard ceremony",
    "British Museum — free entry and genuinely world-class collections",
    "Camden Locks & Market — street food, vintage, and buzzing canal vibes",
    "Borough Market — London's legendary food market a short walk away",
    "Covent Garden piazza — street performers, restaurants & family fun steps from your hotel",
    "South Bank walk — Tate Modern, the Thames, and the London Eye",
    "Long June evenings with the sun setting after 9pm — max exploration time"
  ],
  essentials: [
    { title: "🚇 Getting Around", text: "Get Oyster cards (or use contactless bank cards) on arrival — works on the Tube, buses, and DLR. Daily spend caps in Zone 1-2 keep costs reasonable (~£9/day per person). The Tube is fast; buses show you the city. Your Covent Garden base puts you walking distance from Trafalgar Square, the South Bank, and the West End." },
    { title: "💷 Money & Budget", text: "Many of London's best attractions are free: British Museum, National Gallery, Tate Modern, all royal parks. Budget roughly £30-40pp/day for food eating casually. Pre-book Tower of London and Churchill War Rooms online (cheaper than door price and skips queues). Supermarkets like Sainsbury's Local and Tesco Express (everywhere) are great for breakfast supplies and snacks." },
    { title: "☀️ June Weather", text: "Expect 18-22°C with long sunny days — sunset isn't until 9:15pm! Pack a light layer for evenings and a compact umbrella just in case (London surprises you). June is peak tourist season so pre-booking popular attractions is essential." },
    { title: "👨‍👩‍👧 Family Tips", text: "London is extremely family-friendly. The Tube is manageable with kids (escalators, lifts at major stations). Beefeater tours at the Tower of London are a highlight for all ages. All major parks have playgrounds. Many museums have children's activity trails — pick one up at the entrance. London taxis (black cabs) seat 5 and are fun for kids." },
    { title: "🏨 Your Base: Covent Garden", text: "Brilliant location — the piazza with street performers is right outside, the West End theatres are steps away, and you can walk to Trafalgar Square in 5 minutes. Loads of casual cafés and restaurants within 5 minutes. Seven Dials (a short walk north) is a charming neighborhood with good casual dining." },
    { title: "📱 Useful Apps", text: "Citymapper (London's best transport app — better than Google Maps for the Tube), TfL Go (official), Google Maps for walking. Pre-book: toweroflondontours.org (Tower of London), iwm.org.uk (Churchill War Rooms), stpauls.co.uk (St Paul's). All accept credit cards." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival, Covent Garden & South Bank Introduction",
      neighborhoods: "Covent Garden · Trafalgar Square · South Bank",
      date: "Jun 3",
      mapPins: [
        { lat: 51.5129, lng: -0.1243, label: "Covent Garden Piazza", num: 1, cat: "activity", desc: "Street performers, market stalls & your neighborhood home base" },
        { lat: 51.5117, lng: -0.1267, label: "Seven Dials", num: 2, cat: "activity", desc: "Seven streets meet — charming shops, cafés and casual restaurants" },
        { lat: 51.5080, lng: -0.1281, label: "Trafalgar Square", num: 3, cat: "activity", desc: "Nelson's Column, bronze lions & the National Gallery" },
        { lat: 51.5089, lng: -0.1283, label: "National Gallery", num: 4, cat: "activity", desc: "World-class art museum — free entry" },
        { lat: 51.5076, lng: -0.0994, label: "Tate Modern", num: 5, cat: "activity", desc: "Free modern art gallery in a converted power station" },
        { lat: 51.5033, lng: -0.1195, label: "London Eye", num: 6, cat: "activity", desc: "Iconic observation wheel on the South Bank" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Settle In & Explore Covent Garden", description: "Drop your bags and take a first wander around your neighborhood. The Covent Garden piazza has free street performers all day — acrobats, musicians, comedy acts. The kids will love it. The indoor Apple Market sells handmade crafts and there are affordable cafés everywhere.", details: ["📍 Covent Garden Tube station (Piccadilly line)", "💡 The piazza is at its liveliest from 10am onwards."] },
            { title: "Seven Dials", description: "Walk five minutes north to Seven Dials — where seven streets radiate from a sundial pillar. Independent shops, coffee spots, and a village-within-a-city feel. Good for a first-morning wander.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Monmouth Coffee (Covent Garden)", description: "One of London's best coffee roasters is right in the neighborhood. Simple, excellent coffee and pastries. Join the locals.", meta: "£5-10pp · 27 Monmouth St · Walk-in" }
          ],
          tips: [{ type: "tip", text: "London supermarkets (Sainsbury's, Tesco) are everywhere and much cheaper than tourist cafés for breakfast supplies. Stock up on first-day snacks." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Trafalgar Square & National Gallery", description: "Walk 10 minutes to Trafalgar Square — iconic view with Nelson's Column and bronze lions (perfect photo with kids). The National Gallery behind it is completely free and houses Van Gogh's Sunflowers, Monet's water lilies, and da Vinci paintings. Even with kids, a 45-minute wander through is worthwhile.", details: ["📍 10 min walk from Covent Garden", "💡 Free entry. Kids love spotting familiar paintings."] },
            { title: "South Bank Walk", description: "Walk along the Thames to Waterloo Bridge, cross over and stroll the South Bank. The stretch along the river past the Southbank Centre, National Theatre, and Tate Modern is one of London's great free experiences — street performers, food stalls, river views, and people-watching.", details: [] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "South Bank Food Stalls", description: "The South Bank always has food trucks and stalls near the Southbank Centre. Affordable, varied options — burritos, burgers, crepes, and more. Grab and eat by the river.", meta: "£8-12pp · South Bank riverside" }
          ],
          tips: [{ type: "tip", text: "Waterloo Bridge has arguably the best views in London — the City skyline to the left, Parliament and Big Ben to the right. Stop at the midpoint on both sides." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Back to Covent Garden for Dinner", description: "Head back to your base. Covent Garden has loads of casual restaurant options for families — the Seven Dials area has everything from Italian to Thai.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Dishoom (Covent Garden)", description: "Bombay-inspired café that's become a London institution. Family-friendly, all ages love it. The chicken tikka, black daal, and naan bread are incredible. Go at 5:30-6pm to get seated quickly — queues build after 7pm.", meta: "£15-20pp · 12 Upper St Martin's Lane · Walk-in, arrive early" }
          ],
          tips: [{ type: "reddit", text: "Dishoom is absolutely worth it. The black daal has been slow-cooked for 24 hours. With kids, go early (5:30pm) — the queue at 7pm can be 45 minutes but early evening is much more manageable.", cite: "r/london" }]
        },
        {
          label: "Late Afternoon",
          activities: [
            { title: "Covent Garden Piazza Evening", description: "After dinner, enjoy the piazza as the evening performers take over. London in June stays light until after 9pm — there's no rush. Ice cream from one of the nearby shops and a wander through the covered market is a perfect first evening.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "June means incredibly long days in London. Sunset is around 9:15pm — you'll feel like you have endless time. Take advantage with post-dinner walks." }]
        }
      ]
    },
    {
      num: 2,
      title: "Royal London: Buckingham Palace, Churchill War Rooms & Westminster",
      neighborhoods: "Westminster · St James's · Victoria",
      date: "Jun 4",
      mapPins: [
        { lat: 51.5014, lng: -0.1419, label: "Buckingham Palace", num: 1, cat: "activity", desc: "Royal residence — Changing of the Guard at 11am" },
        { lat: 51.5013, lng: -0.1350, label: "St James's Park", num: 2, cat: "activity", desc: "London's most beautiful royal park with pelicans" },
        { lat: 51.5014, lng: -0.1295, label: "Churchill War Rooms", num: 3, cat: "activity", desc: "Winston Churchill's secret WWII underground bunker" },
        { lat: 51.4995, lng: -0.1246, label: "Big Ben & Westminster", num: 4, cat: "activity", desc: "Houses of Parliament and Elizabeth Tower" },
        { lat: 51.4994, lng: -0.1228, label: "Westminster Bridge", num: 5, cat: "activity", desc: "Classic London view — Big Ben from the bridge" },
        { lat: 51.5138, lng: -0.0984, label: "St Paul's Cathedral", num: 6, cat: "activity", desc: "Sir Christopher Wren's masterpiece — climb the dome" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Buckingham Palace & Changing of the Guard", description: "Take the Tube to St James's Park station. Walk through the park (gorgeous in June) to arrive at Buckingham Palace by 10:30am for a good viewing spot. The Changing of the Guard ceremony happens at 11am on most days in summer — it's free, colorful, and kids love the horses, bearskin hats, and military band.", details: ["💡 In June, Changing of the Guard typically runs daily at 11am — confirm at householddivision.org.uk the day before.", "📍 St James's Park or Victoria Tube, then short walk"] },
            { title: "St James's Park", description: "Walk back through St James's Park after the ceremony. It's London's prettiest park — the bridge over the lake gives a magical view with Buckingham Palace on one side and Horse Guards on the other. Pelicans live by the lake (fed at 2:30pm daily). Perfect for a 20-minute wander.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Grab breakfast near hotel before heading out", description: "Stock up from your local Sainsbury's Local or grab a coffee at one of the Covent Garden cafés before the Tube journey.", meta: "£5-8pp · Covent Garden area" }
          ],
          tips: [{ type: "tip", text: "Arrive at the palace gates by 10:30am to secure a good spot for the ceremony. The right-hand side (facing the palace) typically offers clearer views of the guardsmen emerging." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Churchill War Rooms", description: "A 5-minute walk from St James's Park, this is one of London's most atmospheric and fascinating attractions. Winston Churchill ran WWII from this underground bunker — the rooms are preserved exactly as they were in 1945. The Churchill Museum within is brilliant for all ages. Allow 2-2.5 hours.", details: ["💡 Pre-book online at iwm.org.uk for a timed entry — cheaper than door price (around £27pp). Kids under 15 free!", "📍 Clive Steps, King Charles St, Westminster"] },
            { title: "Westminster Walk", description: "Exit the War Rooms and walk five minutes to Westminster Bridge. Big Ben, the Houses of Parliament, and Westminster Abbey are all here. Walk across the bridge for the classic view.", details: ["💡 Westminster Abbey has an entry fee (~£29pp). If budget is tight, admire the exterior — it's stunning."] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Cabinet War Rooms Café or nearby supermarket", description: "The café inside the Churchill War Rooms is surprisingly good. Or grab food from the Sainsbury's near Victoria for a picnic in St James's Park — much cheaper and the park setting is lovely.", meta: "£8-15pp · In or near Churchill War Rooms" }
          ],
          tips: [{ type: "reddit", text: "Churchill War Rooms absolutely blew my mind. The Map Room is still as it was on the final day of the war in 1945. With kids, it's also incredibly engaging — like stepping into history.", cite: "r/london" }]
        },
        {
          label: "Late Afternoon",
          activities: [
            { title: "St Paul's Cathedral", description: "Walk or take the Tube to St Paul's. Sir Christopher Wren's baroque masterpiece is one of the world's great buildings. Inside, the Whispering Gallery (you can whisper along the dome and hear it on the other side) is magical for kids. Climb higher to the Stone Gallery and the Golden Gallery at the very top for 360° panoramic London views.", details: ["📍 St Paul's Tube (Central line)", "💡 Pre-book online at stpauls.co.uk — around £20pp (kids under 6 free). Climbing to the top is free with your ticket but involves 528 steps."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The view from the top of St Paul's dome is breathtaking — the entire City of London spread out before you. Go in the afternoon when the light is best." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Dinner near Covent Garden or the West End", description: "After a full day on your feet, head back to your Covent Garden base for a casual dinner.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Wahaca (Covent Garden)", description: "Mexican street food inspired by Rick Stein's travels — colorful, casual, family-perfect. Tacos, quesadillas, guacamole. Budget-friendly and kids love it. Multiple dishes to share makes it fun.", meta: "£12-18pp · 66 Chandos Place, Covent Garden · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Tower of London, Tower Bridge & Borough Market",
      neighborhoods: "City of London · Southwark · London Bridge",
      date: "Jun 5",
      mapPins: [
        { lat: 51.5081, lng: -0.0759, label: "Tower of London", num: 1, cat: "activity", desc: "Crown Jewels, Beefeater tours & 1,000 years of history" },
        { lat: 51.5055, lng: -0.0754, label: "Tower Bridge", num: 2, cat: "activity", desc: "Victorian Gothic bridge — cross it and look down through the glass floor" },
        { lat: 51.5055, lng: -0.0910, label: "Borough Market", num: 3, cat: "food", desc: "London's legendary food market under the railway arches" },
        { lat: 51.5138, lng: -0.0984, label: "St Paul's (view from South Bank)", num: 4, cat: "activity", desc: "Great view of the dome from Millennium Bridge" },
        { lat: 51.5063, lng: -0.0960, label: "Tate Modern (Turbine Hall)", num: 5, cat: "activity", desc: "Free — the Turbine Hall has mind-blowing installations" },
        { lat: 51.5099, lng: -0.1181, label: "South Bank walk", num: 6, cat: "activity", desc: "Riverside stroll connecting all these highlights" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tower of London", description: "Arrive at opening (9am) to make the most of your time and beat the crowds. First thing: join a free Yeoman Warder (Beefeater) tour — they're funny, dark, and incredibly knowledgeable. Kids absolutely love the raven stories and grisly history. Then see the Crown Jewels (the Imperial State Crown alone is staggering) and the White Tower.", details: ["💡 Pre-book timed entry at hrp.org.uk/tower-of-london — around £33pp, kids 5-15 ~£16.50, under 5 free. Worth every penny.", "📍 Tower Hill Tube (Circle/District lines)", "⏰ Allow 2.5-3 hours minimum"] },
            { title: "Tower Bridge", description: "Walk across Tower Bridge after the Tower — it's free to walk across. The views up and down the Thames are beautiful. The Tower Bridge Exhibition (£12pp) includes the glass-floor walkway 42 metres above the river — kids either love it or refuse to move! Great fun if you're up for it.", details: ["💡 The glass floor walkway is genuinely exciting — well worth it if the budget allows."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "The Beefeater tours are the hidden gem of the Tower of London. They're not listed prominently but they're free with admission and absolutely brilliant — funny, dark history, great for all ages. Ask at the entrance where the next one starts.", cite: "r/london" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Borough Market", description: "Walk 15 minutes west along the South Bank to Borough Market — London's legendary food market under the Victorian railway arches. Perfect for a late lunch: graze the stalls. Spanish charcuterie, fresh pasta at Padella (queue moves fast), incredible bread, artisan cheeses, fresh seafood, and every street food imaginable.", details: ["📍 London Bridge Tube or short walk from Tower Bridge", "💡 Open Monday-Saturday. Best variety Thursday-Saturday."] },
            { title: "Millennium Bridge & St Paul's View / Tate Modern", description: "After lunch, walk west along the South Bank to the Millennium Bridge. Cross it for a stunning view of St Paul's Cathedral straight ahead. The Tate Modern is right next to the bridge — entry is free and the Turbine Hall almost always has a large-scale installation that kids find fascinating. No need to stay long — 30-45 minutes is enough.", details: ["📍 Free entry to Tate Modern"] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Borough Market Grazing", description: "Don't sit down — graze! Padella for fresh pasta (expect a queue but worth it), Kappacasein for raclette, Bread Ahead for legendary doughnuts, Brindisa for Spanish tapas bites. Let everyone pick their favorite thing.", meta: "£10-15pp grazing · Borough Market · Thurs-Sat best variety" }
          ],
          tips: [{ type: "tip", text: "Bread Ahead Bakery at Borough Market makes the best doughnuts in London. Cream-filled, custard, jam — get one for each family member and eat them on the riverbank." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "South Bank Stroll Back to Covent Garden", description: "Walk or Tube back. The South Bank is beautiful in the long June evening light. Stop at the outdoor book stalls under Waterloo Bridge (open daily, one of London's institutions).", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Pizza Pilgrims (Covent Garden)", description: "Neapolitan pizza done right — charred, bubbly bases, simple quality toppings. Great for families, casual vibe, and right in your Covent Garden neighborhood. A popular London mini-chain that does pizza genuinely well.", meta: "£12-18pp · 11 Kingsway, Covent Garden · Book online or walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "British Museum & Camden Market",
      neighborhoods: "Bloomsbury · Camden · Primrose Hill",
      date: "Jun 6",
      mapPins: [
        { lat: 51.5194, lng: -0.1270, label: "British Museum", num: 1, cat: "activity", desc: "World-class museum — Rosetta Stone, Egyptian mummies, free entry" },
        { lat: 51.5430, lng: -0.1468, label: "Camden Market", num: 2, cat: "activity", desc: "One of London's most vibrant markets — food, fashion, music" },
        { lat: 51.5439, lng: -0.1475, label: "Camden Lock", num: 3, cat: "activity", desc: "The original lock on Regent's Canal — great atmosphere" },
        { lat: 51.5379, lng: -0.1516, label: "Regent's Canal Walk", num: 4, cat: "activity", desc: "Peaceful towpath walk from Camden towards Primrose Hill" },
        { lat: 51.5441, lng: -0.1593, label: "Primrose Hill", num: 5, cat: "activity", desc: "Hilltop park with one of London's best skyline views" },
        { lat: 51.5179, lng: -0.1193, label: "Bloomsbury Cafés", num: 6, cat: "food", desc: "Quiet Georgian streets full of independent cafés near the museum" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "British Museum", description: "Open at 10am — arrive early as it gets busy. Pick up a free floor plan at the entrance. The absolute highlights: Room 4 (Egyptian Sculptures — colossal statues), Room 63-73 (Egyptian mummies — riveting for all ages), Room 1 (the Rosetta Stone — the key that unlocked hieroglyphics), and Room 18 (Parthenon sculptures). With kids, the mummies and ancient weapons are usually a hit.", details: ["📍 Holborn or Tottenham Court Road Tube", "💡 Free entry. Plan 2 hours minimum — it's huge.", "🎯 Ask at the desk for the children's trail booklet — free and keeps kids engaged"] },
            { title: "Great Court & Reading Room", description: "Don't miss the spectacular Great Court — the world's largest covered public square, topped with a stunning glass-and-steel roof designed by Norman Foster. The Reading Room in the center is beautiful.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Grab before leaving — café near hotel", description: "The museum café is fine but pricey. Eat near your hotel or grab from a local café first.", meta: "£6-10pp · Covent Garden/Bloomsbury area" }
          ],
          tips: [{ type: "reddit", text: "British Museum's Egyptian collection is genuinely one of the best in the world, and it's completely free. The mummies are the highlight for kids — don't rush through. The Sutton Hoo helmet in Room 41 is another absolute stunner.", cite: "r/london" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Camden Market & Camden Lock", description: "Take the Northern line from Tottenham Court Road to Camden Town (about 15 minutes). Camden is unlike anywhere else in London — alternative, vibrant, and packed with energy. The Lock Market by the canal is the heart of it: covered stalls selling street food from around the world, vintage clothing, music, art, and curiosities. The lock itself is picturesque — narrow boats pass through.", details: ["📍 Camden Town Tube (Northern line)", "💡 The best part is the area around the lock — the indoor market halls and the canal. Allow 2-3 hours."] },
            { title: "Regent's Canal Towpath", description: "After exploring the market, walk along the Regent's Canal towpath west toward Primrose Hill. It's a peaceful escape — narrowboats moored along the water, locals walking dogs, willow trees trailing in the canal. Beautifully un-touristy.", details: [] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Camden Market Street Food", description: "Camden has London's best market street food in one place. The indoor food market at the Lock has stalls from every cuisine imaginable: Ethiopian injera, Japanese katsu curry, Mexican burritos, Caribbean jerk, Venezuelan arepas. Get everyone to pick something different.", meta: "£8-12pp · Camden Lock Market · Lots of options" }
          ],
          tips: [{ type: "tip", text: "Camden's street food market is genuinely world-class and very affordable. Skip the sit-down restaurants (overpriced) and go straight to the indoor food hall by the lock — that's where the real cooking is." }]
        },
        {
          label: "Late Afternoon",
          activities: [
            { title: "Primrose Hill (Optional)", description: "If legs allow, walk 15 minutes up to Primrose Hill for one of London's best panoramic skyline views — completely free, less crowded than the Eye, and a beautiful park where locals picnic on summer evenings. Worth it if the family has energy.", details: ["💡 On a clear June evening, the view takes in the Shard, Canary Wharf, the BT Tower, St Paul's, and the whole City skyline."] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Final Evening in Covent Garden", description: "Head back to base for your final full evening in London.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Flat Iron (Covent Garden)", description: "Exceptional quality steak at budget prices — the flat iron cut is £15 per person, served with a side salad. One of London's great bargain dining secrets. Casual, no reservations, and a glass of wine for adults is affordable. Perfect family dinner that feels like a treat without breaking the budget.", meta: "£15-20pp · 17-18 Henrietta St, Covent Garden · Walk-in only, quick queue" }
          ],
          tips: [{ type: "reddit", text: "Flat Iron in Covent Garden is incredible value — £15 gets you a genuinely great steak with a side salad. No reservations, the queue is usually only 15-20 minutes. It's a London institution for a reason.", cite: "r/london" }]
        }
      ]
    },
    {
      num: 5,
      title: "Morning Farewell Walk & Last London Moments",
      neighborhoods: "Covent Garden · The Strand · Embankment · South Bank",
      date: "Jun 7",
      mapPins: [
        { lat: 51.5129, lng: -0.1243, label: "Covent Garden — final morning", num: 1, cat: "activity", desc: "Soak up your neighborhood one last time" },
        { lat: 51.5100, lng: -0.1210, label: "The Strand", num: 2, cat: "activity", desc: "Historic street connecting Covent Garden to the City" },
        { lat: 51.5073, lng: -0.1220, label: "Embankment & Cleopatra's Needle", num: 3, cat: "activity", desc: "3,500-year-old Egyptian obelisk on the Thames bank" },
        { lat: 51.5033, lng: -0.1195, label: "London Eye area", num: 4, cat: "activity", desc: "Final views of Westminster from the South Bank" },
        { lat: 51.5075, lng: -0.1065, label: "South Bank — final walk", num: 5, cat: "activity", desc: "Last riverside stroll with St Paul's dome views" },
        { lat: 51.5080, lng: -0.1281, label: "Trafalgar Square farewell", num: 6, cat: "activity", desc: "One last look at the pigeons and Nelson's Column" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Covent Garden Breakfast & Wander", description: "Take your time over breakfast in Covent Garden — the piazza is peaceful in the early morning before the crowds arrive. Walk through the market halls and say goodbye to your London neighborhood.", details: [] },
            { title: "Walk to Embankment via The Strand", description: "Walk down The Strand (one of London's oldest and most historic streets) to the Embankment. Don't miss Cleopatra's Needle — a 3,500-year-old Egyptian obelisk sitting casually on the Thames bank. The riverside gardens are lovely for a final walk.", details: [] }
          ],
          meals: [
            { type: "☕ Final Breakfast", name: "Café in Covent Garden", description: "Sit down at any of the Covent Garden neighborhood cafés for a proper final breakfast. Or treat the family to a Full English at The Ivy Market Grill if budget allows — right on the piazza.", meta: "£10-20pp · Covent Garden area" }
          ],
          tips: [{ type: "tip", text: "London is at its most beautiful in the early morning — quiet streets, soft light, and the city waking up. Take an early walk before the tourists arrive." }]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "South Bank Final Walk", description: "Cross Waterloo Bridge (or Hungerford Bridge) for one final walk along the South Bank. The view from the riverside path — St Paul's dome, the Shard, Tower Bridge in the distance — is London's most beautiful backdrop. Stop at Waterloo Bridge for photos looking both ways.", details: [] },
            { title: "Trafalgar Square Farewell", description: "Walk back via Trafalgar Square. Let the kids climb the lion statues at the base of Nelson's Column (a London rite of passage). Take a final photo with Big Ben in the distance.", details: [] }
          ],
          meals: [
            { type: "🥗 Final Lunch", name: "Grab a sandwich and eat by the Thames", description: "From Pret A Manger, Itsu, or Leon (all over London, all affordable and good quality). Find a bench on the Embankment or South Bank and eat with Thames views. A perfect last London moment.", meta: "£6-10pp · Any central London location" }
          ],
          tips: [{ type: "reddit", text: "Even after many visits, I still get a lump in my throat leaving London. The South Bank walk from Waterloo to Blackfriars on a summer morning, with St Paul's glowing across the water — it never gets old.", cite: "r/london" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Head to Airport / Onward Travel", description: "From Covent Garden: Heathrow is easiest via Piccadilly line direct (45-60 min, ~£6pp with Oyster). Gatwick via Victoria and Gatwick Express (30 min from Victoria, ~£20). St Pancras International for Eurostar to Paris or Brussels is a 15-minute walk from Covent Garden.", details: ["💡 For Heathrow: allow 2 hours before your flight. Piccadilly line from Covent Garden Tube is direct.", "⚠️ Heathrow is massive — check your terminal and add 15 extra minutes to allow for internal transit."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Pick up any last-minute souvenirs at Heathrow duty-free rather than tourist shops in central London — better selection, similar prices. Or grab a Thorntons chocolate box in any supermarket." }]
        }
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
