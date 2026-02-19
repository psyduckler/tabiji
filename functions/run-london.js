const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771455924588_6ri9io",
  email: "bernard.j.huang@gmail.com",
  destination: "London, UK",
  start_date: "2026-04-22",
  end_date: "2026-04-26",
  group_size: "2",
  travel_style: "",
  dining: "Mix of everything",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-18T23:05:24.588Z",
  status: "pending"
};

const itineraryData = {
  destination: "London, UK",
  countryEmoji: "🇬🇧",
  title: "London in 5 Days: Icons, Hidden Gems & Incredible Eats",
  subtitle: "South Bank → Soho → Shoreditch → Notting Hill → Greenwich",
  description: "A carefully curated London adventure for two — blending the iconic landmarks with neighborhood gems most visitors miss. From world-class museums (free!) to buzzing food markets, cozy pubs, and riverside walks, this itinerary captures London at its best in spring.",
  duration: "5 days",
  dates: "Apr 22 – 26, 2026",
  budget: "Moderate",
  pace: "Balanced — full days with breathing room",
  bestFor: "Couples, first-timers & food lovers",
  highlights: [
    "Tower Bridge & Tower of London — 1,000 years of history",
    "Borough Market — London's legendary food market",
    "British Museum — free and mind-blowing",
    "Soho's best restaurants and cocktail bars",
    "Columbia Road Flower Market on Sunday (if timing works)",
    "Greenwich — Royal Observatory & the Prime Meridian",
    "Notting Hill's pastel streets and Portobello Road",
    "Thames riverside walk from Westminster to Tower Bridge",
    "West End theatre — world-class shows",
    "Hidden pubs with centuries of history"
  ],
  essentials: [
    { title: "🚇 Getting Around", text: "Get Oyster cards or use contactless bank cards on the Tube. Daily caps keep costs reasonable (~£8/day Zones 1-2). The Tube is fastest but buses show you more of the city. Walking is often best in central London." },
    { title: "💷 Money Tips", text: "Cards accepted almost everywhere. Tipping: 10-12.5% at restaurants (check if service charge is included). No tipping at pubs or cafés. ATMs (cashpoints) are everywhere but avoid the ones in tourist shops — they charge fees." },
    { title: "🌦️ April Weather", text: "Expect 10-16°C with a mix of sun, clouds, and occasional rain. Pack layers and a light waterproof jacket. London in spring is gorgeous — cherry blossoms, parks in bloom, and long evenings." },
    { title: "🏨 Where to Stay", text: "South Bank or Southwark for central location and value. Covent Garden or Soho for walkability to everything. Shoreditch for trendy vibes. Avoid staying near Heathrow — it's far from the action." },
    { title: "🎭 Theatre Tips", text: "Book West End shows on TodayTix app for discounts. TKTS booth in Leicester Square has same-day half-price tickets. Book popular shows (Hamilton, Wicked) 2-3 weeks ahead." },
    { title: "📱 Useful Apps", text: "Citymapper (best transport app), TodayTix (theatre), OpenTable/Resy (restaurants), Google Maps (walking routes)." }
  ],
  days: [
    {
      num: 1,
      title: "South Bank, Westminster & First London Evening",
      neighborhoods: "Westminster · South Bank · Waterloo",
      date: "Apr 22",
      mapPins: [
        { lat: 51.5014, lng: -0.1419, label: "Westminster & Big Ben", num: 1, cat: "activity", desc: "Iconic Parliament and Elizabeth Tower" },
        { lat: 51.5013, lng: -0.1196, label: "Westminster Bridge", num: 2, cat: "activity", desc: "Classic London view — Big Ben to your left, London Eye ahead" },
        { lat: 51.5033, lng: -0.1195, label: "London Eye", num: 3, cat: "activity", desc: "30-minute ride with panoramic city views" },
        { lat: 51.5076, lng: -0.0994, label: "Southbank Centre", num: 4, cat: "activity", desc: "Cultural hub with free exhibitions and river views" },
        { lat: 51.5074, lng: -0.0901, label: "Borough Market", num: 5, cat: "food", desc: "London's most famous food market" },
        { lat: 51.5099, lng: -0.1181, label: "The Savoy / Beaufort Bar", num: 6, cat: "nightlife", desc: "Art deco cocktail bar in a legendary hotel" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Westminster & Big Ben", description: "Start at Westminster Tube station for the iconic exit — step out and Big Ben is right there. Walk past the Houses of Parliament and through Parliament Square (statues of Churchill, Mandela, Gandhi).", details: ["📍 Westminster Tube station (Jubilee/District/Circle lines)"] },
            { title: "Cross Westminster Bridge", description: "Walk across for the classic postcard view — Big Ben behind you, London Eye ahead. Stop for photos at the midpoint.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Arrive by 10am to beat crowds. Big Ben's bells chime on the hour — time your visit to hear them." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "London Eye (Optional)", description: "The 30-minute rotation gives stunning 360° views over London. Pre-book online to skip the queue (£30-35pp). Best on a clear day.", details: ["💡 If it's overcast, skip this and spend more time at Borough Market instead."] },
            { title: "South Bank Walk → Borough Market", description: "Stroll along the Thames path past the Southbank Centre, National Theatre, and Tate Modern. End at Borough Market for a late lunch — London's best food in one place.", details: ["📍 About 30 min walk, or shorter if you skip sections"] }
          ],
          meals: [
            { type: "🍽️ Late Lunch", name: "Borough Market Grazing", description: "Don't sit down — graze! Padella for fresh pasta (expect a queue but it moves fast), Kappacasein for raclette, Bread Ahead for doughnuts, Neal's Yard Dairy for cheese.", meta: "£15-25 for two grazing · Open Wed-Sat, limited Mon-Tue" }
          ],
          tips: [{ type: "reddit", text: "Padella at Borough Market is the best pasta in London, full stop. The queue looks long but moves fast — 20 min max. Get the pici cacio e pepe.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Thames Sunset Walk", description: "Walk back along the South Bank as the city lights up. The stretch between Waterloo Bridge and Westminster is magical at dusk — Parliament glows gold across the river.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Padella (if skipped at lunch) or Brasserie Zédel", description: "Brasserie Zédel is a hidden gem — a grand Parisian-style brasserie underneath Piccadilly Circus with surprisingly affordable French classics (steak-frites £13!).", meta: "£20-35pp · Piccadilly Circus · No reservations needed" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Cocktails at The Beaufort Bar", description: "End your first night in style at The Savoy's art deco cocktail bar. Gold-leaf ceiling, live piano, impeccable drinks. Dress smart-casual.", details: ["💡 Cocktails £18-22. No reservation needed but arrive by 9pm for seats."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Jet lag working in your favor — London evenings are long in late April (sunset ~8:15pm). Take advantage!" }]
        }
      ]
    },
    {
      num: 2,
      title: "Royal London & Soho Night Out",
      neighborhoods: "St James's · Mayfair · Soho · Covent Garden",
      date: "Apr 23",
      mapPins: [
        { lat: 51.5014, lng: -0.1419, label: "Buckingham Palace", num: 1, cat: "activity", desc: "Royal residence with Changing of the Guard" },
        { lat: 51.5046, lng: -0.1369, label: "St James's Park", num: 2, cat: "activity", desc: "London's most beautiful royal park with pelicans" },
        { lat: 51.5194, lng: -0.1270, label: "British Museum", num: 3, cat: "activity", desc: "World-class museum — free entry" },
        { lat: 51.5131, lng: -0.1370, label: "Soho", num: 4, cat: "food", desc: "London's dining and nightlife epicenter" },
        { lat: 51.5117, lng: -0.1240, label: "Covent Garden", num: 5, cat: "activity", desc: "Street performers, shops, and the Royal Opera House" },
        { lat: 51.5131, lng: -0.1317, label: "Chinatown", num: 6, cat: "food", desc: "Authentic dim sum and late-night eats" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Buckingham Palace & Changing of the Guard", description: "Arrive by 10:30am to get a good spot for the Changing of the Guard (11am, check schedule — not daily). Even without the ceremony, the palace and Victoria Memorial are impressive.", details: ["💡 Check the schedule at householddivision.org.uk — it doesn't happen every day. April typically has frequent ceremonies."] },
            { title: "St James's Park", description: "London's prettiest park is right next to the palace. Walk through to see the pelicans (fed daily at 2:30pm), the lake, and stunning views of Buckingham Palace from the bridge.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "The Wolseley", description: "Grand European café-restaurant on Piccadilly. The full English breakfast here is legendary. Book ahead or arrive early.", meta: "£15-25pp · Piccadilly · Reserve on OpenTable" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "British Museum", description: "One of the world's greatest museums — and it's free. Must-sees: Rosetta Stone, Egyptian mummies, Parthenon Marbles, Sutton Hoo treasure. You could spend days here but 2-3 hours hits the highlights.", details: ["📍 Great Russell St · Free entry · Open daily 10-5", "💡 Grab a free map at the entrance. Start with Room 4 (Egyptian sculptures) and Room 18 (Parthenon)."] },
            { title: "Covent Garden Stroll", description: "Walk south to Covent Garden for street performers in the piazza, the Apple Market, and a coffee break. Peek into the Royal Opera House lobby (free).", details: [] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "Dishoom (Covent Garden)", description: "Bombay-inspired café that's become a London institution. The bacon naan roll and black daal are iconic. Go at lunch to avoid the 2-hour dinner queues.", meta: "£15-20pp · Covent Garden · Walk-ins easier at lunch" }
          ],
          tips: [{ type: "reddit", text: "Dishoom is worth the hype. The black daal has been simmering for 24 hours. Get the chicken ruby and a mango lassi too.", cite: "r/londonfood" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Soho Dinner & Drinks", description: "Soho is London's beating heart for food and nightlife. Narrow streets packed with restaurants, bars, and character. Wander Dean Street, Frith Street, and Old Compton Street.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Bao Soho", description: "Tiny Taiwanese spot — the fluffy bao buns are addictive. Classic pork, fried chicken, or lamb shoulder. Always a queue but it moves fast.", meta: "£20-30 for two · 53 Lexington St · No reservations" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "West End Show or Soho Cocktails", description: "Option A: Catch a West End show (Shaftesbury Avenue theatres are steps away). Option B: Bar hop through Soho — try Bar Termini for negronis, Swift for whisky cocktails, or The French House for a pint of history.", details: ["💡 TodayTix app often has same-day discounts. Or try the TKTS booth in Leicester Square."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The French House in Soho only serves half pints — it's a deliberate choice. De Gaulle drank here during WWII. The atmosphere is unbeatable." }]
        }
      ]
    },
    {
      num: 3,
      title: "Tower of London, East End & Shoreditch",
      neighborhoods: "City of London · Tower Hamlets · Shoreditch · Spitalfields",
      date: "Apr 24",
      mapPins: [
        { lat: 51.5081, lng: -0.0759, label: "Tower of London", num: 1, cat: "activity", desc: "1,000-year-old fortress with Crown Jewels" },
        { lat: 51.5055, lng: -0.0754, label: "Tower Bridge", num: 2, cat: "activity", desc: "Iconic Victorian bridge with glass walkway" },
        { lat: 51.5201, lng: -0.0750, label: "Spitalfields Market", num: 3, cat: "food", desc: "Historic covered market with great food stalls" },
        { lat: 51.5246, lng: -0.0790, label: "Brick Lane", num: 4, cat: "food", desc: "Famous for curry houses, vintage shops, and street art" },
        { lat: 51.5265, lng: -0.0837, label: "Shoreditch", num: 5, cat: "nightlife", desc: "East London's creative hub — bars, galleries, street art" },
        { lat: 51.5139, lng: -0.0755, label: "Sky Garden", num: 6, cat: "activity", desc: "Free rooftop garden with panoramic London views" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tower of London", description: "Arrive at opening (10am) to beat the crowds. Join a free Yeoman Warder (Beefeater) tour — they're hilarious and incredibly knowledgeable. See the Crown Jewels, the White Tower, and the spot where Anne Boleyn lost her head.", details: ["💡 £33pp — prebook on the official website for timed entry. Allow 2.5-3 hours.", "📍 Tower Hill Tube station"] },
            { title: "Tower Bridge", description: "Walk across — it's free and the views are great. The glass floor walkway and Victorian engine rooms cost £12 if you want to go inside.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The Beefeater tours are the highlight — funny, dark, and full of incredible stories. Don't skip them." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sky Garden", description: "Free 360° views from the top of the 'Walkie Talkie' building. Book free tickets online in advance — they release them 3 weeks ahead and go fast.", details: ["💡 Book at skygarden.london — free but must pre-book. Try for a 2-3pm slot."] },
            { title: "Spitalfields & Brick Lane", description: "Walk through Spitalfields Market (food, vintage, crafts) into Brick Lane. Street art everywhere, vintage shops, and London's curry mile. Perfect for wandering.", details: [] }
          ],
          meals: [
            { type: "🍛 Lunch", name: "Gunpowder (Spitalfields)", description: "Modern Indian small plates — the spiced venison doughnut and Kashmiri lamb chops are extraordinary. Small spot, big flavors.", meta: "£25-35pp · 11 White's Row · Book ahead" }
          ],
          tips: [{ type: "reddit", text: "Skip the Brick Lane curry touts who stand outside restaurants calling you in. The best food on Brick Lane isn't the curry houses — it's Beigel Bake (24hr, salt beef beigel, £5) and the street food stalls on weekends.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Shoreditch Evening", description: "Shoreditch comes alive at night. Start with dinner, then explore the bar scene — rooftop bars, speakeasies, craft cocktail spots, and live music.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Smokestak", description: "Low-and-slow BBQ in a railway arch. The brisket is the best in London. Smoky, tender, perfect. Industrial-chic setting.", meta: "£30-40pp · 35 Sclater St · Book on Resy" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Shoreditch Bar Crawl", description: "Happiness Forgets (basement speakeasy, incredible cocktails), Discount Suit Company (bar hidden in a suit shop entrance), or Cargo (club under the railway arches). Shoreditch has London's best nightlife density.", details: ["💡 Happiness Forgets is small — book a table or arrive before 8pm."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "End the night at Beigel Bake on Brick Lane — open 24 hours. A salt beef beigel at 2am is a London rite of passage." }]
        }
      ]
    },
    {
      num: 4,
      title: "Notting Hill, Hyde Park & Kensington",
      neighborhoods: "Notting Hill · Kensington · Hyde Park · Chelsea",
      date: "Apr 25",
      mapPins: [
        { lat: 51.5157, lng: -0.2009, label: "Portobello Road Market", num: 1, cat: "activity", desc: "Antiques, vintage, and street food market" },
        { lat: 51.5125, lng: -0.2060, label: "Notting Hill", num: 2, cat: "activity", desc: "Pastel-colored houses and charming bookshops" },
        { lat: 51.5073, lng: -0.1657, label: "Hyde Park", num: 3, cat: "activity", desc: "London's grandest park — 350 acres" },
        { lat: 51.4966, lng: -0.1764, label: "V&A Museum", num: 4, cat: "activity", desc: "World's leading museum of art and design — free" },
        { lat: 51.4942, lng: -0.1760, label: "Natural History Museum", num: 5, cat: "activity", desc: "Stunning building with incredible collections — free" },
        { lat: 51.5098, lng: -0.1949, label: "Churchill Arms Pub", num: 6, cat: "food", desc: "London's most photographed pub — covered in flowers" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Notting Hill & Portobello Road", description: "Wander the pastel-colored streets of Notting Hill. Portobello Road Market is best on Saturdays (this is a Wednesday, so it'll be quieter but still charming). Browse antique shops, vintage clothing, and the iconic bookshops.", details: ["📍 Notting Hill Gate or Ladbroke Grove Tube", "💡 Wednesday: shops open, market is smaller. Still lovely for photos and browsing."] },
            { title: "Churchill Arms Pub Photo Stop", description: "Even if you don't go in (yet), snap a photo of this incredibly flower-covered pub — it's draped in blossoms, especially gorgeous in April.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Farm Girl Café", description: "Instagram-famous but genuinely good. Excellent coffee, açaí bowls, and avocado toast. Bright, pretty space.", meta: "£12-18pp · Notting Hill · Walk-in" }
          ],
          tips: [{ type: "tip", text: "The best photo streets in Notting Hill: Lancaster Road, Westbourne Park Road, and the pastel crescents off Portobello Road." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hyde Park & Kensington Gardens", description: "Walk through Hyde Park — it's magnificent in spring. See the Serpentine, the Diana Memorial Fountain, and Kensington Palace (where William and Kate live). April means blooming flowers everywhere.", details: [] },
            { title: "V&A Museum or Natural History Museum", description: "Both are free and spectacular. V&A for art, fashion, and design (the Medieval & Renaissance galleries are jaw-dropping). Natural History Museum for the iconic Hintze Hall with the blue whale skeleton.", details: ["💡 Pick one — trying both in an afternoon is rushing it. V&A is less crowded."] }
          ],
          meals: [
            { type: "🥗 Lunch", name: "The Magazine Restaurant (Serpentine Gallery)", description: "Designed by Zaha Hadid inside Hyde Park. Beautiful modern space with a seasonal British menu. Perfect park-side lunch.", meta: "£25-35pp · Hyde Park · Book on OpenTable" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Chelsea & King's Road Stroll", description: "Walk south through Kensington into Chelsea. King's Road has great shops, and the Saatchi Gallery (free) is worth a look if there's a good exhibition on.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "The Five Fields", description: "Michelin-starred tasting menu in Chelsea. Seasonal British cuisine at its finest — the kitchen garden supplies many of the ingredients. Splurge night for two.", meta: "£95pp tasting menu · Chelsea · Book well ahead" }
          ],
          tips: [{ type: "tip", text: "If Five Fields is booked, try The Harwood Arms in Fulham — London's only Michelin-starred pub. Incredible British food, way more relaxed." }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Churchill Arms for a Pint", description: "Circle back to the Churchill Arms — step inside for a proper pint in one of London's most atmospheric pubs. The back room is a full Thai restaurant (surprisingly great). The front bar is pure old-school London.", details: [] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Churchill Arms is touristy outside but the locals still drink there. The Thai food in the back room is legitimately good and cheap for the area.", cite: "r/london" }]
        }
      ]
    },
    {
      num: 5,
      title: "Greenwich & Farewell London",
      neighborhoods: "Greenwich · Bermondsey · London Bridge",
      date: "Apr 26",
      mapPins: [
        { lat: 51.4769, lng: -0.0005, label: "Royal Observatory Greenwich", num: 1, cat: "activity", desc: "Stand on the Prime Meridian — 0° longitude" },
        { lat: 51.4826, lng: -0.0096, label: "Cutty Sark", num: 2, cat: "activity", desc: "Historic clipper ship" },
        { lat: 51.4813, lng: -0.0066, label: "Greenwich Market", num: 3, cat: "food", desc: "Covered market with street food and crafts" },
        { lat: 51.4791, lng: -0.0014, label: "Greenwich Park", num: 4, cat: "activity", desc: "Hilltop views over the Thames and Canary Wharf" },
        { lat: 51.5015, lng: -0.0822, label: "Maltby Street Market", num: 5, cat: "food", desc: "Locals' alternative to Borough Market — under railway arches" },
        { lat: 51.5075, lng: -0.1065, label: "Oxo Tower / South Bank", num: 6, cat: "food", desc: "Farewell drinks with river views" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "DLR to Greenwich", description: "Take the DLR (Docklands Light Railway) from central London — sit at the front for driver's-eye views through Canary Wharf. Or take the Thames Clipper river bus for a scenic ride.", details: ["💡 Thames Clipper from Westminster or Embankment pier — Oyster cards work. About 30 min and gorgeous."] },
            { title: "Cutty Sark & Greenwich Market", description: "Start at the Cutty Sark — the famous tea clipper ship is beautifully restored. Then walk through Greenwich Market for coffee and browsing.", details: ["📍 Cutty Sark DLR station"] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Greenwich Market Food Stalls", description: "Excellent street food — Ethiopian injera, Thai curry, wood-fired pizza, and great coffee. Graze your way through.", meta: "£10-15pp · Greenwich Market · Open daily" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Royal Observatory & Prime Meridian", description: "Climb the hill through Greenwich Park to the Royal Observatory. Stand with one foot in each hemisphere at the Prime Meridian Line. The views from the hilltop over the Thames, Queen's House, and Canary Wharf are iconic.", details: ["💡 £18pp for the Observatory. The park and Prime Meridian courtyard photo (outside) are free. The hill walk takes 10-15 min."] },
            { title: "Greenwich Park", description: "Spread out on the grass and enjoy the view. In April, the park is full of cherry blossoms and spring flowers. A perfect peaceful moment before heading back to the city.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "The Old Brewery (Greenwich)", description: "Craft beer and seasonal British food in the old brewery building at the edge of Greenwich Park. Great burgers and Sunday roast vibes.", meta: "£18-25pp · Old Royal Naval College" }
          ],
          tips: [{ type: "reddit", text: "The view from the top of Greenwich Park is one of the best in London and most tourists never make it here because they stay in Zone 1.", cite: "r/london" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Drinks on the South Bank", description: "Head back to central London for a final evening. Walk along the South Bank as the sun sets — the Thames path from Waterloo to Blackfriars is magical at golden hour.", details: [] }
          ],
          meals: [
            { type: "🍽️ Farewell Dinner", name: "The Anchor Bankside", description: "Historic riverside pub dating to the 1600s (Samuel Pepys watched the Great Fire from here). Proper British food, great ales, and Thames views. A fitting farewell.", meta: "£25-35pp · Bankside · Walk-in or book" }
          ],
          tips: []
        },
        {
          label: "Late Night",
          activities: [
            { title: "Final Thames Walk", description: "One last stroll along the river. The South Bank at night — St Paul's lit up across the water, the Shard gleaming, Tower Bridge glowing — is London at its most beautiful. Soak it in.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "If you want one last cocktail, Dandelyan at the Mondrian hotel (now Lyaness) on the South Bank has inventive drinks with river views." }]
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
